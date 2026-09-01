#!/usr/bin/env python3
"""Publish frozen R0.74H research assets without changing their claims."""

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
VERSION = "1.74"
RELEASE = "r074h"
CODE = "R0.74H"
NEXT = "R0.74I"
FIGURE_DIR = "fig-r074h-collar-flux-repair"
FIGURE_SLUG = "fig-r074h-collar-flux-repair"
TITLE = "R0.74H｜环带通量修复：冻结局部坐标中的双区间闭合"
FROZEN_CORE = "5cd31fd8cde1574f02d9e9af3417686d2a8f8d9c"
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
    source = ROOT / "research/figures/r074h" / FIGURE_DIR
    research_mirror = PUBLIC / "figures/r074h" / FIGURE_DIR
    publication_archive = ROOT / "figures/r074h" / FIGURE_DIR
    for target in (research_mirror, publication_archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    asset_dir = PUBLIC / "assets/r074h"
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
        "figureSchemaVersion": "r074h-publication-compat-v1",
        "figureId": frozen["figureId"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74H collar-flux figure package.",
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
        "data": [file_record(publication_archive / "source-data.csv", "r074h-source-data-v1")],
        "sourceData": [],
        "figure": {"widthMillimetres": 178.0, "heightMillimetres": 90.0, "outputs": outputs},
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
<meta name="description" content="冻结局部坐标中的环带通量修复、双区间闭合与小支付端点">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74h.html"><link rel="stylesheet" href="/bilingual.css">
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
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74H · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74H · 完整中文版本</div><h1>__TITLE__</h1>
<p>上一节排除了把任意大支付量统一压成 (P^{2/3}) 的估计。本节从局部能量恒等式找回正环带通量，并证明对任意光滑周期无外力解成立的双区间闭合。</p>
<div class="labels"><span class="label">PROVED</span><span class="label">FINITE</span><span class="label">OPEN</span><span class="label">LITERATURE BOUNDARY</span><span class="label">NOT CLAY</span></div>
<p>这里得到的是一尺度能量估计，不是 epsilon 正则性、延拓判据或千禧年问题解答。</p></div>
<div class="stamp"><strong>状态 · R0.74H</strong><p>双区间闭合：PROVED</p><p>环带通量修复：PROVED</p><p>证书 25/25：FINITE</p><p>独立复算 150 字段：FINITE</p><p>图件 69/69：FINITE</p><p>弱解稳定与尺度迭代：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 主结论</div><h2>大支付保留线性项，小支付保留 (2/3) 次幂</h2>
<p>对 R0.74E 冻结的两种局部 frame、每个声明范围内的光滑周期无外力解、尺度与柱体，存在统一常数 (C)，使</p>
<div class="equation">\[\boxed{X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr].}\]</div>
<div class="equation">\[\boxed{X_R^F\le C\bigl[(P_R^F)^{2/3}+P_{0,R}^F\bigr]\le C\bigl[(P_R^F)^{2/3}+P_R^F\bigr].}\]</div>
<p>(P_{0,R}^F) 是加入 acceleration row 之前的 Version-F 支付。第二个不等式只用冻结账本的非负性。</p></section>
<section id="s-02"><div class="section-no">02 / 双区间</div><h2>门槛在 (P=1)</h2>
<p>当支付量不超过一时，线性项可由 (P^{2/3}) 吸收，因此两种 frame 都有</p>
<div class="equation">\[\boxed{P_R^\alpha\le1\quad\Longrightarrow\quad X_R^\alpha\le C(P_R^\alpha)^{2/3},\qquad \alpha\in\{M,F\}.}\]</div>
<p>当 (P_R^\alpha>1) 时，定理保留 (+P_R^\alpha)。这正是上一节反例要求支付的大量区间，而不是证明缺口。</p></section>
<section id="s-03"><div class="section-no">03 / 恒等式</div><h2>环带通量从局部能量恒等式进入</h2>
<p><strong>PROVED。</strong>两种冻结坐标中的加权局部能量恒等式、有限 shell 极限与压力规范转移均逐项保留。二次 cutoff row 给出 (2/3) 次幂；剩余有符号项由正环带通量支付。</p>
<p>Version-F 的 acceleration row 没有被隐藏或改写成有利符号，而是先进入 (P_{0,R}^F)，再由完整非负账本比较到 (P_R^F)。</p></section>
<section id="s-04"><div class="section-no">04 / 精确修复</div><h2>把缺失的正通量写入支付量</h2>
<p>记正环带通量为 \(\mathfrak C_R^\alpha\)。精确修复是</p>
<div class="equation">\[\boxed{X_R^\alpha\le C\left[(P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\right].}\]</div>
<p>若定义</p><div class="equation">\[\boxed{\widehat P_R^\alpha=P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2},}\]</div>
<p>则得到同次齐性的形式</p><div class="equation">\[\boxed{X_R^\alpha\le C(\widehat P_R^\alpha)^{2/3}.}\]</div></section>
<section id="s-05"><div class="section-no">05 / 双包检验</div><h2>正环带通量承担缺失的 (L_j) 尺度</h2>
<p>在 R0.74F--G 的精确双包解族上，对所有充分大的 (j)，</p>
<div class="equation">\[\boxed{P_{R_j}^M=P_{R_j}^F\ge cB_j^2L_jR_j^2\longrightarrow\infty.}\]</div>
<div class="equation">\[\boxed{\mathfrak C_{R_j}^M=\mathfrak C_{R_j}^F\ge cB_j^2L_jR_j^2.}\]</div>
<div class="equation">\[\boxed{(\mathfrak C_{R_j}^{\alpha})^{3/2}\ge cB_j^3L_j^{3/2}R_j^3,\qquad \alpha\in\{M,F\}.}\]</div>
<p>因此，修复项确实看见上一节暴露的缺失尺度。</p></section>
<section id="s-06"><div class="section-no">06 / 单向边界</div><h2>没有反向比较，也没有尺度迭代</h2>
<p>这里只证明 collar flux 的单边下界与双区间上界；没有证明反向比较、渐近等价、匹配的 (B_j^3R_j^3) 下界或 logarithmic-frontier theorem。</p>
<p>恒等式中的通量付款仍不是一个可独立控制的正则性量。把它替换成可由弱解数据稳定支付的量，仍是下一门槛。</p></section>
<section id="s-07"><div class="section-no">07 / 证据分层</div><h2>解析定理、有限复算与文献边界</h2>
<p><strong>PROVED：</strong>两种加权局部能量恒等式、finite-shell 与 pressure-gauge 转移、(2/3) cutoff row、正环带通量修复、双区间闭合、小支付端点，以及双包族上的单边通量下界。</p>
<p><strong>FINITE：</strong>Python 证书 25/25 PASS；独立 Ruby 精确实现核对 150 个字段，零差异。图件 validator 69/69 PASS，23 项 SHA 全通过，物理图包共 24 个文件。有限结果只复核代数与图件，不替代解析证明。</p>
<p><strong>LITERATURE BOUNDARY：</strong>限定核对四篇相邻主源，没有定位到完全相同的组合。这只是有限语料中的 non-hit，不支持新颖性或优先权声明。</p></section>
<section id="s-08"><div class="section-no">08 / 开放边界</div><h2>下一步必须独立控制通量</h2>
<ul><li>适用于 suitable weak-solution approximation 的稳定版本；</li><li>替代恒等式级 collar flux、且可独立控制的支付量；</li><li>尺度迭代或吸收机制；</li><li>epsilon 正则性、延拓或奇性排除；</li><li>任意三维全局正则性、blow-up 与 Clay 结论；</li><li>新颖性或发表优先权。</li></ul></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>通量修复与双区间账本</h2>
<picture><source srcset="/assets/r074h/fig-r074h-collar-flux-repair.svg" type="image/svg+xml"><img src="/assets/r074h/fig-r074h-collar-flux-repair.png" alt="R0.74H collar-flux repair and two-regime closure exponent diagram"></picture>
<p><a href="/assets/r074h/fig-r074h-collar-flux-repair.pdf">下载矢量 PDF</a> · <a href="/assets/r074h/fig-r074h-collar-flux-repair.png">下载 600 dpi PNG</a> · <a href="/assets/r074h/fig-r074h-collar-flux-repair.svg">打开 SVG</a> · <a href="/figures/r074h/fig-r074h-collar-flux-repair/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074h/fig-r074h-collar-flux-repair/caption.md">图注</a> · <a href="/figures/r074h/fig-r074h-collar-flux-repair/qa-report.md">图件 QA</a> · <a href="/figures/r074h/fig-r074h-collar-flux-repair/validation.json">69 项验证记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/public/figures/r074h/fig-r074h-collar-flux-repair">完整 24 文件图包</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是精确指数图，不是 DNS、仿真或测量数据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、解析审计、精确证书与文献边界</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_collar_flux_two_regime_closure.md">规范主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_energy_identity_independent_audit.md">能量恒等式独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_packet_flux_independent_audit.md">双包通量独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_scaling_and_claim_audit.md">尺度与主张审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_full_note_adversarial_audit.md">全文对抗审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_final_source_rebind_audit.md">最终源文件重绑定审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_report-source.md">完整报告源</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_collar_flux_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_collar_flux_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074h_collar_flux_certificate.py">Python 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074h_collar_flux_certificate_independent.rb">独立 Ruby 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_primary_literature_boundary.md">四篇主源边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_primary_literature_independent_audit.md">文献独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_gap_matrix.md">证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074h_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74h.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74I</h2><p>寻找可独立控制、适合弱解极限的 collar-flux 替代量，并先验证它能否支持尺度迭代；在此之前不作正则性外推。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def write_dictionary() -> None:
    write_text(ROOT / "research/r074h_bilingual_dictionary.md", """# R0.74H bilingual publication dictionary

The public note is authored completely in Chinese. This dictionary fixes recurring status terminology only.

| Chinese | English |
|---|---|
| 已证明 | PROVED |
| 有限证书或图件复算 | FINITE |
| 开放问题 | OPEN |
| 文献边界 | LITERATURE BOUNDARY |
| 不构成 Clay 问题解答 | NOT CLAY |
| 正环带通量 | positive collar flux |
| 双区间闭合 | two-regime closure |

Chinese title: R0.74H｜环带通量修复：冻结局部坐标中的双区间闭合
English working title: R0.74H — collar-flux repair and two-regime closure in the frozen local frames
""")


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.73"', f'data-site-version="{VERSION}"', "home version"),
        ('/i18n-en.js?v=1.73', f'/i18n-en.js?v={VERSION}', "home i18n"),
        ('/site-refresh.js?v=1.73.1', f'/site-refresh.js?v={VERSION}.1', "home refresh"),
        ('<strong>v1.73</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "home version stat"),
        ('<span><strong>209</strong>公开研究笔记</span>', '<span><strong>210</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74G</strong>最新研究节点</span>', '<span><strong>R0.74H</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74G', 'Research topology · R0.1–R0.74H', "topology label"),
        ('href="#r074g">跳到首页 R0.74G 卡片 →', 'href="#r074h">跳到首页 R0.74H 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74G：111 节已公开，87 节完整封存', 'href="#r070a">R0.70A–R0.74H：112 节已公开，88 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74G</span>', '<span class="route-range">R0.69P–R0.74H</span>', "route range"),
        ('<h3>R0.74G：完整支付闭合，冻结局部坐标不等式被否定</h3>', '<h3>R0.74H：环带通量修复与双区间闭合</h3>', "route title"),
        ('<p class="tree-current-summary">双包存活与完整 denominator 账本合并后，R0.74E 两条冻结候选估计的比值至少按 L_j 发散；修正 denominator 仍开放。NOT CLAY。</p>', '<p class="tree-current-summary">正环带通量修复大支付端，对任意光滑周期无外力解得到 X≤C(P^{2/3}+P)；小支付端保留 P^{2/3}。</p>', "route summary"),
        ('<p class="tree-path">局部付款 → 固定中心运输障碍 → 局部 frame → 双包存活 → 完整分母反例</p>', '<p class="tree-path">局部 frame → 双包存活 → 完整分母反例 → 环带通量修复</p>', "route short path"),
        ('<p class="tree-path"><span>R0.72R–R0.74G：</span>', '<p class="tree-path"><span>R0.72R–R0.74H：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74G"', 'aria-label="R0.69P–R0.74H"', "route aria"),
        ('<summary>展开 119 篇公开笔记</summary>', '<summary>展开 120 篇公开笔记</summary>', "route count"),
        ('综述 v1.73 · 2026-09-01', '综述 v1.74 · 2026-09-02', "home footer"),
        ('全站现有 209 篇公开研究笔记', '全站现有 210 篇公开研究笔记', "recap card count"),
    )
    for old, new, label in pairs:
        home = replace_once(home, old, new, label)

    home, n = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74H 已找回正环带通量，并得到光滑解的一尺度双区间闭合。下一步是把恒等式级通量替换为可独立控制、适合弱解极限的量；尺度迭代与正则性仍开放。</span></div>',
        home,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74H · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74H｜环带通量修复</h2><p class="route-map-intro">正环带通量修复大支付端，并给出 \(X\lesssim P^{2/3}+P\)；小支付端仍保持 \(P^{2/3}\)。弱解稳定与尺度迭代仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74h.pdf">阅读最新 R0.74H 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">210 篇研究笔记总索引</a><a href="#r074h">查看首页 R0.74H 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74H · 112 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>88 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74H</span></div></div></section>'''
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
        '<a class="milestone" href="/notes/r0-74g.html">R0.74G</a>',
        '<a class="milestone" href="/notes/r0-74g.html">R0.74G</a>\n<a class="milestone" href="/notes/r0-74h.html">R0.74H</a>',
        "route H link",
    )
    home = replace_once(
        home,
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74H</span><span class="tree-state current">下一检查点</span></div><h3>R0.74H 下一接口</h3><p>提出一个能支付精确双包族、保持尺度不变且不循环的新 denominator；只有先通过该见证，才检查任意解定理。</p></article></div>',
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74I</span><span class="tree-state current">下一检查点</span></div><h3>R0.74I 下一接口</h3><p>寻找可独立控制、适合弱解极限的 collar-flux 替代量，并检查尺度迭代。</p></article></div>',
        "next route",
    )
    home = home.replace(
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails</p>',
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair</p>',
        1,
    )
    card = r'''          <div class="task-one" id="r074h" data-release="r074h" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74H · 2026-09-02</p><h3>R0.74H｜环带通量修复：冻结局部坐标中的双区间闭合</h3>
            <p>正环带通量补上大支付端，得到 \(X\lesssim P^{2/3}+P\)；当 \(P\le1\) 时仍保持 \(X\lesssim P^{2/3}\)。</p>
            <p><strong>边界：</strong>弱解稳定、独立通量控制与尺度迭代仍开放。</p>
            <p><a href="/notes/r0-74h.html"><strong>阅读 R0.74H 完整中文笔记 →</strong></a><br><a href="/notes/r0-74h.pdf">下载同步 PDF</a> · <a href="/assets/r074h/fig-r074h-collar-flux-repair.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a></p>
          </div>
'''
    home = replace_once(home, '          <div class="task-one" id="r074g"', card + '          <div class="task-one" id="r074g"', "home H card")
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.73"', 'data-site-version="1.74"', "literature version"),
        ('/i18n-en.js?v=1.73', '/i18n-en.js?v=1.74', "literature i18n"),
        ('R0.69P–R0.74G 只列为研究笔记', 'R0.69P–R0.74H 只列为研究笔记', "literature range"),
        ('文献综述 v1.73 · 2026-09-01', '文献综述 v1.74 · 2026-09-02', "literature footer"),
    ):
        page = replace_once(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74H</b><strong>环带通量修复与双区间闭合</strong></header><p>加权局部能量恒等式找回正环带通量，对任意光滑周期无外力解得到 \(X\lesssim P^{2/3}+P\)，小支付端保持 \(P^{2/3}\)。<a href="/notes/r0-74h.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074h-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74I</b><strong>可独立控制的通量支付</strong></header><p>寻找适合弱解极限的 collar-flux 替代量，并检查尺度迭代。</p></div>'
    page, n = re.subn(
        r'<div class="route-step pause"><header><b>开放接口 · R0\.74H</b>.*?</div>',
        lambda _: route,
        page,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074h-boundary">R0.74H 的文献与主张边界</h3><p>限定核对四篇相邻主源，没有定位到完全相同的加权局部能量、正环带通量与双区间组合；有限 non-hit 不证明新颖性或优先权。</p><div class="boundary"><strong>R0.74H 的公开边界</strong><p>PROVED、FINITE、OPEN、LITERATURE BOUNDARY 与 NOT CLAY 在研究笔记中分开。结论只覆盖声明的一尺度光滑解定理；弱解稳定、尺度迭代与正则性仍开放。<a href="/notes/r0-74h.html">阅读完整中文笔记</a>。</p></div>
'''
    page = replace_once(page, '        <section id="references">', boundary + '        <section id="references">', "literature H boundary")
    write_text(LITERATURE, page)


def update_accounting() -> None:
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "publicHtmlNoteCount": 210,
        "postR060PublishedNodeCount": 150,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 167,
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
        "publicHtmlNoteCount": 210,
        "publicPdfNoteCount": 167,
        "postR060PublishedNodeCount": 150,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074i",
        "latestReleaseGate": "tests/r074h-collar-flux-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074h-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074h-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074h-pdf.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74h.html", render_note())
    write_dictionary()
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
