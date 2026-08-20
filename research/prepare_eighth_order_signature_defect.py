#!/usr/bin/env python3
"""Prepare exact compressed data for the R0.68B-2h signature defect."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import gmpy2
import numpy as np

import eighth_order_heat_defect_pilot as defect
import eighth_order_heat_jet_pilot as jet


MAXIMUM_DEGREE = 10
DERIVATIVE_ORDER = 11
EXPECTED_CLASSES = 44_514
EXPECTED_SHIFTS = 16**6

sys.set_int_max_str_digits(100_000)


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


def rational_record(value: Fraction) -> dict[str, str]:
    canonical = f"{value.numerator}/{value.denominator}"
    with gmpy2.context(gmpy2.get_context(), precision=256):
        decimal = format(
            gmpy2.mpfr(value.numerator) / gmpy2.mpfr(value.denominator),
            ".42g",
        )
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": decimal,
        "sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest(),
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_payload_manifest(directory: Path) -> dict[str, object]:
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
    }


def write_csr(directory: Path, matrix: object) -> dict[str, int]:
    matrix = matrix.tocsr()
    matrix.sum_duplicates()
    matrix.sort_indices()
    matrix.indptr.astype("<i8").tofile(directory / "absolute-cycle.indptr.i64")
    matrix.indices.astype("<i4").tofile(directory / "absolute-cycle.indices.i32")
    if np.max(matrix.data, initial=0) >= 2**31:
        raise AssertionError("absolute-path cycle exceeds int32")
    matrix.data.astype("<i4").tofile(directory / "absolute-cycle.data.i32")
    return {
        "rows": int(matrix.shape[0]),
        "columns": int(matrix.shape[1]),
        "nonzeros": int(matrix.nnz),
        "maximumEntry": int(np.max(matrix.data, initial=0)),
        "maximumRowSum": int(np.max(np.asarray(matrix.sum(axis=1)))),
    }


def state_table() -> np.ndarray:
    output = np.empty((64, 14), dtype="<i4")
    for lsb_code in range(64):
        epsilon = defect.free_lsb_epsilon(lsb_code)
        output[lsb_code] = [
            defect.r068.state_index(0, epsilon + dependent_lsb, carry)
            for dependent_lsb in (0, 1)
            for carry in defect.r068.CARRIES
        ]
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    output = arguments.output
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"refusing to reuse nonempty directory {output}")
    output.mkdir(parents=True, exist_ok=True)

    upper = defect.upper_digit_table()
    transfers = [
        defect.r068.signed_digit_transfer(0),
        defect.r068.signed_digit_transfer(1),
    ]
    cross_checks = defect.signature_cross_checks(upper, transfers)
    if not all(record["agreesWithSparseCycleEntries"] for record in cross_checks):
        raise AssertionError("signature spot check failed")
    absolute_transfers = []
    for transfer in transfers:
        absolute = transfer.copy()
        absolute.data = np.abs(absolute.data)
        absolute_transfers.append(absolute)
    absolute_cycle_metadata = write_csr(
        output,
        defect.r068.cycle_matrix(absolute_transfers),
    )

    indptr = [0]
    shells: list[int] = []
    signatures: list[np.ndarray] = []
    multiplicities: list[int] = []
    for lsb_code in range(64):
        shell, signature = defect.signature_table(lsb_code, upper)
        keyed = np.concatenate([shell[:, None], signature], axis=1)
        unique, counts = np.unique(keyed, axis=0, return_counts=True)
        shells.extend(int(value) for value in unique[:, 0])
        signatures.extend(unique[:, 1:].astype(np.int8))
        multiplicities.extend(int(value) for value in counts)
        indptr.append(len(shells))
    signature_array = np.asarray(signatures, dtype="i1")
    if len(shells) != EXPECTED_CLASSES:
        raise AssertionError(f"unexpected class count {len(shells)}")
    if sum(multiplicities) != EXPECTED_SHIFTS:
        raise AssertionError("compressed multiplicities do not cover all shifts")
    if int(np.max(np.abs(signature_array))) != 1:
        raise AssertionError("signature entries are not zero or unit")
    np.asarray(indptr, dtype="<i8").tofile(output / "class.indptr.i64")
    np.asarray(shells, dtype="u1").tofile(output / "class.shell.u8")
    signature_array.tofile(output / "class.signature.i8")
    np.asarray(multiplicities, dtype="<i8").tofile(
        output / "class.multiplicity.i64"
    )
    state_table().tofile(output / "state-by-lsb.i32")

    indices = jet.multiindices(MAXIMUM_DEGREE)
    channel_factors = []
    coarse_factors = []
    for alpha in indices:
        degree = sum(alpha)
        factor = Fraction(
            1,
            math.prod(math.factorial(value) for value in alpha) * 16**degree,
        )
        channel_factors.append(double_double_interval(factor, factor))
        coarse = (
            factor
            * Fraction(45, 16) ** (DERIVATIVE_ORDER - degree)
            / math.factorial(DERIVATIVE_ORDER - degree)
        )
        coarse_factors.append(double_double_interval(coarse, coarse))
    np.asarray(channel_factors, dtype="<f8").tofile(
        output / "channel-factor-hi-lo-radius.f64"
    )
    np.asarray(coarse_factors, dtype="<f8").tofile(
        output / "coarse-channel-factor-hi-lo-radius.f64"
    )

    class_degree_factors = np.empty((EXPECTED_CLASSES, 11, 3), dtype="<f8")
    for class_index, (shell, multiplicity) in enumerate(
        zip(shells, multiplicities, strict=True)
    ):
        for degree in range(11):
            exponent = DERIVATIVE_ORDER - degree
            factor = (
                multiplicity
                * Fraction(shell, 32) ** exponent
                / math.factorial(exponent)
            )
            class_degree_factors[class_index, degree] = double_double_interval(
                factor,
                factor,
            )
    class_degree_factors.tofile(
        output / "class-degree-factor-hi-lo-radius.f64"
    )

    derivative_path = (
        Path(__file__).resolve().parent
        / "certificates/r068b2d-exact/eighth-order-heat-derivative-exact.json"
    )
    derivative_report = json.loads(derivative_path.read_text())
    derivative_value = derivative_report["derivativeMajorant"]["maximumUpper"]
    derivative_upper = Fraction(
        int(derivative_value["numerator"]),
        int(derivative_value["denominator"]),
    )
    np.asarray([fraction_up(derivative_upper)], dtype="<f8").tofile(
        output / "derivative-upper.f64"
    )

    _carry_cycle, carry_metadata = defect.exact_absolute_carry_data()
    payload_manifest = write_payload_manifest(output)
    signature_digest = hashlib.sha256()
    for name in (
        "class.indptr.i64",
        "class.shell.u8",
        "class.signature.i8",
        "class.multiplicity.i64",
        "state-by-lsb.i32",
    ):
        signature_digest.update((output / name).read_bytes())
    metadata = {
        "schemaVersion": "1.0",
        "maximumDegree": MAXIMUM_DEGREE,
        "derivativeOrder": DERIVATIVE_ORDER,
        "channels": len(indices),
        "signatureClasses": len(shells),
        "coveredFreeShifts": sum(multiplicities),
        "maximumAbsoluteSignatureEntry": int(np.max(np.abs(signature_array))),
        "maximumSignatureNonzeros": int(
            np.max(np.count_nonzero(signature_array, axis=1))
        ),
        "signatureBundleSha256": signature_digest.hexdigest(),
        "signatureSpotChecks": cross_checks,
        "absoluteCarry": carry_metadata,
        "absolutePathCycle": absolute_cycle_metadata,
        "derivativeUpper": rational_record(derivative_upper),
        "derivativeCertificateSha256": sha256_file(derivative_path),
        "payloadManifest": payload_manifest,
        "boundary": (
            "The bundle contains exact combinatorial signatures and outward "
            "binary64 double-double enclosures of positive rational weights."
        ),
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
