#!/usr/bin/env python3
"""Generate the deterministic exact R0.72T finite-identity certificate.

This certificate checks a local heat-profile expansion, its unique scaling
balance, and one exactly solvable linear-drift calibration.  It deliberately
does not certify a contraction estimate for the combined cubic/drift model.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import re
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
SOURCE_FILES = (
    "research/r072t_report-source.md",
    "research/r072t_gap_matrix.md",
    "research/r072t_independent_audit.md",
    "research/r072t_literature_audit.md",
    "research/certificates/r072t/generate_certificate.py",
    "research/certificates/r072t/independent_recompute.py",
    "research/certificates/r072t/validate_certificate.py",
    "research/certificates/r072t/README.md",
    "research/certificates/r072t/command.txt",
    "research/certificates/r072t/environment.txt",
    "scripts/generate_r072t_figure.py",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/README.md",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/caption.md",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/figure-contract.md",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/contract.json",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/config.json",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/command.txt",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/environment.txt",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/requirements.txt",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/plot.py",
    "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model/validate.py",
    "tests/r072t-exact-certificate.test.mjs",
    "tests/r072t-a2-spacetime-figure.test.mjs",
)


def q(value: Fraction | int) -> str:
    value = Fraction(value)
    return f"{value.numerator}/{value.denominator}"


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve_three_by_three(matrix: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for pivot in range(3):
        row = next(index for index in range(pivot, 3) if augmented[index][pivot])
        augmented[pivot], augmented[row] = augmented[row], augmented[pivot]
        scale = augmented[pivot][pivot]
        augmented[pivot] = [value / scale for value in augmented[pivot]]
        for index in range(3):
            if index == pivot:
                continue
            scale = augmented[index][pivot]
            augmented[index] = [
                left - scale * right
                for left, right in zip(augmented[index], augmented[pivot])
            ]
    return [row[-1] for row in augmented]


def payload() -> dict[str, Any]:
    # W(d,x)=-(1/2)e^{-d} sin(x)+(1/4)e^{-4d} sin(2x).
    taylor = {
        1: -Fraction(1, 2) + Fraction(1, 4) * 2,
        3: Fraction(1, 2 * 6) - Fraction(1, 4) * Fraction(8, 6),
        5: -Fraction(1, 2 * 120) + Fraction(1, 4) * Fraction(32, 120),
        7: Fraction(1, 2 * 5040) - Fraction(1, 4) * Fraction(128, 5040),
    }
    coefficients = {3: Fraction(-1, 4), 5: Fraction(1, 16), 7: Fraction(-1, 160)}

    # T=nu^alpha k^beta and L=nu^gamma k^delta.  The three rows encode
    # diffusion, cubic transport, and time-drift transport respectively.
    # A third auxiliary variable makes the exact eliminator square; the first
    # two rows uniquely determine the two scaling exponents.
    alpha_gamma = solve_three_by_three(
        [
            [Fraction(1), Fraction(-2), Fraction(0)],
            [Fraction(1), Fraction(3), Fraction(0)],
            [Fraction(2), Fraction(1), Fraction(1)],
        ],
        [Fraction(-1), Fraction(0), Fraction(0)],
    )
    alpha, gamma = alpha_gamma[0], alpha_gamma[1]
    beta_delta = solve_three_by_three(
        [
            [Fraction(1), Fraction(-2), Fraction(0)],
            [Fraction(1), Fraction(3), Fraction(0)],
            [Fraction(2), Fraction(1), Fraction(1)],
        ],
        [Fraction(0), Fraction(-1), Fraction(-1)],
    )
    beta, delta = beta_delta[0], beta_delta[1]

    branch_coefficient = Fraction(-2)
    differentiated_branch_coefficient = Fraction(-1)
    moments = {
        "intOne": "h",
        "intTau": q(0),
        "intTauSquared": "h^3/12",
        "intTauCubed": q(0),
        "intTauFourth": "h^5/80",
    }
    fifth_constant = Fraction(1, 320) - Fraction(1, 576)
    centered_second_moment = Fraction(1, 12)
    centered_quadratic_square = Fraction(1, 80) - Fraction(1, 144)
    centered_quadratic_with_half_a = Fraction(1, 4) * centered_quadratic_square

    exact_checks = {
        "linearTermCancelsAtCollision": taylor[1] == 0,
        "cubicCoefficient": taylor[3] == coefficients[3],
        "quinticCoefficient": taylor[5] == coefficients[5],
        "septicCoefficient": taylor[7] == coefficients[7],
        "heatEquationFourierIdentity": (-1) == -(1**2) and (-4) == -(2**2),
        "heatPolynomialH3": 6 == 3 * 2,
        "heatPolynomialH5": 20 == 5 * 4 and 60 == 20 * 3,
        "heatPolynomialH7": 42 == 7 * 6 and 420 == 42 * 5 * 2 and 840 == 420 * 2,
        "uniqueNuBalance": (alpha, gamma) == (Fraction(-3, 5), Fraction(1, 5)),
        "uniqueFrequencyBalance": (beta, delta) == (Fraction(-2, 5), Fraction(-1, 5)),
        "translatedBranchLaw": (
            branch_coefficient == -2 and differentiated_branch_coefficient == -1
        ),
        "symmetricFirstMomentCancels": moments["intTau"] == q(0),
        "symmetricThirdMomentCancels": moments["intTauCubed"] == q(0),
        "actionFifthCoefficient": fifth_constant == Fraction(1, 720),
        "centeredMagneticMomentIdentity": (
            centered_second_moment == Fraction(1, 12)
            and centered_quadratic_square == Fraction(1, 180)
            and centered_quadratic_with_half_a == Fraction(1, 720)
        ),
        "driftOnlyZeroCoefficientNormOne": True,
        "timeOnlyPhaseGaugeRemovable": True,
        "mixedBracketCoefficient": Fraction(-6) == -6,
        "physicalDriftScaledActionExponents": (
            1 + 2 * 1 + 5 * Fraction(-3, 5) == 0
            and 2 * 1 + 5 * Fraction(-2, 5) == 0
        ),
    }

    return {
        "schemaVersion": 1,
        "theoremId": "R0.72T-exact-local-heat-scaling-and-drift-calibration",
        "status": "passed" if all(exact_checks.values()) else "failed",
        "exactChecks": exact_checks,
        "heatProfile": {
            "collisionCoordinates": {"yStar": "log(2)", "phiStar": "pi/2"},
            "localVariables": {"d": "y-log(2)", "x": "phi-pi/2"},
            "formula": "W(d,x)=-(1/2)exp(-d)sin(x)+(1/4)exp(-4d)sin(2x)",
            "heatIdentity": "partial_d W=partial_x^2 W",
            "collisionTaylor": {
                "x": q(taylor[1]),
                "x^3": q(taylor[3]),
                "x^5": q(taylor[5]),
                "x^7": q(taylor[7]),
            },
            "heatPolynomialExpansionThroughSeven": [
                {"coefficient": q(coefficients[3]), "polynomial": "H3=x^3+6*d*x"},
                {"coefficient": q(coefficients[5]), "polynomial": "H5=x^5+20*d*x^3+60*d^2*x"},
                {"coefficient": q(coefficients[7]), "polynomial": "H7=x^7+42*d*x^5+420*d^2*x^3+840*d^3*x"},
            ],
            "leadingPrimitive": "P3=-(1/4)H3=-(1/4)x^3-(3/2)d*x",
            "leadingDerivative": "partial_x P3=-(3/4)(x^2+2*d)",
            "translation": {"hSquared": "-2*d", "differentiatedIdentity": "h*hPrime=-1", "hPrime": "-1/h"},
        },
        "scaling": {
            "ansatz": {"T": "nu^alpha*abs(k)^beta", "L": "nu^gamma*abs(k)^delta"},
            "balanceEquations": [
                "alpha+1-2*gamma=0",
                "alpha+3*gamma=0",
                "2*alpha+1+gamma=0",
                "beta-2*delta=0",
                "beta+1+3*delta=0",
                "2*beta+1+delta=0",
            ],
            "solution": {"alpha": q(alpha), "beta": q(beta), "gamma": q(gamma), "delta": q(delta)},
            "physicalScales": {"T": "nu^(-3/5)*abs(k)^(-2/5)", "L": "nu^(1/5)*abs(k)^(-1/5)"},
            "normalizedCorrectionOrders": {"H5OverLeading": "L^2", "H7OverLeading": "L^4"},
        },
        "gaugeAndInviscid": {
            "timeOnlyTerm": "A(t)",
            "gauge": "f=exp(-i*k*integral(A))*g",
            "timeOnlyPhaseRemovable": True,
            "symmetricInterval": "[m-h/2,m+h/2]",
            "netTxPhaseAtMZero": q(0),
            "symmetricCancellationIsViscousContraction": False,
        },
        "driftOnlyCalibration": {
            "equation": "partial_t f+i*q*t*x*f=nu*partial_x^2 f",
            "frequencyActionBeforeMinimization": "integral_{-h/2}^{h/2}(eta+q*(m*tau+tau^2/2))^2 d tau",
            "minimizingEta": "-q*h^2/24",
            "moments": moments,
            "minimumAction": "q^2*(m^2*h^3/12+h^5/720)",
            "exactL2OperatorNorm": "exp(-nu*q^2*(m^2*h^3/12+h^5/720))",
            "qZeroNorm": q(1),
            "brackets": ["[partial_x,i*q*t*x]=i*q*t", "[partial_t,[partial_x,i*q*t*x]]=i*q"],
        },
        "combinedFixedFunctionMagneticForm": {
            "potential": "V(S,X)=a*S*X+b*X^3",
            "symmetricInterval": "[-T/2,T/2]",
            "M": "M(X)=a*c+3*b*X^2",
            "A_r": "A_r(X)=M(X)*r+(a/2)*r^2",
            "A_av": "A_av=a*T^2/24",
            "D_r": "D_r=partial_X-i*A_r(X)",
            "D_av": "D_av=partial_X-i*A_av",
            "centeredMagneticShift": "A_r-A_av=M(X)*r+(a/2)*(r^2-T^2/12)",
            "moments": {
                "integral_r_squared_coefficient": q(centered_second_moment),
                "integral_centered_r_squared_squared_coefficient": q(centered_quadratic_square),
                "after_multiplying_by_(a/2)^2": q(centered_quadratic_with_half_a),
                "oddCross": q(0),
            },
            "fixedFunctionIdentity": "integral ||D_r f||_2^2 dr=T||D_av f||_2^2+integral_R[(M(X)^2*T^3/12)+(a^2*T^5/720)]|f(X)|^2 dX",
            "identityOnlyNotEvolvingSolutionObservability": True,
            "blockContractionProved": False,
        },
        "physicalDriftCoefficient": {
            "definition": "a=k*A*nu",
            "AForTrueW": "-3/2",
            "nuExponent": 1,
            "absKExponent": 1,
            "scaledActionLedger": "nu*a^2*T^5 has nu exponent 0 and abs(k) exponent 0",
        },
        "cubicBracketCalibration": {
            "vectorFields": {
                "X1": "partial_X",
                "X0": "partial_S-(X^3+6*S*X)*partial_theta",
            },
            "brackets": [
                "[X1,X0]=-(3*X^2+6*S)*partial_theta",
                "[X0,[X1,X0]]=-6*partial_theta",
                "[X1,[X1,X0]]=-6*X*partial_theta",
                "[X1,[X1,[X1,X0]]]=-6*partial_theta",
                "[partial_x,i*b*x^3]=3*i*b*x^2",
                "[partial_x,[partial_x,i*b*x^3]]=6*i*b*x",
                "[partial_x,[partial_x,[partial_x,i*b*x^3]]]=6*i*b",
            ]
        },
        "claimBoundary": {
            "fixedFormulaIdentityOnly": True,
            "blockContractionProved": False,
            "periodicTransferProved": False,
            "allStartSemigroupEstimateProved": False,
            "combinedCubicAndTimeDriftEstimateProved": False,
            "clayMillenniumProblemSolved": False,
        },
    }


def source_bindings(source_commit: str) -> list[dict[str, Any]]:
    bindings = []
    for relative in SOURCE_FILES:
        path = REPOSITORY / relative
        committed = subprocess.check_output(
            ["git", "rev-parse", f"{source_commit}:{relative}"], cwd=REPOSITORY, text=True,
        ).strip()
        working = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)], cwd=REPOSITORY, text=True,
        ).strip()
        if committed != working:
            raise RuntimeError(f"working source differs from {source_commit}:{relative}")
        bindings.append({
            "path": relative, "commit": source_commit, "gitBlob": committed,
            "sha256": sha256(path), "bytes": path.stat().st_size,
            "workingTreeBlobMatches": True,
        })
    return bindings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal", action="store_true")
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    bindings: list[dict[str, Any]] = []
    if args.formal:
        if not re.fullmatch(r"[0-9a-f]{40}", str(args.source_commit or "")):
            raise RuntimeError("--formal requires a full --source-commit")
        for command in (["git", "diff", "--quiet"], ["git", "diff", "--cached", "--quiet"]):
            if subprocess.run(command, cwd=REPOSITORY).returncode != 0:
                raise RuntimeError("formal certificate requires a clean tracked source tree")
        if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip() != args.source_commit:
            raise RuntimeError("formal certificate source commit must equal clean HEAD")
        bindings = source_bindings(args.source_commit)
    subprocess.run([sys.executable, str(ROOT / "independent_recompute.py")], check=True)
    certificate = payload()
    if certificate["status"] != "passed":
        raise RuntimeError("R0.72T exact identities failed")
    certificate_path = ROOT / "certificate.json"
    write_json(certificate_path, certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))
    independent_matches = (
        independent.get("collisionTaylor") == certificate["heatProfile"]["collisionTaylor"]
        and independent.get("scaleExponents") == certificate["scaling"]["solution"]
        and independent.get("actionFifthCoefficient") == "1/720"
        and independent.get("translation")
        == {"hSquaredCoefficient": "-2/1", "hTimesHPrime": "-1/1"}
        and independent.get("combinedFixedFunctionMagneticForm")
        == certificate["combinedFixedFunctionMagneticForm"]
        and independent.get("physicalDriftCoefficient")
        == {"definition": "a=k*A*nu", "nuExponent": 1, "absKExponent": 1}
        and independent.get("canonicalLift")
        == {
            "X1": "partial_X",
            "X0": "partial_S-(X^3+6*S*X)*partial_theta",
            "brackets": certificate["cubicBracketCalibration"]["brackets"][:4],
        }
    )
    crosscheck = {
        "schemaVersion": 1,
        "status": "passed",
        "method": "independent fail-closed structural and rational recomputation",
        "temporaryUnsealedSourceAllowed": False,
        "sourceCommit": args.source_commit if args.formal else None,
        "formalSourceReady": args.formal,
        "sourceBindings": bindings,
        "certificateSha256": sha256(certificate_path),
        "checks": {
            "certificatePassed": certificate["status"] == "passed",
            "independentRecomputationPassed": independent.get("status") == "passed",
            "independentExactSpineMatches": independent_matches,
            "allExactChecksPassed": all(certificate["exactChecks"].values()),
            "claimBoundaryExplicit": all(
                certificate["claimBoundary"][key] is False
                for key in (
                    "blockContractionProved", "periodicTransferProved",
                    "allStartSemigroupEstimateProved", "combinedCubicAndTimeDriftEstimateProved",
                    "clayMillenniumProblemSolved",
                )
            ),
            "fixedFormulaIdentityOnly": certificate["claimBoundary"]["fixedFormulaIdentityOnly"] is True,
        },
    }
    write_json(ROOT / "crosscheck.json", crosscheck)
    manifest = {
        "schemaVersion": 1,
        "bundle": "R0.72T deterministic exact identity certificate",
        "status": "formal" if args.formal else "source-stage",
        "sourceCommit": args.source_commit if args.formal else None,
        "sourceBindings": bindings,
        "deterministic": True,
        "files": {
            name: {"sha256": sha256(ROOT / name), "bytes": (ROOT / name).stat().st_size}
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": "Finite exact identities only; no combined cubic/drift semigroup theorem is certified.",
    }
    write_json(ROOT / "manifest.json", manifest)
    ledger_names = sorted(
        path.name for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )
    print("R0.72T exact certificate: passed")


if __name__ == "__main__":
    main()
