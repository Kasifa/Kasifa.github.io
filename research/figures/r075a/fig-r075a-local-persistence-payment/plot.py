#!/usr/bin/env python3
"""Deterministic renderer for the R0.75A analytic four-panel figure."""
from __future__ import annotations
import argparse, atexit, csv, hashlib, importlib.metadata, json, math, os, platform, resource, shutil, subprocess, tempfile, time
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any

_MPL_CONFIG=Path(tempfile.mkdtemp(prefix="r075a-mpl-")); os.environ["MPLCONFIGDIR"]=str(_MPL_CONFIG); atexit.register(lambda:shutil.rmtree(_MPL_CONFIG,ignore_errors=True))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from PIL import Image
import pypdfium2 as pdfium

HERE=Path(__file__).resolve().parent; DEFAULT_REPOSITORY=HERE.parents[3]
ARTIFACT_ID="fig-r075a-local-persistence-payment"
REQUIRED_LABEL="ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE SIMULATION | NOT DNS | NO NOVELTY CLAIM | NOT CLAY"
FIXED_DATE=datetime(2026,9,3,tzinfo=timezone.utc)
SOURCE_FILES=("README.md","caption.md","chart-contract-and-source-data.md","command.txt","config.json","contract.json","plot.py","qa-protocol.md","requirements.txt","validate.py")
RAW_FILES=("environment.json","figure.pdf","figure.png","figure.svg","progress.ndjson","qa-final-size.png","qa-grayscale.png","qa-pdf.png","resource-log.ndjson","results.json","source-data.csv")
DETERMINISTIC_GENERATED_FILES=("figure.pdf","figure.png","figure.svg","qa-final-size.png","qa-grayscale.png","qa-pdf.png","results.json","source-data.csv")
PALETTE={"root":"#244C70","root_dark":"#173149","root_light":"#AEBFCC","root_open":"#E8EEF2","ink":"#1F2529","mid":"#747C82","light":"#D9DDE0","pale":"#F2F4F5","paper":"#FFFFFF"}
P=Fraction(32,63); LAMBDA=Fraction(63,32); C_GAMMA=Fraction(8,3969); RHO=Fraction(9,10000); POSITIVE_RATE=Fraction(5,24)*C_GAMMA-RHO/6
CSV_FIELDS=("panel","series","x","y","x_unit","y_unit","exact_value","role","source_locator","note")

def sha256_file(path:Path)->str:
 d=hashlib.sha256();
 with path.open("rb") as h:
  for chunk in iter(lambda:h.read(1<<20),b""): d.update(chunk)
 return d.hexdigest()
def atomic_text(path:Path,text:str)->None:
 path.parent.mkdir(parents=True,exist_ok=True); fd,tmp=tempfile.mkstemp(prefix=f".{path.name}.",dir=path.parent); t=Path(tmp)
 try:
  with os.fdopen(fd,"w",encoding="utf-8",newline="\n") as h:h.write(text)
  os.replace(t,path)
 finally:t.unlink(missing_ok=True)
def atomic_json(path:Path,value:Any)->None:atomic_text(path,json.dumps(value,indent=2,sort_keys=True)+"\n")
def append_json_line(path:Path,value:Any)->None:
 with path.open("a",encoding="utf-8",newline="\n") as h:h.write(json.dumps(value,sort_keys=True)+"\n")
def repository_head(repository:Path)->str:return subprocess.run(["git","rev-parse","HEAD"],cwd=repository,check=True,capture_output=True,text=True).stdout.strip()
def validate_source_binding(repository:Path,config:dict[str,Any])->dict[str,Any]:
 b=config["sourceBinding"]; observed={}
 for key in ("main","primaryAudit","literatureAudit"):
  e=b[key]; p=repository/e["path"]
  if not p.is_file() or sha256_file(p)!=e["sha256"] or p.stat().st_size!=int(e["byteCount"]):raise RuntimeError(f"bound input mismatch: {e['path']}")
  observed[key]={"path":e["path"],"sha256":e["sha256"],"byteCount":int(e["byteCount"])}
 head=repository_head(repository)
 if head!=b["coreCommit"]:raise RuntimeError(f"core commit mismatch: {head}")
 observed["coreCommit"]=head; return observed

def build_source_rows()->list[dict[str,str]]:
 rows=[]
 def add(panel,series,x,y,exact,role,loc,note):rows.append({"panel":panel,"series":series,"x":x,"y":y,"x_unit":"normalized/step","y_unit":"normalized/exponent","exact_value":exact,"role":role,"source_locator":loc,"note":note})
 for v in [
  ("outer x1 left","-1/4","0","-sqrt(pL)R/4","A.9","moving strip face"),("core x1 left","-3/16","0","-3sqrt(pL)R/16","A.10","strictly nested"),("core x1 right","3/16","0","3sqrt(pL)R/16","A.10","strictly nested"),("outer x1 right","1/4","0","sqrt(pL)R/4","A.9","moving strip face"),
  ("z outer left","5/4","-1","5R/4","A.9","normalized z face"),("z core left","21/16","-15/16","21R/16","A.10","strict gap"),("z core right","23/16","-9/16","23R/16","A.10","strict gap"),("z outer right","3/2","-1/2","3R/2","A.9","normalized z face"),("strip volume","1/16","","|S_+|=(1/16)sqrt(pL)R^3","A.12","analytic geometry")]:add("A",v[0],v[1],v[2],v[3],"geometry",v[4],v[5])
 for v in [("persistent branch","0","E(t)>=E_*/2 for all t in J","A.24","X>=(c_0/2)E_*R^3"),("drop branch","1","exists t_0: E(t_0)<E_*/2","A.25","endpoint rise is charged"),("cutoff error","2","E'<=K_phi R^-3 M","A.22","exact R^-3 scale"),("common conclusion","3","X>=c_1E_*R^3","A.26","exhaustive dichotomy")]:add("B",v[0],v[1],"",v[2],"proof branch",v[3],v[4])
 for v in [("X","0","3","X>=cE_*R^3","A.26","R exponent"),("support","1","6","volume<=CL^(1/2)R^6","A.27","support volume"),("Holder","2","3/2","int|u|^3>=cE_*^(3/2)R^(3/2)L^(-1/4)","A.28","cubic step"),("weight","3","1/4","W_2R>=omega^(1/4)","A.13; A.29","payment weight"),("endpoint","4","-1","E_*>=(2R/omega)h_rem","A.30","endpoint substitution"),("payment","5","-5/4","P>=ch^(3/2)R omega^(-5/4)L^(-1/4)","A.31","payment"),("two-thirds","6","-5/6","P^(2/3)>=chR^(2/3)omega^(-5/6)L^(-1/6)","A.1","final"),("rate","7",str(POSITIVE_RATE),"64279/238140000>0","A.34","strict positive")]:add("C",v[0],v[1],v[2],v[3],"exact ledger",v[4],v[5])
 for i,v in enumerate([("PROVED","moving-cutoff identity; local dichotomy; W-remote payment","A.18; A.26; A.1","exact smooth family"),("EXACT","horizontal modal energy and decay","A.36--A.42","global ledger"),("OPEN","complete K; fixed deletion; arbitrary suitable weak solutions; regularity","A.4; Section 8","no promotion"),("NEXT A.63","remote complete-clock extraction","A.63","all endpoint and accumulated rows")]):add("D",v[0],str(i),"",v[1],"claim hierarchy",v[2],v[3])
 return rows
def rows_to_csv(rows):
 import io
 b=io.StringIO(newline="");w=csv.DictWriter(b,fieldnames=CSV_FIELDS,lineterminator="\n");w.writeheader();w.writerows(rows);return b.getvalue()
def blossom(fig):
 c=(.958,.936)
 for i,a in enumerate((90,18,-54,-126,162)):
  r=math.radians(a);fig.add_artist(patches.Ellipse((c[0]+.014*math.cos(r),c[1]+.020*math.sin(r)),.0105,.0163,angle=a-90,transform=fig.transFigure,facecolor="none",edgecolor=PALETTE["root_dark"] if i%2==0 else PALETTE["root_light"],linewidth=.9,zorder=30))
 fig.add_artist(patches.Circle(c,.0035,transform=fig.transFigure,facecolor=PALETTE["ink"],edgecolor="none",zorder=31))
def panel_title(ax,label,title):ax.set_title(f"{label}  {title}",loc="left",fontsize=8.1,fontweight="bold",color=PALETTE["ink"],pad=5)
def badge(ax,text):ax.text(.985,.975,text,transform=ax.transAxes,ha="right",va="top",fontsize=4.05,color=PALETTE["root_dark"],fontweight="bold",bbox={"boxstyle":"round,pad=.20","facecolor":PALETTE["root_open"],"edgecolor":PALETTE["root_light"],"linewidth":.55},zorder=20)
def arrow(ax,a,b,dashed=False):ax.annotate("",xy=b,xytext=a,xycoords=ax.transAxes,arrowprops={"arrowstyle":"-|>","color":PALETTE["mid"],"linewidth":.75,"linestyle":"--" if dashed else "-","mutation_scale":7,"shrinkA":3,"shrinkB":3})
def box(ax,x,y,w,h,text,filled=False,dashed=False,fs=4.5):
 ax.add_patch(patches.FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.010,rounding_size=.014",transform=ax.transAxes,facecolor=PALETTE["root_open"] if filled else PALETTE["paper"],edgecolor=PALETTE["root"] if filled else PALETTE["mid"],linewidth=.8,linestyle="--" if dashed else "-"));ax.text(x+w/2,y+h/2,text,transform=ax.transAxes,ha="center",va="center",fontsize=fs,color=PALETTE["root_dark"] if filled else PALETTE["ink"],linespacing=1.15)

def render_figure(config,rows):
 plt.rcParams.update({"font.family":"DejaVu Sans","font.size":6.3,"figure.facecolor":"white","savefig.facecolor":"white","pdf.fonttype":42,"ps.fonttype":42,"svg.fonttype":"none","svg.hashsalt":ARTIFACT_ID,"axes.unicode_minus":False,"hatch.color":PALETTE["mid"],"hatch.linewidth":.45})
 fig,axs=plt.subplots(2,2,figsize=(178/25.4,116/25.4),dpi=600);fig.subplots_adjust(left=.067,right=.975,bottom=.105,top=.815,wspace=.29,hspace=.47);a,b,c,d=axs.ravel()
 fig.text(.04,.955,"Local persistence/payment dichotomy",ha="left",va="top",fontsize=11,fontweight="bold",color=PALETTE["ink"]);fig.text(.04,.913,"R0.75A | exact moving-cutoff alternative | W-remote witness proved | complete clock open",ha="left",va="top",fontsize=6,color=PALETTE["mid"]);blossom(fig)
 panel_title(a,"A","Moving strip and nested endpoint core");badge(a,"EXACT NORMALIZED GEOMETRY");a.set_xlim(1.22,1.53);a.set_ylim(-1.04,-.46);a.set_xlabel(r"$z/R$",fontsize=5);a.set_ylabel(r"$(x_3-pLR)/R$",fontsize=5);a.tick_params(labelsize=4.5,length=2);a.grid(color=PALETTE["light"],linewidth=.4,linestyle=(0,(2,2)))
 a.add_patch(patches.Rectangle((1.25,-1),.25,.5,facecolor=PALETTE["pale"],edgecolor=PALETTE["mid"],linewidth=1));a.add_patch(patches.Rectangle((21/16,-15/16),2/16,6/16,facecolor=PALETTE["root_open"],edgecolor=PALETTE["root_dark"],linewidth=1.2));a.text(1.375,-.74,r"$\Omega_0(t)$",ha="center",va="center",fontsize=6,fontweight="bold",color=PALETTE["root_dark"]);a.text(1.505,-.98,r"$\mathcal{S}_+(t)$",ha="right",va="bottom",fontsize=5,color=PALETTE["mid"]);a.text(.025,.90,r"$|x_1|<3\sqrt{pL}R/16\ \subset\ |x_1|<\sqrt{pL}R/4$",transform=a.transAxes,ha="left",fontsize=4.25);a.text(.025,.83,r"$|\mathcal{S}_+|=\frac{1}{16}\sqrt{pL}R^3,\quad p=\frac{32}{63}$",transform=a.transAxes,ha="left",fontsize=4.35,color=PALETTE["root_dark"])
 panel_title(b,"B","Exhaustive local-energy alternative");b.axis("off");badge(b,"TWO CASES | NO THIRD BRANCH");box(b,.03,.64,.42,.20,"PERSISTENCE\n"+r"$E(t)\geq E_*/2$ on $J$",filled=True,fs=5);box(b,.55,.64,.42,.20,"ENDPOINT RISE\n"+r"$\exists t_0: E(t_0)<E_*/2$",fs=5);box(b,.57,.35,.38,.14,r"$E'\leq K_\phi R^{-3}M$"+"\ncharges the rise",fs=4.7);arrow(b,(.76,.64),(.76,.49));box(b,.20,.10,.60,.16,r"$X=\int_JM(t)\,dt \geq c_1E_*R^3$",filled=True,fs=6);arrow(b,(.24,.64),(.42,.26));arrow(b,(.76,.35),(.58,.26));b.text(.5,.025,"(A.24) and (A.25) are exhaustive; both close at (A.26)",transform=b.transAxes,ha="center",fontsize=4.3,color=PALETTE["mid"])
 panel_title(c,"C","Hölder, weight, endpoint substitution");c.axis("off");badge(c,"EXACT EXPONENT LEDGER");box(c,.02,.70,.27,.17,r"$X\gtrsim E_*R^3$"+"\n"+r"volume $\lesssim L^{1/2}R^6$",fs=4.6);box(c,.365,.70,.27,.17,"HÖLDER\n"+r"$\int|u|^3\gtrsim E_*^{3/2}R^{3/2}L^{-1/4}$",filled=True,fs=4.35);box(c,.71,.70,.27,.17,"WEIGHT\n"+r"$W_{2R}\geq\omega^{1/4}$",fs=4.6);arrow(c,(.29,.785),(.365,.785));arrow(c,(.635,.785),(.71,.785));box(c,.15,.43,.70,.14,r"$P_R^M\gtrsim \omega^{1/4}E_*^{3/2}R^{-1/2}L^{-1/4}$",fs=4.8);arrow(c,(.50,.70),(.50,.57));box(c,.15,.22,.70,.13,r"$E_*\geq(2R/\omega)h_{\rm rem}\ \Longrightarrow\ (P_R^M)^{2/3}\gtrsim h_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6}$",filled=True,fs=4.15);arrow(c,(.50,.43),(.50,.35));c.text(.5,.105,r"$\frac{5}{24}c_\gamma-\frac{\rho}{6}=\frac{64279}{238140000}>0$",transform=c.transAxes,ha="center",fontsize=5.5,fontweight="bold",color=PALETTE["root_dark"]);c.text(.5,.025,"PERSISTENT + CRITICAL + ARBITRARILY SHORTER SMOOTH FOCUSING",transform=c.transAxes,ha="center",fontsize=4.2,fontweight="bold",color=PALETTE["ink"])
 panel_title(d,"D","Proved boundary and next proposition");d.axis("off");badge(d,"FAIL-CLOSED CLAIM HIERARCHY");cards=[(.70,"PROVED","moving-cutoff identity | local dichotomy\nW-remote endpoint/payment",True,False),(.49,"EXACT","horizontal modal energy and forward decay",False,False),(.28,"OPEN","complete K | fixed deletion | arbitrary suitable weak solutions\nregularity / singularity",False,True),(.06,"NEXT A.63","remote complete-clock extraction\ncontrol every endpoint and accumulated row",True,True)]
 for y,s,t,fill,dash in cards:box(d,.03,y,.20,.145,s,filled=s=="PROVED",dashed=dash,fs=4.5);box(d,.255,y,.71,.145,t,filled=fill,dashed=dash,fs=4.15)
 d.text(.5,.005,"local witness lower bound is not a whole-clock upper bound",transform=d.transAxes,ha="center",fontsize=4.2,color=PALETTE["mid"])
 fig.text(.5,.035,REQUIRED_LABEL,ha="center",va="center",fontsize=5.15,color=PALETTE["root_dark"],fontweight="bold",family="DejaVu Sans Mono");fig.text(.5,.014,"Core commit d15b7d8f | source SHA-256 binding | primary PASS, blockers 0 | literature framing PASS, not novelty",ha="center",va="center",fontsize=4.15,color=PALETTE["mid"]);return fig

def write_exports(fig,out,config):
 meta={"Title":"R0.75A local persistence/payment dichotomy","Author":"C. K. Zeng","Subject":REQUIRED_LABEL,"Keywords":"Navier-Stokes, analytic schematic, local persistence, NOT CLAY","Creator":f"Matplotlib {matplotlib.__version__}; {ARTIFACT_ID}"};dpi=int(config["figure"]["publicationDpi"]);qd=int(config["figure"]["qaDpi"])
 fig.savefig(out/"figure.png",dpi=dpi,metadata={"Title":meta["Title"],"Author":meta["Author"],"Description":REQUIRED_LABEL,"Software":meta["Creator"]});fig.savefig(out/"figure.svg",format="svg",metadata={"Date":"2026-09-03","Title":meta["Title"],"Creator":meta["Creator"],"Description":REQUIRED_LABEL});fig.savefig(out/"figure.pdf",format="pdf",metadata={**meta,"CreationDate":FIXED_DATE,"ModDate":FIXED_DATE});plt.close(fig)
 expected=(int(178/25.4*qd),int(116/25.4*qd))
 with Image.open(out/"figure.png") as im:
  small=im.resize(expected,Image.Resampling.LANCZOS);small.save(out/"qa-final-size.png",dpi=(qd,qd),compress_level=6);small.convert("L").convert("RGB").save(out/"qa-grayscale.png",dpi=(qd,qd),compress_level=6);pub=list(im.size);pdpi=[round(float(x),3) for x in im.info.get("dpi",(0,0))]
 doc=pdfium.PdfDocument(str(out/"figure.pdf"));page_count=len(doc)
 if page_count!=1:doc.close();raise RuntimeError(f"expected one PDF page, found {page_count}")
 page=doc[0];im=page.render(scale=qd/72).to_pil().convert("RGB");im=im.resize(expected,Image.Resampling.LANCZOS) if im.size!=expected else im;im.save(out/"qa-pdf.png",dpi=(qd,qd),compress_level=6);page.close();doc.close();return {"publicationPngPixels":pub,"publicationPngDpi":pdpi,"qaPixels":list(expected),"pdfPageCount":page_count}
def total_memory():
 try:return int(subprocess.run(["sysctl","-n","hw.memsize"],check=True,capture_output=True,text=True).stdout.strip())
 except:return None
def render_package(out_dir=HERE,repository=DEFAULT_REPOSITORY,dependency_root_supplied=False,write_logs=True):
 out_dir.mkdir(parents=True,exist_ok=True);cfg=json.loads((HERE/"config.json").read_text());binding=validate_source_binding(repository,cfg);start=time.monotonic()
 if write_logs:atomic_text(out_dir/"progress.ndjson","");atomic_text(out_dir/"resource-log.ndjson","")
 def log(phase,n):
  if not write_logs:return
  now=datetime.now(timezone.utc).isoformat();elapsed=round(time.monotonic()-start,6);append_json_line(out_dir/"progress.ndjson",{"artifactId":ARTIFACT_ID,"ordinal":n,"phase":phase,"elapsedSeconds":elapsed,"timestampUtc":now});rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);append_json_line(out_dir/"resource-log.ndjson",{"artifactId":ARTIFACT_ID,"ordinal":n,"phase":phase,"elapsedSeconds":elapsed,"residentSetBytes":rss,"timestampUtc":now})
 log("start",1);log("source-binding-verified",2);rows=build_source_rows();atomic_text(out_dir/"source-data.csv",rows_to_csv(rows));log("source-data-written",3);fig=render_figure(cfg,rows);log("figure-composed",4);exports=write_exports(fig,out_dir,cfg);log("vector-raster-pdf-exported",5)
 counts={p:sum(r["panel"]==p for r in rows) for p in "ABCD"};contract=json.loads((HERE/"contract.json").read_text());results={"artifactId":ARTIFACT_ID,"schema":"r075a-figure-results-v1","sourceBinding":binding,"exactConstants":contract["exactConstants"],"claimBoundary":contract["claimBoundary"],"panelRowCounts":counts,"sourceDataRows":len(rows),"exports":exports,"requiredVisibleLabel":REQUIRED_LABEL};atomic_json(out_dir/"results.json",results)
 env={"artifactId":ARTIFACT_ID,"schema":"r075a-figure-environment-v1","createdAtUtc":datetime.now(timezone.utc).isoformat(),"repositoryHead":repository_head(repository),"python":platform.python_version(),"machine":platform.machine(),"logicalCpuCount":os.cpu_count(),"memoryBytes":total_memory(),"dependencyLocatorPolicy":"external version-pinned directory supplied; absolute path omitted" if dependency_root_supplied else "bundled environment","packages":{x:importlib.metadata.version(x) for x in ("numpy","matplotlib","pillow","pypdf","pypdfium2")}};atomic_json(out_dir/"environment.json",env);log("complete",6);return results
def main():
 p=argparse.ArgumentParser();p.add_argument("--render",action="store_true");p.add_argument("--repository",type=Path,default=DEFAULT_REPOSITORY);p.add_argument("--deps",type=Path);p.add_argument("--output",type=Path,default=HERE);a=p.parse_args();
 if not a.render:raise SystemExit("pass --render")
 render_package(a.output.resolve(),repository=a.repository.resolve(),dependency_root_supplied=a.deps is not None,write_logs=True);print(json.dumps({"artifactId":ARTIFACT_ID,"status":"rendered"},sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
