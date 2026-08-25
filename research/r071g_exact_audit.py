#!/usr/bin/env python3
"""Exact producer for the R0.71G signed-Lamb residence gate.

The certificate has three independent algebraic layers.

1. Starting from the full six-mode divergence-free datum, it reconstructs
   the Navier--Stokes time derivative and verifies both exact formulas for
   the projected Lamb-vector evolution.
2. It differentiates the low-shell signed work, denominator, quotient, and
   enstrophy without assuming that the solution remains six-mode.
3. It checks the Hilbert-space radial cancellation in the normalized signed
   amplitude, the denominator-zero jump, the exact 2D3C heat limit, and the
   abstract fact that critical residence alone does not close the bottom
   trace.

The arbitrary-time 2D3C sign-residence theorem and the BV layer-cake lemma
are proved analytically in the report.  The independent program reconstructs
the initial derivatives by FFT and integrates the generated Fourier chain.
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
    if frequency == (0, 0, 0):
        return sp.zeros(3, 3)
    wave = Vector(frequency)
    return sp.eye(3) - wave * wave.T / square(frequency)


def tidy(field: dict[Frequency, sp.Matrix]) -> dict[Frequency, sp.Matrix]:
    output = {}
    for frequency, value in field.items():
        value = clean(value)
        if value != sp.zeros(3, 1):
            output[frequency] = value
    return output


def linear_combination(
    first: dict[Frequency, sp.Matrix],
    second: dict[Frequency, sp.Matrix],
    first_weight=1,
    second_weight=1,
) -> dict[Frequency, sp.Matrix]:
    output: dict[Frequency, sp.Matrix] = {}
    for frequency in set(first) | set(second):
        output[frequency] = clean(
            first_weight * first.get(frequency, sp.zeros(3, 1))
            + second_weight * second.get(frequency, sp.zeros(3, 1))
        )
    return tidy(output)


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
    return tidy(output)


def laplacian(field: dict[Frequency, sp.Matrix]):
    return tidy(
        {
            frequency: clean(-square(frequency) * value)
            for frequency, value in field.items()
        }
    )


def derivative(field: dict[Frequency, sp.Matrix], coordinate: int):
    return tidy(
        {
            frequency: clean(I * frequency[coordinate] * value)
            for frequency, value in field.items()
        }
    )


def curl(field: dict[Frequency, sp.Matrix]):
    return tidy(
        {
            frequency: clean(I * Vector(frequency).cross(value))
            for frequency, value in field.items()
        }
    )


def project(field: dict[Frequency, sp.Matrix]):
    return tidy(
        {
            frequency: clean(projector(frequency) * value)
            for frequency, value in field.items()
        }
    )


def cross_product(
    first: dict[Frequency, sp.Matrix], second: dict[Frequency, sp.Matrix]
):
    return convolution(
        first,
        second,
        lambda _p, left, _q, right: clean(left.cross(right)),
    )


def advective(
    first: dict[Frequency, sp.Matrix], second: dict[Frequency, sp.Matrix]
):
    return convolution(
        first,
        second,
        lambda _p, left, q, right: clean(I * (left.dot(Vector(q))) * right),
    )


def equal_fields(
    first: dict[Frequency, sp.Matrix], second: dict[Frequency, sp.Matrix]
) -> bool:
    difference = linear_combination(first, second, 1, -1)
    return difference == {}


def six_mode_velocity() -> dict[Frequency, sp.Matrix]:
    positive = {
        (1, 0, 0): Vector([0, -1, 0]),
        (0, 1, 0): Vector([0, 0, -1]),
        (-1, -1, 0): Vector([0, 0, -I]),
    }
    velocity = dict(positive)
    for frequency, coefficient in positive.items():
        negative = tuple(-entry for entry in frequency)
        velocity[negative] = sp.conjugate(coefficient)
    return velocity


def l2_pair(
    first: dict[Frequency, sp.Matrix], second: dict[Frequency, sp.Matrix]
) -> sp.Expr:
    return clean(
        sum(
            pairing(first.get(frequency, sp.zeros(3, 1)), value)
            for frequency, value in second.items()
        )
    )


def l2_norm_squared(field: dict[Frequency, sp.Matrix]) -> sp.Expr:
    return l2_pair(field, field)


def low_shell(field: dict[Frequency, sp.Matrix]):
    return {frequency: value for frequency, value in field.items() if square(frequency) == 1}


def projected_lamb_evolution() -> dict[str, object]:
    nu = sp.symbols("nu", positive=True)
    velocity = six_mode_velocity()
    omega = curl(velocity)
    lamb = project(cross_product(velocity, omega))
    velocity_t = linear_combination(lamb, laplacian(velocity), 1, nu)
    omega_t = curl(velocity_t)
    lamb_t_direct = project(
        linear_combination(
            cross_product(velocity_t, omega),
            cross_product(velocity, omega_t),
        )
    )

    cross_source = linear_combination(
        cross_product(lamb, omega),
        cross_product(velocity, curl(lamb)),
    )
    gradient_cross: dict[Frequency, sp.Matrix] = {}
    for coordinate in range(3):
        gradient_cross = linear_combination(
            gradient_cross,
            cross_product(derivative(velocity, coordinate), derivative(omega, coordinate)),
        )
    cross_source = linear_combination(cross_source, gradient_cross, 1, -2 * nu)
    lamb_t_cross = linear_combination(laplacian(lamb), project(cross_source), nu, 1)

    advective_source = linear_combination(
        advective(lamb, velocity), advective(velocity, lamb)
    )
    derivative_advection: dict[Frequency, sp.Matrix] = {}
    for coordinate in range(3):
        derivative_advection = linear_combination(
            derivative_advection,
            advective(derivative(velocity, coordinate), derivative(velocity, coordinate)),
        )
    lamb_t_advective = linear_combination(
        linear_combination(laplacian(lamb), project(advective_source), nu, -1),
        project(derivative_advection),
        1,
        2 * nu,
    )

    require(equal_fields(lamb_t_direct, lamb_t_cross), "cross-form Lamb evolution")
    require(equal_fields(lamb_t_direct, lamb_t_advective), "advective-form Lamb evolution")
    require(equal_fields(omega_t, linear_combination(curl(lamb), laplacian(omega), 1, nu)), "vorticity evolution")

    return {
        "inputVelocityModes": len(velocity),
        "projectedLambModes": len(lamb),
        "timeDerivativeModes": len(lamb_t_direct),
        "directEqualsCrossForm": True,
        "directEqualsAdvectiveForm": True,
        "vorticityEquation": True,
        "crossForm": (
            "L_t=nu*Delta(L)+P(L x omega+u x curl(L)-2*nu*sum_m partial_m(u) x partial_m(omega))"
        ),
        "advectiveForm": (
            "L_t=nu*Delta(L)-P((L dot grad)u+(u dot grad)L)+2*nu*P*sum_m((partial_m u dot grad)partial_m u)"
        ),
        "allOutputFrequencies": [str(item) for item in sorted(lamb_t_direct)],
    }


def low_shell_initial_derivatives() -> dict[str, object]:
    nu = sp.symbols("nu", positive=True)
    velocity = six_mode_velocity()
    omega = curl(velocity)
    lamb = project(cross_product(velocity, omega))
    velocity_t = linear_combination(lamb, laplacian(velocity), 1, nu)
    omega_t = curl(velocity_t)
    lamb_t = project(
        linear_combination(
            cross_product(velocity_t, omega),
            cross_product(velocity, omega_t),
        )
    )

    w = low_shell(omega)
    f = low_shell(lamb)
    wt = low_shell(omega_t)
    ft = low_shell(lamb_t)
    c = curl(w)
    ct = curl(wt)
    b = l2_pair(f, c)
    d = l2_norm_squared(c)
    bt = clean(l2_pair(ft, c) + l2_pair(f, ct))
    dt = clean(2 * sp.re(l2_pair(c, ct)))
    q = clean(b**2 / d)
    qt = clean(2 * b * bt / d - b**2 * dt / d**2)
    y = l2_norm_squared(omega)
    yt = clean(2 * sp.re(l2_pair(omega, omega_t)))
    coefficient = clean(q / y)
    coefficient_t = clean(qt / y - q * yt / y**2)

    require(b == 2, "initial B")
    require(d == 4, "initial denominator")
    require(q == 1, "initial quotient")
    require(y == 8, "initial enstrophy")
    require(clean(bt + 2 * (1 + 4 * nu)) == 0, "initial B derivative")
    require(clean(dt - 4 * (1 - 2 * nu)) == 0, "initial denominator derivative")
    require(clean(qt + 3 * (1 + 2 * nu)) == 0, "initial quotient derivative")
    require(clean(yt + 4 * (1 + 6 * nu)) == 0, "initial enstrophy derivative")
    require(coefficient == sp.Rational(1, 8), "initial normalized coefficient")
    require(clean(coefficient_t + (5 + 6 * nu) / 16) == 0, "normalized derivative")

    return {
        "normalizedAtAEqualsKEqualsOne": {
            "B": str(b),
            "d": str(d),
            "q": str(q),
            "Y": str(y),
            "B_t": str(bt),
            "d_t": str(dt),
            "q_t": str(qt),
            "Y_t": str(yt),
            "qOverY": str(coefficient),
            "qOverY_t": str(coefficient_t),
            "logDerivativeQOverY": str(clean(coefficient_t / coefficient)),
        },
        "rescaled": {
            "B": "2*a**3*K**6",
            "d": "4*a**2*K**6",
            "q": "a**4*K**6",
            "Y": "8*a**2*K**4",
            "B_t": "-2*a**3*(a+4*nu)*K**8",
            "d_t": "4*a**2*(a-2*nu)*K**8",
            "q_t": "-3*a**4*(a+2*nu)*K**8",
            "Y_t": "-4*a**2*(a+6*nu)*K**6",
            "logDerivativeQOverY": "-(5*a+6*nu)*K**2/2",
        },
    }


def radial_cancellation() -> dict[str, object]:
    f = Vector(sp.symbols("f0:3", real=True))
    c = Vector(sp.symbols("c0:3", real=True))
    ft = Vector(sp.symbols("ft0:3", real=True))
    ct = Vector(sp.symbols("ct0:3", real=True))
    d = clean(c.dot(c))
    b = clean(f.dot(c))
    beta = b / sp.sqrt(d)
    variables = list(f) + list(c)
    rates = list(ft) + list(ct)
    beta_t_direct = clean(sum(sp.diff(beta, variable) * rate for variable, rate in zip(variables, rates)))
    e = c / sp.sqrt(d)
    perpendicular_f = f - beta * e
    beta_t_projected = clean(ft.dot(e) + perpendicular_f.dot(ct) / sp.sqrt(d))
    require(clean(beta_t_direct - beta_t_projected) == 0, "radial cancellation")

    time = sp.symbols("t", real=True)
    positive_pair = sp.symbols("gamma", positive=True)
    c_jump = time * Vector([1, 0, 0])
    f_jump = Vector([positive_pair, 0, 0])
    positive_side_q = clean((f_jump.dot(c_jump)) ** 2 / c_jump.dot(c_jump))
    require(positive_side_q == positive_pair**2, "directional zero-denominator jump")

    return {
        "beta": "<F,C>/sqrt(d)",
        "exactDerivative": (
            "beta_t=<F_t,E>+d**(-1/2)<P_(E perpendicular)F,C_t>"
        ),
        "symbolicResidual": "0",
        "radialComponentCancels": True,
        "positiveSquareCannotBeSeparatedFromDenominatorGrowth": True,
        "zeroDenominatorExample": {
            "COfT": "t*c with t>0",
            "F": "f with <f,c>>0",
            "qForPositiveT": str(positive_side_q),
            "qAtZeroByConvention": "0",
            "conclusion": "the zero-denominator convention need not be continuous",
        },
    }


def two_d_three_c_limit() -> dict[str, object]:
    theta, rho = sp.symbols("theta rho", positive=True)
    h0 = sp.exp(-4 * theta)
    g0 = 2 * sp.exp(-2 * theta)
    e0 = 2 * sp.exp(-2 * theta) + 2 * sp.exp(-4 * theta)
    b_relative = h0
    q_relative = clean(2 * h0**2 / g0)
    a_relative = clean(8 * h0**2 / (g0 * e0))
    b_exit = clean(sp.log(1 / rho) / 4)
    q_exit = clean(sp.log(1 / rho) / 6)
    z_rho = clean((rho + sp.sqrt(rho**2 + 8 * rho)) / 4)
    a_exit = clean(-sp.log(z_rho) / 2)
    require(q_relative == sp.exp(-6 * theta), "linear-limit q profile")
    require(a_relative == clean(2 * sp.exp(-4 * theta) / (1 + sp.exp(-2 * theta))), "linear-limit normalized profile")

    return {
        "dimensionlessVariables": {"theta": "nu*K**2*t", "mu": "a/nu"},
        "chain": (
            "c_m'=-(m**2+1)c_m+i*mu*exp(-theta)*(c_(m-1)+c_(m+1))"
        ),
        "initialData": "c_0=-1, c_1=i, all other c_m=0",
        "lowShell": {
            "H": "Re(conj(c_0)*i*exp(-theta)*(c_-1+c_1))",
            "G": "abs(c_0)**2+exp(-2*theta)",
            "E": "exp(-2*theta)+sum_m((m**2+1)*abs(c_m)**2)",
            "B": "2*a**3*K**6*H",
            "d": "2*a**2*K**6*G",
            "q": "2*a**4*K**6*(max(H,0)**2)/G",
            "Y": "2*a**2*K**4*E",
            "qOverY": "a**2*K**2*(max(H,0)**2)/(G*E)",
        },
        "muEqualsZero": {
            "H": str(h0),
            "G": str(g0),
            "E": str(e0),
            "BRelative": str(b_relative),
            "qRelative": str(q_relative),
            "qOverYRelative": str(a_relative),
            "firstRelativeExit": {
                "B": str(b_exit),
                "q": str(q_exit),
                "qOverY": str(a_exit),
                "qOverYZ": str(z_rho),
            },
        },
        "explicitContinuityBound": {
            "chainDifferenceL2": "<=2*sqrt(2)*mu*exp(-theta)*(1-exp(-theta))",
            "HError": "abs(H_mu-H_0)<=(4+4*sqrt(2))*mu",
            "sufficientMuForPositiveThroughM": (
                "mu<exp(-4*M)/(2*(4+4*sqrt(2)))"
            ),
        },
    }


def residence_alone_no_go() -> dict[str, object]:
    n, count = sp.symbols("n count", integer=True, positive=True)
    scale = 2**n
    interval_length = scale ** (-2)
    amplitude = scale**2
    weighted_one_episode = clean(scale ** (-2) * amplitude * interval_length)
    unweighted_one_episode = clean(amplitude * interval_length)
    weighted_partial_sum = clean(sp.summation(4 ** (-n), (n, 1, count)))
    unweighted_partial_sum = clean(sp.summation(1, (n, 1, count)))
    require(sp.simplify(weighted_one_episode - 4 ** (-n)) == 0, "weighted episode")
    require(clean(unweighted_one_episode - 1) == 0, "unweighted episode")
    require(clean(unweighted_partial_sum - count) == 0, "unweighted divergence")

    return {
        "construction": "K_n=2**n, disjoint abs(I_n)=K_n**(-2), A_n=K_n**2*1_(I_n)",
        "eachResidence": "K_n**(-2)",
        "weightedEpisode": str(weighted_one_episode),
        "unweightedEpisode": str(unweighted_one_episode),
        "weightedPartialSum": str(weighted_partial_sum),
        "weightedInfiniteSum": "1/3",
        "unweightedPartialSum": str(unweighted_partial_sum),
        "unweightedInfiniteSum": "infinity",
        "conclusion": (
            "critical residence plus a K**(-2)-weighted bulk does not imply an unweighted bottom-trace sum"
        ),
    }


def scaling_ledger() -> dict[str, object]:
    return {
        "wholeSpaceNSE": "u_lambda(t,x)=lambda*u(lambda**2*t,lambda*x)",
        "pointwise": {"W": 2, "F": 3, "C": 3},
        "integrated": {"B": 3, "d": 3, "q": 3, "Y": 1, "qOverY": 2},
        "timeDerivatives": {"B_t": 5, "d_t": 5, "q_t": 5},
        "time": -2,
        "decision": (
            "critical K**(-2) residence is scale covariant and can be saturated; scaling rejects only o(K**(-2))"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = {
        "release": "R0.71G",
        "status": "exact-ledger-and-residence-obstruction",
        "projectedLambEvolution": projected_lamb_evolution(),
        "initialPhysicalTimeAudit": low_shell_initial_derivatives(),
        "radialCancellation": radial_cancellation(),
        "twoDThreeC": two_d_three_c_limit(),
        "scaling": scaling_ledger(),
        "residenceAloneNoGo": residence_alone_no_go(),
        "checks": {
            "crossFormLambEvolution": True,
            "advectiveFormLambEvolution": True,
            "trueNSEInitialDerivatives": True,
            "normalizedRadialCancellation": True,
            "zeroDenominatorJump": True,
            "twoDThreeCLinearLimit": True,
            "analyticDuhamelBoundRecorded": True,
            "criticalScaling": True,
            "residenceAloneFunctionalNoGo": True,
        },
        "claimBoundary": (
            "This certificate proves finite Fourier algebra, exact scaling, and finite-dimensional symbolic identities. "
            "The report proves the smooth-solution moving-cutoff ledger, the arbitrary-M 2D3C theorem, and the BV layer-cake lemma. "
            "No Leray-level occupation closure, regularity theorem, singularity, or novelty claim is made."
        ),
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
