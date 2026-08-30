#!/usr/bin/env python3
"""Render the content-addressed R0.73H harmonic-feedback journal figure."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE_RELATIVE = "figures/r073h/fig-r073h-harmonic-feedback"
THREAD_ENVIRONMENT = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
)
SOURCE_FILES = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_record(processes: int, threads_per_process: int) -> dict[str, Any]:
    product = subprocess.check_output(
        ["sw_vers", "-productName"], text=True,
    ).strip()
    version = subprocess.check_output(
        ["sw_vers", "-productVersion"], text=True,
    ).strip()
    build = subprocess.check_output(
        ["sw_vers", "-buildVersion"], text=True,
    ).strip()
    cpu = subprocess.check_output(
        ["sysctl", "-n", "machdep.cpu.brand_string"], text=True,
    ).strip()
    memory_bytes = int(subprocess.check_output(
        ["sysctl", "-n", "hw.memsize"], text=True,
    ).strip())
    return {
        "host": platform.node(),
        "operatingSystem": f"{product} {version} ({build}) {platform.machine()}",
        "kernel": f"Darwin {platform.release()}",
        "cpu": cpu,
        "memoryGiB": memory_bytes / (1024 ** 3),
        "processes": processes,
        "threadsPerProcess": threads_per_process,
        "gpu": "not used",
    }


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        ) + "\n",
        encoding="utf-8",
    )


def binding(relative: str, source_commit: str | None = None) -> dict[str, Any]:
    path = ROOT / relative
    row: dict[str, Any] = {
        "bytes": path.stat().st_size,
        "path": relative,
        "sha256": sha256(path),
    }
    if source_commit is not None:
        row["sourceCommit"] = source_commit
    return row


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strict_json(path: Path) -> dict[str, Any]:
    def reject_constant(value: str) -> object:
        raise ValueError("non-finite JSON constant: " + value)

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_constant,
        object_pairs_hook=unique_object,
    )
    require(isinstance(value, dict), str(path) + " must contain a JSON object")
    return value


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT)


def require_commit(commit: str, label: str) -> None:
    result = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, label + " is not a Git commit")


def require_ancestor(older: str, newer: str, message: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, message)


def verify_source_commit(renderer_source_commit: str) -> None:
    require_commit(renderer_source_commit, "renderer source commit")
    for name in SOURCE_FILES:
        relative = f"{PACKAGE_RELATIVE}/{name}"
        payload = git_bytes(renderer_source_commit, relative)
        require(
            payload == (ROOT / relative).read_bytes(),
            "working source differs from renderer source commit: " + relative,
        )


def verify_certificate_inputs(config: dict[str, Any], certificate_commit: str) -> None:
    require_commit(certificate_commit, "certificate commit")
    require(config["certificateCommit"] == certificate_commit,
            "certificate commit does not match config")
    for relative in config["inputs"].values():
        payload = git_bytes(certificate_commit, relative)
        require(payload == (ROOT / relative).read_bytes(),
                "working certificate input differs from immutable commit: " + relative)


def read_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    require(bool(rows), relative + " is empty")
    return rows


def number(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    require(value == value and abs(value) != float("inf"), "non-finite CSV value: " + key)
    return value


def at_endpoint(
    rows: list[dict[str, str]], cutoff: int, endpoint: float, grid_kind: str
) -> list[dict[str, str]]:
    selected = [
        row for row in rows
        if int(row["N"]) == cutoff
        and row["gridKind"] == grid_kind
        and abs(number(row, "profileTime") - endpoint) < 1e-14
    ]
    return sorted(selected, key=lambda row: number(row, "viscousEpsilon"))


def add_blossom(fig: Any, plt: Any, colors: dict[str, str]) -> None:
    from matplotlib.patches import Circle
    import numpy as np

    cx, cy = 0.974, 0.958
    for index, color in enumerate((colors["blue"], colors["gold"]) * 3):
        angle = 2.0 * np.pi * index / 6.0
        fig.add_artist(Circle(
            (cx + 0.010 * np.cos(angle), cy + 0.010 * np.sin(angle)),
            0.0052,
            transform=fig.transFigure,
            facecolor=color,
            edgecolor=colors["paper"],
            linewidth=0.35,
            alpha=0.82,
            zorder=20,
        ))
    fig.add_artist(Circle(
        (cx, cy), 0.0042, transform=fig.transFigure,
        facecolor=colors["ink"], edgecolor=colors["paper"],
        linewidth=0.35, zorder=21,
    ))


def main() -> int:
    started = time.monotonic()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--renderer-source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    args = parser.parse_args()
    for name in THREAD_ENVIRONMENT:
        require(os.environ.get(name) == "1", name + " must be pinned to 1")
    if args.deps:
        sys.path.insert(0, args.deps)

    import matplotlib
    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "r073h-harmonic-feedback-v1"
    import matplotlib.pyplot as plt
    import numpy as np

    config = strict_json(HERE / "config.json")
    contract = strict_json(HERE / "contract.json")
    verify_source_commit(args.renderer_source_commit)
    verify_certificate_inputs(config, args.certificate_commit)
    require_ancestor(args.certificate_commit, args.renderer_source_commit,
                     "renderer source commit must descend from certificate commit")

    inputs = config["inputs"]
    certificate = strict_json(ROOT / inputs["certificate"])
    certificate_validation = strict_json(ROOT / inputs["certificateValidation"])
    exact = strict_json(ROOT / inputs["exactQ2"])
    summary = strict_json(ROOT / inputs["primarySummary"])
    independent = strict_json(ROOT / inputs["independent"])
    rows = read_csv(inputs["primaryRows"])
    cutoff_rows = read_csv(inputs["cutoffConvergence"])
    step_rows = read_csv(inputs["stepConvergence"])

    require(certificate.get("allChecksPass") is True, "certificate did not pass")
    require(certificate_validation.get("allChecksPass") is True,
            "certificate validation did not pass")
    require(exact.get("allChecksPass") is True, "exact q=2 subcertificate did not pass")
    require(summary.get("allChecksPass") is True and summary.get("diagnosticOnly") is True,
            "primary finite diagnostic did not pass or lost its boundary")
    require(independent.get("allChecksPass") is True and independent.get("diagnosticOnly") is True,
            "independent finite diagnostic did not pass or lost its boundary")
    require(certificate["claimLedger"]["finiteDuhamelResponseAtFrozenGrid"]
            == "FINITE_DIAGNOSTIC_ONLY", "finite claim ledger changed")
    require(certificate["claimLedger"]["fullContinuumHarmonicResolvedSemigroupEstimate"]
            == "OPEN", "open continuum estimate was silently closed")
    require(certificate["claimLedger"]["ClayProblem"] == "OPEN",
            "Clay boundary was silently changed")

    endpoint = float(config["profileEndpoint"])
    cutoff = int(config["primaryCutoff"])
    formal = at_endpoint(rows, cutoff, endpoint, "formal")
    holdout_rows = at_endpoint(rows, cutoff, endpoint, "holdout")
    require(len(formal) == 7, "expected seven formal endpoint rows at N=64")
    require(len(holdout_rows) == 1, "expected one holdout endpoint row")
    holdout = holdout_rows[0]
    eps = np.array([number(row, "viscousEpsilon") for row in formal])
    q2 = np.array([number(row, "quadraticNaturalResponse") for row in formal])
    c3 = np.array([number(row, "targetCubicNaturalResponse") for row in formal])
    q2c = np.array([number(row, "quadraticCompensated") for row in formal])
    c3c = np.array([number(row, "targetCubicCompensated") for row in formal])
    signed = np.array([number(row, "totalSignedCompensated") for row in formal])
    fit_eps = np.array(summary["scaling"]["fitWindowViscousEpsilons"], dtype=float)
    index = {float(value): position for position, value in enumerate(eps)}
    fit_index = [index[float(value)] for value in fit_eps]
    q2_slope = float(np.polyfit(np.log(eps[fit_index]), np.log(q2[fit_index]), 1)[0])
    c3_slope = float(np.polyfit(np.log(eps[fit_index]), np.log(c3[fit_index]), 1)[0])
    require(abs(q2_slope - float(summary["scaling"]["quadraticNaturalLogSlope"])) < 2e-13,
            "quadratic slope does not recompute")
    require(abs(c3_slope - float(summary["scaling"]["targetCubicNaturalLogSlope"])) < 2e-13,
            "target-cubic slope does not recompute")

    exact_values = [
        float(Fraction(exact["tailCrossSchur"]["lowBlockLower"])),
        float(Fraction(exact["tailCrossSchur"]["tailLower"])),
        float(Fraction(exact["tailCrossSchur"]["targetLower"])),
        float(Fraction(exact["profilePerturbation"]["hdLower"])),
    ]
    require(exact["tailCrossSchur"]["crossNormUpper"] == "27/16",
            "exact cross bound changed")
    require(exact["profilePerturbation"]["operatorDifferenceUpper"] == "1/40",
            "exact time-perturbation bound changed")

    tolerances = strict_json(ROOT / "research/certificates/r073h/config.json")["tolerances"]
    finest = sorted(
        (row for row in cutoff_rows if int(row["fineN"]) == cutoff),
        key=lambda row: number(row, "viscousEpsilon"),
    )
    step_finest = sorted(
        (row for row in step_rows if abs(number(row, "fineFastStep") - 0.025) < 1e-14),
        key=lambda row: number(row, "viscousEpsilon"),
    )
    independent_formal = sorted(
        (row for row in independent["validations"] if row["gridKind"] == "formal"),
        key=lambda row: float(row["viscousEpsilon"]),
    )
    independent_holdout = [
        row for row in independent["validations"] if row["gridKind"] == "holdout"
    ]
    require(len(finest) == 7 and len(step_finest) == 3 and len(independent_formal) == 4,
            "numerical-check inventory changed")
    require(len(independent_holdout) == 1 and len(independent["validations"]) == 5,
            "independent inventory must be four formal sentinels plus one holdout")
    outer = np.array([
        max(number(row, "v1OuterThreeMassFraction"),
            number(row, "v2OuterThreeMassFraction"),
            number(row, "v3OuterThreeMassFraction"))
        for row in formal
    ])

    style = ROOT / "figures/journal.mplstyle"
    if style.exists():
        plt.style.use(style)
    matplotlib.rcParams.update({
        "figure.constrained_layout.use": False,
        "figure.facecolor": config["palette"]["paper"],
        "axes.facecolor": config["palette"]["paper"],
        "text.color": config["palette"]["ink"],
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })
    colors = config["palette"]
    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(2, 2, figsize=(width, height))
    fig.subplots_adjust(left=0.092, right=0.982, bottom=0.135, top=0.845,
                        wspace=0.31, hspace=0.44)

    ax = axes[0, 0]
    positions = np.arange(4)
    bars = ax.bar(
        positions,
        exact_values,
        color=[colors["blueLight"], colors["blueLight"],
               colors["blue"], colors["blue"]],
        edgecolor=[colors["blue"], colors["blue"], colors["ink"], colors["ink"]],
        hatch=["//", "..", "", "xx"],
        width=0.68,
    )
    ax.set_yscale("log")
    ax.set_ylim(0.015, 100.0)
    ax.set_xticks(positions, [r"low block", r"tail", r"Schur $H_0$", r"time $H_d$"])
    ax.set_ylabel("certified lower bound")
    for bar, label in zip(bars, ("1/5", "95/4", "1/20", "1/40"), strict=True):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.18,
                label, ha="center", va="bottom", fontsize=6.4)
    ax.text(0.02, 0.98, r"exact: $\|PH_0Q\|\leq27/16$; $0\leq d\leq1/450$",
            transform=ax.transAxes, fontsize=5.9, color=colors["muted"], va="top")
    ax.set_title("A  Exact doubled-row energy subcertificate", loc="left", fontweight="bold")

    ax = axes[0, 1]
    ax.loglog(eps, q2, color=colors["blue"], marker="o",
              label=rf"quadratic; slope {q2_slope:.3f}")
    ax.loglog(eps, c3, color=colors["gold"], marker="s", markerfacecolor="white",
              linestyle="--", label=rf"target cubic; slope {c3_slope:.3f}")
    ax.scatter([number(holdout, "viscousEpsilon")],
               [number(holdout, "quadraticNaturalResponse")],
               marker="*", s=42, facecolor="white", edgecolor=colors["blue"], zorder=5)
    ax.scatter([number(holdout, "viscousEpsilon")],
               [number(holdout, "targetCubicNaturalResponse")],
               marker="*", s=42, facecolor="white", edgecolor=colors["gold"], zorder=5,
               label="preregistered holdout")
    ax.set_xlabel(r"viscous parameter $\varepsilon_\nu=|\Lambda|^{-1}$")
    ax.set_ylabel(r"endpoint natural response at $d=0.01$")
    ax.set_title(r"B  Finite response scaling ($N=64$)", loc="left", fontweight="bold")
    ax.legend(handlelength=2.1, loc="upper left")

    ax = axes[1, 0]
    ax.semilogx(eps, q2c, color=colors["blue"], marker="o",
                label=r"quadratic $R_2/\varepsilon_\nu$")
    ax.semilogx(eps, c3c, color=colors["gold"], marker="s", markerfacecolor="white",
                linestyle="--", label=r"target cubic $R_3/\varepsilon_\nu^2$")
    ax.semilogx(eps, signed, color=colors["ink"], marker="D", markerfacecolor="white",
                linestyle=":", label="signed cubic projection")
    hold_eps = number(holdout, "viscousEpsilon")
    for value, color in (
        (number(holdout, "quadraticCompensated"), colors["blue"]),
        (number(holdout, "targetCubicCompensated"), colors["gold"]),
        (number(holdout, "totalSignedCompensated"), colors["ink"]),
    ):
        ax.scatter([hold_eps], [value], marker="*", s=42, facecolor="white",
                   edgecolor=color, zorder=5)
    ax.axhline(0.0, color=colors["muted"], linewidth=0.65)
    ax.set_ylim(-0.80, 1.06)
    ax.set_xlabel(r"viscous parameter $\varepsilon_\nu$")
    ax.set_ylabel("compensated endpoint coefficient")
    ax.text(
        0.15, 0.06,
        "holdout signed: mean {:+.3f} + doubled {:+.3f} = {:+.3f}".format(
            number(holdout, "meanPathSignedCompensated"),
            number(holdout, "doublePathSignedCompensated"),
            number(holdout, "totalSignedCompensated"),
        ),
        transform=ax.transAxes, fontsize=5.8, color=colors["muted"],
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.86, "pad": 1.5},
    )
    ax.set_title("C  Finite compensated coefficients", loc="left", fontweight="bold")
    ax.legend(handlelength=2.0, loc="center left")

    ax = axes[1, 1]
    display_floor = float(config["displayFloorNormalizedGateRatio"])
    ax.loglog(
        [number(row, "viscousEpsilon") for row in finest],
        [max(number(row, "maximumRelativeChange")
             / float(tolerances["finestCutoffRelative"]), display_floor)
         for row in finest],
        color=colors["blue"], marker="o", label=r"cutoff $48\to64$",
    )
    ax.loglog(
        [number(row, "viscousEpsilon") for row in step_finest],
        [max(number(row, "maximumRelativeChange")
             / float(tolerances["stepRelative"]), display_floor)
         for row in step_finest],
        color=colors["gold"], marker="s", markerfacecolor="white", linestyle="--",
        label=r"step $0.05\to0.025$",
    )
    ax.loglog(
        [float(row["viscousEpsilon"]) for row in independent_formal],
        [max(float(row["maximumCoefficientRelativeError"])
         / float(tolerances["independentCoefficientRelative"]), display_floor)
         for row in independent_formal],
        color=colors["ink"], marker="D", markerfacecolor="white", linestyle=":",
        label="independent FFT",
    )
    ax.scatter(
        [float(independent_holdout[0]["viscousEpsilon"])],
        [max(float(independent_holdout[0]["maximumCoefficientRelativeError"])
         / float(tolerances["independentCoefficientRelative"]), display_floor)],
        marker="*", s=42, facecolor="white", edgecolor=colors["ink"], zorder=6,
        label="independent holdout",
    )
    ax.loglog(
        eps, np.maximum(outer / float(tolerances["outerThreeMassFraction"]), display_floor),
        color=colors["muted"], marker="x", linestyle="-.",
        label=rf"outer mass; floor $10^{{-13}}$",
    )
    ax.axhline(1.0, color=colors["gold"], linestyle=(0, (1, 2)), linewidth=0.9,
               label="acceptance gate")
    ax.set_ylim(display_floor / 2.0, 2.5)
    ax.set_xlabel(r"viscous parameter $\varepsilon_\nu$")
    ax.set_ylabel("diagnostic / preregistered tolerance")
    ax.set_title("D  Finite numerical checks", loc="left", fontweight="bold")
    ax.legend(ncol=2, handlelength=1.8, loc="lower left", fontsize=6.2,
              columnspacing=0.9)

    for axis in axes.flat:
        axis.tick_params(pad=2)
    fig.text(0.092, 0.958, "R0.73H HARMONIC FEEDBACK", ha="left", va="top",
             fontsize=11.0, fontweight="bold", color=colors["ink"])
    fig.text(
        0.092, 0.910,
        "Exact q=2 continuum subcertificate beside finite binary64 response and QA diagnostics",
        ha="left", va="top", fontsize=7.0, color=colors["muted"],
    )
    fig.text(
        0.092, 0.025,
        r"A: exact subcertificate. B--D: finite $d=0.01>1/450$ diagnostics; not theorem $d=D$; no continuum saturation or tail bound.",
        ha="left", va="bottom", fontsize=6.0, color=colors["muted"],
    )
    add_blossom(fig, plt, colors)

    metadata_title = "R0.73H exact q=2 subcertificate and finite harmonic-feedback diagnostics"
    creator = PACKAGE_RELATIVE + "/plot.py"
    for name, file_format, metadata, dpi in (
        ("figure.pdf", "pdf", {
            "Creator": creator,
            "Title": metadata_title,
            "Subject": "exact-continuum-subcertificate-plus-finite-diagnostic",
            "CreationDate": None,
            "ModDate": None,
        }, None),
        ("figure.svg", "svg", {
            "Creator": creator,
            "Title": metadata_title,
            "Description": contract["supportedTakeaway"],
            "Date": None,
        }, None),
        ("figure.png", "png", {
            "Software": creator,
            "Title": metadata_title,
            "Description": "exact-continuum-subcertificate-plus-finite-diagnostic",
        }, int(config["pngDpi"])),
    ):
        path = HERE / name
        temporary = path.with_name("." + path.name + ".tmp")
        kwargs: dict[str, object] = {"format": file_format, "metadata": metadata}
        if dpi is not None:
            kwargs["dpi"] = dpi
        fig.savefig(temporary, **kwargs)
        temporary.replace(path)
        if file_format == "svg":
            normalize_svg(path)
    plt.close(fig)

    output_paths = [f"{PACKAGE_RELATIVE}/{name}" for name in
                    ("figure.pdf", "figure.svg", "figure.png")]
    result = {
        "schemaVersion": "r073h-formal-figure-results-v1",
        "release": "R0.73H",
        "figureId": config["figureId"],
        "createdAt": config["createdAt"],
        "rendererSourceCommit": args.renderer_source_commit,
        "certificateCommit": args.certificate_commit,
        "evidenceClass": "exact-continuum-subcertificate-plus-finite-binary64-diagnostic",
        "inputBindings": [binding(relative, args.certificate_commit)
                          for relative in inputs.values()],
        "sourceBindings": [binding(f"{PACKAGE_RELATIVE}/{name}", args.renderer_source_commit)
                           for name in SOURCE_FILES],
        "outputs": [binding(relative) for relative in output_paths],
        "observations": {
            "exact": {
                "lowBlockLower": exact["tailCrossSchur"]["lowBlockLower"],
                "tailLower": exact["tailCrossSchur"]["tailLower"],
                "crossNormUpper": exact["tailCrossSchur"]["crossNormUpper"],
                "h0Lower": exact["tailCrossSchur"]["targetLower"],
                "hdLower": exact["profilePerturbation"]["hdLower"],
                "maximumProfileTime": exact["profilePerturbation"]["maximumProfileTime"],
            },
            "finite": {
                "formalEndpointRowCount": len(formal),
                "profileEndpoint": endpoint,
                "theoremWindowUpper": 1.0 / 450.0,
                "profileEndpointStrictlyOutsideTheoremWindow": endpoint > 1.0 / 450.0,
                "independentFormalSentinelCount": len(independent_formal),
                "independentHoldoutCount": len(independent_holdout),
                "quadraticNaturalLogSlope": q2_slope,
                "targetCubicNaturalLogSlope": c3_slope,
                "holdoutQuadraticCompensated": number(holdout, "quadraticCompensated"),
                "holdoutTargetCubicCompensated": number(holdout, "targetCubicCompensated"),
                "holdoutMeanPathSignedCompensated": number(holdout, "meanPathSignedCompensated"),
                "holdoutDoublePathSignedCompensated": number(holdout, "doublePathSignedCompensated"),
                "holdoutTotalSignedCompensated": number(holdout, "totalSignedCompensated"),
                "maximumNormalizedGateRatio": max(
                    max(number(row, "maximumRelativeChange")
                        / float(tolerances["finestCutoffRelative"]) for row in finest),
                    max(number(row, "maximumRelativeChange")
                        / float(tolerances["stepRelative"]) for row in step_finest),
                    max(float(row["maximumCoefficientRelativeError"])
                        / float(tolerances["independentCoefficientRelative"])
                        for row in independent["validations"]),
                    float(np.max(outer / float(tolerances["outerThreeMassFraction"]))),
                ),
            },
        },
        "claimBoundary": contract["claimBoundary"],
        "compute": compute_record(1, 1),
        "runtime": {
            "processes": 1,
            "threadsPerProcess": 1,
            "wallTimeSeconds": time.monotonic() - started,
        },
    }
    (HERE / "results.json").write_text(canonical(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
