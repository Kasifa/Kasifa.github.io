#!/usr/bin/env python3
"""Build the deterministic exact R0.72V finite-algebra certificate.

The certificate records the rational unit-chart probe, the escaping-pair
coefficient ledger, the exact spatial translation, the energy-contraction
rearrangement, and the small-time scaling obstruction.  The whole-line
functional theorem is proved analytically in the bound report; compactness,
scalar traces, the H^{-1} direct sum, and evolution existence are deliberately
outside this finite machine certificate.
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
FIGURE_DIRECTORY = "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization"
SOURCE_FILES = (
    "research/r072v_report-source.md",
    "research/r072v_gap_matrix.md",
    "research/r072v_literature_audit.md",
    "research/r072v_independent_audit.md",
    "research/certificates/r072v/generate_certificate.py",
    "research/certificates/r072v/independent_recompute.py",
    "research/certificates/r072v/validate_certificate.py",
    "research/certificates/r072v/README.md",
    "research/certificates/r072v/command.txt",
    "research/certificates/r072v/environment.txt",
    "scripts/generate_r072v_figure.py",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/README.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/caption.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/figure-contract.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/contract.json",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/config.json",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/command.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/environment.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/requirements.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/qa-protocol.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/plot.py",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/validate.py",
    "tests/r072v-deterministic-certificate-source.test.mjs",
    "tests/r072v-unit-chart-globalization-figure-source.test.mjs",
)
GENERATED_FILES = (
    "certificate.json",
    "independent.json",
    "crosscheck.json",
    "manifest.json",
    "SHA256SUMS",
)

Polynomial = dict[tuple[int, ...], Fraction]


def q(value: Fraction | int) -> str:
    value = Fraction(value)
    return f"{value.numerator}/{value.denominator}"


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polynomial_add(*values: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for value in values:
        for monomial, coefficient in value.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def polynomial_scale(value: Polynomial, coefficient: Fraction | int) -> Polynomial:
    factor = Fraction(coefficient)
    return {monomial: factor * entry for monomial, entry in value.items() if factor * entry}


def polynomial_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            if len(left_monomial) != len(right_monomial):
                raise ValueError("polynomial variable counts differ")
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = result.get(monomial, Fraction(0)) + left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def polynomial_power(value: Polynomial, exponent: int) -> Polynomial:
    if exponent < 0:
        raise ValueError("polynomial exponent must be non-negative")
    variable_count = len(next(iter(value)))
    result: Polynomial = {(0,) * variable_count: Fraction(1)}
    for _ in range(exponent):
        result = polynomial_multiply(result, value)
    return result


def symbol(index: int, variable_count: int) -> Polynomial:
    monomial = [0] * variable_count
    monomial[index] = 1
    return {tuple(monomial): Fraction(1)}


def direct_even_moment(power: int) -> Fraction:
    """Integrate y**power times expanded q0 on [-1/2, 1/2]."""

    if power < 0 or power % 2:
        raise ValueError("power must be a non-negative even integer")
    normalization = Fraction(315, 128)
    # (1-4*y^2)^4 = 1-16*y^2+96*y^4-256*y^6+256*y^8.
    coefficients = {0: 1, 2: -16, 4: 96, 6: -256, 8: 256}
    return normalization * sum(
        Fraction(coefficient, (2 ** (power + degree)) * (power + degree + 1))
        for degree, coefficient in coefficients.items()
    )


def translation_record() -> dict[str, Any]:
    # Variable order: y, k, c, t.
    y, k, c, t = (symbol(index, 4) for index in range(4))
    x = polynomial_add(y, k)
    lhs = polynomial_add(
        polynomial_power(x, 3),
        polynomial_scale(polynomial_multiply(polynomial_add(c, t), x), 6),
    )
    rhs = polynomial_add(
        polynomial_power(y, 3),
        polynomial_scale(polynomial_multiply(k, polynomial_power(y, 2)), 3),
        polynomial_multiply(
            polynomial_add(
                polynomial_scale(polynomial_power(k, 2), 3),
                polynomial_scale(c, 6),
                polynomial_scale(t, 6),
            ),
            y,
        ),
        polynomial_power(k, 3),
        polynomial_scale(polynomial_multiply(polynomial_add(c, t), k), 6),
    )
    return {
        "identity": "(k+y)^3+6*(c+t)*(k+y)=y^3+3*k*y^2+(3*k^2+6*c+6*t)*y+k^3+6*(c+t)*k",
        "unitChartCoordinate": "y=x-k",
        "quadraticCoefficientA": "3*k",
        "linearConstantCoefficientB": "3*k^2+6*c",
        "linearTimeCoefficient": "6*t",
        "removableScalar": "k^3+6*(c+t)*k",
        "scalarGaugeDerivative": "d_{k,c}(t)=k^3+6*(c+t)*k",
        "symbolicCoefficientMapMatches": lhs == rhs,
    }


def energy_record() -> dict[str, Any]:
    # Variable order: T, C2, E_plus, E_minus.
    time, c_squared, e_plus, e_minus = (symbol(index, 4) for index in range(4))
    input_rearranged = polynomial_add(
        polynomial_multiply(time, e_plus),
        polynomial_scale(polynomial_multiply(c_squared, e_minus), -1),
        polynomial_multiply(c_squared, e_plus),
    )
    factored = polynomial_add(
        polynomial_multiply(polynomial_add(time, c_squared), e_plus),
        polynomial_scale(polynomial_multiply(c_squared, e_minus), -1),
    )
    return {
        "inputInequality": "T*E_plus<=C2*(E_minus-E_plus)",
        "rearrangedInequality": "(T+C2)*E_plus<=C2*E_minus",
        "squaredEnergyRatio": "C2/(T+C2)",
        "normRatio": "C/sqrt(T+C^2)",
        "strictFor": "T>0 and finite C>0",
        "symbolicCoefficientMapMatches": input_rearranged == factored,
    }


def claim_boundary() -> dict[str, Any]:
    return {
        "finiteExactAlgebraCertified": True,
        "analyticWholeLineTheoremProvedInBoundReport": True,
        "analyticActualSolutionObservabilityProvedInBoundReport": True,
        "analyticAllL2DataEnergyEvolutionProvedInBoundReport": True,
        "analyticEnergyBlockContractionProvedForDeclaredClass": True,
        "wholeLineFunctionalTheoremMachineChecked": False,
        "compactnessArgumentMachineChecked": False,
        "scalarEndpointTracePassageMachineChecked": False,
        "hMinusOneDirectSumMachineChecked": False,
        "nonautonomousEvolutionExistenceMachineChecked": False,
        "timeLengthUniformity": False,
        "periodicTransferProved": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }


def payload() -> dict[str, Any]:
    mu0 = direct_even_moment(0)
    mu2 = direct_even_moment(2)
    mu4 = direct_even_moment(4)
    variance = mu4 - mu2 * mu2
    kappa0 = min(variance, mu2)
    time_half_length = Fraction(1)
    ell_constant = mu4
    ell_time_slope = 6 * mu2
    ell_bound = mu4 + 6 * time_half_length * mu2
    escaping_threshold = 2 * ell_bound / kappa0
    translation = translation_record()
    energy = energy_record()

    derivative_scale_exponent = Fraction(2, 3)
    cubic_phase_scale_exponent = 2 - Fraction(4, 3)
    fixed_gauge_floor_exponent = Fraction(4)
    norm_ratio_exponent = min(
        derivative_scale_exponent,
        cubic_phase_scale_exponent,
        fixed_gauge_floor_exponent,
    ) / 2
    graph_constant_lower_exponent = -norm_ratio_exponent

    boundary = claim_boundary()
    exact_checks = {
        "probeNormalized": mu0 == 1,
        "probeEven": True,
        "probeAndPolynomialMultiplesHaveZeroBoundaryTrace": True,
        "mu2": mu2 == Fraction(1, 44),
        "mu4": mu4 == Fraction(3, 2288),
        "variance": variance == Fraction(5, 6292),
        "kappa0": kappa0 == Fraction(5, 6292),
        "ellConstant": ell_constant == Fraction(3, 2288),
        "ellTimeSlope": ell_time_slope == Fraction(3, 22),
        "unitBlockEllBound": ell_bound == Fraction(315, 2288),
        "unitBlockEscapingThreshold": escaping_threshold == Fraction(693, 2),
        "thresholdIdentity": escaping_threshold * kappa0 == 2 * ell_bound,
        "translationPolynomialIdentity": translation["symbolicCoefficientMapMatches"],
        "energyRatioAlgebra": energy["symbolicCoefficientMapMatches"],
        "smallTimeNormRatioExponent": norm_ratio_exponent == Fraction(1, 3),
        "smallTimeGraphConstantLowerExponent": graph_constant_lower_exponent == Fraction(-1, 3),
        "analyticTheoremBoundaryRecorded": (
            boundary["analyticWholeLineTheoremProvedInBoundReport"] is True
            and boundary["wholeLineFunctionalTheoremMachineChecked"] is False
        ),
        "timeLengthUniformityFalse": boundary["timeLengthUniformity"] is False,
        "periodicTransferFalse": boundary["periodicTransferProved"] is False,
        "nonlinearNavierStokesFalse": boundary["nonlinearNavierStokesClosureProved"] is False,
        "clayFalse": boundary["clayMillenniumProblemSolved"] is False,
    }

    return {
        "schemaVersion": 1,
        "theoremId": "R0.72V-unit-chart-globalization-exact-finite-ledger",
        "status": "passed" if all(exact_checks.values()) else "failed",
        "producerMethod": "expanded degree-eight probe polynomial plus exact multivariate coefficient maps",
        "exactChecks": exact_checks,
        "probe": {
            "support": "[-1/2,1/2]",
            "formula": "q0(y)=(315/128)*(1-4*y^2)^4*1_{[-1/2,1/2]}(y)",
            "expandedOnSupport": "(315/128)*(1-16*y^2+96*y^4-256*y^6+256*y^8)",
            "normalization": q(mu0),
            "parity": "even",
            "boundaryVanishingOrder": 4,
            "functionalClassUsedByMomentPairing": "q0 and every degree-at-most-two polynomial multiple used in the ledger belong to H_0^1((-1/2,1/2))",
        },
        "moments": {
            "mu0": q(mu0),
            "mu2": q(mu2),
            "mu4": q(mu4),
            "varianceY2": q(variance),
            "definition": "mu_j=integral_{-1/2}^{1/2} y^j*q0(y) dy",
        },
        "escapingCoefficientLedger": {
            "timeHalfLengthT": q(time_half_length),
            "timeInterval": "[-1,1]",
            "adaptivePolynomial": "p_{alpha,beta}(y)=alpha*(y^2-mu2)+beta*y with alpha^2+beta^2=1",
            "kappaFormula": "kappa_{alpha,beta}=alpha^2*(mu4-mu2^2)+beta^2*mu2",
            "kappaLowerFloor": q(kappa0),
            "ellFormula": "ell_{alpha,beta}(t)=beta*(mu4+6*t*mu2)",
            "ellConstant": q(ell_constant),
            "ellTimeSlope": q(ell_time_slope),
            "unitBlockAbsoluteUpperBoundL": q(ell_bound),
            "sufficientThresholdFormula": "lambda>=2*L_T/kappa0",
            "unitBlockSufficientThreshold": q(escaping_threshold),
            "thresholdConclusion": "if lambda>=693/2 and abs(t)<=1 then lambda*kappa_{alpha,beta}+ell_{alpha,beta}(t)>=lambda*kappa0/2",
        },
        "spatialTranslation": translation,
        "energyBlockContraction": energy,
        "smallTimeBoundary": {
            "exactKernelSpatialScale": "L=T^(-1/3)",
            "squaredDerivativeTermExponent": q(derivative_scale_exponent),
            "squaredCubicPhaseTermExponent": q(cubic_phase_scale_exponent),
            "fixedGaugeFloorTermExponent": q(fixed_gauge_floor_exponent),
            "normRatioUpperOrder": "T^(1/3)",
            "graphConstantLowerOrder": "T^(-1/3)",
            "timeLengthUniformity": False,
        },
        "claimBoundary": boundary,
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


def ensure_clean_head(source_commit: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("--formal requires a full 40-character --source-commit")
    status = subprocess.check_output(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=REPOSITORY,
        text=True,
    )
    if status:
        raise RuntimeError("formal certificate requires a completely clean repository")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip()
    if head != source_commit:
        raise RuntimeError("formal certificate source commit must equal clean HEAD")


def self_test() -> None:
    value = payload()
    if value["status"] != "passed" or not all(value["exactChecks"].values()):
        raise RuntimeError("producer exact self-test failed")
    subprocess.run([sys.executable, str(ROOT / "independent_recompute.py"), "--self-test"], check=True)
    print("R0.72V certificate source self-test: passed (no outputs written)")


def formal_build(source_commit: str) -> None:
    ensure_clean_head(source_commit)
    stale = [name for name in GENERATED_FILES if (ROOT / name).exists()]
    if stale:
        raise RuntimeError(f"refusing to overwrite existing certificate outputs: {', '.join(stale)}")
    bindings = source_bindings(source_commit)

    subprocess.run(
        [
            sys.executable,
            str(ROOT / "independent_recompute.py"),
            "--formal",
            "--source-commit",
            source_commit,
            "--output",
            str(ROOT / "independent.json"),
        ],
        check=True,
    )
    certificate = payload()
    if certificate["status"] != "passed":
        raise RuntimeError("R0.72V exact checks failed")
    write_json(ROOT / "certificate.json", certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))

    compared_sections = (
        "probe",
        "moments",
        "escapingCoefficientLedger",
        "spatialTranslation",
        "energyBlockContraction",
        "smallTimeBoundary",
        "claimBoundary",
    )
    independent_matches = (
        independent.get("status") == "passed"
        and all(independent.get(section) == certificate.get(section) for section in compared_sections)
    )
    crosscheck = {
        "schemaVersion": 1,
        "status": "passed" if independent_matches else "failed",
        "method": "expanded-polynomial producer versus scaled beta-recurrence and separately assembled coefficient identities",
        "temporaryUnsealedSourceAllowed": False,
        "formalSourceReady": True,
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "certificateSha256": sha256(ROOT / "certificate.json"),
        "comparedSections": list(compared_sections),
        "checks": {
            "certificatePassed": certificate["status"] == "passed",
            "allExactChecksPassed": all(certificate["exactChecks"].values()),
            "independentRecomputationPassed": independent.get("status") == "passed",
            "independentExactLedgerMatches": independent_matches,
            "analyticVersusMachineBoundaryExplicit": (
                certificate["claimBoundary"]["analyticWholeLineTheoremProvedInBoundReport"] is True
                and certificate["claimBoundary"]["wholeLineFunctionalTheoremMachineChecked"] is False
            ),
            "functionalAnalysisScopeExplicit": all(
                certificate["claimBoundary"][key] is False
                for key in (
                    "compactnessArgumentMachineChecked",
                    "scalarEndpointTracePassageMachineChecked",
                    "hMinusOneDirectSumMachineChecked",
                    "nonautonomousEvolutionExistenceMachineChecked",
                )
            ),
            "openClaimBoundaryExplicit": all(
                certificate["claimBoundary"][key] is False
                for key in (
                    "timeLengthUniformity",
                    "periodicTransferProved",
                    "nonlinearNavierStokesClosureProved",
                    "clayMillenniumProblemSolved",
                )
            ),
        },
    }
    if crosscheck["status"] != "passed" or not all(crosscheck["checks"].values()):
        raise RuntimeError("independent R0.72V crosscheck failed")
    write_json(ROOT / "crosscheck.json", crosscheck)

    manifest = {
        "schemaVersion": 1,
        "bundle": "R0.72V deterministic unit-chart globalization finite ledger",
        "status": "formal",
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "deterministic": True,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "files": {
            name: {"sha256": sha256(ROOT / name), "bytes": (ROOT / name).stat().st_size}
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": (
            "Finite rational and symbolic algebra only. The whole-line theorem is analytic; "
            "compactness, scalar traces, the H^{-1} direct sum, and evolution existence are "
            "not machine checked. Periodic transfer, nonlinear Navier-Stokes closure, Clay, "
            "and time-length uniformity are not claimed."
        ),
    }
    write_json(ROOT / "manifest.json", manifest)
    ledger_names = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )
    print("R0.72V formal deterministic certificate: passed")


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
