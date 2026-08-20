#!/usr/bin/env python3
"""Prepare exact sparse data for the R0.68B-2f binary128 moment engine."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

import eighth_order_cycle_audit as cycle_audit
import eighth_order_dominant_mass_exact_audit as mass_audit
import eighth_order_heat_jet_pilot as pilot


ROOT_BISECTIONS = 192
LENGTHS = (1, 2, 4, 8)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_payload_manifest(directory: Path) -> dict[str, object]:
    """Bind every generated binary payload before metadata is written."""
    excluded = {"metadata.json", "payload-manifest.sha256"}
    paths = sorted(
        path for path in directory.iterdir()
        if path.is_file() and path.name not in excluded
    )
    lines = [
        f"{sha256_file(path)}  {path.stat().st_size}  {path.name}"
        for path in paths
    ]
    payload = ("\n".join(lines) + "\n").encode()
    (directory / "payload-manifest.sha256").write_bytes(payload)
    return {
        "fileCount": len(paths),
        "totalBytes": sum(path.stat().st_size for path in paths),
        "manifestSha256": hashlib.sha256(payload).hexdigest(),
        "format": "sha256 two-spaces byte-size two-spaces basename newline",
    }


def fraction_up(value: Fraction) -> float:
    output = float(value)
    if Fraction.from_float(output) < value:
        output = math.nextafter(output, math.inf)
    return output


def double_double_interval(
    lower: Fraction,
    upper: Fraction,
) -> tuple[float, float, float]:
    midpoint = (lower + upper) / 2
    high = float(midpoint)
    low = float(midpoint - Fraction.from_float(high))
    approximation = Fraction.from_float(high) + Fraction.from_float(low)
    radius = max(approximation - lower, upper - approximation)
    return high, low, fraction_up(radius)


def write_array(directory: Path, name: str, values: np.ndarray) -> None:
    values.tofile(directory / name)


def write_csr(
    directory: Path,
    stem: str,
    matrix: object,
    data_dtype: object,
) -> dict[str, int]:
    matrix = matrix.tocsr()
    matrix.sum_duplicates()
    matrix.sort_indices()
    write_array(directory, f"{stem}.indptr.i64", matrix.indptr.astype("<i8"))
    write_array(directory, f"{stem}.indices.i32", matrix.indices.astype("<i4"))
    write_array(directory, f"{stem}.data", matrix.data.astype(data_dtype))
    return {
        "rows": int(matrix.shape[0]),
        "columns": int(matrix.shape[1]),
        "nonzeros": int(matrix.nnz),
    }


def flattened_channel_terms(
    indices: list[tuple[int, ...]],
    length: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    operators = pilot.channel_translation_operators(indices, length)
    by_target: list[list[tuple[int, int, int]]] = [
        [] for _ in range(len(indices))
    ]
    for mask, record in enumerate(operators):
        if record is None:
            continue
        sources, operator = record
        operator = operator.tocsr()
        for target in range(len(indices)):
            for position in range(
                int(operator.indptr[target]),
                int(operator.indptr[target + 1]),
            ):
                source = int(sources[int(operator.indices[position])])
                coefficient = int(operator.data[position])
                if float(coefficient) != float(operator.data[position]):
                    raise AssertionError("channel coefficient is not integral")
                by_target[target].append((source, mask, coefficient))
    indptr = [0]
    sources_output: list[int] = []
    masks_output: list[int] = []
    coefficients_output: list[int] = []
    for records in by_target:
        records.sort()
        for source, mask, coefficient in records:
            sources_output.append(source)
            masks_output.append(mask)
            coefficients_output.append(coefficient)
        indptr.append(len(sources_output))
    return (
        np.asarray(indptr, dtype="<i8"),
        np.asarray(sources_output, dtype="<i4"),
        np.asarray(masks_output, dtype="u1"),
        np.asarray(coefficients_output, dtype="<i8"),
    )


def centering_terms(
    indices: list[tuple[int, ...]],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    index_map = {alpha: index for index, alpha in enumerate(indices)}
    indptr = [0]
    sources: list[int] = []
    numerators: list[int] = []
    exponents: list[int] = []
    for alpha in indices:
        records = []
        for beta in np.ndindex(*(value + 1 for value in alpha)):
            difference = sum(
                alpha[coordinate] - beta[coordinate]
                for coordinate in range(pilot.VARIABLES)
            )
            numerator = (-1) ** difference
            for coordinate in range(pilot.VARIABLES):
                numerator *= math.comb(alpha[coordinate], beta[coordinate])
            records.append((index_map[tuple(beta)], numerator, difference))
        records.sort()
        for source, numerator, exponent in records:
            sources.append(source)
            numerators.append(numerator)
            exponents.append(exponent)
        indptr.append(len(sources))
    return (
        np.asarray(indptr, dtype="<i8"),
        np.asarray(sources, dtype="<i4"),
        np.asarray(numerators, dtype="<i4"),
        np.asarray(exponents, dtype="u1"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    output = arguments.output
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(
            f"refusing to mix a new payload with existing files in {output}"
        )
    output.mkdir(parents=True, exist_ok=True)

    transfers = [
        cycle_audit.signed_digit_transfer(0),
        cycle_audit.signed_digit_transfer(1),
    ]
    exact_cycle = cycle_audit.cycle_matrix(transfers)
    cycle_metadata = write_csr(output, "cycle", exact_cycle, "<i2")

    subset_metadata: dict[str, object] = {}
    for bit in (0, 1):
        groups = pilot.digit_edge_groups(bit)
        matrices = pilot.subset_transfer_matrices(groups)
        subset_metadata[str(bit)] = []
        for mask, matrix in enumerate(matrices):
            metadata = write_csr(
                output,
                f"subset-b{bit}-m{mask:02d}",
                matrix,
                "i1",
            )
            subset_metadata[str(bit)].append(metadata)

    indices = pilot.multiindices(10)
    write_array(output, "multiindices.i8", np.asarray(indices, dtype="i1"))
    channel_metadata = {}
    for length in LENGTHS:
        indptr, sources, masks, coefficients = flattened_channel_terms(
            indices,
            length,
        )
        stem = f"channel-l{length}"
        write_array(output, f"{stem}.indptr.i64", indptr)
        write_array(output, f"{stem}.sources.i32", sources)
        write_array(output, f"{stem}.masks.u8", masks)
        write_array(output, f"{stem}.coefficients.i64", coefficients)
        channel_metadata[str(length)] = {
            "records": int(len(sources)),
            "maximumAbsoluteCoefficient": int(
                np.max(np.abs(coefficients), initial=0)
            ),
        }

    (
        centre_indptr,
        centre_sources,
        centre_numerators,
        centre_exponents,
    ) = centering_terms(indices)
    write_array(output, "centering.indptr.i64", centre_indptr)
    write_array(output, "centering.sources.i32", centre_sources)
    write_array(output, "centering.numerators.i32", centre_numerators)
    write_array(output, "centering.exponents.u8", centre_exponents)

    root_interval, _root_values = mass_audit.refined_root_interval(
        ROOT_BISECTIONS
    )
    mass_lowers, mass_uppers, mass_metadata = (
        mass_audit.dominant_mass_intervals(root_interval)
    )
    root_parts = np.asarray(
        double_double_interval(*root_interval),
        dtype="<f8",
    )
    write_array(output, "root-hi-lo-radius.f64", root_parts)
    mass_parts = np.asarray(
        [
            double_double_interval(lower, upper)
            for lower, upper in zip(mass_lowers, mass_uppers, strict=True)
        ],
        dtype="<f8",
    )
    write_array(output, "mass-hi-lo-radius.f64", mass_parts)

    payload_manifest = write_payload_manifest(output)
    metadata = {
        "schemaVersion": "1.0",
        "stateDimension": cycle_audit.DIMENSION,
        "maximumDegree": 10,
        "channelsByDegree": [
            len(pilot.multiindices(degree)) for degree in range(11)
        ],
        "cycle": cycle_metadata,
        "subsetMatrices": subset_metadata,
        "channelOperators": channel_metadata,
        "centeringRecords": int(len(centre_sources)),
        "rootBisections": ROOT_BISECTIONS,
        "dominantMassIntervalVectorSha256": (
            mass_metadata["canonicalIntervalVectorSha256"]
        ),
        "rootDoubleDoubleRadius": float(root_parts[2]),
        "maximumMassDoubleDoubleRadius": float(np.max(mass_parts[:, 2])),
        "payloadManifest": payload_manifest,
        "dataBoundary": (
            "All transfer coefficients are exact integers. Root and mass "
            "centres are binary64 double-double expansions with outward "
            "binary64 radii derived from exact rational intervals."
        ),
    }
    (output / "metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
