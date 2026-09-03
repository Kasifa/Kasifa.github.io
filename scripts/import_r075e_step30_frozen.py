#!/usr/bin/env python3
"""Import only the ten frozen R0.75E Step 30 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075E_STEP30_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "aeaf5e588f2e606ee7deb960dd1f05fa4198e442"
HANDOFF_PATH = "research/r075e_publication_handoff.md"
HANDOFF_SHA256 = "c84b40e4833ebf9ce300ebd405c14605584aee84d0f890b48e17e9228f35d049"
HANDOFF_AUDIT_PATH = "research/r075e_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "5e16fceaa8f2127c817185cfc6c9e881c1068807f12cbea454d36aae2fb86795"

FROZEN = {
    "research/r075e_horizontal_cross_mode_flux_reduction.md": "99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049",
    "research/r075e_horizontal_cross_mode_flux_primary_audit.md": "da2778c1f0d5538981c517fccf75c96a635abbe7fae8833359c727dd2b301860",
    "research/r075e_report-source.md": "96577484d25745b419c30723c0af2d2873fbfff1f3340b79e1d7c9af71327199",
    "research/r075e_horizontal_cross_mode_flux_reduction_certificate.json": "682bdfadd6935e35c9ea85bfcfe9aa74ccbca8341f84791fe0885ee0f0e62946",
    "research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md": "6ffd2fb6601eae3e212ab1b989101eb6ca5e317cf4df9812a9926f6114ac79cf",
    "research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md": "a9d0b7410a6492ef699f1fbfc77906eb4bcadc1c9193887e8f3b8e5c5778d54c",
    "research/r075e_horizontal_cross_mode_flux_reduction_qa_report.md": "14f344f5876b8d016da2fbe0fc465b8c1685738f9fea6dcefaf5c406195c89b5",
    "scripts/r075e_horizontal_cross_mode_flux_reduction_certificate.py": "1d3eed137dc954bfcdfb6fe54ed6e1d3037f2bb18e297b3fb3264bbd8a2ad7ba",
    "scripts/r075e_horizontal_cross_mode_flux_reduction_certificate_independent.rb": "f6a85045c1737f7291441df9c9151d8f786510811f2333ec47843a8f16c2cb99",
    "scripts/r075e_horizontal_cross_mode_flux_reduction_qa.sh": "79065b938b264bc3422bed505f2f5a93f405fbb57bde2f598a7237bdba6d9ef1",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(relative: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), "show", f"{SOURCE_COMMIT}:{relative}"])


def write_exact(relative: str, data: bytes, expected: str) -> None:
    if sha256(data) != expected:
        raise SystemExit(f"source hash drift: {relative}")
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    if target.read_bytes() != data:
        raise SystemExit(f"import byte drift: {relative}")


def main() -> None:
    resolved = subprocess.check_output(
        ["git", "-C", str(SOURCE), "rev-parse", f"{SOURCE_COMMIT}^{{commit}}"], text=True
    ).strip()
    if resolved != SOURCE_COMMIT:
        raise SystemExit(f"frozen commit drift: {resolved}")
    if sha256((SOURCE / HANDOFF_PATH).read_bytes()) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256((SOURCE / HANDOFF_AUDIT_PATH).read_bytes()) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent audit drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75E Step 30",
        "source": SOURCE_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
