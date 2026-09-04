#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75O Step 40 from the verified R0.75N Step 39 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075n_step39_release as previous
import import_r075o_step40_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "b461b2a3ab32f511f10d19bb1743517ee212f6f4"
VERSION = "2.19"
RELEASE = "r075o"
CODE = "R0.75O"
TITLE = "R0.75O｜常剪切下竖向扩散保留 packet flux 增益"
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
            raise RuntimeError(f"R0.75O frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075o_vertical_diffusion_packet_gain_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 19
        or certificate.get("assertions", {}).get("passed") != 19
        or len(certificate.get("checks", {})) != 19
    ):
        raise RuntimeError("R0.75O certificate verdict drift")
    main = (ROOT / "research/r075o_vertical_diffusion_packet_gain.md").read_text()
    for token in (
        r"\tag{O.1}",
        r"\frac{|B|\mathcal W_\infty}{4K^2}E_0",
        "No upper vertical-frequency bound was used",
        r"\tag{O.12}",
        r"\Gamma_K",
        r"\frac{e^{-3/2}}{16\pi}",
        r"\tag{O.17}",
        r"p_{K,23}^{\rm tor}",
        r"\frac{98605}{71442}",
        "strict inequality is required",
        r"\frac{4279}{238140000}",
        r"\tag{O.24}",
        "not yet the Version-M payment",
        "No\nnovelty or priority claim",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75O boundary drift: {token}")


def render_step40_sections() -> str:
    source = (ROOT / "research/r075o_vertical_diffusion_packet_gain.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 314
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
    if section_index != 320:
        raise RuntimeError(f"Step 40 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.18"', 'data-site-version="2.19"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.18", "/i18n-en.js?v=2.19", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="For constant shear, vertical diffusion preserves the K^(-2/3) signed packet-flux gain under a total-frequency cap; the arbitrary-vertical-frequency energy row needs no cap.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75o.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75O · STEP 40 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75O · Step 40 · VERTICAL-DIFFUSION PACKET GAIN</div><h1>{TITLE}</h1><p>对常剪切 <strong>B</strong>，竖向 heat semigroup 的 L2 contraction 保留任意竖向频率的能量行：先消去 diagonal，再用 Schur 得到精确 <strong>1/4</strong> 系数。若另加 total-frequency cap 与 <strong>K^2T&gt;=1</strong>，二维短时 cubic mass 恢复 <strong>K^(-2/3)</strong> flux gain；接入 N 的 collar row 后，严格阈值为 <strong>kappa &gt; 98605/71442</strong>。该界只针对 packet 自己的 full-T2 atom，不是更小的 Version-M collar payment。<strong>E.24 OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">CONSTANT SHEAR</span><span class="label">VERTICAL DIFFUSION</span><span class="label">ARBITRARY VERTICAL FREQUENCIES</span><span class="label">DIAGONAL REMOVED FIRST</span><span class="label">SCHUR 1/4</span><span class="label">TOTAL-FREQUENCY CAP</span><span class="label">REAL PACKET</span><span class="label">K^2 T &gt;= 1</span><span class="label">K^-2/3 GAIN</span><span class="label">KAPPA &gt; 98605/71442</span><span class="label">KAPPA = 3/2 CLOSES</span><span class="label">FULL-T2 ATOM ONLY</span><span class="label">VERSION-M PAYMENT OPEN</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75O STEP 40</strong><p>model：constant shear</p><p>energy row：arbitrary vertical frequencies</p><p>cubic row：total-frequency capped</p><p>flux factor：1/(4K^2)</p><p>cubic gain：K^(-2/3)</p><p>threshold：kappa&gt;98605/71442</p><p>frozen kappa：3/2</p><p>payment：OWN FULL-T2 ATOM</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step40_sections() + '\n<section id="reproduce">', "Step 40 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 40 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075o_vertical_diffusion_packet_gain.md">Step 40 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075o_vertical_diffusion_packet_gain_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075o_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075o_vertical_diffusion_packet_gain_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075o_vertical_diffusion_packet_gain_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075o_vertical_diffusion_packet_gain_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075o_vertical_diffusion_packet_gain_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075o_vertical_diffusion_packet_gain_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075o_vertical_diffusion_packet_gain_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075o_vertical_diffusion_packet_gain_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075o_vertical_diffusion_packet_gain_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075o_vertical_diffusion_packet_gain_qa.sh">QA script</a></p><p><a href="/notes/r0-75o.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 19/19、Ruby 20/20、O.1--O.24 与 24/24 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 132/132 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 40 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-308">← Step 39：radial-collar averaged Wiener row</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 40 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">physical-collar localization, nonconstant shear and packet summation remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75O Step 40 停止。常剪切下的 arbitrary-vertical-frequency energy row 已闭合；加 total-frequency cap 后，二维 cubic conversion 保留 K^(-2/3) gain，并在 frozen kappa=3/2 下以 packet 自己的 full-T2 atom 支付。physical-collar localization、nonconstant shear、inter-packet summation、low horizontal differences、移除 total upper-frequency cap、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均继续开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 40 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.18"', 'data-site-version="2.19"', "home version"),
        ("/i18n-en.js?v=2.18", "/i18n-en.js?v=2.19", "home i18n"),
        ("/site-refresh.js?v=2.18.1", "/site-refresh.js?v=2.19.1", "home refresh"),
        ("<strong>v2.18</strong>网页版本", "<strong>v2.19</strong>网页版本", "home stat version"),
        ("<strong>R0.75N</strong>最新研究节点", "<strong>R0.75O</strong>最新研究节点", "home latest"),
        ("<strong>242</strong>公开研究笔记", "<strong>243</strong>公开研究笔记", "home public count"),
        ("展开 152 篇公开笔记", "展开 153 篇公开笔记", "home route count"),
        ("综述 v2.18 · 2026-09-04", "综述 v2.19 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75N", "Research topology · R0.1–R0.75O", "home topology"),
        ('href="#r075n">跳到首页 R0.75N 卡片 →', 'href="#r075o">跳到首页 R0.75O 卡片 →', "home jump"),
        ("R0.70A–R0.75N：144 节已公开，104 节完整封存", "R0.70A–R0.75O：145 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75N</span>', '<span class="route-range">R0.69P–R0.75O</span>', "home range"),
        ("<h3>R0.75N：canonical radial collar 的 averaged Wiener row</h3>", "<h3>R0.75O：常剪切竖向扩散下的 packet flux gain</h3>", "home route title"),
        ("R0.72R–R0.75N：</span>", "R0.72R–R0.75O：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75N"', 'aria-label="R0.69P–R0.75O"', "home links label"),
        ("全站现有 242 篇公开研究笔记", "全站现有 243 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75O Step 40 证明常剪切下竖向 diffusion 不破坏 packet flux 的 K^(-2/3) gain：能量行允许任意竖向频率，cubic conversion 行需 total-frequency cap；physical-collar localization、nonconstant shear、inter-packet 与 low differences 仍未闭合。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75O · 2026-09-04 · STEP 40 · VERTICAL-DIFFUSION PACKET GAIN</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">常剪切下，vertical heat semigroup 的 L2 contraction 给出 arbitrary-vertical-frequency energy row；加 total-frequency cap 与 K^2T&gt;=1 后，二维 packet 保留 K^(-2/3) cubic gain。接入 N 的 collar row 后，严格阈值 kappa&gt;98605/71442，frozen kappa=3/2 闭合。界只针对 packet 自己的 full-T2 atom，不是 Version-M collar payment。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75o.pdf">阅读最新 R0.75O 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">243 篇研究笔记总索引</a><a href="#r075o">查看首页 R0.75O 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75O · 145 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75O Step 40 vertical-diffusion packet gain</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 40 proves that vertical diffusion preserves the K^(-2/3) packet-flux gain for constant shear: the energy row allows arbitrary vertical frequencies, while cubic conversion uses a total-frequency cap; the bound pays only against the packet own full-T2 atom.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row / dynamical and local payment open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain / physical-collar localization and packet summation open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75n.html">R0.75N</a>', '<a class="milestone" href="/notes/r0-75n.html">R0.75N</a>\n<a class="milestone" href="/notes/r0-75o.html">R0.75O</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>physical-collar localization, nonconstant shear and packet summation remain open</h3><p>仍需把 packet 自己的 full-T2 cubic atom 局部化到 physical buffered collar，处理 nonconstant shear、inter-packet summation 与 low horizontal differences，并移除 cubic conversion 的 total upper-frequency cap；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075o" data-release="r075o" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75O Step 40 · 2026-09-04 · VERTICAL-DIFFUSION PACKET GAIN</p><h3>{TITLE}</h3><p>常剪切下，vertical L2 contraction 保留 arbitrary-vertical-frequency energy estimate；对 real total-frequency-capped packet，短时二维 cubic conversion 给出 K^(-2/3) gain。N 的 collar row 与 frozen kappa=3/2 闭合 normalized coefficient，但只支付 packet 自己的 full-T2 atom。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75o.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75o.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075n"'
    if anchor not in page:
        raise RuntimeError("home R0.75N card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.18"', 'data-site-version="2.19"', "literature version"),
        ("/i18n-en.js?v=2.18", "/i18n-en.js?v=2.19", "literature i18n"),
        ("文献综述 v2.18 · 2026-09-04", "文献综述 v2.19 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75N 只列为研究笔记", "本站 R0.69P–R0.75O 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>vertical diffusion, local payment and packet summation remain open</strong></header><p>universal-cutoff、vertical diffusion、nonconstant shear、buffered-collar local cubic payment、inter-packet summation 与 low difference frequencies 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75O</b><strong>vertical diffusion preserves the packet flux gain for constant shear</strong></header><p>Step 40 用 vertical heat-semigroup contraction 与 Schur estimate 证明 arbitrary-vertical-frequency energy row；对 real total-frequency-capped packet，再由 short-time two-dimensional cubic conversion 保持 K^(-2/3) gain。N 的 collar row 给出严格 kappa threshold，frozen kappa=3/2 闭合，但只支付 packet 自己的 full-T2 atom。<a href="/notes/r0-75o.html">研究笔记</a> <a href="#r075o-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>physical-collar localization, nonconstant shear and packet summation remain open</strong></header><p>physical buffered-collar cubic localization、nonconstant shear、inter-packet summation、low horizontal differences 与移除 total upper-frequency cap 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075o-boundary">R0.75O Step 40 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Coti Zelati--Gallay 2023 给出 higher-dimensional parallel shear 与 transverse diffusion 的相邻语境；Bedrossian--Coti Zelati 2017 研究 shear-flow semigroup 与 enhanced dissipation；Albritton--Beekie--Novack 2022 说明 nonconstant shear 的 hypoelliptic mechanism。R0.75O 的 exact Wiener-row Schur bound、full-T2 short-time cubic conversion 与 frozen local normalization 均为本地证明。有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75O Step 40 公开边界</strong><p>'
        'PROVED：arbitrary-vertical-frequency energy estimate O.4--O.12；total-frequency-capped cubic conversion O.13--O.17；canonical collar insertion O.18--O.20；strict paid-frequency threshold O.21--O.22；frozen kappa=3/2 closure O.23--O.24。'
        'SCOPE：constant shear；the energy row needs no upper vertical-frequency cap；the cubic row uses a finite real packet with n^2+j^2&lt;=4K^2 and K^2T&gt;=1；O.24 pays only against the packet own full-T2 atom。'
        'OPEN：physical buffered-collar cubic localization、nonconstant shear、inter-packet summation、low horizontal differences、removal of the total upper-frequency cap、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75o.html">阅读完整笔记</a> · '
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
    if html_count != 243 or pdf_count not in (199, 200):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 183:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75o.html",
        "latestPublishedResearchPdf": "/notes/r0-75o.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075n":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 145
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 40
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "CONSTANT_SHEAR_VERTICAL_DIFFUSION_PACKET_FLUX_GAIN",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": "43a9b617df0b2478dbdfa649335d6b4040e926b7",
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_VERTICAL_DIFFUSION_PACKET_GAIN",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "constant_shear_model": "PROVED_O4_TO_O12",
            "arbitrary_vertical_frequency_energy_row": "PROVED_WITHOUT_UPPER_VERTICAL_CAP_O4_TO_O12",
            "diagonal_cancellation": "REMOVED_BEFORE_ABSOLUTE_VALUES_O9_TO_O12",
            "vertical_heat_semigroup": "L2_CONTRACTION_O10",
            "energy_flux_constant": "ABS_T_LE_ABS_B_W_INFINITY_E0_OVER_4K2_O12",
            "total_frequency_capped_real_packet": "GAMMA_K_O13_TO_O17",
            "short_time_cubic_lower_bound": "E_MINUS_3_OVER_2_E0_3_OVER_2_OVER_16PIK2_O17",
            "packet_flux_gain": "K_MINUS_2_OVER_3_O2_O20",
            "collar_row_input": "W_INFINITY_LE_C_VARTheta_L_FROM_R075N_O18",
            "normalized_flux": "R_ONE_THIRD_OMEGA_ONE_THIRD_K_MINUS_TWO_THIRDS_O20",
            "strict_kappa_threshold": "KAPPA_GT_98605_OVER_71442_O22",
            "threshold_equality": "FAILS_BECAUSE_L_GROWS",
            "frozen_kappa": "THREE_OVER_TWO_CLOSES_O23_O24",
            "payment_scope": "PACKET_OWN_FULL_T2_ATOM_ONLY_NOT_VERSION_M",
            "physical_collar_localization": "OPEN_NOT_PROVED",
            "inter_packet_summation": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "low_horizontal_difference_sector": "OPEN_NOT_PROVED",
            "removal_of_total_upper_frequency_cap": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_19_OF_19",
            "independent_ruby": "PASS_20_OF_20",
            "negative_mutations": "PASS_PYTHON_132_OF_132_RUBY_132_OF_132",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_O1_TO_O24_24_OF_24",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75o.html",
            "target_pdf": "/notes/r0-75o.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075o_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 40,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 145,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075p",
        "latestPublishedResearchHtml": "/notes/r0-75o.html",
        "latestPublishedResearchPdf": "/notes/r0-75o.pdf",
        "latestReleaseGate": "tests/r075o-step40-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075o-step40-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075o-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075o-step40-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075o-step40-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075o-step40-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075o-step40-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075o-step40",
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
    write_text(PUBLIC / "notes/r0-75o.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 40,
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
