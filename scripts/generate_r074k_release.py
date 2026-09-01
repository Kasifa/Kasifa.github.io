#!/usr/bin/env python3
"""Publish frozen R0.74K research assets without changing their claims."""

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
VERSION = "1.77"
RELEASE = "r074k"
CODE = "R0.74K"
NEXT = "R0.74L"
FIGURE_DIR = "fig-r074k-single-inward-collar"
FIGURE_SLUG = "fig-r074k-single-inward-collar"
TITLE = "R0.74K｜自由热指数为何只卡在最近内领圈"
FROZEN_CORE = "a817fb1169b34d6e92911c448cad9c8c59fae138"
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


def replace_once_or_present(value: str, old: str, new: str, label: str) -> str:
    """Apply a deterministic release transition and tolerate its exact result."""
    if new in value:
        return value
    if old in value:
        return replace_once(value, old, new, label)
    raise RuntimeError(f"{label}: neither source nor generated value found")


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
    source = ROOT / "research/figures/r074k" / FIGURE_DIR
    research_mirror = PUBLIC / "figures/r074k" / FIGURE_DIR
    publication_archive = ROOT / "figures/r074k" / FIGURE_DIR
    for target in (research_mirror, publication_archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    asset_dir = PUBLIC / "assets/r074k"
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
        "figureSchemaVersion": "r074k-publication-compat-v1",
        "figureId": frozen.get("figureId") or frozen["figure_id"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74K single-inward-collar reduction figure package.",
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
        "data": [file_record(publication_archive / "source-data.csv", "r074k-source-data-v1")],
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
<meta name="description" content="最近内领圈的自由热指数障碍、常剪切参考尺度与仍开放的真实包桥估计">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74k.html"><link rel="stylesheet" href="/bilingual.css">
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
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74K · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74K · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我审计了 R0.74J 留下的两个匹配上界方向。精确指数核算表明：如果把真实被动包替换为自由热包，所有更深内壳都有严格指数余量，只有最近的 \(j-1\) 壳在一个正体积薄片上仍以 \(536399/8583708672\) 的系数向错误方向增长。因此，所选的归一化周期桥路线必须保留内向 Brownian bridge 与正剪切滞后之间的相关性。本文还给出一个精确充分条件：若对应的有符号包领圈积分不超过 \(\Gamma_jL_jR_j^5\)，则该精确解族的领圈通量恰好饱和 \(P_j^{2/3}\sqrt{1+\log P_j}\) 尺度。这个随机路径估计尚未证明；匹配上界仍为 OPEN。<strong>NOT CLAY.</strong></p>
<div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div>
<div class="stamp"><strong>状态 · R0.74K</strong><p>单一坏领圈：PROVED</p><p>自由热替换：ROUTE OBSTRUCTION</p><p>匹配支付律：INHERITED</p><p>证书 41/41：FINITE</p><p>图件 41/41：FINITE</p><p>真实包桥估计：OPEN</p><p>匹配上界：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 更深内壳</div><h2>除最近一层外，自由热指数都有严格余量</h2>
<p>固定 \(\lambda=63/32\)、\(c_h=15/16\)、\(c_\gamma=8/3969\)，并记 \(d_m=c_h-2^{1-m}/\lambda\)、\(G_m=c_\gamma(1-4^{-m})\)。对每个物理内壳 \(2\le m\le j-1\)，</p>
<div class="equation">\[\boxed{\frac{d_m^2}{132}-G_m\ge\frac{204385}{134120448}>0.}\]</div>
<p>因此，更深内壳只需要把已有桥账本做得更精确，不需要新的指数机制。</p></section>
<section id="s-02"><div class="section-no">02 / 最近内领圈</div><h2>正体积薄片保留错误方向的增长</h2>
<p>在最近的 \(j-1\) 壳，取 \(4033r_j/8064\le x_3\le(4033/8064+1/256)r_j\)、\(|x_1|,|x_2|&lt;r_j/64\)。冻结薄片的归一化体积为 \(1/262144\)，且</p>
<div class="equation">\[\boxed{G_1-\frac{d_{1,\varepsilon}^2}{132}=\frac{536399}{8583708672}>0.}\]</div>
<p><strong>PROVED：</strong>自由热包替换无法关闭这条指定路线。它不是对目标可观测量上界的反例；真实包仍含差分剪切位移与内向桥的相关性。</p></section>
<section id="s-03"><div class="section-no">03 / 参考尺度</div><h2>常剪切参考包固定了正确的领圈量级</h2>
<div class="equation">\[\sup_{x_3}\int M_j(x_2,x_3)\,dx_2\le CL_jR_j,\qquad
\Gamma_j\int_{I_{2R_j}\cap(-\infty,\tau]} |F_{\rm fr}|^2|\partial_2\psi_j^{R_j}|\le C\Gamma_jL_jR_j^5.\]</div>
<p>该绝对值估计给出参考尺度，但没有处理真实包的时间重数。</p></section>
<section id="s-04"><div class="section-no">04 / 条件充分律</div><h2>剩余问题被压缩成一个有符号包领圈估计</h2>
<div class="equation">\[\boxed{\sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+\le C\Gamma_jL_jR_j^5.}\]</div>
<p>若这个仍为 <strong>OPEN</strong> 的真实包假设成立，则</p>
<div class="equation">\[\boxed{\mathfrak C_j\lesssim B_j^2L_jR_j^2.}\]</div>
<p>再与继承下界及 R0.74J 合并，才可得到这一解族上的 \(\mathfrak C_j\asymp P_j^{2/3}\sqrt{1+\log_+P_j}\)。本节没有证明假设，也没有证明匹配上界。</p></section>
<section id="s-05"><div class="section-no">05 / 证据边界</div><h2>解析、继承、有限复算和文献筛查分开</h2>
<p><strong>PROVED：</strong>更深内壳的统一指数余量、最近内领圈的正体积障碍、常剪切参考尺度，以及“真实包假设推出匹配领圈上界”的条件命题。</p>
<p><strong>INHERITED：</strong>R0.74F--H 的精确光滑周期无外力解族、R0.74J 的 \(P_j\asymp B_j^3R_j^3\)，以及 \(\mathfrak C_j\) 的解族下界。</p>
<p><strong>FINITE：</strong>Python 与独立 Ruby 证书各 41/41；图件验证 41/41，25 文件封存通过。它们只核对精确有理算术和条件指数账本，不证明 Brownian bridge 或 PDE 估计。</p>
<p><strong>LITERATURE BOUNDARY：</strong>限定主源筛查覆盖 Bedrossian--Coti Zelati、Albritton--Beekie--Novack、Villringer、Gardner--Liss--Mattingly 与 Liss--Luan。没有一篇被筛论文提供这里所需的尺度依赖、有限时间、有符号领圈估计；有限非命中不证明新颖性或优先权。</p></section>
<section id="s-06"><div class="section-no">06 / 开放边界</div><h2>剩下的是相关路径估计，不是另一个自由热尾界</h2>
<ul><li>归一化桥与 BV 的时间耦合估计仍为 OPEN；</li><li>最近内壳的正剪切排出与充分假设本身仍为 OPEN；</li><li>\(\mathfrak C_j\) 和更强的 \(X_j\) 匹配上界仍为 OPEN；</li><li>普适平方根对数端点、奇点处好尺度与全局正则性仍为 OPEN。</li></ul>
<p><strong>NOT CLAY：</strong>这里只排除一种自由热比较方法并冻结下一条充分条件，不构成千禧年问题结论。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>单一坏内领圈与真实包桥边界</h2>
<picture><source srcset="/assets/r074k/fig-r074k-single-inward-collar.svg" type="image/svg+xml"><img src="/assets/r074k/fig-r074k-single-inward-collar.png" alt="R0.74K single adverse inward collar and true-packet bridge boundary"></picture>
<p><a href="/assets/r074k/fig-r074k-single-inward-collar.pdf">下载矢量 PDF</a> · <a href="/assets/r074k/fig-r074k-single-inward-collar.png">下载 600 dpi PNG</a> · <a href="/assets/r074k/fig-r074k-single-inward-collar.svg">打开 SVG</a> · <a href="/figures/r074k/fig-r074k-single-inward-collar/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074k/fig-r074k-single-inward-collar/caption.md">图注</a> · <a href="/figures/r074k/fig-r074k-single-inward-collar/qa-report.md">图件 QA</a> · <a href="/figures/r074k/fig-r074k-single-inward-collar/plot.py">绘图源码</a> · <a href="/figures/r074k/fig-r074k-single-inward-collar/validate.py">验证器</a> · <a href="/figures/r074k/fig-r074k-single-inward-collar/manifest.json">图件 manifest</a> · <a href="/figures/r074k/fig-r074k-single-inward-collar/validation.json">41 项验证记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/public/figures/r074k/fig-r074k-single-inward-collar">完整 25 文件图包</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是数学依赖图，不是 DNS、仿真、实验数据或奇点证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、双重解析审计、证书与文献边界</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_single_collar_shear_lag_reduction.md">规范主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_inward_tail_independent_audit.md">内向尾独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_collar_reduction_independent_audit.md">领圈约化独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_figure_independent_audit.md">图件独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_final_source_rebind_audit.md">最终源文件重绑定审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_report-source.md">完整报告源</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_single_collar_exponent_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_single_collar_exponent_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074k_single_collar_exponent_certificate.py">Python 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074k_single_collar_exponent_certificate_independent.rb">独立 Ruby 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_primary_literature_boundary.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_primary_literature_independent_audit.md">文献独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074k_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74k.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74L</h2><p>直接证明或否定真实包的归一化桥—BV 领圈估计；若失败，就把最近内领圈的正剪切排出缺口写成精确反例边界。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def assert_bilingual_dictionary() -> None:
    path = ROOT / "research/r074k_bilingual_dictionary.md"
    if sha256(path) != "c83ded2c62979c42b27e3102907edada0248a70d02c870d9177e675ab5966f66":
        raise RuntimeError("frozen R0.74K bilingual dictionary drift")
    value = path.read_text(encoding="utf-8")
    for marker in ("最近内壳", "内领圈", "自由平方高斯指数", "有符号领圈积分", "自由热证明机制不可行"):
        if marker not in value:
            raise RuntimeError(f"frozen dictionary missing {marker}")


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.76"', f'data-site-version="{VERSION}"', "home version"),
        ('/i18n-en.js?v=1.76', f'/i18n-en.js?v={VERSION}', "home i18n"),
        ('/site-refresh.js?v=1.76.1', f'/site-refresh.js?v={VERSION}.1', "home refresh"),
        ('<strong>v1.76</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "home version stat"),
        ('<span><strong>212</strong>公开研究笔记</span>', '<span><strong>213</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74J</strong>最新研究节点</span>', '<span><strong>R0.74K</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74J', 'Research topology · R0.1–R0.74K', "topology label"),
        ('href="#r074j">跳到首页 R0.74J 卡片 →', 'href="#r074k">跳到首页 R0.74K 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74J：114 节已公开，90 节完整封存', 'href="#r070a">R0.70A–R0.74K：115 节已公开，91 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74J</span>', '<span class="route-range">R0.69P–R0.74K</span>', "route range"),
        ('<h3>R0.74J：第五支付壳与匹配完整支付律</h3>', '<h3>R0.74K：最近内领圈与真实包桥边界</h3>', "route title"),
        ('<p class="tree-current-summary">精确解族的第五支付壳给出完整支付下界；与已知上界合并后，Version M 与 F 共享 P_j≈B_j^3R_j^3。普适端点仍开放。</p>', '<p class="tree-current-summary">自由热比较在所有更深内壳有余量，只在最近内领圈失败；真实包的桥—剪切相关估计仍开放。</p>', "route summary"),
        ('<p class="tree-path">适合弱解移动管 → 第五支付壳 → 匹配完整支付 → 解族平方根对数尺度</p>', '<p class="tree-path">第五支付壳 → 匹配完整支付 → 单一坏内领圈 → 真实包桥边界</p>', "route short path"),
        ('<p class="tree-path"><span>R0.72R–R0.74J：</span>', '<p class="tree-path"><span>R0.72R–R0.74K：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74J"', 'aria-label="R0.69P–R0.74K"', "route aria"),
        ('<summary>展开 122 篇公开笔记</summary>', '<summary>展开 123 篇公开笔记</summary>', "route count"),
        ('综述 v1.76 · 2026-09-02', '综述 v1.77 · 2026-09-02', "home footer"),
        ('全站现有 212 篇公开研究笔记', '全站现有 213 篇公开研究笔记', "recap card count"),
    )
    for old, new, label in pairs:
        home = replace_once_or_present(home, old, new, label)

    home, n = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74K 把自由热比较的缺口缩到最近内领圈。下一步直接处理真实包的桥—剪切相关估计；匹配上界与普适端点仍开放。</span></div>',
        home,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74K · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74K｜自由热指数为何只卡在最近内领圈</h2><p class="route-map-intro">更深内壳都有严格指数余量，最近内领圈仍阻断自由热替换。真实包桥估计和匹配上界保持开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74k.pdf">阅读最新 R0.74K 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">213 篇研究笔记总索引</a><a href="#r074k">查看首页 R0.74K 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74K · 115 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>91 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74K</span></div></div></section>'''
    home, n = re.subn(
        r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>',
        lambda _: latest,
        home,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("latest spotlight replacement failed")

    home = replace_once_or_present(
        home,
        '<a class="milestone" href="/notes/r0-74j.html">R0.74J</a>',
        '<a class="milestone" href="/notes/r0-74j.html">R0.74J</a>\n<a class="milestone" href="/notes/r0-74k.html">R0.74K</a>',
        "route K link",
    )
    home = replace_once_or_present(
        home,
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74K</span><span class="tree-state current">下一检查点</span></div><h3>R0.74K 下一接口</h3><p>分别检查 X_j 与领圈通量的匹配上界，并保留真实包的内向桥相关性。</p></article></div>',
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74L</span><span class="tree-state current">下一检查点</span></div><h3>R0.74L 下一接口</h3><p>直接证明或否定真实包的归一化桥—BV 领圈估计。</p></article></div>',
        "next route",
    )
    home = replace_once_or_present(
        home,
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair → suitable-weak moving-tube gate / square-root-log frontier → fifth-shell matching complete payment</p>',
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair → suitable-weak moving-tube gate / square-root-log frontier → fifth-shell matching complete payment → single inward collar / true-packet bridge boundary</p>',
        "detailed K route",
    )
    card = r'''          <div class="task-one" id="r074k" data-release="r074k" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74K · 2026-09-02</p><h3>R0.74K｜自由热指数为何只卡在最近内领圈</h3>
            <p>更深内壳都有严格指数余量；最近内领圈在正体积薄片上仍阻断自由热替换。</p>
            <p><strong>边界：</strong>这里只排除一种比较方法；真实包桥估计、匹配上界和普适端点仍开放，不构成千禧年问题结论。</p>
            <p><a href="/notes/r0-74k.html"><strong>阅读 R0.74K 完整中文笔记 →</strong></a><br><a href="/notes/r0-74k.pdf">下载同步 PDF</a> · <a href="/assets/r074k/fig-r074k-single-inward-collar.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a></p>
          </div>
'''
    home, removed = re.subn(
        r'\s*<div class="task-one" id="r074k" data-release="r074k"[\s\S]*?</div>\n',
        "\n",
        home,
        count=1,
    )
    if removed not in (0, 1):
        raise RuntimeError("home K card removal failed")
    home = replace_once(home, '          <div class="task-one" id="r074j"', card + '          <div class="task-one" id="r074j"', "home K card")
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.76"', 'data-site-version="1.77"', "literature version"),
        ('/i18n-en.js?v=1.76', '/i18n-en.js?v=1.77', "literature i18n"),
        ('R0.69P–R0.74J 只列为研究笔记', 'R0.69P–R0.74K 只列为研究笔记', "literature range"),
        ('文献综述 v1.76 · 2026-09-02', '文献综述 v1.77 · 2026-09-02', "literature footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74K</b><strong>最近内领圈与真实包桥边界</strong></header><p>自由热比较在所有更深内壳有严格指数余量，只在最近内领圈留下正体积障碍；真实包桥—剪切相关估计保持开放。<a href="/notes/r0-74k.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074k-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74L</b><strong>真实包桥—BV 领圈估计</strong></header><p>直接证明或否定尺度依赖、有限时间、有符号的真实包领圈估计。</p></div>'
    if '<b>开放接口 · R0.74L</b>' not in page:
        page, n = re.subn(
            r'<div class="route-step pause"><header><b>开放接口 · R0\.74K</b>.*?</div>',
            lambda _: route,
            page,
            count=1,
            flags=re.S,
        )
        if n != 1:
            raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074k-boundary">R0.74K 的文献与主张边界</h3><p>限定主源审计覆盖 Bedrossian--Coti Zelati、Albritton--Beekie--Novack、Villringer、Gardner--Liss--Mattingly 与 Liss--Luan。现有结果没有提供这里所需的尺度依赖、有限时间、有符号领圈估计；有限非命中不证明新颖性或优先权。</p><div class="boundary"><strong>R0.74K 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只排除指定的自由热替换，并给出一个仍待证明的真实包充分条件；匹配上界、普适端点与正则性仍开放。<a href="/notes/r0-74k.html">阅读完整中文笔记</a>。</p></div>
'''
    if 'id="r074k-boundary"' not in page:
        page = replace_once(page, '        <section id="references">', boundary + '        <section id="references">', "literature K boundary")
    write_text(LITERATURE, page)


def update_accounting() -> None:
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "publicHtmlNoteCount": 213,
        "postR060PublishedNodeCount": 153,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 170,
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
        "publicHtmlNoteCount": 213,
        "publicPdfNoteCount": 170,
        "postR060PublishedNodeCount": 153,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074l",
        "latestReleaseGate": "tests/r074k-single-collar-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074k-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074k-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074k-pdf.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74k.html", render_note())
        assert_bilingual_dictionary()
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74k.html", render_note())
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
