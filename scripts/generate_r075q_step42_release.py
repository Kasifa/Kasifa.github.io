#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75Q Step 42 from the verified R0.75P Step 41 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075p_step41_release as previous
import import_r075q_step42_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "7aa79f5f565ddcef024f328fc4e470d6a7601e71"
VERSION = "2.21"
RELEASE = "r075q"
CODE = "R0.75Q"
TITLE = "R0.75Q｜空间铺展单谐波的 physical-collar 付款"
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
            raise RuntimeError(f"R0.75Q frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075q_spatially_spread_harmonic_collar_payment_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions") != 20
        or certificate.get("passed") != 20
        or len(certificate.get("checks", {})) != 20
    ):
        raise RuntimeError("R0.75Q certificate verdict drift")
    main = (ROOT / "research/r075q_spatially_spread_harmonic_collar_payment.md").read_text()
    for token in (
        r"\tag{Q.1}",
        r"F_k(t,x_2)=A e^{-k^2t}\cos(k(x_2-Bt))",
        r"\tag{Q.10}",
        r"V_{\xi,3}:=\int_{\mathbb T^3}|\partial_2\xi_{a,R}|\,dx",
        r"\tag{Q.14}",
        r"\frac{A^2|B|V_{\xi,3}}{8k^2}",
        r"\tag{Q.18}",
        r"c_{\rm box}:=\frac{2(1-e^{-3})}{9\pi}",
        r"\tag{Q.21}",
        r"\frac{4279}{238140000}",
        r"\tag{Q.26}",
        "not asserted for a harmonic projection",
        r"\frac{E_{\rm in}}{E_0}\le\frac{a^2R^2}{2\pi}",
        r"\tag{Q.28}",
        "two or more horizontal harmonics",
        "No novelty or priority claim",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75Q boundary drift: {token}")


def render_step42_sections() -> str:
    source = (ROOT / "research/r075q_spatially_spread_harmonic_collar_payment.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 327
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
    if section_index != 334:
        raise RuntimeError(f"Step 42 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.20"', 'data-site-version="2.21"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.20", "/i18n-en.js?v=2.21", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A phase-uniform rectangular subcollar converts one spatially spread constant-shear harmonic into a genuine physical-collar cubic payment without an entrance-concentration hypothesis.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75q.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75Q · STEP 42 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75Q · Step 42 · SPATIALLY SPREAD HARMONIC COLLAR PAYMENT</div><h1>{TITLE}</h1><p>对独立于 <strong>x_1,x_3</strong> 的单个 constant-shear real harmonic，radial cutoff 的常数行先精确消失；phase-uniform period count 与 rectangular subcollar 随后给出 <strong>M_col &gt;= c_box delta_0 a^2 R^3 k^(-2) A^3</strong>，从而以 <strong>k^(-2/3) M_col^(2/3)</strong> 支付 signed flux。该机制不需要入口浓度条件，并覆盖 P 未触及的一个空间铺展 benchmark；多模干涉、vertical structure 与一般 low-entrance packet 仍 <strong>OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">CONSTANT SHEAR</span><span class="label">ONE REAL HARMONIC</span><span class="label">SPATIALLY SPREAD</span><span class="label">EXACT ZERO ROW</span><span class="label">RADIAL DERIVATIVE L1</span><span class="label">PHASE-UNIFORM PERIODS</span><span class="label">RECTANGULAR SUBCOLLAR</span><span class="label">3D COLLAR CUBIC</span><span class="label">K^-2/3 GAIN</span><span class="label">NO ENTRANCE CONCENTRATION</span><span class="label">ACTUAL COMPONENT ONLY</span><span class="label">PROJECTION EXCLUDED</span><span class="label">MULTIMODE OPEN</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75Q STEP 42</strong><p>model：one real shear harmonic</p><p>geometry：radial plateau shell</p><p>phase bound：uniform</p><p>local cubic：R^3 k^-2 A^3</p><p>flux gain：k^-2/3 M_col^2/3</p><p>coefficient：L^2/3 exp(-4279L^2/238140000)</p><p>entrance hypothesis：NOT USED</p><p>payment：ACTUAL COMPONENT ONLY</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step42_sections() + '\n<section id="reproduce">', "Step 42 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 42 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075q_spatially_spread_harmonic_collar_payment.md">Step 42 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075q_spatially_spread_harmonic_collar_payment_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075q_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075q_spatially_spread_harmonic_collar_payment_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075q_spatially_spread_harmonic_collar_payment_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075q_spatially_spread_harmonic_collar_payment_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075q_spatially_spread_harmonic_collar_payment_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075q_spatially_spread_harmonic_collar_payment_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075q_spatially_spread_harmonic_collar_payment_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075q_spatially_spread_harmonic_collar_payment_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075q_spatially_spread_harmonic_collar_payment_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075q_spatially_spread_harmonic_collar_payment_qa.sh">QA script</a></p><p><a href="/notes/r0-75q.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 20/20、Ruby 21/21、Q.1--Q.28 与 28/28 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 180/180 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 42 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-321">← Step 41：entrance-concentrated buffered-collar payment</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 42 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">general low-entrance packets and multimode interference remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75Q Step 42 停止。Q 仅对一个独立于 x_1,x_3 的空间铺展 real harmonic，用 exact zero row、phase-uniform periods 与 rectangular subcollar 闭合 physical-collar payment；Version-M inclusion 仍只对同一速度的 actual component 成立。两个及以上 horizontal modes、destructive interference、arbitrary vertical structure、一般 low-entrance packet、nonconstant shear、inter-packet / low-difference summation、移除 total upper-frequency cap、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均继续开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 42 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.20"', 'data-site-version="2.21"', "home version"),
        ("/i18n-en.js?v=2.20", "/i18n-en.js?v=2.21", "home i18n"),
        ("/site-refresh.js?v=2.20.1", "/site-refresh.js?v=2.21.1", "home refresh"),
        ("<strong>v2.20</strong>网页版本", "<strong>v2.21</strong>网页版本", "home stat version"),
        ("<strong>R0.75P</strong>最新研究节点", "<strong>R0.75Q</strong>最新研究节点", "home latest"),
        ("<strong>244</strong>公开研究笔记", "<strong>245</strong>公开研究笔记", "home public count"),
        ("展开 154 篇公开笔记", "展开 155 篇公开笔记", "home route count"),
        ("综述 v2.20 · 2026-09-04", "综述 v2.21 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75P", "Research topology · R0.1–R0.75Q", "home topology"),
        ('href="#r075p">跳到首页 R0.75P 卡片 →', 'href="#r075q">跳到首页 R0.75Q 卡片 →', "home jump"),
        ("R0.70A–R0.75P：146 节已公开，104 节完整封存", "R0.70A–R0.75Q：147 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75P</span>', '<span class="route-range">R0.69P–R0.75Q</span>', "home range"),
        ("<h3>R0.75P：入口浓度条件下的 buffered-collar payment</h3>", "<h3>R0.75Q：空间铺展单谐波的 physical-collar payment</h3>", "home route title"),
        ("R0.72R–R0.75P：</span>", "R0.72R–R0.75Q：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75P"', 'aria-label="R0.69P–R0.75Q"', "home links label"),
        ("全站现有 244 篇公开研究笔记", "全站现有 245 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75Q Step 42 对一个独立于 x_1,x_3 的空间铺展 constant-shear real harmonic，用 exact zero row、phase-uniform period count 与 rectangular subcollar 完成 physical-collar payment。multimode interference、vertical structure 与一般 low-entrance packet 仍未闭合。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75Q · 2026-09-04 · STEP 42 · SPATIALLY SPREAD HARMONIC COLLAR PAYMENT</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">一个独立于 x_1,x_3 的 constant-shear real harmonic 在 radial derivative row 上先发生 exact constant-row cancellation。phase-uniform period count 与 rectangular subcollar 再给出 M_col &gt;= c_box delta_0 a^2 R^3 k^(-2) A^3，并以 k^(-2/3)M_col^(2/3) 支付 signed flux；不需要 entrance concentration。Version-M inclusion 只覆盖同一速度的 actual component。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75q.pdf">阅读最新 R0.75Q 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">245 篇研究笔记总索引</a><a href="#r075q">查看首页 R0.75Q 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75Q · 147 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75Q Step 42 spatially spread harmonic collar payment</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 42 uses exact zero-row cancellation and a phase-uniform rectangular subcollar to pay one spatially spread constant-shear harmonic into its physical collar without entrance concentration; multimode interference and general low-entrance packets stay open.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment / low-concentration localization and packet summation open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment → spatially spread one-harmonic collar payment / multimode and general low-entrance packets open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75p.html">R0.75P</a>', '<a class="milestone" href="/notes/r0-75p.html">R0.75P</a>\n<a class="milestone" href="/notes/r0-75q.html">R0.75Q</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>general low-entrance packets and multimode interference remain open</h3><p>仍需处理两个及以上 horizontal modes 的 destructive interference、arbitrary vertical structure、一般 low-entrance packet、nonconstant shear、inter-packet / low-difference summation 与移除 total upper-frequency cap；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075q" data-release="r075q" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75Q Step 42 · 2026-09-04 · SPATIALLY SPREAD HARMONIC COLLAR PAYMENT</p><h3>{TITLE}</h3><p>对一个独立于 x_1,x_3 的空间铺展 constant-shear real harmonic，exact zero row、phase-uniform periods 与 rectangular subcollar 给出 R^3k^(-2)A^3 的 local cubic，并把 signed flux 化为 k^(-2/3)M_col^(2/3)。不需要 entrance concentration；Q.26 只覆盖 same-velocity actual component，多模与一般 low-entrance packet 未闭合。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75q.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75q.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075p"'
    if anchor not in page:
        raise RuntimeError("home R0.75P card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.20"', 'data-site-version="2.21"', "literature version"),
        ("/i18n-en.js?v=2.20", "/i18n-en.js?v=2.21", "literature i18n"),
        ("文献综述 v2.20 · 2026-09-04", "文献综述 v2.21 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75P 只列为研究笔记", "本站 R0.69P–R0.75Q 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>low-entrance-concentration signed localization remains open</strong></header><p>localized signed heat kernel / cancellation-preserving near-far estimate、nonconstant shear、inter-packet summation、low horizontal differences 与移除 total upper-frequency cap 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75Q</b><strong>one spatially spread harmonic pays into its physical collar</strong></header><p>Step 42 对独立于 x_1,x_3 的一个 constant-shear real harmonic，先用 exact constant-row cancellation 控制 signed cutoff flux，再用 phase-uniform period count 与 rectangular subcollar 得到 cubic mass；最终有 k^(-2/3)M_col^(2/3) payment，且不需要 entrance concentration。Version-M inclusion 只覆盖 same-velocity actual component。<a href="/notes/r0-75q.html">研究笔记</a> <a href="#r075q-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>multimode interference and general low-entrance packets remain open</strong></header><p>两个及以上 horizontal modes、destructive interference、arbitrary vertical structure、一般 low-entrance packet、nonconstant shear、inter-packet / low-difference summation 与移除 total upper-frequency cap 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075q-boundary">R0.75Q Step 42 的 bounded primary-source screen 与主张边界</h3>'
        '<p>He 2022 给出 passive scalar 的 mode-by-mode shear diffusion；Gardner--Liss--Mattingly 2024 与 He 2026 给出 pathwise 或 streamline-localized enhanced dissipation；Jimenez-Urias--Haine 2021 给出 periodic shear 的 exact modal solution；Wang--Wang--Zhang--Zhang 2019 则处理 thick or positive-measure sets 上的 heat observability。这些相邻结果都不是 shrinking spherical shell 上的 signed derivative cutoff 与 local L3 atom payment。R0.75Q 不导入其 theorem，而是直接证明 phase-uniform period bound 与 rectangular subcollar estimate。有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75Q Step 42 公开边界</strong><p>'
        'PROVED：radial derivative L1 row Q.8--Q.10；exact diagonal cancellation 与 flux bound Q.11--Q.14；phase-uniform rectangular subcollar Q.15--Q.21；physical-collar cubic conversion Q.22--Q.25；stated alignment 下的 conditional actual-component Version-M payment Q.26；low-entrance diagnostic Q.27--Q.28。'
        'SCOPE：constant shear、one real horizontal harmonic、independent of x_1,x_3、total-field based；不需要 entrance concentration；Q.26 另需 same-velocity actual-component realization，Fourier/LP projection 与 arbitrary zero-trajectory realization 明确排除。'
        'OPEN：two or more horizontal modes、destructive interference、arbitrary vertical structure、general low-entrance packets、nonconstant shear、inter-packet / low-difference summation、removal of the total upper-frequency cap、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75q.html">阅读完整笔记</a> · '
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
    if html_count != 245 or pdf_count not in (201, 202):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 185:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75q.html",
        "latestPublishedResearchPdf": "/notes/r0-75q.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075p":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 147
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 42
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "PHYSICAL_COLLAR_PAYMENT_FOR_ONE_SPATIALLY_SPREAD_SHEAR_HARMONIC",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.SOURCE_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_SPATIALLY_SPREAD_HARMONIC_COLLAR_PAYMENT",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "constant_shear_model": "PROVED_FOR_ONE_REAL_HARMONIC_Q1_TO_Q28",
            "spatially_spread_harmonic": "INDEPENDENT_OF_X1_X3",
            "entrance_concentration": "NOT_ASSUMED_LOW_ENTRANCE_DIAGNOSTIC_Q27_Q28",
            "radial_derivative_l1_row": "PROVED_Q8_TO_Q10",
            "signed_flux_cancellation": "EXACT_CONSTANT_ROW_ZERO_Q11_TO_Q14",
            "phase_uniform_period_bound": "PROVED_Q15_TO_Q19",
            "physical_collar_cubic_lower_bound": "C_BOX_DELTA0_A2_R3_K_MINUS2_A3_Q3_Q20_Q21",
            "harmonic_flux_gain": "K_MINUS_2_OVER_3_M_COL_2_OVER_3_Q4_Q22",
            "frozen_normalization": "L_2_OVER_3_R_MINUS_2_OVER_3_OMEGA_1_OVER_3_Q5_Q6_Q23_TO_Q25",
            "payment_scope": "CONDITIONAL_SAME_VELOCITY_ACTUAL_COMPONENT_Q26",
            "harmonic_projection_payment": "EXCLUDED",
            "arbitrary_zero_trajectory_realization": "EXCLUDED",
            "physical_collar_localization": "PROVED_FOR_ONE_SPATIALLY_SPREAD_HARMONIC",
            "general_low_entrance_packets": "OPEN_NOT_COUNTEREXAMPLE",
            "multimode_interference": "OPEN_NOT_PROVED",
            "arbitrary_vertical_structure": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_20_OF_20",
            "independent_ruby": "PASS_21_OF_21",
            "negative_mutations": "PASS_PYTHON_180_OF_180_RUBY_180_OF_180",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_Q1_TO_Q28_28_OF_28",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75q.html",
            "target_pdf": "/notes/r0-75q.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075q_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 42,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 147,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075r",
        "latestPublishedResearchHtml": "/notes/r0-75q.html",
        "latestPublishedResearchPdf": "/notes/r0-75q.pdf",
        "latestReleaseGate": "tests/r075q-step42-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075q-step42-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075q-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075q-step42-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075q-step42-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075q-step42-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075q-step42-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075q-step42",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
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
    write_text(PUBLIC / "notes/r0-75q.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 42,
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
