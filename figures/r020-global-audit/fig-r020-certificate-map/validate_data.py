#!/usr/bin/env python3
"""Cross-check every plotted R0.20 value against the certificate archive."""

from __future__ import annotations

import csv
from decimal import Decimal, getcontext
import json
from pathlib import Path


getcontext().prec = 70
PACKAGE = Path(__file__).resolve().parent
ARCHIVE = PACKAGE.parents[2] / "research" / "certificates" / "r020"


def load_json(name: str) -> dict[str, object]:
    return json.loads((ARCHIVE / name).read_text(encoding="utf-8"))


def close(actual: str, expected: Decimal, tolerance: Decimal = Decimal("1e-14")) -> None:
    if abs(Decimal(actual) - expected) > tolerance:
        raise AssertionError(f"plotted value {actual} != certified value {expected}")


def compact(value: Decimal) -> Decimal:
    return value / (1 + value)


def main() -> None:
    with (PACKAGE / "data.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    by_label = {row["label"]: row for row in rows}

    roots = load_json("interior-root-certificates.json")["roots"]
    for label, root in zip(("interior global maximum", "interior saddle"), roots):
        box = root["stationarySystemCertificate"]["boxDecimal"]
        centers = [
            (Decimal(lower) + Decimal(upper)) / 2
            for lower, upper in box
        ]
        row = by_label[label]
        for key, value in zip(("u", "v", "w"), centers):
            close(row[key], compact(value))
        close(
            row["target_fraction_percent"],
            Decimal(root["objectiveAndHessian"]["targetFractionPercent"]),
        )

    strips = load_json("boundary-strips.json")
    zero = strips["zeroBoundary"]
    infinity = strips["infinityBoundary"]
    delta_zero = Decimal(1) / 2
    epsilon_zero = Decimal(1) / 8
    expected_zero = (
        compact(Decimal(2) - delta_zero),
        compact(Decimal(2) + delta_zero),
        Decimal(0),
        compact(epsilon_zero),
    )
    expected_infinity = (
        compact(Decimal(3) - Decimal(1) / 2),
        compact(Decimal(3) + Decimal(1) / 2),
        Decimal(1) / (1 + Decimal(1) / 4),
        Decimal(1),
    )
    for label, expected in (
        ("x=0 analytic strip", expected_zero),
        ("x=infinity analytic strip", expected_infinity),
    ):
        row = by_label[label]
        for key, value in zip(("xmin", "xmax", "ymin", "ymax"), expected):
            close(row[key], value)
    if zero["dyadicCoreCompactCube"] != [["5/8", "11/16"], ["0", "1"], ["0", "1/16"]]:
        raise AssertionError("unexpected x=0 dyadic core")
    if infinity["dyadicCoreCompactCube"] != [["0", "1"], ["47/64", "49/64"], ["7/8", "1"]]:
        raise AssertionError("unexpected x=infinity dyadic core")

    faces = load_json("boundary-face-certificates.json")["faces"]
    edges = load_json("boundary-edge-certificates.json")["edges"]
    open_face_values = {
        face["face"]: max(
            Decimal(str(root["objectiveAndHessian"]["targetFractionPercentAtCenter"]))
            for root in face["roots"]
        )
        for face in faces
    }
    edge_values = {
        edge["edge"]: Decimal(str(edge["targetFractionPercentMidpoint"]))
        for edge in edges
    }
    closure_values = {
        "p=0 boundary closure": max(
            open_face_values["p_zero"],
            edge_values["p_zero__q_zero"],
            edge_values["p_zero__q_infinity"],
        ),
        "p=infinity boundary closure": max(
            open_face_values["p_infinity"],
            edge_values["p_infinity__q_zero"],
            edge_values["p_infinity__q_infinity"],
        ),
        "q=0 boundary closure": max(
            open_face_values["q_zero"],
            edge_values["p_zero__q_zero"],
            edge_values["p_infinity__q_zero"],
        ),
        "q=infinity boundary closure": max(
            open_face_values["q_infinity"],
            edge_values["p_zero__q_infinity"],
            edge_values["p_infinity__q_infinity"],
        ),
    }
    for label, expected in closure_values.items():
        close(by_label[label]["target_fraction_percent"], expected)

    for name in ("global-bernstein-depth2.json", "global-bernstein-depth3.json"):
        summary = load_json(name)
        if not summary["complete"] or summary["totals"]["unresolvedSamplesRecorded"] != 0:
            raise AssertionError(f"global audit is incomplete in {name}")

    print(json.dumps({"rowsChecked": len(rows), "status": "passed"}))


if __name__ == "__main__":
    main()
