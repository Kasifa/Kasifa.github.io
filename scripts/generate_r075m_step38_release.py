#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75M Step 38 from the verified R0.75L Step 37 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075l_step37_release as previous
import import_r075m_step38_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "7ae8fd8c11bb44234845c9283397755f2ef82905"
VERSION = "2.17"
RELEASE = "r075m"
CODE = "R0.75M"
TITLE = "R0.75M｜单个 dyadic packet 的扩散型 signed-flux 增益"
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
            raise RuntimeError(f"R0.75M frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 19
        or certificate.get("assertions", {}).get("passed") != 19
        or len(certificate.get("checks", {})) != 19
    ):
        raise RuntimeError("R0.75M certificate verdict drift")
    main = (ROOT / "research/r075m_dyadic_packet_diffusive_flux_gain.md").read_text()
    for token in (
        r"\mathcal W_\xi",
        r"\tag{M.2}",
        "Schur's test",
        r"\frac{|B|\mathcal W_\xi}{4K^2}E_0",
        r"\tag{M.11}",
        r"K^{-2/3}M_K^{2/3}",
        r"\tag{M.19}",
        r"\frac{27163}{71442}",
        r"\tag{M.20}",
        "single-dyadic-packet",
        "inter-packet summation",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75M boundary drift: {token}")


def render_step38_sections() -> str:
    source = (ROOT / "research/r075m_dyadic_packet_diffusive_flux_gain.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 300
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
    if section_index != 307:
        raise RuntimeError(f"Step 38 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.16"', 'data-site-version="2.17"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.16", "/i18n-en.js?v=2.17", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Arbitrary finite interference inside one real dyadic constant-shear packet preserves the physical signed-flux K^(-2/3) gain without a packet-cardinality factor">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75m.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75M · STEP 38 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75M · Step 38 · DYADIC-PACKET DIFFUSIVE GAIN</div><h1>{TITLE}</h1><p>对 constant shear 下任意有限 real dyadic horizontal packet，periodic derivative 先严格消去 <strong>diagonal zero mode</strong>；exact modal kernel、Schur test 与 Parseval 给出 against-energy 的 <strong>K^(-2)</strong>，再由 short-time heat lower bound 和 full-torus cubic mass 得到 <strong>K^(-2/3)</strong> 增益，且没有单独的 packet-cardinality loss。代价保留为 <strong>W_xi</strong>；inter-packet summation、frozen-collar calibration 与 low difference-frequency sector 仍开放。<strong>E.24 OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">FINITE REAL DYADIC PACKET</span><span class="label">PHYSICAL SIGNED FLUX</span><span class="label">DIAGONAL CANCELED</span><span class="label">SCHUR TEST</span><span class="label">NO MODE-COUNT LOSS</span><span class="label">ENERGY K^-2</span><span class="label">GAIN K^-2/3</span><span class="label">WIENER ROW W_XI</span><span class="label">FULL-TORUS CUBIC MASS</span><span class="label">ONE PACKET ONLY</span><span class="label">COLLAR CALIBRATION OPEN</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75M STEP 38</strong><p>passive family：EXACT FINITE PACKET</p><p>support：K&lt;=|n|&lt;=2K</p><p>diagonal：CANCELED BEFORE ABS</p><p>aggregation：SCHUR / WIENER</p><p>mode-count loss：NONE EXPLICIT</p><p>energy row：K^-2</p><p>cubic conversion：K^-2/3</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step38_sections() + '\n<section id="reproduce">', "Step 38 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 38 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075m_dyadic_packet_diffusive_flux_gain.md">Step 38 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075m_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075m_dyadic_packet_diffusive_flux_gain_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075m_dyadic_packet_diffusive_flux_gain_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075m_dyadic_packet_diffusive_flux_gain_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075m_dyadic_packet_diffusive_flux_gain_qa.sh">QA script</a></p><p><a href="/notes/r0-75m.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 19/19、Ruby 20/20、M.1--M.20 与 20/20 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 130/130 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 38 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-294">← Step 37：single-harmonic diffusive gain</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 38 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">inter-packet, frozen-collar and low-difference rows remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75M Step 38 停止。one real dyadic constant-shear packet 内的 arbitrary finite interference 已保持 physical signed flux 的 K^(-2/3) gain，且无单独 packet-cardinality loss；inter-packet summation、frozen-collar W_xi calibration、local Version-M atom、nonconstant shear、low difference-frequency sector、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均继续开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 38 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.16"', 'data-site-version="2.17"', "home version"),
        ("/i18n-en.js?v=2.16", "/i18n-en.js?v=2.17", "home i18n"),
        ("/site-refresh.js?v=2.16.1", "/site-refresh.js?v=2.17.1", "home refresh"),
        ("<strong>v2.16</strong>网页版本", "<strong>v2.17</strong>网页版本", "home stat version"),
        ("<strong>R0.75L</strong>最新研究节点", "<strong>R0.75M</strong>最新研究节点", "home latest"),
        ("<strong>240</strong>公开研究笔记", "<strong>241</strong>公开研究笔记", "home public count"),
        ("展开 150 篇公开笔记", "展开 151 篇公开笔记", "home route count"),
        ("综述 v2.16 · 2026-09-04", "综述 v2.17 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75L", "Research topology · R0.1–R0.75M", "home topology"),
        ('href="#r075l">跳到首页 R0.75L 卡片 →', 'href="#r075m">跳到首页 R0.75M 卡片 →', "home jump"),
        ("R0.70A–R0.75L：142 节已公开，104 节完整封存", "R0.70A–R0.75M：143 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75L</span>', '<span class="route-range">R0.69P–R0.75M</span>', "home range"),
        ("<h3>R0.75L：single-harmonic physical signed flux 的 diffusive gain</h3>", "<h3>R0.75M：dyadic-packet signed flux 的 mode-count-free diffusive gain</h3>", "home route title"),
        ("R0.72R–R0.75L：</span>", "R0.72R–R0.75M：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75L"', 'aria-label="R0.69P–R0.75M"', "home links label"),
        ("全站现有 240 篇公开研究笔记", "全站现有 241 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75M Step 38 证明 arbitrary finite interference inside one real dyadic constant-shear packet 不破坏 physical signed flux 的 K^(-2/3) gain，且不产生单独 mode-count loss；inter-packet、frozen-collar calibration 与 low differences 仍未闭合。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75M · 2026-09-04 · STEP 38 · DYADIC-PACKET DIFFUSIVE GAIN</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">one real dyadic constant-shear packet 内的 diagonal 先在取绝对值前消失；exact modal kernel、Schur/Wiener row 与 short-time cubic conversion 保持 K^(-2/3) gain，且不出现单独 packet-cardinality factor。结论不延伸到 inter-packet、frozen collar 或 E.24。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75m.pdf">阅读最新 R0.75M 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">241 篇研究笔记总索引</a><a href="#r075m">查看首页 R0.75M 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75M · 143 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75M Step 38 dyadic-packet diffusive gain</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 38 proves that arbitrary finite interference inside one real dyadic constant-shear packet preserves the K^(-2/3) physical signed-flux gain without a separate packet-cardinality factor.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain / multimode and collar payment open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain / inter-packet and collar payment open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75l.html">R0.75L</a>', '<a class="milestone" href="/notes/r0-75l.html">R0.75L</a>\n<a class="milestone" href="/notes/r0-75m.html">R0.75M</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>inter-packet, frozen-collar and low-difference rows remain open</h3><p>仍需完成 inter-packet summation，量化 frozen-collar W_xi，localize cubic mass，并控制 nonconstant shear 与 low difference-frequency sector；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075m" data-release="r075m" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75M Step 38 · 2026-09-04 · DYADIC-PACKET DIFFUSIVE GAIN</p><h3>{TITLE}</h3><p>exact finite dyadic packet 通过 diagonal cancellation、Schur/Wiener row 与 short-time cubic conversion 保持 physical signed flux 的 K^(-2/3) gain，且无单独 packet-cardinality loss。inter-packet、frozen-collar calibration、local Version-M atom 与 E.24 仍 OPEN。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75m.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75m.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075l"'
    if anchor not in page:
        raise RuntimeError("home R0.75L card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.16"', 'data-site-version="2.17"', "literature version"),
        ("/i18n-en.js?v=2.16", "/i18n-en.js?v=2.17", "literature i18n"),
        ("文献综述 v2.16 · 2026-09-04", "文献综述 v2.17 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75L 只列为研究笔记", "本站 R0.69P–R0.75M 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>paid high/low difference-frequency split remains open</strong></header><p>multimode convolution、frozen-collar localization、|B|V_xi payment、nonconstant shear 与 low difference-frequency sector 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75M</b><strong>dyadic-packet mode-count-free diffusive gain</strong></header><p>Step 38 对 arbitrary finite real dyadic packet 用 exact modal kernel、diagonal cancellation、Schur/Wiener row 与 short-time cubic conversion 保持 K^(-2/3) gain，且无单独 packet-cardinality loss。<a href="/notes/r0-75m.html">研究笔记</a> <a href="#r075m-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>inter-packet, frozen-collar and low-difference rows remain open</strong></header><p>inter-packet summation、frozen-collar W_xi calibration、local Version-M atom、nonconstant shear 与 low difference-frequency sector 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075m-boundary">R0.75M Step 38 的 bounded primary-source screen 与主张边界</h3>'
        '<p>He 支持 horizontal mode-by-mode enhanced-dissipation analysis and summation architecture；Gardner--Liss--Mattingly 提供 nonconstant-shear pathwise control context；Jimenez-Urias--Haine 给出 periodic shear dispersion 的 exact modal representation。R0.75M 的 specific Schur/Wiener kernel 与 Version-M boundary 均为本地推导。没有 inspected source 给出 frozen-collar Wiener payment、inter-packet summation 或 E.24。有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75M Step 38 公开边界</strong><p>'
        'PROVED：finite real dyadic-packet solution M.3--M.6、exact modal kernel 与 diagonal cancellation M.7、Schur/Wiener energy bound M.8--M.11、short-time cubic conversion M.12--M.16、second-derivative Wiener row M.17、target-normalized diagnostic M.18--M.20。'
        'SCOPE：one finite real dyadic constant-shear packet 与 full-torus cubic mass；无单独 packet-cardinality factor。'
        'OPEN：inter-packet summation、frozen-collar W_xi calibration、local Version-M atom、nonconstant shear、low difference-frequency sector、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75m.html">阅读完整笔记</a> · '
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
    if html_count != 241 or pdf_count not in (197, 198):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 181:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75m.html",
        "latestPublishedResearchPdf": "/notes/r0-75m.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075l":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 143
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 38
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "DYADIC_PACKET_DIFFUSIVE_SIGNED_FLUX_GAIN_WITH_CUTOFF_WIENER_NORM",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_DYADIC_PACKET_DIFFUSIVE_SIGNED_FLUX_GAIN",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "exact_passive_family": "PROVED_M3_M6",
            "physical_signed_flux": "DIAGONAL_ZERO_MODE_CANCELED_M7",
            "schur_wiener_energy_bound": "K_MINUS_2_M8_M11_NO_MODE_COUNT",
            "short_time_cubic_conversion": "PROVED_M12_M16",
            "diffusive_payment_gain": "K_MINUS_2_OVER_3_M2_M16",
            "wiener_sobolev_row": "FIRST_AND_SECOND_DERIVATIVES_M17",
            "target_normalization": "PROVED_M18_M19",
            "frequency_threshold": "CONDITIONAL_KAPPA_GT_27163_OVER_71442_M20",
            "scope": "ONE_FINITE_REAL_DYADIC_CONSTANT_SHEAR_PACKET_FULL_TORUS_CUBIC_MASS",
            "packet_cardinality_loss": "NONE_EXPLICIT",
            "inter_packet_summation": "OPEN_NOT_PROVED",
            "frozen_collar_wiener_calibration": "OPEN_NOT_PROVED",
            "local_version_m_atom": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_19_OF_19",
            "independent_ruby": "PASS_20_OF_20",
            "negative_mutations": "PASS_PYTHON_130_OF_130_RUBY_130_OF_130",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_M1_TO_M20_20_OF_20",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75m.html",
            "target_pdf": "/notes/r0-75m.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075m_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 38,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 143,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075n",
        "latestPublishedResearchHtml": "/notes/r0-75m.html",
        "latestPublishedResearchPdf": "/notes/r0-75m.pdf",
        "latestReleaseGate": "tests/r075m-step38-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075m-step38-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075m-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075m-step38-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075m-step38-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075m-step38-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075m-step38-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075m-step38",
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
    write_text(PUBLIC / "notes/r0-75m.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 38,
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
