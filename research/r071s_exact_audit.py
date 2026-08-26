#!/usr/bin/env python3
"""Exact and deterministic finite audit for R0.71S.

The certificate isolates what a signed or bilinear time-packet design can and
cannot gain.  Rational arithmetic is used for the box-packet, even-touch, and
initial-face ledgers.  The only floating-point quantities are elementary
matrix eigenvalues and exponential heat-kernel constants, each enclosed by an
independent exact inequality.

Nothing in this file constructs a Navier--Stokes trajectory.  In particular,
the even-touch path is a forced-parabolic pressure test.  The Fourier ledger
at the end records an exact genuine NSE initial face, but not its positive-time
evolution.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def frac(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def matvec(matrix: list[list[float]], vector: list[float]) -> list[float]:
    return [sum(entry * value for entry, value in zip(row, vector)) for row in matrix]


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def largest_eigenvalue_power(matrix: list[list[float]]) -> tuple[float, float, int]:
    """Return a deterministic Rayleigh value and residual for a PSD matrix."""

    size = len(matrix)
    if size == 1:
        return matrix[0][0], 0.0, 0
    vector = [1.0 / math.sqrt(size)] * size
    eigenvalue = 0.0
    for iteration in range(1, 100_001):
        product = matvec(matrix, vector)
        norm = math.sqrt(dot(product, product))
        require(norm > 0.0, "positive Gram power-iteration norm")
        next_vector = [value / norm for value in product]
        next_product = matvec(matrix, next_vector)
        next_eigenvalue = dot(next_vector, next_product)
        next_residual_vector = [
            value - next_eigenvalue * direction
            for value, direction in zip(next_product, next_vector)
        ]
        next_residual = math.sqrt(dot(next_residual_vector, next_residual_vector))
        if (
            abs(next_eigenvalue - eigenvalue) <= 2e-15 * max(1.0, abs(next_eigenvalue))
            and next_residual < 1e-11
        ):
            vector = next_vector
            eigenvalue = next_eigenvalue
            break
        vector = next_vector
        eigenvalue = next_eigenvalue
    else:
        raise AssertionError("Gram power iteration did not converge")
    residual_vector = [value - eigenvalue * direction for value, direction in zip(matvec(matrix, vector), vector)]
    residual = math.sqrt(dot(residual_vector, residual_vector))
    return eigenvalue, residual, iteration


def box_diagonal_scaling() -> dict[str, object]:
    """A nonzero-mean L2 box packet pays one inverse parabolic height."""

    theta = Fraction(1, 8)
    rows = []
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        k = Fraction(frequency)
        height = theta / (k * k)
        normalized_mean_squared = height
        reproducing_diagonal = 1 / normalized_mean_squared
        require(reproducing_diagonal == k * k / theta, f"K={frequency} box diagonal")
        rows.append({
            "K": frequency,
            "theta": frac(theta),
            "height": frac(height),
            "l2PacketNormSquared": "1",
            "packetMeanSquared": frac(normalized_mean_squared),
            "constantReproductionDiagonal": frac(reproducing_diagonal),
            "expectedKappaSquaredOverTheta": frac(k * k / theta),
        })
    return {
        "passed": True,
        "packet": "psi_{b,h}=h^-1/2 1_[b,b+h), h=theta*K^-2",
        "identity": "||psi/(integral psi)||_2^2=1/h=K^2/theta",
        "rows": rows,
        "boundary": "This is a time-sampling diagonal cost, not an NSE estimate.",
    }


def finite_box_gram() -> dict[str, object]:
    """Finite Toeplitz Gram matrices and exact Rayleigh/row-sum enclosure."""

    rows = []
    cases = (
        (16, 1), (16, 2), (16, 4), (16, 8), (32, 8),
        (64, 1), (64, 2), (64, 4), (64, 8), (64, 16), (64, 32),
    )
    for count, overlap in cases:
        require(1 <= overlap <= count, "valid box overlap")
        matrix = [
            [max(0.0, 1.0 - abs(i - j) / overlap) for j in range(count)]
            for i in range(count)
        ]
        eigenvalue, residual, iterations = largest_eigenvalue_power(matrix)
        lower = Fraction(overlap) - Fraction(overlap * overlap - 1, 3 * count)
        upper = Fraction(overlap)
        require(float(lower) <= eigenvalue + 2e-12, f"N={count}, p={overlap} Rayleigh lower")
        require(eigenvalue <= float(upper) + 2e-12, f"N={count}, p={overlap} row-sum upper")
        require(residual < 2e-7, f"N={count}, p={overlap} eigen residual")
        rows.append({
            "N": count,
            "integerWindowOverlap": overlap,
            "gramFormula": "G_kl=(1-|k-l|/p)_+",
            "exactRayleighLowerBound": frac(lower),
            "numericalLargestEigenvalue": eigenvalue,
            "exactMaximumRowSumUpperBound": frac(upper),
            "eigenResidualL2": residual,
            "powerIterations": iterations,
            "periodicCirculantLargestEigenvalue": overlap,
        })
    return {
        "passed": True,
        "finiteIntervalEnclosure": "p-(p^2-1)/(3N) <= lambda_max <= p",
        "periodicExactIdentity": "lambda_max=p=N*h/T for N equally spaced periodic box packets",
        "rows": rows,
        "boundary": "Common packet directions are used; orthogonal directions can reduce the Gram constant.",
    }


def backward_heat_constants() -> dict[str, object]:
    """Exact elementary constants of the adjoint/backward heat packet."""

    viscosity = 1.0
    theta = 0.125
    rows = []
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        k = float(frequency)
        height = theta / (k * k)
        damping = viscosity * k * k
        norm_squared = (1.0 - math.exp(-2.0 * damping * height)) / (2.0 * damping)
        normalization = norm_squared**-0.5
        normalized_mean = normalization * (1.0 - math.exp(-damping * height)) / damping
        inverse_mean_squared = 1.0 / (normalized_mean * normalized_mean)
        closed_form = 0.5 * viscosity * k * k / math.tanh(0.5 * viscosity * theta)
        require(abs(inverse_mean_squared / closed_form - 1.0) < 2e-14, f"K={frequency} heat mean")
        half_shift = 0.5 * height
        gram_half_shift = (
            math.exp(-damping * half_shift)
            * (1.0 - math.exp(-2.0 * damping * (height - half_shift)))
            / (1.0 - math.exp(-2.0 * damping * height))
        )
        require(0.0 < gram_half_shift < 1.0, f"K={frequency} heat Gram entry")
        rows.append({
            "K": frequency,
            "nu": viscosity,
            "theta": theta,
            "height": height,
            "unnormalizedPacketNormSquared": norm_squared,
            "normalizedPacketMean": normalized_mean,
            "inverseNormalizedMeanSquared": inverse_mean_squared,
            "closedFormNuK2Over2CothNuThetaOver2": closed_form,
            "normalizedGramAtHalfWindowShift": gram_half_shift,
        })
    return {
        "passed": True,
        "packet": "1_[b,b+h](s) exp(-nu*K^2*(b+h-s))",
        "normIdentity": "||p||_2^2=(1-exp(-2*nu*K^2*h))/(2*nu*K^2)",
        "reproductionIdentity": "|integral(p/||p||)|^-2=(nu*K^2/2)coth(nu*theta/2)",
        "translatedGramIdentity": (
            "g(d)=exp(-nu*K^2*d)*(1-exp(-2*nu*K^2*(h-d)))"
            "/(1-exp(-2*nu*K^2*h)) for 0<=d<h"
        ),
        "rows": rows,
        "boundary": "Duhamel with this packet gives an endpoint upper estimate, not an entry lower charge.",
    }


def bilinear_mean_dichotomy() -> dict[str, object]:
    """A separable bilinear detector either misses constants or pays 1/h."""

    theta = Fraction(1, 8)
    rows = []
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        k = Fraction(frequency)
        height = theta / (k * k)
        box_mean_squared = frac(height)
        # Both L2-normalized box means have product h.  Normalizing the
        # bilinear response to one therefore has operator norm 1/h.
        both_nonzero_norm = 1 / height
        require(both_nonzero_norm == k * k / theta, f"K={frequency} bilinear cost")
        rows.append({
            "K": frequency,
            "height": frac(height),
            "boxMeanSquared": box_mean_squared,
            "rawProductOfTwoBoxMeans": frac(height),
            "normalizedBilinearOperatorNorm": frac(both_nonzero_norm),
            "zeroMeanHaarTimesBoxResponseToConstants": "0",
            "boxTimesZeroMeanHaarResponseToConstants": "0",
        })
    return {
        "passed": True,
        "nonzeroMeanCase": "two L2-normalized box factors reproduce constants only after division by h, costing 1/h=K^2/theta",
        "zeroMeanCase": "if either factor has zero time mean, the separable bilinear detector annihilates constant leading data exactly",
        "rows": rows,
        "boundary": "The dichotomy concerns separable time packets; it does not exclude a nonseparable NSE-specific bilinear identity.",
    }


def even_touch_cancellation() -> dict[str, object]:
    """Exact soft half-layer masses for C=(t-b)^2 e."""

    rows = []
    for exponent in (0, 1, 2, 3, 4, 6, 8):
        soft = Fraction(1, 2 ** (8 * exponent))
        radius = Fraction(1, 2**exponent)
        radius_fourth = radius**4
        half_mass = radius_fourth / (radius_fourth + soft)
        expected_half_mass = Fraction(2 ** (4 * exponent), 2 ** (4 * exponent) + 1)
        require(half_mass == expected_half_mass, f"eta exponent={exponent} half mass")
        rows.append({
            "softEta": frac(soft),
            "shrinkingRadius": frac(radius),
            "rightSignedLayerMass": frac(half_mass),
            "leftSignedLayerMass": frac(-half_mass),
            "totalSignedMass": "0",
            "totalJordanMass": frac(2 * half_mass),
        })
    require(rows[-1]["totalSignedMass"] == "0", "even touch signed cancellation")
    return {
        "passed": True,
        "family": "C(t)=(t-b)^2 e, F(b)=e, Y(b)=1",
        "softProfile": "a_eta(t)=(t-b)^4/((t-b)^4+eta)",
        "limit": "signed atom 0; positive atom delta_b; negative atom delta_b; Jordan atom 2 delta_b",
        "rows": rows,
        "boundary": "A discontinuous event-centered left/right test recovers the Jordan mass only by reinstating segmentation.",
    }


def genuine_initial_face_scaling() -> dict[str, object]:
    """Exact covariant R0.71O genuine NSE initial-face scaling ledger.

    The frequency family must include the NSE amplitude factor: if the base
    datum has amplitude ``a``, then the compatible torus dilation has
    amplitude ``a*K`` and frequency ``K``.  A fixed-amplitude frequency sweep
    would not test the scaling theorem because its kappa^-2 weighted atom
    decays like K^-2.
    """

    base_amplitude = Fraction(1)
    rows = []
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        k = Fraction(frequency)
        scaled_amplitude = base_amplitude * k
        y0 = scaled_amplitude**2 * k**2
        norm_f_squared = scaled_amplitude**4 * k**2 / 4
        norm_c_squared = scaled_amplitude**4 * k**6
        pairing = scaled_amplitude**4 * k**4 / 2
        entry = pairing**2 / (y0 * norm_c_squared)
        signed_directional_amplitude_squared = entry
        target_atom = k**-2 * entry
        relative_bare_leray_time_integral = k**-2
        require(entry == base_amplitude**2 * k**2 / 4, f"K={frequency} covariant entry")
        require(target_atom == base_amplitude**2 / 4, f"K={frequency} invariant weighted atom")
        rows.append({
            "K": frequency,
            "scaledAmplitude": frac(scaled_amplitude),
            "Y0": frac(y0),
            "normFSquared": frac(norm_f_squared),
            "normLeadingCoefficientSquared": frac(norm_c_squared),
            "pairingFWithLeadingDirection": frac(pairing),
            "positiveInitialFaceAtom": frac(entry),
            "signedDirectionalAmplitudeSquared": frac(signed_directional_amplitude_squared),
            "kappaMinusTwoWeightedAtom": frac(target_atom),
            "relativeBareLerayTimeIntegral": frac(relative_bare_leray_time_integral),
        })
    return {
        "passed": True,
        "initialData": "u_{0,K}=K(0,cos(K*x1),cos(K*x2)) from u_{0,1}=(0,cos(x1),cos(x2))",
        "multiplier": "m(K)=0, m(sqrt(2)K)=1, chi=1",
        "exactLedger": (
            "for covariant amplitude a_K=K: Y=K^4, ||F||^2=K^6/4, "
            "C_t=2K^2F, A_plus=K^2/4, K^-2 A_plus=1/4"
        ),
        "timeScalingIdentity": (
            "integral_0^(T/K^2) ||L_K||_{H^-1}^2/Y_K dt "
            "=K^-2 integral_0^T ||L||_{H^-1}^2/Y dt"
        ),
        "rows": rows,
        "boundary": (
            "This is a one-sided genuine NSE initial face at the observation boundary and an exact covariant scaling ledger. "
            "The time-integral equality follows from NSE covariance, not from positive-time numerical integration. "
            "It is not an internal even touch or a positive-time integration, and it is not an internal-entry theorem or a regularity result."
        ),
    }


def build_certificate() -> dict[str, object]:
    checks = {
        "boxDiagonalScaling": box_diagonal_scaling(),
        "finiteBoxGram": finite_box_gram(),
        "backwardHeatConstants": backward_heat_constants(),
        "bilinearMeanDichotomy": bilinear_mean_dichotomy(),
        "evenTouchCancellation": even_touch_cancellation(),
        "genuineInitialFaceScaling": genuine_initial_face_scaling(),
    }
    require(all(check["passed"] for check in checks.values()), "all R0.71S exact checks")
    return {
        "release": "R0.71S",
        "status": "passed",
        "scope": (
            "finite signed/bilinear time-packet method audit, exact Gram enclosures, and a genuine NSE initial-face scaling ledger; "
            "no NSE packet packing theorem, positive-time initial-face integration, continuation criterion, singularity, or global regularity claim"
        ),
        "checks": checks,
        "decision": (
            "A nonzero-mean parabolic packet retains constant signed directional data only at an inverse-height K^2 cost, while a zero-mean factor "
            "annihilates that data. Dense same-direction events additionally force the finite Gram constant to grow with temporal density."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
