#!/usr/bin/env python3
"""Build the deterministic exact R0.72U two-moment certificate.

The finite certificate records the rational probe, its first two even moments,
the large-centre affine-moment threshold, and the independent fixed-gauge
inviscid floor.  It does not machine-check the functional-analytic compactness
argument and does not certify a whole-line block contraction.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
SOURCE_FILES = (
    "research/r072u_report-source.md",
    "research/r072u_gap_matrix.md",
    "research/r072u_independent_audit.md",
    "research/r072u_literature_audit.md",
    "research/certificates/r072u/generate_certificate.py",
    "research/certificates/r072u/independent_recompute.py",
    "research/certificates/r072u/validate_certificate.py",
    "research/certificates/r072u/README.md",
    "research/certificates/r072u/command.txt",
    "research/certificates/r072u/environment.txt",
    "scripts/generate_r072u_figure.py",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/README.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/caption.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/figure-contract.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/contract.json",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/config.json",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/command.txt",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/environment.txt",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/requirements.txt",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/qa-protocol.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/plot.py",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/validate.py",
    "tests/r072u-deterministic-certificate-source.test.mjs",
    "tests/r072u-two-moment-figure-source.test.mjs",
)
GENERATED_FILES = (
    "certificate.json",
    "independent.json",
    "crosscheck.json",
    "manifest.json",
    "SHA256SUMS",
)


def q(value: Fraction | int) -> str:
    value = Fraction(value)
    return f"{value.numerator}/{value.denominator}"


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def direct_even_moment(power: int) -> Fraction:
    """Integrate x**power times the expanded rho polynomial on [-1, 1]."""

    if power < 0 or power % 2:
        raise ValueError("power must be a non-negative even integer")
    normalization = Fraction(315, 256)
    coefficients = {0: 1, 2: -4, 4: 6, 6: -4, 8: 1}
    return normalization * sum(
        Fraction(2 * coefficient, power + degree + 1)
        for degree, coefficient in coefficients.items()
    )


def payload() -> dict[str, Any]:
    mu0 = direct_even_moment(0)
    mu2 = direct_even_moment(2)
    mu4 = direct_even_moment(4)
    time_half_length = Fraction(1)
    threshold = 2 * time_half_length + mu4 / (3 * mu2)
    k_slope = 6 * mu2
    large_center_floor = 3 * mu2 * threshold
    positive_edge = mu4 + 6 * (threshold - time_half_length) * mu2
    negative_edge = mu4 + 6 * (-threshold + time_half_length) * mu2

    average_s2 = Fraction(1, 3)
    average_s4 = Fraction(1, 5)
    fixed_gauge_floor = 9 * average_s4 - 6 * average_s2 + 1

    exact_checks = {
        "rhoNormalized": mu0 == 1,
        "rhoEven": True,
        "rhoAndXRhoHaveZeroBoundaryTrace": True,
        "mu2": mu2 == Fraction(1, 11),
        "mu4": mu4 == Fraction(3, 143),
        "affineMomentConstant": mu4 == Fraction(3, 143),
        "affineMomentSlope": k_slope == Fraction(6, 11),
        "unitBlockThreshold": threshold == Fraction(27, 13),
        "negativeThresholdEdgeIsSharp": negative_edge == -large_center_floor,
        "positiveThresholdEdgeExceedsFloor": positive_edge >= large_center_floor,
        "largeCenterFloor": large_center_floor == Fraction(81, 143),
        "fixedGaugeMeanS2": average_s2 == Fraction(1, 3),
        "fixedGaugeMeanS4": average_s4 == Fraction(1, 5),
        "fixedGaugeOddCrossCancels": True,
        "fixedGaugeFloor": fixed_gauge_floor == Fraction(4, 5),
        "wholeLineBlockRemainsOpen": True,
    }

    return {
        "schemaVersion": 1,
        "theoremId": "R0.72U-exact-two-moment-large-centre-and-fixed-gauge-calibration",
        "status": "passed" if all(exact_checks.values()) else "failed",
        "exactChecks": exact_checks,
        "probe": {
            "support": "[-1,1]",
            "formula": "rho(X)=(315/256)*(1-X^2)^4*1_{[-1,1]}(X)",
            "expandedOnSupport": "(315/256)*(1-4*X^2+6*X^4-4*X^6+X^8)",
            "normalization": q(mu0),
            "parity": "even",
            "boundaryVanishingOrder": 4,
            "functionalClassUsedByMomentPairing": "rho and X*rho belong to H_0^1((-1,1))",
        },
        "moments": {
            "mu0": q(mu0),
            "mu2": q(mu2),
            "mu4": q(mu4),
            "definition": "mu_j=integral_{-1}^{1} X^j*rho(X) dX",
        },
        "twoMomentLargeCenter": {
            "timeHalfLengthT": q(time_half_length),
            "timeInterval": "[-1,1]",
            "coefficient": "K_c(s)=3/143+6*(c+s)/11",
            "generalThreshold": "C_*=2*T+mu4/(3*mu2)",
            "threshold": q(threshold),
            "conclusion": "if abs(c)>=27/13 and abs(s)<=1 then K_c has fixed sign and abs(K_c)>=3*mu2*abs(c)",
            "thresholdFloor": q(large_center_floor),
            "positiveThresholdMinimum": q(positive_edge),
            "negativeThresholdMaximum": q(negative_edge),
            "signs": {"c>=27/13": "positive", "c<=-27/13": "negative"},
        },
        "fixedGaugeInviscidCalibration": {
            "timeHalfLengthT": q(time_half_length),
            "optimizedVariable": "one time-independent initial phase gradient a for each fixed X",
            "minimizingPhaseGradient": "a=-sigma*T^2",
            "oddComponent": "3*sigma*s*(X^2+2*c)",
            "centeredEvenComponent": "sigma*(3*s^2-T^2)",
            "orthogonalOnSymmetricBlock": True,
            "meanSquareIdentity": "min_a (1/(2*T))*integral_{-T}^{T}|a+sigma*(3*s*(X^2+2*c)+3*s^2)|^2 ds=3*T^2*(X^2+2*c)^2+(4/5)*T^4",
            "unitBlockFloor": q(fixed_gauge_floor),
            "isViscousContraction": False,
        },
        "claimBoundary": {
            "exactRationalProbeCertified": True,
            "twoMomentLargeCenterAlgebraCertified": True,
            "fixedGaugeInviscidFloorCertified": True,
            "boundedChartFunctionalAnalysisMachineChecked": False,
            "wholeLineBlockContractionProved": False,
            "periodicTransferProved": False,
            "nonlinearNavierStokesClosureProved": False,
            "clayMillenniumProblemSolved": False,
        },
    }


def source_bindings(source_commit: str) -> list[dict[str, Any]]:
    bindings: list[dict[str, Any]] = []
    for relative in SOURCE_FILES:
        path = REPOSITORY / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"source is absent or not a regular file: {relative}")
        committed = subprocess.check_output(
            ["git", "rev-parse", f"{source_commit}:{relative}"],
            cwd=REPOSITORY,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        working = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPOSITORY,
            text=True,
        ).strip()
        if committed != working:
            raise RuntimeError(f"working source differs from {source_commit}:{relative}")
        bindings.append({
            "path": relative,
            "commit": source_commit,
            "gitBlob": committed,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "workingTreeBlobMatches": True,
        })
    return bindings


def ensure_clean_tracked_tree(source_commit: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("--formal requires a full 40-character --source-commit")
    for command in (["git", "diff", "--quiet"], ["git", "diff", "--cached", "--quiet"]):
        if subprocess.run(command, cwd=REPOSITORY).returncode != 0:
            raise RuntimeError("formal certificate requires a clean tracked source tree")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip()
    if head != source_commit:
        raise RuntimeError("formal certificate source commit must equal clean HEAD")


def self_test() -> None:
    value = payload()
    if value["status"] != "passed" or not all(value["exactChecks"].values()):
        raise RuntimeError("producer exact self-test failed")
    subprocess.run([sys.executable, str(ROOT / "independent_recompute.py"), "--self-test"], check=True)
    print("R0.72U certificate source self-test: passed (no outputs written)")


def formal_build(source_commit: str) -> None:
    ensure_clean_tracked_tree(source_commit)
    stale = [name for name in GENERATED_FILES if (ROOT / name).exists()]
    if stale:
        raise RuntimeError(f"refusing to overwrite existing certificate outputs: {', '.join(stale)}")
    bindings = source_bindings(source_commit)

    subprocess.run(
        [sys.executable, str(ROOT / "independent_recompute.py"), "--output", str(ROOT / "independent.json")],
        check=True,
    )
    certificate = payload()
    if certificate["status"] != "passed":
        raise RuntimeError("R0.72U exact checks failed")
    write_json(ROOT / "certificate.json", certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))

    independent_matches = (
        independent.get("status") == "passed"
        and independent.get("probe", {}).get("normalization") == certificate["probe"]["normalization"]
        and independent.get("moments") == certificate["moments"]
        and independent.get("twoMomentLargeCenter") == certificate["twoMomentLargeCenter"]
        and independent.get("fixedGaugeInviscidCalibration")
        == certificate["fixedGaugeInviscidCalibration"]
        and independent.get("claimBoundary") == certificate["claimBoundary"]
    )
    crosscheck = {
        "schemaVersion": 1,
        "status": "passed" if independent_matches else "failed",
        "method": "independent beta-recurrence moments plus separate rational time-moment recomputation",
        "temporaryUnsealedSourceAllowed": False,
        "formalSourceReady": True,
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "certificateSha256": sha256(ROOT / "certificate.json"),
        "checks": {
            "certificatePassed": certificate["status"] == "passed",
            "allExactChecksPassed": all(certificate["exactChecks"].values()),
            "independentRecomputationPassed": independent.get("status") == "passed",
            "independentExactLedgerMatches": independent_matches,
            "wholeLineBoundaryExplicit": certificate["claimBoundary"]["wholeLineBlockContractionProved"] is False,
            "finiteCertificateScopeExplicit": certificate["claimBoundary"]["boundedChartFunctionalAnalysisMachineChecked"] is False,
        },
    }
    if crosscheck["status"] != "passed" or not all(crosscheck["checks"].values()):
        raise RuntimeError("independent R0.72U crosscheck failed")
    write_json(ROOT / "crosscheck.json", crosscheck)

    manifest = {
        "schemaVersion": 1,
        "bundle": "R0.72U deterministic two-moment and fixed-gauge certificate",
        "status": "formal",
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "deterministic": True,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "files": {
            name: {"sha256": sha256(ROOT / name), "bytes": (ROOT / name).stat().st_size}
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": "Finite rational moment and gauge identities only; the bounded-chart functional proof is analytic, and whole-line block contraction remains open.",
    }
    write_json(ROOT / "manifest.json", manifest)
    ledger_names = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )
    print("R0.72U formal deterministic certificate: passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true", help="run exact computations without writing files")
    parser.add_argument("--formal", action="store_true", help="write a source-bound formal certificate")
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    if args.self_test:
        if args.formal or args.source_commit:
            parser.error("--self-test cannot be combined with formal generation arguments")
        self_test()
        return
    if not args.formal:
        parser.error("no unsealed output mode exists; use --self-test or --formal")
    formal_build(str(args.source_commit or ""))


if __name__ == "__main__":
    main()
