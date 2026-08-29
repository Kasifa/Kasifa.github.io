#!/usr/bin/env python3
"""Generate the deterministic R0.73B algebra and finite-data certificate.

The exact part uses rational arithmetic.  The floating-point part only imports
already validated finite Fourier evidence; it is never promoted to an
infinite-dimensional Orr--Sommerfeld/Squire theorem.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SOURCE_FILES = [
    "research/r073b_problem_freeze.md",
    "research/r073b_kinetic_form_proof.md",
    "research/r073b_report-source.md",
    "research/r073b_literature_audit.md",
    "research/r073b_gap_matrix.md",
    "research/r073b_independent_analytic_audit.md",
    "experiments/r073b/weighted_kinetic_screen.py",
    "experiments/r073b/validate_weighted_kinetic_screen.py",
    "experiments/r073b/README.md",
    "experiments/r073b/contract.json",
    "experiments/r073b/requirements.txt",
    "experiments/r073b/command.txt",
    "experiments/r073b/weighted_propagator_rows.csv",
    "experiments/r073b/targeted_asymptotics.csv",
    "experiments/r073b/summary.json",
    "experiments/r073b/validation.json",
    "experiments/r073b/environment.json",
    "experiments/r073b/manifest.json",
    "experiments/r073b/progress.ndjson",
    "research/certificates/r073b/generate_certificate.py",
    "research/certificates/r073b/independent_recompute.py",
    "research/certificates/r073b/independent_recompute.json",
    "research/certificates/r073b/validate_certificate.py",
    "research/certificates/r073b/README.md",
    "research/certificates/r073b/command.txt",
    "research/certificates/r073b/environment.txt",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/README.md",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/caption.md",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/command.txt",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/config.json",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/contract.json",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/environment.txt",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/figure-contract.md",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/manifest-draft.json",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/plot.py",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/qa-protocol.md",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/requirements.txt",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/validate.py",
    "scripts/generate_r073b_release.py",
    "scripts/add-r073b-translations.mjs",
    "scripts/i18n-snapshots/r073b-missing.json",
    "tests/r073b-bloch-kinetic-gate.test.mjs",
    "tests/r073b-release.test.mjs",
    "tests/r073b-deterministic-certificate-source.test.mjs",
    "tests/r073b-bloch-kinetic-transient-figure-source.test.mjs",
]
OUTPUTS = ["certificate.json", "crosscheck.json", "manifest.json", "progress.ndjson"]

Entry = Dict[str, Fraction]
Matrix = List[List[Entry]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--source-stage", action="store_true")
    group.add_argument("--formal", action="store_true")
    parser.add_argument("--source-commit", default="")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def clean(entry: Entry) -> Entry:
    return {key: value for key, value in entry.items() if value}


def add(entry: Entry, basis: str, value: Fraction) -> None:
    entry[basis] = entry.get(basis, Fraction(0)) + value
    if entry[basis] == 0:
        del entry[basis]


def scale(entry: Entry, factor: Fraction) -> Entry:
    return clean({key: factor * value for key, value in entry.items()})


def w_symbol(mode: int) -> Tuple[str, Fraction] | None:
    """Return basis and a_k in W_k=i*a_k*basis."""
    return {
        -2: ("e4", Fraction(1, 8)),
        -1: ("e1", Fraction(-1, 4)),
        1: ("e1", Fraction(1, 4)),
        2: ("e4", Fraction(-1, 8)),
    }.get(mode)


def empty_matrix(size: int) -> Matrix:
    return [[{} for _ in range(size)] for _ in range(size)]


def modes_for(n_cut: int) -> List[int]:
    return list(range(-n_cut, n_cut + 1))


def raw_bloch_matrix(n_cut: int, beta: Fraction, mu: Fraction,
                     coupling: Fraction) -> Matrix:
    modes = modes_for(n_cut)
    matrix = empty_matrix(len(modes))
    for row, n_mode in enumerate(modes):
        lam_n = (Fraction(n_mode) + beta) ** 2 + mu
        add(matrix[row][row], "one", -lam_n)
        for column, m_mode in enumerate(modes):
            shift = n_mode - m_mode
            symbol = w_symbol(shift)
            if symbol is None:
                continue
            basis, amplitude = symbol
            lam_m = (Fraction(m_mode) + beta) ** 2 + mu
            add(matrix[row][column], basis, coupling * amplitude * (
                1 - Fraction(shift * shift) / lam_m
            ))
    return matrix


def conjugate_bloch(matrix: Matrix, n_cut: int, gap: Fraction) -> Matrix:
    modes = modes_for(n_cut)
    result = empty_matrix(len(modes))
    for row, n_mode in enumerate(modes):
        row_weight = gap if n_mode == 0 else Fraction(1)
        for column, m_mode in enumerate(modes):
            column_weight = gap if m_mode == 0 else Fraction(1)
            result[row][column] = scale(
                matrix[row][column], column_weight / row_weight
            )
    return result


def direct_bloch_hr_matrix(n_cut: int, beta: Fraction, mu: Fraction,
                           coupling: Fraction) -> Matrix:
    modes = modes_for(n_cut)
    zero = n_cut
    gap = beta * beta + mu
    result = empty_matrix(len(modes))
    for row, n_mode in enumerate(modes):
        lam_n = (Fraction(n_mode) + beta) ** 2 + mu
        if n_mode == 0:
            add(result[row][row], "one", -gap)
            for column, m_mode in enumerate(modes):
                if m_mode == 0:
                    continue
                symbol = w_symbol(-m_mode)
                if symbol is None:
                    continue
                basis, amplitude = symbol
                lam_m = (Fraction(m_mode) + beta) ** 2 + mu
                # -ic Pi(Ws)+(2c beta/g) Pi(W_x s).
                coefficient = (
                    coupling * amplitude / lam_m
                    + 2 * coupling * beta * m_mode * amplitude
                    / (gap * lam_m)
                )
                add(result[row][column], basis, coefficient)
            continue

        add(result[row][row], "one", -lam_n)
        symbol = w_symbol(n_mode)
        if symbol is not None:
            basis, amplitude = symbol
            add(result[row][zero], basis,
                coupling * amplitude * (gap - n_mode * n_mode))
        for column, m_mode in enumerate(modes):
            if m_mode == 0:
                continue
            shift = n_mode - m_mode
            symbol = w_symbol(shift)
            if symbol is None:
                continue
            basis, amplitude = symbol
            lam_m = (Fraction(m_mode) + beta) ** 2 + mu
            add(result[row][column], basis, coupling * amplitude * (
                1 - Fraction(shift * shift) / lam_m
            ))
    return result


def matrices_equal(left: Matrix, right: Matrix) -> bool:
    return all(
        clean(left[row][column]) == clean(right[row][column])
        for row in range(len(left))
        for column in range(len(left))
    )


def exact_bloch_records() -> dict:
    cases = (
        (3, Fraction(0), Fraction(1, 1000), Fraction(4)),
        (4, Fraction(1, 10), Fraction(1, 100), Fraction(-3)),
        (5, Fraction(-1, 4), Fraction(3, 16), Fraction(1)),
        (6, Fraction(49, 100), Fraction(1, 50), Fraction(4)),
    )
    similarities = []
    cancellations = []
    for n_cut, beta, mu, coupling in cases:
        gap = beta * beta + mu
        raw = raw_bloch_matrix(n_cut, beta, mu, coupling)
        transformed = conjugate_bloch(raw, n_cut, gap)
        direct = direct_bloch_hr_matrix(n_cut, beta, mu, coupling)
        similarities.append({
            "nCut": n_cut,
            "dimension": 2 * n_cut + 1,
            "beta": fraction_text(beta),
            "mu": fraction_text(mu),
            "g": fraction_text(gap),
            "c": fraction_text(coupling),
            "entrywiseExact": matrices_equal(transformed, direct),
        })
        mode_rows = []
        for mode in (-2, -1, 1, 2):
            lam = (Fraction(mode) + beta) ** 2 + mu
            lhs = lam - mode * mode
            rhs = gap + 2 * beta * mode
            mode_rows.append({
                "mode": mode,
                "lambdaMinusModeSquare": fraction_text(lhs),
                "gPlusTwoBetaMode": fraction_text(rhs),
                "exact": lhs == rhs,
            })
        cancellations.append({
            "beta": fraction_text(beta),
            "mu": fraction_text(mu),
            "identity": (
                "Pi0(Wr+Wxx L^-1r)=g Pi0(WL^-1r)"
                "+2i beta Pi0(W_xL^-1r)"
            ),
            "modes": mode_rows,
        })
    return {
        "nearCarrierCancellation": cancellations,
        "rawQToNearCarrierSimilarity": similarities,
    }


def exact_energy_records() -> dict:
    # The Young inequality is checked after clearing denominators:
    # (a^2+b^2)/2-ab=(a-b)^2/2.
    young_samples = []
    for a_value, b_value in (
        (Fraction(0), Fraction(1)),
        (Fraction(3, 5), Fraction(-7, 11)),
        (Fraction(-13, 9), Fraction(5, 4)),
        (Fraction(8), Fraction(8)),
    ):
        left = (a_value * a_value + b_value * b_value) / 2 - a_value * b_value
        right = (a_value - b_value) ** 2 / 2
        young_samples.append({
            "a": fraction_text(a_value),
            "b": fraction_text(b_value),
            "residual": fraction_text(left),
            "square": fraction_text(right),
            "exact": left == right and left >= 0,
        })

    primitive = {
        "WxInfinityExact": "(e^-d+e^-4d)/2",
        "equalityPoint": "x=pi",
        "K(s,d)": "(e^-s-e^-d)/2+(e^-4s-e^-4d)/8",
        "normExponentHalfK": (
            "(e^-s-e^-d)/4+(e^-4s-e^-4d)/16"
        ),
        "uniformNormExponent": "5*|Lambda|*e^-s/16",
        "coefficients": {
            "KFirstHarmonic": "1/2",
            "KSecondHarmonic": "1/8",
            "halfKFirstHarmonic": "1/4",
            "halfKSecondHarmonic": "1/16",
            "uniformSum": "5/16",
        },
        "coefficientLedgerExact": (
            Fraction(1, 2) / 1 == Fraction(1, 2)
            and Fraction(1, 2) / 4 == Fraction(1, 8)
            and Fraction(1, 4) + Fraction(1, 16) == Fraction(5, 16)
        ),
    }
    return {
        "youngProductBound": {
            "identity": "(a^2+b^2)/2-ab=(a-b)^2/2",
            "samples": young_samples,
            "exact": all(row["exact"] for row in young_samples),
        },
        "heatShearPrimitive": primitive,
        "physicalVelocityNormBound": (
            "||U_j(d,s)|| <= exp[-g_j(d-s)+|Lambda|K(s,d)/2]"
        ),
        "osKineticMetric": (
            "E_mu=mu^-1< L_mu v,v>="
            "mu^-1||L_mu^-1/2 q||^2"
        ),
    }


def exact_scaling_records() -> dict:
    exponents = []
    for p_value in (Fraction(0), Fraction(1, 4), Fraction(1, 2),
                    Fraction(3, 4), Fraction(1)):
        for a_value in (Fraction(0), Fraction(1, 2), Fraction(1),
                        Fraction(3, 2)):
            exponent = max(a_value / 2 - p_value, Fraction(0))
            exponents.append({
                "p": fraction_text(p_value),
                "a": fraction_text(a_value),
                "weightedBlockPower": fraction_text(p_value - a_value / 2),
                "predictedDivergenceExponent": fraction_text(exponent),
            })
    raw = []
    for p_value in (Fraction(0), Fraction(1, 4), Fraction(1, 2),
                    Fraction(3, 4), Fraction(1)):
        raw.append({
            "p": fraction_text(p_value),
            "rawBlockPower": fraction_text(p_value - 1),
            "predictedDivergenceExponent": fraction_text(
                max(1 - p_value, Fraction(0))
            ),
        })

    # In the fixed-Lambda kinetic triangular limit, the h-column has squared
    # off-diagonal norm Lambda^2*tau^2*(e^-2d+e^-8d)/8.
    first_pair = 2 * Fraction(1, 4) ** 2
    second_pair = 2 * 2**2 * Fraction(1, 8) ** 2
    # The extra |k| in the kinetic variable makes both coefficients 1/8.
    star_norm_squared = (
        2 * Fraction(1, 8) ** 2,
        2 * Fraction(1, 8) ** 2,
    )
    return {
        "diagonalWeightFamily": {
            "norm": "|h|^2+mu^-a||L_mu^-b/2 r||^2",
            "generatorBlockPower": "mu^(p-a/2)",
            "records": exponents,
            "kineticThreshold": {
                "a": "1/1",
                "fixedLambdaP": "1/2",
                "blockPower": "0/1",
                "everyAAboveOneDivergesOnFixedLambdaPath": True,
            },
        },
        "rawQFamily": {
            "generatorBlockPower": "mu^(p-1)",
            "records": raw,
        },
        "fixedLambdaTriangularColumn": {
            "formula": (
                "||z||^2=Lambda^2*tau^2*(e^-2d+e^-8d)/8"
            ),
            "firstHarmonicCoefficient": fraction_text(first_pair),
            "secondHarmonicCoefficient": fraction_text(second_pair),
            "coefficientsExact": (
                first_pair == Fraction(1, 8)
                and second_pair == Fraction(1, 8)
            ),
            "meanInputLowerBound": "sqrt(1+||z||^2)>1 when Lambda*tau!=0",
        },
        "fixedCFormalColumnScale": {
            "substitution": "Lambda=c/sqrt(mu)",
            "columnNormScale": "|c|*mu^-1/2",
            "finiteMatrixNumericalSupportOnly": True,
        },
        "sharpShearCoefficientLimit": {
            "formula": (
                "rho_mu -> sqrt(e^-2d+e^-8d)/(4*sqrt(2))"
            ),
            "squaredFirstHarmonicCoefficient": fraction_text(
                star_norm_squared[0]
            ),
            "squaredSecondHarmonicCoefficient": fraction_text(
                star_norm_squared[1]
            ),
            "totalSquared": "(e^-2d+e^-8d)/32",
            "equalsHalfWxL2": True,
        },
    }


def exact_checks() -> dict:
    return {
        "bloch": exact_bloch_records(),
        "energy": exact_energy_records(),
        "scaling": exact_scaling_records(),
    }


def experiment_crosscheck() -> dict:
    directory = ROOT / "experiments/r073b"
    summary = json.loads((directory / "summary.json").read_text())
    validation = json.loads((directory / "validation.json").read_text())
    manifest = json.loads((directory / "manifest.json").read_text())
    independent = json.loads(
        (HERE / "independent_recompute.json").read_text()
    )
    files = {
        name: {"bytes": (directory / name).stat().st_size,
               "sha256": sha256(directory / name)}
        for name in (
            "weighted_propagator_rows.csv", "targeted_asymptotics.csv",
            "summary.json", "validation.json", "manifest.json", "contract.json",
        )
    }
    fits = validation["asymptoticFits"]
    by_key = {(row["norm"], row["p"]): row for row in fits}
    return {
        "status": "passed" if (
            validation["status"] == "passed"
            and all(validation["checks"].values())
            and summary["kineticFiniteBoundViolations"] == 0
            and independent["status"] == "passed"
        ) else "failed",
        "finiteDimensionalOnly": True,
        "producerManifestStatus": manifest["status"],
        "caseCount": summary["caseCount"],
        "rowCount": summary["rowCount"],
        "maximumSimilarityError": validation["maximumSimilarityError"],
        "maximumStepRelativeDifference": validation[
            "maximumStepRelativeDifference"
        ],
        "maximumModeRelativeDifference": validation[
            "maximumModeRelativeDifference"
        ],
        "maximumExponentDifference": validation["maximumExponentDifference"],
        "maximumTriangularLimitRelativeDifference": validation[
            "maximumTriangularLimitRelativeDifference"
        ],
        "minimumGeneratorBoundMargin": validation[
            "minimumGeneratorBoundMargin"
        ],
        "kineticFiniteBoundViolations": summary[
            "kineticFiniteBoundViolations"
        ],
        "selectedExponents": {
            "rawQFixedC": by_key[("raw_q", 0.0)][
                "observedDivergenceExponent"
            ],
            "rawQFixedLambda": by_key[("raw_q", 0.5)][
                "observedDivergenceExponent"
            ],
            "kineticFixedC": by_key[("kinetic", 0.0)][
                "observedDivergenceExponent"
            ],
            "kineticFixedLambda": by_key[("kinetic", 0.5)][
                "observedDivergenceExponent"
            ],
            "overweightFixedLambda": by_key[("kinetic_over", 0.5)][
                "observedDivergenceExponent"
            ],
        },
        "fixedLambdaKineticLimits": validation[
            "fixedLambdaKineticLimits"
        ],
        "independentRecompute": independent,
        "files": files,
        "limitations": validation["limitations"],
    }


def git_output(*arguments: str) -> bytes:
    return subprocess.check_output(
        ["git", *arguments], cwd=ROOT, stderr=subprocess.STDOUT
    )


def source_bindings(stage: str, source_commit: str) -> list[dict]:
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"missing bound source: {relative}")
        record = {
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        if stage == "formal":
            blob = git_output("show", f"{source_commit}:{relative}")
            if blob != path.read_bytes():
                raise RuntimeError(
                    f"working source differs from {source_commit}: {relative}"
                )
            record.update({
                "commit": source_commit,
                "gitBlob": git_output(
                    "rev-parse", f"{source_commit}:{relative}"
                ).decode().strip(),
                "workingTreeBytesMatch": True,
            })
        else:
            record.update({"commit": "pending", "workingTreeBytesMatch": True})
        bindings.append(record)
    return bindings


def validate_commit(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("--source-commit must be a lowercase 40-hex commit")
    resolved = git_output("rev-parse", f"{value}^{{commit}}").decode().strip()
    if resolved != value:
        raise ValueError("source commit did not resolve exactly")
    return value


def all_exact_pass(records: dict) -> bool:
    return (
        all(
            row["entrywiseExact"]
            for row in records["bloch"]["rawQToNearCarrierSimilarity"]
        )
        and all(
            mode["exact"]
            for case in records["bloch"]["nearCarrierCancellation"]
            for mode in case["modes"]
        )
        and records["energy"]["youngProductBound"]["exact"]
        and records["energy"]["heatShearPrimitive"][
            "coefficientLedgerExact"
        ]
        and records["scaling"]["fixedLambdaTriangularColumn"][
            "coefficientsExact"
        ]
        and records["scaling"]["sharpShearCoefficientLimit"][
            "equalsHalfWxL2"
        ]
    )


def write_sums() -> None:
    lines = [f"{sha256(HERE / name)}  {name}" for name in OUTPUTS]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    records = exact_checks()
    if not all_exact_pass(records):
        raise AssertionError("internal exact algebra check failed")
    crosscheck = experiment_crosscheck()
    if crosscheck["status"] != "passed":
        raise AssertionError("finite experiment crosscheck failed")
    if args.self_test:
        print(canonical({
            "status": "passed",
            "exactChecks": True,
            "finiteCrosscheck": True,
        }), end="")
        return 0
    if not args.source_stage and not args.formal:
        raise ValueError("choose --source-stage, --formal, or --self-test")
    if args.formal:
        commit = validate_commit(args.source_commit)
        stage = "formal"
    else:
        if args.source_commit:
            raise ValueError("--source-commit is only valid with --formal")
        commit = "pending"
        stage = "source-stage"

    # Resolve and verify every binding before rewriting any certificate output.
    # In particular, a stale or incomplete formal source commit fails closed
    # while leaving the previous source-stage package byte-for-byte intact.
    bindings = source_bindings(stage, commit)

    certificate = {
        "schemaVersion": 1,
        "release": "R0.73B",
        "certificateStage": stage,
        "sourceCommit": commit,
        "exactChecks": records,
        "finiteCrosscheck": crosscheck,
        "claimBoundary": {
            "generalBlochCancellationAlgebraChecked": True,
            "generalBlochFiniteMatrixSimilarityChecked": True,
            "heatShearPrimitiveCoefficientLedgerChecked": True,
            "physicalEnergyYoungInequalityChecked": True,
            "weightScalingPowerLedgerChecked": True,
            "fixedLambdaTriangularColumnCoefficientChecked": True,
            "sharpShearLowGapStarCoefficientChecked": True,
            "finitePropagatorGridChecked": True,
            "analyticInfiniteDimensionalEnergyProofReplacedByCertificate": False,
            "GalerkinTailBoundProved": False,
            "completeOSSquireA2DirectSumProved": False,
            "nonlinearNavierStokesProved": False,
            "clayMillenniumProblemSolved": False,
        },
    }
    (HERE / "certificate.json").write_text(
        canonical(certificate), encoding="utf-8"
    )
    (HERE / "crosscheck.json").write_text(
        canonical(crosscheck), encoding="utf-8"
    )
    manifest = {
        "schemaVersion": 1,
        "release": "R0.73B",
        "created": "2026-08-29",
        "status": stage,
        "sourceBindingKind": (
            "working-tree SHA-256 snapshot" if stage == "source-stage"
            else "exact Git commit blobs and byte-identical working sources"
        ),
        "sourceBindings": bindings,
        "outputs": OUTPUTS,
        "limitations": [
            "exact rational checks certify only the displayed algebraic ledgers",
            "floating-point evidence is finite-dimensional and has no tail enclosure",
            "formal means source-commit sealed; website publication is not asserted",
        ],
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    progress = [
        {"sequence": 0, "event": "start", "release": "R0.73B", "stage": stage},
        {"sequence": 1, "event": "exact-checks-passed"},
        {"sequence": 2, "event": "finite-crosscheck-passed"},
        {"sequence": 3, "event": "source-bindings-verified", "count": len(bindings)},
        {"sequence": 4, "event": "complete", "sourceCommit": commit},
    ]
    (HERE / "progress.ndjson").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in progress),
        encoding="utf-8",
    )
    write_sums()
    print(canonical({
        "status": stage,
        "sourceCommit": commit,
        "sourceBindingCount": len(bindings),
        "exactChecksPassed": True,
        "finiteCrosscheckPassed": True,
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
