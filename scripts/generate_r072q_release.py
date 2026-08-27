#!/usr/bin/env python3
"""Generate the deterministic R0.72Q release from the public R0.72P endpoint.

This source-stage file is intentionally not executed until the exact
certificate and formal figure are sealed.  Its preflight is fail closed: no
HTML or manifest mutation begins before every formal input passes.
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
from generate_r072p_release import assert_mathjax_clean, inline_math


ROOT = Path(os.environ.get("R072Q_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_RELATIVE = "figures/r072q-phase-robust-shape/fig-r072q-phase-robust-shape"
FIGURE_ID = "fig-r072q-phase-robust-shape"
CERTIFICATE_RELATIVE = "research/certificates/r072q"


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72Q · ARBITRARY STATIC PHASES · EXACT CAUSTIC</div>
        <h1>固定 \(M\) 的任意静态相位 shape gate 已闭合；<br>结论仍止于 \(Q_2\le1/2\) 的主谐波锥</h1>
        <p class="lead">对固定有限 \(M\)，任意静态相对相位与 \(Q_2=\sum_{m=2}^M m^2b_m\le1/2\)，归一化 profile 恰有两个临界点。对声明的热衰减路径，实际 Coble shear 在 \(0\le y\le1\) 上具有 \((r,\mathfrak C_0,\mathfrak C_1)=(\pi/12,81,36)\) 的统一 shape contract；归一化 \(F\) 保留更尖锐的 away 常数 \(12\)。1:2 退化集由精确 nephroid 参数式给出，phase-uniform 安全圆盘半径恰为 \(1/4\)。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72Q 任意静态相位固定 M 正类完成</span><strong>phase-robust fixed-M shape gate: CLOSED</strong><p>版本 v0.72Q · 2026-08-28</p><p>fixed \(M\), arbitrary static relative phases: CLOSED</p><p>\(Q_2\le1/2\), two critical points: CLOSED</p><p>physical \((r,C_0,C_1)=(\pi/12,81,36)\) on \(0\le y\le1\): CLOSED</p><p>exact 1:2 caustic and disk radius \(1/4\): CLOSED</p><p>growing \(M\) / phases varying in time: OPEN</p><p>general 3D / Clay problem: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>相位限制被移除，但有限 carrier ceiling 与二阶矩小量仍是定理条件</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · ARBITRARY STATIC PHASES</strong><p>固定 \(M&lt;\infty\)，所有静态 relative phases 任意，且 \(Q_2\le1/2\)。</p></div>
            <div class="verdict-card true"><strong>THEOREM · TWO CRITICAL POINTS</strong><p>临界点各自在 \(0\) 与 \(\pi\) 的 \(\pi/12\) 邻域内，数量恰为二。</p></div>
            <div class="verdict-card true"><strong>THEOREM · PHYSICAL SHAPE</strong><p>对 \(W=e^{-y}F\)、\(0\le y\le1\)，取 \(r=\pi/12\)、\(C_0=81\)、\(C_1=36\)。</p></div>
            <div class="verdict-card false"><strong>OPEN · OUTSIDE THE CONE</strong><p>增长 \(M\)、无 jet dominance、任意时变相位与一般 carrier 集仍开放。</p></div>
          </div>
        </section>

        <section id="normalization"><div class="section-no">01 / Phase quotient</div><h2>全局平移只固定第一谐波，其余相位无需对齐</h2>
          <div class="equation result">\[
          F_y(\phi)=\cos\phi+\sum_{m=2}^{M}r_m(y)\cos(m\phi+\theta_m),
          \quad r_m(y)=b_m e^{-(m^2-1)y},\quad
          S_j(y)=\sum_{m=2}^{M}m^jr_m(y),
          \]</div>
          <p>这里 \(\theta_m\) 与 \(y\) 无关，只有热包络随 \(y\) 变化。从 \(Q_2\le1/2\) 逐项得到 \(S_2(y)\le1/2\)、\(S_1(y)\le1/4\) 与 \(S_0(y)\le1/8\)。点态 Morse/shape 证明只使用这些界；ED 还使用这条固定相位热衰减路径。</p>
        </section>

        <section id="critical"><div class="section-no">02 / Critical-point count</div><h2>边界符号、严格单调与全局排除共同给出恰好两个临界点</h2>
          <p>精确比较 \(\sin(\pi/12)&gt;1/4\) 保证两个固定盒子的边界符号。盒内由 \(|F_y''|\ge\cos(\pi/12)-Q_2&gt;0\) 得严格单调；任一临界点又满足 \(|\sin\phi|\le Q_1\le1/4\)，因此盒外没有遗漏。</p>
        </section>

        <section id="shape"><div class="section-no">03 / Uniform shape contract</div><h2>归一化常数与实际 Coble shear 常数分账</h2>
          <div class="equation result">\[
          r=\frac\pi{12},\qquad
          (C_0,C_1)_{W}=(81,36),\qquad
          (C_1)_{F}=12.
          \]</div>
          <p>\(F\) 的局部 Hessian margin 大于 \(1/3\)。乘回 \(W=e^{-y}F\) 后，在 \(0\le y\le1\) 使用 \(e^{-1}&gt;1/3\)，得到局部 slope 下界 \(1/9\) 与 away 下界 \(1/36\)。正式 ED 调用使用 \(C_1=36\)，不能把归一化常数 \(12\) 直接代入物理 shear。</p>
        </section>

        <section id="fixedm"><div class="section-no">04 / Fixed-M ledger</div><h2>前三阶导数与 slow-time 门槛明确依赖固定 \(M\)</h2>
          <div class="equation result">\[
          \|F\|_\infty\le\frac98,\quad
          \|F'\|_\infty\le\frac54,\quad
          \|F''\|_\infty\le\frac32,\quad
          \|F^{(3)}\|_\infty\le1+\frac M2,
          \qquad \eta_{\rm slow}(M):=\left(1+\frac M2\right)^{-4}.
          \]</div>
          <p class="threshold-ledger">\(\eta_{\rm slow}\) 只是 slow-reference 条件，不是完整小黏性阈值。正式阈值为 \(\eta_\sharp(M)=\min\{1,\eta_{\rm slow}(M),\eta_{\rm CH}(2,\pi/12,81,36,C_{\rm sh}(M))\}\)。family-uniformity 来自 Coble–He Appendix A 与吸收参数的依赖追踪，不是仅凭 compactness；也没有得到 \(M\to\infty\) 的一致定理。</p>
        </section>

        <section id="ed"><div class="section-no">05 / Full-superposition ED</div><h2>R0.72P 的完整传播结论扩展到声明的任意静态相位热路径</h2>
          <p>Coble–He 的 profile-by-profile 定理结合固定 critical boxes、cutoffs、shape bounds 与热衰减导数账本，给固定 \(M\)、任意静态相位的声明热路径一个 proof-level uniform corollary；紧 \(\eta\) 区间仍由精确 \(L^2\) 收缩补齐。</p>
          <div class="equation result">\[
          E(y)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon y}E(0),
          \qquad \int_0^1E(y)\,dy\le C_{\rm ED}\varepsilon^{-1/2}E(0).
          \]</div>
          <p>常数只依赖固定 \(M\) 与声明的 upper shape class，不依赖静态相位、\(R\)、\(\varepsilon\) 或初值。这里没有证明任意时变相位或任意快速变化振幅的 ED。</p>
          <p>物理 cross-cubic/window 推论还要求 active modes 满足固定 \(|\beta_m|\ge\beta_->0\)，隐常数依赖 \((M,\beta_-)\)，不在 \(\beta_-\downarrow0\) 时一致。</p>
        </section>

        <section id="caustic"><div class="section-no">06 / Exact 1:2 caustic</div><h2>退化墙是一条精确 nephroid，而不是数值扫描曲线</h2>
          <div class="equation result">\[
          z(\phi)=\frac18e^{-3i\phi}-\frac38e^{-i\phi},\qquad
          \left(|z|^2-\frac1{16}\right)^3=\frac{27}{1024}(\operatorname{Im}z)^2.
          \]</div>
          <p>其半径范围为 \([1/4,1/2]\)。因此 \(|z|&lt;1/4\) 内所有相位都非退化且恰有两个临界点；半径 \(1/4\) 对 phase-uniform 圆盘是尖锐的。</p>
        </section>

        <section id="wall"><div class="section-no">07 / Wall classification</div><h2>一般墙点是 fold，实轴端点是 cusp；二者都只标记 Morse 适用性</h2>
          <p>墙上一般点满足 \(f^{(3)}=-3\sin\phi\ne0\)，属于 \(A_2\) fold；\(z=\pm1/4\) 的实轴端点满足三阶消失而四阶非零，属于 \(A_3\) cusp。这里没有证明 enhanced dissipation 在墙上失败。</p>
        </section>

        <section id="certificate"><div class="section-no">08 / Independent exact audit</div><h2>Python Fraction 与 JavaScript BigInt 双路只核验有限代数骨架</h2>
          <p>两路独立重建 jet budget、radical comparisons、slow threshold 与 caustic ledger；comparator 要求 canonical payload 精确相等。正式有限证书取 \(M=2\)，只核验有限代数骨架，不替代对所有固定 \(M\) 的解析证明。hash builder 拒绝临时 crosscheck、脏 source lineage、缺件、多件与 symlink。</p>
        </section>

        <section id="literature"><div class="section-no">09 / Literature boundary</div><h2>半群输入来自一手文献，任意静态相位 family uniformity 是本站的 proof-level 抽取</h2>
          <p><a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He</a> 提供时变非退化 shear 的 enhanced-dissipation 框架；<a href="https://arxiv.org/abs/2104.05123">Voorhaar</a> 提供 caustic 的 Laurent-polynomial 语境。两者都不逐字陈述本站固定 \(M\)、\(Q_2\le1/2\)、任意静态相位、声明热路径与 1:2 实系数 nephroid 的组合定理。</p>
        </section>

        <section id="figure"><div class="section-no">10 / Journal figure</div><h2>正式附图区分任意静态相位安全锥、物理 shape 常数与精确 caustic</h2>
          <p><img src="/assets/r072q/fig-r072q-phase-robust-shape.svg" alt="R0.72Q arbitrary-static-phase fixed-M shape gate and exact 1:2 caustic"></p>
          <p><a href="/assets/r072q/fig-r072q-phase-robust-shape.pdf">下载 PDF</a> · <a href="/assets/r072q/fig-r072q-phase-robust-shape.png">下载 PNG</a> · <a href="/assets/r072q/fig-r072q-phase-robust-shape.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">11 / Research value</div><h2>这是从特殊两载波相位线到相位鲁棒有限模式锥的实质扩张</h2>
          <p>R0.72Q 移除了 R0.72P 的 real-collinear restriction，但所有相位仍保持静态；临界点计数、uniform shape 与适用边界由此变成可审计的系数空间几何。它提高了机制类结果的稳健性，但仍不是一般三维稳定阈值。</p>
        </section>

        <section id="scope"><div class="section-no">12 / Scope boundary</div><h2>固定 \(M\) 与 \(Q_2\le1/2\) 是真实边界，不是排版备注</h2>
          <p>没有闭合增长 \(M\)、跨越 caustic 的 profile、任意 time-dependent phases、无 dominant first harmonic 的有限 pattern、fixed-\(R\) arbitrary coupling、一般三维 continuation、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="next"><div class="section-no">13 / Next gate</div><h2>R0.72R：离开 dominant-first-harmonic cone</h2>
          <p>下一节将研究受控的 1:2:3 caustic 或逼近退化墙的 profile，检验 uniform shape contract 在非主谐波锥中的首个失效或可延拓机制。</p>
        </section>

        <section id="reproduce"><div class="section-no">14 / Reproduction</div><h2>报告、独立审计、精确证书与正式附图包</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072q_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072q_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072q_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072q_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072q">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072q-phase-robust-shape/fig-r072q-phase-robust-shape">正式附图包</a> · <a href="/notes/r0-72q.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72q.html">累计回顾</a> · <a href="/recap-r0-61-r0-72q.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = '''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72R</span><span class="tree-state current">下一检查点</span></div>
              <h3>leave the dominant-first-harmonic cone</h3>
              <p>研究受控的 1:2:3 caustic 或逼近退化墙的 profile，定位 uniform shape contract 的首个新边界。</p>
            </article>'''


HOME_Q_CARD = r'''          <div class="task-one" id="r072q" data-release="r072q" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72Q · 2026-08-28</p>
            <h3>固定 \(M\) 的任意静态相位 Morse shape gate 已经闭合</h3>
            <p>在 \(Q_2\le1/2\) 下，所有静态 relative phases 都允许；临界点恰有两个。对声明的热衰减路径，实际 Coble shear 在 \(0\le y\le1\) 可取 \((r,C_0,C_1)=(\pi/12,81,36)\)。</p>
            <p>1:2 退化集是精确 nephroid \(z(\phi)=\frac18e^{-3i\phi}-\frac38e^{-i\phi}\)，phase-uniform 安全圆盘半径恰为 \(1/4\)。</p>
            <p><strong>结论边界：</strong>&nbsp;固定 \(M\) 与 jet dominance 不能删除；任意时变相位和任意快速变化振幅的 ED 未证明；caustic 只标记 Morse applicability，不是 ED 失败。</p>
            <p><a href="/notes/r0-72q.html"><strong>阅读 R0.72Q 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72q.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072q/fig-r072q-phase-robust-shape.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072q">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072q_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072q-phase-robust-shape/fig-r072q-phase-robust-shape">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72q.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72q.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72R：</strong>&nbsp;离开 dominant-first-harmonic cone。</p>
          </div>'''


def validate_inputs() -> None:
    required_inputs = (
        "research/r072q_report-source.md",
        "research/r072q_literature_audit.md",
        "research/r072q_gap_matrix.md",
        "research/r072q_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72p.html",
        "public/recap-r0-61-r0-72p.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72Q release input: {relative}")

    report = (ROOT / "research/r072q_report-source.md").read_text(encoding="utf-8")
    for token in (
        "Q_2:=\\sum_{m=2}^{M}m^2b_m\\le\\frac12",
        "N_{\\rm crit}=2",
        "r=\\frac\\pi{12}",
        "\\mathfrak C_0=81",
        "\\mathfrak C_1=36",
        "z(\\phi)=\\frac18e^{-3i\\phi}-\\frac38e^{-i\\phi}",
        "R0.72R",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72Q report missing claim-boundary token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72Q certificate")
    verify_flat_hash_ledger(figure, "R0.72Q figure")
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if (
        crosscheck.get("status") != "passed"
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not all(value is True for value in crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError("R0.72Q crosscheck is not a formal all-passed seal")

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    publication = manifest.get("publication", {})
    if (
        manifest.get("release") != "R0.72Q"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
        or publication.get("publicCopiesComplete") is not True
        or publication.get("directory") != "public/assets/r072q"
        or publication.get("stem") != FIGURE_ID
    ):
        raise RuntimeError("R0.72Q figure manifest is not a complete formal seal")
    validator = ROOT / "research/validate_figure_package.py"
    completed = subprocess.run(
        [sys.executable, str(validator), str(figure)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0 or json.loads(completed.stdout).get("errors") != []:
        raise RuntimeError("R0.72Q strict figure validation failed")
    expected_public = []
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = ROOT / publication["directory"] / f"{publication['stem']}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72Q public {suffix} is absent or not byte-identical")
        expected_public.append(str(public.relative_to(ROOT)))
    if sorted(row.get("path") for row in publication.get("assets", [])) != sorted(expected_public):
        raise RuntimeError("R0.72Q manifest does not enumerate the exact public assets")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72p.html").read_text(encoding="utf-8")
    replacements = (
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72Q：固定 M、任意静态相位与 Q2≤1/2 下的两临界点 shape gate，以及精确 1:2 caustic。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72Q｜任意静态相位 shape gate 与精确 caustic">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="固定 M 任意静态相位的统一 Morse shape contract 与 phase-uniform 半径 1/4。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072q/fig-r072q-phase-robust-shape.png">'),
        (r'<title>.*?</title>', '<title>R0.72Q｜任意静态相位 shape gate 与精确 caustic</title>'),
    )
    for index, (pattern, value) in enumerate(replacements):
        html = section(html, pattern, value, f"Q note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.29", "/i18n-en.js?v=1.30", "Q note i18n")
    html = required(
        html,
        "@media(max-width:760px){.verdict-grid,.audit-grid{grid-template-columns:1fr}.compact-table{font-size:.82rem}}",
        "@media(max-width:760px){.verdict-grid,.audit-grid{grid-template-columns:1fr}.compact-table{font-size:.82rem}.threshold-ledger mjx-container{display:inline-block;max-width:100%;overflow-x:auto;overflow-y:hidden;vertical-align:middle}}",
        "Q note mobile threshold containment",
    )
    nav = '<nav><a href="#result">结论</a><a href="#normalization">归一化</a><a href="#critical">临界点</a><a href="#shape">shape</a><a href="#fixedm">fixed M</a><a href="#ed">ED</a><a href="#caustic">caustic</a><a href="#wall">墙</a><a href="#certificate">证书</a><a href="#literature">文献边界</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#scope">边界</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "Q note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "Q note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#normalization">01 · phase quotient</a></li><li><a href="#critical">02 · 临界点计数</a></li><li><a href="#shape">03 · shape contract</a></li><li><a href="#fixedm">04 · fixed-M 账本</a></li><li><a href="#ed">05 · full-superposition ED</a></li><li><a href="#caustic">06 · 精确 caustic</a></li><li><a href="#wall">07 · 墙分类</a></li><li><a href="#certificate">08 · 独立证书</a></li><li><a href="#literature">09 · 文献边界</a></li><li><a href="#figure">10 · 正式附图</a></li><li><a href="#value">11 · 研究价值</a></li><li><a href="#scope">12 · 主张边界</a></li><li><a href="#next">13 · R0.72R</a></li><li><a href="#reproduce">14 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "Q note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "Q note article")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72Q · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r'<footer>.*?</footer>', footer, "Q note footer")
    assert_clean(html, "R0.72Q note")
    assert_mathjax_clean(html, "R0.72Q note")
    (PUBLIC / "notes/r0-72q.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72p.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.29", "/i18n-en.js?v=1.30"),
        ("R0.61–R0.72P", "R0.61–R0.72Q"),
        ("累计回顾 · R0.61–R0.72Q · 2026-08-27", "累计回顾 · R0.61–R0.72Q · 2026-08-28"),
        ("R0.61 到 R0.72P 的 106 个研究节点", "R0.61 到 R0.72Q 的 107 个研究节点"),
        ("收录节点：106", "收录节点：107"),
        ("回顾截止时公开笔记：166", "回顾截止时公开笔记：167"),
        ("回顾截止节点：R0.72P", "回顾截止节点：R0.72Q"),
        ("02 · 106 节完整索引", "02 · 107 节完整索引"),
        ("<strong>106</strong><span>R0.61–R0.72Q 研究节点</span>", "<strong>107</strong><span>R0.61–R0.72Q 研究节点</span>"),
        ("<strong>68</strong><span>R0.70A–R0.72P 已公开版本</span>", "<strong>69</strong><span>R0.70A–R0.72Q 已公开版本</span>"),
        ("<strong>44</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>45</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("后面的 106 个节点", "后面的 107 个节点"),
        ("R0.70A–R0.72P 的 68 个版本已经公开；其中 44 个", "R0.70A–R0.72Q 的 69 个版本已经公开；其中 45 个"),
        ("R0.61–R0.72Q 的 106 节公开笔记", "R0.61–R0.72Q 的 107 节公开笔记"),
        ("/recap-r0-61-r0-72p.pdf", "/recap-r0-61-r0-72q.pdf"),
    ):
        html = required(html, old, new, f"Q recap {old}")
    html = section(html, r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72Q 的 107 个节点；最新一节闭合固定 M 任意静态相位 shape gate。">', "Q recap description")
    html = section(html, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十八个阶段、107 个节点：从约化递推到固定 M 任意静态相位 shape gate。">', "Q recap og description")
    html = section(html, r'<title>.*?</title>', '<title>R0.61–R0.72Q｜R0.60 之后的研究回顾</title>', "Q recap title")
    phase = r'''            <article class="phase"><h3>R0.72L–R0.72Q · strong-coupling、物理回填与相位鲁棒 shape gate</h3>
              <p>R0.72L 保留 actual ledger；R0.72M 给出零扩散 action-poor reference，R0.72N 才证明耗散一载波链不属于该安全分支。R0.72O 完成物理回填，R0.72P 在 fixed real-collinear static-phase 1:2 正类上关闭完整传播门。</p>
              <p>R0.72Q 再移除实共线与相位对齐限制，但相位仍保持静态：对固定 \(M\)、任意静态相位与 \(Q_2\le1/2\)，恰有两个临界点；对声明的热衰减路径，实际 Coble shear 在 \(0\le y\le1\) 可取 \((\pi/12,81,36)\)。1:2 caustic 给出尖锐 phase-uniform 半径 \(1/4\)。增长 \(M\) 与一般 carrier 集仍开放。</p>
              <p>R0.72P 的 ED 常数对声明的 \(\lambda\) 区间一致；物理比较常数仍可依赖固定的 \(\lambda_->0\)。R0.72Q 的 ED 只覆盖任意静态相位的热衰减路径，任意时变相位与任意快速变化振幅未证明。它的物理 cross-cubic/window 推论还要求 active modes 满足固定 \(|\beta_m|\ge\beta_->0\)，隐常数依赖 \((M,\beta_-)\)，不在 \(\beta_-\downarrow0\) 时一致。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/notes/r0-72n.html">R0.72N</a><a href="/notes/r0-72o.html">R0.72O</a><a href="/notes/r0-72p.html">R0.72P</a><a href="/notes/r0-72q.html">R0.72Q</a><a href="/assets/r072q/fig-r072q-phase-robust-shape.pdf">R0.72Q 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072q">R0.72Q 证书</a></div></article>'''
    html = section(html, r'            <article class="phase"><h3>R0\.72L–R0\.72P .*?</article>', phase, "Q recap phase")
    node_p = '            <span class="node-ref"><a href="/notes/r0-72p.html">R0.72P</a><span class="node-state kind-closed">闭</span></span>\n'
    node_q = '            <span class="node-ref"><a href="/notes/r0-72q.html">R0.72Q</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_p, node_p + node_q, "Q recap node")
    retained = r'''            <li>R0.72Q 的 fixed-\(M\) arbitrary-static-phase theorem：\(Q_2\le1/2\) 保证恰有两个临界点；对声明热路径，物理 shear 在 \(0\le y\le1\) 的正式 shape 常数为 \((\pi/12,81,36)\)；1:2 caustic 给出尖锐 phase-uniform disk 半径 \(1/4\)。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "Q recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>相位鲁棒的有限模式锥已闭合，一般 superposition 仍远未完成</h2><p>截至 R0.72Q，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 107 个节点或 69 个公开版本解释成 Clay 问题完成比例。</p><p>新的严格增量是 fixed-\(M\)、arbitrary-static-phase、\(Q_2\le1/2\) 的 uniform shape gate，以及精确 1:2 caustic。</p></section>''', "Q recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72R 离开 dominant-first-harmonic cone</h2><p>研究受控 1:2:3 caustic 或逼近退化墙的 profile，定位 uniform shape contract 的首个新边界。</p></section>''', "Q recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72Q 的 69 节已公开；45 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。</p><p>R0.72Q 的点态 shape theorem 覆盖固定 \(M\)、任意静态相位与 \(Q_2\le1/2\) 的 dominant-first-harmonic cone；ED 只对声明的固定相位热衰减路径成立。任意时变相位、任意快速变化振幅、增长 \(M\)、一般 carrier 集和 Clay 正式问题保持开放。</p><p>物理 cross-cubic/window 推论还要求 active modes 满足固定 \(|\beta_m|\ge\beta_->0\)，隐常数依赖 \((M,\beta_-)\)，不在 \(\beta_-\downarrow0\) 时一致。</p></section>''', "Q recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72p.html">保留 R0.72P 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72q.html">打开最新节点 R0.72Q</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072q">查看 R0.72Q 精确证书</a> · <a href="/assets/r072q/fig-r072q-phase-robust-shape.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72q.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72p.pdf">上一版累计回顾 PDF</a></p><p>完整节点索引保留 R0.69W、R0.70A 以后每个公开版本及其原始编号；状态标签只描述证据类型。</p></section>''', "Q recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72Q 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "Q recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 107 or len(set(links)) != 107:
        raise RuntimeError(f"recap node index expected 107 unique links, got {len(links)}/{len(set(links))}")
    assert_clean(html, "R0.72Q recap")
    assert_mathjax_clean(html, "R0.72Q recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72q.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.29"', 'data-site-version="1.30"'),
        ("/i18n-en.js?v=1.29", "/i18n-en.js?v=1.30"),
        ("/site-refresh.js?v=1.29", "/site-refresh.js?v=1.30"),
        ("<strong>2026-08-27</strong>最近修订", "<strong>2026-08-28</strong>最近修订"),
        ("<strong>v1.29</strong>网页版本", "<strong>v1.30</strong>网页版本"),
        ("<strong>166</strong>公开研究笔记", "<strong>167</strong>公开研究笔记"),
        ("<strong>R0.72P</strong>最新研究节点", "<strong>R0.72Q</strong>最新研究节点"),
        ("<strong>full-superposition enhanced dissipation with shape control</strong>当前方向", "<strong>caustic geometry beyond the dominant-first-harmonic cone</strong>当前方向"),
        ("Research topology · R0.1–R0.72P", "Research topology · R0.1–R0.72Q"),
        ("R0.70A–R0.72P：68 节已公开，44 节完整封存", "R0.70A–R0.72Q：69 节已公开，45 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72P</span>', '<span class="route-range">R0.69P–R0.72Q</span>'),
        ('aria-label="R0.69P–R0.72P"', 'aria-label="R0.69P–R0.72Q"'),
        ("展开 76 篇公开笔记", "展开 77 篇公开笔记"),
        ("从 dissipative one-carrier decision 走到 physical reinsertion", "固定 \\(M\\) 的任意静态相位 Morse shape gate 已经闭合"),
        (" → full-superposition ED gate</p>", " → full-superposition ED gate <span>→ arbitrary-static-phase fixed-M shape gate → exact 1:2 caustic</span></p>"),
        ("综述 v1.29 · 2026-08-27", "综述 v1.30 · 2026-08-28"),
        ("上次综述 v1.28 · 2026-08-27", "上次综述 v1.29 · 2026-08-27"),
        ("/recap-r0-61-r0-72p.html", "/recap-r0-61-r0-72q.html"),
        ("/recap-r0-61-r0-72p.pdf", "/recap-r0-61-r0-72q.pdf"),
        (r"对 \(R,2R\)、\(B=2\)、\(0&lt;\lambda_-\le|\lambda|\le1/8\)，完整 propagator 满足常数对 \(R,\varepsilon,\lambda\) 一致的 enhanced dissipation；所有 cross terms 都保留。", r"ED semigroup 结论覆盖 \(R,2R\)、\(B=2\) 与 \(|\lambda|\le1/8\)，包括 \(\lambda=0\)；只有 inherited amplitude-balanced physical comparison 另要求固定 \(0&lt;\lambda_-\le|\lambda|\)，且相关常数可依赖 \(\lambda_-\)。完整 propagator 保留所有 cross terms。"),
    ):
        html = required(html, old, new, f"Q home {old}")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72Q 已闭合 fixed-M arbitrary-static-phase、Q2≤1/2 的 shape gate；下一关是离开 dominant-first-harmonic cone。</span></div>', "Q home focus")
    link_p = '<a class="milestone" href="/notes/r0-72p.html">R0.72P</a>'
    html = once(html, link_p, link_p + '\n                  <a class="milestone" href="/notes/r0-72q.html">R0.72Q</a>', "Q home route link")
    route_q = r'''              <p>R0.72Q 再移除实共线与相位对齐限制，但相位仍保持静态：对固定 \(M\)、任意静态相位与 \(Q_2\le1/2\)，恰有两个临界点；对声明的热衰减路径，实际 Coble shear 在 \(0\le y\le1\) 可取 \((\pi/12,81,36)\)。1:2 caustic 给出尖锐 phase-uniform 半径 \(1/4\)。增长 \(M\) 与一般 carrier 集仍开放。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_q + '              <details class="tree-notes" open>', "Q home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "Q home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72Q · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 107 个节点；全站现有 167 篇公开研究笔记</h3>
            <p>累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72Q 的完整逐节点索引。R0.72Q 对固定 \(M\)、任意静态相位与 \(Q_2\le1/2\) 证明 uniform shape gate，并给出精确 1:2 caustic；ED 仍限于声明的热衰减路径。</p>
            <p>R0.70A–R0.72Q 共 69 个版本已公开；45 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;相位鲁棒有限模式锥已闭合；增长 \(M\)、一般 carrier 集与一般三维问题仍开放。</p>
            <p><a href="/recap-r0-61-r0-72q.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72q.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "Q home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_Q_CARD + '\n        </section>\n\n      </article>', "Q home card")
    if html.count('data-release="r072q"') != 1:
        raise RuntimeError("home must contain exactly one R0.72Q card")
    assert_clean(html, "R0.72Q home")
    assert_mathjax_clean(html, "R0.72Q home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.29", "/i18n-en.js?v=1.30"),
        ("本站 R0.69P–R0.72P 只列为研究笔记", "本站 R0.69P–R0.72Q 只列为研究笔记"),
        ("/recap-r0-61-r0-72p.html", "/recap-r0-61-r0-72q.html"),
        ("文献综述 v1.29 · 2026-08-27", "文献综述 v1.30 · 2026-08-28"),
        ("累计回顾与 105 节索引", "累计回顾与 107 节索引"),
        ("打开 105 节完整索引", "打开 107 节完整索引"),
        (r'<a href="#ref-74">Coble–He</a>要求随时间慢变且具有统一临界结构的 shear', r'<a href="#ref-74">Coble–He</a>只要求 reference shear \(U\) 的 \(\partial_{ty}U\) 足够小；actual shear \(V\) 可快速变化，但必须与 \(U\) 共享临界点并满足统一 sign、shape 与 norm 条件'),
        (r'<div class="boundary"><strong>R0.72P 的主张边界</strong><p>正结果只覆盖 fixed real-collinear-phase 1:2、\(B=2\)、\(0&lt;\lambda_-\le|\lambda|\le1/8\)。\(\lambda=\pm1/4\) 只证明该 Morse theorem 的适用条件退化，不证明 enhanced dissipation 失败。任意相位、任意 carrier 集或增长 \(N\)、fixed-\(R\) arbitrary coupling 与一般三维问题仍开放；限定检索不构成新颖性或优先权证明。</p></div>', r'<div class="boundary"><strong>R0.72P 的主张边界</strong><p>ED semigroup 结论覆盖 fixed real-collinear-phase 1:2、\(B=2\) 与 \(|\lambda|\le1/8\)，包括 \(\lambda=0\)。只有 inherited amplitude-balanced physical comparison 另要求固定 \(0&lt;\lambda_-\le|\lambda|\)，其常数可依赖 \(\lambda_-\)。\(\lambda=\pm1/4\) 只证明该 Morse theorem 的适用条件退化，不证明 enhanced dissipation 失败。任意相位、任意 carrier 集或增长 \(N\)、fixed-\(R\) arbitrary coupling 与一般三维问题仍开放；限定检索不构成新颖性或优先权证明。</p></div>'),
        ("            <li id=\"ref-105\">D. Coble and S. He. <a href=\"https://doi.org/10.4310/CMS.2024.v22.n6.a10\"><em>A Note on Enhanced Dissipation of Time-Dependent Shear Flows</em></a>. Communications in Mathematical Sciences 22(6) (2024). <a href=\"https://arxiv.org/abs/2309.15738\">arXiv:2309.15738</a>.</li>\n", ""),
    ):
        html = required(html, old, new, f"Q literature {old}")
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72Q</b><strong>phase-robust finite-pattern shape contract</strong></header><p>量化实系数同一直线相位 locus 附近的 uniform Morse cone，或构造 fixed critical neighborhoods 失效的精确反族。</p></div>'
    new_steps = r'''<div class="route-step closed"><header><b>R0.72Q</b><strong>fixed-M arbitrary-static-phase shape gate and exact 1:2 caustic</strong></header><p>固定 \(M\)、任意静态相位与 \(Q_2\le1/2\) 下，恰有两个临界点；对声明的热衰减路径，实际 shear 在 \(0\le y\le1\) 的 shape 常数为 \((\pi/12,81,36)\)。1:2 caustic 给出尖锐半径 \(1/4\)。<a href="/notes/r0-72q.html">研究笔记</a> <a href="/recap-r0-61-r0-72q.html">当前累计回顾</a> <a href="#r072q-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72R</b><strong>leave the dominant-first-harmonic cone</strong></header><p>研究受控 1:2:3 caustic 或逼近退化墙的 profile，定位 uniform shape contract 的新边界。</p></div>'''
    html = once(html, old_open, new_steps, "Q literature route")
    boundary = r'''

          <h3 id="r072q-boundary">R0.72Q 的任意静态相位 shape theorem 与 caustic 文献边界</h3>
          <p><a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He, Theorem 1.2 and Appendix A</a> 为单个非退化时变 shear 提供 modewise enhanced dissipation。R0.72Q 对固定静态相位的热衰减路径，通过固定 critical boxes、统一 Hessian margin 与 fixed-\(M\) derivative ledger，从 proof 中抽取声明 family 的一致常数；这不是原论文逐字陈述的 arbitrary-static-phase family theorem。</p>
          <p><a href="https://arxiv.org/abs/2104.05123">Voorhaar</a> 提供 Laurent-polynomial caustic 的代数几何背景，但不直接给出本站实 1:2 coefficient plane 的 nephroid 参数式、phase-uniform disk 或 ED corollary。</p>
          <div class="boundary"><strong>R0.72Q 的主张边界</strong><p>点态 shape theorem 只覆盖固定 \(M\)、任意静态相位、dominant first harmonic 与 \(Q_2\le1/2\)；ED 只对声明的固定相位热衰减路径成立。正式 physical shape 常数 \((\pi/12,81,36)\) 只在 \(0\le y\le1\) 使用，归一化 \(F\) 的 away 常数 \(12\) 不可直接替代。增长 \(M\)、任意 time-dependent phases、任意快速变化振幅、无 jet dominance、跨越 caustic 的 profile、fixed-\(R\) arbitrary coupling 与一般三维问题仍开放；限定检索不构成新颖性或优先权证明。</p><p>物理 cross-cubic/window 推论还要求 active modes 满足固定 \(|\beta_m|\ge\beta_->0\)，隐常数依赖 \((M,\beta_-)\)，不在 \(\beta_-\downarrow0\) 时一致。</p></div>'''
    match = re.search(r'(<h3 id="r072p-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("Q literature boundary: expected one R0.72P boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "Q literature boundary")
    assert_clean(html, "R0.72Q literature")
    assert_mathjax_clean(html, "R0.72Q literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 167:
        raise RuntimeError(f"expected 167 public HTML notes after R0.72Q, got {notes}")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    expected = {
        "latestCompletedRelease": "r072p",
        "siteVersion": "1.29",
        "publicHtmlNoteCount": 166,
        "postR060RecapNodeCount": 106,
        "nextRelease": "r072q",
        "latestReleaseGate": "tests/r072p-superposition-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072p-release.test.mjs",
        "postR070APublishedReleaseCount": 68,
        "postR070AFormalSealedReleaseCount": 44,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72P: {key}")
    stage = release.get("nextReleaseSourceStage", {})
    if (
        stage.get("release") != "r072q"
        or stage.get("stage") != "source-freeze"
        or stage.get("publicationStatus")
        != "pending-formal-certificate-figure-and-publication"
        or stage.get("publicCountersAdvanced") is not False
        or stage.get("releaseGate") != "tests/r072q-phase-robust-shape-gate.test.mjs"
        or stage.get("publicationTest") != "tests/r072q-release.test.mjs"
    ):
        raise RuntimeError("R0.72Q source-stage manifest contract is missing or stale")
    release.update({
        "latestCompletedRelease": "r072q",
        "siteVersion": "1.30",
        "publicHtmlNoteCount": 167,
        "postR060RecapNodeCount": 107,
        "nextRelease": "r072r",
        "latestReleaseGate": "tests/r072q-phase-robust-shape-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072q-release.test.mjs",
        "postR070APublishedReleaseCount": 69,
        "postR070AFormalSealedReleaseCount": 45,
    })
    del release["nextReleaseSourceStage"]
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if site.get("latestRelease") != "R0.72P" or site.get("publicHtmlNoteCount") != 166:
        raise RuntimeError("site-version is not at R0.72P")
    site.update({"version": "1.30", "latestRelease": "R0.72Q", "publicHtmlNoteCount": 167, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") != "r072p" or inventory.get("legacyFormalFigureBacklogCount") != 24:
        raise RuntimeError("formal archive inventory is not at R0.72P")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072p" or "r072q" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72P")
        inventory[key].append("r072q")
    inventory.update({"latestPublishedRelease": "r072q", "publishedReleaseCount": 69, "formalSealedReleaseCount": 45})
    if len(inventory["publishedReleases"]) != 69 or len(inventory["formalSealedReleases"]) != 45:
        raise RuntimeError("formal archive count mismatch after R0.72Q")
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
        "notes/r0-72q.html",
        "recap-r0-61-r0-72q.html",
    ):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({
        "release": "R0.72Q",
        "siteVersion": "1.30",
        "notes": 167,
        "recapNodes": 107,
        "published": 69,
        "formalSealed": 45,
        "legacyBacklog": 24,
        "phases": 28,
        "routeNotes": 77,
        "next": "R0.72R",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
