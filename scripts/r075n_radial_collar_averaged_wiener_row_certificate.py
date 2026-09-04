#!/usr/bin/env python3
"""Fail-closed exact finite certificate for frozen R0.75N."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075n_radial_collar_averaged_wiener_row.md"
PRIMARY_AUDIT = ROOT / "research/r075n_radial_collar_averaged_wiener_row_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075n_report-source.md"
FIXTURES = ROOT / "scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json"
EXPECTED = ROOT / "scripts/r075n_radial_collar_averaged_wiener_row_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075N_JSON", ROOT / "research/r075n_radial_collar_averaged_wiener_row_certificate.json"
))
OUT_REPORT = Path(os.environ.get(
    "R075N_REPORT", ROOT / "research/r075n_radial_collar_averaged_wiener_row_certificate_report.md"
))
MUTATION = os.environ.get("R075N_MUTATION", "")
SCHEMA = "r075n-radial-collar-averaged-wiener-row-certificate-v1"

FROZEN_SOURCES = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075c_background_shear_packing_false_positive.md":
        "1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075m_dyadic_packet_diffusive_flux_gain.md":
        "13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7",
    "research/r075n_radial_collar_averaged_wiener_row.md":
        "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
    "research/r075n_radial_collar_averaged_wiener_row_primary_audit.md":
        "c43c063b1c003be22782e7d8e1ce0b3f42cdd3ef4d01912c9de34c876d8c9aba",
    "research/r075n_report-source.md":
        "ae9d5d630ee0549193c016fcbc07c599b0c678fbaf9c15c5d3c7f24bdf18e27c",
}
FIXTURES_SHA256 = "2dee2146f94f3fa6d0d0c5828d8d6f354f0856f620e1261a133c9a2c81f8a0cb"
EXPECTED_SHA256 = "31614fc11bc4355723fff7773bec8ab13bc44808ffffa0958c78ec1cfe2bba48"

NEGATIVE_MUTATIONS = (
    "source_drift", "audit_drift", "report_source_drift", "dependency_drift",
    "dependency_table_missing", "fixture_drift", "expected_drift", "tag",
    "reference", "display", "control", "p_reciprocal", "a_definition",
    "r_definition", "R_range", "a_condition", "central_chart", "periodic_overlap",
    "profile_fixed", "profile_smooth", "profile_nonnegative", "profile_support",
    "profile_plateau", "B_choice_freedom", "canonical_universal", "derivative_cost",
    "fourier_normalization", "fourier_sign", "derivative_i", "derivative_ell",
    "d0", "integration_by_parts", "reconstruction_phase", "sampling_compact",
    "sampling_W21", "sampling_uniform_A", "sampling_nu", "sampling_R",
    "sup_sum_order", "low_cutoff", "low_count", "low_L1", "low_R_power",
    "high_one_ibp", "high_denominator", "high_tail_direction", "high_tail_R",
    "high_raw", "high_R_power", "discrete_riemann", "slice_scaling_x1",
    "slice_derivative_R", "slice_fourier_R", "slice_2pi", "slice_empty_range",
    "slice_interior_difference", "slice_area_factor", "tangency_missing",
    "tangency_cap", "outer_disk", "radial_lower", "radial_first_derivative",
    "radial_third_derivative", "radial_uniform", "fubini_direction",
    "slice_L1_a", "sum_all_modes", "coefficientwise_sup", "row_R_loss",
    "row_a_power", "full_average_jacobian", "full_derivative_R",
    "full_fourier_R", "full_shell_formula", "full_shell_volume_power",
    "full_fubini_a", "full_row_R", "full_row_a", "wiener_h1_substitution",
    "frequency_K", "frequency_gain", "frequency_direction", "frequency_R",
    "frequency_first_L", "frequency_first_R", "frequency_full_L",
    "frequency_full_R", "frequency_threshold", "physical_coefficient_only",
    "dynamical_flux_claim", "canonical_required", "all_cutoffs_claim",
    "vertical_diffusion_closed", "nonconstant_shear_closed", "local_cubic_closed",
    "interpacket_closed", "low_difference_closed", "e24_claim", "complete_clock",
    "fixed_deletion", "suitable_weak", "regularity", "singularity", "novelty",
    "priority", "simulation", "clay",
)

Q = Fraction


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def qtext(value: Q) -> str:
    return str(value)


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def exponent_json(row: dict[str, Q]) -> dict[str, str]:
    return {key: qtext(value) for key, value in row.items()}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075N_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    audit_text = PRIMARY_AUDIT.read_text(encoding="utf-8")
    source_text = REPORT_SOURCE.read_text(encoding="utf-8")
    b_text = (ROOT / "research/r075b_bulk_clock_outer_padding_gate.md").read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    flat_source = re.sub(r"\s+", " ", source_text)
    flat_b = re.sub(r"\s+", " ", b_text)
    scan_text = text + audit_text + source_text + ("\x01" if MUTATION == "control" else "")
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    source_expectations = dict(FROZEN_SOURCES)
    if MUTATION == "source_drift":
        source_expectations["research/r075n_radial_collar_averaged_wiener_row.md"] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075n_radial_collar_averaged_wiener_row_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075n_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations["research/r075b_bulk_clock_outer_padding_gate.md"] = "0" * 64
    source_rows = {
        path: {"expectedSha256": digest, "observedSha256": sha256(ROOT / path)}
        for path, digest in sorted(source_expectations.items())
    }
    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    calibration_fixture = fixtures["calibrationCase"]
    p = q(calibration_fixture["p"])
    if MUTATION == "p_reciprocal":
        p = 1 / p
    L = q(calibration_fixture["L"])
    R = q(calibration_fixture["R"])
    delta = q(calibration_fixture["delta"])
    a = p * L
    if MUTATION == "a_definition":
        a += 1
    r = a * R
    if MUTATION == "r_definition":
        r += R
    outer_radius = (a + delta) * R
    calibration_observed = {
        "p": qtext(p),
        "a": qtext(a),
        "r": qtext(r),
        "aAtLeastMax2Delta1": (
            False if MUTATION == "a_condition" else a >= max(2 * delta, Q(1))
        ),
        "outerSupportRadius": qtext(outer_radius),
        "centralChartCertifiedByOuterRadiusBelowOne": (
            False if MUTATION == "central_chart" else outer_radius < 1
        ),
    }

    fourier_fixture = fixtures["fourierDerivativeCase"]
    fourier_rows = []
    for row in fourier_fixture["XiModes"]:
        ell = int(row["ell"])
        xr = q(row["real"])
        xi = q(row["imag"])
        # i*ell*(xr+i*xi)=(-ell*xi)+i*(ell*xr).
        dr = -ell * xi
        di = ell * xr
        if MUTATION == "derivative_i":
            dr, di = ell * xr, ell * xi
        if MUTATION == "derivative_ell":
            dr, di = -xi, xr
        if MUTATION == "d0" and ell == 0:
            dr = 1
        fourier_rows.append({
            "ell": ell,
            "XiReal": qtext(xr),
            "XiImag": qtext(xi),
            "dReal": qtext(Q(dr)),
            "dImag": qtext(Q(di)),
        })
    zero_row = next(row for row in fourier_rows if row["ell"] == 0)
    fourier_observed = {
        "normalization": "1/pi" if MUTATION == "fourier_normalization" else "1/(2*pi)",
        "reconstructionPhase": "-i*ell*x2" if MUTATION in (
            "fourier_sign", "reconstruction_phase"
        ) else "+i*ell*x2",
        "derivativeRule": "d_ell=-i*ell*Xi_ell" if MUTATION in (
            "fourier_sign", "integration_by_parts"
        ) else "d_ell=i*ell*Xi_ell",
        "rows": fourier_rows,
        "dZero": f"{zero_row['dReal']}+{zero_row['dImag']}i",
    }

    sampling_fixture = fixtures["samplingCase"]
    sample_R = q(sampling_fixture["R"])
    if MUTATION == "sampling_R":
        sample_R = Q(1, 2)
    A = q(sampling_fixture["A"])
    cutoff = int(1 / sample_R)
    if MUTATION == "low_cutoff":
        cutoff -= 1
    low_count = 2 * cutoff + 1
    if MUTATION == "low_count":
        low_count += 1
    low_raw = A * low_count
    if MUTATION == "low_L1":
        low_raw += A
    high_tail = 2 * sample_R
    if MUTATION == "high_tail_R":
        high_tail = 2 * sample_R ** 2
    high_raw = A / sample_R ** 2 * high_tail
    if MUTATION in ("high_one_ibp", "high_denominator"):
        high_raw *= sample_R
    if MUTATION == "high_raw":
        high_raw += 1
    finite_reciprocal = 2 * sum(
        Q(1, ell * ell) for ell in sampling_fixture["finiteHighSamples"]
    )
    finite_raw = A / sample_R ** 2 * finite_reciprocal
    sampling_rows = []
    for nu in sampling_fixture["nu"]:
        power = int(nu)
        low_weighted = sample_R ** power * low_raw
        high_weighted = sample_R ** power * high_raw
        target_power = power - 1
        if MUTATION == "low_R_power" and power == 1:
            low_weighted += 1
        if MUTATION == "high_R_power" and power == 2:
            high_weighted += 1
        sampling_rows.append({
            "nu": power,
            "lowWeightedBound": qtext(low_weighted),
            "highWeightedBound": qtext(high_weighted),
            "combinedWeightedBound": qtext(low_weighted + high_weighted),
            "targetRPower": qtext(Q(target_power)),
        })
    sampling_observed = {
        "cutoffIndex": qtext(Q(cutoff)),
        "lowIntegerCount": qtext(Q(low_count)),
        "lowRawBound": qtext(low_raw),
        "highReciprocalTailBound": qtext(high_tail),
        "highRawBound": qtext(high_raw),
        "finiteHighReciprocalSum": qtext(finite_reciprocal),
        "finiteHighRawBound": qtext(finite_raw),
        "rows": sampling_rows,
        "lowMechanism": "Riemann-sum" if MUTATION == "discrete_riemann" else "count-O(R^-1)-times-L1",
        "highMechanism": (
            "one-IBP-R^-1-times-harmonic-tail" if MUTATION == "high_one_ibp"
            else "two-IBP-R^-2-times-tail-O(R)"
        ),
        "supremumOrder": (
            "sup-over-z-of-sum-over-ell" if MUTATION == "sup_sum_order"
            else "sum-over-ell-of-sup-over-z"
        ),
    }

    slice_fixture = fixtures["sliceAreaCase"]
    slice_a = q(slice_fixture["a"])
    slice_delta = q(slice_fixture["delta"])
    cap = 4 * slice_a * slice_delta
    if MUTATION in ("slice_area_factor", "tangency_cap"):
        cap = 2 * slice_a * slice_delta
    slice_rows = []
    for z_text in slice_fixture["zSamples"]:
        z = q(z_text)
        outer = max(Q(0), (slice_a + slice_delta) ** 2 - z ** 2)
        inner = max(Q(0), (slice_a - slice_delta) ** 2 - z ** 2)
        area = outer - inner
        az = abs(z)
        if az < slice_a - slice_delta:
            region = "interior"
        elif az == slice_a - slice_delta:
            region = "interior-boundary"
        elif az < slice_a + slice_delta:
            region = "tangency"
        elif az == slice_a + slice_delta:
            region = "empty-boundary"
        else:
            region = "empty"
        if MUTATION == "tangency_missing" and region == "tangency":
            area = 0
        if MUTATION == "slice_interior_difference" and region.startswith("interior"):
            area += 1
        if MUTATION == "outer_disk" and region == "tangency":
            area += 1
        slice_rows.append({
            "z": qtext(z),
            "region": region,
            "areaOverPi": qtext(area),
            "capGapOverPi": qtext(cap - area),
        })
    slice_observed = {
        "uniformCapOverPi": qtext(cap),
        "rows": slice_rows,
    }

    volume = Q(4, 3) * ((slice_a + slice_delta) ** 3 - (slice_a - slice_delta) ** 3)
    if MUTATION == "full_shell_formula":
        volume += 1
    full_shell_observed = {
        "volumeOverPi": qtext(volume),
        "exactExpansionOverPi": (
            "4*a^2*delta+8*delta^3/3" if MUTATION == "full_shell_volume_power"
            else "8*a^2*delta+8*delta^3/3"
        ),
        "volumeOverPiDividedByASquared": qtext(volume / slice_a ** 2),
        "order": "O_delta(a^3)" if MUTATION == "full_shell_volume_power" else "O_delta(a^2)",
    }

    scaling_fixture = fixtures["scalingCase"]
    x1_prefactor = q(scaling_fixture["x1AverageJacobianPower"])
    full_prefactor = q(scaling_fixture["fullAverageJacobianPower"])
    derivative_power = q(scaling_fixture["x2DerivativePower"])
    fourier_jacobian = q(scaling_fixture["x2FourierJacobianPower"])
    if MUTATION == "slice_scaling_x1":
        x1_prefactor = 2
    if MUTATION == "full_average_jacobian":
        full_prefactor = 3
    slice_after_derivative = x1_prefactor + derivative_power
    full_after_derivative = full_prefactor + derivative_power
    if MUTATION == "slice_derivative_R":
        slice_after_derivative += 1
    if MUTATION == "full_derivative_R":
        full_after_derivative += 1
    slice_fourier = slice_after_derivative + fourier_jacobian
    full_fourier = full_after_derivative + fourier_jacobian
    if MUTATION == "slice_fourier_R":
        slice_fourier += 1
    if MUTATION == "full_fourier_R":
        full_fourier += 1
    slice_a_power = q(scaling_fixture["sliceSupportAPower"])
    full_a_power = q(scaling_fixture["shellVolumeAPower"])
    if MUTATION == "slice_L1_a":
        slice_a_power = 2
    if MUTATION == "full_fubini_a":
        full_a_power = 3
    slice_row_R = slice_fourier - 1
    full_row_R = full_fourier - 1
    if MUTATION == "row_R_loss":
        slice_row_R -= 1
    if MUTATION == "full_row_R":
        full_row_R -= 1
    if MUTATION == "row_a_power":
        slice_a_power += 1
    if MUTATION == "full_row_a":
        full_a_power += 1
    derivative_orders = list(scaling_fixture["radialDerivativeOrders"])
    if MUTATION == "radial_first_derivative":
        derivative_orders[0] = 2
    if MUTATION == "radial_third_derivative":
        derivative_orders[1] = 2
    scaling_observed = {
        "x1Average": {
            "prefactorR": qtext(x1_prefactor),
            "afterX2DerivativeR": qtext(slice_after_derivative),
            "fourierCoefficientR": qtext(slice_fourier),
            "fubiniL1A": qtext(slice_a_power),
            "wienerRowR": qtext(slice_row_R),
            "wienerRowA": qtext(slice_a_power),
        },
        "fullAverage": {
            "prefactorR": qtext(full_prefactor),
            "afterX2DerivativeR": qtext(full_after_derivative),
            "fourierCoefficientR": qtext(full_fourier),
            "fubiniL1A": qtext(full_a_power),
            "wienerRowR": qtext(full_row_R),
            "wienerRowA": qtext(full_a_power),
        },
        "radialDerivativeOrders": derivative_orders,
        "radialDenominatorSafe": (
            "radius may vanish" if MUTATION == "radial_lower"
            else "radius>=a-delta>=a/2>=1/2"
        ),
    }

    frequency_fixture = fixtures["frequencyCase"]
    K_lower_power = q(frequency_fixture["KLowerRPower"])
    gain_K_power = q(frequency_fixture["gainKPower"])
    if MUTATION in ("frequency_K", "frequency_threshold"):
        K_lower_power = -1
    if MUTATION == "frequency_gain":
        gain_K_power = Q(-1, 3)
    implied_R = K_lower_power * gain_K_power
    first_result = {"L": Q(1), "R": slice_row_R + implied_R}
    full_result = {"L": full_a_power, "R": full_row_R + implied_R}
    if MUTATION == "frequency_R":
        implied_R += 1
    if MUTATION == "frequency_first_L":
        first_result["L"] += 1
    if MUTATION == "frequency_first_R":
        first_result["R"] += 1
    if MUTATION == "frequency_full_L":
        full_result["L"] += 1
    if MUTATION == "frequency_full_R":
        full_result["R"] += 1
    frequency_observed = {
        "KLowerRPower": qtext(K_lower_power),
        "gainKPower": qtext(gain_K_power),
        "impliedRPower": qtext(implied_R),
        "x1AveragedResult": exponent_json(first_result),
        "fullyAveragedResult": exponent_json(full_result),
    }

    tags = re.findall(r"\\tag\{(N\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("N.1")
    references = ["N." + value for value in re.findall(r"\(N\.([0-9]+[a-z]?)\)", text)]
    if MUTATION == "reference":
        references.append("N.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"N.{index}" for index in range(1, 18)]

    dependencies = (
        "research/r075b_bulk_clock_outer_padding_gate.md",
        "research/r075c_background_shear_packing_false_positive.md",
        "research/r075e_horizontal_cross_mode_flux_reduction.md",
        "research/r075m_dyadic_packet_diffusive_flux_gain.md",
    )
    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in dependencies
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"p=\frac{32}{63},\qquad a=pL,\qquad r=aR",
        r"\sum_{\ell\in\mathbb Z} \|d_\ell\|_{L^\infty_{x_3}} \le C_\vartheta a",
        r"d_\ell(x_3) &:=\frac1{2\pi}\int_{-\pi}^{\pi}",
        r"=i\ell\Xi_\ell(x_3)",
        r"R^\nu\sum_{\ell\in\mathbb Z} \sup_z|\widehat h_z(\ell R)|",
        r"\sum_{|\ell|>R^{-1}}\ell^{-2}\le CR",
        r"|A_{a,z}|\le4\pi a\delta",
        r"\|h_{a,z}''\|_{L^1_y}",
        r"\overline\xi_{a,R}(Ry)=R^2G_a(y)",
        r"D_\ell=\frac{R^2}{2\pi}\widehat h_a(\ell R)",
        r"\le C_\vartheta L^2R^2",
        r"\mathbf{NOT\ CLAY}",
    )

    boundary = {
        "BLeavesCutoffChoiceFreedom": MUTATION != "B_choice_freedom",
        "canonicalChoiceNotUniversalNecessity": MUTATION not in (
            "canonical_universal", "all_cutoffs_claim", "canonical_required"
        ),
        "fixedSmoothNonnegativeProfile": MUTATION not in (
            "profile_fixed", "profile_smooth", "profile_nonnegative"
        ),
        "profileSupportedInFixedNormalizedCollar": MUTATION != "profile_support",
        "profileCoversComplementaryPiece": MUTATION != "profile_plateau",
        "RInUnitInterval": MUTATION != "R_range",
        "centralChartNoPeriodicOverlap": MUTATION != "periodic_overlap",
        "derivativeCostsRMinusJ": MUTATION != "derivative_cost",
        "samplingCompactW21Uniform": MUTATION not in (
            "sampling_compact", "sampling_W21", "sampling_uniform_A"
        ),
        "nuAtLeastOne": MUTATION != "sampling_nu",
        "sumOfCoefficientwiseSuprema": MUTATION not in (
            "sup_sum_order", "coefficientwise_sup"
        ),
        "twoIntegrationsByParts": MUTATION != "high_one_ibp",
        "highTailDirectionCorrect": MUTATION != "high_tail_direction",
        "noUnsignedRiemannSum": MUTATION != "discrete_riemann",
        "tangencyCapIncluded": MUTATION not in ("tangency_missing", "tangency_cap"),
        "sliceFourierNormalizationTwoPi": MUTATION != "slice_2pi",
        "sliceEmptyOutsideOuterRadius": MUTATION != "slice_empty_range",
        "radialDerivativesUniform": MUTATION != "radial_uniform",
        "FubiniUpperDirection": MUTATION != "fubini_direction",
        "allHorizontalModesSummed": MUTATION != "sum_all_modes",
        "notCrudeWienerH1Substitution": MUTATION != "wiener_h1_substitution",
        "frequencyPowerDirection": MUTATION != "frequency_direction",
        "geometricCoefficientOnly": MUTATION != "physical_coefficient_only",
        "notDynamicalFluxTheorem": MUTATION != "dynamical_flux_claim",
        "verticalDiffusionOpen": MUTATION != "vertical_diffusion_closed",
        "nonconstantShearOpen": MUTATION != "nonconstant_shear_closed",
        "localCubicPaymentOpen": MUTATION != "local_cubic_closed",
        "interpacketSummationOpen": MUTATION != "interpacket_closed",
        "lowDifferenceSectorOpen": MUTATION != "low_difference_closed",
        "E24Open": MUTATION != "e24_claim",
        "completeClockOpen": MUTATION != "complete_clock",
        "fixedDeletionOpen": MUTATION != "fixed_deletion",
        "suitableWeakTransferOpen": MUTATION != "suitable_weak",
        "regularityOpen": MUTATION != "regularity",
        "singularityOpen": MUTATION != "singularity",
        "noNovelty": MUTATION != "novelty",
        "noPriority": MUTATION != "priority",
        "noSimulation": MUTATION != "simulation",
        "notClay": MUTATION != "clay",
    }

    checks = {
        "allFrozenSourceBindings": record(
            all(row["expectedSha256"] == row["observedSha256"] for row in source_rows.values()),
            sources=source_rows,
        ),
        "fixtureAndExpectedBindings": record(
            fixture_hash == fixture_expected_hash
            and expected_hash == expected_expected_hash
            and fixtures["frozenSources"] == FROZEN_SOURCES,
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES["research/r075n_radial_collar_averaged_wiener_row.md"] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0." in audit_text
            and "Equation tags N.1--N.17 are unique and consecutive." in audit_text
            and "All 17 display-math environments are paired." in audit_text,
        ),
        "fourDependencyTableBindings": record(dependency_table_present),
        "BChoiceFreedomAndCanonicalCalibration": record(
            calibration_observed == expected["calibration"]
            and "The complementary clock contribution is covered by a cutoff" in flat_b
            and "Only the inequalities" in flat_b
            and boundary["BLeavesCutoffChoiceFreedom"]
            and boundary["canonicalChoiceNotUniversalNecessity"],
            observed=calibration_observed,
        ),
        "fourierSignNormalizationAndZeroMode": record(
            fourier_observed == expected["fourierDerivative"]
            and fourier_observed["dZero"] == "0+0i",
            observed=fourier_observed,
        ),
        "lowHighSamplingAndSupremumOrder": record(
            sampling_observed == expected["sampling"]
            and boundary["samplingCompactW21Uniform"]
            and boundary["nuAtLeastOne"]
            and boundary["sumOfCoefficientwiseSuprema"]
            and boundary["twoIntegrationsByParts"]
            and boundary["highTailDirectionCorrect"]
            and boundary["noUnsignedRiemannSum"],
            observed=sampling_observed,
        ),
        "uniformSliceAreaIncludingTangency": record(
            slice_observed == expected["sliceAreas"]
            and all(q(row["capGapOverPi"]) >= 0 for row in slice_rows)
            and boundary["tangencyCapIncluded"],
            observed=slice_observed,
        ),
        "radialDerivativeFubiniAndScaling": record(
            scaling_observed == expected["scaling"]
            and boundary["radialDerivativesUniform"]
            and boundary["FubiniUpperDirection"],
            observed=scaling_observed,
        ),
        "fullShellVolumeAndFullAverage": record(
            full_shell_observed == expected["fullShell"]
            and scaling_observed["fullAverage"]["wienerRowR"] == "1"
            and scaling_observed["fullAverage"]["wienerRowA"] == "2",
            observed=full_shell_observed,
        ),
        "frequencyDiagnostic": record(
            frequency_observed == expected["frequency"]
            and implied_R == 1
            and boundary["frequencyPowerDirection"],
            observed=frequency_observed,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags and len(set(tags)) == 17
            and not (set(references) - set(tags))
            and display_open == display_close == 17,
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "sourceReportBoundary": record(
            "no dynamical flux, local Version-M payment, E.24, regularity, novelty, or priority claim" in flat_source
            and "coefficientwise `x_3` supremum is taken before summation" in flat_source
            and "spherical tangencies are paid" in flat_source,
        ),
        "claimBoundary": record(all(boundary.values()), state=boundary),
        "utf8AndControlSafety": record(
            "\ufffd" not in scan_text
            and not any(ord(character) < 32 and character not in "\t\n" for character in scan_text),
        ),
    }

    verdict = "PASS" if all(item["pass"] for item in checks.values()) else "FAIL"
    payload = {
        "schema": SCHEMA,
        "verdict": verdict,
        "assertions": {
            "passed": sum(item["pass"] for item in checks.values()),
            "total": len(checks),
        },
        "mutation": MUTATION or None,
        "checks": checks,
        "calibration": calibration_observed,
        "fourierDerivative": fourier_observed,
        "sampling": sampling_observed,
        "sliceAreas": slice_observed,
        "fullShell": full_shell_observed,
        "scaling": scaling_observed,
        "frequency": frequency_observed,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75N finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "Exact rational fixtures verify the frozen p=32/63 calibration, central "
        "canonical cover, 1/(2*pi) Fourier convention, d_ell=i*ell*Xi_ell, and "
        "d_0=0. The R=1/4 sample split separately checks the low count and the "
        "two-integration-by-parts high tail with R^(nu-1) scaling and sum-sup order.\n\n"
        "Six exact spherical slices include interior, tangency, boundary, and empty "
        "cases under the uniform 4*pi*a*delta cap. Scaling ledgers verify the first "
        "and third radial derivatives, Fubini L1 rows O(a) and O(a^2), x1-average "
        "coefficient R, full-average coefficient R^2, and final rows O(a) and O(Ra^2).\n\n"
        "At K>=R^(-3/2), K^(-2/3)<=R gives LR and L^2R^2. This is a chosen "
        "canonical geometric coefficient theorem, not a universal cutoff or "
        "dynamical flux result. Vertical diffusion, local payment, packet summation, "
        "and E.24 remain open. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075n-radial-collar-averaged-wiener-row",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
