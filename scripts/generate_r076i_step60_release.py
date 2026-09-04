#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76I Step 60 from the verified R0.76H Step 59 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076h_step59_release as previous
import import_r076i_step60_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "8b75e48ec55033acba9f4baa0664641a828309bc"
VERSION = "2.39"
RELEASE = "r076i"
CODE = "R0.76I"
TITLE = "R0.76I｜切比雪夫尺度的完整平台增长模态窗口"
RECAP_SLUG = "recap-r0-61-r0-76i"
PREVIOUS_RECAP_SLUG = "recap-r0-61-r0-75w"
RECAP_HASHES = {
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
    return subprocess.check_output(
        ["git", "show", f"{BASELINE_COMMIT}:{relative}"], cwd=ROOT, text=True
    )


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected W milestone recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.76I frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076i_chebyshev_scale_full_plateau_window_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsPassed") != 129
        or certificate.get("assertionsTotal") != 129
        or certificate.get("freezeReady") is not True
        or len(certificate.get("negativeMutations", [])) != 129
    ):
        raise RuntimeError("R0.76I certificate verdict drift")
    main = (ROOT / "research/r076i_chebyshev_scale_full_plateau_window.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{I.1}", r"\tag{I.10}", r"\tag{I.20}", r"\tag{I.30}", r"\tag{I.38}",
        "**CONDITIONAL-LITERATURE**", r"q(L)=o(L^{5/2})", r"-\frac2{11907}",
        "one dyadic band", "independent proof of the imported extrapolation theorem", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76I boundary drift: {token}")
    source_report = (ROOT / "research/r076i_report-source.md").read_text()
    for token in ("arXiv:2607.10501v1", "Proposition 4.2", "UNREFEREED PREPRINT", "NOT CLAY"):
        if token not in source_report:
            raise RuntimeError(f"R0.76I source boundary drift: {token}")


def render_step60_sections() -> str:
    source = (ROOT / "research/r076i_chebyshev_scale_full_plateau_window.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 471
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            heading = re.sub(r"^\d+\.\s*", "", lines[0][3:])
            output.append(
                f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{inline_markup(heading)}</h2>'
            )
            section_open = True
            continue
        stripped = block.strip()
        if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
            output.append(f'<div class="equation">{html.escape(stripped)}</div>')
        elif lines[0].startswith("### "):
            output.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
        elif len(lines) >= 2 and lines[0].startswith("|") and re.match(r"^\|[-:| ]+\|$", lines[1]):
            rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
            cell_style = ' style="overflow-wrap:anywhere;word-break:break-word"'
            head = "".join(f"<th{cell_style}>{inline_markup(cell)}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td{cell_style}>{inline_markup(cell)}</td>" for cell in row) + "</tr>" for row in rows[2:])
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
    if section_index != 480:
        raise RuntimeError(f"Step 60 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.38"', 'data-site-version="2.39"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.38", "/i18n-en.js?v=2.39", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Conditional on Zhang 2026 Proposition 4.2, a Chebyshev-scale full-plateau estimate expands the exact one-band constant-shear window to q=o(L^(5/2)).">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76i.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76I · STEP 60 · 2026-09-05</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76I · Step 60 · CHEBYSHEV-SCALE FULL-PLATEAU WINDOW</div><h1>{TITLE}</h1><p>以 Zhang 2026-07 arXiv v1 Proposition 4.2 为文献前提，I 把 exact real one-band constant-shear family 的完整平台损失从 <code>exp(Cq)</code> 改为 <code>q^7 exp(12√2 q√Δ_a)</code>，其中 <code>Δ_a=O(1/a)</code>；充分窗口由 <code>q=o(L²)</code> 扩展到 <code>q=o(L^(5/2))</code>，规范化精确速率仍为 <code>-2/11907</code>。<strong>CONDITIONAL-LITERATURE. EXACT SHEAR ONLY. NOT CLAY.</strong></p><div class="labels"><span class="label">CONDITIONAL-LITERATURE</span><span class="label">LITERATURE</span><span class="label">PROVED LOCALLY</span><span class="label">FINITE COMPUTATION</span><span class="label">OPEN</span><span class="label">q=o(L^(5/2))</span><span class="label">ONE BAND</span><span class="label">CONSTANT SHEAR</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76I STEP 60</strong><p>source：Zhang arXiv v1</p><p>input：Proposition 4.2</p><p>peer review：NOT CLAIMED</p><p>gap：Δ_a=O(a⁻¹)</p><p>spatial cost：q² exp(12√2q√Δ_a)</p><p>full cost：q⁷ exp(12√2q√Δ_a)</p><p>window：q=o(L^(5/2))</p><p>rate：-2/11907</p><p>family：exact real one-band shear</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step60_sections() + '\n<section id="reproduce">', "Step 60 sections")
    evidence = f'''<section id="reproduce"><div class="section-no">I / 冻结证据</div><h2>Step 60 主文、文献边界、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076i_chebyshev_scale_full_plateau_window.md">Step 60 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076i_report-source.md">source report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076i_chebyshev_scale_full_plateau_window_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076i_chebyshev_scale_full_plateau_window_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076i_chebyshev_scale_full_plateau_window_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076i_chebyshev_scale_full_plateau_window_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076i_chebyshev_scale_full_plateau_window_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076i_chebyshev_scale_full_plateau_window_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076i_chebyshev_scale_full_plateau_window_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076i_chebyshev_scale_full_plateau_window_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076i_chebyshev_scale_full_plateau_window_qa.sh">QA script</a></p><p><a href="/notes/r0-76i.pdf">同步 reader PDF</a> · <a href="/{RECAP_SLUG}.html">R0.61–R0.76I 最新累计回顾</a> · <a href="/{RECAP_SLUG}.pdf">累计回顾 PDF</a> · <a href="/{PREVIOUS_RECAP_SLUG}.html">保留的 W recap</a></p><p class="note">Certificate：Python 129/129、Ruby 129/129、I.1--I.38、42/42 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 129/129 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限证书不证明 Zhang Proposition 4.2 或其他 continuum inequalities；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 60 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>E 的统一障碍、F–H 的显式候选链与 I 的条件性窗口</h2><p><a href="#s-443">E：uniform exp(Cq) window</a> · <a href="#s-452">F：spatial lower bound</a> · <a href="#s-456">G：central-fibre flux</a> · <a href="#s-465">H：full-plateau absorption</a> · <a href="#s-472">I：Chebyshev-scale conditional window</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 60 adjacent")
    next_section = f'''<section id="next"><div class="section-no">STOP / NO LATER RELEASE AUTHORIZED</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Later material remains unauthorized, unread, and unpublished</h2><p style="margin:.15rem 0">本站当前发布至 R0.76I Step 60。I 的组合定理依赖未经独立重证的 Zhang 2026-07 arXiv v1 Proposition 4.2，只覆盖 exact real one-band constant shears。多 dyadic bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。<a href="/{RECAP_SLUG}.html">查看最新累计回顾</a>。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 60 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.38"', 'data-site-version="2.39"', "home version"),
        ("/i18n-en.js?v=2.38", "/i18n-en.js?v=2.39", "home i18n"),
        ("/site-refresh.js?v=2.38.1", "/site-refresh.js?v=2.39.1", "home refresh"),
        ("<strong>v2.38</strong>网页版本", "<strong>v2.39</strong>网页版本", "home stat version"),
        ("<strong>R0.76H</strong>最新研究节点", "<strong>R0.76I</strong>最新研究节点", "home latest"),
        ("<strong>262</strong>公开研究笔记", "<strong>263</strong>公开研究笔记", "home public count"),
        ("展开 172 篇公开笔记", "展开 173 篇公开笔记", "home route count"),
        ("综述 v2.38 · 2026-09-05", "综述 v2.39 · 2026-09-05", "home footer"),
        ("Research topology · R0.1–R0.76H", "Research topology · R0.1–R0.76I", "home topology"),
        ('href="#r076h">跳到首页 R0.76H 卡片 →', 'href="#r076i">跳到首页 R0.76I 卡片 →', "home jump"),
        ("R0.70A–R0.76H：164 节已公开，104 节完整封存", "R0.70A–R0.76I：165 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76H</span>', '<span class="route-range">R0.69P–R0.76I</span>', "home range"),
        ("<h3>R0.76H：完整平台吸收显式 shifted-binomial 候选</h3>", "<h3>R0.76I：切比雪夫尺度完整平台条件性窗口</h3>", "home route title"),
        ("R0.72R–R0.76H：</span>", "R0.72R–R0.76I：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76H"', 'aria-label="R0.69P–R0.76I"', "home links label"),
        ("全站现有 262 篇公开研究笔记", "全站现有 263 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.76I Step 60 在 Zhang 2026-07 arXiv v1 Proposition 4.2 的条件下，把 exact real one-band constant-shear full-plateau cost 改为 q^7 exp(12√2q√Δ_a)，充分窗口扩展至 q=o(L^(5/2))；这不是任意 Navier–Stokes、Version-M 或正则性定理。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76I · 2026-09-05 · STEP 60 · CHEBYSHEV-SCALE FULL-PLATEAU WINDOW</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">Conditional on Zhang 2026 Proposition 4.2, the exact real one-band constant-shear cost becomes q^7 exp(12√2q√Δ_a), with Δ_a=O(1/a), enlarging the sufficient window to q=o(L^(5/2)) while retaining the exact normalized rate -2/11907. CONDITIONAL-LITERATURE. EXACT SHEAR ONLY. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76i.pdf">阅读最新 R0.76I 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾（R0.61–R0.76I，203 节）</a><a href="/notes/">263 篇研究笔记总索引</a><a href="#r076i">查看首页 R0.76I 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76I · 165 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76I Step 60 Chebyshev-scale conditional full-plateau window</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Conditional on Zhang Proposition 4.2, I replaces the exact-shear exp(Cq) full-plateau loss by q^7 exp(O(q/√a)) and enlarges the sufficient mode window to q=o(L^(5/2)).</p>', "home current summary")
    page = replace_once(page, 'nonzero-drift central-fibre lower bound → full-plateau absorption of the same explicit shifted packet and exact normalized rate -2/11907; arbitrary packets, arbitrary fields, and Version-M extraction open</p>', 'exp(Cq) exact-shear window → explicit-packet lower/flux/candidate-killing chain → literature-enabled q^7 exp(O(q/√a)) full-plateau upper bound; arbitrary nonlinear fields and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76h.html">R0.76H</a>', '<a class="milestone" href="/notes/r0-76h.html">R0.76H</a>\n<a class="milestone" href="/notes/r0-76i.html">R0.76I</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED · STOP · NO LATER RELEASE AUTHORIZED</span><span class="tree-state current">BOUNDARY</span></div><h3>Later material remains unauthorized, unread, and unpublished</h3><p>I 的 composite theorem 依赖未经独立重证的 Zhang arXiv v1 Proposition 4.2，且只覆盖 exact real one-band constant shears。multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076i" data-release="r076i" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76I Step 60 · 2026-09-05 · CHEBYSHEV-SCALE FULL-PLATEAU WINDOW</p><h3>{TITLE}</h3><p>在 Zhang 2026-07 arXiv v1 Proposition 4.2 条件下，I 用 bilateral endpoint extrapolation、Erdelyi derivative estimate、Kós terminal trace 与完整四行 energy identity，把 exact real one-band constant-shear sufficient window 扩展到 q=o(L^(5/2))，精确规范化速率仍为 -2/11907。无正式图、simulation、DNS 或 DGX。CONDITIONAL-LITERATURE. NOT CLAY.</p><p><a href="/notes/r0-76i.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76i.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">最新 milestone recap（截止 I）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076h"'
    if anchor not in page:
        raise RuntimeError("home R0.76H card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    recap_card = f'''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计里程碑回顾 R0.61–R0.76I · 2026-09-05</p><h3>R0.60 recap 之后的累计回顾收录 203 个节点；全站现有 263 篇公开研究笔记</h3><p>回顾区分 E 的 exp(Cq)/q=o(L²) 障碍、F–H 的显式候选 lower/flux/absorption 链，以及 I 依赖 Zhang arXiv v1 的 exp(O(q/√a))/q=o(L^(5/2)) 条件性上界。</p><p><strong>当前边界：</strong>independent proof、multiple bands、arbitrary nonlinear packets、Version-M extraction、regularity 与 Clay 仍 OPEN。</p><p><a href="/{RECAP_SLUG}.html"><strong>阅读 R0.61–R0.76I 完整累计回顾 →</strong></a> · <a href="/{RECAP_SLUG}.pdf">下载同步 PDF</a> · <a href="/{PREVIOUS_RECAP_SLUG}.html">保留上一版本</a></p></div>'''
    page = replace_pattern(page, r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>', recap_card, "home recap card")
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.38"', 'data-site-version="2.39"', "literature version"),
        ("/i18n-en.js?v=2.38", "/i18n-en.js?v=2.39", "literature i18n"),
        ("文献综述 v2.38 · 2026-09-05", "文献综述 v2.39 · 2026-09-05", "literature footer"),
        ("本站 R0.69P–R0.76H 只列为研究笔记", "本站 R0.69P–R0.76I 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76I</b><strong>Chebyshev-scale conditional full-plateau window</strong></header><p>Step 60 以 Zhang 2026-07 arXiv v1 Proposition 4.2 为条件性文献输入，用 shrinking endpoint gap <code>Δ_a=O(1/a)</code> 将 exact real one-band constant-shear spatial loss 改为 <code>q² exp(12√2q√Δ_a)</code>；derivative、terminal 与 four-row reconstruction 给出 full cost <code>q⁷ exp(12√2q√Δ_a)</code> 和充分窗口 <code>q=o(L^(5/2))</code>。<a href="/notes/r0-76i.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">milestone recap</a> <a href="#r076i-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><span hidden>开放接口 · 后续版本</span><strong>not authorized, unread, and unpublished</strong></header><p>独立重证 Zhang Proposition 4.2、sharp polynomial dependence、exact-shear matching lower bound、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076i-boundary">R0.76I Step 60 的 conditional-literature 与 exact-shear 边界</h3>'
        '<p><a href="https://arxiv.org/abs/2607.10501v1">Ruizhe Zhang, arXiv:2607.10501v1</a> Proposition 4.2 提供无频率分离的 sparse-Fourier endpoint extrapolation；该 34 页 2026-07 v1 预印本不表述为已同行评审，本站也没有独立重现其 Hardy-space proof。<a href="https://www.mathnet.ru/eng/sm8670">Erdelyi 2017</a> Theorems 2.3、2.20 与 equation (1.2) 提供 interior、Markov derivative 与 Kós endpoint inputs。Zhang Proposition 8.4 的 confluent complex witness 只作较大 sparse-Fourier class 的范围限定语境，不转写成 exact real dyadic heat-shear sharpness。</p>'
        '<div class="boundary"><strong>R0.76I Step 60 公开边界 · CHEBYSHEV-SCALE FULL-PLATEAU WINDOW</strong><p>'
        'LITERATURE：Zhang Proposition 4.2 与 Erdelyi/Kós 三项 exponential-sum inequalities。'
        'PROVED LOCALLY：bilateral rescaling、full-plateau geometry、polynomial derivative/terminal consequences、complete four-row reconstruction、physical powers 与 asymptotic implication。'
        'CONDITIONAL-LITERATURE：组合 boxed theorem 只对 exact real one-band constant shears 给出 q⁷ exp(12√2q√Δ_a) 代价、q=o(L^(5/2)) 充分窗口与精确 normalized rate -2/11907。'
        'FINITE COMPUTATION：只绑定 exact ledgers、bytes、powers、signs、tags 与 claim boundaries，不证明 imported continuum theorem。'
        'OPEN：独立重证 Zhang Proposition 4.2、sharp polynomial dependence、matching exact-shear lower bound、multiple bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。'
        '<strong>NO FULL-CLASS SHARPNESS CLAIM. NO VERSION-M CLAIM. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76i.html">阅读完整笔记</a> · '
        f'<a href="/{RECAP_SLUG}.html">阅读截至 I 的 milestone recap</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
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


def render_recap() -> str:
    slugs = route_post_r060_slugs(HOME.read_text(encoding="utf-8"))
    if len(slugs) != 203 or slugs[0] != "r0-61" or slugs[-1] != "r0-76i":
        raise RuntimeError(f"R0.76I recap route coverage drift: {len(slugs)} {slugs[:1]} {slugs[-1:]}")
    links = "\n".join(f'<a href="/notes/{slug}.html">{slug[3:].upper()}</a>' for slug in slugs)
    return rf'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>R0.61–R0.76I 累计里程碑回顾｜从 exp(Cq) 障碍到条件性切比雪夫尺度窗口</title>
<meta name="description" content="R0.61 至 R0.76I 的 203 节累计回顾，区分 E 的统一指数障碍、F–H 的显式候选链与 I 的文献条件性 q=o(L^(5/2)) exact-shear 窗口">
<link rel="canonical" href="https://kasifa.github.io/{RECAP_SLUG}.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\(","\\)"]],displayMath:[["\\[","\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.7 Georgia,"Songti SC","Noto Serif SC",serif}}nav{{padding:12px 5vw;border-top:5px solid var(--ink);border-bottom:3px double var(--ink);display:flex;justify-content:space-between;gap:1rem}}main{{width:min(1040px,90vw);margin:auto}}header{{padding:55px 0 30px;border-bottom:1px solid var(--line)}}h1{{font-size:clamp(2rem,5vw,3.7rem);line-height:1.08}}h2{{color:var(--rule);margin-top:2.4rem}}section{{border-bottom:1px dotted var(--line);padding-bottom:1.2rem}}.eyebrow{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.06em;text-transform:uppercase}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}}.card,.boundary{{background:var(--raised);border:1px solid var(--line);padding:1rem 1.2rem}}.node-links{{display:flex;flex-wrap:wrap;gap:.45rem}}.node-links a{{border:1px solid var(--line);padding:.2rem .45rem;text-decoration:none}}a{{color:var(--rule)}}code{{overflow-wrap:anywhere}}@media(max-width:720px){{body{{font-size:15px}}.grid{{grid-template-columns:1fr}}nav{{font-size:13px}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}nav{{display:none}}body{{font-size:8.5pt}}main{{width:auto}}header{{padding-top:0}}.card{{break-inside:avoid}}}}</style></head>
<body><nav><a href="/research-review.html">研究首页</a><span>R0.61–R0.76I · 2026-09-05</span></nav><main><header><p class="eyebrow">CUMULATIVE MILESTONE RECAP · 203 NODES</p><h1>从 exp(Cq) 障碍到条件性切比雪夫尺度窗口</h1><p>这是 R0.60 之后的累计里程碑回顾。收录节点：203；回顾截止时公开笔记：263。它逐字节保留截至 R0.75W 的上一版 recap，并把 R0.75X–R0.76I 十二节点接成一条可审计路线，重点区分 E、F–H 与 I 的不同证据等级。</p><p><a href="/{RECAP_SLUG}.pdf">下载同步累计回顾 PDF</a> · <a href="/notes/r0-76i.html">阅读 R0.76I Step 60</a> · <a href="/{PREVIOUS_RECAP_SLUG}.html">保留上一版 milestone recap</a></p></header>
<article><section id="retained"><p class="eyebrow">01 / RETAINED THROUGH W</p><h2>R0.61–R0.75W 的 191 节账本逐字节保留</h2><p>前一累计回顾仍是独立、不被重写的历史对象。它覆盖 clock compression、signed-flux 路线筛选、单模与 two-harmonic exact family，最终由 T–V 关闭 high-carrier pair，并由 W 的独立 local-energy route 支付 low carriers。</p></section>
<section id="e-barrier"><p class="eyebrow">02 / E · UNIFORM BARRIER</p><h2><code>exp(Cq)</code> 上界与 <code>q=o(L²)</code> 窗口</h2><p>R0.76E 对 exact real one-band constant shears 给出频率一致的 full-plateau estimate，但支付 <code>exp(Cq)</code>。因此它只在 <code>q=o(L²)</code> 下保留精确负对数率 <code>-2/11907</code>。这不是任意 packet 或 arbitrary-field theorem。</p></section>
<section id="fgh-chain"><p class="eyebrow">03 / F–H · EXPLICIT PACKET CHAIN</p><h2>空间下界、中心纤维通量与完整平台吸收必须分开</h2><div class="grid"><article class="card"><h3>F · spatial lower bound</h3><p>显式 shifted-binomial packet 证明 E 的固定空间 observation row 至少需要指数级 mode loss；实现例的 drift 为零，因此没有完整通量下界。</p></article><article class="card"><h3>G · central-fibre signed flux</h3><p>同一 packet 加入非零 drift 后，在完整时钟上相对 central-fibre proxy 产生指数 signed-flux lower bound；分母不是 physical plateau mass。</p></article><article class="card"><h3>H · candidate killed</h3><p>相邻完整 plateau fibres 以 <code>exp(O(m/a))</code> 成本吸收 cap；raw rate 为 <code>3/40000</code>，规范化精确率回到 <code>-2/11907</code>，所以只否定 G 的显式候选。</p></article></div></section>
<section id="i-window"><p class="eyebrow">04 / I · CONDITIONAL-LITERATURE</p><h2>缩小端点 gap 把充分窗口扩展到 <code>q=o(L^(5/2))</code></h2><p><strong>LITERATURE：</strong>Zhang 2026-07 arXiv v1 Proposition 4.2 给 arbitrary real-frequency sparse Fourier sums 的 endpoint extrapolation；Erdelyi/Kós 给 interior、Markov derivative 与 reverse-time endpoint inequalities。</p><p><strong>PROVED LOCALLY：</strong>完整 plateau 的 normalized exterior gap 为 <code>Δ_a=O(1/a)</code>；bilateral rescaling、polynomial derivative/terminal rows、complete-real four-row energy identity 与物理归一化给出</p><p>\[|\mathcal T_{{\boldsymbol n,R}}|\le C_Ia^{{2/3}}R^{{-1/3}}q^7e^{{12\sqrt2q\sqrt{{\Delta_a}}}}(M_{{\boldsymbol n,R}}^{{\rm plat}})^{{2/3}}.\]</p><p><strong>CONDITIONAL-LITERATURE：</strong>组合 theorem 依赖未在本站独立重证的 Zhang Proposition 4.2；它只覆盖 exact real one-band constant shears。<code>q=o(L^(5/2))</code> 吸收指数和多项式损失，规范化精确率仍为 <code>-2/11907</code>，因此允许 <code>q</code> 与 <code>L²</code> 同阶。</p></section>
<section id="open-next"><p class="eyebrow">05 / OPEN BOUNDARY</p><h2>距离 arbitrary nonlinear field 仍有结构性缺口</h2><p>独立重证 Zhang Proposition 4.2、sharp polynomial dependence、matching exact-shear lower bound、multiple dyadic bands、nonconstant shear、arbitrary nonlinear packets、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍 OPEN。后续版本未授权、未读取、未发布。<strong>NO FULL-CLASS SHARPNESS CLAIM. NOT CLAY.</strong></p></section>
<section id="audit"><p class="eyebrow">06 / AUDIT BOX</p><h2>冻结 commit、证书与证据等级</h2><div class="boundary"><p><strong>Core commit：</strong><code>{frozen_import.SOURCE_COMMIT}</code></p><p><strong>Core parent：</strong><code>{frozen_import.CORE_PARENT_COMMIT}</code></p><p><strong>Handoff：</strong><code>{frozen_import.HANDOFF_COMMIT}</code></p><p><strong>Handoff SHA-256：</strong><code>{frozen_import.HANDOFF_SHA256}</code></p><p><strong>Main / primary / source SHA-256：</strong><code>{frozen_import.FROZEN['research/r076i_chebyshev_scale_full_plateau_window.md']}</code> / <code>{frozen_import.FROZEN['research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md']}</code> / <code>{frozen_import.FROZEN['research/r076i_report-source.md']}</code></p><p><strong>Certificate：</strong>Python 129/129；Ruby 129/129；I.1–I.38；42/42 displays；3 seeds byte-identical；129 targeted mutations rejected by both implementations。</p><p><strong>Scope：</strong>12/12 frozen files；无正式科学图、simulation、DNS 或 DGX；finite checks 不验证 imported 34-page preprint。CONDITIONAL-LITERATURE. NOT CLAY.</p></div></section>
<section id="node-index"><p class="eyebrow">NODE INDEX / 203</p><h2>R0.61–R0.76I 全部节点</h2><div class="node-links">{links}</div></section></article></main></body></html>'''


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 263 or pdf_count not in (219, 220):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    post_r060 = len(route_post_r060_slugs(route_page))
    if post_r060 != 203:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76i.html",
        "latestPublishedResearchPdf": "/notes/r0-76i.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 203,
        "latestRecapRelease": CODE,
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-05",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076h":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 165
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 60
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "CHEBYSHEV_SCALE_FULL_PLATEAU_WINDOW_FOR_EXACT_ONE_BAND_CONSTANT_SHEARS",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "CONDITIONAL_LITERATURE_ANALYTIC_EXACT_SHEAR_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "novelty_or_priority": "NOT_CLAIMED",
            "imported_input": "ZHANG_2026_ARXIV_V1_PROPOSITION_4_2_UNREFEREED",
            "literature": "ZHANG_PROPOSITION_4_2_ERDELYI_THEOREMS_2_3_2_20_KOS_ENDPOINT",
            "proved_locally": "GEOMETRY_BILATERAL_RESCALING_DERIVATIVE_TERMINAL_FOUR_ROW_PHYSICAL_ASYMPTOTIC",
            "composite_theorem": "CONDITIONAL_LITERATURE",
            "packet_scope": "EXACT_REAL_ONE_BAND_CONSTANT_SHEARS_ONLY",
            "spatial_cost": "Q2_EXP_12_SQRT2_Q_SQRT_DELTA_A",
            "complete_cost": "Q7_EXP_12_SQRT2_Q_SQRT_DELTA_A",
            "mode_window": "Q_LITTLE_O_L_TO_5_OVER_2",
            "normalized_rate": "EXACT_MINUS_TWO_OVER_11907",
            "full_class_sharpness": "NOT_CLAIMED_OPEN_IN_EXACT_SHEAR_CLASS",
            "multiple_bands": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "arbitrary_nonlinear_packets": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED",
            "complete_version_m_extraction": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_129_OF_129",
            "independent_ruby": "PASS_129_OF_129",
            "negative_mutations": "PASS_PYTHON_129_OF_129_RUBY_129_OF_129",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_I1_TO_I38_TAGS_AND_42_OF_42_DISPLAYS",
            "literature_boundary": "FINITE_CERTIFICATE_DOES_NOT_VALIDATE_IMPORTED_PREPRINT",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76i.html",
            "target_pdf": "/notes/r0-76i.pdf",
            "target_primary_figure": None,
            "recap_update_required": True,
            "recap_terminal_release": "R0.76I_STEP60",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076i_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 60,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 203,
        "postR070APublishedReleaseCount": 165,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076j",
        "latestPublishedResearchHtml": "/notes/r0-76i.html",
        "latestPublishedResearchPdf": "/notes/r0-76i.pdf",
        "latestReleaseGate": "tests/r076i-step60-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076i-step60-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076i-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076i-step60-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076i-step60-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076i-step60-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076i-step60-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076i-step60",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "coreParentCommit": frozen_import.CORE_PARENT_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT,
            "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False,
            "recapRequired": True,
        },
        "latestRecapRelease": RELEASE,
        "latestRecapHtml": f"/{RECAP_SLUG}.html",
        "latestRecapPdf": f"/{RECAP_SLUG}.pdf",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_target),
    }
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-76i.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        write_text(PUBLIC / f"{RECAP_SLUG}.html", render_recap())
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
        for target, expected in RECAP_HASHES.items():
            if sha256(target) != expected:
                raise RuntimeError(f"protected W milestone recap drift after generation: {target.relative_to(ROOT)}")
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 60,
        "siteVersion": VERSION,
        "recapUpdated": True,
        "recapNodes": 203,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "theoremStatus": "CONDITIONAL_LITERATURE",
        "modeWindow": "Q_LITTLE_O_L_TO_5_OVER_2",
        "normalizedRate": "MINUS_TWO_OVER_11907",
        "arbitraryPacketClaim": False,
        "unconditionalVersionMClaim": False,
        "laterReleaseAuthorized": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
