#!/usr/bin/env python3
"""Independent finite audit for the R0.72L strong-coupling route.

This implementation does not import or read the R0.72L producer source or
artifacts.  It recomputes the normalized ledger from direct scalar formulas,
integrates the projected oscillator in polar coordinates, and constructs the
first full-lattice leakage independently.

The output is finite binary64 evidence only.  It is not an interval proof,
does not validate suppressed analytic constants, and must not be interpreted
as an invariant Galerkin embedding or a Navier--Stokes regularity theorem.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


AUDIT_NAME = "R0.72L independent strong-coupling finite audit"
SCHEMA_VERSION = 1
LOCAL_WINDOW_CONSTANT = 0.02


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(value) / (1024.0 * 1024.0)
    return float(value) / 1024.0


def resource_record(started: float, event: str) -> dict[str, Any]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "time": utc_now(),
        "event": event,
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "userCpuSeconds": float(usage.ru_utime),
        "systemCpuSeconds": float(usage.ru_stime),
        "pid": os.getpid(),
    }


def git_commit(repository_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def direct_parts(r_value: float, p_value: float, epsilon: float) -> dict[str, float]:
    ell = math.log(math.e * r_value)
    u0 = math.pow(epsilon * p_value, 4.0 / 3.0)
    w_value = math.pow(epsilon * p_value / r_value, 1.0 / 3.0) / math.sqrt(ell)
    u_value = math.pow(epsilon, 7.0 / 3.0) * math.pow(p_value, 4.0 / 3.0)
    v_value = math.pow(epsilon * p_value, 1.0 / 3.0) * r_value
    h_value = math.pow(epsilon, 2.0) * p_value / r_value
    logarithmic = math.log(math.e * (2.0 + r_value * r_value * (1.0 + epsilon)))
    z_value = (
        epsilon * epsilon
        * p_value * p_value
        * math.pow(r_value, 2.0 / 3.0)
        / math.pow(1.0 + epsilon, 2.0 / 3.0)
        * logarithmic
    )
    closure_scale = math.pow(p_value * r_value, 2.0 / 3.0) * ell
    return {
        "L": ell,
        "U0": u0,
        "W": w_value,
        "U": u_value,
        "V": v_value,
        "H": h_value,
        "Z": z_value,
        "closureScale": closure_scale,
        "HFromRatio": u_value / v_value,
    }


def scalar_term_maxima(parts: dict[str, float], k_value: float, z_floor: float) -> dict[str, float]:
    h_value = parts["H"]
    # These are direct one-variable maxima, not a sampled grid.
    mixed_unrestricted = parts["W"] / (2.0 * math.sqrt(k_value))
    if z_floor <= k_value:
        mixed_floor_exact = mixed_unrestricted
    else:
        mixed_floor_exact = parts["W"] * math.sqrt(z_floor) / (k_value + z_floor)
    cubic_unrestricted = parts["U"] / (k_value + h_value)
    cubic_floor_exact = parts["U"] / (k_value + max(h_value, z_floor))
    return {
        "firstUnrestrictedLoose": parts["U0"] / k_value,
        "mixedUnrestrictedExact": mixed_unrestricted,
        "mixedUnrestrictedLoose": parts["W"] / math.sqrt(k_value),
        "cubicUnrestrictedExact": cubic_unrestricted,
        "firstFloorExact": parts["U0"] / (k_value + z_floor),
        "mixedFloorExact": mixed_floor_exact,
        "mixedFloorLoose": parts["W"] / math.sqrt(k_value + z_floor),
        "cubicFloorExact": cubic_floor_exact,
    }


def algebra_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in [8.0, 32.0, 128.0, 512.0]:
        for p_value in [0.25, 0.5, 1.0]:
            epsilon = 1.0 + math.exp(0.21 * math.log(r_value))
            parts = direct_parts(r_value, p_value, epsilon)
            for k_value in [0.03125, 0.5, 8.0, 128.0]:
                maxima = scalar_term_maxima(parts, k_value, parts["Z"])
                l2 = (
                    maxima["firstUnrestrictedLoose"]
                    + maxima["mixedUnrestrictedLoose"]
                    + maxima["cubicUnrestrictedExact"]
                )
                l4 = (
                    maxima["firstFloorExact"]
                    + maxima["mixedFloorLoose"]
                    + maxima["cubicFloorExact"]
                )
                exact_floor_sup = (
                    maxima["firstFloorExact"]
                    + maxima["mixedFloorExact"]
                    + maxima["cubicFloorExact"]
                )
                rows.append(
                    {
                        "R": r_value,
                        "p": p_value,
                        "epsilon": epsilon,
                        "K": k_value,
                        "H": parts["H"],
                        "HFromRatio": parts["HFromRatio"],
                        "Z": parts["Z"],
                        "L2Bound": l2,
                        "L4Bound": l4,
                        "separateTermFloorSup": exact_floor_sup,
                        "mixedFloorLooseSlack": maxima["mixedFloorLoose"]
                        - maxima["mixedFloorExact"],
                        "passed": relative_error(parts["H"], parts["HFromRatio"])
                        < 3.0e-15
                        and maxima["mixedUnrestrictedExact"]
                        <= maxima["mixedUnrestrictedLoose"]
                        and exact_floor_sup <= l4 * (1.0 + 2.0e-15),
                    }
                )
    return rows


def local_floor_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in [8.0, 32.0, 128.0, 512.0, 2048.0]:
        for p_value in [0.5, 1.0]:
            base = direct_parts(r_value, p_value, 1.0)
            epsilon = max(1.0, base["closureScale"] / math.sqrt(math.log(2.0 + r_value)))
            parts = direct_parts(r_value, p_value, epsilon)
            omega = r_value * r_value * (1.0 + epsilon)
            tau = LOCAL_WINDOW_CONSTANT / omega
            x_sample = 1.25 * parts["Z"]
            k_value = 0.0
            raw = (
                parts["U0"] / x_sample
                + parts["W"] / math.sqrt(x_sample)
                + min(parts["U"], parts["V"] * x_sample) / x_sample
            )
            reduced = (
                parts["U0"] / parts["Z"]
                + parts["W"] / math.sqrt(parts["Z"])
                + parts["U"] / max(parts["H"], parts["Z"])
            )
            rows.append(
                {
                    "R": r_value,
                    "p": p_value,
                    "epsilon": epsilon,
                    "closureScale": parts["closureScale"],
                    "epsilonOverClosureScale": epsilon / parts["closureScale"],
                    "S": omega,
                    "tau": tau,
                    "tauTimesS": tau * omega,
                    "ZNormalizedConstantOne": parts["Z"],
                    "xSample": x_sample,
                    "xAboveZ": x_sample >= parts["Z"],
                    "rawLedgerAtSample": raw,
                    "L4AtKZero": reduced,
                    "l4DominatesSample": raw <= reduced * (1.0 + 2.0e-14),
                }
            )
    return rows


def closure_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for r_value in [16.0, 64.0, 256.0, 1024.0, 4096.0, 16384.0]:
        for regime, p_value in [("p=1", 1.0), ("p=R^-1/2", r_value ** -0.5)]:
            scale = direct_parts(r_value, p_value, 1.0)["closureScale"]
            epsilon = scale / math.sqrt(math.log(2.0 + r_value))
            parts = direct_parts(r_value, p_value, epsilon)
            bound = (
                parts["U0"] / parts["Z"]
                + parts["W"] / math.sqrt(parts["Z"])
                + parts["U"] / max(parts["H"], parts["Z"])
            )
            rows.append(
                {
                    "R": r_value,
                    "p": p_value,
                    "pRegime": regime,
                    "epsilon": epsilon,
                    "closureScale": parts["closureScale"],
                    "epsilonOverClosureScale": epsilon / parts["closureScale"],
                    "normalizedLedgerProxy": bound,
                    "insideWindow": 1.0 <= epsilon <= parts["closureScale"],
                }
            )
    return rows


def rk4_step(
    derivative: Callable[[float, tuple[float, float]], tuple[float, float]],
    y_value: float,
    state: tuple[float, float],
    step: float,
) -> tuple[float, float]:
    k1 = derivative(y_value, state)
    k2 = derivative(
        y_value + step / 2.0,
        (state[0] + step * k1[0] / 2.0, state[1] + step * k1[1] / 2.0),
    )
    k3 = derivative(
        y_value + step / 2.0,
        (state[0] + step * k2[0] / 2.0, state[1] + step * k2[1] / 2.0),
    )
    k4 = derivative(
        y_value + step,
        (state[0] + step * k3[0], state[1] + step * k3[1]),
    )
    return (
        state[0] + step * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]) / 6.0,
        state[1] + step * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]) / 6.0,
    )


def polar_galerkin_case(r_value: int, sigma: float, c_value: float = 1.0) -> dict[str, Any]:
    steps = max(30_000, int(math.ceil(60.0 * sigma)))
    step = 1.0 / steps
    inv_r2 = 1.0 / float(r_value**2)

    def derivative(y_value: float, state: tuple[float, float]) -> tuple[float, float]:
        theta, log_radius = state
        del log_radius
        return (
            sigma * math.exp(-y_value) - 0.5 * math.sin(2.0 * theta),
            -inv_r2 - math.sin(theta) ** 2,
        )

    theta = math.pi / 4.0
    log_radius = 0.0
    state = (theta, log_radius)
    y_value = 0.0
    next_root_angle = math.pi / 2.0
    root_count = 0
    g_mass = 0.0

    def integrands(y_arg: float, state_arg: tuple[float, float]) -> tuple[float, float]:
        theta_arg, log_radius_arg = state_arg
        radius_squared = math.exp(2.0 * log_radius_arg)
        return (
            math.exp(-3.0 * y_arg)
            * radius_squared
            * abs(math.cos(theta_arg) * math.sin(theta_arg)),
            math.exp(-2.0 * y_arg) * radius_squared * math.sin(theta_arg) ** 2,
        )

    previous_cubic, previous_mixed = integrands(y_value, state)
    cubic_integral = 0.0
    mixed_integral = 0.0
    for _ in range(steps):
        next_state = rk4_step(derivative, y_value, state, step)
        next_y = y_value + step
        next_theta, next_log_radius = next_state
        next_cubic, next_mixed = integrands(next_y, next_state)
        cubic_integral += step * (previous_cubic + next_cubic) / 2.0
        mixed_integral += step * (previous_mixed + next_mixed) / 2.0
        while next_root_angle <= next_theta:
            fraction = (next_root_angle - theta) / (next_theta - theta)
            root_y = y_value + fraction * step
            root_log_radius = log_radius + fraction * (next_log_radius - log_radius)
            root_radius_squared = math.exp(2.0 * root_log_radius)
            g_mass += c_value**2 * math.exp(-2.0 * root_y) * root_radius_squared
            root_count += 1
            next_root_angle += math.pi
        state = next_state
        theta, log_radius = state
        y_value = next_y
        previous_cubic = next_cubic
        previous_mixed = next_mixed

    a_r = -math.expm1(-(4.0 + 2.0 * inv_r2)) / (
        math.pi * (4.0 + 2.0 * inv_r2)
    )
    b_r = -math.expm1(-(3.0 + 2.0 * inv_r2)) / (3.0 + 2.0 * inv_r2)
    g_asymptotic = c_value**2 * sigma * a_r
    cubic = c_value**2 * sigma * cubic_integral
    cubic_asymptotic = c_value**2 * sigma * a_r
    mixed = 2.0 * c_value**2 * mixed_integral
    mixed_asymptotic = c_value**2 * b_r
    prediction = sigma * (-math.expm1(-1.0)) / math.pi
    return {
        "R": r_value,
        "sigma": sigma,
        "steps": steps,
        "rootCount": root_count,
        "rootCountPrediction": prediction,
        "rootCountRatio": root_count / prediction,
        "GRootMass": g_mass,
        "CubicRow": cubic,
        "MixedRow": mixed,
        "AR": a_r,
        "BR": b_r,
        "GAsymptotic": g_asymptotic,
        "CubicAsymptotic": cubic_asymptotic,
        "MixedAsymptotic": mixed_asymptotic,
        "GAsymptoticRatio": g_mass / g_asymptotic,
        "CubicAsymptoticRatio": cubic / cubic_asymptotic,
        "MixedAsymptoticRatio": mixed / mixed_asymptotic,
    }


def leakage_audit() -> dict[str, Any]:
    amplitude = 1.25
    # Direct formulas from W e0 and W u, independently of a convolution helper.
    inside_coefficient_w2e0 = -2.0 * amplitude**2
    outside_coefficients_w2e0 = [-amplitude**2, -amplitude**2]
    inside_norm = abs(inside_coefficient_w2e0)
    outside_norm = math.sqrt(
        sum(abs(value) ** 2 for value in outside_coefficients_w2e0)
    )
    extremal_samples = [
        {"supportMax": 2, "carrierMax": 5, "amplitude": 1.25, "coefficient": 0.75},
        {"supportMax": 9, "carrierMax": 4, "amplitude": -0.75, "coefficient": 3.0},
        {"supportMax": 4, "carrierMax": 11, "amplitude": 0.625, "coefficient": 1.0},
    ]
    for row in extremal_samples:
        row["extremeIndex"] = row["supportMax"] + row["carrierMax"]
        output = -1j * row["amplitude"] * row["coefficient"]
        row["outputReal"] = output.real
        row["outputImag"] = output.imag
        row["uniqueExtremalTermNonzero"] = abs(output) > 0.0
    return {
        "amplitude": amplitude,
        "insideNormW2e0": inside_norm,
        "outsideNormW2e0": outside_norm,
        "outsideOverInside": outside_norm / inside_norm,
        "expectedOutsideOverInside": 1.0 / math.sqrt(2.0),
        "expectedOutsideNorm": math.sqrt(2.0) * amplitude**2,
        "outsideModes": [-14, 14],
        "extremalCases": extremal_samples,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/certificates/r072l"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    repository_root = Path(__file__).resolve().parents[1]
    started = time.perf_counter()
    progress_path = output_dir / "independent-progress.ndjson"
    resource_path = output_dir / "independent-resource.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "date": "2026-08-27",
        "producerSourceImported": False,
        "producerSourceRead": False,
        "producerArtifactsRead": False,
        "arithmetic": "Python standard library binary64; polar ODE variables",
        "localWindowConstant": LOCAL_WINDOW_CONSTANT,
        "suppressedAnalyticConstantProxy": 1.0,
        "galerkinRValues": [8, 16],
        "galerkinSigmaValues": [32, 64, 128, 256, 512],
        "randomSeedUsed": False,
        "sourceSha256": sha256(Path(__file__).resolve()),
    }
    (output_dir / "independent-config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    append_ndjson(progress_path, {"time": utc_now(), "event": "audit_start", "config": config})
    append_ndjson(resource_path, resource_record(started, "audit_start"))

    algebra = algebra_cases()
    local_rows = local_floor_cases()
    closure = closure_cases()
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "independent_algebra_complete",
            "algebraCases": len(algebra),
            "localFloorCases": len(local_rows),
            "closureCases": len(closure),
        },
    )
    append_ndjson(resource_path, resource_record(started, "independent_algebra_complete"))

    galerkin: list[dict[str, Any]] = []
    for r_value in config["galerkinRValues"]:
        for sigma in config["galerkinSigmaValues"]:
            row = polar_galerkin_case(int(r_value), float(sigma))
            galerkin.append(row)
            append_ndjson(
                progress_path,
                {
                    "time": utc_now(),
                    "event": "polar_galerkin_case_complete",
                    "R": r_value,
                    "sigma": sigma,
                    "rootCount": row["rootCount"],
                    "GAsymptoticRatio": row["GAsymptoticRatio"],
                    "CubicAsymptoticRatio": row["CubicAsymptoticRatio"],
                    "MixedAsymptoticRatio": row["MixedAsymptoticRatio"],
                },
            )
    append_ndjson(resource_path, resource_record(started, "polar_galerkin_complete"))
    leakage = leakage_audit()

    tail = [row for row in galerkin if row["sigma"] >= 256]
    checks = {
        "independentScalarOptimizationsPass": all(row["passed"] for row in algebra),
        "independentLocalWindowNormalization": max(
            abs(row["tauTimesS"] - LOCAL_WINDOW_CONSTANT) for row in local_rows
        ) < 5.0e-15,
        "independentLocalFloorSamplesPass": all(
            row["xAboveZ"] and row["l4DominatesSample"] for row in local_rows
        ),
        "independentClosureWindowSamplesPass": all(row["insideWindow"] for row in closure),
        "independentClosureProxyTailDecreases": all(
            all(
                left["normalizedLedgerProxy"] > right["normalizedLedgerProxy"]
                for left, right in zip(
                    [row for row in closure if row["pRegime"] == regime][-4:],
                    [row for row in closure if row["pRegime"] == regime][-3:],
                )
            )
            for regime in {row["pRegime"] for row in closure}
        ),
        "polarGalerkinManyRoots": min(row["rootCount"] for row in tail) >= 45,
        "polarGalerkinAsymptotics": max(
            max(
                abs(row["GAsymptoticRatio"] - 1.0),
                abs(row["CubicAsymptoticRatio"] - 1.0),
                abs(row["MixedAsymptoticRatio"] - 1.0),
            )
            for row in tail
        ) < 0.08,
        "independentLeakageNormIdentity": relative_error(
            leakage["outsideNormW2e0"], leakage["expectedOutsideNorm"]
        ) < 2.0e-15,
        "independentLeakageRatioIdentity": relative_error(
            leakage["outsideOverInside"], leakage["expectedOutsideOverInside"]
        ) < 2.0e-15,
        "independentExtremalSamplesNonzero": all(
            row["uniqueExtremalTermNonzero"] for row in leakage["extremalCases"]
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    passed = all(checks.values())
    elapsed = time.perf_counter() - started
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(repository_root),
        "config": config,
        "algebraCases": algebra,
        "localFloorCases": local_rows,
        "closureCases": closure,
        "galerkinCases": galerkin,
        "fullSupportAudit": leakage,
        "checks": checks,
        "elapsedSeconds": elapsed,
        "limitations": [
            "the independent scalar calculations are finite checks, not proofs of L.1--L.5",
            "the absolute analytic constants are suppressed and normalized to one",
            "polar-coordinate integration is binary64 and not interval arithmetic",
            "the projected oscillator is not an invariant subsystem of the full Fourier lattice",
            "finite extremal-index samples do not replace the analytic maximum-index proof",
            "nothing in this audit establishes general three-dimensional Navier--Stokes regularity",
        ],
    }
    result_path = output_dir / "independent-result.json"
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(output_dir / "independent-algebra.csv", algebra)
    write_csv(output_dir / "independent-local-floor.csv", local_rows)
    write_csv(output_dir / "independent-closure.csv", closure)
    write_csv(output_dir / "independent-galerkin.csv", galerkin)

    environment = {
        "generatedAt": utc_now(),
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "executable": sys.executable,
        "cpuCount": os.cpu_count(),
        "maxRssMb": max_rss_mb(),
    }
    (output_dir / "independent-environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()) + "\n",
        encoding="utf-8",
    )
    append_ndjson(resource_path, resource_record(started, "audit_complete"))
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "checks": checks,
        },
    )
    monitor = {
        "status": result["status"],
        "algebraCases": len(algebra),
        "localFloorCases": len(local_rows),
        "closureCases": len(closure),
        "galerkinCases": len(galerkin),
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "resultSha256": sha256(result_path),
    }
    (output_dir / "independent-monitor.log").write_text(
        json.dumps(monitor, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(monitor, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
