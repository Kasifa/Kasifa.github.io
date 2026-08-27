#!/usr/bin/env python3

"""Generate the Chinese R0.72E web release from the sealed R0.72D state.

The generator is deliberately strict and idempotent. Mutable pages must be
either the expected v1.17 state or the already-generated v1.18 state.
Generated note/recap files are deterministic and may not be overwritten after
drift. The script does not render PDFs, build figures, update translations, or
run publication tests.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
OLD_VERSION = "1.17"
NEW_VERSION = "1.18"
PUBLISHED_DATE = "2026-08-27"


def replace_once(text: str, before: str, after: str, label: str) -> str:
    count = text.count(before)
    if count != 1:
        raise RuntimeError(f"{label}: expected one old anchor, found {count}")
    return text.replace(before, after, 1)


def replace_all(
    text: str, before: str, after: str, expected_count: int, label: str
) -> str:
    count = text.count(before)
    if count != expected_count:
        raise RuntimeError(
            f"{label}: expected {expected_count} old anchors, found {count}"
        )
    return text.replace(before, after)


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise RuntimeError(f"{label}: expected one new anchor, found {count}")


def require_absent(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count:
        raise RuntimeError(f"{label}: forbidden stale anchor occurs {count} time(s)")


def classify_text_state(
    text: str, old_marker: str, new_marker: str, label: str
) -> str:
    old_count = text.count(old_marker)
    new_count = text.count(new_marker)
    if old_count == 1 and new_count == 0:
        return "old"
    if old_count == 0 and new_count == 1:
        return "new"
    raise RuntimeError(
        f"{label}: expected exactly one old or new marker; "
        f"old={old_count}, new={new_count}"
    )


def write_deterministic(path: Path, content: str, label: str) -> bool:
    if path.exists():
        if path.read_text(encoding="utf-8") != content:
            raise RuntimeError(f"{label}: existing generated file drifted: {path}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


NOTE_HTML = r'''<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <meta name="description" content="研究笔记 R0.72E：精确单载波三角形 NSE 家族在完整负 Sobolev 旋转电荷有界时，使 complete-root ledger 相对 D^{1/3}Λ₁ 以 R^{4/3} 发散。">
  <meta property="og:type" content="article">
  <meta property="og:title" content="R0.72E｜单载波超临界根账本与候选 D^{1/3}Λ₁ payment 失效">
  <meta property="og:description" content="Feynman–Kac、驻相和定量 Hörmander 密度给出完整 H^{-1} action；精确 Bessel 根族使候选归一化支付发散。">
  <meta property="og:image" content="https://kasifa.github.io/figures/r0-72e-supercritical-ledger.png">
  <title>R0.72E｜单载波超临界根账本与候选 D^{1/3}Λ₁ payment 失效</title>
  <script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.90">
  <style>.hero h1{font-size:clamp(1.62rem,3.5vw,2.9rem)}pre{max-width:100%;overflow-x:auto}.audit-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem}.audit-card{border:1px solid var(--line);padding:1rem}.audit-card strong{display:block;color:var(--gold);font-family:var(--mono);margin-bottom:.45rem}@media(max-width:760px){.audit-grid{grid-template-columns:1fr}}@media print{body{font-size:8.7pt}.topline{height:3px}pre{max-width:none;overflow:visible!important;white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-size:7.3pt}}</style>
  <script defer src="/i18n-en.js?v=1.18"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#model">精确解</a><a href="#roots">根族</a><a href="#action">作用量</a><a href="#ledger">物理账本</a><a href="#entry">正进入</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72E · ONE CARRIER · FULL H⁻¹ ACTION · PAYMENT FAILURE</div>
        <h1>一个载波已经足够：<br>候选 \(D^{1/3}\Lambda_1\) payment 被排除</h1>
        <p class="lead">R0.72D 只把归一化 complete-root ledger 推到常数量级。我回到 R0.72A 的单载波 Bessel 家族，固定一个能隔离目标壳的整数 \(q_0\)，再直接估计全部 Fourier 模的负 Sobolev 旋转电荷。Feynman–Kac、驻相和定量漂移括号密度给出 \(Q_{\delta,q_0}=O(\log\delta/\delta)\)。取 \(\delta_R=R^4\) 后，完整 charge 保持有界，而 \(R\) 个正时间根使候选归一化比值按 \(R^{4/3}\) 发散。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72E 完成</span><strong>candidate D^{1/3}Λ₁ payment failure</strong><p>版本 v0.72E · 2026-08-27</p><p>analytic theorem: CLOSED</p><p>physical ledger: CLOSED</p><p>full-frequency charge: CLOSED</p><p>下一对象：frequency-sensitive repair</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节判断</a></li><li><a href="#model">01 · 精确三角形解</a></li><li><a href="#roots">02 · Bessel 根族</a></li><li><a href="#action">03 · 负 Sobolev action</a></li><li><a href="#ledger">04 · 完整物理账本</a></li><li><a href="#entry">05 · 正进入与发散</a></li><li><a href="#audit">06 · 双路证书</a></li><li><a href="#figure">07 · 正式附图</a></li><li><a href="#value">08 · 研究价值</a></li><li><a href="#next">09 · 下一步</a></li><li><a href="#claims">10 · 主张边界</a></li><li><a href="#reproduce">11 · 复现</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Direct verdict</div><h2>候选 \(D^{1/3}\Lambda_1\) 支付在精确光滑子类中失败</h2>
          <div class="equation result">\[
            \boxed{\frac{\mathcal J_{{\rm all},R}([0,T])}
            {D_R^{1/3}\Lambda_1([0,T];u_R)}
            \ge c_{T,q_0,T_*}R^{4/3}\longrightarrow\infty.}
          \]</div>
          <p>每个 \(u_R\) 都是无外力、全局光滑的三维 Navier–Stokes 解，属于 \(u=(f(y,z,t),0,v(y,t))\) 的精确三角形 2.5D 子类。这个定理严格排除的是 complete-root 账本的候选中间估计，不是正则性本身。</p>
          <div class="boundary"><strong>直接边界</strong><p>该家族没有爆破；它反而始终光滑。结论说明候选 \(D^{1/3}\Lambda_1\) complete-root 中间估计不能再作为一般证明的桥，但不排除加入新频率项、初始层费用或更强数据因子的替代估计。</p></div>
        </section>

        <section id="model"><div class="section-no">01 / Exact triangular NSE</div><h2>固定 \(q_0\) 同时保留精确演化与目标壳隔离</h2>
          <p>我取 \(\nu=d=K_z=r_1=1\)、\(K_y=0\)，并固定整数 \(q_0&gt;R_*\)。剪切和正 \(K_z\) sector 写成</p>
          <div class="equation result">\[
            v_R=P_Re^{-q_0^2t}(e^{iq_0y}+e^{-iq_0y}),\qquad
            \widehat f_R(q_0r,1,t)=S_RF_{R,r}(q_0^2t).
          \]</div>
          <div class="equation result">\[
            \partial_xF_R=D_qF_R+\delta_RV(x)F_R,\quad
            (D_qF)_r=-(r^2+q_0^{-2})F_r,\quad
            (VF)_r=-ie^{-x}(F_{r-1}+F_{r+1}).
          \]</div>
          <p>固定 \(q_0\) 不会改变根：精确标量共轭</p>
          <div class="equation result">\[
            \boxed{F_{q_0}(x)=e^{(1-q_0^{-2})x}F_1(x)}
          \]</div>
          <p>取 \(F_R(0)=ie_{-1}\)、\(P_R=q_0^2\delta_R\)。所有 \(r\ne0\) active modes 和剪切模都在固定 target multiplier 之外；壳内只剩 \(\pm(0,0,1)\)。这修复了 \(q=1\) 时 radial annulus 无法隔离目标的问题。</p>
          <div class="equation result">\[
            v_t=v_{yy},\qquad f_t+vf_z=f_{yy}+f_{zz},\qquad
            \mathbb P(u\times\omega)=(-vf_z,0,0).
          \]</div>
        </section>

        <section id="roots"><div class="section-no">02 / Exact Bessel roots</div><h2>前 \(R\) 个根在 \(O(R^{-3})\) 初始层内保持简单</h2>
          <p>令 \(\delta_R=R^4\)、\(U_R(\tau)=F_R(\tau/\delta_R)\)。冻结系统的目标坐标是 \(P_0W(\tau)=J_1(2\tau)\)。增长窗口上的 \(C^1\) 比较误差为 \(O_{q_0}(R^{-1})\)，小于最弱 Bessel slope 的 \(R^{-1/2}\)。因此</p>
          <div class="equation result">\[
            0&lt;t_{k,R}=q_0^{-2}x_{k,R}\le C_{q_0}R^{-3},\qquad
            \sum_{k=1}^R|P_0V(x_{k,R})F_R(x_{k,R})|^2
            =\frac8{\pi^2}\log R+O_{q_0}(1).
          \]</div>
          <p>这些都是固定物理区间 \([0,T]\) 内的正时间内点；我没有把 launch endpoint 算入这 \(R\) 个根。</p>
        </section>

        <section id="action"><div class="section-no">03 / Negative Sobolev action</div><h2>Feynman–Kac 把完整 \(H^{-1}\) 作用量化成二维小球问题</h2>
          <p>令 \(A_q=q_0^{-2}-\partial_\theta^2\) 和
          \(Q_{\delta,q_0}(X)=\int_0^X\|V(x)\phi(x)\|_{A_q^{-1}}^2dx\)。
          对 \(B_t=\sqrt2W_t\)、\(Z_t=\int_0^te^{-(t-s)}e^{iB_s}ds\)，正确的反向时间公式是</p>
          <div class="equation result">\[
            \phi(t,\theta)=ie^{-q_0^{-2}t}e^{-i\theta}
            \mathbb E\!\left[e^{-iB_t}
            e^{-2i\delta\operatorname{Re}(e^{i\theta}Z_t)}\right].
          \]</div>
          <p>固定相位驻相给 \(A_q^{-1}\) norm square \(\lesssim(1+\kappa)^{-1}\)。过程 \(dB=\sqrt2dW\)、\(dZ=(-Z+e^{iB})dt\) 的两个漂移括号在每一点都张成两个 \(Z\) 方向；它们与噪声场组成的绝对行列式恒为 \(4\)。Kusuoka–Stroock Part II 的定量密度界和 Brownian 反射原理给 \(\mathbb E|Z_t|^{-1}\le C_X/t\)，所以</p>
          <div class="equation result">\[
            \boxed{Q_{\delta,q_0}(X)
            \le C_{X,q_0}\frac{1+\log(2+\delta)}{\delta},
            \qquad\delta\ge1.}
          \]</div>
          <p>仅有 smooth density 不够；这里需要小时间多项式上界。常数也不对 \(q_0\to\infty\) 一致，所以 \(q_0\) 必须固定。</p>
        </section>

        <section id="ledger"><div class="section-no">04 / Full physical ledger</div><h2>所有 \(q_0\) 因子和全部 Lamb 频率都进入账本</h2>
          <p>我选择 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、\(S_R^2=\delta_R/\log(2+\delta_R)\)。精确数据和涡量分解为</p>
          <div class="equation result">\[
            D_R=2P_R^2(1+q_0^2)+2S_R^2(q_0^2+2),
          \]</div>
          <div class="equation result">\[
            Y_R(t)=2q_0^2P_R^2e^{-2x}
            +2S_R^2(\|F_R(x)\|_2^2
            +q_0^2\|\partial_\theta\phi_R(x)\|_2^2).
          \]</div>
          <p>能量收缩与一阶矩屏障给 \(D_R\asymp_{q_0}\delta_R^2\) 和 \(\mathcal R_Y([0,T])=O_{T,q_0}(1)\)，不需要额外背景。完整 projected Lamb field 满足</p>
          <div class="equation result">\[
            \|\mathbb P(u_R\times\omega_R)\|_{\dot H^{-1}}^2
            =2S_R^2P_R^2q_0^{-2}\|VF_R\|_{A_q^{-1}}^2.
          \]</div>
          <p>\(H^{-1}\) 权重、时间 Jacobian 和 shear-enstrophy denominator 各贡献 \(q_0^{-2}\)，故</p>
          <div class="equation result">\[
            \frac1T\int_0^T
            \frac{\|\mathbb P(u_R\times\omega_R)\|_{\dot H^{-1}}^2}{Y_R(t)}dt
            \le\frac{e^{2q_0^2T}S_R^2}{Tq_0^6}
            Q_{\delta_R,q_0}(q_0^2T)=O_{T,q_0}(1).
          \]</div>
          <p>这是 full-frequency charge，不是 selected-shell proxy。</p>
        </section>

        <section id="entry"><div class="section-no">05 / Positive entries and divergence</div><h2>交替 crossing sign 不会损失一半根</h2>
          <p>完整 target shell 的每个根都满足
          \(C_{*,t}=-\Delta F_*\) 和
          \(\langle F_*,C_{*,t}\rangle=\|\nabla F_*\|_2^2&gt;0\)。
          因此全部 \(R\) 个根都是 positive right entries。求和给</p>
          <div class="equation result">\[
            \mathcal J_{{\rm all},R}\gtrsim_{q_0}
            \frac{\delta_R}{\log(2+\delta_R)}\log R
            \asymp_{q_0}\delta_R.
          \]</div>
          <p>结合 \(D_R^{1/3}\asymp\delta_R^{2/3}\) 与 bounded \(\Lambda_1\)，得到 \(\delta_R^{1/3}=R^{4/3}\) 发散。</p>
        </section>

        <section id="audit"><div class="section-no">06 / Independent certificates</div><h2>解析证明、producer 和独立 checker 分开承担责任</h2>
          <div class="audit-grid">
            <div class="audit-card"><strong>PRODUCER · 16/16 PASS</strong><p>Fourier split-step；action 窗口固定为 \(X=6\)。有限值为 \(Q_{16}=1.329601902\)、\(Q_{512}=0.097737613\)。同时重算 fixed-\(q_0\) Bessel roots、selected slope mass、first-moment barrier 和指数账本。</p></div>
            <div class="audit-card"><strong>INDEPENDENT · 16/16 PASS</strong><p>不导入 producer，独立 action 窗口固定为 \(X=1\)：\(Q_{16}=1.326217539\)、\(Q_{128}=0.307998939\)。\(R=64\) root mass 为 \(3.565301087\)，相对 frozen 值偏差 \(-4.71\times10^{-6}\)。</p></div>
          </div>
          <p>两个 action 数列属于不同的 \(X\) 窗口，不能逐项互比。有限计算只核对符号、归一化和代表性截断；无限格根证明、驻相、Malliavin 密度与 \(R\to\infty\) 结论由解析报告承担。</p>
        </section>

        <section id="figure"><div class="section-no">07 / Journal figure</div><h2>正式附图分开显示根质量、作用量和最终发散</h2>
          <figure><img src="/figures/r0-72e-supercritical-ledger.svg" alt="R0.72E Bessel root mass, negative Sobolev action, and supercritical normalized ledger"><figcaption>图 R0.72E-1。有限截断展示 selected slope mass 的对数增长、负 Sobolev action 的衰减和最终 \(R^{4/3}\) 标度。数值曲线只作有限审计；极限结论来自解析定理。</figcaption></figure>
        </section>

        <section id="value"><div class="section-no">08 / Research value</div><h2>一条候选证明路线被真正关闭</h2>
          <p>从 R0.71X 到 R0.72D，\(D^{1/3}\Lambda_1\) 一直是 complete-root ledger 的候选支付。当前家族把 exact roots、真实数据、固定物理区间、enstrophy contrast 和 full-frequency charge 放进同一个光滑 NSE 解中，仍使比值发散。因此继续证明这一候选估计已经没有意义。</p>
          <p>对千禧年问题的价值仍是间接的：我排除了一座可能的桥，没有得到 continuation criterion。反例就在全局光滑不变子类中，也说明 raw zero-crossing ledger 可能比正则性所需的量更强。</p>
        </section>

        <section id="next"><div class="section-no">09 / Next finite gate</div><h2>R0.72F 寻找最小 frequency-sensitive repair</h2>
          <p>我会依次测试 frequency-sensitive initial-layer charge、time-weighted rotational action 和直接记录 coupling scale 的数据项。候选先要阻断当前 exact family，再检查是否仍由 Leray 级信息支付；若它已经等价于未知临界范数，就停止该路线。</p>
        </section>

        <section id="claims"><div class="section-no">10 / Claim boundary</div><h2>本节证明什么，也明确不证明什么</h2>
          <ul>
            <li><strong>已证明：</strong>fixed-\(q_0\) Bessel 根、定量 \(A_q^{-1}\) action decay、完整数据与 enstrophy、full-frequency charge 有界、normalized ledger 发散。</li>
            <li><strong>已排除：</strong>声明子类内的 \(\mathcal J_{\rm all}\le CD^{1/3}\Lambda_1\)，其中 \(C\) 与光滑初值无关。</li>
            <li><strong>仍开放：</strong>frequency-sensitive 修正、一般三维 critical-norm bridge、非三角形动力学中的对应结构。</li>
            <li><strong>没有得到：</strong>有限时奇性、一般三维 global regularity、continuation criterion、原创性或优先权结论。</li>
          </ul>
        </section>

        <section id="reproduce"><div class="section-no">11 / Reproduce</div><h2>证明、文献边界、证书、正式附图和累计回顾完整保留</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_independent_audit.md">独立逐式审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072e">producer / independent 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger">附图、数据、manifest、validation 与源代码包</a> · <a href="/figures/r0-72e-supercritical-ledger.pdf">期刊附图 PDF</a></p>
          <p><a href="/notes/r0-72e.pdf">下载同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72e.html">阅读 R0.60 之后累计回顾</a> · <a href="/recap-r0-61-r0-72e.pdf">下载累计回顾 PDF</a></p>
          <pre><code>python3 research/r072e_exact_audit.py --output research/certificates/r072e/result.json
python3 research/r072e_independent_audit.py --output research/certificates/r072e/independent-result.json
python3 figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/build_figure.py --config figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/config.json
python3 figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/qa_images.py --config figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/config.json
python3 figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/validate.py --config figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/config.json</code></pre>
        </section>
      </article>
    </div>
  </main>
  <footer><div>R0.72E · 2026-08-27 · 个人数学研究日志<br><a href="/">返回研究主页</a> · <a href="/literature-review.html">文献综述</a> · <a href="/recap-r0-61-r0-72e.html">累计回顾</a></div></footer>
</body>
</html>
'''


def build_recap() -> str:
    """Derive the 95-node recap from the sealed 94-node R0.72D recap."""

    html = (PUBLIC / "recap-r0-61-r0-72d.html").read_text(encoding="utf-8")
    replacements = [
        (
            '<meta name="description" content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72D 的 94 个研究节点；最新一节构造高频平移 Rudin–Shapiro 内点根，并在保留 full rotational charge 后得到非消失 normalized complete-root ledger。">',
            '<meta name="description" content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72E 的 95 个研究节点；最新一节用单载波 Bessel 根族与完整 H^{-1} action 严格排除候选 D^{1/3}Λ₁ 支付。">',
            "recap description",
        ),
        (
            '<meta property="og:title" content="R0.61–R0.72D｜R0.60 之后的研究回顾">',
            '<meta property="og:title" content="R0.61–R0.72E｜R0.60 之后的研究回顾">',
            "recap og title",
        ),
        (
            '<meta property="og:description" content="二十一个阶段、94 个节点：从约化递推和 complete-root 账本，到 physical phases，再到真实内点根与 full-charge normalized saturation。">',
            '<meta property="og:description" content="二十二个阶段、95 个节点：从约化递推和 complete-root 账本，到 full-charge saturation，再到候选 D^{1/3}Λ₁ payment 的严格失效。">',
            "recap og description",
        ),
        (
            "<title>R0.61–R0.72D｜R0.60 之后的研究回顾</title>",
            "<title>R0.61–R0.72E｜R0.60 之后的研究回顾</title>",
            "recap title",
        ),
        ('/i18n-en.js?v=1.17', '/i18n-en.js?v=1.18', "recap i18n"),
        (
            '<div class="eyebrow">累计回顾 · R0.61–R0.72D · 2026-08-27</div>',
            '<div class="eyebrow">累计回顾 · R0.61–R0.72E · 2026-08-27</div>',
            "recap eyebrow",
        ),
        (
            '<p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72D 的 94 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。</p>',
            '<p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72E 的 95 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。</p>',
            "recap lead",
        ),
        (
            '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72D</strong><p>收录节点：94</p><p>回顾截止时公开笔记：154</p><p>回顾截止节点：R0.72D</p><p>问题状态：仍未解决</p></div>',
            '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72E</strong><p>收录节点：95</p><p>回顾截止时公开笔记：155</p><p>回顾截止节点：R0.72E</p><p>问题状态：仍未解决</p></div>',
            "recap stamp",
        ),
        (
            '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 二十一个研究阶段</a></li><li><a href="#node-index">02 · 94 节完整索引</a></li>',
            '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 二十二个研究阶段</a></li><li><a href="#node-index">02 · 95 节完整索引</a></li>',
            "recap toc",
        ),
        (
            '<div class="metric"><strong>94</strong><span>R0.61–R0.72D 研究节点</span></div>\n            <div class="metric"><strong>56</strong><span>R0.70A–R0.72D 已公开并封存版本</span></div>\n            <div class="metric"><strong>21</strong><span>按问题划分的研究阶段</span></div>',
            '<div class="metric"><strong>95</strong><span>R0.61–R0.72E 研究节点</span></div>\n            <div class="metric"><strong>57</strong><span>R0.70A–R0.72E 已公开并封存版本</span></div>\n            <div class="metric"><strong>22</strong><span>按问题划分的研究阶段</span></div>',
            "recap metrics",
        ),
        (
            "后面的 94 个节点沿着这个缺口推进；R0.70A–R0.72D 的 56 个版本已经公开并封存",
            "后面的 95 个节点沿着这个缺口推进；R0.70A–R0.72E 的 57 个版本已经公开并封存",
            "recap scope counts",
        ),
        (
            '<section id="timeline"><div class="section-no">01 / 研究过程</div><h2>R0.60 之后的路线分成二十一个阶段</h2>',
            '<section id="timeline"><div class="section-no">01 / 研究过程</div><h2>R0.60 之后的路线分成二十二个阶段</h2>',
            "recap phase count",
        ),
        (
            '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.72D 的 94 节公开笔记</h2>',
            '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.72E 的 95 节公开笔记</h2>',
            "recap index title",
        ),
    ]
    for before, after, label in replacements:
        html = replace_once(html, before, after, label)

    phase_anchor = '              <div class="links"><a href="/notes/r0-72d.html">R0.72D</a><a href="/figures/r0-72d-dynamical-ledger.pdf">R0.72D 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072d">R0.72D 证书</a></div></article>'
    phase_e = r'''
            <article class="phase"><h3>R0.72E · 单载波 supercritical ledger 与候选 \(D^{1/3}\Lambda_1\) payment 失效</h3>
              <p>固定整数 \(q_0&gt;R_*\) 后，单载波 Bessel family 同时获得 target-shell isolation 与 exact diagonal conjugacy。前 \(R\) 个正时间简单根落在 \(O(R^{-3})\) 初始层，selected target-row mass 为 \((8/\pi^2)\log R+O(1)\)。</p>
              <p>Feynman–Kac 把完整 \(A_q^{-1}\) action 化成 kinetic Brownian path 的振荡平均；驻相和 Kusuoka–Stroock 的定量漂移括号密度界给 \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\)。取 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、\(S_R^2=\delta_R/\log(2+\delta_R)\)，则 \(D_R\asymp\delta_R^2\)、\(\Lambda_1=O(1)\)、\(\mathcal J_{\rm all}\gtrsim\delta_R\)，从而 normalized ratio 至少按 \(R^{4/3}\) 发散。这个结果排除一条候选中间估计，但所有解仍全局光滑。</p>
              <div class="links"><a href="/notes/r0-72e.html">R0.72E</a><a href="/figures/r0-72e-supercritical-ledger.pdf">R0.72E 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072e">R0.72E 证书</a></div></article>'''
    html = replace_once(html, phase_anchor, phase_anchor + phase_e, "recap phase E")

    html = replace_once(
        html,
        '            <span class="node-ref"><a href="/notes/r0-72d.html">R0.72D</a><span class="node-state kind-closed">闭</span></span>\n          </div>',
        '            <span class="node-ref"><a href="/notes/r0-72d.html">R0.72D</a><span class="node-state kind-closed">闭</span></span>\n            <span class="node-ref"><a href="/notes/r0-72e.html">R0.72E</a><span class="node-state kind-negative">否</span></span>\n          </div>',
        "recap node E",
    )

    retained_d = r'''            <li>R0.72D 的 shifted Rudin–Shapiro dynamical saturation：\(r_j=M+j\) 的热权 multiplier 满足 \(\int\|V_M\|\lesssim M^{-3/2}\)、\(\int\|V_M\|^2\lesssim M^{-1}\)；\(\eta\asymp M^2\) 时仍有 bounded Dyson exposure。一个 \(O(M^{-1/2})\) launch adjustment 在 \(\tau_M=M^{-3}\) 产生 exact simple interior root，slope 为 \(M\) 量级。匹配 background 与 full-frequency projected charge 给 bounded \(\mathcal R_Y\) 和 \(\Lambda_1\)，从而 complete normalized ledger 有正下界。该比值不发散，结论仍限于 exact triangular class。</li>'''
    retained_e = r'''
            <li>R0.72E 的 one-carrier supercritical no-go：固定整数 \(q_0&gt;R_*\) 后，R0.72A 的 Bessel 根通过精确 diagonal conjugacy 保持。Feynman–Kac、\(A_q^{-1}\) 驻相与定量 parabolic Hörmander density 给 full-frequency action \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\)。在 \(\delta_R=R^4\)、\(S_R^2=\delta_R/\log(2+\delta_R)\) 下，完整数据、固定区间 enstrophy contrast 与 rotational charge 都被支付，而 \(\mathcal J_{\rm all}/(D^{1/3}\Lambda_1)\gtrsim R^{4/3}\)。这严格排除候选 \(D^{1/3}\Lambda_1\) complete-root 中间估计，但不产生爆破或一般正则性结论。</li>'''
    html = replace_once(html, retained_d, retained_d + retained_e, "recap retained E")

    old_value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>静态 phase-free 上界已经由真实动力学达到，但比值仍停在 order one</h2>
          <p>截至 R0.72D，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 94 个节点或 56 个已公开并封存版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72C 留下的实际根缺口已经关闭。高频平移 Rudin–Shapiro family 同时保留真实 positive-time root、complete target slope、full data cost、fixed-interval enstrophy contrast 和 full rotational charge；normalized complete ledger 不再随 \(M\) 消失。</p>
          <p>这个结果仍是 exact triangular 2.5D class 内的 sharpness theorem。比值保持有限，没有反驳 \(D^{1/3}\Lambda_1\) payment。一般三维 vortex stretching 与 critical-norm continuation 仍未被触及。</p>
        </section>'''
    new_value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>候选 \(D^{1/3}\Lambda_1\) payment 已被严格排除，但千禧年问题没有因此前进一个“百分比”</h2>
          <p>截至 R0.72E，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 95 个节点或 57 个已公开并封存版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72D 留下的 supercritical alternative 已经实现。一个单载波、始终全局光滑的 exact triangular family，在 full-frequency \(H^{-1}\) rotational charge、真实数据成本和固定区间 enstrophy 全部计入后，仍使 complete-root ledger 相对 \(D^{1/3}\Lambda_1\) 发散。</p>
          <p>这关闭的是候选中间估计，不是正则性问题。它还提示 raw zero-crossing ledger 可能过强：它能在没有任何奇性风险的光滑不变子类里积累。</p>
        </section>'''
    html = replace_once(html, old_value, new_value, "recap value E")

    old_next = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72E 检查 supercritical growth 与 universal order-one ceiling</h2>
          <p>第一条路线把 \(\eta\) 提到 \(M^2\) 以上，并同时改变 block height、width 或 phase geometry，检查 numerator 是否能比 full rotational charge 更快增长。</p>
          <p>如果所有 supercritical routes 都让 \(\Lambda_1\) 同阶增加，第二条路线就证明 triangular class 的 order-one ceiling。两条路线都必须保留 positive-time exact root、固定物理区间、完整 background cost 和 full-frequency charge。</p>
        </section>'''
    new_next = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72F 寻找最小 frequency-sensitive repair</h2>
          <p>下一有限任务先让每个修正量通过 R0.72E exact family：frequency-sensitive initial-layer charge、time-weighted rotational action，以及直接记录 coupling scale 的数据项，必须至少阻断 \(R^{4/3}\) 发散。</p>
          <p>通过反例测试还不够。候选随后必须能由 Leray 级或已知 continuation budget 支付；如果它已经强到等价于未知临界范数，就停止该路线。</p>
        </section>'''
    html = replace_once(html, old_next, new_next, "recap next F")

    html = replace_once(
        html,
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72c.html">保留 R0.72C 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72d.html">打开最新节点 R0.72D</a></p>',
        '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72d.html">保留 R0.72D 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72e.html">打开最新节点 R0.72E</a></p>',
        "recap reproduce navigation",
    )
    html = replace_once(
        html,
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072d">查看 R0.72D 双路证书</a> · <a href="/recap-r0-61-r0-72d.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72c.pdf">上一版累计回顾 PDF</a>',
        '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072e">查看 R0.72E 双路证书</a> · <a href="/recap-r0-61-r0-72e.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72d.pdf">上一版累计回顾 PDF</a>',
        "recap reproduce links",
    )
    html = replace_once(
        html,
        '<div>R0.61–R0.72D 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div>',
        '<div>R0.61–R0.72E 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div>',
        "recap footer",
    )
    require_once(html, "收录节点：95", "recap post node count")
    require_once(
        html, 'href="/notes/r0-72e.html">R0.72E</a><span', "recap post node"
    )
    require_once(
        html, "R0.72F 寻找最小 frequency-sensitive repair", "recap post next"
    )
    return html


def update_home(html: str) -> str:
    """Advance the homepage from the exact v1.17/R0.72D state."""

    replacements = [
        (
            '<html lang="zh-CN" data-site-version="1.17">',
            '<html lang="zh-CN" data-site-version="1.18">',
            "home data version",
        ),
        ('/i18n-en.js?v=1.17', '/i18n-en.js?v=1.18', "home i18n"),
        ('/site-refresh.js?v=1.17', '/site-refresh.js?v=1.18', "home refresh"),
        (
            '<span><strong>v1.17</strong>网页版本</span>',
            '<span><strong>v1.18</strong>网页版本</span>',
            "home visible version",
        ),
        (
            '<span><strong>154</strong>公开研究笔记</span>',
            '<span><strong>155</strong>公开研究笔记</span>',
            "home note count",
        ),
        (
            '<span><strong>R0.72D</strong>最新研究节点</span>',
            '<span><strong>R0.72E</strong>最新研究节点</span>',
            "home latest release",
        ),
        (
            '<span><strong>supercritical growth vs universal order-one ceiling</strong>当前方向</span>',
            '<span><strong>frequency-sensitive repair after candidate-payment failure</strong>当前方向</span>',
            "home current direction",
        ),
        (
            '<div class="summary-item"><strong>我目前关注</strong><span>检查 R0.72D 的 order-one dynamical saturation 能否被超临界增长超过，或是否存在 triangular class 的普适 order-one ceiling。</span></div>',
            '<div class="summary-item"><strong>我目前关注</strong><span>R0.72E 已在 exact smooth class 中排除候选 \\(D^{1/3}\\Lambda_1\\) complete-root payment；下一步寻找最小的 frequency-sensitive repair，并检查它是否仍由 Leray 级信息支付。</span></div>',
            "home focus",
        ),
        (
            '<p class="eyebrow">Research topology · R0.1–R0.72D</p>',
            '<p class="eyebrow">Research topology · R0.1–R0.72E</p>',
            "home topology eyebrow",
        ),
    ]
    for before, after, label in replacements:
        html = replace_once(html, before, after, label)

    html = replace_all(
        html,
        "/recap-r0-61-r0-72d.html",
        "/recap-r0-61-r0-72e.html",
        21,
        "home recap html links",
    )
    html = replace_all(
        html,
        "/recap-r0-61-r0-72d.pdf",
        "/recap-r0-61-r0-72e.pdf",
        20,
        "home recap pdf links",
    )
    html = replace_all(
        html,
        "R0.69P–R0.72D",
        "R0.69P–R0.72E",
        3,
        "home current route ranges",
    )
    html = replace_all(
        html,
        "R0.70A–R0.72D",
        "R0.70A–R0.72E",
        2,
        "home sealed route ranges",
    )

    html = replace_once(
        html,
        '<h3>从 complete-root 局部暴露走到真实内点根与 full-charge saturation</h3>',
        '<h3>从 complete-root 局部暴露走到候选 payment 的严格失效</h3>',
        "home current route title",
    )
    html = replace_once(
        html,
        '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A 把强耦合代价局部化到实际观察层，R0.72B 再以精确 target row 收紧 complete-root 前因子。R0.72C 对任意 physical Fourier phases 得到 sharp \\(M^{-8/3}\\) exact-launch prefactor。R0.72D 把 Rudin–Shapiro 块平移到 \\([M,2M)\\)，构造正时间简单根并保留完整数据成本、固定区间涡量与 full rotational charge；normalized complete-root ledger 有严格正下界，但仍停在 order one。</p>',
        '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A–C 建立 Bessel lower family、target-row participation 与 physical-phase sharp scales；R0.72D 再实现 positive-time root 与 full-charge order-one saturation。R0.72E 固定 \\(q_0&gt;R_*\\)，用 Feynman–Kac、驻相和定量 Hörmander density 控制完整 \\(H^{-1}\\) action；exact one-carrier family 最终使 complete-root ledger 相对候选 \\(D^{1/3}\\Lambda_1\\) payment 按 \\(R^{4/3}\\) 发散。</p>',
        "home current route narrative",
    )
    html = replace_once(
        html,
        " → full-charge normalized order-one saturation</p>",
        " → full-charge normalized order-one saturation → fixed-carrier shell isolation → negative-Sobolev action decay → candidate D^{1/3}Λ₁ payment failure</p>",
        "home route path tail",
    )
    html = replace_once(
        html,
        "<summary>展开 64 篇公开笔记</summary>",
        "<summary>展开 65 篇公开笔记</summary>",
        "home current route note count",
    )
    html = replace_once(
        html,
        '                  <a class="milestone" href="/notes/r0-72d.html">R0.72D</a>\n',
        '                  <a class="milestone" href="/notes/r0-72d.html">R0.72D</a>\n                  <a class="milestone" href="/notes/r0-72e.html">R0.72E</a>\n',
        "home route note E",
    )

    old_next = r'''            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72E</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>supercritical growth vs universal order-one ceiling</h3>
              <p>先把 effective coupling 提到 \(M^2\) 以上，并改变 block height、width 或 phase geometry，检查 normalized numerator 能否比 full rotational charge 更快增长。若所有路线都同步抬高 \(\Lambda_1\)，则转向证明 triangular class 的普适 order-one ceiling。</p>
            </article>'''
    new_next = r'''            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72F</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>frequency-sensitive repair after candidate-payment failure</h3>
              <p>依次测试 initial-layer frequency charge、time-weighted rotational action 和显式 coupling-scale data term。候选必须先阻断 R0.72E exact family，再证明它不等价于尚未知的临界范数。</p>
            </article>'''
    html = replace_once(html, old_next, new_next, "home next F")

    old_recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72D · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 94 个节点；全站现有 154 篇公开研究笔记</h3>
            <p>R0.60 之后的累计回顾按二十一个阶段组织。R0.61–R0.69O 保留约化递推、剪切边界、横向扰动与压力局部预算；R0.69P–R0.71T 依次检查静态环带、协方差谱、projected-Lamb heat、faces、incidence 与真实内部 entry；R0.71U–R0.71Z 处理 second-time jet、complete first row 与全部根边界；R0.72A–C 依次给出 local exposure、target-row participation 与 physical-phase sharp prefactor；R0.72D 再把这个静态尖锐尺度实现为 positive-time exact root 与 full-charge normalized order-one saturation。R0.70A–R0.72E 共 56 个已公开并封存版本。</p>
            <p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72D 在 exact triangular 2.5D class 中证明真实正时间根、完整 target slope 与 full rotational charge 可以同时保持非退化，使 normalized complete-root ledger 不再趋零；比值仍为 order one，因此不是 payment failure 或一般 NSE 正则性结论。</p>
            <p><a href="/recap-r0-61-r0-72e.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72e.pdf">下载同步 PDF</a></p>
          </div>'''
    new_recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72E · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 95 个节点；全站现有 155 篇公开研究笔记</h3>
            <p>R0.60 之后的累计回顾按二十二个阶段组织。R0.61–R0.69O 保留约化递推、剪切边界、横向扰动与压力局部预算；R0.69P–R0.71T 依次检查静态环带、协方差谱、projected-Lamb heat、faces、incidence 与真实内部 entry；R0.71U–R0.71Z 处理 second-time jet、complete first row 与全部根边界；R0.72A–D 依次给出 Bessel lower family、target-row participation、physical-phase sharp prefactor 与 full-charge order-one saturation；R0.72E 再用 fixed-carrier exact family 严格排除候选 \(D^{1/3}\Lambda_1\) payment。R0.70A–R0.72E 共 57 个已公开并封存版本。</p>
            <p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72E 的每个解都全局光滑；它证明的是 complete-root ledger 的候选中间估计失败，并提示 raw zero-crossing ledger 可能比正则性需要更强。</p>
            <p><a href="/recap-r0-61-r0-72e.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72e.pdf">下载同步 PDF</a></p>
          </div>'''
    html = replace_once(html, old_recap, new_recap, "home recap card")

    old_d_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72E：</strong>&nbsp;检查 supercritical growth 与 universal order-one ceiling：任何候选都必须保留 positive-time exact root、固定物理区间、完整 background cost 与 full-frequency charge。</p>
          </div>'''
    new_e_card = r'''            <p><strong style="color:var(--gold)">R0.72E 已完成：</strong>&nbsp;一个 fixed-carrier exact family 在完整 \(H^{-1}\) rotational charge 有界时，使 normalized complete-root ledger 按 \(R^{4/3}\) 发散；这排除候选 \(D^{1/3}\Lambda_1\) payment。</p>
          </div>

          <div class="task-one" id="r072e" data-release="r072e" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72E · 2026-08-27</p>
            <h3>单载波 Bessel 根族严格排除候选 \(D^{1/3}\Lambda_1\) complete-root payment</h3>
            <p>
              固定整数 \(q_0&gt;R_*\)，取 \(\nu=d=K_z=r_1=1\)、\(K_y=0\)。
              载波隔离、精确 diagonal conjugacy 与 Bessel \(C^1\) 比较给前 \(R\) 个正时间简单根；
              selected target-row mass 为 \((8/\pi^2)\log R+O(1)\)。
            </p>
            <p>
              Feynman–Kac、固定相位驻相和定量 Hörmander density 给
              \[
                Q_{\delta,q_0}(X)\le C_{X,q_0}\frac{1+\log(2+\delta)}{\delta}.
              \]
              取 \(\delta_R=R^4\)、\(P_R=q_0^2\delta_R\)、
              \(S_R^2=\delta_R/\log(2+\delta_R)\)，完整数据与 enstrophy contrast 得到支付，
              full-frequency rotational charge 保持有界，而 \(\mathcal J_{\rm all}\gtrsim\delta_R\)。
            </p>
            <p>
              最终
              \[
                \frac{\mathcal J_{{\rm all},R}}
                {D_R^{1/3}\Lambda_1([0,T];u_R)}
                \ge cR^{4/3}\longrightarrow\infty.
              \]
              Producer 与 independent checker 均为 16/16 PASS；两路 action 窗口分别是 \(X=6\) 与 \(X=1\)，不能混合比较。
            </p>
            <p><strong>结论边界：</strong>&nbsp;这是 exact triangular 2.5D 光滑子类中的 candidate-payment no-go theorem。它没有构造奇性，没有给出 continuation criterion，也不解决一般三维 Navier–Stokes 正则性。</p>
            <p>
              <a href="/notes/r0-72e.html"><strong>阅读 R0.72E 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72e.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72e-supercritical-ledger.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072e">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072e_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger">查看附图、数据、进度与源代码包</a> ·
              <a href="/recap-r0-61-r0-72e.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72e.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.72F：</strong>&nbsp;寻找最小 frequency-sensitive repair，并要求它同时阻断当前 exact family、又能由已知 NSE 预算支付。</p>
          </div>'''
    html = replace_once(html, old_d_tail, new_e_card, "home release card E")

    html = replace_once(
        html,
        "        综述 v1.17 · 2026-08-27<br>\n        上次综述 v1.16 · 2026-08-27<br>",
        "        综述 v1.18 · 2026-08-27<br>\n        上次综述 v1.17 · 2026-08-27<br>",
        "home footer",
    )

    require_once(html, 'data-site-version="1.18"', "home post version")
    require_once(html, "<strong>155</strong>公开研究笔记", "home post note count")
    require_once(html, 'id="r072e" data-release="r072e"', "home post E card")
    require_once(html, "NEXT · R0.72F", "home post next")
    require_absent(html, "NEXT · R0.72E", "home stale next")
    return html


def update_literature(html: str) -> str:
    """Advance the literature map from the exact v1.17/R0.72D state."""

    html = replace_once(
        html, '/i18n-en.js?v=1.17', '/i18n-en.js?v=1.18', "literature i18n"
    )
    html = replace_all(
        html,
        "/recap-r0-61-r0-72d.html",
        "/recap-r0-61-r0-72e.html",
        6,
        "literature recap links",
    )
    html = replace_once(
        html,
        "我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72D 只列为研究笔记。我不把计算或笔记外推成正则性定理。",
        "我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72E 只列为研究笔记。我不把计算或笔记外推成正则性定理。",
        "literature scope",
    )
    html = replace_once(
        html,
        '<a href="/recap-r0-61-r0-72e.html">累计回顾与 94 节索引</a>',
        '<a href="/recap-r0-61-r0-72e.html">累计回顾与 95 节索引</a>',
        "literature deck recap count",
    )
    html = replace_once(
        html,
        '<a href="/recap-r0-61-r0-72e.html#node-index">打开 94 节完整索引</a>',
        '<a href="/recap-r0-61-r0-72e.html#node-index">打开 95 节完整索引</a>',
        "literature historical index count",
    )
    html = replace_once(
        html,
        "R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。一般 Navier–Stokes 正则性仍开放。",
        "R0.72D 在 shifted Rudin–Shapiro family 上构造 positive-time exact root，保留 full rotational charge，并得到非消失但不发散的 normalized complete-root ledger。R0.72E 回到 fixed-carrier Bessel family，以定量 negative-Sobolev action 证明 complete-root ledger 相对候选 \\(D^{1/3}\\Lambda_1\\) payment 按 \\(R^{4/3}\\) 发散。一般 Navier–Stokes 正则性仍开放。",
        "literature route deck E",
    )

    old_route_e = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72E</b><strong>supercritical growth vs universal order-one ceiling</strong></header><p>检查 coupling 超过 \(M^2\) 时 normalized numerator 能否比 full charge 更快增长；若不能，转向 triangular class 的普适 order-one ceiling。</p></div>'''
    new_route_e = r'''              <div class="route-step closed"><header><b>R0.72E</b><strong>fixed-carrier Bessel family 排除候选 \(D^{1/3}\Lambda_1\) payment</strong></header><p>固定 \(q_0&gt;R_*\) 隔离 target shell。Feynman–Kac、固定相位驻相与定量 Hörmander density 给 \(Q_{\delta,q_0}\lesssim\log(2+\delta)/\delta\)；取 \(\delta_R=R^4\) 后，full-frequency charge 有界而 normalized complete-root ledger 至少按 \(R^{4/3}\) 发散。所有解仍全局光滑。<a href="/notes/r0-72e.html">研究笔记</a> <a href="/recap-r0-61-r0-72e.html">当前累计回顾</a> <a href="#r072e-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72F</b><strong>frequency-sensitive repair</strong></header><p>候选修正必须先阻断 R0.72E exact family，再证明它能由 Leray 级或已知 continuation budget 支付。</p></div>'''
    html = replace_once(html, old_route_e, new_route_e, "literature route E/F")

    boundary_anchor = (
        "已核对主源没有提供 changing shifted profile 的 launch-inclusive root ledger "
        "或 full-charge lower family；这是有限文献检索结论，不作绝对原创性或优先权声明。</p></div>"
    )
    boundary_e = r'''
          <h3 id="r072e-boundary">R0.72E 的 kinetic density、Bessel 根与主张边界</h3>
          <p>R0.72E 固定整数 \(q_0&gt;R_*\)，因此 \(A_q=q_0^{-2}-\partial_\theta^2\) 的零模权重只进入常数。<a href="#ref-70">DLMF</a> 提供 Jacobi–Anger 展开、Bessel zeros 与导数渐近；它只负责 frozen root ledger。新的 action 证明把角 Brownian motion 提升到 \(dZ=(-Z+e^{iB})dt\)，再用 <a href="#ref-86">Kusuoka–Stroock Part II</a> 的 Corollary (3.25) 与 inequality (3.27) 取得小时间多项式密度界。驻相、负矩和时间积分随后给 \(Q_{\delta,q_0}\lesssim(1+\log(2+\delta))/\delta\)。</p>
          <div class="boundary"><strong>R0.72E 的主源边界</strong><p>仅有 smooth density 不能推出所需负矩；这里使用 Part II 的定量 polynomial bound，并通过 lifted terminal-angle 权重取得二维边缘密度。Part III 的相关 density section 有零漂移限制，不是本节依据。DLMF 不提供非自治 action，Kusuoka–Stroock 也不提供 Bessel roots、NSE amplitude ledger 或 candidate-payment no-go。当前结果排除的是本站声明的 \(D^{1/3}\Lambda_1\) complete-root 中间估计，不作绝对原创性、优先权、奇性或一般正则性声明。</p></div>'''
    html = replace_once(
        html, boundary_anchor, boundary_anchor + boundary_e, "literature boundary E"
    )

    ref85 = r'''            <li id="ref-85">S. Angenent. <a href="https://doi.org/10.1515/crll.1988.390.79"><em>The zero set of a solution of a parabolic equation</em></a>. J. Reine Angew. Math. 390 (1988), 79–96.</li>'''
    ref86 = r'''
            <li id="ref-86">S. Kusuoka and D. Stroock. <a href="https://doi.org/10.15083/00039520"><em>Applications of the Malliavin calculus, Part II</em></a>. J. Fac. Sci. Univ. Tokyo Sect. IA Math. 32 (1985), 1–76; Corollary (3.25) and inequality (3.27), pp. 22–23.</li>'''
    html = replace_once(html, ref85, ref85 + ref86, "literature reference 86")
    html = replace_once(
        html,
        "文献综述 v1.17 · 2026-08-27",
        "文献综述 v1.18 · 2026-08-27",
        "literature footer",
    )

    require_once(html, "<b>R0.72E</b><strong>fixed-carrier", "literature post E")
    require_once(html, "开放接口 · R0.72F", "literature post next")
    require_once(html, 'id="r072e-boundary"', "literature post boundary")
    require_once(html, 'id="ref-86"', "literature post reference")
    require_absent(html, "开放接口 · R0.72E", "literature stale open E")
    return html


def update_release_manifest(text: str) -> str:
    """Advance the release manifest with exact scalar anchors."""

    replacements = [
        (
            '"latestCompletedRelease": "r072d"',
            '"latestCompletedRelease": "r072e"',
            "manifest latest release",
        ),
        (
            '"siteVersion": "1.17"',
            '"siteVersion": "1.18"',
            "manifest site version",
        ),
        (
            '"publicHtmlNoteCount": 154',
            '"publicHtmlNoteCount": 155',
            "manifest note count",
        ),
        (
            '"postR060RecapNodeCount": 94',
            '"postR060RecapNodeCount": 95',
            "manifest recap nodes",
        ),
        (
            '"postR070ASealedReleaseCount": 56',
            '"postR070ASealedReleaseCount": 57',
            "manifest sealed count",
        ),
        (
            '"nextRelease": "r072e"',
            '"nextRelease": "r072f"',
            "manifest next release",
        ),
        (
            '"latestReleaseGate": "tests/r072d-dynamical-ledger-gate.test.mjs"',
            '"latestReleaseGate": "tests/r072e-supercritical-ledger-gate.test.mjs"',
            "manifest gate",
        ),
    ]
    for before, after, label in replacements:
        text = replace_once(text, before, after, label)
    return text


def update_site_version(text: str) -> str:
    """Advance the browser-visible compact version manifest."""

    replacements = [
        ('"version": "1.17"', '"version": "1.18"', "site version"),
        ('"latestRelease": "R0.72D"', '"latestRelease": "R0.72E"', "site latest"),
        (
            '"publicHtmlNoteCount": 154',
            '"publicHtmlNoteCount": 155',
            "site note count",
        ),
    ]
    for before, after, label in replacements:
        text = replace_once(text, before, after, label)
    return text


def write_if_changed(path: Path, before: str, after: str) -> bool:
    if before == after:
        return False
    path.write_text(after, encoding="utf-8")
    return True


def verify_home_new(html: str) -> None:
    require_once(html, 'data-site-version="1.18"', "home final version")
    require_once(html, "<strong>155</strong>公开研究笔记", "home final notes")
    require_once(html, 'id="r072e" data-release="r072e"', "home final release")
    require_once(html, "NEXT · R0.72F", "home final next")
    require_once(
        html,
        '<a class="milestone" href="/notes/r0-72e.html">R0.72E</a>',
        "home final route note",
    )
    require_absent(html, "NEXT · R0.72E", "home final stale next")


def verify_literature_new(html: str) -> None:
    require_once(html, '/i18n-en.js?v=1.18', "literature final version")
    require_once(html, "<b>R0.72E</b><strong>fixed-carrier", "literature final E")
    require_once(html, "开放接口 · R0.72F", "literature final next")
    require_once(html, 'id="r072e-boundary"', "literature final boundary")
    require_once(html, 'id="ref-86"', "literature final reference")
    require_absent(html, "开放接口 · R0.72E", "literature final stale next")


def verify_manifest_new(text: str) -> None:
    data = json.loads(text)
    expected = {
        "latestCompletedRelease": "r072e",
        "siteVersion": "1.18",
        "publicHtmlNoteCount": 155,
        "postR060RecapNodeCount": 95,
        "postR070ASealedReleaseCount": 57,
        "nextRelease": "r072f",
        "latestReleaseGate": "tests/r072e-supercritical-ledger-gate.test.mjs",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise RuntimeError(
                f"manifest final {key}: expected {value!r}, found {data.get(key)!r}"
            )


def verify_site_version_new(text: str) -> None:
    data = json.loads(text)
    expected = {
        "version": "1.18",
        "latestRelease": "R0.72E",
        "publicHtmlNoteCount": 155,
        "publishedDate": PUBLISHED_DATE,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            raise RuntimeError(
                f"site-version final {key}: expected {value!r}, "
                f"found {data.get(key)!r}"
            )


def main() -> None:
    home_path = PUBLIC / "research-review.html"
    literature_path = PUBLIC / "literature-review.html"
    manifest_path = ROOT / "research" / "release-manifest.json"
    site_version_path = PUBLIC / "site-version.json"
    note_path = PUBLIC / "notes" / "r0-72e.html"
    recap_path = PUBLIC / "recap-r0-61-r0-72e.html"

    # Read and classify every mutable source before writing anything.
    home_before = home_path.read_text(encoding="utf-8")
    literature_before = literature_path.read_text(encoding="utf-8")
    manifest_before = manifest_path.read_text(encoding="utf-8")
    site_version_before = site_version_path.read_text(encoding="utf-8")

    home_state = classify_text_state(
        home_before,
        'data-site-version="1.17"',
        'data-site-version="1.18"',
        "home preflight",
    )
    literature_state = classify_text_state(
        literature_before,
        '/i18n-en.js?v=1.17',
        '/i18n-en.js?v=1.18',
        "literature preflight",
    )
    manifest_state = classify_text_state(
        manifest_before,
        '"latestCompletedRelease": "r072d"',
        '"latestCompletedRelease": "r072e"',
        "manifest preflight",
    )
    site_version_state = classify_text_state(
        site_version_before,
        '"latestRelease": "R0.72D"',
        '"latestRelease": "R0.72E"',
        "site-version preflight",
    )

    note_count_before = len(list((PUBLIC / "notes").glob("*.html")))
    if note_path.exists():
        if note_count_before != 155:
            raise RuntimeError(
                "note preflight: R0.72E exists but total HTML note count is "
                f"{note_count_before}, expected 155"
            )
        if note_path.read_text(encoding="utf-8") != NOTE_HTML:
            raise RuntimeError("note preflight: existing R0.72E HTML drifted")
    elif note_count_before != 154:
        raise RuntimeError(
            "note preflight: R0.72E absent but total HTML note count is "
            f"{note_count_before}, expected 154"
        )

    recap_new = build_recap()
    if recap_path.exists() and recap_path.read_text(encoding="utf-8") != recap_new:
        raise RuntimeError("recap preflight: existing R0.72E recap drifted")

    # Compute and fully validate all outputs in memory before the first write.
    home_new = update_home(home_before) if home_state == "old" else home_before
    literature_new = (
        update_literature(literature_before)
        if literature_state == "old"
        else literature_before
    )
    manifest_new = (
        update_release_manifest(manifest_before)
        if manifest_state == "old"
        else manifest_before
    )
    site_version_new = (
        update_site_version(site_version_before)
        if site_version_state == "old"
        else site_version_before
    )
    verify_home_new(home_new)
    verify_literature_new(literature_new)
    verify_manifest_new(manifest_new)
    verify_site_version_new(site_version_new)
    require_once(recap_new, "收录节点：95", "recap final nodes")
    require_once(recap_new, "R0.72F 寻找最小", "recap final next")

    changed: list[str] = []
    if write_deterministic(note_path, NOTE_HTML, "R0.72E note"):
        changed.append(str(note_path.relative_to(ROOT)))
    if write_deterministic(recap_path, recap_new, "R0.72E recap"):
        changed.append(str(recap_path.relative_to(ROOT)))
    if write_if_changed(home_path, home_before, home_new):
        changed.append(str(home_path.relative_to(ROOT)))
    if write_if_changed(literature_path, literature_before, literature_new):
        changed.append(str(literature_path.relative_to(ROOT)))
    if write_if_changed(manifest_path, manifest_before, manifest_new):
        changed.append(str(manifest_path.relative_to(ROOT)))
    if write_if_changed(site_version_path, site_version_before, site_version_new):
        changed.append(str(site_version_path.relative_to(ROOT)))

    # Re-read the disk state: a second run must make no changes.
    final_note_count = len(list((PUBLIC / "notes").glob("*.html")))
    if final_note_count != 155:
        raise RuntimeError(
            f"postflight note count: expected 155, found {final_note_count}"
        )
    if note_path.read_text(encoding="utf-8") != NOTE_HTML:
        raise RuntimeError("postflight note content mismatch")
    if recap_path.read_text(encoding="utf-8") != recap_new:
        raise RuntimeError("postflight recap content mismatch")
    verify_home_new(home_path.read_text(encoding="utf-8"))
    verify_literature_new(literature_path.read_text(encoding="utf-8"))
    verify_manifest_new(manifest_path.read_text(encoding="utf-8"))
    verify_site_version_new(site_version_path.read_text(encoding="utf-8"))

    print(
        json.dumps(
            {
                "release": "R0.72E",
                "siteVersion": NEW_VERSION,
                "changed": changed,
                "idempotent": True,
                "pdfGenerated": False,
                "translationGenerated": False,
                "testsRun": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
