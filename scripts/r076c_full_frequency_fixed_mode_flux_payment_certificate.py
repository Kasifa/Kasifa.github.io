#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.76C."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076c_full_frequency_fixed_mode_flux_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076c_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076C_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076C_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076C_MUTATION", "")
SCHEMA = "r076c-full-frequency-fixed-mode-flux-payment-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf",
    f"research/{STEM}_primary_audit.md":
        "d60546eab80d2fa6ef633efeb0b34120d7b9f81a33249e500f8d94b9a8c15f74",
    "research/r076c_report-source.md":
        "be523d313f5a487fd0b1550cb948f1e05b117f6d1734b8d9cbfd5ab1b5d57b27",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075x_fixed_finite_mode_low_carrier_payment.md":
        "8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763",
    "research/r076b_moderate_carrier_fixed_mode_flux_payment.md":
        "a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d",
}
FIXTURES_SHA256 = "36d1612b57932fad7ff6e9a4375b842d4900b0868625cfb5d498ce89a4dcee82"
EXPECTED_SHA256 = "6dbd56d366b6b048acd769ff5b5eff303ede111153330de763ec04cee571ad52"

GROUPS = {
    "bindings": (
        "main_hash", "primary_hash", "source_hash", "clock_hash",
        "outer_hash", "low_hash", "moderate_hash",
    ),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema", "expected_schema"),
    "integrity": (
        "utf8", "controls", "tags", "display_opens", "display_closes",
        "references", "tex_qquad", "tex_zeta_prime",
    ),
    "geometry": (
        "delta_order", "support_radius", "support_bound", "plateau_length",
        "plateau_bound", "xi_mass", "xi_second_scale",
    ),
    "family": (
        "fixed_q", "integer_modes", "ordered_modes", "real_phases",
        "nonnegative_amplitudes", "real_speed", "dyadic_band",
        "no_carrier_upper", "constant_dependencies",
    ),
    "scaled": (
        "ell", "kappas", "alpha", "ratios", "scaled_gaps", "threshold",
        "high_spatial_branch", "n1r", "lambda", "ultrahigh_branch",
        "velocity", "physical_end", "original_heat_rates",
        "rescaled_real", "rescaled_imaginary", "real_band", "scaled_pde",
    ),
    "space": (
        "maximum_terms", "turan_power", "scaled_i", "chebyshev_measure",
        "scaled_jplus", "length_ratio", "margin", "normalized_derivative",
        "gap_free_space",
    ),
    "time_lemma": (
        "lemma_terms", "lemma_real_band", "family_hypothesis", "center_shift",
        "shifted_lower", "shifted_upper", "sublevel_measure", "subset_y",
        "interval_factor", "net_decay", "pointwise_tail", "weighted_tail",
        "endpoint_tail", "clock_lower", "imaginary_free", "gap_free_time",
    ),
    "ultrahigh": (
        "clock_t", "clock_mass", "zeta_onset", "zeta_linear",
        "gradient_prefactor", "clock_change", "weighted_lambda_power",
        "endpoint_lambda_power", "uniform_endpoint",
    ),
    "identity": (
        "square_pde", "advective_row", "energy_derivative", "xi_second",
        "dissipation", "heat_cancel", "identity_signs", "onset_endpoint",
        "complete_real_square",
    ),
    "point": (
        "point_g", "point_gz", "point_gzz", "point_gs", "point_residual",
    ),
    "payment": (
        "value_rows", "gradient_row", "gradient_paid", "terminal_paid",
        "dimensionless_payment", "low_branch", "full_frequency_union",
        "no_sign_drop",
    ),
    "scale": (
        "fibre_area", "mass_a", "mass_r", "flux_prefactor", "target_a",
        "target_r", "target_m", "r_cancel", "omega_power", "frozen_rate",
    ),
    "source_audit": (
        "nazarov", "friedland_yomdin", "theorem_restatement",
        "imaginary_statement", "local_corollary", "no_novelty",
        "primary_pass", "math_zero", "release_zero", "finite_not_proof",
        "no_figure",
    ),
    "boundary": (
        "fixed_q_only", "growing_q_open", "packets_open", "larger_field_open",
        "analytic_subblock_unused", "sign_route_rejected", "carrier_ibp_rejected",
        "version_m_conditional", "regularity_open", "singularity_open", "not_clay",
    ),
}
NEGATIVE_MUTATIONS = tuple(name for names in GROUPS.values() for name in names)


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


def all_in(value: str, fragments: list[str]) -> bool:
    return all(fragment in value for fragment in fragments)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def encoded(powers: dict[str, Q]) -> dict[str, str | int]:
    return {
        key: int(value) if value.denominator == 1 else qstr(value)
        for key, value in powers.items()
    }


def poly_mul(left: list[Q], right: list[Q]) -> list[Q]:
    result = [Q(0)] * (len(left) + len(right) - 1)
    for i, x_value in enumerate(left):
        for j, y_value in enumerate(right):
            result[i + j] += x_value * y_value
    return result


def poly_derivative(poly: list[Q], order: int = 1) -> list[Q]:
    result = list(poly)
    for _ in range(order):
        result = [Q(index) * result[index] for index in range(1, len(result))]
    return result


def symmetric_integral(poly: list[Q]) -> Q:
    return sum(
        (Q(2) * value / Q(index + 1) if index % 2 == 0 else Q(0))
        for index, value in enumerate(poly)
    )


def phase_cos_sin(value: Q) -> tuple[Q, Q]:
    table = {Q(0): (Q(1), Q(0)), Q(1, 2): (Q(0), Q(1)), Q(1): (Q(-1), Q(0))}
    if value not in table:
        raise ValueError(f"unsupported exact phase: {value}")
    return table[value]


def compare(actual: Any, expected: Any) -> bool:
    return actual == expected


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076C_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76C suite")

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

    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(FROZEN.items())
    }

    profile = fixtures["profile"]
    delta0 = Q(profile["delta0"])
    delta = Q(profile["delta"])
    case = fixtures["scaledCase"]
    q_count = int(case["q"])
    a_value = Q(case["a"])
    radius = Q(case["R"])
    b_shear = Q(case["B"])
    modes = [Q(value) for value in case["frequencies"]]
    amplitudes = [Q(value) for value in case["amplitudes"]]
    phases = [Q(value) for value in case["phasesOverPi"]]
    clock_end = Q(fixtures["clock"]["scaledClockEnd"])
    ell = a_value * radius
    kappas = [mode * ell for mode in modes]
    alpha = kappas[0]
    ratios = [value / alpha for value in kappas]
    gaps = [right - left for left, right in zip(kappas, kappas[1:])]
    velocity = b_shear * radius / a_value
    n1r = modes[0] * radius
    lambda_value = alpha * alpha / (a_value * a_value)
    original_heat = [value * value / (a_value * a_value) for value in kappas]
    rescaled_real = [value * value / (alpha * alpha) for value in kappas]
    rescaled_imag = [value * velocity / lambda_value for value in kappas]
    threshold = 8 * q_count
    temporal_end = clock_end * lambda_value
    computed_case = {
        "ell": qstr(ell),
        "kappas": [qstr(value) for value in kappas],
        "alpha": qstr(alpha),
        "ratios": [qstr(value) for value in ratios],
        "gaps": [qstr(value) for value in gaps],
        "threshold": threshold,
        "highSpatialBranch": alpha >= threshold,
        "n1R": qstr(n1r),
        "lambda": qstr(lambda_value),
        "ultraHighBranch": lambda_value > 1,
        "dyadicBand": modes[-1] <= 2 * modes[0],
        "v": qstr(velocity),
        "physicalEnd": qstr(clock_end * radius * radius),
        "originalHeatRates": [qstr(value) for value in original_heat],
        "rescaledRealMagnitudes": [qstr(value) for value in rescaled_real],
        "rescaledImaginaryMagnitudes": [qstr(value) for value in rescaled_imag],
        "realPartsWithinMinusFourMinusOne": min(rescaled_real) >= 1 and max(rescaled_real) <= 4,
    }

    support_radius = 1 + delta / a_value
    plateau_length = 2 - 2 * delta / a_value
    computed_geometry = {
        "supportRadius": qstr(support_radius),
        "supportWithinThreeHalves": support_radius <= Q(3, 2),
        "centralPlateauLength": qstr(plateau_length),
        "centralPlateauAtLeastOne": plateau_length >= 1,
        "xiMassLowerOverPi": qstr(2 * delta0),
        "xiSecondCoefficientScale": qstr(1 / a_value),
    }

    windows = fixtures["spatialWindows"]
    i_length = Q(windows["I"][1]) - Q(windows["I"][0])
    jp_length = Q(windows["Jplus"][1]) - Q(windows["Jplus"][0])
    scaled_i = alpha * i_length
    cheb_lower = scaled_i / Q(windows["chebyshevThreshold"])
    scaled_jp = alpha * jp_length
    margin = alpha * (Q(windows["Jplus"][1]) - Q(windows["J"][1]))
    computed_space = {
        "maximumTerms": 2 * q_count,
        "turanExponent": 2 * q_count - 1,
        "scaledIMeasure": qstr(scaled_i),
        "chebyshevMeasureLower": qstr(cheb_lower),
        "scaledJplusMeasure": qstr(scaled_jp),
        "lengthRatio": qstr(scaled_jp / cheb_lower),
        "margin": qstr(margin),
        "normalizedPointDerivative": qstr(2 * kappas[1] / alpha),
    }

    shift = Q(5, 2)
    shifted_lower = -Q(4) + shift
    shifted_upper = -Q(1) + shift
    net_decay = -shift + max(abs(shifted_lower), abs(shifted_upper))
    ledger = fixtures["lambdaLedger"]
    weighted_power = (
        Q(ledger["gradientPrefactor"]["lambda"])
        + Q(ledger["changeOfClock"]["sPerTau"]["lambda"])
        + Q(ledger["changeOfClock"]["dsPerDtau"]["lambda"])
        + Q(ledger["weightedTail"]["K"]) * Q(ledger["clockMass"]["KPerH"]["lambda"])
    )
    endpoint_power = (
        Q(ledger["endpointTail"]["T"])
        + Q(ledger["endpointTail"]["K"]) * Q(ledger["clockMass"]["KPerH"]["lambda"])
    )
    computed_time = {
        "maximumTerms": 2 * q_count,
        "turanExponent": 2 * q_count - 1,
        "sublevelMeasureLower": "1/2",
        "centerShift": qstr(shift),
        "shiftedRealLower": qstr(shifted_lower),
        "shiftedRealUpper": qstr(shifted_upper),
        "netDecay": qstr(net_decay),
        "T": qstr(temporal_end),
        "KOverH": qstr(lambda_value),
        "weightedLambdaPower": qstr(weighted_power),
        "endpointLambdaPower": qstr(endpoint_power),
        "gapFactor": "0",
    }

    cos_sin = [phase_cos_sin(value) for value in phases]
    point_g = sum((amp * cs[0] for amp, cs in zip(amplitudes, cos_sin)), Q(0))
    point_gz = sum((amp * kappa * cs[1] for amp, kappa, cs in zip(amplitudes, kappas, cos_sin)), Q(0))
    point_gzz = -sum((amp * kappa * kappa * cs[0] for amp, kappa, cs in zip(amplitudes, kappas, cos_sin)), Q(0))
    point_gs = sum((
        amp * (-rate * cs[0] - kappa * velocity * cs[1])
        for amp, kappa, rate, cs in zip(amplitudes, kappas, original_heat, cos_sin)
    ), Q(0))
    residual = point_gs + velocity * point_gz - point_gzz / (a_value * a_value)
    computed_point = {
        "G": qstr(point_g),
        "Gz": qstr(point_gz),
        "Gzz": qstr(point_gzz),
        "Gs": qstr(point_gs),
        "scaledPdeResidual": qstr(residual),
    }

    identity = fixtures["transportIdentity"]
    i_velocity = Q(identity["v"])
    i_time = Q(identity["s"])
    i_a = Q(identity["a"])
    xi = [Q(1), Q(0), Q(-2), Q(0), Q(1)]
    w_kernel = poly_derivative(xi)
    g_poly = [-i_velocity * i_time, Q(1)]
    g_squared = poly_mul(g_poly, g_poly)
    advective = i_velocity * symmetric_integral(poly_mul(w_kernel, g_squared))
    energy_derivative = -2 * i_velocity * symmetric_integral(poly_mul(xi, g_poly))
    xi_second = symmetric_integral(poly_mul(poly_derivative(xi, 2), g_squared))
    dissipation = symmetric_integral(xi)
    heat_cancellation = -xi_second / (i_a * i_a) + 2 * dissipation / (i_a * i_a)
    computed_identity = {
        "advectiveRow": qstr(advective),
        "energyDerivative": qstr(energy_derivative),
        "xiSecondRow": qstr(xi_second),
        "dissipationRow": qstr(dissipation),
        "heatCancellation": qstr(heat_cancellation),
    }

    computed_scale = {
        "fluxPrefactor": encoded({"a": Q(2), "R": Q(3), "v": Q(1)}),
        "massPrefactor": encoded({"a": Q(2), "R": Q(5), "H": Q(1)}),
        "afterMass": encoded({"a": Q(2, 3), "R": Q(-1, 3), "M": Q(2, 3)}),
        "normalized": encoded({"a": Q(2, 3), "R": Q(0), "omega": Q(1, 3), "p": Q(2, 3)}),
        "frozenRate": qstr(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{C\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"(?<![A-Za-z0-9_.])C\.(\d+)", text)]
    binding_keys = list(sorted(FROZEN))
    checks: dict[str, dict[str, bool]] = {
        "bindings": {
            "main_hash": bindings[binding_keys[4]]["observedSha256"] == bindings[binding_keys[4]]["expectedSha256"],
            "primary_hash": bindings[binding_keys[5]]["observedSha256"] == bindings[binding_keys[5]]["expectedSha256"],
            "source_hash": bindings[binding_keys[6]]["observedSha256"] == bindings[binding_keys[6]]["expectedSha256"],
            "clock_hash": bindings[binding_keys[0]]["observedSha256"] == bindings[binding_keys[0]]["expectedSha256"],
            "outer_hash": bindings[binding_keys[1]]["observedSha256"] == bindings[binding_keys[1]]["expectedSha256"],
            "low_hash": bindings[binding_keys[2]]["observedSha256"] == bindings[binding_keys[2]]["expectedSha256"],
            "moderate_hash": bindings[binding_keys[3]]["observedSha256"] == bindings[binding_keys[3]]["expectedSha256"],
        },
        "inputs": {
            "fixture_hash": sha256(FIXTURES) == FIXTURES_SHA256,
            "expected_hash": sha256(EXPECTED) == EXPECTED_SHA256,
            "fixture_schema": fixtures.get("schema") == "r076c-full-frequency-fixed-mode-flux-payment-fixtures-v1",
            "expected_schema": expected.get("schema") == "r076c-full-frequency-fixed-mode-flux-payment-expected-v1",
        },
        "integrity": {
            "utf8": all(clean_bytes(value) for value in (raw, raw_primary, raw_source)),
            "controls": clean_bytes(raw),
            "tags": tags == list(range(1, 36)),
            "display_opens": text.count("\\[") == 35,
            "display_closes": text.count("\\]") == 35,
            "references": set(refs).issubset(set(tags)),
            "tex_qquad": re.search(r"(?<!\\)\bqquad\b", text) is None,
            "tex_zeta_prime": "zeta'Eds" not in text and "\\zeta'E\\,ds" in text,
        },
        "geometry": {
            "delta_order": Q(0) < delta0 < delta,
            "support_radius": computed_geometry["supportRadius"] == expected["geometry"]["supportRadius"],
            "support_bound": computed_geometry["supportWithinThreeHalves"] is expected["geometry"]["supportWithinThreeHalves"],
            "plateau_length": computed_geometry["centralPlateauLength"] == expected["geometry"]["centralPlateauLength"],
            "plateau_bound": computed_geometry["centralPlateauAtLeastOne"] is expected["geometry"]["centralPlateauAtLeastOne"],
            "xi_mass": computed_geometry["xiMassLowerOverPi"] == expected["geometry"]["xiMassLowerOverPi"],
            "xi_second_scale": computed_geometry["xiSecondCoefficientScale"] == expected["geometry"]["xiSecondCoefficientScale"],
        },
        "family": {
            "fixed_q": "Fix an integer `q>=1`" in compact,
            "integer_modes": r"n_1,\ldots,n_q\in\mathbb N" in compact,
            "ordered_modes": r"1\le n_1<n_2<\cdots<n_q\le2n_1" in compact,
            "real_phases": r"\phi_j\in\mathbb R" in compact,
            "nonnegative_amplitudes": r"A_j\ge0" in compact,
            "real_speed": r"B\in\mathbb R" in compact,
            "dyadic_band": computed_case["dyadicBand"] is expected["scaledCase"]["dyadicBand"],
            "no_carrier_upper": "with no carrier upper bound" in compact,
            "constant_dependencies": all_in(compact, ["depending on `q` and the frozen profiles", "not on `R`, the frequencies", "phases, or `B`"]),
        },
        "scaled": {
            "ell": computed_case["ell"] == expected["scaledCase"]["ell"],
            "kappas": computed_case["kappas"] == expected["scaledCase"]["kappas"],
            "alpha": computed_case["alpha"] == expected["scaledCase"]["alpha"],
            "ratios": computed_case["ratios"] == expected["scaledCase"]["ratios"],
            "scaled_gaps": computed_case["gaps"] == expected["scaledCase"]["gaps"],
            "threshold": computed_case["threshold"] == expected["scaledCase"]["threshold"],
            "high_spatial_branch": computed_case["highSpatialBranch"] is expected["scaledCase"]["highSpatialBranch"],
            "n1r": computed_case["n1R"] == expected["scaledCase"]["n1R"],
            "lambda": computed_case["lambda"] == expected["scaledCase"]["lambda"] and lambda_value == n1r * n1r,
            "ultrahigh_branch": computed_case["ultraHighBranch"] is expected["scaledCase"]["ultraHighBranch"],
            "velocity": computed_case["v"] == expected["scaledCase"]["v"],
            "physical_end": computed_case["physicalEnd"] == expected["scaledCase"]["physicalEnd"],
            "original_heat_rates": computed_case["originalHeatRates"] == expected["scaledCase"]["originalHeatRates"],
            "rescaled_real": computed_case["rescaledRealMagnitudes"] == expected["scaledCase"]["rescaledRealMagnitudes"],
            "rescaled_imaginary": computed_case["rescaledImaginaryMagnitudes"] == expected["scaledCase"]["rescaledImaginaryMagnitudes"],
            "real_band": computed_case["realPartsWithinMinusFourMinusOne"] is expected["scaledCase"]["realPartsWithinMinusFourMinusOne"],
            "scaled_pde": all_in(compact, [r"G_s+vG_z-a^{-2}G_{zz}=0", r"\lambda=\frac{\alpha^2}{a^2}=(n_1R)^2>1"]),
        },
        "space": {
            "maximum_terms": computed_space["maximumTerms"] == expected["spatialObservation"]["maximumTerms"],
            "turan_power": computed_space["turanExponent"] == expected["spatialObservation"]["turanExponent"],
            "scaled_i": computed_space["scaledIMeasure"] == expected["spatialObservation"]["scaledIMeasure"],
            "chebyshev_measure": computed_space["chebyshevMeasureLower"] == expected["spatialObservation"]["chebyshevMeasureLower"],
            "scaled_jplus": computed_space["scaledJplusMeasure"] == expected["spatialObservation"]["scaledJplusMeasure"],
            "length_ratio": computed_space["lengthRatio"] == expected["spatialObservation"]["lengthRatio"],
            "margin": computed_space["margin"] == expected["spatialObservation"]["margin"],
            "normalized_derivative": computed_space["normalizedPointDerivative"] == expected["spatialObservation"]["normalizedPointDerivative"],
            "gap_free_space": all_in(compact, ["spatial observation proved in R0.76B", "arbitrary frequency gaps"]),
        },
        "time_lemma": {
            "lemma_terms": all_in(compact, [r"Q(\tau)=\sum_{r=1}^{N}c_re^{\mu_r\tau}", r"N\le2q"]),
            "lemma_real_band": r"-4\le\operatorname {Re}\mu_r\le-1" in compact,
            "family_hypothesis": "with every `Q(.;z)` an exponential polynomial satisfying C.12" in compact,
            "center_shift": computed_time["centerShift"] == expected["temporalClock"]["centerShift"] and r"Y(r)=e^{5r/2}Q(r)" in compact,
            "shifted_lower": computed_time["shiftedRealLower"] == expected["temporalClock"]["shiftedRealLower"],
            "shifted_upper": computed_time["shiftedRealUpper"] == expected["temporalClock"]["shiftedRealUpper"],
            "sublevel_measure": computed_time["sublevelMeasureLower"] == expected["temporalClock"]["sublevelMeasureLower"] and r"|E|\ge\frac12" in compact,
            "subset_y": "`sup_E|Y|<=e^(5/2)(2I_Q)^(1/3)`" in compact,
            "interval_factor": "`(C tau/|E|)^(N-1)<=C_q(1+tau)^(2q-1)`" in compact,
            "net_decay": computed_time["netDecay"] == expected["temporalClock"]["netDecay"],
            "pointwise_tail": all_in(compact, [r"(1+\tau)^{3(2q-1)}e^{-3\tau}", r"\int_0^1|Q(r)|^3dr"]),
            "weighted_tail": r"\int_0^T\tau k(\tau)^{2/3}d\tau" in compact,
            "endpoint_tail": all_in(compact, [r"k(T)^{2/3}\le C_qT^{-2/3}K_T^{2/3}", "T^(2(2q-1)+2/3)e^(-2T)"]),
            "clock_lower": r"T\ge4" in compact,
            "imaginary_free": "independent of all imaginary parts" in compact,
            "gap_free_time": "independent of all imaginary parts and exponent gaps" in compact,
        },
        "ultrahigh": {
            "clock_t": computed_time["T"] == expected["temporalClock"]["T"] and r"T=4\lambda" in compact,
            "clock_mass": computed_time["KOverH"] == expected["temporalClock"]["KOverH"] and r"K_T=\int_0^{4\lambda}k(\tau)d\tau=\lambda H" in compact,
            "zeta_onset": all_in(compact, ["`zeta(s)=eta_R(R^2s)`", r"\eta_R(0)=0"]),
            "zeta_linear": r"0\le\zeta(s)\le C_\eta s" in compact,
            "gradient_prefactor": r"a^(-2)int Xi_a|G_z|^2<=C_q lambda h^(2/3)" in compact,
            "clock_change": r"\tau=\lambda s" in compact,
            "weighted_lambda_power": computed_time["weightedLambdaPower"] == expected["temporalClock"]["weightedLambdaPower"] and r"C_q\lambda^{-1/3}H^{2/3}" in compact,
            "endpoint_lambda_power": computed_time["endpointLambdaPower"] == expected["temporalClock"]["endpointLambdaPower"],
            "uniform_endpoint": all_in(compact, [r"h(4)^{2/3}=k(4\lambda)^{2/3}", r"\le C_qH^{2/3}"]),
        },
        "identity": {
            "square_pde": all_in(compact_primary, ["(G^2)_s+v(G^2)_z-a^(-2)(G^2)_zz=-2a^(-2)|G_z|^2"]),
            "advective_row": computed_identity["advectiveRow"] == expected["transportIdentity"]["advectiveRow"],
            "energy_derivative": computed_identity["energyDerivative"] == expected["transportIdentity"]["energyDerivative"],
            "xi_second": computed_identity["xiSecondRow"] == expected["transportIdentity"]["xiSecondRow"],
            "dissipation": computed_identity["dissipationRow"] == expected["transportIdentity"]["dissipationRow"],
            "heat_cancel": computed_identity["heatCancellation"] == expected["transportIdentity"]["heatCancellation"],
            "identity_signs": all_in(compact, [r"E'(s)-a^{-2}\int\Xi_a''G^2", r"+2a^{-2}\int\Xi_a|G_z|^2"]),
            "onset_endpoint": all_in(compact, ["Since `zeta(0)=0`", r"\zeta(4)E(4)-\int_0^4\zeta'E\,ds"]),
            "complete_real_square": "exact real-square identity" in compact,
        },
        "point": {
            "point_g": computed_point["G"] == expected["point"]["G"],
            "point_gz": computed_point["Gz"] == expected["point"]["Gz"],
            "point_gzz": computed_point["Gzz"] == expected["point"]["Gzz"],
            "point_gs": computed_point["Gs"] == expected["point"]["Gs"],
            "point_residual": computed_point["scaledPdeResidual"] == expected["point"]["scaledPdeResidual"],
        },
        "payment": {
            "value_rows": all_in(compact, ["value part of C.11", r"\le C_qH^{2/3}"]),
            "gradient_row": r"a^(-2)int Xi_a|G_z|^2<=C_q lambda h^(2/3)" in compact,
            "gradient_paid": "C.26 pays its time integral" in compact,
            "terminal_paid": "Equation C.27 pays the terminal row" in compact,
            "dimensionless_payment": r"\left|v\int_0^4\zeta\int W_aG^2\right| \le C_qH^{2/3}" in compact,
            "low_branch": "R0.76B supplies the complementary branch `alpha<=a`" in compact,
            "full_frequency_union": "so C.4 holds at every carrier" in compact,
            "no_sign_drop": "before any absolute value" in compact,
        },
        "scale": {
            "fibre_area": r"4\pi\delta_0a^2R^5H" in compact,
            "mass_a": computed_scale["massPrefactor"]["a"] == expected["scaleLedger"]["massPrefactor"]["a"],
            "mass_r": computed_scale["massPrefactor"]["R"] == expected["scaleLedger"]["massPrefactor"]["R"],
            "flux_prefactor": computed_scale["fluxPrefactor"] == expected["scaleLedger"]["fluxPrefactor"],
            "target_a": computed_scale["afterMass"]["a"] == expected["scaleLedger"]["afterMass"]["a"],
            "target_r": computed_scale["afterMass"]["R"] == expected["scaleLedger"]["afterMass"]["R"],
            "target_m": computed_scale["afterMass"]["M"] == expected["scaleLedger"]["afterMass"]["M"],
            "r_cancel": computed_scale["normalized"]["R"] == expected["scaleLedger"]["normalized"]["R"],
            "omega_power": computed_scale["normalized"]["omega"] == expected["scaleLedger"]["normalized"]["omega"],
            "frozen_rate": computed_scale["frozenRate"] == expected["scaleLedger"]["frozenRate"] and r"-\frac2{11907}" in compact,
        },
        "source_audit": {
            "nazarov": all_in(compact_source, ["F. L. Nazarov", "https://www.mathnet.ru/eng/aa397"]),
            "friedland_yomdin": all_in(compact_source, ["Omer Friedland and Yosef Yomdin", "https://arxiv.org/abs/1107.0039"]),
            "theorem_restatement": "Theorem 1.1" in compact_source,
            "imaginary_statement": "imaginary parts do not enter the original inequality" in compact_source,
            "local_corollary": all_in(compact_source, ["local corollary, not quoted", "local change of variables"]),
            "no_novelty": "not evidence of novelty or priority" in compact_source,
            "primary_pass": "Current verdict: **PASS**" in primary,
            "math_zero": "Mathematical blocker count: **0**" in primary,
            "release_zero": "Release blocker count: **0**" in primary,
            "finite_not_proof": all_in(compact, ["Finite fixtures may audit", "not proof of the continuum exponential-polynomial lemma"]),
            "no_figure": "No formal scientific figure or simulation is claimed" in compact,
        },
        "boundary": {
            "fixed_q_only": "only for each fixed finite `q`" in compact,
            "growing_q_open": "a quantitative constant suitable for `q=q(L)`" in compact,
            "packets_open": "arbitrary growing packets" in compact,
            "larger_field_open": "projection from a larger velocity" in compact,
            "analytic_subblock_unused": "No density/carrier splitting" in compact,
            "sign_route_rejected": "localized-current sign" in compact,
            "carrier_ibp_rejected": "standalone oscillatory integration by parts" in compact,
            "version_m_conditional": "same conditional `C_q(P_R^M)^(2/3)` consequence" in compact,
            "regularity_open": "regularity" in compact,
            "singularity_open": "singularity" in compact,
            "not_clay": "**NOT CLAY.**" in text and "**NOT CLAY.**" in source and "**NOT CLAY.**" in primary,
        },
    }

    if tuple(checks) != tuple(GROUPS):
        raise SystemExit("R0.76C group order drift")
    for group, names in GROUPS.items():
        if tuple(checks[group]) != tuple(names):
            raise SystemExit(f"R0.76C assertion manifest drift in {group}")
    if MUTATION:
        for group in GROUPS:
            if MUTATION in checks[group]:
                checks[group][MUTATION] = False
                break

    group_pass = {group: all(values.values()) for group, values in checks.items()}
    passed = all(group_pass.values())
    certificate = {
        "schema": SCHEMA,
        "verdict": "PASS" if passed else "FAIL",
        "mutation": MUTATION or None,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "bindings": bindings,
        "computed": {
            "geometry": computed_geometry,
            "scaledCase": computed_case,
            "spatialObservation": computed_space,
            "temporalClock": computed_time,
            "point": computed_point,
            "transportIdentity": computed_identity,
            "scaleLedger": computed_scale,
        },
        "assertions": checks,
        "groupPass": group_pass,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    total = sum(len(values) for values in checks.values())
    passed_count = sum(sum(bool(value) for value in values.values()) for values in checks.values())
    failed = [f"{group}.{name}" for group, values in checks.items() for name, value in values.items() if not value]
    report = [
        "# R0.76C certificate report",
        "",
        f"- Verdict: **{'PASS' if passed else 'FAIL'}**",
        f"- Assertions: {passed_count}/{total}",
        f"- Mutation: `{MUTATION or 'none'}`",
        f"- Exact ultra-high fixture: `q={q_count}`, `n_1R={qstr(n1r)}`, `lambda={qstr(lambda_value)}`, `T={qstr(temporal_end)}`.",
        f"- Weighted lambda exponent: `{qstr(weighted_power)}`; endpoint lambda exponent: `{qstr(endpoint_power)}`.",
        "- Finite exact arithmetic is not proof of Turan--Nazarov or the continuum observation lemmas.",
        "- Formal scientific figure: not applicable.",
        "- Boundary: fixed `q` exact shears only; growing packets, Version-M transfer, regularity, and singularity remain OPEN. **NOT CLAY.**",
    ]
    if failed:
        report.extend(["", "## Failed assertions", ""] + [f"- `{name}`" for name in failed])
    OUT_REPORT.write_text("\n".join(report) + "\n", encoding="utf-8")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
