#!/usr/bin/env python3
"""Compute exact bidirectional resultants for the R0.20 finite faces.

For each two-variable reduced stationary system this script eliminates either
free variable, square-free factorizes the resulting univariate polynomial,
and uses exact Sturm counting on the positive half-line.  Resultant roots are
candidate coordinate values; leading-coefficient artifacts and incompatible
coordinate pairings must still be removed by a later common-root isolation.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import gzip
import hashlib
import json
import os
from pathlib import Path
import sys
import time

import sympy as sp


def emit(stage: str, started: float, **fields: object) -> None:
    record = {
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "elapsedSeconds": round(time.perf_counter() - started, 3),
        "stage": stage,
        **fields,
    }
    print(json.dumps(record, separators=(",", ":")), file=sys.stderr, flush=True)


def load(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schemaVersion") != 1:
        raise ValueError("R0.20 boundary cache schema version 1 is required")
    return payload


def parse(rows: list[list[object]], variables: tuple[sp.Symbol, sp.Symbol]) -> sp.Poly:
    expression = sp.Add(*(
        sp.Rational(int(row[2]), int(row[3]))
        * variables[0] ** int(row[0])
        * variables[1] ** int(row[1])
        for row in rows
    ))
    return sp.Poly(expression, *variables, domain=sp.QQ)


def serialize(source: sp.Poly) -> list[list[str]]:
    return [
        [str(powers[0]), str(int(coefficient.p)), str(int(coefficient.q))]
        for powers, coefficient in source.terms()
    ]


def digest(source: sp.Poly) -> str:
    payload = "\n".join(
        f"{powers[0]}:{coefficient}" for powers, coefficient in source.terms()
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def resultant_record(source: sp.Poly) -> dict[str, object]:
    square_free = source.sqf_part()
    _unit, factors = sp.factor_list(source.as_expr())
    return {
        "degree": source.degree(),
        "termCount": len(source.terms()),
        "exactDigest": digest(source),
        "squareFreeDegree": square_free.degree(),
        "positiveRealRootCountWithMultiplicity": int(source.count_roots(0, sp.oo)),
        "positiveDistinctRootCount": int(square_free.count_roots(0, sp.oo)),
        "factors": [
            {
                "degree": sp.Poly(factor, source.gens[0], domain=sp.QQ).degree(),
                "multiplicity": int(multiplicity),
            }
            for factor, multiplicity in factors
        ],
    }


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, separators=(",", ":")) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def compute_task(
    face_name: str,
    face: dict[str, object],
    keep_axis: int,
    checkpoint_name: str,
) -> dict[str, object]:
    checkpoint = Path(checkpoint_name)
    if checkpoint.exists():
        return json.loads(checkpoint.read_text(encoding="utf-8"))
    variables = tuple(sp.symbols(" ".join(face["freeVariables"])))
    functions = [parse(rows, variables) for rows in face["reducedStationary"]]
    eliminate_axis = 1 - keep_axis
    keep = variables[keep_axis]
    eliminate = variables[eliminate_axis]
    started = time.perf_counter()
    expression = sp.resultant(
        functions[0].as_expr(),
        functions[1].as_expr(),
        eliminate,
    )
    result = sp.Poly(expression, keep, domain=sp.QQ)
    value = {
        "face": face_name,
        "keep": str(keep),
        "eliminate": str(eliminate),
        "report": resultant_record(result),
        "exact": serialize(result),
        "wallSeconds": time.perf_counter() - started,
    }
    checkpoint.parent.mkdir(parents=True, exist_ok=True)
    atomic_json(checkpoint, value)
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--exact-cache", type=Path, required=True)
    parser.add_argument("--checkpoint-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    arguments = parser.parse_args()
    started = time.perf_counter()
    payload = load(arguments.cache)
    arguments.checkpoint_dir.mkdir(parents=True, exist_ok=True)
    tasks = []
    for face_name, face in payload["faces"].items():
        for keep_axis, keep in enumerate(face["freeVariables"]):
            checkpoint = arguments.checkpoint_dir / f"{face_name}-keep-{keep}.json"
            tasks.append((face_name, face, keep_axis, str(checkpoint)))
    emit("starting parallel boundary resultants", started, tasks=len(tasks), workers=arguments.workers)
    values = []
    with ProcessPoolExecutor(max_workers=arguments.workers) as executor:
        futures = [executor.submit(compute_task, *task) for task in tasks]
        for future in as_completed(futures):
            value = future.result()
            values.append(value)
            emit(
                "resultant checkpoint completed",
                started,
                face=value["face"],
                keep=value["keep"],
                degree=value["report"]["degree"],
                taskWallSeconds=round(value["wallSeconds"], 3),
                completed=len(values),
                tasks=len(tasks),
            )
    reports: dict[str, object] = {
        face_name: {"freeVariables": face["freeVariables"]}
        for face_name, face in payload["faces"].items()
    }
    exact: dict[str, object] = {face_name: {} for face_name in payload["faces"]}
    for value in values:
        reports[value["face"]][value["keep"]] = value["report"]
        exact[value["face"]][value["keep"]] = value["exact"]
    output = {
        "schemaVersion": 1,
        "scope": "finite-face exact bidirectional resultants",
        "proofStatus": "exact coordinate candidate counts; common-root pairing pending",
        "faces": reports,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    arguments.exact_cache.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(arguments.exact_cache, "wt", encoding="utf-8", compresslevel=9) as stream:
        json.dump({"schemaVersion": 1, "resultants": exact}, stream, separators=(",", ":"))
    emit("all boundary resultants completed", started, faces=len(reports))


if __name__ == "__main__":
    main()
