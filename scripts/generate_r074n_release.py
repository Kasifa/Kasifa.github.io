#!/usr/bin/env python3
"""Publish the frozen R0.74N research package without changing its claims."""

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
VERSION = "1.80"
RELEASE = "r074n"
CODE = "R0.74N"
NEXT = "R0.74O"
FIGURE_DIR = "fig-r074n-all-shell-synthesis"
TITLE = "R0.74N｜把所有壳层合起来，完整领圈条件闭合了"
FROZEN_CORE = "08f3070d72259793bd29373a6db332844f001511"
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
    source = ROOT / "research/figures/r074n" / FIGURE_DIR
    public_mirror = PUBLIC / "figures/r074n" / FIGURE_DIR
    archive = ROOT / "figures/r074n" / FIGURE_DIR
    for target in (public_mirror, archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
    assets = PUBLIC / "assets/r074n"
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
        "figureSchemaVersion": "r074n-publication-compat-v1",
        "figureId": frozen["figure_id"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74N exact all-shell synthesis figure package.",
        "supportedClaim": "See the frozen caption, source data, validation record, and synchronized research note; this wrapper changes no scientific asset.",
        "createdAt": "2026-09-02T00:00:00Z",
        "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": FROZEN_CORE, "dirty": False},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json", "precision": "frozen exact or deterministic figure package", "solver": "none", "formalCommand": "use the frozen package command.txt and validate.py", "wallTimeSeconds": 1.0, "monitoring": {"enabled": False}},
        "compute": {"host": "local workstation (hostname intentionally omitted)", "operatingSystem": "macOS arm64", "cpu": "arm64 / local CPU", "memoryGiB": 36.0, "processes": 1, "threadsPerProcess": 1},
        "environment": {"python": "3.12.13", "packagesLock": "requirements.txt"},
        "data": [file_record(archive / "source-data.csv", "r074n-source-data-v1")],
        "sourceData": [],
        "figure": {"widthMillimetres": 178.0, "heightMillimetres": 100.0, "outputs": outputs},
        "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": {"allShellSynthesis": "PROVED", "matchingExactFamilyEndpointLaw": "PROVED", "dissipationMatchingLowerBound": "OPEN", "arbitraryFlowEndpoint": "OPEN", "finiteFigureProvesAnalyticTheorem": False, "globalRegularity": False, "notClay": True},
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
<meta name="description" content="全部内壳、主壳和外壳合成为精确解族的完整有符号领圈条件，并给出匹配的 X_j 与领圈通量尺度">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74n.html"><link rel="stylesheet" href="/bilingual.css">
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
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74N · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74N · 完整中文版本</div><h1>__TITLE__</h1>
<p>这一节仍然没有解决三维 Navier--Stokes 千禧年问题。R0.74L 处理了主壳，R0.74M 处理了最近内壳。这里我不再逐行追赶：全部内壳进入同一个有界正部弦长，全部外壳由超高斯权绝对求和。因而，冻结精确解族的完整 R0.74K 有符号领圈条件闭合。再与已经审计的能量闭合式和支付律合并，我得到该精确解族上的 \(X_j\) 与 \(\mathfrak C_j\) 匹配平方根对数尺度。耗散分量只有上界，没有匹配下界；任意流端点估计和正则性问题仍然开放。<strong>NOT CLAY.</strong></p>
<div class="labels"><span class="label">PROVED</span><span class="label">INHERITED</span><span class="label">FINITE</span><span class="label">LITERATURE BOUNDARY</span><span class="label">OPEN</span><span class="label">NOT CLAY</span></div></div>
<div class="stamp"><strong>状态 · R0.74N</strong><p>完整有符号条件：PROVED</p><p>精确族 \(X_j\) 匹配律：PROVED</p><p>耗散匹配下界：OPEN</p><p>证书 84/84：FINITE</p><p>图件 67/67：FINITE</p><p>任意流端点：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 完整主结论</div><h2>全部壳层的完整有符号条件已闭合</h2>
<p>对 R0.74F--N 的精确光滑、周期、无外力双包解族，存在与 \(j\) 无关的 \(C&lt;\infty\) 和 \(j_0\)，使每个 \(j\ge j_0\) 满足</p>
<div class="equation">\[\boxed{\sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+\le C\Gamma_jL_jR_j^5.}\]</div>
<p>这里的完整对象覆盖全部壳层，没有丢掉周期副本，也没有假设壳层或正负包之间发生抵消：</p>
<div class="equation">\[\mathcal I_j=\mathcal I_<+\mathcal I_=+\mathcal I_>,\qquad k\le j-1,\quad k=j,\quad k\ge j+1.\]</div></section>
<section id="s-02"><div class="section-no">02 / 全部内壳</div><h2>所有内壳只留下一个一致有界的正部弦长</h2>
<p>我先逐壳取正部，再把权重放进联合弦长。这个上界故意放弃所有壳层抵消：</p>
<div class="equation">\[0\le D_<\le C\sum_{k\ge1}2^ke^{-4^{k-1}/32}=:C_*&lt;\infty.\]</div>
<p>所有内壳的联合支撑仍落在最大的 \(j-1\) 领圈内，所以 R0.74M 的支撑条件化最后时段排出机制可以一次作用于整个内壳和。坏路径由</p>
<div class="equation">\[\frac1{16}-\frac1{320}-\frac8{3969}=\frac{72851}{1270080}>0\]</div>
<p>支付；好路径进入超高斯尾。由此得到 \(\sup_\tau[\mathcal I_<]_+\le C\Gamma_jL_jR_j^5\)。</p></section>
<section id="s-03"><div class="section-no">03 / 主壳与外壳</div><h2>主壳沿用绝对估计，外壳一次绝对求和</h2>
<p>主壳使用 R0.74L 已审计的真实包绝对估计。外壳只需最大值原理、完整双面领圈导数总量和超高斯权：</p>
<div class="equation">\[|\mathcal I_>(\tau)|\le CR_j^4\sum_{k\ge j+1}4^k\Gamma_k.\]</div>
<p>尾和由首项控制，且有严格指数余量</p>
<div class="equation">\[3c_\gamma-\rho=\frac{1237}{423360}>0.\]</div>
<p>因此 \(\sup_\tau|\mathcal I_>|\le C\Gamma_jL_jR_j^5\)，并同时得到有限截断到无限壳层的统一极限。</p></section>
<section id="s-04"><div class="section-no">04 / 纠正后的精确族结论</div><h2>领圈通量和 \(X_j\) 都达到匹配平方根对数尺度</h2>
<p>R0.74K 先把完整条件转换为领圈通量上界，再与 R0.74H、R0.74J 及 R0.74F 的已审计结论非循环地合并。我得到本节必须显式保留的精确族结论：</p>
<div class="equation">\[\boxed{X_j\asymp\mathfrak C_j\asymp B_j^2L_jR_j^2\asymp P_j^{2/3}\sqrt{1+\log_+P_j}.}\]</div>
<p>这是跨笔记证明合成，不是新的随机引理，也不是任意流上的普适端点不等式。</p></section>
<section id="s-05"><div class="section-no">05 / 分量边界</div><h2>外部动能有两侧界，耗散分量只有上界</h2>
<p>令 \(T_j=B_j^2L_jR_j^2\)。分量结论是</p>
<div class="equation">\[cT_j\le\mathcal U_{{\rm ext},j}^{\infty}\le X_j\le CT_j,\qquad 0\le\mathcal D_{{\rm ext},j}\le CT_j.\]</div>
<p>第二个分量没有已证明的匹配下界；这里不声称 \(\mathcal D_{{\rm ext},j}\ge cT_j\)。</p></section>
<section id="s-06"><div class="section-no">06 / 证据等级</div><h2>解析证明、沿用输入、有限复算和文献边界分开</h2>
<p><strong>PROVED：</strong>完整全壳层有符号条件、无抵消内壳联合和、外壳绝对尾、匹配领圈通量律、跨笔记推出的精确族 \(X_j\) 匹配律及分量边界。</p>
<p><strong>INHERITED：</strong>R0.74F--H 精确解族、R0.74F 外部动能下界、R0.74H 能量闭合式、R0.74J 支付律、R0.74K 转换、R0.74L 主壳估计和 R0.74M 最后时段排出。</p>
<p><strong>FINITE：</strong>Python Fraction 与独立 Ruby Rational 各 84/84、零差异；对抗审计拒绝两类有效 JSON 变异。图包含 26 个文件、24 个 manifest 条目、21 个外部绑定和 25 行校验和，验证器 67/67。有限复算不替代解析证明。</p>
<p><strong>LITERATURE BOUNDARY：</strong>有界八篇一手文献检索没有找到直接给出本节精确全壳层解族结论的定理。有限未命中不证明新颖性、优先权、检索完备性或可发表性。</p></section>
<section id="s-07"><div class="section-no">07 / 开放边界</div><h2>精确族内部已闭合，任意流接口仍未跨越</h2>
<ul><li>耗散分量单独的匹配下界仍为 OPEN；</li><li>任意流上的全壳层有符号领圈控制仍为 OPEN；</li><li>普适平方根对数端点、payment-to-admissibility 与指定点 core-from-shell 仍为 OPEN；</li><li>任意三维数据的正则性或奇性、全局存在与光滑性仍为 OPEN；</li><li>新颖性和优先权仍为 OPEN。</li></ul>
<p><strong>NOT CLAY：</strong>本节只处理一个精确构造解族，不能外推为任意三维 Navier--Stokes 解的定理。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>内壳联合和、主壳、外壳尾与精确族匹配尺度</h2>
<picture><source srcset="/assets/r074n/fig-r074n-all-shell-synthesis.svg" type="image/svg+xml"><img src="/assets/r074n/fig-r074n-all-shell-synthesis.png" alt="R0.74N complete all-shell synthesis and exact-family endpoint scale"></picture>
<p><a href="/assets/r074n/fig-r074n-all-shell-synthesis.pdf">下载矢量 PDF</a> · <a href="/assets/r074n/fig-r074n-all-shell-synthesis.png">下载 600 dpi PNG</a> · <a href="/assets/r074n/fig-r074n-all-shell-synthesis.svg">打开 SVG</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074n/fig-r074n-all-shell-synthesis/caption.md">图注</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/chart-contract-and-source-data.md">图表合同</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/qa-report.md">图件 QA</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/plot.py">绘图源码</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/validate.py">验证器</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/validation.json">67 项验证记录</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/manifest.json">图件 manifest</a> · <a href="/figures/r074n/fig-r074n-all-shell-synthesis/SHA256SUMS">25 项校验和</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是确定性解析示意图，不是 DNS、仿真、随机样本路径或奇点证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、跨笔记审计、双实现证书与完整图包</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_problem_freeze.md">问题冻结</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_all_shell_synthesis.md">解析主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_all_shell_independent_audit.md">壳层独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_crossnote_implication_independent_audit.md">跨笔记推论审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_final_source_rebind_audit.md">最终源文件重绑定</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074n_all_shell_certificate.py">Python 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074n_all_shell_certificate_independent.rb">独立 Ruby 证书</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_all_shell_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_all_shell_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_certificate_adversarial_audit.md">证书对抗审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_primary_literature_boundary.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_primary_literature_independent_audit.md">文献独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_report-source.md">审计后中文 reader source</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_reader_source_independent_audit.md">reader source 独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_figure_independent_audit.md">图件独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074n_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74n.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74O</h2><p>把全壳层领圈控制移到任意流，或建立 payment-to-admissibility 与指定点 core-from-shell 机制；精确族的耗散匹配下界也继续保持开放。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def assert_bilingual_dictionary() -> None:
    path = ROOT / "research/r074n_bilingual_dictionary.md"
    if sha256(path) != "d1418d676333293fab29c11d21da053e60f61241068d4b8aaf2565636c270755":
        raise RuntimeError("frozen R0.74N bilingual dictionary drift")
    value = path.read_text(encoding="utf-8")
    for marker in ("全壳层合成", "无抵消的正部弦长", "精确解族端点匹配律", "外部耗散分量"):
        if marker not in value:
            raise RuntimeError(f"frozen dictionary missing {marker}")


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    replacements = (
        ('data-site-version="1.79"', 'data-site-version="1.80"', "home version"),
        ('/i18n-en.js?v=1.79', '/i18n-en.js?v=1.80', "home i18n"),
        ('/site-refresh.js?v=1.79.1', '/site-refresh.js?v=1.80.1', "home refresh"),
        ('<strong>v1.79</strong>网页版本', '<strong>v1.80</strong>网页版本', "home version stat"),
        ('<span><strong>215</strong>公开研究笔记</span>', '<span><strong>216</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74M</strong>最新研究节点</span>', '<span><strong>R0.74N</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74M', 'Research topology · R0.1–R0.74N', "topology label"),
        ('href="#r074m">跳到首页 R0.74M 卡片 →', 'href="#r074n">跳到首页 R0.74N 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74M：117 节已公开，93 节完整封存', 'href="#r070a">R0.70A–R0.74N：118 节已公开，94 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74M</span>', '<span class="route-range">R0.69P–R0.74N</span>', "route range"),
        ('<h3>R0.74M：最后时段排出与最近内领圈</h3>', '<h3>R0.74N：全壳层合成与完整领圈条件</h3>', "route title"),
        ('<p class="tree-current-summary">最后一小段布朗路径把典型相关支撑推出最近内领圈；完整壳层合成与匹配上界仍开放。</p>', '<p class="tree-current-summary">全部内壳、主壳和外壳已合成；精确解族的领圈通量与 X_j 匹配，耗散下界和任意流端点仍开放。</p>', "route summary"),
        ('<p class="tree-path"><span>R0.72R–R0.74M：</span>', '<p class="tree-path"><span>R0.72R–R0.74N：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74M"', 'aria-label="R0.69P–R0.74N"', "route aria"),
        ('<summary>展开 125 篇公开笔记</summary>', '<summary>展开 126 篇公开笔记</summary>', "route count"),
        ('综述 v1.79 · 2026-09-02', '综述 v1.80 · 2026-09-02', "home footer"),
        ('全站现有 215 篇公开研究笔记', '全站现有 216 篇公开研究笔记', "recap card count"),
    )
    for old, new, label in replacements:
        home = replace_once_or_present(home, old, new, label)

    home, count = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74N 已关闭精确解族的完整全壳层领圈条件，并得到 X_j 与领圈通量匹配律；耗散匹配下界、任意流端点和 Clay 仍开放。</span></div>',
        home, count=1, flags=re.S,
    )
    if count != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74N · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74N｜把所有壳层合起来，完整领圈条件闭合了</h2><p class="route-map-intro">全部内壳、主壳和外壳已合成；精确解族的 X_j 与领圈通量达到匹配平方根对数尺度，耗散下界和任意流端点仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74n.pdf">阅读最新 R0.74N 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">216 篇研究笔记总索引</a><a href="#r074n">查看首页 R0.74N 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74N · 118 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>94 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74N</span></div></div></section>'''
    home, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, home, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")

    home = replace_once_or_present(home, '<a class="milestone" href="/notes/r0-74m.html">R0.74M</a>', '<a class="milestone" href="/notes/r0-74m.html">R0.74M</a>\n<a class="milestone" href="/notes/r0-74n.html">R0.74N</a>', "route N link")
    home = replace_once_or_present(home, '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74N</span><span class="tree-state current">下一检查点</span></div><h3>R0.74N 下一接口</h3><p>合成其余壳层行并检查 R0.74K 完整有符号条件；匹配上界仍开放。</p></article></div>', '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74O</span><span class="tree-state current">下一检查点</span></div><h3>R0.74O 下一接口</h3><p>把全壳层领圈控制移到任意流，或建立 payment-to-admissibility 与指定点 core-from-shell 机制。</p></article></div>', "next route")
    home = replace_once_or_present(home, 'final-segment expulsion / nearest-inward collar</p>', 'final-segment expulsion / nearest-inward collar → all-shell synthesis / exact-family matching endpoint law</p>', "detailed N route")

    card = r'''          <div class="task-one" id="r074n" data-release="r074n" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74N · 2026-09-02</p><h3>R0.74N｜把所有壳层合起来，完整领圈条件闭合了</h3>
            <p>全部壳层在精确解族内完成合成，X_j 与领圈通量达到匹配尺度；耗散下界和任意流端点仍开放。</p>
            <p><a href="/notes/r0-74n.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74n.pdf">PDF</a> · <a href="/assets/r074n/fig-r074n-all-shell-synthesis.pdf">附图</a></p>
          </div>
'''
    home, removed = re.subn(r'\s*<div class="task-one" id="r074n" data-release="r074n"[\s\S]*?</div>\n', "\n", home, count=1)
    if removed not in (0, 1):
        raise RuntimeError("home N card removal failed")
    anchor = '          <div class="task-one" id="r074m"'
    if anchor not in home:
        raise RuntimeError("home M card anchor missing")
    home = home.replace(anchor, card + anchor, 1)
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.79"', 'data-site-version="1.80"', "literature version"),
        ('/i18n-en.js?v=1.79', '/i18n-en.js?v=1.80', "literature i18n"),
        ('R0.69P–R0.74M 只列为研究笔记', 'R0.69P–R0.74N 只列为研究笔记', "literature range"),
        ('文献综述 v1.79 · 2026-09-02', '文献综述 v1.80 · 2026-09-02', "literature footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74N</b><strong>全壳层合成与精确族匹配端点律</strong></header><p>全部内壳进入一致有界的正部弦长，主壳沿用绝对估计，全部外壳由超高斯权绝对求和；精确解族的 X_j 与领圈通量达到匹配尺度。<a href="/notes/r0-74n.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074n-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74O</b><strong>任意流端点与可容许性接口</strong></header><p>任意流全壳层控制、payment-to-admissibility、指定点 core-from-shell 和耗散匹配下界继续开放。</p></div>'
    if '<b>开放接口 · R0.74O</b>' not in page:
        page, count = re.subn(r'<div class="route-step kept"><header><b>R0\.74M</b>.*?<div class="route-step pause"><header><b>开放接口 · R0\.74N</b>.*?</div>', lambda _: route, page, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074n-boundary">R0.74N 的文献与主张边界</h3><p>有界八篇一手文献检索找到了加权 Navier--Stokes 能量、局部能量聚合、剪切增强耗散和随机路径方法的先例，没有找到直接给出本节精确全壳层解族结论的定理。有限未命中不证明新颖性、优先权、检索完备性或可发表性。</p><div class="boundary"><strong>R0.74N 的公开边界</strong><p>PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 分开。本节关闭精确解族的完整全壳层条件，并得到匹配的 X_j 与领圈通量尺度；耗散匹配下界、任意流端点、正则性与 Clay 仍开放。<a href="/notes/r0-74n.html">阅读完整中文笔记</a>。</p></div>\n'''
    if 'id="r074n-boundary"' not in page:
        anchor = '        <section id="references">'
        if anchor not in page:
            raise RuntimeError("literature references anchor missing")
        page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def route_post_r060_count(home: str) -> int:
    start = home.index('<section class="route-overview"')
    end = home.index('<div class="page-shell">', start)
    slugs = re.findall(r'href="/notes/(r0-[^"]+)\.html"', home[start:end])
    return len(slugs) - slugs.index("r0-61")


def update_accounting() -> None:
    html_count = len(list((PUBLIC / "notes").glob("r0-*.html")))
    pdf_count = len(list((PUBLIC / "notes").glob("r0-*.pdf")))
    if not (PUBLIC / "notes/r0-74n.pdf").exists():
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
        "latestCompletedRelease": RELEASE, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 140,
        "nextRelease": "r074o", "latestReleaseGate": "tests/r074n-all-shell-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074n-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x", "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074n-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074n-pdf.mjs", "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74n.html", render_note())
        assert_bilingual_dictionary()
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74n.html", render_note())
    assert_bilingual_dictionary()
    update_home()
    update_literature()
    update_accounting()
    assert_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "translationRoute": "LOCAL_DIRECT_NO_DGX"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
