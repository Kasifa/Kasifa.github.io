#!/usr/bin/env python3
"""R0.69G audit for the signed vorticity-kernel robustness barrier.

The audit checks the Euclidean Levi-Civita contraction, the periodic
Green-Hessian strain multiplier on an explicit real divergence-free Fourier
field, a nonzero vortex-stretching average, spherical angular averages, and
the finite-selector analogue of the magnitude-coupling theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "research/signed_vorticity_kernel_robustness_note.md"
AUDIT = ROOT / "research/signed_vorticity_kernel_robustness_audit.py"


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


def symbolic_kernel_checks() -> tuple[dict[str, bool], dict[str, str]]:
    a = sp.symbols("a0:3", real=True)
    b = sp.symbols("b0:3", real=True)
    z = sp.symbols("z0:3", real=True)
    avec = sp.Matrix(a)
    bvec = sp.Matrix(b)
    zvec = sp.Matrix(z)

    trace_contraction = sum(
        a[i] * a[j] * sp.LeviCivita(i, j, k) * b[k]
        for i in range(3)
        for j in range(3)
        for k in range(3)
    )
    hessian_numerator = sum(
        a[i]
        * a[ell]
        * sp.LeviCivita(i, j, k)
        * (
            3 * z[ell] * z[j]
            - sum(z[q] ** 2 for q in range(3))
            * sp.KroneckerDelta(ell, j)
        )
        * b[k]
        for i in range(3)
        for ell in range(3)
        for j in range(3)
        for k in range(3)
    )
    geometric_numerator = (
        3 * avec.dot(zvec) * zvec.dot(bvec.cross(avec))
    )

    phi = sp.symbols("phi", real=True)
    ey, ez = sp.symbols("e_y e_z", real=True)
    center_direction = sp.Matrix([0, 0, 1])
    neighbor_direction = sp.Matrix([sp.sin(phi), 0, sp.cos(phi)])
    radial_direction = sp.Matrix([sp.symbols("e_x"), ey, ez])
    angular_kernel = sp.simplify(
        radial_direction.dot(center_direction)
        * radial_direction.dot(neighbor_direction.cross(center_direction))
    )

    checks = {
        "antisymmetricTraceTermVanishes": (
            sp.simplify(trace_contraction) == 0
        ),
        "hessianContractionEqualsGeometricKernel": (
            sp.simplify(hessian_numerator - geometric_numerator) == 0
        ),
        "twoLobeModelKernelIsExact": (
            sp.simplify(angular_kernel + sp.sin(phi) * ey * ez) == 0
        ),
        "constantDirectionKernelVanishes": (
            sp.simplify(angular_kernel.subs(phi, 0)) == 0
        ),
    }
    formulas = {
        "periodicStretching": (
            "alpha=xi_i xi_l epsilon_ijk PV integral "
            "partial_lj G(z) omega_k(x+z) dz"
        ),
        "localGeometricKernel": (
            "D(e1,e2,e3)=(e1 dot e3)(e1 dot (e2 cross e3))"
        ),
        "twoLobeModel": "D=-sin(phi) e_y e_z",
        "robustnessDuality": (
            "sup_{g>=0, integral g=1}|integral K g|=||K||_infinity"
        ),
    }
    return checks, formulas


def levi(i: int, j: int, k: int) -> int:
    if len({i, j, k}) < 3:
        return 0
    return 1 if (i, j, k) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1


def butterfly_field() -> dict[tuple[int, int, int], np.ndarray]:
    horizontal = 1.25
    transverse = 0.8
    first_closing = 0.65
    second_closing = 0.4
    centers = (
        (1, 0, 0),
        (0, 1, 0),
        (-1, -1, 0),
        (0, 0, 1),
        (-1, 0, -1),
    )
    amplitudes = (
        np.asarray([0, horizontal, transverse], dtype=np.complex128),
        np.asarray([horizontal, 0, transverse], dtype=np.complex128),
        np.asarray([0, 0, -1j * first_closing], dtype=np.complex128),
        np.asarray([transverse, horizontal, 0], dtype=np.complex128),
        np.asarray([0, -1j * second_closing, 0], dtype=np.complex128),
    )
    result: dict[tuple[int, int, int], np.ndarray] = {}
    for wavevector, amplitude in zip(centers, amplitudes, strict=True):
        result[wavevector] = amplitude
        negative = tuple(-entry for entry in wavevector)
        result[negative] = np.conjugate(amplitude)
    return result


def direct_strain(
    wavevector: tuple[int, int, int], velocity: np.ndarray
) -> np.ndarray:
    k = np.asarray(wavevector, dtype=float)
    gradient = 1j * np.outer(velocity, k)
    return 0.5 * (gradient + gradient.T)


def green_strain(
    wavevector: tuple[int, int, int], vorticity: np.ndarray
) -> np.ndarray:
    k = np.asarray(wavevector, dtype=float)
    hessian = -np.outer(k, k) / np.dot(k, k)
    result = np.zeros((3, 3), dtype=np.complex128)
    for i in range(3):
        for ell in range(3):
            first = sum(
                levi(i, j, m) * hessian[ell, j] * vorticity[m]
                for j in range(3)
                for m in range(3)
            )
            second = sum(
                levi(ell, j, m) * hessian[i, j] * vorticity[m]
                for j in range(3)
                for m in range(3)
            )
            result[i, ell] = 0.5 * (first + second)
    return result


def fourier_checks() -> tuple[dict[str, bool], dict[str, object]]:
    field = butterfly_field()
    vorticity = {
        k: 1j * np.cross(np.asarray(k, dtype=float), coefficient)
        for k, coefficient in field.items()
    }
    strain_direct = {
        k: direct_strain(k, field[k])
        for k in field
    }
    strain_green = {
        k: green_strain(k, vorticity[k])
        for k in field
    }
    divergence_residual = max(
        abs(np.dot(np.asarray(k, dtype=float), coefficient))
        for k, coefficient in field.items()
    )
    multiplier_residual = max(
        float(np.max(np.abs(strain_direct[k] - strain_green[k])))
        for k in field
    )

    grid_size = 16
    axis = np.linspace(0, 2 * math.pi, grid_size, endpoint=False)
    mesh = np.meshgrid(axis, axis, axis, indexing="ij")
    omega_x = np.zeros((3, grid_size, grid_size, grid_size), dtype=np.complex128)
    strain_x = np.zeros(
        (3, 3, grid_size, grid_size, grid_size), dtype=np.complex128
    )
    for wavevector in field:
        phase = np.exp(
            1j
            * sum(
                wavevector[component] * mesh[component]
                for component in range(3)
            )
        )
        omega_x += vorticity[wavevector][:, None, None, None] * phase
        strain_x += strain_green[wavevector][
            :, :, None, None, None
        ] * phase
    stretching_density = np.einsum(
        "ixyz,ijxyz,jxyz->xyz", omega_x, strain_x, omega_x
    )
    stretching_average = float(np.mean(stretching_density).real)
    imaginary_residual = float(np.max(np.abs(stretching_density.imag)))
    expected_average = -4 * 1.25 * 0.8 * (0.65 + 0.4)

    checks = {
        "butterflyIsDivergenceFree": bool(divergence_residual < 1e-14),
        "periodicGreenMultiplierMatchesDirectStrain": (
            multiplier_residual < 1e-14
        ),
        "physicalStretchingDensityIsReal": imaginary_residual < 1e-13,
        "trapezoidalStretchingMatchesExactFourierAverage": (
            abs(stretching_average - expected_average) < 1e-12
        ),
        "exampleHasNonzeroSignedStretching": abs(stretching_average) > 1,
    }
    data = {
        "modeCount": len(field),
        "gridSize": grid_size,
        "divergenceResidual": f"{divergence_residual:.17g}",
        "multiplierResidual": f"{multiplier_residual:.17g}",
        "imaginaryStretchingResidual": f"{imaginary_residual:.17g}",
        "stretchingAverage": f"{stretching_average:.17g}",
        "expectedStretchingAverage": f"{expected_average:.17g}",
    }
    return checks, data


def angular_checks() -> tuple[dict[str, bool], dict[str, object]]:
    tilt = 0.73
    sine_tilt = math.sin(tilt)
    nodes, weights = np.polynomial.legendre.leggauss(160)
    azimuth = np.linspace(0, 2 * math.pi, 512, endpoint=False)
    total_weight = 0.0
    signed_total = 0.0
    absolute_total = 0.0
    biased = []
    values = []
    for mu, weight in zip(nodes, weights, strict=True):
        transverse_radius = math.sqrt(max(0.0, 1 - mu * mu))
        kernel = -sine_tilt * transverse_radius * np.sin(azimuth) * mu
        shell_weight = weight * (2 * math.pi / len(azimuth))
        total_weight += shell_weight * len(azimuth)
        signed_total += shell_weight * float(np.sum(kernel))
        absolute_total += shell_weight * float(np.sum(np.abs(kernel)))
        values.extend(kernel.tolist())
    signed_mean = signed_total / total_weight
    absolute_mean = absolute_total / total_weight
    exact_absolute_mean = 2 * sine_tilt / (3 * math.pi)

    all_biases_match = True
    for eta in (0.0, 0.25, 0.5, 0.9):
        numerator = 0.0
        denominator = 0.0
        for mu, weight in zip(nodes, weights, strict=True):
            transverse_radius = math.sqrt(max(0.0, 1 - mu * mu))
            kernel = -sine_tilt * transverse_radius * np.sin(azimuth) * mu
            magnitude = 1 + eta * np.sign(kernel)
            shell_weight = weight * (2 * math.pi / len(azimuth))
            numerator += shell_weight * float(np.sum(kernel * magnitude))
            denominator += shell_weight * float(np.sum(magnitude))
        observed = numerator / denominator
        expected = eta * exact_absolute_mean
        matches = bool(abs(observed - expected) < 6e-6)
        all_biases_match = all_biases_match and matches
        biased.append(
            {
                "eta": eta,
                "observedWeightedMean": f"{observed:.17g}",
                "expectedWeightedMean": f"{expected:.17g}",
                "matches": matches,
            }
        )

    sampled_supremum = max(abs(value) for value in values)
    exact_supremum = sine_tilt / 2
    finite_kernel = np.asarray([-0.91, -0.2, 0.0, 0.34, 0.87])
    simplex_vertex_values = [
        abs(float(np.dot(finite_kernel, np.eye(len(finite_kernel))[index])))
        for index in range(len(finite_kernel))
    ]
    finite_selector_supremum = max(simplex_vertex_values)

    checks = {
        "uniformAngularAverageCancels": bool(abs(signed_mean) < 1e-15),
        "absoluteAngularMeanMatchesClosedForm": bool(
            abs(absolute_mean - exact_absolute_mean) < 6e-6
        ),
        "allMagnitudeBiasesMatchClosedForm": all_biases_match,
        "sampledSupremumApproachesExactHalfSine": (
            abs(sampled_supremum - exact_supremum) < 5e-5
        ),
        "finitePositiveSelectorRecoversInfinityNorm": bool(
            abs(finite_selector_supremum - np.max(np.abs(finite_kernel)))
            < 1e-15
        ),
    }
    data = {
        "tiltRadians": tilt,
        "uniformSignedMean": f"{signed_mean:.17g}",
        "absoluteMean": f"{absolute_mean:.17g}",
        "exactAbsoluteMean": f"{exact_absolute_mean:.17g}",
        "sampledSupremum": f"{sampled_supremum:.17g}",
        "exactSupremum": f"{exact_supremum:.17g}",
        "magnitudeBiasScenarios": biased,
        "finiteSelectorKernel": finite_kernel.tolist(),
        "finiteSelectorSupremum": float(finite_selector_supremum),
    }
    return checks, data


def build_payload(source_commit: str) -> dict[str, object]:
    symbolic, formulas = symbolic_kernel_checks()
    fourier, fourier_data = fourier_checks()
    angular, angular_data = angular_checks()
    checks = {**symbolic, **fourier, **angular}
    return {
        "schemaVersion": "1.0",
        "study": "R0.69G",
        "status": "passed" if all(checks.values()) else "failed",
        "classification": (
            "rigorous structural no-go for direction-only signed annular "
            "averaging; not a Navier-Stokes regularity theorem"
        ),
        "checks": checks,
        "formulas": formulas,
        "periodicFourierAudit": fourier_data,
        "angularAudit": angular_data,
        "theorem": {
            "robustnessIdentity": (
                "sup_{g>=0, integral_A g=1}|integral_A K g|="
                "||K||_L_infinity(A)"
            ),
            "scope": (
                "eliminates only estimates that use direction-dependent "
                "sign cancellation uniformly over arbitrary nonnegative "
                "magnitude weights"
            ),
            "doesNotEliminate": [
                "magnitude-direction coupled criteria",
                "divergence-free realizability constraints",
                "filtered commutator estimates",
                "pressure-Hessian compensation",
            ],
        },
        "literatureBoundary": {
            "publishedInputs": [
                "Constantin-Fefferman 1993 vorticity direction criterion",
                "Beirao da Veiga-Berselli 2002 half-Holder coherence",
                "Grujic 2009 space-time localization",
            ],
            "unvalidatedPreprints": [
                "arXiv:2606.27560",
                "arXiv:2607.08866",
            ],
        },
        "decision": {
            "closedBranch": "direction-only signed annular averaging",
            "reason": (
                "nonnegative vorticity magnitude can select a sign lobe and "
                "recover the full L-infinity size of the angular kernel"
            ),
            "nextBranch": "pressure-Hessian signed compensation",
        },
        "provenance": {
            "sourceCommit": source_commit,
            "sourceFiles": {
                str(NOTE.relative_to(ROOT)): sha256(NOTE),
                str(AUDIT.relative_to(ROOT)): sha256(AUDIT),
            },
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "sympy": sp.__version__,
        },
    }


def main() -> int:
    args = parse_args()
    payload = build_payload(args.source_commit)
    text = json.dumps(
        payload,
        indent=2 if args.pretty else None,
        sort_keys=True,
    ) + "\n"
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    if args.check and payload["status"] != "passed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
