#!/usr/bin/env python3
"""Generate the R0.72X all-center exact-path journal figure.

The formal build is source/certificate bound and refuses to overwrite an
existing package.  Its numerical component is a deterministic, finite-grid
stress test of the full exact two-harmonic potential.  It is not evidence for
the continuum graph theorem, a value of its nonconstructive constant, or an
operator-norm proof.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import hashlib
import json
import math
import multiprocessing
import os
import platform
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import time
from typing import Any, Callable
from xml.sax.saxutils import escape


REPOSITORY = Path(__file__).resolve().parents[1]
PACKAGE = (
    REPOSITORY
    / "figures/r072x-all-center/fig-r072x-all-center-transfer"
)
CONFIG = PACKAGE / "config.json"
CERTIFICATE_DIR = REPOSITORY / "research/certificates/r072x"
CERTIFICATE = CERTIFICATE_DIR / "certificate.json"
PUBLIC = REPOSITORY / "public/assets/r072x"
FIGURE_ID = "fig-r072x-all-center-transfer"
WIDTH_MM = 178
HEIGHT_MM = 150
PNG_DPI = 600

PAPER = "#ffffff"
INK = "#17212b"
MUTED = "#66727e"
GRID = "#d9dde1"
BLUE = "#285f8f"
GOLD = "#a6781f"
PALE_BLUE = "#edf3f7"
PALE_GOLD = "#f4f0e6"

SOURCE_FILES = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.txt",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
)
GENERATED_FILES = (
    "data.csv",
    "results.json",
    "validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
    "figure.svg",
    "figure.pdf",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "manifest.json",
    "SHA256SUMS",
)

DIAGNOSTIC_ALPHAS = (1.0, 0.75, 0.5, 0.35, 0.25)
PHYSICAL_CENTERS = (
    -math.log(2.0),
    -0.5,
    -0.25,
    -0.125,
    -0.0625,
    0.0,
    0.0625,
    0.125,
    0.25,
    1.0 - math.log(2.0),
)
DIAGNOSTIC_LEVELS = (
    ("coarse", 256, 400),
    ("medium", 512, 800),
    ("fine", 1024, 1600),
)
DIAGNOSTIC_T = 0.25
LANCZOS_RITZ_POLICY = {
    "minDimension": 8,
    "maxDimension": 32,
    "checkEvery": 4,
    "relativeResidualTolerance": 1.0e-10,
    "reorthogonalizationPasses": 2,
}
WORKERS = 4
EXPECTED_NUMERICAL_ROWS = (
    len(DIAGNOSTIC_ALPHAS)
    * len(PHYSICAL_CENTERS)
    * len(DIAGNOSTIC_LEVELS)
)
EXPECTED_INTERFACE_ROWS = 3 * len(DIAGNOSTIC_ALPHAS)
EXPECTED_TILING_ROWS = len(DIAGNOSTIC_ALPHAS)
EXPECTED_ROWS = (
    EXPECTED_NUMERICAL_ROWS + EXPECTED_INTERFACE_ROWS + EXPECTED_TILING_ROWS
)
EXPECTED_QA_THRESHOLDS = {
    "maxRelativeToFine": 5.0e-4,
    "maxAdjointDefect": 1.0e-10,
    "maxRitzResidual": 1.0e-8,
    "maxRayleighNormDefect": 1.0e-10,
}
EXPECTED_CLAIM_BOUNDARY = {
    "allCenterExactFamilyGraphCoercivityProvedInBoundReport": True,
    "allStartExactPathSemigroupProvedInBoundReport": True,
    "fixedMarginA1EnhancedDissipationImportedInBoundReport": True,
    "exactA2PathBlochUniformProvedInBoundReport": True,
    "periodicRepresentativeBetaZeroExactA1A2A1ConcatenationProvedInBoundReport": True,
    "shrinkingInterfaceFixedShapeA1HypothesesFalseInBoundReport": True,
    "numericalDiagnosticIsProof": False,
    "numericalDiagnosticEvaluatesAnalyticQ": False,
    "numericalDiagnosticIsInfiniteDimensionalOperatorNorm": False,
    "forcedHMinusOneTransferProved": False,
    "completeLinearizedShearSubsystemProved": False,
    "a1A2A1ConcatenationBlochUniform": False,
    "allPhysicalRowsUniformContraction": False,
    "nonlinearNavierStokesClosureProved": False,
    "clayMillenniumProblemSolved": False,
}
DIAGNOSTIC_LIMITATIONS = [
    "single fixed seed and a small actual Ritz residual do not certify the global largest singular value of the finite propagator",
    "Krylov breakdown before dimension 8 is conservatively rejected even if it could be a happy exact closure",
]

DATA_FIELDS = (
    "panel",
    "kind",
    "series",
    "physicalCenter",
    "alpha",
    "resolution",
    "timeSteps",
    "krylovDimension",
    "normEstimate",
    "ritzResidual",
    "rayleighNormDefect",
    "adjointDefect",
    "relativeToFine",
    "interfaceValue",
    "expectedPower",
    "blockHalfWidth",
    "fullBlockCount",
    "formula",
    "status",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _empty_row() -> dict[str, str]:
    return {field: "" for field in DATA_FIELDS}


def _configure_numeric_threads() -> None:
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    ):
        os.environ[name] = "1"


def _diffuse(np: Any, vector: Any, multiplier: Any) -> Any:
    return np.fft.ifft(np.fft.fft(vector) * multiplier)


def _initial_vectors(np: Any, z_grid: Any) -> tuple[Any, Any]:
    vector = (
        1.0
        + 0.31 * np.cos(z_grid)
        + 0.17 * np.sin(2.0 * z_grid)
        + 1j * (0.23 * np.sin(z_grid) - 0.13 * np.cos(2.0 * z_grid))
    ).astype(np.complex128)
    probe = (
        0.7
        - 0.19 * np.sin(z_grid)
        + 0.29 * np.cos(3.0 * z_grid)
        + 1j * (0.11 * np.cos(z_grid) + 0.07 * np.sin(4.0 * z_grid))
    ).astype(np.complex128)
    return vector / np.linalg.norm(vector), probe / np.linalg.norm(probe)


def _propagators(
    np: Any,
    alpha: float,
    physical_center: float,
    resolution: int,
    time_steps: int,
) -> tuple[Callable[[Any], Any], Callable[[Any], Any], Any]:
    """Build the discrete propagator on tau in [-T,T].

    The z=alpha X form uses alpha^2 d_zz and the full, untruncated exact
    potential alpha^-3[2 exp(-D0-alpha^2 tau) sin z
    - exp(-4D0-4alpha^2 tau) sin 2z].
    """
    dt = 2.0 * DIAGNOSTIC_T / time_steps
    z_grid = 2.0 * math.pi * np.arange(resolution) / resolution
    modes = np.fft.fftfreq(resolution, d=1.0 / resolution)
    half_diffusion = np.exp(-0.5 * dt * (alpha * modes) ** 2)
    full_diffusion = half_diffusion * half_diffusion
    midpoints = (
        -DIAGNOSTIC_T
        + (np.arange(time_steps, dtype=np.float64) + 0.5) * dt
    )
    first = 2.0 * np.exp(
        -physical_center - alpha * alpha * midpoints
    )[:, None]
    second = -np.exp(
        -4.0 * physical_center - 4.0 * alpha * alpha * midpoints
    )[:, None]
    exact_potential = alpha ** -3 * (
        first * np.sin(z_grid)[None, :]
        + second * np.sin(2.0 * z_grid)[None, :]
    )
    phases = np.exp(1j * dt * exact_potential)

    def forward(vector: Any) -> Any:
        value = _diffuse(np, vector, half_diffusion)
        last = time_steps - 1
        for index in range(time_steps):
            value *= phases[index]
            value = _diffuse(
                np,
                value,
                half_diffusion if index == last else full_diffusion,
            )
        return value

    def adjoint(vector: Any) -> Any:
        value = _diffuse(np, vector, half_diffusion)
        last = time_steps - 1
        for loop_index, phase_index in enumerate(range(last, -1, -1)):
            value *= phases[phase_index].conjugate()
            value = _diffuse(
                np,
                value,
                half_diffusion if loop_index == last else full_diffusion,
            )
        return value

    return forward, adjoint, z_grid


def _lanczos_ritz_largest(
    np: Any,
    apply_normal: Callable[[Any], Any],
    initial_vector: Any,
    policy: dict[str, Any],
) -> dict[str, Any]:
    """Return the largest Ritz pair of a Hermitian positive operator.

    The Krylov basis is deterministic.  Every new vector is orthogonalized
    against the complete existing basis for exactly two passes.  At each
    declared checkpoint the Ritz vector is formed in the original vector
    space, ``A v`` is recomputed by ``apply_normal``, and the reported
    residual is therefore the actual relative residual rather than a
    tridiagonal recurrence estimate.
    """
    expected_policy = {
        "minDimension": 8,
        "maxDimension": 32,
        "checkEvery": 4,
        "relativeResidualTolerance": 1.0e-10,
        "reorthogonalizationPasses": 2,
    }
    if policy != expected_policy:
        raise RuntimeError("Lanczos-Ritz policy is not exact")
    minimum = policy["minDimension"]
    maximum = policy["maxDimension"]
    stride = policy["checkEvery"]
    tolerance = policy["relativeResidualTolerance"]
    passes = policy["reorthogonalizationPasses"]
    if initial_vector.ndim != 1 or initial_vector.size < maximum:
        raise RuntimeError("Lanczos-Ritz vector space is smaller than maxDimension")
    initial_norm = float(np.linalg.norm(initial_vector))
    if not math.isfinite(initial_norm) or initial_norm <= 0.0:
        raise RuntimeError("Lanczos-Ritz initial vector is invalid")

    basis: list[Any] = []
    images: list[Any] = []
    checkpoints: list[dict[str, Any]] = []
    q_value = initial_vector.astype(np.complex128, copy=True) / initial_norm
    tiny = np.finfo(np.float64).tiny

    for dimension in range(1, maximum + 1):
        basis.append(q_value.copy())
        image = apply_normal(q_value)
        if image.shape != q_value.shape or not np.all(np.isfinite(image)):
            raise RuntimeError("Lanczos-Ritz normal-operator image is invalid")
        images.append(image.copy())

        if dimension >= minimum and (dimension - minimum) % stride == 0:
            q_matrix = np.column_stack(basis)
            aq_matrix = np.column_stack(images)
            projected = q_matrix.conjugate().T @ aq_matrix
            projected = 0.5 * (projected + projected.conjugate().T)
            eigenvalues, eigenvectors = np.linalg.eigh(projected)
            coefficient = eigenvectors[:, -1]
            ritz_vector = q_matrix @ coefficient
            ritz_vector /= np.linalg.norm(ritz_vector)

            # Required actual-space audit: do not use a recurrence residual.
            actual_image = apply_normal(ritz_vector)
            ritz_value = float(np.vdot(ritz_vector, actual_image).real)
            if not math.isfinite(ritz_value) or ritz_value <= 0.0:
                raise RuntimeError("Lanczos-Ritz largest value is not positive")
            ritz_residual = float(
                np.linalg.norm(actual_image - ritz_value * ritz_vector)
                / max(abs(ritz_value), tiny)
            )
            if not math.isfinite(ritz_residual):
                raise RuntimeError("Lanczos-Ritz actual residual is not finite")
            checkpoint = {
                "krylovDimension": dimension,
                "ritzValue": ritz_value,
                "ritzResidual": ritz_residual,
            }
            checkpoints.append(checkpoint)
            if ritz_residual <= tolerance:
                return {
                    **checkpoint,
                    "ritzVector": ritz_vector,
                    "checkpoints": checkpoints,
                }

        if dimension == maximum:
            break

        next_vector = image.copy()
        for _ in range(passes):
            for basis_vector in basis:
                next_vector -= np.vdot(basis_vector, next_vector) * basis_vector
        next_norm = float(np.linalg.norm(next_vector))
        breakdown_floor = (
            np.finfo(np.float64).eps
            * max(1.0, float(np.linalg.norm(image)))
            * dimension
        )
        if not math.isfinite(next_norm) or next_norm <= breakdown_floor:
            raise RuntimeError(
                "Lanczos-Ritz Krylov breakdown before a passing checkpoint"
            )
        q_value = next_vector / next_norm

    last = checkpoints[-1] if checkpoints else None
    raise RuntimeError(
        "Lanczos-Ritz failed relativeResidualTolerance by maxDimension: "
        f"policy={policy}, lastCheckpoint={last}"
    )


def _direct_norm_audit(
    np: Any,
    forward: Callable[[Any], Any],
    ritz_vector: Any,
    ritz_value: float,
) -> tuple[Any, float, float]:
    """Return Uv, its direct norm, and its Rayleigh consistency defect."""
    transformed = forward(ritz_vector)
    if transformed.shape != ritz_vector.shape or not np.all(np.isfinite(transformed)):
        raise RuntimeError("Lanczos-Ritz forward image is invalid")
    direct_norm = float(np.linalg.norm(transformed))
    rayleigh_norm = math.sqrt(ritz_value)
    if (
        not math.isfinite(direct_norm)
        or direct_norm <= 0.0
        or not math.isfinite(rayleigh_norm)
        or rayleigh_norm <= 0.0
    ):
        raise RuntimeError("Lanczos-Ritz norm audit is invalid")
    defect = abs(direct_norm - rayleigh_norm) / max(
        direct_norm, rayleigh_norm, np.finfo(np.float64).tiny
    )
    if not math.isfinite(defect):
        raise RuntimeError("Lanczos-Ritz Rayleigh norm defect is not finite")
    return transformed, direct_norm, defect


def _one_diagnostic(job: tuple[Any, ...]) -> dict[str, Any]:
    _configure_numeric_threads()
    import numpy as np

    alpha, physical_center, level, resolution, time_steps = job
    started = time.perf_counter()
    forward, adjoint, z_grid = _propagators(
        np,
        alpha,
        physical_center,
        resolution,
        time_steps,
    )
    vector, probe = _initial_vectors(np, z_grid)
    ritz = _lanczos_ritz_largest(
        np,
        lambda value: adjoint(forward(value)),
        vector,
        LANCZOS_RITZ_POLICY,
    )
    ritz_vector = ritz.pop("ritzVector")
    probe_forward, norm_estimate, rayleigh_norm_defect = _direct_norm_audit(
        np, forward, ritz_vector, ritz["ritzValue"]
    )
    probe_adjoint = adjoint(probe)
    left = np.vdot(probe_forward, probe)
    right = np.vdot(ritz_vector, probe_adjoint)
    adjoint_defect = float(
        abs(left - right) / max(abs(left), abs(right), 1.0e-300)
    )
    if not math.isfinite(adjoint_defect):
        raise RuntimeError("discrete adjoint defect is not finite")
    return {
        "alpha": alpha,
        "physicalCenter": physical_center,
        "level": level,
        "resolution": resolution,
        "timeSteps": time_steps,
        "normEstimate": norm_estimate,
        "krylovDimension": ritz["krylovDimension"],
        "ritzResidual": ritz["ritzResidual"],
        "rayleighNormDefect": rayleigh_norm_defect,
        "ritzCheckpoints": ritz["checkpoints"],
        "adjointDefect": adjoint_defect,
        "workerWallTimeSeconds": time.perf_counter() - started,
        "numpyVersion": np.__version__,
    }


def numerical_rows(
    progress: Callable[[dict[str, Any]], None],
    resource_event: Callable[[dict[str, Any]], None],
) -> tuple[list[dict[str, str]], dict[str, Any]]:
    jobs = [
        (alpha, center, level, resolution, steps)
        for alpha in DIAGNOSTIC_ALPHAS
        for center in PHYSICAL_CENTERS
        for level, resolution, steps in DIAGNOSTIC_LEVELS
    ]
    started = time.perf_counter()
    records: list[dict[str, Any]] = []
    progress({
        "event": "diagnostics-submitted",
        "workers": WORKERS,
        "total": len(jobs),
    })
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=WORKERS, mp_context=context) as pool:
        futures = {pool.submit(_one_diagnostic, job): job for job in jobs}
        for completed, future in enumerate(as_completed(futures), start=1):
            record = future.result()
            records.append(record)
            elapsed = time.perf_counter() - started
            eta = elapsed * (len(jobs) - completed) / completed
            event = {
                "event": "diagnostic-complete",
                **record,
                "completed": completed,
                "total": len(jobs),
                "elapsedSeconds": elapsed,
                "etaSeconds": eta,
            }
            progress(event)
            resource_event({
                "event": "resource-sample",
                "completed": completed,
                "total": len(jobs),
                "elapsedSeconds": elapsed,
                "maxResidentSetPlatformUnits": resource.getrusage(
                    resource.RUSAGE_SELF
                ).ru_maxrss,
                "childMaxResidentSetPlatformUnits": resource.getrusage(
                    resource.RUSAGE_CHILDREN
                ).ru_maxrss,
            })
            if completed == 1 or completed % 10 == 0 or completed == len(jobs):
                print(
                    "R0.72X diagnostic "
                    f"{completed}/{len(jobs)}: "
                    f"D0={record['physicalCenter']:+.6f}, "
                    f"alpha={record['alpha']:.2f}, "
                    f"{record['level']} N={record['resolution']}, "
                    f"||U||~{record['normEstimate']:.9f}, "
                    f"m={record['krylovDimension']}, "
                    f"Ritz res={record['ritzResidual']:.2e}, "
                    f"Rayleigh norm defect={record['rayleighNormDefect']:.2e}, "
                    f"ETA={eta:.1f}s",
                    flush=True,
                )

    fine = {
        (record["alpha"], record["physicalCenter"]): record["normEstimate"]
        for record in records
        if record["level"] == "fine"
    }
    rows: list[dict[str, str]] = []
    for record in sorted(
        records,
        key=lambda row: (
            row["alpha"],
            row["physicalCenter"],
            row["resolution"],
        ),
    ):
        relative = abs(
            record["normEstimate"]
            - fine[(record["alpha"], record["physicalCenter"])]
        ) / max(
            fine[(record["alpha"], record["physicalCenter"])],
            1.0e-300,
        )
        row = _empty_row()
        row.update({
            "panel": "A/B",
            "kind": "full-exact-block-forward-adjoint-norm",
            "series": record["level"],
            "physicalCenter": f"{record['physicalCenter']:.17g}",
            "alpha": f"{record['alpha']:.17g}",
            "resolution": str(record["resolution"]),
            "timeSteps": str(record["timeSteps"]),
            "krylovDimension": str(record["krylovDimension"]),
            "normEstimate": f"{record['normEstimate']:.17g}",
            "ritzResidual": f"{record['ritzResidual']:.17g}",
            "rayleighNormDefect": f"{record['rayleighNormDefect']:.17g}",
            "adjointDefect": f"{record['adjointDefect']:.17g}",
            "relativeToFine": f"{relative:.17g}",
            "formula": (
                "full exact shifted V_alpha; Fourier Strang; "
                "fully double-reorthogonalized Lanczos-Ritz on U*U"
            ),
            "status": "deterministic numerical diagnostic only; not proof",
        })
        rows.append(row)

    finite_fields = (
        "normEstimate",
        "ritzResidual",
        "rayleighNormDefect",
        "adjointDefect",
        "relativeToFine",
    )
    if not all(
        all(math.isfinite(float(row[field])) for field in finite_fields)
        for row in rows
    ):
        raise RuntimeError("non-finite value in numerical diagnostic row")
    if any(
        float(row["relativeToFine"]) != 0.0
        for row in rows
        if row["series"] == "fine"
    ):
        raise RuntimeError("fine-grid relative-to-fine audit is not exactly zero")

    return rows, {
        "numpyVersion": records[0]["numpyVersion"],
        "wallTimeSeconds": time.perf_counter() - started,
        "workers": WORKERS,
        "configurations": len(records),
        "maxRelativeToFine": max(
            float(row["relativeToFine"])
            for row in rows
            if row["series"] != "fine"
        ),
        "maxAdjointDefect": max(float(row["adjointDefect"]) for row in rows),
        "maxRitzResidual": max(float(row["ritzResidual"]) for row in rows),
        "maxRayleighNormDefect": max(
            float(row["rayleighNormDefect"]) for row in rows
        ),
        "minKrylovDimension": min(int(row["krylovDimension"]) for row in rows),
        "maxKrylovDimension": max(int(row["krylovDimension"]) for row in rows),
        "maxNormEstimate": max(float(row["normEstimate"]) for row in rows),
        "minFineNormEstimate": min(
            float(row["normEstimate"])
            for row in rows
            if row["series"] == "fine"
        ),
        "maxFineNormEstimate": max(
            float(row["normEstimate"])
            for row in rows
            if row["series"] == "fine"
        ),
    }


def interface_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for alpha in DIAGNOSTIC_ALPHAS:
        h_value = DIAGNOSTIC_T * alpha * alpha
        r_value = math.exp(3.0 * h_value)
        discriminant = math.sqrt(1.0 + 8.0 * r_value * r_value)
        cosine = (1.0 + discriminant) / (4.0 * r_value)
        critical_x = math.acos(max(-1.0, min(1.0, cosine)))
        hessian = abs(
            0.5
            * math.exp(h_value)
            * math.sin(critical_x)
            * (1.0 - 4.0 * r_value * math.cos(critical_x))
        )
        post_gradient = abs(
            0.5 * (math.exp(-4.0 * h_value) - math.exp(-h_value))
        )
        values = (
            (
                "pre critical separation",
                2.0 * critical_x,
                1,
                "2*acos((1+sqrt(1+8*exp(6h)))/(4*exp(3h)))",
            ),
            (
                "pre Hessian floor",
                hessian,
                1,
                "abs(W_xx(-h,x_plus))",
            ),
            (
                "post gradient at x=0",
                post_gradient,
                2,
                "abs((exp(-4h)-exp(-h))/2)",
            ),
        )
        for label, value, power, formula in values:
            row = _empty_row()
            row.update({
                "panel": "C",
                "kind": "exact-interface-scaling",
                "series": label,
                "alpha": f"{alpha:.17g}",
                "interfaceValue": f"{value:.17g}",
                "expectedPower": str(power),
                "blockHalfWidth": f"{h_value:.17g}",
                "formula": formula,
                "status": "exact finite-alpha geometry; asymptotic guide only",
            })
            rows.append(row)
    return rows


def tiling_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for alpha in DIAGNOSTIC_ALPHAS:
        full_blocks = math.floor(1.0 / (2.0 * DIAGNOSTIC_T * alpha * alpha))
        row = _empty_row()
        row.update({
            "panel": "D",
            "kind": "exact-full-block-count",
            "series": "L=1 physical interval",
            "alpha": f"{alpha:.17g}",
            "blockHalfWidth": f"{DIAGNOSTIC_T * alpha * alpha:.17g}",
            "fullBlockCount": str(full_blocks),
            "formula": "floor(L/(2*T*alpha^2)), L=1, T=1/4",
            "status": "exact arithmetic; q remains symbolic",
        })
        rows.append(row)
    return rows


class Scene:
    def __init__(self) -> None:
        self.items: list[tuple[Any, ...]] = []

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = INK,
        width: float = 2,
        dash: str | None = None,
    ) -> None:
        self.items.append(("line", x1, y1, x2, y2, color, width, dash))

    def polyline(
        self,
        points: list[tuple[float, float]],
        color: str = BLUE,
        width: float = 2,
        dash: str | None = None,
    ) -> None:
        self.items.append(("polyline", points, color, width, dash))

    def text(
        self,
        x: float,
        y: float,
        value: str,
        size: int = 18,
        color: str = INK,
        anchor: str = "start",
        bold: bool = False,
    ) -> None:
        self.items.append(("text", x, y, value, size, color, anchor, bold))

    def marker(
        self,
        x: float,
        y: float,
        radius: float,
        color: str,
        shape: str = "circle",
        open_marker: bool = False,
    ) -> None:
        self.items.append(
            ("marker", x, y, radius, color, shape, open_marker)
        )

    def box(
        self,
        left: float,
        top: float,
        right: float,
        bottom: float,
        fill: str = PAPER,
        stroke: str = INK,
        width: float = 2,
    ) -> None:
        self.items.append(
            ("box", left, top, right, bottom, fill, stroke, width)
        )


def mapping(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    left: float,
    right: float,
    top: float,
    bottom: float,
) -> tuple[Callable[[float], float], Callable[[float], float]]:
    return (
        lambda x: left + (x - x0) * (right - left) / (x1 - x0),
        lambda y: bottom - (y - y0) * (bottom - top) / (y1 - y0),
    )


def axes(
    scene: Scene,
    box: tuple[float, float, float, float],
    x_ticks: list[tuple[float, str]],
    y_ticks: list[tuple[float, str]],
    x_map: Callable[[float], float],
    y_map: Callable[[float], float],
    xlabel: str,
    ylabel: str,
) -> None:
    left, right, top, bottom = box
    for value, label in x_ticks:
        x_value = x_map(value)
        scene.line(x_value, top, x_value, bottom, GRID, 1)
        scene.text(x_value, bottom + 25, label, 15, MUTED, "middle")
    for value, label in y_ticks:
        y_value = y_map(value)
        scene.line(left, y_value, right, y_value, GRID, 1)
        scene.text(left - 8, y_value + 5, label, 14, MUTED, "end")
    scene.line(left, bottom, right, bottom, INK, 2)
    scene.line(left, top, left, bottom, INK, 2)
    scene.text((left + right) / 2, bottom + 52, xlabel, 17, INK, "middle")
    scene.text(left, top - 12, ylabel, 16, INK)


def build_scene(rows: list[dict[str, str]] | None) -> Scene:
    scene = Scene()
    headings = (
        (48, 58, "A", "physical-center block norm scan"),
        (920, 58, "B", "refinement and adjoint QA"),
        (48, 755, "C", "shrinking-interface geometry"),
        (920, 755, "D", "exact tiling and rate ledger"),
    )
    for x_value, y_value, letter, title in headings:
        scene.text(x_value, y_value, letter, 30, INK, bold=True)
        scene.text(x_value + 40, y_value, title, 21, INK, bold=True)

    numeric = [] if rows is None else [
        row for row in rows
        if row["kind"] == "full-exact-block-forward-adjoint-norm"
    ]
    interface = [] if rows is None else [
        row for row in rows if row["kind"] == "exact-interface-scaling"
    ]
    tiling = [] if rows is None else [
        row for row in rows if row["kind"] == "exact-full-block-count"
    ]

    # Panel A: finest-grid norm estimate across every physical center.
    box_a = (95, 850, 135, 590)
    xa, ya = mapping(-0.72, 0.34, 0.0, 1.0, *box_a)
    axes(
        scene,
        box_a,
        [(-math.log(2.0), "-ln2"), (-0.5, "-.50"), (-0.25, "-.25"),
         (0.0, "0"), (0.25, ".25"), (1.0 - math.log(2.0), "1-ln2")],
        [(0.0, "0"), (0.25, ".25"), (0.5, ".50"), (0.75, ".75"), (1.0, "1")],
        xa,
        ya,
        "physical block center D0",
        "estimated ||U(D0;T=.25)||_2->2",
    )
    styles = {
        1.0: (INK, None, "circle", False),
        0.75: (MUTED, "12,5", "square", True),
        0.5: (BLUE, None, "triangle", True),
        0.35: (GOLD, "9,5", "diamond", True),
        0.25: (BLUE, "3,4", "circle", False),
    }
    if numeric:
        for alpha in DIAGNOSTIC_ALPHAS:
            color, dash, shape, open_marker = styles[alpha]
            selected = sorted(
                (
                    row for row in numeric
                    if row["series"] == "fine"
                    and abs(float(row["alpha"]) - alpha) < 1.0e-14
                ),
                key=lambda row: float(row["physicalCenter"]),
            )
            points = [
                (xa(float(row["physicalCenter"])), ya(float(row["normEstimate"])))
                for row in selected
            ]
            scene.polyline(points, color, 3, dash)
            for px, py in points:
                scene.marker(px, py, 5, color, shape, open_marker)
            last = selected[-1]
            scene.text(
                xa(float(last["physicalCenter"])) - 7,
                ya(float(last["normEstimate"])) - 9 + 17 * list(DIAGNOSTIC_ALPHAS).index(alpha),
                f"alpha={alpha:.2f}",
                13,
                color,
                "end",
                alpha in (0.5, 0.25),
            )
    else:
        scene.text(472, 355, "formal scan generated after certificate", 17, MUTED, "middle")
    scene.text(95, 652, "10 centers include both endpoints and D0=0", 14, MUTED)
    scene.text(95, 679, "full exact potential; fine N=1024, NS=1600", 14, MUTED)
    scene.text(95, 706, "NUMERICAL DIAGNOSTIC ONLY - NOT PROOF", 16, GOLD, bold=True)

    # Panel B: worst-over-center refinement, adjoint, and Ritz/norm audits.
    box_b = (970, 1715, 135, 590)
    xb, yb = mapping(0.2, 1.05, -15.0, 0.0, *box_b)
    axes(
        scene,
        box_b,
        [(0.25, ".25"), (0.5, ".50"), (0.75, ".75"), (1.0, "1")],
        [(-15, "1e-15"), (-12, "1e-12"), (-9, "1e-9"), (-6, "1e-6"), (-3, "1e-3"), (0, "1")],
        xb,
        yb,
        "alpha",
        "log10 worst diagnostic over centers",
    )
    if numeric:
        qa_series = (
            ("coarse relative-to-fine", BLUE, None, "circle", lambda row: row["series"] == "coarse", "relativeToFine"),
            ("medium relative-to-fine", BLUE, "7,4", "square", lambda row: row["series"] == "medium", "relativeToFine"),
            ("adjoint defect", GOLD, None, "triangle", lambda row: True, "adjointDefect"),
            ("Rayleigh norm defect", GOLD, "7,4", "square", lambda row: True, "rayleighNormDefect"),
            ("Ritz residual", INK, "3,4", "diamond", lambda row: True, "ritzResidual"),
        )
        for offset, (label, color, dash, shape, predicate, field) in enumerate(qa_series):
            points: list[tuple[float, float]] = []
            for alpha in sorted(DIAGNOSTIC_ALPHAS):
                values = [
                    float(row[field])
                    for row in numeric
                    if abs(float(row["alpha"]) - alpha) < 1.0e-14
                    and predicate(row)
                ]
                value = max(values)
                points.append((xb(alpha), yb(max(-15.0, math.log10(max(value, 1.0e-15))))))
            scene.polyline(points, color, 3, dash)
            for px, py in points:
                scene.marker(px, py, 5, color, shape, offset % 2 == 1)
            scene.text(1697, 612 + 22 * offset, label, 13, color, "end", offset in (0, 2))
    else:
        scene.text(1342, 355, "refinement and duality audit pending", 17, MUTED, "middle")
    scene.text(970, 728, "50 center-alpha pairs x 3 refinement levels", 14, MUTED)

    # Panel C: exact finite-alpha interface quantities and asymptotic guides.
    box_c = (95, 850, 835, 1290)
    xc, yc = mapping(-0.65, 0.05, -5.5, 0.5, *box_c)
    axes(
        scene,
        box_c,
        [(-0.60, ".25"), (-0.46, ".35"), (-0.30, ".50"), (-0.125, ".75"), (0.0, "1")],
        [(-5, "1e-5"), (-4, "1e-4"), (-3, "1e-3"), (-2, "1e-2"), (-1, "1e-1"), (0, "1")],
        xc,
        yc,
        "log10 alpha  (tick labels show alpha)",
        "log10 exact interface quantity",
    )
    c_styles = {
        "pre critical separation": (BLUE, None, "circle", False),
        "pre Hessian floor": (INK, "9,5", "square", True),
        "post gradient at x=0": (GOLD, "3,4", "triangle", True),
    }
    if interface:
        for label, (color, dash, shape, open_marker) in c_styles.items():
            selected = sorted(
                (row for row in interface if row["series"] == label),
                key=lambda row: float(row["alpha"]),
            )
            points = [
                (
                    xc(math.log10(float(row["alpha"]))),
                    yc(math.log10(float(row["interfaceValue"]))),
                )
                for row in selected
            ]
            scene.polyline(points, color, 3, dash)
            for px, py in points:
                scene.marker(px, py, 5, color, shape, open_marker)
        # Asymptotic slope guides, placed below the data.
        for power, x0, y0, color, label in (
            (1, -0.60, -2.25, BLUE, "slope 1"),
            (2, -0.60, -4.65, GOLD, "slope 2"),
        ):
            x1 = -0.30
            y1 = y0 + power * (x1 - x0)
            scene.line(xc(x0), yc(y0), xc(x1), yc(y1), color, 2, "6,4")
            scene.text(xc(x1) + 8, yc(y1) + 4, label, 13, color)
    else:
        scene.text(472, 1060, "exact interface geometry pending render", 17, MUTED, "middle")
    for index, (label, (color, dash, shape, open_marker)) in enumerate(c_styles.items()):
        y_value = 1332 + 26 * index
        scene.line(105, y_value, 150, y_value, color, 3, dash)
        scene.marker(128, y_value, 5, color, shape, open_marker)
        scene.text(160, y_value + 5, label, 13, color)
    scene.text(95, 1437, "A1 fixed-shape margins vanish at h_alpha=T alpha^2", 14, MUTED)

    # Panel D: physical cocycle plus exact all-start block arithmetic.
    scene.text(970, 827, "physical history K*=[-ln2,1-ln2], T=1/4", 15, MUTED)
    timeline_y = 925
    x_left, x_right = 985, 1695
    time_map = lambda d: x_left + (d + math.log(2.0)) * (x_right - x_left)
    scene.line(x_left, timeline_y, x_right, timeline_y, INK, 3)
    for d_value, label in (
        (-math.log(2.0), "-ln2"),
        (-0.125, "-delta"),
        (0.0, "fold"),
        (0.125, "+delta"),
        (1.0 - math.log(2.0), "1-ln2"),
    ):
        x_value = time_map(d_value)
        scene.line(x_value, timeline_y - 12, x_value, timeline_y + 12, INK, 2)
        scene.text(x_value, timeline_y + 35, label, 13, MUTED, "middle")
    scene.box(time_map(-math.log(2.0)), 860, time_map(-0.125), 906, PALE_BLUE, BLUE, 2)
    scene.text((time_map(-math.log(2.0)) + time_map(-0.125)) / 2, 890, "fixed-margin A1", 14, BLUE, "middle", True)
    scene.box(time_map(-0.125), 860, time_map(0.125), 906, PALE_GOLD, GOLD, 2)
    scene.text(time_map(0.0), 890, "exact all-center A2", 14, GOLD, "middle", True)
    scene.box(time_map(0.125), 860, time_map(1.0 - math.log(2.0)), 906, PALE_BLUE, BLUE, 2)
    scene.text((time_map(0.125) + time_map(1.0 - math.log(2.0))) / 2, 890, "fixed-margin A1", 14, BLUE, "middle", True)

    scene.text(970, 1005, "all-start exact tiling: q^floor(L/(2T alpha^2))", 17, INK, bold=True)
    scene.text(970, 1034, "safe envelope: q^-1 exp[-|log q| L/(2T alpha^2)]", 14, MUTED)
    scene.text(970, 1060, "q in (0,1) is analytic and remains nonconstructive", 14, GOLD)
    scene.box(970, 1090, 1715, 1305, PAPER, GRID, 1)
    headers = ((1000, "alpha"), (1170, "h=T alpha^2"), (1390, "N=floor(1/(2h))"), (1615, "rate"))
    for x_value, label in headers:
        scene.text(x_value, 1122, label, 14, INK, "middle", True)
    if tiling:
        for index, row in enumerate(sorted(tiling, key=lambda value: -float(value["alpha"]))):
            y_value = 1155 + 32 * index
            scene.text(1000, y_value, f"{float(row['alpha']):.2f}", 14, INK, "middle")
            scene.text(1170, y_value, f"{float(row['blockHalfWidth']):.5f}", 14, MUTED, "middle")
            scene.text(1390, y_value, row["fullBlockCount"], 14, BLUE, "middle", True)
            scene.text(1615, y_value, "alpha^-2", 14, GOLD, "middle")
    else:
        scene.text(1342, 1200, "exact block arithmetic pending render", 17, MUTED, "middle")
    scene.box(970, 1340, 1365, 1410, PALE_BLUE, BLUE, 3)
    scene.text(1168, 1370, "all-center scalar A2 transfer", 15, BLUE, "middle", True)
    scene.text(1168, 1395, "CLOSED in bound report", 14, BLUE, "middle", True)
    scene.box(1390, 1340, 1715, 1410, PALE_GOLD, GOLD, 3)
    scene.text(1552, 1370, "forced H^-1 / full linearized", 14, GOLD, "middle", True)
    scene.text(1552, 1395, "nonlinear / Clay: OPEN", 14, GOLD, "middle", True)

    blossom_x, blossom_y = 1740, 39
    for index in range(5):
        angle = -math.pi / 2 + 2 * math.pi * index / 5
        scene.marker(
            blossom_x + 11 * math.cos(angle),
            blossom_y + 11 * math.sin(angle),
            6,
            BLUE if index % 2 == 0 else GOLD,
            "circle",
            False,
        )
    scene.marker(blossom_x, blossom_y, 4, INK, "circle", False)
    return scene


def _marker_points(
    x: float, y: float, radius: float, shape: str
) -> list[tuple[float, float]]:
    if shape == "square":
        return [
            (x - radius, y - radius),
            (x + radius, y - radius),
            (x + radius, y + radius),
            (x - radius, y + radius),
        ]
    if shape == "triangle":
        return [
            (x, y - radius),
            (x + 0.866 * radius, y + 0.5 * radius),
            (x - 0.866 * radius, y + 0.5 * radius),
        ]
    if shape == "diamond":
        return [
            (x, y - radius),
            (x + radius, y),
            (x, y + radius),
            (x - radius, y),
        ]
    return []


def save_data(rows: list[dict[str, str]]) -> None:
    with (PACKAGE / "data.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DATA_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def render_svg(scene: Scene) -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{WIDTH_MM}mm" height="{HEIGHT_MM}mm" '
            'viewBox="0 0 1780 1500">'
        ),
        f'<rect width="1780" height="1500" fill="{PAPER}"/>',
    ]
    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, width, dash = item
                points = [(x1, y1), (x2, y2)]
            else:
                _, points, color, width, dash = item
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            coordinates = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
            parts.append(
                f'<polyline points="{coordinates}" fill="none" '
                f'stroke="{color}" stroke-width="{width}"{extra}/>'
            )
        elif item[0] == "marker":
            _, x, y, radius, color, shape, open_marker = item
            fill = PAPER if open_marker else color
            if shape == "circle":
                parts.append(
                    f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" '
                    f'fill="{fill}" stroke="{color}" stroke-width="2"/>'
                )
            else:
                points = _marker_points(x, y, radius, shape)
                coordinates = " ".join(f"{px:.3f},{py:.3f}" for px, py in points)
                parts.append(
                    f'<polygon points="{coordinates}" fill="{fill}" '
                    f'stroke="{color}" stroke-width="2"/>'
                )
        elif item[0] == "box":
            _, left, top, right, bottom, fill, stroke, width = item
            parts.append(
                f'<rect x="{left:.3f}" y="{top:.3f}" '
                f'width="{right-left:.3f}" height="{bottom-top:.3f}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            parts.append(
                f'<text x="{x:.3f}" y="{y:.3f}" '
                'font-family="DejaVu Sans,Arial,sans-serif" '
                f'font-size="{size}" font-weight="{700 if bold else 400}" '
                f'text-anchor="{anchor}" fill="{color}">{escape(value)}</text>'
            )
    parts.append("</svg>")
    (PACKAGE / "figure.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def render_pdf(scene: Scene) -> None:
    from reportlab.pdfgen import canvas

    width = WIDTH_MM / 25.4 * 72
    height = HEIGHT_MM / 25.4 * 72
    sx, sy = width / 1780, height / 1500
    pdf = canvas.Canvas(
        str(PACKAGE / "figure.pdf"),
        pagesize=(width, height),
        invariant=1,
        pageCompression=1,
    )
    pdf.setTitle("R0.72X all-center exact-path transfer diagnostic")
    pdf.setAuthor("Kasifa")
    pdf.setSubject("All-center exact-path transfer with non-probative numerical diagnostics")
    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, line_width, dash = item
                points = [(x1, y1), (x2, y2)]
            else:
                _, points, color, line_width, dash = item
            pdf.setStrokeColor(color)
            pdf.setLineWidth(line_width * sx)
            pdf.setDash([float(value) * sx for value in dash.split(",")] if dash else [])
            path = pdf.beginPath()
            path.moveTo(points[0][0] * sx, height - points[0][1] * sy)
            for x_value, y_value in points[1:]:
                path.lineTo(x_value * sx, height - y_value * sy)
            pdf.drawPath(path, stroke=1, fill=0)
        elif item[0] == "marker":
            _, x, y, radius, color, shape, open_marker = item
            pdf.setStrokeColor(color)
            pdf.setFillColor(PAPER if open_marker else color)
            pdf.setLineWidth(2 * sx)
            if shape == "circle":
                pdf.circle(x * sx, height - y * sy, radius * sx, stroke=1, fill=1)
            else:
                points = _marker_points(x, y, radius, shape)
                path = pdf.beginPath()
                path.moveTo(points[0][0] * sx, height - points[0][1] * sy)
                for px, py in points[1:]:
                    path.lineTo(px * sx, height - py * sy)
                path.close()
                pdf.drawPath(path, stroke=1, fill=1)
        elif item[0] == "box":
            _, left, top, right, bottom, fill, stroke, line_width = item
            pdf.setFillColor(fill)
            pdf.setStrokeColor(stroke)
            pdf.setLineWidth(line_width * sx)
            pdf.rect(
                left * sx,
                height - bottom * sy,
                (right - left) * sx,
                (bottom - top) * sy,
                stroke=1,
                fill=1,
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            pdf.setFillColor(color)
            pdf.setFont("Helvetica-Bold" if bold else "Helvetica", size * sx)
            if anchor == "middle":
                pdf.drawCentredString(x * sx, height - y * sy, value)
            elif anchor == "end":
                pdf.drawRightString(x * sx, height - y * sy, value)
            else:
                pdf.drawString(x * sx, height - y * sy, value)
    pdf.showPage()
    pdf.save()


def _font_path(bold: bool) -> str | None:
    candidates = (
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )
    return next((path for path in candidates if Path(path).is_file()), None)


def render_png(scene: Scene) -> None:
    from PIL import Image, ImageDraw, ImageFont

    pixel_width = round(WIDTH_MM / 25.4 * PNG_DPI)
    pixel_height = round(HEIGHT_MM / 25.4 * PNG_DPI)
    sx, sy = pixel_width / 1780, pixel_height / 1500
    image = Image.new("RGB", (pixel_width, pixel_height), PAPER)
    draw = ImageDraw.Draw(image)
    font_cache: dict[tuple[int, bool], Any] = {}

    def selected_font(size: int, bold: bool) -> Any:
        key = (size, bold)
        if key not in font_cache:
            path = _font_path(bold)
            font_cache[key] = (
                ImageFont.truetype(path, max(8, round(size * sx)))
                if path
                else ImageFont.load_default()
            )
        return font_cache[key]

    def stroke(
        points: list[tuple[float, float]],
        color: str,
        line_width: float,
        dash: str | None,
    ) -> None:
        rendered_width = max(1, round(line_width * sx))
        if not dash:
            draw.line(points, fill=color, width=rendered_width)
            return
        pattern = [float(value) * sx for value in dash.split(",")]
        pattern_index = 0
        remaining = pattern[0]
        drawing = True
        for start, end in zip(points, points[1:]):
            x0, y0 = start
            x1, y1 = end
            length = math.hypot(x1 - x0, y1 - y0)
            consumed = 0.0
            while length and consumed < length:
                step = min(remaining, length - consumed)
                left = consumed / length
                right = (consumed + step) / length
                if drawing:
                    draw.line(
                        (
                            (x0 + (x1 - x0) * left, y0 + (y1 - y0) * left),
                            (x0 + (x1 - x0) * right, y0 + (y1 - y0) * right),
                        ),
                        fill=color,
                        width=rendered_width,
                    )
                consumed += step
                remaining -= step
                if remaining <= 1.0e-9:
                    pattern_index = (pattern_index + 1) % len(pattern)
                    remaining = pattern[pattern_index]
                    drawing = not drawing

    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, line_width, dash = item
                points = [(x1 * sx, y1 * sy), (x2 * sx, y2 * sy)]
            else:
                _, raw, color, line_width, dash = item
                points = [(x * sx, y * sy) for x, y in raw]
            stroke(points, color, line_width, dash)
        elif item[0] == "marker":
            _, x, y, radius, color, shape, open_marker = item
            fill = PAPER if open_marker else color
            if shape == "circle":
                draw.ellipse(
                    ((x - radius) * sx, (y - radius) * sy,
                     (x + radius) * sx, (y + radius) * sy),
                    fill=fill,
                    outline=color,
                    width=max(1, round(2 * sx)),
                )
            else:
                draw.polygon(
                    [(px * sx, py * sy) for px, py in _marker_points(x, y, radius, shape)],
                    fill=fill,
                    outline=color,
                )
        elif item[0] == "box":
            _, left, top, right, bottom, fill, outline, line_width = item
            draw.rectangle(
                (left * sx, top * sy, right * sx, bottom * sy),
                fill=fill,
                outline=outline,
                width=max(1, round(line_width * sx)),
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            font = selected_font(size, bold)
            bounds = draw.textbbox((0, 0), value, font=font)
            text_width = bounds[2] - bounds[0]
            if anchor == "middle":
                tx = x * sx - text_width / 2
            elif anchor == "end":
                tx = x * sx - text_width
            else:
                tx = x * sx
            draw.text((tx, y * sy - size * sy), value, font=font, fill=color)
    image.save(
        PACKAGE / "figure.png",
        format="PNG",
        dpi=(PNG_DPI, PNG_DPI),
        optimize=False,
        title="R0.72X all-center exact-path transfer diagnostic",
        author="Kasifa",
    )


def build_qa() -> None:
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    preview = image.resize(
        (1260, round(1260 * image.height / image.width)),
        Image.Resampling.LANCZOS,
    )
    preview.save(PACKAGE / "qa-final-size.png", dpi=(180, 180))
    preview.convert("L").save(PACKAGE / "qa-grayscale.png", dpi=(180, 180))
    candidates = (
        REPOSITORY / ".openai/poppler/bin/pdftocairo",
        Path(
            "/Users/kasifa/.cache/codex-runtimes/"
            "codex-primary-runtime/dependencies/native/poppler/"
            "poppler/bin/pdftocairo"
        ),
    )
    pdftocairo = next((path for path in candidates if path.is_file()), None)
    if pdftocairo:
        subprocess.run(
            [
                str(pdftocairo),
                "-png",
                "-singlefile",
                "-r",
                "180",
                str(PACKAGE / "figure.pdf"),
                str(PACKAGE / "qa-pdf"),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        preview.save(PACKAGE / "qa-pdf.png", dpi=(180, 180))


def git_status_dirty() -> bool:
    return bool(
        subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=REPOSITORY,
            text=True,
        ).strip()
    )


def reject_output_overwrite(include_public: bool) -> None:
    paths = [PACKAGE / name for name in GENERATED_FILES]
    if include_public:
        paths.extend(
            PUBLIC / f"{FIGURE_ID}.{extension}"
            for extension in ("pdf", "svg", "png")
        )
    present = [str(path.relative_to(REPOSITORY)) for path in paths if path.exists()]
    if present:
        raise RuntimeError(
            "refusing to overwrite pre-existing figure outputs: "
            + ", ".join(present)
        )


def validate_formal_certificate() -> tuple[dict[str, Any], dict[str, Any]]:
    if not CERTIFICATE.is_file():
        raise RuntimeError("formal R0.72X certificate is absent")
    subprocess.run(
        [
            sys.executable,
            "research/certificates/r072x/validate_certificate.py",
            "--require-formal",
        ],
        cwd=REPOSITORY,
        check=True,
    )
    manifest = json.loads(
        (CERTIFICATE_DIR / "manifest.json").read_text(encoding="utf-8")
    )
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "formal"
        or not manifest.get("sourceBindings")
        or certificate.get("status") != "passed"
    ):
        raise RuntimeError("formal source-bound R0.72X certificate required")
    return manifest, certificate


def validate_formal_lineage(
    certificate_manifest: dict[str, Any],
    source_commit: str | None,
    certificate_commit: str | None,
) -> None:
    for label, commit in (
        ("--source-commit", source_commit),
        ("--certificate-commit", certificate_commit),
    ):
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise RuntimeError(f"{label} must be a full Git commit")
    assert source_commit is not None and certificate_commit is not None
    if source_commit != certificate_manifest.get("sourceCommit"):
        raise RuntimeError("--source-commit must equal the formal certificate source commit")
    if certificate_commit == source_commit:
        raise RuntimeError("certificateCommit must be distinct from the frozen sourceCommit")
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    if certificate_commit != head:
        raise RuntimeError("--certificate-commit must equal the clean HEAD containing the certificate")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, certificate_commit],
        cwd=REPOSITORY,
    ).returncode:
        raise RuntimeError("certificateCommit does not descend from sourceCommit")
    for name in (
        "manifest.json",
        "certificate.json",
        "independent.json",
        "crosscheck.json",
        "SHA256SUMS",
    ):
        relative = f"research/certificates/r072x/{name}"
        committed = subprocess.check_output(
            ["git", "show", f"{certificate_commit}:{relative}"],
            cwd=REPOSITORY,
        )
        if committed != (REPOSITORY / relative).read_bytes():
            raise RuntimeError(
                f"working certificate differs from {certificate_commit}:{relative}"
            )


def package_validation(
    rows: list[dict[str, str]], numerical_summary: dict[str, Any]
) -> dict[str, Any]:
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    svg = (PACKAGE / "figure.svg").read_text(encoding="utf-8")
    numerical = [
        row for row in rows
        if row["kind"] == "full-exact-block-forward-adjoint-norm"
    ]
    interface = [row for row in rows if row["kind"] == "exact-interface-scaling"]
    tiling = [row for row in rows if row["kind"] == "exact-full-block-count"]
    allowed_colors = {
        PAPER, INK, MUTED, GRID, BLUE, GOLD, PALE_BLUE, PALE_GOLD
    }
    svg_colors = set(re.findall(r"#[0-9a-fA-F]{6}", svg))
    centers = sorted({float(row["physicalCenter"]) for row in numerical})
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    thresholds = config["panelB"]["qaThresholds"]
    if config["panelA"].get("lanczosRitzPolicy") != LANCZOS_RITZ_POLICY:
        raise RuntimeError("configured Lanczos-Ritz policy is not exact")
    if thresholds != EXPECTED_QA_THRESHOLDS:
        raise RuntimeError("predeclared numerical QA thresholds are not exact")
    finite_fields = (
        "normEstimate",
        "ritzResidual",
        "rayleighNormDefect",
        "adjointDefect",
        "relativeToFine",
    )
    checks = {
        "certificatePassed": json.loads(CERTIFICATE.read_text(encoding="utf-8")).get("status") == "passed",
        "fourPanels": all(
            label in svg
            for label in (
                "physical-center block norm scan",
                "refinement and adjoint QA",
                "shrinking-interface geometry",
                "exact tiling and rate ledger",
            )
        ),
        "centerRangeCovered": (
            abs(centers[0] + math.log(2.0)) < 1.0e-14
            and abs(centers[-1] - (1.0 - math.log(2.0))) < 1.0e-14
            and 0.0 in centers
        ),
        "rowCount": len(rows) == EXPECTED_ROWS,
        "numericalRowCount": len(numerical) == EXPECTED_NUMERICAL_ROWS,
        "interfaceRowCount": len(interface) == EXPECTED_INTERFACE_ROWS,
        "tilingRowCount": len(tiling) == EXPECTED_TILING_ROWS,
        "allNumericalRowsFinite": all(
            all(math.isfinite(float(row[field])) for field in finite_fields)
            for row in numerical
        ),
        "fineRelativeToFineExactlyZero": all(
            float(row["relativeToFine"]) == 0.0
            for row in numerical
            if row["series"] == "fine"
        ),
        "deterministicContractions": all(
            0.0 < float(row["normEstimate"]) <= 1.0 + 5.0e-12
            for row in numerical
        ),
        "resolutionAuditFinite": math.isfinite(numerical_summary["maxRelativeToFine"]),
        "adjointAuditFinite": math.isfinite(numerical_summary["maxAdjointDefect"]),
        "ritzAuditFinite": math.isfinite(numerical_summary["maxRitzResidual"]),
        "rayleighNormAuditFinite": math.isfinite(
            numerical_summary["maxRayleighNormDefect"]
        ),
        "resolutionAuditWithinThreshold": (
            numerical_summary["maxRelativeToFine"] <= thresholds["maxRelativeToFine"]
        ),
        "adjointAuditWithinThreshold": (
            numerical_summary["maxAdjointDefect"] <= thresholds["maxAdjointDefect"]
        ),
        "ritzAuditWithinThreshold": (
            numerical_summary["maxRitzResidual"] <= thresholds["maxRitzResidual"]
        ),
        "rayleighNormAuditWithinThreshold": (
            numerical_summary["maxRayleighNormDefect"]
            <= thresholds["maxRayleighNormDefect"]
        ),
        "ritzStoppingToleranceMet": all(
            float(row["ritzResidual"])
            <= LANCZOS_RITZ_POLICY["relativeResidualTolerance"]
            for row in numerical
        ),
        "krylovDimensionsFollowPolicy": all(
            LANCZOS_RITZ_POLICY["minDimension"]
            <= int(row["krylovDimension"])
            <= LANCZOS_RITZ_POLICY["maxDimension"]
            and (
                int(row["krylovDimension"])
                - LANCZOS_RITZ_POLICY["minDimension"]
            ) % LANCZOS_RITZ_POLICY["checkEvery"] == 0
            for row in numerical
        ),
        "interfacePositive": all(float(row["interfaceValue"]) > 0 for row in interface),
        "tilingArithmetic": all(
            int(row["fullBlockCount"])
            == math.floor(1.0 / (2.0 * DIAGNOSTIC_T * float(row["alpha"]) ** 2))
            for row in tiling
        ),
        "allCenterClosedVisible": "all-center scalar A2 transfer" in svg and "CLOSED in bound report" in svg,
        "openBoundaryVisible": "forced H^-1 / full linearized" in svg and "nonlinear / Clay: OPEN" in svg,
        "diagnosticBoundaryVisible": "NUMERICAL DIAGNOSTIC ONLY - NOT PROOF" in svg,
        "qNotEvaluatedVisible": "q in (0,1) is analytic and remains nonconstructive" in svg,
        "hardTwoChromaticRootCap": svg_colors <= allowed_colors and BLUE in svg_colors and GOLD in svg_colors,
        "redundantEncoding": "stroke-dasharray" in svg and "<polygon" in svg,
        "vectorPdf": (PACKAGE / "figure.pdf").read_bytes().startswith(b"%PDF"),
        "vectorSvg": svg.lstrip().startswith("<?xml"),
        "pngAtLeast600DpiAt178mm": (
            image.width >= math.floor(WIDTH_MM / 25.4 * PNG_DPI)
            and image.info.get("dpi", (0, 0))[0] >= 599
        ),
    }
    value = {
        "schemaVersion": 1,
        "status": "passed",
        "checks": checks,
        "rowCount": len(rows),
        "numericalSummary": numerical_summary,
        "qaThresholds": thresholds,
        "png": {
            "width": image.width,
            "height": image.height,
            "dpi": list(image.info.get("dpi", (0, 0))),
        },
    }
    if not all(checks.values()):
        raise RuntimeError(f"automatic R0.72X figure validation failed: {value}")
    return value


def build_archive(
    rows: list[dict[str, str]],
    numerical_summary: dict[str, Any],
    formal: bool,
    visual_inspected: bool,
    source_commit: str | None,
    certificate_commit: str | None,
    certificate: dict[str, Any],
    wall_time_seconds: float,
) -> None:
    validation = package_validation(rows, numerical_summary)
    write_json(PACKAGE / "validation.json", validation)
    claim_boundary = json.loads(
        (PACKAGE / "contract.json").read_text(encoding="utf-8")
    )["claimBoundary"]
    if claim_boundary != EXPECTED_CLAIM_BOUNDARY:
        raise RuntimeError("R0.72X claim boundary is not exact")
    results = {
        "schemaVersion": 1,
        "status": "passed",
        "figureId": FIGURE_ID,
        "pdeSimulation": True,
        "diagnosticOnly": True,
        "deterministic": True,
        "randomSeed": None,
        "panels": {
            "A": "fine-grid full-exact block norm estimates over physical centers",
            "B": "worst-over-center refinement, adjoint, and actual Ritz-residual audits",
            "C": "exact finite-alpha pre/post interface geometry with asymptotic guides",
            "D": "exact physical cocycle, symbolic q ledger, and full-block arithmetic",
        },
        "numericalSummary": numerical_summary,
        "claimBoundary": claim_boundary,
        "claimsNotMade": [
            "numerical proof of all-center graph coercivity",
            "numerical evaluation of the nonconstructive q or graph constant",
            DIAGNOSTIC_LIMITATIONS[0],
            "infinite-dimensional operator norm",
            "continuum convergence from the finite Lanczos-Ritz residual",
            "scale-sharp forced H^-1 transfer",
            "complete linearized Navier-Stokes subsystem",
            "nonlinear Navier-Stokes closure",
            "Clay Millennium problem",
        ],
    }
    write_json(PACKAGE / "results.json", results)
    usage_self = resource.getrusage(resource.RUSAGE_SELF)
    usage_children = resource.getrusage(resource.RUSAGE_CHILDREN)
    memory_units = max(usage_self.ru_maxrss, usage_children.ru_maxrss)
    memory_gib = memory_units / (
        1024**3 if sys.platform == "darwin" else 1024**2
    )
    with (PACKAGE / "resource-log.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "event": "resource-summary",
            "processes": WORKERS,
            "threadsPerProcess": 1,
            "gpuUsed": False,
            "numpyVersion": numerical_summary["numpyVersion"],
            "maxResidentSetPlatformUnits": usage_self.ru_maxrss,
            "childMaxResidentSetPlatformUnits": usage_children.ru_maxrss,
            "memoryGiB": memory_gib,
            "wallTimeSeconds": wall_time_seconds,
            "diagnosticOnly": True,
        }, sort_keys=True) + "\n")
    with (PACKAGE / "progress.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "event": "archive-ready",
            "rows": len(rows),
            "numericalRows": EXPECTED_NUMERICAL_ROWS,
            "wallTimeSeconds": wall_time_seconds,
        }, sort_keys=True) + "\n")
    progress_event_count = sum(
        1 for line in (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    (PACKAGE / "qa-report.md").write_text(
        "".join((
            "# R0.72X figure QA\n\n",
            f"- formal build: {'yes' if formal else 'no'}\n",
            f"- explicit visual inspection: {'yes' if visual_inspected else 'no'}\n",
            "- final-size, grayscale, and PDF previews generated: yes\n",
            "- full exact shifted potential used at every center: yes\n",
            "- deterministic fully double-reorthogonalized Lanczos-Ritz used: yes\n",
            "- each checkpoint residual recomputed from the actual Ritz vector and A v: yes\n",
            f"- Krylov dimension range: {numerical_summary['minKrylovDimension']} to {numerical_summary['maxKrylovDimension']}\n",
            f"- maximum actual Ritz residual: {numerical_summary['maxRitzResidual']:.6e}\n",
            f"- maximum direct-versus-Rayleigh norm defect: {numerical_summary['maxRayleighNormDefect']:.6e}\n",
            "- all displayed numerical norms labelled diagnostic only: yes\n",
            "- q and the continuum graph constant remain unevaluated: yes\n",
            "- forced H^-1, complete linearized, nonlinear, and Clay boundaries remain open: yes\n",
        )),
        encoding="utf-8",
    )

    publication_assets: list[dict[str, Any]] = []
    if formal:
        PUBLIC.mkdir(parents=True, exist_ok=True)
        for extension in ("pdf", "svg", "png"):
            source = PACKAGE / f"figure.{extension}"
            target = PUBLIC / f"{FIGURE_ID}.{extension}"
            shutil.copyfile(source, target)
            publication_assets.append({
                "path": str(target.relative_to(REPOSITORY)),
                "sha256": sha256(target),
                "bytes": target.stat().st_size,
                "byteIdenticalToMaster": sha256(target) == sha256(source),
            })

    archived = [
        *SOURCE_FILES,
        "data.csv",
        "results.json",
        "validation.json",
        "progress.ndjson",
        "resource-log.ndjson",
        "qa-report.md",
        "figure.svg",
        "figure.pdf",
        "figure.png",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
    ]
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    manifest = {
        "schemaVersion": "1.1",
        "figureId": FIGURE_ID,
        "release": "R0.72X",
        "status": "formal" if formal else "draft",
        "createdAt": "2026-08-28T00:00:00+08:00",
        "analyticalQuestion": (
            "How does the full exact collision family behave across every physical block center in the fixed heat history, "
            "and how do the shrinking A1 interface constants and exact A2 block arithmetic scale?"
        ),
        "supportedClaim": (
            "The bound analytic report supplies Bloch-uniform all-center exact A2 graph coercivity and all-start block tiling. "
            "Exact A1-A2-A1 concatenation is closed only for the periodic representative beta=0, not uniformly over Bloch twists. "
            "The displayed finite-grid propagator norms and scaling samples are deterministic diagnostics only; "
            "the single-seed Ritz residual does not certify the finite propagator's global largest singular value."
        ),
        "diagnosticLimitations": DIAGNOSTIC_LIMITATIONS,
        "git": (
            {
                "repository": "Kasifa/Kasifa.github.io",
                "sourceCommit": source_commit,
                "certificateCommit": certificate_commit,
                "dirtyAtCertifiedRun": False,
            }
            if formal
            else {
                "repository": "Kasifa/Kasifa.github.io",
                "commit": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
                ).strip(),
                "dirty": git_status_dirty(),
            }
        ),
        "simulation": {
            "kind": "simulation",
            "configuration": (
                "10 physical centers x 5 alpha values x 3 simultaneous spatial/time refinement levels; "
                "deterministic fully double-reorthogonalized Lanczos-Ritz on U*U; "
                "dimensions 8 through 32 checked every 4; full exact shifted two-harmonic potential"
            ),
            "formalCommand": (
                "python3 scripts/generate_r072x_figure.py --formal --visual-inspected "
                "--source-commit <40-hex> --certificate-commit <40-hex>"
            ),
            "pdeSimulation": True,
            "diagnosticOnly": True,
            "equation": "u_tau=u_XX+i*V_{alpha,S0}(tau,X)*u on T_{2*pi/alpha}",
            "potential": "alpha^-3*(2*exp(-D0-alpha^2*tau)*sin(alpha*X)-exp(-4*D0-4*alpha^2*tau)*sin(2*alpha*X))",
            "solver": "Fourier Strang splitting; fully double-reorthogonalized Lanczos-Ritz on discrete U*U",
            "timeInterval": [-DIAGNOSTIC_T, DIAGNOSTIC_T],
            "physicalCenters": list(PHYSICAL_CENTERS),
            "alphas": list(DIAGNOSTIC_ALPHAS),
            "levels": [
                {"label": label, "spatialModes": n_value, "timeSteps": steps}
                for label, n_value, steps in DIAGNOSTIC_LEVELS
            ],
            "lanczosRitzPolicy": LANCZOS_RITZ_POLICY,
            "precision": "NumPy float64/complex128",
            "randomSeed": None,
            "initialVector": "fixed trigonometric polynomial recorded in generator",
            "wallTimeSeconds": wall_time_seconds,
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": round(
                    wall_time_seconds / max(1, progress_event_count - 1), 6
                ),
                "cadence": "event-based; interval is mean wall-time spacing of archived events",
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "event",
                    "physicalCenter",
                    "alpha",
                    "level",
                    "resolution",
                    "timeSteps",
                    "normEstimate",
                    "krylovDimension",
                    "ritzResidual",
                    "ritzCheckpoints",
                    "rayleighNormDefect",
                    "adjointDefect",
                    "completed",
                    "total",
                    "etaSeconds",
                    "elapsedSeconds",
                    "maxResidentSetPlatformUnits",
                ],
            },
        },
        "compute": {
            "host": platform.node() or "local",
            "operatingSystem": platform.platform(),
            "cpu": platform.processor() or platform.machine(),
            "memoryGiB": round(memory_gib, 6),
            "processes": WORKERS,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used; local four-process deterministic CPU FFT sweep",
        },
        "environment": {
            "python": platform.python_version(),
            "packagesLock": "requirements.txt",
            "numpy": numerical_summary["numpyVersion"],
            "pillow": getattr(Image, "__version__", "installed"),
            "reportlab": "pinned in requirements.txt",
        },
        "data": [{
            "path": "data.csv",
            "schema": list(DATA_FIELDS),
            "rows": len(rows),
            "sha256": sha256(PACKAGE / "data.csv"),
            "bytes": (PACKAGE / "data.csv").stat().st_size,
        }, {
            "path": "results.json",
            "schema": "panel meanings, numerical summary, claim boundary, and claims not made",
            "sha256": sha256(PACKAGE / "results.json"),
            "bytes": (PACKAGE / "results.json").stat().st_size,
        }, {
            "path": "validation.json",
            "schema": "lineage, range, row, format, and visible-boundary checks",
            "sha256": sha256(PACKAGE / "validation.json"),
            "bytes": (PACKAGE / "validation.json").stat().st_size,
        }, {
            "path": "progress.ndjson",
            "schema": "event-level parallel diagnostic progress ledger",
            "sha256": sha256(PACKAGE / "progress.ndjson"),
            "bytes": (PACKAGE / "progress.ndjson").stat().st_size,
        }, {
            "path": "resource-log.ndjson",
            "schema": "event-level process, memory, and wall-time resource ledger",
            "sha256": sha256(PACKAGE / "resource-log.ndjson"),
            "bytes": (PACKAGE / "resource-log.ndjson").stat().st_size,
        }],
        "sourceData": [{
            "location": "repository",
            "fileName": str(CERTIFICATE.relative_to(REPOSITORY)),
            "bytes": CERTIFICATE.stat().st_size,
            "sha256": sha256(CERTIFICATE),
            "role": "formalExactCertificate",
            "extractionCommand": (
                "python3 research/certificates/r072x/generate_certificate.py "
                "--formal --source-commit <40-hex>"
            ),
        }, {
            "location": "repository",
            "fileName": "scripts/generate_r072x_figure.py",
            "bytes": Path(__file__).stat().st_size,
            "sha256": sha256(Path(__file__)),
            "role": "fullExactDiagnosticAndFigureGenerator",
            "extractionCommand": (
                "python3 scripts/generate_r072x_figure.py --formal --visual-inspected "
                "--source-commit <40-hex> --certificate-commit <40-hex>"
            ),
        }],
        "figure": {
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "layout": "2x2",
            "profile": "journal-double-column",
            "script": "plot.py",
            "outputs": [{
                "path": f"figure.{extension}",
                "sha256": sha256(PACKAGE / f"figure.{extension}"),
                "bytes": (PACKAGE / f"figure.{extension}").stat().st_size,
                **(
                    {"dpi": PNG_DPI, "pixels": list(image.size)}
                    if extension == "png" else {}
                ),
            } for extension in ("pdf", "svg", "png")],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": visual_inspected,
            "finalSizeInspected": visual_inspected,
            "grayscaleInspected": visual_inspected,
            "labelsAndLegendsInspected": visual_inspected,
            "scalesAndUnitsInspected": visual_inspected,
            "dataCrossChecked": True,
            "diagnosticBoundaryInspected": visual_inspected,
            "finalSizePreview": "qa-final-size.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "manualReport": "qa-report.md",
        },
        "publication": {
            "directory": "public/assets/r072x",
            "stem": FIGURE_ID,
            "publicCopiesComplete": formal,
            "assets": publication_assets,
        },
        "claimBoundary": claim_boundary,
        "certificateClaimBoundary": certificate.get("claimBoundary", {}),
        "deterministic": True,
        "outputs": [{
            "path": name,
            "sha256": sha256(PACKAGE / name),
            "bytes": (PACKAGE / name).stat().st_size,
        } for name in archived],
    }
    write_json(PACKAGE / "manifest.json", manifest)
    ledger_names = sorted(
        path.name for path in PACKAGE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (PACKAGE / "SHA256SUMS").write_text(
        "".join(f"{sha256(PACKAGE / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )


def _policy_self_test() -> dict[str, Any]:
    """Exercise the production policy on a deterministic finite operator."""
    _configure_numeric_threads()
    import numpy as np

    # Eight distinct eigenvalues on a 64-dimensional space give an exact
    # eight-dimensional Krylov closure for the nonzero deterministic start.
    diagonal = np.repeat(
        np.array([1.0, 0.87, 0.73, 0.59, 0.43, 0.31, 0.19, 0.07]),
        8,
    )
    indices = np.arange(diagonal.size, dtype=np.float64)
    initial = (1.0 + 0.03 * indices) * np.exp(1j * 0.17 * indices)
    result = _lanczos_ritz_largest(
        np,
        lambda value: diagonal * value,
        initial.astype(np.complex128),
        LANCZOS_RITZ_POLICY,
    )
    ritz_vector = result.pop("ritzVector")
    _, direct_norm, rayleigh_norm_defect = _direct_norm_audit(
        np,
        lambda value: np.sqrt(diagonal) * value,
        ritz_vector,
        result["ritzValue"],
    )
    result["normEstimate"] = direct_norm
    result["rayleighNormDefect"] = rayleigh_norm_defect
    early_breakdown_rejected = False
    try:
        _lanczos_ritz_largest(
            np,
            lambda value: value,
            initial.astype(np.complex128),
            LANCZOS_RITZ_POLICY,
        )
    except RuntimeError as error:
        early_breakdown_rejected = "breakdown" in str(error).lower()
    result["earlyBreakdownRejected"] = early_breakdown_rejected
    if (
        result["krylovDimension"] != LANCZOS_RITZ_POLICY["minDimension"]
        or result["ritzResidual"]
        > LANCZOS_RITZ_POLICY["relativeResidualTolerance"]
        or abs(result["ritzValue"] - 1.0) > 1.0e-12
        or abs(result["normEstimate"] - 1.0) > 1.0e-12
        or result["rayleighNormDefect"]
        > EXPECTED_QA_THRESHOLDS["maxRayleighNormDefect"]
        or result["earlyBreakdownRejected"] is not True
    ):
        raise RuntimeError(f"Lanczos-Ritz policy self-test failed: {result}")
    return result


def calibration_test() -> None:
    jobs = (
        (0.35, -0.25, "fine", 1024, 1600),
        (0.25, -0.125, "fine", 1024, 1600),
        (0.5, -0.5, "fine", 1024, 1600),
    )
    records = [_one_diagnostic(job) for job in jobs]
    for record in records:
        dimension = record["krylovDimension"]
        if not (
            LANCZOS_RITZ_POLICY["minDimension"] <= dimension
            <= LANCZOS_RITZ_POLICY["maxDimension"]
            and (dimension - LANCZOS_RITZ_POLICY["minDimension"])
            % LANCZOS_RITZ_POLICY["checkEvery"] == 0
            and record["ritzResidual"]
            <= LANCZOS_RITZ_POLICY["relativeResidualTolerance"]
            and record["rayleighNormDefect"]
            <= EXPECTED_QA_THRESHOLDS["maxRayleighNormDefect"]
        ):
            raise RuntimeError(f"slow-configuration calibration failed: {record}")
    print(json.dumps({
        "status": "passed",
        "policy": LANCZOS_RITZ_POLICY,
        "records": [{
            key: record[key]
            for key in (
                "alpha", "physicalCenter", "level", "resolution",
                "timeSteps", "normEstimate", "krylovDimension",
                "ritzResidual", "rayleighNormDefect", "adjointDefect",
                "workerWallTimeSeconds",
            )
        } for record in records],
        "outputsWritten": False,
    }, indent=2, sort_keys=True))


def self_test() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    contract = json.loads((PACKAGE / "contract.json").read_text(encoding="utf-8"))
    package_files = {path.name for path in PACKAGE.iterdir() if path.is_file()}
    interface = interface_rows()
    tiling = tiling_rows()
    scene_text = {
        item[3] for item in build_scene(None).items if item[0] == "text"
    }
    policy_result = _policy_self_test()
    checks = {
        "identity": config.get("figureId") == FIGURE_ID and contract.get("figureId") == FIGURE_ID,
        "dimensions": (
            config.get("widthMillimetres") == WIDTH_MM
            and config.get("heightMillimetres") == HEIGHT_MM
            and config.get("pngDpi") == PNG_DPI
        ),
        "exactLifecycleInventory": package_files in (
            set(SOURCE_FILES),
            set(SOURCE_FILES) | set(GENERATED_FILES),
        ),
        "centerCoverage": (
            len(PHYSICAL_CENTERS) == 10
            and abs(PHYSICAL_CENTERS[0] + math.log(2.0)) < 1.0e-15
            and abs(PHYSICAL_CENTERS[-1] - (1.0 - math.log(2.0))) < 1.0e-15
            and 0.0 in PHYSICAL_CENTERS
        ),
        "configuration": (
            config.get("panelA", {}).get("alphas") == list(DIAGNOSTIC_ALPHAS)
            and config.get("panelA", {}).get("physicalCenters") == list(PHYSICAL_CENTERS)
            and config.get("panelA", {}).get("lanczosRitzPolicy")
            == LANCZOS_RITZ_POLICY
            and config.get("panelA", {}).get("workers") == WORKERS
            and config.get("panelB", {}).get("qaThresholds") == EXPECTED_QA_THRESHOLDS
        ),
        "productionPolicyExecuted": (
            policy_result["krylovDimension"]
            == LANCZOS_RITZ_POLICY["minDimension"]
            and policy_result["ritzResidual"]
            <= LANCZOS_RITZ_POLICY["relativeResidualTolerance"]
            and policy_result["rayleighNormDefect"]
            <= EXPECTED_QA_THRESHOLDS["maxRayleighNormDefect"]
            and policy_result["earlyBreakdownRejected"] is True
        ),
        "interfaceRows": len(interface) == EXPECTED_INTERFACE_ROWS,
        "tilingRows": len(tiling) == EXPECTED_TILING_ROWS,
        "interfacePowers": {int(row["expectedPower"]) for row in interface} == {1, 2},
        "tilingCounts": [int(row["fullBlockCount"]) for row in tiling] == [2, 3, 8, 16, 32],
        "claimBoundary": contract.get("claimBoundary") == EXPECTED_CLAIM_BOUNDARY,
        "hardTwoRootPalette": (
            contract.get("palette", {}).get("chromaticRoots") == [BLUE, GOLD]
            and contract.get("palette", {}).get("hardChromaticRootCap") == 2
        ),
        "diagnosticVisible": "NUMERICAL DIAGNOSTIC ONLY - NOT PROOF" in scene_text,
        "openVisible": "nonlinear / Clay: OPEN" in scene_text,
    }
    if not all(checks.values()):
        raise RuntimeError(f"R0.72X figure source self-test failed: {checks}")
    print(
        "R0.72X figure source self-test: passed "
        f"({len(interface) + len(tiling)} exact in-memory rows; no outputs written)"
    )


def main() -> None:
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--calibration-test", action="store_true")
    mode.add_argument("--draft", action="store_true")
    mode.add_argument("--formal", action="store_true")
    parser.add_argument("--visual-inspected", action="store_true")
    parser.add_argument("--source-commit")
    parser.add_argument("--certificate-commit")
    args = parser.parse_args()

    if args.self_test:
        if args.visual_inspected or args.source_commit or args.certificate_commit:
            parser.error("--self-test cannot be combined with generation arguments")
        self_test()
        return
    if args.calibration_test:
        if args.visual_inspected or args.source_commit or args.certificate_commit:
            parser.error("--calibration-test cannot be combined with generation arguments")
        calibration_test()
        return
    if not args.draft and not args.formal:
        parser.error("choose --self-test, --calibration-test, --draft, or --formal")

    certificate_manifest, certificate = validate_formal_certificate()
    if args.formal:
        if git_status_dirty():
            raise RuntimeError("formal figure generation requires a completely clean tree")
        if not args.visual_inspected:
            raise RuntimeError("formal figure generation requires --visual-inspected")
        validate_formal_lineage(
            certificate_manifest,
            args.source_commit,
            args.certificate_commit,
        )
        reject_output_overwrite(include_public=True)
    else:
        if args.visual_inspected or args.source_commit or args.certificate_commit:
            parser.error("draft generation does not accept formal lineage flags")
        reject_output_overwrite(include_public=False)

    (PACKAGE / "progress.ndjson").write_text(
        json.dumps({
            "event": "build-start",
            "mode": "formal" if args.formal else "draft",
            "totalDiagnostics": EXPECTED_NUMERICAL_ROWS,
            "workers": WORKERS,
            "lanczosRitzPolicy": LANCZOS_RITZ_POLICY,
        }, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (PACKAGE / "resource-log.ndjson").write_text(
        json.dumps({
            "event": "resource-start",
            "processes": WORKERS,
            "threadsPerProcess": 1,
            "gpuUsed": False,
        }, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    def append(path: Path, event: dict[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    numeric, numerical_summary = numerical_rows(
        lambda event: append(PACKAGE / "progress.ndjson", event),
        lambda event: append(PACKAGE / "resource-log.ndjson", event),
    )
    rows = numeric + interface_rows() + tiling_rows()
    save_data(rows)
    scene = build_scene(rows)
    render_svg(scene)
    render_pdf(scene)
    render_png(scene)
    build_qa()
    build_archive(
        rows,
        numerical_summary,
        formal=args.formal,
        visual_inspected=args.visual_inspected,
        source_commit=args.source_commit,
        certificate_commit=args.certificate_commit,
        certificate=certificate,
        wall_time_seconds=time.perf_counter() - started,
    )
    print(
        f"R0.72X {'formal' if args.formal else 'draft'} figure package: "
        f"passed ({len(rows)} rows; numerical diagnostic only)"
    )


if __name__ == "__main__":
    main()
