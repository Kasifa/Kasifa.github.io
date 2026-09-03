#!/usr/bin/env python3
"""Fail-closed exact/structural certificate for the frozen R0.75D route screen."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075d_passive_gradient_route_screen.md"
OUT_JSON = Path(
    os.environ.get(
        "R075D_JSON",
        ROOT / "research/r075d_passive_gradient_route_screen_certificate.json",
    )
)
OUT_REPORT = Path(
    os.environ.get(
        "R075D_REPORT",
        ROOT / "research/r075d_passive_gradient_route_screen_certificate_report.md",
    )
)
MUTATION = os.environ.get("R075D_MUTATION", "")
SCHEMA = "r075d-passive-gradient-route-screen-certificate-v1"
MAIN_SHA256 = "54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6"

# R0.75D has no embedded frozen-source table. These are certificate-side
# bindings for the two notes whose results D explicitly invokes.
CERTIFICATE_DEPENDENCIES = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075c_background_shear_packing_false_positive.md":
        "1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89",
}

NEGATIVE_MUTATIONS = (
    "holder_volume",
    "cubic_payment_r",
    "target_weight",
    "klow_threshold",
    "klow_rate",
    "modal_energy_sign",
    "modal_decay",
    "zero_mode_omission",
    "gradient_forcing_sign",
    "gradient_dissipation",
    "transition_volume",
    "block_count",
    "critical_threshold",
    "gap_fraction",
    "transport_sign",
    "transport_dropped",
    "pf_normalization",
    "fallback_cutoff_r",
    "fallback_volume",
    "mixed_holder",
    "mixed_weight",
    "cubic_sum",
    "pb_scale",
    "pb_rate",
    "small_payment_direction",
    "linear_absorbed",
    "interaction_power",
    "component_promotion",
    "high_frequency_proved",
    "intermediate_band_closed",
    "commutator_closed",
    "periodic_dropped",
    "counterexample_promotion",
    "full_clock_promotion",
    "source_drift",
    "dependency_drift",
    "dependency_table_assumed",
    "tag",
    "reference",
    "display",
    "clay",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rat(value: F) -> str:
    return str(value)


def exponent_row(**values: F) -> dict[str, str]:
    return {key: rat(value) for key, value in values.items()}


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075D_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)

    rho = F(9, 10000)
    c_gamma = F(8, 3969)

    volume_l = F(2)
    volume_r = F(4) if MUTATION == "holder_volume" else F(5)
    holder_l = volume_l / 3
    holder_r = volume_r / 3

    cubic_r = F(1) if MUTATION == "cubic_payment_r" else F(2)
    cubic_omega = F(-1)
    cubic_p = F(1)
    cubic_two_thirds_r = F(2, 3) * cubic_r
    cubic_two_thirds_omega = F(2, 3) * cubic_omega
    cubic_two_thirds_p = F(2, 3) * cubic_p

    l2_l = holder_l
    l2_r = holder_r + cubic_two_thirds_r
    l2_omega = cubic_two_thirds_omega
    l2_p = cubic_two_thirds_p

    prefactor_r = F(-1)
    prefactor_omega = F(0) if MUTATION == "target_weight" else F(1)
    target_k = F(2)
    target_l = l2_l
    target_r = l2_r + prefactor_r
    target_omega = l2_omega + prefactor_omega
    target_p = l2_p

    klow_r = -target_r / 2
    klow_l = -target_l / 2
    klow_omega = -target_omega / 2
    if MUTATION == "klow_threshold":
        klow_omega = F(1, 6)

    power_ledger = {
        "D.4_spacetimeVolume": exponent_row(L=volume_l, R=volume_r),
        "D.4_holderMeasureFactor": exponent_row(L=holder_l, R=holder_r),
        "D.4_cubicPayment": exponent_row(
            R=cubic_r, omega=cubic_omega, payment=cubic_p
        ),
        "D.4_cubicTwoThirds": exponent_row(
            R=cubic_two_thirds_r,
            omega=cubic_two_thirds_omega,
            payment=cubic_two_thirds_p,
        ),
        "D.4_L2Bound": exponent_row(
            L=l2_l, R=l2_r, omega=l2_omega, payment=l2_p
        ),
        "D.5_targetCoefficient": exponent_row(
            K=target_k,
            L=target_l,
            R=target_r,
            omega=target_omega,
            payment=target_p,
        ),
        "D.6_Klow": exponent_row(
            L=klow_l, R=klow_r, omega=klow_omega
        ),
    }
    expected_power_ledger = {
        "D.4_spacetimeVolume": {"L": "2", "R": "5"},
        "D.4_holderMeasureFactor": {"L": "2/3", "R": "5/3"},
        "D.4_cubicPayment": {"R": "2", "omega": "-1", "payment": "1"},
        "D.4_cubicTwoThirds": {
            "R": "4/3", "omega": "-2/3", "payment": "2/3"
        },
        "D.4_L2Bound": {
            "L": "2/3", "R": "3", "omega": "-2/3", "payment": "2/3"
        },
        "D.5_targetCoefficient": {
            "K": "2", "L": "2/3", "R": "2",
            "omega": "1/3", "payment": "2/3"
        },
        "D.6_Klow": {"L": "-1/3", "R": "-1", "omega": "-1/6"},
    }

    klow_rate = (-klow_r) * rho / 4 + (-klow_omega) * c_gamma / 4
    if MUTATION == "klow_rate":
        klow_rate += F(1, 10**9)
    expected_klow_rate = F(147163, 476280000)

    block_count_r = F(-2) if MUTATION == "block_count" else F(-1)
    critical_k_r = F(-1) if MUTATION == "critical_threshold" else F(-3, 2)
    critical_rate = (-critical_k_r) * rho / 4
    gap = critical_rate - expected_klow_rate
    if MUTATION == "gap_fraction":
        gap += F(1, 10**9)
    expected_gap = F(27163, 952560000)

    # D.16--D.23: retain the transport row and normalize the two cubic
    # masses separately. The computation is deliberately independent of
    # the earlier frequency-piece ledger.
    mass_normalization_r = (
        F(-1) if MUTATION == "pf_normalization" else F(-2)
    )
    mass_normalization_omega = F(1)
    cubic_integral_r = -mass_normalization_r
    cubic_integral_omega = -mass_normalization_omega

    fallback_volume_l = F(2)
    fallback_volume_r = (
        F(4) if MUTATION == "fallback_volume" else F(5)
    )
    cutoff_prefactor_r = (
        F(-2) if MUTATION == "fallback_cutoff_r" else F(-3)
    )
    cutoff_prefactor_omega = F(1)
    fallback_result_l = fallback_volume_l / 3
    fallback_result_r = (
        cutoff_prefactor_r
        + fallback_volume_r / 3
        + F(2, 3) * cubic_integral_r
    )
    fallback_result_omega = (
        cutoff_prefactor_omega
        + F(2, 3) * cubic_integral_omega
    )

    transport_sign = -1 if MUTATION == "transport_sign" else 1
    transport_retained = MUTATION != "transport_dropped"
    transport_prefactor_r = F(-2)
    transport_prefactor_omega = (
        F(0) if MUTATION == "mixed_weight" else F(1)
    )
    mixed_b_power = F(2, 3) if MUTATION == "mixed_holder" else F(1, 3)
    mixed_f_power = F(1) - mixed_b_power
    mixed_result_r = (
        transport_prefactor_r
        + (mixed_b_power + mixed_f_power) * cubic_integral_r
    )
    mixed_result_omega = (
        transport_prefactor_omega
        + (mixed_b_power + mixed_f_power) * cubic_integral_omega
    )
    cubic_sum_controlled = MUTATION != "cubic_sum"

    pb_l = F(2)
    pb_r = F(-2) if MUTATION == "pb_scale" else F(-3)
    pb_omega = F(1)
    pb_rate = (-pb_r) * rho / 4 - pb_omega * c_gamma / 4
    if MUTATION == "pb_rate":
        pb_rate += F(1, 10**9)
    expected_pb_rate = F(27163, 158760000)

    small_payment_leq_one = MUTATION != "small_payment_direction"
    linear_term_absorbed = MUTATION == "linear_absorbed"
    interaction_pb_power = F(1)
    interaction_pf_power = (
        F(1) if MUTATION == "interaction_power" else F(2)
    )
    interaction_payment_power = F(-2)

    fallback_ledger = {
        "D.16_massNormalization": exponent_row(
            R=mass_normalization_r, omega=mass_normalization_omega
        ),
        "D.18_spacetimeVolume": exponent_row(
            L=fallback_volume_l, R=fallback_volume_r
        ),
        "D.18_cutoffPrefactor": exponent_row(
            R=cutoff_prefactor_r, omega=cutoff_prefactor_omega
        ),
        "D.18_result": exponent_row(
            L=fallback_result_l,
            R=fallback_result_r,
            omega=fallback_result_omega,
            pF=F(2, 3),
        ),
        "D.19_transportPrefactor": exponent_row(
            R=transport_prefactor_r, omega=transport_prefactor_omega
        ),
        "D.19_mixedResult": exponent_row(
            R=mixed_result_r,
            omega=mixed_result_omega,
            pB=mixed_b_power,
            pF=mixed_f_power,
        ),
        "D.22_pBScale": exponent_row(L=pb_l, R=pb_r, omega=pb_omega),
        "D.23_interactionCondition": exponent_row(
            pB=interaction_pb_power,
            pF=interaction_pf_power,
            payment=interaction_payment_power,
        ),
    }
    expected_fallback_ledger = {
        "D.16_massNormalization": {"R": "-2", "omega": "1"},
        "D.18_spacetimeVolume": {"L": "2", "R": "5"},
        "D.18_cutoffPrefactor": {"R": "-3", "omega": "1"},
        "D.18_result": {
            "L": "2/3", "R": "0", "omega": "1/3", "pF": "2/3"
        },
        "D.19_transportPrefactor": {"R": "-2", "omega": "1"},
        "D.19_mixedResult": {
            "R": "0", "omega": "0", "pB": "1/3", "pF": "2/3"
        },
        "D.22_pBScale": {"L": "2", "R": "-3", "omega": "1"},
        "D.23_interactionCondition": {
            "pB": "1", "pF": "2", "payment": "-2"
        },
    }

    modal = {
        "diffusionCoefficient": -1,
        "horizontalLaplacianCoefficient": 1,
        "imaginaryShearCoefficient": 1,
        "energyTimeDerivative": F(1, 2),
        "verticalDissipationSign": 1,
        "horizontalDissipationSign":
            -1 if MUTATION == "modal_energy_sign" else 1,
        "shearRealPart": 0,
        "normDecayCoefficient": 2 if MUTATION == "modal_decay" else 1,
    }
    zero_mode_obstruction = MUTATION != "zero_mode_omission"

    gradient_forcing_sign = 1 if MUTATION == "gradient_forcing_sign" else -1
    gradient_dissipation = (
        "Hessian" if MUTATION == "gradient_dissipation" else "Laplacian"
    )

    transition_l = F(2) if MUTATION == "transition_volume" else F(1)
    transition_r = F(3)
    full_collar_l = F(2)
    full_collar_r = F(3)

    route_state = {
        "exactPassiveFallbackProved": True,
        "smallPaymentFallbackProved": True,
        "frozenLargePaymentBranchClosed": linear_term_absorbed,
        "interactionConditionProved": linear_term_absorbed,
        "transportRetained": transport_retained,
        "unconditionalLowFrequencyLemma":
            MUTATION == "component_promotion",
        "highFrequencyLocalCaptureProved":
            MUTATION == "high_frequency_proved",
        "intermediateBandClosed":
            MUTATION == "intermediate_band_closed",
        "commutatorsClosed":
            MUTATION == "commutator_closed",
        "periodizationRetained":
            MUTATION != "periodic_dropped",
        "exactCounterexampleConstructed":
            MUTATION == "counterexample_promotion",
        "fullClockExtractionProved":
            MUTATION == "full_clock_promotion",
        "clayClaim":
            MUTATION == "clay",
    }

    tags = re.findall(r"\\tag\{(D\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("D.1")
    references = [
        "D." + value for value in re.findall(r"\(D\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("D.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"D.{index}" for index in range(1, 24)]

    dependency_expectations = dict(CERTIFICATE_DEPENDENCIES)
    if MUTATION == "dependency_drift":
        first_path = sorted(dependency_expectations)[0]
        dependency_expectations[first_path] = "0" * 64
    dependency_rows = {
        path: {
            "expectedSha256": dependency_expectations[path],
            "observedSha256": sha256(ROOT / path),
            "bindingMode": "certificate-side",
            "mainTableEntryRequired": False,
        }
        for path in sorted(dependency_expectations)
    }
    dependency_table_assumed = MUTATION == "dependency_table_assumed"
    main_source_table_present = any(
        digest in text for digest in CERTIFICATE_DEPENDENCIES.values()
    )

    b_text = (ROOT / "research/r075b_bulk_clock_outer_padding_gate.md").read_text(
        encoding="utf-8"
    )
    b_tags = set(re.findall(r"\\tag\{(B\.[^}]+)\}", b_text))
    c_text = (
        ROOT / "research/r075c_background_shear_packing_false_positive.md"
    ).read_text(encoding="utf-8")

    required_tokens = (
        r"D_{k,R}^{{\rm out},F}",
        r"\frac{\omega}{R}\int_{I_{2R}}\int",
        r"O(L^2R^5)",
        r"CL^{2/3}R^{5/3}",
        r"CR^2\omega^{-1}P_R^M",
        r"CK^2L^{2/3}R^2\omega^{1/3}(P_R^M)^{2/3}",
        r"cR^{-1}L^{-1/3}\omega^{-1/6}",
        r"\frac\rho4+\frac{c_\gamma}{24}+o(1)",
        "not yet an unconditional low-frequency lemma",
        r"\partial_tf_n-\partial_3^2f_n+(n^2+inb)f_n=0",
        r"F_m(t,x_3)=e^{-m^2t}\sin(mx_3)",
        r"=-b_3\partial_2F",
        r"+\|\Delta_{23}F\|_2^2",
        r"=-\int b_3\,\partial_2F\,\partial_3F",
        r"O(LR^3)",
        r"O(L^2R^3)",
        r"K^2R^3\gg1",
        r"K\gg R^{-3/2}",
        r"\frac\rho8-\frac{c_\gamma}{24}>0",
        r"K_{\rm low}\ll K\lesssim R^{-3/2}",
        r"[P_{\le K},b]\partial_2F",
        r"[P_{\le K},\xi_k^R]F",
        "Periodization must be retained before using any kernel estimate",
        r"p_F&:=R^{-2}\omega",
        r"p_b&:=R^{-2}\omega",
        r"p_F+p_b\le CP_R^M",
        r"\omega R^{-3}\int_{I_{2R}}\int_{\rm out}|F|^2",
        r"CL^{2/3}\omega^{1/3}p_F^{2/3}",
        r"\omega R^{-2}\int_{I_{2R}}\int_{\rm out}|b||F|^2",
        r"=p_b^{1/3}p_F^{2/3}",
        r"+Cp_b^{1/3}p_F^{2/3}",
        r"+CP_R^M.",
        r"P_R^M\le1",
        r"P_R^M\le(P_R^M)^{2/3}",
        r"p_b\asymp L^2\omega R^{-3}",
        r"\frac{27163}{158760000}>0",
        r"P_R^M\ge c p_b\to\infty",
        r"p_bp_F^2\le C(P_R^M)^2",
        "No such uniform interaction bound is presently proved",
        "Reapplying absolute Hölder/Young inequalities cannot change",
        "every commutator and shell-weight tail remains OPEN",
        "NO EXACT COUNTEREXAMPLE CONSTRUCTED",
        "proves neither complete-clock extraction nor a",
        r"\mathbf{NOT\ CLAY}",
    )

    actual_main_hash = sha256(MAIN)
    expected_main_hash = "0" * 64 if MUTATION == "source_drift" else MAIN_SHA256

    checks = {
        "mainSourceBinding": record(
            actual_main_hash == expected_main_hash,
            expectedSha256=expected_main_hash,
            observedSha256=actual_main_hash,
        ),
        "certificateDependencyBindings": record(
            all(
                row["expectedSha256"] == row["observedSha256"]
                for row in dependency_rows.values()
            ),
            sources=dependency_rows,
        ),
        "dependencyBoundary": record(
            not dependency_table_assumed and not main_source_table_present,
            mode="certificate-side only",
            mainContainsFrozenSourceTable=main_source_table_present,
            mainTableEntryRequired=dependency_table_assumed,
        ),
        "powerLedgerD4ToD6": record(
            power_ledger == expected_power_ledger,
            exponents=power_ledger,
        ),
        "exactKlowRateD7": record(
            klow_rate == expected_klow_rate and klow_rate > 0,
            value=rat(klow_rate),
            expected=rat(expected_klow_rate),
        ),
        "fallbackPowerLedgerD16ToD23": record(
            fallback_ledger == expected_fallback_ledger,
            exponents=fallback_ledger,
        ),
        "transportAndCubicSeparation": record(
            transport_sign == 1
            and transport_retained
            and cubic_sum_controlled,
            transportSignOnB14Right=transport_sign,
            transportRetained=transport_retained,
            pFPlusPBControlledByPayment=cubic_sum_controlled,
        ),
        "exactShearPaymentRateD22": record(
            pb_rate == expected_pb_rate and pb_rate > 0,
            pBScale=exponent_row(L=pb_l, R=pb_r, omega=pb_omega),
            value=rat(pb_rate),
            expected=rat(expected_pb_rate),
        ),
        "smallPaymentAndInteractionBoundary": record(
            small_payment_leq_one
            and not linear_term_absorbed
            and (interaction_pb_power, interaction_pf_power,
                 interaction_payment_power) == (F(1), F(2), F(-2)),
            smallPaymentCondition="P_R^M <= 1",
            linearTermAbsorbedOnFrozenBranch=linear_term_absorbed,
            interactionPowers={
                "pB": rat(interaction_pb_power),
                "pF": rat(interaction_pf_power),
                "payment": rat(interaction_payment_power),
            },
        ),
        "modalEquationAndEnergy": record(
            modal == {
                "diffusionCoefficient": -1,
                "horizontalLaplacianCoefficient": 1,
                "imaginaryShearCoefficient": 1,
                "energyTimeDerivative": F(1, 2),
                "verticalDissipationSign": 1,
                "horizontalDissipationSign": 1,
                "shearRealPart": 0,
                "normDecayCoefficient": 1,
            },
            coefficients={
                key: rat(value) if isinstance(value, F) else value
                for key, value in modal.items()
            },
            normDecay="exp[-n^2(t-s)]",
            squaredNormDecay="exp[-2n^2(t-s)]",
        ),
        "verticalZeroModeObstruction": record(
            zero_mode_obstruction
            and r"F_m(t,x_3)=e^{-m^2t}\sin(mx_3)" in text
            and "arbitrarily large vertical gradient" in text,
            horizontalFrequencyAloneSufficient=False,
        ),
        "gradientIdentity": record(
            gradient_forcing_sign == -1
            and gradient_dissipation == "Laplacian",
            forcingSign=gradient_forcing_sign,
            dissipation=gradient_dissipation,
            dissipationNorm="||Delta_23 F||_2^2",
        ),
        "transitionBandGeometry": record(
            (transition_l, transition_r, full_collar_l, full_collar_r)
            == (F(1), F(3), F(2), F(3)),
            transitionVolume=exponent_row(L=transition_l, R=transition_r),
            fullCollarVolume=exponent_row(L=full_collar_l, R=full_collar_r),
            relativeLPower="-1",
        ),
        "shortBlocksAndIntermediateGap": record(
            block_count_r == -1
            and critical_k_r == F(-3, 2)
            and critical_rate == F(27, 80000)
            and gap == expected_gap
            and gap > 0,
            blockCountRPower=rat(block_count_r),
            criticalKRPower=rat(critical_k_r),
            criticalRate=rat(critical_rate),
            gap=rat(gap),
            expectedGap=rat(expected_gap),
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags
            and len(set(tags)) == 23
            and not (set(references) - set(tags))
            and display_open == display_close == 23,
            tags=tags,
            unresolvedLocalReferences=sorted(set(references) - set(tags)),
            displayOpen=display_open,
            displayClose=display_close,
        ),
        "externalReferenceBoundary": record(
            all(label in text and label in b_tags for label in ("B.14", "B.38"))
            and "R0.75C" in text
            and all(
                label in set(re.findall(r"\\tag\{(C\.[^}]+)\}", c_text))
                for label in ("C.13", "C.14", "C.15", "C.35")
            )
            and "R075C_BACKGROUND_SHEAR_DISSIPATION_PAID" in c_text,
            B14Resolved="B.14" in b_tags,
            B38Resolved="B.38" in b_tags,
            R075CSourceBound=True,
        ),
        "requiredTextualSentinels": record(
            all(
                re.sub(r"\s+", " ", token) in flat_text
                for token in required_tokens
            ),
            requiredCount=len(required_tokens),
        ),
        "analyticBlockersRetained": record(
            route_state["exactPassiveFallbackProved"]
            and route_state["smallPaymentFallbackProved"]
            and not route_state["frozenLargePaymentBranchClosed"]
            and not route_state["interactionConditionProved"]
            and route_state["transportRetained"]
            and not route_state["highFrequencyLocalCaptureProved"]
            and not route_state["intermediateBandClosed"]
            and not route_state["commutatorsClosed"]
            and route_state["periodizationRetained"],
            state=route_state,
        ),
        "claimBoundary": record(
            route_state["exactPassiveFallbackProved"]
            and route_state["smallPaymentFallbackProved"]
            and not route_state["frozenLargePaymentBranchClosed"]
            and not route_state["interactionConditionProved"]
            and not route_state["unconditionalLowFrequencyLemma"]
            and not route_state["exactCounterexampleConstructed"]
            and not route_state["fullClockExtractionProved"]
            and not route_state["clayClaim"]
            and "not yet an unconditional low-frequency lemma" in text
            and "NO EXACT COUNTEREXAMPLE CONSTRUCTED" in text
            and "No such uniform interaction bound is presently proved" in text
            and "proves neither complete-clock extraction" in text
            and r"\mathbf{NOT\ CLAY}" in text,
            state=route_state,
        ),
        "textSafety": record(
            not any(ord(char) < 32 and char not in "\n\t" for char in text),
            validUtf8=True,
            controlCharacters=0,
        ),
    }

    verdict = "PASS" if all(item["pass"] for item in checks.values()) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "mutation": MUTATION or None,
        "assertionsPassed": sum(item["pass"] for item in checks.values()),
        "assertionsTotal": len(checks),
        "checks": checks,
        "exactValues": {
            "rho": rat(rho),
            "cGamma": rat(c_gamma),
            "klowRate": rat(klow_rate),
            "expectedKlowRate": rat(expected_klow_rate),
            "criticalRate": rat(critical_rate),
            "intermediateGap": rat(gap),
            "expectedIntermediateGap": rat(expected_gap),
            "shearPaymentRate": rat(pb_rate),
            "expectedShearPaymentRate": rat(expected_pb_rate),
        },
        "powerLedger": power_ledger,
        "fallbackLedger": fallback_ledger,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "dependencyBoundary": (
            "R0.75D has no embedded frozen-source table; B/C are bound "
            "certificate-side only, and any observed dependency drift fails"
        ),
        "boundary": (
            "FINITE EXACT ARITHMETIC/STRUCTURE FOR A ROUTE SCREEN ONLY; "
            "exact passive fallback is P^(2/3)+P and pays only the "
            "small-payment regime; the frozen branch has P to infinity; "
            "low-frequency payment remains conditional; intermediate band, "
            "commutators, high-frequency local capture, and periodic-weight "
            "leakage remain OPEN; no exact counterexample; NOT CLAY"
        ),
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    dependency_lines = "\n".join(
        f"- {path}: {row['observedSha256']} (certificate-side binding)"
        for path, row in dependency_rows.items()
    )
    OUT_REPORT.write_text(
        f"""# R0.75D reproducibility certificate report

- Verdict: **{verdict}**
- Assertions: {payload['assertionsPassed']}/{payload['assertionsTotal']}
- Main SHA-256: {actual_main_hash}
- Tags: {len(tags)} unique; displays: {display_open}/{display_close}
- K-low exact rate: {klow_rate}
- Intermediate-band exact gap: {gap}
- Frozen shear-payment rate: {pb_rate}
- Negative mutations declared: {len(NEGATIVE_MUTATIONS)}

## Certificate-side dependencies

The frozen main note contains no source-hash table. The certificate does not
pretend otherwise and does not require table rows to exist in the main file.
It independently binds only the two directly invoked B/C notes:

{dependency_lines}

## Certified boundary

The certificate recomputes the D.4--D.7 Hölder, R, L, omega, and K powers;
the K-low threshold and exact rate; the horizontal modal energy signs; the
vertical zero-mode obstruction; the D.10--D.11 sign and Laplacian
dissipation; the transition/full-collar volumes; and the block threshold
and exact intermediate-band gap. It also recomputes the D.16--D.23
normalizations, cutoff and mixed Hölder powers, shear-payment rate, the
small-payment direction, and the interaction-condition homogeneity. It
checks all 23 tags, local and external B/C references, displays, control
characters, and required status text.

This is finite exact arithmetic and structural verification of a route
screen. The exact passive fallback is of size P^(2/3)+P and pays the
small-payment regime only. The frozen branch has P tending to infinity, so
the linear term is not absorbed. Low-frequency payment remains conditional.
The interaction condition, high-frequency local capture, intermediate band,
commutators, projection leakage, and periodic weights remain OPEN. No exact
counterexample or complete-clock result is certified. NOT CLAY.
""",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "verdict": verdict,
                "assertions": len(checks),
                "mutation": MUTATION or None,
            },
            sort_keys=True,
        )
    )
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
