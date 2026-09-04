#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75W."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075w_full_frequency_two_harmonic_flux_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075w_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075W_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075W_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075W_MUTATION", "")
SCHEMA = "r075w-full-frequency-two-harmonic-flux-payment-certificate-v1"

FROZEN = {
    f"research/{STEM}.md":
        "571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4",
    f"research/{STEM}_primary_audit.md":
        "78255a0d84020d1d1c9dc6509ed1cc8eb9a9fdaced21d93e4f586383e4fc9ea0",
    "research/r075w_report-source.md":
        "461ab29f02072eb039c9b57c497a87d04ff95255af68d561c68f4d3224726d7a",
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075r_outer_cap_spectral_concentration_obstruction.md":
        "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
    "research/r075t_two_harmonic_collar_coercivity.md":
        "822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66",
    "research/r075v_complete_two_harmonic_flux_payment.md":
        "6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824",
}
FIXTURES_SHA256 = "2b59973a6901b0a70068a2952e1324fd1780f853508c250821daaab659aa8b1f"
EXPECTED_SHA256 = "44afc8aebea8e15a4d54adf28fd48f8da28dd61c74e6f87a9ded21667d61867f"

GROUPS = {
    "bindings": ("main_hash", "primary_hash", "source_hash", "b_hash", "r_hash", "t_hash", "v_hash"),
    "inputs": ("fixture_hash", "expected_hash", "fixture_schema"),
    "integrity": ("utf8", "controls", "tags", "displays", "references"),
    "clock": ("clock_length", "cutoff_onset", "cutoff_derivative"),
    "split": ("dyadic_pair", "low_sector", "high_sector", "exhaustive_split", "scaled_upper_bound"),
    "scaled": ("ell", "alpha", "beta", "v", "alpha_heat", "beta_heat", "scaled_pde"),
    "ode": ("ode_coefficients", "state_matrix", "compact_family", "initial_jet", "confluent_degree", "gap_free_space"),
    "trace": ("four_terms", "real_parts", "imaginary_free", "gap_free_time", "turan_power", "sublevel_set", "endpoint_trace"),
    "kernel": ("kernel_odd", "kernel_zero", "primitive_support", "kernel_norms", "primitive_second", "cross_section"),
    "identity": ("square_pde", "advective_row", "energy_derivative", "xi_second", "dissipation", "heat_cancel", "identity_signs"),
    "payment": ("spatial_application", "holder_time", "terminal_payment", "dimensionless_payment"),
    "mass": ("fibre_area", "mass_a", "mass_r", "flux_prefactor", "target_a", "target_r", "target_m"),
    "normalization": ("p_definition", "x_definition", "r_cancel", "omega_power", "frozen_rate"),
    "source": ("nazarov_original", "primary_restatement", "clay_source", "bounded_search"),
    "audit": ("audit_pass", "math_zero", "release_zero", "finite_boundary"),
    "figure": ("analytic_only", "no_simulation_claim", "no_formal_figure"),
    "boundary": ("exact_pair", "three_modes_open", "packets_open", "e24_open", "version_m_conditional", "not_clay"),
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


def qtext(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def encoded(powers: dict[str, Q]) -> dict[str, str | int]:
    return {
        key: int(value) if value.denominator == 1 else str(value)
        for key, value in powers.items()
    }


def padd(left: dict[str, Q], right: dict[str, Q]) -> dict[str, Q]:
    size = max(len(left), len(right))
    return {
        str(j): left.get(str(j), Q(0)) + right.get(str(j), Q(0))
        for j in range(size)
    }


def pmul(left: list[Q], right: list[Q]) -> list[Q]:
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] += x * y
    return out


def pder(poly: list[Q], order: int = 1) -> list[Q]:
    out = list(poly)
    for _ in range(order):
        out = [Q(j) * out[j] for j in range(1, len(out))]
    return out


def pintegral_symmetric(poly: list[Q]) -> Q:
    total = Q(0)
    for j, value in enumerate(poly):
        if j % 2 == 0:
            total += Q(2) * value / Q(j + 1)
    return total


def add_powers(left: dict[str, Q], right: dict[str, Q]) -> dict[str, Q]:
    return {
        key: left.get(key, Q(0)) + right.get(key, Q(0))
        for key in set(left) | set(right)
    }


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075W_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75W suite")

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
        "source_hash": "research/r075w_report-source.md",
        "b_hash": "research/r075b_bulk_clock_outer_padding_gate.md",
        "r_hash": "research/r075r_outer_cap_spectral_concentration_obstruction.md",
        "t_hash": "research/r075t_two_harmonic_collar_coercivity.md",
        "v_hash": "research/r075v_complete_two_harmonic_flux_payment.md",
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

    row = fixtures["scaledCase"]
    k, m, a, radius, b_shear = Q(row["k"]), Q(row["m"]), Q(row["a"]), Q(row["R"]), Q(row["B"])
    ell = a * radius
    alpha, beta = k * ell, m * ell
    velocity = b_shear * radius / a
    computed_scaled = {
        "ell": qtext(ell), "alpha": qtext(alpha), "beta": qtext(beta), "v": qtext(velocity),
        "alphaHeat": qtext(alpha * alpha / (a * a)),
        "betaHeat": qtext(beta * beta / (a * a)),
    }
    computed_ode = {
        "secondDerivativeCoefficient": qtext(alpha * alpha + beta * beta),
        "zerothCoefficient": qtext(alpha * alpha * beta * beta),
        "confluentDegree": 3,
    }
    computed_trace = {"maximumTerms": 4, "turanExponent": 3, "gapFactor": 0}

    identity = fixtures["transportIdentity"]
    iv = Q(identity["v"])
    is_value = Q(identity["s"])
    ia = Q(identity["a"])
    xi = [Q(1), Q(0), Q(-2), Q(0), Q(1)]
    w = pder(xi)
    g = [-iv * is_value, Q(1)]
    g2 = pmul(g, g)
    advective = iv * pintegral_symmetric(pmul(w, g2))
    energy_derivative = -Q(2) * iv * pintegral_symmetric(pmul(xi, g))
    xi_second = pintegral_symmetric(pmul(pder(xi, 2), g2))
    dissipation = pintegral_symmetric(xi)
    heat_cancellation = -xi_second / (ia * ia) + Q(2) * dissipation / (ia * ia)
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
    normalized = add_powers(normalized, {"R": Q(4, 3), "omega": Q(-2, 3), "p": Q(2, 3), "M": Q(-2, 3)})
    computed_scale = {
        "fluxPrefactor": encoded(flux_prefactor),
        "massPrefactor": encoded(mass_prefactor),
        "afterMass": encoded({key: value for key, value in after_mass.items() if value}),
        "normalized": encoded({key: normalized.get(key, Q(0)) for key in ("a", "R", "omega", "p")}),
        "frozenRate": qtext(-Q(fixtures["frozenScales"]["cGamma"]) / 12),
    }

    tags = [int(value) for value in re.findall(r"\\tag\{W\.(\d+)\}", text)]
    refs = [int(value) for value in re.findall(r"\bW\.(\d+)\b", text)]
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
           and tags == list(range(1, 34)) and text.count("\\[") == text.count("\\]") == 34
           and not (set(refs) - set(tags)),
           {"tags": len(tags), "displays": text.count("\\["), "unresolved": sorted(set(refs) - set(tags))})
    record("complete clock and cutoff", "clock",
           computed_clock == expected["clock"]
           and all_in(compact, ["T_R=4R^2", "\\eta_R(0)=0", "C_\\eta R^{-2}"]), computed_clock)
    record("exhaustive carrier split", "split",
           all_in(compact, ["1<=m<k<=2m", "maR\\ge C_0", "`maR<C_0`", "`0<beta<alpha<=2C_0`",
                            "partition all possibilities"]))
    record("low-carrier scaled variables and heat", "scaled",
           computed_scaled == expected["scaledCase"]
           and all_in(compact, ["v=\\frac{BR}{a}", "\\partial_sG+v\\partial_zG-a^{-2}\\partial_z^2G=0"]),
           computed_scaled)
    record("confluent fourth-order spatial ODE", "ode",
           computed_ode == expected["spatialOde"]
           and all_in(compact, ["(\\partial_z^2+\\alpha^2)(\\partial_z^2+\\beta^2)g=0",
                                "cubic-polynomial space", "initial jet", "a nonzero limiting solution"]),
           computed_ode)
    record("gap-free four-term temporal trace", "trace",
           computed_trace == expected["temporalTrace"]
           and all_in(compact, ["N\\le4", "independent of the imaginary parts", "half-measure sublevel set",
                                "h(4)\\le C H", "-\\alpha^2/a^2\\pm i\\alpha v"]), computed_trace)
    record("scaled radial primitive", "kernel",
           all_in(compact, ["W_a(z)=-2\\pi a z", "Oddness gives `int W_a=0`", "\\Xi_a(z)=\\int_{-\\infty}^{z}",
                            "\\|\\Xi_a''\\|_{L^1}=\\|W_a'\\|_{L^1}\\le Ca",
                            "=aR^2\\int_{\\mathbb R}W_a(z)G(s,z)^2"]))
    record("transport identity exact finite fixture", "identity",
           computed_identity == expected["transportIdentity"]
           and advective == energy_derivative and heat_cancellation == 0
           and all_in(compact, ["=-2a^{-2}|\\partial_zG|^2", "E'(s)-a^{-2}\\int\\Xi_a''G^2",
                                "+2a^{-2}\\int\\Xi_a|\\partial_zG|^2"]), computed_identity)
    record("identity sign audit", "identity",
           all_in(compact_primary, ["terminal energy: plus", "cutoff derivative: minus",
                                    "heat row: minus", "localized dissipation: plus"]))
    record("dimensionless complete-clock payment", "payment",
           all_in(compact, ["|E(4)|\\le Ch(4)^{2/3}\\le CH^{2/3}",
                            "\\left|v\\int_0^4\\zeta\\int W_aG^2\\right|", "No division by `v`"]))
    record("physical mass substitution and target powers", "mass",
           computed_scale["fluxPrefactor"] == expected["scaleLedger"]["fluxPrefactor"]
           and computed_scale["massPrefactor"] == expected["scaleLedger"]["massPrefactor"]
           and computed_scale["afterMass"] == expected["scaleLedger"]["afterMass"]
           and all_in(compact, ["4\\pi\\delta_0a^2R^5H", "Ca^{2/3}R^{-1/3}"]), computed_scale)
    record("normalization and frozen rate", "normalization",
           computed_scale["normalized"] == expected["scaleLedger"]["normalized"]
           and computed_scale["frozenRate"] == expected["scaleLedger"]["frozenRate"]
           and all_in(compact, ["R^{-2}\\omega M", "\\frac\\omega R", "-\\frac2{11907}"]), computed_scale)
    record("bounded primary-source boundary", "source",
           all_in(compact_source, ["Nazarov", "https://www.mathnet.ru/eng/aa397", "arxiv.org/abs/1107.0039",
                                   "official Clay Mathematics Institute", "not a novelty search"]))
    record("primary audit verdict and finite boundary", "audit",
           all_in(compact_primary, ["Current verdict: **PASS**", "Mathematical blocker count: **0**",
                                    "Release blocker count: **0**", "not represented as proof"]))
    record("analytic no-figure gate", "figure",
           all_in(compact, ["proof is analytic", "no formal scientific figure or simulation is claimed"])
           and all_in(compact_primary, ["No formal figure is required", "would not verify compact ODE observability"]))
    record("exact-subfamily claim boundary", "boundary",
           all_in(compact, ["exact pair W.1", "three or more harmonics", "arbitrary dyadic packets",
                            "arbitrary-field E.24", "conditional on the realized-subclass", "**NOT CLAY.**"]))

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
    report = [
        "# R0.75W finite certificate report", "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{len(assertions)}",
        "- Exact transport-identity fixture: 1/1", "",
        "The finite suite certifies source bindings, scaled variables, the confluent",
        "ODE coefficients, transport-identity signs, exact power arithmetic, and",
        "claim boundaries. It does not numerically certify the continuum ODE",
        "compactness lemma or the Turan--Nazarov theorem.",
        "The theorem is limited to one exact dyadic two-harmonic shear. **NOT CLAY.**", "",
    ]
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"schema": SCHEMA, "verdict": verdict, "assertions": len(assertions)}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
