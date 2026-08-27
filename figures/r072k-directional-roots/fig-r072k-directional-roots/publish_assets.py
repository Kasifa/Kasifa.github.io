#!/usr/bin/env python3
"""Publish byte-identical R0.72K masters to public/figures."""

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
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> None:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    publication = config["publication"]
    destination = (REPOSITORY / publication["directory"]).resolve()
    repository = REPOSITORY.resolve()
    if destination != repository and repository not in destination.parents:
        raise ValueError("publication directory escapes the repository")

    stem = str(publication["stem"])
    if not stem or Path(stem).name != stem:
        raise ValueError("publication stem must be one path-free file stem")

    masters = [ROOT / f"figure.{suffix}" for suffix in ("pdf", "svg", "png")]
    missing = [path.name for path in masters if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing figure masters: {missing}")

    destination.mkdir(parents=True, exist_ok=True)
    published: dict[str, str] = {}
    for master in masters:
        target = destination / f"{stem}{master.suffix}"
        shutil.copyfile(master, target)
        source_hash = digest(master)
        target_hash = digest(target)
        if source_hash != target_hash:
            raise RuntimeError(f"published copy differs from {master.name}")
        published[str(target.relative_to(REPOSITORY))] = target_hash

    print(json.dumps({"published": published}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
