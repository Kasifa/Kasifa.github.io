#!/usr/bin/env python3
"""Independent Fourier audit for the R0.71M increment/tangent identities.

This checker reconstructs a deterministic smooth periodic field, an annular
scalar filter, and a fixed positive cell cutoff without importing the exact
producer.  It checks the Lamb commutator in two implementations, the fused
off-band cancellation, the projective cutoff pairing, and the four-row
absolute envelope.

The calculation is a finite Fourier identity audit.  It performs no PDE time
stepping and supplies no sign certificate or regularity conclusion.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np


Frequency = tuple[int, int, int]

VELOCITY_MODES: tuple[
    tuple[Frequency, tuple[complex, complex, complex]], ...
] = (
    ((4, 0, 0), (0.0, 0.70 + 0.15j, 0.35 - 0.10j)),
    ((0, 4, 1), (0.55 - 0.20j, 0.10, -0.40j)),
    ((3, -2, 1), (0.20 + 0.30j, 0.50, 0.15 - 0.10j)),
    ((9, 1, 0), (0.10, 0.45 - 0.25j, 0.35 + 0.15j)),
    ((1, 10, 0), (0.40 + 0.10j, 0.05, -0.30j)),
)

CUTOFF_TERMS: tuple[tuple[str, Frequency, float], ...] = (
    ("cos", (1, 0, 0), 0.15),
    ("sin", (0, 1, 0), 0.10),
    ("cos", (1, 0, 1), 0.07),
    ("sin", (0, 1, -1), 0.05),
    ("cos", (0, 4, 1), 0.09),
    ("sin", (3, -2, 1), 0.06),
)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


class FourierAudit:
    def __init__(self, order: int, kappa: float) -> None:
        self.order = order
        self.kappa = kappa
        frequency = np.fft.fftfreq(order, d=1.0 / order)
        self.kx, self.ky, self.kz = np.meshgrid(
            frequency, frequency, frequency, indexing="ij"
        )
        self.radius = np.sqrt(self.kx**2 + self.ky**2 + self.kz**2)
        ratio = self.radius / kappa
        multiplier = np.zeros_like(ratio)
        core = (ratio >= 0.8) & (ratio <= 1.2)
        low = (ratio > 0.55) & (ratio < 0.8)
        high = (ratio > 1.2) & (ratio < 1.45)
        multiplier[core] = 1.0
        multiplier[low] = 0.5 * (
            1.0 - np.cos(math.pi * (ratio[low] - 0.55) / 0.25)
        )
        multiplier[high] = 0.5 * (
            1.0 + np.cos(math.pi * (ratio[high] - 1.2) / 0.25)
        )
        multiplier[self.radius == 0.0] = 0.0
        self.multiplier = multiplier

    def to_grid(self, field_hat: np.ndarray) -> np.ndarray:
        return np.fft.ifftn(field_hat, axes=(0, 1, 2)) * self.order**3

    def to_hat(self, field: np.ndarray) -> np.ndarray:
        return np.fft.fftn(field, axes=(0, 1, 2)) / self.order**3

    def derivative(self, field_hat: np.ndarray, axis: int) -> np.ndarray:
        frequencies = (self.kx, self.ky, self.kz)[axis]
        return 1j * frequencies[..., None] * field_hat

    def gradient_scalar(self, scalar_hat: np.ndarray) -> np.ndarray:
        return np.stack(
            [1j * self.kx * scalar_hat, 1j * self.ky * scalar_hat, 1j * self.kz * scalar_hat],
            axis=-1,
        )

    def curl(self, field_hat: np.ndarray) -> np.ndarray:
        kvec = np.stack([self.kx, self.ky, self.kz], axis=-1)
        return 1j * np.cross(kvec, field_hat)

    def leray(self, field_hat: np.ndarray) -> np.ndarray:
        kvec = np.stack([self.kx, self.ky, self.kz], axis=-1)
        radius_squared = self.radius**2
        dot = np.sum(kvec * field_hat, axis=-1)
        correction = np.zeros_like(field_hat)
        nonzero = radius_squared > 0.0
        correction[nonzero] = (
            kvec[nonzero] * (dot[nonzero] / radius_squared[nonzero])[..., None]
        )
        return field_hat - correction

    def filter(self, field_hat: np.ndarray) -> np.ndarray:
        return self.multiplier[..., None] * field_hat

    def laplacian(self, field_hat: np.ndarray) -> np.ndarray:
        return -(self.radius**2)[..., None] * field_hat

    def inner(self, left: np.ndarray, right: np.ndarray) -> complex:
        return np.mean(np.sum(np.conjugate(left) * right, axis=-1))

    def norm_squared(self, field: np.ndarray) -> float:
        return float(self.inner(field, field).real)


def signed_support(frequencies: set[Frequency]) -> set[Frequency]:
    support: set[Frequency] = set()
    for frequency in frequencies:
        support.add(frequency)
        support.add(tuple(-component for component in frequency))
    return support


def minkowski_sum(
    left: set[Frequency], right: set[Frequency]
) -> set[Frequency]:
    return {
        tuple(a + b for a, b in zip(left_frequency, right_frequency, strict=True))
        for left_frequency in left
        for right_frequency in right
    }


def annular_multiplier_value(frequency: Frequency, kappa: float) -> float:
    radius = math.sqrt(sum(component * component for component in frequency))
    if radius == 0.0:
        return 0.0
    ratio = radius / kappa
    if 0.8 <= ratio <= 1.2:
        return 1.0
    if 0.55 < ratio < 0.8:
        return 0.5 * (1.0 - math.cos(math.pi * (ratio - 0.55) / 0.25))
    if 1.2 < ratio < 1.45:
        return 0.5 * (1.0 + math.cos(math.pi * (ratio - 1.2) / 0.25))
    return 0.0


def filtered_support(support: set[Frequency], kappa: float) -> set[Frequency]:
    return {
        frequency
        for frequency in support
        if annular_multiplier_value(frequency, kappa) > 0.0
    }


def coordinate_bound(support: set[Frequency]) -> tuple[int, int, int]:
    return tuple(
        max((abs(frequency[axis]) for frequency in support), default=0)
        for axis in range(3)
    )


def validate_alias_safety(order: int, kappa: float) -> None:
    """Reject grids that can wrap a declared mode or a checked zero mode.

    The first condition represents every intermediate Fourier mode strictly
    below Nyquist.  The second makes the periodic trapezoidal means exact for
    every checked product of two audit fields, with one cutoff factor allowed.
    Both are sufficient conditions for this fixed finite-mode construction.
    """

    require(order > 0 and order % 2 == 0, "positive even Fourier grid order")
    require(math.isfinite(kappa) and kappa > 0.0, "finite positive kappa")

    velocity = signed_support({frequency for frequency, _ in VELOCITY_MODES})
    cutoff = {(0, 0, 0)} | signed_support(
        {frequency for _, frequency, _ in CUTOFF_TERMS}
    )
    quadratic = minkowski_sum(velocity, velocity)
    filtered_velocity = filtered_support(velocity, kappa)
    filtered_quadratic = filtered_support(quadratic, kappa)
    require(filtered_velocity, "kappa selects no declared velocity mode")
    require(filtered_quadratic, "kappa selects no declared quadratic mode")

    resolved = minkowski_sum(velocity, filtered_velocity)
    commutator = filtered_quadratic | resolved
    localized = minkowski_sum(cutoff, filtered_velocity)
    total_source = filtered_quadratic | filtered_velocity
    localized_total = minkowski_sum(cutoff, total_source)

    represented = (
        velocity
        | cutoff
        | quadratic
        | commutator
        | localized
        | total_source
        | localized_total
    )
    spectral_bound = coordinate_bound(represented)
    require(
        all(2 * bound < order for bound in spectral_bound),
        "alias-unsafe spectral support: require 2*max|k_axis| < order; "
        f"bounds={spectral_bound}, order={order}",
    )

    audited_fields = (
        velocity
        | filtered_quadratic
        | commutator
        | localized
        | total_source
        | localized_total
    )
    field_bound = coordinate_bound(audited_fields)
    cutoff_bound = coordinate_bound(cutoff)
    quadrature_bound = tuple(
        2 * field + cutoff_component
        for field, cutoff_component in zip(field_bound, cutoff_bound, strict=True)
    )
    require(
        all(bound < order for bound in quadrature_bound),
        "alias-unsafe zero-mode quadrature: require "
        "2*fieldBound+cutoffBound < order; "
        f"bounds={quadrature_bound}, order={order}",
    )


def add_real_mode(
    field_hat: np.ndarray,
    frequency: tuple[int, int, int],
    raw: tuple[complex, complex, complex],
) -> None:
    order = field_hat.shape[0]
    k = np.asarray(frequency, dtype=float)
    vector = np.asarray(raw, dtype=complex)
    vector -= k * np.dot(k, vector) / np.dot(k, k)
    positive = tuple(component % order for component in frequency)
    negative = tuple((-component) % order for component in frequency)
    field_hat[positive] += vector
    field_hat[negative] += np.conjugate(vector)


def deterministic_velocity(order: int) -> np.ndarray:
    field_hat = np.zeros((order, order, order, 3), dtype=complex)
    for frequency, raw in VELOCITY_MODES:
        add_real_mode(field_hat, frequency, raw)
    return field_hat


def build_cutoff(audit: FourierAudit) -> np.ndarray:
    coordinate = 2.0 * math.pi * np.arange(audit.order) / audit.order
    x, y, z = np.meshgrid(coordinate, coordinate, coordinate, indexing="ij")
    coordinates = (x, y, z)
    cutoff = np.full_like(x, 1.1)
    for kind, frequency, coefficient in CUTOFF_TERMS:
        phase = sum(
            component * coordinate_component
            for component, coordinate_component in zip(
                frequency, coordinates, strict=True
            )
        )
        cutoff += coefficient * (np.cos(phase) if kind == "cos" else np.sin(phase))
    require(float(cutoff.min()) > 0.0, "positive cutoff")
    return cutoff


def relative_residual(left: np.ndarray | complex, right: np.ndarray | complex) -> float:
    difference = np.asarray(left) - np.asarray(right)
    denominator = max(
        float(np.linalg.norm(np.asarray(left).ravel())),
        float(np.linalg.norm(np.asarray(right).ravel())),
        1.0e-30,
    )
    return float(np.linalg.norm(difference.ravel()) / denominator)


def run(order: int, kappa: float, viscosity: float) -> dict[str, object]:
    validate_alias_safety(order, kappa)
    audit = FourierAudit(order, kappa)
    velocity_hat = deterministic_velocity(order)
    velocity = audit.to_grid(velocity_hat).real
    divergence_hat = (
        1j
        * (
            audit.kx * velocity_hat[..., 0]
            + audit.ky * velocity_hat[..., 1]
            + audit.kz * velocity_hat[..., 2]
        )
    )
    divergence_residual = float(np.max(np.abs(divergence_hat)))
    require(divergence_residual < 1.0e-12, "divergence-free velocity")

    omega_hat = audit.curl(velocity_hat)
    omega = audit.to_grid(omega_hat).real
    filtered_omega_hat = audit.filter(omega_hat)
    filtered_omega = audit.to_grid(filtered_omega_hat).real

    lamb = np.cross(velocity, omega)
    lamb_hat = audit.to_hat(lamb)
    filtered_lamb_hat = audit.filter(lamb_hat)
    projected_lamb_hat = audit.leray(filtered_lamb_hat)
    field = audit.to_grid(projected_lamb_hat).real
    source_hat = audit.curl(projected_lamb_hat)
    source = audit.to_grid(source_hat).real

    # First implementation of R_j: the defining Lamb commutator.
    resolved_lamb = np.cross(velocity, filtered_omega)
    commutator_direct = audit.to_grid(filtered_lamb_hat).real - resolved_lamb

    # Second implementation: expand the exact quadratic-increment formula.
    speed_squared_hat = audit.to_hat(np.sum(velocity * velocity, axis=-1))
    filtered_speed_gradient = audit.to_grid(
        audit.gradient_scalar(audit.multiplier * speed_squared_hat)
    ).real
    filtered_velocity_hat = audit.filter(velocity_hat)
    filtered_velocity_gradient = np.stack(
        [audit.to_grid(audit.derivative(filtered_velocity_hat, axis)).real for axis in range(3)],
        axis=-2,
    )
    first = 0.5 * filtered_speed_gradient - np.einsum(
        "...a,...ia->...i", velocity, filtered_velocity_gradient
    )

    tensor = velocity[..., :, None] * velocity[..., None, :]
    tensor_hat = np.fft.fftn(tensor, axes=(0, 1, 2)) / order**3
    filtered_tensor_hat = audit.multiplier[..., None, None] * tensor_hat
    divergence_tensor_hat = 1j * (
        audit.kx[..., None] * filtered_tensor_hat[..., 0, :]
        + audit.ky[..., None] * filtered_tensor_hat[..., 1, :]
        + audit.kz[..., None] * filtered_tensor_hat[..., 2, :]
    )
    divergence_tensor = audit.to_grid(divergence_tensor_hat).real
    advect_filtered = np.einsum(
        "...a,...ai->...i", velocity, filtered_velocity_gradient
    )
    commutator_increment = first - divergence_tensor + advect_filtered
    increment_residual = relative_residual(commutator_direct, commutator_increment)
    require(increment_residual < 2.0e-11, "quadratic increment commutator")

    commutator_hat = audit.to_hat(commutator_direct)
    resolved_source_hat = audit.curl(audit.to_hat(resolved_lamb))
    increment_source_hat = audit.curl(commutator_hat)
    fusion_residual = relative_residual(
        source_hat, resolved_source_hat + increment_source_hat
    )
    require(fusion_residual < 2.0e-11, "resolved-increment source fusion")

    support = audit.multiplier > 1.0e-12
    commutator_energy = np.sum(np.abs(commutator_hat) ** 2)
    off_band_energy = np.sum(np.abs(commutator_hat[~support]) ** 2)
    off_band_fraction = float(off_band_energy / commutator_energy)
    require(off_band_fraction > 1.0e-4, "commutator has off-band content")
    high_off_band = audit.radius > 1.45 * kappa + 1.0e-12
    high_off_band_energy = np.sum(np.abs(commutator_hat[high_off_band]) ** 2)
    high_off_band_fraction = float(high_off_band_energy / commutator_energy)
    require(
        high_off_band_fraction > 1.0e-4,
        "commutator has content above the O(kappa) output band",
    )

    cutoff = build_cutoff(audit)
    localized_hat = audit.curl(audit.to_hat(cutoff[..., None] * filtered_omega))
    localized = audit.to_grid(localized_hat).real
    denominator = audit.norm_squared(localized)
    work = float(audit.inner(field, localized).real)
    alpha = work / denominator
    radius = math.sqrt(denominator)
    projected_field = field - alpha * localized

    mismatch_hat = (kappa**2 - audit.radius**2)[..., None] * filtered_omega_hat
    mismatch = audit.to_grid(mismatch_hat).real
    total_source = source + viscosity * mismatch
    localized_total_hat = audit.curl(audit.to_hat(cutoff[..., None] * total_source))
    localized_total = audit.to_grid(localized_total_hat).real
    direction = localized / radius
    projected_localized_total = localized_total - float(
        audit.inner(localized_total, direction).real
    ) * direction
    pairing_left = audit.inner(projected_field, projected_localized_total)

    curl_localized = audit.to_grid(audit.curl(localized_hat)).real
    paired_test = source - alpha * curl_localized
    pairing_right = audit.inner(paired_test, cutoff[..., None] * total_source)
    pairing_residual = relative_residual(pairing_left, pairing_right)
    require(pairing_residual < 3.0e-11, "projective cutoff pairing")

    y_value = audit.norm_squared(omega)
    z_value = work / math.sqrt(y_value * denominator)
    gamma = kappa * abs(work) / (y_value * denominator)
    tangent_envelope = (
        kappa**-2
        * abs(z_value)
        * abs(pairing_left)
        / (math.sqrt(y_value) * radius)
    )

    resolved_source = audit.to_grid(resolved_source_hat).real
    increment_source = audit.to_grid(increment_source_hat).real
    projective_geometry = alpha * curl_localized
    viscous_row = viscosity * mismatch
    weighted_norm = lambda value: audit.norm_squared(  # noqa: E731
        np.sqrt(cutoff)[..., None] * value
    )
    four_row_bound = gamma * kappa**-3 * (
        3.0 * (weighted_norm(resolved_source) + weighted_norm(increment_source))
        + 1.5 * (weighted_norm(projective_geometry) + weighted_norm(viscous_row))
    )
    require(tangent_envelope <= four_row_bound * (1.0 + 1.0e-12), "four-row envelope")

    # Radial form, with C_t=M-nu*kappa^2*C reconstructed algebraically.
    localized_t = localized_total - viscosity * kappa**2 * localized
    denominator_t = 2.0 * float(audit.inner(localized, localized_t).real)
    radial_right = audit.inner(source, cutoff[..., None] * total_source) - (
        work / denominator
    ) * (0.5 * denominator_t + viscosity * kappa**2 * denominator)
    radial_residual = relative_residual(pairing_left, radial_right)
    require(radial_residual < 3.0e-11, "radial projective pairing")

    pairing_components = {
        "sourceSquare": float(audit.inner(source, cutoff[..., None] * source).real),
        "viscousCross": float(
            viscosity * audit.inner(source, cutoff[..., None] * mismatch).real
        ),
        "projectiveSource": float(
            -alpha * audit.inner(curl_localized, cutoff[..., None] * source).real
        ),
        "projectiveViscous": float(
            -alpha
            * viscosity
            * audit.inner(curl_localized, cutoff[..., None] * mismatch).real
        ),
    }
    pairing_component_sum = sum(pairing_components.values())
    require(
        abs(pairing_component_sum - pairing_left.real)
        <= 5.0e-12 * max(abs(pairing_left.real), 1.0),
        "signed pairing components",
    )

    weighted_row_squares = {
        "resolvedTransport": weighted_norm(resolved_source),
        "incrementCommutator": weighted_norm(increment_source),
        "projectiveGeometry": weighted_norm(projective_geometry),
        "viscousMismatch": weighted_norm(viscous_row),
    }

    return {
        "release": "R0.71M",
        "status": "passed",
        "configuration": {
            "gridOrder": order,
            "kappa": kappa,
            "viscosity": viscosity,
            "timeStepping": False,
            "randomness": False,
        },
        "checks": {
            "divergenceResidual": divergence_residual,
            "incrementIdentityRelativeResidual": increment_residual,
            "resolvedIncrementFusionRelativeResidual": fusion_residual,
            "projectivePairingRelativeResidual": pairing_residual,
            "radialPairingRelativeResidual": radial_residual,
            "commutatorOffBandEnergyFraction": off_band_fraction,
            "commutatorHighOffBandEnergyFraction": high_off_band_fraction,
            "tangentEnvelope": tangent_envelope,
            "fourRowUpperBound": four_row_bound,
            "envelopeSlackRatio": four_row_bound / max(tangent_envelope, 1.0e-300),
            "pairingComponents": pairing_components,
            "pairingComponentSum": pairing_component_sum,
            "weightedRowSquares": weighted_row_squares,
        },
        "cell": {
            "Y": y_value,
            "B": work,
            "d": denominator,
            "z": z_value,
            "gamma": gamma,
        },
        "claimBoundary": (
            "Finite Fourier identity audit only.  The high off-band observation "
            "for R_j exhibits the missing O(kappa_j) upper-frequency support in "
            "the displayed Bernstein route.  No PDE trajectory, continuous sign theorem, Leray "
            "limit, or regularity result is asserted."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=64)
    parser.add_argument("--kappa", type=float, default=4.0)
    parser.add_argument("--viscosity", type=float, default=0.2)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    payload = run(arguments.order, arguments.kappa, arguments.viscosity)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
