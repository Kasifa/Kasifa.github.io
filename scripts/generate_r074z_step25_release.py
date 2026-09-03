#!/usr/bin/env python3
"""Publish frozen R0.74Z Step 25 from the verified R0.74Y Step 24 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import generate_r074y_step24_release as previous
import import_r074z_step25_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.04"
RELEASE = "r074z"
CODE = "R0.74Z"
TITLE = "R0.74Z｜远端持续性门：kinetic coercivity、time-tame 条件与 full-clock 开放边界"
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
        raise RuntimeError("Step 25 handoff drift")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 25 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074z_cancellation_cell_gate_certificate.json").read_text())
    checks = certificate.get("checks", {})
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions") != 10
        or len(checks) != 10
        or not all(checks.values())
        or certificate.get("tag_count") != 42
    ):
        raise RuntimeError("Step 25 certificate verdict drift")
    note = (ROOT / "research/r074z_cancellation_cell_gate.md").read_text()
    for token in (
        r"\textbf{TIME-TAME W-KINETIC ESCAPE: CONDITIONALLY BLOCKED;}",
        r"\textbf{FULL-CLOCK Y.57 CANCELLATION CELL: OPEN;}",
        r"\limsup_{L\to\infty}\frac{-\log\theta_L}{L^2}<\kappa_*",
        r"\frac{476239}{1064835072}",
        r"\textbf{NO PAYMENT-COMPATIBLE CELL IS CONSTRUCTED.}",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in note:
            raise RuntimeError(f"Step 25 boundary drift: {token}")

    canonical = ROOT / "research/figures/r074z" / FIGURE_ID
    names = sorted(item.name for item in canonical.iterdir() if item.is_file())
    if len(names) != 25 or sum((canonical / name).stat().st_size for name in names) != 3_032_354:
        raise RuntimeError("Step 25 figure inventory drift")
    for name in names:
        expected = sha256(canonical / name)
        for mirror in (ROOT / "figures/r074z" / FIGURE_ID, PUBLIC / "figures/r074z" / FIGURE_ID):
            if sha256(mirror / name) != expected:
                raise RuntimeError(f"Step 25 figure mirror drift: {name}")
    for filename, expected in frozen_import.KEY_FIGURE_HASHES.items():
        if filename.startswith("figure."):
            suffix = filename.split(".")[-1]
            if sha256(PUBLIC / "assets/r074z" / f"{FIGURE_ID}.{suffix}") != expected:
                raise RuntimeError(f"Step 25 public figure asset drift: {suffix}")
    validation = json.loads((canonical / "validation.json").read_text())
    if validation.get("status") != "PASS" or validation.get("visualQAConfirmed") is not True:
        raise RuntimeError("Step 25 figure validation drift")


def inline_markup(value: str) -> str:
    return previous.inline_markup(value)


def render_step25_sections() -> str:
    source = (ROOT / "research/r074z_step25_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 195
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
    if section_index != 205:
        raise RuntimeError(f"Step 25 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.03"', 'data-site-version="2.04"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.03", "/i18n-en.js?v=2.04", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Exact persistent-tube kinetic coercivity, a conditional time-tame endpoint route, and an open full-clock Y.57 boundary">',
        "note metadata",
    )
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74Z · STEP 25 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74Z · Step 25 · persistence gate</div><h1>{TITLE}</h1><p>remote kinetic floor 若在 (\\theta_LR^3) spacetime tube 上持续，exact two-step fourth-root weights 与 Hölder coercivity 会迫使它自己支付 cubic row。<strong>严格 subcritical persistence route 被阻断；endpoint-to-tube 仅在 time-tame 与 moving-strip all-winding 假设下成立。critical layer、accumulated rows 与 full-clock Y.57 仍 OPEN。NOT CLAY.</strong></p><div class="labels"><span class="label">PERSISTENT TUBE PROVED</span><span class="label">TWO WEIGHT SHIFTS</span><span class="label">STRICT SIDE ONLY</span><span class="label">TIME-TAME CONDITIONAL</span><span class="label">CRITICAL OPEN</span><span class="label">FULL CLOCK OPEN</span><span class="label">ANALYTIC FIGURE</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74Z STEP 25</strong><p>same-b algebra：EXACT</p><p>tube coercivity：PROVED</p><p>strict W-kinetic persistence escape：BLOCKED</p><p>endpoint to R³ tube：CONDITIONAL</p><p>critical kappa layer：OPEN</p><p>complexity rate：NECESSARY ONLY</p><p>accumulated clock rows：OPEN</p><p>full-clock Y.57：OPEN</p><p>cancellation cell：NOT CONSTRUCTED</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    figure = f'''<section id="figure"><div class="section-no">F / 冻结期刊级四联图</div><h2>Remote persistence gate: kinetic coercivity versus the full clock</h2><picture><source srcset="/assets/r074z/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074z/{FIGURE_ID}.png" alt="R0.74Z analytic schematic showing the exact remote-shell weight ladder, strict persistence threshold, conditional time-tame route, and open full-clock hierarchy"></picture><p><a href="/assets/r074z/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074z/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074z/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074z/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r074z/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074z/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r074z/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074z/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">四个面板只编码 exact weight ladder、derived threshold、conditional implication 与 proved/conditional/open hierarchy。ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | NOT CLAY。</p></section>'''
    insertion = render_step25_sections() + "\n" + figure + '\n<section id="reproduce">'
    page = replace_once(page, '<section id="reproduce">', insertion, "Step 25 sections and figure")
    evidence = f'''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 25 主文、primary/literature audits、双实现证书与 figure archive</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_cancellation_cell_gate.md">Step 25 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_cancellation_cell_gate_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_cancellation_cell_gate_literature_audit.md">bounded literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_cancellation_cell_gate_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_cancellation_cell_gate_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_cancellation_cell_gate_certificate.json">Python certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_cancellation_cell_gate_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074z_cancellation_cell_gate_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074z_cancellation_cell_gate_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074z_cancellation_cell_gate_qa.sh">QA script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074z_publication_handoff.md">冻结交接</a></p><p><a href="/notes/r0-74z.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一大里程碑 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">上一 recap PDF</a></p><p class="note">Python：10/10 checks；独立 Ruby：11/11 assertions；Python/Ruby mutations 22/22 与 23/23 rejected；seeds 0/1/42 byte-identical。figure archive 25 files、3,032,354 bytes，deterministic 18/18；证书与图档都保持 critical/full-clock/novelty 边界。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 25 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-186">← Step 24：frozen self-payment no-go 与 formal window</a> · <a href="#next">critical/full-clock dichotomy 仍待证明 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 25 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.75A 等待冻结包</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Z.39 remote persistence/payment dichotomy 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.74Z Step 25 停止。下一步必须控制 critical/shorter temporal concentration、arbitrary ill-conditioned finite cancellations 与 complete clock/payment ledger；endpoint critical layer、full Y.57、whole shell、fixed deletion、regularity 和 singularity 均未证明。R0.75A、R0.75B 与其他未列工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 25 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.03"', 'data-site-version="2.04"', "home version"),
        ("/i18n-en.js?v=2.03", "/i18n-en.js?v=2.04", "home i18n"),
        ("/site-refresh.js?v=2.03.1", "/site-refresh.js?v=2.04.1", "home refresh"),
        ("<strong>v2.03</strong>网页版本", "<strong>v2.04</strong>网页版本", "home stat version"),
        ("<strong>R0.74Y</strong>最新研究节点", "<strong>R0.74Z</strong>最新研究节点", "home latest"),
        ("<strong>227</strong>公开研究笔记", "<strong>228</strong>公开研究笔记", "home public count"),
        ("展开 137 篇公开笔记", "展开 138 篇公开笔记", "home route count"),
        ("综述 v2.03 · 2026-09-03", "综述 v2.04 · 2026-09-03", "home footer"),
        ("Research topology · R0.1–R0.74Y", "Research topology · R0.1–R0.74Z", "home topology"),
        ('href="#r074y">跳到首页 R0.74Y 卡片 →', 'href="#r074z">跳到首页 R0.74Z 卡片 →', "home jump"),
        ("R0.70A–R0.74Y：129 节已公开，102 节完整封存", "R0.70A–R0.74Z：130 节已公开，103 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.74Y</span>', '<span class="route-range">R0.69P–R0.74Z</span>', "home range"),
        ("<h3>R0.74Y：frozen self-payment no-go 与 formal cancellation window</h3>", "<h3>R0.74Z：remote persistence gate 与 full-clock open boundary</h3>", "home route title"),
        ("R0.72R–R0.74Y：</span>", "R0.72R–R0.74Z：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.74Y"', 'aria-label="R0.69P–R0.74Z"', "home links label"),
        ("全站现有 227 篇公开研究笔记", "全站现有 228 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74Z Step 25 证明 persistent remote tube 的 exact kinetic coercivity，并在 strict subcritical residence rate 下阻断 W-kinetic payment escape。endpoint-to-tube 仅在 time-tame 与 moving-strip all-winding 假设下成立；critical layer、accumulated clock rows 与 full-clock Y.57 仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74Z · 2026-09-03 · STEP 25 · PERSISTENCE GATE</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">persistent remote kinetic floor 在 doubled-radius exterior row 中强制自己的 cubic payment；strict subcritical residence route 被 exact coercivity 关闭。time-tame endpoint upgrade 是 conditional，critical layer、arbitrary ill-conditioned families 与 full-clock Y.57 保持 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74z.pdf">阅读最新 R0.74Z 研究笔记 →</a><a href="/assets/r074z/{FIGURE_ID}.pdf">Step 25 冻结四联图</a><a href="/recap-r0-61-r0-74s.html">保留的上一重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">228 篇研究笔记总索引</a><a href="#r074z">查看首页 R0.74Z 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74Z · 130 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>103 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74Z Step 25 persistence gate</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 25 proves exact shell-tube Hölder coercivity and a strict subcritical persistence threshold for the W-kinetic witness. Endpoint-to-tube persistence remains conditional on the moving-frame envelope and all-winding moving-strip uniformity. The critical layer, accumulated clock rows, and full-clock Y.57 remain open.</p>', "home current summary")
    page = replace_once(page, 'three-packet T* obstruction / cubic-payment no-go → frozen same-packet self-payment no-go / amplitude cancellation / non-adjacent no-go / formal cancellation window / Y.57 open</p>', 'frozen self-payment no-go / formal cancellation window → exact remote-tube coercivity / strict persistence threshold / time-tame conditional / full clock open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74y.html">R0.74Y</a>', '<a class="milestone" href="/notes/r0-74y.html">R0.74Y</a>\n<a class="milestone" href="/notes/r0-74z.html">R0.74Z</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.75A FROZEN PACKAGE REQUIRED</span><span class="tree-state current">等待中</span></div><h3>Z.39：remote endpoint persistence/payment dichotomy</h3><p>必须覆盖 critical/shorter temporal concentration、arbitrary ill-conditioned finite cancellations 与 complete clock/payment ledger。R0.75A、R0.75B 与其他未列工作不读取、不公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074z" data-release="r074z" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74Z Step 25 · 2026-09-03 · PERSISTENCE GATE</p><h3>{TITLE}</h3><p>persistent remote kinetic floor 在 (\\theta_LR^3) tube 上会通过 exact two-step weights 与 Hölder coercivity 支付 cubic row；strict subcritical residence route 被阻断。endpoint-to-tube 只在 time-tame 与 moving-strip assumptions 下成立，critical/full-clock branches 仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-74z.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74z.pdf">PDF</a> · <a href="/assets/r074z/{FIGURE_ID}.pdf">冻结四联图</a> · <a href="/recap-r0-61-r0-74s.html">上一大里程碑 recap（保留）</a></p></div>\n'''
    if 'id="r074z" data-release="r074z"' in page:
        page = replace_pattern(
            page,
            r'          <div class="task-one" id="r074z" data-release="r074z"[\s\S]*?</div>\n',
            card,
            "refresh home R0.74Z card",
        )
    else:
        anchor = '          <div class="task-one" id="r074y"'
        if anchor not in page:
            raise RuntimeError("home R0.74Y card anchor missing")
        page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="2.03"', 'data-site-version="2.04"', "literature version"),
        ("/i18n-en.js?v=2.03", "/i18n-en.js?v=2.04", "literature i18n"),
        ("文献综述 v2.03 · 2026-09-03", "文献综述 v2.04 · 2026-09-03", "literature footer"),
        ("本站 R0.69P–R0.74Y 只列为研究笔记", "本站 R0.69P–R0.74Z 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74W</b><strong>remote adjacent-inward relative threshold</strong></header><p>Step 22 在 frozen exact common-shear family 中证明 all-winding conditional-bridge threshold；fixed deletion 仍 OPEN。<a href="/notes/r0-74w.html">研究笔记</a> <a href="#r074w-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74X</b><strong>two-coordinate T* obstruction and cubic-payment no-go</strong></header><p>Step 23 证明 two-coordinate T* endpoint obstruction；actual normalized counterexample NOT PROVED。<a href="/notes/r0-74x.html">研究笔记</a> <a href="#r074x-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74Y</b><strong>frozen self-payment no-go and formal cancellation window</strong></header><p>Step 24 证明 frozen same-packet self-payment no-go；changed geometry 只有 formal window。<a href="/notes/r0-74y.html">研究笔记</a> <a href="#r074y-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74Z</b><strong>remote persistence gate and full-clock open boundary</strong></header><p>Step 25 证明 persistent remote tube 的 exact kinetic coercivity 与 strict subcritical threshold；endpoint-to-tube 是 conditional，critical layer、accumulated rows 与 full-clock Y.57 仍 OPEN。<a href="/notes/r0-74z.html">研究笔记</a> <a href="#r074z-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 等待冻结包</b><strong>Z.39 persistence/payment dichotomy</strong></header><p>必须控制 critical temporal concentration、ill-conditioned finite cancellation 与 complete ledger；R0.75A、R0.75B 与其他未列工作不读取、不公开。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74W</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074z-boundary">R0.74Z Step 25 的 bounded literature screen 与主张边界</h3><p>冻结 audit 对 heat observability、propagation of smallness、small-time control cost、spectral vanishing 与 exponential-polynomial Remez inequalities 作了 bounded primary-source screen。未发现 common-shear、shrinking-strip、weighted cubic-payment 与 full-clock 六部分 conjunction 的 exact collision；这只是截至 2026-09-03 的 finite non-hit，不证明 novelty、priority、nonexistence、correctness 或 publishability。</p><div class="boundary"><strong>R0.74Z Step 25 公开边界</strong><p>PROVED：finite same-b exact NSE closure；remote clock Gamma^(1/4) 与 doubled-radius payment Gamma^(1/16)；persistent remote tube 的 total-field Hölder coercivity；strict limsup kappa_L&lt;kappa_* W-kinetic no-go。CONDITIONAL：endpoint preservation 加 moving-frame envelope 与 moving-strip all-winding uniformity 推出 R^3 persistence；complexity rate 只是 necessary。OPEN：critical layer、endpoint-only 与 arbitrary exponentially ill-conditioned families、accumulated clock rows、full-clock Y.57、complete payment upper、whole shell、fixed deletion、regularity 与 singularity。四联图是 analytic schematic / derived values，不是 PDE data 或 DNS。<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-74z.html">阅读完整笔记</a>。</p></div>\n'
    anchor = '        <section id="references">'
    if 'id="r074z-boundary"' in page:
        page = replace_pattern(
            page,
            r'<h3 id="r074z-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n?',
            boundary,
            "refresh Step 25 literature boundary",
        )
    else:
        if anchor not in page:
            raise RuntimeError("literature reference anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def figure_publication_binding() -> dict[str, object]:
    canonical = ROOT / "research/figures/r074z" / FIGURE_ID
    assets = []
    for extension in ("pdf", "png", "svg"):
        target = PUBLIC / "assets/r074z" / f"{FIGURE_ID}.{extension}"
        assets.append({"path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": sha256(target)})
    return {
        "schemaVersion": "r074z-native-figure-publication-binding-v1",
        "release": CODE,
        "figureId": FIGURE_ID,
        "sourcePublicationStatus": "locally-hash-sealed-precommit",
        "publicationStatus": "published-from-frozen-commit",
        "researchSourceCommit": SOURCE_COMMIT,
        "figureArchiveCommit": FIGURE_COMMIT,
        "archiveDirectory": f"public/figures/r074z/{FIGURE_ID}",
        "researchArchiveDirectory": f"research/figures/r074z/{FIGURE_ID}",
        "sourceArchiveDirectory": f"figures/r074z/{FIGURE_ID}",
        "inventory": {"files": 25, "bytes": sum(item.stat().st_size for item in canonical.iterdir() if item.is_file())},
        "byteIdentityRequired": True,
        "publicCopiesComplete": True,
        "assets": assets,
        "visibleScopeLabel": "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | NOT CLAY",
    }


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 228 or pdf_count not in (184, 185):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.previous.previous.previous.previous.previous.previous.previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    if post_r060 != 168:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74z.html", "latestPublishedResearchPdf": "/notes/r0-74z.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074y":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleaseCount"] = 130
        inventory["formalSealedReleaseCount"] = 103
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalSealedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    inventory["formalSealedReleaseCount"] = 103
    inventory["formalFigureExemptReleases"] = [row for row in inventory["formalFigureExemptReleases"] if row != RELEASE]
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22, "r074x": 23, "r074y": 24, "r074z": 25}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 25, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "postR070APublishedReleaseCount": 130, "postR070AFormalSealedReleaseCount": 103,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075a", "latestPublishedResearchHtml": "/notes/r0-74z.html",
        "latestPublishedResearchPdf": "/notes/r0-74z.pdf",
        "latestReleaseGate": "tests/r074z-step25-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074z-step25-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074z-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074z-step25-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074z-step25-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074z-step25-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074z-step25-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074z-step25", "handoffCommit": HANDOFF_COMMIT,
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
    write_text(PUBLIC / "notes/r0-74z.html", render_note())
    if "--note-only" not in __import__("sys").argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 25,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": False,
        "formalFigure": FIGURE_ID, "figureArchiveFiles": 25,
        "simulation": False, "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
