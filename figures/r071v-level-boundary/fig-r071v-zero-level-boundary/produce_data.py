#!/usr/bin/env python3
"""Produce the R0.71V fixed-target high-frequency tangent ledger.

The calculation evaluates the exact first parameter derivative from the
R0.71U two-root implicit-function construction.  It does not integrate the
nonlinear trajectory.  The target, multiplier, background, and macroscopic
audit window remain fixed while the auxiliary frequencies grow with q.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from datetime import datetime
from pathlib import Path
import resource
import time
from zoneinfo import ZoneInfo

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo("Asia/Shanghai")


def timestamp() -> str:
    return datetime.now(TIMEZONE).isoformat(timespec="milliseconds")


def append_ndjson(path: Path, payload: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def resource_record(stage: str, started: float, **details: object) -> dict[str, object]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "timestamp": timestamp(),
        "stage": stage,
        "elapsedSeconds": time.perf_counter() - started,
        "pid": os.getpid(),
        "logicalCpuCount": os.cpu_count(),
        "loadAverage1m5m15m": list(os.getloadavg()),
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
        **details,
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_phi(beta: np.ndarray | float, time_value: np.ndarray | float, mu: float):
    return np.exp(-mu * time_value) * (-np.expm1(-beta * time_value)) / beta


def stable_phi_prime(beta: np.ndarray | float, time_value: np.ndarray | float, mu: float):
    psi = -np.expm1(-beta * time_value) / beta
    return np.exp(-mu * time_value) * (np.exp(-beta * time_value) - mu * psi)


def stable_phi_second(beta: np.ndarray | float, time_value: np.ndarray | float, mu: float):
    psi = -np.expm1(-beta * time_value) / beta
    return np.exp(-mu * time_value) * (
        -(beta + 2.0 * mu) * np.exp(-beta * time_value) + mu * mu * psi
    )


def piecewise_quad(function, points: list[float], config: dict[str, object]) -> tuple[float, float]:
    cleaned = sorted(set(float(value) for value in points))
    total = 0.0
    error = 0.0
    quadrature = config["quadrature"]
    for left, right in zip(cleaned[:-1], cleaned[1:], strict=True):
        if right <= left:
            continue
        value, estimate = quad(
            function,
            left,
            right,
            epsabs=float(quadrature["absoluteTolerance"]),
            epsrel=float(quadrature["relativeTolerance"]),
            limit=int(quadrature["limit"]),
        )
        total += value
        error += estimate
    return float(total), float(error)


def critical_height(
    function,
    derivative,
    left: float,
    right: float,
    q_value: int,
    early_cutoff: float,
) -> tuple[float, float, int]:
    scaled_left = q_value * q_value * left
    scaled_right = q_value * q_value * right
    scaled_stop = min(scaled_right, max(early_cutoff * 1.5, scaled_left))
    scaled_grid = np.linspace(scaled_left, scaled_stop, 1401) / (q_value * q_value)
    macro_start = max(left, scaled_stop / (q_value * q_value))
    macro_grid = np.linspace(macro_start, right, 801)
    grid = np.unique(np.concatenate(([left, right], scaled_grid, macro_grid)))
    derivative_values = np.asarray([float(derivative(value)) for value in grid])
    candidates = [left, right]
    for index in range(1, len(grid)):
        a_value = derivative_values[index - 1]
        b_value = derivative_values[index]
        if a_value == 0.0:
            candidates.append(float(grid[index - 1]))
        if a_value * b_value < 0.0:
            candidates.append(float(brentq(derivative, grid[index - 1], grid[index])))
    values = [abs(float(function(value))) for value in candidates]
    maximum_index = int(np.argmax(values))
    return values[maximum_index], candidates[maximum_index], len(candidates)


def fit_power(q_values: list[int], values: list[float], tail: int = 4) -> float:
    x_values = np.log(np.asarray(q_values[-tail:], dtype=float))
    y_values = np.log(np.asarray(values[-tail:], dtype=float))
    return float(np.polyfit(x_values, y_values, 1)[0])


def limit_profile(config: dict[str, object]) -> dict[str, object]:
    nu = float(config["viscosity"])
    modulus = int(config["modulus"])
    mode_ratios = np.asarray(config["modeRatios"], dtype=float)
    roots = np.asarray(config["scaledRoots"], dtype=float)
    recurrence_count = int(config["recurrenceCount"])
    l_value = float(config["target"]["Kz"])
    b_values = 2.0 * nu * modulus * modulus * mode_ratios**2

    def psi(beta: float, value: float) -> float:
        return float(-np.expm1(-beta * value) / beta)

    evaluation = np.asarray([
        [psi(b_values[column], root) for column in range(recurrence_count + 1)]
        for root in roots
    ])
    coefficients = np.concatenate((
        np.asarray([1.0]),
        np.linalg.solve(evaluation[:, 1:], -evaluation[:, 0]),
    ))

    def gamma(value):
        value_array = np.asarray(value)
        total = np.zeros_like(value_array, dtype=float)
        for coefficient, beta in zip(
            coefficients, b_values[: recurrence_count + 1], strict=True
        ):
            total += coefficient * (-np.expm1(-beta * value_array)) / beta
        return l_value * total

    def gamma_prime(value):
        value_array = np.asarray(value)
        total = np.zeros_like(value_array, dtype=float)
        for coefficient, beta in zip(
            coefficients, b_values[: recurrence_count + 1], strict=True
        ):
            total += coefficient * np.exp(-beta * value_array)
        return l_value * total

    def gamma_second(value):
        value_array = np.asarray(value)
        total = np.zeros_like(value_array, dtype=float)
        for coefficient, beta in zip(
            coefficients, b_values[: recurrence_count + 1], strict=True
        ):
            total -= coefficient * beta * np.exp(-beta * value_array)
        return l_value * total

    return {
        "bValues": b_values.tolist(),
        "coefficients": coefficients.tolist(),
        "gamma": gamma,
        "gammaPrime": gamma_prime,
        "gammaSecond": gamma_second,
    }


def build_case(q_value: int, config: dict[str, object], started: float) -> dict[str, object]:
    nu = float(config["viscosity"])
    ky = int(config["target"]["Ky"])
    l_value = int(config["target"]["Kz"])
    kappa = float(config["target"]["shellScaleKappaStar"])
    multiplier = float(config["target"]["targetMultiplierMStar"])
    modulus = int(config["modulus"])
    recurrence_count = int(config["recurrenceCount"])
    mode_ratios = np.asarray(config["modeRatios"], dtype=float)
    scaled_roots = np.asarray(config["scaledRoots"], dtype=float)
    scaled_launch_offset = float(config["auditWindow"]["scaledLaunchOffset"])
    ell = float(config["auditWindow"]["length"])
    background_q = int(config["background"]["frequency"])
    background_b = float(config["background"]["fourierCoefficient"])
    early_cutoff = float(config["quadrature"]["scaledEarlyCutoff"])

    rho_squared = float(ky * ky + l_value * l_value)
    declared_rho_squared = float(config["target"]["waveNumberSquaredRho2"])
    if abs(rho_squared - declared_rho_squared) > 1e-14:
        raise ValueError(
            "target.waveNumberSquaredRho2 must equal Ky^2+Kz^2; "
            f"received {declared_rho_squared} versus {rho_squared}"
        )
    rho_fourth = rho_squared * rho_squared
    mu = nu * rho_squared
    epsilon = q_value ** -2
    modes = modulus * mode_ratios * q_value
    beta = 2.0 * nu * modes * (modes - ky)
    alpha = (ky - modes) ** 2 + l_value * l_value
    root_times = scaled_roots / (q_value * q_value)
    window_left = scaled_launch_offset / (q_value * q_value)
    window_right = window_left + ell

    evaluation = np.asarray([
        [
            stable_phi(beta[column], root, mu)
            for column in range(recurrence_count + 1)
        ]
        for root in root_times
    ])
    coefficients = np.concatenate((
        np.asarray([1.0]),
        np.linalg.solve(evaluation[:, 1:], -evaluation[:, 0]),
    ))

    def gamma(time_value):
        values = stable_phi(beta[: recurrence_count + 1], time_value, mu)
        return float(l_value * np.dot(coefficients, values))

    def gamma_prime(time_value):
        values = stable_phi_prime(beta[: recurrence_count + 1], time_value, mu)
        return float(l_value * np.dot(coefficients, values))

    def gamma_second(time_value):
        values = stable_phi_second(beta[: recurrence_count + 1], time_value, mu)
        return float(l_value * np.dot(coefficients, values))

    def background_enstrophy(time_value):
        return (
            2.0
            * background_q**2
            * background_b**2
            * math.exp(-2.0 * nu * background_q**2 * time_value)
        )

    def enstrophy(time_value):
        seed = float(np.sum(alpha * np.exp(-2.0 * nu * alpha * time_value)))
        return background_enstrophy(time_value) + 2.0 * epsilon**2 * seed

    residuals = [abs(gamma(value)) for value in root_times]
    slopes = [abs(gamma_prime(value)) for value in root_times]
    atom_by_root = [
        2.0
        * multiplier**2
        * epsilon**2
        * slope**2
        / (kappa**2 * enstrophy(root))
        for root, slope in zip(root_times, slopes, strict=True)
    ]
    atom_mass = float(sum(atom_by_root))
    second_root_atom = float(atom_by_root[1])

    cutoff_time = min(window_right, early_cutoff / (q_value * q_value))
    breaks = [window_left, *root_times.tolist(), cutoff_time, window_right]
    first_integral, first_error = piecewise_quad(
        lambda value: (
            2.0
            * rho_fourth
            * multiplier**2
            * epsilon**2
            * gamma_prime(value) ** 2
            / (kappa**6 * enstrophy(value))
        ),
        breaks,
        config,
    )
    second_integral, second_error = piecewise_quad(
        lambda value: (
            2.0
            * rho_fourth
            * multiplier**2
            * epsilon**2
            * gamma_second(value) ** 2
            / (kappa**6 * enstrophy(value))
        ),
        breaks,
        config,
    )
    first_row = 2.0 * first_integral / ell
    second_row = 7.0 * ell * second_integral / 3.0

    target_shell_prefactors = {
        "reducedAtomToJ": 2.0 * multiplier**2 / kappa**2,
        "reducedFirstIntegralToB1Star": (
            2.0 * rho_fourth * multiplier**2 / kappa**6
        ),
        "reducedSecondIntegralToB2Star": (
            2.0 * rho_fourth * multiplier**2 / kappa**6
        ),
        "reducedHeightChargeToHSquare": (
            2.0 * rho_fourth * multiplier**2 / kappa**6
        ),
        "reducedDToD": 1.0,
        "reducedFirstIntegralToWeightedFirstRow": (
            4.0 * rho_fourth * multiplier**2 / (ell * kappa**6)
        ),
        "reducedSecondIntegralToWeightedSecondRow": (
            14.0 * ell * rho_fourth * multiplier**2 / (3.0 * kappa**6)
        ),
    }

    c_norm = math.sqrt(2.0) * rho_squared * abs(multiplier)
    excursions: list[dict[str, object]] = []
    excursion_bounds = [
        (float(root_times[0]), float(root_times[1]), "internal"),
        (float(root_times[1]), window_right, "terminal"),
    ]
    for index, (left, right, kind) in enumerate(excursion_bounds, start=1):
        raw_height, height_time, critical_count = critical_height(
            gamma, gamma_prime, left, right, q_value, early_cutoff
        )
        y_integral, y_error = piecewise_quad(
            enstrophy,
            [left, min(right, early_cutoff / (q_value * q_value)), right],
            config,
        )
        height = c_norm * epsilon * raw_height
        slope_norm = c_norm * epsilon * abs(gamma_prime(left))
        d_factor = (
            height**2
            * enstrophy(left)
            / (ell * y_integral * slope_norm**2)
        )
        height_square = kappa**-6 * height**2 / (ell * y_integral)
        root_jet = kappa**-6 * slope_norm**2 / enstrophy(left)
        identity_residual = abs(height_square - d_factor * root_jet)
        identity_relative = identity_residual / max(
            abs(height_square), abs(d_factor * root_jet), 1e-300
        )
        excursions.append({
            "index": index,
            "kind": kind,
            "left": left,
            "right": right,
            "duration": right - left,
            "rawTargetHeight": raw_height,
            "heightTime": height_time,
            "criticalCandidateCount": critical_count,
            "height": height,
            "integratedEnstrophy": y_integral,
            "integratedEnstrophyError": y_error,
            "rootSlopeNorm": slope_norm,
            "rootJet": root_jet,
            "heightSquare": height_square,
            "D": d_factor,
            "heightIdentityResidual": identity_residual,
            "heightIdentityRelative": identity_relative,
        })

    minimum_non_target_radius = min(
        math.hypot(ky + modulus * q_value * integer, l_value)
        for integer in (-1, 1)
    )
    support_radius = float(config["target"]["supportRadius"])
    modular_isolated = (
        minimum_non_target_radius > support_radius
        and background_q > support_radius
        and float(np.min(modes)) > support_radius
    )
    case = {
        "q": q_value,
        "epsilon": epsilon,
        "modes": modes.astype(int).tolist(),
        "beta": beta.tolist(),
        "alpha": alpha.tolist(),
        "coefficients": coefficients.tolist(),
        "scaledRoots": scaled_roots.tolist(),
        "rootTimesFromLaunch": root_times.tolist(),
        "windowFromLaunch": [window_left, window_right],
        "targetResidualMaximum": max(residuals),
        "rootSlopeMagnitudes": slopes,
        "atomByRoot": atom_by_root,
        "atomMass": atom_mass,
        "secondRootAtom": second_root_atom,
        "firstJetIntegral": first_integral,
        "firstJetQuadratureError": first_error,
        "firstRow": first_row,
        "secondJetIntegral": second_integral,
        "secondJetQuadratureError": second_error,
        "secondRow": second_row,
        "targetShellPrefactors": target_shell_prefactors,
        "secondRootAtomOverFirstRow": second_root_atom / first_row,
        "secondRootAtomOverSecondRow": second_root_atom / second_row,
        "secondRootAtomOverTerminalHeightSquare": (
            second_root_atom / excursions[1]["heightSquare"]
        ),
        "enstrophyAtRoots": [enstrophy(value) for value in root_times],
        "enstrophyRatioOnWindow": enstrophy(window_left) / enstrophy(window_right),
        "excursions": excursions,
        "minimumNonTargetRadius": minimum_non_target_radius,
        "modularIsolated": modular_isolated,
    }
    append_ndjson(
        ROOT / "progress.ndjson",
        {
            "timestamp": timestamp(),
            "stage": "q-case-complete",
            "q": q_value,
            "targetResidualMaximum": case["targetResidualMaximum"],
            "secondRootAtom": second_root_atom,
            "totalAtomAuxiliary": atom_mass,
            "firstRow": first_row,
            "secondRow": second_row,
            "secondRootAtomOverFirstRow": case["secondRootAtomOverFirstRow"],
            "internalD": excursions[0]["D"],
            "terminalD": excursions[1]["D"],
            "elapsedSeconds": time.perf_counter() - started,
        },
    )
    append_ndjson(
        ROOT / "resource-log.ndjson",
        resource_record("q-case-complete", started, q=q_value),
    )
    return case


def data_row(
    panel: str,
    series: str,
    q_value: int | str,
    x_value: float,
    y_value: float,
    unit: str,
    formula: str,
    note: str,
) -> dict[str, object]:
    return {
        "panel": panel,
        "series": series,
        "q": q_value,
        "x": f"{x_value:.17g}",
        "y": f"{y_value:.17g}",
        "unit": unit,
        "formula": formula,
        "evidenceClass": "exact-response finite evaluation",
        "note": note,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    arguments = parser.parse_args()
    config_path = arguments.config.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    started = time.perf_counter()
    (ROOT / "progress.ndjson").write_text("", encoding="utf-8")
    (ROOT / "resource-log.ndjson").write_text("", encoding="utf-8")
    append_ndjson(
        ROOT / "progress.ndjson",
        {
            "timestamp": timestamp(),
            "stage": "start",
            "qValues": config["qValues"],
            "classification": config["classification"],
        },
    )
    append_ndjson(ROOT / "resource-log.ndjson", resource_record("start", started))

    cases = [
        build_case(int(q_value), config, started)
        for q_value in config["qValues"]
    ]
    q_values = [int(case["q"]) for case in cases]
    metrics = {
        "secondRootAtom": [float(case["secondRootAtom"]) for case in cases],
        "totalAtomAuxiliary": [float(case["atomMass"]) for case in cases],
        "firstRow": [float(case["firstRow"]) for case in cases],
        "secondRow": [float(case["secondRow"]) for case in cases],
        "terminalHeightSquare": [
            float(case["excursions"][1]["heightSquare"]) for case in cases
        ],
        "secondRootAtomOverFirstRow": [
            float(case["secondRootAtomOverFirstRow"]) for case in cases
        ],
        "secondRootAtomOverSecondRow": [
            float(case["secondRootAtomOverSecondRow"]) for case in cases
        ],
        "secondRootAtomOverTerminalHeightSquare": [
            float(case["secondRootAtomOverTerminalHeightSquare"]) for case in cases
        ],
        "internalD": [float(case["excursions"][0]["D"]) for case in cases],
        "terminalD": [float(case["excursions"][1]["D"]) for case in cases],
    }
    fitted_exponents = {
        name: fit_power(q_values, values)
        for name, values in metrics.items()
    }

    limiting = limit_profile(config)
    profile_spec = config["profile"]
    scaled_grid = np.linspace(
        float(profile_spec["scaledTimeMinimum"]),
        float(profile_spec["scaledTimeMaximum"]),
        int(profile_spec["points"]),
    )
    rows: list[dict[str, object]] = []
    for case in cases:
        q_value = int(case["q"])
        beta = np.asarray(case["beta"], dtype=float)
        coefficients = np.asarray(case["coefficients"], dtype=float)
        mu = float(config["viscosity"]) * (
            int(config["target"]["Ky"]) ** 2 + int(config["target"]["Kz"]) ** 2
        )
        l_value = float(config["target"]["Kz"])
        for scaled_time in scaled_grid:
            time_value = scaled_time / (q_value * q_value)
            profile_value = q_value * q_value * l_value * float(np.dot(
                coefficients,
                stable_phi(beta[: len(coefficients)], time_value, mu),
            ))
            rows.append(data_row(
                "A",
                "rescaled target profile",
                q_value,
                scaled_time,
                profile_value,
                "target coefficient times q^2",
                "q^2 gamma_q(r/q^2)",
                "finite-q exact response tangent",
            ))
    limit_values = limiting["gamma"](scaled_grid)
    for scaled_time, value in zip(scaled_grid, limit_values, strict=True):
        rows.append(data_row(
            "A",
            "limiting target profile",
            "limit",
            float(scaled_time),
            float(value),
            "rescaled target coefficient",
            "Gamma(r)",
            "q to infinity response limit",
        ))

    panel_b = (
        (
            "second-root atom",
            "secondRootAtom",
            "dimensionless",
            "M_{2,q}=lim_{s->0} J_{2,q}(s)/s^2",
        ),
        (
            "target-shell first row",
            "firstRow",
            "dimensionless",
            "(2/ell) B_{1,q}^{(*)}/s^2",
        ),
        (
            "target-shell second row",
            "secondRow",
            "dimensionless",
            "(7 ell/3) B_{2,q}^{(*)}/s^2",
        ),
        (
            "terminal H square",
            "terminalHeightSquare",
            "dimensionless",
            "H_terminal^2 / s^2",
        ),
    )
    panel_c = (
        (
            "second-root atom over first row",
            "secondRootAtomOverFirstRow",
            "ratio",
            "M_{2,q}/[(2/ell) B_{1,q}^{(*)}]",
        ),
        (
            "second-root atom over second row",
            "secondRootAtomOverSecondRow",
            "ratio",
            "M_{2,q}/[(7 ell/3) B_{2,q}^{(*)}]",
        ),
        (
            "second-root atom over terminal H square",
            "secondRootAtomOverTerminalHeightSquare",
            "ratio",
            "M_{2,q}/H_terminal^2",
        ),
    )
    panel_d = (
        ("internal D", "internalD", "dimensionless", "D for root 1 to root 2"),
        ("terminal D", "terminalD", "dimensionless", "D for root 2 to window end"),
    )
    for panel, definitions in (("B", panel_b), ("C", panel_c), ("D", panel_d)):
        for series, metric, unit, formula in definitions:
            for q_value, value in zip(q_values, metrics[metric], strict=True):
                rows.append(data_row(
                    panel,
                    series,
                    q_value,
                    q_value,
                    value,
                    unit,
                    formula,
                    f"tail-four fitted exponent {fitted_exponents[metric]:.8f}",
                ))

    fieldnames = [
        "panel",
        "series",
        "q",
        "x",
        "y",
        "unit",
        "formula",
        "evidenceClass",
        "note",
    ]
    with (ROOT / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (ROOT / "data.json").write_text(
        json.dumps(
            {
                "schema": fieldnames,
                "rowCount": len(rows),
                "rows": rows,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    checks = {
        "allTargetResidualsBelow1e-12": all(
            float(case["targetResidualMaximum"]) < 1e-12 for case in cases
        ),
        "allRootSlopesPositive": all(
            min(case["rootSlopeMagnitudes"]) > 0.0 for case in cases
        ),
        "allAtomsAndRowsPositive": all(
            min(
                float(case["secondRootAtom"]),
                float(case["firstRow"]),
                float(case["secondRow"]),
            )
            > 0.0
            for case in cases
        ),
        "allHeightIdentitiesRelativeBelow5e-15": all(
            max(
                float(excursion["heightIdentityRelative"])
                for excursion in case["excursions"]
            )
            < 5e-15
            for case in cases
        ),
        "allModularCasesIsolated": all(bool(case["modularIsolated"]) for case in cases),
        "allTargetShellPrefactorsMatchDeclared": all(
            all(
                abs(float(case["targetShellPrefactors"][key]) - expected) < 1e-14
                for key, expected in {
                    "reducedAtomToJ": 2.0,
                    "reducedFirstIntegralToB1Star": 8.0,
                    "reducedSecondIntegralToB2Star": 8.0,
                    "reducedHeightChargeToHSquare": 8.0,
                    "reducedDToD": 1.0,
                    "reducedFirstIntegralToWeightedFirstRow": 32.0,
                    "reducedSecondIntegralToWeightedSecondRow": 28.0 / 3.0,
                }.items()
            )
            for case in cases
        ),
        "uniformEnstrophyRatioBelow16": max(
            float(case["enstrophyRatioOnWindow"]) for case in cases
        )
        < 16.0,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    wall_seconds = time.perf_counter() - started
    results = {
        "release": config["release"],
        "figureId": config["figureId"],
        "status": "passed",
        "scope": (
            "exact response functions, exact IFT tangent, deterministic "
            "one-dimensional quadrature, and excursion ledger"
        ),
        "configSha256": sha256(config_path),
        "wallSeconds": wall_seconds,
        "cases": cases,
        "asymptoticLimit": {
            "bValues": limiting["bValues"],
            "coefficients": limiting["coefficients"],
            "rootSlopes": [
                float(abs(limiting["gammaPrime"](value)))
                for value in config["scaledRoots"]
            ],
        },
        "metrics": metrics,
        "fittedExponentsTailFour": fitted_exponents,
        "producerChecks": checks,
        "fixedTargetNormalization": {
            "targetKy": int(config["target"]["Ky"]),
            "targetKz": int(config["target"]["Kz"]),
            "rhoSquared": float(config["target"]["waveNumberSquaredRho2"]),
            "kappaStar": float(config["target"]["shellScaleKappaStar"]),
            "targetMultiplierMStar": float(
                config["target"]["targetMultiplierMStar"]
            ),
            **cases[0]["targetShellPrefactors"],
        },
        "mainEvent": {
            "rootIndex": 2,
            "scaledRoot": float(config["scaledRoots"][1]),
            "atomField": "secondRootAtom",
            "firstRootMayBePaidSeparately": True,
            "totalAtomIsAuxiliaryOnly": True,
        },
        "rowCount": len(rows),
        "claimBoundary": json.loads(
            (ROOT / "contract.json").read_text(encoding="utf-8")
        )["claimBoundary"],
    }
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    metadata = {
        "release": config["release"],
        "figureId": config["figureId"],
        "configSha256": sha256(config_path),
        "resultsSha256": sha256(ROOT / "results.json"),
        "dataCsvSha256": sha256(ROOT / "data.csv"),
        "dataJsonSha256": sha256(ROOT / "data.json"),
        "rowCount": len(rows),
        "schema": fieldnames,
        "fixedTarget": {
            "targetKy": int(config["target"]["Ky"]),
            "targetKz": int(config["target"]["Kz"]),
            "rhoSquared": float(config["target"]["waveNumberSquaredRho2"]),
            "kappaStar": float(config["target"]["shellScaleKappaStar"]),
            "targetMultiplierMStar": float(
                config["target"]["targetMultiplierMStar"]
            ),
        },
        "mainAtom": {
            "rootIndex": 2,
            "scaledRoot": float(config["scaledRoots"][1]),
            "field": "secondRootAtom",
            "totalAtomPlotted": False,
        },
        "targetShellPrefactors": cases[0]["targetShellPrefactors"],
        "evidenceMap": {
            "A": "exact response functions and their q to infinity limit",
            "B": "second prescribed-root atom plus deterministic singleton target-shell first/second jet and terminal-excursion quadratures",
            "C": "second prescribed-root atom divided by the target-shell rows and terminal excursion charge",
            "D": "exact excursion height, enstrophy, and root-slope identity",
        },
        "classification": config["classification"],
        "claimBoundary": results["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        ROOT / "progress.ndjson",
        {
            "timestamp": timestamp(),
            "stage": "producer-complete",
            "completedCases": len(cases),
            "rowCount": len(rows),
            "fittedExponents": fitted_exponents,
            "wallSeconds": wall_seconds,
        },
    )
    append_ndjson(
        ROOT / "resource-log.ndjson",
        resource_record("producer-complete", started, completedCases=len(cases)),
    )
    print(json.dumps({
        "status": "passed",
        "cases": len(cases),
        "rows": len(rows),
        "wallSeconds": wall_seconds,
        "fittedExponents": fitted_exponents,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
