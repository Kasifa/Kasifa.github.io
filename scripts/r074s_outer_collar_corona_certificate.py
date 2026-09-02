#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 14.

This standard-library-only producer checks finite rational fixtures behind
the outer-collar alignment, equal-coordinate best-N spike, cubic Holder
interface, parabolic density-root and jump-tree arithmetic, harmonic Dini
telescope, heat-shear period count, and the inherited Step 13 critical tree.
It also locks the reviewed upstream dependencies and fail-closes selected
formula and claim-boundary wording in the Step 14 note.

The reviewed main-note SHA-256 is locked.  The certificate does not
machine-prove the analytic pressure
decomposition, any suitable-weak-solution estimate, the open temporal tail,
the open jump--corona lemma, an NSE realization of an abstract fixture,
regularity, or the Navier--Stokes Millennium problem.
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
NOTE = Path(
    os.environ.get(
        "R074S_OUTER_COLLAR_NOTE",
        REPO / "research/r074s_outer_collar_corona_obstruction.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_OUTER_COLLAR_JSON",
        REPO / "research/r074s_outer_collar_corona_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_OUTER_COLLAR_REPORT",
        REPO / "research/r074s_outer_collar_corona_certificate_report.md",
    )
)

SCHEMA = "r074s-outer-collar-corona-certificate-v1"
EXPECTED_TAGS = tuple(f"S.{number}" for number in range(343, 377))
LOCKED_NOTE_SHA256 = "c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9"

DEPENDENCIES = {
    "R0.74P": (
        REPO / "research/r074p_temporal_observable_triage.md",
        "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    ),
    "R0.74S-step12": (
        REPO / "research/r074s_terminal_window_morrey_packing.md",
        "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f",
    ),
    "R0.74S-step13": (
        REPO / "research/r074s_temporal_integrability_morrey_threshold.md",
        "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de",
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


def exact(
    identifier: str,
    left: Fraction,
    right: Fraction,
    note: str,
) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def geometric_sum(ratio: Fraction, length: int) -> Fraction:
    return sum((ratio**depth for depth in range(length)), Fraction(0))


def exact_scaling_checks() -> list[dict]:
    """Small symbolic exponent and branching identities."""
    return [
        exact(
            "dimensionless_flux_prefactor_R_power",
            Fraction(2) - Fraction(1),
            Fraction(1),
            "R^2 times the inherited 1/R flux prefactor leaves gamma_k R.",
        ),
        exact(
            "pointwise_post_gradient_R_power",
            Fraction(2) - Fraction(1) - Fraction(1),
            Fraction(0),
            "Pointwise in dimensionless time, |grad psi|=O(R^-1) removes the remaining bare R power.",
        ),
        exact(
            "L1_time_change_before_gradient_R_power",
            Fraction(2) - Fraction(1) - Fraction(2),
            Fraction(-1),
            "The change d sigma=dt/R^2 turns the gamma_k R majorant into gamma_k/R before the gradient bound.",
        ),
        exact(
            "L1_time_change_after_gradient_R_power",
            Fraction(2) - Fraction(1) - Fraction(2) - Fraction(1),
            Fraction(-2),
            "After d sigma=dt/R^2 and |grad psi|=O(R^-1), the direct spacetime row has R^-2.",
        ),
        exact(
            "outer_collar_payment_index",
            Fraction(2 ** (7 + 1)),
            Fraction(2**8),
            "The outer face of shell k starts at the left edge of A_k(2R).",
        ),
        exact(
            "inner_collar_payment_index",
            Fraction(2 ** (7 - 1)),
            Fraction(2**6),
            "The hard inner boundary of shell k is the right edge of A_(k-2)(2R).",
        ),
        exact(
            "inner_weight_log_ratio_coefficient",
            Fraction(4**6 - 4**4, 32),
            Fraction(15 * 4**4, 32),
            "The logarithmic gamma_k/gamma_(k-2) exponent has coefficient 15.",
        ),
        exact(
            "aligned_outer_log_ratio",
            Fraction(4**6 - 4**6, 32),
            Fraction(0),
            "Equal target and payment weights give no outer-face logarithmic gain.",
        ),
        exact(
            "parabolic_children",
            Fraction(2**3 * 2**2),
            Fraction(32),
            "Three spatial halvings and one time-quartering give 32 children.",
        ),
        exact(
            "critical_spatial_cube_conservation",
            Fraction(8) * Fraction(1, 2) ** 3,
            Fraction(1),
            "Eight spatial children with half coefficients conserve the cube.",
        ),
        exact(
            "cubic_holder_conjugacy",
            Fraction(1, 3) + Fraction(2, 3),
            Fraction(1),
            "The coefficient cube and payment power 2/3 are Holder conjugates.",
        ),
        exact(
            "dissipation_pullback_length_dimension",
            Fraction(5) - Fraction(4),
            Fraction(1),
            "|grad u|^2 dx dt has one power of length under NSE scaling.",
        ),
    ]


def collar_geometry_checks() -> dict:
    """Exact endpoint and logarithmic-weight checks on a rational grid."""
    radii = (Fraction(1, 8), Fraction(1), Fraction(7, 3))
    cases = 0
    failures: list[dict] = []
    for radius in radii:
        for k in range(1, 19):
            rho = Fraction(2**k) * radius
            outer_left = 2 * rho
            outer_right = 2 * rho + radius / 8
            payment_left = Fraction(2 ** (k + 1)) * radius
            payment_right = Fraction(2 ** (k + 2)) * radius
            cases += 1
            if not (
                outer_left == payment_left
                and outer_left < outer_right < payment_right
            ):
                failures.append(
                    {"kind": "outer", "R": fs(radius), "k": k}
                )

            if k >= 3:
                inner_left = rho - radius / 8
                inner_right = rho
                inner_payment_left = Fraction(2 ** (k - 1)) * radius
                inner_payment_right = Fraction(2**k) * radius
                log_ratio = Fraction(4 ** (k - 1) - 4 ** (k - 3), 32)
                expected = Fraction(15 * 4 ** (k - 3), 32)
                cases += 1
                if not (
                    inner_payment_left < inner_left < inner_right
                    and inner_right == inner_payment_right
                    and log_ratio == expected
                    and log_ratio > 0
                ):
                    failures.append(
                        {"kind": "inner", "R": fs(radius), "k": k}
                    )
            else:
                cases += 1
                if not (rho <= 4 * radius < 8 * radius):
                    failures.append(
                        {"kind": "core", "R": fs(radius), "k": k}
                    )

    return assertion(
        "collar_indices_gamma_ratios_and_R_geometry",
        not failures,
        "Outer faces align with A_k(2R), inner faces with A_(k-2)(2R), and the gamma-log ratio is exact.",
        cases=cases,
        failures=failures,
    )


def pointwise_weight_tail_checks() -> dict:
    """Check the shell-index implication and a uniform exponential tail majorant."""
    cases = 0
    failures: list[dict] = []
    # On A_j(2R), membership in B_(4 rho_k) forces k>=j.  Moreover the
    # weight exponent increment is at least 3/32 at every subsequent step,
    # so gamma_(j+n)/gamma_j is bounded by exp(-3n/32).
    for radius in (Fraction(1, 8), Fraction(1), Fraction(7, 3)):
        for j in range(1, 18):
            annulus_left = Fraction(2 ** (j + 1)) * radius
            for k in range(1, 24):
                support_right = Fraction(2 ** (k + 2)) * radius
                can_meet = annulus_left < support_right
                cases += 1
                if can_meet != (k >= j):
                    failures.append(
                        {"kind": "support_index", "R": fs(radius), "j": j, "k": k}
                    )
            for offset in range(16):
                k = j + offset
                exponent_gap = Fraction(4 ** (k - 1) - 4 ** (j - 1), 32)
                geometric_gap = Fraction(3 * offset, 32)
                cases += 1
                if exponent_gap < geometric_gap:
                    failures.append(
                        {"kind": "weight_tail", "j": j, "offset": offset}
                    )

    return assertion(
        "pointwise_super_Gaussian_weight_tail_index_grid",
        not failures,
        "Meeting B_(4 rho_k) from A_j(2R) forces k>=j, and exponent gaps dominate a uniform geometric tail.",
        cases=cases,
        failures=failures,
    )


def best_n_tail(values: tuple[Fraction, ...], budget: int) -> Fraction:
    return sum(sorted(values, reverse=True)[budget:], Fraction(0))


def aligned_spike_checks() -> dict:
    """Equal-coordinate and narrow-width fixtures for every sampled N."""
    # If d=t^-r and 1/p-1=-1/r, then d^(1/p-1)=t exactly.
    temporal_types = (
        ("p_4_3", Fraction(4, 3), 4),
        ("p_3_2", Fraction(3, 2), 3),
        ("p_2", Fraction(2), 2),
        ("p_infinity", None, 1),
    )
    payments = (Fraction(1, 3), Fraction(1), Fraction(27, 5))
    profile_norms = (Fraction(1, 2), Fraction(1), Fraction(7, 3))
    cases = 0
    failures: list[dict] = []

    for budget in range(17):
        size = budget + 1
        for label, p, width_power in temporal_types:
            reciprocal_p = Fraction(0) if p is None else 1 / p
            if reciprocal_p - 1 != Fraction(-1, width_power):
                failures.append({"kind": "temporal_exponent", "p": label})
                continue
            for payment, profile_norm in itertools.product(payments, profile_norms):
                t = Fraction(budget + width_power + 2)
                width = t ** (-width_power)
                scaling = t
                coordinate = payment * profile_norm * scaling / size
                values = tuple(coordinate for _ in range(size))

                # Positive rational proxies suffice because alpha_i=w_i cancels
                # before the common target coordinate is formed.
                weights = tuple(Fraction(1, index + 2) for index in range(size))
                raw_l1 = tuple(payment / (size * weight) for weight in weights)
                paid = sum(
                    (weight * mass for weight, mass in zip(weights, raw_l1)),
                    Fraction(0),
                )
                tail = best_n_tail(values, budget)
                cases += 1
                if not (
                    0 < width <= 1
                    and paid == payment
                    and tail == coordinate
                    and tail == payment * profile_norm * scaling / (budget + 1)
                ):
                    failures.append(
                        {
                            "kind": "best_N",
                            "N": budget,
                            "p": label,
                            "payment": fs(payment),
                        }
                    )

    # Exact cubic payments make P^(2/3) rational.  For every sampled fixed
    # N and C_*, choose a rational t (hence a smooth-spike width) that beats
    # C_* P^(2/3).
    for budget, q, constant in itertools.product(
        range(10), range(1, 6), (Fraction(1), Fraction(3), Fraction(10))
    ):
        size = budget + 1
        payment = Fraction(q**3)
        target = Fraction(q**2)
        t = constant * target * size / payment + 1
        tail = payment * t / size
        cases += 1
        if not tail > constant * target:
            failures.append(
                {"kind": "threshold", "N": budget, "q": q, "C": fs(constant)}
            )

    return assertion(
        "arbitrary_fixed_N_aligned_smooth_spike_grid",
        not failures,
        "For N=0 through 16, N+1 aligned coordinates retain one equal Lp norm, and narrow rational widths beat sampled C_* P^(2/3) thresholds.",
        cases=cases,
        failures=failures,
    )


def coefficient_cube_holder_checks() -> dict:
    """Exact Holder, optimizer, zero convention, and repeated incidence."""
    alphabet = tuple(Fraction(value) for value in range(4))
    cases = 0
    equality_cases = 0
    failures: list[dict] = []
    for length in range(5):
        for coefficients in itertools.product(alphabet, repeat=length):
            for payment_roots in itertools.product(alphabet, repeat=length):
                # p_i=r_i^3 and a_i=c_i r_i^2 keep every term rational.
                left = sum(
                    (
                        coefficient * root**2
                        for coefficient, root in zip(coefficients, payment_roots)
                    ),
                    Fraction(0),
                )
                cube_sum = sum(
                    (coefficient**3 for coefficient in coefficients), Fraction(0)
                )
                payment_sum = sum(
                    (root**3 for root in payment_roots), Fraction(0)
                )
                cases += 1
                if left > 0 and left**3 == cube_sum * payment_sum**2:
                    equality_cases += 1
                if left**3 > cube_sum * payment_sum**2:
                    failures.append(
                        {
                            "kind": "Holder",
                            "length": length,
                            "coefficients": [fs(value) for value in coefficients],
                            "roots": [fs(value) for value in payment_roots],
                        }
                    )
                    break
            if failures:
                break
        if failures:
            break

    # These coefficient cubes have rational cube roots, so the exact dual
    # optimizer p_i=c_i^3/sum c^3 can be evaluated without floating point.
    for coefficients, root in (
        ((Fraction(1),), Fraction(1)),
        ((Fraction(3), Fraction(4), Fraction(5)), Fraction(6)),
        ((Fraction(6), Fraction(8), Fraction(10)), Fraction(12)),
    ):
        cube_sum = sum((value**3 for value in coefficients), Fraction(0))
        payments = tuple(value**3 / cube_sum for value in coefficients)
        objective = sum(
            (
                value * (value / root) ** 2
                for value in coefficients
            ),
            Fraction(0),
        )
        cases += 1
        if not (
            cube_sum == root**3
            and sum(payments, Fraction(0)) == 1
            and objective == root
            and objective**3 == cube_sum
        ):
            failures.append(
                {"kind": "optimizer", "coefficients": [fs(v) for v in coefficients]}
            )

    # Node zero occurs twice; Holder must see both occurrences in both sums.
    coefficients = (Fraction(2), Fraction(2), Fraction(1, 2))
    roots = (Fraction(1, 3), Fraction(1, 3), Fraction(3, 4))
    left = sum((c * r**2 for c, r in zip(coefficients, roots)), Fraction(0))
    repeated_cubes = sum((c**3 for c in coefficients), Fraction(0))
    repeated_payments = sum((r**3 for r in roots), Fraction(0))
    distinct_payments = roots[0] ** 3 + roots[2] ** 3
    cases += 1
    if not (
        left**3 <= repeated_cubes * repeated_payments**2
        and repeated_payments > distinct_payments
    ):
        failures.append({"kind": "repeated_incidence"})

    return assertion(
        "coefficient_cube_Holder_and_incidence_grid",
        not failures and equality_cases > 0,
        "The cubic Holder inequality, exact dual optimizer, and repeated-incidence payment are checked with rational data.",
        cases=cases,
        equality_cases=equality_cases,
        failures=failures,
    )


def root_threshold_and_lambda_checks() -> dict:
    """First-root bounds, critical factorization, and lambda cancellation."""
    cases = 0
    failures: list[dict] = []

    for level, lam, ratios in itertools.product(
        range(1, 10),
        (Fraction(1, 3), Fraction(1), Fraction(7, 2)),
        (
            (Fraction(5, 4), Fraction(3, 2)),
            (Fraction(9, 8), Fraction(7, 4), Fraction(2)),
        ),
    ):
        radii = tuple(Fraction(index + 1, 2**level) for index in range(len(ratios)))
        masses = tuple(
            lam * radius * ratio for radius, ratio in zip(radii, ratios)
        )
        total_mass = sum(masses, Fraction(0))
        cases += 1
        if not (
            all(
                lam * radius < mass <= 2 * lam * radius
                for radius, mass in zip(radii, masses)
            )
            and sum(radii, Fraction(0)) <= total_mass / lam
        ):
            failures.append(
                {"kind": "first_root", "level": level, "lambda": fs(lam)}
            )

    # rho=r^3 and m=z^2 r^3 make c=r and p=z^3 r^3 rational.
    for r, z in itertools.product(
        (Fraction(1, 3), Fraction(1), Fraction(5, 2)),
        (Fraction(1, 2), Fraction(1), Fraction(7, 3)),
    ):
        rho = r**3
        mass = z**2 * r**3
        coefficient = r
        payment_root = z * r
        payment = payment_root**3
        cases += 1
        if not (
            mass == coefficient * payment_root**2
            and mass**3 == coefficient**3 * payment**2
            and coefficient**3 == rho
        ):
            failures.append({"kind": "factorization", "r": fs(r), "z": fs(z)})

    # lambda=t^2/2 makes sqrt(2 lambda)=t.  Cubing the full Holder
    # product removes the remaining cube root and leaves 2 M^3 exactly.
    for mass, t in itertools.product(
        (Fraction(1, 5), Fraction(1), Fraction(11, 3)),
        (Fraction(1, 2), Fraction(1), Fraction(5, 2)),
    ):
        lam = t**2 / 2
        radius_sum_bound = mass / lam
        payment_sum_bound = t * mass
        product_cube = radius_sum_bound * payment_sum_bound**2
        cases += 1
        if product_cube != 2 * mass**3:
            failures.append(
                {"kind": "lambda_cancel", "M": fs(mass), "lambda": fs(lam)}
            )

    return assertion(
        "density_root_threshold_factorization_and_lambda_no_gain",
        not failures,
        "First-root thresholds, a_Q=c_Q p_Q^(2/3), and the cubed lambda-cancellation identity hold exactly.",
        cases=cases,
        failures=failures,
    )


def jump_decay_checks() -> dict:
    """32-child scaling and alpha=1,3,5 first-jump Dini fixtures."""
    cases = 0
    failures: list[dict] = []
    kappas = (Fraction(5, 4), Fraction(3, 2), Fraction(2), Fraction(7, 3))
    for alpha, kappa, count in itertools.product((1, 3, 5), kappas, range(2, 8)):
        theta = Fraction(1, 2 ** (alpha - 1)) / kappa
        radii = tuple(Fraction(1, 1) / (kappa * count) for _ in range(count))
        alpha_sum = sum((radius**alpha for radius in radii), Fraction(0))
        cases += 1
        if not (
            sum(radii, Fraction(0)) == 1 / kappa
            and all(radius <= Fraction(1, 2) for radius in radii)
            and alpha_sum <= theta
            and 0 < theta < 1
        ):
            failures.append(
                {
                    "kind": "jump_decay",
                    "alpha": alpha,
                    "kappa": fs(kappa),
                    "count": count,
                }
            )
        for generations in (1, 2, 5, 13):
            partial = geometric_sum(theta, generations)
            bound = 1 / (1 - theta)
            cases += 1
            if not partial < bound:
                failures.append(
                    {
                        "kind": "Dini",
                        "alpha": alpha,
                        "kappa": fs(kappa),
                        "generations": generations,
                    }
                )

    cases += 1
    if not 2**3 * 2**2 == 32:
        failures.append({"kind": "branching"})

    return assertion(
        "parabolic_32_child_and_alpha_1_3_5_jump_decay",
        not failures,
        "The 32-child count and theta_alpha=2^(1-alpha)/kappa bounds are exact for alpha 1, 3, and 5.",
        cases=cases,
        failures=failures,
    )


def harmonic_dini_telescope_checks() -> dict:
    """Exact strict-but-nonsummable product and dyadic block growth."""
    cases = 0
    failures: list[dict] = []
    for start in (0, 1, 3, 11, 37):
        partial = Fraction(0)
        for length in range(65):
            direct = Fraction(1)
            for index in range(length):
                direct *= Fraction(start + index + 1, start + index + 2)
            closed = Fraction(start + 1, start + length + 1)
            partial += direct
            cases += 1
            if direct != closed:
                failures.append(
                    {"kind": "telescope", "start": start, "length": length}
                )
        if partial <= 1:
            failures.append({"kind": "partial_growth", "start": start})

    # At start zero, every dyadic denominator block contributes at least
    # one half.  Hence the finite lower bounds grow without a uniform cap.
    accumulated = Fraction(0)
    for block in range(12):
        block_sum = sum(
            (Fraction(1, denominator) for denominator in range(2**block, 2 ** (block + 1))),
            Fraction(0),
        )
        accumulated += block_sum
        cases += 1
        if block_sum < Fraction(1, 2) or accumulated < Fraction(block + 1, 2):
            failures.append({"kind": "dyadic_block", "block": block})

    return assertion(
        "harmonic_strict_factor_Dini_telescope",
        not failures,
        "The product of theta_d=(d+1)/(d+2) telescopes harmonically, while dyadic blocks force unbounded partial sums.",
        cases=cases,
        failures=failures,
    )


def heat_shear_period_checks() -> dict:
    """Count cos^2 periods in every pre-wavelength dyadic child."""
    cases = 0
    failures: list[dict] = []
    for frequency_level in range(1, 18):
        frequency = 2**frequency_level
        for parent_depth in range(frequency_level):
            child_depth = parent_depth + 1
            child_count = 2**child_depth
            periods_per_child = 2 ** (frequency_level - parent_depth)
            # Lengths are measured in units of pi.  A child has length
            # 2/2^(d+1), while cos^2(nx) has period 1/n.
            child_length = Fraction(2, child_count)
            period_length = Fraction(1, frequency)
            period_ratio = child_length / period_length
            spatial_mass_ratio = Fraction(1, 2) ** 3
            cases += 1
            if not (
                period_ratio == periods_per_child
                and period_ratio.denominator == 1
                and periods_per_child >= 2
                and spatial_mass_ratio == Fraction(1, 8)
            ):
                failures.append(
                    {
                        "L": frequency_level,
                        "parent_depth": parent_depth,
                        "period_ratio": fs(period_ratio),
                    }
                )

    return assertion(
        "heat_shear_dyadic_period_count",
        not failures,
        "For n=2^L and parent depth d<L, every spatial child contains 2^(L-d) full cos^2 periods and receives mass 1/8.",
        cases=cases,
        failures=failures,
    )


def step13_critical_tree_checks() -> dict:
    """Recheck the inherited eight-ary critical ledger used in the corona."""
    cases = 0
    failures: list[dict] = []
    for m in range(1, 11):
        levels = m**3
        p_total = Fraction(levels, m**3)
        b_total = Fraction(levels, m**2)
        s_total = Fraction(5 * levels, 3 * m**2)
        square_total = (
            Fraction(25, 9 * m**4)
            * geometric_sum(Fraction(1, 8), levels)
        )
        square_bound = Fraction(200, 63 * m**4)
        cases += 1
        if not (
            p_total == 1
            and b_total == m
            and s_total == Fraction(5 * m, 3)
            and square_total < square_bound
        ):
            failures.append({"kind": "global", "m": m})

        for depth in range(min(levels, 10)):
            b = Fraction(1, m**2 * 8**depth)
            s = Fraction(5, 3 * m**2 * 8**depth)
            c = Fraction(1, 2**depth)
            p_root = Fraction(1, m * 2**depth)
            payment = p_root**3
            subtree = b**2 * geometric_sum(Fraction(1, 8), levels - depth)
            nonleaf_relation = depth == levels - 1 or 8 * (c / 2) ** 3 == c**3
            cases += 1
            if not (
                8**depth * b == Fraction(1, m**2)
                and 8**depth * s == Fraction(5, 3 * m**2)
                and 8**depth * payment == Fraction(1, m**3)
                and c * p_root**2 == b
                and nonleaf_relation
                and subtree <= Fraction(8, 7) * b**2
            ):
                failures.append({"kind": "node", "m": m, "depth": depth})

        total_nodes = (8**levels - 1) // 7
        for budget in range(min(25, total_nodes)):
            removed = Fraction(0)
            remaining = budget
            for depth in range(levels):
                at_depth = min(remaining, 8**depth)
                removed += Fraction(at_depth, m**2 * 8**depth)
                remaining -= at_depth
                if remaining == 0:
                    break
            exact_tail = Fraction(m) - removed
            lower_tail = Fraction(m) - Fraction(budget, m**2)
            cases += 1
            if exact_tail < lower_tail:
                failures.append({"kind": "best_N", "m": m, "N": budget})

    # The Step 14 embedding uses one temporal branch and all eight spatial
    # children.  It conserves mass while density m/rho drops by 1/4 at each
    # generation, so it never makes a relative upward kappa-jump.
    for rho_zero, mass_zero, depth, kappa in itertools.product(
        (Fraction(1, 3), Fraction(1), Fraction(5, 2)),
        (Fraction(1, 7), Fraction(1), Fraction(9, 4)),
        range(10),
        (Fraction(5, 4), Fraction(2), Fraction(7, 3)),
    ):
        rho = rho_zero / 2**depth
        mass = mass_zero / 8**depth
        density = mass / rho
        closed_density = mass_zero / rho_zero / 4**depth
        child_mass = mass / 8
        child_density = child_mass / (rho / 2)
        cases += 1
        if not (
            density == closed_density
            and 8 * child_mass == mass
            and child_density == density / 4
            and child_density < kappa * density
        ):
            failures.append(
                {
                    "kind": "rho_mass_density_embedding",
                    "depth": depth,
                    "kappa": fs(kappa),
                }
            )

    cases += 1
    if 1 * 8 != 8 or 8 * Fraction(1, 2) ** 3 != 1:
        failures.append({"kind": "one_temporal_eight_spatial_embedding"})

    return assertion(
        "step13_critical_eight_ary_tree_fixtures",
        not failures,
        "The inherited linear, square, factorization, nonleaf cube-conservation, and best-N fixtures remain exact inside one temporal branch.",
        cases=cases,
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
                "The reviewed upstream source matches its locked SHA-256.",
                path=display_path(path),
                expected_sha256=expected,
                actual_sha256=actual,
            )
        )
    return rows


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


def validate_text(text: str, raw: bytes) -> list[dict]:
    tags = tuple(re.findall(r"\\tag\{(S\.\d+)\}", text))
    lines = text.splitlines()
    compact = re.sub(r"\s+", " ", text)
    forbidden = re.findall(
        r"(?:\bwe\b|\bour\b|攻关|主攻|研究纪律|三重审计|杀死错误想法)",
        text,
        flags=re.IGNORECASE,
    )
    required = (
        "**ABSTRACT METHOD OBSTRUCTION**",
        "not a Navier--Stokes counterexample",
        "This implication is **PROVED / CONDITIONAL**",
        "statement is **OPEN** for the bare periodic suitable-weak class",
        "No DNS or DGX computation is used. **NOT CLAY.**",
        "This is a collision boundary, not a novelty or priority claim",
        "Target (S.342) remains **OPEN**",
        r"The same \(E_\tau\) must be used for the defect and high-Rayleigh ancestors",
        "repeated incidence",
        "Neither partial regularity, the bare measure mass, nor the current moving-tube estimate",
        "The certificate does not machine-prove",
    )
    # The final item above belongs to the certificate boundary rather than
    # the note.  It is removed from the required-note set below and is kept
    # here as an explicit reminder in source review.
    required_note = required[:-1]
    citation_urls = (
        "https://doi.org/10.1002/cpa.3160350604",
        "https://doi.org/10.4171/AIHPC/20",
        "https://doi.org/10.1006/aima.2000.1937",
        "https://doi.org/10.1016/j.aim.2024.109654",
        "https://doi.org/10.1007/s00526-017-1151-7",
    )

    rows = [
        assertion(
            "main_note_hash_lock",
            hashlib.sha256(raw).hexdigest() == LOCKED_NOTE_SHA256,
            "The reviewed Step 14 note hash is frozen.",
            expected_sha256=LOCKED_NOTE_SHA256,
            actual_sha256=hashlib.sha256(raw).hexdigest(),
            lock_enforced=True,
        ),
        assertion(
            "sequential_unique_equation_tags",
            tags == EXPECTED_TAGS and len(tags) == len(set(tags)),
            "Equation tags are exactly S.343 through S.376, once each and in order.",
            expected=list(EXPECTED_TAGS),
            actual=list(tags),
        ),
        assertion(
            "balanced_display_delimiters",
            text.count("\\[") == text.count("\\]") and text.count("\\[") > 0,
            "Display-math delimiters are balanced.",
            opens=text.count("\\["),
            closes=text.count("\\]"),
        ),
        assertion(
            "required_claim_boundaries",
            all(snippet in compact for snippet in required_note),
            "Abstract/PDE, conditional/open, collision, no-compute, and NOT CLAY boundaries are present.",
            missing=[snippet for snippet in required_note if snippet not in compact],
        ),
        assertion(
            "primary_source_urls",
            all(url in text for url in citation_urls),
            "All five bounded primary-source links are present.",
            missing=[url for url in citation_urls if url not in text],
        ),
        assertion(
            "discouraged_prose_absent",
            not forbidden,
            "The published-writing discouraged phrases are absent.",
            matches=forbidden,
        ),
        assertion(
            "utf8_no_control_damage",
            b"\x00" not in raw and b"\r" not in raw,
            "The note has no NUL or carriage-return corruption.",
        ),
        assertion(
            "no_trailing_whitespace",
            not any(line.endswith((" ", "\t")) for line in lines),
            "The note has no trailing spaces or tabs.",
        ),
    ]

    equations = {tag: equation_source(text, tag) for tag in EXPECTED_TAGS}
    formula_bindings = (
        (
            "S343_two_collar_geometry",
            all(
                snippet in equations["S.343"]
                for snippet in (
                    "C_{k,R}^-&:=\\{\\rho_k-R/8<|y|<\\rho_k\\}",
                    "C_{k,R}^+&:=\\{2\\rho_k<|y|<2\\rho_k+R/8\\}",
                    "\\subset B_{3\\rho_k}",
                )
            ),
            "S.343 retains both collars and the shell-scale harmonic buffer.",
        ),
        (
            "S344_fixed_gauge_shell_harmonicity",
            "c_R(t)=c_{2R}^{M,R}(t)" in text
            and "p_{k,R}^{\\rm loc}" in equations["S.344"]
            and "h_{k,R}^{\\rm pr}" in equations["S.344"]
            and "h_{k,R}^{\\rm pr}-c_R" in text
            and "harmonic on \\(B_{3\\rho_k}\\)" in compact,
            "S.344 and its prose retain the fixed gauge and shell-scale harmonic remainder.",
        ),
        (
            "S345_four_signed_channels",
            all(
                snippet in equations["S.345"]
                for snippet in ("^{\\rm cub}", "^{\\rm loc}", "^{\\rm har}", "^{\\rm dr}")
            ),
            "S.345 retains all four signed flux channels.",
        ),
        (
            "S347_dimensionless_R_normalization",
            "R^2|\\dot F_{k,R}" in equations["S.347"]
            and "\\sum_\\alpha\\widehat h" in equations["S.347"],
            "S.347 retains h=R^2|Fdot| and the four-majorant upper bound.",
        ),
        (
            "S348_L1_linear_payment_only",
            "L^1(0,4)" in equations["S.348"]
            and "\\le C P_R^M" in equations["S.348"]
            and "CR^{-2}\\int_{\\mathcal T_R}" in text
            and "\\sum_{k:y\\in B_{4\\rho_k}}\\gamma_k" in text
            and "\\mathbf1_{B_{8R}}(y)+W_{2R}(y)" in text,
            "S.348 retains the R^-2 conversion, pointwise weight sum, and L1 linear payment scale.",
        ),
        (
            "S349_explicit_fixed_index_tail",
            "\\mathfrak H^F_{4/3,K,R}" in equations["S.349"]
            and "\\le \\mathfrak T^F_{4/3,K,R}" in equations["S.349"]
            and "\\mathfrak T^F_{4/3,K,R}" in text
            and ":=\\sum_{k>K}\\|h_{k,R}\\|_{L^{4/3}(0,4)}" in text,
            "S.349 explicitly separates the best-K deletion functional from the fixed first-K index tail.",
        ),
        (
            "S350_collar_payment_indices",
            "C_{k,R}^+\\subset A_k(2R)" in equations["S.350"]
            and "C_{k,R}^-\\subset A_{k-2}(2R)" in equations["S.350"],
            "S.350 retains the aligned outer index and shifted inner index.",
        ),
        (
            "S351_inner_gamma_ratio",
            "{\\gamma_k\\over\\gamma_{k-2}}" in equations["S.351"]
            and "15\\,4^{k-3}\\over32" in equations["S.351"],
            "S.351 retains the exact inner-face super-Gaussian ratio.",
        ),
        (
            "S352_outer_gamma_alignment",
            "{\\gamma_k\\over\\gamma_k}=1" in equations["S.352"],
            "S.352 retains exact target/payment weight alignment.",
        ),
        (
            "spike_quantifiers_and_alignment",
            all(
                snippet in compact
                for snippet in (
                    "Fix \\(p\\in(1,\\infty]\\), integers \\(N,K_0\\ge0\\), and \\(C_*,P>0\\)",
                    "M=N+1",
                    "k_1,\\ldots,k_M>K_0",
                    "w_i=\\alpha_i=\\gamma_{k_i}",
                    "after \\(p,N,K_0,C_*\\), and \\(P\\) are fixed, \\(d\\) can be chosen",
                )
            ),
            "The spike first fixes p,N,K0,C*,P, then chooses d, with N+1 aligned coordinates.",
        ),
        (
            "S354_best_N_spike_scaling",
            "{P\\over N+1}" in equations["S.354"]
            and "d^{1/p-1}" in equations["S.354"],
            "S.354 retains the exact common-deletion tail and narrow-width exponent.",
        ),
        (
            "aligned_spike_abstract_not_PDE_boundary",
            r"This is an **ABSTRACT METHOD OBSTRUCTION**. The \(g_i\) are smooth nonnegative scalar rates, not fluxes generated by one velocity and pressure" in compact,
            "The aligned spike remains explicitly abstract and not a PDE-generated flux family.",
        ),
        (
            "S357_coefficient_cube_budget",
            "{a_{\\nu k}^3\\over p_\\nu^2}" in equations["S.357"]
            and "\\sum_{(\\nu,k)\\in\\mathscr I_\\tau}p_\\nu" in equations["S.357"],
            "S.357 counts cubic coefficients and repeated incidence payments.",
        ),
        (
            "S359_exact_cubic_duality",
            "\\sum_ic_i^3" in equations["S.359"]
            and "p_i^{2/3}" in equations["S.359"],
            "S.359 retains the exact cubic dual formula.",
        ),
        (
            "S360_scale_invariant_measure",
            "\\nu_R(A)&:=R^{-1}" in equations["S.360"],
            "S.360 retains the R^-1 pullback normalization.",
        ),
        (
            "S361_32_child_scaling",
            "=32" in equations["S.361"]
            and "{1\\over2}\\rho_Q" in equations["S.361"],
            "S.361 retains 32 children and radius halving.",
        ),
        (
            "S362_first_root_threshold",
            "\\lambda\\rho_Q<m_Q\\le2\\lambda\\rho_Q" in equations["S.362"]
            and "{\\mathfrak M_R\\over\\lambda}" in equations["S.362"]
            and "every proper ancestor below \\(Q_0\\) has density at most \\(\\lambda\\)" in compact,
            "S.362 retains both first-root density bounds and the antichain radius sum.",
        ),
        (
            "S365_lambda_no_gain_identity",
            "{\\mathfrak M_R\\over\\lambda}" in equations["S.365"]
            and "(2\\lambda)^{1/2}\\mathfrak M_R" in equations["S.365"]
            and "=2^{1/3}\\mathfrak M_R" in equations["S.365"],
            "S.365 retains exact cancellation of the density level.",
        ),
        (
            "S367_alpha_jump_decay",
            "\\theta_\\alpha:={2^{1-\\alpha}\\over\\kappa}<1" in equations["S.367"],
            "S.367 retains the alpha-dependent strict jump coefficient.",
        ),
        (
            "S369_harmonic_Dini_telescope",
            "\\theta_d={d+1\\over d+2}<1" in equations["S.369"]
            and "{d_0+1\\over d_0+n+1}" in equations["S.369"]
            and "=\\infty" in equations["S.369"],
            "S.369 retains the strict-but-nonsummable harmonic telescope.",
        ),
        (
            "S370_critical_eight_child_fixture",
            "8\\left({c_S\\over2}\\right)^3=c_S^3" in equations["S.370"]
            and "\\rho_v=2^{-d}\\rho_0" in text
            and "m_v=8^{-d}m_0" in text
            and "\\Theta(v)={m_0\\over\\rho_0}4^{-d}" in text
            and "no relative \\(\\kappa\\)-jump for any \\(\\kappa>1\\)" in compact
            and "not the root-factor coefficient \\(\\rho^{1/3}\\)" in compact,
            "S.370 retains the rho/m/density embedding, no-jump direction, coefficient distinction, and critical cube conservation.",
        ),
        (
            "S371_bounded_shell_incidence",
            "\\le2" in equations["S.371"]
            and "unperiodized lifted cell" in compact
            and "periodic copies must be unfolded first" in compact
            and "not a statement about one torus cell" in compact,
            "S.371 is restricted to one unfolded Euclidean lift before the two-shell incidence bound is used.",
        ),
        (
            "S372_heat_shear_dyadic_frequency",
            "n=2^L" in equations["S.372"],
            "S.372 retains a dyadic heat-shear frequency.",
        ),
        (
            "S373_heat_shear_mass_split",
            "{1\\over8}" in equations["S.373"]
            and "d(Q)<L" in equations["S.373"],
            "S.373 retains the one-eighth mass split strictly above wavelength.",
        ),
        (
            "S374_zero_physical_flux",
            "\\dot F_{k,R}^{(2^L)}(t)=0" in equations["S.374"],
            "S.374 retains zero physical flux for the exact shear family.",
        ),
        (
            "S375_open_PDE_budgets",
            all(
                snippet in equations["S.375"]
                for snippet in (
                    "q_k^{\\rm top}+q_k^{\\rm cor}",
                    "(\\nu,k):\\nu\\rightsquigarrow k",
                    "p_\\nu\\le C_pP_R^M",
                    "{a_{\\nu k}^3\\over p_\\nu^2}\\le C_{\\rm cor}",
                )
            )
            and "full incidence multiset, not over distinct nodes" in compact,
            "S.375 retains the top, corona, repeated-payment, and cubic budgets.",
        ),
        (
            "S375_forest_levels_uniformity_and_assignment",
            all(
                snippet in compact
                for snippet in (
                    "countable, locally finite forest of comoving parabolic dyadic trees",
                    "fixed finite family of shifted grids",
                    "For each top cell \\(T\\), a construction may select a level \\(\\lambda_T>0\\)",
                    "There should exist a universal \\(\\kappa>1\\)",
                    "The quantity \\(a_{\\nu k}\\) is the part assigned to one jump-skeleton node--shell incidence",
                    "These assignments are part of the asserted PDE construction; the measure-tree facts alone do not define them",
                    "independent of the solution, \\(R\\), \\(\\tau\\), the selected levels \\(\\lambda_T\\), the number of top cells, and the forest depth",
                    "every periodic copy after unfolding and every repeated use across forest tops",
                )
            ),
            "The open lemma retains a countable lifted forest, topwise levels, universal constants, and explicit assignment/incidence quantifiers.",
        ),
        (
            "S376_conditional_arrow",
            "\\text{(S.375)}\\quad\\Longrightarrow\\quad" in equations["S.376"]
            and "\\mathcal S_{N_b}" in equations["S.376"],
            "S.376 remains explicitly conditional on the open lemma.",
        ),
        (
            "fixed_solution_tail_not_uniform",
            "This does not make (S.349) uniform in \\(R\\)" in text
            and "energy bracket has no\navailable uniform bound" in text,
            "The fixed-solution L4/3 tail is not promoted to a uniform payment estimate.",
        ),
    )
    rows.extend(
        assertion(identifier, passed, note)
        for identifier, passed, note in formula_bindings
    )
    return rows


def negative_mutation_checks(text: str) -> list[dict]:
    probes = (
        ("fixed_pressure_gauge", "c_R(t)=c_{2R}^{M,R}(t)", "c_{k,R}(t)=(h_{k,R}^{\\rm pr})_{B_{2\\rho_k}}"),
        ("local_row_R_power", "CR^{-2}\\int_{\\mathcal T_R}", "CR^{-1}\\int_{\\mathcal T_R}"),
        ("pointwise_weight_sum", "\\mathbf1_{B_{8R}}(y)+W_{2R}(y)", "\\mathbf1_{B_{8R}}(y)+W_R(y)"),
        ("fixed_tail_order", "\\le \\mathfrak T^F_{4/3,K,R}", "\\ge \\mathfrak T^F_{4/3,K,R}"),
        ("outer_payment_index", "C_{k,R}^+\\subset A_k(2R)", "C_{k,R}^+\\subset A_{k-1}(2R)"),
        ("inner_payment_index", "C_{k,R}^-\\subset A_{k-2}(2R)", "C_{k,R}^-\\subset A_{k-1}(2R)"),
        ("inner_gamma_exponent", "15\\,4^{k-3}\\over32", "12\\,4^{k-3}\\over32"),
        ("outer_gamma_alignment", "{\\gamma_k\\over\\gamma_k}=1", "{\\gamma_k\\over\\gamma_{k-1}}=1"),
        ("dimensionless_R_power", "R^2|\\dot F_{k,R}", "R|\\dot F_{k,R}"),
        ("spike_coordinate_count", "M=N+1", "M=N"),
        ("spike_weight_alignment", "w_i=\\alpha_i=\\gamma_{k_i}", "w_i=\\gamma_{k_i-1},\\quad\\alpha_i=\\gamma_{k_i}"),
        ("spike_quantifier_order", "after \\(p,N,K_0,C_*\\), and \\(P\\) are fixed, \\(d\\) can be chosen", "after \\(d\\) is chosen, \\(p,N,K_0,C_*\\), and \\(P\\) are fixed"),
        ("spike_width_exponent", "d^{1/p-1}", "d^{1-1/p}"),
        ("coefficient_cube", "{a_{\\nu k}^3\\over p_\\nu^2}", "{a_{\\nu k}^2\\over p_\\nu}"),
        ("duality_cube", "\\sum_ic_i^3", "\\sum_ic_i^2"),
        ("pullback_R_normalization", "\\nu_R(A)&:=R^{-1}", "\\nu_R(A)&:=R^0"),
        ("parabolic_branch_count", "#\\operatorname {child}(Q)=32", "#\\operatorname {child}(Q)=16"),
        ("root_upper_threshold", "m_Q\\le2\\lambda\\rho_Q", "m_Q\\le\\lambda\\rho_Q"),
        ("lambda_no_gain_constant", "=2^{1/3}\\mathfrak M_R", "=\\mathfrak M_R"),
        ("jump_decay_power", "\\theta_\\alpha:={2^{1-\\alpha}\\over\\kappa}<1", "\\theta_\\alpha:={2^{-\\alpha}\\over\\kappa}<1"),
        ("harmonic_theta", "\\theta_d={d+1\\over d+2}<1", "\\theta_d={d\\over d+2}<1"),
        ("critical_corona_radius", "\\rho_v=2^{-d}\\rho_0", "\\rho_v=4^{-d}\\rho_0"),
        ("critical_corona_mass", "m_v=8^{-d}m_0", "m_v=4^{-d}m_0"),
        ("critical_corona_density", "\\Theta(v)={m_0\\over\\rho_0}4^{-d}", "\\Theta(v)={m_0\\over\\rho_0}2^{-d}"),
        ("critical_corona_no_jump", "no relative \\(\\kappa\\)-jump for any", "a relative \\(\\kappa\\)-jump for every"),
        ("critical_coefficient_distinction", "not the root-factor\ncoefficient \\(\\rho^{1/3}\\)", "the same as the root-factor\ncoefficient \\(\\rho^{1/3}\\)"),
        ("critical_child_cube", "8\\left({c_S\\over2}\\right)^3=c_S^3", "8\\left({c_S\\over3}\\right)^3=c_S^3"),
        ("single_lift_cell", "unperiodized lifted cell", "periodized torus cell"),
        ("unfold_before_incidence", "periodic copies must be unfolded first", "periodic copies need not be unfolded"),
        ("shell_incidence", "\\le2.}", "\\le3.}"),
        ("heat_shear_frequency", "n=2^L", "n=3^L"),
        ("heat_shear_split", "={1\\over8}\n", "={1\\over4}\n"),
        ("zero_flux", "\\dot F_{k,R}^{(2^L)}(t)=0", "\\dot F_{k,R}^{(2^L)}(t)\\ne0"),
        ("countable_forest", "countable, locally finite forest", "one finite tree"),
        ("shifted_grid_family", "fixed finite family of shifted grids", "one solution-dependent shifted grid"),
        ("topwise_level", "select a level \\(\\lambda_T>0\\)", "use one global level \\(\\lambda>0\\)"),
        ("universal_kappa", "exist a universal \\(\\kappa>1\\)", "exist a solution-dependent \\(\\kappa>1\\)"),
        ("assignment_binding", "These assignments are part of\nthe asserted PDE construction; the measure-tree facts alone do not define\nthem", "These assignments follow automatically from\nthe measure-tree facts"),
        ("uniform_constants", "and \\(\\kappa\\) are independent of the", "and \\(\\kappa\\) may depend on the"),
        ("unfolded_repeated_payment", "periodic copy after unfolding and every repeated use across forest tops", "only distinct nodes"),
        ("conditional_arrow", "\\text{(S.375)}\\quad\\Longrightarrow\\quad", "\\text{(S.375)}\\quad\\Longleftrightarrow\\quad"),
    )
    rows = []
    for identifier, old, new in probes:
        mutated = text.replace(old, new, 1)
        if mutated == text:
            rows.append(
                assertion(
                    f"negative_{identifier}",
                    False,
                    "The intended mutation source was not found.",
                )
            )
            continue
        failed = [row["id"] for row in validate_text(mutated, mutated.encode("utf-8")) if not row["pass"]]
        rows.append(
            assertion(
                f"negative_{identifier}",
                bool(failed),
                "The structural validator rejects the semantic mutation.",
                failed_checks=failed,
            )
        )

    boundary_probes = (
        ("abstract_boundary", "**ABSTRACT METHOD OBSTRUCTION**", "**METHOD EXAMPLE**"),
        ("not_NSE_counterexample", "not a Navier--Stokes counterexample", "is a Navier--Stokes counterexample"),
        ("conditional_boundary", "This implication is **PROVED / CONDITIONAL**", "This implication is **PROVED**"),
        ("open_PDE_lemma", "The following statement is **OPEN**", "The following statement is **PROVED**"),
        ("no_compute_boundary", "No DNS or DGX computation is", "DNS computation is"),
        ("collision_boundary", "This is a collision boundary, not a novelty or priority claim", "This is a novelty and priority claim"),
    )
    for identifier, old, new in boundary_probes:
        mutated = text.replace(old, new)
        if mutated == text:
            rows.append(
                assertion(
                    f"negative_{identifier}",
                    False,
                    "The intended boundary mutation source was not found.",
                )
            )
            continue
        failed = [row["id"] for row in validate_text(mutated, mutated.encode("utf-8")) if not row["pass"]]
        rows.append(
            assertion(
                f"negative_{identifier}",
                bool(failed),
                "The structural validator rejects removal of the claim boundary.",
                failed_checks=failed,
            )
        )

    duplicated = text.replace("\\tag{S.376}", "\\tag{S.375}", 1)
    duplicate_failed = [
        row["id"]
        for row in validate_text(duplicated, duplicated.encode("utf-8"))
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

    damaged = text + "\r"
    damaged_failed = [
        row["id"]
        for row in validate_text(damaged, damaged.encode("utf-8"))
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
    return rows


def build_report(payload: dict) -> str:
    sections = []
    for title, key in (
        ("Exact rational checks", "exact_checks"),
        ("Finite fixture groups", "finite_checks"),
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
            "# R0.74S Step 14 finite certificate report",
            "",
            f"- Schema: `{payload['schema']}`",
            f"- Main note SHA-256 (locked): `{payload['note_sha256']}`",
            f"- Generator SHA-256: `{payload['generator_sha256']}`",
            f"- Exact: {summary['exact_passed']}/{summary['exact_total']}",
            f"- Finite groups: {summary['finite_passed']}/{summary['finite_total']}",
            f"- Finite rational cases: {summary['finite_cases']}",
            f"- Dependencies: {summary['dependency_passed']}/{summary['dependency_total']}",
            f"- Structural: {summary['structural_passed']}/{summary['structural_total']}",
            f"- Negative mutations: {summary['negative_passed']}/{summary['negative_total']}",
            f"- Overall: **{'PASS' if payload['overall_pass'] else 'FAIL'}**",
            "",
            *sections,
            "",
            "## Boundary",
            "",
            "This finite certificate checks exact rational algebra, finite fixtures, upstream hashes, equation numbering, selected formula bindings, and claim wording. It does not machine-prove the analytic pressure decomposition, the inherited PDE estimates, either open packing gate, the open jump--corona lemma, an NSE realization of an abstract fixture, regularity, or the Millennium problem. **FINITE ONLY. NOT CLAY.**",
            "",
        ]
    )


def main() -> int:
    raw = NOTE.read_bytes()
    text = raw.decode("utf-8")
    exact_checks = exact_scaling_checks()
    finite_checks = [
        collar_geometry_checks(),
        pointwise_weight_tail_checks(),
        aligned_spike_checks(),
        coefficient_cube_holder_checks(),
        root_threshold_and_lambda_checks(),
        jump_decay_checks(),
        harmonic_dini_telescope_checks(),
        heat_shear_period_checks(),
        step13_critical_tree_checks(),
    ]
    dependencies = dependency_checks()
    structural = validate_text(text, raw)
    negative = negative_mutation_checks(text)
    all_rows = exact_checks + finite_checks + dependencies + structural + negative
    payload = {
        "schema": SCHEMA,
        "scope": "FINITE ONLY: rational algebra, finite fixtures, dependency hashes, structure, and claim boundaries",
        "note_path": display_path(NOTE),
        "note_sha256": sha256(NOTE),
        "note_sha256_lock_enforced": True,
        "generator_path": display_path(Path(__file__)),
        "generator_sha256": sha256(Path(__file__)),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "dependency_checks": dependencies,
        "structural_checks": structural,
        "negative_checks": negative,
        "claim_boundary": {
            "collar_geometry_and_weight_alignment": "FINITE_AND_TEXT_CHECKED",
            "equal_coordinate_spike": "ABSTRACT_METHOD_OBSTRUCTION_NOT_NSE_COUNTEREXAMPLE",
            "coefficient_cube_implication": "PROVED_CONDITIONAL_ON_DISPLAYED_BUDGETS",
            "density_root_and_jump_tree": "FINITE_FIXTURES_PLUS_ANALYTIC_NOTE",
            "heat_shear_period_split": "FINITE_FIXTURES_PLUS_ANALYTIC_NOTE",
            "analytic_pressure_decomposition": "NOT_MACHINE_PROVED",
            "inherited_componentwise_PDE_payment": "NOT_MACHINE_PROVED",
            "common_deletion_temporal_tail_S342": "OPEN",
            "shell_selective_jump_corona_lemma_S375": "OPEN",
            "ancestor_gate_S288": "OPEN",
            "combined_gate_S303": "OPEN",
            "navier_stokes_millennium_problem_solved": False,
        },
        "summary": {
            "exact_total": len(exact_checks),
            "exact_passed": sum(row["pass"] for row in exact_checks),
            "finite_total": len(finite_checks),
            "finite_passed": sum(row["pass"] for row in finite_checks),
            "finite_cases": sum(int(row.get("cases", 0)) for row in finite_checks),
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
