#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75D Step 29 from the verified R0.75C Step 28 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075c_step28_release as previous
import import_r075d_step29_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.08"
RELEASE = "r075d"
CODE = "R0.75D"
TITLE = "R0.75D｜被动梯度的两区间估计：小支付已闭合，大支付相互作用待解"
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
            raise RuntimeError(f"R0.75D frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r075d_passive_gradient_route_screen_certificate.json").read_text())
    if certificate.get("verdict") != "PASS" or certificate.get("assertionsTotal") != 20 or len(certificate.get("checks", {})) != 20:
        raise RuntimeError("R0.75D certificate verdict drift")
    main = (ROOT / "research/r075d_passive_gradient_route_screen.md").read_text()
    for token in (
        "EXACT PASSIVE CACCIOPPOLI FALLBACK",
        "SMALL-PAYMENT PASSIVE OUTER DISSIPATION: PAID",
        "LOW FULL-SPATIAL FREQUENCY: PAID CONDITIONALLY",
        "HIGH-FREQUENCY LOCAL CAPTURE: OPEN",
        r"p_bp_F^2\le C(P_R^M)^2",
        "NO EXACT COUNTEREXAMPLE CONSTRUCTED",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75D boundary drift: {token}")


def render_step29_sections() -> str:
    source = (ROOT / "research/r075d_step29_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 231
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
    if section_index != 239:
        raise RuntimeError(f"Step 29 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.07"', 'data-site-version="2.08"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.07", "/i18n-en.js?v=2.08", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A proved passive Caccioppoli fallback closes the small-payment regime while the frozen large-payment interaction remains open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75d.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75D · STEP 29 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75D · Step 29 · PASSIVE GRADIENT ROUTE</div><h1>{TITLE}</h1><p>exact passive Caccioppoli ledger 给出 P^(2/3)+P fallback，并严格支付 P_R^M ≤ 1 的 small-payment regime。<strong>大支付 frozen branch 尚未闭合；low frequency 只有条件结论；interaction gate 与 complete clock 仍 OPEN。没有 exact counterexample。NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">PASSIVE FALLBACK PROVED</span><span class="label">SMALL-PAYMENT PAID</span><span class="label">LOW FREQUENCY CONDITIONAL</span><span class="label">LARGE-PAYMENT OPEN</span><span class="label">INTERACTION GATE OPEN</span><span class="label">NO COUNTEREXAMPLE</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75D STEP 29</strong><p>fallback：P^(2/3)+P · PROVED</p><p>P ≤ 1：PASSIVE ROW PAID</p><p>K_low rate：147163/476280000</p><p>frozen p_b rate：27163/158760000</p><p>interaction：p_b p_F^2 ≤ C P^2 · OPEN</p><p>high/intermediate bands：OPEN</p><p>complete clock：OPEN</p><p>exact counterexample：NONE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step29_sections() + '\n<section id="reproduce">', "Step 29 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 29 主文、primary-source boundary、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075d_passive_gradient_route_screen.md">Step 29 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075d_passive_gradient_route_screen_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075d_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075d_passive_gradient_route_screen_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075d_passive_gradient_route_screen_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075d_passive_gradient_route_screen_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075d_passive_gradient_route_screen_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075d_passive_gradient_route_screen_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075d_passive_gradient_route_screen_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075d_passive_gradient_route_screen_qa.sh">QA script</a></p><p><a href="/notes/r0-75d.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 20/20、Ruby 23/23、23 unique tags、23/23 displays、3 个 hash seeds 字节一致，双方 41/41 mutations rejected，unknown mutations fail closed。证书只覆盖 finite exact arithmetic、source binding 与 structural sentinels；primary-source screen 是 bounded non-hit。本节纯解析，无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 29 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-226">← Step 28：background-shear packing false positive</a> · <a href="#next">large-payment interaction / signed transport gate 仍 OPEN →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 29 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.75E 未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">large-payment interaction 与 localized frequency gate 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75D Step 29 停止。下一命题必须证明 interaction inequality、signed transport improvement 或 localized parabolic frequency dichotomy，或构造 accounting 完整的 exact forward counterexample；均未完成。不得把 P^(2/3)+P fallback 写成完整 B.45，不得把 conditional low-frequency calculation 写成无条件 theorem，也不得把 non-absorption 写成 counterexample。R0.75E/F/G/H 与其他后续工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 29 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075d"[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.07"', 'data-site-version="2.08"', "home version"),
        ("/i18n-en.js?v=2.07", "/i18n-en.js?v=2.08", "home i18n"),
        ("/site-refresh.js?v=2.07.1", "/site-refresh.js?v=2.08.1", "home refresh"),
        ("<strong>v2.07</strong>网页版本", "<strong>v2.08</strong>网页版本", "home stat version"),
        ("<strong>R0.75C</strong>最新研究节点", "<strong>R0.75D</strong>最新研究节点", "home latest"),
        ("<strong>231</strong>公开研究笔记", "<strong>232</strong>公开研究笔记", "home public count"),
        ("展开 141 篇公开笔记", "展开 142 篇公开笔记", "home route count"),
        ("综述 v2.07 · 2026-09-03", "综述 v2.08 · 2026-09-03", "home footer"),
        ("Research topology · R0.1–R0.75C", "Research topology · R0.1–R0.75D", "home topology"),
        ('href="#r075c">跳到首页 R0.75C 卡片 →', 'href="#r075d">跳到首页 R0.75D 卡片 →', "home jump"),
        ("R0.70A–R0.75C：133 节已公开，104 节完整封存", "R0.70A–R0.75D：134 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75C</span>', '<span class="route-range">R0.69P–R0.75D</span>', "home range"),
        ("<h3>R0.75C：background-shear packing false positive 与 passive-dissipation gate</h3>", "<h3>R0.75D：passive Caccioppoli fallback 与 large-payment interaction gate</h3>", "home route title"),
        ("R0.72R–R0.75C：</span>", "R0.72R–R0.75D：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75C"', 'aria-label="R0.69P–R0.75D"', "home links label"),
        ("全站现有 231 篇公开研究笔记", "全站现有 232 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.75D Step 29 证明 passive outer-dissipation 的 P^(2/3)+P fallback，并闭合 small-payment regime。冻结 common-shear branch 是严格 large payment；interaction inequality、signed transport 与 localized frequency capture 仍待解决。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75D · 2026-09-03 · STEP 29 · PASSIVE GRADIENT ROUTE</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">exact Caccioppoli ledger 证明 D_out,F ≤ C L^(2/3) ω^(1/3) P^(2/3) + C P，并支付 P ≤ 1；冻结 branch 的 large payment 使 interaction gate 仍 OPEN。无 exact counterexample。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75d.pdf">阅读最新 R0.75D 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">232 篇研究笔记总索引</a><a href="#r075d">查看首页 R0.75D 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75D · 134 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75D Step 29 passive gradient route</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 29 proves an unconditional passive P^(2/3)+P Caccioppoli fallback and closes the small-payment regime. The frozen branch is large-payment, so the interaction inequality, signed transport improvement, localized frequency capture, and complete clock remain open.</p>', "home current summary")
    page = replace_once(page, 'outer padding gate → total-cubic packing false positive / background shear paid / passive dissipation open</p>', 'packing false positive → passive Caccioppoli fallback / small payment paid / large-payment interaction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75c.html">R0.75C</a>', '<a class="milestone" href="/notes/r0-75c.html">R0.75C</a>\n<a class="milestone" href="/notes/r0-75d.html">R0.75D</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.75E NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>large-payment interaction / localized frequency gate</h3><p>必须证明 interaction inequality、signed transport improvement 或 localized parabolic frequency dichotomy，或构造 accounting 完整的 exact forward counterexample。R0.75E/F/G/H 与后续工作未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075d" data-release="r075d" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75D Step 29 · 2026-09-03 · PASSIVE GRADIENT ROUTE</p><h3>{TITLE}</h3><p>exact Caccioppoli ledger 给出 P^(2/3)+P fallback 并支付 small-payment regime；large-payment frozen branch、interaction gate 与 complete clock 仍 OPEN。low frequency 只有条件结论；无正式图、simulation、DNS、DGX 或 exact counterexample。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75d.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75d.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075c"'
    if anchor not in page:
        raise RuntimeError("home R0.75C card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075d-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.07"', 'data-site-version="2.08"', "literature version"),
        ("/i18n-en.js?v=2.07", "/i18n-en.js?v=2.08", "literature i18n"),
        ("文献综述 v2.07 · 2026-09-03", "文献综述 v2.08 · 2026-09-03", "literature footer"),
        ("本站 R0.69P–R0.75C 只列为研究笔记", "本站 R0.69P–R0.75D 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · R0.75D</b><strong>frequency-sensitive passive dissipation gate</strong></header><p>必须证明 passive-gradient block estimate 或构造 accounting 完整的 exact forward passive family；后续材料未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75D</b><strong>passive Caccioppoli fallback and large-payment interaction gate</strong></header><p>Step 29 证明无条件 P^(2/3)+P fallback 并支付 small-payment regime；low-frequency payment 仅为条件结论，large-payment interaction 与 complete clock 仍 OPEN。<a href="/notes/r0-75d.html">研究笔记</a> <a href="#r075d-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.75E</b><strong>large-payment interaction / localized frequency gate</strong></header><p>必须证明 interaction inequality、signed transport improvement 或 localized frequency dichotomy，或构造 accounting 完整的 exact forward counterexample；后续材料未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075d-boundary">R0.75D Step 29 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Albritton--Dong 支持 localized divergence-free transport 的 cutoff-flux 结构；'
        'Fernandez-Dalgo--Lemarie-Rieusset 显示 weighted energy 保留 drift row；'
        'Gardner--Liss--Mattingly 提供 streamline-sensitive enhanced-dissipation 背景。'
        '三者均不直接给出本站 time-dependent shear、periodic physical collar、dyadic payment 与 pure 2/3 exponent 的组合。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75D Step 29 公开边界</strong><p>'
        'PROVED：无条件 D_out,F ≤ C L^(2/3) omega^(1/3) P^(2/3) + C P 与 P ≤ 1 small-payment closure。'
        'CONDITIONAL：localized Rayleigh/cubic comparability 下的 low-frequency payment，rate 147163/476280000。'
        'FINITE：Python 20/20、Ruby 23/23，双方 41/41 mutation rejection。'
        'OPEN：large-payment interaction p_b p_F^2 ≤ C P^2、signed transport、high/intermediate frequency capture、'
        'commutators、periodic leakage、B.45 与 complete clock。冻结 branch 的 p_b rate 为 27163/158760000 > 0，'
        '只排除 small-payment implication，不是否定目标估计。无 exact counterexample、formal figure、simulation、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75d.html">阅读完整笔记</a> · '
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
    if html_count != 232 or pdf_count not in (188, 189):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(previous.previous.previous.route_post_r060_slugs(HOME.read_text(encoding="utf-8")))
    if post_r060 != 172:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75d.html", "latestPublishedResearchPdf": "/notes/r0-75d.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169, "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075c":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 134
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22, "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27, "r075c": 28, "r075d": 29}
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1, "research_version": CODE,
        "scope": "PASSIVE_OUTER_GRADIENT_TWO_REGIME_FALLBACK_AND_ROUTE_SCREEN",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 10,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_ROUTE_SCREEN",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED", "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "passive_caccioppoli_fallback": "PROVED_P_TWO_THIRDS_PLUS_P",
            "small_payment_passive_outer_dissipation": "PAID",
            "low_full_spatial_frequency": "PAID_CONDITIONALLY",
            "frozen_common_shear_branch": "LARGE_PAYMENT_NOT_CLOSED",
            "interaction_gate": "OPEN",
            "high_intermediate_frequency_capture": "OPEN",
            "commutators_periodic_leakage": "OPEN",
            "exact_counterexample": "NOT_CONSTRUCTED",
            "complete_clock": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_10_OF_10",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_20_OF_20",
            "independent_ruby": "PASS_23_OF_23",
            "negative_mutations": "PASS_PYTHON_41_OF_41_RUBY_41_OF_41",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/", "target_html": "/notes/r0-75d.html",
            "target_pdf": "/notes/r0-75d.pdf", "target_primary_figure": None,
            "recap_update_required": False, "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075d_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 29, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 134, "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075e", "latestPublishedResearchHtml": "/notes/r0-75d.html",
        "latestPublishedResearchPdf": "/notes/r0-75d.pdf",
        "latestReleaseGate": "tests/r075d-step29-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075d-step29-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075d-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075d-step29-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075d-step29-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075d-step29-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075d-step29-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075d-step29", "handoffCommit": None,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT, "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False, "recapRequired": False,
        },
        "latestRecapRelease": "r075a", "latestRecapHtml": "/recap-r0-61-r0-75a.html",
        "latestRecapPdf": "/recap-r0-61-r0-75a.pdf", "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-75d.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 29,
        "siteVersion": VERSION, "recapUpdated": False, "recapNodes": 169,
        "formalFigure": None, "formalFigureExemption": True,
        "simulation": False, "pdeData": False, "noveltyClaim": False,
        "clayClaim": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
