#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75P Step 41 from the verified R0.75O Step 40 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075o_step40_release as previous
import import_r075p_step41_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "aa7ab49f369211bb86f1c9c820a33129a4d22716"
VERSION = "2.20"
RELEASE = "r075p"
CODE = "R0.75P"
TITLE = "R0.75P｜入口浓度条件下 buffered collar 完成局部付款"
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
            raise RuntimeError(f"R0.75P frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075p_buffered_collar_entrance_concentration_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 21
        or certificate.get("assertions", {}).get("passed") != 21
        or len(certificate.get("checks", {})) != 21
    ):
        raise RuntimeError("R0.75P certificate verdict drift")
    main = (ROOT / "research/r075p_buffered_collar_entrance_concentration.md").read_text()
    for token in (
        r"\tag{P.1}",
        r"c_*a^{-1}\mu^{5/2}K^{-2}E_0^{3/2}",
        r"\tag{P.10}",
        r"\partial_t\phi_t+B\partial_2\phi_t=0",
        r"\tag{P.16}",
        r"\tau:=c_0\mu K^{-2}",
        r"\tag{P.20}",
        r"p_{K,\rm col}",
        r"\frac{8558}{178605}",
        "At equality the exponential rate vanishes",
        r"\tag{P.30}",
        r"\mathfrak X_{K,\rm col}",
        r"\tag{P.31}",
        "not a Littlewood--Paley",
        "low-concentration complement",
        "No novelty\nor priority claim",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75P boundary drift: {token}")


def render_step41_sections() -> str:
    source = (ROOT / "research/r075p_buffered_collar_entrance_concentration.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 320
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
    if section_index != 327:
        raise RuntimeError(f"Step 41 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.19"', 'data-site-version="2.20"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.19", "/i18n-en.js?v=2.20", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A quantified entrance-energy condition converts the constant-shear packet estimate into a genuine three-dimensional buffered-collar payment, with an exact strict concentration threshold.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75p.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75P · STEP 41 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75P · Step 41 · BUFFERED-COLLAR ENTRANCE CONCENTRATION</div><h1>{TITLE}</h1><p>若常剪切 real packet 在随流移动的入口 cutoff 中满足 <strong>E_in&gt;=mu E_0</strong>，局部能量可在 <strong>tau=c_0 mu K^(-2)</strong> 内保留至少一半。canonical plateau 的精确 fibre length 随即给出真正三维 collar cubic atom，并把 O 的 signed flux 以 <strong>mu^(-5/3)K^(-2/3)</strong> 支付。frozen scales 下严格条件是 <strong>0&lt;=sigma&lt;8558/178605</strong>；等号不含。最终接入 Version-M 只对同一速度的 actual component 成立，Fourier/LP projection 不在结论内。低入口浓度分支仍 <strong>OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">CONSTANT SHEAR</span><span class="label">ENTRANCE CONCENTRATION</span><span class="label">MOVING CUTOFF</span><span class="label">LOCAL ENERGY IDENTITY</span><span class="label">RADIAL PLATEAU FIBRES</span><span class="label">3D COLLAR CUBIC</span><span class="label">MU^5/2</span><span class="label">K^-2/3 GAIN</span><span class="label">SIGMA &lt; 8558/178605</span><span class="label">STRICT ENDPOINT</span><span class="label">ACTUAL COMPONENT ONLY</span><span class="label">PROJECTION EXCLUDED</span><span class="label">LOW CONCENTRATION OPEN</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75P STEP 41</strong><p>model：constant shear</p><p>assumption：E_in&gt;=mu E_0</p><p>persistence：tau=c_0 mu K^-2</p><p>local cubic：mu^(5/2) K^-2</p><p>flux gain：mu^(-5/3) K^-2/3</p><p>threshold：sigma&lt;8558/178605</p><p>endpoint：STRICTLY EXCLUDED</p><p>payment：ACTUAL COMPONENT ONLY</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step41_sections() + '\n<section id="reproduce">', "Step 41 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 41 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075p_buffered_collar_entrance_concentration.md">Step 41 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075p_buffered_collar_entrance_concentration_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075p_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075p_buffered_collar_entrance_concentration_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075p_buffered_collar_entrance_concentration_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075p_buffered_collar_entrance_concentration_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075p_buffered_collar_entrance_concentration_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075p_buffered_collar_entrance_concentration_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075p_buffered_collar_entrance_concentration_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075p_buffered_collar_entrance_concentration_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075p_buffered_collar_entrance_concentration_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075p_buffered_collar_entrance_concentration_qa.sh">QA script</a></p><p><a href="/notes/r0-75p.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 21/21、Ruby 22/22、P.1--P.31 与 31/31 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 132/132 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 41 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-315">← Step 40：constant-shear vertical-diffusion packet gain</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 41 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">low-entrance-concentration signed localization remains OPEN</h2><p style="margin:.15rem 0">本站在 R0.75P Step 41 停止。入口浓度满足严格 threshold 时，moving cutoff、plateau fibre 与 local-energy persistence 已把单个 constant-shear packet 支付到 genuine 3D buffered collar；最终 Version-M inclusion 只对同一速度的 actual component 成立。low-concentration branch、localized signed heat kernel / cancellation-preserving near-far estimate、nonconstant shear、inter-packet summation、low horizontal differences、移除 total upper-frequency cap、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均继续开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 41 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.19"', 'data-site-version="2.20"', "home version"),
        ("/i18n-en.js?v=2.19", "/i18n-en.js?v=2.20", "home i18n"),
        ("/site-refresh.js?v=2.19.1", "/site-refresh.js?v=2.20.1", "home refresh"),
        ("<strong>v2.19</strong>网页版本", "<strong>v2.20</strong>网页版本", "home stat version"),
        ("<strong>R0.75O</strong>最新研究节点", "<strong>R0.75P</strong>最新研究节点", "home latest"),
        ("<strong>243</strong>公开研究笔记", "<strong>244</strong>公开研究笔记", "home public count"),
        ("展开 153 篇公开笔记", "展开 154 篇公开笔记", "home route count"),
        ("综述 v2.19 · 2026-09-04", "综述 v2.20 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75O", "Research topology · R0.1–R0.75P", "home topology"),
        ('href="#r075o">跳到首页 R0.75O 卡片 →', 'href="#r075p">跳到首页 R0.75P 卡片 →', "home jump"),
        ("R0.70A–R0.75O：145 节已公开，104 节完整封存", "R0.70A–R0.75P：146 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75O</span>', '<span class="route-range">R0.69P–R0.75P</span>', "home range"),
        ("<h3>R0.75O：常剪切竖向扩散下的 packet flux gain</h3>", "<h3>R0.75P：入口浓度条件下的 buffered-collar payment</h3>", "home route title"),
        ("R0.72R–R0.75O：</span>", "R0.72R–R0.75P：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75O"', 'aria-label="R0.69P–R0.75P"', "home links label"),
        ("全站现有 243 篇公开研究笔记", "全站现有 244 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75P Step 41 在 quantified entrance concentration 下，把常剪切 packet 的 global full-T2 payment 局部化为 genuine 3D buffered-collar atom，并得到严格 sigma&lt;8558/178605 threshold。low-concentration signed localization、nonconstant shear、inter-packet 与 low differences 仍未闭合。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75P · 2026-09-04 · STEP 41 · BUFFERED-COLLAR ENTRANCE CONCENTRATION</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">对满足 E_in&gt;=mu E_0 的 constant-shear real packet，transported cutoff 保留局部能量至 tau=c_0 mu K^(-2)，canonical plateau fibres 给出 mu^(5/2) 的 genuine 3D collar cubic lower bound。与 O 的 signed-flux row 合并后得到 mu^(-5/3)K^(-2/3) gain；frozen scales 的严格条件为 sigma&lt;8558/178605。最终 Version-M inclusion 只覆盖同一速度的 actual component。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75p.pdf">阅读最新 R0.75P 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">244 篇研究笔记总索引</a><a href="#r075p">查看首页 R0.75P 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75P · 146 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75P Step 41 buffered-collar entrance concentration</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 41 converts the constant-shear packet estimate into a genuine three-dimensional buffered-collar payment under quantified entrance concentration; the strict frozen threshold is sigma&lt;8558/178605, while the low-concentration branch stays open.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain / physical-collar localization and packet summation open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment / low-concentration localization and packet summation open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75o.html">R0.75O</a>', '<a class="milestone" href="/notes/r0-75o.html">R0.75O</a>\n<a class="milestone" href="/notes/r0-75p.html">R0.75P</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>low-entrance-concentration signed localization remains open</h3><p>仍需用 localized signed heat kernel 或保留 cancellation 的 near/far decomposition 处理 low-concentration branch，并处理 nonconstant shear、inter-packet summation、low horizontal differences 与移除 total upper-frequency cap；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075p" data-release="r075p" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75P Step 41 · 2026-09-04 · BUFFERED-COLLAR ENTRANCE CONCENTRATION</p><h3>{TITLE}</h3><p>在 E_in&gt;=mu E_0 下，moving cutoff 与 canonical plateau fibre 给出 mu^(5/2) 的 3D collar cubic lower bound；结合 O 得到 mu^(-5/3)K^(-2/3) flux gain，严格 frozen threshold 是 sigma&lt;8558/178605。P.31 只覆盖 same-velocity actual component，projection 与 low-concentration branch 未闭合。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75p.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75p.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075o"'
    if anchor not in page:
        raise RuntimeError("home R0.75O card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.19"', 'data-site-version="2.20"', "literature version"),
        ("/i18n-en.js?v=2.19", "/i18n-en.js?v=2.20", "literature i18n"),
        ("文献综述 v2.19 · 2026-09-04", "文献综述 v2.20 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75O 只列为研究笔记", "本站 R0.69P–R0.75P 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>physical-collar localization, nonconstant shear and packet summation remain open</strong></header><p>physical buffered-collar cubic localization、nonconstant shear、inter-packet summation、low horizontal differences 与移除 total upper-frequency cap 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75P</b><strong>entrance-concentrated packets pay into a genuine 3D buffered collar</strong></header><p>Step 41 在 E_in&gt;=mu E_0 下，用 transported cutoff local-energy persistence 与 exact radial plateau fibre 得到 mu^(5/2) collar cubic lower bound；结合 O 的 signed-flux row 后得到 mu^(-5/3)K^(-2/3) gain，并给出严格 sigma&lt;8558/178605 threshold。最终 Version-M inclusion 只覆盖 same-velocity actual component。<a href="/notes/r0-75p.html">研究笔记</a> <a href="#r075p-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>low-entrance-concentration signed localization remains open</strong></header><p>localized signed heat kernel / cancellation-preserving near-far estimate、nonconstant shear、inter-packet summation、low horizontal differences 与移除 total upper-frequency cap 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075p-boundary">R0.75P Step 41 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Apraiz--Escauriaza--Wang--Zhang 2014 与 Wang--Wang--Zhang--Zhang 2019 给出 heat observability from measurable or thick sets 的相邻理论；Ervedoza--Zuazua 2011 显示 observability cost 对 geometry 与 time 的依赖；Coti Zelati--Gallay 2023 提供 higher-dimensional parallel shear 的语境。R0.75P 不导入这些 theorem，而是直接证明 transported-cutoff identity、local persistence、exact radial fibre 与 mu^(5/2) cubic lower bound。有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75P Step 41 公开边界</strong><p>'
        'PROVED：canonical plateau fibres P.7--P.10；moving-cutoff local energy and persistence P.14--P.20；physical-collar cubic lower bound P.21--P.24；conditional signed-flux estimate P.25--P.28；exact entrance threshold P.29--P.30；以及 stated alignment 下的 conditional Version-M payment P.31。'
        'SCOPE：constant shear、single real total-frequency-capped packet、E_in&gt;=mu E_0；sigma&lt;8558/178605 是严格充分条件；P.31 另需 same-velocity actual-component realization，Fourier/LP projection 明确排除；P.3--P.30 不使用该 realization。'
        'OPEN：low entrance concentration、localized signed heat kernel or cancellation-preserving near/far estimate、nonconstant shear、inter-packet summation、low horizontal differences、removal of the total upper-frequency cap、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75p.html">阅读完整笔记</a> · '
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
    if html_count != 244 or pdf_count not in (200, 201):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 184:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75p.html",
        "latestPublishedResearchPdf": "/notes/r0-75p.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075o":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 146
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 41
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "BUFFERED_COLLAR_CLOSURE_UNDER_QUANTIFIED_ENTRANCE_CONCENTRATION",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.SOURCE_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_BUFFERED_COLLAR_ENTRANCE_CONCENTRATION",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "constant_shear_model": "PROVED_CONDITIONALLY_P3_TO_P31",
            "entrance_concentration": "ASSUMED_E_IN_GE_MU_E0_P1",
            "canonical_plateau_fibres": "PROVED_P7_TO_P10",
            "moving_cutoff_transport": "EXACT_P14",
            "local_energy_identity": "EXACT_P16",
            "local_energy_persistence": "E_PHI_GE_MU_E0_OVER_2_TO_TAU_P20",
            "physical_collar_cubic_lower_bound": "C_STAR_A_MINUS_1_MU_5_OVER_2_K_MINUS_2_E0_3_OVER_2_P3_P21_TO_P24",
            "packet_flux_gain": "MU_MINUS_5_OVER_3_K_MINUS_2_OVER_3_P4_P26_TO_P28",
            "strict_concentration_threshold": "SIGMA_LT_8558_OVER_178605_P5_P29_P30",
            "threshold_equality": "EXCLUDED_EXPONENTIAL_RATE_ZERO_L_5_OVER_3_GROWS",
            "payment_scope": "CONDITIONAL_SAME_VELOCITY_ACTUAL_COMPONENT_P31",
            "packet_projection_payment": "EXCLUDED",
            "p3_to_p30_realization_independence": "PROVED",
            "physical_collar_localization": "PROVED_FOR_ENTRANCE_CONCENTRATED_PACKET",
            "low_entrance_concentration": "OPEN_NOT_COUNTEREXAMPLE",
            "localized_signed_heat_kernel": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_21_OF_21",
            "independent_ruby": "PASS_22_OF_22",
            "negative_mutations": "PASS_PYTHON_132_OF_132_RUBY_132_OF_132",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_P1_TO_P31_31_OF_31",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75p.html",
            "target_pdf": "/notes/r0-75p.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075p_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 41,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 146,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075q",
        "latestPublishedResearchHtml": "/notes/r0-75p.html",
        "latestPublishedResearchPdf": "/notes/r0-75p.pdf",
        "latestReleaseGate": "tests/r075p-step41-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075p-step41-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075p-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075p-step41-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075p-step41-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075p-step41-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075p-step41-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075p-step41",
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
    write_text(PUBLIC / "notes/r0-75p.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 41,
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
