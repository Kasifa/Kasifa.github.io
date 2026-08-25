#!/usr/bin/env python3
"""Exact symbolic audit for the R0.71N full-scalar fusion.

The audit checks only universal algebra on a classical fixed-cell interval.
It does not estimate the signed second-jet residual, cross a zero denominator,
or assert a Navier--Stokes regularity conclusion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def clean(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.simplify(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def full_scalar_fusion() -> dict[str, object]:
    """Check the radial/projective cancellation and square-plus-residual form."""

    B, d, Y = sp.symbols("B d Y", positive=True)
    B_t, d_t, Y_t = sp.symbols("B_t d_t Y_t", real=True)
    lam = sp.symbols("lambda", real=True)
    acceleration, pairing, mismatch_square = sp.symbols(
        "A I V", real=True
    )
    root = sp.sqrt(Y * d)
    z = B / root

    # B_t=<F_t,C>+<F,C_t>, while I=<F,M>=<F,C_t>+lambda B.
    f_t_c = acceleration
    f_c_t = pairing - lam * B
    b_t_relation = clean(B_t - (f_t_c + f_c_t))
    acceleration_substitution = pairing - lam * B + B_t * 0
    # Solving the relation for A gives A=B_t-I+lambda B.
    solved_acceleration = B_t - pairing + lam * B
    require(clean(b_t_relation.subs(acceleration, solved_acceleration)) == 0,
            "B_t pairing relation")

    n_radial = f_t_c + lam * B
    projective_radial = pairing - B * (d_t / (2 * d) + lam)
    coordinate_source = clean(
        (n_radial + projective_radial) / root - Y_t * z / (2 * Y)
    )
    derivative_source = clean(
        (B_t + lam * B) / root
        - z * (Y_t / (2 * Y) + d_t / (2 * d))
    )
    require(
        clean(coordinate_source.subs(acceleration, solved_acceleration)
              - derivative_source) == 0,
        "full scalar derivative reconstruction",
    )

    # Complete the square: I=P-V, equivalently P=I+V.
    positive_square = pairing + mismatch_square
    signed_residual = clean(
        acceleration
        - mismatch_square
        - B * (Y_t / Y + d_t / d) / 2
    )
    square_source = clean((positive_square + signed_residual) / root)
    require(clean(square_source - coordinate_source) == 0,
            "square plus residual identity")

    nominal_radial = clean(lam * B / root)
    nominal_projective = clean(-lam * B / root)
    require(clean(nominal_radial + nominal_projective) == 0,
            "nominal parabolic cancellation")

    return {
        "passed": True,
        "definitions": {
            "root": "sqrt(Y*d)",
            "z": "B/sqrt(Y*d)",
            "lambda": "nu*kappa^2",
            "I": "int chi G.(G+nu H)",
            "P": "int chi |G+(nu/2)H|^2",
            "V": "(nu^2/4) int chi |H|^2",
            "A": "<G_t,chi W>=<F_t,C>",
        },
        "nominalRadial": str(nominal_radial),
        "nominalProjective": str(nominal_projective),
        "coordinateSource": str(coordinate_source),
        "derivativeSource": str(derivative_source),
        "positiveSquare": str(positive_square),
        "signedResidual": str(signed_residual),
        "squarePlusResidual": str(square_source),
        "boundary": (
            "P is nonnegative, but A, the normalization row, and the annular "
            "mismatch remain signed before the local-enstrophy substitution."
        ),
    }


def local_enstrophy_fusion() -> dict[str, object]:
    """Check that the apparent positive square cancels in the second jet."""

    e_t, e_tt, D, D_t = sp.symbols("e_t e_tt D D_t", real=True)
    nu, lam = sp.symbols("nu lambda", real=True)
    d, Y = sp.symbols("d Y", positive=True)
    d_t, Y_t = sp.symbols("d_t Y_t", real=True)
    pairing, mismatch_square = sp.symbols("I V", real=True)

    B = e_t + nu * D
    B_t = e_tt + nu * D_t
    ell = sp.Rational(1, 2) * (Y_t / Y + d_t / d)
    positive_square = pairing + mismatch_square

    # From B_t=<G_t,chi W>+I-lambda B.
    acceleration = B_t - pairing + lam * B
    residual = clean(acceleration - mismatch_square - B * ell)
    second_jet = clean(B_t + lam * B - B * ell)
    require(clean(positive_square + residual - second_jet) == 0,
            "positive square cancellation in the local-enstrophy jet")

    # Equivalent mismatch representation D=2*kappa^2*e-<chi W,H> is
    # recorded algebraically with lambda=nu*kappa^2.
    e, h_pair, kappa_sq = sp.symbols("e h_pair kappa_sq", real=True)
    d_mismatch = 2 * kappa_sq * e - h_pair
    b_mismatch = clean(e_t + nu * d_mismatch)
    expected = clean(e_t + 2 * lam * e - nu * h_pair)
    require(clean(b_mismatch.subs(kappa_sq, lam / nu) - expected) == 0,
            "annular mismatch representation of B")

    return {
        "passed": True,
        "localBalance": "B=e_t+nu*D_chi",
        "DChi": (
            "int chi |grad W|^2-(1/2)int (Delta chi)|W|^2"
            "=-<chi W,Delta W>"
        ),
        "acceleration": str(clean(acceleration)),
        "positiveSquare": str(positive_square),
        "residual": str(residual),
        "secondJetNumerator": str(second_jet),
        "mismatchFormOfB": str(expected),
        "conclusion": (
            "The displayed positive square cancels exactly against the same "
            "pairing inside <G_t,chi W>; the remaining numerator is a signed "
            "second-time/local-dissipation jet."
        ),
    }


def scaling_ledger() -> dict[str, object]:
    """Check NSE scaling of every numerator row and the complete scalar."""

    exponents = {
        "Y": sp.Rational(1),
        "d": sp.Rational(3),
        "B": sp.Rational(3),
        "z": sp.Rational(1),
        "G": sp.Rational(4),
        "G_t": sp.Rational(6),
        "W": sp.Rational(2),
        "H": sp.Rational(4),
        "dx": sp.Rational(-3),
        "logDerivative": sp.Rational(2),
        "kappa": sp.Rational(1),
        "dt": sp.Rational(-2),
    }
    root = clean((exponents["Y"] + exponents["d"]) / 2)
    acceleration = clean(exponents["G_t"] + exponents["W"] + exponents["dx"])
    mismatch = clean(2 * exponents["H"] + exponents["dx"])
    normalization = clean(exponents["B"] + exponents["logDerivative"])
    scalar = clean(acceleration - root)
    weighted_creation = clean(
        -2 * exponents["kappa"] + exponents["z"] + scalar + exponents["dt"]
    )
    require(root == 2, "sqrt(Yd) scaling")
    require(acceleration == mismatch == normalization == 5,
            "same-order signed numerator rows")
    require(scalar == 3, "J scaling")
    require(weighted_creation == 0, "critical weighted positive creation")

    return {
        "passed": True,
        "NSEScaling": "u_mu(t,x)=mu*u(mu^2*t,mu*x)",
        "rootExponent": str(root),
        "numeratorExponents": {
            "acceleration": str(acceleration),
            "annularMismatchSquare": str(mismatch),
            "normalization": str(normalization),
        },
        "JExponent": str(scalar),
        "kappaMinus2_z_J_dt_Exponent": str(weighted_creation),
        "boundary": (
            "Formal local Euclidean co-scaling of the filter and cutoff, not "
            "a continuous symmetry of one fixed torus or one fixed cell."
        ),
    }


def domain_boundary() -> dict[str, object]:
    """Record, rather than erase, the hard-denominator domain."""

    return {
        "passed": True,
        "identityDomain": ["Y>0", "d_Q>0", "fixed time-independent chi_Q"],
        "zeroFacts": [
            "Y=0 implies omega=0 and hence u=0 for zero-mean periodic data",
            "d_Q=0 implies C_Q=0 and B_Q=<F_j,C_Q>=0",
        ],
        "notCovered": [
            "the quotient z_Q at d_Q=0",
            "one-sided denominator faces",
            "partition refresh atoms",
            "moving cutoffs",
            "Leray-limit passage",
        ],
    }


def run() -> dict[str, object]:
    return {
        "release": "R0.71N",
        "status": "passed",
        "checks": {
            "fullScalarFusion": full_scalar_fusion(),
            "localEnstrophyFusion": local_enstrophy_fusion(),
            "scalingLedger": scaling_ledger(),
            "domainBoundary": domain_boundary(),
        },
        "claimBoundary": (
            "Exact fixed-cell algebra for classical periodic NSE only. The "
            "audit proves neither a sign or energy bound for the second-jet "
            "residual nor a continuation, singularity, or global-regularity result."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
