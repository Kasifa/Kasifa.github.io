#!/usr/bin/env python3
"""Publish frozen R0.74Y Step 24 from the verified R0.74X Step 23 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import generate_r074x_step23_release as previous
import import_r074y_step24_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.03"
RELEASE = "r074y"
CODE = "R0.74Y"
TITLE = "R0.74Y｜付款兼容的双坐标路线筛选：冻结几何 no-go 与形式取消窗口"
HANDOFF_COMMIT = frozen_import.HANDOFF_COMMIT
HANDOFF_SHA256 = frozen_import.HANDOFF_SHA256
SOURCE_COMMIT = frozen_import.SOURCE_COMMIT
RECAP_HASHES = previous.RECAP_HASHES


def sha256(target: Path) -> str:
    return hashlib.sha256(target.read_bytes()).hexdigest()


def write_text(target: Path, value: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def write_json(target: Path, value: object) -> None:
    write_text(target, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once(value: str, old: str, new: str, label: str) -> str:
    if new in value:
        return value
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def replace_pattern(value: str, pattern: str, replacement: str, label: str) -> str:
    value, count = re.subn(pattern, lambda _: replacement, value, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one pattern occurrence, found {count}")
    return value


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"milestone recap drift: {target.relative_to(ROOT)}")
    handoff = ROOT / frozen_import.HANDOFF_PATH
    if sha256(handoff) != HANDOFF_SHA256:
        raise RuntimeError("Step 24 handoff drift")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 24 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074y_payment_compatible_route_screen_certificate.json").read_text())
    checks = certificate.get("checks", [])
    if (
        certificate.get("verdict") != "PASS"
        or len(checks) != 24
        or sum(row.get("cases", 0) for row in checks) != 244
        or not all(row.get("pass") for row in checks)
    ):
        raise RuntimeError("Step 24 certificate verdict drift")
    note = (ROOT / "research/r074y_payment_compatible_route_screen.md").read_text()
    for token in (
        r"\textbf{FROZEN-GEOMETRY NO-GO PROVED; FORMAL CANCELLATION WINDOW FOUND;}",
        r"\textbf{ACCUMULATED-VISCOSITY BRANCH OPEN; NO CONSTRUCTION THEOREM.}",
        r"\Xi_{\rm fr}(65)",
        r"-\frac{875993}{968647680}<0",
        "This note does not prove (Y.57)",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in note:
            raise RuntimeError(f"Step 24 boundary drift: {token}")


def inline_markup(value: str) -> str:
    return previous.inline_markup(value)


def render_step24_sections() -> str:
    source = (ROOT / "research/r074y_step24_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 185
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
    if section_index != 195:
        raise RuntimeError(f"Step 24 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.02"', 'data-site-version="2.03"', "note version")
    page = replace_once(page, '/i18n-en.js?v=2.02', '/i18n-en.js?v=2.03', "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A frozen-geometry self-payment no-go, a formal necessary exponent window for target-field cancellation, and an open accumulated-viscosity branch">',
        "note metadata",
    )
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74Y · STEP 24 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74Y · Step 24 · route screen</div><h1>{TITLE}</h1><p>冻结 common-shear heat-packet geometry 中，W-type adjacent endpoint 无法击败同一 packet 的 mandatory target-lobe cubic payment；非等振幅与非相邻 placement 均严格失败。<strong>changed geometry 只留下形式必要指数窗口，cancellation cell 与 accumulated-viscosity occupation upper 都未证明。ROUTE SCREEN ONLY. NOT CLAY.</strong></p><div class="labels"><span class="label">ROUTE SCREEN</span><span class="label">FROZEN NO-GO PROVED</span><span class="label">AGES DISTINCT</span><span class="label">AMPLITUDE CANCELS</span><span class="label">CANCELLATION WINDOW FORMAL</span><span class="label">Y.57 NOT PROVED</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74Y STEP 24</strong><p>frozen self-payment no-go：PROVED</p><p>unequal amplitudes alone：NO-GO</p><p>non-adjacent placement：NO-GO</p><p>Xi_fr(65)：strictly negative</p><p>changed geometry：formal necessary only</p><p>field cancellation cell：NOT CONSTRUCTED</p><p>accumulated viscosity：OPEN</p><p>Y.57：NOT PROVED</p><p>bounded literature non-hit only</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', "", "remove inherited Step 23 figure")
    page = replace_once(page, '<section id="reproduce">', render_step24_sections() + '\n<section id="reproduce">', "Step 24 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 24 主文、primary/literature audits、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_payment_compatible_route_screen.md">Step 24 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_payment_compatible_route_screen_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_payment_compatible_route_literature_audit.md">bounded literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_payment_compatible_route_screen_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_payment_compatible_route_screen_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_payment_compatible_route_screen_certificate.json">Python certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_payment_compatible_route_screen_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074y_payment_compatible_route_screen_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074y_payment_compatible_route_screen_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074y_payment_compatible_route_screen_qa.sh">QA script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074y_publication_handoff.md">冻结交接</a></p><p><a href="/notes/r0-74y.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一大里程碑 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">上一 recap PDF</a></p><p class="note">Python：24/24 checks、244 cases；独立 Ruby：21 assertions；Python/Ruby mutations 22/22 与 23/23 rejected；seeds 0/1/42 byte-identical。证书覆盖 finite exact arithmetic、structure、hashes 与 claim boundaries；literature 只是 bounded non-hit，二者都不替代 continuum PDE proof。本 route screen 没有正式科学图、PDE data、DNS 或 simulation。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 24 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-176">← Step 23：two-coordinate T* obstruction 与 cubic-payment gate</a> · <a href="#next">Y.57 仍待构造 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 24 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.74Z 等待冻结包</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Y.57 cancellation-cell proposition 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.74Y Step 24 停止。下一步必须构造同一 common shear 下的 adjacent inversion-paired primaries 与有限 correctors，证明 full target-box cancellation、两个 remote strips 上的 negligibility 和 complete payment upper。R0.74Z、R0.75A 及其他未列工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 24 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.02"', 'data-site-version="2.03"', "home version"),
        ('/i18n-en.js?v=2.02', '/i18n-en.js?v=2.03', "home i18n"),
        ('/site-refresh.js?v=2.02.1', '/site-refresh.js?v=2.03.1', "home refresh"),
        ('<strong>v2.02</strong>网页版本', '<strong>v2.03</strong>网页版本', "home stat version"),
        ('<strong>R0.74X</strong>最新研究节点', '<strong>R0.74Y</strong>最新研究节点', "home latest"),
        ('<strong>226</strong>公开研究笔记', '<strong>227</strong>公开研究笔记', "home public count"),
        ('展开 136 篇公开笔记', '展开 137 篇公开笔记', "home route count"),
        ('综述 v2.02 · 2026-09-03', '综述 v2.03 · 2026-09-03', "home footer"),
        ('Research topology · R0.1–R0.74X', 'Research topology · R0.1–R0.74Y', "home topology"),
        ('href="#r074x">跳到首页 R0.74X 卡片 →', 'href="#r074y">跳到首页 R0.74Y 卡片 →', "home jump"),
        ('R0.70A–R0.74X：128 节已公开，102 节完整封存', 'R0.70A–R0.74Y：129 节已公开，102 节完整封存', "home accounting"),
        ('<span class="route-range">R0.69P–R0.74X</span>', '<span class="route-range">R0.69P–R0.74Y</span>', "home range"),
        ('<h3>R0.74X：two-coordinate T* obstruction 与 cubic-payment no-go</h3>', '<h3>R0.74Y：frozen self-payment no-go 与 formal cancellation window</h3>', "home route title"),
        ('R0.72R–R0.74X：</span>', 'R0.72R–R0.74Y：</span>', "home detail range"),
        ('aria-label="R0.69P–R0.74X"', 'aria-label="R0.69P–R0.74Y"', "home links label"),
        ('全站现有 226 篇公开研究笔记', '全站现有 227 篇公开研究笔记', "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74Y Step 24 证明 frozen geometry 的 same-packet endpoint-versus-self-payment no-go，并排除仅靠 unequal amplitudes 或 non-adjacent dyadic placement 的修复。changed geometry 只有 formal necessary exponent window；Y.57 cancellation cell 与 accumulated-viscosity occupation upper 仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74Y · 2026-09-03 · STEP 24 · ROUTE SCREEN</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">frozen geometry 下，W-type endpoint 不能击败同一 packet 的 mandatory cubic payment；amplitude cancels，non-adjacent placement 更差。changed geometry 只给 formal necessary window，Y.57 与 accumulated-viscosity branch 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74y.pdf">阅读最新 R0.74Y 研究笔记 →</a><a href="/recap-r0-61-r0-74s.html">保留的上一重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">227 篇研究笔记总索引</a><a href="#r074y">查看首页 R0.74Y 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74Y · 129 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>102 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74Y Step 24 route screen</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 24 proves the frozen-geometry same-packet endpoint-versus-self-payment no-go. Unequal amplitudes cancel from the decisive exponent and non-adjacent dyadic placement is worse. A changed geometry has only a formal necessary exponent window; no cancellation cell or accumulated-viscosity occupation theorem is constructed.</p>', "home current summary")
    page = replace_once(page, 'three-packet two-coordinate T* obstruction / fixed-set different-time pigeonhole / cubic-payment no-go / X.52 open</p>', 'three-packet T* obstruction / cubic-payment no-go → frozen same-packet self-payment no-go / amplitude cancellation / non-adjacent no-go / formal cancellation window / Y.57 open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74x.html">R0.74X</a>', '<a class="milestone" href="/notes/r0-74x.html">R0.74X</a>\n<a class="milestone" href="/notes/r0-74y.html">R0.74Y</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74Z FROZEN PACKAGE REQUIRED</span><span class="tree-state current">等待中</span></div><h3>Y.57：same-shear cancellation-cell construction</h3><p>必须构造 full target-box exponential field cancellation，并同时证明 correctors 在两个 remote strips 上可忽略、其自身不会恢复 cubic payment、complete payment upper 闭合。R0.74Z、R0.75A 与其他未列工作不读取、不公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074y" data-release="r074y" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74Y Step 24 · 2026-09-03 · ROUTE SCREEN</p><h3>{TITLE}</h3><p>frozen common-shear heat-packet geometry 中，same-packet W endpoint 无法击败 mandatory target-lobe cubic payment；unequal amplitudes 与 non-adjacent placement 均严格失败。changed geometry 只有 formal necessary window，Y.57 和 accumulated viscosity 仍 OPEN。无正式图、PDE data、DNS 或仿真。NOT CLAY.</p><p><a href="/notes/r0-74y.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74y.pdf">PDF</a> · <a href="/recap-r0-61-r0-74s.html">上一大里程碑 recap（保留）</a></p></div>\n'''
    if 'id="r074y" data-release="r074y"' not in page:
        anchor = '          <div class="task-one" id="r074x"'
        if anchor not in page:
            raise RuntimeError("home R0.74X card anchor missing")
        page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.02"', 'data-site-version="2.03"', "literature version"),
        ('/i18n-en.js?v=2.02', '/i18n-en.js?v=2.03', "literature i18n"),
        ('文献综述 v2.02 · 2026-09-03', '文献综述 v2.03 · 2026-09-03', "literature footer"),
        ('本站 R0.69P–R0.74X 只列为研究笔记', '本站 R0.69P–R0.74Y 只列为研究笔记', "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74W</b><strong>remote adjacent-inward relative threshold</strong></header><p>Step 22 在 frozen exact common-shear family 中证明 all-winding conditional-bridge threshold；packet 2 导出 weighted endpoint divergence，否定该 placement 的 matching all-shell upper。fixed deletion 仍 OPEN。<a href="/notes/r0-74w.html">研究笔记</a> <a href="#r074w-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74X</b><strong>two-coordinate T* obstruction and cubic-payment no-go</strong></header><p>Step 23 用 three-packet exact family 证明两个 distinct coordinates 相对 T* 的 endpoint obstruction；actual payment-normalized counterexample NOT PROVED。<a href="/notes/r0-74x.html">研究笔记</a> <a href="#r074x-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74Y</b><strong>frozen self-payment no-go and formal cancellation window</strong></header><p>Step 24 证明 frozen geometry 的 same-packet endpoint-versus-self-payment no-go；unequal amplitudes 与 non-adjacent placement 不能修复。changed geometry 只有 formal necessary exponent window，Y.57 与 accumulated viscosity 仍 OPEN。<a href="/notes/r0-74y.html">研究笔记</a> <a href="#r074y-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 等待冻结包</b><strong>Y.57 same-shear cancellation cell</strong></header><p>必须构造 full target-box cancellation、remote-strip negligibility 与 complete payment upper；R0.74Z、R0.75A 与其他未列工作不读取、不公开。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74W</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074y-boundary">R0.74Y Step 24 的 bounded literature screen 与主张边界</h3><p>冻结 audit 对 exact Navier--Stokes shearing waves、shear-flow passive-scalar pathwise dissipation、heat observability/control cost、propagation of smallness 与 quantitative unique continuation 作了 bounded primary-source screen。未发现六部分 conjunction 的 exact collision；这只是截至 2026-09-03 的 finite non-hit，不证明 novelty、priority、nonexistence、correctness、sharpness 或 publishability。</p><div class="boundary"><strong>R0.74Y Step 24 公开边界</strong><p>PROVED（frozen geometry only）：same-packet W-type adjacent endpoint 不能击败 mandatory target-lobe cubic payment；deficit age ell 与 heat age ell+1 保持分离；Xi_fr(65)=-875993/968647680&lt;0；unequal amplitudes alone 与 non-adjacent dyadic placement 是 strict no-go。FORMAL NECESSARY ONLY：changed geometry 的 positive rational exponent window，不是 constructed family 或 sufficient feasibility proof。FINITE：certificate 为 exact arithmetic/structure，literature 为 bounded non-hit。OPEN / NOT CERTIFIED：Y.57 cancellation cell、changed-geometry platform、all-winding survival、complete payment upper、accumulated-viscosity H1/occupation upper、whole-shell clock、general suitable weak solutions、regularity 与 singularity。无正式科学图、PDE data、DNS 或 simulation。<strong>ROUTE SCREEN ONLY. NOT CLAY.</strong> <a href="/notes/r0-74y.html">阅读完整笔记</a>。</p></div>\n'
    anchor = '        <section id="references">'
    if 'id="r074y-boundary"' in page:
        page = replace_pattern(
            page,
            r'<h3 id="r074y-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n?',
            boundary,
            "refresh Step 24 literature boundary",
        )
    else:
        if anchor not in page:
            raise RuntimeError("literature reference anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 227 or pdf_count not in (183, 184):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.previous.previous.previous.previous.previous.previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    if post_r060 != 167:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74y.html", "latestPublishedResearchPdf": "/notes/r0-74y.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074x":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleaseCount"] = 129
        inventory["formalSealedReleaseCount"] = 102
        inventory["publishedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    inventory["formalSealedReleaseCount"] = 102
    inventory["formalSealedReleases"] = [row for row in inventory["formalSealedReleases"] if row != RELEASE]
    if RELEASE not in inventory["formalFigureExemptReleases"]:
        inventory["formalFigureExemptReleases"].append(RELEASE)
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 0:
        raise RuntimeError("formal inventory duplicate release")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22, "r074x": 23, "r074y": 24}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 24, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "postR070APublishedReleaseCount": 129, "postR070AFormalSealedReleaseCount": 102,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r074z", "latestPublishedResearchHtml": "/notes/r0-74y.html",
        "latestPublishedResearchPdf": "/notes/r0-74y.pdf",
        "latestReleaseGate": "tests/r074y-step24-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074y-step24-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074y-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074y-step24-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074y-step24-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074y-step24-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074y-step24-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074y-step24", "handoffCommit": HANDOFF_COMMIT,
            "sourceCommit": SOURCE_COMMIT, "coreCommit": SOURCE_COMMIT,
            "formalFigureRequired": False, "recapRequired": False,
        },
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-74y.html", render_note())
    if "--note-only" not in __import__("sys").argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 24,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": False,
        "formalFigure": None, "routeScreen": True, "simulation": False,
        "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
