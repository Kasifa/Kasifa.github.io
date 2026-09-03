#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75E Step 30 from the verified R0.75D Step 29 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075d_step29_release as previous
import import_r075e_step30_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.09"
RELEASE = "r075e"
CODE = "R0.75E"
TITLE = "R0.75E｜横向交叉模态通量：实零模全支付，任意实场聚合待解"
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
            raise RuntimeError(f"R0.75E frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075e_horizontal_cross_mode_flux_reduction_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsTotal") != 13
        or len(certificate.get("checks", {})) != 13
    ):
        raise RuntimeError("R0.75E certificate verdict drift")
    main = (ROOT / "research/r075e_horizontal_cross_mode_flux_reduction.md").read_text()
    for token in (
        "purely off-diagonal",
        r"\partial_2F=0",
        r"\mathcal T_\xi(F,b)",
        r"\mathfrak X_{\xi,R}(F,b)\le C(P_R^M)^{2/3}",
        "No such bound is proved here",
        "Algebraic diagnostic only",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75E boundary drift: {token}")


def render_step30_sections() -> str:
    source = (ROOT / "research/r075e_step30_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 239
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
    if section_index != 247:
        raise RuntimeError(f"Step 30 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.08"', 'data-site-version="2.09"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.08", "/i18n-en.js?v=2.09", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="The exact horizontal difference-frequency identity closes the real zero mode for all payment while the arbitrary-real cross-mode gate remains open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75e.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75E · STEP 30 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75E · Step 30 · HORIZONTAL CROSS-MODE FLUX</div><h1>{TITLE}</h1><p>exact Fourier convolution 证明 transport flux 只含 off-diagonal difference frequencies。<strong>实 horizontal zero mode 在任意 payment 下已闭合；complex singleton 仅是代数诊断；任意实场的 signed cross-mode aggregation 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">DIFFERENCE-FREQUENCY IDENTITY PROVED</span><span class="label">DIAGONAL FLUX ZERO</span><span class="label">REAL ZERO MODE ALL-PAYMENT PAID</span><span class="label">COMPLEX SINGLETON DIAGNOSTIC ONLY</span><span class="label">REAL ±N PAIR MAY COUPLE</span><span class="label">GENERAL CROSS-MODE GATE OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75E STEP 30</strong><p>diagonal transport：ZERO</p><p>real zero mode：ALL-PAYMENT PAID</p><p>vertical frequency：ARBITRARY</p><p>finite real pair：T_xi / pi = -1/2</p><p>complex singleton：DIAGNOSTIC ONLY</p><p>general cross-mode gate：OPEN</p><p>complete clock：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step30_sections() + '\n<section id="reproduce">', "Step 30 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 30 主文、primary-source boundary、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075e_horizontal_cross_mode_flux_reduction.md">Step 30 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075e_horizontal_cross_mode_flux_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075e_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075e_horizontal_cross_mode_flux_reduction_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075e_horizontal_cross_mode_flux_reduction_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075e_horizontal_cross_mode_flux_reduction_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075e_horizontal_cross_mode_flux_reduction_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075e_horizontal_cross_mode_flux_reduction_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075e_horizontal_cross_mode_flux_reduction_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075e_horizontal_cross_mode_flux_reduction_qa.sh">QA script</a></p><p><a href="/notes/r0-75e.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 13/13、Ruby 16/16、24 unique tags、24/24 displays、3 个 hash seeds 字节一致，双方 39/39 mutations rejected，unknown mutations fail closed。finite Laurent witness 只验证 E.10 algebra 与 normalization，不是 full spacetime trajectory 或 geometric collar finite model。本节纯解析，无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 30 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-232">← Step 29：passive two-regime fallback</a> · <a href="#next">arbitrary-real signed cross-mode gate 仍 OPEN →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 30 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.75F 未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">arbitrary-real signed cross-mode aggregation 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75E Step 30 停止。下一命题必须控制正 signed cross-mode flux，或建立 difference-frequency decay / localized observability，且不得把 complex singleton 当作物理实场、不得把 finite witness 当作完整 trajectory。complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均未闭合。R0.75F/G/H 与其他后续工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 30 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075e"[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.08"', 'data-site-version="2.09"', "home version"),
        ("/i18n-en.js?v=2.08", "/i18n-en.js?v=2.09", "home i18n"),
        ("/site-refresh.js?v=2.08.1", "/site-refresh.js?v=2.09.1", "home refresh"),
        ("<strong>v2.08</strong>网页版本", "<strong>v2.09</strong>网页版本", "home stat version"),
        ("<strong>R0.75D</strong>最新研究节点", "<strong>R0.75E</strong>最新研究节点", "home latest"),
        ("<strong>232</strong>公开研究笔记", "<strong>233</strong>公开研究笔记", "home public count"),
        ("展开 142 篇公开笔记", "展开 143 篇公开笔记", "home route count"),
        ("综述 v2.08 · 2026-09-03", "综述 v2.09 · 2026-09-03", "home footer"),
        ("Research topology · R0.1–R0.75D", "Research topology · R0.1–R0.75E", "home topology"),
        ('href="#r075d">跳到首页 R0.75D 卡片 →', 'href="#r075e">跳到首页 R0.75E 卡片 →', "home jump"),
        ("R0.70A–R0.75D：134 节已公开，104 节完整封存", "R0.70A–R0.75E：135 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75D</span>', '<span class="route-range">R0.69P–R0.75E</span>', "home range"),
        ("<h3>R0.75D：passive Caccioppoli fallback 与 large-payment interaction gate</h3>", "<h3>R0.75E：horizontal difference-frequency identity 与 real zero-mode all-payment closure</h3>", "home route title"),
        ("R0.72R–R0.75D：</span>", "R0.72R–R0.75E：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75D"', 'aria-label="R0.69P–R0.75E"', "home links label"),
        ("全站现有 232 篇公开研究笔记", "全站现有 233 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75E Step 30 证明 localized shear-transport flux 是纯 off-diagonal difference-frequency quantity，并在任意 payment 下闭合 admissible real horizontal zero mode。任意实场的 signed cross-mode aggregation、complete clock 与 suitable-weak transfer 仍待解决。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75E · 2026-09-03 · STEP 30 · HORIZONTAL CROSS-MODE FLUX</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">exact signed convolution 证明 diagonal flux 为零，并给出 real horizontal zero mode 的 all-payment P^(2/3) closure。nonzero complex singleton 只作代数诊断；general real ±n pairs 与 cross-mode gate 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75e.pdf">阅读最新 R0.75E 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">233 篇研究笔记总索引</a><a href="#r075e">查看首页 R0.75E 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75E · 135 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75E Step 30 horizontal cross-mode flux</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(
        page,
        r'<p class="tree-current-summary">.*?</p>',
        '<p class="tree-current-summary">Step 30 proves the exact horizontal difference-frequency identity and closes the admissible real zero mode for all payment. A nonzero complex singleton is diagnostic only; arbitrary-real signed cross-mode aggregation and the complete clock remain open.</p>',
        "home current summary",
    )
    page = replace_once(
        page,
        'packing false positive → passive Caccioppoli fallback / small payment paid / large-payment interaction open</p>',
        'passive fallback → exact difference-frequency flux / real zero mode all-payment paid / arbitrary-real cross-mode gate open</p>',
        "home route path",
    )
    page = replace_once(
        page,
        '<a class="milestone" href="/notes/r0-75d.html">R0.75D</a>',
        '<a class="milestone" href="/notes/r0-75d.html">R0.75D</a>\n<a class="milestone" href="/notes/r0-75e.html">R0.75E</a>',
        "home milestone",
    )
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.75F NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>arbitrary-real signed cross-mode aggregation</h3><p>必须控制 positive signed cross-mode flux，或建立 difference-frequency decay / localized observability。R0.75F/G/H 与后续工作未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075e" data-release="r075e" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75E Step 30 · 2026-09-03 · HORIZONTAL CROSS-MODE FLUX</p><h3>{TITLE}</h3><p>exact difference-frequency identity 消去全部 diagonal transport，并在任意 payment 下支付 real horizontal zero mode。complex singleton 仅是 algebraic diagnostic；general real cross-mode gate 仍 OPEN。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75e.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75e.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075d"'
    if anchor not in page:
        raise RuntimeError("home R0.75D card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075e-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.08"', 'data-site-version="2.09"', "literature version"),
        ("/i18n-en.js?v=2.08", "/i18n-en.js?v=2.09", "literature i18n"),
        ("文献综述 v2.08 · 2026-09-03", "文献综述 v2.09 · 2026-09-03", "literature footer"),
        ("本站 R0.69P–R0.75D 只列为研究笔记", "本站 R0.69P–R0.75E 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · R0.75E</b><strong>large-payment interaction / localized frequency gate</strong></header><p>必须证明 interaction inequality、signed transport improvement 或 localized frequency dichotomy，或构造 accounting 完整的 exact forward counterexample；后续材料未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75E</b><strong>horizontal difference-frequency identity and real zero-mode closure</strong></header><p>Step 30 证明 localized transport 是纯 off-diagonal difference-frequency flux，并在任意 payment 下支付 admissible real zero mode；complex singleton 仅作代数诊断，general real cross-mode gate 仍 OPEN。<a href="/notes/r0-75e.html">研究笔记</a> <a href="#r075e-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.75F</b><strong>arbitrary-real signed cross-mode aggregation</strong></header><p>必须控制 positive signed cross-mode flux，或建立 difference-frequency decay / localized observability；后续材料未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075e-boundary">R0.75E Step 30 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Siming He 支持 shear 对 streamwise Fourier modes 的保持及 transverse-only data 的 heat evolution；'
        'Gardner--Liss--Mattingly 支持 streamline average decoupling；Albritton--Dong 支持 physical localization 保留 drift flux。'
        '这些来源均不直接给出本站 spherical physical collar、Xi_(m-n) convolution 与 Version-M P^(2/3) normalization 的组合。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75E Step 30 公开边界</strong><p>'
        'PROVED：带终端项和正确符号的 local energy identity、horizontal support invariance、exact difference-frequency formula、'
        'diagonal cancellation、zero-flux spectral-sector closure，以及 real horizontal zero mode 的 all-payment P^(2/3) estimate。'
        'FINITE：real +/-1 witness 的 T_xi/pi = -1/2；Python 13/13、Ruby 16/16，双方 39/39 mutation rejection。'
        'DIAGNOSTIC ONLY：nonzero complex singleton，不是 physical real Navier--Stokes velocity。'
        'OPEN：arbitrary-real signed cross-mode bound、real +/-n aggregation、cutoff Fourier tails、complete clock、fixed deletion、'
        'suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75e.html">阅读完整笔记</a> · '
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
    if html_count != 233 or pdf_count not in (189, 190):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(previous.previous.previous.previous.route_post_r060_slugs(HOME.read_text(encoding="utf-8")))
    if post_r060 != 173:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75e.html",
        "latestPublishedResearchPdf": "/notes/r0-75e.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075d":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 135
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "HORIZONTAL_CROSS_MODE_FLUX_REDUCTION_AND_REAL_ZERO_MODE_ALL_PAYMENT_CLOSURE",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 10,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_STRUCTURAL_REDUCTION",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "horizontal_difference_frequency_identity": "PROVED",
            "diagonal_transport_flux": "ZERO_PROVED",
            "real_horizontal_zero_mode": "ALL_PAYMENT_PAID",
            "zero_flux_spectral_sector": "PAID_CONDITIONALLY",
            "complex_singleton": "ALGEBRAIC_DIAGNOSTIC_ONLY_NOT_PHYSICAL",
            "real_nonzero_harmonic": "PAIR_MAY_COUPLE",
            "general_signed_cross_mode_gate": "OPEN",
            "complete_clock": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_10_OF_10",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_13_OF_13",
            "independent_ruby": "PASS_16_OF_16",
            "negative_mutations": "PASS_PYTHON_39_OF_39_RUBY_39_OF_39",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75e.html",
            "target_pdf": "/notes/r0-75e.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075e_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 30,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 135,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075f",
        "latestPublishedResearchHtml": "/notes/r0-75e.html",
        "latestPublishedResearchPdf": "/notes/r0-75e.pdf",
        "latestReleaseGate": "tests/r075e-step30-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075e-step30-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075e-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075e-step30-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075e-step30-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075e-step30-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075e-step30-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075e-step30",
            "handoffCommit": None,
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
    write_text(PUBLIC / "notes/r0-75e.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 30,
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
