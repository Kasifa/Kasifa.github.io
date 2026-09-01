#!/usr/bin/env python3
"""R0.73X finite Fourier falsification and tent-slice harness.

The exact channel uses Gaussian-rational q-polynomials, q=exp(-s).  The
numerical channel is deliberately narrower: deterministic Fourier-grid and
Gauss-Legendre quadrature compares signed and spatially absolute *static*
scale slices.  It is not interval arithmetic and it does not evolve NSE.

Run with the bundled workspace Python (NumPy is required only for the
converged absolute-value quadrature):

  /Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
    scripts/r073x_finite_fourier_harness.py
"""

from __future__ import annotations

import argparse
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

try:
    import numpy as np
except ModuleNotFoundError as exc:  # pragma: no cover - explicit operator aid
    raise SystemExit(
        "NumPy is required. Run with the bundled workspace Python shown in "
        "the module docstring."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "research" / "r073x_finite_fourier_harness_results.json"
REPORT_PATH = ROOT / "research" / "r073x_finite_fourier_harness_report.md"

F = Fraction
Mode = tuple[int, int, int]
Gaussian = tuple[Fraction, Fraction]
Poly = dict[int, Gaussian]
Field = dict[Mode, Poly]
VectorField = list[Field]

ZERO_MODE: Mode = (0, 0, 0)
ZERO: Gaussian = (F(0), F(0))
HALF = F(1, 2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def g(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return F(real), F(imag)


def gadd(a: Gaussian, b: Gaussian) -> Gaussian:
    return a[0] + b[0], a[1] + b[1]


def gneg(a: Gaussian) -> Gaussian:
    return -a[0], -a[1]


def gmul(a: Gaussian, b: Gaussian) -> Gaussian:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gconj(a: Gaussian) -> Gaussian:
    return a[0], -a[1]


def gscale(a: Gaussian, value: int | Fraction) -> Gaussian:
    return a[0] * value, a[1] * value


def pclean(a: Poly) -> Poly:
    return {power: value for power, value in a.items() if value != ZERO}


def pconst(value: Gaussian) -> Poly:
    return {} if value == ZERO else {0: value}


def padd(a: Poly, b: Poly) -> Poly:
    result = dict(a)
    for power, value in b.items():
        result[power] = gadd(result.get(power, ZERO), value)
    return pclean(result)


def pneg(a: Poly) -> Poly:
    return {power: gneg(value) for power, value in a.items()}


def pscale(a: Poly, value: Gaussian) -> Poly:
    return pclean({power: gmul(coefficient, value) for power, coefficient in a.items()})


def pmul(a: Poly, b: Poly) -> Poly:
    result: Poly = {}
    for left_power, left_value in a.items():
        for right_power, right_value in b.items():
            power = left_power + right_power
            result[power] = gadd(
                result.get(power, ZERO), gmul(left_value, right_value)
            )
    return pclean(result)


def pshift(a: Poly, count: int) -> Poly:
    return {power + count: value for power, value in a.items()}


def fclean(a: Field) -> Field:
    return {mode: pclean(poly) for mode, poly in a.items() if pclean(poly)}


def fadd(a: Field, b: Field) -> Field:
    result = {mode: dict(poly) for mode, poly in a.items()}
    for mode, poly in b.items():
        result[mode] = padd(result.get(mode, {}), poly)
    return fclean(result)


def fneg(a: Field) -> Field:
    return {mode: pneg(poly) for mode, poly in a.items()}


def fscale(a: Field, value: Gaussian) -> Field:
    return fclean({mode: pscale(poly, value) for mode, poly in a.items()})


def mode_add(a: Mode, b: Mode) -> Mode:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def mode_neg(a: Mode) -> Mode:
    return -a[0], -a[1], -a[2]


def norm2(a: Mode) -> int:
    return a[0] * a[0] + a[1] * a[1] + a[2] * a[2]


def fmul(a: Field, b: Field) -> Field:
    result: Field = {}
    for left_mode in sorted(a):
        for right_mode in sorted(b):
            mode = mode_add(left_mode, right_mode)
            result[mode] = padd(
                result.get(mode, {}), pmul(a[left_mode], b[right_mode])
            )
    return fclean(result)


def heat(a: Field) -> Field:
    return {mode: pshift(poly, norm2(mode)) for mode, poly in a.items()}


def derivative(a: Field, coordinate: int) -> Field:
    return fclean(
        {
            mode: pscale(poly, g(0, mode[coordinate]))
            for mode, poly in a.items()
            if mode[coordinate] != 0
        }
    )


def divergence(a: VectorField) -> Field:
    result: Field = {}
    for coordinate in range(3):
        result = fadd(result, derivative(a[coordinate], coordinate))
    return result


def vector_neg(a: VectorField) -> VectorField:
    return [fneg(component) for component in a]


def navier_stokes_rescale(a: VectorField, frequency: int) -> VectorField:
    """Return frequency*u(frequency*x), the unit-amplitude NSE rescaling."""
    require(frequency >= 1, "frequency must be positive")
    result: VectorField = []
    for component in a:
        scaled: Field = {}
        for mode, poly in component.items():
            scaled_mode = tuple(frequency * entry for entry in mode)
            scaled[scaled_mode] = pscale(poly, g(frequency))
        result.append(scaled)
    return result


def mean(a: Field) -> Poly:
    return a.get(ZERO_MODE, {})


def make_w(subset: Iterable[str]) -> VectorField:
    """Return the requested conjugate-pair subset of the R0.73W 2D3C W."""
    positive: dict[str, tuple[Mode, tuple[Gaussian, Gaussian, Gaussian]]] = {
        "x": ((1, 0, 0), (g(), g(-1), g(-HALF))),
        "y": ((0, 1, 0), (g(-1), g(), g(-HALF))),
        "xy": ((1, 1, 0), (g(0, 1), g(0, -1), g(0, HALF))),
    }
    chosen = tuple(subset)
    require(len(chosen) == len(set(chosen)), "duplicate pair label")
    require(all(label in positive for label in chosen), "unknown pair label")
    result: VectorField = [{}, {}, {}]
    for label in chosen:
        mode, vector = positive[label]
        negative = mode_neg(mode)
        for component in range(3):
            result[component][mode] = pconst(vector[component])
            result[component][negative] = pconst(gconj(vector[component]))
    return result


def tensor_stress(u: VectorField) -> list[list[Field]]:
    v = [heat(component) for component in u]
    return [
        [
            fadd(heat(fmul(u[i], u[j])), fneg(fmul(v[i], v[j])))
            for j in range(3)
        ]
        for i in range(3)
    ]


def production_field(u: VectorField) -> Field:
    v = [heat(component) for component in u]
    tau = tensor_stress(u)
    result: Field = {}
    for i in range(3):
        for j in range(3):
            result = fadd(result, fmul(tau[i][j], derivative(v[i], j)))
    return fneg(result)


def third_central_flux(u: VectorField) -> VectorField:
    """Compute K_j=1/2 sum_i E[(u_i-v_i)^2(u_j-v_j)] directly."""
    v = [heat(component) for component in u]
    result: VectorField = []
    for j in range(3):
        total: Field = {}
        for i in range(3):
            term = heat(fmul(fmul(u[i], u[i]), u[j]))
            term = fadd(term, fneg(fmul(v[j], heat(fmul(u[i], u[i])))))
            term = fadd(
                term,
                fneg(fscale(fmul(v[i], heat(fmul(u[i], u[j]))), g(2))),
            )
            term = fadd(
                term, fscale(fmul(fmul(v[i], v[i]), v[j]), g(2))
            )
            total = fadd(total, term)
        result.append(fscale(total, g(HALF)))
    return result


def centered_remainder_direct(u: VectorField) -> Field:
    """Expand the Gaussian first moment in (2.7), independently of Pi-div K."""
    modes = sorted(set().union(*(component.keys() for component in u)))
    amplitudes: dict[tuple[int, Mode], Gaussian] = {}
    for component in range(3):
        for mode, poly in u[component].items():
            require(set(poly) <= {0}, "direct centered remainder expects raw u")
            amplitudes[(component, mode)] = poly.get(0, ZERO)

    result: Field = {}
    triples = [(k, ell, r) for k in modes for ell in modes for r in modes]
    for k, ell, r in triples:
        output_mode = mode_add(mode_add(k, ell), r)
        ordered = (k, ell, r)
        multiplier_by_coordinate: list[Poly] = [{}, {}, {}]
        for mask in range(1, 8):
            selected = [index for index in range(3) if mask & (1 << index)]
            q_mode = ZERO_MODE
            for index in selected:
                q_mode = mode_add(q_mode, ordered[index])
            exponent = norm2(q_mode) + sum(
                norm2(ordered[index]) for index in range(3) if index not in selected
            )
            sign = -1 if (3 - len(selected)) % 2 else 1
            for j in range(3):
                # (1/(4s))*(-2is*q_j) = -(i/2)q_j.
                coefficient = g(0, -F(sign * q_mode[j], 2))
                if coefficient != ZERO:
                    multiplier_by_coordinate[j] = padd(
                        multiplier_by_coordinate[j], {exponent: coefficient}
                    )
        for i in range(3):
            for j in range(3):
                amplitude = gmul(
                    amplitudes.get((j, k), ZERO),
                    gmul(
                        amplitudes.get((i, ell), ZERO),
                        amplitudes.get((i, r), ZERO),
                    ),
                )
                if amplitude == ZERO:
                    continue
                contribution = pscale(multiplier_by_coordinate[j], amplitude)
                result[output_mode] = padd(
                    result.get(output_mode, {}), contribution
                )
    return fclean(result)


def subfilter_energy_field(u: VectorField) -> Field:
    tau = tensor_stress(u)
    result: Field = {}
    for i in range(3):
        result = fadd(result, tau[i][i])
    return fscale(result, g(HALF))


def gradient_covariance_field(u: VectorField) -> Field:
    v = [heat(component) for component in u]
    raw: Field = {}
    filtered: Field = {}
    for i in range(3):
        for j in range(3):
            grad_u = derivative(u[i], j)
            grad_v = derivative(v[i], j)
            raw = fadd(raw, fmul(grad_u, grad_u))
            filtered = fadd(filtered, fmul(grad_v, grad_v))
    return fadd(heat(raw), fneg(filtered))


def is_real_field(a: Field) -> bool:
    for mode, poly in a.items():
        opposite = a.get(mode_neg(mode), {})
        if set(poly) != set(opposite):
            return False
        if any(gconj(value) != opposite[power] for power, value in poly.items()):
            return False
    return True


def evaluate_poly_exact(a: Poly, q: Fraction) -> Gaussian:
    result = ZERO
    for power, coefficient in a.items():
        result = gadd(result, gscale(coefficient, q**power))
    return result


def evaluate_poly_at_carrier_q(
    a: Poly, frequency: int, carrier_q: Fraction
) -> Gaussian:
    """Evaluate powers q^p when p is a multiple of frequency^2."""
    unit = frequency * frequency
    require(all(power % unit == 0 for power in a), "non-carrier q power")
    result = ZERO
    for power, coefficient in a.items():
        result = gadd(result, gscale(coefficient, carrier_q ** (power // unit)))
    return result


def evaluate_poly_float(a: Poly, s: float) -> complex:
    return sum(
        complex(float(value[0]), float(value[1])) * math.exp(-power * s)
        for power, value in a.items()
    )


def probe_poly(a: Field, mode: Mode, phase: str, epsilon: Fraction) -> Poly:
    require(phase in {"cos", "sin"}, "probe phase must be cos or sin")
    result = dict(mean(a))
    for power, value in a.get(mode, {}).items():
        scalar = value[0] if phase == "cos" else -value[1]
        result = padd(result, {power: g(epsilon * scalar)})
    require(all(value[1] == 0 for value in result.values()), "probe is not real")
    return result


def fraction_json(value: Fraction) -> str:
    return str(value)


def gaussian_json(value: Gaussian) -> dict[str, str]:
    return {"imag": str(value[1]), "real": str(value[0])}


def real_poly_json(value: Poly) -> dict[str, str]:
    require(all(coefficient[1] == 0 for coefficient in value.values()), "nonreal poly")
    return {str(power): str(coefficient[0]) for power, coefficient in sorted(value.items())}


def canonical_positive(mode: Mode) -> bool:
    return next((entry > 0 for entry in mode if entry != 0), False)


def find_all_nonzero_probe(
    pi: Field, div_k: Field, remainder: Field, q: Fraction
) -> dict[str, object] | None:
    support = sorted(
        {
            mode
            for mode in set(pi) | set(div_k) | set(remainder)
            if mode != ZERO_MODE and canonical_positive(mode)
        },
        key=lambda mode: (max(abs(x) for x in mode), sum(abs(x) for x in mode), mode),
    )
    candidates: list[tuple[tuple[object, ...], Mode, str, list[Fraction]]] = []
    for mode in support:
        for phase_index, phase in enumerate(("cos", "sin")):
            values: list[Fraction] = []
            for field in (pi, div_k, remainder):
                coefficient = evaluate_poly_exact(field.get(mode, {}), q)
                values.append(coefficient[0] if phase == "cos" else -coefficient[1])
            if all(value != 0 for value in values):
                key = (
                    max(abs(x) for x in mode),
                    sum(abs(x) for x in mode),
                    mode,
                    phase_index,
                )
                candidates.append((key, mode, phase, values))
    if not candidates:
        return None
    _, mode, phase, values = min(candidates, key=lambda row: row[0])
    return {
        "mode": list(mode),
        "phase": phase,
        "rawModeCoefficientsAtQHalf": {
            "divK": str(values[1]),
            "pi": str(values[0]),
            "remainder": str(values[2]),
        },
    }


def decimal_scale_integral(poly: Poly, upper: Decimal) -> Decimal:
    require(all(value[1] == 0 for value in poly.values()), "real integral required")
    with localcontext() as context:
        context.prec = 70
        total = Decimal(0)
        for power, value in sorted(poly.items()):
            coefficient = Decimal(value[0].numerator) / Decimal(value[0].denominator)
            if power == 0:
                total += coefficient * upper
            else:
                n = Decimal(power)
                total += coefficient * (Decimal(1) - (-n * upper).exp()) / n
        return +total


def decimal_text(value: Decimal, digits: int = 50) -> str:
    with localcontext() as context:
        context.prec = digits
        return format(+value, "f")


def float_text(value: float) -> str:
    return format(float(value), ".17g")


def spectral_scale_slice(
    field: Field,
    probe_mode: Mode,
    phase: str,
    epsilon: Fraction,
    grid: int,
    time_order: int,
    upper: float,
) -> dict[str, float]:
    require(all(mode[2] == 0 for mode in field), "quadrature channel is 2D only")
    require(grid > 2 * max(max(abs(mode[0]), abs(mode[1])) for mode in field), "grid aliases modes")
    nodes, weights = np.polynomial.legendre.leggauss(time_order)
    times = 0.5 * upper * (nodes + 1.0)
    time_weights = 0.5 * upper * weights
    coordinates = 2.0 * np.pi * np.arange(grid, dtype=np.float64) / grid
    xx, yy = np.meshgrid(coordinates, coordinates, indexing="ij")
    phase_value = probe_mode[0] * xx + probe_mode[1] * yy
    if phase == "cos":
        eta = 1.0 + float(epsilon) * np.cos(phase_value)
    else:
        eta = 1.0 + float(epsilon) * np.sin(phase_value)
    require(float(np.min(eta)) >= 1.0 - abs(float(epsilon)) - 1e-14, "eta positivity failed")

    signed_total = 0.0
    absolute_total = 0.0
    max_imaginary = 0.0
    for s, time_weight in zip(times, time_weights):
        coefficients = np.zeros((grid, grid), dtype=np.complex128)
        for mode, poly in field.items():
            coefficients[mode[0] % grid, mode[1] % grid] += evaluate_poly_float(poly, float(s))
        values = np.fft.ifft2(coefficients) * (grid * grid)
        max_imaginary = max(max_imaginary, float(np.max(np.abs(values.imag))))
        real_values = values.real
        signed_total += float(time_weight) * float(np.mean(eta * real_values))
        absolute_total += float(time_weight) * float(np.mean(eta * np.abs(real_values)))
    return {
        "absolute": absolute_total,
        "maxImaginaryResidual": max_imaginary,
        "signed": signed_total,
    }


def quadrature_ladder(
    field: Field, mode: Mode, phase: str, epsilon: Fraction
) -> dict[str, object]:
    levels = ((128, 24), (256, 32), (512, 48), (1024, 64))
    rows: list[dict[str, object]] = []
    upper = 1.0
    for grid, time_order in levels:
        values = spectral_scale_slice(
            field, mode, phase, epsilon, grid, time_order, upper
        )
        rows.append(
            {
                "absoluteSpatialScaleIntegral": float_text(values["absolute"]),
                "grid": grid,
                "maxImaginaryResidual": float_text(values["maxImaginaryResidual"]),
                "signedSpatialScaleIntegral": float_text(values["signed"]),
                "timeGaussLegendreOrder": time_order,
            }
        )
    last = rows[-1]
    previous = rows[-2]
    absolute_last = float(last["absoluteSpatialScaleIntegral"])
    absolute_previous = float(previous["absoluteSpatialScaleIntegral"])
    signed_last = float(last["signedSpatialScaleIntegral"])
    signed_previous = float(previous["signedSpatialScaleIntegral"])
    return {
        "absoluteConvergenceDeltaLastTwo": float_text(abs(absolute_last - absolute_previous)),
        "cancellationRatioAbsSignedOverAbsolute": float_text(
            abs(signed_last) / absolute_last
        ),
        "levels": rows,
        "signedConvergenceDeltaLastTwo": float_text(abs(signed_last - signed_previous)),
    }


def mode_inventory(field: Field) -> dict[str, object]:
    return {
        "maxInfinityFrequency": max(
            (max(abs(entry) for entry in mode) for mode in field), default=0
        ),
        "modeCount": len(field),
        "qPowerMaximum": max(
            (power for poly in field.values() for power in poly), default=0
        ),
    }


def exact_witness(
    name: str,
    pair_labels: tuple[str, ...],
    probe_mode: Mode,
    probe_phase: str,
    expected: dict[str, Fraction],
) -> tuple[dict[str, object], dict[str, Field]]:
    epsilon = HALF
    q = HALF
    scale_frequency = 4
    u = make_w(pair_labels)
    pi = production_field(u)
    k_flux = third_central_flux(u)
    div_k = divergence(k_flux)
    remainder_subtraction = fadd(pi, fneg(div_k))
    remainder_direct = centered_remainder_direct(u)
    k = subfilter_energy_field(u)
    d = gradient_covariance_field(u)

    require(divergence(u) == {}, name + ": velocity is not divergence-free")
    require(all(mean(component) == {} for component in u), name + ": nonzero mean")
    require(all(is_real_field(component) for component in u), name + ": velocity is not real")
    require(is_real_field(pi), name + ": Pi is not real")
    require(remainder_direct == remainder_subtraction, name + ": direct S mismatch")

    probe_polys = {
        "pi": probe_poly(pi, probe_mode, probe_phase, epsilon),
        "divK": probe_poly(div_k, probe_mode, probe_phase, epsilon),
        "remainder": probe_poly(
            remainder_direct, probe_mode, probe_phase, epsilon
        ),
        "k": probe_poly(k, probe_mode, probe_phase, epsilon),
        "D": probe_poly(d, probe_mode, probe_phase, epsilon),
    }
    values = {
        label: evaluate_poly_exact(poly, q)[0] for label, poly in probe_polys.items()
    }
    require(
        values["pi"] == values["divK"] + values["remainder"],
        name + ": cutoff split failed",
    )
    for label, value in expected.items():
        require(values[label] == value, f"{name}: unexpected {label}: {values[label]}")
    # Dimensionless base denominator; under the N=4 NSE rescaling below,
    # D and R^{-2}k acquire the same common N^4 factor.
    denominator = values["D"] + values["k"]
    require(denominator > 0, name + ": quadratic denominator is not positive")

    # Verify the admissible-radius interpretation rather than merely assert it:
    # u_{A,N}=A*N*W(Nx), R=1/N, s=log(2)/N^2, theta=log(2).
    scaled_u = navier_stokes_rescale(u, scale_frequency)
    scaled_pi = production_field(scaled_u)
    scaled_div_k = divergence(third_central_flux(scaled_u))
    scaled_remainder = centered_remainder_direct(scaled_u)
    scaled_k = subfilter_energy_field(scaled_u)
    scaled_d = gradient_covariance_field(scaled_u)
    scaled_mode = tuple(scale_frequency * entry for entry in probe_mode)
    scaled_probe_polys = {
        "pi": probe_poly(scaled_pi, scaled_mode, probe_phase, epsilon),
        "divK": probe_poly(scaled_div_k, scaled_mode, probe_phase, epsilon),
        "remainder": probe_poly(
            scaled_remainder, scaled_mode, probe_phase, epsilon
        ),
        "k": probe_poly(scaled_k, scaled_mode, probe_phase, epsilon),
        "D": probe_poly(scaled_d, scaled_mode, probe_phase, epsilon),
    }
    scaled_values = {
        label: evaluate_poly_at_carrier_q(poly, scale_frequency, q)[0]
        for label, poly in scaled_probe_polys.items()
    }
    fourth_power = scale_frequency**4
    second_power = scale_frequency**2
    for label in ("pi", "divK", "remainder", "D"):
        require(
            scaled_values[label] == fourth_power * values[label],
            name + ": NSE rescaling failed for " + label,
        )
    require(
        scaled_values["k"] == second_power * values["k"],
        name + ": NSE rescaling failed for k",
    )
    scaled_denominator = scaled_values["D"] + second_power * scaled_values["k"]
    require(
        scaled_denominator == fourth_power * denominator,
        name + ": scaled denominator mismatch",
    )

    minus_u = vector_neg(u)
    require(production_field(minus_u) == fneg(pi), name + ": Pi parity failed")
    require(
        centered_remainder_direct(minus_u) == fneg(remainder_direct),
        name + ": S parity failed",
    )
    require(subfilter_energy_field(minus_u) == k, name + ": k parity failed")
    require(gradient_covariance_field(minus_u) == d, name + ": D parity failed")

    signed_decimal: dict[str, str] = {}
    for label in ("pi", "remainder"):
        integral = decimal_scale_integral(probe_polys[label], Decimal(1))
        signed_decimal[label] = decimal_text(integral)

    row: dict[str, object] = {
        "absorptionAtCarrierQHalfScaledRadius": {
            "denominatorPerA2": str(denominator),
            "piNumeratorPerA3": str(abs(values["pi"])),
            "piRatio": str(abs(values["pi"]) / denominator) + "*abs(A)",
            "remainderNumeratorPerA3": str(abs(values["remainder"])),
            "remainderRatio": str(abs(values["remainder"]) / denominator) + "*abs(A)",
            "normalization": "all displayed rows divided by N^4, N=4",
            "scope": "exact fixed nonnegative harmonic-probe family at R=1/4",
            "unboundedAsAbsAToInfinity": True,
        },
        "admissibleRadiusRescaling": {
            "R": "1/4",
            "actualDenominatorPerA2": str(scaled_denominator),
            "actualDivKPerA3": str(scaled_values["divK"]),
            "actualDPerA2": str(scaled_values["D"]),
            "actualKPerA2": str(scaled_values["k"]),
            "actualPiPerA3": str(scaled_values["pi"]),
            "actualProbeMode": list(scaled_mode),
            "actualRemainderPerA3": str(scaled_values["remainder"]),
            "carrierHeatFactor": "exp(-N^2*s)=1/2",
            "frequencyN": scale_frequency,
            "s": "log(2)/16",
            "thetaInS_equals_thetaR2": "log(2)",
            "velocity": "u_A,N(x)=A*N*W(N*x)",
        },
        "exactCutoffRowAtQHalf": {
            "D": str(values["D"]),
            "divKEqualsMinusGradEtaDotK": str(values["divK"]),
            "pi": str(values["pi"]),
            "Rminus2KPaymentAfterNormalization": str(values["k"]),
            "remainder": str(values["remainder"]),
            "scaling": "normalized by A-degree and common N^4 after N=4 rescaling",
        },
        "field": {
            "name": name,
            "pairCount": len(pair_labels),
            "pairLabels": list(pair_labels),
            "physical": (
                [
                    "-2*sin(x+y)",
                    "-2*cos(x)+2*sin(x+y)",
                    "-cos(x)-sin(x+y)",
                ]
                if pair_labels == ("x", "xy")
                else [
                    "-2*cos(y)-2*sin(x+y)",
                    "-2*cos(x)+2*sin(x+y)",
                    "-cos(x)-cos(y)-sin(x+y)",
                ]
            ),
        },
        "inventories": {
            "D": mode_inventory(d),
            "Kdiv": mode_inventory(div_k),
            "Pi": mode_inventory(pi),
            "k": mode_inventory(k),
            "remainder": mode_inventory(remainder_direct),
        },
        "parity": {
            "D_even": True,
            "Pi_odd": True,
            "k_even": True,
            "remainder_odd": True,
        },
        "probe": {
            "epsilon": "1/2",
            "etaMinimum": "1/2",
            "mode": list(probe_mode),
            "phase": probe_phase,
        },
        "probeQPolynomials": {
            label: real_poly_json(poly) for label, poly in probe_polys.items()
        },
        "signedCarrierScaleIntegralZeroToOne50Digits": signed_decimal,
    }
    return row, {
        "D": d,
        "divK": div_k,
        "k": k,
        "pi": pi,
        "remainder": remainder_direct,
    }


def build() -> dict[str, object]:
    one_pair = make_w(("x",))
    one_pi = production_field(one_pair)
    one_div_k = divergence(third_central_flux(one_pair))
    one_remainder = centered_remainder_direct(one_pair)
    require(one_pi == {}, "one-pair Pi must vanish")
    require(one_div_k == {}, "one-pair div K must vanish")
    require(one_remainder == {}, "one-pair remainder must vanish")

    two_row, two_fields = exact_witness(
        "two-pair x+xy witness",
        ("x", "xy"),
        (1, 0, 0),
        "sin",
        {
            "pi": F(225, 1024),
            "divK": F(27, 512),
            "remainder": F(171, 1024),
            "k": F(195, 64),
            "D": F(165, 16),
        },
    )
    three_row, three_fields = exact_witness(
        "three-pair R0.73W anchor",
        ("x", "y", "xy"),
        (1, 1, 0),
        "cos",
        {
            "pi": F(-3, 32),
            "divK": F(9, 128),
            "remainder": F(-21, 128),
            "k": F(255, 64),
            "D": F(195, 16),
        },
    )

    pair_subset_scan: dict[str, object] = {}
    for labels in (("x", "y"), ("x", "xy"), ("y", "xy")):
        u = make_w(labels)
        pi = production_field(u)
        div_k = divergence(third_central_flux(u))
        remainder = centered_remainder_direct(u)
        require(remainder == fadd(pi, fneg(div_k)), "subset direct S mismatch")
        pair_subset_scan["+".join(labels)] = {
            "allNonzeroProbeAtQHalf": find_all_nonzero_probe(
                pi, div_k, remainder, HALF
            ),
            "divKIdenticallyZero": div_k == {},
            "piIdenticallyZero": pi == {},
            "remainderIdenticallyZero": remainder == {},
        }

    quadrature: dict[str, object] = {}
    for key, row, fields in (
        ("twoPair", two_row, two_fields),
        ("threePair", three_row, three_fields),
    ):
        probe = row["probe"]
        require(isinstance(probe, dict), "probe schema error")
        mode = tuple(int(value) for value in probe["mode"])
        require(len(mode) == 3, "probe mode schema error")
        phase = str(probe["phase"])
        quadrature[key] = {}
        for field_name in ("pi", "remainder"):
            ladder = quadrature_ladder(fields[field_name], mode, phase, HALF)
            finest = ladder["levels"][-1]
            signed_exact = decimal_scale_integral(
                probe_poly(fields[field_name], mode, phase, HALF), Decimal(1)
            )
            signed_numeric = Decimal(str(finest["signedSpatialScaleIntegral"]))
            signed_error = abs(signed_numeric - signed_exact)
            ladder["signedClosedForm50Digits"] = decimal_text(signed_exact)
            ladder["signedFineVsClosedFormError"] = decimal_text(signed_error, 30)
            require(signed_error < Decimal("5e-14"), key + " signed quadrature failed")
            require(
                float(ladder["absoluteConvergenceDeltaLastTwo"]) < 5e-6,
                key + " absolute quadrature did not converge sufficiently",
            )
            require(
                float(finest["absoluteSpatialScaleIntegral"])
                + 1e-13
                >= abs(float(finest["signedSpatialScaleIntegral"])),
                key + " absolute integral fell below signed integral",
            )
            require(
                float(finest["maxImaginaryResidual"]) < 1e-12,
                key + " Fourier reality residual too large",
            )
            quadrature[key][field_name] = ladder

    script_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return {
        "arithmetic": {
            "absoluteChannel": (
                "deterministic float64 Fourier trapezoid plus Gauss-Legendre; "
                "three-level convergence, not interval-certified"
            ),
            "exactChannel": "finite Gaussian-rational q-polynomials, q=exp(-s)",
            "signedScaleIntegral": "70-digit Decimal evaluation of exact exponential sum",
        },
        "candidateDecisions": {
            "compactCutoffQuadraticAbsorption_5_1_5_2": (
                "OPEN_IN_THIS_HARNESS: harmonic probes are nonnegative but not compactly supported"
            ),
            "fixedHarmonicProbeQuadraticAbsorption": (
                "REFUTED_EXACTLY: two-pair and three-pair ratios grow linearly in abs(A)"
            ),
            "ledgerCompleteCandidate_5_3": (
                "OPEN: the E^(3/2) row has cubic amplitude degree and was not omitted"
            ),
            "onePairProduction": "ZERO_EXACTLY_FOR_TESTED_AND_ANALYTIC_ONE_PHASE_CLASS",
            "staticAbsoluteTentOrCarlesonControl": (
                "OPEN: only a static spatial-scale slice was computed"
            ),
            "twoPairLocalizedSplit": (
                "NONZERO_EXACT_WITNESS: two conjugate pairs suffice for all three harmonic-probe rows"
            ),
        },
        "exactSelfChecks": {
            "directGaussianMomentRemainderEqualsPiMinusDivK": True,
            "onePairAllCubicChannelsZero": True,
            "parityChecks": True,
            "threePairAnchorMinus3Over32": True,
            "twoPairCutoffSplit": "225/1024 = 27/512 + 171/1024",
        },
        "pairSubsetScan": pair_subset_scan,
        "quadrature": quadrature,
        "schemaVersion": 1,
        "scope": {
            "absoluteValuesIntervalCertified": False,
            "carlesonEstimateProved": False,
            "clayConclusion": "OPEN",
            "compactCutoffCertified": False,
            "dgxUsed": False,
            "epsilonRegularityProved": False,
            "networkUsed": False,
            "nonzeroPdeDefectConstructed": False,
            "notClay": True,
            "navierStokesSimulation": False,
            "timeIntegratedPdeStatement": False,
        },
        "scriptSha256": script_sha,
        "threePair": three_row,
        "twoPair": two_row,
    }


def report(result: dict[str, Any]) -> str:
    two = result["twoPair"]
    three = result["threePair"]
    quadrature = result["quadrature"]
    two_pi = quadrature["twoPair"]["pi"]
    two_s = quadrature["twoPair"]["remainder"]
    three_pi = quadrature["threePair"]["pi"]
    three_s = quadrature["threePair"]["remainder"]
    template = r"""# R0.73X minimal finite Fourier harness: exact falsification and tent-slice diagnostic

**Status:** reproducible single-package diagnostic; exact algebra plus converged
absolute-value quadrature; not a two-producer sealed certificate

**Command:**

```bash
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/r073x_finite_fourier_harness.py --check-only
```

- **DGX used:** false
- **Network used:** false
- **Navier--Stokes simulation:** false
- **Clay conclusion:** OPEN

## 1. Quantifier boundary

The exact counterexample below concerns the deliberately strong statement
with a **fixed nonnegative harmonic probe**
\(\eta=1+\tfrac12\Phi_\ell(x)\), where \(\Phi_\ell\) is the declared
sine or cosine phase and the carrier heat factor is
\(Q=e^{{-N^2s}}=1/2\),
and a constant independent of the amplitude \(A\).  To keep the frozen
radius restriction, the harness verifies the exact NSE rescaling
\(u_{{A,N}}(x)=ANW(Nx)\) with \(N=4\), \(R=1/4<\pi/8\),
\(s=(\log2)/16=(\log2)R^2\), and \(\nu=1\).  The displayed exact rows
below have the common \(N^4\) factor divided out.  This
probe is periodic and satisfies \(\eta\ge1/2\), but it is not compactly
supported.  Therefore the calculation does not yet refute the compact local
cutoff versions (5.1)--(5.2) in the problem freeze.  That transfer needs a
separate certified bump or fixed-sign-neighborhood argument.

The tent rows integrate **heat scale only at one frozen time**.  They are not
parabolic time-integrated tent or Carleson norms and cannot establish an
epsilon-regularity or continuation theorem.

## 2. Exact two-pair improvement

One conjugate pair gives \(\Pi_s=\nabla\!\cdot K_s={\mathscr S}_s=0\)
exactly.  Already the two-pair field

\[
u=(-2\sin(x+y),\,-2\cos x+2\sin(x+y),\,-\cos x-\sin(x+y))
\]

with the rescaled probe \(\eta_4=1+\tfrac12\sin(4x)\) has, after division
by the common \(N^4\) factor and at the carrier heat factor \(1/2\),

\[
\langle\eta\Pi_s\rangle=\frac{{225}}{{1024}},\qquad
-\langle\nabla\eta\cdot K_s\rangle=\frac{{27}}{{512}},\qquad
\langle\eta{\mathscr S}_s\rangle=\frac{{171}}{{1024}}.
\]

Thus \(225/1024=27/512+171/1024\), with all three entries nonzero.
The direct Gaussian-moment construction of \({\mathscr S}_s\) agrees
coefficientwise with \(\Pi_s-\nabla\cdot K_s\); it is not obtained by
reusing that subtraction.

For the complete displayed quadratic denominator
\(\nu D+R^{{-2}}k\), with the same common \(N^4\) factor divided out,

\[
N^{{-4}}\langle\eta(\nu D_{{ii,s}}+R^{{-2}}k_s)\rangle
=\frac{{855}}{{64}}A^2.
\]

Consequently the exact ratios are

\[
\frac{{|\langle\eta\Pi_s\rangle|}}
{{\langle\eta(\nu D_{{ii,s}}+R^{{-2}}k_s)\rangle}}
=\frac{{5|A|}}{{304}},\qquad
\frac{{|\langle\eta{\mathscr S}_s\rangle|}}
{{\langle\eta(\nu D_{{ii,s}}+R^{{-2}}k_s)\rangle}}
=\frac{{|A|}}{{80}}.
\]

Hence no amplitude-independent constant controls these two numerators in
this exact harmonic-probe class.  The result also shows that two conjugate
pairs suffice for a fully nonzero localized split; it is not an exhaustive
minimal-wavevector theorem.

## 3. Three-pair anchor reproduction

For the R0.73W three-pair field and the rescaled probe
\(1+\tfrac12\cos(4x+4y)\), the harness recovers, after the same
\(N^4\) normalization,

\[
-\frac3{{32}}=\frac9{{128}}-\frac{{21}}{{128}}.
\]

The complete quadratic denominator is \(1035A^2/64\), so the exact
production and remainder ratios are \(2|A|/345\) and \(7|A|/690\),
respectively.  This independently reproduces the design anchor while
keeping its harmonic-cutoff scope explicit.

## 4. Signed versus spatially absolute heat-scale slices

For each field the harness evaluates in the carrier variable
\(r=N^2s\in(0,1)\), equivalently over the physical heat interval
\(0<s<R^2\),

\[
\left|\int_0^1\!\langle\eta f_r\rangle\,dr\right|
\quad\hbox{{and}}\quad
\int_0^1\!\langle\eta|f_r|\rangle\,dr,
\qquad f\in\{{\Pi,{\mathscr S}}\}}.
\]

The signed value is a 70-digit evaluation of an exact finite exponential
sum.  The absolute value is a deterministic 1024-by-1024 Fourier-grid,
64-node Gauss--Legendre result, accompanied by 128/256/512/1024 convergence.
It is numerical, not interval-certified.

| field | channel | signed/absolute cancellation ratio | last absolute convergence delta |
|---|---:|---:|---:|
| two-pair | \(\Pi\) | __TWO_PI_RATIO__ | __TWO_PI_DELTA__ |
| two-pair | \({{\mathscr S}}\) | __TWO_S_RATIO__ | __TWO_S_DELTA__ |
| three-pair | \(\Pi\) | __THREE_PI_RATIO__ | __THREE_PI_DELTA__ |
| three-pair | \({{\mathscr S}}\) | __THREE_S_RATIO__ | __THREE_S_DELTA__ |

A small ratio records cancellation only.  It gives no upper bound for the
absolute tent quantity.  A bounded ratio along these two finite fields gives
no evidence for a universal Carleson estimate.

## 5. Licensed conclusions and open rows

- **Exact:** the one-pair cubic channels vanish; the displayed two- and
  three-pair cutoff rows and amplitude ratios are exact.
- **Exact falsification:** the fixed-harmonic-probe, amplitude-independent
  quadratic absorption candidates are false.
- **Finite numerical diagnostic:** signed and absolute static scale slices
  differ substantially and the stored quadrature ladder is converged at the
  reported resolution.
- **Still open:** compact-cutoff (5.1)--(5.2), the ledger-complete cubic
  candidate (5.3), any time-integrated tent/Carleson control, suitable-weak
  defect passage, epsilon regularity, and three-dimensional global
  regularity.

NOT CLAY.
"""
    return (
        template.replace("{{", "{")
        .replace("}}", "}")
        .replace("__TWO_PI_RATIO__", str(two_pi["cancellationRatioAbsSignedOverAbsolute"]))
        .replace("__TWO_PI_DELTA__", str(two_pi["absoluteConvergenceDeltaLastTwo"]))
        .replace("__TWO_S_RATIO__", str(two_s["cancellationRatioAbsSignedOverAbsolute"]))
        .replace("__TWO_S_DELTA__", str(two_s["absoluteConvergenceDeltaLastTwo"]))
        .replace("__THREE_PI_RATIO__", str(three_pi["cancellationRatioAbsSignedOverAbsolute"]))
        .replace("__THREE_PI_DELTA__", str(three_pi["absoluteConvergenceDeltaLastTwo"]))
        .replace("__THREE_S_RATIO__", str(three_s["cancellationRatioAbsSignedOverAbsolute"]))
        .replace("__THREE_S_DELTA__", str(three_s["absoluteConvergenceDeltaLastTwo"]))
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="recompute and require byte-identical stored JSON and Markdown",
    )
    args = parser.parse_args()
    print("R073X_STAGE=exact-algebra")
    result = build()
    print("R073X_STAGE=quadrature-and-self-checks-complete")
    encoded_result = canonical(result)
    encoded_report = report(result)
    if args.check_only:
        require(RESULT_PATH.is_file(), "missing " + str(RESULT_PATH))
        require(REPORT_PATH.is_file(), "missing " + str(REPORT_PATH))
        require(
            RESULT_PATH.read_text(encoding="utf-8") == encoded_result,
            "stored JSON is stale",
        )
        require(
            REPORT_PATH.read_text(encoding="utf-8") == encoded_report,
            "stored Markdown is stale",
        )
    else:
        RESULT_PATH.write_text(encoded_result, encoding="utf-8")
        REPORT_PATH.write_text(encoded_report, encoding="utf-8")
    print("R073X_EXACT_CHECKS=PASS")
    print("R073X_TWO_PAIR_SPLIT=225/1024=27/512+171/1024")
    print("R073X_HARMONIC_ABSORPTION=REFUTED_EXACTLY")
    print("R073X_COMPACT_CUTOFF_ABSORPTION=OPEN_IN_THIS_HARNESS")
    print("R073X_CARLESON=OPEN")
    print("R073X_CLAY=OPEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
