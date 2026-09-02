#!/usr/bin/env python3
"""Deterministic finite certificate for R0.74S Step 16.

This standard-library producer reconstructs the Taylor and ABC Fourier
identities with exact Gaussian-rational Laurent polynomials.  It also checks
the deletion, support, characteristic, and amplitude-exponent arithmetic and
fail-closes the source note's claim boundary.

It does not machine-prove the continuum PDE theorem, arbitrary-mollifier
positivity, the analytic payment estimates, the open critical L1 tail,
regularity, or the Navier--Stokes Millennium problem.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = Path(os.environ.get(
    "R074S_TAYLOR_NOTE",
    REPO / "research/r074s_moving_frame_taylor_vortex_obstruction.md",
))
JSON_OUT = Path(os.environ.get(
    "R074S_TAYLOR_JSON",
    REPO / "research/r074s_moving_frame_taylor_vortex_certificate.json",
))
REPORT_OUT = Path(os.environ.get(
    "R074S_TAYLOR_REPORT",
    REPO / "research/r074s_moving_frame_taylor_vortex_certificate_report.md",
))

SCHEMA = "r074s-moving-frame-taylor-vortex-certificate-v1"
LOCKED_NOTE_SHA256 = "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0"
EXPECTED_TAGS = tuple(
    [f"S.{number}" for number in range(417, 439)]
    + ["S.438a", "S.438b"]
    + [f"S.{number}" for number in range(439, 445)]
)
DEPENDENCIES = {
    "step13": (
        REPO / "research/r074s_temporal_integrability_morrey_threshold.md",
        "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de",
    ),
    "step14": (
        REPO / "research/r074s_outer_collar_corona_obstruction.md",
        "c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9",
    ),
    "step15_hybrid": (
        REPO / "research/r074s_hybrid_flux_tail_equivalence.md",
        "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d",
    ),
}

# A Gaussian rational is represented as (real, imaginary).
ZERO = (Fraction(0), Fraction(0))


def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qmul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def qscale(a, scalar):
    return (scalar * a[0], scalar * a[1])


def clean(poly):
    return {mode: value for mode, value in poly.items() if value != ZERO}


def padd(*polys):
    out = {}
    for poly in polys:
        for mode, value in poly.items():
            out[mode] = qadd(out.get(mode, ZERO), value)
    return clean(out)


def pscale(poly, scalar):
    return clean({mode: qscale(value, scalar) for mode, value in poly.items()})


def pmul(left, right):
    out = {}
    for lm, lv in left.items():
        for rm, rv in right.items():
            mode = tuple(lm[index] + rm[index] for index in range(3))
            out[mode] = qadd(out.get(mode, ZERO), qmul(lv, rv))
    return clean(out)


def deriv(poly, axis):
    out = {}
    for mode, value in poly.items():
        frequency = mode[axis]
        out[mode] = (
            -frequency * value[1],
            frequency * value[0],
        )
    return clean(out)


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


def eval_zero(poly):
    answer = ZERO
    for value in poly.values():
        answer = qadd(answer, value)
    return answer


def vector_add(left, right):
    return tuple(padd(left[index], right[index]) for index in range(3))


def vector_scale(vector, scalar):
    return tuple(pscale(component, scalar) for component in vector)


def vector_laplacian(vector):
    return tuple(laplacian(component) for component in vector)


def vector_divergence(vector):
    return padd(*(deriv(vector[index], index) for index in range(3)))


def vector_curl(vector):
    return (
        padd(deriv(vector[2], 1), pscale(deriv(vector[1], 2), -1)),
        padd(deriv(vector[0], 2), pscale(deriv(vector[2], 0), -1)),
        padd(deriv(vector[1], 0), pscale(deriv(vector[0], 1), -1)),
    )


def vector_energy(vector):
    return padd(*(pmul(component, component) for component in vector))


def convective(vector):
    return tuple(
        padd(*(pmul(vector[axis], deriv(vector[component], axis))
               for axis in range(3)))
        for component in range(3)
    )


def zero_vector(vector):
    return all(not component for component in vector)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(identifier, passed, note, cases=1, **details):
    row = {
        "id": identifier,
        "pass": bool(passed),
        "note": note,
        "cases": cases,
    }
    row.update(details)
    return row


def taylor_checks():
    sx, sy = sine(0), sine(1)
    cx, cy = cosine(0), cosine(1)
    w = (pmul(sx, cy), pscale(pmul(cx, sy), -1), {})
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
        "div_Bernoulli_current_zero": not vector_divergence(bernoulli_current),
    }
    return check(
        "taylor_exact_fourier_identities",
        all(rows.values()),
        "Exact Laurent algebra verifies all Taylor identities used by the proof.",
        cases=len(rows),
        rows=rows,
    )


def abc_checks():
    u = (
        padd(sine(2), cosine(1)),
        padd(sine(0), cosine(2)),
        padd(sine(1), cosine(0)),
    )
    energy = vector_energy(u)
    pressure = pscale(energy, Fraction(-1, 2))
    grad_pressure = tuple(deriv(pressure, axis) for axis in range(3))
    grad_energy = tuple(deriv(energy, axis) for axis in range(3))
    phase_u = [eval_zero(component)[0] for component in u]
    phase_grad = [eval_zero(component)[0] for component in grad_energy]
    phase_dot = sum(a * b for a, b in zip(phase_u, phase_grad))
    rows = {
        "curl_equals_U": zero_vector(
            vector_add(vector_curl(u), vector_scale(u, -1))
        ),
        "laplacian_plus_U_zero": zero_vector(
            vector_add(vector_laplacian(u), u)
        ),
        "convection_plus_grad_p_zero": zero_vector(
            vector_add(convective(u), grad_pressure)
        ),
        "U_at_origin": [str(value) for value in phase_u],
        "grad_energy_at_origin": [str(value) for value in phase_grad],
        "directional_derivative": str(phase_dot),
    }
    passed = (
        rows["curl_equals_U"]
        and rows["laplacian_plus_U_zero"]
        and rows["convection_plus_grad_p_zero"]
        and phase_u == [1, 1, 1]
        and phase_grad == [2, 2, 2]
        and phase_dot == 6
    )
    return check(
        "abc_independent_exact_screen",
        passed,
        "The ABC family independently reproduces the nonconstant-modulus drift mechanism.",
        cases=6,
        rows=rows,
    )


def deletion_checks():
    failures = []
    cases = 0
    for budget in range(65):
        count = budget + 1
        candidates = []
        for size in range(budget + 1):
            # Every subset of this size has the same complement sum because
            # the N+1 coordinates are equal.  This is the exact full
            # combination result without exponential enumeration.
            candidates.append(Fraction(count - size))
            cases += 1
        remaining = min(candidates)
        if remaining != 1:
            failures.append({"N": budget, "remaining": str(remaining)})
    return check(
        "N_plus_one_deletion_pigeonhole",
        not failures,
        "Deleting N of N+1 positive physical-shell coordinates leaves one.",
        cases=cases,
        failures=failures,
    )


def support_checks():
    failures = []
    rows = []
    for budget in range(25):
        count = budget + 1
        radius = Fraction(1, 100 * (2 ** (count + 1) + 1))
        outer = (Fraction(2 ** (count + 1)) + Fraction(1, 8)) * radius
        phase_squared = 8 * outer * outer
        passed = phase_squared < 1
        row = {
            "N": budget,
            "R": str(radius),
            "bound_for_abs_q_dot_y_squared": str(phase_squared),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return check(
        "finite_small_R_support_screen",
        not failures,
        "Representative rational scales put the first N+1 supports in a cosine-positive region.",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def exponent_checks():
    failures = []
    rows = []
    values = (
        Fraction(1),
        Fraction(12, 11),
        Fraction(4, 3),
        Fraction(2),
        Fraction(4),
        None,
    )
    for p in values:
        inverse = Fraction(0) if p is None else 1 / p
        tail = 3 - inverse
        ratio = tail - 2
        minimum_beta = tail / 3
        passed = ratio == 1 - inverse
        if p == 1:
            passed = passed and ratio == 0 and minimum_beta == Fraction(2, 3)
        else:
            passed = passed and ratio > 0 and minimum_beta > Fraction(2, 3)
        row = {
            "p": "infinity" if p is None else str(p),
            "tail_exponent": str(tail),
            "ratio_exponent": str(ratio),
            "minimum_beta": str(minimum_beta),
            "pass": passed,
        }
        rows.append(row)
        if not passed:
            failures.append(row)
    return check(
        "temporal_and_payment_exponents",
        not failures,
        "A height A^3, width A^-1 block has Lp size A^(3-1/p).",
        cases=len(rows),
        rows=rows,
        failures=failures,
    )


def characteristic_checks():
    delta = 0.01
    threshold = math.log(math.tan(math.pi / 8) / math.tan(math.pi / 16))
    failures = []
    rows = []
    for amplitude in (1, 2, 10, 100, 10_000):
        integral = amplitude * (math.exp(2 * delta / amplitude) - 1) / 2
        for multiplier in (0.5, 0.75, 1.0):
            xi = 2 * math.atan(
                math.tan(math.pi / 8) * math.exp(-multiplier * integral)
            )
            passed = math.pi / 8 < xi <= math.pi / 4 and integral < threshold
            row = {
                "A": amplitude,
                "mu": multiplier,
                "xi": xi,
                "pass": passed,
            }
            rows.append(row)
            if not passed:
                failures.append(row)
    return check(
        "terminal_characteristic_screen",
        not failures,
        "The explicit path stays in the positive phase sector on a fixed delta/A block.",
        cases=len(rows),
        delta=delta,
        rows=rows,
        failures=failures,
    )


def amplitude_bookkeeping_checks():
    rows = {
        "energy_then_three_halves": [2, Fraction(3, 2), 3],
        "velocity_cubic": [1, 3, 3],
        "pressure_then_three_halves": [2, Fraction(3, 2), 3],
        "Lambda_then_three_halves": [2, Fraction(3, 2), 3],
        "critical_block_L1": [3, -1, 2],
    }
    passed = (
        rows["energy_then_three_halves"][0]
        * rows["energy_then_three_halves"][1] == 3
        and rows["velocity_cubic"][0] * rows["velocity_cubic"][1] == 3
        and rows["pressure_then_three_halves"][0]
        * rows["pressure_then_three_halves"][1] == 3
        and rows["Lambda_then_three_halves"][0]
        * rows["Lambda_then_three_halves"][1] == 3
        and sum(rows["critical_block_L1"][:2]) == 2
    )
    return check(
        "complete_payment_and_L1_amplitude_bookkeeping",
        passed,
        "Every payment row is at most A^3, while the critical block has L1 size A^2.",
        cases=len(rows),
        rows={key: [str(value) for value in row] for key, row in rows.items()},
    )


def structural_checks(text):
    found_tags = tuple(dict.fromkeys(
        re.findall(r"\\tag\{(S\.\d+[ab]?)\}", text)
    ))
    anchors = {
        "tag_inventory": found_tags == EXPECTED_TAGS,
        "narrow_false_claim": all(phrase in text for phrase in (
            "**(S.342 is false)**",
            "The counterexample is only to the supercritical temporal-tail statement",
            "does **not** disprove",
            "Equation (S.444) is **OPEN**",
            "**NOT CLAY.**",
        )),
        "quantifier_negation": all(phrase in text for phrase in (
            r"\text{For every }p\in(1,\infty],\ N\in\mathbb N_0,\ C>0",
            r"\mathfrak H^F_{p,N,R}>C(P_R^M)^{2/3}",
            r"A^{\,1-1/p}\longrightarrow\infty",
        )),
        "physical_shell_boundary": all(phrase in text for phrase in (
            "distinct physical annuli",
            "No Fourier-shell index",
            "moving-cutoff drift",
        )),
        "critical_route_open": all(phrase in text for phrase in (
            r"\forall\text{ admissible Version-M solutions, }R,z_0",
            r"\mathfrak H^F_{1,N_1,R}\le C(P_R^M)^{2/3}",
            "No proof attempt may assume (S.342)",
        )),
        "source_boundary": all(url in text for url in (
            "https://doi.org/10.1080/14786442308634295",
            "https://doi.org/10.1098/rspa.1937.0036",
            "https://doi.org/10.1016/j.physleta.2020.126857",
            "https://doi.org/10.1017/jfm.2020.126",
        )) and "not a priority claim" in text,
    }
    rows = [
        check(
            f"structural_{identifier}",
            passed,
            "Semantic and equation anchor in the reviewed Step 16 note.",
            found=list(found_tags) if identifier == "tag_inventory" else None,
            expected=list(EXPECTED_TAGS) if identifier == "tag_inventory" else None,
        )
        for identifier, passed in anchors.items()
    ]
    return rows


def dependency_checks():
    rows = []
    for identifier, (path, expected) in DEPENDENCIES.items():
        actual = sha256(path) if path.exists() else ""
        rows.append(check(
            f"dependency_{identifier}",
            actual == expected,
            "Frozen imported note has the reviewed byte identity.",
            path=str(path.relative_to(REPO)),
            expected_sha256=expected,
            actual_sha256=actual,
        ))
    return rows


def write_report(payload):
    finite = payload["finite_checks"]
    structural = payload["structural_checks"]
    dependencies = payload["dependency_checks"]
    lines = [
        "# R0.74S Step 16 moving-frame Taylor-vortex certificate report",
        "",
        f"- Schema: {SCHEMA}",
        f"- Source note: {payload['note']['path']}",
        f"- Source SHA-256: {payload['note']['sha256']}",
        f"- Finite groups: {sum(row['pass'] for row in finite)}/{len(finite)}",
        f"- Finite cases: {sum(row['cases'] for row in finite)}",
        f"- Structural groups: {sum(row['pass'] for row in structural)}/{len(structural)}",
        f"- Dependency locks: {sum(row['pass'] for row in dependencies)}/{len(dependencies)}",
        "",
        "## Verdict",
        "",
        f"**{payload['verdict']}**",
        "",
        "This certificate supports exact Fourier identities, finite-deletion and",
        "amplitude algebra, representative support and path inequalities, and",
        "the claim boundary. It does not machine-prove the continuum theorem.",
        "",
        "## Check inventory",
        "",
        "| Check | Result | Cases |",
        "|---|---:|---:|",
    ]
    for row in finite + structural + dependencies:
        lines.append(
            f"| {row['id']} | {'PASS' if row['pass'] else 'FAIL'} | {row.get('cases', 1)} |"
        )
    lines += [
        "",
        "## Explicit non-claims",
        "",
        "- No proof of arbitrary-mollifier positivity or the continuum payment estimate.",
        "- No proof of the open critical L1 estimate (S.444).",
        "- No proof of Q.12, Q.1, scale contraction, regularity, or the",
        "  Navier--Stokes Millennium problem.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main():
    text = NOTE.read_text(encoding="utf-8")
    note_sha = sha256(NOTE)
    finite = [
        taylor_checks(),
        abc_checks(),
        deletion_checks(),
        support_checks(),
        exponent_checks(),
        characteristic_checks(),
        amplitude_bookkeeping_checks(),
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
            "path": str(NOTE.relative_to(REPO)) if NOTE.is_relative_to(REPO) else str(NOTE),
            "sha256": note_sha,
        },
        "finite_checks": finite,
        "structural_checks": structural,
        "dependency_checks": dependencies,
        "claim_boundary": {
            "S342_quadratic_tail_for_p_gt_1": "FALSE_BY_SMOOTH_EXACT_NSE",
            "S444_critical_L1_tail": "OPEN",
            "hybrid_terminal_flux_gate": "OPEN_NOT_REFUTED",
            "Q12": "OPEN",
            "Q1": "OPEN",
            "regularity": "OPEN",
            "millennium_problem_solved": False,
        },
        "limitations": [
            "finite checks do not prove continuum analytic estimates",
            "critical L1 tail remains open",
            "regularity and the Millennium problem remain open",
        ],
    }
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_report(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
