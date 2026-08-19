#!/usr/bin/env python3
"""R0.54 diagnostic for the complete product-affine charge-weight family.

This file performs *non-certified* high-precision localization and deterministic
multistart optimization.  It is deliberately separate from the eventual exact
R0.54 audit: floating-point output from this script may select proof boxes and
candidate active sets, but it must never decide a published sign.

For the former active input charge ``S=162`` set

    alpha = lambda / (1 + S lambda),
    beta  = mu     / (1 + S mu),
    A = alpha + beta,
    B = alpha beta.

At fixed ``(r,c)`` both necessary columns are affine in ``(A,B)``:

    F = M0 - 1 + A M1 + B M2,
    G = g0 + A g1 + B g2.

The complete square ``0<=alpha,beta<1/S`` maps onto

    0 <= A < 2/S,
    max(0, (A-S^-1)/S) < B <= A^2/4,

with the lower inequality non-strict on the part ``A<=1/S``.  The upper curve
``B=A^2/4`` is the symmetric locus ``alpha=beta``.  These identities are exact
and are the starting point for the later global certificate.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import platform
import sys
import time

import gmpy2
import mpmath as mp
import numpy as np
import scipy
from scipy.optimize import minimize

import edge_affine_family_kkt_audit as r052
import edge_charge_character_optimization_audit as r050
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036


Rational = gmpy2.mpq
ACTIVE_CHARGE = 162


def rational_to_float(value: Rational) -> float:
    return float(gmpy2.mpfr(value, 80))


def mp_value(value: Rational) -> mp.mpf:
    return mp.mpf(int(gmpy2.numer(value))) / int(gmpy2.denom(value))


def invariant_bounds(a_sum: Rational) -> tuple[Rational, Rational]:
    """Return the exact closed ``B`` bounds at a fixed invariant ``A``.

    The returned bounds describe the closure of the product-affine square.  At
    ``A>1/S`` the lower bound corresponds to one compactified parameter equal
    to ``1/S`` and is therefore attained only in the infinite-slope limit.
    """

    h = Rational(1, ACTIVE_CHARGE)
    if a_sum < 0 or a_sum > 2 * h:
        raise ValueError("A is outside the closed product-affine invariant domain")
    lower = max(Rational(0), h * (a_sum - h))
    upper = a_sum * a_sum / 4
    return lower, upper


def check_invariant_identity(alpha: Rational, beta: Rational) -> bool:
    h = Rational(1, ACTIVE_CHARGE)
    if not (0 <= alpha <= h and 0 <= beta <= h):
        raise ValueError("alpha and beta must lie in the closed compactified square")
    a_sum = alpha + beta
    product = alpha * beta
    lower, upper = invariant_bounds(a_sum)
    return lower <= product <= upper


@dataclass(frozen=True)
class DiagnosticModel:
    active_degree: np.ndarray
    active_charge: np.ndarray
    active_coefficient: np.ndarray
    zero_degree: np.ndarray
    zero_charge: np.ndarray
    zero_coefficient: np.ndarray
    active_mp: tuple[tuple[int, int, mp.mpf], ...]
    zero_mp: tuple[tuple[int, int, mp.mpf], ...]

    @staticmethod
    def build(maximum_degree: int, progress: bool = False) -> "DiagnosticModel":
        started = time.perf_counter()
        field, _, _, interactions = r028.rational_edge_recurrence(
            maximum_degree, progress, started
        )
        polynomial = r036.field_to_polynomial(field, maximum_degree)
        terms = r048.independent_terms(polynomial)
        active = r050.active_laurent_terms(
            terms, maximum_degree + 1, ACTIVE_CHARGE
        )
        zero = r052.zero_terms(terms, maximum_degree)
        if progress:
            print(
                "[R0.54 diagnostic] built model "
                f"with {len(active)} active terms, {len(zero)} zero terms, "
                f"and {interactions} recurrence interactions",
                file=sys.stderr,
                flush=True,
            )

        def arrays(data: list[tuple[int, int, Rational]]):
            return (
                np.asarray([degree for degree, _, _ in data], dtype=np.float64),
                np.asarray([charge for _, charge, _ in data], dtype=np.float64),
                np.asarray(
                    [rational_to_float(coefficient) for _, _, coefficient in data],
                    dtype=np.float64,
                ),
            )

        active_degree, active_charge, active_coefficient = arrays(active)
        zero_degree, zero_charge, zero_coefficient = arrays(zero)
        return DiagnosticModel(
            active_degree,
            active_charge,
            active_coefficient,
            zero_degree,
            zero_charge,
            zero_coefficient,
            tuple((d, q, mp_value(v)) for d, q, v in active),
            tuple((d, q, mp_value(v)) for d, q, v in zero),
        )

    @staticmethod
    def sigmoid(value: float) -> float:
        if value >= 0:
            inverse = math.exp(-value)
            return 1 / (1 + inverse)
        exponential = math.exp(value)
        return exponential / (1 + exponential)

    def margins(self, coordinates: np.ndarray) -> tuple[float, float]:
        radius, log_character, alpha_logit, beta_logit = coordinates
        character = math.exp(log_character)
        u = self.sigmoid(alpha_logit)
        v = self.sigmoid(beta_logit)
        alpha = u / ACTIVE_CHARGE
        beta = v / ACTIVE_CHARGE
        active_monomial = (
            self.active_coefficient
            * np.power(radius, self.active_degree)
            * np.exp(log_character * self.active_charge)
        )
        active_value = np.sum(
            active_monomial
            * (1 + alpha * self.active_charge)
            * (1 + beta * self.active_charge)
        )
        lam = u / (ACTIVE_CHARGE * (1 - u))
        mu = v / (ACTIVE_CHARGE * (1 - v))
        zero_monomial = (
            self.zero_coefficient
            * np.power(radius, self.zero_degree)
            * np.exp(log_character * self.zero_charge)
        )
        zero_abs_charge = np.abs(self.zero_charge)
        zero_value = np.sum(
            zero_monomial
            * (1 + lam * zero_abs_charge)
            * (1 + mu * zero_abs_charge)
        )
        return float(1 - active_value), float(1 - zero_value)

    def symmetric_equations(
        self, radius: mp.mpf, log_character: mp.mpf, alpha: mp.mpf, x: mp.mpf
    ) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
        """Return ``F=0,G=0`` and diagonal stationarity at fixed ``x=d^2``."""

        character = mp.exp(log_character)
        moments = [mp.mpf("0") for _ in range(4)]
        for degree, charge, coefficient in self.active_mp:
            monomial = coefficient * radius**degree * character**charge
            for power in range(4):
                moments[power] += charge**power * monomial

        g = [mp.mpf("0"), mp.mpf(ACTIVE_CHARGE), -mp.mpf(ACTIVE_CHARGE) ** 2]
        g_t = [mp.mpf("0"), mp.mpf("0"), mp.mpf("0")]
        for degree, charge, coefficient in self.zero_mp:
            monomial = coefficient * radius**degree * character**charge
            shifted = abs(charge) - ACTIVE_CHARGE
            g[0] += monomial
            g[1] += shifted * monomial
            g[2] += shifted**2 * monomial
            g_t[0] += charge * monomial
            g_t[1] += charge * shifted * monomial
            g_t[2] += charge * shifted**2 * monomial
        g[0] -= 1

        product = alpha * alpha - x
        active_value = moments[0] + 2 * alpha * moments[1] + product * moments[2] - 1
        zero_value = g[0] + 2 * alpha * g[1] + product * g[2]
        active_t = moments[1] + 2 * alpha * moments[2] + product * moments[3]
        active_alpha = 2 * moments[1] + 2 * alpha * moments[2]
        zero_t = g_t[0] + 2 * alpha * g_t[1] + product * g_t[2]
        zero_alpha = 2 * g[1] + 2 * alpha * g[2]
        stationarity = active_t * zero_alpha - active_alpha * zero_t
        return active_value, zero_value, stationarity

    def localize_symmetric_candidate(self, digits: int) -> dict[str, str]:
        mp.mp.dps = digits

        def equations(radius: mp.mpf, log_character: mp.mpf, alpha: mp.mpf):
            return self.symmetric_equations(
                radius, log_character, alpha, mp.mpf("0")
            )

        root = mp.findroot(
            equations,
            (
                mp.mpf("0.38262891253047284265"),
                mp.log(mp.mpf("0.79280553858639950451")),
                mp.mpf("0.0060515027062626180062"),
            ),
            solver="mdnewton",
            tol=mp.mpf(10) ** (-(digits - 15)),
            maxsteps=100,
        )
        radius, log_character, alpha = root
        character = mp.exp(log_character)
        lam = alpha / (1 - ACTIVE_CHARGE * alpha)
        residual = equations(radius, log_character, alpha)

        def branch_equations(
            radius_value: mp.mpf,
            log_character_value: mp.mpf,
            alpha_value: mp.mpf,
            x_value: mp.mpf,
        ):
            return mp.matrix(
                self.symmetric_equations(
                    radius_value, log_character_value, alpha_value, x_value
                )
            )

        variables = mp.matrix([radius, log_character, alpha])
        jacobian = mp.matrix(3, 3)
        for row in range(3):
            for column in range(3):
                jacobian[row, column] = mp.diff(
                    lambda value, row=row, column=column: branch_equations(
                        value if column == 0 else variables[0],
                        value if column == 1 else variables[1],
                        value if column == 2 else variables[2],
                        mp.mpf("0"),
                    )[row],
                    variables[column],
                )
        x_derivative = mp.matrix(
            [
                mp.diff(
                    lambda value, row=row: branch_equations(
                        variables[0], variables[1], variables[2], value
                    )[row],
                    mp.mpf("0"),
                )
                for row in range(3)
            ]
        )
        branch_derivative = mp.lu_solve(jacobian, -x_derivative)
        return {
            "radius": mp.nstr(radius, digits),
            "character": mp.nstr(character, digits),
            "alpha": mp.nstr(alpha, digits),
            "beta": mp.nstr(alpha, digits),
            "lambda": mp.nstr(lam, digits),
            "mu": mp.nstr(lam, digits),
            "scaledAlpha": mp.nstr(ACTIVE_CHARGE * alpha, digits),
            "maximumAbsoluteResidual": mp.nstr(max(abs(value) for value in residual), 16),
            "radiusDerivativeWithRespectToAntisymmetricSquare": mp.nstr(
                branch_derivative[0], digits
            ),
            "antisymmetricSecondDerivative": mp.nstr(
                2 * branch_derivative[0], digits
            ),
            "classification": "high-precision diagnostic localization only",
        }

    def multistart(self, starts: int, seed: int, progress: bool) -> dict[str, object]:
        generator = np.random.default_rng(seed)
        initial_points = [
            np.asarray(
                [
                    0.38262,
                    math.log(0.7928),
                    math.log(0.9803 / (1 - 0.9803)),
                    math.log(0.9803 / (1 - 0.9803)),
                ]
            )
        ]
        for _ in range(max(0, starts - 1)):
            radius = generator.uniform(0.36, 0.39)
            log_character = generator.uniform(math.log(0.16), math.log(1.15))
            alpha_logit = generator.uniform(-5.0, 7.0)
            beta_logit = generator.uniform(-5.0, 7.0)
            initial_points.append(
                np.asarray([radius, log_character, alpha_logit, beta_logit])
            )

        records: list[dict[str, object]] = []
        for index, initial in enumerate(initial_points, start=1):
            result = minimize(
                lambda point: -point[0],
                initial,
                method="SLSQP",
                bounds=[
                    (0.34, 0.42),
                    (math.log(0.12), math.log(1.50)),
                    (-12.0, 12.0),
                    (-12.0, 12.0),
                ],
                constraints=[
                    {"type": "ineq", "fun": lambda point: self.margins(point)[0]},
                    {"type": "ineq", "fun": lambda point: self.margins(point)[1]},
                ],
                options={"ftol": 2e-14, "maxiter": 1800, "disp": False},
            )
            active_margin, zero_margin = self.margins(result.x)
            u = self.sigmoid(float(result.x[2]))
            v = self.sigmoid(float(result.x[3]))
            record = {
                "index": index,
                "success": bool(result.success),
                "status": int(result.status),
                "radius": float(result.x[0]),
                "character": math.exp(float(result.x[1])),
                "scaledAlpha": u,
                "scaledBeta": v,
                "lambda": u / (ACTIVE_CHARGE * (1 - u)),
                "mu": v / (ACTIVE_CHARGE * (1 - v)),
                "activeMargin": active_margin,
                "zeroMargin": zero_margin,
                "iterations": int(result.nit),
                "objectiveEvaluations": int(result.nfev),
                "message": str(result.message),
            }
            records.append(record)
            if progress and (index == 1 or index % 8 == 0 or index == len(initial_points)):
                best = max(records, key=lambda item: item["radius"])
                print(
                    f"[R0.54 diagnostic] start {index}/{len(initial_points)}; "
                    f"best r={best['radius']:.16f}; "
                    f"u={best['scaledAlpha']:.9f}, v={best['scaledBeta']:.9f}",
                    file=sys.stderr,
                    flush=True,
                )

        converged_feasible = [
            record
            for record in records
            if record["success"]
            and record["activeMargin"] >= -5e-10
            and record["zeroMargin"] >= -5e-10
        ]
        if not converged_feasible:
            raise AssertionError("no multistart run converged to a feasible point")
        best = max(converged_feasible, key=lambda item: item["radius"])
        near_best = [
            record
            for record in converged_feasible
            if best["radius"] - record["radius"] <= 2e-9
        ]

        def basin(record: dict[str, object]) -> str:
            lower = min(record["scaledAlpha"], record["scaledBeta"])
            upper = max(record["scaledAlpha"], record["scaledBeta"])
            if lower > 0.8 and abs(record["scaledAlpha"] - record["scaledBeta"]) < 0.05:
                return "symmetric product interior"
            if lower < 0.1 and upper > 0.8:
                return "single-factor boundary"
            if upper < 0.1:
                return "near character-only boundary"
            return "other"

        basin_counts = Counter(basin(record) for record in converged_feasible)
        basin_best = {
            name: max(
                (record for record in converged_feasible if basin(record) == name),
                key=lambda item: item["radius"],
            )
            for name in basin_counts
        }
        return {
            "starts": starts,
            "seed": seed,
            "successfulRuns": sum(record["success"] for record in records),
            "convergedFeasibleRuns": len(converged_feasible),
            "nearBestRuns": len(near_best),
            "best": best,
            "nearBest": near_best,
            "basinCounts": dict(basin_counts),
            "bestByBasin": basin_best,
            "allRecords": records,
            "classification": "deterministic finite floating-point reconnaissance only",
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--digits", type=int, default=80)
    parser.add_argument("--starts", type=int, default=64)
    parser.add_argument("--seed", type=int, default=54054)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    started = time.perf_counter()
    model = DiagnosticModel.build(arguments.max_total_degree, arguments.progress)
    localization = model.localize_symmetric_candidate(arguments.digits)
    if arguments.progress:
        print(
            "[R0.54 diagnostic] symmetric localization "
            f"r={localization['radius'][:24]}, "
            "d2-radius derivative="
            f"{localization['radiusDerivativeWithRespectToAntisymmetricSquare'][:24]}",
            file=sys.stderr,
            flush=True,
        )
    multistart = model.multistart(arguments.starts, arguments.seed, arguments.progress)
    payload = {
        "schemaVersion": "0.1-diagnostic",
        "scope": {
            "system": "degree-80 reduced canonical edge generating system",
            "purpose": "select R0.54 proof boxes and active sets",
            "notCertified": True,
            "notClaimed": [
                "global optimality of the product-affine family",
                "a floating-point sign theorem",
                "three-dimensional Navier-Stokes regularity or singularity",
            ],
        },
        "invariantReduction": {
            "activeCharge": ACTIVE_CHARGE,
            "variables": ["A=alpha+beta", "B=alpha*beta"],
            "activeConstraint": "F=M0-1+A*M1+B*M2<=0",
            "zeroConstraint": "G=g0+A*g1+B*g2<=0",
            "domain": "0<=A<2/S, max(0,S^-1*(A-S^-1))<B<=A^2/4",
            "symmetricBoundary": "B=A^2/4",
            "classification": "exact algebraic reduction",
        },
        "symmetricCandidate": localization,
        "multistart": multistart,
        "computation": {
            "createdUtc": datetime.now(timezone.utc).isoformat(),
            "python": platform.python_version(),
            "platform": platform.platform(),
            "exactBackend": f"gmpy2 {gmpy2.version()} / GMP {gmpy2.mp_version()}",
            "highPrecisionBackend": f"mpmath {mp.__version__} at {arguments.digits} digits",
            "optimizationBackend": f"SciPy {scipy.__version__} / NumPy {np.__version__}",
            "randomSeed": arguments.seed,
            "randomnessUse": "deterministic start generation only",
            "floatingPointDecisionUse": True,
            "wallSeconds": time.perf_counter() - started,
        },
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
        temporary.write_text(rendered + "\n", encoding="utf-8")
        temporary.replace(arguments.output)
    else:
        print(rendered)


if __name__ == "__main__":
    main()
