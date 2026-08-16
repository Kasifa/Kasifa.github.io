#!/usr/bin/env python3
"""Cone-chain geometry and first-Picard Duhamel audit.

The base object is the five-wavevector non-coplanar butterfly from R0.8.  A
plain dyadic dilation produces disconnected copies.  The integer map

    M = I + 1 1^T = [[2, 1, 1], [1, 2, 1], [1, 1, 2]]

instead gives the exact cross-shell relation

    c_j + e_j + a_{j+1} = 0,

where k_j=M^j k.  The script enumerates every unsigned triad, validates the
closed formulas for the transported divergence-free polarization, and
computes the first Picard iterate after heat evolution.

The calculations concern a finite Fourier field and its first Duhamel term.
They are not a nonlinear remainder estimate or a regularity result.
"""

from __future__ import annotations

from itertools import combinations, product
import json
import math

import numpy as np

from noncoplanar_butterfly import (
    A_MODE,
    B_MODE,
    C_MODE,
    D_MODE,
    E_MODE,
    CENTERS,
    butterfly_field,
    negate,
    normalized_symmetric_candidate,
)
from triad_leakage_variation import bilinear, hhalf_pairing


MATRIX = np.asarray(
    [
        [2, 1, 1],
        [1, 2, 1],
        [1, 1, 2],
    ],
    dtype=np.int64,
)
MODE_NAMES = ("a", "b", "c", "d", "e")
MODE_BY_NAME = dict(zip(MODE_NAMES, CENTERS, strict=True))
Q = normalized_symmetric_candidate()[0]
ASYMPTOTIC_CONSTANT = 81.0 / (173056.0 * math.sqrt(3.0))


def integer_power(power: int) -> np.ndarray:
    return np.linalg.matrix_power(MATRIX, power)


def transform_mode(
    wavevector: tuple[int, int, int],
    level: int,
) -> tuple[int, int, int]:
    transformed = integer_power(level) @ np.asarray(wavevector, dtype=np.int64)
    return tuple(int(value) for value in transformed)


def shell_vertices(
    maximum_level: int,
) -> list[tuple[int, str, tuple[int, int, int]]]:
    return [
        (level, name, transform_mode(MODE_BY_NAME[name], level))
        for level in range(maximum_level + 1)
        for name in MODE_NAMES
    ]


def dilated_vertices(
    maximum_level: int,
    ratio: int,
) -> list[tuple[int, str, tuple[int, int, int]]]:
    return [
        (
            level,
            name,
            tuple((ratio**level) * value for value in MODE_BY_NAME[name]),
        )
        for level in range(maximum_level + 1)
        for name in MODE_NAMES
    ]


def normalized_signs(signs: tuple[int, int, int]) -> tuple[int, int, int]:
    if signs[0] < 0:
        return tuple(-value for value in signs)
    return signs


def enumerate_unsigned_triads(
    vertices: list[tuple[int, str, tuple[int, int, int]]],
) -> list[dict[str, object]]:
    """Enumerate distinct three-vertex relations up to a common sign."""

    relations: list[dict[str, object]] = []
    for chosen in combinations(vertices, 3):
        found: set[tuple[int, int, int]] = set()
        for signs in product((-1, 1), repeat=3):
            total = tuple(
                sum(
                    signs[index] * chosen[index][2][axis]
                    for index in range(3)
                )
                for axis in range(3)
            )
            if total == (0, 0, 0):
                found.add(normalized_signs(signs))
        for signs in sorted(found):
            relations.append(
                {
                    "vertices": [
                        {
                            "level": level,
                            "name": name,
                            "wavevector": wavevector,
                        }
                        for level, name, wavevector in chosen
                    ],
                    "signs": signs,
                    "crossShell": len({level for level, _, _ in chosen}) > 1,
                }
            )
    return relations


def relation_signature(relation: dict[str, object]) -> tuple[tuple[int, str], ...]:
    vertices = relation["vertices"]
    signs = relation["signs"]
    return tuple(
        (int(vertex["level"]), f"{sign:+d}{vertex['name']}")
        for vertex, sign in zip(vertices, signs, strict=True)
    )


def expected_cone_signatures(maximum_level: int) -> set[tuple[tuple[int, str], ...]]:
    expected: set[tuple[tuple[int, str], ...]] = set()
    for level in range(maximum_level + 1):
        expected.add(((level, "+1a"), (level, "+1b"), (level, "+1c")))
        expected.add(((level, "+1a"), (level, "+1d"), (level, "+1e")))
    for level in range(maximum_level):
        # Vertex order follows MODE_NAMES inside increasing shell levels.
        expected.add(((level, "+1c"), (level, "+1e"), (level + 1, "+1a")))
    return expected


def transverse_invariants() -> dict[str, dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    diagonal = np.ones(3, dtype=np.int64)
    for name, wavevector in MODE_BY_NAME.items():
        vector = np.asarray(wavevector, dtype=np.int64)
        diagonal_sum = int(np.sum(vector))
        transverse = 3 * vector - diagonal_sum * diagonal
        records[name] = {
            "s": diagonal_sum,
            "tau": tuple(int(value) for value in transverse),
        }
    return records


def transformed_shell(level: int) -> dict[tuple[int, int, int], np.ndarray]:
    """Push wavevectors by M^j and coefficients by M^{-j}."""

    base = butterfly_field(*normalized_symmetric_candidate())
    wavevector_map = integer_power(level)
    coefficient_map = np.linalg.matrix_power(MATRIX.astype(float), -level)
    transformed: dict[tuple[int, int, int], np.ndarray] = {}
    for wavevector, coefficient in base.items():
        new_wavevector = tuple(
            int(value)
            for value in wavevector_map @ np.asarray(wavevector, dtype=np.int64)
        )
        transformed[new_wavevector] = coefficient_map @ coefficient
    return transformed


def shell_energy_formula(level: int) -> float:
    x_value = float(4**level)
    return (
        12.0 * Q**2 * math.sqrt((x_value**2 + 2.0) / 3.0)
        + 4.0
        * Q**2
        * math.sqrt((4.0 * x_value**2 + 2.0) / 3.0)
        * (2.0 / 3.0 + 1.0 / (3.0 * x_value**2))
    )


def feed_squared_formula(level: int) -> float:
    x_value = float(4**level)
    return Q**4 * (
        2.0 / 3.0
        + 4.0 / (3.0 * x_value**2)
        - 12.0 / (16.0 * x_value**2 + 2.0)
    )


def heat_parameters(level: int) -> dict[str, float]:
    x_value = float(4**level)
    output_frequency_squared = (16.0 * x_value**2 + 2.0) / 3.0
    input_frequency_squared = (8.0 * x_value**2 + 4.0) / 3.0
    difference = output_frequency_squared - input_frequency_squared
    maximizing_time = math.log(
        output_frequency_squared / input_frequency_squared
    ) / difference
    maximum_scalar = (
        (input_frequency_squared / output_frequency_squared)
        ** (input_frequency_squared / difference)
        / output_frequency_squared
    )
    return {
        "K": output_frequency_squared,
        "L": input_frequency_squared,
        "maximizingTime": maximizing_time,
        "maximumDuhamelScalar": maximum_scalar,
    }


def normalized_first_picard_energy(level: int) -> float:
    heat = heat_parameters(level)
    return (
        2.0
        * math.sqrt(heat["K"])
        * feed_squared_formula(level)
        / shell_energy_formula(level) ** 2
        * heat["maximumDuhamelScalar"] ** 2
    )


def feed_direct(level: int) -> dict[str, float]:
    field = transformed_shell(level)
    target = transform_mode(A_MODE, level + 1)
    coefficient = bilinear(field, field)[target]
    target_vector = np.asarray(target, dtype=float)
    return {
        "targetNorm": float(np.linalg.norm(target_vector)),
        "feedSquared": float(np.vdot(coefficient, coefficient).real),
        "divergenceResidual": float(abs(np.dot(target_vector, coefficient))),
        "shellEnergy": hhalf_pairing(field, field),
    }


def pair_multiplicity(
    support: set[tuple[int, int, int]],
    output: set[tuple[int, int, int]],
) -> int:
    return max(
        sum(
            1
            for p in support
            for q in support
            if tuple(p[axis] + q[axis] for axis in range(3)) == target
        )
        for target in output
    )


def sparse_first_picard_bound(level: int, viscosity: float = 1.0) -> float:
    """Return the general annular multiplicity bound for the normalized shell."""

    x_value = float(4**level)
    field = transformed_shell(level)
    support = set(field)
    target = transform_mode(A_MODE, level + 1)
    output = {target, negate(target)}
    input_norms = [np.linalg.norm(wavevector) for wavevector in support]
    output_norms = [np.linalg.norm(wavevector) for wavevector in output]
    c_zero = min(input_norms) / x_value
    C_zero = max(input_norms) / x_value
    c_one = min(output_norms) / x_value
    C_one = max(output_norms) / x_value
    multiplicity = pair_multiplicity(support, output)
    return (
        C_one
        * C_zero**2
        / (viscosity**2 * c_one**4 * c_zero**2)
        * multiplicity
        / x_value**3
    )


def naive_dilation_audit() -> list[dict[str, int]]:
    records = []
    for ratio in (2, 3, 4):
        for maximum_level in (1, 2, 3):
            triads = enumerate_unsigned_triads(
                dilated_vertices(maximum_level, ratio)
            )
            records.append(
                {
                    "ratio": ratio,
                    "maximumLevel": maximum_level,
                    "vertices": 5 * (maximum_level + 1),
                    "triads": len(triads),
                    "crossShellTriads": sum(
                        int(relation["crossShell"]) for relation in triads
                    ),
                }
            )
    return records


def base_dependent_triples() -> list[dict[str, object]]:
    """Return the linearly dependent triples among the five base centers."""

    records = []
    for indices in combinations(range(len(CENTERS)), 3):
        matrix = np.column_stack([CENTERS[index] for index in indices])
        if round(float(np.linalg.det(matrix))) == 0:
            records.append(
                {
                    "indices": indices,
                    "names": tuple(MODE_NAMES[index] for index in indices),
                }
            )
    return records


def cone_hypergraph_audit() -> list[dict[str, object]]:
    records = []
    for maximum_level in range(1, 6):
        triads = enumerate_unsigned_triads(shell_vertices(maximum_level))
        records.append(
            {
                "maximumLevel": maximum_level,
                "vertices": 5 * (maximum_level + 1),
                "triads": len(triads),
                "crossShellTriads": sum(
                    int(relation["crossShell"]) for relation in triads
                ),
                "signatures": [relation_signature(relation) for relation in triads],
            }
        )
    return records


def duhamel_table() -> list[dict[str, float]]:
    records = []
    for level in range(8):
        x_value = float(4**level)
        direct = feed_direct(level)
        heat = heat_parameters(level)
        energy = shell_energy_formula(level)
        first_picard = normalized_first_picard_energy(level)
        bound = sparse_first_picard_bound(level)
        records.append(
            {
                "level": level,
                "x": x_value,
                "targetNorm": direct["targetNorm"],
                "shellEnergy": energy,
                "feedSquared": feed_squared_formula(level),
                "maximizingTime": heat["maximizingTime"],
                "normalizedFirstPicardHHalfSquared": first_picard,
                "xToFifthScaledEnergy": x_value**5 * first_picard,
                "scaledToLimitRatio": x_value**5
                * first_picard
                / ASYMPTOTIC_CONSTANT,
                "generalSparseBound": bound,
                "exactToGeneralBoundRatio": first_picard / bound,
                "directEnergyRelativeError": abs(direct["shellEnergy"] - energy)
                / energy,
                "directFeedRelativeError": abs(
                    direct["feedSquared"] - feed_squared_formula(level)
                )
                / max(feed_squared_formula(level), 1e-300),
                "divergenceResidual": direct["divergenceResidual"],
            }
        )
    return records


def run_audit() -> dict[str, object]:
    return {
        "statement": (
            "exact triad geometry and first-Picard heat calculation; "
            "not a nonlinear remainder estimate or PDE regularity result"
        ),
        "matrix": MATRIX.tolist(),
        "matrixEigenvalues": sorted(np.linalg.eigvalsh(MATRIX).tolist()),
        "transverseInvariants": transverse_invariants(),
        "baseDependentTriples": base_dependent_triples(),
        "naiveDilations": naive_dilation_audit(),
        "coneHypergraphs": cone_hypergraph_audit(),
        "asymptotic": {
            "claim": "H_j ~ C 4^(-5j)",
            "constant": ASYMPTOTIC_CONSTANT,
        },
        "duhamel": duhamel_table(),
        "generalSparseLemma": {
            "bound": (
                "||w||_Hhalf^2 <= "
                "C1*C0^2*m_N/(nu^2*c1^4*c0^2*N^3) "
                "||u0||_Hhalf^4"
            ),
            "interpretation": (
                "bounded critical energy and m_N=o(N^3) force the "
                "first Picard energy in a comparable output annulus to vanish"
            ),
        },
    }


def validate(audit: dict[str, object]) -> None:
    assert np.allclose(audit["matrixEigenvalues"], [1.0, 1.0, 4.0])
    assert [record["names"] for record in audit["baseDependentTriples"]] == [
        ("a", "b", "c"),
        ("a", "d", "e"),
    ]

    for record in audit["naiveDilations"]:
        assert record["triads"] == 2 * (record["maximumLevel"] + 1)
        assert record["crossShellTriads"] == 0

    for record in audit["coneHypergraphs"]:
        maximum_level = record["maximumLevel"]
        assert record["triads"] == 3 * maximum_level + 2
        assert record["crossShellTriads"] == maximum_level
        assert set(record["signatures"]) == expected_cone_signatures(maximum_level)

    for record in audit["duhamel"]:
        assert record["directEnergyRelativeError"] < 2e-15
        # M^{-j} is evaluated in double precision; by j=7 its condition
        # number is 4^7, so the direct convolution check loses a few digits.
        assert record["directFeedRelativeError"] < 5e-13
        assert record["divergenceResidual"] < 2e-13
        assert record["normalizedFirstPicardHHalfSquared"] < record[
            "generalSparseBound"
        ]
    assert abs(audit["duhamel"][-1]["scaledToLimitRatio"] - 1.0) < 6e-9


def main() -> None:
    audit = run_audit()
    validate(audit)
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
