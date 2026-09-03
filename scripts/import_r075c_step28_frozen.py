#!/usr/bin/env python3
"""Import only the nine frozen R0.75C Step 28 whitelist objects."""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get("R075C_STEP28_SOURCE", "/Users/kasifa/Documents/Math/navier-stokes-r074m"))
SOURCE_COMMIT = "08d2e6e2e8abfead79d8ee47ee63156b5984672a"
HANDOFF_PATH = "research/r075c_publication_handoff.md"
HANDOFF_SHA256 = "6fd6741aed5d992da53dee6f3d1cb02b67bad1c912c9843dcc371cb299cc0910"
HANDOFF_AUDIT_PATH = "research/r075c_publication_handoff_independent_audit.md"
HANDOFF_AUDIT_SHA256 = "30bf74a2041b4e5ddcc28feef8e8e747c6443a0593395639e5f31ae205be83cb"

FROZEN = {
    "research/r075c_background_shear_packing_false_positive.md": "1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89",
    "research/r075c_background_shear_packing_false_positive_primary_audit.md": "b3e1bc0b8e321e2a1bce0dafc74d21ad1f81048b63ab93f42f56e2c2a0760368",
    "research/r075c_background_shear_packing_false_positive_certificate.json": "d57a3d6d400dcd805c09e34ef7c2bec8b4abb35e8478a1e275f3a1324552355f",
    "research/r075c_background_shear_packing_false_positive_certificate_report.md": "5f91ed6b135a196849b26635a505ab809528c593db846e65a41569e13f166f50",
    "research/r075c_background_shear_packing_false_positive_independent_audit.md": "842b87327598c5458cc24937ea8def035886b9134221e77612bc778a2a3f4b8b",
    "research/r075c_background_shear_packing_false_positive_qa_report.md": "13f047fef4fb5934885d78a32f7ffcdc9a7e71eaa58b6afdbf92a965cc0c1afe",
    "scripts/r075c_background_shear_packing_false_positive_certificate.py": "2c75ae98b5ffb4c7c7b4c911758656db47ea349ec91e8c823d9309641853d010",
    "scripts/r075c_background_shear_packing_false_positive_certificate_independent.rb": "b9b8202a2d82cb5a735051cffe2ed4428f307f38c54e67a413adbd9ce20ea76b",
    "scripts/r075c_background_shear_packing_false_positive_qa.sh": "2282c525858c552c4151e4e5f65a83d3098a1d34f5afd50b02a44455fbbe98bb",
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
        "release": "R0.75C Step 28",
        "source": SOURCE_COMMIT,
        "handoffSha256": HANDOFF_SHA256,
        "handoffAuditSha256": HANDOFF_AUDIT_SHA256,
        "frozenFiles": len(FROZEN),
        "formalFigureRequired": False,
        "recapRequired": False,
    })


if __name__ == "__main__":
    main()
