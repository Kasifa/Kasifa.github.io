#!/usr/bin/env python3
"""Publish frozen R0.74I research assets without changing their claims."""

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
VERSION = "1.75"
RELEASE = "r074i"
CODE = "R0.74I"
NEXT = "R0.74J"
FIGURE_DIR = "fig-r074i-moving-tube-log-screen"
FIGURE_SLUG = "fig-r074i-moving-tube-log-screen"
TITLE = "R0.74I｜适合弱解的移动管门与平方根对数支付边界"
FROZEN_CORE = "183af9715e34e714e32df70878e2efb85ed5386f"
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
    source = ROOT / "research/figures/r074i" / FIGURE_DIR
    research_mirror = PUBLIC / "figures/r074i" / FIGURE_DIR
    publication_archive = ROOT / "figures/r074i" / FIGURE_DIR
    for target in (research_mirror, publication_archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    asset_dir = PUBLIC / "assets/r074i"
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
        "figureSchemaVersion": "r074i-publication-compat-v1",
        "figureId": frozen["figureId"],
        "release": CODE,
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Publication metadata wrapper for the frozen R0.74I moving-tube and logarithmic-screen figure package.",
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
        "data": [file_record(publication_archive / "source-data.csv", "r074i-source-data-v1")],
        "sourceData": [],
        "figure": {"widthMillimetres": 180.0, "heightMillimetres": 88.0, "outputs": outputs},
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
<meta name="description" content="适合弱解的 Version-M 移动管门、单尺度 epsilon 桥与平方根对数支付边界">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74i.html"><link rel="stylesheet" href="/bilingual.css">
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
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74I · 2026-09-02</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74I · 完整中文版本</div><h1>__TITLE__</h1>
<p>R0.74H 的双区间估计原本只覆盖光滑周期解。本节把 Version M 推到适合弱解，并证明：若某一尺度上的移动局部能量足够小，就能进入已有的固定柱仅速度 epsilon 正则判据。</p>
<div class="labels"><span class="label">PROVED</span><span class="label">FINITE</span><span class="label">OPEN</span><span class="label">LITERATURE BOUNDARY</span><span class="label">NOT CLAY</span></div>
<p>精确双包家族同时排除了所有低于平方根对数的普适修复；\(\gamma=1/2\) 只是第一个未被否定的端点，不是已证明上界。奇点处所需小量从何而来，仍然开放。</p></div>
<div class="stamp"><strong>状态 · R0.74I</strong><p>Version-M 弱解闭合：PROVED</p><p>单尺度 epsilon 桥：PROVED</p><p>证书 36/36：FINITE</p><p>独立复算 269 字段：FINITE</p><p>图件 82/82：FINITE</p><p>端点上界与尺度传播：OPEN</p><p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>
<section id="s-01"><div class="section-no">01 / 弱解闭合</div><h2>Version M 保留双区间估计</h2>
<p>对笔记范围内的每个周期适合弱解和每个固定可容许尺度 \(R\)，终端锚定的光滑化轨迹可用于局部能量不等式，并得到</p>
<div class="equation">\[\boxed{X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr].}\]</div>
<p>当 \(P_R^M\le1\) 时，线性项由 \(P^{2/3}\) 吸收：</p>
<div class="equation">\[\boxed{P_R^M\le1\quad\Longrightarrow\quad X_R^M\le C(P_R^M)^{2/3}.}\]</div>
<p>这是固定尺度、逐解成立的 Version-M 结果。Version F 的适合弱解扩展没有证明。</p></section>
<section id="s-02"><div class="section-no">02 / 正则门</div><h2>小移动能量进入已有的一尺度判据</h2>
<div class="equation">\[\boxed{\mathcal E^{M,R}(z_0,8R)\le\varepsilon_{\rm tube}\quad\Longrightarrow\quad z_0\text{ 是正则点}.}\]</div>
<div class="equation">\[\boxed{P_R^M\le\varepsilon_P\quad\Longrightarrow\quad z_0\text{ 是正则点}.}\]</div>
<p>这两个命题都以某一给定尺度上的小量为前提。本节没有证明可能奇点处的 \(P_R^M\) 或移动能量必然小。</p></section>
<section id="s-03"><div class="section-no">03 / 移动到固定</div><h2>路径受限后，固定半径柱落入移动管</h2>
<p>终端锚定路径满足 \(\dot X_R=u_R(t,X_R)\)。小移动能量给出</p>
<div class="equation">\[\boxed{|X_R(t)-x_0|\le C R\mathcal E_R^{1/2}.}\]</div>
<p>常数取到足够小时，\(B_{R/2}(x_0)\subset X_R(t)+B_R\)。固定柱中的三次速度量于是满足</p>
<div class="equation">\[\boxed{(R/2)^{-2}\int_{Q_{R/2}(z_0)}|u|^3\le C_I\mathcal E_R^{3/2}.}\]</div>
<p>最后一步调用已有的仅速度一尺度 epsilon 正则判据；移动管本身并不自动产生正则性。</p></section>
<section id="s-04"><div class="section-no">04 / 对数前沿</div><h2>低于平方根对数的普适修复全部失败</h2>
<p>在精确 R0.74F--H 双包族上，对 \(Y_j=X_j\) 和 \(Y_j=\mathfrak C_j\)，Version M 与 Version F 都有</p>
<div class="equation">\[\boxed{\liminf_{j\to\infty}\frac{Y_j}{P_j^{2/3}\sqrt{1+\log_+P_j}}>0.}\]</div>
<p>因此，对每个固定 \(\gamma&lt;1/2\)，不存在统一常数使</p>
<div class="equation">\[\boxed{Y_R\le K P_R^{2/3}(1+\log_+P_R)^\gamma}\]</div>
<p>对所有声明范围内的光滑周期解与尺度成立。该障碍沿高度稀疏的实际支付序列出现，不是对每个大实数 \(P\) 的点态下界。</p></section>
<section id="s-05"><div class="section-no">05 / 端点边界</div><h2>\(\gamma=1/2\) 未被否定，也没有被证明</h2>
<p>在平方根对数端点，现有论证只给正的下比值，不给发散。任何普适端点上界都会迫使尚未证明的匹配支付下界</p>
<div class="equation">\[\boxed{P_j\gtrsim B_j^3R_j^3.}\]</div>
<p>这只是条件推论。不得把它写成冻结解族已经具有的下界，也不得把平方根对数称为已完成的上界定理。</p></section>
<section id="s-06"><div class="section-no">06 / 文献边界</div><h2>移动轨迹与斜柱已有直接先例</h2>
<p><strong>LITERATURE BOUNDARY：</strong>Yang 与 Vasseur--Yang 已使用光滑化流轨迹、参考时刻锚定和单侧后向斜柱；这些几何成分不主张新颖。固定柱插值与仅速度 epsilon 判据也来自已有文献。</p>
<p>限定式主源检索没有找到相同的 Version-M 支付、正环带通量、移动到固定包含与局部标量支付组合。这只是 finite non-hit，不证明新颖性或优先权。</p></section>
<section id="s-07"><div class="section-no">07 / 证据分层</div><h2>解析证明、有限复算与开放命题分开</h2>
<p><strong>PROVED：</strong>固定尺度 Caratheodory 路径、移动测试可容许性、Version-M 弱解双区间估计、路径受限与固定柱包含、仅速度的一尺度 epsilon 桥，以及 \(\gamma&lt;1/2\) 的对数修复排除。</p>
<p><strong>FINITE：</strong>Python 证书 36/36；独立 Ruby 复算 36/36，核对 269 个终端字段且零差异。图件 validator 82/82，24 文件封存通过。有限证书只核对指数代数和图件，不证明 PDE 论证。</p>
<p><strong>OPEN：</strong>Version-F 弱解扩展、奇点处小量机制、跨尺度轨迹比较、端点上界、匹配支付下界与通量的序列稳定性。</p></section>
<section id="s-08"><div class="section-no">08 / 结论边界</div><h2>一尺度门已经存在，缺的是小量来源与传播</h2>
<ul><li>没有证明任何可能奇点自动满足小量条件；</li><li>没有证明小量从一个移动尺度传播到更小尺度；</li><li>没有证明平方根对数端点上界；</li><li>没有排除所有奇点、证明全局光滑或构造 blow-up；</li><li>没有主张新颖性或发表优先权。</li></ul>
<p><strong>NOT CLAY：</strong>任意三维初值的全局正则性与 Clay 千禧年问题仍然开放。</p></section>
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>移动管正则门与对数指数筛选</h2>
<picture><source srcset="/assets/r074i/fig-r074i-moving-tube-log-screen.svg" type="image/svg+xml"><img src="/assets/r074i/fig-r074i-moving-tube-log-screen.png" alt="R0.74I moving-tube regularity gate and square-root logarithmic exponent screen"></picture>
<p><a href="/assets/r074i/fig-r074i-moving-tube-log-screen.pdf">下载矢量 PDF</a> · <a href="/assets/r074i/fig-r074i-moving-tube-log-screen.png">下载 600 dpi PNG</a> · <a href="/assets/r074i/fig-r074i-moving-tube-log-screen.svg">打开 SVG</a> · <a href="/figures/r074i/fig-r074i-moving-tube-log-screen/source-data.csv">精确 source-data.csv</a></p>
<p><a href="/figures/r074i/fig-r074i-moving-tube-log-screen/caption.md">图注</a> · <a href="/figures/r074i/fig-r074i-moving-tube-log-screen/qa-report.md">图件 QA</a> · <a href="/figures/r074i/fig-r074i-moving-tube-log-screen/manifest.json">图件 manifest</a> · <a href="/figures/r074i/fig-r074i-moving-tube-log-screen/validation.json">82 项验证记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/public/figures/r074i/fig-r074i-moving-tube-log-screen">完整 24 文件图包</a></p>
<p class="figure-note">SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是严格蕴含与指数筛选图，不是 DNS、数值仿真或实验数据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>主文、解析审计、精确证书与文献边界</h2><p class="files">
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_suitable_weak_tube_and_log_obstruction.md">规范主文</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_weak_extension_independent_audit.md">弱解扩展独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_epsilon_log_independent_audit.md">epsilon 与对数独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_final_source_rebind_audit.md">最终源文件重绑定审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_report-source.md">完整报告源</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_tube_log_certificate_report.md">证书报告</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_tube_log_certificate.json">冻结 JSON</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074i_tube_log_certificate.py">Python 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r074i_tube_log_certificate_independent.rb">独立 Ruby 实现</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_certificate_independent_audit.md">证书独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_primary_literature_boundary.md">主源文献边界</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_primary_literature_independent_audit.md">文献独立审计</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_gap_matrix.md">23 项证据与缺口矩阵</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_bilingual_dictionary.md">双语边界词典</a> ·
<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074i_freeze_manifest.json">冻结清单</a></p>
<p><a href="/notes/r0-74i.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X，140 节）</a> · <a href="/recap-r0-61-r0-73x.pdf">recap PDF</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>R0.74J</h2><p>检查移动能量小量能否跨尺度传播，并分别决定平方根对数端点上界与匹配支付下界；在此之前不作全局正则性外推。</p></section>
</article></main></body></html>'''
    return page.replace("__VERSION__", VERSION).replace("__TITLE__", TITLE)


def assert_bilingual_dictionary() -> None:
    path = ROOT / "research/r074i_bilingual_dictionary.md"
    if sha256(path) != "3acff1d10887d8c07b9389137bfdbfca1331915ffb3b81870554dcff2c27d530":
        raise RuntimeError("frozen R0.74I bilingual dictionary drift")
    value = path.read_text(encoding="utf-8")
    for marker in ("适合弱解", "平方根对数端点", "PROVED", "FINITE", "OPEN", "NOT CLAY"):
        if marker not in value:
            raise RuntimeError(f"frozen dictionary missing {marker}")


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.74"', f'data-site-version="{VERSION}"', "home version"),
        ('/i18n-en.js?v=1.74', f'/i18n-en.js?v={VERSION}', "home i18n"),
        ('/site-refresh.js?v=1.74.1', f'/site-refresh.js?v={VERSION}.1', "home refresh"),
        ('<strong>v1.74</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "home version stat"),
        ('<span><strong>210</strong>公开研究笔记</span>', '<span><strong>211</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74H</strong>最新研究节点</span>', '<span><strong>R0.74I</strong>最新研究节点</span>', "home latest"),
        ('Research topology · R0.1–R0.74H', 'Research topology · R0.1–R0.74I', "topology label"),
        ('href="#r074h">跳到首页 R0.74H 卡片 →', 'href="#r074i">跳到首页 R0.74I 卡片 →', "jump link"),
        ('href="#r070a">R0.70A–R0.74H：112 节已公开，88 节完整封存', 'href="#r070a">R0.70A–R0.74I：113 节已公开，89 节完整封存', "progress link"),
        ('<span class="route-range">R0.69P–R0.74H</span>', '<span class="route-range">R0.69P–R0.74I</span>', "route range"),
        ('<h3>R0.74H：环带通量修复与双区间闭合</h3>', '<h3>R0.74I：适合弱解移动管门与平方根对数边界</h3>', "route title"),
        ('<p class="tree-current-summary">正环带通量修复大支付端，对任意光滑周期无外力解得到 X≤C(P^{2/3}+P)；小支付端保留 P^{2/3}。</p>', '<p class="tree-current-summary">Version M 已推进到适合弱解；给定尺度上的小移动能量进入既有固定柱 epsilon 判据。所有 gamma&lt;1/2 的对数修复被排除，端点仍开放。</p>', "route summary"),
        ('<p class="tree-path">局部 frame → 双包存活 → 完整分母反例 → 环带通量修复</p>', '<p class="tree-path">环带通量修复 → 适合弱解移动管 → 单尺度 epsilon 门 → 平方根对数边界</p>', "route short path"),
        ('<p class="tree-path"><span>R0.72R–R0.74H：</span>', '<p class="tree-path"><span>R0.72R–R0.74I：</span>', "detailed route range"),
        ('aria-label="R0.69P–R0.74H"', 'aria-label="R0.69P–R0.74I"', "route aria"),
        ('<summary>展开 120 篇公开笔记</summary>', '<summary>展开 121 篇公开笔记</summary>', "route count"),
        ('综述 v1.74 · 2026-09-02', '综述 v1.75 · 2026-09-02', "home footer"),
        ('全站现有 210 篇公开研究笔记', '全站现有 211 篇公开研究笔记', "recap card count"),
    )
    for old, new, label in pairs:
        home = replace_once(home, old, new, label)

    home, n = re.subn(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74I 已把 Version M 推到适合弱解，并建立给定尺度小移动能量到既有 epsilon 判据的桥。下一步要解释小量如何在可能奇点处出现或跨尺度传播；平方根对数端点也仍开放。</span></div>',
        home,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("home focus replacement failed")

    latest = r'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74I · 2026-09-02</p><h2 class="route-map-title" id="latest-release-title">R0.74I｜适合弱解移动管门</h2><p class="route-map-intro">Version M 已推进到适合弱解；给定尺度上的小移动能量进入已有 epsilon 判据。低于平方根对数的修复失败，端点上界仍开放。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74i.pdf">阅读最新 R0.74I 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">211 篇研究笔记总索引</a><a href="#r074i">查看首页 R0.74I 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74I · 113 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>89 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74I</span></div></div></section>'''
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
        '<a class="milestone" href="/notes/r0-74h.html">R0.74H</a>',
        '<a class="milestone" href="/notes/r0-74h.html">R0.74H</a>\n<a class="milestone" href="/notes/r0-74i.html">R0.74I</a>',
        "route I link",
    )
    home = replace_once(
        home,
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74I</span><span class="tree-state current">下一检查点</span></div><h3>R0.74I 下一接口</h3><p>寻找可独立控制、适合弱解极限的 collar-flux 替代量，并检查尺度迭代。</p></article></div>',
        '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74J</span><span class="tree-state current">下一检查点</span></div><h3>R0.74J 下一接口</h3><p>检查移动能量小量的尺度传播，并分别处理平方根对数端点上界与匹配支付下界。</p></article></div>',
        "next route",
    )
    home = home.replace(
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair</p>',
        'localized mixed-covariance four-block size lemma / explicit Gaussian tails → complete-payment obstruction → collar-flux two-regime repair → suitable-weak moving-tube gate / square-root-log frontier</p>',
        1,
    )
    card = r'''          <div class="task-one" id="r074i" data-release="r074i" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74I · 2026-09-02</p><h3>R0.74I｜适合弱解的移动管门与平方根对数支付边界</h3>
            <p>Version M 已推进到适合弱解；给定尺度上的小移动能量进入已有的一尺度 epsilon 判据。</p>
            <p><strong>边界：</strong>低于平方根对数的修复失败；端点上界、奇点处小量与尺度传播仍开放。</p>
            <p><a href="/notes/r0-74i.html"><strong>阅读 R0.74I 完整中文笔记 →</strong></a><br><a href="/notes/r0-74i.pdf">下载同步 PDF</a> · <a href="/assets/r074i/fig-r074i-moving-tube-log-screen.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a></p>
          </div>
'''
    home = replace_once(home, '          <div class="task-one" id="r074h"', card + '          <div class="task-one" id="r074h"', "home I card")
    write_text(HOME, home)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.74"', 'data-site-version="1.75"', "literature version"),
        ('/i18n-en.js?v=1.74', '/i18n-en.js?v=1.75', "literature i18n"),
        ('R0.69P–R0.74H 只列为研究笔记', 'R0.69P–R0.74I 只列为研究笔记', "literature range"),
        ('文献综述 v1.74 · 2026-09-02', '文献综述 v1.75 · 2026-09-02', "literature footer"),
    ):
        page = replace_once(page, old, new, label)
    route = r'<div class="route-step kept"><header><b>R0.74I</b><strong>适合弱解移动管门与平方根对数支付边界</strong></header><p>Version M 已推进到适合弱解；给定尺度上的小移动能量进入已有固定柱 epsilon 判据。精确双包族排除所有 \(\gamma&lt;1/2\) 的普适对数修复，端点上界仍开放。<a href="/notes/r0-74i.html">研究笔记</a> <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> <a href="#r074i-boundary">文献边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74J</b><strong>小量传播与端点决定</strong></header><p>检查移动能量小量的尺度传播，并分别处理平方根对数端点上界与匹配支付下界。</p></div>'
    page, n = re.subn(
        r'<div class="route-step pause"><header><b>开放接口 · R0\.74I</b>.*?</div>',
        lambda _: route,
        page,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise RuntimeError("literature route replacement failed")
    boundary = '''<h3 id="r074i-boundary">R0.74I 的文献与主张边界</h3><p>Yang 与 Vasseur--Yang 已使用光滑化轨迹、参考时刻锚定和单侧后向斜柱；这些几何成分属于先例。限定式检索未找到相同的 Version-M 支付、正环带通量、移动到固定包含与局部标量支付组合，但 finite non-hit 不证明新颖性或优先权。</p><div class="boundary"><strong>R0.74I 的公开边界</strong><p>PROVED、FINITE、OPEN、LITERATURE BOUNDARY 与 NOT CLAY 在研究笔记中分开。一尺度小量可进入既有正则门，但本节没有证明可能奇点处的小量、跨尺度传播或平方根对数端点上界。<a href="/notes/r0-74i.html">阅读完整中文笔记</a>。</p></div>
'''
    page = replace_once(page, '        <section id="references">', boundary + '        <section id="references">', "literature I boundary")
    write_text(LITERATURE, page)


def update_accounting() -> None:
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "publicHtmlNoteCount": 211,
        "postR060PublishedNodeCount": 151,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 168,
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
        "publicHtmlNoteCount": 211,
        "publicPdfNoteCount": 168,
        "postR060PublishedNodeCount": 151,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074j",
        "latestReleaseGate": "tests/r074i-tube-log-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074i-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "scripts/add-r074i-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074i-pdf.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_path)}
    write_json(manifest_path, manifest)


def main() -> None:
    if "--note-only" in sys.argv:
        write_text(PUBLIC / "notes/r0-74i.html", render_note())
        assert_bilingual_dictionary()
        print(json.dumps({"status": "note-regenerated", "release": CODE}, ensure_ascii=False))
        return
    assert_recap()
    copy_figures()
    write_text(PUBLIC / "notes/r0-74i.html", render_note())
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
