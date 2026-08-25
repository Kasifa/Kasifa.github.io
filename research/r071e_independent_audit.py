#!/usr/bin/env python3
"""Independent real-space checker for R0.71E.

This script deliberately imports no project audit module.  It reconstructs
the six-mode datum from trigonometric functions, differentiates it in
physical space, projects its two output radii by explicit formulas, verifies
the solenoidal Lamb representation, and recomputes the heat trace.  A plain
floating-point midpoint rule supplies an additional non-symbolic sanity
check.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import sympy as sp


x, y, z = sp.symbols("x y z", real=True)


def clean(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(
            lambda entry: sp.factor(sp.cancel(sp.trigsimp(sp.expand(entry))))
        )
    return sp.factor(sp.cancel(sp.trigsimp(sp.expand(value))))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def normalized_average(expression: sp.Expr) -> sp.Expr:
    return clean(
        sp.integrate(
            sp.integrate(sp.expand_trig(expression), (x, 0, 2 * sp.pi)),
            (y, 0, 2 * sp.pi),
        )
        / (2 * sp.pi) ** 2
    )


def curl(field: sp.Matrix) -> sp.Matrix:
    return clean(
        sp.Matrix(
            [
                sp.diff(field[2], y) - sp.diff(field[1], z),
                sp.diff(field[0], z) - sp.diff(field[2], x),
                sp.diff(field[1], x) - sp.diff(field[0], y),
            ]
        )
    )


def divergence(field: sp.Matrix) -> sp.Expr:
    return clean(
        sp.diff(field[0], x)
        + sp.diff(field[1], y)
        + sp.diff(field[2], z)
    )


def gradient_square(field: sp.Matrix) -> sp.Expr:
    return clean(
        sum(
            sp.diff(field[row], variable) ** 2
            for row in range(3)
            for variable in (x, y, z)
        )
    )


def build_physical_phase(sign: int) -> dict[str, object]:
    velocity = sp.Matrix(
        [
            0,
            -2 * sp.cos(x),
            2 * sign * sp.sin(x + y) - 2 * sp.cos(y),
        ]
    )
    omega = curl(velocity)
    expected_omega = sp.Matrix(
        [
            2 * sign * sp.cos(x + y) + 2 * sp.sin(y),
            -2 * sign * sp.cos(x + y),
            2 * sp.sin(x),
        ]
    )
    require(divergence(velocity) == 0, "physical divergence")
    require(clean(omega - expected_omega) == sp.zeros(3, 1), "physical curl")

    variables = (x, y, z)
    stretching = clean(velocity.jacobian(variables) * omega)
    transport = clean(
        sum(
            (velocity[index] * omega.diff(variables[index]) for index in range(3)),
            sp.zeros(3, 1),
        )
    )
    nonlinear = clean(stretching - transport)

    omega_low = sp.Matrix([2 * sp.sin(y), 0, 2 * sp.sin(x)])
    omega_high = sp.Matrix(
        [
            2 * sign * sp.cos(x + y),
            -2 * sign * sp.cos(x + y),
            0,
        ]
    )
    require(
        clean(omega - omega_low - omega_high) == sp.zeros(3, 1),
        "two-radius vorticity split",
    )

    # The horizontal field is a shear.  The third component is a passive
    # scalar w, so L_3=-v dot grad w.  This reconstructs the full projected
    # Lamb field, including nonlinear frequencies outside the original
    # six-mode support.
    projected_lamb = sp.Matrix(
        [
            0,
            0,
            4
            * sp.cos(x)
            * (sign * sp.cos(x + y) + sp.sin(y)),
        ]
    )
    raw_lamb = clean(velocity.cross(omega))
    gradient_remainder = clean(raw_lamb - projected_lamb)
    require(
        clean(curl(projected_lamb) - nonlinear) == sp.zeros(3, 1),
        "physical projected Lamb curl",
    )
    require(
        curl(gradient_remainder) == sp.zeros(3, 1),
        "physical Lamb gradient remainder",
    )
    require(divergence(projected_lamb) == 0, "physical Lamb solenoidal")

    energy = normalized_average(velocity.dot(velocity))
    enstrophy = normalized_average(omega.dot(omega))
    palinstrophy = normalized_average(gradient_square(omega))
    stretching_work = normalized_average(omega.dot(stretching))
    transport_work = normalized_average(omega.dot(transport))
    combined_work = normalized_average(omega.dot(nonlinear))
    low_works = tuple(
        normalized_average(omega_low.dot(value))
        for value in (stretching, transport, nonlinear)
    )
    high_works = tuple(
        normalized_average(omega_high.dot(value))
        for value in (stretching, transport, nonlinear)
    )

    require(energy == 6, "physical energy")
    require(enstrophy == 8, "physical enstrophy")
    require(palinstrophy == 12, "physical palinstrophy")
    require(stretching_work == 2 * sign, "physical stretching work")
    require(transport_work == 0, "physical transport cancellation")
    require(combined_work == 2 * sign, "physical combined work")
    require(low_works == (0, 2 * sign, -2 * sign), "physical low works")
    require(
        high_works == (2 * sign, -2 * sign, 4 * sign),
        "physical high works",
    )

    # The horizontal velocity is a shear, so its nonlinear advection is zero.
    horizontal = sp.Matrix([velocity[0], velocity[1]])
    horizontal_advection = clean(
        velocity[0] * horizontal.diff(x) + velocity[1] * horizontal.diff(y)
    )
    require(
        horizontal_advection == sp.zeros(2, 1),
        "2D3C horizontal shear",
    )

    return {
        "sign": sign,
        "velocity": [str(entry) for entry in velocity],
        "vorticity": [str(entry) for entry in omega],
        "projectedLamb": [str(entry) for entry in projected_lamb],
        "gradientRemainderCurl": [str(entry) for entry in curl(gradient_remainder)],
        "norms": {
            "velocityL2Squared": str(energy),
            "enstrophy": str(enstrophy),
            "palinstrophy": str(palinstrophy),
        },
        "works": {
            "stretching": str(stretching_work),
            "transport": str(transport_work),
            "combined": str(combined_work),
            "lowRadiusStretchTransportCombined": [
                str(value) for value in low_works
            ],
            "highRadiusStretchTransportCombined": [
                str(value) for value in high_works
            ],
        },
        "twoDThreeComponentStructure": {
            "horizontalAdvection": [str(entry) for entry in horizontal_advection],
            "thirdComponentEquation": (
                "linear advection-diffusion driven by the decaying horizontal shear"
            ),
        },
    }


def independent_heat_trace() -> dict[str, object]:
    heat, scale, amplitude, theta = sp.symbols(
        "s K a theta", positive=True
    )
    # The sign -1 phase has positive combined work on the low-radius block.
    bottom_y = 8 * amplitude**2 * scale**4
    b = 2 * amplitude**3 * scale**6 * sp.exp(-2 * scale**2 * heat)
    d = 4 * amplitude**2 * scale**6 * sp.exp(-2 * scale**2 * heat)
    q = clean(b**2 / d)
    bulk = clean(sp.integrate(q, (heat, 0, sp.oo)))
    box = clean(sp.integrate(q, (heat, 0, theta / scale**2)))
    bottom = clean(q.subs(heat, 0) / bottom_y)
    normalized_bulk = clean(bulk / bottom_y)
    normalized_box = clean(box / bottom_y)

    require(
        clean(q.subs(heat, 0) - 2 * scale**2 * bulk) == 0,
        "independent trace identity",
    )
    require(
        clean(bottom - amplitude**2 * scale**2 / 8) == 0,
        "independent bottom",
    )
    require(
        clean(normalized_bulk - amplitude**2 / 16) == 0,
        "independent normalized bulk",
    )
    require(
        clean(
            normalized_box
            - amplitude**2 * (1 - sp.exp(-2 * theta)) / 16
        )
        == 0,
        "independent heat box",
    )
    return {
        "positivePhase": -1,
        "bLow": str(b),
        "dLow": str(d),
        "positiveSquare": str(q),
        "heatBulk": str(bulk),
        "bottomOverPhysicalY": str(bottom),
        "normalizedInfiniteBulk": str(normalized_bulk),
        "normalizedFiniteBox": str(normalized_box),
        "bottomEqualsTwoKSquareTimesBulkResidual": "0",
    }


def midpoint_sanity(grid: int = 96) -> dict[str, object]:
    totals = {
        "energy": 0.0,
        "enstrophy": 0.0,
        "palinstrophy": 0.0,
        "stretching": 0.0,
        "transport": 0.0,
        "combined": 0.0,
    }
    for ix in range(grid):
        px = 2 * math.pi * (ix + 0.5) / grid
        for iy in range(grid):
            py = 2 * math.pi * (iy + 0.5) / grid
            u2 = -2 * math.cos(px)
            u3 = 2 * math.sin(px + py) - 2 * math.cos(py)
            omega1 = 2 * math.cos(px + py) + 2 * math.sin(py)
            omega2 = -2 * math.cos(px + py)
            omega3 = 2 * math.sin(px)

            # Explicit derivatives for sigma=+1.
            stretch1 = 0.0
            stretch2 = omega1 * (2 * math.sin(px))
            stretch3 = (
                omega1 * 2 * math.cos(px + py)
                + omega2
                * (2 * math.cos(px + py) + 2 * math.sin(py))
            )
            transport1 = u2 * (
                -2 * math.sin(px + py) + 2 * math.cos(py)
            )
            transport2 = u2 * 2 * math.sin(px + py)
            transport3 = 0.0

            grad_omega_square = (
                (-2 * math.sin(px + py)) ** 2
                + (-2 * math.sin(px + py) + 2 * math.cos(py)) ** 2
                + (2 * math.sin(px + py)) ** 2
                + (2 * math.sin(px + py)) ** 2
                + (2 * math.cos(px)) ** 2
            )

            stretch_dot = (
                omega1 * stretch1 + omega2 * stretch2 + omega3 * stretch3
            )
            transport_dot = (
                omega1 * transport1
                + omega2 * transport2
                + omega3 * transport3
            )
            totals["energy"] += u2 * u2 + u3 * u3
            totals["enstrophy"] += (
                omega1 * omega1 + omega2 * omega2 + omega3 * omega3
            )
            totals["palinstrophy"] += grad_omega_square
            totals["stretching"] += stretch_dot
            totals["transport"] += transport_dot
            totals["combined"] += stretch_dot - transport_dot

    denominator = float(grid * grid)
    averages = {key: value / denominator for key, value in totals.items()}
    expected = {
        "energy": 6.0,
        "enstrophy": 8.0,
        "palinstrophy": 12.0,
        "stretching": 2.0,
        "transport": 0.0,
        "combined": 2.0,
    }
    errors = {key: abs(averages[key] - expected[key]) for key in expected}
    require(max(errors.values()) < 1e-11, "midpoint sanity")
    return {
        "grid": [grid, grid],
        "averages": averages,
        "maximumAbsoluteError": max(errors.values()),
    }


def whole_space_scaling_check() -> dict[str, object]:
    velocity = sp.Matrix([x, -y - z, 0])
    omega = curl(velocity)
    variables = (x, y, z)
    stretching = clean(velocity.jacobian(variables) * omega)
    transport = clean(
        sum(
            (velocity[index] * omega.diff(variables[index]) for index in range(3)),
            sp.zeros(3, 1),
        )
    )
    lamb = clean(velocity.cross(omega))
    require(omega == sp.Matrix([1, 0, 0]), "independent local omega")
    require(
        clean(stretching - transport) == sp.Matrix([1, 0, 0]),
        "independent local nonlinearity",
    )
    require(curl(lamb) == sp.Matrix([1, 0, 0]), "independent local Lamb curl")
    return {
        "localVelocity": [str(entry) for entry in velocity],
        "localVorticity": [str(entry) for entry in omega],
        "localLamb": [str(entry) for entry in lamb],
        "curlLocalLamb": [str(entry) for entry in curl(lamb)],
        "scaling": {
            "energySquaredNorm": "lambda**(-1)",
            "enstrophySquaredNorm": "lambda",
            "LambSquaredNorm": "lambda**3",
            "LambOverEnstrophy": "lambda**2",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    plus = build_physical_phase(1)
    minus = build_physical_phase(-1)
    require(plus["norms"] == minus["norms"], "independent equal norms")
    require(
        plus["works"]["combined"] == "2"
        and minus["works"]["combined"] == "-2",
        "independent phase sign pair",
    )

    payload = {
        "version": "R0.71E-independent",
        "status": "pass",
        "checks": {
            "importsNoProjectAuditModule": True,
            "physicalCurlMatchesStatedVorticity": True,
            "physicalProjectedLambCurlMatchesNonlinearity": True,
            "gradientLambRemainderIsCurlFree": True,
            "phasePairHasEqualQuadraticNorms": True,
            "phasePairHasOppositeCombinedWork": True,
            "lowAndHighOutputWorkTablesClose": True,
            "twoDThreeComponentShearReductionIsVerified": True,
            "heatTraceCostsExactlyTwoFrequencyPowers": True,
            "finiteHeatBoxIsScaleIndependent": True,
            "wholeSpaceLocalJetHasNonzeroLambCurl": True,
            "plainMidpointQuadratureMatchesExactAverages": True,
        },
        "phasePlus": plus,
        "phaseMinus": minus,
        "heatTrace": independent_heat_trace(),
        "wholeSpaceScaling": whole_space_scaling_check(),
        "floatingPointSanity": midpoint_sanity(),
        "claimBoundary": (
            "The checker confirms an exact smooth trace obstruction and the "
            "projected-Lamb identities. It does not infer singularity, "
            "bottom-trace integrability, or global regularity."
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
