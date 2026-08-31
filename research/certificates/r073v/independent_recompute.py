#!/usr/bin/env python3
"""Independently recompute the R0.73V common core.

This path does not import the primary producer.  It represents q-polynomials
as dense tuples, constructs Fourier products through explicit ordered mode
pairs, and binds the complete Germano tables by a canonical SHA-256 digest.
All decisions use fractions.Fraction and exact Gaussian rationals.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Iterable


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "independent-results.json"
F = Fraction
Mode = tuple[int, int, int]
G = tuple[Fraction, Fraction]
Dense = tuple[G, ...]
Field = dict[Mode, Dense]
O: G = (F(0), F(0))


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canon(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def zz(a: int | Fraction = 0, b: int | Fraction = 0) -> G:
    return F(a), F(b)


def ga(a: G, b: G) -> G:
    return a[0] + b[0], a[1] + b[1]


def gn(a: G) -> G:
    return -a[0], -a[1]


def gm(a: G, b: G) -> G:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def gs(a: G, scalar: int | Fraction) -> G:
    scalar = F(scalar)
    return a[0] * scalar, a[1] * scalar


def gc(a: G) -> G:
    return a[0], -a[1]


def gtext(a: G) -> str:
    real, imag = a
    if imag == 0:
        return str(real)
    if real == 0:
        if imag == 1:
            return "i"
        if imag == -1:
            return "-i"
        return str(imag) + "*i"
    sign = "+" if imag > 0 else "-"
    magnitude = abs(imag)
    return str(real) + sign + ("i" if magnitude == 1 else str(magnitude) + "*i")


def trim(a: Iterable[G]) -> Dense:
    values = list(a)
    while values and values[-1] == O:
        values.pop()
    return tuple(values)


def dc(a: G) -> Dense:
    return () if a == O else (a,)


def da(a: Dense, b: Dense) -> Dense:
    size = max(len(a), len(b))
    return trim(ga(a[index] if index < len(a) else O, b[index] if index < len(b) else O)
                for index in range(size))


def dn(a: Dense) -> Dense:
    return tuple(gn(value) for value in a)


def ds(a: Dense, scalar: G) -> Dense:
    return trim(gm(value, scalar) for value in a)


def dm(a: Dense, b: Dense) -> Dense:
    if not a or not b:
        return ()
    result = [O] * (len(a) + len(b) - 1)
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            result[i + j] = ga(result[i + j], gm(left, right))
    return trim(result)


def shift(a: Dense, count: int) -> Dense:
    return () if not a else tuple([O] * count + list(a))


def deval(a: Dense, value: Fraction) -> G:
    total = O
    power = F(1)
    for coefficient in a:
        total = ga(total, gs(coefficient, power))
        power *= value
    return total


def dderivative(a: Dense) -> Dense:
    return trim(gs(a[index], index) for index in range(1, len(a)))


def small(a: Dense) -> dict[str, object]:
    if not a:
        return {"leadingCoefficient": "0", "order": "infinity"}
    work = a
    order = 0
    value = deval(work, F(1))
    while value == O:
        work = dderivative(work)
        order += 1
        need(bool(work), "dense multiplicity failure")
        value = deval(work, F(1))
    factorial = 1
    for integer in range(2, order + 1):
        factorial *= integer
    return {
        "leadingCoefficient": gtext(gs(value, F((-1) ** order, factorial))),
        "order": order,
    }


def dense_json(a: Dense) -> dict[str, object]:
    return {
        "coefficients": {str(index): gtext(value) for index, value in enumerate(a) if value != O},
        "smallS": small(a),
    }


def mk(a: Mode) -> str:
    return ",".join(str(value) for value in a)


def plus(a: Mode, b: Mode) -> Mode:
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


def minus(a: Mode) -> Mode:
    return -a[0], -a[1], -a[2]


def square(a: Mode) -> int:
    return a[0] ** 2 + a[1] ** 2 + a[2] ** 2


def clean(a: Field) -> Field:
    return {mode: trim(poly) for mode, poly in a.items() if trim(poly)}


def fa(a: Field, b: Field) -> Field:
    answer = dict(a)
    for mode, poly in b.items():
        answer[mode] = da(answer.get(mode, ()), poly)
    return clean(answer)


def fn(a: Field) -> Field:
    return {mode: dn(poly) for mode, poly in a.items()}


def fs(a: Field, scalar: G) -> Field:
    return clean({mode: ds(poly, scalar) for mode, poly in a.items()})


def product(a: Field, b: Field) -> Field:
    answer: Field = {}
    for pair in ((left, right) for left in sorted(a) for right in sorted(b)):
        left, right = pair
        mode = plus(left, right)
        answer[mode] = da(answer.get(mode, ()), dm(a[left], b[right]))
    return clean(answer)


def filtered(a: Field) -> Field:
    return {mode: shift(poly, square(mode)) for mode, poly in a.items()}


def dx(a: Field, index: int) -> Field:
    return clean({mode: ds(poly, zz(0, mode[index])) for mode, poly in a.items()})


def at(a: Field, mode: Mode) -> Dense:
    return a.get(mode, ())


def velocity(positive: dict[Mode, tuple[G, G, G]]) -> list[Field]:
    result: list[Field] = [{}, {}, {}]
    for mode in sorted(positive):
        for component in range(3):
            result[component][mode] = dc(positive[mode][component])
            result[component][minus(mode)] = dc(gc(positive[mode][component]))
    return result


def four() -> list[Field]:
    return velocity({
        (1, 0, 0): (zz(), zz(0, -1), zz()),
        (1, 1, 0): (zz(0, -1), zz(0, 1), zz()),
    })


def six() -> list[Field]:
    return velocity({
        (0, 1, 0): (zz(0, -3), zz(), zz()),
        (1, 0, 0): (zz(), zz(0, -2), zz()),
        (1, 1, 0): (zz(0, 2), zz(0, -2), zz()),
    })


def tensor(u: list[Field]) -> list[list[Field]]:
    return [[product(u[i], u[j]) for j in range(3)] for i in range(3)]


def pressure(u: list[Field]) -> Field:
    uu = tensor(u)
    modes = set().union(*(entry.keys() for row in uu for entry in row))
    answer: Field = {}
    for mode in modes:
        denominator = square(mode)
        if denominator == 0:
            continue
        coefficient: Dense = ()
        for i in range(3):
            for j in range(3):
                coefficient = da(coefficient, ds(at(uu[i][j], mode), zz(F(-mode[i] * mode[j], denominator))))
        if coefficient:
            answer[mode] = coefficient
    return answer


def strain(u: list[Field]) -> list[list[Field]]:
    return [[fs(fa(dx(u[j], i), dx(u[i], j)), zz(F(1, 2))) for j in range(3)] for i in range(3)]


def nonlinear(u: list[Field]) -> list[Field]:
    uu = tensor(u)
    p = pressure(u)
    answer: list[Field] = []
    for i in range(3):
        entry: Field = {}
        for k in range(3):
            entry = fa(entry, dx(uu[i][k], k))
        answer.append(fa(entry, dx(p, i)))
    return answer


def cov(a: Field, b: Field) -> Field:
    return fa(filtered(product(a, b)), fn(product(filtered(a), filtered(b))))


def cum3(a: Field, b: Field, c: Field) -> Field:
    answer = filtered(product(product(a, b), c))
    answer = fa(answer, fn(product(filtered(a), filtered(product(b, c)))))
    answer = fa(answer, fn(product(filtered(b), filtered(product(a, c)))))
    answer = fa(answer, fn(product(filtered(c), filtered(product(a, b)))))
    answer = fa(answer, fs(product(product(filtered(a), filtered(b)), filtered(c)), zz(2)))
    return answer


def kappa(u: list[Field]) -> list[list[list[Field]]]:
    return [[[cum3(u[i], u[j], u[k]) for k in range(3)] for j in range(3)] for i in range(3)]


def qb(u: list[Field], p: Field) -> list[Field]:
    return [cov(p, u[i]) for i in range(3)]


def rb(u: list[Field], p: Field) -> list[list[Field]]:
    ss = strain(u)
    return [[cov(p, ss[i][j]) for j in range(3)] for i in range(3)]


def mz() -> list[list[Dense]]:
    return [[() for _ in range(3)] for _ in range(3)]


def ma(a: list[list[Dense]], b: list[list[Dense]]) -> list[list[Dense]]:
    return [[da(a[i][j], b[i][j]) for j in range(3)] for i in range(3)]


def mn(a: list[list[Dense]]) -> list[list[Dense]]:
    return [[dn(a[i][j]) for j in range(3)] for i in range(3)]


def ms(a: list[list[Dense]], scalar: G) -> list[list[Dense]]:
    return [[ds(a[i][j], scalar) for j in range(3)] for i in range(3)]


def mat_at(a: list[list[Field]], mode: Mode) -> list[list[Dense]]:
    return [[at(a[i][j], mode) for j in range(3)] for i in range(3)]


def flux(a: list[list[list[Field]]], mode: Mode) -> list[list[Dense]]:
    answer = mz()
    for i in range(3):
        for j in range(3):
            for k in range(3):
                answer[i][j] = da(answer[i][j], ds(at(a[i][j][k], mode), zz(0, -mode[k])))
    return answer


def qdiv(a: list[Field], mode: Mode) -> list[list[Dense]]:
    return [[
        da(ds(at(a[j], mode), zz(0, -mode[i])), ds(at(a[i], mode), zz(0, -mode[j])))
        for j in range(3)
    ] for i in range(3)]


def mat_json(a: list[list[Dense]]) -> list[list[dict[str, object]]]:
    return [[dense_json(a[i][j]) for j in range(3)] for i in range(3)]


def sparse(a: Field) -> dict[str, object]:
    return {mk(mode): dense_json(poly) for mode, poly in sorted(clean(a).items())}


def kappa_json(a: list[list[list[Field]]]) -> dict[str, object]:
    answer: dict[str, object] = {}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if clean(a[i][j][k]):
                    answer[f"{i + 1}{j + 1}{k + 1}"] = sparse(a[i][j][k])
    return answer


def vector_json(a: list[Field]) -> dict[str, object]:
    return {str(i + 1): sparse(entry) for i, entry in enumerate(a) if clean(entry)}


def matrix_field_json(a: list[list[Field]], scalar: G) -> dict[str, object]:
    answer: dict[str, object] = {}
    for i in range(3):
        for j in range(3):
            entry = fs(a[i][j], scalar)
            if clean(entry):
                answer[f"{i + 1}{j + 1}"] = sparse(entry)
    return answer


def digest(value: object) -> str:
    return hashlib.sha256(canon(value).encode("utf-8")).hexdigest()


def compressed(u: list[Field], mode: Mode) -> dict[str, list[list[Dense]]]:
    nn = nonlinear(u)
    c_fields = [[filtered(fa(product(u[i], nn[j]), product(nn[i], u[j]))) for j in range(3)] for i in range(3)]
    vu = [filtered(entry) for entry in u]
    nv = [filtered(entry) for entry in nn]
    resolved_fields = [[fa(product(vu[i], nv[j]), product(nv[i], vu[j])) for j in range(3)] for i in range(3)]
    c = mat_at(c_fields, mode)
    resolved = mat_at(resolved_fields, mode)
    return {"Ccal": c, "resolved": resolved, "chi": ma(c, mn(resolved))}


def xi_groups(p: Field, u: list[Field]) -> dict[int, list[list[Dense]]]:
    ss = strain(u)
    answer: dict[int, list[list[Dense]]] = {}
    for mode in sorted(p):
        opposite = minus(mode)
        if not any(at(ss[i][j], opposite) for i in range(3) for j in range(3)):
            continue
        group = square(mode)
        answer.setdefault(group, mz())
        weight = tuple([zz(1)] + [O] * (2 * group - 1) + [zz(-1)])
        for i in range(3):
            for j in range(3):
                answer[group][i][j] = da(
                    answer[group][i][j],
                    ds(dm(dm(at(p, mode), at(ss[i][j], opposite)), weight), zz(2)),
                )
    return answer


def quartic(u: list[Field]) -> Field:
    nn = nonlinear(u)
    answer: Field = {}
    for term in (cum3(nn[0], u[0], u[1]), cum3(u[0], nn[0], u[1]), cum3(u[0], u[0], nn[1])):
        answer = fa(answer, fn(term))
    return answer


def epsilon(u: list[Field], mode: Mode) -> dict[str, object]:
    nn = nonlinear(u)
    samples: dict[int, G] = {}
    for e in (0, 1, 2, 3):
        perturbed = [fa(u[index], fs(nn[index], zz(-e))) for index in range(3)]
        samples[e] = deval(at(cum3(perturbed[0], perturbed[0], perturbed[1]), mode), F(1, 2))
    extracted = O
    for e, weight in ((0, F(-11, 6)), (1, F(3)), (2, F(-3, 2)), (3, F(1, 3))):
        extracted = ga(extracted, gs(samples[e], weight))
    return {
        "extractedLinearCoefficient": gtext(extracted),
        "formula": "(-11*f(0)+18*f(1)-9*f(2)+2*f(3))/6",
        "q": "1/2",
        "samples": {str(e): gtext(samples[e]) for e in samples},
    }


def build() -> dict[str, object]:
    u4 = four()
    p4 = pressure(u4)
    k4 = kappa(u4)
    q4 = qb(u4, p4)
    r4 = rb(u4, p4)
    target = (1, 2, 0)
    local = flux(k4, target)
    pressure_row = qdiv(q4, target)
    xi = ms(mat_at(r4, target), zz(2))
    signed = ma(ma(local, pressure_row), xi)
    comp = compressed(u4, target)
    tables = {
        "Q": vector_json(q4),
        "XiEquals2R": matrix_field_json(r4, zz(2)),
        "kappa": kappa_json(k4),
    }

    u6 = six()
    p6 = pressure(u6)
    k6 = kappa(u6)
    q6 = qb(u6, p6)
    r6 = rb(u6, p6)
    zero = (0, 0, 0)
    local6 = flux(k6, zero)
    pressure6 = qdiv(q6, zero)
    xi6 = ms(mat_at(r6, zero), zz(2))
    groups = xi_groups(p6, u6)

    quartic_poly = at(quartic(u4), (0, 2, 0))
    core = {
        "compressedTarget": {
            "Ccal": mat_json(comp["Ccal"]),
            "chi": mat_json(comp["chi"]),
            "resolved": mat_json(comp["resolved"]),
            "signPairDifference": mat_json(ms(comp["chi"], zz(2))),
        },
        "fourSiteTarget": {
            "localKappaFlux": mat_json(local),
            "pressureDiffusion": mat_json(pressure_row),
            "pressureStrainXi": mat_json(xi),
            "signedStressSource": mat_json(signed),
        },
        "quarticSelected": {
            "coefficient": dense_json(quartic_poly),
            "finiteEpsilonAtQHalf": epsilon(u4, (0, 2, 0)),
            "index": "kappa112",
            "mode": [0, 2, 0],
        },
        "sixSiteZeroMode": {
            "contractedKappaFlux": mat_json(local6),
            "pressureDiffusion": mat_json(pressure6),
            "pressureStrainXi": mat_json(xi6),
            "pressureStrainXiByInputNormSquared": {
                str(group): mat_json(matrix) for group, matrix in sorted(groups.items())
            },
        },
        "tableDigest": digest(tables),
    }
    need(core["tableDigest"] == "a7494d44f45b1249a513ac4d44476b7ce5af622b0d59928f4e4631d9715c22f7",
         "complete-table digest drift")
    need(quartic_poly == (O, O, zz(0, 2), O, zz(0, -4), O, zz(0, 2)),
         "quartic polynomial drift")
    need(core["quarticSelected"]["finiteEpsilonAtQHalf"]["extractedLinearCoefficient"] == "9/32*i",
         "finite-epsilon extraction drift")
    return {
        "arithmetic": "independent dense Fraction/Gaussian q-polynomials; no floating point",
        "commonCore": core,
        "independence": {
            "importsPrimaryProducer": False,
            "polynomialRepresentation": "trimmed dense coefficient tuples",
            "standardLibraryOnly": True,
        },
        "producer": {
            "dgx": "not used",
            "floatingPoint": "not used",
            "gpu": "not used",
            "network": "not used",
            "scriptSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    }


def arguments(values: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args(values)


def main(values: Iterable[str] | None = None) -> int:
    options = arguments(values)
    result = build()
    text = canon(result)
    if options.check_only:
        need(OUTPUT.is_file() and not OUTPUT.is_symlink(), "missing independent-results.json")
        need(OUTPUT.read_text(encoding="utf-8") == text, "independent-results.json is stale")
        mode = "check-only"
    else:
        OUTPUT.write_text(text, encoding="utf-8")
        mode = "write"
    print("R073V_INDEPENDENT_RECOMPUTE=PASS mode=" + mode + " tableDigest=" + result["commonCore"]["tableDigest"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print("R073V_INDEPENDENT_RECOMPUTE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
