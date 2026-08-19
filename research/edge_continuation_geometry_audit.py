#!/usr/bin/env python3
"""R0.35 exact audit of charge projection and continuation geometry.

The reduced edge equation contains a charge-zero projector and two Euler
derivatives.  This script records exact checks for four structural facts:

1. charge projection is Fourier projection under the weighted circle action;
2. fixed-charge extraction from a bivariate polydisc is possible exactly when
   |R| < rho_Z^2 rho_W;
3. translating a germ does not commute with the charge projector or the Euler
   fields, so the origin recurrence cannot be reused at a new Taylor center;
4. the nonlinear active fixed-point map is unbounded on a same-radius Wiener
   ball, but admits an explicit outer-to-half-radius bilinear bound 121/48.

The audit also compares the R0.31 certified polydisc with the finite R0.32
candidate hull.  That comparison is geometry, not a singularity theorem and
not a statement about full three-dimensional Navier--Stokes regularity.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time


R031_CERTIFICATE = Path(
    "research/certificates/r031/edge-optimized-majorant.json"
)
R032_CERTIFICATE = Path(
    "research/certificates/r032/edge-singularity-candidates.json"
)
R031_EXPECTED_SHA256 = (
    "32676dcefdf3c5285bdb18aab44bfdba385a84910d5e1d0df00f8ea9039ec395"
)
R032_EXPECTED_SHA256 = (
    "bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575"
)
EXPECTED_TAIL_HULL = {
    "lower": "-22346164857909747/29814773476186336",
    "upper": "-10516903672050296/14033145797491531",
}
PROGRESS_LOG: Path | None = None


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    elapsed = time.perf_counter() - started
    if enabled:
        suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
        print(
            f"[R0.35 +{elapsed:8.2f}s] {stage}{suffix}",
            file=sys.stderr,
            flush=True,
        )
    if PROGRESS_LOG is not None:
        record = {
            "timestampUtc": datetime.now(timezone.utc).isoformat(),
            "elapsedSeconds": elapsed,
            "stage": stage,
            **details,
        }
        with PROGRESS_LOG.open("a", encoding="utf-8") as target:
            target.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            target.flush()
            os.fsync(target.fileno())


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_state(source_commit: str | None) -> dict[str, object]:
    commit = source_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True
    ).strip()
    dirty = bool(
        subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            text=True,
        ).strip()
    )
    return {"commit": commit, "dirty": dirty if source_commit is None else False}


def decimal(value: Fraction, digits: int = 18) -> str:
    return format(float(value), f".{digits}g")


def cube_root_bracket(value: Fraction, digits: int = 30) -> tuple[Fraction, Fraction]:
    """Return an exact decimal bracket for the positive real cube root."""

    if value <= 0:
        raise ValueError("cube_root_bracket requires a positive rational")
    scale = 10**digits
    target_numerator = value.numerator * scale**3
    target_denominator = value.denominator
    low = 0
    high = scale
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**3 * target_denominator <= target_numerator:
            low = middle
        else:
            high = middle
    lower = Fraction(low, scale)
    upper = Fraction(low + 1, scale)
    if not lower**3 <= value < upper**3:
        raise AssertionError("cube-root enclosure failed")
    return lower, upper


def load_inputs() -> tuple[dict[str, object], dict[str, object], dict[str, object]]:
    r031_hash = sha256(R031_CERTIFICATE)
    r032_hash = sha256(R032_CERTIFICATE)
    if r031_hash != R031_EXPECTED_SHA256:
        raise AssertionError("R0.31 certificate hash mismatch")
    if r032_hash != R032_EXPECTED_SHA256:
        raise AssertionError("R0.32 certificate hash mismatch")
    r031 = json.loads(R031_CERTIFICATE.read_text(encoding="utf-8"))
    r032 = json.loads(R032_CERTIFICATE.read_text(encoding="utf-8"))
    hull = r032["diagnostic"]["tailTransportClusterHull"]
    if {key: hull[key] for key in EXPECTED_TAIL_HULL} != EXPECTED_TAIL_HULL:
        raise AssertionError("R0.32 tail candidate hull regression failed")
    provenance = {
        "r031": {
            "path": str(R031_CERTIFICATE),
            "sha256": r031_hash,
            "sourceCommit": r031["git"]["commit"],
            "majorantConstant": r031["formalTheorem"]["majorantConstant"],
            "commonPolydiscRadius": r031["formalTheorem"][
                "commonAnalyticDomain"
            ],
        },
        "r032": {
            "path": str(R032_CERTIFICATE),
            "sha256": r032_hash,
            "sourceCommit": r032["git"]["commit"],
            "tailTransportClusterHull": hull,
            "classification": r032["scope"]["classification"],
        },
    }
    return r031, r032, provenance


def charge_projection_regression() -> dict[str, object]:
    samples = []
    for n, k in ((0, 0), (1, 0), (0, 1), (2, 1), (5, 3), (8, 2)):
        charge = 2 * k - n
        total_degree = n + k
        samples.append(
            {
                "zExponent": n,
                "wExponent": k,
                "charge": charge,
                "totalDegree": total_degree,
                "circleMultiplier": f"exp(i*{charge}*theta)",
                "projectionRetainsExactlyCharge": charge,
            }
        )
    return {
        "circleAction": "gamma_theta(Z,W)=(exp(-i theta)Z,exp(2i theta)W)",
        "projectionFormula": (
            "Pi_q f=(1/(2*pi))*integral_0^(2*pi) "
            "exp(-i*q*theta)*f(gamma_theta(Z,W)) dtheta"
        ),
        "monomialRegression": samples,
        "wienerNorm": "||f||_(rho_Z,rho_W)=sum_(n,k>=0)|f_(n,k)|rho_Z^n rho_W^k",
        "contraction": "||Pi_q f||_rho <= ||f||_rho for every integer q",
    }


def translation_obstruction() -> dict[str, object]:
    return {
        "recenter": "(tau_c f)(zeta,omega)=f(z_0+zeta,w_0+omega)",
        "projectorCounterexamples": [
            {
                "condition": "z_0 != 0",
                "field": "f(Z,W)=Z",
                "tauAfterGlobalPi0": "0",
                "localPi0AfterTau": "z_0",
            },
            {
                "condition": "w_0 != 0",
                "field": "f(Z,W)=W",
                "tauAfterGlobalPi0": "0",
                "localPi0AfterTau": "w_0",
            },
        ],
        "conjugatedEulerFields": {
            "X_c": "(z_0+zeta)*partial_zeta",
            "Y_c": "(w_0+omega)*partial_omega",
        },
        "conjugatedProjector": (
            "Pi_q^c g=(1/(2*pi))*integral exp(-i*q*theta) "
            "g(exp(-i*theta)*(z_0+zeta)-z_0,"
            "exp(2i*theta)*(w_0+omega)-w_0) dtheta"
        ),
        "orbitContainmentSufficientCondition": (
            "an outer local polydisc with radii R_Z,R_W contains the affine "
            "circle orbit of every point in an inner polydisc r_Z,r_W if "
            "R_Z>r_Z+2|z_0| and R_W>r_W+2|w_0|"
        ),
        "conclusion": (
            "the origin coefficient recurrence cannot be copied unchanged at "
            "a nonzero Taylor center"
        ),
    }


def exact_same_radius_output_norm(n: int) -> Fraction:
    """Evaluate Phi on the normalized two-monomial witness algebraically."""

    if n < 1:
        raise ValueError("the witness degree must be positive")
    # Radius factors cancel in the output norm, so the two normalized
    # monomial coefficients can both be represented by 1/2.
    monomials = (
        (Fraction(1, 2), n, 0),
        (Fraction(1, 2), 0, n),
    )
    bracket: dict[tuple[int, int], Fraction] = {}
    for left_coefficient, left_n, left_k in monomials:
        for right_coefficient, right_n, right_k in monomials:
            right_charge = 2 * right_k - right_n
            determinant = left_n * right_k - left_k * right_n
            exponent = (left_n + right_n, left_k + right_k)
            bracket[exponent] = bracket.get(exponent, Fraction(0)) + (
                left_coefficient
                * right_coefficient
                * right_charge
                * determinant
            )
    output_coefficient = bracket[(n, n)]
    output_charge = n
    output_degree = 2 * n
    output_coefficient /= output_charge
    output_coefficient /= output_degree - 1
    return abs(output_coefficient)


def operator_bounds() -> dict[str, object]:
    first_multiplier = Fraction(1, 2)
    second_multiplier = Fraction(9, 8)
    mixed_multiplier = first_multiplier**2
    charge_part = Fraction(33, 16)
    zero_charge_bracket = Fraction(11, 8)
    zero_charge_inverse = Fraction(1, 3)
    zero_charge_part = zero_charge_bracket * zero_charge_inverse
    total = charge_part + zero_charge_part
    if total != Fraction(121, 48):
        raise AssertionError("half-radius bilinear constant regression failed")
    witnesses = []
    for n in (1, 2, 3, 4, 8, 16, 32, 64, 128):
        output_norm = exact_same_radius_output_norm(n)
        expected = Fraction(3 * n * n, 4 * (2 * n - 1))
        if output_norm != expected:
            raise AssertionError("same-radius monomial algebra regression failed")
        witnesses.append(
            {
                "N": n,
                "inputNorm": "1",
                "outputNorm": str(output_norm),
                "outputNormDecimal": decimal(output_norm),
            }
        )
    return {
        "activeFixedPointMap": (
            "Phi(f)=(L-1)^(-1)[(I-Pi0)Q^(-1){f,Qf}"
            "+Pi0 L^(-1){f,Lf}]"
        ),
        "sameRadiusUnboundedness": {
            "witness": (
                "f_N=(rho_Z^(-N)Z^N+rho_W^(-N)W^N)/2, ||f_N||_rho=1"
            ),
            "exactOutputNorm": "||Phi(f_N)||_rho=3*N^2/(4*(2*N-1))",
            "limit": "+infinity",
            "samples": witnesses,
            "exactRegressionRange": "1 <= N <= 128",
        },
        "halfRadiusMultipliers": {
            "sup_n_n_over_2n": str(first_multiplier),
            "sup_n_n2_over_2n": str(second_multiplier),
            "sup_nm_nm_over_2n2m": str(mixed_multiplier),
        },
        "halfRadiusBilinearBound": {
            "nonzeroChargePart": str(charge_part),
            "zeroChargeBracketBeforeLInverse": str(zero_charge_bracket),
            "zeroChargeLInverse": str(zero_charge_inverse),
            "zeroChargePart": str(zero_charge_part),
            "total": str(total),
            "statement": (
                "||B(f,g)||_(rho_Z/2,rho_W/2) <= "
                "(121/48)||f||_rho||g||_rho, where Phi(f)=B(f,f)"
            ),
            "lipschitzStatement": (
                "||Phi(f)-Phi(g)||_(rho/2) <= "
                "(121/48)(||f||_rho+||g||_rho)||f-g||_rho"
            ),
        },
    }


def extraction_geometry(r032: dict[str, object]) -> dict[str, object]:
    certified_radius = Fraction(4, 81)
    certified_r_radius = certified_radius**3
    hull = r032["diagnostic"]["tailTransportClusterHull"]  # type: ignore[index]
    negative_lower = Fraction(hull["lower"])  # type: ignore[index]
    negative_upper = Fraction(hull["upper"])  # type: ignore[index]
    candidate_abs_lower = -negative_upper
    candidate_abs_upper = -negative_lower
    balanced_lower = cube_root_bracket(candidate_abs_lower)
    balanced_upper = cube_root_bracket(candidate_abs_upper)
    radius_ratio_lower = balanced_lower[0] / certified_radius
    radius_ratio_upper = balanced_upper[1] / certified_radius
    r_ratio_lower = candidate_abs_lower / certified_r_radius
    r_ratio_upper = candidate_abs_upper / certified_r_radius
    return {
        "substitution": "Z=Xi^(-1), W=R*Xi^2",
        "coefficientFormula": (
            "F_q(R)=(1/(2*pi*i))*integral F(Xi^(-1),R*Xi^2)"
            "*Xi^(-q-1) dXi"
        ),
        "contourCondition": (
            "1/rho_Z < |Xi| < sqrt(rho_W/|R|); such a contour exists "
            "if and only if |R| < rho_Z^2*rho_W"
        ),
        "isotropicBalance": {
            "minimizedQuantity": "min_|Xi| max(|Xi|^(-1),|R|*|Xi|^2)",
            "balancedXiRadius": "|R|^(-1/3)",
            "minimumBivariateRadius": "|R|^(1/3)",
        },
        "r031": {
            "bivariateRadius": str(certified_radius),
            "bivariateRadiusDecimal": decimal(certified_radius),
            "fixedChargeRadius": str(certified_r_radius),
            "fixedChargeRadiusDecimal": decimal(certified_r_radius),
        },
        "r032FiniteCandidate": {
            "absoluteRLower": str(candidate_abs_lower),
            "absoluteRUpper": str(candidate_abs_upper),
            "absoluteRLowerDecimal": decimal(candidate_abs_lower),
            "absoluteRUpperDecimal": decimal(candidate_abs_upper),
            "balancedRadiusLower": str(balanced_lower[0]),
            "balancedRadiusUpper": str(balanced_upper[1]),
            "balancedRadiusLowerDecimal": decimal(balanced_lower[0]),
            "balancedRadiusUpperDecimal": decimal(balanced_upper[1]),
            "balancedToR031RadiusRatioLower": str(radius_ratio_lower),
            "balancedToR031RadiusRatioUpper": str(radius_ratio_upper),
            "balancedToR031RadiusRatioLowerDecimal": decimal(radius_ratio_lower),
            "balancedToR031RadiusRatioUpperDecimal": decimal(radius_ratio_upper),
            "absoluteRToR031FixedChargeRatioLower": str(r_ratio_lower),
            "absoluteRToR031FixedChargeRatioUpper": str(r_ratio_upper),
            "absoluteRToR031FixedChargeRatioLowerDecimal": decimal(r_ratio_lower),
            "absoluteRToR031FixedChargeRatioUpperDecimal": decimal(r_ratio_upper),
            "classification": (
                "finite exact Pade candidate geometry only; no original-function "
                "singularity or continuation path is certified"
            ),
        },
    }


def build_payload(arguments: argparse.Namespace) -> dict[str, object]:
    started = time.perf_counter()
    progress(arguments.progress, started, "loading pinned R0.31 and R0.32 inputs")
    r031, r032, provenance = load_inputs()
    progress(arguments.progress, started, "checking Fourier charge projection")
    projection = charge_projection_regression()
    progress(arguments.progress, started, "checking translation obstruction")
    translation = translation_obstruction()
    progress(arguments.progress, started, "checking same- and half-radius operators")
    operators = operator_bounds()
    progress(arguments.progress, started, "checking fixed-charge contour geometry")
    geometry = extraction_geometry(r032)

    checks = {
        "pinnedInputHashes": (
            provenance["r031"]["sha256"] == R031_EXPECTED_SHA256
            and provenance["r032"]["sha256"] == R032_EXPECTED_SHA256
        ),
        "chargeActionOnMonomials": all(
            record["charge"] == 2 * record["wExponent"] - record["zExponent"]
            for record in projection["monomialRegression"]
        ),
        "translationCounterexamplesNonzero": all(
            record["localPi0AfterTau"] != record["tauAfterGlobalPi0"]
            for record in translation["projectorCounterexamples"]
        ),
        "halfRadiusDerivativeMaxima": operators["halfRadiusMultipliers"] == {
            "sup_n_n_over_2n": "1/2",
            "sup_n_n2_over_2n": "9/8",
            "sup_nm_nm_over_2n2m": "1/4",
        },
        "halfRadiusConstant": (
            operators["halfRadiusBilinearBound"]["total"] == "121/48"
        ),
        "sameRadiusWitnessGrows": (
            Fraction(
                operators["sameRadiusUnboundedness"]["samples"][-1]["outputNorm"]
            )
            > Fraction(
                operators["sameRadiusUnboundedness"]["samples"][0]["outputNorm"]
            )
        ),
        "sameRadiusFormula": all(
            exact_same_radius_output_norm(n)
            == Fraction(3 * n * n, 4 * (2 * n - 1))
            for n in range(1, 129)
        ),
        "candidateOutsideR031FixedChargeDisc": (
            Fraction(geometry["r032FiniteCandidate"]["absoluteRLower"])
            > Fraction(geometry["r031"]["fixedChargeRadius"])
        ),
        "candidateRequiresLargerBalancedRadius": (
            Fraction(
                geometry["r032FiniteCandidate"][
                    "balancedToR031RadiusRatioLower"
                ]
            )
            > 18
        ),
    }
    if not all(checks.values()):
        failures = [name for name, passed in checks.items() if not passed]
        raise AssertionError("R0.35 checks failed: " + ", ".join(failures))
    progress(
        arguments.progress,
        started,
        "completed R0.35 continuation-geometry certificate",
        passed=True,
        checks=len(checks),
    )
    return {
        "scope": {
            "result": (
                "exact continuation-domain geometry, a translation obstruction, "
                "same-radius unboundedness, and a half-radius operator bound"
            ),
            "classification": (
                "all-order algebraic and functional-analytic statements with "
                "a finite candidate-distance diagnostic"
            ),
            "limitations": [
                "the half-radius estimate is not yet a validated continuation chain",
                "the estimate does not prove existence at a nonzero center",
                "the R0.32 hull remains a finite Pade diagnostic rather than a singularity theorem",
                "no singularity-free torus-saturated domain reaching R=-0.7495 has been constructed",
                "the result concerns the reduced edge system rather than the full three-dimensional PDE",
                "no Navier-Stokes regularity or blow-up conclusion is claimed",
            ],
        },
        "input": provenance,
        "chargeProjection": projection,
        "translationObstruction": translation,
        "operatorScale": operators,
        "fixedChargeExtraction": geometry,
        "checks": checks,
        "computation": {
            "backend": "Python exact integers and Fraction arithmetic",
            "randomSeed": None,
            "wallSeconds": time.perf_counter() - started,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "git": git_state(arguments.source_commit),
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--source-commit",
        help="record an already-created clean source commit in the formal certificate",
    )
    return parser.parse_args()


def main() -> None:
    global PROGRESS_LOG
    arguments = parse_arguments()
    if arguments.progress_log is not None:
        if arguments.progress_log.exists():
            raise SystemExit("--progress-log already exists; choose a new path")
        arguments.progress_log.parent.mkdir(parents=True, exist_ok=True)
        PROGRESS_LOG = arguments.progress_log
    payload = build_payload(arguments)
    if arguments.check and not all(payload["checks"].values()):
        raise AssertionError("R0.35 checks failed")
    serialized = json.dumps(
        payload,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=True,
    ) + "\n"
    if arguments.output is None:
        sys.stdout.write(serialized)
    else:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = arguments.output.with_suffix(
            arguments.output.suffix + f".tmp-{os.getpid()}"
        )
        temporary.write_text(serialized, encoding="utf-8")
        os.replace(temporary, arguments.output)


if __name__ == "__main__":
    main()
