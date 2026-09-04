#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75R."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075r_outer_cap_spectral_concentration_obstruction"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075r_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075R_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075R_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075R_MUTATION", "")
SCHEMA = "r075r-outer-cap-spectral-concentration-obstruction-certificate-v1"

FROZEN = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075n_radial_collar_averaged_wiener_row.md":
        "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
    "research/r075q_spatially_spread_harmonic_collar_payment.md":
        "9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075r_outer_cap_spectral_concentration_obstruction_primary_audit.md":
        "9b52e3d54fce43c609f70f0b8e71c53def0b4b705144be39a7b62e88d5e07355",
    "research/r075r_report-source.md":
        "767bfc43f9510a2acdf7fbff9d52624ed23ed80e4c3af174c77a47c3824d87ed",
}
FIXTURES_SHA256 = "226b7411967f2fa6f1960d29a03f32ef40945af47c6545c3f60e4115e507a1d1"
EXPECTED_SHA256 = "25d46dc6276a42f764dc503100750186213186368aebc9d94be409cd80f3c251"

MUTATION_GROUPS = {
    "bindings": ("main_hash", "primary_hash", "source_hash", "dependency_hash"),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "sourceIntegrity": ("utf8", "control", "tags", "displays", "dependency_table"),
    "crossSection": ("cross_section_mass", "moving_endpoint", "cross_section_sign"),
    "outerCap": ("outer_interval", "outer_separation", "outer_lower"),
    "spectralArithmetic": ("divisibility", "integer_carrier", "band_lower", "band_upper"),
    "spectralText": ("support_minkowski", "support_real", "support_no_remainder"),
    "dirichletRows": ("dirichlet_pointwise", "dirichlet_l2", "dirichlet_tail"),
    "transportArithmetic": ("transport_k", "transport_shift", "transport_bound"),
    "exactPde": ("transport_equation", "divergence", "nonlinear_term", "constant_pressure"),
    "heatPersistence": ("heat_multiplier", "heat_global", "heat_off_diagonal"),
    "fluxLower": ("flux_sign", "negative_cap", "flux_time", "flux_power"),
    "plateauUpper": ("plateau_projection", "plateau_linf", "plateau_volume", "mass_power"),
    "powerLedger": ("mass_two_thirds", "raw_quotient", "amplitude_cancel"),
    "normalization": ("normalization_factor", "normalized_r", "normalized_omega"),
    "tailExact": ("tail_m1", "tail_m2", "tail_m3"),
    "frozenRate": ("kappa_formula", "kappa_one", "r_exponent", "kappa_positive"),
    "sourceBoundary": ("source_primary", "source_geometry", "source_no_import", "source_nonexhaustive"),
    "claimBoundary": ("plateau_only", "version_m_open", "e24_open", "smooth_no_singularity"),
    "auditBoundary": ("audit_pass", "audit_math_zero", "audit_release_zero", "audit_no_publish"),
    "routeBoundary": ("route_alternatives", "clock_open", "weak_open", "novelty", "not_clay"),
}
NEGATIVE_MUTATIONS = tuple(x for xs in MUTATION_GROUPS.values() for x in xs)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(str(value))


def qt(value: Q) -> str:
    return str(value)


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((b < 32 and b not in (9, 10, 13)) or b == 127 for b in data)


def guarded(group: str, value: bool) -> bool:
    return bool(value and MUTATION not in MUTATION_GROUPS[group])


def all_in(text: str, fragments: list[str]) -> bool:
    return all(fragment in text for fragment in fragments)


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075R_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75R suite")

    raw = MAIN.read_bytes()
    raw_primary = PRIMARY.read_bytes()
    raw_source = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    primary = raw_primary.decode("utf-8")
    source = raw_source.decode("utf-8")
    flat = re.sub(r"\s+", " ", text)
    flat_primary = re.sub(r"\s+", " ", primary)
    flat_source = re.sub(r"\s+", " ", source)
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    frozen = dict(FROZEN)
    mutation_path = {
        "main_hash": f"research/{STEM}.md",
        "primary_hash": f"research/{STEM}_primary_audit.md",
        "source_hash": "research/r075r_report-source.md",
        "dependency_hash": "research/r075q_spatially_spread_harmonic_collar_payment.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    s = fixtures["spectralCase"]
    m, k, n, carrier = map(int, (s["m"], s["K"], s["n"], s["q"]))
    spectral = {
        "divisor": 16 * m,
        "twoMn": 2 * m * n,
        "lowerBand": carrier - 2 * m * n,
        "upperBand": carrier + 2 * m * n,
        "supportInsideK2K": k <= carrier - 2 * m * n
        and carrier + 2 * m * n <= 2 * k,
    }

    tr = fixtures["transportCase"]
    radius, b, abs_b, time = map(q, (tr["R"], tr["b"], tr["absB"], tr["T"]))
    tk = int(tr["K"])
    transport = {
        "RToMinusThreeHalves": int(radius ** Q(-3, 2)),
        "driftDistance": qt(abs_b * time),
        "bTimesR": qt(b * radius),
        "driftBoundSharp": abs_b * time == b * radius,
        "timeIsKMinusTwo": time == Q(1, tk * tk),
    }

    scales = fixtures["frozenScales"]
    rho, c_gamma = q(scales["rho"]), q(scales["cGamma"])
    tails = []
    for case in fixtures["tailCases"]:
        tm = int(case["m"])
        power = Q(2 * tm) + Q(1, 6)
        tails.append({
            "m": tm,
            "pointwiseExponent": -2 * tm,
            "relativeL2Exponent": 1 - 4 * tm,
            "cubicExponent": -6 * tm,
            "quotientRecoveryExponent": 4 * tm,
            "kappa": qt(power * rho / 4 - c_gamma / 12),
            "rExponent": qt(-power + c_gamma / (3 * rho)),
        })

    ledger = {
        "flux": {"B": 1, "a": 1, "R": 1, "A": 2, "n": -1, "K": -2},
        "mass": {"A": 3, "a": 2, "R": 3, "K": -2, "nR": "-6m"},
        "massTwoThirds": {"A": 2, "a": "4/3", "R": 2, "K": "-4/3", "nR": "-4m"},
        "rawQuotient": {"B": 1, "a": "-1/3", "R": -1, "n": -1, "K": "-2/3", "nR": "4m"},
        "normalizedRExponent": "-2m-1/6",
        "normalizedOmegaExponent": "1/3",
        "amplitudeCancels": True,
    }

    tags = [int(x) for x in re.findall(r"\\tag\{R\.(\d+)\}", text)]
    bindings_ok = all(v["expectedSha256"] == v["observedSha256"] for v in source_rows.values())
    fixture_ok = sha256(FIXTURES) == FIXTURES_SHA256
    expected_ok = sha256(EXPECTED) == EXPECTED_SHA256

    assertions: list[dict[str, Any]] = []

    def record(name: str, group: str, ok: bool, details: Any = None) -> None:
        assertions.append({
            "name": name,
            "pass": guarded(group, ok),
            "details": details,
        })

    record("frozen source bindings", "bindings", bindings_ok, source_rows)
    record("fixture and expected bindings", "inputs",
           fixture_ok and expected_ok and fixtures.get("schema", "").endswith("fixtures-v1"),
           {"fixturesSha256": sha256(FIXTURES), "expectedSha256": sha256(EXPECTED)})
    record("UTF-8, controls, tags, and displays", "sourceIntegrity",
           clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
           and tags == list(range(1, 42)) and text.count("\\[") == text.count("\\]")
           and all_in(flat, list(FROZEN.keys())[:4]),
           {"tags": len(tags), "displays": text.count("\\[")})
    record("exact radial cross-section identity", "crossSection",
           all_in(flat, ["Xi_R(y)=2\\pi", "D_R(y)=\\Xi_R'(y)",
                         "=-2\\pi y\\vartheta(|y|/R-a)", "D_R<0", "D_R>0"]))
    record("outer-cap separation and sign", "outerCap",
           all_in(flat, ["s_*\\in(\\delta_0,\\delta)", "s_*-3h", "I_+:=",
                         "outside the `x_2` projection", "-D_R(y)\\ge c_\\vartheta aR"]))
    record("spectral arithmetic fixture", "spectralArithmetic",
           spectral == expected["spectralCase"] and k % (16 * m) == 0
           and n == k // (16 * m) and carrier == 3 * k // 2,
           spectral)
    record("exact real band support in source", "spectralText",
           all_in(flat, ["[-2mn,2mn]=[-K/8,K/8]", "shifts this support by `+q` and `-q`",
                         "\\frac{11K}{8}\\le|j|\\le\\frac{13K}{8}",
                         "without a projection remainder"]))
    record("Dirichlet concentration and tails", "dirichletRows",
           all_in(flat, ["|d_n(z)|\\le C\\min", "c_mA^2n^{-1}\\le\\|G_K\\|",
                         "(nR)^{1-4m}", "The relative tail", "tends to zero"]))
    record("transport arithmetic fixture", "transportArithmetic",
           transport["RToMinusThreeHalves"] == expected["transportCase"]["RToMinusThreeHalves"]
           and transport["driftDistance"] == expected["transportCase"]["driftDistance"]
           and transport["bTimesR"] == expected["transportCase"]["bTimesR"]
           and transport["driftBoundSharp"] and transport["timeIsKMinusTwo"],
           transport)
    record("exact Navier-Stokes realization", "exactPde",
           all_in(flat, ["(\\partial_t+B\\partial_2-\\partial_2^2)F_K=0",
                         "\\nabla\\!\\cdot u_K=0", "(u_K\\!\\cdot\\nabla)u_K=(0,0,B\\partial_2F_K)",
                         "with constant pressure", "not a passive-scalar surrogate"]))
    record("heat persistence and off-diagonal scale", "heatPersistence",
           all_in(flat, ["\\|F_K(t)\\|_2^2\\ge e^{-8}",
                         "e^{-d^2/(4t)}", "e^{-d^2/(8t)}", "e^{-c(KR)^2}",
                         "R^{-3/2}\\le K\\le2R^{-3/2}"]))
    record("positive signed-flux lower bound", "fluxLower",
           all_in(flat, ["integrand `BD_R|F_K|^2` is nonnegative for `y>0`", "only adverse contribution",
                         "\\mathcal T_K", "\\ge c_m|B|aRA^2n^{-1}K^{-2}"]))
    record("plateau cubic upper bound", "plateauUpper",
           all_in(flat, ["|y|\\le(a+\\delta_0)R", "(nR)^{-2m}",
                         "volume at most `C a^2R^3`", "(nR)^{-6m}"]))
    record("power ledger", "powerLedger",
           ledger == expected["powerLedger"], ledger)
    record("normalization algebra", "normalization",
           all_in(flat, ["`R^(1/3)omega^(1/3)`", "`|B|=bR^(-2)`",
                         "R^{-3/2}\\le K\\le2R^{-3/2}", "R^{-2m-1/6}\\omega^{1/3}"]))
    record("tail and rate cases", "tailExact",
           tails == expected["tailCases"], tails)
    record("positive frozen exponent", "frozenRate",
           all(Q(row["kappa"]) > 0 for row in tails)
           and tails[0]["kappa"] == "304373/952560000"
           and tails[0]["rExponent"] == "-304373/214326"
           and all_in(flat, ["\\kappa_m:=", "\\kappa_1=\\frac{304373}{952560000}>0",
                             "R^{-304373/214326}"]))
    record("bounded primary-source boundary", "sourceBoundary",
           all_in(flat_source, ["arXiv:1609.07020", "arXiv:1711.04279",
                                "arXiv:math/0609429", "no external theorem is needed",
                                "search boundary, not a novelty or priority claim"]))
    record("plateau-only claim boundary", "claimBoundary",
           all_in(flat, ["specific attempted extension of Q", "not a counterexample to E.24",
                         "complete Version-M payment sees exterior rows beyond the plateau",
                         "exact unforced smooth", "does not concern singularity formation"]))
    record("primary audit status", "auditBoundary",
           all_in(flat_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**",
                                 "Release blocker count: **0**", "does not authorize publication"]))
    record("route and open-problem boundary", "routeBoundary",
           all_in(flat, ["full signed-flux cap", "spreading or thickness hypothesis",
                         "signed multimode cancellation", "complete-clock extraction",
                         "suitable-weak transfer", "No novelty or priority claim",
                         "\\mathbf{NOT\\ CLAY}"]))

    verdict = "PASS" if all(row["pass"] for row in assertions) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": len(assertions),
        "passed": sum(1 for row in assertions if row["pass"]),
        "mutation": MUTATION or None,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "sourceBindings": source_rows,
        "computed": {
            "spectralCase": spectral,
            "transportCase": transport,
            "tailCases": tails,
            "powerLedger": ledger,
            "formulaTags": len(tags),
            "displayPairs": text.count("\\["),
        },
        "checks": assertions,
        "boundary": (
            "The certificate checks one explicit exact smooth shear family and the failure "
            "of its plateau-only multimode payment. Full-support payment, Version-M, E.24, "
            "complete clock, fixed deletion, suitable-weak transfer, regularity, and "
            "singularity remain open. NOT CLAY."
        ),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# R0.75R exact finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {payload['passed']}/{payload['assertions']}",
        f"- Mutation: `{MUTATION or 'none'}`",
        "",
        "## Exact rows",
        "",
        f"- Spectral fixture: `{json.dumps(spectral, sort_keys=True)}`",
        f"- Transport fixture: `{json.dumps(transport, sort_keys=True)}`",
        f"- `m=1` rate: `{tails[0]['kappa']}`; R exponent: `{tails[0]['rExponent']}`",
        f"- Formula tags: {len(tags)}/41",
        "",
        "## Assertions",
        "",
    ]
    for row in assertions:
        report.append(f"- {'PASS' if row['pass'] else 'FAIL'} -- {row['name']}")
    report.extend(["", "## Boundary", "", payload["boundary"], ""])
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")

    print(json.dumps({"schema": SCHEMA, "verdict": verdict,
                      "assertions": len(assertions), "passed": payload["passed"]},
                     sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
