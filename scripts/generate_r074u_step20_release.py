#!/usr/bin/env python3
"""Publish frozen R0.74U Step 20 from the verified R0.74T Step 19 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import generate_r074t_step19_release as previous

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.99"
RELEASE = "r074u"
CODE = "R0.74U"
TITLE = "R0.74U｜内禀运动认证驻留尺度，并关闭指数短驻留逃逸"
FIGURE_ID = "fig-r074u-intrinsic-certified-residence"
HANDOFF_COMMIT = "f3031095b7dfa51837df511f5b015bacb34c473b"
HANDOFF_SHA256 = "115620fe742b3321c7d1422743b202ab83886beb4016fd8da45c81142d66a22b"
SOURCE_COMMIT = "735030d9e51068518796a79571ada291c5414a06"
CORE_COMMIT = "d74e7b297928147334136f4c3cb29c5226d66381"
FIGURE_COMMIT = "8b75193df63a962392f89fcf1dbc20a8411334ba"
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


def frozen_ledger() -> list[tuple[str, str]]:
    handoff = ROOT / "research/r074u_publication_handoff.md"
    if sha256(handoff) != HANDOFF_SHA256:
        raise RuntimeError("Step 20 handoff drift")
    rows = re.findall(r"\| `([0-9a-f]{64})` \| `([^`]+)` \|", handoff.read_text())
    if len(rows) != 35:
        raise RuntimeError(f"Step 20 frozen ledger drift: {len(rows)}")
    return rows


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"milestone recap drift: {target.relative_to(ROOT)}")
    for expected, relative in frozen_ledger():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 20 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074u_intrinsic_certified_residence_certificate.json").read_text())
    checks = certificate.get("checks", [])
    if certificate.get("verdict") != "PASS" or len(checks) != 31 or not all(row.get("pass") for row in checks):
        raise RuntimeError("Step 20 certificate verdict drift")
    if sum(row.get("cases", 0) for row in checks if row.get("group") == "finite") != 869:
        raise RuntimeError("Step 20 finite case count drift")
    note = (ROOT / "research/r074u_intrinsic_certified_residence.md").read_text()
    for token in (
        "R074U_STEP20_STATUS_CERTIFIED_RESIDENCE_PROVED",
        "R074U_STEP20_STATUS_K_SUPERLEVEL_LOWER_ONLY",
        "R074U_STEP20_STATUS_MAXIMAL_K_DWELL_OPEN",
        "**NOT CLAY.**",
    ):
        if token not in note:
            raise RuntimeError(f"Step 20 boundary drift: {token}")
    figure = ROOT / "research/figures/r074u" / FIGURE_ID
    names = json.loads((figure / "manifest.json").read_text())["inventory"]["files"]
    if len(names) != 25 or len(set(names)) != 25:
        raise RuntimeError("Step 20 figure inventory drift")
    for name in names:
        expected = sha256(figure / name)
        for mirror in (ROOT / "figures/r074u" / FIGURE_ID, PUBLIC / "figures/r074u" / FIGURE_ID):
            if sha256(mirror / name) != expected:
                raise RuntimeError(f"Step 20 figure mirror drift: {name}")


def inline_markup(value: str) -> str:
    return previous.previous.previous.inline_markup(value)


def render_step20_sections() -> str:
    source = (ROOT / "research/r074u_step20_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 145
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
    if section_index != 155:
        raise RuntimeError(f"Step 20 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="1.98"', 'data-site-version="1.99"', "note version")
    page = replace_once(page, '/i18n-en.js?v=1.98', '/i18n-en.js?v=1.99', "note i18n")
    page = replace_pattern(page, r'<title>.*?</title><meta name="description" content=".*?">', f'<title>{TITLE}</title><meta name="description" content="intrinsic canonical-lobe motion certifies a two-sided geometric residence corridor, but only a lower bound for the completed-clock superlevel set">', "note metadata")
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74U · STEP 20 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74U · Step 20 完整中文版本</div><h1>{TITLE}</h1><p>包中心的 `R^-2` 速度与物理 annulus 的 `L_iR` 余量，认证一个双边 `Theta(L_iR^3)` 几何驻留走廊。<strong>它只向 completed-clock K-superlevel 传递单向包含和下测度界；几何走廊上界绝不转写成完整 K-superlevel 上界。NOT CLAY.</strong></p><div class="labels"><span class="label">PROVED GEOMETRIC CORRIDOR</span><span class="label">K-SUPERLEVEL LOWER ONLY</span><span class="label">EXPONENTIAL ESCAPE CLOSED</span><span class="label">EXACT COMMON-SHEAR</span><span class="label">MAXIMAL K DWELL OPEN</span><span class="label">NOT PDE DATA</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74U STEP 20</strong><p>U.21-U.25：certified corridor two-sided</p><p>U.33：total-field lobe floor</p><p>U.34-U.35：K-superlevel lower only</p><p>U.36-U.41：dwell conflict proved</p><p>U.45：explicit phase constants</p><p>full K-superlevel upper：OPEN</p><p>arbitrary-clock extraction：OPEN</p><p>regularity / singularity：OPEN</p><p>analytic schematic · NOT PDE DATA / DNS</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="figure">', render_step20_sections() + '\n<section id="figure">', "Step 20 insertion")
    figure = f'''<section id="figure"><div class="section-no">F / 期刊级四联图</div><h2>Intrinsic certified residence 与 bounded-payment conflict</h2><picture><source srcset="/assets/r074u/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074u/{FIGURE_ID}.png" alt="R0.74U Step 20 analytic schematic of the certified geometric corridor, its lower-only inclusion in the K superlevel, and the exponential dwell conflict"></picture><p><a href="/assets/r074u/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074u/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074u/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074u/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r074u/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074u/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r074u/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074u/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">Panels A-C 区分 certified geometric corridor 与 full K-superlevel；Panel D 展示 derived analytic logarithmic conflict。ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY。</p></section>'''
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', figure, "Step 20 figure")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 20 主文、审计、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_intrinsic_certified_residence.md">Step 20 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_intrinsic_certified_residence_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_intrinsic_certified_residence_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_intrinsic_residence_literature_audit.md">literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_intrinsic_certified_residence_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_intrinsic_certified_residence_certificate.json">Python 证书 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_intrinsic_certified_residence_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074u_intrinsic_certified_residence_certificate.py">Python 脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074u_intrinsic_certified_residence_certificate_independent.rb">Ruby 独立脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074u_publication_handoff.md">冻结交接清单</a></p><p><a href="/notes/r0-74u.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一大里程碑 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">上一 recap PDF</a></p><p class="note">Python：31/31 checks、869 exact finite cases；独立 Ruby：9/9 groups、1,651 Rational assertions。Python/Ruby 分别拒绝 23/23 与 24/24 intentional mutations；有限证书不替代 continuum PDE proof。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 20 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-136">← Step 19：schedule-invariant dwell coercivity</a> · <a href="#next">下一冻结包尚未发布 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 20 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 等待明确冻结包</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">full K-superlevel upper ledger 仍是开放接口</h2><p style="margin:.15rem 0">本站在 R0.74U Step 20 停止。后续 frozen package 可以研究 off-target endpoint rows、viscous accumulation、cross terms、shear baseline 与 arbitrary-clock lobe extraction；不得把本节认证几何走廊的上界写成完整 K-superlevel 上界，也不得写成 regularity、singularity 或 Clay theorem。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 20 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    replacements = (
        ('data-site-version="1.98"', 'data-site-version="1.99"', "home version"),
        ('/i18n-en.js?v=1.98', '/i18n-en.js?v=1.99', "home i18n"),
        ('/site-refresh.js?v=1.98.1', '/site-refresh.js?v=1.99.1', "home refresh"),
        ('<strong>v1.98</strong>网页版本', '<strong>v1.99</strong>网页版本', "home stat version"),
        ('<strong>R0.74T</strong>最新研究节点', '<strong>R0.74U</strong>最新研究节点', "home latest"),
        ('<strong>222</strong>公开研究笔记', '<strong>223</strong>公开研究笔记', "home public count"),
        ('展开 132 篇公开笔记', '展开 133 篇公开笔记', "home route count"),
        ('综述 v1.98 · 2026-09-03', '综述 v1.99 · 2026-09-03', "home footer"),
        ('Research topology · R0.1–R0.74T', 'Research topology · R0.1–R0.74U', "home topology"),
        ('href="#r074t">跳到首页 R0.74T 卡片 →', 'href="#r074u">跳到首页 R0.74U 卡片 →', "home jump"),
        ('R0.70A–R0.74T：124 节已公开，99 节完整封存', 'R0.70A–R0.74U：125 节已公开，100 节完整封存', "home accounting"),
        ('<span class="route-range">R0.69P–R0.74T</span>', '<span class="route-range">R0.69P–R0.74U</span>', "home range"),
        ('<h3>R0.74T：错峰外叶 Hölder coercivity 与指数 dwell barrier</h3>', '<h3>R0.74U：内禀认证驻留与 full K-superlevel 边界</h3>', "home route title"),
        ('R0.72R–R0.74T：</span>', 'R0.72R–R0.74U：</span>', "home detail range"),
        ('aria-label="R0.69P–R0.74T"', 'aria-label="R0.69P–R0.74U"', "home links label"),
        ('全站现有 222 篇公开研究笔记', '全站现有 223 篇公开研究笔记', "home recap count"),
    )
    for old, new, label in replacements:
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74U Step 20 已证明 canonical common-shear lobe 的认证几何走廊为 Theta(L_iR^3)，并关闭冻结架构中的指数短驻留逃逸；full K-superlevel 仍只有下界，其上测度、arbitrary-clock extraction、Q.12、Q.1 与正则性仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74U · 2026-09-03 · STEP 20</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">intrinsic motion 认证双边 `Theta(L_iR^3)` 几何走廊，并与 bounded-payment 所需指数短 dwell 冲突。completed-clock K-superlevel 只获得下界；几何走廊上界不外推。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74u.pdf">阅读最新 R0.74U 研究笔记 →</a><a href="/assets/r074u/{FIGURE_ID}.pdf">Step 20 期刊级四联图</a><a href="/recap-r0-61-r0-74s.html">保留的上一重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">223 篇研究笔记总索引</a><a href="#r074u">查看首页 R0.74U 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74U · 125 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>100 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74U Step 20</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 20 证明 intrinsic centre motion 与 physical-annulus room 强制双边 Theta(L_iR^3) certified corridor。该 corridor 只下包含于 completed-clock K-superlevel；full K-superlevel upper measure 与 arbitrary-clock extraction 保持 OPEN。</p>', "home current summary")
    page = replace_once(page, 'schedule-invariant lobe coercivity / exponential dwell ceiling / full clock open</p>', 'schedule-invariant lobe coercivity / exponential dwell ceiling → intrinsic certified corridor / K-superlevel lower only / maximal K dwell open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74t.html">R0.74T</a>', '<a class="milestone" href="/notes/r0-74t.html">R0.74T</a>\n<a class="milestone" href="/notes/r0-74u.html">R0.74U</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · FROZEN PACKAGE</span><span class="tree-state current">等待中</span></div><h3>full K-superlevel upper ledger / arbitrary-clock extraction</h3><p>等待同一发布任务中的下一份明确冻结包；可研究 off-target endpoint rows、viscous accumulation、cross terms 与 shear baseline，不得把 certified corridor upper bound 外推为 full K-superlevel upper bound。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074u" data-release="r074u" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74U Step 20 · 2026-09-03</p><h3>{TITLE}</h3><p>包中心速度与物理 annulus 余量认证双边 Theta(L_iR^3) 几何走廊，并关闭冻结 common-shear 架构中的指数短驻留逃逸。completed-clock K-superlevel 只获得 lower measure bound；其 upper measure 仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-74u.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74u.pdf">PDF</a> · <a href="/assets/r074u/{FIGURE_ID}.pdf">期刊级四联图</a> · <a href="/recap-r0-61-r0-74s.html">上一大里程碑 recap（保留）</a></p></div>\n'''
    if 'id="r074u" data-release="r074u"' not in page:
        anchor = '          <div class="task-one" id="r074t"'
        if anchor not in page:
            raise RuntimeError("home R0.74T card anchor missing")
        page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.98"', 'data-site-version="1.99"', "literature version"),
        ('/i18n-en.js?v=1.98', '/i18n-en.js?v=1.99', "literature i18n"),
        ('文献综述 v1.98 · 2026-09-03', '文献综述 v1.99 · 2026-09-03', "literature footer"),
        ('本站 R0.69P–R0.74T 只列为研究笔记', '本站 R0.69P–R0.74U 只列为研究笔记', "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74T</b><strong>schedule-invariant lobe coercivity 与 exponential dwell barrier</strong></header><p>Step 19 证明 outer-lobe kinetic floor 通过经典 Hölder 强制 cubic payment，并在 inherited adjacent-shell window 导出 necessary exponential dwell ceiling。两个 disjoint R³ windows 存在于同一 exact common-shear 解，但只给 K-clock witness；full clock 与 Hfix bridge 仍 OPEN。<a href="/notes/r0-74t.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">上一里程碑 recap</a> <a href="#r074t-boundary">主张边界</a></p></div><div class="route-step kept"><header><b>R0.74U</b><strong>intrinsic certified residence 与 K-superlevel lower-only boundary</strong></header><p>Step 20 证明 canonical lobe 的认证几何走廊具有双边 Theta(L_iR^3) 尺度，并与 bounded-payment 所需指数短 dwell 冲突。该走廊只下包含于 completed-clock K-superlevel；完整超水平集没有 converse 或 upper measure bound。<a href="/notes/r0-74u.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">上一里程碑 recap</a> <a href="#r074u-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 等待冻结包</b><strong>full K-superlevel upper ledger / arbitrary-clock extraction</strong></header><p>可研究 off-target endpoint rows、viscous accumulation、cross terms 与 shear baseline；不得把 certified geometric corridor 的 upper bound 提升成 full K-superlevel upper bound。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74T</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074u-boundary">R0.74U Step 20 的文献近碰撞与主张边界</h3><p>有限一手来源筛查没有找到同时结合 exact unforced common-shear solution、R^-2 centre speed、physical-annulus room、L_iR^3 certified corridor、total-field K-superlevel lower inclusion 与 cubic-payment conflict 的来源。这个 non-hit 不构成 novelty、priority、correctness、nonexistence 或 publishability claim。</p><p><a href="https://doi.org/10.3390/math14091410">Inage（2026）</a>是重要的 terminology-level near collision：其 coherent same-scale Fourier–helical triads 的 low phase-drift set 获得 upper residence-time estimate；R0.74U 则在 physical-space annulus 中追踪 canonical packet lobe，并只向 completed-clock K-superlevel 传递 lower bound。两者的状态变量、shell、假设和估计方向不同，不能互相替代。</p><div class="boundary"><strong>R0.74U Step 20 公开边界</strong><p>PROVED：U.21-U.25 的 certified geometric corridor 双边尺度；U.33 的 total-field lobe floor；U.34-U.35 的 K-superlevel lower-only statement；U.36-U.41 的 certified-dwell conflict；U.45 的 explicit-phase lower constants。FINITE：Python 31/31 checks、869 cases；Ruby 9/9 groups、1,651 assertions；mutation、reproducibility 与 figure QA 全部通过。OPEN：full K-superlevel upper measure、full completed-clock upper ledger、arbitrary-clock extraction、high-Rayleigh / anomalous defect、fixed deletion、direct hybrid、Q.12、Q.1、scale contraction、regularity 与 singularity。图为 analytic schematic / derived analytic values，不是 PDE data 或 DNS。<strong>NOT CLAY.</strong> <a href="/notes/r0-74u.html">阅读完整中文笔记</a>。</p></div>\n'
    if 'id="r074u-boundary"' not in page:
        anchor = '        <section id="references">'
        if anchor not in page:
            raise RuntimeError("literature reference anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 223 or pdf_count not in (179, 180):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.previous.previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    if post_r060 != 163:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74u.html", "latestPublishedResearchPdf": "/notes/r0-74u.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074t":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleaseCount"] = 125
        inventory["formalSealedReleaseCount"] = 100
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalSealedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 20, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "postR070APublishedReleaseCount": 125, "postR070AFormalSealedReleaseCount": 100,
        "nextRelease": "r074v", "latestPublishedResearchHtml": "/notes/r0-74u.html",
        "latestPublishedResearchPdf": "/notes/r0-74u.pdf",
        "latestReleaseGate": "tests/r074u-step20-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074u-step20-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074u-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074u-step20-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074u-step20-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074u-step20-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074u-step20-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074u-step20", "handoffCommit": HANDOFF_COMMIT,
            "sourceCommit": SOURCE_COMMIT, "coreCommit": CORE_COMMIT,
            "figureSourceCommit": FIGURE_COMMIT,
        },
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-74u.html", render_note())
    if "--note-only" not in __import__("sys").argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 20,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": False,
        "formalFigure": FIGURE_ID, "figureArchiveFiles": 25,
        "simulation": False, "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
