#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.76E."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076e_linear_modal_entropy_window"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076e_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076E_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076E_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076E_MUTATION", "")
SCHEMA = "r076e-linear-modal-entropy-window-certificate-v1"

FROZEN = {
    f"research/{STEM}.md": "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
    f"research/{STEM}_primary_audit.md": "5ce8fb3f2f2f487002b0e391db49855edb3cff72574058e26150813d69615d27",
    "research/r076e_report-source.md": "10e506fa9d250b14d9f42f6eac7c2c83cfca934a85a2da6e223cd473f21e0c12",
    "research/r076d_quantitative_growing_mode_entropy_window.md": "cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md": "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075b_bulk_clock_outer_padding_gate.md": "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
}
FIXTURES_SHA256 = "9b5b0a7d88fe31d4156a7fbc8f73b52a9b5a8271437ee1be867970cec244cf47"
EXPECTED_SHA256 = "af6c1fd49d57945306f5f97a99f160a8fcbaec21bce887b78fe74e0bbe4d4f80"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((byte < 32 and byte not in (9, 10, 13)) or byte == 127 for byte in data)


def flat(value: str) -> str:
    return re.sub(r"\s+", " ", value)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def encoded(powers: dict[str, Q]) -> dict[str, str | int]:
    return {
        key: int(value) if value.denominator == 1 else qstr(value)
        for key, value in powers.items()
    }


def fragments(value: str, parts: list[str]) -> bool:
    return all(part in value for part in parts)


GROUPS = {
    "bindings": ["main_hash", "primary_hash", "source_hash", "d_hash", "r_hash", "clock_hash"],
    "inputs": ["fixture_hash", "expected_hash", "fixture_schema", "expected_schema"],
    "integrity": ["utf8", "controls", "no_cr", "no_trailing", "tags", "display_opens", "display_closes", "unnumbered", "references", "tex_qquad", "tex_quad", "tex_frac", "tex_linebreak"],
    "geometry": ["delta_order", "support_radius", "support_bound", "plateau_length", "plateau_bound"],
    "scaled": ["positive_q", "integer_modes", "ordered_modes", "dyadic_band", "ell", "kappas", "alpha", "n1r", "lambda", "clock_t", "clock_mass", "velocity", "real_band"],
    "space": ["term_count", "turan_power", "chebyshev", "length_ratio", "spatial_formula", "gap_free"],
    "split": ["terms", "m", "m_plus_one", "d0_power", "two_power", "start", "start_conditions", "start_power", "decay_power", "binary_exponent", "binary_negative", "early_power", "late_threshold", "late_monotone", "endpoint_power", "endpoint_threshold"],
    "endpoint": ["unit_length", "unit_chebyshev", "unit_ratio", "finite_insertion", "finite_absorption", "large_monotone", "stronger_power", "endpoint_formula", "full_mass", "no_factorial"],
    "energy": ["gradient_lambda", "q_squared", "gradient_coefficient", "weighted_power", "endpoint_lambda_power", "heat_clock_mass", "cutoff_definition", "cutoff_rows", "energy_identity", "gradient_inequality", "q_absorption", "speed_zero"],
    "scale": ["flux_prefactor", "mass_prefactor", "target", "normalized", "r_cancel", "frozen_rate", "new_window", "witness_new", "witness_old"],
    "proof": ["main_bound", "normalized_bound", "stable_family", "split_choice", "early_bound", "late_bound", "weighted_bound", "endpoint_bound", "bounded_branch", "heat_branch", "onset_bound", "physical_row", "exact_pde", "complete_square", "no_projection"],
    "source": ["nazarov", "friedland_yomdin", "erdelyi", "theorem_number", "complex_scope", "adjacent_real", "adjacent_shift", "local_split", "source_table", "no_new_theorem", "no_novelty", "finite_not_proof", "primary_pass", "blocker_zero"],
    "boundary": ["exact_shear", "one_band", "growing_constant", "r075r_compatible", "arbitrary_packets_open", "version_m_conditional", "regularity_open", "singularity_open", "no_figure", "no_simulation", "not_clay", "sole_publisher"],
}
NEGATIVE_MUTATIONS = tuple(name for names in GROUPS.values() for name in names)


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076E_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76E suite")

    raws = [MAIN.read_bytes(), PRIMARY.read_bytes(), SOURCE.read_bytes()]
    main_text, primary_text, source_text = [raw.decode("utf-8") for raw in raws]
    compact, compact_primary, compact_source = map(flat, (main_text, primary_text, source_text))
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(FROZEN.items())
    }

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
        "ell": qstr(ell),
        "kappas": [qstr(value) for value in kappas],
        "alpha": qstr(alpha),
        "n1R": qstr(n1r),
        "lambda": qstr(lambda_value),
        "T": qstr(temporal_end),
        "KOverH": qstr(lambda_value),
        "dyadicBand": modes[-1] <= 2 * modes[0],
        "v": qstr(velocity),
        "realPartsWithinMinusFourMinusOne": min(real_magnitudes) >= 1 and max(real_magnitudes) <= 4,
    }

    max_terms = 2 * q_count
    space = {
        "maximumTerms": max_terms,
        "turanExponent": max_terms - 1,
        "lengthRatio": qstr(Q(fixtures["spatialObservation"]["jPlusLength"]) / Q(fixtures["spatialObservation"]["chebyshevMeasureLower"])),
    }

    delayed = fixtures["delayedSplit"]
    n_terms = int(delayed["maximumTerms"])
    m_value = 2 * (n_terms - 1)
    m_plus_one = m_value + 1
    sample_d0 = int(delayed["sampleD0"])
    sample_start = int(delayed["sampleStart"])
    strict_power = int(delayed["sampleStartStrictPowerOfTwoUpper"])
    d0_power = 2 * n_terms
    two_power = m_value
    start_power = strict_power * m_plus_one
    decay_power = -2 * sample_start
    binary_exponent = d0_power + two_power + start_power + decay_power
    early_power = Q(int(delayed["earlyWeightPower"]) + 1, int(delayed["earlyWeightPower"]))
    endpoint_power = Q(m_value) + Q(delayed["endpointTimePower"])
    split = {
        "maximumTerms": n_terms,
        "m": m_value,
        "mPlusOne": m_plus_one,
        "sampleD0Power": d0_power,
        "sampleTwoPower": two_power,
        "sampleStart": sample_start,
        "sampleStartPowerContribution": start_power,
        "decayPowerContribution": decay_power,
        "strictBinaryUpperExponent": binary_exponent,
        "weightedEarlyPower": qstr(early_power),
        "lateMonotoneThreshold": m_plus_one,
        "endpointPower": qstr(endpoint_power),
        "endpointMonotoneThreshold": qstr(endpoint_power / 2),
    }

    ledger = fixtures["lambdaLedger"]
    weighted_power = (
        Q(ledger["gradientPrefactor"]["lambda"])
        + Q(ledger["changeOfClock"]["sPerTau"]["lambda"])
        + Q(ledger["changeOfClock"]["dsPerDtau"]["lambda"])
        + Q(ledger["weightedClock"]["K"]) * Q(ledger["clockMass"]["KPerH"]["lambda"])
    )
    endpoint_lambda_power = (
        Q(ledger["endpointClock"]["T"])
        + Q(ledger["endpointClock"]["K"]) * Q(ledger["clockMass"]["KPerH"]["lambda"])
    )
    q_squared = Q(q_count * q_count, int(a_value * a_value))
    energy = {
        "lambda": qstr(lambda_value),
        "qSquaredOverASquared": qstr(q_squared),
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

    tags = [int(value) for value in re.findall(r"\\tag\{E\.(\d+)\}", main_text)]
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])E\.(\d+)", main_text)]
    opens = len(re.findall(r"(?m)^\\\[$", main_text))
    closes = len(re.findall(r"(?m)^\\\]$", main_text))

    checks = {
        "bindings": {
            "main_hash": bindings[f"research/{STEM}.md"]["expectedSha256"] == bindings[f"research/{STEM}.md"]["observedSha256"],
            "primary_hash": bindings[f"research/{STEM}_primary_audit.md"]["expectedSha256"] == bindings[f"research/{STEM}_primary_audit.md"]["observedSha256"],
            "source_hash": bindings["research/r076e_report-source.md"]["expectedSha256"] == bindings["research/r076e_report-source.md"]["observedSha256"],
            "d_hash": bindings["research/r076d_quantitative_growing_mode_entropy_window.md"]["expectedSha256"] == bindings["research/r076d_quantitative_growing_mode_entropy_window.md"]["observedSha256"],
            "r_hash": bindings["research/r075r_outer_cap_spectral_concentration_obstruction.md"]["expectedSha256"] == bindings["research/r075r_outer_cap_spectral_concentration_obstruction.md"]["observedSha256"],
            "clock_hash": bindings["research/r075b_bulk_clock_outer_padding_gate.md"]["expectedSha256"] == bindings["research/r075b_bulk_clock_outer_padding_gate.md"]["observedSha256"],
        },
        "inputs": {
            "fixture_hash": sha256(FIXTURES) == FIXTURES_SHA256,
            "expected_hash": sha256(EXPECTED) == EXPECTED_SHA256,
            "fixture_schema": fixtures["schema"] == "r076e-linear-modal-entropy-window-fixtures-v1",
            "expected_schema": expected["schema"] == "r076e-linear-modal-entropy-window-expected-v1",
        },
        "integrity": {
            "utf8": all(clean_bytes(raw) for raw in raws),
            "controls": clean_bytes(raws[0]),
            "no_cr": all(b"\r" not in raw for raw in raws),
            "no_trailing": all(not line.endswith((" ", "\t")) for value in (main_text, primary_text, source_text) for line in value.splitlines()),
            "tags": tags == list(range(1, 35)),
            "display_opens": opens == 38,
            "display_closes": closes == 38,
            "unnumbered": opens - len(tags) == 4,
            "references": not (set(refs) - set(tags)),
            "tex_qquad": re.search(r"(?<!\\)\bqquad\b", main_text) is None,
            "tex_quad": re.search(r"(?<!\\)\bquad\b", main_text) is None,
            "tex_frac": re.search(r"(?<!\\)\bfrac\{", main_text) is None,
            "tex_linebreak": re.search(r"(?m)(?<!\\)\\$", main_text) is None,
        },
        "geometry": {
            "delta_order": 0 < delta0 < delta,
            "support_radius": geometry["supportRadius"] == expected["geometry"]["supportRadius"],
            "support_bound": geometry["supportWithinThreeHalves"] == expected["geometry"]["supportWithinThreeHalves"],
            "plateau_length": geometry["centralPlateauLength"] == expected["geometry"]["centralPlateauLength"],
            "plateau_bound": geometry["centralPlateauAtLeastOne"] == expected["geometry"]["centralPlateauAtLeastOne"],
        },
        "scaled": {
            "positive_q": q_count >= 1,
            "integer_modes": all(value.denominator == 1 and value >= 1 for value in modes),
            "ordered_modes": modes == sorted(set(modes)),
            "dyadic_band": scaled["dyadicBand"] == expected["scaledCase"]["dyadicBand"],
            "ell": scaled["ell"] == expected["scaledCase"]["ell"],
            "kappas": scaled["kappas"] == expected["scaledCase"]["kappas"],
            "alpha": scaled["alpha"] == expected["scaledCase"]["alpha"],
            "n1r": scaled["n1R"] == expected["scaledCase"]["n1R"],
            "lambda": scaled["lambda"] == expected["scaledCase"]["lambda"] and lambda_value == n1r ** 2,
            "clock_t": scaled["T"] == expected["scaledCase"]["T"],
            "clock_mass": scaled["KOverH"] == expected["scaledCase"]["KOverH"],
            "velocity": scaled["v"] == expected["scaledCase"]["v"],
            "real_band": scaled["realPartsWithinMinusFourMinusOne"] == expected["scaledCase"]["realPartsWithinMinusFourMinusOne"],
        },
        "space": {
            "term_count": space["maximumTerms"] == expected["spatialObservation"]["maximumTerms"],
            "turan_power": space["turanExponent"] == expected["spatialObservation"]["turanExponent"],
            "chebyshev": Q(fixtures["spatialObservation"]["chebyshevMeasureLower"]) == Q(1, 2),
            "length_ratio": space["lengthRatio"] == expected["spatialObservation"]["lengthRatio"],
            "spatial_formula": fragments(compact, [r"D^{2q}h(s)^{1/3}", r"(\alpha+q)^{-1}\|G_z(s)\|_{L^\infty(J)}"]),
            "gap_free": fragments(compact_primary, ["No imaginary-frequency size", "gap, or spectral-gap denominator"]),
        },
        "split": {
            "terms": split["maximumTerms"] == expected["delayedSplit"]["maximumTerms"],
            "m": split["m"] == expected["delayedSplit"]["m"],
            "m_plus_one": split["mPlusOne"] == expected["delayedSplit"]["mPlusOne"],
            "d0_power": split["sampleD0Power"] == expected["delayedSplit"]["sampleD0Power"] and sample_d0 == 2,
            "two_power": split["sampleTwoPower"] == expected["delayedSplit"]["sampleTwoPower"],
            "start": split["sampleStart"] == expected["delayedSplit"]["sampleStart"],
            "start_conditions": sample_start >= max(4, m_plus_one) and sample_start < 2 ** strict_power,
            "start_power": split["sampleStartPowerContribution"] == expected["delayedSplit"]["sampleStartPowerContribution"],
            "decay_power": split["decayPowerContribution"] == expected["delayedSplit"]["decayPowerContribution"],
            "binary_exponent": split["strictBinaryUpperExponent"] == expected["delayedSplit"]["strictBinaryUpperExponent"],
            "binary_negative": binary_exponent < 0,
            "early_power": split["weightedEarlyPower"] == expected["delayedSplit"]["weightedEarlyPower"],
            "late_threshold": split["lateMonotoneThreshold"] == expected["delayedSplit"]["lateMonotoneThreshold"],
            "late_monotone": sample_start >= m_plus_one,
            "endpoint_power": split["endpointPower"] == expected["delayedSplit"]["endpointPower"],
            "endpoint_threshold": split["endpointMonotoneThreshold"] == expected["delayedSplit"]["endpointMonotoneThreshold"] and sample_start >= endpoint_power / 2,
        },
        "endpoint": {
            "unit_length": Q(fixtures["lastUnit"]["intervalLength"]) == Q(expected["lastUnit"]["intervalLength"]),
            "unit_chebyshev": Q(fixtures["lastUnit"]["chebyshevMeasureLower"]) == Q(1, 2),
            "unit_ratio": qstr(Q(fixtures["lastUnit"]["intervalLength"]) / Q(fixtures["lastUnit"]["chebyshevMeasureLower"])) == expected["lastUnit"]["lengthRatio"],
            "finite_insertion": fragments(compact, [r"S_N^{2/3}T^{-2/3}", "4<=T<=S_N"]),
            "finite_absorption": compact.count(r"D_1^{2N}S_N^{2/3}") == 1 and compact.count(r"\le e^{CN}T^{-2/3}") >= 1,
            "large_monotone": compact.count("`T^(m+2/3)e^(-2T)` decreases") == 1,
            "stronger_power": fragments(compact, ["stronger power `m+1` in E.15", "S_N^{m+2/3}e^{-2S_N}"]),
            "endpoint_formula": compact.count(r"k(T)^{2/3}\le e^{CN}T^{-2/3}K_T^{2/3}") == 1,
            "full_mass": compact.count("full `K_T`") == 1 and compact.count("full mass") >= 1,
            "no_factorial": compact.count("Endpoint estimate without a factorial") == 1,
        },
        "energy": {
            "gradient_lambda": energy["lambda"] == expected["energy"]["lambda"],
            "q_squared": energy["qSquaredOverASquared"] == expected["energy"]["qSquaredOverASquared"],
            "gradient_coefficient": energy["gradientCoefficient"] == expected["energy"]["gradientCoefficient"],
            "weighted_power": energy["weightedLambdaPower"] == expected["energy"]["weightedLambdaPower"],
            "endpoint_lambda_power": energy["endpointLambdaPower"] == expected["energy"]["endpointLambdaPower"],
            "heat_clock_mass": compact.count(r"K_T=\lambda H") == 1,
            "cutoff_definition": compact.count("Define `zeta(s):=eta_R(R^2s)`") == 1,
            "cutoff_rows": fragments(compact, [r"\zeta(0)=0", r"|\zeta'|\le C_\eta", r"\zeta(s)\le C_\eta s"]),
            "energy_identity": fragments(compact, [r"exact identity for the complete real square", r"2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2"]),
            "gradient_inequality": compact_primary.count("a^(-2)(alpha+q)^2 <= C(lambda+q^2/a^2)") == 1,
            "q_absorption": fragments(compact, ["q^2/a^2` part costs at most `q^2`", "absorbed by one `e^(C_*q)`"]),
            "speed_zero": compact_primary.count("`B=0` remains covered") == 1,
        },
        "scale": {
            "flux_prefactor": scale["fluxPrefactor"] == expected["scaleLedger"]["fluxPrefactor"],
            "mass_prefactor": scale["massPrefactor"] == expected["scaleLedger"]["massPrefactor"],
            "target": scale["afterMass"] == expected["scaleLedger"]["afterMass"],
            "normalized": scale["normalized"] == expected["scaleLedger"]["normalized"],
            "r_cancel": scale["normalized"]["R"] == 0,
            "frozen_rate": scale["frozenRate"] == expected["scaleLedger"]["frozenRate"],
            "new_window": compact.count("q(L)=o(L^2)") >= 2,
            "witness_new": fixtures["windowWitness"]["newRatio"] == expected["windowWitness"]["newRatio"] and expected["windowWitness"]["newLimit"] == 0,
            "witness_old": fixtures["windowWitness"]["oldRatio"] == expected["windowWitness"]["oldRatio"] and expected["windowWitness"]["oldLimit"] == 2,
        },
        "proof": {
            "main_bound": fragments(compact, [r"|\mathcal T_{\boldsymbol n,R}|", r"\le e^{C_*q}a^{2/3}R^{-1/3}"]),
            "normalized_bound": fragments(compact, [r"\mathfrak X_{\boldsymbol n,R}", r"\le e^{C_*q}a^{2/3}\omega^{1/3}"]),
            "stable_family": fragments(compact, [r"-4\le\operatorname {Re}\mu_r\le-1", r"K_U:=\int_0^Uk(\tau)d\tau"]),
            "split_choice": fragments(compact, [r"S_N=C_0N\log(N+1)", r"D_0^{2N}2^mS_N^{m+1}e^{-2S_N}\le1"]),
            "early_bound": fragments(compact, ["4^{-1/3}S_N^{4/3}K_T^{2/3}", "full observed mass"]),
            "late_bound": fragments(compact, [r"\int_{S_N}^\infty", r"\le1"]),
            "weighted_bound": compact.count(r"[N\log(N+1)]^{4/3}K_T^{2/3}") == 1,
            "endpoint_bound": compact.count("e^{CN}T^{-2/3}K_T^{2/3}") >= 2,
            "bounded_branch": compact.count("If `lambda<=1`") == 1,
            "heat_branch": compact.count("If `lambda>1`") == 1,
            "onset_bound": fragments(compact, [r"[q\log(q+1)]^{4/3}", r"\lambda^{-1/3}H^{2/3}"]),
            "physical_row": fragments(compact, [r"\frac{a^2R^3}{2}v", r"4\pi\delta_0a^2R^5H"]),
            "exact_pde": compact.count(r"\partial_tF+B\partial_2F-\partial_2^2F=0") == 1,
            "complete_square": compact.count("complete real square is") == 1,
            "no_projection": compact.count("It does not apply to a Fourier projection of a larger field") == 1,
        },
        "source": {
            "nazarov": source_text.count("https://www.mathnet.ru/eng/aa397") == 1,
            "friedland_yomdin": source_text.count("https://arxiv.org/abs/1107.0039") == 1,
            "erdelyi": source_text.count("https://people.tamu.edu/~terdelyi/papers-online/sbornik150R.pdf") == 1,
            "theorem_number": compact_source.count("Theorem 2.7.1") >= 1,
            "complex_scope": compact_source.count("complex temporal exponents") >= 1,
            "adjacent_real": source_text.count("remez7.pdf") == 1,
            "adjacent_shift": source_text.count("papers-online/SP.pdf") == 1,
            "local_split": compact_source.count("local improvement from `exp(Cq log(q+1))` to `exp(Cq)`") == 1,
            "source_table": compact_source.count("| centered stable tail E.13 |") == 1,
            "no_new_theorem": compact_source.count("needs no new external theorem") == 1,
            "no_novelty": fragments(compact_source, ["no literature completeness", "novelty, priority, or sharpness"]),
            "finite_not_proof": compact_source.count("Finite arithmetic may audit") == 1,
            "primary_pass": primary_text.count("Current verdict: **PASS**") == 1,
            "blocker_zero": fragments(primary_text, ["Mathematical blocker count: **0**", "Release blocker count: **0**"]),
        },
        "boundary": {
            "exact_shear": compact.count("exact real constant-shear family") >= 1,
            "one_band": compact.count("one dyadic band") >= 1,
            "growing_constant": compact.count("not uniform in `q`") == 1,
            "r075r_compatible": fragments(compact, ["R0.75R concerns an arbitrary growing packet", "not contradicted"]),
            "arbitrary_packets_open": compact.count("arbitrary packets") >= 1,
            "version_m_conditional": compact.count("Version-M") >= 2,
            "regularity_open": compact.count("regularity") >= 1,
            "singularity_open": compact.count("singularity") >= 1,
            "no_figure": compact.count("No simulation or formal scientific figure is claimed") == 1,
            "no_simulation": compact_primary.count("No simulation or formal scientific figure is claimed") == 1,
            "not_clay": main_text.count("**NOT CLAY.**") == 1 and source_text.count("**NOT CLAY.**") == 1 and primary_text.count("**NOT CLAY.**") == 1,
            "sole_publisher": compact_primary.count("sole FIFO publisher") == 1,
        },
    }

    for group, names in GROUPS.items():
        if list(checks[group]) != names:
            raise SystemExit(f"check inventory mismatch in {group}")
    if MUTATION:
        for group in checks.values():
            if MUTATION in group:
                group[MUTATION] = False

    assertions = sum(len(group) for group in checks.values())
    passed = sum(sum(value is True for value in group.values()) for group in checks.values())
    verdict = "PASS" if passed == assertions else "FAIL"
    exact = {
        "geometry": geometry,
        "scaledCase": scaled,
        "spatialObservation": space,
        "delayedSplit": split,
        "energy": energy,
        "scaleLedger": scale,
    }
    result = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertionsPassed": passed,
        "assertionsTotal": assertions,
        "bindings": bindings,
        "checks": checks,
        "exact": exact,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "limits": [
            "finite arithmetic is not proof of Turan--Nazarov or Erdelyi",
            "finite arithmetic is not proof of the continuum collar-flux theorem",
            "the result is restricted to the stated exact-shear family",
            "regularity and singularity remain open",
        ],
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# R0.76E exact finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{assertions}",
        f"- Negative mutations registered: {len(NEGATIVE_MUTATIONS)}",
        f"- Main note SHA-256: `{sha256(MAIN)}`",
        f"- Primary audit SHA-256: `{sha256(PRIMARY)}`",
        f"- Source report SHA-256: `{sha256(SOURCE)}`",
        "",
        "## Exact fixture",
        "",
        f"- `q={q_count}`, `N={n_terms}`, `m={m_value}`, `S={sample_start}`.",
        f"- Strict binary tail upper exponent: `{binary_exponent}`.",
        f"- Early split power: `{qstr(early_power)}`; endpoint power: `{qstr(endpoint_power)}`.",
        f"- `lambda={qstr(lambda_value)}`; weighted carrier power: `{qstr(weighted_power)}`; endpoint carrier power: `{qstr(endpoint_lambda_power)}`.",
        f"- Frozen normalized rate: `{scale['frozenRate']}`.",
        "",
        "## Boundary",
        "",
        "The fixture checks exact split, monotonicity, carrier, and scaling ledgers.",
        "Finite arithmetic is not proof of Turan--Nazarov, Erdelyi, the analytic energy identity, or the continuum collar-flux theorem.",
        "Arbitrary packets, Version-M extraction, regularity, and singularity remain open. **NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"schema": SCHEMA, "verdict": verdict, "assertions": assertions}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
