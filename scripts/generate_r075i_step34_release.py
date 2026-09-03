#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75I Step 34 from the verified R0.75H Step 33 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075h_step33_release as previous
import import_r075i_step34_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.13"
RELEASE = "r075i"
CODE = "R0.75I"
TITLE = "R0.75I｜扩散安全的单区块 flux 估计与有效参与数阈值"
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


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected R0.75A recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75I frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075i_diffusion_safe_block_participation_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 18
        or certificate.get("assertions", {}).get("passed") != 18
        or len(certificate.get("checks", {})) != 18
    ):
        raise RuntimeError("R0.75I certificate verdict drift")
    main = (ROOT / "research/r075i_diffusion_safe_block_participation.md").read_text()
    for token in (
        r"\mathfrak X_j",
        r"N_{\rm eff}",
        r"L^{2/3}\omega^{1/3}R^{-2/3}",
        r"\frac{8558}{35721}",
        r"\frac{27163}{35721}",
        r"-\frac{4279}{238140000}<0",
        r"\frac{27163}{476280000}>0",
        r"\tag{I.27}",
        "is sufficient, not necessary",
        "does **not** prove (I.3) for the frozen passive solution",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75I boundary drift: {token}")


def render_step34_sections() -> str:
    source = (ROOT / "research/r075i_diffusion_safe_block_participation.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 271
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
    if section_index != 278:
        raise RuntimeError(f"Step 34 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.12"', 'data-site-version="2.13"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.12", "/i18n-en.js?v=2.13", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A diffusion-safe one-block flux estimate yields an exact effective-participation threshold; multi-block occupation and signed cancellation remain open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75i.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75I · STEP 34 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75I · Step 34 · DIFFUSION-SAFE BLOCK PARTICIPATION</div><h1>{TITLE}</h1><p>不使用 passive PDE，仅由 support volume、系数界与 spacetime Hölder 得到单区块估计；有效参与数 <strong>N_eff</strong> 精确记录多区块聚合损失。条件 <strong>theta &lt; 8558/35721</strong> 等价于 <strong>beta &gt; 27163/35721</strong>，但实际扩散场的参与数控制仍未证明。<strong>SUFFICIENT ONLY. E.24 OPEN. NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">DIFFUSION-SAFE ONE BLOCK</span><span class="label">NO PDE USED</span><span class="label">N_EFF EXACT</span><span class="label">SUFFICIENT ONLY</span><span class="label">THETA &lt; 8558/35721</span><span class="label">BETA &gt; 27163/35721</span><span class="label">ONE-BLOCK RATE -4279/238140000</span><span class="label">UNIFORM RATE +27163/476280000</span><span class="label">HIGH PARTICIPATION NOT NECESSARY</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75I STEP 34</strong><p>one-block bound：PROVED</p><p>diffusion-safe algebra：PROVED</p><p>N_eff identity：PROVED</p><p>threshold：CONDITIONAL</p><p>high participation：NOT NECESSARY</p><p>signed cancellation：OPEN</p><p>E.24：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step34_sections() + '\n<section id="reproduce">', "Step 34 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 34 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075i_diffusion_safe_block_participation.md">Step 34 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075i_diffusion_safe_block_participation_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075i_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075i_diffusion_safe_block_participation_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075i_diffusion_safe_block_participation_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075i_diffusion_safe_block_participation_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075i_diffusion_safe_block_participation_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075i_diffusion_safe_block_participation_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075i_diffusion_safe_block_participation_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075i_diffusion_safe_block_participation_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075i_diffusion_safe_block_participation_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075i_diffusion_safe_block_participation_qa.sh">QA script</a></p><p><a href="/notes/r0-75i.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 18/18、Ruby 24/24、I.1--I.27 与 27/27 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 83/83 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 34 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-265">← Step 33：pure-transport terminal tube</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 34 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">多区块参与数或 signed cancellation 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75I Step 34 停止。单区块估计虽对 diffusion 安全，却没有证明实际扩散场满足 N_eff 阈值；高参与数也不是必要障碍。signed inter-block cancellation、transition bands、periodic recrossing、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均未闭合。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 34 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075i"[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.12"' in page:
        for old, new, label in (
            ('data-site-version="2.12"', 'data-site-version="2.13"', "home version"),
            ("/i18n-en.js?v=2.12", "/i18n-en.js?v=2.13", "home i18n"),
            ("/site-refresh.js?v=2.12.1", "/site-refresh.js?v=2.13.1", "home refresh"),
            ("<strong>v2.12</strong>网页版本", "<strong>v2.13</strong>网页版本", "home stat version"),
            ("<strong>R0.75H</strong>最新研究节点", "<strong>R0.75I</strong>最新研究节点", "home latest"),
            ("<strong>236</strong>公开研究笔记", "<strong>237</strong>公开研究笔记", "home public count"),
            ("展开 146 篇公开笔记", "展开 147 篇公开笔记", "home route count"),
            ("综述 v2.12 · 2026-09-03", "综述 v2.13 · 2026-09-03", "home footer"),
            ("Research topology · R0.1–R0.75H", "Research topology · R0.1–R0.75I", "home topology"),
            ('href="#r075h">跳到首页 R0.75H 卡片 →', 'href="#r075i">跳到首页 R0.75I 卡片 →', "home jump"),
            ("R0.70A–R0.75H：138 节已公开，104 节完整封存", "R0.70A–R0.75I：139 节已公开，104 节完整封存", "home accounting"),
            ('<span class="route-range">R0.69P–R0.75H</span>', '<span class="route-range">R0.69P–R0.75I</span>', "home range"),
            ("<h3>R0.75H：pure-transport terminal tube 与 R^(1/3) benchmark gain</h3>", "<h3>R0.75I：diffusion-safe block estimate 与 exact participation threshold</h3>", "home route title"),
            ("R0.72R–R0.75H：</span>", "R0.72R–R0.75I：</span>", "home detail range"),
            ('aria-label="R0.69P–R0.75H"', 'aria-label="R0.69P–R0.75I"', "home links label"),
            ("全站现有 236 篇公开研究笔记", "全站现有 237 篇公开研究笔记", "home recap count"),
        ):
            page = replace_once(page, old, new, label)
        page = replace_pattern(
            page,
            r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
            '<div class="summary-item"><strong>我目前关注</strong><span>R0.75I Step 34 用不依赖 passive PDE 的 one-block Hölder 估计定义 exact N_eff 聚合损失，并得到 theta&lt;8558/35721（等价 beta&gt;27163/35721）的条件阈值。实际扩散场的参与数控制或 signed inter-block cancellation 仍待证明。</span></div>',
            "home focus",
        )
        latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75I · 2026-09-03 · STEP 34 · DIFFUSION-SAFE BLOCK PARTICIPATION</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">单个 O(R^3) 区块上的 flux 由 support volume 与 spacetime Hölder 支付，严格 rate 为 -4279/238140000；N_eff^(1/3) 是精确聚合损失，theta&lt;8558/35721 才足以保持目标系数。全区块均匀参与的 rate 为 +27163/476280000，且高参与数不是必要障碍。E.24 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75i.pdf">阅读最新 R0.75I 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">237 篇研究笔记总索引</a><a href="#r075i">查看首页 R0.75I 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75I · 139 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75I Step 34 diffusion-safe block participation</span></div></div></section>'''
        page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
        page = replace_pattern(
            page,
            r'<p class="tree-current-summary">.*?</p>',
            '<p class="tree-current-summary">Step 34 proves a PDE-independent, diffusion-safe one-block flux estimate and identifies N_eff^(1/3) as the exact aggregation loss. The participation threshold is sufficient only; actual multi-block participation, signed cancellation, and E.24 remain open.</p>',
            "home current summary",
        )
        page = replace_once(
            page,
            'exact signed-flux threshold → pure-transport terminal tube / one-third benchmark / diffusive closure open</p>',
            'pure-transport terminal tube → diffusion-safe block estimate / exact participation threshold / multi-block dynamics open</p>',
            "home route path",
        )
        page = replace_once(
            page,
            '<a class="milestone" href="/notes/r0-75h.html">R0.75H</a>',
            '<a class="milestone" href="/notes/r0-75h.html">R0.75H</a>\n<a class="milestone" href="/notes/r0-75i.html">R0.75I</a>',
            "home milestone",
        )
    elif 'data-site-version="2.13"' not in page:
        raise RuntimeError("home baseline version drift")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>multi-block participation or signed cancellation remains unproved</h3><p>必须从 shear transport、diffusion 与 collar geometry 独立控制 N_eff，或证明足够强的 signed inter-block cancellation；单区块局部化本身不能闭合 E.24。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075i" data-release="r075i" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75I Step 34 · 2026-09-03 · DIFFUSION-SAFE BLOCK PARTICIPATION</p><h3>{TITLE}</h3><p>one-block flux estimate 不使用 passive PDE，N_eff^(1/3) 精确记录聚合损失；theta&lt;8558/35721 是 absolute block-summation route 的充分条件，但高参与数并非必要障碍。E.24 未闭合。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75i.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75i.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075h"'
    if anchor not in page:
        raise RuntimeError("home R0.75H card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075i-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.12"' in page:
        for old, new, label in (
            ('data-site-version="2.12"', 'data-site-version="2.13"', "literature version"),
            ("/i18n-en.js?v=2.12", "/i18n-en.js?v=2.13", "literature i18n"),
            ("文献综述 v2.12 · 2026-09-03", "文献综述 v2.13 · 2026-09-03", "literature footer"),
            ("本站 R0.69P–R0.75H 只列为研究笔记", "本站 R0.69P–R0.75I 只列为研究笔记", "literature intro"),
        ):
            page = replace_once(page, old, new, label)
        old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>diffusive terminal-tube control remains open</strong></header><p>必须加入 independent Feynman--Kac occupation、resolvent 或 separately paid source row，且不能把目标 dissipation 放回右侧；后续材料未授权、未读取、未公开。</p></div>'
        route = '<div class="route-step kept"><header><b>R0.75I</b><strong>diffusion-safe block flux and effective participation</strong></header><p>Step 34 证明不使用 passive PDE 的 arbitrary-field one-block estimate，并以 N_eff^(1/3) 精确记录多区块聚合损失；theta&lt;8558/35721 等价于 beta&gt;27163/35721。该条件只充分、不必要，高参与 zero mode 仍可有逐块零 flux。<a href="/notes/r0-75i.html">研究笔记</a> <a href="#r075i-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>multi-block participation or signed cancellation remains open</strong></header><p>必须独立控制实际 diffusing field 的 N_eff，或证明足够强的 signed inter-block cancellation；单区块估计本身不能闭合 E.24。后续材料未授权、未读取、未公开。</p></div>'
        page = replace_once(page, old_next, route, "literature route")
    elif 'data-site-version="2.13"' not in page:
        raise RuntimeError("literature baseline version drift")
    boundary = (
        '<h3 id="r075i-boundary">R0.75I Step 34 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Albritton--Dong 的 passive-scalar work 标识 bounded-total-speed drift 的特殊边界；'
        'Hu--Li 的 Davies weighted-semigroup 方法支持 off-diagonal heat-kernel 思路；'
        'Aronson 的经典结果给出其假设下的 Gaussian fundamental-solution bounds。'
        '没有一个 inspected source 给出 I.19 的参与数估计、signed cross-mode E.24 或 frozen Version-M payment ledger。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75I Step 34 公开边界</strong><p>'
        'PROVED：arbitrary-field one-block estimate I.10--I.14、exact participation identity/bounds I.15--I.17、'
        'conditional threshold I.19--I.23、adverse uniform-block rate I.24--I.26，以及 high-participation zero-flux diagnostic I.27。'
        'SUFFICIENT ONLY：N_eff&lt;=C R^(-theta) 且 theta&lt;8558/35721 可支付 absolute block-summation route；不等式不构成实际扩散场定理，高参与也不是必要障碍或 E.24 counterexample。'
        'OPEN：实际 diffusing field 的 N_eff bound、signed inter-block cancellation、shear-transition bands、periodic recrossing、E.24、complete clock、fixed deletion、suitable-weak transfer、'
        'regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75i.html">阅读完整笔记</a> · '
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
    if html_count != 237 or pdf_count not in (193, 194):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 177:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75i.html",
        "latestPublishedResearchPdf": "/notes/r0-75i.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075h":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 139
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30, "r075f": 31, "r075g": 32,
        "r075h": 33, "r075i": 34,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "DIFFUSION_SAFE_BLOCK_FLUX_AND_EFFECTIVE_PARTICIPATION_THRESHOLD",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_ARBITRARY_FIELD_ONE_BLOCK_ESTIMATE",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "one_block_diffusion_safe_estimate": "PROVED_I10_I14_NO_PDE_USED",
            "effective_participation_identity": "PROVED_I15_I17",
            "participation_finite_bounds": "PROVED_1_TO_CARDINALITY",
            "conditional_threshold": "THETA_STRICTLY_BELOW_8558_OVER_35721",
            "active_fraction_threshold": "BETA_STRICTLY_ABOVE_27163_OVER_35721",
            "one_block_rate": "NEGATIVE_4279_OVER_238140000",
            "uniform_full_block_rate": "POSITIVE_27163_OVER_476280000",
            "high_participation_zero_flux": "PROVED_I27_SUFFICIENT_NOT_NECESSARY",
            "actual_diffusing_field_participation_bound": "OPEN_NOT_PROVED",
            "signed_inter_block_cancellation": "OPEN_NOT_PROVED",
            "transition_bands_and_periodic_recrossing": "OPEN_NOT_PROVED",
            "arbitrary_real_E24": "OPEN",
            "complete_clock": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_18_OF_18",
            "independent_ruby": "PASS_24_OF_24",
            "negative_mutations": "PASS_PYTHON_83_OF_83_RUBY_83_OF_83",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_I1_TO_I27_27_OF_27",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75i.html",
            "target_pdf": "/notes/r0-75i.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075i_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 34,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 139,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075j",
        "latestPublishedResearchHtml": "/notes/r0-75i.html",
        "latestPublishedResearchPdf": "/notes/r0-75i.pdf",
        "latestReleaseGate": "tests/r075i-step34-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075i-step34-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075i-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075i-step34-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075i-step34-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075i-step34-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075i-step34-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075i-step34",
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
    write_text(PUBLIC / "notes/r0-75i.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 34,
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
