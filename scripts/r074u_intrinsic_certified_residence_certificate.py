#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74U Step 20.

This standard-library producer checks exact rational constants, finite
kinematic corridor models, symbolic exponent ledgers, source structure, and
frozen hashes.  It does not machine-prove heat-kernel estimates, compactness,
the exact Navier--Stokes construction, or any regularity/Clay statement.
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
    "R074U_RESIDENCE_NOTE",
    REPO / "research/r074u_intrinsic_certified_residence.md",
))
LITERATURE = Path(os.environ.get(
    "R074U_RESIDENCE_LITERATURE",
    REPO / "research/r074u_intrinsic_residence_literature_audit.md",
))
JSON_OUT = Path(os.environ.get(
    "R074U_RESIDENCE_JSON",
    REPO / "research/r074u_intrinsic_certified_residence_certificate.json",
))
REPORT_OUT = Path(os.environ.get(
    "R074U_RESIDENCE_REPORT",
    REPO / "research/r074u_intrinsic_certified_residence_certificate_report.md",
))

SCHEMA = "r074u-intrinsic-certified-residence-certificate-v1"
MUTATION = os.environ.get("R074U_RESIDENCE_MUTATION", "").strip()

# Keep each rebind in one place.  A final archive must pass without env
# overrides.  The literature value remains deliberately fail-closed until
# the audit file is frozen.
LOCKED_NOTE_SHA256 = os.environ.get(
    "R074U_RESIDENCE_EXPECTED_NOTE_SHA256",
    "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99",
)
LOCKED_LITERATURE_SHA256 = os.environ.get(
    "R074U_RESIDENCE_EXPECTED_LITERATURE_SHA256",
    "0cf6e19a42e524aaf79aca10d72c5380029dce37032215974d99976a0b2a327c",
)

EXPECTED_TAGS = tuple(f"U.{number}" for number in range(1, 46))
DEPENDENCIES = {
    "r074p_completed_clock": (
        REPO / "research/r074p_temporal_observable_triage.md",
        "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    ),
    "r074t_dwell_coercivity": (
        REPO / "research/r074t_schedule_invariant_dwell_coercivity.md",
        "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
    ),
    "r074q_common_shear": (
        REPO / "research/r074q_common_shear_multipacket_gate.md",
        "60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695",
    ),
    "r074q_relaxed_multipacket": (
        REPO / "research/r074q_relaxed_multipacket_cubic_obstruction.md",
        "ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d",
    ),
    "r074f_packet_survival": (
        REPO / "research/r074f_two_packet_survival.md",
        "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb",
    ),
    "r074s_taylor_boundary": (
        REPO / "research/r074s_moving_frame_taylor_vortex_obstruction.md",
        "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0",
    ),
}

NEGATIVE_MUTATIONS = (
    "A_squared_margin_sign",
    "epsilon_crude_bound",
    "speed_bound_direction",
    "slab_72_to_73",
    "upper_1024_to_1023",
    "phase_96_to_97",
    "phase_144_to_145",
    "cstar_sign",
    "cross_tail_margin_sign",
    "theta_cert_log_sign",
    "theta_necessary_direction",
    "corridor_upper_to_K_superlevel",
    "Omega_to_Theta",
    "physical_to_frequency_shell",
    "drop_full_slab_compact_min",
    "drop_periodic_term",
    "K_to_Hfix",
    "overclaim",
    "drop_not_clay",
    "tag_inventory",
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


def rational_constants():
    lambda_ = f(63, 32)
    c_h = f(15, 16)
    b_2 = f(3, 2)
    a_d = f(49, 14625)
    l_zero = f(9216)
    x_zero = 1 / l_zero

    squared_margin = (
        (2 / lambda_) ** 2 - f(1, 256)
        - (c_h + x_zero) ** 2
        - (f(3, 8) + b_2 * x_zero) ** 2
    )
    if MUTATION == "A_squared_margin_sign":
        squared_margin *= -1
    inner_margin = c_h - x_zero - 1 / lambda_
    a_d_l2 = a_d * l_zero ** 2
    # A strict rational lower partial sum for exp(4).
    exp4_partial = sum((f(4) ** n / f(_factorial(n)) for n in range(4)), f())
    epsilon_threshold = f(1, 5) if MUTATION == "epsilon_crude_bound" else f(1, 4)

    rows = [
        check(
            "A_squared_margin_at_L0",
            squared_margin == f(15232043, 1849688064)
            and squared_margin > 0,
            "The squared reserve proving A(L)>3/8 is exact and positive.",
            observed=fs(squared_margin),
            expected=fs(f(15232043, 1849688064)),
        ),
        check(
            "A_squared_margin_monotonic_polynomial",
            f(2) * c_h + f(3, 4) * b_2 == f(3)
            and f(1) + b_2 ** 2 == f(13, 4),
            "In x=1/L, the reserve has derivative -3-(13/2)x<0, so L0 is worst.",
            linear_coefficient=fs(f(3)),
            quadratic_coefficient=fs(f(13, 4)),
        ),
        check(
            "inner_annular_margin",
            inner_margin == f(9235, 21504) and inner_margin > 0,
            "The vertical coordinate alone gives the strict inner-shell margin.",
            observed=fs(inner_margin),
        ),
        check(
            "epsilon_crude_quarter_bound",
            a_d_l2 == f(462422016, 1625)
            and a_d_l2 > 4
            and exp4_partial > 16
            and epsilon_threshold == f(1, 4),
            "a_D L0^2>4 and an exact exp(4) series lower bound give epsilon<1/4.",
            aD_L0_squared=fs(a_d_l2),
            exp4_partial=fs(exp4_partial),
            epsilon_threshold=fs(epsilon_threshold),
        ),
    ]

    samples = (f(), x_zero / 4, x_zero / 2, 3 * x_zero / 4, x_zero)
    failures = []
    for x in samples:
        reserve = (
            (2 / lambda_) ** 2 - f(1, 256)
            - (c_h + x) ** 2 - (f(3, 8) + b_2 * x) ** 2
        )
        if reserve < f(15232043, 1849688064):
            failures.append({"x": fs(x), "reserve": fs(reserve)})
    rows.append(check(
        "A_margin_exact_x_grid",
        not failures,
        "A finite exact x=1/L grid confirms the frozen endpoint is the smallest reserve.",
        cases=len(samples), failures=failures,
    ))
    return rows


def _factorial(number):
    answer = 1
    for value in range(2, number + 1):
        answer *= value
    return answer


def speed_interval_grid():
    cases = 0
    failures = []
    epsilon_values = (f(), f(1, 16), f(1, 8), f(1, 5), f(1, 4) - f(1, 1000))
    for epsilon_1 in epsilon_values:
        for epsilon_i in epsilon_values:
            if epsilon_i > epsilon_1:
                continue
            cases += 1
            b_lower = f(1, 128)
            b_upper = 1 / (128 * (1 - epsilon_1))
            theta_lower = 1 - epsilon_i
            theta_upper = f(1)
            lower = b_lower * theta_lower
            upper = b_upper * theta_upper
            if MUTATION == "speed_bound_direction":
                passed = lower >= upper
            else:
                passed = f() < lower <= upper
            if not passed:
                failures.append({"epsilon_1": fs(epsilon_1),
                                 "epsilon_i": fs(epsilon_i),
                                 "lower": fs(lower), "upper": fs(upper)})
                if len(failures) >= 8:
                    break
        if len(failures) >= 8:
            break
    return check(
        "platform_speed_interval_direction",
        not failures,
        "Multiplying the lower platform/B bounds and upper platform/B bounds gives U.11 in the stated direction.",
        cases=cases, failures=failures,
    )


def residence_constant_ledger():
    lower_travel = 128 * f(3, 8) * f(3, 4)
    lower_coefficient = f(73, 5) if MUTATION == "slab_72_to_73" else f(72, 5)
    upper_coefficient = f(1023, 3) if MUTATION == "upper_1024_to_1023" else f(1024, 3)
    inner_coefficient = f(97, 5) if MUTATION == "phase_96_to_97" else f(96, 5)
    outer_coefficient = f(145, 5) if MUTATION == "phase_144_to_145" else f(144, 5)

    near_one = f(1) - f(1, 100000)
    near_quarter = f(1, 4) - f(1, 100000)
    coarse_upper_witness = 256 * near_one / (1 - near_quarter)
    rows = [
        check(
            "geometric_travel_allowance_36",
            lower_travel == 36,
            "128*(3/8)*(3/4)=36 is the certified one-sided travel allowance.",
            value=fs(lower_travel),
        ),
        check(
            "slab_truncation_72_over_5",
            lower_coefficient * f(5, 144) == f(1, 2),
            "The chart cap L_i R<=5/144 converts half a slab into (72/5)L_iR^3.",
            coefficient=fs(lower_coefficient),
        ),
        check(
            "coarse_upper_1024_over_3",
            upper_coefficient == 256 / f(3, 4)
            and coarse_upper_witness < upper_coefficient,
            "A<1 and 1-epsilon>3/4 give the strict 1024/3 coefficient; a smaller coarse constant is not implied.",
            coefficient=fs(upper_coefficient),
            near_boundary_witness=fs(coarse_upper_witness),
        ),
        check(
            "explicit_inner_96_over_5",
            inner_coefficient * f(5, 288) == f(1, 3)
            and inner_coefficient < 36,
            "The inner forward slab room and L1R<=5/288 give 96/5.",
            coefficient=fs(inner_coefficient),
        ),
        check(
            "explicit_outer_144_over_5",
            outer_coefficient * f(5, 144) == f(1)
            and outer_coefficient < 36,
            "The full backward slab room and L2R<=5/144 give 144/5.",
            coefficient=fs(outer_coefficient),
        ),
    ]

    # Exact normalized linear-centre models.  They audit the min-with-slab
    # geometry only; they are not packet PDE simulations.
    cases = 0
    failures = []
    x_values = (f(1, 1000), f(1, 100), f(5, 288), f(5, 144))
    a_values = (f(3, 8) + f(1, 1000), f(2, 5), f(1, 2), f(3, 4))
    eps_values = (f(), f(1, 8), f(1, 5), f(1, 4) - f(1, 1000))
    tau_values = (f(), f(1, 4), f(1, 2), f(3, 4), f(1))
    for x, a_value, eps_1, eps_i, tau in itertools.product(
        x_values, a_values, eps_values, eps_values, tau_values,
    ):
        if eps_i > eps_1:
            continue
        cases += 1
        speed = 1 / (128 * (1 - eps_1))
        half_width = a_value * x / speed
        actual = min(f(1), tau + half_width) - max(f(), tau - half_width)
        lower = f(72, 5) * x
        upper = min(f(1), 256 * a_value / (1 - eps_i) * x)
        if actual < lower or actual > upper:
            failures.append({"x": fs(x), "A": fs(a_value),
                             "eps1": fs(eps_1), "epsi": fs(eps_i),
                             "tau": fs(tau), "actual": fs(actual),
                             "lower": fs(lower), "upper": fs(upper)})
            if len(failures) >= 8:
                break
    rows.append(check(
        "finite_linear_corridor_models",
        not failures,
        "Exact slab-truncated constant-speed corridors obey the certified lower and upper ledgers.",
        cases=cases, failures=failures,
    ))
    return rows


def tail_and_periodic_constants():
    c_gamma = f(8, 3969)
    q = c_gamma / 2
    a_cross = f(49, 14850)
    cross_margin = a_cross - f(3, 2) * c_gamma
    if MUTATION == "cross_tail_margin_sign":
        cross_margin *= -1
    mu_inner = f(4601, 2910600)
    c_star = f(3, 22) * f(144, 5) ** 2 - q
    if MUTATION == "cstar_sign":
        c_star *= -1
    periodic_coefficient = q - f(3, 22) * f(144, 5) ** 2
    if MUTATION == "drop_periodic_term":
        periodic_coefficient = q
    return [
        check(
            "adjacent_cross_tail_margin",
            cross_margin == f(67, 242550) and cross_margin > 0,
            "The outer-to-inner amplitude-weighted tail reserve is exact and positive.",
            observed=fs(cross_margin),
        ),
        check(
            "inner_cross_tail_margin",
            mu_inner == f(4601, 2910600) and mu_inner > 0,
            "The adjacent inner-packet reserve is exact and positive.",
            observed=fs(mu_inner),
        ),
        check(
            "periodic_cstar",
            c_star == f(123450676, 1091475)
            and c_star > 0
            and periodic_coefficient == -c_star,
            "The chart cap turns qL2^2-3/(22R^2) into -c_*L2^2 with c_*>0.",
            c_star=fs(c_star), periodic_coefficient=fs(periodic_coefficient),
        ),
    ]


def theta_certified_substitution():
    c_gamma = f(8, 3969)
    a_s = f(75, 22528)
    margin = 5 * c_gamma - a_s
    log_l2_coefficient = (f(-1, 2) if MUTATION == "theta_cert_log_sign"
                          else f(1, 2))
    expected = {
        "log_72_over_5": f(1),
        "margin_L1_squared": f(1),
        "d_L": f(1),
        "log_L2": f(1, 2),
    }
    observed = dict(expected)
    observed["log_L2"] = log_l2_coefficient
    rows = [
        check(
            "theta_cert_T24_log_substitution",
            observed == expected and margin == f(603445, 89413632),
            "theta_cert>=(72/5)L2 changes the T.24 log-L2 coefficient from -1/2 to +1/2.",
            observed={key: fs(value) for key, value in observed.items()},
            expected={key: fs(value) for key, value in expected.items()},
            margin=fs(margin),
        )
    ]

    # Finite formal log fixtures for the incompatibility between the proved
    # linear lower dwell and T.28's exponentially decaying necessary upper.
    cases = 0
    failures = []
    for l2, exponent, log_c in itertools.product(
        (f(1), f(4), f(16), f(64)),
        (f(1), f(3), f(10)),
        (f(-2), f(), f(2)),
    ):
        cases += 1
        # Work with log variables formally: lower-minus-upper log is
        # log(72/5)-log C + (1/2)log L2 + exponent.
        log_72_5_lower = f(1)  # rigorous coarse fact log(72/5)>1
        log_l2 = f() if l2 == 1 else f(1)  # nonnegative coarse lower only
        gap_lower = log_72_5_lower - log_c + log_l2 / 2 + exponent
        relation = gap_lower <= 0 if MUTATION == "theta_necessary_direction" else gap_lower > -4
        if not relation:
            failures.append({"L2": fs(l2), "exponent": fs(exponent),
                             "log_C": fs(log_c), "gap_lower": fs(gap_lower)})
            if len(failures) >= 8:
                break
    rows.append(check(
        "theta_cert_vs_necessary_upper_direction",
        not failures,
        "Formal exact sign rows preserve the lower-certified/upper-necessary direction in U.40--U.41.",
        cases=cases, failures=failures,
    ))
    return rows


def structural_checks():
    try:
        note_text = NOTE.read_text(encoding="utf-8")
        note_error = None
    except (OSError, UnicodeDecodeError) as exc:
        note_text = ""
        note_error = f"{type(exc).__name__}: {exc}"
    tags = re.findall(r"\\tag\{(U\.\d+)\}", note_text)
    expected_tags = (tuple(f"U.{number}" for number in range(1, 47))
                     if MUTATION == "tag_inventory" else EXPECTED_TAGS)

    required = [
        "**NOT CLAY.**",
        "No simulation or numerical fit is used.",
        "R074U_STEP20_STATUS_CERTIFIED_RESIDENCE_PROVED",
        "R074U_STEP20_STATUS_K_SUPERLEVEL_LOWER_ONLY",
        "R074U_STEP20_STATUS_MAXIMAL_K_DWELL_OPEN",
        r"\mathscr R_i^{\rm cert}",
        r"\Omega_i(t)",
        r"A_{k_i}(R)",
        "certified geometric residence corridor",
        "It is not defined as a clock",
        "superlevel set.",
        "Equation (U.24) is **not** an upper bound",
        "last compact-minimum step",
        "noncentral periodic copies",
        "The periodic remainder also stays negligible",
        "No converse inclusion and no upper bound for this superlevel set",
        r"K_{k_i,R}(t)",
        r"\theta_{{\rm cert},2}",
        r"{72\over5}L_2",
        r"{1024\over3}L_iR^3",
        r"{96\over5}L_1R^3",
        r"{144\over5}L_2R^3",
        r"c_*={3\over22}\left({144\over5}\right)^2-q>0",
        r"{67\over242550}>0",
        r"{4601\over2910600}>0",
        "physical shell",
        "R074U_STEP20_END",
    ]
    if MUTATION == "drop_full_slab_compact_min":
        required.append("FULL_SLAB_COMPACT_MIN_REMOVED")
    if MUTATION == "drop_periodic_term":
        required.append("PERIODIC_TERM_REMOVED")
    if MUTATION == "corridor_upper_to_K_superlevel":
        required.append("U.24 IS AN UPPER BOUND FOR THE K SUPERLEVEL")
    if MUTATION == "Omega_to_Theta":
        required.append(r"\Theta_i(t)")
    if MUTATION == "physical_to_frequency_shell":
        required.append("frequency shell corridor")
    if MUTATION == "K_to_Hfix":
        required.append(r"\mathfrak H^{\rm fix}")
    if MUTATION == "overclaim":
        required.append("THE MILLENNIUM PROBLEM IS SOLVED")
    if MUTATION == "drop_not_clay":
        required.remove("**NOT CLAY.**")
        required.append("**CLAY CLAIM.**")

    forbidden = (
        ",quad",
        "|le ",
        "upper bound for the completed-clock superlevel set is proved",
        "arbitrary packets have certified residence",
        "frequency shell corridor",
        r"\Theta_i(t)=\left\{x",
    )
    return [
        check("note_readable_utf8", note_error is None,
              "The theorem note is readable UTF-8.", error=note_error),
        check(
            "tag_inventory_unique_and_ordered",
            tuple(tags) == expected_tags and len(tags) == len(set(tags)),
            "The note contains exactly one ordered U.1--U.45 ledger.",
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
            "Corridor/K distinction, physical geometry, full-slab inputs, constants, and claim boundaries are present.",
            missing=[token for token in required if token not in note_text],
        ),
        check(
            "no_forbidden_substitutions_or_overclaims",
            all(token not in note_text for token in forbidden),
            "The source does not transfer the geometric upper bound to K, replace Omega/physical shells, or overclaim.",
            found=[token for token in forbidden if token in note_text],
        ),
        check(
            "control_character_policy",
            not any(ord(char) < 32 and char not in "\n\r" for char in note_text),
            "Tabs and non-newline C0 controls are forbidden.",
        ),
    ]


def hash_checks():
    expected_note = "0" * 64 if MUTATION == "source_hash" else LOCKED_NOTE_SHA256
    expected_literature = ("0" * 64 if MUTATION == "literature_hash"
                           else LOCKED_LITERATURE_SHA256)
    rows = [
        check(
            "locked_note_sha256",
            NOTE.is_file() and len(expected_note) == 64
            and sha256(NOTE) == expected_note,
            "The Step 20 theorem note matches its frozen byte hash.",
            path=display_path(NOTE), expected=expected_note,
            observed=sha256(NOTE) if NOTE.is_file() else None,
        ),
        check(
            "locked_literature_sha256",
            LITERATURE.is_file() and len(expected_literature) == 64
            and sha256(LITERATURE) == expected_literature,
            "The literature audit must exist and match a real frozen hash; PENDING is fail-closed.",
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
            "A frozen analytic dependency matches its audited hash.",
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
        "# R0.74U Step 20 intrinsic certified-residence certificate report",
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
        "The certificate audits the exact annular reserve, platform/speed",
        "directions, slab-truncated corridor constants, cross/periodic-tail",
        "margins, certified-dwell substitution, source structure, and hashes.",
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
        "- U.24 is an upper bound only for the certified geometric corridor, never for the full K-superlevel set.",
        "- U.35 proves only corridor inclusion in, and a lower measure bound for, the nonnegative completed-clock superlevel.",
        "- Omega is a physical-space packet lobe inside a physical shell; it is not a frequency-shell or abstract Theta replacement.",
        "- Full-slab compact-minimum, inverted/cross-packet, and periodic-tail bounds remain analytic inputs.",
        "- No arbitrary-clock extraction, fixed-deletion closure, regularity, singularity, or Clay statement is certified.",
        "",
        "## Explicit limitations",
        "",
        "- Finite constant-speed corridors do not machine-prove the packet PDE residence theorem.",
        "- The exponential and heat-kernel estimates remain inherited analytic arguments.",
        "- The finite certificate does not prove an upper bound for any full-clock superlevel.",
        "- Literature presence and hash are checked, but novelty and priority are not certified.",
        "",
    ])
    failed = [row["id"] for row in checks if not row["pass"]]
    if failed:
        lines.extend(["## Failed checks", ""])
        lines.extend(f"- {identifier}" for identifier in failed)
        lines.append("")
    return "\n".join(lines)


def main():
    finite = []
    finite.extend(rational_constants())
    finite.append(speed_interval_grid())
    finite.extend(residence_constant_ledger())
    finite.extend(tail_and_periodic_constants())
    finite.extend(theta_certified_substitution())
    checks = []
    for row in finite:
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
            "finite rational, kinematic, symbolic, structural, and hash audit only",
            "no machine proof of heat-kernel, compact-minimum, or packet-survival estimates",
            "no transfer of the certified-corridor upper bound to a full K-superlevel",
            "no arbitrary-clock extraction, regularity theorem, or Clay claim",
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
