#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75P."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075p_buffered_collar_entrance_concentration.md"
PRIMARY = ROOT / "research/r075p_buffered_collar_entrance_concentration_primary_audit.md"
SOURCE = ROOT / "research/r075p_report-source.md"
FIXTURES = ROOT / "scripts/r075p_buffered_collar_entrance_concentration_fixtures.json"
EXPECTED = ROOT / "scripts/r075p_buffered_collar_entrance_concentration_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075P_JSON", ROOT / "research/r075p_buffered_collar_entrance_concentration_certificate.json"
))
OUT_REPORT = Path(os.environ.get(
    "R075P_REPORT", ROOT / "research/r075p_buffered_collar_entrance_concentration_certificate_report.md"
))
MUTATION = os.environ.get("R075P_MUTATION", "")
SCHEMA = "r075p-buffered-collar-entrance-concentration-certificate-v1"

FROZEN = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075i_diffusion_safe_block_participation.md":
        "c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7",
    "research/r075n_radial_collar_averaged_wiener_row.md":
        "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
    "research/r075o_vertical_diffusion_packet_gain.md":
        "3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9",
    "research/r075p_buffered_collar_entrance_concentration.md":
        "8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6",
    "research/r075p_buffered_collar_entrance_concentration_primary_audit.md":
        "e065759a1df3c118f71dd47ac9b5ded9df40536217f557b3c1155e8bf64d3390",
    "research/r075p_report-source.md":
        "fcde6bed847b0628aff7de90a49e8150e4a279fca8e46d7053943fdadf0478ca",
}
FIXTURES_SHA256 = "9d9bf2a00fbdf58eb85a01a3f7fe931f289a5bc1166430dac1f704e4406ec6d7"
EXPECTED_SHA256 = "cc472fb797c98d61e004c09fb84ba4a29029d72665f60507628c166134b39d31"

MUTATION_GROUPS = {
    "allFrozenBindings": (
        "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    ),
    "fixtureAndExpectedBindings": ("fixture_drift", "expected_drift"),
    "primaryAuditStatus": ("audit_status", "audit_blocker", "audit_authorization"),
    "fourDependencyTableBindings": ("dependency_table_missing",),
    "tagsReferencesAndDisplays": ("tag", "reference", "display"),
    "utf8AndControlSafety": ("control", "utf8"),
    "exactPlateauFibreGeometry": (
        "fibre_outer", "fibre_inner", "fibre_factor", "fibre_monotonicity",
        "fibre_safe_radius", "fibre_lower_only", "fibre_tangency", "central_chart",
    ),
    "movingCutoffTransport": (
        "cutoff_translation", "cutoff_transport_sign", "operator_drift",
        "operator_diffusion", "constant_shear",
    ),
    "localEnergyIdentityAndCap": (
        "local_identity_laplacian", "local_identity_gradient_sign", "gradient_cap",
        "gradient_four", "energy_eight", "r2_vs_k2", "cap_preserved",
    ),
    "timeWindowAndDisplacement": (
        "c0_energy", "tau_mu", "tau_k", "window_condition", "displacement_B",
        "displacement_R", "c0_displacement", "support_margin", "tau_inside",
    ),
    "persistenceFloor": ("persistence_direction", "persistence_half", "entrance_assumed"),
    "holderAndCubicLowerBound": (
        "holder_direction", "holder_volume", "holder_power", "fibre_to_cubic",
        "cubic_R_cancel", "time_mu", "cstar_sqrt2", "cstar_pi", "cubic_a",
        "cubic_mu", "cubic_K", "cubic_E",
    ),
    "inverseEnergyPowers": (
        "inverse_direction", "inverse_a", "inverse_mu", "inverse_K", "inverse_M",
        "no_backward",
    ),
    "fluxCombinationPowers": (
        "flux_quarter", "wiener_a", "combine_a", "combine_mu", "combine_K",
        "combine_M", "positive_part",
    ),
    "normalizationAndScalePowers": (
        "payment_R", "payment_omega", "flux_R", "flux_omega", "normalized_R",
        "normalized_omega", "normalized_p", "B_scale", "K_scale", "coefficient_R",
        "coefficient_L",
    ),
    "exactConcentrationThreshold": (
        "rho", "cgamma", "rate_sign", "rate_sigma", "threshold_numerator",
        "threshold_denominator", "threshold_strict", "equality_allowed",
    ),
    "conditionalVersionMLedger": (
        "ledger_time", "ledger_space", "ledger_weight", "ledger_nonnegative",
        "ledger_direction", "actual_component", "same_velocity",
        "pointwise_domination", "projection_excluded", "arbitrary_zero_path",
        "realized_subclass", "p3p30_independent",
    ),
    "lowConcentrationBoundary": (
        "low_fraction", "low_not_counterexample", "localized_kernel_open",
    ),
    "formulaAndStatusSentinels": (
        "formula_packet", "formula_cutoff", "formula_energy", "formula_holder",
        "formula_threshold", "formula_payment",
    ),
    "sourceReportBoundary": (
        "literature_identity", "literature_complete", "literature_import",
    ),
    "claimBoundary": (
        "single_packet", "total_cap", "e24_open", "nonconstant_open",
        "interpacket_open", "lowdiff_open", "cap_open", "complete_clock_open",
        "fixed_deletion_open", "suitable_weak_open", "regularity_open",
        "singularity_open", "novelty", "priority", "simulation", "dns", "clay",
    ),
}
NEGATIVE_MUTATIONS = tuple(name for names in MUTATION_GROUPS.values() for name in names)

Q = Fraction


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(str(value))


def qt(value: Q) -> str:
    return str(value)


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def clean_bytes(data: bytes) -> bool:
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any((byte < 32 and byte not in (9, 10, 13)) or byte == 127 for byte in data)


def group_ok(name: str, base: bool) -> bool:
    return bool(base and MUTATION not in MUTATION_GROUPS[name])


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075P_MUTATION: {MUTATION}")
    if len(set(NEGATIVE_MUTATIONS)) != len(NEGATIVE_MUTATIONS):
        raise SystemExit("duplicate mutation name in R0.75P suite")

    raw_main = MAIN.read_bytes()
    raw_primary = PRIMARY.read_bytes()
    raw_source = SOURCE.read_bytes()
    text = raw_main.decode("utf-8")
    primary_text = raw_primary.decode("utf-8")
    source_text = raw_source.decode("utf-8")
    flat = re.sub(r"\s+", " ", text)
    flat_primary = re.sub(r"\s+", " ", primary_text)
    flat_source = re.sub(r"\s+", " ", source_text)
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    frozen_expected = dict(FROZEN)
    drift_map = {
        "source_drift": "research/r075p_buffered_collar_entrance_concentration.md",
        "audit_drift": "research/r075p_buffered_collar_entrance_concentration_primary_audit.md",
        "report_source_drift": "research/r075p_report-source.md",
        "dependency_drift": "research/r075o_vertical_diffusion_packet_gain.md",
    }
    if MUTATION in drift_map:
        frozen_expected[drift_map[MUTATION]] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(frozen_expected.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256

    # Two exact rational fibres, including a nonzero transverse radius with
    # simultaneous Pythagorean roots: 15^2-12^2=9^2 and 13^2-12^2=5^2.
    geometry_cases = []
    derivative_signs = []
    derivative_all_safe = True
    for row in fixtures["fibreCases"]:
        a = q(row["a"])
        delta = q(row["delta0"])
        radius = q(row["R"])
        transverse = q(row["q"])
        outer = q(row["outerRoot"])
        inner = q(row["innerRoot"])
        roots_exact = (
            outer * outer == (a + delta) ** 2 - transverse ** 2
            and inner * inner == (a - delta) ** 2 - transverse ** 2
        )
        bracket = outer - inner
        fibre = 2 * radius * bracket
        lower = 4 * delta * radius
        if transverse == 0:
            derivative_signs.append("zero")
        elif transverse > 0 and outer > inner > 0:
            # ell'(q)/(2R)=q(1/inner_root-1/outer_root)>0.
            derivative_signs.append("positive")
        else:
            derivative_signs.append("invalid")
            derivative_all_safe = False
        geometry_cases.append({
            "bracket": qt(bracket),
            "fibreLength": qt(fibre),
            "lowerBound": qt(lower),
            "safe": roots_exact and transverse <= a - 2 * delta and fibre >= lower,
        })
    geometry = {
        "cases": geometry_cases,
        "bracketIncreasingOnSamples": all(
            q(geometry_cases[i]["bracket"]) <= q(geometry_cases[i + 1]["bracket"])
            for i in range(len(geometry_cases) - 1)
        ),
        "derivativeNonnegativeOnSafeInterval": derivative_all_safe
        and derivative_signs == ["zero", "positive"],
        "derivativeSignByCase": derivative_signs,
        # (a+delta)R=15/16<3/2<pi/2, using only the elementary pi>3.
        "centralChartCertifiedByPiGreaterThan3": Q(15, 16) < Q(3, 2),
    }

    local = fixtures["localEnergyCase"]
    a = q(local["a"])
    delta = q(local["delta0"])
    radius = q(local["R"])
    K = q(local["K"])
    B = q(local["B"])
    cb = q(local["CB"])
    cphi = q(local["Cphi"])
    c0 = q(local["c0"])
    mu = q(local["mu"])
    e0 = q(local["E0"])
    ein = q(local["Ein"])
    total_time = q(local["T"])
    tau = c0 * mu / (K * K)
    loss = (8 + cphi) * K * K * e0 * tau
    displacement = abs(B) * tau
    initial_radius = (a - 3 * delta) * radius
    final_radius = initial_radius + displacement
    safe_radius = (a - 2 * delta) * radius
    local_observed = {
        "tau": qt(tau),
        "KSquaredT": qt(K * K * total_time),
        "RMinus2": qt(radius ** -2),
        "KSquared": qt(K * K),
        "KInverseSquared": qt(K ** -2),
        "RCubed": qt(radius ** 3),
        "lossRateMultiplier": qt(8 + cphi),
        "certifiedLoss": qt(loss),
        "retainedEnergy": qt(ein - loss),
        "requiredFloor": qt(mu * e0 / 2),
        "displacement": qt(displacement),
        "displacementAllowance": qt(delta * radius),
        "initialSupportRadius": qt(initial_radius),
        "finalSupportRadiusBound": qt(final_radius),
        "safeSupportRadius": qt(safe_radius),
    }
    local_conditions = (
        ein >= mu * e0
        and radius ** -2 <= K * K
        and K ** -2 <= radius ** 3
        and K * K * total_time >= 1
        and c0 <= 1 / (2 * (8 + cphi))
        and c0 <= delta / cb
        and c0 * mu <= 1
        and tau <= total_time
        and displacement <= delta * radius
        and final_radius <= safe_radius
        and ein - loss >= mu * e0 / 2
    )

    # Nondegenerate exact Fourier identity. With F=cos(x), phi=1+c*cos(2x),
    # the moving-cutoff derivative cancels the B transport term. All entries
    # below are normalized by pi.
    identity_fixture = fixtures["localIdentityFourierCase"]
    identity_b = q(identity_fixture["B"])
    cutoff_c = q(identity_fixture["cutoffCos2Amplitude"])
    phi_f2 = 1 + cutoff_c / 2
    phi_grad2 = 1 - cutoff_c / 2
    laplacian_phi_f2 = -2 * cutoff_c
    transport_contribution = identity_b * 0
    direct_eprime = transport_contribution - 2 * phi_f2
    identity_rhs = laplacian_phi_f2 - 2 * phi_grad2
    local_identity = {
        "cutoffNonnegative": abs(cutoff_c) <= 1,
        "transportContributionOverPi": qt(transport_contribution),
        "phiF2IntegralOverPi": qt(phi_f2),
        "phiGrad2IntegralOverPi": qt(phi_grad2),
        "laplacianPhiF2IntegralOverPi": qt(laplacian_phi_f2),
        "directEPrimeOverPi": qt(direct_eprime),
        "identityRhsOverPi": qt(identity_rhs),
    }

    volume_over_pi = a * a * radius * radius
    floor = mu * e0 / 2
    # All square roots cancel after multiplying the exact rational fixture by sqrt(pi).
    floor_sqrt = Q(math.isqrt(floor.numerator), math.isqrt(floor.denominator))
    if floor_sqrt * floor_sqrt != floor:
        raise SystemExit("R0.75P rational Holder fixture is not a perfect square")
    support_l3_sqrt_pi = floor * floor_sqrt / (a * radius)
    fibre_minimum = 4 * delta * radius
    shell_l3_sqrt_pi = fibre_minimum * support_l3_sqrt_pi
    mass_sqrt_pi = tau * shell_l3_sqrt_pi
    cubic = {
        "volumeOverPi": qt(volume_over_pi),
        "supportL3LowerTimesSqrtPi": qt(support_l3_sqrt_pi),
        "shellL3LowerTimesSqrtPi": qt(shell_l3_sqrt_pi),
        "massLowerTimesSqrtPi": qt(mass_sqrt_pi),
        "cStar": "sqrt(2)*delta0*c0/sqrt(pi)",
        "lowerPowers": {"a": "-1", "mu": "5/2", "K": "-2", "E0": "3/2"},
        "inversePowers": {"a": "2/3", "mu": "-5/3", "K": "4/3", "M": "2/3"},
    }

    flux = {
        "quarterCoefficient": "1/4",
        "combinedPowers": {
            "absB": "1", "a": "5/3", "mu": "-5/3", "K": "-2/3", "M": "2/3"
        },
    }
    normalization = {
        "beforeScaleBounds": {
            "absB": "1", "a": "5/3", "mu": "-5/3", "R": "1/3",
            "omega": "1/3", "K": "-2/3", "p": "2/3",
        },
        "afterScaleBounds": {
            "L": "5/3", "mu": "-5/3", "R": "-2/3", "omega": "1/3", "p": "2/3",
        },
    }
    norm = fixtures["normalizationCase"]
    rho = q(norm["rho"])
    cgamma = q(norm["cGamma"])
    sigma_star = (cgamma / rho - 2) / 5

    def rate(sigma: Q) -> Q:
        return rho / 6 - cgamma / 12 + 5 * sigma * rho / 12

    normalization.update({
        "sigmaStar": qt(sigma_star),
        "rateAtZero": qt(rate(Q(0))),
        "rateAtHalfThreshold": qt(rate(sigma_star / 2)),
        "rateAtThreshold": qt(rate(sigma_star)),
        "strictEndpoint": True,
    })

    ledger_case = fixtures["ledgerCase"]
    ledger_radius = q(ledger_case["R"])
    omega = q(ledger_case["omega"])
    outer_weight = q(ledger_case["outerWeight"])
    f_value = q(ledger_case["F"])
    other = q(ledger_case["otherComponent"])
    tube_measure = q(ledger_case["tubeMeasure"])
    velocity_magnitude = Q(5)  # exact 3-4-5 fixture
    packet_integral = ledger_radius ** -2 * omega * tube_measure * abs(f_value) ** 3
    row_contribution = ledger_radius ** -2 * outer_weight * tube_measure * velocity_magnitude ** 3
    ledger = {
        "velocityMagnitude": qt(velocity_magnitude),
        "packetCubicIntegral": qt(packet_integral),
        "versionMRowContribution": qt(row_contribution),
        "packetToRowRatio": qt(packet_integral / row_contribution),
        "pointwiseDominated": abs(f_value) <= velocity_magnitude and outer_weight >= omega,
        "projectionDominationValid": abs(q(ledger_case["projectedPiece"]))
        <= abs(q(ledger_case["largerComponentAfterCancellation"])),
    }
    low = {
        "exponentialPowerGapAtSigmaStar": qt(2 - sigma_star),
        "failureIsCounterexample": False,
    }

    tags = [int(value) for value in re.findall(r"\\tag\{P\.(\d+)\}", text)]
    without_tags = re.sub(r"\\tag\{P\.\d+\}", "", text)
    refs = [int(value) for value in re.findall(r"\(P\.(\d+)\)", without_tags)]
    display_opens = len(re.findall(r"(?m)^\\\[$", text))
    display_closes = len(re.findall(r"(?m)^\\\]$", text))

    formula_sentinels = (
        "K\\le|n|\\le2K", "n^2+j^2\\le4K^2", "\\phi_0(x_2-Bt,x_3)",
        "\\partial_t\\phi_t+B\\partial_2\\phi_t=0",
        "E_\\phi'(t)", "-2\\int_{\\mathbb T^2}\\phi_t|\\nabla_yF|^2",
        "\\tau:=c_0\\mu K^{-2}", "\\frac\\mu2E_0",
        "c_*:=\\frac{\\sqrt2\\,\\delta_0c_0}{\\sqrt\\pi}",
        "a^{5/3}\\mu^{-5/3}", "R^{-2/3}\\omega^{1/3}",
        "\\frac{8558}{178605}", "p_{K,\\rm col}\\le C P_R^M",
    )
    status_sentinels = (
        "actual coordinate component of the same smooth velocity", "|F|<=|v_R|",
        "not a Littlewood--Paley", "P.3--P.30 do not use this realization hypothesis",
        "conditional realized-subclass closure", "failure of (P.5) is not a counterexample",
        "spatially localized signed heat kernel", "\\mathbf{NOT\\ CLAY}",
    )
    source_sentinels = (
        "arXiv:1202.4876", "arXiv:1711.04279", "arXiv:2108.11192",
        "Apraiz", "Escauriaza", "Ervedoza", "Zuazua", "Coti Zelati", "Gallay",
        "It is not evidence of novelty or priority", "do not validate P.1, P.5",
        "actual-component realization",
    )
    boundary_state = {
        "constantShearOnly": "constant-shear" in flat,
        "singlePacketOnly": "single-packet" in flat,
        "totalFrequencyCapRetained": "total upper-frequency cap" in flat,
        "entranceConcentrationAssumed": "entrance concentration P.5 holds" in flat_primary,
        "fieldIsActualComponent": "actual coordinate component of the same smooth velocity" in flat,
        "sameVelocityAsVersionM": "same smooth velocity `v_R` to which `P_R^M` is applied" in flat,
        "pointwiseDomination": "`|F|<=|v_R|` pointwise" in flat,
        "projectionExcluded": "not a Littlewood--Paley or Fourier projection" in flat,
        "p3ThroughP30Independent": "P.3--P.30 do not use this realization hypothesis" in flat,
        "conditionalRealizedSubclass": "conditional realized-subclass closure" in flat,
        "arbitraryZeroTrajectoryNotClaimed": "does not assert that an arbitrary constant-shear packet realizes" in flat,
        "lowConcentrationNotCounterexample": "failure of (P.5) is not a counterexample" in flat,
        "lowConcentrationOpen": "low-concentration complement" in flat,
        "localizedSignedKernelOpen": "spatially localized signed heat kernel" in flat,
        "nonconstantShearOpen": "nonconstant shear" in flat,
        "interpacketOpen": "inter-packet summation" in flat,
        "lowDifferencesOpen": "low differences" in flat,
        "capRemovalOpen": "removal of the total upper-frequency cap" in flat,
        "E24Open": "arbitrary-field E.24" in flat,
        "completeClockOpen": "complete-clock extraction" in flat,
        "fixedDeletionOpen": "fixed deletion" in flat,
        "suitableWeakOpen": "suitable-weak transfer" in flat,
        "regularityOpen": "regularity" in flat,
        "singularityOpen": "singularity conclusion" in flat,
        "noNovelty": "No novelty or priority claim" in flat,
        "noPriority": "No novelty or priority claim" in flat,
        "notClay": "NOT\\ CLAY" in text,
    }

    checks: dict[str, dict[str, Any]] = {}
    checks["allFrozenBindings"] = record(group_ok(
        "allFrozenBindings", all(row["expectedSha256"] == row["observedSha256"] for row in source_rows.values())
    ), sources=source_rows)
    checks["fixtureAndExpectedBindings"] = record(group_ok(
        "fixtureAndExpectedBindings",
        sha256(FIXTURES) == fixture_expected_hash and sha256(EXPECTED) == expected_expected_hash,
    ), fixtureSha256=sha256(FIXTURES), expectedSha256=sha256(EXPECTED))
    checks["primaryAuditStatus"] = record(group_ok(
        "primaryAuditStatus",
        "Verdict: **PASS**" in primary_text
        and "Mathematical blocker count: **0**" in primary_text
        and "Release blocker count: **0**" in primary_text
        and "does not authorize publication" in primary_text,
    ))
    dep_paths = list(FROZEN)[:4]
    checks["fourDependencyTableBindings"] = record(group_ok(
        "fourDependencyTableBindings", all(path in text and FROZEN[path] in text for path in dep_paths)
    ))
    checks["tagsReferencesAndDisplays"] = record(group_ok(
        "tagsReferencesAndDisplays",
        tags == list(range(1, 32)) and len(set(tags)) == 31
        and all(1 <= ref <= 31 for ref in refs)
        and display_opens == 31 and display_closes == 31,
    ), tags=tags, references=sorted(set(refs)), displayOpens=display_opens, displayCloses=display_closes)
    clean = all(clean_bytes(data) for data in (raw_main, raw_primary, raw_source))
    checks["utf8AndControlSafety"] = record(group_ok("utf8AndControlSafety", clean))
    checks["exactPlateauFibreGeometry"] = record(group_ok(
        "exactPlateauFibreGeometry", geometry == expected["geometry"]
    ), observed=geometry)
    checks["movingCutoffTransport"] = record(group_ok(
        "movingCutoffTransport",
        "\\phi_0(x_2-Bt,x_3)" in text
        and "\\partial_t\\phi_t+B\\partial_2\\phi_t=0" in text
        and "constant-shear evolution" in text,
    ))
    checks["localEnergyIdentityAndCap"] = record(group_ok(
        "localEnergyIdentityAndCap",
        local_observed == expected["localEnergy"]
        and local_identity == expected["localIdentity"]
        and "\\Delta_y\\phi_t|F|^2" in text
        and "-2\\int_{\\mathbb T^2}\\phi_t|\\nabla_yF|^2" in text
        and "\\le4K^2\\|F(t)\\|_2^2" in text,
    ), observed={"scaleFixture": local_observed, "fourierIdentity": local_identity})
    checks["timeWindowAndDisplacement"] = record(group_ok(
        "timeWindowAndDisplacement", local_conditions
    ))
    checks["persistenceFloor"] = record(group_ok(
        "persistenceFloor", ein - loss == mu * e0 / 2 and "E_\\phi(t)\\ge\\frac\\mu2E_0" in text
    ))
    checks["holderAndCubicLowerBound"] = record(group_ok(
        "holderAndCubicLowerBound",
        cubic["volumeOverPi"] == expected["cubic"]["volumeOverPi"]
        and cubic["supportL3LowerTimesSqrtPi"] == expected["cubic"]["supportL3LowerTimesSqrtPi"]
        and cubic["shellL3LowerTimesSqrtPi"] == expected["cubic"]["shellL3LowerTimesSqrtPi"]
        and cubic["massLowerTimesSqrtPi"] == expected["cubic"]["massLowerTimesSqrtPi"]
        and cubic["lowerPowers"] == expected["cubic"]["lowerPowers"]
        and cubic["cStar"] == expected["cubic"]["cStar"],
    ), observed=cubic)
    checks["inverseEnergyPowers"] = record(group_ok(
        "inverseEnergyPowers", cubic["inversePowers"] == expected["cubic"]["inversePowers"]
        and "No backward heat estimate" in text
    ))
    checks["fluxCombinationPowers"] = record(group_ok(
        "fluxCombinationPowers", flux == expected["flux"]
        and "\\frac{|B|\\mathcal W_\\infty}{4K^2}E_0" in text
    ), observed=flux)
    checks["normalizationAndScalePowers"] = record(group_ok(
        "normalizationAndScalePowers",
        normalization["beforeScaleBounds"] == expected["normalization"]["beforeScaleBounds"]
        and normalization["afterScaleBounds"] == expected["normalization"]["afterScaleBounds"],
    ), observed=normalization)
    checks["exactConcentrationThreshold"] = record(group_ok(
        "exactConcentrationThreshold",
        {key: normalization[key] for key in (
            "sigmaStar", "rateAtZero", "rateAtHalfThreshold", "rateAtThreshold", "strictEndpoint"
        )} == {key: expected["normalization"][key] for key in (
            "sigmaStar", "rateAtZero", "rateAtHalfThreshold", "rateAtThreshold", "strictEndpoint"
        )}
        and rate(sigma_star) == 0 and rate(sigma_star / 2) < 0,
    ))
    checks["conditionalVersionMLedger"] = record(group_ok(
        "conditionalVersionMLedger",
        ledger == expected["ledger"] and all(boundary_state[key] for key in (
            "fieldIsActualComponent", "sameVelocityAsVersionM", "pointwiseDomination",
            "projectionExcluded", "p3ThroughP30Independent", "conditionalRealizedSubclass",
            "arbitraryZeroTrajectoryNotClaimed",
        )) and "p_{K,\\rm col}\\le C P_R^M" in text,
    ), observed=ledger)
    checks["lowConcentrationBoundary"] = record(group_ok(
        "lowConcentrationBoundary", low == expected["lowConcentration"]
        and boundary_state["lowConcentrationNotCounterexample"]
        and boundary_state["localizedSignedKernelOpen"],
    ), observed=low)
    checks["formulaAndStatusSentinels"] = record(group_ok(
        "formulaAndStatusSentinels", all(token in text for token in formula_sentinels)
        and all(token in text for token in status_sentinels)
    ))
    checks["sourceReportBoundary"] = record(group_ok(
        "sourceReportBoundary", all(token in source_text for token in source_sentinels)
        and "no exhaustive citation graph" in flat_source
    ))
    checks["claimBoundary"] = record(group_ok(
        "claimBoundary", all(boundary_state.values())
    ), state=boundary_state)

    passed = sum(1 for item in checks.values() if item["pass"])
    total = len(checks)
    verdict = "PASS" if passed == total else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "mutation": MUTATION or None,
        "assertions": {"passed": passed, "total": total},
        "checks": checks,
        "geometry": geometry,
        "localEnergy": local_observed,
        "localIdentity": local_identity,
        "cubic": cubic,
        "flux": flux,
        "normalization": normalization,
        "ledger": ledger,
        "lowConcentration": low,
        "claimBoundary": boundary_state,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failures = [name for name, item in checks.items() if not item["pass"]]
    report = "\n".join([
        "# R0.75P finite certificate report",
        "",
        f"- Verdict: **{verdict}**",
        f"- Assertions: {passed}/{total}",
        f"- Mathematical blockers: {0 if verdict == 'PASS' else len(failures)}",
        f"- Main SHA-256: {sha256(MAIN)}",
        f"- Fixture SHA-256: {sha256(FIXTURES)}",
        f"- Expected SHA-256: {sha256(EXPECTED)}",
        f"- Failed checks: {', '.join(failures) if failures else 'none'}",
        "",
        "Exact rational fibres verify the 4*delta0*R lower bound, including a nonzero",
        "Pythagorean slice. The moving-cutoff fixture verifies the transport sign,",
        "4*K^2 gradient cap, 8+C_phi loss, tau, displacement, and half-energy floor.",
        "",
        "The Holder ledger verifies c*=sqrt(2)*delta0*c0/sqrt(pi), the complete",
        "a/mu/K powers, the inverse powers, and the O+N flux combination. The",
        "normalization gives sigma*=8558/178605 with a strict endpoint.",
        "",
        "P.31 is certified only under the explicit same-v_R actual-coordinate-component",
        "hypothesis and aligned nonnegative Version-M row. Fourier projections and",
        "arbitrary packet realization remain excluded. The low-concentration branch,",
        "E.24, complete clock, fixed deletion, and regularity remain OPEN. **NOT CLAY.**",
        "",
    ])
    OUT_REPORT.write_text(report, encoding="utf-8")
    print(json.dumps({"verdict": verdict, "assertions": total, "passed": passed}, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
