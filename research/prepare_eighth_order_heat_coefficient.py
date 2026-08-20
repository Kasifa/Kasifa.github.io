#!/usr/bin/env python3
"""Prepare exact sparse data for the R0.68B-2g heat-coefficient enclosure."""

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

import eighth_order_heat_derivative_exact_audit as derivative
import eighth_order_heat_jet_pilot as jet


MAXIMUM_DEGREE = 10
SERIES_ORDER = 64
TIME_TERMS = 120
SHUFFLES = 35

sys.set_int_max_str_digits(100_000)


def as_fraction(value: gmpy2.mpq) -> Fraction:
    return Fraction(int(gmpy2.numer(value)), int(gmpy2.denom(value)))


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    output = arguments.output
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"refusing to reuse nonempty directory {output}")
    output.mkdir(parents=True, exist_ok=True)

    indices = jet.multiindices(MAXIMUM_DEGREE)
    index_map = {alpha: index for index, alpha in enumerate(indices)}
    betas = jet.multiindices(2)
    beta_map = {alpha: index for index, alpha in enumerate(betas)}
    source_by_target = np.full((len(betas), len(indices)), -1, dtype="<i4")
    for beta_index, beta in enumerate(betas):
        for target_index, alpha in enumerate(indices):
            if all(alpha[i] >= beta[i] for i in range(jet.VARIABLES)):
                source = tuple(alpha[i] - beta[i] for i in range(jet.VARIABLES))
                source_by_target[beta_index, target_index] = index_map[source]
    source_by_target.tofile(output / "beta-source-by-target.i32")

    indptr = [0]
    beta_indices: list[int] = []
    numerators: list[int] = []
    denominators: list[int] = []
    canonical_rates: list[str] = []
    coefficient_l1: list[Fraction] = []
    for word in jet.shuffle_words():
        for rate in derivative.rate_polynomials(word):
            coefficient_l1.append(sum((abs(as_fraction(c)) for c in rate.values()), Fraction()))
            for alpha, coefficient in sorted(rate.items()):
                value = as_fraction(coefficient)
                beta_indices.append(beta_map[alpha])
                numerators.append(value.numerator)
                denominators.append(value.denominator)
                canonical_rates.append(
                    f"{len(indptr)-1}:{','.join(map(str, alpha))}:"
                    f"{value.numerator}/{value.denominator}"
                )
            indptr.append(len(beta_indices))
    if len(indptr) != SHUFFLES * 7 + 1:
        raise AssertionError("unexpected heat-rate count")
    np.asarray(indptr, dtype="<i8").tofile(output / "rate.indptr.i64")
    np.asarray(beta_indices, dtype="u1").tofile(output / "rate.beta.u8")
    np.asarray(numerators, dtype="<i8").tofile(output / "rate.numerator.i64")
    np.asarray(denominators, dtype="<i8").tofile(output / "rate.denominator.i64")

    time_lower_mpq, time_upper_mpq = derivative.time_enclosure(TIME_TERMS)
    time_lower = as_fraction(time_lower_mpq)
    time_upper = as_fraction(time_upper_mpq)
    weights = []
    for order in range(SERIES_ORDER + 1):
        exponent = order + 7
        weights.append(
            double_double_interval(
                time_lower**exponent / math.factorial(exponent),
                time_upper**exponent / math.factorial(exponent),
            )
        )
    np.asarray(weights, dtype="<f8").tofile(
        output / "time-weights-hi-lo-radius.f64"
    )

    maximum_rate_l1 = max(coefficient_l1)
    if maximum_rate_l1 != Fraction(605, 16):
        raise AssertionError(f"unexpected heat-rate L1 maximum {maximum_rate_l1}")
    first = SERIES_ORDER + 1
    first_tail = (
        SHUFFLES
        * math.comb(first + 6, 6)
        * maximum_rate_l1**first
        * time_upper ** (first + 7)
        / math.factorial(first + 7)
    )
    ratio = (
        maximum_rate_l1
        * time_upper
        * Fraction(first + 7, (first + 1) * (first + 8))
    )
    if not 0 < ratio < 1:
        raise AssertionError("tail ratio is not contractive")
    tail_upper = first_tail / (1 - ratio)
    np.asarray([fraction_up(tail_upper)], dtype="<f8").tofile(
        output / "coefficient-tail-upper.f64"
    )

    rate_vector = "\n".join(canonical_rates) + "\n"
    payload_manifest = write_payload_manifest(output)
    metadata = {
        "schemaVersion": "1.0",
        "maximumDegree": MAXIMUM_DEGREE,
        "channels": len(indices),
        "spatialVariables": jet.VARIABLES,
        "shuffleCount": SHUFFLES,
        "ratesPerShuffle": 7,
        "rateTerms": len(beta_indices),
        "seriesOrder": SERIES_ORDER,
        "timeSeriesTerms": TIME_TERMS,
        "timeInterval": {
            "lower": rational_record(time_lower),
            "upper": rational_record(time_upper),
            "width": rational_record(time_upper - time_lower),
        },
        "maximumRateCoefficientL1": rational_record(maximum_rate_l1),
        "tail": {
            "firstOmittedOrder": first,
            "firstTermUpper": rational_record(first_tail),
            "successiveRatioUpper": rational_record(ratio),
            "uniformCoefficientUpper": rational_record(tail_upper),
            "proof": (
                "For seven rates with coefficient L1 norm at most Q, "
                "the L1 norm of h_n is at most binomial(n+6,6) Q^n. "
                "The successive majorant ratio decreases for n>=65."
            ),
        },
        "exactRateVectorSha256": hashlib.sha256(
            rate_vector.encode("ascii")
        ).hexdigest(),
        "payloadManifest": payload_manifest,
    }
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
