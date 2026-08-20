#!/usr/bin/env python3
"""Audit the exact R0.63 time-layer and cubic-lift identities.

The heat-layer comparison uses floating-point exponentials only to check two
algebraically identical finite formulas.  The cubic-lift regression is exact
integer arithmetic.  Neither calculation proves the desired operator norm.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path


T = math.log(2.0) / 2.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rudin_shapiro_pair(level: int) -> tuple[list[int], list[int]]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p, q


def tensor_signs(level_l: int, level_m: int) -> list[int]:
    inner, _ = rudin_shapiro_pair(level_l)
    outer, _ = rudin_shapiro_pair(level_m)
    return [outer[r] * inner[n] for r in range(len(outer)) for n in range(len(inner))]


def convolve(left: list[float], right: list[float]) -> list[float]:
    output = [0.0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    return output


def correlation_coefficient(
    left: list[float], middle: list[float], right: list[float], exponent: int
) -> float:
    product = convolve(convolve(left, middle), list(reversed(right)))
    index = exponent + len(right) - 1
    return 0.0 if not 0 <= index < len(product) else product[index]


def direct_layer_sum(
    level_l: int, level_m: int, target: int, tau: tuple[float, float, float]
) -> float:
    length = 1 << level_l
    outputs = 1 << level_m
    count = length * outputs
    high = 4 * count
    signs = tensor_signs(level_l, level_m)
    tau0, tau1, tau2 = tau
    total = 0.0
    for q in range((target - 1) * length, target * length):
        carrier_q = high + q
        for a in range(count):
            carrier_a = high + a
            for b in range(count):
                c = a + b - q
                if not 0 <= c < count:
                    continue
                carrier_b = high + b
                carrier_c = high + c
                sign = signs[q] * signs[a] * signs[b] * signs[c]
                for p1, p2, p3 in (
                    (carrier_a, carrier_b, -carrier_c),
                    (carrier_a, -carrier_c, carrier_b),
                    (-carrier_c, carrier_a, carrier_b),
                ):
                    k1 = -carrier_q + p1
                    k2 = k1 + p2
                    alpha0 = (carrier_q**2 + p1**2 + p2**2 + p3**2) / high**2
                    alpha1 = (k1**2 + p2**2 + p3**2) / high**2
                    alpha2 = (k2**2 + p3**2) / high**2
                    total += sign * math.exp(
                        -tau0 * alpha0 - tau1 * alpha1 - tau2 * alpha2
                    )
    return total


def factorized_layer_sum(
    level_l: int, level_m: int, target: int, tau: tuple[float, float, float]
) -> float:
    length = 1 << level_l
    outputs = 1 << level_m
    count = length * outputs
    high = 4 * count
    signs = tensor_signs(level_l, level_m)
    tau0, tau1, tau2 = tau
    total = 0.0
    carriers = [high + index for index in range(count)]
    scaled = [carrier / high for carrier in carriers]
    for q in range((target - 1) * length, target * length):
        xq = scaled[q]
        outside = signs[q] * math.exp(-tau0 * xq * xq)

        u1 = [
            signs[a]
            * math.exp(-tau0 * scaled[a] ** 2 - tau1 * (scaled[a] - xq) ** 2)
            for a in range(count)
        ]
        v1 = [
            signs[b] * math.exp(-(tau0 + tau1) * scaled[b] ** 2)
            for b in range(count)
        ]
        w1 = [
            signs[c] * math.exp(-(tau0 + tau1 + 2.0 * tau2) * scaled[c] ** 2)
            for c in range(count)
        ]

        u2 = u1
        v2 = [
            signs[b] * math.exp(-(tau0 + tau1 + 2.0 * tau2) * scaled[b] ** 2)
            for b in range(count)
        ]
        w2 = [
            signs[c] * math.exp(-(tau0 + tau1) * scaled[c] ** 2)
            for c in range(count)
        ]

        u3 = [
            signs[a] * math.exp(-(tau0 + tau1) * scaled[a] ** 2)
            for a in range(count)
        ]
        v3 = [
            signs[b] * math.exp(-(tau0 + tau1 + 2.0 * tau2) * scaled[b] ** 2)
            for b in range(count)
        ]
        w3 = [
            signs[c]
            * math.exp(-tau0 * scaled[c] ** 2 - tau1 * (xq + scaled[c]) ** 2)
            for c in range(count)
        ]

        total += outside * sum(
            correlation_coefficient(*weights, q)
            for weights in ((u1, v1, w1), (u2, v2, w2), (u3, v3, w3))
        )
    return total


def exact_convolve(left: list[int], right: list[int]) -> list[int]:
    output = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            output[i + j] += a * b
    return output


def direct_cubic_states(level: int) -> list[list[int]]:
    p, q = rudin_shapiro_pair(level)
    pair = (p, q)
    states: list[list[int]] = []
    for sigma in range(8):
        first = pair[(sigma >> 2) & 1]
        second = pair[(sigma >> 1) & 1]
        third = pair[sigma & 1]
        states.append(exact_convolve(exact_convolve(first, second), list(reversed(third))))
    return states


def lift_step(states: list[list[int]], length: int) -> list[list[int]]:
    old_size = len(states[0])
    new_states = [[0] * (6 * length - 2) for _ in range(8)]
    for sigma in range(8):
        for epsilon in range(8):
            ea = (epsilon >> 2) & 1
            eb = (epsilon >> 1) & 1
            ec = epsilon & 1
            destination = length * (ea + eb - ec) + length
            sign = -1 if (sigma & epsilon).bit_count() % 2 else 1
            child = states[epsilon]
            for index in range(old_size):
                new_states[sigma][destination + index] += sign * child[index]
    return new_states


def cubic_lift_audit(max_level: int) -> tuple[bool, list[dict[str, int | float]]]:
    states = [[1] for _ in range(8)]
    length = 1
    records: list[dict[str, int | float]] = []
    for level in range(1, max_level + 1):
        states = lift_step(states, length)
        length *= 2
        direct = direct_cubic_states(level)
        if states != direct:
            return False, records
        offset = length - 1
        window = [
            (abs(states[0][q + offset]), q)
            for q in range(-1, length + 1)
            if 0 <= q + offset < len(states[0])
        ]
        maximum, exponent = max(window)
        records.append(
            {
                "level": level,
                "M": length,
                "targetWindowMaximum": maximum,
                "exponent": exponent,
                "maximumOverM": maximum / length,
            }
        )
    return True, records


def load_probes(paths: list[Path]) -> list[dict[str, object]]:
    probes: list[dict[str, object]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        probes.append(
            {
                "path": str(path),
                "sha256": sha256(path),
                "M": payload["M"],
                "target": payload["target"],
                "orderedQuarticPaths": payload["orderedQuarticPaths"],
                "S4OverM": float(payload["dimensionlessQuarticKernelSum"])
                / int(payload["M"]),
                "normalizedSignedRatio": payload["normalizedSignedRatio"],
                "cancellationConditionNumber": payload["cancellationConditionNumber"],
                "wallSeconds": payload["wallSeconds"],
                "classification": payload["classification"],
            }
        )
    probes.sort(key=lambda record: int(record["M"]))
    return probes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--probe", type=Path, action="append", default=[])
    parser.add_argument("--max-lift-level", type=int, default=10)
    arguments = parser.parse_args()

    tau_points = [
        (0.0, 0.0, 0.0),
        (0.03, 0.05, 0.07),
        (T / 7.0, T / 5.0, T / 4.0),
    ]
    boxes = [(0, 0), (1, 1), (2, 1), (1, 2)]
    comparisons: list[dict[str, object]] = []
    maximum_residual = 0.0
    for level_l, level_m in boxes:
        outputs = 1 << level_m
        for target, tau in itertools.product(range(1, outputs + 1), tau_points):
            direct = direct_layer_sum(level_l, level_m, target, tau)
            factorized = factorized_layer_sum(level_l, level_m, target, tau)
            residual = abs(direct - factorized)
            scale = max(1.0, abs(direct), abs(factorized))
            relative = residual / scale
            maximum_residual = max(maximum_residual, relative)
            comparisons.append(
                {
                    "levelL": level_l,
                    "levelM": level_m,
                    "target": target,
                    "tau": list(tau),
                    "direct": direct,
                    "factorized": factorized,
                    "relativeResidual": relative,
                }
            )

    lift_ok, lift_records = cubic_lift_audit(arguments.max_lift_level)
    probes = load_probes(arguments.probe)
    checks = {
        "timeLayerFactorizationMatchesDirectPaths": maximum_residual < 5.0e-14,
        "exactEightStateLiftMatchesDirectConvolution": lift_ok,
        "probeClassificationsRemainFiniteEvidence": all(
            "not a proof" in str(record["classification"]) for record in probes
        ),
        "hostileProbeScalesStrictlyIncrease": all(
            int(left["M"]) < int(right["M"])
            for left, right in zip(probes, probes[1:])
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "classification": (
            "exact algebraic transfer regression plus finite long-double stress tests; "
            "not a proof of |S4,m| <= C L^2 M"
        ),
        "checks": checks,
        "timeLayerAudit": {
            "boxes": [list(box) for box in boxes],
            "tauPoints": [list(tau) for tau in tau_points],
            "comparisons": len(comparisons),
            "maximumRelativeResidual": maximum_residual,
        },
        "cubicLift": {
            "baseStates": 2,
            "cubicStates": 8,
            "targetSignedStates": 16,
            "carryShifts": [-1, 0, 1, 2],
            "exactLevelsChecked": arguments.max_lift_level,
            "records": lift_records,
        },
        "hostileWeightedProbes": probes,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(arguments.output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
