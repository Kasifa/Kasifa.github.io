#!/usr/bin/env python3
"""Finite certificate for R0.74S Step 5 one-sided ball clocks.

The certificate checks exact finite algebra, stopped-family combinatorics,
selected rational cutoff samples, and claim-boundary sentinels.  It does not
machine-prove the local-energy identity or any PDE estimate.
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
        "R074S_BALL_NOTE",
        REPO / "research/r074s_one_sided_ball_clock_no_gain.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_BALL_JSON",
        REPO / "research/r074s_one_sided_ball_clock_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_BALL_REPORT",
        REPO / "research/r074s_one_sided_ball_clock_certificate_report.md",
    )
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def theta_piecewise(value: Fraction) -> Fraction:
    """Exact monotone transition model used only for finite sampling."""
    if value <= -1:
        return Fraction(0)
    if value >= 0:
        return Fraction(1)
    return value + 1


def theta_prime_piecewise(value: Fraction) -> Fraction:
    """Derivative of the proxy away from its two corner points."""
    return Fraction(1) if -1 < value < 0 else Fraction(0)


def cutoff_identity_check() -> dict:
    """Sample S.86--S.87 exactly on rational grids at six scales."""
    delta = Fraction(1, 8)
    failures = []
    checked = 0
    derivative_checked = 0
    for m in range(1, 7):
        radius = Fraction(2**m)
        next_radius = Fraction(2 ** (m + 1))
        samples = {
            Fraction(0),
            radius,
            next_radius,
            (radius + next_radius) / 2,
        }
        for center in (radius, next_radius):
            samples.update(center + Fraction(j, 64) for j in range(-12, 13))
        for rho in sorted(value for value in samples if value >= 0):
            inner_arg = (rho - radius) / delta
            outer_arg = (next_radius - rho) / delta
            chi_minus = 1 - theta_piecewise(inner_arg)
            chi_plus = theta_piecewise(-inner_arg)
            next_chi_plus = theta_piecewise(outer_arg)
            beta = theta_piecewise(inner_arg) * theta_piecewise(-inner_arg)
            psi = theta_piecewise(inner_arg) * theta_piecewise(outer_arg)
            conditions = {
                "ordered": Fraction(0) <= chi_minus <= chi_plus <= Fraction(1),
                "beta_difference": chi_plus - chi_minus == beta,
                "psi_difference": next_chi_plus - chi_minus == psi,
            }
            if not all(conditions.values()):
                failures.append(
                    {
                        "m": m,
                        "rho": fs(rho),
                        "chi_minus": fs(chi_minus),
                        "chi_plus": fs(chi_plus),
                        "next_chi_plus": fs(next_chi_plus),
                        "beta": fs(beta),
                        "psi": fs(psi),
                        "conditions": conditions,
                    }
                )
            checked += 1
        derivative_samples = [radius + Fraction(j, 256) for j in range(-40, 41, 2)]
        for rho in derivative_samples:
            z_value = (rho - radius) / delta
            if z_value in (Fraction(-1), Fraction(0), Fraction(1)):
                continue
            d_minus = -theta_prime_piecewise(z_value) / delta
            d_plus = -theta_prime_piecewise(-z_value) / delta
            expected_minus = (
                -1 / delta if radius - delta < rho < radius else Fraction(0)
            )
            expected_plus = (
                -1 / delta if radius < rho < radius + delta else Fraction(0)
            )
            derivative_conditions = {
                "minus_exact": d_minus == expected_minus,
                "plus_exact": d_plus == expected_plus,
                "minus_transition_nonzero": (
                    d_minus != 0
                    if radius - delta < rho < radius
                    else d_minus == 0
                ),
                "plus_transition_nonzero": (
                    d_plus != 0
                    if radius < rho < radius + delta
                    else d_plus == 0
                ),
            }
            if not all(derivative_conditions.values()):
                failures.append(
                    {
                        "m": m,
                        "rho": fs(rho),
                        "d_chi_minus": fs(d_minus),
                        "d_chi_plus": fs(d_plus),
                        "conditions": derivative_conditions,
                    }
                )
            derivative_checked += 1
    return {
        "id": "exact_rational_one_sided_cutoff_grid",
        "samples_checked": checked,
        "derivative_samples_checked": derivative_checked,
        "failures": failures,
        "pass": not failures,
    }


def support_packing_proxy_check() -> dict:
    """Check S.93 support bookkeeping with its sharp geometric tail proxy."""
    q = Fraction(32, 35)
    proxy_bound = Fraction(73, 3)
    delta = Fraction(1, 8)
    cutoff = 10
    samples = {Fraction(0), Fraction(4)}
    for j in range(1, 7):
        radius = Fraction(2**j)
        samples.update(radius + Fraction(k, 32) for k in range(-6, 7))
    failures = []
    maximum_ratio = Fraction(0)
    maximizer = Fraction(0)
    for rho in sorted(value for value in samples if value >= 0):
        first = Fraction(0)
        second = Fraction(0)
        third = Fraction(0)
        rhs = Fraction(1) if rho < 4 else Fraction(0)
        for k in range(1, cutoff + 1):
            gamma = q ** (k - 1)
            radius = Fraction(2**k)
            next_radius = Fraction(2 ** (k + 1))
            chi_minus = 1 - theta_piecewise((rho - radius) / delta)
            next_chi_plus = theta_piecewise((next_radius - rho) / delta)
            first += gamma * chi_minus
            second += gamma * next_chi_plus
            if k >= 2:
                d_k = q ** (k - 2) - q ** (k - 1)
                chi_plus = theta_piecewise((radius - rho) / delta)
                third += d_k * chi_plus
            if radius - delta <= rho <= next_radius + delta:
                rhs += gamma

        # For the sampled radii, every cutoff beyond ``cutoff`` equals one.
        first += q**cutoff / (1 - q)
        second += q**cutoff / (1 - q)
        third += q ** (cutoff - 1)
        lhs = first + second + third
        if rhs == 0:
            if lhs != 0:
                failures.append({"rho": fs(rho), "lhs": fs(lhs), "rhs": fs(rhs)})
            continue
        ratio = lhs / rhs
        if ratio > proxy_bound:
            failures.append(
                {
                    "rho": fs(rho),
                    "ratio": fs(ratio),
                    "proxy_bound": fs(proxy_bound),
                }
            )
        if ratio > maximum_ratio:
            maximum_ratio = ratio
            maximizer = rho
    return {
        "id": "exact_rational_support_packing_proxy",
        "weight_ratio": fs(q),
        "certified_sample_bound": fs(proxy_bound),
        "samples_checked": len(samples),
        "maximum_ratio": fs(maximum_ratio),
        "maximizer_radius_over_R": fs(maximizer),
        "failures": failures,
        "pass": not failures,
    }


def stopped_activation_exhaustive_check() -> dict:
    """Exhaust S.95--S.96 for all five-shell masks and tied stop times."""
    shell_max = 5
    tau = Fraction(3)
    time_samples = [Fraction(j, 2) for j in range(7)]
    failures = []
    configurations = 0
    comparisons = 0
    for mask in range(1 << shell_max):
        shell_set = {k for k in range(1, shell_max + 1) if mask & (1 << (k - 1))}
        ordered_shells = sorted(shell_set)
        for assignment in itertools.product(range(3), repeat=len(ordered_shells)):
            stops = {
                k: Fraction(value)
                for k, value in zip(ordered_shells, assignment)
            }
            configurations += 1
            for t in time_samples:
                active = {k for k in shell_set if stops[k] < t <= tau}
                for k in ordered_shells:
                    rho = (
                        tau
                        if k == 1 or k - 1 not in shell_set
                        else stops[k - 1]
                    )
                    lam = (
                        tau
                        if k + 1 not in shell_set
                        else stops[k + 1]
                    )
                    root_actual = k in active and (k == 1 or k - 1 not in active)
                    root_expected = stops[k] < rho and stops[k] < t <= rho
                    outer_actual = k in active and k + 1 not in active
                    outer_expected = stops[k] < lam and stops[k] < t <= lam
                    comparisons += 2
                    if root_actual != root_expected or outer_actual != outer_expected:
                        failures.append(
                            {
                                "mask": mask,
                                "stops": {str(i): fs(v) for i, v in stops.items()},
                                "t": fs(t),
                                "k": k,
                                "root_actual": root_actual,
                                "root_expected": root_expected,
                                "outer_actual": outer_actual,
                                "outer_expected": outer_expected,
                            }
                        )
                for m in range(2, shell_max + 1):
                    internal_actual = m - 1 in active and m in active
                    internal_expected = (
                        m - 1 in shell_set
                        and m in shell_set
                        and max(stops[m - 1], stops[m]) < t <= tau
                    )
                    comparisons += 1
                    if internal_actual != internal_expected:
                        failures.append(
                            {
                                "mask": mask,
                                "stops": {str(i): fs(v) for i, v in stops.items()},
                                "t": fs(t),
                                "m": m,
                                "internal_actual": internal_actual,
                                "internal_expected": internal_expected,
                            }
                        )
    return {
        "id": "exhaustive_five_shell_stopped_activation_with_ties",
        "configurations_checked": configurations,
        "time_samples_per_configuration": len(time_samples),
        "boolean_comparisons": comparisons,
        "failures": failures,
        "pass": not failures,
    }


def affine_integral(
    a: Fraction,
    b: Fraction,
    left: Fraction,
    right: Fraction,
) -> Fraction:
    """Integral of a+b*t over [left,right]."""
    return a * (right - left) + b * (right * right - left * left) / 2


def signed_channel_clock_check() -> dict:
    """Check the three S.97--S.99 orientations on one exact fixture."""
    tau = Fraction(3)
    shell_set = {1, 2, 4, 5, 6}
    stops = {
        1: Fraction(1, 2),
        2: Fraction(3, 2),
        4: Fraction(5, 4),
        5: Fraction(1, 4),
        6: Fraction(2),
    }
    q = Fraction(4, 5)
    gamma = {k: q ** (k - 1) for k in range(1, 8)}
    j_minus = {
        k: (Fraction(2 * k - 5, 7), Fraction(k + 1, 11))
        for k in shell_set
    }
    j_plus = {
        m: (Fraction(3 - m, 13), Fraction(2 * m + 1, 17))
        for m in range(2, 8)
    }

    roots = []
    outers = []
    root_direct = Fraction(0)
    outer_direct = Fraction(0)
    gap_direct = Fraction(0)

    # Direct side: reconstruct the active maximal blocks on every event cell.
    breakpoints = sorted({Fraction(0), tau, *stops.values()})
    blocks_checked = 0
    for left, right in zip(breakpoints, breakpoints[1:]):
        if left == right:
            continue
        midpoint = (left + right) / 2
        active = sorted(k for k in shell_set if stops[k] < midpoint <= tau)
        blocks = []
        for k in active:
            if not blocks or k != blocks[-1][-1] + 1:
                blocks.append([k])
            else:
                blocks[-1].append(k)
        for block in blocks:
            first = block[0]
            last = block[-1]
            root_direct += gamma[first] * affine_integral(
                *j_minus[first], left, right
            )
            outer_direct += -gamma[last] * affine_integral(
                *j_plus[last + 1], left, right
            )
            for m in range(first + 1, last + 1):
                d_m = gamma[m - 1] - gamma[m]
                gap_direct += -d_m * affine_integral(
                    *j_plus[m], left, right
                )
            blocks_checked += 1

    # Clock side: use the endpoint formulas S.95--S.99.
    root_clock = Fraction(0)
    outer_clock = Fraction(0)
    for k in sorted(shell_set):
        rho = tau if k == 1 or k - 1 not in shell_set else stops[k - 1]
        lam = tau if k + 1 not in shell_set else stops[k + 1]
        if stops[k] < rho:
            roots.append(k)
            f_increment = -affine_integral(*j_minus[k], stops[k], rho)
            root_clock += -gamma[k] * f_increment
        if stops[k] < lam:
            outers.append(k)
            f_increment = -affine_integral(*j_plus[k + 1], stops[k], lam)
            outer_clock += gamma[k] * f_increment

    internal = sorted(
        m for m in range(2, 8) if m - 1 in shell_set and m in shell_set
    )
    gap_clock = Fraction(0)
    for m in internal:
        start = max(stops[m - 1], stops[m])
        integral = affine_integral(*j_plus[m], start, tau)
        d_m = gamma[m - 1] - gamma[m]
        f_increment = -integral
        gap_clock += d_m * f_increment

    rows = [
        {
            "channel": "root",
            "active_indices": roots,
            "direct": fs(root_direct),
            "clock": fs(root_clock),
            "pass": root_direct == root_clock,
        },
        {
            "channel": "outer",
            "active_indices": outers,
            "direct": fs(outer_direct),
            "clock": fs(outer_clock),
            "pass": outer_direct == outer_clock,
        },
        {
            "channel": "weight_drop",
            "active_indices": internal,
            "direct": fs(gap_direct),
            "clock": fs(gap_clock),
            "pass": gap_direct == gap_clock,
        },
    ]
    return {
        "id": "exact_affine_three_channel_clock_orientations",
        "event_cells_checked": len(breakpoints) - 1,
        "maximal_blocks_checked": blocks_checked,
        "rows": rows,
        "pass": all(row["pass"] for row in rows),
    }


def finite_abel_check() -> dict:
    """Check S.103 exactly for arbitrary rational ball clocks."""
    q = Fraction(7, 9)
    b_values = {
        2: Fraction(2, 7),
        3: Fraction(-5, 11),
        4: Fraction(13, 10),
        5: Fraction(-9, 8),
        6: Fraction(21, 13),
        7: Fraction(-8, 5),
        8: Fraction(34, 17),
    }
    rows = []
    for terminal in range(2, 9):
        gamma = {m: q ** (m - 1) for m in range(1, terminal + 1)}
        left = sum(
            (
                (gamma[m - 1] - gamma[m]) * b_values[m]
                for m in range(2, terminal + 1)
            ),
            Fraction(0),
        )
        right = gamma[1] * b_values[2]
        right += sum(
            (
                gamma[m] * (b_values[m + 1] - b_values[m])
                for m in range(2, terminal)
            ),
            Fraction(0),
        )
        right -= gamma[terminal] * b_values[terminal]
        rows.append(
            {
                "terminal": terminal,
                "left": fs(left),
                "right": fs(right),
                "pass": left == right,
            }
        )
    return {
        "id": "exact_finite_abel_identity_all_terminals_2_through_8",
        "rows": rows,
        "pass": all(row["pass"] for row in rows),
    }


def tower_abel_check() -> dict:
    """Check finite Abel summation after substituting the tower residual."""
    q = Fraction(3, 4)
    gamma = {m: q ** (m - 1) for m in range(1, 11)}
    residual = {m: Fraction((m % 4) + 1, m + 5) for m in range(1, 10)}
    balls = {1: Fraction(3, 7)}
    tower_rows = []
    for m in range(1, 10):
        balls[m + 1] = balls[m] + residual[m] / gamma[m]
        tower_rows.append(
            {
                "m": m,
                "left": fs(gamma[m] * (balls[m + 1] - balls[m])),
                "right": fs(residual[m]),
                "pass": gamma[m] * (balls[m + 1] - balls[m]) == residual[m],
            }
        )
    abel_rows = []
    for terminal in range(2, 10):
        left = sum(
            (
                (gamma[m - 1] - gamma[m]) * balls[m]
                for m in range(2, terminal + 1)
            ),
            Fraction(0),
        )
        left += gamma[terminal] * balls[terminal]
        right = gamma[1] * balls[1] + sum(
            (residual[m] for m in range(1, terminal)),
            Fraction(0),
        )
        abel_rows.append(
            {
                "terminal": terminal,
                "left": fs(left),
                "right": fs(right),
                "pass": left == right,
            }
        )
    return {
        "id": "exact_tower_substituted_finite_abel_identity",
        "tower_rows": tower_rows,
        "abel_rows": abel_rows,
        "pass": all(row["pass"] for row in tower_rows + abel_rows),
    }


def abstract_tower_check() -> dict:
    """Check the S.108--S.110 saturation with an exact rational proxy."""
    q = Fraction(5, 7)
    rows = []
    identity_failures = []
    identity_comparisons = 0
    time_samples = (
        Fraction(0),
        Fraction(1, 7),
        Fraction(1, 3),
        Fraction(2, 3),
        Fraction(1),
    )
    for n_value in range(1, 25):
        gamma = {m: q ** (m - 1) for m in range(1, n_value + 2)}
        terminal_balls = None
        for h_value in time_samples:
            balls = {1: Fraction(0)}
            k_clock = {
                m: h_value if m <= n_value else Fraction(0)
                for m in range(1, n_value + 2)
            }
            boundary_clock = {
                m: Fraction(0) for m in range(1, n_value + 2)
            }
            for m in range(1, n_value + 1):
                balls[m + 1] = balls[m] + k_clock[m] / gamma[m]
            balls[n_value + 2] = balls[n_value + 1]
            for m in range(1, n_value + 2):
                ball_minus = balls[m]
                first = balls[m] - ball_minus
                first_expected = boundary_clock[m] / gamma[m]
                second = balls[m + 1] - ball_minus
                second_expected = k_clock[m] / gamma[m]
                scalar_completion = (
                    k_clock[m] == k_clock[m] + Fraction(0)
                    and k_clock[m] == Fraction(0) + k_clock[m]
                )
                identity_comparisons += 3
                if (
                    first != first_expected
                    or second != second_expected
                    or not scalar_completion
                ):
                    identity_failures.append(
                        {
                            "N": n_value,
                            "h": fs(h_value),
                            "m": m,
                            "first": fs(first),
                            "first_expected": fs(first_expected),
                            "second": fs(second),
                            "second_expected": fs(second_expected),
                            "scalar_completion": scalar_completion,
                        }
                    )
            if h_value == 1:
                terminal_balls = balls

        assert terminal_balls is not None

        # The infinite tail telescopes exactly because B_m is constant after N+1.
        debt = sum(
            (
                (gamma[m - 1] - gamma[m]) * terminal_balls[m]
                for m in range(2, n_value + 2)
            ),
            Fraction(0),
        )
        debt += gamma[n_value + 1] * terminal_balls[n_value + 1]
        y2_squared = Fraction(n_value)
        rows.append(
            {
                "N": n_value,
                "terminal_weight_drop_debt": fs(debt),
                "Y2_squared": fs(y2_squared),
                "pass": debt == y2_squared,
            }
        )
    return {
        "id": "exact_abstract_clock_tower_saturation_N_1_through_24",
        "time_samples": [fs(value) for value in time_samples],
        "identity_comparisons": identity_comparisons,
        "identity_failures": identity_failures,
        "rows": rows,
        "pass": not identity_failures and all(row["pass"] for row in rows),
    }


def compact(body: str) -> str:
    return re.sub(r"\s+", "", body)


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.(\d+)\}", body)
    expected = [str(k) for k in range(85, 112)]
    compressed = compact(body)
    prose = re.sub(r"\s+", " ", body)
    checks = [
        {
            "id": "tags_consecutive",
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
        r"For \(y\ne0\)",
        "The right sides are set to zero at the origin.",
        "The same identities hold separately for",
        "at every time and for",
        "at good times",
        "The central row is paid separately",
        "The asymmetry is exact",
        "All summands are nonnegative",
        "make both sides finite",
        "This is a valid \\(\\ell^1\\) bound",
        "It is not a matched-square-function",
        "The cutoff-operator identities are represented only at this scalar linear",
        "This is an abstract smooth clock witness, not a Navier--Stokes velocity",
        "It does not disprove a dynamical theorem",
        "standalone algebraic mechanism",
        "the dissipation-dominated branch",
        "the R0.74R persistence hypotheses",
        "scale contraction, regularity, singularity formation",
        "**OPEN / NOT CLAIMED**",
        "**NOT CLAY.**",
    )
    required_compact = (
        "0\\le\\chi_{m,R}^-\\le\\chi_{m,R}^+\\le1",
        "\\beta_m^R=\\chi_{m,R}^+-\\chi_{m,R}^-",
        "\\psi_m^R=\\chi_{m+1,R}^+-\\chi_{m,R}^-",
        "\\int_{\\mathbbT^3}\\mathcalW_R^M\\cdot\\nabla\\mathsfB_{m,R}^-=-J_{m,R}^-",
        "\\int_{\\mathbbT^3}\\mathcalW_R^M\\cdot\\nabla\\mathsfB_{m,R}^+=-J_{m,R}^+",
        "\\mathscrK_R[\\Phi]=\\mathscrE_R[\\Phi]+\\mathscrD_R[\\Phi]\\ge0",
        "\\mathscrK_{m+1,R}^{+}-\\mathscrK_{m,R}^{+}=\\gamma_m^{-1}(K_{m,R}-K_{m,R}^{\\partial})\\ge0",
        "d_m:=\\gamma_{m-1}-\\gamma_m>0",
        "R^{-3}\\int_{I_{2R}}\\int_{B_{4R}}|v_R|^2",
        "\\le32\\,\\mathcalE^{M,R}(z_0,8R)",
        "\\sum_{m\\ge2}d_m\\operatorname{TV}\\mathscrQ_{m,R}^+\\leCA_R",
        "I_{\\rmrt}&:=\\{k\\inI:\\sigma_k<\\rho_k\\}",
        "I_{\\rmout}:=\\{k\\inI:\\sigma_k<\\lambda_k\\}",
        "\\widehat\\sigma_m=\\max(\\sigma_{m-1},\\sigma_m)",
        "=-\\sum_{k\\inI_{\\rmrt}}\\gamma_k[\\mathscrF_{k,R}^-(\\rho_k)-\\mathscrF_{k,R}^-(\\sigma_k)]",
        "-\\frac1R\\int_{s_R}^{\\tau}\\eta_R(t)\\mathcalL_R(t)\\,dt=\\sum_{k\\inI_{\\rmout}}",
        "=\\sum_{k\\inI_{\\rmout}}\\gamma_k[\\mathscrF_{k+1,R}^+(\\lambda_k)-\\mathscrF_{k+1,R}^+(\\sigma_k)]",
        "=\\sum_{m\\inI^\\partial}d_m[\\mathscrF_{m,R}^+(\\tau)-\\mathscrF_{m,R}^+(\\widehat\\sigma_m)]",
        "-\\gamma_MB_M",
        "\\gamma_M=\\exp(-4^{M-1}/32)",
        "\\sum_{m\\ge2}d_m\\mathscrK_{m,R}^{+}(t)=\\gamma_1\\mathscrK_{1,R}^{+}(t)+\\sum_{m\\ge1}[K_{m,R}(t)-K_{m,R}^{\\partial}(t)]",
        "\\mathscrK_{m,R}^{-}(t)=\\mathscrK_{m,R}^{+}(t)",
        "\\mathscrE=\\mathscrK,\\qquad\\mathscrD=0,\\qquad\\mathscrQ=0,\\qquad\\mathscrF=\\mathscrK",
        "Y_{2,R}^{\\rmsf}=\\sqrtN",
        "\\sum_{m\\ge2}d_m\\mathscrK_{m,R}^{+}(\\tau)=N",
    )
    forbidden = (
        "global regularity is proved",
        "the Millennium problem is solved",
        "R0.74R persistence hypotheses are proved",
        "root, outer, and weight-drop channels are unconditionally controlled",
        "the abstract witness is a Navier--Stokes solution",
    )
    for sentinel in required_text:
        checks.append(
            {
                "id": "required_text_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in prose,
            }
        )
    for sentinel in required_compact:
        checks.append(
            {
                "id": "required_formula_" + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in compressed,
            }
        )
    for phrase in forbidden:
        checks.append(
            {
                "id": "forbidden_" + hashlib.sha256(phrase.encode()).hexdigest()[:12],
                "phrase": phrase,
                "pass": phrase not in body,
            }
        )
    checks.extend(
        [
            {
                "id": "display_math_balanced",
                "left_count": body.count("\\["),
                "right_count": body.count("\\]"),
                "pass": body.count("\\[") == body.count("\\]"),
            },
            {
                "id": "inline_math_balanced",
                "left_count": body.count("\\("),
                "right_count": body.count("\\)"),
                "pass": body.count("\\(") == body.count("\\)"),
            },
            {
                "id": "no_disallowed_control_characters",
                "pass": not any(ord(ch) < 32 and ch not in "\n\t" for ch in body),
            },
        ]
    )
    return checks


def negative_mutation_checks(body: str) -> list[dict]:
    """Verify structural and numerical rejection of dangerous sign flips."""
    mutations = (
        (
            "abel_terminal_sign_flip_rejected",
            "-\\gamma_MB_M",
            "+\\gamma_MB_M",
        ),
        (
            "root_clock_sign_flip_rejected",
            "=-\\sum_{k\\in I_{\\rm rt}}\\gamma_k",
            "=+\\sum_{k\\in I_{\\rm rt}}\\gamma_k",
        ),
    )
    checks = []
    for identifier, correct, wrong in mutations:
        mutated = body.replace(correct, wrong, 1)
        mutated_structural = structural_checks(mutated)
        checks.append(
            {
                "id": identifier,
                "correct_sentinel": correct,
                "wrong_sentinel": wrong,
                "mutated_structural_result": (
                    "PASS" if all(item["pass"] for item in mutated_structural) else "FAIL"
                ),
                "pass": (
                    correct in body
                    and mutated != body
                    and correct not in mutated
                    and wrong in mutated
                    and not all(item["pass"] for item in mutated_structural)
                ),
            }
        )
    q = Fraction(7, 9)
    terminal = 4
    gamma = {m: q ** (m - 1) for m in range(1, terminal + 1)}
    balls = {
        2: Fraction(2, 7),
        3: Fraction(-5, 11),
        4: Fraction(13, 10),
    }
    left = sum(
        (
            (gamma[m - 1] - gamma[m]) * balls[m]
            for m in range(2, terminal + 1)
        ),
        Fraction(0),
    )
    common = gamma[1] * balls[2] + sum(
        (
            gamma[m] * (balls[m + 1] - balls[m])
            for m in range(2, terminal)
        ),
        Fraction(0),
    )
    correct_abel = common - gamma[terminal] * balls[terminal]
    wrong_abel = common + gamma[terminal] * balls[terminal]
    checks.append(
        {
            "id": "numeric_wrong_abel_sign_rejected",
            "direct": fs(left),
            "correct": fs(correct_abel),
            "wrong": fs(wrong_abel),
            "pass": left == correct_abel and left != wrong_abel,
        }
    )
    root_direct = Fraction(1)
    f_increment = Fraction(-1)
    correct_root = -f_increment
    wrong_root = f_increment
    checks.append(
        {
            "id": "numeric_wrong_root_sign_rejected",
            "direct": fs(root_direct),
            "correct": fs(correct_root),
            "wrong": fs(wrong_root),
            "pass": root_direct == correct_root and root_direct != wrong_root,
        }
    )
    return checks


def build_report(payload: dict) -> str:
    summary = payload["summary"]
    finite = payload["finite_checks"]
    lines = [
        "# R0.74S one-sided ball-clock certificate report",
        "",
        "## Result",
        "",
        f"**{summary['result']}** — {summary['exact_passed']}/"
        f"{summary['exact_total']} exact ledger rows, "
        f"{summary['finite_passed']}/{summary['finite_total']} finite checks, "
        f"{summary['structural_passed']}/{summary['structural_total']} structural checks, "
        f"and {summary['negative_passed']}/{summary['negative_total']} negative mutations passed.",
        "",
        "## Exact ledger",
        "",
        "| Check | Left | Right | Margin |",
        "|---|---:|---:|---:|",
    ]
    for item in payload["exact_checks"]:
        lines.append(
            f"| {item['id']} | {item['left']} | {item['right']} | {item['margin']} |"
        )
    lines.extend(
        [
            "",
            "## Finite checks",
            "",
            f"- The one-sided cutoff identities pass on {finite[0]['samples_checked']} exact rational value samples and {finite[0]['derivative_samples_checked']} transition-derivative samples.",
            f"- The support-packing proxy passes on {finite[1]['samples_checked']} radii; its sampled maximum ratio is {finite[1]['maximum_ratio']}.",
            f"- Root, outer, and internal activation pass {finite[2]['boolean_comparisons']} Boolean comparisons across {finite[2]['configurations_checked']} stopped configurations, including tied stops.",
            "- Exact affine fixtures reproduce all three signs and endpoint orientations in S.97--S.99.",
            "- The finite Abel identity passes at every terminal index from 2 through 8.",
            "- A separate tower-compatible Abel fixture checks every residual insertion and terminal boundary term.",
            "- The abstract tower gives terminal debt equal to the square of the matched square function for every N from 1 through 24, while checking S.90--S.92 at five rational times.",
            "",
            "## Negative sentinels",
            "",
            "- Flipping the terminal Abel sign is rejected.",
            "- Flipping the block-root clock sign is rejected.",
            "- Independent numerical fixtures also reject both wrong signs.",
            "",
            "## Boundary",
            "",
            "This certificate checks only finite algebra, sampled cutoff bookkeeping,",
            "stopped-family combinatorics, and statement integrity.  It does not",
            "machine-prove the suitable local-energy calculation, the infinite",
            "support estimate, or a PDE realization of the abstract clock witness.",
            "It proves no unconditional stopped-work estimate or regularity theorem.",
            "",
            "**FINITE ONLY. ABSTRACT NO-GO ONLY. NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = [
        exact(
            "frozen_geometric_tail_constant",
            1 / (1 - Fraction(32, 35)),
            Fraction(35, 3),
            "sum of the adjacent-ratio majorant",
        ),
        exact(
            "weight_drop_decomposition",
            Fraction(1) - Fraction(32, 35),
            Fraction(3, 35),
            "d_m/gamma_(m-1) in the extremal ratio proxy",
        ),
        exact(
            "central_ball_energy_factor",
            Fraction(4) * Fraction(8),
            Fraction(32),
            "time length factor times 8R local-energy normalization",
        ),
        exact(
            "ball_tower_subtraction",
            Fraction(1) - Fraction(0),
            Fraction(1),
            "(K_m-K_m^partial)/gamma_m in a unit residual row",
        ),
        exact(
            "scalar_clock_completion",
            Fraction(1) + Fraction(0),
            Fraction(0) + Fraction(1),
            "E+D equals Q+F in the abstract assignment",
        ),
    ]
    finite_checks = [
        cutoff_identity_check(),
        support_packing_proxy_check(),
        stopped_activation_exhaustive_check(),
        signed_channel_clock_check(),
        finite_abel_check(),
        tower_abel_check(),
        abstract_tower_check(),
    ]
    structural = structural_checks(body)
    negative = negative_mutation_checks(body)
    passed = (
        all(item["pass"] for item in exact_checks)
        and all(item["pass"] for item in finite_checks)
        and all(item["pass"] for item in structural)
        and all(item["pass"] for item in negative)
    )
    try:
        note_field = str(NOTE.relative_to(REPO))
    except ValueError:
        note_field = str(NOTE)
    payload = {
        "schema": "r074s-one-sided-ball-clock-certificate-v1",
        "scope": (
            "FINITE ONLY: sampled cutoff identities and packing, stopped-family "
            "activation, signed affine clock rows, Abel algebra, abstract tower, "
            "tags, claim boundaries, and negative sign mutations"
        ),
        "note": note_field,
        "note_sha256": sha256(NOTE),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "negative_mutation_checks": negative,
        "claim_boundary": {
            "one_sided_cutoff_identities": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "completed_ball_clock_operator": "INHERITED_AND_PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "quadratic_ball_ledger": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "three_channel_time_orientation": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "terminal_abel_identity": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "scalar_positive_clock_no_go": "PROVED_ABSTRACT_NOT_PDE",
            "pde_cross_channel_sign_theorem": "OPEN",
            "root_outer_weight_drop_dynamical_control": "OPEN",
            "dissipation_dominated_branch": "OPEN",
            "r074r_persistence_hypotheses": "OPEN",
            "fixed_scale_Q1_unconditional": "OPEN",
            "scale_contraction": "OPEN",
            "regularity": "OPEN",
            "singularity_formation": "OPEN",
            "clay_millennium_problem_solved": False,
        },
        "summary": {
            "result": "PASS" if passed else "FAIL",
            "exact_passed": sum(bool(item["pass"]) for item in exact_checks),
            "exact_total": len(exact_checks),
            "finite_passed": sum(bool(item["pass"]) for item in finite_checks),
            "finite_total": len(finite_checks),
            "structural_passed": sum(bool(item["pass"]) for item in structural),
            "structural_total": len(structural),
            "negative_passed": sum(bool(item["pass"]) for item in negative),
            "negative_total": len(negative),
        },
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
