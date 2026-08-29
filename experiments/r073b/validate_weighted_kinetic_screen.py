#!/usr/bin/env python3
"""Independent fail-closed validator for the R0.73B finite screen.

This validator does not import the producer.  It independently rebuilds the
raw-q and (h,r) generators, re-integrates selected cases, and writes a targeted
small-gap table.  Passing checks remain statements about finite matrices.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np


NORM_SPECS = {
    "raw_q": (-2.0, 0.0),
    "xmu": (0.0, 0.0),
    "hminus1": (0.0, 1.0),
    "balanced_l2": (1.0, 0.0),
    "kinetic": (1.0, 1.0),
    "kinetic_under": (0.5, 1.0),
    "kinetic_over": (1.5, 1.0),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path,
                        default=Path(__file__).resolve().parent)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def modes_for(n_cut: int) -> np.ndarray:
    return np.arange(-n_cut, n_cut + 1, dtype=int)


def coefficients(d_value: float) -> dict[int, complex]:
    first = math.exp(-d_value)
    second = math.exp(-4.0 * d_value)
    return {
        -2: 1j * second / 8.0,
        -1: -1j * first / 4.0,
        1: 1j * first / 4.0,
        2: -1j * second / 8.0,
    }


def raw_generator(n_cut: int, mu: float, coupling: float,
                  d_value: float) -> np.ndarray:
    modes = modes_for(n_cut)
    shifts = modes[:, None] - modes[None, :]
    w_matrix = np.zeros_like(shifts, dtype=np.complex128)
    for shift, value in coefficients(d_value).items():
        w_matrix[shifts == shift] = value
    lam = modes.astype(float) ** 2 + mu
    matrix = -np.diag(lam.astype(np.complex128))
    matrix += -1j * coupling * w_matrix * (
        1.0 - shifts.astype(float) ** 2 / lam[None, :]
    )
    return matrix


def transformed_generator(n_cut: int, mu: float, coupling: float,
                          d_value: float) -> np.ndarray:
    modes = modes_for(n_cut)
    zero = n_cut
    w = coefficients(d_value)
    matrix = np.zeros((len(modes), len(modes)), dtype=np.complex128)
    for row, n_mode in enumerate(modes):
        if n_mode == 0:
            matrix[row, row] = -mu
            for column, m_mode in enumerate(modes):
                if m_mode:
                    matrix[row, column] = (
                        -1j * coupling * w.get(-int(m_mode), 0j)
                        / (m_mode * m_mode + mu)
                    )
            continue
        matrix[row, row] = -(n_mode * n_mode + mu)
        matrix[row, zero] = (
            -1j * coupling * w.get(int(n_mode), 0j)
            * (mu - n_mode * n_mode)
        )
        for column, m_mode in enumerate(modes):
            if m_mode:
                shift = int(n_mode - m_mode)
                matrix[row, column] += (
                    -1j * coupling * w.get(shift, 0j)
                    * (1.0 - shift * shift / (m_mode * m_mode + mu))
                )
    return matrix


def rk4(n_cut: int, mu: float, coupling: float, start: float,
        end: float, dt_max: float) -> np.ndarray:
    steps = max(1, math.ceil((end - start) / dt_max))
    dt = (end - start) / steps
    propagator = np.eye(2 * n_cut + 1, dtype=np.complex128)
    d_value = start
    for _ in range(steps):
        a1 = transformed_generator(n_cut, mu, coupling, d_value)
        a2 = transformed_generator(n_cut, mu, coupling, d_value + dt / 2.0)
        a4 = transformed_generator(n_cut, mu, coupling, d_value + dt)
        k1 = a1 @ propagator
        k2 = a2 @ (propagator + dt * k1 / 2.0)
        k3 = a2 @ (propagator + dt * k2 / 2.0)
        k4 = a4 @ (propagator + dt * k3)
        propagator += dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        d_value += dt
    return propagator


def weights(n_cut: int, mu: float, norm: str) -> np.ndarray:
    modes = modes_for(n_cut)
    result = np.ones(len(modes), dtype=float)
    if norm == "raw_q":
        result[n_cut] = mu
        return result
    a_value, b_value = NORM_SPECS[norm]
    nonzero = modes != 0
    result[nonzero] = (
        mu ** (-a_value / 2.0)
        * (modes[nonzero].astype(float) ** 2 + mu) ** (-b_value / 2.0)
    )
    return result


def gain(propagator: np.ndarray, n_cut: int, mu: float, norm: str) -> float:
    diagonal = weights(n_cut, mu, norm)
    matrix = diagonal[:, None] * propagator / diagonal[None, :]
    return float(np.linalg.svd(matrix, compute_uv=False)[0])


def triangular_limit_gain(n_cut: int, lam: float, start: float,
                          end: float) -> float:
    modes = modes_for(n_cut)
    tau = end - start
    matrix = np.zeros((len(modes), len(modes)), dtype=np.complex128)
    matrix[n_cut, n_cut] = 1.0
    w_zero = {-2: 1j / 8.0, -1: -1j / 4.0,
              1: 1j / 4.0, 2: -1j / 8.0}
    for index, mode in enumerate(modes):
        if mode == 0:
            continue
        matrix[index, index] = math.exp(-mode * mode * tau)
        if int(mode) in w_zero:
            matrix[index, n_cut] = (
                1j * lam * abs(mode) * w_zero[int(mode)] * tau
                * math.exp(-mode * mode * end)
            )
    return float(np.linalg.svd(matrix, compute_uv=False)[0])


def predicted_exponent(norm: str, p_value: float) -> float:
    if norm == "raw_q":
        return max(1.0 - p_value, 0.0)
    a_value, _ = NORM_SPECS[norm]
    return max(a_value / 2.0 - p_value, 0.0)


def wx_primitive(start: float, end: float) -> float:
    return (
        0.5 * (math.exp(-start) - math.exp(-end))
        + 0.125 * (math.exp(-4.0 * start) - math.exp(-4.0 * end))
    )


def finite_energy_form_checks() -> list[dict[str, float | int]]:
    """Check the Hermitian kinetic generator against the analytic majorant."""
    rows: list[dict[str, float | int]] = []
    for n_cut in (4, 8, 12):
        for mu, lam in ((1e-6, 0.25), (1e-4, 4.0), (0.05, 16.0)):
            coupling = math.sqrt(mu) * lam
            for d_value in (0.0, 0.37, 1.2):
                diagonal = weights(n_cut, mu, "kinetic")
                generator = transformed_generator(
                    n_cut, mu, coupling, d_value
                )
                weighted = diagonal[:, None] * generator / diagonal[None, :]
                numerical = float(np.linalg.eigvalsh(
                    (weighted + weighted.conj().T) / 2.0
                )[-1])
                m_value = 0.5 * (
                    math.exp(-d_value) + math.exp(-4.0 * d_value)
                )
                majorant = -mu + abs(lam) * m_value / 2.0
                rows.append({
                    "N": n_cut,
                    "mu": mu,
                    "Lambda": lam,
                    "d": d_value,
                    "numericalAbscissa": numerical,
                    "analyticMajorant": majorant,
                    "margin": majorant - numerical,
                })
    return rows


def main() -> int:
    args = parse_args()
    directory = args.directory.resolve()
    targeted_path = directory / "targeted_asymptotics.csv"
    validation_path = directory / "validation.json"
    if not args.overwrite and (
        targeted_path.exists() or validation_path.exists()
    ):
        raise RuntimeError("validation outputs exist; use --overwrite")

    manifest = json.loads((directory / "manifest.json").read_text())
    summary = json.loads((directory / "summary.json").read_text())
    contract = json.loads((directory / "contract.json").read_text())
    with (directory / "weighted_propagator_rows.csv").open(
        encoding="utf-8"
    ) as handle:
        baseline = list(csv.DictReader(handle))

    algebra = []
    for n_cut, mu, coupling, d_value in (
        (4, 1e-3, 4.0, 0.0),
        (7, 0.05, -3.0, 0.37),
        (10, 0.25, 1.0, 1.0),
    ):
        transform = np.ones(2 * n_cut + 1)
        transform[n_cut] = mu
        conjugated = raw_generator(n_cut, mu, coupling, d_value) * (
            transform[None, :] / transform[:, None]
        )
        direct = transformed_generator(n_cut, mu, coupling, d_value)
        algebra.append({
            "N": n_cut,
            "mu": mu,
            "c": coupling,
            "d": d_value,
            "maximumEntrywiseSimilarityError": float(
                np.max(np.abs(conjugated - direct))
            ),
        })

    convergence = []
    for mu, coupling, label in (
        (1e-4, 1.0, "fixed-c"),
        (1e-8, 1.0, "fixed-c"),
        (1e-4, 4.0 * math.sqrt(1e-4), "fixed-Lambda"),
        (1e-8, 4.0 * math.sqrt(1e-8), "fixed-Lambda"),
    ):
        coarse = rk4(10, mu, coupling, 0.0, 0.75, 0.0025)
        refined = rk4(10, mu, coupling, 0.0, 0.75, 0.00125)
        expanded = rk4(14, mu, coupling, 0.0, 0.75, 0.00125)
        for norm in NORM_SPECS:
            g0 = gain(coarse, 10, mu, norm)
            g1 = gain(refined, 10, mu, norm)
            g2 = gain(expanded, 14, mu, norm)
            convergence.append({
                "family": label,
                "mu": mu,
                "c": coupling,
                "norm": norm,
                "N10Dt0025": g0,
                "N10Dt00125": g1,
                "N14Dt00125": g2,
                "stepRelativeDifference": abs(g1 - g0) / max(g1, g0),
                "modeRelativeDifference": abs(g2 - g1) / max(g2, g1),
            })

    targeted_rows = []
    for p_value in (0.0, 0.25, 0.5, 0.75, 1.0):
        for mu in tuple(10.0 ** (-exponent) for exponent in range(8, 15)):
            coupling = mu ** p_value
            propagator = rk4(10, mu, coupling, 0.0, 0.75, 0.0025)
            for norm in NORM_SPECS:
                targeted_rows.append({
                    "p": p_value,
                    "mu": mu,
                    "c": coupling,
                    "norm": norm,
                    "gain": gain(propagator, 10, mu, norm),
                    "N": 10,
                    "dtMax": 0.0025,
                    "finiteDimensionalOnly": True,
                })
    with targeted_path.open("w", newline="", encoding="utf-8") as handle:
        fields = ("p", "mu", "c", "norm", "gain", "N", "dtMax",
                  "finiteDimensionalOnly")
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(targeted_rows)

    fits = []
    for norm in NORM_SPECS:
        for p_value in (0.0, 0.25, 0.5, 0.75, 1.0):
            subset = sorted((
                row for row in targeted_rows
                if row["norm"] == norm and row["p"] == p_value
            ), key=lambda row: float(row["mu"]))[:4]
            x_values = np.log([float(row["mu"]) for row in subset])
            y_values = np.log([float(row["gain"]) for row in subset])
            slope = float(np.polyfit(x_values, y_values, 1)[0])
            observed = max(0.0, -slope)
            predicted = predicted_exponent(norm, p_value)
            fits.append({
                "norm": norm,
                "p": p_value,
                "observedDivergenceExponent": observed,
                "predictedDivergenceExponent": predicted,
                "absoluteDifference": abs(observed - predicted),
                "muRange": [float(subset[0]["mu"]),
                            float(subset[-1]["mu"])],
            })

    fixed_lambda_limits = []
    for lam in (0.25, 1.0, 4.0, 16.0):
        matches = [
            row for row in baseline
            if row["pathId"] == f"p0.5-k{lam:g}"
            and math.isclose(float(row["mu"]), 1e-8, rel_tol=0.0,
                             abs_tol=1e-20)
            and int(row["sign"]) == 1 and row["norm"] == "kinetic"
            and float(row["start"]) == 0.0 and float(row["end"]) == 0.75
        ]
        require(len(matches) == 1, f"missing fixed-Lambda row {lam}")
        numerical = float(matches[0]["gain"])
        limiting = triangular_limit_gain(10, lam, 0.0, 0.75)
        fixed_lambda_limits.append({
            "Lambda": lam,
            "mu": 1e-8,
            "finiteGain": numerical,
            "triangularLimitGain": limiting,
            "relativeDifference": abs(numerical - limiting) / limiting,
        })

    kinetic_rows = [row for row in baseline if row["norm"] == "kinetic"]
    energy_rows = finite_energy_form_checks()
    manifest_hashes_ok = all(
        (directory / record["path"]).stat().st_size == record["bytes"]
        and sha256(directory / record["path"]) == record["sha256"]
        for record in manifest["outputs"]
    )
    all_numeric_finite = all(
        math.isfinite(float(row[key]))
        for row in baseline
        for key in (
            "mu", "c", "Lambda", "gain", "logGain", "kineticLogBound",
            "boundMargin",
        )
    )
    checks = {
        "dataContract": (
            contract["release"] == "R0.73B"
            and contract["expected"]["caseCount"] == 280
            and contract["expected"]["primaryRowCount"] == len(baseline)
            and contract["expected"]["targetedRowCount"] == len(targeted_rows)
            and set(contract["norms"]) == set(NORM_SPECS)
            and all(
                contract["norms"][name]["a"] == spec[0]
                and contract["norms"][name]["b"] == spec[1]
                for name, spec in NORM_SPECS.items()
            )
            and all(
                set(contract["primaryData"][group]).issubset(baseline[0])
                for group in (
                    "identityFields", "metricFields", "orientationFields",
                )
            )
            and contract["claimBoundary"]["finiteFourierMatricesMeasured"] is True
            and all(
                contract["claimBoundary"][key] is False
                for key in (
                    "blochDirectSumProved", "galerkinTailBoundProved",
                    "infiniteDimensionalPropagatorProved",
                    "nonlinearNavierStokesProved", "squireRowIntegrated",
                )
            )
        ),
        "manifestScope": (
            manifest["finiteDimensionalOnly"] is True
            and len(manifest["limitations"]) == 5
        ),
        "producerSourceHash": (
            manifest["sourceSha256"]
            == sha256(directory / manifest["source"])
        ),
        "manifestOutputHashes": manifest_hashes_ok,
        "rowAndCaseCounts": (
            len(baseline) == 1960 and summary["rowCount"] == 1960
            and summary["caseCount"] == 280
        ),
        "allRecordedNumbersFinite": all_numeric_finite,
        "rawQToHrGeneratorSimilarity": max(
            row["maximumEntrywiseSimilarityError"] for row in algebra
        ) <= 2e-12,
        "rk4StepRefinement": max(
            row["stepRelativeDifference"] for row in convergence
        ) <= 2e-10,
        "fourierModeRefinement": max(
            row["modeRelativeDifference"] for row in convergence
        ) <= 2e-9,
        "predictedMuExponents": max(
            row["absoluteDifference"] for row in fits
        ) <= 5e-3,
        "fixedLambdaKineticTriangularLimit": max(
            row["relativeDifference"] for row in fixed_lambda_limits
        ) <= 2e-7,
        "signOrientationSymmetry": (
            summary["maximumSignOrientationRelativeDifference"] <= 1e-12
        ),
        "finiteKineticPropagatorBound": all(
            float(row["logGain"]) <= float(row["kineticLogBound"]) + 5e-8
            for row in kinetic_rows
        ),
        "finiteKineticGeneratorBound": min(
            row["margin"] for row in energy_rows
        ) >= -2e-12,
        "claimBoundaryPresent": all(
            str(row["finiteDimensionalOnly"]).lower() == "true"
            for row in baseline
        ),
    }
    status = "passed" if all(checks.values()) else "failed"
    validation = {
        "schemaVersion": 1,
        "status": status,
        "finiteDimensionalOnly": True,
        "checks": checks,
        "algebra": algebra,
        "convergence": convergence,
        "asymptoticFits": fits,
        "fixedLambdaKineticLimits": fixed_lambda_limits,
        "finiteEnergyFormChecks": energy_rows,
        "maximumSimilarityError": max(
            row["maximumEntrywiseSimilarityError"] for row in algebra
        ),
        "maximumStepRelativeDifference": max(
            row["stepRelativeDifference"] for row in convergence
        ),
        "maximumModeRelativeDifference": max(
            row["modeRelativeDifference"] for row in convergence
        ),
        "maximumExponentDifference": max(
            row["absoluteDifference"] for row in fits
        ),
        "maximumTriangularLimitRelativeDifference": max(
            row["relativeDifference"] for row in fixed_lambda_limits
        ),
        "minimumGeneratorBoundMargin": min(
            row["margin"] for row in energy_rows
        ),
        "targetedCsvSha256": sha256(targeted_path),
        "validatorSha256": sha256(Path(__file__).resolve()),
        "claimBoundary": {
            "finiteMatricesChecked": True,
            "infiniteDimensionalConvergenceProved": False,
            "analyticEnergyIdentityProvedByNumerics": False,
            "GalerkinTailBoundProved": False,
            "blochDirectSumProved": False,
            "squireEstimateProved": False,
            "nonlinearNavierStokesProved": False,
        },
        "limitations": [
            "finite Fourier matrices and floating-point RK4 only",
            "exponent fits confirm sampled asymptotics rather than prove them",
            "triangular-limit comparison has no certified infinite-dimensional tail",
        ],
    }
    validation_path.write_text(canonical(validation), encoding="utf-8")
    print(canonical(validation), end="")
    require(status == "passed", "R0.73B validation failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
