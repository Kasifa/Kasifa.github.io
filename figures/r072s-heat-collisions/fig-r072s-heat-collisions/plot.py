#!/usr/bin/env python3
"""Build the R0.72S singular-strata and heat-collision journal figure.

Every plotted curve is a presentation sample of an exact formula proved in
the analytic report.  The script performs no PDE solve, regression, root-count
inference, or numerical caustic classification.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import resource
import subprocess
import sys
import time
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from certificate_ledger import verify_flat_certificate_ledger


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_SOURCES = (
    "README.md", "caption.md", "figure-contract.md", "contract.json",
    "config.json", "command.txt", "requirements.txt", "certificate_ledger.py",
    "plot.py", "qa_images.py", "publish_assets.py", "validate.py",
    "build_manifest.py",
)
FIELDS = (
    "panel", "route", "series", "kind", "x", "y", "phi", "theta",
    "radius", "distance", "source", "pointer", "status", "note",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()


def require_tracked_tree_clean() -> None:
    for command in (
        ("git", "diff", "--quiet", "--"),
        ("git", "diff", "--cached", "--quiet", "--"),
    ):
        completed = subprocess.run(command, cwd=REPOSITORY, check=False)
        if completed.returncode == 1:
            raise RuntimeError("formal figure build rejects tracked or staged drift")
        if completed.returncode != 0:
            raise RuntimeError("unable to verify tracked-tree cleanliness")


def package_source_git_blobs(commit: str) -> dict[str, str]:
    if FULL_SHA.fullmatch(commit) is None:
        raise RuntimeError("formal figure build requires a full HEAD commit")
    records: dict[str, str] = {}
    for name in PACKAGE_SOURCES:
        path = (ROOT / name).resolve()
        relative = str(path.relative_to(REPOSITORY.resolve()))
        try:
            object_type = subprocess.check_output(
                ["git", "cat-file", "-t", f"{commit}:{relative}"],
                cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
            ).strip()
            committed = subprocess.check_output(
                ["git", "rev-parse", f"{commit}:{relative}"],
                cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
            ).strip()
            working = subprocess.check_output(
                ["git", "hash-object", f"--path={relative}", str(path)],
                cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"package source is not tracked at {commit}: {relative}") from exc
        if object_type != "blob" or committed != working:
            raise RuntimeError(f"package source does not match {commit}:{relative}")
        records[relative] = committed
    return records


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--analytic-source", required=True)
    parser.add_argument("--producer-config", required=True)
    parser.add_argument("--producer-result", required=True)
    parser.add_argument("--independent-config", required=True)
    parser.add_argument("--independent-result", required=True)
    parser.add_argument("--crosscheck", required=True)
    return parser.parse_args()


def load_json(path: Path, label: str) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"{label} does not exist: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} must be a JSON object")
    return value


def runtime_lineage(
    args: argparse.Namespace, config: dict[str, Any]
) -> tuple[dict[str, Any], str, dict[str, Any]]:
    bindings = config["formalGitBindings"]
    paths = {
        "analyticSource": Path(args.analytic_source).expanduser().resolve(),
        "producerConfig": Path(args.producer_config).expanduser().resolve(),
        "producerResult": Path(args.producer_result).expanduser().resolve(),
        "independentConfig": Path(args.independent_config).expanduser().resolve(),
        "independentResult": Path(args.independent_result).expanduser().resolve(),
        "crosscheck": Path(args.crosscheck).expanduser().resolve(),
        "certificateLedger": (REPOSITORY / bindings["certificateLedgerPath"]).resolve(),
    }
    canonical = {
        "analyticSource": (REPOSITORY / bindings["sourceCommitPaths"][0]).resolve(),
        **{
            role: (REPOSITORY / relative).resolve()
            for role, relative in bindings["certificateCommitRoles"].items()
        },
        "certificateLedger": (REPOSITORY / bindings["certificateLedgerPath"]).resolve(),
    }
    if paths != canonical:
        raise RuntimeError("formal figure inputs must be the canonical repository files")

    producer_config = load_json(paths["producerConfig"], "producer config")
    independent_config = load_json(paths["independentConfig"], "independent config")
    producer_result = load_json(paths["producerResult"], "producer result")
    independent_result = load_json(paths["independentResult"], "independent result")
    crosscheck = load_json(paths["crosscheck"], "crosscheck")
    checks = crosscheck.get("checks")
    source_commit = crosscheck.get("sourceCommit")
    if (
        crosscheck.get("status") != "passed"
        or not isinstance(checks, dict)
        or not checks
        or not all(value is True for value in checks.values())
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not isinstance(source_commit, str)
        or FULL_SHA.fullmatch(source_commit) is None
        or producer_config.get("gitCommit") != source_commit
        or independent_config.get("gitCommit") != source_commit
        or producer_config.get("sourceTracked") is not True
        or independent_config.get("sourceTracked") is not True
        or producer_config.get("trackedChangesDirty") is not False
        or independent_config.get("trackedChangesDirty") is not False
        or producer_result.get("status") != "passed"
        or independent_result.get("status") != "passed"
    ):
        raise RuntimeError("formal R0.72S certificate lineage is not sealed")

    ledger = verify_flat_certificate_ledger(
        paths["certificateLedger"].parent,
        required_files={
            Path(relative).name
            for relative in bindings["certificateCommitRoles"].values()
        },
    )
    statuses = {
        "analyticSource": "source",
        "producerConfig": "formal-ready-config",
        "producerResult": "passed",
        "independentConfig": "formal-ready-config",
        "independentResult": "passed",
        "crosscheck": "passed-formal-source-only",
        "certificateLedger": "passed-flat-ledger",
    }
    records = {
        name: {"path": str(path), "sha256": sha256(path), "status": statuses[name]}
        for name, path in paths.items()
    }
    return records, source_commit, ledger


def add_row(
    rows: list[dict[str, str]], *, panel: str, route: str, series: str,
    kind: str, x: float, y: float, source: str, pointer: str,
    status: str, note: str, phi: float | str = "", theta: float | str = "",
    radius: float | str = "", distance: float | str = "",
) -> None:
    if not math.isfinite(float(x)) or not math.isfinite(float(y)):
        raise ValueError("non-finite figure datum")
    rows.append({
        "panel": panel,
        "route": route,
        "series": series,
        "kind": kind,
        "x": f"{float(x):.17g}",
        "y": f"{float(y):.17g}",
        "phi": str(phi),
        "theta": str(theta),
        "radius": str(radius),
        "distance": str(distance),
        "source": source,
        "pointer": pointer,
        "status": status,
        "note": note,
    })


def surface(ax: mpl.axes.Axes, palette: dict[str, str]) -> None:
    ax.set_facecolor(palette["paper"])
    ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.75)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(palette["muted"])
        ax.spines[side].set_linewidth(0.65)
    ax.tick_params(labelsize=6.3, colors=palette["ink"], width=0.55)


def panel_title(
    ax: mpl.axes.Axes, letter: str, heading: str, subheading: str,
    palette: dict[str, str],
) -> None:
    ax.text(-0.04, 1.105, letter, transform=ax.transAxes, ha="right", va="top",
            fontsize=10.5, fontweight="bold", color=palette["ink"])
    ax.text(0.0, 1.105, heading, transform=ax.transAxes, ha="left", va="top",
            fontsize=8.6, fontweight="bold", color=palette["ink"])
    ax.text(0.0, 1.035, subheading, transform=ax.transAxes, ha="left", va="top",
            fontsize=6.0, color=palette["muted"])


def main() -> None:
    started = time.perf_counter()
    require_tracked_tree_clean()
    commit = git_commit()
    source_blobs = package_source_git_blobs(commit)
    args = parse_args()
    config = load_json(ROOT / "config.json", "figure config")
    contract = load_json(ROOT / "contract.json", "figure contract")
    lineage, source_commit, ledger = runtime_lineage(args, config)
    palette = config["palette"]

    for name in ("progress.ndjson", "resource-log.ndjson"):
        (ROOT / name).write_text("", encoding="utf-8")
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": utc_now(), "event": "start", "commit": commit}) + "\n")

    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": True,
    })
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(width, height), constrained_layout=False)
    fig.patch.set_facecolor(palette["paper"])
    fig.subplots_adjust(left=0.055, right=0.985, bottom=0.18, top=0.80, wspace=0.31)
    rows: list[dict[str, str]] = []

    # Panel A: exact projection of the A4/A5 incidence spine.
    ax = axes[0]
    surface(ax, palette)
    phi_values = np.linspace(-math.pi, math.pi, int(config["panels"]["A"]["phiSamples"]))
    a_values = np.cos(phi_values) / 15.0
    b_values = np.sin(phi_values) / 5.0
    ax.plot(a_values, b_values, color=palette["red"], lw=1.35,
            label=r"$A_4/A_5$ closure")
    for phi_value, a_value, b_value in zip(phi_values, a_values, b_values):
        add_row(
            rows, panel="A", route="incidence-preimage", series="A4 closure",
            kind="exact-parametric-curve", x=a_value, y=b_value,
            phi=phi_value, source="research/r072s_report-source.md",
            pointer="(1.6)-(1.8)", status="proved",
            note="A=cos(phi)/15, B=sin(phi)/5",
        )
    a5_points = ((1.0 / 15.0, 0.0, 0.0), (-1.0 / 15.0, 0.0, math.pi))
    ax.scatter([item[0] for item in a5_points], [0.0, 0.0], s=24,
               color=palette["ink"], marker="D", zorder=5, label=r"two $A_5$ points")
    for a_value, b_value, phi_value in a5_points:
        add_row(
            rows, panel="A", route="incidence-preimage", series="A5 point",
            kind="exact-point", x=a_value, y=b_value, phi=phi_value,
            source="research/r072s_report-source.md", pointer="(1.6),(1.8)",
            status="proved", note="B=0 and |15A|=1",
        )
    ax.text(0.0, 0.0, r"$A_4$ away from the two diamonds", ha="center", va="center",
            fontsize=5.8, color=palette["muted"])
    ax.text(-0.072, 0.182, r"$det J_{1:4}=5400$", fontsize=6.0,
            color=palette["blueDark"], ha="left")
    ax.set_xlim(-0.078, 0.078)
    ax.set_ylim(-0.225, 0.225)
    ax.set_xlabel(r"incidence parameter $A$", fontsize=7.0)
    ax.set_ylabel(r"incidence parameter $B$", fontsize=7.0)
    panel_title(ax, "A", "Higher-stratum spine",
                "projection of incidence preimages, not the global caustic image", palette)
    ax.legend(loc="lower center", fontsize=5.5, frameon=False, handlelength=2.2)

    # Panel B: the exact A2 colliding branches.
    ax = axes[1]
    surface(ax, palette)
    panel_b = config["panels"]["B"]
    delta_all_b = np.linspace(
        float(panel_b["deltaMinimum"]), float(panel_b["deltaMaximum"]),
        int(panel_b["samples"]),
    )
    delta_b = delta_all_b[delta_all_b <= 0.0]
    k_values = np.exp(-3.0 * delta_b)
    s_plus = (1.0 + np.sqrt(1.0 + 8.0 * k_values**2)) / (4.0 * k_values)
    xi_exact = np.arccos(np.clip(s_plus, -1.0, 1.0))
    xi_leading = np.sqrt(np.maximum(0.0, -2.0 * delta_b))
    for sign, label in ((1.0, "+"), (-1.0, "-")):
        ax.plot(delta_b, sign * xi_exact, color=palette["blueDark"], lw=1.35,
                label="exact colliding branches" if sign > 0 else None)
        ax.plot(delta_b, sign * xi_leading, color=palette["ochre"], lw=0.9,
                linestyle="--", label=r"leading $\pm\sqrt{-2\delta}$" if sign > 0 else None)
        for delta, xi in zip(delta_b, sign * xi_exact):
            add_row(
                rows, panel="B", route="A2-heat-path", series=f"A2 exact {label}",
                kind="exact-analytic-branch", x=delta, y=xi, phi=xi,
                source="research/r072s_report-source.md", pointer="(3.4),(3.12)",
                status="proved", note="phi=pi/2+xi; k=exp(-3delta)",
            )
        for delta, xi in zip(delta_b, sign * xi_leading):
            add_row(
                rows, panel="B", route="A2-heat-path", series=f"A2 leading {label}",
                kind="proved-leading-asymptotic", x=delta, y=xi, phi=xi,
                source="research/r072s_report-source.md", pointer="(3.11)-(3.12)",
                status="leading-order", note="xi^2=-2delta",
            )
    ax.axvline(0.0, color=palette["red"], lw=0.9, linestyle=":")
    ax.scatter([0.0], [0.0], s=24, color=palette["red"], marker="o", zorder=5)
    ax.text(-0.27, 0.86, "4 distinct", fontsize=6.0, color=palette["blueDark"])
    ax.text(0.012, 0.08, "$A_2$\n3 distinct", fontsize=5.8, color=palette["red"])
    ax.text(0.075, 0.86, "2 distinct", fontsize=6.0, color=palette["muted"])
    ax.text(-0.335, -0.98, "noncolliding simple pair omitted; included in counts",
            fontsize=4.65, color=palette["muted"], ha="left")
    ax.set_xlim(float(panel_b["deltaMinimum"]), float(panel_b["deltaMaximum"]))
    ax.set_ylim(-1.05, 1.05)
    ax.set_xlabel(r"$\delta=y-\log 2$", fontsize=7.0)
    ax.set_ylabel(r"$\xi=\phi-\pi/2$", fontsize=7.0)
    panel_title(ax, "B", "Generic $A_2$ fold",
                "one global event; distinct counts 4 / 3 / 2", palette)
    ax.legend(loc="lower left", fontsize=5.5, frameon=False, handlelength=2.2)

    # Panel C: the exact real-even A3 branches and the persistent symmetry axis.
    ax = axes[2]
    surface(ax, palette)
    panel_c = config["panels"]["C"]
    delta_all_c = np.linspace(
        float(panel_c["deltaMinimum"]), float(panel_c["deltaMaximum"]),
        int(panel_c["samples"]),
    )
    delta_c = delta_all_c[delta_all_c <= 0.0]
    tau_values = 0.5 * np.exp(-delta_c)
    a0 = -2563.0 / 1280.0
    b0 = 1.0 / 30.0
    qa = 12.0 * b0 * tau_values**8
    qb = 4.0 * a0 * tau_values**3
    qc = 1.0 - 3.0 * b0 * tau_values**8
    discriminant = qb**2 - 4.0 * qa * qc
    x_root = 2.0 * qc / (-qb + np.sqrt(discriminant))
    phi_exact = np.arccos(np.clip(x_root, -1.0, 1.0))
    phi_leading = np.sqrt(np.maximum(0.0, -6.0 * delta_c))
    for sign, label in ((1.0, "+"), (-1.0, "-")):
        ax.plot(delta_c, sign * phi_exact, color=palette["blueDark"], lw=1.35,
                label="exact off-axis branches" if sign > 0 else None)
        ax.plot(delta_c, sign * phi_leading, color=palette["ochre"], lw=0.9,
                linestyle="--", label=r"leading $\pm\sqrt{-6\delta}$" if sign > 0 else None)
        for delta, phi_value in zip(delta_c, sign * phi_exact):
            add_row(
                rows, panel="C", route="A3-real-even-heat-path",
                series=f"A3 exact {label}", kind="exact-analytic-branch",
                x=delta, y=phi_value, phi=phi_value,
                source="research/r072s_report-source.md", pointer="(4.3)-(4.13)",
                status="proved", note="q_tau(cos(phi))=0",
            )
        for delta, phi_value in zip(delta_c, sign * phi_leading):
            add_row(
                rows, panel="C", route="A3-real-even-heat-path",
                series=f"A3 leading {label}", kind="proved-leading-asymptotic",
                x=delta, y=phi_value, phi=phi_value,
                source="research/r072s_report-source.md", pointer="(4.12)-(4.13)",
                status="leading-order", note="phi^2=-6delta",
            )
    ax.plot(delta_all_c, np.zeros_like(delta_all_c), color=palette["red"], lw=1.0,
            label=r"persistent symmetry branch $\phi=0$")
    for delta in delta_all_c:
        add_row(
            rows, panel="C", route="A3-real-even-heat-path",
            series="A3 persistent axis", kind="exact-symmetry-branch",
            x=delta, y=0.0, phi=0.0,
            source="research/r072s_report-source.md", pointer="(4.3)",
            status="proved", note="sin(phi)=0",
        )
    ax.axvline(0.0, color=palette["red"], lw=0.9, linestyle=":")
    ax.scatter([0.0], [0.0], s=25, color=palette["red"], marker="o", zorder=5)
    ax.text(-0.27, 1.42, "4 distinct", fontsize=6.0, color=palette["blueDark"])
    ax.text(0.012, 0.12, "$A_3$\n2 distinct", fontsize=5.8, color=palette["red"])
    ax.text(0.075, 1.42, "2 distinct", fontsize=6.0, color=palette["muted"])
    ax.text(-0.335, -1.53, r"simple $\phi=\pi$ branch omitted; included in counts",
            fontsize=4.65, color=palette["muted"], ha="left")
    ax.set_xlim(float(panel_c["deltaMinimum"]), float(panel_c["deltaMaximum"]))
    ax.set_ylim(-1.65, 1.65)
    ax.set_xlabel(r"$\delta=y-\log 2$", fontsize=7.0)
    ax.set_ylabel(r"critical angle $\phi$", fontsize=7.0)
    panel_title(ax, "C", "Real-even $A_3$ collision",
                "slice-transverse only; distinct counts 4 / 2 / 2", palette)
    ax.legend(loc="lower left", fontsize=5.15, frameon=False, handlelength=2.0)

    fig.text(
        0.055, 0.055,
        "R0.72S  |  exact-formula presentation; no PDE solve or global caustic fit  |  Clay problem remains open",
        fontsize=5.4, color=palette["muted"], ha="left",
    )

    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    fig.savefig(ROOT / "figure.pdf", facecolor=palette["paper"])
    fig.savefig(ROOT / "figure.svg", facecolor=palette["paper"])
    fig.savefig(
        ROOT / "figure.png", dpi=int(config["figure"]["pngDpi"]),
        facecolor=palette["paper"],
    )
    plt.close(fig)

    a4_residual = np.max(np.abs((15.0 * a_values) ** 2 + (5.0 * b_values) ** 2 - 1.0))
    a2_residual = np.max(np.abs(-np.cos(xi_exact) + k_values * np.cos(2.0 * xi_exact)))
    a3_residual = np.max(np.abs(
        12.0 * b0 * tau_values**8 * np.cos(phi_exact) ** 2
        + 4.0 * a0 * tau_values**3 * np.cos(phi_exact)
        + 1.0 - 3.0 * b0 * tau_values**8
    ))
    formula_checks = {
        "a4SpineResidualMaximum": float(a4_residual),
        "a2CriticalResidualMaximum": float(a2_residual),
        "a2LeadingSquaredResidualMaximum": float(np.max(np.abs(xi_leading**2 + 2.0 * delta_b))),
        "a3CriticalResidualMaximum": float(a3_residual),
        "a3LeadingSquaredResidualMaximum": float(np.max(np.abs(phi_leading**2 + 6.0 * delta_c))),
        "coefficientDerivativeJetDeterminant": 5400,
        "a2DistinctCriticalCounts": {"before": 4, "at": 3, "after": 2},
        "a3DistinctCriticalCounts": {"before": 4, "at": 2, "after": 2},
        "multiplicityCountAtEachCrossing": 4,
    }
    counts = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABC"}
    elapsed = time.perf_counter() - started
    results = {
        "schemaVersion": "r072s-figure-results-v1",
        "status": "passed",
        "rowCount": len(rows),
        "panelRowCounts": counts,
        "formulaChecks": formula_checks,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "noPdeEvolution": True,
        "noFiniteFit": True,
        "numericSamplingDoesNotReplaceContinuousProof": True,
        "repositoryCommitAtBuild": commit,
        "formalSourceCommit": source_commit,
        "verifiedTrackedTreeClean": True,
        "verifiedPackageSourcesAtBuildCommit": True,
        "packageSourceGitBlobs": source_blobs,
        "packageSourceHashes": {name: sha256(ROOT / name) for name in PACKAGE_SOURCES},
        "runtimeLineage": lineage,
        "lineageStatuses": {
            "producer": "passed",
            "independent": "passed",
            "crosscheck": "passed",
            "formalSourceReady": True,
            "temporaryUnsealedSourceAllowed": False,
        },
        "certificateLedgerAudit": ledger,
        "claimBoundary": contract["claimBoundary"],
    }
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = [
        "bundle=R0.72S exact-formula journal figure",
        f"pythonExecutable={sys.executable}",
        f"pythonVersion={sys.version.replace(chr(10), ' ')}",
        f"numpyVersion={np.__version__}",
        f"matplotlibVersion={mpl.__version__}",
        f"platform={platform.platform()}",
        f"machine={platform.machine()}",
        f"cpuCount={os.cpu_count()}",
        f"repositoryCommit={commit}",
        "gpu=not used",
        "dgx=not used",
    ]
    (ROOT / "environment.txt").write_text("\n".join(environment) + "\n", encoding="utf-8")
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"time": utc_now(), "event": "data-ready", "rows": len(rows), "counts": counts}) + "\n")
        handle.write(json.dumps({"time": utc_now(), "event": "complete", "elapsedSeconds": elapsed}) + "\n")
    (ROOT / "resource-log.ndjson").write_text(
        json.dumps({
            "time": utc_now(), "event": "complete", "elapsedSeconds": elapsed,
            "maxRssMb": results["maxRssMb"], "rows": len(rows), "pid": os.getpid(),
        }) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "passed", "rows": len(rows), "counts": counts,
        "elapsedSeconds": elapsed,
    }, indent=2))


if __name__ == "__main__":
    main()
