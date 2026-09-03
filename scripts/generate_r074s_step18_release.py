#!/usr/bin/env python3
"""Publish frozen R0.74S Step 18 from the already-published Step 17 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import generate_r074s_step17_release as previous

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.97"
RELEASE = "r074s"
CODE = "R0.74S"
TITLE = "R0.74S｜固定删除、同时高度与精确时间量词缺口"
FIGURE_ID = "fig-r074s-fixed-deletion-quantifier-gap"
CORE_COMMIT = "5a9c172e1db8886d49fdf15b8676b4810b002ae3"
FIGURE_SEAL = "963613d54303eb240c1daa40c57ffc106a92535b"
STEP17_RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-74s.html": "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81",
    PUBLIC / "recap-r0-61-r0-74s.pdf": "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec",
}
STEP18_HASHES = {
    "research/r074s_fixed_deletion_certificate.json": "3594d71f53c60e9e2b03c139ac1be79fba9a93c71f11d2cd73a9c85aa30ebe00",
    "research/r074s_fixed_deletion_certificate_report.md": "9fd733deff824fe856c41879d130d753770b0e88fa1d03f90cac67ed29ef4283",
    "research/r074s_fixed_deletion_independent_audit.md": "93ecdb2457d77fb945abe2bd71891c0d115fcaf2c3c8280ddf790ea4944a9324",
    "research/r074s_fixed_deletion_literature_audit.md": "fea7470814c0c21399c6e2b25961e8b3791e584cc24612ac37e9d1be7ce707ce",
    "research/r074s_fixed_deletion_primary_audit.md": "dd9abf2e818ef096aa7fe9e2218b88c55ffb94fa6882a572f85f0f08ed31bab8",
    "research/r074s_fixed_deletion_qa_report.md": "7c53c59053204d3a3e4fce6184ca94b0f5693e37ccaa3d37647c8f5d0ceb2587",
    "research/r074s_fixed_deletion_simultaneous_height.md": "305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1",
    "scripts/r074s_fixed_deletion_certificate.py": "a2700804af8b292b86596b23cd19ccd2d9f2cdde723c95b1ce6d0bfa0d09f035",
    "scripts/r074s_fixed_deletion_certificate_independent.rb": "f21eb45ef39bc4f10211cc1a5852e8b1d22c671a5eab52377ddf867647b4009f",
    "scripts/r074s_fixed_deletion_qa.sh": "d6985c1dbaf843095478044ebfe38d79a641205b500f0cdc738a12ae97b87e5f",
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
    previous.verify_sources()
    previous.assert_recap()
    for target, expected in STEP17_RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"Step 17 milestone recap drift: {target.relative_to(ROOT)}")
    for relative, expected in STEP18_HASHES.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 18 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074s_fixed_deletion_certificate.json").read_text(encoding="utf-8"))
    if certificate.get("schema") != "r074s-fixed-deletion-certificate-v1" or certificate.get("verdict") != "PASS":
        raise RuntimeError("Step 18 certificate schema or verdict drift")
    checks = certificate.get("checks", [])
    if len(checks) != 15 or not all(row.get("pass") for row in checks):
        raise RuntimeError("Step 18 certificate inventory drift")
    if sum(row.get("cases", 0) for row in checks if row.get("group") == "finite") != 283157:
        raise RuntimeError("Step 18 finite case count drift")
    note = (ROOT / "research/r074s_fixed_deletion_simultaneous_height.md").read_text(encoding="utf-8")
    for token in ("Equation (S.486) is **OPEN**", "Equation (S.487) is also **OPEN**", "**ABSTRACT CLOCK STRESS TESTS**", "**NOT CLAY.**"):
        if token not in note:
            raise RuntimeError(f"Step 18 claim boundary drift: {token}")


def render_step18_sections() -> str:
    source = (ROOT / "research/r074s_step18_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 125
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            output.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{previous.inline_markup(lines[0][3:])}</h2>')
            section_open = True
            continue
        if lines[0].startswith("### "):
            output.append(f"<h3>{previous.inline_markup(lines[0][4:])}</h3>")
            continue
        stripped = block.strip()
        if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
            output.append(f'<div class="equation">{html.escape(stripped)}</div>')
            continue
        if all(line.startswith("- ") or line.startswith("  ") for line in lines):
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
            output.append("<ul>" + "".join(f"<li>{previous.inline_markup(item)}</li>" for item in items) + "</ul>")
            continue
        output.append(f"<p>{previous.inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    if section_index != 135:
        raise RuntimeError(f"Step 18 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="1.96"', 'data-site-version="1.97"', "note version")
    page = replace_once(page, '/i18n-en.js?v=1.96', '/i18n-en.js?v=1.97', "note i18n")
    page = replace_pattern(page, r"<title>.*?</title><meta name=\"description\" content=\".*?\">", f'<title>{TITLE}</title><meta name="description" content="fixed deletion 与 completed-clock simultaneous height 在已知 payment 后目标尺度等价；triangular clocks 精确分开 moving、fixed 与 separable 时间量词，S.486–S.487 仍 OPEN">', "note metadata")
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74S · STEP 18 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74S · Step 18 完整中文版本</div><h1>{TITLE}</h1><p>Step 18 精确分开 moving deletion、fixed deletion 与 separable coordinatewise maxima，并证明 fixed hybrid tail 与 completed-clock simultaneous height 在已知 payment 后目标尺度等价。 <strong>S.476–S.485、S.488–S.493 为 PROVED；triangular clocks 仅为 ABSTRACT；S.486、S.487、direct hybrid、S.472、S.407、Q.12、Q.1 与正则性仍 OPEN。NOT CLAY.</strong></p><div class="labels"><span class="label">EXACT QUANTIFIER ORDER</span><span class="label">FIXED DELETION</span><span class="label">SIMULTANEOUS HEIGHT</span><span class="label">ABSTRACT CLOCK TEST</span><span class="label">OPEN S.486 / S.487</span><span class="label">NOT PDE DATA</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74S STEP 18</strong><p>S.476–S.493：PROVED / ABSTRACT / OPEN</p><p>moving deletion ≤ fixed deletion ≤ separable maximum</p><p>fixed hybrid ↔ simultaneous height：target-scale only</p><p>unconditional ledger：linear fallback</p><p>triangular-clock separation：ABSTRACT ONLY</p><p>Taylor recurrence：surviving gates compatible</p><p>S.486 / S.487：OPEN</p><p>direct hybrid / S.472 / S.407：OPEN</p><p>Q.12 / Q.1 / regularity：OPEN</p><p>analytic schematic · NOT PDE DATA / DNS</p></div></div></header><article>'''
    page = replace_pattern(page, r"<body><nav class=\"top\">[\s\S]*?</header><article>", hero, "note hero")
    page = replace_once(page, '<section id="figure">', render_step18_sections() + '\n<section id="figure">', "Step 18 insertion")
    figure = f'''<section id="figure"><div class="section-no">F / 期刊级四联图</div><h2>Fixed-deletion functionals 与 temporal quantifier gap</h2><picture><source srcset="/assets/r074s/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074s/{FIGURE_ID}.png" alt="R0.74S Step 18 four-panel analytic schematic of fixed-deletion functionals and the temporal quantifier gap"></picture><p><a href="/assets/r074s/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074s/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074s/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074s/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r074s/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074s/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r074s/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074s/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">Panel A 是 proved inequalities 与 known-payment links；Panels B–D 是 exact abstract clocks。ANALYTIC SCHEMATIC / ABSTRACT CLOCK TEST / NOT PDE DATA / NOT DNS / NOT CLAY。</p></section>'''
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', figure, "Step 18 figure")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 18 主文、审计、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_fixed_deletion_simultaneous_height.md">fixed-deletion 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_fixed_deletion_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_fixed_deletion_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_fixed_deletion_literature_audit.md">literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_fixed_deletion_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_fixed_deletion_certificate.json">Python 证书 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_fixed_deletion_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074s_fixed_deletion_certificate.py">Python 脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074s_fixed_deletion_certificate_independent.rb">Ruby 独立脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_step18_report-source.md">Step 18 中文 reader source</a></p><p><a href="/notes/r0-74s.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的 Step 17 重大路线修正 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">Step 17 recap PDF</a></p><p class="note">Python：5/5 finite groups、283,157 cases、5/5 structural groups、5/5 hash locks；独立 Ruby：8/8 groups、72,144 assertions。Python/Ruby 分别拒绝 12/12 与 13/13 intentional mutations；有限证书不替代 continuum proof。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 18 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-116">← Step 17：闭流线复现与 absolute-tail no-go</a> · <a href="#next">下一冻结包尚未发布 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 18 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 等待明确冻结包</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">后续接口仍由 OPEN PDE input 决定</h2><p style="margin:.15rem 0">本站在 R0.74S Step 18 停止。后续 frozen package 可以研究 direct hybrid、OPEN S.486 / S.487、OPEN S.472、OPEN S.407 或其他明确 PDE-specific mechanism；不得把 ABSTRACT clocks 当作 PDE 数据，也不得把 Q.12、Q.1、regularity 或 Millennium problem 写成 theorem。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 18 next")


def copy_figures() -> None:
    source = ROOT / "figures/r074s" / FIGURE_ID
    if len([item for item in source.iterdir() if item.is_file()]) != 25:
        raise RuntimeError("Step 18 figure inventory is not exactly 25 files")
    for target in (PUBLIC / "figures/r074s" / FIGURE_ID, ROOT / "research/figures/r074s" / FIGURE_ID):
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
    assets = PUBLIC / "assets/r074s"
    assets.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", assets / f"{FIGURE_ID}.{extension}")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.96"', 'data-site-version="1.97"', "home version"),
        ('/i18n-en.js?v=1.96', '/i18n-en.js?v=1.97', "home i18n"),
        ('/site-refresh.js?v=1.96.1', '/site-refresh.js?v=1.97.1', "home refresh"),
        ('<strong>v1.96</strong>网页版本', '<strong>v1.97</strong>网页版本', "home stat version"),
        ('综述 v1.96 · 2026-09-03', '综述 v1.97 · 2026-09-03', "home footer"),
        ('<h3>R0.74S：闭流线复现与绝对时间尾 no-go</h3>', '<h3>R0.74S：fixed deletion、simultaneous height 与时间量词缺口</h3>', "home route title"),
        ('<p class="tree-current-summary">同一 Taylor 光滑精确解的闭轨道复现使 absolute variation 与 complete payment 同为 A³，因此 S.444 及全部 beta&lt;1 power-only tails 为 FALSE；signed excursion 仍为 A²，S.472、direct hybrid 与 S.407 仍 OPEN。NOT CLAY。</p>', '<p class="tree-current-summary">Step 18 精确分开 moving、fixed 与 separable deletion order，并证明 fixed hybrid 与 simultaneous height 只在已知 payment 后目标尺度等价。S.486、S.487、direct hybrid、S.472 与 S.407 仍 OPEN。NOT CLAY。</p>', "home route summary"),
        ('absolute variation A³ / signed excursion A² → S.444 false → S.472 / direct hybrid / S.407 open</p>', 'absolute variation A³ / signed excursion A² → S.444 false → moving/fixed/separable quantifier split → fixed hybrid ↔ simultaneous height at target scale → S.486 / S.487 / direct hybrid / S.407 open</p>', "home route path"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74S Step 18 已锁定 exact temporal quantifier hierarchy：moving deletion ≤ fixed deletion ≤ separable excursion；fixed hybrid 与 completed-clock simultaneous height 在已知 payment 后目标尺度等价。S.486、S.487、direct hybrid、S.472、S.407、Q.12、Q.1 与正则性仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74S · 2026-09-03 · STEP 18</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">moving deletion、fixed deletion 与 separable maxima 的量词层级被精确分开；fixed hybrid 与 completed-clock simultaneous height 在已知 payment 后目标尺度等价。abstract clocks 只排除纯 ledger 推导，S.486–S.487 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74s.pdf">阅读最新 R0.74S 研究笔记 →</a><a href="/assets/r074s/{FIGURE_ID}.pdf">Step 18 期刊级四联图</a><a href="/recap-r0-61-r0-74s.html">保留的重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">221 篇研究笔记总索引</a><a href="#r074s">查看首页 R0.74S 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74S · 123 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>98 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74S Step 18</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home latest spotlight")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · FROZEN PACKAGE</span><span class="tree-state current">等待中</span></div><h3>下一 PDE-specific interface</h3><p>等待同一发布任务中的下一份明确冻结包；可研究 direct hybrid、OPEN S.486 / S.487、OPEN S.472、OPEN S.407 或其他明确 PDE input，不得把 ABSTRACT clocks 当作 PDE 数据。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074s" data-release="r074s" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74S Step 18 · 2026-09-03</p><h3>{TITLE}</h3><p>精确层级为 moving deletion ≤ fixed deletion ≤ separable excursion；fixed hybrid 与 simultaneous height 在已知 payment 后目标尺度等价。triangular clocks 仅为 ABSTRACT；S.486、S.487、direct hybrid、S.472、S.407 与 regularity 仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-74s.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74s.pdf">PDF</a> · <a href="/assets/r074s/{FIGURE_ID}.pdf">期刊级四联图</a> · <a href="/recap-r0-61-r0-74s.html">Step 17 里程碑 recap</a></p></div>\n'''
    page = re.sub(r'^[ \t]*<div class="task-one" id="r074s" data-release="r074s"[\s\S]*?</div>\n?', "", page, flags=re.M)
    anchor = '          <div class="task-one" id="r074r"'
    if anchor not in page:
        raise RuntimeError("home R0.74R anchor missing")
    write_text(HOME, page.replace(anchor, card + anchor, 1))


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.96"', 'data-site-version="1.97"', "literature version"),
        ('/i18n-en.js?v=1.96', '/i18n-en.js?v=1.97', "literature i18n"),
        ('文献综述 v1.96 · 2026-09-03', '文献综述 v1.97 · 2026-09-03', "literature footer"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74S</b><strong>fixed deletion、simultaneous height 与精确时间量词缺口</strong></header><p>Step 18 证明 moving deletion ≤ fixed deletion ≤ separable excursion，并在已知 payment 后双向比较 fixed hybrid tail 与 completed-clock simultaneous height。triangular clocks 仅给 ABSTRACT ledger obstruction，不是 PDE counterexample；S.486、S.487 与 direct hybrid 仍 OPEN。<a href="/notes/r0-74s.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">Step 17 里程碑 recap</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 等待冻结包</b><strong>PDE-specific simultaneous incidence / hybrid payment</strong></header><p>可研究 direct hybrid、OPEN S.486 / S.487、OPEN S.472 或 OPEN S.407；不得把 abstract triangular clocks 当作 PDE 数据。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74S</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074s-boundary">R0.74S Step 18 的文献与主张边界</h3><p>有界两轮一手来源检索核对 Dascaliuc–Grujić 的 signed averaged flux、Yang 的 skewed-cylinder maximal functions，以及 Yu 的 finite-chain bad-scale counting 与 signed-work depletion。它们都不提供 S.486 的全部量词：一个 universal finite deletion budget、覆盖全部 common good terminal times 的 fixed shell set、infinite-shell forward stopped increments 与 quadratic payment。有限未命中不构成 novelty、priority 或 exhaustiveness claim。</p><div class="boundary"><strong>R0.74S Step 18 公开边界</strong><p>PROVED：S.476–S.485、S.488–S.493 的 hierarchy、layer cake、target-scale comparison、linear fallback 与 fixed-R Taylor screen。ABSTRACT ONLY：triangular-clock strictness 与 linear-ledger 不能推出 2/3 power；不是 NSE counterexample。FINITE：Python 283,157 cases；independent Ruby 72,144 assertions；mutation 与 reproducibility checks 全部通过。OPEN：S.486、S.487、direct hybrid、S.472、S.407、Q.12、Q.1、scale contraction 与 regularity。图为 analytic schematic / abstract clock test，不是 PDE data 或 DNS。<strong>NOT CLAY.</strong> <a href="/notes/r0-74s.html">阅读完整中文笔记</a>。</p></div>\n'
    page = re.sub(r'<h3 id="r074s-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n?', "", page)
    anchor = '        <section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    write_text(LITERATURE, page.replace(anchor, boundary + anchor, 1))


def update_notes_index() -> None:
    target = PUBLIC / "notes/index.html"
    page = target.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.96"', 'data-site-version="1.97"', "index version"),
        ('/i18n-en.js?v=1.96', '/i18n-en.js?v=1.97', "index i18n"),
        ('/site-refresh.js?v=1.96', '/site-refresh.js?v=1.97', "index refresh"),
        ('研究笔记总索引 · v1.96 · 2026-09-03', '研究笔记总索引 · v1.97 · 2026-09-03', "index footer"),
    ):
        page = replace_once(page, old, new, label)
    entry = f'''          <li class="note-entry" data-note="r0-74s"><article><div class="entry-copy"><p class="note-code">R0.74S · STEP 18</p><h3>{TITLE.removeprefix("R0.74S｜")}</h3></div><nav class="entry-files" aria-label="R0.74S files"><a class="file-link html" href="/notes/r0-74s.html" aria-label="Read R0.74S HTML">HTML</a><a class="file-link pdf" href="/notes/r0-74s.pdf" aria-label="Download R0.74S PDF">PDF</a></nav></article></li>\n'''
    page, count = re.subn(r'\s*<li class="note-entry" data-note="r0-74s">[\s\S]*?</li>\n?', "\n" + entry, page, count=1)
    if count != 1:
        raise RuntimeError("notes index R0.74S entry missing")
    write_text(target, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if (html_count, pdf_count) != (221, 178):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74s.html", "latestPublishedResearchPdf": "/notes/r0-74s.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": CODE,
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("publishedReleaseCount") != 123 or inventory.get("formalSealedReleaseCount") != 98:
        raise RuntimeError("same-release publication accounting drift")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 18, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "nextRelease": "r074t", "latestPublishedResearchHtml": "/notes/r0-74s.html",
        "latestPublishedResearchPdf": "/notes/r0-74s.pdf",
        "latestReleaseGate": "tests/r074s-step18-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074s-step18-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074s-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074s-step18-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074s-step18-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074s-step18-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074s-step18-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074s-step18",
            "sourceCommit": CORE_COMMIT,
            "figureSeal": FIGURE_SEAL,
        },
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-74s.html", render_note())
    if "--note-only" not in sys.argv:
        copy_figures()
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 18,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "formalFigure": FIGURE_ID,
        "figureArchiveFiles": 25, "simulation": False, "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
