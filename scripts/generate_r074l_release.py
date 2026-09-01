#!/usr/bin/env python3
"""Publish frozen R0.74L research assets without changing their claims."""

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
VERSION = "1.78"
RELEASE = "r074l"
CODE = "R0.74L"
NEXT = "R0.74M"
FIGURE_DIR = "fig-r074l-forward-clock-bv"
FIGURE_SLUG = "fig-r074l-forward-clock-bv"
TITLE = "R0.74L｜变化的桥族、短时钟，和一个闭合的主领圈"
FROZEN_CORE = "1cec35fb40aed23eb2c684a93fcda3eab7175ad9"
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
    source = ROOT / "research/figures/r074l" / FIGURE_DIR
    research_mirror = PUBLIC / "figures/r074l" / FIGURE_DIR
    publication_archive = ROOT / "figures/r074l" / FIGURE_DIR
    for target in (research_mirror, publication_archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    asset_dir = PUBLIC / "assets/r074l"
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
        "figureSchemaVersion": "r074l-publication-compat-v1",
        "figureId": frozen.get("figureId") or frozen["figure_id"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74L common-forward-law and short-clock BV figure package.",
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
        "data": [file_record(publication_archive / "source-data.csv", "r074l-source-data-v1")],
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
        "claimBoundary": {"mainTargetCollar": "PROVED", "nearestInwardCollar": "OPEN", "finiteFigureProvesAnalyticTheorem": False, "globalRegularity": False, "notClay": True},
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


def render_note_legacy_k() -> str:
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
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74L · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74L · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我审计了 R0.74J 留下的两个匹配上界方向。精确指数核算表明：如果把真实被动包替换为自由热包，所有更深内壳都有严格指数余量，只有最近的 \(j-1\) 壳在一个正体积薄片上仍以 \(536399/8583708672\) 的系数向错误方向增长。因此，所选的归一化周期桥路线必须保留内向 Brownian bridge 与正剪切滞后之间的相关性。本文还给出一个精确充分条件：若对应的有符号包领圈积分不超过 \(\Gamma_jL_jR_j^5\)，则该精确解族的领圈通量恰好饱和 \(P_j^{2/3}\sqrt{1+\log P_j}\) 尺度。这个随机路径估计尚未证明；匹配上界仍为 OPEN。<strong>NOT CLAY.</strong></p>
<div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div>
<div class="stamp"><strong>状态 · R0.74L</strong><p>单一坏领圈：PROVED</p><p>自由热替换：ROUTE OBSTRUCTION</p><p>匹配支付律：INHERITED</p><p>证书 41/41：FINITE</p><p>图件 41/41：FINITE</p><p>真实包桥估计：OPEN</p><p>匹配上界：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
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
<picture><source srcset="/assets/r074l/fig-r074l-single-inward-collar.svg" type="image/svg+xml"><img src="/assets/r074l/fig-r074l-single-inward-collar.png" alt="R0.74L single adverse inward collar and true-packet bridge boundary"></picture>
<p><a href="/assets/r074l/fig-r074l-single-inward-collar.pdf">下载矢量 PDF</a> · <a href="/assets/r074l/fig-r074l-single-inward-collar.png">下载 600 dpi PNG</a> · <a href="/assets/r074l/fig-r074l-single-inward-collar.svg">打开 SVG</a> · <a href="/figures/r074l/fig-r074l-single-inward-collar/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074l/fig-r074l-single-inward-collar/caption.md">图注</a> · <a href="/figures/r074l/fig-r074l-single-inward-collar/qa-report.md">图件 QA</a> · <a href="/figures/r074l/fig-r074l-single-inward-collar/plot.py">绘图源码</a> · <a href="/figures/r074l/fig-r074l-single-inward-collar/validate.py">验证器</a> · <a href="/figures/r074l/fig-r074l-single-inward-collar/manifest.json">图件 manifest</a> · <a href="/figures/r074l/fig-r074l-single-inward-collar/validation.json">41 项验证记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/public/figures/r074l/fig-r074l-single-inward-collar">完整 25 文件图包</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是数学依赖图，不是 DNS、仿真、实验数据或奇点证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、双重解析审计、证书与文献边界</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_single_collar_shear_lag_reduction.md">规范主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_inward_tail_independent_audit.md">内向尾独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_collar_reduction_independent_audit.md">领圈约化独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_figure_independent_audit.md">图件独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_final_source_rebind_audit.md">最终源文件重绑定审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_report-source.md">完整报告源</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_single_collar_exponent_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_single_collar_exponent_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074l_single_collar_exponent_certificate.py">Python 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074l_single_collar_exponent_certificate_independent.rb">独立 Ruby 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_primary_literature_boundary.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_primary_literature_independent_audit.md">文献独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74k.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74L</h2><p>直接证明或否定真实包的归一化桥—BV 领圈估计；若失败，就把最近内领圈的正剪切排出缺口写成精确反例边界。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def render_note() -> str:
    page = r'''<!doctype html>
<html lang="zh-CN" data-site-version="__VERSION__">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="把变化的周期桥族反演为共同前向律，并用短时钟 BV 关闭精确解族的主目标领圈">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74l.html"><link rel="stylesheet" href="/bilingual.css">
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
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74L · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74L · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节仍然没有解决三维 Navier--Stokes 千禧年问题。R0.74K 把真实被动包的领圈上界拆成主目标领圈的时间重数和最近内领圈的正剪切排出；我在本节只处理第一项。结果是：主目标领圈所需的归一化周期桥上界已经证明，并通过独立数学审计；最近内领圈仍然 OPEN。核心不是把真实包近似成自由热包，而是先把随终端时刻变化的后向桥族精确反演成同一个前向布朗概率律，再利用真实中心只穿过一个很短的“剪切时钟”区间。<strong>NOT CLAY.</strong></p>
<div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div>
<div class="stamp"><strong>状态 · R0.74L</strong><p>共同前向律：PROVED</p><p>主目标领圈：PROVED</p><p>证书 24/24：FINITE</p><p>图件 45/45：FINITE</p><p>最近内领圈：OPEN</p><p>完整有符号条件：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 主结论</div><h2>主目标领圈的时间重数已经闭合</h2>
<p>保留 R0.74F--K 的精确光滑、周期、无外力解族。对正包 Jensen 上界量 \(\mathscr B_j\)，本节证明</p>
<div class="equation">\[\boxed{\sup_{\tau\in I_{R_j}}\mathscr B_j(\tau)\le C L_jR_j^5.}\]</div>
<p>由包反演对称性和 \(|F_j|^2\le2(|F_j^+|^2+|F_j^-|^2)\)，得到</p>
<div class="equation">\[\boxed{\text{main target collar}\le C\Gamma_jL_jR_j^5.}\]</div>
<p>这里保留全部周期绕行，也没有使用正负包之间的抵消。</p></section>
<section id="s-02"><div class="section-no">02 / 共同概率律</div><h2>先积分，再把变化的桥族精确反演</h2>
<p>后向桥依赖终端时刻，不能把不同终端的桥当成同一条路径来微分。我先对终点变量积分，再利用周期热核对称性，得到同一概率空间上的前向过程</p>
<div class="equation">\[X_0\sim K_{R_j^2},\qquad dX_t=\sqrt2\,dW_t,\qquad q_\omega(t)=q_{\rm pre}+B_j\int_0^t\theta_j(s,h_j+X_s)\,ds.\]</div>
<p>在正剪切区内，\(dq_\omega=B_j\theta_j(t,h_j+X_t)dt\) 只是普通路径积分恒等式，不再是对变化桥族的形式微分。</p></section>
<section id="s-03"><div class="section-no">03 / 坏路径</div><h2>过渡区附近的稀有路径多付一个 \(R_j\)</h2>
<p>对 \(j\ge14\)，坏事件满足 \(\mathbb P(\mathcal G^c)\le4e^{-A L_j^2}\)，其中</p>
<div class="equation">\[A=\frac{4876875}{1476395008},\qquad A-\frac1{320}=\frac{1315703}{7381975040}>0.\]</div>
<p>结合 \(R_j=e^{-L_j^2/320}\)，严格余量足以支付额外的 \(R_j\)；即使只用粗点态领圈界，坏路径仍贡献 \(O(L_jR_j^5)\)。</p></section>
<section id="s-04"><div class="section-no">04 / 短时钟与 BV</div><h2>好路径只穿过一个短时钟区间</h2>
<p>好事件上 \(\theta_j(t,h_j+X_t)>7/8\)。目标领圈在时钟变量中的支撑长度为 \(O(L_jR_j)\)，对应物理时间只有 \(O(L_jR_j^3)\)。固定切片加厚后的 BV 界为</p>
<div class="equation">\[\sup_{x_3}\int M_j^\sharp(x_2,x_3)\,dx_2\le C L_jR_j.\]</div>
<p>小振荡路径冻结到进入时刻；模量失效路径的粗界由 \(\exp[-c/(L_jR_j)]\) 吸收。最终幂次账本为</p>
<div class="equation">\[R_j^6\cdot B_j^{-1}\cdot R_j^{-1}\cdot R_j^{-3}\cdot(L_jR_j)\le C L_jR_j^5.\]</div></section>
<section id="s-05"><div class="section-no">05 / 证据边界</div><h2>解析证明、继承输入、有限复算与文献筛查分开</h2>
<p><strong>PROVED：</strong>周期折叠、共同前向律、坏路径指数余量、加厚固定切片 BV、逆时钟停止时刻、布朗模量，以及主目标领圈两包绝对上界。</p>
<p><strong>INHERITED：</strong>R0.74F--K 精确解族、\(B_jR_j^2\) 的大 \(j\) 校准、包反演对称性与目标领圈几何。</p>
<p><strong>FINITE：</strong>Python 与独立 Ruby 各 24/24、零差异；图件验证 45/45，22/22 校验和通过。它们只认证有限常数、幂次和图件，不替代桥反演、停止时刻或 BV 解析证明。</p>
<p><strong>LITERATURE BOUNDARY：</strong>有界十篇主源审计没有找到直接给出或否定本节周期桥--短时钟 BV 估计的定理。边缘投影与经典 Aronson 捷径因算子不匹配而未使用；有限未命中不证明新颖性或优先权。</p></section>
<section id="s-06"><div class="section-no">06 / 开放边界</div><h2>两个随机门槛只关闭了一个</h2>
<ul><li>最近内领圈的定量正剪切排出仍为 OPEN；</li><li>R0.74K 的完整有符号包条件仍为 OPEN；</li><li>\(\mathfrak C_j\) 与更强的 \(X_j\) 匹配上界仍为 OPEN；</li><li>普适平方根对数端点、奇点处好尺度与全局正则性仍为 OPEN。</li></ul>
<p><strong>NOT CLAY：</strong>本节只关闭精确解族的主目标领圈，不构成任意三维解的正则性或奇性结论。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>共同前向律、短时钟与主领圈幂次</h2>
<picture><source srcset="/assets/r074l/fig-r074l-forward-clock-bv.svg" type="image/svg+xml"><img src="/assets/r074l/fig-r074l-forward-clock-bv.png" alt="R0.74L common forward law, short-clock BV, and main target collar ledger"></picture>
<p><a href="/assets/r074l/fig-r074l-forward-clock-bv.pdf">下载矢量 PDF</a> · <a href="/assets/r074l/fig-r074l-forward-clock-bv.png">下载 600 dpi PNG</a> · <a href="/assets/r074l/fig-r074l-forward-clock-bv.svg">打开 SVG</a> · <a href="/figures/r074l/fig-r074l-forward-clock-bv/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074l/fig-r074l-forward-clock-bv/caption.md">图注</a> · <a href="/figures/r074l/fig-r074l-forward-clock-bv/qa-report.md">图件 QA</a> · <a href="/figures/r074l/fig-r074l-forward-clock-bv/plot.py">绘图源码</a> · <a href="/figures/r074l/fig-r074l-forward-clock-bv/validate.py">验证器</a> · <a href="/figures/r074l/fig-r074l-forward-clock-bv/manifest.json">图件 manifest</a> · <a href="/figures/r074l/fig-r074l-forward-clock-bv/SHA256SUMS">22 项校验和</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_figure_independent_audit.md">图件独立审计</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是解析账本，不是 DNS、仿真、随机采样数据或奇点证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、独立审计、证书与文献边界</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_problem_freeze.md">问题冻结</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_forward_bridge_bv_reduction.md">解析主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_main_collar_independent_audit.md">独立解析审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_final_source_rebind_audit.md">最终源文件重绑定</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074l_main_collar_certificate.py">Python 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074l_main_collar_certificate_independent.rb">独立 Ruby 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_main_collar_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_main_collar_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_primary_literature_audit.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_report-source.md">完整报告源</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074l_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74l.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74M</h2><p>直接处理最近内领圈的正剪切排出；若不能得到定量驱逐，就把精确失败边界冻结为反例。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def assert_bilingual_dictionary() -> None:
    path = ROOT / "research/r074l_bilingual_dictionary.md"
    if sha256(path) != "e31c70998ac43d7f869e52a03c41e4e64f71d2fbdb4061f6abfb852fbd2e1876":
        raise RuntimeError("frozen R0.74L bilingual dictionary drift")
    value = path.read_text(encoding="utf-8")
    for marker in ("随终端时刻变化的桥族", "共同前向概率律", "短时钟支撑", "主目标领圈", "最近内领圈"):
        if marker not in value:
            raise RuntimeError(f"frozen dictionary missing {marker}")


def update_home_legacy_k() -> None:
    home = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.76"', f'data-site-version="{VERSION}"', "home version"),
        ('/i18n-en.js?v=1.76', f'/i18n-en.js?v={VERSION}', "home i18n"),
        ('/site-refresh.js?v=1.76.1', f'/site-refresh.js?v={VERSION}.1', "home refresh"),
        ('<strong>v1.76</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "home version stat"),
        ('<span><strong>212</strong>公开研究笔记</span>', '<span><strong>213</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74J</strong>最新研究节点</span>', '<span><strong>R0.74L</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74J', 'Research topology · R0.1–R0.74L', "topology label"),
        ('href="#r074j">跳到首页 R0.74J 卡片 →', 'href="#r074l">跳到首页 R0.74L 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74J：114 节已公开，90 节完整封存', 'href="#r070a">R0.70A–R0.74L：115 节已公开，91 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74J</span>', '<span class="route-range">R0.69P–R0.74L</span>', "route range"),
        ('<h3>R0.74J：第五支付壳与匹配完整支付律</h3>', '<h3>R0.74L：最近内领圈与真实包桥边界</h3>', "route title"),
        ('<p class="tree-current-summary">精确解族的第五支付壳给出完整支付下界；与已知上界合并后，Version M 与 F 共享 P_j≈B_j^3R_j^3。普适端点仍开放。</p>', '<p class="tree-current-summary">自由热比较在所有更深内壳有余量，只在最近内领圈失败；真实包的桥—剪切相关估计仍开放。</p>', "route summary"),
        ('<p class="tree-path">适合弱解移动管 → 第五支付壳 → 匹配完整支付 → 解族平方根对数尺度</p>', '<p class="tree-path">第五支付壳 → 匹配完整支付 → 单一坏内领圈 → 真实包桥边界</p>', "route short path"),
        ('<p class="tree-path"><span>R0.72R–R0.74J：</span>', '<p class="tree-path"><span>R0.72R–R0.74L：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74J"', 'aria-label="R0.69P–R0.74L"', "route aria"),
        ('<summary>展开 122 篇公开笔记</summary>', '<summary>展开 123 篇公开笔记</summary>', "route count"),
        ('综述 v1.76 · 2026-09-02', '综述 v1.77 · 2026-09-02', "home footer"),
        ('全站现有 212 篇公开研究笔记', '全站现有 213 篇公开研究笔记', "recap card count"),
    )
    for old, new, label in pairs:
        home = replace_once_or_present(home, old, new, label)

    home, n = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74L 把自由热比较的缺口缩到最近内领圈。下一步直接处理真实包的桥—剪切相关估计；匹配上界与普适端点仍开放。</span></div>',
        home,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74L · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74L｜自由热指数为何只卡在最近内领圈</h2><p class="route-map-intro">更深内壳都有严格指数余量，最近内领圈仍阻断自由热替换。真实包桥估计和匹配上界保持开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74k.pdf">阅读最新 R0.74L 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">213 篇研究笔记总索引</a><a href="#r074l">查看首页 R0.74L 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74L · 115 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>91 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74L</span></div></div></section>'''
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
        '<a class="milestone" href="/notes/r0-74j.html">R0.74J</a>\n<a class="milestone" href="/notes/r0-74k.html">R0.74L</a>',
        "route K link",
    )
    home = replace_once_or_present(
        home,
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74L</span><span class="tree-state current">下一检查点</span></div><h3>R0.74L 下一接口</h3><p>分别检查 X_j 与领圈通量的匹配上界，并保留真实包的内向桥相关性。</p></article></div>',
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74L</span><span class="tree-state current">下一检查点</span></div><h3>R0.74L 下一接口</h3><p>直接证明或否定真实包的归一化桥—BV 领圈估计。</p></article></div>',
        "next route",
    )
    home = replace_once_or_present(
        home,
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair → suitable-weak moving-tube gate / square-root-log frontier → fifth-shell matching complete payment</p>',
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair → suitable-weak moving-tube gate / square-root-log frontier → fifth-shell matching complete payment → single inward collar / true-packet bridge boundary</p>',
        "detailed K route",
    )
    card = r'''          <div class="task-one" id="r074l" data-release="r074l" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74L · 2026-09-02</p><h3>R0.74L｜自由热指数为何只卡在最近内领圈</h3>
            <p>更深内壳都有严格指数余量；最近内领圈在正体积薄片上仍阻断自由热替换。</p>
            <p><strong>边界：</strong>这里只排除一种比较方法；真实包桥估计、匹配上界和普适端点仍开放，不构成千禧年问题结论。</p>
            <p><a href="/notes/r0-74k.html"><strong>阅读 R0.74L 完整中文笔记 →</strong></a><br><a href="/notes/r0-74k.pdf">下载同步 PDF</a> · <a href="/assets/r074l/fig-r074l-single-inward-collar.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a></p>
          </div>
'''
    home, removed = re.subn(
        r'\s*<div class="task-one" id="r074l" data-release="r074l"[\s\S]*?</div>\n',
        "\n",
        home,
        count=1,
    )
    if removed not in (0, 1):
        raise RuntimeError("home K card removal failed")
    home = replace_once(home, '          <div class="task-one" id="r074j"', card + '          <div class="task-one" id="r074j"', "home K card")
    write_text(HOME, home)


def update_literature_legacy_k() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.76"', 'data-site-version="1.77"', "literature version"),
        ('/i18n-en.js?v=1.76', '/i18n-en.js?v=1.77', "literature i18n"),
        ('R0.69P–R0.74J 只列为研究笔记', 'R0.69P–R0.74L 只列为研究笔记', "literature range"),
        ('文献综述 v1.76 · 2026-09-02', '文献综述 v1.77 · 2026-09-02', "literature footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74L</b><strong>最近内领圈与真实包桥边界</strong></header><p>自由热比较在所有更深内壳有严格指数余量，只在最近内领圈留下正体积障碍；真实包桥—剪切相关估计保持开放。<a href="/notes/r0-74k.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074l-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74L</b><strong>真实包桥—BV 领圈估计</strong></header><p>直接证明或否定尺度依赖、有限时间、有符号的真实包领圈估计。</p></div>'
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
    boundary = '''<h3 id="r074l-boundary">R0.74L 的文献与主张边界</h3><p>限定主源审计覆盖 Bedrossian--Coti Zelati、Albritton--Beekie--Novack、Villringer、Gardner--Liss--Mattingly 与 Liss--Luan。现有结果没有提供这里所需的尺度依赖、有限时间、有符号领圈估计；有限非命中不证明新颖性或优先权。</p><div class="boundary"><strong>R0.74L 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只排除指定的自由热替换，并给出一个仍待证明的真实包充分条件；匹配上界、普适端点与正则性仍开放。<a href="/notes/r0-74k.html">阅读完整中文笔记</a>。</p></div>
'''
    if 'id="r074l-boundary"' not in page:
        page = replace_once(page, '        <section id="references">', boundary + '        <section id="references">', "literature K boundary")
    write_text(LITERATURE, page)


def update_accounting_legacy_k() -> None:
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
        "latestReleaseGate": "tests/r074l-single-collar-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074l-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074l-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074l-pdf.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.77"', 'data-site-version="1.78"', "home version"),
        ('/i18n-en.js?v=1.77', '/i18n-en.js?v=1.78', "home i18n"),
        ('/site-refresh.js?v=1.77.1', '/site-refresh.js?v=1.78.1', "home refresh"),
        ('<strong>v1.77</strong>网页版本', '<strong>v1.78</strong>网页版本', "home version stat"),
        ('<span><strong>213</strong>公开研究笔记</span>', '<span><strong>214</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74K</strong>最新研究节点</span>', '<span><strong>R0.74L</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74K', 'Research topology · R0.1–R0.74L', "topology label"),
        ('href="#r074k">跳到首页 R0.74K 卡片 →', 'href="#r074l">跳到首页 R0.74L 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74K：115 节已公开，91 节完整封存', 'href="#r070a">R0.70A–R0.74L：116 节已公开，92 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74K</span>', '<span class="route-range">R0.69P–R0.74L</span>', "route range"),
        ('<h3>R0.74K：最近内领圈与真实包桥边界</h3>', '<h3>R0.74L：共同前向律、短时钟与主目标领圈</h3>', "route title"),
        ('<p class="tree-current-summary">自由热比较在所有更深内壳有余量，只在最近内领圈失败；真实包的桥—剪切相关估计仍开放。</p>', '<p class="tree-current-summary">变化的桥族已反演为共同前向律，主目标领圈由短时钟 BV 闭合；最近内领圈仍开放。</p>', "route summary"),
        ('<p class="tree-path"><span>R0.72R–R0.74K：</span>', '<p class="tree-path"><span>R0.72R–R0.74L：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74K"', 'aria-label="R0.69P–R0.74L"', "route aria"),
        ('<summary>展开 123 篇公开笔记</summary>', '<summary>展开 124 篇公开笔记</summary>', "route count"),
        ('综述 v1.77 · 2026-09-02', '综述 v1.78 · 2026-09-02', "home footer"),
        ('全站现有 213 篇公开研究笔记', '全站现有 214 篇公开研究笔记', "recap card count"),
    ):
        home = replace_once_or_present(home, old, new, label)

    home, n = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74L 已关闭主目标领圈的时间重数；下一步只处理最近内领圈的定量正剪切排出。完整有符号条件、匹配上界与普适端点仍开放。</span></div>',
        home, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74L · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74L｜变化的桥族、短时钟，和一个闭合的主领圈</h2><p class="route-map-intro">共同前向律与短时钟 BV 关闭主目标领圈；最近内领圈、完整有符号条件和匹配上界仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74l.pdf">阅读最新 R0.74L 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">214 篇研究笔记总索引</a><a href="#r074l">查看首页 R0.74L 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74L · 116 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>92 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74L</span></div></div></section>'''
    home, n = re.subn(
        r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>',
        lambda _: latest, home, count=1, flags=re.S,
    )
    if n != 1:
        raise RuntimeError("latest spotlight replacement failed")

    home = replace_once_or_present(
        home,
        '<a class="milestone" href="/notes/r0-74k.html">R0.74K</a>',
        '<a class="milestone" href="/notes/r0-74k.html">R0.74K</a>\n<a class="milestone" href="/notes/r0-74l.html">R0.74L</a>',
        "route L link",
    )
    home = replace_once_or_present(
        home,
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74L</span><span class="tree-state current">下一检查点</span></div><h3>R0.74L 下一接口</h3><p>直接证明或否定真实包的归一化桥—BV 领圈估计。</p></article></div>',
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74M</span><span class="tree-state current">下一检查点</span></div><h3>R0.74M 下一接口</h3><p>直接处理最近内领圈的定量正剪切排出；完整有符号条件仍开放。</p></article></div>',
        "next route",
    )
    home = replace_once_or_present(
        home,
        'fifth-shell matching complete payment → single inward collar / true-packet bridge boundary</p>',
        'fifth-shell matching complete payment → single inward collar / true-packet bridge boundary → common forward law / short-clock BV / main target collar</p>',
        "detailed L route",
    )
    card = r'''          <div class="task-one" id="r074l" data-release="r074l" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74L · 2026-09-02</p><h3>R0.74L｜变化的桥族、短时钟，和一个闭合的主领圈</h3>
            <p>我把变化的后向桥族反演为共同前向律，并用短时钟 BV 闭合了精确解族的主目标领圈。最近内领圈仍为 OPEN。</p>
            <p><a href="/notes/r0-74l.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74l.pdf">PDF</a> · <a href="/assets/r074l/fig-r074l-forward-clock-bv.pdf">附图</a></p>
          </div>
'''
    home, removed = re.subn(
        r'\s*<div class="task-one" id="r074l" data-release="r074l"[\s\S]*?</div>\n',
        "\n", home, count=1,
    )
    if removed not in (0, 1):
        raise RuntimeError("home L card removal failed")
    home = replace_once(home, '          <div class="task-one" id="r074k"', card + '          <div class="task-one" id="r074k"', "home L card")
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.77"', 'data-site-version="1.78"', "literature version"),
        ('/i18n-en.js?v=1.77', '/i18n-en.js?v=1.78', "literature i18n"),
        ('R0.69P–R0.74K 只列为研究笔记', 'R0.69P–R0.74L 只列为研究笔记', "literature range"),
        ('文献综述 v1.77 · 2026-09-02', '文献综述 v1.78 · 2026-09-02', "literature footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74L</b><strong>共同前向律、短时钟与主目标领圈</strong></header><p>变化的周期桥族先积分再反演为共同前向律；坏路径指数余量与好路径短时钟 BV 合并，关闭主目标领圈。最近内领圈仍开放。<a href="/notes/r0-74l.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074l-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74M</b><strong>最近内领圈的定量正剪切排出</strong></header><p>直接证明或否定最近内领圈的 expulsion；完整有符号条件与匹配上界保持开放。</p></div>'
    page, n = re.subn(
        r'<div class="route-step pause"><header><b>开放接口 · R0\.74L</b>.*?</div>',
        lambda _: route, page, count=1, flags=re.S,
    )
    if n != 1 and '<b>开放接口 · R0.74M</b>' not in page:
        raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074l-boundary">R0.74L 的文献与主张边界</h3><p>有界十篇主源审计没有找到直接给出或否定本节归一化周期桥--短时钟 BV 估计的定理。边缘投影与经典 Aronson 路线因算子不匹配而未使用；有限未命中不证明新颖性、优先权或检索完备性。</p><div class="boundary"><strong>R0.74L 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只关闭精确解族的主目标领圈；最近内领圈、完整有符号条件、匹配上界与普适正则性仍开放。<a href="/notes/r0-74l.html">阅读完整中文笔记</a>。</p></div>
'''
    if 'id="r074l-boundary"' not in page:
        page = replace_once(page, '        <section id="references">', boundary + '        <section id="references">', "literature L boundary")
    write_text(LITERATURE, page)


def update_accounting() -> None:
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "publicHtmlNoteCount": 214,
        "postR060PublishedNodeCount": 154,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 171,
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
        "publicHtmlNoteCount": 214,
        "publicPdfNoteCount": 171,
        "postR060PublishedNodeCount": 154,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074m",
        "latestReleaseGate": "tests/r074l-main-collar-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074l-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074l-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074l-pdf.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74l.html", render_note())
        assert_bilingual_dictionary()
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74l.html", render_note())
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
