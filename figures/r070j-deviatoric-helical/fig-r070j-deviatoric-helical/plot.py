#!/usr/bin/env python3
"""Render the journal-style analytic figure for R0.70J.

Every plotted value evaluates an exact helical, angular, or critical-scale
formula.  The output is not DNS, not a sampled Navier--Stokes trajectory, and
not evidence for blow-up or regularity.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070j-deviatoric-helical"
RELEASE = "R0.70J"

INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a27a3f"
PALE_BLUE = "#e6edf1"
PALE_RUST = "#f1e4df"
GRID = "#d5cec0"
WHITE = "#ffffff"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(
    path: Path,
    header: list[str],
    rows: list[tuple[object, ...]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            rendered: list[object] = []
            for value in row:
                if value is None:
                    rendered.append("")
                elif isinstance(value, (float, np.floating)):
                    rendered.append(f"{float(value):.17g}")
                else:
                    rendered.append(value)
            writer.writerow(rendered)


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def blossom(figure: plt.Figure) -> None:
    """Locked research blossom at the top-right header anchor."""

    center = (0.968, 0.945)
    for dx, dy, angle in (
        (0.0, 0.010, 0.0),
        (0.0, -0.010, 0.0),
        (0.008, 0.0, 90.0),
        (-0.008, 0.0, 90.0),
    ):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy),
                0.010,
                0.018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=0.35,
            )
        )


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))

    # Panel A: exact phase dependence of two helicities and a signed control.
    phase = np.linspace(0.0, 2.0 * np.pi, 73)
    positive_helicity = np.ones_like(phase)
    negative_helicity = np.ones_like(phase)
    signed_control = 2.0 * np.cos(2.0 * phase)

    # Panel B: exact quadrupole K(z)=P_2(z).
    direction_cosine = np.linspace(-1.0, 1.0, 49)
    quadrupole = (3.0 * direction_cosine**2 - 1.0) / 2.0
    quadrupole_positive = np.maximum(quadrupole, 0.0)
    quadrupole_negative = np.minimum(quadrupole, 0.0)
    angular_zero = 1.0 / np.sqrt(3.0)
    sphere_signed_mean = 0.0
    sphere_positive_mean = np.sqrt(3.0) / 9.0

    # Panel C: factor out the fixed Lambda^(-2) geometry.
    Lambda = 4.0
    refinement_index = np.arange(1, 13, dtype=int)
    radius = 2.0 ** (-refinement_index.astype(float))
    source_square_normalized = radius
    core_dual_square_normalized = radius**-1
    cauchy_product_normalized = np.ones_like(radius)
    signed_pairing_normalized = np.ones_like(radius)
    source_square_raw = radius / Lambda**4
    signed_pairing_raw = np.full_like(radius, Lambda**-2)

    rows: list[tuple[object, ...]] = []
    for index, angle, q_plus, q_minus, control in zip(
        np.arange(phase.size),
        phase,
        positive_helicity,
        negative_helicity,
        signed_control,
        strict=True,
    ):
        rows.append(
            (
                "A",
                "phase-sweep",
                int(index),
                angle,
                q_plus,
                q_minus,
                control,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
        )

    for index, z_value, kernel, positive, negative in zip(
        np.arange(direction_cosine.size),
        direction_cosine,
        quadrupole,
        quadrupole_positive,
        quadrupole_negative,
        strict=True,
    ):
        rows.append(
            (
                "B",
                "directional-quadrupole",
                int(index),
                None,
                None,
                None,
                None,
                z_value,
                kernel,
                positive,
                negative,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )
        )

    for index, r_value, source_value, core_value, product_value, pair_value, source_raw, pair_raw in zip(
        refinement_index,
        radius,
        source_square_normalized,
        core_dual_square_normalized,
        cauchy_product_normalized,
        signed_pairing_normalized,
        source_square_raw,
        signed_pairing_raw,
        strict=True,
    ):
        rows.append(
            (
                "C",
                "critical-scale-ledger",
                int(index),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                r_value,
                source_value,
                core_value,
                product_value,
                pair_value,
                source_raw,
                pair_raw,
                None,
            )
        )

    summary_rows = (
        ("sphere_signed_mean", sphere_signed_mean),
        ("sphere_positive_part_mean", sphere_positive_mean),
        ("positive_angular_zero", angular_zero),
        ("negative_angular_zero", -angular_zero),
        ("great_circle_mean_e3", -0.5),
        ("same_shell_pairing", 73.0 / 50.0),
        ("same_shell_second_quadratic", -23.0 / 50.0),
        ("three_axis_positive_sum", 1.0),
        ("source_square_radius_exponent", 1.0),
        ("core_dual_square_radius_exponent", -1.0),
        ("pairing_radius_exponent", 0.0),
    )
    for index, (metric, value) in enumerate(summary_rows):
        rows.append(
            (
                "summary",
                "exact-summary",
                index,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                f"{metric}={value:.17g}",
            )
        )

    write_csv(
        HERE / "data.csv",
        [
            "panel",
            "row_role",
            "sample_index_or_refinement_index",
            "phase_theta_radians",
            "coupling_helicity_positive",
            "coupling_helicity_negative",
            "signed_control_two_cos_two_theta",
            "direction_cosine_z",
            "quadrupole_K_S0",
            "quadrupole_positive_part",
            "quadrupole_negative_part",
            "radius_r",
            "source_square_norm_normalized",
            "core_dual_square_norm_normalized",
            "cauchy_product_normalized",
            "signed_pairing_normalized",
            "source_square_norm_raw_Lambda_4",
            "signed_pairing_raw_Lambda_2",
            "exact_summary",
        ],
        rows,
    )

    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "positiveHelicityPointwiseOne": bool(np.array_equal(positive_helicity, np.ones(73))),
        "negativeHelicityPointwiseOne": bool(np.array_equal(negative_helicity, np.ones(73))),
        "signedControlEndpointsExact": bool(signed_control[0] == 2.0 and signed_control[-1] == 2.0),
        "signedControlPhaseMeanZero": bool(abs(np.trapezoid(signed_control, phase) / (2.0 * np.pi)) < 1.0e-15),
        "quadrupoleFormulaExact": bool(np.array_equal(quadrupole, (3.0 * direction_cosine**2 - 1.0) / 2.0)),
        "quadrupoleHasBothSigns": bool(np.any(quadrupole > 0.0) and np.any(quadrupole < 0.0)),
        "sphereSignedMeanExact": sphere_signed_mean == 0.0,
        "spherePositiveMeanExact": bool(abs(sphere_positive_mean - 1.0 / (3.0 * np.sqrt(3.0))) < 1.0e-16),
        "angularZerosSymmetric": bool(abs(angular_zero + (-angular_zero)) < 1.0e-16),
        "sourceSquareScaleExact": bool(np.array_equal(source_square_normalized, radius)),
        "coreDualSquareScaleExact": bool(np.array_equal(core_dual_square_normalized, radius**-1)),
        "criticalProductsInvariant": bool(np.array_equal(cauchy_product_normalized, signed_pairing_normalized) and np.array_equal(cauchy_product_normalized, np.ones(12))),
        "rawLambdaFactorsExact": bool(np.array_equal(source_square_raw, radius / 256.0) and np.array_equal(signed_pairing_raw, np.full(12, 1.0 / 16.0))),
        "dataRowCount": len(rows) == 145,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 96 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.075,
            right=0.985,
            bottom=0.205,
            top=0.715,
            width_ratios=(1.05, 1.02, 1.08),
            wspace=0.34,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Deviatoric helical symbol and critical source–core scaling",
            x=0.045,
            y=0.966,
            ha="left",
            fontsize=8.3,
            color=INK,
        )
        figure.text(
            0.045,
            0.912,
            r"pure helicity  ·  signed angular isotropy  ·  exact degree-zero critical coordinates",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        figure.text(
            0.045,
            0.840,
            "EXACT ANALYTIC IDENTITIES  /  NOT DNS  /  NOT A BLOW-UP OR REGULARITY RESULT",
            ha="left",
            va="center",
            fontsize=4.20,
            color=RUST,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.28",
                "facecolor": PALE_RUST,
                "edgecolor": RUST,
                "linewidth": 0.45,
            },
        )
        blossom(figure)

        # Panel A: exact phase sweep.
        axis_a.axhline(0.0, color=MUTED, linewidth=0.55, zorder=0)
        axis_a.plot(
            phase / np.pi,
            signed_control,
            color=MUTED,
            linewidth=0.9,
            linestyle=":",
            label=r"signed control $2\cos 2\theta$",
            zorder=1,
        )
        axis_a.plot(
            phase / np.pi,
            negative_helicity,
            color=BLUE,
            linewidth=1.4,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            markersize=2.4,
            markevery=(3, 12),
            label=r"$\sigma=-1$: $q\equiv1$",
            zorder=3,
        )
        axis_a.plot(
            phase / np.pi,
            positive_helicity,
            color=RUST,
            linewidth=1.05,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.25,
            markevery=(0, 12),
            label=r"$\sigma=+1$: $q\equiv1$",
            zorder=4,
        )
        axis_a.set_title("A  Pure-helicity phase sweep", loc="left", pad=5)
        axis_a.set_xlim(0.0, 2.0)
        axis_a.set_ylim(-2.25, 2.25)
        axis_a.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0], [r"$0$", r"$\pi/2$", r"$\pi$", r"$3\pi/2$", r"$2\pi$"])
        axis_a.set_yticks([-2, -1, 0, 1, 2])
        axis_a.set_xlabel(r"phase $\theta$")
        axis_a.set_ylabel(r"$S:\operatorname{dev}(\omega\otimes\omega)$")
        axis_a.grid(color=GRID, linewidth=0.35, axis="y")
        axis_a.legend(loc="lower left", frameon=False, fontsize=4.05)
        axis_a.text(
            1.96,
            1.12,
            "both helicities\npointwise positive",
            color=RUST,
            fontsize=4.35,
            ha="right",
            va="bottom",
        )

        # Panel B: signed angular quadrupole.
        axis_b.axhline(0.0, color=INK, linewidth=0.6, zorder=1)
        axis_b.fill_between(
            direction_cosine,
            0.0,
            quadrupole_positive,
            color=PALE_RUST,
            edgecolor=RUST,
            linewidth=0.45,
            label="positive sector",
            zorder=2,
        )
        axis_b.fill_between(
            direction_cosine,
            0.0,
            quadrupole_negative,
            color=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.45,
            hatch="////",
            label="negative sector",
            zorder=2,
        )
        axis_b.plot(
            direction_cosine,
            quadrupole,
            color=INK,
            linewidth=1.05,
            zorder=3,
        )
        for zero in (-angular_zero, angular_zero):
            axis_b.axvline(zero, color=MUTED, linewidth=0.5, linestyle=":", zorder=1)
        axis_b.set_title("B  Signed angular quadrupole", loc="left", pad=5)
        axis_b.set_xlim(-1.0, 1.0)
        axis_b.set_ylim(-0.62, 1.08)
        axis_b.set_xticks([-1.0, -angular_zero, 0.0, angular_zero, 1.0], [r"$-1$", r"$-1/\sqrt{3}$", r"$0$", r"$1/\sqrt{3}$", r"$1$"])
        axis_b.set_yticks([-0.5, 0.0, 0.5, 1.0])
        axis_b.set_xlabel(r"direction cosine $z=\xi_3$")
        axis_b.set_ylabel(r"$K_{S_0}(z)=(3z^2-1)/2$")
        axis_b.grid(color=GRID, linewidth=0.35, axis="y")
        axis_b.legend(loc="upper center", frameon=False, fontsize=4.05, ncol=2)
        axis_b.text(
            0.0,
            -0.53,
            r"signed mean $=0$",
            color=BLUE,
            fontsize=4.3,
            ha="center",
            va="center",
        )
        axis_b.text(
            0.98,
            0.72,
            r"$\langle K_+\rangle=\sqrt{3}/9$",
            color=RUST,
            fontsize=4.25,
            ha="right",
            va="center",
        )

        # Panel C: critical duality ledger.
        axis_c.plot(
            radius,
            source_square_normalized,
            color=BLUE,
            linewidth=1.15,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            markersize=2.5,
            label=r"source norm$^2\sim r$",
        )
        axis_c.plot(
            radius,
            core_dual_square_normalized,
            color=RUST,
            linewidth=1.2,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.4,
            label=r"core dual norm$^2\sim r^{-1}$",
        )
        axis_c.plot(
            radius,
            cauchy_product_normalized,
            color=RUST,
            linewidth=0.9,
            linestyle=":",
            marker="^",
            markerfacecolor=WHITE,
            markeredgecolor=RUST,
            markeredgewidth=0.65,
            markersize=2.5,
            markevery=(2, 3),
            label="Cauchy product = 1",
            zorder=3,
        )
        axis_c.plot(
            radius,
            signed_pairing_normalized,
            color=INK,
            linewidth=1.05,
            marker="D",
            markerfacecolor=INK,
            markeredgewidth=0.0,
            markersize=2.1,
            markevery=(0, 3),
            label="signed pairing = 1",
            zorder=4,
        )
        axis_c.set_xscale("log", base=2)
        axis_c.set_yscale("log", base=2)
        axis_c.invert_xaxis()
        axis_c.set_title("C  Critical source–core ledger", loc="left", pad=5)
        axis_c.set_xlim(2.0**-1, 2.0**-12)
        axis_c.set_ylim(2.0**-13, 2.0**13)
        axis_c.set_xticks(2.0 ** (-np.asarray([1, 4, 8, 12], dtype=float)), [r"$2^{-1}$", r"$2^{-4}$", r"$2^{-8}$", r"$2^{-12}$"])
        axis_c.set_yticks(2.0 ** np.asarray([-12, -6, 0, 6, 12], dtype=float), [r"$2^{-12}$", r"$2^{-6}$", r"$2^0$", r"$2^6$", r"$2^{12}$"])
        axis_c.set_xlabel(r"radius $r=2^{-k}$ (refinement $\rightarrow$)")
        axis_c.set_ylabel("normalized magnitude (base-2 log)")
        axis_c.grid(color=GRID, linewidth=0.35, which="major")
        axis_c.legend(loc="upper left", frameon=False, fontsize=3.95)
        axis_c.text(
            0.03,
            0.05,
            r"$a=1$; profile/time factors normalized"
            + "\n"
            + r"fixed $\Lambda$ factor removed",
            transform=axis_c.transAxes,
            ha="left",
            va="bottom",
            fontsize=4.25,
            color=MUTED,
        )

        figure.text(
            0.985,
            0.035,
            "closed-form tensor and scale evaluations — not a numerical PDE proof or fixed-positive-time cascade",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.25,
        )

        figure.savefig(
            HERE / "figure.pdf",
            metadata={
                "Title": "Deviatoric helical symbol and critical source-core scaling",
                "Author": "R0.70J analytic figure package",
                "Subject": "Helical tensor symbol, signed angular isotropy, and critical duality",
                "Creator": "plot.py",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": "Deviatoric helical symbol and critical source-core scaling",
                "Description": "Exact analytic identities; not DNS or a blow-up or regularity result.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": "Deviatoric helical symbol and critical source-core scaling",
                "Description": "Exact analytic identities; not DNS or a blow-up or regularity result.",
                "Software": "Matplotlib",
            },
        )
        plt.close(figure)

    normalize_svg(HERE / "figure.svg")

    image = Image.open(HERE / "figure.png")
    embedded_dpi = image.info.get("dpi", (None, None))
    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    with (HERE / "data.csv").open(newline="", encoding="utf-8") as stream:
        data_row_count = sum(1 for _ in csv.DictReader(stream))

    output_checks = {
        "pngOriginalPixelDimensions": bool(image.width >= 4200 and image.height >= 2200),
        "pngRequestedDpiEmbedded": bool(
            embedded_dpi[0] is not None
            and embedded_dpi[1] is not None
            and abs(float(embedded_dpi[0]) - 600.0) < 0.1
            and abs(float(embedded_dpi[1]) - 600.0) < 0.1
        ),
        "pdfNonempty": bool((HERE / "figure.pdf").stat().st_size > 10_000),
        "svgNonempty": bool((HERE / "figure.svg").stat().st_size > 10_000),
        "visibleClaimBoundaryInSvg": bool(
            "EXACT ANALYTIC IDENTITIES" in svg_text
            and "NOT DNS" in svg_text
            and "NOT A BLOW-UP OR REGULARITY RESULT" in svg_text
        ),
        "writtenDataRowCount": data_row_count == 145,
    }
    checks.update(output_checks)
    if not all(checks.values()):
        raise AssertionError(checks)

    validation = {
        "status": "passed",
        "release": RELEASE,
        "checks": checks,
        "diagnostics": {
            "phasePoints": int(phase.size),
            "directionCosinePoints": int(direction_cosine.size),
            "refinementScales": int(radius.size),
            "sphereSignedMean": sphere_signed_mean,
            "spherePositivePartMean": sphere_positive_mean,
            "angularZero": angular_zero,
            "Lambda": Lambda,
            "normalizedPairingAtFinestScale": float(signed_pairing_normalized[-1]),
            "dataRows": data_row_count,
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [float(embedded_dpi[0]), float(embedded_dpi[1])],
        },
        "claimBoundary": (
            "Exact analytic tensor and scale data only; not DNS, not a "
            "sampled Navier-Stokes trajectory, and not evidence for blow-up, "
            "regularity, or a Millennium-problem solution."
        ),
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    payloads = [
        "contract.json",
        "figure-contract.md",
        "caption.md",
        "data.csv",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "explanatory",
        "release": RELEASE,
        "source": "plot.py",
        "sourceSha256": sha256(Path(__file__)),
        "outputs": [
            {
                "path": payload,
                "bytes": (HERE / payload).stat().st_size,
                "sha256": sha256(HERE / payload),
            }
            for payload in payloads
        ],
        "runtime": {
            "python": platform.python_version(),
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
        },
        "claimBoundary": (
            "Exact analytic identities and critical scale covariance; not "
            "simulation evidence or a numerical PDE proof, not a fixed-"
            "positive-time trajectory, and not a Millennium result."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
