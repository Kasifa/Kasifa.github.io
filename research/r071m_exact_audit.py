#!/usr/bin/env python3
"""Exact structural audit for R0.71M.

The audit checks the algebra behind the annular Lamb commutator, the
fixed-cell projective pairing, the four-row absolute envelope, and the
scale ledger.  It also records the exponents of an L2-normalized heat-packet
family that separates Leray energy from several critical increment/Carleson
budgets.

The heat-packet calculation is a function-space implication test.  It is not
an NSE solution counterexample, and the absolute envelope checked here does
not rule out a smaller signed cancellation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def clean(value: sp.Expr | sp.MatrixBase) -> sp.Expr | sp.MatrixBase:
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: sp.factor(sp.simplify(entry)))
    return sp.factor(sp.simplify(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def matrix_is_zero(value: sp.MatrixBase) -> bool:
    return all(clean(entry) == 0 for entry in value)


def lamb_increment_identity() -> dict[str, object]:
    """Check the universal integrand reduction for the Lamb commutator.

    Write a=u(x-h), b=u(x), delta=a-b, and g=grad K_j(h).  Integration by
    parts gives the displayed raw density for

        T_j(u x curl u) - u x T_j(curl u).

    Its difference from the quadratic-increment density consists exactly of
    two terms killed after integration by int g=0 and div(T_j u)=0.
    """

    a = sp.Matrix(sp.symbols("a1:4", real=True))
    b = sp.Matrix(sp.symbols("b1:4", real=True))
    g = sp.Matrix(sp.symbols("g1:4", real=True))
    delta = a - b

    raw = g * (a.dot(a) / 2 - b.dot(a)) - a * g.dot(delta)
    increment = g * delta.dot(delta) / 2 - delta * g.dot(delta)
    cancellable = -g * b.dot(b) / 2 - b * g.dot(delta)
    residual = clean(raw - increment - cancellable)
    require(matrix_is_zero(residual), "Lamb commutator integrand reduction")

    return {
        "passed": True,
        "convention": "delta_h u(x)=u(x-h)-u(x)",
        "identity": (
            "R_j=int[(|delta_h u|^2/2) grad K_j"
            "-(grad K_j.delta_h u) delta_h u] dh"
        ),
        "rawMinusIncrement": [str(clean(entry)) for entry in cancellable],
        "cancellations": [
            "int grad K_j dh=0",
            "int grad K_j.delta_h u dh=div(T_j u)=0",
        ],
        "residual": [str(clean(entry)) for entry in residual],
        "boundary": (
            "The formula is exact for a translation-invariant scalar filter; "
            "it does not estimate curl(R_j) or a physical-cutoff term."
        ),
    }


def projective_pairing_identity() -> dict[str, object]:
    """Check the fixed-cell pairing with an exact self-adjoint curl model."""

    # D models the self-adjoint curl operator and X multiplication by chi_Q.
    d_op = sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 1]])
    cutoff = sp.diag(sp.Rational(2, 3), sp.Rational(4, 5), sp.Rational(7, 6))
    field = sp.Matrix([2, -1, 3])
    filtered_vorticity = sp.Matrix([1, 2, -1])
    viscous_mismatch = sp.Matrix([-2, 1, 4])
    viscosity = sp.Rational(3, 7)

    localized = clean(d_op * cutoff * filtered_vorticity)
    denominator = clean(localized.dot(localized))
    require(denominator != 0, "nonzero local denominator")
    work = clean(field.dot(localized))
    alpha = clean(work / denominator)
    projector = clean(sp.eye(3) - localized * localized.T / denominator)
    projected_field = clean(projector * field)
    source = clean(d_op * field)
    localized_source = clean(
        d_op * cutoff * (source + viscosity * viscous_mismatch)
    )

    left = clean(projected_field.dot(projector * localized_source))
    right = clean(
        (source - alpha * d_op * localized).dot(
            cutoff * (source + viscosity * viscous_mismatch)
        )
    )
    residual = clean(left - right)
    require(residual == 0, "projective pairing identity")

    signed_expansion = clean(
        source.dot(cutoff * source)
        + viscosity * source.dot(cutoff * viscous_mismatch)
        - alpha * (d_op * localized).dot(cutoff * source)
        - viscosity
        * alpha
        * (d_op * localized).dot(cutoff * viscous_mismatch)
    )
    require(clean(right - signed_expansion) == 0, "signed four-term expansion")

    return {
        "passed": True,
        "finiteExactModel": {
            "curlOperatorSelfAdjoint": [
                [str(entry) for entry in row] for row in d_op.tolist()
            ],
            "cutoffMultiplication": [
                [str(entry) for entry in row] for row in cutoff.tolist()
            ],
            "F": [str(entry) for entry in field],
            "W": [str(entry) for entry in filtered_vorticity],
            "H": [str(entry) for entry in viscous_mismatch],
            "nu": str(viscosity),
            "C": [str(entry) for entry in localized],
            "B": str(work),
            "d": str(denominator),
            "BOverD": str(alpha),
        },
        "left": str(left),
        "right": str(right),
        "residual": str(residual),
        "continuumIdentity": (
            "<P_Q F_j,P_Q M_Q>="
            "int chi_Q [G_j-(B_Q/d_Q)curl C_Q]."
            "[G_j+nu H_j]"
        ),
        "definitions": [
            "G_j=curl F_j",
            "H_j=(Delta+kappa_j^2)W_j",
            "C_Q=curl(chi_Q W_j)",
        ],
    }


def absolute_four_row_envelope() -> dict[str, object]:
    """Certify the constants in the direct four-row Cauchy envelope."""

    a, d, k, v = sp.symbols("A D K V", nonnegative=True)
    first_gap = clean(
        3 * (a**2 + d**2 + k**2) - (a + d + k) ** 2
    )
    second_gap = clean(
        3 * (a**2 + d**2 + v**2) - (a + d + v) ** 2
    )
    first_squares = clean((a - d) ** 2 + (a - k) ** 2 + (d - k) ** 2)
    second_squares = clean((a - d) ** 2 + (a - v) ** 2 + (d - v) ** 2)
    require(clean(first_gap - first_squares) == 0, "first three-row square bound")
    require(clean(second_gap - second_squares) == 0, "second three-row square bound")

    return {
        "passed": True,
        "cauchyStep": "|<g,h>_chi| <= (||g||_chi^2+||h||_chi^2)/2",
        "rows": {
            "A": "curl(u x W_j), resolved transport",
            "D": "curl R_j, increment commutator",
            "K": "(B_Q/d_Q) curl C_Q, projective denominator geometry",
            "V": "nu (Delta+kappa_j^2) W_j, viscous annular mismatch",
        },
        "bound": (
            "Theta_abs_Q <= gamma_abs_Q*kappa^-3*"
            "[3(A_Q^2+D_Q^2)+(3/2)(K_Q^2+V_Q^2)]"
        ),
        "gamma": "gamma_abs_Q=kappa_j*|B_Q|/(Y*d_Q)",
        "firstGapAsSquares": str(first_squares),
        "secondGapAsSquares": str(second_squares),
        "boundary": (
            "D is the split row built from the velocity-increment commutator; "
            "the known undifferentiated defect does not control it directly "
            "because no O(kappa_j) upper-frequency support holds in general.  "
            "The estimate is an "
            "absolute envelope and does not exclude signed cancellation in "
            "the exact pairing."
        ),
    }


def scale_ledger() -> dict[str, object]:
    """Check NSE scaling of the exact pairing and its critical rows."""

    exponents = {
        "kappa": sp.Rational(1),
        "z": sp.Rational(1),
        "sqrtY": sp.Rational(1, 2),
        "rQ": sp.Rational(3, 2),
        "G_L2": sp.Rational(5, 2),
        "dt": sp.Rational(-2),
    }
    gamma = clean(
        exponents["kappa"]
        + exponents["z"]
        - exponents["sqrtY"]
        - exponents["rQ"]
    )
    source_square = clean(
        -3 * exponents["kappa"]
        + 2 * exponents["G_L2"]
        + exponents["dt"]
    )
    tangent = clean(
        -2 * exponents["kappa"]
        + exponents["z"]
        - exponents["sqrtY"]
        - exponents["rQ"]
        + 2 * exponents["G_L2"]
        + exponents["dt"]
    )
    require(gamma == 0, "dimensionless gamma_Q")
    require(source_square == 0, "critical kappa^-3 source square")
    require(tangent == 0, "critical tangent pairing")

    return {
        "passed": True,
        "NSEScaling": "u_lambda(t,x)=lambda*u(lambda^2*t,lambda*x)",
        "scalingBoundary": (
            "formal local Euclidean scaling with the filter and cell cutoff "
            "co-scaled; not a continuous symmetry of one fixed torus/cutoff"
        ),
        "exponents": {key: str(value) for key, value in exponents.items()},
        "gammaExponent": str(gamma),
        "kappaMinus3SourceSquareExponent": str(source_square),
        "weightedTangentExponent": str(tangent),
        "kernelScaling": {
            "K_j": "kappa^3 K(kappa x)",
            "gradKjL1": "kappa ||grad K||_1",
            "H_jKernel": "kappa^5 (Delta+1)K(kappa x)",
            "gradHjL1": "kappa^3 ||grad((Delta+1)K)||_1",
            "viscousIncrementIdentity": (
                "(Delta+kappa^2)T_j omega="
                "int grad H_j(h) x delta_h u dh"
            ),
        },
    }


def heat_packet_separation() -> dict[str, object]:
    """Record exact scale exponents for the normalized heat-packet audit."""

    # u_r=r^-3/2 v(nu*t/r^2,x/r).  The numbers below are powers of r.
    packet = {
        "L2Norm": sp.Rational(0),
        "gradL2Squared": sp.Rational(-2),
        "parabolicTime": sp.Rational(2),
        "YuIncrementEnvelope": sp.Rational(-3, 2),
        "YuIncrementFourthSpatialMass": sp.Rational(-3),
        "projectedLambL2Squared": sp.Rational(-5),
        "enstrophy": sp.Rational(-2),
    }
    dissipation = clean(
        packet["gradL2Squared"] + packet["parabolicTime"]
    )
    yu_defect = clean(
        -1
        + packet["YuIncrementFourthSpatialMass"]
        + packet["parabolicTime"]
    )
    carleson = clean(-3 + 0 + packet["parabolicTime"])
    normalized_lamb = clean(
        packet["projectedLambL2Squared"]
        - packet["enstrophy"]
        + packet["parabolicTime"]
    )
    require(dissipation == 0, "uniform heat energy")
    require(yu_defect == -2, "Yu defect exponent")
    require(carleson == -1, "velocity Carleson exponent")
    require(normalized_lamb == -1, "normalized Lamb exponent")
    # The spatially integrated L3 increment cubed has exponent -3/2.
    cubic_increment_spatial = sp.Rational(-3, 2)
    critical_cubic_envelope = clean(
        -2 + cubic_increment_spatial + packet["parabolicTime"]
    )
    require(
        critical_cubic_envelope == sp.Rational(-3, 2),
        "critical cubic increment exponent",
    )

    return {
        "passed": True,
        "family": "u_r(t,x)=r^-3/2*(exp((nu*t/r^2)*Delta)Phi)((x-x0)/r)",
        "uniformEnergyExponent": str(dissipation),
        "divergentCriticalBudgets": {
            "YuDerivativeCompatibleDefect": str(yu_defect),
            "velocitySquareCarlesonMass": str(carleson),
            "normalizedProjectedLambIntegral": str(normalized_lamb),
            "criticalCubicIncrementEnvelope": str(critical_cubic_envelope),
        },
        "interpolationGap": "s_critical-s_energy=1/2 in dimension three",
        "claimBoundary": (
            "The packets are divergence-free heat flows on R^3 and prove a "
            "function-space non-implication.  They are not nonlinear NSE "
            "solutions and do not disprove an NSE-specific signed estimate."
        ),
    }


def build_payload() -> dict[str, object]:
    return {
        "release": "R0.71M",
        "status": "passed",
        "lambIncrementIdentity": lamb_increment_identity(),
        "projectivePairingIdentity": projective_pairing_identity(),
        "absoluteFourRowEnvelope": absolute_four_row_envelope(),
        "scaleLedger": scale_ledger(),
        "heatPacketSeparation": heat_packet_separation(),
        "claimBoundary": (
            "The audit proves exact filter/projector identities, an absolute "
            "conditional envelope, and a function-space separation.  It "
            "proves no continuation criterion, regularity theorem, finite-time "
            "singularity, originality claim, or Millennium-problem result."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    payload = build_payload()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
