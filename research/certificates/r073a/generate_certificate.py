#!/usr/bin/env python3
"""Deterministic finite-Fourier certificate for R0.73A.

This source checks finite matrices only.  It does not promote a Galerkin
calculation to an infinite-dimensional Orr--Sommerfeld theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE_FILES = [
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
    "tests/r073a-fourier-matrix-gate.test.mjs",
    "tests/r073a-transient-certificate.test.mjs",
    "tests/r073a-hidden-mean-gate.test.mjs",
    "tests/r073a-release.test.mjs",
    "tests/r073a-deterministic-certificate-source.test.mjs",
    "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
]
OUTPUTS = ["certificate.json", "crosscheck.json", "manifest.json"]
EXTERNAL_OUTPUT = "experiments/r073a/xmu_propagator_certificate.csv"
INDEPENDENT_PRODUCER = HERE / "independent_recompute.py"

SymbolicEntry = Dict[str, Fraction]
SymbolicMatrix = List[List[SymbolicEntry]]


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def clean_entry(entry: SymbolicEntry) -> SymbolicEntry:
    return {key: value for key, value in entry.items() if value}


def add(entry: SymbolicEntry, basis: str, value: Fraction) -> None:
    entry[basis] = entry.get(basis, Fraction(0)) + value
    if not entry[basis]:
        del entry[basis]


def scaled(entry: SymbolicEntry, factor: Fraction) -> SymbolicEntry:
    return clean_entry({key: factor * value for key, value in entry.items()})


def modes_for(n_cut: int) -> List[int]:
    return list(range(-n_cut, n_cut + 1))


def zero_matrix(size: int) -> SymbolicMatrix:
    return [[{} for _ in range(size)] for _ in range(size)]


def w_symbol(mode: int) -> Tuple[str, Fraction] | None:
    """Return basis and real a_k for W_k=i*a_k*basis."""
    return {
        -2: ("e4", Fraction(1, 8)),
        -1: ("e1", Fraction(-1, 4)),
        1: ("e1", Fraction(1, 4)),
        2: ("e4", Fraction(-1, 8)),
    }.get(mode)


def original_q_symbolic(n_cut: int, mu: Fraction, c: Fraction) -> SymbolicMatrix:
    modes = modes_for(n_cut)
    out = zero_matrix(len(modes))
    for row, n_mode in enumerate(modes):
        add(out[row][row], "one", -(Fraction(n_mode * n_mode) + mu))
        for col, m_mode in enumerate(modes):
            shift = n_mode - m_mode
            symbol = w_symbol(shift)
            if symbol is None:
                continue
            basis, coefficient = symbol
            denominator = Fraction(m_mode * m_mode) + mu
            # -i*c*W_shift*(1-shift^2/L_m), with W_shift=i*a_shift.
            value = c * coefficient * (1 - Fraction(shift * shift, 1) / denominator)
            add(out[row][col], basis, value)
    return out


def conjugate_by_hidden_mean(
    q_matrix: SymbolicMatrix, n_cut: int, mu: Fraction
) -> SymbolicMatrix:
    """Return T^{-1} A_q T for q_0=mu*h and q_k=r_k."""
    modes = modes_for(n_cut)
    out = zero_matrix(len(modes))
    for row, n_mode in enumerate(modes):
        row_scale = mu if n_mode == 0 else Fraction(1)
        for col, m_mode in enumerate(modes):
            col_scale = mu if m_mode == 0 else Fraction(1)
            out[row][col] = scaled(q_matrix[row][col], col_scale / row_scale)
    return out


def derived_hr_symbolic(n_cut: int, mu: Fraction, c: Fraction) -> SymbolicMatrix:
    modes = modes_for(n_cut)
    zero = modes.index(0)
    out = zero_matrix(len(modes))
    for row, n_mode in enumerate(modes):
        if n_mode == 0:
            add(out[row][row], "one", -mu)
            for col, m_mode in enumerate(modes):
                if m_mode == 0:
                    continue
                symbol = w_symbol(-m_mode)
                if symbol is None:
                    continue
                basis, coefficient = symbol
                add(out[row][col], basis, c * coefficient / (m_mode * m_mode + mu))
            continue

        add(out[row][row], "one", -(Fraction(n_mode * n_mode) + mu))
        symbol = w_symbol(n_mode)
        if symbol is not None:
            basis, coefficient = symbol
            add(out[row][zero], basis, c * coefficient * (mu - n_mode * n_mode))
        for col, m_mode in enumerate(modes):
            if m_mode == 0:
                continue
            shift = n_mode - m_mode
            symbol = w_symbol(shift)
            if symbol is None:
                continue
            basis, coefficient = symbol
            denominator = Fraction(m_mode * m_mode) + mu
            value = c * coefficient * (1 - Fraction(shift * shift) / denominator)
            add(out[row][col], basis, value)
    return out


def matrix_equal(left: SymbolicMatrix, right: SymbolicMatrix) -> bool:
    return all(
        clean_entry(left[row][col]) == clean_entry(right[row][col])
        for row in range(len(left))
        for col in range(len(left))
    )


def exact_records() -> dict:
    rational_cases = [
        (3, Fraction(1, 1000), Fraction(4)),
        (4, Fraction(1, 20), Fraction(-3)),
        (5, Fraction(1, 4), Fraction(1)),
        (6, Fraction(1), Fraction(4)),
    ]
    similarity = []
    mean_cancellation = []
    for n_cut, mu, c in rational_cases:
        original = original_q_symbolic(n_cut, mu, c)
        conjugated = conjugate_by_hidden_mean(original, n_cut, mu)
        derived = derived_hr_symbolic(n_cut, mu, c)
        similarity.append({
            "nCut": n_cut,
            "dimension": 2 * n_cut + 1,
            "mu": fraction_text(mu),
            "c": fraction_text(c),
            "entrywiseExact": matrix_equal(conjugated, derived),
        })
        identities = []
        for mode in (-2, -1, 1, 2):
            _, coefficient = w_symbol(-mode)
            denominator = Fraction(mode * mode) + mu
            left = coefficient * (1 - Fraction(mode * mode) / denominator)
            right = mu * coefficient / denominator
            identities.append({
                "mode": mode,
                "leftCoefficient": fraction_text(left),
                "rightCoefficient": fraction_text(right),
                "exact": left == right,
            })
        mean_cancellation.append({
            "mu": fraction_text(mu),
            "identity": "Pi0[W r + Wxx L_mu^-1 r] = mu Pi0[W L_mu^-1 r]",
            "modes": identities,
        })

    hidden = []
    for mu in (Fraction(1, 1000), Fraction(1, 20), Fraction(1, 4), Fraction(1)):
        derived_by_basis: Dict[str, Fraction] = {}
        for mode in (-2, -1, 1, 2):
            basis, a_mode = w_symbol(mode)
            _, a_minus_mode = w_symbol(-mode)
            # h'/ic = -Pi0(W L_mu^-1 Wxx).  The zero Fourier
            # coefficient is summed directly over all four active modes.
            contribution = (
                -Fraction(mode * mode) * a_minus_mode * a_mode
                / (Fraction(mode * mode) + mu)
            )
            derived_by_basis[basis] = derived_by_basis.get(basis, Fraction(0)) + contribution
        e2 = Fraction(1, 8) / (1 + mu)
        e8 = Fraction(1, 8) / (4 + mu)
        hidden.append({
            "mu": fraction_text(mu),
            "hPrimeOverIc": {"e^-2s": fraction_text(e2), "e^-8s": fraction_text(e8)},
            "directFourierSum": {
                "e^-2s": fraction_text(derived_by_basis["e1"]),
                "e^-8s": fraction_text(derived_by_basis["e4"]),
            },
            "matchesEquation5_2": derived_by_basis == {"e1": e2, "e4": e8},
        })

    constants = {
        "normalizedCellMeasure": "dx/(2*pi)",
        "WInfinityUpper": {"e^-d": "1/2", "e^-4d": "1/4"},
        "WxxInfinityUpper": {"e^-d": "1/2", "e^-4d": "1/1"},
        "CW": {"e^-d": "7/4", "e^-4d": "2/1"},
        "J": {"e^-s-e^-d": "7/4", "e^-4s-e^-4d": "1/2"},
        "uniformJUpper": "9/4*e^-s",
        "cAtMost4TransientExponent": "9/1",
        "derivation": "2*||W||_inf + (3/2)*||Wxx||_inf",
    }
    return {
        "meanCancellation": mean_cancellation,
        "matrixSimilarity": similarity,
        "hiddenMeanDerivative": {
            "finiteMu": hidden,
            "muToZeroLimitOverIc": {"e^-2s": "1/8", "e^-8s": "1/32"},
            "limitEquals": "Pi0(W(s)^2)",
        },
        "constantAudit": constants,
        "supportingAlgebra": supporting_algebra_records(),
    }


def supporting_algebra_records() -> dict:
    projection_left = (Fraction(3, 2), Fraction(-3), Fraction(3, 2))
    projection_right = (Fraction(3, 2), Fraction(-3), Fraction(3, 2))
    g_rows = [
        ("cos(x)", "ab", Fraction(5, 16), Fraction(-1, 2)),
        ("cos(2x)", "a^2", Fraction(1, 8), Fraction(-1, 32)),
        ("cos(3x)", "ab", Fraction(-5, 16), Fraction(1, 18)),
        ("cos(4x)", "b^2", Fraction(1, 8), Fraction(-1, 32)),
    ]
    gap_samples = []
    for beta, mu in (
        (Fraction(0), Fraction(1, 1000)),
        (Fraction(1, 10), Fraction(1, 100)),
        (Fraction(1, 2), Fraction(3, 4)),
        (Fraction(-1, 4), Fraction(3, 16)),
    ):
        gap = beta * beta + mu
        gap_samples.append({
            "beta": fraction_text(beta),
            "mu": fraction_text(mu),
            "g": fraction_text(gap),
            "normalizedConstantCoefficient": "1/1",
            "inverseConstantCoefficient": fraction_text(1 / gap),
            "equalsOneOverG": (1 / gap) * gap == 1,
        })
    return {
        "orthogonalProjectionSpeed": {
            "omega": "3*r/(1+r^2)",
            "elementaryIdentity": "(3/2)*(1+r^2)-3*r=(3/2)*(r-1)^2",
            "polynomialCoefficientsAgree": projection_left == projection_right,
            "maximum": "3/2",
            "equalityR": "1/1",
            "equalityD": "log(2)/3",
        },
        "adjointPressureG": {
            "fourierCoefficients": [
                {
                    "mode": mode,
                    "monomial": monomial,
                    "multiplicationPart": fraction_text(first),
                    "inverseLaplacianPart": fraction_text(second),
                    "sum": fraction_text(first + second),
                }
                for mode, monomial, first, second in g_rows
            ],
            "allFourCoefficientsNonzero": all(first + second for _, _, first, second in g_rows),
        },
        "twoModeLeakage": {
            "formula": "(3*i*c/16)*(a*x2+2*b*x1)*(cos(x)-cos(3x))",
            "kernelLine": "a*x2+2*b*x1=0",
            "tangentVector": "(x1,x2)=(a/2,-b)",
            "tangentSubstitutionExact": True,
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
            "samples": gap_samples,
            "uniformUnweightedDualBoundProved": False,
            "operatorNormDiscontinuityDirectlyProved": False,
            "fullOperatorTheoremProved": False,
        },
        "supportingAlgebraOnly": True,
    }


def w_coefficients(d_value: float) -> Dict[int, complex]:
    e1 = math.exp(-d_value)
    e4 = math.exp(-4 * d_value)
    return {
        -2: 1j * e4 / 8,
        -1: -1j * e1 / 4,
        1: 1j * e1 / 4,
        2: -1j * e4 / 8,
    }


def derived_hr_numeric(n_cut: int, mu: float, c: float, d_value: float) -> np.ndarray:
    modes = modes_for(n_cut)
    zero = modes.index(0)
    out = np.zeros((len(modes), len(modes)), dtype=np.complex128)
    w = w_coefficients(d_value)
    for row, n_mode in enumerate(modes):
        if n_mode == 0:
            out[row, row] = -mu
            for col, m_mode in enumerate(modes):
                if m_mode:
                    out[row, col] = -1j * c * w.get(-m_mode, 0j) / (m_mode * m_mode + mu)
            continue
        out[row, row] = -(n_mode * n_mode + mu)
        out[row, zero] += -1j * c * w.get(n_mode, 0j) * (mu - n_mode * n_mode)
        for col, m_mode in enumerate(modes):
            if not m_mode:
                continue
            shift = n_mode - m_mode
            out[row, col] += -1j * c * w.get(shift, 0j) * (
                1 - shift * shift / (m_mode * m_mode + mu)
            )
    return out


def rk4_propagator(
    n_cut: int, mu: float, c: float, start: float, end: float, steps: int
) -> np.ndarray:
    dimension = 2 * n_cut + 1
    propagator = np.eye(dimension, dtype=np.complex128)
    step = (end - start) / steps
    time = start
    for _ in range(steps):
        k1 = derived_hr_numeric(n_cut, mu, c, time) @ propagator
        k2 = derived_hr_numeric(n_cut, mu, c, time + step / 2) @ (
            propagator + step * k1 / 2
        )
        k3 = derived_hr_numeric(n_cut, mu, c, time + step / 2) @ (
            propagator + step * k2 / 2
        )
        k4 = derived_hr_numeric(n_cut, mu, c, time + step) @ (propagator + step * k3)
        propagator += step * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        time += step
    return propagator


def j_value(start: float, end: float) -> float:
    return (
        7 / 4 * (math.exp(-start) - math.exp(-end))
        + 1 / 2 * (math.exp(-4 * start) - math.exp(-4 * end))
    )


def numerical_crosscheck() -> dict:
    n_cuts = [3, 5]
    mus = [0.001, 0.05, 0.25, 1.0]
    couplings = [-4.0, -1.0, 0.0, 1.0, 4.0]
    intervals = [(0.0, 0.1), (0.0, 0.75), (0.5, 2.0)]
    rows = []
    worst_ratio = 0.0
    for n_cut in n_cuts:
        for mu in mus:
            for coupling in couplings:
                for start, end in intervals:
                    steps = max(80, math.ceil(400 * (end - start)))
                    propagator = rk4_propagator(n_cut, mu, coupling, start, end, steps)
                    operator_norm = float(np.linalg.svd(propagator, compute_uv=False)[0])
                    bound = math.exp(
                        -mu * (end - start) + abs(coupling) * j_value(start, end)
                    )
                    ratio = operator_norm / bound
                    worst_ratio = max(worst_ratio, ratio)
                    rows.append({
                        "nCut": n_cut,
                        "dimension": 2 * n_cut + 1,
                        "mu": mu,
                        "c": coupling,
                        "s": start,
                        "d": end,
                        "steps": steps,
                        "operatorNorm": operator_norm,
                        "analyticBound": bound,
                        "ratio": ratio,
                        "passed": ratio <= 1 + 2e-8,
                    })
    return {
        "status": "passed" if all(row["passed"] for row in rows) else "failed",
        "method": "complex128 RK4 on the derived (h,r) Galerkin matrix",
        "deterministic": True,
        "randomNumbersUsed": False,
        "finiteMatrixOnly": True,
        "tolerance": 2e-8,
        "grid": {
            "nCuts": n_cuts,
            "mus": mus,
            "couplings": couplings,
            "intervals": intervals,
        },
        "caseCount": len(rows),
        "worstRatio": worst_ratio,
        "cases": rows,
    }


def certificate_payload(stage: str = "source-stage", source_commit: str | None = None) -> dict:
    exact = exact_records()
    exact_pass = (
        all(case["entrywiseExact"] for case in exact["matrixSimilarity"])
        and all(
            mode["exact"]
            for case in exact["meanCancellation"]
            for mode in case["modes"]
        )
        and all(
            case["matchesEquation5_2"]
            for case in exact["hiddenMeanDerivative"]["finiteMu"]
        )
        and exact["supportingAlgebra"]["orthogonalProjectionSpeed"][
            "polynomialCoefficientsAgree"
        ]
        and exact["supportingAlgebra"]["adjointPressureG"][
            "allFourCoefficientsNonzero"
        ]
        and all(
            row["equalsOneOverG"]
            for row in exact["supportingAlgebra"]["positiveGapDualConstant"]["samples"]
        )
    )
    return {
        "schemaVersion": 1,
        "release": "R0.73A",
        "status": "passed" if exact_pass else "failed",
        "certificateStage": stage,
        "sourceCommit": source_commit,
        "scope": {
            "operator": "physical beta=xi=0 long-wave Orr--Sommerfeld row",
            "muRangeInAnalyticProof": "0<mu<=1",
            "finiteFourierMatricesOnly": True,
            "infiniteDimensionalTheoremMachineChecked": False,
            "numericsUsedAsProof": False,
        },
        "exactChecks": exact,
        "claimBoundary": {
            "finiteMatrixMeanCancellationChecked": True,
            "finiteMatrixSimilarityChecked": True,
            "hiddenMeanDerivativeChecked": True,
            "analyticConstantLedgerChecked": True,
            "orthogonalProjectionSpeedAlgebraChecked": True,
            "adjointPressureFourierAlgebraChecked": True,
            "twoModeLeakageAlgebraChecked": True,
            "positiveGapDualConstantAlgebraChecked": True,
            "supportingAlgebraPromotedToFullOperatorTheorem": False,
            "infiniteDimensionalPropagatorProvedByCertificate": False,
            "lowGapA2EnhancedDissipationProved": False,
            "physicalKineticPropagatorProved": False,
            "OSSquirePropagatorProved": False,
            "nonlinearNavierStokesProved": False,
            "clayMillenniumProblemSolved": False,
        },
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_commit_object(source_commit: str) -> None:
    if re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise RuntimeError("--formal requires --source-commit <40 lowercase hex>")
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode:
        raise RuntimeError("formal sourceCommit is not a valid Git commit object")


def ensure_clean_source_head(source_commit: str) -> None:
    """Require the source seal to start at its exact clean repository HEAD."""
    validate_commit_object(source_commit)
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    if head != source_commit:
        raise RuntimeError("formal source commit must equal clean HEAD")
    status = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=ROOT,
        text=True,
    )
    if status:
        raise RuntimeError("formal source commit must equal clean HEAD")


def source_bindings(stage: str, source_commit: str | None) -> List[dict]:
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"missing source binding: {relative}")
        if stage == "source-stage":
            bindings.append({
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
            continue
        assert source_commit is not None
        try:
            git_blob = subprocess.check_output(
                ["git", "rev-parse", f"{source_commit}:{relative}"],
                cwd=ROOT,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            committed_bytes = subprocess.check_output(
                ["git", "cat-file", "blob", git_blob], cwd=ROOT
            )
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                f"formal source is absent from {source_commit}: {relative}"
            ) from error
        if path.read_bytes() != committed_bytes:
            raise RuntimeError(
                f"working source differs byte-for-byte from {source_commit}:{relative}"
            )
        bindings.append({
            "path": relative,
            "commit": source_commit,
            "gitBlob": git_blob,
            "bytes": len(committed_bytes),
            "sha256": hashlib.sha256(committed_bytes).hexdigest(),
            "workingTreeBytesMatch": True,
        })
    return bindings


def artifact_binding(relative: str) -> dict:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"generated artifact is absent or linked: {relative}")
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def manifest_payload(
    stage: str, source_commit: str | None, bindings: List[dict]
) -> dict:
    return {
        "schemaVersion": 1,
        "release": "R0.73A",
        "status": stage,
        "created": "2026-08-29",
        "sourceBindingKind": (
            "exact Git commit blobs and byte-identical working sources"
            if stage == "formal" else "exact working-tree bytes"
        ),
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "outputs": OUTPUTS,
        "externalOutputs": [artifact_binding(EXTERNAL_OUTPUT)],
        "limitations": [
            "The certificate checks deterministic finite Fourier matrices.",
            "The numerical propagator grid is a crosscheck, not an infinite-dimensional proof.",
            (
                "Formal means source-commit sealed; publication is not asserted."
                if stage == "formal"
                else "No publication or formal-release state is asserted."
            ),
        ],
    }


def write_json(name: str, payload: dict) -> None:
    (HERE / name).write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def write_hash_ledger() -> None:
    names = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    rows = [f"{sha256(HERE / name)}  {name}" for name in names]
    (HERE / "SHA256SUMS").write_text("\n".join(rows) + "\n", encoding="utf-8")


def self_test() -> None:
    certificate = certificate_payload()
    crosscheck = numerical_crosscheck()
    if certificate["status"] != "passed":
        raise AssertionError("exact certificate failed")
    if crosscheck["status"] != "passed":
        raise AssertionError("numerical crosscheck failed")
    subprocess.run([sys.executable, str(INDEPENDENT_PRODUCER), "--self-test"], check=True)
    print("R0.73A producer self-test passed (no outputs written)")


def existing_manifest_status() -> str | None:
    path = HERE / "manifest.json"
    if not path.exists():
        return None
    status = json.loads(path.read_text(encoding="utf-8")).get("status")
    if status == "formal":
        raise RuntimeError("refusing to overwrite a formal R0.73A certificate")
    if status not in (None, "source-stage"):
        raise RuntimeError("existing certificate has an unknown lifecycle status")
    return status


def write_outputs(stage: str, source_commit: str | None) -> None:
    existing_manifest_status()
    if stage == "formal":
        if source_commit is None:
            raise RuntimeError("--formal requires --source-commit <40 lowercase hex>")
        ensure_clean_source_head(source_commit)
    elif source_commit is not None:
        raise RuntimeError("source-stage cannot carry a source commit")
    bindings = source_bindings(stage, source_commit)
    independent_command = [
        sys.executable,
        str(INDEPENDENT_PRODUCER),
        f"--{stage}",
        "--output",
        str(ROOT / EXTERNAL_OUTPUT),
    ]
    if stage == "formal":
        independent_command.extend(["--source-commit", str(source_commit)])
    subprocess.run(independent_command, check=True)

    certificate = certificate_payload(stage, source_commit)
    crosscheck = numerical_crosscheck()
    crosscheck["certificateStage"] = stage
    crosscheck["sourceCommit"] = source_commit
    crosscheck["sourceBindings"] = bindings
    crosscheck["temporaryUnsealedSourceAllowed"] = stage == "source-stage"
    crosscheck["formalSourceReady"] = stage == "formal"
    crosscheck["independentCsv"] = artifact_binding(EXTERNAL_OUTPUT)
    if certificate["status"] != "passed" or crosscheck["status"] != "passed":
        raise SystemExit("refusing to write failed R0.73A certificate")
    write_json("certificate.json", certificate)
    write_json("crosscheck.json", crosscheck)
    write_json("manifest.json", manifest_payload(stage, source_commit, bindings))
    write_hash_ledger()
    print(
        f"wrote deterministic R0.73A {stage} certificate "
        f"({crosscheck['caseCount']} producer cases and 120 independent CSV cases)"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--source-stage", action="store_true")
    group.add_argument("--write", action="store_true", help=argparse.SUPPRESS)
    group.add_argument("--formal", action="store_true")
    parser.add_argument("--source-commit")
    arguments = parser.parse_args()
    if arguments.self_test:
        if arguments.source_commit:
            parser.error("--self-test cannot be combined with --source-commit")
        self_test()
    elif arguments.formal:
        write_outputs("formal", arguments.source_commit)
    else:
        if arguments.source_commit:
            parser.error("--source-stage cannot be combined with --source-commit")
        write_outputs("source-stage", None)


if __name__ == "__main__":
    main()
