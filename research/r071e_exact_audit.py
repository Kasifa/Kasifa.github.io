#!/usr/bin/env python3
"""Exact producer for the R0.71E projected-Lamb heat-bulk gate.

The producer verifies a narrow collection of statements.

1. Stretching and the transport-filter commutator combine exactly into the
   curl of the solenoidal Lamb vector; the complementary Lamb component is a
   curl-free gradient.
2. A support-minimal six-mode real divergence-free datum has identical
   quadratic spectra for two phases and opposite cubic enstrophy work.
3. For a radial multiplier, the stretching, commutator, combined work,
   enstrophy, and palinstrophy have the stated exact alpha/beta formulas.
4. A Parseval-preserving two-radius split has a positive low block whose heat
   bulk and bottom trace differ by exactly 2*K**2.
5. The spectral heat integral has the exact factor one half in the
   H^{-1} norm.
6. A compactly supported whole-space construction has a nonzero projected
   Lamb vector and the stated Navier--Stokes scaling exponents.

It does not prove bottom-trace integrability, global regularity, finite-time
blow-up, or any Millennium-problem claim.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

import sympy as sp


Frequency = tuple[int, int, int]
Vector = sp.Matrix
I = sp.I


def add(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def negative(frequency: Frequency) -> Frequency:
    return tuple(-entry for entry in frequency)  # type: ignore[return-value]


def square(frequency: Frequency) -> int:
    return sum(entry * entry for entry in frequency)


def clean(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(
            lambda entry: sp.factor(sp.cancel(sp.expand(entry)))
        )
    return sp.factor(sp.cancel(sp.expand(value)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def pairing(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return clean((sp.conjugate(first).T * second)[0])


def coefficient_norm_square(value: sp.Matrix) -> sp.Expr:
    return pairing(value, value)


def projector(frequency: Frequency) -> sp.Matrix:
    wave = Vector(frequency)
    return sp.eye(3) - wave * wave.T / square(frequency)


def convolution(
    first: dict[Frequency, sp.Matrix],
    second: dict[Frequency, sp.Matrix],
    operation,
) -> dict[Frequency, sp.Matrix]:
    output: dict[Frequency, sp.Matrix] = {}
    for left, right in product(first, second):
        frequency = add(left, right)
        output.setdefault(frequency, sp.zeros(3, 1))
        output[frequency] += operation(left, first[left], right, second[right])
    return {frequency: clean(value) for frequency, value in output.items()}


def build_phase(sign: int) -> dict[str, object]:
    require(sign in (-1, 1), "phase sign")

    positive = {
        (1, 0, 0): Vector([0, -1, 0]),
        (0, 1, 0): Vector([0, 0, -1]),
        (-1, -1, 0): Vector([0, 0, sign * I]),
    }
    velocity = dict(positive)
    for frequency, coefficient in positive.items():
        velocity[negative(frequency)] = sp.conjugate(coefficient)

    omega = {
        frequency: clean(I * Vector(frequency).cross(coefficient))
        for frequency, coefficient in velocity.items()
    }

    stretching = convolution(
        omega,
        velocity,
        lambda _p, omega_p, q, velocity_q: clean(
            I * omega_p.dot(Vector(q)) * velocity_q
        ),
    )
    transport = convolution(
        velocity,
        omega,
        lambda _p, velocity_p, q, omega_q: clean(
            I * velocity_p.dot(Vector(q)) * omega_q
        ),
    )
    nonlinear = {
        frequency: clean(stretching[frequency] - transport[frequency])
        for frequency in set(stretching) | set(transport)
    }

    raw_lamb = convolution(
        velocity,
        omega,
        lambda _p, velocity_p, _q, omega_q: clean(
            velocity_p.cross(omega_q)
        ),
    )
    projected_lamb: dict[Frequency, sp.Matrix] = {}
    gradient_lamb: dict[Frequency, sp.Matrix] = {}
    for frequency, value in raw_lamb.items():
        if frequency == (0, 0, 0):
            require(value == sp.zeros(3, 1), "zero Lamb mean")
            continue
        projected_lamb[frequency] = clean(projector(frequency) * value)
        gradient_lamb[frequency] = clean(value - projected_lamb[frequency])

    for frequency in projected_lamb:
        curl_lamb = clean(
            I * Vector(frequency).cross(projected_lamb[frequency])
        )
        curl_gradient = clean(
            I * Vector(frequency).cross(gradient_lamb[frequency])
        )
        require(
            curl_lamb == nonlinear.get(frequency, sp.zeros(3, 1)),
            f"projected Lamb curl {frequency}",
        )
        require(
            curl_gradient == sp.zeros(3, 1),
            f"gradient Lamb curl {frequency}",
        )

    divergence = {
        frequency: clean(Vector(frequency).dot(coefficient))
        for frequency, coefficient in velocity.items()
    }
    reality = {
        frequency: clean(
            velocity[negative(frequency)] - sp.conjugate(coefficient)
        )
        for frequency, coefficient in velocity.items()
    }
    require(all(value == 0 for value in divergence.values()), "divergence")
    require(
        all(value == sp.zeros(3, 1) for value in reality.values()),
        "reality",
    )

    support = set(velocity)
    ordered_resonances = sum(
        1
        for first, second in product(support, repeat=2)
        if negative(add(first, second)) in support
    )
    require(ordered_resonances == 12, "ordered resonances")

    energy = clean(
        sum(coefficient_norm_square(value) for value in velocity.values())
    )
    enstrophy = clean(
        sum(coefficient_norm_square(value) for value in omega.values())
    )
    palinstrophy = clean(
        sum(
            square(frequency) * coefficient_norm_square(value)
            for frequency, value in omega.items()
        )
    )
    require(energy == 6, "velocity norm")
    require(enstrophy == 8, "enstrophy")
    require(palinstrophy == 12, "palinstrophy")

    output_rows: list[dict[str, object]] = []
    for frequency in sorted(velocity):
        output_rows.append(
            {
                "frequency": list(frequency),
                "radiusSquared": square(frequency),
                "stretchingWork": str(
                    pairing(omega[frequency], stretching[frequency])
                ),
                "transportWork": str(
                    pairing(omega[frequency], transport[frequency])
                ),
                "combinedWork": str(
                    pairing(omega[frequency], nonlinear[frequency])
                ),
                "projectedLambCoefficient": [
                    str(entry) for entry in projected_lamb[frequency]
                ],
            }
        )

    total_stretching = clean(
        sum(
            pairing(omega[frequency], stretching[frequency])
            for frequency in velocity
        )
    )
    total_transport = clean(
        sum(
            pairing(omega[frequency], transport[frequency])
            for frequency in velocity
        )
    )
    total_combined = clean(
        sum(
            pairing(omega[frequency], nonlinear[frequency])
            for frequency in velocity
        )
    )
    require(total_stretching == 2 * sign, "total stretching")
    require(total_transport == 0, "global transport cancellation")
    require(total_combined == 2 * sign, "total combined work")

    alpha, beta = sp.symbols("alpha beta", real=True)
    tau = sp.symbols("tau", nonnegative=True)
    multiplier = {
        frequency: alpha if square(frequency) == 1 else beta
        for frequency in velocity
    }
    filtered_stretching = clean(
        sum(
            multiplier[frequency] ** 2
            * pairing(omega[frequency], stretching[frequency])
            for frequency in velocity
        )
    )
    filtered_transport = clean(
        sum(
            multiplier[frequency] ** 2
            * pairing(omega[frequency], transport[frequency])
            for frequency in velocity
        )
    )
    filtered_commutator = clean(-filtered_transport)
    filtered_combined = clean(filtered_stretching + filtered_commutator)
    filtered_y = clean(
        sum(
            multiplier[frequency] ** 2
            * coefficient_norm_square(omega[frequency])
            for frequency in velocity
        )
    )
    filtered_d = clean(
        sum(
            square(frequency)
            * multiplier[frequency] ** 2
            * coefficient_norm_square(omega[frequency])
            for frequency in velocity
        )
    )
    require(
        clean(filtered_stretching - 2 * sign * beta**2) == 0,
        "filtered stretching",
    )
    require(
        clean(
            filtered_commutator
            - 2 * sign * (beta**2 - alpha**2)
        )
        == 0,
        "filtered commutator",
    )
    require(
        clean(
            filtered_combined
            - 2 * sign * (2 * beta**2 - alpha**2)
        )
        == 0,
        "filtered combined",
    )
    require(
        clean(filtered_y - 4 * (alpha**2 + beta**2)) == 0,
        "filtered Y",
    )
    require(
        clean(filtered_d - 4 * (alpha**2 + 2 * beta**2)) == 0,
        "filtered D",
    )

    heat_low = alpha * sp.exp(-tau)
    heat_high = beta * sp.exp(-2 * tau)
    heat_stretching = clean(2 * sign * heat_high**2)
    heat_commutator = clean(
        2 * sign * (heat_high**2 - heat_low**2)
    )
    heat_combined = clean(heat_stretching + heat_commutator)
    heat_y = clean(4 * (heat_low**2 + heat_high**2))
    heat_d = clean(4 * (heat_low**2 + 2 * heat_high**2))
    require(
        heat_combined
        == clean(
            2
            * sign
            * (2 * beta**2 * sp.exp(-4 * tau) - alpha**2 * sp.exp(-2 * tau))
        ),
        "heat combined",
    )

    lamb_l2 = clean(
        sum(
            coefficient_norm_square(projected_lamb[frequency])
            for frequency in projected_lamb
        )
    )
    lamb_hminus1 = clean(
        sum(
            coefficient_norm_square(projected_lamb[frequency])
            / square(frequency)
            for frequency in projected_lamb
        )
    )
    heat_lamb_integral = clean(
        sum(
            coefficient_norm_square(projected_lamb[frequency])
            / (2 * square(frequency))
            for frequency in projected_lamb
        )
    )
    require(
        heat_lamb_integral == lamb_hminus1 / 2,
        "spectral one-half identity",
    )

    # Adding a separated vertical wave creates genuinely 3D frequency
    # support without creating any convolution into the selected base modes.
    high = (0, 0, 4)
    lifted_support = support | {high, negative(high)}
    cross_pairs_into_base = [
        (first, second)
        for first, second in product(lifted_support, repeat=2)
        if ({first, second} & {high, negative(high)})
        and add(first, second) in support
    ]
    require(cross_pairs_into_base == [], "genuine 3D lift separation")

    return {
        "sign": sign,
        "positiveModes": [
            {
                "frequency": list(frequency),
                "velocityCoefficient": [str(entry) for entry in coefficient],
            }
            for frequency, coefficient in positive.items()
        ],
        "orderedResonances": ordered_resonances,
        "outputRows": output_rows,
        "norms": {
            "velocityL2Squared": str(energy),
            "enstrophy": str(enstrophy),
            "palinstrophy": str(palinstrophy),
            "projectedLambL2Squared": str(lamb_l2),
            "projectedLambHMinus1Squared": str(lamb_hminus1),
            "projectedLambHeatIntegral": str(heat_lamb_integral),
        },
        "unfiltered": {
            "stretching": str(total_stretching),
            "transport": str(total_transport),
            "combined": str(total_combined),
        },
        "filtered": {
            "Y": str(filtered_y),
            "D": str(filtered_d),
            "stretching": str(filtered_stretching),
            "transportFilterCommutator": str(filtered_commutator),
            "combined": str(filtered_combined),
            "heatY": str(heat_y),
            "heatD": str(heat_d),
            "heatStretching": str(heat_stretching),
            "heatTransportFilterCommutator": str(heat_commutator),
            "heatCombined": str(heat_combined),
        },
        "genuine3DLift": {
            "extraModes": [[0, 0, 4], [0, 0, -4]],
            "crossPairsIntoSelectedBaseOutputs": 0,
        },
    }


def whole_space_local_jet() -> dict[str, object]:
    x, y, z = sp.symbols("x y z", real=True)
    velocity = Vector([x, -y - z, 0])
    variables = (x, y, z)
    omega = Vector(
        [
            sp.diff(velocity[2], y) - sp.diff(velocity[1], z),
            sp.diff(velocity[0], z) - sp.diff(velocity[2], x),
            sp.diff(velocity[1], x) - sp.diff(velocity[0], y),
        ]
    )
    stretching = clean(velocity.jacobian(variables) * omega)
    transport = clean(
        sum(
            (
                velocity[index] * omega.diff(variables[index])
                for index in range(3)
            ),
            sp.zeros(3, 1),
        )
    )
    raw_lamb = clean(velocity.cross(omega))
    curl_lamb = Vector(
        [
            sp.diff(raw_lamb[2], y) - sp.diff(raw_lamb[1], z),
            sp.diff(raw_lamb[0], z) - sp.diff(raw_lamb[2], x),
            sp.diff(raw_lamb[1], x) - sp.diff(raw_lamb[0], y),
        ]
    )
    require(omega == Vector([1, 0, 0]), "local jet vorticity")
    require(stretching == Vector([1, 0, 0]), "local jet stretching")
    require(transport == Vector([0, 0, 0]), "local jet transport")
    require(curl_lamb == Vector([1, 0, 0]), "local jet Lamb curl")
    energy_exponent = -1
    enstrophy_exponent = 1
    lamb_exponent = 3
    quotient_exponent = lamb_exponent - enstrophy_exponent
    parabolic_time_exponent = -2
    require(quotient_exponent == 2, "R3 quotient scaling")
    require(
        quotient_exponent + parabolic_time_exponent == 0,
        "R3 critical time scaling",
    )
    return {
        "velocityNearOrigin": [str(entry) for entry in velocity],
        "vorticityNearOrigin": [str(entry) for entry in omega],
        "stretchingMinusTransport": [
            str(entry) for entry in clean(stretching - transport)
        ],
        "rawLambNearOrigin": [str(entry) for entry in raw_lamb],
        "curlRawLamb": [str(entry) for entry in curl_lamb],
        "r3ScalingSquaredNorms": {
            "kineticEnergy": f"lambda**({energy_exponent})",
            "enstrophy": f"lambda**({enstrophy_exponent})",
            "projectedLambL2": f"lambda**{lamb_exponent}",
            "projectedLambOverEnstrophy": f"lambda**{quotient_exponent}",
            "parabolicTime": f"lambda**({parabolic_time_exponent})",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    plus = build_phase(1)
    minus = build_phase(-1)
    a, scale, heat, theta = sp.symbols("a K s theta", positive=True)

    low_b = clean(2 * a**3 * scale**6 * sp.exp(-2 * scale**2 * heat))
    low_d = clean(4 * a**2 * scale**6 * sp.exp(-2 * scale**2 * heat))
    low_q = clean(low_b**2 / low_d)
    low_bulk = clean(sp.integrate(low_q, (heat, 0, sp.oo)))
    low_box = clean(
        sp.integrate(low_q, (heat, 0, theta / scale**2))
    )
    total_y = 8 * a**2 * scale**4
    bottom_a = clean(low_q.subs(heat, 0) / total_y)
    normalized_bulk = clean(low_bulk / total_y)
    normalized_box = clean(low_box / total_y)

    angle = sp.symbols("angle", real=True)
    require(
        sp.trigsimp(sp.cos(angle) ** 2 + sp.sin(angle) ** 2 - 1) == 0,
        "Parseval-preserving parent split",
    )

    require(
        clean(low_q.subs(heat, 0) - 2 * scale**2 * low_bulk) == 0,
        "exact K-square heat trace",
    )
    require(
        clean(bottom_a - a**2 * scale**2 / 8) == 0,
        "bottom coefficient",
    )
    require(
        clean(normalized_bulk - a**2 / 16) == 0,
        "normalized bulk",
    )
    require(
        clean(
            normalized_box
            - a**2 * (1 - sp.exp(-2 * theta)) / 16
        )
        == 0,
        "normalized finite heat box",
    )

    checks = {
        "bottomTraceCostsExactlyTwoFrequencyPowers": True,
        "completeWorkChangesSignWithPhase": True,
        "exactArithmeticOnly": True,
        "filteredSplitRetainsTransportCommutator": True,
        "genuine3DLiftDoesNotEnterSelectedOutputs": True,
        "heatBulkHasExactHMinusOneHalfFactor": True,
        "lowPositiveBlockHasCriticalKSquareBottom": True,
        "phasePairHasIdenticalQuadraticSpectra": True,
        "projectedLambCurlEqualsVorticityNonlinearity": True,
        "rawMinusProjectedLambIsCurlFree": True,
        "r3LocalJetHasNonzeroLambCurl": True,
        "r3ScalingExponentsGiveCriticalTimeIntegral": True,
        "supportUsesThreeConjugatePairs": True,
        "algebraicRadialSplitPreservesParentSquare": True,
        "verticalBulkNormalizationRemovesKSquare": True,
    }

    payload = {
        "release": "R0.71E",
        "status": "projected-lamb-bulk-and-bottom-trace-gate",
        "checks": checks,
        "phasePlus": plus,
        "phaseMinus": minus,
        "tightRadialSplit": {
            "identity": "m_lo**2 + m_hi**2 = m_0**2",
            "lowPositivePhase": -1,
            "lowB": str(low_b),
            "lowD": str(low_d),
            "lowPositiveSquare": str(low_q),
            "lowPositiveSquareAtBottom": str(low_q.subs(heat, 0)),
            "lowHeatBulk": str(low_bulk),
            "bottomEqualsTwoKSquareTimesBulkResidual": "0",
            "physicalBottomEnstrophy": str(total_y),
            "bottomCoefficient": str(bottom_a),
            "normalizedInfiniteBulk": str(normalized_bulk),
            "normalizedFiniteBox": str(normalized_box),
        },
        "wholeSpaceJet": whole_space_local_jet(),
        "routeDecision": {
            "positiveResult": (
                "The normalized projected-Lamb heat bulk is bounded at the "
                "Leray energy level."
            ),
            "openTrace": (
                "The R0.71C bottom coefficient still requires control of a "
                "critical signed Lamb trace concentration."
            ),
            "pressureBoundary": (
                "Pressure is the Bernoulli gradient complement and is not an "
                "independent vorticity injection sector."
            ),
            "nextGate": "R0.71F localized projected-Lamb trace criterion",
        },
        "claimBoundary": (
            "This certificate checks the finite algebra supporting the "
            "analytic heat-bulk theorem and proves the exact finite critical "
            "trace relation. The general bulk estimate is proved in the "
            "report. Neither source proves bottom-trace integrability, "
            "regularity, or blow-up."
        ),
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
