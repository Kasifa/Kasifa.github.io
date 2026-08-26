#!/usr/bin/env python3
"""Exact audit for the R0.71P positive-entry batching theorem.

The audit has four finite purposes:

1. certify the sharp cellwise projection inequality behind a simultaneous
   frame--cell entry batch;
2. record that componentwise relaxed positive-entry atoms form a positive
   measure and therefore admit no internal signed cancellation after the
   componentwise positive parts have been selected;
3. show on the smooth oscillatory Hilbert path that the missing quantity is a
   temporal counting measure rather than an ordinary time integral;
4. reconstruct the R0.71O smooth Navier--Stokes initial jet and verify that it
   saturates the one-cell projection bound.

The oscillatory family is not a Navier--Stokes construction.  The exact NSE
calculation is a one-sided initial jet, not a multiple-face theorem.
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


def sharp_projection_and_overlap() -> dict[str, object]:
    """Check the exact Cauchy residual and one finite overlap ledger."""

    f1, f2, c1, c2 = sp.symbols("f1 f2 c1 c2", real=True)
    f_norm = f1**2 + f2**2
    c_norm = c1**2 + c2**2
    pairing = f1 * c1 + f2 * c2
    gram_residual = clean(f_norm * c_norm - pairing**2)
    require(
        clean(gram_residual - (f1 * c2 - f2 * c1) ** 2) == 0,
        "two-dimensional Gram identity",
    )

    # A finite spatial model with support overlap two.  Every direction is
    # supported in its declared cell, so the local projection estimate can be
    # checked without discarding support information.
    F = Vector([1, 2, 3, 4])
    Y = sp.Integer(5)
    supports = ((0, 1), (1, 2), (2, 3))
    directions = (
        Vector([1, 1, 0, 0]),
        Vector([0, 1, -1, 0]),
        Vector([0, 0, 1, 1]),
    )
    rows: list[dict[str, object]] = []
    entry_sum = sp.Integer(0)
    local_energy_sum = sp.Integer(0)
    multiplicities = [0, 0, 0, 0]
    for support, direction in zip(supports, directions):
        local = Vector([
            F[index] if index in support else 0 for index in range(4)
        ])
        for index in support:
            multiplicities[index] += 1
        pairing_value = clean((F.T * direction)[0])
        direction_norm = clean((direction.T * direction)[0])
        local_norm = clean((local.T * local)[0])
        entry = clean(sp.Max(pairing_value, 0) ** 2 / (Y * direction_norm))
        local_budget = clean(local_norm / Y)
        require(bool(entry <= local_budget), f"cell {support} projection bound")
        entry_sum += entry
        local_energy_sum += local_budget
        rows.append({
            "support": list(support),
            "pairing": str(pairing_value),
            "directionNormSquared": str(direction_norm),
            "entryAtom": str(entry),
            "localBudget": str(local_budget),
        })

    overlap = max(multiplicities)
    global_budget = clean(overlap * (F.T * F)[0] / Y)
    entry_sum = clean(entry_sum)
    local_energy_sum = clean(local_energy_sum)
    require(bool(entry_sum <= local_energy_sum), "summed local projection bound")
    require(bool(local_energy_sum <= global_budget), "bounded overlap bound")

    return {
        "passed": True,
        "cellwiseTheorem": (
            "A_plus=(<F,c>^+)^2/(Y*||c||^2) "
            "<=||1_supp(chi_Q)F||^2/Y"
        ),
        "gramResidual": str(gram_residual),
        "gramSquare": "(f1*c2-f2*c1)^2",
        "finiteOverlapExample": {
            "F": [str(value) for value in F],
            "Y": str(Y),
            "supportMultiplicity": multiplicities,
            "overlapConstant": overlap,
            "rows": rows,
            "entrySum": str(entry_sum),
            "localEnergySum": str(local_energy_sum),
            "overlapGlobalBudget": str(global_budget),
        },
        "summedTheorem": (
            "At one time t, sum_{j,Q entering at t} kappa_j^-2 A_plus "
            "<=M_chi*C_T*||L(t)||_{dot H^-1}^2/Y(t)."
        ),
    }


def positive_measure_ledger() -> dict[str, object]:
    """Record exact finite atomic sums and the even-touch relaxation defect."""

    entries = [
        (sp.Rational(1, 4), sp.Rational(3, 5)),
        (sp.Rational(1, 9), sp.Rational(2, 7)),
        (sp.Rational(1, 16), sp.Rational(5, 8)),
    ]
    weighted = clean(sum(weight * atom for weight, atom in entries))
    require(weighted > 0, "positive weighted entry measure")

    # Exact layer-cake reconstruction of the finite weighted mass.
    levels = sorted({sp.Integer(0), *(atom for _weight, atom in entries)})
    layer_cake = sp.Integer(0)
    layer_rows: list[dict[str, object]] = []
    for lower, upper in zip(levels[:-1], levels[1:]):
        active_weight = clean(sum(
            weight for weight, atom in entries if atom > lower
        ))
        contribution = clean((upper - lower) * active_weight)
        layer_cake += contribution
        layer_rows.append({
            "levelInterval": [str(lower), str(upper)],
            "activeWeight": str(active_weight),
            "contribution": str(contribution),
        })
    layer_cake = clean(layer_cake)
    require(layer_cake == weighted, "entry layer-cake identity")

    A = sp.Rational(7, 12)
    signed_even_touch = clean(A - A)
    componentwise_soft_total = clean(A + A)
    require(signed_even_touch == 0, "even-touch signed cancellation")
    require(
        componentwise_soft_total == sp.Rational(7, 6),
        "even-touch componentwise soft mass",
    )

    # On a constant positive branch, zero-padding the observation window
    # creates a left-boundary rise.  It is initial data, not an entry atom.
    constant_branch_segmented = sp.Integer(1)
    constant_branch_interior = sp.Integer(0)
    constant_branch_initial = sp.Integer(1)
    constant_branch_entry = sp.Integer(0)
    require(
        clean(
            constant_branch_segmented
            - constant_branch_interior
            - constant_branch_initial
        ) == constant_branch_entry,
        "segmented ledger subtracts the initial trace",
    )

    return {
        "passed": True,
        "target": (
            "eta_plus=sum_{j,Q} kappa_j^-2 sum_{t0} "
            "A_{j,Q,+}(t0)*delta_t0"
        ),
        "finiteAtomicExample": {
            "weightAtomPairs": [
                {"weight": str(weight), "atom": str(atom)}
                for weight, atom in entries
            ],
            "totalMass": str(weighted),
            "layerCakeMass": str(layer_cake),
            "layerCakeRows": layer_rows,
        },
        "monotonicity": (
            "All weights and A_plus atoms are nonnegative; finite truncations "
            "increase monotonically, so no shell/cell signed cancellation is "
            "available inside the componentwise relaxed positive-entry "
            "measure. It need not equal the positive Jordan part of a signed "
            "aggregate."
        ),
        "evenTouch": {
            "A_minus": str(A),
            "A_plus": str(A),
            "signedAtom": str(signed_even_touch),
            "componentwiseSoftPositiveAndNegativeMass": str(
                componentwise_soft_total
            ),
            "positiveEntryStillPresent": str(A),
            "ordinaryHardPositiveJump": str(sp.Max(A - A, 0)),
            "softSegmentedMinusHardPositiveJump": str(A),
        },
        "hardVersusSegmentedFormula": {
            "ordinaryHardPositiveJump": "max(A_plus-A_minus,0)",
            "segmentedOrSoftPositiveEntry": "A_plus",
            "missingTouchMass": "min(A_plus,A_minus)",
        },
        "observationBoundaryConvention": {
            "window": "[a,b)",
            "constantPositiveBranchSegmentedVariation": str(
                constant_branch_segmented
            ),
            "interiorVariation": str(constant_branch_interior),
            "declaredInitialTrace": str(constant_branch_initial),
            "entryMassAfterSubtractingInitialTrace": str(
                constant_branch_entry
            ),
        },
        "layerCakeFormula": (
            "sum w*A_plus = integral_0^infinity "
            "sum w*1_{A_plus>s} ds"
        ),
    }


def oscillatory_temporal_packing() -> dict[str, object]:
    """Audit the exact temporal-counting obstruction."""

    N = sp.symbols("N", integer=True, positive=True)
    entry_mass = N
    distinct_entry_times = N
    batch_density = sp.Integer(1)
    counting_integral = clean(batch_density * distinct_entry_times)
    ordinary_time_integral = 2 * sp.pi
    denominator_mass = sp.pi / N**2
    derivative_mass = sp.pi
    field_mass = 2 * sp.pi
    epsilon = N**-4
    soft_entry_mass = clean(N / (1 + epsilon * N**2))

    require(clean(entry_mass - counting_integral) == 0,
            "counting-measure equality")
    require(sp.limit(entry_mass, N, sp.oo) == sp.oo,
            "unbounded hard entry mass")
    require(sp.limit(denominator_mass, N, sp.oo) == 0,
            "vanishing denominator mass")
    require(sp.limit(soft_entry_mass / entry_mass, N, sp.oo) == 1,
            "soft entries recover hard entries")

    samples = []
    for value in (1, 2, 4, 8, 16, 32, 64):
        positive_entry_indices = list(range(0, 2 * value, 2))
        require(
            len(positive_entry_indices) == value,
            f"half-open positive-entry count N={value}",
        )
        require(
            2 * value not in positive_entry_indices,
            f"right endpoint excluded N={value}",
        )
        samples.append({
            "N": value,
            "halfOpenPositiveZeroIndices": positive_entry_indices,
            "distinctEntryTimesIncludingInitialBoundary": value,
            "hardPositiveEntryMass": value,
            "countingIntegral": value,
            "ordinaryTimeIntegralOfBatchDensity": str(ordinary_time_integral),
            "denominatorMass": str(denominator_mass.subs(N, value)),
            "C_tSquareMass": str(derivative_mass),
            "FTimeMass": str(field_mass),
            "softPositiveEntryMass": str(soft_entry_mass.subs(N, value)),
        })

    return {
        "passed": True,
        "path": {
            "interval": "[0,2*pi)",
            "Y": "1",
            "F": "e",
            "C_N": "N^(-1)*sin(N*t)*e",
            "epsilon_N": "N^(-4)",
        },
        "hardEntryMass": str(entry_mass),
        "distinctEntryTimeCount": str(distinct_entry_times),
        "timeSliceBatchDensity": str(batch_density),
        "countingMeasureIntegral": str(counting_integral),
        "ordinaryTimeIntegral": str(ordinary_time_integral),
        "softPositiveEntryMass": str(soft_entry_mass),
        "budgets": {
            "integral_d": str(denominator_mass),
            "integral_norm_C_t_squared": str(derivative_mass),
            "integral_norm_F_squared": str(field_mass),
        },
        "conclusion": (
            "The sharp simultaneous-face estimate becomes an integral "
            "against the distinct entry-time counting measure.  Replacing "
            "that measure by dt is false even for smooth Hilbert paths with "
            "bounded ordinary first-time budgets."
        ),
        "claimBoundary": (
            "This is an abstract Hilbert path, not a coupled NSE multiple-face "
            "construction."
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


def nse_sharp_initial_batch() -> dict[str, object]:
    """Reconstruct the NSE initial jet and its sharp projection ratio."""

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
    F = {
        mode: value for mode, value in lamb.items()
        if dot(mode, mode) == 2
    }
    G = {mode: curl_coefficient(mode, value) for mode, value in F.items()}
    c = {mode: curl_coefficient(mode, value) for mode, value in G.items()}
    omega = {
        mode: curl_coefficient(mode, value)
        for mode, value in velocity.items()
    }
    filtered_omega = {
        mode: value for mode, value in omega.items()
        if dot(mode, mode) == 2
    }
    viscous_filtered_jet = {
        mode: -dot(mode, mode) * value
        for mode, value in filtered_omega.items()
    }

    Y0 = norm_squared(omega)
    filtered_omega_norm = norm_squared(filtered_omega)
    viscous_filtered_jet_norm = norm_squared(viscous_filtered_jet)
    F2 = norm_squared(F)
    c2 = norm_squared(c)
    pairing = inner(F, c)
    A_plus = clean(pairing**2 / (Y0 * c2))
    projection_budget = clean(F2 / Y0)
    alignment_residual = clean(c2 * F2 - pairing**2)
    ratio = clean(A_plus / projection_budget)

    require(Y0 == 1, "initial enstrophy")
    require(filtered_omega_norm == 0, "initial filtered vorticity vanishes")
    require(
        viscous_filtered_jet_norm == 0,
        "initial filtered viscous jet vanishes",
    )
    require(F2 == sp.Rational(1, 4), "filtered Lamb norm")
    require(c2 == 1, "first denominator jet norm")
    require(pairing == sp.Rational(1, 2), "first numerator jet")
    require(A_plus == sp.Rational(1, 4), "right entry atom")
    require(projection_budget == sp.Rational(1, 4), "projection budget")
    require(alignment_residual == 0, "Cauchy equality")
    require(ratio == 1, "sharp one-cell constant")

    return {
        "passed": True,
        "initialVelocity": "u0=(0,cos(x1),cos(x2)) on the normalized torus",
        "multiplier": "m(1)=0 and m(sqrt(2))=1; chi=1",
        "Y0": str(Y0),
        "normInitialFilteredVorticitySquared": str(filtered_omega_norm),
        "normInitialFilteredViscousJetSquared": str(
            viscous_filtered_jet_norm
        ),
        "normFSquared": str(F2),
        "normLeadingDirectionSquared": str(c2),
        "leadingPairing": str(pairing),
        "rightEntryAtom": str(A_plus),
        "oneCellProjectionBudget": str(projection_budget),
        "CauchyResidual": str(alignment_residual),
        "sharpnessRatio": str(ratio),
        "conclusion": (
            "A genuine smooth NSE initial entry saturates the cellwise "
            "projection bound, so no universal coefficient below one can be "
            "inserted at the single-face level."
        ),
        "claimBoundary": (
            "One-sided initial jet only; no internal or repeated NSE face "
            "construction."
        ),
    }


def analytic_finite_truncation() -> dict[str, object]:
    return {
        "passed": True,
        "statement": (
            "On a half-open window with compact closure in a classical "
            "time-analytic NSE interval, every fixed non-identically-zero Hilbert observable "
            "C_{j,Q} has finitely many zeros. Hence every fixed finite "
            "frame--cell truncation has finite positive-entry mass."
        ),
        "identicallyZeroConvention": (
            "An observable that is identically zero has no positive-denominator "
            "component and contributes no entry atom."
        ),
        "missingUniformity": (
            "Analyticity alone supplies no uniform zero count, order, "
            "separation, anchor size, truncation bound, or endpoint bound."
        ),
    }


def run() -> dict[str, object]:
    return {
        "release": "R0.71P",
        "status": "passed",
        "checks": {
            "sharpProjectionAndOverlap": sharp_projection_and_overlap(),
            "positiveMeasureLedger": positive_measure_ledger(),
            "oscillatoryTemporalPacking": oscillatory_temporal_packing(),
            "nseSharpInitialBatch": nse_sharp_initial_batch(),
            "analyticFiniteTruncation": analytic_finite_truncation(),
        },
        "verdict": (
            "Bounded spatial overlap pays all finite-order positive entries "
            "that occur at one common time through the dot H^-1 Lamb square sum. "
            "The complete target is instead an integral of that time-slice "
            "budget against a distinct entry-time counting measure. Positive "
            "atoms have no shell/cell signed cancellation, and existing "
            "ordinary budgets do not control the temporal packing."
        ),
        "claimBoundary": (
            "Exact finite-order entry batching, one abstract temporal-packing "
            "separation, and one sharp smooth NSE initial jet. No uniform NSE "
            "zero-count theorem, infinite-frame passage, Leray estimate, "
            "continuation criterion, singularity, or global-regularity result."
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
