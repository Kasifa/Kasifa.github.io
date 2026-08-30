#!/usr/bin/env python3
"""Independent vorticity/FFT validation of the R0.73M a/b/c hierarchy.

The program does not import the primary producer.  It reconstructs the
selected launch from direct Orr--Sommerfeld coefficients, evolves scalar
vorticity on alias-free physical grids, and converts the five endpoint paths
back to physical velocity for coefficient-by-coefficient comparison.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = Path(__file__).resolve()
SOURCE_FILES = (
    "research/r073m_numerical_protocol.md",
    "research/certificates/r073m/README.md",
    "research/certificates/r073m/command.txt",
    "research/certificates/r073m/config.json",
    "research/certificates/r073m/requirements.txt",
    "research/certificates/r073m/primary_diagnostic.py",
    "research/certificates/r073m/independent_linear.py",
    "research/certificates/r073m/independent_hierarchy.py",
    "research/certificates/r073m/exact_identities.py",
    "research/certificates/r073m/generate_certificate.py",
    "research/certificates/r073m/validate_certificate.py",
    "research/certificates/r073m/seal_package.py",
)
KZ_MAX = 3
START = time.monotonic()
EXPECTED_CLAIM_BOUNDARY = {
    "finiteInviscidActionProxyComputed": True,
    "finiteViscousActionComputedSeparately": True,
    "finitePrescribedActionRecodingComputed": True,
    "finiteABCoefficientsComputed": True,
    "continuumActionCertifiedByFiniteComputation": False,
    "continuumGainPrefactorCertifiedByFiniteComputation": False,
    "prefactorLimitCertified": False,
    "twoTermWKBCertified": False,
    "uniformTaylorRadiusCertified": False,
    "fourthOrderRemainderCertified": False,
    "fullNonlinearNavierStokesTrajectoryComputed": False,
    "finiteCutoffAgreementIsTailProof": False,
    "singleFixedBackgroundLyapunovInstabilityCertified": False,
    "transverseThreeDimensionalClosureCertified": False,
    "finiteTimeSingularityCertified": False,
    "clayProblemSolved": False,
}
EXPECTED_EXACT_RATIONALS = {
    "profileTimeEnd": "1/450", "physicalTimeEnd": "1/1800",
    "muStar": "167/1000", "twoRateMargin": "1/1500",
    "threeRateMargin": "1/1000", "fourRateMargin": "21/125",
}
EXPECTED_CONFIG_SHA256 = "100775fd92e34b939c563546b83b838eda60f677f7452a13459cf6ef2b2252fb"
EXPECTED_TOLERANCES = {
    "numericalReality": 1e-10, "eigenResidualRelative": 5e-12,
    "generatorRelative": 5e-12, "divergenceRelative": 5e-10,
    "realityRelative": 5e-10, "forbiddenParityRelative": 5e-10,
    "aEndpointNormalizationAbsolute": 5e-10,
    "outerThreeMassFraction": 1e-8, "physicalKineticGainRelative": 2e-7,
    "largestCutoffActionProxyAbsolute": 2e-12,
    "largestCutoffPrefactorAbsolute": 2e-6,
    "hierarchyFinestCutoffRelative": 1e-6, "hierarchyStepRelative": 1e-7,
    "independentLinearActionRelative": 2e-6,
    "independentLinearGainRelative": 2e-6,
    "independentLinearPrefactorAbsolute": 2e-6,
    "independentLinearRefinement": 2e-6,
    "independentHierarchyCoefficientRelative": 2e-8,
    "independentHierarchyForbiddenParityRelative": 5e-10,
}
EXPECTED_SENTINELS = [
    {"cutoff": 32, "viscousEpsilon": 0.001, "fastStep": 0.05},
    {"cutoff": 48, "viscousEpsilon": 0.00025, "fastStep": 0.05},
    {"cutoff": 64, "viscousEpsilon": 0.0000625, "fastStep": 0.025},
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
for name in (
    "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
    "MKL_NUM_THREADS",
):
    os.environ[name] = "1"
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
from scipy.linalg import eig  # noqa: E402


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"not a regular file: {path}")
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=False, allow_nan=False) + "\n"


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(canonical(value), encoding="utf-8")
    os.replace(temporary, path)


class Monitor:
    def __init__(self, progress: Path, resources: Path) -> None:
        self.progress = progress
        self.resources = resources
        for path in (progress, resources):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    def emit(self, event: str, **fields: object) -> None:
        row = {
            "event": event, "timestampUtc": now(),
            "elapsedSeconds": time.monotonic() - START, **fields,
        }
        line = json.dumps(row, sort_keys=True, allow_nan=False)
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")
        print(line, flush=True)

    def sample(self, event: str, **fields: object) -> None:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        row = {
            "event": event, "timestampUtc": now(),
            "elapsedSeconds": time.monotonic() - START,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetSizePlatformUnits": usage.ru_maxrss,
            **fields,
        }
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")


def source_gate(commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RuntimeError("formal independent run requires a full source commit")
    resolved = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{commit}^{{commit}}"], text=True,
    ).strip()
    if resolved != commit:
        raise RuntimeError("source commit did not resolve exactly")
    head = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True,
    ).strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", commit, head],
        check=False,
    ).returncode != 0:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    rows = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        committed = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{commit}:{relative}"],
        )
        if committed != path.read_bytes():
            raise RuntimeError(f"working source differs from source commit: {relative}")
        rows.append(binding(path, ROOT))
    return {
        "enforced": True, "sourceCommit": commit, "headAtRun": head,
        "allSourceBlobsMatch": True, "bindings": rows,
    }


def verify_upstream(config: Mapping[str, Any]) -> list[dict[str, object]]:
    rows = []
    for expected in config["upstreamBindings"]:
        path = ROOT / expected["path"]
        actual = sha256(path)
        if actual != expected["sha256"]:
            raise RuntimeError(f"upstream hash drift: {expected['path']}")
        rows.append({**expected, "bytes": path.stat().st_size})
    return rows


def matrix_from_os_formula(cutoff: int, epsilon: float) -> np.ndarray:
    gamma = 0.5
    modes = np.arange(-cutoff, cutoff + 1, dtype=int)
    ell = modes.astype(float) ** 2 + 0.25
    shifts = modes[:, None] - modes[None, :]
    w_hat = {1: 0.25j, -1: -0.25j, 2: -0.125j, -2: 0.125j}
    wxx_hat = {1: -0.25j, -1: 0.25j, 2: 0.5j, -2: -0.5j}
    w = np.zeros(shifts.shape, dtype=np.complex128)
    wxx = np.zeros_like(w)
    for shift, value in w_hat.items():
        w[shifts == shift] = value
    for shift, value in wxx_hat.items():
        wxx[shifts == shift] = value
    raw = -1j * gamma * (w + wxx / ell[None, :])
    transformed = ((1.0 / np.sqrt(ell))[:, None]
                   * raw * np.sqrt(ell)[None, :])
    return transformed - epsilon * np.diag(ell)


def anchor(vector: np.ndarray, cutoff: int) -> complex:
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    return complex(0.5 * np.sum(vector / np.sqrt(modes * modes + 0.25)))


def selected_launch(matrix: np.ndarray, cutoff: int,
                    center: complex, radius: float) -> np.ndarray:
    values, vectors = eig(matrix, left=False, right=True, check_finite=False)
    inside = np.flatnonzero(np.abs(values - center) < radius)
    if inside.size != 1:
        raise RuntimeError(f"fixed-contour count is {inside.size}, not one")
    vector = np.asarray(vectors[:, int(inside[0])], dtype=np.complex128)
    vector /= np.linalg.norm(vector)
    value = anchor(vector, cutoff)
    if abs(value) <= 1e-12:
        raise RuntimeError("independent phase anchor vanished")
    vector *= np.exp(-1j * np.angle(value))
    if anchor(vector, cutoff).real < 0.0:
        vector *= -1.0
    return vector


class VorticityFFT:
    def __init__(self, cutoff: int) -> None:
        self.cutoff = cutoff
        self.n = np.arange(-cutoff, cutoff + 1, dtype=int)
        self.kz = np.arange(-KZ_MAX, KZ_MAX + 1, dtype=int)
        self.ny = 8 * cutoff + 8
        self.nz = 16
        self.normalization = self.ny * self.nz
        self.ky_full = np.fft.fftfreq(self.ny, d=1.0 / self.ny)
        self.kz_full = np.fft.fftfreq(self.nz, d=1.0 / self.nz)
        self.ky_grid = self.ky_full[:, None]
        self.kz_grid = self.kz_full[None, :]
        self.wave_squared = self.ky_grid ** 2 + self.kz_grid ** 2

    def embed(self, coefficients: np.ndarray) -> np.ndarray:
        full = np.zeros((self.ny, self.nz), dtype=np.complex128)
        for kz_index, kz in enumerate(self.kz):
            for index, n_mode in enumerate(self.n):
                full[(2 * int(n_mode)) % self.ny, int(kz) % self.nz] = (
                    coefficients[kz_index, index]
                )
        return full

    def extract(self, full: np.ndarray) -> np.ndarray:
        coefficients = np.zeros((len(self.kz), len(self.n)), dtype=np.complex128)
        for kz_index, kz in enumerate(self.kz):
            for index, n_mode in enumerate(self.n):
                coefficients[kz_index, index] = full[
                    (2 * int(n_mode)) % self.ny, int(kz) % self.nz
                ]
        return coefficients

    def physical(self, full: np.ndarray) -> np.ndarray:
        return np.fft.ifftn(full * self.normalization)

    def velocity_full(self, omega: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u2 = np.zeros_like(omega)
        u3 = np.zeros_like(omega)
        nonzero = self.wave_squared > 0.0
        ky = np.broadcast_to(self.ky_grid, self.wave_squared.shape)
        kz = np.broadcast_to(self.kz_grid, self.wave_squared.shape)
        u2[nonzero] = 1j * kz[nonzero] * omega[nonzero] / self.wave_squared[nonzero]
        u3[nonzero] = -1j * ky[nonzero] * omega[nonzero] / self.wave_squared[nonzero]
        return u2, u3

    def advect(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        left_full = self.embed(left)
        right_full = self.embed(right)
        u2, u3 = self.velocity_full(left_full)
        product = (
            self.physical(u2) * self.physical(1j * self.ky_grid * right_full)
            + self.physical(u3) * self.physical(1j * self.kz_grid * right_full)
        )
        return self.extract(np.fft.fftn(product) / self.normalization)

    def linear(self, omega: np.ndarray, absolute_lambda: float,
               d_value: float) -> np.ndarray:
        full = self.embed(omega)
        u2, _ = self.velocity_full(full)
        y = 2.0 * math.pi * np.arange(self.ny) / self.ny
        w = (-0.5 * math.exp(-d_value) * np.sin(2.0 * y)
             + 0.25 * math.exp(-4.0 * d_value) * np.sin(4.0 * y))
        wxx = (0.5 * math.exp(-d_value) * np.sin(2.0 * y)
               - math.exp(-4.0 * d_value) * np.sin(4.0 * y))
        base_advection = (
            (2.0 * absolute_lambda * w)[:, None]
            * self.physical(1j * self.kz_grid * full)
            + self.physical(u2) * (8.0 * absolute_lambda * wxx)[:, None]
        )
        diffusion = -self.wave_squared * full
        return self.extract(
            diffusion - np.fft.fftn(base_advection) / self.normalization
        )

    def launch(self, kinetic: np.ndarray) -> np.ndarray:
        profile = kinetic / (2.0 * np.sqrt(self.n.astype(float) ** 2 + 0.25))
        result = np.zeros((len(self.kz), len(self.n)), dtype=np.complex128)
        square = 4.0 * self.n.astype(float) ** 2 + 1.0
        plus = KZ_MAX + 1
        minus = KZ_MAX - 1
        result[plus] = -1j * square * profile / math.sqrt(2.0)
        for index, n_mode in enumerate(self.n):
            reflected = -int(n_mode) + self.cutoff
            result[minus, reflected] = np.conjugate(result[plus, index])
        return result

    def velocity_coefficients(self, omega: np.ndarray) -> np.ndarray:
        full = self.embed(omega)
        u2, u3 = self.velocity_full(full)
        result = np.zeros((len(self.kz), len(self.n), 2), dtype=np.complex128)
        for kz_index, kz in enumerate(self.kz):
            for index, n_mode in enumerate(self.n):
                y_index = (2 * int(n_mode)) % self.ny
                z_index = int(kz) % self.nz
                result[kz_index, index, 0] = u2[y_index, z_index]
                result[kz_index, index, 1] = u3[y_index, z_index]
        return result


def integrate(cutoff: int, epsilon: float, d_end: float,
              fast_step: float, center: complex, radius: float) -> tuple[np.ndarray, int]:
    space = VorticityFFT(cutoff)
    first = space.launch(selected_launch(
        matrix_from_os_formula(cutoff, epsilon), cutoff, center, radius,
    ))
    zero = np.zeros_like(first)
    state = np.stack((first, zero, zero, zero, zero))
    mask0 = np.zeros_like(first)
    mask0[KZ_MAX] = 1.0
    mask2 = np.zeros_like(first)
    mask2[KZ_MAX - 2] = 1.0
    mask2[KZ_MAX + 2] = 1.0

    def rhs(theta: float, values: np.ndarray) -> np.ndarray:
        one, two0, two2, three0, three2 = values
        d_value = epsilon * theta
        factor = epsilon / 4.0
        absolute_lambda = 1.0 / epsilon
        quadratic = space.advect(one, one)
        return factor * np.stack((
            space.linear(one, absolute_lambda, d_value),
            space.linear(two0, absolute_lambda, d_value) - mask0 * quadratic,
            space.linear(two2, absolute_lambda, d_value) - mask2 * quadratic,
            space.linear(three0, absolute_lambda, d_value)
            - space.advect(one, two0) - space.advect(two0, one),
            space.linear(three2, absolute_lambda, d_value)
            - space.advect(one, two2) - space.advect(two2, one),
        ))

    theta = 0.0
    target = d_end / epsilon
    steps = 0
    while theta < target - 1e-13:
        step = min(fast_step, target - theta)
        k1 = rhs(theta, state)
        k2 = rhs(theta + step / 2.0, state + step * k1 / 2.0)
        k3 = rhs(theta + step / 2.0, state + step * k2 / 2.0)
        k4 = rhs(theta + step, state + step * k3)
        state += step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        theta += step
        steps += 1
    if not bool(np.isfinite(state).all()):
        raise RuntimeError("nonfinite vorticity hierarchy before conversion")
    velocity = np.stack([space.velocity_coefficients(field) for field in state])
    if not bool(np.isfinite(velocity).all()):
        raise RuntimeError("nonfinite independent velocity hierarchy")
    return velocity, steps


def norm(value: np.ndarray) -> float:
    if not bool(np.isfinite(value).all()):
        raise RuntimeError("nonfinite independent hierarchy coefficient array")
    squared = float(np.vdot(value, value).real)
    if not math.isfinite(squared) or squared < -1e-14:
        raise RuntimeError("nonfinite or materially negative squared norm")
    return math.sqrt(max(0.0, squared))


def forbidden_relative(state: np.ndarray) -> float:
    combined = (state[0], state[1] + state[2], state[3] + state[4])
    allowed = ({-1, 1}, {0, -2, 2}, {-1, 1, -3, 3})
    maximum = 0.0
    for field, permitted in zip(combined, allowed):
        forbidden = np.concatenate([
            field[kz + KZ_MAX].ravel()
            for kz in range(-KZ_MAX, KZ_MAX + 1) if kz not in permitted
        ])
        maximum = max(maximum, norm(forbidden) / max(norm(field), 1e-300))
    return maximum


def validate_config(config: Mapping[str, Any]) -> None:
    if config.get("schemaVersion") != "r073m-prescribed-action-finite-config-v1":
        raise RuntimeError("configuration schema mismatch")
    if not (config.get("release") == "R0.73M"
            and config.get("diagnosticOnly") is True
            and config.get("gamma") == 0.5
            and config.get("profileTimeEnd") == 1.0 / 450.0
            and config.get("physicalTimeEnd") == 1.0 / 1800.0
            and config.get("profileToPhysicalTimeRule") == "d=4t"):
        raise RuntimeError("endpoint or evidence contract drift")
    if config.get("exactRationals") != EXPECTED_EXACT_RATIONALS:
        raise RuntimeError("exact rational contract drift")
    if config.get("fixedContour") != {
        "centerReal": 0.17, "centerImag": 0.0, "radius": 0.003,
    }:
        raise RuntimeError("fixed contour drift")
    if config.get("primaryLinearSolver") != {
        "method": "DOP853", "rtol": 1e-10, "atol": 1e-12,
        "maxStep": 1.0 / 115200.0,
    }:
        raise RuntimeError("primary linear solver contract drift")
    if config.get("hierarchy") != {
        "profileTimeSnapshots": [0.0, 1.0 / 450.0],
        "primaryFastStep": 0.05,
        "stepConvergence": {"cutoff": 64,
                            "viscousEpsilons": [0.001, 0.0000625],
                            "fastSteps": [0.1, 0.05, 0.025]},
    }:
        raise RuntimeError("hierarchy contract drift")
    if config.get("displayRhos") != [0.02, 0.05]:
        raise RuntimeError("display rho grid drift")
    if config.get("independentLinear") != {
        "stepCounts": [256, 512],
        "sentinels": [
            {"cutoff": 32, "viscousEpsilon": 0.001},
            {"cutoff": 32, "viscousEpsilon": 0.0000625},
            {"cutoff": 48, "viscousEpsilon": 0.00025},
            {"cutoff": 64, "viscousEpsilon": 0.0005},
            {"cutoff": 64, "viscousEpsilon": 0.0000625},
        ],
    }:
        raise RuntimeError("independent linear contract drift")
    if config.get("independentHierarchy") != {"sentinels": EXPECTED_SENTINELS}:
        raise RuntimeError("independent hierarchy contract drift")
    if (list(config.get("tolerances", {}).items())
            != list(EXPECTED_TOLERANCES.items())):
        raise RuntimeError("tolerance key set, order, or values drifted")
    if (list(config.get("claimBoundary", {}).items())
            != list(EXPECTED_CLAIM_BOUNDARY.items())):
        raise RuntimeError("claim boundary key set, order, spelling, or values drifted")
    schema = config.get("outputSchema", {})
    expected_paths = [
        "linear.finiteInviscidActionProxy", "linear.finiteViscousAction",
        "hierarchy.actualPhysicalLinearGain", "finiteInviscidActionPrefactor",
        "hierarchy.aEndpointL2", "hierarchy.bEndpointL2",
        "hierarchy.cTargetEndpointL2", "hierarchy.cTotalSignedParallel",
    ]
    if ([row.get("path") for row in schema.get("caseScalars", [])]
            != expected_paths
            or schema.get("coefficientArchive", {}).get("stateOrder") != [
                "V1", "V2_Kz0", "V2_KzPlusMinus2",
                "V3_via_Kz0", "V3_via_KzPlusMinus2",
            ]
            or schema.get("thirdOrderTargetDiagnostics", {}).get("rhoValues")
            != [0.02, 0.05]):
        raise RuntimeError("output schema drift")


def main() -> int:
    output = ARGS.output.resolve()
    primary_dir = ARGS.primary_dir.resolve()
    if ARGS.smoke:
        if output.is_relative_to(HERE.resolve()) or primary_dir.is_relative_to(HERE.resolve()):
            raise RuntimeError("smoke paths must be outside the formal package")
    elif (
        output != (HERE / "independent_hierarchy.json").resolve()
        or primary_dir != HERE.resolve()
        or ARGS.config.resolve() != (HERE / "config.json").resolve()
    ):
        raise RuntimeError("formal independent run must use canonical paths")
    for path in (output, ARGS.progress.resolve(), ARGS.resources.resolve()):
        if path.exists() and not ARGS.overwrite:
            raise RuntimeError(f"refusing to overwrite: {path}")
    config = json.loads(ARGS.config.read_text(encoding="utf-8"))
    if sha256(ARGS.config.resolve()) != EXPECTED_CONFIG_SHA256:
        raise RuntimeError("canonical configuration byte contract drift")
    validate_config(config)
    primary_path = primary_dir / "primary_results.json"
    archive_path = primary_dir / "coefficient_endpoints.npz"
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    if primary.get("smokeMode") is not ARGS.smoke or not primary.get("allChecksPass"):
        raise RuntimeError("primary result mode/pass state mismatch")
    provenance = source_gate(ARGS.source_commit, ARGS.smoke)
    upstream = verify_upstream(config)
    monitor = Monitor(ARGS.progress.resolve(), ARGS.resources.resolve())
    monitor.emit("start", smokeMode=ARGS.smoke,
                 method="independent scalar-vorticity alias-free FFT hierarchy")
    monitor.sample("start")

    if ARGS.smoke:
        sentinels = [
            {"cutoff": 8, "viscousEpsilon": 0.001, "fastStep": 0.1},
            {"cutoff": 10, "viscousEpsilon": 0.0005, "fastStep": 0.1},
        ]
        coefficient_tolerance = 2e-3
    else:
        sentinels = config["independentHierarchy"]["sentinels"]
        coefficient_tolerance = float(
            config["tolerances"]["independentHierarchyCoefficientRelative"]
        )
    parity_tolerance = float(
        config["tolerances"]["independentHierarchyForbiddenParityRelative"]
    )
    contour = config["fixedContour"]
    center = complex(float(contour["centerReal"]), float(contour["centerImag"]))
    radius = float(contour["radius"])
    d_end = float(config["profileTimeEnd"])
    names = (
        "V1", "V2_Kz0", "V2_KzPlusMinus2",
        "V3_via_Kz0", "V3_via_KzPlusMinus2",
    )
    validations = []
    archive_index = {
        (int(row["N"]), float(row["epsilon"])): row["archiveKey"]
        for row in primary["archiveIndex"]
    }
    with np.load(archive_path, allow_pickle=False) as archive:
        for index, sentinel in enumerate(sentinels, start=1):
            cutoff = int(sentinel["cutoff"])
            epsilon = float(sentinel["viscousEpsilon"])
            fast_step = float(sentinel["fastStep"])
            monitor.emit("sentinel-start", index=index, N=cutoff, epsilon=epsilon,
                         fastStep=fast_step)
            independent, steps = integrate(
                cutoff, epsilon, d_end, fast_step, center, radius,
            )
            key = archive_index[(cutoff, epsilon)]
            primary_state = archive[key]
            per_path = {
                name: norm(independent[path_index] - primary_state[path_index])
                / max(norm(independent[path_index]), norm(primary_state[path_index]), 1e-300)
                for path_index, name in enumerate(names)
            }
            maximum = max(per_path.values())
            forbidden = forbidden_relative(independent)
            passed = maximum <= coefficient_tolerance and forbidden <= parity_tolerance
            validations.append({
                "N": cutoff, "epsilon": epsilon, "fastStep": fast_step,
                "archiveKey": key, "stepCount": steps,
                "physicalGrid": {
                    "yCount": 8 * cutoff + 8,
                    "zCount": 16,
                    "aliasFreeForHierarchyThroughOrderThree": True,
                },
                "pathRelativeErrors": per_path,
                "maximumCoefficientRelativeError": maximum,
                "forbiddenParityRelative": forbidden,
                "pass": passed,
            })
            monitor.sample("sentinel-complete", index=index, N=cutoff, epsilon=epsilon)
            monitor.emit("sentinel-complete", index=index, N=cutoff, epsilon=epsilon,
                         maximumCoefficientRelativeError=maximum,
                         forbiddenParityRelative=forbidden, passCheck=passed)

    maximum_coefficient = max(row["maximumCoefficientRelativeError"] for row in validations)
    maximum_forbidden = max(row["forbiddenParityRelative"] for row in validations)
    passed = all(row["pass"] for row in validations)
    result = {
        "schemaVersion": "r073m-independent-vorticity-fft-v1",
        "release": "R0.73M",
        "status": "passed" if passed else "failed",
        "smokeMode": ARGS.smoke,
        "method": {
            "matrix": "direct Orr--Sommerfeld Fourier coefficients",
            "state": "scalar vorticity with independently written Biot--Savart recovery",
            "nonlinearity": "alias-free physical-grid FFT products",
            "timeIntegrator": "fixed-step classical RK4 in fast time",
            "importsPrimaryProducer": False,
        },
        "sourceProvenance": {
            "enforced": provenance["enforced"],
            "sourceCommit": provenance["sourceCommit"],
            "allSourceBlobsMatch": provenance["allSourceBlobsMatch"],
            **({"bindings": provenance["bindings"]} if provenance["enforced"] else {}),
        },
        "sourceBinding": binding(SOURCE, ROOT),
        "configurationBinding": binding(ARGS.config.resolve(), ROOT),
        "primaryBindings": [binding(primary_path, primary_dir),
                            binding(archive_path, primary_dir)],
        "upstreamBindings": upstream,
        "sentinels": [
            {
                "cutoff": int(row["cutoff"]),
                "viscousEpsilon": float(row["viscousEpsilon"]),
                "fastStep": float(row["fastStep"]),
            }
            for row in sentinels
        ],
        "validations": validations,
        "maximumCoefficientRelativeError": maximum_coefficient,
        "maximumForbiddenParityRelative": maximum_forbidden,
        "allChecksPass": passed,
        "claimBoundary": config["claimBoundary"],
    }
    atomic_json(output, result)
    monitor.sample("complete", sentinels=len(validations))
    monitor.emit("complete", allChecksPass=passed, sentinels=len(validations))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
