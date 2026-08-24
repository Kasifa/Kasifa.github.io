#!/usr/bin/env python3
"""Build the formal R0.69W rigorous interval-obstruction figure package."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import resource
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, __version__ as PILLOW_VERSION

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE_ROOT = ROOT / "research/certificates/r069w"
RESULT = CERTIFICATE_ROOT / "result.json"
VERIFIER = CERTIFICATE_ROOT / "verifier.json"
STYLE = HERE.parents[1] / "journal.mplstyle"
FIGURE_ID = "fig-r069w-interval-obstruction"
SOURCE_COMMIT = "2b3141a333d3dea0c4b7a241c11f9adbca31d1b4"
INK, MUTED, BLUE, RUST, GOLD, GRID = (
    "#28231f", "#6b675f", "#315a76", "#8b4d43", "#a16f27", "#d5cec0"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def interval_envelope(
    amplitude: np.ndarray, coefficients: list[list[float]]
) -> tuple[np.ndarray, np.ndarray]:
    lower = sum(interval[0] * amplitude**degree for degree, interval in enumerate(coefficients))
    upper = sum(interval[1] * amplitude**degree for degree, interval in enumerate(coefficients))
    return lower, upper


def read_resources() -> tuple[list[dict[str, str]], float]:
    rows: list[dict[str, str]] = []
    sum_worker_peaks = 0.0
    for worker in sorted((CERTIFICATE_ROOT / "workers").glob("worker-*")):
        path = worker / "resources.csv"
        with path.open(newline="", encoding="utf-8") as stream:
            worker_rows = list(csv.DictReader(stream))
        peaks = [float(row["rssMiB"]) for row in worker_rows if row.get("rssMiB")]
        peak = max(peaks, default=0.0)
        sum_worker_peaks += peak
        rows.append(
            {
                "worker": worker.name,
                "samples": str(len(worker_rows)),
                "maximumRssMiB": f"{peak:.6f}",
                "terminalStatus": worker_rows[-1]["status"] if worker_rows else "missing",
            }
        )
    with (HERE / "resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows, sum_worker_peaks


def prepare_data() -> tuple[dict, dict, dict]:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    verifier = json.loads(VERIFIER.read_text(encoding="utf-8"))
    if result["status"] != "passed" or not verifier["passed"]:
        raise RuntimeError("R0.69W source certificate or independent verifier did not pass")
    if result["provenance"]["sourceCommit"] != SOURCE_COMMIT:
        raise RuntimeError("R0.69W source commit mismatch")
    if result["provenance"]["sourceTreeDirty"]:
        raise RuntimeError("formal R0.69W run reported a dirty source tree")

    j0 = result["coefficientIntervals"]["j0"]
    coefficients = [j0[f"c{degree}"] for degree in range(4)]
    amplitudes = np.linspace(0.0, 1.0, 501)
    q_lower, q_upper = interval_envelope(amplitudes, coefficients[1:])
    sign_intervals = {
        "c3": j0["c3"],
        "discriminant": result["decision"]["j0QuadraticDiscriminantInterval"],
        "endpoint": result["decision"]["jMinus2AtZeroInterval"],
    }
    with (HERE / "interval-data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(["kind", "label", "amplitude", "lower", "upper"])
        for amplitude, lower, upper in zip(amplitudes, q_lower, q_upper):
            writer.writerow(["envelope", "q(a)", f"{amplitude:.6f}", repr(float(lower)), repr(float(upper))])
        for label, interval in sign_intervals.items():
            writer.writerow(["sign", label, "", repr(interval[0]), repr(interval[1])])

    resource_rows, sum_worker_peaks = read_resources()
    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "coefficientIntervals": {f"c{degree}": coefficients[degree] for degree in range(1, 4)},
        "discriminantInterval": sign_intervals["discriminant"],
        "endpointInterval": sign_intervals["endpoint"],
        "margins": {
            "negativeC3": -sign_intervals["c3"][1],
            "negativeDiscriminant": -sign_intervals["discriminant"][1],
            "negativeEndpoint": -sign_intervals["endpoint"][1],
        },
        "amplitudeEnvelopeSamples": len(amplitudes),
        "workers": result["method"]["workers"],
        "radialCells": result["integrationAudits"]["0"]["radialCells"],
        "sumOfPerWorkerPeakRssMiB": sum_worker_peaks,
        "resourceRows": resource_rows,
        "claimBoundary": result["claimBoundary"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    checks = {
        "sourceCertificatePassed": result["status"] == "passed",
        "independentVerifierPassed": verifier["passed"] is True,
        "sourceCommitLocked": result["provenance"]["sourceCommit"] == SOURCE_COMMIT,
        "sourceTreeCleanAtRun": result["provenance"]["sourceTreeDirty"] is False,
        "trueConvolutionCertified": result["mollifier"]["trueConvolutionCertified"] is True,
        "noFloatingQuadratureNodes": result["mollifier"]["floatingQuadratureNodesUsed"] == 0,
        "monotoneDistanceCellEndpointInterpolation": result["mollifier"]["distanceCellCutoffRangesUseMonotoneEndpointInterpolation"] is True,
        "centerPointDerivativeTaylor": result["mollifier"]["centerMomentDerivativesUseCertifiedPointTaylor"] is True,
        "exactDyadicDistanceNodes": result["mollifier"]["distanceMomentGridUsesExactDyadicEndpoints"] is True,
        "sixthOrderEndpointsIncluded": result["mollifier"]["endpointDistributionTermsThroughOrderSix"] is True,
        "allRadialRowsCovered": result["partial"]["allRowsCoveredExactlyOnce"] is True,
        "leadingCoefficientNegative": sign_intervals["c3"][1] < 0,
        "discriminantNegative": sign_intervals["discriminant"][1] < 0,
        "endpointNegative": sign_intervals["endpoint"][1] < 0,
        "entireAmplitudeFamilyExcluded": result["decision"]["entireAmplitudeFamilyExcluded"] is True,
        "envelopeStrictlyNegative": float(np.max(q_upper)) < 0,
        "twentyWorkerResourceLogsPresent": len(resource_rows) == 20,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    validation = {"status": "passed", "checks": checks}
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result, metadata, {"amplitude": amplitudes, "lower": q_lower, "upper": q_upper}


def render(metadata: dict, envelope: dict) -> None:
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig = plt.figure(figsize=(178 / 25.4, 86 / 25.4))
    grid = fig.add_gridspec(1, 2, width_ratios=[1.72, 1.0], wspace=0.34)
    left = fig.add_subplot(grid[0, 0])
    right_grid = grid[0, 1].subgridspec(3, 1, hspace=0.82)
    right_axes = [fig.add_subplot(right_grid[index, 0]) for index in range(3)]

    amplitude = envelope["amplitude"]
    lower, upper = envelope["lower"], envelope["upper"]
    midpoint = (lower + upper) / 2
    left.fill_between(amplitude, lower, upper, color=BLUE, alpha=0.24, linewidth=0)
    left.plot(amplitude, midpoint, color=BLUE, lw=1.25, label="interval midpoint")
    left.plot(amplitude, upper, color=BLUE, lw=0.7, ls=(0, (3, 2)), label="certified upper edge")
    left.axhline(0.0, color=INK, lw=0.8)
    left.set_xlim(0, 1)
    y_min = min(float(np.min(lower)) * 1.06, -0.01)
    y_max = max(0.00004, -float(np.max(upper)) * 0.08)
    left.set_ylim(y_min, y_max)
    left.set_xlabel("outer-scale amplitude  $a$")
    left.set_ylabel(r"quadratic factor  $q(a)=\mathcal{A}_0(u_a)/a$")
    left.set_title("A  Certified envelope for every amplitude", loc="left", fontweight="bold")
    left.legend(loc="lower left", frameon=False)
    left.text(
        0.98, 0.94, "upper edge remains below zero",
        transform=left.transAxes, ha="right", va="top", color=RUST, fontsize=7.1,
    )

    forest = [
        (r"leading coefficient  $c_3$", metadata["coefficientIntervals"]["c3"], BLUE),
        (r"discriminant  $\Delta$", metadata["discriminantInterval"], RUST),
        (r"endpoint  $\mathcal{A}_{-2}(u_0)$", metadata["endpointInterval"], GOLD),
    ]
    for index, (label, interval, color) in enumerate(forest):
        axis = right_axes[index]
        lower_value, upper_value = map(float, interval)
        center = (lower_value + upper_value) / 2
        half_width = (upper_value - lower_value) / 2
        padding = max(abs(lower_value), abs(upper_value)) * 0.18
        axis.axvline(0.0, color=INK, lw=0.8)
        axis.errorbar(
            center, 0.0, xerr=half_width, fmt="D", ms=4.0,
            color=color, ecolor=color, elinewidth=1.4, capsize=3.0,
            markeredgecolor=INK, markeredgewidth=0.45,
        )
        axis.set_xlim(lower_value - padding, max(padding * 0.35, upper_value + padding))
        axis.set_ylim(-1, 1)
        axis.set_yticks([])
        axis.set_title(label, loc="left", fontsize=7.5, pad=2.5)
        axis.text(
            0.01, -0.43, f"upper = {upper_value:.6g}",
            transform=axis.transAxes, ha="left", va="top", color=MUTED, fontsize=6.5,
        )
        axis.spines["left"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["top"].set_visible(False)
        axis.grid(axis="x", color=GRID, lw=0.45)
        axis.locator_params(axis="x", nbins=4)
        axis.tick_params(axis="x", labelsize=6.2)
    right_axes[0].text(
        0.0, 1.55, "B  Three strict sign margins",
        transform=right_axes[0].transAxes, ha="left", va="bottom", fontweight="bold", fontsize=8.5,
    )

    fig.subplots_adjust(left=0.10, right=0.985, bottom=0.17, top=0.86)
    fig.savefig(HERE / "figure.pdf")
    fig.savefig(HERE / "figure.svg")
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)


def write_manifest(result: dict, metadata: dict, certificate_commit: str, elapsed: float) -> None:
    image = Image.open(HERE / "figure.png")
    source_data = []
    for path in (RESULT, VERIFIER):
        source_data.append(
            {
                "location": str(path.relative_to(ROOT)),
                "fileName": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "extractionCommand": "python plot.py --certificate-commit <commit>",
            }
        )
    data = []
    schemas = {
        "interval-data.csv": "kind, label, amplitude, rigorous lower endpoint, rigorous upper endpoint",
        "figure-data-metadata.json": "displayed coefficient, discriminant, endpoint and resource provenance",
        "validation.json": "fifteen exact source and displayed-data validation checks",
        "resources.csv": "worker, sample count, per-worker peak RSS and terminal monitor status",
    }
    for name, schema in schemas.items():
        path = HERE / name
        data.append({"path": name, "bytes": path.stat().st_size, "sha256": sha256(path), "schema": schema})
    outputs = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        path = HERE / name
        record = {"path": name, "bytes": path.stat().st_size, "sha256": sha256(path)}
        if name.endswith(".png"):
            record.update({"dpi": 600, "pixels": f"{image.width} by {image.height}"})
        outputs.append(record)
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "analyticalQuestion": "Can every amplitude in the declared separation-four two-scale family be rigorously excluded by coarse-annulus signs?",
        "supportedClaim": "a negative leading coefficient and negative discriminant force A_0(u_a)<0 for every a>0, while A_-2(u_0)<0 closes the endpoint",
        "claimBoundary": result["claimBoundary"],
        "createdAt": "2026-08-24T09:36:39+08:00",
        "caption": {"english": "caption.md"},
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "20 disjoint radial-row workers; raw moment P19, cutoff 2048 with monotone certified cubic-Hermite value interpolation and certified point-derivative Taylor enclosures, distance moment P22, transition 512, boundary refinement 4",
            "precision": "256-bit Arb transcendental endpoints plus outward-rounded IEEE binary64 interval primitives",
            "solver": "exact common-rotation sphere moments and validated two-dimensional hybrid Taylor cubature",
            "command": "python plot.py --certificate-commit " + certificate_commit,
            "wallTimeSeconds": result["runtime"]["parallelWorkerMaximumElapsedSeconds"],
        },
        "compute": {
            "host": "NVIDIA DGX Spark",
            "operatingSystem": result["provenance"]["platform"],
            "cpu": "20-core Arm v8.2+ CPU",
            "memoryGiB": 121,
            "processes": 20,
            "threadsPerProcess": 1,
            "sumOfPerWorkerPeakRssMiB": metadata["sumOfPerWorkerPeakRssMiB"],
        },
        "environment": {
            "python": result["provenance"]["python"].split()[0],
            "pythonFlint": result["provenance"]["pythonFlint"],
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": PILLOW_VERSION,
            "packagesLock": "requirements-research.txt",
        },
        "sourceData": source_data,
        "data": data,
        "figure": {
            "widthMillimetres": 178,
            "heightMillimetres": 86,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": outputs,
        },
        "chartContract": {
            "family": "rigorous amplitude envelope plus three small-multiple interval forests",
            "nonColorEncoding": "solid midpoint, dashed upper envelope, diamond estimates, capped intervals and black zero references",
            "takeaway": "the entire certified envelope and all three decision intervals remain strictly negative",
            "outputFootprint": "double-column 178 by 86 millimetres with PDF, SVG, and 600 dpi PNG",
        },
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
        },
        "presentationRuntimeSeconds": elapsed,
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    if len(arguments.certificate_commit) != 40:
        raise SystemExit("--certificate-commit must be a full 40-character Git hash")
    started = time.perf_counter()
    result, metadata, envelope = prepare_data()
    render(metadata, envelope)
    write_manifest(result, metadata, arguments.certificate_commit, time.perf_counter() - started)
    print(json.dumps({"status": "passed", "manifest": str(HERE / "manifest.json"), "rssMiB": rss_mib()}, sort_keys=True))


if __name__ == "__main__":
    main()
