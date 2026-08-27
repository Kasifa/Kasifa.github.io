#!/usr/bin/env python3
"""Generate the fail-closed R0.72T publication from the R0.72S endpoint.

R0.72T is a formal negative-boundary release: it closes the exact A2
heat-polynomial normal form, scaling and audited method barriers, but it does
not claim the nonautonomous block contraction or a periodic transfer.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from generate_r072o_release import assert_clean, digest, once, required, section, verify_flat_hash_ledger
from generate_r072p_release import assert_mathjax_clean


ROOT = Path(os.environ.get("R072T_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_RELATIVE = "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model"
FIGURE_ID = "fig-r072t-a2-spacetime-model"
CERTIFICATE_RELATIVE = "research/certificates/r072t"


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72T · A2 SPACETIME NORMAL FORM · METHOD BOUNDARY</div>
        <h1>A2 碰撞的缩放已精确固定；<br>现有抽象混合路线仍到不了目标估计</h1>
        <p class="lead">我从 heat identity \(W_d=W_{xx}\) 出发，先把临界点导数芽积分回速度芽，再得到唯一的四项平衡：\(X=\kappa^{1/5}x\)、\(S=\kappa^{2/5}d\)，主模型由 heat polynomial \(H_3=X^3+6SX\) 控制。drift-only 模型有精确 \(a^2T^5/720\) 校准，完整相位有 uniform \(H^1\to H^{-1}\) inviscid mixing；但直接套用 CDZE 只给耗散时间指数 \(6/7\)，没有得到目标 \(3/5\)。因此 block contraction 与 periodic transfer 仍明确开放。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72T exact model 与方法边界完成</span><strong>A2 normal form closed; dissipative transfer open</strong><p>版本 v0.72T · 2026-08-28</p><p>derivative-to-primitive correction: CLOSED</p><p>unique \(1/5,2/5\) scaling: CLOSED</p><p>inviscid mixing and CDZE \(6/7\) barrier: CLOSED</p><p>weighted bracket step five: CLOSED</p><p>block contraction / periodic transfer: OPEN</p><p>Clay problem: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>模型已精确化；穿越碰撞的耗散定理尚未闭合</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · EXACT GERM</strong><p>heat identity 与 Hermite heat-polynomial 展开固定 A2 速度芽；使用临界点导数芽作为 transport potential 会丢失一次积分。</p></div>
            <div class="verdict-card true"><strong>THEOREM · UNIQUE SCALING</strong><p>漂移、三次空间项、扩散与时间导数同时平衡，只允许 \(X=\kappa^{1/5}x\)、\(S=\kappa^{2/5}d\)。</p></div>
            <div class="verdict-card true"><strong>NO-GO · BLACK-BOX MIXING</strong><p>uniform cubic-phase mixing 成立，但 CDZE 的一般转换在这里停在 \(q=6/7\)，弱于 A2 目标 \(3/5\)。</p></div>
            <div class="verdict-card false"><strong>OPEN · VISCOUS PROPAGATOR</strong><p>还没有 uniform nonautonomous block contraction，也没有把局部直线模型转移到周期 exact heat path。</p></div>
          </div>
        </section>

        <section id="primitive"><div class="section-no">01 / Derivative versus primitive</div><h2>临界点方程的芽不是速度势的芽</h2>
          <p>R0.72S 的未乘物理热因子的 profile 导数给出 fold；真正进入 Fourier-row 方程的 physical shear 还带 \(e^{-y_*}=1/2\)。因此这里的精确 leading derivative germ 是 \(W_x\sim-(3/2)d-(3/4)x^2\)。Fourier-mode transport 乘的是 \(W\)，还必须对 \(x\) 积分：</p>
          <div class="equation result">\[W(d,x)-W(d,0)\sim-\frac32dx-\frac14x^3.\]</div>
          <p>若直接把 derivative germ 放进 transport potential，会得到错误的空间次数与错误缩放。本节把这条 derivative-versus-primitive route 作为精确 no-go 记录。</p>
        </section>

        <section id="heat"><div class="section-no">02 / Exact heat polynomial</div><h2>heat identity 把时空 Taylor 系数锁在同一条链上</h2>
          <p>归一化局部变量满足 \(W_d=W_{xx}\)。用 heat polynomials \(H_j\) 组织展开后，证书核对的前三个奇阶块为</p>
          <div class="equation result">\[-\frac14H_3+\frac1{16}H_5-\frac1{160}H_7,\qquad H_3=X^3+6SX.\]</div>
          <p>这不是三个任意 Taylor monomial 的拼接；每个 \(H_j\) 自身满足 heat identity。正式附图同时展示 exact germ、scaled model 与两条方法边界。</p>
        </section>

        <section id="quadratic"><div class="section-no">02B / Wrong-model calibration</div><h2>quadratic potential 有自己的半次尺度，但它不是 A2 collision model</h2>
          <p>若误把模型写成 \(z_t+ik[A(t)+bx^2]z=\nu z_{xx}\)，\(A(t)\) 会被 scalar phase 完全消去。对 \(b\ne0\)，unitary dilation 只平衡 diffusion 与 quadratic potential，得到</p>
          <div class="equation result">\[\boxed{T_{\rm quad}\asymp(\nu|kb|)^{-1/2}}.\]</div>
          <p><a href="https://doi.org/10.1007/s00020-016-2303-4">Viola</a> 的 non-self-adjoint harmonic-oscillator semigroup 理论校准这个错误 quadratic model。它不处理 \(aSX+bX^3\)，也不能替代 A2 collision 的五次平衡。</p>
        </section>

        <section id="scaling"><div class="section-no">03 / Four-term balance</div><h2>两个分数指数由四项联立唯一决定</h2>
          <p>令 \(\kappa=\varepsilon_c/4\)。在局部 Fourier mode 中同时平衡时间导数、横向扩散、\(dx\) 漂移与 \(x^3\) transport，得到</p>
          <div class="equation result">\[\boxed{X=\kappa^{1/5}x,\qquad S=\kappa^{2/5}d}.\]</div>
          <p>在固定 scaled window 上，\(H_5\) 与 \(H_7\) corrections 分别带 \(\kappa^{-2/5}\) 与 \(\kappa^{-4/5}\)。对 physical velocity germ \(A\nu(t-t_*)x+Bx^3\) 和 horizontal Fourier mode \(k\ne0\)，drift calibration 回填为</p>
          <div class="equation result">\[\boxed{T\asymp |kA|^{-2/5}\nu^{-3/5}}.\]</div>
          <p>这个 bounded-chart 渐近不能直接延伸到全直线，因为高阶 heat polynomials 在 \(|X|\to\infty\) 时增长。</p>
        </section>

        <section id="model"><div class="section-no">04 / Parameter-free model</div><h2>缩放后只剩 A2 heat polynomial</h2>
          <p>消去符号、常数与纯时间相位后，局部问题归一到由 \(H_3=X^3+6SX\) 驱动的一维非自治 diffusion model。这个模型保留了碰撞前两个临界点、碰撞时二重临界点和碰撞后无局部临界点的同一时空几何。</p>
          <p>“parameter-free”只指局部 blow-up 后的主模型。向原周期路径回传时仍要控制 cutoff、远场、remainder、相邻 Fourier modes 与时间拼接。</p>
        </section>

        <section id="drift"><div class="section-no">05 / Exact drift calibration</div><h2>线性时漂可以完全解出，常数是 1/720</h2>
          <p>对 drift-only 方程，Fourier characteristic 给出任意起始时刻一致的精确最坏情形。优化初始 Fourier center 后，衰减指数含</p>
          <div class="equation result">\[\boxed{\frac{\nu a^2T^5}{720}}.\]</div>
          <p>这条恒等式校准 \(T^5\) 次数和窗口中心化常数，但它没有处理同阶三次势。因此它不能单独证明完整 A2 模型的 block contraction。</p>
        </section>

        <section id="mixing"><div class="section-no">06 / Inviscid mixing</div><h2>三阶 van der Corput 给 uniform \(H^1\to H^{-1}\)</h2>
          <p>任意时间块的 inviscid phase 都是 linear-plus-cubic polynomial；线性系数依赖块起点，三阶导数却由块长唯一控制。三阶 van der Corput 因而给出对起点一致的 \(T^{-1/3}\) mixing estimate。</p>
          <p>这一步是严格的 inviscid 结论。它不自动等于 viscous semigroup decay，尤其不能跳过 nonautonomous Duhamel error。</p>
        </section>

        <section id="cdze"><div class="section-no">07 / CDZE barrier</div><h2>一般 mixing-to-dissipation 定理在这里损失到 6/7</h2>
          <p><a href="https://doi.org/10.1002/cpa.21831">Coti Zelati–Delgadino–Elgindi</a> 把定量混合转成 enhanced dissipation。把本节的 \(H^{-1}\) mixing 指数代入其一般 black-box 估计，只得到时间尺度指数 \(q=6/7\)，没有达到 A2 scaling 预示的 \(3/5\)。这里的 \(6/7\) 只是指数映射给出的 method ceiling；全直线模型缺少 Poincaré gap 与 compact \(H^1\to L^2\) 嵌入，定理假设本身没有直接满足，因此不能把 \(6/7\) 写成已经得到的粘性衰减率。</p>
          <p>所以这篇文献支持的是一条可审计的方法障碍，不是穿越碰撞的目标定理。</p>
        </section>

        <section id="brackets"><div class="section-no">08 / Weighted brackets</div><h2>Hörmander bookkeeping 在加权意义下走到 step five</h2>
          <p>对扩散方向与非自治 transport 做 commutator bookkeeping，最坏碰撞点需要五级加权链才产生非退化乘法方向。这个 step-five ledger 与 \(1/5,2/5\) scaling 一致。</p>
          <p>bracket generation 是 hypoelliptic 结构证据，不等于带正确常数、正确时间方向和周期边界的 coercive estimate。</p>
        </section>

        <section id="persistent"><div class="section-no">09 / Persistent-form audit</div><h2>combined \(aSX+bX^3\) 对固定函数有精确恒等式，但还不是 solution observability</h2>
          <p>令 block 以 \(S=c\) 为中心，\(r\in[-T/2,T/2]\)，并定义</p>
          <div class="equation result">\[A_r(X)=(ac+3bX^2)r+\frac a2r^2,\qquad A_{\rm av}=\frac{aT^2}{24},\qquad D_r=\partial_X-iA_r.\]</div>
          <p>对每个固定 \(f\in H^1(\mathbb R)\)，odd/even cancellation 给出</p>
          <div class="equation result">\[\int_{-T/2}^{T/2}\!\|D_rf\|_2^2dr=T\|D_{\rm av}f\|_2^2+\int_{\mathbb R}\!\left[\frac{(ac+3bX^2)^2T^3}{12}+\frac{a^2T^5}{720}\right]|f(X)|^2dX.\]</div>
          <p>这是固定 \(f\) 的 persistent coercivity。真实解随 \(r\) 演化，所以该恒等式不是 evolving-solution observability，也不证明 blockContraction。</p>
        </section>

        <section id="boundary"><div class="section-no">10 / PDE boundary</div><h2>block contraction 与 periodic transfer 是两个不同缺口</h2>
          <p><strong>blockContraction=OPEN</strong>：尚缺参数自由模型在目标 \(T\asymp\nu^{-3/5}\) block 上的一致 \(L^2\) 收缩。</p>
          <p><strong>periodicTransfer=OPEN</strong>：即使模型闭合，仍须把局部直线估计与 exact periodic heat path、远场和 remainder 拼接。两者不能由 frozen profile 逐时估计替代。</p>
        </section>

        <section id="certificate"><div class="section-no">11 / Certificate</div><h2>双路证书只封存已声明的有限恒等式</h2>
          <p>精确 producer 与独立实现核对 heat-polynomial 系数、四项缩放线性系统、drift-only \(1/720\) 常数、mixing 指数代入、weighted bracket ledger 与 fixed-form identity。hash ledger 绑定同一 clean source commit。</p>
          <p>证书不声称证明 block contraction、periodic transfer 或一般三维正则性。</p>
        </section>

        <section id="literature"><div class="section-no">12 / Literature boundary</div><h2>stationary finite type、抽象 mixing 与 collision model 分开陈述</h2>
          <p><a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1016/j.jfa.2022.109522">Albritton–Beekie–Novack</a> 给 stationary finite-type benchmarks。<a href="https://doi.org/10.1002/cpa.21831">Coti Zelati–Delgadino–Elgindi</a> 给一般 mixing-to-dissipation 机制。<a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He</a> 处理保持临界点类型与数量的 time-dependent shear。<a href="https://doi.org/10.1007/s00020-016-2303-4">Viola</a> 只校准 quadratic wrong model。</p>
          <p>限定一手检索没有定位到覆盖本节 multiplicity-changing A2 collision 且给目标 \(3/5\) block contraction 的现成定理。这是 bounded-search absence，不是不存在性、新颖性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">13 / Journal figure</div><h2>正式附图把闭合结论与开放缺口分栏</h2>
          <p><img src="/assets/r072t/fig-r072t-a2-spacetime-model.svg" alt="R0.72T A2 spacetime normal form, scaling, and method barriers"></p>
          <p><a href="/assets/r072t/fig-r072t-a2-spacetime-model.pdf">下载 PDF</a> · <a href="/assets/r072t/fig-r072t-a2-spacetime-model.png">下载 PNG</a> · <a href="/assets/r072t/fig-r072t-a2-spacetime-model.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">14 / Research value</div><h2>这一节把“该证什么”与“现成工具能证什么”精确分开</h2>
          <p>R0.72T 的严格增量是 exact spacetime germ、唯一 scaling、parameter-free model、drift calibration、inviscid mixing 与两条独立的方法障碍。它把下一步从模糊的“穿墙 ED”缩成一个可检验的 block observability/coercivity 问题。</p>
          <p>对 Clay 问题的直接价值仍低。这里没有一般三维 continuation estimate，也没有有限时奇性或全局光滑性证明。</p>
        </section>

        <section id="next"><div class="section-no">15 / Next gate</div><h2>R0.72U：先证明参数自由模型的 cutoff observability</h2>
          <p>下一节检查能否对任意 interval center \(S_0\) 以统一常数证明</p>
          <div class="equation result">\[\|\chi u\|_{L^2_SL^2_X}\le C\left[\|\partial_X(\chi u)\|_{L^2_SL^2_X}+\|(\partial_S-i\sigma H_3)(\chi u)\|_{L^2_SH^{-1}_X}\right].\]</div>
          <p>还须用 endpoint control 把它升级为 evolving solutions 的 block contraction。只有这两步闭合后，才进入 periodic transfer。</p>
        </section>

        <section id="reproduce"><div class="section-no">16 / Reproduction</div><h2>报告、文献边界、独立审计、证书与正式附图</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072t_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072t_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072t_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072t_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072t">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model">正式附图包</a> · <a href="/notes/r0-72t.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72t.html">累计回顾</a> · <a href="/recap-r0-61-r0-72t.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72U</span><span class="tree-state current">下一检查点</span></div>
              <h3>direct observability for the parameter-free A2 model</h3>
              <p>检查 \(\|\chi u\|_{L^2L^2}\) 能否由 \(\|\partial_X(\chi u)\|_{L^2L^2}\) 与 equation residual 的 \(L^2_SH^{-1}_X\) 范数统一控制，再补 endpoint estimate；模型收缩闭合前不进入 periodic transfer。</p>
            </article>'''


HOME_T_CARD = r'''          <div class="task-one" id="r072t" data-release="r072t" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72T · 2026-08-28</p>
            <h3>A2 spacetime normal form 与方法边界已精确封存</h3>
            <p>heat identity 要求先把临界点导数芽积分回速度芽；四项联立唯一给出 \(X=\kappa^{1/5}x\)、\(S=\kappa^{2/5}d\)，主模型由 \(H_3=X^3+6SX\) 控制。</p>
            <p>drift-only 解给出精确 \(a^2T^5/720\) 和 physical \(T\asymp|kA|^{-2/5}\nu^{-3/5}\)；combined potential 对固定 \(f\) 有 persistent-form identity。但真实解随时间演化，直接 CDZE 转换也只到 \(q=6/7\)，都没有闭合 solution observability。</p>
            <p><strong>结论边界：</strong>&nbsp;block contraction 与 periodic transfer 仍开放；Clay 问题没有由此推进到解答。</p>
            <p><a href="/notes/r0-72t.html"><strong>阅读 R0.72T 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72t.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072t/fig-r072t-a2-spacetime-model.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072t">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072t_report-source.md">查看完整数学报告</a> ·
              <a href="/recap-r0-61-r0-72t.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72t.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72U：</strong>&nbsp;为参数自由 A2 模型建立直接 block observability。</p>
          </div>'''


def validate_inputs() -> None:
    for relative in (
        "research/r072t_report-source.md", "research/r072t_literature_audit.md",
        "research/r072t_gap_matrix.md", "research/r072t_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md", f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json", "public/notes/r0-72s.html",
        "public/recap-r0-61-r0-72s.html",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72T release input: {relative}")
    report = (ROOT / "research/r072t_report-source.md").read_text(encoding="utf-8")
    for token in ("W_d=W_{xx}", "-\\frac14H_3", "+\\frac1{16}H_5", "-\\frac1{160}H_7",
                  "\\kappa=\\frac{\\varepsilon_c}{4}", "X=\\kappa^{1/5}x",
                  "S=\\kappa^{2/5}d", "X^3+6SX", "720", "6/7",
                  "T\\asymp |kA|^{-2/5}\\nu^{-3/5}", "V(S,X)=aSX+bX^3",
                  "L^2_SH^{-1}_X", "missing observability",
                  "blockContraction=OPEN", "periodicTransfer=OPEN", "Clay=OPEN"):
        if token not in report:
            raise RuntimeError(f"R0.72T report missing stable token: {token}")
    literature = (ROOT / "research/r072t_literature_audit.md").read_text(encoding="utf-8")
    for token in ("10.1002/cpa.21831", "6/7", "bounded search", "blockContraction=OPEN"):
        if token not in literature:
            raise RuntimeError(f"R0.72T literature audit missing boundary token: {token}")
    independent = (ROOT / "research/r072t_independent_audit.md").read_text(encoding="utf-8")
    for token in ("1/720", "6/7", "1+1+1+2=5", "periodicTransfer=OPEN"):
        if token not in independent:
            raise RuntimeError(f"R0.72T independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72T certificate")
    verify_flat_hash_ledger(figure, "R0.72T figure")
    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    source_commit = certificate_manifest.get("sourceCommit")
    source_bindings = certificate_manifest.get("sourceBindings")
    if (certificate_manifest.get("status") != "formal" or
            re.fullmatch(r"[0-9a-f]{40}", str(source_commit)) is None or
            not isinstance(source_bindings, list) or not source_bindings):
        raise RuntimeError("R0.72T certificate manifest is not formally source-bound")
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if (crosscheck.get("status") != "passed" or
            crosscheck.get("temporaryUnsealedSourceAllowed") is not False or
            crosscheck.get("formalSourceReady") is not True or
            crosscheck.get("sourceCommit") != source_commit or
            crosscheck.get("sourceBindings") != source_bindings or
            not all(value is True for value in crosscheck.get("checks", {}).values())):
        raise RuntimeError("R0.72T crosscheck is not a formal all-passed seal")
    certificate_validation = subprocess.run(
        [sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if certificate_validation.returncode != 0:
        raise RuntimeError(
            "R0.72T formal certificate validation failed: " +
            (certificate_validation.stderr or certificate_validation.stdout)[-800:]
        )
    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    publication = manifest.get("publication", {})
    if (manifest.get("release") != "R0.72T" or manifest.get("figureId") != FIGURE_ID or
            manifest.get("status") != "formal" or manifest.get("qa", {}).get("status") != "passed" or
            manifest.get("qa", {}).get("visualInspectionExplicit") is not True or
            publication.get("publicCopiesComplete") is not True or
            publication.get("directory") != "public/assets/r072t" or publication.get("stem") != FIGURE_ID):
        raise RuntimeError("R0.72T figure manifest is not a complete formal seal")
    completed = subprocess.run([sys.executable, str(ROOT / "research/validate_figure_package.py"), str(figure)],
                               cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError("R0.72T strict figure validation failed: " + completed.stderr[-500:])
    validation = json.loads(completed.stdout)
    if validation.get("errors") != []:
        raise RuntimeError("R0.72T strict figure validation reported errors")
    expected_public = []
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = ROOT / publication["directory"] / f"{publication['stem']}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72T public {suffix} is absent or not byte-identical")
        expected_public.append(str(public.relative_to(ROOT)))
    if sorted(row.get("path") for row in publication.get("assets", [])) != sorted(expected_public):
        raise RuntimeError("R0.72T manifest does not enumerate the exact public assets")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72s.html").read_text(encoding="utf-8")
    for index, (pattern, value) in enumerate((
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72T：exact A2 spacetime normal form、唯一 1/5–2/5 缩放、1/720 校准与 CDZE 6/7 方法边界。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72T｜A2 spacetime normal form 与方法边界">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="模型与缩放已精确闭合；block contraction、periodic transfer 与 Clay 问题仍开放。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072t/fig-r072t-a2-spacetime-model.png">'),
        (r'<title>.*?</title>', '<title>R0.72T｜A2 spacetime normal form 与方法边界</title>'),
    )):
        html = section(html, pattern, value, f"T note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.32", "/i18n-en.js?v=1.33", "T note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#primitive">primitive</a><a href="#heat">heat polynomial</a><a href="#quadratic">wrong quadratic</a><a href="#scaling">缩放</a><a href="#model">模型</a><a href="#drift">1/720</a><a href="#mixing">混合</a><a href="#cdze">6/7 barrier</a><a href="#brackets">brackets</a><a href="#persistent">恒等式</a><a href="#boundary">PDE 边界</a><a href="#certificate">证书</a><a href="#literature">文献</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "T note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "T note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#primitive">01 · derivative / primitive</a></li><li><a href="#heat">02 · heat polynomial</a></li><li><a href="#quadratic">02B · wrong quadratic model</a></li><li><a href="#scaling">03 · four-term balance</a></li><li><a href="#model">04 · parameter-free model</a></li><li><a href="#drift">05 · drift calibration</a></li><li><a href="#mixing">06 · inviscid mixing</a></li><li><a href="#cdze">07 · CDZE barrier</a></li><li><a href="#brackets">08 · weighted brackets</a></li><li><a href="#persistent">09 · persistent form</a></li><li><a href="#boundary">10 · PDE boundary</a></li><li><a href="#certificate">11 · certificate</a></li><li><a href="#literature">12 · literature</a></li><li><a href="#figure">13 · journal figure</a></li><li><a href="#value">14 · research value</a></li><li><a href="#next">15 · R0.72U</a></li><li><a href="#reproduce">16 · reproduction</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "T note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "T note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72T · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "T note footer")
    assert_clean(html, "R0.72T note")
    assert_mathjax_clean(html, "R0.72T note")
    (PUBLIC / "notes/r0-72t.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72s.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.32", "/i18n-en.js?v=1.33", "T recap i18n")
    html = required(
        html,
        "      .print-page-break{display:block;break-before:page;page-break-before:always;height:1px}",
        "      .node-ref{break-inside:avoid;page-break-inside:avoid}\n"
        "      .print-page-break{display:block;break-before:page;page-break-before:always;height:1px}",
        "T recap print-safe node rows",
    )
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72T 的 110 个节点；最新一节固定 A2 spacetime normal form 与方法边界。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72T｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十九个阶段、110 个节点：从约化递推到 A2 spacetime model 与 observability 缺口。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.72T｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "T recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72T · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72T 的 110 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72T</strong><p>收录节点：110</p><p>回顾截止时公开笔记：170</p><p>回顾截止节点：R0.72T</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "T recap hero")
    html = required(html, "02 · 109 节完整索引", "02 · 110 节完整索引", "T recap toc")
    html = required(html, "01 · 二十八个研究阶段", "01 · 二十九个研究阶段", "T recap phase toc")
    html = required(html, "R0.60 之后的路线分成二十八个阶段", "R0.60 之后的路线分成二十九个阶段", "T recap phase heading")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2>
          <div class="metrics"><div class="metric"><strong>110</strong><span>R0.61–R0.72T 研究节点</span></div><div class="metric"><strong>72</strong><span>R0.70A–R0.72T 已公开版本</span></div><div class="metric"><strong>48</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div>
          <p>R0.00–R0.60 的内容保留在上一份阶段回顾中。后面的 110 个节点沿一般三维临界控制缺口推进；R0.70A–R0.72T 的 72 个版本已经公开，其中 48 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p>
        </section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "T recap result")
    new_phase = r'''            <article class="phase"><h3>R0.72T · A2 spacetime normal form 与 nonautonomous observability 缺口</h3>
              <p>R0.72T 把 R0.72S 的 pure-second collision 积分回速度芽，并用 heat-polynomial basis 固定 exact spacetime expansion。四项联立唯一给出 \(X=\kappa^{1/5}x\)、\(S=\kappa^{2/5}d\) 与主模型 \(H_3=X^3+6SX\)。</p>
              <p>drift-only 模型有精确 \(a^2T^5/720\) 与 physical \(T\asymp|kA|^{-2/5}\nu^{-3/5}\)；combined \(aSX+bX^3\) 对固定 \(f\) 有 persistent-form identity。Viola 校准的 quadratic half-scale 属于错误模型。直接 CDZE black box 只到 \(q=6/7\)，这些结论都没有闭合 evolving-solution block contraction。</p>
              <p>因此 blockContraction、periodicTransfer 与 Clay 问题仍开放。下一阶段转向参数自由模型的直接 observability。</p>
              <div class="links"><a href="/notes/r0-72t.html">R0.72T</a><a href="/assets/r072t/fig-r072t-a2-spacetime-model.pdf">R0.72T 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072t">R0.72T 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", new_phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "T recap phase")
    html = required(html, "R0.61–R0.72S 的 109 节公开笔记", "R0.61–R0.72T 的 110 节公开笔记", "T recap node title")
    node_s = '            <span class="node-ref"><a href="/notes/r0-72s.html">R0.72S</a><span class="node-state kind-closed">闭</span></span>\n'
    node_t = '            <span class="node-ref"><a href="/notes/r0-72t.html">R0.72T</a><span class="node-state kind-nogo">阻</span></span>\n'
    html = once(html, node_s, node_s + node_t, "T recap node")
    retained = r'''            <li>R0.72T 的 A2 spacetime ledger：exact derivative-to-primitive correction、heat-polynomial germ 与唯一 \(1/5,2/5\) scaling 已闭合；drift-only \(1/720\)、inviscid mixing、CDZE \(6/7\) barrier 和 weighted step-five brackets 已核对。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "T recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>A2 局部模型已经精确化，目标耗散估计仍未建立</h2><p>截至 R0.72T，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 110 个节点或 72 个公开版本解释成 Clay 问题完成比例。</p><p>新的严格增量是 exact spacetime germ、唯一 scaling、parameter-free model、drift calibration、inviscid mixing 与方法障碍。uniform block contraction 和 periodic transfer 仍开放。</p></section>''', "T recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72U 处理 parameter-free model observability</h2><p>目标是以 interval-center-uniform 常数用 \(\partial_X(\chi u)\) 的 \(L^2_SL^2_X\) 范数和 equation residual 的 \(L^2_SH^{-1}_X\) 范数控制 \(\chi u\) 的 \(L^2_SL^2_X\) 范数，并补齐 endpoint control；没有 uniform block contraction 前，不进入 periodic transfer。</p></section>''', "T recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72T 的 72 节已公开；48 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。</p><p>R0.72T 完成的是 exact local model 与明确负结果。它没有证明 block contraction、periodic transfer、一般三维 continuation 或 Clay 正式问题。</p></section>''', "T recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72s.html">保留 R0.72S 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72t.html">打开最新节点 R0.72T</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072t">查看 R0.72T 精确证书</a> · <a href="/assets/r072t/fig-r072t-a2-spacetime-model.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72t.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72s.pdf">上一版累计回顾 PDF</a></p><p>完整节点索引保留 R0.69W、R0.70A 以后每个公开版本及其原始编号；状态标签只描述证据类型。</p></section>''', "T recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72T 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "T recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 110 or len(set(links)) != 110:
        raise RuntimeError(f"recap node index expected 110 unique links, got {len(links)}/{len(set(links))}")
    phases = re.findall(r'<article class="phase">', html)
    if len(phases) != 29:
        raise RuntimeError(f"recap expected 29 phases, got {len(phases)}")
    assert_clean(html, "R0.72T recap")
    assert_mathjax_clean(html, "R0.72T recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72t.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.32"', 'data-site-version="1.33"'),
        ("/i18n-en.js?v=1.32", "/i18n-en.js?v=1.33"),
        ("/site-refresh.js?v=1.32", "/site-refresh.js?v=1.33"),
        ("<strong>v1.32</strong>网页版本", "<strong>v1.33</strong>网页版本"),
        ("<strong>169</strong>公开研究笔记", "<strong>170</strong>公开研究笔记"),
        ("<strong>R0.72S</strong>最新研究节点", "<strong>R0.72T</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72S", "Research topology · R0.1–R0.72T"),
        ("R0.70A–R0.72S：71 节已公开，47 节完整封存", "R0.70A–R0.72T：72 节已公开，48 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72S</span>', '<span class="route-range">R0.69P–R0.72T</span>'),
        ('aria-label="R0.69P–R0.72S"', 'aria-label="R0.69P–R0.72T"'),
        ("展开 79 篇公开笔记", "展开 80 篇公开笔记"),
        ("本站 R0.69P–R0.72S 路线", "本站 R0.69P–R0.72T 路线"),
        ("综述 v1.32 · 2026-08-28", "综述 v1.33 · 2026-08-28"),
        ("上次综述 v1.31 · 2026-08-28", "上次综述 v1.32 · 2026-08-28"),
        ("/recap-r0-61-r0-72s.html", "/recap-r0-61-r0-72t.html"),
        ("/recap-r0-61-r0-72s.pdf", "/recap-r0-61-r0-72t.pdf"),
    ):
        html = required(html, old, new, "T home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72T 已固定 A2 spacetime normal form、唯一缩放与现有方法边界；下一关是参数自由模型的直接 block observability。</span></div>', "T home focus")
    link_s = '<a class="milestone" href="/notes/r0-72s.html">R0.72S</a>'
    html = once(html, link_s, link_s + '\n                  <a class="milestone" href="/notes/r0-72t.html">R0.72T</a>', "T home route link")
    route_t = r'''              <p>R0.72T 先纠正 derivative-to-primitive 混用，再用 heat-polynomial basis 与四项平衡得到唯一 \(1/5,2/5\) scaling。Viola 的 quadratic half-scale 只校准错误模型；drift-only \(1/720\)、physical \(3/5\) 回填、combined fixed-\(f\) identity 与 inviscid mixing 已闭合，但它们都不是 evolving-solution observability。CDZE 只到 \(6/7\)，block contraction 与 periodic transfer 仍开放。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_t + '              <details class="tree-notes" open>', "T home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "T home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72T · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 110 个节点；全站现有 170 篇公开研究笔记</h3>
            <p>累计回顾现分二十九个问题阶段，并给出 R0.61–R0.72T 的完整逐节点索引。R0.72T 增加 exact A2 spacetime germ、唯一 scaling、quadratic wrong-model calibration、physical \(3/5\) 回填、combined fixed-\(f\) identity 与方法障碍。</p>
            <p>R0.70A–R0.72T 共 72 个版本已公开；48 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;参数自由局部模型已经确定；block observability、periodic transfer 与一般三维问题仍开放。</p>
            <p><a href="/recap-r0-61-r0-72t.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72t.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "T home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_T_CARD + '\n        </section>\n\n      </article>', "T home card")
    if html.count('data-release="r072t"') != 1:
        raise RuntimeError("home must contain exactly one R0.72T card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72T">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 80:
        raise RuntimeError("home current-route index must contain 80 note links")
    assert_clean(html, "R0.72T home")
    assert_mathjax_clean(html, "R0.72T home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.32", "/i18n-en.js?v=1.33"),
        ("本站 R0.69P–R0.72S 只列为研究笔记", "本站 R0.69P–R0.72T 只列为研究笔记"),
        ("/recap-r0-61-r0-72s.html", "/recap-r0-61-r0-72t.html"),
        ("文献综述 v1.32 · 2026-08-28", "文献综述 v1.33 · 2026-08-28"),
        ("累计回顾与 109 节索引", "累计回顾与 110 节索引"),
        ("打开 109 节完整索引", "打开 110 节完整索引"),
    ):
        html = required(html, old, new, "T literature " + old)
    html = once(
        html,
        "这里没有完成 global caustic image，也没有证明 ED through collision。一般 Navier–Stokes 正则性仍开放。",
        "这里没有完成 global caustic image，也没有证明 ED through collision。R0.72T 进一步固定 exact A2 spacetime germ 与唯一 scaling，核对 quadratic wrong-model calibration、physical 3/5 回填、combined fixed-f identity、inviscid mixing 和 CDZE 6/7 barrier；block contraction 与 periodic transfer 仍开放。一般 Navier–Stokes 正则性仍开放。",
        "T literature overview",
    )
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72T</b><strong>nonautonomous model estimate through the A2 collision</strong></header><p>缩放 \\(F\'\\sim-3\\delta-(3/2)\\xi^2\\) 的 spacetime normal form，先证明统一 model estimate，再检查向 exact heat path 的 perturbative transfer。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.72T</b><strong>exact A2 normal form and a sharp method boundary</strong></header><p>derivative-to-primitive correction 与 heat-polynomial basis 给唯一 \(1/5,2/5\) scaling；drift-only \(1/720\)、uniform inviscid mixing、CDZE \(6/7\) barrier 与 weighted step-five ledger 已闭合。block contraction 和 periodic transfer 保持开放。<a href="/notes/r0-72t.html">研究笔记</a> <a href="/recap-r0-61-r0-72t.html">当前累计回顾</a> <a href="#r072t-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72U</b><strong>direct observability for the parameter-free model</strong></header><p>用 \(\partial_X(\chi u)\) 的 \(L^2_SL^2_X\) norm 与 equation residual 的 \(L^2_SH^{-1}_X\) norm 控制 \(\chi u\) 的 spacetime \(L^2\) norm，再补 all-start endpoint control。</p></div>'''
    html = once(html, old_open, new_steps, "T literature route")
    boundary = r'''

          <h3 id="r072t-boundary">R0.72T 的 A2 spacetime model 与方法边界</h3>
          <p><a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1016/j.jfa.2022.109522">Albritton–Beekie–Novack</a> 给 stationary finite-type benchmarks。<a href="https://doi.org/10.1002/cpa.21831">Coti Zelati–Delgadino–Elgindi</a> 的一般 mixing-to-dissipation theorem 在本节 \(T^{-1/3}\) input 上只给 \(q=6/7\)，不闭合目标 \(3/5\)。<a href="https://doi.org/10.1007/s00020-016-2303-4">Viola</a> 校准 \((\nu|kb|)^{-1/2}\) quadratic scale，但不覆盖 combined \(aSX+bX^3\)。</p>
          <p><a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He</a> 的 time-dependent theorem 假设临界点数和非退化类型固定；它不覆盖 R0.72S–T 的 multiplicity-changing collision。限定一手检索没有定位到可直接替代 block contraction 与 periodic transfer 的定理。</p>
          <div class="boundary"><strong>R0.72T 的主张边界</strong><p>本节证明 exact local germ、唯一 scaling、drift calibration、uniform inviscid mixing 和两条方法障碍。weighted step-five brackets 只给结构 ledger，不给目标 coercivity。blockContraction=OPEN，periodicTransfer=OPEN，Clay=OPEN。bounded-search absence 不构成不存在性、新颖性或优先权证明。</p></div>'''
    match = re.search(r'(<h3 id="r072s-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("T literature expected R0.72S boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "T literature boundary")
    assert_clean(html, "R0.72T literature")
    assert_mathjax_clean(html, "R0.72T literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 170:
        raise RuntimeError(f"expected 170 public HTML notes after R0.72T, got {notes}")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    expected = {"latestCompletedRelease": "r072s", "siteVersion": "1.32", "publicHtmlNoteCount": 169,
                "postR060RecapNodeCount": 109, "nextRelease": "r072t",
                "latestReleaseGate": "tests/r072s-singular-strata-gate.test.mjs",
                "latestReleasePublicationTest": "tests/r072s-release.test.mjs",
                "postR070APublishedReleaseCount": 71, "postR070AFormalSealedReleaseCount": 47,
                "legacyFormalFigureBacklogCount": 24}
    for key, value in expected.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72S: {key}")
    stage = release.get("nextReleaseSourceStage", {})
    expected_stage = {
        "release": "r072t",
        "stage": "source-freeze",
        "publicationStatus": "pending-formal-certificate-figure-and-publication",
        "publicCountersAdvanced": False,
        "report": "research/r072t_report-source.md",
        "literatureAudit": "research/r072t_literature_audit.md",
        "gapMatrix": "research/r072t_gap_matrix.md",
        "independentAudit": "research/r072t_independent_audit.md",
        "producer": "research/certificates/r072t/generate_certificate.py",
        "independentProducer": "research/certificates/r072t/independent_recompute.py",
        "comparator": "research/certificates/r072t/validate_certificate.py",
        "certificateDirectory": CERTIFICATE_RELATIVE,
        "figureDirectory": FIGURE_RELATIVE,
        "generator": "scripts/generate_r072t_release.py",
        "translationScript": "scripts/add-r072t-translations.mjs",
        "releaseGate": "tests/r072t-a2-spacetime-gate.test.mjs",
        "publicationTest": "tests/r072t-release.test.mjs",
    }
    if stage != expected_stage:
        raise RuntimeError("R0.72T source-stage manifest contract is missing, stale, or has extra fields")
    release.update({"latestCompletedRelease": "r072t", "siteVersion": "1.33", "publicHtmlNoteCount": 170,
                    "postR060RecapNodeCount": 110, "nextRelease": "r072u",
                    "latestReleaseGate": "tests/r072t-a2-spacetime-gate.test.mjs",
                    "latestReleasePublicationTest": "tests/r072t-release.test.mjs",
                    "postR070APublishedReleaseCount": 72, "postR070AFormalSealedReleaseCount": 48,
                    "legacyFormalFigureBacklogCount": 24})
    del release["nextReleaseSourceStage"]
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.32", "R0.72S", 169):
        raise RuntimeError("site-version is not at R0.72S")
    site.update({"version": "1.33", "latestRelease": "R0.72T", "publicHtmlNoteCount": 170,
                 "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
            inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r072s", 71, 47, 24):
        raise RuntimeError("formal archive inventory is not at R0.72S")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072s" or "r072t" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72S")
        inventory[key].append("r072t")
    inventory.update({"latestPublishedRelease": "r072t", "publishedReleaseCount": 72,
                      "formalSealedReleaseCount": 48, "legacyFormalFigureBacklogCount": 24})
    if len(inventory["publishedReleases"]) != 72 or len(inventory["formalSealedReleases"]) != 48:
        raise RuntimeError("formal archive count mismatch after R0.72T")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-72t.html", "recap-r0-61-r0-72t.html"):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({"release": "R0.72T", "siteVersion": "1.33", "notes": 170,
                      "recapNodes": 110, "published": 72, "formalSealed": 48,
                      "legacyBacklog": 24, "phases": 29, "routeNotes": 80,
                      "next": "R0.72U"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
