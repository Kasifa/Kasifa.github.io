#!/usr/bin/env python3
"""R0.28 exact rationalization and finite coefficient-ratio audit.

R0.27 reduces the negative two-generator edge to scalar coefficients
``alpha_(n,k)`` and ``s_(n,k)``.  This script removes every radical and the
quadratic generator from their recurrence by setting

    Z = -6 z,  W = 3 t w,
    A(z,w) = sqrt(2) a(Z,W),
    S(z,w) = sqrt(2) d(Z,W).

The coefficients of ``a`` are rational.  The sharp series is linear in the
two root parameters, ``d = p u + q v``, with rational ``u`` and ``v``.  The
script evaluates these three rational recurrences, proves finite sign
statements over the certified R0.20 root box, and forms exact consecutive
coefficient-ratio intervals.

The ratio intervals are finite coefficient evidence.  They do not prove
convergence of the ratios, locate a dominant singularity, or imply a
Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

import gmpy2

import generated_subspace_sharpness_audit as base


Rational = gmpy2.mpq
RationalLayer = list[Rational]
RationalField = list[RationalLayer | None]
R027_CERTIFICATE = Path(
    "research/certificates/r027/edge-generating-function.json"
)
ROOT_RADIUS = Rational(1, 1_000_000)
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, message: str) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        print(f"[R0.28 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)
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


def rational_digest(value: Rational) -> str:
    return hashlib.sha256(str(value).encode("ascii")).hexdigest()


def rational_decimal(value: Rational, digits: int = 18) -> str:
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = 256
    try:
        return format(gmpy2.mpfr(value), f".{digits}g")
    finally:
        context.precision = previous_precision


def rational_interval_decimal(
    interval: tuple[Rational, Rational], digits: int = 18
) -> list[str]:
    return [rational_decimal(endpoint, digits) for endpoint in interval]


def interval_linear(
    center: Rational,
    u_value: Rational,
    v_value: Rational,
    radius: Rational,
) -> tuple[Rational, Rational]:
    uncertainty = radius * (abs(u_value) + abs(v_value))
    return center - uncertainty, center + uncertainty


def center_to_uncertainty_ratio(
    center: Rational,
    u_value: Rational,
    v_value: Rational,
    radius: Rational,
) -> Rational:
    uncertainty = radius * (abs(u_value) + abs(v_value))
    if uncertainty == 0:
        raise ZeroDivisionError("zero root-box uncertainty")
    return abs(center) / uncertainty


def sigma_decimal(
    d_value: Rational,
    a_value: Rational,
    leaf_count: int,
) -> str:
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = 256
    try:
        d_real = gmpy2.mpfr(d_value)
        a_real = gmpy2.mpfr(a_value)
        denominator = gmpy2.sqrt(d_real**2 + a_real**2 / 12)
        denominator += gmpy2.sqrt(gmpy2.mpfr(2)) * leaf_count * abs(a_real)
        return format(-d_real / denominator, ".40g")
    finally:
        context.precision = previous_precision


def interval_divide(
    numerator: tuple[Rational, Rational],
    denominator: tuple[Rational, Rational],
) -> tuple[Rational, Rational]:
    if denominator[0] <= 0 <= denominator[1]:
        raise ZeroDivisionError("interval denominator contains zero")
    quotients = [
        numerator_endpoint / denominator_endpoint
        for numerator_endpoint in numerator
        for denominator_endpoint in denominator
    ]
    return min(quotients), max(quotients)


def interval_absolute(
    interval: tuple[Rational, Rational],
) -> tuple[Rational, Rational]:
    lower, upper = interval
    if lower <= 0 <= upper:
        return Rational(0), max(abs(lower), abs(upper))
    return min(abs(lower), abs(upper)), max(abs(lower), abs(upper))


def rational_edge_recurrence(
    maximum_leaf_count: int,
    show_progress: bool,
    started: float,
) -> tuple[RationalField, RationalField, RationalField, int]:
    """Return exact coefficients of a, u, and v indexed by (L,k)."""

    zero = Rational(0)
    one = Rational(1)
    a: RationalField = [None] * (maximum_leaf_count + 1)
    u: RationalField = [None] * (maximum_leaf_count + 1)
    v: RationalField = [None] * (maximum_leaf_count + 1)
    a[1] = [one, one]
    u[1] = [Rational(-1, 12), zero]
    v[1] = [zero, Rational(-1, 3)]
    cumulative_interactions = 0

    for leaf_count in range(2, maximum_leaf_count + 1):
        charged_a_numerator = [zero] * (leaf_count + 1)
        zero_a_numerator = [zero] * (leaf_count + 1)
        u_numerator = [zero] * (leaf_count + 1)
        v_numerator = [zero] * (leaf_count + 1)
        layer_interactions = 0

        for left_leaf_count in range(1, leaf_count):
            right_leaf_count = leaf_count - left_leaf_count
            left_a_layer = a[left_leaf_count]
            right_a_layer = a[right_leaf_count]
            right_u_layer = u[right_leaf_count]
            right_v_layer = v[right_leaf_count]
            if any(
                layer is None
                for layer in (
                    left_a_layer,
                    right_a_layer,
                    right_u_layer,
                    right_v_layer,
                )
            ):
                raise AssertionError("missing rational recurrence layer")

            for left_k, left_a in enumerate(left_a_layer):  # type: ignore[arg-type]
                if left_a == 0:
                    continue
                for right_k, right_a in enumerate(right_a_layer):  # type: ignore[arg-type]
                    right_u = right_u_layer[right_k]  # type: ignore[index]
                    right_v = right_v_layer[right_k]  # type: ignore[index]
                    if right_a == 0 and right_u == 0 and right_v == 0:
                        continue
                    output_k = left_k + right_k
                    determinant = (
                        left_leaf_count * right_k
                        - left_k * right_leaf_count
                    )
                    if determinant == 0:
                        continue
                    u_numerator[output_k] += determinant * left_a * right_u
                    v_numerator[output_k] += determinant * left_a * right_v
                    if 3 * output_k == leaf_count:
                        zero_a_numerator[output_k] += (
                            determinant
                            * right_leaf_count
                            * left_a
                            * right_a
                        )
                    else:
                        right_charge = 3 * right_k - right_leaf_count
                        charged_a_numerator[output_k] += (
                            determinant * right_charge * left_a * right_a
                        )
                    layer_interactions += 1

        next_a = [zero] * (leaf_count + 1)
        next_u = [value / (leaf_count - 1) for value in u_numerator]
        next_v = [value / (leaf_count - 1) for value in v_numerator]
        for catalyst_count in range(1, leaf_count):
            charge = 3 * catalyst_count - leaf_count
            if charge == 0:
                next_a[catalyst_count] = (
                    zero_a_numerator[catalyst_count]
                    / (leaf_count * (leaf_count - 1))
                )
            else:
                next_a[catalyst_count] = (
                    charged_a_numerator[catalyst_count]
                    / (charge * (leaf_count - 1))
                )

        a[leaf_count] = next_a
        u[leaf_count] = next_u
        v[leaf_count] = next_v
        cumulative_interactions += layer_interactions
        if leaf_count % 10 == 0 or leaf_count == maximum_leaf_count:
            progress(
                show_progress,
                started,
                f"exact rational leaves {leaf_count:3d}; "
                f"layer interactions {layer_interactions:8d}; "
                f"cumulative {cumulative_interactions:10d}",
            )

    return a, u, v, cumulative_interactions


def exact_value_record(value: Rational) -> dict[str, object]:
    numerator = gmpy2.numer(value)
    denominator = gmpy2.denom(value)
    return {
        "fraction": str(value),
        "sign": int(gmpy2.sign(value)),
        "numeratorDigits": len(str(abs(numerator))),
        "denominatorDigits": len(str(denominator)),
        "sha256": rational_digest(value),
    }


def endpoint_records(
    maximum_parameter: int,
    a: RationalField,
    u: RationalField,
    v: RationalField,
    p_center: Rational,
    q_center: Rational,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    previous: dict[str, object] | None = None

    for parameter in range(1, maximum_parameter + 1):
        leaf_count = 3 * parameter - 1
        catalyst_count = parameter
        a_value = a[leaf_count][catalyst_count]  # type: ignore[index]
        u_value = u[leaf_count][catalyst_count]  # type: ignore[index]
        v_value = v[leaf_count][catalyst_count]  # type: ignore[index]
        d_center = p_center * u_value + q_center * v_value
        d_interval = interval_linear(
            d_center,
            u_value,
            v_value,
            ROOT_RADIUS,
        )
        sign_margin = center_to_uncertainty_ratio(
            d_center,
            u_value,
            v_value,
            ROOT_RADIUS,
        )
        expected_d_sign = 1 if parameter % 2 else -1
        sign_box_certified = (
            d_interval[0] > 0 if expected_d_sign > 0 else d_interval[1] < 0
        )
        sharp_over_l_alpha = d_center / (leaf_count * a_value)
        record: dict[str, object] = {
            "parameter": parameter,
            "leafCount": leaf_count,
            "charge": 1,
            "a": exact_value_record(a_value),
            "u": exact_value_record(u_value),
            "v": exact_value_record(v_value),
            "dCenter": exact_value_record(d_center),
            "dRootBox": {
                "lower": str(d_interval[0]),
                "upper": str(d_interval[1]),
                "decimal": rational_interval_decimal(d_interval),
                "centerToUncertaintyRatio": {
                    "exact": str(sign_margin),
                    "decimal": rational_decimal(sign_margin),
                },
                "expectedParitySign": expected_d_sign,
                "signCertified": sign_box_certified,
            },
            "sharpOverLAlpha": {
                "exact": str(sharp_over_l_alpha),
                "decimal": rational_decimal(sharp_over_l_alpha),
            },
            "sigmaAtCenter": sigma_decimal(d_center, a_value, leaf_count),
        }

        if previous is not None:
            previous_a = previous["aValue"]
            previous_d_interval = previous["dInterval"]
            a_ratio = a_value / previous_a
            d_ratio = interval_divide(d_interval, previous_d_interval)
            absolute_d_ratio = interval_absolute(d_ratio)
            sharp_to_alpha_factor = (
                absolute_d_ratio[0] / abs(a_ratio),
                absolute_d_ratio[1] / abs(a_ratio),
            )
            rho_a = abs(1 / a_ratio)
            rho_d = (
                1 / absolute_d_ratio[1],
                1 / absolute_d_ratio[0],
            )
            record["consecutiveRatios"] = {
                "aNOverPrevious": {
                    "exact": str(a_ratio),
                    "decimal": rational_decimal(a_ratio),
                },
                "absoluteDOverPreviousRootBox": {
                    "lower": str(absolute_d_ratio[0]),
                    "upper": str(absolute_d_ratio[1]),
                    "decimal": rational_interval_decimal(absolute_d_ratio),
                },
                "sharpToAlphaBlockFactorRootBox": {
                    "lower": str(sharp_to_alpha_factor[0]),
                    "upper": str(sharp_to_alpha_factor[1]),
                    "decimal": rational_interval_decimal(sharp_to_alpha_factor),
                },
                "normalizedRadiusProxyA": {
                    "exact": str(rho_a),
                    "decimal": rational_decimal(rho_a),
                },
                "normalizedRadiusProxyD": {
                    "lower": str(rho_d[0]),
                    "upper": str(rho_d[1]),
                    "decimal": rational_interval_decimal(rho_d),
                },
            }

        records.append(record)
        previous = {
            "aValue": a_value,
            "dInterval": d_interval,
        }

    return records


def finite_tail_summary(
    records: list[dict[str, object]], tail_count: int
) -> dict[str, object]:
    ratio_records = [
        record for record in records if "consecutiveRatios" in record
    ]
    tail = ratio_records[-min(tail_count, len(ratio_records)) :]
    rho_a_values = [
        Rational(record["consecutiveRatios"]["normalizedRadiusProxyA"]["exact"])
        for record in tail
    ]
    rho_d_intervals = [
        (
            Rational(
                record["consecutiveRatios"]["normalizedRadiusProxyD"]["lower"]
            ),
            Rational(
                record["consecutiveRatios"]["normalizedRadiusProxyD"]["upper"]
            ),
        )
        for record in tail
    ]
    factor_intervals = [
        (
            Rational(
                record["consecutiveRatios"][
                    "sharpToAlphaBlockFactorRootBox"
                ]["lower"]
            ),
            Rational(
                record["consecutiveRatios"][
                    "sharpToAlphaBlockFactorRootBox"
                ]["upper"]
            ),
        )
        for record in tail
    ]
    a_band = min(rho_a_values), max(rho_a_values)
    d_band = (
        min(interval[0] for interval in rho_d_intervals),
        max(interval[1] for interval in rho_d_intervals),
    )
    factor_band = (
        min(interval[0] for interval in factor_intervals),
        max(interval[1] for interval in factor_intervals),
    )
    persistent_parity_from = None
    for start_index, record in enumerate(records):
        if all(
            later["dRootBox"]["signCertified"]
            for later in records[start_index:]
        ):
            persistent_parity_from = record["parameter"]
            break
    parity_records = [record for record in records if record["parameter"] >= 8]
    persistent_separation_from = None
    for start_index, record in enumerate(ratio_records):
        if all(
            Rational(later["consecutiveRatios"]["normalizedRadiusProxyD"]["upper"])
            < Rational(later["consecutiveRatios"]["normalizedRadiusProxyA"]["exact"])
            and Rational(
                later["consecutiveRatios"][
                    "sharpToAlphaBlockFactorRootBox"
                ]["lower"]
            )
            > 1
            for later in ratio_records[start_index:]
        ):
            persistent_separation_from = record["parameter"]
            break
    separation_records = [
        record
        for record in ratio_records
        if persistent_separation_from is not None
        and record["parameter"] >= persistent_separation_from
    ]
    separation_factor_band = (
        (
            min(
                Rational(
                    record["consecutiveRatios"][
                        "sharpToAlphaBlockFactorRootBox"
                    ]["lower"]
                )
                for record in separation_records
            ),
            max(
                Rational(
                    record["consecutiveRatios"][
                        "sharpToAlphaBlockFactorRootBox"
                    ]["upper"]
                )
                for record in separation_records
            ),
        )
        if separation_records
        else None
    )
    minimum_sign_margin = (
        min(
            Rational(record["dRootBox"]["centerToUncertaintyRatio"]["exact"])
            for record in parity_records
        )
        if parity_records
        else None
    )
    return {
        "tailStart": tail[0]["parameter"],
        "tailEnd": tail[-1]["parameter"],
        "allAEndpointsPositive": all(record["a"]["sign"] > 0 for record in records),
        "persistentRootBoxParitySignFrom": persistent_parity_from,
        "allRootBoxParitySignsCertifiedFrom8": bool(parity_records)
        and all(record["dRootBox"]["signCertified"] for record in parity_records),
        "minimumRootBoxSignMarginFrom8": {
            "exact": None if minimum_sign_margin is None else str(minimum_sign_margin),
            "decimal": (
                None
                if minimum_sign_margin is None
                else rational_decimal(minimum_sign_margin)
            ),
        },
        "persistentFiniteRatioSeparationFrom": persistent_separation_from,
        "persistentFiniteRatioSeparationWindow": {
            "start": persistent_separation_from,
            "end": ratio_records[-1]["parameter"],
            "sharpToAlphaBlockFactorRootBoxBand": {
                "lower": (
                    None
                    if separation_factor_band is None
                    else str(separation_factor_band[0])
                ),
                "upper": (
                    None
                    if separation_factor_band is None
                    else str(separation_factor_band[1])
                ),
                "decimal": (
                    None
                    if separation_factor_band is None
                    else rational_interval_decimal(separation_factor_band)
                ),
            },
        },
        "normalizedRadiusProxyABand": {
            "lower": str(a_band[0]),
            "upper": str(a_band[1]),
            "decimal": rational_interval_decimal(a_band),
        },
        "normalizedRadiusProxyDRootBoxBand": {
            "lower": str(d_band[0]),
            "upper": str(d_band[1]),
            "decimal": rational_interval_decimal(d_band),
        },
        "sharpToAlphaBlockFactorRootBoxBand": {
            "lower": str(factor_band[0]),
            "upper": str(factor_band[1]),
            "decimal": rational_interval_decimal(factor_band),
        },
        "finiteBandsDisjoint": d_band[1] < a_band[0],
        "finiteSharpFactorAboveOne": factor_band[0] > 1,
        "limitation": (
            "these are exact bounds for finitely many consecutive ratios, "
            "not a proof that either coefficient ratio converges"
        ),
    }


def validate_against_r027(records: list[dict[str, object]]) -> dict[str, object]:
    payload = json.loads(R027_CERTIFICATE.read_text(encoding="utf-8"))
    reference = {
        int(record["parameter"]): record
        for record in payload["runs"][-1]["endpoints"]
    }
    maximum_sigma_difference = 0.0
    maximum_ratio_difference = 0.0
    checks: dict[str, object] = {}
    for record in records:
        parameter = int(record["parameter"])
        if parameter not in reference:
            continue
        sigma_difference = abs(
            float(record["sigmaAtCenter"]) - float(reference[parameter]["sigma"])
        )
        ratio_difference = abs(
            float(record["sharpOverLAlpha"]["decimal"])
            - float(reference[parameter]["sharpOverLAlpha"])
        )
        maximum_sigma_difference = max(maximum_sigma_difference, sigma_difference)
        maximum_ratio_difference = max(maximum_ratio_difference, ratio_difference)
        checks[f"N{parameter}"] = {
            "sigmaAbsoluteDifference": sigma_difference,
            "sharpOverLAlphaAbsoluteDifference": ratio_difference,
        }
    if maximum_sigma_difference > 2e-15:
        raise AssertionError("exact rational sigma regression against R0.27 failed")
    if maximum_ratio_difference > 2e-12:
        raise AssertionError("exact rational sharp/alpha regression against R0.27 failed")
    return {
        "maximumSigmaAbsoluteDifference": maximum_sigma_difference,
        "maximumSharpOverLAlphaAbsoluteDifference": maximum_ratio_difference,
        "endpoints": checks,
    }


def build_payload(
    maximum_parameter: int,
    tail_count: int,
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    center, certified_radius, root_certificate_sha = base.load_root_center()
    if certified_radius != ROOT_RADIUS:
        raise AssertionError("unexpected R0.20 root-box radius")
    a, u, v, interaction_count = rational_edge_recurrence(
        3 * maximum_parameter - 1,
        show_progress,
        started,
    )
    records = endpoint_records(
        maximum_parameter,
        a,
        u,
        v,
        center["p"],
        center["q"],
    )
    summary = finite_tail_summary(records, tail_count)
    regression = validate_against_r027(records)
    progress(show_progress, started, "completed exact endpoint validation")
    return {
        "scope": {
            "result": (
                "exact rational factorization and finite root-box coefficient-"
                "ratio bounds on the negative edge"
            ),
            "maximumParameter": maximum_parameter,
            "maximumLeafCount": 3 * maximum_parameter - 1,
            "limitations": [
                "finite coefficient-ratio bands do not prove ratio convergence",
                "no dominant-singularity transfer theorem is proved",
                "no Navier-Stokes regularity conclusion is claimed",
            ],
        },
        "normalization": {
            "variables": "Z=-6z, W=3tw",
            "series": "A=sqrt(2)a(Z,W), S=sqrt(2)d(Z,W)",
            "sharpSplit": "d=p u+q v",
            "initialData": {
                "a": "Z+W",
                "u": "-Z/12",
                "v": "-W/3",
            },
            "rationalGeneratingEquations": {
                "a": (
                    "(L-1)a=(I-Pi0)Q^{-1}{a,Qa}"
                    "+Pi0 L^{-1}{a,La}"
                ),
                "u": "(L-1)u={a,u}",
                "v": "(L-1)v={a,v}",
            },
            "canonicalVariables": {
                "definition": "R=Z^2 W, Xi=Z^{-1}",
                "endpoint": "[R^N Xi^1](a,d)",
                "physicalRelation": "R=108t r and Xi=-xi/6",
            },
        },
        "rootBox": {
            "center": {"p": str(center["p"]), "q": str(center["q"])},
            "radius": str(certified_radius),
            "sourceSha256": root_certificate_sha,
        },
        "endpoints": records,
        "finiteTailSummary": summary,
        "checks": {"R027Regression": regression},
        "computation": {
            "backend": base.RATIONAL_BACKEND,
            "orderedInteractions": interaction_count,
            "wallSeconds": time.perf_counter() - started,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "gmp": gmpy2.mp_version(),
        },
        "git": git_source_state(),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-parameter", type=int, default=25)
    parser.add_argument("--tail-count", type=int, default=10)
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
    if arguments.max_parameter < 2:
        raise SystemExit("--max-parameter must be at least 2")
    if arguments.tail_count < 2:
        raise SystemExit("--tail-count must be at least 2")
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new run path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(
        arguments.max_parameter,
        arguments.tail_count,
        arguments.progress,
    )
    if arguments.check:
        if (
            arguments.max_parameter >= 8
            and not payload["finiteTailSummary"][
                "allRootBoxParitySignsCertifiedFrom8"
            ]
        ):
            raise AssertionError("root-box parity-sign check failed")
        if arguments.max_parameter >= 40:
            summary = payload["finiteTailSummary"]
            if not summary["allAEndpointsPositive"]:
                raise AssertionError("positive a-endpoint check failed")
            if summary["persistentFiniteRatioSeparationFrom"] != 18:
                raise AssertionError("finite ratio-separation regression")
            if not summary["finiteBandsDisjoint"]:
                raise AssertionError("finite tail ratio bands overlap")
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
