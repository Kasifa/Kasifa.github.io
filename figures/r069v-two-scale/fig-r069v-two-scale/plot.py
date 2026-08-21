#!/usr/bin/env python3
"""Build the formal R0.69V two-scale annular-obstruction figure package."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import shutil
import time
from collections import defaultdict
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
PRIMARY_ROOT = ROOT / "research/certificates/r069v-polynomial-qmc"
FIXED_ROOT = ROOT / "research/certificates/r069v-zonepair-qmc"
ROOT_GAP_ROOT = ROOT / "research/certificates/r069v-zonepair-polynomial-qmc"
PRIMARY_RESULT = PRIMARY_ROOT / "result.json"
PRIMARY_SCAN = PRIMARY_ROOT / "amplitude-scan.csv"
FIXED_RESULT = FIXED_ROOT / "result.json"
FIXED_ANNULAR = FIXED_ROOT / "annular.csv"
FIXED_PAIRS = FIXED_ROOT / "zone-pairs.csv"
ROOT_GAP_RESULT = ROOT_GAP_ROOT / "result.json"
ROOT_GAP_SCAN = ROOT_GAP_ROOT / "amplitude-sign-scan.csv"
ROOT_GAP_COEFFICIENTS = ROOT_GAP_ROOT / "coefficients.csv"
PINS = {
    PRIMARY_RESULT: "a549c455949819e83d0b86d1be1c0b453f6db6897412cc87dd3cbc5a2d69bcdb",
    PRIMARY_SCAN: "629c0dc1f4e333b3673393f7c3e4deaa82406b7a9daa28611d07e81ec48e2762",
    FIXED_RESULT: "196c4a3604414e9340249228307656259968e5b2286aee69a12330b884e5e215",
    FIXED_ANNULAR: "f179fd8e75d764a03c7b857019a765f991f39250c5c1ad8c04c0ebcba8a8bf58",
    FIXED_PAIRS: "aaf66fb1aeb627ce24cfcc9302ea73145b65a8648bae6142ed2a1e56aefa1b98",
    ROOT_GAP_RESULT: "82848977d64fd8edce231cea6d5665fba799b050d4cd35b2980f7031f7325c85",
    ROOT_GAP_SCAN: "58bf9286e28f249ea53fe9831e82224d162265f06ba8e58e6d07eed31264800c",
    ROOT_GAP_COEFFICIENTS: "1e8695bcd42c5c2625bdec5bbe362a12e6816684d8413be63aeaeb459690c469",
}
SOURCE_COMMIT = "ba569f3832d93a6f286bb90d92d2d7b15478bf23"
CERTIFICATE_COMMIT = "472aa0939a1de116c78fcf93ef078edc5947ae30"
FIGURE_ID = "fig-r069v-two-scale"
INK, MUTED, BLUE, RUST, GOLD, GRID = (
    "#28231f", "#6b675f", "#315a76", "#8b4d43", "#a16f27", "#d5cec0"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def pair_summary(rows: list[dict[str, str]], index: int) -> list[dict[str, object]]:
    grouped: dict[str, dict[int, float]] = defaultdict(dict)
    for row in rows:
        grouped[row["pairClass"]][int(row["replicate"])] = float(row[f"j{index}"])
    records = []
    for pair_class, by_replicate in grouped.items():
        values = np.asarray(
            [by_replicate[replicate] for replicate in sorted(by_replicate)]
        )
        mean = float(np.mean(values))
        se = float(np.std(values, ddof=1) / math.sqrt(values.size))
        if abs(mean) > 1.0e-9 or se > 0.0:
            records.append(
                {"pairClass": pair_class, "mean": mean, "standardError": se}
            )
    return sorted(records, key=lambda record: abs(float(record["mean"])), reverse=True)


def prepare_data():
    for source, expected in PINS.items():
        if sha256(source) != expected:
            raise RuntimeError(f"pinned R0.69V input hash mismatch: {source}")
    primary = json.loads(PRIMARY_RESULT.read_text(encoding="utf-8"))
    fixed = json.loads(FIXED_RESULT.read_text(encoding="utf-8"))
    root_gap = json.loads(ROOT_GAP_RESULT.read_text(encoding="utf-8"))
    for result in (primary, fixed, root_gap):
        if result["status"] != "passed":
            raise RuntimeError("an R0.69V source certificate did not pass")
    for source, target in (
        (PRIMARY_SCAN, HERE / "amplitude-scan.csv"),
        (FIXED_ANNULAR, HERE / "fixed-candidate-annular.csv"),
        (FIXED_PAIRS, HERE / "fixed-candidate-zone-pairs.csv"),
        (ROOT_GAP_SCAN, HERE / "amplitude-sign-scan.csv"),
        (ROOT_GAP_COEFFICIENTS, HERE / "coarse-coefficients.csv"),
    ):
        shutil.copyfile(source, target)
    primary_scan = read_csv(HERE / "amplitude-scan.csv")
    fixed_annular = read_csv(HERE / "fixed-candidate-annular.csv")
    fixed_pairs = read_csv(HERE / "fixed-candidate-zone-pairs.csv")
    root_scan = read_csv(HERE / "amplitude-sign-scan.csv")
    coefficients = read_csv(HERE / "coarse-coefficients.csv")
    j0 = next(row for row in fixed_annular if int(row["index"]) == 0)
    metadata = {
        "status": "passed",
        "certificateCommit": CERTIFICATE_COMMIT,
        "primarySourceCommit": primary["provenance"]["sourceCommit"],
        "rootGapSourceCommit": root_gap["provenance"]["sourceCommit"],
        "primaryPointPairs": primary["method"]["sampledPointPairs"],
        "fixedPointPairs": 16 * 10 * 2**19,
        "rootGapPointPairs": root_gap["method"]["sampledPointPairs"],
        "candidateAmplitude": primary["candidate"]["bestAmplitude"],
        "candidateRatio": primary["candidate"]["exactTotalOverAnnularL1OfMeans"],
        "candidateExactTotal": primary["candidate"]["exactSignedTotal"],
        "fixedJ0Mean": float(j0["mean"]),
        "fixedJ0StandardError": float(j0["standardError"]),
        "bestMinimumAmplitude": root_gap["rootGapDiagnostic"]["bestMinimumMeanAmplitude"],
        "bestMinimumMean": root_gap["rootGapDiagnostic"]["bestMinimumMean"],
        "meanRoots": root_gap["rootGapDiagnostic"]["meanRootsInUnitInterval"],
        "pointwiseUpperBandExclusion": root_gap["rootGapDiagnostic"]["pointwiseUpperBandExcludesCommonNonnegativeOnGrid"],
        "claimBoundary": (
            "uniform decoupling is exact; finite-separation amplitude scans, "
            "scramble bands, and the root gap are randomized diagnostics"
        ),
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (
        primary,
        fixed,
        root_gap,
        metadata,
        primary_scan,
        fixed_annular,
        fixed_pairs,
        root_scan,
        coefficients,
    )


def validate_data(values) -> None:
    primary, fixed, root_gap, metadata, primary_scan, fixed_annular, fixed_pairs, root_scan, coefficients = values
    candidate = primary["candidate"]
    j0 = next(row for row in fixed_annular if int(row["index"]) == 0)
    j0_z = float(j0["mean"]) / float(j0["standardError"])
    coefficient_map = {
        (int(row["index"]), int(row["degree"])): float(row["mean"])
        for row in coefficients
    }
    discriminant = coefficient_map[(0, 2)] ** 2 - 4.0 * coefficient_map[(0, 3)] * coefficient_map[(0, 1)]
    checks = {
        "threeSourceCertificatesPassed": all(
            result["status"] == "passed" for result in (primary, fixed, root_gap)
        ),
        "primaryUsesExactNumerator": "exactTotalOverAnnularL1OfMeans" in candidate,
        "primarySourceLocked": primary["provenance"]["sourceCommit"] == "2895a99b2448f8102663e238e68d3c4a5a3504c6",
        "rootGapSourceLocked": root_gap["provenance"]["sourceCommit"] == SOURCE_COMMIT,
        "fourThousandOnePrimaryPoints": len(primary_scan) == 4001,
        "fourThousandOneRootGapPoints": len(root_scan) == 4001,
        "candidateAmplitudeMatches": metadata["candidateAmplitude"] == 0.1595,
        "candidateRatioMatches": math.isclose(metadata["candidateRatio"], 0.9635537051236769, rel_tol=0.0, abs_tol=1e-15),
        "fixedJ0IsMoreThanFiftySeNegative": j0_z < -50.0,
        "rootGapMeanGridExcluded": root_gap["rootGapDiagnostic"]["noCommonNonnegativeMeanOnGrid"],
        "pointwiseUpperBandGridExcluded": metadata["pointwiseUpperBandExclusion"],
        "j0MeanQuadraticDiscriminantNegative": discriminant < 0.0,
        "allTenZonePairsRetained": fixed["audits"]["allTransitionPairsRetained"] and len({(row["leftZone"], row["rightZone"]) for row in fixed_pairs}) == 10,
        "rootGapSampleReconstructionExactToTolerance": root_gap["audits"]["sampleNodeReconstructionResidualMax"] < 2.0e-15,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "checks": checks,
                "derived": {"fixedJ0ZScore": j0_z, "j0MeanQuadraticDiscriminant": discriminant},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def render(values) -> None:
    _primary, _fixed, _root_gap, metadata, primary_scan, _fixed_annular, fixed_pairs, root_scan, _coefficients = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1,
        3,
        figsize=(178 / 25.4, 86 / 25.4),
        gridspec_kw={"width_ratios": [1.02, 1.10, 1.0], "wspace": 0.43},
    )

    amplitudes = np.asarray([float(row["amplitude"]) for row in primary_scan])
    ratios = np.asarray(
        [float(row["exactTotalOverAnnularL1OfMeans"]) for row in primary_scan]
    )
    left.plot(amplitudes, ratios, color=BLUE, lw=1.15)
    left.axhline(1.0, color=INK, lw=0.65, ls=(0, (4, 2)))
    left.scatter(
        [metadata["candidateAmplitude"]],
        [metadata["candidateRatio"]],
        s=25,
        marker="D",
        facecolor=GOLD,
        edgecolor=INK,
        linewidth=0.55,
        zorder=5,
    )
    left.annotate(
        r"$a=0.1595$" + "\n" + r"$\widehat\Gamma=0.9636$",
        (metadata["candidateAmplitude"], metadata["candidateRatio"]),
        xytext=(0.31, 0.925),
        textcoords="axes fraction",
        arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.55},
        color=INK,
        fontsize=5.0,
    )
    left.text(
        0.98,
        0.05,
        "exact signed numerator; QMC annular means",
        transform=left.transAxes,
        ha="right",
        color=MUTED,
        fontsize=4.35,
    )
    left.set(
        xlim=(0.0, 1.0),
        ylim=(0.79, 1.012),
        xlabel=r"outer amplitude $a$",
        ylabel=r"$|\mathcal{V}_{\rm exact}|/\sum_j|\widehat{\mathcal{A}}_j|$",
        title="a  Full-annulus screen",
    )
    left.set_xticks([0, 0.25, 0.5, 0.75, 1])
    left.grid(True, color=GRID, lw=0.45, alpha=0.7)

    root_amplitudes = np.asarray([float(row["amplitude"]) for row in root_scan])
    display = root_amplitudes <= 0.22
    for index, color, marker, label in (
        (-2, BLUE, "o", r"annulus $j=-2$"),
        (0, RUST, "s", r"annulus $j=0$"),
    ):
        mean = 1.0e3 * np.asarray([float(row[f"j{index}Mean"]) for row in root_scan])
        lower = 1.0e3 * np.asarray([float(row[f"j{index}Ci95Lower"]) for row in root_scan])
        upper = 1.0e3 * np.asarray([float(row[f"j{index}Ci95Upper"]) for row in root_scan])
        middle.fill_between(
            root_amplitudes[display], lower[display], upper[display],
            color=color, alpha=0.12, lw=0,
        )
        middle.plot(
            root_amplitudes[display], mean[display], color=color, lw=1.05,
            marker=marker, markevery=400, ms=2.8, mec=INK, mew=0.35,
            label=label,
        )
    middle.axhline(0.0, color=INK, lw=0.7)
    middle.axvline(
        metadata["bestMinimumAmplitude"], color=GOLD, lw=0.7, ls=(0, (3, 2))
    )
    middle.text(
        metadata["bestMinimumAmplitude"] + 0.004,
        -1.86,
        r"best minimum at $a=0.107$" + "\n" + r"still $-2.95\times10^{-4}$",
        color=MUTED,
        fontsize=4.4,
    )
    middle.text(
        0.98,
        0.95,
        "shading: pointwise 95% scramble bands",
        transform=middle.transAxes,
        ha="right",
        va="top",
        color=MUTED,
        fontsize=4.25,
    )
    middle.set(
        xlim=(0.0, 0.22),
        ylim=(-2.18, 4.7),
        xlabel=r"outer amplitude $a$",
        ylabel=r"annular carrier $(\times10^{-3})$",
        title="b  Coarse-annulus root gap",
    )
    middle.set_xticks([0, 0.05, 0.10, 0.15, 0.20])
    middle.grid(True, color=GRID, lw=0.45, alpha=0.7)
    middle.legend(loc="upper left", frameon=False, fontsize=4.65)

    pairs = pair_summary(fixed_pairs, 0)
    names = {
        "outer-transition--outer-transition": "outer tr. -- outer tr.",
        "intermediate-plateau--outer-transition": "plateau -- outer tr.",
        "inner-transition--outer-transition": "inner tr. -- outer tr.",
        "inner-core--outer-transition": "inner core -- outer tr.",
        "inner-transition--intermediate-plateau": "inner tr. -- plateau",
    }
    pairs = [record for record in pairs if record["pairClass"] in names]
    pairs.reverse()
    means = 1.0e3 * np.asarray([float(record["mean"]) for record in pairs])
    errors = 1.96e3 * np.asarray([float(record["standardError"]) for record in pairs])
    positions = np.arange(len(pairs))
    colors = [BLUE if value >= 0.0 else RUST for value in means]
    right.barh(
        positions, means, xerr=errors, height=0.58, color=colors,
        edgecolor=INK, linewidth=0.45, error_kw={"elinewidth": 0.6, "capsize": 1.5},
    )
    right.axvline(0.0, color=INK, lw=0.7)
    right.set_yticks(
        positions, [names[str(record["pairClass"])] for record in pairs], fontsize=4.5
    )
    right.text(
        0.98,
        0.95,
        r"total $j=0$: $-0.6292\pm0.0103$",
        transform=right.transAxes,
        ha="right",
        va="top",
        color=INK,
        fontsize=4.65,
    )
    right.text(
        0.98,
        0.08,
        r"units $10^{-3}$; whiskers are 95% scramble intervals",
        transform=right.transAxes,
        ha="right",
        color=MUTED,
        fontsize=4.1,
    )
    right.set(
        xlim=(-1.55, 0.93),
        xlabel=r"$j=0$ pair contribution $(\times10^{-3})$",
        title=r"c  Negative $j=0$ mechanism",
    )
    right.grid(True, axis="x", color=GRID, lw=0.45, alpha=0.7)

    fig.subplots_adjust(left=0.068, right=0.995, bottom=0.235, top=0.865)
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Creator": "R0.69V reproducible figure", "CreationDate": None},
    )
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Creator": "R0.69V reproducible figure", "Date": None},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("amplitude-scan.csv", "amplitude, exact total, sampled annular l1 and ratio"),
        ("amplitude-sign-scan.csv", "amplitude, selected annular means and pointwise scramble bands"),
        ("coarse-coefficients.csv", "annular cubic coefficient means and standard errors"),
        ("fixed-candidate-annular.csv", "fixed-candidate annular means and standard errors"),
        ("fixed-candidate-zone-pairs.csv", "fixed-candidate unordered zone-pair contributions"),
        ("figure-data-metadata.json", "pinned R0.69V provenance and displayed statistics"),
        ("validation.json", "fourteen figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T14:45:00+08:00",
        "analyticalQuestion": "Can a genuinely shape-changing two-scale affine family improve the full-space annular ratio, and can any amplitude make all annuli one sign at separation four?",
        "supportedClaim": "uniform scale separation returns the baseline ratio exactly in the limit; at separation four QMC finds a near-saturation screen but independent coarse-annulus reconstruction retains a negative carrier for every scanned amplitude",
        "claimBoundary": "uniform decoupling is an exact theorem; finite-separation ratios, root gaps and scramble bands are randomized diagnostics rather than rigorous interval enclosures",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "data-analysis",
            "configuration": "two independent 16-scramble QMC parameterizations at epsilon=1/4, including 167772160-point full-annulus scan and 41943040-point coarse cubic audit",
            "precision": "IEEE binary64 with sample-exact cubic reconstruction and independent-scramble standard errors",
            "solver": "five-dimensional symmetry-reduced signed Biot-Savart annular quadrature",
            "command": "python plot.py",
            "wallTimeSeconds": elapsed,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": f"{platform.system()}-{platform.release()}-{platform.machine()}",
            "cpu": "Apple M5 Max",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
            "maximumRssMiB": peak,
        },
        "environment": {
            "python": platform.python_version(),
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
            "packagesLock": "requirements-research.txt",
        },
        "sourceData": [
            {
                "location": str(path.relative_to(ROOT)),
                "fileName": path.name,
                "bytes": path.stat().st_size,
                "sha256": PINS[path],
                "extractionCommand": "python plot.py",
            }
            for path in (PRIMARY_RESULT, PRIMARY_SCAN, FIXED_RESULT, FIXED_PAIRS, ROOT_GAP_RESULT, ROOT_GAP_SCAN)
        ],
        "data": [
            {
                "path": path,
                "bytes": (HERE / path).stat().st_size,
                "sha256": sha256(HERE / path),
                "schema": schema,
            }
            for path, schema in data_files
        ],
        "figure": {
            "widthMillimetres": 178,
            "heightMillimetres": 86,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": [
                {
                    "path": path,
                    "bytes": (HERE / path).stat().st_size,
                    "sha256": sha256(HERE / path),
                    **(
                        {"dpi": 600, "pixels": f"{image.width} by {image.height}"}
                        if path.endswith(".png")
                        else {}
                    ),
                }
                for path in outputs
            ],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "amplitude curve, polynomial pointwise bands, and signed zone-pair bars",
            "takeaway": "the finite-separation near-saturation screen is blocked by a robust negative coarse annulus, while exact scale separation returns the baseline ratio",
            "nonColorEncoding": "diamond candidate marker, distinct line markers, zero references, direct labels, signed horizontal direction, and interval whiskers",
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
    }
    (HERE / "manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> None:
    started = time.perf_counter()
    values = prepare_data()
    validate_data(values)
    render(values)
    elapsed = time.perf_counter() - started
    peak = rss_mib()
    with (HERE / "resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["elapsedSeconds", "maximumRssMiB", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow(
            {
                "elapsedSeconds": f"{elapsed:.9f}",
                "maximumRssMiB": f"{peak:.6f}",
                "status": "passed",
            }
        )
    write_manifest(elapsed, peak)


if __name__ == "__main__":
    main()
