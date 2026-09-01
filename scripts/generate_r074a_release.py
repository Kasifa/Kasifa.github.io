#!/usr/bin/env python3
"""Generate the note-only R0.74A public release from frozen research bytes.

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

from r073y_release_content import _markdown_blocks


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/r074a_localized_kd_size_lemma.md"
REPORT_ZH = ROOT / "research/r074a_localized_kd_size_lemma_zh.md"
HANDOFF = ROOT / "release/handoffs/r074a.json"
FIGURE_SOURCE = ROOT / "research/figures/r074a/fig-r074a-localized-kd-payments"
NOTE = ROOT / "public/notes/r0-74a.html"
HOME = ROOT / "public/research-review.html"
LITERATURE = ROOT / "public/literature-review.html"
SITE_VERSION = ROOT / "public/site-version.json"
MANIFEST = ROOT / "research/release-manifest.json"
INVENTORY = ROOT / "research/formal-archive-inventory.json"
DICTIONARY = ROOT / "research/r074a_bilingual_dictionary.md"
RECAP_HTML = ROOT / "public/recap-r0-61-r0-73x.html"
RECAP_PDF = ROOT / "public/recap-r0-61-r0-73x.pdf"
RECAP_HASHES = {
    RECAP_HTML: "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776",
    RECAP_PDF: "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa",
}
SOURCE_COMMIT = "391debac9d48158ab4b0f90edf873150849e6e57"
FIGURE_PACKAGE_COMMIT = "7bad69a09651ea870cf463640ffff0f34a849cea"

TITLE = "R0.74A｜混合 heat covariance 的局部 size lemma"
SUBTITLE = "core 由局部能量支付，exterior 由两个显式 Gaussian 二次尾支付"
NEXT_GATE = (
    "下一节只检查新 velocity endpoint tail 与复用的 gradient tail，能否在 suitable-weak "
    "blow-up 序列中由更小柱的数据控制、吸收或替换为弱稳定的 coupled tail。先做 time-supremum "
    "obstruction、lower-semicontinuity 与 scale-uniformity 检查；任何失败都记录为 exact "
    "counterexample，不在 tail payment 闭合前提出 quotient coercivity。"
)

SECTION_SLUGS = {
    "1": "frozen-definitions-and-the-clock-qualification",
    "2": "lifted-annuli-and-the-two-quadratic-exterior-inputs",
    "3": "positive-core-exterior-majorization",
    "4": "the-localized-size-theorem",
    "5": "why-the-older-exterior-functional-is-insufficient",
    "6": "proven-rows-and-remaining-gates",
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


def markdown_blocks_tex_safe(value: str) -> str:
    """Keep Markdown emphasis from consuming asterisks inside inline TeX."""
    sentinel = "\ue000"
    if sentinel in value:
        raise RuntimeError("R0.74A report contains the inline-TeX sentinel")
    protected = re.sub(
        r"\\\([\s\S]*?\\\)",
        lambda match: match.group(0).replace("*", sentinel),
        value,
    )
    return _markdown_blocks(protected).replace(sentinel, "*")


def report_sections(report: str) -> tuple[list[tuple[str, str, str]], str]:
    matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", report))
    if len(matches) != 6:
        raise RuntimeError(f"R0.74A report section count drift: {len(matches)}")
    rows: list[tuple[str, str, str]] = []
    references = ""
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(report)
        heading = match.group(1).strip()
        body = report[match.end():end].strip()
        number_match = re.fullmatch(r"(\d+)\.\s+(.+)", heading)
        if number_match is None:
            raise RuntimeError(f"unexpected R0.74A heading: {heading}")
        title = number_match.group(2)
        number = number_match.group(1)
        rows.append((number, title, SECTION_SLUGS[number]))
        public_body = markdown_blocks_tex_safe(body)
        public_body = re.sub(r"<p>### (.*?)</p>", r"<h3>\1</h3>", public_body)
        public_body = re.sub(r"<p>#### (.*?)</p>", r"<h4>\1</h4>", public_body)
        rows[-1] += (public_body,)
    return rows, references


def note_html(report: str) -> str:
    sections, references = report_sections(report)
    section_html = "\n".join(
        f'<section id="{slug}"><div class="section-no">{number.zfill(2)} / 规范报告</div>'
        f'<h2>{title}</h2>{body}</section>'
        for number, title, slug, body in sections
    )
    boundary = (
        '<section id="release-boundary" class="callout"><div class="section-no">B / 结论边界</div>'
        '<h2>证明、有限证书、开放问题与 Clay 边界分开</h2>'
        '<p>PROVED：positiveFourBlockMajorization=PROVED_ANALYTICALLY；'
        'clockMatchedLocalEnergyTailBound=PROVED_ANALYTICALLY；'
        'pressureCutoffInterface=PROVED_BY_INHERITANCE_AND_ANALYTIC_COMBINATION；'
        'oldExteriorPackageOnlyControl=FALSE_BY_EXACT_ENERGY_CLASS_PACKETS；'
        'navierStokesScaling=PROVED_ANALYTICALLY</p>'
        '<p>FINITE：velocityEndpointTail=FINITE_FOR_EVERY_STATED_PERIODIC_ENERGY_CLASS_FIELD；'
        'gradientTail=FINITE_AND_IDENTICAL_TO_R073X_D_EXT；'
        'localizedKDCertificate=FINITE_ARITHMETIC_CROSS_CHECK_ONLY；'
        'formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED；'
        'formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES；formalFigureRows=266；'
        'navierStokesSimulation=NOT_RUN；directNumericalSimulation=NOT_RUN；'
        'ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=false</p>'
        '<p>OPEN：smallerCylinderTailControl=OPEN；tailSmallnessOrAbsorption=OPEN；'
        'coupledTailReplacement=OPEN；weakStabilityAndLowerSemicontinuity=OPEN；'
        'scaleUniformQuotientCoercivity=OPEN；epsilonRegularity=OPEN；'
        'arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN</p>'
        '<p>本节只证明一个正尺度 size lemma：core--core 由 clock-matched local energy 支付，'
        '其余三块由显式 exterior velocity/gradient tails 支付。它不证明尾项小、可吸收、紧致，'
        '也不证明 epsilon regularity、奇性或任意三维全局正则性。NOT CLAY。</p></section>'
    )
    figure = (
        '<section id="figure"><div class="section-no">F / 论文图</div>'
        '<h2>四块付款、旧外部包障碍与 time-supremum tail</h2>'
        '<p><img src="/assets/r074a/fig-r074a-localized-kd-payments.svg" '
        'alt="R0.74A localized mixed heat covariance payments and exact obstruction ledgers"></p>'
        '<p><a href="/assets/r074a/fig-r074a-localized-kd-payments.pdf">下载矢量 PDF</a> · '
        '<a href="/assets/r074a/fig-r074a-localized-kd-payments.png">下载 600 dpi PNG</a> · '
        '<a href="/assets/r074a/fig-r074a-localized-kd-payments.svg">打开 SVG</a></p>'
        '<p>图中 266 行只复算已证明公式与两个函数级 obstruction ledger；不是 DNS、NSE trajectory、'
        '奇性候选或有限采样证明。NOT CLAY。</p></section>'
    )
    reproduce = (
        '<section id="reproduce"><div class="section-no">R / 复现材料</div><h2>冻结证明、审计与证书</h2>'
        '<p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074a_localized_kd_size_lemma.md">英文规范源文</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074a_localized_kd_size_lemma_zh.md">中文完整译文</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074a_independent_audit.md">独立审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074a_primary_literature_audit.md">一手文献审计</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074a_localized_kd_certificate_report.md">有限算术证书报告</a> · '
        '<a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074a_localized_kd_certificate.json">机器可读证书</a></p>'
        '<p><a href="/notes/r0-74a.pdf">同步研究笔记 PDF</a> · '
        '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a> · '
        '<a href="/recap-r0-61-r0-73x.pdf">PDF</a></p></section>'
    )
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="1.67">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title><meta name="description" content="{SUBTITLE}"><link rel="canonical" href="https://kasifa.github.io/notes/r0-74a.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v=1.67"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{--paper:#f3ecd8;--ink:#26231d;--rule:#8b2f2b;--muted:#625d52}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.75 Georgia,"Noto Serif SC",serif}}.top{{border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}main{{width:min(920px,90vw);margin:auto}}.hero{{padding:56px 0 28px;border-bottom:1px solid var(--ink)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,300px);gap:2rem}}h1{{font-size:clamp(2rem,6vw,4rem);line-height:1.05}}h2{{margin-top:3rem;color:var(--rule)}}.stamp,.section-no{{font:700 12px/1.5 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}}article{{padding:20px 0 80px}}p,.callout{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:#fff8e8;padding:14px;border-left:4px solid var(--rule)}}a{{color:#702824}}img{{max-width:100%;height:auto}}.callout{{padding:1rem 1.25rem;background:#fff8e8;border:1px solid #c8bfa8}}@media(max-width:720px){{html,body{{max-width:100%;overflow-x:hidden}}body{{font-size:15px}}main,article,section{{min-width:0}}.hero-inner{{grid-template-columns:1fr}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{.top{{display:none}}body{{background:white;font-size:10.5pt}}main{{width:auto}}.hero{{padding-top:0}}a{{color:inherit;text-decoration:none}}section{{break-inside:auto}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74A · NOT CLAY</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74A · EXACT ANALYTIC SIZE LEMMA / FINITE CERTIFICATE</div><h1>{TITLE}</h1><p>{SUBTITLE}</p><p>四块正 majorization 给出 \\(\\theta^{{1/4}}\\) 或 \\(\\theta\\) 付款；旧的 R0.73X exterior package 单独不够，新 velocity endpoint tail 与复用的 gradient tail 只保证有限，不保证小或可吸收。</p></div><div class="stamp"><strong>状态 · R0.74A 完成</strong><p>版本 R0.74A · 2026-09-01</p><p>size lemma：PROVED</p><p>arithmetic certificate：FINITE</p><p>tail absorption / epsilon regularity：OPEN</p><p>LOCAL DIRECT / NO DGX</p><p>NOT CLAY</p></div></div></header>
<article>{section_html}{figure}{boundary}{reproduce}</article>
</main></body></html>'''


def copy_figures() -> None:
    archive = ROOT / "figures/r074a/fig-r074a-localized-kd-payments"
    public_archive = ROOT / "public/figures/r074a/fig-r074a-localized-kd-payments"
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
            "schema": "r074a-package-record-v1",
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
            "path": f"public/assets/r074a/fig-r074a-localized-kd-payments.{extension}",
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
        })
    compatibility_manifest = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r074a-localized-kd-payments-publication-compat-v1",
        "figureId": "fig-r074a-localized-kd-payments",
        "release": "R0.74A",
        "status": "formal",
        "publicationStatus": "published",
        "analyticalQuestion": "How can the positive mixed heat covariance be localized into a clock-matched core payment and explicit Gaussian exterior tails?",
        "supportedClaim": "A positive four-block majorization yields the stated local size bound. The old R0.73X exterior package alone is insufficient; finite rows only cross-check analytic formulas.",
        "createdAt": "2026-09-01T09:08:08Z",
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
            "formalCommand": "python plot.py --render; python validate.py --verify-only --confirm-visual-qa",
            "wallTimeSeconds": 2.0,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
        },
        "compute": {
            "host": "local workstation (hostname intentionally omitted)",
            "operatingSystem": "macOS arm64",
            "cpu": "arm64 / local CPU",
            "memoryGiB": 36.0,
            "processes": 1,
            "threadsPerProcess": 1,
            "dgxUsed": False,
        },
        "environment": {
            "python": "3.12",
            "packagesLock": "requirements.txt",
            "packages": {"numpy": "2.3.5", "pillow": "12.3.0", "reportlab": "4.4.9", "pypdf": "6.10.0"},
        },
        "data": data,
        "sourceData": [{
            "location": "repository source commit",
            "fileName": "research/r074a_localized_kd_size_lemma.md",
            "bytes": REPORT.stat().st_size,
            "sha256": sha256(REPORT),
            "extractionCommand": "git show 391debac9d48158ab4b0f90edf873150849e6e57:research/r074a_localized_kd_size_lemma.md",
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
            "archiveDirectory": "public/figures/r074a/fig-r074a-localized-kd-payments",
            "researchArchiveDirectory": "research/figures/r074a/fig-r074a-localized-kd-payments",
            "directory": "public/assets/r074a",
            "fileStem": "fig-r074a-localized-kd-payments",
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
    assets = ROOT / "public/assets/r074a"
    assets.mkdir(parents=True, exist_ok=True)
    for extension in ("pdf", "png", "svg"):
        shutil.copy2(FIGURE_SOURCE / f"figure.{extension}", assets / f"fig-r074a-localized-kd-payments.{extension}")


def update_home(value: str) -> str:
    value = replace_once(value, 'data-site-version="1.66"', 'data-site-version="1.67"', "home version attribute")
    value = replace_once(value, '/i18n-en.js?v=1.66', '/i18n-en.js?v=1.67', "home i18n cache")
    value = replace_once(value, '<strong>v1.66</strong>网页版本', '<strong>v1.67</strong>网页版本', "home version badge")
    value = replace_once(value, "综述 v1.66 · 2026-09-01", "综述 v1.67 · 2026-09-01", "home footer version")
    value = replace_once(value, '<strong>202</strong>公开研究笔记', '<strong>203</strong>公开研究笔记', "home note count")
    value = replace_once(
        value,
        "R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 202 篇公开研究笔记",
        "R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 203 篇公开研究笔记",
        "home recap card public-note count",
    )
    value = replace_once(value, '<strong>R0.73Z</strong>最新研究节点', '<strong>R0.74A</strong>最新研究节点', "home latest node")
    old_focus = re.search(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', value, re.S)
    if old_focus is None:
        raise RuntimeError("home current-focus row missing")
    focus = '<div class="summary-item"><strong>我目前关注</strong><span>R0.74A 已把 K_D 的正尺度局部 upper bound 拆成 core--core 与三个 exterior blocks：前者由 clock-matched local energy 支付，后者由一个新 velocity endpoint tail 和 R0.73X gradient tail 支付。下一步只检查这些尾项能否小、可吸收或弱稳定；quotient coercivity、epsilon regularity、任意三维全局正则性和 Clay 仍为 OPEN。</span></div>'
    value = value[:old_focus.start()] + focus + value[old_focus.end():]
    spotlight = re.search(r'<section class="route-overview latest-release-spotlight".*?</section>', value, re.S)
    if spotlight is None:
        raise RuntimeError("latest-release spotlight missing")
    new_spotlight = '<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74A · 2026-09-01</p><h2 class="route-map-title" id="latest-release-title">R0.74A｜混合 heat covariance 的局部 size lemma</h2><p class="route-map-intro">四块 positive majorization 将 core--core 交给 clock-matched local energy，其余三块交给显式 Gaussian velocity/gradient tails。旧 R0.73X exterior package 单独不够；新尾目前只证明有限，不证明小、吸收或紧致。NOT CLAY。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74a.pdf">阅读最新 R0.74A 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">203 篇研究笔记总索引</a><a href="#r074a">查看首页完整 R0.74A 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74A · 105 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>81 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74A</span></div></div></section>'
    value = value[:spotlight.start()] + new_spotlight + value[spotlight.end():]
    for old, new, label in [
        ("Research topology · R0.1–R0.73Z", "Research topology · R0.1–R0.74A", "route topology"),
        ('href="#r073z">跳到首页 R0.73Z 卡片', 'href="#r074a">跳到首页 R0.74A 卡片', "route jump"),
        ("R0.70A–R0.73Z：104 节已公开，80 节完整封存", "R0.70A–R0.74A：105 节已公开，81 节完整封存", "route counts"),
        ("R0.72R–R0.73Z：", "R0.72R–R0.74A：", "route tail range"),
        ('<span class="route-range">R0.69P–R0.73Z</span>', '<span class="route-range">R0.69P–R0.74A</span>', "route range"),
        ('aria-label="R0.69P–R0.73Z"', 'aria-label="R0.69P–R0.74A"', "route aria range"),
        ("展开 112 篇公开笔记", "展开 113 篇公开笔记", "current route note count"),
        ('<a class="milestone" href="/notes/r0-73z.html">R0.73Z</a>', '<a class="milestone" href="/notes/r0-73z.html">R0.73Z</a>\n                  <a class="milestone" href="/notes/r0-74a.html">R0.74A</a>', "route note link"),
    ]:
        value = replace_once(value, old, new, label)
    value = replace_once(value, 'R0.73Z：初始端点有限性障碍、能量兼容正三次修复与 pressure-active 分离已分列', 'R0.74A：core/exterior 四块付款、显式 Gaussian tails 与 old-package obstruction 已分列', "current route title")
    summary_match = re.search(r'<p class="tree-current-summary">.*?</p>', value, re.S)
    if summary_match is None:
        raise RuntimeError("tree current summary missing")
    current_summary = '<p class="tree-current-summary">R0.74A 把 mixed heat covariance 的正尺度 upper bound 精确拆成四块：core 由 local energy 支付，exterior 由两个显式 Gaussian tails 支付。旧 exterior package 单独不足；尾项吸收与 epsilon regularity 仍开放。NOT CLAY。</p>'
    value = value[:summary_match.start()] + current_summary + value[summary_match.end():]
    value = replace_once(value, 'positive-covariance endpoint obstruction / energy-compatible repair / pressure-active separation</p>', 'positive-covariance endpoint obstruction / energy-compatible repair / pressure-active separation → localized mixed-covariance four-block size lemma / explicit Gaussian tails</p>', "current route path")
    next_node = re.search(r'<div class="tree-row">\s*<article class="tree-node next">.*?</article>\s*</div>', value, re.S)
    if next_node is None:
        raise RuntimeError("next route node missing")
    next_html = f'<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74B</span><span class="tree-state current">下一检查点</span></div><h3>R0.74B 下一接口</h3><p>{NEXT_GATE}</p></article></div>'
    value = value[:next_node.start()] + next_html + value[next_node.end():]
    card = f'''<div class="task-one" id="r074a" data-release="r074a" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.74A · 2026-09-01</p><h3>{TITLE}</h3>
            <p>四块 positive majorization 分离 core--core、core--exterior、exterior--core 与 exterior--exterior；对应付款分别带 \\(\\theta^{{1/4}}\\) 或 \\(\\theta\\)。</p>
            <p>旧 R0.73X exterior package 单独不能控制 \\(\\mathcal K_D\\)；新 velocity endpoint tail 与复用的 gradient tail 对每个声明的 energy-class field 有限，但尚未证明小、可吸收或由更小柱控制。</p>
            <p><strong>证明边界：</strong>PROVED：positiveFourBlockMajorization=PROVED_ANALYTICALLY；clockMatchedLocalEnergyTailBound=PROVED_ANALYTICALLY；pressureCutoffInterface=PROVED_BY_INHERITANCE_AND_ANALYTIC_COMBINATION；oldExteriorPackageOnlyControl=FALSE_BY_EXACT_ENERGY_CLASS_PACKETS</p>
            <p><strong>有限边界：</strong>FINITE：velocityEndpointTail=FINITE_FOR_EVERY_STATED_PERIODIC_ENERGY_CLASS_FIELD；gradientTail=FINITE_AND_IDENTICAL_TO_R073X_D_EXT；localizedKDCertificate=FINITE_ARITHMETIC_CROSS_CHECK_ONLY；formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES；formalFigureRows=266；ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=false</p>
            <p><strong>开放边界：</strong>OPEN：smallerCylinderTailControl=OPEN；tailSmallnessOrAbsorption=OPEN；coupledTailReplacement=OPEN；weakStabilityAndLowerSemicontinuity=OPEN；scaleUniformQuotientCoercivity=OPEN；epsilonRegularity=OPEN；arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN。NOT CLAY。</p>
            <p><a href="/notes/r0-74a.html"><strong>阅读 R0.74A 研究笔记 →</strong></a><br><a href="/notes/r0-74a.pdf">下载同步 PDF</a> · <a href="/assets/r074a/fig-r074a-localized-kd-payments.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a></p>
            <p><strong style="color:var(--gold)">下一发布门（R0.74B）：</strong>&nbsp;{NEXT_GATE}</p>
          </div>
          '''
    marker = '<div class="task-one" id="r073z" data-release="r073z"'
    if value.count(marker) != 1:
        raise RuntimeError("R0.73Z home card marker drift")
    value = value.replace(marker, card + marker, 1)
    return value


def update_literature(value: str) -> str:
    value = replace_once(value, 'data-site-version="1.66"', 'data-site-version="1.67"', "literature version attribute")
    value = replace_once(value, '/i18n-en.js?v=1.66', '/i18n-en.js?v=1.67', "literature i18n cache")
    value = replace_once(value, "文献综述 v1.66 · 2026-09-01", "文献综述 v1.67 · 2026-09-01", "literature footer")
    value = replace_once(value, "R0.69P–R0.73Z 只列为研究笔记", "R0.69P–R0.74A 只列为研究笔记", "literature route endpoint")
    next_route = re.search(
        r'<div class="route-step pause"><header><b>开放接口 · R0\.74A</b>.*?</div>',
        value,
        re.S,
    )
    if next_route is None:
        raise RuntimeError("literature next-route interface missing")
    next_route_html = (
        '<div class="route-step kept"><header><b>R0.74A</b>'
        '<strong>localized mixed-covariance four-block size lemma</strong></header>'
        f'<p><strong>{TITLE}</strong></p>'
        '<p>R0.70A–R0.74A：105 节已公开，81 节完整封存。</p>'
        '<p>core/exterior 四块付款、显式 Gaussian velocity/gradient tails 与旧 exterior package 障碍已分别记录。 '
        '<a href="/notes/r0-74a.html">研究笔记</a> '
        '<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> '
        '<a href="#r074a-boundary">文献边界</a></p></div>'
        '<div class="route-step pause"><header><b>开放接口 · R0.74B</b>'
        '<strong>tail absorption, weak stability, and blow-up-sequence compatibility</strong></header>'
        f'<p>{NEXT_GATE}</p></div>'
    )
    value = value[:next_route.start()] + next_route_html + value[next_route.end():]
    insert_marker = '          <ol class="criteria">'
    block = '<h3 id="r074a-boundary">R0.74A：mixed heat covariance 的 core/exterior 四块 size lemma</h3><p>positive majorization 把 core--core、core--exterior、exterior--core 与 exterior--exterior 分开；clock-matched local energy 支付第一块，一个新 velocity endpoint tail 与 R0.73X gradient tail 支付其余三块。两个 exact energy-class packet 说明旧 exterior package 单独不够。<a href="/notes/r0-74a.html">阅读 R0.74A 研究笔记</a>。</p><div class="boundary"><strong>R0.74A 的主张边界</strong><p>PROVED：positiveFourBlockMajorization=PROVED_ANALYTICALLY；clockMatchedLocalEnergyTailBound=PROVED_ANALYTICALLY；pressureCutoffInterface=PROVED_BY_INHERITANCE_AND_ANALYTIC_COMBINATION；oldExteriorPackageOnlyControl=FALSE_BY_EXACT_ENERGY_CLASS_PACKETS；navierStokesScaling=PROVED_ANALYTICALLY</p><p>FINITE：velocityEndpointTail=FINITE_FOR_EVERY_STATED_PERIODIC_ENERGY_CLASS_FIELD；gradientTail=FINITE_AND_IDENTICAL_TO_R073X_D_EXT；localizedKDCertificate=FINITE_ARITHMETIC_CROSS_CHECK_ONLY；formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES；formalFigureRows=266；ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX；dgxUsed=false</p><p>OPEN：smallerCylinderTailControl=OPEN；tailSmallnessOrAbsorption=OPEN；coupledTailReplacement=OPEN；weakStabilityAndLowerSemicontinuity=OPEN；scaleUniformQuotientCoercivity=OPEN；epsilonRegularity=OPEN；arbitraryThreeDimensionalGlobalRegularity=OPEN；clayConclusion=OPEN。NOT CLAY。</p></div>\n'
    value = replace_once(value, insert_marker, block + insert_marker, "literature R0.74A boundary")
    return value


def update_metadata() -> None:
    site = json.loads(SITE_VERSION.read_text(encoding="utf-8"))
    site.update({
        "version": "1.67", "latestRelease": "R0.74A", "publicHtmlNoteCount": 203,
        "postR060PublishedNodeCount": 143, "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X", "publicPdfNoteCount": 160,
        "publishedDate": "2026-09-01",
    })
    write_json(SITE_VERSION, site)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": "r074a", "siteVersion": "1.67", "publicHtmlNoteCount": 203,
        "postR060PublishedNodeCount": 143, "postR060RecapNodeCount": 140,
        "nextRelease": "r074b", "postR070APublishedReleaseCount": 105,
        "postR070AFormalSealedReleaseCount": 81, "publicPdfNoteCount": 160,
        "latestReleaseGate": "tests/r074a-localized-kd-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r074a-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r074a-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r074a-pdfs.mjs",
        "latestRecapRelease": "r073x",
    })
    write_json(MANIFEST, manifest)
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r074a" not in inventory[key]:
            inventory[key].append("r074a")
    inventory.update({
        "latestPublishedRelease": "r074a", "publishedReleaseCount": 105,
        "formalSealedReleaseCount": 81, "legacyFormalFigureBacklogCount": 24,
    })
    write_json(INVENTORY, inventory)
    # Bind the inventory digest only after the inventory update.
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest["formalArchiveInventory"]["sha256"] = sha256(INVENTORY)
    write_json(MANIFEST, manifest)
    write_text(ROOT / "VERSION", "1.67\n")


def write_dictionary() -> None:
    write_text(DICTIONARY, f'''# R0.74A bilingual release dictionary

**Route:** LOCAL DIRECT / NO DGX  
**DGX used:** false

| Public Chinese | Reviewed English |
|---|---|
| {TITLE} | R0.74A \\| A localized size lemma for the mixed heat covariance |
| {SUBTITLE} | The core is paid by local energy and the exterior by two explicit Gaussian quadratic tails |
| 中文正文 01--06 节已完整同步 | Sections 01--06 of the Chinese canonical report are fully synchronized |
| 冻结定义与时间钟说明 | Frozen definitions and the clock qualification |
| 提升环带与两个二次外部输入 | Lifted annuli and the two quadratic exterior inputs |
| 正的核心/外部上界分解 | Positive core/exterior majorization |
| 局部 size 定理 | The localized size theorem |
| 为什么旧 exterior functional 不足 | Why the older exterior functional is insufficient |
| 已证明条目与剩余门槛 | Proven rows and remaining gates |
| 四块 positive majorization | Positive four-block majorization |
| clock-matched local energy | Clock-matched local energy |
| velocity endpoint tail | Velocity endpoint tail |
| 旧 exterior package 单独不够 | The old exterior package is insufficient on its own |
| 尾项小性或吸收 | Tail smallness or absorption |
| 证明、有限证书、开放问题与 Clay 边界分开 | Proofs, finite certificates, open problems, and the Clay boundary are kept separate |
| 本节只证明一个正尺度 size lemma。 | This section proves only a positive-scale size lemma. |
| NOT CLAY。 | NOT CLAY. |

The reviewed Chinese source is `research/r074a_localized_kd_size_lemma_zh.md`;
the frozen English source is `research/r074a_localized_kd_size_lemma.md`.
All 52 display equations and tags are preserved. Mathematical tokens, theorem
quantifiers, certificate payloads, source-data rows, and formal-figure science
remain unchanged.
''')


def build() -> None:
    assert_recap()
    if SITE_VERSION.is_file():
        current_site = json.loads(SITE_VERSION.read_text(encoding="utf-8"))
        if current_site.get("version") == "1.67" and current_site.get("latestRelease") == "R0.74A":
            report = REPORT_ZH.read_text(encoding="utf-8")
            write_text(NOTE, note_html(report))
            copy_figures()
            write_dictionary()
            check()
            return
    report = REPORT_ZH.read_text(encoding="utf-8")
    handoff = json.loads(HANDOFF.read_text(encoding="utf-8"))
    if handoff["releaseId"] != "r074a" or handoff["translationRoute"] != "LOCAL_DIRECT_NO_DGX":
        raise RuntimeError("R0.74A handoff drift")
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
        "version": "1.67", "latestRelease": "R0.74A", "publicHtmlNoteCount": 203,
        "postR060PublishedNodeCount": 143, "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X", "publicPdfNoteCount": 160,
    }
    site = json.loads(SITE_VERSION.read_text(encoding="utf-8"))
    for key, expected in expected_site.items():
        if site.get(key) != expected:
            raise RuntimeError(f"site-version {key} drift")
    note = NOTE.read_text(encoding="utf-8")
    for token in ("PROVED", "FINITE", "OPEN", "NOT CLAY", "LOCAL DIRECT / NO DGX"):
        if token not in note:
            raise RuntimeError(f"public note missing boundary token {token}")
    for token in (
        "冻结定义与时间钟说明", "局部 size 定理", "已证明条目与剩余门槛",
        "01 / 规范报告", "R / 复现材料",
    ):
        if token not in note:
            raise RuntimeError(f"public note missing complete Chinese report token {token}")
    for token in (
        "<h2>Frozen definitions and the clock qualification</h2>",
        "<h2>The localized size theorem</h2>",
        "<h2>Proven rows and remaining gates</h2>",
    ):
        if token in note:
            raise RuntimeError(f"public Chinese note retains English canonical section: {token}")
    if 'inlineMath:[["\\\\(","\\\\)"]]' not in note or 'displayMath:[["\\\\[","\\\\]"]]' not in note:
        raise RuntimeError("public note MathJax delimiters are not JavaScript-safe")
    if (ROOT / "public/recap-r0-61-r0-74a.html").exists() or (ROOT / "public/recap-r0-61-r0-74a.pdf").exists():
        raise RuntimeError("non-milestone R0.74A recap must not exist")
    for extension in ("pdf", "png", "svg"):
        target = ROOT / f"public/assets/r074a/fig-r074a-localized-kd-payments.{extension}"
        if target.read_bytes() != (FIGURE_SOURCE / f"figure.{extension}").read_bytes():
            raise RuntimeError(f"published figure {extension} differs from frozen source")
    public_archive = ROOT / "public/figures/r074a/fig-r074a-localized-kd-payments"
    for source in FIGURE_SOURCE.iterdir():
        if source.is_file() and (public_archive / source.name).read_bytes() != source.read_bytes():
            raise RuntimeError(f"public evidence mirror differs from frozen source: {source.name}")
    if "r074a" not in json.loads(INVENTORY.read_text(encoding="utf-8"))["formalSealedReleases"]:
        raise RuntimeError("formal archive inventory omits r074a")
    if "R0.74B" not in HOME.read_text(encoding="utf-8"):
        raise RuntimeError("home route does not advance to R0.74B")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only:
        check()
    else:
        build()
        check()
    print(json.dumps({"release": "R0.74A", "checked": True, "recapGenerated": False, "translationPath": "LOCAL_DIRECT_NO_DGX", "dgxUsed": False}))


if __name__ == "__main__":
    main()
