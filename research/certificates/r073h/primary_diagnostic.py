#!/usr/bin/env python3
"""R0.73H finite harmonic-resolved amplitude/Duhamel diagnostic.

The producer uses generic physical-velocity Fourier convolution followed by
modewise Leray projection.  Every numerical output is a finite binary64
Galerkin diagnostic.  Exact Kz parity is checked, but no cutoff comparison is
treated as a continuum tail estimate.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
from typing import Any, Iterable, Mapping
import zipfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "research/certificates/r073h/README.md",
    "research/certificates/r073h/command.txt",
    "research/certificates/r073h/config.json",
    "research/certificates/r073h/requirements.txt",
    "research/certificates/r073h/exact_q2_certificate.py",
    "research/certificates/r073h/independent_exact_q2.py",
    "research/certificates/r073h/primary_diagnostic.py",
    "research/certificates/r073h/independent_validate.py",
    "research/certificates/r073h/generate_certificate.py",
    "research/certificates/r073h/validate_certificate.py",
    "research/certificates/r073h/seal_package.py",
)
SCHEMA_VERSION = "r073h-harmonic-duhamel-primary-v1"
EVIDENCE_CLASS = "finite-binary64-galerkin-diagnostic-only"
GAMMA = 0.5
MU = 0.25
KZ_MAX = 3

ROW_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "gridKind", "archivePrefix", "N", "dimensionPerKz", "viscousEpsilon",
    "absoluteLambda", "profileTime", "fastTime", "fastStep",
    "topEigenvalueFastReal", "topEigenvalueFastImag", "topClusterDimension",
    "topRealGap", "topEigenResidualRelative", "generatorRelativeDefect",
    "unitRealLaunchL2", "v1L2", "v1PositiveKzL2", "v2MeanL2",
    "v2DoublePairL2", "v2L2", "v3MeanPathTargetL2",
    "v3DoublePathTargetL2", "v3TargetPairL2", "v3TriplePairL2", "v3L2",
    "quadraticNaturalResponse", "targetCubicNaturalResponse",
    "tripleCubicNaturalResponse", "quadraticCompensated",
    "targetCubicCompensated", "tripleCubicCompensated",
    "meanPathSignedNaturalParallel", "doublePathSignedNaturalParallel",
    "totalSignedNaturalParallel", "meanPathSignedCompensated",
    "doublePathSignedCompensated", "totalSignedCompensated",
    "meanPathCosineWithLinear", "doublePathCosineWithLinear",
    "totalCubicCosineWithLinear", "v1OuterThreeMassFraction",
    "v2OuterThreeMassFraction", "v3OuterThreeMassFraction",
    "maximumDivergenceRelative", "maximumRealityRelative",
    "forbiddenParityRelative", "caseChecksPass",
)

CONVERGENCE_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "viscousEpsilon",
    "absoluteLambda", "coarseN", "fineN", "linearGainRelativeChange",
    "quadraticNaturalRelativeChange", "targetCubicNaturalRelativeChange",
    "tripleCubicNaturalRelativeChange", "signedCubicRelativeChange",
    "maximumRelativeChange", "finestCutoffGateApplied", "passCheck",
    "ordinaryCutoffAgreementIsTailProof",
)

STEP_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "N",
    "viscousEpsilon", "absoluteLambda", "coarseFastStep", "fineFastStep",
    "linearGainRelativeChange", "quadraticNaturalRelativeChange",
    "targetCubicNaturalRelativeChange", "tripleCubicNaturalRelativeChange",
    "signedCubicRelativeChange", "maximumRelativeChange", "passCheck",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.linalg import eig  # noqa: E402


START = time.perf_counter()
SEQUENCE = 0
PROGRESS: Path | None = None


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def atomic_text(path: Path, text: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def emit(event: str, **fields: object) -> None:
    global SEQUENCE
    SEQUENCE += 1
    row = {
        "sequence": SEQUENCE,
        "timestampUtc": now_utc(),
        "elapsedSeconds": round(time.perf_counter() - START, 6),
        "event": event,
        **fields,
    }
    line = json.dumps(row, sort_keys=True, allow_nan=False)
    print(line, flush=True)
    if PROGRESS is not None:
        with PROGRESS.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")


def strict_source_gate(source_commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("formal run requires a full lowercase 40-character source commit")
    resolved = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{source_commit}^{{commit}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if resolved != source_commit:
        raise RuntimeError("source commit did not resolve exactly as a commit object")
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    ancestor = subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", source_commit, head],
        check=False,
    ).returncode == 0
    if not ancestor:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        committed = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{source_commit}:{relative}"],
            check=True, capture_output=True,
        ).stdout
        working = path.read_bytes()
        if committed != working:
            raise RuntimeError(f"working source differs from source commit: {relative}")
        mode = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", source_commit, relative],
            check=True, capture_output=True, text=True,
        ).stdout.split()[0]
        if mode != "100644" and mode != "100755":
            raise RuntimeError(f"source is not a regular Git blob: {relative}")
        bindings.append({
            "path": relative,
            "bytes": len(working),
            "sha256": hashlib.sha256(working).hexdigest(),
            "gitMode": mode,
        })
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtRun": head,
        "sourceCommitIsAncestorOfHead": ancestor,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def validate_config(config: Mapping[str, object]) -> None:
    required = {
        "schemaVersion", "release", "evidenceClass", "diagnosticOnly",
        "pilotInformed", "normalization", "formalGrid", "stepConvergence",
        "independentSentinels", "holdout", "fitWindowViscousEpsilons",
        "tolerances", "claimBoundary",
    }
    if set(config) != required:
        raise ValueError("configuration top-level keys are not exact")
    if config["schemaVersion"] != "r073h-harmonic-duhamel-config-v1":
        raise ValueError("unexpected configuration schema")
    if config["release"] != "R0.73H" or config["diagnosticOnly"] is not True:
        raise ValueError("configuration release/evidence mode is invalid")
    grid = config["formalGrid"]
    assert isinstance(grid, dict)
    cutoffs = list(grid["cutoffs"])
    epsilons = list(grid["viscousEpsilons"])
    snapshots = list(grid["profileTimeSnapshots"])
    if cutoffs != [24, 32, 48, 64]:
        raise ValueError("formal cutoff grid changed")
    if epsilons != [0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001]:
        raise ValueError("formal epsilonNu grid changed")
    expected_snapshots = [index / 1000.0 for index in range(11)]
    if snapshots != expected_snapshots:
        raise ValueError("formal profile-time snapshots changed")
    if float(grid["primaryFastStep"]) != 0.05:
        raise ValueError("formal primary fast step changed")
    if any(not math.isfinite(float(value)) for value in epsilons + snapshots):
        raise ValueError("nonfinite formal grid value")


def smoke_config(config: dict[str, object]) -> dict[str, object]:
    copied = json.loads(json.dumps(config))
    copied["formalGrid"] = {
        "cutoffs": [6, 8],
        "viscousEpsilons": [0.01, 0.005],
        "profileTimeSnapshots": [0.0, 0.001],
        "primaryFastStep": 0.2,
    }
    copied["stepConvergence"] = {
        "cutoff": 8,
        "viscousEpsilons": [0.01],
        "fastSteps": [0.4, 0.2, 0.1],
    }
    copied["holdout"] = {
        "cutoff": 8,
        "viscousEpsilon": 0.002,
        "fastStep": 0.1,
        "notUsedToFitPilotScaling": True,
        "predictions": copied["holdout"]["predictions"],
    }
    copied["fitWindowViscousEpsilons"] = [0.01, 0.005]
    return copied


def frozen_kinetic_matrix(n_cut: int, epsilon_nu: float) -> np.ndarray:
    raw = np.zeros((2 * n_cut + 1, 2 * n_cut + 1), dtype=np.complex128)
    for column, n_mode in enumerate(range(-n_cut, n_cut + 1)):
        lam = n_mode * n_mode + MU
        first = GAMMA * 0.25 * (1.0 - 1.0 / lam)
        second = GAMMA * (-0.125 + 0.5 / lam)
        for shift, value in ((1, first), (-1, -first), (2, second), (-2, -second)):
            output = n_mode + shift
            if -n_cut <= output <= n_cut:
                raw[output + n_cut, column] = value
    modes = np.arange(-n_cut, n_cut + 1, dtype=float)
    lam = modes * modes + MU
    transformed = (1.0 / np.sqrt(lam))[:, None] * raw * np.sqrt(lam)[None, :]
    transformed -= epsilon_nu * np.diag(lam)
    return transformed


def canonical_top(matrix: np.ndarray) -> tuple[complex, np.ndarray, dict[str, object]]:
    values, vectors = eig(matrix, left=False, right=True, check_finite=False)
    top_real = float(np.max(values.real))
    indices = np.flatnonzero(values.real >= top_real - 1.0e-8)
    selected = max(
        (int(index) for index in indices),
        key=lambda index: (float(values[index].real), float(values[index].imag)),
    )
    value = complex(values[selected])
    vector = np.asarray(vectors[:, selected], dtype=np.complex128)
    vector /= np.linalg.norm(vector)
    anchor = int(np.argmax(np.abs(vector)))
    vector *= np.exp(-1j * np.angle(vector[anchor]))
    if vector[anchor].real < 0.0:
        vector *= -1.0
    scale = max(1.0, float(np.linalg.norm(matrix)), abs(value))
    residual = float(np.linalg.norm(matrix @ vector - value * vector) / scale)
    complement = np.delete(values, indices)
    gap = top_real - float(np.max(complement.real)) if len(complement) else math.inf
    return value, vector, {
        "topClusterDimension": int(len(indices)),
        "topRealGap": float(gap),
        "topEigenResidualRelative": residual,
    }


class FourierVelocity:
    def __init__(self, n_cut: int):
        self.n_cut = n_cut
        self.n = np.arange(-n_cut, n_cut + 1, dtype=int)
        self.ky = 2.0 * self.n
        self.kz = np.arange(-KZ_MAX, KZ_MAX + 1, dtype=int)

    def zeros(self) -> np.ndarray:
        return np.zeros((len(self.kz), len(self.n), 2), dtype=np.complex128)

    def background(self, absolute_lambda: float, d: float) -> np.ndarray:
        result = self.zeros()
        center = KZ_MAX
        coefficients = {
            1: 0.5j * absolute_lambda * math.exp(-d),
            -1: -0.5j * absolute_lambda * math.exp(-d),
            2: -0.25j * absolute_lambda * math.exp(-4.0 * d),
            -2: 0.25j * absolute_lambda * math.exp(-4.0 * d),
        }
        for n_mode, value in coefficients.items():
            if -self.n_cut <= n_mode <= self.n_cut:
                result[center, n_mode + self.n_cut, 1] = value
        return result

    def project(self, field: np.ndarray) -> np.ndarray:
        output = np.asarray(field, dtype=np.complex128).copy()
        for index, kz in enumerate(self.kz):
            wave_squared = self.ky * self.ky + float(kz * kz)
            nonzero = wave_squared > 0.0
            dot = self.ky * output[index, :, 0] + float(kz) * output[index, :, 1]
            output[index, nonzero, 0] -= self.ky[nonzero] * dot[nonzero] / wave_squared[nonzero]
            output[index, nonzero, 1] -= float(kz) * dot[nonzero] / wave_squared[nonzero]
        return output

    def bilinear(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """Galerkin slice of P[(left dot grad)right] by exact coefficient convolution."""
        raw = self.zeros()
        length = len(self.n)
        start = self.n_cut
        stop = start + length
        weighted_y = right * self.ky[None, :, None]
        for left_index, left_kz in enumerate(self.kz):
            if not np.any(left[left_index]):
                continue
            for right_index, right_kz in enumerate(self.kz):
                output_kz = int(left_kz + right_kz)
                if abs(output_kz) > KZ_MAX or not np.any(right[right_index]):
                    continue
                output_index = output_kz + KZ_MAX
                for component in range(2):
                    convolution = np.convolve(
                        left[left_index, :, 0], weighted_y[right_index, :, component]
                    )
                    convolution += float(right_kz) * np.convolve(
                        left[left_index, :, 1], right[right_index, :, component]
                    )
                    raw[output_index, :, component] += 1j * convolution[start:stop]
        return self.project(raw)

    def linear(self, field: np.ndarray, absolute_lambda: float, d: float) -> np.ndarray:
        background = self.background(absolute_lambda, d)
        laplacian = -(self.ky[None, :] ** 2 + self.kz[:, None] ** 2)
        return (
            laplacian[:, :, None] * field
            - self.bilinear(background, field)
            - self.bilinear(field, background)
        )

    def unit_real_launch(self, kinetic: np.ndarray) -> np.ndarray:
        profile = kinetic / (2.0 * np.sqrt(self.n.astype(float) ** 2 + MU))
        result = self.zeros()
        plus = KZ_MAX + 1
        minus = KZ_MAX - 1
        result[plus, :, 0] = profile
        result[plus, :, 1] = -2.0 * self.n * profile
        for index, n_mode in enumerate(self.n):
            reflected = -n_mode + self.n_cut
            result[minus, reflected] = np.conjugate(result[plus, index])
        result /= math.sqrt(2.0)
        return result

    def l2(self, field: np.ndarray) -> float:
        return math.sqrt(max(0.0, float(np.vdot(field, field).real)))

    def kz_pair(self, field: np.ndarray, values: Iterable[int]) -> np.ndarray:
        indices = [value + KZ_MAX for value in values]
        return field[indices]

    def divergence_relative(self, field: np.ndarray) -> float:
        scale = max(1.0, float(np.max(np.abs(field))))
        maximum = 0.0
        for index, kz in enumerate(self.kz):
            defect = self.ky * field[index, :, 0] + float(kz) * field[index, :, 1]
            maximum = max(maximum, float(np.max(np.abs(defect))))
        return maximum / scale

    def reality_relative(self, field: np.ndarray) -> float:
        scale = max(1.0, float(np.max(np.abs(field))))
        maximum = 0.0
        for kz_index, kz in enumerate(self.kz):
            reflected_kz = -int(kz) + KZ_MAX
            for index, n_mode in enumerate(self.n):
                reflected_n = -int(n_mode) + self.n_cut
                difference = field[reflected_kz, reflected_n] - np.conjugate(field[kz_index, index])
                maximum = max(maximum, float(np.max(np.abs(difference))))
        return maximum / scale

    def outer_three_fraction(self, field: np.ndarray) -> float:
        mass = float(np.vdot(field, field).real)
        outer = np.abs(self.n) >= self.n_cut - 2
        return float(np.sum(np.abs(field[:, outer]) ** 2) / max(mass, 1.0e-300))


def generator_defect(
    space: FourierVelocity,
    matrix: np.ndarray,
    kinetic: np.ndarray,
    absolute_lambda: float,
) -> float:
    unscaled_real = space.unit_real_launch(kinetic) * math.sqrt(2.0)
    positive = space.zeros()
    positive[KZ_MAX + 1] = unscaled_real[KZ_MAX + 1]
    derivative = space.linear(positive, absolute_lambda, 0.0)
    du2_dt = derivative[KZ_MAX + 1, :, 0]
    dh_dtheta = (
        2.0 * np.sqrt(space.n.astype(float) ** 2 + MU) * du2_dt
        / (4.0 * absolute_lambda)
    )
    return float(
        np.linalg.norm(dh_dtheta - matrix @ kinetic)
        / max(1.0, np.linalg.norm(matrix @ kinetic))
    )


def norm(array: np.ndarray) -> float:
    return math.sqrt(max(0.0, float(np.vdot(array, array).real)))


def forbidden_parity_relative(fields: list[np.ndarray]) -> float:
    allowed = ({-1, 1}, {0, -2, 2}, {-1, 1, -3, 3})
    maximum = 0.0
    for field, permitted in zip(fields, allowed):
        total = norm(field)
        forbidden = np.concatenate([
            field[kz + KZ_MAX].ravel()
            for kz in range(-KZ_MAX, KZ_MAX + 1) if kz not in permitted
        ])
        maximum = max(maximum, norm(forbidden) / max(total, 1.0e-300))
    return maximum


def state_metrics(
    space: FourierVelocity,
    state: np.ndarray,
    epsilon_nu: float,
) -> dict[str, float]:
    first, second0, second2, third0, third2 = state
    second = second0 + second2
    third = third0 + third2
    first_target = space.kz_pair(first, (-1, 1))
    third0_target = space.kz_pair(third0, (-1, 1))
    third2_target = space.kz_pair(third2, (-1, 1))
    third_target = third0_target + third2_target
    third_triple = space.kz_pair(third, (-3, 3))
    gain = norm(first_target)
    gain2 = gain * gain
    gain3 = gain2 * gain
    gain4 = gain2 * gain2

    def alignment(value: np.ndarray) -> tuple[float, float, float]:
        inner = np.vdot(first_target, value)
        value_norm = norm(value)
        signed_natural = float(inner.real / max(gain4, 1.0e-300))
        cosine = float(inner.real / max(gain * value_norm, 1.0e-300))
        return signed_natural, signed_natural / (epsilon_nu**2), cosine

    mean_signed, mean_compensated, mean_cosine = alignment(third0_target)
    double_signed, double_compensated, double_cosine = alignment(third2_target)
    total_signed, total_compensated, total_cosine = alignment(third_target)
    quadratic_natural = norm(second) / max(gain2, 1.0e-300)
    target_cubic_natural = norm(third_target) / max(gain3, 1.0e-300)
    triple_cubic_natural = norm(third_triple) / max(gain3, 1.0e-300)
    combined_fields = [first, second, third]
    return {
        "v1L2": gain,
        "v1PositiveKzL2": norm(first[KZ_MAX + 1]),
        "v2MeanL2": norm(second0),
        "v2DoublePairL2": norm(second2),
        "v2L2": norm(second),
        "v3MeanPathTargetL2": norm(third0_target),
        "v3DoublePathTargetL2": norm(third2_target),
        "v3TargetPairL2": norm(third_target),
        "v3TriplePairL2": norm(third_triple),
        "v3L2": norm(third),
        "quadraticNaturalResponse": quadratic_natural,
        "targetCubicNaturalResponse": target_cubic_natural,
        "tripleCubicNaturalResponse": triple_cubic_natural,
        "quadraticCompensated": quadratic_natural / epsilon_nu,
        "targetCubicCompensated": target_cubic_natural / (epsilon_nu**2),
        "tripleCubicCompensated": triple_cubic_natural / (epsilon_nu**2),
        "meanPathSignedNaturalParallel": mean_signed,
        "doublePathSignedNaturalParallel": double_signed,
        "totalSignedNaturalParallel": total_signed,
        "meanPathSignedCompensated": mean_compensated,
        "doublePathSignedCompensated": double_compensated,
        "totalSignedCompensated": total_compensated,
        "meanPathCosineWithLinear": mean_cosine,
        "doublePathCosineWithLinear": double_cosine,
        "totalCubicCosineWithLinear": total_cosine,
        "v1OuterThreeMassFraction": space.outer_three_fraction(first),
        "v2OuterThreeMassFraction": space.outer_three_fraction(second),
        "v3OuterThreeMassFraction": space.outer_three_fraction(third),
        "maximumDivergenceRelative": max(space.divergence_relative(value) for value in state),
        "maximumRealityRelative": max(space.reality_relative(value) for value in state),
        "forbiddenParityRelative": forbidden_parity_relative(combined_fields),
    }


def integrate_case(
    n_cut: int,
    epsilon_nu: float,
    snapshots: list[float],
    fast_step: float,
    tolerances: Mapping[str, object],
    archive_prefix: str,
    grid_kind: str,
    keep_raw: bool,
) -> dict[str, object]:
    matrix = frozen_kinetic_matrix(n_cut, epsilon_nu)
    eigenvalue, kinetic, spectral = canonical_top(matrix)
    space = FourierVelocity(n_cut)
    zero = space.zeros()
    state = np.stack((space.unit_real_launch(kinetic), zero, zero, zero, zero))
    initial_norm = norm(state[0])
    generator_relative = generator_defect(space, matrix, kinetic, 1.0 / epsilon_nu)
    mask0 = np.zeros_like(zero)
    mask0[KZ_MAX] = 1.0
    mask2 = np.zeros_like(zero)
    mask2[KZ_MAX - 2] = 1.0
    mask2[KZ_MAX + 2] = 1.0

    def rhs(theta: float, values: np.ndarray) -> np.ndarray:
        first, second0, second2, third0, third2 = values
        d = epsilon_nu * theta
        factor = epsilon_nu / 4.0
        absolute_lambda = 1.0 / epsilon_nu
        quadratic = space.bilinear(first, first)
        return factor * np.stack((
            space.linear(first, absolute_lambda, d),
            space.linear(second0, absolute_lambda, d) - mask0 * quadratic,
            space.linear(second2, absolute_lambda, d) - mask2 * quadratic,
            space.linear(third0, absolute_lambda, d)
            - space.bilinear(first, second0) - space.bilinear(second0, first),
            space.linear(third2, absolute_lambda, d)
            - space.bilinear(first, second2) - space.bilinear(second2, first),
        ))

    theta = 0.0
    rows: list[dict[str, object]] = []
    raw_snapshots: list[np.ndarray] = []
    maximum_divergence = 0.0
    maximum_reality = 0.0
    maximum_forbidden = 0.0
    for snapshot_index, profile_time in enumerate(snapshots):
        target_theta = profile_time / epsilon_nu
        while theta < target_theta - 1.0e-13:
            step = min(fast_step, target_theta - theta)
            k1 = rhs(theta, state)
            k2 = rhs(theta + step / 2.0, state + step * k1 / 2.0)
            k3 = rhs(theta + step / 2.0, state + step * k2 / 2.0)
            k4 = rhs(theta + step, state + step * k3)
            state += step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
            theta += step
        theta = target_theta
        metrics = state_metrics(space, state, epsilon_nu)
        maximum_divergence = max(maximum_divergence, metrics["maximumDivergenceRelative"])
        maximum_reality = max(maximum_reality, metrics["maximumRealityRelative"])
        maximum_forbidden = max(maximum_forbidden, metrics["forbiddenParityRelative"])
        case_pass = (
            float(spectral["topEigenResidualRelative"]) <= float(tolerances["eigenResidualRelative"])
            and generator_relative <= float(tolerances["generatorRelative"])
            and metrics["maximumDivergenceRelative"] <= float(tolerances["divergenceRelative"])
            and metrics["maximumRealityRelative"] <= float(tolerances["realityRelative"])
            and metrics["forbiddenParityRelative"] <= float(tolerances["forbiddenParityRelative"])
        )
        rows.append({
            "schemaVersion": SCHEMA_VERSION,
            "evidenceClass": EVIDENCE_CLASS,
            "diagnosticOnly": True,
            "smokeMode": ARGS.smoke,
            "gridKind": grid_kind,
            "archivePrefix": archive_prefix,
            "N": n_cut,
            "dimensionPerKz": 2 * n_cut + 1,
            "viscousEpsilon": epsilon_nu,
            "absoluteLambda": 1.0 / epsilon_nu,
            "profileTime": profile_time,
            "fastTime": target_theta,
            "fastStep": fast_step,
            "topEigenvalueFastReal": float(eigenvalue.real),
            "topEigenvalueFastImag": float(eigenvalue.imag),
            "topClusterDimension": spectral["topClusterDimension"],
            "topRealGap": spectral["topRealGap"],
            "topEigenResidualRelative": spectral["topEigenResidualRelative"],
            "generatorRelativeDefect": generator_relative,
            "unitRealLaunchL2": initial_norm,
            **metrics,
            "caseChecksPass": case_pass,
        })
        if keep_raw:
            raw_snapshots.append(state.copy())
        emit(
            "snapshot_complete",
            gridKind=grid_kind,
            N=n_cut,
            viscousEpsilon=epsilon_nu,
            snapshotIndex=snapshot_index,
            profileTime=profile_time,
            v1L2=metrics["v1L2"],
            v2L2=metrics["v2L2"],
            v3TargetPairL2=metrics["v3TargetPairL2"],
        )
    return {
        "archivePrefix": archive_prefix,
        "gridKind": grid_kind,
        "N": n_cut,
        "viscousEpsilon": epsilon_nu,
        "fastStep": fast_step,
        "rows": rows,
        "endpoint": rows[-1],
        "raw": np.stack(raw_snapshots) if keep_raw else None,
        "checks": {
            "unitRealLaunch": abs(initial_norm - 1.0) <= 2.0e-12,
            "topClusterNonempty": int(spectral["topClusterDimension"]) >= 1,
            "topEigenResidual": float(spectral["topEigenResidualRelative"]) <= float(tolerances["eigenResidualRelative"]),
            "generatorCorrespondence": generator_relative <= float(tolerances["generatorRelative"]),
            "divergence": maximum_divergence <= float(tolerances["divergenceRelative"]),
            "reality": maximum_reality <= float(tolerances["realityRelative"]),
            "parity": maximum_forbidden <= float(tolerances["forbiddenParityRelative"]),
        },
    }


def relative_change(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def comparison_metrics(left: Mapping[str, object], right: Mapping[str, object]) -> dict[str, float]:
    result = {
        "linearGainRelativeChange": relative_change(float(left["v1L2"]), float(right["v1L2"])),
        "quadraticNaturalRelativeChange": relative_change(
            float(left["quadraticNaturalResponse"]), float(right["quadraticNaturalResponse"])
        ),
        "targetCubicNaturalRelativeChange": relative_change(
            float(left["targetCubicNaturalResponse"]), float(right["targetCubicNaturalResponse"])
        ),
        "tripleCubicNaturalRelativeChange": relative_change(
            float(left["tripleCubicNaturalResponse"]), float(right["tripleCubicNaturalResponse"])
        ),
        "signedCubicRelativeChange": relative_change(
            float(left["totalSignedNaturalParallel"]), float(right["totalSignedNaturalParallel"])
        ),
    }
    result["maximumRelativeChange"] = max(result.values())
    return result


def write_csv(path: Path, fields: Iterable[str], rows: list[dict[str, object]]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            encoded = {}
            for field in fields:
                value = row[field]
                if isinstance(value, bool):
                    encoded[field] = "true" if value else "false"
                elif isinstance(value, float):
                    encoded[field] = format(value, ".17g")
                else:
                    encoded[field] = value
            writer.writerow(encoded)
    os.replace(temporary, path)


def write_deterministic_npz(path: Path, arrays: Mapping[str, np.ndarray]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with zipfile.ZipFile(temporary, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(arrays):
            buffer = io.BytesIO()
            np.lib.format.write_array(buffer, np.ascontiguousarray(arrays[name]), allow_pickle=False)
            info = zipfile.ZipInfo(f"{name}.npy", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, buffer.getvalue(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    os.replace(temporary, path)


def log_slope(rows: list[Mapping[str, object]], field: str) -> float:
    x = [math.log(float(row["viscousEpsilon"])) for row in rows]
    y = [math.log(float(row[field])) for row in rows]
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    return sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y)) / sum(
        (a - x_mean) ** 2 for a in x
    )


def prepare_output(output_dir: Path, overwrite: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated = (
        "primary_rows.csv", "cutoff_convergence.csv", "step_convergence.csv",
        "coefficient_snapshots.npz", "environment.json", "primary_summary.json",
        "primary_manifest.json", "progress.ndjson",
    )
    existing = [output_dir / name for name in generated if (output_dir / name).exists()]
    if existing and not overwrite:
        raise RuntimeError("refusing to overwrite existing outputs without --overwrite")
    for path in existing:
        path.unlink()


def main() -> int:
    global PROGRESS
    output_dir = ARGS.output_dir.resolve()
    if ARGS.smoke:
        if is_within(output_dir, HERE):
            raise RuntimeError("smoke output must be outside the formal source tree")
    elif output_dir != HERE.resolve() or ARGS.config.resolve() != (HERE / "config.json").resolve():
        raise RuntimeError("formal mode must use the canonical R0.73H package and config paths")
    config = json.loads(ARGS.config.read_text(encoding="utf-8"))
    validate_config(config)
    source_provenance = strict_source_gate(ARGS.source_commit, ARGS.smoke)
    run_config = smoke_config(config) if ARGS.smoke else config
    prepare_output(output_dir, ARGS.overwrite)
    PROGRESS = output_dir / "progress.ndjson"
    emit("start", smokeMode=ARGS.smoke, sourceCommit=source_provenance["sourceCommit"])

    grid = run_config["formalGrid"]
    tolerances = run_config["tolerances"]
    cutoffs = [int(value) for value in grid["cutoffs"]]
    epsilons = [float(value) for value in grid["viscousEpsilons"]]
    snapshots = [float(value) for value in grid["profileTimeSnapshots"]]
    primary_step = float(grid["primaryFastStep"])
    cases: list[dict[str, object]] = []
    all_rows: list[dict[str, object]] = []
    raw_arrays: dict[str, np.ndarray] = {}
    case_index = 0
    for n_cut in cutoffs:
        for epsilon_nu in epsilons:
            prefix = f"case_{case_index:03d}"
            emit("case_start", gridKind="formal", N=n_cut, viscousEpsilon=epsilon_nu)
            case = integrate_case(
                n_cut, epsilon_nu, snapshots, primary_step, tolerances,
                prefix, "formal", True,
            )
            cases.append(case)
            all_rows.extend(case["rows"])
            raw_arrays[f"{prefix}_states"] = case["raw"]
            emit("case_complete", gridKind="formal", N=n_cut, viscousEpsilon=epsilon_nu)
            case_index += 1

    holdout = run_config["holdout"]
    holdout_prefix = "holdout"
    emit("case_start", gridKind="holdout", N=holdout["cutoff"], viscousEpsilon=holdout["viscousEpsilon"])
    holdout_case = integrate_case(
        int(holdout["cutoff"]), float(holdout["viscousEpsilon"]), snapshots,
        float(holdout["fastStep"]), tolerances, holdout_prefix, "holdout", True,
    )
    all_rows.extend(holdout_case["rows"])
    raw_arrays["holdout_states"] = holdout_case["raw"]
    emit("case_complete", gridKind="holdout", N=holdout["cutoff"], viscousEpsilon=holdout["viscousEpsilon"])

    endpoints = {
        (int(case["N"]), float(case["viscousEpsilon"])): case["endpoint"]
        for case in cases
    }
    convergence_rows: list[dict[str, object]] = []
    for epsilon_nu in epsilons:
        for coarse, fine in zip(cutoffs, cutoffs[1:]):
            changes = comparison_metrics(endpoints[(coarse, epsilon_nu)], endpoints[(fine, epsilon_nu)])
            gate = (not ARGS.smoke) and fine == max(cutoffs)
            convergence_rows.append({
                "schemaVersion": "r073h-cutoff-convergence-v1",
                "evidenceClass": EVIDENCE_CLASS,
                "diagnosticOnly": True,
                "viscousEpsilon": epsilon_nu,
                "absoluteLambda": 1.0 / epsilon_nu,
                "coarseN": coarse,
                "fineN": fine,
                **changes,
                "finestCutoffGateApplied": gate,
                "passCheck": (not gate) or changes["maximumRelativeChange"] <= float(tolerances["finestCutoffRelative"]),
                "ordinaryCutoffAgreementIsTailProof": False,
            })

    step_spec = run_config["stepConvergence"]
    step_rows: list[dict[str, object]] = []
    step_n = int(step_spec["cutoff"])
    for epsilon_nu in [float(value) for value in step_spec["viscousEpsilons"]]:
        step_results: dict[float, Mapping[str, object]] = {primary_step: endpoints[(step_n, epsilon_nu)]}
        for step in [float(value) for value in step_spec["fastSteps"]]:
            if step in step_results:
                continue
            emit("step_case_start", N=step_n, viscousEpsilon=epsilon_nu, fastStep=step)
            result = integrate_case(
                step_n, epsilon_nu, [snapshots[-1]], step, tolerances,
                f"step_N{step_n}", "step", False,
            )
            step_results[step] = result["endpoint"]
            emit("step_case_complete", N=step_n, viscousEpsilon=epsilon_nu, fastStep=step)
        ordered_steps = sorted(step_results, reverse=True)
        for coarse, fine in zip(ordered_steps, ordered_steps[1:]):
            changes = comparison_metrics(step_results[coarse], step_results[fine])
            step_rows.append({
                "schemaVersion": "r073h-step-convergence-v1",
                "evidenceClass": EVIDENCE_CLASS,
                "diagnosticOnly": True,
                "N": step_n,
                "viscousEpsilon": epsilon_nu,
                "absoluteLambda": 1.0 / epsilon_nu,
                "coarseFastStep": coarse,
                "fineFastStep": fine,
                **changes,
                "passCheck": changes["maximumRelativeChange"] <= float(tolerances["stepRelative"]),
            })

    finest = max(cutoffs)
    fit_epsilons = [float(value) for value in run_config["fitWindowViscousEpsilons"]]
    fit_rows = [endpoints[(finest, value)] for value in fit_epsilons]
    quadratic_slope = log_slope(fit_rows, "quadraticNaturalResponse")
    target_cubic_slope = log_slope(fit_rows, "targetCubicNaturalResponse")
    slope_gate_applied = not ARGS.smoke
    slope_checks = {
        "quadraticSlopeInFrozenWindow": (
            (not slope_gate_applied)
            or float(tolerances["quadraticSlopeMinimum"]) <= quadratic_slope <= float(tolerances["quadraticSlopeMaximum"])
        ),
        "targetCubicSlopeInFrozenWindow": (
            (not slope_gate_applied)
            or float(tolerances["targetCubicSlopeMinimum"]) <= target_cubic_slope <= float(tolerances["targetCubicSlopeMaximum"])
        ),
    }

    holdout_endpoint = holdout_case["endpoint"]
    predictions = holdout["predictions"]
    holdout_gate_applied = not ARGS.smoke
    holdout_checks = {
        "quadraticCompensatedPrediction": (
            (not holdout_gate_applied)
            or float(predictions["quadraticCompensatedMinimum"])
            <= float(holdout_endpoint["quadraticCompensated"])
            <= float(predictions["quadraticCompensatedMaximum"])
        ),
        "targetCubicCompensatedPrediction": (
            (not holdout_gate_applied)
            or float(predictions["targetCubicCompensatedMinimum"])
            <= float(holdout_endpoint["targetCubicCompensated"])
            <= float(predictions["targetCubicCompensatedMaximum"])
        ),
        "signedParallelCompensatedPrediction": (
            (not holdout_gate_applied)
            or float(predictions["signedParallelCompensatedMinimum"])
            <= float(holdout_endpoint["totalSignedCompensated"])
            <= float(predictions["signedParallelCompensatedMaximum"])
        ),
    }

    finest_outer = max(
        float(endpoints[(finest, epsilon)][field])
        for epsilon in epsilons
        for field in (
            "v1OuterThreeMassFraction", "v2OuterThreeMassFraction", "v3OuterThreeMassFraction"
        )
    )
    package_checks = {
        "allCaseChecksPass": all(all(case["checks"].values()) for case in cases) and all(holdout_case["checks"].values()),
        "allFinestCutoffChecksPass": all(row["passCheck"] for row in convergence_rows if row["finestCutoffGateApplied"]),
        "allStepChecksPass": all(row["passCheck"] for row in step_rows),
        "finestOuterThreeMassPass": ARGS.smoke or finest_outer <= float(tolerances["outerThreeMassFraction"]),
        **slope_checks,
        **holdout_checks,
    }

    rows_path = output_dir / "primary_rows.csv"
    convergence_path = output_dir / "cutoff_convergence.csv"
    step_path = output_dir / "step_convergence.csv"
    raw_path = output_dir / "coefficient_snapshots.npz"
    write_csv(rows_path, ROW_FIELDS, all_rows)
    write_csv(convergence_path, CONVERGENCE_FIELDS, convergence_rows)
    write_csv(step_path, STEP_FIELDS, step_rows)
    write_deterministic_npz(raw_path, raw_arrays)

    elapsed = time.perf_counter() - START
    environment = {
        "schemaVersion": "r073h-environment-v1",
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logicalCpuCount": os.cpu_count(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "threadEnvironment": {
            name: os.environ.get(name) for name in (
                "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"
            )
        },
        "scientificWallTimeSeconds": elapsed,
        "sourceCommit": source_provenance["sourceCommit"],
        "smokeMode": ARGS.smoke,
    }
    environment_path = output_dir / "environment.json"
    atomic_text(environment_path, canonical(environment))

    companions = [rows_path, convergence_path, step_path, raw_path, environment_path]
    summary = {
        "schemaVersion": SCHEMA_VERSION,
        "release": "R0.73H",
        "evidenceClass": EVIDENCE_CLASS,
        "diagnosticOnly": True,
        "smokeMode": ARGS.smoke,
        "pilotInformed": True,
        "sourceProvenance": source_provenance,
        "configBinding": binding(ARGS.config.resolve(), ROOT),
        "formalGrid": grid,
        "holdout": {
            "configuration": holdout,
            "gateApplied": holdout_gate_applied,
            "endpoint": {field: holdout_endpoint[field] for field in ROW_FIELDS if field in holdout_endpoint},
            "checks": holdout_checks,
        },
        "scaling": {
            "fitWindowViscousEpsilons": fit_epsilons,
            "gateApplied": slope_gate_applied,
            "quadraticNaturalLogSlope": quadratic_slope,
            "targetCubicNaturalLogSlope": target_cubic_slope,
            "checks": slope_checks,
        },
        "verification": {
            "caseCount": len(cases),
            "rowCount": len(all_rows),
            "cutoffComparisonCount": len(convergence_rows),
            "stepComparisonCount": len(step_rows),
            "finestOuterThreeMassMaximum": finest_outer,
            "checks": package_checks,
        },
        "archiveIndex": [
            {
                "archivePrefix": case["archivePrefix"],
                "gridKind": case["gridKind"],
                "N": case["N"],
                "viscousEpsilon": case["viscousEpsilon"],
                "stateOrder": ["V1", "V2_Kz0", "V2_KzPlusMinus2", "V3_via_Kz0", "V3_via_KzPlusMinus2"],
                "shape": list(case["raw"].shape),
            }
            for case in cases + [holdout_case]
        ],
        "dataBindings": [binding(path, output_dir) for path in companions],
        "allChecksPass": all(package_checks.values()),
        "claimBoundary": config["claimBoundary"],
        "continuumConclusion": "none; exact parity plus finite binary64 Galerkin diagnostics only",
    }
    summary_path = output_dir / "primary_summary.json"
    atomic_text(summary_path, canonical(summary))
    emit("complete", allChecksPass=summary["allChecksPass"], scientificWallTimeSeconds=elapsed)
    manifest_files = companions + [summary_path, PROGRESS]
    manifest = {
        "schemaVersion": "r073h-primary-manifest-v1",
        "release": "R0.73H",
        "sourceCommit": source_provenance["sourceCommit"],
        "smokeMode": ARGS.smoke,
        "files": [binding(path, output_dir) for path in manifest_files],
        "allChecksPass": summary["allChecksPass"],
        "claimBoundary": config["claimBoundary"],
    }
    atomic_text(output_dir / "primary_manifest.json", canonical(manifest))
    return 0 if summary["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
