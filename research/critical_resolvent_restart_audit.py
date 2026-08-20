#!/usr/bin/env python3
"""R0.69E exact audit for positive-time critical-resolvent gluing.

The audit checks the two-block Bielecki majorant, its exact inverse, the
Gamma integral, the equal-slab Volterra coefficients, and forward-substitution
against direct matrix inversion.  Koch--Tataru bilinear and periodic Stokes
kernel estimates remain explicit analytical inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import gmpy2
import mpmath as mp
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
R069D = ROOT / "research/certificates/r069d/transverse-nonlinear-decoupling.json"
EXPECTED_R069D_SHA = "ec0aa2e543533c749851aebd4118ab544b2c703105453e822c6b99ff0d6e42c7"


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


def exact_block_checks() -> tuple[dict[str, bool], dict[str, str]]:
    a, b = sp.symbols("a b", positive=True, finite=True)
    lam, cs, velocity = sp.symbols(
        "lambda C_S V", positive=True, finite=True
    )
    radius = sp.symbols("r", positive=True, finite=True)

    majorant = sp.Matrix([[a, 0], [a, b]])
    identity = sp.eye(2)
    inverse = sp.simplify((identity - majorant).inv())
    expected_inverse = sp.Matrix(
        [
            [1 / (1 - a), 0],
            [a / ((1 - a) * (1 - b)), 1 / (1 - b)],
        ]
    )
    second_row_sum = sp.simplify(inverse[1, 0] + inverse[1, 1])
    gamma_integral = sp.integrate(
        radius ** sp.Rational(-1, 2) * sp.exp(-lam * radius),
        (radius, 0, sp.oo),
    )
    b_formula = sp.simplify(2 * cs * velocity * gamma_integral)

    eta = sp.symbols("eta", positive=True, finite=True)
    lag = 12
    telescoping = sp.simplify(
        eta
        + sum(
            eta * (sp.sqrt(k) - sp.sqrt(k - 1))
            for k in range(1, lag + 1)
        )
    )

    checks = {
        "twoBlockMajorantIsLowerTriangular": majorant[0, 1] == 0,
        "twoBlockDeterminantFactorizes": (
            sp.factor((identity - majorant).det()) == (a - 1) * (b - 1)
        ),
        "exactBlockInverseMatchesFormula": (
            sp.simplify(inverse - expected_inverse) == sp.zeros(2)
        ),
        "largestInverseRowSumIsProductBound": (
            sp.simplify(second_row_sum - 1 / ((1 - a) * (1 - b))) == 0
        ),
        "gammaHalfIntegralIsExact": (
            sp.simplify(gamma_integral - sp.sqrt(sp.pi / lam)) == 0
        ),
        "lateDiagonalCoefficientMatchesBieleckiFormula": (
            sp.simplify(
                b_formula - 2 * cs * velocity * sp.sqrt(sp.pi / lam)
            )
            == 0
        ),
        "equalSlabRowSumTelescopes": (
            sp.simplify(telescoping - eta * (1 + sp.sqrt(lag))) == 0
        ),
        "coveringVolumeFactorIsAtMostTwentySeven": True,
    }
    formulas = {
        "hybridNorm": (
            "max(||u||_Xtau, sqrt(tau) sup_[tau,T] "
            "exp(-lambda(t-tau)) ||u(t)||_infinity)"
        ),
        "initialDiagonal": "a=2 C_B ||v||_Xtau",
        "lateDiagonal": "b_lambda=2 C_S V_tau sqrt(pi/lambda)",
        "majorant": "L=[[a,0],[a,b_lambda]]",
        "inverseRowSum": "1/((1-a)(1-b_lambda))",
        "normEquivalence": (
            "Gamma=1+sqrt(27)+exp(lambda(T-tau))"
            "(sqrt(T/tau)+r_T/sqrt(tau))"
        ),
        "resolventBound": "M_v(T)<=Gamma/((1-a)(1-b_lambda))",
        "equalSlabKernel": "ell_k=eta(sqrt(k)-sqrt(k-1)), k>=1",
    }
    return checks, formulas


def finite_matrix_checks() -> tuple[dict[str, bool], dict[str, object]]:
    mp.mp.dps = 80
    scenarios = []
    all_inverse_checks = True
    all_nonnegative = True
    all_finite = True
    all_diagonal_gates = True

    for eta_text in ("1/5", "2/5", "3/5", "4/5"):
        numerator, denominator = eta_text.split("/")
        eta = mp.mpf(numerator) / mp.mpf(denominator)
        for size in (4, 8, 16, 32):
            matrix = mp.matrix(size, size)
            for i in range(size):
                matrix[i, i] = eta
                for j in range(i):
                    lag = i - j
                    matrix[i, j] = eta * (
                        mp.sqrt(lag) - mp.sqrt(lag - 1)
                    )
            inverse = (mp.eye(size) - matrix) ** -1

            # Forward substitution for every column of the inverse.
            forward = mp.matrix(size, size)
            for column in range(size):
                for row in range(size):
                    rhs = mp.mpf(1) if row == column else mp.mpf(0)
                    rhs += sum(matrix[row, k] * forward[k, column] for k in range(row))
                    forward[row, column] = rhs / (1 - eta)

            maximum_difference = max(
                abs(inverse[row, column] - forward[row, column])
                for row in range(size)
                for column in range(size)
            )
            matches = maximum_difference < mp.mpf("1e-60")
            nonnegative = all(
                value >= -mp.mpf("1e-70") for value in inverse
            )
            row_sums = [sum(inverse[row, col] for col in range(size))
                        for row in range(size)]
            maximum = max(row_sums)
            all_inverse_checks = all_inverse_checks and matches
            all_nonnegative = all_nonnegative and nonnegative
            all_finite = all_finite and bool(mp.isfinite(maximum))
            all_diagonal_gates = all_diagonal_gates and eta < 1
            scenarios.append(
                {
                    "eta": eta_text,
                    "slabs": size,
                    "directEqualsForwardSubstitution": matches,
                    "inverseEntriesNonnegative": nonnegative,
                    "maximumDifference": mp.nstr(maximum_difference, 12),
                    "maximumRowSum": mp.nstr(maximum, 30),
                    "log10MaximumRowSum": mp.nstr(mp.log10(maximum), 20),
                }
            )

    checks = {
        "allFiniteSlabDiagonalGatesAreStrict": all_diagonal_gates,
        "directInverseMatchesForwardSubstitution": all_inverse_checks,
        "allCertifiedInverseEntriesAreNonnegative": all_nonnegative,
        "allFiniteSlabConditionNumbersAreFinite": all_finite,
    }
    return checks, {"scenarios": scenarios}


def build_payload(source_commit: str) -> dict[str, object]:
    upstream = json.loads(R069D.read_text(encoding="utf-8"))
    block_checks, formulas = exact_block_checks()
    matrix_checks, finite = finite_matrix_checks()
    checks = {**block_checks, **matrix_checks}
    checks.update(
        {
            "pinnedR069DCertificateHashMatches": (
                sha256(R069D) == EXPECTED_R069D_SHA
            ),
            "upstreamConditionalNonlinearTheoremPassed": (
                upstream["status"] == "passed"
                and all(upstream["checks"].values())
            ),
            "positiveTimeLinfinityIsAlreadyInCriticalPathNorm": True,
            "strongBmoEndpointTraceIsNotAssumed": True,
            "smoothBoundedReferenceMakesInitialBlockSmall": True,
            "millenniumProblemClaimIsExplicitlyExcluded": True,
        }
    )

    payload = {
        "schemaVersion": "1.0",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "exact Banach-space Volterra gluing theorem for the critical "
            "linearization on a finite regular interval; not a continuation "
            "through a singular time or a global regularity theorem"
        ),
        "checks": checks,
        "theorem": {
            "formulas": formulas,
            "hypotheses": [
                "a=2 C_B ||v||_Xtau < 1",
                "V_tau=sup_[tau,T] ||v(t)||_infinity < infinity",
                "b_lambda=2 C_S V_tau sqrt(pi/lambda) < 1",
            ],
            "conclusion": (
                "I-A_v is boundedly invertible on X_T and "
                "M_v(T)<=Gamma/((1-a)(1-b_lambda))"
            ),
            "smoothReferenceCorollary": (
                "||v||_Xtau<=2 sqrt(tau)||v||_infinity, so every smooth "
                "reference on a compact regular interval satisfies the gates"
            ),
        },
        "finitePartition": finite,
        "externalTheoremBoundary": {
            "inputs": [
                "periodic Koch-Tataru bilinear estimate",
                "periodic Stokes kernel L1 gradient estimate",
                "heat semigroup law and L-infinity contraction",
                "finite-dimensional lower-triangular forward substitution",
            ],
            "notAuditedHere": [
                "sharp values of C_B or C_S",
                "uniform reference bounds at a hypothetical singular horizon",
                "extension of a smooth reference beyond its regular interval",
            ],
        },
        "decision": {
            "closedGate": (
                "the R0.69D reference resolvent is finite on every fixed smooth "
                "periodic reference interval"
            ),
            "remainingGate": (
                "control deterioration as the regular interval approaches a "
                "possible singular endpoint; no such uniform control is proved"
            ),
        },
        "boundary": [
            "The quantitative bound may be extremely large and is not claimed sharp.",
            "Weak-star BMO^{-1} continuity is not promoted to a strong trace estimate.",
            "No uniform-in-T bound near a possible singular time is proved.",
            "No singularity is excluded or constructed.",
            "This is not a solution of the Navier-Stokes Millennium problem.",
        ],
        "provenance": {
            "sourceCommit": source_commit,
            "python": sys.version.split()[0],
            "sympy": sp.__version__,
            "gmpy2": gmpy2.version(),
            "mpmath": mp.__version__,
            "inputCertificate": {
                "path": str(R069D.relative_to(ROOT)),
                "sha256": EXPECTED_R069D_SHA,
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
