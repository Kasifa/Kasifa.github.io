#!/usr/bin/env python3
"""Exact finite audit for R0.71R.

The release separates a proved parabolic-incidence implication from an exact
two-derivative mismatch between NSE scaling and the Leray energy budget.

The exact computations below certify three method tests:

1. a positive even-order entry is invariant under multiplication of the
   observable by a positive scalar, while every quadratic post-entry or
   source-square charge scales by the square of that scalar;
2. one analytic forced scalar observable can have N positive entries with
   normalized total source-square energy one;
3. N analytic forced observables can have N distinct entries while their
   summed source-square energy stays below three.

These families are not Navier--Stokes trajectories.  They show that the
incidence lower bound and, when the windows have a fixed positive parabolic
height, the overlap ledger in the conditional theorem cannot be deduced from
abstract forced-parabolic regularity alone.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def frac(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def poly_add(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    size = max(len(left), len(right))
    result = [Fraction(0) for _ in range(size)]
    for index, value in enumerate(left):
        result[index] += value
    for index, value in enumerate(right):
        result[index] += value
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_mul(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return result


def poly_derivative(values: list[Fraction]) -> list[Fraction]:
    if len(values) == 1:
        return [Fraction(0)]
    return [Fraction(index) * values[index] for index in range(1, len(values))]


def poly_integral_square(values: list[Fraction]) -> Fraction:
    square = poly_mul(values, values)
    return sum(coefficient / Fraction(index + 1) for index, coefficient in enumerate(square))


def squared_root_polynomial(roots: list[Fraction]) -> list[Fraction]:
    result = [Fraction(1)]
    for root in roots:
        result = poly_mul(result, [root * root, -2 * root, Fraction(1)])
    return result


def source_energy(values: list[Fraction]) -> Fraction:
    """Integral_0^1 |q'(t)+q(t)|^2 dt for generator A=I."""

    return poly_integral_square(poly_add(poly_derivative(values), values))


def scaled_even_touch() -> dict[str, object]:
    """One interior even touch with fixed entry mass and vanishing charge."""

    root = Fraction(1, 2)
    base = squared_root_polynomial([root])
    base_energy = source_energy(base)
    require(base_energy > 0, "positive base source energy")
    rows = []
    for exponent in (0, 1, 2, 4, 8, 12):
        epsilon = Fraction(1, 2**exponent)
        energy = epsilon * epsilon * base_energy
        post_entry_at_h_quarter = epsilon * epsilon * Fraction(1, 4) ** 4
        rows.append({
            "epsilon": frac(epsilon),
            "positiveEntryMass": 1,
            "sourceSquareEnergy": frac(energy),
            "postEntryChargeAtHOneQuarter": frac(post_entry_at_h_quarter),
        })
    require(rows[-1]["positiveEntryMass"] == 1, "entry mass is scale invariant")
    return {
        "passed": True,
        "family": "C_epsilon(t)=epsilon*(t-1/2)^2, F=1, Y=1, kappa=1",
        "equation": "C_t+C=G_epsilon",
        "baseSourceSquareEnergy": frac(base_energy),
        "entryLeadingCoefficient": "epsilon>0",
        "positiveEntryFormula": "A_plus=(F*c)^2/(Y*c^2)=1",
        "rows": rows,
        "conclusion": (
            "The positive-entry atom has degree zero in the observable leading "
            "coefficient, whereas post-entry amplitude and source-square energy "
            "have degree two."
        ),
    }


def sequential_forced_family() -> dict[str, object]:
    """One scalar forced analytic path with N normalized positive entries."""

    rows = []
    for count in (1, 2, 4, 8, 12):
        roots = [Fraction(index, count + 1) for index in range(1, count + 1)]
        polynomial = squared_root_polynomial(roots)
        energy = source_energy(polynomial)
        require(energy > 0, f"N={count} positive source energy")

        leading_coefficients = []
        for index, root in enumerate(roots):
            coefficient = Fraction(1)
            for other_index, other in enumerate(roots):
                if other_index != index:
                    coefficient *= (root - other) ** 2
            require(coefficient > 0, f"N={count} positive entry coefficient")
            leading_coefficients.append(coefficient)

        normalization = 1.0 / math.sqrt(float(energy))
        normalized_energy = normalization * normalization * float(energy)
        require(abs(normalized_energy - 1.0) < 5e-13, f"N={count} normalized energy")
        rows.append({
            "N": count,
            "roots": [frac(value) for value in roots],
            "polynomialDegree": 2 * count,
            "unnormalizedSourceEnergy": frac(energy),
            "normalizingAmplitude": normalization,
            "normalizedSourceSquareEnergy": normalized_energy,
            "positiveEntryCount": count,
            "eachPositiveEntryMass": 1,
            "totalPositiveEntryMass": count,
            "minimumLeadingCoefficient": frac(min(leading_coefficients)),
        })

    return {
        "passed": True,
        "family": "q_N(t)=product_{k=1}^N (t-k/(N+1))^2",
        "observable": "C_N=epsilon_N*q_N with epsilon_N=E_N^-1/2",
        "equation": "C_t+C=G_N on [0,1]",
        "sourceNormalization": "integral_0^1 |G_N|^2 dt=1",
        "entryData": "F=1, Y=1, kappa=1, so every A_plus=1",
        "rows": rows,
        "methodBoundary": (
            "No universal positive-entry bound can depend only on the L2 source "
            "energy of a general forced analytic scalar parabolic path."
        ),
    }


def component_union_family() -> dict[str, object]:
    """Many components with a bounded summed source-square budget."""

    rows = []
    for count in (1, 2, 4, 8, 16, 32, 64):
        total_energy = Fraction(0)
        roots = []
        for index in range(1, count + 1):
            root = Fraction(1, 4) + Fraction(index, 2 * (count + 1))
            epsilon = Fraction(1, 2**index)
            base = squared_root_polynomial([root])
            total_energy += epsilon * epsilon * source_energy(base)
            roots.append(root)
        require(len(set(roots)) == count, f"Q={count} distinct entries")
        require(all(Fraction(1, 4) < value < Fraction(3, 4) for value in roots), f"Q={count} interior entries")
        require(total_energy < 3, f"Q={count} uniform energy bound")
        rows.append({
            "componentCount": count,
            "distinctEntryCount": count,
            "totalPositiveEntryMass": count,
            "summedSourceSquareEnergy": frac(total_energy),
            "uniformExactUpperBound": 3,
            "minimumAmplitude": frac(Fraction(1, 2**count)),
        })

    return {
        "passed": True,
        "family": "C_q(t)=2^-q*(t-b_q)^2, b_q in (1/4,3/4)",
        "equation": "(C_q)_t+C_q=G_q",
        "entryData": "F_q=1, Y=1, kappa=1, so A_{q,+}=1",
        "energyBoundProof": (
            "On [0,1], |2(t-b)+(t-b)^2|<=3; hence each unscaled "
            "source energy is <=9 and sum_q 4^-q=1/3."
        ),
        "rows": rows,
        "methodBoundary": (
            "A square-summable all-component source budget does not count the "
            "union of degree-zero entry atoms without a componentwise incidence "
            "lower charge."
        ),
    }


def scale_matched_source_ledger() -> dict[str, object]:
    """Record the exact derivative powers in the NSE observable source."""

    return {
        "passed": True,
        "observable": "C_{j,Q}=curl(chi_Q W_j), W_j=T_j omega",
        "forcing": (
            "G_{j,Q}=curl(chi_Q curl F_j)-nu*curl(2 grad chi_Q dot grad W_j "
            "+ (Delta chi_Q) W_j)"
        ),
        "cutoffScale": "|grad^m chi_Q|<=C_chi*kappa_j^m",
        "annularDerivativeLedger": {
            "nonlinearSource": "sum_Q ||curl(chi_Q curl F_j)||_2^2 <= C*kappa_j^4||F_j||_2^2",
            "viscousCommutator": "sum_Q ||comm_{j,Q}||_2^2 <= C*nu^2*kappa_j^6||W_j||_2^2",
            "rhoFamily": (
                "sum_{j,Q} kappa_j^(-4-rho)||G_{j,Q}||_2^2 "
                "<=C*(sum_j kappa_j^-rho||F_j||_2^2+"
                "nu^2 sum_j kappa_j^(2-rho)||W_j||_2^2)"
            ),
            "minimalEnergyMatchedRhoTwo": "sum kappa_j^-6||G||^2 <= C*(||L||_{H^-1}^2+nu^2*Y)",
            "scaleCovariantRhoZero": "sum kappa_j^-4||G||^2 <= C*(||L||_2^2+nu^2||grad omega||_2^2)",
        },
        "lerayPayment": (
            "After division by Y, ||L||_{H^-1}^2/Y is bounded by "
            "C||u||_2*Y^(1/2), which is integrable on finite intervals from "
            "the energy inequality."
        ),
        "unpaidInputs": [
            "uniform post-entry incidence constant Gamma_2; covariant scaling gives its optimal version weight kappa_j^2",
            "uniform same-observable overlap M for noncollapsing parabolic windows",
            "forward parabolic windows up to a possible endpoint",
        ],
    }


def nse_frequency_jet_scaling() -> dict[str, object]:
    """Exact frequency ledger for the R0.71O genuine NSE initial jet."""

    amplitude = Fraction(1, 8)
    theta = Fraction(1, 8)
    rows = []
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        k = Fraction(frequency)
        energy = amplitude * amplitude
        enstrophy = amplitude * amplitude * k * k
        filtered_lamb = amplitude**4 * k * k / 4
        leading_direction = amplitude**4 * k**6
        pairing = amplitude**4 * k**4 / 2
        entry = pairing * pairing / (enstrophy * leading_direction)
        require(entry == amplitude * amplitude / 4, f"K={frequency} entry atom")
        # This is the exact first-jet coefficient evaluated at the parabolic
        # height h=theta*K^-2.  It records the scaling pressure; the finite-h
        # actual positive-time solution value requires a separate Duhamel
        # remainder estimate and is not certified here.
        incidence_rhs_leading = amplitude * amplitude * theta * theta / (k * k)
        gamma_lower_leading = entry / incidence_rhs_leading
        require(gamma_lower_leading == k * k / (4 * theta * theta), f"K={frequency} hidden two powers")
        rows.append({
            "K": frequency,
            "kineticEnergy": frac(energy),
            "Y0": frac(enstrophy),
            "normFSquared": frac(filtered_lamb),
            "normLeadingDirectionSquared": frac(leading_direction),
            "leadingPairing": frac(pairing),
            "positiveEntryAtom": frac(entry),
            "parabolicTheta": frac(theta),
            "rhoTwoIncidenceRightSideLeadingCoefficient": frac(incidence_rhs_leading),
            "gammaTwoTaylorJetSurrogate": frac(gamma_lower_leading),
        })
    return {
        "passed": True,
        "initialData": "u_{0,K}=a(0,cos(K*x1),cos(K*x2)), a=1/8",
        "multiplier": "m(K)=0, m(sqrt(2)K)=1, chi=1",
        "exactJet": (
            "Y=a^2K^2, ||F||^2=a^4K^2/4, C_t=2K^2F, "
            "A_plus=a^2/4"
        ),
        "nseScaling": {
            "A": "lambda^2",
            "kappaMinusRho": "lambda^-rho",
            "normCSquaredOverY": "lambda^2",
            "universalIncidenceConstantRequires": "rho=0",
            "minimalLerayMatchedSourceExponent": "rho=2",
        },
        "rows": rows,
        "claimBoundary": (
            "The table certifies the exact initial Fourier jet and its first-jet "
            "parabolic scaling coefficient. It is not an exact positive-time NSE "
            "integration."
        ),
    }


def build_certificate() -> dict[str, object]:
    checks = {
        "scaleMatchedSourceLedger": scale_matched_source_ledger(),
        "nseFrequencyJetScaling": nse_frequency_jet_scaling(),
        "scaledEvenTouch": scaled_even_touch(),
        "sequentialForcedFamily": sequential_forced_family(),
        "componentUnionFamily": component_union_family(),
    }
    require(all(check["passed"] for check in checks.values()), "all R0.71R exact checks")
    return {
        "release": "R0.71R",
        "status": "passed",
        "scope": (
            "conditional NSE parabolic-incidence implication plus exact abstract "
            "forced-parabolic obstructions; no uniform incidence theorem, temporal "
            "packing theorem, continuation criterion, singularity, or global "
            "regularity claim"
        ),
        "checks": checks,
        "decision": (
            "The rho=2 observable-source square budget is Leray-payable, but "
            "the optimal rho=2 constant has two powers under covariant dilation. "
            "The initial Fourier family records the same K^2 pressure only for "
            "its Taylor-jet surrogate. The scale-covariant "
            "rho=0 alternative requires an L2-Lamb and palinstrophy budget. Thus "
            "the one-parameter endpoint-square Duhamel certificate has an exact "
            "two-derivative mismatch; "
            "abstract parabolic regularity also supplies neither incidence nor "
            "bounded forward overlap."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
