#!/usr/bin/env python3
"""Generate the deterministic R0.72F Chinese web release from v1.18."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DATE = "2026-08-27"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one anchor, found {count}")
    return text.replace(old, new, 1)


def replace_between(text: str, start: str, end: str, replacement: str, label: str) -> str:
    left = text.find(start)
    if left < 0:
        raise RuntimeError(f"{label}: start anchor missing")
    right = text.find(end, left)
    if right < 0:
        raise RuntimeError(f"{label}: end anchor missing")
    return text[:left] + replacement + text[right:]


def normalize_r072f_math(text: str) -> str:
    """Repair early v1.19 prose that used parentheses instead of MathJax delimiters."""
    pairs = [
        ("selected-root (1/3) 下端点", r"selected-root \(1/3\) 下端点"),
        ("Leray-payment (1/2) 上端点", r"Leray-payment \(1/2\) 上端点"),
        (
            r"(w_{\beta,\gamma}=s^{-\beta}[1+\log(1/s)]^\gamma)",
            r"\(w_{\beta,\gamma}=s^{-\beta}[1+\log(1/s)]^\gamma\)",
        ),
        (
            r"(w_*=s^{-1/3}[1+\log(1/s)])",
            r"\(w_*=s^{-1/3}[1+\log(1/s)]\)",
        ),
        (
            r"(w_*(s)=s^{-1/3}[1+\log(1/s)])",
            r"\(w_*(s)=s^{-1/3}[1+\log(1/s)]\)",
        ),
        (r"(4.76\times10^{-4})", r"\(4.76\times10^{-4}\)"),
        ("固定 (w_*)", r"固定 \(w_*\)"),
        (
            r"(s^{-1/3}[1+\log(1/s)])",
            r"\(s^{-1/3}[1+\log(1/s)]\)",
        ),
        ("本站 R0.69P–R0.72E 路线", "本站 R0.69P–R0.72F 路线"),
    ]
    for old, new in pairs:
        text = text.replace(old, new)
    return text


NOTE_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta name="description" content="研究笔记 R0.72F：临界对数初始层权重同时通过 R0.72E selected-root 反例筛查与 Leray 能量支付；完整根估计仍开放。">
  <meta property="og:type" content="article">
  <meta property="og:title" content="R0.72F｜临界对数初始层修正与可行窗口">
  <meta property="og:description" content="selected-root 阈值为 1/3，能量支付阈值为 1/2；最小边界权重是 s^{-1/3}(1+log(1/s))。">
  <meta property="og:image" content="https://kasifa.github.io/figures/r0-72f-critical-log-window.png">
  <title>R0.72F｜临界对数初始层修正与可行窗口</title>
  <script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.90">
  <style>.hero h1{font-size:clamp(1.62rem,3.5vw,2.9rem)}pre{max-width:100%;overflow-x:auto}.audit-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem}.audit-card{border:1px solid var(--line);padding:1rem}.audit-card strong{display:block;color:var(--gold);font-family:var(--mono);margin-bottom:.45rem}@media(max-width:760px){.audit-grid{grid-template-columns:1fr}}@media print{body{font-size:8.7pt}.topline{height:3px}pre{max-width:none;overflow:visible!important;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-size:7.3pt}}</style>
  <script defer src="/i18n-en.js?v=1.19"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#payment">能量支付</a><a href="#family">精确族</a><a href="#frontier">统一边界</a><a href="#audit">证书</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72F · CRITICAL LOG · INITIAL LAYER · ENERGY PAYMENT</div>
        <h1>两道阈值之间，<br>只留下一个临界对数入口</h1>
        <p class="lead">R0.72E 排除了无权候选 \(D^{1/3}\Lambda_1\)。这一节不任意加一个修正项，而是把初始层权重写成 \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\)，分别计算 exact Bessel family 的必要阈值和 Leray 能量可以支付的充分阈值。selected roots 强制 \(\beta\ge1/3\)，纯幂端点还缺一个对数；能量只允许 \(\beta<1/2\)。因此最小边界候选是 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72F 完成</span><strong>critical-log repair selected</strong><p>版本 v0.72F · 2026-08-27</p><p>energy payment: CLOSED</p><p>selected-family frontier: CLOSED</p><p>complete-root estimate: OPEN</p><p>下一对象：all-root trace packing</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节判断</a></li><li><a href="#payment">01 · Leray 支付</a></li><li><a href="#family">02 · 精确族阈值</a></li><li><a href="#frontier">03 · 统一边界</a></li><li><a href="#audit">04 · 双路证书</a></li><li><a href="#figure">05 · 正式附图</a></li><li><a href="#value">06 · 研究价值</a></li><li><a href="#next">07 · 下一步</a></li><li><a href="#claims">08 · 主张边界</a></li><li><a href="#reproduce">09 · 复现</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Direct verdict</div><h2>临界对数权重是两项有限筛查共同允许的最小边界候选</h2>
          <p>对 \(I=[a,a+T]\)，令 \(Y=\|\omega\|_2^2\)、\(L=\mathbb P(u\times\omega)\)，并定义</p>
          <div class="equation result">\[
            \mathscr A_{\beta,\gamma}(I;u)=\frac1T\int_I
            w_{\beta,\gamma}\!\left(\frac{t-a}{T}\right)
            \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}\,dt,
            \qquad
            \Lambda_{1,\beta,\gamma}=\mathcal R_Y[\nu^2+\mathscr A_{\beta,\gamma}].
          \]</div>
          <div class="equation result">\[
            \boxed{\left\{\frac13<\beta<\frac12,\ \gamma\ge0\right\}
            \cup\left\{\beta=\frac13,\ \gamma\ge1\right\}.}
          \]</div>
          <p>这里的“可行”只表示同时没有被当前 selected-root family 排除，而且新增 action 可由 Leray 能量支付。它不表示完整根估计已经成立。</p>
          <div class="equation result">\[
            \boxed{w_*(s)=s^{-1/3}[1+\log(1/s)],\qquad \|w_*\|_2^2=75.}
          \]</div>
        </section>

        <section id="payment"><div class="section-no">01 / Leray payment</div><h2>能量级信息给出严格的 \(1/2\) 上端点</h2>
          <p>Sobolev 对偶、Hölder 和周期 Gagliardo–Nirenberg 不等式给</p>
          <div class="equation result">\[
            \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{\|\omega\|_2^2}
            \le C_{\mathbb T^3}\|u\|_2\|\omega\|_2.
          \]</div>
          <p>在强能量不等式成立的每个 restart time \(a\)，Cauchy–Schwarz 随后给</p>
          <div class="equation result">\[
            \boxed{\mathscr A_{\beta,\gamma}([a,a+T];u)
            \le C_{\mathbb T^3}\|w_{\beta,\gamma}\|_2
            \frac{\|u(a)\|_2^2}{\sqrt{2\nu T}},\qquad \beta<\frac12.}
          \]</div>
          <p>仅凭 \(Y\in L_t^1\)，端点不能延长到 \(\beta\ge1/2\)。用于说明尖锐性的 \(Y(t)=t^{-p}\) 和 \(Y(t)=1/[t\log^2(e/t)]\) 只是标量预算轮廓，不是 Navier–Stokes 涡量轨道。</p>
        </section>

        <section id="family"><div class="section-no">02 / Exact family screen</div><h2>selected Bessel roots 强制 \(1/3\) 与一个端点对数</h2>
          <p>沿用 R0.72E 的 exact triangular family，固定 \(q_0\)，取 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、\(S_R^2=\delta_R/\log(2+\delta_R)\)。对每个固定 \(0<\beta<1\)、\(\gamma\ge0\)，解析上下界为</p>
          <div class="equation result">\[
            Q_{\beta,\gamma,\delta,q_0}(X)
            \asymp\delta^{\beta-1}(\log\delta)^\gamma,
            \qquad
            \mathscr A_{\beta,\gamma}(u_R)
            \asymp\delta_R^\beta(\log\delta_R)^{\gamma-1}.
          \]</div>
          <p>前 \(R\) 个 selected roots 的质量为 \(\mathcal J_{{\rm sel},R}\asymp\delta_R\)，而 \(D_R^{1/3}\asymp\delta_R^{2/3}\)。因此</p>
          <div class="equation result">\[
            \frac{\mathcal J_{{\rm sel},R}}
            {D_R^{1/3}\Lambda_{1,\beta,\gamma}}
            \asymp\delta_R^{1/3-\beta}(\log\delta_R)^{1-\gamma}.
          \]</div>
          <p>所有 \(\beta<1/3\) 失败；\(\beta=1/3\) 时 \(\gamma<1\) 失败。\(w_*\) 使这一个 selected ratio 保持常数量级，但没有控制 selected neighborhoods 之外的其他根。</p>
        </section>

        <section id="frontier"><div class="section-no">03 / Free-amplitude frontier</div><h2>三种修正位于同一个增广多项式边界</h2>
          <p>把 active amplitude \(X_\delta=S_\delta^2\) 留作自由参数。对 \(0<\beta<1\)，选择 \(X_\delta=\delta^{1-\beta}(\log\delta)^{-\gamma}\) 让 action 保持有界。若数据坐标为 \(\mathfrak C\asymp\delta^2\)、coupling 坐标为 \(\Gamma\asymp\delta\)，则 raw selected ledger 强制</p>
          <div class="equation result">\[
            \boxed{2a+c+\beta>1,
            \quad\text{或}\quad2a+c+\beta=1\ \text{且}\ \gamma\ge1.}
          \]</div>
          <p>在历史数据指数 \(a=1/3\) 上，三个边界顶点分别是 critical-log action、\(c=1/3\) coupling payment，以及改变左端根账本后的 \(\alpha=4/9\) atom weight。后两者使用 \(\beta=0\) 的独立对数律，不能被冒充为上式的正 \(\beta\) 端点。</p>
          <p>固定初始 Fourier 支撑的有限个振幅归一化频率矩都趋向常数，因此看不见这一 amplitude-driven 时间尺度。</p>
        </section>

        <section id="audit"><div class="section-no">04 / Independent certificates</div><h2>两种演化与两种奇点求积给出一致的有限审计</h2>
          <div class="audit-grid">
            <div class="audit-card"><strong>PRODUCER · ALL CHECKS PASS</strong><p>512-mode time-dependent Strang split-step Fourier；每一步对奇异权重使用精确零阶和一阶矩。临界归一化从 41.0235 变到 44.1958；fine/coarse 最大相对差 \(1.27\times10^{-3}\)。</p></div>
            <div class="audit-card"><strong>INDEPENDENT · ALL CHECKS PASS</strong><p>实不变格点上的 implicit BDF；沿自适应网格作 Gauss–Legendre 求积，并用 \(x=e^{-z}\) 处理 launch tail。临界归一化从 41.0430 变到 44.2103。</p></div>
          </div>
          <p>两路所有权重、所有六个 \(\delta\) 点的最大逐点相对差为 \(4.76\times10^{-4}\)。独立路径的半径压力小于 \(1.28\times10^{-7}\)，容差压力小于 \(6.64\times10^{-7}\)，最大格点边界能量分数小于 \(8.47\times10^{-42}\)。这些是 binary64 有限审计，不是区间证明。</p>
        </section>

        <section id="figure"><div class="section-no">05 / Journal figure</div><h2>正式附图把两个阈值、有限渐近与三顶点边界分开</h2>
          <figure><img src="/figures/r0-72f-critical-log-window.svg" alt="R0.72F critical-log admissible window, weighted action audit, and augmented frontier"><figcaption>图 R0.72F-1。左：selected-root 与 Leray-payment 阈值；中：producer 与 independent 的临界归一化；右：增广 frontier 的三个修正顶点。图中有限值只佐证解析标度。</figcaption></figure>
        </section>

        <section id="value"><div class="section-no">06 / Research value</div><h2>这一节把“怎么修”压成一个可证伪候选</h2>
          <p>价值不在于增加一个任意强范数，而在于同时给出必要下端点、可支付上端点和最小边界权重。R0.72E 的失败现在被压缩成一个明确问题：critical-log action 是否足以支付完整 raw root ledger。</p>
          <p>这仍没有缩小潜在奇性解的集合，也没有给出 continuation criterion。它只把下一次失败或成功变成一项边界清楚的 trace-packing 定理。</p>
        </section>

        <section id="next"><div class="section-no">07 / Next finite gate</div><h2>R0.72G 只检查完整根，不再移动候选</h2>
          <p>下一步固定 \(w_*\)，先在 exact triangular class 内证明或否定</p>
          <div class="equation result">\[
            \mathcal J_{\rm all}(I)\stackrel{?}{\le}
            C D^{1/3}\mathcal R_Y(I)[\nu^2+\mathscr A_{1/3,1}(I;u)].
          \]</div>
          <p>有限关口必须包含所有根、restart covering 和 left-end cost。只重复 selected Bessel roots 不算推进。</p>
        </section>

        <section id="claims"><div class="section-no">08 / Claim boundary</div><h2>本节证明什么，也明确不证明什么</h2>
          <ul>
            <li><strong>已证明：</strong>Leray 支付、能量信息类的 \(1/2\) 尖锐性、exact family 的 regularly varying action 渐近、selected-family frontier 和 critical-log saturation。</li>
            <li><strong>未证明：</strong>critical-log action 对 complete roots 的上界、restart/dyadic covering、\(\mathcal R_Y\) 的普适支付，以及向非三角形动力学的传递。</li>
            <li><strong>没有得到：</strong>新继续性判据、有限时奇性、一般三维 global regularity、原创性或优先权结论。</li>
          </ul>
        </section>

        <section id="reproduce"><div class="section-no">09 / Reproduce</div><h2>证明、文献、双路证书、附图和累计回顾完整保留</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_independent_audit.md">独立逐式审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072f">producer / independent 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072f-critical-log-window/fig-r072f-critical-log-window">附图、数据、manifest、validation 与源代码包</a> · <a href="/figures/r0-72f-critical-log-window.pdf">期刊附图 PDF</a></p>
          <p><a href="/notes/r0-72f.pdf">下载同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72f.html">阅读 R0.60 之后累计回顾</a> · <a href="/recap-r0-61-r0-72f.pdf">下载累计回顾 PDF</a></p>
          <pre><code>python3 research/r072f_exact_audit.py --output research/certificates/r072f/result.json
python3 research/r072f_independent_audit.py --output research/certificates/r072f/independent-result.json
python3 figures/r072f-critical-log-window/fig-r072f-critical-log-window/build_figure.py
python3 figures/r072f-critical-log-window/fig-r072f-critical-log-window/qa_images.py
python3 figures/r072f-critical-log-window/fig-r072f-critical-log-window/validate.py</code></pre>
        </section>
      </article>
    </div>
  </main>
  <footer><div>R0.72F · 2026-08-27 · 个人数学研究日志<br><a href="/">返回研究主页</a> · <a href="/literature-review.html">文献综述</a> · <a href="/recap-r0-61-r0-72f.html">累计回顾</a></div></footer>
</body>
</html>
'''


RECAP_PHASE_F = r'''            <article class="phase"><h3>R0.72F · 临界对数初始层修正与统一 selected-family frontier</h3>
              <p>对 \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\)，Leray 能量在 \(\beta&lt;1/2\) 时支付对应 projected-Lamb action；仅凭 \(Y\in L_t^1\)，这个 \(1/2\) 端点不能改善。R0.72E exact family 则给 \(Q_{\beta,\gamma}\asymp\delta^{\beta-1}(\log\delta)^\gamma\)，使 selected-root ratio 按 \(\delta^{1/3-\beta}(\log\delta)^{1-\gamma}\) 缩放。最小共同边界因此是 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)，且 \(\|w_*\|_2^2=75\)。</p>
              <p>允许 active amplitude 自由变化后，正 \(\beta\) raw ledger 的必要边界为 \(2a+c+\beta&gt;1\)，或等号且 \(\gamma\ge1\)。在历史 \(a=1/3\) 上，critical-log action、\(c=1/3\) coupling factor 与改变左端量的 \(\alpha=4/9\) root weight 构成三个增广顶点。当前只通过 selected roots 与 Leray payment 两项筛查；complete-root trace inequality 仍未证明。</p>
              <div class="links"><a href="/notes/r0-72f.html">R0.72F</a><a href="/figures/r0-72f-critical-log-window.pdf">R0.72F 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072f">R0.72F 证书</a></div></article>
'''


def build_recap() -> str:
    path = PUBLIC / "recap-r0-61-r0-72e.html"
    html = path.read_text(encoding="utf-8")
    repeated_scope = "R0.61 到 R0.72E 的 95 个研究节点"
    if html.count(repeated_scope) != 2:
        raise RuntimeError("recap repeated scope anchor must occur twice")
    html = html.replace(repeated_scope, "R0.61 到 R0.72F 的 96 个研究节点")
    repeated_title = "R0.61–R0.72E｜R0.60 之后的研究回顾"
    if html.count(repeated_title) != 2:
        raise RuntimeError("recap repeated title anchor must occur twice")
    html = html.replace(repeated_title, "R0.61–R0.72F｜R0.60 之后的研究回顾")
    replacements = [
        ("二十二个阶段、95 个节点", "二十三个阶段、96 个节点"),
        ('/i18n-en.js?v=1.18', '/i18n-en.js?v=1.19'),
        ("累计回顾 · R0.61–R0.72E", "累计回顾 · R0.61–R0.72F"),
        ("<strong>R0.61–R0.72E</strong>", "<strong>R0.61–R0.72F</strong>"),
        ("收录节点：95", "收录节点：96"),
        ("回顾截止时公开笔记：155", "回顾截止时公开笔记：156"),
        ("回顾截止节点：R0.72E", "回顾截止节点：R0.72F"),
        ("01 · 二十二个研究阶段", "01 · 二十三个研究阶段"),
        ("R0.60 之后的路线分成二十二个阶段", "R0.60 之后的路线分成二十三个阶段"),
        ("02 · 95 节完整索引", "02 · 96 节完整索引"),
        ("<strong>95</strong><span>R0.61–R0.72E 研究节点</span>", "<strong>96</strong><span>R0.61–R0.72F 研究节点</span>"),
        ("<strong>57</strong><span>R0.70A–R0.72E 已公开并封存版本</span>", "<strong>58</strong><span>R0.70A–R0.72F 已公开版本</span>\n            <div class=\"metric\"><strong>34</strong><span>当前 formal-figure 合同下完整封存</span></div>\n            <div class=\"metric\"><strong>24</strong><span>旧版 formal-figure 档案待回补</span></div>"),
        ("<strong>22</strong><span>按问题划分的研究阶段</span>", "<strong>23</strong><span>按问题划分的研究阶段</span>"),
        ("后面的 95 个节点", "后面的 96 个节点"),
        ("R0.70A–R0.72E 的 57 个版本已经公开并封存", "R0.70A–R0.72F 的 58 个版本已经公开；其中 34 个满足当前 formal-figure 完整封存合同"),
        ("R0.61–R0.72E 的 95 节公开笔记", "R0.61–R0.72F 的 96 节公开笔记"),
        ("R0.61–R0.72E 回顾", "R0.61–R0.72F 回顾"),
    ]
    for old, new in replacements:
        html = replace_once(html, old, new, f"recap {old[:30]}")

    phase_anchor = '              <div class="links"><a href="/notes/r0-72e.html">R0.72E</a><a href="/figures/r0-72e-supercritical-ledger.pdf">R0.72E 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072e">R0.72E 证书</a></div></article>\n'
    html = replace_once(html, phase_anchor, phase_anchor + RECAP_PHASE_F, "recap phase F")
    node_anchor = '            <span class="node-ref"><a href="/notes/r0-72e.html">R0.72E</a><span class="node-state kind-negative">否</span></span>\n'
    node_f = '            <span class="node-ref"><a href="/notes/r0-72f.html">R0.72F</a><span class="node-state kind-closed">闭</span></span>\n'
    html = replace_once(html, node_anchor, node_anchor + node_f, "recap node F")
    retained_f = r'''            <li>R0.72F 的 critical-log repair screen：\(\mathscr A_{\beta,\gamma}\) 在 \(\beta&lt;1/2\) 时由 Leray 能量支付；R0.72E exact family 则强制 \(\beta&gt;1/3\)，或在端点取 \(\gamma\ge1\)。最小边界权重 \(w_*=s^{-1/3}[1+\log(1/s)]\) 恰好饱和 selected obstruction，free-amplitude audit 进一步给出增广必要 frontier。完整根上界、restart covering 与一般三维传递仍开放。</li>'''
    retained_start = html.find('            <li>R0.72E 的 one-carrier supercritical no-go：')
    if retained_start < 0:
        raise RuntimeError("recap retained F start missing")
    retained_end = html.find("</li>", retained_start)
    if retained_end < 0:
        raise RuntimeError("recap retained F end missing")
    retained_end += len("</li>")
    html = html[:retained_end] + "\n" + retained_f + html[retained_end:]

    value_next = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>最小修正已经被选定，但完整根桥仍未建立</h2>
          <p>截至 R0.72F，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 96 个节点或 58 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72E 排除 unweighted candidate；R0.72F 又证明，任意 regularly varying initial-layer repair 都必须同时跨过 selected-root 的 \(1/3\) 下端点与 Leray payment 的 \(1/2\) 上端点。临界纯幂仍缺一个对数，所以 \(w_*=s^{-1/3}[1+\log(1/s)]\) 是下一步唯一固定候选。</p>
          <p>这是一项 proof-route design theorem，不是 regularity theorem。它的价值是禁止继续移动目标，把下一关压成 complete-root trace packing。</p>
        </section>

        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72G 固定 \(w_*\)，只审完整根 trace packing</h2>
          <p>下一有限任务在 exact triangular class 内先证明或否定 \(\mathcal J_{\rm all}\le CD^{1/3}\Lambda_{1,*}\)。证书必须包含 selected neighborhoods 之外的全部根、restart covering 和左端成本。</p>
          <p>若 complete ratio 仍发散，就关闭这一修正；若 exact class 内成立，再检查一般三维 Hilbert trace theorem 和 Leray 级付款。不会再用新的自由参数临时移动候选。</p>
        </section>

'''
    html = replace_between(html, '        <section id="value">', '        <section id="claims">', value_next, "recap value-next")
    claims = r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>“已公开”和“完整封存”从本版起分开计数</h2>
          <p>R0.70A–R0.72F 的 58 节 HTML/PDF 与研究源稿均已公开。按当前 formal-figure 合同，34 节完整封存；24 节较早版本仍缺 formal 状态或正式附图包，列入可审计的旧档回补清单。公开页存在不等于档案合同完整。</p>
          <p>本回顾没有证明三维 Navier–Stokes 的全局光滑性或有限时破裂。Clay 正式问题仍然开放。</p>
        </section>

'''
    html = replace_between(html, '        <section id="claims">', '        <section id="reproduce">', claims, "recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72e.html">保留 R0.72E 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72f.html">打开最新节点 R0.72F</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072f">查看 R0.72F 双路证书</a> · <a href="/recap-r0-61-r0-72f.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72e.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>
'''
    html = replace_between(html, '        <section id="reproduce">', '      </article>', reproduce, "recap reproduce")
    return html


def update_home(html: str) -> str:
    html = html.replace('/site-refresh.js?v=1.18', '/site-refresh.js?v=1.19')
    if 'data-site-version="1.19"' in html:
        return normalize_r072f_math(html)
    if 'data-site-version="1.18"' not in html:
        raise RuntimeError("home is neither v1.18 nor v1.19")
    html = html.replace('/recap-r0-61-r0-72e', '/recap-r0-61-r0-72f')
    pairs = [
        ('data-site-version="1.18"', 'data-site-version="1.19"'),
        ('/i18n-en.js?v=1.18', '/i18n-en.js?v=1.19'),
        ('<strong>v1.18</strong>网页版本', '<strong>v1.19</strong>网页版本'),
        ('<strong>155</strong>公开研究笔记', '<strong>156</strong>公开研究笔记'),
        ('<strong>R0.72E</strong>最新研究节点', '<strong>R0.72F</strong>最新研究节点'),
        ('<strong>frequency-sensitive repair after candidate-payment failure</strong>当前方向', '<strong>complete-root trace packing for the critical-log repair</strong>当前方向'),
        ('Research topology · R0.1–R0.72E', 'Research topology · R0.1–R0.72F'),
        ('R0.70A–R0.72E 已公开并封存版本', 'R0.70A–R0.72F：58 节已公开，34 节完整封存'),
        ('<span class="route-range">R0.69P–R0.72E</span>', '<span class="route-range">R0.69P–R0.72F</span>'),
        ('<summary>展开 65 篇公开笔记</summary>', '<summary>展开 66 篇公开笔记</summary>'),
        ('aria-label="R0.69P–R0.72E"', 'aria-label="R0.69P–R0.72F"'),
        ('综述 v1.18 · 2026-08-27', '综述 v1.19 · 2026-08-27'),
        ('上次综述 v1.17 · 2026-08-27', '上次综述 v1.18 · 2026-08-27'),
    ]
    for old, new in pairs:
        html = replace_once(html, old, new, f"home {old[:30]}")
    html = replace_once(
        html,
        'R0.72E 已在 exact smooth class 中排除候选 \(D^{1/3}\Lambda_1\) complete-root payment；下一步寻找最小的 frequency-sensitive repair，并检查它是否仍由 Leray 级信息支付。',
        'R0.72F 已把修正压缩到 critical-log initial-layer action；下一步固定这个候选，检查它能否支付 complete-root trace packing。',
        "home summary",
    )
    html = replace_once(
        html,
        'R0.72E 固定 \(q_0&gt;R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。</p>',
        'R0.72E 固定 \(q_0&gt;R_*\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \(H^{-1}\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。</p>',
        "home route paragraph",
    )
    html = replace_once(
        html,
        'candidate D^{1/3}Λ₁ payment failure</p>',
        'candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier</p>',
        "home route path",
    )
    nav_anchor = '                  <a class="milestone" href="/notes/r0-72e.html">R0.72E</a>\n'
    html = replace_once(html, nav_anchor, nav_anchor + '                  <a class="milestone" href="/notes/r0-72f.html">R0.72F</a>\n', "home nav F")

    next_old = r'''          <div class="tree-row">
            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72F</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>frequency-sensitive repair after candidate-payment failure</h3>
              <p>依次测试 initial-layer frequency charge、time-weighted rotational action 和显式 coupling-scale data term。候选必须先阻断 R0.72E exact family，再证明它不等价于尚未知的临界范数。</p>
            </article>
          </div>'''
    next_new = r'''          <div class="tree-row">
            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72G</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>complete-root trace packing for the critical-log repair</h3>
              <p>固定 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)，把全部根、restart covering 与 left-end cost 放进同一个 estimate；不再移动候选。</p>
            </article>
          </div>'''
    html = replace_once(html, next_old, next_new, "home next card")

    recap_new = r'''            <p class="eyebrow">累计回顾 R0.61–R0.72F · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 96 个节点；全站现有 156 篇公开研究笔记</h3>
            <p>累计回顾按二十三个阶段覆盖 R0.61–R0.72F。R0.72E 排除 unweighted payment；R0.72F 给出 selected-root \(1/3\) 下端点、Leray-payment \(1/2\) 上端点与 critical-log 最小边界。R0.70A–R0.72F 共 58 个版本已公开；按当前 formal-figure 合同有 34 个完整封存，24 个旧版附图档案列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72F 只把下一候选固定为 critical-log action；complete-root estimate 仍开放。</p>'''
    html = replace_between(
        html,
        '            <p class="eyebrow">累计回顾 R0.61–R0.72E',
        '            <p><a href="/recap-r0-61-r0-72f.html"',
        recap_new + "\n",
        "home recap card",
    )

    tail_old = r'''            <p><strong style="color:var(--gold)">下一步 R0.72F：</strong>&nbsp;寻找最小 frequency-sensitive repair，并要求它同时阻断当前 exact family、又能由已知 NSE 预算支付。</p>
          </div>'''
    tail_new = r'''            <p><strong style="color:var(--gold)">R0.72F 已完成：</strong>&nbsp;regularly varying initial-layer repair 的两道阈值已经封闭；critical-log weight 是最小边界候选。</p>
          </div>

          <div class="task-one" id="r072f" data-release="r072f" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72F · 2026-08-27</p>
            <h3>临界对数初始层修正同时通过 selected-root 与 Leray-payment 筛查</h3>
            <p>对 \(w_{\beta,\gamma}=s^{-\beta}[1+\log(1/s)]^\gamma\)，Leray energy 在 \(\beta&lt;1/2\) 时支付 action；R0.72E exact family 则强制 \(\beta&gt;1/3\)，或在端点取 \(\gamma\ge1\)。</p>
            <p>最小边界权重为 \(w_*=s^{-1/3}[1+\log(1/s)]\)，且 \(\|w_*\|_2^2=75\)。两路有限审计在 \(\delta=16,\ldots,512\) 上逐点一致到 \(4.76\times10^{-4}\) 以内。</p>
            <p><strong>结论边界：</strong>&nbsp;这只是 viable-candidate theorem。critical-log action 尚未支付 complete-root ledger，也没有给出 continuation criterion。</p>
            <p><a href="/notes/r0-72f.html"><strong>阅读 R0.72F 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72f.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72f-critical-log-window.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072f">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072f_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072f-critical-log-window/fig-r072f-critical-log-window">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72f.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72f.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72G：</strong>&nbsp;固定 \(w_*\)，检查 complete-root trace packing、restart covering 与 left-end cost。</p>
          </div>'''
    html = replace_once(html, tail_old, tail_new, "home release F")
    return normalize_r072f_math(html)


def update_literature(html: str) -> str:
    if '/i18n-en.js?v=1.19' in html:
        return normalize_r072f_math(html)
    html = html.replace('/recap-r0-61-r0-72e', '/recap-r0-61-r0-72f')
    pairs = [
        ('/i18n-en.js?v=1.18', '/i18n-en.js?v=1.19'),
        ('本站 R0.69P–R0.72E 只列为研究笔记', '本站 R0.69P–R0.72F 只列为研究笔记'),
        ('累计回顾与 95 节索引', '累计回顾与 96 节索引'),
        ('打开 95 节完整索引', '打开 96 节完整索引'),
        ('文献综述 v1.18 · 2026-08-27', '文献综述 v1.19 · 2026-08-27'),
    ]
    for old, new in pairs:
        html = replace_once(html, old, new, f"literature {old[:30]}")
    html = replace_once(
        html,
        'R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。一般 Navier–Stokes 正则性仍开放。',
        'R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \(D^{1/3}\Lambda_1\) payment 按 \(R^{4/3}\) 发散。R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。一般 Navier–Stokes 正则性仍开放。',
        "literature deck F",
    )
    old_route = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72F</b><strong>frequency-sensitive repair</strong></header><p>候选修正必须先阻断 R0.72E exact family，再证明它能由 Leray 级或已知 continuation budget 支付。</p></div>'''
    new_route = r'''              <div class="route-step closed"><header><b>R0.72F</b><strong>critical-log initial-layer repair 与可行窗口</strong></header><p>selected Bessel roots 强制 \(\beta\ge1/3\)，纯幂端点还需 \(\gamma\ge1\)；Leray energy 只支付 \(\beta&lt;1/2\)。最小边界权重是 \(s^{-1/3}[1+\log(1/s)]\)。这只通过两项筛查，不是 complete-root theorem。<a href="/notes/r0-72f.html">研究笔记</a> <a href="/recap-r0-61-r0-72f.html">当前累计回顾</a> <a href="#r072f-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72G</b><strong>complete-root trace packing</strong></header><p>固定 critical-log weight，检查全部 roots、restart covering 与 left-end cost；不再更换候选。</p></div>'''
    html = replace_once(html, old_route, new_route, "literature route F/G")
    boundary_f = r'''
          <h3 id="r072f-boundary">R0.72F 的 weighted-action 与时间迹边界</h3>
          <p><a href="#ref-8">Koch–Tataru</a> 的 critical (BMO^{-1}) solution space、<a href="#ref-87">Tao</a> 的 quantitative regularity framework、<a href="#ref-88">Chemin–Planchon</a> 的 time-weighted nonlinear remainder、<a href="#ref-40">Cheskidov–Dai</a> 的动态频率 occupation 与 <a href="#ref-29">Yu</a> 的 filtered palinstrophy defect 都提供邻近结构，但没有一项同时给出 arbitrary large-data/Leray payment、fixed-support amplitude coupling detection 与 distinguished temporal zero-level squared-slope ledger。</p>
          <div class="boundary"><strong>R0.72F 的主源边界</strong><p>本节的 Leray payment 是 Sobolev 对偶、插值和能量不等式的直接推导；critical-log selected-family law 来自 R0.72E exact family。核对的一手来源不陈述 complete-root candidate，也不支持把通过两项筛查升级为 continuation criterion。文献审计是截至 2026-08-27 的 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p></div>'''
    html = replace_once(
        html,
        '          <ol class="criteria">',
        boundary_f + '\n          <ol class="criteria">',
        "literature boundary F",
    )
    ref_anchor = '            <li id="ref-86">S. Kusuoka and D. Stroock. <a href="https://doi.org/10.15083/00039520"><em>Applications of the Malliavin calculus, Part II</em></a>. J. Fac. Sci. Univ. Tokyo Sect. IA Math. 32 (1985), 1–76; Corollary (3.25) and inequality (3.27), pp. 22–23.</li>'
    refs = r'''
            <li id="ref-87">T. Tao. <a href="https://arxiv.org/abs/0710.1604"><em>A quantitative formulation of the global regularity problem for the periodic Navier–Stokes equation</em></a>. Dyn. Partial Differ. Equ. 4 (2007).</li>
            <li id="ref-88">J.-Y. Chemin and F. Planchon. <a href="https://arxiv.org/abs/1111.1356"><em>Self-improving bounds for the Navier–Stokes equations</em></a>. Bull. Soc. Math. France 140 (2012).</li>
            <li id="ref-89">Y. Yang. <a href="https://arxiv.org/abs/2308.09350"><em>Trace theorems for Sobolev spaces on submanifolds</em></a>. Preprint and J. Differential Equations version.</li>'''
    html = replace_once(html, ref_anchor, ref_anchor + refs, "literature refs F")
    return normalize_r072f_math(html)


def update_manifest(text: str) -> str:
    data = json.loads(text)
    if data.get("latestCompletedRelease") == "r072f":
        return text
    if data.get("latestCompletedRelease") != "r072e":
        raise RuntimeError("manifest latest release is not r072e")
    data.update(
        {
            "latestCompletedRelease": "r072f",
            "siteVersion": "1.19",
            "publicHtmlNoteCount": 156,
            "postR060RecapNodeCount": 96,
            "postR070APublishedReleaseCount": 58,
            "postR070AFormalSealedReleaseCount": 34,
            "legacyFormalFigureBacklogCount": 24,
            "nextRelease": "r072g",
            "latestReleaseGate": "tests/r072f-critical-log-window-gate.test.mjs",
            "completionRule": "A new release is formal-sealed only after its analytic proof or stated negative result, required certificates, independent audit, formal figure package, synchronized HTML/PDF, cumulative recap, literature boundary, bilingual dictionary, and publication tests pass. Published and formal-sealed historical counts are tracked separately.",
        }
    )
    data.pop("postR070ASealedReleaseCount", None)
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def update_site_version(text: str) -> str:
    data = json.loads(text)
    data.update(
        {
            "version": "1.19",
            "latestRelease": "R0.72F",
            "publicHtmlNoteCount": 156,
            "publishedDate": DATE,
        }
    )
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")


def main() -> None:
    note = PUBLIC / "notes" / "r0-72f.html"
    recap = PUBLIC / "recap-r0-61-r0-72f.html"
    home = PUBLIC / "research-review.html"
    literature = PUBLIC / "literature-review.html"
    manifest = ROOT / "research" / "release-manifest.json"
    site_version = PUBLIC / "site-version.json"
    write(note, NOTE_HTML)
    write(recap, build_recap())
    write(home, update_home(home.read_text(encoding="utf-8")))
    write(literature, update_literature(literature.read_text(encoding="utf-8")))
    write(manifest, update_manifest(manifest.read_text(encoding="utf-8")))
    write(site_version, update_site_version(site_version.read_text(encoding="utf-8")))
    print(json.dumps({"release": "R0.72F", "siteVersion": "1.19", "noteCount": len(list((PUBLIC / "notes").glob("*.html"))), "recapNodes": 96}, ensure_ascii=False))


if __name__ == "__main__":
    main()
