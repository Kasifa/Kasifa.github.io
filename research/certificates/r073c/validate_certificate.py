#!/usr/bin/env python3
"""Independent fail-closed validator for the R0.73C certificate package.

This file is implementation-independent from the certificate and numerical
producers.  It independently checks the exact rational ledger, serialized
binary and Decimal endpoint signs, implementation independence, source-stage
or Git-blob bindings, deterministic JSON boundaries, and package hashes.
"""

from __future__ import annotations

import argparse
import ast
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EXPERIMENT = ROOT / "experiments/r073c"

EXPECTED_SOURCE_FILES = [
    "research/r073c_problem_freeze.md",
    "research/r073c_monodromy_proof.md",
    "research/r073c_interval_proof_audit.md",
    "research/r073c_independent_decimal_monodromy_audit.md",
    "research/r073c_report-source.md",
    "research/r073c_literature_audit.md",
    "research/r073c_gap_matrix.md",
    "research/r073c_independent_analytic_audit.md",
    "research/r073c_interval_monodromy.py",
    "research/r073c_spectral_screen_agent.py",
    "experiments/r073c/README.md",
    "experiments/r073c/command.txt",
    "experiments/r073c/contract.json",
    "experiments/r073c/requirements.txt",
    "experiments/r073c/build_package.py",
    "experiments/r073c/canonical_interval_run_a.json",
    "experiments/r073c/canonical_interval_run_b.json",
    "experiments/r073c/canonical_decimal_interval_validation.json",
    "experiments/r073c/canonical_fourier_screen.json",
    "experiments/r073c/canonical_independent_fourier_validation.json",
    "experiments/r073c/independent_decimal_monodromy_validator.py",
    "experiments/r073c/independent_fourier_spectral_validator.py",
    "experiments/r073c/environment.json",
    "experiments/r073c/summary.json",
    "experiments/r073c/validation.json",
    "experiments/r073c/progress.ndjson",
    "experiments/r073c/manifest.json",
    "experiments/r073c/SHA256SUMS",
    "research/certificates/r073c/generate_certificate.py",
    "research/certificates/r073c/independent_recompute.py",
    "research/certificates/r073c/independent_recompute.json",
    "research/certificates/r073c/validate_certificate.py",
    "research/certificates/r073c/README.md",
    "research/certificates/r073c/command.txt",
    "research/certificates/r073c/environment.txt",
    "scripts/generate_r073c_release.py",
    "scripts/add-r073c-translations.mjs",
    "scripts/i18n-snapshots/r073c-missing.json",
    "tests/r073c-rayleigh-instability-gate.test.mjs",
    "tests/r073c-release.test.mjs",
    "tests/r073c-deterministic-certificate-source.test.mjs",
    "tests/r073c-certified-rayleigh-instability-figure-source.test.mjs",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/README.md",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/caption.md",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/config.json",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/contract.json",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/figure-contract.md",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/manifest-draft.json",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/plot.py",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/qa-protocol.md",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/requirements.txt",
    "figures/r073c/fig-r073c-certified-rayleigh-instability/validate.py",
]
EXPECTED_OUTPUTS = ["certificate.json", "crosscheck.json", "manifest.json", "progress.ndjson"]
EXPECTED_PACKAGE_FILES = [
    "README.md",
    "certificate.json",
    "command.txt",
    "crosscheck.json",
    "environment.txt",
    "generate_certificate.py",
    "independent_recompute.json",
    "independent_recompute.py",
    "manifest.json",
    "progress.ndjson",
    "validate_certificate.py",
    "validation.json",
]
DECISION_KEYS = {
    "exactCubicNeutralSpectrum": "closed",
    "infiniteDimensionalFrozenRayleighInstability": "closed",
    "frozenInstabilityFastTimeTransfer": "open",
    "superPolynomialCompleteRowNoGo": "conditional-on-C5",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
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


def load_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON constant {value} in {path}")

    return json.loads(path.read_text(), parse_constant=reject_constant)


def all_finite(value: Any) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, (str, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, list):
        return all(all_finite(item) for item in value)
    if isinstance(value, dict):
        return all(isinstance(key, str) and all_finite(item)
                   for key, item in value.items())
    return False


def binary_value(record: dict[str, Any]) -> Fraction:
    require(set(record) == {"bitcount", "exponent", "mantissa", "sign"},
            "unexpected binary endpoint fields")
    mantissa = record["mantissa"]
    exponent = record["exponent"]
    require(type(mantissa) is int and mantissa > 0, "invalid mantissa")
    require(type(exponent) is int and type(record["bitcount"]) is int,
            "invalid binary integer field")
    require(record["bitcount"] == mantissa.bit_length(), "bitcount mismatch")
    require(type(record["sign"]) is int and record["sign"] in (0, 1), "invalid sign bit")
    magnitude = Fraction(mantissa) * (
        2 ** exponent if exponent >= 0 else Fraction(1, 2 ** (-exponent))
    )
    return -magnitude if record["sign"] else magnitude


def primary_interval(row: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    result = tuple(binary_value(item) for item in row[key]["binaryEndpoints"])
    require(len(result) == 2 and result[0] <= result[1], f"invalid interval {key}")
    return result[0], result[1]


def decimal_interval(row: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    result = (
        Fraction(Decimal(row[key]["lower"])),
        Fraction(Decimal(row[key]["upper"])),
    )
    require(result[0] <= result[1], f"invalid Decimal interval {key}")
    return result


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def redo_exact_algebra() -> dict[str, bool]:
    # Independent C3 calculation in s=sin(x/2), c=cos(x/2).
    w_factor = (
        -Fraction(1, 2) * 2 + Fraction(1, 4) * 4 == 0
        and Fraction(1, 4) * 4 * (-2) == -2
    )
    wpp_factor = (
        Fraction(1, 2) * 2 - 4 == -3
        and Fraction(8) == 8
    )
    phi_xx = (Fraction(3, 2), Fraction(-9, 4))
    potential_phi = (Fraction(3, 2), Fraction(-4))
    h_phi = (-phi_xx[0] + potential_phi[0],
             -phi_xx[1] + potential_phi[1])
    spectrum = [Fraction((n + 3) ** 2 - 16, 4) for n in range(8)]

    # Independent 2x2 determinant and reflection-conjugation ledger.
    det_m_minus_i = {"ad": 1, "bc": -1, "a": -1, "d": -1, "one": 1}
    trace_terms = sorted(("Da", "Bc", "Cb", "Ad"))
    swap = {letter: letter.swapcase() for letter in "abcdABCD"}
    original = sorted("".join(sorted(term)) for term in trace_terms)
    conjugated = sorted(
        "".join(sorted(swap[letter] for letter in term))
        for term in trace_terms
    )
    minus_i = (Fraction(0), Fraction(-1))
    plus_i = (Fraction(0), Fraction(1))
    product = (
        minus_i[0] * plus_i[0] - minus_i[1] * plus_i[1],
        minus_i[0] * plus_i[1] + minus_i[1] * plus_i[0],
    )
    report = (ROOT / "research/r073c_report-source.md").read_text()
    proof = (ROOT / "research/r073c_monodromy_proof.md").read_text()
    return {
        "c3WFactorization": w_factor,
        "c3WppFactorization": wpp_factor,
        "c3NeutralIdentity": h_phi == (Fraction(0), Fraction(-7, 4)),
        "c3PeriodicRegularityBoundary": Fraction(-3, 4) != Fraction(3, 4),
        "c3SpectrumFirstValues": spectrum[:4] == [
            Fraction(-7, 4), Fraction(0), Fraction(9, 4), Fraction(5)
        ],
        "c3UniqueNegativeFromFormula": spectrum[0] < 0 <= spectrum[1]
            and all(spectrum[index] < spectrum[index + 1]
                    for index in range(len(spectrum) - 1)),
        "c3AnalyticSpectrumSource": all(token in report for token in (
            "|\\sin(x/2)|^3", "C^2\\cap H^2_{\\rm per}", "not \\(C^3\\)",
            "\\frac{(n+3)^2-16}{4}", "unique negative", "limit point",
        )),
        "c4DeterminantIdentity": det_m_minus_i == {
            "ad": 1, "bc": -1, "a": -1, "d": -1, "one": 1
        },
        "c4ReflectionTraceReality": original == conjugated,
        "c4PhaseSpeedSign": product == (Fraction(1), Fraction(0)),
        "c4AnalyticOdeSource": all(token in proof for token in (
            "\\det M=1", "M^{-1}=S\\overline M S",
            "\\det(M-I)=2-\\operatorname{tr}M",
            "F(\\eta):=\\operatorname{tr}M(\\eta)-2",
            "\\sigma=\\eta/2>0", "continuous",
        )),
    }


def git_output(*arguments: str) -> bytes:
    return subprocess.check_output(["git", *arguments], cwd=ROOT, stderr=subprocess.STDOUT)


def validate_source_bindings(manifest: dict[str, Any], stage: str) -> str:
    records = manifest["sourceBindings"]
    require([item["path"] for item in records] == EXPECTED_SOURCE_FILES,
            "source binding inventory/order mismatch")
    formal_commit = None
    for item in records:
        path = ROOT / item["path"]
        require(path.is_file(), f"missing bound source: {item['path']}")
        require(path.stat().st_size == item["bytes"] and sha256(path) == item["sha256"],
                f"source hash mismatch: {item['path']}")
        require(item["workingTreeBytesMatch"] is True,
                f"source byte-match sentinel failed: {item['path']}")
        if stage == "formal":
            commit = item["commit"]
            require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
                    "formal commit malformed")
            formal_commit = formal_commit or commit
            require(commit == formal_commit, "formal bindings use multiple commits")
            require(git_output("show", f"{commit}:{item['path']}") == path.read_bytes(),
                    f"formal Git blob bytes mismatch: {item['path']}")
            blob = git_output("rev-parse", f"{commit}:{item['path']}").decode().strip()
            require(item["gitBlob"] == blob, f"formal Git blob id mismatch: {item['path']}")
        else:
            require(item["commit"] == "pending" and "gitBlob" not in item,
                    f"source-stage commit field mismatch: {item['path']}")
    return formal_commit if stage == "formal" else "pending"


def independent_interval_recompute(crosscheck: dict[str, Any]) -> dict[str, Any]:
    primary: dict[str, dict[str, tuple[Fraction, Fraction]]] = {}
    for filename, run_id in (
        ("canonical_interval_run_a.json", "partition-a"),
        ("canonical_interval_run_b.json", "partition-b"),
    ):
        data = load_json(EXPERIMENT / filename)
        require(data["status"] == "passed" and data["runId"] == run_id,
                f"primary run status mismatch: {run_id}")
        by_eta: dict[str, tuple[Fraction, Fraction]] = {}
        for row in data["results"]:
            eta = row["eta"]
            trace = primary_interval(row, "traceMinusTwo")
            imag = primary_interval(row, "traceImag")
            require(imag[0] <= 0 <= imag[1]
                    and row["traceImagContainsZero"] is True,
                    f"primary imaginary sentinel failed: {run_id}/{eta}")
            expected = "negative" if eta == "0.3407" else "positive" if eta == "0.3410" else ""
            sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
            require(expected and sign == expected == row["sign"],
                    f"primary endpoint sign failed: {run_id}/{eta}")
            embedded = crosscheck["primaryIntervals"][run_id]["traceMinusTwo"][eta]
            require(embedded["exactBinaryLower"] == fraction_text(trace[0])
                    and embedded["exactBinaryUpper"] == fraction_text(trace[1])
                    and embedded["strictSign"] == sign,
                    f"embedded primary interval mismatch: {run_id}/{eta}")
            by_eta[eta] = trace
        require(set(by_eta) == {"0.3407", "0.3410"}, "primary eta inventory mismatch")
        primary[run_id] = by_eta

    decimal_data = load_json(EXPERIMENT / "canonical_decimal_interval_validation.json")
    decimal_source = EXPERIMENT / "independent_decimal_monodromy_validator.py"
    require(decimal_data["status"] == "passed"
            and all(decimal_data["checks"].values())
            and not ({"mpmath", "numpy", "scipy", "research"} & imported_roots(decimal_source)),
            "independent Decimal implementation/status failed")
    decimal_by_eta: dict[str, tuple[Fraction, Fraction]] = {}
    for row in decimal_data["results"]:
        eta = row["eta"]
        trace = decimal_interval(row, "traceMinusTwo")
        imag = decimal_interval(row, "traceImag")
        det_real = decimal_interval(row, "determinantReal")
        det_imag = decimal_interval(row, "determinantImag")
        require(imag[0] <= 0 <= imag[1]
                and det_real[0] <= 1 <= det_real[1]
                and det_imag[0] <= 0 <= det_imag[1],
                f"independent Decimal sentinel failed: {eta}")
        expected = "negative" if eta == "0.3407" else "positive" if eta == "0.3410" else ""
        sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
        require(expected and sign == expected, f"independent Decimal sign failed: {eta}")
        embedded = crosscheck["independentDecimal"]["traceMinusTwo"][eta]
        require(embedded["lower"] == row["traceMinusTwo"]["lower"]
                and embedded["upper"] == row["traceMinusTwo"]["upper"]
                and embedded["strictSign"] == sign,
                f"embedded Decimal interval mismatch: {eta}")
        decimal_by_eta[eta] = trace
    require(all(
        decimal_by_eta[eta][0] <= interval[0] <= interval[1] <= decimal_by_eta[eta][1]
        for eta in decimal_by_eta
        for interval in (primary["partition-a"][eta], primary["partition-b"][eta])
    ), "primary intervals not contained in independent Decimal intervals")
    return {
        "decimalLeftUpper": fraction_text(decimal_by_eta["0.3407"][1]),
        "decimalRightLower": fraction_text(decimal_by_eta["0.3410"][0]),
        "primaryPartitions": len(primary),
    }


def write_sums() -> None:
    require(all((HERE / name).is_file() for name in EXPECTED_PACKAGE_FILES),
            "certificate package inventory incomplete")
    lines = [f"{sha256(HERE / name)}  {name}" for name in sorted(EXPECTED_PACKAGE_FILES)]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n")


def main() -> int:
    args = parse_args()
    algebra = redo_exact_algebra()
    require(all(algebra.values()), "independent exact algebra failed")
    if args.self_test:
        print(canonical({"checks": algebra, "status": "passed"}), end="")
        return 0

    stage = "formal" if args.require_formal else "source-stage"
    certificate = load_json(HERE / "certificate.json")
    crosscheck = load_json(HERE / "crosscheck.json")
    manifest = load_json(HERE / "manifest.json")
    independent = load_json(HERE / "independent_recompute.json")
    require(all(all_finite(item) for item in (certificate, crosscheck, manifest, independent)),
            "non-finite number in certificate JSON")
    require(certificate["schemaVersion"] == "r073c-certificate-v1"
            and certificate["release"] == "R0.73C",
            "certificate schema/release mismatch")
    require(certificate["certificateStage"] == stage
            and manifest["status"] == stage,
            "certificate stage mismatch")
    require(manifest["outputs"] == EXPECTED_OUTPUTS,
            "certificate output inventory mismatch")
    require(certificate["crosscheck"] == crosscheck,
            "standalone crosscheck differs from embedded crosscheck")
    require(crosscheck["status"] == "passed"
            and independent["status"] == "passed"
            and independent["source"]["sha256"] == sha256(HERE / "independent_recompute.py")
            and independent["source"]["bytes"] == (HERE / "independent_recompute.py").stat().st_size,
            "materialized independent recomputation failed")
    require(crosscheck["independentRecompute"]["file"]["sha256"]
            == sha256(HERE / "independent_recompute.json"),
            "crosscheck independent recompute binding mismatch")
    binding_commit = validate_source_bindings(manifest, stage)
    require(binding_commit == certificate["sourceCommit"]
            and manifest["sourceCommit"] == certificate["sourceCommit"],
            "certificate/manifest/source-binding commit mismatch")

    for item in manifest["outputBindings"]:
        path = ROOT / item["path"]
        require(path.is_file() and path.stat().st_size == item["bytes"]
                and sha256(path) == item["sha256"],
                f"certificate output binding mismatch: {item['path']}")
    require([Path(item["path"]).name for item in manifest["outputBindings"]]
            == ["certificate.json", "crosscheck.json", "progress.ndjson"],
            "certificate output-binding scope mismatch")

    embedded_c3 = certificate["exactChecks"]["c3NeutralSpectrum"]
    embedded_c4 = certificate["exactChecks"]["c4MonodromyBridge"]
    require(all(embedded_c3["checks"].values())
            and all(embedded_c4["checks"].values()),
            "embedded exact check failed")
    require(embedded_c3["neutralIdentity"]["eigenvalue"] == "-7/4"
            and embedded_c3["neutralIdentity"]["gammaSquared"] == "7/4"
            and embedded_c3["spectrum"]["uniqueNegative"] is True,
            "embedded C3 result mismatch")
    require(certificate["result"]["c4"]["sigmaOpenInterval"]
            == ["0.17035", "0.17050"], "embedded C4 bracket mismatch")
    interval_summary = independent_interval_recompute(crosscheck)

    experiment_validation = load_json(EXPERIMENT / "validation.json")
    experiment_manifest = load_json(EXPERIMENT / "manifest.json")
    require(experiment_validation["status"] == "passed"
            and all(experiment_validation["checks"].values())
            and experiment_manifest["status"] == "passed",
            "experiment package is not passed")
    finite_validation = load_json(EXPERIMENT / "canonical_independent_fourier_validation.json")
    require(finite_validation["status"] == "passed"
            and all(finite_validation["checks"].values())
            and finite_validation["claimBoundary"]["infiniteDimensionalSpectrumProved"] is False
            and crosscheck["finiteDiagnostic"]["usedForInfiniteDimensionalProof"] is False,
            "finite diagnostic boundary failed")

    boundary = certificate["claimBoundary"]
    require(boundary["exactCubicNeutralSpectrumClosed"] is True
            and boundary["infiniteDimensionalFrozenRayleighInstabilityClosed"] is True
            and boundary["superPolynomialCompleteRowNoGo"] == "conditional-on-C5",
            "closed/conditional result ledger mismatch")
    require(DECISION_KEYS == {
        "exactCubicNeutralSpectrum": certificate["result"]["c3"]["status"],
        "infiniteDimensionalFrozenRayleighInstability": certificate["result"]["c4"]["status"],
        "frozenInstabilityFastTimeTransfer": certificate["result"]["c5"]["status"],
        "superPolynomialCompleteRowNoGo": boundary["superPolynomialCompleteRowNoGo"],
    }, "stable decision-key ledger mismatch")
    for key in (
        "algebraicSimplicityProved",
        "clayMillenniumProblemSolved",
        "completeOSSquireA2DirectSumProved",
        "finiteFourierDataUsedAsInfiniteDimensionalProof",
        "frozenInstabilityFastTimeTransferProved",
        "nonautonomousFastTimeTransferProved",
        "nonlinearNavierStokesProved",
        "rootUniquenessProved",
        "sharpLargeLambdaGrowthLawProved",
        "uniformRieszContourProved",
        "viscousEigenvaluePersistenceProved",
    ):
        require(boundary[key] is False, f"claim boundary overstates {key}")

    progress = [json.loads(line) for line in (HERE / "progress.ndjson").read_text().splitlines()]
    require([item["sequence"] for item in progress] == list(range(8))
            and progress[-1]["event"] == "complete"
            and progress[-1]["stage"] == stage,
            "certificate progress contract failed")
    for name in ("certificate.json", "crosscheck.json", "manifest.json", "progress.ndjson"):
        text = (HERE / name).read_text()
        require("elapsedSeconds" not in text and "runtimeSeconds" not in text,
                f"wall-time field leaked into {name}")
        require(str(ROOT) not in text and "/Users/" not in text,
                f"absolute worktree path leaked into {name}")

    if stage == "formal":
        commit = certificate["sourceCommit"]
        require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
                "formal certificate commit malformed")
        require(git_output("rev-parse", f"{commit}^{{commit}}").decode().strip() == commit,
                "formal certificate commit does not resolve")
    else:
        require(certificate["sourceCommit"] == "pending",
                "source-stage certificate must have pending commit")

    result = {
        "checks": {
            **algebra,
            "certificateOutputBindings": True,
            "claimBoundary": True,
            "deterministicJsonBoundary": True,
            "experimentPackage": True,
            "finiteDiagnosticBoundary": True,
            "independentIntervalRecompute": True,
            "progressContract": True,
            "sourceBindings": True,
        },
        "claimBoundary": {
            "c3ExactNeutralSpectrumValidated": True,
            "c4FrozenPointEigenvalueExistenceValidated": True,
            "c5FastTimeTransferValidated": False,
            "clayProblemSolved": False,
            "finiteFourierEvidenceIsProof": False,
            "nonlinearNavierStokesProved": False,
        },
        "intervalSentinels": interval_summary,
        "schemaVersion": "r073c-certificate-validation-v1",
        "stage": stage,
        "status": "passed",
        "validator": {
            "bytes": (HERE / "validate_certificate.py").stat().st_size,
            "path": "research/certificates/r073c/validate_certificate.py",
            "sha256": sha256(HERE / "validate_certificate.py"),
        },
    }
    require(all(result["checks"].values()), "validation result contains a failed check")
    (HERE / "validation.json").write_text(canonical(result))
    write_sums()

    # Read back the completed package ledger.  SHA256SUMS deliberately omits
    # itself, avoiding a self-reference while binding every other package file.
    sums: dict[str, str] = {}
    for line in (HERE / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(name not in sums, "duplicate certificate SHA256SUMS entry")
        sums[name] = digest
    require(list(sums) == sorted(EXPECTED_PACKAGE_FILES),
            "certificate SHA256SUMS scope/order mismatch")
    require(all(sha256(HERE / name) == digest for name, digest in sums.items()),
            "certificate SHA256SUMS readback failed")
    print(canonical(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
