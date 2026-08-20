#!/usr/bin/env python3
"""Exact-moment and rational-interval audit for the R0.65 weighted cycle.

For M=16^r and q=2(M-1)/15, the script evaluates the complete quartic
simplex coefficient S4 at the target m=q+1.  The carrier moments are exact
integers.  The simplex Taylor polynomial and its remainder are enclosed with
Fraction arithmetic, including a rational enclosure of T=log(2)/2.

The output certifies finitely many specified scales.  It does not turn those
finite inequalities into an asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


CARRIES = (-1, 0, 1)
WORD = (0, 1, 0, 0)
ALPHA_BOUND = Fraction(75, 8)

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def state_index(target_state: int, cubic_state: int, carry: int) -> int:
    return (target_state * 8 + cubic_state) * 3 + CARRIES.index(carry)


def zero_array(degree: int) -> list[list[int]]:
    return [[0] * (degree + 1) for _ in range(degree + 1)]


def translate_moments(
    source: list[list[int]], degree: int, shift_a: int, shift_b: int
) -> list[list[int]]:
    """Translate raw moments under (a,b)->(a+shift_a,b+shift_b)."""
    if shift_a == 0 and shift_b == 0:
        return [row[:] for row in source]
    current = source
    if shift_a:
        after_a = zero_array(degree)
        for j in range(degree + 1):
            for i in range(degree - j + 1):
                after_a[i][j] = sum(
                    math.comb(i, u) * shift_a ** (i - u) * current[u][j]
                    for u in range(i + 1)
                )
        current = after_a
    if shift_b:
        after_b = zero_array(degree)
        for i in range(degree + 1):
            for j in range(degree - i + 1):
                after_b[i][j] = sum(
                    math.comb(j, v) * shift_b ** (j - v) * current[i][v]
                    for v in range(j + 1)
                )
        current = after_b
    return current


def advance_moments(
    states: list[list[list[int]]], degree: int, length: int, bit: int
) -> list[list[list[int]]]:
    """Apply one target digit with exact binomial moment transport."""
    output = [zero_array(degree) for _ in range(48)]
    for epsilon in range(8):
        epsilon_a = (epsilon >> 2) & 1
        epsilon_b = (epsilon >> 1) & 1
        epsilon_c = epsilon & 1
        coefficient_shift = epsilon_a + epsilon_b - epsilon_c
        for child_carry in CARRIES:
            numerator = child_carry - bit + coefficient_shift
            if numerator % 2:
                continue
            parent_carry = numerator // 2
            if parent_carry not in CARRIES:
                continue
            source = states[state_index(bit, epsilon, child_carry)]
            moved = translate_moments(
                source,
                degree,
                epsilon_a * length,
                epsilon_b * length,
            )
            for target_state in (0, 1):
                for cubic_state in range(8):
                    parity = (
                        target_state * bit
                        + bin(cubic_state & epsilon).count("1")
                    )
                    sign = -1 if parity % 2 else 1
                    target = output[
                        state_index(target_state, cubic_state, parent_carry)
                    ]
                    for i in range(degree + 1):
                        target_row = target[i]
                        moved_row = moved[i]
                        for j in range(degree - i + 1):
                            target_row[j] += sign * moved_row[j]
    return output


Polynomial = dict[tuple[int, int], int]


def polynomial_add(*polynomials: Polynomial) -> Polynomial:
    output: Polynomial = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            output[monomial] = output.get(monomial, 0) + coefficient
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient
    }


def polynomial_scale(polynomial: Polynomial, scalar: int) -> Polynomial:
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def polynomial_multiply(
    left: Polynomial, right: Polynomial, degree: int
) -> Polynomial:
    output: Polynomial = {}
    for (i, j), left_value in left.items():
        for (u, v), right_value in right.items():
            if i + j + u + v > degree:
                continue
            monomial = (i + u, j + v)
            output[monomial] = (
                output.get(monomial, 0) + left_value * right_value
            )
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient
    }


def linear_polynomial(constant: int, a: int = 0, b: int = 0) -> Polynomial:
    output = {(0, 0): constant}
    if a:
        output[(1, 0)] = a
    if b:
        output[(0, 1)] = b
    return output


def square(polynomial: Polynomial) -> Polynomial:
    return polynomial_multiply(polynomial, polynomial, 2)


def rate_polynomials(
    length: int, target: int
) -> list[tuple[Polynomial, Polynomial, Polynomial]]:
    """Return H^2(alpha_0,alpha_1,alpha_2) for the three path orders."""
    carrier_q = 4 * length + target
    carrier_a = linear_polynomial(4 * length, a=1)
    carrier_b = linear_polynomial(4 * length, b=1)
    carrier_c = linear_polynomial(4 * length - target, a=1, b=1)
    a_minus_q = linear_polynomial(-target, a=1)
    q_plus_c = linear_polynomial(8 * length, a=1, b=1)
    alpha_zero = polynomial_add(
        {(0, 0): carrier_q * carrier_q},
        square(carrier_a),
        square(carrier_b),
        square(carrier_c),
    )
    alpha_one_first = polynomial_add(
        square(a_minus_q), square(carrier_b), square(carrier_c)
    )
    alpha_one_third = polynomial_add(
        square(q_plus_c), square(carrier_a), square(carrier_b)
    )
    return [
        (alpha_zero, alpha_one_first, polynomial_scale(square(carrier_c), 2)),
        (alpha_zero, alpha_one_first, polynomial_scale(square(carrier_b), 2)),
        (alpha_zero, alpha_one_third, polynomial_scale(square(carrier_b), 2)),
    ]


def complete_homogeneous_sequence(
    rates: tuple[Polynomial, Polynomial, Polynomial], order: int
) -> list[Polynomial]:
    """Compute h_n(alpha_0,alpha_1,alpha_2), n<=order."""
    alpha_zero, alpha_one, alpha_two = rates
    max_degree = 2 * order
    elementary_one = polynomial_add(alpha_zero, alpha_one, alpha_two)
    elementary_two = polynomial_add(
        polynomial_multiply(alpha_zero, alpha_one, max_degree),
        polynomial_multiply(alpha_zero, alpha_two, max_degree),
        polynomial_multiply(alpha_one, alpha_two, max_degree),
    )
    elementary_three = polynomial_multiply(
        polynomial_multiply(alpha_zero, alpha_one, max_degree),
        alpha_two,
        max_degree,
    )
    sequence: list[Polynomial] = [{(0, 0): 1}]
    for index in range(1, order + 1):
        value = polynomial_multiply(
            elementary_one, sequence[index - 1], max_degree
        )
        if index >= 2:
            value = polynomial_add(
                value,
                polynomial_scale(
                    polynomial_multiply(
                        elementary_two, sequence[index - 2], max_degree
                    ),
                    -1,
                ),
            )
        if index >= 3:
            value = polynomial_add(
                value,
                polynomial_multiply(
                    elementary_three, sequence[index - 3], max_degree
                ),
            )
        sequence.append(value)
    return sequence


def moment_functional(
    polynomial: Polynomial, moments: list[list[int]]
) -> int:
    return sum(
        coefficient * moments[i][j]
        for (i, j), coefficient in polynomial.items()
    )


def time_enclosure(terms: int = 120) -> tuple[Fraction, Fraction]:
    """Enclose T=log(2)/2=atanh(1/3) by an exact positive series."""
    x = Fraction(1, 3)
    lower = sum(
        (x ** (2 * index + 1)) / (2 * index + 1)
        for index in range(terms)
    )
    first_omitted = 2 * terms + 1
    remainder = (
        x**first_omitted
        / first_omitted
        / (1 - x * x)
    )
    return lower, lower + remainder


def interval_polynomial(
    coefficients: list[Fraction],
    time_lower: Fraction,
    time_upper: Fraction,
) -> tuple[Fraction, Fraction]:
    lower = Fraction(0)
    upper = Fraction(0)
    for index, coefficient in enumerate(coefficients):
        power = index + 3
        if coefficient >= 0:
            lower += coefficient * time_lower**power
            upper += coefficient * time_upper**power
        else:
            lower += coefficient * time_upper**power
            upper += coefficient * time_lower**power
    return lower, upper


def simplex_tail_bound(
    order: int, length: int, time_upper: Fraction
) -> Fraction:
    """Bound all omitted Taylor terms over all at most 3 M^2 paths."""
    z = ALPHA_BOUND * time_upper
    ratio = z / (order + 2)
    if ratio >= 1:
        raise ValueError("Taylor order is too small for the geometric tail")
    first = (
        time_upper**3
        / 2
        * z ** (order + 1)
        / (math.factorial(order + 1) * (order + 4))
    )
    return 3 * length * length * first / (1 - ratio)


def fraction_decimal(value: Fraction, digits: int = 42) -> str:
    with localcontext() as context:
        context.prec = digits
        decimal = Decimal(value.numerator) / Decimal(value.denominator)
        return format(decimal, ".34E")


def fraction_hash(value: Fraction) -> str:
    encoded = f"{value.numerator}/{value.denominator}".encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def absolute_interval(
    lower: Fraction, upper: Fraction
) -> tuple[Fraction, Fraction]:
    if lower <= 0 <= upper:
        return Fraction(0), max(-lower, upper)
    return min(abs(lower), abs(upper)), max(abs(lower), abs(upper))


def evaluate_scale(
    length: int,
    target: int,
    moments: list[list[int]],
    order: int,
    time_lower: Fraction,
    time_upper: Fraction,
) -> tuple[dict[str, object], tuple[Fraction, Fraction]]:
    sequences = [
        complete_homogeneous_sequence(rates, order)
        for rates in rate_polynomials(length, target)
    ]
    integer_coefficients = [
        sum(moment_functional(sequence[index], moments) for sequence in sequences)
        for index in range(order + 1)
    ]
    high = 4 * length
    coefficients = [
        Fraction(
            (-1) ** index * value,
            high ** (2 * index) * math.factorial(index + 3),
        )
        for index, value in enumerate(integer_coefficients)
    ]
    partial_lower, partial_upper = interval_polynomial(
        coefficients, time_lower, time_upper
    )
    tail = simplex_tail_bound(order, length, time_upper)
    lower = partial_lower - tail
    upper = partial_upper + tail
    center = (lower + upper) / 2
    abs_lower, abs_upper = absolute_interval(lower, upper)
    record: dict[str, object] = {
        "M": length,
        "q": target,
        "m": target + 1,
        "J0": integer_coefficients[0],
        "unweightedTarget": moments[0][0],
        "intervalLower": fraction_decimal(lower),
        "intervalUpper": fraction_decimal(upper),
        "intervalLowerSha256": fraction_hash(lower),
        "intervalUpperSha256": fraction_hash(upper),
        "centerDisplayOnly": fraction_decimal(center),
        "tailBound": fraction_decimal(tail),
        "relativeTailDisplayOnly": fraction_decimal(tail / abs(center)),
        "S4OverMCenterDisplayOnly": fraction_decimal(center / length),
        "signCertified": "positive" if lower > 0 else "negative" if upper < 0 else "unresolved",
        "absoluteLower": fraction_decimal(abs_lower),
        "absoluteUpper": fraction_decimal(abs_upper),
    }
    return record, (lower, upper)


def initial_states(degree: int) -> list[list[list[int]]]:
    states = [zero_array(degree) for _ in range(48)]
    for target_state in (0, 1):
        for cubic_state in range(8):
            states[state_index(target_state, cubic_state, 0)][0][0] = 1
    return states


def rudin_shapiro_pair(level: int) -> tuple[list[int], list[int]]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p, q


def direct_moment_states(
    level: int, target: int, degree: int
) -> list[list[list[int]]]:
    length = 1 << level
    pair = rudin_shapiro_pair(level)
    output = [zero_array(degree) for _ in range(48)]
    for target_state in (0, 1):
        target_sign = pair[target_state][target]
        for cubic_state in range(8):
            signs_a = pair[(cubic_state >> 2) & 1]
            signs_b = pair[(cubic_state >> 1) & 1]
            signs_c = pair[cubic_state & 1]
            for carry in CARRIES:
                moments = output[state_index(target_state, cubic_state, carry)]
                exponent = target + carry * length
                for a in range(length):
                    for b in range(length):
                        c = a + b - exponent
                        if not 0 <= c < length:
                            continue
                        sign = target_sign * signs_a[a] * signs_b[b] * signs_c[c]
                        for i in range(degree + 1):
                            for j in range(degree - i + 1):
                                moments[i][j] += sign * a**i * b**j
    return output


def direct_moment_audit(max_level: int = 6, degree: int = 4) -> list[dict[str, int]]:
    states = initial_states(degree)
    length = 1
    records: list[dict[str, int]] = []
    for level in range(1, max_level + 1):
        bit = WORD[(level - 1) % 4]
        states = advance_moments(states, degree, length, bit)
        length *= 2
        target = sum(
            WORD[index % 4] << index for index in range(level)
        )
        direct = direct_moment_states(level, target, degree)
        if states != direct:
            raise AssertionError(f"moment transfer mismatch at level {level}")
        records.append(
            {
                "level": level,
                "M": length,
                "q": target,
                "states": 48,
                "momentsPerState": (degree + 1) * (degree + 2) // 2,
            }
        )
    return records


def load_probes(paths: list[Path]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        records.append(
            {
                "path": str(path),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "M": int(payload["M"]),
                "target": int(payload["target"]),
                "S4": str(payload["dimensionlessQuarticKernelSum"]),
                "condition": str(payload["cancellationConditionNumber"]),
                "classification": payload["classification"],
            }
        )
    records.sort(key=lambda record: int(record["M"]))
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-r", type=int, default=24)
    parser.add_argument("--order", type=int, default=48)
    parser.add_argument("--time-series-terms", type=int, default=120)
    parser.add_argument(
        "--profile", choices=("publication", "quick"), default="publication"
    )
    parser.add_argument("--probe", type=Path, action="append", default=[])
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if arguments.profile == "publication":
        if arguments.max_r < 24:
            raise ValueError("publication profile requires max-r at least 24")
        if arguments.order < 48:
            raise ValueError("publication profile requires order at least 48")
    elif arguments.max_r < 2 or arguments.order < 20:
        raise ValueError("quick profile requires max-r at least 2 and order at least 20")
    started = time.perf_counter()
    time_lower, time_upper = time_enclosure(arguments.time_series_terms)
    degree = 2 * arguments.order
    states = initial_states(degree)
    length = 1
    scale_records: list[dict[str, object]] = []
    intervals: list[tuple[Fraction, Fraction]] = []
    for level in range(1, 4 * arguments.max_r + 1):
        bit = WORD[(level - 1) % 4]
        states = advance_moments(states, degree, length, bit)
        length *= 2
        if level % 4:
            continue
        r = level // 4
        target = 2 * (length - 1) // 15
        moments = states[state_index(0, 0, 0)]
        record, interval = evaluate_scale(
            length,
            target,
            moments,
            arguments.order,
            time_lower,
            time_upper,
        )
        record["r"] = r
        if intervals:
            previous_abs = absolute_interval(*intervals[-1])
            current_abs = absolute_interval(*interval)
            ratio_lower = current_abs[0] / previous_abs[1]
            ratio_upper = current_abs[1] / previous_abs[0]
            record["absoluteBlockRatioLower"] = fraction_decimal(ratio_lower)
            record["absoluteBlockRatioUpper"] = fraction_decimal(ratio_upper)
        scale_records.append(record)
        intervals.append(interval)
        if arguments.progress:
            print(
                f"[R0.65 +{time.perf_counter()-started:8.2f}s] "
                f"r={r:02d}/{arguments.max_r} M=16^{r} "
                f"sign={record['signCertified']} "
                f"S4/M={record['S4OverMCenterDisplayOnly']}",
                file=sys.stderr,
                flush=True,
            )

    direct_records = direct_moment_audit()
    probes = load_probes(arguments.probe)
    interval_by_length = {
        int(record["M"]): interval
        for record, interval in zip(scale_records, intervals)
    }
    probe_residuals: list[Fraction] = []
    for probe in probes:
        probe_value = Fraction(str(probe["S4"]))
        lower, upper = interval_by_length[int(probe["M"])]
        center = (lower + upper) / 2
        residual = abs(probe_value - center) / abs(center)
        probe["relativeResidualAgainstExactCenterDisplayOnly"] = fraction_decimal(
            residual
        )
        probe_residuals.append(residual)
    signs = [str(record["signCertified"]) for record in scale_records]
    supercritical_indices = []
    for index in range(1, len(intervals)):
        previous_abs = absolute_interval(*intervals[index - 1])
        current_abs = absolute_interval(*intervals[index])
        if current_abs[0] / previous_abs[1] > 16:
            supercritical_indices.append(index + 1)
    last_lower, last_upper = intervals[-1]
    last_abs = absolute_interval(last_lower, last_upper)
    previous_abs = absolute_interval(*intervals[-2])
    final_ratio = (
        last_abs[0] / previous_abs[1],
        last_abs[1] / previous_abs[0],
    )
    checks: dict[str, bool] = {
        "logTwoOverTwoHasExactRationalEnclosure": time_lower < time_upper,
        "momentTransferMatchesDirectAllStateEnumeration": len(direct_records) == 6,
        "zerothTaylorCoefficientIsThreeTimesUnweightedTarget": all(
            int(record["J0"]) == 3 * int(record["unweightedTarget"])
            for record in scale_records
        ),
        "allPublishedScaleIntervalsExcludeZero": all(
            lower > 0 or upper < 0 for lower, upper in intervals
        ),
        "probeInputsRemainExplicitlyFinitePrecision": all(
            "not a proof" in str(record["classification"]) for record in probes
        ),
    }
    if arguments.profile == "publication":
        checks.update(
            {
                "firstCertifiedSignChangeOccursAtR14": signs[:13]
                == ["positive"] * 13
                and signs[13:] == ["negative"] * (len(signs) - 13),
                "tenConsecutiveCertifiedSupercriticalBlocksR15ThroughR24": all(
                    index in supercritical_indices for index in range(15, 25)
                ),
                "finalNormalizedMagnitudeExceedsOne": last_abs[0] > length,
                "finalBlockRatioLiesBetween25Point29And25Point30": Fraction(
                    2529, 100
                )
                < final_ratio[0]
                and final_ratio[1] < Fraction(2530, 100),
                "finalRelativeTailBelowTwoTimesTenToMinusTwelve": simplex_tail_bound(
                    arguments.order, length, time_upper
                )
                / last_abs[0]
                < Fraction(2, 10**12),
                "fourIndependentLongDoubleProbesAgreeWithinOnePartInTenToTwelve": len(
                    probe_residuals
                )
                == 4
                and max(probe_residuals) < Fraction(1, 10**12),
            }
        )
    else:
        checks["quickProfileDoesNotClaimThePublicationScaleResult"] = (
            arguments.max_r < 24
        )
    if not all(checks.values()):
        raise AssertionError(checks)

    key_exact: dict[str, object] = {}
    exact_indices = (
        (14, 15, arguments.max_r)
        if arguments.profile == "publication"
        else (arguments.max_r,)
    )
    for r in exact_indices:
        lower, upper = intervals[r - 1]
        key_exact[f"r{r}"] = {
            "lowerNumerator": str(lower.numerator),
            "lowerDenominator": str(lower.denominator),
            "upperNumerator": str(upper.numerator),
            "upperDenominator": str(upper.denominator),
        }
    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "profile": arguments.profile,
        "classification": (
            "exact integer moment transport and exact rational Taylor enclosure at "
            "finitely many specified scales; not an asymptotic proof that |S4,m|/M "
            "is unbounded and not a Navier-Stokes regularity result"
        ),
        "checks": checks,
        "targetFamily": {
            "L": 1,
            "M": "16^r",
            "q": "2(16^r-1)/15",
            "m": "q+1",
            "wordLeastSignificantBitFirst": list(WORD),
        },
        "exactMomentTransport": {
            "states": 48,
            "rawMomentVariables": ["a", "b"],
            "maximumTotalDegree": degree,
            "directAudit": direct_records,
        },
        "simplexSeries": {
            "order": arguments.order,
            "timeSeriesTerms": arguments.time_series_terms,
            "TIdentity": "T=log(2)/2=atanh(1/3)",
            "TLowerNumerator": str(time_lower.numerator),
            "TLowerDenominator": str(time_lower.denominator),
            "TUpperNumerator": str(time_upper.numerator),
            "TUpperDenominator": str(time_upper.denominator),
            "uniformAlphaBound": "75/8",
            "pathCountBound": "3 M^2",
            "remainderFormula": (
                "3 M^2 (T^3/2) z^(D+1)/((D+1)!(D+4)) "
                "/ (1-z/(D+2)), z=(75/8)T"
            ),
        },
        "scales": scale_records,
        "certifiedSummary": {
            "firstSignChangeR": 14 if arguments.profile == "publication" else None,
            "consecutiveSupercriticalBlocks": (
                [15, arguments.max_r]
                if arguments.profile == "publication"
                else supercritical_indices
            ),
            "finalAbsoluteBlockRatioLower": fraction_decimal(final_ratio[0]),
            "finalAbsoluteBlockRatioUpper": fraction_decimal(final_ratio[1]),
            "finalAbsoluteS4OverMLower": fraction_decimal(last_abs[0] / length),
            "finalAbsoluteS4OverMUpper": fraction_decimal(last_abs[1] / length),
            "finiteInferenceBoundary": (
                "The finite run rules out a factor-at-most-16 claim on every block, "
                "but does not by itself prove asymptotic supercritical growth."
            ),
        },
        "keyExactIntervals": key_exact,
        "independentLongDoubleProbes": probes,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "randomness": False,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(arguments.output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
