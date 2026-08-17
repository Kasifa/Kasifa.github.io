#!/usr/bin/env python3
"""Audit the finite boundary faces of the compactified R0.20 model.

The ``p=0``, ``p=infinity``, ``q=0`` and ``q=infinity`` faces carry finite
rational limits of the target fraction.  The two ``x`` faces have target
fraction zero and are recorded separately.  On every finite face this script
constructs the exact two-variable stationary equations, removes their exact
common factor, and records the algebraic data needed for subsequent complete
positive-root isolation.

This script analyzes the finite fifth-order model only.  It is not a
Navier--Stokes regularity or singularity proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

import sympy as sp


P, Q, X = sp.symbols("p q x", positive=True)
VARIABLES = (P, Q, X)
FACES = ((0, "zero"), (0, "infinity"), (1, "zero"), (1, "infinity"))


def emit(stage: str, started: float, **fields: object) -> None:
    record = {
        "timestampUtc": datetime.now(timezone.utc).isoformat(),
        "elapsedSeconds": round(time.perf_counter() - started, 3),
        "stage": stage,
        **fields,
    }
    print(json.dumps(record, separators=(",", ":")), file=sys.stderr, flush=True)


def load_cache(path: Path) -> dict[str, object]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        payload = json.load(stream)
    if payload.get("schemaVersion") != 2:
        raise ValueError("R0.20 exact cache schema version 2 is required")
    return payload


def polynomial(rows: list[list[object]]) -> sp.Poly:
    expression = sp.Add(*(
        sp.Rational(int(row[3]), int(row[4]))
        * P ** int(row[0])
        * Q ** int(row[1])
        * X ** int(row[2])
        for row in rows
    ))
    return sp.Poly(expression, *VARIABLES, domain=sp.QQ)


def coefficient_face(source: sp.Poly, axis: int, side: str) -> sp.Poly:
    power = 0 if side == "zero" else source.degree(VARIABLES[axis])
    remaining = tuple(variable for index, variable in enumerate(VARIABLES) if index != axis)
    expression = sp.Add(*(
        coefficient
        * sp.prod(
            VARIABLES[index] ** powers[index]
            for index in range(3)
            if index != axis
        )
        for powers, coefficient in source.terms()
        if powers[axis] == power
    ))
    return sp.Poly(expression, *remaining, domain=sp.QQ)


def digest(source: sp.Poly) -> str:
    payload = "\n".join(
        f"{','.join(map(str, powers))}:{coefficient}"
        for powers, coefficient in source.terms()
    )
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def record(source: sp.Poly) -> dict[str, object]:
    return {
        "termCount": len(source.terms()),
        "degrees": [source.degree(variable) for variable in source.gens],
        "totalDegree": source.total_degree(),
        "exactDigest": digest(source),
    }


def factor_record(source: sp.Poly) -> dict[str, object]:
    unit, factors = sp.factor_list(source.as_expr())
    return {
        "unit": str(unit),
        "factors": [
            {
                "multiplicity": int(multiplicity),
                **record(sp.Poly(factor, *source.gens, domain=sp.QQ)),
            }
            for factor, multiplicity in factors
        ],
    }


def serialize(source: sp.Poly) -> list[list[object]]:
    return [
        [*powers, str(int(coefficient.p)), str(int(coefficient.q))]
        for powers, coefficient in source.terms()
    ]


def analyze_face(
    target: sp.Poly,
    total: sp.Poly,
    axis: int,
    side: str,
) -> tuple[dict[str, object], dict[str, object]]:
    target_face = coefficient_face(target, axis, side)
    total_face = coefficient_face(total, axis, side)
    variables = target_face.gens
    stationary = [
        sp.Poly(
            target_face.diff(variable).as_expr() * total_face.as_expr()
            - target_face.as_expr() * total_face.diff(variable).as_expr(),
            *variables,
            domain=sp.QQ,
        )
        for variable in variables
    ]
    common = sp.gcd(stationary[0], stationary[1])
    reduced = [sp.exquo(item, common) for item in stationary]
    reduced_gcd = sp.gcd(reduced[0], reduced[1])
    report = {
        "fixedVariable": str(VARIABLES[axis]),
        "side": side,
        "freeVariables": [str(variable) for variable in variables],
        "target": record(target_face),
        "total": record(total_face),
        "targetFactorization": factor_record(target_face),
        "stationary": [record(item) for item in stationary],
        "stationaryCommonFactor": {
            **record(common),
            "factorization": factor_record(common),
        },
        "reducedStationary": [record(item) for item in reduced],
        "reducedGcdConstant": reduced_gcd.total_degree() == 0,
    }
    exact = {
        "fixedVariable": str(VARIABLES[axis]),
        "side": side,
        "freeVariables": [str(variable) for variable in variables],
        "target": serialize(target_face),
        "total": serialize(total_face),
        "reducedStationary": [serialize(item) for item in reduced],
    }
    return report, exact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--exact-cache", type=Path)
    arguments = parser.parse_args()
    started = time.perf_counter()
    cache = load_cache(arguments.cache)
    target = polynomial(cache["polynomials"]["target"])
    external = polynomial(cache["polynomials"]["external"])
    total = target + external
    emit("loaded exact target and total", started)
    faces = []
    exact_faces: dict[str, object] = {}
    for axis, side in FACES:
        emit("analyzing finite face", started, variable=str(VARIABLES[axis]), side=side)
        report, exact = analyze_face(target, total, axis, side)
        faces.append(report)
        exact_faces[f"{VARIABLES[axis]}_{side}"] = exact
    result = {
        "schemaVersion": 1,
        "scope": "finite compactification-face stationary systems",
        "proofStatus": "exact construction only; positive roots not yet isolated",
        "zeroTargetFaces": ["x=0", "x=infinity"],
        "finiteFaces": faces,
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if arguments.exact_cache:
        arguments.exact_cache.parent.mkdir(parents=True, exist_ok=True)
        with gzip.open(arguments.exact_cache, "wt", encoding="utf-8", compresslevel=9) as stream:
            json.dump(
                {"schemaVersion": 1, "faces": exact_faces},
                stream,
                separators=(",", ":"),
            )
    emit("boundary algebra audit completed", started, faces=len(faces))


if __name__ == "__main__":
    main()
