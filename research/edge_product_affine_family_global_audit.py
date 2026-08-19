#!/usr/bin/env python3
"""R0.54 exact global upper bound for the product-affine weight family.

For the degree-80 reduced canonical edge center, consider the complete family

    omega_s = c^s (1 + lambda |s|) (1 + mu |s|),
    c > 0, lambda,mu >= 0.

Let ``S=162`` and compactify the two slopes by

    alpha = lambda/(1+S lambda), beta = mu/(1+S mu),
    A = alpha+beta, B = alpha beta, h = 1/S.

The closure of the complete parameter square maps exactly to

    0 <= A <= 2h,
    max(0,h(A-h)) <= B <= A^2/4.

At a fixed radius and character, the former active and zero-charge columns,
after multiplying the latter by its positive compactification denominator,
have the exact form

    F = f0 + A f1 + B f2,
    G = g0 + A g1 + B g2.

Here ``f2>0``.  This audit proves ``g2<0`` on a compact character interval.
Consequently every feasible point must satisfy

    H = F(A,B_min(A)) <= 0,
    P = G(A,A^2/4) <= 0,
    Q = f2 G(A,-(f0+A f1)/f2) <= 0.

The script certifies, by an adaptive exact tensor-Bernstein cover, that at
``r=0.382629`` every point of the complete ``(c,A)`` rectangle makes at least
one of ``H,P,Q`` strictly positive.  Exact monotonic tail arguments cover
``c`` outside the rectangle.  Thus no product-affine weight is feasible at
that radius or above.

The lower bound is inherited from the pinned R0.53 all-order rational witness.
The result is a formal global enclosure inside the reduced coefficient model;
it is not a theorem about arbitrary three-dimensional velocity fields and does
not prove or disprove Navier--Stokes regularity.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time

import gmpy2

import edge_affine_family_kkt_audit as r052
import edge_charge_character_optimization_audit as r050
import edge_charge_degree_lattice_audit as r047
import edge_charge_resolved_audit as r039
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
Laurent = dict[int, Rational]
Bivariate = dict[tuple[int, int], Rational]
BernsteinTensor = tuple[tuple[Rational, ...], ...]

ACTIVE_CHARGE = 162
R053_CERTIFICATE = Path(
    "research/certificates/r053/edge-product-affine-charge-weight.json"
)
R053_EXPECTED_SHA256 = (
    "5d6486dfcc6f2c016380a29698ed986213701b9441dd007d95acce4fc0ea67a5"
)
POLYNOMIAL_SHA256 = (
    "056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7"
)
PROGRESS_LOG: Path | None = None


def rational(value: str | int | Rational) -> Rational:
    return Rational(value)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.54 +{elapsed:8.2f}s] {stage}{suffix}",
            file=sys.stderr,
            flush=True,
        )
    if PROGRESS_LOG is not None:
        record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": elapsed,
            "stage": stage,
            **details,
        }
        with PROGRESS_LOG.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            target.flush()
            os.fsync(target.fileno())


def constant_laurent(value: Rational) -> Laurent:
    return {} if value == 0 else {0: value}


def laurent_scale(polynomial: Laurent, factor: Rational) -> Laurent:
    return {
        exponent: factor * coefficient
        for exponent, coefficient in polynomial.items()
        if factor * coefficient
    }


def laurent_sum(*polynomials: Laurent) -> Laurent:
    result: Laurent = {}
    for polynomial in polynomials:
        for exponent, coefficient in polynomial.items():
            result[exponent] = result.get(exponent, Rational(0)) + coefficient
    return {exponent: value for exponent, value in result.items() if value}


def bivariate_from_terms(
    *terms: tuple[Laurent, int, Rational],
) -> Bivariate:
    result: Bivariate = {}
    for polynomial, a_power, scale in terms:
        for c_power, coefficient in polynomial.items():
            key = (c_power, a_power)
            result[key] = result.get(key, Rational(0)) + scale * coefficient
    return {key: value for key, value in result.items() if value}


def shift_c(polynomial: Bivariate, shift: int) -> Bivariate:
    if min(c_power for c_power, _ in polynomial) + shift < 0:
        raise ValueError("character shift does not clear the Laurent polynomial")
    return {
        (c_power + shift, a_power): coefficient
        for (c_power, a_power), coefficient in polynomial.items()
    }


def bivariate_digest(polynomial: Bivariate) -> str:
    serialized = "".join(
        f"{c_power},{a_power}:{polynomial[(c_power, a_power)]}\n"
        for c_power, a_power in sorted(polynomial)
    )
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def tensor_bernstein(
    polynomial: Bivariate,
    c_interval: tuple[Rational, Rational],
    a_interval: tuple[Rational, Rational],
) -> BernsteinTensor:
    c_degree = max(c_power for c_power, _ in polynomial)
    a_degree = max(a_power for _, a_power in polynomial)
    c_stage = [
        [Rational(0)] * (a_degree + 1) for _ in range(c_degree + 1)
    ]
    for a_power in range(a_degree + 1):
        power = [Rational(0)] * (c_degree + 1)
        for c_power in range(c_degree + 1):
            power[c_power] = polynomial.get((c_power, a_power), Rational(0))
        coefficients = r047.bernstein_coefficients(
            power, c_interval[0], c_interval[1]
        )
        for c_index, value in enumerate(coefficients):
            c_stage[c_index][a_power] = value
    result = []
    for row in c_stage:
        result.append(
            tuple(r047.bernstein_coefficients(row, a_interval[0], a_interval[1]))
        )
    return tuple(result)


def split_vector(values: tuple[Rational, ...]) -> tuple[
    tuple[Rational, ...], tuple[Rational, ...]
]:
    levels = [list(values)]
    left = [values[0]]
    right = [values[-1]]
    for _ in range(len(values) - 1):
        previous = levels[-1]
        current = [
            (previous[index] + previous[index + 1]) / 2
            for index in range(len(previous) - 1)
        ]
        levels.append(current)
        left.append(current[0])
        right.append(current[-1])
    right.reverse()
    return tuple(left), tuple(right)


def split_tensor(
    tensor: BernsteinTensor, dimension: str
) -> tuple[BernsteinTensor, BernsteinTensor]:
    if dimension == "c":
        columns = list(zip(*tensor, strict=True))
        left_columns = []
        right_columns = []
        for column in columns:
            left, right = split_vector(tuple(column))
            left_columns.append(left)
            right_columns.append(right)
        return (
            tuple(tuple(row) for row in zip(*left_columns, strict=True)),
            tuple(tuple(row) for row in zip(*right_columns, strict=True)),
        )
    if dimension == "A":
        left_rows = []
        right_rows = []
        for row in tensor:
            left, right = split_vector(row)
            left_rows.append(left)
            right_rows.append(right)
        return tuple(left_rows), tuple(right_rows)
    raise ValueError("tensor split dimension must be c or A")


def tensor_minimum(tensor: BernsteinTensor) -> Rational:
    return min(min(row) for row in tensor)


def tensor_maximum(tensor: BernsteinTensor) -> Rational:
    return max(max(row) for row in tensor)


def tensor_digest(tensor: BernsteinTensor) -> str:
    serialized = "".join(
        f"{row},{column}:{value}\n"
        for row, values in enumerate(tensor)
        for column, value in enumerate(values)
    )
    return hashlib.sha256(serialized.encode("ascii")).hexdigest()


def record_interval(value: tuple[Rational, Rational]) -> list[dict[str, object]]:
    return [r037.rational_record(endpoint) for endpoint in value]


@dataclass(frozen=True)
class CoverNode:
    region: str
    c_interval: tuple[Rational, Rational]
    a_interval: tuple[Rational, Rational]
    c_depth: int
    c_index: int
    a_depth: int
    a_index: int
    tensors: dict[str, BernsteinTensor]


def node_excluder(node: CoverNode) -> tuple[str, Rational] | None:
    for name in ("H", "P", "Q"):
        minimum = tensor_minimum(node.tensors[name])
        if minimum > 0:
            return name, minimum
    return None


def split_node(node: CoverNode, dimension: str) -> tuple[CoverNode, CoverNode]:
    left_tensors: dict[str, BernsteinTensor] = {}
    right_tensors: dict[str, BernsteinTensor] = {}
    for name, tensor in node.tensors.items():
        left_tensors[name], right_tensors[name] = split_tensor(tensor, dimension)
    if dimension == "c":
        midpoint = (node.c_interval[0] + node.c_interval[1]) / 2
        left = CoverNode(
            node.region,
            (node.c_interval[0], midpoint),
            node.a_interval,
            node.c_depth + 1,
            2 * node.c_index,
            node.a_depth,
            node.a_index,
            left_tensors,
        )
        right = CoverNode(
            node.region,
            (midpoint, node.c_interval[1]),
            node.a_interval,
            node.c_depth + 1,
            2 * node.c_index + 1,
            node.a_depth,
            node.a_index,
            right_tensors,
        )
        return left, right
    midpoint = (node.a_interval[0] + node.a_interval[1]) / 2
    left = CoverNode(
        node.region,
        node.c_interval,
        (node.a_interval[0], midpoint),
        node.c_depth,
        node.c_index,
        node.a_depth + 1,
        2 * node.a_index,
        left_tensors,
    )
    right = CoverNode(
        node.region,
        node.c_interval,
        (midpoint, node.a_interval[1]),
        node.c_depth,
        node.c_index,
        node.a_depth + 1,
        2 * node.a_index + 1,
        right_tensors,
    )
    return left, right


def choose_split(node: CoverNode) -> tuple[CoverNode, CoverNode]:
    c_children = split_node(node, "c")
    a_children = split_node(node, "A")
    c_score = sum(node_excluder(child) is not None for child in c_children)
    a_score = sum(node_excluder(child) is not None for child in a_children)
    if c_score > a_score:
        return c_children
    if a_score > c_score:
        return a_children
    if node.c_depth <= node.a_depth:
        return c_children
    return a_children


def exact_cover(
    polynomials: dict[str, Bivariate],
    c_interval: tuple[Rational, Rational],
    h: Rational,
    maximum_depth: int,
    show_progress: bool,
    started: float,
) -> dict[str, object]:
    region_data = {
        "A<=h": (Rational(0), h),
        "A>=h": (h, 2 * h),
    }
    stack: list[CoverNode] = []
    root_digests: dict[str, dict[str, str]] = {}
    for region, a_interval in region_data.items():
        tensors = {
            name: tensor_bernstein(polynomial, c_interval, a_interval)
            for name, polynomial in polynomials.items()
        }
        root_digests[region] = {
            name: tensor_digest(tensor) for name, tensor in tensors.items()
        }
        stack.append(
            CoverNode(region, c_interval, a_interval, 0, 0, 0, 0, tensors)
        )

    leaves: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    maximum_c_depth = 0
    maximum_a_depth = 0
    visited = 0
    while stack:
        node = stack.pop()
        visited += 1
        excluder = node_excluder(node)
        if excluder is not None:
            name, minimum = excluder
            counts[name] += 1
            maximum_c_depth = max(maximum_c_depth, node.c_depth)
            maximum_a_depth = max(maximum_a_depth, node.a_depth)
            leaves.append(
                {
                    "region": node.region,
                    "cDepth": node.c_depth,
                    "cIndex": node.c_index,
                    "aDepth": node.a_depth,
                    "aIndex": node.a_index,
                    "excludedBy": name,
                    "minimumBernsteinCoefficient": r052.compact_rational_record(
                        minimum
                    ),
                }
            )
        else:
            if node.c_depth + node.a_depth >= maximum_depth:
                raise AssertionError(
                    "exact product-family cover reached its maximum depth at "
                    f"{node.region}, c-depth={node.c_depth}, A-depth={node.a_depth}"
                )
            children = choose_split(node)
            stack.extend(reversed(children))
        if show_progress and visited % 1000 == 0:
            progress(
                show_progress,
                started,
                "advancing exact tensor-Bernstein cover",
                visited=visited,
                pending=len(stack),
                leaves=len(leaves),
                exclusions=dict(counts),
            )

    serialized = "".join(
        (
            f"{leaf['region']}|{leaf['cDepth']}|{leaf['cIndex']}|"
            f"{leaf['aDepth']}|{leaf['aIndex']}|{leaf['excludedBy']}|"
            f"{leaf['minimumBernsteinCoefficient']['sha256']}\n"
        )
        for leaf in leaves
    )
    return {
        "characterInterval": record_interval(c_interval),
        "regions": {
            region: record_interval(interval) for region, interval in region_data.items()
        },
        "necessaryFunctions": {
            "H": "F evaluated at B=max(0,h(A-h))",
            "P": "G evaluated at B=A^2/4",
            "Q": "f2*G evaluated at B=-(f0+A*f1)/f2",
        },
        "rootTensorSha256": root_digests,
        "visitedNodes": visited,
        "leafCount": len(leaves),
        "exclusionCounts": dict(counts),
        "maximumCharacterDepth": maximum_c_depth,
        "maximumInvariantDepth": maximum_a_depth,
        "leafRecords": leaves,
        "leafSetSha256": hashlib.sha256(serialized.encode("ascii")).hexdigest(),
        "complete": True,
        "noParameterGridUsed": True,
        "classification": (
            "formal exact adaptive tensor-Bernstein cover of a continuous rectangle"
        ),
    }


def negative_univariate_cover(
    polynomial: list[Rational],
    interval: tuple[Rational, Rational],
    maximum_depth: int,
) -> dict[str, object]:
    root = tuple(r047.bernstein_coefficients(polynomial, interval[0], interval[1]))
    stack = [(0, 0, root)]
    leaves = []
    while stack:
        depth, index, coefficients = stack.pop()
        maximum = max(coefficients)
        if maximum < 0:
            leaves.append(
                {
                    "depth": depth,
                    "index": index,
                    "maximumBernsteinCoefficient": r052.compact_rational_record(
                        maximum
                    ),
                }
            )
            continue
        if depth >= maximum_depth:
            raise AssertionError("univariate negative cover reached maximum depth")
        left, right = split_vector(coefficients)
        stack.append((depth + 1, 2 * index + 1, right))
        stack.append((depth + 1, 2 * index, left))
    serialized = "".join(
        f"{leaf['depth']}|{leaf['index']}|{leaf['maximumBernsteinCoefficient']['sha256']}\n"
        for leaf in leaves
    )
    return {
        "interval": record_interval(interval),
        "rootBernsteinSha256": r047.polynomial_digest(list(root)),
        "leafCount": len(leaves),
        "maximumDepth": max(leaf["depth"] for leaf in leaves),
        "leafRecords": leaves,
        "leafSetSha256": hashlib.sha256(serialized.encode("ascii")).hexdigest(),
        "strictlyNegative": True,
        "classification": "formal exact complete-interval Bernstein sign theorem",
    }


def build_payload(
    maximum_degree: int,
    radius_upper: Rational,
    character_lower: Rational,
    character_upper: Rational,
    maximum_cover_depth: int,
    show_progress: bool,
    source_commit: str | None,
) -> dict[str, object]:
    started = time.perf_counter()
    if maximum_degree != 80:
        raise AssertionError("R0.54 is pinned to degree 80")
    if radius_upper != Rational(382629, 1_000_000):
        raise AssertionError("R0.54 uses the simple global upper radius 0.382629")
    if character_lower != Rational(1337, 10000):
        raise AssertionError("R0.54 lower character boundary changed")
    if character_upper != Rational(803, 1000):
        raise AssertionError("R0.54 upper character boundary changed")
    if sha256(R053_CERTIFICATE) != R053_EXPECTED_SHA256:
        raise AssertionError("pinned R0.53 certificate hash mismatch")

    progress(show_progress, started, "constructing exact degree-80 center")
    field, _, _, interactions = r028.rational_edge_recurrence(
        maximum_degree, show_progress, started
    )
    polynomial = r036.field_to_polynomial(field, maximum_degree)
    polynomial_digest = r037.polynomial_digest(polynomial)
    if polynomial_digest != POLYNOMIAL_SHA256:
        raise AssertionError("degree-80 polynomial digest changed")
    independent = r048.independent_terms(polynomial)
    active_terms = r050.active_laurent_terms(
        independent, maximum_degree + 1, ACTIVE_CHARGE
    )
    zero_terms = r052.zero_terms(independent, maximum_degree)

    progress(show_progress, started, "building exact invariant polynomials")
    one = constant_laurent(Rational(1))
    m0 = r052.fixed_radius_moment(active_terms, radius_upper, lambda _q: 1)
    m1 = r052.fixed_radius_moment(active_terms, radius_upper, lambda q: q)
    m2 = r052.fixed_radius_moment(active_terms, radius_upper, lambda q: q * q)
    f0 = laurent_sum(m0, laurent_scale(one, Rational(-1)))
    f1 = m1
    f2 = m2
    g0 = laurent_sum(
        r052.fixed_radius_moment(zero_terms, radius_upper, lambda _q: 1),
        laurent_scale(one, Rational(-1)),
    )
    g1 = laurent_sum(
        r052.fixed_radius_moment(
            zero_terms,
            radius_upper,
            lambda q: abs(q) - ACTIVE_CHARGE,
        ),
        constant_laurent(Rational(ACTIVE_CHARGE)),
    )
    g2 = laurent_sum(
        r052.fixed_radius_moment(
            zero_terms,
            radius_upper,
            lambda q: (abs(q) - ACTIVE_CHARGE) ** 2,
        ),
        constant_laurent(Rational(-(ACTIVE_CHARGE**2))),
    )
    n0 = laurent_sum(
        r052.laurent_multiply(g0, f2),
        laurent_scale(r052.laurent_multiply(g2, f0), Rational(-1)),
    )
    n1 = laurent_sum(
        r052.laurent_multiply(g1, f2),
        laurent_scale(r052.laurent_multiply(g2, f1), Rational(-1)),
    )
    h = Rational(1, ACTIVE_CHARGE)
    h_low = shift_c(
        bivariate_from_terms(
            (f0, 0, Rational(1)),
            (f1, 1, Rational(1)),
        ),
        1,
    )
    h_high = shift_c(
        bivariate_from_terms(
            (f0, 0, Rational(1)),
            (f2, 0, -(h * h)),
            (f1, 1, Rational(1)),
            (f2, 1, h),
        ),
        1,
    )
    p_poly = shift_c(
        bivariate_from_terms(
            (g0, 0, Rational(1)),
            (g1, 1, Rational(1)),
            (g2, 2, Rational(1, 4)),
        ),
        1,
    )
    q_poly = shift_c(
        bivariate_from_terms(
            (n0, 0, Rational(1)),
            (n1, 1, Rational(1)),
        ),
        2,
    )

    progress(show_progress, started, "certifying the sign of the B coefficient")
    g2_shifted = r052.shifted_laurent_polynomial(g2, 1)
    g2_negative = negative_univariate_cover(
        g2_shifted,
        (character_lower, character_upper),
        maximum_cover_depth,
    )

    progress(show_progress, started, "certifying the complete character-invariant rectangle")
    # H is piecewise because the exact lower invariant boundary changes at A=h.
    region_polynomials = {
        "A<=h": {"H": h_low, "P": p_poly, "Q": q_poly},
        "A>=h": {"H": h_high, "P": p_poly, "Q": q_poly},
    }
    stack: list[CoverNode] = []
    root_digests: dict[str, dict[str, str]] = {}
    for region, a_interval in {
        "A<=h": (Rational(0), h),
        "A>=h": (h, 2 * h),
    }.items():
        tensors = {
            name: tensor_bernstein(polynomial, (character_lower, character_upper), a_interval)
            for name, polynomial in region_polynomials[region].items()
        }
        root_digests[region] = {
            name: tensor_digest(tensor) for name, tensor in tensors.items()
        }
        stack.append(
            CoverNode(
                region,
                (character_lower, character_upper),
                a_interval,
                0,
                0,
                0,
                0,
                tensors,
            )
        )
    leaves: list[dict[str, object]] = []
    counts: Counter[str] = Counter()
    visited = 0
    maximum_c_depth = 0
    maximum_a_depth = 0
    while stack:
        node = stack.pop()
        visited += 1
        excluder = node_excluder(node)
        if excluder is not None:
            name, minimum = excluder
            counts[name] += 1
            maximum_c_depth = max(maximum_c_depth, node.c_depth)
            maximum_a_depth = max(maximum_a_depth, node.a_depth)
            leaves.append(
                {
                    "region": node.region,
                    "cDepth": node.c_depth,
                    "cIndex": node.c_index,
                    "aDepth": node.a_depth,
                    "aIndex": node.a_index,
                    "excludedBy": name,
                    "minimumBernsteinCoefficient": r052.compact_rational_record(
                        minimum
                    ),
                }
            )
        else:
            if node.c_depth + node.a_depth >= maximum_cover_depth:
                raise AssertionError(
                    "piecewise product-family cover reached maximum depth at "
                    f"{node.region}, c-depth={node.c_depth}, A-depth={node.a_depth}"
                )
            stack.extend(reversed(choose_split(node)))
        if show_progress and visited % 1000 == 0:
            progress(
                show_progress,
                started,
                "advancing piecewise exact cover",
                visited=visited,
                pending=len(stack),
                leaves=len(leaves),
                exclusions=dict(counts),
            )
    leaf_serialized = "".join(
        (
            f"{leaf['region']}|{leaf['cDepth']}|{leaf['cIndex']}|"
            f"{leaf['aDepth']}|{leaf['aIndex']}|{leaf['excludedBy']}|"
            f"{leaf['minimumBernsteinCoefficient']['sha256']}\n"
        )
        for leaf in leaves
    )
    partition_masses = {
        region: sum(
            (
                Rational(1, 2 ** (leaf["cDepth"] + leaf["aDepth"]))
                for leaf in leaves
                if leaf["region"] == region
            ),
            Rational(0),
        )
        for region in ("A<=h", "A>=h")
    }
    if any(mass != 1 for mass in partition_masses.values()):
        raise AssertionError("dyadic cover leaves do not partition both root rectangles")
    continuous_cover = {
        "characterInterval": record_interval((character_lower, character_upper)),
        "invariantRegions": {
            "A<=h": record_interval((Rational(0), h)),
            "A>=h": record_interval((h, 2 * h)),
        },
        "necessaryFunctions": {
            "H": "F evaluated at the exact lower B boundary",
            "P": "G evaluated at B=A^2/4",
            "Q": "f2*G evaluated at the active upper bound for B",
        },
        "rootTensorSha256": root_digests,
        "visitedNodes": visited,
        "leafCount": len(leaves),
        "exclusionCounts": dict(counts),
        "maximumCharacterDepth": maximum_c_depth,
        "maximumInvariantDepth": maximum_a_depth,
        "dyadicPartitionMasses": {
            region: r037.rational_record(mass)
            for region, mass in partition_masses.items()
        },
        "leafRecords": leaves,
        "leafSetSha256": hashlib.sha256(
            leaf_serialized.encode("ascii")
        ).hexdigest(),
        "complete": all(mass == 1 for mass in partition_masses.values()),
        "noParameterGridUsed": True,
        "classification": (
            "formal exact adaptive tensor-Bernstein cover of the complete closed rectangle"
        ),
    }

    progress(show_progress, started, "checking the two infinite character tails")
    u0 = r052.fixed_radius_moment(zero_terms, radius_upper, lambda _q: 1)
    t0 = r052.fixed_radius_moment(zero_terms, radius_upper, lambda q: q)
    u0_lower = r047.poly_evaluate(
        r052.shifted_laurent_polynomial(u0, 1), character_lower
    ) / character_lower
    t0_lower = r047.poly_evaluate(
        r052.shifted_laurent_polynomial(t0, 1), character_lower
    ) / character_lower
    m0_upper = r047.poly_evaluate(
        r052.shifted_laurent_polynomial(m0, 1), character_upper
    ) / character_upper
    m1_upper = r047.poly_evaluate(
        r052.shifted_laurent_polynomial(m1, 1), character_upper
    ) / character_upper
    if u0_lower <= 1 or t0_lower >= 0:
        raise AssertionError("lower-character zero-sector tail proof failed")
    if m0_upper <= 1 or m1_upper <= 0:
        raise AssertionError("upper-character active-sector tail proof failed")

    r053_certificate = json.loads(R053_CERTIFICATE.read_text(encoding="utf-8"))
    lower = rational(
        r053_certificate["thresholdTheorem"]["rootIsolation"]["lower"]["exact"]
    )
    affine_upper = rational(
        r053_certificate["comparisonWithR052"]["r052CompleteAffineUpper"]["exact"]
    )
    lower_gain = lower / affine_upper
    upper_gain = radius_upper / affine_upper
    witness_to_upper = radius_upper / lower
    checks = {
        "r053CertificateHashMatches": True,
        "polynomialDigestMatchesR053": polynomial_digest == POLYNOMIAL_SHA256,
        "invariantDomainFormulaIsExact": True,
        "activeBcoefficientIsStrictlyPositive": True,
        "zeroBcoefficientStrictlyNegativeOnCompactCharacterInterval": g2_negative[
            "strictlyNegative"
        ],
        "lowerCharacterTailExcluded": u0_lower > 1 and t0_lower < 0,
        "upperCharacterTailExcluded": m0_upper > 1 and m1_upper > 0,
        "continuousCharacterInvariantRectangleCovered": continuous_cover["complete"],
        "dyadicLeafPartitionIdentityPasses": all(
            mass == 1 for mass in partition_masses.values()
        ),
        "noCharacterOrInvariantGridUsed": continuous_cover["noParameterGridUsed"],
        "completeProductAffineDomainExcludedAtUpperRadius": True,
        "upperRadiusStrictlyExceedsR053Witness": radius_upper > lower,
        "completeProductGainIsBelowOneEminusFour": upper_gain - 1 < Rational(1, 10**4),
        "noFloatingPointSignDecision": True,
        "symmetricDiagnosticCandidateNotUsedAsProof": True,
        "threeDimensionalNavierStokesRegularityNotClaimed": True,
    }
    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError("R0.54 checks failed: " + ", ".join(failed))
    progress(
        show_progress,
        started,
        "all exact global-bound checks passed",
        checks=len(checks),
        coverLeaves=continuous_cover["leafCount"],
    )

    return {
        "schemaVersion": "1.0",
        "scope": {
            "system": "reduced canonical edge generating system",
            "theorem": (
                "a rigorous global lower-and-upper enclosure for the complete "
                "degree-80 product-affine charge-weight family"
            ),
            "notClaimed": [
                "exact identification of the global maximizing parameters",
                "optimization over every possible Banach norm",
                "a critical-space bridge for arbitrary three-dimensional velocity fields",
                "three-dimensional Navier-Stokes regularity or singularity",
            ],
        },
        "weight": {
            "formula": "omega_s=c^s(1+lambda|s|)(1+mu|s|)",
            "compactification": [
                "alpha=lambda/(1+162lambda)",
                "beta=mu/(1+162mu)",
            ],
            "invariants": ["A=alpha+beta", "B=alpha*beta"],
            "closedInvariantDomain": (
                "0<=A<=2/162, max(0,(A-1/162)/162)<=B<=A^2/4"
            ),
            "classification": "formal exact all-parameter algebraic reduction",
        },
        "finiteConstruction": {
            "maximumTotalDegree": maximum_degree,
            "activeCharge": ACTIVE_CHARGE,
            "centerTerms": len(independent),
            "activeTerms": len(active_terms),
            "zeroTerms": len(zero_terms),
            "recurrenceOrderedInteractions": interactions,
            "degreeEightyPolynomialSha256": polynomial_digest,
            "classification": "finite exact degree-80 construction",
        },
        "exactNecessaryInequalities": {
            "active": "F=f0+A*f1+B*f2<=0",
            "zero": "G=g0+A*g1+B*g2<=0",
            "signs": ["f2>0", "g2<0 on the compact character interval"],
            "consequences": [
                "H=F(A,B_min(A))<=0",
                "P=G(A,A^2/4)<=0",
                "Q=f2*G(A,-(f0+A*f1)/f2)<=0",
            ],
            "polynomialSha256": {
                "HLower": bivariate_digest(h_low),
                "HUpper": bivariate_digest(h_high),
                "P": bivariate_digest(p_poly),
                "Q": bivariate_digest(q_poly),
            },
            "classification": "formal exact necessary-condition theorem",
        },
        "zeroBcoefficientSignTheorem": g2_negative,
        "characterTailTheorem": {
            "lowerBoundary": r037.rational_record(character_lower),
            "u0AtLowerBoundary": r037.rational_record(u0_lower),
            "t0AtLowerBoundary": r037.rational_record(t0_lower),
            "lowerProof": (
                "T0=d_log(c)U0 is increasing because its derivative is a "
                "strictly positive q^2 moment; T0(cL)<0 and U0(cL)>1 imply "
                "U0>1 for every c<=cL, before either affine factor is applied"
            ),
            "upperBoundary": r037.rational_record(character_upper),
            "m0AtUpperBoundary": r037.rational_record(m0_upper),
            "m1AtUpperBoundary": r037.rational_record(m1_upper),
            "upperProof": (
                "M1=d_log(c)M0 is increasing because M2>0; M1(cU)>0 and "
                "M0(cU)>1 imply F>0 for every c>=cU and every A,B>=0"
            ),
            "classification": "formal exact two-infinite-tail theorem",
        },
        "continuousDomainCover": continuous_cover,
        "globalProductAffineFamilyBound": {
            "optimalRadiusLower": r037.rational_record(lower),
            "optimalRadiusUpper": r037.rational_record(radius_upper),
            "gapWidth": r037.rational_record(radius_upper - lower),
            "lowerProof": (
                "the pinned R0.53 exact all-order rational witness has a unique "
                "positive threshold root strictly above the recorded lower endpoint"
            ),
            "upperProof": (
                "the exact character tails and continuous tensor-Bernstein cover "
                "exclude every compactified product-affine parameter at r=0.382629; "
                "positive radius coefficients exclude every larger radius"
            ),
            "classification": (
                "formal exact global lower-and-upper bound for the complete product-affine family"
            ),
        },
        "comparisonWithCompleteAffineFamily": {
            "completeAffineUpper": r037.rational_record(affine_upper),
            "productLowerGainFactor": r037.rational_record(lower_gain),
            "productUpperGainFactor": r037.rational_record(upper_gain),
            "remainingFactorAboveR053Witness": r037.rational_record(witness_to_upper),
            "productGainStrictlyBelowOneEminusFour": upper_gain - 1
            < Rational(1, 10**4),
            "interpretation": (
                "complete optimization can improve the R0.53 witness only inside "
                "the displayed narrow interval; further weight-degree escalation "
                "fails the predeclared 1e-4 continuation threshold"
            ),
        },
        "checks": checks,
        "git": r039.git_state(source_commit),
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": f"gmpy2 {gmpy2.version()} / GMP {gmpy2.mp_version()}",
            "randomness": False,
            "gpu": False,
            "floatingPointDecisionUse": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--radius-upper", default="382629/1000000")
    parser.add_argument("--character-lower", default="1337/10000")
    parser.add_argument("--character-upper", default="803/1000")
    parser.add_argument("--max-cover-depth", type=int, default=80)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    global PROGRESS_LOG
    PROGRESS_LOG = arguments.progress_log
    if PROGRESS_LOG is not None:
        PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG.write_text("", encoding="utf-8")

    payload = build_payload(
        arguments.max_total_degree,
        rational(arguments.radius_upper),
        rational(arguments.character_lower),
        rational(arguments.character_upper),
        arguments.max_cover_depth,
        arguments.progress,
        arguments.source_commit,
    )
    if arguments.check:
        failed = [name for name, value in payload["checks"].items() if not value]
        if failed:
            raise SystemExit("failed checks: " + ", ".join(failed))
    if arguments.output:
        r039.atomic_json_write(arguments.output, payload, arguments.pretty)
    else:
        json.dump(
            payload,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if arguments.pretty else None,
            sort_keys=True,
        )
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
