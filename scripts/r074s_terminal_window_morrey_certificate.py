#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 12.

This standard-library-only producer checks exact finite best-N algebra,
terminal-window split fixtures, rational exponent bookkeeping, moving-tube
cover arithmetic, a symbolic super-Gaussian tail criterion, source integrity,
and the stated claim boundaries in
``r074s_terminal_window_morrey_packing.md``.

It does not machine-prove absolute continuity for NSE flux primitives, the
inherited positive-depth estimate, a uniform terminal-window modulus, either
open packing gate, the conditional Morrey hypothesis, the mixed-norm PDE
estimate, regularity, or the Navier--Stokes Millennium problem.
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
        "R074S_WINDOW_NOTE",
        REPO / "research/r074s_terminal_window_morrey_packing.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_WINDOW_JSON",
        REPO / "research/r074s_terminal_window_morrey_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_WINDOW_REPORT",
        REPO / "research/r074s_terminal_window_morrey_certificate_report.md",
    )
)

# Update these two constants once the moving-packet screen has been merged and
# the main note has received its final byte-level audit.
LOCKED_NOTE_SHA256 = (
    "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f"
)
EXPECTED_LAST_TAG = 306

SCHEMA = "r074s-terminal-window-morrey-certificate-v1"

DEPENDENCIES = {
    "R0.74P": (
        REPO / "research/r074p_temporal_observable_triage.md",
        "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    ),
    "R0.74R-arbitrary": (
        REPO / "research/r074r_arbitrary_clock_extraction_gate.md",
        "ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7",
    ),
    "R0.74R-persistent": (
        REPO / "research/r074r_persistent_lobe_cubic_packing.md",
        "e7f151048e85d95133f8c6414849c0fe9dc40cc48b7a12666b7e21496ddb99b5",
    ),
    "R0.74S-step8": (
        REPO / "research/r074s_defect_relaxed_total_rayleigh_excess.md",
        "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab",
    ),
    "R0.74S-step11": (
        REPO / "research/r074s_shared_budget_terminal_trace_obstruction.md",
        "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693",
    ),
    "R0.74F-packet": (
        REPO / "research/r074f_two_packet_survival.md",
        "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb",
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


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def assertion(identifier: str, passed: bool, note: str, **details) -> dict:
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


def powerset_indices(length: int, max_size: int | None = None):
    upper = length if max_size is None else min(length, max_size)
    for size in range(upper + 1):
        yield from itertools.combinations(range(length), size)


def best_n(values: tuple[Fraction, ...], budget: int) -> Fraction:
    if budget < 0 or any(value < 0 for value in values):
        raise ValueError("best_n requires a nonnegative budget and coordinates")
    return sum(sorted(values, reverse=True)[budget:], Fraction(0))


def best_n_bruteforce(values: tuple[Fraction, ...], budget: int) -> Fraction:
    if budget < 0 or any(value < 0 for value in values):
        raise ValueError("best_n_bruteforce requires nonnegative data")
    candidates = []
    for removed in powerset_indices(len(values), budget):
        removed_set = set(removed)
        candidates.append(
            sum(
                (
                    value
                    for index, value in enumerate(values)
                    if index not in removed_set
                ),
                Fraction(0),
            )
        )
    return min(candidates)


def layer_cake_integral(values: tuple[Fraction, ...], budget: int) -> Fraction:
    """Integrate (#{z_k>t}-N)_+ exactly over its rational breakpoints."""
    levels = sorted({value for value in values if value > 0})
    total = Fraction(0)
    previous = Fraction(0)
    for level in levels:
        count = sum(value >= level for value in values)
        total += (level - previous) * max(count - budget, 0)
        previous = level
    return total


def layer_cake_exhaustive() -> dict:
    alphabet = (
        Fraction(0),
        Fraction(1, 3),
        Fraction(2, 3),
        Fraction(1),
        Fraction(2),
    )
    cases = 0
    failures = []
    for length in range(5):
        for values in itertools.product(alphabet, repeat=length):
            for budget in range(length + 2):
                formula = best_n(values, budget)
                brute = best_n_bruteforce(values, budget)
                integral = layer_cake_integral(values, budget)
                cases += 1
                if formula != brute or formula != integral:
                    failures.append(
                        {
                            "values": [fs(value) for value in values],
                            "budget": budget,
                            "formula": fs(formula),
                            "bruteforce": fs(brute),
                            "layer_cake": fs(integral),
                        }
                    )
                    if len(failures) >= 8:
                        break
            if failures:
                break
        if failures:
            break
    return assertion(
        "best_N_layer_cake_exhaustive",
        not failures,
        "S.278 is checked exactly on every length-at-most-four vector over five rational levels.",
        cases=cases,
        failures=failures,
    )


def best_n_l1_lipschitz_exhaustive() -> dict:
    alphabet = (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(2))
    vectors = tuple(itertools.product(alphabet, repeat=3))
    cases = 0
    failures = []
    for left in vectors:
        for right in vectors:
            distance = sum((abs(a - b) for a, b in zip(left, right)), Fraction(0))
            for budget in range(5):
                gap = abs(best_n(left, budget) - best_n(right, budget))
                cases += 1
                if gap > distance:
                    failures.append(
                        {
                            "left": [fs(value) for value in left],
                            "right": [fs(value) for value in right],
                            "budget": budget,
                            "gap": fs(gap),
                            "l1_distance": fs(distance),
                        }
                    )
                    if len(failures) >= 8:
                        break
            if failures:
                break
        if failures:
            break
    return assertion(
        "best_N_l1_Lipschitz_exhaustive",
        not failures,
        "The S.276 one-Lipschitz estimate is checked exactly on all ordered pairs in a rational grid.",
        cases=cases,
        failures=failures,
    )


def terminal_window_split_exhaustive() -> dict:
    # Each state is (short residual, common-window majorant, depth class).
    states = (
        (Fraction(0), Fraction(0), "shallow"),
        (Fraction(1, 3), Fraction(1, 3), "shallow"),
        (Fraction(1, 3), Fraction(2, 3), "shallow"),
        (Fraction(1), Fraction(2), "shallow"),
        (Fraction(1, 4), Fraction(0), "deep"),
        (Fraction(2), Fraction(0), "deep"),
    )
    cases = 0
    same_set_checks = 0
    failures = []
    for coordinates in itertools.product(states, repeat=4):
        residual = tuple(item[0] for item in coordinates)
        window = tuple(item[1] for item in coordinates)
        deep_total = sum(
            (item[0] for item in coordinates if item[2] == "deep"),
            Fraction(0),
        )
        for budget in range(6):
            cases += 1
            lhs = best_n(residual, budget)
            rhs = best_n(window, budget) + deep_total
            if lhs > rhs:
                failures.append(
                    {
                        "coordinates": [
                            [fs(r), fs(f), depth] for r, f, depth in coordinates
                        ],
                        "budget": budget,
                        "left": fs(lhs),
                        "right": fs(rhs),
                    }
                )
                break
            for removed in powerset_indices(4, budget):
                same_set_checks += 1
                removed_set = set(removed)
                same_left = sum(
                    (
                        value
                        for index, value in enumerate(residual)
                        if index not in removed_set
                    ),
                    Fraction(0),
                )
                same_right = sum(
                    (
                        value
                        for index, value in enumerate(window)
                        if index not in removed_set
                    ),
                    Fraction(0),
                ) + deep_total
                if same_left > same_right:
                    failures.append(
                        {
                            "kind": "same_deletion_set",
                            "removed": list(removed),
                            "left": fs(same_left),
                            "right": fs(same_right),
                        }
                    )
                    break
            if failures:
                break
        if failures:
            break
    return assertion(
        "common_window_shallow_deep_split_exhaustive",
        not failures,
        "A common deletion set pays every shallow coordinate by its window majorant and every deep coordinate by one positive-depth debt.",
        cases=cases,
        same_set_checks=same_set_checks,
        failures=failures,
    )


def terminal_interval_fixtures() -> list[dict]:
    rows = []
    cases = (
        (Fraction(1), Fraction(0), Fraction(3, 4), Fraction(1, 4)),
        (Fraction(2), Fraction(-1), Fraction(1), Fraction(1)),
        (Fraction(7, 3), Fraction(1, 3), Fraction(8, 5), Fraction(3, 2)),
        (Fraction(7, 3), Fraction(1, 3), Fraction(3, 2), Fraction(3, 2)),
    )
    for index, (tau, start, delta, duration) in enumerate(cases, start=1):
        r_squared = Fraction(1)
        last_exit = tau - duration * r_squared
        window_left = max(start, tau - delta * r_squared)
        rows.append(
            assertion(
                f"terminal_interval_inclusion_{index}",
                duration <= delta and last_exit >= window_left,
                "For d<=delta, the last-exit interval lies in the common terminal window.",
                tau=fs(tau),
                start=fs(start),
                delta=fs(delta),
                duration=fs(duration),
                last_exit=fs(last_exit),
                window_left=fs(window_left),
            )
        )
    for numerator, denominator in ((1, 2), (1, 4), (3, 2)):
        root = Fraction(numerator, denominator)
        delta = root**3
        if not 0 < delta < 4:
            continue
        rows.append(
            exact(
                f"delta_inverse_two_thirds_{numerator}_{denominator}",
                Fraction(denominator, numerator) ** 2,
                Fraction(1, 1) / (root**2),
                "For a rational cube delta=a^3, delta^(-2/3)=a^(-2) exactly.",
            )
        )
    return rows


def no_winding_exact_checks() -> list[dict]:
    full_variation = Fraction(65, 32)
    terminal_window_variation = Fraction(4, 32)
    return [
        exact(
            "frozen_packet_full_variation",
            Fraction(65) * Fraction(1, 32),
            full_variation,
            "S.304: B times 65 R^2 is at most 65/32 after the R^2 factors cancel.",
        ),
        assertion(
            "frozen_packet_no_winding_rational_margin",
            full_variation < 3,
            "The exact stronger comparison 65/32<3, together with the standard pi>3, implies 65/32<2 pi without floating point.",
            left=fs(full_variation),
            rational_upper_bound=fs(Fraction(3)),
            rational_margin=fs(Fraction(3) - full_variation),
        ),
        exact(
            "frozen_packet_terminal_window_variation",
            Fraction(4) * Fraction(1, 32),
            terminal_window_variation,
            "S.304: the four-R^2 terminal window has variation at most 1/8.",
        ),
        exact(
            "frozen_packet_terminal_window_one_eighth",
            terminal_window_variation,
            Fraction(1, 8),
            "The terminal-window variation reduces exactly to 1/8.",
        ),
    ]


def synchronized_spike_checks() -> dict:
    rows = []
    failures = []
    for cube_root_m in (1, 2, 3):
        shell_count = cube_root_m**3
        budget = shell_count - 1
        previous_ratio = None
        for cube_root_h in (1, 2, 5, 11):
            height = Fraction(cube_root_h**3)
            epsilon = Fraction(1, 97)
            r_squared = Fraction(9, 4)
            amplitude = height / (epsilon * r_squared)
            one_integral = amplitude * epsilon * r_squared
            vector = (height,) * shell_count
            total = sum(vector, Fraction(0))
            tail = best_n(vector, budget)
            ratio = Fraction(cube_root_h, cube_root_m**2)
            cubed_ratio = tail**3 / total**2
            expected_cubed_ratio = ratio**3
            passed = (
                one_integral == height
                and total == shell_count * height
                and tail == height
                and cubed_ratio == expected_cubed_ratio
                and (previous_ratio is None or ratio > previous_ratio)
            )
            row = {
                "M": shell_count,
                "N": budget,
                "H": fs(height),
                "one_spike_integral": fs(one_integral),
                "total_variation": fs(total),
                "best_N_tail": fs(tail),
                "normalized_ratio": fs(ratio),
                "normalized_ratio_cubed": fs(cubed_ratio),
                "pass": passed,
            }
            rows.append(row)
            if not passed:
                failures.append(row)
            previous_ratio = ratio
    return assertion(
        "synchronized_spike_exact_ratios",
        not failures and rows[-1]["normalized_ratio"] == fs(Fraction(11, 9)),
        "S.281 is checked with cube-valued M and H, so every normalized P^(2/3) ratio remains rational and grows with H at fixed M.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def min_cap_two_regimes_exhaustive() -> dict:
    roots = (
        Fraction(1, 5),
        Fraction(1, 2),
        Fraction(1),
        Fraction(3, 2),
        Fraction(2),
        Fraction(5),
    )
    constants = (Fraction(1, 3), Fraction(1), Fraction(7, 2), Fraction(9))
    cases = 0
    failures = []
    regimes = {"P<=1": 0, "P>=1": 0}
    for root, c_zero, bound in itertools.product(roots, constants, constants):
        payment = root**3
        a_scale = root**2
        lhs = min(c_zero * payment, bound)
        rhs = max(c_zero, bound) * a_scale
        regime = "P<=1" if payment <= 1 else "P>=1"
        regimes[regime] += 1
        cases += 1
        if lhs > rhs:
            failures.append(
                {
                    "root": fs(root),
                    "P": fs(payment),
                    "A": fs(a_scale),
                    "C0": fs(c_zero),
                    "B": fs(bound),
                    "left": fs(lhs),
                    "right": fs(rhs),
                }
            )
    return assertion(
        "conditional_min_cap_P_small_P_large",
        not failures and all(regimes.values()),
        "S.294 is checked separately for P<=1 (P<=P^(2/3)) and P>=1 (1<=P^(2/3)).",
        cases=cases,
        regimes=regimes,
        failures=failures,
    )


def averaged_terminal_optimization_exponents() -> list[dict]:
    delta_power = Fraction(3, 5)
    eta_exponent = -1 + delta_power
    a_exponent = delta_power
    payment_exponent = 1 - delta_power
    substituted_payment_exponent = (
        Fraction(2, 3) * a_exponent + payment_exponent
    )
    return [
        exact(
            "averaged_balance_delta_power",
            Fraction(1, 1) / (1 + Fraction(2, 3)),
            delta_power,
            "Balancing delta P/eta with delta^(-2/3) A gives delta proportional to (eta A/P)^(3/5).",
        ),
        exact(
            "averaged_balance_eta_exponent",
            eta_exponent,
            Fraction(-2, 5),
            "The optimized exceptional-terminal factor is eta^(-2/5).",
        ),
        exact(
            "averaged_balance_A_exponent",
            a_exponent,
            Fraction(3, 5),
            "The optimized A exponent is 3/5.",
        ),
        exact(
            "averaged_balance_P_exponent_before_substitution",
            payment_exponent,
            Fraction(2, 5),
            "The remaining explicit payment exponent is 2/5.",
        ),
        exact(
            "averaged_balance_four_fifths_after_A_substitution",
            substituted_payment_exponent,
            Fraction(4, 5),
            "Substitution A=P^(2/3) gives the S.284 exponent 4/5.",
        ),
    ]


def exception_budget_union_exhaustive() -> dict:
    alphabet = (Fraction(0), Fraction(1), Fraction(2))
    vectors = tuple(itertools.product(alphabet, repeat=3))
    cases = 0
    failures = []
    for defect in vectors:
        for high_rayleigh in vectors:
            combined = tuple(a + b for a, b in zip(defect, high_rayleigh))
            for defect_budget in range(4):
                for high_budget in range(4):
                    lhs = best_n(combined, defect_budget + high_budget)
                    rhs = best_n(defect, defect_budget) + best_n(
                        high_rayleigh, high_budget
                    )
                    cases += 1
                    if lhs > rhs:
                        failures.append(
                            {
                                "defect": [fs(value) for value in defect],
                                "high_Rayleigh": [
                                    fs(value) for value in high_rayleigh
                                ],
                                "N_D": defect_budget,
                                "N_H": high_budget,
                                "left": fs(lhs),
                                "right": fs(rhs),
                            }
                        )
                        if len(failures) >= 8:
                            break
                if failures:
                    break
            if failures:
                break
        if failures:
            break
    return assertion(
        "exception_budget_union_exhaustive",
        not failures,
        "S.286 is checked exactly, including overlapping supports: defect and high-Rayleigh deletion budgets add.",
        cases=cases,
        failures=failures,
    )


def conditional_holder_exhaustive() -> dict:
    alphabet = (Fraction(0), Fraction(1), Fraction(2))
    cases = 0
    equality_cases = 0
    failures = []
    # Write p_k=y_k^3, so p_k^(2/3)=y_k^2 is rational.
    for coefficients in itertools.product(alphabet, repeat=3):
        for roots in itertools.product(alphabet, repeat=3):
            left = sum(
                (coefficient * root**2 for coefficient, root in zip(coefficients, roots)),
                Fraction(0),
            )
            coefficient_cube = sum(
                (coefficient**3 for coefficient in coefficients), Fraction(0)
            )
            payment = sum((root**3 for root in roots), Fraction(0))
            left_cube = left**3
            right_cube = coefficient_cube * payment**2
            cases += 1
            if left_cube == right_cube:
                equality_cases += 1
            if left_cube > right_cube:
                failures.append(
                    {
                        "c": [fs(value) for value in coefficients],
                        "p_cube_roots": [fs(value) for value in roots],
                        "left_cube": fs(left_cube),
                        "right_cube": fs(right_cube),
                    }
                )
                if len(failures) >= 8:
                    break
        if failures:
            break
    return assertion(
        "conditional_charging_Holder_exhaustive",
        not failures and equality_cases > 0,
        "The shellwise Holder row behind S.287 is checked after cubing, with p_k chosen as exact rational cubes.",
        cases=cases,
        equality_cases=equality_cases,
        failures=failures,
    )


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def moving_tube_cover_arithmetic() -> dict:
    lengths = (
        Fraction(0),
        Fraction(1, 7),
        Fraction(1),
        Fraction(5, 2),
        Fraction(8),
        Fraction(65),
        Fraction(511, 3),
    )
    cases = 0
    failures = []
    maximum_ratio = Fraction(0)
    for shell in range(1, 10):
        radial_scale = 2**shell
        balls_per_piece = 2 ** (3 * shell)
        for length in lengths:
            # Normalized greedy count: at most four time triggers, one initial
            # piece, and floor(L/2^k) arc-length triggers.
            pieces = 5 + floor_fraction(length / radial_scale)
            cylinder_count = pieces * balls_per_piece
            sharpened_row = (
                5 * 2 ** (3 * shell) + length * 2 ** (2 * shell)
            )
            advertised_form = 5 * (
                2 ** (3 * shell) + length * 2 ** (2 * shell)
            )
            ratio = Fraction(cylinder_count, 1) / (
                Fraction(2 ** (3 * shell), 1)
                + length * 2 ** (2 * shell)
            )
            maximum_ratio = max(maximum_ratio, ratio)
            cases += 1
            if not (
                cylinder_count <= sharpened_row <= advertised_form
                and pieces >= 1
            ):
                failures.append(
                    {
                        "k": shell,
                        "L": fs(length),
                        "pieces": pieces,
                        "cylinders": fs(Fraction(cylinder_count)),
                        "sharp_bound": fs(sharpened_row),
                        "advertised_bound": fs(advertised_form),
                    }
                )
    return assertion(
        "moving_tube_cover_count_arithmetic",
        not failures and maximum_ratio <= 5,
        "The normalized greedy count has the S.291 shape 2^(3k)+L 2^(2k), with one explicit harmless cover constant.",
        cases=cases,
        maximum_normalized_ratio=fs(maximum_ratio),
        failures=failures,
    )


def monotone_occupation_fixtures() -> dict:
    """Check S.305 after normalizing the torus circumference to one.

    For q(t)=v t, J=[0,a) mod 1, and total displacement D=m+r,
    the exact occupation in q-space is m a+min(r,a).  Dividing by v gives
    its time occupation.  The normalization multiplies D and |J| by the
    same 2*pi factor, so it does not change the asserted inequalities.
    """
    beta_values = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1))
    bounds = (Fraction(1), Fraction(5, 2), Fraction(7))
    arcs = (Fraction(1, 7), Fraction(1, 3), Fraction(3, 4), Fraction(1))
    remainders = (Fraction(0), Fraction(1, 9), Fraction(1, 2), Fraction(8, 9))
    cases = 0
    lower_equalities = 0
    upper_equalities = 0
    failures = []
    for beta, speed_bound, arc, remainder, windings in itertools.product(
        beta_values, bounds, arcs, remainders, range(5)
    ):
        for speed in (
            beta * speed_bound,
            (beta + 1) * speed_bound / 2,
            speed_bound,
        ):
            displacement = Fraction(windings) + remainder
            q_space_occupation = windings * arc + min(remainder, arc)
            occupation = q_space_occupation / speed
            lower = windings * arc / speed_bound
            upper = (windings + 1) * arc / (beta * speed_bound)
            passed = (
                beta * speed_bound <= speed <= speed_bound
                and lower <= occupation <= upper
                and windings == floor_fraction(displacement)
            )
            cases += 1
            lower_equalities += occupation == lower
            upper_equalities += occupation == upper
            if not passed:
                failures.append(
                    {
                        "beta": fs(beta),
                        "B": fs(speed_bound),
                        "speed": fs(speed),
                        "m": windings,
                        "remainder": fs(remainder),
                        "arc": fs(arc),
                        "occupation": fs(occupation),
                        "lower": fs(lower),
                        "upper": fs(upper),
                    }
                )
                if len(failures) >= 8:
                    break
        if failures:
            break
    return assertion(
        "monotone_periodic_occupation_exact_fixtures",
        not failures and lower_equalities > 0 and upper_equalities > 0,
        "S.305 is checked exactly for constant-speed paths after circumference normalization, with both endpoint inequalities attained.",
        cases=cases,
        lower_equalities=lower_equalities,
        upper_equalities=upper_equalities,
        failures=failures,
    )


def mixed_norm_exponent_cancellation() -> dict:
    # None denotes infinity, hence reciprocal exponent zero.
    exponent_pairs = (
        (3, 3),
        (4, 6),
        (6, 6),
        (None, 3),
        (12, 4),
    )
    rows = []
    failures = []
    for q_value, r_value in exponent_pairs:
        inv_q = Fraction(0) if q_value is None else Fraction(1, q_value)
        inv_r = Fraction(0) if r_value is None else Fraction(1, r_value)
        theta = 3 * inv_r + 2 * inv_q
        energy_exponent = 3 - 2 * theta + 2 * (theta - 1)
        cubic_exponent = 4 - 3 * theta + 3 * (theta - 1)
        pressure_exponent = (
            4 - 3 * theta + (2 * theta - 2) + (theta - 1)
        )
        path_exponent = -1 - 3 * inv_r + 2 - 2 * inv_q + theta - 1
        passed = (
            energy_exponent == 1
            and cubic_exponent == 1
            and pressure_exponent == 1
            and path_exponent == 0
        )
        row = {
            "q": "infinity" if q_value is None else str(q_value),
            "r": "infinity" if r_value is None else str(r_value),
            "theta": fs(theta),
            "energy_R_exponent": fs(energy_exponent),
            "cubic_R_exponent": fs(cubic_exponent),
            "pressure_R_exponent": fs(pressure_exponent),
            "path_R_exponent": fs(path_exponent),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return assertion(
        "mixed_norm_R_exponents_cancel_exactly",
        not failures,
        "S.297--S.299 scale exponents are checked as Fractions, including the allowed q=infinity endpoint and finite r.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def super_gaussian_tail_criterion() -> dict:
    """Certify an eventual geometric tail without evaluating exp numerically.

    For gamma_k=exp(-4^(k-1)/32) and w_k=2^(m k) gamma_k,
    w_(k+1)/w_k=2^m exp(-x_k), x_k=3*4^(k-1)/32.
    Since exp(x)>1+x for x>0, x_k>=2^(m+1)-1 implies ratio<1/2.
    """
    rows = []
    failures = []
    for power in range(6):
        threshold = Fraction(2 ** (power + 1) - 1)
        first_shell = None
        for shell in range(1, 32):
            exponent_increment = Fraction(3 * 4 ** (shell - 1), 32)
            if exponent_increment >= threshold:
                first_shell = shell
                break
        if first_shell is None:
            failures.append({"power": power, "reason": "search bound too small"})
            continue
        increment = Fraction(3 * 4 ** (first_shell - 1), 32)
        previous = (
            Fraction(3 * 4 ** (first_shell - 2), 32)
            if first_shell > 1
            else None
        )
        sufficient = increment >= threshold
        first_for_criterion = previous is None or previous < threshold
        geometric_tail_multiplier = Fraction(1, 1) / (1 - Fraction(1, 2))
        passed = sufficient and first_for_criterion and geometric_tail_multiplier == 2
        row = {
            "polynomial_power_m": power,
            "first_certified_shell": first_shell,
            "exponent_increment": fs(increment),
            "elementary_threshold": fs(threshold),
            "previous_increment": None if previous is None else fs(previous),
            "certified_ratio_bound": "strictly_less_than_1/2",
            "geometric_tail_multiplier": fs(geometric_tail_multiplier),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return assertion(
        "super_Gaussian_eventual_geometric_tail",
        not failures,
        "For polynomial weights 2^(mk), m=0,...,5, an exact elementary exp lower bound yields an eventual ratio below 1/2 and hence a two-term geometric tail cap.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def super_gaussian_best_n_filter() -> dict:
    """Check the exact rational form of the abstract S.306 filter."""
    gammas = (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4))
    heights = (Fraction(0), Fraction(1, 3), Fraction(2), Fraction(11, 2))
    cases = 0
    failures = []
    for gamma, power, height in itertools.product(gammas, range(5), heights):
        deletion_budget = None
        ratio_cap = None
        for candidate in range(9):
            candidate_ratio = Fraction(2**power) * gamma ** (
                3 * 4**candidate
            )
            if candidate_ratio < 1:
                deletion_budget = candidate
                ratio_cap = candidate_ratio
                break
        if deletion_budget is None or ratio_cap is None:
            failures.append(
                {
                    "Gamma": fs(gamma),
                    "p": power,
                    "H": fs(height),
                    "reason": "no q_N<1 in search range",
                }
            )
            continue
        majorants = tuple(
            height
            * Fraction(2 ** (power * shell))
            * gamma ** (4**shell)
            for shell in range(deletion_budget + 7)
        )
        tail = sum(majorants[deletion_budget:], Fraction(0))
        first = majorants[deletion_budget]
        geometric_cap = first / (1 - ratio_cap)
        adjacent_ok = all(
            majorants[shell + 1]
            == majorants[shell]
            * Fraction(2**power)
            * gamma ** (3 * 4**shell)
            and Fraction(2**power) * gamma ** (3 * 4**shell) <= ratio_cap
            for shell in range(deletion_budget, len(majorants) - 1)
        )
        finite_best_n = best_n(majorants, deletion_budget)
        passed = (
            ratio_cap < 1
            and adjacent_ok
            and finite_best_n <= tail <= geometric_cap
        )
        cases += 1
        if not passed:
            failures.append(
                {
                    "Gamma": fs(gamma),
                    "p": power,
                    "H": fs(height),
                    "N": deletion_budget,
                    "q_N": fs(ratio_cap),
                    "best_N": fs(finite_best_n),
                    "finite_tail": fs(tail),
                    "geometric_cap": fs(geometric_cap),
                    "adjacent_ok": adjacent_ok,
                }
            )
    return assertion(
        "abstract_super_Gaussian_best_N_filter",
        not failures,
        "S.306 is checked on exact rational Gamma,H,p fixtures: deletion of the first N terms, adjacent ratios, and the geometric cap all agree.",
        cases=cases,
        failures=failures,
    )


REQUIRED_COMPACT_SNIPPETS = {
    "common_terminal_window_definition": r"J_{\tau,\delta}&:=(\max\{s_R,\tau-\deltaR^2\},\tau)",
    "short_deep_reduction": r"\mathcalS_N(r^{\rmsh}(\tau))\le\mathcalV^F_{N,R}(\tau,\delta)+C_{\rmdeep}\delta^{-2/3}A_R",
    "best_N_Lipschitz": r"|\mathcalS_N(a)-\mathcalS_N(b)|&\le\|a-b\|_{\ell^1}",
    "layer_cake_identity": r"\mathcalS_N(z)=\int_0^\infty\bigl(n_z(t)-N\bigr)_+\,dt",
    "window_gate_open": r"\tag{S.280}",
    "synchronized_spike": r"\tag{S.281}",
    "four_fifths_boundary": r"(P_R^M)^{4/5}",
    "optimizer_inside_admissible_delta_range": r"\delta\asymp(\etaA_R/P_R^M)^{3/5}\)liesin\((0,4)\)",
    "exception_budgets_add": r"\mathcalS_{N_D+N_H}(d^{\rmdef}+h)\le\mathcalS_{N_D}(d^{\rmdef})+\mathcalS_{N_H}(h)",
    "ancestor_gate_open": r"\tag{S.288}",
    "moving_tube_cover": r"C_\psi\bigl(2^{3k}+L2^{2k}\bigr)",
    "conditional_min_cap": r"\mathcalS_0(x^{\rmsel}(\tau))\le\max\{C_0,B(M,L)\}A_R",
    "mixed_norm_definition": r"\mathcalU_{q,r}(R):=R^{1-\theta}\|u\|_{L_t^q(I_{8R};L_x^r(\mathbbT^3))}\leM_*",
    "path_exponent_zero": r"R^{-1-3/r+2-2/q+\theta-1}=CM_*",
    "combined_open_gate": r"\tag{S.303}",
    "no_winding_full_interval": r"\operatorname{Var}_{[0,65R^2]}Q\le{65\over32}<2\pi",
    "no_winding_terminal_window": r"\operatorname{Var}_{I_{2R}}Q\le{1\over8}",
    "occupation_lower_bound": r"{m|J|\overB}\le\tau_J",
    "occupation_upper_bound": r"\tau_J\le{(m+1)|J|\over\betaB}",
    "super_Gaussian_filter_hypothesis": r"q_N:=2^p\Gamma^{3\cdot4^N}<1",
    "super_Gaussian_filter_conclusion": r"\mathcalS_N(z)\le\sum_{\ell\geN}z_\ell\le{H2^{pN}\Gamma^{4^N}\over1-q_N}",
}

REQUIRED_LITERAL_SNIPPETS = {
    "not_clay": "**NOT CLAY.**",
    "common_window_continuity": "continuous common-window gate",
    "uniform_modulus_not_claimed": "The modulus in\n(S.277) depends on the solution and scale.",
    "conditional_benchmark": "conditional benchmark, not a theorem for the bare suitable-weak class",
    "abstract_not_NSE": "ABSTRACT BOUNDARY TESTS, NOT NSE COUNTEREXAMPLES",
    "super_Gaussian_boundary": "super-Gaussian",
    "kinematic_screen": "kinematic screen",
    "speed_not_missing_ingredient": "rule out speed alone as the missing\ningredient",
    "bounded_search_boundary": "The search is evidence against an immediate literature shortcut",
}

PRIMARY_LINKS = (
    "https://doi.org/10.1002/cpa.3160350604",
    "https://arxiv.org/abs/2301.09603",
    "https://arxiv.org/abs/math/0607534",
    "https://arxiv.org/abs/math/0607537",
    "https://arxiv.org/abs/2111.14776",
    "https://doi.org/10.3934/dcdss.2013.6.1391",
)


def semantic_contract(text: str, raw: bytes) -> list[dict]:
    compact_text = compact(text)
    rows = [
        assertion(
            identifier,
            compact(snippet) in compact_text,
            f"Required compact source marker: {snippet}",
        )
        for identifier, snippet in REQUIRED_COMPACT_SNIPPETS.items()
    ]
    rows.extend(
        assertion(
            identifier,
            snippet in text,
            f"Required literal source marker: {snippet}",
        )
        for identifier, snippet in REQUIRED_LITERAL_SNIPPETS.items()
    )
    rows.extend(
        assertion(
            f"primary_link_{index}",
            link in text,
            "Required primary-source link.",
            url=link,
        )
        for index, link in enumerate(PRIMARY_LINKS, start=1)
    )
    tags = [int(value) for value in re.findall(r"\\tag\{S\.(\d+)\}", text)]
    rows.extend(
        [
            assertion(
                "S273_final_tags_consecutive",
                tags == list(range(273, EXPECTED_LAST_TAG + 1)),
                "Step 12 equation tags are consecutive, ordered, and reach the frozen final tag.",
                tags=tags,
                expected_last=EXPECTED_LAST_TAG,
            ),
            assertion(
                "S273_final_tags_unique",
                len(tags) == len(set(tags)) == EXPECTED_LAST_TAG - 272,
                "Every frozen Step 12 equation tag occurs exactly once.",
            ),
            assertion(
                "three_universal_gates_remain_open",
                text.count(r"\textbf{OPEN") >= 3
                and "Both antecedents are open" in text,
                "S.280, S.288, and S.303 remain visibly open.",
            ),
            assertion(
                "conditional_not_bare_class",
                text.count("conditional") >= 5
                and "additional uniform hypotheses" in text,
                "Morrey and mixed-norm conclusions remain conditional.",
            ),
            assertion(
                "display_math_balanced",
                text.count(r"\[") == text.count(r"\]"),
                "Display-math delimiters balance.",
            ),
            assertion(
                "no_tabs_or_trailing_whitespace",
                b"\t" not in raw
                and not any(line.rstrip() != line for line in text.splitlines()),
                "Source has no tabs or trailing whitespace.",
            ),
            assertion(
                "no_forbidden_control_characters",
                not any(byte < 32 and byte not in (10,) for byte in raw),
                "Source has LF newlines and no embedded control characters.",
            ),
            assertion(
                "no_DNS_claim",
                "No DNS" in text and "No numerical simulation" not in text,
                "The analytic certificate is not presented as DNS.",
            ),
        ]
    )
    return rows


def negative_mutation_checks(text: str, raw: bytes) -> list[dict]:
    mutations = {
        "reject_layer_cake_missing_positive_part": (
            r"\bigl(n_z(t)-N\bigr)_+",
            r"\bigl(n_z(t)-N\bigr)",
            "layer_cake_identity",
        ),
        "reject_wrong_four_fifths_endpoint": (
            r"(P_R^M)^{4/5}",
            r"(P_R^M)^{2/3}",
            "four_fifths_boundary",
        ),
        "reject_max_to_min_cap": (
            r"\max\{C_0,B(M,L)\}",
            r"\min\{C_0,B(M,L)\}",
            "conditional_min_cap",
        ),
        "reject_budget_sum_to_max": (
            r"N_D+N_H",
            r"\max\{N_D,N_H\}",
            "exception_budgets_add",
        ),
        "reject_open_to_proved": (
            r"\textbf{OPEN",
            r"\textbf{PROVED",
            "three_universal_gates_remain_open",
        ),
        "reject_conditional_boundary_removal": (
            "conditional benchmark, not a theorem for the bare suitable-weak class",
            "theorem for the bare suitable-weak class",
            "conditional_benchmark",
        ),
        "reject_not_clay_removal": (
            "**NOT CLAY.**",
            "**CLAY.**",
            "not_clay",
        ),
        "reject_CKN_primary_link_removal": (
            PRIMARY_LINKS[0],
            "https://invalid.example/ckn",
            "primary_link_1",
        ),
        "reject_super_Gaussian_boundary_removal": (
            "super-Gaussian",
            "fast-decaying",
            "super_Gaussian_boundary",
        ),
        "reject_occupation_beta_denominator": (
            r"{(m+1)|J|\over\beta B}",
            r"{(m+1)|J|\over B}",
            "occupation_upper_bound",
        ),
        "reject_super_Gaussian_ratio_exponent": (
            r"\Gamma^{3\cdot4^N}",
            r"\Gamma^{2\cdot4^N}",
            "super_Gaussian_filter_hypothesis",
        ),
    }
    rows = []
    for identifier, (old, new, expected_failure) in mutations.items():
        mutated = text.replace(old, new)
        checks = {
            row["id"]: row["pass"]
            for row in semantic_contract(mutated, mutated.encode("utf-8"))
        }
        rows.append(
            assertion(
                identifier,
                mutated != text and not checks.get(expected_failure, True),
                f"Mutation must be rejected by {expected_failure}.",
            )
        )
    return rows


def structural_checks(text: str, raw: bytes) -> list[dict]:
    rows = [
        assertion(
            "locked_note_sha256",
            sha256(NOTE) == LOCKED_NOTE_SHA256,
            "The analyzed Step 12 note is byte-identical to the frozen source.",
            actual=sha256(NOTE),
            expected=LOCKED_NOTE_SHA256,
        )
    ]
    rows.extend(semantic_contract(text, raw))
    for label, (path, expected) in DEPENDENCIES.items():
        actual = sha256(path)
        rows.append(
            assertion(
                f"dependency_{label}",
                actual == expected,
                "Frozen dependency hash.",
                path=display_path(path),
                actual=actual,
                expected=expected,
            )
        )
    return rows


def build_payload() -> dict:
    raw = NOTE.read_bytes()
    text = raw.decode("utf-8")
    exact_checks = [
        *terminal_interval_fixtures(),
        *no_winding_exact_checks(),
        *averaged_terminal_optimization_exponents(),
    ]
    finite_checks = [
        layer_cake_exhaustive(),
        best_n_l1_lipschitz_exhaustive(),
        terminal_window_split_exhaustive(),
        synchronized_spike_checks(),
        min_cap_two_regimes_exhaustive(),
        exception_budget_union_exhaustive(),
        conditional_holder_exhaustive(),
        moving_tube_cover_arithmetic(),
        monotone_occupation_fixtures(),
        mixed_norm_exponent_cancellation(),
        super_gaussian_tail_criterion(),
        super_gaussian_best_n_filter(),
    ]
    structural = structural_checks(text, raw)
    negative = negative_mutation_checks(text, raw)
    all_rows = exact_checks + finite_checks + structural + negative
    return {
        "schema": SCHEMA,
        "source": {
            "path": display_path(NOTE),
            "sha256": sha256(NOTE),
            "locked_sha256": LOCKED_NOTE_SHA256,
            "expected_last_equation_tag": f"S.{EXPECTED_LAST_TAG}",
        },
        "scope": {
            "finite_exact_fraction_integer_and_statement_integrity_only": True,
            "uses_floating_point": False,
            "machine_proves_inherited_PDE_estimates": False,
            "machine_proves_uniform_terminal_window_gate_S280": False,
            "machine_proves_universal_ancestor_gate_S288": False,
            "machine_proves_combined_gate_S303_Q12_or_Q1": False,
            "machine_proves_Morrey_hypothesis_for_bare_suitable_weak_class": False,
            "machine_proves_regularity_or_Clay": False,
        },
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "negative_mutation_checks": negative,
        "summary": {
            "exact_passed": sum(row["pass"] for row in exact_checks),
            "exact_total": len(exact_checks),
            "finite_passed": sum(row["pass"] for row in finite_checks),
            "finite_total": len(finite_checks),
            "structural_passed": sum(row["pass"] for row in structural),
            "structural_total": len(structural),
            "negative_passed": sum(row["pass"] for row in negative),
            "negative_total": len(negative),
            "all_pass": all(row["pass"] for row in all_rows),
        },
    }


def render_report(payload: dict) -> str:
    summary = payload["summary"]
    lines = [
        "# R0.74S Step 12 — deterministic certificate report",
        "",
        f"- Schema: {payload['schema']}",
        f"- Source: {payload['source']['path']}",
        f"- Source SHA-256: {payload['source']['sha256']}",
        f"- Exact checks: {summary['exact_passed']}/{summary['exact_total']}",
        f"- Finite checks: {summary['finite_passed']}/{summary['finite_total']}",
        f"- Structural checks: {summary['structural_passed']}/{summary['structural_total']}",
        f"- Negative mutations rejected: {summary['negative_passed']}/{summary['negative_total']}",
        f"- Overall: {'PASS' if summary['all_pass'] else 'FAIL'}",
        "",
        "## Scope",
        "",
        "This certificate checks exact finite algebra, rational scaling",
        "bookkeeping, integer cover counts, an elementary super-Gaussian tail",
        "criterion, frozen hashes, primary links, and claim-boundary wording.",
        "It does not machine-prove the inherited PDE estimates, either universal",
        "packing gate, the conditional Morrey hypothesis for the bare class, Q.12,",
        "Q.1, regularity, or the Navier--Stokes Millennium problem.  **NOT CLAY.**",
        "",
        "## Check groups",
        "",
    ]
    for group in (
        "exact_checks",
        "finite_checks",
        "structural_checks",
        "negative_mutation_checks",
    ):
        lines.extend([f"### {group.replace('_', ' ').title()}", ""])
        for row in payload[group]:
            state = "PASS" if row["pass"] else "FAIL"
            lines.append(f"- **{state}** — {row['id']}: {row['note']}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    payload = build_payload()
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    REPORT_OUT.write_text(render_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], sort_keys=True))
    return 0 if payload["summary"]["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
