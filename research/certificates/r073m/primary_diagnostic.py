#!/usr/bin/env python3
"""Primary finite R0.73M prescribed-action and a/b/c diagnostic.

The program computes the viscous finite selected gain and, separately, the
epsilon-zero finite action proxy.  It evolves the physical harmonic hierarchy
through cubic order and normalizes a, b, and c by the first, second, and third
powers of the actual computed physical gain.  Every result is finite
binary64 evidence only.
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
import resource
import subprocess
import sys
import time
from typing import Any, Iterable, Mapping
import zipfile


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
GENERATED = (
    "primary_results.json",
    "primary_rows.csv",
    "action_nodes.csv",
    "cutoff_convergence.csv",
    "step_convergence.csv",
    "coefficient_endpoints.npz",
    "primary_environment.json",
    "primary_progress.ndjson",
    "primary_resources.ndjson",
    "primary_manifest.json",
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
    "profileTimeEnd": "1/450",
    "physicalTimeEnd": "1/1800",
    "muStar": "167/1000",
    "twoRateMargin": "1/1500",
    "threeRateMargin": "1/1000",
    "fourRateMargin": "21/125",
}
EXPECTED_CONFIG_SHA256 = "d0f757c41ce96971e64860e028e55d9378166ef1df6de28b7c0c2527c6bbb7d4"

EXPECTED_TOLERANCES = {
    "numericalReality": 1e-10,
    "eigenResidualRelative": 5e-12,
    "generatorRelative": 5e-12,
    "divergenceRelative": 5e-10,
    "realityRelative": 5e-10,
    "forbiddenParityRelative": 5e-10,
    "aEndpointNormalizationAbsolute": 5e-10,
    "outerThreeMassFraction": 1e-8,
    "physicalKineticGainRelative": 2e-7,
    "largestCutoffActionProxyAbsolute": 2e-12,
    "largestCutoffPrefactorAbsolute": 2e-6,
    "hierarchyFinestCutoffRelative": 1e-6,
    "hierarchyStepRelative": 1e-7,
    "independentLinearActionRelative": 2e-6,
    "independentLinearGainRelative": 2e-6,
    "independentLinearPrefactorAbsolute": 2e-6,
    "independentLinearRefinement": 2e-6,
    "independentHierarchyCoefficientRelative": 2e-8,
    "independentHierarchyForbiddenParityRelative": 5e-10,
}

EXPECTED_LINEAR_SENTINELS = [
    {"cutoff": 40, "viscousEpsilon": 0.001},
    {"cutoff": 40, "viscousEpsilon": 0.0000625},
    {"cutoff": 48, "viscousEpsilon": 0.00025},
    {"cutoff": 64, "viscousEpsilon": 0.0005},
    {"cutoff": 64, "viscousEpsilon": 0.0000625},
]

EXPECTED_HIERARCHY_SENTINELS = [
    {"cutoff": 40, "viscousEpsilon": 0.001, "fastStep": 0.05},
    {"cutoff": 48, "viscousEpsilon": 0.00025, "fastStep": 0.05},
    {"cutoff": 64, "viscousEpsilon": 0.0000625, "fastStep": 0.025},
]

EXPECTED_UPSTREAM_BINDINGS = [
    {
        "role": "primary selected finite kinetic evolution algorithm",
        "path": "research/r073l_adiabatic_diagnostic.py",
        "sha256": "68d3751a2b2eef3befcf92214bd8846fc4fcf8de22f6d89ceed647014642f824",
    },
    {
        "role": "independent midpoint matrix-exponential algorithm",
        "path": "experiments/r073l/independent_validate.py",
        "sha256": "f7ad15bbda05a965149888d3ddc3a4cc93d75ca8bbc1373d4ad2324105355a05",
    },
    {
        "role": "primary physical-velocity harmonic hierarchy algorithm",
        "path": "research/certificates/r073h/primary_diagnostic.py",
        "sha256": "c7e3d7709f4ebcf003a8d960827703ffe7fa6c8d41647e5104618959527a206f",
    },
    {
        "role": "independent vorticity FFT hierarchy algorithm",
        "path": "research/certificates/r073h/independent_validate.py",
        "sha256": "e91ccabaf5c39bc2e6c22bd1bac17536f5802fa83c74131abad5b0d7558212c8",
    },
    {
        "role": "sealed upstream harmonic and doubled-row certificate",
        "path": "research/certificates/r073h/certificate.json",
        "sha256": "d97ae98ef8309adfc109c33b857d3efe04a8b36b40d9fe8cc3b7a6b1e60c38f1",
    },
    {
        "role": "sealed upstream adiabatic finite package manifest",
        "path": "experiments/r073l/manifest.json",
        "sha256": "3c9171bd8e1fcb7e59fdf4358862c124c8694616a25d9b0143b7636b12051e1a",
    },
]

EXPECTED_OUTPUT_SCHEMA = {
    "caseScalars": [
        {"path": "linear.finiteInviscidActionProxy", "dtype": "float64",
         "shape": [], "normalization": "integral_0^D lambda_(N,0)(d) dd"},
        {"path": "linear.finiteViscousAction", "dtype": "float64",
         "shape": [], "normalization": "integral_0^D lambda_(N,epsilon)(d) dd"},
        {"path": "hierarchy.actualPhysicalLinearGain", "dtype": "float64",
         "shape": [], "normalization": "G_(N,epsilon)=norm(V1(D))_L2"},
        {"path": "finiteInviscidActionPrefactor", "dtype": "float64",
         "shape": [], "normalization": "G_(N,epsilon)*exp(-A_(N,0)/epsilon)"},
        {"path": "hierarchy.aEndpointL2", "dtype": "float64",
         "shape": [], "normalization": "norm(V1/G)_L2"},
        {"path": "hierarchy.bEndpointL2", "dtype": "float64",
         "shape": [], "normalization": "norm(V2/G^2)_L2"},
        {"path": "hierarchy.cTargetEndpointL2", "dtype": "float64",
         "shape": [], "normalization": "norm(Pi_(Kz=+-1)V3/G^3)_L2"},
        {"path": "hierarchy.cTotalSignedParallel", "dtype": "float64",
         "shape": [], "normalization": "Re inner(V1,Pi_(Kz=+-1)V3)/G^4"},
    ],
    "coefficientArchive": {
        "file": "coefficient_endpoints.npz", "dtype": "complex128",
        "shape": [5, 7, "2*N+1", 2],
        "normalization": "raw endpoint physical-velocity Taylor coefficient paths",
        "stateOrder": [
            "V1", "V2_Kz0", "V2_KzPlusMinus2",
            "V3_via_Kz0", "V3_via_KzPlusMinus2",
        ],
    },
    "thirdOrderTargetDiagnostics": {
        "rhoValues": [0.02, 0.05],
        "delta": "rho*finiteInviscidActionPrefactor",
        "target": "delta*a+delta^3*Pi_(Kz=+-1)c",
        "dtype": "float64", "diagnosticOnly": True,
    },
}


class DiagnosticFailure(RuntimeError):
    """Fail-closed numerical or provenance error."""


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
for name in (
    "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "VECLIB_MAXIMUM_THREADS",
    "MKL_NUM_THREADS",
):
    os.environ[name] = "1"
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
import scipy  # noqa: E402
from scipy.integrate import solve_ivp  # noqa: E402
from scipy.interpolate import CubicSpline  # noqa: E402
from scipy.linalg import eig  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DiagnosticFailure(message)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=False, allow_nan=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    require(path.is_file() and not path.is_symlink(), f"not a regular file: {path}")
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, value: object) -> None:
    atomic_text(path, canonical(value))


class Monitor:
    def __init__(self, progress: Path, resources: Path) -> None:
        self.progress = progress
        self.resources = resources
        for path in (progress, resources):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    def emit(self, event: str, **fields: object) -> None:
        row = {
            "event": event,
            "timestampUtc": now(),
            "elapsedSeconds": time.monotonic() - START,
            **fields,
        }
        line = json.dumps(row, sort_keys=True, allow_nan=False)
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(line + "\n")
        print(line, flush=True)

    def sample(self, event: str, **fields: object) -> None:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        try:
            load = list(os.getloadavg())
        except OSError:
            load = None
        row = {
            "event": event,
            "timestampUtc": now(),
            "elapsedSeconds": time.monotonic() - START,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetSizePlatformUnits": usage.ru_maxrss,
            "loadAverage": load,
            **fields,
        }
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")


def source_gate(source_commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
            "formal run requires a full lowercase source commit")
    resolved = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{source_commit}^{{commit}}"],
        text=True,
    ).strip()
    require(resolved == source_commit, "source commit did not resolve exactly")
    head = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True,
    ).strip()
    require(subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", source_commit, head],
        check=False,
    ).returncode == 0, "source commit is not an ancestor of HEAD")
    rows = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        committed = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{source_commit}:{relative}"],
        )
        require(committed == path.read_bytes(),
                f"working source differs from source commit: {relative}")
        rows.append(binding(path, ROOT))
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtRun": head,
        "allSourceBlobsMatch": True,
        "bindings": rows,
    }


def verify_upstream(config: Mapping[str, Any]) -> list[dict[str, object]]:
    rows = []
    for expected in config["upstreamBindings"]:
        path = ROOT / str(expected["path"])
        require(path.is_file() and not path.is_symlink(),
                f"upstream source is absent: {path}")
        actual = sha256(path)
        require(actual == expected["sha256"],
                f"upstream hash drift: {expected['path']}")
        rows.append({
            "role": expected["role"],
            "path": expected["path"],
            "bytes": path.stat().st_size,
            "sha256": actual,
        })
    return rows


def validate_config(config: Mapping[str, Any]) -> None:
    require(list(config) == [
        "schemaVersion", "release", "evidenceClass", "diagnosticOnly", "gamma",
        "profileTimeEnd", "physicalTimeEnd", "profileToPhysicalTimeRule",
        "exactRationals", "cutoffs", "viscousEpsilons", "fixedContour",
        "actionSampleCount", "primaryLinearSolver", "hierarchy", "displayRhos",
        "independentLinear", "independentHierarchy", "tolerances",
        "upstreamBindings", "claimBoundary", "outputSchema",
    ], "configuration top-level key set or order drifted")
    require(config.get("schemaVersion") == "r073m-prescribed-action-finite-config-v1",
            "configuration schema mismatch")
    require(config.get("release") == "R0.73M"
            and config.get("evidenceClass")
            == "finite-binary64-prescribed-action-and-harmonic-diagnostic-only"
            and config.get("diagnosticOnly") is True,
            "release, evidence class, or diagnostic boundary mismatch")
    require(float(config["gamma"]) == 0.5, "gamma must be 1/2")
    require(float(config["profileTimeEnd"]) == 1.0 / 450.0,
            "profile endpoint must be 1/450")
    require(float(config["physicalTimeEnd"]) == 1.0 / 1800.0,
            "physical endpoint must be 1/1800")
    require(config["profileToPhysicalTimeRule"] == "d=4t",
            "profile-to-physical time rule drift")
    require(config.get("exactRationals") == EXPECTED_EXACT_RATIONALS,
            "exact rational configuration drift")
    require([int(x) for x in config["cutoffs"]] == [40, 48, 64],
            "formal cutoffs changed")
    require([float(x) for x in config["viscousEpsilons"]] ==
            [0.001, 0.0005, 0.00025, 0.000125, 0.0000625],
            "formal epsilon grid changed")
    require(int(config["actionSampleCount"]) == 65,
            "formal action sample count changed")
    require(config.get("fixedContour") == {
        "centerReal": 0.17, "centerImag": 0.0, "radius": 0.003,
    }, "fixed contour changed")
    require(config.get("primaryLinearSolver") == {
        "method": "DOP853", "rtol": 1e-10, "atol": 1e-12,
        "maxStep": 1.0 / 115200.0,
    }, "primary linear solver contract changed")
    require(config.get("hierarchy") == {
        "profileTimeSnapshots": [0.0, 1.0 / 450.0],
        "primaryFastStep": 0.05,
        "stepConvergence": {
            "cutoff": 64,
            "viscousEpsilons": [0.001, 0.0000625],
            "fastSteps": [0.1, 0.05, 0.025],
        },
    }, "hierarchy solver or convergence grid changed")
    require(config.get("displayRhos") == [0.02, 0.05],
            "display rho grid changed")
    require(config.get("independentLinear") == {
        "stepCounts": [256, 512], "sentinels": EXPECTED_LINEAR_SENTINELS,
    }, "independent linear grid changed")
    require(config.get("independentHierarchy") == {
        "sentinels": EXPECTED_HIERARCHY_SENTINELS,
    }, "independent hierarchy grid changed")
    require(list(config.get("tolerances", {}).items())
            == list(EXPECTED_TOLERANCES.items()),
            "tolerance key set, order, or value changed")
    require(config.get("upstreamBindings") == EXPECTED_UPSTREAM_BINDINGS,
            "upstream role, path, hash, set, or order changed")
    require(list(config.get("claimBoundary", {}).items())
            == list(EXPECTED_CLAIM_BOUNDARY.items()),
            "claim boundary key set, order, spelling, or values drifted")
    schema = config.get("outputSchema")
    require(schema == EXPECTED_OUTPUT_SCHEMA, "exact outputSchema object drift")
    expected_paths = [
        "linear.finiteInviscidActionProxy", "linear.finiteViscousAction",
        "hierarchy.actualPhysicalLinearGain", "finiteInviscidActionPrefactor",
        "hierarchy.aEndpointL2", "hierarchy.bEndpointL2",
        "hierarchy.cTargetEndpointL2", "hierarchy.cTotalSignedParallel",
    ]
    require([row.get("path") for row in schema.get("caseScalars", [])]
            == expected_paths, "outputSchema scalar field order drift")
    require(all(row.get("dtype") == "float64" and row.get("shape") == []
                and isinstance(row.get("normalization"), str)
                for row in schema["caseScalars"]),
            "outputSchema scalar dtype, shape, or normalization drift")
    archive = schema.get("coefficientArchive", {})
    require(archive.get("file") == "coefficient_endpoints.npz"
            and archive.get("dtype") == "complex128"
            and archive.get("shape") == [5, 7, "2*N+1", 2]
            and archive.get("stateOrder") == [
                "V1", "V2_Kz0", "V2_KzPlusMinus2",
                "V3_via_Kz0", "V3_via_KzPlusMinus2",
            ], "outputSchema coefficient archive drift")
    target = schema.get("thirdOrderTargetDiagnostics", {})
    require(target.get("rhoValues") == [0.02, 0.05]
            and target.get("delta") == "rho*finiteInviscidActionPrefactor"
            and target.get("target") == "delta*a+delta^3*Pi_(Kz=+-1)c"
            and target.get("dtype") == "float64"
            and target.get("diagnosticOnly") is True,
            "outputSchema third-order display contract drift")


def smoke_config(config: Mapping[str, Any]) -> dict[str, Any]:
    value = json.loads(json.dumps(config))
    value["cutoffs"] = [8, 10]
    value["viscousEpsilons"] = [0.001, 0.0005]
    value["actionSampleCount"] = 9
    value["primaryLinearSolver"]["maxStep"] = 1.0 / 3600.0
    value["hierarchy"]["primaryFastStep"] = 0.2
    value["hierarchy"]["stepConvergence"] = {
        "cutoff": 10,
        "viscousEpsilons": [0.001],
        "fastSteps": [0.4, 0.2, 0.1],
    }
    value["independentLinear"] = {
        "stepCounts": [8, 16],
        "sentinels": [
            {"cutoff": 8, "viscousEpsilon": 0.001},
            {"cutoff": 10, "viscousEpsilon": 0.0005},
        ],
    }
    value["independentHierarchy"] = {
        "sentinels": [
            {"cutoff": 8, "viscousEpsilon": 0.001, "fastStep": 0.1},
            {"cutoff": 10, "viscousEpsilon": 0.0005, "fastStep": 0.1},
        ]
    }
    # Smoke checks structure and the independent paths, not formal accuracy.
    value["tolerances"].update({
        "physicalKineticGainRelative": 5e-4,
        "largestCutoffActionProxyAbsolute": 1e-7,
        "largestCutoffPrefactorAbsolute": 1e-4,
        "hierarchyFinestCutoffRelative": 2e-3,
        "hierarchyStepRelative": 2e-3,
        "independentLinearActionRelative": 2e-3,
        "independentLinearGainRelative": 2e-3,
        "independentLinearPrefactorAbsolute": 2e-3,
        "independentLinearRefinement": 2e-3,
        "independentHierarchyCoefficientRelative": 2e-3,
        "outerThreeMassFraction": 0.1,
    })
    return value


def prepare_output(output: Path, overwrite: bool, smoke: bool) -> None:
    output = output.resolve()
    if smoke:
        require(not output.is_relative_to(HERE.resolve()),
                "smoke output must be outside the formal package")
    else:
        require(output == HERE.resolve(), "formal output must use the canonical package")
        require(ARGS.config.resolve() == (HERE / "config.json").resolve(),
                "formal run must use the canonical config")
    output.mkdir(parents=True, exist_ok=True)
    existing = [output / name for name in GENERATED if (output / name).exists()]
    require(not existing or overwrite,
            "refusing to overwrite generated primary files without --overwrite")
    for path in existing:
        path.unlink()


def recurrence_kinetic_matrix(
    cutoff: int, d_value: float, epsilon: float, gamma: float,
) -> np.ndarray:
    mu = gamma * gamma
    raw = np.zeros((2 * cutoff + 1, 2 * cutoff + 1), dtype=np.complex128)
    first_scale = math.exp(-d_value)
    second_scale = math.exp(-4.0 * d_value)
    for column, n_mode in enumerate(range(-cutoff, cutoff + 1)):
        ell = n_mode * n_mode + mu
        first = gamma * first_scale * 0.25 * (1.0 - 1.0 / ell)
        second = gamma * second_scale * (-0.125 + 0.5 / ell)
        for shift, coefficient in (
            (1, first), (-1, -first), (2, second), (-2, -second),
        ):
            target = n_mode + shift
            if -cutoff <= target <= cutoff:
                raw[target + cutoff, column] = coefficient
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    ell = modes * modes + mu
    matrix = ((1.0 / np.sqrt(ell))[:, None] * raw * np.sqrt(ell)[None, :])
    return matrix - epsilon * np.diag(ell)


def phase_anchor(vector: np.ndarray, cutoff: int, gamma: float) -> complex:
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    ell = modes * modes + gamma * gamma
    return complex(0.5 * np.sum(vector / np.sqrt(ell)))


def selected_state(
    matrix: np.ndarray, cutoff: int, gamma: float, center: complex, radius: float,
    canonical_phase: bool = False,
) -> dict[str, Any]:
    values, left, right = eig(matrix, left=True, right=True, check_finite=False)
    inside = np.flatnonzero(np.abs(values - center) < radius)
    require(inside.size == 1, f"fixed-contour count is {inside.size}, not one")
    index = int(inside[0])
    value = complex(values[index])
    lvec = np.asarray(left[:, index], dtype=np.complex128)
    rvec = np.asarray(right[:, index], dtype=np.complex128)
    lvec /= np.linalg.norm(lvec)
    rvec /= np.linalg.norm(rvec)
    anchor = phase_anchor(rvec, cutoff, gamma)
    if canonical_phase:
        require(abs(anchor) > 1e-12, "finite phase anchor vanished")
        rvec *= np.exp(-1j * np.angle(anchor))
        anchor = phase_anchor(rvec, cutoff, gamma)
        if anchor.real < 0.0:
            rvec *= -1.0
            anchor = -anchor
    pairing = complex(np.vdot(lvec, rvec))
    require(abs(pairing) > 1e-12, "selected eigenpair is numerically defective")
    residual = float(np.linalg.norm(matrix @ rvec - value * rvec)
                     / max(1.0, np.linalg.norm(matrix), abs(value)))
    return {
        "lambda": value,
        "left": lvec,
        "right": rvec,
        "pairing": pairing,
        "overlap": float(abs(pairing)),
        "anchor": anchor,
        "residual": residual,
        "contourCount": int(inside.size),
    }


def project(state: Mapping[str, Any], vector: np.ndarray) -> np.ndarray:
    return state["right"] * (np.vdot(state["left"], vector) / state["pairing"])


class FastMatrixAction:
    def __init__(self, cutoff: int, epsilon: float, gamma: float) -> None:
        self.cutoff = cutoff
        self.epsilon = epsilon
        modes = np.arange(-cutoff, cutoff + 1, dtype=float)
        self.ell = modes * modes + gamma * gamma
        self.sqrt_ell = np.sqrt(self.ell)
        self.first = gamma * 0.25 * (1.0 - 1.0 / self.ell)
        self.second = gamma * (-0.125 + 0.5 / self.ell)

    def __call__(self, d_value: float, vector: np.ndarray) -> np.ndarray:
        weighted = self.sqrt_ell * vector
        raw = np.zeros_like(weighted)
        first = math.exp(-d_value) * self.first
        second = math.exp(-4.0 * d_value) * self.second
        raw[1:] += first[:-1] * weighted[:-1]
        raw[:-1] -= first[1:] * weighted[1:]
        raw[2:] += second[:-2] * weighted[:-2]
        raw[:-2] -= second[2:] * weighted[2:]
        return raw / self.sqrt_ell - self.epsilon * self.ell * vector


def spline_integral(grid: np.ndarray, values: np.ndarray) -> tuple[np.ndarray, float]:
    spline = CubicSpline(grid, values)
    primitive = spline.antiderivative()
    cumulative = primitive(grid) - primitive(grid[0])
    return np.asarray(cumulative, dtype=float), float(cumulative[-1])


def linear_case(
    monitor: Monitor, config: Mapping[str, Any], cutoff: int, epsilon: float,
    d_grid: np.ndarray, inviscid_states: list[dict[str, Any]],
    inviscid_cumulative: np.ndarray, inviscid_action: float,
) -> tuple[dict[str, Any], list[dict[str, object]], np.ndarray]:
    gamma = float(config["gamma"])
    contour = config["fixedContour"]
    center = complex(float(contour["centerReal"]), float(contour["centerImag"]))
    radius = float(contour["radius"])
    states = [selected_state(
        recurrence_kinetic_matrix(cutoff, float(d), epsilon, gamma),
        cutoff, gamma, center, radius, canonical_phase=(index == 0),
    ) for index, d in enumerate(d_grid)]
    lambdas = np.array([state["lambda"].real for state in states], dtype=float)
    viscous_cumulative, viscous_action = spline_integral(d_grid, lambdas)
    initial = states[0]["right"].copy()
    initial /= np.linalg.norm(initial)
    action = FastMatrixAction(cutoff, epsilon, gamma)

    def rhs(d_value: float, vector: np.ndarray) -> np.ndarray:
        return action(d_value, vector) / epsilon

    solver_config = config["primaryLinearSolver"]
    solution = solve_ivp(
        rhs, (0.0, float(d_grid[-1])), initial,
        method=str(solver_config["method"]), t_eval=d_grid,
        rtol=float(solver_config["rtol"]), atol=float(solver_config["atol"]),
        max_step=float(solver_config["maxStep"]),
    )
    require(solution.success, f"linear solve failed: {solution.message}")
    terminal = np.asarray(solution.y[:, -1], dtype=np.complex128)
    selected = project(states[-1], terminal)
    complement = terminal - selected
    gain = float(np.linalg.norm(terminal))
    rows = []
    for index, d_value in enumerate(d_grid):
        rows.extend((
            {
                "branch": "inviscid", "N": cutoff, "epsilon": 0.0,
                "sampleIndex": index, "d": float(d_value),
                "lambda": float(inviscid_states[index]["lambda"].real),
                "lambdaImaginary": float(inviscid_states[index]["lambda"].imag),
                "cumulativeAction": float(inviscid_cumulative[index]),
                "fixedContourCount": int(inviscid_states[index]["contourCount"]),
                "phaseAnchorAbs": float(abs(inviscid_states[index]["anchor"])),
                "eigenResidualRelative": float(inviscid_states[index]["residual"]),
                "finiteCompressionOnly": True,
            },
            {
                "branch": "viscous", "N": cutoff, "epsilon": epsilon,
                "sampleIndex": index, "d": float(d_value),
                "lambda": float(lambdas[index]),
                "lambdaImaginary": float(states[index]["lambda"].imag),
                "cumulativeAction": float(viscous_cumulative[index]),
                "fixedContourCount": int(states[index]["contourCount"]),
                "phaseAnchorAbs": float(abs(states[index]["anchor"])),
                "eigenResidualRelative": float(states[index]["residual"]),
                "finiteCompressionOnly": True,
            },
        ))
    result = {
        "N": cutoff,
        "epsilon": epsilon,
        "dimension": 2 * cutoff + 1,
        "finiteInviscidActionProxy": inviscid_action,
        "finiteViscousAction": viscous_action,
        "finiteInviscidExponent": inviscid_action / epsilon,
        "finiteViscousExponent": viscous_action / epsilon,
        "kineticGain": gain,
        "kineticGainNormalizedByFiniteInviscidAction": (
            gain * math.exp(-inviscid_action / epsilon)
        ),
        "kineticGainNormalizedByFiniteViscousAction": (
            gain * math.exp(-viscous_action / epsilon)
        ),
        "terminalSelectedNorm": float(np.linalg.norm(selected)),
        "terminalComplementNorm": float(np.linalg.norm(complement)),
        "terminalComplementToSelectedRatio": float(
            np.linalg.norm(complement) / max(np.linalg.norm(selected), 1e-300)
        ),
        "maximumSelectedEigenvalueImaginaryAbs": max(
            abs(state["lambda"].imag) for state in states + inviscid_states
        ),
        "maximumEigenResidualRelative": max(
            state["residual"] for state in states + inviscid_states
        ),
        "minimumLeftRightOverlap": min(state["overlap"] for state in states),
        "initialPhaseAnchor": {
            "real": float(states[0]["anchor"].real),
            "imag": float(states[0]["anchor"].imag),
        },
        "solver": {
            "success": bool(solution.success),
            "nfev": int(solution.nfev),
            "message": solution.message,
        },
        "finiteCompressionOnly": True,
    }
    monitor.emit("linear-case-complete", N=cutoff, epsilon=epsilon,
                 gain=gain, finiteInviscidActionProxy=inviscid_action,
                 finiteInviscidPrefactor=result[
                     "kineticGainNormalizedByFiniteInviscidAction"
                 ])
    return result, rows, initial


class FourierVelocity:
    def __init__(self, cutoff: int) -> None:
        self.cutoff = cutoff
        self.n = np.arange(-cutoff, cutoff + 1, dtype=int)
        self.ky = 2.0 * self.n
        self.kz = np.arange(-KZ_MAX, KZ_MAX + 1, dtype=int)

    def zeros(self) -> np.ndarray:
        return np.zeros((len(self.kz), len(self.n), 2), dtype=np.complex128)

    def background(self, absolute_lambda: float, d_value: float) -> np.ndarray:
        value = self.zeros()
        center = KZ_MAX
        coefficients = {
            1: 0.5j * absolute_lambda * math.exp(-d_value),
            -1: -0.5j * absolute_lambda * math.exp(-d_value),
            2: -0.25j * absolute_lambda * math.exp(-4.0 * d_value),
            -2: 0.25j * absolute_lambda * math.exp(-4.0 * d_value),
        }
        for n_mode, coefficient in coefficients.items():
            if -self.cutoff <= n_mode <= self.cutoff:
                value[center, n_mode + self.cutoff, 1] = coefficient
        return value

    def project(self, field: np.ndarray) -> np.ndarray:
        output = np.asarray(field, dtype=np.complex128).copy()
        for index, kz in enumerate(self.kz):
            square = self.ky * self.ky + float(kz * kz)
            nonzero = square > 0.0
            dot = self.ky * output[index, :, 0] + float(kz) * output[index, :, 1]
            output[index, nonzero, 0] -= self.ky[nonzero] * dot[nonzero] / square[nonzero]
            output[index, nonzero, 1] -= float(kz) * dot[nonzero] / square[nonzero]
        return output

    def bilinear(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        raw = self.zeros()
        length = len(self.n)
        start = self.cutoff
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

    def linear(self, field: np.ndarray, absolute_lambda: float,
               d_value: float) -> np.ndarray:
        background = self.background(absolute_lambda, d_value)
        laplacian = -(self.ky[None, :] ** 2 + self.kz[:, None] ** 2)
        return (
            laplacian[:, :, None] * field
            - self.bilinear(background, field)
            - self.bilinear(field, background)
        )

    def unit_real_launch(self, kinetic: np.ndarray) -> np.ndarray:
        profile = kinetic / (2.0 * np.sqrt(self.n.astype(float) ** 2 + 0.25))
        result = self.zeros()
        plus = KZ_MAX + 1
        minus = KZ_MAX - 1
        result[plus, :, 0] = profile
        result[plus, :, 1] = -2.0 * self.n * profile
        for index, n_mode in enumerate(self.n):
            reflected = -int(n_mode) + self.cutoff
            result[minus, reflected] = np.conjugate(result[plus, index])
        result /= math.sqrt(2.0)
        return result

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
                reflected_n = -int(n_mode) + self.cutoff
                difference = (
                    field[reflected_kz, reflected_n]
                    - np.conjugate(field[kz_index, index])
                )
                maximum = max(maximum, float(np.max(np.abs(difference))))
        return maximum / scale

    def outer_three_fraction(self, field: np.ndarray) -> float:
        total = float(np.vdot(field, field).real)
        outer = np.abs(self.n) >= self.cutoff - 2
        return float(np.sum(np.abs(field[:, outer]) ** 2) / max(total, 1e-300))


def norm(value: np.ndarray) -> float:
    require(bool(np.isfinite(value).all()), "nonfinite coefficient array")
    squared = float(np.vdot(value, value).real)
    require(math.isfinite(squared) and squared >= -1e-14,
            "nonfinite or materially negative squared norm")
    return math.sqrt(max(0.0, squared))


def forbidden_parity_relative(state: np.ndarray) -> float:
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


def hierarchy_metrics(space: FourierVelocity, state: np.ndarray) -> dict[str, float]:
    first, second0, second2, third0, third2 = state
    second = second0 + second2
    third = third0 + third2
    first_target = first[[KZ_MAX - 1, KZ_MAX + 1]]
    second_target = second[[KZ_MAX - 1, KZ_MAX + 1]]
    third0_target = third0[[KZ_MAX - 1, KZ_MAX + 1]]
    third2_target = third2[[KZ_MAX - 1, KZ_MAX + 1]]
    third_target = third0_target + third2_target
    third_triple = third[[KZ_MAX - 3, KZ_MAX + 3]]
    gain = norm(first_target)
    gain2 = gain * gain
    gain3 = gain2 * gain
    gain4 = gain2 * gain2

    def signed(value: np.ndarray) -> tuple[float, float]:
        inner = np.vdot(first_target, value)
        value_norm = norm(value)
        return (
            float(inner.real / max(gain4, 1e-300)),
            float(inner.real / max(gain * value_norm, 1e-300)),
        )

    mean_signed, mean_cosine = signed(third0_target)
    doubled_signed, doubled_cosine = signed(third2_target)
    total_signed, total_cosine = signed(third_target)
    return {
        "actualPhysicalLinearGain": gain,
        "aEndpointL2": norm(first_target / gain),
        "bEndpointL2": norm(second) / max(gain2, 1e-300),
        "bTargetEndpointL2": norm(second_target) / max(gain2, 1e-300),
        "bMeanEndpointL2": norm(second0) / max(gain2, 1e-300),
        "bDoubleEndpointL2": norm(second2) / max(gain2, 1e-300),
        "cEndpointL2": norm(third) / max(gain3, 1e-300),
        "cTargetEndpointL2": norm(third_target) / max(gain3, 1e-300),
        "cTripleEndpointL2": norm(third_triple) / max(gain3, 1e-300),
        "cMeanPathTargetEndpointL2": norm(third0_target) / max(gain3, 1e-300),
        "cDoublePathTargetEndpointL2": norm(third2_target) / max(gain3, 1e-300),
        "cMeanPathSignedParallel": mean_signed,
        "cDoublePathSignedParallel": doubled_signed,
        "cTotalSignedParallel": total_signed,
        "cMeanPathCosineWithA": mean_cosine,
        "cDoublePathCosineWithA": doubled_cosine,
        "cTotalCosineWithA": total_cosine,
        "v1OuterThreeMassFraction": space.outer_three_fraction(first),
        "v2OuterThreeMassFraction": space.outer_three_fraction(second),
        "v3OuterThreeMassFraction": space.outer_three_fraction(third),
        "maximumDivergenceRelative": max(
            space.divergence_relative(field) for field in state
        ),
        "maximumRealityRelative": max(space.reality_relative(field) for field in state),
        "forbiddenParityRelative": forbidden_parity_relative(state),
    }


def generator_defect(
    space: FourierVelocity, matrix: np.ndarray, kinetic: np.ndarray,
    absolute_lambda: float, d_value: float,
) -> float:
    real_launch = space.unit_real_launch(kinetic) * math.sqrt(2.0)
    positive = space.zeros()
    positive[KZ_MAX + 1] = real_launch[KZ_MAX + 1]
    derivative = space.linear(positive, absolute_lambda, d_value)
    du2_dt = derivative[KZ_MAX + 1, :, 0]
    dh_dtheta = (
        2.0 * np.sqrt(space.n.astype(float) ** 2 + 0.25) * du2_dt
        / (4.0 * absolute_lambda)
    )
    return float(np.linalg.norm(dh_dtheta - matrix @ kinetic)
                 / max(1.0, np.linalg.norm(matrix @ kinetic)))


def integrate_hierarchy(
    cutoff: int, epsilon: float, kinetic_launch: np.ndarray,
    d_end: float, fast_step: float,
) -> tuple[np.ndarray, dict[str, float], int]:
    space = FourierVelocity(cutoff)
    zero = space.zeros()
    state = np.stack((space.unit_real_launch(kinetic_launch), zero, zero, zero, zero))
    mask0 = np.zeros_like(zero)
    mask0[KZ_MAX] = 1.0
    mask2 = np.zeros_like(zero)
    mask2[KZ_MAX - 2] = 1.0
    mask2[KZ_MAX + 2] = 1.0
    initial_norm = norm(state[0])
    require(abs(initial_norm - 1.0) <= 2e-12, "physical real launch is not unit norm")

    def rhs(theta: float, values: np.ndarray) -> np.ndarray:
        one, two0, two2, three0, three2 = values
        d_value = epsilon * theta
        factor = epsilon / 4.0
        absolute_lambda = 1.0 / epsilon
        quadratic = space.bilinear(one, one)
        return factor * np.stack((
            space.linear(one, absolute_lambda, d_value),
            space.linear(two0, absolute_lambda, d_value) - mask0 * quadratic,
            space.linear(two2, absolute_lambda, d_value) - mask2 * quadratic,
            space.linear(three0, absolute_lambda, d_value)
            - space.bilinear(one, two0) - space.bilinear(two0, one),
            space.linear(three2, absolute_lambda, d_value)
            - space.bilinear(one, two2) - space.bilinear(two2, one),
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
    require(bool(np.isfinite(state).all()),
            "nonfinite raw hierarchy coefficient before diagnostics")
    return state, hierarchy_metrics(space, state), steps


def relative_change(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1e-300)


def require_finite_tree(value: object, label: str = "result") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            require_finite_tree(child, f"{label}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            require_finite_tree(child, f"{label}[{index}]")
    elif isinstance(value, (float, np.floating)):
        require(math.isfinite(float(value)), f"nonfinite scalar: {label}")
    elif isinstance(value, (complex, np.complexfloating)):
        require(math.isfinite(float(np.real(value)))
                and math.isfinite(float(np.imag(value))),
                f"nonfinite complex scalar: {label}")


def hierarchy_comparison(left: Mapping[str, float],
                         right: Mapping[str, float]) -> dict[str, float]:
    fields = (
        "actualPhysicalLinearGain", "bEndpointL2", "cTargetEndpointL2",
        "cTripleEndpointL2", "cTotalSignedParallel",
    )
    result = {
        field: relative_change(float(left[field]), float(right[field]))
        for field in fields
    }
    result["maximumRelativeChange"] = max(result.values())
    return result


def write_csv(path: Path, fields: Iterable[str], rows: list[Mapping[str, object]]) -> None:
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


def write_npz(path: Path, arrays: Mapping[str, np.ndarray]) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for name in sorted(arrays):
            buffer = io.BytesIO()
            np.lib.format.write_array(
                buffer, np.ascontiguousarray(arrays[name]), allow_pickle=False,
            )
            info = zipfile.ZipInfo(f"{name}.npy", (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, buffer.getvalue(), compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)
    os.replace(temporary, path)


def archive_key(cutoff: int, epsilon: float) -> str:
    encoded = format(epsilon, ".8e").replace("+", "p").replace("-", "m").replace(".", "p")
    return f"N{cutoff}_epsilon_{encoded}"


def environment_payload(config_path: Path, source: Mapping[str, object],
                        upstream: list[dict[str, object]], smoke: bool) -> dict[str, object]:
    return {
        "schemaVersion": "r073m-primary-environment-v1",
        "createdUtc": now(),
        "python": sys.version,
        "pythonImplementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "logicalCpuCount": os.cpu_count(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "configuration": binding(config_path.resolve(), ROOT),
        "sourceProvenance": source,
        "upstreamBindings": upstream,
        "smokeMode": smoke,
        "threadEnvironment": {
            key: os.environ.get(key) for key in (
                "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS",
            )
        },
    }


def main() -> int:
    output = ARGS.output_dir.resolve()
    config_full = json.loads(ARGS.config.read_text(encoding="utf-8"))
    require(sha256(ARGS.config.resolve()) == EXPECTED_CONFIG_SHA256,
            "canonical configuration byte contract drift")
    validate_config(config_full)
    config = smoke_config(config_full) if ARGS.smoke else config_full
    provenance = source_gate(ARGS.source_commit, ARGS.smoke)
    upstream = verify_upstream(config_full)
    # No output is created or removed before every immutable scientific and
    # provenance gate above has succeeded.
    prepare_output(output, ARGS.overwrite, ARGS.smoke)
    monitor = Monitor(output / "primary_progress.ndjson",
                      output / "primary_resources.ndjson")
    monitor.emit("start", smokeMode=ARGS.smoke,
                 profileTimeEnd=config["profileTimeEnd"],
                 physicalTimeEnd=config["physicalTimeEnd"],
                 profileToPhysicalTimeRule="d=4t")
    monitor.sample("start")

    cutoffs = [int(value) for value in config["cutoffs"]]
    epsilons = [float(value) for value in config["viscousEpsilons"]]
    d_end = float(config["profileTimeEnd"])
    d_grid = np.linspace(0.0, d_end, int(config["actionSampleCount"]))
    gamma = float(config["gamma"])
    contour = config["fixedContour"]
    center = complex(float(contour["centerReal"]), float(contour["centerImag"]))
    radius = float(contour["radius"])
    tolerance = config["tolerances"]

    cases: list[dict[str, Any]] = []
    action_rows: list[dict[str, object]] = []
    raw_arrays: dict[str, np.ndarray] = {}
    launch_vectors: dict[tuple[int, float], np.ndarray] = {}
    for cutoff in cutoffs:
        monitor.emit("cutoff-start", N=cutoff)
        inviscid_states = [selected_state(
            recurrence_kinetic_matrix(cutoff, float(d), 0.0, gamma),
            cutoff, gamma, center, radius, canonical_phase=(index == 0),
        ) for index, d in enumerate(d_grid)]
        inviscid_lambdas = np.array(
            [state["lambda"].real for state in inviscid_states], dtype=float,
        )
        inviscid_cumulative, inviscid_action = spline_integral(
            d_grid, inviscid_lambdas,
        )
        # Store the inviscid branch once per cutoff.
        action_rows.extend({
            "branch": "inviscid", "N": cutoff, "epsilon": 0.0,
            "sampleIndex": index, "d": float(d),
            "lambda": float(inviscid_lambdas[index]),
            "lambdaImaginary": float(inviscid_states[index]["lambda"].imag),
            "cumulativeAction": float(inviscid_cumulative[index]),
            "fixedContourCount": int(inviscid_states[index]["contourCount"]),
            "phaseAnchorAbs": float(abs(inviscid_states[index]["anchor"])),
            "eigenResidualRelative": float(inviscid_states[index]["residual"]),
            "finiteCompressionOnly": True,
        } for index, d in enumerate(d_grid))
        for epsilon in epsilons:
            monitor.emit("case-start", N=cutoff, epsilon=epsilon)
            linear, rows, launch = linear_case(
                monitor, config, cutoff, epsilon, d_grid,
                inviscid_states, inviscid_cumulative, inviscid_action,
            )
            # linear_case returns duplicate inviscid rows for convenience;
            # preserve only its viscous rows because the shared inviscid rows
            # were emitted above.
            action_rows.extend(row for row in rows if row["branch"] == "viscous")
            launch_vectors[(cutoff, epsilon)] = launch
            state, hierarchy, steps = integrate_hierarchy(
                cutoff, epsilon, launch, d_end,
                float(config["hierarchy"]["primaryFastStep"]),
            )
            generator_samples = []
            for generator_d in (0.0, d_end / 2.0, d_end):
                generator_matrix = recurrence_kinetic_matrix(
                    cutoff, generator_d, epsilon, gamma,
                )
                generator_samples.append({
                    "d": generator_d,
                    "relativeDefect": generator_defect(
                        FourierVelocity(cutoff), generator_matrix, launch,
                        1.0 / epsilon, generator_d,
                    ),
                })
            defect = max(row["relativeDefect"] for row in generator_samples)
            physical_gain = float(hierarchy["actualPhysicalLinearGain"])
            kinetic_gain = float(linear["kineticGain"])
            gain_difference = abs(physical_gain - kinetic_gain) / max(
                physical_gain, kinetic_gain, 1e-300,
            )
            prefactor = physical_gain * math.exp(-inviscid_action / epsilon)
            viscous_normalized = physical_gain * math.exp(
                -float(linear["finiteViscousAction"]) / epsilon
            )
            key = archive_key(cutoff, epsilon)
            raw_arrays[key] = state
            case = {
                "N": cutoff,
                "epsilon": epsilon,
                "archiveKey": key,
                "profileTimeEnd": d_end,
                "physicalTimeEnd": d_end / 4.0,
                "profileToPhysicalTimeRule": "d=4t",
                "linear": linear,
                "hierarchy": hierarchy,
                "hierarchyFastStep": float(config["hierarchy"]["primaryFastStep"]),
                "hierarchyStepCount": steps,
                "generatorRelativeDefect": defect,
                "generatorRelativeDefectSamples": generator_samples,
                "physicalKineticGainRelativeDifference": gain_difference,
                "finiteInviscidActionPrefactor": prefactor,
                "finiteViscousActionNormalizedPhysicalGain": viscous_normalized,
                "effectiveTaylorAmplitudePerRho": prefactor,
                "thirdOrderTargetDiagnostics": [],
                "normalization": {
                    "a": "V1/actualPhysicalLinearGain",
                    "b": "V2/actualPhysicalLinearGain^2",
                    "c": "V3/actualPhysicalLinearGain^3",
                },
                "claimBoundary": config_full["claimBoundary"],
            }
            first, _, _, third0, third2 = state
            first_target = first[[KZ_MAX - 1, KZ_MAX + 1]] / physical_gain
            third_target = (
                third0[[KZ_MAX - 1, KZ_MAX + 1]]
                + third2[[KZ_MAX - 1, KZ_MAX + 1]]
            ) / (physical_gain ** 3)
            for rho in [float(value) for value in config["displayRhos"]]:
                delta = rho * prefactor
                target = delta * first_target + delta ** 3 * third_target
                case["thirdOrderTargetDiagnostics"].append({
                    "rho": rho,
                    "delta": delta,
                    "targetRowL2": norm(target),
                    "diagnosticOnly": True,
                    "visualizationChoiceIsCertifiedContinuumTaylorRadius": False,
                    "fullNonlinearTrajectoryComputed": False,
                })
            cases.append(case)
            monitor.sample("case-complete", N=cutoff, epsilon=epsilon,
                           hierarchySteps=steps)
            monitor.emit("case-complete", N=cutoff, epsilon=epsilon,
                         physicalGain=physical_gain, kineticGain=kinetic_gain,
                         finiteInviscidActionPrefactor=prefactor,
                         physicalKineticGainRelativeDifference=gain_difference)
        monitor.emit("cutoff-complete", N=cutoff)

    cutoff_rows: list[dict[str, object]] = []
    for small, large in zip(cutoffs[:-1], cutoffs[1:]):
        for epsilon in epsilons:
            left = next(case for case in cases
                        if case["N"] == small and case["epsilon"] == epsilon)
            right = next(case for case in cases
                         if case["N"] == large and case["epsilon"] == epsilon)
            comparison = hierarchy_comparison(left["hierarchy"], right["hierarchy"])
            cutoff_rows.append({
                "smallN": small,
                "largeN": large,
                "epsilon": epsilon,
                "finiteInviscidActionProxyAbsoluteDifference": abs(
                    left["linear"]["finiteInviscidActionProxy"]
                    - right["linear"]["finiteInviscidActionProxy"]
                ),
                "finiteInviscidActionPrefactorAbsoluteDifference": abs(
                    left["finiteInviscidActionPrefactor"]
                    - right["finiteInviscidActionPrefactor"]
                ),
                "selectedObservableHierarchyMaximumRelativeDifference": comparison[
                    "maximumRelativeChange"
                ],
                "finiteCutoffAgreementIsTailProof": False,
            })

    step_rows: list[dict[str, object]] = []
    step_spec = config["hierarchy"]["stepConvergence"]
    step_cutoff = int(step_spec["cutoff"])
    primary_step = float(config["hierarchy"]["primaryFastStep"])
    for epsilon in [float(value) for value in step_spec["viscousEpsilons"]]:
        reference = next(case for case in cases
                         if case["N"] == step_cutoff and case["epsilon"] == epsilon)
        by_step: dict[float, Mapping[str, float]] = {
            primary_step: reference["hierarchy"]
        }
        for step in [float(value) for value in step_spec["fastSteps"]]:
            if step in by_step:
                continue
            monitor.emit("step-case-start", N=step_cutoff, epsilon=epsilon,
                         fastStep=step)
            _, metrics, count = integrate_hierarchy(
                step_cutoff, epsilon, launch_vectors[(step_cutoff, epsilon)],
                d_end, step,
            )
            by_step[step] = metrics
            monitor.emit("step-case-complete", N=step_cutoff, epsilon=epsilon,
                         fastStep=step, stepCount=count)
        ordered = sorted(by_step, reverse=True)
        for coarse, fine in zip(ordered, ordered[1:]):
            comparison = hierarchy_comparison(by_step[coarse], by_step[fine])
            step_rows.append({
                "N": step_cutoff,
                "epsilon": epsilon,
                "coarseFastStep": coarse,
                "fineFastStep": fine,
                "selectedObservableMaximumRelativeDifference": comparison[
                    "maximumRelativeChange"
                ],
            })

    largest_pair = [row for row in cutoff_rows
                    if row["smallN"] == cutoffs[-2] and row["largeN"] == cutoffs[-1]]
    maximums = {
        "selectedEigenvalueImaginaryAbs": max(
            case["linear"]["maximumSelectedEigenvalueImaginaryAbs"] for case in cases
        ),
        "eigenResidualRelative": max(
            case["linear"]["maximumEigenResidualRelative"] for case in cases
        ),
        "generatorRelativeDefect": max(case["generatorRelativeDefect"] for case in cases),
        "divergenceRelative": max(
            case["hierarchy"]["maximumDivergenceRelative"] for case in cases
        ),
        "realityRelative": max(
            case["hierarchy"]["maximumRealityRelative"] for case in cases
        ),
        "forbiddenParityRelative": max(
            case["hierarchy"]["forbiddenParityRelative"] for case in cases
        ),
        "physicalKineticGainRelative": max(
            case["physicalKineticGainRelativeDifference"] for case in cases
        ),
        "largestCutoffActionProxyAbsolute": max(
            row["finiteInviscidActionProxyAbsoluteDifference"] for row in largest_pair
        ),
        "largestCutoffPrefactorAbsolute": max(
            row["finiteInviscidActionPrefactorAbsoluteDifference"] for row in largest_pair
        ),
        "hierarchyFinestCutoffRelative": max(
            row["selectedObservableHierarchyMaximumRelativeDifference"]
            for row in largest_pair
        ),
        "hierarchyStepRelative": max(
            row["selectedObservableMaximumRelativeDifference"] for row in step_rows
        ),
        "aEndpointNormalizationAbsolute": max(
            abs(case["hierarchy"]["aEndpointL2"] - 1.0) for case in cases
        ),
        "outerThreeMassFraction": max(
            case["hierarchy"][field]
            for case in cases
            for field in (
                "v1OuterThreeMassFraction", "v2OuterThreeMassFraction",
                "v3OuterThreeMassFraction",
            )
        ),
        "minimumPhaseAnchorAbs": min(float(row["phaseAnchorAbs"])
                                      for row in action_rows),
    }
    checks = {
        "selectedEigenvalueNumericallyReal": (
            maximums["selectedEigenvalueImaginaryAbs"]
            <= float(tolerance["numericalReality"])
        ),
        "eigenResidualRelative": (
            maximums["eigenResidualRelative"]
            <= float(tolerance["eigenResidualRelative"])
        ),
        "generatorRelativeDefect": (
            maximums["generatorRelativeDefect"]
            <= float(tolerance["generatorRelative"])
        ),
        "divergenceRelative": (
            maximums["divergenceRelative"] <= float(tolerance["divergenceRelative"])
        ),
        "realityRelative": (
            maximums["realityRelative"] <= float(tolerance["realityRelative"])
        ),
        "forbiddenParityRelative": (
            maximums["forbiddenParityRelative"]
            <= float(tolerance["forbiddenParityRelative"])
        ),
        "physicalKineticGainRelative": (
            maximums["physicalKineticGainRelative"]
            <= float(tolerance["physicalKineticGainRelative"])
        ),
        "largestCutoffActionProxyAbsolute": (
            maximums["largestCutoffActionProxyAbsolute"]
            <= float(tolerance["largestCutoffActionProxyAbsolute"])
        ),
        "largestCutoffPrefactorAbsolute": (
            maximums["largestCutoffPrefactorAbsolute"]
            <= float(tolerance["largestCutoffPrefactorAbsolute"])
        ),
        "hierarchyFinestCutoffRelative": (
            maximums["hierarchyFinestCutoffRelative"]
            <= float(tolerance["hierarchyFinestCutoffRelative"])
        ),
        "hierarchyStepRelative": (
            maximums["hierarchyStepRelative"]
            <= float(tolerance["hierarchyStepRelative"])
        ),
        "aEndpointNormalizationAbsolute": (
            maximums["aEndpointNormalizationAbsolute"]
            <= float(tolerance["aEndpointNormalizationAbsolute"])
        ),
        "outerThreeMassFraction": (
            maximums["outerThreeMassFraction"]
            <= float(tolerance["outerThreeMassFraction"])
        ),
        "allPhaseAnchorsNonzero": maximums["minimumPhaseAnchorAbs"] > 1e-12,
        "allFixedContourCountsOne": all(
            int(row["fixedContourCount"]) == 1 for row in action_rows
        ),
    }
    checks.update({
        "allLinearSolversSucceeded": all(case["linear"]["solver"]["success"] for case in cases),
        "profileEndpointExact": d_end == 1.0 / 450.0,
        "physicalEndpointExact": d_end / 4.0 == 1.0 / 1800.0,
        "quadraticTargetRowsZero": all(
            case["hierarchy"]["bTargetEndpointL2"] <= 1e-13 for case in cases
        ),
        "aEndpointNormalizedByActualGain": (
            maximums["aEndpointNormalizationAbsolute"]
            <= float(tolerance["aEndpointNormalizationAbsolute"])
        ),
    })
    passed = bool(all(checks.values()))

    require_finite_tree(cases, "cases")
    require_finite_tree(action_rows, "actionRows")
    require_finite_tree(cutoff_rows, "cutoffRows")
    require_finite_tree(step_rows, "stepRows")
    require_finite_tree(maximums, "maximums")
    for key, array in raw_arrays.items():
        require(bool(np.isfinite(array).all()),
                f"nonfinite coefficient archive array: {key}")

    rows_path = output / "primary_rows.csv"
    action_path = output / "action_nodes.csv"
    cutoff_path = output / "cutoff_convergence.csv"
    step_path = output / "step_convergence.csv"
    npz_path = output / "coefficient_endpoints.npz"
    primary_fields = (
        "N", "epsilon", "finiteInviscidActionProxy", "finiteViscousAction",
        "kineticGain", "actualPhysicalLinearGain",
        "finiteInviscidActionPrefactor",
        "finiteViscousActionNormalizedPhysicalGain",
        "physicalKineticGainRelativeDifference", "aEndpointL2", "bEndpointL2",
        "bTargetEndpointL2", "cTargetEndpointL2", "cTripleEndpointL2",
        "cMeanPathSignedParallel", "cDoublePathSignedParallel",
        "cTotalSignedParallel", "forbiddenParityRelative",
        "finiteCompressionOnly",
    )
    primary_rows = []
    for case in cases:
        primary_rows.append({
            "N": case["N"],
            "epsilon": case["epsilon"],
            "finiteInviscidActionProxy": case["linear"]["finiteInviscidActionProxy"],
            "finiteViscousAction": case["linear"]["finiteViscousAction"],
            "kineticGain": case["linear"]["kineticGain"],
            "actualPhysicalLinearGain": case["hierarchy"]["actualPhysicalLinearGain"],
            "finiteInviscidActionPrefactor": case["finiteInviscidActionPrefactor"],
            "finiteViscousActionNormalizedPhysicalGain": case[
                "finiteViscousActionNormalizedPhysicalGain"
            ],
            "physicalKineticGainRelativeDifference": case[
                "physicalKineticGainRelativeDifference"
            ],
            "aEndpointL2": case["hierarchy"]["aEndpointL2"],
            "bEndpointL2": case["hierarchy"]["bEndpointL2"],
            "bTargetEndpointL2": case["hierarchy"]["bTargetEndpointL2"],
            "cTargetEndpointL2": case["hierarchy"]["cTargetEndpointL2"],
            "cTripleEndpointL2": case["hierarchy"]["cTripleEndpointL2"],
            "cMeanPathSignedParallel": case["hierarchy"]["cMeanPathSignedParallel"],
            "cDoublePathSignedParallel": case["hierarchy"]["cDoublePathSignedParallel"],
            "cTotalSignedParallel": case["hierarchy"]["cTotalSignedParallel"],
            "forbiddenParityRelative": case["hierarchy"]["forbiddenParityRelative"],
            "finiteCompressionOnly": True,
        })
    write_csv(rows_path, primary_fields, primary_rows)
    write_csv(action_path, (
        "branch", "N", "epsilon", "sampleIndex", "d", "lambda",
        "lambdaImaginary",
        "cumulativeAction", "fixedContourCount", "phaseAnchorAbs",
        "eigenResidualRelative", "finiteCompressionOnly",
    ), action_rows)
    write_csv(cutoff_path, (
        "smallN", "largeN", "epsilon",
        "finiteInviscidActionProxyAbsoluteDifference",
        "finiteInviscidActionPrefactorAbsoluteDifference",
        "selectedObservableHierarchyMaximumRelativeDifference",
        "finiteCutoffAgreementIsTailProof",
    ), cutoff_rows)
    write_csv(step_path, (
        "N", "epsilon", "coarseFastStep", "fineFastStep",
        "selectedObservableMaximumRelativeDifference",
    ), step_rows)
    write_npz(npz_path, raw_arrays)

    environment_path = output / "primary_environment.json"
    atomic_json(environment_path, environment_payload(
        ARGS.config, provenance, upstream, ARGS.smoke,
    ))
    results = {
        "schemaVersion": "r073m-primary-finite-diagnostic-v1",
        "release": "R0.73M",
        "status": "passed" if passed else "failed",
        "smokeMode": ARGS.smoke,
        "sourceProvenance": {
            "enforced": provenance["enforced"],
            "sourceCommit": provenance["sourceCommit"],
            "allSourceBlobsMatch": provenance["allSourceBlobsMatch"],
            **({"bindings": provenance["bindings"]} if provenance["enforced"] else {}),
        },
        "configurationBinding": binding(ARGS.config.resolve(), ROOT),
        "upstreamBindings": upstream,
        "parameters": {
            "gamma": gamma,
            "profileTimeEnd": d_end,
            "physicalTimeEnd": d_end / 4.0,
            "profileToPhysicalTimeRule": "d=4t",
            "cutoffs": cutoffs,
            "viscousEpsilons": epsilons,
            "actionSampleCount": len(d_grid),
            "fixedContour": contour,
            "hierarchyFastStep": config["hierarchy"]["primaryFastStep"],
        },
        "normalization": {
            "finiteInviscidActionProxy": "integral of lambda_(N,0) on [0,D*]",
            "finiteViscousAction": "integral of lambda_(N,epsilon) on [0,D*]",
            "finiteInviscidActionPrefactor": "actualPhysicalLinearGain*exp(-A_(N,0)/epsilon)",
            "a": "V1/actualPhysicalLinearGain",
            "b": "V2/actualPhysicalLinearGain^2",
            "c": "V3/actualPhysicalLinearGain^3",
        },
        "caseCount": len(cases),
        "cases": cases,
        "cutoffComparisons": cutoff_rows,
        "stepComparisons": step_rows,
        "archiveIndex": [
            {
                "archiveKey": case["archiveKey"],
                "N": case["N"],
                "epsilon": case["epsilon"],
                "stateOrder": [
                    "V1", "V2_Kz0", "V2_KzPlusMinus2",
                    "V3_via_Kz0", "V3_via_KzPlusMinus2",
                ],
                "shape": list(raw_arrays[case["archiveKey"]].shape),
            }
            for case in cases
        ],
        "maximums": maximums,
        "checks": checks,
        "allChecksPass": passed,
        "claimBoundary": config_full["claimBoundary"],
        "continuumConclusion": "none; finite action proxy and finite cubic hierarchy only",
    }
    results_path = output / "primary_results.json"
    atomic_json(results_path, results)
    monitor.sample("complete", cases=len(cases))
    monitor.emit("complete", allChecksPass=passed, cases=len(cases),
                 finiteDimensionalOnly=True)
    data_files = (
        results_path, rows_path, action_path, cutoff_path, step_path, npz_path,
        environment_path, output / "primary_progress.ndjson",
        output / "primary_resources.ndjson",
    )
    manifest = {
        "schemaVersion": "r073m-primary-manifest-v1",
        "release": "R0.73M",
        "smokeMode": ARGS.smoke,
        "sourceCommit": provenance.get("sourceCommit"),
        "files": [binding(path, output) for path in data_files],
        "allChecksPass": passed,
        "claimBoundary": config_full["claimBoundary"],
    }
    atomic_json(output / "primary_manifest.json", manifest)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
