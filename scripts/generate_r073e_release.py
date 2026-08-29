#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate and validate the transactional R0.73E GitHub Pages release."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from generate_r072o_release import assert_clean, digest, once, required, section
from generate_r072p_release import assert_mathjax_clean
from r073e_release_content import (
    CERTIFICATE_RELATIVE,
    CLOSED,
    EXPERIMENT_RELATIVE,
    FIGURE_ID,
    FIGURE_RELATIVE,
    HOME_E_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    R073D_RELEASE_BASELINE,
)

ROOT = Path(os.environ.get(
    "R073E_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"
CERTIFIED_REPORT_COMMIT = "803279d72c24a54db27c40dcdad97593636788fc"
FIGURE_DIRECTORY_COMMIT = "f55e54e97db96fb0e050e840d5f2db50d9bbc292"
FIGURE_CERTIFICATE_COMMIT = "1c80e0bd666db16a116920ddb194b26bbec29f9a"

CLOSED_KEYS = (
    "fixedPositiveHalfPlaneNoPollution",
    "allModesRightOfBProjectionNormPersistence",
    "topInviscidClusterExists",
    "topViscousClusterPersistence",
    "topReducedHalfPlaneResolventUniform",
    "frozenTopClusterRelativeDichotomy",
    "fixedFrozenGeneratorVolterraTransfer",
    "logFastTimeTransfer",
    "superPolynomialCompleteRowNoGo",
)
OPEN_KEYS = (
    "certifiedSigmaStarIsRightmost",
    "selectedSigmaStarComplementDichotomy",
    "uniformHalfPlaneBoundAtBEqualsZero",
    "globalRightHalfPlaneNoPollution",
    "absoluteUniformComplementDecay",
    "explicitHalfPlaneGap",
    "explicitViscosityThreshold",
    "quantitativeEigenvalueRate",
    "movingProfileUniformContour",
    "graphDomainKatoTransport",
    "movingProfileEvolutionDichotomy",
    "inviscidRootUnique",
    "inviscidEigenvalueSimple",
    "completeOSSquireA2DirectSum",
    "fixedWindowExponentialLowerLaw",
    "nonlinearNavierStokes",
    "Clay",
)


def verify_complete_flat_ledger(
    directory: Path, label: str, *, require_directory_complete: bool = True
) -> None:
    rows = (directory / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    names: list[str] = []
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if match is None:
            raise RuntimeError(label + ": malformed SHA256SUMS row")
        name = match.group(2)
        if name in names:
            raise RuntimeError(label + ": duplicate SHA256SUMS entry " + name)
        path = directory / name
        if not path.is_file() or digest(path) != match.group(1):
            raise RuntimeError(label + ": hash mismatch " + name)
        names.append(name)
    actual = sorted(
        path.name for path in directory.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    if require_directory_complete and sorted(names) != actual:
        raise RuntimeError(label + ": SHA256SUMS inventory is incomplete")


def verify_manifest_hashes(path: Path, label: str) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    checked = 0
    for group in (
        "sources", "inputs", "outputs",
        "sourceBindings", "outputBindings", "packageBindings",
    ):
        for row in payload.get(group, []):
            if not isinstance(row, dict):
                continue
            relative = row.get("path")
            expected = row.get("sha256")
            if not relative or not re.fullmatch(r"[0-9a-f]{64}", str(expected)):
                raise RuntimeError(f"{label}: malformed {group} hash row")
            candidate = ROOT / relative
            if not candidate.is_file():
                candidate = path.parent / relative
            if not candidate.is_file() or digest(candidate) != expected:
                raise RuntimeError(f"{label}: stale source hash {relative}")
            checked += 1
    if checked == 0:
        raise RuntimeError(label + ": no source hashes were checked")
    return payload


def verify_root_relative_ledger(directory: Path, label: str) -> None:
    rows = (directory / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    declared: list[str] = []
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\\\r\n]+)", row)
        if match is None:
            raise RuntimeError(label + ": malformed SHA256SUMS row")
        relative = match.group(2)
        if not relative.startswith(directory.relative_to(ROOT).as_posix() + "/"):
            raise RuntimeError(label + ": path escaped package " + relative)
        candidate = ROOT / relative
        if not candidate.is_file() or digest(candidate) != match.group(1):
            raise RuntimeError(label + ": hash mismatch " + relative)
        declared.append(candidate.name)
    actual = sorted(path.name for path in directory.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if sorted(declared) != actual:
        raise RuntimeError(label + ": SHA256SUMS inventory is incomplete")


def replace_all(html: str, old: str, new: str, label: str) -> str:
    if old not in html:
        raise RuntimeError(label + ": source not found")
    return html.replace(old, new)


def preflight_release_state() -> None:
    release = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    for key, value in R073D_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.73D: {key}")
    if release.get("nextReleaseSourceStage") is not None:
        raise RuntimeError("R0.73D baseline has an unexpected source-stage payload")
    site = json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8"))
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.44",
        "latestRelease": "R0.73D",
        "publicHtmlNoteCount": 180,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("public site-version is not exactly at R0.73D")
    if (ROOT / "VERSION").read_text(encoding="utf-8") != "1.44\n":
        raise RuntimeError("root VERSION is not R0.73D v1.44")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 180:
        raise RuntimeError("R0.73D preflight expected 180 public HTML notes")
    for relative in (
        "notes/r0-73e.html", "notes/r0-73e.pdf",
        "recap-r0-61-r0-73e.html", "recap-r0-61-r0-73e.pdf",
    ):
        if (PUBLIC / relative).exists():
            raise RuntimeError("R0.73D preflight found premature output: " + relative)
    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.44"', "<strong>180</strong>公开研究笔记",
        "<strong>R0.73D</strong>最新研究节点", 'aria-label="R0.69P–R0.73D"',
    ):
        if token not in home:
            raise RuntimeError("R0.73D home baseline missing token: " + token)
    if 'data-release="r073e"' in home:
        raise RuntimeError("R0.73D home already contains an R0.73E card")
    recap = (PUBLIC / "recap-r0-61-r0-73d.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 120 or len(set(links)) != 120:
        raise RuntimeError("R0.73D recap must contain 120 unique nodes")
    inventory = json.loads((ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8"))
    if (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    ) != ("r073d", 82, 58, 24):
        raise RuntimeError("formal archive inventory is not at R0.73D")


def validate_inputs() -> None:
    required_inputs = (
        "research/r073e_report-source.md",
        "research/r073e_problem_freeze.md",
        "research/r073e_literature_audit.md",
        "research/r073e_gap_matrix.md",
        "research/r073e_halfplane_transfer_proof.md",
        "research/r073e_independent_analytic_audit.md",
        f"{CERTIFICATE_RELATIVE}/certificate.json",
        f"{CERTIFICATE_RELATIVE}/independent_recompute.json",
        f"{CERTIFICATE_RELATIVE}/validation.json",
        f"{CERTIFICATE_RELATIVE}/manifest.json",
        f"{CERTIFICATE_RELATIVE}/validate_certificate.py",
        f"{EXPERIMENT_RELATIVE}/complement_diagnostic.json",
        f"{EXPERIMENT_RELATIVE}/independent_validation.json",
        f"{EXPERIMENT_RELATIVE}/progress.ndjson",
        f"{FIGURE_RELATIVE}/manifest.json",
        f"{FIGURE_RELATIVE}/contract.json",
        f"{FIGURE_RELATIVE}/validation.json",
        f"{FIGURE_RELATIVE}/caption.md",
        f"{FIGURE_RELATIVE}/validate.py",
        "public/notes/r0-73d.html",
        "public/recap-r0-61-r0-73d.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing R0.73E release input: " + relative)

    report = (ROOT / "research/r073e_report-source.md").read_text(encoding="utf-8")
    audit = (ROOT / "research/r073e_independent_analytic_audit.md").read_text(encoding="utf-8")
    freeze = (ROOT / "research/r073e_problem_freeze.md").read_text(encoding="utf-8")
    for key in CLOSED_KEYS:
        for value, label in ((report, "report"), (audit, "audit"), (freeze, "freeze")):
            if key + "=CLOSED" not in value:
                raise RuntimeError(f"R0.73E {label} lost CLOSED token: {key}")
    for key in OPEN_KEYS:
        for value, label in ((report, "report"), (freeze, "freeze")):
            if key + "=OPEN" not in value:
                raise RuntimeError(f"R0.73E {label} lost OPEN token: {key}")
    for token in ("PASS", "Bromwich", "Volterra", "complete-row"):
        if token not in audit:
            raise RuntimeError("R0.73E independent audit missing token: " + token)

    certificate = ROOT / CERTIFICATE_RELATIVE
    verify_complete_flat_ledger(certificate, "R0.73E certificate", require_directory_complete=False)
    subprocess.run([sys.executable, str(certificate / "validate_certificate.py")], cwd=ROOT, check=True)
    verify_complete_flat_ledger(certificate, "R0.73E certificate after validation", require_directory_complete=False)
    cert = json.loads((certificate / "certificate.json").read_text(encoding="utf-8"))
    validation = json.loads((certificate / "validation.json").read_text(encoding="utf-8"))
    if validation.get("allChecksPass") is not True:
        raise RuntimeError("R0.73E certificate validation is not passed")
    theorem = cert.get("theorem", cert.get("claimLedger", cert.get("closedClaims", {})))
    for key in CLOSED_KEYS:
        if theorem.get(key) not in ("CLOSED", True):
            raise RuntimeError("R0.73E certificate theorem is not CLOSED: " + key)
    boundary = cert.get("claimBoundary", {})
    for key in OPEN_KEYS:
        if boundary.get(key) not in (False, "OPEN"):
            raise RuntimeError("R0.73E certificate escaped OPEN boundary: " + key)
    cert_manifest = verify_manifest_hashes(certificate / "manifest.json", "R0.73E certificate manifest")
    source_commit = str(cert.get("sourceCommit", cert_manifest.get("sourceCommit", "")))
    if source_commit != CERTIFIED_REPORT_COMMIT:
        raise RuntimeError("R0.73E certificate is not bound to the audited report commit")
    subprocess.run(["git", "cat-file", "-e", source_commit + "^{commit}"], cwd=ROOT, check=True)
    committed_report = subprocess.run(
        ["git", "show", source_commit + ":research/r073e_report-source.md"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout
    if digest(ROOT / "research/r073e_report-source.md") != hashlib.sha256(committed_report).hexdigest():
        raise RuntimeError("R0.73E report differs from the certificate-bound commit")

    experiment = json.loads((ROOT / EXPERIMENT_RELATIVE / "complement_diagnostic.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / EXPERIMENT_RELATIVE / "independent_validation.json").read_text(encoding="utf-8"))
    if experiment.get("allChecksPass") is not True or independent.get("allChecksPass") is not True:
        raise RuntimeError("R0.73E finite diagnostic validation is not passed")
    if experiment.get("claimBoundary", {}).get("ordinaryCutoffAgreementIsContinuumProof") is not False:
        raise RuntimeError("R0.73E finite diagnostic escaped continuum boundary")
    verify_root_relative_ledger(ROOT / EXPERIMENT_RELATIVE, "R0.73E experiment")

    figure = ROOT / FIGURE_RELATIVE
    figure_manifest = verify_manifest_hashes(figure / "manifest.json", "R0.73E figure manifest")
    contract = json.loads((figure / "contract.json").read_text(encoding="utf-8"))
    figure_validation = json.loads((figure / "validation.json").read_text(encoding="utf-8"))
    if (
        figure_manifest.get("release") != "R0.73E"
        or figure_manifest.get("figureId") != FIGURE_ID
        or figure_manifest.get("status") != "formal"
    ):
        raise RuntimeError("R0.73E figure identity or formal status mismatch")
    subprocess.run(["git", "cat-file", "-e", FIGURE_DIRECTORY_COMMIT + "^{commit}"], cwd=ROOT, check=True)
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", FIGURE_DIRECTORY_COMMIT, "HEAD"], cwd=ROOT
    ).returncode != 0:
        raise RuntimeError("R0.73E formal figure commit is not an ancestor of HEAD")
    if (
        figure_validation.get("status") != "passed"
        or not figure_validation.get("checks")
        or not all(figure_validation["checks"].values())
    ):
        raise RuntimeError("R0.73E figure validation is not passed")
    claims = contract.get("claimBoundary", {})
    if claims.get("formalFiniteDiagnosticFigure") is not True:
        raise RuntimeError("R0.73E figure lost formal diagnostic status")
    for key in (
        "finiteSpectrumIsContinuumSpectrum", "finiteResolventPeaksAreUniformHalfPlaneBound",
        "sampledSemigroupIsContinuousTimeBound", "nonautonomousTransferProvedHere",
        "nonlinearNavierStokesProvedHere", "clayProblemSolved",
    ):
        if claims.get(key) is not False:
            raise RuntimeError("R0.73E figure escaped boundary: " + key)
    subprocess.run(
        [
            sys.executable, str(figure / "validate.py"),
            "--source-commit", figure_manifest["git"]["sourceCommit"],
            "--certificate-commit", FIGURE_CERTIFICATE_COMMIT,
        ],
        cwd=ROOT, check=True,
    )
    verify_complete_flat_ledger(figure, "R0.73E figure")


def publish_figure_assets() -> None:
    figure = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073e"
    target.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        source = figure / f"figure.{suffix}"
        destination = target / f"{FIGURE_ID}.{suffix}"
        shutil.copyfile(source, destination)
        if digest(destination) != digest(source):
            raise RuntimeError("R0.73E public figure copy is not byte-identical: " + suffix)
    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    subprocess.run(
        [
            sys.executable, str(figure / "validate.py"),
            "--source-commit", manifest["git"]["sourceCommit"],
            "--certificate-commit", FIGURE_CERTIFICATE_COMMIT,
        ],
        cwd=ROOT, check=True,
    )
    verify_complete_flat_ledger(figure, "R0.73E published figure")
    expected_public = [f"{FIGURE_ID}.{suffix}" for suffix in ("pdf", "png", "svg")]
    actual_public = sorted(path.name for path in target.iterdir() if path.is_file())
    if actual_public != sorted(expected_public):
        raise RuntimeError("R0.73E public figure copy ledger is incomplete")
    source_outputs = {row["path"]: row["sha256"] for row in manifest["outputs"]}
    for suffix in ("pdf", "png", "svg"):
        if digest(target / f"{FIGURE_ID}.{suffix}") != source_outputs[f"figure.{suffix}"]:
            raise RuntimeError("R0.73E public figure copy ledger is incomplete: " + suffix)


def build_note() -> None:
    html = (PUBLIC / "notes/r0-73d.html").read_text(encoding="utf-8")
    replacements = (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.73E：固定正半平面谱完备性、完整 top cluster 相对二分与对数快时间传递；移动谱束、非线性与 Clay 仍开放。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.73E｜Fixed-half-plane splitting and logarithmic transfer">'),
        ("og description", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="Nine one-row linear statements are CLOSED; moving-profile fixed-window growth, nonlinear dynamics, and Clay remain OPEN.">'),
        ("og image", r'<meta property="og:image" content=".*?">', f'<meta property="og:image" content="https://kasifa.github.io/assets/r073e/{FIGURE_ID}.png">'),
        ("title", r'<title>.*?</title>', '<title>R0.73E｜Fixed-half-plane splitting and logarithmic transfer</title>'),
    )
    for label, pattern, value in replacements:
        html = section(html, pattern, value, "E note " + label)
    html = required(html, "/i18n-en.js?v=1.44", "/i18n-en.js?v=1.45", "E note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#row">精确行</a><a href="#halfplane">半平面</a><a href="#projection">总投影</a><a href="#top">top cluster</a><a href="#dichotomy">相对二分</a><a href="#drift">漂移</a><a href="#transfer">传递</a><a href="#consequence">推论</a><a href="#finite">有限诊断</a><a href="#literature">文献</a><a href="#figure">附图</a><a href="#boundary">边界</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "E note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "E note hero")
    toc_items = (("result", "00 · direct decision"), ("row", "01 · exact row"), ("halfplane", "02 · fixed half-plane"), ("projection", "03 · total projection"), ("top", "04 · complete top cluster"), ("dichotomy", "05 · relative dichotomy"), ("drift", "06 · exact drift"), ("transfer", "07 · logarithmic transfer"), ("consequence", "08 · complete-row consequence"), ("finite", "09 · finite diagnostic"), ("literature", "10 · literature boundary"), ("figure", "11 · journal figure"), ("boundary", "12 · exact boundary"), ("value", "13 · value"), ("next", "14 · R0.73F"), ("reproduce", "15 · reproduction"))
    toc = '      <aside class="toc"><strong>CONTENTS</strong><ol>\n' + "".join(f'        <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_items) + '\n      </ol></aside>'
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "E note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "E note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.73E · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>', "E note footer")
    assert_clean(html, "R0.73E note")
    assert_mathjax_clean(html, "R0.73E note")
    (PUBLIC / "notes/r0-73e.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-73d.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73E 共 121 个节点；最新一节闭合固定正半平面分裂与对数快时间传递。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.73E｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="四十个阶段、121 个节点：从约化递推和环带排除到一条精确线性行的对数快时间传递。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.73E｜R0.60 之后的研究回顾</title>'),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "E recap " + label)
    html = required(html, "/i18n-en.js?v=1.44", "/i18n-en.js?v=1.45", "E recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73E · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页保留 R0.61 到 R0.73E 的全部 121 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C 认证冻结 Rayleigh 不稳定，R0.73D 闭合静态黏性谱簇持续，R0.73E 再闭合固定正半平面与对数快时间传递。一般三维 nonlinear 与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73E</strong><p>收录节点：121</p><p>回顾截止时公开笔记：181</p><p>回顾截止节点：R0.73E</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "E recap hero")
    for old, new in (("02 · 120 节完整索引", "02 · 121 节完整索引"), ("01 · 三十九个研究阶段", "01 · 四十个研究阶段"), ("R0.60 之后的路线分成三十九个阶段", "R0.60 之后的路线分成四十个阶段"), ('data-current-route="R0.69P–R0.73D"', 'data-current-route="R0.69P–R0.73E"')):
        html = required(html, old, new, "E recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>121</strong><span>R0.61–R0.73E 研究节点</span></div><div class="metric"><strong>83</strong><span>R0.70A–R0.73E 已公开版本</span></div><div class="metric"><strong>59</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73E 的 83 个版本已经公开，其中 59 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "E recap result")
    phase = rf'''            <article class="phase"><h3>R0.73E · Fixed-half-plane splitting and logarithmic transfer</h3><p>compact--Fredholm 核心、高虚部 resolvent 尾部与高实部耗散估计拼接后，每个固定正半平面的谱完备性、总 Riesz 投影和 reduced resolvent 统一界闭合。</p><p>选取完整 top cluster 后，Bromwich 移线给出相对 semigroup dichotomy；精确 \(O(\varepsilon\theta)\) profile drift 再通过固定生成元 Volterra 论证传递到任意固定 \(M\log(1/\varepsilon)\) 快时间。</p><p>{CLOSED}。{OPEN}。</p><div class="links"><a href="/notes/r0-73e.html">R0.73E</a><a href="/assets/r073e/{FIGURE_ID}.pdf">R0.73E 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073e">R0.73E 证书</a></div></article>
'''
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "E recap phase")
    html = required(html, "R0.61–R0.73D 的 120 节公开笔记", "R0.61–R0.73E 的 121 节公开笔记", "E recap node title")
    node_d = '            <span class="node-ref"><a href="/notes/r0-73d.html">R0.73D</a><span class="node-state kind-closed">闭</span></span>\n'
    node_e = '            <span class="node-ref"><a href="/notes/r0-73e.html">R0.73E</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_d, node_d + node_e, "E recap node")
    retained = '            <li>R0.73E 闭合每个固定正半平面的谱完备性、完整 top cluster 相对二分、固定生成元 Volterra 传递与任意固定次数多项式上界排除；moving-profile fixed-window、nonlinear 与 Clay 仍开放。</li>\n'
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "E recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>一条精确线性行的对数快时间增长已成为定理；固定窗口与非线性仍未闭合</h2><p>不能把 121 个节点或 83 个公开版本解释成 Clay 完成比例。R0.73E 的严格增量是 fixed-half-plane operator theorem、relative dichotomy 和 logarithmic Volterra transfer，不是有限矩阵外推。</p></section>''', "E recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73F 证明或否证固定小物理窗口上的 moving-profile top bundle</h2><p>目标是建立统一谱隙与演化二分，把 logarithmic fast-time lower bound 升级为 fixed-window \(e^{c|\Lambda|}\)。graph-domain/Kato transport 仍只是候选方法。</p></section>''', "E recap next")
    claims = f'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73E 的 83 节已公开；59 节完整封存；24 节旧档待回补。</p><p>{CLOSED}。</p><p>{OPEN}。</p></section>'''
    html = section(html, r'        <section id="claims">.*?</section>', claims, "E recap claims")
    reproduce = rf'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、审计、证书、有限诊断、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73d.html">保留 R0.73D 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73e.html">打开最新节点 R0.73E</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_halfplane_transfer_proof.md">查看 R0.73E 证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_independent_analytic_audit.md">查看独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073e">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073e">查看有限诊断与监控记录</a> · <a href="/assets/r073e/{FIGURE_ID}.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73e.pdf">下载同步 PDF</a></p><p>continuum theorem 来自解析证明与独立审计。Fourier cutoff 只做诊断和附图。</p></section>'''
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "E recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73E 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>', "E recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 121 or len(set(links)) != 121:
        raise RuntimeError("R0.73E recap expected 121 unique nodes")
    if html.count('<article class="phase">') != 40:
        raise RuntimeError("R0.73E recap expected 40 phases")
    assert_clean(html, "R0.73E recap")
    assert_mathjax_clean(html, "R0.73E recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-73e.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    html = section(html, r'    <section class="route-overview latest-release-spotlight".*?</section>', HOME_LATEST_SPOTLIGHT, "E home latest spotlight")
    for old, new in (
        ('data-site-version="1.44"', 'data-site-version="1.45"'),
        ("/i18n-en.js?v=1.44", "/i18n-en.js?v=1.45"),
        ("/site-refresh.js?v=1.44", "/site-refresh.js?v=1.45"),
        ("<strong>v1.44</strong>网页版本", "<strong>v1.45</strong>网页版本"),
        ("<strong>180</strong>公开研究笔记", "<strong>181</strong>公开研究笔记"),
        ("<strong>R0.73D</strong>最新研究节点", "<strong>R0.73E</strong>最新研究节点"),
        ('<a class="route-map-latest" href="#r073d">跳到首页 R0.73D 卡片 →</a>', '<a class="route-map-latest" href="#r073e">跳到首页 R0.73E 卡片 →</a>'),
        ("complement resolvent / semigroup dichotomy / fixed-projection transfer", "moving-profile top-bundle gap / evolution dichotomy / fixed-window exponential test"),
        ("Research topology · R0.1–R0.73D", "Research topology · R0.1–R0.73E"),
        ("R0.70A–R0.73D：82 节已公开，58 节完整封存", "R0.70A–R0.73E：83 节已公开，59 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73D</span>', '<span class="route-range">R0.69P–R0.73E</span>'),
        ('aria-label="R0.69P–R0.73D"', 'aria-label="R0.69P–R0.73E"'),
        ("展开 90 篇公开笔记", "展开 91 篇公开笔记"),
        ("本站 R0.69P–R0.73D 路线", "本站 R0.69P–R0.73E 路线"),
        ("综述 v1.44 · 2026-08-30", "综述 v1.45 · 2026-08-30"),
        ("上次综述 v1.43 · 2026-08-30", "上次综述 v1.44 · 2026-08-30"),
    ):
        html = required(html, old, new, "E home " + old)
    html = replace_all(html, "/recap-r0-61-r0-73d.html", "/recap-r0-61-r0-73e.html", "E home recap HTML links")
    html = replace_all(html, "/recap-r0-61-r0-73d.pdf", "/recap-r0-61-r0-73e.pdf", "E home recap PDF links")
    html = required(html, '<strong style="color:var(--gold)">下一步 R0.73E：</strong>&nbsp;complement resolvent、semigroup dichotomy 与 fixed-projection transfer。', '<strong style="color:var(--gold)">当时的下一步 R0.73E：</strong>&nbsp;complement resolvent、semigroup dichotomy 与 fixed-projection transfer。', "E home historical D next")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73E 已闭合固定正半平面分裂与对数快时间传递。下一关是在固定小物理窗口上证明或否证 moving-profile top bundle 的统一谱隙与演化二分。</span></div>', "E home focus")
    html = required(html, "<h3>R0.73D：认证 Rayleigh 谱簇的静态小黏性持续已闭合</h3>", "<h3>R0.73E：固定正半平面分裂与对数快时间传递已闭合</h3>", "E home current title")
    html = required(html, "<span>R0.72R–R0.73D：</span>", "<span>R0.72R–R0.73E：</span>", "E home path range")
    html = required(html, "certified frozen Rayleigh instability → static viscous cluster persistence</p>", "certified frozen Rayleigh instability → static viscous cluster persistence → fixed-half-plane logarithmic transfer</p>", "E home path tail")
    link_d = '<a class="milestone" href="/notes/r0-73d.html">R0.73D</a>'
    html = once(html, link_d, link_d + '\n                  <a class="milestone" href="/notes/r0-73e.html">R0.73E</a>', "E home route link")
    route_e = '              <p>R0.73E 把 compact--Fredholm 核心与完整竖线 resolvent 尾部拼接，闭合固定正半平面谱完备性、完整 top cluster 相对二分和对数快时间 Volterra 传递。固定窗口指数律、moving-profile top bundle、完整 OS--Squire、nonlinear 与 Clay 保持 OPEN。</p>\n'
    html = once(html, '              <details class="tree-notes" open>', route_e + '              <details class="tree-notes" open>', "E home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "E home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73E · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 121 个节点；全站现有 181 篇公开研究笔记</h3><p>累计回顾现分四十个阶段，完整保留 R0.61–R0.73E；最新节点分开记录 operator theorem、finite diagnostic、文献边界和 open gate。</p><p>R0.70A–R0.73E 共 83 个版本已公开；59 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;一条精确线性行上的固定正半平面与对数快时间传递已闭合；固定窗口、moving bundle、完整 OS--Squire、nonlinear 与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73e.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73e.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "E home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_E_CARD + '\n        </section>\n\n      </article>', "E home card")
    if html.count('data-release="r073e"') != 1:
        raise RuntimeError("home must contain exactly one R0.73E card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73F：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73F gate")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73E">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 91:
        raise RuntimeError("home current-route index must contain 91 note links")
    assert_clean(html, "R0.73E home")
    assert_mathjax_clean(html, "R0.73E home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (("/i18n-en.js?v=1.44", "/i18n-en.js?v=1.45"), ("本站 R0.69P–R0.73D 只列为研究笔记", "本站 R0.69P–R0.73E 只列为研究笔记"), ("文献综述 v1.44 · 2026-08-30", "文献综述 v1.45 · 2026-08-30"), ("累计回顾与 120 节索引", "累计回顾与 121 节索引"), ("打开 120 节完整索引", "打开 121 节完整索引")):
        html = required(html, old, new, "E literature " + old)
    html = replace_all(html, "/recap-r0-61-r0-73d.html", "/recap-r0-61-r0-73e.html", "E literature recap links")
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73E</b><strong>complement resolvent and fixed-projection transfer</strong></header><p>先控制右半平面 complement resolvent 与 semigroup dichotomy，再检查缓慢 profile drift 的 Volterra 传递。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73E</b><strong>fixed-half-plane splitting and logarithmic transfer</strong></header><p>固定正半平面谱完备性、完整 top cluster 相对二分与 \(M\log(1/\varepsilon)\) Volterra 传递已闭合。<a href="/notes/r0-73e.html">研究笔记</a> <a href="/recap-r0-61-r0-73e.html">当前累计回顾</a> <a href="#r073e-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73F</b><strong>moving-profile top bundle on a fixed physical window</strong></header><p>证明或否证统一谱隙与演化二分，目标是 fixed-window \(e^{c|\Lambda|}\)；graph-domain/Kato transport 仍只是候选方法。</p></div>'''
    html = once(html, old_open, new_steps, "E literature route")
    boundary = f'''

          <h3 id="r073e-boundary">R0.73E 的半平面 resolvent、相对二分与非自治边界</h3>
          <p><a href="https://doi.org/10.1016/j.anihpc.2007.05.004">Shvydkoy--Friedlander 2008</a> 是一般不稳定谱持续先例，但其定理没有明确标注本节所需总投影 operator-norm 拓扑。<a href="https://doi.org/10.1007/978-3-642-66282-9">Kato 的分离谱框架</a>与<a href="https://doi.org/10.1143/JPSJ.5.435">Kato 1950 adiabatic theorem</a>分开使用；<a href="https://doi.org/10.1142/S0129055X19500144">Schmid 的 time-independent-domain 定理</a>及其<a href="https://arxiv.org/abs/1804.11255">time-dependent-domain 预印本</a>也单独核对。<a href="https://doi.org/10.1090/S0002-9947-1978-0461206-1">Gearhart 1978</a>、<a href="https://doi.org/10.1090/S0002-9947-1984-0743749-9">Prüss 1984</a> 与 Engel--Nagel 说明半群统一界需要完整竖线控制。<a href="https://doi.org/10.1016/j.jde.2020.06.046">Grenier--Nguyen 2020</a> 在不同 no-slip half-space 几何和范数中给出统一半群先例。<a href="https://doi.org/10.1006/jdeq.1999.3668">Latushkin--Schnaubelt 1999</a>与<a href="https://doi.org/10.1016/j.na.2008.11.009">Popescu 2009</a>的 evolution-family 条件也没有被自动移植。本节不作原创性、一般强化或优先权声明。</p>
          <div class="boundary"><strong>R0.73E 的主张边界</strong><p>{CLOSED}。</p><p>{OPEN}。有限 Fourier 数据不承担 continuum proof。</p></div>'''
    match = re.search(r'(<h3 id="r073d-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("E literature expected R0.73D boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "E literature boundary")
    references = r'''            <li id="ref-113">T. Kato. <a href="https://doi.org/10.1007/978-3-642-66282-9"><em>Perturbation Theory for Linear Operators</em></a>. Springer, 1995 reprint.</li>
            <li id="ref-114">L. Gearhart. <a href="https://doi.org/10.1090/S0002-9947-1978-0461206-1"><em>Spectral theory for contraction semigroups on Hilbert space</em></a>. Trans. AMS 236 (1978), 385--394.</li>
            <li id="ref-115">J. Prüss. <a href="https://doi.org/10.1090/S0002-9947-1984-0743749-9"><em>On the spectrum of (C_0)-semigroups</em></a>. Trans. AMS 284 (1984), 847--857.</li>
            <li id="ref-116">E. Grenier and T. T. Nguyen. <a href="https://doi.org/10.1016/j.jde.2020.06.046"><em>Sharp bounds for the resolvent of linearized Navier--Stokes equations in the half space around a shear profile</em></a>. J. Differential Equations 269 (2020), 11540--11566.</li>
            <li id="ref-117">T. Kato. <a href="https://doi.org/10.1143/JPSJ.5.435"><em>On the Adiabatic Theorem of Quantum Mechanics</em></a>. J. Phys. Soc. Japan 5 (1950), 435--439.</li>
            <li id="ref-118">J. Schmid. <a href="https://doi.org/10.1142/S0129055X19500144"><em>Adiabatic theorems for general linear operators with time-independent domains</em></a>. Rev. Math. Phys. 31 (2019), 1950014.</li>
            <li id="ref-119">J. Schmid. <a href="https://arxiv.org/abs/1804.11255"><em>Adiabatic theorems for general linear operators with time-dependent domains</em></a>. arXiv:1804.11255 (2018).</li>
            <li id="ref-120">Y. Latushkin and R. Schnaubelt. <a href="https://doi.org/10.1006/jdeq.1999.3668"><em>Evolution semigroups, translation algebras, and exponential dichotomy of cocycles</em></a>. J. Differential Equations 159 (1999), 321--369.</li>
            <li id="ref-121">L. H. Popescu. <a href="https://doi.org/10.1016/j.na.2008.11.009"><em>Exponential dichotomy roughness and structural stability for evolution families without bounded growth and decay</em></a>. Nonlinear Analysis 71 (2009), 935--947.</li>
'''
    html = once(html, "          </ol>\n          <p class=\"source-note\">", references + "          </ol>\n          <p class=\"source-note\">", "E literature references")
    terminal = "R0.73D 再在精确 kinetic space 中证明认证无黏谱簇的 static vanishing-viscosity persistence、Riesz 投影算子范数收敛和代数重数保持；一般先例属于 Shvydkoy--Friedlander，补空间与快时间传递仍为 OPEN。"
    terminal_e = terminal + "R0.73E 用固定正半平面完备性、完整 top cluster 相对二分和固定生成元 Volterra 论证闭合 logarithmic fast-time transfer；moving-profile fixed-window、完整 OS--Squire、nonlinear 与 Clay 仍为 OPEN。"
    html = required(html, terminal, terminal_e, "E literature deck terminal")
    assert_clean(html, "R0.73E literature")
    assert_mathjax_clean(html, "R0.73E literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 181:
        raise RuntimeError("expected 181 public HTML notes after R0.73E")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    for key, value in R073D_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during generation: " + key)
    release.update({
        "latestCompletedRelease": "r073e", "siteVersion": "1.45",
        "publicHtmlNoteCount": 181, "postR060RecapNodeCount": 121,
        "nextRelease": "r073f",
        "latestReleaseGate": "tests/r073e-halfplane-transfer-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073e-release.test.mjs",
        "postR070APublishedReleaseCount": 83,
        "postR070AFormalSealedReleaseCount": 59,
        "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.44", "R0.73D", 180):
        raise RuntimeError("site-version is not at R0.73D")
    site.update({"version": "1.45", "latestRelease": "R0.73E", "publicHtmlNoteCount": 181, "publishedDate": "2026-08-30"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r073d", 82, 58, 24):
        raise RuntimeError("formal archive inventory is not at R0.73D")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r073d" or "r073e" in inventory[key]:
            raise RuntimeError("formal archive is not append-only: " + key)
        inventory[key].append("r073e")
    inventory.update({"latestPublishedRelease": "r073e", "publishedReleaseCount": 83, "formalSealedReleaseCount": 59, "legacyFormalFigureBacklogCount": 24})
    if len(inventory["publishedReleases"]) != 83 or len(inventory["formalSealedReleases"]) != 59:
        raise RuntimeError("formal archive count mismatch after R0.73E")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    release["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": digest(inventory_path),
    }
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "VERSION").write_text("1.45\n", encoding="utf-8")


def update_note_index() -> None:
    import generate_note_index as note_index
    note_index.PUBLIC = PUBLIC
    note_index.NOTES = PUBLIC / "notes"
    note_index.OUTPUT = note_index.NOTES / "index.html"
    notes = [note_index.parse_note(path) for path in note_index.note_files()]
    notes = [replace(note, has_pdf=True) if note.slug == "r0-73e" else note for note in notes]
    note_index.OUTPUT.write_text(note_index.render(notes), encoding="utf-8")
    index = note_index.OUTPUT.read_text(encoding="utf-8")
    for token in ('data-site-version="1.45"', "181 篇公开研究笔记", "<strong>R0.73E</strong><span>最新研究节点</span>", 'data-note="r0-73e"', "/recap-r0-61-r0-73e.html", "研究笔记总索引 · v1.45 · 2026-08-30"):
        if token not in index:
            raise RuntimeError("R0.73E note index missing token: " + token)


def main() -> None:
    preflight_release_state()
    validate_inputs()
    publish_figure_assets()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    update_note_index()
    for relative in ("research-review.html", "literature-review.html", "notes/index.html", "notes/r0-73e.html", "recap-r0-61-r0-73e.html"):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.73E", "siteVersion": "1.45", "notes": 181,
        "recapNodes": 121, "published": 83, "formalSealed": 59,
        "legacyBacklog": 24, "phases": 40, "routeNotes": 91,
        "next": "R0.73F", "rootVersion": "1.45",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
