#!/usr/bin/env python3
"""Publish frozen R0.74M research assets without changing their claims."""

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
VERSION = "1.79"
RELEASE = "r074m"
CODE = "R0.74M"
NEXT = "R0.74N"
FIGURE_DIR = "fig-r074m-nearest-inward-expulsion"
FIGURE_SLUG = FIGURE_DIR
TITLE = "R0.74M｜最后一小段布朗路径，排出了最近内领圈"
FROZEN_CORE = "4b479fd322a0c39b8ae2954719bfe738ebe1b6cf"
RECAP_HASHES = {
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


def assert_recap() -> None:
    for path, expected in RECAP_HASHES.items():
        if sha256(path) != expected:
            raise RuntimeError(f"protected recap drift: {path.relative_to(ROOT)}")


def file_record(path: Path, schema: str) -> dict[str, object]:
    return {"path": path.name, "schema": schema, "bytes": path.stat().st_size, "sha256": sha256(path)}


def copy_figures() -> None:
    source = ROOT / "research/figures/r074m" / FIGURE_DIR
    public_mirror = PUBLIC / "figures/r074m" / FIGURE_DIR
    archive = ROOT / "figures/r074m" / FIGURE_DIR
    for target in (public_mirror, archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    asset_dir = PUBLIC / "assets/r074m"
    asset_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", asset_dir / f"{FIGURE_SLUG}.{extension}")

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
        "figureSchemaVersion": "r074m-publication-compat-v1",
        "figureId": frozen["figure_id"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74M final-segment nearest-inward expulsion figure package.",
        "supportedClaim": "See the frozen caption, source data, validation record, and synchronized research note; this wrapper changes no scientific asset.",
        "createdAt": "2026-09-02T00:00:00Z",
        "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": FROZEN_CORE, "dirty": False},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json", "precision": "frozen exact or deterministic figure package", "solver": "none", "formalCommand": "use the frozen package command.txt and validate.py", "wallTimeSeconds": 1.0, "monitoring": {"enabled": False}},
        "compute": {"host": "local workstation (hostname intentionally omitted)", "operatingSystem": "macOS arm64", "cpu": "arm64 / local CPU", "memoryGiB": 36.0, "processes": 1, "threadsPerProcess": 1},
        "environment": {"python": "3.12.13", "packagesLock": "requirements.txt"},
        "data": [file_record(archive / "source-data.csv", "r074m-source-data-v1")],
        "sourceData": [],
        "figure": {"widthMillimetres": 178.0, "heightMillimetres": 88.0, "outputs": outputs},
        "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": {"nearestInwardCollar": "PROVED", "remainingShellSynthesis": "OPEN", "finiteFigureProvesAnalyticTheorem": False, "globalRegularity": False, "notClay": True},
        "publication": {
            "archiveDirectory": f"public/figures/{RELEASE}/{FIGURE_DIR}",
            "researchArchiveDirectory": f"research/figures/{RELEASE}/{FIGURE_DIR}",
            "directory": f"public/assets/{RELEASE}",
            "fileStem": FIGURE_SLUG,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "releaseSourceCommit": FROZEN_CORE,
            "figurePackageCommit": FROZEN_CORE,
            "assets": [{"path": f"public/assets/{RELEASE}/{FIGURE_SLUG}.{item['path'].split('.')[-1]}", "bytes": item["bytes"], "sha256": item["sha256"]} for item in outputs],
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
<meta name="description" content="最后一小段布朗路径给出相关支撑上的正剪切位移，关闭精确解族的最近内领圈完整有符号行">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74m.html"><link rel="stylesheet" href="/bilingual.css">
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
@media print{:root{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}.top{display:none}body{background:#fff;font-size:9.3pt;line-height:1.5}main{width:auto}.hero{padding-top:0}.hero-inner{grid-template-columns:1fr 220px}h2{margin:1.7rem 0 .6rem}a{color:inherit;text-decoration:none}.equation,.stamp{break-inside:avoid}}
</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74M · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74M · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节仍然没有解决三维 Navier--Stokes 千禧年问题。R0.74L 关闭了主目标领圈；我在本节处理另一个局部门槛：最近内领圈 \(k=j-1\) 的完整有符号行。真实剪切在最后一小段物理时间内把典型布朗路径对应的横向中心推出领圈，少数来得太快的路径则由明确的高斯尾支付。结论只属于 R0.74F--H 构造的精确光滑、周期、无外力解族。<strong>NOT CLAY.</strong></p>
<div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div>
<div class="stamp"><strong>状态 · R0.74M</strong><p>最近内领圈完整行：PROVED</p><p>最后时段排出：PROVED</p><p>证书 38/38：FINITE</p><p>图件 49/49：FINITE</p><p>完整壳层合成：OPEN</p><p>匹配上界：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 主结论</div><h2>最近内领圈完整有符号行已闭合</h2>
<p>沿用 \(R_j=e^{-L_j^2/320}\)、\(\Gamma_{j-1}/\Gamma_j=e^{G_1L_j^2}\)、\(G_1=2/1323\)，并固定 \(s_{R_j}=61R_j^2\)、\(I_{R_j}=(64R_j^2,65R_j^2)\)。本节证明：存在与 \(j\) 无关的 \(C&lt;\infty\)，使充分大的 \(j\) 满足</p>
<div class="equation">\[\boxed{\sup_{\tau\in I_{R_j}}[\mathcal J_{j,j-1}(\tau)]_+\le C\Gamma_jL_jR_j^5.}\]</div>
<p>这里控制完整的 \(j-1\) 截止函数导数，保留全部周期绕行、两包自项和交叉项；四倍安全上界不假设正负包抵消。</p></section>
<section id="s-02"><div class="section-no">02 / 相关支撑</div><h2>领圈位置与剪切滞后留在同一个期望里</h2>
<p>我没有把真实被动包换成自由热包。R0.74L 的共同前向概率律保留端点领圈与剪切滞后的相关性，其中 \(T=R_j^2+t\)，</p>
<div class="equation">\[\begin{aligned}\mathcal P^-(\tau)={}&R_j^6\int_{61R_j^2}^{\tau}\eta_{R_j}(t)\int_{\mathbb T}|\partial K_T(u)|^2\\&\quad\times\mathbb E^{\rm fw}[K_T(X_t)\,\overline D^-(t,q_\omega(t)+u,h_j+X_t)]\,du\,dt.\end{aligned}\]</div>
<p>后面的排出结论只在这个相关支撑上证明；没有使用“给定终点就必然排出”的原则。</p></section>
<section id="s-03"><div class="section-no">03 / 最后时段</div><h2>最后 \(R_j^2/64\) 产生可量化正位移</h2>
<p>若终点落在最近内领圈，而最后一段布朗路径离终点不超过 \(L_jR_j/16\)，则路径保持在 \(|h_j+X_s|\le3L_jR_j/5\) 内。未含 padding 的几何余量为</p>
<div class="equation">\[\frac35-\frac{32}{63}-\frac1{16}=\frac{149}{5040}>0.\]</div>
<p>完整支撑另含 \(R_j/8\) padding；归一化余量是 \(149/5040-1/(8L_j)\)，所以包含关系只对充分大的 \(L_j\) 使用。内向热流缺陷与平台缺陷比较后得到</p>
<div class="equation">\[\mathfrak S_t^\leftarrow[X]\ge\Sigma_{L_j},\qquad\Sigma_L=\frac1{32768}e^{-L^2/640}.\]</div></section>
<section id="s-04"><div class="section-no">04 / 尺度分离</div><h2>位移趋于零，但比领圈尺度大得越来越多</h2>
<div class="equation">\[\frac{\Sigma_L}{LR}=\frac{e^{L^2/640}}{32768L}\longrightarrow\infty.\]</div>
<p>因此领圈支撑迫使横向热核导数在距离至少 \(\Sigma_{L_j}/2\) 处取值，好路径进入</p>
<div class="equation">\[\exp\!\left[-c\frac{\Sigma_{L_j}^2}{R_j^2}\right]=\exp[-c'e^{L_j^2/320}]\]</div>
<p>这样的超高斯尾。这里的“排出”不是常数量级位移，而是两个趋零尺度之间的严格分离。</p></section>
<section id="s-05"><div class="section-no">05 / 坏路径</div><h2>快速回返事件由明确高斯尾支付</h2>
<p>坏事件是最后 \(R_j^2/64\) 内的布朗振幅超过 \(L_jR_j/16\)。反射估计给出 \(\mathbb P(\mathcal H_t^c)\le4e^{-L_j^2/16}\)。所需指数余量为</p>
<div class="equation">\[\frac1{16}-\frac1{320}-\frac2{1323}=\frac{24497}{423360}>0.\]</div>
<p>它足以支付额外的 \(R_j\) 和壳权差；这个指数来自最后时段长度与允许振幅，不是数值拟合。</p></section>
<section id="s-06"><div class="section-no">06 / 完整两包行</div><h2>四倍安全上界把一包估计送回原始行</h2>
<p>好、坏路径合并后，正包非负上界满足</p>
<div class="equation">\[\sup_{\tau\in I_{R_j}}\mathcal P^-(\tau)\le Ce^{-G_1L_j^2}L_jR_j^5.\]</div>
<p>权重正好换回 \(\Gamma_j\)。再用反演对称性和 \(|F_j^++F_j^-|^2\le2(|F_j^+|^2+|F_j^-|^2)\) 得到主定理，不需要交叉项的符号信息。</p></section>
<section id="s-07"><div class="section-no">07 / 证据等级</div><h2>解析证明、沿用输入、有限复算和文献边界分开</h2>
<p><strong>PROVED：</strong>最近内领圈完整行、相关支撑上的最后时段正剪切位移、好路径超高斯尾、坏路径高斯支付，以及全部周期绕行与两包交叉项的安全控制。</p>
<p><strong>INHERITED：</strong>R0.74F--H 精确光滑周期无外力解族、R0.74L 共同前向概率律、\(B_jR_j^2\) 校准、反演对称性和截止几何。</p>
<p><strong>FINITE：</strong>Python 与独立 Ruby 各 38/38、零差异；图件验证 49/49，23 项校验和通过。有限复算只认证常数、阈值、指数余量和幂次账本，不替代解析证明。</p>
<p><strong>LITERATURE BOUNDARY：</strong>有界七篇一手文献检索没有找到直接给出或否定这里的端点相关、随 \(j\) 一致、指数变平的有符号领圈估计。有限未命中不证明新颖性、优先权或检索完备性。</p></section>
<section id="s-08"><div class="section-no">08 / 开放边界</div><h2>两个局部门槛已闭合，全壳层合成仍未完成</h2>
<ul><li>其余壳层行的合成和 R0.74K 完整有符号条件仍为 OPEN；</li><li>\(\mathfrak C_j\) 与更强的 \(X_j\) 匹配上界仍为 OPEN；</li><li>普适平方根对数端点、任意三维数据的正则性或奇性仍为 OPEN；</li><li>新颖性和优先权判断仍为 OPEN。</li></ul>
<p><strong>NOT CLAY：</strong>本节只推进精确解族内部的领圈分析，不能外推为任意三维 Navier--Stokes 解的定理。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>最后时段排出、尺度分离与好坏路径支付</h2>
<picture><source srcset="/assets/r074m/fig-r074m-nearest-inward-expulsion.svg" type="image/svg+xml"><img src="/assets/r074m/fig-r074m-nearest-inward-expulsion.png" alt="R0.74M final-segment expulsion at the nearest inward collar"></picture>
<p><a href="/assets/r074m/fig-r074m-nearest-inward-expulsion.pdf">下载矢量 PDF</a> · <a href="/assets/r074m/fig-r074m-nearest-inward-expulsion.png">下载 600 dpi PNG</a> · <a href="/assets/r074m/fig-r074m-nearest-inward-expulsion.svg">打开 SVG</a> · <a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/caption.md">图注</a> · <a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/qa-report.md">图件 QA</a> · <a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/plot.py">绘图源码</a> · <a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/validate.py">验证器</a> · <a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/validation.json">49 项验证记录</a> · <a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/manifest.json">图件 manifest</a> · <a href="/figures/r074m/fig-r074m-nearest-inward-expulsion/SHA256SUMS">23 项校验和</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是解析账本，不是 DNS、仿真、布朗样本路径或奇点证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、独立审计、双实现证书与完整图包</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_problem_freeze.md">问题冻结</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_final_segment_expulsion.md">解析主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_nearest_inward_independent_audit.md">独立解析审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_final_source_rebind_audit.md">最终源文件重绑定</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074m_nearest_inward_certificate.py">Python 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074m_nearest_inward_certificate_independent.rb">独立 Ruby 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_nearest_inward_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_nearest_inward_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_primary_literature_boundary.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_report-source.md">审计后中文 reader source</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_reader_source_independent_audit.md">reader source 独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_figure_independent_audit.md">图件独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074m_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74m.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74N</h2><p>合成其余壳层行，直接检查 R0.74K 完整有符号条件；匹配上界与普适端点继续保持开放。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def assert_bilingual_dictionary() -> None:
    path = ROOT / "research/r074m_bilingual_dictionary.md"
    if sha256(path) != "2cdef53de03fa7f032e61943c1664949a2c77aeacde924488105cdbe41954899":
        raise RuntimeError("frozen R0.74M bilingual dictionary drift")
    value = path.read_text(encoding="utf-8")
    for marker in ("最后一小段路径排出", "最近内领圈完整行", "端点相关的领圈支撑", "四倍安全上界", "解族内定理"):
        if marker not in value:
            raise RuntimeError(f"frozen dictionary missing {marker}")


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.78"', 'data-site-version="1.79"', "home version"),
        ('/i18n-en.js?v=1.78', '/i18n-en.js?v=1.79', "home i18n"),
        ('/site-refresh.js?v=1.78.1', '/site-refresh.js?v=1.79.1', "home refresh"),
        ('<strong>v1.78</strong>网页版本', '<strong>v1.79</strong>网页版本', "home version stat"),
        ('<span><strong>214</strong>公开研究笔记</span>', '<span><strong>215</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74L</strong>最新研究节点</span>', '<span><strong>R0.74M</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74L', 'Research topology · R0.1–R0.74M', "topology label"),
        ('href="#r074l">跳到首页 R0.74L 卡片 →', 'href="#r074m">跳到首页 R0.74M 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74L：116 节已公开，92 节完整封存', 'href="#r070a">R0.70A–R0.74M：117 节已公开，93 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74L</span>', '<span class="route-range">R0.69P–R0.74M</span>', "route range"),
        ('<h3>R0.74L：共同前向律、短时钟与主目标领圈</h3>', '<h3>R0.74M：最后时段排出与最近内领圈</h3>', "route title"),
        ('<p class="tree-current-summary">变化的桥族已反演为共同前向律，主目标领圈由短时钟 BV 闭合；最近内领圈仍开放。</p>', '<p class="tree-current-summary">最后一小段布朗路径把典型相关支撑推出最近内领圈；完整壳层合成与匹配上界仍开放。</p>', "route summary"),
        ('<p class="tree-path"><span>R0.72R–R0.74L：</span>', '<p class="tree-path"><span>R0.72R–R0.74M：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74L"', 'aria-label="R0.69P–R0.74M"', "route aria"),
        ('<summary>展开 124 篇公开笔记</summary>', '<summary>展开 125 篇公开笔记</summary>', "route count"),
        ('综述 v1.78 · 2026-09-02', '综述 v1.79 · 2026-09-02', "home footer"),
        ('全站现有 214 篇公开研究笔记', '全站现有 215 篇公开研究笔记', "recap card count"),
    ):
        home = replace_once_or_present(home, old, new, label)

    home, count = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74M 已关闭最近内领圈完整行；下一步合成其余壳层并检查 R0.74K 完整有符号条件。匹配上界与普适端点仍开放。</span></div>',
        home, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74M · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74M｜最后一小段布朗路径，排出了最近内领圈</h2><p class="route-map-intro">相关支撑上的最后时段排出关闭最近内领圈完整行；全壳层合成、匹配上界和普适端点仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74m.pdf">阅读最新 R0.74M 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">215 篇研究笔记总索引</a><a href="#r074m">查看首页 R0.74M 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74M · 117 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>93 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74M</span></div></div></section>'''
    home, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, home, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")

    home = replace_once_or_present(home, '<a class="milestone" href="/notes/r0-74l.html">R0.74L</a>', '<a class="milestone" href="/notes/r0-74l.html">R0.74L</a>\n<a class="milestone" href="/notes/r0-74m.html">R0.74M</a>', "route M link")
    old_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74M</span><span class="tree-state current">下一检查点</span></div><h3>R0.74M 下一接口</h3><p>直接处理最近内领圈的定量正剪切排出；完整有符号条件仍开放。</p></article></div>'
    new_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74N</span><span class="tree-state current">下一检查点</span></div><h3>R0.74N 下一接口</h3><p>合成其余壳层行并检查 R0.74K 完整有符号条件；匹配上界仍开放。</p></article></div>'
    home = replace_once_or_present(home, old_next, new_next, "next route")
    home = replace_once_or_present(home, 'common forward law / short-clock BV / main target collar</p>', 'common forward law / short-clock BV / main target collar → final-segment expulsion / nearest-inward collar</p>', "detailed M route")

    card = r'''          <div class="task-one" id="r074m" data-release="r074m" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74M · 2026-09-02</p><h3>R0.74M｜最后一小段布朗路径，排出了最近内领圈</h3>
            <p>典型相关路径由最后时段正剪切推出领圈，快速回返路径由高斯尾支付；最近内领圈完整行已闭合。</p>
            <p><a href="/notes/r0-74m.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74m.pdf">PDF</a> · <a href="/assets/r074m/fig-r074m-nearest-inward-expulsion.pdf">附图</a></p>
          </div>
'''
    home, removed = re.subn(r'\s*<div class="task-one" id="r074m" data-release="r074m"[\s\S]*?</div>\n', "\n", home, count=1)
    if removed not in (0, 1):
        raise RuntimeError("home M card removal failed")
    if '          <div class="task-one" id="r074l"' not in home:
        raise RuntimeError("home L card anchor missing")
    home = home.replace('          <div class="task-one" id="r074l"', card + '          <div class="task-one" id="r074l"', 1)
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.78"', 'data-site-version="1.79"', "literature version"),
        ('/i18n-en.js?v=1.78', '/i18n-en.js?v=1.79', "literature i18n"),
        ('R0.69P–R0.74L 只列为研究笔记', 'R0.69P–R0.74M 只列为研究笔记', "literature range"),
        ('文献综述 v1.78 · 2026-09-02', '文献综述 v1.79 · 2026-09-02', "literature footer"),
    ):
        page = replace_once_or_present(page, old, new, label)

    route = r'<div class="route-step kept"><header><b>R0.74M</b><strong>最后时段排出与最近内领圈</strong></header><p>相关支撑上的最后一小段布朗路径产生渐近大于领圈尺度的正剪切位移；快速回返路径由明确高斯尾支付。<a href="/notes/r0-74m.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074m-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74N</b><strong>其余壳层行与完整有符号条件</strong></header><p>合成剩余壳层，检查 R0.74K 完整有符号条件；匹配上界与普适端点保持开放。</p></div>'
    if '<b>开放接口 · R0.74N</b>' not in page:
        page, count = re.subn(r'<div class="route-step pause"><header><b>开放接口 · R0\.74M</b>.*?</div>', lambda _: route, page, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074m-boundary">R0.74M 的文献与主张边界</h3><p>有界七篇一手文献检索没有找到直接给出或否定这里的端点相关、随 j 一致、指数变平的有符号最近内领圈估计。Malliavin 密度、Hörmander 光滑性、Markov 桥表示和固定剪切混合结果都缺少至少一个必要结构；有限未命中不证明新颖性、优先权或检索完备性。</p><div class="boundary"><strong>R0.74M 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只关闭精确解族的最近内领圈完整行；其余壳层合成、匹配上界、普适端点与全局正则性仍开放。<a href="/notes/r0-74m.html">阅读完整中文笔记</a>。</p></div>\n'''
    if 'id="r074m-boundary"' not in page:
        if '        <section id="references">' not in page:
            raise RuntimeError("literature references anchor missing")
        page = page.replace('        <section id="references">', boundary + '        <section id="references">', 1)
    write_text(LITERATURE, page)


def route_post_r060_count(home: str) -> int:
    start = home.index('<section class="route-overview"')
    end = home.index('<div class="page-shell">', start)
    slugs = re.findall(r'href="/notes/(r0-[^"]+)\.html"', home[start:end])
    return len(slugs) - slugs.index("r0-61")


def update_accounting() -> None:
    html_count = len(list((PUBLIC / "notes").glob("r0-*.html")))
    pdf_count = len(list((PUBLIC / "notes").glob("r0-*.pdf")))
    if not (PUBLIC / "notes/r0-74m.pdf").exists():
        pdf_count += 1
    post_r060 = route_post_r060_count(HOME.read_text(encoding="utf-8"))

    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {"schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE, "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 140, "latestRecapRelease": "R0.73X", "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-02"})

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
        "latestCompletedRelease": RELEASE,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074n",
        "latestReleaseGate": "tests/r074m-nearest-inward-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074m-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074m-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074m-pdf.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74m.html", render_note())
        assert_bilingual_dictionary()
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74m.html", render_note())
    assert_bilingual_dictionary()
    update_home()
    update_literature()
    update_accounting()
    assert_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "translationRoute": "LOCAL_DIRECT_NO_DGX"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
