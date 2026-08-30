#!/usr/bin/env python3
"""Independent alias-free vorticity/FFT validation of R0.73H finite data.

This script does not import the primary producer.  It independently rebuilds
the frozen Orr--Sommerfeld matrix, uses scalar vorticity and Biot--Savart
recovery, evaluates products on an alias-free physical grid, and compares raw
complex endpoint coefficients against the primary archive.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "research/certificates/r073h/README.md",
    "research/certificates/r073h/command.txt",
    "research/certificates/r073h/config.json",
    "research/certificates/r073h/requirements.txt",
    "research/certificates/r073h/exact_q2_certificate.py",
    "research/certificates/r073h/independent_exact_q2.py",
    "research/certificates/r073h/primary_diagnostic.py",
    "research/certificates/r073h/independent_validate.py",
    "research/certificates/r073h/generate_certificate.py",
    "research/certificates/r073h/validate_certificate.py",
    "research/certificates/r073h/seal_package.py",
)
KZ_MAX = 3
MU = 0.25


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--primary-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import numpy as np  # noqa: E402
from scipy.linalg import eig  # noqa: E402


START = time.perf_counter()
SEQUENCE = 0
PROGRESS = ARGS.output.resolve().with_name("independent_progress.ndjson")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def emit(event: str, **fields: object) -> None:
    global SEQUENCE
    SEQUENCE += 1
    row = {
        "sequence": SEQUENCE,
        "timestampUtc": now_utc(),
        "elapsedSeconds": round(time.perf_counter() - START, 6),
        "event": event,
        **fields,
    }
    line = json.dumps(row, sort_keys=True, allow_nan=False)
    print(line, flush=True)
    with PROGRESS.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


def source_gate(source_commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("formal validation requires a full lowercase source commit")
    resolved = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{source_commit}^{{commit}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if resolved != source_commit:
        raise RuntimeError("source commit did not resolve exactly")
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", source_commit, head],
        check=False,
    ).returncode != 0:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        tree = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", source_commit, relative],
            check=True, capture_output=True, text=True,
        ).stdout.split()
        if len(tree) < 3 or tree[0] not in {"100644", "100755"}:
            raise RuntimeError(f"source is not a regular Git blob: {relative}")
        committed = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{source_commit}:{relative}"],
            check=True, capture_output=True,
        ).stdout
        if committed != path.read_bytes():
            raise RuntimeError(f"working source differs from source commit: {relative}")
        working = path.read_bytes()
        bindings.append({
            "path": relative,
            "gitMode": tree[0],
            "bytes": len(working),
            "sha256": hashlib.sha256(working).hexdigest(),
        })
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtRun": head,
        "sourceCommitIsAncestorOfHead": True,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def matrix_from_os_formula(n_cut: int, epsilon_nu: float) -> np.ndarray:
    gamma = 0.5
    modes = np.arange(-n_cut, n_cut + 1, dtype=int)
    lam = modes.astype(float) ** 2 + MU
    shifts = modes[:, None] - modes[None, :]
    w_hat = {1: 0.25j, -1: -0.25j, 2: -0.125j, -2: 0.125j}
    wxx_hat = {1: -0.25j, -1: 0.25j, 2: 0.5j, -2: -0.5j}
    w = np.zeros(shifts.shape, dtype=np.complex128)
    wxx = np.zeros_like(w)
    for shift, value in w_hat.items():
        w[shifts == shift] = value
    for shift, value in wxx_hat.items():
        wxx[shifts == shift] = value
    raw = -1j * gamma * (w + wxx / lam[None, :])
    transformed = (1.0 / np.sqrt(lam))[:, None] * raw * np.sqrt(lam)[None, :]
    transformed -= epsilon_nu * np.diag(lam)
    return transformed


def canonical_top(matrix: np.ndarray) -> np.ndarray:
    values, vectors = eig(matrix, left=False, right=True, check_finite=False)
    top_real = float(np.max(values.real))
    candidates = np.flatnonzero(values.real >= top_real - 1.0e-8)
    selected = max(
        (int(index) for index in candidates),
        key=lambda index: (float(values[index].real), float(values[index].imag)),
    )
    vector = np.asarray(vectors[:, selected], dtype=np.complex128)
    vector /= np.linalg.norm(vector)
    anchor = int(np.argmax(np.abs(vector)))
    vector *= np.exp(-1j * np.angle(vector[anchor]))
    if vector[anchor].real < 0.0:
        vector *= -1.0
    return vector


class VorticityFFT:
    def __init__(self, n_cut: int):
        self.n_cut = n_cut
        self.n = np.arange(-n_cut, n_cut + 1, dtype=int)
        self.kz = np.arange(-KZ_MAX, KZ_MAX + 1, dtype=int)
        self.ny = 8 * n_cut + 8
        self.nz = 16
        self.normalization = self.ny * self.nz
        self.ky_full = np.fft.fftfreq(self.ny, d=1.0 / self.ny)
        self.kz_full = np.fft.fftfreq(self.nz, d=1.0 / self.nz)
        self.ky_grid = self.ky_full[:, None]
        self.kz_grid = self.kz_full[None, :]
        self.wave_squared = self.ky_grid**2 + self.kz_grid**2

    def embed(self, coefficients: np.ndarray) -> np.ndarray:
        full = np.zeros((self.ny, self.nz), dtype=np.complex128)
        for kz_index, kz in enumerate(self.kz):
            for index, n_mode in enumerate(self.n):
                full[(2 * int(n_mode)) % self.ny, int(kz) % self.nz] = coefficients[kz_index, index]
        return full

    def extract(self, full: np.ndarray) -> np.ndarray:
        coefficients = np.zeros((len(self.kz), len(self.n)), dtype=np.complex128)
        for kz_index, kz in enumerate(self.kz):
            for index, n_mode in enumerate(self.n):
                coefficients[kz_index, index] = full[(2 * int(n_mode)) % self.ny, int(kz) % self.nz]
        return coefficients

    def physical(self, full: np.ndarray) -> np.ndarray:
        return np.fft.ifftn(full * self.normalization)

    def velocity_full(self, omega_full: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u2 = np.zeros_like(omega_full)
        u3 = np.zeros_like(omega_full)
        nonzero = self.wave_squared > 0.0
        kz = np.broadcast_to(self.kz_grid, self.wave_squared.shape)
        ky = np.broadcast_to(self.ky_grid, self.wave_squared.shape)
        u2[nonzero] = 1j * kz[nonzero] * omega_full[nonzero] / self.wave_squared[nonzero]
        u3[nonzero] = -1j * ky[nonzero] * omega_full[nonzero] / self.wave_squared[nonzero]
        return u2, u3

    def advect(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        left_full = self.embed(left)
        right_full = self.embed(right)
        u2, u3 = self.velocity_full(left_full)
        product = (
            self.physical(u2) * self.physical(1j * self.ky_grid * right_full)
            + self.physical(u3) * self.physical(1j * self.kz_grid * right_full)
        )
        return self.extract(np.fft.fftn(product) / self.normalization)

    def linear(self, omega: np.ndarray, absolute_lambda: float, d: float) -> np.ndarray:
        full = self.embed(omega)
        u2, _ = self.velocity_full(full)
        y = 2.0 * math.pi * np.arange(self.ny) / self.ny
        w = -0.5 * math.exp(-d) * np.sin(2.0 * y) + 0.25 * math.exp(-4.0 * d) * np.sin(4.0 * y)
        wxx = 0.5 * math.exp(-d) * np.sin(2.0 * y) - math.exp(-4.0 * d) * np.sin(4.0 * y)
        base_advection = (
            (2.0 * absolute_lambda * w)[:, None]
            * self.physical(1j * self.kz_grid * full)
            + self.physical(u2) * (8.0 * absolute_lambda * wxx)[:, None]
        )
        diffusion = -self.wave_squared * full
        return self.extract(diffusion - np.fft.fftn(base_advection) / self.normalization)

    def launch(self, kinetic: np.ndarray) -> np.ndarray:
        profile = kinetic / (2.0 * np.sqrt(self.n.astype(float) ** 2 + MU))
        result = np.zeros((len(self.kz), len(self.n)), dtype=np.complex128)
        wave_squared = 4.0 * self.n.astype(float) ** 2 + 1.0
        plus = KZ_MAX + 1
        minus = KZ_MAX - 1
        result[plus] = -1j * wave_squared * profile / math.sqrt(2.0)
        for index, n_mode in enumerate(self.n):
            reflected = -int(n_mode) + self.n_cut
            result[minus, reflected] = np.conjugate(result[plus, index])
        return result

    def velocity_coefficients(self, omega: np.ndarray) -> np.ndarray:
        full = self.embed(omega)
        u2, u3 = self.velocity_full(full)
        result = np.zeros((len(self.kz), len(self.n), 2), dtype=np.complex128)
        for kz_index, kz in enumerate(self.kz):
            for index, n_mode in enumerate(self.n):
                y_index = (2 * int(n_mode)) % self.ny
                z_index = int(kz) % self.nz
                result[kz_index, index, 0] = u2[y_index, z_index]
                result[kz_index, index, 1] = u3[y_index, z_index]
        return result


def integrate(n_cut: int, epsilon_nu: float, d_end: float, fast_step: float) -> np.ndarray:
    space = VorticityFFT(n_cut)
    first = space.launch(canonical_top(matrix_from_os_formula(n_cut, epsilon_nu)))
    zero = np.zeros_like(first)
    state = np.stack((first, zero, zero, zero, zero))
    mask0 = np.zeros_like(first)
    mask0[KZ_MAX] = 1.0
    mask2 = np.zeros_like(first)
    mask2[KZ_MAX - 2] = 1.0
    mask2[KZ_MAX + 2] = 1.0

    def rhs(theta: float, values: np.ndarray) -> np.ndarray:
        one, two0, two2, three0, three2 = values
        d = epsilon_nu * theta
        factor = epsilon_nu / 4.0
        absolute_lambda = 1.0 / epsilon_nu
        quadratic = space.advect(one, one)
        return factor * np.stack((
            space.linear(one, absolute_lambda, d),
            space.linear(two0, absolute_lambda, d) - mask0 * quadratic,
            space.linear(two2, absolute_lambda, d) - mask2 * quadratic,
            space.linear(three0, absolute_lambda, d)
            - space.advect(one, two0) - space.advect(two0, one),
            space.linear(three2, absolute_lambda, d)
            - space.advect(one, two2) - space.advect(two2, one),
        ))

    theta = 0.0
    theta_end = d_end / epsilon_nu
    while theta < theta_end - 1.0e-13:
        step = min(fast_step, theta_end - theta)
        k1 = rhs(theta, state)
        k2 = rhs(theta + step / 2.0, state + step * k1 / 2.0)
        k3 = rhs(theta + step / 2.0, state + step * k2 / 2.0)
        k4 = rhs(theta + step, state + step * k3)
        state += step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        theta += step
    return np.stack([space.velocity_coefficients(value) for value in state])


def norm(array: np.ndarray) -> float:
    return math.sqrt(max(0.0, float(np.vdot(array, array).real)))


def forbidden_relative(state: np.ndarray) -> float:
    combined = (state[0], state[1] + state[2], state[3] + state[4])
    allowed = ({-1, 1}, {0, -2, 2}, {-1, 1, -3, 3})
    maximum = 0.0
    for field, permitted in zip(combined, allowed):
        forbidden = np.concatenate([
            field[kz + KZ_MAX].ravel()
            for kz in range(-KZ_MAX, KZ_MAX + 1) if kz not in permitted
        ])
        maximum = max(maximum, norm(forbidden) / max(norm(field), 1.0e-300))
    return maximum


def source_cases(config: Mapping[str, object], summary: Mapping[str, object], smoke: bool) -> list[dict[str, object]]:
    if smoke:
        archive = summary["archiveIndex"]
        formal = [row for row in archive if row["gridKind"] == "formal"]
        selected = [formal[0], formal[-1], next(row for row in archive if row["gridKind"] == "holdout")]
        return [{
            "cutoff": int(row["N"]),
            "viscousEpsilon": float(row["viscousEpsilon"]),
            "fastStep": (
                float(summary["formalGrid"]["primaryFastStep"])
                if row["gridKind"] == "formal"
                else float(summary["holdout"]["configuration"]["fastStep"])
            ),
            "archivePrefix": row["archivePrefix"],
            "gridKind": row["gridKind"],
        } for row in selected]
    archive_lookup = {
        (int(row["N"]), float(row["viscousEpsilon"]), row["gridKind"]): row["archivePrefix"]
        for row in summary["archiveIndex"]
    }
    cases = []
    for sentinel in config["independentSentinels"]:
        n_cut = int(sentinel["cutoff"])
        epsilon_nu = float(sentinel["viscousEpsilon"])
        cases.append({
            **sentinel,
            "archivePrefix": archive_lookup[(n_cut, epsilon_nu, "formal")],
            "gridKind": "formal",
        })
    holdout = config["holdout"]
    cases.append({
        "cutoff": int(holdout["cutoff"]),
        "viscousEpsilon": float(holdout["viscousEpsilon"]),
        "fastStep": float(holdout["fastStep"]),
        "archivePrefix": archive_lookup[(int(holdout["cutoff"]), float(holdout["viscousEpsilon"]), "holdout")],
        "gridKind": "holdout",
    })
    return cases


def main() -> int:
    output = ARGS.output.resolve()
    primary_dir = ARGS.primary_dir.resolve()
    if ARGS.smoke:
        if is_within(output, HERE) or is_within(primary_dir, HERE):
            raise RuntimeError("smoke inputs and output must be outside the formal source tree")
    elif (
        output != (HERE / "independent_validation.json").resolve()
        or primary_dir != HERE.resolve()
        or ARGS.config.resolve() != (HERE / "config.json").resolve()
    ):
        raise RuntimeError("formal validation must use the canonical R0.73H package and config paths")
    if (output.exists() or PROGRESS.exists()) and not ARGS.overwrite:
        raise RuntimeError("refusing to overwrite independent outputs without --overwrite")
    if output.exists():
        output.unlink()
    if PROGRESS.exists():
        PROGRESS.unlink()
    output.parent.mkdir(parents=True, exist_ok=True)
    provenance = source_gate(ARGS.source_commit, ARGS.smoke)
    config = json.loads(ARGS.config.read_text(encoding="utf-8"))
    summary_path = primary_dir / "primary_summary.json"
    manifest_path = primary_dir / "primary_manifest.json"
    archive_path = primary_dir / "coefficient_snapshots.npz"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if summary["smokeMode"] is not ARGS.smoke or not summary["allChecksPass"]:
        raise RuntimeError("primary summary mode/pass state is incompatible")
    tolerance = float(config["tolerances"]["independentCoefficientRelative"])
    forbidden_tolerance = float(config["tolerances"]["independentForbiddenParityRelative"])
    d_end = float(summary["formalGrid"]["profileTimeSnapshots"][-1])
    cases = source_cases(config, summary, ARGS.smoke)
    emit("start", caseCount=len(cases), smokeMode=ARGS.smoke)
    validations = []
    with np.load(archive_path, allow_pickle=False) as archive:
        for index, case in enumerate(cases, start=1):
            n_cut = int(case["cutoff"])
            epsilon_nu = float(case["viscousEpsilon"])
            fast_step = float(case["fastStep"])
            prefix = str(case["archivePrefix"])
            emit("sentinel_start", index=index, N=n_cut, viscousEpsilon=epsilon_nu, fastStep=fast_step)
            independent = integrate(n_cut, epsilon_nu, d_end, fast_step)
            primary = archive[f"{prefix}_states"][-1]
            per_path = {}
            for path_index, name in enumerate((
                "V1", "V2_Kz0", "V2_KzPlusMinus2", "V3_via_Kz0", "V3_via_KzPlusMinus2"
            )):
                per_path[name] = norm(independent[path_index] - primary[path_index]) / max(
                    norm(independent[path_index]), norm(primary[path_index]), 1.0e-300
                )
            maximum = max(per_path.values())
            forbidden = forbidden_relative(independent)
            passed = maximum <= tolerance and forbidden <= forbidden_tolerance
            validations.append({
                "N": n_cut,
                "viscousEpsilon": epsilon_nu,
                "absoluteLambda": 1.0 / epsilon_nu,
                "fastStep": fast_step,
                "gridKind": case["gridKind"],
                "archivePrefix": prefix,
                "physicalGrid": {
                    "yCount": 8 * n_cut + 8,
                    "zCount": 16,
                    "aliasFreeForHierarchyThroughOrderThree": True,
                },
                "pathRelativeErrors": per_path,
                "maximumCoefficientRelativeError": maximum,
                "forbiddenParityRelative": forbidden,
                "pass": passed,
            })
            emit("sentinel_complete", index=index, maximumCoefficientRelativeError=maximum, forbiddenParityRelative=forbidden, passCheck=passed)
    result = {
        "schemaVersion": "r073h-independent-vorticity-fft-v1",
        "release": "R0.73H",
        "evidenceClass": "independent-finite-binary64-galerkin-diagnostic-only",
        "diagnosticOnly": True,
        "smokeMode": ARGS.smoke,
        "sourceProvenance": provenance,
        "methods": {
            "matrix": "direct Orr--Sommerfeld Fourier coefficients",
            "state": "scalar vorticity with independently written Biot--Savart recovery",
            "nonlinearity": "alias-free physical grid, FFT derivatives and products",
            "timeIntegrator": "fixed-step classical RK4 in fast time",
            "importsPrimaryProducer": False,
        },
        "primaryBindings": [
            binding(summary_path, primary_dir), binding(manifest_path, primary_dir), binding(archive_path, primary_dir)
        ],
        "tolerances": {
            "coefficientRelative": tolerance,
            "forbiddenParityRelative": forbidden_tolerance,
        },
        "validations": validations,
        "maximumCoefficientRelativeError": max(row["maximumCoefficientRelativeError"] for row in validations),
        "maximumForbiddenParityRelative": max(row["forbiddenParityRelative"] for row in validations),
        "allChecksPass": all(row["pass"] for row in validations),
        "scientificWallTimeSeconds": time.perf_counter() - START,
        "claimBoundary": config["claimBoundary"],
    }
    emit("complete", allChecksPass=result["allChecksPass"], maximumCoefficientRelativeError=result["maximumCoefficientRelativeError"])
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(canonical(result), encoding="utf-8")
    os.replace(temporary, output)
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
