#!/usr/bin/env python3
"""Independent Decimal interval validator for the R0.73C monodromy bracket.

This file is intentionally self-contained.  It imports neither the primary
monodromy program nor mpmath.  Directed interval operations use two explicit
``decimal.Context`` objects with ROUND_FLOOR and ROUND_CEILING.  Pi is enclosed
from Machin's identity and alternating arctangent series.  The Rayleigh flow,
Picard tube, normalized Taylor jets, and endpoint bracket are reimplemented
below.

The formal default runtime is CPython 3.12 with decimal 1.70 and libmpdec
4.0.0.  A mismatch fails closed instead of silently producing a certificate
under a different arithmetic kernel.
"""

from __future__ import annotations

import argparse
from decimal import (
    Clamped,
    Context,
    Decimal,
    DivisionByZero,
    FloatOperation,
    InvalidOperation,
    Overflow,
    ROUND_CEILING,
    ROUND_FLOOR,
    Subnormal,
    Underflow,
)
import decimal
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
from typing import Iterable, Sequence


SCHEMA_VERSION = "r073c-independent-decimal-monodromy-v1"
EXPECTED_PYTHON = (3, 12)
EXPECTED_DECIMAL_VERSION = "1.70"
EXPECTED_LIBMPDEC_VERSION = "4.0.0"
DEFAULT_ETA_LOW = "0.3407"
DEFAULT_ETA_HIGH = "0.3410"

CTX_DOWN: Context
CTX_UP: Context
WORKING_PRECISION = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eta-low", default=DEFAULT_ETA_LOW)
    parser.add_argument("--eta-high", default=DEFAULT_ETA_HIGH)
    parser.add_argument("--steps", type=int, default=256)
    parser.add_argument("--order", type=int, default=8)
    parser.add_argument("--precision", type=int, default=80)
    parser.add_argument("--max-picard-attempts", type=int, default=12)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress", type=Path)
    parser.add_argument("--run-id", default="decimal-independent")
    return parser.parse_args()


def configure_arithmetic(precision: int) -> None:
    global CTX_DOWN, CTX_UP, WORKING_PRECISION
    if precision < 70:
        raise ValueError("formal validator requires precision >= 70")
    common = {
        "prec": precision,
        "Emin": -999999999,
        "Emax": 999999999,
        "capitals": 1,
        "clamp": 0,
    }
    CTX_DOWN = Context(rounding=ROUND_FLOOR, **common)
    CTX_UP = Context(rounding=ROUND_CEILING, **common)
    for context in (CTX_DOWN, CTX_UP):
        context.traps[DivisionByZero] = True
        context.traps[InvalidOperation] = True
        context.traps[Overflow] = True
        context.traps[FloatOperation] = True
        context.traps[Underflow] = True
        context.traps[Subnormal] = True
        context.traps[Clamped] = True
        context.clear_flags()
    WORKING_PRECISION = precision


def runtime_checks() -> dict[str, object]:
    actual_python = tuple(sys.version_info[:2])
    actual_decimal = decimal.__version__
    actual_libmpdec = getattr(decimal, "__libmpdec_version__", None)
    checks = {
        "cpython": platform.python_implementation() == "CPython",
        "pythonMajorMinor": actual_python == EXPECTED_PYTHON,
        "decimalVersion": actual_decimal == EXPECTED_DECIMAL_VERSION,
        "libmpdecVersion": actual_libmpdec == EXPECTED_LIBMPDEC_VERSION,
        "primaryNotImported": (
            "research.r073c_interval_monodromy" not in sys.modules
            and "r073c_interval_monodromy" not in sys.modules
        ),
        "mpmathNotImported": not any(
            name == "mpmath" or name.startswith("mpmath.")
            for name in sys.modules
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(f"runtime version/import gate failed: {checks}")
    return {
        "checks": checks,
        "python": platform.python_version(),
        "pythonImplementation": platform.python_implementation(),
        "decimalVersion": actual_decimal,
        "libmpdecVersion": actual_libmpdec,
    }


def decimal_from(value: str | int | Decimal) -> Decimal:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        raise TypeError("booleans are not interval endpoints")
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, str):
        return Decimal(value)
    raise TypeError(f"unsupported Decimal input {type(value)!r}")


class Interval:
    """Closed finite Decimal interval with directed primitive operations."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: Decimal, hi: Decimal) -> None:
        if not (isinstance(lo, Decimal) and isinstance(hi, Decimal)):
            raise TypeError("Interval endpoints must be Decimal")
        if not (lo.is_finite() and hi.is_finite()):
            raise ArithmeticError("non-finite interval endpoint")
        if lo > hi:
            raise ArithmeticError(f"reversed interval [{lo}, {hi}]")
        self.lo = lo
        self.hi = hi

    @classmethod
    def point(cls, value: str | int | Decimal) -> "Interval":
        exact = decimal_from(value)
        return cls(CTX_DOWN.plus(exact), CTX_UP.plus(exact))

    @classmethod
    def bounds(
        cls,
        lower: str | int | Decimal,
        upper: str | int | Decimal,
    ) -> "Interval":
        return cls(
            CTX_DOWN.plus(decimal_from(lower)),
            CTX_UP.plus(decimal_from(upper)),
        )

    @staticmethod
    def coerce(value: "Interval | str | int | Decimal") -> "Interval":
        return value if isinstance(value, Interval) else Interval.point(value)

    def __add__(self, other: "Interval | str | int | Decimal") -> "Interval":
        rhs = self.coerce(other)
        return Interval(
            CTX_DOWN.add(self.lo, rhs.lo),
            CTX_UP.add(self.hi, rhs.hi),
        )

    __radd__ = __add__

    def __neg__(self) -> "Interval":
        return Interval(CTX_DOWN.minus(self.hi), CTX_UP.minus(self.lo))

    def __sub__(self, other: "Interval | str | int | Decimal") -> "Interval":
        rhs = self.coerce(other)
        return Interval(
            CTX_DOWN.subtract(self.lo, rhs.hi),
            CTX_UP.subtract(self.hi, rhs.lo),
        )

    def __rsub__(
        self, other: "Interval | str | int | Decimal"
    ) -> "Interval":
        return self.coerce(other) - self

    def __mul__(self, other: "Interval | str | int | Decimal") -> "Interval":
        rhs = self.coerce(other)
        lows = (
            CTX_DOWN.multiply(self.lo, rhs.lo),
            CTX_DOWN.multiply(self.lo, rhs.hi),
            CTX_DOWN.multiply(self.hi, rhs.lo),
            CTX_DOWN.multiply(self.hi, rhs.hi),
        )
        highs = (
            CTX_UP.multiply(self.lo, rhs.lo),
            CTX_UP.multiply(self.lo, rhs.hi),
            CTX_UP.multiply(self.hi, rhs.lo),
            CTX_UP.multiply(self.hi, rhs.hi),
        )
        return Interval(min(lows), max(highs))

    __rmul__ = __mul__

    def __truediv__(
        self, other: "Interval | str | int | Decimal"
    ) -> "Interval":
        rhs = self.coerce(other)
        if rhs.contains_zero():
            raise ZeroDivisionError(f"interval denominator contains zero: {rhs}")
        lows = (
            CTX_DOWN.divide(self.lo, rhs.lo),
            CTX_DOWN.divide(self.lo, rhs.hi),
            CTX_DOWN.divide(self.hi, rhs.lo),
            CTX_DOWN.divide(self.hi, rhs.hi),
        )
        highs = (
            CTX_UP.divide(self.lo, rhs.lo),
            CTX_UP.divide(self.lo, rhs.hi),
            CTX_UP.divide(self.hi, rhs.lo),
            CTX_UP.divide(self.hi, rhs.hi),
        )
        return Interval(min(lows), max(highs))

    def __rtruediv__(
        self, other: "Interval | str | int | Decimal"
    ) -> "Interval":
        return self.coerce(other) / self

    def square(self) -> "Interval":
        zero = Decimal(0)
        if self.lo <= zero <= self.hi:
            upper = max(
                CTX_UP.multiply(self.lo, self.lo),
                CTX_UP.multiply(self.hi, self.hi),
            )
            return Interval(zero, upper)
        if self.hi < zero:
            return Interval(
                CTX_DOWN.multiply(self.hi, self.hi),
                CTX_UP.multiply(self.lo, self.lo),
            )
        return Interval(
            CTX_DOWN.multiply(self.lo, self.lo),
            CTX_UP.multiply(self.hi, self.hi),
        )

    def pow_int(self, exponent: int) -> "Interval":
        if exponent < 0:
            return Interval.point(1) / self.pow_int(-exponent)
        if exponent == 0:
            return Interval.point(1)
        if exponent == 1:
            return self
        if exponent == 2:
            return self.square()
        result = Interval.point(1)
        factor = self
        power = exponent
        while power:
            if power & 1:
                result = result * factor
            power >>= 1
            if power:
                factor = factor.square()
        return result

    def contains_zero(self) -> bool:
        return self.lo <= 0 <= self.hi

    def contains(self, other: "Interval") -> bool:
        return self.lo <= other.lo and other.hi <= self.hi

    def strict_sign(self) -> str:
        if self.hi < 0:
            return "negative"
        if self.lo > 0:
            return "positive"
        return "unresolved"

    def width_upper(self) -> Decimal:
        return CTX_UP.subtract(self.hi, self.lo)

    def record(self) -> dict[str, str]:
        return {"lower": str(self.lo), "upper": str(self.hi)}

    def __repr__(self) -> str:
        return f"Interval({self.lo!r}, {self.hi!r})"


def interval_hull(left: Interval, right: Interval) -> Interval:
    return Interval(min(left.lo, right.lo), max(left.hi, right.hi))


def vector_hull(
    left: Sequence[Interval], right: Sequence[Interval]
) -> list[Interval]:
    if len(left) != len(right):
        raise ValueError("vector hull dimension mismatch")
    return [interval_hull(a, b) for a, b in zip(left, right)]


def vector_contained(
    inner: Sequence[Interval], outer: Sequence[Interval]
) -> bool:
    return (
        len(inner) == len(outer)
        and all(box.contains(value) for value, box in zip(inner, outer))
    )


def all_finite(values: Iterable[Interval]) -> bool:
    return all(value.lo.is_finite() and value.hi.is_finite()
               for value in values)


def sum_intervals(values: Iterable[Interval]) -> Interval:
    total = Interval.point(0)
    for value in values:
        total = total + value
    return total


def atan_inverse_enclosure(
    denominator: int, tolerance: Decimal
) -> tuple[Interval, int, Interval]:
    """Enclose atan(1/q) by an alternating series with its next term."""
    if denominator <= 1:
        raise ValueError("Machin arctangent denominator must exceed one")
    x = Interval.point(1) / denominator
    x_squared = x.square()
    term = x
    partial = Interval.point(0)
    index = 0
    while index < 10000:
        partial = partial + term if index % 2 == 0 else partial - term
        next_term = (
            term * x_squared * (2 * index + 1) / (2 * index + 3)
        )
        if next_term.hi <= tolerance:
            if index % 2 == 0:
                enclosure = Interval(
                    CTX_DOWN.subtract(partial.lo, next_term.hi),
                    partial.hi,
                )
            else:
                enclosure = Interval(
                    partial.lo,
                    CTX_UP.add(partial.hi, next_term.hi),
                )
            return enclosure, index + 1, next_term
        term = next_term
        index += 1
    raise RuntimeError("arctangent series did not meet tolerance")


def machin_pi_enclosure(precision: int) -> tuple[Interval, dict[str, object]]:
    guard_digits = 15
    tolerance = Decimal(f"1e-{precision - guard_digits}")
    atan_five, terms_five, tail_five = atan_inverse_enclosure(5, tolerance)
    atan_239, terms_239, tail_239 = atan_inverse_enclosure(239, tolerance)
    pi_interval = 16 * atan_five - 4 * atan_239
    weighted_tail_ceiling = CTX_UP.add(
        CTX_UP.multiply(Decimal(16), tail_five.hi),
        CTX_UP.multiply(Decimal(4), tail_239.hi),
    )
    sanity = (
        Decimal(3) < pi_interval.lo
        and pi_interval.hi < Decimal(4)
        and pi_interval.width_upper() > 0
    )
    if not sanity:
        raise ArithmeticError("Machin pi enclosure failed sanity gate")
    return pi_interval, {
        "formula": "pi = 16*atan(1/5) - 4*atan(1/239)",
        "series": "atan(x)=sum((-1)^k*x^(2k+1)/(2k+1))",
        "alternatingTailBound": True,
        "enclosureRule": (
            "even last index: [S-next,S]; odd last index: [S,S+next]"
        ),
        "weightedNextTermCeiling": str(weighted_tail_ceiling),
        "tolerance": str(tolerance),
        "atanOneFifthTerms": terms_five,
        "atanOneFifthNextTerm": tail_five.record(),
        "atanOne239Terms": terms_239,
        "atanOne239NextTerm": tail_239.record(),
        "pi": pi_interval.record(),
    }


def rhs(state: Sequence[Interval], eta: Interval) -> list[Interval]:
    if len(state) != 12:
        raise ValueError("R0.73C autonomous state must have dimension 12")
    s1, c1, s2, c2 = state[:4]
    w_value = -s1 / 2 + s2 / 4
    w_xx = s1 / 2 - s2
    denominator = w_value.square() + eta.square()
    if denominator.lo <= 0:
        raise ArithmeticError("Rayleigh denominator lost positivity")
    p_real = Interval.point("0.25") + w_xx * w_value / denominator
    p_imag = w_xx * eta / denominator
    output = [c1, -s1, 2 * c2, -2 * s2]
    for offset in (4, 8):
        u_real, u_imag, v_real, v_imag = state[offset:offset + 4]
        output.extend([
            v_real,
            v_imag,
            p_real * u_real - p_imag * u_imag,
            p_imag * u_real + p_real * u_imag,
        ])
    if not all_finite(output):
        raise ArithmeticError("non-finite RHS enclosure")
    return output


def series_add(
    left: Sequence[Interval], right: Sequence[Interval]
) -> list[Interval]:
    if len(left) != len(right):
        raise ValueError("series addition length mismatch")
    return [a + b for a, b in zip(left, right)]


def series_scale(
    values: Sequence[Interval], factor: Interval | str | int
) -> list[Interval]:
    return [Interval.coerce(factor) * value for value in values]


def series_mul(
    left: Sequence[Interval],
    right: Sequence[Interval],
    degree: int,
) -> list[Interval]:
    if len(left) < degree + 1 or len(right) < degree + 1:
        raise ValueError("series multiplication input too short")
    output: list[Interval] = []
    for index in range(degree + 1):
        output.append(sum_intervals(
            left[j] * right[index - j] for j in range(index + 1)
        ))
    return output


def series_reciprocal(
    values: Sequence[Interval], degree: int
) -> list[Interval]:
    if len(values) < degree + 1:
        raise ValueError("reciprocal series input too short")
    if values[0].contains_zero():
        raise ZeroDivisionError("Taylor denominator contains zero")
    output = [Interval.point(0) for _ in range(degree + 1)]
    output[0] = 1 / values[0]
    for index in range(1, degree + 1):
        convolution = sum_intervals(
            values[j] * output[index - j]
            for j in range(1, index + 1)
        )
        output[index] = -output[0] * convolution
    return output


def series_divide(
    numerator: Sequence[Interval],
    denominator: Sequence[Interval],
    degree: int,
) -> list[Interval]:
    return series_mul(
        numerator,
        series_reciprocal(denominator, degree),
        degree,
    )


def taylor_coefficients(
    initial: Sequence[Interval], eta: Interval, degree: int
) -> list[list[Interval]]:
    coefficients = [
        [value] + [Interval.point(0) for _ in range(degree)]
        for value in initial
    ]
    for index in range(degree):
        active_degree = index
        s1 = coefficients[0][:active_degree + 1]
        c1 = coefficients[1][:active_degree + 1]
        s2 = coefficients[2][:active_degree + 1]
        c2 = coefficients[3][:active_degree + 1]
        w_value = series_add(
            series_scale(s1, Interval.point("-0.5")),
            series_scale(s2, Interval.point("0.25")),
        )
        w_xx = series_add(
            series_scale(s1, Interval.point("0.5")),
            series_scale(s2, Interval.point(-1)),
        )
        denominator = series_mul(
            w_value, w_value, active_degree
        )
        denominator[0] = denominator[0] + eta.square()
        p_real = series_divide(
            series_mul(w_xx, w_value, active_degree),
            denominator,
            active_degree,
        )
        p_real[0] = p_real[0] + Interval.point("0.25")
        p_imag = series_scale(
            series_divide(w_xx, denominator, active_degree), eta
        )
        rhs_series: list[list[Interval]] = [
            c1,
            series_scale(s1, -1),
            series_scale(c2, 2),
            series_scale(s2, -2),
        ]
        for offset in (4, 8):
            u_real = coefficients[offset][:active_degree + 1]
            u_imag = coefficients[offset + 1][:active_degree + 1]
            v_real = coefficients[offset + 2][:active_degree + 1]
            v_imag = coefficients[offset + 3][:active_degree + 1]
            rhs_series.extend([
                v_real,
                v_imag,
                series_add(
                    series_mul(p_real, u_real, active_degree),
                    series_scale(
                        series_mul(p_imag, u_imag, active_degree), -1
                    ),
                ),
                series_add(
                    series_mul(p_imag, u_real, active_degree),
                    series_mul(p_real, u_imag, active_degree),
                ),
            ])
        divisor = Interval.point(index + 1)
        for component in range(12):
            coefficients[component][index + 1] = (
                rhs_series[component][index] / divisor
            )
    return coefficients


def expanded_box(
    base: Sequence[Interval],
    scale: int,
    second_order_pad: Interval,
) -> list[Interval]:
    output: list[Interval] = []
    scale_decimal = Decimal(scale)
    two = Decimal(2)
    for value in base:
        width = CTX_UP.subtract(value.hi, value.lo)
        radius = CTX_UP.divide(width, two)
        one_scale_pad = CTX_UP.add(radius, second_order_pad.hi)
        extra = CTX_UP.multiply(scale_decimal, one_scale_pad)
        output.append(Interval(
            CTX_DOWN.subtract(value.lo, extra),
            CTX_UP.add(value.hi, extra),
        ))
    return output


def picard_enclosure(
    initial: Sequence[Interval],
    eta: Interval,
    step: Interval,
    max_attempts: int,
) -> tuple[list[Interval], int]:
    zero_to_step = Interval(Decimal(0), step.hi)
    first_image = [
        value + zero_to_step * derivative
        for value, derivative in zip(initial, rhs(initial, eta))
    ]
    base = vector_hull(initial, first_image)
    tiny = Interval.point(Decimal(f"1e-{WORKING_PRECISION - 15}"))
    second_order_pad = 64 * step.square() + tiny
    for attempt in range(max_attempts):
        scale = 2 ** attempt
        enclosure = expanded_box(base, scale, second_order_pad)
        image = [
            value + zero_to_step * derivative
            for value, derivative in zip(initial, rhs(enclosure, eta))
        ]
        if vector_contained(image, enclosure):
            return enclosure, attempt
    raise RuntimeError("Picard enclosure did not close")


def evaluate_polynomial(
    coefficients: Sequence[Interval], step: Interval, stop: int
) -> Interval:
    value = coefficients[stop]
    for index in range(stop - 1, -1, -1):
        value = coefficients[index] + step * value
    return value


def validated_step(
    initial: Sequence[Interval],
    eta: Interval,
    step: Interval,
    order: int,
    max_picard_attempts: int,
) -> tuple[list[Interval], int]:
    enclosure, attempt = picard_enclosure(
        initial, eta, step, max_picard_attempts
    )
    launch = taylor_coefficients(initial, eta, order - 1)
    remainder = taylor_coefficients(enclosure, eta, order)
    step_power = step.pow_int(order)
    output = []
    for component in range(12):
        polynomial = evaluate_polynomial(
            launch[component], step, order - 1
        )
        tail = step_power * remainder[component][order]
        output.append(polynomial + tail)
    if not all_finite(output):
        raise ArithmeticError("non-finite validated step output")
    return output, attempt


def initial_state() -> list[Interval]:
    values = (0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0)
    return [Interval.point(value) for value in values]


def complex_multiply(
    left: tuple[Interval, Interval],
    right: tuple[Interval, Interval],
) -> tuple[Interval, Interval]:
    left_real, left_imag = left
    right_real, right_imag = right
    return (
        left_real * right_real - left_imag * right_imag,
        left_real * right_imag + left_imag * right_real,
    )


class ProgressReporter:
    def __init__(self, path: Path | None, run_id: str) -> None:
        self.path = path
        self.run_id = run_id
        self.started = time.monotonic()
        self.stream = None

    def __enter__(self) -> "ProgressReporter":
        if self.path is not None:
            self.stream = self.path.open("w", encoding="utf-8")
        return self

    def emit(self, event: str, **payload: object) -> None:
        row = {
            "event": event,
            "runId": self.run_id,
            "elapsedSeconds": round(time.monotonic() - self.started, 3),
            **payload,
        }
        rendered = json.dumps(row, sort_keys=True)
        print(rendered, file=sys.stderr, flush=True)
        if self.stream is not None:
            self.stream.write(rendered + "\n")
            self.stream.flush()

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.stream is not None:
            self.stream.close()


def integrate(
    eta_text: str,
    steps: int,
    order: int,
    pi_interval: Interval,
    max_picard_attempts: int,
    reporter: ProgressReporter,
) -> dict[str, object]:
    eta = Interval.point(eta_text)
    if eta.lo <= 0:
        raise ValueError("eta endpoint must be positive")
    total = 2 * pi_interval
    step = total / steps
    state = initial_state()
    stride = max(1, steps // 8)
    maximum_attempt = 0
    attempt_sum = 0
    for index in range(steps):
        state, attempt = validated_step(
            state, eta, step, order, max_picard_attempts
        )
        maximum_attempt = max(maximum_attempt, attempt)
        attempt_sum += attempt
        completed = index + 1
        if completed == steps or completed % stride == 0:
            reporter.emit(
                "validated-step",
                eta=eta_text,
                completed=completed,
                total=steps,
                order=order,
                maximumPicardAttempt=maximum_attempt,
            )
    trace_real = state[4] + state[10]
    trace_imag = state[5] + state[11]
    residual = trace_real - 2

    a = (state[4], state[5])
    b = (state[8], state[9])
    c = (state[6], state[7])
    d = (state[10], state[11])
    ad = complex_multiply(a, d)
    bc = complex_multiply(b, c)
    determinant = (ad[0] - bc[0], ad[1] - bc[1])

    finite = all_finite(state) and all_finite([
        trace_real, trace_imag, residual,
        determinant[0], determinant[1],
    ])
    imag_contains_zero = trace_imag.contains_zero()
    determinant_contains_one = (
        determinant[0].lo <= 1 <= determinant[0].hi
        and determinant[1].contains_zero()
    )
    if not finite:
        raise ArithmeticError("final integration intervals are non-finite")
    if not imag_contains_zero:
        raise ArithmeticError("trace imaginary interval excludes zero")
    if not determinant_contains_one:
        raise ArithmeticError("monodromy determinant interval excludes one")
    return {
        "eta": eta_text,
        "step": step.record(),
        "steps": steps,
        "order": order,
        "traceReal": trace_real.record(),
        "traceImag": trace_imag.record(),
        "traceMinusTwo": residual.record(),
        "sign": residual.strict_sign(),
        "determinantReal": determinant[0].record(),
        "determinantImag": determinant[1].record(),
        "checks": {
            "allFinite": finite,
            "traceImagContainsZero": imag_contains_zero,
            "determinantContainsOnePlusZeroI": determinant_contains_one,
        },
        "picard": {
            "maximumAttempt": maximum_attempt,
            "attemptSum": attempt_sum,
        },
        "fourierTruncationUsed": False,
        "primaryImported": False,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_payload(path: Path | None, payload: dict[str, object]) -> None:
    rendered = json.dumps(
        payload, indent=2, sort_keys=True, allow_nan=False
    ) + "\n"
    if path is None:
        print(rendered, end="")
    else:
        path.write_text(rendered, encoding="utf-8")


def main() -> int:
    args = parse_args()
    payload: dict[str, object]
    try:
        source_path = Path(__file__).resolve()
        source_hash_before = sha256(source_path)
        runtime = runtime_checks()
        configure_arithmetic(args.precision)
        if args.steps <= 0 or args.order < 2:
            raise ValueError("steps must be positive and order at least two")
        if args.max_picard_attempts <= 0:
            raise ValueError("max Picard attempts must be positive")
        eta_low = Interval.point(args.eta_low)
        eta_high = Interval.point(args.eta_high)
        if not (
            eta_low.lo > 0
            and eta_low.hi < eta_high.lo
            and args.eta_low == DEFAULT_ETA_LOW
            and args.eta_high == DEFAULT_ETA_HIGH
        ):
            raise ValueError(
                "formal bracket must be the ordered endpoints "
                f"{DEFAULT_ETA_LOW}, {DEFAULT_ETA_HIGH}"
            )
        pi_interval, pi_metadata = machin_pi_enclosure(args.precision)
        with ProgressReporter(args.progress, args.run_id) as reporter:
            reporter.emit(
                "run-start",
                steps=args.steps,
                order=args.order,
                precision=args.precision,
                etaLow=args.eta_low,
                etaHigh=args.eta_high,
            )
            results = [
                integrate(
                    eta_text,
                    args.steps,
                    args.order,
                    pi_interval,
                    args.max_picard_attempts,
                    reporter,
                )
                for eta_text in (args.eta_low, args.eta_high)
            ]
            signs = [row["sign"] for row in results]
            signs_resolved = all(sign in {"negative", "positive"}
                                 for sign in signs)
            signs_opposite = (
                signs_resolved
                and signs[0] != signs[1]
            )
            all_imaginary_checks = all(
                row["checks"]["traceImagContainsZero"] for row in results
            )
            all_finite_checks = all(
                row["checks"]["allFinite"] for row in results
            )
            all_determinant_checks = all(
                row["checks"]["determinantContainsOnePlusZeroI"]
                for row in results
            )
            if not signs_opposite:
                raise ArithmeticError(
                    f"endpoint signs are not strictly opposite: {signs}"
                )
            if not (
                all_imaginary_checks
                and all_finite_checks
                and all_determinant_checks
            ):
                raise ArithmeticError("final fail-closed invariant gate failed")
            reporter.emit(
                "run-complete",
                status="passed",
                signs={
                    args.eta_low: signs[0],
                    args.eta_high: signs[1],
                },
            )
        source_hash_after = sha256(source_path)
        if source_hash_before != source_hash_after:
            raise RuntimeError("validator source changed during execution")
        critical_flags_clear = all(
            not context.flags[signal]
            for context in (CTX_DOWN, CTX_UP)
            for signal in (
                DivisionByZero,
                InvalidOperation,
                Overflow,
                Underflow,
                Subnormal,
                Clamped,
                FloatOperation,
            )
        )
        if not critical_flags_clear:
            raise ArithmeticError("critical Decimal context flag was raised")
        sigma_bracket = Interval.point("0.5") * Interval.bounds(
            args.eta_low, args.eta_high
        )
        checks = {
            "runtimeVersionGate": all(runtime["checks"].values()),
            "sourceHashStableDuringRun": (
                source_hash_before == source_hash_after
            ),
            "criticalDecimalFlagsClear": critical_flags_clear,
            "machinPiFiniteAndBetweenThreeAndFour": (
                pi_interval.lo > 3 and pi_interval.hi < 4
            ),
            "allEndpointIntervalsFinite": all_finite_checks,
            "endpointSignsResolved": signs_resolved,
            "endpointSignsOpposite": signs_opposite,
            "allTraceImaginaryIntervalsContainZero": all_imaginary_checks,
            "allDeterminantIntervalsContainOne": all_determinant_checks,
            "noPrimaryImport": True,
            "noMpmathImport": True,
        }
        payload = {
            "schemaVersion": SCHEMA_VERSION,
            "status": "passed" if all(checks.values()) else "failed",
            "scope": (
                "independent Decimal directed-rounding validation of the "
                "R0.73C Rayleigh monodromy endpoint sign bracket"
            ),
            "arithmetic": {
                **runtime,
                "workingPrecisionDigits": args.precision,
                "lowerRounding": "ROUND_FLOOR",
                "upperRounding": "ROUND_CEILING",
                "transcendentalLibraryUsed": False,
            },
            "source": {
                "path": str(source_path),
                "bytes": source_path.stat().st_size,
                "sha256": source_hash_after,
            },
            "parameters": {
                "etaLow": args.eta_low,
                "etaHigh": args.eta_high,
                "steps": args.steps,
                "order": args.order,
                "precision": args.precision,
                "maxPicardAttempts": args.max_picard_attempts,
                "runId": args.run_id,
            },
            "machinPi": pi_metadata,
            "results": results,
            "checks": checks,
            "theoremConsequence": {
                "conditionalOnAnalyticMonodromyLemma": True,
                "etaRootOpenInterval": {
                    "lower": args.eta_low,
                    "upper": args.eta_high,
                },
                "sigmaEqualsEtaOverTwo": True,
                "sigmaRootOpenInterval": sigma_bracket.record(),
                "positiveRealPointSpectrumExists": True,
                "rootUniquenessProved": False,
                "eigenvalueSimplicityProved": False,
            },
            "claimBoundary": {
                "infiniteDimensionalPeriodicOdeBracketValidated": True,
                "fourierTruncationUsed": False,
                "nonautonomousTransferProved": False,
                "nonlinearNavierStokesProved": False,
                "clayProblemSolved": False,
            },
        }
        if payload["status"] != "passed":
            raise RuntimeError("aggregate validation checks did not all pass")
        write_payload(args.output, payload)
        return 0
    except Exception as error:
        payload = {
            "schemaVersion": SCHEMA_VERSION,
            "status": "failed",
            "errorType": type(error).__name__,
            "error": str(error),
            "parameters": {
                "etaLow": args.eta_low,
                "etaHigh": args.eta_high,
                "steps": args.steps,
                "order": args.order,
                "precision": args.precision,
                "maxPicardAttempts": args.max_picard_attempts,
                "runId": args.run_id,
            },
        }
        write_payload(args.output, payload)
        print(json.dumps(payload, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
