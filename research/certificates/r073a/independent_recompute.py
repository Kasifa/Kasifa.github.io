#!/usr/bin/env python3
"""Independent raw-q propagator producer for the R0.73A CSV certificate.

The implementation does not import or execute the main certificate producer.
It starts from the original q Fourier matrix, integrates that matrix, and only
then conjugates the propagator into X_mu coordinates.  These finite Galerkin
values are deterministic crosschecks, not an infinite-dimensional proof.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path
from typing import Dict, List

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "experiments" / "r073a" / "xmu_propagator_certificate.csv"
HEADER = [
    "certificateId", "s", "d", "mu", "c", "gain", "bound",
    "sourceCommit", "certificateCommit",
]
FLOAT_TOLERANCE = 2e-8


def lattice(n_cut: int) -> List[int]:
    return list(range(-n_cut, n_cut + 1))


def w_fourier(time: float) -> Dict[int, complex]:
    return {
        -2: 1j * math.exp(-4 * time) / 8,
        -1: -1j * math.exp(-time) / 4,
        1: 1j * math.exp(-time) / 4,
        2: -1j * math.exp(-4 * time) / 8,
    }


def q_generator(n_cut: int, mu: float, coupling: float, time: float) -> np.ndarray:
    modes = lattice(n_cut)
    matrix = np.zeros((len(modes), len(modes)), dtype=np.complex128)
    coefficients = w_fourier(time)
    for row, n_mode in enumerate(modes):
        for column, m_mode in enumerate(modes):
            if n_mode == m_mode:
                matrix[row, column] -= n_mode * n_mode + mu
            shift = n_mode - m_mode
            coefficient = coefficients.get(shift)
            if coefficient is not None:
                matrix[row, column] += -1j * coupling * coefficient * (
                    1 - shift * shift / (m_mode * m_mode + mu)
                )
    return matrix


def raw_propagator(
    n_cut: int,
    mu: float,
    coupling: float,
    start: float,
    end: float,
    steps: int,
) -> np.ndarray:
    result = np.eye(2 * n_cut + 1, dtype=np.complex128)
    delta = (end - start) / steps
    time = start
    for _ in range(steps):
        k1 = q_generator(n_cut, mu, coupling, time) @ result
        k2 = q_generator(n_cut, mu, coupling, time + delta / 2) @ (
            result + delta * k1 / 2
        )
        k3 = q_generator(n_cut, mu, coupling, time + delta / 2) @ (
            result + delta * k2 / 2
        )
        k4 = q_generator(n_cut, mu, coupling, time + delta) @ (
            result + delta * k3
        )
        result += delta * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        time += delta
    return result


def xmu_gain(
    n_cut: int, mu: float, coupling: float, start: float, end: float
) -> float:
    modes = lattice(n_cut)
    zero = modes.index(0)
    transform = np.eye(len(modes), dtype=np.complex128)
    inverse = np.eye(len(modes), dtype=np.complex128)
    transform[zero, zero] = mu
    inverse[zero, zero] = 1 / mu
    steps = max(160, math.ceil(800 * (end - start)))
    x_propagator = inverse @ raw_propagator(
        n_cut, mu, coupling, start, end, steps
    ) @ transform
    return float(np.linalg.norm(x_propagator, ord=2))


def analytic_bound(mu: float, coupling: float, start: float, end: float) -> float:
    integral = (
        7 / 4 * (math.exp(-start) - math.exp(-end))
        + 1 / 2 * (math.exp(-4 * start) - math.exp(-4 * end))
    )
    return math.exp(-mu * (end - start) + abs(coupling) * integral)


def number(value: float) -> str:
    return format(value, ".17g")


def identifier(
    n_cut: int, mu_index: int, coupling_index: int, interval_index: int
) -> str:
    return (
        f"R073A-XMU-N{n_cut:02d}-M{mu_index:02d}"
        f"-C{coupling_index:02d}-T{interval_index:02d}"
    )


def rows(stage: str, source_commit: str | None) -> List[dict[str, str]]:
    commit_text = source_commit if stage == "formal" else "pending"
    output = []
    mus = (0.001, 0.05, 0.25, 1.0)
    couplings = (-4.0, -1.0, 0.0, 1.0, 4.0)
    intervals = ((0.0, 0.1), (0.0, 0.75), (0.5, 2.0))
    for n_cut in (3, 5):
        for mu_index, mu in enumerate(mus, start=1):
            for coupling_index, coupling in enumerate(couplings, start=1):
                for interval_index, (start, end) in enumerate(intervals, start=1):
                    gain = xmu_gain(n_cut, mu, coupling, start, end)
                    bound = analytic_bound(mu, coupling, start, end)
                    if gain > bound + FLOAT_TOLERANCE:
                        raise RuntimeError(
                            f"finite propagator crosscheck exceeded bound: "
                            f"N={n_cut}, mu={mu}, c={coupling}, [{start},{end}]"
                        )
                    output.append({
                        "certificateId": identifier(
                            n_cut, mu_index, coupling_index, interval_index
                        ),
                        "s": number(start),
                        "d": number(end),
                        "mu": number(mu),
                        "c": number(coupling),
                        "gain": number(gain),
                        "bound": number(bound),
                        "sourceCommit": commit_text,
                        "certificateCommit": "pending",
                    })
    return output


def validate_source_commit(stage: str, source_commit: str | None) -> None:
    if stage == "source-stage":
        if source_commit is not None:
            raise RuntimeError("source-stage CSV cannot carry a source commit")
        return
    if source_commit is None or re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise RuntimeError("formal CSV requires --source-commit <40 lowercase hex>")


def write_csv(path: Path, values: List[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--self-test", action="store_true")
    modes.add_argument("--source-stage", action="store_true")
    modes.add_argument("--formal", action="store_true")
    parser.add_argument("--source-commit")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.self_test:
        if args.source_commit:
            parser.error("--self-test cannot be combined with --source-commit")
        values = rows("source-stage", None)
        if len(values) != 120 or len({row["certificateId"] for row in values}) != 120:
            raise RuntimeError("independent CSV grid is incomplete")
        print("R0.73A independent raw-q producer passed (120 cases; no output written)")
        return
    stage = "formal" if args.formal else "source-stage"
    validate_source_commit(stage, args.source_commit)
    values = rows(stage, args.source_commit)
    write_csv(args.output, values)
    print(f"wrote {len(values)} deterministic R0.73A {stage} CSV rows")


if __name__ == "__main__":
    main()
