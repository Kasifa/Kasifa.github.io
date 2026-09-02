#!/usr/bin/env python3
"""Import the immutable R0.74S Step 16 package from its frozen commit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/Users/kasifa/Documents/Math/navier-stokes-r074m")
COMMIT = "159ea3c548e51b918512855cf79959460e882b48"
FILES = {
    "research/r074s_moving_frame_taylor_vortex_obstruction.md": "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0",
    "research/r074s_moving_frame_taylor_vortex_primary_audit.md": "1140e3f72ddf9565bb6e9c565aaf10de75c8f04b9417ad12e4cddffbabc9a262",
    "research/r074s_moving_frame_taylor_vortex_independent_audit.md": "30af657d18b428fa0355a8cd93a3cf7b7af452588561259ae53a9a734dc55da2",
    "research/r074s_moving_frame_taylor_vortex_certificate.json": "27f93a7e23268be2c337eef6ae0488a8fb60508c51f6dbf12080807e5f636271",
    "research/r074s_moving_frame_taylor_vortex_certificate_report.md": "9b2868d2e9a7cf0bd574ab347d266da1e30a1426c22d48a20f3a472557eab362",
    "scripts/r074s_moving_frame_taylor_vortex_certificate.py": "ec11a53bfc6221344eabd8b809c72deb8996adb56a2da81a6502bc7b914bb54a",
    "scripts/r074s_moving_frame_taylor_vortex_certificate_independent.rb": "9b1fcd3805e162bf7d8f24a2ed0818722dc9413ca709696380d0f02614892677",
}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(SOURCE), *args])


def main() -> None:
    head = git("rev-parse", "HEAD").decode().strip()
    if git("cat-file", "-t", COMMIT).decode().strip() != "commit":
        raise RuntimeError(f"frozen commit is unavailable: {COMMIT}")

    imported: list[dict[str, str | int]] = []
    for relative, expected in FILES.items():
        payload = git("show", f"{COMMIT}:{relative}")
        actual = hashlib.sha256(payload).hexdigest()
        if actual != expected:
            raise RuntimeError(f"frozen object hash drift: {relative}: {actual}")
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        imported.append({"path": relative, "sha256": actual, "bytes": len(payload)})

    if git("rev-parse", "HEAD").decode().strip() != head:
        raise RuntimeError("source HEAD changed during import")
    print(json.dumps({
        "source": str(SOURCE),
        "sourceHeadObserved": head,
        "commit": COMMIT,
        "readMode": "git-show-frozen-commit-only",
        "imported": imported,
    }, indent=2))


if __name__ == "__main__":
    main()
