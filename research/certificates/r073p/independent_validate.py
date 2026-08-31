#!/usr/bin/env python3
"""Independently recalculate the R0.73P formula diagnostic.

The producer is neither imported nor called.  In particular, the lattice
radii are obtained from Legendre's three-square characterization instead of
enumerating integer triples.  This is a formula-only diagnostic, not a
Navier--Stokes simulation and not a nonlinear or global-regularity result.
"""

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
    parser.add_argument("--reference", default=str(HERE / "diagnostic.json"))
    parser.add_argument("--source-data", default=str(HERE / "source-data.csv"))
    parser.add_argument(
        "--output", default=str(HERE / "independent_validation.json")
    )
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, relative: float) -> bool:
    return math.isclose(left, right, rel_tol=relative, abs_tol=relative * 1e-300)


def relative_error(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1e-300)
    return abs(left - right) / scale


def is_sum_of_three_squares(value: int) -> bool:
    """Legendre: n is representable iff n != 4^a(8b+7)."""
    require(value > 0, "three-square test requires a positive integer")
    reduced = value
    while reduced % 4 == 0:
        reduced //= 4
    return reduced % 8 != 7


def independent_log_grid(minimum: float, maximum: float, count: int) -> list[float]:
    """Base-10 construction, separate from the producer's natural-log path."""
    lower = math.log10(minimum)
    upper = math.log10(maximum)
    return [10.0 ** (lower + (upper - lower) * i / (count - 1)) for i in range(count)]


def independent_linear_grid(minimum: float, maximum: float, count: int) -> list[float]:
    step = (maximum - minimum) / (count - 1)
    return [minimum + step * i for i in range(count)]


def independent_frequency_grid(settings: dict[str, Any]) -> list[int]:
    values = {
        int(round(value))
        for value in independent_log_grid(
            float(settings["minimumFrequency"]),
            float(settings["maximumFrequency"]),
            int(settings["logSamples"]),
        )
    }
    values.update(
        (int(settings["minimumFrequency"]), int(settings["maximumFrequency"]))
    )
    return sorted(values)


def append_monitor(stage: str, **fields: object) -> None:
    now = utc_now()
    elapsed = time.monotonic() - START
    progress = {
        "stage": stage,
        "timestampUtc": now,
        "elapsedSeconds": elapsed,
        "validator": "independent-three-square",
        **fields,
    }
    maximum_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_mib = (
        maximum_rss / (1024.0 * 1024.0)
        if sys.platform == "darwin"
        else maximum_rss / 1024.0
    )
    resources = {
        "stage": stage,
        "timestampUtc": now,
        "elapsedSeconds": elapsed,
        "maximumResidentSetMiB": rss_mib,
        "processes": 1,
        "threadsPerProcess": 1,
        "gpu": "not used",
        "executionHost": platform.node(),
        "validator": "independent-three-square",
    }
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(progress, sort_keys=True) + "\n")
    with (HERE / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(resources, sort_keys=True) + "\n")


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    reference_path = Path(args.reference).resolve()
    source_path = Path(args.source_data).resolve()
    output_path = Path(args.output).resolve()
    require(output_path == HERE / "independent_validation.json", "output path drift")
    config = load_json(config_path)
    reference = load_json(reference_path)
    require(
        config.get("schemaVersion") == "r073p-formula-diagnostic-config-v1",
        "configuration schema drift",
    )
    require(
        reference.get("schemaVersion") == "r073p-formula-diagnostic-v1",
        "reference diagnostic schema drift",
    )
    require(reference.get("allChecksPass") is True, "primary diagnostic did not pass")
    append_monitor("independent-start")

    with source_path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "source CSV schema drift")
        rows = list(reader)
    threshold_rows = [row for row in rows if row["record_type"] == "threshold"]
    power_rows = [row for row in rows if row["record_type"] == "sobolev_power"]
    heat_rows = [row for row in rows if row["record_type"] == "heat_lattice"]
    require(len(rows) == len(threshold_rows) + len(power_rows) + len(heat_rows), "unknown CSV row kind")

    tolerance = float(config["tolerances"]["independentRelative"])
    grid_tolerance = float(config["tolerances"]["gridRelative"])
    panel_a = config["panelA"]
    frequencies = independent_frequency_grid(panel_a)
    require(len(threshold_rows) == len(frequencies), "threshold row-count drift")
    threshold_errors: list[float] = []
    for index, (row, frequency) in enumerate(zip(threshold_rows, frequencies)):
        require(int(row["sample_index"]) == index, "threshold index drift")
        require(int(row["N"]) == frequency, "threshold frequency-grid drift")
        expected_h3 = float(panel_a["normalizedH3Radius"]) / frequency**3
        expected_half = float(panel_a["normalizedCriticalRadius"]) / math.sqrt(frequency)
        threshold_errors.extend(
            (
                relative_error(float(row["h3_threshold"]), expected_h3),
                relative_error(float(row["hhalf_threshold"]), expected_half),
            )
        )

    panel_b = config["panelB"]
    gammas = independent_linear_grid(
        float(panel_b["minimumGamma"]),
        float(panel_b["maximumGamma"]),
        int(panel_b["samples"]),
    )
    require(len(power_rows) == len(gammas), "Sobolev-power row-count drift")
    power_errors: list[float] = []
    open_strip_signs = True
    for index, (row, gamma) in enumerate(zip(power_rows, gammas)):
        require(int(row["sample_index"]) == index, "Sobolev-power index drift")
        stored_gamma = float(row["gamma"])
        require(close(stored_gamma, gamma, grid_tolerance), "gamma-grid drift")
        expected = (-stored_gamma, 0.5 - stored_gamma, 3.0 - stored_gamma)
        observed = tuple(float(row[key]) for key in ("l2_power", "hhalf_power", "h3_power"))
        power_errors.extend(relative_error(left, right) for left, right in zip(observed, expected))
        if 0.5 < stored_gamma < 3.0:
            open_strip_signs = open_strip_signs and (
                observed[0] < 0.0 and observed[1] < 0.0 and observed[2] > 0.0
            )

    panel_c = config["panelC"]
    minimum_tau = float(panel_c["minimumTau"])
    cutoff = int(panel_c["cutoffNormSquared"])
    half_width = int(panel_c["latticeHalfWidth"])
    continuous_peak_at_minimum = 3.0 / (2.0 * minimum_tau)
    radii = [value for value in range(1, cutoff + 1) if is_sum_of_three_squares(value)]
    require(len(heat_rows) == int(panel_c["logSamples"]), "heat row-count drift")
    independent_taus = independent_log_grid(
        minimum_tau, float(panel_c["maximumTau"]), int(panel_c["logSamples"])
    )
    heat_value_errors: list[float] = []
    bound_errors: list[float] = []
    tau_grid_errors: list[float] = []
    maxima_exact = True
    witnesses_exact = True
    bounds_hold = True
    maximizing_radii: list[int] = []
    for index, (row, independent_tau) in enumerate(zip(heat_rows, independent_taus)):
        require(int(row["sample_index"]) == index, "heat row index drift")
        tau = float(row["tau"])
        tau_grid_errors.append(relative_error(tau, independent_tau))
        best_n = max(
            radii,
            key=lambda value: value**1.5 * math.exp(-tau * value),
        )
        discrete = best_n**1.5 * math.exp(-tau * best_n)
        continuous = (3.0 / (2.0 * math.e * tau)) ** 1.5
        ratio = discrete / continuous
        observed_n = int(row["maximizer_norm_squared"])
        observed_discrete = float(row["discrete_heat"])
        observed_continuous = float(row["continuous_heat_bound"])
        observed_ratio = float(row["discrete_to_continuous"])
        maxima_exact = maxima_exact and observed_n == best_n
        witnesses_exact = witnesses_exact and (
            int(row["k1"]) ** 2 + int(row["k2"]) ** 2 + int(row["k3"]) ** 2
            == observed_n
        )
        bounds_hold = bounds_hold and observed_discrete <= observed_continuous * (
            1.0 + float(config["tolerances"]["continuousEnvelopeSlack"])
        )
        heat_value_errors.extend(
            (
                relative_error(observed_discrete, discrete),
                relative_error(observed_ratio, ratio),
            )
        )
        bound_errors.append(relative_error(observed_continuous, continuous))
        maximizing_radii.append(best_n)

    figure_dir = ROOT / str(config["figureReference"])
    figure_source = figure_dir / "source-data.csv"
    figure_config = load_json(figure_dir / "config.json")
    figure_results = load_json(figure_dir / "results.json")
    figure_validation = load_json(figure_dir / "validation.json")
    figure_claims = figure_validation.get("claimBoundary", {})
    maximum_threshold_error = max(threshold_errors, default=0.0)
    maximum_power_error = max(power_errors, default=0.0)
    maximum_heat_error = max(heat_value_errors, default=0.0)
    maximum_bound_error = max(bound_errors, default=0.0)
    maximum_tau_grid_error = max(tau_grid_errors, default=0.0)
    source_hash = sha256(source_path)
    checks = {
        "producerCodeNotImportedOrCalled": True,
        "sourceDataHashMatchesPrimary": source_hash == reference["sourceData"]["sha256"],
        "sourceDataRowsMatchPrimary": len(rows) == int(reference["sourceData"]["rows"]),
        "thresholdFrequencyGridIndependent": [int(row["N"]) for row in threshold_rows] == frequencies,
        "thresholdPowersIndependent": maximum_threshold_error <= tolerance,
        "sobolevPowerGridIndependent": maximum_power_error <= tolerance,
        "openGammaStripSignsIndependent": open_strip_signs,
        "threeSquareRadiusCountExact": len(radii) == 3414,
        "latticeCutoffIdentity": cutoff == half_width * half_width == 4096,
        "cutoffStrictlyBeyondContinuousPeak": cutoff > continuous_peak_at_minimum,
        "cutoffNumericalInequalityExact": cutoff > 1500.0,
        "continuousPeakRangeMonotonic": all(
            3.0 / (2.0 * float(row["tau"])) <= continuous_peak_at_minimum
            for row in heat_rows
        ),
        "tauGridIndependent": maximum_tau_grid_error <= grid_tolerance,
        "latticeMaximaIndependent": maxima_exact,
        "latticeWitnessesValid": witnesses_exact,
        "latticeValuesIndependent": maximum_heat_error <= tolerance,
        "continuousBoundIndependent": maximum_bound_error <= tolerance and bounds_hold,
        "figureSourceDataByteIdentical": source_path.read_bytes() == figure_source.read_bytes(),
        "figureSourceDataHashIndependent": source_hash == sha256(figure_source),
        "figureConfigurationKeyValuesExact": (
            figure_config.get("panelA") == config.get("panelA")
            and all(figure_config.get("panelB", {}).get(key) == panel_b.get(key) for key in ("minimumGamma", "maximumGamma", "samples", "criticalIndex", "highIndex"))
            and all(figure_config.get("panelC", {}).get(key) == panel_c.get(key) for key in ("minimumTau", "maximumTau", "logSamples", "latticeHalfWidth"))
        ),
        "figureResultsIndependent": (
            figure_results.get("rowCount") == len(rows)
            and figure_results.get("facts", {}).get("panelC", {}).get("representableRadiusCountThroughCutoff") == len(radii)
            and figure_results.get("facts", {}).get("panelC", {}).get("maximumMaximizerNormSquared") == max(maximizing_radii)
        ),
        "figureClaimBoundaryConservative": (
            figure_claims.get("navierStokesSimulation") is False
            and figure_claims.get("nonlinearEntryCertificate") is False
            and figure_claims.get("globalRegularityTheorem") is False
            and figure_claims.get("clayProblemSolved") is False
        ),
        "claimBoundaryExact": reference.get("claimBoundary") == config.get("claimBoundary"),
        "unsupportedClaimsRemainFalse": all(
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
    require(all(checks.values()), "independent validation failed: " + repr([
        key for key, passed in checks.items() if not passed
    ]))
    result = {
        "schemaVersion": "r073p-formula-diagnostic-independent-validation-v1",
        "release": "R0.73P",
        "status": "passed",
        "allChecksPass": True,
        "createdUtc": utc_now(),
        "method": {
            "producerCodeImported": False,
            "producerCodeCalled": False,
            "thresholdGrid": "base-10 logarithmic grid with integer deduplication",
            "sobolevPowers": "direct exponent identities",
            "latticeRadii": "Legendre three-square characterization",
            "latticeMaximization": "exhaustive scan of every representable norm-squared through 4096",
        },
        "software": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "dependencies": "Python standard library only",
        },
        "checks": checks,
        "observations": {
            "sourceRows": len(rows),
            "thresholdRows": len(threshold_rows),
            "sobolevPowerRows": len(power_rows),
            "heatLatticeRows": len(heat_rows),
            "representableRadiusCountThroughCutoff": len(radii),
            "cutoffNormSquared": cutoff,
            "continuousPeakNormSquaredAtMinimumTau": continuous_peak_at_minimum,
            "minimumMaximizerNormSquared": min(maximizing_radii),
            "maximumMaximizerNormSquared": max(maximizing_radii),
            "maximumThresholdRelativeError": maximum_threshold_error,
            "maximumSobolevPowerRelativeError": maximum_power_error,
            "maximumTauGridRelativeError": maximum_tau_grid_error,
            "maximumHeatRelativeError": maximum_heat_error,
            "maximumContinuousBoundRelativeError": maximum_bound_error,
        },
        "sourceData": {
            "path": source_path.relative_to(ROOT).as_posix(),
            "rows": len(rows),
            "bytes": source_path.stat().st_size,
            "sha256": source_hash,
        },
        "figureReference": str(config["figureReference"]),
        "claimBoundary": config["claimBoundary"],
    }
    output_path.write_text(canonical(result), encoding="utf-8")
    append_monitor("independent-complete", allChecksPass=True, checks=len(checks))
    print(canonical({
        "status": "passed",
        "checks": len(checks),
        "representableRadii": len(radii),
        "cutoffStrictlyBeyondContinuousPeak": cutoff > continuous_peak_at_minimum,
    }), end="")


if __name__ == "__main__":
    main()
