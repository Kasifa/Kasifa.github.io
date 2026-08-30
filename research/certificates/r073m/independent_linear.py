#!/usr/bin/env python3
"""Independent midpoint-exponential linear/action validation for R0.73M.

This file does not import the primary producer.  It constructs the kinetic
matrix directly from the Orr--Sommerfeld Fourier coefficients, uses midpoint
quadrature for both finite actions, and propagates by a product of dense
matrix exponentials.
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
    {"cutoff": 32, "viscousEpsilon": 0.001},
    {"cutoff": 32, "viscousEpsilon": 0.0000625},
    {"cutoff": 48, "viscousEpsilon": 0.00025},
    {"cutoff": 64, "viscousEpsilon": 0.0005},
    {"cutoff": 64, "viscousEpsilon": 0.0000625},
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
from scipy.linalg import eig, expm  # noqa: E402


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


def matrix_from_os_formula(
    cutoff: int, d_value: float, epsilon: float, gamma: float,
) -> np.ndarray:
    modes = np.arange(-cutoff, cutoff + 1, dtype=int)
    ell = modes.astype(float) ** 2 + gamma * gamma
    shifts = modes[:, None] - modes[None, :]
    w_hat = {
        1: 0.25j * math.exp(-d_value),
        -1: -0.25j * math.exp(-d_value),
        2: -0.125j * math.exp(-4.0 * d_value),
        -2: 0.125j * math.exp(-4.0 * d_value),
    }
    wxx_hat = {
        1: -0.25j * math.exp(-d_value),
        -1: 0.25j * math.exp(-d_value),
        2: 0.5j * math.exp(-4.0 * d_value),
        -2: -0.5j * math.exp(-4.0 * d_value),
    }
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


def anchor(vector: np.ndarray, cutoff: int, gamma: float) -> complex:
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    return complex(0.5 * np.sum(vector / np.sqrt(modes * modes + gamma * gamma)))


def selected(matrix: np.ndarray, cutoff: int, gamma: float,
             center: complex, radius: float, phase: bool) -> tuple[complex, np.ndarray]:
    values, vectors = eig(matrix, left=False, right=True, check_finite=False)
    inside = np.flatnonzero(np.abs(values - center) < radius)
    if inside.size != 1:
        raise RuntimeError(f"fixed-contour count is {inside.size}, not one")
    index = int(inside[0])
    vector = np.asarray(vectors[:, index], dtype=np.complex128)
    vector /= np.linalg.norm(vector)
    if phase:
        value = anchor(vector, cutoff, gamma)
        if abs(value) <= 1e-12:
            raise RuntimeError("independent phase anchor vanished")
        vector *= np.exp(-1j * np.angle(value))
        if anchor(vector, cutoff, gamma).real < 0.0:
            vector *= -1.0
    return complex(values[index]), vector


def reconstruct(
    cutoff: int, epsilon: float, steps: int, d_end: float, gamma: float,
    center: complex, radius: float,
) -> dict[str, float]:
    _, vector = selected(
        matrix_from_os_formula(cutoff, 0.0, epsilon, gamma),
        cutoff, gamma, center, radius, True,
    )
    step = d_end / steps
    inviscid_action = 0.0
    viscous_action = 0.0
    for index in range(steps):
        midpoint = (index + 0.5) * step
        viscous_matrix = matrix_from_os_formula(
            cutoff, midpoint, epsilon, gamma,
        )
        inviscid_matrix = matrix_from_os_formula(
            cutoff, midpoint, 0.0, gamma,
        )
        viscous_lambda, _ = selected(
            viscous_matrix, cutoff, gamma, center, radius, False,
        )
        inviscid_lambda, _ = selected(
            inviscid_matrix, cutoff, gamma, center, radius, False,
        )
        viscous_action += step * viscous_lambda.real
        inviscid_action += step * inviscid_lambda.real
        vector = expm((step / epsilon) * viscous_matrix) @ vector
    gain = float(np.linalg.norm(vector))
    result = {
        "steps": steps,
        "gain": gain,
        "finiteInviscidActionProxy": float(inviscid_action),
        "finiteViscousAction": float(viscous_action),
        "finiteInviscidActionPrefactor": (
            gain * math.exp(-inviscid_action / epsilon)
        ),
        "finiteViscousActionNormalizedGain": (
            gain * math.exp(-viscous_action / epsilon)
        ),
    }
    if not bool(np.isfinite(vector).all()) or not all(
        math.isfinite(float(value)) for value in result.values()
    ):
        raise RuntimeError("nonfinite independent linear reconstruction")
    return result


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1e-300)


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
        "stepCounts": [256, 512], "sentinels": EXPECTED_SENTINELS,
    }:
        raise RuntimeError("independent linear contract drift")
    if config.get("independentHierarchy", {}).get("sentinels") != [
        {"cutoff": 32, "viscousEpsilon": 0.001, "fastStep": 0.05},
        {"cutoff": 48, "viscousEpsilon": 0.00025, "fastStep": 0.05},
        {"cutoff": 64, "viscousEpsilon": 0.0000625, "fastStep": 0.025},
    ]:
        raise RuntimeError("independent hierarchy sentinel contract drift")
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
        output != (HERE / "independent_linear.json").resolve()
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
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    if primary.get("smokeMode") is not ARGS.smoke or not primary.get("allChecksPass"):
        raise RuntimeError("primary result mode/pass state mismatch")
    provenance = source_gate(ARGS.source_commit, ARGS.smoke)
    upstream = verify_upstream(config)
    monitor = Monitor(ARGS.progress.resolve(), ARGS.resources.resolve())
    monitor.emit("start", smokeMode=ARGS.smoke,
                 method="midpoint matrix-exponential product plus midpoint actions")
    monitor.sample("start")

    if ARGS.smoke:
        sentinels = [
            {"cutoff": 8, "viscousEpsilon": 0.001},
            {"cutoff": 10, "viscousEpsilon": 0.0005},
        ]
        step_counts = [8, 16]
        tolerance = {
            **config["tolerances"],
            "independentLinearActionRelative": 2e-3,
            "independentLinearGainRelative": 2e-3,
            "independentLinearPrefactorAbsolute": 2e-3,
            "independentLinearRefinement": 2e-3,
        }
    else:
        sentinels = config["independentLinear"]["sentinels"]
        step_counts = [int(value) for value in config["independentLinear"]["stepCounts"]]
        tolerance = config["tolerances"]
    gamma = float(config["gamma"])
    d_end = float(config["profileTimeEnd"])
    contour = config["fixedContour"]
    center = complex(float(contour["centerReal"]), float(contour["centerImag"]))
    radius = float(contour["radius"])
    validations = []
    for index, sentinel in enumerate(sentinels, start=1):
        cutoff = int(sentinel["cutoff"])
        epsilon = float(sentinel["viscousEpsilon"])
        monitor.emit("sentinel-start", index=index, N=cutoff, epsilon=epsilon)
        reconstructions = [
            reconstruct(cutoff, epsilon, steps, d_end, gamma, center, radius)
            for steps in step_counts
        ]
        reference = next(
            case for case in primary["cases"]
            if int(case["N"]) == cutoff and float(case["epsilon"]) == epsilon
        )
        finest = reconstructions[-1]
        comparison = {
            "gainRelative": relative(
                finest["gain"], reference["hierarchy"]["actualPhysicalLinearGain"]
            ),
            "finiteInviscidActionProxyRelative": relative(
                finest["finiteInviscidActionProxy"],
                reference["linear"]["finiteInviscidActionProxy"],
            ),
            "finiteViscousActionRelative": relative(
                finest["finiteViscousAction"],
                reference["linear"]["finiteViscousAction"],
            ),
            "finiteInviscidActionPrefactorAbsolute": abs(
                finest["finiteInviscidActionPrefactor"]
                - reference["finiteInviscidActionPrefactor"]
            ),
        }
        refinement = {
            key: relative(reconstructions[-1][key], reconstructions[-2][key])
            for key in (
                "gain", "finiteInviscidActionProxy", "finiteViscousAction",
                "finiteInviscidActionPrefactor",
            )
        }
        checks = {
            "gain": comparison["gainRelative"]
            <= float(tolerance["independentLinearGainRelative"]),
            "finiteInviscidActionProxy": comparison[
                "finiteInviscidActionProxyRelative"
            ] <= float(tolerance["independentLinearActionRelative"]),
            "finiteViscousAction": comparison["finiteViscousActionRelative"]
            <= float(tolerance["independentLinearActionRelative"]),
            "finiteInviscidActionPrefactor": comparison[
                "finiteInviscidActionPrefactorAbsolute"
            ] <= float(tolerance["independentLinearPrefactorAbsolute"]),
            "stepRefinement": max(refinement.values())
            <= float(tolerance["independentLinearRefinement"]),
        }
        validations.append({
            "N": cutoff, "epsilon": epsilon,
            "reconstructions": reconstructions,
            "finestVsPrimary": comparison,
            "lastTwoStepCountsRelative": refinement,
            "checks": checks,
            "pass": all(checks.values()),
        })
        monitor.sample("sentinel-complete", index=index, N=cutoff, epsilon=epsilon)
        monitor.emit("sentinel-complete", index=index, N=cutoff, epsilon=epsilon,
                     passCheck=all(checks.values()))

    maximums = {
        "gainRelative": max(row["finestVsPrimary"]["gainRelative"] for row in validations),
        "finiteInviscidActionProxyRelative": max(
            row["finestVsPrimary"]["finiteInviscidActionProxyRelative"]
            for row in validations
        ),
        "finiteViscousActionRelative": max(
            row["finestVsPrimary"]["finiteViscousActionRelative"]
            for row in validations
        ),
        "finiteInviscidActionPrefactorAbsolute": max(
            row["finestVsPrimary"]["finiteInviscidActionPrefactorAbsolute"]
            for row in validations
        ),
        "stepRefinement": max(
            max(row["lastTwoStepCountsRelative"].values()) for row in validations
        ),
    }
    passed = all(row["pass"] for row in validations)
    result = {
        "schemaVersion": "r073m-independent-linear-action-v1",
        "release": "R0.73M",
        "status": "passed" if passed else "failed",
        "smokeMode": ARGS.smoke,
        "method": {
            "matrix": "direct Orr--Sommerfeld Fourier coefficients",
            "propagation": "piecewise midpoint dense matrix-exponential product",
            "actions": "independent midpoint quadrature for epsilon and epsilon-zero branches",
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
        "primaryBinding": binding(primary_path, primary_dir),
        "upstreamBindings": upstream,
        "sentinels": [
            {"cutoff": int(row["cutoff"]), "viscousEpsilon": float(row["viscousEpsilon"])}
            for row in sentinels
        ],
        "stepCounts": step_counts,
        "validations": validations,
        "maximums": maximums,
        "allChecksPass": passed,
        "claimBoundary": config["claimBoundary"],
    }
    atomic_json(output, result)
    monitor.sample("complete", sentinels=len(validations))
    monitor.emit("complete", allChecksPass=passed, sentinels=len(validations))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
