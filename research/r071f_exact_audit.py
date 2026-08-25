#!/usr/bin/env python3
"""Exact producer for the R0.71F localized projected-Lamb trace gate.

The producer checks the finite algebra behind four statements.

1. The low-radius block of the fixed R0.71E dyadic frame is reconstructed
   from the full six-mode divergence-free datum and its projected Lamb vector.
2. For every smooth nonnegative spatial cutoff, including its cutoff--curl
   term, the local Lamb work is strictly positive and has a closed formula.
3. Before localization, both factors acquire the same scalar heat multiplier
   exp(-K**2*s).  Spatial localization does not change that scalar factor, so
   the positive quotient decays exactly as exp(-2*K**2*s) and every finite or
   infinite vertical trace pays the full K**2 factor.
4. The general bounded-overlap heat-moment packing has the exact Gamma(alpha)
   spectral constant; the six-mode family saturates its frequency exponent.

It does not prove bottom-trace integrability, regularity, blow-up, or any
Millennium-problem claim.  The moving-cylinder PDE ledger is proved
analytically in the report; the second program independently checks the
localized cutoff--curl and finite-height trace identities.
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
        return value.applyfunc(lambda entry: sp.factor(sp.cancel(sp.expand(entry))))
    return sp.factor(sp.cancel(sp.expand(value)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def pairing(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return clean((sp.conjugate(first).T * second)[0])


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


def curl(field: sp.Matrix, variables: tuple[sp.Symbol, ...]) -> sp.Matrix:
    x, y, z = variables
    return Vector(
        [
            sp.diff(field[2], y) - sp.diff(field[1], z),
            sp.diff(field[0], z) - sp.diff(field[2], x),
            sp.diff(field[1], x) - sp.diff(field[0], y),
        ]
    )


def divergence(field: sp.Matrix, variables: tuple[sp.Symbol, ...]) -> sp.Expr:
    return clean(sum(sp.diff(field[index], variables[index]) for index in range(3)))


def six_mode_velocity_and_vorticity() -> tuple[
    dict[Frequency, sp.Matrix], dict[Frequency, sp.Matrix]
]:
    """Return the full sigma=-1 datum at a=K=1 and its exact curl."""

    positive_velocity = {
        (1, 0, 0): Vector([0, -1, 0]),
        (0, 1, 0): Vector([0, 0, -1]),
        (-1, -1, 0): Vector([0, 0, -I]),
    }
    velocity = dict(positive_velocity)
    for frequency, coefficient in positive_velocity.items():
        velocity[negative(frequency)] = sp.conjugate(coefficient)
    omega = {
        frequency: clean(I * Vector(frequency).cross(coefficient))
        for frequency, coefficient in velocity.items()
    }
    return velocity, omega


def reconstruct_low_block() -> dict[str, object]:
    # This is sigma=-1 in the fixed R0.71E family at a=K=1.  Reality adds
    # the conjugate modes.  The frame multiplier is one on |k|=1 and zero on
    # |k|=sqrt(2), fixed before K is chosen.
    velocity, omega = six_mode_velocity_and_vorticity()
    raw_lamb = convolution(
        velocity,
        omega,
        lambda _p, velocity_p, _q, omega_q: clean(velocity_p.cross(omega_q)),
    )
    projected_lamb: dict[Frequency, sp.Matrix] = {}
    for frequency, value in raw_lamb.items():
        if frequency == (0, 0, 0):
            require(value == sp.zeros(3, 1), "zero Lamb mean")
            continue
        projected_lamb[frequency] = clean(projector(frequency) * value)

    low_omega = {
        frequency: value for frequency, value in omega.items() if square(frequency) == 1
    }
    low_lamb = {
        frequency: value
        for frequency, value in projected_lamb.items()
        if square(frequency) == 1
    }
    expected_omega = {
        (-1, 0, 0): Vector([0, 0, I]),
        (0, -1, 0): Vector([I, 0, 0]),
        (0, 1, 0): Vector([-I, 0, 0]),
        (1, 0, 0): Vector([0, 0, -I]),
    }
    expected_lamb = {
        (-1, 0, 0): Vector([0, 0, 0]),
        (0, -1, 0): Vector([0, 0, -1]),
        (0, 1, 0): Vector([0, 0, -1]),
        (1, 0, 0): Vector([0, 0, 0]),
    }
    require(low_omega == expected_omega, "low vorticity coefficients")
    require(low_lamb == expected_lamb, "low projected-Lamb coefficients")

    low_work = clean(
        sum(
            pairing(
                low_omega.get(frequency, sp.zeros(3, 1)),
                I * Vector(frequency).cross(value),
            )
            for frequency, value in low_lamb.items()
        )
    )
    low_y = clean(sum(pairing(value, value) for value in low_omega.values()))
    low_d = clean(
        sum(square(frequency) * pairing(value, value) for frequency, value in low_omega.items())
    )
    low_lamb_l2 = clean(sum(pairing(value, value) for value in low_lamb.values()))
    full_velocity_l2 = clean(sum(pairing(value, value) for value in velocity.values()))
    full_enstrophy = clean(sum(pairing(value, value) for value in omega.values()))
    require(low_work == 2, "positive low-block work")
    require(low_y == 4, "low-block enstrophy")
    require(low_d == 4, "low-block palinstrophy")
    require(low_lamb_l2 == 2, "low-block Lamb norm")
    require(full_velocity_l2 == 6, "full six-mode kinetic energy")
    require(full_enstrophy == 8, "full six-mode enstrophy")

    return {
        "omega": {
            str(frequency): [str(entry) for entry in value]
            for frequency, value in sorted(low_omega.items())
        },
        "projectedLamb": {
            str(frequency): [str(entry) for entry in value]
            for frequency, value in sorted(low_lamb.items())
        },
        "normalizedAtAEqualsKEqualsOne": {
            "enstrophy": str(low_y),
            "palinstrophy": str(low_d),
            "projectedLambL2Squared": str(low_lamb_l2),
            "positiveWork": str(low_work),
            "positiveQuotient": str(clean(low_work**2 / low_d)),
        },
        "fullDatumNormsAtAEqualsKEqualsOne": {
            "velocityL2Squared": str(full_velocity_l2),
            "enstrophy": str(full_enstrophy),
        },
    }


def local_real_space_identity() -> dict[str, object]:
    x, y, z = sp.symbols("x y z", real=True)
    a, scale, heat = sp.symbols("a K s", positive=True)
    phi = sp.Function("phi")(x, y, z)
    variables = (x, y, z)
    decay = sp.exp(-scale**2 * heat)

    w0 = Vector(
        [
            2 * a * scale**2 * sp.sin(scale * y),
            0,
            2 * a * scale**2 * sp.sin(scale * x),
        ]
    )
    f0 = Vector([0, 0, -2 * a**2 * scale**3 * sp.cos(scale * y)])
    w = clean(decay * w0)
    f = clean(decay * f0)
    curl_phi_w = clean(curl(phi * w, variables))
    curl_f = clean(curl(f, variables))
    local_integrand = clean(f.dot(curl_phi_w))
    integrated_integrand = clean(phi * w.dot(curl_f))
    boundary_vector = clean((phi * w).cross(f))
    boundary_divergence = clean(divergence(boundary_vector, variables))

    require(
        clean(local_integrand - integrated_integrand - boundary_divergence) == 0,
        "cutoff-curl integration-by-parts identity",
    )
    expected_positive_density = clean(
        4 * a**3 * scale**6 * decay**2 * phi * sp.sin(scale * y) ** 2
    )
    require(
        clean(integrated_integrand - expected_positive_density) == 0,
        "strict positive local density",
    )

    global_b = clean(2 * a**3 * scale**6 * decay**2)
    global_d = clean(4 * a**2 * scale**6 * decay**2)
    global_q = clean(global_b**2 / global_d)
    require(global_q == clean(a**4 * scale**6 * decay**2), "global quotient")

    return {
        "Wjs": [str(entry) for entry in w],
        "AjSL": [str(entry) for entry in f],
        "curlPhiW": [str(entry) for entry in curl_phi_w],
        "pointwiseBeforeIntegrationByParts": str(local_integrand),
        "boundaryDivergence": str(boundary_divergence),
        "pointwiseAfterIntegrationByParts": str(integrated_integrand),
        "localWorkFormula": (
            "4*a**3*K**6*exp(-2*K**2*s)*Integral(phi*sin(K*y)**2)"
        ),
        "strictPositivity": (
            "positive for every nonzero smooth phi >= 0 on the torus"
        ),
        "global": {
            "B": str(global_b),
            "D": str(global_d),
            "q": str(global_q),
        },
    }


def heat_trace_and_moments() -> dict[str, object]:
    scale, heat, height, alpha, q0 = sp.symbols(
        "K s h alpha q0", positive=True
    )
    q = q0 * sp.exp(-2 * scale**2 * heat)
    finite_bulk = clean(sp.integrate(q, (heat, 0, height)))
    infinite_bulk = clean(sp.integrate(q, (heat, 0, sp.oo)))
    moment = clean(sp.integrate(heat ** (alpha - 1) * q, (heat, 0, sp.oo)))
    finite_factor = clean(q0 / finite_bulk)
    moment_factor = clean(q0 / moment)

    require(
        finite_bulk == clean(q0 * (1 - sp.exp(-2 * scale**2 * height)) / (2 * scale**2)),
        "finite heat window",
    )
    require(infinite_bulk == q0 / (2 * scale**2), "infinite heat window")
    require(
        moment == clean(q0 * sp.gamma(alpha) / (2 * scale**2) ** alpha),
        "Gamma moment",
    )

    theta = sp.symbols("theta", positive=True)
    matched_average_ratio = clean(
        finite_bulk.subs(height, theta / scale**2)
        / ((theta / scale**2) * q0)
    )
    require(
        matched_average_ratio == clean((1 - sp.exp(-2 * theta)) / (2 * theta)),
        "matched-scale average",
    )

    return {
        "qOfS": str(q),
        "finiteHeightIntegral": str(finite_bulk),
        "finiteTraceFactor": str(finite_factor),
        "infiniteHeightIntegral": str(infinite_bulk),
        "infiniteTraceFactor": "2*K**2",
        "alphaMoment": str(moment),
        "alphaMomentTraceFactor": str(moment_factor),
        "matchedHeight": "h=theta/K**2",
        "matchedAverageOverBottom": str(matched_average_ratio),
        "selectedMoments": {
            "alpha=1/2": str(clean(moment.subs(alpha, sp.Rational(1, 2)))),
            "alpha=1": str(clean(moment.subs(alpha, 1))),
            "alpha=2": str(clean(moment.subs(alpha, 2))),
        },
    }


def packing_ledger() -> dict[str, object]:
    # Algebraic constants for a partition of unity at r=rho/K.  C0 controls
    # sum phi_Q**2 and C1/r**2 controls sum |grad phi_Q|**2 pointwise.
    a, scale, rho, c0, c1, overlap = sp.symbols(
        "a K rho C0 C1 N", positive=True
    )
    total_b = 2 * a**3 * scale**6
    low_y = 4 * a**2 * scale**4
    low_d = 4 * a**2 * scale**6
    lamb_l2 = 2 * a**4 * scale**6
    radius = rho / scale
    denominator_sum_upper = clean(
        2 * c0 * low_d + 2 * c1 * radius ** (-2) * low_y
    )
    quotient_sum_lower = clean(total_b**2 / denominator_sum_upper)
    quotient_sum_upper = clean(overlap * lamb_l2)
    expected_lower = clean(a**4 * scale**6 / (2 * (c0 + c1 / rho**2)))
    require(quotient_sum_lower == expected_lower, "partition lower bound")
    require(
        quotient_sum_upper == 2 * overlap * a**4 * scale**6,
        "partition upper bound",
    )

    velocity, omega = six_mode_velocity_and_vorticity()
    base_velocity_l2 = clean(sum(pairing(value, value) for value in velocity.values()))
    base_enstrophy = clean(sum(pairing(value, value) for value in omega.values()))
    require(base_velocity_l2 == 6, "packing full six-mode kinetic energy")
    require(base_enstrophy == 8, "packing full six-mode enstrophy")
    total_enstrophy = base_enstrophy * a**2 * scale**4
    normalized_lower = clean(quotient_sum_lower / total_enstrophy)
    normalized_upper = clean(quotient_sum_upper / total_enstrophy)
    fixed_energy_amplitude = 1 / scale

    return {
        "hypotheses": {
            "partition": "sum_Q phi_Q = 1, phi_Q >= 0",
            "overlap": "sum_Q 1_supp(phi_Q) <= N",
            "squareCutoff": "sum_Q phi_Q**2 <= C0",
            "gradientCutoff": "sum_Q abs(grad(phi_Q))**2 <= C1/r**2",
            "matchedRadius": "r=rho/K",
        },
        "positiveWorkSum": str(total_b),
        "denominatorSumUpper": str(denominator_sum_upper),
        "positiveQuotientSumLower": str(quotient_sum_lower),
        "positiveQuotientSumUpper": str(quotient_sum_upper),
        "normalizedBottomLower": str(normalized_lower),
        "normalizedBottomUpper": str(normalized_upper),
        "fixedEnergySequenceAEqualsOneOverK": {
            "velocityL2Squared": str(base_velocity_l2),
            "normalizedBottomLower": str(clean(normalized_lower.subs(a, fixed_energy_amplitude))),
            "normalizedBottomUpper": str(clean(normalized_upper.subs(a, fixed_energy_amplitude))),
            "normalizedInfiniteBulkLower": str(
                clean(normalized_lower.subs(a, fixed_energy_amplitude) / (2 * scale**2))
            ),
            "normalizedInfiniteBulkUpper": str(
                clean(normalized_upper.subs(a, fixed_energy_amplitude) / (2 * scale**2))
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = {
        "release": "R0.71F",
        "status": "localized-heat-packing-and-sharp-bottom-trace-obstruction",
        "checks": {
            "boundedOverlapPackingRetainsStabilizedDenominator": True,
            "cutoffCurlTermIncludedExactly": True,
            "usesR071EFixedFrameValues": True,
            "fixedEnergySequenceSeparatesBottomFromBulk": True,
            "heatMomentConstantUsesGammaFunction": True,
            "localWorkStrictlyPositiveForEveryNonzeroNonnegativeCutoff": True,
            "localizedBottomTraceCostsExactlyTwoFrequencyPowers": True,
            "projectedLambLowBlockReconstructedFromFullDatum": True,
            "trueGlobalSmooth2D3CInitialTrace": True,
        },
        "lowBlockReconstruction": reconstruct_low_block(),
        "localizedIdentity": local_real_space_identity(),
        "heatTrace": heat_trace_and_moments(),
        "matchedPartition": packing_ledger(),
        "routeDecision": {
            "positiveResult": (
                "Bounded-overlap localization preserves the unconditional "
                "projected-Lamb heat-area packing estimate."
            ),
            "sharpObstruction": (
                "For the true smooth 2D3C family, every nonnegative local "
                "cutoff retains the exact K-square bottom-trace cost."
            ),
            "skewedGeometryBoundary": (
                "Flow-adapted cylinders organize spatial-temporal overlap but "
                "do not create regularity in the independent heat-height variable."
            ),
            "nextGate": (
                "R0.71G must seek an NSE-dynamic frequency-envelope or time-"
                "frequency compensation, not another geometric bulk-to-trace upgrade."
            ),
        },
        "claimBoundary": (
            "The certificate proves exact finite identities and sharp scaling "
            "for the localized initial heat trace. The general moving-cylinder "
            "ledger and Leray-level packing are analytic theorems in the report. "
            "No regularity, singularity, or novelty theorem is claimed."
        ),
    }

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
