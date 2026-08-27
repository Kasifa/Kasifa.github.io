#!/usr/bin/env python3
"""Generate the deterministic R0.72P release from the public R0.72O endpoint."""

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


ROOT = Path(os.environ.get("R072P_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"


def inline_math(fragment: str) -> str:
    """Restore MathJax delimiters around balanced inline-formula markers.

    The release fragments use ordinary balanced parentheses only as compact
    inline-math markers; full-width Chinese parentheses remain prose.  A
    depth-aware pass is required because formulae such as ``E(y)`` and
    ``O(a^2)`` contain their own parentheses.
    """
    output: list[str] = []
    index = 0
    in_tag = False
    while index < len(fragment):
        character = fragment[index]
        if not in_tag and fragment.startswith(r"\[", index):
            close = fragment.find(r"\]", index + 2)
            if close < 0:
                raise RuntimeError("unclosed display-math delimiter in R0.72P fragment")
            output.append(fragment[index : close + 2])
            index = close + 2
            continue
        if not in_tag and fragment.startswith(r"\(", index):
            close = fragment.find(r"\)", index + 2)
            if close < 0:
                raise RuntimeError("unclosed inline-math delimiter in R0.72P fragment")
            output.append(fragment[index : close + 2])
            index = close + 2
            continue
        if character == "<":
            in_tag = True
        if character == ">":
            in_tag = False
            output.append(character)
            index += 1
            continue
        if not in_tag and character == "(" and (index == 0 or fragment[index - 1] != "\\"):
            depth = 1
            cursor = index + 1
            while cursor < len(fragment) and depth:
                if fragment[cursor] == "(":
                    depth += 1
                elif fragment[cursor] == ")":
                    depth -= 1
                cursor += 1
            if depth:
                raise RuntimeError("unbalanced inline-math marker in R0.72P fragment")
            content = fragment[index + 1 : cursor - 1]
            if "<" in content or ">" in content or "\n" in content:
                raise RuntimeError(f"invalid inline-math marker: {content!r}")
            output.extend((r"\(", content, r"\)"))
            index = cursor
            continue
        output.append(character)
        index += 1
    return "".join(output)


def assert_mathjax_clean(text: str, label: str, *, check_naked: bool = True) -> None:
    """Reject common delimiter corruption and unwrapped TeX outside displays."""
    without_displays = re.sub(r"\\\[.*?\\\]", "", text, flags=re.S)
    malformed_delimiters = {
        "function argument escaped as a fresh delimiter": r"[A-Za-z0-9_}]\\\(",
        "nested inline delimiter": r"\\\((?:(?!\\\)).)*\\\(",
    }
    for reason, pattern in malformed_delimiters.items():
        match = re.search(pattern, without_displays)
        if match:
            raise RuntimeError(f"{label}: {reason}: {match.group(0)!r}")
    if not check_naked:
        return
    outside_math = re.sub(r"\\\(.*?\\\)", "", without_displays, flags=re.S)
    naked = re.search(
        r"(?<!\\)\([^<>\n]*\\(?:lambda|varepsilon|phi|pi|mathcal|rm|sqrt|"
        r"le|ge|in|times|lvert|partial)[^<>\n]*\)(?!\\)",
        outside_math,
    )
    if naked:
        raise RuntimeError(f"{label}: naked parenthesized TeX: {naked.group(0)!r}")


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72P · FULL-SUPERPOSITION ED · MORSE WALL</div>
        <h1>完整两载波传播门已经闭合；<br>结论止于固定实系数同一直线相位（同相或反相） 1:2 正类</h1>
        <p class="lead">对载波 (R,2R)、实系数同一直线相位（同相或反相）、(B=2) 与 (0&lt;\lambda_-\le|\lambda|\le1/8)，完整 affine-row propagator 满足常数对 (R,\varepsilon\ge1,\lambda) 一致的 enhanced-dissipation 估计。所有 self/cross terms 都留在同一传播子内，因此 R0.72O 的 full-superposition cubic gate 在这个固定正类上无条件闭合。(\lambda=\pm1/4) 只是一手 Morse 定理的精确适用边界，不是 enhanced dissipation 失败。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72P 固定两载波正类完成</span><strong>1:2 real-collinear-phase superposition gate: CLOSED</strong><p>版本 v0.72P · 2026-08-27</p><p>fixed carrier pattern (R:2R): CLOSED</p><p>full-superposition ED: CLOSED</p><p>uniform (R,\varepsilon,\lambda) constants: CLOSED</p><p>Morse applicability wall (\lvert\lambda\rvert=1/4): EXACT</p><p>arbitrary phases / carrier sets: OPEN</p><p>fixed-(R) arbitrary coupling / general 3D: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>一个非平凡 full-superposition 正类已经从条件接口升级为定理</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · FIXED 1:2 CLASS</strong><p>(r_1=R,r_2=2R,w_1=a,w_2=\lambda a)，实系数同一直线相位（同相或反相），(B=N=2)、(p=2^{-1/2})，且 (0&lt;\lambda_-\le|\lambda|\le1/8)。</p></div>
            <div class="verdict-card true"><strong>THEOREM · FULL PROPAGATOR</strong><p>(E(y)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon y}E(0))，常数只依赖固定 shape 上界，不依赖 (R,\varepsilon,\lambda) 或初值。</p></div>
            <div class="verdict-card true"><strong>COROLLARY · CROSS CUBIC</strong><p>(\mathcal C_\times\lesssim a^2N^2\sqrt\varepsilon=4a^2\sqrt\varepsilon)，继承 (U_{\rm ED}\asymp\varepsilon^{11/6}p^{4/3})。</p></div>
            <div class="verdict-card false"><strong>OPEN · GENERAL SUPERPOSITION</strong><p>任意相位、任意 carrier 集、增长 (N)、fixed-(R) 任意耦合与一般三维问题都没有由本节闭合。</p></div>
          </div>
        </section>

        <section id="reduction"><div class="section-no">01 / Exact cell reduction</div><h2>两个载波必须作为一个完整算子缩到固定圆周</h2>
          <p>在 affine invariant row (\Lambda_{R,q_*}=\{(nR,q_*):n\in\mathbb Z\}) 上令 (y=R^2x)、(\phi=R\theta)。完整 convolution 精确化为</p>
          <div class="equation result">\[
          \partial_yG=(\partial_\phi^2-R^{-2})G-is\varepsilon W_\lambda(y,\phi)G,
          \qquad W_\lambda=e^{-y}\cos\phi+\lambda e^{-4y}\cos2\phi.
          \]</div>
          <p>cell 与 (R) 无关，并保留全部 self/cross coupling；没有逐载波求和。</p>
        </section>

        <section id="shape"><div class="section-no">02 / Uniform shape lemma</div><h2>临界点固定为 (0,\pi)，Morse margin 对整个系数锥一致</h2>
          <div class="equation result">\[
          \partial_\phi W_\lambda=-e^{-y}\sin\phi\bigl(1+4\lambda e^{-3y}\cos\phi\bigr).
          \]</div>
          <p>当 (|\lambda|\le1/8) 时，括号始终位于 ([1/2,3/2])。临界集恰为 ({0,\pi})，fixed neighborhoods、cutoffs、二阶下界及 profile 范数可对 (y\in[0,1]) 和声明的 (\lambda)-族统一选择。</p>
        </section>

        <section id="theorem"><div class="section-no">03 / Uniform theorem extraction</div><h2>Coble–He 定理作用于完整 profile，统一常数来自固定 shape 数据</h2>
          <p><a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He, Theorem 1.2</a> 对单个非退化时变剪切给 modewise (e^{-c\eta^{1/2}|k|^{1/2}t}) 衰减。本站固定 critical neighborhoods 与 cutoffs，并用上一节的 uniform shape bounds 控制 Appendix A 的吸收常数，从 proof 中抽取统一 (\eta_0,C_{\rm ED},c_{\rm ED})。</p>
          <p>这是声明 1:2 参数族的 proof-level corollary，不是原论文逐字陈述的 arbitrary-family theorem，也不覆盖任意 Fourier superposition。</p>
        </section>

        <section id="compact"><div class="section-no">04 / Compact parameter completion</div><h2>小扩散定理与 (L^2) 收缩共同覆盖全部 (\varepsilon\ge1)</h2>
          <p>令 (t=\varepsilon y)、(\eta=\varepsilon^{-1})。Coble–He 控制充分小 (\eta)；剩余紧区间由 skew transport 下的精确 (L^2) 收缩补齐，并扩大同一个固定 prefactor。</p>
          <div class="equation result">\[
          E(y)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon y}E(0),\qquad
          E(1)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon}E(0),\qquad
          \int_0^1E(y)\,dy\le C_{\rm ED}\varepsilon^{-1/2}E(0).
          \]</div>
        </section>

        <section id="cubic"><div class="section-no">05 / Full cross cubic</div><h2>R0.72O 的条件门在这个 (N=2) 正类上变成无条件估计</h2>
          <div class="equation result">\[
          \mathcal C_\times\lesssim4a^2\sqrt\varepsilon,
          \qquad U_{\rm ED}\asymp\varepsilon^{11/6}p^{4/3},
          \qquad p=2^{-1/2}.
          \]</div>
          <p>这里估计完整 superposition propagator；结论不依赖把两个 one-carrier estimates 相加。</p>
        </section>

        <section id="window"><div class="section-no">06 / Physical window</div><h2>已证强耦合窗口保留精确 (p) 因子</h2>
          <div class="equation result">\[
          \boxed{\sqrt\varepsilon\lesssim p^{2/3}R^{2/3}L_{R,\varepsilon}},\qquad
          \boxed{\varepsilon\lesssim p^{4/3}R^{4/3}L_{R,\varepsilon}^{2}},
          \quad p=2^{-1/2}.
          \]</div>
          <p>窗口上沿仍只给统一有界；little-o 子区间才给 normalized ratio 衰减。fixed-(R) 任意强耦合没有闭合。</p>
        </section>

        <section id="wall"><div class="section-no">07 / Exact Morse wall</div><h2>(\lambda=\pm1/4) 是适用性墙，不是动力学反例</h2>
          <p>在 (y=0)，(\lambda=1/4) 使 (\phi=\pi) 的前三个 (\phi)-导数消失；(\lambda=-1/4) 在 (\phi=0) 同样退化，第四导数非零。越过该值还会出现额外临界点。</p>
          <p><strong>精确边界：</strong>&nbsp;(|\lambda|=1/4) 只证明当前 Morse-based theorem 不再可直接调用；它不证明 enhanced dissipation 失败，更不证明 Navier–Stokes 失稳。</p>
        </section>

        <section id="scope"><div class="section-no">08 / Scope boundary</div><h2>固定正类与一般多载波问题严格分开</h2>
          <p>已闭合：fixed real-collinear-phase 1:2 pattern、(B=2)、声明的 (\lambda)-cone、完整 affine row、任意初值与 exact-root correction。</p>
          <p>仍开放：任意相位、任意有限或增长 carrier 集、跨越 Morse wall 的 profile、fixed-(R) 任意 coupling、一般三维 continuation、有限时奇性与全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="literature"><div class="section-no">09 / Literature boundary</div><h2>一手来源提供半群框架，本站负责参数族统一化与物理回填</h2>
          <p><a href="https://arxiv.org/abs/2309.15738">Coble–He</a> 是时变非退化剪切的直接输入；<a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1112/jlms.12782">Coti Zelati–Gallay</a> 说明 profile 临界结构决定 enhanced-dissipation rate。</p>
          <p>限定检索没有找到直接陈述本站 fixed real-collinear-phase 1:2 heat-decaying profile、(R)-uniform cell reduction、full cross cubic 与物理窗口的同一现成定理；这项检索不构成新颖性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">10 / Journal figure</div><h2>正式附图同时标出正类、统一传播与适用性墙</h2>
          <p><img src="/assets/r072p/fig-r072p-superposition-gate.svg" alt="R0.72P two-carrier full-superposition enhanced-dissipation gate and Morse applicability wall"></p>
          <p><a href="/assets/r072p/fig-r072p-superposition-gate.pdf">下载 PDF</a> · <a href="/assets/r072p/fig-r072p-superposition-gate.png">下载 PNG</a> · <a href="/assets/r072p/fig-r072p-superposition-gate.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">11 / Research value</div><h2>在本项目中首次把 multi-carrier gate 在一个非平凡完整正类上严格关闭</h2>
          <p>R0.72P 的增量不是再做一条 one-carrier estimate，而是证明 cross terms 共存时的完整传播子仍有 uniform enhanced dissipation，并把它接回 (\varepsilon^{11/6}p^{4/3}) 物理账本。</p>
          <p>价值限于特殊 triangular 2.5D mechanism class；它不是一般三维稳定阈值，也不改变 Clay 问题仍开放的状态。</p>
        </section>

        <section id="next"><div class="section-no">12 / Next gate</div><h2>R0.72Q：测试相位扰动与更一般有限 pattern 的 uniform shape contract</h2>
          <p>下一步先量化 real-collinear phase locus 附近的可容许相位锥，或给出首个使 fixed critical neighborhoods 失效的精确反族。</p>
        </section>

        <section id="reproduce"><div class="section-no">13 / Reproduction</div><h2>报告、审计、证书与正式附图包</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072p_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072p_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072p_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072p_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072p">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072p-superposition-gate/fig-r072p-superposition-gate">正式附图包</a> · <a href="/notes/r0-72p.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72p.html">累计回顾</a> · <a href="/recap-r0-61-r0-72p.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72Q</span><span class="tree-state current">下一检查点</span></div>
              <h3>phase-robust finite-pattern shape contract</h3>
              <p>量化实系数同一直线相位 locus 附近的 uniform Morse cone，或构造 fixed critical neighborhoods 失效的精确反族。</p>
            </article>'''


HOME_RECAP = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72P · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 106 个节点；全站现有 166 篇公开研究笔记</h3>
            <p>累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72P 的完整逐节点索引。R0.72P 对 fixed real-collinear-phase 1:2、(B=2) 与声明的 (\lambda)-cone 证明 full-superposition ED，从而关闭一个真实 two-carrier cross-term gate。</p>
            <p>R0.70A–R0.72P 共 68 个版本已公开；44 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;固定两载波正类已闭合；arbitrary phase/carriers、fixed geometry 与一般三维问题仍开放。</p>
            <p><a href="/recap-r0-61-r0-72p.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72p.pdf">下载同步 PDF</a></p>
          </div>'''


HOME_P_CARD = r'''          <div class="task-one" id="r072p" data-release="r072p" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72P · 2026-08-27</p>
            <h3>固定实系数同一直线相位（同相或反相） 1:2 正类的完整多载波传播门已经闭合</h3>
            <p>对 (R,2R)、(B=2)、(0&lt;\lambda_-\le|\lambda|\le1/8)，完整 propagator 满足常数对 (R,\varepsilon,\lambda) 一致的 enhanced dissipation；所有 cross terms 都保留。</p>
            <p>因此 (\mathcal C_\times\lesssim4a^2\sqrt\varepsilon)，并接回 (U_{\rm ED}\asymp\varepsilon^{11/6}p^{4/3})、(p=2^{-1/2}) 的物理窗口。</p>
            <p><strong>结论边界：</strong>&nbsp;(\lambda=\pm1/4) 只是 Morse theorem-applicability wall；任意相位、一般 carrier 集、fixed-(R) 任意耦合与一般三维正则性仍开放。</p>
            <p><a href="/notes/r0-72p.html"><strong>阅读 R0.72P 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72p.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072p/fig-r072p-superposition-gate.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072p">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072p_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072p_literature_audit.md">查看文献边界审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072p-superposition-gate/fig-r072p-superposition-gate">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72p.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72p.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72Q：</strong>&nbsp;量化 phase-robust finite-pattern shape contract。</p>
          </div>'''


def validate_inputs() -> None:
    for relative in (
        "research/r072p_report-source.md",
        "research/r072p_literature_audit.md",
        "research/r072p_gap_matrix.md",
        "research/r072p_independent_audit.md",
        "research/certificates/r072p/README.md",
        "research/certificates/r072p/crosscheck.json",
        "figures/r072p-superposition-gate/fig-r072p-superposition-gate/manifest.json",
        "public/notes/r0-72o.html",
        "public/recap-r0-61-r0-72o.html",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72P release input: {relative}")
    report = (ROOT / "research/r072p_report-source.md").read_text(encoding="utf-8")
    for token in ("r_1=R", "r_2=2R", "B=2", "p=2^{-1/2}", "full-superposition", "|\\lambda|=1/4", "The Clay Millennium problem remains open"):
        if token not in report:
            raise RuntimeError(f"R0.72P report missing claim-boundary token: {token}")
    certificate = ROOT / "research/certificates/r072p"
    figure = ROOT / "figures/r072p-superposition-gate/fig-r072p-superposition-gate"
    verify_flat_hash_ledger(certificate, "R0.72P certificate")
    verify_flat_hash_ledger(figure, "R0.72P figure")
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if crosscheck.get("status") != "passed":
        raise RuntimeError("R0.72P crosscheck is not passed")
    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    publication = manifest.get("publication", {})
    if (
        manifest.get("release") != "R0.72P"
        or manifest.get("figureId") != "fig-r072p-superposition-gate"
        or manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
        or publication.get("publicCopiesComplete") is not True
        or publication.get("directory") != "public/assets/r072p"
        or publication.get("stem") != "fig-r072p-superposition-gate"
    ):
        raise RuntimeError("R0.72P figure manifest is not a complete formal seal")
    validator = ROOT / "research/validate_figure_package.py"
    completed = subprocess.run([sys.executable, str(validator), str(figure)], cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0 or json.loads(completed.stdout).get("errors") != []:
        raise RuntimeError("R0.72P strict figure validation failed")
    expected_public = []
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = ROOT / publication["directory"] / f"{publication['stem']}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72P public {suffix} is absent or not byte-identical")
        expected_public.append(str(public.relative_to(ROOT)))
    if sorted(row.get("path") for row in publication.get("assets", [])) != sorted(expected_public):
        raise RuntimeError("R0.72P manifest does not enumerate the exact public assets")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72o.html").read_text(encoding="utf-8")
    for index, (pattern, value) in enumerate((
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72P：固定实系数同一直线相位（同相或反相） 1:2 两载波的 full-superposition enhanced dissipation 与精确 Morse 适用边界。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72P｜两载波完整传播门与 Morse 墙">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="固定 1:2 正类的统一 full-superposition ED、cross cubic 与 λ=±1/4 Morse applicability wall。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072p/fig-r072p-superposition-gate.png">'),
        (r'<title>.*?</title>', '<title>R0.72P｜两载波完整传播门与 Morse 墙</title>'),
    )):
        html = section(html, pattern, value, f"note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.28", "/i18n-en.js?v=1.29", "note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#reduction">约化</a><a href="#shape">形状</a><a href="#theorem">定理</a><a href="#compact">紧区间</a><a href="#cubic">交叉项</a><a href="#window">窗口</a><a href="#wall">Morse 墙</a><a href="#scope">边界</a><a href="#literature">文献边界</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "note nav")
    html = section(html, r'    <header class="hero">.*?</header>', inline_math(NOTE_HERO), "note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#reduction">01 · cell 约化</a></li><li><a href="#shape">02 · uniform shape</a></li><li><a href="#theorem">03 · 定理抽取</a></li><li><a href="#compact">04 · 紧参数补齐</a></li><li><a href="#cubic">05 · full cross cubic</a></li><li><a href="#window">06 · 物理窗口</a></li><li><a href="#wall">07 · Morse 墙</a></li><li><a href="#scope">08 · 主张边界</a></li><li><a href="#literature">09 · 文献边界</a></li><li><a href="#figure">10 · 正式附图</a></li><li><a href="#value">11 · 研究价值</a></li><li><a href="#next">12 · R0.72Q</a></li><li><a href="#reproduce">13 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "note toc")
    html = section(html, r'      <article>.*?</article>', inline_math(NOTE_ARTICLE), "note article")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72P · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r'<footer>.*?</footer>', footer, "note footer")
    assert_clean(html, "R0.72P note")
    assert_mathjax_clean(html, "R0.72P note")
    (PUBLIC / "notes/r0-72p.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72o.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.28", "/i18n-en.js?v=1.29"),
        ("R0.61–R0.72O", "R0.61–R0.72P"),
        ("R0.61 到 R0.72O 的 105 个研究节点", "R0.61 到 R0.72P 的 106 个研究节点"),
        ("收录节点：105", "收录节点：106"),
        ("回顾截止时公开笔记：165", "回顾截止时公开笔记：166"),
        ("回顾截止节点：R0.72O", "回顾截止节点：R0.72P"),
        ("02 · 105 节完整索引", "02 · 106 节完整索引"),
        ("<strong>105</strong><span>R0.61–R0.72P 研究节点</span>", "<strong>106</strong><span>R0.61–R0.72P 研究节点</span>"),
        ("<strong>67</strong><span>R0.70A–R0.72O 已公开版本</span>", "<strong>68</strong><span>R0.70A–R0.72P 已公开版本</span>"),
        ("<strong>43</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>44</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("后面的 105 个节点", "后面的 106 个节点"),
        ("R0.70A–R0.72O 的 67 个版本已经公开；其中 43 个", "R0.70A–R0.72P 的 68 个版本已经公开；其中 44 个"),
        ("R0.61–R0.72P 的 105 节公开笔记", "R0.61–R0.72P 的 106 节公开笔记"),
        ("/recap-r0-61-r0-72o.pdf", "/recap-r0-61-r0-72p.pdf"),
    ):
        html = required(html, old, new, f"recap {old}")
    html = section(html, r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72P 的 106 个节点；最新一节闭合固定 1:2 两载波的完整传播门。">', "recap description")
    html = section(html, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十八个阶段、106 个节点：从约化递推到固定两载波 full-superposition ED。">', "recap og description")
    html = section(html, r'<title>.*?</title>', '<title>R0.61–R0.72P｜R0.60 之后的研究回顾</title>', "recap title")
    phase = r'''            <article class="phase"><h3>R0.72L–R0.72P · strong-coupling、物理回填与完整两载波传播</h3>
              <p>R0.72L–N 保留 actual ledger 并排除声明一载波上的 action-poor route；R0.72O 将 (O(a^2\sqrt\varepsilon)) cubic 回填为 (\varepsilon^{11/6}) physical numerator。</p>
              <p>R0.72P 对 fixed real-collinear-phase 1:2、(B=2)、(0&lt;\lambda_-\le|\lambda|\le1/8) 的完整 superposition 证明 uniform ED，从而闭合真实 (N=2) cross cubic。(\lambda=\pm1/4) 仅为 Morse theorem-applicability wall；任意相位与一般 carrier 集仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/notes/r0-72n.html">R0.72N</a><a href="/notes/r0-72o.html">R0.72O</a><a href="/notes/r0-72p.html">R0.72P</a><a href="/assets/r072p/fig-r072p-superposition-gate.pdf">R0.72P 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072p">R0.72P 证书</a></div></article>'''
    html = section(html, r'            <article class="phase"><h3>R0\.72L–R0\.72O .*?</article>', inline_math(phase), "recap P phase")
    node_o = '            <span class="node-ref"><a href="/notes/r0-72o.html">R0.72O</a><span class="node-state kind-conditional">条件</span></span>\n'
    node_p = '            <span class="node-ref"><a href="/notes/r0-72p.html">R0.72P</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_o, node_o + node_p, "recap P node")
    retained = r'''            <li>R0.72P 的 fixed-pattern full-superposition theorem：对实系数同一直线相位（同相或反相） (R:2R)、(B=2) 与声明的 (\lambda)-cone，完整 propagator 的 (C_{\rm ED},c_{\rm ED}) 对 (R,\varepsilon,\lambda) 一致，因而 (\mathcal C_\times\lesssim4a^2\sqrt\varepsilon)。(\lambda=\pm1/4) 只标记 Morse applicability wall。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", inline_math(retained) + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained P")
    html = section(html, r'        <section id="value">.*?</section>', inline_math(r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>一个完整两载波正类已闭合，一般 superposition 仍是独立问题</h2><p>截至 R0.72P，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 106 个节点或 68 个公开版本解释成 Clay 问题完成比例。</p><p>新的严格结果是 fixed real-collinear-phase 1:2 full-superposition ED、真实 cross cubic payment 与精确 Morse theorem-applicability wall。</p></section>'''), "recap value")
    html = section(html, r'        <section id="next">.*?</section>', inline_math(r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72Q 测试 phase-robust finite-pattern shape contract</h2><p>先量化实系数同一直线相位 locus 附近的 uniform Morse cone，或构造 fixed critical neighborhoods 失效的精确反族。</p></section>'''), "recap next")
    html = section(html, r'        <section id="claims">.*?</section>', inline_math(r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72P 的 68 节已公开；44 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。</p><p>R0.72P 只覆盖 fixed real-collinear-phase 1:2、(B=2) 与声明的 (\lambda)-cone。任意相位、一般 carrier 集、fixed-(R) 任意耦合和 Clay 正式问题保持开放。</p></section>'''), "recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', inline_math(r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72o.html">保留 R0.72O 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72p.html">打开最新节点 R0.72P</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072p">查看 R0.72P 精确证书</a> · <a href="/assets/r072p/fig-r072p-superposition-gate.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72p.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72o.pdf">上一版累计回顾 PDF</a></p><p>完整节点索引保留 R0.69W、R0.70A 以后每个公开版本及其原始编号；状态标签只描述证据类型。</p></section>'''), "recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72P 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>', "recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 106 or len(set(links)) != 106:
        raise RuntimeError(f"recap node index expected 106 unique links, got {len(links)}/{len(set(links))}")
    for slug in ["r0-69w"] + [f"r0-70{chr(c)}" for c in range(97, 123)] + [f"r0-71{chr(c)}" for c in range(97, 123)] + [f"r0-72{chr(c)}" for c in range(97, 113)]:
        if slug not in links:
            raise RuntimeError(f"recap node index missing required release: {slug}")
    assert_clean(html, "R0.72P recap")
    assert_mathjax_clean(html, "R0.72P recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72p.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.28"', 'data-site-version="1.29"'),
        ("/i18n-en.js?v=1.28", "/i18n-en.js?v=1.29"),
        ("/site-refresh.js?v=1.28", "/site-refresh.js?v=1.29"),
        ("<strong>v1.28</strong>网页版本", "<strong>v1.29</strong>网页版本"),
        ("<strong>165</strong>公开研究笔记", "<strong>166</strong>公开研究笔记"),
        ("<strong>R0.72O</strong>最新研究节点", "<strong>R0.72P</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72O", "Research topology · R0.1–R0.72P"),
        ("R0.70A–R0.72O：67 节已公开，43 节完整封存", "R0.70A–R0.72P：68 节已公开，44 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72O</span>', '<span class="route-range">R0.69P–R0.72P</span>'),
        ('aria-label="R0.69P–R0.72O"', 'aria-label="R0.69P–R0.72P"'),
        ("展开 75 篇公开笔记", "展开 76 篇公开笔记"),
        ("综述 v1.28 · 2026-08-27", "综述 v1.29 · 2026-08-27"),
        ("上次综述 v1.27 · 2026-08-27", "上次综述 v1.28 · 2026-08-27"),
        ("/recap-r0-61-r0-72o.html", "/recap-r0-61-r0-72p.html"),
        ("/recap-r0-61-r0-72o.pdf", "/recap-r0-61-r0-72p.pdf"),
    ):
        html = required(html, old, new, f"home {old}")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72P 已闭合 fixed real-collinear-phase 1:2 正类的 full-superposition ED；下一关是 phase-robust finite-pattern shape contract。</span></div>', "home focus")
    old_tail = r'R0.72O 将该结果回填 normalized physical ledger，得到 \(\varepsilon^{11/6}\) numerator 与加倍的 growing-geometry window，并把多载波问题隔离为 full-superposition ED gate。</p>'
    new_tail = old_tail[:-4] + 'R0.72P 再把 fixed real-collinear-phase 1:2、B=2 与声明的 lambda cone 缩到固定 cell，从 Coble–He proof 抽取 uniform constants，闭合完整 two-carrier cross-term gate；±1/4 只标记 Morse applicability wall。</p>'
    html = once(html, old_tail, new_tail, "home route prose")
    link_o = '<a class="milestone" href="/notes/r0-72o.html">R0.72O</a>'
    html = once(html, link_o, link_o + '\n                  <a class="milestone" href="/notes/r0-72p.html">R0.72P</a>', "home route P link")
    html = section(html, r'            <article class="tree-node next">.*?</article>', inline_math(HOME_NEXT), "home next")
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', inline_math(HOME_RECAP), "home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + inline_math(HOME_P_CARD) + '\n        </section>\n\n      </article>', "home P card")
    if html.count('data-release="r072p"') != 1:
        raise RuntimeError("home must contain exactly one R0.72P card")
    assert_clean(html, "R0.72P home")
    assert_mathjax_clean(html, "R0.72P home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.28", "/i18n-en.js?v=1.29"),
        ("本站 R0.69P–R0.72O 只列为研究笔记", "本站 R0.69P–R0.72P 只列为研究笔记"),
        ("/recap-r0-61-r0-72o.html", "/recap-r0-61-r0-72p.html"),
        ("文献综述 v1.28 · 2026-08-27", "文献综述 v1.29 · 2026-08-27"),
    ):
        html = required(html, old, new, f"literature {old}")
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72P</b><strong>full-superposition ED with explicit shape control</strong></header><p>在固定有限 carrier pattern 与 uniform Morse margin 下证明 integrated ED，或直接证明 rowwise cubic flux estimate。</p></div>'
    new_steps = '<div class="route-step closed"><header><b>R0.72P</b><strong>fixed 1:2 full-superposition ED and exact Morse wall</strong></header><p>固定实系数同一直线相位（同相或反相） 1:2、B=2 与声明的 lambda cone 后，完整 propagator 有 uniform ED，真实 cross cubic gate 闭合；±1/4 仅为 Morse theorem-applicability wall。<a href="/notes/r0-72p.html">研究笔记</a> <a href="/recap-r0-61-r0-72p.html">当前累计回顾</a> <a href="#r072p-boundary">方法边界</a></p></div>\n              <div class="route-step pause"><header><b>开放接口 · R0.72Q</b><strong>phase-robust finite-pattern shape contract</strong></header><p>量化实系数同一直线相位 locus 附近的 uniform Morse cone，或构造 fixed critical neighborhoods 失效的精确反族。</p></div>'
    html = once(html, old_open, inline_math(new_steps), "literature P route")
    boundary = r'''

          <h3 id="r072p-boundary">R0.72P 的完整两载波传播与 Morse 文献边界</h3>
          <p><a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He, Theorem 1.2</a> 给单个非退化 time-dependent shear 的 modewise enhanced dissipation。R0.72P 先把完整 (R,2R) convolution 缩到固定 cell，再利用 Appendix A 的 fixed critical neighborhoods、cutoffs 与 uniform shape bounds，从 proof 中抽取对声明 (\lambda)-family 一致的 constants；紧 (\eta)-区间由本站 (L^2) contraction 补齐。</p>
          <p><a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1112/jlms.12782">Coti Zelati–Gallay</a> 提供 stationary profile 的 hypocoercive 与 degeneracy-dependent 背景，但不直接陈述本站 heat-decaying 1:2 profile 或 physical cubic corollary。</p>
          <div class="boundary"><strong>R0.72P 的主张边界</strong><p>正结果只覆盖 fixed real-collinear-phase 1:2、(B=2)、(0&lt;\lambda_-\le|\lambda|\le1/8)。(\lambda=\pm1/4) 只证明该 Morse theorem 的适用条件退化，不证明 enhanced dissipation 失败。任意相位、任意 carrier 集或增长 (N)、fixed-(R) arbitrary coupling 与一般三维问题仍开放；限定检索不构成新颖性或优先权证明。</p></div>'''
    html = section(html, r'(<h3 id="r072o-boundary">.*?<div class="boundary">.*?</div>)', r'\1' + inline_math(boundary), "literature P boundary")
    assert_clean(html, "R0.72P literature")
    assert_mathjax_clean(html, "R0.72P literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 166:
        raise RuntimeError(f"expected 166 public HTML notes after R0.72P, got {notes}")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    expected = {
        "latestCompletedRelease": "r072o", "siteVersion": "1.28",
        "publicHtmlNoteCount": 165, "postR060RecapNodeCount": 105,
        "nextRelease": "r072p",
        "latestReleaseGate": "tests/r072o-physical-reinsertion-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072o-release.test.mjs",
        "postR070APublishedReleaseCount": 67,
        "postR070AFormalSealedReleaseCount": 43,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72O: {key}")
    release.update({
        "latestCompletedRelease": "r072p", "siteVersion": "1.29",
        "publicHtmlNoteCount": 166, "postR060RecapNodeCount": 106,
        "nextRelease": "r072q",
        "latestReleaseGate": "tests/r072p-superposition-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072p-release.test.mjs",
        "postR070APublishedReleaseCount": 68,
        "postR070AFormalSealedReleaseCount": 44,
    })
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if site.get("latestRelease") != "R0.72O" or site.get("publicHtmlNoteCount") != 165:
        raise RuntimeError("site-version is not at R0.72O")
    site.update({"version": "1.29", "latestRelease": "R0.72P", "publicHtmlNoteCount": 166, "publishedDate": "2026-08-27"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") != "r072o" or inventory.get("legacyFormalFigureBacklogCount") != 24:
        raise RuntimeError("formal archive inventory is not at R0.72O")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072o" or "r072p" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72O")
        inventory[key].append("r072p")
    inventory.update({"latestPublishedRelease": "r072p", "publishedReleaseCount": 68, "formalSealedReleaseCount": 44})
    if len(inventory["publishedReleases"]) != 68 or len(inventory["formalSealedReleases"]) != 44:
        raise RuntimeError("formal archive count mismatch after R0.72P")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-72p.html", "recap-r0-61-r0-72p.html"):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({
        "release": "R0.72P", "siteVersion": "1.29", "notes": 166,
        "recapNodes": 106, "published": 68, "formalSealed": 44,
        "legacyBacklog": 24, "phases": 28, "routeNotes": 76,
        "next": "R0.72Q",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
