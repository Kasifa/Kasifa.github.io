#!/usr/bin/env python3
"""Publish frozen R0.74V Step 21 from the verified R0.74U Step 20 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

import generate_r074u_step20_release as previous

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.00"
RELEASE = "r074v"
CODE = "R0.74V"
TITLE = "R0.74V｜完整时钟上界路线备忘录：精确分解、粗预算与开放占用门"
HANDOFF_COMMIT = "2bd41a53800b2d6f532b6843f4d70ad7fad7ed46"
HANDOFF_SHA256 = "3832ebf8b0fc84ecbb21d064ee3c94a73ce2f56966f29a0d911a6a411c2697ca"
SOURCE_COMMIT = "29f2b56d1a1a22b665de4b36736eeea20c0a0039"
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
    handoff = ROOT / "research/r074v_publication_handoff.md"
    if sha256(handoff) != HANDOFF_SHA256:
        raise RuntimeError("Step 21 handoff drift")
    rows = re.findall(r"\| `([0-9a-f]{64})` \| `([^`]+)` \|", handoff.read_text())
    if len(rows) != 9:
        raise RuntimeError(f"Step 21 frozen ledger drift: {len(rows)}")
    return rows


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"milestone recap drift: {target.relative_to(ROOT)}")
    for expected, relative in frozen_ledger():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"Step 21 frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074v_completed_clock_upper_route_certificate.json").read_text())
    checks = certificate.get("checks", [])
    if certificate.get("verdict") != "PASS" or len(checks) != 33 or not all(row.get("pass") for row in checks):
        raise RuntimeError("Step 21 certificate verdict drift")
    if sum(row.get("cases", 0) for row in checks if row.get("group") == "finite") != 77:
        raise RuntimeError("Step 21 finite case count drift")
    note = (ROOT / "research/r074v_completed_clock_upper_route.md").read_text()
    for token in (
        "R074V_STEP21_STATUS_ROUTE_ONLY",
        "R074V_STEP21_STATUS_K_SUPERLEVEL_UPPER_OPEN",
        "R074V_STEP21_STATUS_ALL_K_LIFTED_COPY_SUMMATION_OPEN",
        "R074V_STEP21_STATUS_RAW_ENDPOINT_MEASURE_GOOD_TIMES_ONLY",
        "**NOT CLAY.**",
    ):
        if token not in note:
            raise RuntimeError(f"Step 21 boundary drift: {token}")


def inline_markup(value: str) -> str:
    return previous.inline_markup(value)


def render_step21_sections() -> str:
    source = (ROOT / "research/r074v_step21_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 155
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
    if section_index != 165:
        raise RuntimeError(f"Step 21 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="1.99"', 'data-site-version="2.00"', "note version")
    page = replace_once(page, '/i18n-en.js?v=1.99', '/i18n-en.js?v=2.00', "note i18n")
    page = replace_pattern(page, r'<title>.*?</title><meta name="description" content=".*?">', f'<title>{TITLE}</title><meta name="description" content="route memo for the completed-clock upper ledger: exact decompositions, coarse budgets, conditional algebra, and explicit open gates">', "note metadata")
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74V · STEP 21 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74V · Step 21 · 路线备忘录</div><h1>{TITLE}</h1><p>本节只完成 completed-clock upper 的精确分解、粗预算、条件代数与失败条件。<strong>V.47-V.50、V.56、all-k lifted-copy extension 和 common-shear remote comparison 全部保持 OPEN；这不是 completed-clock upper theorem。NOT CLAY.</strong></p><div class="labels"><span class="label">ROUTE MEMO</span><span class="label">EXACT DECOMPOSITIONS</span><span class="label">COARSE BUDGETS</span><span class="label">CONDITIONAL ALGEBRA</span><span class="label">V.47-V.50 OPEN</span><span class="label">V.56 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74V STEP 21</strong><p>V.16：good-time completion exact</p><p>V.17-V.23：splitting / absorption exact</p><p>V.31-V.41：lifted coarse budgets</p><p>V.47-V.50：OPEN inputs</p><p>V.56：CONDITIONAL / OPEN</p><p>chi(65)=12191/132088320 &gt; 0</p><p>remote common-shear comparison：OPEN</p><p>regularity / singularity：OPEN</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', render_step21_sections(), "remove inherited figure and insert Step 21")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 21 路线主文、审计、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074v_completed_clock_upper_route.md">路线主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074v_completed_clock_upper_route_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074v_completed_clock_upper_route_independent_audit.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074v_completed_clock_upper_route_qa_report.md">QA report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074v_completed_clock_upper_route_certificate.json">Python 证书 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074v_completed_clock_upper_route_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074v_completed_clock_upper_route_certificate.py">Python 脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074v_completed_clock_upper_route_certificate_independent.rb">Ruby 独立脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074v_completed_clock_upper_route_qa.sh">QA 脚本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074v_publication_handoff.md">冻结交接清单</a></p><p><a href="/notes/r0-74v.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74s.html">保留的上一大里程碑 recap</a> · <a href="/recap-r0-61-r0-74s.pdf">上一 recap PDF</a></p><p class="note">Python：33/33 checks、77 exact finite cases；独立 Ruby：7/7 groups、106 assertions。Python/Ruby 分别拒绝 29/29 与 30/30 intentional mutations；有限算术与结构证书不替代 continuum PDE proof。本路线包没有科学图、DNS、仿真或 PDE 数据。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 21 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-146">← Step 20：intrinsic certified residence</a> · <a href="#next">R0.74W 冻结包尚未发布 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 21 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.74W 等待冻结包</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">先判定 remote adjacent-inward common-shear comparison</h2><p style="margin:.15rem 0">本站在 R0.74V Step 21 停止。后续只有在独立冻结交接后才可发布；当前不读取或公开未冻结的 R0.74W。V.0 remote comparison 先于 V.1 finite-table occupation，二者均不得预写为已证。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 21 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = page.replace(
        'R0.70A–R0.74V：126 节已公开，101 节完整封存',
        'R0.70A–R0.74V：126 节已公开，100 节完整封存',
    )
    for old, new, label in (
        ('data-site-version="1.99"', 'data-site-version="2.00"', "home version"),
        ('/i18n-en.js?v=1.99', '/i18n-en.js?v=2.00', "home i18n"),
        ('/site-refresh.js?v=1.99.1', '/site-refresh.js?v=2.00.1', "home refresh"),
        ('<strong>v1.99</strong>网页版本', '<strong>v2.00</strong>网页版本', "home stat version"),
        ('<strong>R0.74U</strong>最新研究节点', '<strong>R0.74V</strong>最新研究节点', "home latest"),
        ('<strong>223</strong>公开研究笔记', '<strong>224</strong>公开研究笔记', "home public count"),
        ('展开 133 篇公开笔记', '展开 134 篇公开笔记', "home route count"),
        ('综述 v1.99 · 2026-09-03', '综述 v2.00 · 2026-09-03', "home footer"),
        ('Research topology · R0.1–R0.74U', 'Research topology · R0.1–R0.74V', "home topology"),
        ('href="#r074u">跳到首页 R0.74U 卡片 →', 'href="#r074v">跳到首页 R0.74V 卡片 →', "home jump"),
        ('R0.70A–R0.74U：125 节已公开，100 节完整封存', 'R0.70A–R0.74V：126 节已公开，100 节完整封存', "home accounting"),
        ('<span class="route-range">R0.69P–R0.74U</span>', '<span class="route-range">R0.69P–R0.74V</span>', "home range"),
        ('<h3>R0.74U：内禀认证驻留与 full K-superlevel 边界</h3>', '<h3>R0.74V：completed-clock upper 路线备忘录与 occupation gates</h3>', "home route title"),
        ('R0.72R–R0.74U：</span>', 'R0.72R–R0.74V：</span>', "home detail range"),
        ('aria-label="R0.69P–R0.74U"', 'aria-label="R0.69P–R0.74V"', "home links label"),
        ('全站现有 223 篇公开研究笔记', '全站现有 224 篇公开研究笔记', "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74V Step 21 已完成 completed-clock upper 的精确分解、lifted-multiplicity 粗预算与条件代数。V.47-V.50、V.56、all-k lifted-copy extension、remote common-shear comparison、regularity 与 singularity 全部保持 OPEN。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74V · 2026-09-03 · STEP 21 · ROUTE MEMO</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">精确 completion/splitting、lifted chord/volume 粗预算与 conditional target algebra 已建立；V.47-V.50、V.56、all-k lifted-copy occupation 和 remote common-shear comparison 仍 OPEN。不是 completed-clock upper theorem。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74v.pdf">阅读最新 R0.74V 研究笔记 →</a><a href="/recap-r0-61-r0-74s.html">保留的上一重大路线修正 recap（R0.61–R0.74S，161 节）</a><a href="/notes/">224 篇研究笔记总索引</a><a href="#r074v">查看首页 R0.74V 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74V · 126 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>100 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74V Step 21 route memo</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 21 将 completed-clock upper 拆成 exact completion、packet/cross absorption、lifted multiplicity、persistent baselines 与 occupation gates。解析 occupation 和 remote common-shear comparison 未闭合，所以 V.56 与 all-shell upper 保持 OPEN。</p>', "home current summary")
    page = replace_once(page, 'intrinsic certified corridor / K-superlevel lower only / maximal K dwell open</p>', 'intrinsic certified corridor / K-superlevel lower only → completed-clock upper route memo / occupation gates open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-74u.html">R0.74U</a>', '<a class="milestone" href="/notes/r0-74u.html">R0.74U</a>\n<a class="milestone" href="/notes/r0-74v.html">R0.74V</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74W FROZEN PACKAGE</span><span class="tree-state current">等待中</span></div><h3>remote adjacent-inward comparison / finite-table occupation</h3><p>等待同一发布任务中的明确冻结包；当前不读取或公开未冻结内容。先判定 common-shear remote strip，再处理六对 central-chart occupation，均不得预写为已证。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r074v" data-release="r074v" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74V Step 21 · 2026-09-03 · ROUTE MEMO</p><h3>{TITLE}</h3><p>本路线备忘录建立精确分解、lifted-multiplicity 粗预算、条件 target-superlevel algebra 与七类失败条件；V.47-V.50、V.56、all-k occupation 和 remote common-shear comparison 均未证明。无科学图、DNS 或仿真。NOT CLAY.</p><p><a href="/notes/r0-74v.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74v.pdf">PDF</a> · <a href="/recap-r0-61-r0-74s.html">上一大里程碑 recap（保留）</a></p></div>\n'''
    if 'id="r074v" data-release="r074v"' not in page:
        anchor = '          <div class="task-one" id="r074u"'
        if anchor not in page:
            raise RuntimeError("home R0.74U card anchor missing")
        page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.99"', 'data-site-version="2.00"', "literature version"),
        ('/i18n-en.js?v=1.99', '/i18n-en.js?v=2.00', "literature i18n"),
        ('文献综述 v1.99 · 2026-09-03', '文献综述 v2.00 · 2026-09-03', "literature footer"),
        ('本站 R0.69P–R0.74U 只列为研究笔记', '本站 R0.69P–R0.74V 只列为研究笔记', "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74T</b><strong>schedule-invariant lobe coercivity 与 exponential dwell barrier</strong></header><p>Step 19 证明 outer-lobe kinetic floor 通过经典 Hölder 强制 cubic payment，并在 inherited adjacent-shell window 导出 necessary exponential dwell ceiling。两个 disjoint R³ windows 存在于同一 exact common-shear 解，但只给 K-clock witness；full clock 与 Hfix bridge 仍 OPEN。<a href="/notes/r0-74t.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">上一里程碑 recap</a> <a href="#r074t-boundary">主张边界</a></p></div><div class="route-step kept"><header><b>R0.74U</b><strong>intrinsic certified residence 与 K-superlevel lower-only boundary</strong></header><p>Step 20 证明 canonical lobe 的认证几何走廊具有双边 Theta(L_iR^3) 尺度，并与 bounded-payment 所需指数短 dwell 冲突。该走廊只下包含于 completed-clock K-superlevel；完整超水平集没有 converse 或 upper measure bound。<a href="/notes/r0-74u.html">研究笔记</a> <a href="/recap-r0-61-r0-74s.html">上一里程碑 recap</a> <a href="#r074u-boundary">主张边界</a></p></div><div class="route-step kept"><header><b>R0.74V</b><strong>completed-clock upper route memo</strong></header><p>Step 21 建立 exact completion/splitting、lifted-multiplicity coarse budgets、conditional algebra 和 failure conditions。V.47-V.50、V.56、all-k lifted-copy occupation 与 remote common-shear comparison 均为 OPEN。<a href="/notes/r0-74v.html">路线备忘录</a> <a href="#r074v-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74W 等待冻结包</b><strong>remote adjacent-inward comparison / finite-table occupation</strong></header><p>当前不读取或公开未冻结内容；后续结果只有在冻结交接后才可进入本站。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74T</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r074v-boundary">R0.74V Step 21 路线与主张边界</h3><p>本冻结包没有 literature audit，也不作 novelty、priority、nonexistence 或 publishability 判断。本页只记录数学主张等级，不把路线计划转写成文献碰撞结论。</p><div class="boundary"><strong>R0.74V Step 21 公开边界</strong><p>PROVED（仅路线组件）：good-time 三行 completion 与 hard-time canonical-AC 约定；shear/packet exact splitting；packet cross Young absorption；lifted chord ell_k=s_k+s_k^3；periodized-volume tiling；common-shear/all-shell coarse budgets；conditional target algebra；free comparator 的正指数 chi(65)=12191/132088320。FINITE：Python 33/33 groups、77 cases；Ruby 7/7 groups、106 assertions；29/29 与 30/30 mutations rejected。OPEN：V.47-V.50、V.56、all-k lifted-copy extension、remote/adjacent-inward common-shear comparison、all-shell matching upper、fixed deletion、arbitrary-clock extraction、scale contraction、regularity、singularity 与 Millennium problem。没有科学图、DNS、仿真或 PDE 数据。<strong>NOT CLAY.</strong> <a href="/notes/r0-74v.html">阅读路线备忘录</a>。</p></div>\n'
    if 'id="r074v-boundary"' in page:
        page = replace_pattern(page, r'<h3 id="r074v-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n', boundary, "literature R0.74V boundary")
    else:
        anchor = '        <section id="references">'
        if anchor not in page:
            raise RuntimeError("literature reference anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 224 or pdf_count not in (180, 181):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = previous.previous.previous.previous.route_post_r060_count(HOME.read_text(encoding="utf-8"))
    if post_r060 != 164:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-74v.html", "latestPublishedResearchPdf": "/notes/r0-74v.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 161, "latestRecapRelease": "R0.74S",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r074u":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleaseCount"] = 126
        inventory["formalSealedReleaseCount"] = 100
        inventory["publishedReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    inventory["formalSealedReleaseCount"] = 100
    inventory["formalSealedReleases"] = [row for row in inventory["formalSealedReleases"] if row != RELEASE]
    if RELEASE not in inventory["formalFigureExemptReleases"]:
        inventory["formalFigureExemptReleases"].append(RELEASE)
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalSealedReleases"].count(RELEASE) != 0:
        raise RuntimeError("formal inventory duplicate release")
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21}
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 21, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 161,
        "postR070APublishedReleaseCount": 126, "postR070AFormalSealedReleaseCount": 100,
        "formalFigureExemptReleaseCount": 2,
        "nextRelease": "r074w", "latestPublishedResearchHtml": "/notes/r0-74v.html",
        "latestPublishedResearchPdf": "/notes/r0-74v.pdf",
        "latestReleaseGate": "tests/r074v-step21-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074v-step21-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074v-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r074v-step21-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074v-step21-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r074v-step21-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r074v-step21-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r074v-step21", "handoffCommit": HANDOFF_COMMIT,
            "sourceCommit": SOURCE_COMMIT, "coreCommit": SOURCE_COMMIT,
            "formalFigureRequired": False, "recapRequired": False,
        },
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-74v.html", render_note())
    if "--note-only" not in __import__("sys").argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 21,
        "siteVersion": VERSION, "milestoneRecapPreserved": True, "recapUpdated": False,
        "formalFigure": None, "simulation": False, "pdeData": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
