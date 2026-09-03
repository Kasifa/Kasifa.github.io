#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75C Step 28 from the verified R0.75B Step 27 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075b_step27_release as previous
import import_r075c_step28_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.07"
RELEASE = "r075c"
CODE = "R0.75C"
TITLE = "R0.75C｜背景剪切的 packing 假阳性：B.44 普适性淘汰，passive dissipation 待解"
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
            raise RuntimeError(f"R0.75C frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r075c_background_shear_packing_false_positive_certificate.json").read_text())
    if certificate.get("verdict") != "PASS" or len(certificate.get("checks", {})) != 8 or certificate.get("tags") != 36:
        raise RuntimeError("R0.75C certificate verdict drift")
    main = (ROOT / "research/r075c_background_shear_packing_false_positive.md").read_text()
    for token in (
        "R075C_UNIVERSAL_NEFF_THRESHOLD_DISPROVED",
        "R075C_BACKGROUND_SHEAR_DISSIPATION_PAID",
        "R075C_TOTAL_CUBIC_PACKING_FALSE_POSITIVE",
        "R075C_PASSIVE_DISSIPATION_OPEN",
        r"\frac{27163}{158760000}>0",
        "direct outer-dissipation estimate (B.45) is neither proved nor",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75C boundary drift: {token}")


def render_step28_sections() -> str:
    source = (ROOT / "research/r075c_step28_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 225
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
    if section_index != 231:
        raise RuntimeError(f"Step 28 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.06"', 'data-site-version="2.07"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.06", "/i18n-en.js?v=2.07", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="The universal total-cubic packing threshold has a paid background-shear false positive; passive outer dissipation remains open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75c.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75C · STEP 28 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75C · Step 28 · PACKING FALSE POSITIVE</div><h1>{TITLE}</h1><p>冻结 saturation shear 使 total-velocity cubic packing 在 \(N\asymp R^{{-1}}\) 个 blocks 上饱和，却仍以 BV heat estimate 支付真实 shear dissipation。<strong>universal B.44：DISPROVED；B.45：NEITHER PROVED NOR DISPROVED；passive dissipation：OPEN。这不是 Navier--Stokes counterexample。NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">B.44 UNIVERSALITY DISPROVED</span><span class="label">SHEAR DISSIPATION PAID</span><span class="label">TOTAL-CUBIC FALSE POSITIVE</span><span class="label">B.45 UNDECIDED</span><span class="label">PASSIVE ROW OPEN</span><span class="label">NOT NSE COUNTEREXAMPLE</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75C STEP 28</strong><p>exact smooth saturation shear</p><p>universal B.44：DISPROVED</p><p>threshold gap：27163/158760000</p><p>shear dissipation：PAID</p><p>ratio：ω^(1/3)L^(-1/3) → 0</p><p>B.45：NEITHER PROVED NOR DISPROVED</p><p>passive dissipation：OPEN</p><p>full K / fixed deletion：OPEN</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step28_sections() + '\n<section id="reproduce">', "Step 28 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 28 主文、primary audit、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075c_background_shear_packing_false_positive.md">Step 28 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075c_background_shear_packing_false_positive_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075c_background_shear_packing_false_positive_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075c_background_shear_packing_false_positive_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075c_background_shear_packing_false_positive_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075c_background_shear_packing_false_positive_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075c_background_shear_packing_false_positive_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075c_background_shear_packing_false_positive_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075c_background_shear_packing_false_positive_qa.sh">QA script</a></p><p><a href="/notes/r0-75c.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 8/8、Ruby 9/9、36 unique tags、3 个 hash seeds 字节一致、18/18 与 19/19 mutations rejected。证书只覆盖 finite exact arithmetic、source binding 与 structural sentinels。本次白名单无新增 literature-collision artifact；bounded finite non-hit 不构成 novelty 或 priority 判断。本节纯解析，无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 28 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-216">← Step 27：outer padding gate</a> · <a href="#next">frequency-sensitive passive dissipation gate 仍 OPEN →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 28 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.75D 未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">frequency-sensitive passive dissipation gate 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75C Step 28 停止。下一命题必须证明 frequency-sensitive passive block estimate，或构造 accounting 完整的 exact forward passive family；二者均未完成。不得把 auxiliary B.44 false positive 写成 Navier--Stokes counterexample，不得把 B.45 写成已否定，也不得把 shear-row payment 写成 passive-row closure。full K、fixed deletion、arbitrary suitable weak extension、regularity 与 singularity 均未证明。R0.75D/E/F/G 与其他后续工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 28 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075c"[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.06"', 'data-site-version="2.07"', "home version"),
        ("/i18n-en.js?v=2.06", "/i18n-en.js?v=2.07", "home i18n"),
        ("/site-refresh.js?v=2.06.1", "/site-refresh.js?v=2.07.1", "home refresh"),
        ("<strong>v2.06</strong>网页版本", "<strong>v2.07</strong>网页版本", "home stat version"),
        ("<strong>R0.75B</strong>最新研究节点", "<strong>R0.75C</strong>最新研究节点", "home latest"),
        ("<strong>230</strong>公开研究笔记", "<strong>231</strong>公开研究笔记", "home public count"),
        ("展开 140 篇公开笔记", "展开 141 篇公开笔记", "home route count"),
        ("综述 v2.06 · 2026-09-03", "综述 v2.07 · 2026-09-03", "home footer"),
        ("Research topology · R0.1–R0.75B", "Research topology · R0.1–R0.75C", "home topology"),
        ('href="#r075b">跳到首页 R0.75B 卡片 →', 'href="#r075c">跳到首页 R0.75C 卡片 →', "home jump"),
        ("R0.70A–R0.75B：132 节已公开，104 节完整封存", "R0.70A–R0.75C：133 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75B</span>', '<span class="route-range">R0.69P–R0.75C</span>', "home range"),
        ("<h3>R0.75B：safe complete subclock 与 outer-dissipation packing gate</h3>", "<h3>R0.75C：background-shear packing false positive 与 passive-dissipation gate</h3>", "home route title"),
        ("R0.72R–R0.75B：</span>", "R0.72R–R0.75C：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75B"', 'aria-label="R0.69P–R0.75C"', "home links label"),
        ("全站现有 230 篇公开研究笔记", "全站现有 231 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.75C Step 28 证明 total-velocity cubic packing 会被低频、已支付的 background shear 触发为 false positive，因此 B.44 不能是普适必要条件。B.45 既未证也未否；下一缺口只剩 frequency-sensitive passive dissipation。</span></div>', "home focus")
    latest = rf'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75C · 2026-09-03 · STEP 28 · PACKING FALSE POSITIVE</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">saturation shear 使 \(N_{{\rm eff}}^{{\rm sh}}\asymp R^{{-1}}\) 并违反 B.44 threshold，却仍直接支付真实 shear dissipation。universal B.44 被否定；B.45 未被否定，passive row 仍 OPEN。这不是 NSE counterexample。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75c.pdf">阅读最新 R0.75C 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">231 篇研究笔记总索引</a><a href="#r075c">查看首页 R0.75C 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75C · 133 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75C Step 28 packing false positive</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 28 disproves universal necessity of the total-cubic packing threshold: a persistent low-frequency shear saturates the block count while its gradient dissipation is paid. B.45 remains undecided and only the passive dissipation row remains open.</p>', "home current summary")
    page = replace_once(page, 'moving-cutoff endpoint dichotomy → safe complete subclock paid / full endpoint paid / outer accumulated-dissipation packing open</p>', 'outer padding gate → total-cubic packing false positive / background shear paid / passive dissipation open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75b.html">R0.75B</a>', '<a class="milestone" href="/notes/r0-75b.html">R0.75B</a>\n<a class="milestone" href="/notes/r0-75c.html">R0.75C</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.75D NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>frequency-sensitive passive dissipation gate</h3><p>必须证明 passive-gradient block estimate 或构造 accounting 完整的 exact forward passive family。R0.75D/E/F/G 与后续工作未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075c" data-release="r075c" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75C Step 28 · 2026-09-03 · PACKING FALSE POSITIVE</p><h3>{TITLE}</h3><p>saturation shear 令 total-cubic \(N_{{\\rm eff}}\) 违反 B.44 threshold，但 shear dissipation 仍为 \(o((P_R^M)^{{2/3}})\)。因此 universal B.44 被否定，而 B.45 与 passive row 仍 OPEN。这不是 NSE counterexample。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75c.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75c.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075b"'
    if anchor not in page:
        raise RuntimeError("home R0.75B card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075c-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.06"', 'data-site-version="2.07"', "literature version"),
        ("/i18n-en.js?v=2.06", "/i18n-en.js?v=2.07", "literature i18n"),
        ("文献综述 v2.06 · 2026-09-03", "文献综述 v2.07 · 2026-09-03", "literature footer"),
        ("本站 R0.69P–R0.75B 只列为研究笔记", "本站 R0.69P–R0.75C 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · R0.75C</b><strong>outer-collar accumulated-dissipation packing</strong></header><p>必须证明有效 packing threshold 或构造 accounting 完整的 exact smooth counterexample；后续材料未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75C</b><strong>background-shear packing false positive and paid dissipation</strong></header><p>Step 28 证明 total-cubic packing 会对 persistent low-frequency background shear 产生 false positive；universal B.44 被否定，但 shear dissipation 已支付，B.45 与 passive row 仍 OPEN。<a href="/notes/r0-75c.html">研究笔记</a> <a href="#r075c-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.75D</b><strong>frequency-sensitive passive dissipation gate</strong></header><p>必须证明 passive-gradient block estimate 或构造 accounting 完整的 exact forward passive family；后续材料未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = r'<h3 id="r075c-boundary">R0.75C Step 28 的 bounded evidence 与主张边界</h3><p>本次冻结白名单没有新增 literature-collision artifact；handoff 只授权 bounded finite non-hit 表述，因此不形成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p><div class="boundary"><strong>R0.75C Step 28 公开边界</strong><p>PROVED：冻结 exact smooth saturation-shear family 上 \(N_{\rm eff}^{\rm sh}\asymp R^{-1}\)，精确 threshold gap 为 \(27163/158760000>0\)，从而 universal B.44 proposal 被否定；同一 shear 的 outer dissipation 仍由 \(\omega^{1/3}L^{-1/3}\to0\) 支付。FINITE：Python 8/8、Ruby 9/9、18/18 与 19/19 mutation rejection。OPEN：B.45、passive dissipation、full K、fixed deletion、arbitrary suitable-weak extension、regularity 与 singularity。这只是 auxiliary packing-condition counterexample，不是 Navier--Stokes counterexample。正式图件 NOT APPLICABLE；无 simulation、DNS 或 DGX。<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75c.html">阅读完整笔记</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap</a>。</p></div>' + "\n"
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 231 or pdf_count not in (187, 188):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(previous.previous.route_post_r060_slugs(HOME.read_text(encoding="utf-8")))
    if post_r060 != 171:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75c.html", "latestPublishedResearchPdf": "/notes/r0-75c.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169, "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075b":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 133
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22, "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27, "r075c": 28}
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1, "research_version": CODE,
        "scope": "BACKGROUND_SHEAR_PACKING_FALSE_POSITIVE_AND_PAID_DISSIPATION",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 9,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_ROUTE_PRUNING_LEMMA",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED", "dgx": "NOT_USED",
            "novelty_priority_publishability": "NOT_CLAIMED",
            "universal_b44": "DISPROVED",
            "b44_as_sufficient_condition": "REMAINS_VALID_WHEN_SATISFIED",
            "background_shear_dissipation": "PAID",
            "direct_b45": "NEITHER_PROVED_NOR_DISPROVED",
            "passive_dissipation": "OPEN",
            "navier_stokes_counterexample": "NOT_CLAIMED_NOT_PROVED",
            "full_clock_fixed_deletion": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_9_OF_9",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_8_OF_8",
            "independent_ruby": "PASS_9_OF_9",
            "negative_mutations": "PASS_PYTHON_18_OF_18_RUBY_19_OF_19",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/", "target_html": "/notes/r0-75c.html",
            "target_pdf": "/notes/r0-75c.pdf", "target_primary_figure": None,
            "recap_update_required": False, "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075c_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 28, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 133, "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075d", "latestPublishedResearchHtml": "/notes/r0-75c.html",
        "latestPublishedResearchPdf": "/notes/r0-75c.pdf",
        "latestReleaseGate": "tests/r075c-step28-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075c-step28-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075c-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075c-step28-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075c-step28-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075c-step28-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075c-step28-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075c-step28", "handoffCommit": None,
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
    write_text(PUBLIC / "notes/r0-75c.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 28,
        "siteVersion": VERSION, "recapUpdated": False, "recapNodes": 169,
        "formalFigure": None, "formalFigureExemption": True,
        "simulation": False, "pdeData": False, "noveltyClaim": False,
        "clayClaim": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
