#!/usr/bin/env python3
"""Compute the finite R0.73O Kolmogorov spectrum consistency diagnostic."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import platform
from pathlib import Path
import resource
import sys
import time


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()
import numpy as np  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
START = time.monotonic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--output-dir", default=str(HERE))
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
                "gpu": "not used",
                "executionHost": "local workstation",
            }, sort_keys=True) + "\n")


def kolmogorov_matrix(alpha: float, reynolds: float, truncation: int) -> np.ndarray:
    modes = np.arange(-truncation, truncation + 1, dtype=np.float64)
    d = alpha * alpha + modes * modes
    matrix = np.diag(-d / reynolds).astype(np.complex128)
    for index, mode in enumerate(modes):
        if index > 0:
            d_minus = alpha * alpha + (mode - 1.0) ** 2
            matrix[index, index - 1] = alpha * (1.0 - d_minus) / (2.0 * d[index])
        if index + 1 < len(modes):
            d_plus = alpha * alpha + (mode + 1.0) ** 2
            matrix[index, index + 1] = -alpha * (1.0 - d_plus) / (2.0 * d[index])
    return matrix


def leading_pair(alpha: float, reynolds: float, truncation: int) -> dict[str, object]:
    matrix = kolmogorov_matrix(alpha, reynolds, truncation)
    values, vectors = np.linalg.eig(matrix)
    index = int(np.argmax(values.real))
    value = values[index]
    vector = vectors[:, index]
    residual = np.linalg.norm(matrix @ vector - value * vector)
    relative = residual / (np.linalg.norm(matrix, ord=2) * np.linalg.norm(vector))
    return {
        "eigenvalue": value,
        "absoluteResidual": float(residual),
        "relativeResidual": float(relative),
        "matrixDimension": int(matrix.shape[0]),
    }


def spectral_abscissa(alpha: float, reynolds: float, truncation: int) -> float:
    matrix = kolmogorov_matrix(alpha, reynolds, truncation)
    return float(np.max(np.linalg.eigvals(matrix).real))


def finite_crossing(alpha: float, truncation: int, lower: float, upper: float) -> float:
    f_lower = spectral_abscissa(alpha, lower, truncation)
    f_upper = spectral_abscissa(alpha, upper, truncation)
    if not (f_lower < 0.0 < f_upper):
        raise RuntimeError("finite critical bracket does not straddle zero")
    for _ in range(60):
        midpoint = (lower + upper) / 2.0
        value = spectral_abscissa(alpha, midpoint, truncation)
        if value > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    return (lower + upper) / 2.0


CSV_FIELDS = (
    "record_type",
    "record_id",
    "alpha",
    "reynolds",
    "truncation",
    "matrix_dimension",
    "spectral_abscissa",
    "leading_imaginary_part",
    "absolute_residual",
    "relative_residual",
    "physical_growth_rate",
    "physical_efolding_time",
    "critical_lower",
    "critical_upper",
    "evidence_boundary",
)


def base_row(kind: str, identifier: str, alpha: float) -> dict[str, str]:
    row = {field: "" for field in CSV_FIELDS}
    row.update({
        "record_type": kind,
        "record_id": identifier,
        "alpha": f"{alpha:.17g}",
        "evidence_boundary": (
            "finite Fourier diagnostic only; rigorous threshold is an external "
            "computer-assisted theorem input"
        ),
    })
    return row


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    output = Path(args.output_dir).resolve()
    if not output.is_dir() or output.is_symlink():
        raise RuntimeError("output directory must be an existing nonsymlink directory")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schemaVersion") != "r073o-kolmogorov-spectrum-config-v1":
        raise RuntimeError("configuration schema drift")

    alpha = float(config["alpha"])
    target_r = float(config["targetReynolds"])
    amplitude = float(config["forcingAmplitude"])
    forcing_mode = int(config["forcingWaveNumber"])
    x_mode = int(config["physicalXWaveNumber"])
    viscosity = float(config["viscosity"])
    critical_lower, critical_upper = map(float, config["rigorousCriticalInterval"])
    truncations = [int(value) for value in config["truncations"]]
    primary_n = int(config["primaryTruncation"])
    monitor = Monitor(output)
    monitor.event("start", alpha=alpha, targetReynolds=target_r)

    if primary_n not in truncations:
        raise RuntimeError("primary truncation absent from convergence inventory")
    parameter_checks = {
        "alphaEmbeddingIdentity": math.isclose(
            alpha, x_mode / forcing_mode, rel_tol=0.0, abs_tol=1e-15
        ),
        "reynoldsScalingIdentity": math.isclose(
            target_r, amplitude / (viscosity * forcing_mode),
            rel_tol=0.0, abs_tol=1e-15,
        ),
        "targetStrictlyAboveRigorousInterval": target_r > critical_upper,
        "criticalIntervalOrdered": critical_lower < critical_upper,
        "truncationsStrictlyIncreasing": truncations == sorted(set(truncations)),
    }
    if not all(parameter_checks.values()):
        raise RuntimeError("parameter identity check failed")
    monitor.event("parameter-identities", checks=len(parameter_checks))

    rows: list[dict[str, str]] = []
    convergence: list[dict[str, object]] = []
    for truncation in truncations:
        pair = leading_pair(alpha, target_r, truncation)
        eigenvalue = pair["eigenvalue"]
        physical_growth = amplitude * forcing_mode * float(eigenvalue.real)
        row = base_row("convergence", f"convergence_{truncation:04d}", alpha)
        row.update({
            "reynolds": f"{target_r:.17g}",
            "truncation": str(truncation),
            "matrix_dimension": str(pair["matrixDimension"]),
            "spectral_abscissa": f"{float(eigenvalue.real):.17g}",
            "leading_imaginary_part": f"{float(eigenvalue.imag):.17g}",
            "absolute_residual": f"{pair['absoluteResidual']:.17g}",
            "relative_residual": f"{pair['relativeResidual']:.17g}",
            "physical_growth_rate": f"{physical_growth:.17g}",
            "physical_efolding_time": f"{1.0 / physical_growth:.17g}",
            "critical_lower": f"{critical_lower:.17g}",
            "critical_upper": f"{critical_upper:.17g}",
        })
        rows.append(row)
        convergence.append({
            "truncation": truncation,
            **pair,
            "physicalGrowthRate": physical_growth,
            "physicalEfoldingTime": 1.0 / physical_growth,
        })
    monitor.event("convergence", truncations=len(truncations))

    sweep_config = config["sweep"]
    sweep_values = np.linspace(
        float(sweep_config["start"]),
        float(sweep_config["end"]),
        int(sweep_config["count"]),
    )
    sweep_n = int(sweep_config["truncation"])
    sweep_abscissae: list[float] = []
    for index, reynolds in enumerate(sweep_values):
        abscissa = spectral_abscissa(alpha, float(reynolds), sweep_n)
        sweep_abscissae.append(abscissa)
        row = base_row("sweep", f"sweep_{index:04d}", alpha)
        row.update({
            "reynolds": f"{float(reynolds):.17g}",
            "truncation": str(sweep_n),
            "matrix_dimension": str(2 * sweep_n + 1),
            "spectral_abscissa": f"{abscissa:.17g}",
            "critical_lower": f"{critical_lower:.17g}",
            "critical_upper": f"{critical_upper:.17g}",
        })
        rows.append(row)
    monitor.event("sweep", samples=len(sweep_values), truncation=sweep_n)

    crossing = finite_crossing(
        alpha,
        primary_n,
        float(sweep_config["start"]),
        float(sweep_config["end"]),
    )
    primary = next(item for item in convergence if item["truncation"] == primary_n)
    primary_value = float(primary["eigenvalue"].real)
    tail_values = [
        float(item["eigenvalue"].real)
        for item in convergence
        if int(item["truncation"]) >= 20
    ]
    tail_spread = max(abs(value - primary_value) for value in tail_values)
    critical_midpoint = (critical_lower + critical_upper) / 2.0
    tolerances = config["checks"]
    numerical_checks = {
        "targetSpectralAbscissaPositive": (
            primary_value >= float(tolerances["targetMinimumSpectralAbscissa"])
        ),
        "convergenceSpreadFromN20Small": (
            tail_spread <= float(tolerances["maxConvergenceSpreadFromN20"])
        ),
        "primaryRelativeResidualSmall": (
            float(primary["relativeResidual"]) <= float(tolerances["maxEigenResidual"])
        ),
        "finiteCriticalCrossingMatchesRigorousMidpoint": (
            abs(crossing - critical_midpoint)
            <= float(tolerances["maxCriticalMidpointError"])
        ),
        "sweepStrictlyIncreasing": bool(np.all(np.diff(sweep_abscissae) > 0.0)),
        "sweepStraddlesZero": min(sweep_abscissae) < 0.0 < max(sweep_abscissae),
        "leadingEigenvalueNumericallyReal": (
            abs(float(primary["eigenvalue"].imag)) < 1e-12
        ),
    }
    if not all(numerical_checks.values()):
        raise RuntimeError("finite spectrum diagnostic check failed")

    csv_path = output / "source-data.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    result = {
        "schemaVersion": "r073o-kolmogorov-spectrum-diagnostic-v1",
        "release": "R0.73O",
        "status": "passed",
        "allChecksPass": True,
        "parameters": {
            "alpha": alpha,
            "targetReynolds": target_r,
            "forcingAmplitude": amplitude,
            "forcingWaveNumber": forcing_mode,
            "physicalXWaveNumber": x_mode,
            "viscosity": viscosity,
            "physicalGrowthRule": "lambda=A*N*sigma",
        },
        "externalRigorousInput": {
            "criticalInterval": [critical_lower, critical_upper],
            "source": "Nagatou 2004; later restatement Watanabe et al. 2016",
            "recomputedByThisScript": False,
        },
        "finiteResults": {
            "primaryTruncation": primary_n,
            "matrixDimension": primary["matrixDimension"],
            "leadingEigenvalueReal": primary_value,
            "leadingEigenvalueImaginary": float(primary["eigenvalue"].imag),
            "relativeResidual": float(primary["relativeResidual"]),
            "physicalGrowthRate": float(primary["physicalGrowthRate"]),
            "physicalEfoldingTime": float(primary["physicalEfoldingTime"]),
            "tailSpreadFromN20": tail_spread,
            "finiteCriticalCrossing": crossing,
            "finiteCriticalMidpointError": crossing - critical_midpoint,
        },
        "checks": {**parameter_checks, **numerical_checks},
        "claimBoundary": config["claimBoundary"],
        "sourceData": {
            "path": "research/certificates/r073o/source-data.csv",
            "rows": len(rows),
            "convergenceRows": len(convergence),
            "sweepRows": len(sweep_values),
            "bytes": csv_path.stat().st_size,
            "sha256": sha256(csv_path),
        },
    }
    diagnostic_path = output / "diagnostic.json"
    diagnostic_path.write_text(canonical(result), encoding="utf-8")
    environment = {
        "schemaVersion": "r073o-kolmogorov-spectrum-environment-v1",
        "createdUtc": utc_now(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "configuration": {
            "path": str(config_path.relative_to(ROOT)),
            "bytes": config_path.stat().st_size,
            "sha256": sha256(config_path),
        },
        "compute": {
            "processes": 1,
            "gpu": "not used",
            "executionHost": "local workstation",
            "wallTimeSeconds": time.monotonic() - START,
            "maximumResidentSetMiB": rss_mib(),
        },
    }
    (output / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event(
        "complete",
        allChecksPass=True,
        spectralAbscissa=primary_value,
        finiteCriticalCrossing=crossing,
    )
    print(canonical({
        "status": "passed",
        "spectralAbscissa": primary_value,
        "finiteCriticalCrossing": crossing,
        "physicalGrowthRate": primary["physicalGrowthRate"],
        "rows": len(rows),
        "checks": len(result["checks"]),
    }), end="")


if __name__ == "__main__":
    main()
