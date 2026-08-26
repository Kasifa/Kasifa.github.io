#!/usr/bin/env python3
"""Extract and independently reconstruct the R0.71Z journal-figure data."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time
from zoneinfo import ZoneInfo

import matplotlib
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")
FIELDS = (
    "panel",
    "series",
    "M",
    "N",
    "eta",
    "etaPower",
    "R",
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


def load_primary(path: Path, release: str) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("release") != release or payload.get("status") != "passed":
        raise RuntimeError(f"primary certificate is not a passed {release} payload")
    checks = payload.get("checks", [])
    if not checks or not all(bool(check.get("passed")) for check in checks):
        raise RuntimeError("primary certificate contains a failed check")
    return payload


def load_independent(path: Path, release: str) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("release") != release or payload.get("passed") is not True:
        raise RuntimeError(f"independent certificate is not a passed {release} payload")
    checks = payload.get("checks", [])
    if not checks or not all(bool(check.get("passed")) for check in checks):
        raise RuntimeError("independent certificate contains a failed check")
    if int(payload.get("passedCheckCount", -1)) != int(payload.get("checkCount", -2)):
        raise RuntimeError("independent certificate check counts disagree")
    return payload


def add_row(
    rows: list[dict[str, object]],
    *,
    panel: str,
    series: str,
    m_value: int = 0,
    n_value: int = 0,
    eta: float = 0.0,
    eta_power: float = 0.0,
    r_value: float = 0.0,
    x: float,
    y: float,
    raw_value: float,
    reference_value: float,
    unit: str,
    formula: str,
    evidence_class: str,
    source: str,
    note: str,
) -> None:
    numeric = (x, y, raw_value, reference_value, eta, eta_power, r_value)
    if not all(math.isfinite(value) for value in numeric):
        raise ValueError(f"non-finite row for {panel}/{series}: {numeric}")
    if x <= 0.0 or y <= 0.0 or raw_value <= 0.0 or reference_value <= 0.0:
        raise ValueError(f"non-positive plotted row for {panel}/{series}: {numeric}")
    rows.append(
        {
            "panel": panel,
            "series": series,
            "M": m_value,
            "N": n_value,
            "eta": eta,
            "etaPower": eta_power,
            "R": r_value,
            "x": x,
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
    release = str(config["release"])
    primary_path = REPOSITORY / Path(config["sourceCertificates"]["primary"])
    independent_path = REPOSITORY / Path(config["sourceCertificates"]["independent"])
    primary = load_primary(primary_path, release)
    independent = load_independent(independent_path, release)
    primary_source = str(primary_path.relative_to(REPOSITORY))
    independent_source = str(independent_path.relative_to(REPOSITORY))

    parameters = primary["parameters"]
    m_values = [int(value) for value in parameters["MValues"]]
    lattice_rows = primary["lattice"]["rows"]
    if [int(row["M"]) for row in lattice_rows] != m_values:
        raise RuntimeError("certificate lattice grid differs from parameter M grid")
    if any(m < 3 or m % 2 != 1 for m in m_values):
        raise RuntimeError("figure expects odd carrier counts M=2N+1")

    optimizer = float(primary["amplitudeOptimizer"]["maximum"])
    c_kappa = float(primary["BVConstant"]["value"])
    lambda0_l = float(parameters["lambda0L"])
    multiplier_upper = float(primary["multiplierRatio"]["upperConstant"])
    common_multiplier = optimizer * multiplier_upper ** (1.0 / 3.0)

    source_formula_errors: list[float] = []
    lattice_factor: dict[int, float] = {}
    lattice_upper: dict[int, float] = {}
    for source_row in lattice_rows:
        m_value = int(source_row["M"])
        ks = m_value * (m_value + 1) * (2 * m_value + 1) / 6.0
        exact = m_value / ks
        upper = 3.0 / m_value**2
        source_formula_errors.extend(
            [
                relative_error(float(source_row["minimumKs"]), ks),
                relative_error(float(source_row["MOverMinimumKs"]), exact),
                relative_error(float(source_row["upperThreeOverM2"]), upper),
            ]
        )
        lattice_factor[m_value] = exact
        lattice_upper[m_value] = upper
        append_ndjson(
            ROOT / "progress.ndjson",
            {"stage": "lattice-row-extracted", "M": m_value, "MOverKs": exact},
        )
    if max(source_formula_errors, default=0.0) > 3.0e-15:
        raise RuntimeError(f"lattice source reconstruction error {max(source_formula_errors):.3e}")

    bounded_eta = float(config["boundedEta"])
    bounded_source = next(
        row for row in primary["boundedCouplingEnvelope"]["rows"]
        if relative_error(float(row["eta"]), bounded_eta) < 1.0e-15
    )
    bounded_by_m = {int(row["M"]): float(row["envelope"]) for row in bounded_source["values"]}
    if sorted(bounded_by_m) != sorted(m_values):
        raise RuntimeError("bounded-coupling certificate grid differs from lattice grid")

    strong_by_m = {
        int(row["M"]): float(row["envelope"])
        for row in primary["strongCouplingDiagnostic"]["rows"]
    }
    if sorted(strong_by_m) != sorted(m_values):
        raise RuntimeError("strong-coupling certificate grid differs from lattice grid")

    rows: list[dict[str, object]] = []
    for m_value in m_values:
        n_value = (m_value - 1) // 2
        add_row(
            rows,
            panel="A",
            series="exact minimum-lattice factor M/Ks",
            m_value=m_value,
            n_value=n_value,
            x=float(m_value),
            y=lattice_factor[m_value],
            raw_value=lattice_factor[m_value],
            reference_value=lattice_upper[m_value],
            unit="dimensionless exact lattice factor",
            formula="M/[M(M+1)(2M+1)/6]",
            evidence_class="exact certified lattice identity",
            source=primary_source,
            note="minimum over distinct positive integer carrier multipliers",
        )
        add_row(
            rows,
            panel="A",
            series="analytic upper bound 3/M^2",
            m_value=m_value,
            n_value=n_value,
            x=float(m_value),
            y=lattice_upper[m_value],
            raw_value=lattice_upper[m_value],
            reference_value=lattice_factor[m_value],
            unit="dimensionless analytic upper bound",
            formula="3/M^2",
            evidence_class="exact analytic upper bound",
            source=primary_source,
            note="not a fitted trend",
        )

    common_b_reference = bounded_by_m[m_values[0]]
    bounded_formula_errors: list[float] = []
    for m_value in m_values:
        n_value = (m_value - 1) // 2
        eta = bounded_eta
        cbv = math.exp(2.0 * lambda0_l) * (4.0 + c_kappa * eta)
        reconstructed = common_multiplier * cbv * lattice_factor[m_value] * eta ** (4.0 / 3.0)
        bounded_formula_errors.append(relative_error(reconstructed, bounded_by_m[m_value]))
        complete_raw = bounded_by_m[m_value]
        selected_raw = n_value * complete_raw
        add_row(
            rows,
            panel="B",
            series="complete-root BV envelope; eta=1",
            m_value=m_value,
            n_value=n_value,
            eta=eta,
            x=float(m_value),
            y=complete_raw / common_b_reference,
            raw_value=complete_raw,
            reference_value=common_b_reference,
            unit="upper envelope / common M=3 value",
            formula="C*CBV(eta)*(M/Ks)*eta^(4/3)",
            evidence_class="exact complete-root theorem envelope",
            source=primary_source,
            note="bounded observation coupling; complete squared-slope mass",
        )
        add_row(
            rows,
            panel="B",
            series="prior selected-root envelope; N=(M-1)/2",
            m_value=m_value,
            n_value=n_value,
            eta=eta,
            x=float(m_value),
            y=selected_raw / common_b_reference,
            raw_value=selected_raw,
            reference_value=common_b_reference,
            unit="prior upper envelope / common M=3 value",
            formula="N*C*CBV(eta)*(M/Ks)*eta^(4/3)",
            evidence_class="analytic reconstruction of prior selected-root payment",
            source="research/r071y_report-source.md",
            note="neutral comparator only; not new R0.71Z evidence",
        )
    if max(bounded_formula_errors, default=0.0) > 3.0e-14:
        raise RuntimeError(f"bounded-envelope reconstruction error {max(bounded_formula_errors):.3e}")

    coupling_series = {
        0.0: "bounded eta=1",
        0.5: "eta=M^(1/2)",
        6.0 / 7.0: "eta=M^(6/7)",
    }
    coupling_raw: dict[float, list[float]] = {alpha: [] for alpha in coupling_series}
    critical_formula_errors: list[float] = []
    for alpha, label in coupling_series.items():
        for m_value in m_values:
            eta = 1.0 if alpha == 0.0 else m_value**alpha
            cbv = math.exp(2.0 * lambda0_l) * (4.0 + c_kappa * eta)
            raw = common_multiplier * cbv * lattice_factor[m_value] * eta ** (4.0 / 3.0)
            coupling_raw[alpha].append(raw)
            if abs(alpha - 6.0 / 7.0) < 1.0e-15:
                critical_formula_errors.append(relative_error(raw, strong_by_m[m_value]))
        reference = coupling_raw[alpha][0]
        for m_value, raw in zip(m_values, coupling_raw[alpha], strict=True):
            add_row(
                rows,
                panel="C",
                series=label,
                m_value=m_value,
                n_value=(m_value - 1) // 2,
                eta=1.0 if alpha == 0.0 else m_value**alpha,
                eta_power=alpha,
                x=float(m_value),
                y=raw / reference,
                raw_value=raw,
                reference_value=reference,
                unit="upper envelope / own M=3 value",
                formula="C*(M/Ks)*eta^(4/3)*exp(2*lambda0L)*(4+Ckappa*eta)",
                evidence_class="exact R0.71Z upper-envelope formula",
                source=primary_source,
                note="fixed geometry constants retained; strong-coupling curves are diagnostics, not constructions",
            )
    if max(critical_formula_errors, default=0.0) > 5.0e-14:
        raise RuntimeError(f"critical-envelope reconstruction error {max(critical_formula_errors):.3e}")

    nu = float(parameters["nu"])
    d_value = float(parameters["d"])
    a0 = float(parameters["A0"])
    heat_coefficient = 2.0 * nu * d_value**2 * a0
    certified_retention = {
        int(row["R"]): float(row["thetaI"])
        for row in primary["fixedWindowRetention"]["rows"]
        if int(row["R"]) <= int(config["retentionMaximumR"])
    }
    retention_errors: list[float] = []
    for r_value in range(1, int(config["retentionMaximumR"]) + 1):
        retention = math.exp(-heat_coefficient * r_value**2)
        if r_value in certified_retention:
            retention_errors.append(relative_error(retention, certified_retention[r_value]))
        add_row(
            rows,
            panel="D",
            series="fixed-window exact heat retention",
            r_value=float(r_value),
            x=float(r_value),
            y=retention,
            raw_value=retention,
            reference_value=1.0,
            unit="retained enstrophy fraction",
            formula="exp(-2*nu*d^2*A0*R^2)",
            evidence_class="exact global heat-shear retention formula",
            source=primary_source,
            note="analytic heat shear; no nonzero target-root atom",
        )
        add_row(
            rows,
            panel="D",
            series="launch-inclusive retention",
            r_value=float(r_value),
            x=float(r_value),
            y=1.0,
            raw_value=1.0,
            reference_value=1.0,
            unit="retained enstrophy fraction",
            formula="1",
            evidence_class="exact launch-inclusive normalization identity",
            source=primary_source,
            note="payment interval contains launch; roots remain counted on the later observation window",
        )
    if max(retention_errors, default=0.0) > 3.0e-14:
        raise RuntimeError(f"retention reconstruction error {max(retention_errors):.3e}")

    with (ROOT / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data.json").write_text(
        json.dumps(
            {
                "schemaVersion": "1.0.0",
                "release": release,
                "figureId": config["figureId"],
                "rowCount": len(rows),
                "fields": list(FIELDS),
                "rows": rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    fits = {
        "latticeMOverKs": fit_power(m_values[-8:], [lattice_factor[m] for m in m_values[-8:]]),
        "completeRootBoundedEta": fit_power(m_values[-8:], [bounded_by_m[m] for m in m_values[-8:]]),
        "selectedRootBoundedEta": fit_power(m_values[-8:], [((m - 1) / 2) * bounded_by_m[m] for m in m_values[-8:]]),
        "etaBounded": fit_power(m_values[-8:], coupling_raw[0.0][-8:]),
        "etaMOneHalf": fit_power(m_values[-8:], coupling_raw[0.5][-8:]),
        "etaMSixSevenths": fit_power(m_values[-8:], coupling_raw[6.0 / 7.0][-8:]),
    }
    results = {
        "release": release,
        "figureId": config["figureId"],
        "status": "passed",
        "sourceCertificates": {
            "primary": {"path": primary_source, "sha256": sha256(primary_path), "checks": len(primary["checks"])},
            "independent": {"path": independent_source, "sha256": sha256(independent_path), "checks": len(independent["checks"])},
        },
        "parameters": {
            "MValues": m_values,
            "boundedEta": bounded_eta,
            "nu": nu,
            "d": d_value,
            "A0": a0,
            "heatCoefficient": heat_coefficient,
            "Ckappa": c_kappa,
            "lambda0L": lambda0_l,
            "amplitudeOptimizerMaximum": optimizer,
            "multiplierRatioUpper": multiplier_upper,
        },
        "derivedFigureFits": fits,
        "sourceFitValues": {
            "latticeMOverKs": float(primary["lattice"]["tailPower"]),
            "boundedCoupling": float(bounded_source["tailPowerInM"]),
            "criticalEta": float(primary["strongCouplingDiagnostic"]["fittedMPower"]),
        },
        "crossChecks": {
            "maximumLatticeRelativeError": max(source_formula_errors, default=0.0),
            "maximumBoundedEnvelopeRelativeError": max(bounded_formula_errors, default=0.0),
            "maximumCriticalEnvelopeRelativeError": max(critical_formula_errors, default=0.0),
            "maximumCertifiedRetentionRelativeError": max(retention_errors, default=0.0),
            "primaryCheckCount": len(primary["checks"]),
            "independentCheckCount": len(independent["checks"]),
            "independentAllPassed": bool(independent["passed"]),
        },
        "rowCount": len(rows),
        "claimBoundary": contract["claimBoundary"],
        "producerWallSeconds": time.perf_counter() - started,
    }
    (ROOT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    source_records = []
    for label, path in (
        ("primary", primary_path),
        ("independent", independent_path),
        ("analytic-source", REPOSITORY / Path(config["analyticSources"][0])),
        ("independent-audit", REPOSITORY / Path(config["analyticSources"][1])),
    ):
        source_records.append(
            {
                "label": label,
                "path": str(path.relative_to(REPOSITORY)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    metadata = {
        "schemaVersion": "1.0.0",
        "release": release,
        "figureId": config["figureId"],
        "generatedAt": timestamp(),
        "rowCount": len(rows),
        "sourceCertificates": source_records,
        "configSha256": sha256(args.config),
        "contractSha256": sha256(ROOT / "contract.json"),
        "dataCsvSha256": sha256(ROOT / "data.csv"),
        "dataJsonSha256": sha256(ROOT / "data.json"),
        "resultsSha256": sha256(ROOT / "results.json"),
        "evidenceMap": {
            "A": "exact certified lattice identity and analytic upper bound",
            "B": "exact complete-root theorem envelope plus a neutral reconstruction of the prior selected-root factor",
            "C": "exact R0.71Z envelope formula evaluated under three declared coupling laws",
            "D": "exact global heat-shear retention and launch-inclusive normalization identity",
        },
        "claimBoundary": contract["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    environment = (
        f"generatedAt={timestamp()}\n"
        f"python={platform.python_version()}\n"
        f"pythonExecutable={sys.executable}\n"
        f"platform={platform.platform()}\n"
        f"machine={platform.machine()}\n"
        f"logicalCpuCount={os.cpu_count()}\n"
        f"numpy={np.__version__}\n"
        f"matplotlib={matplotlib.__version__}\n"
        f"Pillow={Image.__version__}\n"
        "precision=source Decimal 110 digits; independent binary64 figure reconstruction\n"
        "randomSeed=none\n"
        "gpu=not used\n"
        "dgx=not used\n"
    )
    (ROOT / "environment.txt").write_text(environment, encoding="utf-8")

    elapsed = time.perf_counter() - started
    append_ndjson(ROOT / "progress.ndjson", {"stage": "producer-complete", "rowCount": len(rows), "elapsedSeconds": elapsed})
    append_ndjson(ROOT / "resource-log.ndjson", resource_record("producer-complete", started, rowCount=len(rows)))
    print(
        json.dumps(
            {
                "status": "passed",
                "rows": len(rows),
                "tailPowers": {key: value["power"] for key, value in fits.items()},
                "maximumSourceError": max(
                    source_formula_errors + bounded_formula_errors + critical_formula_errors + retention_errors,
                    default=0.0,
                ),
                "elapsedSeconds": elapsed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
