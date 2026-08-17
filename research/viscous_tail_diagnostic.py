#!/usr/bin/env python3
"""Exploratory high-order viscous Taylor diagnostic at the R0.20 root.

This companion to ``viscous_target_taylor_audit.py`` computes the complete
finite-shell Fourier--Taylor recurrence in complex128 arithmetic.  It records
support counts, Fourier l1 coefficient sizes, root-test indicators, and the
target projection through a configurable order.  Independent shell levels
run in separate worker processes and report progress as they finish.

The calculation is a convergence and workload diagnostic.  Floating-point
coefficients and empirical root indicators are not Taylor-tail bounds and
are not used as proof of a Navier--Stokes statement.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import math
from pathlib import Path
import platform
import sys
import time

import numpy as np

from polarization_relay import geometry
import two_shell_taylor as shell
import viscous_target_taylor_audit as exact


def field_l1(field: shell.Field) -> float:
    return sum(float(np.linalg.norm(value)) for value in field.values())


def level_record(
    level: int,
    maximum_order: int,
    root: tuple[float, float, float],
) -> dict[str, object]:
    started = time.perf_counter()
    initial = exact.optimized_initial_field(level, *root)
    coefficients = shell.taylor_coefficients(
        initial,
        level,
        maximum_order=maximum_order,
    )
    target = tuple(int(value) for value in geometry(level + 1)["a"])
    fifth = coefficients[5].get(target, shell.ZERO)
    fifth_norm_squared = float(np.vdot(fifth, fifth).real)
    l1_values = [field_l1(field) for field in coefficients]
    target_records = []
    for order, field in enumerate(coefficients):
        value = field.get(target, shell.ZERO)
        if order >= 5:
            relative = complex(np.vdot(fifth, value) / fifth_norm_squared)
            line_defect = float(np.linalg.norm(value - relative * fifth))
        else:
            relative = 0.0j
            line_defect = float(np.linalg.norm(value))
        target_records.append(
            {
                "order": order,
                "norm": float(np.linalg.norm(value)),
                "relativeToOrderFive": {
                    "real": relative.real,
                    "imaginary": relative.imag,
                },
                "targetLineDefect": line_defect,
            }
        )
    return {
        "level": level,
        "delta": 4.0 ** (-level),
        "supportCounts": [len(field) for field in coefficients],
        "fourierL1CoefficientNorms": l1_values,
        "rootTestIndicators": [
            None if order == 0 else value ** (1.0 / order)
            for order, value in enumerate(l1_values)
        ],
        "target": list(target),
        "targetByOrder": target_records,
        "wallSeconds": time.perf_counter() - started,
    }


def audit(
    levels: list[int],
    maximum_order: int,
    workers: int,
    show_progress: bool,
) -> dict[str, object]:
    if maximum_order < 7:
        raise ValueError("The diagnostic order must be at least seven.")
    center, radius, certificate_hash = exact.load_root_box()
    root = float(center["p"]), float(center["q"]), float(center["x"])
    started = time.perf_counter()
    records = []
    with ProcessPoolExecutor(max_workers=min(workers, len(levels))) as pool:
        futures = {
            pool.submit(level_record, level, maximum_order, root): level
            for level in levels
        }
        for future in as_completed(futures):
            record = future.result()
            records.append(record)
            if show_progress:
                print(
                    f"[R0.21 +{time.perf_counter() - started:7.2f}s] "
                    f"level {record['level']} complete; "
                    f"order-{maximum_order} support={record['supportCounts'][-1]}",
                    file=sys.stderr,
                    flush=True,
                )
    records.sort(key=lambda record: record["level"])
    return {
        "schemaVersion": 1,
        "scope": "exploratory high-order viscous Taylor convergence at the R0.20 root",
        "proofStatus": "floating-point diagnostic only; no infinite-tail certificate",
        "configuration": {
            "levels": levels,
            "maximumOrder": maximum_order,
            "workers": min(workers, len(levels)),
            "rootBoxRadius": str(radius),
            "rootCertificate": str(exact.ROOT_CERTIFICATE),
            "rootCertificateSha256": certificate_hash,
        },
        "rootCenter": {variable: str(value) for variable, value in center.items()},
        "levels": records,
        "environment": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "platform": platform.platform(),
        },
        "git": exact.git_source_state(),
        "wallSeconds": time.perf_counter() - started,
    }


def validate(result: dict[str, object]) -> None:
    records = result["levels"]
    assert records
    for record in records:
        assert all(
            target["norm"] == 0.0 for target in record["targetByOrder"][:5]
        )
        assert all(value > 0 for value in record["fourierL1CoefficientNorms"])
        assert all(
            math.isfinite(value)
            for value in record["fourierL1CoefficientNorms"]
        )
        assert record["targetByOrder"][5]["relativeToOrderFive"]["real"] == 1.0
        assert abs(record["targetByOrder"][6]["relativeToOrderFive"]["imaginary"]) < 1.0e-12
    if len(records) >= 2:
        last = records[-1]["fourierL1CoefficientNorms"][-1]
        previous = records[-2]["fourierL1CoefficientNorms"][-1]
        assert abs(last / previous - 1.0) < 0.02


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--levels", type=int, nargs="+", default=[3, 4, 5])
    parser.add_argument("--maximum-order", type=int, default=12)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    result = audit(
        arguments.levels,
        arguments.maximum_order,
        arguments.workers,
        arguments.progress,
    )
    if arguments.check:
        validate(result)
    text = json.dumps(
        result,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=True,
    )
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
