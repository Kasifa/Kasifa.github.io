#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed R0.72Z OS--Squire threshold release.

R0.72Z closes a signed high-gap Orr--Sommerfeld graph tier and exact
orientation-paid Squire history estimates.  It leaves the low-gap physical
row, the complete linearized subsystem, nonlinear Navier--Stokes, and the
Clay problem open.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from generate_r072o_release import (
    assert_clean,
    digest,
    once,
    required,
    section,
    verify_flat_hash_ledger,
)
from generate_r072p_release import assert_mathjax_clean


ROOT = Path(os.environ.get("R072Z_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r072z-os-squire-threshold"
FIGURE_RELATIVE = f"figures/r072z/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r072z"

R072Y_RELEASE_BASELINE = {
    "latestCompletedRelease": "r072y",
    "siteVersion": "1.38",
    "publicHtmlNoteCount": 175,
    "postR060RecapNodeCount": 115,
    "nextRelease": "r072z",
    "latestReleaseGate": "tests/r072y-full-row-forced-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r072y-release.test.mjs",
    "postR070APublishedReleaseCount": 77,
    "postR070AFormalSealedReleaseCount": 53,
    "legacyFormalFigureBacklogCount": 24,
}

SOURCE_STAGE_CONTRACT = {
    "release": "r072z",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r072z_report-source.md",
    "literatureAudit": "research/r072z_literature_audit.md",
    "gapMatrix": "research/r072z_gap_matrix.md",
    "independentAudit": "research/r072z_independent_audit.md",
    "producer": "research/certificates/r072z/generate_certificate.py",
    "independentProducer": "research/certificates/r072z/independent_recompute.py",
    "comparator": "research/certificates/r072z/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r072z_release.py",
    "translationScript": "scripts/add-r072z-translations.mjs",
    "releaseGate": "tests/r072z-os-squire-gate.test.mjs",
    "publicationTest": "tests/r072z-release.test.mjs",
}

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.72Z · ORR--SOMMERFELD · SQUIRE ORIENTATION</div>
        <h1>压力反馈的高间隙阈值，<br>与必须支付的 Squire 方向代价</h1>
        <p class="lead">我把 Orr--Sommerfeld 压力项写成精确有符号交换子形式，在 signed high-gap 类上得到 prefactor-one 衰减与受迫 graph estimates；同时把 Squire 传递拆成精确方向系数和历史卷积。结论明确停在 high-gap \(q\)-graph：low-gap physical row、完整 direct sum、非线性闭合与 Clay 问题仍为 OPEN。</p></div>
      <div class="stamp"><span class="state">状态 · R0.72Z scoped graph tier 完成</span><strong>high-gap OS and orientation-paid Squire</strong><p>版本 v0.72Z · 2026-08-28</p><p>high-gap q graph: CLOSED</p><p>orientation-paid history: CLOSED</p><p>all-row prefactor-one: FALSE</p><p>low-gap physical row: OPEN</p><p>nonlinear / Clay: OPEN</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>高间隙 \(q\)-graph 已闭合；低间隙物理行没有被外推</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · HIGH-GAP OS</strong><p>exactOSFeedbackCommutatorIdentity=CLOSED；signedRelativeFormOSAbsorption=CLOSED；highGapOSPrefactorOneDecay=CLOSED；highGapOSForcedScaleLedger=CLOSED；alphaMinusTwoOSGapSufficiency=CLOSED。</p></div><div class="verdict-card true"><strong>CLOSED · SQUIRE WITH PAYMENT</strong><p>exactSquireDuhamel=CLOSED；exactKineticOrientationNormalization=CLOSED；optimalInstantaneousSquireCoefficient=CLOSED；orientationUniformWithLambdaPayment=CLOSED；fixedRowOSSquireGraphRegularity=CLOSED。</p></div><div class="verdict-card false"><strong>FALSE · UNPAID UNIFORMITY</strong><p>allStrongRowsOSPrefactorOneContraction=FALSE；rawOrientationUniformFromCOnly=FALSE；epsilonOnlySquireTransfer=FALSE；uniformlyEquivalentLambdaIndependentContractiveNorm=FALSE。</p></div><div class="verdict-card false"><strong>OPEN · LOW GAP AND CLAY</strong><p>lowGapOSTransientA2Propagator=OPEN；unconditionalStrongFullRowA2Estimate=OPEN；BlochUniformPhysicalVelocityDirectSum=OPEN；nonlinearNavierStokes=OPEN；Clay=OPEN。</p></div></div></section>
        <section id="form"><div class="section-no">01 / Exact pressure form</div><h2>压力反馈不是无结构的 bounded perturbation</h2><div class="equation result">\[q_d=(-\mathcal L-icW)q-icW_{xx}\mathcal L^{-1}q.\]</div><p>交换子恒等式把实部化成含 \(W_{xxx}\) 的有符号相对 form；它固定了符号，也避免把低间隙压力项错误当成普通 \(L^2\) forcing。</p></section>
        <section id="threshold"><div class="section-no">02 / Signed threshold</div><h2>精确 signed threshold 与显式 sufficient majorant 分开记录</h2><div class="equation result">\[\Theta_K(c,\beta,\mu)=\sup_{d\in K}\lambda_{\max}(-cH_{\beta,\mu}(d))<1,\]</div><div class="equation result">\[\Theta_K\le\widehat\Theta_K:=|c|M_{3,K}g^{-3/2}s_{\beta,\mu},\qquad g=\operatorname{dist}(\beta,\mathbb Z)^2+\mu.\]</div><div class="equation result">\[\|U_{\rm OS}(d,s)\|_{2\to2}\le e^{-(1-\Theta_K)g(d-s)}.\]</div><p>这是一条 signed high-gap \(q\)-graph theorem，不是完整 physical kinetic-energy theorem。</p></section>
        <section id="power"><div class="section-no">03 / Explicit high-gap class</div><h2>\(g\gtrsim |c|^{2/5}\) 是透明的充分条件</h2><div class="equation result">\[g\ge\left(\frac{|c|M_{3,K}}{\theta_0}\right)^{2/5}\quad\Longrightarrow\quad \widehat\Theta_K\le\theta_0<1.\]</div><p>在 \(|c|=4\alpha^{-5}\) 下，这给出 \(g\gtrsim\alpha^{-2}\)。该 \(2/5\) 指数对无权瞬时 coercivity 的高模二频 witness 是 sharp；它不宣称临界 low-gap propagator 已解决。</p></section>
        <section id="forcing"><div class="section-no">04 / Forced graph ledger</div><h2>受迫尺度只在 signed high-gap 类继承</h2><p>指数 kernel 给出 \(L_d^2L_x^2\)、standard \(H^{-1}\) 与 semiclassical negative norm 的显式输入输出常数。每条估计都保留 \((1-\Theta_K)g\)；没有把 R0.72Y 的 scalar power 自动推广到全部 strong rows。</p></section>
        <section id="counter"><div class="section-no">05 / Prefactor-one obstruction</div><h2>低模二频 witness 产生正的瞬时增长</h2><p>选择压力 form 的符号与二频数据，可使 \(d\|q\|_2^2/dd>0\)。因此 allStrongRowsOSPrefactorOneContraction=FALSE；仍可能存在带 transient prefactor 的 low-gap theorem。</p></section>
        <section id="tangent"><div class="section-no">06 / Exact tangent mode</div><h2>gapless abstract OS 行精确沿 heat tangent 演化</h2><div class="equation result">\[q_*(d)=W_{xx}(d),\qquad \mathcal L_0^{-1}q_*=-W,\qquad (q_*)_d=W_{xxxx}.\]</div><p>两项非正规输运精确抵消，所以 abstractGaplessOSA2StrictContraction=FALSE。该 witness 属于 unprojected abstract mean-zero OS equation；我没有把它冒充 \(\mu=0\) physical velocity row。</p></section>
        <section id="collision"><div class="section-no">07 / Collision scaling</div><h2>缩放后压力反馈仍是 leading order</h2><p>在 \(d=\alpha^2S,\ x=\alpha X\) 下，transport 与 \(V_{XX}\mathcal L_\alpha^{-1}\) 同阶。high-gap perturbation 因而不能直接穿过 collision；collisionScaleOSLimitingAbsorption 保持 OPEN。</p></section>
        <section id="squire"><div class="section-no">08 / Exact Squire history</div><h2>终点值不能替代 \(q\) 的因果历史</h2><div class="equation result">\[\eta(d)=U_c(d,d_-)\eta_-+i\xi\Lambda\int_{d_-}^{d}U_c(d,s)W_x\mathcal L^{-1}q(s)\,ds.\]</div><p>instantaneousQEndpointAloneControlsEta=FALSE；正确输入是带 kernel 的历史范数。</p></section>
        <section id="orientation"><div class="section-no">09 / Kinetic orientation</div><h2>方向归一化把不可避免的 \(\Lambda\) payment 写清</h2><div class="equation result">\[b_j(d)=\|M_{W_x(d)}\mathcal L^{-1/2}\|_{2\to2},\qquad a_j(d)=|\xi\Lambda|b_j(d),\]</div><div class="equation result">\[a_{j,K}\le |\Lambda|M_{1,K}\chi_j,\qquad \chi_j=\frac{|\xi|}{\sqrt g}\le1.\]</div><p>给定 \(|\Lambda|\) payment 后可对方向统一；只从 \(c=\gamma\Lambda\) 推出 angle-uniform bound 为 FALSE，因为 \(\gamma\to0\) 会暴露 transverse lift-up。</p></section>
        <section id="optimal"><div class="section-no">10 / Exact instantaneous coefficient</div><h2>有限维方向矩阵的 induced norm 给出最优瞬时常数</h2><p>optimalInstantaneousSquireCoefficient=CLOSED。粗略 \(M_{1,K}g^{-1/2}\) 上界便于 direct estimates，但不被宣称在每一行都达到。</p></section>
        <section id="kernel"><div class="section-no">11 / Strong-kernel transfer</div><h2>history payment 同时保留普通 gap 与 A2 block kernel</h2><div class="equation result">\[\ell_j=\min\{g^{-1},A_\vartheta\alpha^2\},\qquad m_j=\min\{(2g)^{-1/2},\sqrt{B_\vartheta}\alpha\}.\]</div><p>strongKernelConditionalSquireTransfer 是 conditional CLOSED：它以已经声明的 \(Q\)-history estimate 为输入，不反向证明 low-gap OS propagator。</p></section>
        <section id="rates"><div class="section-no">12 / Damping-rate collision</div><h2>相等衰减率必须保留 transient polynomial</h2><div class="equation result">\[\int_0^\tau e^{-\lambda(\tau-s)}e^{-\omega s}\,ds=\frac{e^{-\omega\tau}-e^{-\lambda\tau}}{\lambda-\omega}\to\tau e^{-\lambda\tau}.\]</div><p>equalRateUniformGapDenominator=FALSE；分母不能在 \(\lambda=\omega\) 时被静态常数替代。</p></section>
        <section id="graph"><div class="section-no">13 / Fixed-row graph theorem</div><h2>固定 high-gap OS--Squire graph tier 已闭合</h2><p>在 \(\Theta_K<1\)、\(\mu>0\) 且支付显式 orientation、gap 与 \(|\Lambda|\) 权重时，\(q\to\eta\to u\) 的固定行 graph regularity 为 CLOSED。该范数的等价常数随参数退化，所以不能直接求和成 uniform kinetic direct sum。</p></section>
        <section id="literature"><div class="section-no">14 / Literature boundary</div><h2>固定几何 OS 与 Squire 先例存在；collision 组合没有被这些文献覆盖</h2><p>Jia、Beekie--Chen--Jia、Ding--Lin 处理 active OS pressure 的固定谱或临界几何；Li--Wei--Zhang 与 Jerome--Chomaz 显示三维 Squire orientation/lift-up 结构。我只报告有界 primary-source search，不把“未发现”写成首创性证明。</p></section>
        <section id="evidence"><div class="section-no">15 / Evidence boundary</div><h2>解析证明、双路证书和附图各自限界</h2><p>解析报告承担无限维 form bounds、semigroup、sharpness limit 与 graph domain。双路证书核对符号、有限 Fourier pairs、指数算术、kernel 与方向矩阵。附图只展示已证明 threshold、witness 与 payment，不构成证明。</p></section>
        <section id="figure"><div class="section-no">16 / Journal figure</div><h2>正式附图分开 high-gap closure、negative witnesses 与 Squire payment</h2><p><img src="/assets/r072z/fig-r072z-os-squire-threshold.svg" alt="R0.72Z signed OS threshold and orientation-paid Squire transfer"></p><p><a href="/assets/r072z/fig-r072z-os-squire-threshold.pdf">下载 PDF</a> · <a href="/assets/r072z/fig-r072z-os-squire-threshold.png">下载 PNG</a> · <a href="/assets/r072z/fig-r072z-os-squire-threshold.svg">打开 SVG</a></p></section>
        <section id="value"><div class="section-no">17 / Research value</div><h2>本节把“压力项未处理”改成一个精确分区问题</h2><p>严格增量是 high-gap OS threshold、sharp obstruction、exact tangent mode 与 orientation-paid Squire history。直接 Clay 价值仍低：low-gap physical rows、Bloch-uniform direct sum、nonlinear convolution、vortex stretching bootstrap 与 continuation criterion 均未完成。</p></section>
        <section id="next"><div class="section-no">18 / Next gate</div><h2>R0.73A：分离 tangent/lift-up 子空间，寻找带 transient prefactor 的 low-gap OS propagator</h2><p>下一节不再要求不可能的 all-row prefactor-one contraction；目标是识别有限维慢模、构造投影后 resolvent/propagator estimate，并保持 physical-row 与 abstract tangent witness 的边界。</p></section>
        <section id="reproduce"><div class="section-no">19 / Reproduction</div><h2>完整报告、文献审计、边界矩阵、证书与附图</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072z_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072z_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072z_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072z_independent_audit.md">独立数学审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072z">确定性双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072z/fig-r072z-os-squire-threshold">正式附图包</a> · <a href="/notes/r0-72z.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72z.html">累计回顾</a> · <a href="/recap-r0-61-r0-72z.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73A</span><span class="tree-state current">下一检查点</span></div>
              <h3>projected low-gap OS propagator with a transient prefactor</h3><p>分离 tangent/lift-up 慢子空间，研究投影后 limiting absorption 与 low-gap propagator；任何结论都保留 physical-row、Bloch 与参数权重。</p>
            </article>'''

HOME_Z_CARD = r'''          <div class="task-one" id="r072z" data-release="r072z" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72Z · 2026-08-28</p><h3>压力反馈的 high-gap threshold 与 orientation-paid Squire history</h3>
            <p>我把 Orr--Sommerfeld pressure feedback 写成 exact signed relative form，并在显式 high-gap 类上闭合 prefactor-one \(q\)-graph 与 forced ledger。</p><p>Squire 传递按 exact orientation coefficient、\(\Lambda\) payment 与 causal history 记录；只从 \(c\) 推导 angle-uniform bound、all-row prefactor-one contraction 和 \(\Lambda\)-independent contractive norm 均为 FALSE。</p>
            <p><strong>结论边界：</strong>&nbsp;low-gap physical row、BlochUniformPhysicalVelocityDirectSum、nonlinearNavierStokes 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-72z.html"><strong>阅读 R0.72Z 研究笔记 →</strong></a><br><a href="/notes/r0-72z.pdf">下载同步研究笔记 PDF</a> · <a href="/assets/r072z/fig-r072z-os-squire-threshold.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072z">查看确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072z_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-72z.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73A：</strong>&nbsp;projected low-gap OS propagator with an explicit transient prefactor。</p>
          </div>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R072Y_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72Y: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError("R0.72Z source-stage manifest contract is missing, stale, or has extra fields")


def preflight_release_state() -> None:
    release = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    expected_site = {"schemaVersion": "research-site-version-v1", "version": "1.38", "latestRelease": "R0.72Y", "publicHtmlNoteCount": 175, "publishedDate": "2026-08-28"}
    if json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8")) != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.72Y")
    if len(list((PUBLIC / "notes").glob("*.html"))) != 175:
        raise RuntimeError("R0.72Y preflight expected 175 public HTML notes")
    for relative in ("notes/r0-72z.html", "notes/r0-72z.pdf", "recap-r0-61-r0-72z.html", "recap-r0-61-r0-72z.pdf"):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.72Y preflight found premature public output: {relative}")
    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in ('data-site-version="1.38"', "<strong>175</strong>公开研究笔记", "<strong>R0.72Y</strong>最新研究节点", 'aria-label="R0.69P–R0.72Y"'):
        if token not in home:
            raise RuntimeError(f"R0.72Y home baseline missing token: {token}")
    if 'data-release="r072z"' in home:
        raise RuntimeError("R0.72Y home already contains an R0.72Z card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72Y">(.*?)</nav>', home, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 85:
        raise RuntimeError("R0.72Y home route expected 85 notes")
    recap = (PUBLIC / "recap-r0-61-r0-72y.html").read_text(encoding="utf-8")
    start, end = recap.index('<section id="node-index">'), recap.index("</section>", recap.index('<section id="node-index">'))
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 115 or len(set(links)) != 115 or recap.count('<article class="phase">') != 34:
        raise RuntimeError("R0.72Y recap baseline expected 115 unique nodes and 34 phases")
    inventory = json.loads((ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r072y", 77, 53, 24):
        raise RuntimeError("formal archive inventory is not at R0.72Y")


def _binding_paths(manifest: dict) -> set[str]:
    bindings = manifest.get("sourceBindings")
    if not isinstance(bindings, list):
        raise RuntimeError("formal certificate sourceBindings are missing")
    paths = {row.get("path") for row in bindings if isinstance(row, dict)}
    if None in paths or len(paths) != len(bindings):
        raise RuntimeError("formal certificate sourceBindings are malformed or duplicated")
    return paths


def validate_inputs() -> None:
    required_inputs = (
        "research/r072z_report-source.md", "research/r072z_literature_audit.md", "research/r072z_gap_matrix.md", "research/r072z_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md", f"{CERTIFICATE_RELATIVE}/crosscheck.json", f"{CERTIFICATE_RELATIVE}/manifest.json", f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72y.html", "public/recap-r0-61-r0-72y.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72Z release input: {relative}")
    report = (ROOT / "research/r072z_report-source.md").read_text(encoding="utf-8")
    for token in (
        "exactOSFeedbackCommutatorIdentity", "signedRelativeFormOSAbsorption", "highGapOSPrefactorOneDecay", "highModeOSGapExponentSharpness",
        "exactGaplessOSTangentMode", "exactSquireDuhamel", "orientationUniformWithLambdaPayment", "fixedRowOSSquireGraphRegularity",
        "allStrongRowsOSPrefactorOneContraction", "rawOrientationUniformFromCOnly", "lowGapOSTransientA2Propagator", "nonlinearNavierStokes", "Clay",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72Z report missing stable token: {token}")
    audit = (ROOT / "research/r072z_independent_audit.md").read_text(encoding="utf-8")
    for token in ("PASS", "pressure commutator and sign", "high-gap exponent", "exact Squire induced norm", "low-gap"):
        if token not in audit:
            raise RuntimeError(f"R0.72Z independent audit missing token: {token}")
    certificate, figure = ROOT / CERTIFICATE_RELATIVE, ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72Z certificate")
    verify_flat_hash_ledger(figure, "R0.72Z figure")
    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    source_commit = str(certificate_manifest.get("sourceCommit", ""))
    if certificate_manifest.get("status") != "formal" or not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("R0.72Z certificate is not formal or source-frozen")
    if crosscheck.get("status") != "passed" or crosscheck.get("formalSourceReady") is not True or crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("R0.72Z certificate crosscheck is not formal")
    if crosscheck.get("sourceCommit") != source_commit or crosscheck.get("sourceBindings") != certificate_manifest.get("sourceBindings") or not all(crosscheck.get("checks", {}).values()):
        raise RuntimeError("R0.72Z certificate lineage or exhaustive checks failed")
    expected_bound_sources = {
        "research/r072z_report-source.md", "research/r072z_gap_matrix.md", "research/r072z_literature_audit.md", "research/r072z_independent_audit.md",
        "research/certificates/r072z/generate_certificate.py", "research/certificates/r072z/independent_recompute.py", "research/certificates/r072z/validate_certificate.py",
        "scripts/generate_r072z_release.py", "scripts/add-r072z-translations.mjs", "tests/r072z-os-squire-gate.test.mjs", "tests/r072z-release.test.mjs",
        "tests/r072z-deterministic-certificate-source.test.mjs", "tests/r072z-os-squire-figure-source.test.mjs",
        f"{FIGURE_RELATIVE}/contract.json", f"{FIGURE_RELATIVE}/config.json", f"{FIGURE_RELATIVE}/caption.md", f"{FIGURE_RELATIVE}/README.md",
    }
    missing_bindings = expected_bound_sources - _binding_paths(certificate_manifest)
    if missing_bindings:
        raise RuntimeError(f"R0.72Z formal source binding is incomplete: {sorted(missing_bindings)}")
    subprocess.run([sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"], cwd=ROOT, check=True)
    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("release") != "R0.72Z" or manifest.get("figureId") != FIGURE_ID:
        raise RuntimeError("R0.72Z figure identity mismatch")
    if manifest.get("status") != "formal" or manifest.get("qa", {}).get("status") != "passed" or manifest.get("qa", {}).get("visualInspectionExplicit") is not True:
        raise RuntimeError("R0.72Z figure is not formally validated")
    git = manifest.get("git", {})
    certificate_commit = str(git.get("certificateCommit", ""))
    if git.get("sourceCommit") != source_commit or not re.fullmatch(r"[0-9a-f]{40}", certificate_commit) or certificate_commit == source_commit:
        raise RuntimeError("R0.72Z figure does not preserve two-commit lineage")
    claims = manifest.get("claimBoundary", {})
    expected_claims = {
        "signedRelativeFormOSAbsorptionClosedInBoundReport": True,
        "highGapOSPrefactorOneDecayClosedInBoundReport": True,
        "alphaMinusTwoOSGapSufficiencyClosedInBoundReport": True,
        "highModeOSGapExponentSharpnessClosedInBoundReport": True,
        "exactGaplessOSTangentModeClosedInBoundReport": True,
        "exactKineticOrientationNormalizationClosedInBoundReport": True,
        "orientationUniformWithLambdaPaymentClosedInBoundReport": True,
        "strongKernelConditionalSquireTransferClosedInBoundReport": True,
        "allStrongRowsOSPrefactorOneContraction": False,
        "abstractGaplessOSA2StrictContraction": False,
        "lambdaIndependentSquireTransfer": False,
        "lowGapOSTransientA2Propagator": False,
        "BlochUniformPhysicalVelocityDirectSum": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
        "figureIsAnalyticProof": False,
        "figureContainsPDESimulation": False,
        "exponentsAreFitted": False,
    }
    if claims != expected_claims:
        raise RuntimeError("R0.72Z figure claim boundary is not exact")
    subprocess.run([sys.executable, str(figure / "validate.py"), "--require-formal"], cwd=ROOT, check=True)
    if manifest.get("publication", {}).get("directory") != "public/assets/r072z":
        raise RuntimeError("R0.72Z figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master, public = figure / f"figure.{suffix}", PUBLIC / "assets/r072z" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72Z public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72y.html").read_text(encoding="utf-8")
    replacements = (
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72Z：Orr--Sommerfeld 压力反馈的 signed high-gap threshold 与 orientation-paid Squire history。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72Z｜OS pressure threshold and orientation-paid Squire transfer">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="high-gap q graph 为 CLOSED；low-gap physical row、nonlinear Navier--Stokes 与 Clay 保持 OPEN。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072z/fig-r072z-os-squire-threshold.png">'),
        (r'<title>.*?</title>', '<title>R0.72Z｜OS pressure threshold and orientation-paid Squire transfer</title>'),
    )
    for index, (pattern, value) in enumerate(replacements):
        html = section(html, pattern, value, f"Z note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.38", "/i18n-en.js?v=1.39", "Z note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#form">pressure form</a><a href="#threshold">阈值</a><a href="#power">power</a><a href="#forcing">forcing</a><a href="#counter">反例</a><a href="#tangent">tangent</a><a href="#collision">collision</a><a href="#squire">Squire</a><a href="#orientation">方向</a><a href="#optimal">最优常数</a><a href="#kernel">kernel</a><a href="#rates">rates</a><a href="#graph">graph</a><a href="#literature">文献</a><a href="#evidence">证据</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "Z note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "Z note hero")
    toc_items = [("result", "00 · direct decision"), ("form", "01 · exact pressure form"), ("threshold", "02 · signed threshold"), ("power", "03 · high-gap power"), ("forcing", "04 · forced graph"), ("counter", "05 · obstruction"), ("tangent", "06 · tangent mode"), ("collision", "07 · collision scaling"), ("squire", "08 · Squire history"), ("orientation", "09 · orientation"), ("optimal", "10 · exact coefficient"), ("kernel", "11 · strong kernel"), ("rates", "12 · damping rates"), ("graph", "13 · fixed-row graph"), ("literature", "14 · literature"), ("evidence", "15 · evidence"), ("figure", "16 · journal figure"), ("value", "17 · value"), ("next", "18 · R0.73A"), ("reproduce", "19 · reproduction")]
    toc = '      <aside class="toc"><strong>CONTENTS</strong><ol>\n' + "".join(f'        <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_items) + '\n      </ol></aside>'
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "Z note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "Z note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72Z · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "Z note footer")
    assert_clean(html, "R0.72Z note")
    assert_mathjax_clean(html, "R0.72Z note")
    (PUBLIC / "notes/r0-72z.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72y.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.38", "/i18n-en.js?v=1.39", "Z recap i18n")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72Z 的 116 个节点；最新一节闭合 high-gap OS graph 与 orientation-paid Squire history。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72Z｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十五个阶段、116 个节点：从约化递推到 signed high-gap OS 与 Squire orientation boundary。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.72Z｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "Z recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72Z · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页完整保留 R0.61 到 R0.72Z 的 116 个研究节点。R0.69P 以后的路线从局部证书推进到 scalar A2 collision path，再回到完整 Fourier row；R0.72Z 进一步闭合 signed high-gap OS \(q\)-graph 和 orientation-paid Squire history。low-gap physical row、nonlinear Navier--Stokes 与 Clay 都没有被外推。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72Z</strong><p>收录节点：116</p><p>回顾截止时公开笔记：176</p><p>回顾截止节点：R0.72Z</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "Z recap hero")
    for old, new in (("02 · 115 节完整索引", "02 · 116 节完整索引"), ("01 · 三十四个研究阶段", "01 · 三十五个研究阶段"), ("R0.60 之后的路线分成三十四个阶段", "R0.60 之后的路线分成三十五个阶段")):
        html = required(html, old, new, "Z recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>116</strong><span>R0.61–R0.72Z 研究节点</span></div><div class="metric"><strong>78</strong><span>R0.70A–R0.72Z 已公开版本</span></div><div class="metric"><strong>54</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.72Z 的 78 个版本已公开，其中 54 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "Z recap result")
    new_phase = r'''            <article class="phase"><h3>R0.72Z · signed high-gap OS and orientation-paid Squire history</h3><p>exact OS pressure form、signed high-gap prefactor-one \(q\)-decay、forced graph ledger、exact Squire Duhamel 与 orientation payment 均为 CLOSED。</p><p>all-row prefactor-one contraction、raw \(c\)-only orientation uniformity 与 \(\Lambda\)-independent contractive norm 为 FALSE；exact tangent mode 解释 low-gap collision 中的慢方向。</p><p>lowGapOSTransientA2Propagator、BlochUniformPhysicalVelocityDirectSum、nonlinearNavierStokes 与 Clay 保持 OPEN。</p><div class="links"><a href="/notes/r0-72z.html">R0.72Z</a><a href="/assets/r072z/fig-r072z-os-squire-threshold.pdf">R0.72Z 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072z">R0.72Z 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", new_phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "Z recap phase")
    html = required(html, "R0.61–R0.72Y 的 115 节公开笔记", "R0.61–R0.72Z 的 116 节公开笔记", "Z recap node title")
    node_y = '            <span class="node-ref"><a href="/notes/r0-72y.html">R0.72Y</a><span class="node-state kind-closed">闭</span></span>\n'
    node_z = '            <span class="node-ref"><a href="/notes/r0-72z.html">R0.72Z</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_y, node_y + node_z, "Z recap node")
    retained = '            <li>R0.72Z 闭合 signed high-gap OS graph 与 orientation-paid Squire history，同时把 low-gap physical row 明确保留为 OPEN。</li>\n'
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "Z recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>high-gap pressure absorption 已闭合，但没有成为 low-gap physical theorem</h2><p>不能把 116 个节点或 78 个公开版本解释成 Clay 问题完成比例。R0.72Z 的严格增量是 signed OS threshold、sharp negative witnesses、exact tangent mode 与 orientation-paid Squire history；直接 Clay 价值仍低。</p></section>''', "Z recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73A 研究投影后的 low-gap OS propagator</h2><p>分离 tangent/lift-up 慢子空间，寻求带显式 transient prefactor 的 limiting-absorption 或 evolution estimate。</p></section>''', "Z recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72Z 的 78 节已公开；54 节完整封存；24 节旧档待回补。</p><p>allStrongRowsOSPrefactorOneContraction、rawOrientationUniformFromCOnly 与 epsilonOnlySquireTransfer 为 FALSE；lowGapOSTransientA2Propagator、unconditionalStrongFullRowA2Estimate、nonlinearNavierStokes 与 Clay 为 OPEN。</p></section>''', "Z recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72y.html">保留 R0.72Y 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72z.html">打开最新节点 R0.72Z</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072z">查看 R0.72Z 确定性证书</a> · <a href="/assets/r072z/fig-r072z-os-squire-threshold.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72z.pdf">下载同步 PDF</a></p><p>完整节点索引保留 R0.61 起的全部历史编号；状态标签只描述证据类型。</p></section>''', "Z recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72Z 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "Z recap footer")
    start, end = html.index('<section id="node-index">'), html.index("</section>", html.index('<section id="node-index">'))
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 116 or len(set(links)) != 116 or html.count('<article class="phase">') != 35:
        raise RuntimeError("R0.72Z recap expected 116 unique nodes and 35 phases")
    assert_clean(html, "R0.72Z recap")
    assert_mathjax_clean(html, "R0.72Z recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72z.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.38"', 'data-site-version="1.39"'), ("/i18n-en.js?v=1.38", "/i18n-en.js?v=1.39"), ("/site-refresh.js?v=1.38", "/site-refresh.js?v=1.39"),
        ("<strong>v1.38</strong>网页版本", "<strong>v1.39</strong>网页版本"), ("<strong>175</strong>公开研究笔记", "<strong>176</strong>公开研究笔记"), ("<strong>R0.72Y</strong>最新研究节点", "<strong>R0.72Z</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72Y", "Research topology · R0.1–R0.72Z"), ("R0.70A–R0.72Y：77 节已公开，53 节完整封存", "R0.70A–R0.72Z：78 节已公开，54 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72Y</span>', '<span class="route-range">R0.69P–R0.72Z</span>'), ('aria-label="R0.69P–R0.72Y"', 'aria-label="R0.69P–R0.72Z"'),
        ("展开 85 篇公开笔记", "展开 86 篇公开笔记"), ("本站 R0.69P–R0.72Y 路线", "本站 R0.69P–R0.72Z 路线"),
        ("综述 v1.38 · 2026-08-28", "综述 v1.39 · 2026-08-28"), ("上次综述 v1.37 · 2026-08-28", "上次综述 v1.38 · 2026-08-28"),
        ("/recap-r0-61-r0-72y.html", "/recap-r0-61-r0-72z.html"), ("/recap-r0-61-r0-72y.pdf", "/recap-r0-61-r0-72z.pdf"),
    ):
        html = required(html, old, new, "Z home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72Z 已闭合 signed high-gap OS q-graph 与 orientation-paid Squire history。下一关是分离 tangent/lift-up 子空间，寻找带 transient prefactor 的 low-gap OS propagator。</span></div>', "Z home focus")
    link_y = '<a class="milestone" href="/notes/r0-72y.html">R0.72Y</a>'
    html = once(html, link_y, link_y + '\n                  <a class="milestone" href="/notes/r0-72z.html">R0.72Z</a>', "Z home route link")
    route_z = r'''              <p>R0.72Z 把 active OS pressure 写成 exact signed relative form，在 high-gap \(q\)-graph 上闭合 prefactor-one decay 与 forcing；Squire transfer 按 orientation、\(\Lambda\) payment 与 causal history 闭合。all-row prefactor-one contraction 为 FALSE；low-gap physical row 与 nonlinear/Clay 仍为 OPEN。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_z + '              <details class="tree-notes" open>', "Z home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "Z home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.72Z · 2026-08-28</p><h3>R0.60 recap 之后的累计回顾收录 116 个节点；全站现有 176 篇公开研究笔记</h3><p>累计回顾现分三十五个问题阶段，并给出 R0.61–R0.72Z 的完整索引；R0.72Z 分开记录 high-gap OS closure、negative witnesses 与 Squire orientation payment。</p><p>R0.70A–R0.72Z 共 78 个版本已公开；54 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;signed high-gap \(q\)-graph 已闭合；low-gap physical row 与 nonlinear/Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-72z.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72z.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "Z home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_Z_CARD + '\n        </section>\n\n      </article>', "Z home card")
    if html.count('data-release="r072z"') != 1:
        raise RuntimeError("home must contain exactly one R0.72Z card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72Z">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 86:
        raise RuntimeError("home current-route index must contain 86 note links")
    assert_clean(html, "R0.72Z home")
    assert_mathjax_clean(html, "R0.72Z home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.38", "/i18n-en.js?v=1.39"), ("本站 R0.69P–R0.72Y 只列为研究笔记", "本站 R0.69P–R0.72Z 只列为研究笔记"),
        ("/recap-r0-61-r0-72y.html", "/recap-r0-61-r0-72z.html"), ("文献综述 v1.38 · 2026-08-28", "文献综述 v1.39 · 2026-08-28"),
        ("累计回顾与 115 节索引", "累计回顾与 116 节索引"), ("打开 115 节完整索引", "打开 116 节完整索引"),
    ):
        html = required(html, old, new, "Z literature " + old)
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.72Z</b><strong>OS pressure absorption and orientation-dependent Squire transfer</strong></header><p>直接研究 \(q\to\eta\) 三角系统，按 orientation ratio、damping gap 与 exceptional rows 分区，并保留 lift-up transient prefactor。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.72Z</b><strong>signed high-gap OS and orientation-paid Squire history</strong></header><p>exact pressure form、high-gap prefactor-one \(q\)-graph、sharp negative witnesses 与 orientation-paid Squire history 已闭合。low-gap physical row 仍 OPEN。<a href="/notes/r0-72z.html">研究笔记</a> <a href="/recap-r0-61-r0-72z.html">当前累计回顾</a> <a href="#r072z-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73A</b><strong>projected low-gap OS propagator</strong></header><p>分离 tangent/lift-up 慢子空间，寻求带 explicit transient prefactor 的 low-gap limiting absorption 或 evolution estimate。</p></div>'''
    html = once(html, old_open, new_steps, "Z literature route")
    boundary = r'''

          <h3 id="r072z-boundary">R0.72Z 的 OS--Squire 先例与 collision 边界</h3>
          <p>Jia、Beekie--Chen--Jia 与 Ding--Lin 给出 fixed spectral/critical geometry 下的 active Orr--Sommerfeld pressure 方法；Li--Wei--Zhang 与 Jerome--Chomaz 固定三维 Squire orientation 与 lift-up 的结构代价。现有核验没有把这些结果与本项目的 time-dependent critical-point collision、Bloch rows 和 physical direct sum 同时结合。我只报告 bounded primary-source search；它不是新颖性或优先权证明。</p>
          <div class="boundary"><strong>R0.72Z 的主张边界</strong><p>signed high-gap OS \(q\)-graph、forced ledger、exact tangent witness 与 orientation-paid Squire history 为 CLOSED。allStrongRowsOSPrefactorOneContraction、rawOrientationUniformFromCOnly 与 epsilonOnlySquireTransfer 为 FALSE。lowGapOSTransientA2Propagator、unconditionalStrongFullRowA2Estimate、BlochUniformPhysicalVelocityDirectSum、nonlinearNavierStokes 与 Clay 为 OPEN。</p></div>'''
    match = re.search(r'(<h3 id="r072y-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("Z literature expected R0.72Y boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "Z literature boundary")
    assert_clean(html, "R0.72Z literature")
    assert_mathjax_clean(html, "R0.72Z literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    if len(list((PUBLIC / "notes").glob("*.html"))) != 176:
        raise RuntimeError("expected 176 public HTML notes after R0.72Z")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r072z", "siteVersion": "1.39", "publicHtmlNoteCount": 176, "postR060RecapNodeCount": 116,
        "nextRelease": "r073a", "latestReleaseGate": "tests/r072z-os-squire-gate.test.mjs", "latestReleasePublicationTest": "tests/r072z-release.test.mjs",
        "postR070APublishedReleaseCount": 78, "postR070AFormalSealedReleaseCount": 54, "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.38", "R0.72Y", 175):
        raise RuntimeError("site-version is not at R0.72Y")
    site.update({"version": "1.39", "latestRelease": "R0.72Z", "publicHtmlNoteCount": 176, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r072y", 77, 53, 24):
        raise RuntimeError("formal archive inventory is not at R0.72Y")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072y" or "r072z" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72Y")
        inventory[key].append("r072z")
    inventory.update({"latestPublishedRelease": "r072z", "publishedReleaseCount": 78, "formalSealedReleaseCount": 54, "legacyFormalFigureBacklogCount": 24})
    if len(inventory["publishedReleases"]) != 78 or len(inventory["formalSealedReleases"]) != 54:
        raise RuntimeError("formal archive count mismatch after R0.72Z")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "VERSION").write_text("1.39\n", encoding="utf-8")


def main() -> None:
    preflight_release_state()
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-72z.html", "recap-r0-61-r0-72z.html"):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.72Z", "siteVersion": "1.39", "notes": 176, "recapNodes": 116,
        "published": 78, "formalSealed": 54, "legacyBacklog": 24, "phases": 35, "routeNotes": 86, "next": "R0.73A",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
