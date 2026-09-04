#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.76D."""

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
STEM = "r076d_quantitative_growing_mode_entropy_window"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076d_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076D_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076D_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076D_MUTATION", "")
SCHEMA = "r076d-quantitative-growing-mode-entropy-window-certificate-v1"

FROZEN = {
    f"research/{STEM}.md": "cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e",
    f"research/{STEM}_primary_audit.md": "9b99247ceb34cadc12c7f4f0858be642316ca80d1ff83d05dfd745a9906356d8",
    "research/r076d_report-source.md": "f2358780d382dcace69b7ebef855bf3c8e63d15b581dc86b62b7e3c751fbd310",
    "research/r076c_full_frequency_fixed_mode_flux_payment.md": "2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md": "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075b_bulk_clock_outer_padding_gate.md": "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
}
FIXTURES_SHA256 = "ffe5c2b9a1a6b0c20b710dc45fcac9543069ea6af38dce34804665012984b374"
EXPECTED_SHA256 = "eb5dd9ebaa6a74cbc7f999fdbd55ee54a50588342c3dfba9412ac53c935ba2dd"


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


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def encoded(powers: dict[str, Q]) -> dict[str, str | int]:
    return {key: int(value) if value.denominator == 1 else qstr(value)
            for key, value in powers.items()}


def all_in(value: str, fragments: list[str]) -> bool:
    return all(fragment in value for fragment in fragments)


GROUPS = {
    "bindings": ["main_hash", "primary_hash", "source_hash", "c_hash", "r_hash", "clock_hash"],
    "inputs": ["fixture_hash", "expected_hash", "fixture_schema", "expected_schema"],
    "integrity": ["utf8", "controls", "no_cr", "no_trailing", "tags", "display_opens", "display_closes", "references", "tex_qquad", "tex_frac"],
    "geometry": ["delta_order", "support_radius", "support_bound", "plateau_length", "plateau_bound"],
    "scaled": ["positive_q", "integer_modes", "ordered_modes", "dyadic_band", "ell", "kappas", "alpha", "n1r", "lambda", "clock_t", "clock_mass", "velocity", "real_band"],
    "space": ["term_count", "turan_power", "chebyshev", "length_ratio", "map_scale", "original_frequency", "rescaled_frequency", "bernstein_rational", "bernstein_e", "returned_rational", "returned_e", "interval_containment", "gap_free"],
    "heat": ["heat_terms", "m", "factorial_argument", "factorial", "factorial_over_four", "center_shift", "shifted_lower", "shifted_upper", "net_decay", "heat_endpoint_power", "endpoint_comparison", "tail_formula", "endpoint_formula", "family_hypothesis", "imaginary_free"],
    "energy": ["gradient_lambda", "q_squared", "gradient_coefficient", "gradient_inequality", "onset", "weighted_power", "energy_endpoint_power", "bounded_branch", "high_branch", "endpoint_cancel", "q_absorption", "speed_zero"],
    "scale": ["flux_prefactor", "mass_prefactor", "target", "normalized", "r_cancel", "frozen_rate", "entropy_window", "limsup_rate"],
    "proof": ["main_bound", "normalized_bound", "spatial_lemma", "heat_lemma", "bounded_trace", "heat_clock", "energy_identity", "physical_row", "exact_pde", "complete_square", "no_sign_route", "no_projection"],
    "source": ["nazarov", "friedland_yomdin", "erdelyi", "theorem_number", "complex_coefficients", "source_space", "source_heat", "source_flux", "source_rate", "local_deductions", "no_novelty", "finite_not_proof", "primary_pass", "math_zero", "release_zero"],
    "boundary": ["exact_shear", "one_band", "growing_constant", "r075r_compatible", "arbitrary_packets_open", "version_m_conditional", "regularity_open", "singularity_open", "no_figure", "not_clay"],
}
NEGATIVE_MUTATIONS = tuple(name for values in GROUPS.values() for name in values)


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076D_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76D suite")

    raws = [MAIN.read_bytes(), PRIMARY.read_bytes(), SOURCE.read_bytes()]
    text, primary, source = [raw.decode("utf-8") for raw in raws]
    compact, compact_primary, compact_source = map(flat, (text, primary, source))
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    bindings = {path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
                for path, digest in sorted(FROZEN.items())}

    profile = fixtures["profile"]
    delta0, delta = Q(profile["delta0"]), Q(profile["delta"])
    case = fixtures["scaledCase"]
    q_count, a_value, radius, b_shear = int(case["q"]), Q(case["a"]), Q(case["R"]), Q(case["B"])
    modes = [Q(value) for value in case["frequencies"]]
    ell = a_value * radius
    kappas = [mode * ell for mode in modes]
    alpha = kappas[0]
    n1r = modes[0] * radius
    lambda_value = (alpha / a_value) ** 2
    clock_end = Q(fixtures["clock"]["scaledClockEnd"])
    temporal_end = clock_end * lambda_value
    velocity = b_shear * radius / a_value
    real_magnitudes = [(kappa / alpha) ** 2 for kappa in kappas]
    geometry = {
        "supportRadius": qstr(1 + delta / a_value),
        "supportWithinThreeHalves": 1 + delta / a_value <= Q(3, 2),
        "centralPlateauLength": qstr(2 - 2 * delta / a_value),
        "centralPlateauAtLeastOne": 2 - 2 * delta / a_value >= 1,
    }
    scaled = {
        "ell": qstr(ell), "kappas": [qstr(x) for x in kappas], "alpha": qstr(alpha),
        "n1R": qstr(n1r), "lambda": qstr(lambda_value), "T": qstr(temporal_end),
        "KOverH": qstr(lambda_value), "dyadicBand": modes[-1] <= 2 * modes[0],
        "v": qstr(velocity),
        "realPartsWithinMinusFourMinusOne": min(real_magnitudes) >= 1 and max(real_magnitudes) <= 4,
    }

    maximum_terms = 2 * q_count
    local_scale = Q(fixtures["spatialObservation"]["localMapScale"])
    maximum_original_frequency = 2 * alpha
    maximum_rescaled_frequency = local_scale * maximum_original_frequency
    space = {
        "maximumTerms": maximum_terms,
        "turanExponent": maximum_terms - 1,
        "lengthRatio": qstr(Q(fixtures["spatialObservation"]["jPlusLength"]) /
                            Q(fixtures["spatialObservation"]["chebyshevMeasureLower"])),
        "maximumOriginalFrequency": qstr(maximum_original_frequency),
        "maximumRescaledFrequency": qstr(maximum_rescaled_frequency),
        "bernsteinConstantRationalPart": qstr(alpha),
        "bernsteinConstantEMultiplier": qstr(2 * (maximum_terms + 1)),
        "returnedDerivativeRationalPart": qstr(2 * alpha),
        "returnedDerivativeEMultiplier": qstr(4 * (maximum_terms + 1)),
    }

    n_terms = int(fixtures["heatTail"]["maximumTerms"])
    m_value = 2 * (n_terms - 1)
    factorial_arg = m_value + 1
    shift = Q(fixtures["heatTail"]["centerShift"])
    shifted_lower, shifted_upper = -Q(4) + shift, -Q(1) + shift
    endpoint_r = Q(m_value) + Q(2, 3)
    heat = {
        "maximumTerms": n_terms, "m": m_value, "factorialArgument": factorial_arg,
        "factorial": math.factorial(factorial_arg),
        "factorialOverFour": math.factorial(factorial_arg) // 4,
        "endpointPower": qstr(endpoint_r),
        "endpointComparisonPower": m_value,
        "shiftedRealLower": qstr(shifted_lower), "shiftedRealUpper": qstr(shifted_upper),
        "netDecay": qstr(-shift + max(abs(shifted_lower), abs(shifted_upper))),
    }

    ledger = fixtures["lambdaLedger"]
    weighted_power = (Q(ledger["gradientPrefactor"]["lambda"])
                      + Q(ledger["changeOfClock"]["sPerTau"]["lambda"])
                      + Q(ledger["changeOfClock"]["dsPerDtau"]["lambda"])
                      + Q(ledger["weightedTail"]["K"]) * Q(ledger["clockMass"]["KPerH"]["lambda"]))
    endpoint_lambda_power = (Q(ledger["endpointTail"]["T"])
                             + Q(ledger["endpointTail"]["K"]) * Q(ledger["clockMass"]["KPerH"]["lambda"]))
    q_squared = Q(q_count * q_count, int(a_value * a_value))
    energy = {
        "lambda": qstr(lambda_value), "qSquaredOverASquared": qstr(q_squared),
        "gradientCoefficient": qstr(lambda_value + q_squared),
        "weightedLambdaPower": qstr(weighted_power),
        "endpointLambdaPower": qstr(endpoint_lambda_power),
    }

    scale = {
        "fluxPrefactor": encoded({"a": Q(2), "R": Q(3), "v": Q(1)}),
        "massPrefactor": encoded({"a": Q(2), "R": Q(5), "H": Q(1)}),
        "afterMass": encoded({"a": Q(2, 3), "R": Q(-1, 3), "M": Q(2, 3)}),
        "normalized": encoded({"a": Q(2, 3), "R": Q(0), "omega": Q(1, 3), "p": Q(2, 3)}),
        "frozenRate": qstr(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(x) for x in re.findall(r"\\tag\{D\.(\d+)\}", text)]
    refs = [int(x) for x in re.findall(r"(?<![A-Za-z0-9_.])D\.(\d+)", text)]
    checks: dict[str, dict[str, bool]] = {
        "bindings": {
            "main_hash": bindings[f"research/{STEM}.md"]["expectedSha256"] == bindings[f"research/{STEM}.md"]["observedSha256"],
            "primary_hash": bindings[f"research/{STEM}_primary_audit.md"]["expectedSha256"] == bindings[f"research/{STEM}_primary_audit.md"]["observedSha256"],
            "source_hash": bindings["research/r076d_report-source.md"]["expectedSha256"] == bindings["research/r076d_report-source.md"]["observedSha256"],
            "c_hash": bindings["research/r076c_full_frequency_fixed_mode_flux_payment.md"]["expectedSha256"] == bindings["research/r076c_full_frequency_fixed_mode_flux_payment.md"]["observedSha256"],
            "r_hash": bindings["research/r075r_outer_cap_spectral_concentration_obstruction.md"]["expectedSha256"] == bindings["research/r075r_outer_cap_spectral_concentration_obstruction.md"]["observedSha256"],
            "clock_hash": bindings["research/r075b_bulk_clock_outer_padding_gate.md"]["expectedSha256"] == bindings["research/r075b_bulk_clock_outer_padding_gate.md"]["observedSha256"],
        },
        "inputs": {
            "fixture_hash": sha256(FIXTURES) == FIXTURES_SHA256,
            "expected_hash": sha256(EXPECTED) == EXPECTED_SHA256,
            "fixture_schema": fixtures["schema"] == "r076d-quantitative-growing-mode-entropy-window-fixtures-v1",
            "expected_schema": expected["schema"] == "r076d-quantitative-growing-mode-entropy-window-expected-v1",
        },
        "integrity": {
            "utf8": all(clean_bytes(raw) for raw in raws), "controls": clean_bytes(raws[0]),
            "no_cr": b"\r" not in raws[0],
            "no_trailing": all(not line.endswith((" ", "\t")) for line in text.splitlines()),
            "tags": tags == list(range(1, 42)),
            "display_opens": len(re.findall(r"(?m)^\\\[$", text)) == 41,
            "display_closes": len(re.findall(r"(?m)^\\\]$", text)) == 41,
            "references": not (set(refs) - set(tags)),
            "tex_qquad": re.search(r"(?<!\\)\bqquad\b", text) is None,
            "tex_frac": re.search(r"(?<!\\)\bfrac\{", text) is None,
        },
        "geometry": {
            "delta_order": 0 < delta0 < delta,
            "support_radius": geometry["supportRadius"] == expected["geometry"]["supportRadius"],
            "support_bound": geometry["supportWithinThreeHalves"] == expected["geometry"]["supportWithinThreeHalves"],
            "plateau_length": geometry["centralPlateauLength"] == expected["geometry"]["centralPlateauLength"],
            "plateau_bound": geometry["centralPlateauAtLeastOne"] == expected["geometry"]["centralPlateauAtLeastOne"],
        },
        "scaled": {
            "positive_q": q_count >= 1, "integer_modes": all(x.denominator == 1 and x >= 1 for x in modes),
            "ordered_modes": modes == sorted(set(modes)), "dyadic_band": scaled["dyadicBand"] == expected["scaledCase"]["dyadicBand"],
            "ell": scaled["ell"] == expected["scaledCase"]["ell"], "kappas": scaled["kappas"] == expected["scaledCase"]["kappas"],
            "alpha": scaled["alpha"] == expected["scaledCase"]["alpha"], "n1r": scaled["n1R"] == expected["scaledCase"]["n1R"],
            "lambda": scaled["lambda"] == expected["scaledCase"]["lambda"] and lambda_value == n1r ** 2,
            "clock_t": scaled["T"] == expected["scaledCase"]["T"], "clock_mass": scaled["KOverH"] == expected["scaledCase"]["KOverH"],
            "velocity": scaled["v"] == expected["scaledCase"]["v"],
            "real_band": scaled["realPartsWithinMinusFourMinusOne"] == expected["scaledCase"]["realPartsWithinMinusFourMinusOne"],
        },
        "space": {
            "term_count": space["maximumTerms"] == expected["spatialObservation"]["maximumTerms"],
            "turan_power": space["turanExponent"] == expected["spatialObservation"]["turanExponent"],
            "chebyshev": Q(fixtures["spatialObservation"]["chebyshevMeasureLower"]) == Q(1, 2),
            "length_ratio": space["lengthRatio"] == expected["spatialObservation"]["lengthRatio"],
            "map_scale": local_scale == Q(1, 2),
            "original_frequency": space["maximumOriginalFrequency"] == expected["spatialObservation"]["maximumOriginalFrequency"],
            "rescaled_frequency": space["maximumRescaledFrequency"] == expected["spatialObservation"]["maximumRescaledFrequency"],
            "bernstein_rational": space["bernsteinConstantRationalPart"] == expected["spatialObservation"]["bernsteinConstantRationalPart"],
            "bernstein_e": space["bernsteinConstantEMultiplier"] == expected["spatialObservation"]["bernsteinConstantEMultiplier"],
            "returned_rational": space["returnedDerivativeRationalPart"] == expected["spatialObservation"]["returnedDerivativeRationalPart"],
            "returned_e": space["returnedDerivativeEMultiplier"] == expected["spatialObservation"]["returnedDerivativeEMultiplier"],
            "interval_containment": all_in(compact, ["For `z_0 in J`", "observation interval is contained in `J^+`"]),
            "gap_free": all_in(compact, ["There is no dependence on the size or separation", "Imaginary parts and exponent gaps never enter"]),
        },
        "heat": {
            "heat_terms": heat["maximumTerms"] == expected["heatTail"]["maximumTerms"], "m": heat["m"] == expected["heatTail"]["m"],
            "factorial_argument": heat["factorialArgument"] == expected["heatTail"]["factorialArgument"],
            "factorial": heat["factorial"] == expected["heatTail"]["factorial"],
            "factorial_over_four": heat["factorialOverFour"] == expected["heatTail"]["factorialOverFour"],
            "center_shift": shift == Q(5, 2), "shifted_lower": heat["shiftedRealLower"] == expected["heatTail"]["shiftedRealLower"],
            "shifted_upper": heat["shiftedRealUpper"] == expected["heatTail"]["shiftedRealUpper"], "net_decay": heat["netDecay"] == expected["heatTail"]["netDecay"],
            "heat_endpoint_power": heat["endpointPower"] == expected["heatTail"]["endpointPower"],
            "endpoint_comparison": Q(fixtures["heatTail"]["endpointComparison"]) == Q(5, 4) and heat["endpointComparisonPower"] == expected["heatTail"]["endpointComparisonPower"],
            "tail_formula": all_in(compact, ["m=2(N-1)", "\\frac{(m+1)!}{4}"]),
            "endpoint_formula": all_in(compact, ["\\left(\\frac54\\right)^m", "T^{2/3}(1+T)^me^{-2T}"]),
            "family_hypothesis": compact.count("every `Q(.;z)` satisfying D.20") == 1,
            "imaginary_free": compact.count("Imaginary parts and exponent gaps never enter") == 1,
        },
        "energy": {
            "gradient_lambda": energy["lambda"] == expected["energy"]["lambda"],
            "q_squared": energy["qSquaredOverASquared"] == expected["energy"]["qSquaredOverASquared"],
            "gradient_coefficient": energy["gradientCoefficient"] == expected["energy"]["gradientCoefficient"],
            "gradient_inequality": compact_primary.count("a^(-2)(alpha+q)^2 <= C(lambda+q^2/a^2)") == 1,
            "onset": compact.count("0\\le\\zeta(s)\\le C_\\eta s") == 1,
            "weighted_power": energy["weightedLambdaPower"] == expected["energy"]["weightedLambdaPower"],
            "energy_endpoint_power": energy["endpointLambdaPower"] == expected["energy"]["endpointLambdaPower"],
            "bounded_branch": compact.count("When `lambda<=1`") == 1,
            "high_branch": compact.count("When `lambda>1`") == 1,
            "endpoint_cancel": all_in(compact_primary, ["T^(-2/3)K_T^(2/3)", "cancel exactly"]),
            "q_absorption": compact.count("polynomial factor is absorbed") == 1,
            "speed_zero": compact_primary.count("`B=0` is covered") == 1,
        },
        "scale": {
            "flux_prefactor": scale["fluxPrefactor"] == expected["scaleLedger"]["fluxPrefactor"],
            "mass_prefactor": scale["massPrefactor"] == expected["scaleLedger"]["massPrefactor"],
            "target": scale["afterMass"] == expected["scaleLedger"]["afterMass"],
            "normalized": scale["normalized"] == expected["scaleLedger"]["normalized"],
            "r_cancel": scale["normalized"]["R"] == 0,
            "frozen_rate": scale["frozenRate"] == expected["scaleLedger"]["frozenRate"],
            "entropy_window": compact.count("q(L)\\log(q(L)+1)=o(L^2)") >= 1,
            "limsup_rate": compact.count("-\\frac2{11907}") >= 2,
        },
        "proof": {
            "main_bound": all_in(compact, ["|\\mathcal T_{\\boldsymbol n,R}|", "\\exp\\!\\bigl(C_*q\\log(q+1)\\bigr)", "a^{2/3}R^{-1/3}"]),
            "normalized_bound": all_in(compact, ["\\mathfrak X_{\\boldsymbol n,R}", "a^{2/3}\\omega^{1/3}"]),
            "spatial_lemma": all_in(compact, ["**Lemma D.1.**", "(\\alpha+q)^{-1}\\|g'\\|_{L^\\infty(J)}"]),
            "heat_lemma": all_in(compact, ["**Lemma D.2.**", "\\int_0^T\\tau k(\\tau)^{2/3}d\\tau"]),
            "bounded_trace": all_in(compact, ["h(4)\\le D^{6q}H", "h(4)^{2/3}\\le D^{4q}H^{2/3}"]),
            "heat_clock": all_in(compact, ["\\tau=\\lambda s", "K_T=lambda H"]),
            "energy_identity": all_in(compact, ["exact real-square identity", "2a^{-2}\\int_0^4\\zeta\\int\\Xi_a|G_z|^2"]),
            "physical_row": all_in(compact, ["\\frac{a^2R^3}{2}v", "4\\pi\\delta_0a^2R^5H"]),
            "exact_pde": compact.count("\\partial_tF+B\\partial_2F-\\partial_2^2F=0") == 1,
            "complete_square": compact.count("complete real square before absolute values") == 1,
            "no_sign_route": all_in(compact, ["No analytic-density split", "localized-current sign", "standalone carrier integration by parts"]),
            "no_projection": compact.count("cannot be applied merely to a Fourier projection") == 1,
        },
        "source": {
            "nazarov": "https://www.mathnet.ru/eng/aa397" in source,
            "friedland_yomdin": "https://arxiv.org/abs/1107.0039" in source,
            "erdelyi": "https://people.tamu.edu/~terdelyi/papers-online/sbornik150R.pdf" in source,
            "theorem_number": compact_source.count("Theorem 2.7.1") >= 1,
            "complex_coefficients": "a_j in C" in source,
            "source_space": "D.17, D.21, and D.27" in source,
            "source_heat": "D.21--D.26" in source,
            "source_flux": "D.32--D.39 together with D.5" in source,
            "source_rate": "D.40 and frozen value" in source,
            "local_deductions": compact_source.count("Everything after those two inputs") == 1,
            "no_novelty": all_in(compact_source, ["not evidence of novelty or priority", "no completeness, novelty, priority, or sharpness claim"]),
            "finite_not_proof": compact_source.count("Finite arithmetic may audit") == 1,
            "primary_pass": "Current verdict: **PASS**" in primary,
            "math_zero": "Mathematical blocker count: **0**" in primary,
            "release_zero": "Release blocker count: **0**" in primary,
        },
        "boundary": {
            "exact_shear": compact.count("exact constant-shear family") >= 1,
            "one_band": compact.count("one dyadic band") >= 1,
            "growing_constant": compact.count("constant grows with `q`") == 1,
            "r075r_compatible": compact.count("R0.75R already rules out") == 1,
            "arbitrary_packets_open": compact.count("arbitrary packets") >= 1,
            "version_m_conditional": compact.count("Version-M") >= 2,
            "regularity_open": compact.count("regularity") >= 1,
            "singularity_open": compact.count("singularity") >= 1,
            "no_figure": compact.count("No formal scientific figure or simulation is claimed") == 1,
            "not_clay": "**NOT CLAY.**" in text and "**NOT CLAY.**" in source and "**NOT CLAY.**" in primary,
        },
    }

    for group, names in GROUPS.items():
        if list(checks[group]) != names:
            raise SystemExit(f"check inventory mismatch in {group}")
    if MUTATION:
        for group in checks.values():
            if MUTATION in group:
                group[MUTATION] = False
                break

    assertions = sum(len(group) for group in checks.values())
    passed = sum(sum(bool(value) for value in group.values()) for group in checks.values())
    verdict = "PASS" if passed == assertions else "FAIL"
    exact = {"geometry": geometry, "scaledCase": scaled, "spatialObservation": space,
             "heatTail": heat, "energy": energy, "scaleLedger": scale}
    payload: dict[str, Any] = {
        "schema": SCHEMA, "suite": "R0.76D quantitative growing-mode entropy window",
        "verdict": verdict, "assertionsPassed": passed, "assertionsTotal": assertions,
        "mutation": MUTATION or None, "negativeMutations": list(NEGATIVE_MUTATIONS),
        "bindings": bindings, "exact": exact, "checks": checks,
        "continuumBoundary": "Finite exact checks do not prove Turan--Nazarov, Erdelyi, or the analytic flux estimate.",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# R0.76D exact certificate report", "", f"- Verdict: **{verdict}**.",
        f"- Assertions: {passed}/{assertions}.", f"- Named negative mutations: {len(NEGATIVE_MUTATIONS)}.",
        "- Exact sections: geometry, scaled case, spatial observation, heat tail, energy, and scale ledger.",
        "- Continuum boundary: finite arithmetic is not proof of either imported inequality or of the analytic theorem.",
        "", "The exact fixture has q=3, N=6, m=10, 11!/4=9,979,200, lambda=4,",
        "gradient coefficient 257/64, onset exponent -1/3, endpoint exponent 0,",
        "and frozen normalized rate -2/11907. **NOT CLAY.**", "",
    ]
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"suite": "r076d", "status": verdict, "assertions": assertions}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
