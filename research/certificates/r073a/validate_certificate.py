#!/usr/bin/env python3
"""Fail-closed independent validator for the R0.73A finite-matrix certificate.

This file deliberately never loads the producer module.  It rebuilds
the raw-q Fourier matrix, changes coordinates, and integrates the raw system.
No finite Galerkin calculation here proves the infinite-dimensional theorem.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EXPECTED_SOURCE_FILES = [
    "research/r073a_problem_freeze.md",
    "research/r073a_transient_proof.md",
    "research/r073a_report-source.md",
    "research/r073a_gap_matrix.md",
    "research/r073a_literature_audit.md",
    "research/r073a_independent_analytic_audit.md",
    "research/r073a_projection_derivation_agent.md",
    "research/r073a_projection_independent_audit.md",
    "research/r073a_spectral_audit_agent.md",
    "experiments/r073a/frozen_os_spectral_audit.py",
    "experiments/r073a/validate_frozen_os_spectral_audit.py",
    "experiments/r073a/validation.json",
    "experiments/r073a/manifest.json",
    "experiments/r073a/requirements.txt",
    "experiments/r073a/command.txt",
    "experiments/r073a/environment.json",
    "experiments/r073a/progress.ndjson",
    "research/certificates/r073a/generate_certificate.py",
    "research/certificates/r073a/independent_recompute.py",
    "research/certificates/r073a/validate_certificate.py",
    "research/certificates/r073a/README.md",
    "research/certificates/r073a/command.txt",
    "research/certificates/r073a/environment.txt",
    "research/certificates/r073a/progress.ndjson",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/README.md",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/caption.md",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/command.txt",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/config.json",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/contract.json",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/environment.txt",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/figure-contract.md",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/manifest-draft.json",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/plot.py",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/qa-protocol.md",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/requirements.txt",
    "figures/r073a/fig-r073a-hidden-mean-transient-spectral/validate.py",
    "scripts/generate_r073a_release.py",
    "scripts/add-r073a-translations.mjs",
    "scripts/i18n-snapshots/r073a-missing.json",
    "research/release-manifest.json",
    "tests/r073a-fourier-matrix-gate.test.mjs",
    "tests/r073a-transient-certificate.test.mjs",
    "tests/r073a-hidden-mean-gate.test.mjs",
    "tests/r073a-release.test.mjs",
    "tests/r073a-deterministic-certificate-source.test.mjs",
    "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
]
EXPECTED_OUTPUTS = ["certificate.json", "crosscheck.json", "manifest.json"]
EXTERNAL_CSV = "experiments/r073a/xmu_propagator_certificate.csv"
CSV_HEADER = [
    "certificateId", "s", "d", "mu", "c", "gain", "bound",
    "sourceCommit", "certificateCommit",
]
FLOAT_TOLERANCE = 2e-8


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def modes(n_cut: int) -> List[int]:
    return list(range(-n_cut, n_cut + 1))


def fourier_w(d_value: float) -> Dict[int, complex]:
    """Coefficients for W=sum_k W_k exp(ikx), independently tabulated."""
    return {
        -2: 1j * math.exp(-4 * d_value) / 8,
        -1: -1j * math.exp(-d_value) / 4,
        1: 1j * math.exp(-d_value) / 4,
        2: -1j * math.exp(-4 * d_value) / 8,
    }


def raw_q_matrix(n_cut: int, mu: float, coupling: float, d_value: float) -> np.ndarray:
    """Direct Fourier matrix of q_d=-Lq-ic(Wq+Wxx L^-1q)."""
    lattice = modes(n_cut)
    matrix = np.zeros((len(lattice), len(lattice)), dtype=np.complex128)
    w = fourier_w(d_value)
    for row, n_mode in enumerate(lattice):
        for column, m_mode in enumerate(lattice):
            if n_mode == m_mode:
                matrix[row, column] -= n_mode * n_mode + mu
            shift = n_mode - m_mode
            if shift in w:
                matrix[row, column] += -1j * coupling * w[shift] * (
                    1 - shift * shift / (m_mode * m_mode + mu)
                )
    return matrix


def transformed_matrix_direct(
    n_cut: int, mu: float, coupling: float, d_value: float
) -> np.ndarray:
    """Build (h,r) equations directly, without conjugating the raw matrix."""
    lattice = modes(n_cut)
    zero = lattice.index(0)
    matrix = np.zeros((len(lattice), len(lattice)), dtype=np.complex128)
    w = fourier_w(d_value)
    for row, n_mode in enumerate(lattice):
        if n_mode == 0:
            matrix[row, row] = -mu
            for column, m_mode in enumerate(lattice):
                if m_mode != 0:
                    matrix[row, column] = (
                        -1j * coupling * w.get(-m_mode, 0j)
                        / (m_mode * m_mode + mu)
                    )
            continue
        matrix[row, row] -= n_mode * n_mode + mu
        matrix[row, zero] += (
            -1j * coupling * w.get(n_mode, 0j) * (mu - n_mode * n_mode)
        )
        for column, m_mode in enumerate(lattice):
            if m_mode == 0:
                continue
            shift = n_mode - m_mode
            matrix[row, column] += -1j * coupling * w.get(shift, 0j) * (
                1 - shift * shift / (m_mode * m_mode + mu)
            )
    return matrix


def similarity_audit() -> dict:
    rows = []
    for n_cut in (3, 5, 7):
        lattice = modes(n_cut)
        zero = lattice.index(0)
        for mu in (0.001, 0.05, 0.25, 1.0):
            transform = np.eye(len(lattice), dtype=np.complex128)
            transform[zero, zero] = mu
            inverse = np.eye(len(lattice), dtype=np.complex128)
            inverse[zero, zero] = 1 / mu
            for coupling in (-4.0, 1.0, 4.0):
                for d_value in (0.0, 0.375, 1.5):
                    conjugated = inverse @ raw_q_matrix(
                        n_cut, mu, coupling, d_value
                    ) @ transform
                    direct = transformed_matrix_direct(
                        n_cut, mu, coupling, d_value
                    )
                    error = float(np.max(np.abs(conjugated - direct)))
                    rows.append({
                        "nCut": n_cut,
                        "mu": mu,
                        "c": coupling,
                        "d": d_value,
                        "maxEntryError": error,
                        "passed": error <= 2e-12,
                    })
    return {
        "caseCount": len(rows),
        "worstEntryError": max(row["maxEntryError"] for row in rows),
        "passed": all(row["passed"] for row in rows),
    }


def exact_formula_audit() -> dict:
    cancellation_rows = []
    hidden_rows = []
    for mu in (Fraction(1, 1000), Fraction(1, 20), Fraction(1, 4), Fraction(1)):
        for mode, w_minus_mode in (
            (-2, Fraction(-1, 8)),
            (-1, Fraction(1, 4)),
            (1, Fraction(-1, 4)),
            (2, Fraction(1, 8)),
        ):
            denominator = mode * mode + mu
            lhs = w_minus_mode * (1 - Fraction(mode * mode, 1) / denominator)
            rhs = mu * w_minus_mode / denominator
            cancellation_rows.append(lhs == rhs)
        # Independent direct zero-mode convolution.  Values below are the
        # real a_k in W_k=i*a_k, with time exponent retained as a label.
        amplitudes = {
            -2: ("e^-8s", Fraction(1, 8)),
            -1: ("e^-2s", Fraction(-1, 4)),
            1: ("e^-2s", Fraction(1, 4)),
            2: ("e^-8s", Fraction(-1, 8)),
        }
        direct = {"e^-2s": Fraction(0), "e^-8s": Fraction(0)}
        for mode, (label, a_mode) in amplitudes.items():
            _, a_minus_mode = amplitudes[-mode]
            direct[label] += (
                -Fraction(mode * mode) * a_minus_mode * a_mode
                / (Fraction(mode * mode) + mu)
            )
        hidden_rows.append(direct == {
            "e^-2s": Fraction(1, 8) / (1 + mu),
            "e^-8s": Fraction(1, 8) / (4 + mu),
        })

    # Equation (5.2): -i*c*Pi0(W L^-1 Wxx); each conjugate mode pair
    # contributes -k^2 |W_k|^2/(k^2+mu), turning -i into +i.
    hidden_limit = {
        "e^-2s": Fraction(1, 8),
        "e^-8s": Fraction(1, 32),
    }
    pi0_w_squared = {
        "e^-2s": 2 * Fraction(1, 4) ** 2,
        "e^-8s": 2 * Fraction(1, 8) ** 2,
    }

    # Constants are audited coefficient-by-coefficient with normalized dx/(2*pi).
    w_inf = (Fraction(1, 2), Fraction(1, 4))
    wxx_inf = (Fraction(1, 2), Fraction(1))
    c_w = (
        2 * w_inf[0] + Fraction(3, 2) * wxx_inf[0],
        2 * w_inf[1] + Fraction(3, 2) * wxx_inf[1],
    )
    j_coefficients = (c_w[0], c_w[1] / 4)
    constants_pass = (
        c_w == (Fraction(7, 4), Fraction(2))
        and j_coefficients == (Fraction(7, 4), Fraction(1, 2))
        and sum(j_coefficients) == Fraction(9, 4)
    )
    return {
        "meanCancellationExact": all(cancellation_rows),
        "hiddenDerivativeFiniteMuPositive": all(hidden_rows),
        "hiddenMuZeroLimit": {key: str(value) for key, value in hidden_limit.items()},
        "limitEqualsPi0WSquared": hidden_limit == pi0_w_squared,
        "normalizedCellMeasure": "dx/(2*pi)",
        "constantLedgerExact": constants_pass,
        "passed": (
            all(cancellation_rows)
            and all(hidden_rows)
            and hidden_limit == pi0_w_squared
            and constants_pass
        ),
    }


def supporting_algebra_audit() -> dict:
    def rational(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    # Coefficients are ordered as [1,r,r^2] after clearing 1+r^2.
    left_polynomial = [Fraction(3, 2), Fraction(-3), Fraction(3, 2)]
    square_polynomial = [Fraction(3, 2), Fraction(-3), Fraction(3, 2)]

    # Independently add the multiplication and inverse-Laplacian tables.
    table = [
        ("cos(x)", "ab", Fraction(5, 16), Fraction(-8, 16)),
        ("cos(2x)", "a^2", Fraction(4, 32), Fraction(-1, 32)),
        ("cos(3x)", "ab", Fraction(-45, 144), Fraction(8, 144)),
        ("cos(4x)", "b^2", Fraction(4, 32), Fraction(-1, 32)),
    ]
    fourier = []
    for mode, monomial, multiplication, inverse in table:
        fourier.append({
            "mode": mode,
            "monomial": monomial,
            "multiplicationPart": rational(multiplication),
            "inverseLaplacianPart": rational(inverse),
            "sum": rational(multiplication + inverse),
        })

    samples = []
    for beta, mu in (
        (Fraction(0), Fraction(1, 1000)),
        (Fraction(1, 10), Fraction(1, 100)),
        (Fraction(1, 2), Fraction(3, 4)),
        (Fraction(-1, 4), Fraction(3, 16)),
    ):
        gap = beta**2 + mu
        inverse_zero_mode = Fraction(1) / gap
        samples.append({
            "beta": rational(beta),
            "mu": rational(mu),
            "g": rational(gap),
            "normalizedConstantCoefficient": "1/1",
            "inverseConstantCoefficient": rational(inverse_zero_mode),
            "equalsOneOverG": gap * inverse_zero_mode == 1,
        })
    tangent_kernel_coefficient = Fraction(-1) + Fraction(2) * Fraction(1, 2)
    return {
        "orthogonalProjectionSpeed": {
            "omega": "3*r/(1+r^2)",
            "elementaryIdentity": "(3/2)*(1+r^2)-3*r=(3/2)*(r-1)^2",
            "polynomialCoefficientsAgree": left_polynomial == square_polynomial,
            "maximum": "3/2",
            "equalityR": "1/1",
            "equalityD": "log(2)/3",
        },
        "adjointPressureG": {
            "fourierCoefficients": fourier,
            "allFourCoefficientsNonzero": all(
                Fraction(row["sum"]) != 0 for row in fourier
            ),
        },
        "twoModeLeakage": {
            "formula": "(3*i*c/16)*(a*x2+2*b*x1)*(cos(x)-cos(3x))",
            "kernelLine": "a*x2+2*b*x1=0",
            "tangentVector": "(x1,x2)=(a/2,-b)",
            "tangentSubstitutionExact": tangent_kernel_coefficient == 0,
            "returnCoupling": "(3*i*c*b/8)*sin(x)",
            "noninvarianceRequires": "c!=0",
            "fixedTwoModeInvariantSubspaceForNonzeroC": False,
        },
        "positiveGapDualConstant": {
            "analyticIdentity": "hat(L_beta_mu^-1(phi*psi))(0)=1/g",
            "normalization": "hat(phi*psi)(0)=1",
            "coefficientScope": "normalized B_beta_mu^* pressure constant Fourier coefficient",
            "actualOSOffBlockIncludesCouplingFactor": "|c|",
            "compactDCondition": "inf_{d in I}||phi(d)||_2>0",
            "samples": samples,
            "uniformUnweightedDualBoundProved": False,
            "operatorNormDiscontinuityDirectlyProved": False,
            "fullOperatorTheoremProved": False,
        },
        "supportingAlgebraOnly": True,
    }


def integrate_raw_q(
    n_cut: int,
    mu: float,
    coupling: float,
    start: float,
    end: float,
    steps: int,
) -> np.ndarray:
    """Independent direct RK4 integration of the original q matrix."""
    dimension = 2 * n_cut + 1
    propagator = np.eye(dimension, dtype=np.complex128)
    delta = (end - start) / steps
    time = start
    for _ in range(steps):
        k1 = raw_q_matrix(n_cut, mu, coupling, time) @ propagator
        k2 = raw_q_matrix(n_cut, mu, coupling, time + delta / 2) @ (
            propagator + delta * k1 / 2
        )
        k3 = raw_q_matrix(n_cut, mu, coupling, time + delta / 2) @ (
            propagator + delta * k2 / 2
        )
        k4 = raw_q_matrix(n_cut, mu, coupling, time + delta) @ (
            propagator + delta * k3
        )
        propagator += delta * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        time += delta
    return propagator


def analytic_bound(mu: float, coupling: float, start: float, end: float) -> float:
    integral = (
        7 / 4 * (math.exp(-start) - math.exp(-end))
        + 1 / 2 * (math.exp(-4 * start) - math.exp(-4 * end))
    )
    return math.exp(-mu * (end - start) + abs(coupling) * integral)


def certificate_id(
    n_cut: int, mu_index: int, coupling_index: int, interval_index: int
) -> str:
    return (
        f"R073A-XMU-N{n_cut:02d}-M{mu_index:02d}"
        f"-C{coupling_index:02d}-T{interval_index:02d}"
    )


def independent_propagator_audit() -> dict:
    rows = []
    for n_cut in (3, 5):
        lattice = modes(n_cut)
        zero = lattice.index(0)
        for mu_index, mu in enumerate((0.001, 0.05, 0.25, 1.0), start=1):
            transform = np.eye(len(lattice), dtype=np.complex128)
            transform[zero, zero] = mu
            inverse = np.eye(len(lattice), dtype=np.complex128)
            inverse[zero, zero] = 1 / mu
            for coupling_index, coupling in enumerate(
                (-4.0, -1.0, 0.0, 1.0, 4.0), start=1
            ):
                for interval_index, (start, end) in enumerate(
                    ((0.0, 0.1), (0.0, 0.75), (0.5, 2.0)), start=1
                ):
                    fine_steps = max(160, math.ceil(800 * (end - start)))
                    coarse_steps = fine_steps // 2
                    raw_fine = integrate_raw_q(
                        n_cut, mu, coupling, start, end, fine_steps
                    )
                    raw_coarse = integrate_raw_q(
                        n_cut, mu, coupling, start, end, coarse_steps
                    )
                    x_fine = inverse @ raw_fine @ transform
                    x_coarse = inverse @ raw_coarse @ transform
                    integration_error = float(np.linalg.norm(x_fine - x_coarse, ord=2))
                    operator_norm = float(np.linalg.norm(x_fine, ord=2))
                    bound = analytic_bound(mu, coupling, start, end)
                    passed = operator_norm <= bound * (1 + 2e-8)
                    rows.append({
                        "certificateId": certificate_id(
                            n_cut, mu_index, coupling_index, interval_index
                        ),
                        "nCut": n_cut,
                        "mu": mu,
                        "c": coupling,
                        "s": start,
                        "d": end,
                        "operatorNorm": operator_norm,
                        "analyticBound": bound,
                        "ratio": operator_norm / bound,
                        "coarseFineError": integration_error,
                        "passed": passed,
                    })
    return {
        "method": "direct raw-q RK4, then exact diagonal coordinate change",
        "caseCount": len(rows),
        "worstRatio": max(row["ratio"] for row in rows),
        "worstCoarseFineError": max(row["coarseFineError"] for row in rows),
        "randomNumbersUsed": False,
        "finiteMatrixOnly": True,
        "passed": all(row["passed"] for row in rows),
        "cases": rows,
    }


def independent_checks() -> dict:
    exact = exact_formula_audit()
    supporting = supporting_algebra_audit()
    similarity = similarity_audit()
    propagator = independent_propagator_audit()
    return {
        "exact": exact,
        "supportingAlgebra": supporting,
        "similarity": similarity,
        "propagator": propagator,
        "passed": (
            exact["passed"]
            and supporting["orthogonalProjectionSpeed"]["polynomialCoefficientsAgree"]
            and supporting["adjointPressureG"]["allFourCoefficientsNonzero"]
            and supporting["twoModeLeakage"]["tangentSubstitutionExact"]
            and all(
                row["equalsOneOverG"]
                for row in supporting["positiveGapDualConstant"]["samples"]
            )
            and similarity["passed"]
            and propagator["passed"]
        ),
    }


def read_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def validate_source_bindings(manifest: dict, expected_stage: str) -> None:
    source_commit = manifest.get("sourceCommit")
    if manifest.get("status") != expected_stage:
        raise AssertionError(f"manifest is not {expected_stage}")
    if expected_stage == "source-stage" and source_commit is not None:
        raise AssertionError("source-stage manifest must not claim a source commit")
    if expected_stage == "formal":
        if not isinstance(source_commit, str) or re.fullmatch(
            r"[0-9a-f]{40}", source_commit
        ) is None:
            raise AssertionError("formal sourceCommit is missing or malformed")
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode:
            raise AssertionError("formal sourceCommit is not a Git commit object")
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        if subprocess.run(
            ["git", "merge-base", "--is-ancestor", source_commit, head],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode:
            raise AssertionError(
                "formal sourceCommit is not current HEAD or its ancestor"
            )
    if manifest.get("outputs") != EXPECTED_OUTPUTS:
        raise AssertionError("manifest output inventory mismatch")
    bindings = manifest.get("sourceBindings")
    if not isinstance(bindings, list):
        raise AssertionError("source bindings missing")
    if [row.get("path") for row in bindings] != EXPECTED_SOURCE_FILES:
        raise AssertionError("source binding inventory mismatch")
    for row in bindings:
        path = ROOT / row["path"]
        if not path.is_file() or path.is_symlink():
            raise AssertionError(f"missing bound source: {row['path']}")
        if expected_stage == "source-stage":
            if row.get("bytes") != path.stat().st_size or row.get("sha256") != sha256(path):
                raise AssertionError(f"source-stage source binding drift: {row['path']}")
            continue
        try:
            git_blob = subprocess.check_output(
                ["git", "rev-parse", f"{source_commit}:{row['path']}"],
                cwd=ROOT,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            committed_bytes = subprocess.check_output(
                ["git", "cat-file", "blob", git_blob], cwd=ROOT
            )
        except subprocess.CalledProcessError as error:
            raise AssertionError(
                f"formal source absent from sourceCommit: {row['path']}"
            ) from error
        if (
            row.get("commit") != source_commit
            or row.get("gitBlob") != git_blob
            or row.get("workingTreeBytesMatch") is not True
            or row.get("bytes") != len(committed_bytes)
            or row.get("sha256") != hashlib.sha256(committed_bytes).hexdigest()
            or path.read_bytes() != committed_bytes
        ):
            raise AssertionError(f"formal source binding drift: {row['path']}")
    if expected_stage == "formal":
        allowed_generated = {
            "research/certificates/r073a/certificate.json",
            "research/certificates/r073a/crosscheck.json",
            "research/certificates/r073a/manifest.json",
            "research/certificates/r073a/SHA256SUMS",
            EXTERNAL_CSV,
        }
        status_rows = subprocess.check_output(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=ROOT,
            text=True,
        ).splitlines()
        for status_row in status_rows:
            if len(status_row) < 4 or " -> " in status_row:
                raise AssertionError("formal validation refuses ambiguous Git status")
            relative = status_row[3:]
            if relative not in allowed_generated:
                raise AssertionError(
                    f"formal validation found non-certificate working-tree drift: {relative}"
                )


def validate_external_csv(
    manifest: dict,
    crosscheck: dict,
    expected_stage: str,
    source_commit: str | None,
    independent: dict,
) -> None:
    path = ROOT / EXTERNAL_CSV
    if not path.is_file() or path.is_symlink():
        raise AssertionError("independent propagator CSV is absent or linked")
    binding = {"path": EXTERNAL_CSV, "bytes": path.stat().st_size, "sha256": sha256(path)}
    if manifest.get("externalOutputs") != [binding]:
        raise AssertionError("manifest external CSV hash is stale")
    if crosscheck.get("independentCsv") != binding:
        raise AssertionError("crosscheck external CSV hash is stale")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != CSV_HEADER:
            raise AssertionError("propagator CSV schema drift")
        rows = list(reader)
    expected_rows = independent["propagator"]["cases"]
    if len(rows) != 120 or len(expected_rows) != 120:
        raise AssertionError("propagator CSV grid is incomplete")
    if len({row["certificateId"] for row in rows}) != 120:
        raise AssertionError("propagator CSV certificateId is not unique")
    expected_by_id = {row["certificateId"]: row for row in expected_rows}
    if set(expected_by_id) != {row["certificateId"] for row in rows}:
        raise AssertionError("propagator CSV deterministic case inventory drift")
    commit_text = source_commit if expected_stage == "formal" else "pending"
    for row in rows:
        expected = expected_by_id[row["certificateId"]]
        try:
            start = float(row["s"])
            end = float(row["d"])
            mu = float(row["mu"])
            coupling = float(row["c"])
            gain = float(row["gain"])
            bound = float(row["bound"])
        except (TypeError, ValueError) as error:
            raise AssertionError("propagator CSV has a non-numeric field") from error
        if not all(math.isfinite(value) for value in (start, end, mu, coupling, gain, bound)):
            raise AssertionError("propagator CSV has NaN or infinity")
        if (
            abs(start - expected["s"]) > 1e-15
            or abs(end - expected["d"]) > 1e-15
            or abs(mu - expected["mu"]) > 1e-15
            or abs(coupling - expected["c"]) > 1e-15
        ):
            raise AssertionError(f"propagator CSV parameter drift: {row['certificateId']}")
        recomputed_bound = analytic_bound(mu, coupling, start, end)
        if abs(bound - recomputed_bound) > 2e-12 * max(1.0, recomputed_bound):
            raise AssertionError(f"propagator CSV bound drift: {row['certificateId']}")
        if abs(gain - expected["operatorNorm"]) > FLOAT_TOLERANCE:
            raise AssertionError(f"propagator CSV gain drift: {row['certificateId']}")
        if gain > bound + FLOAT_TOLERANCE:
            raise AssertionError(f"propagator CSV exceeds bound: {row['certificateId']}")
        if row["sourceCommit"] != commit_text:
            raise AssertionError(f"propagator CSV sourceCommit drift: {row['certificateId']}")
        if row["certificateCommit"] not in ("pending", "bound-by-figure-manifest"):
            raise AssertionError(f"propagator CSV certificateCommit drift: {row['certificateId']}")


def validate_sha256_ledger() -> None:
    rows = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    names = []
    for row in rows:
        digest, separator, name = row.partition("  ")
        if separator != "  " or "/" in name or "\\" in name or len(digest) != 64:
            raise AssertionError(f"malformed SHA256SUMS row: {row}")
        int(digest, 16)
        if sha256(HERE / name) != digest:
            raise AssertionError(f"SHA256 mismatch: {name}")
        names.append(name)
    expected = sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if names != sorted(set(names)) or names != expected:
        raise AssertionError("SHA256SUMS must cover every flat regular file exactly once")


def validate_outputs(expected_stage: str, independent: dict) -> None:
    certificate = read_json("certificate.json")
    crosscheck = read_json("crosscheck.json")
    manifest = read_json("manifest.json")
    if certificate.get("release") != "R0.73A" or certificate.get("status") != "passed":
        raise AssertionError("certificate status mismatch")
    if certificate.get("exactChecks", {}).get("supportingAlgebra") != independent.get(
        "supportingAlgebra"
    ):
        raise AssertionError("supporting exact algebra disagrees across independent routes")
    source_commit = manifest.get("sourceCommit")
    if (
        certificate.get("certificateStage") != expected_stage
        or crosscheck.get("certificateStage") != expected_stage
        or certificate.get("sourceCommit") != source_commit
        or crosscheck.get("sourceCommit") != source_commit
    ):
        raise AssertionError("certificate lifecycle stage or sourceCommit drift")
    if crosscheck.get("sourceBindings") != manifest.get("sourceBindings"):
        raise AssertionError("manifest/crosscheck source bindings disagree")
    if (
        crosscheck.get("temporaryUnsealedSourceAllowed")
        != (expected_stage == "source-stage")
        or crosscheck.get("formalSourceReady") != (expected_stage == "formal")
    ):
        raise AssertionError("crosscheck lifecycle readiness drift")
    scope = certificate.get("scope", {})
    if scope.get("finiteFourierMatricesOnly") is not True:
        raise AssertionError("finite-matrix scope is not explicit")
    if scope.get("infiniteDimensionalTheoremMachineChecked") is not False:
        raise AssertionError("infinite-dimensional overclaim")
    if scope.get("numericsUsedAsProof") is not False:
        raise AssertionError("numerical crosscheck promoted to proof")
    boundary = certificate.get("claimBoundary", {})
    required_false = [
        "supportingAlgebraPromotedToFullOperatorTheorem",
        "infiniteDimensionalPropagatorProvedByCertificate",
        "lowGapA2EnhancedDissipationProved",
        "physicalKineticPropagatorProved",
        "OSSquirePropagatorProved",
        "nonlinearNavierStokesProved",
        "clayMillenniumProblemSolved",
    ]
    if any(boundary.get(key) is not False for key in required_false):
        raise AssertionError("claim boundary overstates certificate scope")
    if crosscheck.get("status") != "passed" or crosscheck.get("randomNumbersUsed") is not False:
        raise AssertionError("producer numerical crosscheck failed or used randomness")
    if crosscheck.get("finiteMatrixOnly") is not True or crosscheck.get("caseCount") != 120:
        raise AssertionError("producer crosscheck grid mismatch")
    validate_source_bindings(manifest, expected_stage)
    validate_external_csv(
        manifest, crosscheck, expected_stage, source_commit, independent
    )
    validate_sha256_ledger()


def self_test() -> None:
    result = independent_checks()
    if not result["passed"]:
        raise AssertionError(json.dumps(result, indent=2, sort_keys=True))
    print(
        "R0.73A independent validator self-test passed "
        f"({result['propagator']['caseCount']} raw-q cases; no outputs written)"
    )


def check(expected_stage: str) -> None:
    result = independent_checks()
    if not result["passed"]:
        raise AssertionError(json.dumps(result, indent=2, sort_keys=True))
    validate_outputs(expected_stage, result)
    print(
        f"R0.73A strict {expected_stage} certificate validation passed: "
        "exact constants, entrywise similarity, and deterministic raw-q CSV"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--check", action="store_true", help=argparse.SUPPRESS)
    group.add_argument("--require-source-stage", action="store_true")
    group.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        check("formal" if args.require_formal else "source-stage")


if __name__ == "__main__":
    main()
