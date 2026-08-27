#!/usr/bin/env python3
"""Generate the deterministic R0.72L GitHub Pages release from site v1.24."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: missing {old}")
    return text.replace(old, new)


def section(text: str, pattern: str, new: str, label: str) -> str:
    updated, count = re.subn(pattern, lambda _match: new, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return updated


def assert_clean(text: str, label: str) -> None:
    bad = [
        (index, ord(character))
        for index, character in enumerate(text)
        if ord(character) < 32 and character not in "\t\n\r"
    ]
    if bad:
        raise RuntimeError(f"{label}: forbidden control characters {bad[:8]}")


HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72L · MODERATE STRONG COUPLING · ENSTROPHY-AWARE LEDGER</div>
        <h1>小耦合不是共同频带的真实边界；<br>极强耦合缺口现在可以准确写出</h1>
        <p class="lead">我把实际涡量对比 \(K=\mathcal R_Y\) 和实际 critical-log action \(x=\Theta Q_*\) 保留在分母里，并在长度 \((R^2+gB)^{-1}\) 的局部窗口构造精确目标根。完整复根账本因此从 \(gB/R^2\ll1\) 推进到一个随 \(R\) 增长的中强耦合区间。区间上沿只给统一有界；只有 little-o 子区间才给趋零。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72L 定理完成</span><strong>moderate strong coupling closes in the common band</strong><p>版本 v0.72L · 2026-08-27</p><p>coupling-uniform full-lattice upper bound: CLOSED</p><p>local exact root and action floor: CLOSED</p><p>moderate strong window: CLOSED</p><p>extreme strong coupling: OPEN</p><p>一般三维正则性：OPEN</p></div>
    </div></header>'''


ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Four decisions</div><h2>我得到一个真正越过扰动区的窗口，但没有把任意强耦合写成已解决</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · ALL COUPLINGS</strong><p>完整 Fourier 格点上，complete-root ledger 对每个 \(\varepsilon=gB/R^2&gt;0\) 都有一个保留实际 \(K\) 与 \(x\) 的统一上界。</p></div>
            <div class="verdict-card true"><strong>THEOREM · LOCAL FLOOR</strong><p>对声明的 phase-aligned、row-aligned、exact-corrected 构造族，在 \(\tau=c_*/(R^2+gB)\) 上产生精确根并保留目标行；这个 action floor 允许 common-band global exposure scale \(\varepsilon\) 任意大。</p></div>
            <div class="verdict-card true"><strong>CLOSED · MODERATE STRONG</strong><p>当 \(1\lesssim\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\) 时，完整物理账本统一有界；little-o 子区间内才趋零。</p></div>
            <div class="verdict-card false"><strong>OPEN · EXTREME STRONG</strong><p>超过该窗口后，仍缺一个 full-lattice enstrophy/action lower bound 或更强的 cubic mixing estimate。</p></div>
          </div>
        </section>

        <section id="parameter"><div class="section-no">01 / Invariant parameter</div><h2>strong coupling 应由 common-band exposure scale 定义</h2>
          <p>共同频带中的尺度不变量及其单边 exposure 比较是</p>
          <div class="equation result">\[
            \varepsilon:=\frac{gB}{R^2},\qquad g=|\delta|a,\qquad
            |\delta|\int_0^\infty\|V_w(x)\|\,dx\lesssim\varepsilon,
            \qquad
            p=\frac{\sqrt N}{B}\in(0,1].
          \]</div>
          <p>这里只使用 \(\|V_w(x)\|\) 上界给出的单边比较，不假设反向估计；实际 Duhamel exposure 可以更小。同时改变 shear coefficient 与 \(\delta\) 的表示方式不会改变动力学，所以 bare \(\delta\) 不能定义强耦合。这里 \(B\) 记录 multiplier coherence，distinct integer carriers 给出 \(p\gtrsim R^{-1/2}\)。</p>
        </section>

        <section id="ledger"><div class="section-no">02 / Coupling-uniform ledger</div><h2>完整账本保留实际涡量对比和实际作用量</h2>
          <p>令 \(K=\mathcal R_Y(I)\)、\(x=\Theta Q_*^I\)、\(L_R=1+\log R\)，并定义</p>
          <div class="equation result">\[
          \begin{aligned}
          U_0&=\varepsilon^{4/3}p^{4/3},&
          W&=\varepsilon^{1/3}p^{1/3}R^{-1/3}L_R^{-1/2},\\
          U&=\varepsilon^{7/3}p^{4/3},&
          V&=\varepsilon^{1/3}p^{1/3}R.
          \end{aligned}
          \]</div>
          <div class="equation result">\[
            \boxed{\frac{\mathcal J_{\rm all}}{D^{1/3}\Lambda_{1,*}}
            \le C\left[\frac{U_0}{K+x}
            +W\frac{\sqrt x}{K+x}
            +\frac{\min\{U,Vx\}}{K+x}\right].}
          \]</div>
          <p>这个上界来自 R0.72K 的 complete-root sampling、R0.72H 的 mixed row 和 R0.72J 的 hybrid cubic minimum。它不要求 \(\varepsilon\ll1\)，但强耦合下只给单边 root lift，不能写成双边等价。</p>
        </section>

        <section id="physical"><div class="section-no">03 / Why the denominator pays</div><h2>\(\Lambda_{1,*}\) 至少包含 \(K+x\)</h2>
          <p>固定 decoupled background 给出 \(\inf_IY\gtrsim E_{\rm phys}\)，所以每个 root atom 至多为 \(C\Theta|h|^2\)。另一方面，target Fourier sector 给 action lower bound，而 \(\inf Y\le Y(0)\lesssim E_{\rm phys}\)。两条方向不能混用，但合起来得到</p>
          <div class="equation result">\[
            \boxed{\mathcal J_{\rm all}\lesssim\Theta G_{\rm all}^{\rm ex},
            \qquad \Lambda_{1,*}\gtrsim K+x.}
          \]</div>
          <p>如果 \(K\gtrsim\varepsilon^{7/3}p^{4/3}\)，enstrophy contrast 本身足以支付最强 cubic term。这只是充分分支；本节没有证明级联必然迫使 \(K\) 这样增长。</p>
        </section>

        <section id="floor"><div class="section-no">04 / Local exact root</div><h2>全局 exposure scale 很大时，一个 coupling-time 窗口仍然很小</h2>
          <p>对 phase-aligned、row-aligned launch 与固定背景，令 \(\Omega=R^2+gB\)、\(\tau=c_*/\Omega\)。在这段时间里，heat change 与 coupling exposure 都是 \(O(c_*)\)。用 target coordinate 的一坐标线性 correction 可得</p>
          <div class="equation result">\[
            P_0F(\tau)=0,\qquad
            \frac{|\zeta|}{\sqrt N}\lesssim
            c_*\frac{\varepsilon p}{1+\varepsilon},\qquad
            |h(x)|\ge caN\quad(0\le x\le\tau).
          \]</div>
          <p>因此 \(Q_*^I\gtrsim a^2N^2\Omega^{-2/3}[1+\log(2+\Omega)]\)，并且</p>
          <div class="equation result">\[
            \boxed{x\ge Z:=c\varepsilon^2p^2R^{2/3}(1+\varepsilon)^{-2/3}
            [1+\log(2+R^2(1+\varepsilon))].}
          \]</div>
          <p>这个 floor 只属于带固定背景、相位与行对齐、exact-corrected 的构造族，不是任意初值的结论。</p>
        </section>

        <section id="window"><div class="section-no">05 / Moderate strong window</div><h2>从 fixed smallness 推进到随频率增长的强耦合区间</h2>
          <div class="equation result">\[
            \boxed{1\lesssim\varepsilon
            \lesssim p^{2/3}R^{2/3}(1+\log R).}
          \]</div>
          <p>在这个区间内，first-root 和 mixed-row 项趋零，cubic 项在上沿保持 \(O(1)\)。如果 \(\varepsilon=o(p^{2/3}R^{2/3}(1+\log R))\)，三项才全部趋零。</p>
          <p>当 \(B\asymp\sqrt N\) 时，窗口可达 \(R^{2/3}\log R\)；最相干的 \(B\asymp N\)、\(N\asymp R\) 情形仍可达 \(R^{1/3}\log R\)。</p>
        </section>

        <section id="galerkin"><div class="section-no">06 / Galerkin warning</div><h2>三模截断会线性增长，但它从第一个 coupling time 就漏掉高壳层</h2>
          <p>单 carrier 的三模 projected ODE 有 \(\theta_y=\sigma e^{-y}-\tfrac12\sin2\theta\)。因此 root count、root-slope mass 与 cubic row 都可按 \(\sigma\) 线性增长。这个 countertheorem 对 projected ODE 是严格的。</p>
          <p>完整卷积却没有非零有限 Fourier-support invariant subspace。对 \(u_R=(e_R+e_{-R})/\sqrt2\)，</p>
          <div class="equation result">\[
            W_Ru_R=-i\sqrt2a\,e_0-
            \frac{ia}{\sqrt2}(e_{2R}+e_{-2R}),\qquad
            \frac{\|(I-P)W_Ru_R\|}{\|PW_Ru_R\|}=\frac1{\sqrt2}.
          \]</div>
          <p>所以 Galerkin 轨道在大量旋转之前已经产生 \(O(1)\) 外壳层质量。它不是 full Fourier lattice，也不能作为 full triangular PDE 的反例。</p>
        </section>

        <section id="multiscale"><div class="section-no">07 / Multiscale raw interface</div><h2>dyadic Schur estimate 消除了额外的 shell-count 因子</h2>
          <div class="equation result">\[
            \boxed{\mathcal C_\times\lesssim|\delta|E_0
            \left(\sum_j\frac{\sigma_j^4}{R_j^2}\right)^{1/2}
            \left(\sum_k\frac{\beta_k^2}{R_k^2}\right)^{1/2}.}
          \]</div>
          <p>核 \(R_jR_k/(R_j^2+R_k^2)\lesssim2^{-|j-k|}\) 使常数与 shell 数无关。但显式 shell moments 尚未被一个 global \(D^{1/3}\Lambda_{1,*}\) 无条件吸收。</p>
        </section>

        <section id="audit"><div class="section-no">08 / Two-route audit</div><h2>幂次、窗口与 Galerkin 边界分别核对</h2>
          <div class="audit-grid">
            <div class="audit-card"><strong>PRODUCER · PASS</strong><p>生产证书逐项重建 \(U_0,W,U,V,H,Z\)，扫描窗口内外的归一化项，并数值核对 projected polar ODE。</p><p class="mini-kpi">deterministic · finite corroboration</p></div>
            <div class="audit-card"><strong>INDEPENDENT · PASS WITH QUALIFICATIONS</strong><p>独立路线重新推导 root/action lift 的不等式方向、局部 correction 与 little-o 边界；它明确禁止把上沿 \(O(1)\) 写成衰减。</p><p class="mini-kpi"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_independent_audit.md">独立逐式审计</a></p></div>
          </div>
        </section>

        <section id="figure"><div class="section-no">09 / Journal figure</div><h2>正式附图分开标出新窗口、三项付款与 Galerkin 泄漏</h2>
          <p><img src="/assets/r072l/fig-r072l-strong-window.svg" alt="R0.72L moderate strong-coupling window and Galerkin non-embedding formal figure"></p>
          <p><a href="/assets/r072l/fig-r072l-strong-window.pdf">下载 PDF</a> · <a href="/assets/r072l/fig-r072l-strong-window.png">下载 PNG</a> · <a href="/assets/r072l/fig-r072l-strong-window.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">10 / Research value</div><h2>价值在于扩大严格闭合区，并把下一缺口压成一个公式</h2>
          <p>R0.72K 的 small-coupling 假设并非共同频带路线的真实终点。R0.72L 证明完整根账本能进入一个随 \(R\) 扩大的强耦合区间，同时把更极端区域的第一未付款项准确分离出来。</p>
          <p>这仍是特殊 exact 2.5D class 内的证明机制压力测试。只有把账本连接到 \(L_t^\infty L_x^3\) 或另一个一般三维 continuation criterion，才会对 Clay 问题形成直接推进。</p>
        </section>

        <section id="next"><div class="section-no">11 / Next gate</div><h2>R0.72M：量化 extreme strong coupling 的 full-lattice cascade</h2>
          <p>下一步要证明 enstrophy contrast、all-time action 或 true cubic mixing 中至少一个足以支付 \(\varepsilon^{7/3}p^{4/3}\)。不能再用 finite Galerkin 轨道替代完整卷积链。</p>
        </section>

        <section id="claims"><div class="section-no">12 / Claim boundary</div><h2>一般 Navier–Stokes 问题仍然开放</h2>
          <p>本节没有闭合任意强耦合，没有完成 multiscale physical absorption，也没有给出一般三维 continuation criterion、有限时奇性或全局光滑性证明。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="reproduce"><div class="section-no">13 / Reproduction</div><h2>报告、双路证书、附图与累计回顾</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_independent_audit.md">独立审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072l">双路机器证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072l-strong-window/fig-r072l-strong-window">正式附图包</a> · <a href="/notes/r0-72l.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72l.html">累计回顾</a> · <a href="/recap-r0-61-r0-72l.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


def build_note() -> None:
    html = (PUBLIC / "notes" / "r0-72k.html").read_text(encoding="utf-8")
    html = section(html, r'<meta name="description" content=".*?">',
                   '<meta name="description" content="研究笔记 R0.72L：保留实际 enstrophy contrast 与 critical-log action，把 complete-root ledger 推进到随 R 增长的 moderate strong-coupling window，并分离 extreme strong remainder。">', "note description")
    html = section(html, r'<meta property="og:title" content=".*?">',
                   '<meta property="og:title" content="R0.72L｜小耦合不是真实边界">', "note og title")
    html = section(html, r'<meta property="og:description" content=".*?">',
                   '<meta property="og:description" content="完整 Fourier 格点的中强耦合闭合、局部 action floor 与 Galerkin 非嵌入边界。">', "note og description")
    html = section(html, r'<meta property="og:image" content=".*?">',
                   '<meta property="og:image" content="https://kasifa.github.io/assets/r072l/fig-r072l-strong-window.png">', "note og image")
    html = section(html, r'<title>.*?</title>', '<title>R0.72L｜小耦合不是真实边界</title>', "note title")
    html = required(html, "/i18n-en.js?v=1.24", "/i18n-en.js?v=1.25", "note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#parameter">参数</a><a href="#ledger">账本</a><a href="#physical">物理量</a><a href="#floor">局部根</a><a href="#window">强耦合窗</a><a href="#galerkin">Galerkin</a><a href="#multiscale">多尺度</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "note nav")
    html = section(html, r'    <header class="hero">.*?</header>', HERO, "note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 四句判断</a></li><li><a href="#parameter">01 · 强耦合参数</a></li><li><a href="#ledger">02 · 统一账本</a></li><li><a href="#physical">03 · 物理分母</a></li><li><a href="#floor">04 · 局部精确根</a></li><li><a href="#window">05 · 中强耦合窗</a></li><li><a href="#galerkin">06 · Galerkin 边界</a></li><li><a href="#multiscale">07 · 多尺度接口</a></li><li><a href="#audit">08 · 双路审计</a></li><li><a href="#figure">09 · 正式附图</a></li><li><a href="#value">10 · 研究价值</a></li><li><a href="#next">11 · R0.72M</a></li><li><a href="#claims">12 · 主张边界</a></li><li><a href="#reproduce">13 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "note toc")
    html = section(html, r'      <article>.*?</article>', ARTICLE, "note article")
    html = section(html, r'<footer>.*?</footer>',
                   '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72L · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>',
                   "note footer")
    assert_clean(html, "R0.72L note")
    (PUBLIC / "notes" / "r0-72l.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72k.html").read_text(encoding="utf-8")
    changes = [
        ("R0.61 到 R0.72K 的 101 个研究节点", "R0.61 到 R0.72L 的 102 个研究节点"),
        ("二十七个阶段、101 个节点", "二十八个阶段、102 个节点"),
        ("/i18n-en.js?v=1.24", "/i18n-en.js?v=1.25"),
        ("收录节点：101", "收录节点：102"),
        ("回顾截止时公开笔记：161", "回顾截止时公开笔记：162"),
        ("回顾截止节点：R0.72K", "回顾截止节点：R0.72L"),
        ("01 · 二十七个研究阶段", "01 · 二十八个研究阶段"),
        ("02 · 101 节完整索引", "02 · 102 节完整索引"),
        ("<strong>101</strong><span>R0.61–R0.72K 研究节点</span>", "<strong>102</strong><span>R0.61–R0.72L 研究节点</span>"),
        ("<strong>63</strong><span>R0.70A–R0.72K 已公开版本</span>", "<strong>64</strong><span>R0.70A–R0.72L 已公开版本</span>"),
        ("<strong>39</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>40</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("<strong>27</strong><span>按问题划分的研究阶段</span>", "<strong>28</strong><span>按问题划分的研究阶段</span>"),
        ("后面的 101 个节点", "后面的 102 个节点"),
        ("R0.70A–R0.72K 的 63 个版本已经公开；其中 39 个", "R0.70A–R0.72L 的 64 个版本已经公开；其中 40 个"),
        ("R0.60 之后的路线分成二十七个阶段", "R0.60 之后的路线分成二十八个阶段"),
        ("R0.61–R0.72K 的 101 节公开笔记", "R0.61–R0.72L 的 102 节公开笔记"),
        ("R0.61–R0.72K", "R0.61–R0.72L"),
        ("/recap-r0-61-r0-72k", "/recap-r0-61-r0-72l"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"recap {old}")
    html = section(html, r'<meta name="description" content=".*?">',
                   '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72L 的 102 个研究节点；最新一节把共同频带推进到随 R 增长的中强耦合窗口。">', "recap description")
    html = section(html, r'<meta property="og:description" content=".*?">',
                   '<meta property="og:description" content="二十八个阶段、102 个节点：从约化递推和时间迹账本，到 critical-log candidate，再到中强耦合闭合。">', "recap og description")
    phase_k_end = '<div class="links"><a href="/notes/r0-72k.html">R0.72K</a><a href="/figures/r0-72k-directional-roots.pdf">R0.72K 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072k">R0.72K 证书</a></div></article>'
    phase_l = r'''
            <article class="phase"><h3>R0.72L · 中强耦合闭合与极强耦合余项</h3>
              <p>我把 actual enstrophy contrast \(K\) 与 actual action \(x\) 留在 complete-root denominator 中，得到对所有 \(\varepsilon=gB/R^2&gt;0\) 有效的 full-lattice upper bound。对带固定背景、phase-aligned、row-aligned、exact-corrected 的构造族，局部精确根再给出 \(x\ge Z\)。</p>
              <p>这把 closure 推进到 \(1\lesssim\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\)。上沿只给 \(O(1)\)，little-o 子区间才趋零。三模 Galerkin 的线性增长不能嵌入完整格点；extreme strong coupling 仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/assets/r072l/fig-r072l-strong-window.pdf">R0.72L 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072l">R0.72L 证书</a></div></article>'''
    html = once(html, phase_k_end, phase_k_end + phase_l, "recap L phase")
    node_k = '            <span class="node-ref"><a href="/notes/r0-72k.html">R0.72K</a><span class="node-state kind-closed">闭</span></span>\n'
    node_l = '            <span class="node-ref"><a href="/notes/r0-72l.html">R0.72L</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_k, node_k + node_l, "recap L node")
    kept = r'''            <li>R0.72L 的 enstrophy-aware strong window：对所有 coupling strengths 保留 \(K=\mathcal R_Y\) 与 \(x=\Theta Q_*\) 的 complete-root upper bound；带固定背景、phase-aligned、row-aligned、exact-corrected 的构造族给出 \(x\ge Z\)，把 common-band closure 推进到 \(\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\)。上沿只统一有界，little-o 子区间趋零；extreme strong coupling 仍开放。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", kept + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained L")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>小耦合不再是共同频带的边界，但极强耦合仍没有付款</h2>
          <p>截至 R0.72L，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 102 个节点或 64 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>新的严格结果是 coupling-uniform enstrophy-aware upper bound、允许 global exposure scale 任意大的 local action floor，以及一个随 \(R\) 增长的 moderate strong-coupling closure。</p>
          <p>窗口上沿只保证归一化账本为 \(O(1)\)。只有 \(\varepsilon=o(p^{2/3}R^{2/3}(1+\log R))\) 才得到衰减；极强耦合和 multiscale physical absorption 继续开放。</p>
        </section>''', "recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72M 量化 extreme strong coupling 的 full-lattice cascade</h2>
          <p>下一步需要证明 enstrophy contrast、all-time action 或 improved cubic mixing 至少有一个支付 \(\varepsilon^{7/3}p^{4/3}\)。</p>
          <p>finite Galerkin 不能替代完整卷积链；separated heat windows 的 multiscale Schur ledger 保留为并列接口。</p>
        </section>''', "recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72L 的 64 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，40 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。</p>
          <p>R0.72L 限于 exact finite triangular common-band class；local floor 还要求固定背景、phase alignment、row alignment 与 exact correction。它没有闭合 extreme strong coupling、multiscale physical payment 或一般三维 Navier–Stokes 全局光滑性；Clay 正式问题仍然开放。</p>
        </section>''', "recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72k.html">保留 R0.72K 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72l.html">打开最新节点 R0.72L</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072l">查看 R0.72L 双路证书</a> · <a href="/assets/r072l/fig-r072l-strong-window.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72l.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72k.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>''', "recap reproduce")
    assert_clean(html, "R0.72L recap")
    (PUBLIC / "recap-r0-61-r0-72l.html").write_text(html, encoding="utf-8")


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72M</span><span class="tree-state current">下一检查点</span></div>
              <h3>extreme strong-coupling cascade ledger</h3>
              <p>量化 full-lattice enstrophy contrast、all-time action 或 improved cubic mixing，支付 R0.72L 留下的 \(\varepsilon^{7/3}p^{4/3}\) 余项；multiscale Schur ledger 保留为并列接口。</p>
            </article>'''


HOME_RECAP = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72L · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 102 个节点；全站现有 162 篇公开研究笔记</h3>
            <p>累计回顾现在分为二十八个问题阶段，完整覆盖 R0.61–R0.72L。我保留 R0.72E–K 的 critical-log、mixed/cubic 与 complex-root 路线，并追加 R0.72L 的 enstrophy-aware moderate strong-coupling closure。R0.70A–R0.72L 共 64 个版本已公开；40 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;common-band 已越过 fixed-small coupling；窗口上沿只给 \(O(1)\)，little-o 子区间才衰减；extreme strong remainder 与 multiscale physical absorption 仍开放。</p>
            <p><a href="/recap-r0-61-r0-72l.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72l.pdf">下载同步 PDF</a></p>
          </div>'''


HOME_L_CARD = r'''          <div class="task-one" id="r072l" data-release="r072l" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72L · 2026-08-27</p>
            <h3>保留实际 enstrophy 与 action 后，小耦合不再是共同频带的边界</h3>
            <p>对所有 \(\varepsilon=gB/R^2&gt;0\)，我得到保留 \(K=\mathcal R_Y\) 与 \(x=\Theta Q_*\) 的 full-lattice complete-root upper bound。对带固定背景、phase-aligned、row-aligned 的 launch，local exact correction 在 \(\tau=c_*/(R^2+gB)\) 产生精确根并给出 \(x\ge Z\)。</p>
            <p>由此 \(1\lesssim\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\) 内账本统一有界；只有 little-o 子区间内趋零。Galerkin 的线性坏族不能嵌入完整 Fourier lattice。</p>
            <p><strong>结论边界：</strong>&nbsp;extreme strong coupling、multiscale physical absorption 与一般三维正则性仍开放。</p>
            <p><a href="/notes/r0-72l.html"><strong>阅读 R0.72L 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72l.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072l/fig-r072l-strong-window.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072l">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072l_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072l-strong-window/fig-r072l-strong-window">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72l.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72l.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72M：</strong>&nbsp;量化 extreme strong coupling 的 full-lattice cascade/enstrophy/action alternative。</p>
          </div>'''


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    if 'data-site-version="1.24"' in html:
        changes = [
            ('data-site-version="1.24"', 'data-site-version="1.25"'),
            ("/i18n-en.js?v=1.24", "/i18n-en.js?v=1.25"),
            ("/site-refresh.js?v=1.24", "/site-refresh.js?v=1.25"),
            ("/recap-r0-61-r0-72k", "/recap-r0-61-r0-72l"),
            ("<strong>v1.24</strong>网页版本", "<strong>v1.25</strong>网页版本"),
            ("<strong>161</strong>公开研究笔记", "<strong>162</strong>公开研究笔记"),
            ("<strong>R0.72K</strong>最新研究节点", "<strong>R0.72L</strong>最新研究节点"),
            ("<strong>strong-coupling continuous-row ledger</strong>当前方向", "<strong>extreme strong-coupling cascade ledger</strong>当前方向"),
            ("Research topology · R0.1–R0.72K", "Research topology · R0.1–R0.72L"),
            ("R0.70A–R0.72K：63 节已公开，39 节完整封存", "R0.70A–R0.72L：64 节已公开，40 节完整封存"),
            ("R0.69P–R0.72K", "R0.69P–R0.72L"),
            ("展开 71 篇公开笔记", "展开 72 篇公开笔记"),
            ("综述 v1.24 · 2026-08-27", "综述 v1.25 · 2026-08-27"),
            ("上次综述 v1.23 · 2026-08-27", "上次综述 v1.24 · 2026-08-27"),
        ]
        for old, new in changes:
            html = required(html, old, new, f"home {old}")
        html = once(html,
            r"R0.72K 已用逐根隙 directional projection 闭合 complete complex-target ledger；common-band 完整根质量虽为 \(a^2N^2\) 量级，物理 critical-log 归一化后仍统一衰减。",
            r"R0.72L 已保留实际 enstrophy contrast 与 critical-log action，把 common-band complete-root ledger 推进到随 \(R\) 增长的 moderate strong-coupling window；extreme strong remainder 仍开放。", "home summary")
        html = once(html, "从 cubic no-go 走到 directional sampling 与 complete complex-root closure", "从 complete complex-root closure 走到 moderate strong-coupling window", "home route title")
        html = once(html,
            r"R0.72K 再对每个复根隙选择独立 norming direction，把 mixed row 与 true cubic 转成 complete complex-target ledger，并证明其 common-band 物理归一化比统一衰减。</p>",
            r"R0.72K 再对每个复根隙选择独立 norming direction，把 mixed row 与 true cubic 转成 complete complex-target ledger，并证明其 common-band 物理归一化比统一衰减。R0.72L 保留 actual \(K\) 与 \(x\)，用 local exact root/action floor 把闭合区推进到 \(\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\)。</p>", "home L route prose")
        html = once(html, "complete complex-root ledger</p>", "complete complex-root ledger → moderate strong-coupling window → extreme remainder</p>", "home route path")
        nav_k = '                  <a class="milestone" href="/notes/r0-72k.html">R0.72K</a>\n'
        html = once(html, nav_k, nav_k + '                  <a class="milestone" href="/notes/r0-72l.html">R0.72L</a>\n', "home L nav")
        old_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72L：</strong>&nbsp;检查 strong-coupling continuous-row ledger，并保留 multiscale heat windows 为后续接口。</p>
          </div>
        </section>'''
        new_tail = r'''            <p><strong style="color:var(--gold)">R0.72L 已完成：</strong>&nbsp;complete-root ledger 进入随 \(R\) 增长的中强耦合窗口；extreme strong remainder 已被单独写出。</p>
          </div>

''' + HOME_L_CARD + r'''
        </section>'''
        html = once(html, old_tail, new_tail, "home L card")
    elif 'data-site-version="1.25"' not in html:
        raise RuntimeError("home: expected site v1.24 or v1.25")

    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
                   r'<div class="summary-item"><strong>我目前关注</strong><span>R0.72L 已保留实际 enstrophy contrast 与 critical-log action，把 common-band complete-root ledger 推进到随 \(R\) 增长的 moderate strong-coupling window；extreme strong remainder 仍开放。</span></div>', "home normalized summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "home normalized next")
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', HOME_RECAP, "home normalized recap")
    html = section(html, r'          <div class="task-one" id="r072l" data-release="r072l".*?</div>', HOME_L_CARD, "home normalized L card")
    html = html.replace("complete-root ledger 进入随 (R) 增长", r"complete-root ledger 进入随 \(R\) 增长")
    for token in ["v1.25", "162", "R0.72L", "NEXT · R0.72M", "data-release=\"r072l\""]:
        if token not in html:
            raise RuntimeError(f"home: missing normalized token {token}")
    assert_clean(html, "R0.72L home")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    if "/i18n-en.js?v=1.25" in html:
        assert_clean(html, "R0.72L literature")
        return
    changes = [
        ("/recap-r0-61-r0-72k", "/recap-r0-61-r0-72l"),
        ("/i18n-en.js?v=1.24", "/i18n-en.js?v=1.25"),
        ("文献综述 v1.24 · 2026-08-27", "文献综述 v1.25 · 2026-08-27"),
        ("本站 R0.69P–R0.72K 只列为研究笔记", "本站 R0.69P–R0.72L 只列为研究笔记"),
        ("累计回顾与 101 节索引", "累计回顾与 102 节索引"),
        ("打开 101 节完整索引", "打开 102 节完整索引"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"literature {old}")
    html = once(html,
        r"R0.72K 通过逐根隙 norming direction 闭合 complete complex-target ledger，并证明其 common-band 物理归一化比仍统一衰减。一般 Navier–Stokes 正则性仍开放。</p>",
        r"R0.72K 通过逐根隙 norming direction 闭合 complete complex-target ledger，并证明其 common-band 物理归一化比仍统一衰减。R0.72L 保留实际 enstrophy contrast 与 critical-log action，闭合随 \(R\) 增长的 moderate strong-coupling window；窗口上沿只给 \(O(1)\)，little-o 子区间才衰减。一般 Navier–Stokes 正则性仍开放。</p>", "literature L route")
    open_l = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72L</b><strong>strong-coupling continuous-row ledger</strong></header><p>检查离开 \(gB/R^2\le\gamma_0\) 后的 mixed-row 与 true-cubic payment；multiscale heat windows 保留为并列后续接口。</p></div>'''
    closed_l = r'''              <div class="route-step closed"><header><b>R0.72L</b><strong>enstrophy-aware moderate strong-coupling closure</strong></header><p>保留实际 \(K=\mathcal R_Y\) 与 \(x=\Theta Q_*\)，在带固定背景、phase-aligned、row-aligned、exact-corrected 的构造族上建立 local action floor；窗口上沿统一有界，little-o 子区间才衰减。<a href="/notes/r0-72l.html">研究笔记</a> <a href="/recap-r0-61-r0-72l.html">当前累计回顾</a> <a href="#r072l-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72M</b><strong>extreme strong-coupling cascade ledger</strong></header><p>量化 full-lattice enstrophy、all-time action 或 improved cubic mixing，支付 \(\varepsilon^{7/3}p^{4/3}\) 余项；multiscale Schur ledger 保留为并列接口。</p></div>'''
    html = once(html, open_l, closed_l, "literature L cards")
    boundary_k = r'''          <div class="boundary"><strong>R0.72K 的主张边界</strong><p>方向引理的证明完整写出；限定检索未发现同一 fixed-level endpoint-slope packing 公式，但不据此主张新颖性或优先权。complete-root consequence 限于 finite triangular class，common-band decay 还保留 perturbative assumptions。</p></div>'''
    boundary_l = r'''

          <h3 id="r072l-boundary">R0.72L 的 strong-coupling、2D3C 与 Galerkin 边界</h3>
          <p><a href="https://doi.org/10.1063/1.4990082">Biferale–Buzzicotti–Linkmann</a> 说明 2D3C 是精确 PDE 结构；<a href="https://doi.org/10.1063/1.858309">Waleffe</a> 强调 triad transfer 依赖精确 Fourier geometry；<a href="https://doi.org/10.1017/jfm.2013.637">Moffatt</a> 说明 isolated triad truncation 与 exact evolution 可以显著不同。因此本节把三模 Galerkin countertheorem 与 full-lattice non-embedding proposition 分开陈述。</p>
          <p><a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a> 的 small-\(BMO^{-1}\) 理论不能与这里的 \(\varepsilon\) 等同；<a href="https://doi.org/10.4310/MAA.2007.v14.n2.a5">Chan–Vasseur</a> 的 logarithmic Prodi–Serrin improvement 也不是这里的 temporal critical-log action。<a href="https://doi.org/10.1070/RM2003v058n02ABEH000609">Escauriaza–Seregin–Šverák</a> 的 \(L_t^\infty L_x^3\) endpoint 仍是外部继续性基线，但当前 ledger 尚未推出它。</p>
          <p><a href="https://doi.org/10.1090/jams/838">Tao</a> 的 averaged Navier–Stokes blowup 说明 generic cancellation 与 harmonic estimates 不足以替代原方程结构；它不是 genuine NSE blowup。<a href="https://doi.org/10.1007/s00222-025-01396-z">Coiculescu–Palasek</a> 的 large-critical-data smooth nonuniqueness 位于无限能量、非 Leray–Hopf 边界，也不是 Clay 反例。</p>
          <div class="boundary"><strong>R0.72L 的主张边界</strong><p>限定检索没有找到项目公式或 \(p^{2/3}R^{2/3}(1+\log R)\) 窗口的直接前例，但这不构成新颖性或优先权证明。local floor 只属于带固定背景、phase-aligned、row-aligned、exact-corrected 的构造族；窗口上沿只给 \(O(1)\)，little-o 子区间才衰减；Galerkin 结果不是 full Fourier lattice 结论。</p></div>'''
    html = once(html, boundary_k, boundary_k + boundary_l, "literature L boundary")
    assert_clean(html, "R0.72L literature")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    count = len(list((PUBLIC / "notes").glob("*.html")))
    if count != 162:
        raise RuntimeError(f"expected 162 public HTML notes, found {count}")
    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({"latestCompletedRelease": "r072l", "siteVersion": "1.25",
                    "publicHtmlNoteCount": count, "postR060RecapNodeCount": 102,
                    "nextRelease": "r072m",
                    "latestReleaseGate": "tests/r072l-strong-coupling-gate.test.mjs",
                    "postR070APublishedReleaseCount": 64,
                    "postR070AFormalSealedReleaseCount": 40,
                    "legacyFormalFigureBacklogCount": 24})
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.25", "latestRelease": "R0.72L", "publicHtmlNoteCount": count})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update({"latestPublishedRelease": "r072l", "publishedReleaseCount": 64,
                      "formalSealedReleaseCount": 40, "legacyFormalFigureBacklogCount": 24})
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072l" not in inventory[key]:
            inventory[key].append("r072l")
    if len(inventory["legacyFormalFigureBacklog"]) != 24:
        raise RuntimeError("legacy formal-figure backlog changed unexpectedly")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ["research-review.html", "literature-review.html",
                     "notes/r0-72l.html", "recap-r0-61-r0-72l.html"]:
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({"release": "R0.72L", "siteVersion": "1.25", "notes": 162,
                      "recapNodes": 102, "published": 64, "formalSealed": 40,
                      "legacyBacklog": 24, "phases": 28, "next": "R0.72M"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
