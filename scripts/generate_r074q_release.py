#!/usr/bin/env python3
"""Publish the frozen analytic R0.74Q package without changing its mathematics."""

from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.83"
RELEASE = "r074q"
CODE = "R0.74Q"
TITLE = "R0.74Q｜许多壳层同时亮起，为什么仍然压不低支付？"
FROZEN_MANIFEST_SHA256 = "8cb1d3c9089e9694ef753655c8a7e06d69c7e9a3838a35ea3b5f93219b4e4d01"
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


def verify_frozen_package() -> None:
    manifest_path = ROOT / "research/r074q_freeze_manifest.json"
    if sha256(manifest_path) != FROZEN_MANIFEST_SHA256:
        raise RuntimeError("R0.74Q frozen manifest drift")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["completionRule"] = "Each completed research section publishes one note release. Its core transaction publishes the reviewed Chinese HTML and current routes first; local translation and the synchronized note PDF are separate later stages. Formal sealing requires the stated proof or negative result, required certificates, independent audit, accounting and publication gates, plus either a formal figure package or a frozen analytic-release exemption that explicitly declares the figure not applicable and forbids simulation or fabricated figures. A cumulative recap is created only at a declared major milestone; a non-milestone release preserves the previous recap bytes and records published-node and recap-node counts separately."
    for artifact in manifest["artifacts"].values():
        path = ROOT / artifact["path"]
        if path.stat().st_size != artifact["bytes"] or sha256(path) != artifact["sha256"]:
            raise RuntimeError(f"frozen artifact drift: {artifact['path']}")
    claims = manifest["claim_status"]
    if claims["formal_figure"] != "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION":
        raise RuntimeError("R0.74Q formal-figure boundary drift")
    if claims["simulation_or_dns"] != "NOT_USED" or claims["dgx"] != "NOT_USED":
        raise RuntimeError("R0.74Q simulation/DGX boundary drift")


def inline_markup(value: str) -> str:
    value = html.escape(" ".join(value.split()))
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)


def report_body() -> str:
    source = (ROOT / "research/r074q_report-source.md").read_text(encoding="utf-8").strip()
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
            out.append(
                f'<section id="s-{section_index:02d}"><div class="section-no">'
                f'{section_index:02d} / 完整正文</div><h2>{inline_markup(lines[0][3:])}</h2>'
            )
            section_open = True
            continue
        if lines[0].startswith("### "):
            out.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
            continue
        stripped = block.strip()
        if stripped.startswith("\[") and stripped.endswith("\]"):
            out.append(f'<div class="equation">{html.escape(stripped)}</div>')
            continue
        if all(re.match(r"^\d+\.\s", line) or line.startswith("   ") for line in lines):
            items: list[str] = []
            current = ""
            for line in lines:
                match = re.match(r"^\d+\.\s+(.*)", line)
                if match:
                    if current:
                        items.append(current)
                    current = match.group(1)
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
<title>{TITLE}</title><meta name="description" content="有效壳层归约、共同剪切多包压力测试与真实三次支付阻断；固定尺度不等式仍开放">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74q.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\(","\\)"]],displayMath:[["\\[","\\]"]],macros:{{fint:"\\mathop{{\\unicode{{x2A0F}}}}\\limits"}}}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}}.top{{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}.top a{{font-weight:700;text-decoration:none}}main{{width:min(940px,90vw);margin:auto}}.hero{{padding:54px 0 30px;border-bottom:1px solid var(--line)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}}h1{{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}}h2{{margin:2.5rem 0 1rem;color:var(--rule);font-size:1.55rem}}h3{{margin:1.7rem 0 .65rem;font-size:1.16rem}}.stamp,.section-no,.label{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}}.stamp{{border:1px solid var(--line);padding:1rem;background:var(--raised)}}article{{padding:14px 0 72px}}section{{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}}p,li{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}}.labels{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}.label{{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}}a{{color:var(--rule)}}.files{{line-height:2}}.note{{color:var(--muted);font-size:.94rem}}@media(max-width:720px){{body{{font-size:15px}}.hero-inner{{grid-template-columns:1fr}}main,article,section{{min-width:0}}.top{{font-size:13px}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}.top{{display:none}}body{{background:#fff;font-size:9.3pt;line-height:1.5}}main{{width:auto}}.hero{{padding-top:0}}.hero-inner{{grid-template-columns:1fr 220px}}h2{{margin:1.7rem 0 .6rem}}a{{color:inherit;text-decoration:none}}.equation,.stamp{{break-inside:avoid}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74Q · 2026-09-02</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74Q · 完整中文版本</div><h1>{TITLE}</h1><p>我证明了 terminal effective-shell best-\(N\) 归约，并在共同剪切的光滑精确族上完成 growing finite multipacket 压力测试。equal-target 架构能同时点亮许多目标壳层，却被最外 lobe 的真实非负三次支付阻断；这不证明固定尺度不等式。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">CONDITIONAL</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74Q</strong><p>有效壳层归约：PROVED</p><p>共同剪切精确族：PROVED / PRIOR STRUCTURE</p><p>all-lobe dominance：PROVED</p><p>三次支付阻断：PROVED</p><p>signed flux 与完整 \(Y_2\)：OPEN</p><p>正式图件：NOT APPLICABLE</p><p>纯解析 / 无仿真 / NO DGX</p></div></div></header><article>
{report_body()}
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>解析主文、双证书与独立审计</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074q_problem_freeze.md">问题冻结</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074q_common_shear_multipacket_gate.md">共同剪切门</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074q_relaxed_multipacket_cubic_obstruction.md">放松多包与三次支付</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074q_common_shear_gate_certificate.py">共同剪切证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074q_relaxed_multipacket_certificate.py">放松族证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074q_primary_literature_boundary.md">文献边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074q_gap_matrix.md">证据与缺口矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074q_report-source.md">完整中文 reader source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074q_freeze_manifest.json">冻结清单</a></p><p><a href="/notes/r0-74q.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74o.html">上一大里程碑 recap（截止 R0.74O，157 节）</a> · <a href="/recap-r0-61-r0-74o.pdf">recap PDF</a></p><p class="note">本节纯解析，没有 Navier--Stokes 数值仿真、DNS、DGX 或正式图件。</p></section>
<section id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74R</h2><p>从 convex cubic payment 反推一般有效壳层 packing，同时独立处理 signed flux、完整 \(Y_2\) 与非 equal-target 振幅优化。</p></section></article></main></body></html>'''


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    replacements = (
        ('data-site-version="1.82"', 'data-site-version="1.83"', "home version"),
        ('/i18n-en.js?v=1.82', '/i18n-en.js?v=1.83', "home i18n"),
        ('/site-refresh.js?v=1.82.1', '/site-refresh.js?v=1.83.1', "home refresh"),
        ('<strong>v1.82</strong>网页版本', '<strong>v1.83</strong>网页版本', "home stat version"),
        ('<span><strong>218</strong>公开研究笔记</span>', '<span><strong>219</strong>公开研究笔记</span>', "home notes"),
        ('<span><strong>R0.74P</strong>最新研究节点</span>', '<span><strong>R0.74Q</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74P', 'Research topology · R0.1–R0.74Q', "topology"),
        ('href="#r074p">跳到首页 R0.74P 卡片 →', 'href="#r074q">跳到首页 R0.74Q 卡片 →', "jump"),
        ('href="#r070a">R0.70A–R0.74P：120 节已公开，96 节完整封存', 'href="#r070a">R0.70A–R0.74Q：121 节已公开，96 节完整封存', "progress"),
        ('<span class="route-range">R0.69P–R0.74P</span>', '<span class="route-range">R0.69P–R0.74Q</span>', "range"),
        ('<h3>R0.74P：时间可观测量筛选与匹配时钟边界</h3>', '<h3>R0.74Q：有效壳层归约与三次支付阻断</h3>', "route title"),
        ('<p class="tree-path"><span>R0.72R–R0.74P：</span>', '<p class="tree-path"><span>R0.72R–R0.74Q：</span>', "path range"),
        ('aria-label="R0.69P–R0.74P"', 'aria-label="R0.69P–R0.74Q"', "aria"),
        ('<summary>展开 128 篇公开笔记</summary>', '<summary>展开 129 篇公开笔记</summary>', "route count"),
        ('综述 v1.82 · 2026-09-02', '综述 v1.83 · 2026-09-02', "footer"),
        ('全站现有 218 篇公开研究笔记', '全站现有 219 篇公开研究笔记', "recap count"),
    )
    for old, new, label in replacements:
        page = replace_once_or_present(page, old, new, label)
    focus = '<div class="summary-item"><strong>我目前关注</strong><span>R0.74Q 已把多壳层压力测试拆成有效壳层归约、共同剪切几何和真实三次支付三层；equal-target 精确族被凸支付阻断，但 signed flux、完整 Y₂ 上界与一般 packing 仍开放。</span></div>'
    page, count = re.subn(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', focus, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("home focus replacement failed")
    latest = '''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74Q · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74Q｜许多壳层同时亮起，为什么仍然压不低支付？</h2><p class="route-map-intro">有效壳层归约成立；共同剪切多包可以同时点亮目标壳层，但 equal-target 架构被最外真实三次支付阻断。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74q.pdf">阅读最新 R0.74Q 研究笔记 →</a><a href="/recap-r0-61-r0-74o.html">最新大里程碑 recap（R0.61–R0.74O，157 节）</a><a href="/notes/">219 篇研究笔记总索引</a><a href="#r074q">查看首页 R0.74Q 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74Q · 121 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>96 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74Q</span></div></div></section>'''
    page, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")
    page = replace_once_or_present(page, '<a class="milestone" href="/notes/r0-74p.html">R0.74P</a>', '<a class="milestone" href="/notes/r0-74p.html">R0.74P</a>\n<a class="milestone" href="/notes/r0-74q.html">R0.74Q</a>', "milestone")
    old_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74Q</span><span class="tree-state current">下一检查点</span></div><h3>R0.74Q 下一接口</h3><p>证明或否定逐壳层 ℓ1 通量向匹配 ℓ2 时钟的 PDE 压缩，并检验预定中心尺度装箱。</p></article></div>'
    new_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74R</span><span class="tree-state current">下一检查点</span></div><h3>R0.74R 下一接口</h3><p>从 convex cubic payment 反推一般有效壳层 packing，并独立处理 signed flux、完整 Y₂ 与非 equal-target 振幅优化。</p></article></div>'
    page = replace_once_or_present(page, old_next, new_next, "next route")
    page = replace_once_or_present(page, 'temporal-observable triage / defect-completed shell clock / matched-square-function boundary</p>', 'temporal-observable triage / defect-completed shell clock / matched-square-function boundary → effective-shell reduction / common-shear multipacket stress test / cubic-payment obstruction</p>', "path tail")
    card = '''          <div class="task-one" id="r074q" data-release="r074q" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74Q · 2026-09-02</p><h3>R0.74Q｜许多壳层同时亮起，为什么仍然压不低支付？</h3><p>有效壳层归约成立；共同剪切多包可以同时点亮目标壳层，但 equal-target 架构被最外真实三次支付阻断。</p><p><a href="/notes/r0-74q.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74q.pdf">PDF</a></p></div>\n'''
    anchor = '          <div class="task-one" id="r074p"'
    if anchor not in page:
        raise RuntimeError("home P card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.82"', 'data-site-version="1.83"', "lit version"),
        ('/i18n-en.js?v=1.82', '/i18n-en.js?v=1.83', "lit i18n"),
        ('R0.69P–R0.74P 只列为研究笔记', 'R0.69P–R0.74Q 只列为研究笔记', "lit range"),
        ('文献综述 v1.82 · 2026-09-02', '文献综述 v1.83 · 2026-09-02', "lit footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    old = '<div class="route-step pause"><header><b>开放接口 · R0.74Q</b><strong>ℓ1 到匹配 ℓ2 的 PDE 压缩</strong></header><p>有效壳层、持续时间、尺度装箱与预定中心的收缩迭代仍开放。</p></div>'
    new = '<div class="route-step kept"><header><b>R0.74Q</b><strong>有效壳层归约与三次支付阻断</strong></header><p>terminal best-N 归约成立；共同剪切精确多包与 all-lobe dominance 通过，但 canonical equal-target 族被最外真实 velocity-cubic payment 阻断。signed flux、完整 Y₂ 上界和一般 packing 仍开放。<a href="/notes/r0-74q.html">研究笔记</a> <a href="/recap-r0-61-r0-74o.html">最新里程碑 recap</a> <a href="#r074q-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74R</b><strong>从 convex payment 到一般 packing</strong></header><p>一般有效壳层 packing、非 equal-target 优化、signed flux 与完整 Y₂ 仍开放。</p></div>'
    page = replace_once_or_present(page, old, new, "literature route")
    boundary = '<h3 id="r074q-boundary">R0.74Q 的文献与主张边界</h3><p>有界十四篇一手来源筛查覆盖 2D3C、共同标量叠加、被动标量、频率局部正则、determining modes 与物理尺度通量。2D3C 和共同线性标量方程的叠加机制是既有结构，不能作为新颖性主张；有限未命中也不证明新颖性、优先权或可发表性。</p><div class="boundary"><strong>R0.74Q 的公开边界</strong><p>PROVED、INHERITED、FINITE、CONDITIONAL、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 分开。signed cumulative flux、完整平方函数上界、固定尺度不等式、正则性与奇点仍开放。<a href="/notes/r0-74q.html">阅读完整中文笔记</a>。</p></div>\n'
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
    if not (PUBLIC / "notes/r0-74q.pdf").exists():
        pdf_count += 1
    post_r060 = route_post_r060_count(HOME.read_text(encoding="utf-8"))
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {"schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE, "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "latestRecapRelease": "R0.74O", "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-02"})
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if RELEASE not in inventory["publishedReleases"]:
        inventory["publishedReleases"].append(RELEASE)
    exempt = inventory.setdefault("formalFigureExemptReleases", [])
    if RELEASE not in exempt:
        exempt.append(RELEASE)
    inventory["definitions"]["formalFigureExempt"] = "The release is published, the frozen research manifest declares that a formal figure is not applicable, and the publication contains no simulation or fabricated figure package."
    inventory["latestPublishedRelease"] = RELEASE
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    inventory["formalFigureExemptReleaseCount"] = len(exempt)
    write_json(inventory_path, inventory)
    manifest_path = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({"latestCompletedRelease": RELEASE, "siteVersion": VERSION, "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "nextRelease": "r074r", "latestReleaseGate": "tests/r074q-effective-shell-gate.test.mjs", "latestReleasePublicationTest": "tests/r074q-release.test.mjs", "postR070APublishedReleaseCount": inventory["publishedReleaseCount"], "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"], "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"], "latestRecapRelease": "r074o", "latestRecapHtml": "/recap-r0-61-r0-74o.html", "latestRecapPdf": "/recap-r0-61-r0-74o.pdf", "latestReleaseTranslationScript": "scripts/add-r074q-translations.mjs", "latestReleasePdfBinder": "scripts/bind-r074q-pdf.mjs", "recapPolicy": "MILESTONE_ONLY"})
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    verify_frozen_package()
    assert_recap()
    write_text(PUBLIC / "notes/r0-74q.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
    assert_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "formalFigure": "NOT_APPLICABLE", "simulation": False, "dgxUsed": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
