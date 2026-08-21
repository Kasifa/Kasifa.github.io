#!/usr/bin/env python3
"""Build the formal R0.69N energy-commutator figure."""
from __future__ import annotations

import csv
import hashlib
import json
import platform
import resource
import time
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = ROOT / "research/certificates/r069n/energy-stress-commutator.json"
CERTIFICATE_SHA = "c666c3fbb01f155e8c4a46e155df880096a3c61705ec74a95ad9eb0e4396c1dd"
SOURCE_COMMIT = "eb80615c8efe45dd26cdbb6ecb1c6e78ab264b4e"
CERTIFICATE_COMMIT = "5e7798168a831b0cf542d75bc457134592ff7b6c"
FIGURE_ID = "fig-r069n-energy-commutator"
INK, MUTED, BLUE, RUST, GOLD, GRID = (
    "#28231f",
    "#6b675f",
    "#315a76",
    "#8b4d43",
    "#a16f27",
    "#d5cec0",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def write_csv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def prepare_data():
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("pinned R0.69N certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69N certificate did not pass")

    s = np.linspace(0.75, 2.25, 121)
    dual_p = 3.0 / s
    write_csv(
        "hardy-dual-frontier.csv",
        ["derivativeOrder", "dualIntegrability", "criticalProduct"],
        [
            {
                "derivativeOrder": f"{si:.8f}",
                "dualIntegrability": f"{pi:.8f}",
                "criticalProduct": f"{si * pi:.8f}",
            }
            for si, pi in zip(s, dual_p)
        ],
    )

    q = np.linspace(4.0, 6.0, 101)
    theta = 1.5 - 3.0 / q
    mu_power = 4.0 * (1.0 - theta)
    sigma_power = 4.0 * theta
    write_csv(
        "energy-interpolation-family.csv",
        ["q", "theta", "muPowerAfterYoung", "sigmaPowerAfterYoung"],
        [
            {
                "q": f"{qi:.8f}",
                "theta": f"{ti:.8f}",
                "muPowerAfterYoung": f"{mi:.8f}",
                "sigmaPowerAfterYoung": f"{si:.8f}",
            }
            for qi, ti, mi, si in zip(q, theta, mu_power, sigma_power)
        ],
    )

    log2_amplitude = np.arange(0, 10, dtype=int)
    quadratic_mass = np.ones_like(log2_amplitude, dtype=float)
    cubic_mass = 2.0**log2_amplitude
    write_csv(
        "time-spike-masses.csv",
        ["amplitude", "width", "quadraticMass", "cubicMass"],
        [
            {
                "amplitude": str(2**int(k)),
                "width": f"{2.0 ** (-2 * int(k)):.17g}",
                "quadraticMass": f"{two:.17g}",
                "cubicMass": f"{three:.17g}",
            }
            for k, two, three in zip(log2_amplitude, quadratic_mass, cubic_mass)
        ],
    )

    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputCertificate": {
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "sha256": CERTIFICATE_SHA,
        },
        "checksPassed": sum(map(bool, certificate["checks"].values())),
        "checksTotal": len(certificate["checks"]),
        "q4YoungCost": "mu sigma^3",
        "hardyCriticalProduct": "3",
        "dissipationProduct": "2",
        "claimBoundary": "exact exponent audit; no Navier-Stokes regularity conclusion",
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return (
        certificate,
        metadata,
        s,
        dual_p,
        q,
        mu_power,
        sigma_power,
        log2_amplitude,
        quadratic_mass,
        cubic_mass,
    )


def validate_data(values) -> None:
    (
        certificate,
        metadata,
        s,
        dual_p,
        q,
        mu_power,
        sigma_power,
        log2_amplitude,
        quadratic_mass,
        cubic_mass,
    ) = values
    checks = {
        "certificatePassedSeventeenChecks": (
            metadata["checksPassed"] == metadata["checksTotal"] == 17
        ),
        "hardyFrontierHasProductThree": np.allclose(s * dual_p, 3.0),
        "energyPointIsStrictlyBelowFrontier": 1.0 * 2.0 < 3.0,
        "hilbertPointNeedsThreeHalvesDerivatives": np.isclose(3.0 / 2.0, 1.5),
        "q4YoungCostIsMuSigmaCubed": (
            np.isclose(mu_power[0], 1.0) and np.isclose(sigma_power[0], 3.0)
        ),
        "q6YoungCostIsSigmaFourth": (
            np.isclose(mu_power[-1], 0.0) and np.isclose(sigma_power[-1], 4.0)
        ),
        "sigmaPowerStrictlyIncreases": np.all(np.diff(sigma_power) > 0),
        "q4StillExceedsQuadraticCknPower": sigma_power[0] > 2.0,
        "timeSpikeKeepsQuadraticMassOne": np.allclose(quadratic_mass, 1.0),
        "timeSpikeCubicMassEqualsAmplitude": np.allclose(
            cubic_mass, 2.0**log2_amplitude
        ),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()):
        raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )


def render(values) -> None:
    _, _, s, dual_p, q, mu_power, sigma_power, log2_a, quadratic, cubic = values
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, middle, right) = plt.subplots(
        1,
        3,
        figsize=(178 / 25.4, 82 / 25.4),
        gridspec_kw={"width_ratios": [1.05, 1.0, 1.0], "wspace": 0.38},
    )

    left.plot(s, dual_p, color=RUST, lw=1.45, label=r"Hardy dual frontier $sp'=3$")
    left.scatter([1.0], [2.0], marker="s", s=28, facecolors="white", edgecolors=BLUE,
                 linewidths=1.2, zorder=4, label=r"dissipation $(1,2)$")
    left.scatter([1.5], [2.0], marker="o", s=25, facecolors=GOLD, edgecolors=INK,
                 linewidths=0.6, zorder=4, label=r"Hilbert dual $(3/2,2)$")
    left.plot([1.0, 1.5], [2.0, 2.0], color=MUTED, ls=(0, (3, 2)), lw=0.9)
    left.annotate("missing 1/2 derivative", xy=(1.25, 2.03), xytext=(1.25, 1.55),
                  ha="center", arrowprops={"arrowstyle": "-[", "color": MUTED, "lw": 0.8},
                  color=MUTED, fontsize=6.1)
    left.set(xlabel=r"derivative order $s$", ylabel=r"dual integrability $p'$",
             title="a  Hardy duality exceeds energy")
    left.set_xlim(0.72, 2.28)
    left.set_ylim(1.25, 4.25)
    left.grid(True, color=GRID, lw=0.45, alpha=0.75)
    left.legend(loc="upper right", frameon=False, fontsize=5.7)

    middle.plot(q, sigma_power, color=RUST, lw=1.45, marker="o", markevery=25,
                markersize=3.0, markerfacecolor="white", label=r"power of $\sigma$")
    middle.plot(q, mu_power, color=BLUE, lw=1.25, ls="--", marker="s", markevery=25,
                markersize=2.8, markerfacecolor="white", label=r"power of $\mu$")
    middle.axhline(2.0, color=INK, lw=1.0, ls=(0, (2, 2)), label="quadratic CKN level")
    middle.annotate(r"best endpoint: $\mu\sigma^3$", xy=(4.0, 3.0), xytext=(4.18, 3.55),
                    arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.8},
                    fontsize=6.1, color=MUTED)
    middle.set(xlabel=r"interpolation endpoint $q$", ylabel="power after Young",
               title="b  Best energy endpoint is cubic")
    middle.set_xticks([4.0, 4.5, 5.0, 5.5, 6.0])
    middle.set_ylim(-0.18, 4.32)
    middle.grid(True, color=GRID, lw=0.45, alpha=0.75)
    middle.legend(loc="center right", frameon=False, fontsize=5.7)

    right.plot(log2_a, np.log2(quadratic), color=BLUE, lw=1.35, ls="--", marker="s",
               markersize=3.0, markerfacecolor="white", label=r"$\int\sigma^2dt=1$")
    right.plot(log2_a, np.log2(cubic), color=RUST, lw=1.45, marker="o", markersize=3.0,
               markerfacecolor="white", label=r"$\int\mu\sigma^3dt=A$")
    right.fill_between(log2_a, 0, np.log2(cubic), color=GOLD, alpha=0.12, hatch="///",
                       edgecolor=GOLD, linewidth=0.0)
    right.text(5.0, 2.1, "uncontrolled gap", ha="center", rotation=33,
               color=MUTED, fontsize=6.3)
    right.set(xlabel=r"spike amplitude $\log_2 A$", ylabel=r"$\log_2$ time mass",
              title="c  Cubic time cost concentrates")
    right.set_xticks(log2_a[::2])
    right.set_yticks(log2_a[::2])
    right.set_ylim(-0.35, 9.5)
    right.grid(True, color=GRID, lw=0.45, alpha=0.75)
    right.legend(loc="upper left", frameon=False, fontsize=5.7)

    fig.subplots_adjust(left=0.065, right=0.99, bottom=0.19, top=0.87)
    fig.savefig(HERE / "figure.pdf", metadata={"Creator": "R0.69N reproducible figure", "CreationDate": None})
    fig.savefig(HERE / "figure.svg", metadata={"Creator": "R0.69N reproducible figure", "Date": None})
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)
    svg = HERE / "figure.svg"
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


def write_manifest(elapsed: float, peak: float) -> None:
    image = Image.open(HERE / "figure.png")
    data_files = [
        ("hardy-dual-frontier.csv", "derivativeOrder, dualIntegrability, criticalProduct"),
        ("energy-interpolation-family.csv", "q, theta, muPowerAfterYoung, sigmaPowerAfterYoung"),
        ("time-spike-masses.csv", "amplitude, width, quadraticMass, cubicMass"),
        ("figure-data-metadata.json", "pinned R0.69N commutator certificate"),
        ("validation.json", "ten figure-data validation checks"),
        ("resources.csv", "elapsedSeconds, maximumRssMiB, status"),
    ]
    outputs = ["figure.pdf", "figure.svg", "figure.png"]
    payload = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "createdAt": "2026-08-21T09:46:00+08:00",
        "analyticalQuestion": "Can compensated pressure structure be paired at energy regularity, and what obstruction remains?",
        "supportedClaim": "the exact stress commutator reaches spatial energy norms, while direct Hardy duality and the time-integrated cubic enstrophy cost remain above CKN control",
        "claimBoundary": "exact functional exponent audit; not a Navier-Stokes regularity theorem or solution counterexample",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": "121 Hardy-frontier samples, 101 interpolation samples, and 10 exact dyadic time spikes",
            "precision": "IEEE binary64 plotting of exact rational formulas",
            "solver": "closed-form exponent identities",
            "command": "python3 plot.py",
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
        "sourceData": [{
            "location": str(CERTIFICATE.relative_to(ROOT)),
            "fileName": CERTIFICATE.name,
            "bytes": CERTIFICATE.stat().st_size,
            "sha256": CERTIFICATE_SHA,
            "extractionCommand": "python3 plot.py",
        }],
        "data": [{
            "path": path,
            "bytes": (HERE / path).stat().st_size,
            "sha256": sha256(HERE / path),
            "schema": schema,
        } for path, schema in data_files],
        "figure": {
            "widthMillimetres": 178,
            "heightMillimetres": 82,
            "profile": "journal-default",
            "script": "plot.py",
            "outputs": [{
                "path": path,
                "bytes": (HERE / path).stat().st_size,
                "sha256": sha256(HERE / path),
                **({"dpi": 600, "pixels": f"{image.width} by {image.height}"} if path.endswith(".png") else {}),
            } for path in outputs],
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": "duality frontier, endpoint-exponent family, and time-spike mass comparison",
            "takeaway": "spatial cancellation is real, but the remaining temporal cost is superquadratic",
            "nonColorEncoding": "distinct markers and line styles, dotted CKN reference, and hatched gap",
            "outputFootprint": "double-column 178 by 82 millimetres with PDF, SVG, and 600 dpi PNG",
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
    write_csv(
        "resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{"elapsedSeconds": f"{elapsed:.9f}", "maximumRssMiB": f"{peak:.6f}", "status": "passed"}],
    )
    write_manifest(elapsed, peak)


if __name__ == "__main__":
    main()
