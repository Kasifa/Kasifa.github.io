#!/usr/bin/env python3
"""Publish frozen R0.74T Step 19 from the verified R0.74S Step 18 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import generate_r074s_step18_release as previous

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.98"
RELEASE = "r074t"
CODE = "R0.74T"
TITLE = "R0.74T｜错峰外叶的 Hölder 强制付款与指数驻留屏障"
FIGURE_ID = "fig-r074t-schedule-invariant-dwell-barrier"
HANDOFF_COMMIT = "cbe52bd5df2dfdb948b0ac8bb761ccd8774004f1"
SOURCE_COMMIT = "2a3a59d4626face7b883159ee9b18500005e41d7"
CORE_COMMIT = "b120598d36140385676bb4a9922d46abcdff0ba4"
FIGURE_COMMIT = "0433c129868ddf349c7b64d427747f590fa06898"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-74s.html": "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81",
    PUBLIC / "recap-r0-61-r0-74s.pdf": "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec",
}
FROZEN_HASHES = {
    "research/r074t_publication_handoff.md": "13ff4edeeebf1da9c9356246c3308e67109857bf36fbceb67fcba5188c1fa71f",
    "research/r074t_schedule_invariant_dwell_coercivity.md": "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
    "research/r074t_schedule_invariant_dwell_primary_audit.md": "0a0a66f6e8d84bb6fad18f6744f02bbf4c2848c96fa5b37dd4b8dc49c628ef99",
    "research/r074t_schedule_invariant_literature_audit.md": "60b49f6279c696a370af5f8050a6162753372eba81f8215e02e15259f084e88b",
    "research/r074t_schedule_invariant_dwell_certificate.json": "ab78d8a8e9a76dc2650d147836c3a51d011c6ef7866f84aa08ed4868b8323c47",
    "research/r074t_schedule_invariant_dwell_certificate_report.md": "acb54e58cf4af40d759962a593a17379cf2bc9769d9664abae800f6afe73764c",
    "research/r074t_schedule_invariant_dwell_independent_audit.md": "81d51239452e48b692125f5a19d2cc1a1ca66c5b65aa0405a1b8d429279b289d",
    "research/r074t_schedule_invariant_dwell_qa_report.md": "b942f990639600a1357518a92361b9c971f5fbaccb2b2bd92189448975b7996a",
    "scripts/r074t_schedule_invariant_dwell_certificate.py": "3229eb8f50a03d66e30449c36070f8734bdded6ed7b11e11324013597b715895",
    "scripts/r074t_schedule_invariant_dwell_certificate_independent.rb": "5fedbd8496e66cc55a4c624b57b21e229a00c948de28df59f91f5ac7461ea03e",
    "scripts/r074t_schedule_invariant_dwell_qa.sh": "371b5c74b1210cd7e8e8151472786b0992e2771ae8e08812f158febfee61b64e",
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
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"milestone recap drift: {target.relative_to(ROOT)}")
    for relative, expected in FROZEN_HASHES.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 19 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074t_schedule_invariant_dwell_certificate.json").read_text())
    checks = certificate.get("checks", [])
    if certificate.get("verdict") != "PASS" or len(checks) != 31 or not all(row.get("pass") for row in checks):
        raise RuntimeError("Step 19 certificate verdict drift")
    if sum(row.get("cases", 0) for row in checks if row.get("group") == "finite") != 18933:
        raise RuntimeError("Step 19 finite case count drift")
    note = (ROOT / "research/r074t_schedule_invariant_dwell_coercivity.md").read_text()
    for token in (
        "R074T_STEP19_STATUS_LOCAL_COERCIVITY_PROVED",
        "R074T_STEP19_STATUS_DWELL_THRESHOLD_PROVED",
        "R074T_STEP19_STATUS_FULL_CLOCK_GATE_OPEN",
        "**NOT CLAY.**",
    ):
        if token not in note:
            raise RuntimeError(f"Step 19 boundary drift: {token}")
    figure = ROOT / "research/figures/r074t" / FIGURE_ID
    names = json.loads((figure / "manifest.json").read_text())["inventory"]["files"]
    if len(names) != 25 or len(set(names)) != 25:
        raise RuntimeError("Step 19 figure inventory drift")
    for name in names:
        expected = sha256(figure / name)
        for mirror in (ROOT / "figures/r074t" / FIGURE_ID, PUBLIC / "figures/r074t" / FIGURE_ID):
            if sha256(mirror / name) != expected:
                raise RuntimeError(f"Step 19 figure mirror drift: {name}")


def render_step19_sections() -> str:
    source = (ROOT / "research/r074t_step19_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 135
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            heading = re.sub(r"^\d+\.\s*", "", lines[0][3:])
            output.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{previous.previous.inline_markup(heading)}</h2>')
            section_open = True
            continue
        if lines[0].startswith("### "):
            output.append(f"<h3>{previous.previous.inline_markup(lines[0][4:])}</h3>")
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
            output.append("<ul>" + "".join(f"<li>{previous.previous.inline_markup(item)}</li>" for item in items) + "</ul>")
            continue
        output.append(f"<p>{previous.previous.inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    if section_index != 145:
        raise RuntimeError(f"Step 19 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="1.97"', 'data-site-version="1.98"', "note version")
    page = replace_once(page, '/i18n-en.js?v=1.97', '/i18n-en.js?v=1.98', "note i18n")
    page = replace_pattern(page, r"<title>.*?</title><meta name=\"description\" content=\".*?\">", f'<title>{TITLE}</title><meta name="description" content="schedule-invariant outer-lobe Hölder coercivity forces an exponential dwell ceiling; two disjoint common-shear lobe windows do not prove a full completed-clock bound">', "note metadata")
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74T · STEP 19 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74T · Step 19 完整中文版本</div><h1>{TITLE}</h1><p>持续 outer lobe 的 kinetic floor 通过精确 Hölder 常数强制支付；相邻壳的低付款因此要求 normalized dwell 指数坍缩。<strong>同一个 exact common-shear 解可以实现两个 disjoint R³ windows，但这只给 K-clock fixed-deletion witness，不给 full clock upper bound，也不能替换为 Hfix。NOT CLAY.</strong></p><div class="labels"><span class="label">PROVED LOCAL COERCIVITY</span><span class="label">EXPONENTIAL DWELL CEILING</span><span class="label">EXACT COMMON-SHEAR</span><span class="label">K-CLOCK ONLY</span><span class="label">FULL CLOCK OPEN</span><span class="label">NOT PDE DATA</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74T STEP 19</strong><p>T.9-T.10：PROVED</p><p>T.17：K-clock witness only</p><p>T.24-T.29：PROVED dwell ceiling</p><p>T.34-T.43：exact common-shear windows</p><p>two windows：strictly disjoint</p><p>full completed clock：OPEN</p><p>K → Hfix without payment：OPEN</p><p>Q.12 / Q.1 / regularity：OPEN</p><p>analytic schematic · NOT PDE DATA / DNS</p></div></div></header><article>'''
    page = replace_pattern(page, r"<body><nav class=\"top\">[\s\S]*?</header><article>", hero, "note hero")
    page = replace_once(page, '<section id="figure">', render_step19_sections() + '\n<section id="figure">', "Step 19 insertion")
    figure = f'''<section id="figure"><div class="section-no">F / 期刊级四联图</div><h2>Schedule-invariant lobe coercivity 与 dwell barrier</h2><picture><source srcset="/assets/r074t/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074t/{FIGURE_ID}.png" alt="R0.74T Step 19 analytic schematic of two disjoint lobe windows, exact Holder coefficient, and exponential dwell ceiling"></picture><p><a href="/assets/r074t/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074t/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074t/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074t/{FIGURE_ID}/caption.md">caption</a> · <a href="/figures/r074t/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074t/{FIGURE_ID}/plot.py">复现脚本</a> · <a href="/figures/r074t/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074t/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">Panels A-B 是 exact schedule 与 Hölder coefficient；Panels C-D 是 derived analytic path。ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY。</p></section>'''
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', figure, "Step 19 figure")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 19 主文、审计、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_schedule_invariant_dwell_coercivity.md">Step 19 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_schedule_invariant_dwell_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_schedule_invariant_dwell_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_schedule_invariant_literature_audit.md">literature audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_schedule_invariant_dwell_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_schedule_invariant_dwell_certificate.json">Python 证书 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_schedule_invariant_dwell_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074t_schedule_invariant_dwell_certificate.py">Python 脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074t_schedule_invariant_dwell_certificate_independent.rb">Ruby 独立脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074t_publication_handoff.md">冻结交接清单</a></p><p><a href="/notes/r0-74t.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一大里程碑 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">上一 recap PDF</a></p><p class="note">Python：31/31 groups、18,933 cases；独立 Ruby：11/11 groups、9,201 assertions。Python/Ruby 分别拒绝 26/26 与 27/27 intentional mutations；有限证书不替代 continuum PDE proof。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 19 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-126">← Step 18：fixed deletion 与同时高度</a> · <a href="#next">下一冻结包尚未发布 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 19 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 等待明确冻结包</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">full clock 与 intrinsic short residence 仍是开放接口</h2><p style="margin:.15rem 0">本站在 R0.74T Step 19 停止。后续 frozen package 可以研究 stated slab 外的 scheduling、真正指数短的 maximal comparable-floor residence、full completed-clock payment、off-target clocks 或 K-to-Hfix bridge；不得把本节的 lower witness 写成 full-clock upper bound，也不得写成 regularity、singularity 或 Clay theorem。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 19 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    replacements = (
        ('data-site-version="1.97"', 'data-site-version="1.98"', "home version"),
        ('/i18n-en.js?v=1.97', '/i18n-en.js?v=1.98', "home i18n"),
        ('/site-refresh.js?v=1.97.1', '/site-refresh.js?v=1.98.1', "home refresh"),
        ('<strong>v1.97</strong>网页版本', '<strong>v1.98</strong>网页版本', "home stat version"),
        ('<strong>R0.74S</strong>最新研究节点', '<strong>R0.74T</strong>最新研究节点', "home latest"),
        ('<strong>221</strong>公开研究笔记', '<strong>222</strong>公开研究笔记', "home public note count"),
        ('展开 131 篇公开笔记', '展开 132 篇公开笔记', "home current route note count"),
        ('综述 v1.97 · 2026-09-03', '综述 v1.98 · 2026-09-03', "home footer"),
        ('Research topology · R0.1–R0.74S', 'Research topology · R0.1–R0.74T', "home topology"),
        ('href="#r074s">跳到首页 R0.74S 卡片 →', 'href="#r074t">跳到首页 R0.74T 卡片 →', "home jump"),
        ('R0.70A–R0.74S：123 节已公开，98 节完整封存', 'R0.70A–R0.74T：124 节已公开，99 节完整封存', "home accounting"),
        ('<span class="route-range">R0.69P–R0.74S</span>', '<span class="route-range">R0.69P–R0.74T</span>', "home route range"),
        ('<h3>R0.74S：fixed deletion、simultaneous height 与时间量词缺口</h3>', '<h3>R0.74T：错峰外叶 Hölder coercivity 与指数 dwell barrier</h3>', "home route title"),
        ('R0.72R–R0.74S：</span>', 'R0.72R–R0.74T：</span>', "home detail range"),
        ('aria-label="R0.69P–R0.74S"', 'aria-label="R0.69P–R0.74T"', "home note links"),
        ('全站现有 221 篇公开研究笔记', '全站现有 222 篇公开研究笔记', "home recap count"),
    )
    for old, new, label in replacements:
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74T Step 19 已证明 schedule-invariant outer-lobe Hölder coercivity 与相邻壳指数 dwell ceiling；两个 disjoint R³ windows 可在同一 exact common-shear 解中实现，但 full completed-clock upper bound、K-to-Hfix bridge、Q.12、Q.1 与正则性仍 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74T · 2026-09-03 · STEP 19</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">persistent outer lobe 通过精确 Hölder 常数强制 cubic payment；ordinary R³ dwell 因此无法靠错开峰值变便宜。两个 disjoint windows 只给 K-clock witness，不给 full clock upper bound。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74t.pdf">阅读最新 R0.74T 研究笔记 →</a><a href="/assets/r074t/{FIGURE_ID}.pdf">Step 19 期刊级四联图</a><a href="/recap-r0-61-r0-74s.html">保留的上一重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">222 篇研究笔记总索引</a><a href="#r074t">查看首页 R0.74T 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74T · 124 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>99 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74T Step 19</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 19 证明 persistent outer-lobe kinetic floor 强制精确 cubic payment，并把 inherited adjacent-shell low-payment escape 压到指数短 dwell。两个 disjoint R³ windows 可在同一 exact common-shear 解中实现，但只给 K-clock fixed-deletion witness；full clock 与 Hfix bridge 仍 OPEN。</p>', "home current summary")
    page = replace_once(page, 'S.342 / S.407 open</p>', 'S.342 / S.407 open → fixed-deletion quantifier split → schedule-invariant lobe coercivity / exponential dwell ceiling / full clock open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74s.html">R0.74S</a>', '<a class="milestone" href="/notes/r0-74s.html">R0.74S</a>\n<a class="milestone" href="/notes/r0-74t.html">R0.74T</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · FROZEN PACKAGE</span><span class="tree-state current">等待中</span></div><h3>full clock / intrinsic short residence</h3><p>等待同一发布任务中的下一份明确冻结包；可研究真正指数短的 maximal residence、off-target clocks、full completed-clock payment 或 K-to-Hfix bridge，不得把 lower witness 写成 full upper bound。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074t" data-release="r074t" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74T Step 19 · 2026-09-03</p><h3>{TITLE}</h3><p>persistent outer lobe 强制精确 cubic payment；两个 disjoint R³ windows 可由同一 exact common-shear 解实现，但 ordinary dwell 不能逃过指数付款屏障。full completed clock 与 K-to-Hfix bridge 仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-74t.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74t.pdf">PDF</a> · <a href="/assets/r074t/{FIGURE_ID}.pdf">期刊级四联图</a> · <a href="/recap-r0-61-r0-74s.html">上一大里程碑 recap（保留）</a></p></div>\n'''
    anchor = '          <div class="task-one" id="r074s"'
    if anchor not in page:
        raise RuntimeError("home R0.74S card anchor missing")
    write_text(HOME, page.replace(anchor, card + anchor, 1))


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.97"', 'data-site-version="1.98"', "literature version"),
        ('/i18n-en.js?v=1.97', '/i18n-en.js?v=1.98', "literature i18n"),
        ('文献综述 v1.97 · 2026-09-03', '文献综述 v1.98 · 2026-09-03', "literature footer"),
        ('本站 R0.69P–R0.74S 只列为研究笔记', '本站 R0.69P–R0.74T 只列为研究笔记', "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74S</b><strong>fixed deletion、simultaneous height 与精确时间量词缺口</strong></header><p>Step 18 证明 moving deletion ≤ fixed deletion ≤ separable excursion，并在已知 payment 后双向比较 fixed hybrid tail 与 completed-clock simultaneous height。triangular clocks 仅给 ABSTRACT ledger obstruction，不是 PDE counterexample；S.486、S.487 与 direct hybrid 仍 OPEN。<a href="/notes/r0-74s.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">Step 17 里程碑 recap</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step kept"><header><b>R0.74T</b><strong>schedule-invariant lobe coercivity 与 exponential dwell barrier</strong></header><p>Step 19 证明 outer-lobe kinetic floor 通过经典 Hölder 强制 cubic payment，并在 inherited adjacent-shell window 导出 necessary exponential dwell ceiling。两个 disjoint R³ windows 存在于同一 exact common-shear 解，但只给 K-clock witness；full clock 与 Hfix bridge 仍 OPEN。<a href="/notes/r0-74t.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">上一里程碑 recap</a> <a href="#r074t-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 等待冻结包</b><strong>full clock / intrinsic short residence</strong></header><p>可研究真正指数短的 maximal residence、off-target clocks、full completed-clock payment 或 K-to-Hfix bridge；不得把 lower witness 提升成 full upper bound。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74S</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074t-boundary">R0.74T Step 19 的文献与主张边界</h3><p>两轮有限一手来源检索核对 exact shearing-wave superposition、classical 2D3C split、periodic-shear scalar dispersion、forced passive-scalar blocks 与 time schedules，以及 physical-shell flux locality。没有一篇被筛来源同时给出同一 unforced common-shear 解内的可独立 lobe windows、total-field floor、positive weighted cubic payment、disjoint-time K-clock witness 与 inherited exponential dwell threshold。这个结论仅为 six-source non-hit，不构成 novelty、priority 或 exhaustiveness claim。</p><div class="boundary"><strong>R0.74T Step 19 公开边界</strong><p>PROVED：T.9-T.10 的 exact outer-lobe coercivity；T.17 的 K-clock one-deletion witness；T.24-T.29 的 dwell identity 与 necessary exponential ceiling；T.34-T.43 的同一 exact common-shear solution 内 two disjoint windows。FINITE：Python 18,933 cases；independent Ruby 9,201 assertions；mutation 与 reproducibility checks 全部通过。OPEN：full completed-clock upper bound、off-target clocks、K-to-Hfix bridge、fixed deletion、direct hybrid、Q.12、Q.1、scale contraction、regularity 与 singularity。图为 analytic schematic / derived analytic values，不是 PDE data 或 DNS。<strong>NOT CLAY.</strong> <a href="/notes/r0-74t.html">阅读完整中文笔记</a>。</p></div>\n'
    anchor = '        <section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    write_text(LITERATURE, page.replace(anchor, boundary + anchor, 1))


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 222 or pdf_count not in (178, 179):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    if post_r060 != 162:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74t.html", "latestPublishedResearchPdf": "/notes/r0-74t.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074s":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleaseCount"] = 124
        inventory["formalSealedReleaseCount"] = 99
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalSealedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 19, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "postR070APublishedReleaseCount": 124, "postR070AFormalSealedReleaseCount": 99,
        "nextRelease": "r074u", "latestPublishedResearchHtml": "/notes/r0-74t.html",
        "latestPublishedResearchPdf": "/notes/r0-74t.pdf",
        "latestReleaseGate": "tests/r074t-step19-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074t-step19-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074t-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074t-step19-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074t-step19-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074t-step19-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074t-step19-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074t-step19", "handoffCommit": HANDOFF_COMMIT,
            "sourceCommit": SOURCE_COMMIT, "coreCommit": CORE_COMMIT,
            "figureSourceCommit": FIGURE_COMMIT,
        },
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-74t.html", render_note())
    if "--note-only" not in __import__("sys").argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 19,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": False,
        "formalFigure": FIGURE_ID, "figureArchiveFiles": 25,
        "simulation": False, "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
