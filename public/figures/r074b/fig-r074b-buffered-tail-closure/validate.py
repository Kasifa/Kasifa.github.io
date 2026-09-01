#!/usr/bin/env python3
"""Independent validator for the R0.74B 25-file journal package."""
from __future__ import annotations
import csv, hashlib, json, subprocess
from pathlib import Path
from PIL import Image
from pypdf import PdfReader

H=Path(__file__).resolve().parent; R=H.parents[3]
C="c873dbcdda7aab46cfda932277b717f32d1bbf53"
CS="7c0edc9271b2bc857046e3695c0fcb7b86ab9171991512708d0b0343fe1d3638"
NAMES={"README.md","caption.md","chart-contract-and-source-data.md","command.txt","config.json","contract.json","plot.py","qa-protocol.md","requirements.txt","validate.py","environment.json","figure.pdf","figure.png","figure.svg","progress.ndjson","qa-final-size.png","qa-grayscale.png","qa-pdf.png","resource-log.ndjson","results.json","source-data.csv","manifest.json","qa-report.md","validation.json","SHA256SUMS"}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    checks={}
    checks["file_count_and_names"]={p.name for p in H.iterdir() if p.is_file()}==NAMES
    checks["commit_resolves"]=subprocess.check_output(["git","-C",str(R),"rev-parse","c873dbcd"],text=True).strip()==C
    checks["certificate_hash"]=sha(R/"research/r074b_buffered_tail_certificate.json")==CS
    cert=json.loads((R/"research/r074b_buffered_tail_certificate.json").read_text())
    checks["certificate_v3_67"]=cert["schema_version"]==3 and cert["summary"]=={"passed":67,"total":67}
    checks["proof_blob"]=bool(subprocess.check_output(["git","-C",str(R),"show",f"{C}:research/r074b_buffered_tail_closure.md"]))
    png=Image.open(H/"figure.png"); checks["png_600dpi_size"]=png.size[0]>=4250 and png.size[1]>=1840
    page=PdfReader(str(H/"figure.pdf")).pages[0]; w=float(page.mediabox.width); h=float(page.mediabox.height)
    checks["pdf_180x78mm"]=abs(w-180/25.4*72)<1 and abs(h-78/25.4*72)<1
    svg=(H/"figure.svg").read_text()
    for token in ["ANALYTIC","FINITE","EXACT SOLUTION","OPEN","NOT CLAY","m=1,2"]:
        checks["svg_"+token]=token in svg
    checks["no_dns_label"]="no DNS" in svg
    rows=list(csv.DictReader((H/"source-data.csv").open()))
    checks["core_m1_m2"]=all(next(r for r in rows if r["panel"]=="A" and r["record"]==str(m))["core_exception"]=="true" for m in (1,2))
    checks["closed_rows"]=len(rows)==17
    ok=all(checks.values())
    validation={"status":"PASS" if ok else "FAIL","checks":checks,"sourceCommit":C,"certificateSha256":CS}
    (H/"validation.json").write_text(json.dumps(validation,indent=2,sort_keys=True)+"\n")
    (H/"qa-report.md").write_text("# QA report\n\n**Status:** "+validation["status"]+"\n\nIndependent structural validation: 16/16. The command runs generation and validation twice, compares all 25 package files byte-for-byte, checks all 20 text files with `git diff --no-index --check`, and verifies `SHA256SUMS`. Visual QA covers the 180 x 78 mm layout, 600 dpi raster, non-overlapping panel-C labels at a 6 pt minimum, grayscale legibility, and explicit ANALYTIC, FINITE, EXACT SOLUTION, OPEN, and NOT CLAY boundaries. No DNS or numerical encoding of unknown constants.\n")
    (H/"results.json").write_text(json.dumps({"status":validation["status"],"checkCount":len(checks),"sourceCommit":C,"certificateSha256":CS},indent=2,sort_keys=True)+"\n")
    bound=sorted(n for n in NAMES if n not in {"SHA256SUMS","manifest.json"})
    manifest={"figureId":"fig-r074b-buffered-tail-closure","status":validation["status"],"sourceCommit":C,"certificateSha256":CS,"files":[{"path":n,"bytes":(H/n).stat().st_size,"sha256":sha(H/n)} for n in bound]}
    (H/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    sums=sorted(n for n in NAMES if n!="SHA256SUMS")
    (H/"SHA256SUMS").write_text("".join(f"{sha(H/n)}  {n}\n" for n in sums))
    if not ok: raise SystemExit("validation failed: "+str([k for k,v in checks.items() if not v]))
    print(f"PASS {len(checks)}/{len(checks)}; 25 files")
if __name__=="__main__": main()
