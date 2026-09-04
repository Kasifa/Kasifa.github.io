#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75U."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075u_two_harmonic_difference_frequency_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075u_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075U_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075U_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075U_MUTATION", "")
SCHEMA = "r075u-two-harmonic-difference-frequency-payment-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4",
    f"research/{STEM}_primary_audit.md":
        "3687decf19ff49016e101a174d066b355689dcca7a4dc36a941b84994b118d6a",
    "research/r075u_report-source.md":
        "d0e9356a162b683a33c5b4c49692a62962d2a9c63cccba9eb9d84040aaf4a01f",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075s_full_frequency_single_harmonic_clock_payment.md":
        "d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd",
    "research/r075t_two_harmonic_collar_coercivity.md":
        "822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66",
}
FIXTURES_SHA256 = "c654b79a1b3b69078df01000c43fee54fdff39ea64c7bc47e206b114dc20b0c6"
EXPECTED_SHA256 = "381e80ca54eee51fb3aab823837f0bfdc28e84353e02c8f41fceed261d6aec12"

GROUPS = {
    "bindings": ("main_hash", "primary_hash", "source_hash", "dependency_hash"),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references"),
    "clock": ("clock_length", "cutoff_onset", "cutoff_derivative"),
    "radial": ("radial_low", "radial_high", "quotient", "no_extra_d"),
    "moment": ("tau", "phase_travel", "node_crossing", "cubic_moment"),
    "slowLow": ("low_heat", "slow_phase", "sine_distance", "q_sigma"),
    "slowHigh": ("high_heat", "zeta_onset", "laplace_first", "laplace_second"),
    "fast": ("fast_phase", "w_zero", "bv_ibp", "tau_compare"),
    "scaling": ("time_change", "amplitude_cancel", "d_power", "r_power"),
    "mass": ("t_coercivity", "a_power", "target_power"),
    "normalization": ("p_definition", "x_definition", "r_cancel", "omega_rate"),
    "exactPde": ("transport_heat", "exact_shear", "background_boundary"),
    "source": ("primary_sources", "no_import", "bounded_search"),
    "audit": ("audit_pass", "math_zero", "release_zero", "alias_boundary"),
    "boundary": ("difference_only", "self_sum_open", "low_carrier_open", "e24_open", "not_clay"),
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


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def add(left: dict[str, Q], right: dict[str, Q]) -> dict[str, Q]:
    return {key: left.get(key, Q(0)) + right.get(key, Q(0)) for key in set(left) | set(right)}


def encoded(powers: dict[str, Q]) -> dict[str, str | int]:
    return {key: int(value) if value.denominator == 1 else str(value) for key, value in powers.items()}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075U_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75U suite")

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
        "source_hash": "research/r075u_report-source.md",
        "dependency_hash": "research/r075t_two_harmonic_collar_coercivity.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    clock = fixtures["clock"]
    radius = Q(clock["R"])
    duration = Q(clock["durationCoefficient"]) * radius ** int(clock["durationRPower"])
    computed_clock = {"T": qtext(duration)}

    phase_cases = []
    for row in fixtures["phaseCases"]:
        lam = Q(row["Lambda"])
        sigma = Q(row["sigmaAbs"])
        initial = Q(row["initialDistance"])
        tau = Q(1) if lam <= 1 else 1 / lam
        travel = sigma * tau
        qq = min(Q(1), initial + travel)
        phase_cases.append({
            "name": row["name"],
            "tau": qtext(tau),
            "phaseTravel": qtext(travel),
            "q": qtext(qq),
            "regime": "slow" if travel <= 1 else "fast",
        })

    radial_cases = []
    for row in fixtures["radialCases"]:
        epsilon = Q(row["n"]) * Q(row["a"]) * Q(row["R"])
        radial_cases.append({
            "name": row["name"],
            "naR": qtext(epsilon),
            "branch": "low" if epsilon <= 1 else "high",
        })

    time_row = {"d": Q(-1), "R": Q(-4, 3)}
    after_radial = add(time_row, {"d": Q(1), "a": Q(2), "R": Q(3)})
    after_radial.pop("d")
    after_mass = add(after_radial, {"a": Q(-4, 3), "R": Q(-2)})
    normalized = add(after_mass, {"R": Q(-1), "omega": Q(1)})
    normalized = add(normalized, {"R": Q(4, 3), "omega": Q(-2, 3), "p": Q(2, 3)})
    scale_ledger = {
        "afterRadial": encoded(after_radial),
        "afterMass": encoded(after_mass),
        "normalized": encoded(normalized),
        "frozenRate": qtext(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{U\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"U\.(\d+)", text)]
    assertions: list[dict[str, Any]] = []

    def record(name: str, group: str, ok: bool, details: Any = None) -> None:
        assertions.append({"name": name, "pass": guarded(group, ok), "details": details})

    record("frozen source bindings", "bindings",
           all(row["expectedSha256"] == row["observedSha256"] for row in bindings.values()), bindings)
    record("fixture and expected bindings", "inputs",
           sha256(FIXTURES) == FIXTURES_SHA256 and sha256(EXPECTED) == EXPECTED_SHA256
           and fixtures["schema"].endswith("fixtures-v1"))
    record("UTF-8, controls, tags, displays, and references", "integrity",
           clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
           and tags == list(range(1, 29)) and text.count("\\[") == text.count("\\]") == 28
           and not (set(refs) - set(tags)),
           {"tags": len(tags), "displays": text.count("\\["), "unresolved": sorted(set(refs) - set(tags))})
    record("complete clock and cutoff onset", "clock",
           computed_clock == expected["clock"]
           and all_in(compact, ["T_R=4R^2", "\\eta_R(0)=0", "C_\\eta R^{-2}"]), computed_clock)
    record("uniform radial quotient", "radial",
           radial_cases == expected["radialCases"]
           and all_in(compact, ["\\min\\{naR,1\\}", "\\frac{|J_{n,R}|}{n}\\le Ca^2R^3",
                                "otherwise `n^(-1)<=aR`"]), radial_cases)
    record("phase-distance moment", "moment",
           phase_cases == expected["phaseCases"]
           and all_in(compact, ["periodic triangular wave", "\\int_0^\\tau h(s)^3",
                                "\\ge c\\tau q^3", "cubic mean is `r^3/4`"]), phase_cases)
    record("slow low-heat branch", "slowLow",
           all_in(compact, ["Assume `|sigma|tau<=1`", "If `Lambda<=1`", "|\\sin(\\alpha+\\sigma s)|\\le Cq",
                            "`q>=c|sigma|`"]))
    record("slow high-heat Laplace branch", "slowHigh",
           all_in(compact, ["If `Lambda>=1`", "zeta(s)<=C_eta s", "\\int_0^\\infty se^{-\\Lambda s}",
                            "C|\\sigma|\\tau^2q", "\\le C\\tau^{2/3}q^2"]))
    record("fast bounded-variation branch", "fast",
           all_in(compact, ["Assume `|sigma|tau>=1`", "Since `w(0)=0`", "one integration by parts",
                            "\\le C\\tau", "at most `C tau^(2/3)`"]))
    record("exact scaling and amplitude cancellation", "scaling",
           all_in(compact, ["\\Lambda=(k^2+m^2)R^2", "\\sigma=dBR^2", "If `AC=0`",
                            "\\frac C{dR^{4/3}}", "The amplitude product cancels exactly"]))
    record("defect mass and target powers", "mass",
           scale_ledger["afterRadial"] == expected["scaleLedger"]["afterRadial"]
           and scale_ledger["afterMass"] == expected["scaleLedger"]["afterMass"]
           and all_in(compact, ["Ca^2R^{5/3}", "ca^2R^3", "Ca^{2/3}R^{-1/3}"]), scale_ledger)
    record("normalization and frozen rate", "normalization",
           scale_ledger["normalized"] == expected["scaleLedger"]["normalized"]
           and scale_ledger["frozenRate"] == expected["scaleLedger"]["frozenRate"]
           and all_in(compact, ["R^{-2}\\omega M", "\\frac\\omega R", "-\\frac2{11907}"]))
    record("exact shear PDE and background boundary", "exactPde",
           all_in(compact, ["\\partial_tF+B\\partial_2F-\\partial_2^2F=0",
                            "exact smooth unforced shear", "nonzero constant background",
                            "mean-zero, inversion-paired Version-M subclass"]))
    record("bounded primary-source boundary", "source",
           all_in(compact_source, ["arXiv:1604.01831", "arXiv:1609.07020v6", "arXiv:1711.04279",
                                   "not an exhaustive novelty or priority search",
                                   "no external theorem has been silently substituted"]))
    record("primary audit verdict and alias boundary", "audit",
           all_in(compact_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**",
                                    "Release blocker count: **0**", "fixed-grid scan can alias"]))
    record("claim boundary", "boundary",
           all_in(compact, ["difference-frequency target T.31", "not a complete two-harmonic flux theorem",
                            "self frequencies `2k,2m`", "low carriers with", "arbitrary-field E.24",
                            "\\mathbf{NOT\\ CLAY}"]))

    verdict = "PASS" if all(row["pass"] for row in assertions) else "FAIL"
    output = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": assertions,
        "assertionCount": len(assertions),
        "bindings": bindings,
        "clock": computed_clock,
        "phaseCases": phase_cases,
        "radialCases": radial_cases,
        "scaleLedger": scale_ledger,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    passed = sum(1 for row in assertions if row["pass"])
    report = [
        "# R0.75U finite certificate report", "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{len(assertions)}",
        f"- Phase fixtures: {len(phase_cases)}/4",
        f"- Radial fixtures: {len(radial_cases)}/2", "",
        "The finite suite certifies bindings and exact scale arithmetic.  It does not",
        "numerically certify the continuum moving-phase lemma.  The self/sum block and",
        "complete two-mode payment remain OPEN. **NOT CLAY.**", "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"schema": SCHEMA, "verdict": verdict, "assertions": len(assertions)}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
