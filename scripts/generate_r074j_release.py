#!/usr/bin/env python3
"""Publish frozen R0.74J research assets without changing their claims."""

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
VERSION = "1.76"
RELEASE = "r074j"
CODE = "R0.74J"
NEXT = "R0.74K"
FIGURE_DIR = "fig-r074j-fifth-shell-payment"
FIGURE_SLUG = "fig-r074j-fifth-shell-payment"
TITLE = "R0.74J｜第五支付壳给出的匹配完整支付律"
FROZEN_CORE = "3f5f9ad68d5d0e8c5998e560f0489731522a4dd5"
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


def replace_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_recap() -> None:
    for path, expected in RECAP_HASHES.items():
        if sha256(path) != expected:
            raise RuntimeError(f"protected recap drift: {path.relative_to(ROOT)}")


def file_record(path: Path, schema: str) -> dict[str, object]:
    return {
        "path": path.name,
        "schema": schema,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def copy_figures() -> None:
    source = ROOT / "research/figures/r074j" / FIGURE_DIR
    research_mirror = PUBLIC / "figures/r074j" / FIGURE_DIR
    publication_archive = ROOT / "figures/r074j" / FIGURE_DIR
    for target in (research_mirror, publication_archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    asset_dir = PUBLIC / "assets/r074j"
    asset_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", asset_dir / f"{FIGURE_SLUG}.{extension}")

    frozen_manifest = source / "manifest.json"
    frozen = json.loads(frozen_manifest.read_text(encoding="utf-8"))
    outputs = []
    for extension in ("svg", "pdf", "png"):
        item = file_record(publication_archive / f"figure.{extension}", f"{extension}-journal-master")
        if extension == "png":
            item["dpi"] = 600
        outputs.append(item)
    manifest = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r074j-publication-compat-v1",
        "figureId": frozen["figureId"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74J fifth-shell matching-payment figure package.",
        "supportedClaim": "See the frozen caption, source data, validation record, and synchronized research note; this wrapper changes no scientific asset.",
        "createdAt": "2026-09-02T00:00:00Z",
        "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": FROZEN_CORE, "dirty": False},
        "computation": {
            "kind": "exact-formula-audit",
            "configuration": "config.json",
            "precision": "frozen exact or deterministic figure package",
            "solver": "none",
            "formalCommand": "use the frozen package command.txt and validate.py",
            "wallTimeSeconds": 1.0,
            "monitoring": {"enabled": False},
        },
        "compute": {
            "host": "local workstation (hostname intentionally omitted)",
            "operatingSystem": "macOS arm64",
            "cpu": "arm64 / local CPU",
            "memoryGiB": 36.0,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {"python": "3.12.13", "packagesLock": "requirements.txt"},
        "data": [file_record(publication_archive / "source-data.csv", "r074j-source-data-v1")],
        "sourceData": [],
        "figure": {"widthMillimetres": 178.0, "heightMillimetres": 88.0, "outputs": outputs},
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "pdfInspected": True,
            "visualQaConfirmed": True,
            "report": "qa-report.md",
        },
        "claimBoundary": {"finiteFigureProvesAnalyticTheorem": False, "globalRegularity": False, "notClay": True},
        "publication": {
            "archiveDirectory": f"public/figures/{RELEASE}/{FIGURE_DIR}",
            "researchArchiveDirectory": f"research/figures/{RELEASE}/{FIGURE_DIR}",
            "directory": f"public/assets/{RELEASE}",
            "fileStem": FIGURE_SLUG,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "releaseSourceCommit": FROZEN_CORE,
            "figurePackageCommit": FROZEN_CORE,
            "assets": [
                {
                    "path": f"public/assets/{RELEASE}/{FIGURE_SLUG}.{item['path'].split('.')[-1]}",
                    "bytes": item["bytes"],
                    "sha256": item["sha256"],
                }
                for item in outputs
            ],
        },
        "provenance": {
            "frozenResearchManifestSha256": sha256(frozen_manifest),
            "compatibilityScope": "publication archive metadata only; frozen research/public packages and all scientific assets are unchanged",
        },
    }
    write_json(publication_archive / "manifest.json", manifest)
    names = sorted(
        path.name
        for path in publication_archive.iterdir()
        if path.is_file() and path.name not in {"SHA256SUMS", ".DS_Store"}
    )
    write_text(
        publication_archive / "SHA256SUMS",
        "".join(f"{sha256(publication_archive / name)}  {name}\n" for name in names),
    )


def render_note() -> str:
    page = r'''<!doctype html>
<html lang="zh-CN" data-site-version="__VERSION__">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="精确光滑周期无外力解族上的第五支付壳下界、匹配完整支付律与平方根对数尺度">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74j.html"><link rel="stylesheet" href="/bilingual.css">
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
@media print{:root{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}.top{display:none}body{background:#fff;font-size:9.6pt;line-height:1.56}main{width:auto}.hero{padding-top:0}.hero-inner{grid-template-columns:1fr 220px}h2{margin:2rem 0 .7rem}a{color:inherit;text-decoration:none}.equation,.stamp{break-inside:avoid}}
</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74J · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74J · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我重新核对了 R0.74F--H 构造并在 R0.74I 中再次分析的精确、光滑、周期、无外力解族。在支付半径 \(2R_j\) 的第五壳，一个固定盒中的背景剪切在整个支付时间窗内保持至少 \(1/2\)，所以非负的速度三次项给出 \(8e^{-8}B_j^3R_j^3\) 的下界。与 R0.74G 已证明的上界合并后，Version M 和 Version F 的共同完整支付量满足 \(P_j\asymp B_j^3R_j^3\)，并且 \(\log P_j/L_j^2\to3/320\)。这是一个精确解族上的匹配支付律，不是普适平方根对数端点上界；它没有给出 \(X_j\) 或 \(\mathfrak C_j\) 的匹配上界，也没有在可能奇点处制造小量条件。 <strong>NOT CLAY.</strong></p>
<div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div>
<div class="stamp"><strong>状态 · R0.74J</strong><p>第五壳下界：PROVED</p><p>匹配完整支付律：PROVED</p><p>R0.74G 上界：INHERITED</p><p>证书 38/38：FINITE</p><p>独立复算 287 字段：FINITE</p><p>图件 79/79：FINITE</p><p>普适端点上界：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 第五支付壳</div><h2>固定盒给出非负三次量下界</h2>
<p>取 \(z_{0,j}=(65R_j^2,0)\)、\(A_5(2R_j)=\{64R_j\le |x|&lt;128R_j\}\) 和 \(\Gamma_5=e^{-8}\)。对所有充分大的 \(j\)，选定盒完全落在第五壳内，背景剪切在支付窗内至少为 \(1/2\)。因此</p>
<div class="equation">\[\boxed{\mathcal G_u(z_{0,j},2R_j;1)\ge 8e^{-8}B_j^3R_j^3.}\]</div>
<p>这里使用的是非负速度三次项。下界来自解析证明，不来自有限采样或仿真。</p></section>
<section id="s-02"><div class="section-no">02 / 匹配支付</div><h2>Version M 与 Version F 共享同一完整支付量</h2>
<p>把上式与 R0.74G 的匹配上界及精确零 frame 恒等式合并，得到</p>
<div class="equation">\[\boxed{8e^{-8}B_j^3R_j^3\le P_j:=P_{R_j}^M=P_{R_j}^F\le CB_j^3R_j^3.}\]</div>
<p><strong>INHERITED：</strong>解族、零 frame 恒等式、\(\beta_j=B_jR_j^2\to1/128\) 与上界来自 R0.74F--H 和 R0.74G；本节新证明的是第五壳下界及其与这些结果的精确合并。</p></section>
<section id="s-03"><div class="section-no">03 / 对数率</div><h2>支付增长率与稀疏系数都固定下来</h2>
<div class="equation">\[\boxed{\frac{\log P_j}{L_j^2}\longrightarrow\frac3{320},\qquad \log\frac{P_{j+1}}{P_j}=\frac9{320}L_j^2+O(1).}\]</div>
<p>第一个常数是完整支付的对数率；第二个常数记录实际支付序列的 lacunarity。二者只针对这一精确解族。</p></section>
<section id="s-04"><div class="section-no">04 / 平方根对数尺度</div><h2>匹配支付解释了解族上的端点量级</h2>
<div class="equation">\[\boxed{P_j^{2/3}\sqrt{1+\log_+P_j}\asymp B_j^2L_jR_j^2.}\]</div>
<p>该等价关系解释了 R0.74I 中出现的平方根对数尺度，但它不是对任意解、任意尺度成立的普适端点上界。</p></section>
<section id="s-05"><div class="section-no">05 / 证据分层</div><h2>解析证明、继承结果和有限复算分别记录</h2>
<p><strong>PROVED：</strong>周期热平台下界、第五壳中的固定盒、非负速度三次下界、两种版本的匹配完整支付律、\(3/320\) 对数率与 \(9/320\) 稀疏系数。</p>
<p><strong>INHERITED：</strong>R0.74F--H 精确解族、零 frame 恒等式、振幅校准与 R0.74G 的匹配上界。</p>
<p><strong>FINITE：</strong>Python 证书 38/38 并逐字节复现冻结 JSON；独立 Ruby 复算 38/38，比较 287 个终端字段且零差异。图件 validator 79/79，24 文件封存通过。有限证书只核对精确算术和图件，不证明热方程或连续定理。</p></section>
<section id="s-06"><div class="section-no">06 / 文献边界</div><h2>四篇主源只限定先例与非命中范围</h2>
<p><strong>LITERATURE BOUNDARY：</strong>限定检索覆盖 Yang（2022）、Vasseur--Yang（2021）、Lei--Ren（2024）和 Wang--Wu--Zhou（2019）。移动柱、部分正则与一尺度 epsilon 机制已有先例。</p>
<p>这四篇论文中没有找到相同的匹配完整支付定理；有限非命中不证明新颖性或优先权。</p></section>
<section id="s-07"><div class="section-no">07 / 开放边界</div><h2>匹配支付不等于普适端点或正则性</h2>
<ul><li>普适平方根对数端点上界仍为 OPEN；</li><li>\(X_j\) 与 \(\mathfrak C_j\) 的匹配上界仍未证明；</li><li>从支付到可容许性、从外壳到移动核心的控制仍开放；</li><li>可能奇点处的给定好尺度定理仍开放；</li><li>全局正则性、奇点排除、新颖性与优先权均未证明。</li></ul>
<p><strong>NOT CLAY：</strong>这是一条精确解族上的匹配支付律，不是 Clay 千禧年问题的解答。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>第五壳下界与匹配支付链</h2>
<picture><source srcset="/assets/r074j/fig-r074j-fifth-shell-payment.svg" type="image/svg+xml"><img src="/assets/r074j/fig-r074j-fifth-shell-payment.png" alt="R0.74J fifth-shell lower bound and matching complete-payment law"></picture>
<p><a href="/assets/r074j/fig-r074j-fifth-shell-payment.pdf">下载矢量 PDF</a> · <a href="/assets/r074j/fig-r074j-fifth-shell-payment.png">下载 600 dpi PNG</a> · <a href="/assets/r074j/fig-r074j-fifth-shell-payment.svg">打开 SVG</a> · <a href="/figures/r074j/fig-r074j-fifth-shell-payment/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074j/fig-r074j-fifth-shell-payment/caption.md">图注</a> · <a href="/figures/r074j/fig-r074j-fifth-shell-payment/qa-report.md">图件 QA</a> · <a href="/figures/r074j/fig-r074j-fifth-shell-payment/plot.py">绘图源码</a> · <a href="/figures/r074j/fig-r074j-fifth-shell-payment/validate.py">验证器</a> · <a href="/figures/r074j/fig-r074j-fifth-shell-payment/manifest.json">图件 manifest</a> · <a href="/figures/r074j/fig-r074j-fifth-shell-payment/validation.json">79 项验证记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/public/figures/r074j/fig-r074j-fifth-shell-payment">完整 24 文件图包</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是解析关系图，不是 DNS、数值仿真、实验数据或奇点证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、解析审计、精确证书与文献边界</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_matching_payment_law.md">规范主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_heat_platform_independent_audit.md">热平台独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_complete_payment_ledger_independent_audit.md">完整支付独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_final_source_rebind_audit.md">最终源文件重绑定审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_report-source.md">完整报告源</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_matching_payment_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_matching_payment_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074j_matching_payment_certificate.py">Python 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074j_matching_payment_certificate_independent.rb">独立 Ruby 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_primary_literature_boundary.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_primary_literature_independent_audit.md">文献独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074j_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74j.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74K</h2><p>分别检查 \(X_j\) 与 \(\mathfrak C_j\) 的匹配上界，并保留精确包的内向桥与剪切滞后；在获得真实包估计前不外推普适端点或正则性。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def assert_bilingual_dictionary() -> None:
    path = ROOT / "research/r074j_bilingual_dictionary.md"
    if sha256(path) != "3ea788eeb84cd82ae24dd6c9584223b8caef5d927eea8b3a0aef348c81991a8b":
        raise RuntimeError("frozen R0.74J bilingual dictionary drift")
    value = path.read_text(encoding="utf-8")
    for marker in ("第五支付壳", "匹配完整支付律", "PROVED", "INHERITED", "FINITE", "OPEN", "NOT CLAY"):
        if marker not in value:
            raise RuntimeError(f"frozen dictionary missing {marker}")


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.75"', f'data-site-version="{VERSION}"', "home version"),
        ('/i18n-en.js?v=1.75', f'/i18n-en.js?v={VERSION}', "home i18n"),
        ('/site-refresh.js?v=1.75.1', f'/site-refresh.js?v={VERSION}.1', "home refresh"),
        ('<strong>v1.75</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "home version stat"),
        ('<span><strong>211</strong>公开研究笔记</span>', '<span><strong>212</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74I</strong>最新研究节点</span>', '<span><strong>R0.74J</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74I', 'Research topology · R0.1–R0.74J', "topology label"),
        ('href="#r074i">跳到首页 R0.74I 卡片 →', 'href="#r074j">跳到首页 R0.74J 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74I：113 节已公开，89 节完整封存', 'href="#r070a">R0.70A–R0.74J：114 节已公开，90 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74I</span>', '<span class="route-range">R0.69P–R0.74J</span>', "route range"),
        ('<h3>R0.74I：适合弱解移动管门与平方根对数边界</h3>', '<h3>R0.74J：第五支付壳与匹配完整支付律</h3>', "route title"),
        ('<p class="tree-current-summary">Version M 已推进到适合弱解；给定尺度上的小移动能量进入既有固定柱 epsilon 判据。所有 gamma&lt;1/2 的对数修复被排除，端点仍开放。</p>', '<p class="tree-current-summary">精确解族的第五支付壳给出完整支付下界；与已知上界合并后，Version M 与 F 共享 P_j≈B_j^3R_j^3。普适端点仍开放。</p>', "route summary"),
        ('<p class="tree-path">环带通量修复 → 适合弱解移动管 → 单尺度 epsilon 门 → 平方根对数边界</p>', '<p class="tree-path">适合弱解移动管 → 第五支付壳 → 匹配完整支付 → 解族平方根对数尺度</p>', "route short path"),
        ('<p class="tree-path"><span>R0.72R–R0.74I：</span>', '<p class="tree-path"><span>R0.72R–R0.74J：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74I"', 'aria-label="R0.69P–R0.74J"', "route aria"),
        ('<summary>展开 121 篇公开笔记</summary>', '<summary>展开 122 篇公开笔记</summary>', "route count"),
        ('综述 v1.75 · 2026-09-02', '综述 v1.76 · 2026-09-02', "home footer"),
        ('全站现有 211 篇公开研究笔记', '全站现有 212 篇公开研究笔记', "recap card count"),
    )
    for old, new, label in pairs:
        home = replace_once(home, old, new, label)

    home, n = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74J 已在精确解族上证明匹配完整支付律。下一步要分别处理 X_j 与领圈通量的匹配上界，并保留真实包的桥相关性；普适端点和奇点处小量仍开放。</span></div>',
        home,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74J · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74J｜第五支付壳与匹配完整支付律</h2><p class="route-map-intro">第五支付壳给出精确解族的完整支付下界；与已知上界合并后，Version M 与 F 共享匹配量级。普适平方根对数端点仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74j.pdf">阅读最新 R0.74J 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">212 篇研究笔记总索引</a><a href="#r074j">查看首页 R0.74J 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74J · 114 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>90 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74J</span></div></div></section>'''
    home, n = re.subn(
        r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>',
        lambda _: latest,
        home,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("latest spotlight replacement failed")

    home = replace_once(
        home,
        '<a class="milestone" href="/notes/r0-74i.html">R0.74I</a>',
        '<a class="milestone" href="/notes/r0-74i.html">R0.74I</a>\n<a class="milestone" href="/notes/r0-74j.html">R0.74J</a>',
        "route J link",
    )
    home = replace_once(
        home,
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74J</span><span class="tree-state current">下一检查点</span></div><h3>R0.74J 下一接口</h3><p>检查移动能量小量的尺度传播，并分别处理平方根对数端点上界与匹配支付下界。</p></article></div>',
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74K</span><span class="tree-state current">下一检查点</span></div><h3>R0.74K 下一接口</h3><p>分别检查 X_j 与领圈通量的匹配上界，并保留真实包的内向桥相关性。</p></article></div>',
        "next route",
    )
    home = home.replace(
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair → suitable-weak moving-tube gate / square-root-log frontier</p>',
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair → suitable-weak moving-tube gate / square-root-log frontier → fifth-shell matching complete payment</p>',
        1,
    )
    card = r'''          <div class="task-one" id="r074j" data-release="r074j" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74J · 2026-09-02</p><h3>R0.74J｜第五支付壳给出的匹配完整支付律</h3>
            <p>第五支付壳给出 \(8e^{-8}B_j^3R_j^3\) 下界；与已有上界合并后，精确解族满足 \(P_j\asymp B_j^3R_j^3\)。</p>
            <p><strong>边界：</strong>只证明解族上的匹配支付；普适端点、\(X_j\) 与领圈通量的匹配上界仍开放。非 Clay 结论。</p>
            <p><a href="/notes/r0-74j.html"><strong>阅读 R0.74J 完整中文笔记 →</strong></a><br><a href="/notes/r0-74j.pdf">下载同步 PDF</a> · <a href="/assets/r074j/fig-r074j-fifth-shell-payment.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a></p>
          </div>
'''
    home = replace_once(home, '          <div class="task-one" id="r074i"', card + '          <div class="task-one" id="r074i"', "home J card")
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.75"', 'data-site-version="1.76"', "literature version"),
        ('/i18n-en.js?v=1.75', '/i18n-en.js?v=1.76', "literature i18n"),
        ('R0.69P–R0.74I 只列为研究笔记', 'R0.69P–R0.74J 只列为研究笔记', "literature range"),
        ('文献综述 v1.75 · 2026-09-02', '文献综述 v1.76 · 2026-09-02', "literature footer"),
    ):
        page = replace_once(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74J</b><strong>第五支付壳与匹配完整支付律</strong></header><p>精确解族的第五支付壳给出完整支付下界；与 R0.74G 上界合并后，Version M 与 F 的完整支付量都满足 \(P_j\asymp B_j^3R_j^3\)。这不是普适端点上界。<a href="/notes/r0-74j.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074j-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74K</b><strong>两个匹配上界方向</strong></header><p>分别检查 \(X_j\) 与领圈通量的匹配上界，并保留真实包的内向桥相关性。</p></div>'
    page, n = re.subn(
        r'<div class="route-step pause"><header><b>开放接口 · R0\.74J</b>.*?</div>',
        lambda _: route,
        page,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074j-boundary">R0.74J 的文献与主张边界</h3><p>限定主源审计覆盖 Yang、Vasseur--Yang、Lei--Ren 与 Wang--Wu--Zhou。移动柱、部分正则与一尺度 epsilon 机制已有先例。四篇论文中没有找到相同的匹配完整支付定理，但 finite non-hit 不证明新颖性或优先权。</p><div class="boundary"><strong>R0.74J 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只在精确解族上闭合完整支付量级；普适平方根对数端点、两个可观测量的匹配上界与奇点处小量仍开放。<a href="/notes/r0-74j.html">阅读完整中文笔记</a>。</p></div>
'''
    page = replace_once(page, '        <section id="references">', boundary + '        <section id="references">', "literature J boundary")
    write_text(LITERATURE, page)


def update_accounting() -> None:
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "publicHtmlNoteCount": 212,
        "postR060PublishedNodeCount": 152,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 169,
        "publishedDate": "2026-09-02",
    })
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
        "publicHtmlNoteCount": 212,
        "publicPdfNoteCount": 169,
        "postR060PublishedNodeCount": 152,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074k",
        "latestReleaseGate": "tests/r074j-matching-payment-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074j-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074j-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074j-pdf.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74j.html", render_note())
        assert_bilingual_dictionary()
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74j.html", render_note())
    assert_bilingual_dictionary()
    update_home()
    update_literature()
    update_accounting()
    assert_recap()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "siteVersion": VERSION,
        "recapPreserved": True,
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
