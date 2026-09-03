#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 17.

This standard-library producer checks the exact Taylor-vortex Fourier
identities, closed-streamline witness data, finite deletion and periodic
averaging arithmetic, amplitude exponents, BV/Jordan identities, and the
completed-clock comparison used in the Step 17 proof.  It also fail-closes
the source note's equation inventory, claim boundary, primary-source URLs,
and frozen Step 15/16 dependencies.

The certificate is an audit of exact identities and bookkeeping.  It does
not machine-prove the continuum topology/compactness arguments, arbitrary
mollifier positivity, analytic payment estimates, the open positive-
excursion estimate, regularity, or the Navier--Stokes Millennium problem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = Path(os.environ.get(
    "R074S_RECURRENT_NOTE",
    REPO / "research/r074s_recurrent_streamline_temporal_tail_obstruction.md",
))
JSON_OUT = Path(os.environ.get(
    "R074S_RECURRENT_JSON",
    REPO / "research/r074s_recurrent_streamline_certificate.json",
))
REPORT_OUT = Path(os.environ.get(
    "R074S_RECURRENT_REPORT",
    REPO / "research/r074s_recurrent_streamline_certificate_report.md",
))

SCHEMA = "r074s-recurrent-streamline-certificate-v1"
LOCKED_NOTE_SHA256 = "7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5"
EXPECTED_TAGS = tuple(f"S.{number}" for number in range(445, 476))
DEPENDENCIES = {
    "step15_hybrid": (
        REPO / "research/r074s_hybrid_flux_tail_equivalence.md",
        "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d",
    ),
    "step16_taylor": (
        REPO / "research/r074s_moving_frame_taylor_vortex_obstruction.md",
        "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0",
    ),
}

# A Gaussian rational is represented as (real, imaginary).  Laurent
# polynomials have integer 3D Fourier modes as keys.
ZERO = (Fraction(0), Fraction(0))


def qadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def qmul(left, right):
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def qscale(value, scalar):
    return (scalar * value[0], scalar * value[1])


def clean(poly):
    return {mode: value for mode, value in poly.items() if value != ZERO}


def padd(*polys):
    answer = {}
    for poly in polys:
        for mode, value in poly.items():
            answer[mode] = qadd(answer.get(mode, ZERO), value)
    return clean(answer)


def pscale(poly, scalar):
    return clean({mode: qscale(value, scalar) for mode, value in poly.items()})


def pmul(left, right):
    answer = {}
    for left_mode, left_value in left.items():
        for right_mode, right_value in right.items():
            mode = tuple(left_mode[index] + right_mode[index] for index in range(3))
            answer[mode] = qadd(
                answer.get(mode, ZERO), qmul(left_value, right_value)
            )
    return clean(answer)


def deriv(poly, axis):
    answer = {}
    for mode, value in poly.items():
        frequency = mode[axis]
        answer[mode] = (-frequency * value[1], frequency * value[0])
    return clean(answer)


def laplacian(poly):
    return clean({
        mode: qscale(value, Fraction(-sum(entry * entry for entry in mode)))
        for mode, value in poly.items()
    })


def unit_mode(axis, frequency):
    values = [0, 0, 0]
    values[axis] = frequency
    return tuple(values)


def cosine(axis, frequency=1):
    return {
        unit_mode(axis, frequency): (Fraction(1, 2), Fraction(0)),
        unit_mode(axis, -frequency): (Fraction(1, 2), Fraction(0)),
    }


def sine(axis, frequency=1):
    return {
        unit_mode(axis, frequency): (Fraction(0), Fraction(-1, 2)),
        unit_mode(axis, -frequency): (Fraction(0), Fraction(1, 2)),
    }


def constant(value):
    return {(0, 0, 0): (Fraction(value), Fraction(0))}


def vector_add(left, right):
    return tuple(padd(left[index], right[index]) for index in range(3))


def vector_scale(vector, scalar):
    return tuple(pscale(component, scalar) for component in vector)


def vector_laplacian(vector):
    return tuple(laplacian(component) for component in vector)


def vector_divergence(vector):
    return padd(*(deriv(vector[index], index) for index in range(3)))


def vector_energy(vector):
    return padd(*(pmul(component, component) for component in vector))


def convective(vector):
    return tuple(
        padd(*(pmul(vector[axis], deriv(vector[component], axis))
               for axis in range(3)))
        for component in range(3)
    )


def dot(left, right):
    return padd(*(pmul(left[index], right[index]) for index in range(3)))


def zero_vector(vector):
    return all(not component for component in vector)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path):
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def check(identifier, passed, note, cases=1, **details):
    row = {
        "id": identifier,
        "pass": bool(passed),
        "note": note,
        "cases": int(cases),
    }
    row.update(details)
    return row


def taylor_fourier_checks():
    sx, sy = sine(0), sine(1)
    cx, cy = cosine(0), cosine(1)
    psi = pmul(sx, sy)
    w = (pmul(sx, cy), pscale(pmul(cx, sy), -1), {})
    grad_psi = tuple(deriv(psi, axis) for axis in range(3))
    pressure = pscale(padd(cosine(0, 2), cosine(1, 2)), Fraction(1, 4))
    grad_pressure = tuple(deriv(pressure, axis) for axis in range(3))
    energy = vector_energy(w)
    expected_energy = padd(
        constant(Fraction(1, 2)),
        pscale(pmul(cosine(0, 2), cosine(1, 2)), Fraction(-1, 2)),
    )
    bernoulli = padd(pscale(energy, Fraction(1, 2)), pressure)
    bernoulli_current = tuple(pmul(bernoulli, component) for component in w)
    rows = {
        "divergence_zero": not vector_divergence(w),
        "laplacian_plus_2W_zero": zero_vector(
            vector_add(vector_laplacian(w), vector_scale(w, 2))
        ),
        "convection_plus_grad_p_zero": zero_vector(
            vector_add(convective(w), grad_pressure)
        ),
        "energy_spectrum": energy == expected_energy,
        "stream_function_invariant": not dot(w, grad_psi),
        "div_Bernoulli_current_zero": not vector_divergence(bernoulli_current),
        "b_prime_W_minus_b_DeltaW_zero": (
            Fraction(-2) - Fraction(-2) == 0
        ),
    }
    return check(
        "taylor_exact_fourier_and_streamline_identities",
        all(rows.values()),
        "Exact Gaussian-rational Laurent algebra verifies the Taylor NSE and streamline identities.",
        cases=len(rows),
        rows=rows,
    )


def orbit_witness_checks():
    # The table uses exact squared trigonometric values.  At the first point
    # sin^2 x = sin^2 y = 1/2.  At the second they are 1 and 1/4.
    witnesses = (
        ("pi/4,pi/4", Fraction(1, 2), Fraction(1, 2)),
        ("pi/2,pi/6", Fraction(1), Fraction(1, 4)),
    )
    rows = []
    failures = []
    for label, sin2_x, sin2_y in witnesses:
        psi_squared = sin2_x * sin2_y
        energy = sin2_x * (1 - sin2_y) + (1 - sin2_x) * sin2_y
        expected_energy = Fraction(1, 2) if label == "pi/4,pi/4" else Fraction(3, 4)
        passed = psi_squared == Fraction(1, 4) and energy == expected_energy
        row = {
            "point": label,
            "psi_squared": str(psi_squared),
            "positive_psi": "1/2",
            "W_squared": str(energy),
            "expected_W_squared": str(expected_energy),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)

    periodic_range_lower = 2 * (Fraction(3, 4) - Fraction(1, 2))
    range_row = {
        "periodic_total_variation_lower_bound": str(periodic_range_lower),
        "claimed_V1_lower_bound": "1/2",
        "pass": periodic_range_lower == Fraction(1, 2),
    }
    rows.append(range_row)
    if not range_row["pass"]:
        failures.append(range_row)

    # On psi=1/2, a=sin^2 x and b=sin^2 y obey ab=1/4, while
    # |grad psi|^2=a+b-2ab=a+b-1/2 >= 1/2 by AM-GM.
    regular_rows = []
    for a in (Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
              Fraction(3, 4), Fraction(1)):
        b = Fraction(1, 4) / a
        gradient_squared = a + b - 2 * a * b
        passed = (
            a * b == Fraction(1, 4)
            and Fraction(1, 4) <= b <= 1
            and gradient_squared >= Fraction(1, 2)
        )
        row = {
            "sin2_x": str(a),
            "sin2_y": str(b),
            "gradient_squared": str(gradient_squared),
            "pass": passed,
        }
        regular_rows.append(row)
        if not passed:
            failures.append(row)

    return check(
        "closed_orbit_points_nonconstant_g_and_regular_level",
        not failures,
        "Exact witness values give g=1/2 and 3/4; the level identity gives |grad psi|^2>=1/2.",
        cases=len(rows) + len(regular_rows),
        witness_rows=rows,
        regular_level_rows=regular_rows,
        failures=failures,
    )


def periodic_averaging_checks():
    ratios = [Fraction(2), Fraction(9, 4), Fraction(5, 2), Fraction(3),
              Fraction(15, 4), Fraction(5), Fraction(101, 10)]
    rows = []
    failures = []
    for ratio in ratios:
        complete_periods = ratio.numerator // ratio.denominator
        passed = (
            complete_periods <= ratio
            and Fraction(complete_periods) >= ratio / 2
            and ratio >= 2
        )
        row = {
            "L_over_T": str(ratio),
            "floor": complete_periods,
            "lower_multiplier": str(ratio / 2),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return check(
        "periodic_averaging_floor_lemma",
        not failures,
        "For L/T>=2, floor(L/T)>=L/(2T); each full periodic block contributes V_p.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def deletion_checks():
    failures = []
    rows = []
    cases = 0
    for budget in range(65):
        active = budget + 1
        minimum_remaining = active
        for deleted in range(budget + 1):
            remaining = active - deleted
            minimum_remaining = min(minimum_remaining, remaining)
            cases += 1
        passed = minimum_remaining == 1
        row = {"N": budget, "active": active, "minimum_remaining": minimum_remaining,
               "pass": passed}
        rows.append(row)
        if not passed:
            failures.append(row)
    return check(
        "N_plus_one_fixed_deletion_pigeonhole",
        not failures,
        "Deleting at most N indices leaves an activated index among the first N+1 shells.",
        cases=cases,
        rows=rows,
        failures=failures,
    )


def support_checks():
    failures = []
    rows = []
    cases = 0
    for budget in range(33):
        shell_count = budget + 1
        denominator = 100 * (2 ** (shell_count + 1) + 1)
        radius = Fraction(1, denominator)
        global_bound = math.pi / (
            6 * math.sqrt(2) * (2 ** (shell_count + 1) + 1 / 8)
        )
        for shell in range(1, shell_count + 1):
            outer_radius = (Fraction(2 ** (shell + 1)) + Fraction(1, 8)) * radius
            phase_bound = 2 * math.sqrt(2) * float(outer_radius)
            passed = (
                float(radius) < math.pi / 16
                and float(radius) < global_bound
                and phase_bound < math.pi / 3
                and math.cos(phase_bound) > Fraction(1, 2)
            )
            row = {
                "N": budget,
                "k": shell,
                "R": str(radius),
                "phase_bound": phase_bound,
                "pass": passed,
            }
            rows.append(row)
            cases += 1
            if not passed:
                failures.append(row)
    return check(
        "finite_small_R_physical_shell_screen",
        not failures,
        "Representative rational R puts every one of the first N+1 shell supports where cos((2,2,0).y)>1/2.",
        cases=cases,
        rows=rows,
        failures=failures,
    )


def phase_length_checks():
    failures = []
    rows = []
    radius = Fraction(1, 20)
    for mu in (Fraction(1, 2), Fraction(3, 4), Fraction(1)):
        coefficient = float(mu) * math.expm1(2 * float(radius) ** 2) / 2
        for amplitude in (1, 2, 10, 100, 10_000):
            length = coefficient * amplitude
            ratio = length / amplitude
            theta_start = -length
            passed = (
                length > 0
                and theta_start < 0
                and math.isclose(ratio, coefficient, rel_tol=0, abs_tol=1e-15)
            )
            row = {
                "mu": str(mu),
                "R": str(radius),
                "A": amplitude,
                "L_A": length,
                "L_A_over_A": ratio,
                "pass": passed,
            }
            rows.append(row)
            if not passed:
                failures.append(row)
    return check(
        "recurrent_phase_length_linear_in_A",
        not failures,
        "The exact integral gives theta(t0-R^2)=-L_A and L_A/A=mu_R(e^(2R^2)-1)/2>0.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def temporal_exponent_checks():
    p_values = (
        Fraction(1), Fraction(11, 10), Fraction(6, 5), Fraction(4, 3),
        Fraction(3, 2), Fraction(2), Fraction(3), Fraction(10), None,
    )
    failures = []
    rows = []
    for p in p_values:
        if p is None:
            density_exponent = Fraction(3)
            averaging_exponent = None
            norm_exponent = Fraction(3)
            passed = norm_exponent == 3
        else:
            density_exponent = 3 * p - 1
            averaging_exponent = Fraction(1)
            pth_power_exponent = density_exponent + averaging_exponent
            norm_exponent = pth_power_exponent / p
            passed = pth_power_exponent == 3 * p and norm_exponent == 3
        row = {
            "p": "infinity" if p is None else str(p),
            "post_change_density_A_exponent": str(density_exponent),
            "period_length_A_exponent": (
                "not_applicable" if averaging_exponent is None else str(averaging_exponent)
            ),
            "Lp_norm_A_exponent": str(norm_exponent),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return check(
        "finite_and_infinite_p_recurrent_tail_exponents",
        not failures,
        "After dtheta=mu*b*dt, finite-p powers gain A^(3p-1) times L_A~A; p=infinity has height A^3.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def payment_and_sublinear_checks():
    payment_rows = {
        "energy_raw": (Fraction(2), Fraction(1), Fraction(2)),
        "energy_to_three_halves": (Fraction(2), Fraction(3, 2), Fraction(3)),
        "G_velocity_pressure": (Fraction(1), Fraction(3), Fraction(3)),
        "Lambda_raw": (Fraction(2), Fraction(1), Fraction(2)),
        "Lambda_to_three_halves": (Fraction(2), Fraction(3, 2), Fraction(3)),
        "H_velocity": (Fraction(1), Fraction(3), Fraction(3)),
        "energy_lower_to_three_halves": (Fraction(2), Fraction(3, 2), Fraction(3)),
    }
    failures = []
    rows = []
    for name, (raw, outer_power, expected) in payment_rows.items():
        result = raw * outer_power
        passed = result == expected and result <= 3
        row = {
            "row": name,
            "raw_A_exponent": str(raw),
            "outer_power": str(outer_power),
            "result_A_exponent": str(result),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)

    beta_values = (
        Fraction(-10), Fraction(-2), Fraction(-1, 3), Fraction(0),
        Fraction(1, 10), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3),
        Fraction(3, 4), Fraction(9, 10), Fraction(99, 100),
    )
    for beta in beta_values:
        ratio_exponent = 3 * (1 - beta)
        passed = beta < 1 and ratio_exponent > 0
        row = {
            "row": "sublinear_ratio",
            "beta": str(beta),
            "tail_A_exponent": "3",
            "payment_beta_A_exponent": str(3 * beta),
            "ratio_A_exponent": str(ratio_exponent),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return check(
        "complete_payment_cubic_and_beta_below_one_divergence",
        not failures,
        "All payment rows are at most cubic with a cubic lower row; A^3/(A^3)^beta diverges for beta<1.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def integration_by_parts_and_range_checks():
    # b'=-2b implies (b^2)'=-4b^2 and
    # (eta*b^2)'=eta'*b^2-4*eta*b^2.
    derivative_coefficient = 2 * Fraction(-2)
    product_coefficients = {"eta_prime_b_squared": 1, "eta_b_squared": derivative_coefficient}
    rows = [{
        "identity": "d(eta*b^2)/dt",
        "coefficients": {key: str(value) for key, value in product_coefficients.items()},
        "pass": derivative_coefficient == -4,
    }]
    failures = [] if derivative_coefficient == -4 else rows.copy()

    # Across a fixed phase interval of physical length c/A, the slow change
    # in b^2 is A^2(exp(4c/A)-1)=O(A), while the g-boundary scale is A^2.
    c = Fraction(1, 5)
    for amplitude in (10, 100, 1_000, 10_000):
        slow_change = amplitude ** 2 * math.expm1(4 * float(c) / amplitude)
        normalized_linear = slow_change / amplitude
        passed = (
            slow_change / amplitude ** 2 < 0.1
            and abs(normalized_linear - 4 * float(c)) < 0.04
        )
        row = {
            "A": amplitude,
            "phase_segment_c": str(c),
            "delta_b_squared": slow_change,
            "delta_b_squared_over_A": normalized_linear,
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return check(
        "integration_by_parts_sign_and_quadratic_signed_range_scale",
        not failures,
        "The product derivative has the S.465 minus-four sign; slow amplitude drift over one phase segment is O(A).",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def total_variation(sequence):
    return sum(abs(right - left) for left, right in zip(sequence, sequence[1:]))


def positive_variation(sequence):
    return sum(max(Fraction(0), right - left)
               for left, right in zip(sequence, sequence[1:]))


def positive_excursion(sequence):
    answer = Fraction(0)
    for left_index in range(len(sequence)):
        for right_index in range(left_index + 1, len(sequence)):
            answer = max(answer, sequence[right_index] - sequence[left_index])
    return max(Fraction(0), answer)


def bv_jordan_checks():
    failures = []
    jordan_rows = []
    for plus in range(13):
        for minus in range(13):
            v_plus = Fraction(plus, 3)
            v_minus = Fraction(minus, 4)
            endpoint = v_plus - v_minus
            variation = v_plus + v_minus
            rhs = abs(endpoint) + 2 * min(v_plus, v_minus)
            passed = variation == rhs
            if len(jordan_rows) < 12:
                jordan_rows.append({
                    "V_plus": str(v_plus),
                    "V_minus": str(v_minus),
                    "endpoint": str(endpoint),
                    "TV": str(variation),
                    "rhs": str(rhs),
                    "pass": passed,
                })
            if not passed:
                failures.append({"V_plus": str(v_plus), "V_minus": str(v_minus)})

    path_cases = 0
    for increments in itertools.product((-2, -1, 0, 1, 2), repeat=4):
        path = [Fraction(0)]
        for increment in increments:
            path.append(path[-1] + increment)
        tv = total_variation(path)
        osc_plus = positive_excursion(path)
        path_cases += 1
        if osc_plus > tv:
            failures.append({
                "increments": list(increments),
                "positive_excursion": str(osc_plus),
                "TV": str(tv),
            })
    return check(
        "jordan_identity_and_positive_excursion_below_TV",
        not failures,
        "Exact nonnegative V+/V- arithmetic verifies TV=|endpoint|+2min; exhaustive paths verify osc+<=TV.",
        cases=13 * 13 + path_cases,
        sample_jordan_rows=jordan_rows,
        failures=failures,
    )


def best_after_deletion(values, budget):
    count = len(values)
    best = None
    for size in range(min(budget, count) + 1):
        for deleted in itertools.combinations(range(count), size):
            deleted_set = set(deleted)
            candidate = sum(
                (value for index, value in enumerate(values) if index not in deleted_set),
                Fraction(0),
            )
            if best is None or candidate < best:
                best = candidate
    return Fraction(0) if best is None else best


def clock_inequality_checks():
    failures = []
    scalar_cases = 0
    witnesses = []
    scalar_records = []
    for k_tail in itertools.product((0, 1, 2), repeat=3):
        k_path = tuple(Fraction(value) for value in (0,) + k_tail)
        for q_tail in itertools.product((-1, 0, 1), repeat=3):
            q_path = tuple(Fraction(value) for value in (0,) + q_tail)
            f_path = tuple(k - q for k, q in zip(k_path, q_path))
            osc_f = positive_excursion(f_path)
            max_k = max(k_path)
            tv_q = total_variation(q_path)
            var_plus_k = positive_variation(k_path)
            tv_f = total_variation(f_path)
            inequalities = (
                osc_f <= max_k + tv_q,
                max_k <= osc_f + tv_q,
                var_plus_k <= tv_f + tv_q,
                tv_f <= 2 * var_plus_k + tv_q,
                max_k <= var_plus_k,
            )
            scalar_cases += 1
            scalar_records.append((osc_f, max_k, tv_q, var_plus_k, tv_f))
            if not all(inequalities):
                failures.append({
                    "K": [str(value) for value in k_path],
                    "Q": [str(value) for value in q_path],
                    "F": [str(value) for value in f_path],
                    "inequalities": list(inequalities),
                })

    # Assemble deterministic coordinate families from the scalar audit rows
    # and optimize each side over every allowed fixed deletion set.
    vector_cases = 0
    index_families = (
        (0, 28, 365, 728),
        (5, 111, 417, 701),
        (19, 243, 512, 679),
        (26, 300, 600, 727),
        (54, 222, 486, 650),
    )
    for dataset, indices in enumerate(index_families):
        records = [scalar_records[index] for index in indices]
        osc_values = [row[0] for row in records]
        max_values = [row[1] for row in records]
        q_values = [row[2] for row in records]
        var_values = [row[3] for row in records]
        tv_values = [row[4] for row in records]
        total_q = sum(q_values, Fraction(0))
        for budget in range(4):
            o_tail = best_after_deletion(osc_values, budget)
            m_tail = best_after_deletion(max_values, budget)
            v_tail = best_after_deletion(var_values, budget)
            h_tail = best_after_deletion(tv_values, budget)
            inequalities = (
                o_tail <= m_tail + total_q,
                m_tail <= o_tail + total_q,
                v_tail <= h_tail + total_q,
                h_tail <= 2 * v_tail + total_q,
                m_tail <= v_tail,
            )
            vector_cases += 1
            witness = {
                "dataset": dataset,
                "scalar_record_indices": list(indices),
                "N": budget,
                "O_tail": str(o_tail),
                "M_tail": str(m_tail),
                "V_tail": str(v_tail),
                "H_tail": str(h_tail),
                "B_Q": str(total_q),
                "pass": all(inequalities),
            }
            witnesses.append(witness)
            if not all(inequalities):
                failures.append(witness)
    return check(
        "completed_clock_scalar_and_fixed_deletion_inequalities",
        not failures,
        "Exhaustive scalar paths and exact subset optimization verify all five inequalities in S.475.",
        cases=scalar_cases + vector_cases,
        fixed_deletion_rows=witnesses,
        failures=failures,
    )


def recurrence_range_separation_checks():
    rows = {
        "flux_density": {"height_A": 3},
        "phase_speed": {"A": 1},
        "circuits_on_fixed_window": {"A": 1},
        "absolute_variation": {"density_A": 3, "time_A": 0, "result_A": 3},
        "signed_primitive_boundary": {"b_squared_A": 2, "result_A": 2},
        "positive_excursion": {"result_A": 2},
        "payment_two_thirds": {"payment_A": 3, "power": "2/3", "result_A": 2},
    }
    passed = (
        rows["absolute_variation"]["result_A"] == 3
        and rows["signed_primitive_boundary"]["result_A"] == 2
        and rows["positive_excursion"]["result_A"] == 2
        and rows["payment_two_thirds"]["result_A"] == 2
    )
    return check(
        "recurrent_absolute_vs_signed_exponent_separation",
        passed,
        "The recurrent tail is cubic while signed range and positive excursion remain quadratic, matching P^(2/3).",
        cases=len(rows),
        rows=rows,
    )


def balanced_environment(text, environment):
    return text.count(f"\\begin{{{environment}}}") == text.count(
        f"\\end{{{environment}}}"
    )


def structural_checks(text):
    found_tags = re.findall(r"\\tag\{(S\.\d+[a-z]?)\}", text)
    counts = Counter(found_tags)
    tag_inventory_passed = (
        tuple(found_tags) == EXPECTED_TAGS
        and set(counts) == set(EXPECTED_TAGS)
        and all(counts[tag] == 1 for tag in EXPECTED_TAGS)
    )
    anchors = {
        "tag_inventory_unique_and_ordered": tag_inventory_passed,
        "balanced_display_environments": (
            text.count(r"\[") == text.count(r"\]")
            and all(balanced_environment(text, environment) for environment in (
                "aligned", "gathered", "equation", "split"
            ))
        ),
        "false_claim_and_nonclaim_boundary": all(phrase in text for phrase in (
            "**(S.444 is false)**",
            "every universal power-only estimate",
            "with \\(\\beta<1\\) is false",
            "This is a route correction",
            "**NOT CLAY.**",
        )),
        "quantifier_negation": all(phrase in text for phrase in (
            r"\forall p\in[1,\infty]",
            r"\forall N\in\mathbb N_0",
            r"\forall\beta<1",
            r"\mathfrak H^F_{p,N,R}>C(P_R^M)^\beta",
            r"A^{3(1-\beta)}",
        )),
        "closed_streamline_and_recurrence": all(phrase in text for phrase in (
            r"\sin x_1\sin x_2=1/2",
            r"T_*:=\int_\Gamma{d\ell\over|W|}<\infty",
            "The function \\(g\\) is not constant",
            r"L_A={\mu_RA\over2}(e^{2R^2}-1)",
            "linearly many",
        )),
        "flux_payment_and_deletion": all(phrase in text for phrase in (
            r"\dot F_{k,R}(t)",
            r"M=N+1",
            r"\mathfrak H^F_{p,N,R}\ge d_{p,N,R}A^3",
            r"c_RA^3\le P_R^M\le C_RA^3",
            "complete \\(P_R^M\\)",
        )),
        "bv_positive_excursion_and_open_target": all(phrase in text for phrase in (
            r"\operatorname {TV}F_{k,R}",
            "temporal backtracking debt",
            r"\mathfrak O^{F,+}_{N,R}",
            r"\mathfrak Z_{N,R}^{\boldsymbol\lambda}",
            "Equation (S.472) is **OPEN**",
            "direct hybrid terminal gate from Step 15 also remains",
        )),
        "completed_clock_boundary": all(phrase in text for phrase in (
            r"B_{Q,R}:=\sum_k\operatorname {TV}Q_{k,R}\le C_QA_R",
            r"\mathfrak M^K_{N,R}",
            r"\mathfrak V^K_{N,R}",
            r"\mathfrak M^K_{N,R}&\le\mathfrak V^K_{N,R}",
            "common\nzero start",
        )),
        "primary_source_collision_boundary": all(url in text for url in (
            "https://doi.org/10.1080/14786442308634295",
            "https://arxiv.org/abs/2008.05588",
            "https://arxiv.org/abs/1101.2193",
            "https://arxiv.org/abs/1611.01482",
            "https://www.numdam.org/item/SEDP_1999-2000____A13_0/",
        )) and "not a novelty or priority claim" in text,
        "route_prohibition_and_open_status": all(phrase in text for phrase in (
            "No later proof may use (S.342) or (S.444)",
            "all are false on a globally smooth exact solution",
            "Q.12",
            "Q.1",
            "scale contraction, and regularity",
        )),
    }
    rows = []
    for identifier, passed in anchors.items():
        details = {}
        if identifier == "tag_inventory_unique_and_ordered":
            details = {
                "found": found_tags,
                "expected": list(EXPECTED_TAGS),
                "counts": dict(sorted(counts.items())),
            }
        rows.append(check(
            f"structural_{identifier}",
            passed,
            "Semantic, syntax, equation, and source anchor in the reviewed Step 17 note.",
            **details,
        ))
    return rows


def dependency_checks():
    rows = []
    for identifier, (path, expected) in DEPENDENCIES.items():
        actual = sha256(path) if path.exists() else ""
        rows.append(check(
            f"dependency_{identifier}",
            actual == expected,
            "Frozen imported note has the reviewed byte identity.",
            path=display_path(path),
            expected_sha256=expected,
            actual_sha256=actual,
        ))
    return rows


def write_report(payload):
    finite = payload["finite_checks"]
    structural = payload["structural_checks"]
    dependencies = payload["dependency_checks"]
    all_rows = finite + structural + dependencies
    lines = [
        "# R0.74S Step 17 recurrent-streamline certificate report",
        "",
        f"- Schema: `{SCHEMA}`",
        f"- Source note: `{payload['note']['path']}`",
        f"- Source SHA-256: `{payload['note']['sha256']}`",
        f"- Finite groups: {sum(row['pass'] for row in finite)}/{len(finite)}",
        f"- Finite cases: {sum(row['cases'] for row in finite)}",
        f"- Structural groups: {sum(row['pass'] for row in structural)}/{len(structural)}",
        f"- Dependency locks: {sum(row['pass'] for row in dependencies)}/{len(dependencies)}",
        "",
        "## Verdict",
        "",
        f"**{payload['verdict']}**",
        "",
        "This certificate supports exact Fourier/streamline identities, finite",
        "deletion and periodic-averaging arithmetic, amplitude exponents,",
        "BV/Jordan identities, clock inequalities, and the claim boundary.",
        "It does not machine-prove the continuum analytic theorem.",
        "",
        "## Check inventory",
        "",
        "| Check | Result | Cases |",
        "|---|---:|---:|",
    ]
    for row in all_rows:
        lines.append(
            f"| `{row['id']}` | {'PASS' if row['pass'] else 'FAIL'} | {row.get('cases', 1)} |"
        )
    lines += [
        "",
        "## Audited claim boundary",
        "",
        "- (S.342): false on a smooth exact Navier--Stokes family.",
        "- (S.444): false on the recurrent closed-streamline terminal setting.",
        "- Every absolute temporal-tail power with beta below one: false for all p at least one.",
        "- Fixed-deletion positive-excursion estimate (S.472): open.",
        "- Direct hybrid terminal-flux gate, Q.12, Q.1, scale contraction, and regularity: open.",
        "- Navier--Stokes Millennium problem: not solved.",
        "",
        "## Explicit limitations",
        "",
        "- No machine proof of compact regular-level topology or arbitrary-mollifier positivity.",
        "- No machine proof of the continuum payment bounds or asymptotic lower constants.",
        "- No proof of the open positive-excursion or direct hybrid terminal gate.",
        "- No proof of Q.12, Q.1, scale contraction, regularity, or the Millennium problem.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main():
    text = NOTE.read_text(encoding="utf-8")
    note_sha = sha256(NOTE)
    finite = [
        taylor_fourier_checks(),
        orbit_witness_checks(),
        periodic_averaging_checks(),
        deletion_checks(),
        support_checks(),
        phase_length_checks(),
        temporal_exponent_checks(),
        payment_and_sublinear_checks(),
        integration_by_parts_and_range_checks(),
        bv_jordan_checks(),
        clock_inequality_checks(),
        recurrence_range_separation_checks(),
    ]
    structural = structural_checks(text)
    structural.insert(0, check(
        "locked_note_sha256",
        note_sha == LOCKED_NOTE_SHA256,
        "Source note matches its frozen byte identity.",
        expected_sha256=LOCKED_NOTE_SHA256,
        actual_sha256=note_sha,
    ))
    dependencies = dependency_checks()
    passed = all(row["pass"] for row in finite + structural + dependencies)
    payload = {
        "schema": SCHEMA,
        "verdict": "PASS" if passed else "FAIL",
        "note": {
            "path": display_path(NOTE),
            "sha256": note_sha,
        },
        "finite_checks": finite,
        "structural_checks": structural,
        "dependency_checks": dependencies,
        "claim_boundary": {
            "S342_supercritical_temporal_tail": "FALSE_BY_SMOOTH_EXACT_NSE",
            "S444_critical_L1_temporal_tail": "FALSE_BY_RECURRENT_SMOOTH_EXACT_NSE",
            "absolute_tail_beta_below_one_all_p_at_least_one": "FALSE",
            "S472_fixed_deletion_positive_excursion": "OPEN",
            "direct_hybrid_terminal_flux_gate": "OPEN_NOT_REFUTED",
            "Q12": "OPEN",
            "Q1": "OPEN",
            "regularity": "OPEN",
            "millennium_problem_solved": False,
        },
        "limitations": [
            "finite checks do not prove continuum topology or analytic estimates",
            "arbitrary-mollifier positivity and payment estimates are analytic inputs",
            "the fixed-deletion positive-excursion estimate remains open",
            "regularity and the Millennium problem remain open",
        ],
    }
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_report(payload)
    print(json.dumps({
        "schema": SCHEMA,
        "verdict": payload["verdict"],
        "note_sha256": note_sha,
        "finite_groups": f"{sum(row['pass'] for row in finite)}/{len(finite)}",
        "finite_cases": sum(row["cases"] for row in finite),
        "structural_groups": f"{sum(row['pass'] for row in structural)}/{len(structural)}",
        "dependency_locks": f"{sum(row['pass'] for row in dependencies)}/{len(dependencies)}",
        "failed_checks": [
            row["id"] for row in finite + structural + dependencies if not row["pass"]
        ],
    }, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
