#!/usr/bin/env python3
"""R0.27 generating equations and scalar negative-edge audit.

R0.26 proves that b_N is an exact two-generator edge coefficient.  On this
edge every offset is collinear, so a coefficient is determined by two scalar
amplitudes: an in-plane stream amplitude alpha and an out-of-plane sharp
amplitude s.  Their Taylor recurrence closes without four-vector Leray
operations.

The scalar recurrence is the coefficient form of a nonlocal generating
equation for alpha and a linear transport equation for s.  This audit derives
that representation, checks it against the R0.26 certificate through N=25,
and extends a dual-precision probe of the b_N endpoint through N=75.

The finite probe strongly tests the asymptotic question but does not prove a
generating-function singularity theorem or a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

import gmpy2

import boundary_face_channel_audit as channel
import generated_subspace_sharpness_audit as base


Real = gmpy2.mpfr
ScalarLayer = list[Real]
ScalarField = list[ScalarLayer | None]

P_MINUS: base.Label = (-1, -1, -1)
C_PLUS: base.Label = (1, -1, -1)
R026_CERTIFICATE = Path(
    "research/certificates/r026/boundary-edge-transfer.json"
)
DEFAULT_PRECISIONS = (160, 224)
DEFAULT_SCALE_PER_LEAF = 4
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, message: str) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        print(f"[R0.27 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)
    if PROGRESS_LOG is not None:
        record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": elapsed,
            "stage": message,
        }
        with PROGRESS_LOG.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, ensure_ascii=False) + "\n")
            target.flush()
            os.fsync(target.fileno())


def git_source_state() -> dict[str, object]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    dirty = bool(
        subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
    )
    return {"commit": commit, "dirty": dirty}


def atomic_json_write(path: Path, payload: dict[str, object], pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    with temporary.open("w", encoding="utf-8") as target:
        json.dump(
            payload,
            target,
            ensure_ascii=False,
            indent=2 if pretty else None,
            sort_keys=True,
        )
        target.write("\n")
        target.flush()
        os.fsync(target.fileno())
    os.replace(temporary, path)


def load_initial_scalars(
    scale_per_leaf: int,
) -> tuple[Real, Real, Real, Real, Real, dict[str, base.Rational]]:
    center, _, _ = base.load_root_center()
    p_value, q_value, x_value = (
        center[name] for name in ("p", "q", "x")
    )
    pump_norm_squared = base.Rational(1) + p_value * p_value / 12
    catalyst_norm_squared = base.Rational(1) + q_value * q_value / 3
    radicand = x_value * pump_norm_squared / (
        4 * catalyst_norm_squared
    )
    initial = channel.embedded_initial_field(center, radicand)
    square_root_two = gmpy2.sqrt(Real(2))
    sharp_direction = (
        Real(1) / square_root_two,
        -Real(1) / square_root_two,
        Real(0),
    )
    scale = Real(scale_per_leaf)

    def scalar_pair(label: base.Label) -> tuple[Real, Real]:
        coefficient = initial[label]
        alpha = -coefficient[3] / square_root_two
        sharp = channel.real_dot(coefficient[:3], sharp_direction)
        return alpha / scale, sharp / scale

    pump_alpha, pump_sharp = scalar_pair(P_MINUS)
    catalyst_alpha, catalyst_sharp = scalar_pair(C_PLUS)
    return (
        pump_alpha,
        pump_sharp,
        catalyst_alpha,
        catalyst_sharp,
        gmpy2.sqrt(Real(radicand)),
        center,
    )


def scalar_edge_recurrence(
    maximum_leaf_count: int,
    scale_per_leaf: int,
    show_progress: bool,
    started: float,
    precision_bits: int,
) -> tuple[ScalarField, ScalarField, Real, dict[str, base.Rational]]:
    """Return scaled alpha and sharp coefficients indexed by (L,k).

    The stored coefficient is the physical coefficient divided by
    scale_per_leaf**L.  Every normalized quantity and every sharp/alpha growth
    ratio used below is invariant under this rescaling.
    """

    (
        pump_alpha,
        pump_sharp,
        catalyst_alpha,
        catalyst_sharp,
        generator,
        center,
    ) = load_initial_scalars(scale_per_leaf)
    square_root_two = gmpy2.sqrt(Real(2))
    alpha: ScalarField = [None] * (maximum_leaf_count + 1)
    sharp: ScalarField = [None] * (maximum_leaf_count + 1)
    alpha[1] = [pump_alpha, catalyst_alpha]
    sharp[1] = [pump_sharp, catalyst_sharp]

    for leaf_count in range(2, maximum_leaf_count + 1):
        charged_alpha_numerator = [Real(0)] * (leaf_count + 1)
        zero_alpha_numerator = [Real(0)] * (leaf_count + 1)
        sharp_numerator = [Real(0)] * (leaf_count + 1)
        interaction_count = 0

        for left_leaf_count in range(1, leaf_count):
            right_leaf_count = leaf_count - left_leaf_count
            left_alpha_layer = alpha[left_leaf_count]
            right_alpha_layer = alpha[right_leaf_count]
            right_sharp_layer = sharp[right_leaf_count]
            if (
                left_alpha_layer is None
                or right_alpha_layer is None
                or right_sharp_layer is None
            ):
                raise AssertionError("missing scalar recurrence layer")

            for left_catalyst_count, left_alpha in enumerate(
                left_alpha_layer
            ):
                if left_alpha == 0:
                    continue
                for right_catalyst_count, right_alpha in enumerate(
                    right_alpha_layer
                ):
                    right_sharp = right_sharp_layer[right_catalyst_count]
                    if right_alpha == 0 and right_sharp == 0:
                        continue
                    output_catalyst_count = (
                        left_catalyst_count + right_catalyst_count
                    )
                    determinant_twice = (
                        left_leaf_count * right_catalyst_count
                        - left_catalyst_count * right_leaf_count
                    )
                    sharp_numerator[output_catalyst_count] += (
                        determinant_twice * left_alpha * right_sharp
                    )
                    if 3 * output_catalyst_count == leaf_count:
                        zero_alpha_numerator[output_catalyst_count] += (
                            determinant_twice
                            * right_leaf_count
                            * left_alpha
                            * right_alpha
                        )
                    else:
                        charged_alpha_numerator[output_catalyst_count] += (
                            determinant_twice
                            * (3 * right_catalyst_count - right_leaf_count)
                            * left_alpha
                            * right_alpha
                        )
                    interaction_count += 1

        common_scale = square_root_two / (2 * (leaf_count - 1))
        next_sharp = [
            common_scale * value for value in sharp_numerator
        ]
        next_alpha = [Real(0)] * (leaf_count + 1)
        for catalyst_count in range(1, leaf_count):
            integer_charge = 3 * catalyst_count - leaf_count
            if integer_charge == 0:
                next_alpha[catalyst_count] = (
                    square_root_two
                    * zero_alpha_numerator[catalyst_count]
                    / (2 * leaf_count * (leaf_count - 1))
                )
            else:
                next_alpha[catalyst_count] = (
                    square_root_two
                    * charged_alpha_numerator[catalyst_count]
                    / (2 * (leaf_count - 1) * integer_charge)
                )
        alpha[leaf_count] = next_alpha
        sharp[leaf_count] = next_sharp

        if leaf_count % 25 == 0 or leaf_count == maximum_leaf_count:
            progress(
                show_progress,
                started,
                f"precision {precision_bits}: leaves {leaf_count:3d}, "
                f"ordered scalar interactions {interaction_count:8d}",
            )

    return alpha, sharp, generator, center


def endpoint_record(
    parameter: int,
    alpha: Real,
    sharp: Real,
    previous_alpha: Real | None,
    previous_sharp: Real | None,
) -> dict[str, object]:
    leaf_count = 3 * parameter - 1
    charge = Real(1) / 6
    square_root_two = gmpy2.sqrt(Real(2))
    transverse_norm = gmpy2.sqrt(
        sharp * sharp + 3 * charge * charge * alpha * alpha
    )
    mode_norm = transverse_norm + square_root_two * leaf_count * abs(alpha)
    sigma = sharp / mode_norm
    sharp_over_l_alpha = sharp / (leaf_count * alpha)
    block_growth_ratio = None
    if (
        previous_alpha is not None
        and previous_sharp is not None
        and previous_alpha != 0
        and previous_sharp != 0
    ):
        block_growth_ratio = abs(
            (sharp / previous_sharp) / (alpha / previous_alpha)
        )
    return {
        "parameter": parameter,
        "leafCount": leaf_count,
        "sigma": float(sigma),
        "absoluteSigma": float(abs(sigma)),
        "NAbsSigma": float(parameter * abs(sigma)),
        "oneMinusAbsoluteSigma": float(1 - abs(sigma)),
        "sharpOverLAlpha": float(sharp_over_l_alpha),
        "absoluteSharpOverLAlpha": float(abs(sharp_over_l_alpha)),
        "sharpToAlphaBlockGrowthRatio": (
            None if block_growth_ratio is None else float(block_growth_ratio)
        ),
        "highPrecisionSigma": channel.decimal_string(sigma),
        "highPrecisionSharpOverLAlpha": channel.decimal_string(
            sharp_over_l_alpha
        ),
    }


def zero_charge_record(parameter: int, alpha: Real, sharp: Real) -> dict[str, object]:
    leaf_count = 3 * parameter
    square_root_two = gmpy2.sqrt(Real(2))
    mode_norm = abs(sharp) + square_root_two * leaf_count * abs(alpha)
    sharp_fraction = sharp / mode_norm
    return {
        "parameter": parameter,
        "leafCount": leaf_count,
        "sharpFraction": float(sharp_fraction),
        "absoluteSharpFraction": float(abs(sharp_fraction)),
        "highPrecisionSharpFraction": channel.decimal_string(sharp_fraction),
    }


def first_persistent_alternation(
    endpoints: list[dict[str, object]],
) -> int | None:
    for start_index, record in enumerate(endpoints):
        if all(
            ((-1) ** later["parameter"]) * later["sigma"] > 0
            for later in endpoints[start_index:]
        ):
            return record["parameter"]
    return None


def first_threshold(
    endpoints: list[dict[str, object]],
    threshold: float,
) -> int | None:
    for record in endpoints:
        if record["absoluteSigma"] >= threshold:
            return record["parameter"]
    return None


def log_linear_fit(
    records: list[dict[str, object]],
    field: str,
) -> dict[str, float]:
    points = [
        (float(record["parameter"]), float(record[field]))
        for record in records
        if record[field] > 0
    ]
    x_mean = sum(point[0] for point in points) / len(points)
    logs = [(x, math.log(value)) for x, value in points]
    y_mean = sum(point[1] for point in logs) / len(logs)
    denominator = sum((x - x_mean) ** 2 for x, _ in logs)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in logs) / denominator
    intercept = y_mean - slope * x_mean
    return {
        "logSlopePerParameter": slope,
        "multiplicativeFactorPerParameter": math.exp(slope),
        "intercept": intercept,
    }


def tail_summary(endpoints: list[dict[str, object]]) -> dict[str, object]:
    tail_count = min(20, len(endpoints))
    tail = endpoints[-tail_count:]
    growth_ratios = [
        record["sharpToAlphaBlockGrowthRatio"]
        for record in tail
        if record["sharpToAlphaBlockGrowthRatio"] is not None
    ]
    return {
        "tailStart": tail[0]["parameter"],
        "tailEnd": tail[-1]["parameter"],
        "persistentAlternatingSignFrom": first_persistent_alternation(endpoints),
        "thresholds": {
            "absSigmaAtLeast0.5": first_threshold(endpoints, 0.5),
            "absSigmaAtLeast0.9": first_threshold(endpoints, 0.9),
            "absSigmaAtLeast0.99": first_threshold(endpoints, 0.99),
            "absSigmaAtLeast0.999": first_threshold(endpoints, 0.999),
        },
        "lastEndpoint": endpoints[-1],
        "sharpOverLAlphaGrowth": {
            "minimumTailBlockRatio": min(growth_ratios),
            "medianTailBlockRatio": statistics.median(growth_ratios),
            "maximumTailBlockRatio": max(growth_ratios),
            "geometricMeanTailBlockRatio": math.exp(
                sum(math.log(value) for value in growth_ratios)
                / len(growth_ratios)
            ),
            "logLinearFit": log_linear_fit(
                tail, "absoluteSharpOverLAlpha"
            ),
        },
        "sigmaDefectFit": log_linear_fit(
            tail, "oneMinusAbsoluteSigma"
        ),
        "interpretation": (
            "the finite tail is consistent with exponential growth of "
            "|s_N/(L alpha_N)| and alternating convergence of sigma_N to "
            "unit modulus; this is numerical evidence, not a singularity theorem"
        ),
    }


def run_precision(
    precision_bits: int,
    maximum_parameter: int,
    scale_per_leaf: int,
    show_progress: bool,
    started: float,
) -> dict[str, object]:
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = precision_bits
    try:
        maximum_leaf_count = 3 * maximum_parameter
        alpha, sharp, generator, center = scalar_edge_recurrence(
            maximum_leaf_count,
            scale_per_leaf,
            show_progress,
            started,
            precision_bits,
        )
        endpoints: list[dict[str, object]] = []
        previous_alpha = None
        previous_sharp = None
        for parameter in range(2, maximum_parameter + 1):
            leaf_count = 3 * parameter - 1
            catalyst_count = parameter
            alpha_value = alpha[leaf_count][catalyst_count]  # type: ignore[index]
            sharp_value = sharp[leaf_count][catalyst_count]  # type: ignore[index]
            endpoints.append(
                endpoint_record(
                    parameter,
                    alpha_value,
                    sharp_value,
                    previous_alpha,
                    previous_sharp,
                )
            )
            previous_alpha = alpha_value
            previous_sharp = sharp_value

        zero_charge = []
        for parameter in range(1, maximum_parameter + 1):
            leaf_count = 3 * parameter
            catalyst_count = parameter
            zero_charge.append(
                zero_charge_record(
                    parameter,
                    alpha[leaf_count][catalyst_count],  # type: ignore[index]
                    sharp[leaf_count][catalyst_count],  # type: ignore[index]
                )
            )

        progress(
            show_progress,
            started,
            f"precision {precision_bits}: completed endpoint extraction",
        )
        return {
            "precisionBits": precision_bits,
            "scalePerLeaf": scale_per_leaf,
            "quadraticGenerator": float(generator),
            "parameters": {
                "p": float(center["p"]),
                "q": float(center["q"]),
            },
            "endpoints": endpoints,
            "zeroChargeRay": zero_charge,
            "tailSummary": tail_summary(endpoints),
        }
    finally:
        context.precision = previous_precision


def endpoint_map(run: dict[str, object]) -> dict[int, dict[str, object]]:
    return {
        record["parameter"]: record
        for record in run["endpoints"]
    }


def relative_difference(left: str | float, right: str | float) -> float:
    left_real = Real(left)
    right_real = Real(right)
    denominator = max(abs(left_real), abs(right_real), Real("1e-300"))
    return float(abs(left_real - right_real) / denominator)


def validate_runs(
    runs: list[dict[str, object]],
    maximum_parameter: int,
) -> dict[str, object]:
    reference_payload = json.loads(R026_CERTIFICATE.read_text())
    reference = {
        record["parameter"]: record
        for record in reference_payload["runs"][-1]["endpoints"]
    }
    high = endpoint_map(runs[-1])
    regression: dict[str, object] = {}
    for parameter in range(2, min(25, maximum_parameter) + 1):
        difference = relative_difference(
            high[parameter]["sigma"],
            reference[parameter]["right"]["sigma"],
        )
        if difference > 2e-14:
            raise AssertionError(
                f"R0.26 scalar-edge regression failed at N={parameter}"
            )
        regression[f"N{parameter}"] = {
            "rightSigmaRelativeDifference": difference
        }

    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = max(run["precisionBits"] for run in runs) + 32
    stability: dict[str, object] = {}
    maximum_difference = 0.0
    try:
        low = endpoint_map(runs[-2])
        for parameter in range(2, maximum_parameter + 1):
            sigma_difference = relative_difference(
                low[parameter]["highPrecisionSigma"],
                high[parameter]["highPrecisionSigma"],
            )
            ratio_difference = relative_difference(
                low[parameter]["highPrecisionSharpOverLAlpha"],
                high[parameter]["highPrecisionSharpOverLAlpha"],
            )
            maximum_difference = max(
                maximum_difference,
                sigma_difference,
                ratio_difference,
            )
            stability[f"N{parameter}"] = {
                "sigmaRelativeDifference": sigma_difference,
                "sharpOverLAlphaRelativeDifference": ratio_difference,
            }
    finally:
        context.precision = previous_precision
    stability["maximumRelativeDifference"] = maximum_difference
    if maximum_difference > 1e-34:
        raise AssertionError(
            f"dual-precision scalar recurrence failed: {maximum_difference}"
        )

    tail = runs[-1]["tailSummary"]
    if maximum_parameter >= 75:
        last = tail["lastEndpoint"]
        if last["absoluteSigma"] < 0.999:
            raise AssertionError("the N=75 sharp-dominance probe regressed")
        if tail["persistentAlternatingSignFrom"] > 10:
            raise AssertionError("the endpoint parity pattern regressed")

    return {
        "R026Regression": regression,
        "precisionStability": stability,
        "finiteTailChecks": {
            "persistentAlternatingSignFrom": tail[
                "persistentAlternatingSignFrom"
            ],
            "lastAbsoluteSigma": tail["lastEndpoint"]["absoluteSigma"],
            "lastNAbsSigma": tail["lastEndpoint"]["NAbsSigma"],
            "lastAbsoluteSharpOverLAlpha": tail["lastEndpoint"][
                "absoluteSharpOverLAlpha"
            ],
        },
    }


def build_payload(
    maximum_parameter: int,
    precisions: tuple[int, ...],
    scale_per_leaf: int,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    runs = [
        run_precision(
            precision,
            maximum_parameter,
            scale_per_leaf,
            show_progress,
            started,
        )
        for precision in precisions
    ]
    checks = validate_runs(runs, maximum_parameter)
    return {
        "scope": {
            "result": (
                "exact scalar generating equations on the negative edge "
                "and a dual-precision endpoint probe"
            ),
            "maximumParameter": maximum_parameter,
            "maximumLeafCount": 3 * maximum_parameter,
            "limitations": [
                "the N-window is finite and does not prove a singularity asymptotic",
                "the positive-edge first variation is not analyzed here",
                "no Navier-Stokes regularity conclusion is claimed",
            ],
        },
        "edgeCoordinates": {
            "counts": "n pump leaves and k catalyst leaves",
            "leafCount": "L=n+k",
            "integerCharge": "Q=2k-n=3k-L",
            "label": "(k-n,-L,-L)",
            "offset": "beta=L(-1,-1,2)/3",
            "sharpDirection": "h=(1,-1,0)/sqrt(2)",
            "coefficient": (
                "w=s h+(3 q alpha/sqrt(2))(-1,-1,2)/3, "
                "ell=-sqrt(2)L alpha"
            ),
            "bEndpoint": "(n,k,L,Q)=(2N-1,N,3N-1,1)",
        },
        "generatingEquations": {
            "series": (
                "A(z,w)=sum alpha_(n,k) z^n w^k and "
                "S(z,w)=sum s_(n,k) z^n w^k"
            ),
            "operators": {
                "X": "z partial_z",
                "Y": "w partial_w",
                "L": "X+Y",
                "Q": "2Y-X",
                "bracket": "{F,G}=XF YG-YF XG",
                "Pi0": "projection onto integer charge Q=0",
            },
            "alphaEquation": (
                "(L-1)A=(1/sqrt(2))[(I-Pi0)Q^{-1}{A,QA}"
                "+Pi0 L^{-1}{A,LA}]"
            ),
            "sharpEquation": "(L-1)S=(1/sqrt(2)){A,S}",
            "canonicalVariables": {
                "definition": "r=z^2 w, xi=z^{-1}",
                "monomial": "z^n w^k=r^k xi^Q",
                "operators": "L=3r partial_r-xi partial_xi, Q=xi partial_xi",
                "bracket": (
                    "{F,G}=(r partial_r F)(xi partial_xi G)"
                    "-(xi partial_xi F)(r partial_r G)"
                ),
                "endpointExtraction": "b_N=[r^N xi^1](A,S)",
            },
            "initialScalars": {
                "A": "-6sqrt(2) z+3sqrt(2)t w",
                "S": "(p/sqrt(2))z-sqrt(2)q t w",
            },
        },
        "runs": runs,
        "checks": checks,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
        },
        "git": git_source_state(),
        "wallSeconds": time.perf_counter() - started,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-parameter",
        type=int,
        default=75,
        help="largest b-family parameter (default: 75)",
    )
    parser.add_argument(
        "--precisions",
        type=int,
        nargs="+",
        default=list(DEFAULT_PRECISIONS),
        help="MPFR precision levels in bits",
    )
    parser.add_argument(
        "--scale-per-leaf",
        type=int,
        default=DEFAULT_SCALE_PER_LEAF,
        help="exact exponential rescaling used internally (default: 4)",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--progress-log",
        type=Path,
        help="append-only NDJSON progress record; must not already exist",
    )
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> None:
    global PROGRESS_LOG
    arguments = parse_arguments()
    if arguments.max_parameter < 25:
        raise SystemExit("--max-parameter must be at least 25")
    precisions = tuple(sorted(set(arguments.precisions)))
    if len(precisions) < 2:
        raise SystemExit("at least two precision levels are required")
    if arguments.scale_per_leaf < 1:
        raise SystemExit("--scale-per-leaf must be positive")
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new run path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(
        arguments.max_parameter,
        precisions,
        arguments.scale_per_leaf,
        arguments.progress,
    )
    if arguments.output is not None:
        atomic_json_write(arguments.output, payload, arguments.pretty)
    else:
        json.dump(
            payload,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if arguments.pretty else None,
            sort_keys=True,
        )
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
