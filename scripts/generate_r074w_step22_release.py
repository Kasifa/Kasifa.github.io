#!/usr/bin/env python3
"""Publish frozen R0.74W Step 22 from the verified R0.74V Step 21 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import generate_r074v_step21_release as previous
import import_r074w_step22_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.01"
RELEASE = "r074w"
CODE = "R0.74W"
TITLE = "R0.74W｜远端相邻内壳 common-shear 阈值与加权端点阻断"
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
        raise RuntimeError("Step 22 handoff drift")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 22 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074w_remote_adjacent_inward_comparison_certificate.json").read_text())
    checks = certificate.get("checks", [])
    if certificate.get("verdict") != "PASS" or len(checks) != 33 or not all(row.get("pass") for row in checks):
        raise RuntimeError("Step 22 certificate verdict drift")
    note = (ROOT / "research/r074w_remote_adjacent_inward_comparison.md").read_text()
    for token in (
        "R074W_REMOTE_V0_SCALE_DICHOTOMY",
        "R074W_PACKET2_RELATIVE_SURVIVAL",
        "R074W_PACKET1_ORIGINAL_SCALE_SWEPT",
        "R074W_NOT_CLAY",
        "**NOT CLAY.**",
    ):
        if token not in note:
            raise RuntimeError(f"Step 22 boundary drift: {token}")

    canonical = ROOT / "research/figures/r074w" / FIGURE_ID
    names = sorted(item.name for item in canonical.iterdir() if item.is_file())
    if len(names) != 25 or sum((canonical / name).stat().st_size for name in names) != 3_774_363:
        raise RuntimeError("Step 22 figure inventory drift")
    for name in names:
        expected = sha256(canonical / name)
        for mirror in (ROOT / "figures/r074w" / FIGURE_ID, PUBLIC / "figures/r074w" / FIGURE_ID):
            if sha256(mirror / name) != expected:
                raise RuntimeError(f"Step 22 figure mirror drift: {name}")
    for extension, expected in frozen_import.KEY_FIGURE_HASHES.items():
        suffix = extension.split(".")[-1]
        if sha256(PUBLIC / "assets/r074w" / f"{FIGURE_ID}.{suffix}") != expected:
            raise RuntimeError(f"Step 22 public figure asset drift: {suffix}")
    validation = json.loads((canonical / "validation.json").read_text())
    if validation.get("status") != "PASS" or validation.get("visualQAConfirmed") is not True:
        raise RuntimeError("Step 22 figure validation drift")


def inline_markup(value: str) -> str:
    return previous.inline_markup(value)


def render_step22_sections() -> str:
    source = (ROOT / "research/r074w_step22_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 165
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
    if section_index != 175:
        raise RuntimeError(f"Step 22 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.00"', 'data-site-version="2.01"', "note version")
    page = replace_once(page, '/i18n-en.js?v=2.00', '/i18n-en.js?v=2.01', "note i18n")
    page = replace_pattern(page, r'<title>.*?</title><meta name="description" content=".*?">', f'<title>{TITLE}</title><meta name="description" content="exact all-winding conditional-bridge threshold for remote adjacent-inward common-shear packets, with a frozen-placement endpoint obstruction and fixed deletion open">', "note metadata")
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74W · STEP 22 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74W · Step 22 · 严格冻结 family</div><h1>{TITLE}</h1><p>exact all-winding conditional bridge 给出 remote strip 的 relative survival/sweeping 阈值。<strong>packet 2 强制 adjacent-inward weighted endpoint 发散，否定 frozen placement 的 matching all-shell O(T*) upper；fixed deletion 仍可删去唯一发散坐标，保持 OPEN。NOT CLAY.</strong></p><div class="labels"><span class="label">RELATIVE PROBABILITY</span><span class="label">UNIFORM SLAB</span><span class="label">ALL WINDINGS RETAINED</span><span class="label">PACKET 1 SWEPT</span><span class="label">PACKET 2 SURVIVES</span><span class="label">ALL-SHELL UPPER FALSE</span><span class="label">FIXED DELETION OPEN</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74W STEP 22</strong><p>q(ell)=p²/(4ell)</p><p>rho&lt;q65：uniform survival</p><p>rho&gt;q64：uniform sweeping</p><p>fixed ell strict sides：classified</p><p>critical equality：OPEN</p><p>packet 2 endpoint：diverges</p><p>fixed deletion：OPEN</p><p>bounded literature non-hit only</p><p>analytic schematic · NOT PDE DATA / DNS</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    figure = f'''<section id="figure"><div class="section-no">F / 冻结期刊级四联图</div><h2>Remote adjacent-inward threshold 与 weighted endpoint obstruction</h2><picture><source srcset="/assets/r074w/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074w/{FIGURE_ID}.png" alt="R0.74W analytic schematic showing the remote adjacent-inward shell, logarithmic survival-sweeping threshold, exact all-winding conditional-bridge proof map, and weighted endpoint divergence with fixed deletion open"></picture><p><a href="/assets/r074w/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074w/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074w/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074w/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r074w/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074w/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r074w/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074w/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">四个面板只编码 analytic geometry、exact thresholds、proof dependencies 与 derived leading scale；没有 sampled trajectories、PDE data、DNS 或 finite-L numerical certificate。ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY。</p></section>'''
    insertion = render_step22_sections() + "\n" + figure + "\n<section id=\"reproduce\">"
    page = replace_once(page, '<section id="reproduce">', insertion, "Step 22 sections and figure")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 22 主文、primary/literature audits、双实现证书与 figure archive</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_remote_adjacent_inward_comparison.md">Step 22 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_remote_adjacent_inward_comparison_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_remote_adjacent_inward_literature_audit.md">bounded literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_remote_adjacent_inward_comparison_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_remote_adjacent_inward_comparison_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_remote_adjacent_inward_comparison_certificate.json">Python certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_remote_adjacent_inward_comparison_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074w_remote_adjacent_inward_comparison_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074w_remote_adjacent_inward_comparison_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074w_remote_adjacent_inward_comparison_qa.sh">QA script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074w_publication_handoff.md">冻结交接</a></p><p><a href="/notes/r0-74w.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一大里程碑 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">上一 recap PDF</a></p><p class="note">Python：33/33 checks、33 exact cases；独立 Ruby：6/6 groups、56 assertions；Python/Ruby mutations 23/23 与 24/24 rejected；figure archive 25 files、3,774,363 bytes，deterministic 18/18。证书是 finite exact arithmetic/structure；literature 只是 bounded non-hit，二者都不替代 continuum PDE proof。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 22 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-156">← Step 21：completed-clock upper route memo</a> · <a href="#next">下一冻结包尚未发布 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 22 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 等待独立冻结交接</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">fixed deletion 与 whole-shell occupation 仍是开放接口</h2><p style="margin:.15rem 0">本站在 R0.74W Step 22 停止。当前结论只否定 frozen placement 的 matching all-shell upper；唯一发散坐标 k2-1=k1 可被 fixed deletion 删除。未提交的 R0.74X/R0.74Y 未读取、未公开；后续只有收到独立冻结交接后才进入发布链。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 22 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.00"', 'data-site-version="2.01"', "home version"),
        ('/i18n-en.js?v=2.00', '/i18n-en.js?v=2.01', "home i18n"),
        ('/site-refresh.js?v=2.00.1', '/site-refresh.js?v=2.01.1', "home refresh"),
        ('<strong>v2.00</strong>网页版本', '<strong>v2.01</strong>网页版本', "home stat version"),
        ('<strong>R0.74V</strong>最新研究节点', '<strong>R0.74W</strong>最新研究节点', "home latest"),
        ('<strong>224</strong>公开研究笔记', '<strong>225</strong>公开研究笔记', "home public count"),
        ('展开 134 篇公开笔记', '展开 135 篇公开笔记', "home route count"),
        ('综述 v2.00 · 2026-09-03', '综述 v2.01 · 2026-09-03', "home footer"),
        ('Research topology · R0.1–R0.74V', 'Research topology · R0.1–R0.74W', "home topology"),
        ('href="#r074v">跳到首页 R0.74V 卡片 →', 'href="#r074w">跳到首页 R0.74W 卡片 →', "home jump"),
        ('R0.70A–R0.74V：126 节已公开，100 节完整封存', 'R0.70A–R0.74W：127 节已公开，101 节完整封存', "home accounting"),
        ('<span class="route-range">R0.69P–R0.74V</span>', '<span class="route-range">R0.69P–R0.74W</span>', "home range"),
        ('<h3>R0.74V：completed-clock upper 路线备忘录与 occupation gates</h3>', '<h3>R0.74W：remote common-shear threshold 与 frozen-placement obstruction</h3>', "home route title"),
        ('R0.72R–R0.74V：</span>', 'R0.72R–R0.74W：</span>', "home detail range"),
        ('aria-label="R0.69P–R0.74V"', 'aria-label="R0.69P–R0.74W"', "home links label"),
        ('全站现有 224 篇公开研究笔记', '全站现有 225 篇公开研究笔记', "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74W Step 22 证明 frozen common-shear family 的 remote adjacent-inward relative threshold，并由 packet 2 得到 weighted endpoint divergence。matching all-shell upper 对该 placement 为 FALSE；fixed deletion、whole-shell occupation、一般解与 regularity 仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74W · 2026-09-03 · STEP 22</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">exact all-winding bridge 给出 relative survival/sweeping threshold；packet 2 forces adjacent-inward weighted endpoint divergence，否定 frozen placement 的 matching all-shell upper。fixed deletion remains OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74w.pdf">阅读最新 R0.74W 研究笔记 →</a><a href="/assets/r074w/{FIGURE_ID}.pdf">Step 22 冻结四联图</a><a href="/recap-r0-61-r0-74s.html">保留的上一重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">225 篇研究笔记总索引</a><a href="#r074w">查看首页 R0.74W 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74W · 127 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>101 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74W Step 22</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 22 closes the remote adjacent-inward comparison inside the frozen exact family: rates below q65 survive uniformly, rates above q64 sweep uniformly, and fixed limiting ell is classified by strict comparison with q(ell). Equality and fixed deletion remain OPEN。</p>', "home current summary")
    page = replace_once(page, 'completed-clock upper route memo / occupation gates open</p>', 'completed-clock upper route memo → remote relative threshold / frozen-placement all-shell upper false / fixed deletion open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74v.html">R0.74V</a>', '<a class="milestone" href="/notes/r0-74v.html">R0.74V</a>\n<a class="milestone" href="/notes/r0-74w.html">R0.74W</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · FROZEN PACKAGE REQUIRED</span><span class="tree-state current">等待中</span></div><h3>fixed deletion / whole-shell occupation / target-coordinate duration</h3><p>当前不读取或公开未提交的 R0.74X/R0.74Y。后续必须先独立冻结；不得把 one-coordinate endpoint divergence 改写成 fixed-deletion obstruction 或 arbitrary-solution theorem。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074w" data-release="r074w" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74W Step 22 · 2026-09-03</p><h3>{TITLE}</h3><p>exact all-winding bridge comparison 证明 remote strip 的 relative threshold；原始尺度下 packet 1 swept、packet 2 survives，后者导致 adjacent-inward weighted endpoint divergence。matching all-shell upper 对 frozen placement 为 FALSE，但 fixed deletion 仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-74w.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74w.pdf">PDF</a> · <a href="/assets/r074w/{FIGURE_ID}.pdf">冻结四联图</a> · <a href="/recap-r0-61-r0-74s.html">上一大里程碑 recap（保留）</a></p></div>\n'''
    if 'id="r074w" data-release="r074w"' not in page:
        anchor = '          <div class="task-one" id="r074v"'
        if anchor not in page:
            raise RuntimeError("home R0.74V card anchor missing")
        page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = page.replace(
        '<header><b>开放接口 · 等待下一冻结包</b>',
        '<header><b>开放接口 · 等待冻结包</b>',
    )
    for old, new, label in (
        ('data-site-version="2.00"', 'data-site-version="2.01"', "literature version"),
        ('/i18n-en.js?v=2.00', '/i18n-en.js?v=2.01', "literature i18n"),
        ('文献综述 v2.00 · 2026-09-03', '文献综述 v2.01 · 2026-09-03', "literature footer"),
        ('本站 R0.69P–R0.74V 只列为研究笔记', '本站 R0.69P–R0.74W 只列为研究笔记', "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74U</b><strong>intrinsic certified residence 与 K-superlevel lower-only boundary</strong></header><p>Step 20 证明 canonical lobe 的认证几何走廊具有双边 Theta(L_iR^3) 尺度；completed-clock K-superlevel 只获得 lower measure bound。<a href="/notes/r0-74u.html">研究笔记</a> <a href="#r074u-boundary">主张边界</a></p></div><div class="route-step kept"><header><b>R0.74V</b><strong>completed-clock upper route memo</strong></header><p>Step 21 建立 exact completion/splitting、lifted-multiplicity coarse budgets、conditional algebra 和 failure conditions。<a href="/notes/r0-74v.html">路线备忘录</a> <a href="#r074v-boundary">主张边界</a></p></div><div class="route-step kept"><header><b>R0.74W</b><strong>remote adjacent-inward relative threshold</strong></header><p>Step 22 在 frozen exact common-shear family 中证明 all-winding conditional-bridge threshold；packet 2 导出 weighted endpoint divergence，否定该 placement 的 matching all-shell upper。fixed deletion 仍 OPEN。<a href="/notes/r0-74w.html">研究笔记</a> <a href="#r074w-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 等待冻结包</b><strong>fixed deletion / whole-shell occupation / target-coordinate duration</strong></header><p>未提交的 R0.74X/R0.74Y 不读取、不公开；one-coordinate endpoint divergence 不能外推成 fixed-deletion obstruction。</p></div>'
    if '<header><b>R0.74W</b><strong>remote adjacent-inward relative threshold</strong>' not in page:
        page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74T</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074w-boundary">R0.74W Step 22 的 bounded literature screen 与主张边界</h3><p>冻结 audit 筛查了 exact shear waves、enhanced dissipation/hypoellipticity、shear-flow large deviations、random-shear Brownian-bridge functionals 与 Fourier-helical residence-time compression。未发现六项机制完整合取的 exact collision；这只是截至 2026-09-03 的 finite primary-source non-hit，不是 novelty、priority、correctness、nonexistence 或 publishability 证据。</p><div class="boundary"><strong>R0.74W Step 22 公开边界</strong><p>PROVED（frozen exact family only）：all-winding bridge representation；central conditional probability 中的 q(ell)=p²/(4ell) logarithmic rate；uniform slab 的 strict survival/sweeping；amplitude-weighted inversion 与 cross-packet noncancellation；packet-2 adjacent-inward endpoint divergence；matching all-shell O(T*) upper 对 frozen placement 为 FALSE。OPEN：critical equality、fixed deletion、whole-shell/time occupation、positive variation、accumulated viscosity、payment normalization、arbitrary-clock extraction、scale contraction、general suitable weak solutions、regularity 与 singularity。四联图是 analytic schematic / derived values，不是 PDE data 或 DNS。<strong>NOT CLAY.</strong> <a href="/notes/r0-74w.html">阅读完整笔记</a>。</p></div>\n'
    anchor = '        <section id="references">'
    if 'id="r074w-boundary"' not in page:
        if anchor not in page:
            raise RuntimeError("literature reference anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    page = page.replace(
        "matching all-shell O(T*) upper 对 frozen placement 为 FALSE。OPEN：",
        "matching all-shell O(T*) upper 对 frozen placement 为 FALSE。FINITE：bounded primary-source screen 只得到截至 2026-09-03 的 non-hit，不证明 novelty、priority、correctness、nonexistence 或 publishability。OPEN：",
    )
    write_text(LITERATURE, page)


def figure_publication_binding() -> dict[str, object]:
    canonical = ROOT / "research/figures/r074w" / FIGURE_ID
    assets = []
    for extension in ("pdf", "png", "svg"):
        target = PUBLIC / "assets/r074w" / f"{FIGURE_ID}.{extension}"
        assets.append({"path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": sha256(target)})
    return {
        "schemaVersion": "r074w-native-figure-publication-binding-v1",
        "release": CODE,
        "figureId": FIGURE_ID,
        "sourcePublicationStatus": "locally-hash-sealed-precommit",
        "publicationStatus": "published-from-frozen-commit",
        "researchSourceCommit": SOURCE_COMMIT,
        "figureArchiveCommit": FIGURE_COMMIT,
        "archiveDirectory": f"public/figures/r074w/{FIGURE_ID}",
        "researchArchiveDirectory": f"research/figures/r074w/{FIGURE_ID}",
        "sourceArchiveDirectory": f"figures/r074w/{FIGURE_ID}",
        "inventory": {"files": 25, "bytes": sum(item.stat().st_size for item in canonical.iterdir() if item.is_file())},
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
        "assets": assets,
        "visibleScopeLabel": "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY",
    }


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 225 or pdf_count not in (181, 182):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.previous.previous.previous.previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    if post_r060 != 165:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74w.html", "latestPublishedResearchPdf": "/notes/r0-74w.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074v":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleaseCount"] = 127
        inventory["formalSealedReleaseCount"] = 101
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalSealedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if RELEASE in inventory["formalFigureExemptReleases"]:
        inventory["formalFigureExemptReleases"].remove(RELEASE)
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 22, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "postR070APublishedReleaseCount": 127, "postR070AFormalSealedReleaseCount": 101,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r074x", "latestPublishedResearchHtml": "/notes/r0-74w.html",
        "latestPublishedResearchPdf": "/notes/r0-74w.pdf",
        "latestReleaseGate": "tests/r074w-step22-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074w-step22-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074w-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074w-step22-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074w-step22-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074w-step22-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074w-step22-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074w-step22", "handoffCommit": HANDOFF_COMMIT,
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
    write_text(PUBLIC / "notes/r0-74w.html", render_note())
    if "--note-only" not in __import__("sys").argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 22,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": False,
        "formalFigure": FIGURE_ID, "figureArchiveFiles": 25,
        "simulation": False, "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
