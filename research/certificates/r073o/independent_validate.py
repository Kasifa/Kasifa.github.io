#!/usr/bin/env python3
"""Independently validate the finite R0.73O Kolmogorov spectrum diagnostic.

This script starts from the generalized Fourier eigenproblem

    A c = sigma B c,

obtained directly from

    sigma Delta phi - R^{-1} Delta^2 phi
        + sin(Y) (Delta + I) partial_X phi = 0.

It does not import or call the producer script.  The calculation is a finite
Fourier diagnostic only; it is not a proof about the infinite-dimensional
operator and does not replace the cited computer-assisted theorem.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import platform
import sys
import time


def bootstrap() -> None:
    """Add explicitly supplied dependency roots before importing numerics."""
    for index, value in enumerate(sys.argv):
        if value in {"--deps", "--scipy-deps"} and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
        elif value.startswith("--deps=") or value.startswith("--scipy-deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))


bootstrap()
import numpy as np  # noqa: E402

try:  # SciPy is preferred because it solves A c = sigma B c directly.
    import scipy  # noqa: E402
    import scipy.linalg  # noqa: E402
except ModuleNotFoundError:  # Reproducible fallback for the bundled runtime.
    scipy = None


HERE = Path(__file__).resolve().parent
START = time.monotonic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--scipy-deps", default="")
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--reference", default=str(HERE / "diagnostic.json"))
    parser.add_argument(
        "--output", default=str(HERE / "independent_validation.json")
    )
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def assemble_generalized_problem(
    alpha: float, reynolds: float, truncation: int
) -> tuple[np.ndarray, np.ndarray]:
    """Assemble A and B directly from the Fourier coefficients of the PDE."""
    modes = np.arange(-truncation, truncation + 1, dtype=np.float64)
    d = alpha * alpha + modes * modes
    dimension = modes.size
    a_matrix = np.zeros((dimension, dimension), dtype=np.float64)
    b_matrix = np.diag(-d)

    # R^{-1} Delta^2 is diagonal in the Fourier basis.
    a_matrix[np.diag_indices(dimension)] = d * d / reynolds

    # -sin(Y)(Delta+I)partial_X sends input j to output j+1 and j-1.
    # These entries are assembled by source column, independently of the
    # row-normalized tridiagonal formula used by the producer.
    for source_index, source_d in enumerate(d):
        coefficient = 0.5 * alpha * (1.0 - source_d)
        if source_index + 1 < dimension:
            a_matrix[source_index + 1, source_index] -= coefficient
        if source_index > 0:
            a_matrix[source_index - 1, source_index] += coefficient
    return a_matrix, b_matrix


def generalized_eigensystem(
    a_matrix: np.ndarray,
    b_matrix: np.ndarray,
    *,
    equilibrate_rows: bool,
) -> tuple[np.ndarray, np.ndarray, str]:
    if equilibrate_rows:
        # Left multiplication by an invertible diagonal matrix preserves every
        # generalized eigenvalue.  Here it removes the O(M^4) versus O(M^2)
        # scale disparity in the raw pencil before the QZ algorithm is called.
        b_diagonal = np.abs(np.diag(b_matrix))
        row_scale = 1.0 / b_diagonal
        solve_a = row_scale[:, np.newaxis] * a_matrix
        solve_b = row_scale[:, np.newaxis] * b_matrix
        suffix = " after |diag(B)| row equilibration"
    else:
        solve_a = a_matrix
        solve_b = b_matrix
        suffix = " on raw pencil"
    if scipy is not None:
        values, vectors = scipy.linalg.eig(
            solve_a,
            solve_b,
            right=True,
            check_finite=True,
            overwrite_a=False,
            overwrite_b=False,
        )
        return values, vectors, "scipy.linalg.eig(A,B)" + suffix

    # B is nonsingular because alpha != 0.  This fallback preserves the
    # independently assembled A,B path, although it reduces the problem to a
    # standard eigenproblem when SciPy is unavailable.
    reduced = np.linalg.solve(solve_b, solve_a)
    values, vectors = np.linalg.eig(reduced)
    return (
        values,
        vectors,
        "numpy.linalg.eig(solve(B,A)) fallback" + suffix,
    )


def leading_pair(alpha: float, reynolds: float, truncation: int) -> dict[str, object]:
    a_matrix, b_matrix = assemble_generalized_problem(alpha, reynolds, truncation)
    raw_values, raw_vectors, raw_solver = generalized_eigensystem(
        a_matrix, b_matrix, equilibrate_rows=False
    )
    values, vectors, solver = generalized_eigensystem(
        a_matrix, b_matrix, equilibrate_rows=True
    )
    raw_finite = np.isfinite(raw_values.real) & np.isfinite(raw_values.imag)
    if not np.all(raw_finite):
        raise RuntimeError("raw generalized eigensolver returned a nonfinite eigenvalue")
    finite = np.isfinite(values.real) & np.isfinite(values.imag)
    if not np.all(finite):
        raise RuntimeError("generalized eigensolver returned a nonfinite eigenvalue")
    raw_index = int(np.argmax(raw_values.real))
    raw_value = complex(raw_values[raw_index])
    raw_vector = raw_vectors[:, raw_index]
    index = int(np.argmax(values.real))
    value = complex(values[index])
    vector = vectors[:, index]
    raw_residual = np.linalg.norm(
        a_matrix @ raw_vector - raw_value * (b_matrix @ raw_vector)
    )
    residual = np.linalg.norm(a_matrix @ vector - value * (b_matrix @ vector))
    row_scale = 1.0 / np.abs(np.diag(b_matrix))
    equilibrated_a = row_scale[:, np.newaxis] * a_matrix
    equilibrated_b = row_scale[:, np.newaxis] * b_matrix
    equilibrated_residual = np.linalg.norm(
        equilibrated_a @ vector - value * (equilibrated_b @ vector)
    )
    raw_scale = (
        np.linalg.norm(a_matrix, ord=2)
        + abs(raw_value) * np.linalg.norm(b_matrix, ord=2)
    ) * np.linalg.norm(raw_vector)
    scale = (
        np.linalg.norm(a_matrix, ord=2)
        + abs(value) * np.linalg.norm(b_matrix, ord=2)
    ) * np.linalg.norm(vector)
    equilibrated_scale = (
        np.linalg.norm(equilibrated_a, ord=2)
        + abs(value) * np.linalg.norm(equilibrated_b, ord=2)
    ) * np.linalg.norm(vector)
    relative = float(residual / scale)
    return {
        "truncation": truncation,
        "matrixDimension": int(2 * truncation + 1),
        "leadingEigenvalueReal": float(value.real),
        "leadingEigenvalueImaginary": float(value.imag),
        "absoluteGeneralizedResidual": float(residual),
        "relativeGeneralizedResidual": relative,
        "equilibratedAbsoluteGeneralizedResidual": float(
            equilibrated_residual
        ),
        "equilibratedRelativeGeneralizedResidual": float(
            equilibrated_residual / equilibrated_scale
        ),
        "solver": solver,
        "rawPencilLeadingEigenvalueReal": float(raw_value.real),
        "rawPencilLeadingEigenvalueImaginary": float(raw_value.imag),
        "rawPencilRelativeGeneralizedResidual": float(raw_residual / raw_scale),
        "rawPencilSolver": raw_solver,
        "absoluteRawToEquilibratedSigmaDifference": abs(
            float(raw_value.real) - float(value.real)
        ),
    }


def finite_crossing(
    alpha: float,
    truncation: int,
    lower: float,
    upper: float,
    iterations: int = 56,
) -> float:
    def abscissa(reynolds: float) -> float:
        return float(
            leading_pair(alpha, reynolds, truncation)["leadingEigenvalueReal"]
        )

    lower_value = abscissa(lower)
    upper_value = abscissa(upper)
    if not lower_value < 0.0 < upper_value:
        raise RuntimeError("finite critical bracket does not straddle zero")
    for _ in range(iterations):
        midpoint = 0.5 * (lower + upper)
        if abscissa(midpoint) > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    return 0.5 * (lower + upper)


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    reference_path = Path(args.reference).resolve()
    output_path = Path(args.output).resolve()
    if output_path.name != "independent_validation.json":
        raise RuntimeError("output filename must be independent_validation.json")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    if config.get("schemaVersion") != "r073o-kolmogorov-spectrum-config-v1":
        raise RuntimeError("configuration schema drift")
    if reference.get("schemaVersion") != "r073o-kolmogorov-spectrum-diagnostic-v1":
        raise RuntimeError("reference diagnostic schema drift")

    alpha = float(config["alpha"])
    target_reynolds = float(config["targetReynolds"])
    amplitude = float(config["forcingAmplitude"])
    forcing_mode = int(config["forcingWaveNumber"])
    viscosity = float(config["viscosity"])
    primary_truncation = int(config["primaryTruncation"])
    truncations = [int(value) for value in config["truncations"]]
    rigorous_lower, rigorous_upper = map(float, config["rigorousCriticalInterval"])

    convergence: list[dict[str, object]] = []
    for truncation in truncations:
        item = leading_pair(alpha, target_reynolds, truncation)
        sigma = float(item["leadingEigenvalueReal"])
        item["physicalGrowthRate"] = amplitude * forcing_mode * sigma
        convergence.append(item)

    primary = next(
        item for item in convergence if item["truncation"] == primary_truncation
    )
    primary_sigma = float(primary["leadingEigenvalueReal"])
    physical_growth = float(primary["physicalGrowthRate"])
    for item in convergence:
        item["absoluteDifferenceFromPrimary"] = abs(
            float(item["leadingEigenvalueReal"]) - primary_sigma
        )

    crossing = finite_crossing(
        alpha,
        primary_truncation,
        float(config["sweep"]["start"]),
        float(config["sweep"]["end"]),
    )
    reference_results = reference["finiteResults"]
    reference_sigma = float(reference_results["leadingEigenvalueReal"])
    reference_growth = float(reference_results["physicalGrowthRate"])
    reference_crossing = float(reference_results["finiteCriticalCrossing"])
    tail_spread = max(
        abs(float(item["leadingEigenvalueReal"]) - primary_sigma)
        for item in convergence
        if int(item["truncation"]) >= 20
    )
    max_equilibrated_relative_residual = max(
        float(item["equilibratedRelativeGeneralizedResidual"])
        for item in convergence
    )
    tolerances = config["checks"]
    checks = {
        "alphaEmbeddingIdentity": math.isclose(
            alpha,
            int(config["physicalXWaveNumber"]) / forcing_mode,
            rel_tol=0.0,
            abs_tol=1e-15,
        ),
        "reynoldsScalingIdentity": math.isclose(
            target_reynolds,
            amplitude / (viscosity * forcing_mode),
            rel_tol=0.0,
            abs_tol=1e-15,
        ),
        "primarySigmaPositive": primary_sigma > 0.0,
        "primaryEigenvalueNumericallyReal": abs(
            float(primary["leadingEigenvalueImaginary"])
        ) < 1e-12,
        "allEquilibratedGeneralizedResidualsSmall": (
            max_equilibrated_relative_residual < 5e-12
        ),
        "tailConvergenceFromM20Small": tail_spread
        <= float(tolerances["maxConvergenceSpreadFromN20"]),
        "independentSigmaMatchesProducer": abs(primary_sigma - reference_sigma)
        < 5e-13,
        "physicalGrowthMatchesProducer": abs(physical_growth - reference_growth)
        < 2e-10,
        "finiteCrossingMatchesProducer": abs(crossing - reference_crossing) < 5e-12,
        "rawPencilScaleDriftRemainsSmallInSign": (
            float(primary["rawPencilLeadingEigenvalueReal"]) > 0.0
            and float(primary["absoluteRawToEquilibratedSigmaDifference"]) < 5e-10
        ),
        "targetAboveImportedRigorousInterval": target_reynolds > rigorous_upper,
    }
    status = "passed" if all(checks.values()) else "failed"

    result = {
        "schemaVersion": "r073o-kolmogorov-spectrum-independent-validation-v1",
        "release": "R0.73O",
        "status": status,
        "allChecksPass": all(checks.values()),
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "method": {
            "equation": "A c = sigma B c",
            "assembly": (
                "A and B assembled by source Fourier column directly from "
                "sigma Delta phi - R^-1 Delta^2 phi + "
                "sin(Y)(Delta+I)partial_X phi = 0"
            ),
            "producerCodeImported": False,
            "primarySolver": primary["solver"],
            "rawPencilSolver": primary["rawPencilSolver"],
            "rowEquilibration": (
                "left multiply both A and B by diag(1/abs(diag(B))); "
                "this preserves the generalized eigenvalues"
            ),
        },
        "parameters": {
            "alpha": alpha,
            "targetReynolds": target_reynolds,
            "forcingAmplitude": amplitude,
            "forcingWaveNumber": forcing_mode,
            "viscosity": viscosity,
            "primaryTruncation": primary_truncation,
            "physicalGrowthRule": "lambda=A*N*sigma",
        },
        "independentFiniteResults": {
            "leadingEigenvalueReal": primary_sigma,
            "leadingEigenvalueImaginary": float(
                primary["leadingEigenvalueImaginary"]
            ),
            "physicalGrowthRate": physical_growth,
            "physicalEfoldingTime": 1.0 / physical_growth,
            "relativeGeneralizedResidual": float(
                primary["relativeGeneralizedResidual"]
            ),
            "equilibratedRelativeGeneralizedResidual": float(
                primary["equilibratedRelativeGeneralizedResidual"]
            ),
            "maxEquilibratedRelativeGeneralizedResidualAcrossTruncations": (
                max_equilibrated_relative_residual
            ),
            "tailSpreadFromM20": tail_spread,
            "finiteCriticalCrossing": crossing,
            "rawPencilLeadingEigenvalueReal": float(
                primary["rawPencilLeadingEigenvalueReal"]
            ),
            "absoluteRawToEquilibratedSigmaDifference": float(
                primary["absoluteRawToEquilibratedSigmaDifference"]
            ),
        },
        "producerComparison": {
            "producerSigma": reference_sigma,
            "absoluteSigmaDifference": abs(primary_sigma - reference_sigma),
            "producerPhysicalGrowthRate": reference_growth,
            "absolutePhysicalGrowthDifference": abs(
                physical_growth - reference_growth
            ),
            "producerFiniteCriticalCrossing": reference_crossing,
            "absoluteFiniteCrossingDifference": abs(crossing - reference_crossing),
        },
        "convergence": convergence,
        "checks": checks,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": None if scipy is None else scipy.__version__,
            "platform": platform.platform(),
        },
        "compute": {
            "executionHost": "local workstation",
            "gpu": "not used",
            "processes": 1,
            "wallTimeSeconds": time.monotonic() - START,
        },
        "claimBoundary": {
            "finiteFourierDiagnosticOnly": True,
            "provesInfiniteDimensionalSpectrum": False,
            "replacesNagatouComputerAssistedCertificate": False,
            "provesNonlinearInstability": False,
            "provesThreeDimensionalSingularity": False,
            "solvesClayProblem": False,
        },
        "externalRigorousInput": {
            "criticalInterval": [rigorous_lower, rigorous_upper],
            "recomputedByThisScript": False,
            "usedOnlyForComparison": True,
        },
    }
    output_path.write_text(canonical(result), encoding="utf-8")
    print(
        canonical(
            {
                "status": status,
                "solver": primary["solver"],
                "sigmaMax": primary_sigma,
                "physicalGrowthRate": physical_growth,
                "finiteCriticalCrossing": crossing,
                "absoluteSigmaDifference": abs(primary_sigma - reference_sigma),
                "tailSpreadFromM20": tail_spread,
                "maxEquilibratedRelativeGeneralizedResidual": (
                    max_equilibrated_relative_residual
                ),
            }
        ),
        end="",
    )
    if status != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
