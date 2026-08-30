#!/usr/bin/env python3
"""Render the content-addressed R0.73G four-panel finite diagnostic."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}


def read_csv(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    args = parser.parse_args()
    if args.deps:
        sys.path.insert(0, args.deps)

    import matplotlib

    matplotlib.use("Agg")
    matplotlib.rcParams["svg.hashsalt"] = "r073g-formal-row-leakage-v1"
    import matplotlib.pyplot as plt
    import numpy as np

    config_path = HERE / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    inputs = config["inputs"]
    rows = read_csv(inputs["rows"])
    convergence = read_csv(inputs["convergence"])
    summary = json.loads((ROOT / inputs["summary"]).read_text(encoding="utf-8"))
    independent = json.loads((ROOT / inputs["independent"]).read_text(encoding="utf-8"))
    if not summary["crossValidation"]["allKernelChecksPass"]:
        raise RuntimeError("primary kernel cross-check did not pass")
    if not independent["allChecksPass"]:
        raise RuntimeError("independent validation did not pass")
    if not summary["diagnosticOnly"]:
        raise RuntimeError("finite evidence boundary is missing")

    cutoffs = sorted({int(row["N"]) for row in rows})
    primary_cutoff = int(config["primaryCutoff"])
    if primary_cutoff != max(cutoffs):
        raise RuntimeError("primary cutoff is not the maximum archived cutoff")
    colors = ["#737373", "#67a9cf", "#2166ac", "#053061"]
    markers = ["v", "s", "o", "D"]
    style = ROOT / "figures" / "journal.mplstyle"
    if style.exists():
        plt.style.use(style)

    width = float(config["widthMillimetres"]) / 25.4
    height = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(2, 2, figsize=(width, height))
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.145, top=0.965,
                        wspace=0.31, hspace=0.43)

    ax = axes[0, 0]
    for color, marker, n_cut in zip(colors, markers, cutoffs):
        subset = sorted(
            (row for row in rows if int(row["N"]) == n_cut),
            key=lambda row: float(row["absoluteLambda"]),
        )
        ax.plot(
            [float(row["absoluteLambda"]) for row in subset],
            [float(row["topEigenvalueFastReal"]) for row in subset],
            color=color, marker=marker,
            markerfacecolor="white" if n_cut != primary_cutoff else color,
            label=rf"$N={n_cut}$",
        )
    ax.axhline(float(config["analyticReference"]), color="#b35806",
               linestyle=":", label="0.17035 reference")
    ax.set_xscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel(r"$\Re\lambda_{\rm top}$ (fast time)")
    ax.set_title("A  Frozen top eigenvalue", loc="left", fontweight="bold")
    ax.legend(ncol=2, handlelength=1.8)

    ax = axes[0, 1]
    for color, marker, n_cut in zip(colors, markers, cutoffs):
        subset = sorted(
            (row for row in rows if int(row["N"]) == n_cut),
            key=lambda row: float(row["absoluteLambda"]),
        )
        ax.plot(
            [float(row["absoluteLambda"]) for row in subset],
            [float(row["physicalH3ToL2Cost"]) for row in subset],
            color=color, marker=marker,
            markerfacecolor="white" if n_cut != primary_cutoff else color,
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel(r"physical $\|u_v\|_{H^3}/\|u_v\|_2$")
    ax.set_title("B  Physical Sobolev cost", loc="left", fontweight="bold")

    primary = sorted(
        (row for row in rows if int(row["N"]) == primary_cutoff),
        key=lambda row: float(row["absoluteLambda"]),
    )
    x_primary = [float(row["absoluteLambda"]) for row in primary]
    ax = axes[1, 0]
    ax.plot(
        x_primary,
        [float(row["kz2ProjectedLeakagePositiveUnitRowKernelA"]) for row in primary],
        color="#2166ac", marker="o", label=r"$K_z=2$: $B(u_+,u_+)$",
    )
    ax.plot(
        x_primary,
        [float(row["kz0ProjectedLeakageUnscaledRealPairKernelA"]) for row in primary],
        color="#b35806", marker="s", markerfacecolor="white", linestyle="--",
        label=r"$K_z=0$: $B(u_++\bar u_+,u_++\bar u_+)$",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel(r"projected quadratic leakage $L^2$")
    ax.set_title(f"C  Generated rows at cutoff $N={primary_cutoff}$",
                 loc="left", fontweight="bold")
    ax.legend(handlelength=2.2)

    ax = axes[1, 1]
    floor = float(config["displayFloor"])
    kernel_defect = [
        max(float(row["kz2KernelScaleOneDifference"]),
            float(row["kz0KernelScaleOneDifference"]),
            float(row["maximumKernelCoefficientScaleOneDifference"]))
        for row in primary
    ]
    finest = sorted(
        (row for row in convergence if int(row["fineN"]) == primary_cutoff),
        key=lambda row: float(row["absoluteLambda"]),
    )
    ax.plot(x_primary, np.maximum(kernel_defect, floor), color="#252525",
            marker="x", linestyle=":", label=r"independent kernels (floor $10^{-18}$)")
    ax.plot(
        [float(row["absoluteLambda"]) for row in finest],
        [max(float(row["maximumRelativeChange"]), floor) for row in finest],
        color="#2166ac", marker="o", label="cutoff 96 vs 128",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel("scale-one defect or relative change")
    ax.set_title("D  Numerical cross-checks", loc="left", fontweight="bold")
    ax.legend(handlelength=2.1)

    for axis in axes.flat:
        axis.tick_params(pad=2)
    fig.text(
        0.105, 0.025,
        "Finite binary64 Fourier compressions; diagnostic only.  "
        "Normalized positive physical row has unit L2 norm.",
        ha="left", va="bottom", fontsize=6.2, color="#252525",
    )

    metadata_title = "R0.73G finite nonlinear row-leakage diagnostic"
    creator = "figures/r073g/fig-r073g-nonlinear-row-leakage/plot.py"
    outputs = []
    for name, file_format, metadata, dpi in (
        ("figure.pdf", "pdf", {"Creator": creator, "Title": metadata_title,
          "Subject": "finite-binary64-diagnostic-only", "CreationDate": None,
          "ModDate": None}, None),
        ("figure.svg", "svg", {"Creator": creator, "Title": metadata_title,
          "Description": "finite-binary64-diagnostic-only", "Date": None}, None),
        ("figure.png", "png", {"Software": creator, "Title": metadata_title,
          "Description": "finite-binary64-diagnostic-only"}, int(config["pngDpi"])),
    ):
        path = HERE / name
        temporary = path.with_name("." + path.name + ".tmp")
        kwargs: dict[str, object] = {"format": file_format, "metadata": metadata}
        if dpi is not None:
            kwargs["dpi"] = dpi
        fig.savefig(temporary, **kwargs)
        temporary.replace(path)
        outputs.append(binding(str(path.relative_to(ROOT))))
    plt.close(fig)

    result = {
        "schemaVersion": "r073g-formal-figure-results-v1",
        "figureId": config["figureId"],
        "evidenceClass": "finite-binary64-diagnostic-only",
        "inputs": [binding(path) for path in inputs.values()],
        "configBinding": binding(str(config_path.relative_to(ROOT))),
        "outputs": outputs,
        "primaryCutoff": primary_cutoff,
        "observed": summary["primaryCutoffObservedRanges"],
        "crossValidation": {
            "primaryMaximumScaleOneDifference": summary["crossValidation"]["maximumScaleOneDifference"],
            "independentMaximumScaleOneError": independent["maximumScaleOneError"],
            "allChecksPass": True,
        },
        "claimBoundary": summary["claimBoundary"],
    }
    (HERE / "results.json").write_text(canonical(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
