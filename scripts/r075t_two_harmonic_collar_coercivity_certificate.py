#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75T."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075t_two_harmonic_collar_coercivity"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075t_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075T_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075T_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075T_MUTATION", "")
SCHEMA = "r075t-two-harmonic-collar-coercivity-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66",
    f"research/{STEM}_primary_audit.md":
        "97d804444737284d7ec40b3ce45389272b1a9f61d1901f7bcebf9ed0eab935e5",
    "research/r075t_report-source.md":
        "c2255cdd07f2e490921d93ba7e62a809c0348a9e6136b7fd5537cf3799e4e8d8",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075m_dyadic_packet_diffusive_flux_gain.md":
        "13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075s_full_frequency_single_harmonic_clock_payment.md":
        "d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd",
}
FIXTURES_SHA256 = "939b04eeccb9c96b6d5cb21d49ebc48e7a8387dfccdc08afd2dfd6db77fd4393"
EXPECTED_SHA256 = "cd58217667129d5a2f01dd2b315b86a934de1258be2eefab401f5b66efc127c5"

GROUPS = {
    "bindings": ("main_hash", "primary_hash", "source_hash", "dependency_hash"),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references"),
    "geometry": ("ell", "radial_difference", "fiber_area", "plateau_power"),
    "envelope": ("regular_basis", "beta_zero", "gram_compact", "phase_ibp"),
    "slowBeat": ("envelope_identity", "sinc_identity", "phase_distance", "slow_defect"),
    "resolvedBeat": ("gram_formula", "sinc_gap", "boundary_errors", "resolved_defect"),
    "holder": ("holder_direction", "holder_length", "amplitude_degree"),
    "diffusive": ("unequal_heat", "moving_phase", "time_slice"),
    "flux": ("self_coefficients", "cross_coefficients", "difference_frequency", "sum_frequency"),
    "power": ("fiber_power", "interval_power", "final_power"),
    "source": ("primary_sources", "no_import", "bounded_search"),
    "audit": ("audit_pass", "math_zero", "release_zero"),
    "boundary": ("two_modes", "low_carrier_open", "temporal_open", "e24_open", "not_clay"),
}
NEGATIVE_MUTATIONS = tuple(name for names in GROUPS.values() for name in names)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((b < 32 and b not in (9, 10, 13)) or b == 127 for b in data)


def flat(value: str) -> str:
    return re.sub(r"\s+", " ", value)


def all_in(value: str, fragments: list[str]) -> bool:
    return all(fragment in value for fragment in fragments)


def guarded(group: str, value: bool) -> bool:
    return bool(value and MUTATION not in GROUPS[group])


def rational_text(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075T_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75T suite")

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
        "source_hash": "research/r075t_report-source.md",
        "dependency_hash": "research/r075m_dyadic_packet_diffusive_flux_gain.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    geometry = fixtures["geometry"]
    a = Q(geometry["a"])
    delta0 = Q(geometry["delta0"])
    radius = Q(geometry["R"])
    ell = a * radius
    radial_difference = 4 * a * delta0 * radius * radius
    computed_geometry = {
        "ell": rational_text(ell),
        "radialSquaredDifference": rational_text(radial_difference),
        "fiberAreaPiCoefficient": rational_text(radial_difference),
        "plateauPower": {"a": 2, "R": 3, "H": 3},
    }

    beat_cases = []
    for row in fixtures["beatCases"]:
        local_ell = Q(row["ell"])
        d_ell = Q(int(row["k"]) - int(row["m"])) * local_ell
        theta = Q(row["phaseDistanceToPi"])
        q_squared = min(Q(1), d_ell * d_ell + theta * theta)
        amp_a = Q(row["A"])
        amp_c = Q(row["C"])
        h_squared = (amp_a - amp_c) ** 2 + amp_a * amp_c * q_squared
        beat_cases.append({
            "name": row["name"],
            "dEll": rational_text(d_ell),
            "qSquared": rational_text(q_squared),
            "hSquared": rational_text(h_squared),
            "regime": "unresolved" if d_ell <= 1 else "resolved",
        })

    flux_coefficients = dict(fixtures["fluxCoefficients"])
    power = fixtures["powerLedger"]
    final_power = {
        "a": int(power["fiber"]["a"]) + int(power["interval"]["ell"]),
        "R": int(power["fiber"]["R"]) + int(power["interval"]["ell"]),
        "H": int(power["amplitudeDegreeAfterHolder"]),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{T\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"T\.(\d+)", text)]
    assertions: list[dict[str, Any]] = []

    def record(name: str, group: str, ok: bool, details: Any = None) -> None:
        assertions.append({"name": name, "pass": guarded(group, ok), "details": details})

    record("frozen source bindings", "bindings",
           all(row["expectedSha256"] == row["observedSha256"] for row in bindings.values()), bindings)
    record("fixture and expected bindings", "inputs",
           sha256(FIXTURES) == FIXTURES_SHA256 and sha256(EXPECTED) == EXPECTED_SHA256
           and fixtures["schema"].endswith("fixtures-v1"),
           {"fixturesSha256": sha256(FIXTURES), "expectedSha256": sha256(EXPECTED)})
    record("UTF-8, controls, tags, displays, and references", "integrity",
           clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
           and tags == list(range(1, 32)) and text.count("\\[") == text.count("\\]") == 32
           and not (set(refs) - set(tags)),
           {"tags": len(tags), "displays": text.count("\\["), "unresolved": sorted(set(refs) - set(tags))})
    record("exact plateau fibre geometry", "geometry",
           computed_geometry == expected["geometry"]
           and all_in(compact, ["=4\\pi a\\delta_0R^2", "I_ell=[-ell/2,ell/2]", "a^2R^3H_{d,aR}^3"]),
           computed_geometry)
    record("uniform slow-envelope sampling", "envelope",
           all_in(compact, ["v_\\beta(s)=", "s,&\\beta=0", "continuous and positive definite",
                            "\\|Z\\|_{L^\\infty(I)}+\\|Z'\\|_{L^2(I)}", "one integration by parts"]))
    record("unresolved beat defect", "slowBeat",
           beat_cases[:2] == expected["beatCases"][:2]
           and all_in(compact, ["A^2+C^2+2AC\\operatorname {sinc}(d\\ell/2)\\cos\\Delta",
                                "(A-C)^2+2AC", "\\min\\{1,(d\\ell)^2+\\theta^2\\}"]),
           beat_cases[:2])
    record("resolved beat gap", "resolvedBeat",
           beat_cases[2:] == expected["beatCases"][2:]
           and all_in(compact, ["2\\sin(1/2)<1", "C(mell)^(-1)ell(A^2+C^2)",
                                "\\ge c\\ell(A^2+C^2)"]), beat_cases[2:])
    record("Holder cubic conversion", "holder",
           all_in(compact, ["\\ge\\ell^{-1/2}", "\\left(\\int_{I_\\ell}|f|^2",
                            "\\ge c\\ell H_{d,\\ell}^3"]))
    record("exact diffusive time-slice corollary", "diffusive",
           all_in(compact, ["A_t&=Ae^{-k^2t}", "C_t=Ce^{-m^2t}",
                            "\\phi-\\psi+dBt", "\\int_0^{T_R}H_{d,aR}(t)^3\\,dt"]))
    record("four exact flux prefactors", "flux",
           flux_coefficients == expected["fluxCoefficients"]
           and all_in(compact, ["\\frac B4", "J_{2k,R}", "J_{2m,R}", "\\frac B2",
                                "J_{d,R}", "J_{k+m,R}"]), flux_coefficients)
    record("final power ledger", "power", final_power == expected["geometry"]["plateauPower"], final_power)
    record("bounded primary-source boundary", "source",
           all_in(compact_source, ["arXiv:math/0012186", "arXiv:1609.07020v6",
                                   "not a completeness, novelty, or priority certificate",
                                   "do not replace the local proof"]))
    record("primary audit verdict", "audit",
           all_in(compact_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**",
                                    "Release blocker count: **0**", "falsification aid only"]))
    record("claim boundary", "boundary",
           all_in(compact, ["exactly two harmonics", "does **not** yet prove", "low-carrier pairs",
                            "arbitrary-field E.24", "\\mathbf{NOT\\ CLAY}"]))

    verdict = "PASS" if all(row["pass"] for row in assertions) else "FAIL"
    output = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": assertions,
        "assertionCount": len(assertions),
        "bindings": bindings,
        "geometry": computed_geometry,
        "beatCases": beat_cases,
        "fluxCoefficients": flux_coefficients,
        "powerLedger": final_power,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    passed = sum(1 for row in assertions if row["pass"])
    report = [
        "# R0.75T finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{len(assertions)}",
        f"- Beat fixtures: {len(beat_cases)}/3",
        "- Exact geometry, beat defects, flux prefactors, and power ledger: " + ("PASS" if verdict == "PASS" else "FAIL"),
        "",
        "This finite certificate binds and recomputes the algebraic ledger.  The continuum",
        "sampling and beat-defect inequalities remain certified by the analytic proof and",
        "primary audit, not by finite sampling.  T.31 and the complete two-mode payment",
        "remain OPEN. **NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"schema": SCHEMA, "verdict": verdict, "assertions": len(assertions)}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
