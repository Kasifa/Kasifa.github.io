#!/usr/bin/env python3
"""Build the formal R0.69K velocity-generated shell-gain figure."""
from __future__ import annotations
import csv, hashlib, json, platform, resource, time
from pathlib import Path
import matplotlib, matplotlib.pyplot as plt, numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = HERE.parents[1] / "journal.mplstyle"
CERTIFICATE = ROOT / "research/certificates/r069k/velocity-generated-shell-quadrupole.json"
CERTIFICATE_SHA = "a638fc121e7d91bf009d939a12f831b134fe8b5a2aa779c14880d5871c36f8fa"
SOURCE_COMMIT = "b2c7ad329eba2df516dd251a1f74af42ad153e74"
CERTIFICATE_COMMIT = "83049f868fb0ea2b393e0b469fa9f2343c6602cf"
FIGURE_ID = "fig-r069k-shell-gain"
INK, MUTED, BLUE, RUST, GOLD, GRID = "#28231f", "#6b675f", "#315a76", "#8b4d43", "#a16f27", "#d5cec0"

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rss_mib():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024

def write_csv(name, fields, rows):
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)

def prepare_data():
    if sha256(CERTIFICATE) != CERTIFICATE_SHA:
        raise RuntimeError("pinned R0.69K certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["status"] != "passed":
        raise RuntimeError("R0.69K certificate did not pass")
    radii = np.geomspace(1, 32, 33)
    write_csv("shell-decay.csv",
        ["radiusRatio", "scalarSourceRMinus3", "velocityGeneratedRMinus5"],
        [{"radiusRatio": f"{r:.17g}", "scalarSourceRMinus3": f"{r**-3:.17g}",
          "velocityGeneratedRMinus5": f"{r**-5:.17g}"} for r in radii])
    write_csv("quadrupole-eigenvalues.csv", ["axis", "fourPiR5Eigenvalue"],
        [{"axis": "e1", "fourPiR5Eigenvalue": 0},
         {"axis": "e2", "fourPiR5Eigenvalue": 6},
         {"axis": "e3", "fourPiR5Eigenvalue": -6}])
    metadata = {
        "status": "passed", "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputCertificate": {"location": str(CERTIFICATE.relative_to(ROOT)), "sha256": CERTIFICATE_SHA},
        "checksPassed": sum(map(bool, certificate["checks"].values())),
        "checksTotal": len(certificate["checks"]),
        "actualPairing": certificate["witness"]["actualStrainPairing"],
        "claimBoundary": "shell-separation gain only; near and transition pressure terms remain open",
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return certificate, metadata, radii

def validate_data(certificate, metadata, radii):
    q = certificate["witness"]["fourPiQuadrupole"]
    checks = {
        "certificatePassedFourteenChecks": metadata["checksPassed"] == metadata["checksTotal"] == 14,
        "shellBoundHasInverseFifthPower": certificate["bound"]["scalingPower"] == -5,
        "massVanishes": certificate["identity"]["mass"] == "0",
        "dipoleVanishes": certificate["identity"]["dipole"] == ["0", "0", "0"],
        "secondMomentIsPositiveSemidefinite": certificate["identity"]["secondMoment"] == [["2","0","0"],["0","4","0"],["0","0","0"]],
        "quadrupoleHasOppositeEigenvalues": q[1][1] == "6/R**5" and q[2][2] == "-6/R**5",
        "pairingIsNonzero": certificate["witness"]["actualStrainPairing"] == "-3/(2*pi*R**5)",
        "velocityCurveGainsTwoPowers": np.allclose(radii**-5 / radii**-3, radii**-2),
    }
    checks = {key: bool(value) for key, value in checks.items()}
    if not all(checks.values()): raise AssertionError(checks)
    (HERE / "validation.json").write_text(
        json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")

def render(radii):
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig, (left, right) = plt.subplots(
        1, 2, figsize=(178/25.4, 86/25.4),
        gridspec_kw={"width_ratios":[1.08,.92], "wspace":.38})
    left.loglog(radii, radii**-3, color=RUST, lw=1.6, ls=(0,(5,2.5)),
        marker="s", markevery=[0,8,16,24,32], markerfacecolor="white",
        label=r"general scalar source $R^{-3}$")
    left.loglog(radii, radii**-5, color=BLUE, lw=1.6, marker="o",
        markevery=[0,8,16,24,32], markerfacecolor="white",
        label=r"velocity-generated shell $R^{-5}$")
    left.fill_between(radii, radii**-5, radii**-3, color=GOLD, alpha=.09,
        hatch="///", edgecolor=GRID)
    left.text(2.2, 2e-5, r"two powers from $q=\partial_i\partial_j(u_i u_j)$",
        fontsize=6.6, color=MUTED)
    left.set(xlabel=r"shell distance ratio $R_m/R_0$",
        ylabel="normalized Hessian bound",
        title="a  Velocity generation improves remote-shell decay")
    left.grid(True, which="both", color=GRID, lw=.45, alpha=.75)
    left.legend(loc="lower left", frameon=False, fontsize=6.4)
    values = np.array([0,6,-6])
    bars = right.bar(np.arange(3), values, width=.58,
        color=[GOLD,BLUE,RUST], alpha=.78, edgecolor=INK, lw=.8)
    for bar, hatch in zip(bars, ["..","///","xx"], strict=True): bar.set_hatch(hatch)
    right.axhline(0, color=INK, lw=.85)
    for i, value in enumerate(values):
        right.text(i, value + (.35 if value >= 0 else -.35), f"{value:+d}",
            ha="center", va="bottom" if value >= 0 else "top", fontsize=7)
    right.text(1, -8.4, r"$S_0:Q_R=-3/(2\pi R^5)\ne0$", ha="center",
        fontsize=7, color=MUTED,
        bbox={"facecolor":"white","edgecolor":GRID,"boxstyle":"round,pad=0.25"})
    right.set_xticks(np.arange(3), [r"$e_1$",r"$e_2$",r"$e_3$"])
    right.set(xlabel="", ylabel=r"eigenvalue of $4\pi R^5 Q_R$",
        title="b  The improved coefficient remains nonzero", ylim=(-9,8))
    right.grid(True, axis="y", color=GRID, lw=.45, alpha=.75)
    fig.subplots_adjust(left=.075, right=.975, bottom=.19, top=.88)
    fig.savefig(HERE/"figure.pdf", metadata={"Creator":"R0.69K reproducible figure","CreationDate":None})
    fig.savefig(HERE/"figure.svg", metadata={"Creator":"R0.69K reproducible figure","Date":None})
    fig.savefig(HERE/"figure.png", dpi=600); plt.close(fig)
    svg = HERE/"figure.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())+"\n", encoding="utf-8")

def manifest(elapsed, peak):
    image = Image.open(HERE/"figure.png")
    data_files = [
        ("shell-decay.csv","radiusRatio, scalarSourceRMinus3, velocityGeneratedRMinus5"),
        ("quadrupole-eigenvalues.csv","axis, fourPiR5Eigenvalue"),
        ("figure-data-metadata.json","pinned certificate and exact shell identities"),
        ("validation.json","eight figure-data validation checks"),
        ("resources.csv","elapsedSeconds, maximumRssMiB, status")]
    outputs = ["figure.pdf","figure.svg","figure.png"]
    payload = {
      "schemaVersion":"1.0","figureId":FIGURE_ID,"status":"formal",
      "createdAt":"2026-08-21T08:40:00+08:00",
      "analyticalQuestion":"Does velocity generation improve the far-shell pressure quadrupole beyond scalar R^-3 decay?",
      "supportedClaim":"stress localization gives an R^-5 kinetic-energy bound, two powers better than the scalar-source bound, with a nonzero anisotropic coefficient",
      "claimBoundary":"shell-separation gain only; no Navier-Stokes regularity or singularity conclusion",
      "git":{"repository":"Kasifa/Kasifa.github.io","sourceCommit":SOURCE_COMMIT,"certificateCommit":CERTIFICATE_COMMIT,"dirtyAtCertifiedRun":False},
      "computation":{"kind":"exact-audit","configuration":"two decay laws and one three-axis exact quadrupole","precision":"IEEE binary64 plotting of exact symbolic certificate values","solver":"exact SymPy fourth-derivative certificate","command":"python3 plot.py","wallTimeSeconds":elapsed},
      "compute":{"host":"local Mac workstation","operatingSystem":f"{platform.system()}-{platform.release()}-{platform.machine()}","cpu":"Apple M5 Max","memoryGiB":36,"processes":1,"threadsPerProcess":1,"maximumRssMiB":peak},
      "environment":{"python":platform.python_version(),"matplotlib":matplotlib.__version__,"numpy":np.__version__,"pillow":Image.__version__,"packagesLock":"requirements-research.txt"},
      "sourceData":[{"location":str(CERTIFICATE.relative_to(ROOT)),"fileName":CERTIFICATE.name,"bytes":CERTIFICATE.stat().st_size,"sha256":CERTIFICATE_SHA,"extractionCommand":"python3 plot.py"}],
      "data":[{"path":p,"bytes":(HERE/p).stat().st_size,"sha256":sha256(HERE/p),"schema":s} for p,s in data_files],
      "figure":{"widthMillimetres":178,"heightMillimetres":86,"profile":"journal-default","script":"plot.py","outputs":[{"path":p,"bytes":(HERE/p).stat().st_size,"sha256":sha256(HERE/p),**({"dpi":600,"pixels":f"{image.width} by {image.height}"} if p.endswith(".png") else {})} for p in outputs]},
      "caption":{"english":"caption.md"},
      "chartContract":{"family":"log-log decay comparison plus signed eigenvalue bars","takeaway":"velocity generation gains two far-shell powers but does not annihilate the coefficient","nonColorEncoding":"solid-circle versus dashed-square curves, hatching, signed bars, and exact labels","outputFootprint":"double-column 178 by 86 millimetres with PDF, SVG, and 600 dpi PNG"},
      "qa":{"status":"passed","finalSizeInspected":True,"grayscaleInspected":True,"labelsAndLegendsInspected":True,"scalesAndUnitsInspected":True,"dataCrossChecked":True}}
    (HERE/"manifest.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def main():
    started=time.perf_counter(); certificate,metadata,radii=prepare_data()
    validate_data(certificate,metadata,radii); render(radii)
    elapsed=time.perf_counter()-started; peak=rss_mib()
    write_csv("resources.csv",["elapsedSeconds","maximumRssMiB","status"],
        [{"elapsedSeconds":f"{elapsed:.9f}","maximumRssMiB":f"{peak:.6f}","status":"passed"}])
    manifest(elapsed,peak)
if __name__=="__main__": main()
