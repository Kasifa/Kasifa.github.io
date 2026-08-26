#!/usr/bin/env python3
"""Independent reconstruction and artifact validation for Figure R0.71V.

This validator deliberately does not import ``produce_data.py``.  It rebuilds
the two-root interpolation at 80 digits, independently re-evaluates the
binary64 quadratures and excursions, checks every fixed target-shell
prefactor, and then inspects the rendered outputs.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import subprocess
import time
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

import mpmath as mp
import numpy as np
from PIL import Image
from scipy.integrate import quad
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo("Asia/Shanghai")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_error(actual: float, expected: float) -> float:
    return abs(actual - expected) / max(abs(actual), abs(expected), 1e-300)


def add_check(
    checks: list[dict[str, object]],
    name: str,
    passed: bool,
    observed: object,
    criterion: str,
) -> None:
    checks.append({
        "name": name,
        "passed": bool(passed),
        "observed": observed,
        "criterion": criterion,
    })


def append_log(path: Path, payload: dict[str, object]) -> None:
    payload = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        **payload,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def quadrature(function, points: list[float]) -> tuple[float, float]:
    cleaned = sorted(set(float(value) for value in points))
    total = 0.0
    error = 0.0
    for left, right in zip(cleaned[:-1], cleaned[1:], strict=True):
        if right <= left:
            continue
        value, estimate = quad(
            function,
            left,
            right,
            epsabs=1e-29,
            epsrel=8e-11,
            limit=700,
        )
        total += value
        error += estimate
    return float(total), float(error)


def maximum_on_component(
    function,
    derivative,
    left: float,
    right: float,
    q_value: int,
) -> tuple[float, float, int]:
    scaled_left = q_value * q_value * left
    scaled_right = q_value * q_value * right
    scaled_stop = min(scaled_right, 512.0)
    scaled_start = scaled_left * (1.0 + 2e-11)
    if scaled_stop > scaled_start:
        scaled_grid = np.geomspace(
            max(scaled_start, 1e-12), scaled_stop, 2601
        ) / (q_value * q_value)
    else:
        scaled_grid = np.asarray([], dtype=float)
    macro_start = max(left, scaled_stop / (q_value * q_value))
    macro_grid = np.linspace(macro_start, right, 1201)
    grid = np.unique(np.concatenate(([left, right], scaled_grid, macro_grid)))
    derivative_values = np.asarray([float(derivative(value)) for value in grid])
    candidates = [left, right]
    for index in range(1, len(grid)):
        previous = derivative_values[index - 1]
        current = derivative_values[index]
        if previous == 0.0:
            candidates.append(float(grid[index - 1]))
        if previous * current < 0.0:
            candidates.append(float(brentq(
                derivative,
                float(grid[index - 1]),
                float(grid[index]),
                xtol=1e-15,
                rtol=1e-14,
            )))
    values = np.asarray([abs(float(function(value))) for value in candidates])
    selected = int(np.argmax(values))
    return float(values[selected]), float(candidates[selected]), len(candidates)


def reconstruct_case(q_value: int, config: dict[str, object]) -> dict[str, object]:
    mp.mp.dps = 80
    nu_mp = mp.mpf(str(config["viscosity"]))
    ky = int(config["target"]["Ky"])
    kz = int(config["target"]["Kz"])
    kappa = float(config["target"]["shellScaleKappaStar"])
    m_star = float(config["target"]["targetMultiplierMStar"])
    d_value = int(config["modulus"])
    ratios = [int(value) for value in config["modeRatios"]]
    roots_scaled = [mp.mpf(str(value)) for value in config["scaledRoots"]]
    ell = float(config["auditWindow"]["length"])
    launch_scaled = float(config["auditWindow"]["scaledLaunchOffset"])
    background_q = int(config["background"]["frequency"])
    background_b = float(config["background"]["fourierCoefficient"])
    epsilon = q_value**-2
    rho_squared = float(ky * ky + kz * kz)
    rho_fourth = rho_squared**2
    mu_mp = nu_mp * mp.mpf(ky * ky + kz * kz)
    modes = [d_value * ratio * q_value for ratio in ratios]
    beta_mp = [
        2 * nu_mp * mp.mpf(mode) * mp.mpf(mode - ky)
        for mode in modes
    ]

    def phi_mp(beta_value: mp.mpf, time_value: mp.mpf) -> mp.mpf:
        return mp.exp(-mu_mp * time_value) * (
            1 - mp.exp(-beta_value * time_value)
        ) / beta_value

    root_times_mp = [root / (q_value * q_value) for root in roots_scaled]
    matrix = mp.matrix([
        [phi_mp(beta_mp[column], root_times_mp[row]) for column in (1, 2)]
        for row in range(2)
    ])
    rhs = mp.matrix([
        -phi_mp(beta_mp[0], root_times_mp[row]) for row in range(2)
    ])
    solved = mp.lu_solve(matrix, rhs)
    coefficients_mp = [mp.mpf(1), solved[0], solved[1]]
    coefficient_floats = np.asarray([float(value) for value in coefficients_mp])
    beta = np.asarray([float(value) for value in beta_mp], dtype=float)
    mu = float(mu_mp)

    def phi_float(beta_values: np.ndarray, time_value: float) -> np.ndarray:
        return (
            np.exp(-mu * time_value)
            * (-np.expm1(-beta_values * time_value))
            / beta_values
        )

    def gamma(time_value: float) -> float:
        return float(kz * np.dot(
            coefficient_floats,
            phi_float(beta[:3], time_value),
        ))

    def gamma_prime(time_value: float) -> float:
        local_beta = beta[:3]
        psi = -np.expm1(-local_beta * time_value) / local_beta
        values = np.exp(-mu * time_value) * (
            np.exp(-local_beta * time_value) - mu * psi
        )
        return float(kz * np.dot(coefficient_floats, values))

    def gamma_second(time_value: float) -> float:
        local_beta = beta[:3]
        psi = -np.expm1(-local_beta * time_value) / local_beta
        values = np.exp(-mu * time_value) * (
            -(local_beta + 2.0 * mu) * np.exp(-local_beta * time_value)
            + mu * mu * psi
        )
        return float(kz * np.dot(coefficient_floats, values))

    alpha = np.asarray([(ky - mode) ** 2 + kz * kz for mode in modes], dtype=float)

    def enstrophy(time_value: float) -> float:
        background = (
            2.0
            * background_q**2
            * background_b**2
            * math.exp(-2.0 * float(nu_mp) * background_q**2 * time_value)
        )
        seeds = 2.0 * epsilon**2 * float(np.sum(
            alpha * np.exp(-2.0 * float(nu_mp) * alpha * time_value)
        ))
        return background + seeds

    roots = [float(value) for value in root_times_mp]
    root_residuals_high_precision = []
    for root in root_times_mp:
        value = mp.mpf(kz) * sum(
            coefficient * phi_mp(beta_value, root)
            for coefficient, beta_value in zip(
                coefficients_mp, beta_mp[:3], strict=True
            )
        )
        root_residuals_high_precision.append(float(abs(value)))
    slopes = [abs(gamma_prime(root)) for root in roots]
    reduced_atoms = [
        epsilon**2 * slope**2 / enstrophy(root)
        for slope, root in zip(slopes, roots, strict=True)
    ]
    full_atoms = [2.0 * m_star**2 * value / kappa**2 for value in reduced_atoms]

    window_left = launch_scaled / q_value**2
    window_right = window_left + ell
    cutoff = min(window_right, 32.0 / q_value**2)
    breaks = [window_left, *roots, cutoff, window_right]
    reduced_b1, b1_error = quadrature(
        lambda time_value: (
            epsilon**2 * gamma_prime(time_value) ** 2 / enstrophy(time_value)
        ),
        breaks,
    )
    reduced_b2, b2_error = quadrature(
        lambda time_value: (
            epsilon**2 * gamma_second(time_value) ** 2 / enstrophy(time_value)
        ),
        breaks,
    )
    b1_star = 2.0 * rho_fourth * m_star**2 * reduced_b1 / kappa**6
    b2_star = 2.0 * rho_fourth * m_star**2 * reduced_b2 / kappa**6
    first_row = 2.0 * b1_star / ell
    second_row = 7.0 * ell * b2_star / 3.0

    excursions: list[dict[str, float | int | str]] = []
    bounds = [
        (roots[0], roots[1], "internal"),
        (roots[1], window_right, "terminal"),
    ]
    full_height_prefactor = 2.0 * rho_fourth * m_star**2 / kappa**6
    for root_index, (left, right, kind) in enumerate(bounds):
        raw_height, height_time, critical_count = maximum_on_component(
            gamma, gamma_prime, left, right, q_value
        )
        exposure, exposure_error = quadrature(
            enstrophy,
            [left, min(right, 32.0 / q_value**2), right],
        )
        reduced_height_charge = (
            epsilon**2 * raw_height**2 / (ell * exposure)
        )
        full_height_square = full_height_prefactor * reduced_height_charge
        d_factor = reduced_height_charge / reduced_atoms[root_index]
        excursions.append({
            "kind": kind,
            "rawHeight": raw_height,
            "heightTime": height_time,
            "criticalCount": critical_count,
            "exposure": exposure,
            "exposureError": exposure_error,
            "reducedHeightCharge": reduced_height_charge,
            "heightSquare": full_height_square,
            "D": d_factor,
        })

    return {
        "q": q_value,
        "coefficientsHighPrecision": [mp.nstr(value, 45) for value in coefficients_mp],
        "coefficients": coefficient_floats.tolist(),
        "rootResidualMaximumHighPrecision": max(root_residuals_high_precision),
        "slopes": slopes,
        "reducedAtoms": reduced_atoms,
        "fullAtoms": full_atoms,
        "reducedB1": reduced_b1,
        "reducedB2": reduced_b2,
        "B1Star": b1_star,
        "B2Star": b2_star,
        "firstRow": first_row,
        "secondRow": second_row,
        "b1QuadratureError": b1_error,
        "b2QuadratureError": b2_error,
        "excursions": excursions,
        "prefactors": {
            "JOverReducedAtom": full_atoms[1] / reduced_atoms[1],
            "B1StarOverReducedB1": b1_star / reduced_b1,
            "B2StarOverReducedB2": b2_star / reduced_b2,
            "HOverReducedHeight": (
                excursions[1]["heightSquare"]
                / excursions[1]["reducedHeightCharge"]
            ),
            "DOverReducedD": 1.0,
            "secondAtomOverFirstRowReducedFormula": (
                reduced_atoms[1] / (16.0 * reduced_b1)
            ),
            "secondAtomOverSecondRowReducedFormula": (
                3.0 * reduced_atoms[1] / (14.0 * reduced_b2)
            ),
            "secondAtomOverTerminalHeightReducedFormula": (
                reduced_atoms[1]
                / (4.0 * excursions[1]["reducedHeightCharge"])
            ),
        },
    }


def fit_power(q_values: list[int], values: list[float]) -> float:
    return float(np.polyfit(
        np.log(np.asarray(q_values[-4:], dtype=float)),
        np.log(np.asarray(values[-4:], dtype=float)),
        1,
    )[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    config_path = arguments.config.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    metadata = json.loads(
        (ROOT / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    data_json = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    with (ROOT / "data.csv").open(encoding="utf-8") as stream:
        csv_rows = list(csv.DictReader(stream))
    checks: list[dict[str, object]] = []
    append_log(ROOT / "progress.ndjson", {"stage": "independent-validation-start"})

    expected_q = [8, 16, 32, 64, 128, 256]
    observed_q = [int(case["q"]) for case in results["cases"]]
    add_check(checks, "declared q grid", observed_q == expected_q, observed_q, str(expected_q))
    add_check(
        checks,
        "configuration values",
        config["viscosity"] == 0.02
        and config["target"]["Ky"] == 1
        and config["target"]["Kz"] == 1
        and config["target"]["waveNumberSquaredRho2"] == 2.0
        and config["target"]["shellScaleKappaStar"] == 1.0
        and config["target"]["targetMultiplierMStar"] == 1.0
        and config["modulus"] == 8
        and config["recurrenceCount"] == 2
        and config["scaledRoots"] == [0.1, 0.2]
        and config["auditWindow"]["length"] == 0.5
        and config["background"] == {"frequency": 4, "fourierCoefficient": 0.25},
        config,
        "nu=.02, Ky=Kz=kappa*=m*=1, rho^2=2, d=8, N=2, roots=.1,.2, ell=.5, Q=4, B=.25",
    )
    add_check(
        checks,
        "configuration hash",
        results["configSha256"] == digest(config_path)
        and metadata["configSha256"] == digest(config_path),
        {
            "actual": digest(config_path),
            "results": results["configSha256"],
            "metadata": metadata["configSha256"],
        },
        "all recorded config SHA256 values agree",
    )
    add_check(
        checks,
        "public target metadata",
        metadata.get("fixedTarget") == {
            "targetKy": 1,
            "targetKz": 1,
            "rhoSquared": 2.0,
            "kappaStar": 1.0,
            "targetMultiplierMStar": 1.0,
        }
        and metadata.get("mainAtom") == {
            "rootIndex": 2,
            "scaledRoot": 0.2,
            "field": "secondRootAtom",
            "totalAtomPlotted": False,
        },
        {
            "fixedTarget": metadata.get("fixedTarget"),
            "mainAtom": metadata.get("mainAtom"),
        },
        "metadata identifies targetKz and the second-root main atom",
    )

    reconstructions = [reconstruct_case(q_value, config) for q_value in expected_q]
    maximum_coefficient_error = 0.0
    maximum_metric_error = 0.0
    maximum_excursion_error = 0.0
    maximum_high_precision_residual = 0.0
    prefactor_observations: list[dict[str, float]] = []
    for produced, independent in zip(results["cases"], reconstructions, strict=True):
        maximum_coefficient_error = max(
            maximum_coefficient_error,
            max(
                relative_error(float(actual), float(expected))
                for actual, expected in zip(
                    produced["coefficients"],
                    independent["coefficients"],
                    strict=True,
                )
            ),
        )
        metric_pairs = [
            (produced["atomByRoot"][1], independent["fullAtoms"][1]),
            (produced["firstJetIntegral"], independent["B1Star"]),
            (produced["secondJetIntegral"], independent["B2Star"]),
            (produced["firstRow"], independent["firstRow"]),
            (produced["secondRow"], independent["secondRow"]),
            (
                produced["secondRootAtomOverFirstRow"],
                independent["prefactors"]["secondAtomOverFirstRowReducedFormula"],
            ),
            (
                produced["secondRootAtomOverSecondRow"],
                independent["prefactors"]["secondAtomOverSecondRowReducedFormula"],
            ),
            (
                produced["secondRootAtomOverTerminalHeightSquare"],
                independent["prefactors"]["secondAtomOverTerminalHeightReducedFormula"],
            ),
        ]
        maximum_metric_error = max(
            maximum_metric_error,
            max(relative_error(float(actual), float(expected)) for actual, expected in metric_pairs),
        )
        for produced_excursion, independent_excursion in zip(
            produced["excursions"], independent["excursions"], strict=True
        ):
            maximum_excursion_error = max(
                maximum_excursion_error,
                relative_error(
                    float(produced_excursion["heightSquare"]),
                    float(independent_excursion["heightSquare"]),
                ),
                relative_error(
                    float(produced_excursion["D"]),
                    float(independent_excursion["D"]),
                ),
            )
        maximum_high_precision_residual = max(
            maximum_high_precision_residual,
            float(independent["rootResidualMaximumHighPrecision"]),
        )
        prefactor_observations.append({
            key: float(value) for key, value in independent["prefactors"].items()
            if key in {
                "JOverReducedAtom",
                "B1StarOverReducedB1",
                "B2StarOverReducedB2",
                "HOverReducedHeight",
                "DOverReducedD",
            }
        })
    add_check(
        checks,
        "80-digit interpolation coefficients",
        maximum_coefficient_error < 2e-11,
        maximum_coefficient_error,
        "maximum relative difference below 2e-11",
    )
    add_check(
        checks,
        "80-digit prescribed roots",
        maximum_high_precision_residual < 1e-65,
        maximum_high_precision_residual,
        "maximum high-precision root residual below 1e-65",
    )
    add_check(
        checks,
        "independent atom and target-shell jet rows",
        maximum_metric_error < 1.5e-7,
        maximum_metric_error,
        "maximum relative difference below 1.5e-7",
    )
    add_check(
        checks,
        "independent excursion reconstruction",
        maximum_excursion_error < 2e-7,
        maximum_excursion_error,
        "maximum relative difference below 2e-7",
    )
    expected_prefactors = {
        "JOverReducedAtom": 2.0,
        "B1StarOverReducedB1": 8.0,
        "B2StarOverReducedB2": 8.0,
        "HOverReducedHeight": 8.0,
        "DOverReducedD": 1.0,
    }
    prefactors_pass = all(
        relative_error(row[key], expected) < 2e-14
        for row in prefactor_observations
        for key, expected in expected_prefactors.items()
    )
    add_check(
        checks,
        "fixed target-shell prefactors",
        prefactors_pass,
        prefactor_observations,
        "J=2*j_red, B1*=8*b1_red, B2*=8*b2_red, H^2=8*h_red^2, D unchanged",
    )

    metric_values = {
        "secondRootAtom": [item["fullAtoms"][1] for item in reconstructions],
        "firstRow": [item["firstRow"] for item in reconstructions],
        "secondRow": [item["secondRow"] for item in reconstructions],
        "terminalHeightSquare": [
            float(item["excursions"][1]["heightSquare"]) for item in reconstructions
        ],
        "secondRootAtomOverFirstRow": [
            item["fullAtoms"][1] / item["firstRow"] for item in reconstructions
        ],
        "secondRootAtomOverSecondRow": [
            item["fullAtoms"][1] / item["secondRow"] for item in reconstructions
        ],
        "secondRootAtomOverTerminalHeightSquare": [
            item["fullAtoms"][1] / float(item["excursions"][1]["heightSquare"])
            for item in reconstructions
        ],
        "internalD": [float(item["excursions"][0]["D"]) for item in reconstructions],
        "terminalD": [float(item["excursions"][1]["D"]) for item in reconstructions],
    }
    expected_powers = {
        "secondRootAtom": -4.0,
        "firstRow": -6.0,
        "secondRow": -2.0,
        "terminalHeightSquare": -8.0,
        "secondRootAtomOverFirstRow": 2.0,
        "secondRootAtomOverSecondRow": -2.0,
        "secondRootAtomOverTerminalHeightSquare": 4.0,
        "internalD": -2.0,
        "terminalD": -4.0,
    }
    independent_powers = {
        name: fit_power(expected_q, values) for name, values in metric_values.items()
    }
    add_check(
        checks,
        "tail-four asymptotic powers",
        all(
            abs(independent_powers[name] - expected) < 0.12
            for name, expected in expected_powers.items()
        ),
        independent_powers,
        "each tail-four fitted power lies within 0.12 of its analytic order",
    )
    add_check(
        checks,
        "second-root first-row no-go ratio",
        all(
            later > earlier
            for earlier, later in zip(
                metric_values["secondRootAtomOverFirstRow"][:-1],
                metric_values["secondRootAtomOverFirstRow"][1:],
                strict=True,
            )
        )
        and metric_values["secondRootAtomOverFirstRow"][-1] > 2500,
        metric_values["secondRootAtomOverFirstRow"],
        "strictly increasing and above 2500 at q=256",
    )

    expected_row_count = 7 * int(config["profile"]["points"]) + (4 + 3 + 2) * 6
    add_check(
        checks,
        "plot-data row count",
        len(csv_rows) == data_json["rowCount"] == metadata["rowCount"] == expected_row_count,
        {
            "csv": len(csv_rows),
            "json": data_json["rowCount"],
            "metadata": metadata["rowCount"],
            "expected": expected_row_count,
        },
        "seven profile traces plus nine six-point ledger series",
    )
    required_series = {
        ("B", "second-root atom"),
        ("B", "target-shell first row"),
        ("B", "target-shell second row"),
        ("B", "terminal H square"),
        ("C", "second-root atom over first row"),
        ("C", "second-root atom over second row"),
        ("C", "second-root atom over terminal H square"),
        ("D", "internal D"),
        ("D", "terminal D"),
    }
    observed_series = {(row["panel"], row["series"]) for row in csv_rows}
    add_check(
        checks,
        "second-root data semantics",
        required_series <= observed_series
        and not any("total atom" in row["series"] for row in csv_rows),
        sorted(required_series & observed_series),
        "Panels B/C use only the second-root atom; total atom is not plotted",
    )
    add_check(
        checks,
        "data and results hashes",
        metadata["resultsSha256"] == digest(ROOT / "results.json")
        and metadata["dataCsvSha256"] == digest(ROOT / "data.csv")
        and metadata["dataJsonSha256"] == digest(ROOT / "data.json"),
        {
            "results": digest(ROOT / "results.json"),
            "csv": digest(ROOT / "data.csv"),
            "json": digest(ROOT / "data.json"),
        },
        "metadata SHA256 values match generated files",
    )

    caption = (ROOT / "caption.md").read_text(encoding="utf-8")
    contract = (ROOT / "figure-contract.md").read_text(encoding="utf-8")
    semantic_text = caption + "\n" + contract
    semantic_tokens = [
        "second prescribed root",
        "first root is separately paid",
        "K_y=K_z=1",
        "J=2j_{\\rm red}",
        "\\mathcal B_1^{(*)}=8b_{1,\\rm red}",
        "not a covariant",
    ]
    add_check(
        checks,
        "caption and contract semantics",
        all(token in semantic_text for token in semantic_tokens),
        {token: token in semantic_text for token in semantic_tokens},
        "second-root, notation, prefactor, and dilation boundaries are explicit",
    )

    required_artifacts = [
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "qa-original.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "qa-report.md",
    ]
    missing_artifacts = [name for name in required_artifacts if not (ROOT / name).is_file()]
    add_check(
        checks,
        "required rendered artifacts",
        not missing_artifacts,
        missing_artifacts,
        "all PDF/SVG/600-dpi PNG and QA assets exist",
    )
    if not missing_artifacts:
        with Image.open(ROOT / "figure.png") as image:
            archive_size = image.size
            archive_dpi = image.info.get("dpi", (0.0, 0.0))
        expected_width = round(
            round(float(config["figure"]["widthMillimetres"]) / 25.4, 2)
            * int(config["figure"]["pngDpi"])
        )
        expected_height = round(
            round(float(config["figure"]["heightMillimetres"]) / 25.4, 2)
            * int(config["figure"]["pngDpi"])
        )
        add_check(
            checks,
            "archival PNG geometry",
            abs(archive_size[0] - expected_width) <= 3
            and abs(archive_size[1] - expected_height) <= 3
            and min(archive_dpi) >= 599.0,
            {"pixels": archive_size, "dpi": archive_dpi},
            f"approximately {expected_width} by {expected_height} pixels at 600 dpi",
        )
        svg_root = ET.parse(ROOT / "figure.svg").getroot()
        add_check(
            checks,
            "SVG parse and dimensions",
            svg_root.tag.endswith("svg")
            and "width" in svg_root.attrib
            and "height" in svg_root.attrib,
            svg_root.attrib,
            "well-formed SVG root with width and height",
        )
        pdf_info = subprocess.run(
            ["pdfinfo", str(ROOT / "figure.pdf")],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        page_line = next(
            line for line in pdf_info.splitlines() if line.startswith("Page size:")
        )
        page_count_line = next(
            line for line in pdf_info.splitlines() if line.startswith("Pages:")
        )
        parts = page_line.split()
        page_width = float(parts[2])
        page_height = float(parts[4])
        expected_width_pt = float(config["figure"]["widthMillimetres"]) / 25.4 * 72.0
        expected_height_pt = float(config["figure"]["heightMillimetres"]) / 25.4 * 72.0
        add_check(
            checks,
            "PDF page count and final size",
            page_count_line.split(":", 1)[1].strip() == "1"
            and abs(page_width - expected_width_pt) < 0.8
            and abs(page_height - expected_height_pt) < 0.8,
            {"pages": page_count_line, "pageSize": page_line},
            "one page at declared 178.05 by 134.11 mm size",
        )
        qa_report = (ROOT / "qa-report.md").read_text(encoding="utf-8")
        add_check(
            checks,
            "final-size visual QA status",
            "PENDING" not in qa_report and qa_report.count("PASS") >= 13,
            {"pending": "PENDING" in qa_report, "passCount": qa_report.count("PASS")},
            "manual final-size, grayscale, and PDF checks all marked PASS",
        )

    log_records: dict[str, list[dict[str, object]]] = {}
    logs_valid = True
    for name in ("progress.ndjson", "resource-log.ndjson"):
        records = []
        try:
            for line in (ROOT / name).read_text(encoding="utf-8").splitlines():
                if line.strip():
                    records.append(json.loads(line))
        except (OSError, json.JSONDecodeError):
            logs_valid = False
        log_records[name] = records
        logs_valid = logs_valid and bool(records)
    add_check(
        checks,
        "process monitoring logs",
        logs_valid
        and any(item.get("stage") == "producer-complete" for item in log_records["progress.ndjson"])
        and any(item.get("stage") == "plot-complete" for item in log_records["progress.ndjson"])
        and any(item.get("stage") == "qa-complete" for item in log_records["progress.ndjson"]),
        {name: len(records) for name, records in log_records.items()},
        "parseable non-empty progress/resource logs include producer, plot, and QA stages",
    )

    elapsed = time.perf_counter() - started
    passed = all(bool(check["passed"]) for check in checks)
    payload = {
        "release": config["release"],
        "figureId": config["figureId"],
        "status": "passed" if passed else "failed",
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "method": (
            "standalone 80-digit mpmath interpolation; independent SciPy "
            "quadrature and excursion reconstruction; fixed target-shell "
            "prefactor audit; CSV/JSON/hash and PDF/SVG/PNG/final-size QA"
        ),
        "precision": "80-digit interpolation and independent IEEE binary64 quadrature",
        "checkCount": len(checks),
        "checks": checks,
        "independentPowersTailFour": independent_powers,
        "maximumRelativeErrors": {
            "coefficients": maximum_coefficient_error,
            "atomAndRows": maximum_metric_error,
            "excursions": maximum_excursion_error,
        },
        "targetShellPrefactors": expected_prefactors,
        "reconstruction": reconstructions,
        "wallSeconds": elapsed,
        "claimBoundary": results["claimBoundary"],
    }
    append_log(ROOT / "progress.ndjson", {
        "stage": "independent-validation-complete" if passed else "independent-validation-failed",
        "checkCount": len(checks),
        "elapsedSeconds": elapsed,
    })
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(ROOT / "resource-log.ndjson", {
        "stage": "independent-validation-complete" if passed else "independent-validation-failed",
        "elapsedSeconds": elapsed,
        "pid": os.getpid(),
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
    })
    arguments.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": payload["status"],
        "checkCount": len(checks),
        "maximumRelativeErrors": payload["maximumRelativeErrors"],
        "independentPowersTailFour": independent_powers,
        "wallSeconds": elapsed,
    }, indent=2, sort_keys=True))
    if not passed:
        failed_names = [check["name"] for check in checks if not check["passed"]]
        raise AssertionError(f"validation failed: {failed_names}")


if __name__ == "__main__":
    main()
