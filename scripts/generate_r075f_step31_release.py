#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75F Step 31 from the verified R0.75E Step 30 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075e_step30_release as previous
import import_r075f_step31_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.10"
RELEASE = "r075f"
CODE = "R0.75F"
TITLE = "R0.75F｜模态相位积分恒等式：离对角账本精确回收，正性比较失效"
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
            raise RuntimeError(f"R0.75F frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075f_modal_phase_integration_identity_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 16
        or len(certificate.get("checks", {})) != 16
    ):
        raise RuntimeError("R0.75F certificate verdict drift")
    main = (ROOT / "research/r075f_modal_phase_integration_identity.md").read_text()
    for token in (
        r"i\ell b g_{nm}",
        r"\mathcal T_\xi",
        r"\mathcal E_{\rm diag}+\mathcal D_{\rm diag}",
        r"\frac{2N+N^{-1}}3\longrightarrow\infty",
        "not a counterexample to the R0.75E target",
        "None of these is proved here.",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75F boundary drift: {token}")


def render_step31_sections() -> str:
    source = (ROOT / "research/r075f_step31_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 247
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
    if section_index != 255:
        raise RuntimeError(f"Step 31 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.09"', 'data-site-version="2.10"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.09", "/i18n-en.js?v=2.10", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Exact modal phase integration recovers only the existing off-diagonal energy ledger, while positivity alone cannot control the localized form">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75f.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75F · STEP 31 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75F · Step 31 · MODAL PHASE-INTEGRATION NO-GO</div><h1>{TITLE}</h1><p>direct modal phase integration 精确重建同一个 off-diagonal energy ledger，不能凭代数产生新 coercivity。<strong>positivity-only diagonal comparison 被 exact real Fejer family 排除；E.24 与真正的 dynamic/payment-sensitive routes 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">MODAL PRODUCT IDENTITY PROVED</span><span class="label">OFF-DIAGONAL LEDGER RECONSTRUCTED</span><span class="label">PHASE SUBSTITUTION TAUTOLOGICAL</span><span class="label">POSITIVITY-ONLY CONTROL FALSE</span><span class="label">NOT AN E.24 COUNTEREXAMPLE</span><span class="label">DYNAMIC ROUTES REMAIN VIABLE</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75F STEP 31</strong><p>phase identity：PROVED</p><p>off-diagonal residual：ZERO</p><p>diagonal identity：UNCHANGED</p><p>Fejer ratios：19/9 · 17/5 · 33/7</p><p>positivity-only route：REJECTED</p><p>frozen-collar counterexample：NO</p><p>E.24：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step31_sections() + '\n<section id="reproduce">', "Step 31 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 31 主文、primary-source boundary、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075f_modal_phase_integration_identity.md">Step 31 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075f_modal_phase_integration_identity_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075f_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075f_modal_phase_integration_identity_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075f_modal_phase_integration_identity_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075f_modal_phase_integration_identity_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075f_modal_phase_integration_identity_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075f_modal_phase_integration_identity_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075f_modal_phase_integration_identity_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075f_modal_phase_integration_identity_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075f_modal_phase_integration_identity_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075f_modal_phase_integration_identity_qa.sh">QA script</a></p><p><a href="/notes/r0-75f.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 16/16、Ruby 20/20、23 unique tags、23/23 displays、3 个 hash seeds 与 regeneration 字节稳定，双方 43/43 mutations rejected，unknown mutations fail closed。closed two-mode fixture 从 i ell b g 独立得到 transport；Fejer family 只否定 positivity-only comparison，不是 frozen-collar counterexample。本节纯解析，无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 31 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-240">← Step 30：difference-frequency reduction</a> · <a href="#next">genuine dynamic/payment-sensitive estimate 仍 OPEN →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 31 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">E.24 需要真正的新 coercive information</h2><p style="margin:.15rem 0">本站在 R0.75F Step 31 停止。后续命题必须加入 uncertainty、resolvent/hypocoercive、pathwise residence-time 或 payment-sensitive positive Toeplitz estimate；不得把 circular phase substitution 当作新估计，也不得把 Fejer family 误称为 frozen-collar counterexample。complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均未闭合。后续工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 31 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075f"[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.09"', 'data-site-version="2.10"', "home version"),
        ("/i18n-en.js?v=2.09", "/i18n-en.js?v=2.10", "home i18n"),
        ("/site-refresh.js?v=2.09.1", "/site-refresh.js?v=2.10.1", "home refresh"),
        ("<strong>v2.09</strong>网页版本", "<strong>v2.10</strong>网页版本", "home stat version"),
        ("<strong>R0.75E</strong>最新研究节点", "<strong>R0.75F</strong>最新研究节点", "home latest"),
        ("<strong>233</strong>公开研究笔记", "<strong>234</strong>公开研究笔记", "home public count"),
        ("展开 143 篇公开笔记", "展开 144 篇公开笔记", "home route count"),
        ("综述 v2.09 · 2026-09-03", "综述 v2.10 · 2026-09-03", "home footer"),
        ("Research topology · R0.1–R0.75E", "Research topology · R0.1–R0.75F", "home topology"),
        ('href="#r075e">跳到首页 R0.75E 卡片 →', 'href="#r075f">跳到首页 R0.75F 卡片 →', "home jump"),
        ("R0.70A–R0.75E：135 节已公开，104 节完整封存", "R0.70A–R0.75F：136 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75E</span>', '<span class="route-range">R0.69P–R0.75F</span>', "home range"),
        ("<h3>R0.75E：horizontal difference-frequency identity 与 real zero-mode all-payment closure</h3>", "<h3>R0.75F：modal phase-integration identity 与 positivity-only diagonal no-go</h3>", "home route title"),
        ("R0.72R–R0.75E：</span>", "R0.72R–R0.75F：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75E"', 'aria-label="R0.69P–R0.75F"', "home links label"),
        ("全站现有 233 篇公开研究笔记", "全站现有 234 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75F Step 31 证明 direct modal phase integration 只重建既有 off-diagonal energy ledger，并以 exact real Fejer family 排除 positivity-only diagonal comparison。E.24 所需的 dynamic 或 payment-sensitive coercivity 仍待建立。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75F · 2026-09-03 · STEP 31 · MODAL PHASE-INTEGRATION NO-GO</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">exact modal-product identity 把 signed flux 还原为原 energy identity 的 off-diagonal projection；substitution 后只剩 diagonal identity。Fejer family 排除 positivity-only comparison，但不是 E.24 counterexample。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75f.pdf">阅读最新 R0.75F 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">234 篇研究笔记总索引</a><a href="#r075f">查看首页 R0.75F 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75F · 136 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75F Step 31 modal phase-integration no-go</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(
        page,
        r'<p class="tree-current-summary">.*?</p>',
        '<p class="tree-current-summary">Step 31 proves that direct modal phase integration exactly reconstructs the existing off-diagonal ledger and that positivity alone cannot control the localized form by its diagonal average. E.24 and genuinely coercive routes remain open.</p>',
        "home current summary",
    )
    page = replace_once(
        page,
        'passive fallback → exact difference-frequency flux / real zero mode all-payment paid / arbitrary-real cross-mode gate open</p>',
        'difference-frequency flux → exact phase reconstruction / positivity-only diagonal no-go / dynamic coercivity open</p>',
        "home route path",
    )
    page = replace_once(
        page,
        '<a class="milestone" href="/notes/r0-75e.html">R0.75E</a>',
        '<a class="milestone" href="/notes/r0-75e.html">R0.75E</a>\n<a class="milestone" href="/notes/r0-75f.html">R0.75F</a>',
        "home milestone",
    )
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>genuine dynamic/payment-sensitive coercivity for E.24</h3><p>必须加入 uncertainty、resolvent/hypocoercive、pathwise residence-time 或 payment-sensitive positive Toeplitz information；后续工作未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075f" data-release="r075f" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75F Step 31 · 2026-09-03 · MODAL PHASE-INTEGRATION NO-GO</p><h3>{TITLE}</h3><p>direct phase substitution 精确回收原 off-diagonal ledger，不给出新 coercivity；exact real Fejer family 排除 positivity-only comparison，但不是 frozen-collar counterexample。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75f.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75f.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075e"'
    if anchor not in page:
        raise RuntimeError("home R0.75E card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075f-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    for old, new, label in (
        ('data-site-version="2.09"', 'data-site-version="2.10"', "literature version"),
        ("/i18n-en.js?v=2.09", "/i18n-en.js?v=2.10", "literature i18n"),
        ("文献综述 v2.09 · 2026-09-03", "文献综述 v2.10 · 2026-09-03", "literature footer"),
        ("本站 R0.69P–R0.75E 只列为研究笔记", "本站 R0.69P–R0.75F 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · R0.75F</b><strong>arbitrary-real signed cross-mode aggregation</strong></header><p>必须控制 positive signed cross-mode flux，或建立 difference-frequency decay / localized observability；后续材料未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75F</b><strong>modal phase-integration identity and diagonal-control no-go</strong></header><p>Step 31 证明 direct phase substitution 只重建原 off-diagonal energy ledger，并以 exact real Fejer family 排除 positivity-only diagonal comparison；该 family 不是 E.24 counterexample，真正的 dynamic/payment-sensitive routes 仍 OPEN。<a href="/notes/r0-75f.html">研究笔记</a> <a href="#r075f-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>genuine coercive information for E.24</strong></header><p>必须加入 uncertainty、resolvent/hypocoercive、pathwise residence-time 或 payment-sensitive positive Toeplitz estimate；后续材料未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075f-boundary">R0.75F Step 31 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Siming He 支持 nonzero shear modes 的 enhanced decay 需要 resolvent/semigroup information；'
        'Gardner--Liss--Mattingly 的 pathwise 方法加入 trajectory separation 与 local shear information；'
        'Albritton--Dong 支持 physical localization 保留 drift flux 并需要定量 drift/geometric control。'
        '这些来源均不直接给出 frozen spherical-collar Toeplitz form 或 Version-M E.24 payment estimate。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75F Step 31 公开边界</strong><p>'
        'PROVED：modal-product equation；T_xi=E_off-A_off+D_off；substitution 后 E_diag+D_diag=A_diag；'
        'direct phase integration 不增加独立 sign、small factor 或 observability。'
        'FINITE NO-GO：real Fejer family 的 ratio=(2N+N^-1)/3 发散，排除 positivity-only diagonal comparison；'
        'N=3/5/7 的 exact ratios 为 19/9、17/5、33/7。'
        'NOT A COUNTEREXAMPLE：该 family 不是 frozen geometric collar，不否定 E.24。'
        'OPEN：E.24、uncertainty/resolvent/pathwise/payment-sensitive routes、complete clock、fixed deletion、'
        'suitable-weak transfer、regularity 与 singularity。无 formal figure、simulation、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75f.html">阅读完整笔记</a> · '
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
    if html_count != 234 or pdf_count not in (190, 191):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(previous.previous.previous.previous.previous.route_post_r060_slugs(HOME.read_text(encoding="utf-8")))
    if post_r060 != 174:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75f.html",
        "latestPublishedResearchPdf": "/notes/r0-75f.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075e":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 136
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30, "r075f": 31,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "MODAL_PHASE_INTEGRATION_IDENTITY_AND_POSITIVITY_ONLY_DIAGONAL_CONTROL_NO_GO",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_ROUTE_PRUNING",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "modal_product_identity": "PROVED",
            "off_diagonal_phase_reconstruction": "PROVED_EXACT_ZERO_RESIDUAL",
            "diagonal_modal_identity": "UNCHANGED",
            "direct_phase_substitution": "TAUTOLOGICAL_NO_NEW_BOUND",
            "positivity_only_diagonal_comparison": "REFUTED_BY_EXACT_REAL_FEJER_FAMILY",
            "frozen_collar_counterexample": "NOT_CONSTRUCTED",
            "arbitrary_real_E24": "OPEN",
            "dynamic_payment_sensitive_routes": "VIABLE_UNPROVED",
            "complete_clock": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_16_OF_16",
            "independent_ruby": "PASS_20_OF_20",
            "negative_mutations": "PASS_PYTHON_43_OF_43_RUBY_43_OF_43",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75f.html",
            "target_pdf": "/notes/r0-75f.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075f_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 31,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 136,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075g",
        "latestPublishedResearchHtml": "/notes/r0-75f.html",
        "latestPublishedResearchPdf": "/notes/r0-75f.pdf",
        "latestReleaseGate": "tests/r075f-step31-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075f-step31-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075f-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075f-step31-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075f-step31-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075f-step31-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075f-step31-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075f-step31",
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
    write_text(PUBLIC / "notes/r0-75f.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 31,
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
