#!/usr/bin/env python3
"""Validate the R0.60 figure tables and pinned formal provenance."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    certificate_path = ROOT / metadata["formalCertificate"]["path"]
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    if sha256(certificate_path) != metadata["formalCertificate"]["sha256"]:
        raise AssertionError("formal certificate hash mismatch")
    if certificate["git"]["sourceCommit"] != metadata["formalCertificate"]["formalSourceCommit"]:
        raise AssertionError("formal source commit mismatch")
    if not all(certificate["checks"].values()):
        raise AssertionError("formal certificate contains a failed check")

    support = rows("support-gaps.csv")
    if len(support) != 14 * 5:
        raise AssertionError("unexpected support-gap row count")
    formulas = {3: (3, 1), 5: (2, 2), 7: (1, 3), 9: (0, 4)}
    for row in support:
        n_value = int(row["N"])
        high = int(row["H"])
        order = int(row["order"])
        gap = int(row["gap"])
        if high != 4 * n_value:
            raise AssertionError("H=4N mismatch")
        expected = max(0, 5 - n_value) if order == 11 else formulas[order][0] * n_value + formulas[order][1]
        if gap != expected or not math.isclose(float(row["gapOverH"]), gap / high, rel_tol=1e-15):
            raise AssertionError("support-gap formula mismatch")
        if order in formulas and row["targetStatus"] != "excluded":
            raise AssertionError("excluded odd order mislabeled")
        if order == 11 and (row["targetStatus"] == "support-admissible") != (n_value >= 5):
            raise AssertionError("order-eleven witness threshold mismatch")

    events = rows("picard-events.csv")
    required = {
        (2, "target plane", "reached", "-Q+Q=0"),
        (3, "original V support", "returned", "-Q+P-P=-Q"),
        (4, "target plane", "support-admissible", "-Q+Q+P-P=0"),
        (11, "target plane", "support-admissible", "zero path for N>=5"),
    }
    observed = {(int(row["order"]), row["lane"], row["status"], row["path"]) for row in events}
    if not required.issubset(observed):
        raise AssertionError("required support events are missing")
    print(json.dumps({"status": "passed", "formalChecks": len(certificate["checks"]), "supportRows": len(support), "eventRows": len(events)}, sort_keys=True))


if __name__ == "__main__":
    main()

