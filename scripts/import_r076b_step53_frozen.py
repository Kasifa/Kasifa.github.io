#!/usr/bin/env python3
"""Import only the twelve frozen R0.76B Step 53 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076B_STEP53_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "b31c53a5e48e2de56088ac2715a95000a64e2c9a"
CORE_PARENT_COMMIT = "9d3e65316204f67f6122b5fdf47c38014d723e10"
HANDOFF_PATH = "research/r076b_publication_handoff.md"
HANDOFF_SHA256 = "cf35f0cbf8ffaddf392ae1635bdf022c08cf7801e5a7fac307db83d4ba365196"
HANDOFF_AUDIT_PATH = "research/r076b_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "db93f10d26c0bb894ed1b06a999835d7eb4706b286bdfc763d9db97e32703bf3"

FROZEN = {
    "research/r076b_moderate_carrier_fixed_mode_flux_payment.md": "a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d",
    "research/r076b_moderate_carrier_fixed_mode_flux_payment_primary_audit.md": "0a6314c454021da284bbf157de36d6c2bd1683d600a21c8394f723acc26aa447",
    "research/r076b_report-source.md": "362fcf898a533efaf4072c876dba09f4231c131ad1c48d48efc92c52215428fc",
    "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_fixtures.json": "1f9b3df9cb8ff3f9d22250ce425b837d40268829bf18cb3e12b3f7d2dca64bf2",
    "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_expected.json": "4533edf290e07f1fddc5df1b9ef1655a5623f4a3714e840b1c402cdf3b8db3f1",
    "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.py": "b4ec0ba8fbbe9033dcec3254a1acc3a4f7e662fe320c4697f253f575aa98863a",
    "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_certificate_independent.rb": "0b53934fc132eda0c51a5885d8b50089b74897aeaff1373e1033bc825c43e849",
    "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_qa.sh": "dd4d802ce353c9698323cc2ad600df35794cce4796cf9457a63786165be47756",
    "research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.json": "d825624473f176c054134a75a47cb63fee65f7fe3bfe946ae505522a9c3c053e",
    "research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate_report.md": "5ae840453141f3059b94459996f7aaf808766fe3367ea433251343de128f938e",
    "research/r076b_moderate_carrier_fixed_mode_flux_payment_independent_audit.md": "1962313e8898dd6cdbafa9f1b543712d3660c25521c039e5311b21629bb1f6bf",
    "research/r076b_moderate_carrier_fixed_mode_flux_payment_qa_report.md": "7ec49c58e8eb209af2e836155b0126f8257e61b89f8742d04331ae31dc628f6d",
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
        "release": "R0.76B Step 53",
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
