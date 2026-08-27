#!/usr/bin/env python3
"""Producer finite audit for the R0.72L strong-coupling ledger.

The analytic report carries the proofs.  This standard-library program only
checks finite algebraic identities and examples:

* the monomial exponents in the L.1--L.5 normalized ledger;
* the pointwise optimizations used to pass from L.1 to L.2 and L.4;
* finite local-action-floor and closure-window samples with the suppressed
  absolute constant normalized to one; and
* a three-mode Galerkin oscillator together with the exact leakage that makes
  that truncation non-portable to the full Fourier lattice.

Binary64 integration and a finite parameter scan are corroboration, not a
proof, an interval certificate, a DNS, or a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


SCHEMA_VERSION = 1
AUDIT_NAME = "R0.72L strong-coupling producer finite audit"
LOCAL_WINDOW_CONSTANT = 0.02


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(value) / (1024.0 * 1024.0)
    return float(value) / 1024.0


def resource_record(started: float, event: str) -> dict[str, Any]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "time": utc_now(),
        "event": event,
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "userCpuSeconds": float(usage.ru_utime),
        "systemCpuSeconds": float(usage.ru_stime),
        "pid": os.getpid(),
    }


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def add_exp(*values: dict[str, Fraction]) -> dict[str, Fraction]:
    keys = set().union(*(value.keys() for value in values))
    return {
        key: sum((value.get(key, Fraction(0)) for value in values), Fraction(0))
        for key in sorted(keys)
        if sum((value.get(key, Fraction(0)) for value in values), Fraction(0))
        != 0
    }


def scale_exp(value: dict[str, Fraction], factor: Fraction) -> dict[str, Fraction]:
    return {key: exponent * factor for key, exponent in value.items() if exponent}


def exponent_audit() -> dict[str, Any]:
    epsilon = {"epsilon": Fraction(1)}
    p_value = {"p": Fraction(1)}
    r_value = {"R": Fraction(1)}
    ell = {"L": Fraction(1)}
    one_third = Fraction(1, 3)

    computed = {
        "U0": add_exp(scale_exp(epsilon, 4 * one_third), scale_exp(p_value, 4 * one_third)),
        "W": add_exp(
            scale_exp(epsilon, one_third),
            scale_exp(p_value, one_third),
            scale_exp(r_value, -one_third),
            scale_exp(ell, Fraction(-1, 2)),
        ),
        "U": add_exp(scale_exp(epsilon, 7 * one_third), scale_exp(p_value, 4 * one_third)),
        "V": add_exp(scale_exp(epsilon, one_third), scale_exp(p_value, one_third), r_value),
    }
    computed["H=U/V"] = add_exp(computed["U"], scale_exp(computed["V"], Fraction(-1)))
    expected = {
        "U0": {"epsilon": Fraction(4, 3), "p": Fraction(4, 3)},
        "W": {
            "L": Fraction(-1, 2),
            "R": Fraction(-1, 3),
            "epsilon": Fraction(1, 3),
            "p": Fraction(1, 3),
        },
        "U": {"epsilon": Fraction(7, 3), "p": Fraction(4, 3)},
        "V": {"R": Fraction(1), "epsilon": Fraction(1, 3), "p": Fraction(1, 3)},
        "H=U/V": {"R": Fraction(-1), "epsilon": Fraction(2), "p": Fraction(1)},
    }

    def serialize(value: dict[str, Fraction]) -> dict[str, str]:
        return {key: str(exponent) for key, exponent in value.items()}

    return {
        "computed": {key: serialize(value) for key, value in computed.items()},
        "expected": {key: serialize(value) for key, value in expected.items()},
        "checks": {key: computed[key] == expected[key] for key in expected},
    }


def ledger_values(r_value: float, p_value: float, epsilon: float) -> dict[str, float]:
    ell = 1.0 + math.log(r_value)
    u0 = epsilon ** (4.0 / 3.0) * p_value ** (4.0 / 3.0)
    w_value = (
        epsilon ** (1.0 / 3.0)
        * p_value ** (1.0 / 3.0)
        * r_value ** (-1.0 / 3.0)
        * ell ** (-0.5)
    )
    u_value = epsilon ** (7.0 / 3.0) * p_value ** (4.0 / 3.0)
    v_value = epsilon ** (1.0 / 3.0) * p_value ** (1.0 / 3.0) * r_value
    h_value = u_value / v_value
    z_value = (
        epsilon**2
        * p_value**2
        * r_value ** (2.0 / 3.0)
        * (1.0 + epsilon) ** (-2.0 / 3.0)
        * (1.0 + math.log(2.0 + r_value**2 * (1.0 + epsilon)))
    )
    closure_scale = p_value ** (2.0 / 3.0) * r_value ** (2.0 / 3.0) * ell
    return {
        "L": ell,
        "U0": u0,
        "W": w_value,
        "U": u_value,
        "V": v_value,
        "H": h_value,
        "Z": z_value,
        "closureScale": closure_scale,
    }


def raw_ledger(parts: dict[str, float], k_value: float, x_value: float) -> float:
    return (
        parts["U0"] / (k_value + x_value)
        + parts["W"] * math.sqrt(x_value) / (k_value + x_value)
        + min(parts["U"], parts["V"] * x_value) / (k_value + x_value)
    )


def reduced_l2(parts: dict[str, float], k_value: float) -> float:
    return (
        parts["U0"] / k_value
        + parts["W"] / math.sqrt(k_value)
        + parts["U"] / (k_value + parts["H"])
    )


def reduced_l4(parts: dict[str, float], k_value: float) -> float:
    return (
        parts["U0"] / (k_value + parts["Z"])
        + parts["W"] / math.sqrt(k_value + parts["Z"])
        + parts["U"] / (k_value + max(parts["H"], parts["Z"]))
    )


def optimization_scan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in [8.0, 32.0, 128.0, 512.0]:
        for p_value in [0.25, 0.5, 1.0]:
            parts = ledger_values(r_value, p_value, epsilon=1.0 + r_value ** 0.21)
            for k_value in [0.03125, 0.5, 8.0, 128.0]:
                l2 = reduced_l2(parts, k_value)
                l4 = reduced_l4(parts, k_value)
                x_grid = [10.0 ** (-6.0 + 12.0 * index / 480.0) for index in range(481)]
                all_raw = [raw_ledger(parts, k_value, x_value) for x_value in x_grid]
                floor_grid = [
                    parts["Z"] * 10.0 ** (6.0 * index / 360.0)
                    for index in range(361)
                ]
                floor_raw = [raw_ledger(parts, k_value, x_value) for x_value in floor_grid]
                rows.append(
                    {
                        "R": r_value,
                        "p": p_value,
                        "epsilon": 1.0 + r_value ** 0.21,
                        "K": k_value,
                        "Z": parts["Z"],
                        "maxRawGrid": max(all_raw),
                        "L2Bound": l2,
                        "L2Slack": l2 - max(all_raw),
                        "maxRawAboveFloorGrid": max(floor_raw),
                        "L4Bound": l4,
                        "L4Slack": l4 - max(floor_raw),
                        "passed": max(all_raw) <= l2 * (1.0 + 2.0e-14)
                        and max(floor_raw) <= l4 * (1.0 + 2.0e-14),
                    }
                )
    return rows


def local_floor_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in [8.0, 32.0, 128.0, 512.0, 2048.0]:
        for p_value in [0.5, 1.0]:
            closure = ledger_values(r_value, p_value, 1.0)["closureScale"]
            epsilon = max(1.0, closure / math.sqrt(math.log(2.0 + r_value)))
            parts = ledger_values(r_value, p_value, epsilon)
            s_value = r_value**2 * (1.0 + epsilon)
            tau = LOCAL_WINDOW_CONSTANT / s_value
            x_sample = 1.25 * parts["Z"]
            l4 = reduced_l4(parts, 0.0)
            raw = raw_ledger(parts, 0.0, x_sample)
            rows.append(
                {
                    "R": r_value,
                    "p": p_value,
                    "epsilon": epsilon,
                    "closureScale": parts["closureScale"],
                    "epsilonOverClosureScale": epsilon / parts["closureScale"],
                    "S": s_value,
                    "tau": tau,
                    "tauTimesS": tau * s_value,
                    "ZNormalizedConstantOne": parts["Z"],
                    "xSample": x_sample,
                    "xAboveZ": x_sample >= parts["Z"],
                    "rawLedgerAtSample": raw,
                    "L4AtKZero": l4,
                    "l4DominatesSample": raw <= l4 * (1.0 + 2.0e-14),
                }
            )
    return rows


def closure_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in [16.0, 64.0, 256.0, 1024.0, 4096.0, 16384.0]:
        for regime, p_value in [("p=1", 1.0), ("p=R^-1/2", r_value ** -0.5)]:
            initial = ledger_values(r_value, p_value, 1.0)
            epsilon = initial["closureScale"] / math.sqrt(math.log(2.0 + r_value))
            parts = ledger_values(r_value, p_value, epsilon)
            bound = reduced_l4(parts, 0.0)
            rows.append(
                {
                    "R": r_value,
                    "p": p_value,
                    "pRegime": regime,
                    "epsilon": epsilon,
                    "closureScale": parts["closureScale"],
                    "epsilonOverClosureScale": epsilon / parts["closureScale"],
                    "normalizedLedgerProxy": bound,
                    "insideWindow": 1.0 <= epsilon <= parts["closureScale"],
                }
            )
    return rows


def rk4_step(
    derivative: Callable[[float, tuple[float, float]], tuple[float, float]],
    y_value: float,
    state: tuple[float, float],
    step: float,
) -> tuple[float, float]:
    k1 = derivative(y_value, state)
    k2 = derivative(
        y_value + 0.5 * step,
        (state[0] + 0.5 * step * k1[0], state[1] + 0.5 * step * k1[1]),
    )
    k3 = derivative(
        y_value + 0.5 * step,
        (state[0] + 0.5 * step * k2[0], state[1] + 0.5 * step * k2[1]),
    )
    k4 = derivative(
        y_value + step,
        (state[0] + step * k3[0], state[1] + step * k3[1]),
    )
    return (
        state[0] + step * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]) / 6.0,
        state[1] + step * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]) / 6.0,
    )


def galerkin_case(r_value: int, sigma: float, c_value: float = 1.0) -> dict[str, Any]:
    # At least 240 steps per fastest angular period, and never fewer than 20k.
    steps = max(20_000, int(math.ceil(40.0 * sigma)))
    step = 1.0 / steps
    inv_r2 = 1.0 / float(r_value**2)

    def derivative(y_value: float, state: tuple[float, float]) -> tuple[float, float]:
        u_value, v_value = state
        coupling = sigma * math.exp(-y_value)
        return (
            -inv_r2 * u_value - coupling * v_value,
            coupling * u_value - (1.0 + inv_r2) * v_value,
        )

    state = (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0))
    y_value = 0.0
    g_mass = 0.0
    cubic_integral = 0.0
    mixed_integral = 0.0
    root_count = 0
    previous_u, previous_v = state
    previous_cubic = math.exp(-3.0 * y_value) * abs(previous_u * previous_v)
    previous_mixed = math.exp(-2.0 * y_value) * previous_v**2
    for _ in range(steps):
        next_state = rk4_step(derivative, y_value, state, step)
        next_y = y_value + step
        next_u, next_v = next_state
        next_cubic = math.exp(-3.0 * next_y) * abs(next_u * next_v)
        next_mixed = math.exp(-2.0 * next_y) * next_v**2
        cubic_integral += 0.5 * step * (previous_cubic + next_cubic)
        mixed_integral += 0.5 * step * (previous_mixed + next_mixed)
        if previous_u == 0.0 or previous_u * next_u < 0.0:
            fraction = abs(previous_u) / (abs(previous_u) + abs(next_u))
            root_y = y_value + fraction * step
            root_v = previous_v + fraction * (next_v - previous_v)
            g_mass += c_value**2 * math.exp(-2.0 * root_y) * root_v**2
            root_count += 1
        state = next_state
        y_value = next_y
        previous_u, previous_v = state
        previous_cubic = next_cubic
        previous_mixed = next_mixed

    a_r = (1.0 - math.exp(-(4.0 + 2.0 * inv_r2))) / (
        math.pi * (4.0 + 2.0 * inv_r2)
    )
    b_r = (1.0 - math.exp(-(3.0 + 2.0 * inv_r2))) / (3.0 + 2.0 * inv_r2)
    c_row = c_value**2 * sigma * cubic_integral
    e_q = 2.0 * c_value**2 * mixed_integral
    g_asymptotic = c_value**2 * sigma * a_r
    c_asymptotic = c_value**2 * sigma * a_r
    e_asymptotic = c_value**2 * b_r
    root_prediction = sigma * (1.0 - math.exp(-1.0)) / math.pi
    return {
        "R": r_value,
        "sigma": sigma,
        "steps": steps,
        "rootCount": root_count,
        "rootCountPrediction": root_prediction,
        "rootCountRatio": root_count / root_prediction,
        "GRootMass": g_mass,
        "CubicRow": c_row,
        "MixedRow": e_q,
        "AR": a_r,
        "BR": b_r,
        "GAsymptotic": g_asymptotic,
        "CubicAsymptotic": c_asymptotic,
        "MixedAsymptotic": e_asymptotic,
        "GAsymptoticRatio": g_mass / g_asymptotic,
        "CubicAsymptoticRatio": c_row / c_asymptotic,
        "MixedAsymptoticRatio": e_q / e_asymptotic,
    }


def apply_single_carrier(
    vector: dict[int, complex], r_value: int, amplitude: float
) -> dict[int, complex]:
    if not vector:
        return {}
    output: dict[int, complex] = {}
    candidates = {index - r_value for index in vector} | {
        index + r_value for index in vector
    }
    for index in candidates:
        value = -1j * amplitude * (
            vector.get(index - r_value, 0.0j)
            + vector.get(index + r_value, 0.0j)
        )
        if abs(value) > 0.0:
            output[index] = value
    return output


def full_support_cases() -> dict[str, Any]:
    r_value = 7
    amplitude = 1.25
    e0 = {0: 1.0 + 0.0j}
    first = apply_single_carrier(e0, r_value, amplitude)
    second = apply_single_carrier(first, r_value, amplitude)
    outside = {index: value for index, value in second.items() if abs(index) > r_value}
    inside_norm = abs(second.get(0, 0.0j))
    outside_norm = math.sqrt(sum(abs(value) ** 2 for value in outside.values()))

    extremal_rows: list[dict[str, Any]] = []
    for support, carriers in [
        ({-3: 2.0, -1: -1.5, 2: 0.75}, {2: 0.5, 5: 1.25}),
        ({-8: 1.0, 0: -2.0, 9: 3.0}, {1: 2.0, 4: -0.75}),
        ({-2: 1.0, 4: 1.0}, {3: 0.25, 11: 0.625}),
    ]:
        s_star = max(support)
        r_star = max(carriers)
        extreme_index = s_star + r_star
        contributions = [
            -1j * amplitude_value * support.get(extreme_index - carrier, 0.0)
            for carrier, amplitude_value in carriers.items()
            if support.get(extreme_index - carrier, 0.0) != 0.0
        ] + [
            -1j * amplitude_value * support.get(extreme_index + carrier, 0.0)
            for carrier, amplitude_value in carriers.items()
            if support.get(extreme_index + carrier, 0.0) != 0.0
        ]
        expected = -1j * carriers[r_star] * support[s_star]
        actual = sum(contributions, 0.0j)
        extremal_rows.append(
            {
                "supportMax": s_star,
                "carrierMax": r_star,
                "extremeIndex": extreme_index,
                "contributionCount": len(contributions),
                "expectedReal": expected.real,
                "expectedImag": expected.imag,
                "actualReal": actual.real,
                "actualImag": actual.imag,
                "uniqueNonzeroExtreme": len(contributions) == 1
                and abs(actual - expected) < 1.0e-14,
            }
        )

    expected_outside_norm = math.sqrt(2.0) * amplitude**2
    return {
        "carrier": r_value,
        "amplitude": amplitude,
        "firstSupport": sorted(first),
        "secondSupport": sorted(second),
        "insideNormW2e0": inside_norm,
        "outsideNormW2e0": outside_norm,
        "outsideOverInside": outside_norm / inside_norm,
        "expectedOutsideOverInside": 1.0 / math.sqrt(2.0),
        "expectedOutsideNorm": expected_outside_norm,
        "extremalCases": extremal_rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/certificates/r072l"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    progress_path = output_dir / "producer-progress.ndjson"
    resource_path = output_dir / "producer-resource.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "date": "2026-08-27",
        "arithmetic": "Python standard library; exact Fraction exponents and binary64 finite scans",
        "localWindowConstant": LOCAL_WINDOW_CONSTANT,
        "suppressedAnalyticConstantProxy": 1.0,
        "galerkinRValues": [8, 16],
        "galerkinSigmaValues": [32, 64, 128, 256, 512],
        "randomSeedUsed": False,
        "sourceSha256": sha256(Path(__file__).resolve()),
    }
    (output_dir / "config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "seed.txt").write_text(
        "deterministic:no-random-seed\n", encoding="utf-8"
    )
    append_ndjson(progress_path, {"time": utc_now(), "event": "audit_start", "config": config})
    append_ndjson(resource_path, resource_record(started, "audit_start"))

    exponents = exponent_audit()
    optimization = optimization_scan()
    local_rows = local_floor_cases()
    closure = closure_cases()
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "normalized_ledger_complete",
            "optimizationCases": len(optimization),
            "localFloorCases": len(local_rows),
            "closureCases": len(closure),
        },
    )
    append_ndjson(resource_path, resource_record(started, "normalized_ledger_complete"))

    galerkin: list[dict[str, Any]] = []
    for r_value in config["galerkinRValues"]:
        for sigma in config["galerkinSigmaValues"]:
            row = galerkin_case(int(r_value), float(sigma))
            galerkin.append(row)
            append_ndjson(
                progress_path,
                {
                    "time": utc_now(),
                    "event": "galerkin_case_complete",
                    "R": r_value,
                    "sigma": sigma,
                    "rootCount": row["rootCount"],
                    "GAsymptoticRatio": row["GAsymptoticRatio"],
                    "CubicAsymptoticRatio": row["CubicAsymptoticRatio"],
                    "MixedAsymptoticRatio": row["MixedAsymptoticRatio"],
                },
            )
    append_ndjson(resource_path, resource_record(started, "galerkin_complete"))

    support = full_support_cases()
    tail = [row for row in galerkin if row["sigma"] >= 256]
    checks = {
        "allExponentIdentitiesExact": all(exponents["checks"].values()),
        "l2AndL4FiniteScansPass": all(row["passed"] for row in optimization),
        "localWindowNormalizationExact": max(
            abs(row["tauTimesS"] - LOCAL_WINDOW_CONSTANT) for row in local_rows
        ) < 5.0e-15,
        "localSamplesRespectNormalizedFloor": all(row["xAboveZ"] for row in local_rows),
        "localSamplesRespectL4Reduction": all(row["l4DominatesSample"] for row in local_rows),
        "closureSamplesInsideWindow": all(row["insideWindow"] for row in closure),
        "closureRatioDecreases": all(
            all(
                left["epsilonOverClosureScale"]
                > right["epsilonOverClosureScale"]
                for left, right in zip(
                    [row for row in closure if row["pRegime"] == regime],
                    [row for row in closure if row["pRegime"] == regime][1:],
                )
            )
            for regime in {row["pRegime"] for row in closure}
        ),
        "closureProxyTailDecreases": all(
            all(
                left["normalizedLedgerProxy"] > right["normalizedLedgerProxy"]
                for left, right in zip(
                    [row for row in closure if row["pRegime"] == regime][-4:],
                    [row for row in closure if row["pRegime"] == regime][-3:],
                )
            )
            for regime in {row["pRegime"] for row in closure}
        ),
        "galerkinProducesManyRoots": min(row["rootCount"] for row in tail) >= 45,
        "galerkinRootMassApproachesAsymptotic": max(
            abs(row["GAsymptoticRatio"] - 1.0) for row in tail
        ) < 0.08,
        "galerkinCubicApproachesAsymptotic": max(
            abs(row["CubicAsymptoticRatio"] - 1.0) for row in tail
        ) < 0.06,
        "galerkinMixedApproachesAsymptotic": max(
            abs(row["MixedAsymptoticRatio"] - 1.0) for row in tail
        ) < 0.04,
        "singleCarrierLeaksOutsideThreeModes": support["secondSupport"] == [-14, 0, 14],
        "leakageNormIdentity": relative_error(
            support["outsideNormW2e0"], support["expectedOutsideNorm"]
        ) < 2.0e-15,
        "leakageRatioIdentity": relative_error(
            support["outsideOverInside"], support["expectedOutsideOverInside"]
        ) < 2.0e-15,
        "finiteExtremalSamplesUnique": all(
            row["uniqueNonzeroExtreme"] for row in support["extremalCases"]
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    passed = all(checks.values())
    elapsed = time.perf_counter() - started
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(),
        "config": config,
        "exponentAudit": exponents,
        "optimizationCases": optimization,
        "localFloorCases": local_rows,
        "closureCases": closure,
        "galerkinCases": galerkin,
        "fullSupportAudit": support,
        "checks": checks,
        "elapsedSeconds": elapsed,
        "limitations": [
            "L.1--L.5 are analytic statements; this finite audit does not prove them",
            "the unknown absolute constants in the local floor and closure window are normalized to one only for exponent and scaling checks",
            "the local action floor is sampled finitely and is not an interval lower bound",
            "the Galerkin oscillator deletes the plus-or-minus 2R leakage and is not an invariant subsystem of the full lattice",
            "the extremal-index samples corroborate but do not replace the full-support analytic proof",
            "no DNS or general three-dimensional Navier--Stokes regularity claim is made",
        ],
    }
    result_path = output_dir / "result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(output_dir / "producer-optimization.csv", optimization)
    write_csv(output_dir / "producer-local-floor.csv", local_rows)
    write_csv(output_dir / "producer-closure.csv", closure)
    write_csv(output_dir / "producer-galerkin.csv", galerkin)

    environment = {
        "generatedAt": utc_now(),
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "executable": sys.executable,
        "cpuCount": os.cpu_count(),
        "maxRssMb": max_rss_mb(),
    }
    (output_dir / "environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()) + "\n",
        encoding="utf-8",
    )
    append_ndjson(resource_path, resource_record(started, "audit_complete"))
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "checks": checks,
        },
    )
    monitor = {
        "status": result["status"],
        "optimizationCases": len(optimization),
        "localFloorCases": len(local_rows),
        "closureCases": len(closure),
        "galerkinCases": len(galerkin),
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "resultSha256": sha256(result_path),
    }
    (output_dir / "producer-monitor.log").write_text(
        json.dumps(monitor, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(monitor, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
