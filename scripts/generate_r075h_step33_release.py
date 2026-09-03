#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75H Step 33 from the verified R0.75G Step 32 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075g_step32_release as previous
import import_r075h_step33_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.12"
RELEASE = "r075h"
CODE = "R0.75H"
TITLE = "R0.75H｜纯输运 collar flux 的单程终端管闭合：R^(1/3) 增益在弹道基准中实现"
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
            raise RuntimeError(f"R0.75H frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075h_single_pass_transport_flux_closure_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 19
        or certificate.get("assertions", {}).get("passed") != 19
        or len(certificate.get("checks", {})) != 19
    ):
        raise RuntimeError("R0.75H certificate verdict drift")
    main = (ROOT / "research/r075h_single_pass_transport_flux_closure.md").read_text()
    for token in (
        r"\mathfrak X_{\xi,R}^{\rm tr}(H,q)",
        r"[\mathcal T_{\xi,\eta}^{\rm tr}]_+",
        r"L^{2/3}\omega^{1/3}R^{-2/3}",
        r"-\frac{4279}{238140000}<0",
        r"\tag{H.28}",
        "The benchmark pair is not asserted to solve",
        "does **not** prove the passive advection-diffusion target E.24",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75H boundary drift: {token}")


def render_step33_sections() -> str:
    source = (ROOT / "research/r075h_single_pass_transport_flux_closure.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 264
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
    if section_index != 271:
        raise RuntimeError(f"Step 33 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.11"', 'data-site-version="2.12"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.11", "/i18n-en.js?v=2.12", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Pure-transport terminal-tube closure realizes the one-third signed-flux gain in the exact ballistic benchmark; the diffusive estimate remains open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75h.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75H · STEP 33 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75H · Step 33 · PURE-TRANSPORT TERMINAL-TUBE CLOSURE</div><h1>{TITLE}</h1><p>冻结的非减时间 cutoff 给出精确 signed-flux endpoint identity；单程终端管的 characteristic persistence 与 spacetime Hölder 随后实现 <strong>R^(1/3)</strong> 增益，严格率为 <strong>-4279/238140000</strong>。<strong>这只证明 pure-transport benchmark；diffusive E.24 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">PURE TRANSPORT PROVED</span><span class="label">SIGNED POSITIVE PART</span><span class="label">TERMINAL TUBE</span><span class="label">FIXED LIFT / NO SEAM</span><span class="label">R^(1/3) BENCHMARK GAIN</span><span class="label">RATE -4279/238140000</span><span class="label">DIFFUSIVE EXTENSION OPEN</span><span class="label">E.24 OPEN</span><span class="label">NOT AN NSE SOLUTION FUNCTIONAL</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75H STEP 33</strong><p>transport identity：PROVED</p><p>terminal persistence：PROVED</p><p>cubic payment：PROVED</p><p>alpha=1/3 rate：NEGATIVE</p><p>absolute flux：NOT CLAIMED</p><p>diffusive H.28：CIRCULAR ROUTE</p><p>E.24：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step33_sections() + '\n<section id="reproduce">', "Step 33 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 33 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075h_single_pass_transport_flux_closure.md">Step 33 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075h_single_pass_transport_flux_closure_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075h_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075h_single_pass_transport_flux_closure_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075h_single_pass_transport_flux_closure_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075h_single_pass_transport_flux_closure_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075h_single_pass_transport_flux_closure_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075h_single_pass_transport_flux_closure_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075h_single_pass_transport_flux_closure_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075h_single_pass_transport_flux_closure_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075h_single_pass_transport_flux_closure_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075h_single_pass_transport_flux_closure_qa.sh">QA script</a></p><p><a href="/notes/r0-75h.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 19/19、Ruby 22/22、H.1--H.29 与 29/29 displays，3 个 Python hash seeds 字节稳定；两套实现分别拒绝 66/66 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12，显式包含 fixtures 与 expected JSON。本节纯解析，无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 33 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-256">← Step 32：signed-flux gain threshold</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 33 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Diffusive terminal-tube estimate 与 E.24 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75H Step 33 停止。本节只闭合 exact pure-transport ballistic benchmark；H.28 中的正号 dissipation 正是目标未知量，不能循环使用。多 block、shear-transition bands、periodic recrossing、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均未闭合。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 33 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075h"[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.11"' in page:
        for old, new, label in (
            ('data-site-version="2.11"', 'data-site-version="2.12"', "home version"),
            ("/i18n-en.js?v=2.11", "/i18n-en.js?v=2.12", "home i18n"),
            ("/site-refresh.js?v=2.11.1", "/site-refresh.js?v=2.12.1", "home refresh"),
            ("<strong>v2.11</strong>网页版本", "<strong>v2.12</strong>网页版本", "home stat version"),
            ("<strong>R0.75G</strong>最新研究节点", "<strong>R0.75H</strong>最新研究节点", "home latest"),
            ("<strong>235</strong>公开研究笔记", "<strong>236</strong>公开研究笔记", "home public count"),
            ("展开 145 篇公开笔记", "展开 146 篇公开笔记", "home route count"),
            ("综述 v2.11 · 2026-09-03", "综述 v2.12 · 2026-09-03", "home footer"),
            ("Research topology · R0.1–R0.75G", "Research topology · R0.1–R0.75H", "home topology"),
            ('href="#r075g">跳到首页 R0.75G 卡片 →', 'href="#r075h">跳到首页 R0.75H 卡片 →', "home jump"),
            ("R0.70A–R0.75G：137 节已公开，104 节完整封存", "R0.70A–R0.75H：138 节已公开，104 节完整封存", "home accounting"),
            ('<span class="route-range">R0.69P–R0.75G</span>', '<span class="route-range">R0.69P–R0.75H</span>', "home range"),
            ("<h3>R0.75G：signed-flux gain 的 exact threshold 与 residence exponent</h3>", "<h3>R0.75H：pure-transport terminal tube 与 R^(1/3) benchmark gain</h3>", "home route title"),
            ("R0.72R–R0.75G：</span>", "R0.72R–R0.75H：</span>", "home detail range"),
            ('aria-label="R0.69P–R0.75G"', 'aria-label="R0.69P–R0.75H"', "home links label"),
            ("全站现有 235 篇公开研究笔记", "全站现有 236 篇公开研究笔记", "home recap count"),
        ):
            page = replace_once(page, old, new, label)
        page = replace_pattern(
            page,
            r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
            '<div class="summary-item"><strong>我目前关注</strong><span>R0.75H Step 33 在 exact pure-transport benchmark 中，用 signed endpoint identity、单程终端管 persistence 与 spacetime Hölder 实现 R^(1/3) gain。diffusive H.28 会把目标 dissipation 放回右侧，因此 E.24 仍待独立估计。</span></div>',
            "home focus",
        )
        latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75H · 2026-09-03 · STEP 33 · PURE-TRANSPORT TERMINAL-TUBE CLOSURE</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">在 exact ballistic benchmark 中，非减 cutoff 把正号 signed flux 控制为 terminal half-energy；单程终端管 persistence 与 cubic payment 给出 R^(1/3) gain，rate 为 -4279/238140000。这个结论不覆盖 diffusion，E.24 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75h.pdf">阅读最新 R0.75H 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">236 篇研究笔记总索引</a><a href="#r075h">查看首页 R0.75H 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75H · 138 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75H Step 33 pure-transport terminal-tube closure</span></div></div></section>'''
        page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
        page = replace_pattern(
            page,
            r'<p class="tree-current-summary">.*?</p>',
            '<p class="tree-current-summary">Step 33 proves the exact signed pure-transport endpoint identity and a terminal-tube cubic estimate with the one-third gain. The benchmark is ballistic, not a Navier--Stokes solution functional; its diffusive extension and E.24 remain open.</p>',
            "home current summary",
        )
        page = replace_once(
            page,
            'phase-substitution no-go → exact signed-flux gain threshold / one-third target / positive gain open</p>',
            'exact signed-flux threshold → pure-transport terminal tube / one-third benchmark / diffusive closure open</p>',
            "home route path",
        )
        page = replace_once(
            page,
            '<a class="milestone" href="/notes/r0-75g.html">R0.75G</a>',
            '<a class="milestone" href="/notes/r0-75g.html">R0.75G</a>\n<a class="milestone" href="/notes/r0-75h.html">R0.75H</a>',
            "home milestone",
        )
    elif 'data-site-version="2.12"' not in page:
        raise RuntimeError("home baseline version drift")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>diffusive terminal-tube control remains unproved</h3><p>必须在不复用目标 dissipation 的前提下加入 Feynman--Kac occupation、resolvent 或 separately paid source information；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075h" data-release="r075h" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75H Step 33 · 2026-09-03 · PURE-TRANSPORT TERMINAL-TUBE CLOSURE</p><h3>{TITLE}</h3><p>exact pure-transport identity 把 positive signed flux 控制到 terminal half-energy；单程终端管 persistence 与 spacetime Hölder 给出 R^(1/3) benchmark gain。diffusive H.28 仍循环，E.24 未闭合。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75h.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75h.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075g"'
    if anchor not in page:
        raise RuntimeError("home R0.75G card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075h-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.11"' in page:
        for old, new, label in (
            ('data-site-version="2.11"', 'data-site-version="2.12"', "literature version"),
            ("/i18n-en.js?v=2.11", "/i18n-en.js?v=2.12", "literature i18n"),
            ("文献综述 v2.11 · 2026-09-03", "文献综述 v2.12 · 2026-09-03", "literature footer"),
            ("本站 R0.69P–R0.75G 只列为研究笔记", "本站 R0.69P–R0.75H 只列为研究笔记", "literature intro"),
        ):
            page = replace_once(page, old, new, label)
        old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>positive signed-flux gain remains open</strong></header><p>必须加入 independent dynamic、resolvent、pathwise residence-time 或 payment-sensitive information；后续材料未授权、未读取、未公开。</p></div>'
        route = '<div class="route-step kept"><header><b>R0.75H</b><strong>pure-transport terminal-tube closure</strong></header><p>Step 33 证明非减 cutoff 的 exact signed-flux endpoint identity，并在 fixed-lift、no-seam 的单程终端管中以 characteristic persistence 和 spacetime Hölder 实现 R^(1/3) benchmark gain。这个 pair 不是 Navier--Stokes solution functional，diffusive H.28 仍循环。<a href="/notes/r0-75h.html">研究笔记</a> <a href="#r075h-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>diffusive terminal-tube control remains open</strong></header><p>必须加入 independent Feynman--Kac occupation、resolvent 或 separately paid source row，且不能把目标 dissipation 放回右侧；后续材料未授权、未读取、未公开。</p></div>'
        page = replace_once(page, old_next, route, "literature route")
    elif 'data-site-version="2.12"' not in page:
        raise RuntimeError("literature baseline version drift")
    boundary = (
        '<h3 id="r075h-boundary">R0.75H Step 33 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Alphonse--Martin 的 moving-support control result 使用 integral-thickness geometry；'
        'Gardner--Liss--Mattingly 的 pathwise 方法加入 diffusive trajectories 与 local shear；'
        'Albritton--Dong 的 local passive-scalar theory 保留 quantitative drift-flux cost。'
        '没有一个 inspected source 给出 frozen terminal-tube cubic estimate、从 H.28 移除目标 dissipation，或证明 E.24。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75H Step 33 公开边界</strong><p>'
        'PROVED：pure transport 的 full-window signed identity H.13--H.14、terminal persistence H.16--H.19、'
        'cubic payment H.23、严格 rate -4279/238140000，以及 matching-background 下的 R^(1/3) scale H.26。'
        'FINITE BENCHMARK ONLY：P_R^(M,tr) 是 Version-M formula 在 pure-transport pair 上的值，不是 Navier--Stokes solution payment；'
        '结论只控制正号 signed flux，不控制 absolute flux、multiple windings 或 diffusion。'
        'OPEN：独立支付的 diffusive terminal-tube/resolvent estimate、shear-transition bands、periodic recrossing、E.24、complete clock、fixed deletion、suitable-weak transfer、'
        'regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75h.html">阅读完整笔记</a> · '
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
    if html_count != 236 or pdf_count not in (192, 193):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 176:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75h.html",
        "latestPublishedResearchPdf": "/notes/r0-75h.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075g":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 138
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30, "r075f": 31, "r075g": 32,
        "r075h": 33,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "PURE_TRANSPORT_TERMINAL_TUBE_SIGNED_FLUX_CLOSURE",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_PURE_TRANSPORT_BENCHMARK",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "pure_transport_signed_identity": "PROVED_H13_H14",
            "terminal_tube_persistence": "PROVED_H16_H19_FIXED_LIFT_NO_SEAM",
            "terminal_tube_cubic_payment": "PROVED_H23",
            "alpha_one_third_benchmark_gain": "PROVED_STRICT_NEGATIVE_RATE",
            "frozen_rate": "NEGATIVE_4279_OVER_238140000",
            "matching_background_comparison": "PROVED_H26_WITH_STATED_LOWER_SCALE",
            "benchmark_version_m_measurement": "FORMULA_EVALUATED_ON_PURE_TRANSPORT_NOT_NSE_SOLUTION",
            "absolute_flux": "NOT_CLAIMED",
            "multiple_windings": "NOT_COVERED",
            "diffusive_identity_H28": "EXACT_BUT_CIRCULAR_FOR_TARGET_DISSIPATION",
            "diffusive_terminal_tube": "OPEN_UNPROVED",
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
            "python_certificate": "PASS_19_OF_19",
            "independent_ruby": "PASS_22_OF_22",
            "negative_mutations": "PASS_PYTHON_66_OF_66_RUBY_66_OF_66",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_H1_TO_H29_29_OF_29",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75h.html",
            "target_pdf": "/notes/r0-75h.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075h_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 33,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 138,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075i",
        "latestPublishedResearchHtml": "/notes/r0-75h.html",
        "latestPublishedResearchPdf": "/notes/r0-75h.pdf",
        "latestReleaseGate": "tests/r075h-step33-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075h-step33-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075h-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075h-step33-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075h-step33-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075h-step33-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075h-step33-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075h-step33",
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
    write_text(PUBLIC / "notes/r0-75h.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 33,
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
