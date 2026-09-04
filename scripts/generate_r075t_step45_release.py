#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75T Step 45 from the verified R0.75S Step 44 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075s_step44_release as previous
import import_r075t_step45_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "44bd7ca8deb935640b7511f517529ac66e4a6a36"
VERSION = "2.24"
RELEASE = "r075t"
CODE = "R0.75T"
TITLE = "R0.75T｜单个二谐波 dyadic pair 的空间 collar coercivity"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75a.html": "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
    PUBLIC / "recap-r0-61-r0-75a.pdf": "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
base_inline_markup = previous.inline_markup


def inline_markup(value: str) -> str:
    """Render the frozen source's lightweight inline Markdown for the public reader."""
    rendered = base_inline_markup(value)
    return re.sub(r"`([^`\n]+)`", r"<code>\1</code>", rendered)


def baseline_text(relative: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{BASELINE_COMMIT}:{relative}"], cwd=ROOT, text=True
    )


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected R0.75A recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75T frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075t_two_harmonic_collar_coercivity_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionCount") != 14
        or len(certificate.get("assertions", [])) != 14
    ):
        raise RuntimeError("R0.75T certificate verdict drift")
    main = (ROOT / "research/r075t_two_harmonic_collar_coercivity.md").read_text()
    for token in (
        r"\tag{T.1}",
        r"H_{d,\ell}^2",
        r"\tag{T.3}",
        r"4\pi a\delta_0R^2",
        r"\tag{T.10}",
        r"\tag{T.13}",
        r"\tag{T.24}",
        r"\tag{T.27}",
        r"\tag{T.29}",
        r"\tag{T.30}",
        r"\tag{T.31}",
        "does **not** yet prove",
        "complete two-harmonic signed flux is bounded",
        "No novelty or",
        "priority claim is made",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75T boundary drift: {token}")


def render_step45_sections() -> str:
    source = (ROOT / "research/r075t_two_harmonic_collar_coercivity.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 350
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
    if section_index != 357:
        raise RuntimeError(f"Step 45 reader section drift: {section_index}")
    # The PDF browser occasionally exposes \qquad as literal text in the
    # generated print layer.  Equivalent explicit thin-space pairs avoid that
    # renderer defect without changing the frozen Markdown source or formula.
    rendered = "\n".join(output).replace(r"\qquad", r"\;\;")
    return rendered.replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.23"', 'data-site-version="2.24"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.23", "/i18n-en.js?v=2.24", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Spatial collar coercivity for exactly two harmonics in one high-carrier dyadic pair, with sharp beat degeneracy and an exact four-frequency flux identity.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75t.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75T · STEP 45 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75T · Step 45 · TWO-HARMONIC SPATIAL COLLAR COERCIVITY</div><h1>{TITLE}</h1><p>对同一 dyadic band 内恰好两个 real harmonics，在 <strong>maR &gt;= C_0</strong> 的 high-carrier 条件下，physical plateau collar 的空间三次质量由显式 beat defect 控制。退化率是 sharp；exact diffusive pair 只得到 time-slice corollary 与 four-frequency flux identity，尚未得到完整二模时间付款。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">SPATIAL THEOREM</span><span class="label">EXACTLY TWO HARMONICS</span><span class="label">ONE DYADIC PAIR</span><span class="label">HIGH CARRIER</span><span class="label">EXACT PLATEAU FIBRE</span><span class="label">SLOW-ENVELOPE COERCIVITY</span><span class="label">BEAT DEFECT</span><span class="label">SHARP DEGENERACY</span><span class="label">UNEQUAL HEAT RATES</span><span class="label">FOUR-FREQUENCY FLUX</span><span class="label">TEMPORAL PAYMENT OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75T STEP 45</strong><p>scope：exactly two harmonics</p><p>band：1 &lt;= m &lt; k &lt;= 2m</p><p>carrier：maR &gt;= C_0</p><p>defect：H_(d,aR)</p><p>geometry：4 pi a delta_0 R^2</p><p>mass：c a^2 R^3 H^3</p><p>heat rates：retained unequal</p><p>flux rows：2k / 2m / d / k+m</p><p>open：weighted temporal d-row</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step45_sections() + '\n<section id="reproduce">', "Step 45 sections")
    evidence = '''<section id="reproduce"><div class="section-no">T / 冻结证据</div><h2>Step 45 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075t_two_harmonic_collar_coercivity.md">Step 45 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075t_two_harmonic_collar_coercivity_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075t_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075t_two_harmonic_collar_coercivity_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075t_two_harmonic_collar_coercivity_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075t_two_harmonic_collar_coercivity_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075t_two_harmonic_collar_coercivity_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075t_two_harmonic_collar_coercivity_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075t_two_harmonic_collar_coercivity_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075t_two_harmonic_collar_coercivity_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075t_two_harmonic_collar_coercivity_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075t_two_harmonic_collar_coercivity_qa.sh">QA script</a></p><p><a href="/notes/r0-75t.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 14/14、Ruby 15/15、T.1--T.31、31/31 tags 与 32/32 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 52/52 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限探针不证明 continuum coercivity constants；本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 45 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-344">← Step 44：single-harmonic complete-clock payment</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 45 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">weighted temporal difference-frequency payment remains OPEN</h2><p style="margin:.15rem 0">本站在 R0.75T Step 45 停止。T 只证明 high-carrier dyadic pair 的空间 collar coercivity、exact diffusive time-slice corollary 与 four-frequency flux identity；它没有证明 weighted temporal difference-frequency estimate 或 complete two-harmonic signed-flux payment，也不覆盖 low-carrier pairs、三个及以上 harmonics、arbitrary packets、nonconstant shear、vertical dependence、projection、E.24 或 Version-M extraction。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 45 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.23"', 'data-site-version="2.24"', "home version"),
        ("/i18n-en.js?v=2.23", "/i18n-en.js?v=2.24", "home i18n"),
        ("/site-refresh.js?v=2.23.1", "/site-refresh.js?v=2.24.1", "home refresh"),
        ("<strong>v2.23</strong>网页版本", "<strong>v2.24</strong>网页版本", "home stat version"),
        ("<strong>R0.75S</strong>最新研究节点", "<strong>R0.75T</strong>最新研究节点", "home latest"),
        ("<strong>247</strong>公开研究笔记", "<strong>248</strong>公开研究笔记", "home public count"),
        ("展开 157 篇公开笔记", "展开 158 篇公开笔记", "home route count"),
        ("综述 v2.23 · 2026-09-04", "综述 v2.24 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75S", "Research topology · R0.1–R0.75T", "home topology"),
        ('href="#r075s">跳到首页 R0.75S 卡片 →', 'href="#r075t">跳到首页 R0.75T 卡片 →', "home jump"),
        ("R0.70A–R0.75S：149 节已公开，104 节完整封存", "R0.70A–R0.75T：150 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75S</span>', '<span class="route-range">R0.69P–R0.75T</span>', "home range"),
        ("<h3>R0.75S：单实谐波的全频率 complete-clock collar payment</h3>", "<h3>R0.75T：单个二谐波 dyadic pair 的空间 collar coercivity</h3>", "home route title"),
        ("R0.72R–R0.75S：</span>", "R0.72R–R0.75T：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75S"', 'aria-label="R0.69P–R0.75T"', "home links label"),
        ("全站现有 247 篇公开研究笔记", "全站现有 248 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75T Step 45 闭合 high-carrier dyadic pair 的空间 two-harmonic collar coercivity，以 sharp beat defect 精确记录破坏性干涉；weighted temporal difference-frequency estimate 与 complete two-harmonic payment 仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75T · 2026-09-04 · STEP 45 · TWO-HARMONIC SPATIAL COLLAR COERCIVITY</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">同一 dyadic band 内恰好两个 real harmonics 在 <strong>maR &gt;= C_0</strong> 时满足空间 collar coercivity；显式 beat defect 同时记录 amplitude mismatch、beat scale 与 cancelling phase distance。time-slice corollary 保留 unequal heat rates，但 weighted temporal difference-frequency payment 仍未证明。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75t.pdf">阅读最新 R0.75T 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">248 篇研究笔记总索引</a><a href="#r075t">查看首页 R0.75T 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75T · 150 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75T Step 45 two-harmonic spatial collar coercivity</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 45 proves spatial two-harmonic collar coercivity for one high-carrier dyadic pair; the weighted temporal difference-frequency row and complete two-mode payment remain open.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment → spatially spread one-harmonic collar payment → plateau-only multimode obstruction → full-frequency single-harmonic complete-clock payment / multimode interference open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment → spatially spread one-harmonic collar payment → plateau-only multimode obstruction → full-frequency single-harmonic complete-clock payment → high-carrier two-harmonic spatial coercivity / temporal difference-frequency payment open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75s.html">R0.75S</a>', '<a class="milestone" href="/notes/r0-75s.html">R0.75S</a>\n<a class="milestone" href="/notes/r0-75t.html">R0.75T</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>weighted temporal difference-frequency payment remains open</h3><p>T 尚未控制 exact flux 中与 beat defect 同步移动的 low difference-frequency row，也未得到 complete two-harmonic signed-flux payment；low-carrier pairs、三个及以上 harmonics、arbitrary packets、nonconstant shear、vertical dependence、projection、E.24 与 Version-M extraction 仍开放。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075t" data-release="r075t" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75T Step 45 · 2026-09-04 · TWO-HARMONIC SPATIAL COLLAR COERCIVITY</p><h3>{TITLE}</h3><p>对一个 high-carrier dyadic pair，T 以显式 beat defect 证明 exact two-wave spatial collar coercivity，并保留 unequal heat damping 的 time-slice corollary与四个 nonconstant flux frequencies。它不是完整二模时间付款。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75t.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75t.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075s"'
    if anchor not in page:
        raise RuntimeError("home R0.75S card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.23"', 'data-site-version="2.24"', "literature version"),
        ("/i18n-en.js?v=2.23", "/i18n-en.js?v=2.24", "literature i18n"),
        ("文献综述 v2.23 · 2026-09-04", "文献综述 v2.24 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75S 只列为研究笔记", "本站 R0.69P–R0.75T 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>multimode interference and packet aggregation remain open</strong></header><p>两个及以上 harmonics 的 cubic interference、pairwise difference frequencies、nonconstant shear、arbitrary vertical structure、Version-M admissibility/aggregation 与 arbitrary-field E.24 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75T</b><strong>two-harmonic spatial collar coercivity for one dyadic pair</strong></header><p>Step 45 在 `maR&gt;=C_0` 下，对同一 dyadic band 内恰好两个 real harmonics 证明 phase-sharp spatial collar coercivity；exact beat defect 同时记录 amplitude mismatch、beat scale 与 cancelling relative phase。diffusive corollary 保留 unequal heat rates，four-frequency flux identity 也已精确展开，但 weighted temporal difference-frequency estimate 仍开放。<a href="/notes/r0-75t.html">研究笔记</a> <a href="#r075t-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>weighted temporal difference-frequency payment remains open</strong></header><p>仍需用同一 moving beat defect 支付 exact flux 的 low difference-frequency row，并兼容 self 与 sum rows；complete two-harmonic payment、low carriers、三个及以上 harmonics、arbitrary packets、nonconstant shear、vertical dependence、projection、E.24 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075t-boundary">R0.75T Step 45 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Kovrizhkin 2000 与 Egidi--Veselić 2020 给出 bounded spectral pieces 和 torus spectral subspaces 的相邻 Logvinenko--Sereda / observability 背景；它们不提供 T 的 exact two-real-wave defect、shrinking radial plateau fibre 或未证的 temporal row T.31。T 的 continuum inequality 由本地 elementary Gram/coercivity 论证直接证明，不导入这些外部定理。有限检索不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.75T Step 45 公开边界 · SPATIAL TWO-HARMONIC SCOPE</strong><p>'
        'PROVED：exact plateau fibre T.10；uniform slow-envelope sampling T.13；sharp unresolved-beat defect T.21--T.24；resolved-beat gap T.25--T.27；spatial cubic coercivity T.3；unequal-rate diffusive time-slice corollary T.6；以及 four-frequency flux identity T.30。'
        'OPEN：weighted temporal difference-frequency estimate T.31、complete two-harmonic signed-flux payment、low-carrier pairs、三个及以上 harmonics、arbitrary packets、inter-packet aggregation、nonconstant or vertically dependent shear、projection、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。T 不与 R 的 growing-mode obstruction 冲突。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO COMPLETE TWO-MODE PAYMENT. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75t.html">阅读完整笔记</a> · '
        '<a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 248 or pdf_count not in (204, 205):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 188:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75t.html",
        "latestPublishedResearchPdf": "/notes/r0-75t.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075s":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 150
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 45
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "SPATIAL_TWO_HARMONIC_DYADIC_PAIR_COLLAR_COERCIVITY",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": "1c7432ac79521f26aab3b32a0dd4a272484f2776",
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_POSITIVE_SPATIAL_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "two_harmonic_spatial_collar_coercivity": "PROVED_T3",
            "dyadic_pair_condition": "ONE_LE_M_LT_K_LE_2M",
            "high_carrier_condition": "MA_R_GE_C0_REQUIRED",
            "exact_plateau_fibre": "PROVED_T10",
            "slow_envelope_sampling": "PROVED_T13",
            "unresolved_beat_defect": "PROVED_T21_T24",
            "resolved_beat_gap": "PROVED_T25_T27",
            "sharp_degeneracy": "PROVED",
            "diffusive_time_slice_corollary": "PROVED_T6_UNEQUAL_HEAT_RATES_RETAINED",
            "four_frequency_flux_identity": "PROVED_T30",
            "weighted_temporal_difference_frequency_estimate": "OPEN_T31_NOT_PROVED",
            "complete_two_harmonic_signed_flux_payment": "OPEN_NOT_PROVED",
            "low_carrier_pair": "OPEN_NOT_PROVED",
            "three_or_more_harmonics": "OPEN_NOT_PROVED",
            "arbitrary_packets_and_inter_packet_aggregation": "OPEN_NOT_PROVED",
            "projection_from_larger_velocity": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "vertically_dependent_shear": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED",
            "complete_version_m_extraction": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_14_OF_14",
            "independent_ruby": "PASS_15_OF_15",
            "negative_mutations": "PASS_PYTHON_52_OF_52_RUBY_52_OF_52",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_T1_TO_T31_TAGS_31_OF_31_DISPLAYS_32_OF_32",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75t.html",
            "target_pdf": "/notes/r0-75t.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075t_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 45,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 150,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075u",
        "latestPublishedResearchHtml": "/notes/r0-75t.html",
        "latestPublishedResearchPdf": "/notes/r0-75t.pdf",
        "latestReleaseGate": "tests/r075t-step45-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075t-step45-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075t-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075t-step45-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075t-step45-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075t-step45-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075t-step45-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075t-step45",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT,
            "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False,
            "recapRequired": False,
        },
        "latestRecapRelease": "r075a",
        "latestRecapHtml": "/recap-r0-61-r0-75a.html",
        "latestRecapPdf": "/recap-r0-61-r0-75a.pdf",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_target),
    }
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-75t.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 45,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 169,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
