#!/usr/bin/env python3
"""Deterministic certificate for the R0.73X Gaussian velocity-tail lemma.

This package checks only scalar kernel calculus, Navier--Stokes scaling
bookkeeping, annular geometry, and the concentration exponents used in the
functional counterexamples.  It does not solve or time-step Navier--Stokes.

Run:

  python3 scripts/r073x_gaussian_tail_certificate.py --check-only
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "research" / "r073x_gaussian_tail_certificate.json"
REPORT_PATH = ROOT / "research" / "r073x_gaussian_tail_certificate_report.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def adaptive_simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    tolerance: float = 1.0e-13,
    max_depth: int = 24,
) -> float:
    """Dependency-free adaptive Simpson quadrature on a finite interval."""

    midpoint = 0.5 * (left + right)
    f_left = function(left)
    f_mid = function(midpoint)
    f_right = function(right)
    whole = (right - left) * (f_left + 4.0 * f_mid + f_right) / 6.0

    def recurse(
        a: float,
        b: float,
        fa: float,
        fm: float,
        fb: float,
        estimate: float,
        tol: float,
        depth: int,
    ) -> float:
        middle = 0.5 * (a + b)
        left_middle = 0.5 * (a + middle)
        right_middle = 0.5 * (middle + b)
        flm = function(left_middle)
        frm = function(right_middle)
        left_estimate = (middle - a) * (fa + 4.0 * flm + fm) / 6.0
        right_estimate = (b - middle) * (fm + 4.0 * frm + fb) / 6.0
        refined = left_estimate + right_estimate
        if depth <= 0 or abs(refined - estimate) <= 15.0 * tol:
            return refined + (refined - estimate) / 15.0
        return recurse(
            a,
            middle,
            fa,
            flm,
            fm,
            left_estimate,
            0.5 * tol,
            depth - 1,
        ) + recurse(
            middle,
            b,
            fm,
            frm,
            fb,
            right_estimate,
            0.5 * tol,
            depth - 1,
        )

    return recurse(
        left,
        right,
        f_left,
        f_mid,
        f_right,
        whole,
        tolerance,
        max_depth,
    )


def kernel_ratio(q: float) -> float:
    """Ratio ((|y|/s)g_s)/(s^(-1/2)g_(2s)) for q=|y|/sqrt(s)."""

    return (2.0 ** 1.5) * q * math.exp(-(q * q) / 8.0)


def direct_scale_integral(a: float, theta: float, radius: float) -> float:
    """Numerically integrate int_0^(theta R^2) s^-2 exp(-aR^2/s) ds.

    The substitution s=theta R^2 exp(-r) is used only to make direct
    quadrature stable.  The certified comparison is with the independently
    evaluated closed form exp(-a/theta)/(aR^2).
    """

    def integrand(r_value: float) -> float:
        exponent = r_value - (a / theta) * math.exp(r_value)
        if exponent < -745.0:
            return 0.0
        return math.exp(exponent) / (theta * radius * radius)

    # Beyond r=16 the double-exponential tail is far below binary64 range
    # for every parameter in the declared grid.
    # Use a relative scale set by the endpoint value.  A fixed absolute
    # tolerance would silently accept a poor answer when a/theta is large
    # and the whole integral is exponentially small.
    endpoint_scale = abs(integrand(0.0))
    tolerance = max(5.0e-324, endpoint_scale * 1.0e-13)
    return adaptive_simpson(integrand, 0.0, 16.0, tolerance=tolerance)


def smooth_bump(value: float) -> tuple[float, float, float]:
    """Return a standard C-infinity bump and its first two derivatives."""

    if abs(value) >= 1.0:
        return 0.0, 0.0, 0.0
    denominator = 1.0 - value * value
    logarithmic_first = -2.0 * value / (denominator * denominator)
    logarithmic_second = (
        -2.0 / (denominator * denominator)
        - 8.0 * value * value / (denominator * denominator * denominator)
    )
    bump = math.exp(-1.0 / denominator)
    first = bump * logarithmic_first
    second = bump * (logarithmic_first * logarithmic_first + logarithmic_second)
    return bump, first, second


def packet_integrals(delta: float, nodes: int = 32) -> dict[str, float]:
    """Directly integrate an explicit scaled divergence-free packet.

    The physical cube and mesh are rebuilt for every delta.  No scaling
    exponent is used in the quadrature.  A smooth positive radial weight is
    included, so the recovered slopes are asymptotic rather than identities
    inserted by construction.
    """

    require(delta > 0.0 and nodes >= 8, "invalid packet quadrature parameters")
    alpha = 0.35
    step = 2.0 * delta / nodes
    weighted_l2 = 0.0
    weighted_l3 = 0.0
    weighted_gradient_l2 = 0.0
    moment = [0.0, 0.0, 0.0]
    for i in range(nodes):
        physical_x = -delta + (i + 0.5) * step
        x = physical_x / delta
        f, fp, fpp = smooth_bump(x)
        for j in range(nodes):
            physical_y = -delta + (j + 0.5) * step
            y = physical_y / delta
            base_y, base_y_first, base_y_second = smooth_bump(y)
            g = base_y * (1.0 + alpha * y)
            gp = base_y_first * (1.0 + alpha * y) + alpha * base_y
            gpp = base_y_second * (1.0 + alpha * y) + 2.0 * alpha * base_y_first
            for k in range(nodes):
                physical_z = -delta + (k + 0.5) * step
                z = physical_z / delta
                h, hp, _ = smooth_bump(z)

                u1 = f * gp * h
                u2 = -fp * g * h
                norm_squared = u1 * u1 + u2 * u2
                norm = math.sqrt(norm_squared)

                inverse_delta = 1.0 / delta
                gradient_squared = inverse_delta * inverse_delta * (
                    (fp * gp * h) ** 2
                    + (f * gpp * h) ** 2
                    + (f * gp * hp) ** 2
                    + (fpp * g * h) ** 2
                    + (fp * gp * h) ** 2
                    + (fp * g * hp) ** 2
                )
                weight = math.exp(
                    -0.2
                    * (
                        physical_x * physical_x
                        + physical_y * physical_y
                        + physical_z * physical_z
                    )
                )
                cell = step * step * step
                weighted_l2 += cell * weight * norm_squared
                weighted_l3 += cell * weight * norm_squared * norm
                weighted_gradient_l2 += cell * weight * gradient_squared
                moment[0] += cell * u1 * norm_squared
                moment[1] += cell * u2 * norm_squared

    require(weighted_l2 > 0.0 and weighted_l3 > 0.0, "zero packet norm")
    require(weighted_gradient_l2 > 0.0, "zero packet gradient")
    return {
        "delta": delta,
        "weighted_L2": weighted_l2,
        "weighted_L2_to_three_halves": weighted_l2 ** 1.5,
        "weighted_L3": weighted_l3,
        "ratio": weighted_l3 / (weighted_l2 ** 1.5),
        "weighted_gradient_L2": weighted_gradient_l2,
        "moment_component_1": moment[0],
        "moment_component_2": moment[1],
    }


def consecutive_slopes(rows: list[dict[str, float]], key: str) -> list[float]:
    slopes: list[float] = []
    for left, right in zip(rows, rows[1:]):
        slopes.append(
            math.log(left[key] / right[key])
            / math.log(left["delta"] / right["delta"])
        )
    return slopes


def generate() -> dict[str, Any]:
    analytic_maximizer = 2.0
    analytic_kernel_constant = (2.0 ** 2.5) * math.exp(-0.5)
    grid_values = [kernel_ratio(index / 4096.0) for index in range(16 * 4096 + 1)]
    grid_maximum = max(grid_values)
    grid_argmax = grid_values.index(grid_maximum) / 4096.0
    require(abs(grid_argmax - analytic_maximizer) <= 1.0 / 4096.0, "kernel maximizer mismatch")
    require(grid_maximum <= analytic_kernel_constant * (1.0 + 2.0e-15), "kernel bound failed")

    first_moment_constant = 4.0 / math.sqrt(math.pi)
    pointwise_constant = analytic_kernel_constant + (2.0 ** 1.5) * first_moment_constant
    require(pointwise_constant < 10.0, "unexpected pointwise constant")

    integral_rows: list[dict[str, float | int]] = []
    maximum_relative_error = 0.0
    for theta in (1.0, 0.5, 0.25, 0.125):
        for radius in (0.125, 0.25, 0.75):
            for annulus_index in (1, 2, 3, 4):
                a = (4.0 ** annulus_index) / 32.0
                numerical = direct_scale_integral(a, theta, radius)
                closed_form = math.exp(-a / theta) / (a * radius * radius)
                relative_error = abs(numerical - closed_form) / closed_form
                maximum_relative_error = max(maximum_relative_error, relative_error)
                integral_rows.append(
                    {
                        "annulus_index": annulus_index,
                        "theta": theta,
                        "radius": radius,
                        "numerical": numerical,
                        "closed_form": closed_form,
                        "relative_error": relative_error,
                    }
                )
    require(maximum_relative_error < 5.0e-11, "scale-integral quadrature mismatch")

    # Degree means the exponent of lambda under u_lambda=lambda*u(lambda^2t,lambda*x).
    degrees = {
        "u": Fraction(1),
        "u_cubed": Fraction(3),
        "S": Fraction(4),
        "s": Fraction(-2),
        "dx": Fraction(-3),
        "dt": Fraction(-2),
        "R_inverse_cubed": Fraction(3),
    }
    tent_degree = (
        degrees["S"]
        + degrees["s"]
        + degrees["dx"]
        + degrees["dt"]
        + degrees["R_inverse_cubed"]
    )
    tail_degree = (
        Fraction(1)  # s^{-1/2}
        + degrees["u_cubed"]
        + degrees["s"]
        + degrees["dx"]
        + degrees["dt"]
        + degrees["R_inverse_cubed"]
    )
    require(tent_degree == 0, "absolute tent scaling is not invariant")
    require(tail_degree == 0, "exact velocity-tail scaling is not invariant")

    annular_geometry_rows = []
    for annulus_index in range(1, 65):
        left = (2 ** annulus_index) - 1
        right = 2 ** (annulus_index - 1)
        require(left >= right, "annular distance inequality failed")
        annular_geometry_rows.append(
            {
                "annulus_index": annulus_index,
                "two_to_m_minus_one": left,
                "two_to_m_minus_one_lower_bound": right,
            }
        )

    heat_ball_coefficient = (4.0 * math.pi / 3.0) * ((8.0 * math.pi) ** -1.5)
    heat_ball_closed = 1.0 / (12.0 * math.sqrt(2.0 * math.pi))
    annular_assembly = 32.0 * heat_ball_coefficient
    annular_assembly_closed = 8.0 / (3.0 * math.sqrt(2.0 * math.pi))
    core_left = Fraction(2, 1)
    core_right = Fraction(8, 1) * Fraction(1, 4)
    require(abs(heat_ball_coefficient - heat_ball_closed) < 2.0e-17, "heat-ball constant failed")
    require(abs(annular_assembly - annular_assembly_closed) < 3.0e-16, "annular assembly failed")
    require(core_left == core_right, "core coefficient assembly failed")

    # Derive packet powers from the declared ambient dimension; no exponent
    # below is entered as an independent literal.
    dimension = Fraction(3, 1)
    packet_exponents = {
        "weighted_L3": dimension,
        "weighted_L2_to_three_halves": Fraction(3, 2) * dimension,
        "ratio_L3_over_L2_to_three_halves": -Fraction(1, 2) * dimension,
        "gradient_L2": dimension - 2,
    }
    require(
        packet_exponents["weighted_L3"]
        - packet_exponents["weighted_L2_to_three_halves"]
        == packet_exponents["ratio_L3_over_L2_to_three_halves"],
        "packet concentration exponent mismatch",
    )

    packet_rows = [
        packet_integrals(delta)
        for delta in (0.25, 0.125, 0.0625, 0.03125, 0.015625)
    ]
    packet_numeric_slopes = {
        "weighted_L3": consecutive_slopes(packet_rows, "weighted_L3"),
        "weighted_L2_to_three_halves": consecutive_slopes(
            packet_rows, "weighted_L2_to_three_halves"
        ),
        "ratio_L3_over_L2_to_three_halves": consecutive_slopes(packet_rows, "ratio"),
        "gradient_L2": consecutive_slopes(packet_rows, "weighted_gradient_L2"),
    }
    for key, expected in packet_exponents.items():
        observed = packet_numeric_slopes[key][-1]
        require(abs(observed - float(expected)) < 2.0e-3, f"packet slope mismatch: {key}")
    require(
        abs(packet_rows[0]["moment_component_1"]) > 1.0e-12,
        "explicit packet has zero numerical cubic moment",
    )

    # Derive the viscosity and radius powers in the local energy interpolation
    # from the three-dimensional L^3 interpolation parameter.
    target_q = Fraction(3, 1)
    interpolation_alpha = dimension * (Fraction(1, 2) - 1 / target_q)
    gradient_norm_power = target_q * interpolation_alpha
    gradient_energy_power = gradient_norm_power / 2
    mass_energy_power = target_q * (1 - interpolation_alpha) / 2
    time_length_power = 1 - gradient_energy_power
    viscosity_power = -gradient_energy_power
    radius_power = (
        mass_energy_power + gradient_energy_power + 2 * time_length_power
    )
    require(interpolation_alpha == Fraction(1, 2), "interpolation alpha mismatch")
    require(viscosity_power == Fraction(-3, 4), "viscosity exponent mismatch")
    require(radius_power == 2, "interpolation radius exponent mismatch")

    tail_series: dict[str, dict[str, float]] = {}
    for theta in (1.0, 0.25, 0.0625):
        terms = [math.exp(-(4.0 ** index) / (32.0 * theta)) for index in range(1, 9)]
        tail_series[str(theta)] = {
            "first_term": terms[0],
            "partial_sum_8": sum(terms),
            "last_term": terms[-1],
        }
        require(terms == sorted(terms, reverse=True), "tail weights are not decreasing")

    # Prove a summable majorant for the worst allowed exponential c=1/32.
    worst_c = 1.0 / 32.0
    summability_threshold = None
    for annulus_index in range(1, 65):
        log_comparison = 0.5 * worst_c * (4.0 ** annulus_index) - annulus_index * math.log(2.0)
        next_increment = 1.5 * worst_c * (4.0 ** annulus_index) - math.log(2.0)
        if log_comparison >= 0.0 and next_increment >= 0.0:
            summability_threshold = annulus_index
            break
    require(summability_threshold is not None, "no lifted-tail summability threshold")
    for annulus_index in range(summability_threshold, summability_threshold + 32):
        require(
            annulus_index * math.log(2.0)
            <= 0.5 * worst_c * (4.0 ** annulus_index),
            "polynomial/exponential comparison failed",
        )
    geometric_ratio = math.exp(
        -1.5 * worst_c * (4.0 ** summability_threshold)
    )
    require(0.0 < geometric_ratio < 1.0, "invalid geometric tail ratio")

    payload: dict[str, Any] = {
        "schema": "r073x-gaussian-tail-certificate-v2",
        "claim_boundary": {
            "navier_stokes_time_step": False,
            "pde_regularization": False,
            "clay_conclusion": "OPEN",
            "scope": "scalar Gaussian calculus and functional scaling only",
        },
        "kernel_domination": {
            "analytic_argmax_q": analytic_maximizer,
            "analytic_constant": analytic_kernel_constant,
            "grid_argmax_q": grid_argmax,
            "grid_maximum": grid_maximum,
            "first_moment_constant": first_moment_constant,
            "combined_pointwise_constant": pointwise_constant,
            "status": "PASS",
        },
        "scale_integral": {
            "identity": "int_0^(theta*R^2) s^-2 exp(-a*R^2/s) ds = exp(-a/theta)/(a*R^2)",
            "maximum_relative_error": maximum_relative_error,
            "rows": integral_rows,
            "status": "PASS",
        },
        "annular_geometry": {
            "distance_rows": annular_geometry_rows,
            "heat_ball_coefficient": heat_ball_coefficient,
            "heat_ball_closed_form": heat_ball_closed,
            "annular_assembly": annular_assembly,
            "annular_assembly_closed_form": annular_assembly_closed,
            "core_coefficient_identity": f"{core_left}={core_right}",
            "status": "PASS",
        },
        "scaling": {
            "absolute_tent_degree": str(tent_degree),
            "exact_velocity_tail_degree": str(tail_degree),
            "status": "PASS",
        },
        "packet_concentration": {
            "dimension": str(dimension),
            "derived_exponents": {
                key: str(value) for key, value in packet_exponents.items()
            },
            "numeric_rows": packet_rows,
            "numeric_slopes": packet_numeric_slopes,
            "status": "PASS",
        },
        "energy_interpolation": {
            "target_q": str(target_q),
            "interpolation_alpha": str(interpolation_alpha),
            "mass_energy_power": str(mass_energy_power),
            "gradient_energy_power": str(gradient_energy_power),
            "time_length_power": str(time_length_power),
            "viscosity_power": str(viscosity_power),
            "radius_power": str(radius_power),
            "status": "PASS",
        },
        "lifted_tail_summability": {
            "worst_c": worst_c,
            "threshold": summability_threshold,
            "geometric_ratio_from_threshold": geometric_ratio,
            "comparison": "2^m exp(-c 4^m) <= exp(-(c/2)4^m)",
            "status": "PASS",
        },
        "tail_series": tail_series,
        "overall": "PASS",
    }
    digest_payload = canonical(payload).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(digest_payload).hexdigest()
    return payload


def render_report(payload: dict[str, Any]) -> str:
    kernel = payload["kernel_domination"]
    integral = payload["scale_integral"]
    packet = payload["packet_concentration"]
    annular = payload["annular_geometry"]
    interpolation = payload["energy_interpolation"]
    numeric_slopes = packet["numeric_slopes"]
    exponents = packet["derived_exponents"]
    return f"""# R0.73X Gaussian velocity-tail scalar certificate

**Status:** `{payload['overall']}`

**Scope:** scalar Gaussian kernel domination, scale integration, NSE degree
bookkeeping, and translated-packet concentration powers.  This is not a PDE
simulation, regularity theorem, or Clay conclusion.

## Reproduction

```bash
python3 scripts/r073x_gaussian_tail_certificate.py --check-only
```

## Certified rows

- Kernel ratio maximum: `q={kernel['analytic_argmax_q']}` with constant
  `{kernel['analytic_constant']:.17g}`; the deterministic grid maximum is
  `{kernel['grid_maximum']:.17g}`.
- A fully explicit admissible pointwise constant in
  `|S_s| <= C s^(-1/2) P_(2s)(|u|^3)` is
  `{kernel['combined_pointwise_constant']:.17g}`.
- Direct quadrature versus the closed scale-integral formula has maximum
  relative error `{integral['maximum_relative_error']:.3e}` on the declared
  48-case grid.
- Annular distance, heat-ball coefficient
  `{annular['heat_ball_coefficient']:.17g}`, and final coefficient
  `{annular['annular_assembly']:.17g}` are assembled independently.
- Both the absolute tent and exact exterior-tail functionals have NSE scaling
  degree zero.
- A shrinking remote packet has derived `L3` power `{exponents['weighted_L3']}` and
  weighted-`L2`-to-`3/2` power
  `{exponents['weighted_L2_to_three_halves']}`; their ratio has power
  `{exponents['ratio_L3_over_L2_to_three_halves']}`.  Direct packet quadrature
  recovers final consecutive slopes
  `{numeric_slopes['weighted_L3'][-1]:.9f}`,
  `{numeric_slopes['weighted_L2_to_three_halves'][-1]:.9f}`, and
  `{numeric_slopes['ratio_L3_over_L2_to_three_halves'][-1]:.9f}`.
- The energy interpolation independently gives viscosity power
  `{interpolation['viscosity_power']}` and radius power
  `{interpolation['radius_power']}`; the lifted polynomial tail is bounded by
  a geometric super-exponential majorant.

`payload_sha256={payload['payload_sha256']}`

NOT CLAY.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="run every check without rewriting stored artifacts",
    )
    arguments = parser.parse_args()
    payload = generate()
    if not arguments.check_only:
        RESULT_PATH.write_text(canonical(payload), encoding="utf-8")
        REPORT_PATH.write_text(render_report(payload), encoding="utf-8")
    print("R073X_GAUSSIAN_KERNEL=PASS")
    print("R073X_SCALE_INTEGRAL=PASS")
    print("R073X_ANNULAR_GEOMETRY=PASS")
    print("R073X_SCALING=PASS")
    print("R073X_PACKET_NUMERIC_SLOPES=PASS")
    print("R073X_INTERPOLATION_AND_LIFT=PASS")
    print("R073X_PACKET_L2_TAIL=REFUTED_FUNCTIONALLY")
    print("R073X_PDE_REGULARITY=OPEN")
    print("R073X_CLAY=OPEN")
    print(f"R073X_PAYLOAD_SHA256={payload['payload_sha256']}")


if __name__ == "__main__":
    main()
