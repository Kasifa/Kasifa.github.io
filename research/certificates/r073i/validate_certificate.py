#!/usr/bin/env python3
"""Fail-closed validator for the R0.73I certificate package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any


def args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path(__file__).parent)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--write", action="store_true")
    return parser.parse_args()


def strict_json(path: Path) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError("non-finite JSON value " + value)
    value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)
    if not isinstance(value, dict):
        raise ValueError("expected JSON object: " + str(path))
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_ledger(directory: Path) -> bool:
    ledger = directory / "SHA256SUMS"
    if not ledger.exists():
        return True  # pre-seal validation
    declared: list[str] = []
    for row in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", row)
        if not match:
            return False
        name = match.group(2)
        path = directory / name
        if name in declared or not path.is_file() or digest(path) != match.group(1):
            return False
        declared.append(name)
    actual = sorted(path.name for path in directory.iterdir()
                    if path.is_file() and path.name != "SHA256SUMS")
    return declared == sorted(declared) == actual


def main() -> None:
    parsed = args()
    directory = parsed.directory.resolve()
    root = parsed.root.resolve() if parsed.root else directory.parents[2]
    certificate = strict_json(directory / "certificate.json")
    independent = strict_json(directory / "independent_recompute.json")
    finite = strict_json(root / "experiments/r073i/summary.json")
    ledger = certificate.get("claimLedger", {})
    checks = {
        "certificateSchema": certificate.get("schemaVersion") == "r073i-exact-certificate-v1",
        "certificatePassed": certificate.get("allChecksPass") is True,
        "independentSchema": independent.get("schemaVersion") == "r073i-independent-recompute-v1",
        "independentPassed": independent.get("allChecksPass") is True,
        "endpointClosed": ledger.get("inheritedEndpointStrictlyBelowOneOver450") == "CLOSED",
        "upperActionClosed": ledger.get("improvedContinuumUpperAction") == "CLOSED",
        "tangentClosed": ledger.get("zeroWindowTangentAction") == "CLOSED",
        "matchingActionOpen": ledger.get("matchingSelectedGainAction") == "OPEN",
        "clayOpen": ledger.get("Clay") == "OPEN",
        "finiteDiagnosticOnly": finite.get("diagnosticOnly") is True,
        "finiteContinuumClaimFalse": finite.get("claimBoundary", {}).get("finiteActionIsContinuumAction") is False,
        "sourceBindingsNonempty": len(certificate.get("sourceBindings", [])) >= 10,
        "flatLedgerValidIfPresent": validate_ledger(directory),
    }
    payload = {
        "schemaVersion": "r073i-certificate-validation-v1",
        "allChecksPass": all(checks.values()),
        "checks": checks,
    }
    if not payload["allChecksPass"]:
        raise RuntimeError("R0.73I certificate validation failed: "
                           + ", ".join(key for key, value in checks.items() if not value))
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if parsed.write:
        (directory / "validation.json").write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
