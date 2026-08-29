#!/usr/bin/env python3
"""Independent fail-closed validator for the R0.73B certificate package.

The validator never imports the producer.  It redoes the rational identities,
re-fits selected CSV exponents with a scalar least-squares formula, and
recomputes the fixed-Lambda triangular singular value by power iteration.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EXPECTED_SOURCE_FILES = [
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
EXPECTED_OUTPUTS = ["certificate.json", "crosscheck.json", "manifest.json", "progress.ndjson"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--require-source-stage", action="store_true")
    group.add_argument("--require-formal", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def git_output(*arguments: str) -> bytes:
    return subprocess.check_output(
        ["git", *arguments], cwd=ROOT, stderr=subprocess.STDOUT
    )


def redo_rational_algebra() -> dict[str, bool]:
    cancellation = []
    similarity = []
    for beta, mu in (
        (Fraction(0), Fraction(1, 1000)),
        (Fraction(1, 10), Fraction(1, 100)),
        (Fraction(-1, 4), Fraction(3, 16)),
        (Fraction(49, 100), Fraction(1, 50)),
    ):
        gap = beta * beta + mu
        for mode in (-2, -1, 1, 2):
            lam = (mode + beta) ** 2 + mu
            cancellation.append(
                lam - mode * mode == gap + 2 * beta * mode
            )
            # The amplitude of W_{-mode} cancels from the zero-row check.
            conjugated_zero_row = (1 - Fraction(mode * mode) / lam) / gap
            direct_zero_row = (
                Fraction(1, 1) / lam
                + 2 * beta * mode / (gap * lam)
            )
            # The amplitude of W_mode likewise cancels from the h-column.
            conjugated_h_column = gap * (
                1 - Fraction(mode * mode) / gap
            )
            direct_h_column = gap - mode * mode
            similarity.append(
                conjugated_zero_row == direct_zero_row
                and conjugated_h_column == direct_h_column
            )

    young = []
    for a_value, b_value in (
        (Fraction(0), Fraction(1)),
        (Fraction(3, 5), Fraction(-7, 11)),
        (Fraction(-13, 9), Fraction(5, 4)),
        (Fraction(8), Fraction(8)),
    ):
        young.append(
            (a_value * a_value + b_value * b_value) / 2
            - a_value * b_value == (a_value - b_value) ** 2 / 2
        )

    primitive = (
        Fraction(1, 2) / 1 == Fraction(1, 2)
        and Fraction(1, 2) / 4 == Fraction(1, 8)
        and Fraction(1, 4) + Fraction(1, 16) == Fraction(5, 16)
    )
    triangular = (
        2 * Fraction(1, 4) ** 2 == Fraction(1, 8)
        and 2 * 4 * Fraction(1, 8) ** 2 == Fraction(1, 8)
    )
    star = (
        2 * Fraction(1, 8) ** 2 == Fraction(1, 32)
        and 2 * Fraction(1, 8) ** 2 == Fraction(1, 32)
    )
    threshold = all(
        max(a_value / 2 - p_value, Fraction(0))
        == Fraction(record)
        for a_value, p_value, record in (
            (Fraction(1), Fraction(1, 2), 0),
            (Fraction(3, 2), Fraction(1, 2), Fraction(1, 4)),
            (Fraction(1), Fraction(0), Fraction(1, 2)),
            (Fraction(1, 2), Fraction(0), Fraction(1, 4)),
        )
    )
    return {
        "generalBlochCancellation": all(cancellation),
        "generalBlochMatrixSimilarity": all(similarity),
        "youngIdentity": all(young),
        "heatShearPrimitive": primitive,
        "triangularColumnCoefficients": triangular,
        "sharpShearStarCoefficients": star,
        "weightThresholdPowers": threshold,
    }


def slope(rows: list[dict[str, str]]) -> float:
    x_values = [math.log(float(row["mu"])) for row in rows]
    y_values = [math.log(float(row["gain"])) for row in rows]
    x_mean = sum(x_values) / len(x_values)
    y_mean = sum(y_values) / len(y_values)
    numerator = sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x_values, y_values)
    )
    denominator = sum((x_value - x_mean) ** 2 for x_value in x_values)
    return numerator / denominator


def targeted_exponent(rows: list[dict[str, str]], norm: str,
                      p_value: float) -> float:
    subset = sorted((
        row for row in rows
        if row["norm"] == norm and float(row["p"]) == p_value
    ), key=lambda row: float(row["mu"]))[:4]
    require(len(subset) == 4, f"missing targeted rows: {norm}, {p_value}")
    return max(0.0, -slope(subset))


def triangular_gain(lam: float, start: float, end: float) -> float:
    tau = end - start
    d1 = math.exp(-tau)
    d2 = math.exp(-4.0 * tau)
    # Coordinates: h, -2, -1, +1, +2.  Only signs differ in z, and signs
    # are immaterial to the singular value; retain a symmetric real choice.
    z2 = lam * 2.0 / 8.0 * tau * math.exp(-4.0 * end)
    z1 = lam / 4.0 * tau * math.exp(-end)
    matrix = [
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [z2, d2, 0.0, 0.0, 0.0],
        [z1, 0.0, d1, 0.0, 0.0],
        [-z1, 0.0, 0.0, d1, 0.0],
        [-z2, 0.0, 0.0, 0.0, d2],
    ]
    gram = [[sum(matrix[k][i] * matrix[k][j] for k in range(5))
             for j in range(5)] for i in range(5)]
    vector = [1.0, 0.1, -0.2, 0.3, -0.4]
    for _ in range(200):
        result = [sum(gram[i][j] * vector[j] for j in range(5))
                  for i in range(5)]
        length = math.sqrt(sum(value * value for value in result))
        vector = [value / length for value in result]
    eigenvalue = sum(
        vector[i] * gram[i][j] * vector[j]
        for i in range(5) for j in range(5)
    )
    return math.sqrt(eigenvalue)


def validate_source_bindings(manifest: dict, stage: str) -> bool:
    if [row["path"] for row in manifest["sourceBindings"]] != EXPECTED_SOURCE_FILES:
        return False
    for record in manifest["sourceBindings"]:
        path = ROOT / record["path"]
        if not path.is_file():
            return False
        if path.stat().st_size != record["bytes"] or sha256(path) != record["sha256"]:
            return False
        if stage == "formal":
            commit = manifest["sourceBindings"][0]["commit"]
            if record["commit"] != commit or record["workingTreeBytesMatch"] is not True:
                return False
            try:
                if git_output("show", f"{commit}:{record['path']}") != path.read_bytes():
                    return False
                blob = git_output("rev-parse", f"{commit}:{record['path']}").decode().strip()
            except subprocess.CalledProcessError:
                return False
            if record["gitBlob"] != blob:
                return False
        elif record["commit"] != "pending":
            return False
    return True


def main() -> int:
    args = parse_args()
    algebra = redo_rational_algebra()
    require(all(algebra.values()), "independent rational algebra failed")
    if args.self_test:
        print(canonical({"status": "passed", "checks": algebra}), end="")
        return 0
    if not args.require_source_stage and not args.require_formal:
        raise ValueError("choose --require-source-stage, --require-formal, or --self-test")

    certificate = json.loads((HERE / "certificate.json").read_text())
    crosscheck = json.loads((HERE / "crosscheck.json").read_text())
    manifest = json.loads((HERE / "manifest.json").read_text())
    stage = "formal" if args.require_formal else "source-stage"
    require(certificate["certificateStage"] == stage,
            "certificate stage mismatch")
    require(manifest["status"] == stage, "manifest stage mismatch")
    require(manifest["outputs"] == EXPECTED_OUTPUTS, "output list mismatch")
    require(validate_source_bindings(manifest, stage),
            "source binding validation failed")
    require(certificate["finiteCrosscheck"] == crosscheck,
            "crosscheck file differs from embedded certificate")

    sums = {}
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        sums[name] = digest
    require(set(sums) == set(EXPECTED_OUTPUTS), "SHA256SUMS scope mismatch")
    require(all(sha256(HERE / name) == sums[name] for name in EXPECTED_OUTPUTS),
            "certificate output hash mismatch")

    experiment = ROOT / "experiments/r073b"
    validation = json.loads((experiment / "validation.json").read_text())
    summary = json.loads((experiment / "summary.json").read_text())
    require(validation["status"] == "passed" and all(validation["checks"].values()),
            "experiment validation is not passed")
    require(summary["caseCount"] == 280 and summary["rowCount"] == 1960,
            "experiment coverage mismatch")
    require(summary["kineticFiniteBoundViolations"] == 0,
            "finite kinetic bound violation")
    with (experiment / "targeted_asymptotics.csv").open(encoding="utf-8") as handle:
        targeted = list(csv.DictReader(handle))
    require(len(targeted) == 245, "targeted CSV row count mismatch")

    observed = {
        "rawQFixedC": targeted_exponent(targeted, "raw_q", 0.0),
        "rawQFixedLambda": targeted_exponent(targeted, "raw_q", 0.5),
        "kineticFixedC": targeted_exponent(targeted, "kinetic", 0.0),
        "kineticFixedLambda": targeted_exponent(targeted, "kinetic", 0.5),
        "overweightFixedLambda": targeted_exponent(
            targeted, "kinetic_over", 0.5
        ),
    }
    expected = {
        "rawQFixedC": 1.0,
        "rawQFixedLambda": 0.5,
        "kineticFixedC": 0.5,
        "kineticFixedLambda": 0.0,
        "overweightFixedLambda": 0.25,
    }
    exponent_errors = {
        key: abs(observed[key] - expected[key]) for key in observed
    }
    require(max(exponent_errors.values()) <= 5e-3,
            "selected exponent recomputation failed")
    require(all(
        abs(observed[key] - crosscheck["selectedExponents"][key]) <= 1e-12
        for key in observed
    ), "embedded selected exponents differ")
    independent = crosscheck["independentRecompute"]
    require(independent["status"] == "passed"
            and independent["producerImported"] is False,
            "independent scalar recomputation is not passed")
    require(all(
        abs(observed[key] - independent["selectedObservedExponents"][key])
        <= 1e-12 for key in observed
    ), "independent scalar exponents differ")

    triangular_errors = []
    for record in crosscheck["fixedLambdaKineticLimits"]:
        recomputed = triangular_gain(float(record["Lambda"]), 0.0, 0.75)
        triangular_errors.append(
            abs(recomputed - float(record["triangularLimitGain"]))
            / float(record["triangularLimitGain"])
        )
    require(max(triangular_errors) <= 2e-13,
            "triangular singular-value recomputation failed")
    require(all(
        abs(
            triangular_gain(float(key), 0.0, 0.75) - float(value)
        ) / float(value) <= 2e-13
        for key, value in independent["fixedLambdaTriangularGains"].items()
    ), "independent triangular gains differ")

    progress = [json.loads(line) for line in
                (HERE / "progress.ndjson").read_text().splitlines()]
    require([row["sequence"] for row in progress] == [0, 1, 2, 3, 4]
            and progress[-1]["event"] == "complete",
            "certificate progress contract failed")

    boundary = certificate["claimBoundary"]
    require(boundary["finitePropagatorGridChecked"] is True,
            "finite evidence boundary missing")
    require(all(boundary[key] is False for key in (
        "analyticInfiniteDimensionalEnergyProofReplacedByCertificate",
        "GalerkinTailBoundProved", "completeOSSquireA2DirectSumProved",
        "nonlinearNavierStokesProved", "clayMillenniumProblemSolved",
    )), "claim boundary overstates result")
    if stage == "formal":
        commit = certificate["sourceCommit"]
        require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
                "formal source commit malformed")
        require(git_output("rev-parse", f"{commit}^{{commit}}").decode().strip() == commit,
                "formal source commit does not resolve")
    else:
        require(certificate["sourceCommit"] == "pending",
                "source-stage commit must be pending")

    result = {
        "schemaVersion": 1,
        "status": "passed",
        "stage": stage,
        "checks": {
            **algebra,
            "sourceBindings": True,
            "certificateHashes": True,
            "finiteExperimentValidation": True,
            "selectedExponentRecompute": True,
            "independentScalarRecompute": True,
            "triangularGainRecompute": True,
            "progressContract": True,
            "claimBoundary": True,
        },
        "selectedObservedExponents": observed,
        "maximumSelectedExponentError": max(exponent_errors.values()),
        "maximumTriangularGainRelativeError": max(triangular_errors),
        "claimBoundary": {
            "finiteAlgebraAndMatricesValidated": True,
            "infiniteDimensionalTheoremProvedByThisValidator": False,
            "nonlinearNavierStokesProved": False,
        },
    }
    (HERE / "validation.json").write_text(canonical(result), encoding="utf-8")
    print(canonical(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
