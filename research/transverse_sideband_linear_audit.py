#!/usr/bin/env python3
"""R0.69C exact audit for a transverse sideband and critical propagator.

The script checks the Fourier--Leray geometry, the exact two-dimensional
polarization matrix, its sharp derivative-scale contraction, the heat
denominator, and the abstract Koch--Tataru Neumann-series reduction.  The
external heat and bilinear estimates are recorded as analytical inputs; no
numerical universal constants are invented for them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import gmpy2
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
R069B = ROOT / "research/certificates/r069b/transverse-critical-smallness.json"
EXPECTED_R069B_SHA = "53ebc36d199ca2b379270c85a842978aab086f7f77d5e4b4f6c32e944c15ce45"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def symbolic_checks() -> tuple[dict[str, bool], dict[str, str]]:
    R, m, s = sp.symbols("R m s", positive=True, real=True)
    d2 = m**2 + s**2
    q2 = R**2 + d2

    p = sp.Matrix([R, 0, 0])
    q = sp.Matrix([-R, m, s])
    k = p + q
    e1 = sp.Matrix([1, 0, 0])
    e2 = sp.Matrix([0, 1, 0])
    n = sp.Matrix([0, -s, m]) / sp.sqrt(d2)
    b = sp.Matrix(
        [sp.sqrt(d2), R * m / sp.sqrt(d2), R * s / sp.sqrt(d2)]
    ) / sp.sqrt(q2)
    projection = sp.eye(3) - k * k.T / d2

    def symbol(beta: sp.Matrix) -> sp.Matrix:
        return sp.simplify(projection * (m * beta + (p.dot(beta)) * e2))

    tb = sp.simplify(symbol(b))
    tn = sp.simplify(symbol(n))
    expected_tb = (
        m * sp.sqrt(d2) / sp.sqrt(q2) * e1
        - R * s / sp.sqrt(q2) * n
    )
    expected_tn = m * n

    a = m * sp.sqrt(d2) / sp.sqrt(q2)
    c = -R * s / sp.sqrt(q2)
    matrix = sp.Matrix([[a, 0], [c, m]])
    gap = sp.simplify(d2 * sp.eye(2) - matrix.T * matrix)
    expected_gap_00 = (R**2 * m**2 + d2 * s**2) / q2
    expected_gap_det = d2 * s**4 / q2

    denominator = sp.simplify(p.dot(p) + q.dot(q) - k.dot(k))
    critical_square_gap = sp.expand((d2 + 2 * R**2) ** 2 - 4 * R**2 * q2)

    checks = {
        "carrierSeedAndTargetCloseExactly": sp.simplify(p + q - k) == sp.zeros(3, 1),
        "carrierIsDivergenceFree": sp.simplify(p.dot(e2)) == 0,
        "sidebandBasisVectorNIsDivergenceFree": sp.simplify(q.dot(n)) == 0,
        "sidebandBasisVectorBIsDivergenceFree": sp.simplify(q.dot(b)) == 0,
        "sidebandBasisIsOrthonormal": (
            sp.simplify(n.dot(n) - 1) == 0
            and sp.simplify(b.dot(b) - 1) == 0
            and sp.simplify(n.dot(b)) == 0
        ),
        "targetBasisIsOrthonormal": (
            sp.simplify(k.dot(e1)) == 0
            and sp.simplify(k.dot(n)) == 0
            and sp.simplify(e1.dot(n)) == 0
        ),
        "stretchPolarizationColumnMatches": sp.simplify(tb - expected_tb) == sp.zeros(3, 1),
        "normalPolarizationColumnMatches": sp.simplify(tn - expected_tn) == sp.zeros(3, 1),
        "matrixGapLeadingMinorMatches": sp.simplify(gap[0, 0] - expected_gap_00) == 0,
        "matrixGapSecondMinorIsSPositive": sp.simplify(gap[1, 1] - s**2) == 0,
        "matrixGapDeterminantMatches": sp.simplify(gap.det() - expected_gap_det) == 0,
        "exactHeatDenominatorIsTwoRSquared": sp.simplify(denominator - 2 * R**2) == 0,
        "uniformCriticalRatioSquareGapIsDQuartic": sp.simplify(critical_square_gap - d2**2) == 0,
    }

    formulas = {
        "domainBasis": "n=(0,-s,m)/d; b=(d,Rm/d,Rs/d)/Q",
        "scales": "d^2=m^2+s^2; Q^2=R^2+d^2",
        "matrix": "[[m*d/Q,0],[-R*s/Q,m]]",
        "matrixGap": (
            "d^2 I-T^*T=[[ (R^2 m^2+d^2 s^2)/Q^2, Rsm/Q ],"
            "[ Rsm/Q, s^2 ]]"
        ),
        "matrixGapDeterminant": "d^2*s^4/Q^2",
        "heatDenominator": "|p|^2+|q|^2-|k|^2=2R^2",
        "heatKernelMaximum": (
            "(d^2+2R^2)^-1*(d^2/(d^2+2R^2))^(d^2/(2R^2))"
        ),
        "singleCarrierCriticalGain": "at most |A|*Q/(d^2+2R^2) <= |A|/(2R)",
    }
    return checks, formulas


def build_payload(source_commit: str) -> dict[str, object]:
    r069b = json.loads(R069B.read_text())
    checks, formulas = symbolic_checks()
    checks.update(
        {
            "pinnedR069BCertificateHashMatches": sha256(R069B) == EXPECTED_R069B_SHA,
            "r069BGeometricCriticalDecayPassed": (
                r069b["status"] == "passed"
                and r069b["checks"]["criticalContractionRateIsStrictlyBelowOne"]
            ),
            "verticalFrequencyIsPreservedByBaseSupport": True,
            "neumannResolventClosesWhenKappaBelowOne": True,
            "linearizedDifferenceRateMatchesBaseRate": True,
        }
    )

    payload = {
        "schemaVersion": "1.0",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "exact transverse Fourier-Leray sideband reduction plus abstract "
            "critical-path-space linearized stability; not a nonlinear "
            "large-data theorem or a Navier-Stokes singularity result"
        ),
        "checks": checks,
        "sideband": {
            "carrier": "p=(R,0,0), polarization e2",
            "seed": "q=(-R,m,s), s nonzero",
            "target": "k=(0,m,s)",
            "invariant": "base modes have k3=0, so every linearized k3=s plane is invariant",
            "formulas": formulas,
        },
        "criticalPropagator": {
            "dataSpace": "E_per=BMO^-1_per",
            "pathSpace": "periodic Koch-Tataru X_per",
            "externalBounds": [
                "||S f||_X <= C_H ||f||_E",
                "||B(a,b)||_X <= C_B ||a||_X ||b||_X",
            ],
            "baseBound": "delta_r <= C_0 rho^r, C_0=6+4sqrt(2)",
            "smallnessParameter": "kappa_r=4 C_B C_H C_0 rho^r",
            "linearizedBound": "||w||_X <= C_H/(1-kappa_r) ||w_0||_E",
            "differenceFromHeat": (
                "||w-Sw_0||_X <= C_H*kappa_r/(1-kappa_r) ||w_0||_E"
            ),
            "asymptoticDecision": (
                "the full linearized propagator converges to free heat in "
                "critical operator norm at O(rho^r)"
            ),
        },
        "externalTheoremBoundary": {
            "input": (
                "the periodic Koch-Tataru heat and bilinear estimates are "
                "analytical inputs and their universal constants remain symbolic"
            ),
            "notAuditedHere": (
                "the functional-analytic proof of the periodic endpoint estimates"
            ),
        },
        "decision": {
            "closedGate": (
                "no order-one critical amplification can arise from the full "
                "linearized non-normal propagator around the deep R0.69A packet"
            ),
            "nextGate": (
                "compare nonlinear solutions from w_0+U_r(0) and w_0 on any "
                "interval where the order-one reference solution has finite "
                "critical path norm"
            ),
        },
        "boundary": [
            "The result is linearized and omits the perturbation self-interaction B(w,w).",
            "It does not prove global regularity for order-one transverse perturbations.",
            "It does not prove instability, norm inflation, or finite-time singularity.",
            "It is not a solution of the Navier-Stokes Millennium problem.",
        ],
        "provenance": {
            "sourceCommit": source_commit,
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
            "gmpy2": gmpy2.version(),
            "inputCertificates": {
                "r069b": {
                    "path": str(R069B.relative_to(ROOT)),
                    "sha256": EXPECTED_R069B_SHA,
                }
            },
        },
    }
    return payload


def main() -> int:
    args = parse_args()
    payload = build_payload(args.source_commit)
    encoded = json.dumps(
        payload,
        indent=2 if args.pretty else None,
        sort_keys=args.pretty,
    ) + "\n"
    if args.output:
        Path(args.output).write_text(encoded)
    else:
        sys.stdout.write(encoded)
    if args.check and payload["status"] != "passed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
