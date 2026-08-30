#!/usr/bin/env python3
"""Render the content-addressed R0.73F four-panel finite diagnostic."""

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


def configure_dependencies(path: str | None) -> None:
    if path:
        sys.path.insert(0, path)


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


def close(a: float, b: float, tolerance: float = 1e-14) -> bool:
    return abs(a - b) <= tolerance * max(1.0, abs(a), abs(b))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=None, help="directory containing scientific wheels")
    args = parser.parse_args()
    configure_dependencies(args.deps)

    import matplotlib.pyplot as plt
    import numpy as np

    config_path = HERE / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    inputs = config["inputs"]
    summary = json.loads((ROOT / inputs["summary"]).read_text(encoding="utf-8"))
    independent = json.loads((ROOT / inputs["independent"]).read_text(encoding="utf-8"))
    moving = read_csv(inputs["movingRows"])
    convergence = read_csv(inputs["convergenceRows"])
    nonnormal = read_csv(inputs["nonnormalRows"])
    rotating = read_csv(inputs["rotatingRows"])

    assert summary["allPrimaryChecksPass"] is True
    assert independent["allChecksPass"] is True
    assert summary["diagnosticEndpointIsCertifiedD0"] is False
    assert close(float(summary["diagnosticPhysicalEndpoint"]), 0.01)

    endpoint = [
        row for row in moving
        if int(row["N"]) == config["primaryCutoff"]
        and close(float(row["physicalTime"]), config["diagnosticPhysicalEndpoint"])
    ]
    endpoint.sort(key=lambda row: float(row["absoluteLambda"]))
    expected_eps = summary["primaryGrid"]["epsilons"]
    assert sorted(float(row["epsilon"]) for row in endpoint) == sorted(expected_eps)

    lambdas = np.asarray([float(row["absoluteLambda"]) for row in endpoint])
    full_rates = np.asarray([float(row["normalizedFullRate"]) for row in endpoint])
    top_rates = np.asarray([float(row["normalizedTopRate"]) for row in endpoint])

    finest = [
        row for row in convergence
        if row["kind"] == "step-halving"
        and int(row["N"]) == config["primaryCutoff"]
        and close(float(row["fineFastStep"]), 0.125)
    ]
    cutoff = [
        row for row in convergence
        if row["kind"] == "cutoff-discrepancy-not-tail-bound"
        and int(row["N"]) == 96 and int(row["coarseFastStep"]) == 48
    ]
    finest.sort(key=lambda row: 1.0 / float(row["epsilon"]))
    cutoff.sort(key=lambda row: 1.0 / float(row["epsilon"]))
    independent_rows = sorted(
        [row for row in independent["validations"] if int(row["N"]) == 96],
        key=lambda row: 1.0 / float(row["epsilon"]),
    )

    floor = float(config["errorFloor"])
    step_x = np.asarray([1.0 / float(row["epsilon"]) for row in finest])
    step_y_raw = np.asarray([
        max(float(row["fullNormalizedRateDifference"]),
            float(row["topNormalizedRateDifference"])) for row in finest
    ])
    cutoff_x = np.asarray([1.0 / float(row["epsilon"]) for row in cutoff])
    cutoff_y_raw = np.asarray([
        max(float(row["fullNormalizedRateDifference"]),
            float(row["topNormalizedRateDifference"])) for row in cutoff
    ])
    independent_x = np.asarray([1.0 / float(row["epsilon"]) for row in independent_rows])
    independent_y_raw = np.asarray([
        max(float(row["errors"]["fullRate"]), float(row["errors"]["topRate"]))
        for row in independent_rows
    ])

    ce_sizes = np.asarray([int(row["size"]) for row in nonnormal])
    ce_norms = np.asarray([float(row["semigroupNorm"]) for row in nonnormal])
    ce_reference = np.asarray([float(row["lowerReference"]) for row in nonnormal])
    phase = np.asarray([float(row["normalizedPhysicalTime"]) for row in rotating])
    branches = [np.asarray([float(row[f"lambda{j}"]) for row in rotating]) for j in range(3)]
    rotating_max = np.asarray([float(row["pointwiseMaximum"]) for row in rotating])

    style = ROOT / "figures" / "journal.mplstyle"
    plt.style.use(style)
    width = config["widthMillimetres"] / 25.4
    height = config["heightMillimetres"] / 25.4
    fig, axes = plt.subplots(2, 2, figsize=(width, height), constrained_layout=True)
    blue, orange, dark, mid, light = "#2166ac", "#b35806", "#252525", "#737373", "#bdbdbd"

    ax = axes[0, 0]
    ax.plot(lambdas, full_rates, color=blue, marker="o", label="full propagator norm")
    ax.plot(lambdas, top_rates, color=orange, marker="s", markerfacecolor="white",
            linestyle="--", label="finite top-block conorm")
    ax.axhline(float(config["analyticReference"]), color=mid, linestyle=":",
               label=r"frozen analytic reference $0.17035$")
    ax.set_xscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel(r"$(\varepsilon/d_{diag})\,\log$ gain")
    ax.set_title("A  Fixed-window finite gains", loc="left", fontweight="bold")
    ax.text(0.98, 0.04, r"$N=96$, $d_{diag}=0.01$ (not certified $d_0$)",
            transform=ax.transAxes, ha="right", fontsize=6.5, color=dark)
    ax.legend(loc="upper right", handlelength=2.2)

    ax = axes[0, 1]
    ax.plot(step_x, np.maximum(step_y_raw, floor), color=orange, marker="s",
            markerfacecolor="white", linestyle="--", label="step 0.25 vs 0.125")
    ax.plot(cutoff_x, np.maximum(cutoff_y_raw, floor), color=blue, marker="o",
            label="cutoff 48 vs 96")
    ax.plot(independent_x, np.maximum(independent_y_raw, floor), color=dark,
            marker="x", linestyle=":", label="independent reconstruction")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$|\Lambda|=\varepsilon^{-1}$")
    ax.set_ylabel("max normalized-rate discrepancy")
    ax.set_title("B  Numerical cross-checks", loc="left", fontweight="bold")
    ax.text(0.02, 0.04, r"display floor $10^{-17}$; cutoff agreement $\ne$ tail bound",
            transform=ax.transAxes, fontsize=6.5, color=dark)
    ax.legend(loc="upper right", handlelength=2.2)

    ax = axes[1, 0]
    ax.plot(ce_sizes, ce_norms, color=blue, marker="o", label=r"exact $\|e^{D_n/n}\|_2$")
    ax.plot(ce_sizes, ce_reference, color=orange, marker="s", markerfacecolor="white",
            linestyle="--", label=r"rigorous lower bound $n/e$")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel(r"matrix parameter $n$")
    ax.set_ylabel("semigroup norm at $t=1/n$")
    ax.set_title("C  Exact nonnormal prefactor trap", loc="left", fontweight="bold")
    ax.legend(loc="upper left")
    ax.text(0.98, 0.05, r"$\sigma(D_n)=\{-n\}$, yet $\|e^{D_n/n}\|\geq n/e$",
            transform=ax.transAxes, ha="right", fontsize=6.5, color=dark)

    ax = axes[1, 1]
    styles = ["-", "--", ":"]
    for j, (branch, linestyle) in enumerate(zip(branches, styles)):
        ax.plot(phase, branch, color=mid if j else light, linestyle=linestyle,
                linewidth=0.9, label=rf"branch $\lambda_{j}$")
    ax.plot(phase, rotating_max, color=blue, linewidth=1.6,
            label=r"pointwise $\max_j\lambda_j$")
    ax.axhline(0.0, color=dark, linewidth=0.55)
    ax.set_xlabel("normalized physical time")
    ax.set_ylabel("instantaneous branch value")
    ax.set_title("D  Exact rotating-edge trap", loc="left", fontweight="bold")
    ax.text(0.02, 0.08,
            "pointwise minimum of maximum = 1/4\nall branch integrals = -1/4",
            transform=ax.transAxes, fontsize=6.5, color=dark, zorder=10,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9,
                  "pad": 1.0})
    ax.legend(loc="upper right", ncol=2, columnspacing=0.8, handlelength=1.8)

    for ax in axes.flat:
        ax.tick_params(pad=2)

    outputs = []
    for name, kwargs in (
        ("figure.pdf", {}),
        ("figure.svg", {}),
        ("figure.png", {"dpi": int(config["pngDpi"])}),
    ):
        path = HERE / name
        fig.savefig(path, **kwargs)
        outputs.append(binding(str(path.relative_to(ROOT))))
    plt.close(fig)

    claim_boundary = {
        "formalFiniteDiagnosticFigure": True,
        "diagnosticDIsCertifiedD0": False,
        "finiteTopEqualsContinuumTop": False,
        "ordinaryCutoffAgreementIsTailProof": False,
        "finiteGainProvesContinuumDichotomy": False,
        "sampledTimeIsContinuousTimeBound": False,
        "finiteRateEqualsAnalyticKappa": False,
        "counterexamplesDescribeExactFourierRow": False,
        "nonlinearNavierStokes": False,
        "clayProblemSolved": False,
    }
    result = {
        "schemaVersion": "r073f-figure-results-v1",
        "figureId": config["figureId"],
        "inputs": [binding(path) for path in inputs.values()],
        "configBinding": binding(str(config_path.relative_to(ROOT))),
        "outputs": outputs,
        "panelA": {
            "absoluteLambda": lambdas.tolist(),
            "normalizedFullRate": full_rates.tolist(),
            "normalizedTopRate": top_rates.tolist(),
            "analyticReference": config["analyticReference"],
        },
        "panelB": {
            "stepHalvingMaximumRateDifference": step_y_raw.tolist(),
            "cutoff48To96MaximumRateDifference": cutoff_y_raw.tolist(),
            "independentMaximumRateDifference": independent_y_raw.tolist(),
            "displayFloor": floor,
        },
        "panelC": {
            "maximumClosedFormResidual": summary["counterexamples"]["nonnormalPrefactor"]["maximumClosedFormResidual"],
            "largestObservedNorm": float(ce_norms.max()),
        },
        "panelD": {
            "sampledMinimumPointwiseMaximum": float(rotating_max.min()),
            "exactBranchIntegral": -0.25,
        },
        "claimBoundary": claim_boundary,
    }
    (HERE / "results.json").write_text(canonical(result), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
