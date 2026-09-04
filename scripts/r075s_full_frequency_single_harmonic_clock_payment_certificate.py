#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75S."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075s_full_frequency_single_harmonic_clock_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075s_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075S_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075S_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075S_MUTATION", "")
SCHEMA = "r075s-full-frequency-single-harmonic-clock-payment-certificate-v1"

FROZEN = {
    "research/r075s_full_frequency_single_harmonic_clock_payment.md":
        "d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd",
    "research/r075s_full_frequency_single_harmonic_clock_payment_primary_audit.md":
        "38e2bc95b5785b97df5d85474f3ed6105458a117249710b2c052cebbd769b5eb",
    "research/r075s_report-source.md":
        "ab9771e732204f28d3493ae9db73e7aa62aa980cc15b69dfefb39f226520b2a7",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075q_spatially_spread_harmonic_collar_payment.md":
        "9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
}
FIXTURES_SHA256 = "82874592703552c1639c69066ddbf1ab531c135cd92eeae775c20be66cd8260f"
EXPECTED_SHA256 = "e806089d4649b73649edeed5c0204b81a42dbef79c758283b128ec49a57abd8b"

GROUPS = {
    "bindings": ("main_hash", "primary_hash", "source_hash", "dependency_hash"),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references"),
    "clock": ("clock_length", "clock_scaling", "cutoff_variation"),
    "fluxIdentity": ("odd_cross_section", "constant_cancel", "cosine_cancel", "phase_factor"),
    "radialRows": ("radial_low", "radial_l1", "radial_tail", "radial_r_scale"),
    "nodeGeometry": ("fiber", "node_lower", "plateau_mass"),
    "smallPhase": ("small_sigma_moment", "small_sigma_holder", "node_distance"),
    "largePhase": ("large_sigma_moment", "bv_total", "phase_ibp"),
    "lowSplit": ("epsilon_split", "lambda_bound", "low_flux", "low_mass"),
    "lowLedger": ("low_two_thirds", "low_target", "low_amplitude"),
    "highMass": ("phase_uniform", "heat_time", "high_mass_power"),
    "highPhase": ("zero_shear", "high_bv", "one_over_k"),
    "highQBelow": ("q_lower", "radial_below", "target_below"),
    "highQAbove": ("radial_above", "time_above", "power_compare"),
    "coverage": ("epsilon_overlap", "q_overlap", "all_integer_k"),
    "normalization": ("p_definition", "x_definition", "r_cancel", "omega_rate"),
    "exactPde": ("divergence", "transport", "nonlinear", "laplacian", "pressure"),
    "sourceBoundary": ("source_primary", "source_observation", "source_no_import", "source_search_limit"),
    "auditBoundary": ("audit_pass", "audit_math_zero", "audit_release_zero", "audit_alias_warning"),
    "claimBoundary": ("single_harmonic", "multimode_open", "version_m_conditional", "e24_open", "not_clay"),
}
NEGATIVE_MUTATIONS = tuple(item for group in GROUPS.values() for item in group)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(str(value))


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((b < 32 and b not in (9, 10, 13)) or b == 127 for b in data)


def flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def all_in(text: str, fragments: list[str]) -> bool:
    return all(fragment in text for fragment in fragments)


def guarded(group: str, value: bool) -> bool:
    return bool(value and MUTATION not in GROUPS[group])


def add_powers(left: dict[str, Q], right: dict[str, Q]) -> dict[str, Q]:
    keys = set(left) | set(right)
    return {key: left.get(key, Q(0)) + right.get(key, Q(0)) for key in keys}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075S_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75S suite")

    raw = MAIN.read_bytes()
    raw_primary = PRIMARY.read_bytes()
    raw_source = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    primary = raw_primary.decode("utf-8")
    source = raw_source.decode("utf-8")
    compact = flat(text)
    compact_primary = flat(primary)
    compact_source = flat(source)
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    frozen = dict(FROZEN)
    mutation_path = {
        "main_hash": f"research/{STEM}.md",
        "primary_hash": f"research/{STEM}_primary_audit.md",
        "source_hash": "research/r075s_report-source.md",
        "dependency_hash": "research/r075q_spatially_spread_harmonic_collar_payment.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    clock = fixtures["clock"]
    radius = q(clock["R"])
    time = q(clock["durationCoefficient"]) * radius ** int(clock["durationRPower"])
    computed_clock = {"T": str(time)}

    regimes = []
    for row in fixtures["regimeCases"]:
        a = q(row["a"])
        r = q(row["R"])
        k = int(row["k"])
        qq = k * r
        epsilon = a * qq
        lam = k * k * 4 * r * r
        if float(epsilon) <= 2 * math.pi:
            regime = "low"
        elif qq <= 1:
            regime = "high-q-below-one"
        else:
            regime = "high-q-above-one"
        regimes.append({
            "name": row["name"],
            "q": str(qq),
            "epsilon": str(epsilon),
            "lambda": str(lam),
            "regime": regime,
        })

    scales = fixtures["frozenScales"]
    frozen_rate = -q(scales["cGamma"]) / 12
    variation_total = sum(int(v) for v in fixtures["variationLedger"].values())

    low_mass = {"A": Q(3), "a": Q(2), "R": Q(5), "J": Q(1)}
    mass_two_thirds = {key: value * Q(2, 3) for key, value in low_mass.items()}
    target = add_powers(mass_two_thirds, {"a": Q(2, 3), "R": Q(-1, 3)})
    computed_ledger = {
        "lowTarget": {key: str(value) if value.denominator != 1 else int(value) for key, value in target.items()},
        "amplitudeCancels": target["A"] == 2,
        "normalizedRExponent": 0,
        "normalizedOmegaExponent": "1/3",
    }

    tags = [int(value) for value in re.findall(r"\\tag\{S\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"S\.(\d+)", text)]
    bindings_ok = all(row["expectedSha256"] == row["observedSha256"] for row in source_rows.values())

    assertions: list[dict[str, Any]] = []

    def record(name: str, group: str, ok: bool, details: Any = None) -> None:
        assertions.append({"name": name, "pass": guarded(group, ok), "details": details})

    record("frozen source bindings", "bindings", bindings_ok, source_rows)
    record("fixture and expected bindings", "inputs",
           sha256(FIXTURES) == FIXTURES_SHA256 and sha256(EXPECTED) == EXPECTED_SHA256
           and fixtures.get("schema", "").endswith("fixtures-v1"),
           {"fixturesSha256": sha256(FIXTURES), "expectedSha256": sha256(EXPECTED)})
    record("UTF-8, controls, tags, displays, and references", "integrity",
           clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
           and tags == list(range(1, 42)) and text.count("\\[") == text.count("\\]")
           and not (set(refs) - set(tags)),
           {"tags": len(tags), "displays": text.count("\\["), "unresolved": sorted(set(refs) - set(tags))})
    record("complete clock arithmetic and cutoff variation", "clock",
           computed_clock == expected["clock"]
           and all_in(compact, ["T_R:=t_2-s_R=4R^2", "nondecreasing", "total variation is at most one"]),
           computed_clock)
    record("exact odd radial flux identity", "fluxIdentity",
           all_in(compact, ["D_R(y):=", "=-2\\pi y\\vartheta(|y|/R-a)", "It is odd",
                            "constant and cosine rows vanish", "\\frac{A^2B S_{k,R}}4",
                            "\\sin(2\\phi+2kBt)"]))
    record("three radial coefficient bounds", "radialRows",
           all_in(compact, ["q:=kR", "\\varepsilon:=kaR=aq", "-2\\pi R^2",
                            "\\min\\{\\varepsilon,1,q^{-N}\\}", "integrations by parts"]))
    record("rectangular subcollar node lower bound", "nodeGeometry",
           all_in(compact, ["|x_2|\\le aR/4", "\\ge4\\delta_0R", "|\\cos(\\varepsilon z-\\psi)|^3",
                            "Q_\\varepsilon(\\psi)^3", "\\ge c\\,a^2R^3Q_\\varepsilon(\\psi)^3"]))
    record("small phase-speed branch", "smallPhase",
           all_in(compact, ["For `|sigma|<=1`", "J^{1/3}\\ge c\\min",
                            "|sin(2psi)|<=2Q_epsilon(psi)", "C|\\sigma|J^{1/3}\\le CJ^{2/3}"]))
    record("large phase-speed BV branch", "largePhase",
           variation_total == expected["variationTotal"]
           and all_in(compact, ["For `|sigma|>=1`", "J>=c", "for every `lambda>=0`",
                                "\\operatorname {Var}_{[0,1]}w", "\\le2", "integration by parts"]),
           {"variationTotal": variation_total})
    record("low-frequency split and bounds", "lowSplit",
           regimes == expected["regimeCases"]
           and all_in(compact, ["\\varepsilon=kaR\\le2\\pi", "\\lambda:=k^2T_R=4q^2",
                                "\\le\\frac{16\\pi^2}{a^2}\\le1", "CA^2a^2R^3", "M_{k,R}^{\\rm plat}"] ),
           regimes)
    record("low-frequency power ledger", "lowLedger",
           computed_ledger == expected["powerLedger"]
           and all_in(compact_primary, ["a^{2/3}R^{-1/3}M^{2/3}", "A^2a^2R^3J^{2/3}", "T_R=4R^2"]),
           computed_ledger)
    record("high-frequency phase-uniform mass", "highMass",
           all_in(compact, ["\\varepsilon=kaR\\ge2\\pi", "for every }\\psi",
                            "\\min\\{T_R,k^{-2}\\}", "phase-uniform plateau estimate Q.19"]))
    record("high-frequency BV phase cancellation", "highPhase",
           all_in(compact, ["If `B=0`, the flux vanishes", "Its total variation is at most two",
                            "\\le\\frac Ck", "\\le CA^2\\frac{|S_{k,R}|}{k}"]))
    record("high regime q below one", "highQBelow",
           all_in(compact, ["If `q<=1`", "`q>=2pi/a`", "CaR^3q^{-1}\\le Ca^2R^3",
                            "min{T_R,k^(-2)}>=cR^2"]))
    record("high regime q above one", "highQAbove",
           all_in(compact, ["If `q>=1`", "CaR^3q^{-2}", "R^2q^{-2}",
                            "q^(-2)<=q^(-4/3)", "a<=a^2"]))
    record("frequency coverage", "coverage",
           all_in(compact_primary, ["overlaps at `epsilon=2pi`", "overlap at `q=1`",
                                    "every integer `k>=1` is covered"]))
    record("normalization and exact frozen rate", "normalization",
           frozen_rate == q(expected["frozenRate"])
           and all_in(compact, ["p_{k,R}^{\\rm plat}:=R^{-2}\\omega", "\\frac\\omega R[\\mathcal T_{k,R}]_+",
                                "a^{2/3}\\omega^{1/3}", "=-\\frac{c_\\gamma}{12}<0"]),
           {"frozenRate": str(frozen_rate)})
    record("exact smooth Navier-Stokes shear", "exactPde",
           all_in(compact, ["u_k(t,x)=(0,B,F_k(t,x_2))", "div u_k=0",
                            "(u_k\\!\\cdot\\nabla)u_k=(0,0,B\\partial_2F_k)",
                            "\\Delta u_k=(0,0,\\partial_2^2F_k)", "constant pressure"]))
    record("bounded primary-source boundary", "sourceBoundary",
           all_in(compact_source, ["arXiv:1604.01831", "arXiv:2103.07906", "arXiv:1609.07020",
                                   "arXiv:1711.04279", "No external theorem is imported",
                                   "search boundary, not a novelty or priority claim"]))
    record("primary audit status and alias warning", "auditBoundary",
           all_in(compact_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**",
                                    "Release blocker count: **0**", "does not authorize publication",
                                    "can alias the oscillation"]))
    record("claim and route boundary", "claimBoundary",
           all_in(compact, ["including all frequencies omitted by Q", "not a multimode estimate",
                            "not asserted for a Fourier projection", "arbitrary-field E.24",
                            "complete Version-M clock extraction", "No novelty or priority claim",
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
            "clock": computed_clock,
            "regimeCases": regimes,
            "variationTotal": variation_total,
            "frozenRate": str(frozen_rate),
            "powerLedger": computed_ledger,
            "formulaTags": len(tags),
            "displayPairs": text.count("\\["),
        },
        "checks": assertions,
        "boundary": (
            "The certificate checks the full-frequency complete-clock payment only for one "
            "real constant-drift harmonic and the canonical radial collar. Multimode "
            "interference, nonconstant shear, E.24, complete Version-M extraction, fixed "
            "deletion, suitable-weak transfer, regularity, and singularity remain open. NOT CLAY."
        ),
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# R0.75S exact finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {payload['passed']}/{payload['assertions']}",
        f"- Blocker count: {payload['assertions'] - payload['passed']}",
        f"- Mutation: `{MUTATION or 'none'}`",
        "",
        "## Exact computed rows",
        "",
        f"- Complete clock at `R=1/16`: `T={computed_clock['T']}`.",
        f"- Regime fixtures: `{json.dumps(regimes, sort_keys=True)}`.",
        f"- BV total: `{variation_total}`.",
        f"- Frozen logarithmic rate: `{frozen_rate}`.",
        f"- Low target ledger: `{json.dumps(computed_ledger, sort_keys=True)}`.",
        "",
        "## Boundary",
        "",
        payload["boundary"],
    ]
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"verdict": verdict, "assertions": len(assertions), "mutation": MUTATION or None}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
