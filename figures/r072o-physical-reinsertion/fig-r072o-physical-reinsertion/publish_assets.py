#!/usr/bin/env python3
"""Publish byte-identical R0.72O masters to public/assets/r072o."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    publication = config["publication"]
    destination = (REPOSITORY / publication["directory"]).resolve()
    repository = REPOSITORY.resolve()
    if destination != repository and repository not in destination.parents:
        raise ValueError("publication directory escapes repository")
    stem = str(publication["stem"])
    if not stem or Path(stem).name != stem:
        raise ValueError("publication stem must be one path-free stem")
    destination.mkdir(parents=True, exist_ok=True)
    published: dict[str, str] = {}
    for suffix in ("pdf", "svg", "png"):
        master = ROOT / f"figure.{suffix}"
        if not master.is_file():
            raise FileNotFoundError(master)
        target = destination / f"{stem}.{suffix}"
        shutil.copyfile(master, target)
        if digest(master) != digest(target):
            raise RuntimeError(f"published {suffix} differs from master")
        published[str(target.relative_to(REPOSITORY))] = digest(target)
    print(json.dumps({"published": published}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
