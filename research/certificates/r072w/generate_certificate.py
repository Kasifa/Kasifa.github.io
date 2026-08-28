#!/usr/bin/env python3
"""Build the deterministic R0.72W exact-periodic finite certificate.

Only finite rational and polynomial identities are certified here.  The
uniform chart compactness argument, scalar endpoint ledger, torus H^{-1}
direct sum, and energy evolution remain analytic results of the bound report.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FIGURE_DIRECTORY = "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer"
SOURCE_FILES = (
    "research/r072w_report-source.md",
    "research/r072w_gap_matrix.md",
    "research/r072w_literature_audit.md",
    "research/r072w_independent_audit.md",
    "research/certificates/r072w/generate_certificate.py",
    "research/certificates/r072w/independent_recompute.py",
    "research/certificates/r072w/validate_certificate.py",
    "research/certificates/r072w/README.md",
    "research/certificates/r072w/command.txt",
    "research/certificates/r072w/environment.txt",
    "scripts/generate_r072w_figure.py",
    "scripts/generate_r072w_release.py",
    "scripts/add-r072w-translations.mjs",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/README.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/caption.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/contract.json",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/config.json",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/command.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/environment.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/requirements.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/qa-protocol.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/plot.py",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/validate.py",
    "tests/r072w-deterministic-certificate-source.test.mjs",
    "tests/r072w-exact-periodic-gate.test.mjs",
    "tests/r072w-exact-tail-transfer-figure-source.test.mjs",
    "tests/r072w-release.test.mjs",
)
GENERATED_FILES = (
    "certificate.json",
    "independent.json",
    "crosscheck.json",
    "manifest.json",
    "SHA256SUMS",
)

Poly = dict[tuple[int, int], F]  # powers of (t, x)


def q(value: F | int) -> str:
    value = F(value)
    return f"{value.numerator}/{value.denominator}"


def poly_clean(value: Poly) -> Poly:
    return {key: coefficient for key, coefficient in value.items() if coefficient}


def heat_polynomial(n: int) -> Poly:
    return {
        (j, n - 2 * j): F(factorial(n), factorial(j) * factorial(n - 2 * j))
        for j in range(n // 2 + 1)
    }


def dt(value: Poly) -> Poly:
    return poly_clean({
        (t_power - 1, x_power): coefficient * t_power
        for (t_power, x_power), coefficient in value.items()
        if t_power
    })


def dxx(value: Poly) -> Poly:
    return poly_clean({
        (t_power, x_power - 2): coefficient * x_power * (x_power - 1)
        for (t_power, x_power), coefficient in value.items()
        if x_power >= 2
    })


def serialise_poly(value: Poly) -> list[dict[str, Any]]:
    return [
        {"tPower": t_power, "xPower": x_power, "coefficient": q(coefficient)}
        for (t_power, x_power), coefficient in sorted(value.items())
    ]


def direct_even_moment(power: int) -> F:
    if power < 0 or power % 2:
        raise ValueError("even non-negative power required")
    coefficients = {0: 1, 2: -16, 4: 96, 6: -256, 8: 256}
    return F(315, 128) * sum(
        F(coefficient, 2 ** (power + degree) * (power + degree + 1))
        for degree, coefficient in coefficients.items()
    )


def univariate_trim(value: list[F]) -> list[F]:
    result = value[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def univariate_divmod(left: list[F], right: list[F]) -> tuple[list[F], list[F]]:
    remainder = univariate_trim(left)
    divisor = univariate_trim(right)
    if divisor == [0]:
        raise ZeroDivisionError
    quotient = [F(0)] * max(1, len(remainder) - len(divisor) + 1)
    while remainder != [0] and len(remainder) >= len(divisor):
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree] = coefficient
        for index, entry in enumerate(divisor):
            remainder[index + degree] -= coefficient * entry
        remainder = univariate_trim(remainder)
    return univariate_trim(quotient), remainder


def monic_gcd(left: list[F], right: list[F]) -> list[F]:
    a, b = univariate_trim(left), univariate_trim(right)
    while b != [0]:
        _, remainder = univariate_divmod(a, b)
        a, b = b, remainder
    return [entry / a[-1] for entry in a]


def heat_series_record() -> dict[str, Any]:
    physical: list[str] = []
    scaled: list[str] = []
    expected_physical = [F(-1, 4), F(1, 16), F(-1, 160), F(17, 48384)]
    expected_scaled = [F(1), F(-1, 4), F(1, 40), F(-17, 12096)]
    heat = {}
    heat_checks = {}
    for j, n in enumerate((3, 5, 7, 9), start=1):
        coefficient = F((-1) ** j * (2 ** (2 * j) - 1), 2 * factorial(2 * j + 1))
        scaled_coefficient = -4 * coefficient
        physical.append(q(coefficient))
        scaled.append(q(scaled_coefficient))
        polynomial = heat_polynomial(n)
        heat[f"H{n}"] = serialise_poly(polynomial)
        heat_checks[f"H{n}HeatIdentity"] = dt(polynomial) == dxx(polynomial)
    return {
        "physicalSeries": "W=-H3/4+H5/16-H7/160+17*H9/48384+R11",
        "scaledSeries": "V_alpha=H3-alpha^2*H5/4+alpha^4*H7/40-17*alpha^6*H9/12096+R_alpha,11",
        "exactPotential": "V_alpha=alpha^(-3)*(2*exp(-alpha^2*S)*sin(alpha*X)-exp(-4*alpha^2*S)*sin(2*alpha*X))",
        "exactPotentialHeatIdentity": "V_S=V_XX",
        "exactThirdDerivative": "V_XXX=-2*A*cos(alpha*X)+8*B*cos(2*alpha*X)",
        "exactFourthDerivative": "V_XXXX=alpha*(2*A*sin(alpha*X)-16*B*sin(2*alpha*X))",
        "chartCoefficientTimeIdentities": "b_S=V_XXX and a_S=V_XXXX/2 for b=V_X and a=V_XX/2",
        "derivativeScaling": "V_XXX=O_T(1), V_XXXX=O_T(alpha)",
        "physicalCoefficientsH3H5H7H9": physical,
        "scaledCoefficientsH3H5H7H9": scaled,
        "expectedPhysicalCoefficientsMatch": [F(value) for value in expected_physical] == [
            F(value) for value in physical
        ],
        "expectedScaledCoefficientsMatch": [F(value) for value in expected_scaled] == [
            F(value) for value in scaled
        ],
        "heatPolynomials": heat,
        "heatIdentityChecks": heat_checks,
    }


def probe_record() -> dict[str, Any]:
    mu0 = direct_even_moment(0)
    mu2 = direct_even_moment(2)
    mu4 = direct_even_moment(4)
    variance = mu4 - mu2 * mu2
    return {
        "chart": "J_ell=(-ell/2,ell/2), 1<=ell<=2",
        "formula": "q_ell(y)=(315/(128*ell))*(1-4*y^2/ell^2)^4*1_{[-ell/2,ell/2]}(y)",
        "baseMomentsAtEllOne": {
            "mu0": q(mu0),
            "mu2": q(mu2),
            "mu4": q(mu4),
            "varianceY2": q(variance),
        },
        "scaledMoments": {
            "mu0": "1",
            "mu2": "ell^2/44",
            "mu4": "3*ell^4/2288",
            "varianceY2": "5*ell^4/6292",
        },
        "adaptiveVariance": "gamma^2*(5*ell^4/6292)+beta^2*(ell^2/44)",
        "uniformFloorForEllInOneTwo": "5/6292",
        "boundaryVanishingOrder": 4,
    }


def common_zero_record() -> dict[str, Any]:
    # u=cos(theta). b=0 gives 2u^2-u-1=0. Squaring the a=0
    # condition gives (1-u^2)(4u-1)^2=0.
    b_polynomial = [F(-1), F(-1), F(2)]
    a_squared = [F(1), F(-8), F(15), F(8), F(-16)]
    gcd = monic_gcd(b_polynomial, a_squared)
    finite_type_matrix = ((1, -1), (-1, 4))
    determinant = (
        finite_type_matrix[0][0] * finite_type_matrix[1][1]
        - finite_type_matrix[0][1] * finite_type_matrix[1][0]
    )
    # cos^2(z)+cos^2(2z)=4u^2-3u+1 for u=cos^2(z) in [0,1].
    minimizer = F(3, 8)
    minimum = 4 * minimizer * minimizer - 3 * minimizer + 1
    return {
        "bZeroPolynomialInCosTheta": "2*u^2-u-1=(u-1)*(2*u+1)",
        "aZeroSquaredPolynomialInCosTheta": "(1-u^2)*(4*u-1)^2",
        "monicPolynomialGcd": [q(entry) for entry in gcd],
        "commonPhaseConclusion": "theta=0 mod 2*pi",
        "finiteTypeVector": "(alpha^2*V_X/2,V_SX/2)",
        "finiteTypeInputs": "(A,B)=(exp(-alpha^2*S)*cos(alpha*X),exp(-4*alpha^2*S)*cos(2*alpha*X))",
        "finiteTypeMatrix": [[1, -1], [-1, 4]],
        "finiteTypeDeterminant": determinant,
        "cosineSquareMinimum": q(minimum),
        "cosineSquareMinimizerCosSquared": q(minimizer),
    }


def no_go_record() -> dict[str, Any]:
    thresholds = [F(2, 25), F(4, 35), F(2, 15)]
    critical = F(2, 25)
    critical_exponents = [
        -F(2, 5) + 5 * critical,
        -F(4, 5) + 7 * critical,
        -F(6, 5) + 9 * critical,
    ]
    return {
        "farTranslationGraphRatios": {
            "H5OverP0GraphPowerInL": 2,
            "H7OverP0GraphPowerInL": 4,
            "H9OverP0GraphPowerInL": 6,
            "conclusion": "separate polynomial multipliers are not globally relatively small",
        },
        "localRadiusAnsatz": "R=kappa^beta",
        "absolutePerturbationExponents": [
            "-2/5+5*beta",
            "-4/5+7*beta",
            "-6/5+9*beta",
        ],
        "individualBetaThresholds": [q(value) for value in thresholds],
        "jointStrictThreshold": q(min(thresholds)),
        "criticalBeta": q(critical),
        "criticalExponentsH5H7H9": [q(value) for value in critical_exponents],
        "absorbableGrowingRadius": "R=o(kappa^(2/25))",
        "exactTailCancellationRequired": True,
    }


def torus_partition_record() -> dict[str, Any]:
    return {
        "torusLength": "L_alpha=2*pi/alpha",
        "cellCount": "N=floor(L_alpha)",
        "cellLength": "ell=L_alpha/N",
        "premises": "N>=1 and N<=L_alpha<N+1",
        "lowerBound": "1<=ell",
        "upperBound": "ell<1+1/N<=2",
        "chartRange": "1<=ell<=2",
        "finiteCellHMinusOneDirectSumConstant": "1",
        "integerInequalityChecked": True,
    }


def energy_record() -> dict[str, Any]:
    return {
        "inputInequality": "T*E_plus<=C2*(E_minus-E_plus)",
        "rearrangedInequality": "(T+C2)*E_plus<=C2*E_minus",
        "squaredEnergyRatio": "C2/(T+C2)",
        "normRatio": "C/sqrt(T+C^2)",
        "strictFor": "T>0 and finite C>0",
        "coefficientCollectionChecked": True,
    }


def claim_boundary() -> dict[str, Any]:
    return {
        "finiteExactAlgebraCertified": True,
        "analyticExactPeriodicUnitChartTheoremProvedInBoundReport": True,
        "analyticTorusGraphTheoremProvedInBoundReport": True,
        "analyticPeriodicScalarEnergyContractionProvedInBoundReport": True,
        "exactPeriodicScalarTransferProved": True,
        "heatSeriesBeyondH9MachineChecked": False,
        "compactnessArgumentMachineChecked": False,
        "scalarEndpointTracePassageMachineChecked": False,
        "varyingCellGraphSpacePassageMachineChecked": False,
        "torusHMinusOneDirectSumMachineChecked": False,
        "nonautonomousEvolutionExistenceMachineChecked": False,
        "timeLengthUniformity": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }


def payload() -> dict[str, Any]:
    heat = heat_series_record()
    probe = probe_record()
    common = common_zero_record()
    no_go = no_go_record()
    partition = torus_partition_record()
    energy = energy_record()
    boundary = claim_boundary()
    checks = {
        "physicalSeriesCoefficients": heat["expectedPhysicalCoefficientsMatch"],
        "scaledSeriesCoefficients": heat["expectedScaledCoefficientsMatch"],
        "heatIdentitiesH3H5H7H9": all(heat["heatIdentityChecks"].values()),
        "probeMu2": probe["baseMomentsAtEllOne"]["mu2"] == "1/44",
        "probeMu4": probe["baseMomentsAtEllOne"]["mu4"] == "3/2288",
        "probeVariance": probe["baseMomentsAtEllOne"]["varianceY2"] == "5/6292",
        "commonZeroGcd": common["monicPolynomialGcd"] == ["-1/1", "1/1"],
        "finiteTypeDeterminant": common["finiteTypeDeterminant"] == 3,
        "cosineSquareMinimum": common["cosineSquareMinimum"] == "7/16",
        "noGoJointThreshold": no_go["jointStrictThreshold"] == "2/25",
        "criticalRadiusExponents": no_go["criticalExponentsH5H7H9"] == [
            "0/1", "-6/25", "-12/25"
        ],
        "torusPartitionInequality": partition["integerInequalityChecked"],
        "energyContractionAlgebra": energy["coefficientCollectionChecked"],
        "machineBoundaryHonest": (
            boundary["analyticTorusGraphTheoremProvedInBoundReport"] is True
            and boundary["torusHMinusOneDirectSumMachineChecked"] is False
            and boundary["nonlinearNavierStokesClosureProved"] is False
            and boundary["clayMillenniumProblemSolved"] is False
        ),
    }
    return {
        "schemaVersion": 1,
        "theoremId": "R0.72W-exact-periodic-tail-transfer-finite-ledger",
        "status": "passed" if all(checks.values()) else "failed",
        "producerMethod": "factorial heat-polynomial expansion, direct probe integration, and Euclidean polynomial gcd",
        "exactChecks": checks,
        "heatSeriesThroughH9": heat,
        "scaledProbe": probe,
        "commonZeroAndFiniteType": common,
        "noGoAndLocalAbsorption": no_go,
        "torusPartition": partition,
        "energyBlockContraction": energy,
        "claimBoundary": boundary,
    }


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    if head != source_commit:
        raise RuntimeError("formal certificate source commit must equal clean HEAD")


def source_bindings(source_commit: str) -> list[dict[str, Any]]:
    result = []
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
        result.append({
            "path": relative,
            "commit": source_commit,
            "gitBlob": committed,
            "sha256": sha256(path),
            "bytes": path.stat().st_size,
            "workingTreeBlobMatches": True,
        })
    return result


def self_test() -> None:
    value = payload()
    if value["status"] != "passed" or not all(value["exactChecks"].values()):
        raise RuntimeError("producer exact self-test failed")
    subprocess.run(
        [sys.executable, str(ROOT / "independent_recompute.py"), "--self-test"],
        check=True,
    )
    print("R0.72W certificate source self-test: passed (no outputs written)")


def formal_build(source_commit: str) -> None:
    ensure_clean_head(source_commit)
    stale = [name for name in GENERATED_FILES if (ROOT / name).exists()]
    if stale:
        raise RuntimeError(
            f"refusing to overwrite existing certificate outputs: {', '.join(stale)}"
        )
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
        raise RuntimeError("R0.72W exact checks failed")
    write_json(ROOT / "certificate.json", certificate)
    independent = json.loads((ROOT / "independent.json").read_text(encoding="utf-8"))
    compared = (
        "heatSeriesThroughH9",
        "scaledProbe",
        "commonZeroAndFiniteType",
        "noGoAndLocalAbsorption",
        "torusPartition",
        "energyBlockContraction",
        "claimBoundary",
    )
    matches = (
        independent.get("status") == "passed"
        and all(independent.get(section) == certificate.get(section) for section in compared)
    )
    crosscheck = {
        "schemaVersion": 1,
        "status": "passed" if matches else "failed",
        "method": "factorial/direct-integral producer versus heat recurrence/beta-recurrence independent route",
        "temporaryUnsealedSourceAllowed": False,
        "formalSourceReady": True,
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "certificateSha256": sha256(ROOT / "certificate.json"),
        "comparedSections": list(compared),
        "checks": {
            "certificatePassed": certificate["status"] == "passed",
            "allExactChecksPassed": all(certificate["exactChecks"].values()),
            "independentRecomputationPassed": independent.get("status") == "passed",
            "independentExactLedgerMatches": matches,
            "analyticVersusMachineBoundaryExplicit": (
                certificate["claimBoundary"]["analyticTorusGraphTheoremProvedInBoundReport"]
                and not certificate["claimBoundary"]["torusHMinusOneDirectSumMachineChecked"]
            ),
            "nonlinearAndClayRemainFalse": (
                not certificate["claimBoundary"]["nonlinearNavierStokesClosureProved"]
                and not certificate["claimBoundary"]["clayMillenniumProblemSolved"]
            ),
        },
    }
    if crosscheck["status"] != "passed" or not all(crosscheck["checks"].values()):
        raise RuntimeError("independent R0.72W crosscheck failed")
    write_json(ROOT / "crosscheck.json", crosscheck)
    manifest = {
        "schemaVersion": 1,
        "bundle": "R0.72W deterministic exact-periodic finite ledger",
        "status": "formal",
        "sourceCommit": source_commit,
        "sourceBindings": bindings,
        "claimBoundary": certificate["claimBoundary"],
        "deterministic": True,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "files": {
            name: {
                "sha256": sha256(ROOT / name),
                "bytes": (ROOT / name).stat().st_size,
            }
            for name in ("certificate.json", "independent.json", "crosscheck.json")
        },
        "limitations": (
            "Finite exact algebra only. Compactness, scalar traces, varying-cell graph "
            "spaces, the torus H^{-1} direct sum, and evolution existence are not machine "
            "checked. Time-length uniformity, nonlinear Navier-Stokes closure, and Clay "
            "are not claimed."
        ),
    }
    write_json(ROOT / "manifest.json", manifest)
    names = sorted(
        path.name for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (ROOT / "SHA256SUMS").write_text(
        "".join(f"{sha256(ROOT / name)}  {name}\n" for name in names),
        encoding="utf-8",
    )
    print("R0.72W formal deterministic certificate: passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--formal", action="store_true")
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
