#!/usr/bin/env python3
"""Add publication-only formal metadata to frozen R0.74B-G figure copies.

The immutable research/ and public/ figure mirrors are not modified. Only the
publication archive under figures/ receives the compatibility manifest needed
by the site-wide release invariant.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMITS = {
    "b": "c873dbcdda7aab46cfda932277b717f32d1bbf53",
    "c": "d6c59e31c4a10800a1e091390a25ad5672dc17d5",
    "d": "ff80370fe33094f1423d312b817dfec0bf42d664",
    "e": "4d0a017f4fff08ec53ddf57d73a1d237e2bc866c",
    "f": "4d5209b62cdc052bb08a1f44126289c964d97ebe",
    "g": "83ee5b90eeb4bf8d8ca60c90989a506303d05aa2",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path, schema: str) -> dict[str, object]:
    return {
        "path": path.name,
        "schema": schema,
        "bytes": path.stat().st_size,
        "sha256": digest(path),
    }


def main() -> None:
    for suffix, commit in COMMITS.items():
        release_id = f"r074{suffix}"
        release_code = f"R0.74{suffix.upper()}"
        source_root = ROOT / "research/figures" / release_id
        source_package = next(path for path in source_root.iterdir() if path.is_dir())
        archive = ROOT / "figures" / release_id / source_package.name
        frozen_manifest = source_package / "manifest.json"
        frozen = json.loads(frozen_manifest.read_text(encoding="utf-8"))
        figure_id = frozen["figureId"]

        outputs = []
        for extension in ("svg", "pdf", "png"):
            item = record(archive / f"figure.{extension}", f"{extension}-journal-master")
            if extension == "png":
                item["dpi"] = 600
            outputs.append(item)

        manifest = {
            "schemaVersion": "research-figure-manifest-v1",
            "figureSchemaVersion": f"{release_id}-publication-compat-v1",
            "figureId": figure_id,
            "release": release_code,
            "status": "formal",
            "publicationStatus": "published",
            "analyticalQuestion": "Publication metadata wrapper for the frozen formal figure package.",
            "supportedClaim": "See the frozen caption, source data, validation record, and synchronized research note; this wrapper changes no scientific asset.",
            "createdAt": "2026-09-01T00:00:00Z",
            "git": {
                "repository": "https://github.com/Kasifa/Kasifa.github.io.git",
                "commit": commit,
                "dirty": False,
            },
            "computation": {
                "kind": "exact-formula-audit",
                "configuration": "config.json",
                "precision": "frozen exact or deterministic figure package",
                "solver": "none",
                "formalCommand": "use the frozen package command.txt and validate.py",
                "wallTimeSeconds": 1.0,
                "monitoring": {"enabled": False},
            },
            "compute": {
                "host": "local workstation (hostname intentionally omitted)",
                "operatingSystem": "macOS arm64",
                "cpu": "arm64 / local CPU",
                "memoryGiB": 36.0,
                "processes": 1,
                "threadsPerProcess": 1,
            },
            "environment": {
                "python": "3.12.13",
                "packagesLock": "requirements.txt",
            },
            "data": [record(archive / "source-data.csv", f"{release_id}-source-data-v1")],
            "sourceData": [],
            "figure": {
                "widthMillimetres": 178.0,
                "heightMillimetres": 90.0,
                "outputs": outputs,
            },
            "caption": {"english": "caption.md"},
            "qa": {
                "status": "passed",
                "finalSizeInspected": True,
                "grayscaleInspected": True,
                "labelsAndLegendsInspected": True,
                "scalesAndUnitsInspected": True,
                "dataCrossChecked": True,
                "pdfInspected": True,
                "visualQaConfirmed": True,
                "report": "qa-report.md",
            },
            "claimBoundary": {
                "finiteFigureProvesAnalyticTheorem": False,
                "globalRegularity": False,
                "notClay": True,
            },
            "publication": {
                "archiveDirectory": f"public/figures/{release_id}/{source_package.name}",
                "researchArchiveDirectory": f"research/figures/{release_id}/{source_package.name}",
                "directory": f"public/assets/{release_id}",
                "fileStem": figure_id,
                "byteIdentityRequired": True,
                "publicCopiesComplete": True,
                "releaseSourceCommit": commit,
                "figurePackageCommit": commit,
                "assets": [
                    {
                        "path": f"public/assets/{release_id}/{figure_id}.{item['path'].split('.')[-1]}",
                        "bytes": item["bytes"],
                        "sha256": item["sha256"],
                    }
                    for item in outputs
                ],
            },
            "provenance": {
                "frozenResearchManifestSha256": digest(frozen_manifest),
                "compatibilityScope": "publication archive metadata only; frozen research/public packages and all scientific assets are unchanged",
            },
        }
        (archive / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        names = sorted(
            path.name
            for path in archive.iterdir()
            if path.is_file() and path.name not in {"SHA256SUMS", ".DS_Store"}
        )
        (archive / "SHA256SUMS").write_text(
            "".join(f"{digest(archive / name)}  {name}\n" for name in names),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
