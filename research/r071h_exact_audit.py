#!/usr/bin/env python3
"""Exact symbolic audit for the R0.71H global-smooth 2D3C witness.

The program reconstructs the normalized six-mode datum at a=K=1 from the
R0.71G exact Fourier algebra, verifies the angular and source-curvature
identities, and records their exact rescaling. It performs no numerical
integration and does not claim a time-integrated no-go.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
R071G = ROOT / "research" / "r071g_exact_audit.py"


def load_r071g():
    spec = importlib.util.spec_from_file_location("r071g_exact", R071G)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load R0.71G exact audit")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(output: Path | None = None) -> None:
    m = load_r071g()
    nu = sp.symbols("nu", positive=True)
    a, k, energy = sp.symbols("a K energy", positive=True)

    velocity = m.six_mode_velocity()
    omega = m.curl(velocity)
    lamb = m.project(m.cross_product(velocity, omega))
    velocity_t = m.linear_combination(lamb, m.laplacian(velocity), 1, nu)
    omega_t = m.curl(velocity_t)
    lamb_t = m.project(
        m.linear_combination(
            m.cross_product(velocity_t, omega),
            m.cross_product(velocity, omega_t),
        )
    )

    c = m.curl(m.low_shell(omega))
    c_t = m.curl(m.low_shell(omega_t))
    f_t = m.low_shell(lamb_t)
    d = m.l2_norm_squared(c)
    radial_rate = m.clean(m.l2_pair(c, c_t) / d)
    perpendicular_c_t = m.linear_combination(c_t, c, 1, -radial_rate)

    base = {
        "kineticEnergy": m.l2_norm_squared(velocity),
        "Y": m.l2_norm_squared(omega),
        "d": d,
        "FtNormSquared": m.l2_norm_squared(f_t),
        "radialRate": radial_rate,
        "perpendicularCtNormSquared": m.l2_norm_squared(perpendicular_c_t),
        "angularRatioSquared": m.clean(
            m.l2_norm_squared(perpendicular_c_t) / d
        ),
    }

    assert base["kineticEnergy"] == 6
    assert base["Y"] == 8
    assert base["d"] == 4
    assert m.clean(base["FtNormSquared"] - 2 * (3 * nu + 2) ** 2) == 0
    assert m.clean(base["perpendicularCtNormSquared"] - 1) == 0
    assert m.clean(base["angularRatioSquared"] - sp.Rational(1, 4)) == 0

    velocity_a = {
        frequency: m.clean(a * value) for frequency, value in velocity.items()
    }
    omega_a = m.curl(velocity_a)
    lamb_a = m.project(m.cross_product(velocity_a, omega_a))
    velocity_a_t = m.linear_combination(
        lamb_a, m.laplacian(velocity_a), 1, nu
    )
    omega_a_t = m.curl(velocity_a_t)
    lamb_a_t = m.project(
        m.linear_combination(
            m.cross_product(velocity_a_t, omega_a),
            m.cross_product(velocity_a, omega_a_t),
        )
    )
    c_a = m.curl(m.low_shell(omega_a))
    c_a_t = m.curl(m.low_shell(omega_a_t))
    d_a = m.l2_norm_squared(c_a)
    radial_rate_a = m.clean(m.l2_pair(c_a, c_a_t) / d_a)
    perpendicular_c_a_t = m.linear_combination(
        c_a_t, c_a, 1, -radial_rate_a
    )
    f_a = m.low_shell(lamb_a)
    sqrt_d_a = sp.sqrt(d_a)
    e_a = {
        frequency: m.clean(value / sqrt_d_a)
        for frequency, value in c_a.items()
    }
    beta_a = m.clean(m.l2_pair(f_a, c_a) / sqrt_d_a)
    perpendicular_f_a = m.linear_combination(
        f_a, e_a, 1, -beta_a
    )
    e_a_t = {
        frequency: m.clean(value / sqrt_d_a)
        for frequency, value in perpendicular_c_a_t.items()
    }
    beta_angular_a = m.clean(m.l2_pair(perpendicular_f_a, e_a_t))
    q_angular_a = m.clean(2 * beta_a * beta_angular_a)
    normalized_angular_a = m.clean(
        q_angular_a / m.l2_norm_squared(omega_a)
    )
    amplitude_exact = {
        "kineticEnergy": m.l2_norm_squared(velocity_a),
        "Y": m.l2_norm_squared(omega_a),
        "d": d_a,
        "FtNormSquared": m.l2_norm_squared(m.low_shell(lamb_a_t)),
        "perpendicularCtNormSquared": m.l2_norm_squared(perpendicular_c_a_t),
        "betaAngularTerm": beta_angular_a,
        "qAngularTerm": q_angular_a,
        "qOverYAngularTerm": normalized_angular_a,
    }
    assert amplitude_exact["kineticEnergy"] == 6 * a**2
    assert amplitude_exact["Y"] == 8 * a**2
    assert amplitude_exact["d"] == 4 * a**2
    assert m.clean(
        amplitude_exact["FtNormSquared"]
        - 2 * a**4 * (2 * a + 3 * nu) ** 2
    ) == 0
    assert m.clean(
        amplitude_exact["perpendicularCtNormSquared"] - a**4
    ) == 0
    assert m.clean(amplitude_exact["betaAngularTerm"] - a**3 / 2) == 0
    assert m.clean(amplitude_exact["qAngularTerm"] - a**5) == 0
    assert m.clean(amplitude_exact["qOverYAngularTerm"] - a**3 / 8) == 0

    source = m.clean(
        k ** (-4)
        * (2 * a**4 * (3 * nu + 2 * a) ** 2 * k**10)
        / (8 * a**2 * k**4)
    )
    angular_squared = m.clean((a**4 * k**10) / (4 * a**2 * k**6))
    normalized = m.clean((a**4 * k**6) / (8 * a**2 * k**4))
    normalized_log_derivative = -(5 * a + 6 * nu) * k**2 / 2

    assert source == a**2 * k**2 * (2 * a + 3 * nu) ** 2 / 4
    assert angular_squared == a**2 * k**4 / 4
    assert normalized == a**2 * k**2 / 8

    u = sp.sqrt(energy / 6)
    fixed_energy_source = m.clean(source.subs(a, u / k))
    fixed_energy_angular_squared = m.clean(angular_squared.subs(a, u / k))
    fixed_energy_d = m.clean((4 * a**2 * k**6).subs(a, u / k))

    assert sp.limit(fixed_energy_source, k, sp.oo) == 3 * energy * nu**2 / 8
    assert sp.limit(fixed_energy_angular_squared, k, sp.oo) == sp.oo
    assert fixed_energy_d == 2 * energy * k**4 / 3

    delta = sp.symbols("delta", positive=True)
    chi = {
        (0, 0, 0): sp.Rational(1, 2),
        (0, 0, 1): delta / 4,
        (0, 0, -1): delta / 4,
    }
    low_w = m.low_shell(omega)
    localized_w = {}
    for chi_frequency, chi_value in chi.items():
        for frequency, value in low_w.items():
            output_frequency = m.add(chi_frequency, frequency)
            localized_w.setdefault(output_frequency, sp.zeros(3, 1))
            localized_w[output_frequency] += chi_value * value
    localized_c = m.curl(m.tidy(localized_w))
    localized_d = m.l2_norm_squared(localized_c)
    localized_gradient = m.clean(
        sum(
            m.l2_norm_squared(m.derivative(localized_c, coordinate))
            for coordinate in range(3)
        )
    )
    heat_commutator = m.linear_combination(
        m.laplacian(localized_c), localized_c, 1, 1
    )
    commutator_radial = m.clean(
        m.l2_pair(localized_c, heat_commutator) / localized_d
    )
    perpendicular_commutator = m.linear_combination(
        heat_commutator, localized_c, 1, -commutator_radial
    )
    localized_rayleigh = m.clean(localized_gradient / localized_d)
    localized_projective_source = m.clean(
        m.l2_norm_squared(perpendicular_commutator) / localized_d
    )
    assert m.clean(
        localized_d - (3 * delta**2 + 4) / 4
    ) == 0
    assert m.clean(
        localized_rayleigh
        - 2 * (3 * delta**2 + 2) / (3 * delta**2 + 4)
    ) == 0
    assert m.clean(
        localized_projective_source
        - 12 * delta**2 / (3 * delta**2 + 4) ** 2
    ) == 0

    payload = {
        "status": "pointwise-angular-no-go-only",
        "baseExact": {key: str(value) for key, value in base.items()},
        "amplitudeExactAtK1": {
            key: str(value) for key, value in amplitude_exact.items()
        },
        "rescaled": {
            "kineticEnergy": "6*a**2*K**2",
            "d": "4*a**2*K**6",
            "sourceDensity": str(source),
            "angularRatioSquared": str(angular_squared),
            "qOverY": str(normalized),
            "qOverYLogDerivative": str(normalized_log_derivative),
            "qOverYAngularTerm": "a**3*K**4/8",
        },
        "fixedEnergy": {
            "a": "sqrt(energy/6)/K",
            "d": str(fixed_energy_d),
            "sourceDensity": str(fixed_energy_source),
            "sourceDensityLimit": str(3 * energy * nu**2 / 8),
            "angularRatioSquared": str(fixed_energy_angular_squared),
            "angularRatio": "sqrt(energy/6)*K/2",
            "qOverYAngularTerm": "(energy/6)**(3/2)*K/8",
            "pointwiseAngularDiverges": True,
            "denominatorStrictlyPositive": True,
        },
        "finiteFourierCutoff": {
            "chi": "(1+delta*cos(z))/2",
            "deltaRange": "0<delta<=1",
            "denominator": str(localized_d),
            "K^-2RayleighQuotient": str(localized_rayleigh),
            "projectiveHeatCommutatorRatio": str(
                localized_projective_source
            ),
            "K^-2IntegratedProjectiveSourceLimit": (
                "nu*M*12*delta**2/(3*delta**2+4)**2"
            ),
            "decision": "finite positive saturation, not divergence",
        },
        "scaling": {
            "K": 1,
            "qOverY": 2,
            "TV_qOverY": 2,
            "K^-2_TV_qOverY": 0,
            "sourceDensity": 2,
            "timeIntegratedSource": 0,
            "angularRatio": 2,
            "timeIntegratedAngularRatio": 0,
            "kineticEnergy": -1,
        },
        "claimBoundary": (
            "The exact global-smooth 2D3C family disproves a finite pointwise "
            "energy-only bound for the unweighted angular ratio at d>0 for "
            "the declared low-sphere multiplier. It does not disprove the "
            "scale-weighted BV or time-integrated source/angular budgets, "
            "or assert the same witness for every preassigned smooth frame."
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
