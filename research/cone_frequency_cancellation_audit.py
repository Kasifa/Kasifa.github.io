#!/usr/bin/env python3
"""R0.21 exact audit of the cone-frequency cancellation geometry.

Every signed input frequency has the form

    K_delta(c, beta) = delta^(-1) c (1, 1, 1) + beta,
    beta . (1, 1, 1) = 0.

In the rational label G(c, beta) = (6 c, 3 beta_1, 3 beta_2), the eight
signed inputs are exactly the vertices of a linearly transformed cube.  The
support obtained from exactly ell input leaves therefore contains
(ell + 1)^3 labels.  The zero label occurs exactly when ell is even, giving
(ell + 1)^3 - 1 nonzero Fourier modes in that case.

The same charge-offset representation makes the apparent delta^(-1)
derivative loss removable mode by mode through incompressibility.  This
script certifies the exact frequency geometry used in that lemma.  It does
not yet prove closure of an infinite analytic sequence norm, bound the
Taylor tail, or prove a Navier--Stokes regularity or singularity result.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Iterable

import fifth_order_tree_audit as tree


Rational = Fraction
Label = tuple[Rational, Rational, Rational]
ZERO_LABEL: Label = (Rational(0), Rational(0), Rational(0))
DEFAULT_MAXIMUM_LEAVES = 13


def progress(enabled: bool, started: float, message: str) -> None:
    if enabled:
        elapsed = time.perf_counter() - started
        print(f"[R0.21 Gate A +{elapsed:7.2f}s] {message}", file=sys.stderr, flush=True)


def git_source_state() -> dict[str, object]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    dirty = bool(
        subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
    )
    return {"commit": commit, "dirty": dirty}


def label_add(left: Label, right: Label) -> Label:
    return tuple(left[index] + right[index] for index in range(3))  # type: ignore[return-value]


def label_scale(scalar: int, value: Label) -> Label:
    return tuple(Rational(scalar) * component for component in value)  # type: ignore[return-value]


def frequency_label(frequency: tree.FrequencyExpansion) -> Label:
    leading, offset = frequency
    if not leading[0] == leading[1] == leading[2]:
        raise ValueError("The leading frequency is not diagonal.")
    if sum(offset, start=Rational(0)) != 0:
        raise ValueError("The frequency offset is not transverse to the diagonal.")
    return 6 * leading[0], 3 * offset[0], 3 * offset[1]


def label_record(value: Label) -> list[str]:
    return [str(component) for component in value]


def cube_vertices(a: Label, b: Label, c: Label) -> set[Label]:
    return {
        label_add(label_add(label_scale(sa, a), label_scale(sb, b)), label_scale(sc, c))
        for sa in (-1, 1)
        for sb in (-1, 1)
        for sc in (-1, 1)
    }


def determinant(columns: tuple[Label, Label, Label]) -> Rational:
    a, b, c = columns
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - b[0] * (a[1] * c[2] - a[2] * c[1])
        + c[0] * (a[1] * b[2] - a[2] * b[1])
    )


def support_profiles(generators: tuple[Label, ...], maximum_leaves: int) -> list[dict[str, object]]:
    current = {ZERO_LABEL}
    profiles: list[dict[str, object]] = []
    target = frequency_label(tree.NEXT_A_POSITIVE)
    for leaves in range(1, maximum_leaves + 1):
        current = {label_add(label, generator) for label in current for generator in generators}
        contains_zero = ZERO_LABEL in current
        nonzero_count = len(current) - int(contains_zero)
        profiles.append(
            {
                "leaves": leaves,
                "allLabelCount": len(current),
                "expectedAllLabelCount": (leaves + 1) ** 3,
                "containsZero": contains_zero,
                "expectedContainsZero": leaves % 2 == 0,
                "nonzeroModeCount": nonzero_count,
                "expectedNonzeroModeCount": (leaves + 1) ** 3 - int(leaves % 2 == 0),
                "containsNextShellTarget": target in current,
            }
        )
    return profiles


def compositions(total: int, length: int) -> Iterable[tuple[int, ...]]:
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, length - 1):
            yield (first,) + rest


def target_degree_counts(maximum_leaves: int) -> list[dict[str, int]]:
    frequencies = tree.signed_frequencies()
    result: list[dict[str, int]] = []
    for leaves in range(1, maximum_leaves + 1):
        count = sum(
            tree.degree_frequency(degree, frequencies) == tree.NEXT_A_POSITIVE
            for degree in compositions(leaves, len(frequencies))
        )
        result.append({"leaves": leaves, "signedMultiplicityDegreeCount": count})
    return result


def generated_frequency_geometry(maximum_leaves: int) -> dict[str, object]:
    """Check A parallel to d, B perpendicular to d, and A.B = 0."""

    frequencies = tree.signed_frequencies()
    current = {(tree.ZERO_VECTOR, tree.ZERO_VECTOR)}
    checked = 0
    for _ in range(maximum_leaves):
        current = {
            tree.frequency_add(frequency, generator)
            for frequency in current
            for generator in frequencies
        }
        for leading, offset in current:
            assert leading[0] == leading[1] == leading[2]
            assert sum(offset, start=Rational(0)) == 0
            assert tree.dot(leading, offset) == 0
            checked += 1
    return {
        "maximumLeaves": maximum_leaves,
        "generatedLabelsCheckedWithRepetition": checked,
        "leadingVectorsAreDiagonal": True,
        "offsetsAreTransverse": True,
        "dimensionlessHeatCrossTermsAreZero": True,
        "heatIdentity": "delta^2 |K_delta(c,beta)|^2 = 3 c^2 + delta^2 |beta|^2",
    }


def audit(maximum_leaves: int, show_progress: bool = False) -> dict[str, object]:
    started = time.perf_counter()
    positive = tuple(frequency_label(frequency) for frequency in tree.POSITIVE_FREQUENCIES)
    signed = tuple(frequency_label(frequency) for frequency in tree.signed_frequencies())
    progress(show_progress, started, "converted the eight signed inputs to rational labels")

    # In label coordinates the four positive inputs are a +/- b +/- c, while
    # the negatives supply the other four independent sign choices.
    a: Label = (Rational(3, 2), Rational(0), Rational(0))
    b: Label = (Rational(0), Rational(0), Rational(3, 2))
    c: Label = (Rational(-1, 2), Rational(1), Rational(-1, 2))
    basis_determinant = determinant((a, b, c))
    vertices = cube_vertices(a, b, c)
    assert set(signed) == vertices
    assert basis_determinant != 0
    progress(show_progress, started, "verified the exact transformed-cube representation")

    profiles = support_profiles(signed, maximum_leaves)
    progress(show_progress, started, f"enumerated exact supports through {maximum_leaves} leaves")
    target_counts = target_degree_counts(min(maximum_leaves, 8))
    geometry = generated_frequency_geometry(maximum_leaves)
    progress(show_progress, started, "checked the diagonal/transverse decomposition on every support")

    return {
        "scope": {
            "result": "exact cone-frequency geometry and modewise cancellation input",
            "notClaimed": [
                "closure of the infinite analytic sequence norm",
                "a uniform Taylor remainder bound",
                "a Navier--Stokes regularity or singularity result",
            ],
        },
        "coordinates": {
            "diagonalVector": [1, 1, 1],
            "frequencyForm": "K_delta(c,beta) = delta^-1 c (1,1,1) + beta",
            "rationalLabel": "G(c,beta) = (6c, 3 beta_1, 3 beta_2)",
            "positiveInputLabels": [label_record(value) for value in positive],
            "signedInputLabels": [label_record(value) for value in signed],
        },
        "cubeRepresentation": {
            "a": label_record(a),
            "b": label_record(b),
            "c": label_record(c),
            "basisDeterminant": str(basis_determinant),
            "signedInputsEqualAllIndependentSignChoices": True,
            "exactSupportFormula": {
                "allLabelsAtLeafCountL": "(L + 1)^3",
                "zeroOccursExactlyForEvenL": True,
                "nonzeroModesAtOddL": "(L + 1)^3",
                "nonzeroModesAtEvenL": "(L + 1)^3 - 1",
            },
        },
        "supportProfiles": profiles,
        "nextShellTargetDegreeCounts": target_counts,
        "generatedGeometry": geometry,
        "modewiseCancellationIdentities": {
            "chargedInput": (
                "K_delta(c2,beta2).u1 = (beta2 - (c2/c1) beta1).u1 "
                "when c1 != 0 and K_delta(c1,beta1).u1 = 0"
            ),
            "chargeZeroInputBound": (
                "|K_delta(c2,beta2).u1| <= |beta2||u1| + |c2| L_delta(u1)"
            ),
            "longitudinalSeminorm": "L_delta(u) = delta^-1 |(1,1,1).u|",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "git": git_source_state(),
        "wallSeconds": time.perf_counter() - started,
    }


def validate(result: dict[str, object]) -> None:
    cube = result["cubeRepresentation"]
    assert cube["basisDeterminant"] != "0"
    assert cube["signedInputsEqualAllIndependentSignChoices"] is True
    for profile in result["supportProfiles"]:
        assert profile["allLabelCount"] == profile["expectedAllLabelCount"]
        assert profile["containsZero"] == profile["expectedContainsZero"]
        assert profile["nonzeroModeCount"] == profile["expectedNonzeroModeCount"]
    target_counts = {
        record["leaves"]: record["signedMultiplicityDegreeCount"]
        for record in result["nextShellTargetDegreeCounts"]
    }
    assert [target_counts[leaves] for leaves in range(1, 9)] == [0, 0, 0, 0, 0, 3, 0, 14]
    geometry = result["generatedGeometry"]
    assert geometry["leadingVectorsAreDiagonal"] is True
    assert geometry["offsetsAreTransverse"] is True
    assert geometry["dimensionlessHeatCrossTermsAreZero"] is True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-leaves", type=int, default=DEFAULT_MAXIMUM_LEAVES)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    if arguments.maximum_leaves < 8:
        parser.error("--maximum-leaves must be at least 8 to validate target reachability")
    result = audit(arguments.maximum_leaves, arguments.progress)
    if arguments.check:
        validate(result)
    serialized = json.dumps(
        result,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=True,
    )
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n")
    print(serialized)


if __name__ == "__main__":
    main()
