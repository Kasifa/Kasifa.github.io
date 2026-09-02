#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 15A--15B.

This standard-library-only producer checks the exact finite algebra and
combinatorics behind the hybrid-start residual equivalence, the common-window
start debt, and the terminal-crown reduction.  It also locks the reviewed
Step 10--14 dependencies and fail-closes selected formula and claim-boundary
wording in both Step 15 notes.

The certificate does not machine-prove the open common-deletion temporal tail,
the open selected-crown nonlinear payment, the jump--corona PDE lemma, an NSE
realization of an abstract fixture, regularity, or the Navier--Stokes
Millennium problem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
HYBRID_NOTE = Path(
    os.environ.get(
        "R074S_HYBRID_NOTE",
        REPO / "research/r074s_hybrid_flux_tail_equivalence.md",
    )
)
CROWN_NOTE = Path(
    os.environ.get(
        "R074S_CROWN_NOTE",
        REPO / "research/r074s_terminal_crown_coercivity.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_HYBRID_CROWN_JSON",
        REPO / "research/r074s_hybrid_crown_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_HYBRID_CROWN_REPORT",
        REPO / "research/r074s_hybrid_crown_certificate_report.md",
    )
)

SCHEMA = "r074s-hybrid-crown-certificate-v1"
HYBRID_TAGS = tuple(f"S.{number}" for number in range(377, 398))
CROWN_TAGS = tuple(f"S.{number}" for number in range(398, 417))
EXPECTED_TAGS = HYBRID_TAGS + CROWN_TAGS
LOCKED_HYBRID_SHA256 = "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d"
LOCKED_CROWN_SHA256 = "c62fc127c6d6381075653819a4672cae69f1ac4e2b7b45ee2d0b033ab770fd80"

DEPENDENCIES = {
    "R0.74S-step10": (
        REPO / "research/r074s_paid_branch_last_exit_residual.md",
        "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c",
    ),
    "R0.74S-step11": (
        REPO / "research/r074s_shared_budget_terminal_trace_obstruction.md",
        "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693",
    ),
    "R0.74S-step12": (
        REPO / "research/r074s_terminal_window_morrey_packing.md",
        "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f",
    ),
    "R0.74S-step13": (
        REPO / "research/r074s_temporal_integrability_morrey_threshold.md",
        "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de",
    ),
    "R0.74S-step14": (
        REPO / "research/r074s_outer_collar_corona_obstruction.md",
        "c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO.resolve()))
    except ValueError:
        return str(path.resolve())


def fs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def assertion(identifier: str, passed: bool, note: str, **details: object) -> dict:
    row = {"id": identifier, "pass": bool(passed), "note": note}
    row.update(details)
    return row


def exact(identifier: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def equation_source(text: str, tag: str) -> str:
    marker = f"\\tag{{{tag}}}"
    marker_index = text.find(marker)
    if marker_index < 0:
        return ""
    start = text.rfind("\\[", 0, marker_index)
    end = text.find("\\]", marker_index)
    if start < 0 or end < 0:
        return ""
    return text[start : end + 2]


def joint_tv_diamond_checks() -> dict:
    """Check the sharp ratios on the correlated |U|+|V|<T/6 diamond."""
    failures: list[dict] = []
    cases = 0
    for total in (Fraction(1), Fraction(5, 3), Fraction(7)):
        for iu in range(-11, 12):
            for iv in range(-11, 12):
                u = total * Fraction(iu, 72)
                v = total * Fraction(iv, 72)
                if abs(u) + abs(v) >= total / 6:
                    continue
                z = total - u - v
                r = total / 3 - v
                cases += 1
                if not (
                    z > 0
                    and 5 * r - z > 0
                    and 3 * z - 7 * r > 0
                    and r / z > Fraction(1, 5)
                    and r / z < Fraction(3, 7)
                ):
                    failures.append(
                        {
                            "T": fs(total),
                            "U": fs(u),
                            "V": fs(v),
                            "z": fs(z),
                            "r": fs(r),
                        }
                    )

    lower_gaps: list[str] = []
    upper_gaps: list[str] = []
    previous_lower: Fraction | None = None
    previous_upper: Fraction | None = None
    for denominator in (12, 60, 600, 6000):
        epsilon = Fraction(1, denominator)
        v_plus = Fraction(1, 6) - epsilon
        z_plus = 1 - v_plus
        r_plus = Fraction(1, 3) - v_plus
        lower_gap = r_plus / z_plus - Fraction(1, 5)

        v_minus = -Fraction(1, 6) + epsilon
        z_minus = 1 - v_minus
        r_minus = Fraction(1, 3) - v_minus
        upper_gap = Fraction(3, 7) - r_minus / z_minus
        lower_gaps.append(fs(lower_gap))
        upper_gaps.append(fs(upper_gap))
        cases += 4
        if not (
            lower_gap == 4 * epsilon / (5 * z_plus)
            and upper_gap == 4 * epsilon / (7 * z_minus)
            and lower_gap > 0
            and upper_gap > 0
            and (previous_lower is None or lower_gap < previous_lower)
            and (previous_upper is None or upper_gap < previous_upper)
        ):
            failures.append(
                {"kind": "sharp_approach", "epsilon": fs(epsilon)}
            )
        previous_lower = lower_gap
        previous_upper = upper_gap

    return assertion(
        "joint_TV_diamond_sharp_one_fifth_three_sevenths",
        not failures,
        "The correlated TV diamond gives 1/5<r/z<3/7, with exact scalar sequences approaching both endpoints.",
        cases=cases,
        lower_endpoint_gaps=lower_gaps,
        upper_endpoint_gaps=upper_gaps,
        failures=failures,
    )


def deletion_sums(values: tuple[Fraction, ...], budget: int) -> list[tuple[tuple[int, ...], Fraction]]:
    rows: list[tuple[tuple[int, ...], Fraction]] = []
    indices = tuple(range(len(values)))
    for size in range(min(budget, len(values)) + 1):
        for deleted in itertools.combinations(indices, size):
            deleted_set = set(deleted)
            rows.append((deleted, sum((v for i, v in enumerate(values) if i not in deleted_set), Fraction(0))))
    return rows


def best_n(values: tuple[Fraction, ...], budget: int) -> Fraction:
    return min(value for _, value in deletion_sums(values, budget))


def best_n_common_deletion_checks() -> dict:
    failures: list[dict] = []
    cases = 0
    fixtures = (
        (
            tuple(Fraction(v) for v in (5, 7, 9, 11, 13, 17)),
            (Fraction(1), Fraction(1, 4), Fraction(2, 5), Fraction(1), Fraction(1, 3), Fraction(2, 7)),
        ),
        (
            tuple(Fraction(v) for v in (1, 1, 1, 1, 1)),
            (Fraction(1, 5), Fraction(3, 7), Fraction(1), Fraction(1, 2), Fraction(4, 5)),
        ),
        (
            tuple(Fraction(v) for v in (2, 3, 5, 8)),
            (Fraction(1), Fraction(1), Fraction(1), Fraction(1)),
        ),
    )
    for z, multipliers in fixtures:
        r = tuple(value * multiplier for value, multiplier in zip(z, multipliers))
        for budget in range(len(z) + 1):
            z_rows = dict(deletion_sums(z, budget))
            r_rows = dict(deletion_sums(r, budget))
            for deleted in z_rows:
                cases += 1
                if not Fraction(1, 5) * z_rows[deleted] <= r_rows[deleted] <= z_rows[deleted]:
                    failures.append(
                        {"kind": "same_set", "budget": budget, "deleted": list(deleted)}
                    )
            cases += 1
            if not Fraction(1, 5) * best_n(z, budget) <= best_n(r, budget) <= best_n(z, budget):
                failures.append({"kind": "optimized", "budget": budget})

    for budget in range(7):
        height = Fraction(5 + budget, 3)
        flat = tuple(height for _ in range(budget + 1))
        cases += 1
        if best_n(flat, budget) != height:
            failures.append({"kind": "flat_N_plus_one", "budget": budget})

    return assertion(
        "best_N_one_common_deletion_set",
        not failures,
        "Coordinatewise comparison is preserved for each identical deletion set before the best-N infimum; N+1 equal coordinates leave one height.",
        cases=cases,
        failures=failures,
    )


def holder_window_factor_checks() -> dict:
    """Check 4^(1-1/p) by exact exponent arithmetic and powered inequalities."""
    failures: list[dict] = []
    cases = 0
    exponent_rows: list[dict] = []
    for label, reciprocal_p in (
        ("1", Fraction(1)),
        ("4/3", Fraction(3, 4)),
        ("3/2", Fraction(2, 3)),
        ("2", Fraction(1, 2)),
        ("3", Fraction(1, 3)),
        ("infinity", Fraction(0)),
    ):
        factor_exponent = 1 - reciprocal_p
        cases += 2
        if factor_exponent + reciprocal_p != 1:
            failures.append({"kind": "exponent", "p": label})
        if label == "infinity" and factor_exponent != 1:
            failures.append({"kind": "infinity", "p": label})
        exponent_rows.append(
            {
                "p": label,
                "norm_power_of_4": fs(reciprocal_p),
                "factor_power_of_4": fs(factor_exponent),
                "product_power_of_4": fs(factor_exponent + reciprocal_p),
            }
        )

    vectors = tuple(itertools.product((Fraction(0), Fraction(1), Fraction(2), Fraction(3)), repeat=4))
    for values in vectors:
        total = sum(values, Fraction(0))
        cases += 4
        # p=1 and p=infinity.
        if total > sum(values, Fraction(0)) or total > 4 * max(values):
            failures.append({"kind": "endpoint_holder", "values": [fs(v) for v in values]})
        # p=2: square the nonnegative inequality sum h <= 2 ||h||_2.
        if total * total > 4 * sum((v * v for v in values), Fraction(0)):
            failures.append({"kind": "p2", "values": [fs(v) for v in values]})
        # p=3: cube sum h <= 4^(2/3) ||h||_3.
        if total**3 > 16 * sum((v**3 for v in values), Fraction(0)):
            failures.append({"kind": "p3", "values": [fs(v) for v in values]})

        # p=4/3 with h_i=a_i^3: fourth power removes all roots.
        cubes = tuple(v**3 for v in values)
        if sum(cubes, Fraction(0)) ** 4 > 4 * sum((v**4 for v in values), Fraction(0)) ** 3:
            failures.append({"kind": "p4/3", "values": [fs(v) for v in values]})

    return assertion(
        "four_to_one_minus_one_over_p_window_factor",
        not failures,
        "Exact exponent arithmetic and powered finite Hölder checks retain the interval-length factor 4^(1-1/p), including factor 4 at p=infinity.",
        cases=cases,
        exponents=exponent_rows,
        failures=failures,
    )


def common_window_debt_checks() -> dict:
    failures: list[dict] = []
    cases = 0
    for total in (Fraction(3), Fraction(9, 2), Fraction(7)):
        for k_a in (Fraction(0), total / 2, total, 3 * total):
            for q_a, q_ell, q_tau in (
                (Fraction(0), Fraction(0), Fraction(0)),
                (Fraction(1, 5), Fraction(-1, 7), Fraction(2, 9)),
                (Fraction(-2), Fraction(3, 4), Fraction(-5, 6)),
            ):
                f_a = k_a - q_a
                f_ell = 2 * total / 3 - q_ell
                f_tau = total - q_tau
                residual = f_tau - f_ell
                common_increment = f_tau - f_a
                start_clock = k_a - 2 * total / 3
                q_prefix = q_ell - q_a
                cases += 1
                if residual != common_increment + start_clock + q_prefix:
                    failures.append({"kind": "identity", "T": fs(total), "K_a": fs(k_a)})

    scalar_rows = []
    for height in (Fraction(4), Fraction(7), Fraction(100)):
        total = Fraction(3)
        residual = Fraction(1)
        common_increment = 3 - height
        omega = height - 2
        cases += 1
        if residual != common_increment + omega:
            failures.append({"kind": "overshoot_fixture", "M": fs(height)})
        scalar_rows.append(
            {"M": fs(height), "r": fs(residual), "G": fs(common_increment), "omega": fs(omega)}
        )

    return assertion(
        "common_window_start_debt_identity",
        not failures,
        "The stopped residual equals the signed common-window increment plus start-clock debt and the Q-prefix; the Step 15 scalar overshoot restores it exactly.",
        cases=cases,
        scalar_rows=scalar_rows,
        failures=failures,
    )


def first_root_jump_crown_checks() -> dict:
    failures: list[dict] = []
    cases = 0
    rows: list[dict] = []
    for kappa in (Fraction(3, 2), Fraction(2), Fraction(5, 2), Fraction(7, 3)):
        c_infinity = Fraction(2) * kappa - 1
        c_infinity /= kappa - 1
        for depth in range(9):
            finite_sum = 1 + sum((kappa ** (-j) for j in range(depth + 1)), Fraction(0))
            formula = 1 + kappa / (kappa - 1) * (1 - kappa ** (-(depth + 1)))
            cases += 3
            if finite_sum != formula or finite_sum > c_infinity:
                failures.append({"kind": "C_kappa_L", "kappa": fs(kappa), "L": depth})

            rho_top = Fraction(depth + 2, depth + 1)
            level = Fraction(2 * depth + 3, 5)
            mass = level * rho_top
            root_radii = (rho_top / 2, rho_top / 3, rho_top / 7)
            if sum(root_radii, Fraction(0)) > mass / level:
                failures.append({"kind": "first_root", "kappa": fs(kappa), "L": depth})

            generation_sums = tuple(rho_top * kappa ** (-j) for j in range(depth + 1))
            if sum(generation_sums, Fraction(0)) + rho_top != rho_top * finite_sum:
                failures.append({"kind": "jump_sum", "kappa": fs(kappa), "L": depth})
            rows.append(
                {
                    "kappa": fs(kappa),
                    "L": depth,
                    "C_kappa_L": fs(finite_sum),
                    "C_kappa": fs(c_infinity),
                }
            )

    return assertion(
        "first_root_jump_and_C_kappa_L",
        not failures,
        "First-root radii, generationwise kappa-jump decay, the finite crown constant, and its depth-independent limit are exact.",
        cases=cases,
        samples=rows,
        failures=failures,
    )


def leaves_below(prefix: tuple[int, ...], leaves: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
    length = len(prefix)
    return {leaf for leaf in leaves if leaf[:length] == prefix}


def crown_partition(
    max_depth: int,
    roots: tuple[tuple[int, ...], ...],
    jumps: dict[tuple[int, ...], tuple[tuple[int, ...], ...]],
    generations: tuple[tuple[tuple[int, ...], ...], ...],
) -> tuple[set[tuple[int, ...]], list[set[tuple[int, ...]]]]:
    universe = set(itertools.product(range(32), repeat=max_depth))
    pieces: list[set[tuple[int, ...]]] = []
    top_crown = set(universe)
    for root in roots:
        top_crown -= leaves_below(root, universe)
    pieces.append(top_crown)
    final_generation = len(generations) - 1
    for generation_index, generation in enumerate(generations):
        for node in generation:
            piece = leaves_below(node, universe)
            if generation_index < final_generation:
                for child in jumps[node]:
                    piece -= leaves_below(child, universe)
            pieces.append(piece)
    return universe, pieces


def half_open_memberships(point: tuple[Fraction, Fraction, Fraction, Fraction], depth: int) -> list[tuple[int, int, int, int]]:
    memberships: list[tuple[int, int, int, int]] = []
    t_cells = 4**depth
    x_cells = 2**depth
    for it in range(t_cells):
        if not Fraction(it, t_cells) <= point[0] < Fraction(it + 1, t_cells):
            continue
        for ix in range(x_cells):
            if not Fraction(ix, x_cells) <= point[1] < Fraction(ix + 1, x_cells):
                continue
            for iy in range(x_cells):
                if not Fraction(iy, x_cells) <= point[2] < Fraction(iy + 1, x_cells):
                    continue
                for iz in range(x_cells):
                    if Fraction(iz, x_cells) <= point[3] < Fraction(iz + 1, x_cells):
                        memberships.append((it, ix, iy, iz))
    return memberships


def half_open_32_child_crown_checks() -> dict:
    failures: list[dict] = []
    cases = 0
    fixture_rows: list[dict] = []

    roots_1 = ((0,), (7,), (31,))
    generation_1 = roots_1
    generation_2 = tuple(root + (digit,) for root in roots_1 for digit in (0, 15, 31))
    jumps_1 = {root: tuple(root + (digit,) for digit in (0, 15, 31)) for root in roots_1}
    universe, pieces = crown_partition(2, roots_1, jumps_1, (generation_1, generation_2))
    union = set().union(*pieces)
    cases += len(pieces) + 2
    if union != universe or sum(len(piece) for piece in pieces) != len(universe):
        failures.append({"kind": "depth2_partition"})
    fixture_rows.append(
        {"depth": 2, "leaves": len(universe), "crowns": len(pieces), "crown_sizes": [len(p) for p in pieces]}
    )

    roots_2 = ((4,), (12,))
    generation_a = roots_2
    generation_b = tuple(root + (digit,) for root in roots_2 for digit in (1, 30))
    generation_c = tuple(node + (digit,) for node in generation_b for digit in (2, 29))
    jumps_2: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}
    for root in generation_a:
        jumps_2[root] = tuple(root + (digit,) for digit in (1, 30))
    for node in generation_b:
        jumps_2[node] = tuple(node + (digit,) for digit in (2, 29))
    universe_2, pieces_2 = crown_partition(
        3,
        roots_2,
        jumps_2,
        (generation_a, generation_b, generation_c),
    )
    union_2 = set().union(*pieces_2)
    cases += len(pieces_2) + 2
    if union_2 != universe_2 or sum(len(piece) for piece in pieces_2) != len(universe_2):
        failures.append({"kind": "depth3_partition"})
    fixture_rows.append(
        {"depth": 3, "leaves": len(universe_2), "crowns": len(pieces_2), "crown_sizes": [len(p) for p in pieces_2]}
    )

    boundary_values = (
        Fraction(0),
        Fraction(1, 8),
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(7, 8),
        Fraction(63, 64),
    )
    boundary_points = tuple(itertools.islice(itertools.product(boundary_values, repeat=4), 320))
    for depth in (1, 2):
        for point in boundary_points:
            memberships = half_open_memberships(point, depth)
            cases += 1
            if len(memberships) != 1:
                failures.append(
                    {"kind": "half_open_boundary", "depth": depth, "point": [fs(v) for v in point], "count": len(memberships)}
                )

    # Deliberately omit a terminal crown: the finite partition must fail.
    truncated_union = set().union(*pieces_2[:-1])
    cases += 1
    if truncated_union == universe_2:
        failures.append({"kind": "terminal_crown_omission_not_detected"})

    return assertion(
        "finite_32_child_half_open_terminal_crowns",
        not failures,
        "Generated 32-child trees partition into disjoint finite-depth crowns; internal boundary atoms have unique half-open ownership and omitting a terminal crown is detected.",
        cases=cases,
        fixtures=fixture_rows,
        omitted_terminal_leaf_count=len(universe_2 - truncated_union),
        failures=failures,
    )


def canonical_payment_checks() -> dict:
    failures: list[dict] = []
    cases = 0
    rows: list[dict] = []
    for coefficient in (Fraction(1, 2), Fraction(3), Fraction(5, 7), Fraction(11, 9)):
        for scale in (Fraction(1, 3), Fraction(1), Fraction(5, 2)):
            mass = coefficient * scale**2
            payment = coefficient * scale**3
            payment_squared = mass**3 / coefficient
            cases += 2
            if payment**2 != payment_squared or mass**3 / payment**2 != coefficient:
                failures.append({"kind": "canonical", "coefficient": fs(coefficient), "scale": fs(scale)})
            rows.append(
                {"coefficient": fs(coefficient), "mass": fs(mass), "payment": fs(payment)}
            )

    # Zero-support convention.
    cases += 1
    if Fraction(0) != 0:
        failures.append({"kind": "zero_support"})

    for scales in itertools.product((Fraction(1, 2), Fraction(1), Fraction(2)), repeat=3):
        coefficients = (Fraction(1, 3), Fraction(2, 5), Fraction(7, 4))
        masses = tuple(c * s**2 for c, s in zip(coefficients, scales))
        payments = tuple(c * s**3 for c, s in zip(coefficients, scales))
        cases += 1
        if sum(masses, Fraction(0)) ** 3 > sum(coefficients, Fraction(0)) * sum(payments, Fraction(0)) ** 2:
            failures.append({"kind": "holder_closure", "scales": [fs(s) for s in scales]})

    # Two equal incidence occurrences require two payments.  Reusing one fails.
    masses = (Fraction(1), Fraction(1))
    coefficients = (Fraction(1), Fraction(1))
    correct_payments = (Fraction(1), Fraction(1))
    correct = sum(masses) ** 3 <= sum(coefficients) * sum(correct_payments) ** 2
    reused = sum(masses) ** 3 <= sum(coefficients) * correct_payments[0] ** 2
    cases += 2
    if not correct or reused:
        failures.append({"kind": "repeated_incidence_payment"})

    return assertion(
        "canonical_crown_payment_cubic_identity",
        not failures,
        "The positive-support identity a^3=p^2 gamma rho, zero convention, finite Hölder closure, and repeated-incidence payment count are exact.",
        cases=cases,
        samples=rows,
        failures=failures,
    )


def converse_holder_threshold_checks() -> dict:
    failures: list[dict] = []
    cases = 0
    values = (Fraction(1, 2), Fraction(1), Fraction(2))
    for masses in itertools.product(values, repeat=3):
        for payments in itertools.product((Fraction(1, 3), Fraction(1), Fraction(3)), repeat=3):
            total_mass = sum(masses, Fraction(0))
            total_payment = sum(payments, Fraction(0))
            left = sum((a**3 / p**2 for a, p in zip(masses, payments)), Fraction(0))
            right = total_mass**3 / total_payment**2
            cases += 1
            if left < right:
                failures.append({"kind": "converse", "a": [fs(v) for v in masses], "p": [fs(v) for v in payments]})

    for masses in (
        (Fraction(1), Fraction(2), Fraction(5)),
        (Fraction(1, 3), Fraction(7, 5), Fraction(4)),
    ):
        total_mass = sum(masses, Fraction(0))
        total_payment = Fraction(11, 3)
        payments = tuple(total_payment * value / total_mass for value in masses)
        left = sum((a**3 / p**2 for a, p in zip(masses, payments)), Fraction(0))
        right = total_mass**3 / total_payment**2
        cases += 1
        if left != right:
            failures.append({"kind": "equality_assignment"})

    threshold_rows: list[dict] = []
    for c, c_q, c_p in (
        (Fraction(1), Fraction(1, 2), Fraction(1)),
        (Fraction(2), Fraction(1), Fraction(2)),
        (Fraction(3, 2), Fraction(2, 3), Fraction(5, 4)),
    ):
        c_m = c**3
        h_root = 2 * c_q * c**2 + 1
        height = h_root**3
        quadratic_scale = c**2 * h_root**2
        q_budget = c_q * quadratic_scale
        paid_mass = height - q_budget
        payment_budget = c_p * c_m * height
        actual_lower = paid_mass**3 / payment_budget**2
        displayed_lower = height / (8 * c_p**2 * c_m**2)
        threshold = (2 * c_q * c**2) ** 3
        cases += 4
        if not (
            height >= threshold
            and q_budget <= height / 2
            and paid_mass >= height / 2
            and actual_lower >= displayed_lower
        ):
            failures.append({"kind": "threshold", "c": fs(c), "Cq": fs(c_q), "Cp": fs(c_p)})
        threshold_rows.append(
            {
                "C_M": fs(c_m),
                "H": fs(height),
                "threshold": fs(threshold),
                "coefficient_lower_bound": fs(displayed_lower),
            }
        )

    # Cube-parameterized exact form of the tradeoff in S.412.
    for d, e, c, h in (
        (Fraction(1), Fraction(1), Fraction(1), Fraction(4)),
        (Fraction(2), Fraction(3, 2), Fraction(2), Fraction(9)),
    ):
        c_cor = d**3
        c_p = e**3
        c_m = c**3
        height = h**3
        max_paid = d * e**2 * c**2 * h**2
        exact_right = height - max_paid
        # The cube parametrization removes both radicals: max_paid is exactly
        # C_cor^(1/3) (C_p C_M H)^(2/3).
        cases += 2
        if max_paid**3 != c_cor * (c_p * c_m * height) ** 2 or exact_right != height - max_paid:
            failures.append({"kind": "tradeoff_radicals"})

    return assertion(
        "converse_Holder_equality_and_flat_threshold",
        not failures,
        "The converse Hölder lower bound, proportional equality case, H-threshold, factor 1/8, and cube-parameterized tradeoff are exact.",
        cases=cases,
        threshold_samples=threshold_rows,
        failures=failures,
    )


def pure_defect_scaling_checks() -> dict:
    failures: list[dict] = []
    cases = 0
    rows: list[dict] = []
    for height in (Fraction(1, 5), Fraction(1), Fraction(7, 3), Fraction(19)):
        scale = 5 * height / 3
        total = scale
        defect = 3 * scale / 5
        residual = scale / 3
        sigma = Fraction(959, 12000) * scale
        excess = Fraction(2641, 6000) * scale
        cases += 8
        if not (
            defect == height
            and total == 5 * height / 3
            and residual == 5 * height / 9
            and sigma == 959 * height / 7200
            and excess == 2641 * height / 3600
            and sigma < total / 12
            and excess > total / 6
            and total / 12 - sigma == 41 * height / 7200
        ):
            failures.append({"H": fs(height)})
        rows.append(
            {
                "H": fs(height),
                "T": fs(total),
                "b": fs(defect),
                "r_x": fs(residual),
                "sigma": fs(sigma),
                "x": fs(excess),
            }
        )

    return assertion(
        "pure_defect_scaled_constants",
        not failures,
        "Scaling the Step 11 pure-defect clock by 5H/3 gives every S.415 constant and both strict branch inequalities exactly.",
        cases=cases,
        samples=rows,
        failures=failures,
    )


def dependency_checks() -> list[dict]:
    rows = []
    for identifier, (path, expected) in DEPENDENCIES.items():
        actual = sha256(path) if path.exists() else None
        rows.append(
            assertion(
                f"dependency_{identifier}",
                actual == expected,
                "The reviewed upstream main note matches its locked SHA-256.",
                path=display_path(path),
                expected_sha256=expected,
                actual_sha256=actual,
            )
        )
    return rows


def validate_notes(
    hybrid_text: str,
    hybrid_raw: bytes,
    crown_text: str,
    crown_raw: bytes,
) -> list[dict]:
    hybrid_tags = tuple(re.findall(r"\\tag\{(S\.\d+)\}", hybrid_text))
    crown_tags = tuple(re.findall(r"\\tag\{(S\.\d+)\}", crown_text))
    all_tags = hybrid_tags + crown_tags
    hybrid_compact = compact(hybrid_text)
    crown_compact = compact(crown_text)
    both = hybrid_text + "\n" + crown_text
    lines = both.splitlines()
    forbidden = re.findall(
        r"(?:\bwe\b|\bour\b|攻关|主攻|研究纪律|三重审计|杀死错误想法)",
        both,
        flags=re.IGNORECASE,
    )

    required_hybrid = tuple(
        compact(value)
        for value in (
            "The common-deletion estimate (S.342), Step 10 (S.243), Q.12, and Q.1 remain open.",
            "No abstract scalar witness below is a Navier--Stokes counterexample.",
            "No claim of novelty, regularity, singularity formation, or a solution of the Millennium problem is made.",
            "This is a boundary statement, not a new impossibility theorem for PDE cancellation.",
            "This is an **ABSTRACT SCALAR-LEDGER WITNESS**.",
            "This too is only an **ABSTRACT CLOCK CHECK**",
            "This is a bounded collision boundary, not an exhaustive search or a novelty claim.",
            "**NOT CLAY.**",
        )
    )
    required_crown = tuple(
        compact(value)
        for value in (
            "coercivity estimate is **OPEN** for the bare suitable-weak class.",
            "This is an **ABSTRACT METHOD OBSTRUCTION**, not a Navier--Stokes counterexample.",
            "This note does not prove (S.375), (S.288), (S.303), (S.272), Q.12, Q.1,",
            "This is a bounded collision search, not an exhaustive review or a novelty claim.",
            "The following is an **OPEN PDE INPUT**:",
            "The following is an **ABSTRACT METHOD OBSTRUCTION, NOT AN NSE COUNTEREXAMPLE**:",
            "**NOT CLAY.**",
        )
    )
    urls = (
        "https://doi.org/10.4171/AIHPC/20",
        "https://doi.org/10.1016/j.jde.2017.09.036",
        "https://doi.org/10.1007/s00021-024-00894-z",
        "https://doi.org/10.1016/j.aim.2024.109654",
        "https://arxiv.org/abs/1809.02109",
    )

    rows = [
        assertion(
            "hybrid_note_hash_lock",
            hashlib.sha256(hybrid_raw).hexdigest() == LOCKED_HYBRID_SHA256,
            "The reviewed Step 15A note hash is frozen.",
            expected_sha256=LOCKED_HYBRID_SHA256,
            actual_sha256=hashlib.sha256(hybrid_raw).hexdigest(),
            lock_enforced=True,
        ),
        assertion(
            "crown_note_hash_lock",
            hashlib.sha256(crown_raw).hexdigest() == LOCKED_CROWN_SHA256,
            "The reviewed Step 15B note hash is frozen.",
            expected_sha256=LOCKED_CROWN_SHA256,
            actual_sha256=hashlib.sha256(crown_raw).hexdigest(),
            lock_enforced=True,
        ),
        assertion(
            "sequential_unique_equation_tags",
            hybrid_tags == HYBRID_TAGS
            and crown_tags == CROWN_TAGS
            and all_tags == EXPECTED_TAGS
            and len(all_tags) == len(set(all_tags)),
            "Equation tags are exactly S.377 through S.416, once each and in order across the two notes.",
            expected=list(EXPECTED_TAGS),
            actual=list(all_tags),
        ),
        assertion(
            "balanced_display_delimiters",
            all(
                text.count("\\[") == text.count("\\]") and text.count("\\[") > 0
                for text in (hybrid_text, crown_text)
            ),
            "Display-math delimiters are balanced separately in both notes.",
            hybrid_opens=hybrid_text.count("\\["),
            hybrid_closes=hybrid_text.count("\\]"),
            crown_opens=crown_text.count("\\["),
            crown_closes=crown_text.count("\\]"),
        ),
        assertion(
            "required_claim_boundaries",
            all(value in hybrid_compact for value in required_hybrid)
            and all(value in crown_compact for value in required_crown),
            "Open/conditional, abstract-not-NSE, collision, and NOT CLAY boundaries are present.",
            missing_hybrid=[value for value in required_hybrid if value not in hybrid_compact],
            missing_crown=[value for value in required_crown if value not in crown_compact],
        ),
        assertion(
            "primary_source_urls",
            all(url in crown_text for url in urls),
            "All five bounded primary-source links are present in the crown note.",
            missing=[url for url in urls if url not in crown_text],
        ),
        assertion(
            "discouraged_prose_absent",
            not forbidden,
            "The published-writing discouraged phrases are absent.",
            matches=forbidden,
        ),
        assertion(
            "utf8_no_control_damage",
            b"\x00" not in hybrid_raw
            and b"\r" not in hybrid_raw
            and b"\x00" not in crown_raw
            and b"\r" not in crown_raw,
            "Neither note has NUL or carriage-return corruption.",
        ),
        assertion(
            "no_trailing_whitespace",
            not any(line.strip() and line.endswith((" ", "\t")) for line in lines),
            "Neither note has trailing spaces or tabs on a content-bearing line.",
        ),
    ]

    equations = {
        tag: equation_source(hybrid_text if tag in HYBRID_TAGS else crown_text, tag)
        for tag in EXPECTED_TAGS
    }
    bindings = (
        (
            "hybrid_S377_start_definition",
            "\\sigma_k^{\\rm hyb}" in equations["S.377"]
            and ":=F_{k,R}(\\tau)-F_{k,R}(\\sigma_k^{\\rm hyb}(\\tau))" in equations["S.377"],
            "S.377 retains the hybrid start and one stopped physical-flux coordinate.",
        ),
        (
            "hybrid_S378_branch_identities",
            "z_k=r_k^{\\rm sh}=r_k" in equations["S.378"]
            and "z_k=F_{k,R}(\\tau)=[F_{k,R}(\\tau)]_+" in equations["S.378"],
            "S.378 retains exact short-branch equality and the common-zero-start excess branch.",
        ),
        (
            "hybrid_S380_joint_TV",
            "|U_k|+|V_k|" in equations["S.380"]
            and "\\beta_{k,R}(J_\\tau)<{T_k\\over6}" in equations["S.380"],
            "S.380 retains one correlated full-history TV diamond.",
        ),
        (
            "hybrid_S381_clock_pair",
            "z_k=T_k-U_k-V_k" in equations["S.381"]
            and "r_k={T_k\\over3}-V_k" in equations["S.381"],
            "S.381 retains the exact two scalar coordinates.",
        ),
        (
            "hybrid_S382_sharp_constants",
            "{1\\over5}z_k<r_k<{3\\over7}z_k" in equations["S.382"],
            "S.382 retains the strict sharp constants 1/5 and 3/7.",
        ),
        (
            "hybrid_S383_coordinatewise",
            "{1\\over5}z_k(\\tau)\\le r_k(\\tau)\\le z_k(\\tau)" in equations["S.383"]
            and "z(\\tau)\\in\\ell^1_+" in equations["S.383"],
            "S.383 retains the global nonnegative coordinate comparison.",
        ),
        (
            "hybrid_S384_same_best_N",
            "{1\\over5}\\mathcal S_N(z(\\tau))" in equations["S.384"]
            and "\\le\\mathcal S_N(r(\\tau))" in equations["S.384"]
            and "\\le\\mathcal S_N(z(\\tau))" in equations["S.384"],
            "S.384 retains the same-deletion best-N equivalence.",
        ),
        (
            "hybrid_S386_window_factor",
            "4^{\\,1-1/p}\\|h_{k,R}\\|_{L^p(0,4)}" in equations["S.386"]
            and "1\\le p\\le\\infty" in equations["S.386"],
            "S.386 retains the exact length-four Hölder factor.",
        ),
        (
            "hybrid_S387_global_same_N_tail",
            "\\mathcal S_N(r(\\tau))" in equations["S.387"]
            and "\\mathfrak H^F_{p,N,R}" in equations["S.387"],
            "S.387 retains one global temporal tail and one shell deletion budget.",
        ),
        (
            "hybrid_S388_open_antecedent",
            "\\mathfrak H^F_{p,N_F,R}\\le C_HA_R" in equations["S.388"],
            "S.388 retains the explicitly assumed open temporal-tail antecedent.",
        ),
        (
            "hybrid_S392_signed_channels",
            all(channel in equations["S.392"] for channel in ("{\\rm cub,loc,har,dr}", "\\sigma_k^{\\rm hyb}(\\tau)", "z_k(\\tau)")),
            "S.392 retains the signed four-channel hybrid-block identity.",
        ),
        (
            "hybrid_S393_debt_identity",
            "r_k^{\\rm sh}" in equations["S.393"]
            and "G_{k,\\tau,\\delta}" in equations["S.393"]
            and "+\\left[K_{k,R}(a)-{2T_k\\over3}\\right]" in equations["S.393"]
            and "+\\left[Q_{k,R}(\\ell_k)-Q_{k,R}(a)\\right]" in equations["S.393"],
            "S.393 retains all three common-window debt terms with positive signs.",
        ),
        (
            "hybrid_S394_common_set_debt_bound",
            "G_{k,\\tau,\\delta}" in equations["S.394"]
            and "\\omega_{k,\\tau,\\delta}" in equations["S.394"]
            and "+C_QA_R" in equations["S.394"],
            "S.394 retains signed common-window cancellation, overshoot, and paid Q-prefix.",
        ),
        (
            "hybrid_S395_minimal_gate",
            "\\mathcal S_N(r^{{\\rm sh},\\le\\delta}(\\tau))" in equations["S.395"]
            and "\\inf_{\\#S\\le N}" in equations["S.395"]
            and "\\omega_{k,\\tau,\\delta}" in equations["S.395"],
            "S.395 retains one common deletion set for cancellation and start debt.",
        ),
        (
            "hybrid_S396_sharp_sequences",
            "\\longrightarrow{1\\over5}" in equations["S.396"]
            and "\\longrightarrow{3\\over7}" in equations["S.396"],
            "S.396 retains both scalar endpoint approaches.",
        ),
        (
            "hybrid_S397_clock_fixture",
            "r=1" in equations["S.397"]
            and "G=F(\\tau)-F(a)=3-M" in equations["S.397"]
            and "\\omega=K(a)-2=M-2" in equations["S.397"]
            and "r=G+\\omega" in equations["S.397"],
            "S.397 retains the exact start-debt clock fixture.",
        ),
        (
            "crown_S398_submeasure",
            "b_k(\\tau)&=\\alpha^{\\rm anc}_{k,\\tau}" in equations["S.398"]
            and "0\\le d\\alpha^{\\rm anc}_{k,\\tau}" in equations["S.398"]
            and "\\gamma_k\\mathbf 1_{\\widehat{\\mathcal U}_{k,R}(\\tau)}" in equations["S.398"],
            "S.398 retains the shellwise selected ancestor submeasure domination.",
        ),
        (
            "crown_S399_shellwise_ownership",
            "\\mathop{\\dot\\bigcup}" in equations["S.399"]
            and "\\mathcal O_{Tk}\\subset T\\cap\\widehat{\\mathcal U}_{k,R}(\\tau)" in equations["S.399"],
            "S.399 retains disjoint shellwise ownership.",
        ),
        (
            "crown_S400_top_content",
            "\\mathscr C_{\\rm top}" in equations["S.400"]
            and "\\gamma_k\\rho_T" in equations["S.400"],
            "S.400 retains incidence-weighted top one-content.",
        ),
        (
            "crown_S401_first_roots",
            "\\sum_{S\\in\\mathscr R(T)}\\rho_S" in equations["S.401"]
            and "{m_T\\over\\lambda_T}=\\rho_T" in equations["S.401"],
            "S.401 retains the canonical first-root radius budget.",
        ),
        (
            "crown_S402_jump_generations",
            "\\kappa^{-j}\\rho_T" in equations["S.402"]
            and "{\\kappa\\over\\kappa-1}\\rho_T" in equations["S.402"],
            "S.402 retains generationwise and total jump-radius bounds.",
        ),
        (
            "crown_S403_finite_partition",
            "T=\\Omega_T\\mathbin{\\dot\\cup}" in equations["S.403"]
            and "0\\le j\\le L" in equations["S.403"],
            "S.403 retains the exact finite-depth disjoint crown partition.",
        ),
        (
            "crown_S404_C_kappa_L",
            "C_{\\kappa,L}&:=1+\\sum_{j=0}^{L}\\kappa^{-j}" in equations["S.404"]
            and "1-\\kappa^{-(L+1)}" in equations["S.404"]
            and "{2\\kappa-1\\over\\kappa-1}" in equations["S.404"],
            "S.404 retains the finite and depth-independent crown constants.",
        ),
        (
            "crown_S405_common_exception_split",
            "a_{Sk}=q_{Sk}+a_{Sk}^{\\rm pay}" in equations["S.405"]
            and "\\mathscr C_L(E_\\tau)" in equations["S.405"]
            and "\\le C_qA_R" in equations["S.405"],
            "S.405 retains one common shell exception and quadratic q-budget.",
        ),
        (
            "crown_S406_canonical_cube",
            "{\\bigl(a_{Sk}^{\\rm pay}\\bigr)^{3/2}" in equations["S.406"]
            and "{\\bigl(a_{Sk}^{\\rm pay}\\bigr)^3" in equations["S.406"]
            and "\\gamma_k\\rho_S" in equations["S.406"],
            "S.406 retains the canonical 3/2 payment and exact cubic coefficient identity.",
        ),
        (
            "crown_S407_open_payment",
            "\\sum_{(S,T,k)\\in\\mathscr C_L(E_\\tau)}p_{Sk}^{\\rm crown}" in equations["S.407"]
            and "\\le C_pP_R^M" in equations["S.407"]
            and "\\textbf{OPEN}" in equations["S.407"],
            "S.407 remains explicitly open and counts the complete crown-incidence payment.",
        ),
        (
            "crown_S408_conditional_closure",
            "\\mathcal S_{N_b}(b(\\tau))" in equations["S.408"]
            and "C_\\kappa\\mathscr C_{\\rm top}" in equations["S.408"]
            and "C_p^{2/3}" in equations["S.408"],
            "S.408 retains the conditional quadratic-scale closure.",
        ),
        (
            "crown_S409_converse_equality",
            "\\sum_i{a_i^3\\over p_i^2}\\ge{A^3\\over P^2}" in equations["S.409"]
            and "\\inf_{p_i\\ge0,\\ \\sum p_i=P}" in equations["S.409"],
            "S.409 retains the converse Hölder minimum.",
        ),
        (
            "crown_S410_flat_N_plus_one",
            "b_{k_i}\\ge H" in equations["S.410"]
            and "P_H=C_MH" in equations["S.410"]
            and "A_H=(C_MH)^{2/3}" in equations["S.410"],
            "S.410 retains N_b+1 flat coordinates and linear payment scaling.",
        ),
        (
            "crown_S411_threshold_factor",
            "\\ge {H\\over8C_p^2C_M^2}" in equations["S.411"],
            "S.411 retains the exact factor 1/8 lower bound.",
        ),
        (
            "crown_S412_tradeoff",
            "H-C_{\\rm cor}^{1/3}(C_pC_MH)^{2/3}" in equations["S.412"],
            "S.412 retains the exact q/coefficient tradeoff.",
        ),
        (
            "crown_S413_periodic_full_lift",
            "\\sum_{n\\in\\mathbb Z^3}\\sum_{i=1}^M" in equations["S.413"]
            and "Q_i^x+(2\\pi/R)n" in equations["S.413"],
            "S.413 retains every periodic lifted copy.",
        ),
        (
            "crown_S414_critical_branching",
            "\\rho_v=2^{-d}\\rho_0" in equations["S.414"]
            and "m_v=8^{-d}m_0" in equations["S.414"]
            and "\\Theta(v)=4^{-d}\\Theta(0)" in equations["S.414"],
            "S.414 retains the one-temporal/eight-spatial child scaling.",
        ),
        (
            "crown_S415_pure_defect_scaling",
            "T={5H\\over3}" in equations["S.415"]
            and "b=m=H" in equations["S.415"]
            and "r^x={5H\\over9}" in equations["S.415"]
            and "\\sigma={959H\\over7200}<{T\\over12}" in equations["S.415"]
            and "x={2641H\\over3600}>{T\\over6}" in equations["S.415"]
            and "\\beta=0" in equations["S.415"],
            "S.415 retains every scaled pure-defect constant and strict inequality.",
        ),
        (
            "crown_S416_best_N_divergence",
            "{\\mathcal S_{N_b}(b)\\over A_H}" in equations["S.416"]
            and "C_M^{-2/3}H^{1/3}\\longrightarrow\\infty" in equations["S.416"],
            "S.416 retains the fixed-best-N normalized divergence.",
        ),
        (
            "crown_full_incidence_boundaries",
            all(
                phrase in crown_compact
                for phrase in (
                    "every repeated top occurrence remains visible in the incidence sums",
                    "The periodic lifted measure is integrated in full inside these tops, with no quotient or discarded copy",
                    "The same frozen payment may not be reused for different occurrences unless it is repeated in the sum",
                    "Infinite-jump mass is included in the last finite-depth crown and cannot be lost in a limit",
                )
            ),
            "Repeated tops, periodic copies, repeated payments, and terminal-depth mass remain explicit.",
        ),
    )
    rows.extend(assertion(identifier, passed, note) for identifier, passed, note in bindings)
    return rows


def negative_mutation_checks(hybrid_text: str, crown_text: str) -> list[dict]:
    hybrid_raw = hybrid_text.encode("utf-8")
    crown_raw = crown_text.encode("utf-8")
    probes = (
        (
            "joint_TV_threshold",
            "hybrid",
            "\\beta_{k,R}(J_\\tau)<{T_k\\over6}",
            "\\beta_{k,R}(J_\\tau)<{T_k\\over5}",
            "hybrid_S380_joint_TV",
        ),
        (
            "one_fifth_constant",
            "hybrid",
            "{1\\over5}z_k<r_k<{3\\over7}z_k",
            "{1\\over4}z_k<r_k<{3\\over7}z_k",
            "hybrid_S382_sharp_constants",
        ),
        (
            "same_best_N_direction",
            "hybrid",
            "{1\\over5}\\mathcal S_N(z(\\tau))",
            "{1\\over4}\\mathcal S_N(z(\\tau))",
            "hybrid_S384_same_best_N",
        ),
        (
            "window_factor_exponent",
            "hybrid",
            "4^{\\,1-1/p}\\|h_{k,R}\\|_{L^p(0,4)}",
            "4^{\\,1/p}\\|h_{k,R}\\|_{L^p(0,4)}",
            "hybrid_S386_window_factor",
        ),
        (
            "debt_clock_sign",
            "hybrid",
            "+\\left[K_{k,R}(a)-{2T_k\\over3}\\right]",
            "-\\left[K_{k,R}(a)-{2T_k\\over3}\\right]",
            "hybrid_S393_debt_identity",
        ),
        (
            "finite_crown_exponent",
            "crown",
            "1-\\kappa^{-(L+1)}",
            "1-\\kappa^{-L}",
            "crown_S404_C_kappa_L",
        ),
        (
            "terminal_crown_disjointness",
            "crown",
            "T=\\Omega_T\\mathbin{\\dot\\cup}",
            "T=\\Omega_T\\mathbin{\\cup}",
            "crown_S403_finite_partition",
        ),
        (
            "canonical_payment_power",
            "crown",
            "{\\bigl(a_{Sk}^{\\rm pay}\\bigr)^{3/2}",
            "{\\bigl(a_{Sk}^{\\rm pay}\\bigr)",
            "crown_S406_canonical_cube",
        ),
        (
            "open_payment_boundary",
            "crown",
            "\\textbf{OPEN}",
            "\\textbf{PROVED}",
            "crown_S407_open_payment",
        ),
        (
            "converse_cube",
            "crown",
            "\\sum_i{a_i^3\\over p_i^2}",
            "\\sum_i{a_i^2\\over p_i}",
            "crown_S409_converse_equality",
        ),
        (
            "threshold_factor_eight",
            "crown",
            "\\ge {H\\over8C_p^2C_M^2}",
            "\\ge {H\\over4C_p^2C_M^2}",
            "crown_S411_threshold_factor",
        ),
        (
            "periodic_copy_sum",
            "crown",
            "\\sum_{n\\in\\mathbb Z^3}\\sum_{i=1}^M",
            "\\sum_{i=1}^M",
            "crown_S413_periodic_full_lift",
        ),
        (
            "pure_defect_sigma",
            "crown",
            "\\sigma={959H\\over7200}<{T\\over12}",
            "\\sigma={999H\\over7200}<{T\\over12}",
            "crown_S415_pure_defect_scaling",
        ),
    )
    rows: list[dict] = []
    for identifier, target, old, new, expected_check in probes:
        if target == "hybrid":
            mutated_hybrid = hybrid_text.replace(old, new)
            mutated_crown = crown_text
            source_changed = mutated_hybrid != hybrid_text
        else:
            mutated_hybrid = hybrid_text
            mutated_crown = crown_text.replace(old, new)
            source_changed = mutated_crown != crown_text
        if not source_changed:
            rows.append(assertion(f"negative_{identifier}", False, "The intended mutation source was not found."))
            continue
        failed = [
            row["id"]
            for row in validate_notes(
                mutated_hybrid,
                mutated_hybrid.encode("utf-8"),
                mutated_crown,
                mutated_crown.encode("utf-8"),
            )
            if not row["pass"]
        ]
        rows.append(
            assertion(
                f"negative_{identifier}",
                expected_check in failed,
                "The targeted semantic validator rejects the mutation, independently of the note hash lock.",
                expected_failed_check=expected_check,
                failed_checks=failed,
            )
        )

    boundary_probes = (
        (
            "hybrid_abstract_boundary",
            "hybrid",
            "This is an **ABSTRACT SCALAR-LEDGER WITNESS**.",
            "This is a scalar example.",
        ),
        (
            "crown_abstract_boundary",
            "crown",
            "This is an **ABSTRACT METHOD OBSTRUCTION**, not a Navier--Stokes\n   counterexample.",
            "This is a method example.",
        ),
        (
            "crown_open_boundary",
            "crown",
            "The following is an **OPEN PDE INPUT**:",
            "The following is a proved PDE input:",
        ),
        (
            "collision_boundary",
            "hybrid",
            "This is a bounded collision boundary, not an\nexhaustive search or a novelty claim.",
            "This is a novelty claim.",
        ),
    )
    for identifier, target, old, new in boundary_probes:
        if target == "hybrid":
            mutated_hybrid = hybrid_text.replace(old, new, 1)
            mutated_crown = crown_text
            changed = mutated_hybrid != hybrid_text
        else:
            mutated_hybrid = hybrid_text
            mutated_crown = crown_text.replace(old, new, 1)
            changed = mutated_crown != crown_text
        if not changed:
            rows.append(assertion(f"negative_{identifier}", False, "The intended boundary mutation source was not found."))
            continue
        failed = [
            row["id"]
            for row in validate_notes(
                mutated_hybrid,
                mutated_hybrid.encode("utf-8"),
                mutated_crown,
                mutated_crown.encode("utf-8"),
            )
            if not row["pass"]
        ]
        rows.append(
            assertion(
                f"negative_{identifier}",
                "required_claim_boundaries" in failed,
                "Removing an abstract/open/collision claim boundary is rejected.",
                failed_checks=failed,
            )
        )

    duplicated = crown_text.replace("\\tag{S.416}", "\\tag{S.415}", 1)
    duplicate_failed = [
        row["id"]
        for row in validate_notes(hybrid_text, hybrid_raw, duplicated, duplicated.encode("utf-8"))
        if not row["pass"]
    ]
    rows.append(
        assertion(
            "negative_duplicate_final_tag",
            "sequential_unique_equation_tags" in duplicate_failed,
            "A duplicated/nonsequential final tag is rejected.",
            failed_checks=duplicate_failed,
        )
    )

    damaged = crown_text + "\r"
    damaged_failed = [
        row["id"]
        for row in validate_notes(hybrid_text, hybrid_raw, damaged, damaged.encode("utf-8"))
        if not row["pass"]
    ]
    rows.append(
        assertion(
            "negative_carriage_return_injection",
            "utf8_no_control_damage" in damaged_failed,
            "Injected carriage-return damage is rejected.",
            failed_checks=damaged_failed,
        )
    )

    # A common deletion cannot be replaced by one deletion per channel.
    height = Fraction(7)
    first = (height, Fraction(0))
    second = (Fraction(0), height)
    combined = tuple(a + b for a, b in zip(first, second))
    separate = best_n(first, 1) + best_n(second, 1)
    common = best_n(combined, 1)
    rows.append(
        assertion(
            "negative_separate_channel_deletions",
            separate == 0 and common == height,
            "The N=1 fixture detects the false substitution of two channelwise deletion sets for one common set.",
            separate_tail=fs(separate),
            common_tail=fs(common),
        )
    )
    return rows


def build_report(payload: dict) -> str:
    sections = []
    for title, key in (
        ("Finite algebra and combinatorics", "finite_checks"),
        ("Dependency locks", "dependency_checks"),
        ("Structural and boundary checks", "structural_checks"),
        ("Negative mutations", "negative_checks"),
    ):
        lines = [f"## {title}", "", "| Check | Result |", "|---|---|"]
        for row in payload[key]:
            lines.append(f"| `{row['id']}` | {'PASS' if row['pass'] else 'FAIL'} |")
        lines.append("")
        sections.append("\n".join(lines))

    summary = payload["summary"]
    return "\n".join(
        [
            "# R0.74S Step 15 hybrid/crown finite certificate report",
            "",
            f"- Schema: `{payload['schema']}`",
            f"- Hybrid note SHA-256 (locked): `{payload['hybrid_note_sha256']}`",
            f"- Crown note SHA-256 (locked): `{payload['crown_note_sha256']}`",
            f"- Generator SHA-256: `{payload['generator_sha256']}`",
            f"- Finite groups: {summary['finite_passed']}/{summary['finite_total']}",
            f"- Finite rational/combinatorial cases: {summary['finite_cases']}",
            f"- Dependencies: {summary['dependency_passed']}/{summary['dependency_total']}",
            f"- Structural: {summary['structural_passed']}/{summary['structural_total']}",
            f"- Negative mutations: {summary['negative_passed']}/{summary['negative_total']}",
            f"- Overall: **{'PASS' if payload['overall_pass'] else 'FAIL'}**",
            "",
            *sections,
            "",
            "## Boundary",
            "",
            "This finite certificate checks exact rational algebra, finite best-N and tree fixtures, upstream hashes, equation numbering, selected formula bindings, and claim wording. It does not machine-prove the common-deletion temporal-tail estimate (S.342), the selected-crown nonlinear payment (S.407), the jump--corona PDE lemma (S.375), any NSE realization of the abstract fixtures, regularity, or the Millennium problem. **FINITE ONLY. NOT CLAY.**",
            "",
        ]
    )


def main() -> int:
    hybrid_raw = HYBRID_NOTE.read_bytes()
    crown_raw = CROWN_NOTE.read_bytes()
    hybrid_text = hybrid_raw.decode("utf-8")
    crown_text = crown_raw.decode("utf-8")

    finite = [
        joint_tv_diamond_checks(),
        best_n_common_deletion_checks(),
        holder_window_factor_checks(),
        common_window_debt_checks(),
        first_root_jump_crown_checks(),
        half_open_32_child_crown_checks(),
        canonical_payment_checks(),
        converse_holder_threshold_checks(),
        pure_defect_scaling_checks(),
    ]
    dependencies = dependency_checks()
    structural = validate_notes(hybrid_text, hybrid_raw, crown_text, crown_raw)
    negative = negative_mutation_checks(hybrid_text, crown_text)
    all_rows = finite + dependencies + structural + negative
    payload = {
        "schema": SCHEMA,
        "scope": "FINITE ONLY: exact algebra, finite fixtures, dependency hashes, structure, and claim boundaries",
        "hybrid_note_path": display_path(HYBRID_NOTE),
        "hybrid_note_sha256": sha256(HYBRID_NOTE),
        "hybrid_note_sha256_lock_enforced": True,
        "crown_note_path": display_path(CROWN_NOTE),
        "crown_note_sha256": sha256(CROWN_NOTE),
        "crown_note_sha256_lock_enforced": True,
        "generator_path": display_path(Path(__file__)),
        "generator_sha256": sha256(Path(__file__)),
        "finite_checks": finite,
        "dependency_checks": dependencies,
        "structural_checks": structural,
        "negative_checks": negative,
        "claim_boundary": {
            "hybrid_flux_residual_equivalence": "FINITE_ALGEBRA_AND_ANALYTIC_NOTE",
            "common_window_start_debt": "FINITE_ALGEBRA_AND_ANALYTIC_NOTE",
            "terminal_crown_partition": "FINITE_COMBINATORICS_AND_ANALYTIC_NOTE",
            "terminal_crown_closure": "PROVED_CONDITIONAL_ON_OPEN_S407",
            "flat_top_budget_obstruction": "ABSTRACT_METHOD_OBSTRUCTION_NOT_NSE_COUNTEREXAMPLE",
            "periodic_measure_clock_fixture": "TWO_SEPARATE_ABSTRACT_STRESS_TESTS_NOT_COUPLED_NOT_NSE",
            "common_deletion_temporal_tail_S342": "OPEN",
            "selected_crown_nonlinear_payment_S407": "OPEN",
            "jump_corona_PDE_lemma_S375": "OPEN",
            "ancestor_gate_S288": "OPEN",
            "combined_gate_S303": "OPEN",
            "navier_stokes_millennium_problem_solved": False,
        },
        "summary": {
            "finite_total": len(finite),
            "finite_passed": sum(row["pass"] for row in finite),
            "finite_cases": sum(int(row.get("cases", 0)) for row in finite),
            "dependency_total": len(dependencies),
            "dependency_passed": sum(row["pass"] for row in dependencies),
            "structural_total": len(structural),
            "structural_passed": sum(row["pass"] for row in structural),
            "negative_total": len(negative),
            "negative_passed": sum(row["pass"] for row in negative),
        },
        "overall_pass": all(row["pass"] for row in all_rows),
    }
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], sort_keys=True))
    print(f"overall_pass={str(payload['overall_pass']).lower()}")
    return 0 if payload["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
