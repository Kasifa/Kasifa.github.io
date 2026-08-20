#!/usr/bin/env python3
"""R0.69A source-bound assembly audit for the complete target Picard series.

The audit joins four already certified inputs:

* the quartic heat asymptotic from R0.66;
* the sixth-order dominant heat projection from R0.67C-2;
* the all-order tail estimate from R0.68A; and
* the corrected eighth-order dominant heat projection from R0.68B-2h.

For the periodic target family and quartic-critical amplitude it certifies the
dimensionless limit of the complete target Fourier coefficient divided by its
quadratic Picard coefficient.  It is an assembly theorem inside the globally
smooth invariant-shear class, not a singularity or regularity theorem for
general three-dimensional Navier--Stokes solutions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from fractions import Fraction
from pathlib import Path

import gmpy2


sys.set_int_max_str_digits(100_000)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

DEFAULT_QUARTIC = ROOT / "research/certificates/r066/spectral-audit.json"
DEFAULT_SIXTH = (
    ROOT
    / "research/certificates/r067c2/"
    "sixth-order-heat-dominant-projection-audit.json"
)
DEFAULT_TAIL = (
    ROOT / "research/certificates/r068a/all-order-tail-reduction-audit.json"
)
DEFAULT_EIGHTH = (
    ROOT / "research/certificates/r068b2h-corrected-heat/defect-sign.json"
)
DEFAULT_EIGHTH_SPECTRUM = (
    ROOT / "research/certificates/r068b1/eighth-order-cycle-audit.json"
)

EXPECTED_HASHES = {
    "quartic": "a6f66c8bea8806fee3716b8d6611a2e0720e29969d94d991672cf3626ba8bcb2",
    "sixth": "740a90d543104aeed3848a4196776ae0b16b714d08c5966db735a7eb63e81af5",
    "tail": "f6d94a8be1d1c1394311b745bdac82db64cc43ab198e36ca209997975f21f50a",
    "eighth": "c79f78816ae780074b90c7eb098d0b804253e1a449cbd0e0b8e60861de0f5bca",
    "eighthSpectrum": "00d60f5abd080f90c551126f388e005df4ead5bd556308f8a63c5972766d483b",
}

PRECISION = 256


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def fraction_mpfr(value: Fraction, mode: object) -> gmpy2.mpfr:
    with gmpy2.context(gmpy2.get_context(), precision=PRECISION, round=mode):
        return gmpy2.mpfr(value.numerator) / gmpy2.mpfr(value.denominator)


def s2_limit_interval() -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    """Enclose (1-2^(-(31/30)^2))/(2(31/30)^2) outward."""
    x = Fraction(31 * 31, 30 * 30)
    x_down = fraction_mpfr(x, gmpy2.RoundDown)
    x_up = fraction_mpfr(x, gmpy2.RoundUp)
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundDown
    ):
        log_two_down = gmpy2.log(gmpy2.mpfr(2))
        product_down = x_down * log_two_down
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundUp
    ):
        log_two_up = gmpy2.log(gmpy2.mpfr(2))
        product_up = x_up * log_two_up
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundDown
    ):
        exponent_low = -product_up
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundUp
    ):
        exponent_high = -product_down
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundDown
    ):
        exp_low = gmpy2.exp(exponent_low)
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundUp
    ):
        exp_high = gmpy2.exp(exponent_high)
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundDown
    ):
        lower = (gmpy2.mpfr(1) - exp_high) / (2 * x_up)
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundUp
    ):
        upper = (gmpy2.mpfr(1) - exp_low) / (2 * x_down)
    return lower, upper


def positive_ratio_interval(
    numerator_lower: Fraction,
    numerator_upper: Fraction,
    denominator_lower: gmpy2.mpfr,
    denominator_upper: gmpy2.mpfr,
) -> tuple[gmpy2.mpfr, gmpy2.mpfr]:
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundDown
    ):
        lower = fraction_mpfr(numerator_lower, gmpy2.RoundDown) / denominator_upper
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundUp
    ):
        upper = fraction_mpfr(numerator_upper, gmpy2.RoundUp) / denominator_lower
    return lower, upper


def decimal_record(lower: gmpy2.mpfr, upper: gmpy2.mpfr) -> dict[str, str]:
    return {
        "lower": format(lower, ".50g"),
        "upper": format(upper, ".50g"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit", default="uncommitted")
    parser.add_argument("--quartic-certificate", type=Path, default=DEFAULT_QUARTIC)
    parser.add_argument("--sixth-certificate", type=Path, default=DEFAULT_SIXTH)
    parser.add_argument("--tail-certificate", type=Path, default=DEFAULT_TAIL)
    parser.add_argument("--eighth-certificate", type=Path, default=DEFAULT_EIGHTH)
    parser.add_argument(
        "--eighth-spectrum-certificate",
        type=Path,
        default=DEFAULT_EIGHTH_SPECTRUM,
    )
    parser.add_argument("--pretty", action="store_true")
    arguments = parser.parse_args()

    paths = {
        "quartic": arguments.quartic_certificate,
        "sixth": arguments.sixth_certificate,
        "tail": arguments.tail_certificate,
        "eighth": arguments.eighth_certificate,
        "eighthSpectrum": arguments.eighth_spectrum_certificate,
    }
    reports = {name: load_json(path) for name, path in paths.items()}
    hashes = {name: sha256_file(path) for name, path in paths.items()}

    quartic = reports["quartic"]
    sixth = reports["sixth"]
    tail = reports["tail"]
    eighth = reports["eighth"]
    eighth_spectrum = reports["eighthSpectrum"]

    quartic_theorem = quartic["certifiedTheorem"]
    coefficient_lower = Fraction(
        int(quartic_theorem["coefficientLowerNumerator"]),
        int(quartic_theorem["coefficientLowerDenominator"]),
    )
    coefficient_upper = Fraction(
        int(quartic_theorem["coefficientUpperNumerator"]),
        int(quartic_theorem["coefficientUpperDenominator"]),
    )
    root_lower = Fraction(
        int(quartic["massSpectrum"]["dominantLowerNumerator"]),
        int(quartic["massSpectrum"]["dominantLowerDenominator"]),
    )

    s2_lower, s2_upper = s2_limit_interval()
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundDown
    ):
        denominator_lower = gmpy2.mpfr(3600) * s2_lower
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundUp
    ):
        denominator_upper = gmpy2.mpfr(3600) * s2_upper
    correction_lower, correction_upper = positive_ratio_interval(
        -coefficient_upper,
        -coefficient_lower,
        denominator_lower,
        denominator_upper,
    )
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundDown
    ):
        full_lower = gmpy2.mpfr(1) + correction_lower
    with gmpy2.context(
        gmpy2.get_context(), precision=PRECISION, round=gmpy2.RoundUp
    ):
        full_upper = gmpy2.mpfr(1) + correction_upper

    sixth_rate = Fraction(16, 1) / root_lower
    eighth_rate = Fraction(256, 1) / (root_lower * root_lower)
    tail_rate = Fraction(
        int(tail["constants"]["simpleCriticalTailBlockRate"]["numerator"]),
        int(tail["constants"]["simpleCriticalTailBlockRate"]["denominator"]),
    )

    checks = {
        "upstreamStatusesPassed": (
            quartic["status"] == "passed"
            and sixth["status"] == "passed"
            and tail["status"] == "passed"
            and eighth["status"] == "strict-passed"
        ),
        "pinnedQuarticCertificateHashMatches": (
            hashes["quartic"] == EXPECTED_HASHES["quartic"]
        ),
        "pinnedSixthCertificateHashMatches": (
            hashes["sixth"] == EXPECTED_HASHES["sixth"]
        ),
        "pinnedTailCertificateHashMatches": (
            hashes["tail"] == EXPECTED_HASHES["tail"]
        ),
        "pinnedEighthCertificateHashMatches": (
            hashes["eighth"] == EXPECTED_HASHES["eighth"]
        ),
        "pinnedEighthSpectrumCertificateHashMatches": (
            hashes["eighthSpectrum"] == EXPECTED_HASHES["eighthSpectrum"]
        ),
        "quarticCoefficientIsStrictlyNegative": (
            coefficient_lower < coefficient_upper < 0
            and quartic_theorem["coefficientSign"] == "negative"
        ),
        "sixthDominantHeatProjectionIsStrictlyNegative": (
            sixth["conclusion"]["dominantHeatProjectionUpper"] < 0
            and sixth["checks"]["completeDominantHeatProjectionIsStrictlyNegative"]
        ),
        "eighthDominantHeatProjectionIsStrictlyNegative": (
            eighth["correctedDominantHeat"]["upper"] < 0
            and eighth["checks"]["correctedDominantHeatIntervalIsStrictlyNegative"]
        ),
        "eighthDominantRootStrictlyExceedsComplement": (
            eighth["resolvent"]["rootLower"] > 4800
            and eighth_spectrum["checks"]
            ["degreeTenRootsAreStrictlyInsideRadiusFourThousandEightHundred"]
            and eighth_spectrum["checks"]
            ["degreeEighteenRootsAreStrictlyInsideRadiusFourThousandEightHundred"]
        ),
        "eighthZeroJetRemainderIsStrictlyContractive": (
            0 < eighth["resolvent"]["remainderContraction"]
            < eighth["resolvent"]["rootLower"]
        ),
        "quadraticLimitIntervalIsStrictlyPositive": 0 < s2_lower <= s2_upper,
        "quarticCorrectionLimitIsStrictlyPositive": (
            0 < correction_lower <= correction_upper
        ),
        "sixthCriticalRateIsContractive": sixth_rate < 1,
        "eighthCriticalRateIsContractive": eighth_rate < 1,
        "allOrderTailRateIsContractive": tail_rate < 1,
        "completeTargetLimitStrictlyExceedsOne": 1 < full_lower <= full_upper,
        "invariantShearClassIsExplicitlyNotASingularityClaim": (
            "globally smooth" in tail["classification"]
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    result = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "complete target Picard-series asymptotic for one periodic family "
            "inside the globally smooth invariant-shear class; not a "
            "three-dimensional Navier-Stokes singularity or regularity theorem"
        ),
        "checks": checks,
        "family": {
            "M_r": "16^r",
            "q_r": "2(16^r-1)/15",
            "m_r": "q_r+1=(2M_r+13)/15",
            "H_r": "4M_r",
            "epsilonSquared": "(16/lambda)^r",
            "amplitude": "A_r=epsilon_r*sqrt(H_r)",
            "observationTime": "t_r=log(2)/(2H_r^2)",
        },
        "asymptoticAssembly": {
            "normalizedTarget": (
                "Ghat(0,m_r,t_r)/(A_r^2 Ghat_2(0,m_r,t_r))"
            ),
            "quadraticLimit": "1",
            "quarticLimit": "-C_*/(3600 D_*)",
            "sixthLimit": "0",
            "eighthLimit": "0",
            "ordersAtLeastTenLimit": "0",
            "D_*": "(1-2^(-(31/30)^2))/(2(31/30)^2)",
            "completeLimit": "1-C_*/(3600 D_*)",
        },
        "certifiedIntervals": {
            "quadraticDimensionlessLimit": decimal_record(s2_lower, s2_upper),
            "positiveQuarticCorrection": decimal_record(
                correction_lower, correction_upper
            ),
            "completeNormalizedTargetLimit": decimal_record(
                full_lower, full_upper
            ),
        },
        "decayRates": {
            "sixthUpperFromLambdaLower": {
                "exact": f"{sixth_rate.numerator}/{sixth_rate.denominator}",
                "decimal": f"{float(sixth_rate):.18e}",
            },
            "eighthUpperFromLambdaLower": {
                "exact": f"{eighth_rate.numerator}/{eighth_rate.denominator}",
                "decimal": f"{float(eighth_rate):.18e}",
            },
            "ordersAtLeastTen": {
                "exact": f"{tail_rate.numerator}/{tail_rate.denominator}",
                "decimal": f"{float(tail_rate):.18e}",
            },
        },
        "eighthOrderAsymptoticLemma": {
            "dominantRoot": "nu=256 lambda",
            "finiteComplementRadiusUpper": 4800,
            "zeroDegreeTenJetRemainderContraction": eighth["resolvent"]
            ["remainderContraction"],
            "correctedCoefficient": eighth["correctedDominantHeat"],
            "conclusion": "S_8,r/nu^r converges to a strictly negative limit",
        },
        "provenance": {
            "sourceCommit": arguments.source_commit,
            "python": platform.python_version(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "inputCertificates": {
                name: {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": hashes[name],
                }
                for name, path in paths.items()
            },
        },
        "boundary": [
            "The packet is an exactly invariant parallel-shear solution and is globally smooth.",
            "The theorem closes one target Fourier coefficient, not a critical norm of arbitrary solutions.",
            "It proves neither finite-time singularity nor global regularity for general three-dimensional data.",
            "It is not a solution of the Navier-Stokes Millennium problem.",
        ],
    }
    serialized = json.dumps(
        result,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=not arguments.pretty,
    ) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized)
    sys.stdout.write(serialized)


if __name__ == "__main__":
    main()
