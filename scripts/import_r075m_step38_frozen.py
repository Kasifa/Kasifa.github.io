#!/usr/bin/env python3
"""Import only the twelve frozen R0.75M Step 38 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075M_STEP38_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "decc558786108fd1ce4a7f86d906d12c4eb61a25"
HANDOFF_COMMIT = "138b2081c18bdd4409b354bfe2aeea86db6ce185"
HANDOFF_PATH = "research/r075m_publication_handoff.md"
HANDOFF_SHA256 = "89f814a6c52ce6c4d2a52eedff9042eaaff00fb9fbe44028d398679da6f12d85"
HANDOFF_AUDIT_PATH = "research/r075m_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "fd8ba9ebb88a478d091c7a8535386c920a0f8964b7c91b4f4317488770633589"

FROZEN = {
    "research/r075m_dyadic_packet_diffusive_flux_gain.md": "13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7",
    "research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md": "2b5ee050c09e3be925143c12c29082c3fe562a83b9a2d2669511a2bb1684d7dc",
    "research/r075m_report-source.md": "f8ed7af8ef5051b0efa73177d0530562917d55dfa6476b00b8f871db0da99d67",
    "scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json": "b93d727b4bf0729af2064e51fbc0c1450d98806c9b92fe11727b4d5423fa157f",
    "scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json": "cef1705998bc935448f371d6f389d46059b59e99bf230bd75dad0489fb85a4f4",
    "research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json": "1794cee5294ed55a41697f74d6a4b0bbb5e31e59b3a74ed11f277d0ae8e17423",
    "research/r075m_dyadic_packet_diffusive_flux_gain_certificate_report.md": "cd2882d59ec90471d1e74cb135426490c46863fbf6e6df3db3532926aaa5002f",
    "research/r075m_dyadic_packet_diffusive_flux_gain_independent_audit.md": "507fdbb899f0e74abccc0477405949ca07f9379d4b20ce20ab3bd87e63a76881",
    "research/r075m_dyadic_packet_diffusive_flux_gain_qa_report.md": "b7513c9ee3660a21473f7ea87a19d4ae0f70aa6a99ceb88b397d159e7a56bad0",
    "scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate.py": "8a55852a3eabcf8989feadcb25cb178db57b1dccbd2249e73d48e61e7755811b",
    "scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate_independent.rb": "6436063bc4ec623dfc27d7fc3edee8ee6751784f8a43ecdd5aa1b4170b35dd1b",
    "scripts/r075m_dyadic_packet_diffusive_flux_gain_qa.sh": "9e61cb0e57f4116e371beda1d6709ca479ea146538758287d6451b2641e87cf2",
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
    for commit in (SOURCE_COMMIT, HANDOFF_COMMIT):
        resolved = subprocess.check_output(
            ["git", "-C", str(SOURCE), "rev-parse", f"{commit}^{{commit}}"], text=True
        ).strip()
        if resolved != commit:
            raise SystemExit(f"frozen commit drift: {resolved}")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_PATH)) != HANDOFF_SHA256:
        raise SystemExit("handoff drift")
    if sha256(git_bytes(HANDOFF_COMMIT, HANDOFF_AUDIT_PATH)) != HANDOFF_AUDIT_SHA256:
        raise SystemExit("handoff independent audit drift")
    for relative, expected in FROZEN.items():
        write_exact(relative, git_bytes(SOURCE_COMMIT, relative), expected)
    print({
        "status": "PASS",
        "release": "R0.75M Step 38",
        "source": SOURCE_COMMIT,
        "handoffCommit": HANDOFF_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
