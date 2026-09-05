#!/usr/bin/env python3
"""Exact rational Fourier regression for D.13, D.16, D.18, D.20.

This checks a finite initial slice, not NS evolution or a PDE theorem.
No third-party packages, floating point, simulations, or random sampling.
"""

from fractions import Fraction as F
import json
import platform


ZERO = (F(0), F(0))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def conjugate(a):
    return (a[0], -a[1])


def product(a, b):
    result = {}
    for k, ak in a.items():
        for l, bl in b.items():
            wave = (k[0] + l[0], k[1] + l[1])
            result[wave] = add(result.get(wave, ZERO), mul(ak, bl))
    return {k: v for k, v in result.items() if v != ZERO}


def derivative(a, axis):
    return {k: mul((F(0), F(k[axis])), v)
            for k, v in a.items() if k[axis]}


def field(first_sign=-1, keep_diagonal=True):
    half = F(1, 2)
    u = [
        {(0, 1): (first_sign * half, F(0)),
         (0, -1): (first_sign * half, F(0))},
        {},
        {(1, 0): (F(0), -half), (-1, 0): (F(0), half)},
    ]
    if keep_diagonal:
        u[2].update({(1, 1): (half, F(0)), (-1, -1): (half, F(0))})
    return u


def coefficients(u):
    adv = []
    for component in u:
        value = {}
        for axis in (0, 1):
            for k, v in product(u[axis], derivative(component, axis)).items():
                value[k] = add(value.get(k, ZERO), v)
        adv.append({k: v for k, v in value.items() if v != ZERO})
    energy, dissipation, production = {}, {}, {}
    for component, nonlinear in zip(u, adv):
        for k, uk in component.items():
            radius_squared = sum(n * n for n in k)
            e = mul(conjugate(uk), uk)
            assert e[1] == 0
            energy[radius_squared] = energy.get(radius_squared, F(0)) + e[0]
            dissipation[radius_squared] = (
                dissipation.get(radius_squared, F(0)) + radius_squared * e[0]
            )
            transfer = mul(conjugate(uk), nonlinear.get(k, ZERO))
            production[radius_squared] = add(
                production.get(radius_squared, ZERO), (-transfer[0], -transfer[1])
            )
    assert all(value[1] == 0 for value in production.values())
    return energy, dissipation, {k: v[0] for k, v in production.items()}


def encoded(values):
    return {str(k): str(v) for k, v in sorted(values.items())}


def main():
    energy, dissipation, production = coefficients(field())
    assert energy == {1: F(1), 2: F(1, 2)}
    assert dissipation == {1: F(1), 2: F(1)}
    assert production == {1: F(-1, 4), 2: F(1, 4)}
    assert sum(production.values()) == 0
    limiting = lambda values: sum(F(k * k) * v for k, v in values.items())
    ratio_d = limiting(production) / limiting(dissipation)
    ratio_de = limiting(production) / (limiting(dissipation) + limiting(energy))
    assert ratio_d == F(3, 20)
    assert ratio_de == F(3, 32)

    reversed_production = coefficients(field(first_sign=1))[2]
    removed_production = coefficients(field(keep_diagonal=False))[2]
    assert reversed_production == {k: -v for k, v in production.items()}
    assert reversed_production != production
    assert all(v == 0 for v in removed_production.values())
    assert removed_production != production

    return {
        "status": "PASS",
        "arithmetic": "fractions.Fraction Gaussian rationals; no floating point",
        "normalization": "torus average, A=1; d1^2 and d2^2 factored out",
        "energy_coefficients_by_squared_wave_number": encoded(energy),
        "dissipation_coefficients_by_squared_wave_number": encoded(dissipation),
        "nonlinear_production_coefficients_by_squared_wave_number": encoded(production),
        "initial_L2_squared": str(sum(energy.values())),
        "initial_gradient_L2_squared": str(sum(dissipation.values())),
        "initial_H1_squared": str(sum(energy.values()) + sum(dissipation.values())),
        "small_R_production_over_dissipation_per_A": str(ratio_d),
        "small_R_production_over_energy_plus_dissipation_per_A": str(ratio_de),
        "input_sensitivity": {
            "reversing_first_component_reverses_production": True,
            "removing_diagonal_mode_annuls_production": True,
        },
        "not_checked": [
            "positive-time PDE solution",
            "Fourier multiplier limiting theorem",
            "weak endpoint energy identity",
            "moving cutoff paid inequality",
            "regularity or singularity",
        ],
        "runtime": {
            "python": platform.python_version(),
            "machine": platform.machine(),
            "system": platform.system(),
            "workers": 1,
            "precision": "exact rational",
            "seed": None,
        },
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
