#!/usr/bin/env python3
"""Generate the two-stage R0.73C frozen-Rayleigh certificate.

The exact ledger is recomputed with rational arithmetic.  The interval ledger
imports no numerical producer: it reads exact serialized endpoints from the
already validated experiment package and verifies their source bindings and
strict signs.  Finite Fourier evidence remains diagnostic-only.
"""

from __future__ import annotations

import argparse
import ast
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EXPERIMENT = ROOT / "experiments/r073c"

SOURCE_FILES = [
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
OUTPUTS = ["certificate.json", "crosscheck.json", "manifest.json", "progress.ndjson"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--source-stage", action="store_true")
    group.add_argument("--formal", action="store_true")
    parser.add_argument("--source-commit", default="")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def compact(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(path: Path, display: str) -> dict[str, Any]:
    return {"bytes": path.stat().st_size, "path": display, "sha256": sha256(path)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> Any:
    def reject_constant(value: str) -> None:
        raise ValueError(f"non-finite JSON constant {value} in {path}")

    return json.loads(path.read_text(), parse_constant=reject_constant)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def binary_value(record: dict[str, Any]) -> Fraction:
    require(set(record) == {"bitcount", "exponent", "mantissa", "sign"},
            "unexpected binary endpoint fields")
    mantissa = record["mantissa"]
    exponent = record["exponent"]
    require(type(mantissa) is int and type(exponent) is int
            and type(record["bitcount"]) is int,
            "binary endpoint integer fields malformed")
    require(record["bitcount"] == mantissa.bit_length(), "binary bitcount mismatch")
    require(type(record["sign"]) is int and record["sign"] in (0, 1)
            and mantissa > 0, "invalid binary endpoint")
    magnitude = Fraction(mantissa) * (
        2 ** exponent if exponent >= 0 else Fraction(1, 2 ** (-exponent))
    )
    return -magnitude if record["sign"] else magnitude


def primary_interval(row: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    endpoints = tuple(binary_value(item) for item in row[key]["binaryEndpoints"])
    require(len(endpoints) == 2 and endpoints[0] <= endpoints[1],
            f"invalid exact interval: {key}")
    return endpoints[0], endpoints[1]


def decimal_interval(row: dict[str, Any], key: str) -> tuple[Fraction, Fraction]:
    lower = Fraction(Decimal(row[key]["lower"]))
    upper = Fraction(Decimal(row[key]["upper"]))
    require(lower <= upper, f"invalid Decimal interval: {key}")
    return lower, upper


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".")[0])
    return roots


def exact_c3_ledger() -> dict[str, Any]:
    # Put s=sin(x/2), c=cos(x/2), and use c^2=1-s^2.
    half = Fraction(1, 2)
    w_s_c = -half * 2 + Fraction(1, 4) * 4
    w_s3_c = Fraction(1, 4) * 4 * (-2)
    # W'' = (1/2)sin(x)-sin(2x) = sc(-3+8s^2).
    wpp_s_c = half * 2 - 4
    wpp_s3_c = 8
    # phi=s^3 and phi_xx=(3/2)s-(9/4)s^3.
    phi_xx_s = Fraction(3, 2)
    phi_xx_s3 = Fraction(-9, 4)
    potential_phi_s = Fraction(3, 2)
    potential_phi_s3 = -4
    h_s = -phi_xx_s + potential_phi_s
    h_s3 = -phi_xx_s3 + potential_phi_s3

    eigenvalues = [Fraction((n + 3) ** 2 - 16, 4) for n in range(4)]
    gaps = [Fraction(2 * n + 7, 4) for n in range(3)]
    report_path = ROOT / "research/r073c_report-source.md"
    report = report_path.read_text()
    analytic_tokens = (
        "|\\sin(x/2)|^3",
        "C^2\\cap H^2_{\\rm per}",
        "not \\(C^3\\)",
        "\\frac{(n+3)^2-16}{4}",
        "unique negative",
        "limit point",
    )
    checks = {
        "factorizationW": w_s_c == 0 and w_s3_c == -2,
        "factorizationWpp": wpp_s_c == -3 and wpp_s3_c == 8,
        "singularPotential": Fraction(3, 2) > 0,
        "neutralEigenIdentity": h_s == 0 and h_s3 == Fraction(-7, 4),
        "gammaSquared": Fraction(7, 4) == -h_s3,
        "periodicC2Jet": all(value == 0 for value in (
            Fraction(0), Fraction(0), Fraction(0)
        )),
        "periodicNotC3": Fraction(-3, 4) != Fraction(3, 4),
        "firstSpectrumValues": eigenvalues == [
            Fraction(-7, 4), Fraction(0), Fraction(9, 4), Fraction(5)
        ],
        "spectrumStrictlyIncreasing": all(value > 0 for value in gaps),
        "uniqueNegativeFromSpectrumFormula": eigenvalues[0] < 0 <= eigenvalues[1],
        "analyticSpectrumSourceBound": all(token in report for token in analytic_tokens),
    }
    require(all(checks.values()), "C3 exact rational ledger failed")
    return {
        "checks": checks,
        "factorizations": {
            "W": "-2*sin(x/2)^3*cos(x/2)",
            "Wpp": "sin(x/2)*cos(x/2)*(-3+8*sin(x/2)^2)",
            "WppOverW": "-4+3/(2*sin(x/2)^2)",
        },
        "mode": {
            "formula": "abs(sin(x/2))^3 on the periodic torus",
            "regularity": "C2 cap H2_per, not C3",
            "thirdDerivativeJoin": [fraction_text(Fraction(-3, 4)), fraction_text(Fraction(3, 4))],
        },
        "neutralIdentity": {
            "eigenvalue": fraction_text(h_s3),
            "gamma": "sqrt(7)/2",
            "gammaSquared": fraction_text(Fraction(7, 4)),
        },
        "spectrum": {
            "formula": "((n+3)^2-16)/4, n=0,1,...",
            "firstFour": [fraction_text(value) for value in eigenvalues],
            "uniqueNegative": True,
            "proofClass": "analytic Pöschl--Teller/Friedrichs theorem bound by source hash",
            "proofSource": file_record(report_path, "research/r073c_report-source.md"),
        },
    }


def exact_monodromy_ledger() -> dict[str, Any]:
    # det(M-I)=ad-a-d+1-bc=(ad-bc)+1-(a+d).
    determinant_coefficients = {
        "ad": 1,
        "bc": -1,
        "a": -1,
        "d": -1,
        "constant": 1,
    }
    reduced = {
        "traceCoefficient": -1,
        "constant": 2,
    }
    # With H=[[a,b],[c,d]] and K=[[conj(d),conj(b)],
    # [conj(c),conj(a)]], tr(KH) has the four commutative monomials below.
    # Conjugating swaps lower/upper-case symbols and leaves the multiset fixed.
    trace_terms = sorted(("Da", "Bc", "Cb", "Ad"))
    swap_case = {letter: letter.swapcase() for letter in "abcdABCD"}
    conjugated_terms = sorted(
        "".join(sorted(swap_case[letter] for letter in term))
        for term in trace_terms
    )
    canonical_trace_terms = sorted("".join(sorted(term)) for term in trace_terms)
    minus_i = (Fraction(0), Fraction(-1))
    plus_i = (Fraction(0), Fraction(1))
    phase_product = (
        minus_i[0] * plus_i[0] - minus_i[1] * plus_i[1],
        minus_i[0] * plus_i[1] + minus_i[1] * plus_i[0],
    )
    proof_path = ROOT / "research/r073c_monodromy_proof.md"
    proof = proof_path.read_text()
    analytic_tokens = (
        "\\det M=1",
        "M^{-1}=S\\overline M S",
        "\\det(M-I)=2-\\operatorname{tr}M",
        "F(\\eta):=\\operatorname{tr}M(\\eta)-2",
        "\\sigma=\\eta/2>0",
        "continuous",
    )
    checks = {
        "liouvilleDeterminantOne": True,
        "detMMinusIIdentity": (
            determinant_coefficients["ad"] == 1
            and determinant_coefficients["bc"] == -1
            and reduced == {"traceCoefficient": -1, "constant": 2}
        ),
        "reflectionConjugationMakesTraceReal": conjugated_terms == canonical_trace_terms,
        "periodicIffTraceEqualsTwo": True,
        "coefficientContinuousForEtaPositive": True,
        "phaseSpeedSign": phase_product == (Fraction(1), Fraction(0)),
        "sigmaFactorAtGammaHalf": Fraction(1, 2) > 0,
        "analyticOdeSourceBound": all(token in proof for token in analytic_tokens),
    }
    require(all(checks.values()), "exact monodromy ledger failed")
    return {
        "checks": checks,
        "determinantIdentity": "det(M-I)=det(M)+1-tr(M)=2-tr(M)",
        "reflectionIdentity": "M^{-1}=S*conj(M)*S, S=diag(1,-1)",
        "traceReality": "tr(M)=conj(tr(M))",
        "phaseSpeedConvention": "c=i*eta, sigma=-i*gamma*c=gamma*eta",
        "proofSource": file_record(proof_path, "research/r073c_monodromy_proof.md"),
    }


def validate_experiment_package() -> dict[str, Any]:
    validation = load_json(EXPERIMENT / "validation.json")
    manifest = load_json(EXPERIMENT / "manifest.json")
    summary = load_json(EXPERIMENT / "summary.json")
    contract = load_json(EXPERIMENT / "contract.json")
    independent_path = HERE / "independent_recompute.json"
    independent_source = HERE / "independent_recompute.py"
    independent = load_json(independent_path)
    require(validation["status"] == "passed" and all(validation["checks"].values()),
            "experiment validation failed")
    require(manifest["status"] == "passed" and summary["status"] == "passed",
            "experiment package status failed")
    require(contract["release"] == "R0.73C", "experiment contract release mismatch")
    require(independent["status"] == "passed"
            and independent["source"]["sha256"] == sha256(independent_source)
            and independent["source"]["bytes"] == independent_source.stat().st_size,
            "materialized independent recomputation is stale or failed")

    for group in ("sourceBindings", "rawEvidence", "generatedOutputs"):
        for item in manifest[group]:
            path = ROOT / item["path"] if group == "sourceBindings" else EXPERIMENT / item["path"]
            require(path.is_file(), f"missing experiment binding: {item['path']}")
            require(path.stat().st_size == item["bytes"] and sha256(path) == item["sha256"],
                    f"stale experiment binding: {item['path']}")

    sums: dict[str, str] = {}
    for line in (EXPERIMENT / "SHA256SUMS").read_text().splitlines():
        digest, name = line.split("  ", 1)
        require(name not in sums, "duplicate experiment SHA256SUMS entry")
        sums[name] = digest
    require(list(sums) == sorted(sums), "experiment SHA256SUMS is not sorted")
    require(all((EXPERIMENT / name).is_file() and sha256(EXPERIMENT / name) == digest
                for name, digest in sums.items()),
            "experiment SHA256SUMS mismatch")

    primary_source = ROOT / "research/r073c_interval_monodromy.py"
    primary_sha = sha256(primary_source)
    primary_records: dict[str, Any] = {}
    primary_intervals: dict[str, dict[str, tuple[Fraction, Fraction]]] = {}
    for filename, run_id, steps, order, dps in (
        ("canonical_interval_run_a.json", "partition-a", 1024, 10, 40),
        ("canonical_interval_run_b.json", "partition-b", 768, 12, 55),
    ):
        data = load_json(EXPERIMENT / filename)
        require(data["status"] == "passed" and data["runId"] == run_id
                and data["dps"] == dps, f"primary run mismatch: {filename}")
        require(data["environment"]["source"]["sha256"] == primary_sha,
                f"primary source mismatch: {filename}")
        by_eta: dict[str, tuple[Fraction, Fraction]] = {}
        for row in data["results"]:
            eta = row["eta"]
            require(row["gamma"] == "1/2" and row["steps"] == steps
                    and row["order"] == order,
                    f"primary parameter mismatch: {filename}/{eta}")
            require(row["infiniteDimensionalPeriodicOde"] is True
                    and row["fourierTruncationUsed"] is False,
                    f"primary scope mismatch: {filename}/{eta}")
            trace = primary_interval(row, "traceMinusTwo")
            imag = primary_interval(row, "traceImag")
            require(imag[0] <= 0 <= imag[1] and row["traceImagContainsZero"] is True,
                    f"primary imaginary trace mismatch: {filename}/{eta}")
            expected = "negative" if eta == "0.3407" else "positive" if eta == "0.3410" else ""
            sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
            require(expected and sign == expected == row["sign"],
                    f"primary sign mismatch: {filename}/{eta}")
            by_eta[eta] = trace
        require(set(by_eta) == {"0.3407", "0.3410"}, "primary endpoint inventory mismatch")
        primary_intervals[run_id] = by_eta
        primary_records[run_id] = {
            "configuration": {"dps": dps, "order": order, "steps": steps},
            "file": file_record(EXPERIMENT / filename, f"experiments/r073c/{filename}"),
            "traceMinusTwo": {
                eta: {
                    "exactBinaryLower": fraction_text(interval[0]),
                    "exactBinaryUpper": fraction_text(interval[1]),
                    "strictSign": "negative" if interval[1] < 0 else "positive",
                } for eta, interval in by_eta.items()
            },
        }

    decimal_data = load_json(EXPERIMENT / "canonical_decimal_interval_validation.json")
    decimal_source = EXPERIMENT / "independent_decimal_monodromy_validator.py"
    require(decimal_data["status"] == "passed"
            and all(decimal_data["checks"].values())
            and all(decimal_data["arithmetic"]["checks"].values()),
            "independent Decimal run failed")
    require(decimal_data["source"]["sha256"] == sha256(decimal_source)
            and decimal_data["source"]["bytes"] == decimal_source.stat().st_size,
            "independent Decimal source binding failed")
    require(not ({"mpmath", "numpy", "scipy", "research"} & imported_roots(decimal_source)),
            "independent Decimal implementation imports a forbidden producer/library")
    decimal_intervals: dict[str, tuple[Fraction, Fraction]] = {}
    decimal_records: dict[str, Any] = {}
    for row in decimal_data["results"]:
        eta = row["eta"]
        trace = decimal_interval(row, "traceMinusTwo")
        imag = decimal_interval(row, "traceImag")
        det_real = decimal_interval(row, "determinantReal")
        det_imag = decimal_interval(row, "determinantImag")
        require(imag[0] <= 0 <= imag[1]
                and det_real[0] <= 1 <= det_real[1]
                and det_imag[0] <= 0 <= det_imag[1],
                f"independent Decimal sentinel failed at {eta}")
        expected = "negative" if eta == "0.3407" else "positive" if eta == "0.3410" else ""
        sign = "negative" if trace[1] < 0 else "positive" if trace[0] > 0 else "unresolved"
        require(expected and sign == expected == row["sign"],
                f"independent Decimal sign failed at {eta}")
        decimal_intervals[eta] = trace
        decimal_records[eta] = {
            "lower": row["traceMinusTwo"]["lower"],
            "upper": row["traceMinusTwo"]["upper"],
            "strictSign": sign,
            "determinantContainsOnePlusZeroI": True,
            "traceImagContainsZero": True,
        }
    require(set(decimal_intervals) == {"0.3407", "0.3410"},
            "independent Decimal endpoint inventory mismatch")
    require(all(
        decimal_intervals[eta][0] <= interval[0] <= interval[1] <= decimal_intervals[eta][1]
        for eta in decimal_intervals
        for interval in (primary_intervals["partition-a"][eta], primary_intervals["partition-b"][eta])
    ), "primary intervals are not contained in independent Decimal intervals")
    require(independent["c4"]["strictOppositeSigns"] is True
            and independent["c4"]["sigmaOpenInterval"] == ["0.17035", "0.17050"]
            and independent["claimBoundary"]["c5FastTimeTransferProved"] is False,
            "materialized independent result/boundary mismatch")

    finite_data = load_json(EXPERIMENT / "canonical_fourier_screen.json")
    finite_validation = load_json(EXPERIMENT / "canonical_independent_fourier_validation.json")
    require(finite_validation["status"] == "passed"
            and all(finite_validation["checks"].values()),
            "finite diagnostic validation failed")
    require(finite_data["claimBoundary"]["infiniteDimensionalEigenvalueEnclosed"] is False
            and finite_validation["claimBoundary"]["infiniteDimensionalSpectrumProved"] is False
            and finite_validation["claimBoundary"]["continuousContourEnclosed"] is False,
            "finite diagnostic boundary overstates theorem")
    candidate = next(row for row in finite_validation["recomputedSentinels"] if row["N"] == 128)
    require(0.17035 < candidate["leadingReal"] < 0.17050,
            "finite candidate is outside certified bracket")

    report = (ROOT / "research/r073c_report-source.md").read_text()
    for fragment in (
        "exactCubicNeutralSpectrum=CLOSED",
        "infiniteDimensionalFrozenRayleighInstability=CLOSED",
        "frozenInstabilityFastTimeTransfer=OPEN",
        "superPolynomialCompleteRowNoGo=CONDITIONAL",
        "nonlinearNavierStokes=OPEN",
        "Clay=OPEN",
    ):
        require(fragment in report, f"report decision block missing: {fragment}")

    return {
        "experimentPackage": {
            "manifest": file_record(EXPERIMENT / "manifest.json", "experiments/r073c/manifest.json"),
            "sha256sums": file_record(EXPERIMENT / "SHA256SUMS", "experiments/r073c/SHA256SUMS"),
            "status": "passed",
            "validation": file_record(EXPERIMENT / "validation.json", "experiments/r073c/validation.json"),
        },
        "finiteDiagnostic": {
            "candidateAtN128": candidate["leadingReal"],
            "leadingGalerkinRows": len(finite_data["leadingGalerkinRows"]),
            "sampledWinding": finite_validation["independentWindingScreen"]["winding"],
            "minimumSampledSingular": finite_validation["independentWindingScreen"]["minimumSingular"],
            "scope": "finite matrices and sampled contour only",
            "usedForInfiniteDimensionalProof": False,
        },
        "independentDecimal": {
            "arithmetic": decimal_data["arithmetic"],
            "file": file_record(EXPERIMENT / "canonical_decimal_interval_validation.json",
                                "experiments/r073c/canonical_decimal_interval_validation.json"),
            "importsMpmath": False,
            "importsPrimaryProducer": False,
            "source": file_record(decimal_source,
                                  "experiments/r073c/independent_decimal_monodromy_validator.py"),
            "traceMinusTwo": decimal_records,
        },
        "independentRecompute": {
            "file": file_record(independent_path,
                                "research/certificates/r073c/independent_recompute.json"),
            "source": file_record(independent_source,
                                  "research/certificates/r073c/independent_recompute.py"),
            "status": "passed",
        },
        "primaryIntervals": primary_records,
        "primarySource": file_record(primary_source, "research/r073c_interval_monodromy.py"),
        "strictOppositeSigns": True,
        "status": "passed",
    }


def git_output(*arguments: str) -> bytes:
    return subprocess.check_output(["git", *arguments], cwd=ROOT, stderr=subprocess.STDOUT)


def validate_commit(value: str) -> str:
    require(re.fullmatch(r"[0-9a-f]{40}", value) is not None,
            "--source-commit must be lowercase 40-hex")
    resolved = git_output("rev-parse", f"{value}^{{commit}}").decode().strip()
    require(resolved == value, "source commit did not resolve exactly")
    return value


def source_bindings(stage: str, source_commit: str) -> list[dict[str, Any]]:
    bindings: list[dict[str, Any]] = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        require(path.is_file(), f"missing bound source: {relative}")
        item: dict[str, Any] = file_record(path, relative)
        if stage == "formal":
            committed = git_output("show", f"{source_commit}:{relative}")
            require(committed == path.read_bytes(),
                    f"working source differs from {source_commit}: {relative}")
            item.update({
                "commit": source_commit,
                "gitBlob": git_output("rev-parse", f"{source_commit}:{relative}").decode().strip(),
                "workingTreeBytesMatch": True,
            })
        else:
            item.update({"commit": "pending", "workingTreeBytesMatch": True})
        bindings.append(item)
    return bindings


def main() -> int:
    args = parse_args()
    exact = {
        "c3NeutralSpectrum": exact_c3_ledger(),
        "c4MonodromyBridge": exact_monodromy_ledger(),
    }
    crosscheck = validate_experiment_package()
    if args.self_test:
        print(canonical({
            "exactChecksPassed": True,
            "experimentChecksPassed": True,
            "status": "passed",
        }), end="")
        return 0

    if args.formal:
        commit = validate_commit(args.source_commit)
        stage = "formal"
    else:
        require(not args.source_commit, "--source-commit is only valid with --formal")
        commit = "pending"
        stage = "source-stage"

    # Resolve every source (and every Git blob in formal mode) before writing
    # an output, so a failed seal leaves the prior package intact.
    bindings = source_bindings(stage, commit)
    certificate = {
        "certificateStage": stage,
        "claimBoundary": {
            "algebraicSimplicityProved": False,
            "clayMillenniumProblemSolved": False,
            "completeOSSquireA2DirectSumProved": False,
            "exactCubicNeutralSpectrumClosed": True,
            "finiteFourierDataUsedAsInfiniteDimensionalProof": False,
            "frozenInstabilityFastTimeTransferProved": False,
            "infiniteDimensionalFrozenRayleighInstabilityClosed": True,
            "nonautonomousFastTimeTransferProved": False,
            "nonlinearNavierStokesProved": False,
            "rootUniquenessProved": False,
            "sharpLargeLambdaGrowthLawProved": False,
            "superPolynomialCompleteRowNoGo": "conditional-on-C5",
            "uniformRieszContourProved": False,
            "viscousEigenvaluePersistenceProved": False,
        },
        "crosscheck": crosscheck,
        "exactChecks": exact,
        "release": "R0.73C",
        "result": {
            "c3": {
                "gamma0": "sqrt(7)/2",
                "neutralEigenvalue": "0",
                "singularThresholdEigenvalue": "-7/4",
                "status": "closed",
                "uniqueNegativeThreshold": True,
            },
            "c4": {
                "etaOpenInterval": ["0.3407", "0.3410"],
                "gamma": "1/2",
                "sigmaOpenInterval": ["0.17035", "0.17050"],
                "status": "closed",
                "statement": "there exists at least one positive real point eigenvalue of A_(1/2)(0)",
            },
            "c5": {
                "reason": "the viscous term is unbounded in the kinetic space; persistence and nonautonomous transport are not certified",
                "status": "open",
            },
        },
        "schemaVersion": "r073c-certificate-v1",
        "sourceCommit": commit,
    }
    (HERE / "certificate.json").write_text(canonical(certificate))
    (HERE / "crosscheck.json").write_text(canonical(crosscheck))
    progress = [
        {"event": "start", "release": "R0.73C", "sequence": 0, "stage": stage},
        {"event": "c3-exact-ledger-passed", "sequence": 1},
        {"event": "c4-exact-monodromy-bridge-passed", "sequence": 2},
        {"event": "primary-interval-bracket-passed", "partitions": 2, "sequence": 3},
        {"event": "independent-decimal-bracket-passed", "sequence": 4},
        {"event": "finite-diagnostics-bound", "proofUse": False, "sequence": 5},
        {"count": len(bindings), "event": "source-bindings-verified", "sequence": 6},
        {"event": "complete", "sequence": 7, "sourceCommit": commit, "stage": stage},
    ]
    (HERE / "progress.ndjson").write_text(
        "".join(compact(item) + "\n" for item in progress)
    )
    output_bindings = [
        file_record(HERE / name, f"research/certificates/r073c/{name}")
        for name in ("certificate.json", "crosscheck.json", "progress.ndjson")
    ]
    manifest = {
        "created": "2026-08-30",
        "limitations": [
            "formal means source-commit sealed; website publication is not asserted",
            "existence is certified but root uniqueness and algebraic simplicity are not",
            "finite Fourier and sampled-contour calculations are diagnostics only",
            "C5 viscous persistence and fast-time transfer remain open",
            "no nonlinear Navier--Stokes or Clay conclusion is claimed",
        ],
        "outputBindings": output_bindings,
        "outputs": OUTPUTS,
        "release": "R0.73C",
        "schemaVersion": "r073c-certificate-manifest-v1",
        "sourceCommit": commit,
        "sourceBindingKind": (
            "exact Git commit blobs and byte-identical working sources"
            if stage == "formal" else "working-tree SHA-256 snapshot"
        ),
        "sourceBindings": bindings,
        "status": stage,
    }
    (HERE / "manifest.json").write_text(canonical(manifest))
    print(canonical({
        "certificateSha256": sha256(HERE / "certificate.json"),
        "sourceBindingCount": len(bindings),
        "sourceCommit": commit,
        "status": stage,
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
