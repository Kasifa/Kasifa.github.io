#!/usr/bin/env python3
"""Publish the R0.74S analytic package without changing frozen mathematics."""

from __future__ import annotations

import hashlib, html, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.87"
RELEASE = "r074s"
CODE = "R0.74S"
TITLE = "R0.74S｜no-exception stopped-work 二次界 no-go"
FIGURE_ID = "fig-r074s-ball-clock-debt"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-74o.html": "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2",
    PUBLIC / "recap-r0-61-r0-74o.pdf": "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076",
}


def sha256(target: Path) -> str:
    return hashlib.sha256(target.read_bytes()).hexdigest()


def write_text(target: Path, value: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def write_json(target: Path, value: object) -> None:
    write_text(target, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once_or_present(value: str, old: str, new: str, label: str) -> str:
    if new in value:
        return value
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_recap() -> None:
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected recap drift: {target.relative_to(ROOT)}")


def verify_sources() -> None:
    expected = {
        "research/r074s_one_sided_ball_clock_no_gain.md": "178c3431f808fa0bb7c8bbf116bd2fdf8c7335eea75e93ba11f51d7eeba7f1af",
        "research/r074s_one_sided_ball_clock_certificate.json": "1afcea511445b75c05da034130c4f1719f4b129c1df496ba5b3f65025ff57219",
        "research/r074s_one_sided_ball_clock_primary_audit.md": "83093d667b0f0ac0af919651c4dd45f87e60b8d2ebde59017f8abdfbd33041b9",
        "research/r074s_one_sided_ball_clock_independent_audit.md": "5ee63f78699891801151171f7fa68e103e52b04d2cc07b20ce48c1d3dd31b209",
        "research/r074s_cross_channel_recombination_no_gain.md": "c24d3673a5e3315777b47fa9751f8546a7df99538b6b22df7566ceb8fdce2e03",
        "scripts/r074s_cross_channel_recombination_certificate.py": "88644cdb311987755777fb951d1eb2ce5e0bdf0e6b829399832def0d9c54cb7c",
        "scripts/r074s_cross_channel_recombination_certificate_independent.rb": "cd5d7afadbaa9a257681f82d9e373777ac735c7675359310fb3a6efffc10ecef",
        "research/r074s_cross_channel_recombination_certificate.json": "5cd6ce5ba59586154c39cdfc5904eec4894dd51370d0cb02c0cd51bff58f4a63",
        "research/r074s_cross_channel_recombination_certificate_report.md": "548a68ca6ae82ea5f18e22504ee41da507569da4c283dbb8506f24b384aba189",
        "research/r074s_dissipation_rayleigh_gate.md": "e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3",
        "research/r074s_dissipation_rayleigh_primary_audit.md": "304bc2b87b9eb97d4f46d8bc4a77da3b1f11e2c37e95e20956504bb4681b2175",
        "research/r074s_dissipation_rayleigh_independent_audit.md": "efc30eb21e8d4e125d4b189455d4419bca9b5d1f1effeb265edba1cdf4a48233",
        "scripts/r074s_dissipation_rayleigh_certificate.py": "61bb1322151b66fc0cf780d2dfc15e0e06dde9a6cc59cc192be1b8c9e8d5e76a",
        "scripts/r074s_dissipation_rayleigh_certificate_independent.rb": "a4ce5bb0d3f20f549e70b7196487fd9540a5ff7be658d4cd52573d65f1a77ff3",
        "research/r074s_dissipation_rayleigh_certificate.json": "4f26fefe25ec92cdae86c2a45f384d0ed87ab3afe83a7d9ef7829ff829be6be1",
        "research/r074s_dissipation_rayleigh_certificate_report.md": "5c566f53e378c9f3fba2a690c3962051142ac00990c1177548b9ae3e956b14cb",
        "research/r074s_defect_relaxed_total_rayleigh_excess.md": "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab",
        "research/r074s_defect_relaxed_total_rayleigh_primary_audit.md": "dbcba5ea68899faf74e4d38c232c58fdd3a71f1b2dcefb1eb007fcf102cd4f73",
        "research/r074s_defect_relaxed_total_rayleigh_independent_audit.md": "d7cb626b07b735b6ef19c8ca20fff670795e32768f3224a756901b230183d875",
        "scripts/r074s_defect_relaxed_total_rayleigh_certificate.py": "18735df5a8eff96167ef6314dad04150636c800c276e2fcffc7cbd8177fce9cf",
        "scripts/r074s_defect_relaxed_total_rayleigh_certificate_independent.rb": "b18b0a0b9937b106c5879a9e28996dd6892ab53f19decb7bca4db38c70a11343",
        "research/r074s_defect_relaxed_total_rayleigh_certificate.json": "3639edbccfddd97781805ed121fc91407771b9bf051ffefae5a17ad80087c69c",
        "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md": "3a6d1e263daa7041edc4083a76c38af44f4fbcd7d2efc8f57592eecbd19ec55a",
    }
    for relative, expected_hash in expected.items():
        if sha256(ROOT / relative) != expected_hash:
            raise RuntimeError(f"frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074s_one_sided_ball_clock_certificate.json").read_text(encoding="utf-8"))
    if certificate["summary"] != {"exact_passed": 5, "exact_total": 5, "finite_passed": 7, "finite_total": 7, "negative_passed": 4, "negative_total": 4, "result": "PASS", "structural_passed": 55, "structural_total": 55}:
        raise RuntimeError("R0.74S certificate boundary drift")
    step6 = json.loads((ROOT / "research/r074s_cross_channel_recombination_certificate.json").read_text(encoding="utf-8"))
    if step6["summary"] != {"exact_passed": 4, "exact_total": 4, "finite_passed": 8, "finite_total": 8, "structural_passed": 58, "structural_total": 58, "negative_passed": 10, "negative_total": 10, "result": "PASS"}:
        raise RuntimeError("R0.74S Step 6 certificate boundary drift")
    step7 = json.loads((ROOT / "research/r074s_dissipation_rayleigh_certificate.json").read_text(encoding="utf-8"))
    if step7["summary"] != {"exact_passed": 16, "exact_total": 16, "finite_passed": 8, "finite_total": 8, "negative_mutations_passed": 9, "negative_mutations_total": 9, "structural_passed": 52, "structural_total": 52}:
        raise RuntimeError("R0.74S Step 7 certificate boundary drift")
    step8 = json.loads((ROOT / "research/r074s_defect_relaxed_total_rayleigh_certificate.json").read_text(encoding="utf-8"))
    if step8["summary"] != {"exact_passed": 16, "exact_total": 16, "finite_passed": 19, "finite_total": 19, "negative_mutations_passed": 20, "negative_mutations_total": 20, "structural_passed": 75, "structural_total": 75}:
        raise RuntimeError("R0.74S Step 8 final certificate boundary drift")


def inline_markup(value: str) -> str:
    value = html.escape(" ".join(value.split()))
    value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', value)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)


def report_body() -> str:
    source = (ROOT / "research/r074s_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 0
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            output.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{inline_markup(lines[0][3:])}</h2>')
            section_open = True
            continue
        if lines[0].startswith("### "):
            output.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
            continue
        stripped = block.strip()
        if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
            output.append(f'<div class="equation">{html.escape(stripped)}</div>')
            continue
        if all(line.startswith("- ") or line.startswith("  ") for line in lines):
            items, current = [], ""
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
            continue
        output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    return "\n".join(output)


def render_note() -> str:
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title><meta name="description" content="no-exception stopped work 与 full terminal flux 的 B_Q-精度等价，以及 smooth exact-family no-go">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74s.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}}.top{{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}.top a{{font-weight:700;text-decoration:none}}main{{width:min(940px,90vw);margin:auto}}.hero{{padding:54px 0 30px;border-bottom:1px solid var(--line)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}}h1{{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}}h2{{margin:2.5rem 0 1rem;color:var(--rule);font-size:1.55rem}}.stamp,.section-no,.label{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}}.stamp{{border:1px solid var(--line);padding:1rem;background:var(--raised)}}article{{padding:14px 0 72px}}section{{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}}p,li{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}}.labels{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}.label{{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}}a{{color:var(--rule)}}.files{{line-height:2}}.note{{color:var(--muted);font-size:.94rem}}picture img{{display:block;width:100%;height:auto}}@media(max-width:720px){{body{{font-size:15px}}.hero-inner{{grid-template-columns:1fr}}main,article,section{{min-width:0}}.top{{font-size:13px}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}.top{{display:none}}body{{background:#fff;font-size:9.3pt;line-height:1.5}}main{{width:auto}}.hero{{padding-top:0}}.hero-inner{{grid-template-columns:1fr 220px}}h2{{margin:1.7rem 0 .6rem;break-after:avoid}}#figure{{break-before:page}}a{{color:inherit;text-decoration:none}}a[href]::after{{content:none!important}}.equation,.stamp{{break-inside:avoid}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74S · 2026-09-02</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74S · 完整中文版本</div><h1>{TITLE}</h1><p>\\(\\mathfrak W_{{\\rm up}}\\) 与 full terminal positive flux 只差已付的 \\(B_Q\\)；smooth exact family 使 \\(\\mathfrak W_{{\\rm up}}/(P_R^M)^{{2/3}}\\to\\infty\\)。<strong>UNIVERSAL NO-EXCEPTION BOUND REFUTED. NOT CLAY.</strong></p><div class="labels"><span class="label">PROVED</span><span class="label">EXACT NSE NO-GO</span><span class="label">S.38 RETAINED</span><span class="label">BEST-N NEXT</span><span class="label">FINITE AUDIT</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74S</strong><p>S.163–S.196：PROVED</p><p>stopped work / full flux：EQUIVALENT WITHIN B_Q</p><p>普适 no-exception 二次界：REFUTED</p><p>S.38 条件蕴含：RETAINED</p><p>fixed best-N exceptions：OPEN</p><p>Jordan envelope 二次界：OPEN</p><p>Step 6 scalar no-go：RETAINED</p><p>Q.1 / regularity：OPEN</p><p>无仿真 / NO DGX</p></div></div></header><article>
{report_body()}
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>excess bridge、B_Q-精度等价与 exact-family no-go</h2><picture><source srcset="/assets/r074s/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074s/{FIGURE_ID}.png" alt="R0.74S stopped-work equivalence and exact-family no-go"></picture><p><a href="/assets/r074s/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074s/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074s/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074s/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074s/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">解析恒等式与 inherited smooth exact NSE family 的尺度 no-go；不是 DNS、奇点或正则性证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>解析主文、证书与独立审计</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_problem_freeze.md">问题冻结</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_cross_channel_recombination_no_gain.md">Step 6 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_dissipation_rayleigh_gate.md">Step 7 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_defect_relaxed_total_rayleigh_excess.md">Step 8 最终解析主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_defect_relaxed_total_rayleigh_primary_audit.md">Step 8 主审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_defect_relaxed_total_rayleigh_independent_audit.md">Step 8 独立审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_defect_relaxed_total_rayleigh_certificate.json">Step 8 机器证书 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_defect_relaxed_total_rayleigh_certificate_report.md">Step 8 证书报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_claim_state_update.md">主张边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_literature_boundary.md">文献边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_report-source.md">中文 reader source</a></p><p><a href="/notes/r0-74s.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74o.html">上一大里程碑 recap（截止 R0.74O，157 节）</a> · <a href="/recap-r0-61-r0-74o.pdf">PDF</a></p><p class="note">最终 Step 8：Python 16/16 exact、19/19 finite、75/75 structural、20/20 mutations；Ruby 14/14 groups、22/22 exact、61/61 structural、14/14 source mutations、10/10 artifact mutations、6/6 report checks。有限证书不替代解析证明。</p></section>
<section id="next"><div class="section-no">NEXT / 下一门槛</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">R0.74T</h2><p style="margin:.15rem 0">回到 fixed best-\\(N\\)、terminal-dependent exceptions，并用 \\(\\sqrt N\\,Y_{{2,R}}^{{\\rm sf}}\\) 支付尾部；不再尝试 no-exception supremum。</p></section></article></main></body></html>'''


def copy_figures() -> None:
    source = ROOT / "research/figures/r074s" / FIGURE_ID
    for target in (PUBLIC / "figures/r074s" / FIGURE_ID, ROOT / "figures/r074s" / FIGURE_ID):
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
    pairs = (
        ('data-site-version="1.86"', 'data-site-version="1.87"', "home version"),
        ('/i18n-en.js?v=1.86', '/i18n-en.js?v=1.87', "home i18n"),
        ('/site-refresh.js?v=1.86.1', '/site-refresh.js?v=1.87.1', "home refresh"),
        ('<strong>v1.86</strong>网页版本', '<strong>v1.87</strong>网页版本', "home stat version"),
        ('<h3>R0.74S：低 Rayleigh 耗散支已支付</h3>', '<h3>R0.74S：no-exception stopped-work 二次界 no-go</h3>', "current route title"),
        ('<p class="tree-current-summary">耗散主导 clock 的低 Rayleigh 类具有抛物动能时间质量，并由 (P_R^M)^(2/3) 同时支付；high-Rayleigh 与 anomalous-defect residual 保持开放。NOT CLAY。</p>', '<p class="tree-current-summary">no-exception stopped work 与 full terminal positive flux 只差已付 B_Q；smooth exact family 严格否定普适二次界。S.38 保留，下一步转向 fixed best-N terminal exceptions。NOT CLAY。</p>', "current route summary"),
        ('<p class="tree-path">abstract scalar no-go → 耗散三分法 → low-Rayleigh kinetic mass → all-shell quadratic payment → two open residuals</p>', '<p class="tree-path">low-Rayleigh payment → total-Rayleigh excess → B_Q-precision equivalence → exact NSE no-go → fixed best-N exceptions</p>', "current route path"),
        ('综述 v1.86 · 2026-09-02', '综述 v1.87 · 2026-09-02', "footer"),
    )
    for old, new, label in pairs:
        page = replace_once_or_present(page, old, new, label)
    page, count = re.subn(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74S 已严格排除 no-exception stopped-work 二次界；S.38 条件蕴含仍成立。下一门槛是 fixed best-N、terminal-dependent exceptions，并以 sqrt(N)Y2 支付尾部，而不是继续修补同一个 universal supremum。</span></div>', page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("home focus replacement failed")
    latest = '''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74S · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74S｜no-exception stopped-work 二次界 no-go</h2><p class="route-map-intro">W_up 与 full terminal flux 只差已付 B_Q；smooth exact family 使 W_up/(P_R^M)^(2/3)→∞。S.38 保留，下一步转向 fixed best-N exceptions。NOT CLAY。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74s.pdf">阅读最新 R0.74S 研究笔记 →</a><a href="/assets/r074s/fig-r074s-ball-clock-debt.pdf">期刊主图</a><a href="/recap-r0-61-r0-74o.html">最新大里程碑 recap（R0.61–R0.74O，157 节）</a><a href="/notes/">221 篇研究笔记总索引</a><a href="#r074s">查看首页 R0.74S 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74S · 123 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>98 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74S</span></div></div></section>'''
    page, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")
    page = replace_once_or_present(page, '<a class="milestone" href="/notes/r0-74r.html">R0.74R</a>', '<a class="milestone" href="/notes/r0-74r.html">R0.74R</a>\n<a class="milestone" href="/notes/r0-74s.html">R0.74S</a>', "milestone")
    old_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74T</span><span class="tree-state current">下一检查点</span></div><h3>R0.74T 下一接口</h3><p>只检验 high-Rayleigh 黏性 residual 与 anomalous-defect residual 的 PDE 支付或一致 finite-exception 定理。</p></article></div>'
    new_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74T</span><span class="tree-state current">下一检查点</span></div><h3>R0.74T 下一接口</h3><p>回到 fixed best-N、terminal-dependent exceptions，并用 sqrt(N)Y2 支付尾部；不再尝试 no-exception supremum。</p></article></div>'
    page = replace_once_or_present(page, old_next, new_next, "next route")
    page = replace_once_or_present(page, 'terminal-window convex packing / arbitrary-clock triage / abstract scalar no-go → low-Rayleigh dissipation payment / high-Rayleigh and defect residuals</p>', 'terminal-window convex packing / arbitrary-clock triage / low-Rayleigh payment → excess bridge → no-exception exact NSE no-go → fixed best-N exceptions</p>', "path tail")
    card = '''          <div class="task-one" id="r074s" data-release="r074s" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74S · 2026-09-02</p><h3>R0.74S｜no-exception stopped-work 二次界 no-go</h3><p>W_up 与 full flux 只差已付 B_Q；smooth exact family 严格否定普适二次界。下一步转向 fixed best-N exceptions。NOT CLAY。</p><p><a href="/notes/r0-74s.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74s.pdf">PDF</a> · <a href="/assets/r074s/fig-r074s-ball-clock-debt.pdf">附图</a></p></div>\n'''
    page = re.sub(r'^[ \t]*<div class="task-one" id="r074s" data-release="r074s"[\s\S]*?</div>\n?', "", page, flags=re.M)
    anchor = '          <div class="task-one" id="r074r"'
    if anchor not in page:
        raise RuntimeError("home R card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.86"', 'data-site-version="1.87"', "lit version"), ('/i18n-en.js?v=1.86', '/i18n-en.js?v=1.87', "lit i18n"), ('文献综述 v1.86 · 2026-09-02', '文献综述 v1.87 · 2026-09-02', "lit footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    old = '<div class="route-step kept"><header><b>R0.74S</b><strong>低 Rayleigh 耗散支的抛物动能质量与二次支付</strong></header><p>耗散主导 clock 被精确分成 defect、high-Rayleigh 与 low-Rayleigh 三类；低支由 (P_R^M)^(2/3) 同时支付。Step 6 的 abstract scalar no-go 保留在原范围。<a href="/notes/r0-74s.html">研究笔记</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74T</b><strong>high-Rayleigh 与 anomalous-defect residual</strong></header><p>下一步只检验两项 residual 的 PDE 支付或一致 finite-exception 定理；条件接口不得写成完成结论。</p></div>'
    new = '<div class="route-step kept"><header><b>R0.74S</b><strong>no-exception stopped work 的 B_Q-精度等价与 exact NSE no-go</strong></header><p>S.163–S.196 建立 total-Rayleigh excess interface；S.197–S.198 证明 W_up 与 full terminal flux 只差已付 B_Q；S.199 用 smooth exact family 严格否定普适 no-exception 二次界。S.38 条件蕴含保留。<a href="/notes/r0-74s.html">研究笔记</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74T</b><strong>fixed best-N terminal exceptions</strong></header><p>回到 R0.74Q 的 terminal-dependent exception quantifier，并用 sqrt(N)Y2 支付尾部。</p></div>'
    page = replace_once_or_present(page, old, new, "literature route")
    boundary = '<h3 id="r074s-boundary">R0.74S 的文献与主张边界</h3><p>Step 8 使用 inherited suitable-weak measures、Q-variation、padded-shell cubic payment、Step 2 gate 与 R0.74O/P smooth exact family；这里不声称新颖性、优先权或一般正则性。</p><div class="boundary"><strong>R0.74S 的公开边界</strong><p>PROVED：S.163–S.196 的 excess interface 与 stopped-work bridge；|W_up−C_full|≤B_Q；K_full−B_Q≤W_up≤K_full+B_Q。REFUTED：普适 W_up≲(P_R^M)^(2/3) no-exception antecedent。RETAINED：S.38 条件蕴含。FINITE：最终 Python 16/16、19/19、75/75、20/20；Ruby 14/14 groups、22/22 exact、61/61 structural、14/14 source mutations、10/10 artifact mutations、6/6 report checks。OPEN：fixed best-N terminal exceptions、Jordan envelope 二次界、Q.1 与正则性。<strong>NOT CLAY.</strong> <a href="/notes/r0-74s.html">阅读完整中文笔记</a>。</p></div>\n'
    page = re.sub(r'<h3 id="r074s-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n?', "", page)
    anchor = '        <section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_notes_index() -> None:
    target = PUBLIC / "notes/index.html"
    page = target.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.86"', 'data-site-version="1.87"', "index version"), ('/i18n-en.js?v=1.86', '/i18n-en.js?v=1.87', "index i18n"), ('/site-refresh.js?v=1.86', '/site-refresh.js?v=1.87', "index refresh"), ('研究笔记总索引 · v1.86 · 2026-09-02', '研究笔记总索引 · v1.87 · 2026-09-02', "index footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    entry = '''          <li class="note-entry" data-note="r0-74s"><article><div class="entry-copy"><p class="note-code">R0.74S</p><h3>no-exception stopped-work 二次界 no-go</h3></div><nav class="entry-files" aria-label="R0.74S files"><a class="file-link html" href="/notes/r0-74s.html" aria-label="Read R0.74S HTML">HTML</a><a class="file-link pdf" href="/notes/r0-74s.pdf" aria-label="Download R0.74S PDF">PDF</a></nav></article></li>\n'''
    anchor = '          <li class="note-entry" data-note="r0-74r">'
    page, existing = re.subn(r'\s*<li class="note-entry" data-note="r0-74s">[\s\S]*?</li>\n?', "\n" + entry, page, count=1)
    if existing == 0:
        if anchor not in page:
            raise RuntimeError("index R anchor missing")
        page = page.replace(anchor, entry + anchor, 1)
    write_text(target, page)


def route_post_r060_count(page: str) -> int:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    slugs = re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end])
    return len(slugs) - slugs.index("r0-61")


def update_accounting() -> None:
    html_count = len(list((PUBLIC / "notes").glob("r0-*.html")))
    pdf_count = len(list((PUBLIC / "notes").glob("r0-*.pdf"))) + (0 if (PUBLIC / "notes/r0-74s.pdf").exists() else 1)
    post_r060 = route_post_r060_count(HOME.read_text(encoding="utf-8"))
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {"schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE, "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "latestRecapRelease": "R0.74O", "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-02"})
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if RELEASE not in inventory[key]:
            inventory[key].append(RELEASE)
    inventory["latestPublishedRelease"] = RELEASE
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    inventory["formalFigureExemptReleaseCount"] = len(inventory.get("formalFigureExemptReleases", []))
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({"latestCompletedRelease": RELEASE, "siteVersion": VERSION, "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "nextRelease": "r074t", "latestReleaseGate": "tests/r074s-ball-clock-gate.test.mjs", "latestReleasePublicationTest": "tests/r074s-release.test.mjs", "postR070APublishedReleaseCount": inventory["publishedReleaseCount"], "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"], "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"], "latestRecapRelease": "r074o", "latestRecapHtml": "/recap-r0-61-r0-74o.html", "latestRecapPdf": "/recap-r0-61-r0-74o.pdf", "latestReleaseTranslationScript": "scripts/add-r074s-translations.mjs", "latestReleasePdfBinder": "scripts/bind-r074s-pdf.mjs", "recapPolicy": "MILESTONE_ONLY"})
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_sources()
    assert_recap()
    write_text(PUBLIC / "notes/r0-74s.html", render_note())
    if "--note-only" not in sys.argv:
        copy_figures(); update_home(); update_literature(); update_notes_index(); update_accounting()
    assert_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "formalFigure": FIGURE_ID, "simulation": False, "dgxUsed": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
