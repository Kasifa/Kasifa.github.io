#!/usr/bin/env python3
"""Generate the note-only R0.73Z public release from frozen research bytes.

The research handoff and the publication pipeline validate the frozen source
hashes.  This script owns only reader-facing HTML, route accounting, copied
figure assets, and publication metadata.  The R0.73X recap is byte-preserved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

from r073y_release_content import _markdown_blocks, _slug


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/r073z_report-source.md"
HANDOFF = ROOT / "release/handoffs/r073z.json"
FIGURE_SOURCE = ROOT / "research/figures/r073z/fig-r073z-covariance-separation"
NOTE = ROOT / "public/notes/r0-73z.html"
HOME = ROOT / "public/research-review.html"
LITERATURE = ROOT / "public/literature-review.html"
SITE_VERSION = ROOT / "public/site-version.json"
MANIFEST = ROOT / "research/release-manifest.json"
INVENTORY = ROOT / "research/formal-archive-inventory.json"
DICTIONARY = ROOT / "research/r073z_bilingual_dictionary.md"
RECAP_HTML = ROOT / "public/recap-r0-61-r0-73x.html"
RECAP_PDF = ROOT / "public/recap-r0-61-r0-73x.pdf"
RECAP_HASHES = {
    RECAP_HTML: "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776",
    RECAP_PDF: "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa",
}
SOURCE_COMMIT = "7321e8a2c50817b58edd6e3bf1dd35bb3a24576b"
FIGURE_PACKAGE_COMMIT = "845a8b825f06513c454807ae770bcaee6d0d3b04"

TITLE = "R0.73Z｜正三次 heat covariance 的有限性障碍与能量兼容修复"
SUBTITLE = "从初始端点发散，到能量级有限性与 pressure-active 分离见证"
NEXT_GATE = (
    "下一节只攻击一个接口：把 K_D 的 global energy upper bound 局部化为 "
    "E^square(z_0,4R)^{3/2} 加最小、明确、可缩放的 exterior velocity/gradient tail，"
    "并用它支付 crossed witness 激活的 Q_s·∇χ。先完成 core/exterior split 与 crossed-family "
    "scaling test；若局部付款失败，就发布 exact counterexample，不提前重启 quotient coercivity。"
)


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


def report_sections(report: str) -> tuple[list[tuple[str, str, str]], str]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if len(matches) != 11:
        raise RuntimeError(f"R0.73Z report section count drift: {len(matches)}")
    used: set[str] = set()
    rows: list[tuple[str, str, str]] = []
    references = ""
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        heading = match.group(1).strip()
        body = report[match.end():end].strip()
        if heading == "参考文献":
            references = _markdown_blocks(body)
            continue
        number_match = re.fullmatch(r"(\d+)\.\s+(.+)", heading)
        if number_match is None:
            raise RuntimeError(f"unexpected R0.73Z heading: {heading}")
        title = number_match.group(2)
        rows.append((number_match.group(1), title, _slug(title, used)))
        public_body = _markdown_blocks(body).replace(
            "我们还没有得到", "目前尚未得到"
        )
        rows[-1] += (public_body,)
    return rows, references


def note_html(report: str) -> str:
    sections, references = report_sections(report)
    section_html = "\n".join(
        f'<section id="{slug}"><div class="section-no">{number.zfill(2)} / canonical report</div>'
        f'<h2>{title}</h2>{body}</section>'
        for number, title, slug, body in sections
    )
    boundary = (
        '<section id="release-boundary" class="callout"><div class="section-no">B / Exact claim boundary</div>'
        '<h2>证明、有限证书、开放问题与 Clay 边界分开</h2>'
        '<p>PROVED：originalDThreeHalvesScaling=PROVED_ANALYTICALLY；smoothCylinderFiniteness=PROVED_ANALYTICALLY；'
        'initialEndpointEnergyClassFiniteness=FALSE_BY_EXACT_LERAY_HOPF_SHEAR；'
        'energyCompatibleKDUpperBound=PROVED_ANALYTICALLY；exactKernelKD=PROVED_ANALYTICALLY；'
        'localCenteredOscillationProductLowerBound=PROVED_ANALYTICALLY；'
        'pressureActiveCrossedFamily=PROVED_ANALYTICALLY</p>'
        '<p>FINITE：covarianceFourierCertificate=FINITE_CROSS_CHECK_ONLY；'
        'formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED；'
        'formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES；formalFigureRows=201；'
        'navierStokesSimulation=NOT_RUN；directNumericalSimulation=NOT_RUN；'
        'ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=false</p>'
        '<p>OPEN：interiorSuitableWeakFiniteness=OPEN；localKDUpperPayment=OPEN；'
        'genuinelyThreeDimensionalPressureActiveInvisibleFamily=OPEN；'
        'scaleUniformQuotientCoercivity=OPEN；epsilonRegularity=OPEN；'
        'arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN</p>'
        '<p>本节证明初始端点障碍、一个能量兼容的正三次观测以及 pressure-active 分离见证。'
        '它不证明 CKN coercivity、epsilon regularity、奇性或任意三维全局正则性。NOT CLAY。</p></section>'
    )
    figure = (
        '<section id="figure"><div class="section-no">F / Journal figure</div>'
        '<h2>端点障碍、能量修复与 pressure-active 分离</h2>'
        '<p><img src="/assets/r073z/fig-r073z-covariance-separation.svg" '
        'alt="R0.73Z covariance separation, endpoint obstruction, and pressure-active exact kernel"></p>'
        '<p><a href="/assets/r073z/fig-r073z-covariance-separation.pdf">下载矢量 PDF</a> · '
        '<a href="/assets/r073z/fig-r073z-covariance-separation.png">下载 600 dpi PNG</a> · '
        '<a href="/assets/r073z/fig-r073z-covariance-separation.svg">打开 SVG</a></p>'
        '<p>图中 201 行是解析公式的确定性取值，不是 DNS、simulation、奇性候选或有限采样证明。NOT CLAY。</p></section>'
    )
    reproduce = (
        '<section id="reproduce"><div class="section-no">R / Reproduction</div><h2>冻结证明、审计与证书</h2>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073z_finiteness_obstruction_and_repair.md">有限性障碍与修复证明</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073z_pressure_active_kernel.md">pressure-active kernel</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073z_finiteness_independent_audit.md">独立审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073z_primary_literature_audit.md">一手文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073z_evidence_gap_matrix.md">主张—证据矩阵</a></p>'
        '<p><a href="/notes/r0-73z.pdf">同步研究笔记 PDF</a> · '
        '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a> · '
        '<a href="/recap-r0-61-r0-73x.pdf">PDF</a></p></section>'
    )
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="1.66">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title><meta name="description" content="{SUBTITLE}"><link rel="canonical" href="https://kasifa.github.io/notes/r0-73z.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v=1.66"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{--paper:#f3ecd8;--ink:#26231d;--rule:#8b2f2b;--muted:#625d52}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.75 Georgia,"Noto Serif SC",serif}}.top{{border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}main{{width:min(920px,90vw);margin:auto}}.hero{{padding:56px 0 28px;border-bottom:1px solid var(--ink)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,300px);gap:2rem}}h1{{font-size:clamp(2rem,6vw,4rem);line-height:1.05}}h2{{margin-top:3rem;color:var(--rule)}}.stamp,.section-no{{font:700 12px/1.5 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}}article{{padding:20px 0 80px}}p,.callout{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:#fff8e8;padding:14px;border-left:4px solid var(--rule)}}a{{color:#702824}}img{{max-width:100%;height:auto}}.callout{{padding:1rem 1.25rem;background:#fff8e8;border:1px solid #c8bfa8}}@media(max-width:720px){{html,body{{max-width:100%;overflow-x:hidden}}body{{font-size:15px}}main,article,section{{min-width:0}}.hero-inner{{grid-template-columns:1fr}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{.top{{display:none}}body{{background:white;font-size:10.5pt}}main{{width:auto}}.hero{{padding-top:0}}a{{color:inherit;text-decoration:none}}section{{break-inside:auto}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.73Z · NOT CLAY</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.73Z · EXACT ANALYTIC THEOREMS / FINITE CERTIFICATE</div><h1>{TITLE}</h1><p>{SUBTITLE}</p><p>原候选 D<sub>ii,s</sub><sup>3/2</sup> 在 L<sup>2</sup> 初始迹可发散；修复量 D<sub>ii,s</sub>√k<sub>s</sub> 由 Leray energy 支付，并由 crossed exact family 分离 pressure-cutoff debt。</p></div><div class="stamp"><strong>状态 · R0.73Z 完成</strong><p>版本 R0.73Z · 2026-09-01</p><p>analytic theorems：PROVED</p><p>Fourier certificate：FINITE</p><p>local payment / epsilon regularity：OPEN</p><p>LOCAL DIRECT / NO DGX</p><p>NOT CLAY</p></div></div></header>
<article>{section_html}{figure}{boundary}{reproduce}<section id="references"><div class="section-no">References</div><h2>参考文献</h2>{references}</section></article>
</main></body></html>'''


def copy_figures() -> None:
    archive = ROOT / "figures/r073z/fig-r073z-covariance-separation"
    public_archive = ROOT / "public/figures/r073z/fig-r073z-covariance-separation"
    for target in (archive, public_archive):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(FIGURE_SOURCE, target)

    # Adapt only the publication archive mirror to the repository's legacy
    # validator. The frozen research package and public evidence mirror remain
    # byte-exact, including their newer `producer.py` manifest schema.
    (archive / "producer.py").rename(archive / "plot.py")
    data_names = (
        "source-data.csv", "results.json", "environment.json", "progress.ndjson",
        "resource-log.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
        "validation.json", "qa-report.md",
    )
    data = [
        {
            "path": name,
            "schema": "r073z-package-record-v1",
            "bytes": (archive / name).stat().st_size,
            "sha256": sha256(archive / name),
        }
        for name in data_names
    ]
    outputs = []
    for name, schema in (
        ("figure.svg", "svg-journal-master"),
        ("figure.pdf", "one-page-pdf-journal-master"),
        ("figure.png", "png-journal-master"),
    ):
        record = {
            "path": name,
            "schema": schema,
            "bytes": (archive / name).stat().st_size,
            "sha256": sha256(archive / name),
        }
        if name.endswith(".png"):
            record["dpi"] = 600
        outputs.append(record)
    asset_records = []
    for extension in ("pdf", "png", "svg"):
        source = archive / f"figure.{extension}"
        asset_records.append({
            "path": f"public/assets/r073z/fig-r073z-covariance-separation.{extension}",
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
        })
    compatibility_manifest = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r073z-covariance-separation-publication-compat-v1",
        "figureId": "fig-r073z-covariance-separation",
        "release": "R0.73Z",
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "Does the proposed positive cubic heat covariance remain finite at the suitable-weak initial endpoint, and what energy-compatible repair survives the exact kernel tests?",
        "supportedClaim": "The original D_ii,s^(3/2) observable fails energy-class initial-endpoint finiteness; D_ii,s sqrt(k_s) is nonnegative, scale invariant, cubic, and Leray-energy controlled. Finite rows only cross-check analytic formulas.",
        "createdAt": "2026-09-01T08:35:36Z",
        "git": {
            "repository": "https://github.com/Kasifa/Kasifa.github.io.git",
            "sourceCommit": SOURCE_COMMIT,
            "certificateCommit": FIGURE_PACKAGE_COMMIT,
            "dirtyAtCertifiedRun": False,
        },
        "computation": {
            "kind": "exact-formula-audit",
            "configuration": "config.json",
            "precision": "closed-form identities audited in IEEE-754 binary64",
            "solver": "none",
            "formalCommand": "python plot.py --render; python validate.py --write-metadata --confirm-visual-qa; python validate.py --verify-only --confirm-visual-qa",
            "wallTimeSeconds": 2.835454,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
        },
        "compute": {
            "host": "local workstation (hostname intentionally omitted)",
            "operatingSystem": "macOS-26.6.2-arm64-arm-64bit",
            "cpu": "arm64 / local CPU",
            "memoryGiB": 36.0,
            "processes": 1,
            "threadsPerProcess": 1,
            "dgxUsed": False,
        },
        "environment": {
            "python": "3.12.13",
            "packagesLock": "requirements.txt",
            "packages": {"numpy": "2.3.5", "pillow": "12.3.0", "reportlab": "4.4.9", "pypdf": "6.10.0"},
        },
        "data": data,
        "sourceData": [{
            "location": "repository source commit",
            "fileName": "research/r073z_report-source.md",
            "bytes": REPORT.stat().st_size,
            "sha256": sha256(REPORT),
            "extractionCommand": "git show 7321e8a2c50817b58edd6e3bf1dd35bb3a24576b:research/r073z_report-source.md",
        }],
        "figure": {"widthMillimetres": 178.0, "heightMillimetres": 74.0, "outputs": outputs},
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
        "claimBoundary": {
            "analyticConsequencesOnly": True,
            "finiteRowsProveQuantifiers": False,
            "globalRegularity": False,
            "notClay": True,
        },
        "publication": {
            "archiveDirectory": "public/figures/r073z/fig-r073z-covariance-separation",
            "researchArchiveDirectory": "research/figures/r073z/fig-r073z-covariance-separation",
            "directory": "public/assets/r073z",
            "fileStem": "fig-r073z-covariance-separation",
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "releaseSourceCommit": SOURCE_COMMIT,
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "assets": asset_records,
        },
        "provenance": {
            "frozenResearchManifestSha256": sha256(FIGURE_SOURCE / "manifest.json"),
            "compatibilityScope": "publication archive metadata only; scientific files and public masters are unchanged",
        },
    }
    write_json(archive / "manifest.json", compatibility_manifest)
    ledger_names = sorted(
        path.name for path in archive.iterdir()
        if path.is_file() and path.name not in {"SHA256SUMS", ".DS_Store"}
    )
    write_text(
        archive / "SHA256SUMS",
        "".join(f"{sha256(archive / name)}  {name}\n" for name in ledger_names),
    )
    assets = ROOT / "public/assets/r073z"
    assets.mkdir(parents=True, exist_ok=True)
    for extension in ("pdf", "png", "svg"):
        shutil.copy2(FIGURE_SOURCE / f"figure.{extension}", assets / f"fig-r073z-covariance-separation.{extension}")


def update_home(value: str) -> str:
    value = replace_once(value, 'data-site-version="1.65"', 'data-site-version="1.66"', "home version attribute")
    value = replace_once(value, '/i18n-en.js?v=1.65', '/i18n-en.js?v=1.66', "home i18n cache")
    value = replace_once(value, '<strong>v1.65</strong>网页版本', '<strong>v1.66</strong>网页版本', "home version badge")
    value = replace_once(value, "综述 v1.65 · 2026-09-01", "综述 v1.66 · 2026-09-01", "home footer version")
    value = replace_once(value, '<strong>201</strong>公开研究笔记', '<strong>202</strong>公开研究笔记', "home note count")
    value = replace_once(
        value,
        "R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 201 篇公开研究笔记",
        "R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 202 篇公开研究笔记",
        "home recap card public-note count",
    )
    value = replace_once(value, '<strong>R0.73Y</strong>最新研究节点', '<strong>R0.73Z</strong>最新研究节点', "home latest node")
    old_focus = re.search(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', value, re.S)
    if old_focus is None:
        raise RuntimeError("home current-focus row missing")
    focus = '<div class="summary-item"><strong>我目前关注</strong><span>R0.73Z 已关闭 D_{ii,s}^{3/2} 的能量类初始端点有限性，并以 D_{ii,s}√k_s 给出可由 Leray energy 支付的正三次修复。下一步只处理 K_D 的局部 upper payment 与 pressure-cutoff debt；quotient coercivity、epsilon regularity、任意三维全局正则性和 Clay 仍为 OPEN。</span></div>'
    value = value[:old_focus.start()] + focus + value[old_focus.end():]
    spotlight = re.search(r'<section class="route-overview latest-release-spotlight".*?</section>', value, re.S)
    if spotlight is None:
        raise RuntimeError("latest-release spotlight missing")
    new_spotlight = '<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.73Z · 2026-09-01</p><h2 class="route-map-title" id="latest-release-title">R0.73Z｜正三次 heat covariance 的有限性障碍与能量兼容修复</h2><p class="route-map-intro">D_{ii,s}^{3/2} 形式上尺度正确、三次齐次且能检测 shear kernel，但在 L² 初始迹可发散。修复量 D_{ii,s}√k_s 保留正性与临界齐次性，并由 Leray energy 支付；crossed exact family 进一步显示 pressure-cutoff debt 必须单独结算。NOT CLAY。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73z.pdf">阅读最新 R0.73Z 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">202 篇研究笔记总索引</a><a href="#r073z">查看首页完整 R0.73Z 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73Z · 104 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>80 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73Z</span></div></div></section>'
    value = value[:spotlight.start()] + new_spotlight + value[spotlight.end():]
    for old, new, label in [
        ("Research topology · R0.1–R0.73Y", "Research topology · R0.1–R0.73Z", "route topology"),
        ('href="#r073y">跳到首页 R0.73Y 卡片', 'href="#r073z">跳到首页 R0.73Z 卡片', "route jump"),
        ("R0.70A–R0.73Y：103 节已公开，79 节完整封存", "R0.70A–R0.73Z：104 节已公开，80 节完整封存", "route counts"),
        ("R0.72R–R0.73Y：", "R0.72R–R0.73Z：", "route tail range"),
        ('<span class="route-range">R0.69P–R0.73Y</span>', '<span class="route-range">R0.69P–R0.73Z</span>', "route range"),
        ('aria-label="R0.69P–R0.73Y"', 'aria-label="R0.69P–R0.73Z"', "route aria range"),
        ("展开 111 篇公开笔记", "展开 112 篇公开笔记", "current route note count"),
        ('<a class="milestone" href="/notes/r0-73y.html">R0.73Y</a>', '<a class="milestone" href="/notes/r0-73y.html">R0.73Y</a>\n                  <a class="milestone" href="/notes/r0-73z.html">R0.73Z</a>', "route note link"),
    ]:
        value = replace_once(value, old, new, label)
    value = replace_once(value, 'R0.73Y：exact shear kernel、全振幅零 production、A != 0 时严格正 heat covariance 与 production-only no-go 已分列', 'R0.73Z：初始端点有限性障碍、能量兼容正三次修复与 pressure-active 分离已分列', "current route title")
    summary_match = re.search(r'<p class="tree-current-summary">.*?</p>', value, re.S)
    if summary_match is None:
        raise RuntimeError("tree current summary missing")
    current_summary = '<p class="tree-current-summary">R0.73Y 关闭 production-only coercivity；R0.73Z 又证明 D_{ii,s}^{3/2} 在能量类初始迹可发散，并以 D_{ii,s}√k_s 建立 Leray 可支付的正三次修复。crossed pressure-active exact family 表明 local pressure debt 仍须独立结算。NOT CLAY。</p>'
    value = value[:summary_match.start()] + current_summary + value[summary_match.end():]
    value = replace_once(value, 'exact shear all-scale production obstruction</p>', 'exact shear all-scale production obstruction → positive-covariance endpoint obstruction / energy-compatible repair / pressure-active separation</p>', "current route path")
    next_node = re.search(r'<div class="tree-row">\s*<article class="tree-node next">.*?</article>\s*</div>', value, re.S)
    if next_node is None:
        raise RuntimeError("next route node missing")
    next_html = f'<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74A</span><span class="tree-state current">下一检查点</span></div><h3>R0.74A 下一接口</h3><p>{NEXT_GATE}</p></article></div>'
    value = value[:next_node.start()] + next_html + value[next_node.end():]
    card = f'''<div class="task-one" id="r073z" data-release="r073z" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73Z · 2026-09-01</p><h3>{TITLE}</h3>
            <p>原候选 \(D_{{ii,s}}^{{3/2}}\) 在 smooth cylinder 内有限，却可在 energy-class 初始迹发散。修复量 \(D_{{ii,s}}\sqrt{{k_s}}\) 保留非负性、尺度不变性和三次齐次，并由 Leray energy 直接支付。</p>
            <p>crossed exact NSE family 同时满足 \(\Pi_s=\mathscr S_s=0\)，但指定 pressure covariance 与 local cutoff debt 非零；因此不能只 quotient 零压 shear kernel。</p>
            <p><strong>证明边界：</strong>PROVED：initialEndpointEnergyClassFiniteness=FALSE_BY_EXACT_LERAY_HOPF_SHEAR；energyCompatibleKDUpperBound=PROVED_ANALYTICALLY；exactKernelKD=PROVED_ANALYTICALLY；pressureActiveCrossedFamily=PROVED_ANALYTICALLY</p>
            <p><strong>有限边界：</strong>FINITE：covarianceFourierCertificate=FINITE_CROSS_CHECK_ONLY；formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES；formalFigureRows=201；ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=false</p>
            <p><strong>开放边界：</strong>OPEN：interiorSuitableWeakFiniteness=OPEN；localKDUpperPayment=OPEN；scaleUniformQuotientCoercivity=OPEN；epsilonRegularity=OPEN；arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN。NOT CLAY。</p>
            <p><a href="/notes/r0-73z.html"><strong>阅读 R0.73Z 研究笔记 →</strong></a><br><a href="/notes/r0-73z.pdf">下载同步 PDF</a> · <a href="/assets/r073z/fig-r073z-covariance-separation.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a></p>
            <p><strong style="color:var(--gold)">下一发布门（R0.74A）：</strong>&nbsp;{NEXT_GATE}</p>
          </div>
          '''
    marker = '<div class="task-one" id="r073y" data-release="r073y"'
    if value.count(marker) != 1:
        raise RuntimeError("R0.73Y home card marker drift")
    value = value.replace(marker, card + marker, 1)
    return value


def update_literature(value: str) -> str:
    value = replace_once(value, 'data-site-version="1.65"', 'data-site-version="1.66"', "literature version attribute")
    value = replace_once(value, '/i18n-en.js?v=1.65', '/i18n-en.js?v=1.66', "literature i18n cache")
    value = replace_once(value, "文献综述 v1.65 · 2026-09-01", "文献综述 v1.66 · 2026-09-01", "literature footer")
    value = replace_once(value, "R0.69P–R0.73Y 只列为研究笔记", "R0.69P–R0.73Z 只列为研究笔记", "literature route endpoint")
    next_route = re.search(
        r'<div class="route-step pause"><header><b>开放接口 · R0\.73Z</b>.*?</div>',
        value,
        re.S,
    )
    if next_route is None:
        raise RuntimeError("literature next-route interface missing")
    next_route_html = (
        '<div class="route-step kept"><header><b>R0.73Z</b>'
        '<strong>positive-covariance endpoint obstruction and energy-compatible repair</strong></header>'
        f'<p><strong>{TITLE}</strong></p>'
        '<p>R0.70A–R0.73Z：104 节已公开，80 节完整封存。</p>'
        '<p>初始端点障碍、能量兼容修复与 pressure-active 分离已分别记录。 '
        '<a href="/notes/r0-73z.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> '
        '<a href="#r073z-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.74A</b>'
        '<strong>local K_D payment and pressure-cutoff debt</strong></header>'
        f'<p>{NEXT_GATE}</p></div>'
    )
    value = value[:next_route.start()] + next_route_html + value[next_route.end():]
    insert_marker = '          <ol class="criteria">'
    block = '<h3 id="r073z-boundary">R0.73Z：positive covariance 的初始端点障碍、能量修复与 pressure-active 分离</h3><p>原 D_s^{3/2} 候选的尺度与 smooth-cylinder 性质成立，但 general energy-class 初始端点有限性被 exact Leray--Hopf shear 否定；D_s√k_s 的 global periodic upper bound 则由 Leray energy 支付。crossed classical exact family 同时给出零 production 与非零指定 pressure covariance。限定式检索未定位相同 mixed observable；non-hit 不证明 novelty 或 priority。<a href="/notes/r0-73z.html">阅读 R0.73Z 研究笔记</a>。</p><div class="boundary"><strong>R0.73Z 的主张边界</strong><p>PROVED：initialEndpointEnergyClassFiniteness=FALSE_BY_EXACT_LERAY_HOPF_SHEAR；energyCompatibleKDUpperBound=PROVED_ANALYTICALLY；exactKernelKD=PROVED_ANALYTICALLY；localCenteredOscillationProductLowerBound=PROVED_ANALYTICALLY；pressureActiveCrossedFamily=PROVED_ANALYTICALLY</p><p>FINITE：covarianceFourierCertificate=FINITE_CROSS_CHECK_ONLY；formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES；formalFigureRows=201；ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=false</p><p>OPEN：interiorSuitableWeakFiniteness=OPEN；localKDUpperPayment=OPEN；genuinelyThreeDimensionalPressureActiveInvisibleFamily=OPEN；scaleUniformQuotientCoercivity=OPEN；epsilonRegularity=OPEN；arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN。NOT CLAY。</p></div>\n'
    value = replace_once(value, insert_marker, block + insert_marker, "literature R0.73Z boundary")
    return value


def update_metadata() -> None:
    site = json.loads(SITE_VERSION.read_text(encoding="utf-8"))
    site.update({
        "version": "1.66", "latestRelease": "R0.73Z", "publicHtmlNoteCount": 202,
        "postR060PublishedNodeCount": 142, "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X", "publicPdfNoteCount": 159,
        "publishedDate": "2026-09-01",
    })
    write_json(SITE_VERSION, site)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": "r073z", "siteVersion": "1.66", "publicHtmlNoteCount": 202,
        "postR060PublishedNodeCount": 142, "postR060RecapNodeCount": 140,
        "nextRelease": "r074a", "postR070APublishedReleaseCount": 104,
        "postR070AFormalSealedReleaseCount": 80, "publicPdfNoteCount": 159,
        "latestReleaseGate": "tests/r073z-covariance-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073z-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r073z-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r073z-pdfs.mjs",
        "latestRecapRelease": "r073x",
    })
    write_json(MANIFEST, manifest)
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r073z" not in inventory[key]:
            inventory[key].append("r073z")
    inventory.update({
        "latestPublishedRelease": "r073z", "publishedReleaseCount": 104,
        "formalSealedReleaseCount": 80, "legacyFormalFigureBacklogCount": 24,
    })
    write_json(INVENTORY, inventory)
    # Bind the inventory digest only after the inventory update.
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["formalArchiveInventory"]["sha256"] = sha256(INVENTORY)
    write_json(MANIFEST, manifest)
    write_text(ROOT / "VERSION", "1.66\n")


def write_dictionary() -> None:
    write_text(DICTIONARY, f'''# R0.73Z bilingual release dictionary

**Route:** LOCAL DIRECT / NO DGX  
**DGX used:** false

| Public Chinese | Reviewed English |
|---|---|
| {TITLE} | R0.73Z | Finiteness obstruction for a positive cubic heat covariance and an energy-compatible repair |
| {SUBTITLE} | From divergence at the initial endpoint to an energy-class finite observable and a pressure-active separation witness |
| 初始端点有限性障碍 | Initial-endpoint finiteness obstruction |
| 能量兼容正三次修复 | Energy-compatible positive cubic repair |
| pressure-active 分离见证 | Pressure-active separation witness |
| 证明、有限证书、开放问题与 Clay 边界分开 | Proofs, finite certificates, open problems, and the Clay boundary are kept separate |
| 本节不证明 CKN coercivity、epsilon regularity、奇性或任意三维全局正则性。 | This section does not prove CKN coercivity, epsilon regularity, singularity formation, or arbitrary three-dimensional global regularity. |
| NOT CLAY。 | NOT CLAY. |

Mathematical tokens, theorem quantifiers, certificate payloads, source-data rows,
and formal-figure science remain byte-frozen in the research handoff.
''')


def build() -> None:
    assert_recap()
    if SITE_VERSION.is_file():
        current_site = json.loads(SITE_VERSION.read_text(encoding="utf-8"))
        if current_site.get("version") == "1.66" and current_site.get("latestRelease") == "R0.73Z":
            copy_figures()
            check()
            return
    report = REPORT.read_text(encoding="utf-8")
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    if handoff["releaseId"] != "r073z" or handoff["translationRoute"] != "LOCAL_DIRECT_NO_DGX":
        raise RuntimeError("R0.73Z handoff drift")
    write_text(NOTE, note_html(report))
    copy_figures()
    write_text(HOME, update_home(HOME.read_text(encoding="utf-8")))
    write_text(LITERATURE, update_literature(LITERATURE.read_text(encoding="utf-8")))
    update_metadata()
    write_dictionary()
    # Generate the latest-first index from the now-current site-version ledger.
    import subprocess
    subprocess.run(["python3", str(ROOT / "scripts/generate_note_index.py")], cwd=ROOT, check=True)
    assert_recap()


def check() -> None:
    assert_recap()
    expected_site = {
        "version": "1.66", "latestRelease": "R0.73Z", "publicHtmlNoteCount": 202,
        "postR060PublishedNodeCount": 142, "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X", "publicPdfNoteCount": 159,
    }
    site = json.loads(SITE_VERSION.read_text(encoding="utf-8"))
    for key, expected in expected_site.items():
        if site.get(key) != expected:
            raise RuntimeError(f"site-version {key} drift")
    note = NOTE.read_text(encoding="utf-8")
    for token in ("PROVED", "FINITE", "OPEN", "NOT CLAY", "LOCAL DIRECT / NO DGX"):
        if token not in note:
            raise RuntimeError(f"public note missing boundary token {token}")
    if 'inlineMath:[["\\\\(","\\\\)"]]' not in note or 'displayMath:[["\\\\[","\\\\]"]]' not in note:
        raise RuntimeError("public note MathJax delimiters are not JavaScript-safe")
    if (ROOT / "public/recap-r0-61-r0-73z.html").exists() or (ROOT / "public/recap-r0-61-r0-73z.pdf").exists():
        raise RuntimeError("non-milestone R0.73Z recap must not exist")
    for extension in ("pdf", "png", "svg"):
        target = ROOT / f"public/assets/r073z/fig-r073z-covariance-separation.{extension}"
        if target.read_bytes() != (FIGURE_SOURCE / f"figure.{extension}").read_bytes():
            raise RuntimeError(f"published figure {extension} differs from frozen source")
    public_archive = ROOT / "public/figures/r073z/fig-r073z-covariance-separation"
    for source in FIGURE_SOURCE.iterdir():
        if source.is_file() and (public_archive / source.name).read_bytes() != source.read_bytes():
            raise RuntimeError(f"public evidence mirror differs from frozen source: {source.name}")
    if "r073z" not in json.loads(INVENTORY.read_text(encoding="utf-8"))["formalSealedReleases"]:
        raise RuntimeError("formal archive inventory omits r073z")
    if "R0.74A" not in HOME.read_text(encoding="utf-8"):
        raise RuntimeError("home route does not advance to R0.74A")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only:
        check()
    else:
        build()
        check()
    print(json.dumps({"release": "R0.73Z", "checked": True, "recapGenerated": False, "translationPath": "LOCAL_DIRECT_NO_DGX", "dgxUsed": False}))


if __name__ == "__main__":
    main()
