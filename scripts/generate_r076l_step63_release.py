#!/usr/bin/env python3
"""Publish frozen R0.76L Step 63 from the verified R0.76K baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076k_step62_release as previous
import import_r076l_step63_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "77cbb6174b4d757fd8ca579f9a3d570d2135ec77"
VERSION = "2.42"
RELEASE = "r076l"
CODE = "R0.76L"
TITLE = "R0.76L｜抛物边缘平滑、完整时钟余项与 full-plateau 双边界"
RECAP_SLUG = "recap-r0-61-r0-76i"
RECAP_HASHES = {
    PUBLIC / f"{RECAP_SLUG}.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
    PUBLIC / f"{RECAP_SLUG}.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
    PUBLIC / "recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
    PUBLIC / "recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
    PUBLIC / "notes/r0-76j.html": "501371270954bb64dae9db784c6981a945730f346d5db971550f3b9d85505de2",
    PUBLIC / "notes/r0-76j.pdf": "d264c951c9e3e43ab02181ebc4827513a1f6abe0ff37b07bb89ca9d2c6351d87",
    PUBLIC / "notes/r0-76k.html": "d4960ea6616b718a4a9edf217f53cbfc276df9fe0662b107f10bca8bf779042d",
    PUBLIC / "notes/r0-76k.pdf": "b3dce39a5d020a3c2d74133bdfd5c0324e46aefe8b34471b0acb349f90ddc7e1",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
inline_markup = previous.inline_markup


def baseline_text(relative: str) -> str:
    return subprocess.check_output(["git", "show", f"{BASELINE_COMMIT}:{relative}"], cwd=ROOT, text=True)


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected milestone recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.76L frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r076l_parabolic_edge_smoothing_complete_clock_certificate.json").read_text())
    if (certificate.get("verdict") != "PASS"
            or certificate.get("assertionsPassed") != 64 or certificate.get("assertionsTotal") != 64
            or certificate.get("freezeReady") is not True
            or len(certificate.get("negativeMutations", [])) != 25):
        raise RuntimeError("R0.76L certificate verdict drift")
    exact = certificate.get("exact", {})
    if (exact.get("structure") != {"displayCount": 78, "firstTag": 1, "lastTag": 72, "referencesClosed": True, "tagCount": 72, "tagSequenceComplete": True}
            or exact.get("claims", {}).get("completeClockEventuallyPositiveForFamily") is not True
            or exact.get("claims", {}).get("candidateKilledForThisFamily") is not True
            or exact.get("claims", {}).get("bulkA4SaddleTheorem") is not False
            or exact.get("diagnostic", {}).get("knownPreasymptoticAwaySequence") != "degreePower=3/4; metric=unitTiltOverMu; displayedDirection=awayFromLimit"):
        raise RuntimeError("R0.76L exact ledger drift")
    main = (ROOT / "research/r076l_parabolic_edge_smoothing_complete_clock.md").read_text()
    compact = " ".join(main.split())
    for token in (
        r"\tag{L.1}", r"\tag{L.11}", r"\tag{L.13}", r"\tag{L.66}", r"\tag{L.72}",
        r"\sqrt A\ll m=o(A^2)", r"-\frac2{11907}<0", "m=kappa A^4",
        "moves slightly away", "**NOT CLAY.**",
    ):
        if token not in compact:
            raise RuntimeError(f"R0.76L boundary drift: {token}")
    source = (ROOT / "research/r076l_report-source.md").read_text()
    for token in ("DLMF", "Hall", "Kabluchko", "Batahan", "m=kappa A^4", "NOT CLAY"):
        if token not in source:
            raise RuntimeError(f"R0.76L source boundary drift: {token}")
    figure = ROOT / f"research/figures/r076l/{frozen_import.FIGURE_ID}"
    for name in frozen_import.FIGURE_NAMES:
        expected = frozen_import.FROZEN[f"{frozen_import.FIGURE_SOURCE_PREFIX}{name}"]
        if sha256(figure / name) != expected:
            raise RuntimeError(f"R0.76L figure archive drift: {name}")


def render_sections() -> str:
    source = (ROOT / "research/r076l_parabolic_edge_smoothing_complete_clock.md").read_text().strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 496
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
        elif lines[0].startswith("### "):
            output.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
        elif len(lines) >= 2 and lines[0].startswith("|") and re.match(r"^\|[-:| ]+\|$", lines[1]):
            rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
            style = ' style="overflow-wrap:anywhere;word-break:break-word"'
            head = "".join(f"<th{style}>{inline_markup(cell)}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td{style}>{inline_markup(cell)}</td>" for cell in row) + "</tr>" for row in rows[2:])
            output.append(f'<div class="table-wrap"><table style="table-layout:fixed;width:100%"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
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
    if section_index != 507:
        raise RuntimeError(f"Step 63 reader section drift: {section_index}")
    return "\n".join(output).replace(",qquad", r",\;\;").replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.41"', 'data-site-version="2.42"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.41", "/i18n-en.js?v=2.42", "note i18n")
    page = replace_once(page, "</head>", '<style>@media print{#next{font-size:8.5pt;line-height:1.35}}</style></head>', "note final-page print fit")
    page = replace_pattern(page, r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Parabolic edge smoothing, eventual complete-clock signed-flux positivity, two-sided full-plateau bounds, and the exact normalized rate for one explicit start-prepaid family.">', "note metadata")
    page = replace_pattern(page, r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76l.html">', "note canonical")
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76L · STEP 63 · 2026-09-05</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76L · Step 63 · PARABOLIC EDGE COMPLETE CLOCK</div><h1>{TITLE}</h1><p>L 跟踪同一个 start-prepaid 实整数单 dyadic 带 Chebyshev 剪切流跨越完整时钟。对 <code>√A ≪ m = o(A²)</code>，固定切片的 <code>μ^(3/2)</code> edge 指数被抛物演化压到完整时钟的 <code>μ=(m²/A)^(1/3)</code> 尺度；完整有符号 collar flux 最终为正，并相对 full physical plateau 得到双边估计。冻结归一化二次对数率仍为 <code>-2/11907</code>，所以该显式族不是目标估计的反例。<strong>PROVED LOCALLY FOR THIS FAMILY. HIGH-DEGREE THRESHOLD OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">LITERATURE</span><span class="label">PROVED LOCALLY</span><span class="label">FINITE COMPUTATION</span><span class="label">OPEN</span><span class="label">START-PREPAID FAMILY</span><span class="label">COMPLETE CLOCK POSITIVE</span><span class="label">FULL PHYSICAL PLATEAU</span><span class="label">√A ≪ m = o(A²)</span><span class="label">RATE -2/11907</span><span class="label">FORMAL FIGURE</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76L STEP 63</strong><p>family：explicit start-prepaid</p><p>modes：m,...,2m</p><p>degree：q=m+1</p><p>scale：μ=(m²/A)^(1/3)</p><p>fixed slice：μ^(3/2)</p><p>complete clock：exp(Θ(μ))</p><p>signed flux：eventually positive</p><p>denominator：full plateau L³ mass</p><p>normalized rate：-2/11907</p><p>m≈κA⁴ threshold：OPEN</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_sections() + '\n<section id="reproduce">', "Step 63 sections")
    links = " · ".join([
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076l_parabolic_edge_smoothing_complete_clock.md">Step 63 主文</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076l_parabolic_edge_smoothing_complete_clock_primary_audit.md">primary audit</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076l_report-source.md">source report</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076l_parabolic_edge_smoothing_complete_clock_fixtures.json">fixtures JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076l_parabolic_edge_smoothing_complete_clock_expected.json">expected JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076l_parabolic_edge_smoothing_complete_clock_certificate.json">certificate JSON</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076l_parabolic_edge_smoothing_complete_clock_certificate_report.md">Python report</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076l_parabolic_edge_smoothing_complete_clock_independent_audit.md">Ruby independent audit</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076l_parabolic_edge_smoothing_complete_clock_qa_report.md">certificate QA</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076l_parabolic_edge_smoothing_complete_clock_certificate.py">Python script</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076l_parabolic_edge_smoothing_complete_clock_certificate_independent.rb">Ruby script</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076l_parabolic_edge_smoothing_complete_clock_qa.sh">QA script</a>',
    ])
    figure = f'''<section id="figure"><div class="section-no">FIGURE R0.76L-1 / 冻结有限诊断</div><h2>Forward Chebyshev edge saddle</h2><picture><source srcset="/assets/r076l/{frozen_import.FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r076l/{frozen_import.FIGURE_ID}.png" alt="R0.76L finite diagnostic for the parabolic Chebyshev edge saddle, logarithmic amplitude, and unit-coordinate tilt"></picture><p><a href="/assets/r076l/{frozen_import.FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r076l/{frozen_import.FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r076l/{frozen_import.FIGURE_ID}.svg">SVG</a> · <a href="/figures/r076l/{frozen_import.FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r076l/{frozen_import.FIGURE_ID}/data.csv">data</a> · <a href="/figures/r076l/{frozen_import.FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r076l/{frozen_import.FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r076l/{frozen_import.FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">三面板均为无量纲 binary64 有限诊断，不是 PDE simulation 或 DNS。<code>p=0.75</code> 的有限 tilt 序列在显示区间内略微远离解析极限，尚未进入最终渐近趋近；第三面板是单位坐标有限差分，不是数值导数。FINITE DIAGNOSTIC ONLY. NOT CLAY.</p></section>'''
    evidence = f'''<section id="reproduce"><div class="section-no">L / 冻结证据</div><h2>Step 63 主文、来源边界、双实现证书、formal figure 与 fail-closed QA</h2><p class="files">{links}</p><p><a href="/notes/r0-76l.pdf">同步 reader PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I）</a> · <a href="/{RECAP_SLUG}.pdf">截至 I 的 recap PDF</a></p><p class="note">Certificate：Python 64/64、Ruby 279/279、L.1--L.72、78 displays；25 个 observed-ledger mutations、26 个 parsed-input mutations、11 个参数敏感性与 21 项单字节绑定篡改均被拒绝。完整冻结 ledger 为 24/24。正式图包含 12 个文件、599,429 bytes，SVG/PDF/600 dpi PNG 与 archived data/code/logs/manifest/QA 字节绑定。有限证书和图不替代 continuum proof；本节无 PDE simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', figure + evidence, "Step 63 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>K 的单切片下界与 L 的完整时钟族内吸收</h2><p><a href="#s-489">K：real dyadic fixed-slice lower bound</a> · <a href="#s-497">L：parabolic edge complete clock</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 63 adjacent")
    next_section = f'''<section id="next"><div class="section-no">STOP / NO LATER RELEASE AUTHORIZED</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Later material remains unauthorized, unread, and unpublished</h2><p style="margin:.15rem 0">本站当前发布至 R0.76L Step 63。L 只处理显式 start-prepaid 实整数单 dyadic 带剪切族在 <code>√A ≪ m = o(A²)</code> 下的完整时钟与 full-plateau quotient。<code>m≈κA⁴</code> 的 bulk-exterior saddle、候选阈值、<code>m≈A²</code> 转换区、arbitrary packets、Version-M、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。<a href="/{RECAP_SLUG}.html">查看上一大里程碑 recap（截止 I，不覆盖 J/K/L）</a>。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 63 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    replacements = (
        ('data-site-version="2.41"', 'data-site-version="2.42"', "home version"),
        ("/i18n-en.js?v=2.41", "/i18n-en.js?v=2.42", "home i18n"),
        ("/site-refresh.js?v=2.41.1", "/site-refresh.js?v=2.42.1", "home refresh"),
        ("<strong>v2.41</strong>网页版本", "<strong>v2.42</strong>网页版本", "home stat version"),
        ("<strong>R0.76K</strong>最新研究节点", "<strong>R0.76L</strong>最新研究节点", "home latest"),
        ("<strong>265</strong>公开研究笔记", "<strong>266</strong>公开研究笔记", "home count"),
        ("展开 175 篇公开笔记", "展开 176 篇公开笔记", "home route count"),
        ("综述 v2.41 · 2026-09-05", "综述 v2.42 · 2026-09-05", "home footer"),
        ("Research topology · R0.1–R0.76K", "Research topology · R0.1–R0.76L", "home topology"),
        ('href="#r076k">跳到首页 R0.76K 卡片 →', 'href="#r076l">跳到首页 R0.76L 卡片 →', "home jump"),
        ("R0.70A–R0.76K：167 节已公开，104 节完整封存", "R0.70A–R0.76L：168 节已公开，105 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76K</span>', '<span class="route-range">R0.69P–R0.76L</span>', "home range"),
        ("<h3>R0.76K：实单频带 edge 下界与 exact heat-shear 单切片</h3>", "<h3>R0.76L：抛物边缘平滑与完整时钟 full-plateau 余项</h3>", "home route title"),
        ("R0.72R–R0.76K：</span>", "R0.72R–R0.76L：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76K"', 'aria-label="R0.69P–R0.76L"', "home label"),
        ("全站现有 265 篇公开研究笔记", "全站现有 266 篇公开研究笔记", "home recap count"),
    )
    for old, new, label in replacements:
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76L Step 63 证明显式 start-prepaid 实整数单 dyadic 带族在 √A ≪ m=o(A²) 下的 complete-clock signed flux 最终为正，并相对 full plateau 得到 exp(Θ(μ)) 双边界；m≈κA⁴ 的 high-degree route 仍开放。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76L · 2026-09-05 · STEP 63 · PARABOLIC EDGE COMPLETE CLOCK</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">For one explicit start-prepaid real integer one-dyadic-band shear, parabolic evolution reduces the fixed-slice μ^(3/2) edge exponent to a complete-clock exp(Θ(μ)) residual throughout √A ≪ m=o(A²). The signed flux is eventually positive, but the normalized quadratic logarithmic rate is -2/11907, so this family is not a counterexample. The high-degree m≈κA⁴ route remains open. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76l.pdf">阅读最新 R0.76L 研究笔记 →</a><a href="/assets/r076l/{frozen_import.FIGURE_ID}.pdf">R0.76L 冻结三联图</a><a href="/{RECAP_SLUG}.html">上一大里程碑回顾（截止 I，203 节；不覆盖 J/K/L）</a><a href="/notes/">266 篇研究笔记总索引</a><a href="#r076l">查看首页 R0.76L 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76L · 168 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>105 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76L Step 63 complete-clock family-specific absorption</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">L follows the same explicit start-prepaid packet through the complete clock, proves eventual signed-flux positivity and full-plateau exp(Θ(μ)) bounds for √A ≪ m=o(A²), and records normalized rate -2/11907.</p>', "home summary")
    page = replace_once(page, 'real-dyadic fixed-slice lower sharpness and signed-cap slice for q=o(L²); complete-clock quotient, arbitrary nonlinear fields, and Version-M extraction open</p>',
        'real-dyadic fixed-slice lower sharpness and signed-cap slice for q=o(L²) → start-prepaid parabolic edge smoothing, complete-clock positivity, and full-plateau exp(Θ(μ)) bounds for √A ≪ m=o(A²); m≈κA⁴, arbitrary packets, and Version-M extraction open</p>', "home path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76k.html">R0.76K</a>',
        '<a class="milestone" href="/notes/r0-76k.html">R0.76K</a>\n<a class="milestone" href="/notes/r0-76l.html">R0.76L</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED · STOP · NO LATER RELEASE AUTHORIZED</span><span class="tree-state current">BOUNDARY</span></div><h3>Later material remains unauthorized, unread, and unpublished</h3><p>L 只关闭显式 start-prepaid 单 dyadic 带族在 √A ≪ m=o(A²) 下的 complete-clock sign 与 full-plateau payment。m≈κA⁴ 的 bulk-exterior saddle和候选阈值、m≈A² 转换区、arbitrary packets、Version-M、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''<div class="task-one" id="r076l" data-release="r076l" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76L Step 63 · 2026-09-05 · PARABOLIC EDGE COMPLETE CLOCK</p><h3>{TITLE}</h3><p>对显式 start-prepaid 实整数单 dyadic 带剪切族，L 在 √A ≪ m=o(A²) 中证明 complete signed collar flux 最终为正，并给出相对 full physical plateau 的双边界。完整时钟 edge 余项从 fixed-slice μ^(3/2) 降到 exp(Θ(μ))，归一化二次对数率仍为 -2/11907。p=0.75 的有限 tilt 序列在图示区间内略微远离极限；这不构成渐近反例。NOT CLAY.</p><p><a href="/notes/r0-76l.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76l.pdf">PDF</a> · <a href="/assets/r076l/{frozen_import.FIGURE_ID}.pdf">冻结三联图</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I，不覆盖 J/K/L）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076k"'
    if anchor not in page:
        raise RuntimeError("home K card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    page = replace_pattern(page, r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>',
        f'''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">上一大里程碑回顾 R0.61–R0.76I · 2026-09-05</p><h3>累计回顾收录 203 个节点；全站现有 266 篇公开研究笔记</h3><p>回顾覆盖端点仍为 I。I recap 保持字节不变；J、K 与 L 都在其后，均不触发新 recap。</p><p><strong>当前边界：</strong>m≈κA⁴ bulk saddle、arbitrary packets、Version-M extraction、regularity 与 Clay 仍 OPEN。</p><p><a href="/{RECAP_SLUG}.html"><strong>阅读截止 I 的完整累计回顾 →</strong></a> · <a href="/{RECAP_SLUG}.pdf">下载同步 PDF</a></p></div>''', "home recap card")
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.41"', 'data-site-version="2.42"', "lit version"),
        ("/i18n-en.js?v=2.41", "/i18n-en.js?v=2.42", "lit i18n"),
        ("文献综述 v2.41 · 2026-09-05", "文献综述 v2.42 · 2026-09-05", "lit footer"),
        ("本站 R0.69P–R0.76K 只列为研究笔记", "本站 R0.69P–R0.76L 只列为研究笔记", "lit intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76L</b><strong>parabolic edge smoothing and the complete-clock residual</strong></header><p>Step 63 对显式 start-prepaid 实整数单 dyadic 带剪切族证明：在 <code>√A ≪ m=o(A²)</code> 中，complete signed collar flux 最终为正，相对 full physical plateau 的 quotient 具有 <code>exp(Θ(μ))</code> 双边界，冻结归一化二次对数率为 <code>-2/11907</code>。这是 family-specific negative result；<code>m≈κA⁴</code> 的正式阈值仍 OPEN。<a href="/notes/r0-76l.html">研究笔记</a> <a href="/assets/r076l/{frozen_import.FIGURE_ID}.pdf">冻结三联图</a> <a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I，不覆盖 J/K/L）</a> <a href="#r076l-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><span hidden>开放接口 · 后续版本</span><strong>not authorized, unread, and unpublished</strong></header><p><code>m≈κA⁴</code> bulk-exterior saddle、候选阈值、<code>m≈A²</code> transition、arbitrary packets、Version-M、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "lit route")
    boundary = (
        '<h3 id="r076l-boundary">R0.76L Step 63 的 polynomial heat flow 与 family-specific 完整时钟边界</h3>'
        '<p><a href="https://dlmf.nist.gov/18.5">NIST DLMF §18.5</a>、<a href="https://dlmf.nist.gov/18.9">§18.9</a> 与 <a href="https://dlmf.nist.gov/18.14">§18.14</a> 支持 classical Chebyshev representations、derivatives 与 interval inequalities；'
        '<a href="https://link.springer.com/article/10.1007/s11005-025-01946-9">Hall–Ho 2025</a> 与 <a href="https://ahl.centre-mersenne.org/item/AHL_2025__8__1_0/">Kabluchko 2025</a> 提供 polynomial heat-flow/Hermite 的现代背景。Batahan–Shehata 与 Khan 给出 fixed-scale Hermite–Chebyshev operational precedents，因此该 operational idea 不作新颖性主张。</p>'
        '<div class="boundary"><strong>R0.76L Step 63 公开边界 · PARABOLIC EDGE COMPLETE CLOCK</strong><p>'
        'LITERATURE：polynomial heat-flow formulas、Gaussian convolution 与 classical Chebyshev/Gegenbauer facts。'
        'PROVED LOCALLY：simultaneous growing-degree edge Laplace principle、fixed-edge tilt、finite-η consecutive-integer exact-shear transfer、所述显式族的 complete-clock positivity、full-plateau 双边界及 normalized rate -2/11907。'
        'FINITE COMPUTATION：绑定 24 个冻结对象，Python 64/64、independent Ruby 279/279，25/25 与 26/26 mutations、11/11 sensitivity、21/21 single-byte tamper checks；formal figure 为 16 行 binary64 diagnostic。p=0.75 tilt 在显示区间内略微远离极限，未用作渐近证据。'
        'OPEN：m≈κA⁴ bulk saddle 和候选阈值、m≈A² transition、arbitrary packets、Version-M、fixed deletion、suitable-weak transfer、regularity 与 singularity。'
        '<strong>FAMILY-SPECIFIC RESULT. NO NOVELTY OR PRIORITY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76l.html">阅读完整笔记</a> · '
        f'<a href="/{RECAP_SLUG}.html">上一大里程碑 recap（截止 I，不覆盖 J/K/L）</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature references anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def figure_publication_binding() -> dict[str, object]:
    canonical = ROOT / f"research/figures/r076l/{frozen_import.FIGURE_ID}"
    assets = []
    for extension in ("pdf", "png", "svg"):
        target = PUBLIC / "assets/r076l" / f"{frozen_import.FIGURE_ID}.{extension}"
        assets.append({"path": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "sha256": sha256(target)})
    return {
        "schemaVersion": "r076l-native-figure-publication-binding-v1",
        "release": CODE, "figureId": frozen_import.FIGURE_ID,
        "publicationStatus": "published-from-frozen-commits",
        "researchSourceCommit": frozen_import.SOURCE_COMMIT,
        "certificateCommit": frozen_import.CERTIFICATE_COMMIT,
        "handoffCommit": frozen_import.HANDOFF_COMMIT,
        "archiveDirectory": f"public/figures/r076l/{frozen_import.FIGURE_ID}",
        "researchArchiveDirectory": f"research/figures/r076l/{frozen_import.FIGURE_ID}",
        "sourceArchiveDirectory": f"figures/r076l-parabolic-edge/{frozen_import.FIGURE_ID}",
        "inventory": {"files": len(frozen_import.FIGURE_NAMES), "bytes": sum(item.stat().st_size for item in canonical.iterdir() if item.is_file())},
        "byteIdentityRequired": True, "publicCopiesComplete": True, "assets": assets,
        "visibleScopeLabel": "FINITE BINARY64 DIAGNOSTIC | P=0.75 TILT PRE-ASYMPTOTICALLY AWAY | NOT PDE SIMULATION | NOT DNS | NO NOVELTY CLAIM | NOT CLAY",
    }


def update_accounting() -> None:
    html_count = len([p for p in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in p.name])
    pdf_count = len([p for p in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in p.name])
    if html_count != 266 or pdf_count not in (222, 223):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(previous.previous.route_post_r060_slugs(HOME.read_text()))
    if post_r060 != 206:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76l.html", "latestPublishedResearchPdf": "/notes/r0-76l.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 203, "latestRecapRelease": "R0.76I",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-05",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076k":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalSealedReleases"].append(RELEASE)
    if (inventory.get("latestPublishedRelease") != RELEASE
            or inventory["publishedReleases"].count(RELEASE) != 1
            or inventory["formalSealedReleases"].count(RELEASE) != 1
            or RELEASE in inventory["formalFigureExemptReleases"]):
        raise RuntimeError("formal inventory release drift")
    inventory["publishedReleaseCount"] = 168
    inventory["formalSealedReleaseCount"] = 105
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 63
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1, "research_version": CODE,
        "scope": "PARABOLIC_EDGE_SMOOTHING_COMPLETE_CLOCK_SIGN_FULL_PLATEAU_EXPLICIT_START_PREPAID_FAMILY",
        "source_commit": frozen_import.SOURCE_COMMIT, "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "initial_source_commit": frozen_import.INITIAL_SOURCE_COMMIT, "certificate_commit": frozen_import.CERTIFICATE_COMMIT,
        "predecessor_handoff_commit": frozen_import.PREDECESSOR_HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256, "frozen_file_count": 24,
        "claim_status": {
            "publication_kind": "PROVED_LOCAL_EXPLICIT_FAMILY_COMPLETE_CLOCK_POSITIVITY_AND_FULL_PLATEAU_TWO_SIDED_BOUND",
            "formal_figure": "REQUIRED_FINITE_BINARY64_DIAGNOSTIC", "simulation_or_dns": "NOT_USED", "dgx": "NOT_USED",
            "novelty_or_priority": "NOT_CLAIMED",
            "literature": "CLASSICAL_POLYNOMIAL_HEAT_FLOW_GAUSSIAN_CONVOLUTION_CHEBYSHEV_GEGENBAUER_FACTS",
            "proved_locally": "DOUBLE_SCALE_EDGE_TILT_INTEGER_SHEAR_TRANSFER_COMPLETE_CLOCK_POSITIVITY_FULL_PLATEAU_TWO_SIDED_BOUND_NORMALIZED_RATE",
            "packet_scope": "EXPLICIT_START_PREPAID_REAL_INTEGER_ONE_DYADIC_BAND_FAMILY_ONLY",
            "degree_window": "SQRT_A_LITTLE_O_M_AND_M_LITTLE_O_A_SQUARED",
            "complete_clock_signed_flux": "EVENTUALLY_POSITIVE_FOR_THIS_FAMILY",
            "full_plateau_quotient": "TWO_SIDED_EXP_THETA_MU_WITH_POLYNOMIAL_PREFACTORS",
            "normalized_quadratic_log_rate": "MINUS_2_OVER_11907",
            "candidate_status": "RULED_OUT_FOR_THIS_EXPLICIT_FAMILY_IN_STATED_WINDOW",
            "formal_high_degree_threshold": "M_COMPARABLE_KAPPA_A_TO_FOUR_OPEN_NOT_A_THEOREM",
            "m_comparable_a_squared_transition": "OPEN_NOT_PROVED",
            "arbitrary_packets": "OPEN_NOT_PROVED",
            "version_m_extraction": "OPEN_NOT_PROVED", "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_24_OF_24", "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_64_OF_64", "independent_ruby": "PASS_279_OF_279",
            "negative_mutations": "PASS_PYTHON_25_OF_25_RUBY_26_OF_26",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_L1_TO_L72_AND_78_DISPLAYS",
            "arithmetic_sensitivity": "PASS_11_OF_11", "single_byte_binding_tamper": "PASS_21_OF_21",
            "formal_figure_or_simulation_package": "PASS_12_FILES_599429_BYTES",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4", "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76l.html", "target_pdf": "/notes/r0-76l.pdf",
            "target_primary_figure": f"/assets/r076l/{frozen_import.FIGURE_ID}.svg",
            "recap_update_required": False, "recap_terminal_release": "R0.76I_STEP60",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076l_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 63, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 203,
        "postR070APublishedReleaseCount": 168, "postR070AFormalSealedReleaseCount": 105,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"], "nextRelease": "r076m",
        "latestPublishedResearchHtml": "/notes/r0-76l.html", "latestPublishedResearchPdf": "/notes/r0-76l.pdf",
        "latestReleaseGate": "tests/r076l-step63-gate.test.mjs", "latestReleasePublicationTest": "tests/r076l-step63-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076l-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076l-step63-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076l-step63-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076l-step63-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076l-step63-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076l-step63", "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "initialSourceCommit": frozen_import.INITIAL_SOURCE_COMMIT, "certificateCommit": frozen_import.CERTIFICATE_COMMIT,
            "predecessorHandoffCommit": frozen_import.PREDECESSOR_HANDOFF_COMMIT, "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT, "coreCommit": frozen_import.SOURCE_COMMIT,
            "figureSourceCommit": frozen_import.CERTIFICATE_COMMIT,
            "formalFigureRequired": True, "recapRequired": False,
        },
        "latestFormalFigurePublication": figure_publication_binding(),
        "latestRecapRelease": "r076i", "latestRecapHtml": f"/{RECAP_SLUG}.html",
        "latestRecapPdf": f"/{RECAP_SLUG}.pdf", "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-76l.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
        for target, expected in RECAP_HASHES.items():
            if sha256(target) != expected:
                raise RuntimeError(f"protected recap drift after generation: {target.relative_to(ROOT)}")
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 63, "siteVersion": VERSION,
        "recapUpdated": False, "recapRelease": "R0.76I", "formalFigure": frozen_import.FIGURE_ID, "formalFigureExemption": False,
        "simulation": False, "pdeData": False, "noveltyClaim": False, "clayClaim": False,
        "theoremStatus": "PROVED_LOCAL_EXPLICIT_FAMILY_COMPLETE_CLOCK_FULL_PLATEAU",
        "modeWindow": "SQRT_A_LITTLE_O_M_AND_M_LITTLE_O_A_SQUARED",
        "normalizedQuadraticLogRate": "MINUS_2_OVER_11907", "formalHighDegreeThreshold": "OPEN",
        "laterReleaseAuthorized": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
