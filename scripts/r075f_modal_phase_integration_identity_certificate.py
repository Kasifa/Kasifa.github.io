#!/usr/bin/env python3
"""Fail-closed finite certificate for the frozen R0.75F identity."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "research/r075f_modal_phase_integration_identity.md"
PRIMARY_AUDIT = ROOT / "research/r075f_modal_phase_integration_identity_primary_audit.md"
REPORT_SOURCE = ROOT / "research/r075f_report-source.md"
FIXTURES = ROOT / "scripts/r075f_modal_phase_integration_identity_fixtures.json"
EXPECTED = ROOT / "scripts/r075f_modal_phase_integration_identity_expected.json"
OUT_JSON = Path(os.environ.get(
    "R075F_JSON",
    ROOT / "research/r075f_modal_phase_integration_identity_certificate.json",
))
OUT_REPORT = Path(os.environ.get(
    "R075F_REPORT",
    ROOT / "research/r075f_modal_phase_integration_identity_certificate_report.md",
))
MUTATION = os.environ.get("R075F_MUTATION", "")
SCHEMA = "r075f-modal-phase-integration-identity-certificate-v1"

FROZEN_SOURCES = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075e_horizontal_cross_mode_flux_reduction.md":
        "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075f_modal_phase_integration_identity.md":
        "f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440",
    "research/r075f_modal_phase_integration_identity_primary_audit.md":
        "4320ac5544b51888eb8088db98e500a9877ecfe9a984f156783cac096a27c99a",
    "research/r075f_report-source.md":
        "3838603ea143b2efe1e96995fac34d7e8565211dc91dd244ab01cf6d526f3481",
}
FIXTURES_SHA256 = "0ce9b3bf060f4b38fe497be7bcdad3d1bdbd51ea27ff9aab146c8b10f5a0aced"
EXPECTED_SHA256 = "3946cb2cc992f4d1e55b88a7be9b7ecd8529e76a437093af6583f8fdacf2ddc9"

NEGATIVE_MUTATIONS = (
    "source_drift",
    "audit_drift",
    "report_source_drift",
    "dependency_drift",
    "dependency_table_missing",
    "fixture_drift",
    "expected_drift",
    "tag",
    "reference",
    "display",
    "control",
    "mode_n_shear_sign",
    "mode_m_shear_sign",
    "ell_sign",
    "product_cross_two",
    "phase_lhs_sign",
    "no_division",
    "period_factor",
    "endpoint_half",
    "dissipation_factor",
    "gradient_nm_sign",
    "cutoff_ell_sign",
    "eta_initial",
    "eta_terminal",
    "time_ibp_sign",
    "vertical_ibp_sign",
    "square_decomposition",
    "transport_reconstruction",
    "cancellation_residual",
    "diagonal_identity",
    "fejer_even_allowed",
    "fejer_count",
    "fejer_fourth",
    "fejer_weight_bound",
    "fejer_mean",
    "fejer_ratio_n3",
    "fejer_ratio_n5",
    "fejer_ratio_n7",
    "fejer_divergence",
    "counterexample_claim",
    "e24_closed",
    "full_clock",
    "clay",
)

Q = Fraction
Z = tuple[Q, Q]
ZERO: Z = (Q(0), Q(0))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: str | int) -> Q:
    return Q(value)


def z(value: list[str] | tuple[Q, Q]) -> Z:
    if isinstance(value, tuple):
        return value
    return (q(value[0]), q(value[1]))


def zadd(*values: Z) -> Z:
    return (sum(value[0] for value in values), sum(value[1] for value in values))


def zscale(scale: Q, value: Z) -> Z:
    return (scale * value[0], scale * value[1])


def zmul(left: Z, right: Z) -> Z:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def zconj(value: Z) -> Z:
    return (value[0], -value[1])


def imul(scale: Q, value: Z) -> Z:
    return (-scale * value[1], scale * value[0])


def qtext(value: Q) -> str:
    return str(value)


def zjson(value: Z) -> list[str]:
    return [qtext(value[0]), qtext(value[1])]


def padd(*values: Z) -> Z:
    """Add formal a+b*p polynomials, represented by rational pairs."""
    return zadd(*values)


def pscale(scale: Q, value: Z) -> Z:
    return zscale(scale, value)


def pjson(value: Z) -> list[str]:
    return zjson(value)


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075F_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    flat_text = re.sub(r"\s+", " ", text)
    scan_text = text + ("\x01" if MUTATION == "control" else "")
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))

    source_expectations = dict(FROZEN_SOURCES)
    if MUTATION == "source_drift":
        source_expectations["research/r075f_modal_phase_integration_identity.md"] = "0" * 64
    if MUTATION == "audit_drift":
        source_expectations[
            "research/r075f_modal_phase_integration_identity_primary_audit.md"
        ] = "0" * 64
    if MUTATION == "report_source_drift":
        source_expectations["research/r075f_report-source.md"] = "0" * 64
    if MUTATION == "dependency_drift":
        source_expectations[
            "research/r075b_bulk_clock_outer_padding_gate.md"
        ] = "0" * 64
    source_rows = {
        path: {
            "expectedSha256": digest,
            "observedSha256": sha256(ROOT / path),
        }
        for path, digest in sorted(source_expectations.items())
    }

    fixture_expected_hash = "0" * 64 if MUTATION == "fixture_drift" else FIXTURES_SHA256
    expected_expected_hash = "0" * 64 if MUTATION == "expected_drift" else EXPECTED_SHA256
    fixture_hash = sha256(FIXTURES)
    expected_hash = sha256(EXPECTED)

    # F.5--F.8: generic rational complex point data, with the two modal
    # equations evaluated independently before the product identity.
    case = fixtures["productCase"]
    n = int(case["n"])
    m = int(case["m"])
    b = q(case["b"])
    fn = z(case["fN"])
    fnp = z(case["fNPrime"])
    fnpp = z(case["fNSecond"])
    fm = z(case["fM"])
    fmp = z(case["fMPrime"])
    fmpp = z(case["fMSecond"])
    cfm, cfmp, cfmpp = zconj(fm), zconj(fmp), zconj(fmpp)

    n_shear_sign = 1 if MUTATION == "mode_n_shear_sign" else -1
    m_shear_sign = -1 if MUTATION == "mode_m_shear_sign" else 1
    dtfn = zadd(fnpp, zscale(-n * n, fn), imul(n_shear_sign * n * b, fn))
    dtcfm = zadd(cfmpp, zscale(-m * m, cfm), imul(m_shear_sign * m * b, cfm))
    g = zmul(fn, cfm)
    dtg = zadd(zmul(dtfn, cfm), zmul(fn, dtcfm))
    cross_factor = 1 if MUTATION == "product_cross_two" else 2
    cross = zmul(fnp, cfmp)
    gsecond = zadd(zmul(fnpp, cfm), zscale(cross_factor, cross), zmul(fn, cfmpp))
    ell = n - m if MUTATION == "ell_sign" else m - n
    lhs_sign = -1 if MUTATION == "phase_lhs_sign" else 1
    phase_lhs = imul(lhs_sign * ell * b, g)
    phase_rhs = zadd(
        dtg,
        zscale(-1, gsecond),
        zscale(2, cross),
        zscale(n * n + m * m, g),
    )
    product_observed = {
        "ell": ell,
        "nm": n * m,
        "dtFN": zjson(dtfn),
        "dtConjugateFM": zjson(dtcfm),
        "g": zjson(g),
        "dtG": zjson(dtg),
        "gSecond": zjson(gsecond),
        "phaseLhs": zjson(phase_lhs),
        "phaseRhs": zjson(phase_rhs),
    }
    no_division = (
        MUTATION != "no_division"
        and "No division by \\(b\\) or \\(\\ell\\) occurs." in text
    )

    # F.9--F.18: exact integrated moments for one ordered pair and its
    # conjugate reverse. All reported forms are normalized by pi.
    moment = fixtures["phaseMomentCase"]
    primary = moment["primaryOrderedPair"]
    endpoint = z(primary["endpoint"])
    eta_prime = z(primary["etaPrime"])
    xi_second = z(primary["xiSecond"])
    mass = z(primary["mass"])
    vertical_gradient = z(primary["verticalGradient"])
    mn = int(moment["n"]) * int(moment["m"])
    mell = (
        int(moment["n"]) - int(moment["m"])
        if MUTATION == "ell_sign"
        else int(moment["m"]) - int(moment["n"])
    )
    eta_initial = q(moment["etaAtInitial"])
    eta_terminal = q(moment["etaAtTerminal"])
    if MUTATION == "eta_initial":
        eta_initial = Q(1)
    if MUTATION == "eta_terminal":
        eta_terminal = Q(0)

    period_over_pi = Q(1) if MUTATION == "period_factor" else Q(2)
    half_energy = Q(1) if MUTATION == "endpoint_half" else Q(1, 2)
    endpoint_factor = half_energy * period_over_pi
    cutoff_factor = half_energy * period_over_pi
    dissipation_factor = (
        Q(1) if MUTATION == "dissipation_factor" else period_over_pi
    )
    gradient_nm = -mn if MUTATION == "gradient_nm_sign" else mn
    cutoff_ell_square_sign = 1 if MUTATION == "cutoff_ell_sign" else -1

    time_sign = 1 if MUTATION == "time_ibp_sign" else -1
    vertical_sign = 1 if MUTATION == "vertical_ibp_sign" else -1
    decomposition_mass = (
        mell * mell - 2 * mn
        if MUTATION == "square_decomposition"
        else mell * mell + 2 * mn
    )
    single_transport = zadd(
        zscale(eta_terminal, endpoint),
        zscale(time_sign, eta_prime),
        zscale(vertical_sign, xi_second),
        zscale(decomposition_mass, mass),
        zscale(2, vertical_gradient),
    )
    endpoint_off = endpoint_factor * 2 * endpoint[0]
    cutoff_off = cutoff_factor * 2 * (
        eta_prime[0] + xi_second[0]
        + cutoff_ell_square_sign * mell * mell * mass[0]
    )
    dissipation_off = dissipation_factor * 2 * (
        vertical_gradient[0] + gradient_nm * mass[0]
    )
    transport_multiplier = 2 if MUTATION == "transport_reconstruction" else 1
    transport = transport_multiplier * 2 * single_transport[0]
    reconstructed = endpoint_off - cutoff_off + dissipation_off
    cancellation_remainder = (
        transport - reconstructed + (Q(1) if MUTATION == "cancellation_residual" else 0)
    )
    diagonal_direct = MUTATION != "diagonal_identity"
    normalization_observed = {
        "horizontalPeriodOverPi": qtext(period_over_pi),
        "endpointHalfEnergyFactorOverPi": qtext(endpoint_factor),
        "cutoffHalfEnergyFactorOverPi": qtext(cutoff_factor),
        "dissipationPeriodFactorOverPi": qtext(dissipation_factor),
        "horizontalGradientMultiplier": qtext(gradient_nm),
    }
    phase_observed = {
        "ell": mell,
        "ellSquared": mell * mell,
        "nm": mn,
        "nSquaredPlusMSquared": decomposition_mass,
        "singlePairTOverPiBeforeRealSum": zjson(single_transport),
        "endpointOffOverPi": qtext(endpoint_off),
        "cutoffOffOverPi": qtext(cutoff_off),
        "dissipationOffOverPi": qtext(dissipation_off),
        "transportOverPi": qtext(transport),
        "endpointMinusCutoffPlusDissipationOverPi": qtext(reconstructed),
        "postSubstitutionOffDiagonalRemainderOverPi": qtext(cancellation_remainder),
    }

    # A genuine two-mode solution, evaluated in Q[p] with p=pi^-2.
    # Here f_1=e^(-2t)e^(-i*pi*t/2)e^(ix3), f_-1=conj(f_1),
    # eta=t*e^(4(t-1)), Xi_0=1/2 and Xi_{+/-2}=e^(+/-2ix3)/4.
    # Dividing every row by Kq (K=2*pi^2, q=e^-4) leaves linear
    # polynomials a+b*p. Transport is integrated directly from i*ell*b*g.
    closed = fixtures["closedSolutionCase"]
    cn = int(closed["n"])
    cm = int(closed["m"])
    cell = cn - cm if MUTATION == "ell_sign" else cm - cn
    cb_over_pi = q(closed["bOverPi"])
    decay = q(closed["decayRate"])
    eta_rate = q(closed["etaExponentialRate"])
    wave_n = int(closed["x3WaveN"])
    wave_m = int(closed["x3WaveM"])
    elementary = closed["elementaryIntegrals"]
    int_cos = z(elementary["integralCosPiT"])
    int_t_cos = z(elementary["integralTCosPiT"])
    pi_int_t_sin = z(elementary["piTimesIntegralTSinPiT"])

    closed_endpoint_diag = z(["1", "0"])
    closed_endpoint_off = z(["-1/2", "0"])
    closed_cutoff_diag = z(["3", "0"])
    cutoff_time_coefficient = (
        eta_rate
        - cell * cell
        + (cell * cell if MUTATION == "cutoff_ell_sign" else -cell * cell)
    )
    closed_cutoff_off = pscale(
        Q(1, 2),
        padd(int_cos, pscale(cutoff_time_coefficient, int_t_cos)),
    )
    closed_dissipation_diag = z(["2", "0"])
    vertical_multiplier = wave_n * wave_m
    closed_dissipation_off = pscale(
        vertical_multiplier + (
            -cn * cm if MUTATION == "gradient_nm_sign" else cn * cm
        ),
        int_t_cos,
    )
    direct_transport_sign = -1 if MUTATION == "phase_lhs_sign" else 1
    direct_transport_factor = (
        2 if MUTATION == "transport_reconstruction" else 1
    )
    closed_transport_direct = pscale(
        direct_transport_factor * direct_transport_sign * Q(cell) * cb_over_pi / 2,
        pi_int_t_sin,
    )
    closed_left = padd(
        closed_endpoint_diag,
        closed_endpoint_off,
        closed_dissipation_diag,
        closed_dissipation_off,
    )
    closed_right = padd(
        closed_cutoff_diag,
        closed_cutoff_off,
        closed_transport_direct,
    )

    closed_time_endpoint = pscale(eta_terminal, closed_endpoint_off)
    closed_time_eta_prime = pscale(
        Q(1, 2),
        padd(int_cos, pscale(eta_rate, int_t_cos)),
    )
    closed_time_direct = pscale(
        Q(1, 2),
        padd(
            pscale(-2 * decay, int_t_cos),
            pscale(direct_transport_sign * Q(cell) * cb_over_pi, pi_int_t_sin),
        ),
    )
    closed_time_endpoint_minus_eta = padd(
        closed_time_endpoint,
        pscale(time_sign, closed_time_eta_prime),
    )
    g_wave = wave_n - wave_m
    closed_vertical_left = pscale(
        Q(-vertical_sign * g_wave * g_wave, 2),
        int_t_cos,
    )
    xi_wave = cell
    closed_vertical_right = pscale(
        Q(-vertical_sign * xi_wave * xi_wave, 2),
        int_t_cos,
    )
    closed_phase_twice_gradient = pscale(
        vertical_multiplier,
        int_t_cos,
    )
    closed_mass_multiplier = (
        cn * cn - cm * cm
        if MUTATION == "square_decomposition"
        else cn * cn + cm * cm
    )
    closed_phase_mass = pscale(
        Q(closed_mass_multiplier, 2),
        int_t_cos,
    )
    closed_phase_sum = padd(
        closed_time_direct,
        closed_vertical_left,
        closed_phase_twice_gradient,
        closed_phase_mass,
    )
    closed_f17_right = padd(
        closed_endpoint_off,
        pscale(-1, closed_cutoff_off),
        closed_dissipation_off,
    )
    closed_f17_residual = padd(
        closed_transport_direct,
        pscale(-1, closed_f17_right),
        z(["1", "0"]) if MUTATION == "cancellation_residual" else ZERO,
    )
    closed_f18_left = padd(closed_endpoint_diag, closed_dissipation_diag)
    closed_f18_right = (
        z(["0", "0"]) if MUTATION == "diagonal_identity" else closed_cutoff_diag
    )
    closed_observed = {
        "endpointDiag": pjson(closed_endpoint_diag),
        "endpointOff": pjson(closed_endpoint_off),
        "cutoffDiag": pjson(closed_cutoff_diag),
        "cutoffOff": pjson(closed_cutoff_off),
        "dissipationDiag": pjson(closed_dissipation_diag),
        "dissipationOff": pjson(closed_dissipation_off),
        "transportDirect": pjson(closed_transport_direct),
        "localEnergyLeft": pjson(closed_left),
        "localEnergyRight": pjson(closed_right),
        "timeDerivativeDirect": pjson(closed_time_direct),
        "timeEndpoint": pjson(closed_time_endpoint),
        "timeEtaPrime": pjson(closed_time_eta_prime),
        "timeEndpointMinusEtaPrime": pjson(closed_time_endpoint_minus_eta),
        "verticalIbpLeft": pjson(closed_vertical_left),
        "verticalIbpRight": pjson(closed_vertical_right),
        "phaseTimeRow": pjson(closed_time_direct),
        "phaseMinusGSecondRow": pjson(closed_vertical_left),
        "phaseTwiceGradientRow": pjson(closed_phase_twice_gradient),
        "phaseMassRow": pjson(closed_phase_mass),
        "phaseRowsSum": pjson(closed_phase_sum),
        "f17Right": pjson(closed_f17_right),
        "f17Residual": pjson(closed_f17_residual),
        "f18Left": pjson(closed_f18_left),
        "f18Right": pjson(closed_f18_right),
    }

    # F.19--F.23: count every ordered pair in D_N * conjugate(D_N).
    ns = list(fixtures["fejerOddN"])
    if MUTATION == "fejer_even_allowed":
        ns.append(4)
    fejer_rows: dict[str, dict[str, Any]] = {}
    for current_n in ns:
        half = (current_n - 1) // 2
        modes = list(range(-half, half + 1))
        counts = {
            difference: sum(
                1 for left in modes for right in modes
                if left - right == difference
            )
            for difference in range(-(current_n - 1), current_n)
        }
        if MUTATION == "fejer_count" and current_n == 3:
            counts[0] += 1
        count_values = [counts[key] for key in sorted(counts)]
        fourth = sum(value * value for value in count_values)
        if MUTATION == "fejer_fourth" and current_n == 5:
            fourth += 1
        x_mean = Q(len(modes), current_n * current_n)
        a_squared_mean = Q(len(modes), current_n)
        if MUTATION == "fejer_mean" and current_n == 7:
            x_mean += Q(1, 7)
        localized = Q(fourth, current_n ** 3)
        ratio = localized / (x_mean * a_squared_mean)
        if MUTATION == f"fejer_ratio_n{current_n}":
            ratio += 1
        weight_bound = (
            False if MUTATION == "fejer_weight_bound" and current_n == 3
            else len(modes) == current_n
        )
        fejer_rows[str(current_n)] = {
            "differenceCounts": count_values,
            "fourthMoment": qtext(Q(fourth)),
            "xMean": qtext(x_mean),
            "aSquaredMean": qtext(a_squared_mean),
            "localizedMean": qtext(localized),
            "ratio": qtext(ratio),
            "odd": current_n % 2 == 1,
            "realSymmetric": modes == [-value for value in reversed(modes)],
            "weightBoundByTriangle": weight_bound,
        }
    divergence_leading_coefficient = (
        Q(-2, 3) if MUTATION == "fejer_divergence" else Q(2, 3)
    )

    tags = re.findall(r"\\tag\{(F\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("F.1")
    references = [
        "F." + value for value in re.findall(r"\(F\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("F.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"F.{index}" for index in range(1, 24)]

    dependency_table_present = all(
        any(path in line and FROZEN_SOURCES[path] in line for line in text.splitlines())
        for path in (
            "research/r075b_bulk_clock_outer_padding_gate.md",
            "research/r075e_horizontal_cross_mode_flux_reduction.md",
        )
    )
    if MUTATION == "dependency_table_missing":
        dependency_table_present = False

    required_tokens = (
        r"\ell=m-n",
        r"i\ell b g_{nm}",
        r"+2f_n'\overline{f_m}'",
        r"n^2+m^2=(m-n)^2+2nm=\ell^2+2nm",
        r"\mathcal T_\xi =\mathcal E_{\rm off} -\mathcal A_{\rm off} +\mathcal D_{\rm off}",
        r"\mathcal E_{\rm diag}+\mathcal D_{\rm diag} =\mathcal A_{\rm diag}",
        r"\langle h\rangle:=\frac1{2\pi}",
        r"0\le X_N\le1",
        r"\frac{2N^3+N}{3}",
        r"\frac{2N+N^{-1}}3\longrightarrow\infty",
        "not a counterexample to the R0.75E target",
        "None of these is proved here.",
        r"\mathbf{NOT\ CLAY}",
    )

    audit_text = PRIMARY_AUDIT.read_text(encoding="utf-8")
    boundary = {
        "positivityOnlyComparisonRuledOut": True,
        "frozenCollarCounterexample": MUTATION == "counterexample_claim",
        "arbitraryRealE24Proved": MUTATION == "e24_closed",
        "completeClockProved": MUTATION == "full_clock",
        "clayClaim": MUTATION == "clay",
    }

    checks = {
        "allFrozenSourceBindings": record(
            all(row["expectedSha256"] == row["observedSha256"]
                for row in source_rows.values()),
            sources=source_rows,
        ),
        "fixtureAndExpectedBindings": record(
            fixture_hash == fixture_expected_hash
            and expected_hash == expected_expected_hash
            and fixtures["schema"] ==
                "r075f-modal-phase-integration-identity-fixtures-v1"
            and expected["schema"] ==
                "r075f-modal-phase-integration-identity-expected-v1"
            and fixtures["frozenSources"] == FROZEN_SOURCES,
            fixtures={"expected": fixture_expected_hash, "observed": fixture_hash},
            expected={"expected": expected_expected_hash, "observed": expected_hash},
        ),
        "primaryAuditBindingAndStatus": record(
            FROZEN_SOURCES[
                "research/r075f_modal_phase_integration_identity.md"
            ] in audit_text
            and "Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0."
                in audit_text
            and "Equation tags F.1--F.23 are unique and consecutive." in audit_text,
        ),
        "mainDependencyTableBindings": record(dependency_table_present),
        "modalProductEquationF5ToF8": record(
            product_observed == expected["productCase"]
            and phase_lhs == phase_rhs
            and no_division,
            observed=product_observed,
        ),
        "piAndGradientNormalizationF9ToF13": record(
            normalization_observed == expected["normalization"],
            observed=normalization_observed,
        ),
        "endpointConditionsAndIntegrationByPartsF14F15": record(
            eta_initial == 0
            and eta_terminal == 1
            and time_sign == -1
            and vertical_sign == -1,
            etaInitial=qtext(eta_initial),
            etaTerminal=qtext(eta_terminal),
            timeDerivativeCutoffSign=time_sign,
            verticalSecondDerivativeCutoffSign=vertical_sign,
        ),
        "phaseReconstructionF16F17": record(
            phase_observed == expected["phaseMomentCase"]
            and transport == reconstructed,
            observed=phase_observed,
        ),
        "closedSolutionDirectIntegrationF5ToF18": record(
            closed_observed == expected["closedSolutionNormalizedByKq"]
            and closed_time_direct == closed_time_endpoint_minus_eta
            and closed_vertical_left == closed_vertical_right
            and closed_phase_sum == closed_transport_direct
            and closed_left == closed_right
            and closed_f17_residual == ZERO
            and closed_f18_left == closed_f18_right,
            formalVariable="p=pi^-2",
            normalizedRows=closed_observed,
        ),
        "completeCancellationAndDiagonalIdentityF18": record(
            cancellation_remainder == 0 and diagonal_direct,
            remainderOverPi=qtext(cancellation_remainder),
            diagonalIdentityDirectlyRecoverable=diagonal_direct,
        ),
        "fejerExactCountsF19ToF22": record(
            set(fejer_rows) == set(expected["fejer"])
            and all(
                row["differenceCounts"] ==
                    expected["fejer"][key]["differenceCounts"]
                and row["fourthMoment"] ==
                    expected["fejer"][key]["fourthMoment"]
                and row["xMean"] == expected["fejer"][key]["xMean"]
                and row["aSquaredMean"] ==
                    expected["fejer"][key]["aSquaredMean"]
                and row["localizedMean"] ==
                    expected["fejer"][key]["localizedMean"]
                and row["odd"] and row["realSymmetric"]
                and row["weightBoundByTriangle"]
                for key, row in fejer_rows.items()
            ),
            rows=fejer_rows,
        ),
        "fejerRatiosAndDivergenceF23": record(
            all(
                fejer_rows[key]["ratio"] == expected["fejer"][key]["ratio"]
                for key in expected["fejer"]
            )
            and divergence_leading_coefficient == Q(2, 3),
            ratios={key: row["ratio"] for key, row in fejer_rows.items()},
            leadingCoefficient=qtext(divergence_leading_coefficient),
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags
            and len(set(tags)) == 23
            and not (set(references) - set(tags))
            and display_open == display_close == 23,
            tags=tags,
            references=sorted(set(references)),
            displays={"open": display_open, "close": display_close},
        ),
        "formulaAndStatusSentinels": record(
            all(re.sub(r"\s+", " ", token) in flat_text for token in required_tokens),
        ),
        "claimBoundary": record(
            boundary["positivityOnlyComparisonRuledOut"]
            and not boundary["frozenCollarCounterexample"]
            and not boundary["arbitraryRealE24Proved"]
            and not boundary["completeClockProved"]
            and not boundary["clayClaim"],
            state=boundary,
        ),
        "utf8AndControlSafety": record(
            "\ufffd" not in scan_text
            and not any(
                ord(character) < 32 and character not in "\t\n"
                for character in scan_text
            ),
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
        "exactProductCase": product_observed,
        "exactPhaseFormsOverPi": phase_observed,
        "closedSolutionNormalizedByKq": closed_observed,
        "fejerRows": fejer_rows,
        "claimBoundary": boundary,
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )

    failed = [name for name, item in checks.items() if not item["pass"]]
    OUT_REPORT.write_text(
        "# R0.75F finite certificate report\n\n"
        f"- Verdict: **{verdict}**\n"
        f"- Assertions: {payload['assertions']['passed']}/{payload['assertions']['total']}\n"
        f"- Main SHA-256: {sha256(MAIN)}\n"
        f"- Fixture SHA-256: {fixture_hash}\n"
        f"- Expected SHA-256: {expected_hash}\n"
        f"- Failed checks: {'none' if not failed else '; '.join(failed)}\n\n"
        "The rational complex fixture verifies both modal equations, the product "
        "rule, ell=m-n, and F.8 without division by b or ell. The closed two-mode "
        "solution is then integrated independently in Q[p], p=pi^-2: transport "
        "comes directly from i*ell*b*g, both integration-by-parts identities are "
        "checked separately, and F.12, F.17, and F.18 have zero residual. The "
        "additional arbitrary moment fixture checks pi/2pi row normalization.\n\n"
        "For N=3,5,7 the producer enumerates every ordered difference pair, "
        "recomputes the fourth moment and normalized means, and obtains ratios "
        "19/9, 17/5, and 33/7. This rules out only the positivity-only uniform "
        "diagonal comparison. It is not a frozen-collar counterexample. E.24, "
        "complete clock, fixed deletion, suitable-weak transfer, and regularity "
        "remain OPEN. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "suite": "r075f-modal-phase-integration-identity",
        "verdict": verdict,
        "assertions": len(checks),
    }, sort_keys=True))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
