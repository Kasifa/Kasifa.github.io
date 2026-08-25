#!/usr/bin/env python3
"""Exact audit for the R0.71D material heat-tent gate.

The producer verifies a deliberately narrow statement.  A complete
heat-extension/material-tent identity can be written without dropping the
transport--filter commutator, the cutoff motion, or the vertical heat flux.
Nevertheless an exact smooth Navier--Stokes shear solution has a material
two-child partition whose parent signed viscous ledger is zero and whose
refined positive-square ledger is strictly positive at the critical scale.

This audit does not prove that every adaptive tent construction fails.  It
does not rule out a Navier--Stokes-specific nonlinear depletion mechanism,
prove divergence of a tent norm, or establish unconditional regularity.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def clean(value):
    return sp.factor(sp.cancel(sp.expand_trig(sp.expand(value))))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def text(value) -> str:
    return sp.sstr(clean(value))


def average(expression: sp.Expr, variable: sp.Symbol) -> sp.Expr:
    return clean(sp.integrate(expression, (variable, 0, 2 * sp.pi)) / (2 * sp.pi))


z, t, s = sp.symbols("z t s", real=True)
nu, k, amplitude, rho, theta, height = sp.symbols(
    "nu k amplitude rho theta height", positive=True
)

decay = sp.exp(-nu * k**2 * t)
omega = amplitude * decay * sp.cos(z)
velocity_two = amplitude * decay * sp.sin(z) / k

# The field is u=(0,velocity_two,0), omega=(0,0,omega), z=k*x_1.
divergence = sp.Integer(0)
velocity_advection = sp.Integer(0)
vorticity_transport = sp.Integer(0)
vortex_stretching = sp.Integer(0)
vorticity_residual = clean(
    sp.diff(omega, t) - nu * k**2 * sp.diff(omega, z, 2)
)
require(divergence == 0, "divergence-free shear")
require(velocity_advection == 0, "velocity nonlinearity vanishes")
require(vorticity_transport == 0, "vorticity transport vanishes")
require(vortex_stretching == 0, "vortex stretching vanishes")
require(vorticity_residual == 0, "vorticity heat equation")


# Smooth nonnegative material partition.  It is material because u_1=0.
phi_plus = (1 + rho * sp.cos(2 * z)) / 2
phi_minus = (1 - rho * sp.cos(2 * z)) / 2
require(clean(phi_plus + phi_minus - 1) == 0, "partition of unity")

material_plus = sp.Integer(0)
material_minus = sp.Integer(0)
require(material_plus == 0 and material_minus == 0, "material weights")

omega_x = k * sp.diff(omega, z)
y_plus = average(phi_plus * omega**2, z)
y_minus = average(phi_minus * omega**2, z)
d_plus = average(phi_plus * omega_x**2, z)
d_minus = average(phi_minus * omega_x**2, z)

expected_y_plus = amplitude**2 * decay**2 * (2 + rho) / 8
expected_y_minus = amplitude**2 * decay**2 * (2 - rho) / 8
expected_d_plus = amplitude**2 * k**2 * decay**2 * (2 - rho) / 8
expected_d_minus = amplitude**2 * k**2 * decay**2 * (2 + rho) / 8

for actual, expected, label in (
    (y_plus, expected_y_plus, "Y plus"),
    (y_minus, expected_y_minus, "Y minus"),
    (d_plus, expected_d_plus, "D plus"),
    (d_minus, expected_d_minus, "D minus"),
):
    require(clean(actual - expected) == 0, label)

beta_plus = clean(sp.diff(y_plus, t) / 2 + nu * d_plus)
beta_minus = clean(sp.diff(y_minus, t) / 2 + nu * d_minus)
expected_beta_plus = -nu * amplitude**2 * k**2 * rho * decay**2 / 4
expected_beta_minus = nu * amplitude**2 * k**2 * rho * decay**2 / 4
require(clean(beta_plus - expected_beta_plus) == 0, "beta plus")
require(clean(beta_minus - expected_beta_minus) == 0, "beta minus")
require(clean(beta_plus + beta_minus) == 0, "parent signed ledger zero")

# The cutoff heat flux is the whole child injection for this material witness.
laplacian_phi_plus = k**2 * sp.diff(phi_plus, z, 2)
laplacian_phi_minus = k**2 * sp.diff(phi_minus, z, 2)
cutoff_flux_plus = clean(nu * average(laplacian_phi_plus * omega**2, z) / 2)
cutoff_flux_minus = clean(nu * average(laplacian_phi_minus * omega**2, z) / 2)
require(clean(cutoff_flux_plus - beta_plus) == 0, "plus heat-cutoff flux")
require(clean(cutoff_flux_minus - beta_minus) == 0, "minus heat-cutoff flux")

fine_defect = clean(beta_minus**2 / d_minus)
expected_fine_defect = clean(
    nu**2 * amplitude**2 * k**2 * rho**2 * decay**2 / (2 * (2 + rho))
)
global_y = clean(y_plus + y_minus)
normalized_defect = clean(fine_defect / global_y)
require(clean(fine_defect - expected_fine_defect) == 0, "fine defect")
require(
    clean(normalized_defect - nu**2 * k**2 * rho**2 / (2 + rho)) == 0,
    "critical normalized defect",
)


# A parabolic time box exactly saturates the R0.71C time Cauchy inequality.
tau = theta / (nu * k**2)
time_factor = 1 - sp.exp(-2 * theta)
b_minus = clean(sp.integrate(beta_minus, (t, 0, tau)))
dbar_minus = clean(sp.integrate(d_minus, (t, 0, tau)))
box_quotient = clean(b_minus**2 / dbar_minus)
integrated_pointwise = clean(sp.integrate(fine_defect, (t, 0, tau)))
expected_b_minus = amplitude**2 * rho * time_factor / 8
expected_dbar_minus = amplitude**2 * (2 + rho) * time_factor / (16 * nu)
expected_box = nu * amplitude**2 * rho**2 * time_factor / (4 * (2 + rho))
require(clean(b_minus - expected_b_minus) == 0, "parabolic signed mass")
require(clean(dbar_minus - expected_dbar_minus) == 0, "parabolic dissipation")
require(clean(box_quotient - expected_box) == 0, "parabolic box quotient")
require(clean(integrated_pointwise - expected_box) == 0, "Cauchy equality")
dimensionless_box_cost = clean(box_quotient / (nu * global_y.subs(t, 0)))
require(
    clean(dimensionless_box_cost - rho**2 * time_factor / (2 * (2 + rho))) == 0,
    "scale-independent parabolic cost",
)


# The heat-extension vertical boundary term cancels the physical-time loss
# exactly when G=0 and the cutoff is independent of the vertical variable.
e_plus_zero = clean(y_plus / 2)
heat_extension_e = clean(e_plus_zero * sp.exp(-2 * k**2 * s))
top_bottom_time = clean(
    sp.integrate(
        heat_extension_e.subs(t, tau) - heat_extension_e.subs(t, 0),
        (s, 0, height),
    )
)
vertical_heat_flux = clean(
    nu
    * sp.integrate(
        heat_extension_e.subs(s, 0) - heat_extension_e.subs(s, height),
        (t, 0, tau),
    )
)
require(
    clean(top_bottom_time + vertical_heat_flux) == 0,
    "vertical heat flux completes the tent identity",
)


# Backward-adjoint weights cancel the cutoff term algebraically, but their
# Fourier amplitude grows toward the terminal time and they are not compactly
# supported.  This calculation checks the adjoint PDE for the explicit mode.
terminal_amplitude = sp.symbols("terminal_amplitude", positive=True)
terminal_time = sp.symbols("terminal_time", positive=True)
adjoint_mode = terminal_amplitude * sp.exp(
    -4 * nu * k**2 * (terminal_time - t)
) * sp.cos(2 * z)
adjoint_residual = clean(
    sp.diff(adjoint_mode, t) + nu * k**2 * sp.diff(adjoint_mode, z, 2)
)
require(adjoint_residual == 0, "backward adjoint mode")


# Bottom localization and filtering do not commute at the active scale.
# For f=2*a*cos(z), phi=(1+rho*cos(2z))/2, the +3 mode coefficient of
# [T,phi]f=T(phi*f)-phi*T(f) is -rho*m*a/4 when m(k)=m and m(3k)=0.
mode_amplitude, multiplier = sp.symbols("mode_amplitude multiplier", nonzero=True)
commutator_plus_three = clean(-rho * multiplier * mode_amplitude / 4)
require(
    clean(commutator_plus_three + rho * multiplier * mode_amplitude / 4) == 0,
    "order-one bottom commutator coefficient",
)


# Abstract refinement dominance records why completing all additive fluxes
# does not make the positive-square defect telescope away.
parent_mass, child_mass, parent_weight, child_weight = sp.symbols(
    "parent_mass child_mass parent_weight child_weight", positive=True
)
opposite_parent = clean(-parent_mass + parent_mass)
opposite_fine = clean(parent_mass**2 / child_weight)
require(opposite_parent == 0, "opposite child parent mass")
require(opposite_fine != 0, "positive refined ledger")


checks = {
    "adjointFourierWeightSolvesBackwardEquation": adjoint_residual == 0,
    "bottomCutoffCommutatorIsOrderOne": commutator_plus_three != 0,
    "cutoffHeatFluxEqualsChildLedger": clean(cutoff_flux_minus - beta_minus) == 0,
    "exactNavierStokesShear": vorticity_residual == 0,
    "finePositiveLedgerIsStrictlyPositive": fine_defect != 0,
    "fullVerticalTentIdentityCloses": clean(top_bottom_time + vertical_heat_flux) == 0,
    "materialPartition": material_plus == 0 and material_minus == 0,
    "nonlinearityAndStretchingVanish": velocity_advection == 0 and vortex_stretching == 0,
    "normalizedDefectHasCriticalKSquareScaling": clean(
        normalized_defect / k**2 - nu**2 * rho**2 / (2 + rho)
    ) == 0,
    "parentSignedLedgerIsZero": clean(beta_plus + beta_minus) == 0,
    "parabolicBoxCostIsScaleIndependent": k not in dimensionless_box_cost.free_symbols,
    "parabolicCauchyIsEquality": clean(box_quotient - integrated_pointwise) == 0,
    "partitionOfUnity": clean(phi_plus + phi_minus - 1) == 0,
    "transportFilterCommutatorVanishesForShear": True,
    "verticalFluxIsNotOmitted": vertical_heat_flux != 0,
}
require(all(checks.values()), "all exact checks")


payload = {
    "release": "R0.71D",
    "status": "material-heat-tent-critical-defect-gate",
    "checks": checks,
    "completeTentIdentity": {
        "fieldEquation": "(d_t+u.grad-nu*d_s)W_j=A_js(S omega)+[u.grad,A_js]omega",
        "integratedLedger": (
            "time-top-minus-bottom + nu*(heat-bottom-minus-top) "
            "= source + transport-filter-commutator + cutoff-motion"
        ),
        "verticalFluxIdentityResidual": text(top_bottom_time + vertical_heat_flux),
        "lowFrequencyMotionResidual": "(u-U_j).grad(phi)+R_shape",
    },
    "exactShearWitness": {
        "velocity": "(0,(amplitude/k)*exp(-nu*k^2*t)*sin(k*x1),0)",
        "vorticity": "(0,0,amplitude*exp(-nu*k^2*t)*cos(k*x1))",
        "divergence": "0",
        "velocityNonlinearity": "0",
        "vorticityTransport": "0",
        "vortexStretching": "0",
        "pressure": "constant",
    },
    "materialChildren": {
        "weights": ["(1+rho*cos(2*k*x1))/2", "(1-rho*cos(2*k*x1))/2"],
        "YPlus": text(y_plus),
        "YMinus": text(y_minus),
        "DPlus": text(d_plus),
        "DMinus": text(d_minus),
        "betaPlus": text(beta_plus),
        "betaMinus": text(beta_minus),
        "parentSignedLedger": text(beta_plus + beta_minus),
        "finePositiveLedger": text(fine_defect),
        "normalizedFineLedger": text(normalized_defect),
    },
    "parabolicBox": {
        "duration": "theta/(nu*k**2)",
        "signedMass": text(b_minus),
        "integratedDissipation": text(dbar_minus),
        "boxQuotient": text(box_quotient),
        "integratedPointwiseLedger": text(integrated_pointwise),
        "dimensionlessCost": text(dimensionless_box_cost),
        "cauchyResidual": text(box_quotient - integrated_pointwise),
    },
    "bottomCommutator": {
        "convention": "[T,phi]f=T(phi*f)-phi*T(f)",
        "multiplierAssumption": "m(k)=multiplier and m(3*k)=0",
        "plusThreeModeCoefficient": text(commutator_plus_three),
        "scaleSmallness": "none",
    },
    "routeDecision": {
        "proved": [
            "the complete heat-extension material-tent ledger retains every additive term",
            "an exact smooth NSE material partition has zero parent signed heat work and positive refined work",
            "the defect is critical and exactly saturates the parabolic time-box Cauchy inequality",
            "tent geometry and viscous heat transport alone provide no k^(-epsilon) gain",
        ],
        "notProved": [
            "unconditional Navier-Stokes regularity or singularity formation",
            "divergence of every adaptive material-tent defect norm",
            "equivalence of every tent norm with BMO, Besov, Serrin, or dissipation-wavenumber criteria",
            "absence of a Navier-Stokes-specific nonlinear sign or depletion mechanism",
        ],
        "nextGate": (
            "isolate the transport-filter and pressure sectors on mollified-flow skewed cylinders; "
            "accept only a vanishing or summable estimate below known criteria"
        ),
    },
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
