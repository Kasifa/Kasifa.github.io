#!/usr/bin/env python3
"""Publish frozen R0.76J Step 61 from the verified R0.76I baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076i_step60_release as previous
import import_r076j_step61_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "f24e3e73b2debd8197a92dfaf8cd424f272b7d25"
VERSION = "2.40"
RELEASE = "r076j"
CODE = "R0.76J"
TITLE = "R0.76J｜本地重构端点外推并解除 exact-shear 窗口的文献条件"
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
            raise RuntimeError(f"R0.76J frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r076j_local_edge_extrapolation_reconstruction_certificate.json").read_text())
    if (certificate.get("verdict") != "PASS" or certificate.get("assertionsPassed") != 96
            or certificate.get("assertionsTotal") != 96 or certificate.get("freezeReady") is not True
            or len(certificate.get("negativeMutations", [])) != 96):
        raise RuntimeError("R0.76J certificate verdict drift")
    main = (ROOT / "research/r076j_local_edge_extrapolation_reconstruction.md").read_text()
    compact = " ".join(main.split())
    for token in (
        r"\tag{J.1}", r"\tag{J.10}", r"\tag{J.20}", r"\tag{J.30}", r"\tag{J.40}", r"\tag{J.46}",
        "PROVED LOCALLY FROM ESTABLISHED LITERATURE", r"q=o(L^{5/2})", r"-\frac2{11907}",
        r"\sqrt{\frac{250}{19}}", r"\frac{20}{19}", "exact one-band constant shear", "**NOT CLAY.**",
    ):
        if token not in compact:
            raise RuntimeError(f"R0.76J boundary drift: {token}")
    source = (ROOT / "research/r076j_report-source.md").read_text()
    for token in ("Zhang", "Proposition 4.2", "Erdelyi", "Kós", "NOT CLAY"):
        if token not in source:
            raise RuntimeError(f"R0.76J source boundary drift: {token}")


def render_sections() -> str:
    source = (ROOT / "research/r076j_local_edge_extrapolation_reconstruction.md").read_text().strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 480
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
    if section_index != 488:
        raise RuntimeError(f"Step 61 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.39"', 'data-site-version="2.40"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.39", "/i18n-en.js?v=2.40", "note i18n")
    page = replace_pattern(page, r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A local Takenaka–Malmquist and Laguerre reconstruction proves the endpoint extrapolation needed for the exact one-band constant-shear q=o(L^(5/2)) window.">', "note metadata")
    page = replace_pattern(page, r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76j.html">', "note canonical")
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76J · STEP 61 · 2026-09-05</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76J · Step 61 · LOCAL EDGE EXTRAPOLATION RECONSTRUCTION</div><h1>{TITLE}</h1><p>J 以有限竖线 Takenaka–Malmquist 基、正负时间 Laguerre majorant 与半线尾部回收，在本站本地证明 exact real one-band constant-shear 所需的 endpoint extrapolation。空间代价为 <code>q² exp(20√2 q√Δ_a)</code>，完整代价为 <code>q⁷ exp(20√2 q√Δ_a)</code>；充分窗口仍为 <code>q=o(L^(5/2))</code>，精确规范化速率仍为 <code>-2/11907</code>。<strong>PROVED LOCALLY FROM ESTABLISHED LITERATURE. EXACT SHEAR ONLY. NOT CLAY.</strong></p><div class="labels"><span class="label">LITERATURE</span><span class="label">PROVED LOCALLY</span><span class="label">PROVED LOCALLY FROM ESTABLISHED LITERATURE</span><span class="label">FINITE COMPUTATION</span><span class="label">OPEN</span><span class="label">LOCAL EDGE PROOF</span><span class="label">I HISTORY: CONDITIONAL-LITERATURE</span><span class="label">q=o(L^(5/2))</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76J STEP 61</strong><p>new theorem：PROVED LOCALLY</p><p>literature：Erdelyi / Kós</p><p>Zhang Prop. 4.2：architecture only</p><p>edge constant：√(250/19)</p><p>tail recovery：20/19</p><p>cutoff：25N/α</p><p>spatial cost：q² exp(20√2q√Δ_a)</p><p>full cost：q⁷ exp(20√2q√Δ_a)</p><p>window：q=o(L^(5/2))</p><p>rate：-2/11907</p><p>family：exact real one-band shear</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_sections() + '\n<section id="reproduce">', "Step 61 sections")
    links = " · ".join([
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076j_local_edge_extrapolation_reconstruction.md">Step 61 主文</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md">primary audit</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076j_report-source.md">source report</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076j_local_edge_extrapolation_reconstruction_fixtures.json">fixtures JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076j_local_edge_extrapolation_reconstruction_expected.json">expected JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076j_local_edge_extrapolation_reconstruction_certificate.json">certificate JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076j_local_edge_extrapolation_reconstruction_certificate_report.md">Python report</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076j_local_edge_extrapolation_reconstruction_independent_audit.md">Ruby independent audit</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076j_local_edge_extrapolation_reconstruction_qa_report.md">certificate QA</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076j_local_edge_extrapolation_reconstruction_certificate.py">Python script</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076j_local_edge_extrapolation_reconstruction_certificate_independent.rb">Ruby script</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076j_local_edge_extrapolation_reconstruction_qa.sh">QA script</a>',
    ])
    evidence = f'''<section id="reproduce"><div class="section-no">J / 冻结证据</div><h2>Step 61 主文、来源边界、双实现证书与 fail-closed QA</h2><p class="files">{links}</p><p><a href="/notes/r0-76j.pdf">同步 reader PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I）</a> · <a href="/{RECAP_SLUG}.pdf">截至 I 的 recap PDF</a></p><p class="note">Certificate：Python 96/96、Ruby 107/107、J.1--J.46、48/48 displays，3 个 Python hash seeds 及 regeneration 字节稳定；两套实现分别拒绝 96/96 与 107/107 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限证书不替代 continuum proof；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 61 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>I 的条件性窗口与 J 的本地端点重构</h2><p><a href="#s-472">I：Chebyshev-scale conditional window</a> · <a href="#s-481">J：local edge reconstruction</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 61 adjacent")
    next_section = f'''<section id="next"><div class="section-no">STOP / NO LATER RELEASE AUTHORIZED</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Later material remains unauthorized, unread, and unpublished</h2><p style="margin:.15rem 0">本站当前发布至 R0.76J Step 61。J 在 exact real one-band constant-shear family 内本地重构 endpoint extrapolation，但最优常数、matching lower bound、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。I 的历史性 CONDITIONAL-LITERATURE 标签不改写。后续版本未授权、未读取、未公开。<a href="/{RECAP_SLUG}.html">查看上一大里程碑 recap（截止 I）</a>。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 61 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    replacements = (
        ('data-site-version="2.39"', 'data-site-version="2.40"', "home version"),
        ("/i18n-en.js?v=2.39", "/i18n-en.js?v=2.40", "home i18n"),
        ("/site-refresh.js?v=2.39.1", "/site-refresh.js?v=2.40.1", "home refresh"),
        ("<strong>v2.39</strong>网页版本", "<strong>v2.40</strong>网页版本", "home stat version"),
        ("<strong>R0.76I</strong>最新研究节点", "<strong>R0.76J</strong>最新研究节点", "home latest"),
        ("<strong>263</strong>公开研究笔记", "<strong>264</strong>公开研究笔记", "home count"),
        ("展开 173 篇公开笔记", "展开 174 篇公开笔记", "home route count"),
        ("综述 v2.39 · 2026-09-05", "综述 v2.40 · 2026-09-05", "home footer"),
        ("Research topology · R0.1–R0.76I", "Research topology · R0.1–R0.76J", "home topology"),
        ('href="#r076i">跳到首页 R0.76I 卡片 →', 'href="#r076j">跳到首页 R0.76J 卡片 →', "home jump"),
        ("R0.70A–R0.76I：165 节已公开，104 节完整封存", "R0.70A–R0.76J：166 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76I</span>', '<span class="route-range">R0.69P–R0.76J</span>', "home range"),
        ("<h3>R0.76I：切比雪夫尺度完整平台条件性窗口</h3>", "<h3>R0.76J：本地重构端点外推并解除 exact-shear 文献条件</h3>", "home route title"),
        ("R0.72R–R0.76I：</span>", "R0.72R–R0.76J：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76I"', 'aria-label="R0.69P–R0.76J"', "home label"),
        ("全站现有 263 篇公开研究笔记", "全站现有 264 篇公开研究笔记", "home recap count"),
    )
    for old, new, label in replacements:
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76J Step 61 本地重构 exact real one-band constant-shear 所需的 endpoint extrapolation，使 q=o(L^(5/2)) 窗口不再依赖 Zhang Proposition 4.2；结论不覆盖任意 Navier–Stokes、Version-M 或正则性。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76J · 2026-09-05 · STEP 61 · LOCAL EDGE EXTRAPOLATION RECONSTRUCTION</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">A local Takenaka–Malmquist/Laguerre proof gives the exact-shear endpoint bound with full cost q^7 exp(20√2q√Δ_a), preserving q=o(L^(5/2)) and exact normalized rate -2/11907. PROVED LOCALLY FROM ESTABLISHED LITERATURE. EXACT SHEAR ONLY. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76j.pdf">阅读最新 R0.76J 研究笔记 →</a><a href="/{RECAP_SLUG}.html">上一大里程碑回顾（截止 I，203 节）</a><a href="/notes/">264 篇研究笔记总索引</a><a href="#r076j">查看首页 R0.76J 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76J · 166 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76J Step 61 local edge reconstruction</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">J locally reconstructs the endpoint inequality behind I for exact real one-band constant shears, with q⁷ exp(20√2q√Δ_a) full cost and the same q=o(L^(5/2)) window.</p>', "home summary")
    page = replace_once(page, 'literature-enabled q^7 exp(O(q/√a)) full-plateau upper bound; arbitrary nonlinear fields and Version-M extraction open</p>', 'literature-enabled q^7 exp(O(q/√a)) bound → local Takenaka–Malmquist/Laguerre endpoint reconstruction with q^7 exp(20√2q√Δ_a); arbitrary nonlinear fields and Version-M extraction open</p>', "home path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76i.html">R0.76I</a>', '<a class="milestone" href="/notes/r0-76i.html">R0.76I</a>\n<a class="milestone" href="/notes/r0-76j.html">R0.76J</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED · STOP · NO LATER RELEASE AUTHORIZED</span><span class="tree-state current">BOUNDARY</span></div><h3>Later material remains unauthorized, unread, and unpublished</h3><p>J 本地重构 exact-shear endpoint theorem；optimal constants、matching lower bound、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。I 的历史性 CONDITIONAL-LITERATURE 标签保持不变。后续版本未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''<div class="task-one" id="r076j" data-release="r076j" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76J Step 61 · 2026-09-05 · LOCAL EDGE EXTRAPOLATION RECONSTRUCTION</p><h3>{TITLE}</h3><p>J 用有限竖线 Takenaka–Malmquist 基、Laguerre majorant 与半线尾部回收，本地证明 exact real one-band constant-shear 所需的 endpoint extrapolation。完整代价为 q⁷ exp(20√2q√Δ_a)，充分窗口仍为 q=o(L^(5/2))，精确规范化速率仍为 -2/11907。PROVED LOCALLY FROM ESTABLISHED LITERATURE. NOT CLAY.</p><p><a href="/notes/r0-76j.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76j.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076i"'
    if anchor not in page:
        raise RuntimeError("home I card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    page = replace_pattern(page, r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>',
        f'''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">上一大里程碑回顾 R0.61–R0.76I · 2026-09-05</p><h3>累计回顾收录 203 个节点；全站现有 264 篇公开研究笔记</h3><p>回顾覆盖端点仍为 I。I recap 保持字节不变；J 是其后的本地重构节点，不触发新 recap。</p><p><strong>当前边界：</strong>multiple bands、arbitrary nonlinear packets、Version-M extraction、regularity 与 Clay 仍 OPEN。</p><p><a href="/{RECAP_SLUG}.html"><strong>阅读截止 I 的完整累计回顾 →</strong></a> · <a href="/{RECAP_SLUG}.pdf">下载同步 PDF</a></p></div>''', "home recap card")
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.39"', 'data-site-version="2.40"', "lit version"),
        ("/i18n-en.js?v=2.39", "/i18n-en.js?v=2.40", "lit i18n"),
        ("文献综述 v2.39 · 2026-09-05", "文献综述 v2.40 · 2026-09-05", "lit footer"),
        ("本站 R0.69P–R0.76I 只列为研究笔记", "本站 R0.69P–R0.76J 只列为研究笔记", "lit intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76J</b><strong>local edge extrapolation reconstruction</strong></header><p>Step 61 以 finite vertical-line Takenaka–Malmquist basis、Laguerre majorants 与 half-line tail recovery 本地证明 exact-shear endpoint inequality；空间代价为 <code>q² exp(20√2q√Δ_a)</code>，完整代价为 <code>q⁷ exp(20√2q√Δ_a)</code>，仍给 <code>q=o(L^(5/2))</code>。Zhang Proposition 4.2 只作架构和更优常数比较，不再作为 J 定理输入。<a href="/notes/r0-76j.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I）</a> <a href="#r076j-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><span hidden>开放接口 · 后续版本</span><strong>not authorized, unread, and unpublished</strong></header><p>最优常数、exact-shear matching lower bound、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "lit route")
    boundary = (
        '<h3 id="r076j-boundary">R0.76J Step 61 的本地端点重构与 exact-shear 边界</h3>'
        '<p><a href="https://www.mathnet.ru/eng/sm8670">Erdelyi 2017</a> 的 Markov inequality 与 Kós endpoint estimate 是 J 保留的已建立同行评审输入。<a href="https://arxiv.org/abs/2607.10501v1">Zhang 2026 arXiv v1</a> Proposition 4.2 只作 proof architecture 与较优常数比较；J 不再从该命题导入定理。</p>'
        '<div class="boundary"><strong>R0.76J Step 61 公开边界 · LOCAL EDGE EXTRAPOLATION RECONSTRUCTION</strong><p>'
        'LITERATURE：Erdelyi Markov 与 Kós endpoint estimates。'
        'PROVED LOCALLY：vertical-line Takenaka–Malmquist basis、Volterra/Laguerre coefficient formula、正负半线 majorants、weighted tail recovery、half-line comparison 与 finite endpoint theorem。'
        'PROVED LOCALLY FROM ESTABLISHED LITERATURE：exact real one-band constant-shear 的 q⁷ exp(20√2q√Δ_a) 完整代价、q=o(L^(5/2)) 窗口与 normalized rate -2/11907。'
        'FINITE COMPUTATION：绑定 12 个冻结对象、constants、powers、signs、J.1–J.46 与 48 displays。'
        'HISTORICAL BOUNDARY：I 的 CONDITIONAL-LITERATURE 状态保持原样，不以 J 回写历史。'
        'OPEN：optimal constants、matching exact-shear lower bound、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。'
        '<strong>NO FULL-CLASS SHARPNESS CLAIM. NO VERSION-M CLAIM. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76j.html">阅读完整笔记</a> · '
        f'<a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I）</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature references anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def route_post_r060_slugs(page: str) -> list[str]:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    return ordered[ordered.index("r0-61"):]


def update_accounting() -> None:
    html_count = len([p for p in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in p.name])
    pdf_count = len([p for p in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in p.name])
    if html_count != 264 or pdf_count not in (220, 221):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(route_post_r060_slugs(HOME.read_text()))
    if post_r060 != 204:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76j.html", "latestPublishedResearchPdf": "/notes/r0-76j.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 203, "latestRecapRelease": "R0.76I",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-05",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076i":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE or inventory["publishedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory release drift")
    inventory["publishedReleaseCount"] = 166
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 61
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1, "research_version": CODE,
        "scope": "LOCAL_EDGE_EXTRAPOLATION_RECONSTRUCTION_FOR_EXACT_ONE_BAND_CONSTANT_SHEARS",
        "source_commit": frozen_import.SOURCE_COMMIT, "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT, "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256, "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "PROVED_LOCALLY_FROM_ESTABLISHED_LITERATURE_EXACT_SHEAR_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION", "simulation_or_dns": "NOT_USED", "dgx": "NOT_USED",
            "novelty_or_priority": "NOT_CLAIMED", "zhang_proposition_4_2": "ARCHITECTURE_AND_SHARPER_CONSTANT_COMPARISON_ONLY_NOT_IMPORTED",
            "literature": "ERDELYI_MARKOV_AND_KOS_ENDPOINT_ESTABLISHED_INPUTS",
            "proved_locally": "TAKENAKA_MALMQUIST_LAGUERRE_HALF_LINE_TAIL_FINITE_ENDPOINT",
            "composite_theorem": "PROVED_LOCALLY_FROM_ESTABLISHED_LITERATURE",
            "historical_i_status": "CONDITIONAL_LITERATURE_PRESERVED",
            "packet_scope": "EXACT_REAL_ONE_BAND_CONSTANT_SHEARS_ONLY",
            "complete_cost": "Q7_EXP_20_SQRT2_Q_SQRT_DELTA_A", "mode_window": "Q_LITTLE_O_L_TO_5_OVER_2",
            "normalized_rate": "EXACT_MINUS_TWO_OVER_11907", "multiple_bands": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED", "arbitrary_nonlinear_packets": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED", "complete_version_m_extraction": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED", "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12", "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_96_OF_96", "independent_ruby": "PASS_107_OF_107",
            "negative_mutations": "PASS_PYTHON_96_OF_96_RUBY_107_OF_107", "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE", "equation_tags_and_displays": "PASS_J1_TO_J46_TAGS_AND_48_OF_48_DISPLAYS",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4", "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76j.html", "target_pdf": "/notes/r0-76j.pdf", "target_primary_figure": None,
            "recap_update_required": False, "recap_terminal_release": "R0.76I_STEP60",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076j_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 61, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 203,
        "postR070APublishedReleaseCount": 166, "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"], "nextRelease": "r076k",
        "latestPublishedResearchHtml": "/notes/r0-76j.html", "latestPublishedResearchPdf": "/notes/r0-76j.pdf",
        "latestReleaseGate": "tests/r076j-step61-gate.test.mjs", "latestReleasePublicationTest": "tests/r076j-step61-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076j-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076j-step61-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076j-step61-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076j-step61-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076j-step61-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076j-step61", "handoffCommit": frozen_import.HANDOFF_COMMIT,
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
    write_text(PUBLIC / "notes/r0-76j.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
        for target, expected in RECAP_HASHES.items():
            if sha256(target) != expected:
                raise RuntimeError(f"protected recap drift after generation: {target.relative_to(ROOT)}")
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 61, "siteVersion": VERSION,
        "recapUpdated": False, "recapRelease": "R0.76I", "formalFigure": None, "formalFigureExemption": True,
        "simulation": False, "pdeData": False, "noveltyClaim": False, "clayClaim": False,
        "theoremStatus": "PROVED_LOCALLY_FROM_ESTABLISHED_LITERATURE", "modeWindow": "Q_LITTLE_O_L_TO_5_OVER_2",
        "normalizedRate": "MINUS_TWO_OVER_11907", "laterReleaseAuthorized": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
