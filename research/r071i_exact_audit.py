#!/usr/bin/env python3
"""Exact symbolic producer for the R0.71I joint-creation release.

The audit has four independent claim layers: the hard and soft Hilbert-space
identities, the two-eigenvalue common-heat pulse, an exact Fourier
reconstruction of the global-smooth 2D3C zero-entry datum, and the cutoff
refresh gap.  The fixed-window 2D3C limit is a Duhamel estimate proved in the
report; this script checks its finite Fourier initial data and every displayed
closed-form limiting profile.  It performs no DNS or PDE time stepping.
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


def localize(module, field, delta, sign):
    chi = {
        (0, 0, 0): sp.Rational(1, 2),
        (0, 0, 1): sign * delta / 4,
        (0, 0, -1): sign * delta / 4,
    }
    localized = {}
    for chi_frequency, chi_value in chi.items():
        for frequency, value in field.items():
            output_frequency = module.add(chi_frequency, frequency)
            localized.setdefault(output_frequency, sp.zeros(3, 1))
            localized[output_frequency] += chi_value * value
    return module.tidy(localized)


def main(output: Path | None = None) -> None:
    m = load_fourier_algebra()
    nu, k = sp.symbols("nu K", positive=True)
    theta = sp.symbols("theta", nonnegative=True)

    # Hard scalar and amplitude-vector identities on one positive-denominator
    # component.  The symbols stand for the exact Hilbert contractions in the
    # report; these reductions guard signs and factors of two.
    lam, beta, y, s_value, radius, pm2, y_value = sp.symbols(
        "lambda beta y S rho pm2 Y", positive=True
    )
    beta_t = s_value - lam * beta
    q = beta**2
    q_t = sp.diff(q, beta) * beta_t
    a = q / y_value
    y_t = y * y_value
    a_t = sp.diff(a, beta) * beta_t + sp.diff(a, y_value) * y_t
    hard_scalar_residual = sp.simplify(
        a_t + (2 * lam + y) * a - 2 * beta * s_value / y_value
    )
    assert hard_scalar_residual == 0

    z, joint = sp.symbols("z J", positive=True)
    z_t = joint - lam * z
    normalized_a_t = sp.diff(z**2, z) * z_t
    normalized_residual = sp.simplify(
        normalized_a_t + 2 * lam * z**2 - 2 * z * joint
    )
    assert normalized_residual == 0
    vector_radial_square = sp.expand(joint**2)
    vector_tangent_square = sp.expand(z**2 * pm2 / radius**2)

    # Soft denominator ledger.  theta_epsilon is the exact radial mass defect.
    theta_epsilon = sp.symbols("theta_epsilon", nonnegative=True)
    beta_epsilon, s_epsilon = sp.symbols(
        "beta_epsilon S_epsilon", positive=True
    )
    beta_epsilon_t = s_epsilon - lam * (1 + theta_epsilon) * beta_epsilon
    a_epsilon = beta_epsilon**2 / y_value
    a_epsilon_t = (
        sp.diff(a_epsilon, beta_epsilon) * beta_epsilon_t
        + sp.diff(a_epsilon, y_value) * y_t
    )
    soft_scalar_residual = sp.simplify(
        a_epsilon_t
        + (2 * lam * (1 + theta_epsilon) + y) * a_epsilon
        - 2 * beta_epsilon * s_epsilon / y_value
    )
    assert soft_scalar_residual == 0

    # Common-heat zero-face pulse.  x=exp(-2*nu*K^2*t).
    x = sp.symbols("x", positive=True)
    pulse_a = x * (1 - x) ** 2 / (2 * (1 + x))
    pulse_derivative = sp.factor(sp.diff(pulse_a, x))
    x_star = (sp.sqrt(17) - 3) / 4
    pulse_peak = sp.simplify(pulse_a.subs(x, x_star))
    pulse_tv = sp.simplify(2 * pulse_peak)
    heat_volume = sp.Rational(3, 8) / (nu * k**4)
    volume_ratio = sp.simplify((pulse_tv / k**2) / heat_volume)
    expected_derivative = (
        (x - 1) * (2 * x**2 + 3 * x - 1) / (2 * (x + 1) ** 2)
    )
    assert sp.simplify(pulse_derivative - expected_derivative) == 0
    assert pulse_peak == (71 - 17 * sp.sqrt(17)) / 16
    assert volume_ratio == nu * (71 - 17 * sp.sqrt(17)) * k**2 / 3

    tau = sp.symbols("tau", nonnegative=True)
    sx = sp.exp(-2 * tau)
    joint_over_nuk2 = sp.simplify(
        sx ** sp.Rational(3, 2)
        * (sx + 3)
        / (sp.sqrt(2) * (1 + sx) ** sp.Rational(3, 2))
    )
    joint_square_integral = sp.simplify(
        sp.integrate(
            joint_over_nuk2**2,
            (tau, 0, sp.oo),
        )
    )
    assert joint_square_integral == sp.Rational(3, 4) * (1 - sp.log(2))

    # Symmetric, radial two-ring, true 2D3C zero-entry datum at K=1.
    imaginary = sp.I
    e2 = sp.Matrix([0, 1, 0])
    e3 = sp.Matrix([0, 0, 1])
    velocity = {
        (1, 0, 0): e2,
        (-1, 0, 0): e2,
        (0, 2, 0): imaginary * e3 / 2,
        (0, -2, 0): -imaginary * e3 / 2,
        (0, 3, 0): -imaginary * e3 / 3,
        (0, -3, 0): imaginary * e3 / 3,
    }
    for channel, coefficient in (
        (2, sp.Rational(1, 5)),
        (3, sp.Rational(1, 10)),
    ):
        for horizontal_sign in (-1, 1):
            velocity[(horizontal_sign, channel, 0)] = coefficient * e3
            velocity[(-horizontal_sign, -channel, 0)] = coefficient * e3

    keep = {
        (horizontal_sign, vertical_frequency, 0)
        for horizontal_sign in (-1, 1)
        for vertical_frequency in (-3, -2, 2, 3)
    }
    omega = m.curl(velocity)
    lamb = m.project(m.cross_product(velocity, omega))
    f_value = {frequency: value for frequency, value in lamb.items() if frequency in keep}
    c_value = m.curl(
        {frequency: value for frequency, value in omega.items() if frequency in keep}
    )
    initial = {
        "kineticEnergy": m.l2_norm_squared(velocity),
        "YOverK2": m.l2_norm_squared(omega),
        "FNormSquaredOverK2": m.l2_norm_squared(f_value),
        "dOverK4": m.l2_norm_squared(c_value),
        "BOverK3": m.l2_pair(f_value, c_value),
    }
    assert initial == {
        "kineticEnergy": sp.Rational(263, 90),
        "YOverK2": sp.Rational(36, 5),
        "FNormSquaredOverK2": 8,
        "dOverK4": 8,
        "BOverK3": 0,
    }

    leading_x = sp.exp(-10 * theta)
    q0 = sp.simplify(4 * leading_x * (1 - leading_x) ** 2 / (1 + leading_x))
    y0 = (
        2 * sp.exp(-2 * theta)
        + 2 * sp.exp(-8 * theta)
        + 2 * sp.exp(-18 * theta)
        + sp.Rational(4, 5) * sp.exp(-10 * theta)
        + sp.Rational(2, 5) * sp.exp(-20 * theta)
    )
    f0_squared = 4 * (sp.exp(-10 * theta) + sp.exp(-20 * theta))
    a0 = sp.simplify(q0 / y0)
    g0 = sp.simplify(f0_squared / y0)
    theta_star = sp.log(2) / 10
    q0_star = sp.simplify(q0.subs(theta, theta_star))
    a0_star = sp.simplify(a0.subs(theta, theta_star))
    assert q0.subs(theta, 0) == 0
    assert q0_star == sp.Rational(1, 3)
    expected_a0_star = 2 / (
        3 * (1 + 3 * 2 ** sp.Rational(1, 5) + 2 * 2 ** sp.Rational(4, 5))
    )
    assert sp.simplify(a0_star - expected_a0_star) == 0

    # Exact complementary-cutoff refresh gap on the R0.71G six-mode datum.
    alpha, delta, fixed_u = sp.symbols("alpha delta U", positive=True)
    base_velocity = {
        frequency: m.clean(alpha * value)
        for frequency, value in m.six_mode_velocity().items()
    }
    base_omega = m.curl(base_velocity)
    low_omega = m.low_shell(base_omega)
    base_lamb = m.project(m.cross_product(base_velocity, base_omega))
    low_lamb = m.low_shell(base_lamb)
    y_base = m.l2_norm_squared(base_omega)
    assert y_base == 8 * alpha**2
    cutoff_rows = {}
    for sign in (-1, 1):
        localized_c = m.curl(localize(m, low_omega, delta, sign))
        b_value = m.clean(m.l2_pair(low_lamb, localized_c))
        d_value = m.clean(m.l2_norm_squared(localized_c))
        a_value = m.clean((b_value**2 / d_value) / y_base)
        assert b_value == alpha**3
        assert sp.simplify(
            d_value - alpha**2 * (3 * delta**2 + 4) / 4
        ) == 0
        assert sp.simplify(
            a_value - alpha**2 / (2 * (3 * delta**2 + 4))
        ) == 0
        cutoff_rows[str(sign)] = {
            "BOverK6": str(b_value),
            "dOverK6": str(d_value),
            "aOverK2": str(a_value),
        }
    aggregate = alpha**2 * k**2 / (3 * delta**2 + 4)
    refresh_gap = sp.simplify(aggregate.subs(delta, 0) - aggregate.subs(delta, 1))
    fixed_energy_gap = sp.simplify(refresh_gap.subs(alpha, fixed_u / k))
    assert refresh_gap == 3 * alpha**2 * k**2 / 28
    assert fixed_energy_gap == 3 * fixed_u**2 / 28

    payload = {
        "status": "joint-identity-closed-heat-volume-alone-rejected",
        "hardIdentity": {
            "scalarResidual": str(hard_scalar_residual),
            "normalizedResidual": str(normalized_residual),
            "amplitudeVectorRadialSquare": str(vector_radial_square),
            "amplitudeVectorTangentSquare": str(vector_tangent_square),
        },
        "softIdentity": {
            "scalarResidual": str(soft_scalar_residual),
            "radialDamping": "lambda*epsilon/(d+epsilon)",
            "sign": "plus on the left-hand side",
        },
        "commonHeatZeroFacePulse": {
            "a": str(pulse_a),
            "xAtPeak": str(x_star),
            "aPeak": str(pulse_peak),
            "totalVariation": str(pulse_tv),
            "weightedHeatVolume": str(heat_volume),
            "weightedVariationOverVolume": str(volume_ratio),
            "jointOverNuK2": str(joint_over_nuk2),
            "integralJointSquaredOverNuK2": str(joint_square_integral),
            "boundary": "common heat Hilbert pair, not by itself an NSE F/C pair",
        },
        "true2D3CZeroEntryPulse": {
            "multiplier": "fixed smooth radial real-even two-ring template near |xi/K|^2=5,10",
            "retainedModesAtK1": [list(frequency) for frequency in sorted(keep)],
            "initial": {key: str(value) for key, value in initial.items()},
            "weakAdvectionParameter": "1/(nu*K)",
            "leadingQOverK2": str(q0),
            "leadingYOverK2": str(y0),
            "leadingF2OverK2": str(f0_squared),
            "leadingA": str(a0),
            "leadingG": str(g0),
            "thetaStar": str(theta_star),
            "qAtThetaStar": str(q0_star),
            "aAtThetaStar": str(a0_star),
            "weightedBVScale": "at least a0(thetaStar)/(2*K**2)",
            "weightedHeatVolumeScale": "O(K**-4)",
            "boundary": "adapted two-ring component, not every preassigned dyadic frame",
        },
        "cutoffRefresh": {
            "cutoffs": "(1 +/- delta*cos(K*x3))/2",
            "cells": cutoff_rows,
            "aggregate": str(aggregate),
            "oneRefreshGap": str(refresh_gap),
            "fixedEnergyGap": str(fixed_energy_gap),
            "boundary": "uncontrolled refresh only",
        },
        "claimBoundary": (
            "The exact identities and global-smooth 2D3C pulse reject control "
            "of one-sided joint creation by the R0.71F heat volume alone for "
            "the declared multiplier. They do not reject the full weighted-BV "
            "target or prove any regularity theorem."
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
