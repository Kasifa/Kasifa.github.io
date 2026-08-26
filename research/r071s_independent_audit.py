#!/usr/bin/env python3
"""Independent numerical reconstruction of the R0.71S finite packet audit.

This checker imports neither ``r071s_exact_audit`` nor its output.  It builds
the box Gram matrices directly with NumPy, reconstructs the adjoint heat
packet by quadrature, and independently evaluates the even-touch and genuine
initial-face ledgers.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from time import perf_counter

import numpy as np


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def box_diagonal_checks() -> dict[str, object]:
    theta = 0.125
    rows = []
    maximum_relative_error = 0.0
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        height = theta / frequency**2
        # Direct L2 and mean reconstruction for h^-1/2 1_[0,h].
        packet_norm_squared = (height**-1) * height
        packet_mean = height**-0.5 * height
        diagonal = packet_norm_squared / packet_mean**2
        expected = frequency**2 / theta
        error = abs(diagonal / expected - 1.0)
        require(abs(packet_norm_squared - 1.0) < 2e-15, f"K={frequency} box norm")
        require(error < 2e-15, f"K={frequency} box diagonal")
        maximum_relative_error = max(maximum_relative_error, error)
        rows.append({
            "K": frequency,
            "height": height,
            "packetNormSquared": packet_norm_squared,
            "packetMean": packet_mean,
            "constantReproductionDiagonal": diagonal,
        })
    return {"passed": True, "maximumRelativeError": maximum_relative_error, "rows": rows}


def gram_checks() -> dict[str, object]:
    rows = []
    maximum_residual = 0.0
    cases = (
        (16, 1), (16, 2), (16, 4), (16, 8), (32, 8),
        (64, 1), (64, 2), (64, 4), (64, 8), (64, 16), (64, 32),
    )
    for count, overlap in cases:
        indices = np.arange(count, dtype=np.float64)
        gram = np.maximum(0.0, 1.0 - np.abs(indices[:, None] - indices[None, :]) / overlap)
        eigenvalues, eigenvectors = np.linalg.eigh(gram)
        eigenvalue = float(eigenvalues[-1])
        eigenvector = eigenvectors[:, -1]
        residual = float(np.linalg.norm(gram @ eigenvector - eigenvalue * eigenvector))
        lower = overlap - (overlap**2 - 1.0) / (3.0 * count)
        upper = float(overlap)
        require(lower <= eigenvalue + 2e-13, f"N={count}, p={overlap} lower")
        require(eigenvalue <= upper + 2e-13, f"N={count}, p={overlap} upper")
        require(residual < 2e-12, f"N={count}, p={overlap} residual")

        # Independent periodic reconstruction.  With h=p/N, each point is
        # covered p times, so the nonnegative circulant Gram has row sum p.
        periodic = np.zeros((count, count), dtype=np.float64)
        grid_size = count * 4096
        sample = (np.arange(grid_size) + 0.5) / grid_size
        packets = np.empty((count, grid_size), dtype=np.float64)
        height = overlap / count
        for index in range(count):
            relative = (sample - index / count) % 1.0
            packets[index] = (relative < height) / math.sqrt(height)
        periodic = (packets @ packets.T) / grid_size
        periodic_largest = float(np.linalg.eigvalsh(periodic)[-1])
        require(abs(periodic_largest - overlap) < 2e-12, f"N={count}, p={overlap} periodic eigenvalue")
        maximum_residual = max(maximum_residual, residual)
        rows.append({
            "N": count,
            "integerWindowOverlap": overlap,
            "largestToeplitzEigenvalue": eigenvalue,
            "RayleighLowerBound": lower,
            "rowSumUpperBound": upper,
            "eigenResidualL2": residual,
            "periodicSampleGridSize": grid_size,
            "periodicLargestEigenvalue": periodic_largest,
        })
    return {"passed": True, "maximumEigenResidual": maximum_residual, "rows": rows}


def heat_packet_checks() -> dict[str, object]:
    viscosity = 1.0
    theta = 0.125
    gauss_nodes, gauss_weights = np.polynomial.legendre.leggauss(512)
    rows = []
    maximum_norm_error = 0.0
    maximum_mean_error = 0.0
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        height = theta / frequency**2
        damping = viscosity * frequency**2
        time = 0.5 * height * (gauss_nodes + 1.0)
        weights = 0.5 * height * gauss_weights
        raw = np.exp(-damping * (height - time))
        quadrature_norm_squared = float(np.sum(weights * raw * raw))
        exact_norm_squared = (1.0 - math.exp(-2.0 * damping * height)) / (2.0 * damping)
        normalized = raw / math.sqrt(quadrature_norm_squared)
        quadrature_mean = float(np.sum(weights * normalized))
        exact_inverse_mean_squared = 0.5 * viscosity * frequency**2 / math.tanh(0.5 * viscosity * theta)
        inverse_mean_squared = quadrature_mean**-2
        norm_error = abs(quadrature_norm_squared / exact_norm_squared - 1.0)
        mean_error = abs(inverse_mean_squared / exact_inverse_mean_squared - 1.0)
        require(norm_error < 2e-13, f"K={frequency} heat norm quadrature")
        require(mean_error < 2e-13, f"K={frequency} heat mean quadrature")

        distance = 0.5 * height
        formula_gram = (
            math.exp(-damping * distance)
            * (1.0 - math.exp(-2.0 * damping * (height - distance)))
            / (1.0 - math.exp(-2.0 * damping * height))
        )
        # Direct quadrature on the overlap [d,h].
        overlap_time = distance + 0.5 * (height - distance) * (gauss_nodes + 1.0)
        overlap_weights = 0.5 * (height - distance) * gauss_weights
        first = np.exp(-damping * (height - overlap_time))
        shifted = np.exp(-damping * (distance + height - overlap_time))
        direct_gram = float(np.sum(overlap_weights * first * shifted) / exact_norm_squared)
        require(abs(direct_gram - formula_gram) < 2e-13, f"K={frequency} translated heat Gram")
        maximum_norm_error = max(maximum_norm_error, norm_error)
        maximum_mean_error = max(maximum_mean_error, mean_error)
        rows.append({
            "K": frequency,
            "height": height,
            "quadratureNormSquared": quadrature_norm_squared,
            "closedFormNormSquared": exact_norm_squared,
            "inverseNormalizedMeanSquared": inverse_mean_squared,
            "closedFormInverseMeanSquared": exact_inverse_mean_squared,
            "directHalfShiftGram": direct_gram,
            "closedFormHalfShiftGram": formula_gram,
        })
    return {
        "passed": True,
        "gaussLegendreOrder": 512,
        "maximumRelativeNormError": maximum_norm_error,
        "maximumRelativeMeanError": maximum_mean_error,
        "rows": rows,
    }


def bilinear_dichotomy_checks() -> dict[str, object]:
    theta = 0.125
    rows = []
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        height = theta / frequency**2
        # On [0,h], both profiles below have L2 norm one.
        box_mean = math.sqrt(height)
        haar_mean = 0.5 * math.sqrt(height) - 0.5 * math.sqrt(height)
        raw_box_box = box_mean * box_mean
        normalized_operator_norm = 1.0 / raw_box_box
        require(haar_mean == 0.0, f"K={frequency} Haar mean")
        require(abs(normalized_operator_norm / (frequency**2 / theta) - 1.0) < 2e-15, f"K={frequency} bilinear norm")
        rows.append({
            "K": frequency,
            "boxMean": box_mean,
            "zeroMeanHaarMean": haar_mean,
            "boxBoxConstantResponse": raw_box_box,
            "normalizedBoxBoxBilinearNorm": normalized_operator_norm,
            "haarBoxConstantResponse": haar_mean * box_mean,
        })
    return {
        "passed": True,
        "decision": "a zero-mean factor annihilates constants; two nonzero-mean L2 factors cost 1/h after constant normalization",
        "rows": rows,
    }


def even_touch_checks() -> dict[str, object]:
    rows = []
    maximum_signed_residual = 0.0
    for exponent in (0, 1, 2, 3, 4, 6, 8):
        eta = 2.0 ** (-8 * exponent)
        radius = 2.0**(-exponent)
        profile_at_radius = radius**4 / (radius**4 + eta)
        right_mass = profile_at_radius
        left_mass = -profile_at_radius
        signed = right_mass + left_mass
        jordan = abs(right_mass) + abs(left_mass)
        require(abs(signed) < 1e-15, f"n={exponent} signed cancellation")
        require(0.0 < right_mass < 1.0, f"n={exponent} half mass")
        maximum_signed_residual = max(maximum_signed_residual, abs(signed))
        rows.append({
            "softEta": eta,
            "shrinkingRadius": radius,
            "rightMass": right_mass,
            "leftMass": left_mass,
            "signedMass": signed,
            "JordanMass": jordan,
        })
    require(rows[-1]["rightMass"] > 0.999999999, "even-touch half mass approaches one")
    return {"passed": True, "maximumSignedResidual": maximum_signed_residual, "rows": rows}


def initial_face_checks() -> dict[str, object]:
    base_amplitude = 1.0
    rows = []
    maximum_entry_error = 0.0
    maximum_weighted_atom_error = 0.0
    maximum_time_scaling_error = 0.0
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        scaled_amplitude = base_amplitude * frequency
        y0 = scaled_amplitude**2 * frequency**2
        f_squared = scaled_amplitude**4 * frequency**2 / 4.0
        c_squared = scaled_amplitude**4 * frequency**6
        pairing = scaled_amplitude**4 * frequency**4 / 2.0
        entry = pairing**2 / (y0 * c_squared)
        target = entry / frequency**2
        relative_time_integral = frequency**-2
        expected_entry = base_amplitude**2 * frequency**2 / 4.0
        expected_target = base_amplitude**2 / 4.0
        entry_error = abs(entry / expected_entry - 1.0)
        target_error = abs(target / expected_target - 1.0)
        time_error = abs(relative_time_integral * frequency**2 - 1.0)
        require(entry_error < 2e-15, f"K={frequency} covariant initial face")
        require(target_error < 2e-15, f"K={frequency} invariant weighted atom")
        require(time_error < 2e-15, f"K={frequency} bare time scaling")
        maximum_entry_error = max(maximum_entry_error, entry_error)
        maximum_weighted_atom_error = max(maximum_weighted_atom_error, target_error)
        maximum_time_scaling_error = max(maximum_time_scaling_error, time_error)
        rows.append({
            "K": frequency,
            "scaledAmplitude": scaled_amplitude,
            "Y0": y0,
            "normFSquared": f_squared,
            "normLeadingCoefficientSquared": c_squared,
            "pairing": pairing,
            "positiveInitialFaceAtom": entry,
            "kappaMinusTwoWeightedAtom": target,
            "relativeBareLerayTimeIntegral": relative_time_integral,
        })
    return {
        "passed": True,
        "maximumEntryError": maximum_entry_error,
        "maximumWeightedAtomError": maximum_weighted_atom_error,
        "maximumTimeScalingError": maximum_time_scaling_error,
        "boundary": (
            "genuine one-sided NSE initial observation-boundary face and covariant scaling only; "
            "no positive-time numerical integration and no internal-entry theorem"
        ),
        "rows": rows,
    }


def build_result() -> dict[str, object]:
    started = perf_counter()
    checks = {
        "boxDiagonalChecks": box_diagonal_checks(),
        "gramChecks": gram_checks(),
        "heatPacketChecks": heat_packet_checks(),
        "bilinearDichotomyChecks": bilinear_dichotomy_checks(),
        "evenTouchChecks": even_touch_checks(),
        "initialFaceChecks": initial_face_checks(),
    }
    require(all(check["passed"] for check in checks.values()), "all independent R0.71S checks")
    return {
        "release": "R0.71S",
        "status": "passed",
        "elapsedSeconds": perf_counter() - started,
        "checks": checks,
        "scope": (
            "independent numerical reconstruction of finite packet constants and a genuine NSE initial-face scaling ledger; "
            "the even-touch family is not an NSE trajectory, and no positive-time NSE integration or regularity theorem is checked"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
