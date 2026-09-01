#!/usr/bin/env python3
"""Publish the frozen R0.74G note without changing research-side sources."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.73"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-73x.html": "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776",
    PUBLIC / "recap-r0-61-r0-73x.pdf": "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa",
}
FIGURE_DIR = "fig-r074g-complete-payment-ledger"
FIGURE_SLUG = "fig-r074g-complete-payment-ledger"
TITLE = "R0.74G｜完整支付闭合：一个显式光滑解族否定冻结局部坐标不等式"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_recap() -> None:
    for path, expected in RECAP_HASHES.items():
        if sha256(path) != expected:
            raise RuntimeError(f"protected recap drift: {path.relative_to(ROOT)}")


def copy_figures() -> None:
    source = ROOT / "research/figures/r074g" / FIGURE_DIR
    for target in (
        ROOT / "figures/r074g" / FIGURE_DIR,
        PUBLIC / "figures/r074g" / FIGURE_DIR,
    ):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
    asset_dir = PUBLIC / "assets/r074g"
    asset_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", asset_dir / f"{FIGURE_SLUG}.{extension}")


def render_note() -> str:
    page = r'''<!doctype html>
<html lang="zh-CN" data-site-version="__VERSION__">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="完整支付账本闭合；显式光滑 2D3C 解族使 R0.74E 两条冻结不等式的比值至少按 L_j 发散">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74g.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v=__VERSION__"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={tex:{inlineMath:[["\\(","\\)"]],displayMath:[["\\[","\\]"]]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script><style>
:root{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}
@media(prefers-color-scheme:dark){:root{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}
*{box-sizing:border-box}html,body{max-width:100%;overflow-x:hidden}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}
.top{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}.top a{font-weight:700;text-decoration:none}
main{width:min(940px,90vw);margin:auto}.hero{padding:54px 0 30px;border-bottom:1px solid var(--line)}.hero-inner{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}
h1{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}h2{margin:2.8rem 0 1rem;color:var(--rule);font-size:1.55rem}
.stamp,.section-no,.label{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}.stamp{border:1px solid var(--line);padding:1rem;background:var(--raised)}
article{padding:14px 0 72px}section{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}p,li{overflow-wrap:anywhere}.equation{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}.callout{padding:1rem 1.2rem;background:var(--raised);border:1px solid var(--line)}
.labels{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}.label{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}a{color:var(--rule)}img{max-width:100%;height:auto}.files{line-height:2}.figure-note{color:var(--muted);font-size:.94rem}
@media(max-width:720px){body{font-size:15px}.hero-inner{grid-template-columns:1fr}main,article,section{min-width:0}.top{font-size:13px}.equation mjx-container[display="true"]{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}
@media print{:root{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}.top{display:none}body{background:#fff;font-size:10.2pt}main{width:auto}.hero{padding-top:0}.hero-inner{grid-template-columns:1fr 220px}a{color:inherit;text-decoration:none}.equation,.stamp{break-inside:avoid}}
</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74G · 2026-09-01</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74G · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节完成双包族的完整分母账本，并严格否定 R0.74E 中两条已经冻结的候选不等式。</p>
<div class="labels"><span class="label">PROVED</span><span class="label">FINITE</span><span class="label">OPEN</span><span class="label">ROUTE REJECTED</span><span class="label">NOT CLAY</span></div>
<p><strong>ROUTE REJECTED</strong> 只表示指定的两条内部候选估计被反例排除，不表示所有局部坐标估计都失败。<strong>NOT CLAY</strong> 表示本节不构成 Clay 千禧年问题的解答。</p></div>
<div class="stamp"><strong>状态 · R0.74G</strong><p>完整支付反例：PROVED</p><p>三份解析审计：PASS</p><p>有限证书 31/31：FINITE</p><p>图件验证 70/70：FINITE</p><p>R0.74E (3.11)/(4.17)：ROUTE REJECTED</p><p>修正 denominator：OPEN</p><p>Clay 问题：NOT CLAY</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 结论与范围</div><h2>完整支付账本已经闭合</h2>
<p>这一节没有解决三维 Navier--Stokes 千禧年问题。它研究同一个精确、光滑、周期、零均值、无外力的 2D3C 解族，并补齐 R0.74F 尚未估计的缓冲局部能量、规范压力、速度三次项和代数调和项。</p>
<p>与双包存活下界合并后，R0.74E 的式 (3.11) 和式 (4.17) 都不能由解与尺度无关的常数成立。结论是严格的路线淘汰，不是奇性或正则性定理。</p></section>
<section id="s-02"><div class="section-no">02 / 冻结参数</div><h2>同一精确解族与反例尺度</h2>
<div class="equation">\[\lambda=\frac{63}{32},\quad c_h=\frac{15}{16},\quad
\alpha=\frac{14}{15},\quad \beta=\frac{\sqrt{31}}{16},\quad
c_R=\frac1{320},\quad \kappa=16.\]</div>
<div class="equation">\[L_j=\lambda2^j,\qquad R_j=e^{-c_RL_j^2},\qquad r_j=L_jR_j,
\qquad \gamma_j=e^{-c_\gamma L_j^2},\quad c_\gamma=\frac8{3969}.\]</div>
<p>振幅选为</p><div class="equation">\[\mathfrak a_j=B_j\gamma_j^{-1/2}.\]</div>
<p>这里 \(B_j\) 是统一支付尺度；振幅选择与全部分母项在同一账本中处理，没有只保留有利项。</p></section>
<section id="s-03"><div class="section-no">03 / 分子下界</div><h2>R0.74F 的双包存活进入最终比值</h2>
<p>奇对称局部 frame 使 Version-M 与 Version-F 的中心都固定。R0.74F 的全 winding 周期 Brownian bridge 定理给出，对所有充分大的 \(j\)，</p>
<div class="equation">\[\boxed{X_{R_j}^M=X_{R_j}^F\ge cB_j^2L_jR_j^2.}\]</div>
<p>这一步仍是解析定理；有限证书从某个离散层级开始通过，不能替代“充分大”的渐近量词。</p></section>
<section id="s-04"><div class="section-no">04 / 局部能量与压力</div><h2>二次和规范压力行都由同一尺度支付</h2>
<p>缓冲局部能量证明显式排除 packet 梯度进入内球，并保留背景、过渡区和所有周期复制。虽然物理压力 \(p=0\)，移动与减法坐标仍产生规范压力；Riesz/Newton 分解和局部平均估计证明该压力行由同一缓冲能量控制。</p>
<p><strong>PROVED：</strong>能量与压力不是被省略或声明为“低阶”，而是逐项进入最终 denominator 上界。</p></section>
<section id="s-05"><div class="section-no">05 / 全时间占据</div><h2>所有环带、周期复制和 \(p=2,3\) 行</h2>
<p>全时间 occupation 引理同时处理两个 packet、全部 dyadic annuli 和全部周期复制。归一化周期桥、单边路径几何与 Peetre 卷积给出 \(p=2,3\) 的统一上界。</p>
<p>这一行支付 velocity cubic 与 algebraic harmonic packet 项，也保留 background、transition 和 mixed \(G_u\) 项；没有把有限时间窗替换成单点估计。</p></section>
<section id="s-06"><div class="section-no">06 / 完整分母</div><h2>统一上界与比值发散</h2>
<p><strong>PROVED。</strong>对选定振幅和所有充分大的 \(j\)，两种冻结版本都有</p>
<div class="equation">\[\boxed{P_{R_j}^M=P_{R_j}^F\le CB_j^3R_j^3.}\]</div>
<p>因此</p>
<div class="equation">\[\boxed{
\frac{X_{R_j}^M}{(P_{R_j}^M)^{2/3}}
=\frac{X_{R_j}^F}{(P_{R_j}^F)^{2/3}}
\ge cL_j\longrightarrow\infty.}\]</div>
<p>这个发散同时包含缓冲能量的 \(3/2\) 次幂、规范压力、速度三次项和代数调和项；它不是“不完整分母”的伪反例。</p></section>
<section id="s-07"><div class="section-no">07 / 路线结论</div><h2>两条冻结不等式被否定</h2>
<p><strong>ROUTE REJECTED：</strong>不存在一个与解和尺度无关的常数，使 R0.74E 的式 (3.11) 或式 (4.17) 对该精确解族成立。原先冻结的右端不能支付 travelling two-packet 机制，因此从当前路线中退出。</p>
<p>这不表示每一种局部 frame、每一种 denominator 或每一种入口 flux 设计都失败。下一步必须提出新的尺度不变分母，并先用本解族压力测试，避免把待证结论直接放入分母。</p></section>
<section id="s-08"><div class="section-no">08 / 证据分层</div><h2>解析证明与有限复算严格分开</h2>
<p><strong>PROVED：</strong>缓冲能量、规范压力、全时间全复制 occupation、完整 velocity/harmonic 支付、分母上界及两种比值发散均为解析结果；三份独立解析审计分别复核这些部分。</p>
<p><strong>FINITE：</strong>确定性证书 31/31 PASS，独立精确算术实现逐行一致；它只核对有理恒等式、指数余量和几何门。图件 validator 70/70 PASS；图是公式账本，不是 DNS、随机仿真或测量数据。</p></section>
<section id="s-09"><div class="section-no">09 / 文献与开放边界</div><h2>有界检索不承担新颖性声明</h2>
<p><strong>BOUNDED LITERATURE AUDIT：</strong>局部能量、Feynman--Kac、Brownian bridge、Riesz/Newton、Peetre 与 2D3C 被动标量机制各有直接先例。有限检索没有穷尽文献，因此不声明“首次”、新颖性或优先权。</p>
<ul><li>能支付该双包族且不循环的新尺度不变 denominator；</li><li>修正 denominator 对任意解的定理；</li><li>epsilon regularity、continuation 或奇性排除；</li><li>任意三维全局正则性、blow-up 或 Clay 结论。</li></ul>
<p><strong>OPEN / NOT CLAY：</strong>本节没有构造奇点，也没有推出正则性，更不是 Clay 问题的解答。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>完整账本、发散比值与边界</h2>
<picture><source srcset="/assets/r074g/fig-r074g-complete-payment-ledger.svg" type="image/svg+xml"><img src="/assets/r074g/fig-r074g-complete-payment-ledger.png" alt="R0.74G complete payment ledger, divergent ratios, and open boundaries"></picture>
<p><a href="/assets/r074g/fig-r074g-complete-payment-ledger.pdf">下载矢量 PDF</a> · <a href="/assets/r074g/fig-r074g-complete-payment-ledger.png">下载 600 dpi PNG</a> · <a href="/assets/r074g/fig-r074g-complete-payment-ledger.svg">打开 SVG</a> · <a href="/figures/r074g/fig-r074g-complete-payment-ledger/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074g/fig-r074g-complete-payment-ledger/caption.md">图注</a> · <a href="/figures/r074g/fig-r074g-complete-payment-ledger/qa-report.md">图件 QA</a> · <a href="/figures/r074g/fig-r074g-complete-payment-ledger/validation.json">70 项验证记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/public/figures/r074g/fig-r074g-complete-payment-ledger">完整 24 文件图包</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。三者来自同一冻结图包。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、三份解析审计与证书</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_complete_payment_counterexample.md">规范主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_energy_pressure_independent_audit.md">能量—压力独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_occupation_independent_audit.md">occupation 独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_complete_ledger_adversarial_audit.md">完整账本对抗审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_complete_payment_certificate_report.md">有限证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_complete_payment_certificate.json">原始 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074g_complete_payment_certificate.py">证书脚本</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074g_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74g.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74H</h2><p>先提出一个能支付精确双包族、保持尺度不变且不把目标量循环写回右端的新 denominator；随后再检查任意解定理。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def write_dictionary() -> None:
    write_text(ROOT / "research/r074g_bilingual_dictionary.md", """# R0.74G bilingual publication dictionary

The public note is authored completely in Chinese. This dictionary fixes recurring status terminology only.

| Chinese | English |
|---|---|
| 已证明 | PROVED |
| 有限证书或图件复算 | FINITE |
| 开放问题 | OPEN |
| 指定路线被否定 | ROUTE REJECTED |
| 不构成 Clay 问题解答 | NOT CLAY |
| 有界文献审计 | BOUNDED LITERATURE AUDIT |

Chinese title: R0.74G｜完整支付闭合：一个显式光滑解族否定冻结局部坐标不等式
English working title: R0.74G — complete-payment closure rejects the frozen local-frame inequalities
""")


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.72"', f'data-site-version="{VERSION}"', "home version"),
        ('/i18n-en.js?v=1.72', f'/i18n-en.js?v={VERSION}', "home i18n"),
        ('/site-refresh.js?v=1.72.1', f'/site-refresh.js?v={VERSION}.1', "home refresh"),
        ('<strong>v1.72</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "home version stat"),
        ('<span><strong>208</strong>公开研究笔记</span>', '<span><strong>209</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74F</strong>最新研究节点</span>', '<span><strong>R0.74G</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74F', 'Research topology · R0.1–R0.74G', "topology label"),
        ('href="#r074f">跳到首页 R0.74F 卡片 →', 'href="#r074g">跳到首页 R0.74G 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74F：110 节已公开，86 节完整封存', 'href="#r070a">R0.70A–R0.74G：111 节已公开，87 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74F</span>', '<span class="route-range">R0.69P–R0.74G</span>', "route range"),
        ('<h3>R0.74F：双包存活已闭合，完整 denominator 仍开放</h3>', '<h3>R0.74G：完整支付闭合，冻结局部坐标不等式被否定</h3>', "route title"),
        ('<p class="tree-current-summary">奇对称局部 frame 锁定中心，周期 Brownian bridge 证明双包存活；完整付款账本与振幅闭合仍开放。NOT CLAY。</p>', '<p class="tree-current-summary">双包存活与完整 denominator 账本合并后，R0.74E 两条冻结候选估计的比值至少按 L_j 发散；修正 denominator 仍开放。NOT CLAY。</p>', "route summary"),
        ('<p class="tree-path">正观测修复 → 局部付款 → 固定中心运输障碍 → 局部 frame → 双包存活</p>', '<p class="tree-path">局部付款 → 固定中心运输障碍 → 局部 frame → 双包存活 → 完整分母反例</p>', "route short path"),
        ('<span>R0.72R–R0.74F：</span>', '<span>R0.72R–R0.74G：</span>', "route detail range"),
        ('aria-label="R0.69P–R0.74F"', 'aria-label="R0.69P–R0.74G"', "route aria"),
        ('综述 v1.72 · 2026-09-01', f'综述 v{VERSION} · 2026-09-01', "home footer"),
        ('全站现有 208 篇公开研究笔记', '全站现有 209 篇公开研究笔记', "home recap card count"),
    )
    for old, new, label in pairs:
        home = replace_once(home, old, new, label)

    home, n = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74G 已用完整支付账本严格否定 R0.74E 的两条冻结候选估计。下一步寻找能支付双包族、保持尺度不变且不循环的新 denominator；任意三维正则性与 Clay 仍为 OPEN。</span></div>',
        home, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("home focus replacement failed")

    latest = '''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74G · 2026-09-01</p><h2 class="route-map-title" id="latest-release-title">R0.74G｜完整支付闭合</h2><p class="route-map-intro">完整 denominator 账本与双包存活下界合并后，两条冻结局部坐标不等式的比值至少按 \(L_j\) 发散。指定路线被否定；修正 denominator 仍开放。NOT CLAY。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74g.pdf">阅读最新 R0.74G 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">209 篇研究笔记总索引</a><a href="#r074g">查看首页 R0.74G 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74G · 111 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>87 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74G</span></div></div></section>'''
    home, n = re.subn(r'<section class="route-overview latest-release-spotlight".*?</section>', latest, home, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("latest spotlight replacement failed")

    home, n = re.subn(
        r'<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0\.74G</span>.*?</article></div>',
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74H</span><span class="tree-state current">下一检查点</span></div><h3>R0.74H 下一接口</h3><p>提出一个能支付精确双包族、保持尺度不变且不循环的新 denominator；只有先通过该见证，才检查任意解定理。</p></article></div>',
        home, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("next route replacement failed")

    home = replace_once(home, '<a class="milestone" href="/notes/r0-74f.html">R0.74F</a>', '<a class="milestone" href="/notes/r0-74f.html">R0.74F</a>\n<a class="milestone" href="/notes/r0-74g.html">R0.74G</a>', "route note link")
    card = '''          <div class="task-one" id="r074g" data-release="r074g" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74G · 2026-09-01</p><h3>R0.74G｜完整支付闭合：显式光滑解族否定冻结不等式</h3>
            <p>缓冲能量、规范压力、速度三次项和代数调和项全部进入同一分母；与双包存活合并后，两条冻结候选估计的比值至少按 \(L_j\) 发散。</p>
            <p><strong>状态：</strong>PROVED / FINITE / OPEN / ROUTE REJECTED / NOT CLAY。</p>
            <p><a href="/notes/r0-74g.html"><strong>阅读 R0.74G 完整中文笔记 →</strong></a><br><a href="/notes/r0-74g.pdf">下载同步 PDF</a> · <a href="/assets/r074g/fig-r074g-complete-payment-ledger.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a></p>
            <p><strong style="color:var(--gold)">下一接口：</strong>&nbsp;寻找能支付双包族、尺度不变且不循环的新 denominator。</p>
          </div>
'''
    home = replace_once(home, '<div class="task-one" id="r074f" data-release="r074f"', card + '          <div class="task-one" id="r074f" data-release="r074f"', "home R0.74G card")
    home = home.replace('R0.69P–R0.74F', 'R0.69P–R0.74G')
    home = home.replace('R0.70A–R0.74F', 'R0.70A–R0.74G')
    home = home.replace('R0.72R–R0.74F', 'R0.72R–R0.74G')
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.72"', f'data-site-version="{VERSION}"', "literature version"),
        ('/i18n-en.js?v=1.72', f'/i18n-en.js?v={VERSION}', "literature i18n"),
        ('R0.69P–R0.74F 只列为研究笔记', 'R0.69P–R0.74G 只列为研究笔记', "literature range"),
        ('文献综述 v1.72 · 2026-09-01', f'文献综述 v{VERSION} · 2026-09-01', "literature footer"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74G</b><strong>完整支付闭合与冻结局部坐标路线淘汰</strong></header><p>缓冲局部能量、规范压力、全时间 occupation、速度三次项与代数调和项全部闭合；与双包存活合并后，R0.74E 两条候选不等式的比值至少按 \\(L_j\\) 发散。<a href="/notes/r0-74g.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074g-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74H</b><strong>新的尺度不变 denominator</strong></header><p>先寻找能支付精确双包族且不循环的新分母，再检查任意解定理。</p></div>'
    page, n = re.subn(r'<div class="route-step pause"><header><b>开放接口 · R0\.74G</b>.*?</div>', route, page, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074g-boundary">R0.74G 的文献与主张边界</h3><p>local energy、Feynman--Kac、Brownian bridge、Riesz/Newton、Peetre 与 2D3C 被动标量机制均有直接先例；限定检索没有穷尽文献，本站不声明新颖性或优先权。</p><div class="boundary"><strong>R0.74G 的公开边界</strong><p>PROVED、FINITE、OPEN、ROUTE REJECTED 与 NOT CLAY 在研究笔记中逐项分开。路线结论只否定 R0.74E 的两条冻结候选估计。<a href="/notes/r0-74g.html">阅读完整中文笔记</a>。</p></div>
'''
    page = replace_once(page, '        <section id="references">', boundary + '        <section id="references">', "literature boundary")
    write_text(LITERATURE, page)


def update_accounting() -> None:
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": "R0.74G",
        "publicHtmlNoteCount": 209,
        "postR060PublishedNodeCount": 149,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 166,
        "publishedDate": "2026-09-01",
    })
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r074g" not in inventory[key]:
            inventory[key].append("r074g")
    inventory["latestPublishedRelease"] = "r074g"
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    write_json(inventory_path, inventory)

    manifest_path = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": "r074g",
        "siteVersion": VERSION,
        "publicHtmlNoteCount": 209,
        "publicPdfNoteCount": 166,
        "postR060PublishedNodeCount": 149,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074h",
        "latestReleaseGate": "tests/r074g-release.test.mjs",
        "latestReleasePublicationTest": "tests/r074g-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "LOCAL_DIRECT_CHINESE_AUTHORING",
        "latestReleasePdfBinder": "scripts/bind-r074b-g-pdfs.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_path),
    }
    write_json(manifest_path, manifest)


def main() -> None:
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74g.html", render_note())
    write_dictionary()
    update_home()
    update_literature()
    update_accounting()
    assert_recap()
    print(json.dumps({
        "status": "generated",
        "latestRelease": "R0.74G",
        "siteVersion": VERSION,
        "recapPreserved": True,
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
