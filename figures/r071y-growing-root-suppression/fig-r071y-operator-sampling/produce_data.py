#!/usr/bin/env python3
"""Extract and independently reconstruct the R0.71Y figure data.

The committed-form R0.71Y certificate JSON files are the only scientific
inputs.  This script does not rerun the theorem audits or a PDE solver.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import time
from zoneinfo import ZoneInfo

import numpy as np


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")
FIELDS = (
    "panel",
    "series",
    "N",
    "M",
    "h",
    "deltaObs",
    "x",
    "y",
    "rawValue",
    "referenceValue",
    "unit",
    "formula",
    "evidenceClass",
    "source",
    "note",
)


def timestamp() -> str:
    return datetime.now(TIMEZONE).isoformat(timespec="milliseconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_ndjson(path: Path, payload: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": timestamp(), **payload}, sort_keys=True) + "\n")


def resource_record(stage: str, started: float, **details: object) -> dict[str, object]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "stage": stage,
        "elapsedSeconds": time.perf_counter() - started,
        "pid": os.getpid(),
        "logicalCpuCount": os.cpu_count(),
        "loadAverage1m5m15m": list(os.getloadavg()),
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
        **details,
    }


def load_source(config: dict[str, object], key: str) -> tuple[Path, dict[str, object]]:
    relative = Path(config["sourceCertificates"][key])
    path = REPOSITORY / relative
    if not path.is_file():
        raise FileNotFoundError(f"source certificate is missing: {relative}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("status") != "passed":
        raise RuntimeError(f"source certificate did not pass: {relative}")
    if payload.get("release") != config["release"]:
        raise RuntimeError(f"source certificate release differs from config: {relative}")
    if not all(bool(check["passed"]) for check in payload["checks"]):
        raise RuntimeError(f"at least one source check failed: {relative}")
    return path, payload


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), np.finfo(float).tiny)


def fit_power(x_values: list[float], y_values: list[float]) -> dict[str, float]:
    x = np.log(np.asarray(x_values, dtype=float))
    y = np.log(np.asarray(y_values, dtype=float))
    slope, intercept = np.polyfit(x, y, 1)
    fitted = slope * x + intercept
    residual = y - fitted
    centered = y - np.mean(y)
    denominator = float(np.dot(centered, centered))
    return {
        "power": float(slope),
        "logCoefficient": float(intercept),
        "rSquared": 1.0 - float(np.dot(residual, residual)) / denominator if denominator else 1.0,
    }


def lattice_cost(n_value: int) -> float:
    m_value = 2 * n_value + 1
    return float(m_value * (m_value + 1) * (2 * m_value + 1) / 6)


def add_row(
    rows: list[dict[str, object]],
    *,
    panel: str,
    series: str,
    n_value: int,
    h: float,
    delta_obs: float,
    y: float,
    raw_value: float,
    reference_value: float,
    unit: str,
    formula: str,
    evidence_class: str,
    source: str,
    note: str,
) -> None:
    values = (float(n_value), y, raw_value, reference_value, h, delta_obs)
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f"non-finite plot row for {panel}/{series}: {values}")
    if n_value <= 0 or y <= 0.0 or raw_value <= 0.0 or reference_value <= 0.0 or h < 0.0 or delta_obs < 0.0:
        raise ValueError(f"invalid positive plot row for {panel}/{series}: {values}")
    rows.append(
        {
            "panel": panel,
            "series": series,
            "N": n_value,
            "M": 2 * n_value + 1,
            "h": h,
            "deltaObs": delta_obs,
            "x": float(n_value),
            "y": y,
            "rawValue": raw_value,
            "referenceValue": reference_value,
            "unit": unit,
            "formula": formula,
            "evidenceClass": evidence_class,
            "source": source,
            "note": note,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    (ROOT / "progress.ndjson").write_text("", encoding="utf-8")
    (ROOT / "resource-log.ndjson").write_text("", encoding="utf-8")
    append_ndjson(ROOT / "progress.ndjson", {"stage": "producer-start"})

    config = json.loads(args.config.read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    primary_path, primary = load_source(config, "primary")
    independent_path, independent = load_source(config, "independent")
    primary_source = str(primary_path.relative_to(REPOSITORY))
    independent_source = str(independent_path.relative_to(REPOSITORY))

    n_values = [int(value) for value in primary["parameters"]["NValues"]]
    lattice_rows = primary["latticeRows"]
    if [int(row["N"]) for row in lattice_rows] != n_values:
        raise RuntimeError("primary lattice grid differs from its parameter grid")
    if any(int(row["M"]) != 2 * int(row["N"]) + 1 for row in lattice_rows):
        raise RuntimeError("source carrier counts do not satisfy M=2N+1")

    b_rate = 2.0 * float(primary["parameters"]["nu"]) * float(primary["parameters"]["d"]) ** 2
    fixed_delta = float(config["fixedDeltaObs"])
    fixed_gap = float(config["fixedGap"])
    envelope_source = next(
        row for row in primary["envelopeRows"] if float(row["deltaObs"]) == fixed_delta
    )
    no_separation_values = [float(row["upperEnvelope"]) for row in envelope_source["values"]]
    if [int(row["N"]) for row in envelope_source["values"]] != n_values:
        raise RuntimeError("fixed-coupling envelope grid differs from lattice grid")

    optimizer_max = float(primary["optimizer"]["maximum"])
    multiplier_ratio_upper = float(primary["multiplierRatioUpper"])
    source_errors: list[float] = []
    independent_errors: list[float] = []
    fixed_separated_values: list[float] = []
    quasiuniform_values: list[float] = []
    for source_row, envelope_value in zip(lattice_rows, no_separation_values, strict=True):
        n_value = int(source_row["N"])
        m_value = 2 * n_value + 1
        ks_value = lattice_cost(n_value)
        factor = n_value * m_value / ks_value
        upper = 3.0 / (4.0 * n_value)
        source_errors.extend(
            [
                relative_error(float(source_row["minimumKs"]), ks_value),
                relative_error(float(source_row["NMOverMinimumKs"]), factor),
                relative_error(float(source_row["threeOverFourN"]), upper),
            ]
        )
        expected_envelope = optimizer_max * factor * fixed_delta ** (4.0 / 3.0) * multiplier_ratio_upper ** (1.0 / 3.0)
        source_errors.append(relative_error(envelope_value, expected_envelope))
        fixed_separated_values.append(m_value / (b_rate * fixed_gap * ks_value))
        quasiuniform_values.append(m_value / (b_rate * (1.0 / n_value) * ks_value))
        append_ndjson(
            ROOT / "progress.ndjson",
            {
                "stage": "theorem-row-reconstructed",
                "N": n_value,
                "latticeFactor": factor,
                "fixedDeltaObsEnvelope": envelope_value,
            },
        )

    independent_index = {int(row["N"]): row for row in independent["rows"]}
    for n_value in sorted(independent_index):
        expected_ratio = (n_value * (2 * n_value + 1) / lattice_cost(n_value)) / (3.0 / (4.0 * n_value))
        independent_errors.append(
            relative_error(float(independent_index[n_value]["latticeBoundRatio"]), expected_ratio)
        )
    determinant_check = next(check for check in independent["checks"] if check["name"] == "equal-grid determinant factorization")
    independent_errors.append(
        relative_error(
            float(determinant_check["value"]["maxRelativeError"]),
            max(float(row["relativeError"]) for row in independent["equalGridRows"]),
        )
    )
    maximum_source_error = max(source_errors, default=0.0)
    maximum_independent_error = max(independent_errors, default=0.0)
    if maximum_source_error > 2.0e-14:
        raise RuntimeError(f"source formulas differ from reconstruction by {maximum_source_error:.3e}")
    if maximum_independent_error > 2.0e-14:
        raise RuntimeError(f"independent rows differ from reconstruction by {maximum_independent_error:.3e}")

    rows: list[dict[str, object]] = []
    for source_row in lattice_rows:
        n_value = int(source_row["N"])
        factor = float(source_row["NMOverMinimumKs"])
        upper = float(source_row["threeOverFourN"])
        add_row(
            rows,
            panel="A",
            series="exact minimum-lattice factor NM/Ks",
            n_value=n_value,
            h=0.0,
            delta_obs=0.0,
            y=factor,
            raw_value=factor,
            reference_value=upper,
            unit="dimensionless theorem factor",
            formula="N(2N+1)/sum_{j=1}^{2N+1} j^2",
            evidence_class="exact analytic lattice identity",
            source=primary_source,
            note="unit carrier phases; minimum over distinct positive integer carrier frequencies",
        )
        add_row(
            rows,
            panel="A",
            series="analytic upper bound 3/(4N)",
            n_value=n_value,
            h=0.0,
            delta_obs=0.0,
            y=upper,
            raw_value=upper,
            reference_value=factor,
            unit="dimensionless theorem bound",
            formula="3/(4N)",
            evidence_class="exact analytic upper bound",
            source=primary_source,
            note="upper bound for the minimum-lattice factor; not a fitted trend",
        )

    references = {
        "no separation; fixed delta_obs=1/8": no_separation_values[0],
        "separated; fixed h=0.05": fixed_separated_values[0],
        "separated; h=N^-1": quasiuniform_values[0],
    }
    for index, n_value in enumerate(n_values):
        series_payloads = (
            (
                "no separation; fixed delta_obs=1/8",
                0.0,
                no_separation_values[index],
                "optimized selected-root upper envelope / N=1 value",
                "C(delta_obs) N M / K_s, normalized at N=1",
                "exact nonlinear selected-root theorem envelope",
                "fixed observation coupling; selected roots; unit phases and full enstrophy floors",
            ),
            (
                "separated; fixed h=0.05",
                fixed_gap,
                fixed_separated_values[index],
                "separated upper-envelope factor / N=1 value",
                "[M/(b h K_s)] / value at N=1",
                "exact nonlinear separated-root theorem envelope",
                "fixed scaled separation; common theorem constants cancel under normalization",
            ),
            (
                "separated; h=N^-1",
                1.0 / n_value,
                quasiuniform_values[index],
                "separated upper-envelope factor / N=1 value",
                "[M/(b N^-1 K_s)] / value at N=1",
                "exact nonlinear separated-root theorem envelope",
                "quasi-uniform roots in a fixed scaled interval; same normalized N-law as no separation",
            ),
        )
        for series, h_value, raw_value, unit, formula, evidence_class, note in series_payloads:
            add_row(
                rows,
                panel="B",
                series=series,
                n_value=n_value,
                h=h_value,
                delta_obs=fixed_delta,
                y=raw_value / references[series],
                raw_value=raw_value,
                reference_value=references[series],
                unit=unit,
                formula=formula,
                evidence_class=evidence_class,
                source=primary_source,
                note=note,
            )

    inverse_rows = primary["equalGridInverseLower"]
    if [int(row["N"]) for row in inverse_rows] != [int(value) for value in config["equalGridNValues"]]:
        raise RuntimeError("equal-grid inverse audit grid differs from config")
    inverse_formula_errors: list[float] = []
    for source_row in inverse_rows:
        n_value = int(source_row["N"])
        gap = n_value ** -3.0
        r_max = n_value + 1.0
        base = b_rate * gap * r_max**2
        expected_log = -math.log10(gap) - 0.5 * (n_value - 1) * math.log10(base)
        recorded_log = float(source_row["log10InverseLower"])
        inverse_formula_errors.extend(
            [
                relative_error(float(source_row["bGapRmaxSquared"]), base),
                relative_error(recorded_log, expected_log),
            ]
        )
        add_row(
            rows,
            panel="C",
            series="equal-grid inverse lower bound; h=N^-3",
            n_value=n_value,
            h=gap,
            delta_obs=0.0,
            y=recorded_log,
            raw_value=10.0**recorded_log,
            reference_value=base,
            unit="log10 lower bound for ||M^-1||_2",
            formula="log10[h^-1 (b h (N+1)^2)^(-(N-1)/2)]",
            evidence_class="exact determinant-based conditioning lower bound",
            source=primary_source,
            note="canonical r_l=l; conditioning lower bound is not an upper bound on nonlinear IFT radius",
        )
        append_ndjson(
            ROOT / "progress.ndjson",
            {"stage": "equal-grid-bound-reconstructed", "N": n_value, "log10InverseLower": recorded_log},
        )
    maximum_inverse_error = max(inverse_formula_errors, default=0.0)
    if maximum_inverse_error > 2.0e-14:
        raise RuntimeError(f"equal-grid formula differs from source by {maximum_inverse_error:.3e}")

    fits = {
        "latticeFactor": fit_power(n_values[-6:], [float(row["NMOverMinimumKs"]) for row in lattice_rows[-6:]]),
        "noSeparationFixedDeltaObs": fit_power(n_values[-6:], no_separation_values[-6:]),
        "separatedFixedGap": fit_power(n_values[-6:], fixed_separated_values[-6:]),
        "separatedQuasiuniformGap": fit_power(n_values[-6:], quasiuniform_values[-6:]),
    }
    source_fit_values = {
        "latticeFactor": float(primary["latticeTailPower"]),
        "noSeparationFixedDeltaObs": float(envelope_source["tailPower"]),
        "separatedFixedGap": float(primary["separatedRootEnvelope"]["fixedGapTailPower"]),
        "separatedQuasiuniformGap": float(primary["separatedRootEnvelope"]["quasiuniformGapTailPower"]),
    }
    maximum_fit_difference = max(abs(fits[key]["power"] - source_fit_values[key]) for key in fits)
    if maximum_fit_difference > 2.0e-12:
        raise RuntimeError(f"independent tail fits differ from source by {maximum_fit_difference:.3e}")

    with (ROOT / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    data_payload = {
        "schemaVersion": "1.0.0",
        "release": config["release"],
        "figureId": config["figureId"],
        "rowCount": len(rows),
        "fields": list(FIELDS),
        "rows": rows,
    }
    (ROOT / "data.json").write_text(json.dumps(data_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    results = {
        "release": config["release"],
        "figureId": config["figureId"],
        "status": "passed",
        "sourceCertificates": {
            "primary": {"path": primary_source, "sha256": sha256(primary_path), "checks": len(primary["checks"])},
            "independent": {"path": independent_source, "sha256": sha256(independent_path), "checks": len(independent["checks"]), "seed": independent.get("seed")},
        },
        "parameters": {
            "NValues": n_values,
            "fixedDeltaObs": fixed_delta,
            "fixedGap": fixed_gap,
            "bRate": b_rate,
            "equalGridGapLaw": config["equalGridGapLaw"],
        },
        "derivedFigureFits": fits,
        "sourceFitValues": source_fit_values,
        "equalGridInverseRows": inverse_rows,
        "crossChecks": {
            "maximumPrimaryFormulaRelativeError": maximum_source_error,
            "maximumIndependentRowRelativeError": maximum_independent_error,
            "maximumEqualGridFormulaRelativeError": maximum_inverse_error,
            "maximumTailPowerDifference": maximum_fit_difference,
            "independentFiniteMatrixCheckCount": len(independent["checks"]),
            "independentEqualGridMinimumBoundRatio": min(float(row["boundRatio"]) for row in independent["equalGridRows"]),
        },
        "claimBoundary": contract["claimBoundary"],
        "producerWallSeconds": time.perf_counter() - started,
    }
    (ROOT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    metadata = {
        "schemaVersion": "1.0.0",
        "release": config["release"],
        "figureId": config["figureId"],
        "generatedAt": timestamp(),
        "rowCount": len(rows),
        "sourceCertificates": [
            {"label": "primary", "path": primary_source, "bytes": primary_path.stat().st_size, "sha256": sha256(primary_path)},
            {"label": "independent", "path": independent_source, "bytes": independent_path.stat().st_size, "sha256": sha256(independent_path)},
        ],
        "configSha256": sha256(args.config),
        "contractSha256": sha256(ROOT / "contract.json"),
        "dataCsvSha256": sha256(ROOT / "data.csv"),
        "dataJsonSha256": sha256(ROOT / "data.json"),
        "resultsSha256": sha256(ROOT / "results.json"),
        "evidenceMap": {
            "A": "exact lattice identity and analytic upper bound",
            "B": "exact nonlinear selected-root theorem envelopes, normalized only for N-law comparison",
            "C": "exact determinant-based equal-grid inverse lower bound",
        },
        "claimBoundary": contract["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    elapsed = time.perf_counter() - started
    append_ndjson(ROOT / "progress.ndjson", {"stage": "producer-complete", "rowCount": len(rows), "elapsedSeconds": elapsed})
    append_ndjson(
        ROOT / "resource-log.ndjson",
        resource_record("producer-complete", started, rowCount=len(rows)),
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "rows": len(rows),
                "tailPowers": {key: value["power"] for key, value in fits.items()},
                "equalGridLog10Range": [float(inverse_rows[0]["log10InverseLower"]), float(inverse_rows[-1]["log10InverseLower"])],
                "elapsedSeconds": elapsed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
