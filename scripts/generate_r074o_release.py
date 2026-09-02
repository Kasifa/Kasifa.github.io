#!/usr/bin/env python3
"""Publish the frozen R0.74O no-go milestone without changing its claims."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.81"
RELEASE = "r074o"
CODE = "R0.74O"
NEXT = "R0.74P"
FIGURE_DIR = "fig-r074o-amplitude-endpoint"
TITLE = "R0.74O｜自由振幅否定了标量平方根对数端点"
FROZEN_CORE = "ed3dc3e48192708a45abd55550662fb559e0262e"
HISTORICAL_RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-73x.html": "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776",
    PUBLIC / "recap-r0-61-r0-73x.pdf": "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once_or_present(value: str, old: str, new: str, label: str) -> str:
    if new in value:
        return value
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_historical_recap() -> None:
    for path, expected in HISTORICAL_RECAP_HASHES.items():
        if sha256(path) != expected:
            raise RuntimeError(f"protected recap drift: {path.relative_to(ROOT)}")


def file_record(path: Path, schema: str) -> dict[str, object]:
    return {"path": path.name, "schema": schema, "bytes": path.stat().st_size, "sha256": sha256(path)}


def copy_figures() -> None:
    source = ROOT / "research/figures/r074o" / FIGURE_DIR
    public_mirror = PUBLIC / "figures/r074o" / FIGURE_DIR
    archive = ROOT / "figures/r074o" / FIGURE_DIR
    for target in (public_mirror, archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
    assets = PUBLIC / "assets/r074o"
    assets.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", assets / f"{FIGURE_DIR}.{extension}")

    frozen_manifest = source / "manifest.json"
    frozen = json.loads(frozen_manifest.read_text(encoding="utf-8"))
    outputs = []
    for extension in ("svg", "pdf", "png"):
        item = file_record(archive / f"figure.{extension}", f"{extension}-journal-master")
        if extension == "png":
            item["dpi"] = 600
        outputs.append(item)
    wrapper = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r074o-publication-compat-v1",
        "figureId": frozen["figure_id"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74O scalar-payment-only endpoint no-go figure package.",
        "supportedClaim": "See the frozen caption, source data, validation record, and synchronized research note; this wrapper changes no scientific asset.",
        "createdAt": "2026-09-02T00:00:00Z",
        "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": FROZEN_CORE, "dirty": False},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json", "precision": "frozen exact or deterministic figure package", "solver": "none", "formalCommand": "use the frozen package command.txt and validate.py", "wallTimeSeconds": 1.0, "monitoring": {"enabled": False}},
        "compute": {"host": "local workstation (hostname intentionally omitted)", "operatingSystem": "macOS arm64", "cpu": "arm64 / local CPU", "memoryGiB": 36.0, "processes": 1, "threadsPerProcess": 1},
        "environment": {"python": "3.12.13", "packagesLock": "requirements.txt"},
        "data": [file_record(archive / "source-data.csv", "r074o-source-data-v1")],
        "sourceData": [],
        "figure": {"widthMillimetres": 178.0, "heightMillimetres": 100.0, "outputs": outputs},
        "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": {"scalarPaymentOnlySquareRootLogEndpoint": "REFUTED", "realizedScalarNoGoFrontier": "PROVED", "optimalUniversalReplacement": "OPEN", "dissipationMatchingLowerBound": "OPEN", "augmentedArbitraryFlowEndpoint": "OPEN", "finiteFigureProvesAnalyticTheorem": False, "globalRegularity": False, "notClay": True},
        "publication": {
            "archiveDirectory": f"public/figures/{RELEASE}/{FIGURE_DIR}",
            "researchArchiveDirectory": f"research/figures/{RELEASE}/{FIGURE_DIR}",
            "directory": f"public/assets/{RELEASE}",
            "fileStem": FIGURE_DIR,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "releaseSourceCommit": FROZEN_CORE,
            "figurePackageCommit": FROZEN_CORE,
            "assets": [{"path": f"public/assets/{RELEASE}/{FIGURE_DIR}.{item['path'].split('.')[-1]}", "bytes": item["bytes"], "sha256": item["sha256"]} for item in outputs],
        },
        "provenance": {"frozenResearchManifestSha256": sha256(frozen_manifest), "compatibilityScope": "publication archive metadata only; frozen research/public packages and all scientific assets are unchanged"},
    }
    write_json(archive / "manifest.json", wrapper)
    names = sorted(path.name for path in archive.iterdir() if path.is_file() and path.name not in {"SHA256SUMS", ".DS_Store"})
    write_text(archive / "SHA256SUMS", "".join(f"{sha256(archive / name)}  {name}\n" for name in names))


def render_note() -> str:
    page = r'''<!doctype html>
<html lang="zh-CN" data-site-version="__VERSION__">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="同一精确 2D3C 解中的自由被动振幅否定只依赖冻结标量支付的普适平方根对数端点">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74o.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v=__VERSION__"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={tex:{inlineMath:[["\\(","\\)"]],displayMath:[["\\[","\\]"]]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script><style>
:root{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}
@media(prefers-color-scheme:dark){:root{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}
*{box-sizing:border-box}html,body{max-width:100%;overflow-x:hidden}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}
.top{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}.top a{font-weight:700;text-decoration:none}
main{width:min(940px,90vw);margin:auto}.hero{padding:54px 0 30px;border-bottom:1px solid var(--line)}.hero-inner{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}
h1{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}h2{margin:2.5rem 0 1rem;color:var(--rule);font-size:1.55rem}
.stamp,.section-no,.label{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}.stamp{border:1px solid var(--line);padding:1rem;background:var(--raised)}
article{padding:14px 0 72px}section{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}p,li{overflow-wrap:anywhere}.equation{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}.callout{padding:1rem 1.2rem;background:var(--raised);border:1px solid var(--line)}
.labels{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}.label{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}a{color:var(--rule)}img{max-width:100%;height:auto}.files{line-height:2}.figure-note{color:var(--muted);font-size:.94rem}
@media(max-width:720px){body{font-size:15px}.hero-inner{grid-template-columns:1fr}main,article,section{min-width:0}.top{font-size:13px}.equation mjx-container[display="true"]{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}
@media print{:root{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}.top{display:none}body{background:#fff;font-size:9pt;line-height:1.42}main{width:auto}.hero{padding-top:0}.hero-inner{grid-template-columns:1fr 220px}h2{margin:1.35rem 0 .45rem}.callout{padding:.6rem .8rem}a{color:inherit;text-decoration:none}.equation,.stamp{break-inside:avoid}}
</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74O · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74O · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节仍然没有解决三维 Navier--Stokes 千禧年问题。R0.74N 在归一化振幅上得到平方根对数匹配律。这里我没有更换流动几何，只放开同一个精确 2D3C 解中一直存在的被动分量振幅。完整标量支付仍停留在背景剪切尺度，而端点量与正领圈通量按振幅平方增长。因此，只依赖冻结标量支付的普适平方根对数端点是假的；更强的已实现标量次前沿也被排除。带独立结构可观测量的端点、任意流正则性和 Clay 问题仍然开放。<strong>NOT CLAY.</strong></p>
<div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div>
<div class="stamp"><strong>状态 · R0.74O</strong><p>标量平方根对数端点：FALSE</p><p>已实现 no-go 前沿：PROVED</p><p>证书 245/245：FINITE</p><p>图件 72/72：FINITE</p><p>增广任意流端点：OPEN</p><p>耗散匹配下界：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 精确振幅自由</div><h2>我只放开被动分量，不改变流动几何</h2>
<p>令 \(m=\rho-\tfrac32c_\gamma=43/423360>0\)，并取</p>
<div class="equation">\[\varkappa_j=L_j^{2/3}\exp\!\left(\frac m3L_j^2\right),\qquad \mathfrak a_{*,j}=\varkappa_jB_j\Gamma_j^{-1/2}.\]</div>
<p>对每个有限 \(j\)，\(u_j^*=(\mathfrak a_{*,j}F_j,B_j\theta_j,0)\)、\(p_j^*=0\) 仍是精确、光滑、周期、均值为零、无外力解。这来自被动分量的特殊线性振幅自由，不是一般 Navier--Stokes 振幅缩放。</p></section>
<section id="s-02"><div class="section-no">02 / 完整支付</div><h2>标量支付保持在背景剪切尺度</h2>
<p>局部能量、规范压力、速度三次项、调和项、加速度与第五支付壳全部重算后，M、F 两框架一致：</p>
<div class="equation">\[\boxed{P_{R_j}^{M,*}=P_{R_j}^{F,*}\asymp B_j^3R_j^3,\qquad \log P_{R_j}^{\alpha,*}=3\rho L_j^2+O(1).}\]</div>
<p>能量行保留严格正余量 \(e_E-2m/3=1171/943200>0\)。反例位于大支付区；小支付估计不受影响。</p></section>
<section id="s-03"><div class="section-no">03 / 二次目标量</div><h2>端点量与正领圈通量按振幅平方增长</h2>
<p>领圈通量对被动振幅严格二次齐次。R0.74F 的终端存活下界对任意被动振幅成立，R0.74N 的全壳上界也可精确缩放。非循环合并后得到</p>
<div class="equation">\[\boxed{X_{R_j}^{\alpha,*}\asymp\mathfrak C_{R_j}^{\alpha,*}\asymp\varkappa_j^2B_j^2L_jR_j^2,\qquad \alpha\in\{M,F\}.}\]</div>
<p>这里 \(X_*\) 的下界来自端点能量分量。耗散分量单独只有上界；没有证明匹配耗散下界。</p></section>
<section id="s-04"><div class="section-no">04 / 标量端点 no-go</div><h2>平方根对数不再是普适标量上界</h2>
<p>定义 \(\delta_*=86/11907\)、\(q_*=8024/11907\)。同一列精确解满足</p>
<div class="equation">\[\boxed{X_{R_j}^{\alpha,*}\asymp\mathfrak C_{R_j}^{\alpha,*}\asymp(P_{R_j}^{\alpha,*})^{8024/11907}(1+\log_+P_{R_j}^{\alpha,*})^{7/6}.}\]</div>
<div class="equation">\[\frac{X_{R_j}^{\alpha,*}}{(P_{R_j}^{\alpha,*})^{2/3}\sqrt{1+\log_+P_{R_j}^{\alpha,*}}}\asymp\frac{\mathfrak C_{R_j}^{\alpha,*}}{(P_{R_j}^{\alpha,*})^{2/3}\sqrt{1+\log_+P_{R_j}^{\alpha,*}}}\longrightarrow\infty.\]</div>
<p>因此，只依赖冻结标量支付的普适平方根对数端点是 FALSE。更一般地，任何 \(\Phi(p)=o\!\left(p^{8024/11907}(1+\log_+p)^{7/6}\right)\) 都不能成为普适标量 majorant。这里不声称该指数最优。</p></section>
<section id="s-05"><div class="section-no">05 / 固定对数幂量词</div><h2>每个预先固定的对数幂也分别失败</h2>
<p>先固定任意 \(\gamma\in\mathbb R\)，再选择 \(M>\max\{0,\gamma-1/2\}\) 和 \(\varkappa_\gamma=L^M\)。则存在一个可依赖于 \(\gamma\) 的精确光滑解族，使</p>
<div class="equation">\[P^{2/3}(1+\log_+P)^\gamma\]</div>
<p>不是普适上界。我没有声称同一列多项式振幅同时处理所有 \(\gamma\)。这条推论与上一节的一列指数振幅定理必须分开。</p></section>
<section id="s-06"><div class="section-no">06 / 证据等级</div><h2>解析结论、继承输入、有限复算和文献边界分开</h2>
<p><strong>PROVED：</strong>任意被动振幅下的精确解结构、完整支付账本、\(P_*\) 尺度、领圈通量的精确二次缩放、\(X_*\) 的非循环两侧闭合、标量次前沿 no-go 与固定 \(\gamma\) 推论。</p>
<p><strong>INHERITED：</strong>R0.74F--N 的精确 2D3C 解、终端叶片下界、通量恒等式、第五壳下界与归一化全壳上界。</p>
<p><strong>FINITE：</strong>Python Fraction 与独立 Ruby Rational 重建 245/245；图包含 26 个文件、24 个 manifest 条目、15 个外部绑定和 25 行校验和，内部验证 72/72。有限复算不替代解析证明。</p>
<p><strong>LITERATURE BOUNDARY：</strong>十四篇一手来源确认 2D3C 被动分量的任意振幅先例，并区分局部能量、压力、通量、偏斜柱体与 Carleson 控制。有限未命中不证明新颖性、优先权、穷尽性或可发表性。</p></section>
<section id="s-07"><div class="section-no">07 / 开放边界</div><h2>下一步必须加入真正独立的结构可观测量</h2>
<ul><li>最优的普适替代前沿仍为 OPEN；</li><li>能检测二次被动振幅、又能稳定传到 suitable weak 极限的增广量仍为 OPEN；</li><li>任意光滑流的增广端点定理、payment-to-admissibility 与 prescribed good scale 仍为 OPEN；</li><li>耗散分量单独的匹配下界仍为 OPEN；</li><li>任意三维数据的正则性或奇性、全局存在与光滑性仍为 OPEN；</li><li>新颖性和优先权仍为 OPEN。</li></ul>
<p><strong>NOT CLAY：</strong>这里构造的是全局光滑结构解上的 no-go，没有奇点，也没有任意数据的全局正则性结论。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>标量支付保持不变，二次目标量逃离平方根对数端点</h2>
<picture><source srcset="/assets/r074o/fig-r074o-amplitude-endpoint.svg" type="image/svg+xml"><img src="/assets/r074o/fig-r074o-amplitude-endpoint.png" alt="R0.74O passive-amplitude endpoint no-go"></picture>
<p><a href="/assets/r074o/fig-r074o-amplitude-endpoint.pdf">下载矢量 PDF</a> · <a href="/assets/r074o/fig-r074o-amplitude-endpoint.png">下载 600 dpi PNG</a> · <a href="/assets/r074o/fig-r074o-amplitude-endpoint.svg">打开 SVG</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/source-data.csv">source-data.csv</a></p>
<p><a href="/figures/r074o/fig-r074o-amplitude-endpoint/caption.md">图注</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/chart-contract-and-source-data.md">图表合同</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/qa-report.md">图件 QA</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/plot.py">绘图源码</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/validate.py">验证器</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/validation.json">72 项验证记录</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/manifest.json">图件 manifest</a> · <a href="/figures/r074o/fig-r074o-amplitude-endpoint/SHA256SUMS">25 项校验和</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是确定性解析示意图，不是 DNS、仿真、拟合数据、采样路径或奇点证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>证明、独立审计、双实现证书、里程碑增量与完整图包</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_problem_freeze.md">问题冻结</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_amplitude_endpoint_counterexample.md">解析主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_amplitude_endpoint_independent_audit.md">解析独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_final_source_rebind_audit.md">最终源文件重绑定</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074o_amplitude_endpoint_certificate.py">Python 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074o_amplitude_endpoint_certificate_independent.rb">独立 Ruby 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_amplitude_endpoint_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_amplitude_endpoint_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_primary_literature_boundary.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_primary_literature_independent_audit.md">文献独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_report-source.md">审计后中文 reader source</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_reader_source_independent_audit.md">reader source 独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_milestone_recap_delta.md">里程碑 recap 增量</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_milestone_recap_independent_audit.md">recap 独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_figure_independent_audit.md">图件独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074o_freeze_manifest.json">冻结清单</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/tests/r074o-amplitude-endpoint-gate.test.mjs">R0.74O 数学门禁</a></p>
<p><a href="/notes/r0-74o.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74o.html">累计回顾 R0.61–R0.74O</a> · <a href="/recap-r0-61-r0-74o.pdf">累计回顾 PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74P</h2><p>冻结一个非循环、尺度临界、可弱稳定的增广可观测量，先检验它是否能看见本节的二次被动振幅。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def assert_bilingual_dictionary() -> None:
    path = ROOT / "research/r074o_bilingual_dictionary.md"
    if sha256(path) != "9dfecf5ccfef88bf7ad2b63532c825078af5665aae0862679323a63a78424e87":
        raise RuntimeError("frozen R0.74O bilingual dictionary drift")
    value = path.read_text(encoding="utf-8")
    for marker in ("平方根对数端点", "自由振幅", "标量次前沿", "端点动能—耗散量"):
        if marker not in value:
            raise RuntimeError(f"frozen dictionary missing {marker}")


def extract_post_r060_slugs(home: str) -> list[str]:
    start = home.index('<section class="route-overview"')
    end = home.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', home[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    first = ordered.index("r0-61")
    return ordered[first:]


def render_recap(slugs: list[str]) -> str:
    if len(slugs) != 157 or slugs[0] != "r0-61" or slugs[-1] != "r0-74o":
        raise RuntimeError(f"recap route coverage drift: {len(slugs)} {slugs[:1]} {slugs[-1:]}")
    links = "\n".join(f'<a href="/notes/{slug}.html">{slug[3:].upper()}</a>' for slug in slugs)
    return rf'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>R0.61–R0.74O 累计回顾｜从 projected-Lamb 到标量支付 no-go</title>
<meta name="description" content="R0.61 至 R0.74O 的 157 节累计回顾：保留结果、淘汰路线、证据等级与下一增广可观测量接口">
<link rel="canonical" href="https://kasifa.github.io/recap-r0-61-r0-74o.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.7 Georgia,"Songti SC",serif}}nav{{padding:12px 5vw;border-top:5px solid var(--ink);border-bottom:3px double var(--ink);display:flex;justify-content:space-between}}main{{width:min(980px,90vw);margin:auto}}header{{padding:55px 0 30px;border-bottom:1px solid var(--line)}}h1{{font-size:clamp(2rem,5vw,3.7rem);line-height:1.08}}h2{{color:var(--rule);margin-top:2.4rem}}section{{border-bottom:1px dotted var(--line);padding-bottom:1rem}}.eyebrow,.tag{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.06em;text-transform:uppercase}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}}.card,.boundary{{background:var(--raised);border:1px solid var(--line);padding:1rem 1.2rem}}.node-links{{display:flex;flex-wrap:wrap;gap:.45rem}}.node-links a{{border:1px solid var(--line);padding:.2rem .45rem;text-decoration:none}}a{{color:var(--rule)}}code{{overflow-wrap:anywhere}}@media(max-width:720px){{body{{font-size:15px}}.grid{{grid-template-columns:1fr}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}nav{{display:none}}body{{font-size:9pt}}main{{width:auto}}header{{padding-top:0}}.card{{break-inside:avoid}}}}</style></head>
<body><nav><a href="/research-review.html">研究首页</a><span>R0.61–R0.74O · 2026-09-02</span></nav><main><header><p class="eyebrow">MAJOR MILESTONE RECAP · 157 NODES</p><h1>从 signed production 到标量支付 no-go</h1><p>这是 R0.60 之后第二份累计回顾。收录节点：157；回顾截止时公开笔记：217。它保留 R0.61–R0.73X 的旧回顾字节不变，并新增 R0.73Y、R0.73Z 与 R0.74A–R0.74O 共 17 个节点。</p><p><a href="/recap-r0-61-r0-74o.pdf">下载同步累计回顾 PDF</a> · <a href="/notes/r0-74o.html">阅读 R0.74O</a></p></header>
<article><section id="retained"><p class="eyebrow">01 / 历史主干</p><h2>R0.61–R0.73X：保留旧结论，不重写旧证据</h2><p>前一阶段从 projected-Lamb 热体积闭合、局部热 packing、临界底部 trace，推进到精确 shear、谱分支、绝热跟踪、临界稳定管和显式外部尾项。若某个延续论证需要速度作用量，仍必须明确写出 <code>\mathcal V\in L_t^1</code>；若某个双线性上界出现常数，则 <code>2K^2</code> 只能在其原有假设下使用。这些历史输入不因本次里程碑而升级。</p></section>
<section><p class="eyebrow">02 / 四个新阶段</p><h2>R0.73Y–R0.74O：17 个节点把问题压缩到新的接口</h2><div class="grid">
<div class="card"><h3>Y–E｜从 production-only 失败到局部坐标支付</h3><p>精确 shear 排除 production-only coercivity；正 covariance、混合 covariance、缓冲环带与随流坐标逐层区分了符号、绝对值、压力和运输。固定中心及其零均值修复均被精确解排除，局部随流坐标成为必要结构。</p></div>
<div class="card"><h3>F–J｜精确双包族与完整支付</h3><p>周期 Brownian bridge 给出终端外环存活；完整支付账本随后闭合，并加入正领圈通量修复。Version M 推进到 suitable weak 门，<code>gamma &lt; 1/2</code> 被精确族排除；第五支付壳给出 <code>P_j asymp B_j^3 R_j^3</code>。</p></div>
<div class="card"><h3>K–N｜全壳层闭合与归一化匹配</h3><p>最近内领圈被压缩为唯一障碍；共同前向律、短时钟 BV、末段排出和超高斯外壳求和依次关闭。归一化精确族达到 <code>X_j asymp C_j asymp P_j^(2/3) sqrt(1+log P_j)</code>，但这还不是任意流端点。</p></div>
<div class="card"><h3>O｜冻结标量支付本身不够</h3><p>同一精确 2D3C 解中的被动振幅可独立放大二次目标量，却不改变标量支付主尺度。因此普适平方根对数端点为 FALSE；任何 (o(p^{{8024/11907}}(1+\log p)^{{7/6}})) 的标量 majorant 也失败。这里没有证明最优替代前沿。</p></div></div></section>
<section><p class="eyebrow">03 / 被淘汰的路线</p><h2>失败结论只作用于写明的命题</h2><ul><li>只看 signed production 的 coercivity：被精确 shear 排除；</li><li>固定中心或只扣除总均值的运输修复：被精确平流与零均值 2D3C 族排除；</li><li>遗漏第五壳的支付账本：不能支持完整下界；</li><li>把归一化振幅的平方根对数匹配外推成普适标量端点：被 R0.74O 的自由被动振幅排除。</li></ul><p>这些 no-go 不是 Navier–Stokes 全局正则性的否定，也不是奇点构造。</p></section>
<section><p class="eyebrow">04 / 证据等级</p><h2>解析、继承、有限复算与文献边界继续分开</h2><div class="boundary"><p><strong>PROVED：</strong>只列当前文件中完成的解析命题。</p><p><strong>INHERITED：</strong>引用前序节点并保持原量词。</p><p><strong>FINITE：</strong>证书、图件和浏览器 QA 只验证实现与有限代数。</p><p><strong>LITERATURE BOUNDARY：</strong>有限检索不证明新颖性、优先权或完备性。</p><p><strong>OPEN：</strong>最优前沿、增广量的弱稳定性、任意流端点与正则性。</p><p><strong>NOT CLAY：</strong>这些结果既未证明任意三维初值全局光滑，也未构造有限时奇点。</p></div></section>
<section><p class="eyebrow">05 / 新方向</p><h2>R0.74P：冻结一个能看见被动振幅的增广可观测量</h2><p>下一接口不是再调标量支付的对数幂，而是加入真正独立、尺度临界、非循环并可传到 suitable weak 极限的结构可观测量。第一道测试是：它必须对 R0.74O 的二次被动振幅增长作出响应，同时保留压力、局部能量缺陷和移动管几何。</p></section>
<section id="node-index"><p class="eyebrow">NODE INDEX / 157</p><h2>R0.61–R0.74O 全部节点</h2><div class="node-links">{links}</div></section>
</article></main></body></html>'''


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    replacements = (
        ('data-site-version="1.80"', 'data-site-version="1.81"', "home version"),
        ('/i18n-en.js?v=1.80', '/i18n-en.js?v=1.81', "home i18n"),
        ('/site-refresh.js?v=1.80.1', '/site-refresh.js?v=1.81.1', "home refresh"),
        ('<strong>v1.80</strong>网页版本', '<strong>v1.81</strong>网页版本', "home version stat"),
        ('<span><strong>216</strong>公开研究笔记</span>', '<span><strong>217</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74N</strong>最新研究节点</span>', '<span><strong>R0.74O</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74N', 'Research topology · R0.1–R0.74O', "topology label"),
        ('href="#r074n">跳到首页 R0.74N 卡片 →', 'href="#r074o">跳到首页 R0.74O 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74N：118 节已公开，94 节完整封存', 'href="#r070a">R0.70A–R0.74O：119 节已公开，95 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74N</span>', '<span class="route-range">R0.69P–R0.74O</span>', "route range"),
        ('<h3>R0.74N：全壳层合成与完整领圈条件</h3>', '<h3>R0.74O：自由振幅否定标量平方根对数端点</h3>', "route title"),
        ('<p class="tree-current-summary">全部内壳、主壳和外壳已合成；精确解族的领圈通量与 X_j 匹配，耗散下界和任意流端点仍开放。</p>', '<p class="tree-current-summary">同一精确 2D3C 解的自由被动振幅排除冻结标量支付的普适平方根对数端点；增广可观测量与任意流端点仍开放。</p>', "route summary"),
        ('<p class="tree-path"><span>R0.72R–R0.74N：</span>', '<p class="tree-path"><span>R0.72R–R0.74O：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74N"', 'aria-label="R0.69P–R0.74O"', "route aria"),
        ('<summary>展开 126 篇公开笔记</summary>', '<summary>展开 127 篇公开笔记</summary>', "route count"),
        ('综述 v1.80 · 2026-09-02', '综述 v1.81 · 2026-09-02', "home footer"),
        ('全站现有 216 篇公开研究笔记', '全站现有 217 篇公开研究笔记', "recap card count"),
    )
    for old, new, label in replacements:
        home = replace_once_or_present(home, old, new, label)

    home, count = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74O 已排除只依赖冻结标量支付的普适平方根对数端点。下一步要加入能看见二次被动振幅、又可弱稳定传递的独立结构可观测量；任意流正则性和 Clay 仍开放。</span></div>',
        home, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74O · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74O｜自由振幅否定了标量平方根对数端点</h2><p class="route-map-intro">同一精确 2D3C 解中的自由被动振幅让二次目标量逃离冻结标量支付；增广可观测量、耗散匹配下界与任意流端点仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74o.pdf">阅读最新 R0.74O 研究笔记 →</a><a href="/recap-r0-61-r0-74o.html">最新大里程碑 recap（R0.61–R0.74O，157 节）</a><a href="/notes/">217 篇研究笔记总索引</a><a href="#r074o">查看首页 R0.74O 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74O · 119 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>95 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74O</span></div></div></section>'''
    home, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, home, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")

    home = replace_once_or_present(home, '<a class="milestone" href="/notes/r0-74n.html">R0.74N</a>', '<a class="milestone" href="/notes/r0-74n.html">R0.74N</a>\n<a class="milestone" href="/notes/r0-74o.html">R0.74O</a>', "route O link")
    home = replace_once_or_present(home, '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74O</span><span class="tree-state current">下一检查点</span></div><h3>R0.74O 下一接口</h3><p>把全壳层领圈控制移到任意流，或建立 payment-to-admissibility 与指定点 core-from-shell 机制。</p></article></div>', '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74P</span><span class="tree-state current">下一检查点</span></div><h3>R0.74P 下一接口</h3><p>冻结一个能看见二次被动振幅、尺度临界、非循环并可弱稳定传递的增广可观测量。</p></article></div>', "next route")
    home = replace_once_or_present(home, 'all-shell synthesis / exact-family matching endpoint law</p>', 'all-shell synthesis / exact-family matching endpoint law → passive-amplitude scalar endpoint no-go</p>', "detailed O route")

    card = r'''          <div class="task-one" id="r074o" data-release="r074o" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74O · 2026-09-02</p><h3>R0.74O｜自由振幅否定了标量平方根对数端点</h3>
            <p>自由被动振幅不改变冻结标量支付主尺度，却让端点量与正领圈通量二次增长；增广任意流端点仍开放。</p>
            <p><a href="/notes/r0-74o.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74o.pdf">PDF</a> · <a href="/assets/r074o/fig-r074o-amplitude-endpoint.pdf">附图</a> · <a href="/recap-r0-61-r0-74o.html">里程碑 recap</a></p>
          </div>
'''
    home, removed = re.subn(r'\s*<div class="task-one" id="r074o" data-release="r074o"[\s\S]*?</div>\n', "\n", home, count=1)
    if removed not in (0, 1):
        raise RuntimeError("home N card removal failed")
    anchor = '          <div class="task-one" id="r074n"'
    if anchor not in home:
        raise RuntimeError("home M card anchor missing")
    home = home.replace(anchor, card + anchor, 1)
    recap = r'''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.74O · 2026-09-02</p><h3>R0.60 recap 之后的累计回顾收录 157 个节点；全站现有 217 篇公开研究笔记</h3><p>新里程碑把 R0.73Y–R0.74O 分成四段：production-only 障碍、局部坐标与完整支付、全壳层平方根对数匹配，以及自由振幅对标量端点的 no-go。</p><p><strong>当前边界：</strong>冻结标量支付不足以普适控制二次目标量；下一步必须加入可弱稳定、能看见被动振幅的独立结构可观测量。任意三维初值正则性与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-74o.html"><strong>阅读 R0.61–R0.74O 完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-74o.pdf">下载同步 PDF</a></p></div>'''
    home, count = re.subn(r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>', lambda _: recap, home, count=1)
    if count != 1:
        raise RuntimeError("home recap card replacement failed")
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.80"', 'data-site-version="1.81"', "literature version"),
        ('/i18n-en.js?v=1.80', '/i18n-en.js?v=1.81', "literature i18n"),
        ('R0.69P–R0.74N 只列为研究笔记', 'R0.69P–R0.74O 只列为研究笔记', "literature range"),
        ('文献综述 v1.80 · 2026-09-02', '文献综述 v1.81 · 2026-09-02', "literature footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74O</b><strong>自由被动振幅与标量端点 no-go</strong></header><p>同一精确 2D3C 解中放开被动分量振幅，完整标量支付仍在背景剪切尺度，端点量与正领圈通量却按振幅平方增长；普适平方根对数端点及更强的已实现标量次前沿因此被排除。<a href="/notes/r0-74o.html">研究笔记</a> <a href="/recap-r0-61-r0-74o.html">最新里程碑 recap</a> <a href="#r074o-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74P</b><strong>增广可观测量与弱稳定接口</strong></header><p>需要一个能看见二次被动振幅、尺度临界、非循环并可传到 suitable weak 极限的独立结构量。</p></div>'
    if '<b>开放接口 · R0.74P</b>' not in page:
        page, count = re.subn(r'<div class="route-step kept"><header><b>R0\.74N</b>.*?<div class="route-step pause"><header><b>开放接口 · R0\.74O</b>.*?</div>', lambda _: route, page, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074o-boundary">R0.74O 的文献与主张边界</h3><p>十四篇一手来源确认 2D3C 被动分量的任意振幅先例，并区分局部能量、压力、通量、偏斜柱体与 Carleson 控制。有限未命中不证明新颖性、优先权、检索完备性或可发表性。</p><div class="boundary"><strong>R0.74O 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 分开。本节排除冻结标量支付的普适平方根对数端点和已实现标量次前沿；最优替代、增广任意流端点、正则性与 Clay 仍开放。<a href="/notes/r0-74o.html">阅读完整中文笔记</a> · <a href="/recap-r0-61-r0-74o.html">阅读里程碑 recap</a>。</p></div>\n'''
    if 'id="r074o-boundary"' not in page:
        anchor = '        <section id="references">'
        if anchor not in page:
            raise RuntimeError("literature references anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def route_post_r060_count(home: str) -> int:
    return len(extract_post_r060_slugs(home))


def update_accounting() -> None:
    html_count = len(list((PUBLIC / "notes").glob("r0-*.html")))
    pdf_count = len(list((PUBLIC / "notes").glob("r0-*.pdf")))
    if not (PUBLIC / "notes/r0-74o.pdf").exists():
        pdf_count += 1
    post_r060 = route_post_r060_count(HOME.read_text(encoding="utf-8"))
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {"schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE, "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "latestRecapRelease": CODE, "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-02"})

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if RELEASE not in inventory[key]:
            inventory[key].append(RELEASE)
    inventory["latestPublishedRelease"] = RELEASE
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    write_json(inventory_path, inventory)

    manifest_path = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157,
        "nextRelease": "r074p", "latestReleaseGate": "tests/r074o-amplitude-endpoint-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074o-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": RELEASE, "latestRecapHtml": "/recap-r0-61-r0-74o.html",
        "latestRecapPdf": "/recap-r0-61-r0-74o.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074o-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074o-pdf.mjs", "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74o.html", render_note())
        assert_bilingual_dictionary()
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_historical_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74o.html", render_note())
    assert_bilingual_dictionary()
    update_home()
    write_text(PUBLIC / "recap-r0-61-r0-74o.html", render_recap(extract_post_r060_slugs(HOME.read_text(encoding="utf-8"))))
    update_literature()
    update_accounting()
    assert_historical_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "recapNodeCount": 157, "translationRoute": "LOCAL_DIRECT_NO_DGX"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
