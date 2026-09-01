#!/usr/bin/env python3
"""Generate the deterministic R0.74B three-panel journal package."""
from __future__ import annotations
import csv, hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from PIL import Image, ImageOps
import pypdfium2 as pdfium

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
COMMIT="c873dbcdda7aab46cfda932277b717f32d1bbf53"
CERT_SHA="7c0edc9271b2bc857046e3695c0fcb7b86ab9171991512708d0b0343fe1d3638"
PROOF="research/r074b_buffered_tail_closure.md"
CERT="research/r074b_buffered_tail_certificate.json"
NAVY="#174A7E"; BLUE="#DCEAF5"; GREY="#555555"; LIGHT="#F4F5F6"
RED="#C44E35"; AMBER="#C99522"; GREEN="#3A7D44"
FROZEN_UTC="2026-09-01T00:00:00+00:00"

def sha(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()
def canonical(x): return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
def box(ax,x,y,w,h,text,edge=NAVY,face="white",ls="-",fs=7.0,lw=.9):
    p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.012,rounding_size=0.02",
        edgecolor=edge,facecolor=face,linewidth=lw,linestyle=ls)
    ax.add_patch(p); ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,color="#20242A")
def arrow(ax,a,b,color=NAVY,ls="-"):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=8,linewidth=.8,color=color,linestyle=ls))
def tag(ax,x,y,text,color,ls="-"):
    ax.text(x,y,text,ha="left",va="center",fontsize=6.2,fontweight="bold",color=color,
        bbox=dict(boxstyle="round,pad=.18",fc="white",ec=color,lw=.7,ls=ls))

def rows():
    out=[]
    for m in range(1,7):
        out.append(["A","shell",m,2**m,2**(m+1),2**m-1/8,2**(m+1)+1/8,
                    m,m-1,m-2,str(m<=2).lower(),4**(m-1)/32,
                    "analytic geometry"])
    out += [
        ["B","clock","std","","","","","","","","","", "kappa=1; factor=1+nu"],
        ["B","clock","nu","","","","","","","","","", "kappa=nu; factor=2 nu^(2/3)"],
        ["B","composition","P","","","","","","","","","", "P degree 3"],
        ["B","composition","P^(2/3)","","","","","","","","","", "degree 2"],
        ["B","composition","P term","","","","","","","","","", "degree 3"],
        ["C","Lambda","outer","","","","","","","","","", "1/2 Lambda_(2R)"],
        ["C","Lambda","core","","","","","","","","","", "1/(16 R^3)"],
        ["C","gauge-volume","R power","","","","","","","","","", "-2+3=+1; NSE scale 0"],
        ["C","normalization","G_u/G_p","","","","","","","","","", "factor 4"],
        ["C","shear","quadratic","","","","","","","","","", "N^0"],
        ["C","shear","cubic-only","","","","","","","","","", "N^-2"],
    ]
    return out

def draw():
    plt.rcParams.update({"font.family":"DejaVu Sans","pdf.fonttype":42,"svg.fonttype":"none","svg.hashsalt":"r074b-c873dbcd"})
    fig=plt.figure(figsize=(180/25.4,78/25.4),dpi=600,facecolor="white")
    gs=fig.add_gridspec(1,3,left=.025,right=.985,bottom=.11,top=.91,wspace=.075)
    axes=[fig.add_subplot(gs[0,i]) for i in range(3)]
    for i,ax in enumerate(axes):
        ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
        ax.text(.0,1.035,chr(65+i),fontsize=10,fontweight="bold",va="top")
    # A
    ax=axes[0]; ax.text(.08,1.02,"Exact doubled-radius shell map",fontsize=8.2,fontweight="bold",va="top")
    tag(ax,.67,.96,"ANALYTIC",NAVY)
    for k,(lab,y,c) in enumerate([("$A_{m-1}(R)$",.73,"#E8EEF4"),("$A_m(R)$",.64,BLUE),("$A_{m+1}(R)$",.55,"#E8EEF4")]):
        ax.add_patch(Rectangle((.13,y),.39,.062,fc=c,ec=NAVY,lw=.7)); ax.text(.325,y+.031,lab,ha="center",va="center",fontsize=6.8)
        j=["$A_{m-2}(2R)$","$A_{m-1}(2R)$","$A_m(2R)$"][k]
        ax.add_patch(Rectangle((.62,y),.30,.062,fc="white",ec=NAVY,lw=.7)); ax.text(.77,y+.031,j,ha="center",va="center",fontsize=6.5)
        arrow(ax,(.52,y+.031),(.62,y+.031))
    ax.text(.52,.50,"outward keeps $\\gamma_m$",ha="center",fontsize=6.3,color=NAVY)
    ax.add_patch(Rectangle((.08,.29),.84,.14,fc="#F3E9D2",ec=AMBER,lw=.8,hatch="///"))
    ax.text(.50,.36,"CORE $B_{4R}$: inner collars $m=1,2$\npaid by $\\mathcal{E}(z_0,8R)^{3/2}$",ha="center",va="center",fontsize=6.8)
    ax.text(.08,.21,"same $R$:  $\\gamma_m\\not\\lesssim\\gamma_{m+1}$",fontsize=6.4,color=RED)
    ax.text(.08,.15,"double $R$: $A_k(R)=A_{k-1}(2R)$  ✓",fontsize=6.5,color=GREEN)
    tag(ax,.08,.07,"FINITE: indices + ×4",GREY,"--")
    # B
    ax=axes[1]; ax.text(.08,1.02,"Clock / Hölder payment flow",fontsize=8.2,fontweight="bold",va="top"); tag(ax,.69,.96,"ANALYTIC",NAVY)
    box(ax,.05,.76,.40,.12,"std: $\\kappa=1$\n$(1+\\nu)$",face=BLUE)
    box(ax,.55,.76,.40,.12,"visc: $\\kappa=\\nu$\n$2\\nu^{2/3}$",face=BLUE)
    box(ax,.15,.55,.70,.12,"suitable local energy\n$R^{-3}S_2$  +  direct flux",face="white")
    arrow(ax,(.25,.76),(.35,.67)); arrow(ax,(.75,.76),(.65,.67))
    box(ax,.05,.34,.42,.12,"weighted Hölder\n$R^{-3}S_2\\lesssim P^{2/3}$",face="#EEF6EE",edge=GREEN)
    box(ax,.55,.34,.40,.12,"cubic / pressure\n$\\lesssim P$",face="#FFF6E5",edge=AMBER)
    arrow(ax,(.35,.55),(.26,.46)); arrow(ax,(.65,.55),(.75,.46))
    box(ax,.12,.14,.76,.13,"$\\mathcal{U}_{ext}^{\\infty}+\\mathcal{D}_{ext}$\n$\\leq C(P^{2/3}+P)$",face=BLUE)
    arrow(ax,(.26,.34),(.38,.27)); arrow(ax,(.75,.34),(.62,.27))
    ax.text(.50,.08,"$P=\\mathcal{E}(8R)^{3/2}+\\mathcal{A}_{ext}(2R)$",ha="center",fontsize=6.6)
    tag(ax,.04,.02,"FINITE: 67/67",GREY,"--"); tag(ax,.65,.02,"OPEN: remove +P?",AMBER)
    # C
    ax=axes[2]; ax.text(.08,1.02,"Pressure inheritance and closure",fontsize=7.8,fontweight="bold",va="top"); tag(ax,.67,.96,"ANALYTIC",NAVY)
    box(ax,.02,.74,.28,.14,"$\\Lambda_R$\ncore $1/16$\nouter $1/2$",fs=6.0)
    box(ax,.36,.74,.28,.14,"$\\mathcal{G}_u(R)$\ncore + $2R$",fs=6.0)
    box(ax,.70,.74,.28,.14,"$\\mathcal{G}_p(R)$\nCZ + gauge\n$+H_u$",fs=6.0)
    box(ax,.14,.55,.72,.11,"gauge volume: $R^{-2}\\times R^3=R$\n$\\mathcal{A}_{ext}(R)\\leq CP$",face=BLUE)
    for x in (.175,.50,.825): arrow(ax,(x,.75),(x+(0.5-x)*.45,.66))
    box(ax,.07,.34,.86,.13,"$\\mathcal{K}_D+R^{-1}\\!\\int|Q_s\\cdot\\nabla\\eta_R|$\n$\\leq C(P+P^{3/2})$",face="white")
    arrow(ax,(.5,.55),(.5,.47))
    box(ax,.18,.23,.64,.075,"$P\\leq1\\Rightarrow$ RHS $\\leq CP$\nsize closure, not absorption",edge=GREEN,face="#EEF6EE",fs=6.3)
    box(ax,.05,.055,.90,.115,"exact shear: quadratic $N^0$ vs cubic / $H$ $N^{-2}$\nsame-window cubic-only no-go; not a buffered no-go",edge=RED,face="#FAECE8",fs=6.15)
    tag(ax,.05,.015,"EXACT SOLUTION",RED); tag(ax,.66,.015,"NOT CLAY",GREY)
    fig.text(.5,.035,"Schematic proof ledger • no DNS • no unknown constant encoded numerically",ha="center",fontsize=6.5,color=GREY)
    fixed_dt=datetime(2026,9,1,tzinfo=timezone.utc)
    fig.savefig(HERE/"figure.svg",metadata={"Date":FROZEN_UTC,"Description":f"SourceCommit={COMMIT}; CertificateSHA256={CERT_SHA}"})
    fig.savefig(HERE/"figure.pdf",metadata={"Title":"R0.74B buffered-tail closure","Subject":f"{COMMIT}; {CERT_SHA}","CreationDate":fixed_dt,"ModDate":fixed_dt})
    fig.savefig(HERE/"figure.png",dpi=600)
    plt.close(fig)
    svg=HERE/"figure.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())+"\n",encoding="utf-8",newline="\n")

def render_pdf():
    doc=pdfium.PdfDocument(str(HERE/"figure.pdf")); page=doc[0]
    im=page.render(scale=4252/page.get_size()[0]).to_pil().convert("RGB")
    im.save(HERE/"qa-pdf.png"); page.close(); doc.close()
    src=Image.open(HERE/"figure.png").convert("RGB")
    src.resize((2126,922),Image.Resampling.LANCZOS).save(HERE/"qa-final-size.png")
    ImageOps.grayscale(src).convert("RGB").save(HERE/"qa-grayscale.png")

def write_package():
    proof_bytes=subprocess.run(["git","-C",str(REPO),"show",f"{COMMIT}:{PROOF}"],check=True,capture_output=True).stdout
    cert=REPO/CERT
    assert hashlib.sha256(cert.read_bytes()).hexdigest()==CERT_SHA
    assert json.loads(cert.read_text())["summary"]=={"passed":67,"total":67}
    data=rows()
    with (HERE/"source-data.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f,lineterminator="\n"); w.writerow(["panel","series","record","r_lo","r_hi","collar_lo","collar_hi","outward_j","current_j","inward_j","core_exception","gamma_log_coefficient","note"]); w.writerows(data)
    config={"figureId":"fig-r074b-buffered-tail-closure","canvasMm":[180,78],"dpi":600,"panels":["A","B","C"],"sourceCommit":COMMIT,"certificateSha256":CERT_SHA,"dns":False,"unknownConstantsNumericallyEncoded":False}
    contract={"schema":"r074b-figure-contract-v1","sourceCommit":COMMIT,"certificate":{"schemaVersion":3,"checks":"67/67","sha256":CERT_SHA},"statuses":["ANALYTIC","FINITE","EXACT SOLUTION","OPEN","NOT CLAY"],"expectedFileCount":25}
    (HERE/"config.json").write_text(canonical(config)); (HERE/"contract.json").write_text(canonical(contract))
    caption=("Figure X. Buffered closure of the R0.74A Gaussian tails. (A) One-shell cutoff enlargement at R is paid by the exact doubled-radius annulus map; m=1,2 remain core rows. (B) Suitable local energy and weighted Hölder give C(P^(2/3)+P), with distinct clocks. (C) Algebraic, velocity, and gauge-corrected pressure rows inherit the same payment, giving C(P+P^(3/2)) and CP for P<=1. The exact-shear inset obstructs only same-window cubic-only payment. Solid boxes are analytic; dashed badges are finite checks. No DNS. NOT CLAY.\n")
    (HERE/"caption.md").write_text(caption)
    (HERE/"README.md").write_text("# R0.74B buffered-tail closure figure\n\nReproducible 25-file journal package frozen to commit "+COMMIT+". Run plot.py, then validate.py.\n")
    (HERE/"chart-contract-and-source-data.md").write_text("# Chart contract and source data\n\nAll geometry and exponents are closed-form rows in source-data.csv. Unknown constants are labels only, never numeric marks. No DNS or simulation.\n")
    (HERE/"qa-protocol.md").write_text("# QA protocol\n\nVerify commit/hash, 25 files, 180x78 mm PDF, 600 dpi PNG, panel/status labels, grayscale legibility, no DNS, no numerical encoding of C.\n")
    (HERE/"requirements.txt").write_text("matplotlib==3.10.6\npillow==12.3.0\npypdf==6.10.0\npypdfium2==5.13.0\n")
    (HERE/"environment.json").write_text(canonical({"frozenUtc":FROZEN_UTC,"python":sys.version,"dgxUsed":False,"networkUsed":False}))
    (HERE/"progress.ndjson").write_text(canonical({"event":"rendered","utc":FROZEN_UTC}).strip()+"\n")
    (HERE/"resource-log.ndjson").write_text(canonical({"cpuOnly":True,"dns":False,"simulation":False}).strip()+"\n")
    (HERE/"results.json").write_text(canonical({"status":"PREVALIDATION","sourceCommit":COMMIT,"certificateSha256":CERT_SHA,"rows":len(data)}))
    (HERE/"qa-report.md").write_text("# QA report\n\nPending independent validator.\n")
    (HERE/"validation.json").write_text(canonical({"status":"PENDING"}))
    (HERE/"manifest.json").write_text(canonical({"figureId":config["figureId"],"sourceCommit":COMMIT,"certificateSha256":CERT_SHA,"files":[]}))
    (HERE/"SHA256SUMS").write_text("")

if __name__=="__main__":
    write_package(); draw(); render_pdf()
