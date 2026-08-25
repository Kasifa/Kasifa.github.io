#!/usr/bin/env python3
"""Exact symbolic producer for the R0.71J full-frame gate.

The audit has three layers.  First, it checks the all-shell positive-defect
identity obtained from the R0.71I scalar evolution.  Second, it reconstructs
an exact zero-entry 2D3C datum inside the broad flat-top dyadic parent frame
declared in R0.71E.  Third, it verifies the closed-form pure-heat limit and
the resulting K**2 separation between full-frame positive creation and the
full-frame physical-time heat endpoint.  No DNS or finite-K PDE time stepping
is used.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
R071G = ROOT / "research" / "r071g_exact_audit.py"


def load_fourier_algebra():
    spec = importlib.util.spec_from_file_location("r071g_exact", R071G)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load R0.71G exact Fourier algebra")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scalar(value: sp.Expr) -> str:
    return str(sp.simplify(value))


def main(output: Path | None = None) -> None:
    m = load_fourier_algebra()
    nu, k = sp.symbols("nu K", positive=True)

    # All-shell positive-defect identity.  The declarations jp,jm >= 0
    # represent J^+ and J^- on the branch z > 0.
    a, z, jp, jm, theta_epsilon = sp.symbols(
        "a z Jplus Jminus theta_epsilon", nonnegative=True
    )
    shell_scale = sp.symbols("kappa", positive=True)
    weight = shell_scale**-2
    a_t = 2 * z * (jp - jm) - 2 * nu * shell_scale**2 * a
    hard_defect = sp.simplify(
        2 * weight * z * jp
        - (weight * a_t + 2 * nu * a + 2 * weight * z * jm)
    )
    assert hard_defect == 0

    soft_a_t = (
        2 * z * (jp - jm)
        - 2 * nu * shell_scale**2 * (1 + theta_epsilon) * a
    )
    soft_defect = sp.simplify(
        2 * weight * z * jp
        - (
            weight * soft_a_t
            + 2 * nu * (1 + theta_epsilon) * a
            + 2 * weight * z * jm
        )
    )
    assert soft_defect == 0

    # The R0.71E parent at scale kappa=4K is identically one on the
    # log-radius interval [0,1/2].  All initial vertical modes and all initial
    # Lamb-output modes below have squared normalized radii in [16,32] at K=1.
    imaginary = sp.I
    e2 = sp.Matrix([0, 1, 0])
    e3 = sp.Matrix([0, 0, 1])
    n1, n2 = 4, 5
    velocity = {
        (1, 0, 0): e2,
        (-1, 0, 0): e2,
        (0, n1, 0): imaginary * e3 / n1,
        (0, -n1, 0): -imaginary * e3 / n1,
        (0, n2, 0): -imaginary * e3 / n2,
        (0, -n2, 0): imaginary * e3 / n2,
    }
    for channel in (n1, n2):
        for horizontal_sign in (-1, 1):
            velocity[(horizontal_sign, channel, 0)] = e3
            velocity[(-horizontal_sign, -channel, 0)] = e3

    def in_flat_parent(frequency: tuple[int, int, int]) -> bool:
        radius_squared = sum(entry * entry for entry in frequency)
        return 16 <= radius_squared <= 32

    omega = m.curl(velocity)
    lamb = m.project(m.cross_product(velocity, omega))
    selected_f = {
        frequency: value
        for frequency, value in lamb.items()
        if in_flat_parent(frequency)
    }
    selected_c = m.curl(
        {
            frequency: value
            for frequency, value in omega.items()
            if in_flat_parent(frequency)
        }
    )
    assert selected_f == lamb
    assert {
        abs(frequency[1]) for frequency in selected_f
    } == {n1, n2}
    initial = {
        "kineticEnergy": m.l2_norm_squared(velocity),
        "YOverK2": m.l2_norm_squared(omega),
        "FParentNormSquaredOverK2": m.l2_norm_squared(selected_f),
        "dParentOverK4": m.l2_norm_squared(selected_c),
        "BParentOverK3": m.l2_pair(selected_f, selected_c),
    }
    expected_initial = {
        "kineticEnergy": sp.Rational(2041, 200),
        "YOverK2": sp.Integer(178),
        "FParentNormSquaredOverK2": sp.Integer(500),
        "dParentOverK4": sp.Integer(3942),
        "BParentOverK3": sp.Integer(0),
    }
    assert initial == expected_initial

    selected_f_radii = sorted(
        {sum(entry * entry for entry in frequency) for frequency in selected_f}
    )
    selected_c_radii = sorted(
        {sum(entry * entry for entry in frequency) for frequency in selected_c}
    )
    assert selected_f_radii == [16, 17, 20, 25, 26, 29]
    assert selected_c_radii == [16, 17, 25, 26]

    # Pure-heat limit on theta=nu*K**2*t.  The true 2D3C sideband system
    # differs by a bounded shift of size 1/(nu*K), so these profiles are the
    # rigorous fixed-window limit proved in the report.
    theta = sp.symbols("theta", nonnegative=True)
    b0 = 4 * (sp.exp(-34 * theta) - sp.exp(-52 * theta))
    d0 = (
        32 * sp.exp(-32 * theta)
        + 50 * sp.exp(-50 * theta)
        + 1156 * sp.exp(-34 * theta)
        + 2704 * sp.exp(-52 * theta)
    )
    y0 = (
        2 * sp.exp(-2 * theta)
        + 2 * sp.exp(-32 * theta)
        + 2 * sp.exp(-50 * theta)
        + 68 * sp.exp(-34 * theta)
        + 104 * sp.exp(-52 * theta)
    )
    f0_squared = (
        4 * sp.exp(-34 * theta)
        + 192 * sp.exp(-36 * theta)
        + 4 * sp.exp(-52 * theta)
        + 300 * sp.exp(-54 * theta)
    )
    q0 = sp.simplify(b0**2 / d0)
    amplitude0 = sp.simplify(q0 / y0)
    theta_star = sp.log(2) / 18
    b_star = sp.simplify(b0.subs(theta, theta_star))
    d_star = sp.simplify(d0.subs(theta, theta_star))
    y_star = sp.simplify(y0.subs(theta, theta_star))
    f_star = sp.simplify(f0_squared.subs(theta, theta_star))
    q_star = sp.simplify(q0.subs(theta, theta_star))
    amplitude_star = sp.simplify(amplitude0.subs(theta, theta_star))
    expected_amplitude_star = sp.Rational(4) / (
        57
        * (2 ** sp.Rational(1, 9) + 44)
        * (
            3 * 2 ** sp.Rational(1, 9)
            + 4 * 2 ** sp.Rational(7, 9)
            + 120
        )
    )
    assert b0.subs(theta, 0) == 0
    assert amplitude0.subs(theta, 0) == 0
    assert sp.simplify(amplitude_star - expected_amplitude_star) == 0
    assert amplitude_star > 0

    # The selected parent has kappa=4K.  For sufficiently large dyadic K,
    # fixed-window convergence gives a(theta*) >= amplitude_star/2, hence
    # Z_full >= amplitude_star/(64*K**2).  The support of every R0.71E parent
    # lies in 2^j*[2^(-1/2),2], so the weighted tight-frame multiplier is at
    # most 4*|xi|^-2.  All Lamb modes retain |xi_2| >= 4K and
    # ||L||_2^2/Y <= ||V||_infty^2 <= 4, yielding
    # H_full <= (1-exp(-2*theta_star))/(2*nu*K**4).
    creation_lower = amplitude_star / (64 * k**2)
    heat_upper = (1 - sp.exp(-2 * theta_star)) / (2 * nu * k**4)
    separation_lower = sp.simplify(creation_lower / heat_upper)
    assert separation_lower == sp.simplify(
        nu
        * amplitude_star
        * k**2
        / (32 * (1 - sp.exp(-2 * theta_star)))
    )

    payload = {
        "status": "all-shell-positive-defect-closed-full-frame-heat-payment-rejected",
        "positiveDefectIdentity": {
            "hardResidual": scalar(hard_defect),
            "softResidual": scalar(soft_defect),
            "hardFormula": (
                "2*sum(kappa^-2*z^+*J^+) = d_t sum(kappa^-2*a) "
                "+ 2*nu*sum(a) + 2*sum(kappa^-2*z^+*J^-)"
            ),
            "softExtra": "2*nu*sum(theta_epsilon*a)",
            "boundary": "fixed finite frame/cell family between refreshes; hard zero faces remain separate",
        },
        "broadParentWitness": {
            "frame": "R0.71E smooth log-radius flat-top dyadic parent frame",
            "parentScale": "kappa=4*K",
            "channels": [n1, n2],
            "flatParentFRadiusSquared": selected_f_radii,
            "flatParentCRadiusSquared": selected_c_radii,
            "initial": {key: scalar(value) for key, value in initial.items()},
            "globalSmoothReason": "2D3C shear plus linear passive advection-diffusion",
        },
        "pureHeatLimit": {
            "BOverK3": scalar(b0),
            "dOverK4": scalar(d0),
            "YOverK2": scalar(y0),
            "FParentSquaredOverK2": scalar(f0_squared),
            "qOverK2": scalar(q0),
            "a": scalar(amplitude0),
            "thetaStar": scalar(theta_star),
            "BAtThetaStarOverK3": scalar(b_star),
            "dAtThetaStarOverK4": scalar(d_star),
            "YAtThetaStarOverK2": scalar(y_star),
            "FAtThetaStarSquaredOverK2": scalar(f_star),
            "qAtThetaStarOverK2": scalar(q_star),
            "aAtThetaStar": scalar(amplitude_star),
            "aAtThetaStarDecimal": str(sp.N(amplitude_star, 30)),
            "weakAdvectionParameter": "1/(nu*K)",
        },
        "fullFrameSeparation": {
            "frameWeightBound": "sum_j 2^(-2j)|m_j(xi)|^2 <= 4|xi|^-2",
            "verticalSpectralGap": "|xi| >= |xi_2| >= 4*K",
            "lambOverEnstrophy": "||L||_2^2/Y <= ||V||_infty^2 = 4*exp(-2*theta)",
            "positiveCreationLower": scalar(creation_lower),
            "physicalTimeHeatUpper": scalar(heat_upper),
            "creationOverHeatLower": scalar(separation_lower),
            "scaling": "at least a fixed positive multiple of nu*K^2",
        },
        "claimBoundary": (
            "The all-shell positive-defect identity rules out cancellation after "
            "taking shellwise positive parts.  The global-smooth broad-frame "
            "witness rejects payment of total positive creation by the total "
            "physical-time heat endpoint alone.  It does not control matched "
            "spatial cells, denominator/refresh faces, another NSE budget, the "
            "full weighted-BV target, or Navier-Stokes regularity."
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    main(arguments.output)
