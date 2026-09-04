#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76G Step 58 from the verified R0.76F Step 57 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076f_step57_release as previous
import import_r076g_step58_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "0458100dfcc96ff7c6eb0c2999cb60ece605e5f7"
VERSION = "2.37"
RELEASE = "r076g"
CODE = "R0.76G"
TITLE = "R0.76G｜完整时钟中心纤维通量的指数下界"
RECAP_SLUG = "recap-r0-61-r0-75w"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
    PUBLIC / "recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
base_inline_markup = previous.inline_markup


def inline_markup(value: str) -> str:
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
            raise RuntimeError(f"protected W milestone recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.76G frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsPassed") != 120
        or certificate.get("assertionsTotal") != 120
        or not all(
            value is True
            for group in certificate.get("checks", {}).values()
            for value in group.values()
        )
        or len(certificate.get("negativeMutations", [])) != 120
    ):
        raise RuntimeError("R0.76G certificate verdict drift")
    main = (ROOT / "research/r076g_complete_clock_central_fibre_flux_lower_bound.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{G.1}", r"\tag{G.10}", r"\tag{G.20}", r"\tag{G.30}", r"\tag{G.40}",
        r"q=2m+1", r"n_q=4m=2n_1", r"B=-\frac{\beta a}{R}",
        r"\left(\frac97\right)^{4m}", r"\frac{q(L)}{L^2}\longrightarrow\frac2{3969}",
        "The numerator in G.8 is the complete signed flux", "not the full physical plateau mass", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76G boundary drift: {token}")
    source_report = (ROOT / "research/r076g_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "No completeness, novelty, or priority claim is made" not in compact:
        raise RuntimeError("R0.76G bounded source-claim boundary drift")


def render_step58_sections() -> str:
    source = (ROOT / "research/r076g_complete_clock_central_fibre_flux_lower_bound.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 455
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
        elif re.match(r"^\d+\. ", lines[0]):
            items = []
            current = ""
            for line in lines:
                if re.match(r"^\d+\. ", line):
                    if current:
                        items.append(current)
                    current = re.sub(r"^\d+\. ", "", line)
                else:
                    current += " " + line.strip()
            if current:
                items.append(current)
            output.append("<ol>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ol>")
        else:
            output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    if section_index != 464:
        raise RuntimeError(f"Step 58 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.36"', 'data-site-version="2.37"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.36", "/i18n-en.js?v=2.37", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="An explicit exponential lower bound for the complete-clock signed collar flux against a central-fibre proxy in an exact real dyadic shear.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76g.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76G · STEP 58 · 2026-09-05</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76G · Step 58 · COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND</div><h1>{TITLE}</h1><p>G 把 F 的零漂移空间观测障碍推进到非零漂移、完整冻结时钟和完全积分的 signed collar flux：在显式 exact real dyadic shear 上，完整 signed flux 相对中心纤维 proxy 的比值至少按 <code>β(9/7)^(4m)</code> 增长，且 <code>q(L)/L²→2/3969</code>。分母不是完整 physical plateau mass，因此这不是对 E、E.24 或 Version-M 的反例。<strong>NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">COMPLETE CLOCK</span><span class="label">SIGNED FLUX LOWER BOUND</span><span class="label">NONZERO DRIFT</span><span class="label">CENTRAL-FIBRE PROXY</span><span class="label">(9/7)^(4M)</span><span class="label">Q / L² → 2/3969</span><span class="label">EXACT REAL DYADIC SHEAR</span><span class="label">NO FULL-PLATEAU LOWER BOUND</span><span class="label">NO VERSION-M COUNTEREXAMPLE</span><span class="label">NO ARBITRARY PACKETS</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76G STEP 58</strong><p>m：floor(a²/1024)</p><p>q：2m+1</p><p>modes：2m, ..., 4m</p><p>band：4m = 2(2m)</p><p>β：1/100</p><p>B：-βa/R ≠ 0</p><p>clock：0 ≤ s ≤ 4</p><p>terminal：3 &lt; s &lt; 4</p><p>flux：complete and signed</p><p>ratio：at least c*β(9/7)^(4m)</p><p>denominator：central fibre only</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step58_sections() + '\n<section id="reproduce">', "Step 58 sections")
    evidence = '''<section id="reproduce"><div class="section-no">G / 冻结证据</div><h2>Step 58 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076g_complete_clock_central_fibre_flux_lower_bound.md">Step 58 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076g_complete_clock_central_fibre_flux_lower_bound_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076g_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076g_complete_clock_central_fibre_flux_lower_bound_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076g_complete_clock_central_fibre_flux_lower_bound_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076g_complete_clock_central_fibre_flux_lower_bound_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076g_complete_clock_central_fibre_flux_lower_bound_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076g_complete_clock_central_fibre_flux_lower_bound_qa.sh">QA script</a></p><p><a href="/notes/r0-76g.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 120/120、Ruby 120/120、G.1--G.40、40/40 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 120/120 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 Gaussian limiting lemma 的 continuum proof；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 58 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>F 的空间障碍与 G 的完整时钟 signed-flux 障碍</h2><p><a href="#s-450">F：2^(q-1) spatial-observation lower bound</a> · <a href="#s-456">G：complete-clock central-fibre flux lower bound</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 58 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.76H QUEUED</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">H remains unread until G is fully verified online</h2><p style="margin:.15rem 0">本站当前发布至 R0.76G Step 58。H 已进入唯一 FIFO 发布队列，但在 G 完成全部上线核验前不读取、不公开。G 的 lower bound 针对完整时钟上的 complete signed flux，但分母仅为 central-fibre proxy；它不能替换为完整 physical plateau mass，也不是对 R0.76E、E.24 或 Version-M 的反例。full-plateau mode dependence、optimal exponential base、arbitrary packets、nonconstant shears、Version-M membership and extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 58 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.36"', 'data-site-version="2.37"', "home version"),
        ("/i18n-en.js?v=2.36", "/i18n-en.js?v=2.37", "home i18n"),
        ("/site-refresh.js?v=2.36.1", "/site-refresh.js?v=2.37.1", "home refresh"),
        ("<strong>v2.36</strong>网页版本", "<strong>v2.37</strong>网页版本", "home stat version"),
        ("<strong>R0.76F</strong>最新研究节点", "<strong>R0.76G</strong>最新研究节点", "home latest"),
        ("<strong>260</strong>公开研究笔记", "<strong>261</strong>公开研究笔记", "home public count"),
        ("展开 170 篇公开笔记", "展开 171 篇公开笔记", "home route count"),
        ("综述 v2.36 · 2026-09-04", "综述 v2.37 · 2026-09-05", "home footer"),
        ("Research topology · R0.1–R0.76F", "Research topology · R0.1–R0.76G", "home topology"),
        ('href="#r076f">跳到首页 R0.76F 卡片 →', 'href="#r076g">跳到首页 R0.76G 卡片 →', "home jump"),
        ("R0.70A–R0.76F：162 节已公开，104 节完整封存", "R0.70A–R0.76G：163 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76F</span>', '<span class="route-range">R0.69P–R0.76G</span>', "home range"),
        ("<h3>R0.76F：继承空间观测的指数下界</h3>", "<h3>R0.76G：完整时钟中心纤维通量的指数下界</h3>", "home route title"),
        ("R0.72R–R0.76F：</span>", "R0.72R–R0.76G：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76F"', 'aria-label="R0.69P–R0.76G"', "home links label"),
        ("全站现有 260 篇公开研究笔记", "全站现有 261 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76G Step 58 构造非零漂移 exact real dyadic shear，在完整冻结时钟上得到 complete signed collar flux 相对 central-fibre proxy 的 exp(cq) 下界；分母不是完整 physical plateau mass，因此不构成对 E、E.24 或 Version-M 的反例。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76G · 2026-09-05 · STEP 58 · COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">G 用非零漂移 exact real dyadic packet 在完整冻结时钟上证明 complete signed collar flux 相对 central-fibre proxy 至少按 β(9/7)^(4m) 增长，且 q/L²→2/3969。它不转移为 full-plateau lower bound。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76g.pdf">阅读最新 R0.76G 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">261 篇研究笔记总索引</a><a href="#r076g">查看首页 R0.76G 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76G · 163 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76G Step 58 complete-clock central-fibre flux lower bound</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">G gives an exp(cq) lower bound for the complete-clock signed collar flux against a central-fibre proxy in an exact nonzero-drift shear; the full physical plateau denominator remains open.</p>', "home current summary")
    page = replace_once(page, 'exp(C q log(q+1)) growing-mode window → delayed stable-clock exp(C q) upper loss → exact binomial 2^(q-1) spatial-observation lower bound; complete signed flux, arbitrary packets, arbitrary fields, and Version-M extraction open</p>', 'delayed stable-clock exp(C q) upper loss → exact binomial 2^(q-1) spatial-observation lower bound → nonzero-drift complete-clock signed-flux exp(cq) lower bound against a central-fibre proxy; full plateau, arbitrary packets, arbitrary fields, and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76f.html">R0.76F</a>', '<a class="milestone" href="/notes/r0-76f.html">R0.76F</a>\n<a class="milestone" href="/notes/r0-76g.html">R0.76G</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.76H</span><span class="tree-state current">QUEUED</span></div><h3>H remains unread until G is fully verified online</h3><p>H 已进入唯一 FIFO 发布队列，但在 G 完成全部上线核验前不读取、不公开。G 的 complete signed-flux lower bound 使用 central-fibre proxy；不能替换为完整 physical plateau mass，也不是对 E、E.24 或 Version-M 的反例。full-plateau mode dependence、optimal exponential base、arbitrary packets、nonconstant shears、Version-M membership and extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076g" data-release="r076g" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76G Step 58 · 2026-09-05 · COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND</p><h3>{TITLE}</h3><p>G 选择 m=floor(a²/1024)、q=2m+1 与非零漂移 B=-βa/R，在完整冻结时钟上证明 complete signed collar flux 相对 central-fibre proxy 至少按 β(9/7)^(4m) 增长。分母不是完整 physical plateau mass；不作 E.24、Version-M、regularity 或 singularity 反例主张。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76g.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76g.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076f"'
    if anchor not in page:
        raise RuntimeError("home R0.76F card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.36"', 'data-site-version="2.37"', "literature version"),
        ("/i18n-en.js?v=2.36", "/i18n-en.js?v=2.37", "literature i18n"),
        ("文献综述 v2.36 · 2026-09-04", "文献综述 v2.37 · 2026-09-05", "literature footer"),
        ("本站 R0.69P–R0.76F 只列为研究笔记", "本站 R0.69P–R0.76G 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76G</b><strong>complete-clock central-fibre signed-flux lower bound</strong></header><p>Step 58 取 <code>m=floor(a²/1024)</code>、<code>q=2m+1</code>、modes <code>2m,...,4m</code> 与非零 drift <code>B=-βa/R</code>，在完整冻结时钟上证明 complete signed collar flux 相对 central-fibre proxy 至少按 <code>β(9/7)^(4m)</code> 增长，且 <code>q(L)/L²→2/3969</code>。分母不是完整 physical plateau mass，因此不构成对 E、E.24 或 Version-M 的反例。<a href="/notes/r0-76g.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076g-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.76H</b><strong>queued; unread until G is fully verified online</strong></header><p>H 已进入唯一 FIFO 发布队列，但在 G 完成全部上线核验前不读取、不公开。full-plateau mode dependence、optimal exponential base、arbitrary packets、nonconstant shears、Version-M membership and extraction、arbitrary-field E.24、fixed deletion、suitable-weak transfer、regularity 与 singularity仍开放。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · R0\.76G</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076g-boundary">R0.76G Step 58 的 bounded primary-source screen 与主张边界</h3>'
        '<p><a href="https://arxiv.org/abs/1711.04279">Wang--Wang--Zhang--Zhang 2017</a> 与 <a href="https://arxiv.org/abs/1711.06088">Egidi--Veselic 2018</a> 给出 heat observability 的 thickness/spectral-inequality 背景；<a href="https://arxiv.org/abs/math/0307158">Miller 2004</a> 和 <a href="https://arxiv.org/abs/1806.00969">Laurent--Leautaud 2021</a> 记录 small-time cost、geometry 与 vanishing structure；<a href="https://www.mathnet.ru/eng/aa397">Nazarov</a>、<a href="https://arxiv.org/abs/1809.09726">Tikhonov--Yuditskii</a> 提供从 F 继承的 exponential-polynomial boundary。G 不导入 observability theorem，而以显式 periodic Gaussian expectation 和 elementary moment estimates 证明本地 functional；bounded search 不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.76G Step 58 公开边界 · COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND</strong><p>'
        'PROVED：取 m=floor(a²/1024)、q=2m+1、positive modes 2m,...,4m、β=1/100 与 B=-βa/R，得到 exact real smooth unforced NSE shear；在完整 scaled clock 0&lt;=s&lt;=4 上，complete signed flux 相对 central-fibre L3 proxy 的 ratio 至少为 c*β(9/7)^(4m)。并且 q(L)/L²→2/3969，normalized liminf rate 大于 2/35721。'
        'SIGN AND CLOCK：cutoff 在 terminal interval (3,4) 等于一；positive cap favourable，negative cap 是唯一 adverse contribution，base ratio 为 4/9；central upper base 来自 233/200&lt;7/6。'
        'SOURCE BOUNDARY：周边 heat-observability 与 Remez 文献不陈述 G 的 signed shrinking-collar functional；G 不作 novelty、priority 或 optimal-base claim。'
        'OPEN：分母 M_L^I 不是完整 physical plateau mass；full-plateau mode dependence、optimal exponential base、arbitrary packets、nonconstant shears、Version-M membership/extraction、arbitrary-field E.24、fixed deletion、suitable-weak transfer、regularity 与 singularity仍开放。finite checks 不代替 Gaussian limiting lemma；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>COMPLETE CLOCK. SIGNED FLUX LOWER BOUND. CENTRAL-FIBRE PROXY ONLY. NO FULL-PLATEAU LOWER BOUND. NO VERSION-M COUNTEREXAMPLE. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76g.html">阅读完整笔记</a> · '
        f'<a href="/{RECAP_SLUG}.html">保留截至 W 的 milestone recap</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 261 or pdf_count not in (217, 218):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 201:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76g.html",
        "latestPublishedResearchPdf": "/notes/r0-76g.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-05",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076f":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 163
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 58
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "COMPLETE_CLOCK_CENTRAL_FIBRE_SIGNED_FLUX_LOWER_BOUND",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_COMPLETE_CLOCK_SIGNED_FLUX_LOWER_BOUND",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "mode_count": "Q_EQUALS_TWO_M_PLUS_ONE",
            "m_rule": "FLOOR_A_SQUARED_OVER_1024",
            "integer_modes": "TWO_M_THROUGH_FOUR_M",
            "dyadic_band": "FOUR_M_EQUALS_TWO_TIMES_TWO_M",
            "drift": "B_EQUALS_MINUS_BETA_A_OVER_R_NONZERO",
            "scaled_clock": "ZERO_TO_FOUR_COMPLETE_CLOCK_TERMINAL_THREE_TO_FOUR",
            "complete_signed_flux": "LOWER_BOUND_PROVED_AGAINST_CENTRAL_FIBRE_PROXY",
            "flux_ratio_lower_bound": "C_STAR_BETA_TIMES_NINE_SEVENTHS_TO_FOUR_M",
            "mode_density": "Q_OVER_L_SQUARED_TO_TWO_OVER_3969",
            "normalized_rate": "LIMINF_AT_LEAST_FOUR_LOG_NINE_SEVENTHS_OVER_3969_MINUS_TWO_OVER_11907_GT_TWO_OVER_35721",
            "positive_cap": "FAVOURABLE_SIGN",
            "negative_cap": "ONLY_ADVERSE_CONTRIBUTION_BASE_RATIO_FOUR_NINTHS",
            "central_upper_base": "233_OVER_200_LT_SEVEN_SIXTHS",
            "central_fibre_proxy": "NOT_FULL_PHYSICAL_PLATEAU_MASS",
            "full_plateau_lower_bound": "NOT_PROVED",
            "r076e_e24_version_m_counterexample": "NOT_CLAIMED",
            "external_inputs": "HEAT_OBSERVABILITY_AND_REMEZ_CONTEXT_ONLY_NO_THEOREM_IMPORTED",
            "local_deductions": "EXPLICIT_PERIODIC_GAUSSIAN_EXPECTATION_AND_ELEMENTARY_MOMENT_ESTIMATES",
            "optimal_exponential_base": "OPEN_NOT_PROVED",
            "arbitrary_growing_packets": "OPEN_NOT_PROVED",
            "nonconstant_or_vertical_shear": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_120_OF_120",
            "independent_ruby": "PASS_120_OF_120",
            "negative_mutations": "PASS_PYTHON_120_OF_120_RUBY_120_OF_120",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_G1_TO_G40_TAGS_AND_40_OF_40_DISPLAYS",
            "exact_fixtures": "PASS_M3_Q7_MODES_6_TO_12_AND_EXACT_RATIONAL_LEDGER",
            "continuum_boundary": "FINITE_CERTIFICATE_IS_NOT_PROOF_OF_GAUSSIAN_LIMITING_LEMMA_OR_FULL_PLATEAU_TRANSFER",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76g.html",
            "target_pdf": "/notes/r0-76g.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076g_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 58,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 163,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076h",
        "latestPublishedResearchHtml": "/notes/r0-76g.html",
        "latestPublishedResearchPdf": "/notes/r0-76g.pdf",
        "latestReleaseGate": "tests/r076g-step58-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076g-step58-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076g-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076g-step58-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076g-step58-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076g-step58-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076g-step58-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076g-step58",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "coreParentCommit": frozen_import.CORE_PARENT_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT,
            "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False,
            "recapRequired": False,
        },
        "latestRecapRelease": "r075w",
        "latestRecapHtml": "/recap-r0-61-r0-75w.html",
        "latestRecapPdf": "/recap-r0-61-r0-75w.pdf",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_target),
    }
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-76g.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
        for target, expected in RECAP_HASHES.items():
            if sha256(target) != expected:
                raise RuntimeError(f"protected W milestone recap drift after generation: {target.relative_to(ROOT)}")
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 58,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "completeClockSignedFluxLowerBound": "C_STAR_BETA_TIMES_NINE_SEVENTHS_TO_FOUR_M",
        "centralFibreProxyOnly": True,
        "fullPlateauLowerBoundClaim": False,
        "completeFluxLowerBoundClaim": True,
        "arbitraryGrowingPacketClaim": False,
        "arbitraryFieldClaim": False,
        "unconditionalVersionMClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
