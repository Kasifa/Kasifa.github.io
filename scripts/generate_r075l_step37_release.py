#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75L Step 37 from the verified R0.75K Step 36 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075k_step36_release as previous
import import_r075l_step37_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.16"
RELEASE = "r075l"
CODE = "R0.75L"
TITLE = "R0.75L｜单实谐波物理 signed flux 的扩散型高频增益"
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
            raise RuntimeError(f"R0.75L frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 19
        or certificate.get("assertions", {}).get("passed") != 19
        or len(certificate.get("checks", {})) != 19
    ):
        raise RuntimeError("R0.75L certificate verdict drift")
    main = (ROOT / "research/r075l_single_harmonic_diffusive_signed_flux_gain.md").read_text()
    for token in (
        r"\boxed{\mathcal L_BF_k=0.}",
        r"\mathcal T_{k,\eta}",
        r"\tag{L.9}",
        r"M_k",
        r"k^{-2/3}",
        r"\tag{L.15}",
        r"\frac{27163}{71442}",
        r"\tag{L.17}",
        "one real",
        "full-torus cubic mass",
        "does not sum arbitrary cross modes",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75L boundary drift: {token}")


def render_step37_sections() -> str:
    source = (ROOT / "research/r075l_single_harmonic_diffusive_signed_flux_gain.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 293
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
    if section_index != 300:
        raise RuntimeError(f"Step 37 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.15"', 'data-site-version="2.16"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.15", "/i18n-en.js?v=2.16", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="One real constant-shear passive harmonic gains an exact diffusion-compatible k^(-2/3) factor for the physical signed flux against its full-torus cubic mass">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75l.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75L · STEP 37 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75L · Step 37 · DIFFUSIVE SIGNED-FLUX GAIN</div><h1>{TITLE}</h1><p>对 constant shear 下的一个 real horizontal harmonic，先利用 periodic derivative 严格消去 <strong>zero mode</strong>，再取绝对值；普通 heat decay 使 physical signed flux 带有 <strong>k^(-2)</strong>，与 exact full-torus cubic mass 比较后得到真正的 <strong>k^(-2/3)</strong> 增益。这是 single-harmonic benchmark，不支付 <strong>|B|V_xi</strong>，不处理 multimode、frozen collar 或 low-frequency sector。<strong>E.24 OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">EXACT PASSIVE HARMONIC</span><span class="label">PHYSICAL SIGNED FLUX</span><span class="label">ZERO MODE CANCELED</span><span class="label">ONLY +/-2k</span><span class="label">FLUX k^-2</span><span class="label">CUBIC MASS k^-2</span><span class="label">GAIN k^-2/3</span><span class="label">FULL-TORUS ATOM</span><span class="label">SINGLE HARMONIC ONLY</span><span class="label">|B|V_XI UNPAID</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75L STEP 37</strong><p>passive family：EXACT</p><p>source：PHYSICAL SIGNED FLUX</p><p>diagonal zero mode：CANCELED</p><p>surviving modes：+/-2k</p><p>flux decay：k^-2</p><p>cubic conversion：k^-2/3</p><p>scope：ONE REAL HARMONIC</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step37_sections() + '\n<section id="reproduce">', "Step 37 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 37 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075l_single_harmonic_diffusive_signed_flux_gain.md">Step 37 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075l_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075l_single_harmonic_diffusive_signed_flux_gain_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075l_single_harmonic_diffusive_signed_flux_gain_qa.sh">QA script</a></p><p><a href="/notes/r0-75l.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 19/19、Ruby 20/20、L.1--L.17 与 17/17 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 120/120 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 37 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-286">← Step 36：fixed positive-majorant trace loss</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 37 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">paid high/low difference-frequency split remains OPEN</h2><p style="margin:.15rem 0">本站在 R0.75L Step 37 停止。single real constant-shear harmonic 的 physical signed flux 已获得 diffusion-compatible k^(-2/3) gain；multimode convolution、frozen-collar localization、|B|V_xi payment、nonconstant shear、low difference-frequency sector、G.1、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均继续开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 37 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075l"[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.15"' in page:
        for old, new, label in (
            ('data-site-version="2.15"', 'data-site-version="2.16"', "home version"),
            ("/i18n-en.js?v=2.15", "/i18n-en.js?v=2.16", "home i18n"),
            ("/site-refresh.js?v=2.15.1", "/site-refresh.js?v=2.16.1", "home refresh"),
            ("<strong>v2.15</strong>网页版本", "<strong>v2.16</strong>网页版本", "home stat version"),
            ("<strong>R0.75K</strong>最新研究节点", "<strong>R0.75L</strong>最新研究节点", "home latest"),
            ("<strong>239</strong>公开研究笔记", "<strong>240</strong>公开研究笔记", "home public count"),
            ("展开 149 篇公开笔记", "展开 150 篇公开笔记", "home route count"),
            ("综述 v2.15 · 2026-09-04", "综述 v2.16 · 2026-09-04", "home footer"),
            ("Research topology · R0.1–R0.75K", "Research topology · R0.1–R0.75L", "home topology"),
            ('href="#r075k">跳到首页 R0.75K 卡片 →', 'href="#r075l">跳到首页 R0.75L 卡片 →', "home jump"),
            ("R0.70A–R0.75K：141 节已公开，104 节完整封存", "R0.70A–R0.75L：142 节已公开，104 节完整封存", "home accounting"),
            ('<span class="route-range">R0.69P–R0.75K</span>', '<span class="route-range">R0.69P–R0.75L</span>', "home range"),
            ("<h3>R0.75K：fixed positive majorant 的 high-frequency trace loss</h3>", "<h3>R0.75L：single-harmonic physical signed flux 的 diffusive gain</h3>", "home route title"),
            ("R0.72R–R0.75K：</span>", "R0.72R–R0.75L：</span>", "home detail range"),
            ('aria-label="R0.69P–R0.75K"', 'aria-label="R0.69P–R0.75L"', "home links label"),
            ("全站现有 239 篇公开研究笔记", "全站现有 240 篇公开研究笔记", "home recap count"),
        ):
            page = replace_once(page, old, new, label)
        page = replace_pattern(
            page,
            r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
            '<div class="summary-item"><strong>我目前关注</strong><span>R0.75L Step 37 证明 one real constant-shear harmonic 的 physical signed flux 在 exact diagonal cancellation 后获得 diffusion-compatible k^(-2/3) gain；multimode、frozen-collar localization 与 |B|V_xi payment 仍未闭合。</span></div>',
            "home focus",
        )
        latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75L · 2026-09-04 · STEP 37 · DIFFUSIVE SIGNED-FLUX GAIN</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">one real constant-shear passive harmonic 的 zero mode 在取绝对值前严格消失；ordinary heat decay 令 physical signed flux 带有 k^(-2)，与 full-torus cubic mass 比较后得到 k^(-2/3) gain。结论不延伸到 multimode、frozen collar 或 E.24。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75l.pdf">阅读最新 R0.75L 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">240 篇研究笔记总索引</a><a href="#r075l">查看首页 R0.75L 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75L · 142 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75L Step 37 diffusive signed-flux gain</span></div></div></section>'''
        page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
        page = replace_pattern(
            page,
            r'<p class="tree-current-summary">.*?</p>',
            '<p class="tree-current-summary">Step 37 proves an exact diffusion-compatible k^(-2/3) gain for the physical signed flux of one real constant-shear harmonic, measured against its full-torus cubic mass.</p>',
            "home current summary",
        )
        page = replace_once(
            page,
            'mean-zero adjoint obstruction → fixed positive-majorant trace loss / signed-frequency payment open</p>',
            'fixed positive-majorant trace loss → single-harmonic diffusive signed-flux gain / multimode and collar payment open</p>',
            "home route path",
        )
        page = replace_once(
            page,
            '<a class="milestone" href="/notes/r0-75k.html">R0.75K</a>',
            '<a class="milestone" href="/notes/r0-75k.html">R0.75K</a>\n<a class="milestone" href="/notes/r0-75l.html">R0.75L</a>',
            "home milestone",
        )
    elif 'data-site-version="2.16"' not in page:
        raise RuntimeError("home baseline version drift")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>a paid high/low difference-frequency split remains open</h3><p>仍需证明 multimode convolution 与 frozen-collar localization，支付 |B|V_xi，并控制 nonconstant shear 和 low difference-frequency sector；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075l" data-release="r075l" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75L Step 37 · 2026-09-04 · DIFFUSIVE SIGNED-FLUX GAIN</p><h3>{TITLE}</h3><p>exact one-real-harmonic family 在 zero-mode cancellation 后给出 physical signed flux 的 k^(-2) decay；与 full-torus cubic mass 比较得到 k^(-2/3) gain。multimode、frozen collar、|B|V_xi payment 与 E.24 仍 OPEN。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75l.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75l.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075k"'
    if anchor not in page:
        raise RuntimeError("home R0.75K card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075l-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.15"' in page:
        for old, new, label in (
            ('data-site-version="2.15"', 'data-site-version="2.16"', "literature version"),
            ("/i18n-en.js?v=2.15", "/i18n-en.js?v=2.16", "literature i18n"),
            ("文献综述 v2.15 · 2026-09-04", "文献综述 v2.16 · 2026-09-04", "literature footer"),
            ("本站 R0.69P–R0.75K 只列为研究笔记", "本站 R0.69P–R0.75L 只列为研究笔记", "literature intro"),
        ):
            page = replace_once(page, old, new, label)
        old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>signed or frequency-aware entrance payment remains open</strong></header><p>signed kernels、F-dependent/frequency-adapted tests 与其他 genuinely available Version-M trace/frequency row 仍未排除；后续材料未授权、未读取、未公开。</p></div>'
        route = '<div class="route-step kept"><header><b>R0.75L</b><strong>single-harmonic diffusive physical signed-flux gain</strong></header><p>Step 37 对 one real constant-shear harmonic 先消去 zero mode，再由 ordinary heat decay 得到 physical signed flux 的 k^(-2) bound；与 exact full-torus cubic mass 比较后得到 k^(-2/3) gain。<a href="/notes/r0-75l.html">研究笔记</a> <a href="#r075l-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>paid high/low difference-frequency split remains open</strong></header><p>multimode convolution、frozen-collar localization、|B|V_xi payment、nonconstant shear 与 low difference-frequency sector 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
        page = replace_once(page, old_next, route, "literature route")
    elif 'data-site-version="2.16"' not in page:
        raise RuntimeError("literature baseline version drift")
    boundary = (
        '<h3 id="r075l-boundary">R0.75L Step 37 的 bounded primary-source screen 与主张边界</h3>'
        '<p>He 支持 horizontal mode-by-mode enhanced-dissipation architecture；Gardner--Liss--Mattingly 提供 passive shear diffusion 的 pathwise local-streamline context；Jimenez-Urias--Haine 给出 periodic shear dispersion 的 exact modal/Mathieu representation。R0.75L 不导入这些更强机制，而只用 exact constant-shear harmonic 的 ordinary heat decay。没有 inspected source 给出 frozen-collar Version-M payment 或 E.24。有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75L Step 37 公开边界</strong><p>'
        'PROVED：exact passive family L.2--L.5、diagonal zero-mode cancellation L.6--L.8、k^(-2) physical signed-flux bound L.9、exact cubic mass 与 k^(-2/3) payment gain L.10--L.13、target-normalized diagnostic L.14--L.15，以及 conditional frequency threshold L.16--L.17。'
        'SCOPE：one real constant-shear harmonic 与 full-torus cubic mass；|B|V_xi 尚未支付。'
        'OPEN：multimode convolution、frozen-collar localization、nonconstant shear、low difference-frequency sector、G.1、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75l.html">阅读完整笔记</a> · '
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
    if html_count != 240 or pdf_count not in (196, 197):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 180:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75l.html",
        "latestPublishedResearchPdf": "/notes/r0-75l.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075k":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 142
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30, "r075f": 31, "r075g": 32,
        "r075h": 33, "r075i": 34, "r075j": 35, "r075k": 36, "r075l": 37,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "SINGLE_HARMONIC_DIFFUSIVE_SIGNED_FLUX_GAIN",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_SINGLE_HARMONIC_DIFFUSIVE_SIGNED_FLUX_GAIN",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "exact_passive_family": "PROVED_L2_L5",
            "physical_signed_flux": "DIAGONAL_ZERO_MODE_CANCELED_L6_L8",
            "flux_bound": "EXACT_K_MINUS_2_L9",
            "full_torus_cubic_mass": "EXACT_L10",
            "diffusive_payment_gain": "K_MINUS_2_OVER_3_L1_L10_L13",
            "target_normalization": "PROVED_L14_L15",
            "frequency_threshold": "CONDITIONAL_KAPPA_GT_27163_OVER_71442_L16_L17",
            "scope": "ONE_REAL_CONSTANT_SHEAR_HARMONIC_FULL_TORUS_CUBIC_MASS",
            "background_payment": "B_TIMES_VARIATION_UNPAID",
            "multimode_convolution": "OPEN_NOT_PROVED",
            "frozen_collar_localization": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "low_frequency_sector": "OPEN_NOT_PROVED",
            "G1": "OPEN_NOT_PROVED",
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
            "negative_mutations": "PASS_PYTHON_120_OF_120_RUBY_120_OF_120",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_L1_TO_L17_17_OF_17",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75l.html",
            "target_pdf": "/notes/r0-75l.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075l_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 37,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 142,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075m",
        "latestPublishedResearchHtml": "/notes/r0-75l.html",
        "latestPublishedResearchPdf": "/notes/r0-75l.pdf",
        "latestReleaseGate": "tests/r075l-step37-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075l-step37-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075l-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075l-step37-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075l-step37-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075l-step37-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075l-step37-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075l-step37",
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
    write_text(PUBLIC / "notes/r0-75l.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 37,
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
