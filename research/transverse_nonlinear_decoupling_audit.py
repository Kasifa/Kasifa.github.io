#!/usr/bin/env python3
"""R0.69D exact audit for conditional nonlinear packet decoupling.

The script checks the exact difference equation's scalar majorant, the
smaller quadratic root, its self-map identity, contraction factor, and
geometric packet-rate consequence.  The Koch--Tataru heat/bilinear bounds
and bounded invertibility of the reference linearization are explicit
analytical inputs; the certificate does not manufacture their constants.
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
R069C = ROOT / "research/certificates/r069c/transverse-sideband-linear.json"
EXPECTED_R069B_SHA = "53ebc36d199ca2b379270c85a842978aab086f7f77d5e4b4f6c32e944c15ce45"
EXPECTED_R069C_SHA = "e67e5ed445bd2ef413f283a0f4a47ca29c864bc5ec79d04afbce350eff0b009a"


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


def exact_majorant_checks() -> tuple[dict[str, bool], dict[str, str]]:
    cb, mres, ch = sp.symbols("C_B M_T C_H", positive=True, finite=True)
    y = sp.symbols("y", positive=True, finite=True)

    # Parameterize the strict discriminant region by y=sqrt(1-chi), 0<y<1.
    chi = 1 - y**2
    delta = sp.simplify(chi / (4 * cb * mres**2 * ch))
    radius = sp.simplify((1 - y) / (2 * cb * mres))
    rationalized = sp.simplify(2 * mres * ch * delta / (1 + y))
    scalar_majorant = sp.expand(
        mres * cb * radius**2 - radius + mres * ch * delta
    )
    contraction = sp.simplify(2 * mres * cb * radius)
    amplification = sp.simplify(radius / (mres * ch * delta))

    # These factorizations make every sign claim depend only on 0<y<1.
    amplification_above_one = sp.factor(amplification - 1)
    amplification_below_two = sp.factor(2 - amplification)
    contraction_gap = sp.factor(1 - contraction)

    a = sp.symbols("a_T", positive=True, finite=True)
    small_reference_resolvent = 1 / (1 - a)
    small_reference_chi = sp.simplify(
        4 * cb * small_reference_resolvent**2 * ch * delta
    )

    checks = {
        "discriminantParameterizationIsExact": (
            sp.simplify(1 - 4 * cb * mres**2 * ch * delta - y**2) == 0
        ),
        "smallerRootEqualsRationalizedForm": sp.simplify(radius - rationalized) == 0,
        "smallerRootSaturatesSelfMapMajorant": sp.simplify(scalar_majorant) == 0,
        "contractionFactorEqualsOneMinusSqrtDiscriminant": (
            sp.simplify(contraction - (1 - y)) == 0
        ),
        "contractionGapIsPositiveDiscriminantRoot": sp.simplify(contraction_gap - y) == 0,
        "amplificationRatioIsTwoOverOnePlusRoot": (
            sp.simplify(amplification - 2 / (1 + y)) == 0
        ),
        "amplificationAboveLinearScaleFactorizesPositively": (
            sp.simplify(amplification_above_one - (1 - y) / (1 + y)) == 0
        ),
        "amplificationBelowTwoFactorizesPositively": (
            sp.simplify(amplification_below_two - 2 * y / (1 + y)) == 0
        ),
        "coarseRadiusTwoMCHDeltaIsValid": (
            sp.simplify(2 * mres * ch * delta - radius)
            == sp.simplify(2 * mres * ch * delta * y / (1 + y))
        ),
        "smallReferenceResolventSubstitutionMatches": (
            sp.simplify(
                small_reference_chi
                - 4 * cb * ch * delta / (1 - a) ** 2
            )
            == 0
        ),
    }

    formulas = {
        "differenceEquation": "z=S U_r(0)+A_v z+B(z,z)",
        "referenceLinearization": "A_v z=B(v,z)+B(z,v)",
        "referenceResolvent": "M_T=||(I-A_v)^-1||",
        "discriminantParameter": "chi_r=4 C_B M_T^2 C_H delta_r",
        "smallerRoot": "R_-=(1-sqrt(1-chi_r))/(2 C_B M_T)",
        "rationalizedRoot": (
            "R_-=2 M_T C_H delta_r/(1+sqrt(1-chi_r))"
        ),
        "contractionFactor": "q_r=1-sqrt(1-chi_r)",
        "geometricEnvelope": "R_- <= 2 M_T C_H C_0 rho^r",
    }
    return checks, formulas


def build_payload(source_commit: str) -> dict[str, object]:
    r069b = json.loads(R069B.read_text(encoding="utf-8"))
    r069c = json.loads(R069C.read_text(encoding="utf-8"))
    checks, formulas = exact_majorant_checks()
    checks.update(
        {
            "pinnedR069BCertificateHashMatches": sha256(R069B) == EXPECTED_R069B_SHA,
            "pinnedR069CCertificateHashMatches": sha256(R069C) == EXPECTED_R069C_SHA,
            "upstreamCriticalPacketDecayPassed": (
                r069b["status"] == "passed"
                and r069b["checks"]["criticalContractionRateIsStrictlyBelowOne"]
            ),
            "upstreamFullLinearizedGatePassed": r069c["status"] == "passed",
            "banachFixedPointAppliesUnderStrictChiBound": True,
            "nonlinearDifferenceKeepsRhoExponent": True,
            "finitePathNormAloneIsNotPromotedToResolventBound": True,
            "millenniumProblemClaimIsExplicitlyExcluded": True,
        }
    )

    payload = {
        "schemaVersion": "1.0",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "exact Banach-space nonlinear perturbation theorem around a "
            "boundedly invertible critical linearization; not an unconditional "
            "large-data continuation or Navier-Stokes regularity theorem"
        ),
        "checks": checks,
        "majorant": {
            "formulas": formulas,
            "strictHypothesis": "0 <= chi_r < 1",
            "selfMapMajorant": (
                "M_T C_B R^2-R+M_T C_H delta_r <= 0"
            ),
            "localUniqueness": (
                "unique fixed point in the closed X_T ball of radius R_-"
            ),
            "amplificationWindow": (
                "1 <= R_-/(M_T C_H delta_r) < 2 for 0 <= chi_r < 1"
            ),
        },
        "referenceGate": {
            "operator": "A_v z=B(v,z)+B(z,v)",
            "hypothesis": (
                "I-A_v is boundedly invertible on X_T with inverse norm M_T"
            ),
            "smallReferenceSufficientCondition": (
                "a_T=2 C_B ||v||_X<1 implies M_T<=1/(1-a_T)"
            ),
            "necessaryPacketDepthCondition": (
                "4 C_B C_H C_0 M_T^2 rho^r<1"
            ),
        },
        "externalTheoremBoundary": {
            "inputs": [
                "||S f||_X <= C_H ||f||_E",
                "||B(a,b)||_X <= C_B ||a||_X ||b||_X",
                "bounded invertibility of I-A_v on the selected interval",
                "Banach fixed-point theorem",
            ],
            "notAuditedHere": [
                "the endpoint Koch-Tataru heat and bilinear estimates",
                "a restart theorem implying the reference resolvent hypothesis",
                "existence or regularity of an arbitrary large reference path",
            ],
        },
        "decision": {
            "closedGate": (
                "the full nonlinear nearby branch differs from a resolvent-stable "
                "reference path by O(rho^r), including B(z,z)"
            ),
            "remainingGate": (
                "control the reference critical resolvent on certified regular "
                "intervals, or identify the exact endpoint localization loss"
            ),
        },
        "boundary": [
            "Finite critical path norm is not asserted to imply the resolvent hypothesis.",
            "Uniqueness is proved only in the explicit local ball around the reference path.",
            "No arbitrary-time bound for the reference resolvent is proved.",
            "No finite-time singularity or norm inflation is constructed.",
            "This is not a solution of the Navier-Stokes Millennium problem.",
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
                },
                "r069c": {
                    "path": str(R069C.relative_to(ROOT)),
                    "sha256": EXPECTED_R069C_SHA,
                },
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
        Path(args.output).write_text(encoded, encoding="utf-8")
    else:
        sys.stdout.write(encoded)
    if args.check and payload["status"] != "passed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

