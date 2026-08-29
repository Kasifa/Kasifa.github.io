#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed R0.73B Bloch/kinetic release.

R0.73B closes an exact zero-lattice Bloch cancellation and a complete
linearized physical-velocity finite-transient estimate at the viscous row
rate. It does not prove an A2 direct sum, a sharp large-|Lambda| law, a
nonlinear estimate, or the Clay problem.
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


ROOT = Path(os.environ.get("R073B_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r073b-bloch-kinetic-transient"
FIGURE_RELATIVE = f"figures/r073b/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073b"
EXPERIMENT_RELATIVE = "experiments/r073b"

R073A_RELEASE_BASELINE = {
    "latestCompletedRelease": "r073a",
    "siteVersion": "1.40",
    "publicHtmlNoteCount": 177,
    "postR060RecapNodeCount": 117,
    "nextRelease": "r073b",
    "latestReleaseGate": "tests/r073a-hidden-mean-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r073a-release.test.mjs",
    "postR070APublishedReleaseCount": 79,
    "postR070AFormalSealedReleaseCount": 55,
    "legacyFormalFigureBacklogCount": 24,
}

SOURCE_STAGE_CONTRACT = {
    "release": "r073b",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r073b_report-source.md",
    "problemFreeze": "research/r073b_problem_freeze.md",
    "literatureAudit": "research/r073b_literature_audit.md",
    "gapMatrix": "research/r073b_gap_matrix.md",
    "analyticProof": "research/r073b_kinetic_form_proof.md",
    "independentAudit": "research/r073b_independent_analytic_audit.md",
    "independentAnalyticAudit": "research/r073b_independent_analytic_audit.md",
    "producer": "research/certificates/r073b/generate_certificate.py",
    "independentProducer": "research/certificates/r073b/independent_recompute.py",
    "comparator": "research/certificates/r073b/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "experimentDirectory": EXPERIMENT_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r073b_release.py",
    "translationScript": "scripts/add-r073b-translations.mjs",
    "translationSnapshot": "scripts/i18n-snapshots/r073b-missing.json",
    "releaseGate": "tests/r073b-bloch-kinetic-gate.test.mjs",
    "publicationTest": "tests/r073b-release.test.mjs",
    "certificateSourceTest": "tests/r073b-deterministic-certificate-source.test.mjs",
    "figureSourceTest": "tests/r073b-bloch-kinetic-transient-figure-source.test.mjs",
}

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73B · BLOCH CARRIER · PHYSICAL KINETIC ENERGY</div>
        <h1>我把近零 Bloch 载波的奇性压成方向因子，<br>并闭合完整线性速度行的有限瞬态界</h1>
        <p class="lead">zero-lattice Bloch carrier 的精确抵消把耦合侧的 \(g^{-1}\) 化为 \(\omega=2\gamma\beta/g\)，满足 \(|\omega|\le1\)。更重要的是，primitive velocity kinetic energy 直接覆盖 Orr--Sommerfeld、Squire 与 exceptional rows，并在 viscous row rate 上无行数损失地求和。A2、sharp \(|\Lambda|\) law、nonlinear 与 Clay 仍为 OPEN。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73B scoped linear theorem 完成</span><strong>Bloch cancellation and kinetic transient</strong><p>版本 v0.73B · 2026-08-29</p><p>Bloch carrier cancellation: CLOSED</p><p>physical kinetic direct sum: CLOSED</p><p>fixed-c low-gap uniformity: FALSE</p><p>prefactor-one contraction: FALSE</p><p>A2 / sharp Lambda law: OPEN</p><p>nonlinear / Clay: OPEN</p></div>
    </div></header>'''

# The public mathematical text decodes to \(0<g\le1\); raw HTML uses
# ``&lt;`` below so the i18n extractor cannot misread ``<g`` as a tag.
NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>完整线性速度系统在黏性行速率上有有限瞬态；这不是 enhanced-dissipation 或 nonlinear theorem</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · EXACT BLOCH ALGEBRA</strong><p>exactBlochNearCarrierCancellation=CLOSED；exactBlochCarrierSystem=CLOSED；boundedBlochOrientationCoefficient=CLOSED；blochNearCarrierFiniteTransient=CLOSED。</p></div><div class="verdict-card true"><strong>CLOSED · COMPLETE LINEAR KINETIC ROW</strong><p>exactHeatShearGradientPrimitive=CLOSED；completePhysicalKineticFiniteTransient=CLOSED；completeOSSquireKineticFiniteTransient=CLOSED；blochUniformPhysicalVelocityDirectSumAtViscousRates=CLOSED；physicalKineticForcedDuhamel=CLOSED。</p></div><div class="verdict-card false"><strong>FALSE · UNIFORMITY CLAIMS</strong><p>lambdaIndependentKineticPrefactor=FALSE；fixedCUniformLowGapKineticPropagator=FALSE；allRowPrefactorOneKineticContraction=FALSE。fixed \(c\ne0\) 对应 \(|\Lambda|=|c|/\sqrt\mu\to\infty\)，不能与 fixed \(\Lambda\) 混写。</p></div><div class="verdict-card false"><strong>OPEN · STRONGER TARGETS</strong><p>polynomiallySharpLambdaKineticPrefactor=OPEN；completeOSSquireA2DirectSum=OPEN；transportedAdjointPressureA2Modulation=OPEN；nonlinearNavierStokes=OPEN；Clay=OPEN。</p></div></div></section>
        <section id="bloch"><div class="section-no">01 / Bloch carrier</div><h2>零格点载波是精确坐标；端点处不是唯一最低模</h2><div class="equation result">\[h=\Pi_0(\mathcal L^{-1}q),\qquad r=Q_0q,\qquad q=gh+r,\quad g=\beta^2+\xi^2+\gamma^2.\]</div><p>我在半开 Bloch cell \([-1/2,1/2)\) 上选 zero-lattice carrier。包含端点 \(\beta=-1/2\) 有最低特征值重数二，所以只声明 selected carrier，不声明 unique slow mode。</p></section>
        <section id="cancellation"><div class="section-no">02 / Exact cancellation</div><h2>两次周期分部积分把 raw inverse gap 化为物理方向</h2><div class="equation result">\[\boxed{\Pi_0(Wr+W_{xx}\mathcal L^{-1}r)=g\Pi_0(W\mathcal L^{-1}r)+2i\beta\Pi_0(W_x\mathcal L^{-1}r).}\]</div><div class="equation result">\[\frac{2c\beta}{g}=\Lambda\frac{2\gamma\beta}{\beta^2+\xi^2+\gamma^2},\qquad \left|\frac{2c\beta}{g}\right|\le|\Lambda|.\]</div><p>抵消只正则化 homogeneous coupling；受迫均值仍支付 \(g^{-1}\Pi_0F_q\)。</p></section>
        <section id="hybrid"><div class="section-no">03 / Hybrid transient</div><h2>\(X_g\) 中得到全起点、有限瞬态的黏性速率界</h2><div class="equation result">\[\|U(d,s)\|_{X_g}\le\exp\{-g(d-s)+|c|J_c(s,d)+|\Lambda|J_\Lambda(s,d)\}.\]</div><p>\(J_c\) 与 \(J_\Lambda\) 都由 \(e^{-d}\)、\(e^{-4d}\) 显式积分，因而在整个 heat path 上有限。该 homogeneous \(X_g\) theorem 明确要求 \(F_q=0\)、\(\mu>0\)、\(0&lt;g\le1\)；它不外推成 kinetic norm 的 \(A_2\) 速率。</p></section>
        <section id="energy"><div class="section-no">04 / Primitive kinetic identity</div><h2>完整 divergence-free velocity 行直接给出统一能量账本</h2><div class="equation result">\[\frac12\frac d{dd}\|u\|_2^2+\|A_\beta u\|_2^2+\mu\|u\|_2^2=-\Lambda\operatorname{Re}\langle W_xv,u_3\rangle+\operatorname{Re}\langle F,u\rangle.\]</div><p>primitive components 覆盖 \(\mu=0\) 的 exceptional rows；当 \(\mu>0\) 时它与 exact Orr--Sommerfeld--Squire kinetic identity 一致。</p></section>
        <section id="primitive"><div class="section-no">05 / Heat primitive</div><h2>剪切梯度沿热路径可积，而且常数精确</h2><div class="equation result">\[\|W_x(d)\|_\infty=\frac12(e^{-d}+e^{-4d}),\quad K(s,d)=\frac12(e^{-s}-e^{-d})+\frac18(e^{-4s}-e^{-4d}).\]</div><p>等号在 \(x=\pi\) 取得；因此 \(K(0,\infty)=5/8\)。</p></section>
        <section id="propagator"><div class="section-no">06 / Complete row propagator</div><h2>每一行都保留自己的黏性衰减，并只支付共同 transient</h2><div class="equation result">\[\boxed{\|U_j(d,s)\|_{L^2_u\to L^2_u}\le\exp[-g_j(d-s)+\tfrac{|\Lambda|}{2}K(s,d)].}\]</div><div class="equation result">\[\|U(d,s)\|_{L^2_\sigma\to L^2_\sigma}\le e^{|\Lambda|K(s,d)/2}\le e^{5|\Lambda|e^{-s}/16}.\]</div><p>离散 Fourier rows 用有限部分和与单调收敛求和；连续 Bloch 参数用 orthogonal direct integral。没有 row-count factor。</p></section>
        <section id="forcing"><div class="section-no">07 / Forced Duhamel</div><h2>投影后的物理 forcing 使用同一 kernel</h2><div class="equation result">\[\|u_j(d)\|\le G_j(d,s)\|u_j(s)\|+\int_s^dG_j(d,\tau)\|F_j(\tau)\|\,d\tau.\]</div><p>结论要求 \(F_j\in L^1_{\rm loc}L^2\)，先对 smooth divergence-free data 证明，再由密度传到 mild solutions。</p></section>
        <section id="ossquire"><div class="section-no">08 / OS--Squire metric</div><h2>正横向间隙时，完整 kinetic metric 精确分解</h2><div class="equation result">\[\|u\|_2^2=\mu^{-1}\bigl(\|\mathcal L^{-1/2}q\|_2^2+\|\eta\|_2^2\bigr).\]</div><p>这表明 Squire 不是被删除，而是已包含在物理速度能量中；它仍没有得到 complete \(A_2\) direct-sum rate。</p></section>
        <section id="sharp"><div class="section-no">09 / Sharp shear form</div><h2>二维物理行的最佳 instantaneous shear coefficient 有精确低间隙极限</h2><div class="equation result">\[\rho_\mu=\sqrt\mu\|\mathcal L_\mu^{-1/2}S\mathcal L_\mu^{-1/2}\|,\quad S=-i(W_x\partial_x+\tfrac12W_{xx}).\]</div><div class="equation result">\[\boxed{\rho_\mu(d)\to\tfrac12\|W_x(d)\|_2=\frac{\sqrt{e^{-2d}+e^{-8d}}}{4\sqrt2}.}\]</div><p>integrated low-gap coefficient 为 \(0.188106027072\ldots\)，小于 elementary all-row coefficient \(5/16\)。它是 logarithmic-norm limit，不是 exact maximum transient gain。</p></section>
        <section id="growth"><div class="section-no">10 / Instantaneous growth witness</div><h2>载波—切向二维试验平面排除 prefactor-one contraction</h2><div class="equation result">\[\lambda_{\rm trial}>0\quad\Longleftrightarrow\quad \Lambda^2A^2>4\mu B.\]</div><p>对每个 fixed nonzero \(\Lambda\)，充分小的 \(\mu\) 都出现严格 instantaneous kinetic growth。这个 witness 由两个方向组成，不应误称为只含两个 Fourier modes。</p></section>
        <section id="liftup"><div class="section-no">11 / Exact lift-up lower bound</div><h2>\(\Lambda\)-independent transient prefactor 被显式解排除</h2><div class="equation result">\[\frac{\|u(d)\|^2}{\|u(s)\|^2}=1+\frac{\Lambda^2(d-s)^2}{8}(e^{-2d}+e^{-8d}).\]</div><p>这只否定 \(\Lambda\)-independent prefactor，不否定本节的 \(e^{C|\Lambda|}\) upper bound，也没有给出 sharp 大参数阶。</p></section>
        <section id="fixedc"><div class="section-no">12 / Parameter path</div><h2>fixed \(\Lambda\) 与 fixed \(c\) 是不同的低间隙命题</h2><p>fixed bounded \(\Lambda\) 时，physical kinetic propagator 在 \(\mu\downarrow0\) 保持有限。fixed nonzero \(c\) 时，\(\Lambda=c/\sqrt\mu\)，由 regular-system continuity 与非零低模投影得到至少 \(C\mu^{-1/2}\) 的 kinetic growth。因此 fixedCUniformLowGapKineticPropagator=FALSE。</p></section>
        <section id="finite"><div class="section-no">13 / Finite diagnostic</div><h2>有限矩阵验证参数路径与权重阈值，但不承担无限维证明</h2><p>deterministic screen 包含 280 propagators、1960 primary norm rows 与 245 targeted rows。它复核 generator similarity、步长和模数收敛、符号对称、kinetic upper bound 与 fixed-\(\Lambda\) triangular limit。没有 Galerkin tail enclosure，也没有 nonlinear convolution。</p></section>
        <section id="literature"><div class="section-no">14 / Literature boundary</div><h2>已有 OS--Squire、lift-up、Riesz projection 与 nonautonomous propagator 工具；本节只报告组合接口</h2><p>Colombo--Dolce--Montalto--Ventura、Jerome--Chomaz、Bedrossian--Germain--Masmoudi、Li--Wei--Zhang、Li--Zhao、Wei--Zhang--Zhao 与 Bedrossian--Coti Zelati 分别覆盖相邻工具。bounded primary-source search 没有发现同一来源同时处理本项目的双谐波 heat path、near carrier、physical velocity、Squire 与 Bloch direct sum；这不是 novelty 或 priority proof。</p></section>
        <section id="evidence"><div class="section-no">15 / Evidence boundary</div><h2>解析证明、确定性证书、有限 screen 与附图分工明确</h2><p>无限维结论由 energy identity、operator-norm tail bound、Gronwall 与 direct-sum argument 承担。证书复核精确代数和绑定的 finite rows；附图展示已审计公式和有限诊断，不构成证明。</p></section>
        <section id="figure"><div class="section-no">16 / Journal figure</div><h2>Bloch 抵消、kinetic envelope、sharp coefficient 与参数路径分面展示</h2><p><img src="/assets/r073b/fig-r073b-bloch-kinetic-transient.svg" alt="R0.73B Bloch cancellation and physical kinetic finite-transient audit"></p><p><a href="/assets/r073b/fig-r073b-bloch-kinetic-transient.pdf">下载 PDF</a> · <a href="/assets/r073b/fig-r073b-bloch-kinetic-transient.png">下载 PNG</a> · <a href="/assets/r073b/fig-r073b-bloch-kinetic-transient.svg">打开 SVG</a></p></section>
        <section id="value"><div class="section-no">17 / Research value</div><h2>这是 complete linearized viscous-rate closure，不是 Millennium problem 的直接解</h2><p>严格增量是：near-carrier inverse gap 被物理方向吸收；完整 velocity/Squire rows 获得可求和的有限 transient；fixed-\(c\) singular path 与 fixed-\(\Lambda\) path 被分开。A2-scale pressure modulation、nonlinear frequency transfer、vortex stretching 和 continuation criterion 都未闭合。</p></section>
        <section id="next"><div class="section-no">18 / Next gate</div><h2>R0.73C：先确定大 \(|\Lambda|\) transient 的 sharp 量级</h2><p>下一节比较 exact lift-up lower bound、triangular low-gap limit 与可构造的 polynomial upper mechanism；只有在 \(|\Lambda|\) 依赖清楚后，才尝试 complete OS--Squire \(A_2\) direct sum。</p></section>
        <section id="reproduce"><div class="section-no">19 / Reproduction</div><h2>完整报告、独立审计、证书、实验和正式附图</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073b_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073b_kinetic_form_proof.md">kinetic shear-form proof</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073b_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073b_literature_audit.md">文献边界审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073b">确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073b">有限诊断</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073b/fig-r073b-bloch-kinetic-transient">正式附图包</a> · <a href="/notes/r0-73b.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73b.html">累计回顾</a> · <a href="/recap-r0-61-r0-73b.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73C</span><span class="tree-state current">下一检查点</span></div>
              <h3>sharp large-Lambda transient law</h3><p>比较 exact lift-up lower bound、low-gap triangular limit 与 polynomial upper mechanism，先确定 \(|\Lambda|\) 依赖，再进入 complete OS--Squire A2 direct sum。</p>
            </article>'''

HOME_B_CARD = r'''          <div class="task-one" id="r073b" data-release="r073b" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73B · 2026-08-29</p><h3>Bloch near-carrier cancellation 与 complete physical-kinetic finite transient</h3>
            <p>zero-lattice Bloch carrier 的 exact cancellation 把 coupling-side \(g^{-1}\) 化为 bounded physical orientation；primitive velocity energy 再覆盖 OS、Squire 与 exceptional rows。</p><p>每一行保留 \(e^{-g_j(d-s)}\) 并共同支付 \(e^{|\Lambda|K/2}\)，离散 rows 和连续 Bloch direct integral 都没有 row-count loss。</p>
            <p><strong>结论边界：</strong>&nbsp;fixed-\(c\) low-gap uniformity 与 prefactor-one contraction 为 FALSE；sharp \(|\Lambda|\) law、complete A2 direct sum、transportedAdjointPressureA2Modulation、nonlinearNavierStokes 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-73b.html"><strong>阅读 R0.73B 研究笔记 →</strong></a><br><a href="/notes/r0-73b.pdf">下载同步研究笔记 PDF</a> · <a href="/assets/r073b/fig-r073b-bloch-kinetic-transient.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073b">查看确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073b_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73b.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73C：</strong>&nbsp;sharp large-\(|\Lambda|\) transient law。</p>
          </div>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R073A_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.73A: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError("R0.73B source-stage manifest contract is missing, stale, or has extra fields")


def preflight_release_state() -> None:
    release = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    expected_site = {"schemaVersion": "research-site-version-v1", "version": "1.40", "latestRelease": "R0.73A", "publicHtmlNoteCount": 177, "publishedDate": "2026-08-29"}
    if json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8")) != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.73A")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 177:
        raise RuntimeError("R0.73A preflight expected 177 public HTML notes")
    for relative in ("notes/r0-73b.html", "notes/r0-73b.pdf", "recap-r0-61-r0-73b.html", "recap-r0-61-r0-73b.pdf"):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.73A preflight found premature public output: {relative}")
    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in ('data-site-version="1.40"', "<strong>177</strong>公开研究笔记", "<strong>R0.73A</strong>最新研究节点", 'aria-label="R0.69P–R0.73A"'):
        if token not in home:
            raise RuntimeError(f"R0.73A home baseline missing token: {token}")
    if 'data-release="r073b"' in home:
        raise RuntimeError("R0.73A home already contains an R0.73B card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73A">(.*?)</nav>', home, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 87:
        raise RuntimeError("R0.73A home route expected 87 notes")
    recap = (PUBLIC / "recap-r0-61-r0-73a.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 117 or len(set(links)) != 117 or recap.count('<article class="phase">') != 36:
        raise RuntimeError("R0.73A recap baseline expected 117 unique nodes and 36 phases")
    inventory = json.loads((ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r073a", 79, 55, 24):
        raise RuntimeError("formal archive inventory is not at R0.73A")


def _binding_paths(manifest: dict) -> set[str]:
    bindings = manifest.get("sourceBindings")
    if not isinstance(bindings, list) or not bindings:
        raise RuntimeError("formal certificate sourceBindings are missing")
    paths = {row.get("path") for row in bindings if isinstance(row, dict)}
    if None in paths or len(paths) != len(bindings):
        raise RuntimeError("formal certificate sourceBindings are malformed or duplicated")
    return paths


def _verify_experiment_manifest() -> None:
    directory = ROOT / EXPERIMENT_RELATIVE
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "completed" or manifest.get("finiteDimensionalOnly") is not True:
        raise RuntimeError("R0.73B finite experiment scope or status mismatch")
    if manifest.get("configuration", {}).get("caseCount") != 280 or manifest.get("configuration", {}).get("normCount") != 7:
        raise RuntimeError("R0.73B finite experiment grid mismatch")
    source = directory / str(manifest.get("source", ""))
    if not source.is_file() or digest(source) != manifest.get("sourceSha256"):
        raise RuntimeError("R0.73B finite experiment source hash mismatch")
    for row in manifest.get("outputs", []):
        path = directory / str(row.get("path", ""))
        if not path.is_file() or path.stat().st_size != row.get("bytes") or digest(path) != row.get("sha256"):
            raise RuntimeError(f"R0.73B finite experiment output hash mismatch: {row.get('path')}")
    validation = json.loads((directory / "validation.json").read_text(encoding="utf-8"))
    if validation.get("status") != "passed" or not all(validation.get("checks", {}).values()):
        raise RuntimeError("R0.73B finite experiment validation failed")


def validate_inputs() -> None:
    required_inputs = (
        "research/r073b_report-source.md", "research/r073b_problem_freeze.md", "research/r073b_literature_audit.md",
        "research/r073b_gap_matrix.md", "research/r073b_kinetic_form_proof.md", "research/r073b_independent_analytic_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md", f"{CERTIFICATE_RELATIVE}/certificate.json",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json", f"{CERTIFICATE_RELATIVE}/manifest.json",
        f"{EXPERIMENT_RELATIVE}/manifest.json", f"{EXPERIMENT_RELATIVE}/contract.json",
        f"{EXPERIMENT_RELATIVE}/summary.json", f"{EXPERIMENT_RELATIVE}/validation.json",
        f"{EXPERIMENT_RELATIVE}/weighted_propagator_rows.csv", f"{EXPERIMENT_RELATIVE}/targeted_asymptotics.csv",
        f"{FIGURE_RELATIVE}/manifest.json", f"{FIGURE_RELATIVE}/contract.json", f"{FIGURE_RELATIVE}/config.json",
        f"{FIGURE_RELATIVE}/caption.md", f"{FIGURE_RELATIVE}/README.md", f"{FIGURE_RELATIVE}/validate.py",
        "scripts/i18n-snapshots/r073b-missing.json", "public/notes/r0-73a.html", "public/recap-r0-61-r0-73a.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.73B release input: {relative}")
    report = (ROOT / "research/r073b_report-source.md").read_text(encoding="utf-8")
    for token in (
        "exactBlochNearCarrierCancellation", "exactBlochCarrierSystem", "blochNearCarrierFiniteTransient",
        "exactHeatShearGradientPrimitive", "completePhysicalKineticFiniteTransient",
        "completeOSSquireKineticFiniteTransient", "blochUniformPhysicalVelocityDirectSumAtViscousRates",
        "physicalKineticForcedDuhamel", "sharpKineticShearFormCoefficientAndLowGapLimit",
        "nearCarrierInstantaneousKineticGrowth", "lambdaIndependentKineticPrefactor",
        "fixedCUniformLowGapKineticPropagator", "allRowPrefactorOneKineticContraction",
        "polynomiallySharpLambdaKineticPrefactor", "completeOSSquireA2DirectSum",
        "transportedAdjointPressureA2Modulation",
        "nonlinearNavierStokes", "Clay", "\\texttt{ANALYTIC\\_PASS}", "\\texttt{FALSE}", "\\texttt{OPEN}",
    ):
        if token not in report:
            raise RuntimeError(f"R0.73B report missing final stable token: {token}")
    if "TO_PROVE" in report or "TO_DISPROVE" in report:
        raise RuntimeError("R0.73B report still contains candidate-only claim states")
    audit = (ROOT / "research/r073b_independent_analytic_audit.md").read_text(encoding="utf-8")
    for token in ("ANALYTIC PASS", "Bloch", "physical kinetic", "fixed-\\(c\\)", "direct sum"):
        if token not in audit:
            raise RuntimeError(f"R0.73B independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.73B certificate")
    verify_flat_hash_ledger(figure, "R0.73B figure")
    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    certificate_payload = json.loads((certificate / "certificate.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if certificate_manifest.get("status") != "formal" or certificate_payload.get("certificateStage") != "formal":
        raise RuntimeError("R0.73B certificate is not formal")
    source_commit = str(certificate_payload.get("sourceCommit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("R0.73B certificate source commit is absent")
    if crosscheck.get("status") != "passed" or crosscheck.get("finiteDimensionalOnly") is not True:
        raise RuntimeError("R0.73B finite crosscheck is not a passed finite-only audit")
    expected_bound_sources = {
        "research/r073b_report-source.md", "research/r073b_problem_freeze.md", "research/r073b_literature_audit.md",
        "research/r073b_gap_matrix.md", "research/r073b_kinetic_form_proof.md", "research/r073b_independent_analytic_audit.md",
        "research/certificates/r073b/generate_certificate.py", "research/certificates/r073b/independent_recompute.py",
        "research/certificates/r073b/validate_certificate.py",
        "experiments/r073b/weighted_kinetic_screen.py", "experiments/r073b/validate_weighted_kinetic_screen.py",
        "experiments/r073b/manifest.json", "experiments/r073b/validation.json",
        "scripts/generate_r073b_release.py", "scripts/add-r073b-translations.mjs", "scripts/i18n-snapshots/r073b-missing.json",
        "tests/r073b-bloch-kinetic-gate.test.mjs", "tests/r073b-release.test.mjs",
        "tests/r073b-deterministic-certificate-source.test.mjs", "tests/r073b-bloch-kinetic-transient-figure-source.test.mjs",
        f"{FIGURE_RELATIVE}/contract.json", f"{FIGURE_RELATIVE}/config.json", f"{FIGURE_RELATIVE}/caption.md", f"{FIGURE_RELATIVE}/README.md",
    }
    missing_bindings = expected_bound_sources - _binding_paths(certificate_manifest)
    if missing_bindings:
        raise RuntimeError(f"R0.73B formal source binding is incomplete: {sorted(missing_bindings)}")
    subprocess.run([sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"], cwd=ROOT, check=True)
    _verify_experiment_manifest()

    figure_manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    figure_contract = json.loads((figure / "contract.json").read_text(encoding="utf-8"))
    if figure_manifest.get("release") != "R0.73B" or figure_manifest.get("figureId") != FIGURE_ID or figure_manifest.get("status") != "formal":
        raise RuntimeError("R0.73B figure identity or formal status mismatch")
    if figure_manifest.get("qa", {}).get("status") != "passed" or figure_manifest.get("qa", {}).get("visualInspectionExplicit") is not True:
        raise RuntimeError("R0.73B figure visual QA is not formal")
    claims = figure_contract.get("claimBoundary", {})
    for key in ("finiteDimensionalRowsAreTheorem", "enhancedDissipationA2DirectSum", "nonlinearNavierStokesClosure", "clayMillenniumProblemSolved", "exactMaximumTransientGain"):
        if claims.get(key) is not False:
            raise RuntimeError(f"R0.73B figure escaped OPEN boundary: {key}")
    subprocess.run([sys.executable, str(figure / "validate.py")], cwd=ROOT, check=True)
    if figure_manifest.get("publication", {}).get("directory") != "public/assets/r073b":
        raise RuntimeError("R0.73B figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = PUBLIC / "assets/r073b" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.73B public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-73a.html").read_text(encoding="utf-8")
    replacements = (
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.73B：Bloch near-carrier cancellation 与完整 physical-kinetic viscous-rate finite transient。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.73B｜Bloch cancellation and physical kinetic transient">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="完整线性速度行可求和；A2、sharp Lambda law、nonlinear 与 Clay 保持 OPEN。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r073b/fig-r073b-bloch-kinetic-transient.png">'),
        (r'<title>.*?</title>', '<title>R0.73B｜Bloch cancellation and physical kinetic transient</title>'),
    )
    for index, (pattern, value) in enumerate(replacements):
        html = section(html, pattern, value, f"B note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.40", "/i18n-en.js?v=1.41", "B note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#bloch">Bloch</a><a href="#cancellation">抵消</a><a href="#hybrid">hybrid</a><a href="#energy">能量</a><a href="#primitive">primitive</a><a href="#propagator">propagator</a><a href="#forcing">forcing</a><a href="#ossquire">OS--Squire</a><a href="#sharp">sharp coefficient</a><a href="#growth">growth</a><a href="#liftup">lift-up</a><a href="#fixedc">路径</a><a href="#finite">finite</a><a href="#literature">文献</a><a href="#evidence">证据</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "B note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "B note hero")
    toc_items = [("result", "00 · direct decision"), ("bloch", "01 · Bloch carrier"), ("cancellation", "02 · exact cancellation"), ("hybrid", "03 · hybrid transient"), ("energy", "04 · kinetic identity"), ("primitive", "05 · heat primitive"), ("propagator", "06 · complete row"), ("forcing", "07 · Duhamel"), ("ossquire", "08 · OS--Squire"), ("sharp", "09 · sharp coefficient"), ("growth", "10 · growth witness"), ("liftup", "11 · lift-up"), ("fixedc", "12 · parameter path"), ("finite", "13 · finite diagnostic"), ("literature", "14 · literature"), ("evidence", "15 · evidence"), ("figure", "16 · journal figure"), ("value", "17 · value"), ("next", "18 · R0.73C"), ("reproduce", "19 · reproduction")]
    toc = '      <aside class="toc"><strong>CONTENTS</strong><ol>\n' + "".join(f'        <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_items) + '\n      </ol></aside>'
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "B note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "B note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.73B · 2026-08-29<br><a href="/">返回研究主页</a></div></footer>', "B note footer")
    for stale in ("fig-r073a-hidden-mean-transient-spectral", "R0.73A scoped physical row"):
        if stale in html:
            raise RuntimeError(f"R0.73B note contains stale R0.73A copy: {stale}")
    assert_clean(html, "R0.73B note")
    assert_mathjax_clean(html, "R0.73B note")
    (PUBLIC / "notes/r0-73b.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-73a.html").read_text(encoding="utf-8")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.73B 的 118 个节点；最新一节闭合 Bloch carrier cancellation 与 complete physical-kinetic finite transient。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.73B｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十七个阶段、118 个节点：从约化递推到 Bloch near-carrier 与 complete linear kinetic direct sum。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.73B｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "B recap " + label)
    html = required(html, "/i18n-en.js?v=1.40", "/i18n-en.js?v=1.41", "B recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.73B · 2026-08-29</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页完整保留 R0.61 到 R0.73B 的 118 个研究节点。R0.69P 以后从局部证书推进到 scalar A2 collision、完整 Fourier row 与 high-gap OS；R0.73A 正则化 physical hidden mean，R0.73B 再闭合 exact Bloch near-carrier cancellation 与 complete linear physical-kinetic finite transient。A2、nonlinear 与 Clay 没有被外推。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73B</strong><p>收录节点：118</p><p>回顾截止时公开笔记：178</p><p>回顾截止节点：R0.73B</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "B recap hero")
    for old, new in (("02 · 117 节完整索引", "02 · 118 节完整索引"), ("01 · 三十六个研究阶段", "01 · 三十七个研究阶段"), ("R0.60 之后的路线分成三十六个阶段", "R0.60 之后的路线分成三十七个阶段"), ('data-current-route="R0.69P–R0.73A"', 'data-current-route="R0.69P–R0.73B"')):
        html = required(html, old, new, "B recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>118</strong><span>R0.61–R0.73B 研究节点</span></div><div class="metric"><strong>80</strong><span>R0.70A–R0.73B 已公开版本</span></div><div class="metric"><strong>56</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.73B 的 80 个版本已公开，其中 56 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "B recap result")
    phase = r'''            <article class="phase"><h3>R0.73B · Bloch carrier and complete physical-kinetic finite transient</h3><p>exact Bloch near-carrier cancellation、bounded orientation coefficient、complete primitive kinetic row estimate、forced Duhamel 与 row/direct-integral summation 为 CLOSED。</p><p>sharp OS shear coefficient 有 exact low-gap limit；载波—切向 growth witness、exact lift-up 与 fixed-\(c\) lower bound 分别排除 prefactor-one、\(\Lambda\)-independent 与 fixed-\(c\) uniformity。</p><p>sharp large-\(|\Lambda|\) law、complete OS--Squire A2 direct sum、transportedAdjointPressureA2Modulation、nonlinearNavierStokes 与 Clay 保持 OPEN。</p><div class="links"><a href="/notes/r0-73b.html">R0.73B</a><a href="/assets/r073b/fig-r073b-bloch-kinetic-transient.pdf">R0.73B 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073b">R0.73B 证书</a></div></article>
'''
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "B recap phase")
    html = required(html, "R0.61–R0.73A 的 117 节公开笔记", "R0.61–R0.73B 的 118 节公开笔记", "B recap node title")
    node_a = '            <span class="node-ref"><a href="/notes/r0-73a.html">R0.73A</a><span class="node-state kind-closed">闭</span></span>\n'
    node_b = '            <span class="node-ref"><a href="/notes/r0-73b.html">R0.73B</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_a, node_a + node_b, "B recap node")
    html = required(
        html,
        '<span class="node-ref"><a href="/notes/r0-72t.html">R0.72T</a><span class="node-state kind-nogo">阻</span></span>',
        '<span class="node-ref"><a href="/notes/r0-72t.html">R0.72T</a><span class="node-state kind-conditional">条件</span></span>',
        "B recap R0.72T state",
    )
    html = required(
        html,
        '<li>R0.72S 的 marked singular-strata ledger：incidence preimage 止于 \\(A_5\\)，coefficient-derivative jet determinant 为 \\(5400\\)；pure-second \\(A_2\\) path 的 distinct count 是 \\(4/3/2\\)，real-even \\(A_3\\) path 是 \\(4/2/2\\)，且两者 crossing multiplicity 都为四。</li>',
        '<li>R0.72S 在 fixed-first-harmonic \\(1{:}2{:}3\\) family 内证明 incidence preimages 止于 \\(A_5\\)，coefficient-derivative jet determinant 为 \\(5400\\)。pure-second \\(A_2\\) path 的 distinct count 是 \\(4/3/2\\)，real-even \\(A_3\\) path 是 \\(4/2/2\\)；两者只在碰撞时按重数计为四，A3 只在 real-even slice 内横截。这不是四维 caustic image 的全局分类。</li>',
        "B recap R0.72S scope",
    )
    html = required(
        html,
        '<li>R0.73A 闭合 physical hidden-mean coordinate 与 \\(X_\\mu\\) finite-transient viscous-rate theorem，同时把 fixed-\\(\\Lambda\\) limit、kinetic/Squire/Bloch 与 nonlinear/Clay 保留为 OPEN。</li>',
        '<li>R0.73A 用 \\(h=\\Pi_0q/\\mu\\) 记录 hidden physical mean，在 \\(X_\\mu\\) 中闭合 all-start finite-transient viscous-rate bound。lifted tangent line 对每个 \\(c_\\mu\\ne0\\) 的正 gap 不 invariant；nonzero limit 只沿 \\(c_\\mu\\to c_0\\ne0\\)，fixed \\(\\Lambda\\) raw-\\(q\\) limit 与 kinetic/Squire/Bloch/nonlinear/Clay 保持 OPEN。</li>',
        "B recap R0.73A raw-q scope",
    )
    retained = r'''            <li>R0.73B 闭合 Bloch near-carrier cancellation 与 complete linear physical-kinetic finite transient，同时把 fixed-\(c\) uniformity、sharp \(|\Lambda|\) law、A2 direct sum 与 nonlinear/Clay 明确分开。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "B recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>该双谐波 heat path 上 complete linearized row 的 viscous-rate finite transient 已闭合；A2 与 nonlinear 门仍未闭合</h2><p>不能把 118 个节点或 80 个公开版本解释成 Clay 问题完成比例。R0.73B 的严格增量是 exact Bloch carrier cancellation、physical kinetic direct sum、sharp shear-form low-gap limit 和路径限定的反例；直接 Clay 价值仍有限。</p></section>''', "B recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73C 确定 sharp large-\(|\Lambda|\) transient law</h2><p>比较 exact lift-up lower bound、low-gap triangular limit 与 polynomial upper mechanism，再决定 complete OS--Squire A2 direct sum 的权重。</p></section>''', "B recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73B 的 80 节已公开；56 节完整封存；24 节旧档待回补。</p><p>lambdaIndependentKineticPrefactor、fixedCUniformLowGapKineticPropagator 与 allRowPrefactorOneKineticContraction 为 FALSE；polynomiallySharpLambdaKineticPrefactor、completeOSSquireA2DirectSum、transportedAdjointPressureA2Modulation、nonlinearNavierStokes 与 Clay 为 OPEN。</p></section>''', "B recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、实验、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73a.html">保留 R0.73A 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73b.html">打开最新节点 R0.73B</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073b">查看 R0.73B 确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073b">查看 finite diagnostic</a> · <a href="/assets/r073b/fig-r073b-bloch-kinetic-transient.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73b.pdf">下载同步 PDF</a></p><p>deterministic screen 包含 280 propagators、1960 primary norm rows 与 245 targeted rows。它复核 generator similarity、步长和模数收敛、符号对称、kinetic upper bound 与 fixed-\(\Lambda\) triangular limit。没有 Galerkin tail enclosure，也不证明无限维收敛或 nonlinear convolution。</p><p>完整节点索引保留 R0.61 起的全部历史编号；状态标签只描述证据类型。</p></section>''', "B recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73B 回顾 · 2026-08-29<br><a href="/">返回研究主页</a></div></footer>', "B recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 118 or len(set(links)) != 118 or html.count('<article class="phase">') != 37:
        raise RuntimeError("R0.73B recap expected 118 unique nodes and 37 phases")
    assert_clean(html, "R0.73B recap")
    assert_mathjax_clean(html, "R0.73B recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-73b.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.40"', 'data-site-version="1.41"'), ("/i18n-en.js?v=1.40", "/i18n-en.js?v=1.41"), ("/site-refresh.js?v=1.40", "/site-refresh.js?v=1.41"),
        ("<strong>2026-08-28</strong>最近修订", "<strong>2026-08-29</strong>最近修订"), ("<strong>v1.40</strong>网页版本", "<strong>v1.41</strong>网页版本"), ("<strong>177</strong>公开研究笔记", "<strong>178</strong>公开研究笔记"), ("<strong>R0.73A</strong>最新研究节点", "<strong>R0.73B</strong>最新研究节点"),
        ("Research topology · R0.1–R0.73A", "Research topology · R0.1–R0.73B"), ("R0.70A–R0.73A：79 节已公开，55 节完整封存", "R0.70A–R0.73B：80 节已公开，56 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73A</span>', '<span class="route-range">R0.69P–R0.73B</span>'), ('aria-label="R0.69P–R0.73A"', 'aria-label="R0.69P–R0.73B"'),
        ("展开 87 篇公开笔记", "展开 88 篇公开笔记"), ("本站 R0.69P–R0.73A 路线", "本站 R0.69P–R0.73B 路线"),
        ("综述 v1.40 · 2026-08-29", "综述 v1.41 · 2026-08-29"), ("上次综述 v1.39 · 2026-08-28", "上次综述 v1.40 · 2026-08-29"),
        ("/recap-r0-61-r0-73a.html", "/recap-r0-61-r0-73b.html"), ("/recap-r0-61-r0-73a.pdf", "/recap-r0-61-r0-73b.pdf"),
        ("<strong style=\"color:var(--gold)\">下一步 R0.73B：</strong>&nbsp;weighted physical modulation and kinetic control。", "<strong style=\"color:var(--gold)\">当时的下一步 R0.73B：</strong>&nbsp;weighted physical modulation and kinetic control。"),
    ):
        html = required(html, old, new, "B home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73B 已闭合 exact Bloch near-carrier cancellation 与 complete linear physical-kinetic finite transient。下一关是 sharp large-\(|\Lambda|\) transient law。</span></div>', "B home focus")
    link_a = '<a class="milestone" href="/notes/r0-73a.html">R0.73A</a>'
    html = once(html, link_a, link_a + '\n                  <a class="milestone" href="/notes/r0-73b.html">R0.73B</a>', "B home route link")
    route_b = r'''              <p>R0.73B 由 exact Bloch carrier cancellation 得到 bounded physical orientation，并用 primitive kinetic identity 闭合 complete linear velocity/Squire rows 的 finite transient direct sum。fixed-\(c\) uniformity 与 prefactor-one contraction 为 FALSE；A2、sharp \(|\Lambda|\)、nonlinear 与 Clay 保持 OPEN。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_b + '              <details class="tree-notes" open>', "B home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "B home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73B · 2026-08-29</p><h3>R0.60 recap 之后的累计回顾收录 118 个节点；全站现有 178 篇公开研究笔记</h3><p>累计回顾现分三十七个问题阶段，并给出 R0.61–R0.73B 的完整索引；R0.73B 分开记录 infinite-dimensional energy theorem、path-qualified negative results 与 finite diagnostic。</p><p>R0.70A–R0.73B 共 80 个版本已公开；56 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;complete linear viscous-rate direct sum 已闭合；sharp \(|\Lambda|\)、A2、nonlinear 与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73b.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73b.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "B home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_B_CARD + '\n        </section>\n\n      </article>', "B home card")
    if html.count('data-release="r073b"') != 1:
        raise RuntimeError("home must contain exactly one R0.73B card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73C：') != 1 or '<strong style="color:var(--gold)">下一步 R0.73B：' in html:
        raise RuntimeError("home must distinguish the unique current R0.73C next gate from historical R0.73B")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73B">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 88:
        raise RuntimeError("home current-route index must contain 88 note links")
    assert_clean(html, "R0.73B home")
    assert_mathjax_clean(html, "R0.73B home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.40", "/i18n-en.js?v=1.41"), ("本站 R0.69P–R0.73A 只列为研究笔记", "本站 R0.69P–R0.73B 只列为研究笔记"),
        ("/recap-r0-61-r0-73a.html", "/recap-r0-61-r0-73b.html"), ("文献综述 v1.40 · 2026-08-29", "文献综述 v1.41 · 2026-08-29"),
        ("累计回顾与 117 节索引", "累计回顾与 118 节索引"), ("打开 117 节完整索引", "打开 118 节完整索引"),
    ):
        html = required(html, old, new, "B literature " + old)
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73B</b><strong>weighted physical modulation and kinetic control</strong></header><p>把 physical mean、tangent carrier、near-constant mode 与 adjoint pressure cost 统一到显式带权演化估计。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73B</b><strong>Bloch carrier and complete physical-kinetic finite transient</strong></header><p>exact Bloch cancellation、bounded orientation、primitive kinetic row estimate、forced Duhamel 与 direct-sum/direct-integral closure 已完成。fixed-\(c\) uniformity 与 prefactor-one contraction 为 FALSE；A2、sharp \(|\Lambda|\)、nonlinear 与 Clay 保持 OPEN。<a href="/notes/r0-73b.html">研究笔记</a> <a href="/recap-r0-61-r0-73b.html">当前累计回顾</a> <a href="#r073b-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73C</b><strong>sharp large-Lambda transient law</strong></header><p>比较 exact lift-up lower bound、triangular low-gap limit 与 polynomial upper mechanism，再选择 A2 modulation 的正确权重。</p></div>'''
    html = once(html, old_open, new_steps, "B literature route")
    boundary = r'''

          <h3 id="r073b-boundary">R0.73B 的 Bloch、OS--Squire 与 kinetic transient 文献边界</h3>
          <p>Jerome--Chomaz 固定 OS--Squire physical kinetic metric 与 lift-up；Bedrossian--Germain--Masmoudi 固定 streak/lift-up dynamics；Li--Wei--Zhang 给 periodic three-dimensional good unknown；Li--Zhao 与 Wei--Zhang--Zhao 给不同 nonautonomous shear propagator；Bedrossian--Coti Zelati 给 hypocoercive weights。bounded primary-source search 没有发现同一来源同时给出本项目的 double-harmonic heat path、near carrier、physical velocity、Squire 与 Bloch direct sum。我只报告组合接口，不把它写成 novelty 或 priority proof。</p>
          <div class="boundary"><strong>R0.73B 的主张边界</strong><p>exactBlochNearCarrierCancellation、completePhysicalKineticFiniteTransient、completeOSSquireKineticFiniteTransient 与 blochUniformPhysicalVelocityDirectSumAtViscousRates 为 CLOSED。lambdaIndependentKineticPrefactor、fixedCUniformLowGapKineticPropagator 与 allRowPrefactorOneKineticContraction 为 FALSE。polynomiallySharpLambdaKineticPrefactor、completeOSSquireA2DirectSum、nonlinearNavierStokes 与 Clay 为 OPEN。</p></div>'''
    match = re.search(r'(<h3 id="r073a-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("B literature expected R0.73A boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "B literature boundary")
    assert_clean(html, "R0.73B literature")
    assert_mathjax_clean(html, "R0.73B literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 178:
        raise RuntimeError("expected 178 public HTML notes after R0.73B")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r073b", "siteVersion": "1.41", "publicHtmlNoteCount": 178, "postR060RecapNodeCount": 118,
        "nextRelease": "r073c", "latestReleaseGate": "tests/r073b-bloch-kinetic-gate.test.mjs", "latestReleasePublicationTest": "tests/r073b-release.test.mjs",
        "postR070APublishedReleaseCount": 80, "postR070AFormalSealedReleaseCount": 56, "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.40", "R0.73A", 177):
        raise RuntimeError("site-version is not at R0.73A")
    site.update({"version": "1.41", "latestRelease": "R0.73B", "publicHtmlNoteCount": 178, "publishedDate": "2026-08-29"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r073a", 79, 55, 24):
        raise RuntimeError("formal archive inventory is not at R0.73A")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r073a" or "r073b" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.73A")
        inventory[key].append("r073b")
    inventory.update({"latestPublishedRelease": "r073b", "publishedReleaseCount": 80, "formalSealedReleaseCount": 56, "legacyFormalFigureBacklogCount": 24})
    if len(inventory["publishedReleases"]) != 80 or len(inventory["formalSealedReleases"]) != 56:
        raise RuntimeError("formal archive count mismatch after R0.73B")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "VERSION").write_text("1.41\n", encoding="utf-8")


def main() -> None:
    preflight_release_state()
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-73b.html", "recap-r0-61-r0-73b.html"):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.73B", "siteVersion": "1.41", "notes": 178, "recapNodes": 118,
        "published": 80, "formalSealed": 56, "legacyBacklog": 24, "phases": 37, "routeNotes": 88, "next": "R0.73C",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
