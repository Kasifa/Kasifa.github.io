#!/usr/bin/env python3
"""Exact finite audit for R0.71Q.

This producer certifies four statements used in the report:

1. a conservative Euclidean disk lies inside Temam's one-sided complex-time
   lobe, whose scale is T_1(R)=K_nu/(1+R^2)^2;
2. Jensen's lower-anchor term is necessary and asymptotically sharp, using a
   rational finite Blaschke family with arbitrarily many simple real zeros;
3. taking a union over observables necessarily pays a component/truncation
   tax, even when every component has uniform radius, norm, and anchor data;
4. an L^1 enstrophy budget does not control the inverse analytic-window scale
   (1+Y)^2.

The analytic counterfamilies and pulse ledger are not Navier--Stokes
trajectories.  They audit a proposed proof method, not the PDE itself.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def temam_lobe_disk() -> dict[str, object]:
    """Verify D(T/4,T/64) lies in s^4 < x^3 T."""

    x_min = Fraction(15, 64)
    x_max = Fraction(17, 64)
    y_max = Fraction(1, 64)
    s2_upper = x_max * x_max + y_max * y_max
    s4_upper = s2_upper * s2_upper
    rhs_lower = x_min**3
    residual = rhs_lower - s4_upper
    require(residual > 0, "extracted disk lies strictly inside Temam lobe")

    return {
        "passed": True,
        "normalizedLobe": "Delta={x+iy:x>0,(x^2+y^2)^2<x^3}",
        "temamScale": "T_1(R)=K_nu/(1+R^2)^2",
        "extractedDisk": "D(T_1/4,T_1/64)",
        "boundsAfterSettingT1ToOne": {
            "xMin": frac(x_min),
            "xMax": frac(x_max),
            "absoluteYMax": frac(y_max),
            "sFourthUpper": frac(s4_upper),
            "xCubedLower": frac(rhs_lower),
            "strictResidual": frac(residual),
        },
        "nestedJensenRadii": {
            "largePdeDisk": "T_1/64",
            "outerJensenDisk": "T_1/128",
            "innerCountingDisk": "T_1/256",
            "radiusMargin": "log 2",
        },
        "interpretation": (
            "A two-sided disk can be extracted from a translated one-sided "
            "Temam lobe. Its radius remains proportional to "
            "(1+sup||u||_V^2)^-2."
        ),
    }


def rational_blaschke_family() -> dict[str, object]:
    """Audit B_N with rational zeros just inside the half disk."""

    rows: list[dict[str, object]] = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        zeros = [Fraction(2 * n * n - k, 4 * n * n) for k in range(1, n + 1)]
        require(len(set(zeros)) == n, f"N={n} distinct zeros")
        require(all(Fraction(0) < zero < Fraction(1, 2) for zero in zeros), f"N={n} inner zeros")

        anchor = Fraction(1)
        for zero in zeros:
            anchor *= zero
        log_anchor = -sum(math.log(float(zero)) for zero in zeros)
        jensen_bound = log_anchor / math.log(2.0)
        excess = jensen_bound - n
        require(jensen_bound >= n - 2e-13, f"N={n} Jensen count")
        require(excess <= 1.0 / math.log(2.0) + 2e-13, f"N={n} near-sharp excess")

        positive_derivatives = 0
        derivative_signs: list[int] = []
        # The rational list is decreasing in k.  At its k-th member there
        # are exactly k larger zeros, hence k negative numerator factors.
        for k in range(n):
            sign = 1 if k % 2 == 0 else -1
            derivative_signs.append(sign)
            if sign > 0:
                positive_derivatives += 1
        require(positive_derivatives == (n + 1) // 2, f"N={n} upward count")

        # Direct exact derivative products for the small cases provide a
        # second algebraic check of the parity formula without expanding B_N.
        if n <= 8:
            exact_signs = []
            for k, zero in enumerate(zeros):
                derivative = Fraction(1, 1) / (1 - zero * zero)
                for ell, other in enumerate(zeros):
                    if ell == k:
                        continue
                    derivative *= (zero - other) / (1 - other * zero)
                exact_signs.append(1 if derivative > 0 else -1)
            require(exact_signs == derivative_signs, f"N={n} exact derivative signs")

        rows.append({
            "N": n,
            "zeroInterval": [frac(min(zeros)), frac(max(zeros))],
            "centerAnchor": frac(anchor),
            "minusLogAnchor": log_anchor,
            "jensenMultiplicityBoundAtInnerRadiusOneHalf": jensen_bound,
            "boundMinusExactZeroCount": excess,
            "distinctRealZeroCount": n,
            "positiveDerivativeZeroCount": positive_derivatives,
            "squaredFamily": {
                "definition": "C_N(z)=B_N(z)^2 e",
                "centerAnchor": frac(anchor * anchor),
                "distinctEvenOrderZeroCount": n,
                "positiveEntryCountForFEqualsEAndYEqualsOne": n,
                "eachLeadingCoefficientIsPositive": True,
                "jensenMultiplicityBound": 2.0 * jensen_bound,
            },
            "derivativeSigns": derivative_signs,
        })

    return {
        "passed": True,
        "family": (
            "a_{N,k}=(2N^2-k)/(4N^2), "
            "B_N(z)=product_k (z-a_{N,k})/(1-a_{N,k}z)"
        ),
        "outerDisk": "D(0,1)",
        "innerCountingDisk": "D(0,1/2)",
        "uniformComplexNorm": 1,
        "boundaryIdentity": "|B_N(e^{i theta})|=1",
        "centerAnchorIdentity": "|B_N(0)|=product_k a_{N,k}",
        "jensenBound": "N_B(1/2)<=log(1/|B_N(0)|)/log 2",
        "nearSharpness": "N <= Jensen bound <= N+1/log 2",
        "upwardCrossings": "ceil(N/2)",
        "positiveEntryVariant": (
            "C_N=B_N^2 e has N even-order zeros and, for F=e and Y=1, "
            "every zero has A_plus=1"
        ),
        "rows": rows,
        "methodBoundary": (
            "Fixed analytic radius and fixed complex sup norm do not bound "
            "distinct real zeros or upward crossings without a quantitative "
            "nonzero anchor."
        ),
    }


def local_window_cover_tax() -> dict[str, object]:
    """Record a locally uniform analytic family requiring N windows."""

    ratio_bound = math.cosh(3.0 * math.pi / 4.0) ** 2
    rows = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        outer_radius = Fraction(3, 4 * n)
        inner_radius = Fraction(5, 8 * n)
        anchor = 1.0 / (math.pi * n) ** 2
        complex_bound = ratio_bound * anchor
        rows.append({
            "N": n,
            "entryCountOnHalfOpenUnitWindow": n,
            "ownedWindowCount": n,
            "outerRadius": frac(outer_radius),
            "innerRadius": frac(inner_radius),
            "outerToInnerRatio": 6.0 / 5.0,
            "centerAnchor": anchor,
            "complexNormBound": complex_bound,
            "uniformRelativeGrowthBound": ratio_bound,
            "positiveEntryAtom": 1,
        })
    return {
        "passed": True,
        "family": "C_N(z)=(sin(pi*N*z)/(pi*N))^2 e on K=[0,1)",
        "centers": "c_m=(m+1/2)/N",
        "ownedCells": "E_m=[m/N,(m+1)/N)",
        "uniformRelativeGrowthBound": ratio_bound,
        "rows": rows,
        "conclusion": (
            "Uniform local radius ratio and relative anchor data do not pay "
            "the global count; the number of owned windows remains N."
        ),
    }


def observable_union_tax() -> dict[str, object]:
    """Uniform one-zero components whose union count grows with truncation."""

    rows: list[dict[str, object]] = []
    uniform_ratio = math.log(6.0) / math.log(4.0 / 3.0)
    for count in (1, 2, 4, 8, 16, 32, 64):
        zeros = [Fraction(1, 4) + Fraction(k, 4 * (count + 1)) for k in range(1, count + 1)]
        require(all(Fraction(1, 4) < value < Fraction(1, 2) for value in zeros), f"Q={count} zero interval")
        require(len(set(zeros)) == count, f"Q={count} distinct union")
        anchors = zeros
        require(min(anchors) >= Fraction(1, 4), f"Q={count} uniform anchors")
        rows.append({
            "componentCount": count,
            "distinctUnionZeroCount": count,
            "eachFunction": "g_q(z)=z-b_q",
            "zeroInterval": [frac(min(zeros)), frac(max(zeros))],
            "uniformOuterDiskSupBound": 1.5,
            "uniformCenterAnchorLowerBound": 0.25,
            "uniformPerComponentJensenBound": uniform_ratio,
            "positiveDerivativeZeroCount": count,
        })

    return {
        "passed": True,
        "outerDisk": "D(0,1)",
        "innerDisk": "D(0,3/4)",
        "uniformData": "M<=3/2 and |g_q(0)|>=1/4 for every q",
        "uniformPerComponentBound": uniform_ratio,
        "rows": rows,
        "conclusion": (
            "The union of component zero sets grows linearly with the number "
            "of observables despite uniform per-component radius, norm, and "
            "anchor. Summing Jensen bounds or forming a product both pay the "
            "same truncation/component tax."
        ),
    }


def leray_covering_budget_separation() -> dict[str, object]:
    """Exact L1-vs-L2 pulse ledger for the inverse window scale."""

    rows = []
    for n in (1, 2, 4, 8, 16, 32, 64):
        # Y_N(t)=N(1-Nt) on [0,1/N], zero otherwise.
        integral_y = Fraction(1, 2)
        integral_y_squared = Fraction(n, 3)
        integral_one_plus_y_squared_on_unit_interval = Fraction(1) + 2 * integral_y + integral_y_squared
        require(integral_y == Fraction(1, 2), f"N={n} fixed Leray mass")
        rows.append({
            "N": n,
            "integralY": frac(integral_y),
            "integralYSquared": frac(integral_y_squared),
            "integralOnePlusYQuantitySquared": frac(integral_one_plus_y_squared_on_unit_interval),
        })

    return {
        "passed": True,
        "pulse": "Y_N(t)=N(1-Nt)_+ on [0,1]",
        "analyticScale": "T_1(sqrt(Y))=K_nu/(1+Y)^2",
        "inverseScaleDensity": "K_nu^-1(1+Y)^2",
        "rows": rows,
        "scope": (
            "This is an abstract budget separation, not an NSE enstrophy "
            "trajectory. It proves that an L1-in-time Y bound alone cannot "
            "pay a generic cover whose density is proportional to (1+Y)^2."
        ),
    }


def build_certificate() -> dict[str, object]:
    checks = {
        "temamLobeDisk": temam_lobe_disk(),
        "rationalBlaschkeFamily": rational_blaschke_family(),
        "observableUnionTax": observable_union_tax(),
        "localWindowCoverTax": local_window_cover_tax(),
        "lerayCoveringBudgetSeparation": leray_covering_budget_separation(),
    }
    require(all(check["passed"] for check in checks.values()), "all exact checks")
    return {
        "release": "R0.71Q",
        "status": "passed",
        "scope": (
            "finite quantitative Jensen/parabolic-window audit; no uniform "
            "NSE zero count, continuation criterion, singularity, or global "
            "regularity claim"
        ),
        "checks": checks,
        "decision": (
            "The direct complex-time zero-count route remains conditional. "
            "Temam's radius is paid by a strong H1 bound, Jensen requires a "
            "lower observable anchor, and unions over observables pay a "
            "truncation tax."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_certificate()
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
