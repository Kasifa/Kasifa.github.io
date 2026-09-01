#!/usr/bin/env python3
"""Render the source-bound R0.73Y exact-shear figure archive."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.metadata
import json
import math
import os
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
EXPECTED_RUNTIME = {"python": "3.12.13", "numpy": "2.5.2", "matplotlib": "3.10.6"}
RAW_FILES = (
    "environment.json", "figure.pdf", "figure.png", "figure.svg",
    "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "resource-log.ndjson", "results.json", "source-data.csv",
)
SOURCE_FILES = (
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
)
METADATA_FILES = ("SHA256SUMS", "manifest.json", "qa-report.md", "validation.json")
CSV_FIELDS = (
    "panel", "record", "series", "x", "y", "x_unit", "y_unit",
    "evidence_class", "formula_source",
)
FORMULA_SOURCE = "frozen commit 1ecc6fe2, Theorem 1.1 equation (1.4)"
PALETTE = {
    "navy": "#1F4E79", "gold": "#B8841C", "orange": "#C45B32",
    "olive": "#6D7F38", "charcoal": "#263238", "gray": "#7A858E",
    "light_gray": "#D9DEE3", "pale_blue": "#DDEAF3",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "JSON root must be an object: " + path.name)
    return value


def assert_runtime_contract(
    python_version: str,
    numpy_version: str,
    matplotlib_version: str,
) -> None:
    actual = {
        "python": python_version,
        "numpy": numpy_version,
        "matplotlib": matplotlib_version,
    }
    need(actual == EXPECTED_RUNTIME, f"runtime drift: expected {EXPECTED_RUNTIME}, got {actual}")


def live_runtime_versions() -> dict[str, str]:
    versions = {
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "matplotlib": importlib.metadata.version("matplotlib"),
    }
    assert_runtime_contract(versions["python"], versions["numpy"], versions["matplotlib"])
    return versions


def verify_source_files(source_root: Path, config: dict[str, Any]) -> None:
    for relative, expected in config["sourceBinding"]["files"].items():
        path = source_root / relative
        need(path.is_file(), "frozen source file missing: " + relative)
        need(sha256(path) == expected, "frozen source byte drift: " + relative)
    certificate = load_json(source_root / "research/r073y_exact_shear_certificate.json")
    need(certificate.get("status") == "PASS", "certificate status drift")
    need(certificate.get("not_clay") is True, "certificate claim-boundary drift")
    need(
        certificate.get("payload_sha256") == config["sourceBinding"]["certificatePayloadSha256"],
        "certificate payload drift",
    )


def verify_source_binding(source_root: Path, config: dict[str, Any]) -> None:
    need(source_root.is_dir(), "R073Y_SOURCE_ROOT is not a directory")
    process = subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
    )
    need(process.returncode == 0, "R073Y_SOURCE_ROOT is not a readable git checkout")
    actual_commit = process.stdout.strip()
    need(actual_commit == config["sourceBinding"]["commit"], "frozen source commit drift")
    status = subprocess.run(
        ["git", "-C", str(source_root), "status", "--porcelain", "--untracked-files=no"],
        capture_output=True,
        text=True,
    )
    need(status.returncode == 0 and not status.stdout.strip(), "frozen source checkout is dirty")
    verify_source_files(source_root, config)


def preflight_archive() -> None:
    actual = {path.name for path in HERE.iterdir()}
    allowed = set(SOURCE_FILES + RAW_FILES + METADATA_FILES)
    need(set(SOURCE_FILES).issubset(actual), "source inventory is incomplete")
    need(actual.issubset(allowed), "unexpected package entry before render: " + repr(sorted(actual - allowed)))
    need(all((HERE / name).is_file() and not (HERE / name).is_symlink() for name in SOURCE_FILES), "source file or symlink drift")


def prepare_mpl_config() -> tuple[Path, tempfile.TemporaryDirectory[str] | None]:
    raw = os.environ.get("MPLCONFIGDIR")
    if raw:
        path = Path(raw).expanduser().resolve()
        need(path != HERE and HERE not in path.parents, "MPLCONFIGDIR must be outside the archive")
        path.mkdir(parents=True, exist_ok=True)
        return path, None
    owner = tempfile.TemporaryDirectory(prefix="mpl-config-")
    path = Path(owner.name).resolve()
    need(path != HERE and HERE not in path.parents, "system Matplotlib cache entered archive")
    os.environ["MPLCONFIGDIR"] = str(path)
    return path, owner


def number(value: float) -> str:
    value = float(value)
    if value == 0.0:
        return "0"
    return format(value, ".17g")


def generate_payload(config: dict[str, Any], np: Any) -> tuple[list[dict[str, str]], dict[str, Any], dict[str, Any]]:
    rows: list[dict[str, str]] = []
    panel_a = config["panelA"]
    x2 = np.linspace(0.0, float(panel_a["phaseMaximum"]), int(panel_a["points"]))
    profiles: dict[str, Any] = {}
    for scale in panel_a["heatScales"]:
        s = float(scale)
        q = math.exp(-2.0 * s)
        values = 0.5 * (1.0 - q) * (1.0 - q * np.cos(2.0 * x2))
        label = format(s, "g")
        profiles[label] = values
        for index, (x, y) in enumerate(zip(x2, values)):
            rows.append({
                "panel": "A", "record": f"a-{label}-{index:04d}", "series": "D-s-" + label,
                "x": number(x), "y": number(y), "x_unit": "radian", "y_unit": "normalized covariance",
                "evidence_class": "analytic exact formula", "formula_source": FORMULA_SOURCE,
            })
    for series in ("Pi", "S"):
        for index, x in enumerate(x2):
            rows.append({
                "panel": "A", "record": f"a-{series}-{index:04d}", "series": series,
                "x": number(x), "y": "0", "x_unit": "radian", "y_unit": "normalized production",
                "evidence_class": "analytic exact zero", "formula_source": FORMULA_SOURCE,
            })

    panel_b = config["panelB"]
    s_grid = np.geomspace(
        float(panel_b["heatScaleMinimum"]), float(panel_b["heatScaleMaximum"]), int(panel_b["points"])
    )
    q = np.exp(-2.0 * s_grid)
    d_min = 0.5 * (1.0 - q) ** 2
    d_mean = 0.5 * (1.0 - q)
    d_max = 0.5 * (1.0 - np.exp(-4.0 * s_grid))
    statistics = {"pointwise-min": d_min, "spatial-mean": d_mean, "pointwise-max": d_max}
    for series, values in statistics.items():
        for index, (x, y) in enumerate(zip(s_grid, values)):
            rows.append({
                "panel": "B", "record": f"b-{series}-{index:04d}", "series": series,
                "x": number(x), "y": number(y), "x_unit": "heat scale", "y_unit": "normalized covariance",
                "evidence_class": "analytic exact statistic", "formula_source": FORMULA_SOURCE,
            })

    panel_c = config["panelC"]
    amplitude = np.linspace(
        float(panel_c["amplitudeMinimum"]), float(panel_c["amplitudeMaximum"]), int(panel_c["points"])
    )
    cubic = amplitude**3
    amplitude_series = {"positive-size": cubic, "abs-Pi": np.zeros_like(amplitude), "abs-S": np.zeros_like(amplitude)}
    for series, values in amplitude_series.items():
        evidence = "analytic amplitude homogeneity" if series == "positive-size" else "analytic exact zero"
        for index, (x, y) in enumerate(zip(amplitude, values)):
            rows.append({
                "panel": "C", "record": f"c-{series}-{index:04d}", "series": series,
                "x": number(x), "y": number(y), "x_unit": "absolute amplitude", "y_unit": "normalized magnitude",
                "evidence_class": evidence, "formula_source": FORMULA_SOURCE,
            })

    audit_x = np.linspace(0.0, 2.0 * math.pi, 4096, endpoint=False)
    maximum_profile_error = 0.0
    maximum_statistic_error = 0.0
    minimum_covariance = math.inf
    for scale in panel_a["heatScales"]:
        s = float(scale)
        q_scalar = math.exp(-2.0 * s)
        expanded = 0.5 * (1.0 - q_scalar) + 0.5 * (math.exp(-4.0 * s) - q_scalar) * np.cos(2.0 * audit_x)
        closed = 0.5 * (1.0 - q_scalar) * (1.0 - q_scalar * np.cos(2.0 * audit_x))
        maximum_profile_error = max(maximum_profile_error, float(np.max(np.abs(expanded - closed))))
        exact_stats = (
            0.5 * (1.0 - q_scalar) ** 2,
            0.5 * (1.0 - q_scalar),
            0.5 * (1.0 - math.exp(-4.0 * s)),
        )
        sampled_stats = (float(np.min(closed)), float(np.mean(closed)), float(np.max(closed)))
        maximum_statistic_error = max(
            maximum_statistic_error, max(abs(left - right) for left, right in zip(exact_stats, sampled_stats))
        )
        minimum_covariance = min(minimum_covariance, sampled_stats[0])
    tolerance = 5.0e-13
    audit = {
        "checksPassed": maximum_profile_error <= tolerance and maximum_statistic_error <= tolerance and minimum_covariance > 0.0,
        "maximumProfileIdentityError": maximum_profile_error,
        "maximumStatisticError": maximum_statistic_error,
        "minimumAuditedCovariance": minimum_covariance,
        "tolerance": tolerance,
    }
    need(audit["checksPassed"], "analytic formula audit failed")
    arrays = {
        "amplitude": amplitude, "cubic": cubic, "d_max": d_max, "d_mean": d_mean,
        "d_min": d_min, "profiles": profiles, "s_grid": s_grid, "x2": x2,
    }
    return rows, arrays, audit


def add_blossom(fig: Any, Circle: Any, np: Any) -> None:
    center = np.array([0.979, 0.955])
    for angle in np.linspace(0.0, 2.0 * math.pi, 5, endpoint=False):
        position = center + 0.008 * np.array([math.cos(angle), math.sin(angle)])
        fig.add_artist(Circle(position, 0.006, transform=fig.transFigure, facecolor=PALETTE["pale_blue"], edgecolor=PALETTE["navy"], linewidth=0.45, clip_on=False, zorder=20))
    fig.add_artist(Circle(center, 0.0038, transform=fig.transFigure, facecolor=PALETTE["gold"], edgecolor=PALETTE["charcoal"], linewidth=0.4, clip_on=False, zorder=21))


def render_figure(config: dict[str, Any], arrays: dict[str, Any], output: Path, np: Any, matplotlib: Any, plt: Any, Circle: Any) -> dict[str, Any]:
    matplotlib.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 6.4, "axes.titlesize": 7.1,
        "axes.labelsize": 6.4, "xtick.labelsize": 5.7, "ytick.labelsize": 5.7,
        "legend.fontsize": 5.4, "axes.linewidth": 0.6, "lines.linewidth": 1.15,
        "svg.hashsalt": "r073y-exact-shear-archive-v2", "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    width_inches = float(config["widthMillimetres"]) / 25.4
    height_inches = float(config["heightMillimetres"]) / 25.4
    fig, axes = plt.subplots(1, 3, figsize=(width_inches, height_inches), constrained_layout=False)
    fig.subplots_adjust(left=0.069, right=0.987, bottom=0.238, top=0.70, wspace=0.40)
    fig.patch.set_facecolor("white")
    ax_a, ax_b, ax_c = axes
    fig.suptitle("Exact-shear obstruction to production-only coercivity", x=0.069, y=0.962, ha="left", va="top", fontsize=10.2, fontweight="bold", color=PALETTE["charcoal"])
    fig.text(0.069, 0.865, "ANALYTIC EXACT WITNESS - NOT DNS", ha="left", va="center", fontsize=6.2, fontweight="bold", color=PALETTE["charcoal"], bbox={"boxstyle": "round,pad=0.24", "facecolor": "white", "edgecolor": PALETTE["gray"], "linewidth": 0.55})
    fig.text(0.987, 0.865, r"$D_{ii,s}=\frac{1}{2}(1-e^{-2s})(1-e^{-2s}\cos 2x_2)$", ha="right", va="center", fontsize=6.25, color=PALETTE["charcoal"])
    add_blossom(fig, Circle, np)

    scales = [float(value) for value in config["panelA"]["heatScales"]]
    colors = [PALETTE["navy"], PALETTE["gold"], PALETTE["orange"], PALETTE["olive"]]
    styles = ["-", "--", "-.", ":"]
    for scale, color, style in zip(scales, colors, styles):
        label = format(scale, "g")
        ax_a.plot(arrays["x2"] / math.pi, arrays["profiles"][label], color=color, linestyle=style, label=rf"$s={label}$")
    ax_a.axhline(0.0, color=PALETTE["charcoal"], linestyle=(0, (3, 2)), linewidth=0.75)
    ax_a.text(0.04, 0.575, r"$\Pi_s=\mathscr{S}_s=0$", ha="left", va="top", fontsize=5.4, color=PALETTE["charcoal"])
    ax_a.set_title("Heat-gradient covariance profiles", loc="left", pad=5)
    ax_a.set_xlabel(r"phase $x_2/\pi$")
    ax_a.set_ylabel(r"$D_{ii,s}$ (normalized)")
    ax_a.set_xlim(0.0, 2.0); ax_a.set_ylim(-0.025, 0.62)
    ax_a.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0])
    ax_a.legend(loc="upper right", frameon=False, ncol=2, handlelength=2.2, columnspacing=0.75)

    ax_b.loglog(arrays["s_grid"], arrays["d_min"], color=PALETTE["orange"], linestyle="--", label="pointwise min")
    ax_b.loglog(arrays["s_grid"], arrays["d_mean"], color=PALETTE["navy"], linestyle="-", label="spatial mean")
    ax_b.loglog(arrays["s_grid"], arrays["d_max"], color=PALETTE["olive"], linestyle="-.", label="pointwise max")
    ax_b.set_title("Exact statistics across heat scale", loc="left", pad=5)
    ax_b.set_xlabel(r"heat scale $s$"); ax_b.set_ylabel(r"statistic of $D_{ii,s}$")
    ax_b.set_xlim(1.0e-3, 3.0); ax_b.set_ylim(1.0e-6, 0.75)
    ax_b.legend(loc="lower right", frameon=False, handlelength=2.25)
    ax_b.text(0.05, 0.94, r"$\min D>0$ for every $s>0$", transform=ax_b.transAxes, ha="left", va="top", fontsize=5.4, color=PALETTE["charcoal"])

    ax_c.fill_between(arrays["amplitude"], 0.0, arrays["cubic"], color=PALETTE["pale_blue"], alpha=0.72, linewidth=0.0)
    ax_c.plot(arrays["amplitude"], arrays["cubic"], color=PALETTE["navy"], label=r"positive size: $|A|^3$")
    ax_c.axhline(0.0, color=PALETTE["charcoal"], linestyle=(0, (3, 2)), linewidth=0.75)
    ax_c.text(3.42, 1.25, r"$|\Pi_s|=|\mathscr{S}_s|=0$", ha="right", va="bottom", fontsize=5.4, color=PALETTE["charcoal"])
    ax_c.set_title("Amplitude homogeneity", loc="left", pad=5)
    ax_c.set_xlabel(r"amplitude $|A|$"); ax_c.set_ylabel("normalized magnitude")
    ax_c.set_xlim(0.0, 3.5); ax_c.set_ylim(-0.9, 45.0)
    ax_c.legend(loc="upper left", frameon=False)
    ax_c.text(0.05, 0.62, "no finite production-only\nmodulus sees this family", transform=ax_c.transAxes, ha="left", va="bottom", fontsize=5.25, color=PALETTE["charcoal"])

    for marker, axis in zip(("(A)", "(B)", "(C)"), axes):
        axis.text(-0.19, 1.13, marker, transform=axis.transAxes, ha="left", va="bottom", fontsize=7.0, fontweight="bold", color=PALETTE["charcoal"])
        axis.spines["top"].set_visible(False); axis.spines["right"].set_visible(False)
        axis.spines["left"].set_color(PALETTE["gray"]); axis.spines["bottom"].set_color(PALETTE["gray"])
        axis.tick_params(colors=PALETTE["charcoal"], width=0.55, length=2.4)
        axis.grid(True, which="major", axis="y", color=PALETTE["light_gray"], linewidth=0.42, alpha=0.72)
        axis.set_axisbelow(True)
    fig.text(0.069, 0.052, "Normalization: one Fourier shear mode with b=n=1 at a fixed time slice. Closed-form evaluation; no trajectory was numerically evolved.", ha="left", va="bottom", fontsize=5.2, color=PALETTE["gray"])

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    figure_bounds = fig.bbox
    failures: list[dict[str, float | str]] = []
    for artist in fig.findobj(match=lambda item: hasattr(item, "get_window_extent") and item.get_visible()):
        try:
            bounds = artist.get_window_extent(renderer)
        except Exception:
            continue
        if bounds.width == 0.0 and bounds.height == 0.0:
            continue
        if bounds.x0 < figure_bounds.x0 - 1.0 or bounds.y0 < figure_bounds.y0 - 1.0 or bounds.x1 > figure_bounds.x1 + 1.0 or bounds.y1 > figure_bounds.y1 + 1.0:
            failures.append({"artist": type(artist).__name__, "x0": float(bounds.x0), "y0": float(bounds.y0), "x1": float(bounds.x1), "y1": float(bounds.y1)})

    fixed_date = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)
    fig.savefig(output / "figure.pdf", format="pdf", metadata={"Title": "R0.73Y exact-shear obstruction", "Author": "C. K. Zeng", "Subject": "Analytic exact witness, not DNS", "Creator": "r073y-exact-shear-archive-v2", "Producer": "Matplotlib", "CreationDate": fixed_date, "ModDate": fixed_date})
    fig.savefig(output / "figure.svg", format="svg", metadata={"Title": "R0.73Y exact-shear obstruction", "Creator": "r073y-exact-shear-archive-v2", "Date": None})
    fig.savefig(output / "figure.png", format="png", dpi=int(config["pngDpi"]), facecolor="white", metadata={"Software": "r073y-exact-shear-archive-v2"})
    plt.close(fig)
    return {"artistBoundsFailures": failures, "artistBoundsPass": not failures}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")


def write_ndjson(path: Path, rows: list[dict[str, object]]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8", newline="\n")


def create_qa(config: dict[str, Any], output: Path, Image: Any, ImageOps: Any, pdfium: Any) -> dict[str, Any]:
    qa_width = int(float(config["widthMillimetres"]) / 25.4 * int(config["qaDpi"]))
    qa_height = int(float(config["heightMillimetres"]) / 25.4 * int(config["qaDpi"]))
    with Image.open(output / "figure.png") as opened:
        master = opened.convert("RGB")
        final_size = master.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
        final_size.save(output / "qa-final-size.png", dpi=(int(config["qaDpi"]), int(config["qaDpi"])), optimize=False)
        grayscale = ImageOps.grayscale(final_size).convert("RGB")
        grayscale.save(output / "qa-grayscale.png", dpi=(int(config["qaDpi"]), int(config["qaDpi"])), optimize=False)
    document = pdfium.PdfDocument(str(output / "figure.pdf"))
    need(len(document) == 1, "rendered PDF is not one page")
    page = document[0]
    width_points, _ = page.get_size()
    pdf_image = page.render(scale=qa_width / float(width_points)).to_pil().convert("RGB")
    page.close(); document.close()
    if pdf_image.size != (qa_width, qa_height):
        pdf_image = pdf_image.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
    pdf_image.save(output / "qa-pdf.png", dpi=(int(config["qaDpi"]), int(config["qaDpi"])), optimize=False)
    return {"qaPixels": [qa_width, qa_height]}


def render(config: dict[str, Any], source_root: Path, runtime_versions: dict[str, str], mpl_config_policy: str) -> None:
    start_wall = time.perf_counter(); start_cpu = time.process_time(); pid = os.getpid()
    progress: list[dict[str, object]] = []
    def event(name: str, **details: object) -> None:
        progress.append({"elapsedSeconds": time.perf_counter() - start_wall, "event": name, "pid": pid, "utc": utc_now(), **details})

    event("preflight-pass", sourceCommit=config["sourceBinding"]["commit"], runtime=runtime_versions)
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    from PIL import Image, ImageOps
    import pypdfium2 as pdfium

    with tempfile.TemporaryDirectory(prefix="figure-output-") as temporary:
        output = Path(temporary)
        rows, arrays, audit = generate_payload(config, np)
        event("source-data-generated", rows=len(rows), formulaAudit=audit)
        render_audit = render_figure(config, arrays, output, np, matplotlib, plt, Circle)
        need(render_audit["artistBoundsPass"], "renderer artist bounds failed")
        event("journal-exports-rendered", outputs=["figure.pdf", "figure.png", "figure.svg"])
        qa = create_qa(config, output, Image, ImageOps, pdfium)
        event("qa-assets-rendered", outputs=["qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"])
        write_csv(output / "source-data.csv", rows)
        results = {
            "claimBoundary": {"analyticExactWitness": True, "dns": False, "notClay": True},
            "formulaAudit": audit,
            "render": {
                **render_audit,
                "figurePhysicalSizeMillimetres": [config["widthMillimetres"], config["heightMillimetres"]],
                "pngDpi": config["pngDpi"],
                **qa,
            },
            "rowCounts": {
                "A": sum(row["panel"] == "A" for row in rows),
                "B": sum(row["panel"] == "B" for row in rows),
                "C": sum(row["panel"] == "C" for row in rows),
                "total": len(rows),
            },
            "schema": "r073y-exact-shear-results-v2",
            "sourceBinding": {
                "certificatePayloadSha256": config["sourceBinding"]["certificatePayloadSha256"],
                "commit": config["sourceBinding"]["commit"],
                "exclusiveFormulaSource": True,
                "status": "PASS",
            },
            "status": "PASS",
        }
        (output / "results.json").write_text(canonical(results), encoding="utf-8", newline="\n")
        memory_bytes = None
        try:
            page_size = int(os.sysconf("SC_PAGE_SIZE")); pages = int(os.sysconf("SC_PHYS_PAGES")); memory_bytes = page_size * pages
        except (ValueError, OSError, AttributeError):
            pass
        environment = {
            "createdAtUtc": utc_now(), "logicalCpuCount": os.cpu_count(), "machine": platform.machine(),
            "matplotlibConfigPolicy": mpl_config_policy, "memoryBytes": memory_bytes,
            "operatingSystem": platform.platform(), "packages": {
                "matplotlib": runtime_versions["matplotlib"], "numpy": runtime_versions["numpy"],
                "pillow": importlib.metadata.version("pillow"), "pypdf": importlib.metadata.version("pypdf"),
                "pypdfium2": importlib.metadata.version("pypdfium2"),
            }, "processes": 1, "python": runtime_versions["python"],
            "schema": "r073y-environment-observation-v2", "sourceRootPolicy": "external environment variable; absolute value intentionally not recorded",
            "threadsPerProcess": 1,
        }
        (output / "environment.json").write_text(canonical(environment), encoding="utf-8", newline="\n")
        event("archive-raw-layer-complete", deterministicOutputs=8, nondeterministicObservabilityOutputs=3)
        write_ndjson(output / "progress.ndjson", progress)
        usage = resource.getrusage(resource.RUSAGE_SELF)
        rss_unit = "bytes" if sys.platform == "darwin" else "kilobytes"
        resource_rows = [{
            "cpuSeconds": time.process_time() - start_cpu, "maximumResidentSetSizeRaw": float(usage.ru_maxrss),
            "maximumResidentSetSizeRawUnit": rss_unit, "pid": pid, "processes": 1,
            "schema": "r073y-resource-observation-v2", "threadsPerProcess": 1,
            "utc": utc_now(), "wallSeconds": time.perf_counter() - start_wall,
        }]
        write_ndjson(output / "resource-log.ndjson", resource_rows)
        for name in RAW_FILES:
            need((output / name).is_file(), "renderer omitted raw/result file: " + name)
        for name in RAW_FILES:
            os.replace(output / name, HERE / name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    need(args.render, "use --render")
    preflight_archive()
    config = load_json(HERE / "config.json")
    runtime_versions = live_runtime_versions()
    source_value = os.environ.get("R073Y_SOURCE_ROOT")
    need(bool(source_value), "R073Y_SOURCE_ROOT is required")
    source_root = Path(str(source_value)).expanduser().resolve()
    verify_source_binding(source_root, config)
    mpl_config, owner = prepare_mpl_config()
    try:
        policy = "explicit external environment directory" if owner is None else "system temporary directory removed after render"
        render(config, source_root, runtime_versions, policy)
    finally:
        if owner is not None:
            owner.cleanup()
    print("PASS: source-bound 600-dpi analytic figure raw layer rendered")


if __name__ == "__main__":
    main()
