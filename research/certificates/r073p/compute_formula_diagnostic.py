#!/usr/bin/env python3
"""Produce the R0.73P closed-form and exact finite-lattice diagnostic."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
START = time.monotonic()
CSV_FIELDS = (
    "record_type",
    "sample_index",
    "N",
    "h3_threshold",
    "hhalf_threshold",
    "gamma",
    "l2_power",
    "hhalf_power",
    "h3_power",
    "tau",
    "discrete_heat",
    "continuous_heat_bound",
    "discrete_to_continuous",
    "maximizer_norm_squared",
    "k1",
    "k2",
    "k3",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--output-dir", default=str(HERE))
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_record(path: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


class Monitor:
    def __init__(self, output: Path) -> None:
        self.progress = output / "progress.ndjson"
        self.resources = output / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        now = utc_now()
        elapsed = time.monotonic() - START
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": now,
                "elapsedSeconds": elapsed,
                **fields,
            }, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "stage": stage,
                "timestampUtc": now,
                "elapsedSeconds": elapsed,
                "maximumResidentSetMiB": rss_mib(),
                "processes": 1,
                "threadsPerProcess": 1,
                "gpu": "not used",
                "executionHost": platform.node(),
            }, sort_keys=True) + "\n")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def log_grid(minimum: float, maximum: float, count: int) -> list[float]:
    require(minimum > 0.0 and maximum > minimum and count >= 2, "invalid log grid")
    lower = math.log(minimum)
    upper = math.log(maximum)
    return [
        math.exp(lower + (upper - lower) * index / (count - 1))
        for index in range(count)
    ]


def linear_grid(minimum: float, maximum: float, count: int) -> list[float]:
    require(maximum > minimum and count >= 2, "invalid linear grid")
    return [
        minimum + (maximum - minimum) * index / (count - 1)
        for index in range(count)
    ]


def frequency_grid(settings: dict[str, Any]) -> list[int]:
    values = {
        int(round(value))
        for value in log_grid(
            float(settings["minimumFrequency"]),
            float(settings["maximumFrequency"]),
            int(settings["logSamples"]),
        )
    }
    values.add(int(settings["minimumFrequency"]))
    values.add(int(settings["maximumFrequency"]))
    return sorted(values)


def triple_enumerated_radii(half_width: int) -> dict[int, tuple[int, int, int]]:
    """Enumerate one nonnegative integer triple for each radius up to K^2."""
    require(half_width >= 1, "lattice half-width must be positive")
    cutoff = half_width * half_width
    representatives: dict[int, tuple[int, int, int]] = {}
    for i in range(half_width + 1):
        i2 = i * i
        for j in range(half_width + 1):
            partial = i2 + j * j
            if partial > cutoff:
                break
            for k in range(math.isqrt(cutoff - partial) + 1):
                norm_squared = partial + k * k
                if norm_squared and norm_squared not in representatives:
                    representatives[norm_squared] = (i, j, k)
    require(cutoff in representatives, "cutoff radius has no lattice representative")
    return representatives


def heat_value(norm_squared: int, tau: float) -> float:
    return norm_squared**1.5 * math.exp(-tau * norm_squared)


def empty_row(kind: str, index: int) -> dict[str, str]:
    row = {field: "" for field in CSV_FIELDS}
    row["record_type"] = kind
    row["sample_index"] = str(index)
    return row


def relevant_figure_config(config: dict[str, Any]) -> dict[str, object]:
    return {
        "panelA": {
            key: config["panelA"][key]
            for key in (
                "minimumFrequency",
                "maximumFrequency",
                "logSamples",
                "normalizedH3Radius",
                "normalizedCriticalRadius",
            )
        },
        "panelB": {
            key: config["panelB"][key]
            for key in (
                "minimumGamma",
                "maximumGamma",
                "samples",
                "criticalIndex",
                "highIndex",
            )
        },
        "panelC": {
            key: config["panelC"][key]
            for key in (
                "minimumTau",
                "maximumTau",
                "logSamples",
                "latticeHalfWidth",
            )
        },
    }


def generate_rows(
    config: dict[str, Any], monitor: Monitor
) -> tuple[list[dict[str, str]], dict[str, object]]:
    rows: list[dict[str, str]] = []

    panel_a = config["panelA"]
    h3_radius = float(panel_a["normalizedH3Radius"])
    hhalf_radius = float(panel_a["normalizedCriticalRadius"])
    frequencies = frequency_grid(panel_a)
    for index, frequency in enumerate(frequencies):
        row = empty_row("threshold", index)
        row.update({
            "N": str(frequency),
            "h3_threshold": format(h3_radius * frequency ** -3.0, ".17g"),
            "hhalf_threshold": format(hhalf_radius * frequency ** -0.5, ".17g"),
        })
        rows.append(row)
    monitor.event("panel-a-thresholds", rows=len(frequencies))

    panel_b = config["panelB"]
    gammas = linear_grid(
        float(panel_b["minimumGamma"]),
        float(panel_b["maximumGamma"]),
        int(panel_b["samples"]),
    )
    for index, gamma in enumerate(gammas):
        row = empty_row("sobolev_power", index)
        row.update({
            "gamma": format(gamma, ".17g"),
            "l2_power": format(-gamma, ".17g"),
            "hhalf_power": format(0.5 - gamma, ".17g"),
            "h3_power": format(3.0 - gamma, ".17g"),
        })
        rows.append(row)
    monitor.event("panel-b-sobolev-powers", rows=len(gammas))

    panel_c = config["panelC"]
    minimum_tau = float(panel_c["minimumTau"])
    maximum_tau = float(panel_c["maximumTau"])
    half_width = int(panel_c["latticeHalfWidth"])
    cutoff = int(panel_c["cutoffNormSquared"])
    require(cutoff == half_width * half_width, "cutoff/half-width identity drift")
    representatives = triple_enumerated_radii(half_width)
    radii = sorted(representatives)
    taus = log_grid(minimum_tau, maximum_tau, int(panel_c["logSamples"]))
    maximizing_radii: list[int] = []
    ratios: list[float] = []
    for index, tau in enumerate(taus):
        best_n = max(radii, key=lambda value: heat_value(value, tau))
        discrete = heat_value(best_n, tau)
        continuous = (3.0 / (2.0 * math.e * tau)) ** 1.5
        ratio = discrete / continuous
        k1, k2, k3 = representatives[best_n]
        row = empty_row("heat_lattice", index)
        row.update({
            "tau": format(tau, ".17g"),
            "discrete_heat": format(discrete, ".17g"),
            "continuous_heat_bound": format(continuous, ".17g"),
            "discrete_to_continuous": format(ratio, ".17g"),
            "maximizer_norm_squared": str(best_n),
            "k1": str(k1),
            "k2": str(k2),
            "k3": str(k3),
        })
        rows.append(row)
        maximizing_radii.append(best_n)
        ratios.append(ratio)
    monitor.event(
        "panel-c-lattice-maxima",
        rows=len(taus),
        representableRadii=len(representatives),
        cutoffNormSquared=cutoff,
    )

    continuous_peak_at_minimum = 3.0 / (2.0 * minimum_tau)
    relative_tolerance = float(config["tolerances"]["formulaRelative"])
    facts = {
        "panelA": {
            "rowCount": len(frequencies),
            "minimumFrequency": min(frequencies),
            "maximumFrequency": max(frequencies),
            "maximumH3NormalizationError": max(
                abs((h3_radius * n ** -3.0) * n**3 / h3_radius - 1.0)
                for n in frequencies
            ),
            "maximumCriticalNormalizationError": max(
                abs((hhalf_radius * n ** -0.5) * n**0.5 / hhalf_radius - 1.0)
                for n in frequencies
            ),
        },
        "panelB": {
            "rowCount": len(gammas),
            "criticalBoundary": float(panel_b["criticalIndex"]),
            "highBoundary": float(panel_b["highIndex"]),
            "openStrip": [0.5, 3.0],
            "interiorSignChecks": sum(0.5 < gamma < 3.0 for gamma in gammas),
        },
        "panelC": {
            "rowCount": len(taus),
            "tauRange": [minimum_tau, maximum_tau],
            "latticeHalfWidth": half_width,
            "cutoffNormSquared": cutoff,
            "continuousPeakNormSquaredAtMinimumTau": continuous_peak_at_minimum,
            "representableRadiusCountThroughCutoff": len(representatives),
            "minimumMaximizerNormSquared": min(maximizing_radii),
            "maximumMaximizerNormSquared": max(maximizing_radii),
            "minimumDiscreteToContinuousRatio": min(ratios),
            "maximumDiscreteToContinuousRatio": max(ratios),
            "tailStrictlyDecreasingBeyondCutoff": cutoff > continuous_peak_at_minimum,
            "allDiscreteValuesBelowContinuousBound": all(
                ratio <= 1.0 + relative_tolerance for ratio in ratios
            ),
        },
    }
    return rows, facts


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    output = Path(args.output_dir).resolve()
    require(output.is_dir() and not output.is_symlink(), "invalid output directory")
    config = load_json(config_path)
    require(
        config.get("schemaVersion") == "r073p-formula-diagnostic-config-v1",
        "configuration schema drift",
    )
    monitor = Monitor(output)
    monitor.event("start", release=config.get("release"))

    figure_dir = ROOT / str(config["figureReference"])
    figure_files = {
        name: figure_dir / name
        for name in ("config.json", "source-data.csv", "results.json", "validation.json")
    }
    require(figure_dir.is_dir() and not figure_dir.is_symlink(), "missing figure directory")
    for path in figure_files.values():
        require(path.is_file() and not path.is_symlink(), "missing figure input: " + path.name)
    figure_config = load_json(figure_files["config.json"])
    figure_results = load_json(figure_files["results.json"])
    figure_validation = load_json(figure_files["validation.json"])

    config_match = relevant_figure_config(config) == relevant_figure_config(figure_config)
    require(config_match, "certificate and figure formula configuration differ")
    rows, facts = generate_rows(config, monitor)

    csv_path = output / "source-data.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        # The reference figure uses a platform-independent LF ledger.  Fix the
        # terminator explicitly so the certificate can bind it byte for byte.
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with figure_files["source-data.csv"].open("r", encoding="utf-8", newline="") as stream:
        figure_reader = csv.DictReader(stream)
        require(tuple(figure_reader.fieldnames or ()) == CSV_FIELDS, "figure CSV schema drift")
        figure_rows = list(figure_reader)
    rows_exact = rows == figure_rows
    bytes_exact = csv_path.read_bytes() == figure_files["source-data.csv"].read_bytes()

    figure_facts = figure_results.get("facts", {})
    figure_claims = figure_validation.get("claimBoundary", {})
    checks = {
        "figureConfigurationExact": config_match,
        "panelAFormulaChecksPass": (
            facts["panelA"]["maximumH3NormalizationError"] <= 3e-15
            and facts["panelA"]["maximumCriticalNormalizationError"] <= 3e-15
        ),
        "panelAFrequencyRangeExact": (
            facts["panelA"]["minimumFrequency"] == 1
            and facts["panelA"]["maximumFrequency"] == 100000
        ),
        "panelBSobolevPowersExactByConstruction": True,
        "panelBOpenStripExact": facts["panelB"]["openStrip"] == [0.5, 3.0],
        "panelBOpenStripSigns": all(
            -gamma < 0.0 and 0.5 - gamma < 0.0 and 3.0 - gamma > 0.0
            for gamma in linear_grid(0.0, 3.5, 351)
            if 0.5 < gamma < 3.0
        ),
        "panelCCutoffIdentity": facts["panelC"]["cutoffNormSquared"] == 4096,
        "panelCCutoffStrictlyBeyondAllContinuousPeaks": (
            facts["panelC"]["cutoffNormSquared"]
            > facts["panelC"]["continuousPeakNormSquaredAtMinimumTau"]
        ),
        "panelCGlobalTailEnclosed": facts["panelC"]["tailStrictlyDecreasingBeyondCutoff"],
        "panelCContinuousUpperBound": facts["panelC"]["allDiscreteValuesBelowContinuousBound"],
        "panelCMaximizerWitnessesExact": all(
            int(row["k1"]) ** 2 + int(row["k2"]) ** 2 + int(row["k3"]) ** 2
            == int(row["maximizer_norm_squared"])
            for row in rows
            if row["record_type"] == "heat_lattice"
        ),
        "figureSourceRowsByteIdentical": rows_exact and bytes_exact,
        "figureResultsCountsExact": (
            figure_results.get("rowCount") == len(rows)
            and figure_facts.get("panelA", {}).get("rowCount") == facts["panelA"]["rowCount"]
            and figure_facts.get("panelB", {}).get("rowCount") == facts["panelB"]["rowCount"]
            and figure_facts.get("panelC", {}).get("rowCount") == facts["panelC"]["rowCount"]
        ),
        "figureResultsCutoffExact": (
            figure_facts.get("panelC", {}).get("cutoffNormSquared") == 4096
            and figure_facts.get("panelC", {}).get("maximumMaximizerNormSquared")
            == facts["panelC"]["maximumMaximizerNormSquared"]
        ),
        "figureValidationFormulaBoundaryConsistent": (
            figure_claims.get("closedFormThresholdComparison") is True
            and figure_claims.get("pureModeSobolevScaling") is True
            and figure_claims.get("exactSampledLinearLatticeMaximum") is True
            and figure_claims.get("navierStokesSimulation") is False
            and figure_claims.get("nonlinearEntryCertificate") is False
            and figure_claims.get("globalRegularityTheorem") is False
            and figure_claims.get("clayProblemSolved") is False
        ),
        "claimBoundaryExplicitAndNegativeClaimsFalse": all(
            config["claimBoundary"][key] is False
            for key in (
                "navierStokesSimulation",
                "nonlinearEntryCertified",
                "pdeNecessityEstablished",
                "globalRegularityEstablished",
                "finiteTimeSingularityEstablished",
                "clayProblemSolved",
            )
        ),
    }
    require(all(checks.values()), "primary diagnostic failed: " + repr([
        key for key, passed in checks.items() if not passed
    ]))
    monitor.event("figure-cross-check", checks=len(checks), rows=len(rows))

    diagnostic = {
        "schemaVersion": "r073p-formula-diagnostic-v1",
        "release": "R0.73P",
        "status": "passed",
        "allChecksPass": True,
        "createdUtc": utc_now(),
        "evidenceClass": config["evidenceClass"],
        "checks": checks,
        "formulas": {
            "directH3Threshold": "N^-3",
            "criticalHhalfThreshold": "N^-1/2",
            "pureModeL2Power": "-gamma",
            "pureModeHhalfPower": "1/2-gamma",
            "pureModeH3Power": "3-gamma",
            "openGammaStrip": "1/2<gamma<3",
            "discreteHeatMaximum": "max_{k in Z^3 minus {0}} |k|^3 exp(-tau |k|^2)",
            "continuousHeatUpperBound": "(3/(2 e tau))^(3/2)",
        },
        "facts": facts,
        "sourceData": {
            "path": csv_path.relative_to(ROOT).as_posix(),
            "rows": len(rows),
            "thresholdRows": facts["panelA"]["rowCount"],
            "sobolevPowerRows": facts["panelB"]["rowCount"],
            "heatLatticeRows": facts["panelC"]["rowCount"],
            "bytes": csv_path.stat().st_size,
            "sha256": sha256(csv_path),
            "byteIdenticalToFigureSourceData": bytes_exact,
        },
        "figureBindings": [
            relative_record(figure_files[name])
            for name in ("config.json", "source-data.csv", "results.json", "validation.json")
        ],
        "claimBoundary": config["claimBoundary"],
    }
    diagnostic_path = output / "diagnostic.json"
    diagnostic_path.write_text(canonical(diagnostic), encoding="utf-8")

    environment = {
        "schemaVersion": "r073p-formula-diagnostic-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "arithmetic": "IEEE-754 binary64 plus exact integer lattice enumeration",
        "dependencies": "Python standard library only",
        "randomSeed": "not applicable; deterministic calculation",
        "compute": {
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "wallTimeSeconds": time.monotonic() - START,
            "maximumResidentSetMiB": rss_mib(),
        },
        "configuration": relative_record(config_path),
        "figureBindings": diagnostic["figureBindings"],
    }
    (output / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("complete", allChecksPass=True, rows=len(rows))
    print(canonical({
        "status": "passed",
        "checks": len(checks),
        "rows": len(rows),
        "figureSourceDataByteIdentical": bytes_exact,
    }), end="")


if __name__ == "__main__":
    main()
