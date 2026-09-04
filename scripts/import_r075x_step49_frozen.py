#!/usr/bin/env python3
"""Import only the twelve frozen R0.75X Step 49 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075X_STEP49_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "a97e197521b4efc0e3450f34cda5e646a2560d57"
CORE_PARENT_COMMIT = "3f2461b7ae0fd4a19c6d83dea859ead9fb5ff64d"
HANDOFF_PATH = "research/r075x_publication_handoff.md"
HANDOFF_SHA256 = "bf49a24643fda42abc7cc863349dd4da29dafe76e1ff8cc18641c6c7ca09f4cd"
HANDOFF_AUDIT_PATH = "research/r075x_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "7c013cdc97247ddb54ef588a44a7df4f0d689fbaf2a95fd10f70b3512e1122c5"

FROZEN = {
    "research/r075x_fixed_finite_mode_low_carrier_payment.md": "8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763",
    "research/r075x_fixed_finite_mode_low_carrier_payment_primary_audit.md": "8fffbf0c8ad50d5765c734f8e5627ce0dbe0d6b2aad4bcb26aa5c298f6143b2c",
    "research/r075x_report-source.md": "8fa756c7efe2660dbc5eeb51e2a11d10dce58f36f4c0d0f757000be1447b7f34",
    "scripts/r075x_fixed_finite_mode_low_carrier_payment_fixtures.json": "de231e977d9a2551222f0a4f0a8ebcb65490f76574bc4fa494db480e2b61a0e9",
    "scripts/r075x_fixed_finite_mode_low_carrier_payment_expected.json": "879ff3458050e712048654eb91623a00e5436a22f12c6b814fb137aa8af96311",
    "scripts/r075x_fixed_finite_mode_low_carrier_payment_certificate.py": "926dbcd704645d61392349437b10049c33b7ad8d77703e462ac3c784510190b4",
    "scripts/r075x_fixed_finite_mode_low_carrier_payment_certificate_independent.rb": "521d2026b6f27c466087b51663f7d3ca46bf9e84c3f51378fc403e05833b5ca1",
    "scripts/r075x_fixed_finite_mode_low_carrier_payment_qa.sh": "a94b5c96e600cdd9ea5c9ad8975bad5003058c067de079c495d27df7fcab7d7f",
    "research/r075x_fixed_finite_mode_low_carrier_payment_certificate.json": "717ce6ba1dcf4db39015db85c450bb1e2b7b31ff89e6b42ffb2bc30f31e3af05",
    "research/r075x_fixed_finite_mode_low_carrier_payment_certificate_report.md": "8725b6d6db67640fe20f1708d0942d994b174eaab0527828a0e0653aeb1c3701",
    "research/r075x_fixed_finite_mode_low_carrier_payment_independent_audit.md": "a1075d0ef321805a5d5d77be465820c85bd4ef820545531d983bab93094debf1",
    "research/r075x_fixed_finite_mode_low_carrier_payment_qa_report.md": "a35de008fb5195331153ed8fddfc5ba1bd064d19e423f2309bf44685cc05f183",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{commit}:{relative}"])


def write_exact(relative: str, data: bytes, expected: str) -> None:
    if sha256(data) != expected:
        raise SystemExit(f"source hash drift: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit(f"import byte drift: {relative}")


def main() -> None:
    for commit in (SOURCE_COMMIT, CORE_PARENT_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {resolved}")
    core_parent = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^"], text=True
    ).strip()
    if core_parent != CORE_PARENT_COMMIT:
        raise SystemExit(f"core parent drift: {core_parent}")
    if sha256((SOURCE / HANDOFF_PATH).read_bytes()) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256((SOURCE / HANDOFF_AUDIT_PATH).read_bytes()) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent-audit drift")
    changed = subprocess.check_output(
        ["git", "-C", str(SOURCE), "show", "--pretty=format:", "--name-only", SOURCE_COMMIT], text=True
    ).split()
    if set(changed) != set(FROZEN) or len(changed) != len(FROZEN):
        raise SystemExit("core changed-path whitelist drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75X Step 49",
        "source": SOURCE_COMMIT,
        "coreParentCommit": CORE_PARENT_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffIndependentAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
