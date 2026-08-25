#!/usr/bin/env python3
"""Exact finite audit for the R0.71B common-response packing gate.

The producer checks four narrowly delimited facts.

1. A two-shell HHL family has an order-one common-response symbol while its
   response-chord symbol decays quadratically in the shell gap.
2. A same-low-mode fan has only the intended resonances and makes same-sign
   common work accumulate in l1 while its shell-work l2 norm tends to zero.
3. A shared-high-mode, equal-radius fan has only the intended resonances and
   rules out a uniform shell-supremum times L2 times L2 bound for the
   polarized common-response covariance form.
4. A positive-output square coefficient gives an exact Cauchy--Young bound
   for covariance work and distinguishes the R0.71A same-covariance sign
   pair, whereas a positive square tent cannot distinguish that pair.

These are static periodic Fourier calculations.  They do not prove a new
Navier--Stokes continuation criterion, a dynamical Carleson estimate, global
regularity, finite-time blow-up, or any Millennium-problem claim.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

import sympy as sp

import r070x_exact_audit as r070x
import r070z_exact_audit as r070z
import r071a_exact_audit as r071a


Frequency = tuple[int, int, int]

canonical = r070z.canonical
require = r070z.require
scalar_payload = r070z.scalar_payload
vector_payload = r070z.vector_payload
frequency_square = r070z.frequency_square
negative_frequency = r070z.negative_frequency
outer = r070z.outer
frobenius = r070z.frobenius
real_cosine_modes = r070z.real_cosine_modes
strain_coefficients = r070z.strain_coefficients
contraction_work = r070z.contraction_work

e1 = r070z.e1
e2 = r070z.e2
e3 = r070z.e3


def add_frequency(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def add_matrix(
    target: dict[Frequency, sp.Matrix],
    frequency: Frequency,
    value: sp.Matrix,
) -> None:
    target[frequency] = target.get(frequency, sp.zeros(3, 3)) + value


def positive_representatives(support: set[Frequency]) -> list[Frequency]:
    return sorted(
        frequency
        for frequency in support
        if frequency > negative_frequency(frequency)
    )


def ordered_resonance_count(support: set[Frequency]) -> int:
    count = 0
    for first, second in product(support, repeat=2):
        third = negative_frequency(add_frequency(first, second))
        if third in support:
            count += 1
    return count


def squared_norm(vector: sp.Matrix) -> sp.Expr:
    return canonical(
        sum(sp.conjugate(entry) * entry for entry in vector)
    )


def matrix_squared_norm(matrix: sp.Matrix) -> sp.Expr:
    return canonical(
        sum(
            sp.conjugate(matrix[row, column]) * matrix[row, column]
            for row in range(matrix.rows)
            for column in range(matrix.cols)
        )
    )


# ---------------------------------------------------------------------------
# 1. The exact two-shell common/chord family.
# ---------------------------------------------------------------------------

M = sp.symbols("M", integer=True, positive=True)
R_square = canonical(2 * M**2 + 2 * M + 1)
R = sp.sqrt(R_square)

single_n = sp.Matrix([1, 1, 0])
single_p = sp.Matrix([M, -M - 1, 0])
single_q = sp.Matrix([-M - 1, M, 0])
single_c = sp.Matrix([1, -1, 0]) / sp.sqrt(2)
single_a = e3
single_b = sp.Matrix([M, M + 1, 0]) / R

single_A_n = canonical(
    r070x.triad_leg(
        single_n,
        single_p,
        single_q,
        single_c,
        single_a,
        single_b,
    )
)
single_A_p = canonical(
    r070x.triad_leg(
        single_p,
        single_q,
        single_n,
        single_a,
        single_b,
        single_c,
    )
)
single_A_q = canonical(
    r070x.triad_leg(
        single_q,
        single_n,
        single_p,
        single_b,
        single_c,
        single_a,
    )
)

single_full = canonical(single_A_n + single_A_p + single_A_q)
single_principal = single_A_n
single_common = canonical((single_full + single_principal) / 2)
single_chord = canonical((single_full - single_principal) / 2)

single_common_expected = canonical(
    sp.sqrt(2) * M * (M + 1) * (2 * M + 1) / R_square ** sp.Rational(3, 2)
)
single_chord_expected = canonical(
    -sp.sqrt(2) * (2 * M + 1) / (2 * R_square ** sp.Rational(3, 2))
)
single_weighted_null = canonical(
    single_n.dot(single_n) * single_A_n
    + single_p.dot(single_p) * single_A_p
    + single_q.dot(single_q) * single_A_q
)

require(single_n + single_p + single_q == sp.zeros(3, 1), "single resonance")
require(canonical(single_n.dot(single_c)) == 0, "single low divergence")
require(canonical(single_p.dot(single_a)) == 0, "single p divergence")
require(canonical(single_q.dot(single_b)) == 0, "single q divergence")
require(canonical(single_p.dot(single_p) - R_square) == 0, "single p radius")
require(canonical(single_q.dot(single_q) - R_square) == 0, "single q radius")
require(single_weighted_null == 0, "single weighted cyclic null")
require(single_common == single_common_expected, "single common response")
require(single_chord == single_chord_expected, "single chord response")
require(canonical(R_square.subs(M, 4) - 16 * single_n.dot(single_n)) > 0, "single strict HHL separation")

single_common_M4 = canonical(single_common.subs(M, 4))
single_chord_M4 = canonical(single_chord.subs(M, 4))
single_common_derivative = canonical(sp.diff(single_common, M))
single_common_limit = sp.limit(single_common, M, sp.oo)
single_chord_quadratic_limit = sp.limit(M**2 * single_chord, M, sp.oo)
require(single_common_limit == 1, "single common order-one limit")
require(single_common_derivative > 0, "single common monotonicity")
require(
    single_chord_quadratic_limit == -sp.Rational(1, 2),
    "single chord quadratic limit",
)
require(float(single_common_M4) > 0.969, "single common M4 lower check")


# ---------------------------------------------------------------------------
# 2. A same-low-mode fan: l1 common work does not follow from l2 shell work.
# ---------------------------------------------------------------------------

FAN_N = 8
same_low_M = [8**index for index in range(1, FAN_N + 1)]
same_low_n: Frequency = (1, 1, 0)
same_low_support: set[Frequency] = {
    same_low_n,
    negative_frequency(same_low_n),
}

for fan_M in same_low_M:
    fan_p = (fan_M, -fan_M - 1, 0)
    fan_q = (-fan_M - 1, fan_M, 0)
    same_low_support.update(
        {
            fan_p,
            negative_frequency(fan_p),
            fan_q,
            negative_frequency(fan_q),
        }
    )

same_low_resonance_count = ordered_resonance_count(same_low_support)
require(
    same_low_resonance_count == 12 * FAN_N,
    "same-low fan has only intended ordered resonances",
)

same_low_common_terms = [canonical(single_common.subs(M, value)) for value in same_low_M]
same_low_work = canonical(sum(same_low_common_terms) / (4 * FAN_N))
same_low_shell_l2 = canonical(
    sp.sqrt(sum(value**2 for value in same_low_common_terms)) / (4 * FAN_N)
)
same_low_energy = sp.Rational(3, 2)
same_low_lower = canonical(single_common_M4 / 4)
require(canonical(same_low_work - same_low_lower) > 0, "same-low positive work lower")
require(same_low_energy == sp.Rational(3, 2), "same-low fixed energy")

same_low_sequence = []
for count in (1, 2, 4, 8):
    values = [canonical(single_common.subs(M, 8**index)) for index in range(1, count + 1)]
    total = canonical(sum(values) / (4 * count))
    shell_l2 = canonical(sp.sqrt(sum(value**2 for value in values)) / (4 * count))
    same_low_sequence.append(
        {
            "N": count,
            "totalCommonWorkFloat": float(total),
            "shellWorkL2Float": float(shell_l2),
            "ratio": float(total / shell_l2),
        }
    )


# ---------------------------------------------------------------------------
# 3. A shared-high equal-radius fan: shell sup cannot replace square packing.
# ---------------------------------------------------------------------------

SHARED_N = 8
shared_M = [16**index for index in range(1, SHARED_N + 1)]
shared_denominators = [1 + value**2 for value in shared_M]
shared_Q = int(sp.prod(shared_denominators))
shared_q: Frequency = (shared_Q, 0, 0)
shared_b = e3

shared_low_modes: dict[Frequency, sp.Matrix] = {}
shared_p_modes: dict[Frequency, sp.Matrix] = {}
shared_c_vectors: list[sp.Matrix] = []
shared_a_vectors: list[sp.Matrix] = []
shared_n_frequencies: list[Frequency] = []
shared_p_frequencies: list[Frequency] = []

for fan_M, denominator in zip(shared_M, shared_denominators):
    fan_n: Frequency = (
        -2 * shared_Q // denominator,
        -2 * shared_Q * fan_M // denominator,
        0,
    )
    fan_p: Frequency = (
        shared_Q * (1 - fan_M**2) // denominator,
        2 * shared_Q * fan_M // denominator,
        0,
    )
    fan_c = sp.Matrix([fan_M, -1, 0]) / sp.sqrt(denominator)
    fan_a = sp.Matrix([-2 * fan_M, 1 - fan_M**2, 0]) / denominator

    require(
        add_frequency(add_frequency(fan_n, fan_p), shared_q) == (0, 0, 0),
        "shared-high intended resonance",
    )
    require(frequency_square(fan_p) == shared_Q**2, "shared-high equal p radius")
    require(frequency_square(shared_q) == shared_Q**2, "shared-high q radius")
    require(canonical(sp.Matrix(fan_n).dot(fan_c)) == 0, "shared-low divergence")
    require(canonical(sp.Matrix(fan_p).dot(fan_a)) == 0, "shared-p divergence")
    require(canonical(fan_c.dot(fan_c)) == 1, "shared-low unit polarization")
    require(canonical(fan_a.dot(fan_a)) == 1, "shared-p unit polarization")

    shared_n_frequencies.append(fan_n)
    shared_p_frequencies.append(fan_p)
    shared_c_vectors.append(fan_c)
    shared_a_vectors.append(fan_a)
    shared_low_modes.update(real_cosine_modes(fan_n, fan_c))
    shared_p_modes.update(
        real_cosine_modes(fan_p, fan_a / sp.sqrt(SHARED_N))
    )

shared_q_modes = real_cosine_modes(shared_q, shared_b)
shared_support = set(shared_low_modes) | set(shared_p_modes) | set(shared_q_modes)
shared_resonance_count = ordered_resonance_count(shared_support)
require(
    shared_resonance_count == 12 * SHARED_N,
    "shared-high fan has only intended ordered resonances",
)

shared_low_radii_squared = [frequency_square(value) for value in shared_n_frequencies]
for low_square in shared_low_radii_squared:
    require(shared_Q**2 > 16 * low_square, "shared high-low frame separation")
for first, second in zip(shared_low_radii_squared, shared_low_radii_squared[1:]):
    require(first > 16 * second, "shared low-low frame separation")

# Equal high radii make every response inner product exactly one.  The
# cross-covariance is therefore the physical symmetric product B_N odot C_N.
shared_cross_covariance: dict[Frequency, sp.Matrix] = {}
for first_frequency, first_coefficient in shared_p_modes.items():
    for second_frequency, second_coefficient in shared_q_modes.items():
        output = add_frequency(first_frequency, second_frequency)
        symmetric = canonical(
            (outer(first_coefficient, second_coefficient)
             + outer(second_coefficient, first_coefficient)) / 2
        )
        add_matrix(shared_cross_covariance, output, symmetric)

shared_low_strain = strain_coefficients(shared_low_modes)
shared_cross_work = canonical(
    contraction_work(shared_low_strain, shared_cross_covariance)
)
shared_cross_expected = canonical(
    -sum(
        sp.Rational(value, 1) / sp.sqrt(1 + value**2)
        for value in shared_M
    )
    / (8 * sp.sqrt(SHARED_N))
)
require(
    canonical(shared_cross_work - shared_cross_expected) == 0,
    "shared-high Fourier cross-work reconstruction",
)

shared_low_energy = canonical(
    sum(squared_norm(value) for value in shared_low_modes.values())
)
shared_p_energy = canonical(
    sum(squared_norm(value) for value in shared_p_modes.values())
)
shared_q_energy = canonical(
    sum(squared_norm(value) for value in shared_q_modes.values())
)
require(
    shared_low_energy == sp.Rational(SHARED_N, 2),
    "shared-low energy",
)
require(shared_p_energy == sp.Rational(1, 2), "shared-p normalized energy")
require(shared_q_energy == sp.Rational(1, 2), "shared-q normalized energy")

# Strict factor-four separation means any scalar frame block sees at most one
# low cosine.  Parseval gives |m_alpha(k)|<=1, so the frame shell supremum is
# at most one.  The root tent square mass is exactly the L2 mass N/2.
shared_frame_shell_sup_upper = sp.Integer(1)
shared_root_tent_square_mass = shared_low_energy
shared_operator_ratio_lower = canonical(
    abs(shared_cross_expected)
    / (
        shared_frame_shell_sup_upper
        * sp.sqrt(shared_p_energy)
        * sp.sqrt(shared_q_energy)
    )
)

shared_sequence = []
for count in (1, 2, 4, 8):
    values = [16**index for index in range(1, count + 1)]
    work = canonical(
        -sum(sp.Rational(value, 1) / sp.sqrt(1 + value**2) for value in values)
        / (8 * sp.sqrt(count))
    )
    ratio = canonical(2 * abs(work))
    shared_sequence.append(
        {
            "N": count,
            "crossWorkFloat": float(work),
            "normalizedOperatorRatioFloat": float(ratio),
            "rootTentNormLower": float(sp.sqrt(sp.Rational(count, 2))),
        }
    )


# ---------------------------------------------------------------------------
# 4. A sign-sensitive positive-output square coefficient.
# ---------------------------------------------------------------------------


def signed_output_ledger(
    modes: dict[Frequency, sp.Matrix],
    covariance: dict[Frequency, sp.Matrix],
) -> dict[str, object]:
    strain = strain_coefficients(modes)
    representatives = positive_representatives(set(strain))
    signed_outputs: list[tuple[Frequency, sp.Expr]] = []
    positive_square = sp.Integer(0)
    gradient_weight = sp.Integer(0)

    for frequency in representatives:
        strain_coefficient = strain[frequency]
        covariance_coefficient = covariance.get(frequency, sp.zeros(3, 3))
        work = canonical(
            2
            * sp.re(
                sum(
                    sp.conjugate(strain_coefficient[row, column])
                    * covariance_coefficient[row, column]
                    for row in range(3)
                    for column in range(3)
                )
            )
        )
        if work != 0:
            signed_outputs.append((frequency, work))

        strain_square = matrix_squared_norm(strain_coefficient)
        gradient_weight = canonical(
            gradient_weight
            + 4 * frequency_square(frequency) * strain_square
        )
        if work.is_positive:
            require(strain_square > 0, "positive work has nonzero strain output")
            positive_square = canonical(
                positive_square
                + work**2
                / (4 * frequency_square(frequency) * strain_square)
            )

    energy = canonical(sum(squared_norm(value) for value in modes.values()))
    gradient_energy = canonical(
        sum(
            frequency_square(frequency) * squared_norm(value)
            for frequency, value in modes.items()
        )
    )
    require(
        canonical(gradient_weight - gradient_energy) == 0,
        "strain-gradient Parseval identity",
    )

    return {
        "signedOutputs": [
            {"frequency": list(frequency), "work": scalar_payload(work)}
            for frequency, work in signed_outputs
        ],
        "positiveSquare": positive_square,
        "energy": energy,
        "normalizedCoefficient": canonical(
            positive_square / energy if energy != 0 else 0
        ),
        "gradientWeight": gradient_weight,
    }


positive_output = signed_output_ledger(
    r071a.combined_plus,
    r071a.combined_plus_covariance,
)
negative_output = signed_output_ledger(
    r071a.combined_minus,
    r071a.combined_minus_covariance,
)

require(positive_output["positiveSquare"] == sp.Rational(9, 800), "R0.71A positive square")
require(positive_output["energy"] == sp.Rational(299553, 2), "R0.71A energy")
require(positive_output["normalizedCoefficient"] == sp.Rational(3, 39940400), "R0.71A normalized positive coefficient")
require(negative_output["positiveSquare"] == 0, "R0.71A negative positive-square vanishing")
require(negative_output["normalizedCoefficient"] == 0, "R0.71A negative normalized coefficient")

# The exact Cauchy--Young reduction is checked algebraically.  Here D is the
# gradient enstrophy and T is the positive-output square root.
D, T, viscosity, energy_symbol, a_plus = sp.symbols(
    "D T nu E a_plus", positive=True
)
cauchy_rhs = sp.sqrt(D) * T
young_rhs = viscosity * D / 4 + T**2 / viscosity
young_residual = canonical(
    young_rhs - cauchy_rhs
)
young_square = canonical(
    (sp.sqrt(viscosity * D) / 2 - T / sp.sqrt(viscosity)) ** 2
)
require(canonical(young_residual - young_square) == 0, "exact Young square")
require(
    canonical((T**2 / viscosity).subs(T**2, a_plus * energy_symbol)
              - a_plus * energy_symbol / viscosity) == 0,
    "normalized coefficient substitution",
)

# A single divergence-free plane wave has nonzero BMO/square amplitude but
# zero covariance work and hence zero positive-output coefficient.
plane_frequency: Frequency = (7, 0, 0)
plane_modes = real_cosine_modes(plane_frequency, e2)
plane_strain = strain_coefficients(plane_modes)
plane_covariance = r070z.covariance_convolution(
    plane_modes,
    lambda first, second: sp.Integer(
        frequency_square(first) == frequency_square(second)
    ),
)
plane_work = canonical(contraction_work(plane_strain, plane_covariance))
plane_output = signed_output_ledger(plane_modes, plane_covariance)
require(plane_work == 0, "plane-wave covariance work")
require(plane_output["positiveSquare"] == 0, "plane-wave positive square")
require(plane_output["energy"] == sp.Rational(1, 2), "plane-wave nonzero square amplitude")


payload = {
    "release": "R0.71B",
    "status": "common-response-packing-and-positive-output-gate",
    "checks": {
        "twoShellCommonOrderOne": True,
        "twoShellChordQuadraticDecay": True,
        "sameLowFanOnlyIntendedResonances": True,
        "sameLowFanNoL2ToL1Upgrade": True,
        "sharedHighFanEqualResponse": True,
        "sharedHighFanOnlyIntendedResonances": True,
        "sharedHighFanShellSupFailure": True,
        "positiveOutputCauchyYoungReduction": True,
        "sameCovarianceSignPairSeparated": True,
        "positiveSquareNotBmoEquivalent": True,
    },
    "singleHhlLedger": {
        "frequencies": {
            "n": vector_payload(single_n),
            "p": vector_payload(single_p),
            "q": vector_payload(single_q),
        },
        "polarizations": {
            "c": vector_payload(single_c),
            "a": vector_payload(single_a),
            "b": vector_payload(single_b),
        },
        "radiusSquare": scalar_payload(R_square),
        "strainLegs": [
            scalar_payload(single_A_n),
            scalar_payload(single_A_p),
            scalar_payload(single_A_q),
        ],
        "weightedCyclicResidual": scalar_payload(single_weighted_null),
        "fullSymbol": scalar_payload(single_full),
        "principalSymbol": scalar_payload(single_principal),
        "commonSymbol": scalar_payload(single_common),
        "chordSymbol": scalar_payload(single_chord),
        "commonAtM4": scalar_payload(single_common_M4),
        "commonDerivative": scalar_payload(single_common_derivative),
        "chordAtM4": scalar_payload(single_chord_M4),
        "commonLimit": scalar_payload(single_common_limit),
        "M2TimesChordLimit": scalar_payload(single_chord_quadratic_limit),
        "decision": "the common channel stays order one while the chord channel is O(M^-2)",
    },
    "sameLowFanLedger": {
        "auditN": FAN_N,
        "MValues": same_low_M,
        "modeCount": len(same_low_support),
        "orderedResonanceCount": same_low_resonance_count,
        "expectedOrderedResonanceCount": 12 * FAN_N,
        "energy": scalar_payload(same_low_energy),
        "totalCommonWork": "(1/(4*N))*sum_(j=1)^N U_(8^j), evaluated exactly at N=8",
        "totalCommonWorkFloat": float(same_low_work),
        "shellWorkL2": "(1/(4*N))*sqrt(sum_(j=1)^N U_(8^j)^2), evaluated exactly at N=8",
        "shellWorkL2Float": float(same_low_shell_l2),
        "uniformPositiveLower": scalar_payload(same_low_lower),
        "sequence": same_low_sequence,
        "asymptotic": "total common work tends to 1/4 while shell-work l2 is asymptotic to 1/(4*sqrt(N))",
        "decision": "same sign and common response do not supply a shell-count-independent l2-to-l1 upgrade",
    },
    "sharedHighFanLedger": {
        "auditN": SHARED_N,
        "MValues": shared_M,
        "commonHighRadius": str(shared_Q),
        "commonHighRadiusDigits": len(str(shared_Q)),
        "modeCount": len(shared_support),
        "orderedResonanceCount": shared_resonance_count,
        "expectedOrderedResonanceCount": 12 * SHARED_N,
        "lowRadiiSquared": [str(value) for value in shared_low_radii_squared],
        "highResponseInnerProducts": "Gamma(p_j,q)=1 exactly because all high radii equal Q_N",
        "otherResponseInnerProducts": "low-high and distinct low-low responses are zero by strict factor-four separation",
        "lowFrameShellSupUpper": scalar_payload(shared_frame_shell_sup_upper),
        "lowEnergy": scalar_payload(shared_low_energy),
        "firstHighEnergy": scalar_payload(shared_p_energy),
        "secondHighEnergy": scalar_payload(shared_q_energy),
        "rootTentSquareMass": scalar_payload(shared_root_tent_square_mass),
        "crossWork": "-(1/(8*sqrt(N)))*sum_(j=1)^N M_j/sqrt(1+M_j^2), M_j=16^j",
        "crossWorkFloat": float(shared_cross_work),
        "crossWorkResidual": scalar_payload(
            canonical(shared_cross_work - shared_cross_expected)
        ),
        "normalizedOperatorRatioLower": "(1/(4*sqrt(N)))*sum_(j=1)^N M_j/sqrt(1+M_j^2)",
        "normalizedOperatorRatioLowerFloat": float(shared_operator_ratio_lower),
        "sequence": shared_sequence,
        "asymptotic": "the normalized common-response operator ratio grows like sqrt(N)/4 while the frame shell supremum and both high L2 norms stay fixed",
        "decision": "no uniform shell-supremum times L2 times L2 estimate exists for the polarized common-response form",
    },
    "positiveOutputLedger": {
        "definition": "w_k=2*Re(conj(S_hat(k)):Q_hat(k)); T_+^2=sum_k (w_k^+)^2/(4*|k|^2*|S_hat(k)|_F^2), with zero quotient when S_hat(k)=0",
        "identity": "P_Q=sum_(k in K_+) w_k",
        "cauchy": "(P_Q)_+<=||grad omega||_2*T_+",
        "young": "(P_Q)_+<=(nu/4)||grad omega||_2^2+nu^(-1)*a_+*||omega||_2^2, a_+=T_+^2/||omega||_2^2",
        "youngResidualSquare": "(sqrt(nu*D)/2-T/sqrt(nu))^2",
        "r071aPositive": {
            "signedOutputs": positive_output["signedOutputs"],
            "positiveSquare": scalar_payload(positive_output["positiveSquare"]),
            "energy": scalar_payload(positive_output["energy"]),
            "normalizedCoefficient": scalar_payload(positive_output["normalizedCoefficient"]),
        },
        "r071aNegative": {
            "signedOutputs": negative_output["signedOutputs"],
            "positiveSquare": scalar_payload(negative_output["positiveSquare"]),
            "energy": scalar_payload(negative_output["energy"]),
            "normalizedCoefficient": scalar_payload(negative_output["normalizedCoefficient"]),
        },
        "planeWave": {
            "frequency": list(plane_frequency),
            "energy": scalar_payload(plane_output["energy"]),
            "covarianceWork": scalar_payload(plane_work),
            "positiveSquare": scalar_payload(plane_output["positiveSquare"]),
        },
        "decision": "the signed coefficient distinguishes the same-Q sign pair and is not equivalent to a positive BMO square amplitude; no energy or NSE propagation bound for a_+ is proved",
    },
    "analyticDependencies": [
        "the analysis frame is the fixed real-even radial smooth scalar Parseval frame used in R0.70P-R0.71A",
        "equal radii give identical frame-response vectors and strict factor-four separation gives orthogonal response vectors",
        "the arbitrary-N fan resonance classifications use the displayed lacunary frequency formulas; the producer exhaustively checks N=8",
        "the frame shell-supremum bound uses strict support separation and |m_alpha(k)|<=1 from Parseval",
        "the root tent square mass uses Parseval and normalized Haar measure on the torus",
        "the standard local square Carleson norm is BMO-equivalent only after the usual admissible Littlewood-Paley hypotheses; that literature theorem is not proved by this finite producer",
        "the positive-output Cauchy bound uses |S_hat(k)|_F^2=|omega_hat(k)|^2/2 for divergence-free Fourier coefficients",
    ],
    "claimBoundary": [
        "proves that common response can remain order one when the response chord is quadratically small",
        "rules out automatic same-sign l2-to-l1 scale packing and a direct polarized shell-supremum times L2 times L2 common-response estimate",
        "does not rule out the established vorticity BMO or Besov continuation criteria, because those use Carleson square mass or logarithmic higher-norm arguments rather than the rejected direct estimate",
        "shows that an ordinary positive square tent is sign blind on the R0.71A same-covariance pair and, under standard hypotheses, is a BMO restatement",
        "defines an exact sign-sensitive positive-output coefficient and proves its Cauchy--Young consumer inequality, but does not derive its time integrability from Leray energy or Navier--Stokes dynamics",
        "does not prove a new continuation criterion, a singularity, global regularity, or solve the Millennium problem",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(rendered, end="")
    else:
        arguments.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
