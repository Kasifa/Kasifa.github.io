#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75N Step 39 from the verified R0.75M Step 38 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075m_step38_release as previous
import import_r075n_step39_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "78341fec702c64578682f81c887105d4a01e51d2"
VERSION = "2.18"
RELEASE = "r075n"
CODE = "R0.75N"
TITLE = "R0.75N｜径向 collar 平均后的 Wiener row 无 R^(-1) 损失"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75a.html": "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
    PUBLIC / "recap-r0-61-r0-75a.pdf": "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
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
            raise RuntimeError(f"protected R0.75A recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75N frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075n_radial_collar_averaged_wiener_row_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 16
        or certificate.get("assertions", {}).get("passed") != 16
        or len(certificate.get("checks", {})) != 16
    ):
        raise RuntimeError("R0.75N certificate verdict drift")
    main = (ROOT / "research/r075n_radial_collar_averaged_wiener_row.md").read_text()
    for token in (
        r"p=\frac{32}{63}",
        r"\tag{N.2}",
        r"\sum_{\ell\in\mathbb Z}",
        r"\|d_\ell\|_{L^\infty_{x_3}}",
        r"\tag{N.3}",
        "the supremum is taken separately",
        r"\tag{N.8}",
        "two integrations by parts",
        r"4\pi a\delta",
        r"\tag{N.12}",
        "K>=R^(-3/2)",
        r"\tag{N.17}",
        "canonical radial representative",
        "does not extend",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75N boundary drift: {token}")


def render_step39_sections() -> str:
    source = (ROOT / "research/r075n_radial_collar_averaged_wiener_row.md").read_text(encoding="utf-8").strip()
    # The frozen handoff contains one presentation-only TeX typo in (N.12).
    # Keep the audited source byte-exact and repair only the rendered reader.
    frozen_render_typo = r":=left\{"
    if source.count(frozen_render_typo) != 1:
        raise RuntimeError("R0.75N frozen N.12 render-typo count drift")
    source = source.replace(frozen_render_typo, r":=\left\{")
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 307
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
        elif len(lines) >= 2 and lines[0].startswith("|") and re.match(r"^\|[-:| ]+\|$", lines[1]):
            rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
            head = "".join(f"<th>{inline_markup(cell)}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{inline_markup(cell)}</td>" for cell in row) + "</tr>" for row in rows[2:])
            output.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
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
    if section_index != 314:
        raise RuntimeError(f"Step 39 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.17"', 'data-site-version="2.18"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.17", "/i18n-en.js?v=2.18", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A selectable canonical radial collar has an x1-averaged derivative Wiener row O(L), with no negative power of R, and a fully averaged row O(L^2 R)">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75n.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75N · STEP 39 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75N · Step 39 · RADIAL-COLLAR AVERAGED WIENER ROW</div><h1>{TITLE}</h1><p>对 frozen outer-collar construction 允许的一种 <strong>canonical smooth radial representative</strong>，横向平均消除了 pointwise derivative 看似存在的 <strong>R^(-1)</strong> 损失。系数逐个取 <strong>x_3 supremum</strong> 后再求和，得到 <strong>sum ||d_l||_infinity = O(L)</strong>；再平均 x_3 后得到 <strong>sum |D_l| = O(L^2 R)</strong>。这是 selectable geometric coefficient theorem，不是 universal-cutoff 或 dynamical-flux theorem。<strong>E.24 OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">CANONICAL RADIAL COLLAR</span><span class="label">SELECTABLE CUTOFF</span><span class="label">X1-AVERAGED ROW</span><span class="label">SUM-SUP ORDER</span><span class="label">D0 = 0</span><span class="label">NO R^-1 LOSS</span><span class="label">WIENER ROW O(L)</span><span class="label">FULL AVERAGE O(L^2 R)</span><span class="label">TANGENCY INCLUDED</span><span class="label">TWO IBP</span><span class="label">K &gt;= R^-3/2</span><span class="label">COEFFICIENT THEOREM ONLY</span><span class="label">DYNAMICAL FLUX OPEN</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75N STEP 39</strong><p>cutoff：SELECTABLE CANONICAL RADIAL</p><p>calibration：p=32/63, a=pL</p><p>Fourier sign：d_l=+i l Xi_l</p><p>zero mode：d_0=0</p><p>x1 row：O(L)</p><p>full row：O(L^2 R)</p><p>high K：K&gt;=R^-3/2</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step39_sections() + '\n<section id="reproduce">', "Step 39 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 39 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075n_radial_collar_averaged_wiener_row.md">Step 39 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075n_radial_collar_averaged_wiener_row_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075n_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075n_radial_collar_averaged_wiener_row_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075n_radial_collar_averaged_wiener_row_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075n_radial_collar_averaged_wiener_row_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075n_radial_collar_averaged_wiener_row_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075n_radial_collar_averaged_wiener_row_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075n_radial_collar_averaged_wiener_row_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075n_radial_collar_averaged_wiener_row_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075n_radial_collar_averaged_wiener_row_qa.sh">QA script</a></p><p><a href="/notes/r0-75n.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 16/16、Ruby 17/17、N.1--N.17 与 17/17 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 107/107 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 39 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-301">← Step 38：dyadic-packet diffusive gain</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 39 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">vertical diffusion, local payment and packet summation remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75N Step 39 停止。一个 selectable canonical radial collar 的 x_1-averaged Wiener row 已为 O(L)，fully averaged row 已为 O(L^2R)，且 high-frequency diagnostic 不产生 R 的负幂；universal-cutoff、vertical diffusion、nonconstant shear、buffered-collar local cubic payment、inter-packet summation、low differences、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均继续开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 39 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.17"', 'data-site-version="2.18"', "home version"),
        ("/i18n-en.js?v=2.17", "/i18n-en.js?v=2.18", "home i18n"),
        ("/site-refresh.js?v=2.17.1", "/site-refresh.js?v=2.18.1", "home refresh"),
        ("<strong>v2.17</strong>网页版本", "<strong>v2.18</strong>网页版本", "home stat version"),
        ("<strong>R0.75M</strong>最新研究节点", "<strong>R0.75N</strong>最新研究节点", "home latest"),
        ("<strong>241</strong>公开研究笔记", "<strong>242</strong>公开研究笔记", "home public count"),
        ("展开 151 篇公开笔记", "展开 152 篇公开笔记", "home route count"),
        ("综述 v2.17 · 2026-09-04", "综述 v2.18 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75M", "Research topology · R0.1–R0.75N", "home topology"),
        ('href="#r075m">跳到首页 R0.75M 卡片 →', 'href="#r075n">跳到首页 R0.75N 卡片 →', "home jump"),
        ("R0.70A–R0.75M：143 节已公开，104 节完整封存", "R0.70A–R0.75N：144 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75M</span>', '<span class="route-range">R0.69P–R0.75N</span>', "home range"),
        ("<h3>R0.75M：dyadic-packet signed flux 的 mode-count-free diffusive gain</h3>", "<h3>R0.75N：canonical radial collar 的 averaged Wiener row</h3>", "home route title"),
        ("R0.72R–R0.75M：</span>", "R0.72R–R0.75N：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75M"', 'aria-label="R0.69P–R0.75N"', "home links label"),
        ("全站现有 241 篇公开研究笔记", "全站现有 242 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75N Step 39 证明一个 selectable canonical radial collar 的 x_1-averaged derivative Wiener row 为 O(L)，fully averaged row 为 O(L^2R)，且高频系数诊断不损失 R 的负幂；vertical diffusion、local payment、inter-packet 与 low differences 仍未闭合。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75N · 2026-09-04 · STEP 39 · RADIAL-COLLAR AVERAGED WIENER ROW</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">一个 selectable canonical radial collar 经 x_1 averaging 后，其 coefficientwise-supremum Wiener row 为 O(L)，fully averaged row 为 O(L^2R)；exact slice geometry 覆盖 spherical tangency，low/high Fourier-sample split 避免 R^(-1) 损失。结论不延伸到 universal cutoff、dynamical flux 或 E.24。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75n.pdf">阅读最新 R0.75N 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">242 篇研究笔记总索引</a><a href="#r075n">查看首页 R0.75N 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75N · 144 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75N Step 39 radial-collar averaged Wiener row</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 39 proves that one selectable canonical radial collar has an x_1-averaged derivative Wiener row O(L) and a fully averaged row O(L^2R), with no negative power of R in the high-frequency coefficient diagnostic.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain / inter-packet and collar payment open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row / dynamical and local payment open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75m.html">R0.75M</a>', '<a class="milestone" href="/notes/r0-75m.html">R0.75M</a>\n<a class="milestone" href="/notes/r0-75n.html">R0.75N</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>vertical diffusion, local payment and packet summation remain open</h3><p>仍需把 one-dimensional constant-shear time kernel 扩展到 vertical diffusion 与 nonconstant shear，以 buffered collar atom 支付 local cubic mass，并控制 inter-packet summation 与 low difference frequencies；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075n" data-release="r075n" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75N Step 39 · 2026-09-04 · RADIAL-COLLAR AVERAGED WIENER ROW</p><h3>{TITLE}</h3><p>一个 selectable canonical radial collar 通过 exact slice geometry、first/third radial derivative ledger 与 low/high Fourier-sample split，得到 x_1-averaged Wiener row O(L) 及 fully averaged row O(L^2R)，不留下 R 的负幂。universal-cutoff、dynamical flux、local cubic payment 与 E.24 仍 OPEN。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75n.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75n.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075m"'
    if anchor not in page:
        raise RuntimeError("home R0.75M card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.17"', 'data-site-version="2.18"', "literature version"),
        ("/i18n-en.js?v=2.17", "/i18n-en.js?v=2.18", "literature i18n"),
        ("文献综述 v2.17 · 2026-09-04", "文献综述 v2.18 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75M 只列为研究笔记", "本站 R0.69P–R0.75N 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>inter-packet, frozen-collar and low-difference rows remain open</strong></header><p>inter-packet summation、frozen-collar W_xi calibration、local Version-M atom、nonconstant shear 与 low difference-frequency sector 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75N</b><strong>canonical radial-collar averaged Wiener row</strong></header><p>Step 39 对一个 selectable canonical radial collar 用 exact slice geometry、first/third radial derivative ledger 与 low/high Fourier-sample split 证明 x_1-averaged row O(L) 及 fully averaged row O(L^2R)，避免 R 的负幂。<a href="/notes/r0-75n.html">研究笔记</a> <a href="#r075n-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>vertical diffusion, local payment and packet summation remain open</strong></header><p>universal-cutoff、vertical diffusion、nonconstant shear、buffered-collar local cubic payment、inter-packet summation 与 low difference frequencies 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075n-boundary">R0.75N Step 39 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Garces--Rhodes--Peña 支持 physical projection 与 Fourier slice 的对应；Rux--Quellmalz--Steidl 提供 radial averaging、Abel-type relation 与 one-dimensional Fourier transform 的邻近框架；Herz 说明 convex boundary curvature 与 Fourier decay 的经典联系。R0.75N 的 discrete sampling split、coefficientwise x_3 supremum、tangency-area payment 及 frozen R,L scaling 均为本地证明。有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75N Step 39 公开边界</strong><p>'
        'PROVED：canonical radial collar N.1--N.5、scale-correct Fourier sampling lemma N.6--N.9、uniform x_1-averaged coefficient row N.10--N.13、fully averaged row N.14--N.16 与 high-frequency coefficient diagnostic N.17。'
        'SCOPE：one selectable canonical radial representative in the central torus chart；sum_l ||d_l||_infinity=O(L)，sum_l |D_l|=O(L^2R)，spherical tangencies included。'
        'OPEN：universal-cutoff statement、vertical diffusion、nonconstant shear、buffered-collar local cubic payment、inter-packet summation、low differences、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75n.html">阅读完整笔记</a> · '
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
    if html_count != 242 or pdf_count not in (198, 199):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 182:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75n.html",
        "latestPublishedResearchPdf": "/notes/r0-75n.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075m":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 144
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 39
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "CANONICAL_RADIAL_COLLAR_AVERAGED_WIENER_ROW_WITHOUT_R_NEGATIVE_LOSS",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_CANONICAL_RADIAL_COLLAR_WIENER_ROW",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "canonical_radial_cutoff": "SELECTABLE_ALLOWED_REPRESENTATIVE_N1_N5",
            "fourier_sign_and_zero_mode": "D_ELL_PLUS_I_ELL_XI_ELL_AND_D0_ZERO_N5",
            "sampling_lemma": "LOW_HIGH_TWO_IBP_R_NU_MINUS_ONE_N6_N9",
            "coefficientwise_supremum_order": "SUM_ELL_SUP_X3_PROVED_N2_N13",
            "x1_averaged_row": "O_L_WITHOUT_R_NEGATIVE_POWER_N2",
            "fully_averaged_row": "O_L_SQUARED_R_N3_N16",
            "spherical_tangency": "INCLUDED_BY_4_PI_A_DELTA_CAP_N12",
            "frequency_threshold": "K_GE_R_MINUS_3_OVER_2_DIAGNOSTIC_N17",
            "scope": "ONE_SELECTABLE_CANONICAL_RADIAL_COLLAR_CENTRAL_TORUS_CHART",
            "universal_cutoff_theorem": "OPEN_NOT_PROVED",
            "dynamical_flux_theorem": "OPEN_NOT_PROVED",
            "inter_packet_summation": "OPEN_NOT_PROVED",
            "buffered_collar_local_cubic_payment": "OPEN_NOT_PROVED",
            "vertical_diffusion": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "low_difference_frequency_sector": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED",
            "complete_clock": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_16_OF_16",
            "independent_ruby": "PASS_17_OF_17",
            "negative_mutations": "PASS_PYTHON_107_OF_107_RUBY_107_OF_107",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_N1_TO_N17_17_OF_17",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75n.html",
            "target_pdf": "/notes/r0-75n.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075n_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 39,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 144,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075o",
        "latestPublishedResearchHtml": "/notes/r0-75n.html",
        "latestPublishedResearchPdf": "/notes/r0-75n.pdf",
        "latestReleaseGate": "tests/r075n-step39-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075n-step39-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075n-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075n-step39-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075n-step39-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075n-step39-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075n-step39-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075n-step39",
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
    write_text(PUBLIC / "notes/r0-75n.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 39,
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
