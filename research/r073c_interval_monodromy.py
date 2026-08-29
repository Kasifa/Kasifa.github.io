#!/usr/bin/env python3
"""Validated Taylor enclosure for the R0.73C Rayleigh monodromy.

This program works directly with the periodic Rayleigh ODE

    phi'' = (gamma^2 + W'' / (W - i eta)) phi,

where ``W=-sin(x)/2+sin(2x)/4``.  It does not truncate Fourier space.  The
real autonomous system also evolves sin(x), cos(x), sin(2x), and cos(2x), so
all interval operations are algebraic after launch.  Each step uses a Taylor
polynomial and a normalized-derivative remainder evaluated on a Picard
enclosure of the whole step.

The only non-standard dependency is mpmath 1.3.0.  Its ``iv`` context is used
only for algebraic operations and the directed enclosure of pi.  The formal
R0.73C certificate records the exact binary endpoints as well as readable
decimal intervals.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Iterable, Sequence

import mpmath
from mpmath import iv


GAMMA_SQUARED = iv.mpf(["0.25", "0.25"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--eta", action="append", required=True,
                        help="positive rational/decimal endpoint")
    parser.add_argument("--steps", type=int, default=1024)
    parser.add_argument("--order", type=int, default=12)
    parser.add_argument("--dps", type=int, default=50)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress", type=Path)
    parser.add_argument("--run-id", default="standalone")
    parser.add_argument("--require-bracket", action="store_true")
    return parser.parse_args()


def point(value: str | int) -> iv.mpf:
    return iv.mpf([str(value), str(value)])


def raw_endpoint(value: tuple[int, int, int, int]) -> dict[str, int]:
    """Serialize an exact libmp binary endpoint without decimal rounding."""
    sign, mantissa, exponent, bitcount = value
    return {
        "sign": int(sign),
        "mantissa": int(mantissa),
        "exponent": int(exponent),
        "bitcount": int(bitcount),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arithmetic_sources() -> list[dict[str, object]]:
    package = Path(mpmath.__file__).resolve().parent
    paths = [
        package / "ctx_iv.py",
        package / "libmp/libmpi.py",
        package / "libmp/libmpf.py",
        package / "libmp/libelefun.py",
    ]
    return [{
        "path": str(path.relative_to(package)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    } for path in paths]


def interval_record(value: iv.mpf) -> dict[str, object]:
    lower, upper = value._mpi_
    return {
        "decimal": str(value),
        "binaryEndpoints": [raw_endpoint(lower), raw_endpoint(upper)],
    }


def record_progress(rows: list[dict[str, object]], path: Path | None,
                    row: dict[str, object]) -> None:
    rows.append(row)
    rendered = json.dumps(row, sort_keys=True)
    print(rendered, file=sys.stderr, flush=True)
    if path:
        with path.open("a", encoding="utf-8") as stream:
            stream.write(rendered + "\n")
            stream.flush()


def hull(left: iv.mpf, right: iv.mpf) -> iv.mpf:
    lower = left.a if left.a < right.a else right.a
    upper = left.b if left.b > right.b else right.b
    return iv.mpf([lower, upper])


def inflate(value: iv.mpf, factor: iv.mpf,
            absolute: iv.mpf) -> iv.mpf:
    midpoint = (value.a + value.b) / 2
    radius = (value.b - value.a) / 2
    padding = (1 + factor) * radius + absolute
    return iv.mpf([midpoint - padding, midpoint + padding])


def vector_hull(left: Sequence[iv.mpf],
                right: Sequence[iv.mpf]) -> list[iv.mpf]:
    return [hull(a, b) for a, b in zip(left, right)]


def vector_in(left: Sequence[iv.mpf],
              right: Sequence[iv.mpf]) -> bool:
    return all(a in b for a, b in zip(left, right))


def rhs(state: Sequence[iv.mpf], eta: iv.mpf) -> list[iv.mpf]:
    s1, c1, s2, c2 = state[:4]
    w_value = -s1 / 2 + s2 / 4
    w_xx = s1 / 2 - s2
    denominator = w_value ** 2 + eta ** 2
    p_real = GAMMA_SQUARED + w_xx * w_value / denominator
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
    return output


def series_add(left: Sequence[iv.mpf],
               right: Sequence[iv.mpf]) -> list[iv.mpf]:
    return [a + b for a, b in zip(left, right)]


def series_scale(values: Sequence[iv.mpf],
                 factor: iv.mpf) -> list[iv.mpf]:
    return [factor * value for value in values]


def series_mul(left: Sequence[iv.mpf],
               right: Sequence[iv.mpf], degree: int) -> list[iv.mpf]:
    zero = point(0)
    output = [zero for _ in range(degree + 1)]
    for index in range(degree + 1):
        output[index] = sum(
            (left[j] * right[index - j] for j in range(index + 1)),
            zero,
        )
    return output


def series_reciprocal(values: Sequence[iv.mpf],
                      degree: int) -> list[iv.mpf]:
    if point(0) in values[0]:
        raise ZeroDivisionError("Taylor denominator contains zero")
    zero = point(0)
    output = [zero for _ in range(degree + 1)]
    output[0] = 1 / values[0]
    for index in range(1, degree + 1):
        convolution = sum(
            (values[j] * output[index - j]
             for j in range(1, index + 1)),
            zero,
        )
        output[index] = -output[0] * convolution
    return output


def series_divide(numerator: Sequence[iv.mpf],
                  denominator: Sequence[iv.mpf],
                  degree: int) -> list[iv.mpf]:
    return series_mul(
        numerator,
        series_reciprocal(denominator, degree),
        degree,
    )


def taylor_coefficients(initial: Sequence[iv.mpf], eta: iv.mpf,
                        degree: int) -> list[list[iv.mpf]]:
    zero = point(0)
    coefficients = [
        [value] + [zero for _ in range(degree)] for value in initial
    ]
    for index in range(degree):
        active_degree = index
        s1 = coefficients[0][:active_degree + 1]
        c1 = coefficients[1][:active_degree + 1]
        s2 = coefficients[2][:active_degree + 1]
        c2 = coefficients[3][:active_degree + 1]
        w_value = series_add(
            series_scale(s1, point("-0.5")),
            series_scale(s2, point("0.25")),
        )
        w_xx = series_add(
            series_scale(s1, point("0.5")),
            series_scale(s2, point(-1)),
        )
        denominator = series_mul(w_value, w_value, active_degree)
        denominator[0] += eta ** 2
        p_real = series_divide(
            series_mul(w_xx, w_value, active_degree),
            denominator,
            active_degree,
        )
        p_real[0] += GAMMA_SQUARED
        p_imag = series_scale(
            series_divide(w_xx, denominator, active_degree), eta
        )

        rhs_series: list[list[iv.mpf]] = [
            c1,
            series_scale(s1, point(-1)),
            series_scale(c2, point(2)),
            series_scale(s2, point(-2)),
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
                        series_mul(p_imag, u_imag, active_degree),
                        point(-1),
                    ),
                ),
                series_add(
                    series_mul(p_imag, u_real, active_degree),
                    series_mul(p_real, u_imag, active_degree),
                ),
            ])
        divisor = point(index + 1)
        for component in range(len(coefficients)):
            coefficients[component][index + 1] = (
                rhs_series[component][index] / divisor
            )
    return coefficients


def picard_enclosure(initial: Sequence[iv.mpf], eta: iv.mpf,
                     step: iv.mpf) -> list[iv.mpf]:
    zero_to_step = iv.mpf([0, step.b])
    first_image = [
        value + zero_to_step * derivative
        for value, derivative in zip(initial, rhs(initial, eta))
    ]
    base = vector_hull(initial, first_image)
    # The coefficient can rotate a fundamental column rapidly near the
    # collision shoulder.  A deliberately relaxed O(h^2) padding keeps the
    # Picard box invariant without using a pointwise numerical predictor.
    second_order_pad = 64 * step ** 2 + point("1e-45")
    for attempt in range(8):
        scale = point(2 ** attempt)
        enclosure = [
            inflate(value, scale, scale * second_order_pad)
            for value in base
        ]
        image = [
            value + zero_to_step * derivative
            for value, derivative in zip(initial, rhs(enclosure, eta))
        ]
        if vector_in(image, enclosure):
            return enclosure
    raise RuntimeError("Picard enclosure did not close")


def evaluate_polynomial(coefficients: Sequence[iv.mpf],
                        step: iv.mpf, stop: int) -> iv.mpf:
    value = coefficients[stop]
    for index in range(stop - 1, -1, -1):
        value = coefficients[index] + step * value
    return value


def validated_step(initial: Sequence[iv.mpf], eta: iv.mpf,
                   step: iv.mpf, order: int) -> list[iv.mpf]:
    enclosure = picard_enclosure(initial, eta, step)
    launch = taylor_coefficients(initial, eta, order - 1)
    remainder = taylor_coefficients(enclosure, eta, order)
    output = []
    for component in range(len(initial)):
        polynomial = evaluate_polynomial(
            launch[component], step, order - 1
        )
        tail = (step ** order) * remainder[component][order]
        output.append(polynomial + tail)
    return output


def initial_state() -> list[iv.mpf]:
    # Fundamental columns (1,0)^T and (0,1)^T.
    values = [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0]
    return [point(value) for value in values]


def integrate(eta_text: str, steps: int, order: int,
              progress: list[dict[str, object]] | None = None,
              run_id: str = "standalone",
              progress_path: Path | None = None) -> dict[str, object]:
    if steps <= 0 or order < 2:
        raise ValueError("steps must be positive and order at least two")
    eta = point(eta_text)
    if eta.a <= 0:
        raise ValueError("eta must be positive")

    # mpmath 1.3.0 implements iv.pi by floor/ceiling evaluation of mpf_pi.
    total = 2 * iv.pi
    nominal = total / point(steps)
    state = initial_state()
    stride = max(1, steps // 8)
    for index in range(steps):
        state = validated_step(state, eta, nominal, order)
        completed = index + 1
        if progress is not None and (
            completed == steps or completed % stride == 0
        ):
            record_progress(progress, progress_path, {
                "event": "validated-step",
                "runId": run_id,
                "eta": eta_text,
                "completed": completed,
                "total": steps,
                "order": order,
            })

    trace_real = state[4] + state[10]
    trace_imag = state[5] + state[11]
    residual = trace_real - 2
    return {
        "eta": eta_text,
        "gamma": "1/2",
        "step": interval_record(nominal),
        "steps": steps,
        "order": order,
        "traceReal": interval_record(trace_real),
        "traceImag": interval_record(trace_imag),
        "traceImagContainsZero": bool(point(0) in trace_imag),
        "traceMinusTwo": interval_record(residual),
        "sign": (
            "negative" if residual.b < 0 else
            "positive" if residual.a > 0 else
            "unresolved"
        ),
        "infiniteDimensionalPeriodicOde": True,
        "fourierTruncationUsed": False,
    }


def main() -> None:
    args = parse_args()
    if mpmath.__version__ != "1.3.0":
        raise RuntimeError(
            "formal arithmetic requires mpmath==1.3.0; loaded "
            + mpmath.__version__
        )
    iv.dps = args.dps
    if args.progress:
        args.progress.write_text("", encoding="utf-8")
    progress: list[dict[str, object]] = []
    record_progress(progress, args.progress, {
        "event": "run-start",
        "runId": args.run_id,
        "etas": args.eta,
        "steps": args.steps,
        "order": args.order,
        "dps": args.dps,
    })
    results = [
        integrate(eta, args.steps, args.order, progress, args.run_id,
                  args.progress)
        for eta in args.eta
    ]
    if args.require_bracket:
        if len(results) != 2:
            raise RuntimeError("formal bracket requires exactly two endpoints")
        left_eta = point(args.eta[0])
        right_eta = point(args.eta[1])
        if not left_eta.b < right_eta.a:
            raise RuntimeError("formal bracket endpoints are not ordered")
        if {results[0]["sign"], results[1]["sign"]} != {
            "negative", "positive"
        }:
            raise RuntimeError("formal bracket endpoints are not opposite-sign")
        if not all(row["traceImagContainsZero"] for row in results):
            raise RuntimeError("trace imaginary sentinel excludes exact zero")
    record_progress(progress, args.progress, {
        "event": "run-complete",
        "runId": args.run_id,
        "signs": {row["eta"]: row["sign"] for row in results},
    })
    payload = {
        "schemaVersion": "r073c-interval-monodromy-v2",
        "arithmetic": (
            "mpmath 1.3.0 iv directed binary interval arithmetic; "
            "algebraic operations and iv.pi only"
        ),
        "dps": args.dps,
        "status": "passed" if args.require_bracket else "completed",
        "runId": args.run_id,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "mpmath": mpmath.__version__,
            "source": {
                "path": str(Path(__file__).resolve()),
                "bytes": Path(__file__).stat().st_size,
                "sha256": sha256(Path(__file__).resolve()),
            },
            "arithmeticSources": arithmetic_sources(),
        },
        "results": results,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
