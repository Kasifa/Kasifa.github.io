#!/usr/bin/env python3
"""Generate the deterministic R0.72G Chinese web release from site v1.19."""

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


NOTE_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta name="description" content="研究笔记 R0.72G：在精确实单载波三角形 Navier–Stokes 族上，用 Rolle–BV 论证把完整根斜率质量压到负 Sobolev action，并证明 critical-log payment 的完整根尖锐饱和。">
  <meta property="og:type" content="article">
  <meta property="og:title" content="R0.72G｜精确单载波上的完整根打包">
  <meta property="og:description" content="根数与根间距不进入常数；完整根质量恰为对数量级。结论只覆盖声明的精确实单载波族。">
  <meta property="og:image" content="https://kasifa.github.io/figures/r0-72g-complete-root-packing.png">
  <title>R0.72G｜精确单载波上的完整根打包</title>
  <script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.90">
  <style>.hero h1{font-size:clamp(1.62rem,3.5vw,2.9rem)}pre{max-width:100%;overflow-x:auto}.audit-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem}.audit-card{border:1px solid var(--line);padding:1rem}.audit-card strong{display:block;color:var(--gold);font-family:var(--mono);margin-bottom:.45rem}.compact-table{width:100%;border-collapse:collapse}.compact-table th,.compact-table td{border:1px solid var(--line);padding:.55rem;text-align:left;vertical-align:top}@media(max-width:760px){.audit-grid{grid-template-columns:1fr}.compact-table{font-size:.82rem}}@media print{body{font-size:8.7pt}.topline{height:3px}pre{max-width:none;overflow:visible!important;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-size:7.3pt}}</style>
  <script defer src="/i18n-en.js?v=1.20"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#lattice">格点</a><a href="#rolle">证明</a><a href="#sharp">尖锐性</a><a href="#physical">物理账本</a><a href="#audit">证书</a><a href="#figure">附图</a><a href="#literature">文献</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72G · COMPLETE ROOTS · ROLLE–BV · CRITICAL LOG</div>
        <h1>把预选根撤掉之后，<br>完整账本仍只有一个对数</h1>
        <p class="lead">R0.72F 留下的疑问是：selected Bessel neighborhoods 之外的根，会不会藏着更大的斜率质量。我在精确实单载波格点上不再计数根，也不假设根分离；实相位 gauge、目标行恒等式与 Rolle–BV 归约直接把全部根压到完整 \(H^{-1}\) action。结果是 \(G_{\rm all}\asymp\log\delta\)，critical-log payment 在这条精确族上成立而且尖锐。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72G 完成</span><strong>exact one-carrier gate closed</strong><p>版本 v0.72G · 2026-08-27</p><p>complete-root estimate: CLOSED</p><p>critical-log saturation: SHARP</p><p>general triangular transfer: OPEN</p><p>一般三维正则性：OPEN</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节判断</a></li><li><a href="#lattice">01 · 精确格点</a></li><li><a href="#rolle">02 · Rolle–BV</a></li><li><a href="#sharp">03 · 尖锐对数</a></li><li><a href="#physical">04 · 物理账本</a></li><li><a href="#audit">05 · 双路证书</a></li><li><a href="#figure">06 · 正式附图</a></li><li><a href="#literature">07 · 文献边界</a></li><li><a href="#value">08 · 研究价值</a></li><li><a href="#next">09 · 下一步</a></li><li><a href="#claims">10 · 主张边界</a></li><li><a href="#reproduce">11 · 复现</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Direct verdict</div><h2>完整根斜率质量由同一个负 Sobolev action 支付</h2>
          <p>固定整数 \(q_0\) 大于目标 multiplier 的支撑半径，令 \(\mu=q_0^{-2}\)，并只考虑 \(\delta\ge1\)。对精确单载波格点</p>
          <div class="equation result">\[
            F_x=-A_\mu F+\delta V(x)F,\qquad
            (A_\mu F)_r=(r^2+\mu)F_r,\qquad
            (VF)_r=-ie^{-x}(F_{r-1}+F_{r+1}),\quad F(0)=ie_{-1},
          \]</div>
          <p>写 \(f=F_0\)、\(h=P_0VF\)、\(q=\lVert VF\rVert_{A_\mu^{-1}}^2\)。在半开窗 \([0,X)\) 上，把根和定义成任意有限根子集之和的单调上确界：</p>
          <div class="equation result">\[
            G_{\rm all}(\delta;X)=\sum_{\substack{x\in[0,X)\\f(x)=0}}|h(x)|^2.
          \]</div>
          <div class="equation result">\[
            \boxed{G_{\rm all}(\delta;X)
            \le 1+2\!\left[(2+\mu)\mu+\delta\sqrt{2\mu(1+\mu)}\right]
            \int_0^Xq(x)\,dx.}
          \]</div>
          <p>R0.72E 已给 \(\int_0^Xq\lesssim(1+\log(2+\delta))/\delta\)，所以 \(G_{\rm all}\lesssim1+\log(2+\delta)\)。常数不依赖根数或根间距。</p>
        </section>

        <section id="lattice"><div class="section-no">01 / Real phase and target rows</div><h2>相位 gauge 把目标坐标变成实函数</h2>
          <p>置 \(F_r=i^{-r}a_r\)，则 \(a_{-1}(0)=1\)，其余初值为零，且</p>
          <div class="equation result">\[
            a_r'=-(r^2+\mu)a_r+\delta e^{-x}(a_{r-1}-a_{r+1}).
          \]</div>
          <p>系数和初值都为实数，因此 \(f=a_0\) 与 \(h=e^{-x}(a_{-1}-a_1)\) 为实函数。目标行给出两个精确恒等式：</p>
          <div class="equation result">\[
            \boxed{f'+\mu f=\delta h,\qquad
            h'=-(2+\mu)h+\delta b,\quad b=P_0V^2F.}
          \]</div>
          <p>若 \(q=\lVert VF\rVert_{A_\mu^{-1}}^2\)，则 Cauchy–Schwarz 直接给</p>
          <div class="equation result">\[
            |h|^2\le\mu q,\qquad |b|^2\le2(1+\mu)q.
          \]</div>
          <p>launch root 单独贡献 \(h(0)^2=1\)。这一步也解释了为何结论不能直接搬到任意复相位目标坐标。</p>
        </section>

        <section id="rolle"><div class="section-no">02 / Root-count-free packing</div><h2>相邻目标根之间必有一个 \(h\) 的零点</h2>
          <p>令 \(\psi=e^{\mu x}f\)，则 \(\psi'=\delta e^{\mu x}h\)。对任意有限的正根子集 \(0&lt;x_1&lt;\cdots&lt;x_N&lt;X\)，Rolle 定理在每两个相邻目标根之间给出一个 \(h\) 的零点。于是 \(h^2\) 的总变差支付所有采样值：</p>
          <div class="equation result">\[
            \sum_{j=1}^N|h(x_j)|^2
            \le 2\int_0^X|h(x)h'(x)|\,dx.
          \]</div>
          <p>多重根满足 \(h=0\)，无需另加重数。代入目标行恒等式，再用上面的 \(q\)-界与 Cauchy–Schwarz，就得到主上界。最后对所有有限根子集取上确界，因此证明没有暗中使用根集有限、根间距正下界或解析零点计数。</p>
          <p>\(\delta=0\) 被明确排除：此时 \(f\equiv0\) 而 \(h\not\equiv0\)，按同一定义完整根质量发散。这正是定理保留 \(\delta\ge1\) 的原因。</p>
        </section>

        <section id="sharp"><div class="section-no">03 / Sharp Bessel subsequence</div><h2>selected roots 已经把对数上界取到</h2>
          <p>沿 R0.72E 的 \(\delta_R=R^4\)，标准 Bessel 零点与导数渐近给</p>
          <div class="equation result">\[
            G_R^{\rm sel}=\frac8{\pi^2}\log R+O_{q_0}(1)
            =\frac2{\pi^2}\log\delta_R+O_{q_0}(1).
          \]</div>
          <p>selected roots 是 complete roots 的子集，与刚证明的上界合并后，</p>
          <div class="equation result">\[
            \boxed{G_{\rm all}(\delta_R;X)\asymp_{X,q_0}\log\delta_R.}
          \]</div>
          <p>因此额外根可以改变有界常数，却不能在这条精确族中制造隐藏的超对数斜率质量。</p>
        </section>

        <section id="physical"><div class="section-no">04 / Physical ledger</div><h2>critical-log payment 在完整根集上成立并饱和</h2>
          <p>回到全局光滑的实三角形解 \(u=(f_{\rm phys}(y,z,t),0,v(y,t))\)。保持 shear amplitude \(P=q_0^2\delta\)，并令 active squared amplitude \(A_\delta=S_\delta^2\le C_A\delta\)。根账本使用 \([0,T)\)，连续积分使用 \([0,T]\)，从而不让终端根在两边产生不同约定。对所有充分大的 \(\delta\)，</p>
          <div class="equation result">\[
            \boxed{\mathcal J_{\rm all}([0,T))
            \le C_{T,q_0,C_A}D^{1/3}\Lambda_{1,*}([0,T];u),}
          \]</div>
          <p>其中 \(\Lambda_{1,*}=\mathcal R_Y[1+\mathscr A_*]\)，\(\mathscr A_*\) 使用 R0.72F 的 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)。对原始幅度 \(A_R=\delta_R/\log(2+\delta_R)\)，</p>
          <div class="equation result">\[
            \mathcal J_{{\rm all},R}\asymp\delta_R,\qquad
            D_R^{1/3}\Lambda_{1,*}\asymp\delta_R,\qquad
            \frac{\mathcal J_{{\rm all},R}}{D_R^{1/3}\Lambda_{1,*}}\asymp1.
          \]</div>
          <p>这把 R0.72F 的 selected-root saturation 提升为同一测试序列上的 complete-root saturation。它仍不是一般三维解的 continuation criterion。</p>
        </section>

        <section id="audit"><div class="section-no">05 / Independent certificates</div><h2>实格点 RK4 与复 Fourier Strang 得到同一根账本</h2>
          <div class="audit-grid">
            <div class="audit-card"><strong>PRODUCER · ALL CHECKS PASS</strong><p>实不变格点、fixed-step RK4、cubic Hermite + Brent 求根；\(R=8,12,16,24,32,48,64\)。根数从 443 增至 31,242，complete mass 从 3.629980008 增至 7.091268660。</p></div>
            <div class="audit-card"><strong>INDEPENDENT · ALL CHECKS PASS</strong><p>复 Fourier Strang split，热半步与时间势积分均精确；独立覆盖 \(R=8,12,16,24,32\)。共同根数逐点完全一致，最大 complete-mass 差为 \(9.18\times10^{-7}\)。</p></div>
          </div>
          <p>producer 的有限 \(\log\delta\) 斜率是 \(0.40754165\)，对照渐近 \(4/\pi^2=0.40528473\)。最大步长压力 \(7.40\times10^{-7}\)，最大半径压力 \(4.39\times10^{-8}\)，horizon tail 为 \(1.67\times10^{-8}\)。这些结果只审计实现和有限渐近，不替代解析证明，也不是区间证书。两次失败的初始压力测试连同修正原因都保留在证书目录中。</p>
        </section>

        <section id="figure"><div class="section-no">06 / Journal figure</div><h2>正式附图分开显示完整质量、独立一致性与 dyadic packets</h2>
          <figure><img src="/figures/r0-72g-complete-root-packing.svg" alt="R0.72G complete-root logarithmic packing, finite resolved root count, and dyadic root-mass packets"><figcaption>图 R0.72G-1。左：两路 complete mass、selected mass 与对数 guide；中：有限窗内 resolved root count；右：\(R=64\) 的 dyadic root-mass packets。有限点只用于实现审计，解析结论来自 Rolle–BV 证明。</figcaption></figure>
        </section>

        <section id="literature"><div class="section-no">07 / Literature boundary</div><h2>时间解析性、空间零数与固定采样都不是这条估计</h2>
          <p>DLMF 的 Jacobi–Anger 展开、Bessel zeros 与导数渐近支持 selected logarithmic lower mass；Kusuoka–Stroock 的定量密度估计是继承自 R0.72E 的 action 上界输入。Poláčik–Šverák 说明复杂量热流的固定点时间迹可以在无界半线上出现趋向无穷的零点序列，但不否定正距离紧区间上的有限根数。</p>
          <p>Dong–Zhang、Giga 等的时间解析性只给正时间根的隔离，不给 launch-uniform 根数、根分离或平方斜率和。Angenent、Matano 控制一维实抛物方程的空间零数；de Branges、Paley–Wiener 与 Cartwright 理论则处理满足结构条件的固定采样或整函数零点。它们都不能替代这里随解移动的 temporal self-zero sampling。</p>
          <p>截至 2026-08-27 的限定一手来源检索中，我没有找到直接给出本节 complete temporal root-slope estimate 的定理。这是 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p>
        </section>

        <section id="value"><div class="section-no">08 / Research value</div><h2>这一节关闭了候选在原始反例族上的最后一个漏洞</h2>
          <p>R0.72E 只需要 selected roots 就足以排除无权 payment；R0.72F 用同一 selected family 选出 critical-log repair。R0.72G 进一步证明，遗漏的根不会让这条 exact family 重新击穿修正。于是这条测试序列现在同时给出 complete-root 上界和匹配下界。</p>
          <p>价值是把下一障碍从“也许还有更多根”推进到“多载波混合行能否维数无关地支付”。这是一项精确模型类内部的 trace-packing 定理，不是千禧年问题的部分解答；节点数也不能换算成问题完成比例。</p>
        </section>

        <section id="next"><div class="section-no">09 / Next finite gate</div><h2>R0.72H 转向有限实多载波的混合行</h2>
          <p>下一步保留实相位、固定目标和有限载波，不先跨到一般三维系统。目标是处理 finite real multi-carrier 的 mixed row term：</p>
          <div class="equation result">\[
            \mathcal E_Q=\int|h\,QF|,\qquad
            Q=P_0\bigl[V'+V(D+\lambda_0)\bigr].
          \]</div>
          <p>有限关口只有两个可接受结果：证明它可由 critical-log action 以载波数无关常数支付，或构造一个随载波数增长的显式反族。两者都必须保留 complete roots、launch atom 与 full-frequency charge。</p>
        </section>

        <section id="claims"><div class="section-no">10 / Claim boundary</div><h2>证明域被固定在精确实单载波 ray</h2>
          <table class="compact-table"><thead><tr><th>已证明</th><th>仍开放</th></tr></thead><tbody><tr><td>目标相位实化；两个精确目标行恒等式；不依赖根数的 Rolle–BV packing；完整质量 \(\asymp\log\delta\)；声明物理幅度族上的 critical-log complete-root payment 与尖锐饱和。</td><td>有限或无限多载波的维数无关常数；一般 triangular launch data；任意复目标；restart/dyadic 覆盖到一般弱解；三维 Navier–Stokes continuation 或 singularity theorem。</td></tr></tbody></table>
          <p>所有构造解仍是全局光滑的三角形 2.5D 解。本页既没有构造有限时奇性，也没有证明一般三维解全局光滑；Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="reproduce"><div class="section-no">11 / Reproduce</div><h2>报告、证明审计、双路证书与正式附图全部保留</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_literature_audit.md">一手文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_independent_audit.md">独立逐式审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072g">双路数值证书与失败尝试</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072g-complete-root-packing/fig-r072g-complete-root-packing">正式附图、数据、代码、环境与校验和</a> · <a href="/figures/r0-72g-complete-root-packing.pdf">期刊附图 PDF</a> · <a href="/notes/r0-72g.pdf">同步研究笔记 PDF</a></p>
          <p><a href="/recap-r0-61-r0-72g.html">阅读 R0.60 之后的完整累计回顾</a> · <a href="/recap-r0-61-r0-72g.pdf">下载累计回顾 PDF</a> · <a href="/notes/r0-72f.html">返回 R0.72F</a></p>
        </section>
      </article>
    </div>
  </main>
  <footer><div>R0.72G · 2026-08-27 · 个人数学研究日志<br><a href="/">返回研究主页</a> · <a href="/literature-review.html">文献综述</a> · <a href="/recap-r0-61-r0-72g.html">累计回顾</a></div></footer>
</body>
</html>
'''


RECAP_PHASE_FG = r'''            <article class="phase"><h3>R0.72F–R0.72G · 临界对数候选与完整根封闭</h3>
              <p>R0.72F 对 \(w_{\beta,\gamma}(s)=s^{-\beta}[1+\log(1/s)]^\gamma\) 分别计算 Leray payment 与 selected Bessel obstruction：能量支付要求 \(\beta&lt;1/2\)，exact family 强制 \(\beta&gt;1/3\)，或在端点取 \(\gamma\ge1\)。最小共同边界是 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)。</p>
              <p>R0.72G 固定这个候选，不再预选根。在精确实单载波格点上，phase gauge、目标行恒等式与 Rolle–BV 归约给出不依赖根数和根间距的 \(G_{\rm all}\lesssim\log\delta\)；selected Bessel roots 给匹配下界。原始幅度序列上，完整物理 root ledger 与 \(D^{1/3}\Lambda_{1,*}\) 同阶。下一障碍转到有限实多载波的 mixed row；一般三维传递仍开放。</p>
              <div class="links"><a href="/notes/r0-72f.html">R0.72F</a><a href="/notes/r0-72g.html">R0.72G</a><a href="/figures/r0-72g-complete-root-packing.pdf">R0.72G 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072g">R0.72G 证书</a></div></article>
'''


def build_recap() -> str:
    html = (PUBLIC / "recap-r0-61-r0-72f.html").read_text(encoding="utf-8")
    repeated_title = 'R0.61–R0.72F｜R0.60 之后的研究回顾'
    if html.count(repeated_title) != 2:
        raise RuntimeError("recap repeated title anchor must occur twice")
    html = html.replace(repeated_title, 'R0.61–R0.72G｜R0.60 之后的研究回顾')
    repeated_scope = 'R0.61 到 R0.72F 的 96 个研究节点'
    if html.count(repeated_scope) != 2:
        raise RuntimeError("recap repeated scope anchor must occur twice")
    html = html.replace(repeated_scope, 'R0.61 到 R0.72G 的 97 个研究节点')
    pairs = [
        ('R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72G 的 97 个研究节点；最新一节用单载波 Bessel 根族与完整 H^{-1} action 严格排除候选 D^{1/3}Λ₁ 支付。', 'R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72G 的 97 个研究节点；最新一节在精确实单载波族上封闭完整根打包并证明 critical-log 尖锐饱和。'),
        ('二十三个阶段、96 个节点：从约化递推和 complete-root 账本，到 full-charge saturation，再到候选 D^{1/3}Λ₁ payment 的严格失效。', '二十三个阶段、97 个节点：从约化递推和时间迹账本，到 unweighted payment 失效，再到 critical-log complete-root 尖锐封闭。'),
        ('/i18n-en.js?v=1.19', '/i18n-en.js?v=1.20'),
        ('累计回顾 · R0.61–R0.72F', '累计回顾 · R0.61–R0.72G'),
        ('<strong>R0.61–R0.72F</strong>', '<strong>R0.61–R0.72G</strong>'),
        ('收录节点：96', '收录节点：97'),
        ('回顾截止时公开笔记：156', '回顾截止时公开笔记：157'),
        ('回顾截止节点：R0.72F', '回顾截止节点：R0.72G'),
        ('02 · 96 节完整索引', '02 · 97 节完整索引'),
        ('<strong>96</strong><span>R0.61–R0.72F 研究节点</span>', '<strong>97</strong><span>R0.61–R0.72G 研究节点</span>'),
        ('<strong>58</strong><span>R0.70A–R0.72F 已公开版本</span>', '<strong>59</strong><span>R0.70A–R0.72G 已公开版本</span>'),
        ('<strong>34</strong><span>当前 formal-figure 合同下完整封存</span>', '<strong>35</strong><span>当前 formal-figure 合同下完整封存</span>'),
        ('后面的 96 个节点', '后面的 97 个节点'),
        ('R0.70A–R0.72F 的 58 个版本已经公开；其中 34 个满足当前 formal-figure 完整封存合同', 'R0.70A–R0.72G 的 59 个版本已经公开；其中 35 个满足当前 formal-figure 完整封存合同'),
        ('R0.61–R0.72F 的 96 节公开笔记', 'R0.61–R0.72G 的 97 节公开笔记'),
        ('R0.61–R0.72F 回顾', 'R0.61–R0.72G 回顾'),
    ]
    for old, new in pairs:
        html = replace_once(html, old, new, f"recap {old[:34]}")
    html = html.replace('/recap-r0-61-r0-72f.html', '/recap-r0-61-r0-72g.html')
    html = html.replace('/recap-r0-61-r0-72f.pdf', '/recap-r0-61-r0-72g.pdf')
    malformed_metrics = '''            <div class="metric"><strong>97</strong><span>R0.61–R0.72G 研究节点</span></div>
            <div class="metric"><strong>59</strong><span>R0.70A–R0.72G 已公开版本</span>
            <div class="metric"><strong>35</strong><span>当前 formal-figure 合同下完整封存</span></div>
            <div class="metric"><strong>24</strong><span>旧版 formal-figure 档案待回补</span></div></div>
            <div class="metric"><strong>23</strong><span>按问题划分的研究阶段</span></div>
            <div class="metric"><strong>0</strong><span>全局正则性证明或破裂构造</span></div>'''
    corrected_metrics = '''            <div class="metric"><strong>97</strong><span>R0.61–R0.72G 研究节点</span></div>
            <div class="metric"><strong>59</strong><span>R0.70A–R0.72G 已公开版本</span></div>
            <div class="metric"><strong>35</strong><span>当前 formal-figure 合同下完整封存</span></div>
            <div class="metric"><strong>24</strong><span>旧版 formal-figure 档案待回补</span></div>
            <div class="metric"><strong>23</strong><span>按问题划分的研究阶段</span></div>
            <div class="metric"><strong>0</strong><span>全局正则性证明或破裂构造</span></div>'''
    html = replace_once(html, malformed_metrics, corrected_metrics, "recap metric grid")
    html = replace_once(
        html,
        "@media print{\n      .timeline{display:block;overflow:visible}",
        "@media print{\n      body{font-size:8.6pt;line-height:1.52}\n      .timeline{display:block;overflow:visible}",
        "recap compact print typography",
    )

    phase_start = '            <article class="phase"><h3>R0.72F · 临界对数初始层修正与统一 selected-family frontier</h3>'
    phase_left = html.find(phase_start)
    if phase_left < 0:
        raise RuntimeError("recap R0.72F phase missing")
    phase_right = html.find('</article>', phase_left)
    if phase_right < 0:
        raise RuntimeError("recap R0.72F phase end missing")
    phase_right += len('</article>')
    html = html[:phase_left] + RECAP_PHASE_FG.rstrip() + html[phase_right:]

    node_f = '            <span class="node-ref"><a href="/notes/r0-72f.html">R0.72F</a><span class="node-state kind-closed">闭</span></span>\n'
    node_g = '            <span class="node-ref"><a href="/notes/r0-72g.html">R0.72G</a><span class="node-state kind-closed">闭</span></span>\n'
    html = replace_once(html, node_f, node_f + node_g, "recap node G")

    retained_f = r'''            <li>R0.72F 的 critical-log repair screen：\(\mathscr A_{\beta,\gamma}\) 在 \(\beta&lt;1/2\) 时由 Leray 能量支付；R0.72E exact family 则强制 \(\beta&gt;1/3\)，或在端点取 \(\gamma\ge1\)。最小边界权重 \(w_*=s^{-1/3}[1+\log(1/s)]\) 恰好饱和 selected obstruction，free-amplitude audit 进一步给出增广必要 frontier。完整根上界、restart covering 与一般三维传递仍开放。</li>'''
    retained_g = r'''
            <li>R0.72G 的 exact one-carrier complete-root theorem：实相位 gauge、两个目标行恒等式与 Rolle–BV 归约给出根数无关的 \(G_{\rm all}\lesssim\log\delta\)；selected Bessel roots 给匹配下界。原始幅度序列上 \(\mathcal J_{\rm all}\asymp D^{1/3}\Lambda_{1,*}\asymp\delta\)，所以 critical-log payment 对完整根集尖锐。结论只覆盖固定 \(q_0\)、实单载波、\(\delta\ge1\) 与 \(A_\delta=O(\delta)\)；多载波和一般三维传递仍开放。</li>'''
    html = replace_once(html, retained_f, retained_f + retained_g, "recap retained G")

    value_next = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>单载波上的完整根缺口已经封闭，主障碍转到混合行</h2>
          <p>截至 R0.72G，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 97 个节点或 59 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72E 排除 unweighted candidate；R0.72F 选出 critical-log 最小修正；R0.72G 又证明，在制造原反例的 exact one-carrier ray 上，遗漏的根不会击穿这一修正。这里的完整根质量恰是对数量级，原始幅度序列使两边同阶。</p>
          <p>这是一项精确模型类内部的 sharp trace-packing theorem，不是 regularity theorem。它把下一关从未知根数压缩为有限多载波中一个明确的 mixed-row payment。</p>
        </section>

        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72H 检查有限实多载波 mixed row</h2>
          <p>下一有限任务保留 real phase、fixed target 与 full-frequency charge，处理 \(\mathcal E_Q=\int|hQF|\)，其中 \(Q=P_0[V'+V(D+\lambda_0)]\)。目标是证明载波数无关的 critical-log payment，或构造一个显式 growing-carrier 反族。</p>
          <p>这一步不会先假定一般三维 Hilbert trace theorem，也不会换掉 critical-log candidate。只有多载波关口完成后，才有理由讨论 restart covering 与一般三维传递。</p>
        </section>

'''
    html = replace_between(html, '        <section id="value">', '        <section id="claims">', value_next, "recap value-next G")
    claims = r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72G 的 59 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，35 节完整封存；24 节较早版本仍缺 formal 状态或正式附图包，列入可审计的旧档回补清单。公开页存在不等于档案合同完整。</p>
          <p>R0.72G 的定理限于精确实单载波三角形 2.5D 光滑解族。本回顾没有证明三维 Navier–Stokes 的全局光滑性或有限时破裂；Clay 正式问题仍然开放。</p>
        </section>

'''
    html = replace_between(html, '        <section id="claims">', '        <section id="reproduce">', claims, "recap claims G")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72f.html">保留 R0.72F 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72g.html">打开最新节点 R0.72G</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072g">查看 R0.72G 双路证书</a> · <a href="/recap-r0-61-r0-72g.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72f.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>
'''
    html = replace_between(html, '        <section id="reproduce">', '      </article>', reproduce, "recap reproduce G")
    return html


def update_home(html: str) -> str:
    if 'data-site-version="1.20"' in html:
        return html
    if 'data-site-version="1.19"' not in html:
        raise RuntimeError("home is not site v1.19")
    html = html.replace('/recap-r0-61-r0-72f', '/recap-r0-61-r0-72g')
    pairs = [
        ('data-site-version="1.19"', 'data-site-version="1.20"'),
        ('/i18n-en.js?v=1.19', '/i18n-en.js?v=1.20'),
        ('/site-refresh.js?v=1.19', '/site-refresh.js?v=1.20'),
        ('<strong>v1.19</strong>网页版本', '<strong>v1.20</strong>网页版本'),
        ('<strong>156</strong>公开研究笔记', '<strong>157</strong>公开研究笔记'),
        ('<strong>R0.72F</strong>最新研究节点', '<strong>R0.72G</strong>最新研究节点'),
        ('<strong>complete-root trace packing for the critical-log repair</strong>当前方向', '<strong>finite real multi-carrier mixed-row payment</strong>当前方向'),
        ('Research topology · R0.1–R0.72F', 'Research topology · R0.1–R0.72G'),
        ('R0.70A–R0.72F：58 节已公开，34 节完整封存', 'R0.70A–R0.72G：59 节已公开，35 节完整封存'),
        ('<span class="route-range">R0.69P–R0.72F</span>', '<span class="route-range">R0.69P–R0.72G</span>'),
        ('<summary>展开 66 篇公开笔记</summary>', '<summary>展开 67 篇公开笔记</summary>'),
        ('aria-label="R0.69P–R0.72F"', 'aria-label="R0.69P–R0.72G"'),
        ('本站 R0.69P–R0.72F 路线', '本站 R0.69P–R0.72G 路线'),
        ('综述 v1.19 · 2026-08-27', '综述 v1.20 · 2026-08-27'),
        ('上次综述 v1.18 · 2026-08-27', '上次综述 v1.19 · 2026-08-27'),
    ]
    for old, new in pairs:
        html = replace_once(html, old, new, f"home {old[:36]}")
    html = replace_once(
        html,
        'R0.72F 已把修正压缩到 critical-log initial-layer action；下一步固定这个候选，检查它能否支付 complete-root trace packing。',
        'R0.72G 已在精确实单载波族上封闭 complete-root trace packing，并证明 critical-log payment 尖锐；下一步只审有限实多载波的新 mixed row。',
        "home current summary G",
    )
    html = replace_once(
        html,
        '从 complete-root 局部暴露走到候选 payment 的严格失效',
        '从候选 payment 失效走到 critical-log complete-root 尖锐封闭',
        "home route heading G",
    )
    html = replace_once(
        html,
        r'R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。</p>',
        r'R0.72F 随后证明 selected roots 强制 \(1/3\) 下端点，而 Leray energy 只支付到 \(1/2\)；最小边界修正是 \(s^{-1/3}[1+\log(1/s)]\)。R0.72G 固定这一候选，用实相位 gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量 \(G_{\rm all}\asymp\log\delta\)，并在原始幅度序列上得到 complete-root sharp saturation。</p>',
        "home route paragraph G",
    )
    html = replace_once(
        html,
        'candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier</p>',
        'candidate D^{1/3}Λ₁ payment failure → critical-log repair → selected-family frontier → complete-root Rolle–BV closure → sharp critical-log saturation</p>',
        "home route path G",
    )
    nav_f = '                  <a class="milestone" href="/notes/r0-72f.html">R0.72F</a>\n'
    html = replace_once(html, nav_f, nav_f + '                  <a class="milestone" href="/notes/r0-72g.html">R0.72G</a>\n', "home nav G")

    next_old = r'''          <div class="tree-row">
            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72G</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>complete-root trace packing for the critical-log repair</h3>
              <p>固定 \(w_*(s)=s^{-1/3}[1+\log(1/s)]\)，把全部根、restart covering 与 left-end cost 放进同一个 estimate；不再移动候选。</p>
            </article>
          </div>'''
    next_new = r'''          <div class="tree-row">
            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72H</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>dimension-free mixed-row payment in finite real multi-carrier systems</h3>
              <p>保留 real phase、fixed target 与 full-frequency charge，证明 \(\mathcal E_Q=\int|hQF|\) 可由 critical-log action 以载波数无关常数支付，或给出显式 growing-carrier 反族。</p>
            </article>
          </div>'''
    html = replace_once(html, next_old, next_new, "home next H")

    recap_new = r'''            <p class="eyebrow">累计回顾 R0.61–R0.72G · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 97 个节点；全站现有 157 篇公开研究笔记</h3>
            <p>累计回顾保持二十三个问题阶段，完整覆盖 R0.61–R0.72G。R0.72E 排除 unweighted payment，R0.72F 选出 critical-log 最小修正，R0.72G 在 exact real one-carrier ray 上封闭 complete roots 并证明尖锐饱和。R0.70A–R0.72G 共 59 个版本已公开；按当前 formal-figure 合同有 35 个完整封存，24 个旧版附图档案列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。下一障碍是有限实多载波 mixed row 的维数无关支付，不是重复单载波根扫描。</p>'''
    html = replace_between(
        html,
        '            <p class="eyebrow">累计回顾 R0.61–R0.72F',
        '            <p><a href="/recap-r0-61-r0-72g.html"',
        recap_new + "\n",
        "home recap card G",
    )

    release_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72G：</strong>&nbsp;固定 \(w_*\)，检查 complete-root trace packing、restart covering 与 left-end cost。</p>
          </div>'''
    release_g = r'''            <p><strong style="color:var(--gold)">R0.72G 已完成：</strong>&nbsp;exact real one-carrier ray 上的全部根由 Rolle–BV 与完整 action 支付；critical-log payment 对 complete roots 尖锐。</p>
          </div>

          <div class="task-one" id="r072g" data-release="r072g" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72G · 2026-08-27</p>
            <h3>精确实单载波上的完整根斜率质量恰为对数量级</h3>
            <p>写 \(f=F_0\)、\(h=P_0VF\)、\(q=\lVert VF\rVert_{A_\mu^{-1}}^2\)。实相位 gauge 给 \(f,h\in\mathbb R\)，目标行恒等式与 Rolle–BV 归约给</p>
            <p>\[
              G_{\rm all}(\delta;X)\le1+2\bigl[(2+\mu)\mu+\delta\sqrt{2\mu(1+\mu)}\bigr]\int_0^Xq(x)\,dx
              \lesssim1+\log(2+\delta).
            \]</p>
            <p>selected Bessel roots 给匹配下界，所以 \(G_{\rm all}(\delta_R;X)\asymp\log\delta_R\)。原始幅度序列上，\(\mathcal J_{\rm all}\asymp D^{1/3}\Lambda_{1,*}\asymp\delta_R\)：critical-log repair 对完整根集成立并尖锐。</p>
            <p><strong>结论边界：</strong>&nbsp;定理只覆盖固定 \(q_0\)、\(\delta\ge1\)、实单载波与 \(A_\delta=O(\delta)\) 的 exact triangular 2.5D 光滑解族；不是一般三维 continuation theorem，也没有解决千禧年问题。</p>
            <p><a href="/notes/r0-72g.html"><strong>阅读 R0.72G 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72g.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72g-complete-root-packing.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072g">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072g_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072g-complete-root-packing/fig-r072g-complete-root-packing">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72g.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72g.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72H：</strong>&nbsp;处理有限实多载波的新 mixed row \(\mathcal E_Q=\int|hQF|\)，要求 dimension-free payment 或显式 growing-carrier 反族。</p>
          </div>'''
    html = replace_once(html, release_tail, release_g, "home release G")
    return html


def update_literature(html: str) -> str:
    if '/i18n-en.js?v=1.20' in html:
        return html
    if '/i18n-en.js?v=1.19' not in html:
        raise RuntimeError("literature is not site v1.19")
    html = html.replace('/recap-r0-61-r0-72f', '/recap-r0-61-r0-72g')
    pairs = [
        ('/i18n-en.js?v=1.19', '/i18n-en.js?v=1.20'),
        ('本站 R0.69P–R0.72F 只列为研究笔记', '本站 R0.69P–R0.72G 只列为研究笔记'),
        ('累计回顾与 96 节索引', '累计回顾与 97 节索引'),
        ('打开 96 节完整索引', '打开 97 节完整索引'),
        ('文献综述 v1.19 · 2026-08-27', '文献综述 v1.20 · 2026-08-27'),
    ]
    for old, new in pairs:
        html = replace_once(html, old, new, f"literature {old[:36]}")
    html = replace_once(
        html,
        r'R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。一般 Navier–Stokes 正则性仍开放。</p>',
        r'R0.72F 再用 regularly varying initial-layer weights 分离 selected-root 的 \(1/3\) 阈值与 Leray payment 的 \(1/2\) 阈值，并选出 critical-log 最小边界。R0.72G 在 exact real one-carrier lattice 上用 phase gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量恰为对数量级，并得到 critical-log complete-root sharp saturation。一般 Navier–Stokes 正则性仍开放。</p>',
        "literature deck G",
    )
    old_route = r'''              <div class="route-step closed"><header><b>R0.72F</b><strong>critical-log initial-layer repair 与可行窗口</strong></header><p>selected Bessel roots 强制 \(\beta\ge1/3\)，纯幂端点还需 \(\gamma\ge1\)；Leray energy 只支付 \(\beta&lt;1/2\)。最小边界权重是 \(s^{-1/3}[1+\log(1/s)]\)。这只通过两项筛查，不是 complete-root theorem。<a href="/notes/r0-72f.html">研究笔记</a> <a href="/recap-r0-61-r0-72g.html">当前累计回顾</a> <a href="#r072f-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72G</b><strong>complete-root trace packing</strong></header><p>固定 critical-log weight，检查全部 roots、restart covering 与 left-end cost；不再更换候选。</p></div>'''
    new_route = r'''              <div class="route-step closed"><header><b>R0.72F</b><strong>critical-log initial-layer repair 与可行窗口</strong></header><p>selected Bessel roots 强制 \(\beta\ge1/3\)，纯幂端点还需 \(\gamma\ge1\)；Leray energy 只支付 \(\beta&lt;1/2\)。最小边界权重是 \(s^{-1/3}[1+\log(1/s)]\)。这只通过两项筛查，不是 complete-root theorem。<a href="/notes/r0-72f.html">研究笔记</a> <a href="/recap-r0-61-r0-72g.html">当前累计回顾</a> <a href="#r072f-boundary">方法边界</a></p></div>
              <div class="route-step closed"><header><b>R0.72G</b><strong>exact one-carrier complete-root packing 与尖锐饱和</strong></header><p>实相位 gauge、目标行恒等式与 Rolle–BV 归约给 \(G_{\rm all}\lesssim\log\delta\)，selected Bessel roots 给匹配下界；原始幅度序列上 critical-log payment 对 complete roots 同阶。结论限于精确实单载波 ray。<a href="/notes/r0-72g.html">研究笔记</a> <a href="/recap-r0-61-r0-72g.html">当前累计回顾</a> <a href="#r072g-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72H</b><strong>finite real multi-carrier mixed-row payment</strong></header><p>处理 \(\mathcal E_Q=\int|hQF|\)，要求载波数无关的 critical-log payment，或构造显式 growing-carrier 反族。</p></div>'''
    html = replace_once(html, old_route, new_route, "literature route G/H")
    boundary_g = r'''
          <h3 id="r072g-boundary">R0.72G 的 temporal self-zero sampling 边界</h3>
          <p><a href="#ref-70">DLMF</a> 的 Jacobi–Anger 展开、Bessel zeros 与导数渐近支持 selected logarithmic lower mass；<a href="#ref-86">Kusuoka–Stroock</a> 的定量 density input 支持继承自 R0.72E 的 negative-Sobolev action 上界。<a href="#ref-90">Poláčik–Šverák</a> 给出复杂量热流固定点时间迹在无界半线上出现 \(\tau_k\to\infty\) 零点序列的例子，但不否定紧正时间区间上的有限根数，也不估计根斜率平方和。</p>
          <p><a href="#ref-91">Dong–Zhang</a>、<a href="#ref-69">Giga 等</a>与<a href="#ref-68">Masuda</a>的时间解析性或唯一延拓结果不能推出 launch-uniform root count、root separation 或 slope mass。<a href="#ref-85">Angenent</a>与<a href="#ref-92">Matano</a>控制一维实抛物方程的空间零数；<a href="#ref-93">de Branges</a>、<a href="#ref-94">Ortega-Cerdà–Seip</a>和<a href="#ref-95">Levin</a>处理结构受控的固定采样或整函数零点，也不直接适用于随解移动的 temporal self-zero nodes。</p>
          <div class="boundary"><strong>R0.72G 的主源边界</strong><p>本节真正使用的是 exact one-carrier lattice 的实相位 gauge、两个目标行恒等式与 Rolle–BV 归约；它们把根采样转成连续 negative-Sobolev action，不依赖解析零点计数。限定一手来源检索没有找到直接给出这条 complete temporal root-slope estimate 的定理；该判断是截至 2026-08-27 的 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p></div>
'''
    html = replace_once(html, '          <ol class="criteria">', boundary_g + '          <ol class="criteria">', "literature boundary G")
    ref_89 = '            <li id="ref-89">Y. Yang. <a href="https://arxiv.org/abs/2308.09350"><em>Trace theorems for Sobolev spaces on submanifolds</em></a>. Preprint and J. Differential Equations version.</li>'
    refs_g = r'''
            <li id="ref-90">P. Poláčik and V. Šverák. <a href="https://doi.org/10.1515/CRELLE.2008.022"><em>Zeros of complex caloric functions and singularities of complex viscous Burgers equation</em></a>. J. Reine Angew. Math. 616 (2008), 205–217; <a href="https://arxiv.org/abs/math/0612506">arXiv version</a>.</li>
            <li id="ref-91">H. Dong and Q. S. Zhang. <a href="https://arxiv.org/abs/1907.01687"><em>Time analyticity for the heat equation and Navier–Stokes equations</em></a>. J. Funct. Anal. 279 (2020), 108563.</li>
            <li id="ref-92">H. Matano. <a href="https://repository.dl.itc.u-tokyo.ac.jp/records/39589"><em>Nonincrease of the lap-number of a solution for a one-dimensional semilinear parabolic equation</em></a>. J. Fac. Sci. Univ. Tokyo Sect. IA Math. 29 (1982), 401–441.</li>
            <li id="ref-93">L. de Branges. <a href="https://www.math.purdue.edu/~branges/Hilbert%20Spaces%20of%20Entire%20Functions.pdf"><em>Hilbert Spaces of Entire Functions</em></a>. Prentice-Hall (1968).</li>
            <li id="ref-94">J. Ortega-Cerdà and K. Seip. <a href="https://annals.math.princeton.edu/2002/155-3/p03"><em>Fourier frames</em></a>. Ann. of Math. 155 (2002), 789–806.</li>
            <li id="ref-95">B. Ya. Levin. <a href="https://bookstore.ams.org/mmono-5/"><em>Distribution of Zeros of Entire Functions</em></a>. American Mathematical Society (1964).</li>'''
    html = replace_once(html, ref_89, ref_89 + refs_g, "literature refs G")
    return html


def update_manifest(text: str) -> str:
    data = json.loads(text)
    data.update(
        {
            "latestCompletedRelease": "r072g",
            "siteVersion": "1.20",
            "publicHtmlNoteCount": 157,
            "postR060RecapNodeCount": 97,
            "postR070APublishedReleaseCount": 59,
            "postR070AFormalSealedReleaseCount": 35,
            "legacyFormalFigureBacklogCount": 24,
            "nextRelease": "r072h",
            "latestReleaseGate": "tests/r072g-complete-root-packing-gate.test.mjs",
        }
    )
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def update_site_version(text: str) -> str:
    data = json.loads(text)
    data.update(
        {
            "version": "1.20",
            "latestRelease": "R0.72G",
            "publicHtmlNoteCount": 157,
            "publishedDate": DATE,
        }
    )
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def update_inventory(text: str) -> str:
    data = json.loads(text)
    published = data["publishedReleases"]
    sealed = data["formalSealedReleases"]
    if "r072g" not in published:
        published.append("r072g")
    if "r072g" not in sealed:
        sealed.append("r072g")
    if len(published) != 59:
        raise RuntimeError(f"published inventory count is {len(published)}, expected 59")
    if len(sealed) != 35:
        raise RuntimeError(f"sealed inventory count is {len(sealed)}, expected 35")
    backlog = data["legacyFormalFigureBacklog"]
    if len(backlog) != 24:
        raise RuntimeError(f"legacy backlog count is {len(backlog)}, expected 24")
    data.update(
        {
            "latestPublishedRelease": "r072g",
            "publishedReleaseCount": len(published),
            "formalSealedReleaseCount": len(sealed),
            "legacyFormalFigureBacklogCount": len(backlog),
        }
    )
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")


def audit_text_output(path: Path) -> None:
    payload = path.read_bytes()
    controls = [
        (index, byte)
        for index, byte in enumerate(payload)
        if byte < 32 and byte not in (9, 10)
    ]
    if controls:
        raise RuntimeError(f"{path}: forbidden C0 controls {controls[:8]}")
    text = payload.decode("utf-8")
    broken_tokens = (
        "deltage",
        "asymplog",
        "delta_R,qquad",
        "墠",
        "G_{m all}",
        "G_{ m all}",
    )
    present = [token for token in broken_tokens if token in text]
    if present:
        raise RuntimeError(f"{path}: broken TeX tokens {present}")


def main() -> None:
    note = PUBLIC / "notes" / "r0-72g.html"
    recap = PUBLIC / "recap-r0-61-r0-72g.html"
    home = PUBLIC / "research-review.html"
    literature = PUBLIC / "literature-review.html"
    manifest = ROOT / "research" / "release-manifest.json"
    site_version = PUBLIC / "site-version.json"
    inventory = ROOT / "research" / "formal-archive-inventory.json"
    write(note, NOTE_HTML)
    write(recap, build_recap())
    write(home, update_home(home.read_text(encoding="utf-8")))
    write(literature, update_literature(literature.read_text(encoding="utf-8")))
    write(manifest, update_manifest(manifest.read_text(encoding="utf-8")))
    write(site_version, update_site_version(site_version.read_text(encoding="utf-8")))
    write(inventory, update_inventory(inventory.read_text(encoding="utf-8")))
    for path in (note, recap, home, literature):
        audit_text_output(path)
    note_count = len(list((PUBLIC / "notes").glob("*.html")))
    if note_count != 157:
        raise RuntimeError(f"public HTML note count is {note_count}, expected 157")
    print(json.dumps({"release": "R0.72G", "siteVersion": "1.20", "noteCount": note_count, "recapNodes": 97, "published": 59, "formalSealed": 35, "legacyBacklog": 24}, ensure_ascii=False))


if __name__ == "__main__":
    main()
