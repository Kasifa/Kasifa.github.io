#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75K Step 36 from the verified R0.75J Step 35 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075j_step35_release as previous
import import_r075k_step36_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.15"
RELEASE = "r075k"
CODE = "R0.75K"
TITLE = "R0.75K｜固定正伴随 majorant 的高频 trace loss"
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
            raise RuntimeError(f"R0.75K frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 19
        or certificate.get("assertions", {}).get("passed") != 19
        or len(certificate.get("checks", {})) != 19
    ):
        raise RuntimeError("R0.75K certificate verdict drift")
    main = (ROOT / "research/r075k_positive_majorant_high_frequency_trace_loss.md").read_text()
    for token in (
        r"q(x_2):=1+\cos x_2\ge a(x_2)",
        r"\mathcal L^*\Phi=q",
        r"\boxed{\mathcal L F_k=0.}",
        r"B_k:=\frac12\int_0^{2\pi}\Phi(0)|F_k(0)|^2",
        r"M_k",
        r"\longrightarrow\infty",
        r"\boxed{\mathcal T_k=0.}",
        r"\tag{K.18}",
        "fixed nontrivial nonnegative entrance",
        "frequency-localized cancellation",
        "not a counterexample to E.24",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75K boundary drift: {token}")


def render_step36_sections() -> str:
    source = (ROOT / "research/r075k_positive_majorant_high_frequency_trace_loss.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 285
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
    if section_index != 293:
        raise RuntimeError(f"Step 36 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.14"', 'data-site-version="2.15"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.14", "/i18n-en.js?v=2.15", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A fixed nonnegative entrance weight loses high-frequency signed cancellation and cannot be paid uniformly by the local spacetime cubic atom alone">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75k.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75K · STEP 36 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75K · Step 36 · HIGH-FREQUENCY TRACE LOSS</div><h1>{TITLE}</h1><p>对固定非平凡的非负 entrance weight，显式高频被动场使 initial quadratic trace 保持正量，而局部时空 cubic mass 以 <strong>k^(-2)</strong> 衰减，故付款比按 <strong>k^(4/3)</strong> 发散。与此同时，真实 signed flux 对每个整数频率都严格为零：positivity 引入的零模测量的是证明损失，不是物理 flux。<strong>FIXED POSITIVE WEIGHT + LOCAL CUBIC ATOM ALONE RULED OUT. E.24 OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">SMOOTH PASSIVE FAMILY</span><span class="label">POSITIVE MAJORANT</span><span class="label">ENTRANCE MASS POSITIVE</span><span class="label">TRACE ROW FIXED</span><span class="label">CUBIC MASS k^-2</span><span class="label">RATIO k^4/3</span><span class="label">SIGNED FLUX ZERO</span><span class="label">PROOF LOSS</span><span class="label">FIXED WEIGHT ONLY</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75K STEP 36</strong><p>positive majorant：ADMISSIBLE</p><p>passive family：EXACT</p><p>entrance trace：FREQUENCY-INDEPENDENT</p><p>cubic mass：k^-2</p><p>payment ratio：k^4/3</p><p>actual signed flux：ZERO</p><p>scope：FIXED WEIGHT + LOCAL ATOM</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step36_sections() + '\n<section id="reproduce">', "Step 36 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 36 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075k_positive_majorant_high_frequency_trace_loss.md">Step 36 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075k_positive_majorant_high_frequency_trace_loss_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075k_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075k_positive_majorant_high_frequency_trace_loss_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075k_positive_majorant_high_frequency_trace_loss_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075k_positive_majorant_high_frequency_trace_loss_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075k_positive_majorant_high_frequency_trace_loss_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075k_positive_majorant_high_frequency_trace_loss_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075k_positive_majorant_high_frequency_trace_loss_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075k_positive_majorant_high_frequency_trace_loss_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075k_positive_majorant_high_frequency_trace_loss_qa.sh">QA script</a></p><p><a href="/notes/r0-75k.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 19/19、Ruby 21/21、K.1--K.18 与 18/18 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 100/100 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 36 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-279">← Step 35：mean-zero adjoint obstruction</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 36 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">保留 signed/frequency 信息的付款机制仍为 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75K Step 36 停止。fixed nonnegative entrance weight 加 local spacetime cubic atom alone 已被高频族排除，但 signed kernel、F-dependent 或 frequency-adapted test，以及由其他 genuinely available Version-M trace/frequency row 付款仍未排除。transition、periodic geometry、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均继续开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 36 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075k"[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.14"' in page:
        for old, new, label in (
            ('data-site-version="2.14"', 'data-site-version="2.15"', "home version"),
            ("/i18n-en.js?v=2.14", "/i18n-en.js?v=2.15", "home i18n"),
            ("/site-refresh.js?v=2.14.1", "/site-refresh.js?v=2.15.1", "home refresh"),
            ("<strong>v2.14</strong>网页版本", "<strong>v2.15</strong>网页版本", "home stat version"),
            ("<strong>R0.75J</strong>最新研究节点", "<strong>R0.75K</strong>最新研究节点", "home latest"),
            ("<strong>238</strong>公开研究笔记", "<strong>239</strong>公开研究笔记", "home public count"),
            ("展开 148 篇公开笔记", "展开 149 篇公开笔记", "home route count"),
            ("综述 v2.14 · 2026-09-03", "综述 v2.15 · 2026-09-04", "home footer"),
            ("Research topology · R0.1–R0.75J", "Research topology · R0.1–R0.75K", "home topology"),
            ('href="#r075j">跳到首页 R0.75J 卡片 →', 'href="#r075k">跳到首页 R0.75K 卡片 →', "home jump"),
            ("R0.70A–R0.75J：140 节已公开，104 节完整封存", "R0.70A–R0.75K：141 节已公开，104 节完整封存", "home accounting"),
            ('<span class="route-range">R0.69P–R0.75J</span>', '<span class="route-range">R0.69P–R0.75K</span>', "home range"),
            ("<h3>R0.75J：mean-zero signed adjoint obstruction 与 paid majorant gate</h3>", "<h3>R0.75K：fixed positive majorant 的 high-frequency trace loss</h3>", "home route title"),
            ("R0.72R–R0.75J：</span>", "R0.72R–R0.75K：</span>", "home detail range"),
            ('aria-label="R0.69P–R0.75J"', 'aria-label="R0.69P–R0.75K"', "home links label"),
            ("全站现有 238 篇公开研究笔记", "全站现有 239 篇公开研究笔记", "home recap count"),
        ):
            page = replace_once(page, old, new, label)
        page = replace_pattern(
            page,
            r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
            '<div class="summary-item"><strong>我目前关注</strong><span>R0.75K Step 36 证明 fixed nonnegative entrance weight 的 positive-majorant boundary row 不能由 local spacetime cubic atom alone 在频率上一致支付；真实 signed flux 同时严格为零，故这是 positivity proof loss，而非 E.24 counterexample。</span></div>',
            "home focus",
        )
        latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75K · 2026-09-04 · STEP 36 · HIGH-FREQUENCY TRACE LOSS</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">固定非负 entrance weight 的 quadratic trace 保持正量，而显式 passive Fourier family 的 local spacetime cubic mass 以 k^(-2) 衰减，付款比按 k^(4/3) 发散；真实 signed flux 却严格为零。结论只排除 fixed positive weight + local cubic atom alone。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75k.pdf">阅读最新 R0.75K 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">239 篇研究笔记总索引</a><a href="#r075k">查看首页 R0.75K 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75K · 141 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75K Step 36 high-frequency trace loss</span></div></div></section>'''
        page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
        page = replace_pattern(
            page,
            r'<p class="tree-current-summary">.*?</p>',
            '<p class="tree-current-summary">Step 36 proves that a fixed nontrivial nonnegative entrance weight loses high-frequency signed cancellation: its boundary row stays positive while the local cubic mass decays like k^(-2). The actual signed flux remains zero.</p>',
            "home current summary",
        )
        page = replace_once(
            page,
            'diffusion-safe one-block estimate → mean-zero adjoint obstruction / paid positive majorant open</p>',
            'mean-zero adjoint obstruction → fixed positive-majorant trace loss / signed-frequency payment open</p>',
            "home route path",
        )
        page = replace_once(
            page,
            '<a class="milestone" href="/notes/r0-75j.html">R0.75J</a>',
            '<a class="milestone" href="/notes/r0-75j.html">R0.75J</a>\n<a class="milestone" href="/notes/r0-75k.html">R0.75K</a>',
            "home milestone",
        )
    elif 'data-site-version="2.15"' not in page:
        raise RuntimeError("home baseline version drift")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>a signed or frequency-aware entrance payment remains open</h3><p>仍需保留 signed/frequency cancellation，或构造可审计的 F-dependent/frequency-adapted test，或证明其他 genuinely available Version-M trace/frequency row 可支付；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075k" data-release="r075k" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75K Step 36 · 2026-09-04 · HIGH-FREQUENCY TRACE LOSS</p><h3>{TITLE}</h3><p>显式 smooth passive family 使 fixed positive entrance row 与频率无关，而 local spacetime cubic mass 按 k^(-2) 衰减，ratio 按 k^(4/3) 发散；actual signed flux 对每个 k 都为零。结论只排除 fixed positive weight + local cubic atom alone。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75k.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75k.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075j"'
    if anchor not in page:
        raise RuntimeError("home R0.75J card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075k-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.14"' in page:
        for old, new, label in (
            ('data-site-version="2.14"', 'data-site-version="2.15"', "literature version"),
            ("/i18n-en.js?v=2.14", "/i18n-en.js?v=2.15", "literature i18n"),
            ("文献综述 v2.14 · 2026-09-03", "文献综述 v2.15 · 2026-09-04", "literature footer"),
            ("本站 R0.69P–R0.75J 只列为研究笔记", "本站 R0.69P–R0.75K 只列为研究笔记", "literature intro"),
        ):
            page = replace_once(page, old, new, label)
        old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>a paid nonnegative majorant remains open</strong></header><p>必须构造并支付满足 a&lt;=L*Phi 的 nonnegative majorant，尤其是 frozen Version-M atoms 下的 initial occupation/source row 及 transition/periodic geometry；后续材料未授权、未读取、未公开。</p></div>'
        route = '<div class="route-step kept"><header><b>R0.75K</b><strong>fixed positive-majorant high-frequency trace loss</strong></header><p>Step 36 以 exact passive Fourier family 证明 fixed nontrivial nonnegative entrance weight 的 boundary row 保持正量，而 local spacetime cubic atom 按 k^(-2) 衰减，ratio 按 k^(4/3) 发散；actual signed flux 同时严格为零。<a href="/notes/r0-75k.html">研究笔记</a> <a href="#r075k-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>signed or frequency-aware entrance payment remains open</strong></header><p>signed kernels、F-dependent/frequency-adapted tests 与其他 genuinely available Version-M trace/frequency row 仍未排除；后续材料未授权、未读取、未公开。</p></div>'
        page = replace_once(page, old_next, route, "literature route")
    elif 'data-site-version="2.15"' not in page:
        raise RuntimeError("literature baseline version drift")
    boundary = (
        '<h3 id="r075k-boundary">R0.75K Step 36 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Albritton--Dong 支持把 constant-shear operator 视为标准 passive subfamily；'
        'Hu--Li 的 Davies 方法提供 positive off-diagonal semigroup context；'
        'Gardner--Liss--Mattingly 说明 pathwise shear-diffusion representation 可保留动力学信息。'
        '没有一个 inspected source 把 positive entrance row 转换为 frozen Version-M cubic payment，也没有给出 E.24。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75K Step 36 公开边界</strong><p>'
        'PROVED：smooth positive majorant K.4--K.7、exact real passive family K.8--K.10、frequency-independent boundary row K.11、exact cubic mass 与 divergent ratio K.12--K.14、zero actual signed flux K.15--K.16、general fixed-weight lemma K.17。'
        'LIMITED NO-GO：只排除 fixed nontrivial nonnegative entrance weight 与 local spacetime cubic atom alone 的组合；这是 positivity proof loss，不是 E.24 counterexample。'
        'OPEN：signed kernels、F-dependent 或 frequency-adapted tests、其他 available Version-M trace/frequency payment、transition/periodic geometry、E.24、complete clock、fixed deletion、suitable-weak transfer、'
        'regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75k.html">阅读完整笔记</a> · '
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
    if html_count != 239 or pdf_count not in (195, 196):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 179:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75k.html",
        "latestPublishedResearchPdf": "/notes/r0-75k.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075j":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 141
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30, "r075f": 31, "r075g": 32,
        "r075h": 33, "r075i": 34, "r075j": 35, "r075k": 36,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "FIXED_POSITIVE_MAJORANT_HIGH_FREQUENCY_TRACE_LOSS",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_FIXED_POSITIVE_MAJORANT_HIGH_FREQUENCY_TRACE_LOSS",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "positive_majorant": "SMOOTH_NONNEGATIVE_ADMISSIBLE_K4_K7",
            "exact_passive_family": "PROVED_K8_K10",
            "positive_entrance_row": "FREQUENCY_INDEPENDENT_K11",
            "local_spacetime_cubic_mass": "EXACT_K12_DECAYS_K_MINUS_2",
            "trace_to_cubic_ratio": "DIVERGES_K_TO_THE_4_OVER_3_K13_K14",
            "physical_signed_flux": "EXACTLY_ZERO_K15_K16",
            "fixed_nonnegative_weight": "GENERAL_RIEMANN_LEBESGUE_LIMIT_K17",
            "limited_no_go": "FIXED_POSITIVE_ENTRANCE_WEIGHT_PLUS_LOCAL_CUBIC_ATOM_ALONE_K18",
            "signed_or_frequency_aware_repair": "OPEN_NOT_RULED_OUT",
            "full_version_m_trace_frequency_payment": "OPEN_NOT_RULED_OUT",
            "E24_counterexample": "NOT_CLAIMED_SIGNED_FLUX_ZERO",
            "transition_bands_and_periodic_geometry": "OPEN_NOT_PROVED",
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
            "independent_ruby": "PASS_21_OF_21",
            "negative_mutations": "PASS_PYTHON_100_OF_100_RUBY_100_OF_100",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_K1_TO_K18_18_OF_18",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75k.html",
            "target_pdf": "/notes/r0-75k.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075k_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 36,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 141,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075l",
        "latestPublishedResearchHtml": "/notes/r0-75k.html",
        "latestPublishedResearchPdf": "/notes/r0-75k.pdf",
        "latestReleaseGate": "tests/r075k-step36-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075k-step36-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075k-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075k-step36-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075k-step36-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075k-step36-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075k-step36-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075k-step36",
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
    write_text(PUBLIC / "notes/r0-75k.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 36,
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
