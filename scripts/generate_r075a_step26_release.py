#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75A Step 26 from the verified R0.74Z Step 25 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r074z_step25_release as previous
import import_r075a_step26_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.05"
RELEASE = "r075a"
CODE = "R0.75A"
TITLE = "R0.75A｜局部持续/付款二分：moving-cutoff 关闭任意短 endpoint focusing"
FIGURE_ID = frozen_import.FIGURE_ID
RECAP_SLUG = "recap-r0-61-r0-75a"
OLD_RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-74s.html": "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81",
    PUBLIC / "recap-r0-61-r0-74s.pdf": "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec",
}


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
    for target, expected in OLD_RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected R0.74S recap drift: {target.relative_to(ROOT)}")
    if sha256(ROOT / frozen_import.HANDOFF_PATH) != frozen_import.HANDOFF_SHA256:
        raise RuntimeError("R0.75A Step 26 handoff drift")
    for relative, expected in {**frozen_import.FROZEN, **frozen_import.RECAP}.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75A frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075a_spectral_persistence_payment_dichotomy_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsPassed") != 14
        or certificate.get("assertionsTotal") != 14
        or certificate.get("exactValues", {}).get("gapA34") != "64279/238140000"
    ):
        raise RuntimeError("R0.75A certificate verdict drift")
    main = (ROOT / "research/r075a_spectral_persistence_payment_dichotomy.md").read_text()
    for token in (
        r"\textbf{W-REMOTE ENDPOINT PERSISTENCE/PAYMENT DICHOTOMY: PROVED}",
        r"\textbf{COMPLETE }K\textbf{, FIXED DELETION, AND REGULARITY: OPEN.}",
        r"R^{2/3}\omega^{-5/6}L^{-1/6}",
        r"\frac{64279}{238140000}>0",
        r"\mathbf{NOT\ CLAY}",
        "R075A_COMPLETE_CLOCK_OPEN",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75A boundary drift: {token}")

    canonical = ROOT / "research/figures/r075a" / FIGURE_ID
    names = sorted(item.name for item in canonical.iterdir() if item.is_file())
    if len(names) != 25 or sum((canonical / name).stat().st_size for name in names) != 2_588_462:
        raise RuntimeError("R0.75A figure inventory drift")
    for name in names:
        expected = sha256(canonical / name)
        for mirror in (ROOT / "figures/r075a" / FIGURE_ID, PUBLIC / "figures/r075a" / FIGURE_ID):
            if sha256(mirror / name) != expected:
                raise RuntimeError(f"R0.75A figure mirror drift: {name}")
    for filename, expected in frozen_import.KEY_FIGURE_HASHES.items():
        if filename.startswith("figure."):
            extension = filename.rsplit(".", 1)[1]
            if sha256(PUBLIC / "assets/r075a" / f"{FIGURE_ID}.{extension}") != expected:
                raise RuntimeError(f"R0.75A public figure asset drift: {extension}")
    validation = json.loads((canonical / "validation.json").read_text())
    if validation.get("status") != "PASS":
        raise RuntimeError("R0.75A figure validation drift")


def inline_markup(value: str) -> str:
    return previous.inline_markup(value)


def render_step26_sections() -> str:
    source = (ROOT / "research/r075a_step26_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 205
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
    if section_index != 215:
        raise RuntimeError(f"Step 26 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.04"', 'data-site-version="2.05"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.04", "/i18n-en.js?v=2.05", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Exact moving-cutoff local persistence/payment dichotomy for the frozen smooth common-shear family; complete clock remains open">',
        "note metadata",
    )
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75A · STEP 26 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75A · Step 26 · local dichotomy</div><h1>{TITLE}</h1><p>对完整总场使用 exact moving-cutoff identity 后，局部质量要么在 cR³ 回看窗中持续，要么快速上升本身强制同一扩大 strip 的 spacetime mass。<strong>两支穷尽并给出 W-remote payment lower；critical 与任意更短光滑 focusing 已覆盖。完整 K、fixed deletion、suitable-weak extension 与 regularity 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">MOVING-CUTOFF EXACT</span><span class="label">TWO CASES EXHAUSTIVE</span><span class="label">W-REMOTE PAYMENT PROVED</span><span class="label">CRITICAL COVERED</span><span class="label">COMPLETE K OPEN</span><span class="label">FIXED DELETION OPEN</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75A STEP 26</strong><p>exact smooth common-shear family</p><p>moving-cutoff identity：PROVED</p><p>persistence / rapid-rise：EXHAUSTIVE</p><p>W-remote endpoint/payment：PROVED</p><p>exact gap：64279/238140000 &gt; 0</p><p>horizontal modal energy：EXACT</p><p>complete clock K：OPEN</p><p>fixed deletion / suitable weak：OPEN</p><p>regularity / singularity：OPEN</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    figure = f'''<section id="figure"><div class="section-no">F / 冻结期刊级四联图</div><h2>Local persistence/payment dichotomy</h2><picture><source srcset="/assets/r075a/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r075a/{FIGURE_ID}.png" alt="R0.75A analytic schematic of the moving strip, exhaustive local-energy branches, payment exponent ledger, and open complete-clock boundary"></picture><p><a href="/assets/r075a/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r075a/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r075a/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r075a/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r075a/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r075a/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r075a/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r075a/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">四个面板编码 exact moving geometry、两个穷尽分支、Hölder/weight/endpoint substitution 与 proved/open hierarchy。ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE SIMULATION | NOT DNS | NO NOVELTY CLAIM | NOT CLAY。</p></section>'''
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', figure, "Step 26 figure")
    insertion = render_step26_sections() + '\n<section id="figure">'
    page = replace_once(page, '<section id="figure">', insertion, "Step 26 sections")
    evidence = f'''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 26 主文、审计、双实现证书、formal figure 与累计回顾</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy.md">Step 26 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_literature_audit.md">bounded literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_route_risk_audit.md">route risk audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_certificate_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_publication_handoff.md">冻结交接</a></p><p><a href="/notes/r0-75a.pdf">同步 reader PDF</a> · <a href="/{RECAP_SLUG}.html">R0.61–R0.75A 累计回顾</a> · <a href="/{RECAP_SLUG}.pdf">累计回顾 PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一里程碑 recap</a></p><p class="note">Certificate：Python 14/14、Ruby 17/17、3 个 hash seed 字节一致、8 个定向 mutation 双实现拒绝。figure archive：25 files、2,588,462 bytes，verify-only 与终尺寸/灰度/PDF visual QA 均 PASS。有限证书与有界文献 non-hit 均不构成 novelty、priority 或连续 PDE proof。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 26 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-196">← Step 25：remote persistence gate</a> · <a href="#next">A.63 remote complete-clock extraction 仍 OPEN →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 26 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.75B 未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">A.63 remote complete-clock extraction 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75A Step 26 停止。后续必须同时控制 endpoint、accumulated 与 off-target clock rows，并避免把 strip lower 写成 whole-shell upper。complete K、fixed deletion、arbitrary suitable weak solutions、contraction、regularity 与 singularity 均未证明。R0.75B、R0.75C、R0.75D 与其他后续工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 26 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.04"', 'data-site-version="2.05"', "home version"),
        ("/i18n-en.js?v=2.04", "/i18n-en.js?v=2.05", "home i18n"),
        ("/site-refresh.js?v=2.04.1", "/site-refresh.js?v=2.05.1", "home refresh"),
        ("<strong>v2.04</strong>网页版本", "<strong>v2.05</strong>网页版本", "home stat version"),
        ("<strong>R0.74Z</strong>最新研究节点", "<strong>R0.75A</strong>最新研究节点", "home latest"),
        ("<strong>228</strong>公开研究笔记", "<strong>229</strong>公开研究笔记", "home public count"),
        ("展开 138 篇公开笔记", "展开 139 篇公开笔记", "home route count"),
        ("综述 v2.04 · 2026-09-03", "综述 v2.05 · 2026-09-03", "home footer"),
        ("Research topology · R0.1–R0.74Z", "Research topology · R0.1–R0.75A", "home topology"),
        ('href="#r074z">跳到首页 R0.74Z 卡片 →', 'href="#r075a">跳到首页 R0.75A 卡片 →', "home jump"),
        ("R0.70A–R0.74Z：130 节已公开，103 节完整封存", "R0.70A–R0.75A：131 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.74Z</span>', '<span class="route-range">R0.69P–R0.75A</span>', "home range"),
        ("<h3>R0.74Z：remote persistence gate 与 full-clock open boundary</h3>", "<h3>R0.75A：moving-cutoff local dichotomy 与 complete-clock open boundary</h3>", "home route title"),
        ("R0.72R–R0.74Z：</span>", "R0.72R–R0.75A：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.74Z"', 'aria-label="R0.69P–R0.75A"', "home links label"),
        ("全站现有 228 篇公开研究笔记", "全站现有 229 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.75A Step 26 已用 exact moving-cutoff identity 关闭 W-remote 正体积 endpoint core 的 critical 与任意短光滑 focusing：persistence 与 rapid-rise 两支都强制 Version-M cubic payment。下一缺口是 A.63 remote complete-clock extraction；complete K、fixed deletion 与 suitable-weak extension 仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75A · 2026-09-03 · STEP 26 · LOCAL DICHOTOMY</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">moving-cutoff exact identity 把 endpoint core 分成 persistence 与 rapid-rise 两支；二者都给出 W-remote exterior payment lower，并统一覆盖 critical 与任意更短光滑 focusing。complete K、fixed deletion 与 suitable-weak extension 保持 OPEN。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75a.pdf">阅读最新 R0.75A 研究笔记 →</a><a href="/assets/r075a/{FIGURE_ID}.pdf">Step 26 冻结四联图</a><a href="/{RECAP_SLUG}.html">最新累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">229 篇研究笔记总索引</a><a href="#r075a">查看首页 R0.75A 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75A · 131 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75A Step 26 local dichotomy</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 26 proves an exact moving-cutoff endpoint persistence/payment dichotomy for the smooth common-shear family. Persistent, critical, and arbitrarily shorter smooth focusing all pay in the W-remote exterior row. Complete-clock extraction, fixed deletion, and suitable-weak extension remain open.</p>', "home current summary")
    page = replace_once(page, 'frozen self-payment no-go / formal cancellation window → exact remote-tube coercivity / strict persistence threshold / time-tame conditional / full clock open</p>', 'remote-tube coercivity / conditional endpoint persistence → exact moving-cutoff dichotomy / critical and shorter focusing closed / complete clock open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74z.html">R0.74Z</a>', '<a class="milestone" href="/notes/r0-74z.html">R0.74Z</a>\n<a class="milestone" href="/notes/r0-75a.html">R0.75A</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.75B NOT AUTHORIZED · A.63</span><span class="tree-state current">OPEN</span></div><h3>remote complete-clock extraction</h3><p>必须同时控制 endpoint、accumulated 与 off-target rows；不得把 strip lower 写成 whole-shell upper。R0.75B/C/D 与后续工作未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075a" data-release="r075a" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75A Step 26 · 2026-09-03 · LOCAL DICHOTOMY</p><h3>{TITLE}</h3><p>exact moving-cutoff identity 使 persistence 与 rapid-rise 两支都产生 W-remote payment lower，覆盖 critical 与任意更短的光滑 endpoint focusing。complete K、fixed deletion、suitable-weak extension 与 regularity 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75a.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75a.pdf">PDF</a> · <a href="/assets/r075a/{FIGURE_ID}.pdf">冻结四联图</a> · <a href="/{RECAP_SLUG}.html">P–A 累计回顾</a></p></div>\n'''
    if 'id="r075a" data-release="r075a"' in page:
        page = replace_pattern(
            page,
            r'          <div class="task-one" id="r075a" data-release="r075a"[\s\S]*?</div>\n',
            card,
            "refresh home R0.75A card",
        )
    else:
        anchor = '          <div class="task-one" id="r074z"'
        if anchor not in page:
            raise RuntimeError("home R0.74Z card anchor missing")
        page = page.replace(anchor, card + anchor, 1)
    recap_card = f'''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计里程碑回顾 R0.61–R0.75A · 2026-09-03</p><h3>R0.60 recap 之后的累计回顾收录 169 个节点；全站现有 229 篇公开研究笔记</h3><p>P–A 把宽泛的 clock-compression 问题压缩为一个已证局部二分和一个明确的 complete-clock extraction 缺口。A 关闭任意短 endpoint focusing，却不控制完整 K。</p><p><strong>当前边界：</strong>W-remote endpoint/payment dichotomy 对精确光滑 common-shear family 已证；A.63、fixed deletion、suitable-weak extension、regularity 与 Clay 仍 OPEN。</p><p><a href="/{RECAP_SLUG}.html"><strong>阅读 R0.61–R0.75A 完整累计回顾 →</strong></a> · <a href="/{RECAP_SLUG}.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留上一版本</a></p></div>'''
    page = replace_pattern(page, r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>', recap_card, "home recap card")
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.04"', 'data-site-version="2.05"', "literature version"),
        ("/i18n-en.js?v=2.04", "/i18n-en.js?v=2.05", "literature i18n"),
        ("文献综述 v2.04 · 2026-09-03", "文献综述 v2.05 · 2026-09-03", "literature footer"),
        ("本站 R0.69P–R0.74Z 只列为研究笔记", "本站 R0.69P–R0.75A 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74W</b><strong>remote adjacent-inward relative threshold</strong></header><p>Step 22 在 frozen exact common-shear family 中证明 all-winding conditional-bridge threshold；fixed deletion 仍 OPEN。<a href="/notes/r0-74w.html">研究笔记</a> <a href="#r074w-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74X</b><strong>two-coordinate T* obstruction and cubic-payment no-go</strong></header><p>Step 23 证明 two-coordinate T* endpoint obstruction；actual normalized counterexample NOT PROVED。<a href="/notes/r0-74x.html">研究笔记</a> <a href="#r074x-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74Y</b><strong>frozen self-payment no-go and formal cancellation window</strong></header><p>Step 24 证明 frozen same-packet self-payment no-go；changed geometry 只有 formal window。<a href="/notes/r0-74y.html">研究笔记</a> <a href="#r074y-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74Z</b><strong>remote persistence gate and full-clock open boundary</strong></header><p>Step 25 证明 persistent remote tube 的 exact kinetic coercivity 与 strict subcritical threshold；endpoint-to-tube 是 conditional。<a href="/notes/r0-74z.html">研究笔记</a> <a href="#r074z-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.75A</b><strong>moving-cutoff endpoint persistence/payment dichotomy</strong></header><p>Step 26 证明 persistence 与 rapid-rise 两支穷尽并强制 W-remote payment，覆盖 critical 与任意短光滑 focusing；complete K 仍 OPEN。<a href="/notes/r0-75a.html">研究笔记</a> <a href="/recap-r0-61-r0-75a.html">P–A recap</a> <a href="#r075a-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · A.63</b><strong>remote complete-clock extraction</strong></header><p>必须控制 endpoint、accumulated 与 off-target rows；R0.75B/C/D 与后续工作未读取、未公开。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74W</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r075a-boundary">R0.75A Step 26 的 bounded literature screen 与主张边界</h3><p>Wang--Wang--Zhang--Zhang（arXiv:1711.04279，§3.2）的 pure-heat inner-endpoint / outer-spacetime nested-cutoff estimate 是最近方法先例。它不包含 residual shear、moving periodic anisotropic strip、shell weight 或 Version-M cubic conversion。七篇一手来源的 bounded non-hit 不证明 novelty、priority、nonexistence、correctness 或 publishability。</p><div class="boundary"><strong>R0.75A Step 26 公开边界</strong><p>PROVED：精确光滑 finite common-shear family；moving-cutoff identity；persistence / rapid-rise exhaustive dichotomy；W-remote endpoint/payment lower；critical 与任意短光滑 focusing；horizontal modal energy。FINITE：Python 14/14、Ruby 17/17、8 个 mutation 双实现拒绝。OPEN：complete K、fixed deletion、whole-shell upper、arbitrary suitable weak extension、contraction、regularity 与 singularity。四联图是 analytic schematic / derived values，不是 PDE simulation 或 DNS。<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75a.html">阅读完整笔记</a> · <a href="/recap-r0-61-r0-75a.html">阅读 P–A recap</a>。</p></div>\n'
    if 'id="r075a-boundary"' in page:
        page = replace_pattern(
            page,
            r'<h3 id="r075a-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n?',
            boundary,
            "refresh Step 26 literature boundary",
        )
    else:
        anchor = '        <section id="references">'
        if anchor not in page:
            raise RuntimeError("literature reference anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def route_post_r060_slugs(page: str) -> list[str]:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    return ordered[ordered.index("r0-61"):]


def render_recap() -> str:
    slugs = route_post_r060_slugs(HOME.read_text(encoding="utf-8"))
    if len(slugs) != 169 or slugs[0] != "r0-61" or slugs[-1] != "r0-75a":
        raise RuntimeError(f"R0.75A recap route coverage drift: {len(slugs)} {slugs[:1]} {slugs[-1:]}")
    links = "\n".join(f'<a href="/notes/{slug}.html">{slug[3:].upper()}</a>' for slug in slugs)
    nodes = [
        ("P", "defect-completed clock", "在不丢失 anomalous dissipation 的前提下定义 suitable-weak clock。", "K=Q+F=E+D≥0；quadratic 与 flux variations 继承付款账本。", "defect-only detection；循环使用 full-dissipation baseline。", "严谨 ledger/compactness，不是 best-N compression。", "exact multipacket stress test。"),
        ("Q", "common-shear multipackets", "以 exact smooth unforced NSE 实现多个坐标。", "有限 same-shear passive packets 与 inversion partners 精确闭合；canonical equal-target family 产生付款。", "naive additivity 与 canonical cheap-payment design。", "constructed-family theorem，不是 universal exclusion；non-hit 不是 novelty。", "arbitrary-clock extraction。"),
        ("R", "arbitrary clocks", "从大 clock 提取 persistent lobe 或 paid branch。", "endpoint averaging、padded persistence、good-time closure 与 conditional lobe extraction；exposed lobe cubically pays。", "用 abstract clock example 代替 PDE extraction。", "uniform arbitrary-suitable-weak extraction 仍 OPEN。", "修正 deletion/time quantifiers。"),
        ("S", "fixed-deletion quantifiers", "排序 terminal time、deletion set 与 shell supremum。", "hybrid、fixed-set simultaneous height 与 coordinatewise excursion 完成排序；known payment 后 fixed hybrid 与 simultaneous height target-scale 等价。", "absolute variation 与 separable coordinatewise maxima。", "functional counterexamples，不是 NSE counterexamples。", "schedule-invariant physical residence。"),
        ("T", "schedule-invariant dwell", "一次 deletion 后处理 asynchronous lobes。", "theta R³ residence 强制 exact exterior cubic payment；两个 nonnegative clocks 给出 N=1 floor。", "以 H_fix 取代 K、反向不等式与未证 target-time shift。", "local coercivity 已证；full-clock extraction OPEN。", "certify actual packet residence。"),
        ("U", "intrinsic residence", "在完整 terminal slab 保持 dominance。", "exact corridor/slab/all-winding estimates 给出 total-field lobe 与 Omega(LR³) certified residence。", "把 corridor occupation 转成 full K-superlevel occupation，或把 Omega 升为 Theta。", "explicit-family lower theorem，不是 maximal-clock upper。", "completed-clock upper ledger。"),
        ("V", "completed-clock upper screen", "控制 explicit-family 每个 clock row。", "exact lifted tiling 与 coarse shear/packet budgets；V.46–V.50 只限定到六对 central-chart。", "all-shell K-upper、arbitrary-k extension、torus cap 与漏记 accumulated dissipation。", "即使在六对有限表域，whole-annulus occupation estimates 仍 OPEN；all-shell upper 也 OPEN。", "adjacent-inward remote comparison。"),
        ("W", "remote adjacent inward", "把 outer packet 向内移动一个 dyadic shell 测试。", "all-winding survival、inversion/cross margins 与 exact endpoint geometry 给出 remote lower witness。", "absolute o(1)、free age、deleted windings 与 whole-shell promotion。", "无 fixed-deletion 或 whole-clock upper theorem。", "three-packet payment gate。"),
        ("X", "three-packet gate", "一次 deletion 后保留两个坐标且保持 cheap payment。", "exact three-packet algebra、四个 cross margins 与两个 endpoint lowers 给出 two-coordinate obstruction。", "把两个 actual-strip uppers 提升为 whole-clock upper。", "payment-normalized fixed-deletion counterexample NOT PROVED。", "payment-compatible cancellation。"),
        ("Y", "route screen", "取消 target 同时保留 remote coordinate。", "exact arithmetic 排除 frozen geometry，并找到 formal changed-geometry exponent window。", "dyadic r≥2 route；把 accumulated-viscosity dimensional screen 当 theorem。", "necessary window，不是 construction；platform、windings、survival 与 H1 occupation 要重证。", "cancellation-cell gate。"),
        ("Z", "cancellation cell", "有限 Gaussian/Hermite/time-offset cells 能否只在 endpoint focusing。", "exact closure、time-tame conditional persistence 与 strict subcritical dwell obstruction，带 positive exact payment gap。", "literal vertical/time translates、qualitative analyticity 充当 quantitative theorem、unconditioned finite-family claims。", "在 Z，critical/ill-conditioned endpoint focusing 与 full Y.57 clock 仍 OPEN；literature 只是 finite non-hit。", "exact moving-cutoff identity。"),
        ("A", "moving-cutoff dichotomy", "任意短 total-field endpoint focusing 能否逃避 W-kinetic payment。", "exact smooth common-shear family 中，persistence 与 rapid-rise 两支穷尽，并得到 \\((P_R^M)^{2/3}\\gtrsim h_{\\rm rem}R^{2/3}\\omega^{-5/6}L^{-1/6}\\)；exact gap \\(64279/238140000>0\\)。", "backward-growing Fourier mode、horizontal band 作为 full generator、global modal energy 自动等于 local payment、此 lemma 必须用 spectral observability。", "只针对 positive-volume endpoint core 与 exact smooth family；无 complete-clock upper、fixed deletion 或 suitable-weak extension。", "A.63 remote complete-clock extraction，控制 endpoint、accumulated、off-target rows，且不把 strip lower 改成 whole-shell upper。"),
    ]
    cards = "\n".join(
        f'''<article class="card node"><p class="eyebrow">{code} / {name}</p><dl><dt>Problem</dt><dd>{problem}</dd><dt>Result</dt><dd>{result}</dd><dt>Rejected</dt><dd>{rejected}</dd><dt>Boundary</dt><dd>{boundary}</dd><dt>Next</dt><dd>{next_step}</dd></dl></article>'''
        for code, name, problem, result, rejected, boundary, next_step in nodes
    )
    return rf'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>R0.61–R0.75A 累计里程碑回顾｜从 clock compression 到 local dichotomy</title>
<meta name="description" content="R0.61 至 R0.75A 的 169 节累计回顾，含 P–A 五字段节点账本、R0.75A moving-cutoff dichotomy、完整审计边界与 A.63 开放接口">
<link rel="canonical" href="https://kasifa.github.io/{RECAP_SLUG}.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\(","\\)"]],displayMath:[["\\[","\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.7 Georgia,"Songti SC","Noto Serif SC",serif}}nav{{padding:12px 5vw;border-top:5px solid var(--ink);border-bottom:3px double var(--ink);display:flex;justify-content:space-between;gap:1rem}}main{{width:min(1040px,90vw);margin:auto}}header{{padding:55px 0 30px;border-bottom:1px solid var(--line)}}h1{{font-size:clamp(2rem,5vw,3.7rem);line-height:1.08}}h2{{color:var(--rule);margin-top:2.4rem}}section{{border-bottom:1px dotted var(--line);padding-bottom:1.2rem}}.eyebrow{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.06em;text-transform:uppercase}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}}.card,.boundary{{background:var(--raised);border:1px solid var(--line);padding:1rem 1.2rem}}.node dl{{display:grid;grid-template-columns:7rem 1fr;gap:.28rem .7rem;margin:0}}.node dt{{font-weight:700;color:var(--rule)}}.node dd{{margin:0}}.node-links{{display:flex;flex-wrap:wrap;gap:.45rem}}.node-links a{{border:1px solid var(--line);padding:.2rem .45rem;text-decoration:none}}a{{color:var(--rule)}}code{{overflow-wrap:anywhere}}@media(max-width:720px){{body{{font-size:15px}}.grid{{grid-template-columns:1fr}}nav{{font-size:13px}}.node dl{{grid-template-columns:1fr}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}nav{{display:none}}body{{font-size:8.5pt}}main{{width:auto}}header{{padding-top:0}}.card{{break-inside:avoid}}}}</style></head>
<body><nav><a href="/research-review.html">研究首页</a><span>R0.61–R0.75A · 2026-09-03</span></nav><main><header><p class="eyebrow">CUMULATIVE MILESTONE RECAP · 169 NODES</p><h1>从 clock compression 到 local persistence/payment dichotomy</h1><p>这是 R0.60 之后的累计里程碑回顾。收录节点：169；回顾截止时公开笔记：229。它保留 R0.74S 与更早 recap 字节不变，在现有路线之后新增 R0.74T–R0.75A 八个节点，并以 P–A 五字段 ledger 固定最新问题、结果、被拒路线、边界和下一步。</p><p><a href="/{RECAP_SLUG}.pdf">下载同步累计回顾 PDF</a> · <a href="/notes/r0-75a.html">阅读 R0.75A Step 26</a> · <a href="/recap-r0-61-r0-74s.html">上一版重大路线修正 recap</a></p></header>
<article><section id="retained"><p class="eyebrow">01 / P–A MILESTONE</p><h2>一个已证局部二分，一个被隔离的 complete-clock 缺口</h2><p>P–A 把宽泛的 clock-compression 问题转成一个 proved local dichotomy 和一个 sharply isolated remaining gap。路线完成 local-energy clock，压力测试 finite deletion 与 exact common-shear multipackets，修正 time/deletion quantifiers，证明 schedule-invariant residence 与 remote adjacent-inward witnesses，并检验 three-packet 与 cancellation-cell routes。R0.75A 最终关闭 W remote kinetic witness 的 arbitrarily short endpoint focusing：localized mass 要么向后持续，要么其 rapid change 强制同一个 exterior cubic payment。下一问题是 complete-clock extraction，不是 spectral persistence。</p><ul><li>projected-Lamb 全局与局部压缩，以及 \(\int_0^\infty\Theta_s^2ds\le\frac12\|u\|_4^4\)。</li><li>归一化热体积 \(\mathcal V\in L_t^1\) 的无条件 Leray 能量估计。</li><li>固定 Parseval 框架上的精确 \(2K^2\) 底边迹代价，以及若干量词明确的光滑 NSE 解族和有限 Fourier 符号对。</li></ul></section>
<section id="timeline"><p class="eyebrow">02 / P–A FIVE-FIELD LEDGER</p><h2>Problem / Result / Rejected / Boundary / Next</h2><div class="grid">{cards}</div></section>
<section id="changed"><p class="eyebrow">03 / WHAT CHANGED AT A</p><h2>critical 与任意短光滑 endpoint focusing 不再是逃逸分支</h2><p>moving-cutoff identity 直接作用于 total field；persistence 与 rapid-rise 两支穷尽并统一给出 W-remote payment lower：</p><p>\((P_R^M)^{{2/3}}\gtrsim h_{{\rm rem}}R^{{2/3}}\omega^{{-5/6}}L^{{-1/6}}\)，且 exact exponent gap 为 \(64279/238140000>0\)。该结论对有限 family size、coefficients、spectral bandwidth 与 temporal conditioning 统一，因为它不逐 packet 分解。它没有给出 whole-shell upper 或 complete-clock upper。</p></section>
<section id="open-next"><p class="eyebrow">04 / OPEN NEXT</p><h2>A.63 remote complete-clock extraction</h2><p>后续必须同时控制 endpoint、accumulated 与 off-target rows，并避免把 strip lower 改写成 whole-shell upper。complete K、fixed deletion、arbitrary suitable weak extension、contraction、regularity 与 singularity 仍 OPEN。R0.75B/C/D 未读取、未发布。</p></section>
<section id="audit"><p class="eyebrow">05 / AUDIT BOX</p><h2>冻结 commits、prose hashes、certificate 与 figure ledger</h2><div class="boundary"><p><strong>Core commit：</strong><code>{frozen_import.SOURCE_COMMIT}</code></p><p><strong>Figure archive commit：</strong><code>{frozen_import.FIGURE_COMMIT}</code></p><p><strong>Recap delta commit：</strong><code>{frozen_import.RECAP_COMMIT}</code></p><p><strong>Main / primary / literature SHA-256：</strong><code>{frozen_import.FROZEN['research/r075a_spectral_persistence_payment_dichotomy.md']}</code> / <code>{frozen_import.FROZEN['research/r075a_spectral_persistence_payment_dichotomy_primary_audit.md']}</code> / <code>{frozen_import.FROZEN['research/r075a_spectral_persistence_payment_dichotomy_literature_audit.md']}</code></p><p><strong>Certificate：</strong>Python 14/14；Ruby 17/17；64 unique tags；3 seeds byte-identical；8 targeted mutations rejected by both implementations。</p><p><strong>Figure：</strong>25 files；2,588,462 bytes；SVG <code>{frozen_import.KEY_FIGURE_HASHES['figure.svg']}</code>；PNG <code>{frozen_import.KEY_FIGURE_HASHES['figure.png']}</code>；PDF <code>{frozen_import.KEY_FIGURE_HASHES['figure.pdf']}</code>。</p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy.md">main</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_literature_audit.md">literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075a_spectral_persistence_payment_dichotomy_certificate.json">certificate JSON</a> · <a href="/figures/r075a/{FIGURE_ID}/manifest.json">figure manifest</a></p><p><strong>Literature boundary：</strong>pure-heat nested cutoff 有明确方法先例；bounded non-hit 不证明 novelty 或 priority。<strong>NOT CLAY.</strong></p></div></section>
<section id="node-index"><p class="eyebrow">NODE INDEX / 169</p><h2>R0.61–R0.75A 全部节点</h2><div class="node-links">{links}</div></section></article></main></body></html>'''


def figure_publication_binding() -> dict[str, object]:
    canonical = ROOT / "research/figures/r075a" / FIGURE_ID
    assets = []
    for extension in ("pdf", "png", "svg"):
        target = PUBLIC / "assets/r075a" / f"{FIGURE_ID}.{extension}"
        assets.append({"path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": sha256(target)})
    return {
        "schemaVersion": "r075a-native-figure-publication-binding-v1",
        "release": CODE,
        "figureId": FIGURE_ID,
        "publicationStatus": "published-from-frozen-commit",
        "researchSourceCommit": frozen_import.SOURCE_COMMIT,
        "figureArchiveCommit": frozen_import.FIGURE_COMMIT,
        "archiveDirectory": f"public/figures/r075a/{FIGURE_ID}",
        "researchArchiveDirectory": f"research/figures/r075a/{FIGURE_ID}",
        "sourceArchiveDirectory": f"figures/r075a/{FIGURE_ID}",
        "inventory": {"files": 25, "bytes": sum(item.stat().st_size for item in canonical.iterdir() if item.is_file())},
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
        "assets": assets,
        "visibleScopeLabel": "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE SIMULATION | NOT DNS | NO NOVELTY CLAIM | NOT CLAY",
    }


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 229 or pdf_count not in (185, 186):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(route_post_r060_slugs(HOME.read_text(encoding="utf-8")))
    if post_r060 != 169:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75a.html", "latestPublishedResearchPdf": "/notes/r0-75a.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169, "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074z":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalSealedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 131
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleases"] = [row for row in inventory["formalFigureExemptReleases"] if row != RELEASE]
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22, "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 26, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 131, "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075b", "latestPublishedResearchHtml": "/notes/r0-75a.html",
        "latestPublishedResearchPdf": "/notes/r0-75a.pdf",
        "latestReleaseGate": "tests/r075a-step26-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075a-step26-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075a-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075a-step26-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075a-step26-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075a-step26-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075a-step26-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075a-step26", "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "sourceCommit": frozen_import.SOURCE_COMMIT, "coreCommit": frozen_import.SOURCE_COMMIT,
            "figureSourceCommit": frozen_import.FIGURE_COMMIT, "recapSourceCommit": frozen_import.RECAP_COMMIT,
            "formalFigureRequired": True, "recapRequired": True,
        },
        "latestFormalFigurePublication": figure_publication_binding(),
        "latestRecapRelease": "r075a", "latestRecapHtml": f"/{RECAP_SLUG}.html",
        "latestRecapPdf": f"/{RECAP_SLUG}.pdf", "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-75a.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        write_text(PUBLIC / f"{RECAP_SLUG}.html", render_recap())
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 26,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": True,
        "recapNodes": 169, "formalFigure": FIGURE_ID, "figureArchiveFiles": 25,
        "figureArchiveBytes": 2_588_462, "simulation": False, "pdeData": False,
        "noveltyClaim": False, "clayClaim": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
