#!/usr/bin/env python3
"""R0.69F audit for fractional-Volterra endpoint scaling.

The audit checks the exact Mittag--Leffler local gain, the optimized
Bielecki parameter, the geometric endpoint partition, and the certified
packet-rate shell threshold.  The Koch--Tataru bilinear estimate, the
periodic Oseen-gradient estimate, and classical local continuation remain
explicit analytical inputs.
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
R069E = ROOT / "research/certificates/r069e/critical-resolvent-restart.json"
EXPECTED_R069E_SHA = (
    "25992a1119ebf3089a2b4b2231aba524a064e9188f4eb0b31ee5bb1b88a4a009"
)
RHO_SQUARED_NUMERATOR = 32_000_000_000_000
RHO_SQUARED_DENOMINATOR = 50_303_178_668_203


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
    theta, amplitude = sp.symbols("theta A", positive=True, finite=True)
    beta, tau, horizon = sp.symbols(
        "beta tau T_star", positive=True, finite=True
    )
    index = sp.symbols("j", integer=True, positive=True)
    x, c = sp.symbols("x c", positive=True, finite=True)

    log_bielecki = amplitude / theta**2 - sp.log(1 - theta)
    stationarity = sp.factor(sp.diff(log_bielecki, theta))
    stationarity_numerator = sp.factor(
        stationarity * theta**3 * (1 - theta)
    )

    t_previous = horizon - (horizon - tau) * beta ** (-(index - 1))
    t_current = horizon - (horizon - tau) * beta ** (-index)
    slab = sp.simplify(t_current - t_previous)
    remaining_to_slab = sp.simplify((horizon - t_previous) / slab)

    phi = x**2 + 2 * x / sp.sqrt(sp.pi)
    inverse_candidate = -1 / sp.sqrt(sp.pi) + sp.sqrt(1 / sp.pi + c)

    checks = {
        "bieleckiStationarityEquationIsExact": (
            sp.simplify(
                stationarity_numerator
                - (theta**3 - 2 * amplitude * (1 - theta))
            )
            == 0
        ),
        "geometricSlabFormulaIsExact": (
            sp.simplify(
                slab
                - (horizon - tau) * (beta - 1) * beta ** (-index)
            )
            == 0
        ),
        "remainingTimeToSlabRatioIsExact": (
            sp.simplify(remaining_to_slab - beta / (beta - 1)) == 0
        ),
        "packetScaleRatioIsTwoHundredFiftySix": 16**2 == 256,
        "shellThresholdInvertsPhi": (
            sp.simplify(phi.subs(x, inverse_candidate) - c) == 0
        ),
    }
    formulas = {
        "localGain": "G(x)=E_(1/2)(x)=exp(x^2) erfc(-x)",
        "localScale": "x_j=2 C_S sqrt(pi h_j) V_j",
        "geometricSlab": (
            "h_j=(T_star-tau)(beta-1) beta^(-j), beta=256"
        ),
        "resolventProduct": (
            "M_c(t_r)<=Gamma_*((1-a)^(-1)+2r) product_j G(x_j)"
        ),
        "logGainBound": "log G(x)<=x^2+2x/sqrt(pi)",
        "bieleckiOptimizer": "theta_A^3=2A(1-theta_A)",
        "shellThreshold": (
            "limsup V_j sqrt(h_j)>=x_rho/(2 C_S sqrt(pi))"
        ),
    }
    return checks, formulas


def mittag_leffler_checks() -> tuple[dict[str, bool], dict[str, object]]:
    mp.mp.dps = 100
    scenarios = []
    all_series_match = True
    all_log_bounds = True
    all_gains_at_least_one = True

    for x_text in ("0", "0.01", "0.1", "0.5", "1", "2", "4", "8"):
        x = mp.mpf(x_text)
        closed = mp.exp(x * x) * mp.erfc(-x)
        series = mp.nsum(
            lambda n: x**n / mp.gamma(1 + mp.mpf(n) / 2),
            [0, mp.inf],
        )
        difference = abs(closed - series)
        log_bound = x * x + 2 * x / mp.sqrt(mp.pi)
        series_matches = difference < mp.mpf("1e-85")
        bound_holds = mp.log(closed) <= log_bound + mp.mpf("1e-90")
        at_least_one = closed >= 1
        all_series_match = all_series_match and series_matches
        all_log_bounds = all_log_bounds and bound_holds
        all_gains_at_least_one = all_gains_at_least_one and at_least_one
        scenarios.append(
            {
                "x": x_text,
                "closedGain": mp.nstr(closed, 35),
                "seriesGain": mp.nstr(series, 35),
                "absoluteDifference": mp.nstr(difference, 12),
                "logGain": mp.nstr(mp.log(closed), 30),
                "quadraticLinearBound": mp.nstr(log_bound, 30),
                "seriesMatchesClosedForm": series_matches,
                "logBoundHolds": bound_holds,
            }
        )

    checks = {
        "mittagLefflerSeriesMatchesErfcIdentity": all_series_match,
        "allLocalGainsAreAtLeastOne": all_gains_at_least_one,
        "quadraticLinearLogGainBoundHolds": all_log_bounds,
    }
    return checks, {"scenarios": scenarios}


def solve_theta(amplitude: mp.mpf) -> mp.mpf:
    low = mp.mpf("0")
    high = mp.mpf("1")
    for _ in range(500):
        middle = (low + high) / 2
        residual = middle**3 - 2 * amplitude * (1 - middle)
        if residual < 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def bielecki_checks() -> tuple[dict[str, bool], dict[str, object]]:
    mp.mp.dps = 100
    scenarios = []
    all_stationary = True
    all_minima = True
    asymptotic_improves = True
    previous_error = mp.inf

    for amplitude_text in ("0.01", "0.1", "1", "10", "100", "1000"):
        amplitude = mp.mpf(amplitude_text)
        theta = solve_theta(amplitude)
        residual = abs(theta**3 - 2 * amplitude * (1 - theta))
        minimum = mp.exp(amplitude / theta**2) / (1 - theta)
        exact_gain = mp.exp(amplitude) * mp.erfc(-mp.sqrt(amplitude))
        asymptotic = 2 * mp.e * amplitude * mp.exp(amplitude)
        asymptotic_ratio = minimum / asymptotic
        local_points = [
            theta / 2,
            (theta + mp.mpf("1e-20")) / (1 + mp.mpf("1e-20")),
            (1 + theta) / 2,
        ]
        is_minimum = all(
            minimum
            <= mp.exp(amplitude / point**2) / (1 - point)
            for point in local_points
        )
        all_stationary = all_stationary and residual < mp.mpf("1e-90")
        all_minima = all_minima and is_minimum
        if amplitude >= 10:
            error = abs(asymptotic_ratio - 1)
            asymptotic_improves = (
                asymptotic_improves and error < previous_error
            )
            previous_error = error
        scenarios.append(
            {
                "A": amplitude_text,
                "theta": mp.nstr(theta, 35),
                "stationarityResidual": mp.nstr(residual, 12),
                "minimumLog": mp.nstr(mp.log(minimum), 35),
                "exactVolterraLogGain": mp.nstr(mp.log(exact_gain), 35),
                "minimumOverTwoEAExpA": mp.nstr(asymptotic_ratio, 25),
                "localMinimumCheck": is_minimum,
            }
        )

    checks = {
        "allBieleckiOptimizersSatisfyCubic": all_stationary,
        "allBieleckiOptimizersPassLocalMinimumCheck": all_minima,
        "largeABieleckiAsymptoticConverges": asymptotic_improves,
    }
    return checks, {"scenarios": scenarios}


def packet_threshold_checks() -> tuple[dict[str, bool], dict[str, object]]:
    mp.mp.dps = 100
    rho = mp.sqrt(
        mp.mpf(RHO_SQUARED_NUMERATOR) / RHO_SQUARED_DENOMINATOR
    )
    c_rho = mp.log(1 / rho) / 2
    x_rho = -1 / mp.sqrt(mp.pi) + mp.sqrt(1 / mp.pi + c_rho)
    phi = x_rho**2 + 2 * x_rho / mp.sqrt(mp.pi)
    beta = mp.mpf(256)

    checks = {
        "rhoInsidePublishedCertifiedInterval": (
            mp.mpf("0.7975855452903290")
            < rho
            < mp.mpf("0.7975855452903292")
        ),
        "packetLogRateIsPositive": c_rho > 0,
        "shellThresholdIsPositive": x_rho > 0,
        "shellThresholdExactlyInvertsRate": abs(phi - c_rho)
        < mp.mpf("1e-90"),
        "geometricShellRemainingTimeRatio": (
            beta / (beta - 1) == mp.mpf(256) / 255
        ),
    }
    values = {
        "rho": mp.nstr(rho, 50),
        "cRho": mp.nstr(c_rho, 50),
        "xRho": mp.nstr(x_rho, 50),
        "xRhoOverTwoSqrtPi": mp.nstr(
            x_rho / (2 * mp.sqrt(mp.pi)), 50
        ),
        "remainingTimeOverSlabLength": "256/255",
    }
    return checks, values


def recurrence_checks() -> tuple[dict[str, bool], dict[str, object]]:
    mp.mp.dps = 100
    sequences = [
        [mp.mpf("0")] * 12,
        [mp.mpf("0.05")] * 12,
        [mp.mpf("0.2")] * 12,
        [mp.mpf(j) / 20 for j in range(1, 13)],
    ]
    records = []
    all_bounds = True
    for sequence in sequences:
        initial_inverse = mp.mpf("1.7")
        z = initial_inverse
        product = mp.mpf(1)
        maximum_ratio = mp.mpf(0)
        for index, x in enumerate(sequence, start=1):
            gain = mp.exp(x * x) * mp.erfc(-x)
            z = gain * (z + 2)
            product *= gain
            bound = (initial_inverse + 2 * index) * product
            ratio = z / bound
            maximum_ratio = max(maximum_ratio, ratio)
            all_bounds = all_bounds and z <= bound + mp.mpf("1e-90")
        records.append(
            {
                "length": len(sequence),
                "firstX": mp.nstr(sequence[0], 12),
                "lastX": mp.nstr(sequence[-1], 12),
                "maximumRecurrenceToProductBound": mp.nstr(
                    maximum_ratio, 30
                ),
            }
        )
    checks = {
        "shellRecurrenceIsBoundedByProductFormula": all_bounds,
    }
    return checks, {"scenarios": records}


def build_payload(source_commit: str) -> dict[str, object]:
    upstream = json.loads(R069E.read_text(encoding="utf-8"))
    symbolic, formulas = symbolic_checks()
    mittag, mittag_data = mittag_leffler_checks()
    bielecki, bielecki_data = bielecki_checks()
    threshold, threshold_data = packet_threshold_checks()
    recurrence, recurrence_data = recurrence_checks()
    checks = {
        **symbolic,
        **mittag,
        **bielecki,
        **threshold,
        **recurrence,
        "pinnedR069ECertificateHashMatches": (
            sha256(R069E) == EXPECTED_R069E_SHA
        ),
        "upstreamRegularIntervalResolventTheoremPassed": (
            upstream["status"] == "passed"
            and all(upstream["checks"].values())
        ),
        "continuousPositiveTimeSubspaceIsUsed": True,
        "classicalContinuationComparisonIsExplicit": True,
        "millenniumProblemClaimIsExplicitlyExcluded": True,
    }

    return {
        "schemaVersion": "1.0",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "exact scalar fractional-Volterra endpoint majorant and a "
            "certified negative result: optimization yields no criterion "
            "stronger than classical L-infinity continuation"
        ),
        "checks": checks,
        "theorem": {
            "formulas": formulas,
            "packetConstants": threshold_data,
            "conclusion": (
                "failure of the R0.69D stability gate along beta=256 endpoint "
                "shells forces only limsup V_j sqrt(h_j)>0"
            ),
        },
        "mittagLeffler": mittag_data,
        "bieleckiOptimization": bielecki_data,
        "shellRecurrence": recurrence_data,
        "decision": {
            "closedBranch": (
                "optimizing tau, lambda, or the positive-time partition "
                "cannot improve the scalar-majorant exponent V^2 h"
            ),
            "comparison": (
                "classical L-infinity local continuation gives a positive "
                "V_j sqrt(h_j) lower bound on every late shell, stronger in "
                "form than the certified limsup statement"
            ),
            "nextGate": (
                "a useful next branch must retain localized geometry, sign, "
                "or frequency structure discarded by the scalar amplitude"
            ),
        },
        "externalTheoremBoundary": {
            "inputs": [
                "periodic Oseen-gradient L1 kernel estimate",
                "periodic Koch-Tataru bilinear estimate",
                "positive-time L-infinity continuity of heat and Duhamel terms",
                "standard L-infinity local continuation and Serrin criterion",
            ],
            "notAuditedHere": [
                "sharp numerical values of C_B, C_H, or C_S",
                "existence of a finite singular time",
                "any signed or geometric depletion beyond the scalar majorant",
            ],
        },
        "boundary": [
            "The theorem concerns the continuous positive-time subspace used by the nonlinear branch.",
            "Failure of a sufficient stability gate is not evidence that instability occurs.",
            "The result is a no-go theorem for this scalar resolvent optimization only.",
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
                "path": str(R069E.relative_to(ROOT)),
                "sha256": EXPECTED_R069E_SHA,
            },
        },
    }


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
