#!/usr/bin/env python3
"""Publish the R0.74S analytic package without changing frozen mathematics."""

from __future__ import annotations

import hashlib, html, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.85"
RELEASE = "r074s"
CODE = "R0.74S"
TITLE = "R0.74S｜一侧球时钟为何仍留下 ℓ¹ 债务"
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
<title>{TITLE}</title><meta name="description" content="四通道 circular recombination、三通道 genealogy 终端 ℓ¹ 债务与 abstract scalar no-go">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74s.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}}.top{{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}.top a{{font-weight:700;text-decoration:none}}main{{width:min(940px,90vw);margin:auto}}.hero{{padding:54px 0 30px;border-bottom:1px solid var(--line)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}}h1{{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}}h2{{margin:2.5rem 0 1rem;color:var(--rule);font-size:1.55rem}}.stamp,.section-no,.label{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}}.stamp{{border:1px solid var(--line);padding:1rem;background:var(--raised)}}article{{padding:14px 0 72px}}section{{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}}p,li{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}}.labels{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}.label{{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}}a{{color:var(--rule)}}.files{{line-height:2}}.note{{color:var(--muted);font-size:.94rem}}picture img{{display:block;width:100%;height:auto}}@media(max-width:720px){{body{{font-size:15px}}.hero-inner{{grid-template-columns:1fr}}main,article,section{{min-width:0}}.top{{font-size:13px}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}.top{{display:none}}body{{background:#fff;font-size:9.3pt;line-height:1.5}}main{{width:auto}}.hero{{padding-top:0}}.hero-inner{{grid-template-columns:1fr 220px}}h2{{margin:1.7rem 0 .6rem}}a{{color:inherit;text-decoration:none}}a[href]::after{{content:none!important}}.equation,.stamp{{break-inside:avoid}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74S · 2026-09-02</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74S · 完整中文版本</div><h1>{TITLE}</h1><p>四通道 signed recombination 精确返回原 stopped increments；拆出 mismatch 后，三通道消去时间 genealogy 债务，但终端仍是 root-boundary 加 \\(\\ell^1\\) residual。<strong>PROVED ABSTRACT SCALAR NO-GO ONLY. NOT PDE/NSE. NOT CLAY.</strong></p><div class="labels"><span class="label">PROVED</span><span class="label">CIRCULAR ROUTE</span><span class="label">FINITE</span><span class="label">ABSTRACT SCALAR NO-GO</span><span class="label">OPEN</span><span class="label">NOT PDE/NSE</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74S</strong><p>一侧 ball cutoff：PROVED</p><p>四通道重组：PROVED / CIRCULAR</p><p>三通道 genealogy：PROVED</p><p>终端 ℓ¹ 分解：PROVED</p><p>单块 no-go：PROVED ABSTRACT</p><p>PDE/NSE counterexample：NOT CLAIMED</p><p>PDE-weighted genealogy：OPEN</p><p>Q.1 / regularity：OPEN</p><p>无仿真 / NO DGX</p></div></div></header><article>
{report_body()}
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>跨通道重组、终端 ℓ¹ 债务与抽象 no-go</h2><picture><source srcset="/assets/r074s/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074s/{FIGURE_ID}.png" alt="R0.74S cross-channel recombination and terminal l1 debt"></picture><p><a href="/assets/r074s/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074s/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074s/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074s/{FIGURE_ID}/source-data.csv">source data</a> · <a href="/figures/r074s/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">确定性解析图，不是 DNS、仿真、PDE/NSE 反例、奇点或正则性证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>解析主文、证书与独立审计</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_problem_freeze.md">问题冻结</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_one_sided_ball_clock_no_gain.md">Step 5 解析主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_cross_channel_recombination_no_gain.md">Step 6 解析主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_cross_channel_primary_audit.md">Step 6 主审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_cross_channel_independent_audit.md">Step 6 独立审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_claim_state_update.md">主张边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_literature_boundary.md">文献与优先权边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_report-source.md">完整中文 reader source</a></p><p><a href="/notes/r0-74s.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74o.html">上一大里程碑 recap（截止 R0.74O，157 节）</a> · <a href="/recap-r0-61-r0-74o.pdf">PDF</a></p><p class="note">Step 5：5/5 exact、7/7 finite、55/55 structural、4/4 mutations；Step 6：Python 4/4 exact、8/8 finite、58/58 structural、10/10 mutations，Ruby 9/9 independent、8/8 mutations。有限证书不替代解析证明。</p></section>
<section id="next"><div class="section-no">NEXT / 下一门槛</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">R0.74T</h2><p style="margin:.15rem 0">下一步只检验能看见 block length 或 signed transport 的 PDE-paid quantity，优先回到耗散主导分支；不再重试线性重组或未加权 genealogy。</p></section></article></main></body></html>'''


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
        ('data-site-version="1.84"', 'data-site-version="1.85"', "home version"), ('/i18n-en.js?v=1.84', '/i18n-en.js?v=1.85', "home i18n"), ('/site-refresh.js?v=1.84.1', '/site-refresh.js?v=1.85.1', "home refresh"),
        ('<strong>v1.84</strong>网页版本', '<strong>v1.85</strong>网页版本', "home stat version"), ('<span><strong>220</strong>公开研究笔记</span>', '<span><strong>221</strong>公开研究笔记</span>', "home notes"), ('<span><strong>R0.74R</strong>最新研究节点</span>', '<span><strong>R0.74S</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74R', 'Research topology · R0.1–R0.74S', "topology"), ('href="#r074r">跳到首页 R0.74R 卡片 →', 'href="#r074s">跳到首页 R0.74S 卡片 →', "jump"), ('href="#r070a">R0.70A–R0.74R：122 节已公开，97 节完整封存', 'href="#r070a">R0.70A–R0.74S：123 节已公开，98 节完整封存', "progress"),
        ('<span class="route-range">R0.69P–R0.74R</span>', '<span class="route-range">R0.69P–R0.74S</span>', "range"), ('<summary>展开 130 篇公开笔记</summary>', '<summary>展开 131 篇公开笔记</summary>', "route count"), ('aria-label="R0.69P–R0.74R"', 'aria-label="R0.69P–R0.74S"', "aria"),
        ('<h3>R0.74S：一侧 ball-clock 与 ℓ¹/ℓ² no-go</h3>', '<h3>R0.74S：跨通道重组与终端 ℓ¹ debt</h3>', "current route title"),
        ('<p class="tree-current-summary">一侧球完成与终端 Abel 恒等式只给出 ℓ¹；抽象时钟塔排除仅靠正性、线性与 tower identity 获得 ℓ² 压缩。不是 PDE/NSE 反例，NOT CLAY。</p>', '<p class="tree-current-summary">完整 signed 重组精确返回原增量；三通道重组只把债务集中到终端 ℓ¹ residual。单块标量 no-go，不是 PDE/NSE 反例，NOT CLAY。</p>', "current route summary"),
        ('<p class="tree-path">窗口质量收缩 → 任意时钟三分法 → 一侧 ball completion → terminal Abel identity → 抽象 ℓ¹/ℓ² no-go</p>', '<p class="tree-path">一侧 ball-clock → 四通道 circular recombination → 三通道 terminal genealogy → abstract scalar no-go</p>', "current route path"),
        ('<p class="tree-path"><span>R0.72R–R0.74R：</span>', '<p class="tree-path"><span>R0.72R–R0.74S：</span>', "path range"), ('综述 v1.84 · 2026-09-02', '综述 v1.85 · 2026-09-02', "footer"), ('全站现有 220 篇公开研究笔记', '全站现有 221 篇公开研究笔记', "recap count"),
    )
    for old, new, label in pairs:
        page = replace_once_or_present(page, old, new, label)
    page, count = re.subn(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74S 已证明四通道 signed recombination 精确返回原 stopped increments；拆出 mismatch 后三通道消去时间债务，但终端仍为 block-root + ℓ¹ residual。单块标量族给出 N/√N no-go；PDE-weighted genealogy 与耗散付款开放。</span></div>', page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("home focus replacement failed")
    latest = '''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74S · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74S｜一侧球时钟为何仍留下 ℓ¹ 债务</h2><p class="route-map-intro">完整 signed 重组是 circular；三通道正结果仍停在终端 ℓ¹ residual。单块标量 no-go，不是 PDE/NSE 反例，NOT CLAY。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74s.pdf">阅读最新 R0.74S 研究笔记 →</a><a href="/assets/r074s/fig-r074s-ball-clock-debt.pdf">期刊主图</a><a href="/recap-r0-61-r0-74o.html">最新大里程碑 recap（R0.61–R0.74O，157 节）</a><a href="/notes/">221 篇研究笔记总索引</a><a href="#r074s">查看首页 R0.74S 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74S · 123 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>98 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74S</span></div></div></section>'''
    page, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")
    page = replace_once_or_present(page, '<a class="milestone" href="/notes/r0-74r.html">R0.74R</a>', '<a class="milestone" href="/notes/r0-74r.html">R0.74R</a>\n<a class="milestone" href="/notes/r0-74s.html">R0.74S</a>', "milestone")
    old_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74T</span><span class="tree-state current">下一检查点</span></div><h3>R0.74T 下一接口</h3><p>检验跨通道动力学符号关系，或证明 stopped block genealogy 的统一有限复杂度；不再叠加同类正时钟。</p></article></div>'
    new_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74T</span><span class="tree-state current">下一检查点</span></div><h3>R0.74T 下一接口</h3><p>检验能看见 block length 或 signed transport 的 PDE-paid quantity，优先回到耗散主导分支。</p></article></div>'
    page = replace_once_or_present(page, old_next, new_next, "next route")
    page = replace_once_or_present(page, 'terminal-window convex packing / arbitrary-clock triage / open extraction gate → one-sided ball-clock Abel identity / abstract ℓ¹-to-ℓ² no-go</p>', 'terminal-window convex packing / arbitrary-clock triage / one-sided ball-clock → four-channel circular recombination / three-channel terminal genealogy / abstract scalar no-go</p>', "path tail")
    card = '''          <div class="task-one" id="r074s" data-release="r074s" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74S · 2026-09-02</p><h3>R0.74S｜跨通道重组与终端 ℓ¹ 债务</h3><p>完整 signed 重组精确返回原增量；三通道重组只把债务集中到终端 ℓ¹ residual。单块标量 no-go，不是 PDE/NSE 反例，NOT CLAY。</p><p><a href="/notes/r0-74s.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74s.pdf">PDF</a> · <a href="/assets/r074s/fig-r074s-ball-clock-debt.pdf">附图</a></p></div>\n'''
    page = re.sub(r'^[ \t]*<div class="task-one" id="r074s" data-release="r074s"[\s\S]*?</div>\n?', "", page, flags=re.M)
    anchor = '          <div class="task-one" id="r074r"'
    if anchor not in page:
        raise RuntimeError("home R card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.84"', 'data-site-version="1.85"', "lit version"), ('/i18n-en.js?v=1.84', '/i18n-en.js?v=1.85', "lit i18n"), ('R0.69P–R0.74R 只列为研究笔记', 'R0.69P–R0.74S 只列为研究笔记', "lit range"), ('文献综述 v1.84 · 2026-09-02', '文献综述 v1.85 · 2026-09-02', "lit footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    old = '<div class="route-step kept"><header><b>R0.74S</b><strong>一侧 ball-clock Abel 恒等式与 ℓ¹/ℓ² no-go</strong></header><p>三条 stopped channel、二次 ball ledger 与 terminal Abel identity 已证明；抽象时钟塔排除 scalar positivity、linearity、tower identities 单独推出匹配 ℓ² 压缩。不是 PDE/NSE 反例。<a href="/notes/r0-74s.html">研究笔记</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74T</b><strong>跨通道动力学符号或有限 genealogy</strong></header><p>下一步不再增加同类 positive completion，而要保留 root/outer/weight-drop 之间的动力学关系。</p></div>'
    new = '<div class="route-step kept"><header><b>R0.74S</b><strong>四通道 circular recombination、三通道终端分解与 abstract scalar no-go</strong></header><p>完整 signed 重组精确返回原 stopped increments；拆出 mismatch 后，三通道消去 start/merge temporal debts，但终端仍为每块 root-boundary 加全部非负 shell residual 的 ℓ¹ mass。单块标量族排除未加权 genealogy 压缩。<a href="/notes/r0-74s.html">研究笔记</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74T</b><strong>PDE-weighted genealogy 或耗散付款</strong></header><p>下一步检验能看见 block length 或 signed transport 的 PDE-paid quantity，优先回到耗散主导分支。</p></div>'
    page = replace_once_or_present(page, old, new, "literature route")
    boundary = '<h3 id="r074s-boundary">R0.74S 的文献与主张边界</h3><p>四通道与 genealogy 恒等式采用本项目冻结记号；这里没有提出一般 NSE 定理，也不声称新颖性或优先权。</p><div class="boundary"><strong>R0.74S 的公开边界</strong><p>PROVED：完整 signed recombination 精确返回原 stopped increments，故线性路线 circular；三通道分解消去全部 start/merge temporal debts，并留下 block-root 加 shell-residual ℓ¹ mass。NO-GO：单块、一激活、零 merger 的抽象标量族仅排除未加权 component/epoch/merger count 对工作量的匹配压缩。FINITE：Step 6 Python 4/4、8/8、58/58、10/10；Ruby 9/9、8/8，cross-check PASS。OPEN：PDE-weighted genealogy、Q.1、正则性与奇点。<strong>ABSTRACT SCALAR NO-GO ONLY. NOT PDE/NSE. NOT CLAY.</strong> <a href="/notes/r0-74s.html">阅读完整中文笔记</a>。</p></div>\n'
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
        ('data-site-version="1.84"', 'data-site-version="1.85"', "index version"), ('/i18n-en.js?v=1.84', '/i18n-en.js?v=1.85', "index i18n"), ('/site-refresh.js?v=1.84', '/site-refresh.js?v=1.85', "index refresh"), ('content="220 篇公开研究笔记，最新节点 R0.74R。"', 'content="221 篇公开研究笔记，最新节点 R0.74S。"', "index og"), ('<div class="stat"><strong>220</strong><span>公开 HTML 笔记</span></div>', '<div class="stat"><strong>221</strong><span>公开 HTML 笔记</span></div>', "index html"), ('<div class="stat"><strong>177</strong><span>同步 PDF</span></div>', '<div class="stat"><strong>178</strong><span>同步 PDF</span></div>', "index pdf"), ('<div class="stat"><strong>R0.74R</strong><span>最新研究节点</span></div>', '<div class="stat"><strong>R0.74S</strong><span>最新研究节点</span></div>', "index latest"), ('<span><span>18</span> <span>篇</span></span>', '<span><span>19</span> <span>篇</span></span>', "series count"), ('研究笔记总索引 · v1.84 · 2026-09-02', '研究笔记总索引 · v1.85 · 2026-09-02', "index footer"), ('最新节点 R0.74R · 持续修订', '最新节点 R0.74S · 持续修订', "index footer latest"),
    ):
        page = replace_once_or_present(page, old, new, label)
    entry = '''          <li class="note-entry" data-note="r0-74s"><article><div class="entry-copy"><p class="note-code">R0.74S</p><h3>跨通道重组为何仍留下终端 ℓ¹ 债务</h3></div><nav class="entry-files" aria-label="R0.74S files"><a class="file-link html" href="/notes/r0-74s.html" aria-label="Read R0.74S HTML">HTML</a><a class="file-link pdf" href="/notes/r0-74s.pdf" aria-label="Download R0.74S PDF">PDF</a></nav></article></li>\n'''
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
