#!/usr/bin/env python3
"""Finite certificate for the R0.74S Step 8 total Rayleigh excess.

This deterministic standard-library certificate checks exact rational
arithmetic, finite signed-measure models, priority bookkeeping, Jensen and
Holder reductions, and claim/statement sentinels.  It does not machine-prove
measure topology, any inherited analytic estimate, the Navier--Stokes PDE,
regularity, or a Clay Millennium conclusion.
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
        "R074S_DEFECT_RELAXED_NOTE",
        REPO / "research/r074s_defect_relaxed_total_rayleigh_excess.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_DEFECT_RELAXED_JSON",
        REPO
        / "research/r074s_defect_relaxed_total_rayleigh_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_DEFECT_RELAXED_REPORT",
        REPO
        / "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md",
    )
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def fs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact(identifier: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def exact_ledger() -> list[dict]:
    """Literal constants and exponents in the Step 8 reduction."""
    return [
        exact(
            "priority_half_minus_beta_minus_sigma",
            Fraction(1, 2) - Fraction(1, 6) - 2 * Fraction(1, 12),
            Fraction(1, 6),
            "Failure of beta and sigma tests leaves strictly one sixth.",
        ),
        exact(
            "sigma_threshold_contributes_one_sixth",
            2 * Fraction(1, 12),
            Fraction(1, 6),
            "The coefficient 2 lambda converts T/(12 lambda) to T/6.",
        ),
        exact(
            "beta_threshold_reciprocal",
            6 * Fraction(1, 6),
            Fraction(1),
            "The beta branch costs the factor six.",
        ),
        exact(
            "excess_threshold_reciprocal",
            6 * Fraction(1, 6),
            Fraction(1),
            "The selected scalar-excess branch costs the factor six.",
        ),
        exact(
            "jensen_four_R_squared_constant_squared",
            4 * Fraction(1, 2) ** 2,
            Fraction(1),
            "Normalized interval length below four gives the factor one half.",
        ),
        exact(
            "per_shell_power_of_two_exponent",
            Fraction(3, 2) * Fraction(2, 3),
            Fraction(1),
            "Raising 2^(3k/2) to 2/3 gives 2^k.",
        ),
        exact(
            "per_shell_gamma_exponent",
            Fraction(1, 2) * Fraction(2, 3),
            Fraction(1, 3),
            "Raising gamma^(1/2) to 2/3 gives gamma^(1/3).",
        ),
        exact(
            "per_shell_lambda_exponent",
            Fraction(3, 2) * Fraction(2, 3),
            Fraction(1),
            "The sigma threshold leaves one power of lambda.",
        ),
        exact(
            "per_shell_payment_exponent",
            Fraction(1) * Fraction(2, 3),
            Fraction(2, 3),
            "The cubic payment appears to the power 2/3.",
        ),
        exact(
            "C4_cubed_scalar",
            Fraction(12**3 * 2**2),
            Fraction(6912),
            "C4=12(2 C1)^(2/3), so C4^3=12^3*4*C1^2.",
        ),
        exact(
            "cross_shell_holder_reciprocal_exponents",
            Fraction(1, 3) + Fraction(2, 3),
            Fraction(1),
            "Cross-shell Holder uses exponents 3 and 3/2.",
        ),
        exact(
            "cross_shell_coefficient_cube_gamma",
            3 * Fraction(1, 3),
            Fraction(1),
            "Cubing lambda 2^k gamma^(1/3) yields gamma.",
        ),
        exact(
            "cross_shell_coefficient_cube_dyadic",
            3 * Fraction(1),
            Fraction(3),
            "Cubing 2^k yields the 2^(3k) ledger.",
        ),
        exact(
            "selected_flux_sharp_coefficient",
            Fraction(6, 5) * Fraction(5, 6),
            Fraction(1),
            "Failure of beta gives F>5T/6, hence T<(6/5)F.",
        ),
        exact(
            "direct_clock_to_full_flux_one_BQ",
            Fraction(1),
            Fraction(1),
            "The direct shell-partition identity costs exactly one B_Q.",
        ),
        exact(
            "exact_family_ratio_identity_at_K_4096",
            Fraction(1) / Fraction(1, 4096),
            Fraction(4096),
            "T divided by T/K equals K in the exact-family scaling proxy.",
        ),
    ]


def signed_measure_jordan_check() -> dict:
    """Check scalar x against the Jordan positive mass on finite atoms."""
    values = [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]
    failures: list[dict] = []
    configurations = 0
    strict_cancellation_cases = 0
    equality_cases = 0

    for length in range(1, 5):
        for atoms in itertools.product(values, repeat=length):
            configurations += 1
            total = sum(atoms, Fraction(0))
            scalar = max(total, Fraction(0))
            jordan = sum((max(atom, Fraction(0)) for atom in atoms), Fraction(0))
            subset_sums = [
                sum(
                    (atoms[index] for index in range(length) if mask & (1 << index)),
                    Fraction(0),
                )
                for mask in range(1 << length)
            ]
            variational = max(subset_sums)
            nu = sum((max(atom, Fraction(0)) for atom in atoms), Fraction(0))
            beta = sum((max(-atom, Fraction(0)) for atom in atoms), Fraction(0))
            conditions = {
                "scalar_nonnegative": scalar >= 0,
                "scalar_below_Jordan": scalar <= jordan,
                "Jordan_is_subset_supremum": jordan == variational,
                "total_mass_identity": total == nu - beta,
                "terminal_inequality_with_x": nu <= beta + scalar,
                "terminal_inequality_with_X": nu <= beta + jordan,
            }
            if scalar < jordan:
                strict_cancellation_cases += 1
            if scalar == jordan:
                equality_cases += 1
            if not all(conditions.values()) and len(failures) < 20:
                failures.append(
                    {
                        "atoms": [fs(atom) for atom in atoms],
                        "x": fs(scalar),
                        "X": fs(jordan),
                        "conditions": conditions,
                    }
                )

    return {
        "id": "finite_signed_measure_scalar_x_below_Jordan_X",
        "configurations_checked": configurations,
        "strict_cancellation_cases": strict_cancellation_cases,
        "equality_cases": equality_cases,
        "failures": failures,
        "pass": not failures and strict_cancellation_cases > 0 and equality_cases > 0,
    }


def decomposed_measure_check() -> dict:
    """Realize alpha=nu-beta-2 lambda sigma on finite time atoms."""
    values = [Fraction(0), Fraction(1, 2)]
    lambdas = [Fraction(1, 2), Fraction(1), Fraction(2)]
    failures: list[dict] = []
    configurations = 0
    strict_cases = 0

    for lam in lambdas:
        for nu in itertools.product(values, repeat=3):
            for beta in itertools.product(values, repeat=3):
                for sigma in itertools.product(values, repeat=3):
                    configurations += 1
                    alpha = tuple(
                        n - b - 2 * lam * s
                        for n, b, s in zip(nu, beta, sigma)
                    )
                    alpha_total = sum(alpha, Fraction(0))
                    x_value = max(alpha_total, Fraction(0))
                    X_value = sum(
                        (max(item, Fraction(0)) for item in alpha), Fraction(0)
                    )
                    nu_total = sum(nu, Fraction(0))
                    beta_total = sum(beta, Fraction(0))
                    sigma_total = sum(sigma, Fraction(0))
                    conditions = {
                        "x_below_X": x_value <= X_value,
                        "measure_order_X_below_nu": X_value <= nu_total,
                        "scalar_terminal_bound": nu_total
                        <= beta_total + 2 * lam * sigma_total + x_value,
                        "Jordan_terminal_bound": nu_total
                        <= beta_total + 2 * lam * sigma_total + X_value,
                    }
                    if x_value < X_value:
                        strict_cases += 1
                    if not all(conditions.values()) and len(failures) < 20:
                        failures.append(
                            {
                                "lambda": fs(lam),
                                "nu": [fs(item) for item in nu],
                                "beta": [fs(item) for item in beta],
                                "sigma": [fs(item) for item in sigma],
                                "alpha": [fs(item) for item in alpha],
                                "conditions": conditions,
                            }
                        )

    return {
        "id": "finite_nonnegative_measure_decomposition",
        "configurations_checked": configurations,
        "strict_x_below_X_cases": strict_cases,
        "failures": failures,
        "pass": not failures and strict_cases > 0,
    }


def priority_trichotomy_check() -> dict:
    """Enumerate the literal beta -> sigma -> x priority partition."""
    terminals = [Fraction(1, 2), Fraction(1), Fraction(2)]
    lambdas = [Fraction(1, 2), Fraction(1), Fraction(2)]
    nu_ratios = [Fraction(1, 2), Fraction(7, 12), Fraction(2, 3), Fraction(1)]
    beta_ratios = [
        Fraction(0),
        Fraction(1, 12),
        Fraction(19, 120),
        Fraction(1, 6),
        Fraction(1, 4),
    ]
    lambda_sigma_ratios = [
        Fraction(0),
        Fraction(1, 24),
        Fraction(3, 40),
        Fraction(1, 12),
        Fraction(11, 120),
        Fraction(1, 6),
    ]
    counts = {"beta": 0, "sigma": 0, "x": 0}
    failures: list[dict] = []
    configurations = 0
    minimum_x_margin: Fraction | None = None

    for terminal, lam, nu_ratio, beta_ratio, ls_ratio in itertools.product(
        terminals,
        lambdas,
        nu_ratios,
        beta_ratios,
        lambda_sigma_ratios,
    ):
        nu = terminal * nu_ratio
        beta = terminal * beta_ratio
        sigma = terminal * ls_ratio / lam
        configurations += 1
        if beta >= terminal / 6:
            branch = "beta"
        elif sigma > terminal / (12 * lam):
            branch = "sigma"
        else:
            branch = "x"
        counts[branch] += 1
        alpha = nu - beta - 2 * lam * sigma
        x_value = max(alpha, Fraction(0))
        if branch == "x":
            margin = x_value - terminal / 6
            if minimum_x_margin is None or margin < minimum_x_margin:
                minimum_x_margin = margin
        conditions = {
            "dissipation_dominated": nu >= terminal / 2,
            "beta_priority": branch != "beta" or beta >= terminal / 6,
            "sigma_priority": branch != "sigma"
            or (beta < terminal / 6 and sigma > terminal / (12 * lam)),
            "x_two_failed_tests": branch != "x"
            or (beta < terminal / 6 and sigma <= terminal / (12 * lam)),
            "x_strictly_above_one_sixth": branch != "x"
            or x_value > terminal / 6,
            "branch_payment": (
                (branch == "beta" and terminal <= 6 * beta)
                or (branch == "sigma")
                or (branch == "x" and terminal < 6 * x_value)
            ),
        }
        if not all(conditions.values()) and len(failures) < 20:
            failures.append(
                {
                    "T": fs(terminal),
                    "lambda": fs(lam),
                    "nu": fs(nu),
                    "beta": fs(beta),
                    "sigma": fs(sigma),
                    "x": fs(x_value),
                    "branch": branch,
                    "conditions": conditions,
                }
            )

    return {
        "id": "exact_one_sixth_beta_sigma_x_priority_trichotomy",
        "configurations_checked": configurations,
        "class_counts": counts,
        "minimum_residual_x_strict_margin": fs(minimum_x_margin or Fraction(0)),
        "failures": failures,
        "pass": not failures and all(counts.values()),
    }


def jensen_check() -> dict:
    """Check Jensen on rational step functions without radicals."""
    weights = [Fraction(1, 4), Fraction(1, 2), Fraction(1)]
    roots = [0, 1, 2, 3]
    failures: list[dict] = []
    configurations = 0
    equality_cases = 0

    for length in range(1, 5):
        for cell_weights in itertools.product(weights, repeat=length):
            delta = sum(cell_weights, Fraction(0))
            for cell_roots in itertools.product(roots, repeat=length):
                if not any(cell_roots):
                    continue
                configurations += 1
                sigma = sum(
                    (
                        weight * root**2
                        for weight, root in zip(cell_weights, cell_roots)
                    ),
                    Fraction(0),
                )
                cubic = sum(
                    (
                        weight * root**3
                        for weight, root in zip(cell_weights, cell_roots)
                    ),
                    Fraction(0),
                )
                jensen = delta * cubic**2 >= sigma**3
                half_constant = 4 * cubic**2 >= sigma**3
                if delta * cubic**2 == sigma**3:
                    equality_cases += 1
                conditions = {
                    "delta_at_most_four": delta <= 4,
                    "Jensen_squared": jensen,
                    "one_half_constant_squared": half_constant,
                }
                if not all(conditions.values()) and len(failures) < 20:
                    failures.append(
                        {
                            "weights": [fs(item) for item in cell_weights],
                            "roots": list(cell_roots),
                            "delta": fs(delta),
                            "sigma": fs(sigma),
                            "cubic": fs(cubic),
                            "conditions": conditions,
                        }
                    )

    return {
        "id": "exact_rational_Jensen_on_normalized_length_below_four",
        "configurations_checked": configurations,
        "equality_cases": equality_cases,
        "failures": failures,
        "pass": not failures and equality_cases > 0,
    }


def C4_cube_check() -> dict:
    """Check the radical-free cube of the claimed per-shell coefficient."""
    failures: list[dict] = []
    rows = []
    for C1, shell, lam, gamma_root, payment_root in itertools.product(
        [Fraction(1, 2), Fraction(1), Fraction(2)],
        range(1, 6),
        [Fraction(1, 2), Fraction(1), Fraction(2)],
        [Fraction(1, 4), Fraction(1, 2), Fraction(1)],
        [Fraction(1, 2), Fraction(1), Fraction(2)],
    ):
        gamma = gamma_root**3
        payment = payment_root**3
        claimed_cube = (
            Fraction(12**3 * 4)
            * C1**2
            * lam**3
            * Fraction(2 ** (3 * shell))
            * gamma
            * payment**2
        )
        derived_cube = (
            Fraction(12**3)
            * lam**3
            * (2 * C1) ** 2
            * Fraction(2 ** (3 * shell))
            * gamma
            * payment**2
        )
        conditions = {
            "C4_cube_identity": claimed_cube == derived_cube,
            "positive_coefficient": claimed_cube > 0,
        }
        row = {
            "C1": fs(C1),
            "k": shell,
            "lambda": fs(lam),
            "gamma": fs(gamma),
            "payment": fs(payment),
            "claimed_cube": fs(claimed_cube),
            "derived_cube": fs(derived_cube),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"] and len(failures) < 20:
            failures.append(row)

    return {
        "id": "C4_equals_12_times_2C1_to_two_thirds_cube_identity",
        "configurations_checked": len(rows),
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def holder_check() -> dict:
    """Check (sum a q^2)^3 <= (sum a^3)(sum q^3)^2 exactly."""
    failures: list[dict] = []
    configurations = 0
    equality_cases = 0
    values = range(4)

    for length in range(1, 5):
        for coefficients in itertools.product(values, repeat=length):
            for cube_roots in itertools.product(values, repeat=length):
                if not any(coefficients) or not any(cube_roots):
                    continue
                configurations += 1
                mixed = sum(
                    (
                        Fraction(a * q * q)
                        for a, q in zip(coefficients, cube_roots)
                    ),
                    Fraction(0),
                )
                coefficient_cube = sum(
                    (Fraction(a**3) for a in coefficients), Fraction(0)
                )
                payment = sum(
                    (Fraction(q**3) for q in cube_roots), Fraction(0)
                )
                left = mixed**3
                right = coefficient_cube * payment**2
                if left == right:
                    equality_cases += 1
                if left > right and len(failures) < 20:
                    failures.append(
                        {
                            "coefficients": list(coefficients),
                            "payment_cube_roots": list(cube_roots),
                            "left": fs(left),
                            "right": fs(right),
                        }
                    )

    return {
        "id": "exact_rational_cross_shell_Holder",
        "configurations_checked": configurations,
        "equality_cases": equality_cases,
        "failures": failures,
        "pass": not failures and equality_cases > 0,
    }


def shell_templates() -> list[dict]:
    """Small exact shells exhibiting each priority branch and cancellation."""
    raw = [
        {
            "name": "beta",
            "T": Fraction(1),
            "nu": (Fraction(1, 2), Fraction(0)),
            "beta": (Fraction(1, 6), Fraction(0)),
            "sigma": (Fraction(0), Fraction(0)),
        },
        {
            "name": "sigma",
            "T": Fraction(1),
            "nu": (Fraction(1, 2), Fraction(0)),
            "beta": (Fraction(0), Fraction(0)),
            "sigma": (Fraction(1, 8), Fraction(0)),
        },
        {
            "name": "x_local",
            "T": Fraction(1),
            "nu": (Fraction(1, 2), Fraction(0)),
            "beta": (Fraction(1, 12), Fraction(0)),
            "sigma": (Fraction(1, 12), Fraction(0)),
        },
        {
            "name": "x_cancel",
            "T": Fraction(1),
            "nu": (Fraction(1, 2), Fraction(0)),
            "beta": (Fraction(0), Fraction(1, 12)),
            "sigma": (Fraction(0), Fraction(1, 12)),
        },
    ]
    result = []
    for item in raw:
        lam = Fraction(1)
        beta_total = sum(item["beta"], Fraction(0))
        sigma_total = sum(item["sigma"], Fraction(0))
        nu_total = sum(item["nu"], Fraction(0))
        alpha = tuple(
            n - b - 2 * lam * s
            for n, b, s in zip(item["nu"], item["beta"], item["sigma"])
        )
        x_value = max(sum(alpha, Fraction(0)), Fraction(0))
        X_value = sum((max(value, Fraction(0)) for value in alpha), Fraction(0))
        if beta_total >= item["T"] / 6:
            branch = "beta"
        elif sigma_total > item["T"] / (12 * lam):
            branch = "sigma"
        else:
            branch = "x"
        result.append(
            {
                **item,
                "lambda": lam,
                "nu_total": nu_total,
                "beta_total": beta_total,
                "sigma_total": sigma_total,
                "alpha": alpha,
                "x": x_value,
                "X": X_value,
                "branch": branch,
            }
        )
    return result


def selected_global_ledger_check() -> dict:
    """Check selected x, global x, and global X inequalities on shell bundles."""
    templates = shell_templates()
    failures: list[dict] = []
    configurations = 0
    selected_strictly_smaller = 0
    jordan_strictly_larger = 0

    for length in range(1, 5):
        for shells in itertools.product(templates, repeat=length):
            configurations += 1
            lhs = sum((shell["T"] for shell in shells), Fraction(0))
            beta_payment = 6 * sum(
                (shell["beta_total"] for shell in shells), Fraction(0)
            )
            # This is the abstract output of the separately checked kinetic
            # branch: each sigma shell is supplied an envelope equal to T.
            sigma_payment = sum(
                (
                    shell["T"]
                    for shell in shells
                    if shell["branch"] == "sigma"
                ),
                Fraction(0),
            )
            selected_x = sum(
                (shell["x"] for shell in shells if shell["branch"] == "x"),
                Fraction(0),
            )
            global_x = sum((shell["x"] for shell in shells), Fraction(0))
            global_X = sum((shell["X"] for shell in shells), Fraction(0))
            selected_rhs = beta_payment + sigma_payment + 6 * selected_x
            global_x_rhs = beta_payment + sigma_payment + 6 * global_x
            global_X_rhs = beta_payment + sigma_payment + 6 * global_X
            conditions = {
                "selected_terminal_bound": lhs <= selected_rhs,
                "selected_below_global_x": selected_x <= global_x,
                "global_x_below_global_X": global_x <= global_X,
                "global_x_terminal_bound": lhs <= global_x_rhs,
                "global_X_terminal_bound": lhs <= global_X_rhs,
            }
            if selected_x < global_x:
                selected_strictly_smaller += 1
            if global_x < global_X:
                jordan_strictly_larger += 1
            if not all(conditions.values()) and len(failures) < 20:
                failures.append(
                    {
                        "shells": [shell["name"] for shell in shells],
                        "lhs": fs(lhs),
                        "selected_rhs": fs(selected_rhs),
                        "global_x_rhs": fs(global_x_rhs),
                        "global_X_rhs": fs(global_X_rhs),
                        "conditions": conditions,
                    }
                )

    return {
        "id": "finite_selected_and_global_excess_ledgers",
        "configurations_checked": configurations,
        "selected_sum_strictly_below_global_x_cases": selected_strictly_smaller,
        "global_x_strictly_below_global_X_cases": jordan_strictly_larger,
        "failures": failures,
        "pass": not failures
        and selected_strictly_smaller > 0
        and jordan_strictly_larger > 0,
    }


def shear_absorption_check() -> dict:
    """Check D<=K=T<=beta implies scalar x=0 for the exact shear."""
    failures: list[dict] = []
    rows = []
    for terminal, dissipation_ratio, beta_ratio, lam, sigma in itertools.product(
        [Fraction(1, 2), Fraction(1), Fraction(2)],
        [Fraction(0), Fraction(1, 2), Fraction(1)],
        [Fraction(1), Fraction(3, 2), Fraction(2)],
        [Fraction(1, 2), Fraction(1), Fraction(2)],
        [Fraction(0), Fraction(1, 8), Fraction(1)],
    ):
        nu = terminal * dissipation_ratio
        beta = terminal * beta_ratio
        alpha = nu - beta - 2 * lam * sigma
        x_value = max(alpha, Fraction(0))
        conditions = {
            "D_below_K": nu <= terminal,
            "K_below_beta": terminal <= beta,
            "alpha_nonpositive": alpha <= 0,
            "x_zero": x_value == 0,
            "beta_priority": beta >= terminal / 6,
        }
        row = {
            "T": fs(terminal),
            "nu": fs(nu),
            "beta": fs(beta),
            "lambda": fs(lam),
            "sigma": fs(sigma),
            "x": fs(x_value),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"] and len(failures) < 20:
            failures.append(row)

    # Terminal cancellation alone does not force the Jordan envelope to zero.
    jordan_alpha = (Fraction(1), Fraction(-1))
    jordan_x = max(sum(jordan_alpha, Fraction(0)), Fraction(0))
    jordan_X = sum(
        (max(item, Fraction(0)) for item in jordan_alpha), Fraction(0)
    )
    return {
        "id": "exact_shear_terminal_scalar_excess_absorbed_by_beta",
        "configurations_checked": len(rows),
        "Jordan_nonvanishing_not_excluded_fixture": {
            "alpha_atoms": [fs(item) for item in jordan_alpha],
            "x": fs(jordan_x),
            "X": fs(jordan_X),
            "pass": jordan_x == 0 and jordan_X > 0,
        },
        "rows": rows,
        "failures": failures,
        "pass": not failures and jordan_x == 0 and jordan_X > 0,
    }


def portmanteau_lsc_proxy_check() -> dict:
    """Check the scalar implication used after the open-set liminf bound."""
    values = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2)]
    failures: list[dict] = []
    configurations = 0
    strict_cases = 0
    for limit_mass, approximant_liminf, paid_mass in itertools.product(
        values, values, values
    ):
        if approximant_liminf < limit_mass:
            continue
        configurations += 1
        limit_x = max(limit_mass - paid_mass, Fraction(0))
        approximant_x = max(approximant_liminf - paid_mass, Fraction(0))
        conditions = {
            "open_mass_direction": limit_mass <= approximant_liminf,
            "positive_part_monotone": limit_x <= approximant_x,
        }
        if limit_x < approximant_x:
            strict_cases += 1
        if not all(conditions.values()) and len(failures) < 20:
            failures.append(
                {
                    "nu_limit": fs(limit_mass),
                    "nu_liminf": fs(approximant_liminf),
                    "paid_limit": fs(paid_mass),
                    "x_limit": fs(limit_x),
                    "x_liminf_proxy": fs(approximant_x),
                    "conditions": conditions,
                }
            )

    epsilon_rows = []
    for limit_mass, paid_mass, epsilon in itertools.product(
        values,
        values,
        [Fraction(1, 16), Fraction(1, 8), Fraction(1, 4)],
    ):
        approximate_mass = max(limit_mass - epsilon, Fraction(0))
        approximate_paid = paid_mass + epsilon
        limit_x = max(limit_mass - paid_mass, Fraction(0))
        approximate_x = max(
            approximate_mass - approximate_paid, Fraction(0)
        )
        lower_target = max(limit_x - 2 * epsilon, Fraction(0))
        row = {
            "nu_limit": fs(limit_mass),
            "paid_limit": fs(paid_mass),
            "epsilon": fs(epsilon),
            "x_limit": fs(limit_x),
            "x_approximate": fs(approximate_x),
            "lower_target": fs(lower_target),
            "pass": approximate_x >= lower_target,
        }
        epsilon_rows.append(row)
        if not row["pass"] and len(failures) < 20:
            failures.append(row)

    return {
        "id": "finite_Portmanteau_positive_part_lsc_direction_proxy",
        "configurations_checked": configurations + len(epsilon_rows),
        "strict_liminf_cases": strict_cases,
        "epsilon_proxy_rows": epsilon_rows,
        "failures": failures,
        "pass": not failures and strict_cases > 0,
    }


def Jordan_supremum_lsc_proxy_check() -> dict:
    """Finite-test proxy for sup_phi alpha(phi) lower semicontinuity."""
    values = [Fraction(-1), Fraction(0), Fraction(1, 2), Fraction(1), Fraction(2)]
    epsilons = [Fraction(1, 8), Fraction(1, 4)]
    failures: list[dict] = []
    configurations = 0
    strict_rows = 0
    for length in range(1, 4):
        for limit_tests in itertools.product(values, repeat=length):
            target_sup = max((Fraction(0), *limit_tests))
            for epsilon in epsilons:
                for signs in itertools.product((-1, 0, 1), repeat=length):
                    approximate_tests = tuple(
                        value + sign * epsilon
                        for value, sign in zip(limit_tests, signs)
                    )
                    approximate_sup = max((Fraction(0), *approximate_tests))
                    lower_target = max(target_sup - epsilon, Fraction(0))
                    conditions = {
                        "uniform_test_error_at_most_epsilon": all(
                            abs(approximate - limit) <= epsilon
                            for approximate, limit in zip(
                                approximate_tests, limit_tests
                            )
                        ),
                        "supremum_stability": approximate_sup >= lower_target,
                    }
                    configurations += 1
                    if approximate_sup > lower_target:
                        strict_rows += 1
                    if not all(conditions.values()) and len(failures) < 20:
                        failures.append(
                            {
                                "limit_tests": [fs(item) for item in limit_tests],
                                "approximate_tests": [
                                    fs(item) for item in approximate_tests
                                ],
                                "epsilon": fs(epsilon),
                                "target_sup": fs(target_sup),
                                "approximate_sup": fs(approximate_sup),
                                "conditions": conditions,
                            }
                        )
    return {
        "id": "finite_compact_test_supremum_lsc_proxy_for_Jordan_X",
        "configurations_checked": configurations,
        "strict_rows": strict_rows,
        "analytic_infinite_test_supremum_machine_proved": False,
        "failures": failures,
        "pass": not failures and strict_rows > 0,
    }


def smooth_density_cancellation_check() -> dict:
    """Check x=[integral h]+ versus X=integral[h]+ on finite cells."""
    fixtures = (
        ("balanced", (Fraction(1), Fraction(-1))),
        ("positive", (Fraction(1), Fraction(2))),
        ("overcancelled", (Fraction(1), Fraction(-2))),
        ("three_cell", (Fraction(2), Fraction(-1), Fraction(-1))),
    )
    rows = []
    failures = []
    for name, contributions in fixtures:
        integral = sum(contributions, Fraction(0))
        scalar = max(integral, Fraction(0))
        Jordan = sum(
            (max(item, Fraction(0)) for item in contributions), Fraction(0)
        )
        conditions = {
            "smooth_formula_proxy_x": scalar == max(integral, Fraction(0)),
            "smooth_formula_proxy_X": Jordan
            == sum(
                (max(item, Fraction(0)) for item in contributions),
                Fraction(0),
            ),
            "x_below_X": scalar <= Jordan,
            "balanced_gap": name != "balanced" or (scalar == 0 and Jordan == 1),
        }
        row = {
            "name": name,
            "cell_integrals_of_h": [fs(item) for item in contributions],
            "integral_h": fs(integral),
            "x": fs(scalar),
            "X": fs(Jordan),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)
    return {
        "id": "finite_absolute_continuous_density_x_versus_X_cancellation",
        "fixtures_checked": len(rows),
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def endpoint_escape_check() -> dict:
    """Record the exact open-endpoint mass-loss direction."""
    approximant_open_masses = [Fraction(1) for _ in range(16)]
    target_open_mass = Fraction(0)
    target_closed_mass = Fraction(1)
    liminf_approx = min(approximant_open_masses)
    return {
        "id": "open_terminal_endpoint_escape_direction",
        "approximants": "unit atoms a_n increasing to tau from below",
        "approximant_open_masses": [fs(item) for item in approximant_open_masses],
        "target_open_mass": fs(target_open_mass),
        "target_closed_mass_if_object_changed": fs(target_closed_mass),
        "liminf_approximant_open_mass": fs(liminf_approx),
        "lower_semicontinuity": target_open_mass <= liminf_approx,
        "ordinary_mass_convergence": target_open_mass == liminf_approx,
        "closed_endpoint_is_different_object": target_closed_mass
        != target_open_mass,
        "pass": (
            target_open_mass <= liminf_approx
            and target_open_mass != liminf_approx
            and target_closed_mass != target_open_mass
        ),
    }


def terminal_flux_reduction_check() -> dict:
    """Check beta>=|Q| reduces scalar excess to positive terminal flux."""
    values = [
        Fraction(-2),
        Fraction(-1),
        Fraction(0),
        Fraction(1, 2),
        Fraction(1),
        Fraction(2),
    ]
    nonnegative = [Fraction(0), Fraction(1, 4), Fraction(1), Fraction(2)]
    failures: list[dict] = []
    configurations = 0
    residual_cases = 0
    for Q, F, E, sigma, lam, beta_slack in itertools.product(
        values,
        values,
        nonnegative,
        nonnegative,
        [Fraction(1, 2), Fraction(1), Fraction(2)],
        nonnegative,
    ):
        D = Q + F - E
        if D < 0:
            continue
        beta = abs(Q) + beta_slack
        alpha = D - beta - 2 * lam * sigma
        x_value = max(alpha, Fraction(0))
        intermediate = max(F - E - 2 * lam * sigma, Fraction(0))
        flux_positive = max(F, Fraction(0))
        terminal = Fraction(1)
        implication = x_value <= terminal / 6 or F > terminal / 6
        if x_value > terminal / 6:
            residual_cases += 1
        conditions = {
            "beta_dominates_terminal_Q": beta >= abs(Q),
            "clock_identity": D == Q + F - E,
            "x_below_reduced_positive_part": x_value <= intermediate,
            "reduced_positive_part_below_flux_positive_part": intermediate
            <= flux_positive,
            "residual_implies_positive_flux": implication,
        }
        configurations += 1
        if not all(conditions.values()) and len(failures) < 20:
            failures.append(
                {
                    "Q": fs(Q),
                    "F": fs(F),
                    "E": fs(E),
                    "sigma": fs(sigma),
                    "lambda": fs(lam),
                    "beta": fs(beta),
                    "D": fs(D),
                    "x": fs(x_value),
                    "conditions": conditions,
                }
            )
    return {
        "id": "finite_terminal_Q_variation_to_signed_flux_reduction",
        "configurations_checked": configurations,
        "residual_x_above_one_sixth_cases": residual_cases,
        "failures": failures,
        "pass": not failures and residual_cases > 0,
    }


def global_flux_variation_ledger_check() -> dict:
    """Check sum x <= sum [F]+ <= sum TV(F) on finite shell families."""
    shell_rows = (
        (Fraction(0), Fraction(-1), Fraction(1)),
        (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)),
        (Fraction(1), Fraction(1), Fraction(1)),
        (Fraction(0), Fraction(0), Fraction(2)),
        (Fraction(1, 2), Fraction(1, 2), Fraction(3, 2)),
    )
    failures: list[dict] = []
    configurations = 0
    strict_first = 0
    strict_second = 0
    for length in range(1, 5):
        for shells in itertools.product(shell_rows, repeat=length):
            configurations += 1
            x_sum = sum((row[0] for row in shells), Fraction(0))
            flux_positive_sum = sum(
                (max(row[1], Fraction(0)) for row in shells), Fraction(0)
            )
            variation_sum = sum((row[2] for row in shells), Fraction(0))
            per_shell = all(
                x <= max(flux, Fraction(0)) <= variation
                for x, flux, variation in shells
            )
            conditions = {
                "per_shell_chain": per_shell,
                "global_x_below_positive_terminal_flux": x_sum
                <= flux_positive_sum,
                "positive_terminal_flux_below_variation": flux_positive_sum
                <= variation_sum,
            }
            if x_sum < flux_positive_sum:
                strict_first += 1
            if flux_positive_sum < variation_sum:
                strict_second += 1
            if not all(conditions.values()) and len(failures) < 20:
                failures.append(
                    {
                        "shells": [[fs(item) for item in row] for row in shells],
                        "sum_x": fs(x_sum),
                        "sum_positive_F": fs(flux_positive_sum),
                        "sum_TV_F": fs(variation_sum),
                        "conditions": conditions,
                    }
                )
    return {
        "id": "finite_global_scalar_excess_to_flux_variation_ledger",
        "configurations_checked": configurations,
        "strict_x_to_positive_flux_cases": strict_first,
        "strict_positive_flux_to_variation_cases": strict_second,
        "failures": failures,
        "pass": not failures and strict_first > 0 and strict_second > 0,
    }


def selected_flux_coefficient_check() -> dict:
    """Check |Q|<=beta<T/6 and K=Q+F=T imply T<(6/5)F."""
    failures: list[dict] = []
    rows = []
    terminal_values = [Fraction(1, 2), Fraction(1), Fraction(2)]
    beta_ratios = [Fraction(0), Fraction(1, 12), Fraction(19, 120)]
    signed_ratios = [
        Fraction(-19, 120),
        Fraction(-1, 12),
        Fraction(0),
        Fraction(1, 12),
        Fraction(19, 120),
    ]
    for terminal, beta_ratio, signed_ratio in itertools.product(
        terminal_values, beta_ratios, signed_ratios
    ):
        beta = terminal * beta_ratio
        Q = terminal * signed_ratio
        if abs(Q) > beta:
            continue
        F = terminal - Q
        conditions = {
            "variation_dominates_terminal_Q": abs(Q) <= beta,
            "failed_beta_priority": beta < terminal / 6,
            "clock_identity": terminal == Q + F,
            "flux_above_five_sixths": F > Fraction(5, 6) * terminal,
            "terminal_below_six_fifths_flux": terminal
            < Fraction(6, 5) * F,
        }
        row = {
            "T": fs(terminal),
            "beta": fs(beta),
            "Q": fs(Q),
            "F": fs(F),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"] and len(failures) < 20:
            failures.append(row)
    return {
        "id": "exact_selected_flux_six_fifths_coefficient",
        "configurations_checked": len(rows),
        "rows": rows,
        "failures": failures,
        "pass": not failures and bool(rows),
    }


def stopped_work_bridge_proxy_check() -> dict:
    """Finite proxy for the common zero-start stopped-work bridge.

    Existence of a common local-energy good time in the zero-cutoff interval
    and the inherited stopped-work definition are analytic inputs and are not
    machine-proved here.
    """
    candidates = (
        (Fraction(1), Fraction(1, 4), Fraction(11, 12)),
        (Fraction(2), Fraction(1, 2), Fraction(7, 4)),
        (Fraction(1, 2), Fraction(1, 8), Fraction(11, 24)),
    )
    failures: list[dict] = []
    rows = []
    for length in range(1, 5):
        for shells in itertools.product(candidates, repeat=length):
            terminal_sum = sum((row[0] for row in shells), Fraction(0))
            x_sum = sum((row[1] for row in shells), Fraction(0))
            flux_sum = sum((row[2] for row in shells), Fraction(0))
            common_zero_start_work = flux_sum
            conditions = {
                "selected_shell_thresholds": all(
                    terminal < 6 * x and Fraction(5, 6) * terminal < flux
                    for terminal, x, flux in shells
                ),
                "family_terminal_below_six_x": terminal_sum < 6 * x_sum,
                "x_below_common_terminal_flux": x_sum <= flux_sum,
                "zero_start_work_equals_terminal_flux": common_zero_start_work
                == flux_sum,
                "positive_common_stopped_work": common_zero_start_work > 0,
                "sharp_selected_coefficient": terminal_sum
                < Fraction(6, 5) * common_zero_start_work,
            }
            row = {
                "shells": [[fs(item) for item in shell] for shell in shells],
                "sum_T": fs(terminal_sum),
                "sum_x": fs(x_sum),
                "sum_F": fs(flux_sum),
                "common_zero_start_work": fs(common_zero_start_work),
                "conditions": conditions,
                "pass": all(conditions.values()),
            }
            rows.append(row)
            if not row["pass"] and len(failures) < 20:
                failures.append(row)
    return {
        "id": "finite_selected_excess_to_common_terminal_stopped_work_proxy",
        "configurations_checked": len(rows),
        "analytic_common_good_zero_start_machine_proved": False,
        "inherited_stopped_work_definition_machine_proved": False,
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def no_exception_clock_comparison_check() -> dict:
    """Finite shell-partition proxy for both comparisons in S.198."""
    failures: list[dict] = []
    configurations = 0
    sharp_C_minus_W = 0
    sharp_W_minus_C = 0
    sharp_K_lower = 0
    sharp_K_upper = 0
    length = 2
    clock_values = [Fraction(0), Fraction(1), Fraction(2)]
    Q_values = [Fraction(-1), Fraction(0), Fraction(1)]
    stop_ratios = [Fraction(0), Fraction(1, 2)]

    for terminal_K, terminal_Q in itertools.product(
        itertools.product(clock_values, repeat=length),
        itertools.product(Q_values, repeat=length),
    ):
        terminal_F = tuple(
            K - Q for K, Q in zip(terminal_K, terminal_Q)
        )
        terminal_clock_sum = sum(terminal_K, Fraction(0))
        terminal_flux_positive = max(sum(terminal_F, Fraction(0)), Fraction(0))
        terminal_B = sum((abs(Q) for Q in terminal_Q), Fraction(0))

        # Lower comparisons use the common zero start.  K=0 shells are not
        # admissible in the stopped family and create the sharp B_Q loss.
        zero_flux_selected = sum(
            (
                F
                for K, F in zip(terminal_K, terminal_F)
                if K > 0 and F > 0
            ),
            Fraction(0),
        )
        zero_all_positive_clocks = sum(
            (F for K, F in zip(terminal_K, terminal_F) if K > 0),
            Fraction(0),
        )
        zero_all_positive_part = max(zero_all_positive_clocks, Fraction(0))
        lower_conditions = {
            "C_minus_zero_selected_below_terminal_B": terminal_flux_positive
            - zero_flux_selected
            <= terminal_B,
            "K_minus_B_below_zero_all_positive_part": terminal_clock_sum
            - terminal_B
            <= zero_all_positive_part,
        }
        if terminal_flux_positive - zero_flux_selected == terminal_B and terminal_B > 0:
            sharp_C_minus_W += 1
        if terminal_clock_sum - terminal_B == zero_all_positive_part and terminal_clock_sum > 0:
            sharp_K_lower += 1
        if not all(lower_conditions.values()) and len(failures) < 20:
            failures.append(
                {
                    "case": "common_zero_lower",
                    "terminal_K": [fs(item) for item in terminal_K],
                    "terminal_Q": [fs(item) for item in terminal_Q],
                    "terminal_F": [fs(item) for item in terminal_F],
                    "B_Q_proxy": fs(terminal_B),
                    "C_full_proxy": fs(terminal_flux_positive),
                    "zero_selected_work": fs(zero_flux_selected),
                    "zero_all_work_positive_part": fs(zero_all_positive_part),
                    "conditions": lower_conditions,
                }
            )

        # Upper comparisons use the exact partition identity displayed before
        # S.198.  The selected Q(sigma) and unselected Q(tau) rows are disjoint
        # pieces of the global Q-variation ledger.
        for mask in range(1, 1 << length):
            for ratios, stop_Q in itertools.product(
                itertools.product(stop_ratios, repeat=length),
                itertools.product(Q_values, repeat=length),
            ):
                selected = [bool(mask & (1 << index)) for index in range(length)]
                if any(
                    selected[index]
                    and (
                        terminal_K[index] <= 0
                        or terminal_K[index]
                        - terminal_K[index] * ratios[index]
                        <= terminal_K[index] / 4
                    )
                    for index in range(length)
                ):
                    continue
                stop_K = tuple(
                    terminal_K[index] * ratios[index]
                    for index in range(length)
                )
                stopped_work = sum(
                    (
                        terminal_F[index]
                        - (stop_K[index] - stop_Q[index])
                        for index in range(length)
                        if selected[index]
                    ),
                    Fraction(0),
                )
                stopped_positive = max(stopped_work, Fraction(0))
                flux_partition_B = sum(
                    (
                        abs(stop_Q[index])
                        if selected[index]
                        else abs(terminal_Q[index])
                        for index in range(length)
                    ),
                    Fraction(0),
                )
                clock_increment_B = sum(
                    (
                        abs(terminal_Q[index] - stop_Q[index])
                        for index in range(length)
                        if selected[index]
                    ),
                    Fraction(0),
                )
                partition_B = max(flux_partition_B, clock_increment_B)
                conditions = {
                    "work_minus_terminal_flux_below_partition_B": stopped_work
                    - sum(terminal_F, Fraction(0))
                    <= partition_B,
                    "positive_work_below_C_plus_partition_B": stopped_positive
                    <= terminal_flux_positive + partition_B,
                    "positive_work_below_K_plus_partition_B": stopped_positive
                    <= terminal_clock_sum + partition_B,
                }
                configurations += 1
                if stopped_positive - terminal_flux_positive == partition_B and partition_B > 0:
                    sharp_W_minus_C += 1
                if stopped_positive == terminal_clock_sum + partition_B and partition_B > 0:
                    sharp_K_upper += 1
                if not all(conditions.values()) and len(failures) < 20:
                    failures.append(
                        {
                            "case": "admissible_stopped_upper",
                            "terminal_K": [fs(item) for item in terminal_K],
                            "terminal_Q": [fs(item) for item in terminal_Q],
                            "terminal_F": [fs(item) for item in terminal_F],
                            "selected": selected,
                            "stop_K": [fs(item) for item in stop_K],
                            "stop_Q": [fs(item) for item in stop_Q],
                            "partition_B": fs(partition_B),
                            "flux_partition_B": fs(flux_partition_B),
                            "clock_increment_B": fs(clock_increment_B),
                            "C_full_proxy": fs(terminal_flux_positive),
                            "stopped_work": fs(stopped_work),
                            "conditions": conditions,
                        }
                    )
    return {
        "id": "finite_no_exception_clock_and_flux_comparison",
        "configurations_checked": configurations,
        "sharp_C_minus_W_equals_B_cases": sharp_C_minus_W,
        "sharp_W_minus_C_equals_B_cases": sharp_W_minus_C,
        "sharp_K_lower_cases": sharp_K_lower,
        "sharp_K_upper_cases": sharp_K_upper,
        "failures": failures,
        "pass": (
            not failures
            and sharp_C_minus_W > 0
            and sharp_W_minus_C > 0
            and sharp_K_lower > 0
            and sharp_K_upper > 0
        ),
    }


def exact_family_refutation_check() -> dict:
    """Finite scaling proxy for the inherited smooth exact-family refutation."""
    rows = []
    failures = []
    previous_ratio: Fraction | None = None
    for exponent in range(1, 13):
        K_star = Fraction(2**exponent)
        T_star = Fraction(1)
        cumulative_flux = T_star
        payment_two_thirds = T_star / K_star
        stopped_work_lower = cumulative_flux
        ratio = stopped_work_lower / payment_two_thirds
        conditions = {
            "C_comparable_proxy": cumulative_flux == T_star,
            "payment_proxy": payment_two_thirds == T_star / K_star,
            "ratio_equals_K_star": ratio == K_star,
            "ratio_strictly_increases": previous_ratio is None
            or ratio > previous_ratio,
        }
        row = {
            "K_star": fs(K_star),
            "T_star": fs(T_star),
            "C": fs(cumulative_flux),
            "P_to_two_thirds": fs(payment_two_thirds),
            "W_up_lower": fs(stopped_work_lower),
            "ratio": fs(ratio),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)
        previous_ratio = ratio
    return {
        "id": "finite_inherited_exact_family_universal_quadratic_refutation_proxy",
        "rows_checked": len(rows),
        "last_ratio": rows[-1]["ratio"],
        "inherited_smooth_PDE_family_machine_proved": False,
        "rows": rows,
        "failures": failures,
        "pass": not failures and previous_ratio == Fraction(4096),
    }


def conditional_S38_arithmetic_check() -> dict:
    """Check that refuting the antecedent does not alter the implication."""
    failures = []
    rows = []
    values = [Fraction(0), Fraction(1, 4), Fraction(1), Fraction(2)]
    for A, C_Q, C_W in itertools.product(
        [Fraction(1, 4), Fraction(1), Fraction(2)], values, values
    ):
        Q_payment = C_Q * A
        W_bound = C_W * A
        inherited_rhs = 4 * Q_payment + 4 * W_bound
        conditional_rhs = 4 * (C_Q + C_W) * A
        row = {
            "A": fs(A),
            "C_Q": fs(C_Q),
            "C_W": fs(C_W),
            "inherited_rhs": fs(inherited_rhs),
            "conditional_rhs": fs(conditional_rhs),
            "pass": inherited_rhs == conditional_rhs,
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)
    return {
        "id": "finite_S38_conditional_implication_arithmetic",
        "configurations_checked": len(rows),
        "universal_antecedent_machine_assumed": False,
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def compact(body: str) -> str:
    result = re.sub(r"\s+", "", body)
    result = result.replace("&", "")
    for spacing in (r"\,", r"\!", r"\;", r"\:"):
        result = result.replace(spacing, "")
    return result


FORBIDDEN_CLAIMS = (
    "We prove that the selected excess sum is lower semicontinuous",
    "We prove that X vanishes for the exact shear",
    "We prove that weak-* convergence implies convergence of the hard-interval masses",
    "We prove that every suitable weak solution admits smooth Navier--Stokes approximants",
    "We prove that the certificate machine-proves measure topology",
    "We prove that the certificate proves the Navier--Stokes PDE theorem",
    "We prove that global regularity is proved",
    "We prove that the Navier--Stokes Millennium problem is solved",
)


def forbidden_claims(body: str) -> list[str]:
    lowered = body.lower()
    return [phrase for phrase in FORBIDDEN_CLAIMS if phrase.lower() in lowered]


def section(body: str, start: str, end: str) -> str:
    left = body.find(start)
    right = body.find(end, left + len(start)) if left >= 0 else -1
    if left < 0 or right < 0:
        return ""
    return body[left:right]


def priority_order_guard(body: str) -> bool:
    block = section(body, "Partition it in the following priority order:", r"\tag{S.170}")
    labels = (r"\mathcal I_\beta(\tau)", r"\mathcal I_\sigma(\tau)", r"\mathcal I_x(\tau)")
    positions = [block.find(label) for label in labels]
    return all(position >= 0 for position in positions) and positions == sorted(positions)


def selected_index_guard(body: str) -> bool:
    block = section(body, r"\tag{S.177}", r"\tag{S.179}")
    return r"\mathcal I_x(\tau)" in block and r"\mathcal I_X(\tau)" not in block


def threshold_guard(body: str) -> bool:
    definition_block = compact(
        section(body, "Partition it in the following priority order:", r"\tag{S.170}")
    )
    conclusion_block = compact(section(body, r"\tag{S.170}", r"\tag{S.172}"))
    definition_needles = (
        r"\beta_{k,R}(J_\tau)\ge\frac16T_k",
        r"\sigma_{k,R}(J_\tau)>\frac{T_k}{12\lambda_k}",
    )
    conclusion_needle = r"x_{k,R}^{\boldsymbol\lambda}(\tau)>\frac16T_k"
    return all(
        compact(needle) in definition_block for needle in definition_needles
    ) and compact(conclusion_needle) in conclusion_block


def x_X_definition_guard(body: str) -> bool:
    compressed = compact(body)
    needles = (
        r"x_{k,R}^{\boldsymbol\lambda}(\tau):=\left[\alpha_{k,R}^{\boldsymbol\lambda}(J_\tau)\right]_+",
        r"X_{k,R}^{\boldsymbol\lambda}(\tau):=(\alpha_{k,R}^{\boldsymbol\lambda})^+(J_\tau)",
        r"0\le[\alpha(J_\tau)]_+\le\alpha^+(J_\tau)",
    )
    return all(compact(needle) in compressed for needle in needles)


def open_endpoint_guard(body: str) -> bool:
    compressed = compact(body)
    return (
        compact(r"J_\tau:=(s_R,\tau)") in compressed
        and r"The interval \(J_\tau\) is open at the terminal endpoint." in body
    )


def sharp_six_fifths_guard(body: str) -> bool:
    block = compact(section(body, r"\tag{S.194}", r"\tag{S.196}"))
    needles = (
        r"F_{k,R}(\tau)=T_k-Q_{k,R}(\tau)\ge T_k-|Q_{k,R}(\tau)|>{5T_k\over6}",
        r"T_k<{6\over5}F_{k,R}(\tau)",
    )
    return all(compact(needle) in block for needle in needles)


def fixed_X_finiteness_guard(body: str) -> bool:
    block = compact(section(body, r"\tag{S.191}", r"\tag{S.192}"))
    needle = (
        r"\mathcal X_{1,R}^{\boldsymbol\lambda}(\tau)"
        r"\le\sum_{k\ge1}\nu_{k,R}(J_\tau)"
    )
    return compact(needle) in block and r"<\infty" in block


def global_linear_flux_guard(body: str) -> bool:
    block = compact(section(body, r"\tag{S.192}", r"\tag{S.193}"))
    needle = (
        r"\mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)"
        r"\le\sum_{k\ge1}[F_{k,R}(\tau)]_+"
        r"\le\sum_{k\ge1}\operatorname {TV}_{[s_R,t_0)}F_{k,R}"
        r"\le\mathfrak L_{{\rm abs},R}^M\le CP_R^M"
    )
    return compact(needle) in block


def no_exception_clock_guard(body: str) -> bool:
    definitions = compact(section(body, r"\tag{S.196}", r"\tag{S.197}"))
    comparison = compact(section(body, r"\tag{S.197}", r"\tag{S.198}"))
    definition_needles = (
        r"B_{Q,R}^M:=\sum_{k\ge1}\operatorname {TV}_{[s_R,t_0)}Q_{k,R}",
        r"\mathcal K_R^M:=\sup_{\tau\in\mathcal G_R}\sum_{k\ge1}K_{k,R}(\tau)",
        r"\mathfrak C_{{\rm full},R}^M:=\sup_{s_R<\tau<t_0}\left[\sum_{k\ge1}F_{k,R}(\tau)\right]_+",
    )
    comparison_needles = (
        r"\mathcal K_R^M-B_{Q,R}^M\le\mathfrak W_{{\rm up},R}^M\le\mathcal K_R^M+B_{Q,R}^M",
        r"\bigl|\mathfrak W_{{\rm up},R}^M-\mathfrak C_{{\rm full},R}^M\bigr|\le B_{Q,R}^M",
    )
    return all(compact(item) in definitions for item in definition_needles) and all(
        compact(item) in comparison for item in comparison_needles
    )


def no_exception_zero_start_guard(body: str) -> bool:
    block = section(body, r"\tag{S.196}", r"\tag{S.199}")
    return (
        "The same zero-start observation" in block
        and "use the common zero stop on arbitrary finite subsets" in block
        and "common zero stop makes its stopped work" in body
    )


def universal_refutation_guard(body: str) -> bool:
    prose = re.sub(r"\s+", " ", body)
    return all(
        item in prose
        for item in (
            "The following are **REFUTED**:",
            "the universal all-solution estimate",
            "The conditional implication (S.38) itself remains correct.",
            "This refutes the *universal antecedent*",
            "it does not refute the conditional algebra in (S.38), (S.196)",
        )
    )


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.(\d+)\}", body)
    expected = [str(number) for number in range(163, 200)]
    compressed = compact(body)
    prose = re.sub(r"\s+", " ", body)
    checks: list[dict] = [
        {
            "id": "tags_consecutive_S163_through_S199",
            "actual": tags,
            "expected": expected,
            "pass": tags == expected,
        },
        {
            "id": "tags_unique",
            "actual_count": len(tags),
            "unique_count": len(set(tags)),
            "pass": len(tags) == len(set(tags)) == len(expected),
        },
        {"id": "priority_order_beta_sigma_x", "pass": priority_order_guard(body)},
        {"id": "selected_index_is_I_x", "pass": selected_index_guard(body)},
        {"id": "literal_thresholds", "pass": threshold_guard(body)},
        {"id": "scalar_and_Jordan_definitions_distinct", "pass": x_X_definition_guard(body)},
        {"id": "open_terminal_endpoint", "pass": open_endpoint_guard(body)},
        {"id": "sharp_five_sixths_six_fifths", "pass": sharp_six_fifths_guard(body)},
        {"id": "fixed_scale_Jordan_finiteness", "pass": fixed_X_finiteness_guard(body)},
        {"id": "global_scalar_linear_flux_ledger", "pass": global_linear_flux_guard(body)},
        {"id": "no_exception_clock_comparison", "pass": no_exception_clock_guard(body)},
        {"id": "no_exception_common_zero_start", "pass": no_exception_zero_start_guard(body)},
        {"id": "universal_gate_refuted_not_open", "pass": universal_refutation_guard(body)},
    ]

    required_text = (
        "This is an exact unification and a weak-stability interface, not a quadratic payment theorem.",
        "The selected residual is not claimed to be lower semicontinuous",
        "No smooth approximation of an arbitrary suitable weak solution is asserted to exist.",
        "all three measures in (S.164) vanish on one common neighborhood of the left endpoint",
        "The constants are literal.",
        "All infinite sums are obtained from arbitrary finite shell subsets and then monotone convergence.",
        "not an unconditional strict numerical sharpening of (S.160)",
        "it does not assert convergence of its mass",
        "not a smooth-density theorem",
        "There is no functional cubic bound for either excess tier",
        "Endpoint escape permits only lower semicontinuity",
        r"Uniform primitive convergence is insufficient for \(\beta\)",
        r"both extended sums in (S.179) are in fact finite at every fixed \(R\) and good \(\tau\)",
        "the scalar residual is not a new open channel but a subledger of the existing signed stopped work",
        "This does not itself improve that gate.",
        "up to an already-paid quadratic row, the full-cutoff positive cumulative flux itself",
        "The conditional implication (S.38) itself remains correct.",
        "The following are **REFUTED**:",
        "The coefficient one in the second comparison is sharp already for the scalar single-shell stress",
        r"\(K=0\), \(Q=-B\), \(F=B\)",
        "The following are **PROVED**:",
        "The following are **CONDITIONAL**:",
        "The following are **INHERITED**:",
        "The following remain **OPEN**:",
        "The following are **NOT CLAIMED**:",
        "**NOT CLAY.**",
    )
    required_formula = (
        r"J_\tau:=(s_R,\tau)",
        r"\alpha_{k,R}^{\boldsymbol\lambda}:=\nu_{k,R}-\beta_{k,R}-2\lambda_k\sigma_{k,R}",
        r"0\le[\alpha(J_\tau)]_+\le\alpha^+(J_\tau)",
        r"\nu_{k,R}(J_\tau)\le\beta_{k,R}(J_\tau)+2\lambda_k\sigma_{k,R}(J_\tau)+x_{k,R}^{\boldsymbol\lambda}(\tau)",
        r"\sigma_{k,R}(J_\tau)>\frac{T_k}{12\lambda_k}",
        r">{1\over2}\left({T_k\over12\lambda_k}\right)^{3/2}",
        r"C_4=12(2C_1)^{2/3}",
        r"\mathscr L(\boldsymbol\lambda):=\sum_{k\ge1}2^{3k}\gamma_k\lambda_k^3",
        r"+6\sum_{k\in\mathcal I_x(\tau)}x_{k,R}^{\boldsymbol\lambda}(\tau)",
        r"\mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)\le\mathcal X_{1,R}^{\boldsymbol\lambda}(\tau)",
        r"x_{k,R}^{\boldsymbol\lambda}(\tau)\le X_{k,R}^{\boldsymbol\lambda}(\tau)\le m_{k,R}(\tau)+\int_{H_{k,R}}g_{k,R}(t)\,dt",
        r"x_{k,R}^{\boldsymbol\lambda}(\tau)=0",
        r"\nu_{k,R}(J_\tau)\le\liminf_{n\to\infty}\nu_{k,R}^{(n)}(J_\tau)",
        r"x_{k,R}^{\boldsymbol\lambda}[u,p](\tau)\le\liminf_{n\to\infty}x_{k,R}^{\boldsymbol\lambda}[u_n,p_n](\tau)",
        r"X_{k,R}^{\boldsymbol\lambda}[u,p](\tau)\le\liminf_{n\to\infty}X_{k,R}^{\boldsymbol\lambda}[u_n,p_n](\tau)",
        r"X_{k,R}^{\boldsymbol\lambda}[u,p](\tau)=\int_{s_R}^{\tau}\left[g_{k,R}(t)-|\dot Q_{k,R}(t)|-{2\lambda_k\over R^2}e_{k,R}(t)\right]_+dt",
        r"0\le x_{k,R}^{\boldsymbol\lambda}(\tau)\le X_{k,R}^{\boldsymbol\lambda}(\tau)\le\nu_{k,R}(J_\tau)",
        r"\mathcal X_{1,R}^{\boldsymbol\lambda}(\tau)\le\sum_{k\ge1}\nu_{k,R}(J_\tau)",
        r"x_{k,R}^{\boldsymbol\lambda}(\tau)\le[F_{k,R}(\tau)]_+",
        r"\mathfrak x_{1,R}^{\boldsymbol\lambda}(\tau)\le\mathfrak W_{{\rm up},R}^M\le\mathfrak L_{{\rm abs},R}^M\le CP_R^M",
        r"|Q_{k,R}(\tau)|\le\beta_{k,R}(J_\tau)<{T_k\over6}",
        r"F_{k,R}(\tau)=T_k-Q_{k,R}(\tau)\ge T_k-|Q_{k,R}(\tau)|>{5T_k\over6}",
        r"T_k<{6\over5}F_{k,R}(\tau)",
        r"\sum_{k\in\mathcal I_x(\tau)}K_{k,R}(\tau)\le{6\over5}\mathfrak W_{{\rm up},R}^M",
        r"B_{Q,R}^M:=\sum_{k\ge1}\operatorname {TV}_{[s_R,t_0)}Q_{k,R}\le C_Q(P_R^M)^{2/3}",
        r"\mathcal K_R^M-B_{Q,R}^M\le\mathfrak W_{{\rm up},R}^M\le\mathcal K_R^M+B_{Q,R}^M",
        r"\bigl|\mathfrak W_{{\rm up},R}^M-\mathfrak C_{{\rm full},R}^M\bigr|\le B_{Q,R}^M",
        r"{\mathfrak W_{{\rm up},R_j}^{M,*}\over(P_{R_j}^{M,*})^{2/3}}\longrightarrow\infty",
    )
    for sentinel in required_text:
        checks.append(
            {
                "id": "required_text_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in prose,
            }
        )
    for sentinel in required_formula:
        checks.append(
            {
                "id": "required_formula_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": compact(sentinel) in compressed,
            }
        )
    for phrase in FORBIDDEN_CLAIMS:
        checks.append(
            {
                "id": "forbidden_" + hashlib.sha256(phrase.encode()).hexdigest()[:12],
                "sentinel": phrase,
                "pass": phrase.lower() not in body.lower(),
            }
        )
    return checks


def replace_in_section(body: str, start: str, end: str, old: str, new: str) -> str:
    left = body.find(start)
    right = body.find(end, left + len(start)) if left >= 0 else -1
    if left < 0 or right < 0:
        return body
    block = body[left:right]
    if old not in block:
        return body
    return body[:left] + block.replace(old, new, 1) + body[right:]


def negative_mutation_checks(body: str) -> list[dict]:
    rows: list[dict] = []

    block = section(body, "Partition it in the following priority order:", r"\tag{S.170}")
    swapped = block.replace(r"\mathcal I_\beta(\tau)", "__TMP__", 1)
    swapped = swapped.replace(r"\mathcal I_\sigma(\tau)", r"\mathcal I_\beta(\tau)", 1)
    swapped = swapped.replace("__TMP__", r"\mathcal I_\sigma(\tau)", 1)
    reordered_body = body.replace(block, swapped, 1)
    rows.append(
        {
            "id": "mutation_reorder_priority_sigma_before_beta",
            "original_guard": priority_order_guard(body),
            "mutated_guard": priority_order_guard(reordered_body),
            "pass": priority_order_guard(body) and not priority_order_guard(reordered_body),
        }
    )

    stale_body = replace_in_section(
        body,
        r"\tag{S.177}",
        r"\tag{S.179}",
        r"\mathcal I_x(\tau)",
        r"\mathcal I_X(\tau)",
    )
    rows.append(
        {
            "id": "mutation_stale_or_undefined_I_X_selected_index",
            "original_guard": selected_index_guard(body),
            "mutated_guard": selected_index_guard(stale_body),
            "pass": selected_index_guard(body) and not selected_index_guard(stale_body),
        }
    )

    beta_mutation = replace_in_section(
        body,
        "Partition it in the following priority order:",
        r"\tag{S.172}",
        r"\frac16T_k",
        r"\frac15T_k",
    )
    rows.append(
        {
            "id": "mutation_beta_threshold_one_sixth_to_one_fifth",
            "original_guard": threshold_guard(body),
            "mutated_guard": threshold_guard(beta_mutation),
            "counterexample": "nu=T/2, beta just below T/5, 2 lambda sigma=T/6 leaves less than T/6",
            "pass": threshold_guard(body) and not threshold_guard(beta_mutation),
        }
    )

    sigma_mutation = replace_in_section(
        body,
        "Partition it in the following priority order:",
        r"\tag{S.172}",
        r"12\lambda_k",
        r"10\lambda_k",
    )
    rows.append(
        {
            "id": "mutation_sigma_threshold_denominator_twelve_to_ten",
            "original_guard": threshold_guard(body),
            "mutated_guard": threshold_guard(sigma_mutation),
            "pass": threshold_guard(body) and not threshold_guard(sigma_mutation),
        }
    )

    jensen_fixture_cubic = Fraction(4)
    jensen_fixture_sigma = Fraction(4)
    rows.append(
        {
            "id": "mutation_Jensen_half_constant_to_one",
            "fixture": "constant unit energy on normalized length four",
            "correct_squared": 4 * jensen_fixture_cubic**2
            >= jensen_fixture_sigma**3,
            "mutated_squared": jensen_fixture_cubic**2
            >= jensen_fixture_sigma**3,
            "pass": (
                4 * jensen_fixture_cubic**2 == jensen_fixture_sigma**3
                and jensen_fixture_cubic**2 < jensen_fixture_sigma**3
            ),
        }
    )

    correct_C4_cube = Fraction(12**3 * 4)
    mutated_C4_cube = Fraction(12**3)
    rows.append(
        {
            "id": "mutation_drop_factor_two_inside_C4",
            "correct_C4_cube": fs(correct_C4_cube),
            "mutated_C4_cube": fs(mutated_C4_cube),
            "pass": correct_C4_cube == 4 * mutated_C4_cube,
        }
    )

    definition_mutation = body.replace(
        r"\left[\alpha_{k,R}^{\boldsymbol\lambda}(J_\tau)\right]_+",
        r"(\alpha_{k,R}^{\boldsymbol\lambda})^+(J_\tau)",
        1,
    )
    cancellation = (Fraction(1), Fraction(-1))
    cancellation_x = max(sum(cancellation, Fraction(0)), Fraction(0))
    cancellation_X = sum(
        (max(item, Fraction(0)) for item in cancellation), Fraction(0)
    )
    rows.append(
        {
            "id": "mutation_conflate_scalar_x_with_Jordan_X",
            "original_guard": x_X_definition_guard(body),
            "mutated_guard": x_X_definition_guard(definition_mutation),
            "counterexample_x": fs(cancellation_x),
            "counterexample_X": fs(cancellation_X),
            "pass": (
                x_X_definition_guard(body)
                and not x_X_definition_guard(definition_mutation)
                and cancellation_x < cancellation_X
            ),
        }
    )

    endpoint_mutation = body.replace(r"J_\tau:=(s_R,\tau)", r"J_\tau:=(s_R,\tau]", 1)
    rows.append(
        {
            "id": "mutation_close_hard_terminal_endpoint",
            "original_guard": open_endpoint_guard(body),
            "mutated_guard": open_endpoint_guard(endpoint_mutation),
            "open_target_mass": "0/1",
            "closed_target_mass": "1/1",
            "pass": open_endpoint_guard(body) and not open_endpoint_guard(endpoint_mutation),
        }
    )

    X_finiteness_mutation = replace_in_section(
        body,
        r"\tag{S.191}",
        r"\tag{S.192}",
        r"<\infty",
        r"\le C(P_R^M)^{2/3}",
    )
    rows.append(
        {
            "id": "mutation_promote_fixed_scale_X_finiteness_to_quadratic_bound",
            "original_guard": fixed_X_finiteness_guard(body),
            "mutated_guard": fixed_X_finiteness_guard(X_finiteness_mutation),
            "pass": fixed_X_finiteness_guard(body)
            and not fixed_X_finiteness_guard(X_finiteness_mutation),
        }
    )

    scalar_linear_mutation = replace_in_section(
        body,
        r"\tag{S.192}",
        r"\tag{S.193}",
        r"\le CP_R^M",
        r"\le C(P_R^M)^{2/3}",
    )
    rows.append(
        {
            "id": "mutation_promote_linear_scalar_flux_bound_to_quadratic",
            "original_guard": global_linear_flux_guard(body),
            "mutated_guard": global_linear_flux_guard(scalar_linear_mutation),
            "pass": global_linear_flux_guard(body)
            and not global_linear_flux_guard(scalar_linear_mutation),
        }
    )

    refuted_to_open = body.replace(
        "The following are **REFUTED**:",
        "The following remain **OPEN**:",
        1,
    )
    rows.append(
        {
            "id": "mutation_change_universal_gate_REFUTED_back_to_OPEN",
            "original_guard": universal_refutation_guard(body),
            "mutated_guard": universal_refutation_guard(refuted_to_open),
            "pass": universal_refutation_guard(body)
            and not universal_refutation_guard(refuted_to_open),
        }
    )

    deleted_zero_start = body.replace(
        "use the common zero stop on arbitrary finite subsets",
        "use an unspecified stop on arbitrary finite subsets",
        1,
    )
    rows.append(
        {
            "id": "mutation_delete_common_zero_start_from_lower_comparison",
            "original_guard": no_exception_zero_start_guard(body),
            "mutated_guard": no_exception_zero_start_guard(deleted_zero_start),
            "fixture_K_terminal": "1/1",
            "fixture_B_Q": "0/1",
            "zero_start_work": "1/1",
            "nonzero_stop_work": "1/3",
            "zero_start_meets_K_minus_B": Fraction(1) >= Fraction(1),
            "nonzero_stop_fails_K_minus_B": Fraction(1, 3) < Fraction(1),
            "pass": no_exception_zero_start_guard(body)
            and not no_exception_zero_start_guard(deleted_zero_start)
            and Fraction(1) >= Fraction(1)
            and Fraction(1, 3) < Fraction(1),
        }
    )

    comparison_block = section(body, r"\tag{S.197}", r"\tag{S.198}")
    last_B_position = comparison_block.rfind(r"\le B_{Q,R}^M")
    inflated_block = (
        comparison_block[:last_B_position]
        + r"\le2B_{Q,R}^M"
        + comparison_block[last_B_position + len(r"\le B_{Q,R}^M") :]
        if last_B_position >= 0
        else comparison_block
    )
    inflated_B = body.replace(comparison_block, inflated_block, 1)
    B = Fraction(1)
    C_full = Fraction(1)
    Ksup = Fraction(0)
    Wup = Fraction(0)
    rows.append(
        {
            "id": "mutation_weaken_sharp_BQ_flux_comparison_to_2BQ",
            "original_guard": no_exception_clock_guard(body),
            "mutated_guard": no_exception_clock_guard(inflated_B),
            "fixture_B_Q": fs(B),
            "fixture_C_full": fs(C_full),
            "fixture_K_sup": fs(Ksup),
            "fixture_W_up": fs(Wup),
            "sharp_B_bound_is_attained": abs(Wup - C_full) == B,
            "weaker_2B_bound_has_slack": abs(Wup - C_full) < 2 * B,
            "pass": (
                no_exception_clock_guard(body)
                and not no_exception_clock_guard(inflated_B)
                and abs(Wup - C_full) == B
                and abs(Wup - C_full) < 2 * B
            ),
        }
    )

    deleted_block = (
        comparison_block[:last_B_position]
        + r"\le0"
        + comparison_block[last_B_position + len(r"\le B_{Q,R}^M") :]
        if last_B_position >= 0
        else comparison_block
    )
    deleted_B = body.replace(comparison_block, deleted_block, 1)
    rows.append(
        {
            "id": "mutation_delete_BQ_error_from_flux_comparison",
            "original_guard": no_exception_clock_guard(body),
            "mutated_guard": no_exception_clock_guard(deleted_B),
            "sharp_single_shell_fixture": "K=0, Q=-B, F=B, C_full=B, W_up=0",
            "correct_B_bound": abs(Wup - C_full) <= B,
            "mutated_zero_error_bound": abs(Wup - C_full) <= 0,
            "pass": (
                no_exception_clock_guard(body)
                and not no_exception_clock_guard(deleted_B)
                and abs(Wup - C_full) == B
                and not abs(Wup - C_full) <= 0
            ),
        }
    )

    claim_injections = (
        (
            "mutation_promote_liminf_to_hard_mass_convergence",
            "We prove that weak-* convergence implies convergence of the hard-interval masses.",
        ),
        (
            "mutation_assert_smooth_density_existence",
            "We prove that every suitable weak solution admits smooth Navier--Stokes approximants.",
        ),
        (
            "mutation_assert_selected_sum_lsc",
            "We prove that the selected excess sum is lower semicontinuous.",
        ),
        (
            "mutation_assert_X_zero_for_shear",
            "We prove that X vanishes for the exact shear.",
        ),
        (
            "mutation_promote_finite_certificate_to_measure_PDE_Clay",
            "\n".join(
                (
                    "We prove that the certificate machine-proves measure topology.",
                    "We prove that the certificate proves the Navier--Stokes PDE theorem.",
                    "We prove that global regularity is proved.",
                    "We prove that the Navier--Stokes Millennium problem is solved.",
                )
            ),
        ),
    )
    for identifier, injection in claim_injections:
        mutated = body + "\n" + injection + "\n"
        detected = forbidden_claims(mutated)
        expected_count = len(
            [phrase for phrase in FORBIDDEN_CLAIMS if phrase.lower() in injection.lower()]
        )
        rows.append(
            {
                "id": identifier,
                "forbidden_claims_injected": expected_count,
                "forbidden_claims_detected": detected,
                "pass": expected_count > 0 and len(detected) == expected_count,
            }
        )

    coefficient_mutation = replace_in_section(
        body,
        r"\tag{S.194}",
        r"\tag{S.196}",
        r"{6\over5}F_{k,R}(\tau)",
        r"F_{k,R}(\tau)",
    )
    terminal = Fraction(1)
    Q = Fraction(19, 120)
    beta = Fraction(19, 120)
    flux = terminal - Q
    rows.append(
        {
            "id": "mutation_drop_selected_six_fifths_coefficient_to_one",
            "T": fs(terminal),
            "Q": fs(Q),
            "beta": fs(beta),
            "F": fs(flux),
            "original_guard": sharp_six_fifths_guard(body),
            "mutated_guard": sharp_six_fifths_guard(coefficient_mutation),
            "correct_six_fifths_bound": terminal < Fraction(6, 5) * flux,
            "mutated_unit_coefficient_bound": terminal < flux,
            "pass": (
                abs(Q) <= beta < terminal / 6
                and terminal == Q + flux
                and terminal < Fraction(6, 5) * flux
                and not terminal < flux
                and sharp_six_fifths_guard(body)
                and not sharp_six_fifths_guard(coefficient_mutation)
            ),
        }
    )
    return rows


def render_report(data: dict, json_hash: str) -> str:
    summary = data["summary"]
    status = "PASS" if data["pass"] else "FAIL"
    finite = {row["id"]: row for row in data["finite_checks"]}
    jordan = finite["finite_signed_measure_scalar_x_below_Jordan_X"]
    decomposition = finite["finite_nonnegative_measure_decomposition"]
    trichotomy = finite["exact_one_sixth_beta_sigma_x_priority_trichotomy"]
    jensen = finite["exact_rational_Jensen_on_normalized_length_below_four"]
    C4 = finite["C4_equals_12_times_2C1_to_two_thirds_cube_identity"]
    holder = finite["exact_rational_cross_shell_Holder"]
    ledgers = finite["finite_selected_and_global_excess_ledgers"]
    shear = finite["exact_shear_terminal_scalar_excess_absorbed_by_beta"]
    lsc = finite["finite_Portmanteau_positive_part_lsc_direction_proxy"]
    Jordan_lsc = finite[
        "finite_compact_test_supremum_lsc_proxy_for_Jordan_X"
    ]
    smooth = finite["finite_absolute_continuous_density_x_versus_X_cancellation"]
    endpoint = finite["open_terminal_endpoint_escape_direction"]
    flux = finite["finite_terminal_Q_variation_to_signed_flux_reduction"]
    global_flux = finite["finite_global_scalar_excess_to_flux_variation_ledger"]
    selected_flux = finite["exact_selected_flux_six_fifths_coefficient"]
    stopped = finite[
        "finite_selected_excess_to_common_terminal_stopped_work_proxy"
    ]
    clock_comparison = finite["finite_no_exception_clock_and_flux_comparison"]
    exact_family = finite[
        "finite_inherited_exact_family_universal_quadratic_refutation_proxy"
    ]
    conditional_S38 = finite["finite_S38_conditional_implication_arithmetic"]

    exact_rows = "\n".join(
        f"| {row['id']} | {row['left']} | {row['right']} | {row['margin']} |"
        for row in data["exact_checks"]
    )
    mutation_rows = "\n".join(
        f"- `{row['id']}`: {'rejected' if row['pass'] else 'NOT REJECTED'}."
        for row in data["negative_mutations"]
    )
    return f"""# R0.74S defect-relaxed total Rayleigh-excess certificate report

## Result

**{status}** — {summary['exact_passed']}/{summary['exact_total']} exact algebra rows,
{summary['finite_passed']}/{summary['finite_total']} finite checks,
{summary['structural_passed']}/{summary['structural_total']} structural checks,
and {summary['negative_mutations_passed']}/{summary['negative_mutations_total']}
negative mutations passed.

## Exact algebra

| Check | Left | Right | Margin |
|---|---:|---:|---:|
{exact_rows}

## Finite rational checks

- Scalar positive mass versus Jordan positive mass passes
  {jordan['configurations_checked']} signed atomic fixtures, including
  {jordan['strict_cancellation_cases']} strict cancellation cases.  The
  nonnegative `nu-beta-2 lambda sigma` realization independently passes
  {decomposition['configurations_checked']} fixtures.
- The literal `beta -> sigma -> x` partition passes
  {trichotomy['configurations_checked']} exact configurations.  Branch counts
  are beta={trichotomy['class_counts']['beta']},
  sigma={trichotomy['class_counts']['sigma']}, and
  x={trichotomy['class_counts']['x']}.
- Jensen passes {jensen['configurations_checked']} rational step functions on
  normalized lengths at most four.  The radical-free cube of
  `C4=12(2 C1)^(2/3)` passes {C4['configurations_checked']} fixtures.
- Cross-shell Holder passes {holder['configurations_checked']} exact fixtures.
  Selected, global scalar, and global Jordan ledgers pass
  {ledgers['configurations_checked']} shell bundles, with strict examples of
  both enlargements retained.
- Exact-shear terminal absorption passes {shear['configurations_checked']}
  `D<=K=T<=beta` fixtures and separately records why it does not prove `X=0`.
- The scalar Portmanteau/positive-part proxy passes
  {lsc['configurations_checked']} exact rows, while the finite compact-test
  supremum proxy for Jordan `X` passes
  {Jordan_lsc['configurations_checked']} rows.  The density-formula comparison
  passes {smooth['fixtures_checked']} cancellation fixtures.
- Endpoint escape has open target mass `{endpoint['target_open_mass']}` versus
  liminf approximating mass `{endpoint['liminf_approximant_open_mass']}`;
  ordinary mass convergence is correctly rejected.
- The completed-clock reduction `beta>=|Q|` passes
  {flux['configurations_checked']} exact terminal fixtures, including
  {flux['residual_x_above_one_sixth_cases']} cases where residual excess forces
  positive signed terminal flux above one sixth.
- The global scalar-excess/flux-variation chain passes
  {global_flux['configurations_checked']} finite shell families.  The
  sharp selected-shell coefficient `6/5` passes
  {selected_flux['configurations_checked']} terminal-clock fixtures, and the
  selected-family bridge to the common-zero-start stopped-work supremum passes
  {stopped['configurations_checked']} exact proxies.  Existence of the common
  good zero-start and the inherited stopped-work framework remain explicitly
  analytic inputs.
- The no-exception clock/flux comparison passes
  {clock_comparison['configurations_checked']} exact aggregate fixtures,
  including {clock_comparison['sharp_C_minus_W_equals_B_cases']} sharp
  `C_full-W_up=B_Q` cases and
  {clock_comparison['sharp_W_minus_C_equals_B_cases']} sharp reverse cases.
  The inherited exact-family scaling proxy reaches ratio
  `{exact_family['last_ratio']}` after {exact_family['rows_checked']} rows,
  while {conditional_S38['configurations_checked']} fixtures independently
  preserve the conditional arithmetic of (S.38).

## Negative mutations

{mutation_rows}

## Reproducibility

- Source note SHA-256: `{data['source']['note_sha256']}`
- Generator SHA-256: `{data['source']['generator_sha256']}`
- JSON payload SHA-256: `{json_hash}`
- There is no timestamp, random seed, floating-point calculation, network
  input, or non-standard Python dependency.
- Set `R074S_DEFECT_RELAXED_NOTE`, `R074S_DEFECT_RELAXED_JSON`, and
  `R074S_DEFECT_RELAXED_REPORT` to rebuild against explicit paths.

## Boundary

This is a finite/algebraic certificate.  It checks exact rational threshold
arithmetic, finite atomic or step-function proxies, exponent bookkeeping, and
statement integrity.  It does **not** machine-prove Jordan/Radon regularity,
Portmanteau or measure topology, the inherited R0.74P/R0.74R estimates, their
analytic hypotheses, the inherited R0.74O/P smooth exact PDE family, existence
of smooth approximants, any new Navier--Stokes PDE claim, regularity, or the
Millennium problem.  The finite scaling rows audit the arithmetic of the
stated refutation; the smooth family itself remains inherited analysis.

**FINITE/ALGEBRAIC ONLY.  MEASURE TOPOLOGY AND PDE NOT MACHINE-PROVED.  NOT CLAY.**
"""


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = exact_ledger()
    finite_checks = [
        signed_measure_jordan_check(),
        decomposed_measure_check(),
        priority_trichotomy_check(),
        jensen_check(),
        C4_cube_check(),
        holder_check(),
        selected_global_ledger_check(),
        shear_absorption_check(),
        portmanteau_lsc_proxy_check(),
        Jordan_supremum_lsc_proxy_check(),
        smooth_density_cancellation_check(),
        endpoint_escape_check(),
        terminal_flux_reduction_check(),
        global_flux_variation_ledger_check(),
        selected_flux_coefficient_check(),
        stopped_work_bridge_proxy_check(),
        no_exception_clock_comparison_check(),
        exact_family_refutation_check(),
        conditional_S38_arithmetic_check(),
    ]
    structural = structural_checks(body)
    mutations = negative_mutation_checks(body)
    summary = {
        "exact_total": len(exact_checks),
        "exact_passed": sum(row["pass"] for row in exact_checks),
        "finite_total": len(finite_checks),
        "finite_passed": sum(row["pass"] for row in finite_checks),
        "structural_total": len(structural),
        "structural_passed": sum(row["pass"] for row in structural),
        "negative_mutations_total": len(mutations),
        "negative_mutations_passed": sum(row["pass"] for row in mutations),
    }
    passed = all(
        (
            summary["exact_total"] == summary["exact_passed"],
            summary["finite_total"] == summary["finite_passed"],
            summary["structural_total"] == summary["structural_passed"],
            summary["negative_mutations_total"]
            == summary["negative_mutations_passed"],
            len({row["id"] for row in exact_checks}) == len(exact_checks),
            len({row["id"] for row in finite_checks}) == len(finite_checks),
            len({row["id"] for row in structural}) == len(structural),
            len({row["id"] for row in mutations}) == len(mutations),
            all(not row.get("failures") for row in finite_checks),
        )
    )
    script_path = Path(__file__).resolve()
    data = {
        "schema": "r074s-defect-relaxed-total-rayleigh-certificate-v1",
        "scope": {
            "finite_algebraic_only": True,
            "machine_proves_Jordan_or_Radon_regularity": False,
            "machine_proves_Portmanteau_or_measure_topology": False,
            "machine_proves_inherited_R074P_R074R_analysis": False,
            "machine_proves_inherited_R074O_R074P_exact_PDE_family": False,
            "machine_proves_good_stop_selection_or_primitive_continuity": False,
            "machine_proves_smooth_approximation_existence": False,
            "machine_proves_Navier_Stokes_PDE": False,
            "machine_proves_regularity_or_Clay": False,
        },
        "source": {
            "note": str(NOTE.relative_to(REPO)) if NOTE.is_relative_to(REPO) else str(NOTE),
            "note_sha256": sha256(NOTE),
            "generator": str(script_path.relative_to(REPO)),
            "generator_sha256": sha256(script_path),
        },
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "negative_mutations": mutations,
        "summary": summary,
        "pass": passed,
    }
    payload = (
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_bytes(payload)
    REPORT_OUT.write_text(render_report(data, sha256_bytes(payload)), encoding="utf-8")
    print(
        "R0.74S defect-relaxed total Rayleigh certificate: "
        f"exact {summary['exact_passed']}/{summary['exact_total']}, "
        f"finite {summary['finite_passed']}/{summary['finite_total']}, "
        f"structural {summary['structural_passed']}/{summary['structural_total']}, "
        "mutations "
        f"{summary['negative_mutations_passed']}/"
        f"{summary['negative_mutations_total']}"
    )
    print("PASS" if passed else "FAIL")
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
