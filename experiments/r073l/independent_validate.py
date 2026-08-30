#!/usr/bin/env python3
"""Independent midpoint-product validation for the R0.73L diagnostic.

This reconstruction deliberately does not import the primary solver.  It uses
piecewise midpoint matrix exponentials instead of solve_ivp and recomputes the
selected action from midpoint eigenvalues.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=os.environ.get("R073L_DEPS", ""))
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
from scipy.linalg import eig, expm  # noqa: E402


START = time.monotonic()
SOURCE = Path(__file__).resolve()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def emit(path: Path, event: str, **fields: object) -> None:
    row = {
        "event": event,
        "timestampUtc": now(),
        "elapsedSeconds": time.monotonic() - START,
        **fields,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")
    print(json.dumps(row, sort_keys=True), file=sys.stderr, flush=True)


def sample(path: Path, event: str, **fields: object) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    row = {
        "event": event,
        "timestampUtc": now(),
        "elapsedSeconds": time.monotonic() - START,
        "userCpuSeconds": usage.ru_utime,
        "systemCpuSeconds": usage.ru_stime,
        "maximumResidentSetSizePlatformUnits": usage.ru_maxrss,
        **fields,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, sort_keys=True) + "\n")


def matrix(cutoff: int, d_value: float, epsilon: float,
           gamma: float) -> np.ndarray:
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    ell = modes * modes + gamma * gamma
    raw = np.zeros((modes.size, modes.size), dtype=np.complex128)
    for column, n in enumerate(modes.astype(int)):
        first = (gamma * math.exp(-d_value) * 0.25
                 * (1.0 - 1.0 / ell[column]))
        second = (gamma * math.exp(-4.0 * d_value)
                  * (-0.125 + 0.5 / ell[column]))
        for shift, coefficient in (
            (1, first), (-1, -first),
            (2, second), (-2, -second),
        ):
            target = n + shift
            if -cutoff <= target <= cutoff:
                raw[target + cutoff, column] = coefficient
    result = ((1.0 / np.sqrt(ell))[:, None]
              * raw
              * np.sqrt(ell)[None, :])
    return result - epsilon * np.diag(ell)


def selected_state(value: np.ndarray, center: complex,
                   radius: float) -> dict[str, Any]:
    eigenvalues, left, right = eig(value, left=True, right=True,
                                   check_finite=False)
    indices = np.flatnonzero(np.abs(eigenvalues - center) < radius)
    if indices.size != 1:
        raise RuntimeError(f"fixed-contour count is {indices.size}")
    index = int(indices[0])
    lvec = left[:, index] / np.linalg.norm(left[:, index])
    rvec = right[:, index] / np.linalg.norm(right[:, index])
    pairing = complex(np.vdot(lvec, rvec))
    return {
        "lambda": complex(eigenvalues[index]),
        "left": lvec,
        "right": rvec,
        "pairing": pairing,
    }


def reconstruct(cutoff: int, epsilon: float, steps: int,
                slow_end: float, gamma: float, center: complex,
                radius: float) -> dict[str, float]:
    initial_state = selected_state(matrix(cutoff, 0.0, epsilon, gamma),
                                   center, radius)
    vector = initial_state["right"].copy()
    vector /= np.linalg.norm(vector)
    step = slow_end / steps
    action = 0.0
    for index in range(steps):
        midpoint = (index + 0.5) * step
        block = matrix(cutoff, midpoint, epsilon, gamma)
        midpoint_state = selected_state(block, center, radius)
        action += step * midpoint_state["lambda"].real / epsilon
        vector = expm((step / epsilon) * block) @ vector
    terminal_state = selected_state(
        matrix(cutoff, slow_end, epsilon, gamma), center, radius,
    )
    selected = (terminal_state["right"]
                * (np.vdot(terminal_state["left"], vector)
                   / terminal_state["pairing"]))
    complement = vector - selected
    gain = float(np.linalg.norm(vector))
    leakage = float(np.linalg.norm(complement) / np.linalg.norm(selected))
    return {
        "steps": steps,
        "terminalAction": float(action),
        "terminalGain": gain,
        "terminalActionNormalizedGain": gain / math.exp(action),
        "terminalComplementToSelectedRatio": leakage,
    }


def main() -> int:
    ARGS.progress.parent.mkdir(parents=True, exist_ok=True)
    ARGS.progress.write_text("", encoding="utf-8")
    ARGS.resources.write_text("", encoding="utf-8")
    config = json.loads(ARGS.config.read_text(encoding="utf-8"))
    primary = json.loads(ARGS.primary.read_text(encoding="utf-8"))
    cutoff = int(config["independentValidation"]["cutoff"])
    steps_list = [int(value)
                  for value in config["independentValidation"]["stepCounts"]]
    epsilons = [float(value) for value in config["epsilons"]]
    gamma = float(config["gamma"])
    slow_end = float(config["slowEnd"])
    contour = config["fixedContour"]
    center = complex(float(contour["centerReal"]),
                     float(contour["centerImag"]))
    radius = float(contour["radius"])
    emit(ARGS.progress, "start", cutoff=cutoff, epsilons=epsilons,
         stepCounts=steps_list, method="midpoint exponential product")
    sample(ARGS.resources, "start")

    cases: list[dict[str, Any]] = []
    for epsilon in epsilons:
        reconstructions = []
        for steps in steps_list:
            row = reconstruct(cutoff, epsilon, steps, slow_end, gamma,
                              center, radius)
            reconstructions.append(row)
            emit(ARGS.progress, "reconstruction", epsilon=epsilon,
                 steps=steps,
                 normalizedGain=row["terminalActionNormalizedGain"],
                 leakage=row["terminalComplementToSelectedRatio"])
        reference = next(
            case for case in primary["cases"]
            if case["N"] == cutoff and case["epsilon"] == epsilon
        )["summary"]
        finest = reconstructions[-1]
        cases.append({
            "epsilon": epsilon,
            "reconstructions": reconstructions,
            "finestVsPrimary": {
                "terminalGainAbsDifference": abs(
                    finest["terminalGain"] - reference["terminalGain"]
                ),
                "terminalActionAbsDifference": abs(
                    finest["terminalAction"] - reference["terminalAction"]
                ),
                "terminalNormalizedGainAbsDifference": abs(
                    finest["terminalActionNormalizedGain"]
                    - reference["terminalActionNormalizedGain"]
                ),
                "terminalLeakageAbsDifference": abs(
                    finest["terminalComplementToSelectedRatio"]
                    - reference["terminalComplementToSelectedRatio"]
                ),
            },
            "lastTwoStepCounts": {
                "terminalNormalizedGainAbsDifference": abs(
                    reconstructions[-1]["terminalActionNormalizedGain"]
                    - reconstructions[-2]["terminalActionNormalizedGain"]
                ),
                "terminalLeakageAbsDifference": abs(
                    reconstructions[-1]["terminalComplementToSelectedRatio"]
                    - reconstructions[-2]["terminalComplementToSelectedRatio"]
                ),
            },
        })
        sample(ARGS.resources, "case-complete", epsilon=epsilon)

    maximums = {
        "finestVsPrimaryNormalizedGain": max(
            row["finestVsPrimary"]["terminalNormalizedGainAbsDifference"]
            for row in cases
        ),
        "finestVsPrimaryLeakage": max(
            row["finestVsPrimary"]["terminalLeakageAbsDifference"]
            for row in cases
        ),
        "lastTwoNormalizedGain": max(
            row["lastTwoStepCounts"]["terminalNormalizedGainAbsDifference"]
            for row in cases
        ),
        "lastTwoLeakage": max(
            row["lastTwoStepCounts"]["terminalLeakageAbsDifference"]
            for row in cases
        ),
    }
    tolerances = config["independentValidation"]["tolerances"]
    checks = {
        "finestAgreesWithPrimaryNormalizedGain": (
            maximums["finestVsPrimaryNormalizedGain"]
            <= float(tolerances["primaryNormalizedGain"])
        ),
        "finestAgreesWithPrimaryLeakage": (
            maximums["finestVsPrimaryLeakage"]
            <= float(tolerances["primaryLeakage"])
        ),
        "stepRefinementConvergesNormalizedGain": (
            maximums["lastTwoNormalizedGain"]
            <= float(tolerances["refinementNormalizedGain"])
        ),
        "stepRefinementConvergesLeakage": (
            maximums["lastTwoLeakage"]
            <= float(tolerances["refinementLeakage"])
        ),
    }
    passed = bool(all(checks.values()))
    payload = {
        "schemaVersion": "r073l-independent-validation-v1",
        "release": "R0.73L",
        "createdUtc": now(),
        "status": "passed" if passed else "failed",
        "method": "piecewise midpoint matrix-exponential product",
        "sourceBinding": {
            "path": "experiments/r073l/independent_validate.py",
            "sha256": sha256(SOURCE),
        },
        "configurationBinding": {
            "path": str(ARGS.config),
            "sha256": sha256(ARGS.config),
        },
        "primaryBinding": {
            "path": str(ARGS.primary),
            "sha256": sha256(ARGS.primary),
        },
        "cases": cases,
        "maximums": maximums,
        "checks": checks,
        "allChecksPass": passed,
        "claimBoundary": {
            "independentFiniteReconstruction": True,
            "continuumProof": False,
        },
    }
    write_json(ARGS.output, payload)
    sample(ARGS.resources, "complete", cases=len(cases))
    emit(ARGS.progress, "complete", status=payload["status"],
         maximums=maximums)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())

