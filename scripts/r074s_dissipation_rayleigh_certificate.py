#!/usr/bin/env python3
"""Finite certificate for R0.74S Step 7 low-Rayleigh dissipation.

The certificate checks exact rational threshold arithmetic, normalization
exponents, finite rational trichotomy and Jensen fixtures, sequence-profile
algebra, and statement sentinels.  It does not machine-prove the inherited
analytic estimates (R.214) or (R.211), any Navier--Stokes PDE assertion, or
any regularity/Clay conclusion.
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
        "R074S_DISSIPATION_NOTE",
        REPO / "research/r074s_dissipation_rayleigh_gate.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_DISSIPATION_JSON",
        REPO / "research/r074s_dissipation_rayleigh_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_DISSIPATION_REPORT",
        REPO / "research/r074s_dissipation_rayleigh_certificate_report.md",
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
    """Exact arithmetic and exponent bookkeeping behind S.148--S.155."""
    rows = [
        exact(
            "trichotomy_half_minus_two_eighths",
            Fraction(1, 2) - Fraction(1, 8) - Fraction(1, 8),
            Fraction(1, 4),
            "The unassigned low-Rayleigh viscous share is one quarter.",
        ),
        exact(
            "g_over_e_normalization_factor_two",
            2 * Fraction(1, 2),
            Fraction(1),
            "The 1/(2R) in e and 1/R in g force g=(2 rho/R^2)e.",
        ),
        exact(
            "jensen_four_R_squared_constant_squared",
            4 * Fraction(1, 2) ** 2,
            Fraction(1),
            "delta<=4 gives delta^(-1/2)>=1/2.",
        ),
        exact(
            "per_shell_power_of_two_exponent",
            Fraction(3, 2) * Fraction(2, 3),
            Fraction(1),
            "Raising the Hölder shell factor 2^(3k/2) to 2/3 gives 2^k.",
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
            "The low-mass denominator produces one power of lambda.",
        ),
        exact(
            "per_shell_payment_exponent",
            Fraction(1) * Fraction(2, 3),
            Fraction(2, 3),
            "The per-shell payment appears to the power 2/3.",
        ),
        exact(
            "per_shell_C1_exponent",
            Fraction(1) * Fraction(2, 3),
            Fraction(2, 3),
            "The inherited Hölder constant appears to the power 2/3.",
        ),
        exact(
            "per_shell_scalar_two_exponent",
            Fraction(1) * Fraction(2, 3)
            + Fraction(9, 2) * Fraction(2, 3),
            Fraction(11, 3),
            "2*8^(3/2), raised to 2/3, agrees with 8*2^(2/3).",
        ),
        exact(
            "cross_shell_holder_reciprocal_exponents",
            Fraction(1, 3) + Fraction(2, 3),
            Fraction(1),
            "Hölder uses exponents 3 and 3/2.",
        ),
        exact(
            "cross_shell_coefficient_cube_gamma_exponent",
            3 * Fraction(1, 3),
            Fraction(1),
            "(lambda 2^k gamma^(1/3))^3 contributes gamma.",
        ),
        exact(
            "residual_threshold_reciprocal",
            8 * Fraction(1, 8),
            Fraction(1),
            "Each one-eighth residual threshold yields the coefficient eight.",
        ),
        exact(
            "canonical_profile_geometric_sum",
            Fraction(1, 8) / (1 - Fraction(1, 8)),
            Fraction(1, 7),
            "epsilon=1 gives lambda_k=2^(-2k)gamma_k^(-1/3) and L=1/7.",
        ),
        exact(
            "constant_profile_tail_base_exponent",
            Fraction(3 * 4**3, 32),
            Fraction(6),
            "At k=4 the ratio exponent is six.",
        ),
        exact(
            "constant_profile_tail_exponent_growth",
            Fraction(3 * 4**4, 32) / Fraction(3 * 4**3, 32),
            Fraction(4),
            "The ratio exponent grows by a factor four at every next shell.",
        ),
        exact(
            "constant_profile_exp_series_lower_bound",
            1 + Fraction(6) + Fraction(6) ** 2 / 2,
            Fraction(25),
            "exp(6)>=1+6+6^2/2=25>16, so the tail ratio is below 1/2.",
        ),
    ]
    return rows


def trichotomy_enumeration() -> dict:
    """Enumerate exact rational dissipation splits and priority classes."""
    failures: list[dict] = []
    configurations = 0
    eligible = 0
    class_counts = {"defect": 0, "high": 0, "low": 0}
    denominator = 16

    for t_num in range(1, 5):
        terminal = Fraction(t_num, 2)
        values = [terminal * Fraction(j, denominator) for j in range(9)]
        for defect, high, low in itertools.product(values, repeat=3):
            configurations += 1
            total_dissipation = defect + high + low
            if total_dissipation < terminal / 2:
                continue
            eligible += 1
            if defect >= terminal / 8:
                branch = "defect"
            elif high >= terminal / 8:
                branch = "high"
            else:
                branch = "low"
            class_counts[branch] += 1

            conditions = {
                "priority_exhaustive": branch in class_counts,
                "defect_threshold": (
                    branch != "defect" or defect >= terminal / 8
                ),
                "high_threshold_and_no_defect": (
                    branch != "high"
                    or (defect < terminal / 8 and high >= terminal / 8)
                ),
                "low_two_strict_failures": (
                    branch != "low"
                    or (defect < terminal / 8 and high < terminal / 8)
                ),
                "low_viscous_mass_gt_quarter": (
                    branch != "low" or low > terminal / 4
                ),
                "defect_residual_factor_eight": (
                    branch != "defect" or terminal <= 8 * defect
                ),
                "high_residual_factor_eight": (
                    branch != "high" or terminal <= 8 * high
                ),
            }
            if not all(conditions.values()) and len(failures) < 20:
                failures.append(
                    {
                        "T": fs(terminal),
                        "defect": fs(defect),
                        "high": fs(high),
                        "low": fs(low),
                        "D": fs(total_dissipation),
                        "branch": branch,
                        "conditions": conditions,
                    }
                )

    return {
        "id": "exact_rational_priority_trichotomy",
        "grid_denominator": denominator,
        "configurations_checked": configurations,
        "dissipation_branch_configurations": eligible,
        "class_counts": class_counts,
        "failures": failures,
        "pass": not failures and sum(class_counts.values()) == eligible,
    }


def low_mass_enumeration() -> dict:
    """Check G>T/4 and G<=2 lambda E imply E>T/(8 lambda)."""
    failures: list[dict] = []
    configurations = 0
    minimum_margin: Fraction | None = None
    terminals = [Fraction(1, 2), Fraction(1), Fraction(2), Fraction(3)]
    lambdas = [
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(1),
        Fraction(2),
        Fraction(4),
    ]

    for terminal, lam, g_step, slack_step in itertools.product(
        terminals, lambdas, range(1, 9), range(5)
    ):
        viscous_mass = terminal / 4 + terminal * Fraction(g_step, 32)
        kinetic_mass = (
            viscous_mass / (2 * lam)
            + terminal * Fraction(slack_step, 64) / lam
        )
        configurations += 1
        target = terminal / (8 * lam)
        margin = kinetic_mass - target
        if minimum_margin is None or margin < minimum_margin:
            minimum_margin = margin
        conditions = {
            "strict_quarter_input": viscous_mass > terminal / 4,
            "factor_two_relation": viscous_mass <= 2 * lam * kinetic_mass,
            "strict_kinetic_mass_output": kinetic_mass > target,
        }
        if not all(conditions.values()) and len(failures) < 20:
            failures.append(
                {
                    "T": fs(terminal),
                    "lambda": fs(lam),
                    "G_low": fs(viscous_mass),
                    "E_normalized": fs(kinetic_mass),
                    "target": fs(target),
                    "conditions": conditions,
                }
            )

    return {
        "id": "exact_rational_low_rayleigh_mass_implication",
        "configurations_checked": configurations,
        "minimum_strict_margin": fs(minimum_margin or Fraction(0)),
        "failures": failures,
        "pass": not failures,
    }


def direct_low_set_boundary_check() -> dict:
    """Check the direct low-set definition at eta=0 and at zero rows.

    The Sobolev fact that a vanishing weighted kinetic denominator forces
    the weak gradient to vanish on the open positive-cutoff set is analytic
    and is not machine-proved here.  This check starts from the resulting
    row condition U=G=0 and verifies the direct algebraic boundary.
    """
    failures: list[dict] = []
    rows = []
    positive_values = [
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(1),
        Fraction(2),
    ]

    # eta=0: the direct rows vanish even when raw U and G are arbitrary.
    for radius, gamma, lam, kinetic_raw, gradient_raw in itertools.product(
        positive_values,
        positive_values,
        positive_values,
        [Fraction(0), Fraction(1, 3), Fraction(2)],
        [Fraction(0), Fraction(1, 5), Fraction(3)],
    ):
        eta = Fraction(0)
        energy = gamma * eta * kinetic_raw / (2 * radius)
        dissipation = gamma * eta * gradient_raw / radius
        low_member = dissipation <= 2 * lam * energy / radius**2
        row = {
            "case": "eta_zero",
            "R": fs(radius),
            "gamma": fs(gamma),
            "lambda": fs(lam),
            "raw_U": fs(kinetic_raw),
            "raw_G": fs(gradient_raw),
            "e": fs(energy),
            "g": fs(dissipation),
            "direct_L_member": low_member,
            "pass": energy == 0 and dissipation == 0 and low_member,
        }
        rows.append(row)
        if not row["pass"] and len(failures) < 20:
            failures.append(row)

    # Zero denominator after the analytic U=0 => G=0 input from the note.
    for radius, gamma, lam, eta in itertools.product(
        positive_values,
        positive_values,
        positive_values,
        [Fraction(0), Fraction(1)],
    ):
        kinetic_raw = Fraction(0)
        gradient_raw = Fraction(0)
        energy = gamma * eta * kinetic_raw / (2 * radius)
        dissipation = gamma * eta * gradient_raw / radius
        low_member = dissipation <= 2 * lam * energy / radius**2
        row = {
            "case": "zero_denominator_and_zero_gradient_row",
            "R": fs(radius),
            "gamma": fs(gamma),
            "lambda": fs(lam),
            "eta": fs(eta),
            "e": fs(energy),
            "g": fs(dissipation),
            "direct_L_member": low_member,
            "pass": energy == 0 and dissipation == 0 and low_member,
        }
        rows.append(row)
        if not row["pass"] and len(failures) < 20:
            failures.append(row)

    return {
        "id": "direct_low_set_eta_zero_and_zero_denominator_boundaries",
        "configurations_checked": len(rows),
        "eta_zero_configurations": sum(
            row["case"] == "eta_zero" for row in rows
        ),
        "zero_denominator_configurations": sum(
            row["case"] == "zero_denominator_and_zero_gradient_row"
            for row in rows
        ),
        "analytic_zero_denominator_gradient_implication_machine_proved": False,
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def jensen_enumeration() -> dict:
    """Enumerate rational step functions with square-valued energy levels."""
    failures: list[dict] = []
    configurations = 0
    strict_combined_checks = 0
    equality_cases = 0
    weights = [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)]
    levels = [0, 1, 2, 3]

    for length in range(1, 5):
        for cell_weights in itertools.product(weights, repeat=length):
            delta = sum(cell_weights, Fraction(0))
            for roots in itertools.product(levels, repeat=length):
                if not any(roots):
                    continue
                kinetic_mass = sum(
                    (weight * root * root for weight, root in zip(cell_weights, roots)),
                    Fraction(0),
                )
                three_halves_mass = sum(
                    (weight * root**3 for weight, root in zip(cell_weights, roots)),
                    Fraction(0),
                )
                configurations += 1
                jensen_left = delta * three_halves_mass**2
                jensen_right = kinetic_mass**3
                four_interval_left = 4 * three_halves_mass**2
                if jensen_left == jensen_right:
                    equality_cases += 1

                # Couple the strict mass step without introducing radicals:
                # choose a rational B<E and compare 4 J^2 > B^3.
                lower_mass_target = max(
                    Fraction(0), kinetic_mass - Fraction(1, 64)
                )
                combined = four_interval_left > lower_mass_target**3
                strict_combined_checks += 1
                conditions = {
                    "delta_at_most_four": delta <= 4,
                    "jensen_squared": jensen_left >= jensen_right,
                    "four_R2_constant_squared": four_interval_left >= jensen_right,
                    "strict_low_mass_combination": combined,
                }
                if not all(conditions.values()) and len(failures) < 20:
                    failures.append(
                        {
                            "weights": [fs(item) for item in cell_weights],
                            "square_roots": list(roots),
                            "delta": fs(delta),
                            "E": fs(kinetic_mass),
                            "J": fs(three_halves_mass),
                            "conditions": conditions,
                        }
                    )

    return {
        "id": "exact_rational_step_function_jensen_delta_at_most_four",
        "configurations_checked": configurations,
        "strict_low_mass_combinations_checked": strict_combined_checks,
        "jensen_equality_cases": equality_cases,
        "failures": failures,
        "pass": not failures and equality_cases > 0,
    }


def holder_enumeration() -> dict:
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
                left_sum = sum(
                    Fraction(a * q * q)
                    for a, q in zip(coefficients, cube_roots)
                )
                coefficient_cube_sum = sum(
                    (Fraction(a**3) for a in coefficients), Fraction(0)
                )
                payment_sum = sum(
                    (Fraction(q**3) for q in cube_roots), Fraction(0)
                )
                left = left_sum**3
                right = coefficient_cube_sum * payment_sum**2
                if left == right:
                    equality_cases += 1
                if left > right and len(failures) < 20:
                    failures.append(
                        {
                            "a": list(coefficients),
                            "payment_cube_roots": list(cube_roots),
                            "left": fs(left),
                            "right": fs(right),
                        }
                    )

    return {
        "id": "exact_rational_cross_shell_holder",
        "configurations_checked": configurations,
        "holder_equality_cases": equality_cases,
        "failures": failures,
        "pass": not failures and equality_cases > 0,
    }


def constant_profile_tail_check() -> dict:
    """Verify a rational sufficient tail comparison for lambda_k=1."""
    rows = []
    failures = []
    for shell in range(4, 33):
        exponent_gap = Fraction(3 * 4 ** (shell - 1), 32)
        exp_lower = 1 + exponent_gap + exponent_gap**2 / 2
        conditions = {
            "gap_at_least_six": exponent_gap >= 6,
            "elementary_exp_lower_bound_exceeds_sixteen": exp_lower > 16,
            "ratio_strictly_below_one_half": exp_lower > 16,
        }
        row = {
            "k": shell,
            "ratio": "8*exp(-3*4^(k-1)/32)",
            "exponent_gap": fs(exponent_gap),
            "1_plus_x_plus_x2_over_2": fs(exp_lower),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)

    return {
        "id": "constant_lambda_super_gaussian_geometric_tail",
        "tail_starts_at_shell": 4,
        "tail_ratios_checked": len(rows),
        "comparison_ratio_upper_bound": "1/2 (strict)",
        "symbolic_tail_invariant": (
            "x_4=6 and x_(k+1)=4*x_k, hence x_k>=6 for every k>=4"
        ),
        "proof_device": "exp(x)>=1+x+x^2/2, checked with exact rationals",
        "rows": rows,
        "failures": failures,
        "pass": not failures,
    }


def profile_boundary_check() -> dict:
    """Verify canonical epsilon=1 and critical coefficient ledgers."""
    rows = []
    failures = []
    canonical_partial = Fraction(0)
    critical_partial = Fraction(0)
    for shell in range(1, 65):
        canonical_two_exponent = 3 * shell + 3 * (-2 * shell)
        canonical_gamma_exponent = Fraction(1) + 3 * Fraction(-1, 3)
        canonical_coefficient = Fraction(1, 2 ** (3 * shell))
        canonical_partial += canonical_coefficient

        critical_two_exponent = 3 * shell + 3 * (-shell)
        critical_gamma_exponent = Fraction(1) + 3 * Fraction(-1, 3)
        critical_coefficient = Fraction(1)
        critical_partial += critical_coefficient
        conditions = {
            "canonical_two_exponent": canonical_two_exponent == -3 * shell,
            "canonical_gamma_cancels": canonical_gamma_exponent == 0,
            "canonical_coefficient": canonical_coefficient
            == Fraction(1, 2 ** (3 * shell)),
            "critical_two_cancels": critical_two_exponent == 0,
            "critical_gamma_cancels": critical_gamma_exponent == 0,
            "critical_coefficient_one": critical_coefficient == 1,
            "critical_partial_sum_grows": critical_partial == shell,
        }
        row = {
            "k": shell,
            "canonical_coefficient": fs(canonical_coefficient),
            "canonical_partial_sum": fs(canonical_partial),
            "critical_coefficient": fs(critical_coefficient),
            "critical_partial_sum": fs(critical_partial),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)

    infinite_sum = Fraction(1, 8) / (1 - Fraction(1, 8))
    return {
        "id": "canonical_one_seventh_and_critical_boundary",
        "shells_checked": len(rows),
        "canonical_profile": "lambda_k=2^(-2k)*gamma_k^(-1/3)",
        "canonical_infinite_coefficient_sum": fs(infinite_sum),
        "critical_profile": "lambda_k=2^(-k)*gamma_k^(-1/3)",
        "critical_partial_sum_at_64": fs(critical_partial),
        "rows": rows,
        "failures": failures,
        "pass": not failures and infinite_sum == Fraction(1, 7),
    }


def near_critical_exact_sum_check() -> dict:
    """Check the near-critical geometric sum for epsilon=n/3 exactly."""
    rows = []
    failures = []
    for numerator in range(1, 10):
        epsilon = Fraction(numerator, 3)
        ratio = Fraction(1, 2**numerator)
        infinite_sum = ratio / (1 - ratio)
        partial_sum = sum(
            (ratio**shell for shell in range(1, 65)), Fraction(0)
        )
        exact_tail = ratio**65 / (1 - ratio)
        conditions = {
            "ratio_is_two_to_minus_three_epsilon": 3 * epsilon == numerator,
            "geometric_identity": partial_sum + exact_tail == infinite_sum,
            "positive_ratio_below_one": 0 < ratio < 1,
            "epsilon_one_gives_one_seventh": (
                epsilon != 1 or infinite_sum == Fraction(1, 7)
            ),
        }
        row = {
            "epsilon": fs(epsilon),
            "ratio_2_to_minus_3epsilon": fs(ratio),
            "partial_sum_1_through_64": fs(partial_sum),
            "tail_after_64": fs(exact_tail),
            "infinite_sum": fs(infinite_sum),
            "conditions": conditions,
            "pass": all(conditions.values()),
        }
        rows.append(row)
        if not row["pass"]:
            failures.append(row)
    return {
        "id": "near_critical_profile_exact_geometric_sums",
        "epsilon_values_checked": len(rows),
        "epsilon_grid": "n/3 for n=1,...,9",
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
    "the machine certificate proves (R.214)",
    "the machine certificate proves (R.211)",
    "the certificate proves the Navier--Stokes PDE theorem",
    "the Navier--Stokes Millennium problem is solved",
    "global regularity is proved",
    "the high-Rayleigh class is closed",
    "the anomalous-defect class is closed",
)


def forbidden_claims(body: str) -> list[str]:
    lowered = body.lower()
    return [phrase for phrase in FORBIDDEN_CLAIMS if phrase.lower() in lowered]


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.(\d+)\}", body)
    expected = [str(value) for value in range(142, 163)]
    compressed = compact(body)
    prose = re.sub(r"\s+", " ", body)
    checks = [
        {
            "id": "tags_consecutive_S142_through_S162",
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
    ]

    required_text = (
        "one-eighth/one-eighth/one-quarter trichotomy",
        "The remaining high-Rayleigh and anomalous-defect classes are **OPEN**.",
        "it is not asserted to be a sharp Fourier localization",
        "not a positive lower bound for the Lebesgue measure of a time set",
        "Fix measurable representatives of these rows, setting both to zero on their common exceptional null set.",
        "The primary definition uses only the measurable rows in (S.142)",
        "membership in \(L_{k,R}\) is equivalently expressed through the",
        "No zero-over-zero convention is needed.",
        "Thin time support is favorable in this inequality",
        "The endpoint energy",
        "may be zero and is not used.",
        "This is a **PROVED CONDITIONAL IMPLICATION**, not a finite-exception theorem.",
        "The high-Rayleigh alternative cannot simply be deleted.",
        "high-Rayleigh time set \(H_{k,R}\) at every active time with \(\eta_R(t)>0\)",
        "the high-Rayleigh time set can be nonempty",
        "The following are **PROVED**:",
        "The following are **INHERITED**:",
        "The following remain **OPEN**:",
        "The following are **NOT CLAIMED**:",
        "the padded-shell Hölder estimate (R.214) and shell-dependent payment",
        "bound (R.211) from R0.74R",
        "absence of anomalous local-energy defect for suitable weak solutions",
        "**NOT CLAY.**",
    )
    required_formula = (
        "D_{k,R}(\\tau)=\\int_{s_R}^{\\tau}g_{k,R}(t)dt+m_{k,R}(\\tau)",
        "L_{k,R}:={\\left\\{t\\in(s_R,\\tau):g_{k,R}(t)\\le{2\\lambda_k\\overR^2}e_{k,R}(t)\\right\\}}",
        "\\eta_R(t)>0,\\quad\\int_{\\mathbbT^3}\\Psi_k^R|v_R|^2>0",
        "t\\inL_{k,R}\\quad\\Longleftrightarrow\\quad\\rho_{k,R}(t)\\le\\lambda_k",
        "1_{L_{k,R}}(t)g_{k,R}(t)\\le{2\\lambda_k\\overR^2}1_{L_{k,R}}(t)e_{k,R}(t)",
        "\\int_{L_{k,R}}g_{k,R}(t)dt=D_{k,R}(\\tau)-m_{k,R}(\\tau)-\\int_{H_{k,R}}g_{k,R}(t)dt>\\frac14T_k",
        "{1\\overR^2}\\int_{L_{k,R}}e_{k,R}(t)dt>{T_k\\over8\\lambda_k}",
        ">{1\\over2}\\left({T_k\\over8\\lambda_k}\\right)^{3/2}",
        "T_k\\leC_2\\lambda_k2^k\\gamma_k^{1/3}(p_{k,R}^{\\rmlo})^{2/3}",
        "\\mathscrL(\\boldsymbol\\lambda):=\\sum_{k\\ge1}2^{3k}\\gamma_k\\lambda_k^3",
        "\\sum_{k\\in\\mathcalI_{\\rmlo}(\\tau)}K_{k,R}(\\tau)\\leC_2\\mathscrL(\\boldsymbol\\lambda)^{1/3}",
        "{a_{k+1}\\overa_k}=8\\exp\\!\\left(-{3\\cdot4^{k-1}\\over32}\\right)",
        "\\lambda_k^{(\\varepsilon)}:=2^{-(1+\\varepsilon)k}\\gamma_k^{-1/3}",
        "\\mathscrL(\\boldsymbol\\lambda^{(\\varepsilon)})=\\sum_{k\\ge1}2^{-3\\varepsilon k}={2^{-3\\varepsilon}\\over1-2^{-3\\varepsilon}}",
        "\\lambda_k^{\\rmcrit}:=2^{-k}\\gamma_k^{-1/3}",
        "2^{3k}\\gamma_k(\\lambda_k^{\\rmcrit})^3=1",
        "+8\\sum_{k\\in\\mathcalI_{\\rmdef}(\\tau)}m_{k,R}(\\tau)",
        "+8\\sum_{k\\in\\mathcalI_{\\rmhi}(\\tau)}\\int_{H_{k,R}}g_{k,R}(t)dt",
        "{\\rho_{k,R}^{(N)}\\overR^2N^2}\\longrightarrow1",
        "p_N=0,\\qquadA\\ne0,\\quadN\\in\\mathbbN",
    )

    for sentinel in required_text:
        checks.append(
            {
                "id": "required_text_"
                + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in prose,
            }
        )
    for sentinel in required_formula:
        normalized_sentinel = compact(sentinel)
        checks.append(
            {
                "id": "required_formula_"
                + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": normalized_sentinel in compressed,
            }
        )
    for phrase in FORBIDDEN_CLAIMS:
        checks.append(
            {
                "id": "forbidden_"
                + hashlib.sha256(phrase.encode()).hexdigest()[:12],
                "sentinel": phrase,
                "pass": phrase.lower() not in body.lower(),
            }
        )
    return checks


def negative_mutation_checks(body: str) -> list[dict]:
    rows: list[dict] = []

    terminal = Fraction(1)
    defect = Fraction(3, 16)
    high = Fraction(3, 16)
    low = Fraction(1, 8)
    mutated_cutoff = Fraction(1, 4)
    mutated_low = defect < mutated_cutoff and high < mutated_cutoff
    rows.append(
        {
            "id": "mutation_threshold_eighth_to_quarter",
            "fixture": {
                "T": fs(terminal),
                "defect": fs(defect),
                "high": fs(high),
                "low": fs(low),
                "D": fs(defect + high + low),
            },
            "mutation_result": "incorrectly_low" if mutated_low else "not_low",
            "counterexample": mutated_low and low <= terminal / 4,
            "pass": mutated_low and low <= terminal / 4,
        }
    )

    terminal = Fraction(1)
    lam = Fraction(1)
    kinetic_mass = Fraction(1, 6)
    viscous_mass = Fraction(1, 3)
    rows.append(
        {
            "id": "mutation_drop_g_over_e_factor_two",
            "fixture": {
                "T": fs(terminal),
                "lambda": fs(lam),
                "E_normalized": fs(kinetic_mass),
                "G_low": fs(viscous_mass),
            },
            "correct_relation": viscous_mass == 2 * lam * kinetic_mass,
            "correct_output": kinetic_mass > terminal / (8 * lam),
            "mutated_output_E_gt_T_over_4lambda": kinetic_mass
            > terminal / (4 * lam),
            "pass": (
                viscous_mass == 2 * lam * kinetic_mass
                and kinetic_mass > terminal / (8 * lam)
                and not kinetic_mass > terminal / (4 * lam)
            ),
        }
    )

    # If rho were used at eta=0, it could disagree with the direct row
    # definition: the rows vanish and are low, while the raw quotient is high.
    eta = Fraction(0)
    radius = gamma = lam = kinetic_raw = Fraction(1)
    gradient_raw = Fraction(100)
    energy = gamma * eta * kinetic_raw / (2 * radius)
    dissipation = gamma * eta * gradient_raw / radius
    direct_low = dissipation <= 2 * lam * energy / radius**2
    raw_rho = radius**2 * gradient_raw / kinetic_raw
    mutated_quotient_low = raw_rho <= lam
    rows.append(
        {
            "id": "mutation_extend_rho_equivalence_to_eta_zero",
            "direct_e": fs(energy),
            "direct_g": fs(dissipation),
            "raw_rho": fs(raw_rho),
            "direct_L_member": direct_low,
            "mutated_quotient_L_member": mutated_quotient_low,
            "pass": direct_low and not mutated_quotient_low,
        }
    )

    delta = Fraction(2)
    kinetic_mass = Fraction(5)
    three_halves_mass = Fraction(9)
    correct_left = delta * three_halves_mass**2
    right = kinetic_mass**3
    rows.append(
        {
            "id": "mutation_reverse_jensen_direction",
            "fixture": "two unit cells with energy roots 1 and 2",
            "delta_J_squared": fs(correct_left),
            "E_cubed": fs(right),
            "correct_direction": correct_left >= right,
            "mutated_reverse_direction": correct_left <= right,
            "pass": correct_left > right,
        }
    )

    delta = Fraction(4)
    kinetic_mass = Fraction(4)
    three_halves_mass = Fraction(4)
    rows.append(
        {
            "id": "mutation_replace_jensen_half_by_one",
            "fixture": "constant unit energy on normalized length four",
            "J": fs(three_halves_mass),
            "half_E_three_halves_squared_test": 4 * three_halves_mass**2
            >= kinetic_mass**3,
            "mutated_one_E_three_halves_squared_test": three_halves_mass**2
            >= kinetic_mass**3,
            "pass": (
                4 * three_halves_mass**2 == kinetic_mass**3
                and three_halves_mass**2 < kinetic_mass**3
            ),
        }
    )

    gamma = Fraction(1, 64)
    correct_gamma_factor = Fraction(1, 4)
    mutated_gamma_factor = Fraction(1, 16)
    terminal_value = correct_gamma_factor
    rows.append(
        {
            "id": "mutation_gamma_exponent_one_third_to_two_thirds",
            "fixture_gamma": fs(gamma),
            "correct_gamma_one_third": fs(correct_gamma_factor),
            "mutated_gamma_two_thirds": fs(mutated_gamma_factor),
            "equality_fixture_T": fs(terminal_value),
            "pass": (
                correct_gamma_factor**3 == gamma
                and mutated_gamma_factor**3 == gamma**2
                and terminal_value > mutated_gamma_factor
            ),
        }
    )

    critical_partial = Fraction(64)
    rows.append(
        {
            "id": "mutation_declare_critical_lambda_summable",
            "critical_coefficients_checked": 64,
            "critical_partial_sum": fs(critical_partial),
            "mutated_uniform_bound": fs(Fraction(1, 7)),
            "pass": critical_partial > Fraction(1, 7),
        }
    )

    terminal = Fraction(1)
    residual = Fraction(1, 8)
    rows.append(
        {
            "id": "mutation_residual_factor_eight_to_four",
            "T": fs(terminal),
            "one_eighth_residual": fs(residual),
            "correct_eight_payment": fs(8 * residual),
            "mutated_four_payment": fs(4 * residual),
            "pass": terminal <= 8 * residual and terminal > 4 * residual,
        }
    )

    mutated_body = body + "\n" + "\n".join(
        (
            "The machine certificate proves (R.214).",
            "The machine certificate proves (R.211).",
            "The certificate proves the Navier--Stokes PDE theorem.",
            "The Navier--Stokes Millennium problem is solved.",
        )
    )
    detected = forbidden_claims(mutated_body)
    rows.append(
        {
            "id": "mutation_promote_finite_checks_to_analytic_PDE_Clay_claims",
            "forbidden_claims_injected": 4,
            "forbidden_claims_detected": detected,
            "pass": len(detected) == 4,
        }
    )
    return rows


def render_report(data: dict, json_hash: str) -> str:
    summary = data["summary"]
    finite_by_id = {row["id"]: row for row in data["finite_checks"]}
    trichotomy = finite_by_id["exact_rational_priority_trichotomy"]
    low_mass = finite_by_id["exact_rational_low_rayleigh_mass_implication"]
    direct_boundary = finite_by_id[
        "direct_low_set_eta_zero_and_zero_denominator_boundaries"
    ]
    jensen = finite_by_id[
        "exact_rational_step_function_jensen_delta_at_most_four"
    ]
    holder = finite_by_id["exact_rational_cross_shell_holder"]
    constant = finite_by_id["constant_lambda_super_gaussian_geometric_tail"]
    profiles = finite_by_id["canonical_one_seventh_and_critical_boundary"]
    near_critical = finite_by_id["near_critical_profile_exact_geometric_sums"]

    exact_rows = "\n".join(
        f"| {row['id']} | {row['left']} | {row['right']} | {row['margin']} |"
        for row in data["exact_checks"]
    )
    mutation_rows = "\n".join(
        f"- `{row['id']}`: {'rejected' if row['pass'] else 'NOT REJECTED'}."
        for row in data["negative_mutations"]
    )
    return f"""# R0.74S low-Rayleigh dissipation certificate report

## Result

**PASS** — {summary['exact_passed']}/{summary['exact_total']} exact algebra rows,
{summary['finite_passed']}/{summary['finite_total']} finite checks,
{summary['structural_passed']}/{summary['structural_total']} structural checks,
and {summary['negative_mutations_passed']}/{summary['negative_mutations_total']} negative
mutations passed.

## Exact algebra

| Check | Left | Right | Margin |
|---|---:|---:|---:|
{exact_rows}

## Finite rational checks

- The priority trichotomy passes {trichotomy['dissipation_branch_configurations']}
  eligible exact rational splits out of {trichotomy['configurations_checked']}
  grid configurations.  Its class counts are
  defect={trichotomy['class_counts']['defect']},
  high={trichotomy['class_counts']['high']}, and
  low={trichotomy['class_counts']['low']}.
- The low-Rayleigh mass implication passes
  {low_mass['configurations_checked']} exact rational fixtures, including the
  normalization factor two and the strict `T/(8 lambda)` conclusion.
- The direct definition of `L` passes {direct_boundary['configurations_checked']}
  eta-zero and zero-row boundary fixtures.  The analytic weak-gradient fact
  used to reach the zero row from a zero weighted denominator is explicitly
  outside this machine check.
- Jensen passes {jensen['configurations_checked']} rational step functions on
  normalized lengths at most four, with {jensen['jensen_equality_cases']}
  equality cases retained.  The square-valued energy levels make every
  comparison exact and radical-free.
- Cross-shell Hölder passes {holder['configurations_checked']} exact rational
  coefficient/payment fixtures, with {holder['holder_equality_cases']}
  equality cases.
- For `lambda_k=1`, the exact base `x_4=6` and recurrence
  `x_(k+1)=4x_k` give a strict geometric ratio below `1/2` from shell four;
  {constant['tail_ratios_checked']} exact rational rows check the ledger.
  This uses `exp(x) >= 1+x+x^2/2` only as the displayed elementary comparison.
- For `lambda_k=2^(-2k) gamma_k^(-1/3)`, the coefficient ledger is
  `2^(-3k)` and its exact infinite geometric sum is
  `{profiles['canonical_infinite_coefficient_sum']}`.  The critical profile
  has unit coefficients and partial sum
  `{profiles['critical_partial_sum_at_64']}` at shell 64.
- The general near-critical geometric formula passes
  {near_critical['epsilon_values_checked']} exact epsilon values on the grid
  `epsilon=n/3`, including the canonical `epsilon=1` sum `1/7`.

## Negative mutations

{mutation_rows}

## Reproducibility

- Source note SHA-256: `{data['source']['note_sha256']}`
- Generator SHA-256: `{data['source']['generator_sha256']}`
- JSON payload SHA-256: `{json_hash}`
- The output contains no timestamp, random seed, floating-point calculation,
  network input, or non-standard Python dependency.
- Set `R074S_DISSIPATION_NOTE`, `R074S_DISSIPATION_JSON`, and
  `R074S_DISSIPATION_REPORT` to rebuild against explicit paths.

## Boundary

This is a finite/algebraic certificate.  It checks rational threshold
arithmetic, finite rational step functions, exponent bookkeeping, elementary
sequence comparisons, and statement integrity.  It does **not** machine-prove
the inherited padded-shell Hölder estimate (R.214), the shell-dependent
payment theorem (R.211), their analytic hypotheses, any Navier--Stokes PDE
claim, regularity, or the Millennium problem.

**FINITE/ALGEBRAIC ONLY.  INHERITED ANALYSIS NOT MACHINE-PROVED.  NOT CLAY.**
"""


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = exact_ledger()
    finite_checks = [
        trichotomy_enumeration(),
        low_mass_enumeration(),
        direct_low_set_boundary_check(),
        jensen_enumeration(),
        holder_enumeration(),
        constant_profile_tail_check(),
        profile_boundary_check(),
        near_critical_exact_sum_check(),
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

    data = {
        "schema": "r074s-dissipation-rayleigh-certificate-v1",
        "scope": {
            "finite_algebraic_only": True,
            "machine_proves_R214": False,
            "machine_proves_R211": False,
            "machine_proves_Navier_Stokes_PDE": False,
            "machine_proves_zero_denominator_weak_gradient_fact": False,
            "machine_proves_regularity_or_Clay": False,
        },
        "source": {
            "note": str(NOTE.relative_to(REPO))
            if NOTE.is_relative_to(REPO)
            else str(NOTE),
            "note_sha256": sha256(NOTE),
            "generator": str(Path(__file__).resolve().relative_to(REPO)),
            "generator_sha256": sha256(Path(__file__).resolve()),
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
    REPORT_OUT.write_text(
        render_report(data, sha256_bytes(payload)), encoding="utf-8"
    )

    print(
        "R0.74S low-Rayleigh certificate: "
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
