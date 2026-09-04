#!/usr/bin/env python3
"""Publish frozen R0.76K Step 62 from the verified R0.76J baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076j_step61_release as previous
import import_r076k_step62_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "4958433a93f12f4f8a8c9df2a5c0503193c282f9"
VERSION = "2.41"
RELEASE = "r076k"
CODE = "R0.76K"
TITLE = "R0.76K｜实单频带 edge 下界、exact heat-shear 与 signed-cap 单切片"
RECAP_SLUG = "recap-r0-61-r0-76i"
RECAP_HASHES = {
    PUBLIC / f"{RECAP_SLUG}.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
    PUBLIC / f"{RECAP_SLUG}.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
    PUBLIC / "recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
    PUBLIC / "recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
inline_markup = previous.inline_markup


def baseline_text(relative: str) -> str:
    return subprocess.check_output(["git", "show", f"{BASELINE_COMMIT}:{relative}"], cwd=ROOT, text=True)


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected milestone recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.76K frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r076k_real_dyadic_edge_sharpness_certificate.json").read_text())
    if (certificate.get("status") != "PASS" or certificate.get("verdict") != "PASS"
            or certificate.get("assertionsPassed") != 118 or certificate.get("assertionsTotal") != 118
            or certificate.get("freezeReady") is not True
            or len(certificate.get("negativeMutations", [])) != 118):
        raise RuntimeError("R0.76K certificate verdict drift")
    main = (ROOT / "research/r076k_real_dyadic_edge_sharpness.md").read_text()
    compact = " ".join(main.split())
    for token in (
        r"\tag{K.1}", r"\tag{K.24}", r"\tag{K.35}", r"\tag{K.48}",
        r"\frac1{2\sqrt2}", r"\frac d{128}", r"\frac q{\sqrt2}",
        r"\eta_Lq(L)^27^{q(L)}\longrightarrow0", "q(L)=o(L^2)",
        "A^(3/2)<<m=o(A^2)", "**NOT CLAY.**",
    ):
        if token not in compact:
            raise RuntimeError(f"R0.76K boundary drift: {token}")
    source = (ROOT / "research/r076k_report-source.md").read_text()
    for token in ("Zhang", "Proposition 7.1", "Chen", "DLMF", "q=o(L^2)", "NOT CLAY"):
        if token not in source:
            raise RuntimeError(f"R0.76K source boundary drift: {token}")


def render_sections() -> str:
    source = (ROOT / "research/r076k_real_dyadic_edge_sharpness.md").read_text().strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 488
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            heading = re.sub(r"^\d+\.\s*", "", lines[0][3:])
            output.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{inline_markup(heading)}</h2>')
            section_open = True
            continue
        stripped = block.strip()
        if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
            output.append(f'<div class="equation">{html.escape(stripped)}</div>')
        elif lines[0].startswith("### "):
            output.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
        elif len(lines) >= 2 and lines[0].startswith("|") and re.match(r"^\|[-:| ]+\|$", lines[1]):
            rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
            style = ' style="overflow-wrap:anywhere;word-break:break-word"'
            head = "".join(f"<th{style}>{inline_markup(cell)}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td{style}>{inline_markup(cell)}</td>" for cell in row) + "</tr>" for row in rows[2:])
            output.append(f'<div class="table-wrap"><table style="table-layout:fixed;width:100%"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
        elif all(line.startswith("- ") or line.startswith("  ") for line in lines):
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
            output.append("<ul>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ul>")
        else:
            output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    if section_index != 496:
        raise RuntimeError(f"Step 62 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.40"', 'data-site-version="2.41"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.40", "/i18n-en.js?v=2.41", "note i18n")
    page = replace_pattern(page, r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Real one-dyadic-band edge lower bounds, exact integer heat-shear slice realization, and signed-cap slice algebra; the complete-clock quotient remains open.">', "note metadata")
    page = replace_pattern(page, r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76k.html">', "note canonical")
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76K · STEP 62 · 2026-09-05</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76K · Step 62 · REAL DYADIC EDGE SHARPNESS</div><h1>{TITLE}</h1><p>K 证明 <code>exp(cq√d)</code> 的 edge 尺度与 endpoint 的线性 <code>q</code> 因子已经出现在 real one-dyadic-band cosine packets 中，并把见证精确嵌入任意一个预先指定的 exact integer heat-shear 切片。统一构造覆盖 <code>q=o(L²)</code>，signed two-cap algebra 也在该切片闭合；但完整 <code>q=o(L^(5/2))</code> 下界与 complete-clock signed flux/full-plateau quotient 仍未证明。<strong>PROVED LOCALLY. FIXED SINGLE SLICE ONLY. NOT CLAY.</strong></p><div class="labels"><span class="label">LITERATURE</span><span class="label">PROVED LOCALLY</span><span class="label">FINITE COMPUTATION</span><span class="label">OPEN</span><span class="label">REAL ONE DYADIC BAND</span><span class="label">EXACT HEAT-SHEAR SLICE</span><span class="label">q=o(L²)</span><span class="label">FULL q=o(L^(5/2)) LOWER OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76K STEP 62</strong><p>pointwise：exp((q-1) arcosh(1+d))/(2√2)</p><p>exterior：d exp(2(q-1)√(7d/8))/128</p><p>endpoint：q/√2 in L²</p><p>mode count：q positive cosines = 2q branches</p><p>slice：prescribed (s*,B)</p><p>uniform range：q=o(L²)</p><p>signed cap：single-slice positive pairing</p><p>clock obstruction：exp(cTm²/A²)</p><p>complete signed quotient：OPEN</p><p>L³ endpoint optimality：OPEN</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_sections() + '\n<section id="reproduce">', "Step 62 sections")
    links = " · ".join([
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076k_real_dyadic_edge_sharpness.md">Step 62 主文</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076k_real_dyadic_edge_sharpness_primary_audit.md">primary audit</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076k_report-source.md">source report</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076k_real_dyadic_edge_sharpness_fixtures.json">fixtures JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076k_real_dyadic_edge_sharpness_expected.json">expected JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076k_real_dyadic_edge_sharpness_certificate.json">certificate JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076k_real_dyadic_edge_sharpness_certificate_report.md">Python report</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076k_real_dyadic_edge_sharpness_independent_audit.md">Ruby independent audit</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076k_real_dyadic_edge_sharpness_qa_report.md">certificate QA</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076k_real_dyadic_edge_sharpness_certificate.py">Python script</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076k_real_dyadic_edge_sharpness_certificate_independent.rb">Ruby script</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076k_real_dyadic_edge_sharpness_qa.sh">QA script</a>',
    ])
    evidence = f'''<section id="reproduce"><div class="section-no">K / 冻结证据</div><h2>Step 62 主文、来源边界、双实现证书与 fail-closed QA</h2><p class="files">{links}</p><p><a href="/notes/r0-76k.pdf">同步 reader PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I）</a> · <a href="/{RECAP_SLUG}.pdf">截至 I 的 recap PDF</a></p><p class="note">Certificate：Python 118/118、Ruby 168/168、K.1--K.48、48/48 displays，3 个 Python hash seeds 及 regeneration 字节稳定；两套实现分别拒绝 118/118 与 168/168 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限证书不替代 continuum proof；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 62 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>J 的上界重构与 K 的实单频带单切片下界</h2><p><a href="#s-481">J：local edge upper reconstruction</a> · <a href="#s-489">K：real dyadic fixed-slice lower bound</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 62 adjacent")
    next_section = f'''<section id="next"><div class="section-no">STOP / NO LATER RELEASE AUTHORIZED</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Later material remains unauthorized, unread, and unpublished</h2><p style="margin:.15rem 0">本站当前发布至 R0.76K Step 62。K 只证明 real one-dyadic-band exact heat-shear 的固定单切片下界与 signed-cap slice 结果；完整 <code>q=o(L^(5/2))</code> 下界、complete-clock signed flux/full-plateau quotient、L³ endpoint optimality、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。<a href="/{RECAP_SLUG}.html">查看上一大里程碑 recap（截止 I，不覆盖 J/K）</a>。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 62 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    replacements = (
        ('data-site-version="2.40"', 'data-site-version="2.41"', "home version"),
        ("/i18n-en.js?v=2.40", "/i18n-en.js?v=2.41", "home i18n"),
        ("/site-refresh.js?v=2.40.1", "/site-refresh.js?v=2.41.1", "home refresh"),
        ("<strong>v2.40</strong>网页版本", "<strong>v2.41</strong>网页版本", "home stat version"),
        ("<strong>R0.76J</strong>最新研究节点", "<strong>R0.76K</strong>最新研究节点", "home latest"),
        ("<strong>264</strong>公开研究笔记", "<strong>265</strong>公开研究笔记", "home count"),
        ("展开 174 篇公开笔记", "展开 175 篇公开笔记", "home route count"),
        ("综述 v2.40 · 2026-09-05", "综述 v2.41 · 2026-09-05", "home footer"),
        ("Research topology · R0.1–R0.76J", "Research topology · R0.1–R0.76K", "home topology"),
        ('href="#r076j">跳到首页 R0.76J 卡片 →', 'href="#r076k">跳到首页 R0.76K 卡片 →', "home jump"),
        ("R0.70A–R0.76J：166 节已公开，104 节完整封存", "R0.70A–R0.76K：167 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76J</span>', '<span class="route-range">R0.69P–R0.76K</span>', "home range"),
        ("<h3>R0.76J：本地重构端点外推并解除 exact-shear 文献条件</h3>", "<h3>R0.76K：实单频带 edge 下界与 exact heat-shear 单切片</h3>", "home route title"),
        ("R0.72R–R0.76J：</span>", "R0.72R–R0.76K：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76J"', 'aria-label="R0.69P–R0.76K"', "home label"),
        ("全站现有 264 篇公开研究笔记", "全站现有 265 篇公开研究笔记", "home recap count"),
    )
    for old, new, label in replacements:
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76K Step 62 证明 real one-dyadic-band exact heat-shear 的固定单切片 edge 下界与 signed-cap pairing，并覆盖 q=o(L²)；完整 q=o(L^(5/2)) 下界和 full-clock signed flux/full-plateau quotient 仍开放。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76K · 2026-09-05 · STEP 62 · REAL DYADIC EDGE SHARPNESS</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">The exp(cq√d) edge scale and linear endpoint factor already occur for real one-dyadic-band cosine packets. Exact integer heat-shear realization and favourable signed-cap pairing hold at any prescribed slice throughout q=o(L²). The complete-clock signed quotient and the full q=o(L^(5/2)) lower range remain open. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76k.pdf">阅读最新 R0.76K 研究笔记 →</a><a href="/{RECAP_SLUG}.html">上一大里程碑回顾（截止 I，203 节；不覆盖 J/K）</a><a href="/notes/">265 篇研究笔记总索引</a><a href="#r076k">查看首页 R0.76K 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76K · 167 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76K Step 62 real dyadic single-slice lower bound</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">K proves the real one-dyadic-band edge and endpoint lower scales inside exact heat-shear slices for q=o(L²), and closes the signed-cap pairing only at that selected slice.</p>', "home summary")
    page = replace_once(page, 'local Takenaka–Malmquist/Laguerre endpoint reconstruction with q^7 exp(20√2q√Δ_a); arbitrary nonlinear fields and Version-M extraction open</p>',
        'local Takenaka–Malmquist/Laguerre endpoint reconstruction with q^7 exp(20√2q√Δ_a) → real-dyadic fixed-slice lower sharpness and signed-cap slice for q=o(L²); complete-clock quotient, arbitrary nonlinear fields, and Version-M extraction open</p>', "home path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76j.html">R0.76J</a>',
        '<a class="milestone" href="/notes/r0-76j.html">R0.76J</a>\n<a class="milestone" href="/notes/r0-76k.html">R0.76K</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED · STOP · NO LATER RELEASE AUTHORIZED</span><span class="tree-state current">BOUNDARY</span></div><h3>Later material remains unauthorized, unread, and unpublished</h3><p>K 只关闭 fixed single-slice lower bound 与 signed-cap pairing。完整 q=o(L^(5/2)) 下界、complete-clock signed flux/full-plateau quotient、L³ endpoint optimality、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''<div class="task-one" id="r076k" data-release="r076k" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76K Step 62 · 2026-09-05 · REAL DYADIC EDGE SHARPNESS</p><h3>{TITLE}</h3><p>K 证明 real one-dyadic-band cosine packets 已具有 exp(cq√d) edge 尺度与线性 q endpoint 因子；任意指定 (s*,B) 都可由 exact integer heat-shear 在一个切片精确实现。统一构造覆盖 q=o(L²)，signed two-cap pairing 也只在该切片闭合。完整时钟 quotient 仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-76k.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76k.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I，不覆盖 J/K）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076j"'
    if anchor not in page:
        raise RuntimeError("home J card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    page = replace_pattern(page, r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>',
        f'''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">上一大里程碑回顾 R0.61–R0.76I · 2026-09-05</p><h3>累计回顾收录 203 个节点；全站现有 265 篇公开研究笔记</h3><p>回顾覆盖端点仍为 I。I recap 保持字节不变；J 与 K 都在其后，均不触发新 recap。</p><p><strong>当前边界：</strong>完整时钟 signed quotient、multiple bands、arbitrary nonlinear packets、Version-M extraction、regularity 与 Clay 仍 OPEN。</p><p><a href="/{RECAP_SLUG}.html"><strong>阅读截止 I 的完整累计回顾 →</strong></a> · <a href="/{RECAP_SLUG}.pdf">下载同步 PDF</a></p></div>''', "home recap card")
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.40"', 'data-site-version="2.41"', "lit version"),
        ("/i18n-en.js?v=2.40", "/i18n-en.js?v=2.41", "lit i18n"),
        ("文献综述 v2.40 · 2026-09-05", "文献综述 v2.41 · 2026-09-05", "lit footer"),
        ("本站 R0.69P–R0.76J 只列为研究笔记", "本站 R0.69P–R0.76K 只列为研究笔记", "lit intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76K</b><strong>real one-band edge lower bounds and exact heat-shear slice</strong></header><p>Step 62 证明 real one-dyadic-band cosine packets 的 <code>exp(cq√d)</code> edge 下界、linear <code>q</code> endpoint factor 与 exterior interval lower bound；任意 prescribed <code>(s*,B)</code> 都可由 consecutive integer modes 在 exact heat-shear 单切片实现。uniform range 为 <code>q=o(L²)</code>，signed-cap pairing 只在该切片闭合。<a href="/notes/r0-76k.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I，不覆盖 J/K）</a> <a href="#r076k-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><span hidden>开放接口 · 后续版本</span><strong>not authorized, unread, and unpublished</strong></header><p>完整 <code>q=o(L^(5/2))</code> 下界、complete-clock signed flux/full-plateau quotient、L³ endpoint optimality、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "lit route")
    boundary = (
        '<h3 id="r076k-boundary">R0.76K Step 62 的实单频带下界与 fixed-slice 边界</h3>'
        '<p><a href="https://arxiv.org/abs/2607.10501v1">Zhang 2026 arXiv v1</a> Proposition 7.1 提供既有 complex confluent Chebyshev architecture；'
        '<a href="https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.36">Chen–Price 2019</a> 是 clustered-Fourier 历史背景。'
        '<a href="https://dlmf.nist.gov/18.3">NIST DLMF §18.3</a> 与 <a href="https://dlmf.nist.gov/18.6">§18.6</a> 支持标准 Legendre orthogonality 与 endpoint normalization。</p>'
        '<div class="boundary"><strong>R0.76K Step 62 公开边界 · REAL DYADIC EDGE SHARPNESS</strong><p>'
        'LITERATURE：complex confluent architecture 与 classical orthogonal-polynomial facts。'
        'PROVED LOCALLY：real conjugate pairing、one-dyadic-band pointwise/integrated lower bounds、endpoint q/√2、exact integer heat-shear slice、q=o(L²) varying-degree range、signed two-cap slice identity、exact semigroup formula 与 backward warning。'
        'FINITE COMPUTATION：绑定 12 个冻结对象、118/118 Python assertions、168/168 independent Ruby assertions、K.1–K.48 与 48 displays。'
        'MODE COUNT：q 表示 positive cosine modes，对应 2q complex branches；不改写成 complex T_q inclusion。'
        'OPEN：完整 q=o(L^(5/2)) 下界、complete-clock signed flux/full-plateau quotient、L³ endpoint optimality、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。'
        '<strong>NO COMPLETE-CLOCK LOWER THEOREM. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76k.html">阅读完整笔记</a> · '
        f'<a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I，不覆盖 J/K）</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature references anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([p for p in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in p.name])
    pdf_count = len([p for p in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in p.name])
    if html_count != 265 or pdf_count not in (221, 222):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(previous.route_post_r060_slugs(HOME.read_text()))
    if post_r060 != 205:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76k.html", "latestPublishedResearchPdf": "/notes/r0-76k.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 203, "latestRecapRelease": "R0.76I",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-05",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076j":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE or inventory["publishedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory release drift")
    inventory["publishedReleaseCount"] = 167
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 62
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1, "research_version": CODE,
        "scope": "REAL_ONE_DYADIC_BAND_EDGE_LOWER_BOUNDS_EXACT_HEAT_SHEAR_SIGNED_CAP_SINGLE_SLICE",
        "source_commit": frozen_import.SOURCE_COMMIT, "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT, "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256, "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "PROVED_LOCAL_REAL_DYADIC_EXACT_HEAT_SHEAR_SINGLE_SLICE_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION", "simulation_or_dns": "NOT_USED", "dgx": "NOT_USED",
            "novelty_or_priority": "NOT_CLAIMED",
            "literature": "ZHANG_PROP_7_1_ARCHITECTURE_CHEN_PRICE_MOTIVATION_DLMF_STANDARD_FACTS",
            "proved_locally": "REAL_DYADIC_LOWER_BOUNDS_ENDPOINT_INTEGER_SLICE_SIGNED_CAP_SEMIGROUP_WARNING",
            "mode_count": "Q_POSITIVE_COSINE_MODES_EQUALS_2Q_COMPLEX_BRANCHES_NOT_COMPLEX_TQ_INCLUSION",
            "packet_scope": "EXACT_REAL_ONE_DYADIC_BAND_FIXED_SINGLE_SLICE_ONLY",
            "varying_degree_range": "Q_LITTLE_O_L_SQUARED_PROVED",
            "full_upper_window_lower_bound": "Q_LITTLE_O_L_TO_5_OVER_2_OPEN",
            "complete_clock_signed_flux_full_plateau_quotient": "OPEN_NOT_PROVED",
            "l3_endpoint_optimality": "OPEN_NOT_PROVED",
            "multiple_bands": "OPEN_NOT_PROVED", "nonconstant_shear": "OPEN_NOT_PROVED",
            "arbitrary_nonlinear_packets": "OPEN_NOT_PROVED", "E24": "OPEN_NOT_PROVED",
            "version_m_extraction": "OPEN_NOT_PROVED", "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12", "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_118_OF_118", "independent_ruby": "PASS_168_OF_168",
            "negative_mutations": "PASS_PYTHON_118_OF_118_RUBY_168_OF_168",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_K1_TO_K48_AND_48_OF_48_DISPLAYS",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4", "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76k.html", "target_pdf": "/notes/r0-76k.pdf", "target_primary_figure": None,
            "recap_update_required": False, "recap_terminal_release": "R0.76I_STEP60",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076k_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 62, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 203,
        "postR070APublishedReleaseCount": 167, "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"], "nextRelease": "r076l",
        "latestPublishedResearchHtml": "/notes/r0-76k.html", "latestPublishedResearchPdf": "/notes/r0-76k.pdf",
        "latestReleaseGate": "tests/r076k-step62-gate.test.mjs", "latestReleasePublicationTest": "tests/r076k-step62-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076k-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076k-step62-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076k-step62-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076k-step62-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076k-step62-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076k-step62", "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "coreParentCommit": frozen_import.CORE_PARENT_COMMIT, "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT, "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False, "recapRequired": False,
        },
        "latestRecapRelease": "r076i", "latestRecapHtml": f"/{RECAP_SLUG}.html",
        "latestRecapPdf": f"/{RECAP_SLUG}.pdf", "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-76k.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
        for target, expected in RECAP_HASHES.items():
            if sha256(target) != expected:
                raise RuntimeError(f"protected recap drift after generation: {target.relative_to(ROOT)}")
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 62, "siteVersion": VERSION,
        "recapUpdated": False, "recapRelease": "R0.76I", "formalFigure": None, "formalFigureExemption": True,
        "simulation": False, "pdeData": False, "noveltyClaim": False, "clayClaim": False,
        "theoremStatus": "PROVED_LOCAL_REAL_DYADIC_EXACT_HEAT_SHEAR_SINGLE_SLICE",
        "modeWindow": "Q_LITTLE_O_L_SQUARED", "fullUpperWindowLowerBound": "OPEN",
        "completeClockSignedQuotient": "OPEN", "laterReleaseAuthorized": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
