#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate and validate the R0.73D public release from the R0.73C site."""

from __future__ import annotations

from dataclasses import replace
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from generate_r072o_release import (
    assert_clean,
    digest,
    once,
    required,
    section,
)
from generate_r072p_release import assert_mathjax_clean
from r073d_release_content import (
    CERTIFICATE_RELATIVE,
    EXPERIMENT_RELATIVE,
    FIGURE_ID,
    FIGURE_RELATIVE,
    HOME_D_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    R073C_RELEASE_BASELINE,
)


ROOT = Path(os.environ.get(
    "R073D_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"


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


def git_commit_for(relative: str) -> str:
    commit = subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", relative],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise RuntimeError("missing Git commit for " + relative)
    subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT, check=True,
    )
    return commit


def preflight_release_state() -> None:
    release = json.loads(
        (ROOT / "research/release-manifest.json").read_text(encoding="utf-8")
    )
    for key, value in R073C_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.73C: {key}")
    if release.get("nextReleaseSourceStage") is not None:
        raise RuntimeError("R0.73C baseline has an unexpected source-stage payload")
    expected_site = {
        "schemaVersion": "research-site-version-v1",
        "version": "1.43",
        "latestRelease": "R0.73C",
        "publicHtmlNoteCount": 179,
        "publishedDate": "2026-08-30",
    }
    site = json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8"))
    if site != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.73C")
    if (ROOT / "VERSION").read_text(encoding="utf-8") != "1.43\n":
        raise RuntimeError("root VERSION is not R0.73C v1.43")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 179:
        raise RuntimeError("R0.73C preflight expected 179 public HTML notes")
    for relative in (
        "notes/r0-73d.html", "notes/r0-73d.pdf",
        "recap-r0-61-r0-73d.html", "recap-r0-61-r0-73d.pdf",
    ):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.73C preflight found premature output: {relative}")
    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.43"', "<strong>179</strong>公开研究笔记",
        "<strong>R0.73C</strong>最新研究节点",
        'aria-label="R0.69P–R0.73C"',
    ):
        if token not in home:
            raise RuntimeError("R0.73C home baseline missing token: " + token)
    if 'data-release="r073d"' in home:
        raise RuntimeError("R0.73C home already contains an R0.73D card")
    recap = (PUBLIC / "recap-r0-61-r0-73c.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 119 or len(set(links)) != 119:
        raise RuntimeError("R0.73C recap must contain 119 unique nodes")
    inventory = json.loads(
        (ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8")
    )
    state = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073c", 81, 57, 24):
        raise RuntimeError("formal archive inventory is not at R0.73C")


def validate_inputs() -> None:
    required_inputs = (
        "research/r073d_report-source.md",
        "research/r073d_problem_freeze.md",
        "research/r073d_literature_audit.md",
        "research/r073d_gap_matrix.md",
        "research/r073d_viscous_persistence_proof.md",
        "research/r073d_independent_analytic_audit.md",
        "research/r073d_viscous_cluster_diagnostic.py",
        f"{CERTIFICATE_RELATIVE}/certificate.json",
        f"{CERTIFICATE_RELATIVE}/independent_recompute.json",
        f"{CERTIFICATE_RELATIVE}/validation.json",
        f"{CERTIFICATE_RELATIVE}/manifest.json",
        f"{EXPERIMENT_RELATIVE}/viscous_cluster_diagnostic.json",
        f"{EXPERIMENT_RELATIVE}/independent_validation.json",
        f"{EXPERIMENT_RELATIVE}/progress.ndjson",
        f"{FIGURE_RELATIVE}/manifest.json",
        f"{FIGURE_RELATIVE}/contract.json",
        f"{FIGURE_RELATIVE}/config.json",
        f"{FIGURE_RELATIVE}/caption.md",
        f"{FIGURE_RELATIVE}/validate.py",
        "public/notes/r0-73c.html",
        "public/recap-r0-61-r0-73c.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing R0.73D release input: " + relative)

    report = (ROOT / "research/r073d_report-source.md").read_text(encoding="utf-8")
    for token in (
        "staticVanishingViscosityPersistence=CLOSED",
        "fixedContourResolventUniform=CLOSED",
        "fixedClusterRieszProjectionNormConvergence=CLOSED",
        "fixedClusterAlgebraicMultiplicityPreserved=CLOSED",
        "fixedClusterEigenvaluesConverge=CLOSED",
        "Shvydkoy and Friedlander",
    ):
        if token not in report:
            raise RuntimeError("R0.73D report missing final token: " + token)
    for token in (
        "The constants defining the contour and the viscosity threshold are",
        "algebraic multiplicity is unknown",
        "remain open",
    ):
        if token not in report:
            raise RuntimeError("R0.73D report lost limitation: " + token)

    audit = (ROOT / "research/r073d_independent_analytic_audit.md").read_text(
        encoding="utf-8"
    )
    for token in ("PASS", "operator norm", "algebraic multiplicity", "right half-plane"):
        if token not in audit:
            raise RuntimeError("R0.73D independent audit missing token: " + token)

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_complete_flat_ledger(
        certificate, "R0.73D certificate", require_directory_complete=False
    )
    verify_complete_flat_ledger(figure, "R0.73D figure")
    subprocess.run(
        [sys.executable, str(certificate / "validate_certificate.py")],
        cwd=ROOT, check=True,
    )
    verify_complete_flat_ledger(
        certificate, "R0.73D certificate after validation",
        require_directory_complete=False,
    )
    certificate_payload = json.loads(
        (certificate / "certificate.json").read_text(encoding="utf-8")
    )
    validation = json.loads(
        (certificate / "validation.json").read_text(encoding="utf-8")
    )
    if validation.get("allChecksPass") is not True:
        raise RuntimeError("R0.73D certificate validation is not passed")
    theorem = certificate_payload.get("theorem", {})
    for key in (
        "staticVanishingViscosityPersistence",
        "fixedContourResolventUniform",
        "fixedClusterRieszProjectionNormConvergence",
        "fixedClusterAlgebraicMultiplicityPreserved",
        "fixedClusterEigenvaluesConverge",
    ):
        if theorem.get(key) != "CLOSED":
            raise RuntimeError("R0.73D theorem gate is not CLOSED: " + key)
    for key in (
        "inviscidEigenvalueSimple", "quantitativeEigenvalueRate",
        "uniformComplementaryDichotomy", "logFastTimeTransfer",
        "nonlinearNavierStokes", "clayProblemSolved",
    ):
        if certificate_payload.get("claimBoundary", {}).get(key) is not False:
            raise RuntimeError("R0.73D certificate escaped boundary: " + key)

    experiment = json.loads(
        (ROOT / EXPERIMENT_RELATIVE / "viscous_cluster_diagnostic.json").read_text(
            encoding="utf-8"
        )
    )
    independent = json.loads(
        (ROOT / EXPERIMENT_RELATIVE / "independent_validation.json").read_text(
            encoding="utf-8"
        )
    )
    if not all(experiment.get("checks", {}).values()):
        raise RuntimeError("R0.73D finite diagnostic checks are not passed")
    if independent.get("allChecksPass") is not True:
        raise RuntimeError("R0.73D independent finite validation is not passed")
    if experiment.get("claimBoundary", {}).get(
        "ordinaryCutoffConvergenceIsContinuumProof"
    ) is not False:
        raise RuntimeError("R0.73D finite diagnostic escaped continuum boundary")

    figure_manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    figure_contract = json.loads((figure / "contract.json").read_text(encoding="utf-8"))
    if (
        figure_manifest.get("release") != "R0.73D"
        or figure_manifest.get("figureId") != FIGURE_ID
        or figure_manifest.get("status") != "formal"
    ):
        raise RuntimeError("R0.73D figure identity or status mismatch")
    if (
        figure_manifest.get("qa", {}).get("status") != "passed"
        or figure_manifest.get("qa", {}).get("visualInspectionExplicit") is not True
    ):
        raise RuntimeError("R0.73D figure visual QA is not passed")
    claims = figure_contract.get("claimBoundary", {})
    if claims.get("staticVanishingViscosityPersistence") is not True:
        raise RuntimeError("R0.73D figure lost the static theorem")
    for key in (
        "finiteCurvesAreContinuumProof", "inviscidEigenvalueSimple",
        "explicitContourRadius", "logFastTimeTransfer",
        "nonlinearNavierStokes", "clayProblemSolved",
    ):
        if claims.get(key) is not False:
            raise RuntimeError("R0.73D figure escaped boundary: " + key)

    source_commit = str(figure_manifest.get("git", {}).get("sourceCommit", ""))
    certificate_commit = git_commit_for(
        "research/certificates/r073d/certificate.json"
    )
    if source_commit != git_commit_for(
        "figures/r073d/fig-r073d-viscous-cluster-persistence/plot.py"
    ):
        raise RuntimeError("R0.73D figure source commit is not the plotting commit")
    if figure_manifest.get("git", {}).get("certificateCommit") != certificate_commit:
        raise RuntimeError("R0.73D figure certificate commit is stale")
    committed_certificate = subprocess.run(
        ["git", "show", certificate_commit + ":research/certificates/r073d/certificate.json"],
        cwd=ROOT, check=True, capture_output=True,
    ).stdout
    if digest(ROOT / "research/certificates/r073d/certificate.json") != __import__(
        "hashlib"
    ).sha256(committed_certificate).hexdigest():
        raise RuntimeError("certificate commit does not contain the bound certificate")
    subprocess.run(
        [
            sys.executable, str(figure / "validate.py"),
            "--source-commit", source_commit,
            "--certificate-commit", certificate_commit,
        ],
        cwd=ROOT, check=True,
    )
    if figure_manifest.get("publication", {}).get("directory") != "public/assets/r073d":
        raise RuntimeError("R0.73D figure publication directory mismatch")


def publish_figure_assets() -> None:
    figure = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073d"
    target.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        source = figure / f"figure.{suffix}"
        destination = target / f"{FIGURE_ID}.{suffix}"
        shutil.copyfile(source, destination)
        if digest(destination) != digest(source):
            raise RuntimeError(f"R0.73D public {suffix} is not byte-identical")
    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    subprocess.run(
        [
            sys.executable, str(figure / "validate.py"),
            "--source-commit", manifest["git"]["sourceCommit"],
            "--certificate-commit", git_commit_for(
                "research/certificates/r073d/certificate.json"
            ),
        ],
        cwd=ROOT, check=True,
    )
    verify_complete_flat_ledger(figure, "R0.73D published figure")
    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("publication", {}).get("publicCopiesComplete") is not True:
        raise RuntimeError("R0.73D public figure copy ledger is incomplete")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-73c.html").read_text(encoding="utf-8")
    replacements = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="研究笔记 R0.73D：认证 Rayleigh 谱簇在充分小正黏性下持续，Riesz 投影按 kinetic-space 算子范数收敛；快时间与非线性仍开放。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.73D｜Static viscous persistence of a Rayleigh cluster">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="Fixed-cluster persistence, Riesz norm convergence, and algebraic multiplicity are CLOSED; complement, fast time, nonlinear, and Clay remain OPEN.">'),
        ("og image", r'<meta property="og:image" content=".*?">',
         f'<meta property="og:image" content="https://kasifa.github.io/assets/r073d/{FIGURE_ID}.png">'),
        ("title", r'<title>.*?</title>',
         '<title>R0.73D｜Static viscous persistence of a Rayleigh cluster</title>'),
    )
    for label, pattern, value in replacements:
        html = section(html, pattern, value, "D note " + label)
    html = required(html, "/i18n-en.js?v=1.43", "/i18n-en.js?v=1.44", "D note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#operator">算子</a><a href="#theorem">定理</a><a href="#isometry">等距变换</a><a href="#compact">紧修正</a><a href="#base">基础 resolvent</a><a href="#fredholm">Fredholm</a><a href="#projection">投影</a><a href="#multiplicity">重数</a><a href="#finite">有限诊断</a><a href="#literature">文献</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#boundary">边界</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "D note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "D note hero")
    toc_items = [
        ("result", "00 · direct decision"), ("operator", "01 · operator and space"),
        ("theorem", "02 · fixed-cluster theorem"), ("isometry", "03 · exact isometry"),
        ("compact", "04 · compact correction"), ("base", "05 · dissipative base"),
        ("fredholm", "06 · Fredholm contour"), ("projection", "07 · projection norm"),
        ("multiplicity", "08 · multiplicity"), ("finite", "09 · finite diagnostic"),
        ("literature", "10 · literature boundary"), ("figure", "11 · journal figure"),
        ("value", "12 · value"), ("boundary", "13 · exact boundary"),
        ("next", "14 · R0.73E"), ("reproduce", "15 · reproduction"),
    ]
    toc = '      <aside class="toc"><strong>CONTENTS</strong><ol>\n' + "".join(
        f'        <li><a href="#{anchor}">{label}</a></li>'
        for anchor, label in toc_items
    ) + '\n      </ol></aside>'
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "D note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "D note article")
    html = section(
        html, r'<footer>.*?</footer>',
        '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.73D · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>',
        "D note footer",
    )
    for stale in ("fig-r073c-certified-rayleigh-instability", "周期单值矩阵的实迹"):
        if stale in html:
            raise RuntimeError("R0.73D note contains stale R0.73C copy: " + stale)
    assert_clean(html, "R0.73D note")
    assert_mathjax_clean(html, "R0.73D note")
    (PUBLIC / "notes/r0-73d.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-73c.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73D 共 120 个节点；最新一节闭合认证 Rayleigh 谱簇的静态小黏性持续。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.61–R0.73D｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="三十九个阶段、120 个节点：从约化递推和环带排除到认证 Rayleigh 谱簇的静态黏性持续。">'),
        ("title", r'<title>.*?</title>',
         '<title>R0.61–R0.73D｜R0.60 之后的研究回顾</title>'),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "D recap " + label)
    html = required(html, "/i18n-en.js?v=1.43", "/i18n-en.js?v=1.44", "D recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.73D · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页保留 R0.61 到 R0.73D 的全部 120 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C 认证无穷维冻结 Rayleigh 不稳定；R0.73D 再闭合固定谱簇的静态小黏性持续。一般三维 nonlinear 与 Clay 没有被外推。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73D</strong><p>收录节点：120</p><p>回顾截止时公开笔记：180</p><p>回顾截止节点：R0.73D</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "D recap hero")
    for old, new in (
        ("02 · 119 节完整索引", "02 · 120 节完整索引"),
        ("01 · 三十八个研究阶段", "01 · 三十九个研究阶段"),
        ("R0.60 之后的路线分成三十八个阶段", "R0.60 之后的路线分成三十九个阶段"),
        ('data-current-route="R0.69P–R0.73C"', 'data-current-route="R0.69P–R0.73D"'),
    ):
        html = required(html, old, new, "D recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>120</strong><span>R0.61–R0.73D 研究节点</span></div><div class="metric"><strong>82</strong><span>R0.70A–R0.73D 已公开版本</span></div><div class="metric"><strong>58</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73D 的 82 个版本已经公开，其中 58 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "D recap result")
    phase = r'''            <article class="phase"><h3>R0.73D · Static viscous persistence of the certified Rayleigh cluster</h3><p>在固定 \(d=0,\gamma=1/2\) 行上，exact kinetic-space isometry、紧 Fourier commutator、耗散基础 resolvent 与 Fredholm 因子闭合 fixedContourResolventUniform。</p><p>减去解析基础 resolvent 后，紧 sandwich 在围道上一致按算子范数收敛，因此 fixedClusterRieszProjectionNormConvergence、fixedClusterAlgebraicMultiplicityPreserved 与 fixedClusterEigenvaluesConverge 全部为 CLOSED。</p><p>一般谱持续先例属于 Shvydkoy--Friedlander；本节不作首创声明。单性、显式阈值、全右半平面 complement、moving profile、fast time、完整 OS--Squire、nonlinear 与 Clay 保持 OPEN。</p><div class="links"><a href="/notes/r0-73d.html">R0.73D</a><a href="/assets/r073d/fig-r073d-viscous-cluster-persistence.pdf">R0.73D 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073d">R0.73D 证书</a></div></article>
'''
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "D recap phase")
    html = required(
        html, "R0.61–R0.73C 的 119 节公开笔记",
        "R0.61–R0.73D 的 120 节公开笔记", "D recap node title",
    )
    node_c = '            <span class="node-ref"><a href="/notes/r0-73c.html">R0.73C</a><span class="node-state kind-closed">闭</span></span>\n'
    node_d = '            <span class="node-ref"><a href="/notes/r0-73d.html">R0.73D</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_c, node_c + node_d, "D recap node")
    retained = r'''            <li>R0.73D 闭合认证 Rayleigh 谱簇的 static vanishing-viscosity persistence、Riesz 投影算子范数收敛、总代数重数保持与簇特征值收敛；补空间和非自治传递仍开放。</li>
'''
    html = once(
        html, "          </ul>\n          <p>这些结果可以分别整理成",
        retained + "          </ul>\n          <p>这些结果可以分别整理成",
        "D recap retained",
    )
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>冻结不稳定与静态黏性持续都已成为定理；全局动力学仍缺补空间控制</h2><p>不能把 120 个节点或 82 个公开版本解释成 Clay 完成比例。R0.73D 的严格增量是 fixed-cluster operator theorem，不是有限矩阵外推；一般 abstract persistence 已有 Shvydkoy--Friedlander 先例。本节对后续快时间路线有必要价值，但仍只覆盖一条冻结二维线性行。</p></section>''', "D recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73E 检查 complement resolvent、semigroup dichotomy 与 fixed-projection transfer</h2><p>先在固定右半平面带中排除围道外谱污染并控制 complement semigroup，再检查缓慢 profile drift 的 Volterra 传递。</p></section>''', "D recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73D 的 82 节已公开；58 节完整封存；24 节旧档待回补。</p><p>staticVanishingViscosityPersistence、fixedClusterRieszProjectionNormConvergence、fixedClusterAlgebraicMultiplicityPreserved 与 fixedClusterEigenvaluesConverge 为 CLOSED。inviscidEigenvalueSimple、quantitativeEigenvalueRate、globalRightHalfPlaneNoPollution、uniformComplementaryDichotomy、movingProfileUniformContour、logFastTimeTransfer、completeOSSquireA2DirectSum、nonlinearNavierStokes 与 Clay 为 OPEN。</p></section>''', "D recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、证书、有限诊断、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73c.html">保留 R0.73C 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73d.html">打开最新节点 R0.73D</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073d_viscous_persistence_proof.md">查看 R0.73D 证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073d">查看 R0.73D 正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073d">查看有限诊断与监控记录</a> · <a href="/assets/r073d/fig-r073d-viscous-cluster-persistence.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73d.pdf">下载同步 PDF</a></p><p>continuum theorem 来自 compact-Fredholm 解析证明。Fourier cutoff 只做诊断和附图，不证明无穷维谱持续。</p></section>''', "D recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73D 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>', "D recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 120 or len(set(links)) != 120:
        raise RuntimeError("R0.73D recap expected 120 unique nodes")
    if html.count('<article class="phase">') != 39:
        raise RuntimeError("R0.73D recap expected 39 phases")
    assert_clean(html, "R0.73D recap")
    assert_mathjax_clean(html, "R0.73D recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-73d.html").write_text(html, encoding="utf-8")


def replace_all(html: str, old: str, new: str, label: str) -> str:
    count = html.count(old)
    if count == 0:
        raise RuntimeError(label + ": source not found")
    return html.replace(old, new)


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    html = section(
        html,
        r'    <section class="route-overview latest-release-spotlight".*?</section>',
        HOME_LATEST_SPOTLIGHT,
        "D home latest spotlight",
    )
    for old, new in (
        ('data-site-version="1.43"', 'data-site-version="1.44"'),
        ("/i18n-en.js?v=1.43", "/i18n-en.js?v=1.44"),
        ("/site-refresh.js?v=1.43", "/site-refresh.js?v=1.44"),
        ("<strong>v1.43</strong>网页版本", "<strong>v1.44</strong>网页版本"),
        ("<strong>179</strong>公开研究笔记", "<strong>180</strong>公开研究笔记"),
        ("<strong>R0.73C</strong>最新研究节点", "<strong>R0.73D</strong>最新研究节点"),
        ("Research topology · R0.1–R0.73C", "Research topology · R0.1–R0.73D"),
        ("R0.70A–R0.73C：81 节已公开，57 节完整封存", "R0.70A–R0.73D：82 节已公开，58 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73C</span>', '<span class="route-range">R0.69P–R0.73D</span>'),
        ('aria-label="R0.69P–R0.73C"', 'aria-label="R0.69P–R0.73D"'),
        ("展开 89 篇公开笔记", "展开 90 篇公开笔记"),
        ("本站 R0.69P–R0.73C 路线", "本站 R0.69P–R0.73D 路线"),
        ("综述 v1.43 · 2026-08-30", "综述 v1.44 · 2026-08-30"),
        ("上次综述 v1.42 · 2026-08-30", "上次综述 v1.43 · 2026-08-30"),
    ):
        html = required(html, old, new, "D home " + old)
    html = replace_all(html, "/recap-r0-61-r0-73c.html", "/recap-r0-61-r0-73d.html", "D home recap HTML links")
    html = replace_all(html, "/recap-r0-61-r0-73c.pdf", "/recap-r0-61-r0-73d.pdf", "D home recap PDF links")
    html = required(
        html,
        '<strong style="color:var(--gold)">下一步 R0.73D：</strong>&nbsp;vanishing-viscosity Evans/Riesz persistence。',
        '<strong style="color:var(--gold)">当时的下一步 R0.73D：</strong>&nbsp;vanishing-viscosity Evans/Riesz persistence。',
        "D home historical C next",
    )
    html = section(
        html,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73D 已闭合认证 Rayleigh 谱簇的静态小黏性持续。下一关是 complement resolvent、semigroup dichotomy 与 fixed-projection transfer。</span></div>',
        "D home focus",
    )
    html = required(
        html, "<h3>R0.73C：无穷维冻结 Rayleigh 不稳定已闭合</h3>",
        "<h3>R0.73D：认证 Rayleigh 谱簇的静态小黏性持续已闭合</h3>",
        "D home current title",
    )
    html = required(html, "<span>R0.72R–R0.73C：</span>", "<span>R0.72R–R0.73D：</span>", "D home path range")
    html = required(
        html,
        "certified frozen Rayleigh instability</p>",
        "certified frozen Rayleigh instability → static viscous cluster persistence</p>",
        "D home path tail",
    )
    link_c = '<a class="milestone" href="/notes/r0-73c.html">R0.73C</a>'
    html = once(html, link_c, link_c + '\n                  <a class="milestone" href="/notes/r0-73d.html">R0.73D</a>', "D home route link")
    route_d = r'''              <p>R0.73D 在 exact kinetic space 中保留定义域跳变，用紧 Fourier commutator、耗散基础 resolvent 和 Fredholm 因子证明固定黏性谱簇持续；Riesz 投影按算子范数收敛，总代数重数保持。一般先例属于 Shvydkoy--Friedlander；simplicity、rate、complement、fast time、nonlinear 与 Clay 保持 OPEN。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_d + '              <details class="tree-notes" open>', "D home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "D home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73D · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 120 个节点；全站现有 180 篇公开研究笔记</h3><p>累计回顾现分三十九个阶段，完整保留 R0.61–R0.73D；R0.73D 分开记录 operator theorem、finite diagnostic、一般文献先例和 open gate。</p><p>R0.70A–R0.73D 共 82 个版本已公开；58 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;冻结 Rayleigh 不稳定与固定谱簇静态黏性持续已闭合；complement、fast time、A2、nonlinear 与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73d.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73d.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "D home recap")
    html = once(
        html,
        '          </div>\n        </section>\n\n      </article>',
        '          </div>\n\n' + HOME_D_CARD + '\n        </section>\n\n      </article>',
        "D home card",
    )
    if html.count('data-release="r073d"') != 1:
        raise RuntimeError("home must contain exactly one R0.73D card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73E：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73E gate")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73D">(.*?)</nav>',
        html, flags=re.S,
    )
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 90:
        raise RuntimeError("home current-route index must contain 90 note links")
    assert_clean(html, "R0.73D home")
    assert_mathjax_clean(html, "R0.73D home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.43", "/i18n-en.js?v=1.44"),
        ("本站 R0.69P–R0.73C 只列为研究笔记", "本站 R0.69P–R0.73D 只列为研究笔记"),
        ("文献综述 v1.43 · 2026-08-30", "文献综述 v1.44 · 2026-08-30"),
        ("累计回顾与 119 节索引", "累计回顾与 120 节索引"),
        ("打开 119 节完整索引", "打开 120 节完整索引"),
    ):
        html = required(html, old, new, "D literature " + old)
    html = replace_all(html, "/recap-r0-61-r0-73c.html", "/recap-r0-61-r0-73d.html", "D literature recap links")
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73D</b><strong>vanishing-viscosity Evans/Riesz persistence</strong></header><p>先闭合黏性特征值延拓、统一 Riesz 投影和补空间 resolvent，再进入非自治 Kato transport。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73D</b><strong>static viscous persistence of the certified Rayleigh cluster</strong></header><p>fixed contour、Riesz projection norm convergence、cluster multiplicity 与 cluster eigenvalue convergence 已闭合。一般先例属于 Shvydkoy--Friedlander；不作首创声明。<a href="/notes/r0-73d.html">研究笔记</a> <a href="/recap-r0-61-r0-73d.html">当前累计回顾</a> <a href="#r073d-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73E</b><strong>complement resolvent and fixed-projection transfer</strong></header><p>先控制右半平面 complement resolvent 与 semigroup dichotomy，再检查缓慢 profile drift 的 Volterra 传递。</p></div>'''
    html = once(html, old_open, new_steps, "D literature route")
    boundary = r'''

          <h3 id="r073d-boundary">R0.73D 的无黏到黏性谱持续与固定谱簇边界</h3>
          <p>Shvydkoy--Friedlander 2008 的 Theorem 2.1(ii)--(iii) 是一般周期无黏到黏性不稳定谱持续、代数重数与 Riesz 谱子空间的决定性先例。Li 2005 给出周期 Kolmogorov-flow 例子；Li--Lin 2011 在 no-slip channel 中用 Wasow 渐近与 Rouché 定理处理 Orr--Sommerfeld 延拓。R0.73D 的增量是认证 double-harmonic row 在精确 kinetic space 中的自包含 compact-Fredholm 实现，并明确证明固定谱簇投影的算子范数收敛；不作一般首创、严格强化或优先权声明。</p>
          <div class="boundary"><strong>R0.73D 的主张边界</strong><p>staticVanishingViscosityPersistence、fixedClusterRieszProjectionNormConvergence、fixedClusterAlgebraicMultiplicityPreserved 与 fixedClusterEigenvaluesConverge 为 CLOSED。inviscidEigenvalueSimple、quantitativeEigenvalueRate、globalRightHalfPlaneNoPollution、uniformComplementaryDichotomy、movingProfileUniformContour、logFastTimeTransfer、completeOSSquireA2DirectSum、nonlinearNavierStokes 与 Clay 为 OPEN。有限 Fourier 曲线不承担 continuum proof。</p></div>'''
    match = re.search(r'(<h3 id="r073c-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("D literature expected R0.73C boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "D literature boundary")
    terminal = "R0.73C 随后用 exact cubic neutral spectrum 与 validated periodic-ODE monodromy sign certificate 证明一条 infinite-dimensional frozen Rayleigh instability；viscous fast-time transfer 仍为 OPEN，super-polynomial complete-row no-go 只为 CONDITIONAL。"
    terminal_d = terminal + "R0.73D 再在精确 kinetic space 中证明认证无黏谱簇的 static vanishing-viscosity persistence、Riesz 投影算子范数收敛和代数重数保持；一般先例属于 Shvydkoy--Friedlander，补空间与快时间传递仍为 OPEN。"
    html = required(html, terminal, terminal_d, "D literature deck terminal")
    assert_clean(html, "R0.73D literature")
    assert_mathjax_clean(html, "R0.73D literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 180:
        raise RuntimeError("expected 180 public HTML notes after R0.73D")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    for key, value in R073C_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during generation: " + key)
    release.update({
        "latestCompletedRelease": "r073d", "siteVersion": "1.44",
        "publicHtmlNoteCount": 180, "postR060RecapNodeCount": 120,
        "nextRelease": "r073e",
        "latestReleaseGate": "tests/r073d-viscous-persistence-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073d-release.test.mjs",
        "postR070APublishedReleaseCount": 82,
        "postR070AFormalSealedReleaseCount": 58,
        "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    release_path.write_text(
        json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.43", "R0.73C", 179):
        raise RuntimeError("site-version is not at R0.73C")
    site.update({
        "version": "1.44", "latestRelease": "R0.73D",
        "publicHtmlNoteCount": 180, "publishedDate": "2026-08-30",
    })
    site_path.write_text(
        json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073c", 81, 57, 24):
        raise RuntimeError("formal archive inventory is not at R0.73C")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r073c" or "r073d" in inventory[key]:
            raise RuntimeError("formal archive is not append-only: " + key)
        inventory[key].append("r073d")
    inventory.update({
        "latestPublishedRelease": "r073d", "publishedReleaseCount": 82,
        "formalSealedReleaseCount": 58, "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 82 or len(inventory["formalSealedReleases"]) != 58:
        raise RuntimeError("formal archive count mismatch after R0.73D")
    inventory_path.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (ROOT / "VERSION").write_text("1.44\n", encoding="utf-8")


def update_note_index() -> None:
    import generate_note_index as note_index

    note_index.PUBLIC = PUBLIC
    note_index.NOTES = PUBLIC / "notes"
    note_index.OUTPUT = note_index.NOTES / "index.html"
    notes = [note_index.parse_note(path) for path in note_index.note_files()]
    notes = [replace(note, has_pdf=True) if note.slug == "r0-73d" else note for note in notes]
    note_index.OUTPUT.write_text(note_index.render(notes), encoding="utf-8")
    index = note_index.OUTPUT.read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.44"', "180 篇公开研究笔记",
        "<strong>R0.73D</strong><span>最新研究节点</span>",
        'data-note="r0-73d"', "/recap-r0-61-r0-73d.html",
        "研究笔记总索引 · v1.44 · 2026-08-30",
    ):
        if token not in index:
            raise RuntimeError("R0.73D note index missing token: " + token)


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
    for relative in (
        "research-review.html", "literature-review.html", "notes/index.html",
        "notes/r0-73d.html", "recap-r0-61-r0-73d.html",
    ):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.73D", "siteVersion": "1.44", "notes": 180,
        "recapNodes": 120, "published": 82, "formalSealed": 58,
        "legacyBacklog": 24, "phases": 39, "routeNotes": 90,
        "next": "R0.73E", "rootVersion": "1.44",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
