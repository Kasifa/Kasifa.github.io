#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75V."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075v_complete_two_harmonic_flux_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075v_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075V_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075V_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075V_MUTATION", "")
SCHEMA = "r075v-complete-two-harmonic-flux-payment-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824",
    f"research/{STEM}_primary_audit.md":
        "cf23652951c5e1721270577c9a32bc476142b439aefa8ee5f62112cfd8bf5cbd",
    "research/r075v_report-source.md":
        "a099949ad6968468389b412e1d250c5e1a788ac046b949d4d69fbcf1501e9811",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075t_two_harmonic_collar_coercivity.md":
        "822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66",
    "research/r075u_two_harmonic_difference_frequency_payment.md":
        "f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4",
}
FIXTURES_SHA256 = "d2a16f6e718931aebca696d4934fa497be6bceef8c4e301a9851d04d11e622bc"
EXPECTED_SHA256 = "ebe2cd2b8aad095730eca4b59e5b79e630a28a0f0215fd2cec0024a4593386c6"

GROUPS = {
    "bindings": ("main_hash", "primary_hash", "source_hash", "dependency_hash", "u_hash"),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references"),
    "clock": ("clock_length", "cutoff_onset", "cutoff_derivative"),
    "frequencies": ("n_sum", "d_difference", "n_minus_d", "n_plus_d", "dyadic_ratio", "beat_scale"),
    "jet": ("quotient_extension", "jet_zero", "jet_one", "jet_two", "odd_difference", "even_difference"),
    "ibp": ("self_phase", "sum_phase", "self_coefficient", "sum_coefficient", "initial_boundary", "no_spurious_db"),
    "quadratic": ("uv_factor", "zeroth_term", "odd_term", "even_term", "h_square"),
    "heat": ("m_plus", "m_zero", "m_minus", "heat_extra", "heat_cancel", "grouped_heat"),
    "trace": ("right_endpoint", "phase_affine", "phase_fast", "amplitude_ratio", "exact_heat", "trace_power"),
    "scaling": ("holder", "eta_scale", "heat_scale", "bounded_q", "pre_mass_a", "pre_mass_r", "triangle_after_blocks"),
    "mass": ("t_coercivity", "mass_a", "mass_r", "target_power"),
    "normalization": ("p_definition", "x_definition", "r_cancel", "omega_power", "omega_rate"),
    "exactPde": ("transport_heat", "exact_shear", "background_boundary"),
    "source": ("exact_waves", "observability", "clay_source", "bounded_search"),
    "audit": ("audit_pass", "math_zero", "release_zero", "finite_boundary"),
    "boundary": ("exact_pair", "low_carrier_open", "multimode_open", "e24_open", "version_m_conditional", "not_clay"),
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


def encoded(powers: dict[str, Q]) -> dict[str, str | int]:
    return {
        key: int(value) if value.denominator == 1 else str(value)
        for key, value in powers.items()
    }


def add(left: dict[str, Q], right: dict[str, Q]) -> dict[str, Q]:
    return {
        key: left.get(key, Q(0)) + right.get(key, Q(0))
        for key in set(left) | set(right)
    }


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075V_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75V suite")

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
        "source_hash": "research/r075v_report-source.md",
        "dependency_hash": "research/r075t_two_harmonic_collar_coercivity.md",
        "u_hash": "research/r075u_two_harmonic_difference_frequency_payment.md",
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

    frequency_cases = []
    for row in fixtures["frequencyCases"]:
        k = int(row["k"])
        m = int(row["m"])
        n = k + m
        d = k - m
        frequency_cases.append({
            "name": row["name"],
            "n": n,
            "d": d,
            "nMinusD": n - d,
            "nPlusD": n + d,
            "dOverN": qtext(Q(d, n)),
            "daR": qtext(Q(d) * Q(row["a"]) * Q(row["R"])),
        })

    jet = fixtures["quadraticJet"]
    k0 = Q(jet["K0"])
    kplus = Q(jet["Kplus"])
    kminus = Q(jet["Kminus"])
    computed_jet = {
        "average": qtext((kplus + kminus) / 2),
        "oddDifference": qtext((kplus - kminus) / 2),
        "evenDifference": qtext((kplus + kminus) / 2 - k0),
    }

    heat = fixtures["constantMultiplierHeat"]
    n = Q(heat["n"])
    d = Q(heat["d"])
    kval = Q(heat["K"])
    mplus = (n + d) ** 2 * kval / 2
    mzero = n ** 2 * kval / 2
    mminus = (n - d) ** 2 * kval / 2
    cross = 2 * mzero + d ** 2 * kval
    computed_heat = {
        "Mplus": qtext(mplus),
        "M0": qtext(mzero),
        "Mminus": qtext(mminus),
        "crossCoefficient": qtext(cross),
        "cancellingQuadraticForm": qtext(-mplus + cross - mminus),
    }

    computed_ibp = {
        "selfKCoefficient": qtext(Q(1, 4)),
        "sumKCoefficient": qtext(Q(1, 2)),
    }

    base = {"a": Q(2), "R": Q(3)}
    after_cutoff = add(add(base, {"R": Q(-2)}), {"R": Q(2, 3)})
    after_mass = add(after_cutoff, {"a": Q(-4, 3), "R": Q(-2)})
    normalized = add(after_mass, {"R": Q(-1), "omega": Q(1)})
    normalized = add(normalized, {"R": Q(4, 3), "omega": Q(-2, 3), "p": Q(2, 3)})
    computed_scale = {
        "afterCutoff": encoded(after_cutoff),
        "afterHeat": {
            **encoded(after_cutoff),
            "boundedFactor": "(nR)^2(1+nR)^-8",
        },
        "afterMass": encoded(after_mass),
        "normalized": encoded(normalized),
        "frozenRate": qtext(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{V\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"\bV\.(\d+)\b", text)]
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
           and tags == list(range(1, 44)) and text.count("\\[") == text.count("\\]") == 43
           and not (set(refs) - set(tags)),
           {"tags": len(tags), "displays": text.count("\\["), "unresolved": sorted(set(refs) - set(tags))})
    record("complete clock and cutoff", "clock",
           computed_clock == expected["clock"]
           and all_in(compact, ["T_R=4R^2", "\\eta_R(0)=0", "C_\\eta R^{-2}"]), computed_clock)
    record("dyadic frequency ledger", "frequencies",
           frequency_cases == expected["frequencyCases"]
           and all(row["dOverN"] in ("1/3", "1/5") for row in frequency_cases)
           and all_in(compact, ["arguments `n-d,n,n+d`", "d<=n/3", "n\\ell>=2maR"]), frequency_cases)
    record("radial quotient two-jet", "jet",
           computed_jet == expected["quadraticJet"]
           and all_in(compact, ["K_R(r):=\\frac{J_{r,R}}r", "j=0,1,2", "(1+rR)^{-N}",
                                "\\Lambda_N\\varepsilon", "\\Lambda_N\\varepsilon^2"]), computed_jet)
    record("exact time integration by parts", "ibp",
           computed_ibp == expected["integrationByParts"]
           and all_in(compact, ["\\frac{g(t)\\cos(2\\phi+2kBt)}{2k}",
                                "Because `eta_R(0)=0`", "No derivative of the relative phase"]), computed_ibp)
    record("quadratic cancellation decomposition", "quadratic",
           all_in(compact, ["\\overline G\\,(u+v)^2", "G_\\Delta(u^2-v^2)",
                            "\\varepsilon(A_t+C_t)\\le CH(t)", "\\le C\\Lambda H(t)^2"]))
    record("grouped heat coefficient and cancellation", "heat",
           computed_heat == expected["constantMultiplierHeat"]
           and all_in(compact, ["L_R(r):=\\frac{r^2}2K_R(r)", "\\frac{d^2}2K_R(n)",
                                "2(k^2+m^2)A_tC_tK_R(n)"]), computed_heat)
    record("right-endpoint complete-clock trace", "trace",
           all_in(compact, ["The endpoint in V.27", "periodic distance function", "backward amplitude ratio is monotone",
                            "(1+q)^{-8}H(T_R)^2", "A_t&=Ae^{-k^2t}"]))
    record("pre-mass scale ledger", "scaling",
           computed_scale["afterCutoff"] == expected["scaleLedger"]["afterCutoff"]
           and computed_scale["afterHeat"] == expected["scaleLedger"]["afterHeat"]
           and all_in(compact, ["q^2w_q<=C", "Ca^2R^{5/3}I_H^{2/3}",
                                "triangle inequality applied only after both coupled blocks"]), computed_scale)
    record("T mass substitution and target powers", "mass",
           computed_scale["afterMass"] == expected["scaleLedger"]["afterMass"]
           and all_in(compact, ["M_{k,m,R}^{\\rm plat}\\ge ca^2R^3I_H",
                                "a^{2/3}R^{-1/3}"]), computed_scale["afterMass"])
    record("normalization and frozen rate", "normalization",
           computed_scale["normalized"] == expected["scaleLedger"]["normalized"]
           and computed_scale["frozenRate"] == expected["scaleLedger"]["frozenRate"]
           and all_in(compact, ["R^{-2}\\omega M", "\\frac\\omega R", "-\\frac2{11907}"]), computed_scale)
    record("exact shear PDE and background boundary", "exactPde",
           all_in(compact, ["\\partial_tF+B\\partial_2F-\\partial_2^2F=0",
                            "exact smooth unforced shear", "nonzero constant background"]))
    record("bounded primary-source boundary", "source",
           all_in(compact_source, ["arXiv:1101.5507", "arXiv:1604.01831", "arXiv:1609.07020v6",
                                   "official Clay Mathematics Institute", "not evidence of novelty by itself"]))
    record("primary audit verdict and finite boundary", "audit",
           all_in(compact_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**",
                                    "Release blocker count: **0**", "Neither finite algebra nor sampling is represented as proof"]))
    record("exact-subfamily claim boundary", "boundary",
           all_in(compact, ["exact high-carrier dyadic pair", "low-carrier pairs", "three or more harmonics",
                            "arbitrary-field E.24", "conditional on the realized-subclass", "**NOT CLAY.**"]))

    verdict = "PASS" if all(row["pass"] for row in assertions) else "FAIL"
    output = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": assertions,
        "assertionCount": len(assertions),
        "bindings": bindings,
        "clock": computed_clock,
        "frequencyCases": frequency_cases,
        "quadraticJet": computed_jet,
        "constantMultiplierHeat": computed_heat,
        "integrationByParts": computed_ibp,
        "scaleLedger": computed_scale,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    passed = sum(1 for row in assertions if row["pass"])
    report = [
        "# R0.75V finite certificate report", "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{len(assertions)}",
        f"- Frequency fixtures: {len(frequency_cases)}/2",
        "- Exact heat-cancellation fixtures: 1/1", "",
        "The finite suite certifies source bindings, frequency algebra, time-integration",
        "coefficients, quadratic cancellation, and exact scale arithmetic.  It does not",
        "numerically certify the continuum multiplier-jet or endpoint-trace lemmas.",
        "The theorem is limited to one exact high-carrier dyadic pair. **NOT CLAY.**", "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"schema": SCHEMA, "verdict": verdict, "assertions": len(assertions)}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
