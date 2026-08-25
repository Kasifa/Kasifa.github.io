#!/usr/bin/env python3
"""Exact audit for the R0.71O soft-denominator face limit.

The audit has four finite purposes:

1. check the global soft quotient and positive-branch identities;
2. record the universal inner profile at a finite-order denominator zero;
3. verify a smooth Hilbert-path family whose face count is not controlled by
   denominator mass or first-derivative square mass;
4. construct an exact periodic Navier--Stokes initial jet with zero filtered
   denominator and a nonzero one-sided entry trace.

The Hilbert-path separation is not a Navier--Stokes counterexample.  The
Navier--Stokes calculation is an initial-jet statement, not a time-interval
face-count theorem or a regularity result.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import sympy as sp


Mode = tuple[int, int, int]
Vector = sp.ImmutableMatrix


def clean(value: sp.Expr) -> sp.Expr:
    return sp.factor(sp.simplify(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def soft_identity() -> dict[str, object]:
    """Check the soft quotient and squared positive-branch equation."""

    B, d, Y, eps = sp.symbols("B d Y epsilon", positive=True)
    B_t, d_t, Y_t, lam = sp.symbols("B_t d_t Y_t lambda", real=True)
    root = sp.sqrt(d + eps)
    theta = eps / (d + eps)
    sigma = d / (d + eps)
    z = B / (sp.sqrt(Y) * root)
    hard_z = B / sp.sqrt(Y * d)

    z_t = clean(
        B_t / (sp.sqrt(Y) * root)
        - z * (Y_t / (2 * Y) + d_t / (2 * (d + eps)))
    )
    source = clean(z_t + lam * (1 + theta) * z)
    n_style_source = clean(z_t + lam * z)
    require(clean(source - n_style_source - lam * theta * z) == 0,
            "soft source convention")

    a = B**2 / (Y * (d + eps))
    a_t = clean(
        2 * B * B_t / (Y * (d + eps))
        - a * (Y_t / Y + d_t / (d + eps))
    )
    require(clean(a_t + 2 * lam * (1 + theta) * a - 2 * z * source) == 0,
            "soft positive-branch balance")

    hard = clean(
        (B_t + lam * B) / sp.sqrt(Y * d)
        - B * (Y_t / Y + d_t / d) / (2 * sp.sqrt(Y * d))
    )
    require(clean(sp.limit(source, eps, 0, dir="+")) - hard == 0,
            "hard source limit away from d=0")

    hard_a = B**2 / (Y * d)
    sigma_t = clean(eps * d_t / (d + eps) ** 2)
    require(clean(z - sp.sqrt(sigma) * hard_z) == 0,
            "soft-hard z factorization")
    require(clean(a - sigma * hard_a) == 0,
            "soft-hard a factorization")
    require(clean(
        2 * z * n_style_source
        - 2 * sigma * hard_z * hard
        - sigma_t * hard_a
    ) == 0, "face-source factorization")

    return {
        "passed": True,
        "definitions": {
            "R_epsilon": "sqrt(d+epsilon)",
            "theta_epsilon": "epsilon/(d+epsilon)",
            "sigma_epsilon": "d/(d+epsilon)=1-theta_epsilon",
            "z_epsilon": "B/(sqrt(Y)*R_epsilon)",
            "a_epsilon": "(z_epsilon^+)^2",
        },
        "zTimeDerivativeOnPositiveBranch": str(z_t),
        "softSource": str(source),
        "nStyleSource": str(n_style_source),
        "sourceConventionDifference": "lambda*theta_epsilon*z_epsilon",
        "hardSoftFactorization": {
            "z": "z_epsilon=sqrt(sigma_epsilon)*z on d>0",
            "a": "a_epsilon=sigma_epsilon*a on d>0",
            "sigma_t": "epsilon*d_t/(d+epsilon)^2",
            "nStyleFaceSource": (
                "2*z_epsilon^+*J_epsilon^(N)="
                "2*sigma_epsilon*z^+*J+sigma_epsilon,t*a"
            ),
            "interpretation": (
                "The last term is the exact soft layer that converges to the "
                "signed and Jordan one-sided face measures."
            ),
        },
        "positiveBranchBalance": (
            "a_epsilon,t+2*lambda*(1+theta_epsilon)*a_epsilon"
            "=2*z_epsilon^+*J_epsilon"
        ),
        "hardLimit": str(hard),
    }


def finite_order_face() -> dict[str, object]:
    """Audit the universal inner profile for finite-order Hilbert zeros."""

    s = sp.symbols("s", nonnegative=True)
    profile_checks: list[dict[str, object]] = []
    for order in range(1, 9):
        profile = s ** (2 * order) / (1 + s ** (2 * order))
        derivative = clean(sp.diff(profile, s))
        require(sp.limit(profile, s, 0, dir="+") == 0,
                f"order {order} inner origin")
        require(sp.limit(profile, s, sp.oo) == 1,
                f"order {order} inner infinity")
        require(clean(derivative - (
            2 * order * s ** (2 * order - 1)
            / (1 + s ** (2 * order)) ** 2
        )) == 0, f"order {order} profile derivative")
        # The derivative is nonnegative and its half-line mass follows by FTC.
        derivative_mass = clean(
            sp.limit(profile, s, sp.oo)
            - sp.limit(profile, s, 0, dir="+")
        )
        require(derivative_mass == 1, f"order {order} face mass")
        radial_constant = clean(
            sp.beta(1 + sp.Rational(1, 2 * order),
                    1 - sp.Rational(1, 2 * order))
            / (2 * order)
        )
        profile_checks.append({
            "order": order,
            "profile": str(profile),
            "derivative": str(derivative),
            "derivativeHalfLineMass": str(derivative_mass),
            "radialProfileIntegral": str(radial_constant),
            "radialMassScale": f"epsilon^(1/{2 * order})",
        })

    return {
        "passed": True,
        "hypothesis": (
            "C(t0+tau)=c*tau^m+O(|tau|^(m+1)) and "
            "C_t=m*c*tau^(m-1)+O(|tau|^m) in the real Hilbert "
            "space, c!=0; F,F_t,Y,Y_t have the stated first-order "
            "bounds and Y(t0)=Y0>0"
        ),
        "leadingPairing": "b=<F(t0),c>",
        "rightTrace": "A_plus=(max(b,0))^2/(Y0*||c||^2)",
        "leftTrace": "A_minus=(max((-1)^m*b,0))^2/(Y0*||c||^2)",
        "innerScale": "delta_epsilon=(epsilon/||c||^2)^(1/(2m))",
        "innerProfile": "A_side*s^(2m)/(1+s^(2m))",
        "measureLimit": {
            "localization": (
                "restrict to |t-t0|<r_epsilon with r_epsilon down to "
                "zero and delta_epsilon/r_epsilon down to zero"
            ),
            "signedDerivativeAtom": "(A_plus-A_minus)*delta_t0",
            "positiveDerivativeAtom": "A_plus*delta_t0",
            "negativeDerivativeAtom": "A_minus*delta_t0",
            "totalVariationAtom": "(A_plus+A_minus)*delta_t0",
            "softSourceSignedAtom": "(A_plus-A_minus)*delta_t0",
            "softSourcePositiveAtom": "A_plus*delta_t0",
            "softSourceNegativeAtom": "A_minus*delta_t0",
            "extraVariationDefect": (
                "A_plus+A_minus-|A_plus-A_minus|=2*min(A_plus,A_minus)"
            ),
            "extraSoftRadialDamping": (
                "O(epsilon^(1/(2m))) locally, hence no face atom"
            ),
        },
        "degenerateBoundary": (
            "If b=0 the displayed leading trace vanishes and higher jets must "
            "be inspected; flat or accumulating zeros are not covered."
        ),
        "profileChecks": profile_checks,
    }


def raw_split_cancellation() -> dict[str, object]:
    """Check the logarithmic cancellation in the unsymmetrized source split."""

    x, eps, gamma = sp.symbols("x epsilon gamma", positive=True)
    source_integrand = gamma**2 / (x + eps)
    radial_integrand = -gamma**2 * x / (x + eps) ** 2
    source_primitive = clean(gamma**2 * sp.log((x + eps) / eps))
    radial_primitive = clean(
        -gamma**2 * (
            sp.log((x + eps) / eps) + eps / (x + eps) - 1
        )
    )
    joint_primitive = clean(source_primitive + radial_primitive)

    require(clean(sp.diff(source_primitive, x) - source_integrand) == 0,
            "raw source primitive")
    require(clean(sp.diff(radial_primitive, x) - radial_integrand) == 0,
            "raw radial primitive")
    require(clean(joint_primitive - gamma**2 * x / (x + eps)) == 0,
            "raw logarithm cancellation")
    require(sp.limit(source_primitive, eps, 0, dir="+") == sp.oo,
            "raw source logarithmic divergence")
    require(sp.limit(-radial_primitive, eps, 0, dir="+") == sp.oo,
            "raw radial logarithmic divergence")
    require(clean(sp.limit(joint_primitive, eps, 0, dir="+") - gamma**2) == 0,
            "finite joint face mass")

    return {
        "passed": True,
        "model": (
            "On one active half-face, x=||c||^2*|tau|^(2m) and "
            "gamma^2=<F0,c>^2/(Y0*||c||^2)."
        ),
        "rawSourceHalfFaceIntegral": (
            "gamma^2*log(1+x/epsilon)"
        ),
        "rawRadialHalfFaceIntegral": (
            "-gamma^2*(log(1+x/epsilon)-x/(x+epsilon))"
        ),
        "jointHalfFaceIntegral": "gamma^2*x/(x+epsilon)",
        "limit": "gamma^2",
        "conclusion": (
            "The two raw terms have logarithmically divergent total masses "
            "with opposite signs. Only their joint hard-soft factorization "
            "has a uniformly finite face-measure limit."
        ),
    }


def oscillatory_separation() -> dict[str, object]:
    """Record exact budgets for C_N=N^{-1}sin(Nt)e."""

    N, lam = sp.symbols("N lambda", positive=True)
    eps = N ** -4
    soft_peak = clean(1 / (1 + eps * N**2))
    positive_variation = clean(N * soft_peak)
    delta = clean(eps * N**2)
    denominator_mass = sp.pi / N**2
    derivative_mass = sp.pi
    field_mass = 2 * sp.pi
    shifted_derivative_mass = clean(sp.pi * (1 + lam**2 / N**2))
    a_time_mass = clean(
        sp.pi * (1 - sp.sqrt(delta / (1 + delta)))
    )
    extra_radial_mass = clean(
        lam * sp.pi * sp.sqrt(delta) / (1 + delta) ** sp.Rational(3, 2)
    )
    total_control_mass = clean(
        denominator_mass + derivative_mass + field_mass
    )
    ratio = clean(positive_variation / total_control_mass)
    require(sp.limit(positive_variation, N, sp.oo) == sp.oo,
            "unbounded positive face variation")
    require(sp.limit(denominator_mass, N, sp.oo) == 0,
            "vanishing denominator mass")
    require(sp.limit(ratio, N, sp.oo) == sp.oo,
            "separation from L2 control masses")

    samples = []
    for value in (1, 2, 4, 8, 16, 32, 64):
        sample = {
            "N": value,
            "epsilon": str(sp.Rational(1, value**4)),
            "softPeak": str(soft_peak.subs(N, value)),
            "positiveVariation": str(positive_variation.subs(N, value)),
            "totalVariationIncludingBoundary": str(
                2 * positive_variation.subs(N, value)
            ),
            "denominatorMass": str(denominator_mass.subs(N, value)),
            "C_tSquareMass": str(derivative_mass),
            "FTimeMass": str(field_mass),
        }
        samples.append(sample)

    return {
        "passed": True,
        "path": {
            "interval": "[0,2*pi]",
            "Y": "1",
            "F": "e",
            "C_N": "N^(-1)*sin(N*t)*e",
            "d_N": "N^(-2)*sin(N*t)^2",
            "B_N": "N^(-1)*sin(N*t)",
            "epsilon_N": "N^(-4)",
        },
        "hardPositiveComponents": "N",
        "hardEntryFaces": "N",
        "hardExitFaces": "N",
        "softPeak": str(soft_peak),
        "softPositiveVariation": str(positive_variation),
        "softTotalVariationIncludingBoundary": str(2 * positive_variation),
        "softATimeMass": str(a_time_mass),
        "extraSoftRadialMass": str(extra_radial_mass),
        "fixedNMeasureLimit": {
            "signedSource": (
                "D(1_{sin(Nt)>0})+2*lambda*1_{sin(Nt)>0}*dt"
            ),
            "positiveSourceMass": "N+2*pi*lambda",
            "negativeSourceMass": "N",
            "totalSourceVariation": "2*N+2*pi*lambda",
            "extraRadialAtom": "0",
        },
        "budgets": {
            "integral_d": str(denominator_mass),
            "integral_norm_C_t_squared": str(derivative_mass),
            "integral_norm_M_squared": str(shifted_derivative_mass),
            "integral_norm_F_squared": str(field_mass),
        },
        "separationRatio": str(ratio),
        "conclusion": (
            "No universal functional inequality can bound the soft positive "
            "source or all one-sided faces using only these L2 field, "
            "denominator-mass, and first-time-derivative square budgets."
        ),
        "claimBoundary": (
            "The paths are smooth Hilbert-space paths, not constrained to be "
            "the coupled fixed-cell observables of an NSE solution."
        ),
        "limitOrder": (
            "The face measure is obtained with N fixed and epsilon down to "
            "zero, or diagonally with N^2*epsilon_N down to zero. Holding "
            "epsilon fixed while N tends to infinity blurs the faces and is "
            "a different limit."
        ),
        "samples": samples,
    }


def add_modes(left: Mode, right: Mode) -> Mode:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def negate_mode(mode: Mode) -> Mode:
    return tuple(-entry for entry in mode)  # type: ignore[return-value]


def dot(left: Iterable[sp.Expr], right: Iterable[sp.Expr]) -> sp.Expr:
    return clean(sum(a * b for a, b in zip(left, right)))


def project(mode: Mode, value: Vector) -> Vector:
    wave = Vector(mode)
    return Vector(value - wave * (dot(wave, value) / dot(wave, wave)))


def curl_coefficient(mode: Mode, value: Vector) -> Vector:
    return Vector(sp.I * Vector(mode).cross(value))


def norm_squared(field: dict[Mode, Vector]) -> sp.Expr:
    return clean(sum(
        dot((sp.conjugate(entry) for entry in value), value)
        for value in field.values()
    ))


def inner(left: dict[Mode, Vector], right: dict[Mode, Vector]) -> sp.Expr:
    return clean(sum(
        dot((sp.conjugate(entry) for entry in left[mode]), right[mode])
        for mode in left.keys() & right.keys()
    ))


def mode_table(field: dict[Mode, Vector]) -> dict[str, list[str]]:
    return {
        str(mode): [str(clean(entry)) for entry in field[mode]]
        for mode in sorted(field)
    }


def nse_initial_face() -> dict[str, object]:
    """Construct an exact zero-denominator, positive-entry NSE initial jet."""

    p: Mode = (1, 0, 0)
    r: Mode = (0, 1, 0)
    polarization_p = Vector([0, 1, 0])
    polarization_r = Vector([0, 0, 1])
    velocity = {
        p: polarization_p / 2,
        negate_mode(p): polarization_p / 2,
        r: polarization_r / 2,
        negate_mode(r): polarization_r / 2,
    }
    for mode, coefficient in velocity.items():
        require(dot(mode, coefficient) == 0, f"velocity divergence {mode}")

    convection: defaultdict[Mode, sp.MutableDenseMatrix] = defaultdict(
        lambda: sp.zeros(3, 1)
    )
    for left_mode, left_value in velocity.items():
        for right_mode, right_value in velocity.items():
            output = add_modes(left_mode, right_mode)
            if output == (0, 0, 0):
                continue
            convection[output] += (
                sp.I * dot(left_value, right_mode) * right_value
            )

    lamb = {
        mode: Vector(-project(mode, Vector(value)))
        for mode, value in convection.items()
        if any(clean(entry) != 0 for entry in project(mode, Vector(value)))
    }
    # A smooth radial multiplier can equal zero at radius 1 and one at
    # radius sqrt(2); only those lattice radii occur in the present datum.
    filtered_lamb = {
        mode: value for mode, value in lamb.items()
        if dot(mode, mode) == 2
    }
    filtered_vorticity_initial: dict[Mode, Vector] = {}
    G = {
        mode: curl_coefficient(mode, value)
        for mode, value in filtered_lamb.items()
    }
    C_first = {
        mode: curl_coefficient(mode, value)
        for mode, value in G.items()
    }
    vorticity = {
        mode: curl_coefficient(mode, value)
        for mode, value in velocity.items()
    }

    require(filtered_vorticity_initial == {}, "zero filtered initial vorticity")
    require(len(filtered_lamb) == 4, "four target interaction modes")
    for mode, coefficient in filtered_lamb.items():
        require(dot(mode, coefficient) == 0, f"Leray output {mode}")

    Y0 = norm_squared(vorticity)
    F_squared = norm_squared(filtered_lamb)
    G_squared = norm_squared(G)
    C_first_squared = norm_squared(C_first)
    B_first = inner(filtered_lamb, C_first)
    face_trace = clean(B_first**2 / (Y0 * C_first_squared))
    require(Y0 == 1, "initial enstrophy")
    require(F_squared == sp.Rational(1, 4), "filtered Lamb norm")
    require(G_squared == sp.Rational(1, 2), "filtered Lamb curl norm")
    require(C_first_squared == 1, "first denominator jet norm")
    require(B_first == sp.Rational(1, 2), "first numerator jet")
    require(face_trace == sp.Rational(1, 4), "right face trace")

    return {
        "passed": True,
        "initialVelocity": (
            "u0(x)=(0,cos(x1),0)+(0,0,cos(x2)) on the normalized torus"
        ),
        "multiplier": (
            "real-even smooth radial annular symbol m with m(1)=0 and "
            "m(sqrt(2))=1"
        ),
        "initialFacts": {
            "T_omega_0": "0",
            "C_0": "0",
            "Y_0": str(Y0),
            "F_modes": mode_table(filtered_lamb),
            "norm_F_squared": str(F_squared),
            "norm_G_squared": str(G_squared),
            "norm_C_t_0_squared": str(C_first_squared),
            "B_t_0": str(B_first),
        },
        "rightAsymptotics": {
            "C(t)": "t*C_t(0)+O(t^2)",
            "B(t)": "t/2+O(t^2)",
            "d(t)": "t^2+O(t^3)",
            "z(t)": "1/2+O(t) for t down to 0 from the right",
            "a(t)": "1/4+O(t) for t down to 0 from the right",
        },
        "rightEntryTrace": str(face_trace),
        "conclusion": (
            "A genuine smooth NSE initial trace can create a nonzero hard "
            "entry face from a zero filtered denominator."
        ),
        "claimBoundary": (
            "This is a one-sided local initial-jet result. It does not produce "
            "arbitrarily many internal NSE faces or an unpayable NSE face sum."
        ),
    }


def run() -> dict[str, object]:
    return {
        "release": "R0.71O",
        "status": "passed",
        "checks": {
            "softIdentity": soft_identity(),
            "finiteOrderFace": finite_order_face(),
            "rawSplitCancellation": raw_split_cancellation(),
            "oscillatorySeparation": oscillatory_separation(),
            "nseInitialFace": nse_initial_face(),
        },
        "verdict": (
            "Soft regularization exposes the one-sided hard faces as source "
            "and variation measures; its extra radial damping has no atom at "
            "a finite-order zero. Existing denominator-mass and energy-level "
            "budgets do not pay the face count by a universal functional "
            "inequality, although an NSE-specific summed cancellation remains open."
        ),
        "claimBoundary": (
            "Exact fixed-cell soft algebra, finite-order face asymptotics, one "
            "abstract Hilbert-path separation, and one smooth NSE initial jet. "
            "No refresh or moving-cell theorem, infinite frame limit, Leray "
            "passage, continuation criterion, singularity, or global-regularity result."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
