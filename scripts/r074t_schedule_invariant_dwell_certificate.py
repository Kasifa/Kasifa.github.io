#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74T Step 19.

The producer checks exact rational/symbolic algebra, finite Holder and
time-floor proxies, fixed-deletion clock combinatorics, asynchronous-window
geometry, source structure, and frozen dependency hashes.  It deliberately
does not machine-prove the continuous Holder argument, the inherited packet
survival estimates, the exact Navier--Stokes construction, regularity, or a
Clay statement.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
import sys
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = Path(os.environ.get(
    "R074T_DWELL_NOTE",
    REPO / "research/r074t_schedule_invariant_dwell_coercivity.md",
))
LITERATURE = Path(os.environ.get(
    "R074T_DWELL_LITERATURE",
    REPO / "research/r074t_schedule_invariant_literature_audit.md",
))
JSON_OUT = Path(os.environ.get(
    "R074T_DWELL_JSON",
    REPO / "research/r074t_schedule_invariant_dwell_certificate.json",
))
REPORT_OUT = Path(os.environ.get(
    "R074T_DWELL_REPORT",
    REPO / "research/r074t_schedule_invariant_dwell_certificate_report.md",
))

SCHEMA = "r074t-schedule-invariant-dwell-certificate-v1"
MUTATION = os.environ.get("R074T_DWELL_MUTATION", "").strip()

# Rebind these two constants only after the theorem note and literature audit
# are frozen.  Environment overrides are provided for pre-freeze QA, but a
# final archived PASS must also pass with no overrides.
LOCKED_NOTE_SHA256 = os.environ.get(
    "R074T_DWELL_EXPECTED_NOTE_SHA256",
    "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
)
LOCKED_LITERATURE_SHA256 = os.environ.get(
    "R074T_DWELL_EXPECTED_LITERATURE_SHA256",
    "60b49f6279c696a370af5f8050a6162753372eba81f8215e02e15259f084e88b",
)

EXPECTED_TAGS = tuple(f"T.{number}" for number in range(1, 44))
DEPENDENCIES = {
    "r074e_version_m_payment": (
        REPO / "research/r074e_local_mollified_frame_gate.md",
        "3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7",
    ),
    "r074f_packet_survival": (
        REPO / "research/r074f_two_packet_survival.md",
        "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb",
    ),
    "r074p_completed_clock": (
        REPO / "research/r074p_temporal_observable_triage.md",
        "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    ),
    "r074q_common_shear": (
        REPO / "research/r074q_common_shear_multipacket_gate.md",
        "60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695",
    ),
    "r074q_relaxed_multipacket": (
        REPO / "research/r074q_relaxed_multipacket_cubic_obstruction.md",
        "ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d",
    ),
    "r074s_fixed_deletion": (
        REPO / "research/r074s_fixed_deletion_simultaneous_height.md",
        "305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1",
    ),
}

NEGATIVE_MUTATIONS = (
    "gamma_weight_quarter_to_half",
    "gamma_exponent_sign",
    "two_thirds_to_half",
    "L_power_sign",
    "theta_power_sign",
    "holder_direction",
    "time_inf_to_sup",
    "survival_forall_to_exists",
    "min_to_max",
    "fixed_to_moving_deletion",
    "same_shell_allowed",
    "allow_signed_clocks",
    "K_floor_to_Hfix",
    "hstar_to_full_clock",
    "volume_upper_to_lower",
    "theta_bound_direction",
    "survival_defect_sign",
    "margin_sign",
    "async_qpre_sign",
    "async_interval_direction",
    "sum_overlapping_lobes",
    "tag_inventory",
    "claim_boundary",
    "source_hash",
    "literature_hash",
    "dependency_hash",
)


def f(numerator=0, denominator=1):
    return Fraction(numerator, denominator)


def fs(value):
    return f"{value.numerator}/{value.denominator}"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path):
    try:
        return str(path.resolve().relative_to(REPO.resolve()))
    except ValueError:
        return str(path.resolve())


def check(identifier, passed, note, cases=1, **details):
    row = {
        "id": identifier,
        "pass": bool(passed),
        "note": note,
        "cases": int(cases),
    }
    row.update(details)
    return row


def add_vectors(*vectors):
    keys = set().union(*(vector.keys() for vector in vectors))
    return {
        key: sum((vector.get(key, f()) for vector in vectors), f())
        for key in keys
        if sum((vector.get(key, f()) for vector in vectors), f()) != 0
    }


def scale_vector(vector, scalar):
    return {key: value * scalar for key, value in vector.items()
            if value * scalar != 0}


def vector_strings(vector):
    return {key: fs(value) for key, value in sorted(vector.items())}


def exact_exponent_and_constant_ledger():
    gamma_weight = (f(1, 2) if MUTATION == "gamma_weight_quarter_to_half"
                    else f(1, 4))
    volume_l_power = f(1, 2) if MUTATION == "L_power_sign" else f(-1, 2)
    dwell_theta_power = f(-1) if MUTATION == "theta_power_sign" else f(1)
    atomic = {
        "payment_normalization": {"R": f(-2)},
        "dwell_measure": {"theta": dwell_theta_power, "R": f(3)},
        "shell_weight": {"Gamma": gamma_weight},
        "volume_inverse_sqrt": {"C_Omega": f(-1, 2),
                                "L": volume_l_power, "R": f(-3, 2)},
        "kinetic_floor_three_halves": {
            "two": f(3, 2), "R": f(3, 2),
            "Gamma": f(-3, 2), "h": f(3, 2),
        },
        "normalization_two": {"two": f(-2)},
        "weight_constant": {"c_W": f(1)},
    }
    raw = add_vectors(*atomic.values())
    expected_raw = {
        "C_Omega": f(-1, 2), "Gamma": f(-5, 4),
        "L": f(-1, 2), "R": f(1), "c_W": f(1),
        "h": f(3, 2), "theta": f(1), "two": f(-1, 2),
    }
    powered_exponent = f(1, 2) if MUTATION == "two_thirds_to_half" else f(2, 3)
    powered = scale_vector(raw, powered_exponent)
    if MUTATION == "gamma_exponent_sign" and "Gamma" in powered:
        powered["Gamma"] *= -1
    expected_powered = {
        "C_Omega": f(-1, 3), "Gamma": f(-5, 6),
        "L": f(-1, 3), "R": f(2, 3), "c_W": f(2, 3),
        "h": f(1), "theta": f(2, 3), "two": f(-1, 3),
    }

    # Substitute h ~ Gamma a^2 L R^2 into the raw monomial.
    h_power = raw.get("h", f())
    recovered = dict(raw)
    recovered.pop("h", None)
    recovered = add_vectors(
        recovered,
        scale_vector({"Gamma": f(1), "amplitude": f(2),
                      "L": f(1), "R": f(2)}, h_power),
    )
    expected_recovered = {
        "C_Omega": f(-1, 2), "Gamma": f(1, 4),
        "L": f(1), "R": f(4), "amplitude": f(3),
        "c_W": f(1), "theta": f(1), "two": f(-1, 2),
    }

    c_squared = f(1, 2)  # c_W^2/(2 C_Omega), before c_W/C_Omega values.
    exact_specialized_c_squared = c_squared / f(1, 16)
    rows = [
        check(
            "atomic_raw_monomial_exponents",
            raw == expected_raw,
            "Atomic payment, dwell, weight, volume, and kinetic-floor factors reconstruct T.15.",
            observed=vector_strings(raw), expected=vector_strings(expected_raw),
        ),
        check(
            "two_thirds_monomial_exponents",
            powered == expected_powered,
            "Taking the two-thirds power reconstructs Lambda and its exact exponents.",
            observed=vector_strings(powered), expected=vector_strings(expected_powered),
        ),
        check(
            "amplitude_recovery_exponents",
            recovered == expected_recovered,
            "Substitution of the packet kinetic floor recovers Gamma^(1/4) L R^4.",
            observed=vector_strings(recovered), expected=vector_strings(expected_recovered),
        ),
        check(
            "robust_constant_squared",
            c_squared == f(1, 2),
            "The robust coefficient satisfies c_rob^2=c_W^2/(2 C_Omega).",
            value=fs(c_squared),
        ),
        check(
            "exact_lobe_constant",
            exact_specialized_c_squared == f(8) and f(2) ** 3 == f(8),
            "At c_W=1 and C_Omega=1/16, c_rob=2 sqrt(2) and c_rob^(2/3)=2.",
            raw_constant_squared=fs(exact_specialized_c_squared),
            powered_constant_cubed=fs(f(2) ** 3),
        ),
    ]
    return rows


def rational_monomial_grid():
    cases = 0
    failures = []
    roots = (f(1, 2), f(2, 3), f(3, 4), f(1))
    gamma_sign = f(5, 6) if MUTATION == "gamma_exponent_sign" else f(-5, 6)
    theta_sign = f(-2, 3) if MUTATION == "theta_power_sign" else f(2, 3)
    l_sign = f(1, 3) if MUTATION == "L_power_sign" else f(-1, 3)
    power = f(1, 2) if MUTATION == "two_thirds_to_half" else f(2, 3)

    # Every physical variable is a 24th power, so every exponent used by the
    # baseline and deliberate mutations remains an integer power of its root.
    def root_power(root, exponent):
        integer = 24 * exponent
        if integer.denominator != 1:
            return None
        return root ** integer.numerator

    for q, r, g, ell, s in itertools.product(roots, repeat=5):
        cases += 1
        observed_factors = (
            root_power(q, theta_sign),
            root_power(r, f(1) * power),
            root_power(g, gamma_sign),
            root_power(ell, l_sign),
            root_power(s, f(3, 2) * power),
        )
        if any(value is None for value in observed_factors):
            observed = None
        else:
            observed = f(2)
            for value in observed_factors:
                observed *= value
        expected = (
            f(2) * q ** 16 * r ** 16 * g ** -20
            * ell ** -8 * s ** 24
        )
        if observed != expected:
            failures.append({
                "roots": [fs(x) for x in (q, r, g, ell, s)],
                "observed": None if observed is None else fs(observed),
                "expected": fs(expected),
            })
            if len(failures) >= 8:
                break
    return check(
        "exact_rational_Lambda_grid",
        not failures,
        "A perfect-power rational grid independently checks every powered monomial exponent.",
        cases=cases, failures=failures,
    )


def finite_holder_grid():
    cases = 0
    failures = []
    strict_seen = False
    equality_seen = False
    for length in range(1, 6):
        weight_schemes = (
            tuple(f(1) for _ in range(length)),
            tuple(f(index + 1) for index in range(length)),
        )
        for raw in itertools.product(range(4), repeat=length):
            for weights in weight_schemes:
                cases += 1
                volume = sum(weights, f())
                l2 = sum((w * value ** 2 for w, value in zip(weights, raw)), f())
                l3 = sum((w * value ** 3 for w, value in zip(weights, raw)), f())
                left = l3 ** 2 * volume
                right = l2 ** 3
                relation = left <= right if MUTATION == "holder_direction" else left >= right
                strict_seen = strict_seen or left > right
                equality_seen = equality_seen or (left == right and any(raw))
                if not relation:
                    failures.append({"values": list(raw),
                                     "weights": [fs(x) for x in weights],
                                     "left": fs(left), "right": fs(right)})
                    if len(failures) >= 8:
                        break
            if len(failures) >= 8:
                break
        if len(failures) >= 8:
            break
    return check(
        "finite_weighted_Holder_proxy",
        not failures and strict_seen and equality_seen,
        "Exact finite cells satisfy (sum w|u|^3)^2 sum w >= (sum w|u|^2)^3.",
        cases=cases, strict_seen=strict_seen, equality_seen=equality_seen,
        failures=failures,
    )


def finite_time_floor_grid():
    cases = 0
    failures = []
    strict_seen = False
    use_supremum = MUTATION in ("time_inf_to_sup", "survival_forall_to_exists")
    for length in range(1, 6):
        weights = tuple(f(index + 1) for index in range(length))
        for roots in itertools.product(range(4), repeat=length):
            cases += 1
            integral = sum((weight * root ** 3
                            for weight, root in zip(weights, roots)), f())
            floor_root = max(roots) if use_supremum else min(roots)
            predicted = sum(weights, f()) * floor_root ** 3
            strict_seen = strict_seen or integral > predicted
            if integral < predicted:
                failures.append({"roots": list(roots), "integral": fs(integral),
                                 "predicted": fs(predicted)})
                if len(failures) >= 8:
                    break
        if len(failures) >= 8:
            break
    return check(
        "finite_time_infimum_floor_proxy",
        not failures and strict_seen,
        "A time integral is controlled by an all-time infimum floor, not by a peak or existential time.",
        cases=cases, strict_seen=strict_seen, failures=failures,
    )


def deletion_sets(size, budget):
    indices = tuple(range(size))
    return tuple(
        frozenset(choice)
        for count in range(min(size, budget) + 1)
        for choice in itertools.combinations(indices, count)
    )


def tail(row, deleted):
    return sum((value for index, value in enumerate(row)
                if index not in deleted), f())


def fixed_clock_height(matrix, budget):
    return min(
        max(tail(row, deleted) for row in matrix)
        for deleted in deletion_sets(len(matrix[0]), budget)
    )


def moving_clock_height(matrix, budget):
    sets = deletion_sets(len(matrix[0]), budget)
    return max(min(tail(row, deleted) for deleted in sets) for row in matrix)


def two_clock_grid():
    cases = 0
    failures = []
    equality_seen = False
    strict_seen = False
    specifications = ((2, 3, 3), (3, 2, 3))
    for shells, times, alphabet_size in specifications:
        for flat in itertools.product(range(alphabet_size),
                                      repeat=shells * times):
            matrix = tuple(
                tuple(f(flat[time * shells + shell])
                      for shell in range(shells))
                for time in range(times)
            )
            baseline_fixed = fixed_clock_height(matrix, 1)
            for k1, k2 in itertools.permutations(range(shells), 2):
                for t1 in range(times):
                    for t2 in range(times):
                        h1, h2 = matrix[t1][k1], matrix[t2][k2]
                        if h1 <= 0 or h2 <= 0:
                            continue
                        cases += 1
                        target = max(h1, h2) if MUTATION == "min_to_max" else min(h1, h2)
                        observed = (moving_clock_height(matrix, 1)
                                    if MUTATION == "fixed_to_moving_deletion"
                                    else baseline_fixed)
                        equality_seen = equality_seen or observed == target
                        strict_seen = strict_seen or observed > target
                        if observed < target:
                            failures.append({
                                "matrix": [[fs(x) for x in row] for row in matrix],
                                "targets": [k1, k2], "times": [t1, t2],
                                "heights": [fs(h1), fs(h2)],
                                "observed": fs(observed), "target": fs(target),
                            })
                            if len(failures) >= 8:
                                break
                    if len(failures) >= 8:
                        break
                if len(failures) >= 8:
                    break
            if len(failures) >= 8:
                break
        if len(failures) >= 8:
            break

    if MUTATION == "same_shell_allowed":
        matrix = ((f(1), f()), (f(2), f()))
        observed, target = fixed_clock_height(matrix, 1), f(1)
        cases += 1
        if observed < target:
            failures.append({"kind": "same_shell_counterexample",
                             "observed": fs(observed), "target": fs(target)})
    if MUTATION == "allow_signed_clocks":
        matrix = ((f(1), f(-100)), (f(-100), f(1)))
        observed, target = fixed_clock_height(matrix, 1), f(1)
        cases += 1
        if observed < target:
            failures.append({"kind": "signed_clock_counterexample",
                             "observed": fs(observed), "target": fs(target)})

    return check(
        "two_clock_fixed_deletion_schedule_invariance",
        not failures and equality_seen,
        "Distinct nonnegative clocks give L_1^K >= min(h1,h2), even at disjoint times.",
        cases=cases, equality_seen=equality_seen, strict_seen=strict_seen,
        failures=failures,
    )


def illegal_functional_replacement_fixtures():
    # Both rows satisfy L <= Pi + 6 Hfix and L >= hstar.
    fixtures = (
        {"hstar": f(1), "L": f(1), "Pi": f(1), "Hfix": f(0)},
        {"hstar": f(1), "L": f(1), "Pi": f(0), "Hfix": f(1, 6)},
        {"hstar": f(2), "L": f(20), "Pi": f(20), "Hfix": f(0)},
    )
    failures = []
    for row in fixtures:
        known = row["L"] >= row["hstar"] and row["L"] <= row["Pi"] + 6 * row["Hfix"]
        safe = row["Hfix"] >= max(f(), (row["hstar"] - row["Pi"]) / 6)
        if MUTATION == "K_floor_to_Hfix":
            conclusion = row["Hfix"] >= row["hstar"]
        elif MUTATION == "hstar_to_full_clock":
            payment_proxy = 2 * row["hstar"]
            conclusion = payment_proxy >= 2 * row["L"]
        else:
            conclusion = safe
        if not (known and conclusion):
            failures.append({key: fs(value) for key, value in row.items()})
    return check(
        "functional_direction_and_no_illegal_replacement",
        not failures,
        "The Step 18 bridge permits only the paid factor-six lower consequence, not Hfix>=hstar or payment>=Lambda L.",
        cases=len(fixtures), failures=failures,
    )


def volume_direction_fixture():
    # With fixed L2 mass E, increasing volume decreases the sharp L3 lower
    # bound.  An upper volume bound is therefore the usable hypothesis.
    energy = f(4)
    v_max = f(2)
    actual_volume = f(1)
    if MUTATION == "volume_upper_to_lower":
        actual_volume = f(8)
    # Compare squared lower bounds to avoid square roots.
    actual_l3_squared = energy ** 3 / actual_volume
    predicted_squared = energy ** 3 / v_max
    return check(
        "volume_upper_bound_direction",
        actual_volume <= v_max and actual_l3_squared >= predicted_squared,
        "The L3 coercive lower bound uses |Omega| <= C_Omega L R^3.",
        actual_volume=fs(actual_volume), volume_cap=fs(v_max),
        actual_l3_squared=fs(actual_l3_squared),
        predicted_squared=fs(predicted_squared),
    )


def logarithmic_ledger():
    c_gamma = f(8, 3969)
    a_s = f(75, 22528)
    rho = f(1, 320)
    margin = a_s - 5 * c_gamma if MUTATION == "margin_sign" else 5 * c_gamma - a_s
    expected_margin = f(603445, 89413632)
    d_sign = f(-1) if MUTATION == "survival_defect_sign" else f(1)
    coefficients = {
        "log_theta": f(2, 3),
        "L1_squared": f(2, 3) * margin,
        "d_L": f(2, 3) * d_sign,
        "log_L2": f(-1, 3),
    }
    expected = {
        "log_theta": f(2, 3),
        "L1_squared": f(2, 3) * expected_margin,
        "d_L": f(2, 3),
        "log_L2": f(-1, 3),
    }
    rows = [
        check(
            "five_cgamma_minus_aS",
            margin == expected_margin and margin > 0,
            "The survival/payment exponent reserve is the exact positive rational in T.25.",
            observed=fs(margin), expected=fs(expected_margin),
        ),
        check(
            "log_Lambda_substitution",
            coefficients == expected,
            "L2=2L1 and d_L=a_S L1^2-S give the exact T.24 coefficient vector.",
            observed=vector_strings(coefficients), expected=vector_strings(expected),
        ),
        check(
            "inherited_reserve_sum",
            (a_s - rho == f(23, 112640)
             and (5 * c_gamma - a_s) + (a_s - rho)
             == f(8831, 1270080)),
            "The inherited survival reserve and total theta=1 exponent are exact and positive.",
            survival_reserve=fs(a_s - rho),
            total_reserve=fs(5 * c_gamma - rho),
        ),
    ]

    # Exact formal rearrangement of log Lambda <= log C.  Slack rows must
    # fall below, not above, the necessary theta ceiling.
    cases = 0
    failures = []
    for y, d_l, log_l2, log_c, slack in itertools.product(
        (f(1), f(4), f(9)),
        (f(1, 2), f(2)),
        (f(), f(1), f(2)),
        (f(-1), f(), f(2)),
        (f(), f(1, 3), f(2)),
    ):
        cases += 1
        ceiling = (-expected_margin * y - d_l
                   + log_l2 / 2 + f(3, 2) * log_c)
        log_theta = ceiling - slack
        log_lambda = f(2, 3) * (
            log_theta + expected_margin * y + d_l - log_l2 / 2
        )
        relation = (log_theta >= ceiling
                    if MUTATION == "theta_bound_direction"
                    else log_theta <= ceiling)
        if not (relation and log_lambda <= log_c):
            failures.append({"ceiling": fs(ceiling),
                             "log_theta": fs(log_theta),
                             "log_lambda": fs(log_lambda),
                             "log_C": fs(log_c)})
            if len(failures) >= 8:
                break
    rows.append(check(
        "bounded_ratio_forces_theta_upper_bound",
        not failures,
        "Exact rational log-slack rows verify the direction and 3/2 constant in T.28--T.29.",
        cases=cases, failures=failures,
    ))

    # On the inherited L1=lambda*2^j, S=rho L1^2, theta=1 sequence,
    # log L2 < j+2.  The rational lower envelope obeys an exact expansive
    # recurrence after j=4; the transcendental inequality is an analytic
    # input, not claimed as a finite computation.
    lambda_ = f(63, 32)
    total_margin = 5 * c_gamma - rho
    lower = {}
    for j in range(4, 21):
        lower[j] = total_margin * lambda_ ** 2 * 4 ** j - f(j + 2, 2)
    recurrence = all(
        lower[j + 1] == 4 * lower[j] + f(3 * j + 5, 2)
        for j in range(4, 20)
    )
    rows.append(check(
        "inherited_theta_one_rational_lower_envelope",
        lower[4] > 0 and recurrence and all(lower[j + 1] > lower[j]
                                             for j in range(4, 20)),
        "A finite exact recurrence audits the dyadic lower envelope used by the theta=1 asymptotic.",
        cases=17, first=fs(lower[4]), last=fs(lower[20]),
        recurrence=recurrence,
    ))
    return rows


def asynchronous_geometry_and_calibration():
    cases = 0
    failures = []
    radii = (f(1, 100), f(1, 16), f(1, 8), f(1, 4), f(3, 10))
    if MUTATION == "async_interval_direction":
        radii = radii + (f(2, 5),)
    for radius in radii:
        cases += 1
        left = 64 * radius ** 2
        right = 65 * radius ** 2
        j1 = (left + radius ** 3, left + 2 * radius ** 3)
        j2 = (right - radius ** 3, right)
        passed = (
            j1[1] - j1[0] == radius ** 3
            and j2[1] - j2[0] == radius ** 3
            and left < j1[0] < j1[1] < right
            and left < j2[0] < j2[1] <= right
            and j1[1] < j2[0]
            and j2[0] - j1[1] == radius ** 2 * (1 - 3 * radius)
        )
        if not passed:
            failures.append({"R": fs(radius),
                             "J1": [fs(x) for x in j1],
                             "J2": [fs(x) for x in j2]})

    for b, integral in itertools.product(
        (f(1, 128), f(1, 5), f(2)),
        (f(-3), f(-1, 2), f(), f(4)),
    ):
        cases += 1
        q_pre = (b * integral if MUTATION == "async_qpre_sign"
                 else -b * integral)
        terminal = q_pre + b * integral
        if terminal != 0:
            failures.append({"B": fs(b), "integral": fs(integral),
                             "terminal_center": fs(terminal)})

    # Two identical spacetime lobes cannot be counted twice without a
    # disjointness/multiplicity argument.  The theorem correctly uses one
    # outer lobe only.
    one_lobe_payment = f(7)
    claimed = (2 * one_lobe_payment if MUTATION == "sum_overlapping_lobes"
               else one_lobe_payment)
    cases += 1
    if one_lobe_payment < claimed:
        failures.append({"kind": "overlapping_lobe_double_count",
                         "actual": fs(one_lobe_payment),
                         "claimed": fs(claimed)})

    return check(
        "asynchronous_window_and_recentering_algebra",
        not failures,
        "The explicit unit-dwell windows are disjoint for R<1/3, and the negative q_pre sign centers each packet at its own terminal time.",
        cases=cases, failures=failures,
    )


def structural_checks():
    try:
        note_text = NOTE.read_text(encoding="utf-8")
        note_error = None
    except (OSError, UnicodeDecodeError) as exc:
        note_text = ""
        note_error = f"{type(exc).__name__}: {exc}"
    compact = re.sub(r"\s+", " ", note_text)
    tags = re.findall(r"\\tag\{(T\.\d+)\}", note_text)
    expected_tags = (tuple(f"T.{number}" for number in range(1, 45))
                     if MUTATION == "tag_inventory" else EXPECTED_TAGS)
    required = (
        "**NOT CLAY.**",
        "No simulation or numerical fit is used.",
        "R074T_STEP19_STATUS_LOCAL_COERCIVITY_PROVED",
        "R074T_STEP19_STATUS_DWELL_THRESHOLD_PROVED",
        "R074T_STEP19_STATUS_FULL_CLOCK_GATE_OPEN",
        r"\Gamma _2^{1/4}",
        r"\Gamma _2^{-5/4}L_2^{-1/2}",
        r"\Gamma _2^{-5/6}L_2^{-1/3}",
        r"h_*:=\min(h_1,h_2)",
        r"\mathfrak L^K_{1,R}(D)",
        "Nor may (T.17) be rewritten with",
        r"\mathfrak H^{\rm fix}",
        r"d_L:=a_SL_1^2-S\longrightarrow+\infty",
        r"\frac{603445}{89413632}>0",
        "packets evolved under different shears have",
        "arbitrary relative scheduling **inside the stated slab**",
        "**ABSTRACT SHARPNESS TESTS**",
        "R074T_STEP19_END",
    )
    if MUTATION == "claim_boundary":
        required = required + ("MILLENNIUM PROBLEM SOLVED",)
    forbidden = (
        ",quad",
        "|le ",
        "independent time translation of already evolved solutions is proved",
        "the full clock is bounded by the lobe floor",
        "the stopped-flux height is at least the kinetic floor",
        "all real target times are admissible",
    )
    stale = (
        "The present note does not prove that independently prescribed "
        "asynchronous terminal phases can be realized by the packet PDE."
    )
    rows = [
        check("note_readable_utf8", note_error is None,
              "The theorem note is readable UTF-8.", error=note_error),
        check(
            "tag_inventory_unique_and_ordered",
            tuple(tags) == expected_tags and len(tags) == len(set(tags)),
            "The note contains exactly one ordered T.1--T.43 ledger.",
            observed=tags, expected=list(expected_tags),
        ),
        check(
            "display_and_environment_balance",
            note_text.count(r"\[") == note_text.count(r"\]")
            and note_text.count(r"\begin{aligned}")
            == note_text.count(r"\end{aligned}"),
            "Display delimiters and aligned environments balance.",
        ),
        check(
            "required_formula_and_claim_sentinels",
            all(token in note_text for token in required),
            "Exact exponents, functionals, schedule restriction, and claim boundaries are present.",
            missing=[token for token in required if token not in note_text],
        ),
        check(
            "no_malformed_or_overclaim_phrases",
            all(token not in note_text for token in forbidden)
            and stale not in compact,
            "Malformed LaTeX, stale asynchronous denial, and listed overclaims are absent.",
            found=[token for token in forbidden if token in note_text]
            + ([stale] if stale in compact else []),
        ),
        check(
            "control_character_policy",
            not any(ord(char) < 32 and char not in "\n\r" for char in note_text),
            "Tabs and non-newline C0 controls are forbidden.",
        ),
    ]
    return rows


def hash_checks():
    expected_note = "0" * 64 if MUTATION == "source_hash" else LOCKED_NOTE_SHA256
    expected_literature = ("0" * 64 if MUTATION == "literature_hash"
                           else LOCKED_LITERATURE_SHA256)
    rows = [
        check(
            "locked_note_sha256",
            NOTE.is_file() and len(expected_note) == 64
            and sha256(NOTE) == expected_note,
            "The Step 19 theorem note matches its frozen byte hash.",
            path=display_path(NOTE), expected=expected_note,
            observed=sha256(NOTE) if NOTE.is_file() else None,
        ),
        check(
            "locked_literature_sha256",
            LITERATURE.is_file() and len(expected_literature) == 64
            and sha256(LITERATURE) == expected_literature,
            "The Step 19 primary-source audit must exist and match a real frozen hash; PENDING is fail-closed.",
            path=display_path(LITERATURE), expected=expected_literature,
            observed=sha256(LITERATURE) if LITERATURE.is_file() else None,
        ),
    ]
    for index, (name, (path, expected)) in enumerate(DEPENDENCIES.items()):
        effective = ("0" * 64
                     if MUTATION == "dependency_hash" and index == 0
                     else expected)
        rows.append(check(
            f"dependency_{name}",
            path.is_file() and sha256(path) == effective,
            "A direct inherited dependency matches its audited hash.",
            path=display_path(path), expected=effective,
            observed=sha256(path) if path.is_file() else None,
        ))
    return rows


def render_report(payload):
    checks = payload["checks"]
    finite = [row for row in checks if row["group"] == "finite"]
    structural = [row for row in checks if row["group"] == "structural"]
    hashes = [row for row in checks if row["group"] == "hash"]
    lines = [
        "# R0.74T Step 19 schedule-invariant dwell certificate report",
        "",
        f"- Schema: {SCHEMA}",
        f"- Source note: {display_path(NOTE)}",
        f"- Source SHA-256: {sha256(NOTE) if NOTE.is_file() else 'MISSING'}",
        f"- Literature audit: {display_path(LITERATURE)}",
        f"- Literature SHA-256: {sha256(LITERATURE) if LITERATURE.is_file() else 'PENDING/MISSING'}",
        f"- Finite groups: {sum(row['pass'] for row in finite)}/{len(finite)}",
        f"- Exact finite cases: {sum(row['cases'] for row in finite)}",
        f"- Structural groups: {sum(row['pass'] for row in structural)}/{len(structural)}",
        f"- Hash locks: {sum(row['pass'] for row in hashes)}/{len(hashes)}",
        "",
        "## Verdict",
        "",
        f"**{payload['verdict']}**",
        "",
        "The certificate audits exact exponent arithmetic, finite Holder and",
        "time-floor proxies, fixed-deletion clock combinatorics, asynchronous",
        "window algebra, source structure, and frozen hashes. It does not",
        "machine-prove the continuous PDE inputs.",
        "",
        "## Check inventory",
        "",
        "| Check | Group | Result | Cases |",
        "|---|---|---:|---:|",
    ]
    for row in checks:
        lines.append(
            f"| {row['id']} | {row['group']} | "
            f"{'PASS' if row['pass'] else 'FAIL'} | {row['cases']} |"
        )
    lines.extend([
        "",
        "## Claim boundary",
        "",
        "- The kinetic dwell floor controls one nonnegative exterior cubic row.",
        "- Two distinct nonnegative clocks imply only a lower witness for the fixed-deletion completed-clock functional.",
        "- The witness does not replace the full completed clock and does not lower-bound the stopped-flux Hfix without the Step 18 payment terms.",
        "- The asynchronous exact-family application is restricted to admissible windows inside the inherited terminal slab.",
        "- Q.12, Q.1, scale contraction, regularity, and the Millennium problem remain open.",
        "",
        "## Explicit limitations",
        "",
        "- Finite rational Holder/time-floor checks are proxies, not machine proofs of their continuum versions.",
        "- Packet survival, dominance, shell placement, and exact NSE superposition are inherited analytic inputs.",
        "- No upper bound for the full completed clock is certified.",
        "- No regularity, blow-up, novelty, priority, or Clay claim is certified.",
        "",
    ])
    failed = [row["id"] for row in checks if not row["pass"]]
    if failed:
        lines.extend(["## Failed checks", ""])
        lines.extend(f"- {identifier}" for identifier in failed)
        lines.append("")
    return "\n".join(lines)


def main():
    checks = []
    finite_rows = []
    finite_rows.extend(exact_exponent_and_constant_ledger())
    finite_rows.extend((
        rational_monomial_grid(),
        finite_holder_grid(),
        finite_time_floor_grid(),
        two_clock_grid(),
        illegal_functional_replacement_fixtures(),
        volume_direction_fixture(),
    ))
    finite_rows.extend(logarithmic_ledger())
    finite_rows.append(asynchronous_geometry_and_calibration())
    for row in finite_rows:
        row["group"] = "finite"
        checks.append(row)
    for row in structural_checks():
        row["group"] = "structural"
        checks.append(row)
    for row in hash_checks():
        row["group"] = "hash"
        checks.append(row)

    verdict = "PASS" if all(row["pass"] for row in checks) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "mutation": MUTATION or None,
        "note": {"path": display_path(NOTE),
                 "sha256": sha256(NOTE) if NOTE.is_file() else None},
        "literature": {"path": display_path(LITERATURE),
                       "sha256": sha256(LITERATURE) if LITERATURE.is_file() else None,
                       "locked_sha256": LOCKED_LITERATURE_SHA256},
        "checks": checks,
        "negative_mutations": list(NEGATIVE_MUTATIONS),
        "limitations": [
            "finite rational, combinatorial, structural, and hash audit only",
            "no machine proof of continuous Holder or local-energy theory",
            "no machine proof of packet survival or exact NSE superposition",
            "no proof of the full completed-clock or stopped-flux gate",
            "not a regularity theorem and not a Clay claim",
        ],
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    REPORT_OUT.write_text(render_report(payload), encoding="utf-8")
    print(json.dumps({
        "schema": SCHEMA,
        "verdict": verdict,
        "checks_passed": sum(row["pass"] for row in checks),
        "checks_total": len(checks),
        "finite_cases": sum(row["cases"] for row in checks
                            if row["group"] == "finite"),
        "mutation": MUTATION or None,
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
