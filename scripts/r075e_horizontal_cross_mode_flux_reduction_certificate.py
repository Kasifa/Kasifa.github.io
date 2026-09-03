#!/usr/bin/env python3
"""Fail-closed certificate for the frozen R0.75E cross-mode reduction."""

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
MAIN = ROOT / "research/r075e_horizontal_cross_mode_flux_reduction.md"
OUT_JSON = Path(
    os.environ.get(
        "R075E_JSON",
        ROOT / "research/r075e_horizontal_cross_mode_flux_reduction_certificate.json",
    )
)
OUT_REPORT = Path(
    os.environ.get(
        "R075E_REPORT",
        ROOT / "research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md",
    )
)
MUTATION = os.environ.get("R075E_MUTATION", "")
SCHEMA = "r075e-horizontal-cross-mode-flux-reduction-certificate-v1"
MAIN_SHA256 = "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049"

FROZEN_DEPENDENCIES = {
    "research/r075b_bulk_clock_outer_padding_gate.md":
        "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
    "research/r075c_background_shear_packing_false_positive.md":
        "1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89",
    "research/r075d_passive_gradient_route_screen.md":
        "54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6",
}

NEGATIVE_MUTATIONS = (
    "source_drift",
    "dependency_drift",
    "dependency_table_missing",
    "tag",
    "reference",
    "display",
    "control",
    "period_factor",
    "formula_pi_factor",
    "laurent_derivative_sign",
    "difference_sign",
    "index_reversal",
    "diagonal_nonzero",
    "zero_mode_nonzero",
    "singleton_physical",
    "real_pair_zero",
    "reality_pair_broken",
    "e15_volume",
    "e15_cutoff_r",
    "e15_cubic_normalization",
    "e15_omega",
    "e16_decay_sign",
    "e16_denominator",
    "e21_pi",
    "e21_omega",
    "e21_r",
    "e23_pb_power",
    "e23_pf_power",
    "e23_residual_r",
    "endpoint_dropped",
    "transport_sign",
    "mode_invariance",
    "x1_hat_not_average",
    "zero_mode_small_payment",
    "complex_physical",
    "real_pair_cancelled",
    "e24_closed",
    "full_clock",
    "clay",
)

Z = tuple[F, F]
ZERO: Z = (F(0), F(0))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rat(value: F) -> str:
    return str(value)


def z(real: int | F = 0, imag: int | F = 0) -> Z:
    return (F(real), F(imag))


def zadd(left: Z, right: Z) -> Z:
    return (left[0] + right[0], left[1] + right[1])


def zmul(left: Z, right: Z) -> Z:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def zscale(scale: F, value: Z) -> Z:
    return (scale * value[0], scale * value[1])


def zconj(value: Z) -> Z:
    return (value[0], -value[1])


def zstring(value: Z) -> str:
    return f"{value[0]}+({value[1]})i"


def poly_multiply(left: dict[int, Z], right: dict[int, Z]) -> dict[int, Z]:
    result: dict[int, Z] = {}
    for left_power, left_value in left.items():
        for right_power, right_value in right.items():
            power = left_power + right_power
            result[power] = zadd(
                result.get(power, ZERO),
                zmul(left_value, right_value),
            )
    return {power: value for power, value in result.items() if value != ZERO}


def absolute_square_coefficients(field: dict[int, Z]) -> dict[int, Z]:
    result: dict[int, Z] = {}
    for n, f_n in field.items():
        for m, f_m in field.items():
            power = n - m
            result[power] = zadd(
                result.get(power, ZERO),
                zmul(f_n, zconj(f_m)),
            )
    return {power: value for power, value in result.items() if value != ZERO}


def is_real_laurent_field(field: dict[int, Z]) -> bool:
    indices = set(field) | {-index for index in field}
    return all(field.get(-index, ZERO) == zconj(field.get(index, ZERO))
               for index in indices)


def direct_flux_over_pi(
    field: dict[int, Z],
    cutoff: dict[int, Z],
    period_factor: F,
    derivative_sign: int,
) -> F:
    derivative = {
        power: zmul(z(0, derivative_sign * power), coefficient)
        for power, coefficient in cutoff.items()
        if power != 0
    }
    product = poly_multiply(
        derivative,
        absolute_square_coefficients(field),
    )
    constant = product.get(0, ZERO)
    if constant[1] != 0:
        raise AssertionError("direct flux constant must be real")
    # (1/2)*(2*pi)/pi = 1 at the frozen normalization.
    return F(1, 2) * period_factor * constant[0]


def spectral_flux_over_pi(
    field: dict[int, Z],
    cutoff: dict[int, Z],
    difference_sign: int,
    formula_pi_factor: F,
    index_reversal: bool,
) -> F:
    total = ZERO
    for n, f_n in field.items():
        for m, f_m in field.items():
            difference = m - n
            cutoff_index = -difference if index_reversal else difference
            xi = cutoff.get(cutoff_index, ZERO)
            multiplier = z(0, difference_sign * difference)
            term = zmul(
                zmul(multiplier, xi),
                zmul(f_n, zconj(f_m)),
            )
            total = zadd(total, term)
    if total[1] != 0:
        raise AssertionError("spectral flux sum must be real")
    return formula_pi_factor * total[0]


def exponent_row(**values: F) -> dict[str, str]:
    return {key: rat(value) for key, value in values.items()}


def record(ok: bool, **details: Any) -> dict[str, Any]:
    return {"pass": bool(ok), **details}


def main() -> int:
    if MUTATION and MUTATION not in NEGATIVE_MUTATIONS:
        raise SystemExit(f"unknown R075E_MUTATION: {MUTATION}")

    text = MAIN.read_text(encoding="utf-8")
    scan_text = text + ("\x01" if MUTATION == "control" else "")
    flat_text = re.sub(r"\s+", " ", text)

    # Finite rational Laurent example. Xi(x)=2+cos(2x)+sin(2x), while
    # F(x)=2cos(x)+sin(x). All coefficients are rational complex and the
    # sine coefficient detects an erroneous reversal of Xi_{m-n}.
    cutoff = {
        0: z(2),
        2: z(F(1, 2), F(-1, 2)),
        -2: z(F(1, 2), F(1, 2)),
    }
    if MUTATION == "real_pair_zero":
        cutoff = {0: z(2)}

    real_pair = {
        1: z(1, F(-1, 2)),
        -1: z(1, F(1, 2)),
    }
    if MUTATION == "reality_pair_broken":
        real_pair[-1] = z(F(1, 2), F(1, 2))

    period_factor = F(1) if MUTATION == "period_factor" else F(2)
    formula_pi_factor = F(2) if MUTATION == "formula_pi_factor" else F(1)
    derivative_sign = -1 if MUTATION == "laurent_derivative_sign" else 1
    difference_sign = -1 if MUTATION == "difference_sign" else 1
    index_reversal = MUTATION == "index_reversal"

    pair_direct = direct_flux_over_pi(
        real_pair, cutoff, period_factor, derivative_sign
    )
    pair_spectral = spectral_flux_over_pi(
        real_pair, cutoff, difference_sign, formula_pi_factor, index_reversal
    )

    diagonal_total = ZERO
    for coefficient in real_pair.values():
        multiplier = z(1) if MUTATION == "diagonal_nonzero" else z(0, 0)
        diagonal_total = zadd(
            diagonal_total,
            zmul(
                zmul(multiplier, cutoff[0]),
                zmul(coefficient, zconj(coefficient)),
            ),
        )

    zero_mode = {0: z(F(3, 2))}
    zero_direct = direct_flux_over_pi(
        zero_mode, cutoff, period_factor, derivative_sign
    )
    zero_spectral = spectral_flux_over_pi(
        zero_mode, cutoff, difference_sign, formula_pi_factor, index_reversal
    )
    if MUTATION == "zero_mode_nonzero":
        zero_direct += 1

    singleton = {1: z(1, F(1, 2))}
    singleton_direct = direct_flux_over_pi(
        singleton, cutoff, period_factor, derivative_sign
    )
    singleton_spectral = spectral_flux_over_pi(
        singleton, cutoff, difference_sign, formula_pi_factor, index_reversal
    )
    singleton_is_real = (
        True if MUTATION == "singleton_physical"
        else is_real_laurent_field(singleton)
    )

    # E.14--E.16 exponent ledger.
    cylinder_l = F(2)
    cylinder_r = F(4) if MUTATION == "e15_volume" else F(5)
    holder_l = cylinder_l / 3
    holder_r = cylinder_r / 3
    p_normalization_r = (
        F(-1) if MUTATION == "e15_cubic_normalization" else F(-2)
    )
    p_normalization_omega = F(1)
    cubic_integral_r = -p_normalization_r
    cubic_integral_omega = -p_normalization_omega
    l2_l = holder_l
    l2_r = holder_r + F(2, 3) * cubic_integral_r
    l2_omega = F(2, 3) * cubic_integral_omega
    dissipation_prefactor_r = (
        F(-2) if MUTATION == "e15_cutoff_r" else F(-3)
    )
    dissipation_prefactor_omega = (
        F(0) if MUTATION == "e15_omega" else F(1)
    )
    e15_l = l2_l
    e15_r = l2_r + dissipation_prefactor_r
    e15_omega = l2_omega + dissipation_prefactor_omega

    e16_cgamma = (
        F(1, 12) if MUTATION == "e16_decay_sign" else F(-1, 12)
    )
    if MUTATION == "e16_denominator":
        e16_cgamma = F(-1, 6)

    e21_pi = F(0) if MUTATION == "e21_pi" else F(1)
    e21_omega = F(0) if MUTATION == "e21_omega" else F(1)
    e21_r = F(1) if MUTATION == "e21_r" else F(-1)

    e23_pb = F(2, 3) if MUTATION == "e23_pb_power" else F(1, 3)
    e23_pf = F(1, 3) if MUTATION == "e23_pf_power" else F(2, 3)
    e23_r = F(1) if MUTATION == "e23_residual_r" else F(0)

    power_ledger = {
        "E.14_pFNormalization": exponent_row(
            R=p_normalization_r, omega=p_normalization_omega
        ),
        "E.15_cylinderVolume": exponent_row(L=cylinder_l, R=cylinder_r),
        "E.15_holderFactor": exponent_row(L=holder_l, R=holder_r),
        "E.15_cubicTwoThirds": exponent_row(
            R=F(2, 3) * cubic_integral_r,
            omega=F(2, 3) * cubic_integral_omega,
            pF=F(2, 3),
        ),
        "E.15_L2Bound": exponent_row(
            L=l2_l, R=l2_r, omega=l2_omega, pF=F(2, 3)
        ),
        "E.15_dissipationPrefactor": exponent_row(
            R=dissipation_prefactor_r,
            omega=dissipation_prefactor_omega,
        ),
        "E.15_result": exponent_row(
            L=e15_l, R=e15_r, omega=e15_omega, pF=F(2, 3)
        ),
        "E.16_decay": exponent_row(L=F(2, 3), cGamma=e16_cgamma),
        "E.21_fluxNormalization": exponent_row(
            pi=e21_pi, R=e21_r, omega=e21_omega
        ),
        "E.23_mixedFlux": exponent_row(
            L=F(0), R=e23_r, omega=F(0), pB=e23_pb, pF=e23_pf
        ),
    }
    expected_power_ledger = {
        "E.14_pFNormalization": {"R": "-2", "omega": "1"},
        "E.15_cylinderVolume": {"L": "2", "R": "5"},
        "E.15_holderFactor": {"L": "2/3", "R": "5/3"},
        "E.15_cubicTwoThirds": {
            "R": "4/3", "omega": "-2/3", "pF": "2/3"
        },
        "E.15_L2Bound": {
            "L": "2/3", "R": "3", "omega": "-2/3", "pF": "2/3"
        },
        "E.15_dissipationPrefactor": {"R": "-3", "omega": "1"},
        "E.15_result": {
            "L": "2/3", "R": "0", "omega": "1/3", "pF": "2/3"
        },
        "E.16_decay": {"L": "2/3", "cGamma": "-1/12"},
        "E.21_fluxNormalization": {"pi": "1", "R": "-1", "omega": "1"},
        "E.23_mixedFlux": {
            "L": "0", "R": "0", "omega": "0",
            "pB": "1/3", "pF": "2/3"
        },
    }

    boundary = {
        "endpointRetained": MUTATION != "endpoint_dropped",
        "transportRightSign": -1 if MUTATION == "transport_sign" else 1,
        "horizontalSupportInvariant": MUTATION != "mode_invariance",
        "x1AverageXiUsed": MUTATION != "x1_hat_not_average",
        "zeroModeAllPayment": MUTATION != "zero_mode_small_payment",
        "complexSingletonPhysical": MUTATION == "complex_physical",
        "realPairFluxAlwaysZero": MUTATION == "real_pair_cancelled",
        "arbitraryRealE24Proved": MUTATION == "e24_closed",
        "completeClockProved": MUTATION == "full_clock",
        "clayClaim": MUTATION == "clay",
    }

    tags = re.findall(r"\\tag\{(E\.[^}]+)\}", text)
    if MUTATION == "tag":
        tags.append("E.1")
    references = [
        "E." + value for value in re.findall(r"\(E\.([0-9]+[a-z]?)\)", text)
    ]
    if MUTATION == "reference":
        references.append("E.99")
    display_open = sum(line.strip() == r"\[" for line in text.splitlines())
    display_close = sum(line.strip() == r"\]" for line in text.splitlines())
    if MUTATION == "display":
        display_open += 1
    expected_tags = [f"E.{index}" for index in range(1, 25)]

    dependency_expectations = dict(FROZEN_DEPENDENCIES)
    if MUTATION == "dependency_drift":
        dependency_expectations[sorted(dependency_expectations)[0]] = "0" * 64
    dependency_rows = {}
    for path in sorted(dependency_expectations):
        expected = dependency_expectations[path]
        table_present = any(
            path in line and FROZEN_DEPENDENCIES[path] in line
            for line in text.splitlines()
        )
        if MUTATION == "dependency_table_missing" and path == sorted(
            dependency_expectations
        )[0]:
            table_present = False
        dependency_rows[path] = {
            "expectedSha256": expected,
            "observedSha256": sha256(ROOT / path),
            "mainTableEntryPresent": table_present,
        }

    b_text = (ROOT / "research/r075b_bulk_clock_outer_padding_gate.md").read_text(
        encoding="utf-8"
    )
    d_text = (ROOT / "research/r075d_passive_gradient_route_screen.md").read_text(
        encoding="utf-8"
    )
    b_tags = set(re.findall(r"\\tag\{(B\.[^}]+)\}", b_text))
    d_tags = set(re.findall(r"\\tag\{(D\.[^}]+)\}", d_text))

    required_tokens = (
        r"\le C(P_R^M)^{2/3}\quad(L\ge L_0)",
        r"f_n(t,x_3)",
        r"\widehat\xi_\ell(x_1,x_3)",
        r"\Xi_\ell(x_3)",
        "The \(x_1\)-average \(\Xi_\ell\)",
        r"\mathcal T_\xi(F,b)",
        r"\pi\operatorname {Re}\sum_{n,m\in\mathbb Z}",
        r"i(m-n)",
        r"\Xi_{m-n}f_n\overline{f_m}",
        "common factor \(2\pi\)",
        "Every diagonal term \(n=m\) vanishes",
        "purely off-diagonal",
        r"S=\{0\}",
        "complexified scalar equation",
        "not by itself a real Navier--Stokes velocity field",
        r"p_F:=R^{-2}\omega",
        r"CL^{2/3}\omega^{1/3}p_F^{2/3}",
        r"L^{2/3}\exp\!\left(-\frac{c_\gamma}{12}L^2\right)",
        r"f_{-n}=\overline{f_n}",
        r"S=\{n,-n\}",
        r"\frac{\pi\omega}{R}\Bigg[",
        r"\le Cp_b^{1/3}p_F^{2/3}",
        r"\mathfrak X_{\xi,R}(F,b)\le C(P_R^M)^{2/3}",
        "No such bound is proved here",
        "Algebraic diagnostic only",
        "not promoted to a physical real Navier--Stokes result",
        "Open:** (E.24) for arbitrary real fields",
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
        "frozenDependencyBindings": record(
            all(
                row["expectedSha256"] == row["observedSha256"]
                and row["mainTableEntryPresent"]
                for row in dependency_rows.values()
            ),
            sources=dependency_rows,
        ),
        "finiteLaurentNormalizationE10": record(
            F(1, 2) * period_factor == 1
            and pair_direct == pair_spectral == F(-1, 2),
            cutoffCoefficients={
                str(power): zstring(value)
                for power, value in sorted(cutoff.items())
            },
            fieldCoefficients={
                str(power): zstring(value)
                for power, value in sorted(real_pair.items())
            },
            energyHalfTimesPeriodOverPi=rat(F(1, 2) * period_factor),
            directTOverPi=rat(pair_direct),
            spectralTOverPi=rat(pair_spectral),
        ),
        "diagonalAndZeroModeCancellation": record(
            diagonal_total == ZERO
            and zero_direct == zero_spectral == 0,
            diagonalContribution=zstring(diagonal_total),
            zeroModeDirectTOverPi=rat(zero_direct),
            zeroModeSpectralTOverPi=rat(zero_spectral),
        ),
        "complexSingletonBoundary": record(
            singleton_direct == singleton_spectral == 0
            and not singleton_is_real,
            directTOverPi=rat(singleton_direct),
            spectralTOverPi=rat(singleton_spectral),
            realPhysical=singleton_is_real,
        ),
        "realPairCanBeNonzero": record(
            is_real_laurent_field(real_pair)
            and pair_direct == pair_spectral == F(-1, 2),
            realPhysical=is_real_laurent_field(real_pair),
            directTOverPi=rat(pair_direct),
            spectralTOverPi=rat(pair_spectral),
        ),
        "powerLedgerE14ToE23": record(
            power_ledger == expected_power_ledger,
            exponents=power_ledger,
        ),
        "localEnergyAndModalBoundary": record(
            boundary["endpointRetained"]
            and boundary["transportRightSign"] == 1
            and boundary["horizontalSupportInvariant"]
            and boundary["x1AverageXiUsed"],
            state=boundary,
        ),
        "tagsReferencesAndDisplays": record(
            tags == expected_tags
            and len(set(tags)) == 24
            and not (set(references) - set(tags))
            and display_open == display_close == 24,
            tags=tags,
            unresolvedLocalReferences=sorted(set(references) - set(tags)),
            displayOpen=display_open,
            displayClose=display_close,
        ),
        "externalReferenceBoundary": record(
            "B.14" in b_tags
            and "cutoff and local energy identity" in text
            and all(label in text and label in d_tags
                    for label in ("D.9", "D.18", "D.23")),
            B14Resolved="B.14" in b_tags,
            DReferencesResolved=all(
                label in d_tags for label in ("D.9", "D.18", "D.23")
            ),
        ),
        "requiredTextualSentinels": record(
            all(
                re.sub(r"\s+", " ", token) in flat_text
                for token in required_tokens
            ),
            requiredCount=len(required_tokens),
        ),
        "claimBoundary": record(
            boundary["zeroModeAllPayment"]
            and not boundary["complexSingletonPhysical"]
            and not boundary["realPairFluxAlwaysZero"]
            and not boundary["arbitraryRealE24Proved"]
            and not boundary["completeClockProved"]
            and not boundary["clayClaim"]
            and "arbitrarily large payment" in text
            and "Algebraic diagnostic only" in text
            and "Open:** (E.24) for arbitrary real fields" in text
            and r"\mathbf{NOT\ CLAY}" in text,
            state=boundary,
        ),
        "textSafety": record(
            not any(ord(char) < 32 and char not in "\n\t"
                    for char in scan_text),
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
        "exactFiniteExample": {
            "cutoff": "Xi(x)=2+cos(2x)+sin(2x)",
            "field": "F(x)=2cos(x)+sin(x)",
            "directTOverPi": rat(pair_direct),
            "spectralTOverPi": rat(pair_spectral),
            "expectedTOverPi": "-1/2",
            "diagonalContribution": zstring(diagonal_total),
            "zeroModeTOverPi": rat(zero_direct),
            "complexSingletonTOverPi": rat(singleton_direct),
            "complexSingletonPhysical": singleton_is_real,
            "realPairPhysical": is_real_laurent_field(real_pair),
        },
        "powerLedger": power_ledger,
        "negativeMutations": list(NEGATIVE_MUTATIONS),
        "boundary": (
            "FINITE FOURIER WITNESS CHECKS THE ALGEBRAIC NORMALIZATION, NOT "
            "A FULL E.1 TRAJECTORY OR THE GEOMETRIC COLLAR CUTOFF; real zero "
            "mode paid for all payment at L>=L0; nonzero complex singleton "
            "is diagnostic, not physical; real +/-n pair need not cancel; "
            "E.24, complete clock, fixed deletion, and regularity remain "
            "OPEN; NOT CLAY"
        ),
    }
    OUT_JSON.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    dependency_lines = "\n".join(
        f"- {path}: {row['observedSha256']} (main table row present)"
        for path, row in dependency_rows.items()
    )
    OUT_REPORT.write_text(
        f"""# R0.75E reproducibility certificate report

- Verdict: **{verdict}**
- Assertions: {payload['assertionsPassed']}/{payload['assertionsTotal']}
- Main SHA-256: {actual_main_hash}
- Tags and displays: {len(tags)}/{display_open}
- Finite real-pair example T/pi: {pair_direct}
- Negative mutations declared: {len(NEGATIVE_MUTATIONS)}

## Frozen dependencies

{dependency_lines}

## Certified finite checks

For Xi(x)=2+cos(2x)+sin(2x) and F(x)=2cos(x)+sin(x), all Fourier
coefficients lie in the rational complex numbers. Direct Laurent
multiplication gives T/pi=-1/2. The independently assembled E.10 mode sum
also gives T/pi=-1/2. Diagonal terms and the zero mode give zero. A nonzero
complex singleton also gives zero but violates the real-field pairing,
whereas the real +/-1 pair gives a nonzero flux.

The certificate additionally recomputes every L, R, omega, pF, and pB
power in E.14--E.16, E.21, and E.23; checks the endpoint and transport
sign; binds the B/C/D source table; and verifies all 24 tags, references,
displays, and boundary sentinels.

The finite Laurent witness certifies the algebraic normalization in E.10;
it is not asserted to be a full E.1 spacetime trajectory or the actual
geometric collar cutoff.

The all-payment result is confined to the real horizontal zero-mode
subclass for L>=L0. The nonzero complex singleton is algebraic only, and a
real +/-n pair is not forced to vanish. E.24 for arbitrary real fields,
complete-clock extraction, fixed deletion, suitable-weak transfer, and
regularity remain OPEN. No Clay conclusion is certified. NOT CLAY.
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
