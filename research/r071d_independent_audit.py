#!/usr/bin/env python3
"""Independent exact checker for the R0.71D localization obstruction.

This checker deliberately imports no project audit module. It reconstructs an
embedded two-dimensional Navier--Stokes Fourier solution, its two-weight
local enstrophy ledger, the parabolic-time equality case, and the bottom
Littlewood--Paley cutoff commutator directly from their definitions.

The deciding identities use exact SymPy arithmetic. A separate midpoint
quadrature uses only the standard math module and floating-point summation as
a small sanity check of the local integral formulas.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import sympy as sp


Frequency2 = tuple[int, int]


def clean(expression: sp.Expr) -> sp.Expr:
    """Return a stable exact form for a scalar expression."""

    return sp.factor(sp.cancel(sp.trigsimp(sp.expand(expression))))


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def as_text(value: sp.Expr | str | int) -> str:
    if isinstance(value, sp.Basic):
        return sp.sstr(clean(value))
    return str(value)


def vector_clean(vector: sp.Matrix) -> sp.Matrix:
    return vector.applyfunc(clean)


def normalized_average(expression: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> sp.Expr:
    integral = sp.integrate(
        sp.integrate(sp.expand_trig(expression), (x, 0, 2 * sp.pi)),
        (y, 0, 2 * sp.pi),
    )
    return clean(integral / (4 * sp.pi**2))


def normalized_phase_average(expression: sp.Expr, x: sp.Symbol) -> sp.Expr:
    integral = sp.integrate(sp.expand_trig(expression), (x, 0, 2 * sp.pi))
    return clean(integral / (2 * sp.pi))


def material_shear_audit() -> dict[str, object]:
    """Rebuild the pointwise-material shear and its exact heat ledger."""

    x = sp.symbols("X", real=True)
    time = sp.symbols("t", nonnegative=True)
    amplitude, viscosity, wave_number, rho, theta = sp.symbols(
        "A nu k rho theta", positive=True
    )
    decay = sp.exp(-viscosity * wave_number**2 * time)
    velocity = sp.Matrix(
        [0, amplitude * decay * sp.sin(x) / wave_number, 0]
    )
    omega = amplitude * decay * sp.cos(x)
    weights = {
        "plus": (1 + rho * sp.cos(2 * x)) / 2,
        "minus": (1 - rho * sp.cos(2 * x)) / 2,
    }
    expected_y = {
        "plus": amplitude**2 * decay**2 * (2 + rho) / 8,
        "minus": amplitude**2 * decay**2 * (2 - rho) / 8,
    }
    expected_d = {
        "plus": amplitude**2 * wave_number**2 * decay**2 * (2 - rho) / 8,
        "minus": amplitude**2 * wave_number**2 * decay**2 * (2 + rho) / 8,
    }
    expected_beta = {
        "plus": (
            -viscosity
            * amplitude**2
            * wave_number**2
            * rho
            * decay**2
            / 4
        ),
        "minus": (
            viscosity
            * amplitude**2
            * wave_number**2
            * rho
            * decay**2
            / 4
        ),
    }

    reconstructed_omega = clean(wave_number * sp.diff(velocity[1], x))
    divergence = clean(wave_number * sp.diff(velocity[0], x))
    velocity_advection = vector_clean(
        velocity[0] * wave_number * velocity.diff(x)
    )
    vorticity_transport = clean(
        velocity[0] * wave_number * sp.diff(omega, x)
    )
    stretching = sp.zeros(3, 1)
    heat_residual = vector_clean(
        velocity.diff(time)
        - viscosity * wave_number**2 * velocity.diff(x, 2)
    )
    need(clean(reconstructed_omega - omega) == 0, "material shear curl")
    need(divergence == 0, "material shear divergence")
    need(velocity_advection == sp.zeros(3, 1), "material shear advection")
    need(vorticity_transport == 0, "material shear vorticity transport")
    need(stretching == sp.zeros(3, 1), "material shear stretching")
    need(heat_residual == sp.zeros(3, 1), "material shear heat residual")

    local_y: dict[str, sp.Expr] = {}
    local_d: dict[str, sp.Expr] = {}
    beta: dict[str, sp.Expr] = {}
    material_derivative: dict[str, sp.Expr] = {}
    gradient_square = (
        amplitude**2
        * wave_number**2
        * decay**2
        * sp.sin(x) ** 2
    )

    for label, weight in weights.items():
        # The weight depends only on x1 while u has only an x2 component.
        material_derivative[label] = clean(
            velocity[0] * wave_number * sp.diff(weight, x)
        )
        need(
            material_derivative[label] == 0,
            f"material shear material derivative {label}",
        )
        cutoff_laplacian = clean(
            wave_number**2 * sp.diff(weight, x, 2)
        )
        local_y[label] = normalized_phase_average(weight * omega**2, x)
        local_d[label] = normalized_phase_average(
            weight * gradient_square, x
        )
        beta[label] = normalized_phase_average(
            viscosity * cutoff_laplacian * omega**2 / 2, x
        )
        need(
            clean(local_y[label] - expected_y[label]) == 0,
            f"material shear Y_{label}",
        )
        need(
            clean(local_d[label] - expected_d[label]) == 0,
            f"material shear D_{label}",
        )
        need(
            clean(beta[label] - expected_beta[label]) == 0,
            f"material shear beta_{label}",
        )
        need(
            clean(
                -viscosity * wave_number**2 * local_y[label]
                + viscosity * local_d[label]
                - beta[label]
            )
            == 0,
            f"material shear local balance {label}",
        )

    parent_beta = clean(beta["plus"] + beta["minus"])
    fine_defect = clean(beta["minus"] ** 2 / local_d["minus"])
    total_y = clean(local_y["plus"] + local_y["minus"])
    normalized_defect = clean(fine_defect / total_y)
    expected_defect = (
        viscosity**2
        * amplitude**2
        * wave_number**2
        * rho**2
        * decay**2
        / (2 * (2 + rho))
    )
    expected_normalized = (
        viscosity**2 * wave_number**2 * rho**2 / (2 + rho)
    )
    need(parent_beta == 0, "material shear parent signed beta")
    need(
        clean(fine_defect - expected_defect) == 0,
        "material shear fine defect",
    )
    need(
        clean(normalized_defect - expected_normalized) == 0,
        "material shear normalized defect",
    )

    tau = theta / (viscosity * wave_number**2)
    integrated_beta = clean(sp.integrate(beta["minus"], (time, 0, tau)))
    integrated_dissipation = clean(
        sp.integrate(local_d["minus"], (time, 0, tau))
    )
    integrated_positive_square = clean(
        sp.integrate(
            beta["minus"] ** 2 / local_d["minus"], (time, 0, tau)
        )
    )
    expected_integrated_beta = (
        amplitude**2 * rho * (1 - sp.exp(-2 * theta)) / 8
    )
    expected_integrated_dissipation = (
        amplitude**2
        * (2 + rho)
        * (1 - sp.exp(-2 * theta))
        / (16 * viscosity)
    )
    expected_box_cost = (
        viscosity
        * amplitude**2
        * rho**2
        * (1 - sp.exp(-2 * theta))
        / (4 * (2 + rho))
    )
    integrated_normalized = clean(expected_normalized * tau)
    need(
        clean(integrated_beta - expected_integrated_beta) == 0,
        "material shear parabolic B",
    )
    need(
        clean(
            integrated_dissipation - expected_integrated_dissipation
        )
        == 0,
        "material shear parabolic Dbar",
    )
    need(
        clean(integrated_positive_square - expected_box_cost) == 0,
        "material shear integrated positive square",
    )
    need(
        clean(
            integrated_beta**2 / integrated_dissipation
            - integrated_positive_square
        )
        == 0,
        "material shear exact Cauchy equality",
    )
    need(
        clean(integrated_normalized - viscosity * theta * rho**2 / (2 + rho))
        == 0,
        "material shear scale-independent normalized cost",
    )

    return {
        "field": {
            "velocity": "(0,A/k*exp(-nu*k^2*t)*sin(k*x1),0)",
            "vorticity": "(0,0,A*exp(-nu*k^2*t)*cos(k*x1))",
            "divergence": as_text(divergence),
            "velocityAdvection": [as_text(entry) for entry in velocity_advection],
            "vorticityTransport": as_text(vorticity_transport),
            "vortexStretching": [as_text(entry) for entry in stretching],
            "heatResidual": [as_text(entry) for entry in heat_residual],
            "pressure": "constant",
            "status": "exact smooth shear NSE solution",
        },
        "weights": {
            "definition": "phi_+/-=(1+/-rho*cos(2*k*x1))/2",
            "materialDerivativePlus": as_text(material_derivative["plus"]),
            "materialDerivativeMinus": as_text(material_derivative["minus"]),
            "pointwiseMaterial": True,
        },
        "localLedger": {
            "YPlus": "A^2*exp(-2*nu*k^2*t)*(2+rho)/8",
            "YMinus": "A^2*exp(-2*nu*k^2*t)*(2-rho)/8",
            "DPlus": "A^2*k^2*exp(-2*nu*k^2*t)*(2-rho)/8",
            "DMinus": "A^2*k^2*exp(-2*nu*k^2*t)*(2+rho)/8",
            "betaPlus": "-nu*A^2*k^2*rho*exp(-2*nu*k^2*t)/4",
            "betaMinus": "nu*A^2*k^2*rho*exp(-2*nu*k^2*t)/4",
            "parentSignedBeta": as_text(parent_beta),
            "finePositiveLedger": (
                "nu^2*A^2*k^2*rho^2*exp(-2*nu*k^2*t)/(2*(2+rho))"
            ),
            "totalY": "A^2*exp(-2*nu*k^2*t)/2",
            "fineLedgerOverTotalY": "nu^2*k^2*rho^2/(2+rho)",
            "balance": "(1/2)Y_+/-' + nu*D_+/- = beta_+/-",
        },
        "parabolicInterval": {
            "intervalLength": "tau=theta/(nu*k^2)",
            "B": "A^2*rho*(1-exp(-2*theta))/8",
            "Dbar": "A^2*(2+rho)*(1-exp(-2*theta))/(16*nu)",
            "B2OverDbar": (
                "nu*A^2*rho^2*(1-exp(-2*theta))/(4*(2+rho))"
            ),
            "integralBeta2OverD": (
                "nu*A^2*rho^2*(1-exp(-2*theta))/(4*(2+rho))"
            ),
            "equalityResidual": "0",
            "integralNormalizedDefect": "nu*theta*rho^2/(2+rho)",
            "dimensionlessCostAfterViscousNormalization": (
                "theta*rho^2/(2+rho)"
            ),
            "scaleIndependentInK": True,
        },
    }


def nse_family_audit() -> dict[str, object]:
    """Rebuild the embedded-2D exact NSE family in phase coordinates."""

    x, y = sp.symbols("X Y", real=True)
    amplitude, viscosity, wave_number = sp.symbols("a nu N", positive=True)

    psi = amplitude * (sp.cos(x) + sp.cos(y))
    velocity = sp.Matrix(
        [
            wave_number * sp.diff(psi, y),
            -wave_number * sp.diff(psi, x),
            0,
        ]
    )
    divergence = clean(
        wave_number * sp.diff(velocity[0], x)
        + wave_number * sp.diff(velocity[1], y)
    )
    vorticity_scalar = clean(
        wave_number * sp.diff(velocity[1], x)
        - wave_number * sp.diff(velocity[0], y)
    )
    vorticity = sp.Matrix([0, 0, vorticity_scalar])

    transport = clean(
        velocity[0] * wave_number * sp.diff(vorticity_scalar, x)
        + velocity[1] * wave_number * sp.diff(vorticity_scalar, y)
    )
    stretching = sp.zeros(3, 1)

    advection = vector_clean(
        velocity[0] * wave_number * velocity.diff(x)
        + velocity[1] * wave_number * velocity.diff(y)
    )
    gradient_potential = vector_clean(
        sp.Matrix(
            [
                wave_number
                * sp.diff(
                    amplitude**2 * wave_number**2 * sp.cos(x) * sp.cos(y), x
                ),
                wave_number
                * sp.diff(
                    amplitude**2 * wave_number**2 * sp.cos(x) * sp.cos(y), y
                ),
                0,
            ]
        )
    )
    laplacian_velocity = vector_clean(
        wave_number**2 * (velocity.diff(x, 2) + velocity.diff(y, 2))
    )
    time_derivative_velocity = vector_clean(
        -viscosity * wave_number**2 * velocity
    )
    heat_residual = vector_clean(
        time_derivative_velocity - viscosity * laplacian_velocity
    )

    need(divergence == 0, "velocity divergence")
    need(transport == 0, "vorticity transport nonlinearity")
    need(stretching == sp.zeros(3, 1), "vortex stretching")
    need(advection == gradient_potential, "velocity advection is a gradient")
    need(heat_residual == sp.zeros(3, 1), "linear heat residual")
    need(
        vorticity
        == sp.Matrix(
            [0, 0, amplitude * wave_number**2 * (sp.cos(x) + sp.cos(y))]
        ),
        "vorticity reconstruction",
    )

    return {
        "streamFunction": "a(t)*(cos(N*x1)+cos(N*x2))",
        "amplitudeLaw": "a'(t)=-nu*N^2*a(t)",
        "velocity": [
            "-a(t)*N*sin(N*x2)",
            "a(t)*N*sin(N*x1)",
            "0",
        ],
        "vorticity": "(0,0,C(t)*(cos(N*x1)+cos(N*x2))), C=a*N^2",
        "divergence": as_text(divergence),
        "vorticityTransport": as_text(transport),
        "vortexStretching": [as_text(entry) for entry in stretching],
        "velocityAdvection": (
            "grad(a(t)^2*N^2*cos(N*x1)*cos(N*x2)); "
            "its Leray projection is zero"
        ),
        "pressure": "-a(t)^2*N^2*cos(N*x1)*cos(N*x2)",
        "heatResidual": [as_text(entry) for entry in heat_residual],
        "conclusion": "an exact smooth 2D solution embedded in the 3D torus",
    }


def local_ledger_audit() -> dict[str, object]:
    """Check the exact two-child local enstrophy ledger."""

    x, y = sp.symbols("X Y", real=True)
    coefficient, viscosity, wave_number, rho = sp.symbols(
        "C nu N rho", positive=True
    )
    omega = coefficient * (sp.cos(x) + sp.cos(y))
    weights = {
        "plus": (1 + rho * sp.cos(x - y)) / 2,
        "minus": (1 - rho * sp.cos(x - y)) / 2,
    }
    expected_y = {
        "plus": coefficient**2 * (sp.Rational(1, 2) + rho / 4),
        "minus": coefficient**2 * (sp.Rational(1, 2) - rho / 4),
    }
    expected_d = coefficient**2 * wave_number**2 / 2
    expected_beta = {
        "plus": -viscosity * rho * coefficient**2 * wave_number**2 / 4,
        "minus": viscosity * rho * coefficient**2 * wave_number**2 / 4,
    }

    local_y: dict[str, sp.Expr] = {}
    local_d: dict[str, sp.Expr] = {}
    beta: dict[str, sp.Expr] = {}
    transport_flux: dict[str, sp.Expr] = {}

    # Here a=C/N^2, so u=(-C/N sin Y, C/N sin X, 0).
    velocity_x = -coefficient * sp.sin(y) / wave_number
    velocity_y = coefficient * sp.sin(x) / wave_number
    gradient_square = coefficient**2 * wave_number**2 * (
        sp.sin(x) ** 2 + sp.sin(y) ** 2
    )

    for label, weight in weights.items():
        local_y[label] = normalized_average(weight * omega**2, x, y)
        local_d[label] = normalized_average(weight * gradient_square, x, y)
        cutoff_transport = clean(
            velocity_x * wave_number * sp.diff(weight, x)
            + velocity_y * wave_number * sp.diff(weight, y)
        )
        cutoff_laplacian = clean(
            wave_number**2 * (sp.diff(weight, x, 2) + sp.diff(weight, y, 2))
        )
        transport_flux[label] = clean(
            normalized_average(cutoff_transport * omega**2 / 2, x, y)
        )
        beta[label] = clean(
            normalized_average(
                (cutoff_transport + viscosity * cutoff_laplacian) * omega**2 / 2,
                x,
                y,
            )
        )
        need(clean(local_y[label] - expected_y[label]) == 0, f"Y_{label}")
        need(clean(local_d[label] - expected_d) == 0, f"D_{label}")
        need(clean(transport_flux[label]) == 0, f"transport flux {label}")
        need(clean(beta[label] - expected_beta[label]) == 0, f"beta_{label}")

        # If C'=-nu*N^2*C, then (1/2)Y'+nu*D=beta.
        energy_derivative_half = -viscosity * wave_number**2 * local_y[label]
        need(
            clean(
                energy_derivative_half
                + viscosity * local_d[label]
                - beta[label]
            )
            == 0,
            f"local balance {label}",
        )

    parent_beta = clean(beta["plus"] + beta["minus"])
    defect = clean(beta["minus"] ** 2 / local_d["minus"])
    total_y = clean(local_y["plus"] + local_y["minus"])
    normalized_defect = clean(defect / total_y)
    need(parent_beta == 0, "parent signed heat flux")
    need(
        clean(
            defect
            - viscosity**2
            * rho**2
            * coefficient**2
            * wave_number**2
            / 8
        )
        == 0,
        "positive child refinement defect",
    )
    need(
        clean(
            normalized_defect - viscosity**2 * rho**2 * wave_number**2 / 8
        )
        == 0,
        "normalized defect",
    )

    return {
        "normalizedSpatialMeasure": "(2*pi)^(-2) dX dY, X=N*x1, Y=N*x2",
        "weights": "phi_+/-=(1+/-rho*cos(N*(x1-x2)))/2, 0<rho<1",
        "weightBoundary": (
            "the weights are static rather than pointwise material; "
            "their integrated cutoff-transport term vanishes exactly"
        ),
        "YPlus": as_text(local_y["plus"]),
        "YMinus": as_text(local_y["minus"]),
        "DPlus": as_text(local_d["plus"]),
        "DMinus": as_text(local_d["minus"]),
        "transportFluxPlus": as_text(transport_flux["plus"]),
        "transportFluxMinus": as_text(transport_flux["minus"]),
        "betaPlus": as_text(beta["plus"]),
        "betaMinus": as_text(beta["minus"]),
        "parentSignedBeta": as_text(parent_beta),
        "finePositiveLedger": as_text(defect),
        "totalY": as_text(total_y),
        "fineLedgerOverTotalY": as_text(normalized_defect),
        "balance": "(1/2)Y_+/-' + nu*D_+/- = beta_+/-",
    }


def parabolic_interval_audit() -> dict[str, object]:
    """Verify the exact equality case on a parabolic time interval."""

    time = sp.symbols("t", nonnegative=True)
    mass, viscosity, wave_number, rho, theta = sp.symbols(
        "m nu N rho theta", positive=True
    )
    tau = theta / (viscosity * wave_number**2)
    coefficient = mass * wave_number**2 * sp.exp(
        -viscosity * wave_number**2 * time
    )
    dissipation = coefficient**2 * wave_number**2 / 2
    positive_flux = viscosity * rho * coefficient**2 * wave_number**2 / 4

    integrated_dissipation = clean(
        sp.integrate(dissipation, (time, 0, tau))
    )
    signed_mass = clean(sp.integrate(positive_flux, (time, 0, tau)))
    positive_square = clean(
        sp.integrate(positive_flux**2 / dissipation, (time, 0, tau))
    )
    expected_dissipation = (
        mass**2
        * wave_number**4
        * (1 - sp.exp(-2 * theta))
        / (4 * viscosity)
    )
    expected_mass = (
        rho
        * mass**2
        * wave_number**4
        * (1 - sp.exp(-2 * theta))
        / 8
    )
    expected_square = (
        viscosity
        * rho**2
        * mass**2
        * wave_number**4
        * (1 - sp.exp(-2 * theta))
        / 16
    )

    need(
        clean(integrated_dissipation - expected_dissipation) == 0,
        "parabolic integrated dissipation",
    )
    need(clean(signed_mass - expected_mass) == 0, "parabolic signed mass")
    need(
        clean(positive_square - expected_square) == 0,
        "positive square integral",
    )
    need(
        clean(signed_mass**2 / integrated_dissipation - positive_square) == 0,
        "parabolic Cauchy equality",
    )

    return {
        "amplitude": "C(t)=m*N^2*exp(-nu*N^2*t)",
        "intervalLength": "tau=theta/(nu*N^2)",
        "Dbar": "m^2*N^4*(1-exp(-2*theta))/(4*nu)",
        "B": "rho*m^2*N^4*(1-exp(-2*theta))/8",
        "B2OverDbar": "nu*rho^2*m^2*N^4*(1-exp(-2*theta))/16",
        "integralBeta2OverD": (
            "nu*rho^2*m^2*N^4*(1-exp(-2*theta))/16"
        ),
        "equalityResidual": "0",
        "consequence": (
            "the signed-box Cauchy lower bound is saturated on the positive child"
        ),
    }


def add_frequency(first: Frequency2, second: Frequency2) -> Frequency2:
    return first[0] + second[0], first[1] + second[1]


def multiply_modes(
    first: dict[Frequency2, sp.Expr],
    second: dict[Frequency2, sp.Expr],
) -> dict[Frequency2, sp.Expr]:
    result: dict[Frequency2, sp.Expr] = {}
    for first_frequency, first_coefficient in first.items():
        for second_frequency, second_coefficient in second.items():
            output = add_frequency(first_frequency, second_frequency)
            result[output] = result.get(output, sp.Integer(0)) + (
                first_coefficient * second_coefficient
            )
    return {
        frequency: clean(coefficient)
        for frequency, coefficient in result.items()
        if clean(coefficient) != 0
    }


def lp_commutator_audit() -> dict[str, object]:
    """Reconstruct [T_j,phi_+] omega from signed Fourier coefficients."""

    rho, multiplier = sp.symbols("rho m", positive=True)
    omega_modes: dict[Frequency2, sp.Expr] = {
        (1, 0): sp.Rational(1, 2),
        (-1, 0): sp.Rational(1, 2),
        (0, 1): sp.Rational(1, 2),
        (0, -1): sp.Rational(1, 2),
    }
    phi_modes: dict[Frequency2, sp.Expr] = {
        (0, 0): sp.Rational(1, 2),
        (1, -1): rho / 4,
        (-1, 1): rho / 4,
    }

    def symbol(frequency: Frequency2) -> sp.Expr:
        radius_square = frequency[0] ** 2 + frequency[1] ** 2
        if radius_square == 1:
            return multiplier
        if radius_square == 5:
            return sp.Integer(0)
        raise AssertionError(f"unexpected LP radius square {radius_square}")

    product_modes = multiply_modes(phi_modes, omega_modes)
    filtered_product = {
        frequency: clean(symbol(frequency) * coefficient)
        for frequency, coefficient in product_modes.items()
    }
    filtered_omega = {
        frequency: clean(multiplier * coefficient)
        for frequency, coefficient in omega_modes.items()
    }
    phi_filtered_omega = multiply_modes(phi_modes, filtered_omega)
    support = set(filtered_product) | set(phi_filtered_omega)
    commutator = {
        frequency: clean(
            filtered_product.get(frequency, sp.Integer(0))
            - phi_filtered_omega.get(frequency, sp.Integer(0))
        )
        for frequency in support
    }
    commutator = {
        frequency: coefficient
        for frequency, coefficient in commutator.items()
        if coefficient != 0
    }

    high_frequencies = {(2, -1), (-2, 1), (1, -2), (-1, 2)}
    need(set(commutator) == high_frequencies, "commutator support")
    for frequency in high_frequencies:
        need(
            clean(commutator[frequency] + rho * multiplier / 8) == 0,
            f"commutator coefficient {frequency}",
        )
    cosine_coefficient = clean(2 * commutator[(2, -1)])
    need(
        clean(cosine_coefficient + rho * multiplier / 4) == 0,
        "cosine commutator coefficient",
    )

    return {
        "convention": "[T_j,phi]f=T_j(phi*f)-phi*T_j(f)",
        "symbolValues": "m_j(N)=m, m_j(sqrt(5)*N)=0",
        "input": "cos(N*x1)+cos(N*x2)",
        "weight": "phi_+=(1+rho*cos(N*(x1-x2)))/2",
        "nonzeroCosineModes": ["(2,-1)", "(1,-2)"],
        "cosineCoefficientRelativeToInputAmplitude": as_text(
            cosine_coefficient
        ),
        "identity": (
            "[T_j,phi_+]omega=-(rho*m*C/4)*"
            "(cos(N*(2*x1-x2))+cos(N*(x1-2*x2)))"
        ),
    }


def stable_float(value: float) -> float:
    return float(f"{value:.15g}")


def numeric_quadrature_audit() -> dict[str, object]:
    """Check the local formulas by an independent midpoint quadrature."""

    grid = 48
    coefficient = 1.3
    viscosity = 0.7
    wave_number = 3.0
    rho = 0.6
    totals = {
        "YPlus": 0.0,
        "YMinus": 0.0,
        "DPlus": 0.0,
        "DMinus": 0.0,
        "transportPlus": 0.0,
        "transportMinus": 0.0,
        "betaPlus": 0.0,
        "betaMinus": 0.0,
    }
    for first_index in range(grid):
        x = 2 * math.pi * (first_index + 0.5) / grid
        for second_index in range(grid):
            y = 2 * math.pi * (second_index + 0.5) / grid
            omega = coefficient * (math.cos(x) + math.cos(y))
            gradient_square = coefficient**2 * wave_number**2 * (
                math.sin(x) ** 2 + math.sin(y) ** 2
            )
            velocity_x = -coefficient * math.sin(y) / wave_number
            velocity_y = coefficient * math.sin(x) / wave_number
            for label, sign in (("Plus", 1.0), ("Minus", -1.0)):
                weight = (1 + sign * rho * math.cos(x - y)) / 2
                weight_x = (
                    -sign * rho * wave_number * math.sin(x - y) / 2
                )
                weight_y = (
                    sign * rho * wave_number * math.sin(x - y) / 2
                )
                cutoff_transport = (
                    velocity_x * weight_x + velocity_y * weight_y
                )
                cutoff_laplacian = (
                    -sign * rho * wave_number**2 * math.cos(x - y)
                )
                totals[f"Y{label}"] += weight * omega**2
                totals[f"D{label}"] += weight * gradient_square
                totals[f"transport{label}"] += (
                    cutoff_transport * omega**2 / 2
                )
                totals[f"beta{label}"] += (
                    cutoff_transport + viscosity * cutoff_laplacian
                ) * omega**2 / 2

    point_count = grid * grid
    averages = {key: value / point_count for key, value in totals.items()}
    expected = {
        "YPlus": coefficient**2 * (0.5 + rho / 4),
        "YMinus": coefficient**2 * (0.5 - rho / 4),
        "DPlus": coefficient**2 * wave_number**2 / 2,
        "DMinus": coefficient**2 * wave_number**2 / 2,
        "transportPlus": 0.0,
        "transportMinus": 0.0,
        "betaPlus": (
            -viscosity * rho * coefficient**2 * wave_number**2 / 4
        ),
        "betaMinus": (
            viscosity * rho * coefficient**2 * wave_number**2 / 4
        ),
    }
    errors = {key: abs(averages[key] - expected[key]) for key in expected}
    maximum_error = max(errors.values())
    need(maximum_error < 2.0e-13, "independent midpoint quadrature")

    return {
        "method": (
            "48x48 phase-space midpoint rule using only standard math scalars"
        ),
        "parameters": {
            "C": coefficient,
            "N": wave_number,
            "nu": viscosity,
            "rho": rho,
        },
        "averages": {
            key: stable_float(value) for key, value in sorted(averages.items())
        },
        "expected": {
            key: stable_float(value) for key, value in sorted(expected.items())
        },
        "maxAbsError": stable_float(maximum_error),
        "status": "pass",
    }


def build_certificate() -> dict[str, object]:
    return {
        "version": "R0.71D-independent",
        "arithmetic": (
            "exact SymPy identities plus an independent 48x48 midpoint quadrature"
        ),
        "materialShear": material_shear_audit(),
        "embedded2DStressCheck": {
            "field": nse_family_audit(),
            "localLedger": local_ledger_audit(),
            "parabolicInterval": parabolic_interval_audit(),
            "numericQuadrature": numeric_quadrature_audit(),
        },
        "lpCutoffCommutator": lp_commutator_audit(),
        "claimBoundary": {
            "proved": [
                (
                    "the stated shear is an exact smooth NSE solution and the "
                    "two cutoff weights are pointwise material"
                ),
                (
                    "its parent signed heat flux is zero while the positive "
                    "child ledger is strictly positive and scale-critical"
                ),
                (
                    "the material-shear parabolic box saturates the signed-time "
                    "Cauchy lower bound with k-independent normalized cost"
                ),
                (
                    "the stated cellular Fourier field is an exact smooth 2D "
                    "Navier--Stokes solution embedded in three dimensions"
                ),
                (
                    "the two static weights have zero parent signed flux but a "
                    "strictly positive child signed-before-square heat ledger"
                ),
                (
                    "the child heat-flux box saturates the signed-time Cauchy "
                    "lower bound on a parabolic interval"
                ),
                (
                    "under the stated multiplier values the bottom cutoff "
                    "commutator has cosine coefficient -rho*m/4"
                ),
            ],
            "notProved": [
                "unconditional regularity for three-dimensional Navier--Stokes",
                (
                    "divergence of the flux ledger for every material or "
                    "parabolic tent family"
                ),
                "failure of every compact, adjoint, or flow-adapted localization",
                (
                    "absence of an NSE-specific nonlinear sign or depletion "
                    "cancellation"
                ),
            ],
            "scope": (
                "a pointwise-material scale-critical heat-flux obstruction, an "
                "embedded-2D stress check, and the stated LP-cutoff obstruction; "
                "not a general no-go theorem"
            ),
        },
        "status": "pass",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    certificate = build_certificate()
    serialized = json.dumps(
        certificate, indent=2, sort_keys=True, ensure_ascii=False
    )
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
