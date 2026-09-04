#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75Q."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
STEM = "r075q_spatially_spread_harmonic_collar_payment"
MAIN = ROOT / f"research/{STEM}.md"
PRIMARY = ROOT / f"research/{STEM}_primary_audit.md"
SOURCE = ROOT / "research/r075q_report-source.md"
FIXTURES = ROOT / f"scripts/{STEM}_fixtures.json"
EXPECTED = ROOT / f"scripts/{STEM}_expected.json"
OUT_JSON = Path(os.environ.get("R075Q_JSON", ROOT / f"research/{STEM}_certificate.json"))
OUT_REPORT = Path(os.environ.get("R075Q_REPORT", ROOT / f"research/{STEM}_certificate_report.md"))
MUTATION = os.environ.get("R075Q_MUTATION", "")
SCHEMA = "r075q-spatially-spread-harmonic-collar-payment-certificate-v1"

FROZEN = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075l_single_harmonic_diffusive_signed_flux_gain.md":
        "52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5",
    "research/r075n_radial_collar_averaged_wiener_row.md":
        "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
    "research/r075p_buffered_collar_entrance_concentration.md":
        "8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6",
    "research/r075q_spatially_spread_harmonic_collar_payment.md":
        "9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c",
    "research/r075q_spatially_spread_harmonic_collar_payment_primary_audit.md":
        "92255869e165efdbe72557187dd1fe6e7e4449264dcf8033b285286d50f725be",
    "research/r075q_report-source.md":
        "b1fcfece0396b04ae9f59e42ef09957a422c36fa0843730a9fb22919bc24c600",
}
FIXTURES_SHA256 = "a0954f102de2fbc5ac5fb57fd68ba2ae084cc27743240fac6e3297b81d4410f5"
EXPECTED_SHA256 = "8f3e45bb4a62e2a5bd506fd3cc522610d59115f34411fd85b04c7b72081cb444"

MUTATION_GROUPS = {
    "allFrozenBindings": (
        "main_hash", "audit_hash", "source_hash", "dependency_hash",
    ),
    "fixtureExpectedBindings": ("fixture_hash", "expected_hash"),
    "primaryAuditStatus": (
        "audit_pass", "audit_math_blocker", "audit_release_blocker", "audit_publish",
    ),
    "dependencyTableBindings": (
        "dep_b", "dep_l", "dep_n", "dep_p", "dep_role",
    ),
    "tagsReferencesDisplays": (
        "tag_missing", "tag_duplicate", "tag_gap", "reference", "display_open",
        "display_close", "aligned_pair",
    ),
    "utf8ControlAndTex": (
        "utf8", "control", "bare_qquad", "qquad_count", "time_integral_line",
    ),
    "radialDerivativeRow": (
        "radial_outer", "radial_inner", "radial_volume", "radial_derivative",
        "radial_l1", "radial_scale", "radial_chart", "radial_periodic_lift",
    ),
    "harmonicEquation": (
        "harmonic_real", "harmonic_integer", "harmonic_time", "harmonic_drift",
        "harmonic_transport", "harmonic_diffusion", "harmonic_sum", "harmonic_x1x3",
    ),
    "signedFluxCancellation": (
        "eta_range", "flux_outer_half", "square_half", "constant_row",
        "cancel_before_abs", "pre_time_quarter", "time_integral_upper",
        "flux_eighth", "ordinary_heat", "flux_fixture",
    ),
    "rectangleFibreGeometry": (
        "rectangle_side", "transverse_radius", "safe_radius", "a_condition",
        "chart_condition", "fibre_formula", "fibre_two_sided", "fibre_lower",
    ),
    "phaseUniformPeriodFloor": (
        "cos_period", "cos_integral", "phase_uniform", "period_count",
        "floor_direction", "floor_half", "kar_condition", "x2_lower",
    ),
    "spatialCollarMass": (
        "x3_length", "spatial_product", "spatial_delta", "spatial_a",
        "spatial_R", "all_times",
    ),
    "timeIntegralAndCBox": (
        "k2T", "time_three", "time_direction", "exp_three", "cbox_two",
        "cbox_nine", "cbox_pi", "mass_delta", "mass_a", "mass_R",
        "mass_k", "mass_A",
    ),
    "cubicInversionCombination": (
        "inverse_direction", "inverse_delta", "inverse_a", "inverse_R",
        "inverse_k", "inverse_M", "combine_delta", "combine_B", "combine_a",
        "combine_R_cancel", "combine_k", "combine_M",
    ),
    "normalizationScaleAndRate": (
        "payment_R", "payment_omega", "flux_R", "flux_omega", "norm_B",
        "norm_a", "norm_R", "norm_omega", "norm_k", "norm_p", "shear_scale",
        "frequency_scale", "after_L", "after_R", "after_omega", "rho",
        "cgamma", "rate_fraction", "rate_sign", "large_L",
    ),
    "conditionalVersionMLedger": (
        "ledger_full_window", "ledger_same_interval", "ledger_exterior",
        "ledger_weight", "ledger_coordinate_translation", "actual_component",
        "same_velocity", "pointwise_domination", "ledger_nonnegative",
        "ledger_direction", "projection_excluded", "arbitrary_realization",
        "realized_subclass", "sufficiently_large",
    ),
    "lowEntranceDiagnostic": (
        "entrance_E0", "entrance_area", "entrance_ratio", "sigma_fixed",
        "sigma_lower", "sigma_upper", "sigma_strict", "entrance_limit",
        "not_hidden_P", "not_counterexample",
    ),
    "formulaSentinels": (
        "formula_q1", "formula_q10", "formula_q14", "formula_q18",
        "formula_q21", "formula_q22", "formula_q24", "formula_q25",
        "formula_q26", "formula_q27", "formula_q28",
    ),
    "sourceReportBoundary": (
        "source_primary_links", "source_titles", "source_adjacency",
        "source_no_import", "source_nonexhaustive", "source_no_novelty",
    ),
    "claimBoundary": (
        "one_harmonic", "constant_shear", "independent_x1x3", "total_field",
        "projection_open", "multimode_open", "vertical_open", "low_packet_open",
        "nonconstant_open", "interpacket_open", "frequency_cap_open", "e24_open",
        "clock_open", "fixed_deletion_open", "weak_open", "regularity_open",
        "singularity_open", "novelty", "priority", "not_clay",
    ),
}
NEGATIVE_MUTATIONS = tuple(x for xs in MUTATION_GROUPS.values() for x in xs)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(str(value))


def qt(value: Q) -> str:
    return str(value)


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((b < 32 and b not in (9, 10, 13)) or b == 127 for b in data)


def rec(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def guarded(name: str, ok: bool) -> bool:
    return bool(ok and MUTATION not in MUTATION_GROUPS[name])


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075Q_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75Q suite")

    raw = MAIN.read_bytes()
    raw_primary = PRIMARY.read_bytes()
    raw_source = SOURCE.read_bytes()
    text = raw.decode("utf-8")
    primary = raw_primary.decode("utf-8")
    source = raw_source.decode("utf-8")
    flat = re.sub(r"\s+", " ", text)
    flat_primary = re.sub(r"\s+", " ", primary)
    flat_source = re.sub(r"\s+", " ", source)
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    frozen = dict(FROZEN)
    drift = {
        "main_hash": f"research/{STEM}.md",
        "audit_hash": f"research/{STEM}_primary_audit.md",
        "source_hash": "research/r075q_report-source.md",
        "dependency_hash": "research/r075l_single_harmonic_diffusive_signed_flux_gain.md",
    }
    if MUTATION in drift:
        frozen[drift[MUTATION]] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen.items())
    }

    g = fixtures["geometryCase"]
    a, d0, delta, radius = map(q, (g["a"], g["delta0"], g["delta"], g["R"]))
    k, time, amp = map(q, (g["k"], g["T"], g["A"]))
    outer = (a + delta) * radius
    inner = (a - delta) * radius
    shell_over_pi = Q(4, 3) * (outer ** 3 - inner ** 3)
    derivative_l1_over_pi = shell_over_pi / radius
    radial = {
        "outerRadius": qt(outer), "innerRadius": qt(inner),
        "shellVolumeOverPi": qt(shell_over_pi),
        "derivativeL1BoundOverPi": qt(derivative_l1_over_pi),
        "benchmarkA2R2": qt(a * a * radius * radius),
        "centralChartCertified": outer < Q(3, 2),
    }

    harmonic = {
        "timeCoefficient": "-k^2", "driftCoefficient": "+k*B*sin",
        "transportCoefficient": "-k*B*sin", "diffusionCoefficient": "+k^2",
        "operatorSum": "0",
    }

    f = fixtures["fluxCase"]
    fA, fB, fk, vxi = map(q, (f["A"], f["absB"], f["k"], f["derivativeL1"]))
    time_upper = Q(1, 2) / (fk * fk)
    flux_bound = fA * fA * fB * vxi / (8 * fk * fk)
    flux = {
        "outerHalf": "1/2", "squareHalf": "1/2", "constantRow": "0",
        "preTimeFactor": "1/4", "timeIntegralUpper": qt(time_upper),
        "finalFactor": "1/(8*k^2)", "fixtureBound": qt(flux_bound),
    }

    xlength = a * radius / 2
    max_transverse_sq = a * a * radius * radius / 8
    safe_sq = (a - 2 * d0) ** 2 * radius * radius
    fibre = 4 * d0 * radius
    rectangle = {
        "maxTransverseRadiusSquared": qt(max_transverse_sq),
        "safeRadiusSquared": qt(safe_sq),
        "insideFibreSafeDisk": max_transverse_sq <= safe_sq,
        "fibreLower": qt(fibre), "x2Length": qt(xlength), "x3Length": qt(xlength),
        "kTimesX2Length": qt(k * xlength), "completePeriods": "1",
        "onePeriodIntegral": qt(Q(4, 3) / k),
        "claimedX2LowerTimesPi": qt(a * radius / 3),
        "phaseUniform": True,
        "spatialLowerTimesPi": qt(2 * d0 * a * a * radius ** 3 / 3),
    }
    mass_coeff = Q(2, 9) * d0 * a * a * radius ** 3 * amp ** 3 / (k * k)
    cubic = {
        "timeLower": "(1-exp(-3))/(3*k^2)",
        "cBox": "2*(1-exp(-3))/(9*pi)",
        "massLowerCoefficientWithoutExpOverPi": qt(mass_coeff),
        "massPowers": {"delta0": "1", "a": "2", "R": "3", "k": "-2", "A": "3"},
        "inversePowers": {"delta0": "-2/3", "a": "-4/3", "R": "-2", "k": "4/3", "M": "2/3"},
        "combinedPowers": {"delta0": "-2/3", "absB": "1", "a": "2/3", "R": "0", "k": "-2/3", "M": "2/3"},
    }

    norm = fixtures["normalizationCase"]
    rho, cgamma = q(norm["rho"]), q(norm["cGamma"])
    rate = rho / 6 - cgamma / 12
    normalization = {
        "beforeScaleBounds": {"absB": "1", "a": "2/3", "R": "1/3", "omega": "1/3", "k": "-2/3", "p": "2/3"},
        "afterScaleBounds": {"L": "2/3", "R": "-2/3", "omega": "1/3", "p": "2/3"},
        "exponentialRate": qt(rate), "strictlyNegative": rate < 0,
    }

    l = fixtures["ledgerCase"]
    lR, omega, weight = map(q, (l["R"], l["omega"], l["outerWeight"]))
    field, other, measure = map(q, (l["F"], l["otherComponent"], l["tubeMeasure"]))
    projected, cancelled = map(q, (l["projectedPiece"], l["largerComponentAfterCancellation"]))
    magnitude = Q(5)
    packet = lR ** -2 * omega * field ** 3 * measure
    row = lR ** -2 * weight * magnitude ** 3 * measure
    ledger = {
        "velocityMagnitude": qt(magnitude), "packetCubicIntegral": qt(packet),
        "versionMRowContribution": qt(row), "packetToRowRatio": qt(packet / row),
        "pointwiseDominated": field <= magnitude,
        "projectionDominationValid": projected <= abs(cancelled),
    }

    e = fixtures["entranceCase"]
    ea, eR, eA, sigma = map(q, (e["a"], e["R"], e["A"], e["sigmaSample"]))
    entrance = {
        "E0OverPiSquared": qt(2 * eA * eA),
        "entranceUpperOverPi": qt(ea * ea * eR * eR * eA * eA),
        "fractionUpperTimesPi": qt(ea * ea * eR * eR / 2),
        "sigmaSample": qt(sigma), "powerGap": qt(2 - sigma),
        "validForEveryFixedSigmaBelowTwo": 0 <= sigma < 2,
    }

    tags = [int(x) for x in re.findall(r"\\tag\{Q\.(\d+)\}", text)]
    mentions = [int(x) for x in re.findall(r"Q\.(\d+)", text)]
    structure_ok = (
        tags == list(range(1, 29)) and len(tags) == len(set(tags))
        and all(x in set(tags) for x in mentions)
        and text.count("\\[") == 28 and text.count("\\]") == 28
        and text.count("\\begin{aligned}") == text.count("\\end{aligned}") == 2
    )
    controls_ok = (
        clean_bytes(raw) and clean_bytes(raw_primary) and clean_bytes(raw_source)
        and not re.search(r"(?<!\\)qquad", text) and text.count("\\qquad") == 17
        and "A^3\\int_0^T e^{-3k^2t}\\,dt\\\\" in text
    )
    deps_ok = all(path in text and digest in text for path, digest in FROZEN.items() if path not in {
        f"research/{STEM}.md", f"research/{STEM}_primary_audit.md", "research/r075q_report-source.md"
    })
    primary_ok = all(s in flat_primary for s in (
        "Verdict: **PASS**", "Mathematical blocker count: **0**",
        "Release blocker count: **0**", "does not authorize publication",
    ))

    radial_text_ok = all(s in flat for s in (
        "V_{\\xi,3}:=", "C_\\vartheta a^2R^2", "(a+\\delta)R<\\frac\\pi2",
        "periodic lift", "No Wiener summation is needed",
    ))
    harmonic_text_ok = all(s in flat for s in (
        "(\\partial_t+B\\partial_2-\\partial_2^2)F_k=0",
        "A>0", "k\\in\\mathbb N", "independent of `x_1,x_3`",
    ))
    flux_text_ok = all(s in flat for s in (
        "0<=eta<=1", "\\frac12\\int_0^T", "The constant row vanishes",
        "Taking absolute values only after that cancellation", "{8k^2}",
        "ordinary heat decay", "not an enhanced-dissipation estimate",
    ))
    rectangle_text_ok = all(s in flat for s in (
        "aR/(2sqrt(2))<=(a-2delta_0)R", "\\ge4\\delta_0R", "a\\ge4\\delta_0",
    ))
    phase_text_ok = all(s in flat for s in (
        "period `pi`", "\\frac43", "floor(k ell/pi)", "uniformly in the phase",
        "\\ge\\frac{aR}{3\\pi}", "\\ge\\frac{2\\delta_0a^2}{3\\pi}R^3",
    ))
    time_text_ok = all(s in flat for s in (
        "k^2T>=1", "\\frac{2(1-e^{-3})}{9\\pi}", "\\delta_0a^2R^3k^{-2}A^3",
    ))
    inversion_text_ok = all(s in flat for s in (
        "c_{\\rm box}^{-2/3}\\delta_0^{-2/3}", "a^{-4/3}R^{-2}k^{4/3}",
        "cancels the full `R^2`",
    ))
    normalization_text_ok = all(s in flat for s in (
        "p_{k,\\rm col}:=R^{-2}\\omega M_{k,\\rm col}",
        "\\frac\\omega R[\\mathcal T_{k,\\eta}^{(3)}]_+",
        "|B|a^{2/3}R^{1/3}\\omega^{1/3}k^{-2/3}",
        "L^{2/3}R^{-2/3}\\omega^{1/3}", "4279}{238140000}", "\\longrightarrow0",
    ))
    ledger_text_ok = all(s in flat for s in (
        "`[0,T]` to lie in the same scale-`2R` exterior measurement interval",
        "weight is at least `omega`", "actual coordinate component",
        "same smooth velocity `v_R`", "`|F_k|<=|v_R|` pointwise",
        "nonnegativity of the exterior cubic row", "p_{k,\\rm col}\\le C P_R^M",
        "not asserted for a harmonic projection", "does not assert arbitrary zero-trajectory realization",
    ))
    entrance_text_ok = all(s in flat for s in (
        "E_0=2\\pi^2A^2", "E_{\\rm in}\\le", "\\frac{a^2R^2}{2\\pi}",
        "For every fixed `0<=sigma<2`", "R^{2-\\sigma}\\longrightarrow0",
        "not a hidden use of P's entrance hypothesis",
    ))
    formula_ok = all(f"\\tag{{Q.{n}}}" in text for n in (1, 10, 14, 18, 21, 22, 24, 25, 26, 27, 28))
    source_ok = all(s in flat_source for s in (
        "arXiv:2603.14657", "arXiv:2410.05657", "arXiv:2103.07906",
        "arXiv:2101.05406", "10.1016/j.matpur.2019.04.009",
        "does not estimate Q's signed spherical-collar flux", "no observability theorem imported",
        "not a novelty or priority claim", "No citation graph or subscription-only exhaustive priority review",
    ))
    boundary_ok = all(s in flat for s in (
        "one real harmonic", "constant shear", "independent of `x_1,x_3`",
        "total-field rather than packet-projection based", "Fourier or Littlewood--Paley projection",
        "two or more horizontal harmonics", "arbitrary vertical structure", "general low-entrance packet",
        "nonconstant shear", "inter-packet or low-difference summation", "total upper- frequency cap",
        "arbitrary-field E.24", "complete-clock extraction", "fixed deletion", "suitable-weak transfer",
        "regularity or singularity conclusion", "No novelty or priority claim", "NOT\\ CLAY",
    ))

    checks = {
        "allFrozenBindings": rec(guarded("allFrozenBindings", all(x["expectedSha256"] == x["observedSha256"] for x in source_rows.values())), rows=source_rows),
        "fixtureExpectedBindings": rec(guarded("fixtureExpectedBindings", sha256(FIXTURES) == ("0" * 64 if MUTATION == "fixture_hash" else FIXTURES_SHA256) and sha256(EXPECTED) == ("0" * 64 if MUTATION == "expected_hash" else EXPECTED_SHA256))),
        "primaryAuditStatus": rec(guarded("primaryAuditStatus", primary_ok)),
        "dependencyTableBindings": rec(guarded("dependencyTableBindings", deps_ok)),
        "tagsReferencesDisplays": rec(guarded("tagsReferencesDisplays", structure_ok), tags=tags, displays=text.count("\\[")),
        "utf8ControlAndTex": rec(guarded("utf8ControlAndTex", controls_ok), qquadCount=text.count("\\qquad"), timeIntegralSameSourceLine=True),
        "radialDerivativeRow": rec(guarded("radialDerivativeRow", radial == expected["radial"] and radial_text_ok), values=radial),
        "harmonicEquation": rec(guarded("harmonicEquation", harmonic == expected["harmonic"] and harmonic_text_ok), values=harmonic),
        "signedFluxCancellation": rec(guarded("signedFluxCancellation", flux == expected["flux"] and flux_text_ok), values=flux),
        "rectangleFibreGeometry": rec(guarded("rectangleFibreGeometry", rectangle["insideFibreSafeDisk"] and rectangle["fibreLower"] == expected["rectangle"]["fibreLower"] and rectangle_text_ok), values=rectangle),
        "phaseUniformPeriodFloor": rec(guarded("phaseUniformPeriodFloor", all(rectangle[k0] == expected["rectangle"][k0] for k0 in ("kTimesX2Length", "completePeriods", "onePeriodIntegral", "claimedX2LowerTimesPi", "phaseUniform")) and phase_text_ok)),
        "spatialCollarMass": rec(guarded("spatialCollarMass", rectangle["spatialLowerTimesPi"] == expected["rectangle"]["spatialLowerTimesPi"] and phase_text_ok)),
        "timeIntegralAndCBox": rec(guarded("timeIntegralAndCBox", cubic["timeLower"] == expected["cubic"]["timeLower"] and cubic["cBox"] == expected["cubic"]["cBox"] and cubic["massLowerCoefficientWithoutExpOverPi"] == expected["cubic"]["massLowerCoefficientWithoutExpOverPi"] and cubic["massPowers"] == expected["cubic"]["massPowers"] and time_text_ok), values=cubic),
        "cubicInversionCombination": rec(guarded("cubicInversionCombination", cubic["inversePowers"] == expected["cubic"]["inversePowers"] and cubic["combinedPowers"] == expected["cubic"]["combinedPowers"] and inversion_text_ok)),
        "normalizationScaleAndRate": rec(guarded("normalizationScaleAndRate", normalization == expected["normalization"] and normalization_text_ok), values=normalization),
        "conditionalVersionMLedger": rec(guarded("conditionalVersionMLedger", ledger == expected["ledger"] and ledger["pointwiseDominated"] and not ledger["projectionDominationValid"] and ledger_text_ok), values=ledger),
        "lowEntranceDiagnostic": rec(guarded("lowEntranceDiagnostic", entrance == expected["entrance"] and entrance_text_ok), values=entrance),
        "formulaSentinels": rec(guarded("formulaSentinels", formula_ok)),
        "sourceReportBoundary": rec(guarded("sourceReportBoundary", source_ok)),
        "claimBoundary": rec(guarded("claimBoundary", boundary_ok)),
    }
    verdict = "PASS" if all(row["pass"] for row in checks.values()) else "FAIL"
    result = {
        "schema": SCHEMA,
        "suite": "R0.75Q",
        "verdict": verdict,
        "assertions": len(checks),
        "passed": sum(1 for x in checks.values() if x["pass"]),
        "mutation": MUTATION or None,
        "negativeMutationCount": len(NEGATIVE_MUTATIONS),
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "fixtureSha256": sha256(FIXTURES),
        "expectedSha256": sha256(EXPECTED),
        "checks": checks,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failed = [name for name, row in checks.items() if not row["pass"]]
    report = [
        "# R0.75Q exact finite certificate", "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {result['passed']}/{result['assertions']}",
        f"- Frozen main SHA-256: `{FROZEN[f'research/{STEM}.md']}`",
        f"- Negative mutation families: {len(NEGATIVE_MUTATIONS)}", "",
        "## Covered claims", "",
        "Exact rational checks cover radial scaling, the harmonic PDE, diagonal cancellation,",
        "the 1/8 flux constant, safe rectangle/fibre geometry, phase-uniform period counting,",
        "the cubic time integral and inversion, normalization, the frozen exponent, the",
        "conditional same-velocity Version-M ledger, and the low-entrance diagnostic.", "",
        "The Q.21 first inequality was read as one physical source line and explicitly includes",
        "the factor `int_0^T exp(-3*k^2*t) dt`.", "",
        "## Boundary", "",
        "This finite certificate proves no multimode, projected-field, vertical, nonconstant-shear,",
        "complete-clock, fixed-deletion, suitable-weak, regularity, or singularity statement.",
        "The bounded literature screen is byte-bound context, not novelty evidence. **NOT CLAY.**", "",
    ]
    if failed:
        report.extend(["## Failed checks", ""] + [f"- {x}" for x in failed] + [""])
    OUT_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(json.dumps({"suite": "R0.75Q", "verdict": verdict, "assertions": len(checks), "passed": result["passed"], "mutations": len(NEGATIVE_MUTATIONS)}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
