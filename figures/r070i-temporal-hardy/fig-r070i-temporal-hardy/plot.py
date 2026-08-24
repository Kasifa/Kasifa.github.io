#!/usr/bin/env python3
"""Render the journal-style analytic figure for R0.70I.

Every plotted value evaluates a displayed closed formula.  The figure is a
finite-chain envelope, a scalar Hardy diagnostic, and an initial-boundary
scale ledger.  It is not a simulated NSE trajectory and not a
fixed-positive-top counterexample.
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
FIGURE_ID = "fig-r070i-temporal-hardy"
RELEASE = "R0.70I"

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


def truncated_hardy_integral(alpha: float, epsilon: np.ndarray) -> np.ndarray:
    """Return integral_epsilon^1 s^(-1/2-2 alpha) ds exactly."""

    endpoint_exponent = 0.5 - 2.0 * alpha
    if abs(endpoint_exponent) < 1.0e-14:
        return np.log(1.0 / epsilon)
    return (1.0 - epsilon**endpoint_exponent) / endpoint_exponent


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))

    # Panel A: normalized finite-chain temporal envelope.
    rho = 0.25
    chain_depth = 6
    r_finest = rho**chain_depth
    breakpoint = r_finest**2
    cap = r_finest**-1
    time_exponent = np.arange(0, 33, dtype=int)
    backward_time = 2.0 ** (-time_exponent.astype(float))
    hardy_reference = backward_time**-0.5
    finite_chain_envelope = np.minimum(cap, hardy_reference)

    # Panel B: scalar endpoint test f(s)=s^(-alpha).
    cutoff_depth = np.arange(2, 33, dtype=int)
    epsilon = 2.0 ** (-cutoff_depth.astype(float))
    alphas = np.asarray([3.0 / 20.0, 1.0 / 4.0, 7.0 / 20.0])
    alpha_roles = ("subcritical", "critical", "supercritical")
    integrand_powers = 0.5 + 2.0 * alphas
    hardy_integrals = np.vstack(
        [truncated_hardy_integral(alpha, epsilon) for alpha in alphas]
    )

    # Panel C: fixed-amplitude initial-boundary scale covariance.
    amplitude = 1.0 / 8.0
    refinement_index = np.arange(1, 13, dtype=int)
    radius = 2.0 ** (-refinement_index.astype(float))
    energy = amplitude**2 * radius
    integrated_dissipation = amplitude**2 * radius
    target_scale_factor = amplitude**4 / radius
    energy_dual = radius**-3 * energy**2

    rows: list[tuple[object, ...]] = []
    for index, s, reference, envelope in zip(
        time_exponent,
        backward_time,
        hardy_reference,
        finite_chain_envelope,
        strict=True,
    ):
        rows.append(
            (
                "A",
                "finite-chain-envelope",
                int(index),
                s,
                reference,
                envelope,
                cap,
                r_finest,
                breakpoint,
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

    for alpha_index, (alpha, role, power) in enumerate(
        zip(alphas, alpha_roles, integrand_powers, strict=True)
    ):
        for depth_index, eps, integral in zip(
            cutoff_depth,
            epsilon,
            hardy_integrals[alpha_index],
            strict=True,
        ):
            rows.append(
                (
                    "B",
                    role,
                    int(depth_index),
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    eps,
                    alpha,
                    power,
                    integral,
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

    for index, r_value, e_value, d_value, t_value, q_value in zip(
        refinement_index,
        radius,
        energy,
        integrated_dissipation,
        target_scale_factor,
        energy_dual,
        strict=True,
    ):
        rows.append(
            (
                "C",
                "initial-boundary-scale-ledger",
                int(index),
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
                r_value,
                amplitude,
                e_value,
                d_value,
                t_value,
                q_value,
                t_value / q_value,
                q_value / t_value,
            )
        )

    write_csv(
        HERE / "data.csv",
        [
            "panel",
            "row_role",
            "scale_index_or_cutoff_depth",
            "backward_time_s",
            "hardy_reference_s_minus_one_half",
            "finite_chain_envelope_G_K",
            "finest_scale_cap_r_K_minus_1",
            "finest_radius_r_K",
            "breakpoint_r_K_squared",
            "epsilon",
            "alpha",
            "integrand_power_one_half_plus_two_alpha",
            "truncated_hardy_integral",
            "radius_r",
            "fixed_amplitude_a",
            "energy_E_a_squared_r",
            "integrated_dissipation_D_a_squared_r",
            "target_functional_scale_factor_T_n_a_fourth_r_minus_1",
            "dual_Q_r_minus_3_E_squared",
            "T_n_scale_factor_over_Q_scale_factor",
            "Q_scale_factor_over_T_n_scale_factor",
        ],
        rows,
    )

    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "finiteChainParametersExact": bool(
            rho == 0.25
            and chain_depth == 6
            and r_finest == 2.0**-12
            and breakpoint == 2.0**-24
            and cap == 2.0**12
        ),
        "finiteChainEnvelopeExact": bool(
            np.array_equal(
                finite_chain_envelope,
                np.minimum(r_finest**-1, backward_time**-0.5),
            )
        ),
        "hardyRegionExact": bool(
            np.array_equal(
                finite_chain_envelope[backward_time >= breakpoint],
                hardy_reference[backward_time >= breakpoint],
            )
        ),
        "finestScaleSaturationExact": bool(
            np.array_equal(
                finite_chain_envelope[backward_time <= breakpoint],
                np.full(np.sum(backward_time <= breakpoint), cap),
            )
        ),
        "alphaThresholdPowersExact": bool(
            np.array_equal(integrand_powers, np.asarray([0.8, 1.0, 1.2]))
        ),
        "criticalIntegralIsLogarithmic": bool(
            np.allclose(
                hardy_integrals[1],
                np.log(1.0 / epsilon),
                rtol=1.0e-14,
                atol=1.0e-14,
            )
        ),
        "subcriticalIntegralBoundedByLimit": bool(
            np.all(hardy_integrals[0] < 5.0)
            and np.all(np.diff(hardy_integrals[0]) > 0.0)
        ),
        "criticalAndSupercriticalGrowth": bool(
            np.all(np.diff(hardy_integrals[1]) > 0.0)
            and np.all(np.diff(hardy_integrals[2]) > 0.0)
            and hardy_integrals[2, -1] > hardy_integrals[1, -1]
        ),
        "energyAndDissipationScalingExact": bool(
            np.array_equal(energy, integrated_dissipation)
            and np.array_equal(energy[1:] / energy[:-1], np.full(11, 0.5))
        ),
        "inverseScaleQuantitiesExact": bool(
            np.array_equal(target_scale_factor[1:] / target_scale_factor[:-1], np.full(11, 2.0))
            and np.array_equal(energy_dual[1:] / energy_dual[:-1], np.full(11, 2.0))
            and np.array_equal(energy_dual, amplitude**4 / radius)
        ),
        "normalizedTargetAndDualScaleFactorsCoincide": bool(
            np.array_equal(target_scale_factor, energy_dual)
            and np.array_equal(target_scale_factor / energy_dual, np.ones(12))
        ),
        "dataRowCount": len(rows) == 138,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 94 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.080,
            right=0.985,
            bottom=0.205,
            top=0.715,
            width_ratios=(1.03, 1.08, 1.03),
            wspace=0.35,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Temporal Hardy envelope and an initial-boundary scale ledger",
            x=0.045,
            y=0.966,
            ha="left",
            fontsize=8.3,
            color=INK,
        )
        figure.text(
            0.045,
            0.912,
            r"finite geometric chain  ·  exact scalar endpoint  ·  fixed-amplitude NSE scale covariance",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        figure.text(
            0.045,
            0.840,
            "CLOSED-FORM ANALYTIC SCALING  /  NOT A SIMULATED NSE TRAJECTORY  /  NOT A FIXED-POSITIVE-TOP COUNTEREXAMPLE",
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

        # Panel A: the s^(-1/2) regime and the finite finest-scale cap.
        axis_a.axvspan(
            backward_time.min(),
            breakpoint,
            color=PALE_RUST,
            alpha=0.75,
            linewidth=0.0,
            zorder=0,
        )
        axis_a.axvspan(
            breakpoint,
            backward_time.max(),
            color=PALE_BLUE,
            alpha=0.65,
            linewidth=0.0,
            zorder=0,
        )
        axis_a.plot(
            backward_time,
            hardy_reference,
            color=BLUE,
            linewidth=1.0,
            linestyle="--",
            label=r"Hardy reference $s^{-1/2}$",
            zorder=2,
        )
        axis_a.plot(
            backward_time,
            finite_chain_envelope,
            color=RUST,
            linewidth=1.35,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.3,
            markevery=4,
            label=r"finite envelope $G_K(s)$",
            zorder=3,
        )
        axis_a.axhline(
            cap,
            color=INK,
            linewidth=0.75,
            linestyle=":",
            label=r"cap $r_K^{-1}=2^{12}$",
            zorder=2,
        )
        axis_a.axvline(
            breakpoint,
            color=MUTED,
            linewidth=0.55,
            linestyle=":",
            zorder=1,
        )
        axis_a.set_xscale("log", base=2)
        axis_a.set_yscale("log", base=2)
        axis_a.invert_xaxis()
        axis_a.set_title("A  Finite-chain temporal kernel", loc="left", pad=5)
        axis_a.set_xlim(1.0, 2.0**-32)
        axis_a.set_ylim(2.0**-0.5, 2.0**13)
        axis_a.set_xticks(
            2.0 ** (-np.asarray([0, 8, 16, 24, 32], dtype=float)),
            [r"$2^0$", r"$2^{-8}$", r"$2^{-16}$", r"$2^{-24}$", r"$2^{-32}$"],
        )
        axis_a.set_yticks(
            2.0 ** np.asarray([0, 4, 8, 12], dtype=float),
            [r"$2^0$", r"$2^4$", r"$2^8$", r"$2^{12}$"],
        )
        axis_a.set_xlabel(r"backward time $s=t_0-t$ (base 2)")
        axis_a.set_ylabel(r"normalized envelope $G_K(s)$")
        axis_a.grid(color=GRID, linewidth=0.35, which="major")
        axis_a.legend(loc="upper left", frameon=False, fontsize=4.15)
        axis_a.text(
            2.0**-7,
            2.0**8.25,
            r"$s^{-1/2}$ region",
            color=BLUE,
            fontsize=4.55,
            ha="center",
        )
        axis_a.text(
            2.0**-28,
            2.0**10.9,
            "finest-scale\nsaturation",
            color=RUST,
            fontsize=4.45,
            ha="center",
            va="top",
        )
        axis_a.annotate(
            r"$s=r_K^2$",
            xy=(breakpoint, cap),
            xytext=(2.0**-18.5, 2.0**11.0),
            fontsize=4.4,
            color=MUTED,
            arrowprops={
                "arrowstyle": "->",
                "color": MUTED,
                "linewidth": 0.5,
                "shrinkA": 1,
                "shrinkB": 2,
            },
        )

        # Panel B: exact scalar Hardy endpoint.
        styles = (
            {
                "color": BLUE,
                "linestyle": "--",
                "marker": "o",
                "markerfacecolor": WHITE,
                "markeredgecolor": BLUE,
                "label": r"$\alpha=3/20$  bounded",
            },
            {
                "color": INK,
                "linestyle": ":",
                "marker": "^",
                "markerfacecolor": WHITE,
                "markeredgecolor": INK,
                "label": r"$\alpha=1/4$  logarithmic",
            },
            {
                "color": RUST,
                "linestyle": "-",
                "marker": "s",
                "markerfacecolor": RUST,
                "markeredgecolor": RUST,
                "label": r"$\alpha=7/20$  power growth",
            },
        )
        for values, style in zip(hardy_integrals, styles, strict=True):
            axis_b.plot(
                cutoff_depth,
                values,
                linewidth=1.15,
                markeredgewidth=0.65,
                markersize=2.5,
                markevery=5,
                **style,
            )
        axis_b.set_yscale("log", base=2)
        axis_b.set_title(r"B  Hardy endpoint $\alpha=1/4$", loc="left", pad=5)
        axis_b.set_xlim(2, 32)
        axis_b.set_ylim(2.0**-1, 2.0**9.5)
        axis_b.set_xticks([2, 8, 16, 24, 32])
        axis_b.set_yticks(
            2.0 ** np.asarray([0, 2, 4, 6, 8], dtype=float),
            [r"$1$", r"$2^2$", r"$2^4$", r"$2^6$", r"$2^8$"],
        )
        axis_b.set_xlabel(r"cutoff depth $J$ ($\varepsilon=2^{-J}$)")
        axis_b.set_ylabel(r"$H_\alpha(2^{-J})$ (base-2 log)")
        axis_b.grid(color=GRID, linewidth=0.35, which="major")
        axis_b.legend(loc="upper left", frameon=False, fontsize=4.25)
        axis_b.text(
            0.98,
            0.05,
            r"integrand power $p=\frac{1}{2}+2\alpha$" + "\n" + r"finite iff $p<1$",
            transform=axis_b.transAxes,
            ha="right",
            va="bottom",
            fontsize=4.45,
            color=MUTED,
        )

        # Panel C: fixed-amplitude initial-boundary scaling only.
        axis_c.plot(
            radius,
            energy,
            color=BLUE,
            linewidth=1.1,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.7,
            markersize=2.7,
            label=r"$E=D=a^2r$",
        )
        axis_c.plot(
            radius,
            target_scale_factor,
            color=RUST,
            linewidth=1.25,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.6,
            markevery=(0, 2),
            label=r"target scale $\mathcal{T}_n\sim a^4r^{-1}$",
        )
        axis_c.plot(
            radius,
            energy_dual,
            color=RUST,
            linewidth=1.0,
            linestyle=":",
            marker="^",
            markerfacecolor=WHITE,
            markeredgecolor=RUST,
            markeredgewidth=0.7,
            markersize=2.7,
            markevery=(1, 2),
            label=r"dual scale $r^{-3}E^2=a^4r^{-1}$",
        )
        axis_c.set_xscale("log", base=2)
        axis_c.set_yscale("log", base=2)
        axis_c.invert_xaxis()
        axis_c.set_title("C  Initial-boundary scale ledger", loc="left", pad=5)
        axis_c.set_xlim(2.0**-1, 2.0**-12)
        axis_c.set_ylim(2.0**-19, 2.0**4)
        axis_c.set_xticks(
            2.0 ** (-np.asarray([1, 4, 8, 12], dtype=float)),
            [r"$2^{-1}$", r"$2^{-4}$", r"$2^{-8}$", r"$2^{-12}$"],
        )
        axis_c.set_yticks(
            2.0 ** np.asarray([-18, -12, -6, 0], dtype=float),
            [r"$2^{-18}$", r"$2^{-12}$", r"$2^{-6}$", r"$2^0$"],
        )
        axis_c.set_xlabel(r"radius $r=2^{-k}$ (refinement $\rightarrow$)")
        axis_c.set_ylabel("normalized magnitude (base-2 log)")
        axis_c.grid(color=GRID, linewidth=0.35, which="major")
        axis_c.legend(loc="upper left", frameon=False, fontsize=4.15)
        axis_c.text(
            0.97,
            0.05,
            r"fixed $a=2^{-3}$" + "\nunit profile constants",
            transform=axis_c.transAxes,
            ha="right",
            va="bottom",
            fontsize=4.45,
            color=MUTED,
        )
        axis_c.text(
            2.0**-10.5,
            2.0**1.4,
            "same normalized\n" + r"$r^{-1}$ scale factor",
            ha="center",
            va="bottom",
            fontsize=4.45,
            color=RUST,
        )

        figure.text(
            0.985,
            0.035,
            "normalized closed-form envelopes and scale ledgers — not simulation evidence or a numerical PDE proof",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.35,
        )

        figure.savefig(
            HERE / "figure.pdf",
            metadata={
                "Title": "Temporal Hardy envelope and an initial-boundary scale ledger",
                "Author": "R0.70I analytic figure package",
                "Subject": "Finite-chain temporal kernel, Hardy endpoint, and initial-boundary scaling",
                "Creator": "plot.py",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": "Temporal Hardy envelope and an initial-boundary scale ledger",
                "Description": "Closed-form analytic scaling; not a simulated NSE trajectory or a fixed-positive-top counterexample.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": "Temporal Hardy envelope and an initial-boundary scale ledger",
                "Description": "Closed-form analytic scaling; not a simulated NSE trajectory or a fixed-positive-top counterexample.",
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
            "CLOSED-FORM ANALYTIC SCALING" in svg_text
            and "NOT A SIMULATED NSE TRAJECTORY" in svg_text
            and "NOT A FIXED-POSITIVE-TOP COUNTEREXAMPLE" in svg_text
        ),
        "writtenDataRowCount": data_row_count == 138,
    }
    checks.update(output_checks)
    if not all(checks.values()):
        raise AssertionError(checks)

    validation = {
        "status": "passed",
        "release": RELEASE,
        "checks": checks,
        "diagnostics": {
            "rho": rho,
            "chainDepthK": chain_depth,
            "rK": r_finest,
            "breakpoint_rK_squared": breakpoint,
            "finiteChainCap": cap,
            "alphaThreshold": 0.25,
            "integrandPowers": [float(value) for value in integrand_powers],
            "subcriticalIntegralAtJ32": float(hardy_integrals[0, -1]),
            "criticalIntegralAtJ32": float(hardy_integrals[1, -1]),
            "supercriticalIntegralAtJ32": float(hardy_integrals[2, -1]),
            "fixedAmplitude": amplitude,
            "normalizedTargetScaleFactorOverDualScaleFactor": float(
                target_scale_factor[0] / energy_dual[0]
            ),
            "dataRows": data_row_count,
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [
                float(embedded_dpi[0]),
                float(embedded_dpi[1]),
            ],
        },
        "claimBoundary": (
            "Closed-form analytic scaling only; not simulation evidence or a "
            "numerical PDE proof. It is not a simulated NSE trajectory and not "
            "a fixed-positive-top counterexample."
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
                "path": name,
                "bytes": (HERE / name).stat().st_size,
                "sha256": sha256(HERE / name),
            }
            for name in payloads
        ],
        "png": {
            "pixels": [image.width, image.height],
            "requestedDpi": 600,
            "embeddedDpi": [
                float(embedded_dpi[0]),
                float(embedded_dpi[1]),
            ],
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "claimBoundary": (
            "Closed-form R0.70I temporal-envelope and initial-boundary scaling "
            "diagnostics; not simulation evidence or a numerical PDE proof; not "
            "a simulated NSE trajectory or a fixed-positive-top counterexample."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
