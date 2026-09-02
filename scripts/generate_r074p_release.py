#!/usr/bin/env python3
"""Publish the frozen R0.74P package without changing its mathematics."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.82"
RELEASE = "r074p"
CODE = "R0.74P"
FIGURE_DIR = "fig-r074p-observable-triage"
TITLE = "R0.74P｜哪些时间可观测量真正看见了缺失的尺度？"
FROZEN_CORE = "3306812e962fc0e2fecc227d0ffea6ae062c91f2"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-74o.html": "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2",
    PUBLIC / "recap-r0-61-r0-74o.pdf": "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once_or_present(value: str, old: str, new: str, label: str) -> str:
    if new in value:
        return value
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_recap() -> None:
    for path, expected in RECAP_HASHES.items():
        if sha256(path) != expected:
            raise RuntimeError(f"protected recap drift: {path.relative_to(ROOT)}")


def record(path: Path, schema: str) -> dict[str, object]:
    return {"path": path.name, "schema": schema, "bytes": path.stat().st_size, "sha256": sha256(path)}


def copy_figures() -> None:
    source = ROOT / "research/figures/r074p" / FIGURE_DIR
    public_mirror = PUBLIC / "figures/r074p" / FIGURE_DIR
    archive = ROOT / "figures/r074p" / FIGURE_DIR
    for target in (public_mirror, archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
    assets = PUBLIC / "assets/r074p"
    assets.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{ext}", assets / f"{FIGURE_DIR}.{ext}")

    frozen_manifest = source / "manifest.json"
    frozen = json.loads(frozen_manifest.read_text(encoding="utf-8"))
    outputs = []
    for ext in ("svg", "pdf", "png"):
        item = record(archive / f"figure.{ext}", f"{ext}-journal-master")
        if ext == "png":
            item["dpi"] = 600
        outputs.append(item)
    wrapper = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r074p-publication-compat-v1",
        "figureId": frozen["figure_id"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication wrapper for the frozen temporal-observable triage figure.",
        "supportedClaim": "The positive-order window misses the target scale; the target shell clock detects it; the complete matched square-function upper bound remains open.",
        "createdAt": "2026-09-02T00:00:00Z",
        "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": FROZEN_CORE, "dirty": False},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json", "precision": "frozen exact or deterministic package", "solver": "none", "formalCommand": "use command.txt and validate.py", "wallTimeSeconds": 1.0, "monitoring": {"enabled": False}},
        "compute": {"host": "local workstation (hostname omitted)", "operatingSystem": "macOS arm64", "cpu": "arm64 / local CPU", "memoryGiB": 36.0, "processes": 1, "threadsPerProcess": 1},
        "environment": {"python": "3.12.13", "packagesLock": "requirements.txt"},
        "data": [record(archive / "source-data.csv", "r074p-source-data-v1")],
        "sourceData": [],
        "figure": {"widthMillimetres": 178.0, "heightMillimetres": 100.0, "outputs": outputs},
        "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": {"positiveOrderWindowNoGo": "PROVED", "defectCompletedClock": "PROVED", "targetShellTwoSidedScale": "PROVED", "completeMatchedSquareFunctionUpperBound": "OPEN", "fixedScaleSuitableWeakStability": "PROVED", "globalRegularity": False, "notClay": True},
        "publication": {
            "archiveDirectory": f"public/figures/{RELEASE}/{FIGURE_DIR}",
            "researchArchiveDirectory": f"research/figures/{RELEASE}/{FIGURE_DIR}",
            "directory": f"public/assets/{RELEASE}",
            "fileStem": FIGURE_DIR,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "releaseSourceCommit": FROZEN_CORE,
            "figurePackageCommit": FROZEN_CORE,
            "assets": [{"path": f"public/assets/{RELEASE}/{FIGURE_DIR}.{item['path'].split('.')[-1]}", "bytes": item["bytes"], "sha256": item["sha256"]} for item in outputs],
        },
        "provenance": {"frozenResearchManifestSha256": sha256(frozen_manifest), "compatibilityScope": "publication metadata only; frozen scientific assets are unchanged"},
    }
    write_json(archive / "manifest.json", wrapper)
    names = sorted(p.name for p in archive.iterdir() if p.is_file() and p.name not in {"SHA256SUMS", ".DS_Store"})
    write_text(archive / "SHA256SUMS", "".join(f"{sha256(archive / name)}  {name}\n" for name in names))


def inline_markup(value: str) -> str:
    value = html.escape(" ".join(value.split()))
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    return value


def report_body() -> str:
    source = (ROOT / "research/r074p_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    out: list[str] = []
    section_open = False
    section_index = 0
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                out.append("</section>")
            section_index += 1
            heading = inline_markup(lines[0][3:])
            out.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{heading}</h2>')
            section_open = True
            continue
        stripped = block.strip()
        if stripped.startswith("\\[") and stripped.endswith("\\]"):
            out.append(f'<div class="equation">{html.escape(stripped)}</div>')
            continue
        if all(re.match(r"^\d+\.\s", line) or line.startswith("   ") for line in lines):
            items: list[str] = []
            current = ""
            for line in lines:
                m = re.match(r"^\d+\.\s+(.*)", line)
                if m:
                    if current:
                        items.append(current)
                    current = m.group(1)
                else:
                    current += " " + line.strip()
            if current:
                items.append(current)
            out.append("<ol>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ol>")
            continue
        if all(line.startswith("- ") or line.startswith("  ") for line in lines):
            items: list[str] = []
            current = ""
            for line in lines:
                if line.startswith("- "):
                    if current:
                        items.append(current)
                    current = line[2:]
                else:
                    current += " " + line.strip()
            if current:
                items.append(current)
            out.append("<ul>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ul>")
            continue
        out.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        out.append("</section>")
    return "\n".join(out)


def render_note() -> str:
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title><meta name="description" content="正阶窗口、能量振荡与缺陷补全壳层时钟的严格筛选；目标壳可检出，完整匹配平方函数上界仍开放">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74p.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]],macros:{{fint:"\\\\mathop{{\\\\unicode{{x2A0F}}}}\\\\limits"}}}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}}.top{{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}.top a{{font-weight:700;text-decoration:none}}main{{width:min(940px,90vw);margin:auto}}.hero{{padding:54px 0 30px;border-bottom:1px solid var(--line)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}}h1{{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}}h2{{margin:2.5rem 0 1rem;color:var(--rule);font-size:1.55rem}}.stamp,.section-no,.label{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}}.stamp{{border:1px solid var(--line);padding:1rem;background:var(--raised)}}article{{padding:14px 0 72px}}section{{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}}p,li{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}}.labels{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}.label{{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}}a{{color:var(--rule)}}img{{max-width:100%;height:auto}}.files{{line-height:2}}.figure-note{{color:var(--muted);font-size:.94rem}}@media(max-width:720px){{body{{font-size:15px}}.hero-inner{{grid-template-columns:1fr}}main,article,section{{min-width:0}}.top{{font-size:13px}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}.top{{display:none}}body{{background:#fff;font-size:9.3pt;line-height:1.5}}main{{width:auto}}.hero{{padding-top:0}}.hero-inner{{grid-template-columns:1fr 220px}}h2{{margin:1.7rem 0 .6rem}}a{{color:inherit;text-decoration:none}}.equation,.stamp{{break-inside:avoid}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74P · 2026-09-02</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74P · 完整中文版本</div><h1>{TITLE}</h1><p>我筛选了正阶时间窗口、能量振荡与缺陷补全壳层时钟。固定正阶窗口严格漏掉目标尺度；能量振荡只是端点的重包装；缺陷补全时钟通过目标壳检出与固定尺度适合弱解稳定性两道门槛，但完整匹配平方函数上界仍然 <strong>OPEN</strong>。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74P</strong><p>正阶窗口漏检：PROVED NO-GO</p><p>缺陷补全时钟：PROVED</p><p>目标壳双边尺度：PROVED</p><p>完整 \(Y_2\) 上界：OPEN</p><p>证书 52/52：FINITE</p><p>图件 20/20：FINITE</p><p>LOCAL DIRECT / NO DGX</p></div></div></header><article>
{report_body()}
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>三个候选时间可观测量的严格筛选</h2><picture><source srcset="/assets/r074p/{FIGURE_DIR}.svg" type="image/svg+xml"><img src="/assets/r074p/{FIGURE_DIR}.png" alt="R0.74P temporal observable triage"></picture><p><a href="/assets/r074p/{FIGURE_DIR}.pdf">下载矢量 PDF</a> · <a href="/assets/r074p/{FIGURE_DIR}.png">下载 600 dpi PNG</a> · <a href="/assets/r074p/{FIGURE_DIR}.svg">打开 SVG</a> · <a href="/figures/r074p/{FIGURE_DIR}/source-data.csv">source-data.csv</a></p><p><a href="/figures/r074p/{FIGURE_DIR}/caption.md">图注</a> · <a href="/figures/r074p/{FIGURE_DIR}/qa-report.md">图件 QA</a> · <a href="/figures/r074p/{FIGURE_DIR}/plot.py">绘图源码</a> · <a href="/figures/r074p/{FIGURE_DIR}/validate.py">验证器</a> · <a href="/figures/r074p/{FIGURE_DIR}/validation.json">20 项验证记录</a> · <a href="/figures/r074p/{FIGURE_DIR}/manifest.json">manifest</a> · <a href="/figures/r074p/{FIGURE_DIR}/SHA256SUMS">校验和</a></p><p class="figure-note">确定性解析图，不是 DNS、仿真、奇点或正则性证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>完整主文、双实现证书、独立审计与图包</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_problem_freeze.md">问题冻结</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_temporal_observable_triage.md">解析主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_main_independent_audit.md">独立审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074p_temporal_clock_certificate.py">Python 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074p_temporal_clock_certificate_independent.rb">独立 Ruby 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_temporal_clock_certificate.json">冻结 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_primary_literature_boundary.md">文献边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_gap_matrix.md">证据与缺口矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_bilingual_dictionary.md">双语词典</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_report-source.md">完整中文 reader source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074p_freeze_manifest.json">冻结清单</a></p><p><a href="/notes/r0-74p.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74o.html">上一大里程碑 recap（截止 R0.74O，157 节）</a> · <a href="/recap-r0-61-r0-74o.pdf">recap PDF</a></p></section>
<section id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74Q</h2><p>证明或否定逐壳层 \(\ell^1\) 通量账本向匹配 \(\ell^2\) 时钟的 PDE 压缩，并检验预定中心与尺度装箱。</p></section></article></main></body></html>'''


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.81"', 'data-site-version="1.82"', "home version"),
        ('/i18n-en.js?v=1.81', '/i18n-en.js?v=1.82', "home i18n"),
        ('/site-refresh.js?v=1.81.1', '/site-refresh.js?v=1.82.1', "home refresh"),
        ('<strong>v1.81</strong>网页版本', '<strong>v1.82</strong>网页版本', "home stat version"),
        ('<span><strong>217</strong>公开研究笔记</span>', '<span><strong>218</strong>公开研究笔记</span>', "home notes"),
        ('<span><strong>R0.74O</strong>最新研究节点</span>', '<span><strong>R0.74P</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74O', 'Research topology · R0.1–R0.74P', "topology"),
        ('href="#r074o">跳到首页 R0.74O 卡片 →', 'href="#r074p">跳到首页 R0.74P 卡片 →', "jump"),
        ('href="#r070a">R0.70A–R0.74O：119 节已公开，95 节完整封存', 'href="#r070a">R0.70A–R0.74P：120 节已公开，96 节完整封存', "progress"),
        ('<span class="route-range">R0.69P–R0.74O</span>', '<span class="route-range">R0.69P–R0.74P</span>', "range"),
        ('<h3>R0.74O：自由振幅否定标量平方根对数端点</h3>', '<h3>R0.74P：时间可观测量筛选与匹配时钟边界</h3>', "route title"),
        ('<p class="tree-path"><span>R0.72R–R0.74O：</span>', '<p class="tree-path"><span>R0.72R–R0.74P：</span>', "path range"),
        ('aria-label="R0.69P–R0.74O"', 'aria-label="R0.69P–R0.74P"', "aria"),
        ('<summary>展开 127 篇公开笔记</summary>', '<summary>展开 128 篇公开笔记</summary>', "route count"),
        ('综述 v1.81 · 2026-09-02', '综述 v1.82 · 2026-09-02', "footer"),
        ('全站现有 217 篇公开研究笔记', '全站现有 218 篇公开研究笔记', "recap count only"),
    ):
        page = replace_once_or_present(page, old, new, label)
    page, count = re.subn(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74P 已排除固定正阶时间窗口，确认能量振荡只是端点重包装，并把缺口缩成逐壳层 ℓ1 通量向匹配 ℓ2 时钟的 PDE 压缩；完整平方函数上界、尺度装箱与 Clay 仍开放。</span></div>', page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("home focus replacement failed")
    latest = '''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74P · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74P｜哪些时间可观测量真正看见了缺失的尺度？</h2><p class="route-map-intro">固定正阶窗口漏检，能量振荡重建端点；缺陷补全时钟能看见目标壳，但完整匹配平方函数上界仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74p.pdf">阅读最新 R0.74P 研究笔记 →</a><a href="/recap-r0-61-r0-74o.html">最新大里程碑 recap（R0.61–R0.74O，157 节）</a><a href="/notes/">218 篇研究笔记总索引</a><a href="#r074p">查看首页 R0.74P 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74P · 120 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>96 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74P</span></div></div></section>'''
    page, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")
    page = replace_once_or_present(page, '<a class="milestone" href="/notes/r0-74o.html">R0.74O</a>', '<a class="milestone" href="/notes/r0-74o.html">R0.74O</a>\n<a class="milestone" href="/notes/r0-74p.html">R0.74P</a>', "milestone")
    old_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74P</span><span class="tree-state current">下一检查点</span></div><h3>R0.74P 下一接口</h3><p>冻结一个能看见二次被动振幅、尺度临界、非循环并可弱稳定传递的增广可观测量。</p></article></div>'
    new_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74Q</span><span class="tree-state current">下一检查点</span></div><h3>R0.74Q 下一接口</h3><p>证明或否定逐壳层 ℓ1 通量向匹配 ℓ2 时钟的 PDE 压缩，并检验预定中心尺度装箱。</p></article></div>'
    page = replace_once_or_present(page, old_next, new_next, "next route")
    page = replace_once_or_present(page, 'all-shell synthesis / exact-family matching endpoint law → passive-amplitude scalar endpoint no-go</p>', 'all-shell synthesis / exact-family matching endpoint law → passive-amplitude scalar endpoint no-go → temporal-observable triage / defect-completed shell clock / matched-square-function boundary</p>', "path tail")
    card = '''          <div class="task-one" id="r074p" data-release="r074p" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74P · 2026-09-02</p><h3>R0.74P｜哪些时间可观测量真正看见了缺失的尺度？</h3><p>固定正阶窗口漏检，能量振荡重建端点；缺陷补全时钟能看见目标壳，但完整匹配平方函数上界仍开放。</p><p><a href="/notes/r0-74p.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74p.pdf">PDF</a> · <a href="/assets/r074p/fig-r074p-observable-triage.pdf">附图</a></p></div>\n'''
    anchor = '          <div class="task-one" id="r074o"'
    if anchor not in page:
        raise RuntimeError("home O card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.81"', 'data-site-version="1.82"', "lit version"),
        ('/i18n-en.js?v=1.81', '/i18n-en.js?v=1.82', "lit i18n"),
        ('R0.69P–R0.74O 只列为研究笔记', 'R0.69P–R0.74P 只列为研究笔记', "lit range"),
        ('文献综述 v1.81 · 2026-09-02', '文献综述 v1.82 · 2026-09-02', "lit footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    old = '<div class="route-step pause"><header><b>开放接口 · R0.74P</b><strong>增广可观测量与弱稳定接口</strong></header><p>需要一个能看见二次被动振幅、尺度临界、非循环并可传到 suitable weak 极限的独立结构量。</p></div>'
    new = '<div class="route-step kept"><header><b>R0.74P</b><strong>时间可观测量筛选与匹配时钟边界</strong></header><p>固定正阶窗口严格漏检；能量振荡重建端点；缺陷补全时钟在固定尺度适合弱解极限下稳定，目标壳达到目标尺度，完整匹配平方函数上界仍开放。<a href="/notes/r0-74p.html">研究笔记</a> <a href="/recap-r0-61-r0-74o.html">最新里程碑 recap</a> <a href="#r074p-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74Q</b><strong>ℓ1 到匹配 ℓ2 的 PDE 压缩</strong></header><p>有效壳层、持续时间、尺度装箱与预定中心的收缩迭代仍开放。</p></div>'
    page = replace_once_or_present(page, old, new, "literature route")
    boundary = '<h3 id="r074p-boundary">R0.74P 的文献与主张边界</h3><p>有界八篇一手来源检索覆盖适合弱解、局部耗散、移动圆柱、固定物理壳层通量、空间正则区间与 quantitative regularity epochs；Yu 2026 是移动窗口与尺度缺陷账本的相邻预印本。没有来源被用来替代本节的壳层时钟证明。有限未命中不证明新颖性、优先权、检索完备性或可发表性。</p><div class="boundary"><strong>R0.74P 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 分开。完整匹配平方函数上界、PDE 压缩、尺度装箱、收缩迭代和任意三维正则性仍开放。<a href="/notes/r0-74p.html">阅读完整中文笔记</a>。</p></div>\n'
    anchor = '        <section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def route_post_r060_count(page: str) -> int:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    slugs = re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end])
    return len(slugs) - slugs.index("r0-61")


def update_accounting() -> None:
    html_count = len(list((PUBLIC / "notes").glob("r0-*.html")))
    pdf_count = len(list((PUBLIC / "notes").glob("r0-*.pdf")))
    if not (PUBLIC / "notes/r0-74p.pdf").exists():
        pdf_count += 1
    post_r060 = route_post_r060_count(HOME.read_text(encoding="utf-8"))
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {"schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE, "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "latestRecapRelease": "R0.74O", "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-02"})
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if RELEASE not in inventory[key]:
            inventory[key].append(RELEASE)
    inventory["latestPublishedRelease"] = RELEASE
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    write_json(inventory_path, inventory)
    manifest_path = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({"latestCompletedRelease": RELEASE, "siteVersion": VERSION, "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "nextRelease": "r074q", "latestReleaseGate": "tests/r074p-temporal-observable-gate.test.mjs", "latestReleasePublicationTest": "tests/r074p-release.test.mjs", "postR070APublishedReleaseCount": inventory["publishedReleaseCount"], "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"], "latestRecapRelease": "r074o", "latestRecapHtml": "/recap-r0-61-r0-74o.html", "latestRecapPdf": "/recap-r0-61-r0-74o.pdf", "latestReleaseTranslationScript": "scripts/add-r074p-translations.mjs", "latestReleasePdfBinder": "scripts/bind-r074p-pdf.mjs", "recapPolicy": "MILESTONE_ONLY"})
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74p.html", render_note())
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74p.html", render_note())
    if sha256(ROOT / "research/r074p_bilingual_dictionary.md") != "dab3258d619655de4efde7a4ac6f0488d5fc2693a92b9ade49446164dfa8c2ca":
        raise RuntimeError("frozen bilingual dictionary drift")
    update_home()
    update_literature()
    update_accounting()
    assert_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "translationRoute": "LOCAL_DIRECT_NO_DGX"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
