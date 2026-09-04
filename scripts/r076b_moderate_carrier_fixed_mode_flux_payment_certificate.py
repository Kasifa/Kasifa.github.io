#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.76B."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r076b_moderate_carrier_fixed_mode_flux_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r076b_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R076B_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R076B_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R076B_MUTATION", "")
SCHEMA = "r076b-moderate-carrier-fixed-mode-flux-payment-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d",
    f"research/{STEM}_primary_audit.md":
        "0a6314c454021da284bbf157de36d6c2bd1683d600a21c8394f723acc26aa447",
    "research/r076b_report-source.md":
        "362fcf898a533efaf4072c876dba09f4231c131ad1c48d48efc92c52215428fc",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075w_full_frequency_two_harmonic_flux_payment.md":
        "571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4",
    "research/r075x_fixed_finite_mode_low_carrier_payment.md":
        "8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763",
    "research/r075z_unresolved_cluster_carrier_current_gate.md":
        "30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97",
    "research/r076a_complete_clock_localized_current_sign_obstruction.md":
        "d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb",
}
FIXTURES_SHA256 = "1f9b3df9cb8ff3f9d22250ce425b837d40268829bf18cb3e12b3f7d2dca64bf2"
EXPECTED_SHA256 = "4533edf290e07f1fddc5df1b9ef1655a5623f4a3714e840b1c402cdf3b8db3f1"

GROUPS = {
    "bindings": (
        "main_hash", "primary_hash", "source_hash", "b_hash", "r_hash",
        "w_hash", "x_hash", "z_hash", "a_hash",
    ),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema", "expected_schema"),
    "integrity": (
        "utf8", "controls", "tags", "display_opens", "display_closes",
        "references", "tex_left", "tex_fraction",
    ),
    "geometry": (
        "delta_order", "support_radius", "support_bound", "plateau_length",
        "plateau_bound", "xi_mass", "xi_second_scale",
    ),
    "family": (
        "fixed_q", "integer_modes", "ordered_modes", "real_phases",
        "dyadic_band", "alpha", "threshold", "high_branch", "inverse_radius",
        "scaled_gaps",
    ),
    "scaled": (
        "ell", "kappas", "ratios", "velocity", "heat_rates", "real_parts",
        "scaled_pde", "clock",
    ),
    "space_value": (
        "term_count", "turan_power", "scaled_i", "chebyshev_measure",
        "scaled_jplus", "length_ratio", "imaginary_roots", "gap_free_value",
    ),
    "space_derivative": (
        "compact_roots", "companion_family", "unit_window", "double_window",
        "margin", "jet_uniqueness", "alpha_factor", "point_derivative",
    ),
    "time_trace": (
        "temporal_terms", "temporal_power", "sublevel_measure", "real_bound",
        "imaginary_free", "gap_free_time", "terminal_trace",
    ),
    "identity": (
        "square_pde", "advective_row", "energy_derivative", "xi_second",
        "dissipation", "heat_cancel", "identity_signs", "onset",
    ),
    "point": (
        "point_g", "point_gz", "point_gzz", "point_gs", "point_residual",
        "endpoint_family",
    ),
    "payment": (
        "value_row", "xi_second_row", "gradient_ratio", "holder_time",
        "endpoint_payment", "dimensionless_payment", "full_real_square",
    ),
    "scale": (
        "fibre_area", "mass_a", "mass_r", "flux_prefactor", "target_a",
        "target_r", "target_m", "r_cancel", "omega_power", "frozen_rate",
    ),
    "source_audit": (
        "nazarov", "primary_restatement", "erdelyi", "brudnyi", "jaming_saba",
        "local_ode_proof", "no_novelty", "audit_pass", "math_zero",
        "release_zero", "finite_not_proof", "no_figure",
    ),
    "boundary": (
        "x_split", "n1r_closed", "ultrahigh_open", "growing_q_open",
        "packets_open", "analytic_subblock_unused", "carrier_ibp_rejected",
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


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R076B_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.76B suite")

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
        "source_hash": "research/r076b_report-source.md",
        "b_hash": "research/r075b_bulk_clock_outer_padding_gate.md",
        "r_hash": "research/r075r_outer_cap_spectral_concentration_obstruction.md",
        "w_hash": "research/r075w_full_frequency_two_harmonic_flux_payment.md",
        "x_hash": "research/r075x_fixed_finite_mode_low_carrier_payment.md",
        "z_hash": "research/r075z_unresolved_cluster_carrier_current_gate.md",
        "a_hash": "research/r076a_complete_clock_localized_current_sign_obstruction.md",
    }.get(MUTATION)
    if mutation_path:
        frozen[mutation_path] = "0" * 64
    bindings = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
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
    ell = a_value * radius
    kappas = [mode * ell for mode in modes]
    alpha = kappas[0]
    ratios = [value / alpha for value in kappas]
    gaps = [right - left for left, right in zip(kappas, kappas[1:])]
    velocity = b_shear * radius / a_value
    heat_rates = [value * value / (a_value * a_value) for value in kappas]
    threshold = 8 * q_count
    clock_end = Q(fixtures["clock"]["clockEnd"])
    computed_case = {
        "ell": qstr(ell),
        "alphas": [qstr(value) for value in kappas],
        "ratios": [qstr(value) for value in ratios],
        "gaps": [qstr(value) for value in gaps],
        "threshold": threshold,
        "highBranch": alpha >= threshold,
        "inverseRadiusEndpoint": modes[0] * radius == 1 and alpha == a_value,
        "dyadicBand": modes[-1] <= 2 * modes[0],
        "v": qstr(velocity),
        "physicalEnd": qstr(clock_end * radius * radius),
        "heatRates": [qstr(value) for value in heat_rates],
        "realPartsWithinFour": max(heat_rates) <= 4,
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
    j_right = Q(windows["J"][1])
    jp_right = Q(windows["Jplus"][1])
    margin = alpha * (jp_right - j_right)
    computed_space = {
        "maximumTerms": 2 * q_count,
        "turanExponent": 2 * q_count - 1,
        "scaledIMeasure": qstr(scaled_i),
        "chebyshevMeasureLower": qstr(cheb_lower),
        "scaledJplusMeasure": qstr(scaled_jp),
        "lengthRatio": qstr(scaled_jp / cheb_lower),
        "margin": qstr(margin),
        "normalizedPointDerivative": qstr((2 * kappas[1]) / alpha),
    }
    computed_time = {
        "maximumTerms": 2 * q_count,
        "turanExponent": 2 * q_count - 1,
        "sublevelMeasureLower": "2",
        "realPartBound": "4",
        "gapFactor": "0",
    }

    cos_sin = [phase_cos_sin(value) for value in phases]
    point_g = sum(amp * cs[0] for amp, cs in zip(amplitudes, cos_sin))
    point_gz = sum(amp * kappa * cs[1] for amp, kappa, cs in zip(amplitudes, kappas, cos_sin))
    point_gzz = -sum(
        amp * kappa * kappa * cs[0]
        for amp, kappa, cs in zip(amplitudes, kappas, cos_sin)
    )
    point_gs = sum(
        amp * (-rate * cs[0] - kappa * velocity * cs[1])
        for amp, kappa, rate, cs in zip(amplitudes, kappas, heat_rates, cos_sin)
    )
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
    energy_derivative = -Q(2) * i_velocity * symmetric_integral(poly_mul(xi, g_poly))
    xi_second = symmetric_integral(poly_mul(poly_derivative(xi, 2), g_squared))
    dissipation = symmetric_integral(xi)
    heat_cancellation = -xi_second / (i_a * i_a) + Q(2) * dissipation / (i_a * i_a)
    computed_identity = {
        "advectiveRow": qstr(advective),
        "energyDerivative": qstr(energy_derivative),
        "xiSecondRow": qstr(xi_second),
        "dissipationRow": qstr(dissipation),
        "heatCancellation": qstr(heat_cancellation),
    }

    after_mass = {"a": Q(2, 3), "R": Q(-1, 3), "M": Q(2, 3)}
    normalized = {"a": Q(2, 3), "R": Q(0), "omega": Q(1, 3), "p": Q(2, 3)}
    computed_scale = {
        "fluxPrefactor": encoded({"a": Q(2), "R": Q(3), "v": Q(1)}),
        "massPrefactor": encoded({"a": Q(2), "R": Q(5), "H": Q(1)}),
        "afterMass": encoded(after_mass),
        "normalized": encoded(normalized),
        "frozenRate": qstr(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{B\.(\d+)\}", text)]
    references = [int(value) for value in re.findall(r"\bB\.(\d+)\b", text)]
    display_opens = len(re.findall(r"(?m)^\\\[$", text))
    display_closes = len(re.findall(r"(?m)^\\\]$", text))
    assertions: list[dict[str, Any]] = []

    def record(name: str, group: str, ok: bool, details: Any = None) -> None:
        assertions.append({
            "name": name,
            "group": group,
            "pass": bool(ok) and MUTATION not in GROUPS[group],
            "details": details,
        })

    record(
        "frozen source bindings", "bindings",
        all(row["expectedSha256"] == row["observedSha256"] for row in bindings.values()),
        bindings,
    )
    record(
        "fixture and expected bindings", "inputs",
        sha256(FIXTURES) == FIXTURES_SHA256
        and sha256(EXPECTED) == EXPECTED_SHA256
        and fixtures["schema"].endswith("fixtures-v1")
        and expected["schema"].endswith("expected-v1"),
    )
    record(
        "UTF-8, controls, equation tags, displays, references, and TeX escapes", "integrity",
        clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
        and tags == list(range(1, 42))
        and display_opens == display_closes == 41
        and not (set(references) - set(tags))
        and r"\begin{aligned}" in text
        and r"-\frac2{11907}" in text,
        {"tags": len(tags), "opens": display_opens, "closes": display_closes},
    )
    record(
        "frozen primitive geometry", "geometry",
        0 < delta0 < delta and computed_geometry == expected["geometry"]
        and all_in(compact, [
            r"\Xi_a(z)=\int_{-\infty}^zW_a(r)",
            r"\|\Xi_a''\|_1\le Ca", "supported in `J`",
            r"4\pi\delta_0a^2R^5H",
        ]),
        computed_geometry,
    )
    record(
        "fixed-q dyadic high branch and inverse-radius endpoint", "family",
        computed_case == expected["scaledCase"]
        and all_in(compact, [
            "Fix an integer `q>=1`", r"n_1,\ldots,n_q\in\mathbb N",
            r"\phi_j\in\mathbb R", r"n_q\le2n_1", r"n_1R\le1",
            r"8q\le\alpha\le a", r"\kappa_q\le2\alpha",
        ]),
        computed_case,
    )
    record(
        "scaled variables, clock, heat rates, and PDE", "scaled",
        residual == 0 and velocity == 1 and max(heat_rates) <= 4
        and all_in(compact, [
            r"s=\frac t{R^2}", r"v=\frac{BR}{a}",
            r"\partial_sG+v\partial_zG-a^{-2}\partial_z^2G=0",
            r"0\le\kappa_j^2/a^2\le4",
        ]),
    )
    record(
        "carrier-scaled Turan--Nazarov value observation", "space_value",
        computed_space == expected["spatialObservation"]
        and all_in(compact, [
            r"r_j=\kappa_j/\alpha\in[1,2]", r"|E|\ge\frac\alpha2",
            "|alpha J^+|/|E|<=8", r"(8C)^{2q-1}",
            "No frequency separation enters the constant",
        ]),
        computed_space,
    )
    record(
        "compact unit-window derivative observation", "space_derivative",
        margin >= Q(windows["localHalfWidth"])
        and Q(computed_space["normalizedPointDerivative"]) == Q(289, 144)
        and all_in(compact, [
            r"\prod_{j=1}^m(\partial_x^2+r_j^2)f=0",
            "complete initial jet", "contradicting ODE uniqueness",
            "concentric double window", "g'=alpha f'(alpha z)",
            r"\alpha^{-1}\|G_z(s)\|",
        ]),
        {"margin": qstr(margin)},
    )
    record(
        "gap-free complete-clock terminal trace", "time_trace",
        computed_time == expected["temporalTrace"]
        and all_in(compact, [
            r"N_z\le2q", r"-\kappa_j^2/a^2\pm i\kappa_jv",
            "independent of `v` and of all gaps", r"h(4)\le C_qH",
        ]),
        computed_time,
    )
    record(
        "exact square transport identity and polynomial fixture", "identity",
        computed_identity == expected["transportIdentity"]
        and advective == energy_derivative and heat_cancellation == 0
        and all_in(compact, [
            r"=-2a^{-2}|G_z|^2", r"=E'(s)-a^{-2}\int\Xi_a''G^2",
            r"+2a^{-2}\int\Xi_a|G_z|^2", "Since `zeta(0)=0`",
        ]),
        computed_identity,
    )
    record(
        "exact endpoint-family point and PDE residual", "point",
        computed_point == expected["point"] and residual == 0
        and alpha == a_value and modes[0] * radius == 1,
        computed_point,
    )
    record(
        "complete real-field payment", "payment",
        all_in(compact, [
            r"\left(\frac\alpha a\right)^2h(s)^{2/3}",
            r"\le C_qH^{2/3}", "complete square `G^2`",
            "all cross-cluster products", "no localized-current sign",
        ])
        and all_in(compact_primary, [
            "terminal row is positive", "localized gradient row positive",
            "No row is dropped by sign", "standalone carrier-block method",
        ]),
    )
    record(
        "physical scale and normalization ledger", "scale",
        computed_scale == expected["scaleLedger"]
        and all_in(compact, [
            r"\frac{a^2R^3}{2}v", r"C_qa^{2/3}R^{-1/3}",
            r"R^{-2}\omega M", r"\frac\omega R", r"-\frac2{11907}",
        ]),
        computed_scale,
    )
    record(
        "primary-source, mathematical-audit, and no-figure boundary", "source_audit",
        all_in(compact_source, [
            "https://www.mathnet.ru/eng/aa397", "https://arxiv.org/abs/1107.0039",
            "https://arxiv.org/abs/1602.02315", "https://doi.org/10.1006/jath.2001.3576",
            "https://arxiv.org/abs/2311.17714", "proves that statement directly",
            "not evidence of novelty or priority",
        ])
        and all_in(compact_primary, [
            "Current verdict: **PASS**", "Mathematical blocker count: **0**",
            "Release blocker count: **0**", "not represented as proof",
            "No formal figure is required",
        ]),
    )
    record(
        "exact theorem and open-claim boundary", "boundary",
        all_in(compact, [
            "R0.75X with `C_0=8q`", "under the full condition B.4",
            "entire exact-shear carrier range", "ultra-high sector `n_1R>1`",
            "constant uniform in growing `q`", "arbitrary growing packets",
            "The proof above restores the full real field", "R0.76A",
            "Version-M measurement row", "regularity", "singularity", "**NOT CLAY.**",
        ]),
    )

    verdict = "PASS" if all(item["pass"] for item in assertions) else "FAIL"
    certificate = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": assertions,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "bindings": bindings,
        "computed": {
            "geometry": computed_geometry,
            "scaledCase": computed_case,
            "spatialObservation": computed_space,
            "temporalTrace": computed_time,
            "point": computed_point,
            "transportIdentity": computed_identity,
            "scaleLedger": computed_scale,
        },
        "boundary": {
            "fixedQInverseRadiusPayment": "PROVED",
            "analyticDensitySubblock": "NOT_USED",
            "standaloneCarrierSpatialIntegrationByParts": "REJECTED",
            "ultraHighCarrier": "OPEN",
            "growingModeCount": "OPEN",
            "arbitraryPackets": "OPEN",
            "versionMTransfer": "CONDITIONAL_ONLY",
            "regularity": "OPEN",
            "singularity": "OPEN",
            "clayProblemSolved": False,
        },
        "mutation": MUTATION or None,
    }
    OUT_JSON.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    passed = sum(item["pass"] for item in assertions)
    report = [
        "# R0.76B exact finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{len(assertions)}",
        f"- Mutation challenge: {MUTATION or 'none'}",
        f"- Blocker count: {0 if verdict == 'PASS' else 1}",
        "",
        "The certificate recomputes one exact q=3 high-branch endpoint family,",
        "spatial-window geometry, temporal real-part bounds, a polynomial energy",
        "identity, and the physical/normalized scale ledger using exact rational",
        "arithmetic.  It does not certify the continuum observation theorems.",
        "",
        "The proved scope is fixed q with n_1 R <= 1.  Ultra-high carriers,",
        "growing packets, Version-M transfer, regularity, and singularity remain",
        "OPEN. **NOT CLAY.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"suite": SCHEMA, "verdict": verdict, "assertions": len(assertions), "mutation": MUTATION}))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
