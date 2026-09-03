#!/usr/bin/env python3
"""Publish frozen R0.74X Step 23 from the verified R0.74W Step 22 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import generate_r074w_step22_release as previous
import import_r074x_step23_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.02"
RELEASE = "r074x"
CODE = "R0.74X"
TITLE = "R0.74X｜三 packet fixed-deletion endpoint obstruction 与 cubic-payment gate"
FIGURE_ID = frozen_import.FIGURE_ID
HANDOFF_COMMIT = frozen_import.HANDOFF_COMMIT
HANDOFF_SHA256 = frozen_import.HANDOFF_SHA256
SOURCE_COMMIT = frozen_import.SOURCE_COMMIT
FIGURE_COMMIT = frozen_import.FIGURE_COMMIT
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
        raise RuntimeError("Step 23 handoff drift")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 23 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074x_three_packet_fixed_deletion_gate_certificate.json").read_text())
    checks = certificate.get("checks", [])
    if certificate.get("verdict") != "PASS" or len(checks) != 31 or not all(row.get("pass") for row in checks):
        raise RuntimeError("Step 23 certificate verdict drift")
    note = (ROOT / "research/r074x_three_packet_fixed_deletion_gate.md").read_text()
    for token in (
        r"\textbf{THREE-PACKET TWO-COORDINATE ENDPOINT OBSTRUCTION: PROVED,}",
        r"\textbf{ACTUAL FIXED-DELETION GATE COUNTEREXAMPLE: NOT PROVED,}",
        r"\textbf{EQUAL-TARGET W-STRIP ROUTE: NO-GO BY CUBIC PAYMENT.}",
        "payment-compatible two-coordinate proposition",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in note:
            raise RuntimeError(f"Step 23 boundary drift: {token}")

    canonical = ROOT / "research/figures/r074x" / FIGURE_ID
    names = sorted(item.name for item in canonical.iterdir() if item.is_file())
    if len(names) != 25 or sum((canonical / name).stat().st_size for name in names) != 3_096_940:
        raise RuntimeError("Step 23 figure inventory drift")
    for name in names:
        expected = sha256(canonical / name)
        for mirror in (ROOT / "figures/r074x" / FIGURE_ID, PUBLIC / "figures/r074x" / FIGURE_ID):
            if sha256(mirror / name) != expected:
                raise RuntimeError(f"Step 23 figure mirror drift: {name}")
    for extension, expected in frozen_import.KEY_FIGURE_HASHES.items():
        suffix = extension.split(".")[-1]
        if sha256(PUBLIC / "assets/r074x" / f"{FIGURE_ID}.{suffix}") != expected:
            raise RuntimeError(f"Step 23 public figure asset drift: {suffix}")
    validation = json.loads((canonical / "validation.json").read_text())
    if validation.get("status") != "PASS" or validation.get("visualQAConfirmed") is not True:
        raise RuntimeError("Step 23 figure validation drift")


def inline_markup(value: str) -> str:
    return previous.inline_markup(value)


def render_step23_sections() -> str:
    source = (ROOT / "research/r074x_step23_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 175
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            heading = re.sub(r"^\d+\.\s*", "", lines[0][3:])
            output.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{inline_markup(heading)}</h2>')
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
    if section_index != 185:
        raise RuntimeError(f"Step 23 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.01"', 'data-site-version="2.02"', "note version")
    page = replace_once(page, '/i18n-en.js?v=2.01', '/i18n-en.js?v=2.02', "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="A frozen exact three-packet family proves a two-coordinate T-star endpoint obstruction, while cubic payment blocks the actual normalized fixed-deletion counterexample">',
        "note metadata",
    )
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74X · STEP 23 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74X · Step 23 · 严格冻结 family</div><h1>{TITLE}</h1><p>三个 exact common-shear packets 在两个 distinct coordinates 上给出相对 T* 的 endpoint divergence；fixed deletion 的删除集先固定，witness times 可以不同。<strong>但 outer cubic payment 的指数严格更大：actual payment-normalized counterexample NOT PROVED，equal-target W-strip route NO-GO。NOT CLAY.</strong></p><div class="labels"><span class="label">TWO COORDINATES</span><span class="label">TIMES MAY DIFFER</span><span class="label">T* OBSTRUCTION PROVED</span><span class="label">ACTUAL GATE NOT PROVED</span><span class="label">CUBIC PAYMENT NO-GO</span><span class="label">WHOLE SHELL OPEN</span><span class="label">NEXT X.52</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74X STEP 23</strong><p>exact three-packet NSE family</p><p>two-coordinate T* obstruction：PROVED</p><p>deletion set fixed first</p><p>witness times：may differ</p><p>actual normalized gate：NOT PROVED</p><p>equal-target W-strip：NO-GO</p><p>whole shell / dissipation：OPEN</p><p>bounded literature non-hit only</p><p>analytic schematic · NOT PDE DATA / DNS</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', "", "remove inherited Step 22 figure")
    figure = f'''<section id="figure"><div class="section-no">F / 冻结期刊级四联图</div><h2>Three-packet endpoint height versus cubic payment</h2><picture><source srcset="/assets/r074x/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074x/{FIGURE_ID}.png" alt="R0.74X analytic schematic showing three packet scales, the different-time fixed-deletion pigeonhole, the strict cubic-payment rate gap, and the proved-not-proved-no-go claim hierarchy"></picture><p><a href="/assets/r074x/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074x/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074x/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074x/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r074x/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074x/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r074x/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074x/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">四个面板只编码 analytic scale index、fixed-deletion quantifier、derived exponent comparison 与 claim hierarchy；没有 sampled trajectories、PDE data、DNS 或 simulation。ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY。</p></section>'''
    insertion = render_step23_sections() + "\n" + figure + "\n<section id=\"reproduce\">"
    page = replace_once(page, '<section id="reproduce">', insertion, "Step 23 sections and figure")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 23 主文、primary/literature audits、双实现证书与 figure archive</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_three_packet_fixed_deletion_gate.md">Step 23 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_three_packet_fixed_deletion_gate_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_three_packet_fixed_deletion_literature_audit.md">bounded literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_three_packet_fixed_deletion_gate_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_three_packet_fixed_deletion_gate_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_three_packet_fixed_deletion_gate_certificate.json">Python certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_three_packet_fixed_deletion_gate_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074x_three_packet_fixed_deletion_gate_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074x_three_packet_fixed_deletion_gate_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074x_three_packet_fixed_deletion_gate_qa.sh">QA script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074x_publication_handoff.md">冻结交接</a></p><p><a href="/notes/r0-74x.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一大里程碑 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">上一 recap PDF</a></p><p class="note">Python：31/31 checks、231 exact cases/assertions；独立 Ruby：5/5 groups、36 assertions；Python/Ruby mutations 24/24 与 25/25 rejected；figure archive 25 files、3,096,940 bytes，deterministic 18/18。证书是 finite exact arithmetic/structure；literature 只是 bounded non-hit，二者都不替代 continuum PDE proof。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 23 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-166">← Step 22：remote adjacent-inward threshold</a> · <a href="#next">下一冻结包尚未发布 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 23 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 等待独立冻结交接</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">payment-compatible two-coordinate construction X.52 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.74X Step 23 停止。当前只证明两个坐标相对 T* 的 endpoint obstruction，并证明 equal-target W-strip route 被 cubic payment 阻断；actual payment-normalized fixed-deletion counterexample、whole-shell clock 与 accumulated dissipation 均未证明。R0.74Y/R0.74Z 与其他未列工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 23 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.01"', 'data-site-version="2.02"', "home version"),
        ('/i18n-en.js?v=2.01', '/i18n-en.js?v=2.02', "home i18n"),
        ('/site-refresh.js?v=2.01.1', '/site-refresh.js?v=2.02.1', "home refresh"),
        ('<strong>v2.01</strong>网页版本', '<strong>v2.02</strong>网页版本', "home stat version"),
        ('<strong>R0.74W</strong>最新研究节点', '<strong>R0.74X</strong>最新研究节点', "home latest"),
        ('<strong>225</strong>公开研究笔记', '<strong>226</strong>公开研究笔记', "home public count"),
        ('展开 135 篇公开笔记', '展开 136 篇公开笔记', "home route count"),
        ('综述 v2.01 · 2026-09-03', '综述 v2.02 · 2026-09-03', "home footer"),
        ('Research topology · R0.1–R0.74W', 'Research topology · R0.1–R0.74X', "home topology"),
        ('href="#r074w">跳到首页 R0.74W 卡片 →', 'href="#r074x">跳到首页 R0.74X 卡片 →', "home jump"),
        ('R0.70A–R0.74W：127 节已公开，101 节完整封存', 'R0.70A–R0.74X：128 节已公开，102 节完整封存', "home accounting"),
        ('<span class="route-range">R0.69P–R0.74W</span>', '<span class="route-range">R0.69P–R0.74X</span>', "home range"),
        ('<h3>R0.74W：remote common-shear threshold 与 frozen-placement obstruction</h3>', '<h3>R0.74X：two-coordinate T* obstruction 与 cubic-payment no-go</h3>', "home route title"),
        ('R0.72R–R0.74W：</span>', 'R0.72R–R0.74X：</span>', "home detail range"),
        ('aria-label="R0.69P–R0.74W"', 'aria-label="R0.69P–R0.74X"', "home links label"),
        ('全站现有 225 篇公开研究笔记', '全站现有 226 篇公开研究笔记', "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74X Step 23 在 frozen exact three-packet family 中证明两个 distinct coordinates 相对 T* 的 endpoint obstruction；fixed deletion 的 witness times 可以不同。但 outer cubic payment 严格压过两个 audited strip rates，actual normalized counterexample NOT PROVED，X.52 仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74X · 2026-09-03 · STEP 23</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">three-packet exact family 给出 two-coordinate T*-normalized endpoint obstruction；不同 witness times 仍通过 fixed-set deletion quantifier。actual payment-normalized counterexample NOT PROVED，equal-target W-strip route NO-GO BY CUBIC PAYMENT。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74x.pdf">阅读最新 R0.74X 研究笔记 →</a><a href="/assets/r074x/{FIGURE_ID}.pdf">Step 23 冻结四联图</a><a href="/recap-r0-61-r0-74s.html">保留的上一重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">226 篇研究笔记总索引</a><a href="#r074x">查看首页 R0.74X 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74X · 128 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>102 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74X Step 23</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 23 proves a two-coordinate endpoint obstruction relative to T* in one frozen exact three-packet family. The fixed deletion set is chosen before the time supremum, so the witnesses may occur at different times. The actual payment-normalized counterexample is NOT PROVED; the equal-target W-strip route is a cubic-payment NO-GO。</p>', "home current summary")
    page = replace_once(page, 'remote relative threshold / frozen-placement all-shell upper false / fixed deletion open</p>', 'remote relative threshold → three-packet two-coordinate T* obstruction / fixed-set different-time pigeonhole / cubic-payment no-go / X.52 open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74w.html">R0.74W</a>', '<a class="milestone" href="/notes/r0-74w.html">R0.74W</a>\n<a class="milestone" href="/notes/r0-74x.html">R0.74X</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74Y FROZEN PACKAGE REQUIRED</span><span class="tree-state current">等待中</span></div><h3>payment-compatible two-coordinate construction X.52</h3><p>当前 actual (P_R^M)^(2/3)-normalized gate counterexample、whole-shell clock 与 accumulated dissipation 均未证明。后续必须先独立冻结；R0.74Y/R0.74Z 与其他未列工作不读取、不公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074x" data-release="r074x" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74X Step 23 · 2026-09-03</p><h3>{TITLE}</h3><p>exact three-packet family 在两个 distinct coordinates 上证明相对 T* 的 endpoint divergence；fixed deletion 的时间可不同。outer cubic payment 的更大指数使两个 W-strip witnesses 相对 actual normalization 趋零，因此 actual gate counterexample NOT PROVED，equal-target route NO-GO。NOT CLAY.</p><p><a href="/notes/r0-74x.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74x.pdf">PDF</a> · <a href="/assets/r074x/{FIGURE_ID}.pdf">冻结四联图</a> · <a href="/recap-r0-61-r0-74s.html">上一大里程碑 recap（保留）</a></p></div>\n'''
    if 'id="r074x" data-release="r074x"' not in page:
        anchor = '          <div class="task-one" id="r074w"'
        if anchor not in page:
            raise RuntimeError("home R0.74W card anchor missing")
        page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.01"', 'data-site-version="2.02"', "literature version"),
        ('/i18n-en.js?v=2.01', '/i18n-en.js?v=2.02', "literature i18n"),
        ('文献综述 v2.01 · 2026-09-03', '文献综述 v2.02 · 2026-09-03', "literature footer"),
        ('本站 R0.69P–R0.74W 只列为研究笔记', '本站 R0.69P–R0.74X 只列为研究笔记', "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74W</b><strong>remote adjacent-inward relative threshold</strong></header><p>Step 22 在 frozen exact common-shear family 中证明 all-winding conditional-bridge threshold；packet 2 导出 weighted endpoint divergence，否定该 placement 的 matching all-shell upper。fixed deletion 仍 OPEN。<a href="/notes/r0-74w.html">研究笔记</a> <a href="#r074w-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74X</b><strong>two-coordinate T* obstruction and cubic-payment no-go</strong></header><p>Step 23 用 three-packet exact family 证明两个 distinct coordinates 相对 T* 的 endpoint obstruction；fixed deletion 的 witness times 可以不同。actual payment-normalized counterexample NOT PROVED，equal-target W-strip route 被 cubic payment 阻断。<a href="/notes/r0-74x.html">研究笔记</a> <a href="#r074x-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 等待冻结包</b><strong>payment-compatible two-coordinate construction X.52</strong></header><p>actual normalized fixed-deletion counterexample、whole-shell clock 与 accumulated dissipation 仍 OPEN；R0.74Y/R0.74Z 与其他未列工作不读取、不公开。</p></div>'
    if '<header><b>R0.74X</b><strong>two-coordinate T* obstruction and cubic-payment no-go</strong>' not in page:
        page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74W</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074x-boundary">R0.74X Step 23 的 bounded literature screen 与主张边界</h3><p>冻结 audit 筛查 exact Navier--Stokes shearing waves、shear-flow passive-scalar pathwise/large-deviation analysis、local kinetic-energy regularity criteria 与 localized Navier--Stokes inequality constructions。未发现 five-part conjunction 的 exact collision；这只是截至 2026-09-03 的 finite primary-source non-hit，不是 novelty、priority、correctness、nonexistence 或 publishability 证据。</p><div class="boundary"><strong>R0.74X Step 23 公开边界</strong><p>PROVED（frozen exact family only）：exact three-packet smooth NSE family；packets 2、3 relative survival；two distinct T*-normalized endpoint divergences；fixed-set different-time pigeonhole；two audited strip integrals are negligible relative to (P_R^M)^(2/3)。FINITE：bounded primary-source screen only。NOT PROVED：actual payment-normalized fixed-deletion counterexample；whole-shell clock upper/lower；accumulated-dissipation enhancement。NO-GO：equal-target W-strip route by exterior cubic payment。OPEN：payment-compatible construction X.52、positive variation、accumulated viscosity、arbitrary-clock extraction、scale contraction、general suitable weak solutions、regularity 与 singularity。四联图是 analytic schematic / derived values，不是 PDE data 或 DNS。<strong>NOT CLAY.</strong> <a href="/notes/r0-74x.html">阅读完整笔记</a>。</p></div>\n'
    anchor = '        <section id="references">'
    if 'id="r074x-boundary"' not in page:
        if anchor not in page:
            raise RuntimeError("literature reference anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def figure_publication_binding() -> dict[str, object]:
    canonical = ROOT / "research/figures/r074x" / FIGURE_ID
    assets = []
    for extension in ("pdf", "png", "svg"):
        target = PUBLIC / "assets/r074x" / f"{FIGURE_ID}.{extension}"
        assets.append({"path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": sha256(target)})
    return {
        "schemaVersion": "r074x-native-figure-publication-binding-v1",
        "release": CODE,
        "figureId": FIGURE_ID,
        "sourcePublicationStatus": "locally-hash-sealed-precommit",
        "publicationStatus": "published-from-frozen-commit",
        "researchSourceCommit": SOURCE_COMMIT,
        "figureArchiveCommit": FIGURE_COMMIT,
        "archiveDirectory": f"public/figures/r074x/{FIGURE_ID}",
        "researchArchiveDirectory": f"research/figures/r074x/{FIGURE_ID}",
        "sourceArchiveDirectory": f"figures/r074x/{FIGURE_ID}",
        "inventory": {"files": 25, "bytes": sum(item.stat().st_size for item in canonical.iterdir() if item.is_file())},
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
        "assets": assets,
        "visibleScopeLabel": "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY",
    }


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 226 or pdf_count not in (182, 183):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.previous.previous.previous.previous.previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    if post_r060 != 166:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74x.html", "latestPublishedResearchPdf": "/notes/r0-74x.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074w":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleaseCount"] = 128
        inventory["formalSealedReleaseCount"] = 102
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalSealedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if RELEASE in inventory["formalFigureExemptReleases"]:
        inventory["formalFigureExemptReleases"].remove(RELEASE)
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22, "r074x": 23}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 23, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "postR070APublishedReleaseCount": 128, "postR070AFormalSealedReleaseCount": 102,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r074y", "latestPublishedResearchHtml": "/notes/r0-74x.html",
        "latestPublishedResearchPdf": "/notes/r0-74x.pdf",
        "latestReleaseGate": "tests/r074x-step23-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074x-step23-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074x-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074x-step23-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074x-step23-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074x-step23-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074x-step23-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074x-step23", "handoffCommit": HANDOFF_COMMIT,
            "sourceCommit": SOURCE_COMMIT, "coreCommit": SOURCE_COMMIT,
            "figureSourceCommit": FIGURE_COMMIT, "formalFigureRequired": True,
            "recapRequired": False,
        },
        "latestFormalFigurePublication": figure_publication_binding(),
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-74x.html", render_note())
    if "--note-only" not in __import__("sys").argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 23,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": False,
        "formalFigure": FIGURE_ID, "figureArchiveFiles": 25,
        "simulation": False, "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
