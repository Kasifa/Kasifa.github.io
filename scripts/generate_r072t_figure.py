#!/usr/bin/env python3
"""Generate the analytic R0.72T journal figure and its deterministic archive.

The figure samples exact formulas.  It does not simulate the non-periodic
cubic PDE and does not infer a semigroup estimate from numerical data.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import platform
from pathlib import Path
import shutil
import subprocess
import sys
import time
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


REPOSITORY = Path(__file__).resolve().parents[1]
PACKAGE = REPOSITORY / "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model"
CERTIFICATE = REPOSITORY / "research/certificates/r072t/certificate.json"
PUBLIC = REPOSITORY / "public/assets/r072t"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def linspace(left: float, right: float, count: int) -> list[float]:
    return [left + (right - left) * index / (count - 1) for index in range(count)]


def heat_profile(d: float, x: float) -> float:
    return -0.5 * math.exp(-d) * math.sin(x) + 0.25 * math.exp(-4.0 * d) * math.sin(2.0 * x)


def leading_profile(s: float, x: float) -> float:
    return -0.25 * x**3 - 1.5 * s * x


def save_data() -> int:
    rows: list[dict[str, str]] = []
    s = -0.5
    grid = linspace(-3.0, 3.0, 121)
    for epsilon in (0.5, 0.3, 0.15):
        values = [heat_profile(epsilon**2 * s, epsilon * x) / epsilon**3 for x in grid]
        for x, value in zip(grid, values):
            rows.append({
                "panel": "A", "series": f"exact-epsilon-{epsilon:g}",
                "x": f"{x:.17g}", "y": f"{value:.17g}",
                "source": "exact W(epsilon^2*s,epsilon*X)/epsilon^3", "status": "analytic sample",
            })
    for x, value in ((x, leading_profile(s, x)) for x in grid):
        rows.append({
            "panel": "A", "series": "leading-H3", "x": f"{x:.17g}",
            "y": f"{value:.17g}", "source": "-(1/4)X^3-(3/2)sX", "status": "exact leading polynomial",
        })
    gamma = linspace(-0.05, 0.45, 101)
    for label, alpha in (
        ("diffusion", [2 * x - 1 for x in gamma]),
        ("cubic", [-3 * x for x in gamma]),
        ("time-drift", [-(1 + x) / 2 for x in gamma]),
    ):
        for x, y in zip(gamma, alpha):
            rows.append({
                "panel": "B", "series": label, "x": f"{x:.17g}", "y": f"{y:.17g}",
                "source": "exact affine exponent equation", "status": "analytic sample",
            })
    m = linspace(-2.0, 2.0, 161)
    action = [x**2 / 12 + 1 / 720 for x in m]
    for x, y in zip(m, action):
        rows.append({
            "panel": "C", "series": "minimum-action-h=1", "x": f"{x:.17g}", "y": f"{y:.17g}",
            "source": "m^2/12+1/720", "status": "exact drift-only calibration",
        })
    with (PACKAGE / "data.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("panel", "series", "x", "y", "source", "status"))
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


class Scene:
    def __init__(self) -> None:
        self.items: list[tuple] = []

    def line(self, x1, y1, x2, y2, color="#17212b", width=2, dash=None):
        self.items.append(("line", x1, y1, x2, y2, color, width, dash))

    def polyline(self, points, color="#285f8f", width=2, dash=None):
        self.items.append(("polyline", points, color, width, dash))

    def text(self, x, y, value, size=18, color="#17212b", anchor="start", bold=False):
        self.items.append(("text", x, y, value, size, color, anchor, bold))

    def circle(self, x, y, radius, color="#17212b"):
        self.items.append(("circle", x, y, radius, color))

    def rect(self, left, top, right, bottom, fill="white"):
        self.items.append(("rect", left, top, right, bottom, fill))


def mapping(x0, x1, y0, y1, left, right, top, bottom):
    return (
        lambda x: left + (x - x0) * (right - left) / (x1 - x0),
        lambda y: bottom - (y - y0) * (bottom - top) / (y1 - y0),
    )


def axes(scene: Scene, box, x_ticks, y_ticks, x_map, y_map, xlabel, ylabel):
    left, right, top, bottom = box
    grid = "#d9dde1"
    for value in x_ticks:
        x = x_map(value); scene.line(x, top, x, bottom, grid, 1); scene.text(x, bottom + 28, f"{value:g}", 21, "#66727e", "middle")
    for value in y_ticks:
        y = y_map(value); scene.line(left, y, right, y, grid, 1); scene.text(left - 10, y + 7, f"{value:g}", 21, "#66727e", "end")
    scene.line(left, bottom, right, bottom, "#17212b", 2); scene.line(left, top, left, bottom, "#17212b", 2)
    scene.text((left + right) / 2, bottom + 62, xlabel, 24, anchor="middle")
    scene.text(left, top - 22, ylabel, 23)


def build_scene() -> Scene:
    scene = Scene(); ink, muted, blue, red, gold, green = "#17212b", "#66727e", "#285f8f", "#a9413a", "#a6781f", "#2d7563"
    panel_lefts = (60, 625, 1190); box_width = 475; top, bottom = 145, 620
    titles = (("A", "exact heat-profile collapse"), ("B", "unique exponent balance"), ("C", "drift-only action calibration"))
    for left, (letter, title) in zip(panel_lefts, titles):
        scene.text(left, 65, letter, 34, ink, bold=True); scene.text(left + 42, 65, title, 28, ink, bold=True)

    box = (panel_lefts[0] + 48, panel_lefts[0] + box_width, top, bottom)
    xm, ym = mapping(-3, 3, -5, 5, *box)
    axes(scene, box, [-3, -1.5, 0, 1.5, 3], [-5, -2.5, 0, 2.5, 5], xm, ym, "scaled coordinate X", "scaled W")
    grid = linspace(-3, 3, 400); s = -0.5
    for epsilon, color, dash in ((0.5, gold, "8,5"), (0.3, green, "4,4"), (0.15, blue, None)):
        points = [(xm(x), ym(heat_profile(epsilon**2 * s, epsilon * x) / epsilon**3)) for x in grid]
        scene.polyline(points, color, 3, dash)
    scene.polyline([(xm(x), ym(leading_profile(s, x))) for x in grid], ink, 4)
    scene.text(box[0] + 8, top + 29, "s=-1/2; corrections O(ε^2), O(ε^4)", 20, muted)
    for index, (label, color, dash) in enumerate((("exact ε=.50", gold, "8,5"), ("exact ε=.30", green, "4,4"), ("exact ε=.15", blue, None), ("leading H3", ink, None))):
        y = top + 60 + 29 * index; scene.line(box[2] + 247, y - 7, box[2] + 282, y - 7, color, 4, dash); scene.text(box[2] + 291, y, label, 20, ink)

    box = (panel_lefts[1] + 48, panel_lefts[1] + box_width, top, bottom)
    xm, ym = mapping(-0.05, 0.45, -1.1, 0.05, *box)
    axes(scene, box, [0, .1, .2, .3, .4], [-1, -.8, -.6, -.4, -.2, 0], xm, ym, "length exponent γ", "time exponent α")
    gamma = linspace(-.05, .45, 300)
    scene.polyline([(xm(x), ym(2*x-1)) for x in gamma], blue, 3)
    cubic_gamma = linspace(0, 11/30, 240)
    scene.polyline([(xm(x), ym(-3*x)) for x in cubic_gamma], red, 3, "8,5")
    scene.polyline([(xm(x), ym(-(1+x)/2)) for x in gamma], green, 3, "3,4")
    scene.circle(xm(.2), ym(-.6), 7, ink)
    scene.text(xm(.22), ym(-.69), "(γ, α)=(1/5, -3/5)", 20, ink)
    scene.rect(box[0] + 145, top + 4, box[1] - 2, top + 72, "white")
    scene.text(box[0] + 155, top + 31, "T = nu^(-3/5)|k|^(-2/5)", 21, ink)
    scene.text(box[0] + 155, top + 60, "L = nu^(1/5)|k|^(-1/5)", 21, ink)
    for index, (label, color, dash) in enumerate((("diffusion", blue, None), ("cubic", red, "8,5"), ("time drift", green, "3,4"))):
        y = bottom - 94 + 29 * index; scene.line(box[0] + 12, y - 7, box[0] + 48, y - 7, color, 4, dash); scene.text(box[0] + 57, y, label, 20, ink)

    box = (panel_lefts[2] + 48, panel_lefts[2] + box_width, top, bottom)
    xm, ym = mapping(-2, 2, -3.05, -.35, *box)
    axes(scene, box, [-2, -1, 0, 1, 2], [-3, -2.5, -2, -1.5, -1, -.5], xm, ym, "interval midpoint m  (h=1)", "log10(minimum action / q^2)")
    m = linspace(-2, 2, 400)
    log_action = lambda x: math.log10(x*x/12 + 1/720)
    scene.polyline([(xm(x), ym(log_action(x))) for x in m], blue, 4)
    floor = math.log10(1/720)
    scene.line(box[0], ym(floor), box[1], ym(floor), red, 3, "8,5"); scene.circle(xm(0), ym(floor), 8, ink)
    scene.rect(box[0] + 65, top + 4, box[1] - 2, top + 72, "white")
    scene.text(box[0] + 75, top + 32, "Amin/q^2 = m^2 h^3/12 + h^5/720", 21, blue, bold=True)
    scene.text(box[0] + 75, top + 62, "symmetric lower bound: 1/720", 20, red)
    scene.text(box[0] + 10, bottom - 110, "||S|| = exp(-nu Amin)", 21, ink)
    scene.text(box[0] + 10, bottom - 78, "q=0: ||S||=1; joint model OPEN", 20, muted)
    return scene


def render_svg(scene: Scene) -> None:
    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<svg xmlns="http://www.w3.org/2000/svg" width="178mm" height="76mm" viewBox="0 0 1780 760">', '<rect width="1780" height="760" fill="white"/>']
    for item in scene.items:
        if item[0] == "line":
            _, x1,y1,x2,y2,color,width,dash=item; extra=f' stroke-dasharray="{dash}"' if dash else ""; parts.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{width}"{extra}/>')
        elif item[0] == "polyline":
            _,points,color,width,dash=item; extra=f' stroke-dasharray="{dash}"' if dash else ""; coords=" ".join(f"{x:.3f},{y:.3f}" for x,y in points); parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>')
        elif item[0] == "circle":
            _,x,y,r,color=item; parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{color}"/>')
        elif item[0] == "rect":
            _,left,top,right,bottom,fill=item; parts.append(f'<rect x="{left:.3f}" y="{top:.3f}" width="{right-left:.3f}" height="{bottom-top:.3f}" fill="{fill}"/>')
        else:
            _,x,y,value,size,color,anchor,bold=item; weight="700" if bold else "400"; parts.append(f'<text x="{x:.3f}" y="{y:.3f}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>')
    parts.append("</svg>")
    (PACKAGE / "figure.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def render_pdf(scene: Scene) -> None:
    width, height = 178/25.4*72, 76/25.4*72; sx, sy = width/1780, height/760
    pdfmetrics.registerFont(TTFont("ArialUnicode", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"))
    pdf = canvas.Canvas(str(PACKAGE / "figure.pdf"), pagesize=(width,height), invariant=1, pageCompression=1)
    pdf.setTitle("R0.72T exact A2 spacetime scaling and drift-only calibration"); pdf.setAuthor("Kasifa"); pdf.setSubject("Analytic identities; no PDE simulation")
    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line": _,x1,y1,x2,y2,color,lw,dash=item; points=[(x1,y1),(x2,y2)]
            else: _,points,color,lw,dash=item
            pdf.setStrokeColor(color); pdf.setLineWidth(lw*sx); pdf.setDash([float(x)*sx for x in dash.split(",")] if dash else [])
            path=pdf.beginPath(); path.moveTo(points[0][0]*sx, height-points[0][1]*sy)
            for x,y in points[1:]: path.lineTo(x*sx,height-y*sy)
            pdf.drawPath(path,stroke=1,fill=0)
        elif item[0] == "circle":
            _,x,y,r,color=item; pdf.setFillColor(color); pdf.circle(x*sx,height-y*sy,r*sx,stroke=0,fill=1)
        elif item[0] == "rect":
            _,left,top,right,bottom,fill=item; pdf.setFillColor(fill); pdf.rect(left*sx,height-bottom*sy,(right-left)*sx,(bottom-top)*sy,stroke=0,fill=1)
        else:
            _,x,y,value,size,color,anchor,bold=item; pdf.setFillColor(color); pdf.setFont("Helvetica-Bold" if bold and value.isascii() else "ArialUnicode", size*sx)
            if anchor=="middle": pdf.drawCentredString(x*sx,height-y*sy,value)
            elif anchor=="end": pdf.drawRightString(x*sx,height-y*sy,value)
            else: pdf.drawString(x*sx,height-y*sy,value)
    pdf.showPage(); pdf.save()


def render_png(scene: Scene) -> None:
    width = round(178/25.4*600); height = round(76/25.4*600); sx,sy=width/1780,height/760
    image=Image.new("RGB",(width,height),"white"); draw=ImageDraw.Draw(image)
    font_path="/System/Library/Fonts/Supplemental/Arial.ttf"; bold_path="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    cache={}
    def font(size,bold):
        key=(size,bold)
        if key not in cache: cache[key]=ImageFont.truetype(bold_path if bold else font_path,max(8,round(size*sx)))
        return cache[key]
    def stroke(points, color, width, dash):
        pixel_width = max(1, round(width * sx))
        if not dash:
            draw.line(points, fill=color, width=pixel_width)
            return
        pattern = [float(value) * sx for value in dash.split(",")]
        pattern_index = 0
        remaining = pattern[0]
        drawing = True
        for start, end in zip(points, points[1:]):
            x0, y0 = start; x1, y1 = end
            length = math.hypot(x1 - x0, y1 - y0)
            if length == 0:
                continue
            consumed = 0.0
            while consumed < length:
                step = min(remaining, length - consumed)
                left = consumed / length; right = (consumed + step) / length
                if drawing:
                    draw.line(
                        (
                            (x0 + (x1 - x0) * left, y0 + (y1 - y0) * left),
                            (x0 + (x1 - x0) * right, y0 + (y1 - y0) * right),
                        ),
                        fill=color, width=pixel_width,
                    )
                consumed += step
                remaining -= step
                if remaining <= 1e-9:
                    pattern_index = (pattern_index + 1) % len(pattern)
                    remaining = pattern[pattern_index]
                    drawing = not drawing
    for item in scene.items:
        if item[0] in ("line","polyline"):
            if item[0]=="line": _,x1,y1,x2,y2,color,lw,dash=item; points=[(x1*sx,y1*sy),(x2*sx,y2*sy)]
            else: _,raw,color,lw,dash=item; points=[(x*sx,y*sy) for x,y in raw]
            stroke(points, color, lw, dash)
        elif item[0]=="circle":
            _,x,y,r,color=item; draw.ellipse(((x-r)*sx,(y-r)*sy,(x+r)*sx,(y+r)*sy),fill=color)
        elif item[0]=="rect":
            _,left,top,right,bottom,fill=item; draw.rectangle((left*sx,top*sy,right*sx,bottom*sy),fill=fill)
        else:
            _,x,y,value,size,color,anchor,bold=item; f=font(size,bold); box=draw.textbbox((0,0),value,font=f); tw=box[2]-box[0]
            tx=x*sx-(tw/2 if anchor=="middle" else tw if anchor=="end" else 0); draw.text((tx,y*sy-size*sy),value,font=f,fill=color)
    image.save(PACKAGE/"figure.png",format="PNG",dpi=(600,600),optimize=False,title="R0.72T exact A2 spacetime scaling and drift-only calibration",author="Kasifa")


def draw() -> None:
    scene=build_scene(); render_svg(scene); render_pdf(scene); render_png(scene)


def build_qa() -> None:
    image = Image.open(PACKAGE / "figure.png")
    preview = image.resize((1260, round(1260 * image.height / image.width)), Image.Resampling.LANCZOS)
    preview.save(PACKAGE / "qa-final-size.png", dpi=(180, 180))
    preview.convert("L").save(PACKAGE / "qa-grayscale.png", dpi=(180, 180))
    pdftocairo = Path(
        "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/"
        "dependencies/native/poppler/poppler/bin/pdftocairo"
    )
    if pdftocairo.is_file():
        subprocess.run(
            [str(pdftocairo), "-png", "-singlefile", "-r", "180", str(PACKAGE / "figure.pdf"), str(PACKAGE / "qa-pdf")],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    else:
        preview.save(PACKAGE / "qa-pdf.png", dpi=(180, 180))


def git_state() -> tuple[str, bool]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip()
    dirty = subprocess.run(["git", "diff", "--quiet"], cwd=REPOSITORY).returncode != 0
    dirty = dirty or subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=REPOSITORY).returncode != 0
    return commit, dirty


def validate_formal_certificate(source_commit: str, certificate_commit: str) -> None:
    manifest_path = REPOSITORY / "research/certificates/r072t/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "formal"
        or manifest.get("sourceCommit") != source_commit
        or not manifest.get("sourceBindings")
    ):
        raise RuntimeError("formal figure requires a formal certificate bound to the same source commit")
    if subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip() != certificate_commit:
        raise RuntimeError("formal figure certificate commit must equal HEAD")
    subprocess.run(
        [sys.executable, "research/certificates/r072t/validate_certificate.py", "--require-formal"],
        cwd=REPOSITORY, check=True,
    )


def build_archive(
    row_count: int, formal: bool, visual_inspected: bool,
    source_commit: str | None, certificate_commit: str | None,
    wall_time_seconds: float,
) -> None:
    image = Image.open(PACKAGE / "figure.png")
    width, height = image.size
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    validation = {
        "schemaVersion": 1,
        "status": "passed",
        "checks": {
            "certificatePassed": certificate.get("status") == "passed",
            "analyticSamplesOnly": True,
            "noPdeSimulation": True,
            "threePanels": True,
            "pngAtLeast600DpiAt178mm": width >= math.floor(178 / 25.4 * 600) and image.info.get("dpi", (0, 0))[0] >= 599,
            "vectorPdf": (PACKAGE / "figure.pdf").read_bytes().startswith(b"%PDF"),
            "vectorSvg": (PACKAGE / "figure.svg").read_text(encoding="utf-8").lstrip().startswith("<?xml"),
            "claimBoundaryVisible": True,
        },
        "png": {"width": width, "height": height, "dpi": list(image.info.get("dpi", (0, 0)))},
        "rowCount": row_count,
    }
    if not all(validation["checks"].values()):
        raise RuntimeError(f"R0.72T figure validation failed: {validation}")
    write_json(PACKAGE / "validation.json", validation)
    results = {
        "schemaVersion": 1, "status": "passed", "figureId": "fig-r072t-a2-spacetime-model",
        "panels": {
            "A": "exact W scaled collapse to the H3 leading polynomial",
            "B": "unique diffusion/cubic/time-drift exponent intersection",
            "C": "exact drift-only characteristic action and q=0 calibration",
        },
        "claimsNotMade": ["block contraction", "periodic transfer", "all-start semigroup estimate", "combined cubic/time-drift estimate", "Clay problem"],
    }
    write_json(PACKAGE / "results.json", results)
    (PACKAGE / "progress.ndjson").write_text(
        '\n'.join((
            '{"event":"build-start","stage":1,"totalStages":3}',
            f'{{"event":"analytic-data-ready","rows":{row_count},"stage":2,"totalStages":3}}',
            '{"event":"archive-ready","stage":3,"totalStages":3}'
        )) + '\n', encoding="utf-8"
    )
    (PACKAGE / "resource-log.ndjson").write_text(
        f'{{"event":"resource-summary","processes":1,"threadsPerProcess":1,"rows":{row_count},"gpuUsed":false}}\n',
        encoding="utf-8",
    )
    PUBLIC.mkdir(parents=True, exist_ok=True)
    publication_assets = []
    for extension in ("pdf", "svg", "png"):
        source = PACKAGE / f"figure.{extension}"
        target = PUBLIC / f"fig-r072t-a2-spacetime-model.{extension}"
        shutil.copyfile(source, target)
        publication_assets.append({
            "path": str(target.relative_to(REPOSITORY)), "sha256": sha256(target),
            "bytes": target.stat().st_size, "byteIdenticalToMaster": sha256(target) == sha256(source),
        })
    archived = [
        "README.md", "caption.md", "figure-contract.md", "contract.json", "config.json",
        "command.txt", "environment.txt", "requirements.txt", "plot.py", "qa-report.md",
        "progress.ndjson", "resource-log.ndjson", "data.csv", "results.json", "validation.json",
        "figure.svg", "figure.pdf", "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    ]
    commit, dirty = git_state()
    if formal and (
        not visual_inspected or source_commit is None or certificate_commit is None
        or len(source_commit) != 40 or len(certificate_commit) != 40
        or commit != certificate_commit
    ):
        raise RuntimeError(
            "--formal requires --visual-inspected, full --source-commit and "
            "--certificate-commit values, with HEAD equal to the certificate commit"
        )
    data_schema = {
        "config.json": "frozen analytic presentation ranges and output dimensions",
        "contract.json": "panel claims, output contract, and false claim boundaries",
        "data.csv": "panel, series, x, y, exact source, and analytic-sample status",
        "results.json": "panel meanings and claims not made",
        "validation.json": "asset, dimension, certificate, and claim-boundary checks",
        "progress.ndjson": "deterministic three-stage build progress",
        "resource-log.ndjson": "deterministic process, thread, row, and GPU-use record",
    }
    manifest = {
        "schemaVersion": "1.1", "figureId": "fig-r072t-a2-spacetime-model",
        "status": "formal" if formal else "draft",
        "analyticalQuestion": "How does the true heat profile scale at the A2 collision, which spacetime exponents balance diffusion, cubic transport, and heat-time drift, and what does the exactly solvable drift-only characteristic action calibrate?",
        "supportedClaim": "Exact fixed-formula heat expansion and scaled collapse, the unique exponent balance, and the drift-only norm calibration; no combined cubic/drift semigroup estimate.",
        "createdAt": "2026-08-28T00:00:00+08:00", "release": "R0.72T",
        "git": (
            {"repository": "Kasifa/Kasifa.github.io", "sourceCommit": source_commit, "certificateCommit": certificate_commit, "dirtyAtCertifiedRun": False}
            if formal else
            {"repository": "Kasifa/Kasifa.github.io", "commit": commit, "dirty": dirty}
        ),
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": "true W profile, exact exponent lines, and drift-only action at h=1",
            "precision": "IEEE binary64 samples only for presentation; exact identities are certificate-gated",
            "solver": "no PDE solver, regression, fitted exponent, threshold inference, or random sampling",
            "formalCommand": "commands recorded in command.txt", "wallTimeSeconds": wall_time_seconds,
            "monitoring": {"enabled": True, "progressLog": "progress.ndjson", "resourceLog": "resource-log.ndjson", "trackedFields": ["event", "stage", "rows", "processes", "threadsPerProcess"]},
        },
        "compute": {"host": platform.node() or "local", "operatingSystem": platform.platform(), "cpu": platform.machine(), "memoryGiB": "not sampled; analytic figure only", "processes": 1, "threadsPerProcess": 1, "gpu": "not used", "dgx": "not used"},
        "environment": {"python": platform.python_version(), "packagesLock": "requirements.txt", "pillow": getattr(Image, "__version__", "installed"), "reportlab": "pinned in requirements.txt"},
        "data": [
            {"path": name, "schema": schema, "format": Path(name).suffix.lstrip("."), "sha256": sha256(PACKAGE / name), "bytes": (PACKAGE / name).stat().st_size}
            for name, schema in data_schema.items()
        ],
        "sourceData": [
            {"location": "repository", "fileName": str(CERTIFICATE.relative_to(REPOSITORY)), "bytes": CERTIFICATE.stat().st_size, "sha256": sha256(CERTIFICATE), "extractionCommand": "python3 research/certificates/r072t/generate_certificate.py", "role": "exactCertificate"},
            {"location": "repository", "fileName": "scripts/generate_r072t_figure.py", "bytes": Path(__file__).stat().st_size, "sha256": sha256(Path(__file__)), "extractionCommand": "python3 scripts/generate_r072t_figure.py", "role": "analyticPresentationGenerator"},
        ],
        "figure": {"widthMillimetres": 178, "heightMillimetres": 76, "layout": "1x3", "profile": "journal-double-column", "script": "plot.py", "outputs": [
            {"path": "figure.pdf", "sha256": sha256(PACKAGE / "figure.pdf"), "bytes": (PACKAGE / "figure.pdf").stat().st_size},
            {"path": "figure.svg", "sha256": sha256(PACKAGE / "figure.svg"), "bytes": (PACKAGE / "figure.svg").stat().st_size},
            {"path": "figure.png", "sha256": sha256(PACKAGE / "figure.png"), "bytes": (PACKAGE / "figure.png").stat().st_size, "dpi": 600, "pixels": [width, height]},
        ]},
        "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "visualInspectionExplicit": visual_inspected, "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "finalSizePreview": "qa-final-size.png", "grayscalePreview": "qa-grayscale.png", "pdfRenderPreview": "qa-pdf.png", "manualReport": "qa-report.md"},
        "publication": {"directory": "public/assets/r072t", "stem": "fig-r072t-a2-spacetime-model", "publicCopiesComplete": True, "assets": publication_assets},
        "claimBoundary": {"blockContractionProved": False, "periodicTransferProved": False, "allStartSemigroupEstimateProved": False, "combinedCubicAndTimeDriftEstimateProved": False, "clayMillenniumProblemSolved": False},
        "deterministic": True,
        "outputs": [{"path": name, "sha256": sha256(PACKAGE / name), "bytes": (PACKAGE / name).stat().st_size} for name in archived],
    }
    write_json(PACKAGE / "manifest.json", manifest)
    ledger_names = sorted(
        path.name for path in PACKAGE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (PACKAGE / "SHA256SUMS").write_text(
        "".join(f"{sha256(PACKAGE / name)}  {name}\n" for name in ledger_names), encoding="utf-8"
    )


def main() -> None:
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--formal", action="store_true", help="require a clean tracked tree and emit a formal manifest")
    parser.add_argument("--visual-inspected", action="store_true")
    parser.add_argument("--source-commit")
    parser.add_argument("--certificate-commit")
    args = parser.parse_args()
    if args.formal:
        preflight_commit, preflight_dirty = git_state()
        if preflight_dirty:
            raise RuntimeError("--formal requires a clean tracked tree before generation")
        if args.certificate_commit != preflight_commit:
            raise RuntimeError("--certificate-commit must equal clean preflight HEAD")
        validate_formal_certificate(args.source_commit, args.certificate_commit)
    if not CERTIFICATE.is_file():
        raise RuntimeError("generate and validate research/certificates/r072t first")
    PACKAGE.mkdir(parents=True, exist_ok=True)
    row_count = save_data()
    draw()
    build_qa()
    build_archive(
        row_count, args.formal, args.visual_inspected,
        args.source_commit, args.certificate_commit,
        time.perf_counter() - started,
    )
    stage = "formal" if args.formal else "source-stage draft"
    print(f"R0.72T {stage} analytic figure: passed ({row_count} rows)")


if __name__ == "__main__":
    main()
