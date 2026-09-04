#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76F Step 57 from the verified R0.76E Step 56 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076e_step56_release as previous
import import_r076f_step57_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "975a83df17490fed95688234c89791bf4762a8d7"
VERSION = "2.36"
RELEASE = "r076f"
CODE = "R0.76F"
TITLE = "R0.76F｜继承空间观测的指数下界"
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
            raise RuntimeError(f"R0.76F frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076f_exponential_spatial_observation_lower_bound_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsPassed") != 83
        or certificate.get("assertionsTotal") != 83
        or not all(
            value is True
            for group in certificate.get("checks", {}).values()
            for value in group.values()
        )
        or len(certificate.get("negativeMutations", [])) != 83
    ):
        raise RuntimeError("R0.76F certificate verdict drift")
    main = (ROOT / "research/r076f_exponential_spatial_observation_lower_bound.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{F.1}", r"\tag{F.4}", r"\tag{F.10}", r"\tag{F.15}", r"\tag{F.18}",
        r"n_j=q+j-1", r"n_q=2q-1\le2q=2n_1", r"2^{q-1}",
        r"\frac{\sin(3x)}{\sin x}", r"\log C_q\ge(q-1)\log2",
        "not a lower bound for the complete collar flux", "No novelty, priority", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76F boundary drift: {token}")
    source_report = (ROOT / "research/r076f_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "This absence is not evidence of novelty or priority" not in compact:
        raise RuntimeError("R0.76F bounded source-claim boundary drift")


def render_step57_sections() -> str:
    source = (ROOT / "research/r076f_exponential_spatial_observation_lower_bound.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 449
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
    if section_index != 455:
        raise RuntimeError(f"Step 57 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.35"', 'data-site-version="2.36"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.35", "/i18n-en.js?v=2.36", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="An explicit 2^(q-1) lower bound for the inherited spatial observation constant in exact real dyadic shears.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76f.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76F · STEP 57 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76F · Step 57 · EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND</div><h1>{TITLE}</h1><p>F 在 E 的同一组嵌套区间与 exact real dyadic-shear fibre 内构造 <code>H=e^(iqδz)(1-e^(iδz))^(q-1)</code>，给出空间观测常数至少 <code>2^(q-1)</code>。因此这一观测步骤的 <code>exp(Theta(q))</code> 阶不可被统一常数或多项式替代；但构造取 <code>B=0</code>，完整 transport flux 为零，所以这不是完整 collar-flux 的指数下界。<strong>NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">EXACT REAL DYADIC SHEAR</span><span class="label">2^(Q-1) LOWER BOUND</span><span class="label">EXP(THETA(Q)) SHARPNESS</span><span class="label">BINOMIAL CONSTRUCTION</span><span class="label">POSITIVE FREQUENCIES</span><span class="label">FIXED I AND J</span><span class="label">B = 0</span><span class="label">SPATIAL ROW ONLY</span><span class="label">NO FULL-FLUX LOWER BOUND</span><span class="label">NO ARBITRARY PACKETS</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76F STEP 57</strong><p>q：integer q &gt;= 2</p><p>δ：0 &lt; δ &lt;= 2π/3</p><p>I：[-1/2, 1/2]</p><p>J：[-3/2, 3/2]</p><p>modes：q, ..., 2q-1</p><p>band：n_q &lt;= 2 n_1</p><p>amplitudes：binomial, nonnegative</p><p>observation：at least 2^(q-1)</p><p>order：exp(Theta(q))</p><p>shear：exact, B=0</p><p>complete flux：not lower-bounded</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step57_sections() + '\n<section id="reproduce">', "Step 57 sections")
    evidence = '''<section id="reproduce"><div class="section-no">F / 冻结证据</div><h2>Step 57 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076f_exponential_spatial_observation_lower_bound.md">Step 57 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076f_exponential_spatial_observation_lower_bound_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076f_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076f_exponential_spatial_observation_lower_bound_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076f_exponential_spatial_observation_lower_bound_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076f_exponential_spatial_observation_lower_bound_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076f_exponential_spatial_observation_lower_bound_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076f_exponential_spatial_observation_lower_bound_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076f_exponential_spatial_observation_lower_bound_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076f_exponential_spatial_observation_lower_bound_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076f_exponential_spatial_observation_lower_bound_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076f_exponential_spatial_observation_lower_bound_qa.sh">QA script</a></p><p><a href="/notes/r0-76f.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 83/83、Ruby 83/83、F.1--F.18、18/18 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 83/83 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 continuum norm inequality、导入的 Remez 事实或 Navier--Stokes embedding；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 57 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>E 的指数上界与 F 的指数阶下界</h2><p><a href="#s-442">E：exp(C q) linear modal-entropy window</a> · <a href="#s-450">F：2^(q-1) spatial-observation lower bound</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 57 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 开放边界</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">complete signed flux, arbitrary packets, and Version-M extraction remain OPEN</h2><p style="margin:.15rem 0">本站当前发布至 R0.76F Step 57。F 只证明同一 spatial observation row 的常数至少按 <code>2^(q-1)</code> 增长；实现例取 <code>B=0</code>，完整 transport flux 为零，因此没有得到 complete signed collar-flux 的指数下界，也未排除利用完整时空 cancellation 的其他证明。optimal exponential base、mode counts comparable with <code>L^2</code>、arbitrary packets、nonconstant shear、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 仍开放。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 57 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.35"', 'data-site-version="2.36"', "home version"),
        ("/i18n-en.js?v=2.35", "/i18n-en.js?v=2.36", "home i18n"),
        ("/site-refresh.js?v=2.35.1", "/site-refresh.js?v=2.36.1", "home refresh"),
        ("<strong>v2.35</strong>网页版本", "<strong>v2.36</strong>网页版本", "home stat version"),
        ("<strong>R0.76E</strong>最新研究节点", "<strong>R0.76F</strong>最新研究节点", "home latest"),
        ("<strong>259</strong>公开研究笔记", "<strong>260</strong>公开研究笔记", "home public count"),
        ("展开 169 篇公开笔记", "展开 170 篇公开笔记", "home route count"),
        ("综述 v2.35 · 2026-09-04", "综述 v2.36 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.76E", "Research topology · R0.1–R0.76F", "home topology"),
        ('href="#r076e">跳到首页 R0.76E 卡片 →', 'href="#r076f">跳到首页 R0.76F 卡片 →', "home jump"),
        ("R0.70A–R0.76E：161 节已公开，104 节完整封存", "R0.70A–R0.76F：162 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76E</span>', '<span class="route-range">R0.69P–R0.76F</span>', "home range"),
        ("<h3>R0.76E：精确剪切的线性模态熵窗口</h3>", "<h3>R0.76F：继承空间观测的指数下界</h3>", "home route title"),
        ("R0.72R–R0.76E：</span>", "R0.72R–R0.76F：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76E"', 'aria-label="R0.69P–R0.76F"', "home links label"),
        ("全站现有 259 篇公开研究笔记", "全站现有 260 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76F Step 57 在 E 的 exact real dyadic-shear observation geometry 内给出 2^(q-1) 下界，说明 exp(Theta(q)) 阶不可降为多项式。该例 B=0、完整 transport flux 为零，所以 complete signed flux 与任意包仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76F · 2026-09-04 · STEP 57 · EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">F 用 exact binomial dyadic packet 证明继承空间观测常数至少为 2^(q-1)，与 E 的 exp(Cq) 上界在指数阶相匹配。这只锁定 spatial row；实现例 B=0，完整 transport flux 为零。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76f.pdf">阅读最新 R0.76F 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">260 篇研究笔记总索引</a><a href="#r076f">查看首页 R0.76F 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76F · 162 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76F Step 57 exponential spatial-observation lower bound</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">F gives an explicit 2^(q-1) lower bound inside the exact real dyadic-shear observation geometry, so polynomial dependence on q is impossible for that row; it is not a complete-flux lower bound.</p>', "home current summary")
    page = replace_once(page, 'ultra-high heat-clock payment → exp(C q log(q+1)) growing-mode window → delayed stable-clock exp(C q) loss / q=o(L^2) exact-shear window; arbitrary packets, arbitrary fields, and Version-M extraction open</p>', 'exp(C q log(q+1)) growing-mode window → delayed stable-clock exp(C q) upper loss → exact binomial 2^(q-1) spatial-observation lower bound; complete signed flux, arbitrary packets, arbitrary fields, and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76e.html">R0.76E</a>', '<a class="milestone" href="/notes/r0-76e.html">R0.76E</a>\n<a class="milestone" href="/notes/r0-76f.html">R0.76F</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.76G</span><span class="tree-state current">QUEUED</span></div><h3>complete signed flux, arbitrary packets, and Version-M extraction</h3><p>G 已进入唯一 FIFO 发布队列，但在 F 完成全部上线核验前不读取、不公开。F 只锁定 inherited spatial observation row 的指数阶，且实现例 B=0、完整 transport flux 为零。matching complete-flux lower bound、full space-time cancellation、optimal exponential base、mode counts comparable with L^2、arbitrary packets、nonconstant shear、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity仍开放。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076f" data-release="r076f" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76F Step 57 · 2026-09-04 · EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND</p><h3>{TITLE}</h3><p>F 用 binomial amplitudes 与相位对齐构造 q 个正频率 q,...,2q-1，在固定 I/J 几何上得到 observation ratio 至少 2^(q-1)，从而排除这一空间步骤中的 uniform 或 polynomial q dependence。构造属于 exact smooth shear，但 B=0，不能推出 complete collar-flux 下界。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76f.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76f.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076e"'
    if anchor not in page:
        raise RuntimeError("home R0.76E card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.35"', 'data-site-version="2.36"', "literature version"),
        ("/i18n-en.js?v=2.35", "/i18n-en.js?v=2.36", "literature i18n"),
        ("文献综述 v2.35 · 2026-09-04", "文献综述 v2.36 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.76E 只列为研究笔记", "本站 R0.69P–R0.76F 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76F</b><strong>exponential lower bound for the inherited spatial observation</strong></header><p>Step 57 用 <code>e^(iqδz)(1-e^(iδz))^(q-1)</code> 的 phase-aligned real part，在 exact real positive-frequency dyadic shear fibre 与 E 的固定 I/J 几何内证明 observation ratio 至少 <code>2^(q-1)</code>。因此同一 spatial row 的 uniform 或 polynomial q dependence 不可能；实现例 <code>B=0</code>，不产生 complete collar-flux lower bound。<a href="/notes/r0-76f.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076f-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.76G</b><strong>queued; unread until F is fully verified online</strong></header><p>G 已进入唯一 FIFO 发布队列，但在 F 完成全部上线核验前不读取、不公开。F 只锁定 inherited spatial observation row 的指数阶；matching complete-flux lower bound、full space-time cancellation、optimal exponential base、mode counts comparable with L^2、arbitrary packets、nonconstant shear、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity仍开放。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · R0\.76F 尚未发布</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076f-boundary">R0.76F Step 57 的 bounded primary-source screen 与主张边界</h3>'
        '<p><a href="https://m.mathnet.ru/php/archive.phtml?jrnid=aa&amp;option_lang=eng&amp;paperid=397&amp;wshow=paper">Nazarov 1993/1994</a> 是 measurable local estimate 的原始来源；<a href="https://arxiv.org/abs/2606.24823">Friedland 2026 preprint</a> 明确记录一般 Turan--Nazarov 阶指数的 sharpness；<a href="https://doi.org/10.1007/s00365-019-09473-2">Tikhonov--Yuditskii 2020</a> 给出 fixed-geometry trigonometric Remez 的精确 circle constant。F 的 real positive-frequency dyadic specialization 与 <code>2^(q-1)</code> 常数是本地主文中的直接构造；bounded search 不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.76F Step 57 公开边界 · EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND</strong><p>'
        'PROVED：对 q&gt;=2、0&lt;δ&lt;=2π/3，存在频率 q,...,2q-1、非负 binomial amplitudes 与实 phases，使 E 的固定 I=[-1/2,1/2]、J=[-3/2,3/2] observation ratio 至少为 2^(q-1)。因此这一 spatial row 的有效常数满足 log C_q&gt;=(q-1)log2，uniform 或 polynomial q dependence 不可能。'
        'EXACT-SHEAR REALIZATION：取 δ=aR、B=0，构造是 smooth unforced exact heat shear 的初始 scaled fibre。'
        'ASYMPTOTIC BOUNDARY：若 q(L)/L^2 沿子列保持正下界，单纯优化该 observation row 不能保留精确 -2/11907 coefficient；小的 quadratic density 仍可能留下负的总指数。'
        'SOURCE BOUNDARY：一般 Remez/Turan--Nazarov 指数 sharpness 已见文献；F 不作 novelty、priority 或 optimal-base claim。'
        'OPEN：complete signed collar-flux lower bound、full space-time cancellation route、optimal exponential base、mode counts comparable with L^2、arbitrary packets、nonconstant shear、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。构造取 B=0，完整 transport flux 为零；finite checks 不代替 continuum theorem；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>SPATIAL ROW ONLY. EXP(THETA(Q)) ORDER SHARP. B=0. NO COMPLETE-FLUX LOWER BOUND. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76f.html">阅读完整笔记</a> · '
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
    if html_count != 260 or pdf_count not in (216, 217):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 200:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76f.html",
        "latestPublishedResearchPdf": "/notes/r0-76f.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076e":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 162
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 57
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "EXPONENTIAL_LOWER_BOUND_FOR_INHERITED_SPATIAL_OBSERVATION",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_SPATIAL_OBSERVATION_LOWER_BOUND",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "mode_count": "INTEGER_Q_AT_LEAST_TWO",
            "spacing": "ZERO_LT_DELTA_LE_TWO_PI_OVER_THREE",
            "intervals": "I_MINUS_HALF_TO_HALF_J_MINUS_THREE_HALVES_TO_THREE_HALVES",
            "integer_modes": "N_J_EQUALS_Q_PLUS_J_MINUS_ONE",
            "real_phases": "PHASE_ALIGNED_REAL_PART",
            "nonnegative_amplitudes": "BINOMIAL_COEFFICIENTS",
            "dyadic_band": "N_Q_EQUALS_TWO_Q_MINUS_ONE_LE_TWO_N_1",
            "spatial_observation_lower_bound": "AT_LEAST_TWO_TO_Q_MINUS_ONE",
            "observation_constant": "LOG_C_Q_AT_LEAST_Q_MINUS_ONE_TIMES_LOG_TWO",
            "uniform_or_polynomial_q_dependence": "IMPOSSIBLE_FOR_INHERITED_SPATIAL_ROW",
            "upper_lower_order_match": "EXP_THETA_Q_ONLY_NO_OPTIMAL_BASE_CLAIM",
            "exact_shear_embedding": "SMOOTH_UNFORCED_CONSTANT_PRESSURE_WITH_B_ZERO",
            "complete_transport_flux": "ZERO_FOR_REALIZING_EXAMPLE",
            "complete_collar_flux_lower_bound": "NOT_PROVED",
            "quadratic_mode_density": "CHANGES_EXACT_NORMALIZED_COEFFICIENT_ALONG_SUBSEQUENCE",
            "small_quadratic_density": "NEGATIVE_TOTAL_EXPONENT_MAY_STILL_REMAIN",
            "external_inputs": "GENERAL_TURAN_NAZAROV_AND_TRIGONOMETRIC_REMEZ_SHARPNESS_CONTEXT",
            "local_deductions": "EXPLICIT_BINOMIAL_DYADIC_REAL_SHEAR_SPECIALIZATION_AND_TWO_TO_Q_MINUS_ONE_BOUND",
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
            "python_certificate": "PASS_83_OF_83",
            "independent_ruby": "PASS_83_OF_83",
            "negative_mutations": "PASS_PYTHON_83_OF_83_RUBY_83_OF_83",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_F1_TO_F18_TAGS_AND_18_OF_18_DISPLAYS",
            "exact_fixtures": "PASS_Q4_MODES_4_TO_7_BINOMIAL_1_3_3_1_DELTA_TWO_PI_OVER_THREE_LOWER_BOUND_8",
            "continuum_boundary": "FINITE_CERTIFICATE_IS_NOT_PROOF_OF_CONTINUUM_NORM_INEQUALITY_IMPORTED_REMEZ_FACTS_OR_NAVIER_STOKES_EMBEDDING",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76f.html",
            "target_pdf": "/notes/r0-76f.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076f_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 57,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 162,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076g",
        "latestPublishedResearchHtml": "/notes/r0-76f.html",
        "latestPublishedResearchPdf": "/notes/r0-76f.pdf",
        "latestReleaseGate": "tests/r076f-step57-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076f-step57-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076f-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076f-step57-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076f-step57-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076f-step57-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076f-step57-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076f-step57",
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
    write_text(PUBLIC / "notes/r0-76f.html", render_note())
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
        "latestCompletedStep": 57,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "spatialObservationLowerBound": "TWO_TO_Q_MINUS_ONE",
        "observationOrderSharpness": "EXP_THETA_Q",
        "completeFluxLowerBoundClaim": False,
        "arbitraryGrowingPacketClaim": False,
        "arbitraryFieldClaim": False,
        "unconditionalVersionMClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
