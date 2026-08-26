#!/usr/bin/env python3
"""Independent numerical audit for R0.71Q.

This checker imports neither the exact producer nor previous release code. It
samples finite Blaschke products on the unit circle, checks their prescribed
zeros and crossing orientations, probes the extracted Temam disk, and audits
the component-union and covering-scale ledgers.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from time import perf_counter

import numpy as np


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def blaschke_value(z: np.ndarray | complex, zeros: np.ndarray) -> np.ndarray | complex:
    value = np.ones_like(z, dtype=np.complex128) if isinstance(z, np.ndarray) else 1.0 + 0.0j
    for zero in zeros:
        value = value * (z - zero) / (1.0 - zero * z)
    return value


def blaschke_checks() -> dict[str, object]:
    rows = []
    max_boundary_error = 0.0
    max_zero_residual = 0.0
    max_jensen_identity_error = 0.0
    for n in (1, 2, 4, 8, 16, 32, 64):
        indices = np.arange(1, n + 1, dtype=np.float64)
        zeros = (2.0 * n * n - indices) / (4.0 * n * n)
        angles = np.linspace(0.0, 2.0 * np.pi, 8192, endpoint=False)
        boundary = blaschke_value(np.exp(1j * angles), zeros)
        boundary_error = float(np.max(np.abs(np.abs(boundary) - 1.0)))
        zero_residual = float(max(abs(blaschke_value(complex(zero), zeros)) for zero in zeros))

        log_anchor_direct = -float(np.sum(np.log(zeros)))
        center = complex(blaschke_value(0.0 + 0.0j, zeros))
        log_anchor_product = -math.log(abs(center))
        identity_error = abs(log_anchor_direct - log_anchor_product)

        signs = []
        for index, zero in enumerate(zeros):
            sign = 1.0
            for other_index, other in enumerate(zeros):
                if index == other_index:
                    continue
                sign *= math.copysign(1.0, zero - other)
            signs.append(1 if sign > 0 else -1)
        upward = sum(sign > 0 for sign in signs)

        require(boundary_error < 5e-13, f"N={n} unit boundary")
        require(zero_residual < 5e-13, f"N={n} prescribed zeros")
        require(identity_error < 2e-13, f"N={n} anchor product")
        require(upward == (n + 1) // 2, f"N={n} upward crossings")

        max_boundary_error = max(max_boundary_error, boundary_error)
        max_zero_residual = max(max_zero_residual, zero_residual)
        max_jensen_identity_error = max(max_jensen_identity_error, identity_error)
        rows.append({
            "N": n,
            "boundaryModulusMaximumError": boundary_error,
            "maximumPrescribedZeroResidual": zero_residual,
            "minusLogCenterAnchor": log_anchor_direct,
            "jensenBound": log_anchor_direct / math.log(2.0),
            "jensenBoundMinusN": log_anchor_direct / math.log(2.0) - n,
            "anchorProductLogError": identity_error,
            "positiveDerivativeZeroCount": upward,
            "squaredFamilyPositiveEntryCount": n,
        })

    return {
        "passed": True,
        "circleSampleCount": 8192,
        "maximumBoundaryModulusError": max_boundary_error,
        "maximumZeroResidual": max_zero_residual,
        "maximumAnchorProductLogError": max_jensen_identity_error,
        "rows": rows,
    }


def lobe_disk_sampling() -> dict[str, object]:
    generator = np.random.default_rng(71072)
    count = 200_000
    radius = np.sqrt(generator.random(count)) / 64.0
    angle = generator.random(count) * 2.0 * np.pi
    x = 0.25 + radius * np.cos(angle)
    y = radius * np.sin(angle)
    residual = x**3 - (x**2 + y**2) ** 2
    minimum = float(np.min(residual))
    require(minimum > 0.0, "sampled disk lies in normalized Temam lobe")
    return {
        "passed": True,
        "seed": 71072,
        "sampleCount": count,
        "diskCenter": 0.25,
        "diskRadius": 1.0 / 64.0,
        "minimumLobeResidual": minimum,
    }


def union_tax_checks() -> dict[str, object]:
    rows = []
    per_component_bound = math.log(6.0) / math.log(4.0 / 3.0)
    for count in (1, 2, 4, 8, 16, 32, 64):
        indices = np.arange(1, count + 1, dtype=np.float64)
        zeros = 0.25 + indices / (4.0 * (count + 1.0))
        anchors = zeros.copy()
        sup_bounds = 1.0 + zeros
        require(float(np.min(anchors)) > 0.25, f"Q={count} anchor")
        require(float(np.max(sup_bounds)) < 1.5, f"Q={count} sup")
        require(len(np.unique(zeros)) == count, f"Q={count} union")
        rows.append({
            "componentCount": count,
            "distinctUnionZeroCount": len(np.unique(zeros)),
            "minimumAnchor": float(np.min(anchors)),
            "maximumOuterDiskSupBound": float(np.max(sup_bounds)),
            "uniformPerComponentJensenBound": per_component_bound,
        })
    return {"passed": True, "rows": rows}


def covering_scale_checks() -> dict[str, object]:
    rows = []
    for enstrophy in (0.0, 0.25, 1.0, 4.0, 16.0, 64.0, 256.0):
        temam_scale = (1.0 + enstrophy) ** -2
        inner_radius = temam_scale / 256.0
        safe_cover_bound = 2 + math.ceil(2.0 / inner_radius)
        rows.append({
            "Y": enstrophy,
            "normalizedTemamScale": temam_scale,
            "innerCountingRadius": inner_radius,
            "safeUnitIntervalCoverBound": safe_cover_bound,
            "inverseScale": 1.0 / temam_scale,
        })
    require(rows[-1]["inverseScale"] > 60_000.0, "cover cost growth")
    return {"passed": True, "rows": rows}


def local_window_family_checks() -> dict[str, object]:
    angles = np.linspace(0.0, 2.0 * np.pi, 16384, endpoint=False)
    theoretical = math.cosh(3.0 * math.pi / 4.0) ** 2
    rows = []
    maximum_ratio = 0.0
    for n in (1, 2, 4, 8, 16, 32, 64):
        center = 0.5 / n
        outer_radius = 0.75 / n
        z = center + outer_radius * np.exp(1j * angles)
        values = (np.sin(np.pi * n * z) / (np.pi * n)) ** 2
        anchor = abs((np.sin(np.pi * n * center) / (np.pi * n)) ** 2)
        ratio = float(np.max(np.abs(values)) / anchor)
        require(ratio <= theoretical * (1.0 + 5e-13), f"N={n} local relative growth")
        maximum_ratio = max(maximum_ratio, ratio)
        rows.append({
            "N": n,
            "ownedEntryCount": n,
            "ownedWindowCount": n,
            "sampledRelativeGrowth": ratio,
            "theoreticalRelativeGrowthBound": theoretical,
            "centerAnchor": anchor,
        })
    return {
        "passed": True,
        "circleSampleCount": len(angles),
        "maximumSampledRelativeGrowth": maximum_ratio,
        "theoreticalRelativeGrowthBound": theoretical,
        "rows": rows,
    }


def build_result() -> dict[str, object]:
    started = perf_counter()
    checks = {
        "blaschkeChecks": blaschke_checks(),
        "lobeDiskSampling": lobe_disk_sampling(),
        "unionTaxChecks": union_tax_checks(),
        "localWindowFamilyChecks": local_window_family_checks(),
        "coveringScaleChecks": covering_scale_checks(),
    }
    require(all(check["passed"] for check in checks.values()), "all independent checks")
    return {
        "release": "R0.71Q",
        "status": "passed",
        "elapsedSeconds": perf_counter() - started,
        "checks": checks,
        "scope": (
            "independent numerical corroboration of finite analytic geometry "
            "and counterfamilies; no PDE time evolution and no NSE zero-count "
            "or regularity claim"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
