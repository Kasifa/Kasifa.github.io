#!/usr/bin/env python3
"""Extract exact finite R0.33 moment-condition diagnostics for plotting."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r033/edge-moment-structure.json"


def write_rows(
    path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]
) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    finite = payload["finiteDiagnostics"]
    turan_rows = [
        {
            "sequence": record["sequence"],
            "index": record["index"],
            "minor": record["minor"],
            "sign": record["minorSign"],
            "normalized": record["normalized"],
            "normalized_decimal": record["normalizedDecimal"],
        }
        for record in finite["turanRecords"]
    ]
    write_rows(
        PACKAGE / "turan.csv",
        ("sequence", "index", "minor", "sign", "normalized", "normalized_decimal"),
        turan_rows,
    )

    hankel_rows = [
        {
            "sequence": record["sequence"],
            "matrix_kind": record["matrixKind"],
            "shift": record["shift"],
            "order": record["order"],
            "determinant": record["determinant"],
            "sign": record["sign"],
        }
        for record in finite["hankelDeterminants"]
    ]
    write_rows(
        PACKAGE / "hankel-signs.csv",
        ("sequence", "matrix_kind", "shift", "order", "determinant", "sign"),
        hankel_rows,
    )

    witness_rows = []
    for record in payload["theorem"]["witnesses"]:
        witness_rows.append(
            {
                "sequence": record["sequence"],
                "matrix_kind": "shifted" if record["shift"] else "ordinary",
                "shift": record["shift"],
                "order": record["order"],
                "determinant": record["determinant"]["exact"],
                "decimal": record["determinant"]["decimal"],
            }
        )
    write_rows(
        PACKAGE / "witnesses.csv",
        ("sequence", "matrix_kind", "shift", "order", "determinant", "decimal"),
        witness_rows,
    )


if __name__ == "__main__":
    main()
