#!/usr/bin/env python3
"""Generate the deterministic R0.72S release from the public R0.72R endpoint.

The fail-closed preflight verifies the formal exact certificate, the formal
heat-collision figure package, and byte-identical public figure copies before
mutating HTML or manifests.  This script does not generate PDFs.
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


ROOT = Path(os.environ.get("R072S_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_RELATIVE = "figures/r072s-heat-collisions/fig-r072s-heat-collisions"
FIGURE_ID = "fig-r072s-heat-collisions"
CERTIFICATE_RELATIVE = "research/certificates/r072s"
ARNOLD_1997 = "https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_4"


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72S · EXACT SINGULAR STRATA · TWO HEAT COLLISIONS</div>
        <h1>局部奇性账本已经闭合；<br>两条热路径给出不同的临界点碰撞</h1>
        <p class="lead">对固定第一谐波的 complex \(1{:}2{:}3\) family，我把 incidence preimage 精确分成 \(A_2,A_3,A_4,A_5\)，并核对 coefficient-derivative jet determinant \(5400\)。一个 pure-second path 在 \(y_*=\log2\) 发生全系数切片中横截的 \(A_2\) fold，distinct count 为 \(4/3/2\)；另一个 real-even path 发生 symmetry-restricted \(A_3\)，distinct count 为 \(4/2/2\)，且只在实偶切片内横截。两者在碰撞时按重数都计为四。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72S exact local strata 与 heat collisions 完成</span><strong>marked singular strata and two exact heat paths: CLOSED</strong><p>版本 v0.72S · 2026-08-28</p><p>incidence-preimage \(A_2/A_3/A_4/A_5\) ledger: CLOSED</p><p>restricted miniversal modulo constants: CLOSED</p><p>pure-second \(A_2\) distinct count \(4/3/2\): CLOSED</p><p>real-even \(A_3\) distinct count \(4/2/2\): CLOSED</p><p>global caustic image classification: OPEN</p><p>ED through collision / Clay problem: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r"""      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>局部奇性与两条全热路径已精确计数，穿墙 PDE 仍开放</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · MARKED INCIDENCE STRATA</strong><p>每个 incidence preimage 恰为 \(A_2,A_3,A_4\) 或 \(A_5\)；该有限谐波族没有更高型。</p></div>
            <div class="verdict-card true"><strong>THEOREM · RESTRICTED MINIVERSAL</strong><p>四个系数方向对一至四阶导数 jet 的行列式为 \(5400\)，所以 modulo additive constants 局部余维依次为 \(1,2,3,4\)。</p></div>
            <div class="verdict-card true"><strong>THEOREM · TWO HEAT COLLISIONS</strong><p>pure-second \(A_2\) 路径的 distinct count 是 \(4/3/2\)；real-even \(A_3\) 路径是 \(4/2/2\)。两者碰撞时按重数均为四。</p></div>
            <div class="verdict-card false"><strong>OPEN · GLOBAL IMAGE AND PDE</strong><p>没有分类完整四维 caustic image，也没有证明临界点数或重数改变时仍统一成立的 enhanced dissipation。</p></div>
          </div>
        </section>

        <section id="incidence"><div class="section-no">01 / Incidence preimages</div><h2>先固定退化临界点，再分类它的 vanishing order</h2>
          <p>在 \(z_3e^{3i\phi}=A+iB\) 下，\(f'=f''=0\) 等价于</p>
          <div class="equation result">\[
          z_3=(A+iB)e^{-3i\phi},\qquad
          z_2=e^{-2i\phi}\left[-\frac{\cos\phi+9A}{4}
          -\frac{i(\sin\phi+3B)}2\right].
          \]</div>
          <div class="equation result">\[
          f'''=3(5B-\sin\phi),\quad f''''=3(15A-\cos\phi),
          \]</div>
          <div class="equation result">\[
          f'''''=15(\sin\phi-13B),\quad
          f''''''=15(\cos\phi-39A).
          \]</div>
          <p>因此 \(B\ne\sin\phi/5\) 给 \(A_2\)；再令 \(B=\sin\phi/5\) 得 \(A_3\) 条件；继续令 \(A=\cos\phi/15\) 得 \(A_4\)，其五阶 jet 为 \(-24\sin\phi\)。端点再退化时六阶 jet 为 \(-24\cos\phi\ne0\)，所以终止于 \(A_5\)。</p>
        </section>

        <section id="versal"><div class="section-no">02 / Restricted miniversality</div><h2>5400 控制 derivative jets，不包含函数值方向</h2>
          <div class="equation result">\[
          W_0=\begin{pmatrix}
          0&-2&0&-3\\-4&0&-9&0\\0&8&0&27\\16&0&81&0
          \end{pmatrix},\qquad \boxed{\det W_0=5400}.
          \]</div>
          <p>任意 \(\phi\) 只旋转二、三谐波的两个实系数块，行列式不变。这个结论给出 critical-point geometry modulo additive constants 的 restricted miniversal，也就是 \(R^+\)-versal。若连函数值一起记录，\(A_5\) 的 full miniversal deformation 还需要一个常数参数。</p>
          <p>允许 marked state \(\phi\) 移动后，单个局部 \(A_k\) coefficient branch 的余维为 \(k-1\)。这是 preimage branch 的局部结论，不是完整 projected caustic 已经嵌入或没有 self-intersection 的证明。</p>
        </section>

        <section id="a2"><div class="section-no">03 / Pure-second A2 path</div><h2>一个二次方程给出全路径唯一退化与 \(4/3/2\)</h2>
          <div class="equation result">\[
          F_y(\phi)=\cos\phi-4e^{-3y}\sin2\phi,\qquad
          F_y'=2k\sin^2\phi-\sin\phi-k,\quad k=8e^{-3y}.
          \]</div>
          <div class="equation result">\[
          s_\pm(k)=\frac{1\pm\sqrt{1+8k^2}}{4k}.
          \]</div>
          <p>\(s_-\in(-1,0)\) 对全部 \(k&gt;0\) 成立；\(s_+\) 在 \(k&gt;1\) 时位于 \((0,1)\)，在 \(k=1\) 等于一，在 \(0&lt;k&lt;1\) 时离开实 sine range。结合 \(F_y''=\cos\phi(-1+4k\sin\phi)\)，全路径唯一退化点是 \(y_*=\log2,\phi_*=\pi/2\)。</p>
          <div class="equation result">\[
          N_{\rm distinct}(y)=
          \begin{cases}4,&0\le y&lt;\log2,\\3,&y=\log2,\\2,&y&gt;\log2.
          \end{cases}
          \]</div>
          <p>等号时一个 \(A_2\) 点为二重根，另有两个简单点，所以按重数仍为四。这个 representative 的第三 carrier 为零，但 \(F'''=\partial_yF'=-3\ne0\)，路径对 full four-real coefficient slice 的局部 codimension-one \(A_2\) wall 横截。</p>
        </section>

        <section id="a3"><div class="section-no">04 / Real-even A3 path</div><h2>对称轴保留中心临界点，两个 off-axis roots 并入它</h2>
          <div class="equation result">\[
          H_y(\phi)=\cos\phi-\frac{2563}{1280}e^{-3y}\cos2\phi
          +\frac1{30}e^{-8y}\cos3\phi.
          \]</div>
          <p>写 \(t=e^{-y}\)、\(x=\cos\phi\)，则 \(H_y'=-\sin\phi\,q_t(x)\)，其中</p>
          <div class="equation result">\[
          q_t(x)=\frac25t^8x^2-\frac{2563}{320}t^3x+1-\frac1{10}t^8.
          \]</div>
          <p>\(q_t\) 在 \([-1,1]\) 上严格下降，\(q_t(-1)&gt;0\)，且 \(q_t(1)\) 恰在 \(t=1/2\) 变号。因此</p>
          <div class="equation result">\[
          N_{\rm distinct}(y)=
          \begin{cases}4,&0\le y&lt;\log2,\\2,&y=\log2,\\2,&y&gt;\log2.
          \end{cases}
          \]</div>
          <p>碰撞点 \(\phi=0\) 是 \(A_3\) 三重根，\(\phi=\pi\) 是简单根，所以按重数仍为四。这里 \(H''''=\partial_yH''=-1533/512\ne0\)。函数芽属于 ambient \(A_3\) stratum，但一参数路径只在 real-even 二维切片内横截 endpoint wall；不能称为 full-space transverse \(A_3\)。</p>
        </section>

        <section id="local"><div class="section-no">05 / Local branch laws</div><h2>两种碰撞都有平方根分支，但中心机制不同</h2>
          <p>令 \(\delta=y-\log2\)。在 \(A_2\) 点取 \(\xi=\phi-\pi/2\)，在 \(A_3\) 点取 \(\phi\) 本身，则</p>
          <div class="equation result">\[
          F_y'=-3\delta-\frac32\xi^2
          +O(\delta^2+|\delta|\xi^2+\xi^4),\qquad
          \xi_\pm=\pm\sqrt{-2\delta}+O(|\delta|^{3/2}),
          \]</div>
          <div class="equation result">\[
          H_y'=K\phi\left(\delta+\frac{\phi^2}{6}\right)
          +O(\delta^2|\phi|+|\delta||\phi|^3+|\phi|^5),\quad
          K=-\frac{1533}{512},\quad
          \phi_\pm=\pm\sqrt{-6\delta}+O(|\delta|^{3/2}).
          \]</div>
          <p>第一条路径中碰撞点随后消失；第二条路径中反射对称性让中心点始终保留。附图只展示这两条已证明的局部分支，不替代全局单调性证明。</p>
        </section>

        <section id="counts"><div class="section-no">06 / Count convention</div><h2>distinct locations 与 root multiplicity 必须分开</h2>
          <p>pure-second \(A_2\) 的 before/at/after distinct count 是 \(4/3/2\)，碰撞时重数分解为 \(2+1+1=4\)。real-even \(A_3\) 是 \(4/2/2\)，碰撞时为 \(3+1=4\)。把阈值时刻简写为“\(4\to2\)”会丢失两种局部机制的差别。</p>
          <p>同样，incidence preimage 是带 marked \(\phi\) 的解；把它投影到 \((z_2,z_3)\) 后，多个 preimages 可以落在同一系数点。本节没有枚举这种 multisingularity，也没有给完整 chamber diagram。</p>
        </section>

        <section id="pde"><div class="section-no">07 / PDE boundary</div><h2>冻结 profile 的有限型速率不能拼成穿越碰撞的定理</h2>
          <p>stationary finite-type 文献给 frozen \(A_2\) profile 的 \(\nu^{3/5}\) benchmark 和 frozen \(A_3\) profile 的 \(\nu^{2/3}\) benchmark。现有 nonautonomous 结果覆盖共同非退化临界点、固定空间 profile 的时间调制或保持临界点类型与数量的刚性平移；它们不覆盖这里的 creation、annihilation 或 multiplicity change。</p>
          <p>因此 R0.72S 没有证明 ED through collision。把每个 frozen time 的速率逐点拼接，也不能替代一个统一的非自治 subelliptic 或 hypocoercive estimate。</p>
        </section>

        <section id="certificate"><div class="section-no">08 / Exact certificate</div><h2>Fraction 与 BigInt 双路只封存有限代数骨架</h2>
          <p>Python rational producer 与独立 JavaScript BigInt audit 重建 incidence jets、determinant \(5400\)、两条路径的 exact sign guards、crossing jets 和 leading split coefficients \(-2,-6\)。comparator 要求 canonical payload 精确相同，正式证书还绑定同一 clean source commit。</p>
          <p>唯一碰撞与全局 distinct/multiplicity counts 由连续 root-count proof 推出；机器证书只核对该证明使用的有限恒等式和符号守卫。它不分类全局 caustic image，也不证明穿墙 enhanced dissipation。</p>
        </section>

        <section id="literature"><div class="section-no">09 / Literature boundary</div><h2>一般奇性理论、degree-three 拓扑与本站精确路径是三件事</h2>
          <p><a href="https://www.mathnet.ru/eng/rm4237">Arnol'd (1975)</a> 给出 \(A_k\) 与 versality 的标准局部框架；<a href="https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_4">Arnol'd (1997)</a> 研究 real degree-three maximal-real-critical region 的拓扑。R0.72S 不把 degree-three region 本身主张为新发现。</p>
          <p><a href="https://doi.org/10.1016/j.jfa.2022.109522">Albritton–Beekie–Novack</a> 与 <a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 给 stationary finite-type benchmarks；<a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He</a>、<a href="https://arxiv.org/abs/2501.16905">Benthaus–Nobili</a> 和 <a href="https://arxiv.org/abs/2603.14624">Benthaus–Coclite–Nobili</a> 划定当前 nonautonomous 边界。限定一手检索没有定位到穿越这里 multiplicity-changing collision 的 ED theorem；这是 bounded-search absence，不是不存在性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">10 / Journal figure</div><h2>三联图分别展示 incidence spine、A2 branches 与 A3 branches</h2>
          <p><img src="/assets/r072s/fig-r072s-heat-collisions.svg" alt="R0.72S exact singular strata and two heat-law critical-point collisions"></p>
          <p><a href="/assets/r072s/fig-r072s-heat-collisions.pdf">下载 PDF</a> · <a href="/assets/r072s/fig-r072s-heat-collisions.png">下载 PNG</a> · <a href="/assets/r072s/fig-r072s-heat-collisions.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">11 / Research value</div><h2>下一道可检验问题已经从几何墙转成非自治局部模型</h2>
          <p>R0.72S 的直接增量是一个可审计的局部 singular-strata ledger，以及两条全时间精确计数的 heat-law path。它给下一步 PDE 分析提供碰撞时间、jet constants 与 square-root branch scales，也明确说明现有 nondegenerate time-dependent theorem 在哪里失去假设。</p>
          <p>对 Clay 问题的直接价值仍低。这里是有限谐波 scalar shear 与特殊 triangular reduction 的局部几何，没有一般三维 continuation estimate，也没有奇性构造或全局正则性证明。</p>
        </section>

        <section id="scope"><div class="section-no">12 / Scope boundary</div><h2>local marked strata 不等于 global caustic，也不等于 Clay 进展比例</h2>
          <p>没有证明 incidence map injective、全部 self-intersections、multisingularities、完整 complement chambers、real \(A_{2j+1}^{\pm}\) refinement、two-parameter full-slice transverse \(A_3\)、任意相位 heat path、ED through collision、一般三维稳定性、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="next"><div class="section-no">13 / Next gate</div><h2>R0.72T：缩放 A2 spacetime normal form，并先证明模型估计</h2>
          <p>下一节围绕 \(F'\sim-3\delta-(3/2)\xi^2\) 选择时空尺度，平衡 time drift、quadratic spatial degeneracy、transport frequency 与 diffusion。只有先得到 uniform nonautonomous model estimate，才讨论向 exact heat path 的 perturbative transfer。</p>
        </section>

        <section id="reproduce"><div class="section-no">14 / Reproduction</div><h2>报告、文献边界、独立审计、精确证书与正式附图包</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072s_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072s_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072s_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072s_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072s">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072s-heat-collisions/fig-r072s-heat-collisions">正式附图包</a> · <a href="/notes/r0-72s.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72s.html">累计回顾</a> · <a href="/recap-r0-61-r0-72s.pdf">累计回顾 PDF</a></p>
        </section>
      </article>"""


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72T</span><span class="tree-state current">下一检查点</span></div>
              <h3>nonautonomous model estimate through the A2 collision</h3>
              <p>缩放 \(F'\sim-3\delta-(3/2)\xi^2\) 的 spacetime normal form，先证明统一 model estimate，再检查能否回传到 exact heat path。</p>
            </article>'''


HOME_S_CARD = r'''          <div class="task-one" id="r072s" data-release="r072s" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72S · 2026-08-28</p>
            <h3>marked \(A_2\)–\(A_5\) strata 与两条 heat collision 已精确闭合</h3>
            <p>incidence preimage 由 higher jets 精确分为 \(A_2,A_3,A_4,A_5\)；四个系数方向的一至四阶 derivative-jet determinant 为 \(5400\)，支持 modulo constants 的 restricted miniversal 与单个 marked branch 的局部余维 \(1,2,3,4\)。</p>
            <p>pure-second path 的 distinct count 为 \(4/3/2\)，且全 \(y\ge0\) 只有 \(y=\log2\) 一个 \(A_2\) 事件；real-even path 为 \(4/2/2\)，其 \(A_3\) 只在 real-even slice 内横截。两条路径在碰撞时按重数都为四。</p>
            <p><strong>结论边界：</strong>&nbsp;没有完成 global caustic image、自交或 chamber 分类，也没有证明 multiplicity-changing collision 上的 enhanced dissipation。Clay 问题保持开放。</p>
            <p><a href="/notes/r0-72s.html"><strong>阅读 R0.72S 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72s.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072s/fig-r072s-heat-collisions.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072s">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072s_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072s-heat-collisions/fig-r072s-heat-collisions">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72s.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72s.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72T：</strong>&nbsp;缩放 A2 spacetime normal form，并先证明非自治 model estimate。</p>
          </div>'''


def validate_inputs() -> None:
    required_inputs = (
        "research/r072s_report-source.md",
        "research/r072s_literature_audit.md",
        "research/r072s_gap_matrix.md",
        "research/r072s_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72r.html",
        "public/recap-r0-61-r0-72r.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72S release input: {relative}")

    report = (ROOT / "research/r072s_report-source.md").read_text(encoding="utf-8")
    for token in (
        "Every incidence preimage has one of the types \\(A_2,A_3,A_4,A_5\\)",
        "restricted miniversal (\\(R^+\\)-versal) unfolding through \\(A_5\\)",
        "\\boxed{\\det W_0=5400.}",
        "3,&y=\\log2",
        "2,&y\\ge\\log2",
        "total multiplicity four",
        "not called transverse in the full coefficient space",
        "enhanced dissipation uniformly through an \\(A_2\\) or \\(A_3\\) collision",
        "R0.72T",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72S report missing claim-boundary token: {token}")
    literature = (ROOT / "research/r072s_literature_audit.md").read_text(encoding="utf-8")
    for token in (
        "restricted miniversal",
        "bounded-search absence",
        ARNOLD_1997,
        "one-dimensional curve that hits it cannot be transverse",
        "does not discharge any clause of",
    ):
        if token not in literature:
            raise RuntimeError(f"R0.72S literature audit missing boundary token: {token}")
    independent = (ROOT / "research/r072s_independent_audit.md").read_text(encoding="utf-8")
    for token in ("4/3/2", "4/2/2", "5400", "only inside that", "global caustic image"):
        if token not in independent:
            raise RuntimeError(f"R0.72S independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72S certificate")
    verify_flat_hash_ledger(figure, "R0.72S figure")
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if (
        crosscheck.get("status") != "passed"
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not all(value is True for value in crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError("R0.72S crosscheck is not a formal all-passed seal")

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    publication = manifest.get("publication", {})
    if (
        manifest.get("release") != "R0.72S"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
        or publication.get("publicCopiesComplete") is not True
        or publication.get("directory") != "public/assets/r072s"
        or publication.get("stem") != FIGURE_ID
    ):
        raise RuntimeError("R0.72S figure manifest is not a complete formal seal")
    validator = ROOT / "research/validate_figure_package.py"
    completed = subprocess.run(
        [sys.executable, str(validator), str(figure)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("R0.72S strict figure validation failed")
    try:
        validation = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError("R0.72S strict figure validator did not return JSON") from error
    if validation.get("errors") != []:
        raise RuntimeError("R0.72S strict figure validation reported errors")
    expected_public = []
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = ROOT / publication["directory"] / f"{publication['stem']}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72S public {suffix} is absent or not byte-identical")
        expected_public.append(str(public.relative_to(ROOT)))
    if sorted(row.get("path") for row in publication.get("assets", [])) != sorted(expected_public):
        raise RuntimeError("R0.72S manifest does not enumerate the exact public assets")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72r.html").read_text(encoding="utf-8")
    replacements = (
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72S：incidence-preimage A2–A5 分类、restricted miniversal、pure-second 4/3/2 与 real-even 4/2/2 heat collisions。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72S｜exact singular strata 与两条 heat collision">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="局部 A2–A5 账本与两条全热路径已精确计数；global caustic 和 ED through collision 保持开放。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072s/fig-r072s-heat-collisions.png">'),
        (r'<title>.*?</title>', '<title>R0.72S｜exact singular strata 与两条 heat collision</title>'),
    )
    for index, (pattern, value) in enumerate(replacements):
        html = section(html, pattern, value, f"S note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.31", "/i18n-en.js?v=1.32", "S note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#incidence">incidence</a><a href="#versal">versal</a><a href="#a2">A2 path</a><a href="#a3">A3 path</a><a href="#local">局部分支</a><a href="#counts">计数口径</a><a href="#pde">PDE 边界</a><a href="#certificate">证书</a><a href="#literature">文献边界</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#scope">边界</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "S note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "S note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#incidence">01 · incidence preimages</a></li><li><a href="#versal">02 · restricted miniversal</a></li><li><a href="#a2">03 · pure-second A2</a></li><li><a href="#a3">04 · real-even A3</a></li><li><a href="#local">05 · 局部分支律</a></li><li><a href="#counts">06 · 计数口径</a></li><li><a href="#pde">07 · PDE 边界</a></li><li><a href="#certificate">08 · exact certificate</a></li><li><a href="#literature">09 · 文献边界</a></li><li><a href="#figure">10 · 正式附图</a></li><li><a href="#value">11 · 研究价值</a></li><li><a href="#scope">12 · 主张边界</a></li><li><a href="#next">13 · R0.72T</a></li><li><a href="#reproduce">14 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "S note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "S note article")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72S · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r'<footer>.*?</footer>', footer, "S note footer")
    if ARNOLD_1997 not in html or "4122-5_" + "8" in html:
        raise RuntimeError("R0.72S note must use the Arnol'd 1997 chapter _4 link")
    assert_clean(html, "R0.72S note")
    assert_mathjax_clean(html, "R0.72S note")
    (PUBLIC / "notes/r0-72s.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72r.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.31", "/i18n-en.js?v=1.32", "S recap i18n")
    html = section(html, r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72S 的 109 个节点；最新一节闭合 marked A2–A5 strata 与两条 exact heat collisions。">', "S recap description")
    html = section(html, r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72S｜R0.60 之后的研究回顾">', "S recap og title")
    html = section(html, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十八个阶段、109 个节点：从约化递推到 exact singular strata 与 heat collisions。">', "S recap og description")
    html = section(html, r'<title>.*?</title>', '<title>R0.61–R0.72S｜R0.60 之后的研究回顾</title>', "S recap title")
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72S · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72S 的 109 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72S</strong><p>收录节点：109</p><p>回顾截止时公开笔记：169</p><p>回顾截止节点：R0.72S</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "S recap hero")
    html = required(html, "02 · 108 节完整索引", "02 · 109 节完整索引", "S recap toc count")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2>
          <div class="metrics"><div class="metric"><strong>109</strong><span>R0.61–R0.72S 研究节点</span></div><div class="metric"><strong>71</strong><span>R0.70A–R0.72S 已公开版本</span></div><div class="metric"><strong>47</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div>
          <p>R0.00–R0.60 的内容保留在上一份阶段回顾中。后面的 109 个节点沿一般三维临界控制缺口推进；R0.70A–R0.72S 的 71 个版本已经公开，其中 47 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p>
        </section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "S recap result")
    phase = r'''            <article class="phase"><h3>R0.72L–R0.72S · strong-coupling、物理回填与 exact caustic-local geometry</h3>
              <p>R0.72L–O 保留 actual ledger、排除 action-poor dissipative launch，并完成物理回填。R0.72P 在 fixed real-collinear static-phase 1:2 正类上关闭传播门；R0.72Q 给 fixed-\(M\) arbitrary-static-phase sufficient cone；R0.72R 再构造该旧锥外的四实维 caustic-free compact core。</p>
              <p>R0.72S 对 fixed-first-harmonic \(1{:}2{:}3\) incidence preimages 给出 \(A_2,A_3,A_4,A_5\) 精确 ledger，并用 determinant \(5400\) 闭合 modulo constants 的 restricted miniversal。pure-second heat path 的 distinct count 为 \(4/3/2\)，real-even path 为 \(4/2/2\)；两者在碰撞时按重数都为四。</p>
              <p>这些是 local marked-strata 与两条 explicit path 的结论，不是 global caustic image classification。A3 path 只在 real-even slice 内横截；ED through collision、任意三维 continuation 与 Clay 正式问题仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/notes/r0-72n.html">R0.72N</a><a href="/notes/r0-72o.html">R0.72O</a><a href="/notes/r0-72p.html">R0.72P</a><a href="/notes/r0-72q.html">R0.72Q</a><a href="/notes/r0-72r.html">R0.72R</a><a href="/notes/r0-72s.html">R0.72S</a><a href="/assets/r072s/fig-r072s-heat-collisions.pdf">R0.72S 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072s">R0.72S 证书</a></div></article>'''
    html = section(html, r'            <article class="phase"><h3>R0\.72L–R0\.72R .*?</article>', phase, "S recap phase")
    html = required(html, "R0.61–R0.72R 的 108 节公开笔记", "R0.61–R0.72S 的 109 节公开笔记", "S recap node heading")
    node_r = '            <span class="node-ref"><a href="/notes/r0-72r.html">R0.72R</a><span class="node-state kind-closed">闭</span></span>\n'
    node_s = '            <span class="node-ref"><a href="/notes/r0-72s.html">R0.72S</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_r, node_r + node_s, "S recap node")
    retained = r'''            <li>R0.72S 的 marked singular-strata ledger：incidence preimage 止于 \(A_5\)，coefficient-derivative jet determinant 为 \(5400\)；pure-second \(A_2\) path 的 distinct count 是 \(4/3/2\)，real-even \(A_3\) path 是 \(4/2/2\)，且两者 crossing multiplicity 都为四。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "S recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>局部 caustic 类型已经精确化，穿越碰撞的 PDE 估计仍未建立</h2><p>截至 R0.72S，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 109 个节点或 71 个公开版本解释成 Clay 问题完成比例。</p><p>新的严格增量是 incidence-preimage \(A_2\)–\(A_5\) ledger、restricted miniversal，以及两条全时间 exact heat path 的 distinct/multiplicity count。完整 projected caustic、自交、chambers 与 ED through collision 仍开放。</p></section>''', "S recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72T 先处理 A2 spacetime normal form</h2><p>围绕 \(F'\sim-3\delta-(3/2)\xi^2\) 选择时空缩放，证明一个统一 nonautonomous model estimate；没有该估计前，不把 frozen \(\nu^{3/5}\) benchmark 外推成穿墙定理。</p></section>''', "S recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72S 的 71 节已公开；47 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。</p><p>R0.72S 分类的是 marked incidence preimages，并只对两条 explicit heat path 作全局计数。它没有给整个 \(\mathbb C^2\) caustic image 的 chamber classification；A3 只在 real-even slice 内横截，ED through collision 与 Clay 正式问题保持开放。</p></section>''', "S recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72r.html">保留 R0.72R 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72s.html">打开最新节点 R0.72S</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072s">查看 R0.72S 精确证书</a> · <a href="/assets/r072s/fig-r072s-heat-collisions.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72s.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72r.pdf">上一版累计回顾 PDF</a></p><p>完整节点索引保留 R0.69W、R0.70A 以后每个公开版本及其原始编号；状态标签只描述证据类型。</p></section>''', "S recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72S 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "S recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 109 or len(set(links)) != 109:
        raise RuntimeError(f"recap node index expected 109 unique links, got {len(links)}/{len(set(links))}")
    assert_clean(html, "R0.72S recap")
    assert_mathjax_clean(html, "R0.72S recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72s.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.31"', 'data-site-version="1.32"'),
        ("/i18n-en.js?v=1.31", "/i18n-en.js?v=1.32"),
        ("/site-refresh.js?v=1.31", "/site-refresh.js?v=1.32"),
        ("<strong>v1.31</strong>网页版本", "<strong>v1.32</strong>网页版本"),
        ("<strong>168</strong>公开研究笔记", "<strong>169</strong>公开研究笔记"),
        ("<strong>R0.72R</strong>最新研究节点", "<strong>R0.72S</strong>最新研究节点"),
        ("<strong>caustic-wall stratification and nonautonomous crossing</strong>当前方向", "<strong>nonautonomous enhanced dissipation through singular collision</strong>当前方向"),
        ("Research topology · R0.1–R0.72R", "Research topology · R0.1–R0.72S"),
        ("R0.70A–R0.72R：70 节已公开，46 节完整封存", "R0.70A–R0.72S：71 节已公开，47 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72R</span>', '<span class="route-range">R0.69P–R0.72S</span>'),
        ('aria-label="R0.69P–R0.72R"', 'aria-label="R0.69P–R0.72S"'),
        ("展开 78 篇公开笔记", "展开 79 篇公开笔记"),
        ("本站 R0.69P–R0.72R 路线", "本站 R0.69P–R0.72S 路线"),
        ("下一步 R0.72S：</strong>", "阶段后续 R0.72S（已完成）：</strong>"),
        ("综述 v1.31 · 2026-08-28", "综述 v1.32 · 2026-08-28"),
        ("上次综述 v1.30 · 2026-08-28", "上次综述 v1.31 · 2026-08-28"),
        ("/recap-r0-61-r0-72r.html", "/recap-r0-61-r0-72s.html"),
        ("/recap-r0-61-r0-72r.pdf", "/recap-r0-61-r0-72s.pdf"),
    ):
        html = required(html, old, new, f"S home {old}")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72S 已闭合 marked A2–A5 strata 与两条 exact heat collisions；下一关是 A2 spacetime normal form 上的非自治 model estimate。</span></div>', "S home focus")
    link_r = '<a class="milestone" href="/notes/r0-72r.html">R0.72R</a>'
    html = once(html, link_r, link_r + '\n                  <a class="milestone" href="/notes/r0-72s.html">R0.72S</a>', "S home route link")
    route_s = r'''              <p>R0.72S 把 R0.72R 的 incidence 继续分成 marked \(A_2,A_3,A_4,A_5\) strata；determinant \(5400\) 给 modulo constants 的 restricted miniversal。pure-second path 具有全局 \(4/3/2\) distinct count，real-even path 具有 \(4/2/2\)，crossing multiplicity 均为四。A3 只在 real-even slice 内横截；global caustic image 与 ED through collision 没有闭合。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_s + '              <details class="tree-notes" open>', "S home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "S home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72S · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 109 个节点；全站现有 169 篇公开研究笔记</h3>
            <p>累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72S 的完整逐节点索引。R0.72S 增加 incidence-preimage \(A_2\)–\(A_5\) ledger、restricted miniversal，以及 pure-second \(4/3/2\) 与 real-even \(4/2/2\) 两条 exact heat path。</p>
            <p>R0.70A–R0.72S 共 71 个版本已公开；47 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;局部 caustic 类型已经精确化；global image、ED through collision 与一般三维问题仍开放。</p>
            <p><a href="/recap-r0-61-r0-72s.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72s.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "S home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_S_CARD + '\n        </section>\n\n      </article>', "S home card")
    if html.count('data-release="r072s"') != 1:
        raise RuntimeError("home must contain exactly one R0.72S card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72S">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 79:
        raise RuntimeError("home current-route index must contain 79 note links")
    assert_clean(html, "R0.72S home")
    assert_mathjax_clean(html, "R0.72S home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.31", "/i18n-en.js?v=1.32"),
        ("本站 R0.69P–R0.72R 只列为研究笔记", "本站 R0.69P–R0.72S 只列为研究笔记"),
        ("/recap-r0-61-r0-72r.html", "/recap-r0-61-r0-72s.html"),
        ("文献综述 v1.31 · 2026-08-28", "文献综述 v1.32 · 2026-08-28"),
        ("累计回顾与 108 节索引", "累计回顾与 109 节索引"),
        ("打开 108 节完整索引", "打开 109 节完整索引"),
    ):
        html = required(html, old, new, f"S literature {old}")

    overview_old = r'''R0.72R 构造整体位于旧加权锥外的四实维 rational polydisc，闭合对所有 \(y\ge0\) 的全热路径 root localization，并在 \(0\le y\le1\) 闭合物理 \((\pi/48,144,240)\) shape contract 与 coefficient-uniform fixed-pattern commensurate 1:2:3 triangular affine-row enhanced dissipation；完整四维 caustic stratification 未完成。一般 Navier–Stokes 正则性仍开放。'''
    overview_new = r'''R0.72R 构造整体位于旧加权锥外的四实维 rational polydisc，闭合对所有 \(y\ge0\) 的全热路径 root localization，并在 \(0\le y\le1\) 闭合物理 \((\pi/48,144,240)\) shape contract 与 coefficient-uniform fixed-pattern commensurate 1:2:3 triangular affine-row enhanced dissipation；完整四维 caustic stratification 未完成。R0.72S 进一步把 fixed-first-harmonic \(1{:}2{:}3\) 的 marked incidence preimages 精确分为 \(A_2,A_3,A_4,A_5\)，用 determinant \(5400\) 证明 modulo constants 的 restricted miniversal，并对 pure-second \(A_2\) 与 real-even \(A_3\) 两条 heat path 分别给出 \(4/3/2\) 与 \(4/2/2\) 的 distinct count；后者只在 real-even slice 内横截。这里没有完成 global caustic image，也没有证明 ED through collision。一般 Navier–Stokes 正则性仍开放。'''
    html = once(html, overview_old, overview_new, "S literature route overview")

    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72S</b><strong>approach a declared caustic stratum</strong></header><p>在明确紧系数盒上分离 generic \\(A_2\\)、\\(A_3\\) 与更高余维 strata，并研究逼近或穿越指定 wall 的热路径。</p></div>'
    new_steps = r'''<div class="route-step closed"><header><b>R0.72S</b><strong>marked singular strata and two exact heat collisions</strong></header><p>fixed-first-harmonic \(1{:}2{:}3\) incidence preimages 止于 \(A_5\)，coefficient-derivative jet determinant 为 \(5400\)。pure-second \(A_2\) path 的 distinct count 是 \(4/3/2\)，real-even \(A_3\) path 是 \(4/2/2\)；两者只在碰撞时按重数计为四，A3 只在 real-even slice 内横截。<a href="/notes/r0-72s.html">研究笔记</a> <a href="/recap-r0-61-r0-72s.html">当前累计回顾</a> <a href="#r072s-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72T</b><strong>nonautonomous model estimate through the A2 collision</strong></header><p>缩放 \(F'\sim-3\delta-(3/2)\xi^2\) 的 spacetime normal form，先证明统一 model estimate，再检查向 exact heat path 的 perturbative transfer。</p></div>'''
    html = once(html, old_open, new_steps, "S literature route")

    boundary = r'''

          <h3 id="r072s-boundary">R0.72S 的 marked strata、热碰撞与 PDE 文献边界</h3>
          <p><a href="https://www.mathnet.ru/eng/rm4237">Arnol'd (1975)</a> 给出 \(A_k\) 与 versality 的标准局部框架；<a href="https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_4">Arnol'd (1997)</a> 已研究 degree-three maximal-real-critical region 的拓扑。R0.72S 的 determinant \(5400\) 只支持 critical-point geometry modulo additive constants 的 restricted miniversal，或 \(R^+\)-versal；包含函数值方向的 full \(A_5\) miniversal 还需一个常数参数。</p>
          <p><a href="https://doi.org/10.1016/j.aim.2023.109275">Voorhaar</a> 处理 complex Laurent coefficient space 中的 Morse discriminant；<a href="https://arxiv.org/abs/2411.02234">Esterov–Voorhaar</a> 仍把更高余维 Lyashko–Looijenga strata 列为问题。R0.72S 分类的是带 marked \(\phi\) 的 incidence preimages；投影后的自交、multisingularities 与全部 real complement chambers 没有由此自动得到。</p>
          <p><a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1016/j.jfa.2022.109522">Albritton–Beekie–Novack</a> 给 frozen finite-type profiles 的 stationary benchmarks。<a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He</a>、<a href="https://arxiv.org/abs/2501.16905">Benthaus–Nobili</a> 与 <a href="https://arxiv.org/abs/2603.14624">Benthaus–Coclite–Nobili</a> 的 nonautonomous results 保持临界点类型与数量；它们不覆盖这里的 creation、annihilation 或 multiplicity change。</p>
          <div class="boundary"><strong>R0.72S 的主张边界</strong><p>结论限于 fixed-first-harmonic \(\mathbb C^2\cong\mathbb R^4\) coefficient slice。pure-second path 在该切片中横截局部 codimension-one \(A_2\) branch，distinct count 为 \(4/3/2\)；real-even path 的 \(A_3\) 只在二维 real-even slice 内横截，distinct count 为 \(4/2/2\)。两条路径都只在碰撞时按重数计为四；碰撞后实临界点的总重数为二。没有完成 global caustic image、self-intersections、chambers、ED through collision 或一般三维 continuation。限定一手检索的 absence 不构成不存在性、新颖性或优先权证明；Clay 千禧年问题仍未解决。</p></div>'''
    match = re.search(r'(<h3 id="r072r-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("S literature boundary: expected one R0.72R boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "S literature boundary")

    references = '''            <li id="ref-108">V. I. Arnol'd. <a href="https://www.mathnet.ru/eng/rm4237"><em>Critical points of smooth functions and their normal forms</em></a>. Russian Math. Surveys 30 (1975), 1–75; <a href="https://doi.org/10.1070/RM1975v030n05ABEH001521">DOI</a>.</li>
            <li id="ref-109">A. Esterov and A. Voorhaar. <a href="https://arxiv.org/abs/2411.02234"><em>Basecondary polytopes</em></a>. Preprint, 2024.</li>
'''
    html = once(html, '          </ol>\n          <p class="source-note">资料截止：2026-08-28。', references + '          </ol>\n          <p class="source-note">资料截止：2026-08-28。', "S literature references")
    if ARNOLD_1997 not in html or "4122-5_" + "8" in html:
        raise RuntimeError("R0.72S literature must use the Arnol'd 1997 chapter _4 link")
    assert_clean(html, "R0.72S literature")
    assert_mathjax_clean(html, "R0.72S literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 169:
        raise RuntimeError(f"expected 169 public HTML notes after R0.72S, got {notes}")

    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    expected = {
        "latestCompletedRelease": "r072r",
        "siteVersion": "1.31",
        "publicHtmlNoteCount": 168,
        "postR060RecapNodeCount": 108,
        "nextRelease": "r072s",
        "latestReleaseGate": "tests/r072r-caustic-free-core-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072r-release.test.mjs",
        "postR070APublishedReleaseCount": 70,
        "postR070AFormalSealedReleaseCount": 46,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72R: {key}")
    stage = release.get("nextReleaseSourceStage", {})
    expected_stage = {
        "release": "r072s",
        "stage": "source-freeze",
        "publicationStatus": "pending-formal-certificate-figure-and-publication",
        "publicCountersAdvanced": False,
        "report": "research/r072s_report-source.md",
        "literatureAudit": "research/r072s_literature_audit.md",
        "gapMatrix": "research/r072s_gap_matrix.md",
        "independentAudit": "research/r072s_independent_audit.md",
        "producer": "research/r072s_exact_audit.py",
        "independentProducer": "research/r072s_independent_audit.mjs",
        "comparator": "research/r072s_compare_audits.py",
        "certificateDirectory": CERTIFICATE_RELATIVE,
        "figureDirectory": FIGURE_RELATIVE,
        "generator": "scripts/generate_r072s_release.py",
        "translationScript": "scripts/add-r072s-translations.mjs",
        "releaseGate": "tests/r072s-singular-strata-gate.test.mjs",
        "publicationTest": "tests/r072s-release.test.mjs",
    }
    if stage != expected_stage:
        raise RuntimeError("R0.72S source-stage manifest contract is missing or stale")
    release.update({
        "latestCompletedRelease": "r072s",
        "siteVersion": "1.32",
        "publicHtmlNoteCount": 169,
        "postR060RecapNodeCount": 109,
        "nextRelease": "r072t",
        "latestReleaseGate": "tests/r072s-singular-strata-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072s-release.test.mjs",
        "postR070APublishedReleaseCount": 71,
        "postR070AFormalSealedReleaseCount": 47,
        "legacyFormalFigureBacklogCount": 24,
    })
    del release["nextReleaseSourceStage"]
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (
        site.get("version") != "1.31"
        or site.get("latestRelease") != "R0.72R"
        or site.get("publicHtmlNoteCount") != 168
    ):
        raise RuntimeError("site-version is not at R0.72R")
    site.update({
        "version": "1.32",
        "latestRelease": "R0.72S",
        "publicHtmlNoteCount": 169,
        "publishedDate": "2026-08-28",
    })
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (
        inventory.get("latestPublishedRelease") != "r072r"
        or inventory.get("publishedReleaseCount") != 70
        or inventory.get("formalSealedReleaseCount") != 46
        or inventory.get("legacyFormalFigureBacklogCount") != 24
    ):
        raise RuntimeError("formal archive inventory is not at R0.72R")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072r" or "r072s" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72R")
        inventory[key].append("r072s")
    inventory.update({
        "latestPublishedRelease": "r072s",
        "publishedReleaseCount": 71,
        "formalSealedReleaseCount": 47,
        "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 71 or len(inventory["formalSealedReleases"]) != 47:
        raise RuntimeError("formal archive count mismatch after R0.72S")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in (
        "research-review.html",
        "literature-review.html",
        "notes/r0-72s.html",
        "recap-r0-61-r0-72s.html",
    ):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({
        "release": "R0.72S",
        "siteVersion": "1.32",
        "notes": 169,
        "recapNodes": 109,
        "published": 71,
        "formalSealed": 47,
        "legacyBacklog": 24,
        "phases": 28,
        "routeNotes": 79,
        "next": "R0.72T",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
