#!/usr/bin/env python3
"""Import only the twelve frozen R0.76C Step 54 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R076C_STEP54_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "e2057338114e1d09355270196d23c37a13b25048"
CORE_PARENT_COMMIT = "87fdf888a511c47a64816c281e117f2462358bb8"
HANDOFF_PATH = "research/r076c_publication_handoff.md"
HANDOFF_SHA256 = "58bea911e1556a56632fb924a023e8c72ffa7765d2e5e7d5f35693abc4f84884"
HANDOFF_AUDIT_PATH = "research/r076c_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "d71ced54951327205076e3718695847baabfde41c6ee58807f99a8c70f0cdf44"

FROZEN = {
    "research/r076c_full_frequency_fixed_mode_flux_payment.md": "2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf",
    "research/r076c_full_frequency_fixed_mode_flux_payment_primary_audit.md": "d60546eab80d2fa6ef633efeb0b34120d7b9f81a33249e500f8d94b9a8c15f74",
    "research/r076c_report-source.md": "be523d313f5a487fd0b1550cb948f1e05b117f6d1734b8d9cbfd5ab1b5d57b27",
    "scripts/r076c_full_frequency_fixed_mode_flux_payment_fixtures.json": "36d1612b57932fad7ff6e9a4375b842d4900b0868625cfb5d498ce89a4dcee82",
    "scripts/r076c_full_frequency_fixed_mode_flux_payment_expected.json": "6dbd56d366b6b048acd769ff5b5eff303ede111153330de763ec04cee571ad52",
    "scripts/r076c_full_frequency_fixed_mode_flux_payment_certificate.py": "cd336bbee4c0e0a31be3642522bdc4703b724ef5d5f21ca587a74d84e7897452",
    "scripts/r076c_full_frequency_fixed_mode_flux_payment_certificate_independent.rb": "4e26bc8b0c79222bbc3c5f4945a8c85fff9980bcf6ad5f607de48ace86293259",
    "scripts/r076c_full_frequency_fixed_mode_flux_payment_qa.sh": "55e0325e87df901aa4261971f204a8b2bcdd7f45a98ea358e73f47f3da8e166f",
    "research/r076c_full_frequency_fixed_mode_flux_payment_certificate.json": "0ffd5fff7812eb777866cff70eb0bff68112ae176ffd8706ea732ddda55b4a9b",
    "research/r076c_full_frequency_fixed_mode_flux_payment_certificate_report.md": "be4c0d24e4b98fd0ae7c26fd4fd0fb955dc7007f64bba2c49f517b71c17ba8f6",
    "research/r076c_full_frequency_fixed_mode_flux_payment_independent_audit.md": "a24ebbf47641c706dd756ce23ba65f5b68c59010bfa1e65f829ae97d7022c358",
    "research/r076c_full_frequency_fixed_mode_flux_payment_qa_report.md": "ccea7ec3ec37ed32c3746d11f67f8e3eee0a66089a53934dbac5fa0005f3dfc6",
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
        "release": "R0.76C Step 54",
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
