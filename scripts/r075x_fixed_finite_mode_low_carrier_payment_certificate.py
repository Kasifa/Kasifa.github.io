#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75X."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075x_fixed_finite_mode_low_carrier_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075x_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075X_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075X_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075X_MUTATION", "")
SCHEMA = "r075x-fixed-finite-mode-low-carrier-payment-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763",
    f"research/{STEM}_primary_audit.md":
        "8fffbf0c8ad50d5765c734f8e5627ce0dbe0d6b2aad4bcb26aa5c298f6143b2c",
    "research/r075x_report-source.md":
        "8fa756c7efe2660dbc5eeb51e2a11d10dce58f36f4c0d0f757000be1447b7f34",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075w_full_frequency_two_harmonic_flux_payment.md":
        "571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4",
}
FIXTURES_SHA256 = "de231e977d9a2551222f0a4f0a8ebcb65490f76574bc4fa494db480e2b61a0e9"
EXPECTED_SHA256 = "879ff3458050e712048654eb91623a00e5436a22f12c6b814fb137aa8af96311"

GROUPS = {
    "bindings": ("main_hash", "primary_hash", "source_hash", "b_hash", "r_hash", "w_hash"),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references"),
    "clock": ("clock_length", "cutoff_onset", "cutoff_derivative"),
    "family": ("fixed_q", "ordered_modes", "dyadic_band", "low_carrier", "scaled_upper"),
    "scaled": ("ell", "alphas", "velocity", "heat_rates", "scaled_pde"),
    "ode": ("ode_order", "symmetric_coefficients", "last_row", "compact_family",
            "initial_jet", "confluent_degree", "gap_free_space"),
    "trace": ("term_count", "real_parts", "imaginary_free", "gap_free_time",
              "turan_power", "sublevel_measure", "endpoint_trace"),
    "kernel": ("kernel_odd", "kernel_zero", "primitive_support", "kernel_norms",
               "primitive_second", "cross_section"),
    "identity": ("square_pde", "advective_row", "energy_derivative", "xi_second",
                 "dissipation", "heat_cancel", "identity_signs"),
    "payment": ("spatial_application", "holder_time", "terminal_payment",
                "dimensionless_payment"),
    "mass": ("fibre_area", "mass_a", "mass_r", "flux_prefactor", "target_a",
             "target_r", "target_m"),
    "normalization": ("p_definition", "x_definition", "r_cancel", "omega_power",
                      "frozen_rate"),
    "q_boundary": ("temporal_growth", "spatial_nonquantitative", "fixed_q_only",
                   "r_obstruction"),
    "source": ("nazarov_original", "primary_restatement", "bounded_search"),
    "audit": ("audit_pass", "math_zero", "release_zero", "finite_boundary"),
    "figure": ("analytic_only", "no_simulation_claim", "no_formal_figure"),
    "boundary": ("low_only", "high_three_open", "packets_open", "e24_open",
                 "version_m_conditional", "not_clay"),
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


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def encoded(powers: dict[str, Q]) -> dict[str, str | int]:
    return {
        key: int(value) if value.denominator == 1 else str(value)
        for key, value in powers.items()
    }


def poly_mul(left: list[Q], right: list[Q]) -> list[Q]:
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, x_value in enumerate(left):
        for j, y_value in enumerate(right):
            out[i + j] += x_value * y_value
    return out


def poly_derivative(poly: list[Q], order: int = 1) -> list[Q]:
    out = list(poly)
    for _ in range(order):
        out = [Q(index) * out[index] for index in range(1, len(out))]
    return out


def symmetric_integral(poly: list[Q]) -> Q:
    return sum(
        (Q(2) * value / Q(index + 1) if index % 2 == 0 else Q(0))
        for index, value in enumerate(poly)
    )


def add_powers(left: dict[str, Q], right: dict[str, Q]) -> dict[str, Q]:
    return {key: left.get(key, Q(0)) + right.get(key, Q(0)) for key in set(left) | set(right)}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075X_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75X suite")

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
        "source_hash": "research/r075x_report-source.md",
        "b_hash": "research/r075b_bulk_clock_outer_padding_gate.md",
        "r_hash": "research/r075r_outer_cap_spectral_concentration_obstruction.md",
        "w_hash": "research/r075w_full_frequency_two_harmonic_flux_payment.md",
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

    case = fixtures["scaledCase"]
    q_count = int(case["q"])
    modes = [Q(value) for value in case["frequencies"]]
    a_value = Q(case["a"])
    radius = Q(case["R"])
    b_shear = Q(case["B"])
    c_zero = Q(case["C0"])
    ell = a_value * radius
    alphas = [mode * ell for mode in modes]
    velocity = b_shear * radius / a_value
    heat_rates = [alpha * alpha / (a_value * a_value) for alpha in alphas]
    computed_scaled = {
        "ell": qtext(ell),
        "alphas": [qtext(value) for value in alphas],
        "v": qtext(velocity),
        "heatRates": [qtext(value) for value in heat_rates],
        "lowCarrier": bool(modes[0] * ell < c_zero),
        "dyadicBand": bool(modes[-1] <= 2 * modes[0]),
    }

    squares = [alpha * alpha for alpha in alphas]
    sigmas = [
        sum((prod for combination in itertools.combinations(squares, degree)
             for prod in [__import__("functools").reduce(lambda x, y: x * y, combination, Q(1))]), Q(0))
        for degree in range(1, q_count + 1)
    ]
    last_row: list[Q] = []
    for sigma in reversed(sigmas):
        last_row.extend([-sigma, Q(0)])
    computed_ode = {
        "q": q_count,
        "order": 2 * q_count,
        "sigma": [qtext(value) for value in sigmas],
        "lastRow": [qtext(value) for value in last_row],
        "fullyConfluentDegree": 2 * q_count - 1,
    }
    computed_trace = {
        "maximumTerms": 2 * q_count,
        "turanExponent": 2 * q_count - 1,
        "sublevelMeasureLower": 2,
        "gapFactor": 0,
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
        "advectiveRow": qtext(advective),
        "energyDerivative": qtext(energy_derivative),
        "xiSecondRow": qtext(xi_second),
        "dissipationRow": qtext(dissipation),
        "heatCancellation": qtext(heat_cancellation),
    }

    flux_prefactor = {"a": Q(2), "R": Q(3), "v": Q(1)}
    mass_prefactor = {"a": Q(2), "R": Q(5), "H": Q(1)}
    after_mass = add_powers(
        {"a": Q(2), "R": Q(3), "H": Q(2, 3)},
        {"a": Q(-4, 3), "R": Q(-10, 3), "H": Q(-2, 3), "M": Q(2, 3)},
    )
    normalized = add_powers(after_mass, {"omega": Q(1), "R": Q(-1)})
    normalized = add_powers(
        normalized,
        {"R": Q(4, 3), "omega": Q(-2, 3), "p": Q(2, 3), "M": Q(-2, 3)},
    )
    computed_scale = {
        "fluxPrefactor": encoded(flux_prefactor),
        "massPrefactor": encoded(mass_prefactor),
        "afterMass": encoded({key: value for key, value in after_mass.items() if value}),
        "normalized": encoded({key: normalized.get(key, Q(0)) for key in ("a", "R", "omega", "p")}),
        "frozenRate": qtext(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{X\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"\bX\.(\d+)\b", text)]
    assertions: list[dict[str, Any]] = []

    def record(name: str, group: str, ok: bool, details: Any = None) -> None:
        assertions.append({"name": name, "pass": bool(ok and MUTATION not in GROUPS[group]), "details": details})

    record("frozen source bindings", "bindings",
           all(row["expectedSha256"] == row["observedSha256"] for row in bindings.values()), bindings)
    record("fixture and expected bindings", "inputs",
           sha256(FIXTURES) == FIXTURES_SHA256 and sha256(EXPECTED) == EXPECTED_SHA256
           and fixtures["schema"].endswith("fixtures-v1"))
    record("UTF-8, controls, tags, displays, and references", "integrity",
           clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
           and tags == list(range(1, 37)) and text.count("\\[") == text.count("\\]") == 36
           and not (set(refs) - set(tags)),
           {"tags": len(tags), "displays": text.count("\\["), "unresolved": sorted(set(refs) - set(tags))})
    record("complete clock and cutoff", "clock",
           computed_clock == expected["clock"]
           and all_in(compact, ["4R^2", "\\eta_R(0)=0", "C_\\eta R^{-2}"]), computed_clock)
    record("fixed finite dyadic low-carrier family", "family",
           computed_scaled["lowCarrier"] and computed_scaled["dyadicBand"]
           and all_in(compact, ["Fix an integer `q>=1`", "n_q\\le2n_1", "n_1aR<C_0",
                                "0<\\alpha_1<\\cdots<\\alpha_q\\le2C_0"]))
    record("scaled variables and heat rates", "scaled",
           computed_scaled == expected["scaledCase"]
           and all_in(compact, ["v=\\frac{BR}{a}",
                                "\\partial_sG+v\\partial_zG-a^{-2}\\partial_z^2G=0"]), computed_scaled)
    record("2q-order confluent spatial ODE", "ode",
           computed_ode == expected["spatialOde"]
           and all_in(compact, ["\\prod_{j=1}^q(\\partial_z^2+\\alpha_j^2)g=0",
                                "(-\\sigma_q,0,-\\sigma_{q-1},0,\\ldots,-\\sigma_1,0)",
                                "degree at most `2q-1`", "unit initial jet", "No inverse frequency gap"]),
           computed_ode)
    record("gap-free 2q-term temporal trace", "trace",
           computed_trace == expected["temporalTrace"]
           and all_in(compact, ["N\\le2q", "independent of the imaginary parts",
                                "has measure at least two", "h(4)\\le C_qH",
                                "-\\alpha_j^2/a^2\\pm i\\alpha_jv"]), computed_trace)
    record("scaled radial primitive", "kernel",
           all_in(compact, ["W_a(z)=-2\\pi az", "Oddness gives `int W_a=0`",
                            "\\Xi_a(z)=\\int_{-\\infty}^zW_a(r)", "\\|\\Xi_a''\\|_1\\le Ca",
                            "\\frac{a^2R^3}{2}v"]))
    record("transport identity exact finite fixture", "identity",
           computed_identity == expected["transportIdentity"]
           and advective == energy_derivative and heat_cancellation == 0
           and all_in(compact, ["=-2a^{-2}|\\partial_zG|^2", "=E'(s)-a^{-2}\\int\\Xi_a''G^2",
                                "+2a^{-2}\\int\\Xi_a|\\partial_zG|^2"]), computed_identity)
    record("identity signs and complete payment", "payment",
           all_in(compact_primary, ["terminal row is positive", "cutoff derivative row negative",
                                    "`Xi_a''` row negative", "localized gradient row positive"])
           and all_in(compact, ["|E(4)|\\le C_qh(4)^{2/3}\\le C_qH^{2/3}",
                                "\\le C_qH^{2/3}", "never divides by `v`"]))
    record("physical mass substitution and target powers", "mass",
           computed_scale["fluxPrefactor"] == expected["scaleLedger"]["fluxPrefactor"]
           and computed_scale["massPrefactor"] == expected["scaleLedger"]["massPrefactor"]
           and computed_scale["afterMass"] == expected["scaleLedger"]["afterMass"]
           and all_in(compact, ["4\\pi\\delta_0a^2R^5H", "C_qa^{2/3}R^{-1/3}"]), computed_scale)
    record("normalization and frozen rate", "normalization",
           computed_scale["normalized"] == expected["scaleLedger"]["normalized"]
           and computed_scale["frozenRate"] == expected["scaleLedger"]["frozenRate"]
           and all_in(compact, ["R^{-2}\\omega M", "\\frac\\omega R", "-\\frac2{11907}"]),
           computed_scale)
    record("explicit fixed-q boundary", "q_boundary",
           all_in(compact, ["grows at most exponentially in `q`", "no quantitative uniform bound in `q`",
                            "fixed-finite-dimensional theorem", "outer-cap construction of R0.75R"]))
    record("bounded primary-source boundary", "source",
           all_in(compact_source, ["Nazarov", "https://www.mathnet.ru/eng/aa397",
                                   "https://arxiv.org/abs/1107.0039", "no completeness, novelty, or priority claim"]))
    record("primary audit verdict and finite boundary", "audit",
           all_in(compact_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**",
                                    "Release blocker count: **0**", "not represented as proof"]))
    record("analytic no-figure gate", "figure",
           all_in(compact, ["proof is analytic", "no formal scientific figure or simulation is claimed"])
           and all_in(compact_primary, ["No formal figure is required", "no simulation result enters the claim"]))
    record("fixed-subfamily claim boundary", "boundary",
           all_in(compact, ["high-carrier sector for three or more modes", "arbitrary dyadic packets",
                            "arbitrary-field E.24", "Version-M measurement row", "**NOT CLAY.**"]))

    verdict = "PASS" if all(row["pass"] for row in assertions) else "FAIL"
    output = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": assertions,
        "assertionCount": len(assertions),
        "bindings": bindings,
        "clock": computed_clock,
        "scaledCase": computed_scaled,
        "spatialOde": computed_ode,
        "temporalTrace": computed_trace,
        "transportIdentity": computed_identity,
        "scaleLedger": computed_scale,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    passed = sum(1 for row in assertions if row["pass"])
    OUT_REPORT.write_text(
        "\n".join([
            "# R0.75X finite certificate report", "",
            f"- Verdict: **{verdict}**",
            f"- Assertions: {passed}/{len(assertions)}",
            "- Exact transport-identity fixture: 1/1", "",
            "The finite suite certifies the q=3 companion coefficients, scaled",
            "variables, term count, transport-identity signs, exact power arithmetic,",
            "source bindings, and claim boundaries. It does not numerically certify",
            "the continuum fixed-q compactness lemma or the Turan--Nazarov theorem.",
            "The theorem is low-carrier and fixed-finite-dimensional. **NOT CLAY.**", "",
        ]),
        encoding="utf-8",
    )
    print(json.dumps({"suite": "r075x-python", "verdict": verdict, "assertions": len(assertions)}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
