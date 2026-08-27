#!/usr/bin/env python3
"""Generate the deterministic R0.72M GitHub Pages release from site v1.25."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


ROOT = Path(os.environ.get("R072M_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
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
    for phrase in ("我们", "攻关", "主攻", "研究纪律", "杀死错误想法", "突破"):
        if phrase in text:
            raise RuntimeError(f"{label}: discouraged public phrase {phrase}")


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72M · EXACT DANGER WINDOW · FULL-LATTICE PHASE MIXING</div>
        <h1>危险项只在中间 action 窗口出现；<br>完整一载波参考链落在窗口下方</h1>
        <p class="lead">我先把 R0.72L 的 scalar cubic remainder 写成精确超水平区间，再在完整无限 Fourier 格点上求解一载波零扩散参考链。Bessel 解给出 \(\sigma^2\) 涡量尺度、\(\sigma^{4/3}\log\sigma\) lifted action 和 \((16/\pi^2)a^2\log\sigma\) 的 true-cubic 主项。这个参考链属于 action-poor 分支；耗散链的同类统一估计仍未证明。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72M 定理完成</span><strong>exact scalar window and frozen full-lattice screen</strong><p>版本 v0.72M · 2026-08-27</p><p>exact scalar superlevel theorem: CLOSED</p><p>full-lattice Bessel benchmark: CLOSED</p><p>frozen cubic coefficient: CLOSED</p><p>dissipative uniform theorem: OPEN</p><p>一般三维正则性：OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>R0.72L 的坏项不是随 action 单调变坏</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · EXACT WINDOW</strong><p>令 \(T(x)=\min\{U,Vx\}/(K+x)\)、\(H=U/V\)。当 \(A&lt;U/(K+H)\) 时，\(T(x)&gt;A\) 恰好等价于 \(\frac{AK}{V-A}&lt;x&lt;\frac UA-K\)；否则超水平集为空。</p></div>
            <div class="verdict-card true"><strong>THEOREM · FULL LATTICE</strong><p>零扩散参考链保留完整无限格点和 \(e^{-y}\) coupling envelope。对声明的反对称 launch，精确解为 \(f_n(s)=\sqrt2J_n'(2s)\)。</p></div>
            <div class="verdict-card true"><strong>THEOREM · ACTION-POOR PLACEMENT</strong><p>固定一载波几何下，\(x/H\asymp\sigma^{-2/3}\log\sigma\) 且 \(Vx/K\asymp\sigma^{-1/3}\log\sigma\)，所以该参考链位于危险窗口下方。</p></div>
            <div class="verdict-card false"><strong>OPEN · DISSIPATIVE CHAIN</strong><p>删除 \(-n^2f_n\) 是基准操作，不是耗散方程的精确约化。有限数值曲线不替代统一解析估计。</p></div>
          </div>
        </section>

        <section id="window"><div class="section-no">01 / Scalar theorem</div><h2>完整超水平集可以逐端点写出</h2>
          <div class="equation result">\[
            T(x)=\frac{\min\{U,Vx\}}{K+x},\qquad H=\frac UV,
          \]</div>
          <div class="equation result">\[
            \boxed{\{x\ge0:T(x)>A\}=
            \left(\frac{AK}{V-A},\,\frac UA-K\right)}
          \]</div>
          <p>上式要求 \(0&lt;A&lt;U/(K+H)\)。有 inherited floor \(x\ge Z\) 时，只需与 \([Z,\infty)\) 相交。\(T\) 在 \(H\) 左侧上升、右侧下降。因此 action 太少和 denominator 足够大都是安全分支，只有中间区间可能使这个 scalar term 变大。</p>
        </section>

        <section id="bessel"><div class="section-no">02 / Complete lattice</div><h2>参考模型使用完整无限格点，不使用三模闭包</h2>
          <p>取与目标频率正交的一载波，写 \(\mu=q_*^2/R^2&gt;0\)。删去 relative diagonal heat 后，保留完整 coupling chain</p>
          <div class="equation result">\[
            \partial_yf_n=\sigma e^{-y}(f_{n-1}-f_{n+1}),\qquad
            s=\sigma(1-e^{-y}).
          \]</div>
          <p>对 \(f_1(0)=2^{-1/2}\)、\(f_{-1}(0)=-2^{-1/2}\)，生成函数或 Bessel 传播子给出</p>
          <div class="equation result">\[
            \boxed{f_n(s)=\sqrt2J_n'(2s)},\qquad
            \boxed{\sum_n n^2|f_n(s)|^2=1+s^2}.
          \]</div>
          <p>第二个恒等式把固定几何下的参考 enstrophy contrast 定位为 \(K_{\rm fr}\asymp\sigma^2\)。</p>
        </section>

        <section id="action"><div class="section-no">03 / Complete action</div><h2>negative-norm action 必须包含全格点，不等于一个目标行</h2>
          <p>令 \(Bf=(f_{n-1}-f_{n+1})_n\)，并定义</p>
          <div class="equation result">\[
            q(s)=\sum_{n\in\mathbb Z}\frac{|(Bf(s))_n|^2}{\mu+n^2}.
          \]</div>
          <p>驻相、Airy 转折区和尾部估计给 \(q(s)\lesssim(1+s)^{-1}\)。因此</p>
          <div class="equation result">\[
            A_\sigma\sim A_0\sigma^{-2/3}\log\sigma,\qquad
            A_0=\int_0^\infty s^{-1/3}q(s)\,ds\in(0,\infty).
          \]</div>
          <p>乘回 inherited \(\Theta\asymp\sigma^2\) 后，\(x_{\rm fr}\asymp\sigma^{4/3}\log\sigma\)。单独的 target row 只给同指数的正信号，不能替代 \(q(s)\) 或它的常数。</p>
        </section>

        <section id="cubic"><div class="section-no">04 / True cubic</div><h2>绝对 cubic variation 只有对数增长</h2>
          <p>写 \(u(s)=f_1(s)=\sqrt2J_1'(2s)\)。恢复 carrier envelope 和 target heat 后，reference true-cubic mass 恰为</p>
          <div class="equation result">\[
            \mathcal C_{\rm fr}(\sigma)=4a^2
            \int_0^{\sigma(1-e^{-1})}
            \left(1-\frac{s}{\sigma}\right)^{2+2\mu}|u(s)u'(s)|\,ds.
          \]</div>
          <p>Bessel 导数的大参数展开及振荡绝对值平均给出尖锐主项</p>
          <div class="equation result">\[
            \boxed{\mathcal C_{\rm fr}(\sigma)
            =\frac{16}{\pi^2}a^2\log\sigma+O(a^2)},\qquad
            \frac{\mathcal C_{\rm fr}}{\sigma a^2}\to0.
          \]</div>
        </section>

        <section id="placement"><div class="section-no">05 / Branch placement</div><h2>这个参考族已由原始 \(Vx\) 分支支付</h2>
          <p>在 \(p=1\)、固定 \(R=R_0\) 的账本中，\(U\asymp\sigma^{7/3}\)、\(V\asymp\sigma^{1/3}\)、\(H\asymp\sigma^2\)。于是</p>
          <div class="equation result">\[
            \frac{x_{\rm fr}}H\asymp\sigma^{-2/3}\log\sigma\to0,\qquad
            \frac{Vx_{\rm fr}}{K_{\rm fr}}\asymp
            \sigma^{-1/3}\log\sigma\to0.
          \]</div>
          <p>因此 R0.72L 对所有 \(x\ge Z\) 的优化在这个 family 上不尖锐。这个结论只定位一个精确参考族，不说明所有 extreme-coupling 解都 action-poor。</p>
        </section>

        <section id="audit"><div class="section-no">06 / Independent audit</div><h2>解析式和有限诊断走两套独立数值路线</h2>
          <div class="audit-grid">
            <div class="audit-card"><strong>PRODUCER · PASS</strong><p>producer 使用 differentiated Bessel functions、Gauss quadrature 和 Fourier phase splitting，核对 exact window、Bessel moment、action scaling、frozen cubic 以及 dissipative finite diagnostic。</p><p class="mini-kpi">deterministic · binary64 · finite corroboration</p></div>
            <div class="audit-card"><strong>INDEPENDENT · PASS</strong><p>independent route 改用 Bessel recurrence、angular FFT Parseval、独立求积和 finite-chain Cayley split。crosscheck 对同名量分别设置精度门限。</p><p class="mini-kpi"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_independent_audit.md">独立逐式审计</a></p></div>
          </div>
          <p>耗散曲线只表明两种有限离散在声明网格上相互一致。它没有证明 \(\mathcal C_{\rm diss}=O(\log\sigma)\)。</p>
        </section>

        <section id="figure"><div class="section-no">07 / Journal figure</div><h2>附图把解析定理、参考渐近和有限耗散诊断分开</h2>
          <p><img src="/assets/r072m/fig-r072m-danger-window.svg" alt="R0.72M exact danger window and full-lattice phase-mixing formal figure"></p>
          <p><a href="/assets/r072m/fig-r072m-danger-window.pdf">下载 PDF</a> · <a href="/assets/r072m/fig-r072m-danger-window.png">下载 PNG</a> · <a href="/assets/r072m/fig-r072m-danger-window.svg">打开 SVG</a></p>
        </section>

        <section id="literature"><div class="section-no">08 / Literature boundary</div><h2>triad 几何、enhanced dissipation 和这里的 cubic action 不是同一结论</h2>
          <p><a href="https://doi.org/10.1063/1.858309">Waleffe</a> 说明三波传递依赖几何与极化；<a href="https://doi.org/10.1017/jfm.2013.637">Moffatt</a> 说明截断 triad 与精确演化可以不同。这里的 Bessel wave 占据完整格点。</p>
          <p><a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1112/jlms.12782">Coti Zelati–Gallay</a> 给出 shear enhanced-dissipation semigroup 结果，但不直接控制本节带绝对值的 project-specific cubic variation。本站结论只按当前报告与证书陈述，不据限定检索主张优先权。</p>
        </section>

        <section id="value"><div class="section-no">09 / Research value</div><h2>价值在于把“action 够不够大”改成一个可判定区间</h2>
          <p>R0.72M 修正了上一节对 \(x\) 全区间优化造成的损失，并给出一个完整无限格点上的尖锐基准。它说明至少有一种真实 phase-mixing geometry 不会触发 scalar danger window，且 raw \(O(\sigma)\) cubic bound 在该参考模型上损失很大。</p>
          <p>这仍没有建立一般 dissipative theorem，也没有导出 \(L_t^\infty L_x^3\) 或其他一般三维 continuation criterion。它对 Clay 问题的价值目前是筛选机制和缩小下一证明目标，而不是解决原问题。</p>
        </section>

        <section id="next"><div class="section-no">10 / Next gate</div><h2>R0.72N：回到带 \(-n^2f_n\) 的耗散链</h2>
          <p>下一节并行检查两个可证目标：直接证明 \(\mathcal C_{\rm diss}(\sigma)\lesssim a^2[1+\log(1+\sigma)]\)，或证明 \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\)。前者绕开 scalar window，后者把 action 放在窗口下方。</p>
        </section>

        <section id="claims"><div class="section-no">11 / Claim boundary</div><h2>一般 Navier–Stokes 问题仍然开放</h2>
          <p>本节没有把零扩散参考链当成耗散 PDE，没有从有限诊断外推连续统渐近，也没有完成任意强耦合、多载波、多尺度物理吸收、有限时奇性或全局光滑性证明。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="reproduce"><div class="section-no">12 / Reproduction</div><h2>报告、双路证书、正式附图和累计回顾</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_independent_audit.md">独立审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072m">双路机器证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072m-danger-window/fig-r072m-danger-window">正式附图包</a> · <a href="/notes/r0-72m.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72m.html">累计回顾</a> · <a href="/recap-r0-61-r0-72m.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72N</span><span class="tree-state current">下一检查点</span></div>
              <h3>dissipative one-carrier cubic/action theorem</h3>
              <p>回到带 \(-n^2f_n\) 的完整耗散链，证明 logarithmic true-cubic bound，或证明 action-poor inequality \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\)。</p>
            </article>'''


HOME_RECAP = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72M · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 103 个节点；全站现有 163 篇公开研究笔记</h3>
            <p>累计回顾保持二十八个问题阶段，完整覆盖 R0.61–R0.72M。R0.72M 把 extreme strong scalar remainder 改写成精确 action danger window，并用完整一载波 Bessel reference 证明 action-poor placement 与 sharp logarithmic cubic law。R0.70A–R0.72M 共 65 个版本已公开；41 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;零扩散参考链位于危险窗口下方；耗散一载波链的统一 cubic/action theorem 与 multiscale physical absorption 仍开放。</p>
            <p><a href="/recap-r0-61-r0-72m.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72m.pdf">下载同步 PDF</a></p>
          </div>'''


HOME_M_CARD = r'''          <div class="task-one" id="r072m" data-release="r072m" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72M · 2026-08-27</p>
            <h3>scalar cubic 只在中间 action 窗口危险；完整一载波参考链落在窗口下方</h3>
            <p>我精确求出 \(T(x)=\min\{U,Vx\}/(K+x)\) 的全部超水平集，并在完整无限 Fourier lattice 上得到 \(f_n(s)=\sqrt2J_n'(2s)\)。参考链的 gradient moment 为 \(1+s^2\)，lifted action 为 \(\sigma^{4/3}\log\sigma\) 量级。</p>
            <p>reference true-cubic mass 满足 \(\mathcal C_{\rm fr}=(16/\pi^2)a^2\log\sigma+O(a^2)\)，且 \(Vx_{\rm fr}/K_{\rm fr}\to0\)。两套有限审计一致；dissipative curves 只作诊断。</p>
            <p><strong>结论边界：</strong>&nbsp;零扩散 reference 不是 dissipative PDE；一般三维正则性仍开放。</p>
            <p><a href="/notes/r0-72m.html"><strong>阅读 R0.72M 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72m.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072m/fig-r072m-danger-window.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072m">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072m_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072m-danger-window/fig-r072m-danger-window">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72m.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72m.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72N：</strong>&nbsp;证明耗散一载波链的 logarithmic cubic bound 或 action-poor inequality。</p>
          </div>'''


def build_note() -> None:
    html = (PUBLIC / "notes" / "r0-72l.html").read_text(encoding="utf-8")
    replacements = [
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72M：求出 scalar cubic 的精确 action danger window，并在完整一载波格点上证明 Bessel action 与 logarithmic true-cubic benchmark。">', "description"),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72M｜精确 action danger window">', "og title"),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="完整 Fourier 格点的 Bessel benchmark、action-poor placement 与耗散链开放边界。">', "og description"),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072m/fig-r072m-danger-window.png">', "og image"),
        (r'<title>.*?</title>', '<title>R0.72M｜精确 action danger window</title>', "title"),
    ]
    for pattern, value, label in replacements:
        html = section(html, pattern, value, f"note {label}")
    html = required(html, "/i18n-en.js?v=1.25", "/i18n-en.js?v=1.26", "note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#window">危险窗</a><a href="#bessel">完整格点</a><a href="#action">作用量</a><a href="#cubic">cubic</a><a href="#placement">分支定位</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#literature">文献边界</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#window">01 · 精确危险窗</a></li><li><a href="#bessel">02 · 完整格点</a></li><li><a href="#action">03 · 完整作用量</a></li><li><a href="#cubic">04 · true cubic</a></li><li><a href="#placement">05 · 分支定位</a></li><li><a href="#audit">06 · 双路审计</a></li><li><a href="#figure">07 · 正式附图</a></li><li><a href="#literature">08 · 文献边界</a></li><li><a href="#value">09 · 研究价值</a></li><li><a href="#next">10 · R0.72N</a></li><li><a href="#claims">11 · 主张边界</a></li><li><a href="#reproduce">12 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72M · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>', "note footer")
    assert_clean(html, "R0.72M note")
    (PUBLIC / "notes" / "r0-72m.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72l.html").read_text(encoding="utf-8")
    changes = [
        ("/i18n-en.js?v=1.25", "/i18n-en.js?v=1.26"),
        ("R0.61–R0.72L", "R0.61–R0.72M"),
        ("R0.61 到 R0.72L 的 102 个研究节点", "R0.61 到 R0.72M 的 103 个研究节点"),
        ("收录节点：102", "收录节点：103"),
        ("回顾截止时公开笔记：162", "回顾截止时公开笔记：163"),
        ("回顾截止节点：R0.72L", "回顾截止节点：R0.72M"),
        ("02 · 102 节完整索引", "02 · 103 节完整索引"),
        ("<strong>102</strong><span>R0.61–R0.72M 研究节点</span>", "<strong>103</strong><span>R0.61–R0.72M 研究节点</span>"),
        ("<strong>64</strong><span>R0.70A–R0.72L 已公开版本</span>", "<strong>65</strong><span>R0.70A–R0.72M 已公开版本</span>"),
        ("<strong>40</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>41</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("后面的 102 个节点", "后面的 103 个节点"),
        ("R0.70A–R0.72L 的 64 个版本已经公开；其中 40 个", "R0.70A–R0.72M 的 65 个版本已经公开；其中 41 个"),
        ("R0.61–R0.72M 的 102 节公开笔记", "R0.61–R0.72M 的 103 节公开笔记"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"recap {old}")
    html = section(html, r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72M 的 103 个研究节点；最新一节给出精确 action danger window 与完整一载波 phase-mixing benchmark。">', "recap description")
    html = section(html, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十八个阶段、103 个节点：从约化递推和时间迹账本，到 critical-log candidate、strong-coupling window 和完整一载波参考链。">', "recap og description")
    html = section(html, r'<title>.*?</title>', '<title>R0.61–R0.72M｜R0.60 之后的研究回顾</title>', "recap title")
    html = required(html, "/recap-r0-61-r0-72l.pdf", "/recap-r0-61-r0-72m.pdf", "recap self PDF")

    old_phase = r'''            <article class="phase"><h3>R0.72L · 中强耦合闭合与极强耦合余项</h3>
              <p>我把 actual enstrophy contrast \(K\) 与 actual action \(x\) 留在 complete-root denominator 中，得到对所有 \(\varepsilon=gB/R^2&gt;0\) 有效的 full-lattice upper bound。对带固定背景、phase-aligned、row-aligned、exact-corrected 的构造族，局部精确根再给出 \(x\ge Z\)。</p>
              <p>这把 closure 推进到 \(1\lesssim\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\)。上沿只给 \(O(1)\)，little-o 子区间才趋零。三模 Galerkin 的线性增长不能嵌入完整格点；extreme strong coupling 仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/assets/r072l/fig-r072l-strong-window.pdf">R0.72L 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072l">R0.72L 证书</a></div></article>'''
    new_phase = r'''            <article class="phase"><h3>R0.72L–R0.72M · 中强耦合窗口与精确 action screen</h3>
              <p>R0.72L 把 actual enstrophy contrast \(K\) 与 actual action \(x\) 留在 complete-root denominator 中，将 closure 推进到随 \(R\) 增长的 moderate strong-coupling window。R0.72M 随后精确求出 scalar cubic 的全部超水平区间。</p>
              <p>完整一载波零扩散参考链有 Bessel 解、\(K_{\rm fr}\asymp\sigma^2\)、\(x_{\rm fr}\asymp\sigma^{4/3}\log\sigma\) 和 \(\mathcal C_{\rm fr}=(16/\pi^2)a^2\log\sigma+O(a^2)\)。它位于 action-poor 分支；带 diagonal heat 的耗散链仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/assets/r072m/fig-r072m-danger-window.pdf">R0.72M 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072m">R0.72M 证书</a></div></article>'''
    html = once(html, old_phase, new_phase, "recap M phase")
    node_l = '            <span class="node-ref"><a href="/notes/r0-72l.html">R0.72L</a><span class="node-state kind-closed">闭</span></span>\n'
    node_m = '            <span class="node-ref"><a href="/notes/r0-72m.html">R0.72M</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_l, node_l + node_m, "recap M node")
    retained_m = r'''            <li>R0.72M 的 exact danger-window theorem 与 full-lattice reference：\(\min\{U,Vx\}/(K+x)\) 的超水平集是显式中间开区间；完整一载波零扩散链有 \(f_n(s)=\sqrt2J_n'(2s)\)、gradient moment \(1+s^2\)、lifted action \(\asymp\sigma^{4/3}\log\sigma\) 与 true-cubic 主项 \((16/\pi^2)a^2\log\sigma\)。该 reference 属于 action-poor 分支；dissipative theorem 仍开放。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained_m + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained M")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>scalar danger window 已精确化，耗散链仍是下一道门</h2>
          <p>截至 R0.72M，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 103 个节点或 65 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>新的严格结果是 exact scalar superlevel theorem、完整无限格点的 Bessel reference、complete action asymptotic 和 \(16/\pi^2\) sharp cubic coefficient。</p>
          <p>零扩散 reference 位于 action-poor 分支，但它不是带 \(-n^2f_n\) 的 dissipative chain。后一对象的 uniform logarithmic cubic 或 action-poor theorem 仍开放。</p>
        </section>''', "recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72N 回到 dissipative one-carrier chain</h2>
          <p>并行检查 \(\mathcal C_{\rm diss}\lesssim a^2[1+\log(1+\sigma)]\) 与 \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\)。</p>
          <p>前者直接支付 true cubic，后者证明 action 落在 danger window 下方；multiscale Schur ledger 保留为并列接口。</p>
        </section>''', "recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72M 的 65 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，41 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。</p>
          <p>R0.72M 的 analytic theorem 限于 scalar ledger 和声明的完整一载波 zero-diffusion reference。有限 dissipative diagnostics 不是 continuum theorem；Clay 正式问题仍然开放。</p>
        </section>''', "recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72l.html">保留 R0.72L 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72m.html">打开最新节点 R0.72M</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072m">查看 R0.72M 双路证书</a> · <a href="/assets/r072m/fig-r072m-danger-window.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72m.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72l.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>''', "recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72M 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>', "recap footer")
    assert_clean(html, "R0.72M recap")
    (PUBLIC / "recap-r0-61-r0-72m.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    changes = [
        ('data-site-version="1.25"', 'data-site-version="1.26"'),
        ("/i18n-en.js?v=1.25", "/i18n-en.js?v=1.26"),
        ("/site-refresh.js?v=1.25", "/site-refresh.js?v=1.26"),
        ("<strong>v1.25</strong>网页版本", "<strong>v1.26</strong>网页版本"),
        ("<strong>162</strong>公开研究笔记", "<strong>163</strong>公开研究笔记"),
        ("<strong>R0.72L</strong>最新研究节点", "<strong>R0.72M</strong>最新研究节点"),
        ("<strong>extreme strong-coupling cascade ledger</strong>当前方向", "<strong>dissipative one-carrier cubic/action theorem</strong>当前方向"),
        ("Research topology · R0.1–R0.72L", "Research topology · R0.1–R0.72M"),
        ("R0.70A–R0.72L：64 节已公开，40 节完整封存", "R0.70A–R0.72M：65 节已公开，41 节完整封存"),
        ("<span class=\"route-range\">R0.69P–R0.72L</span>", "<span class=\"route-range\">R0.69P–R0.72M</span>"),
        ('aria-label="R0.69P–R0.72L"', 'aria-label="R0.69P–R0.72M"'),
        ("展开 72 篇公开笔记", "展开 73 篇公开笔记"),
        ("综述 v1.25 · 2026-08-27", "综述 v1.26 · 2026-08-27"),
        ("上次综述 v1.24 · 2026-08-27", "上次综述 v1.25 · 2026-08-27"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"home {old}")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', r'<div class="summary-item"><strong>我目前关注</strong><span>R0.72M 已把 scalar cubic remainder 精确化为 action danger window，并在完整一载波 Bessel reference 上证明 action-poor placement 与 logarithmic true-cubic law；dissipative one-carrier theorem 仍开放。</span></div>', "home summary")
    html = once(html, "从 complete complex-root closure 走到 moderate strong-coupling window", "从 moderate strong-coupling window 走到 exact action screen", "home route title")
    old_route_end = r'''R0.72K 再对每个复根隙选择独立 norming direction，把 mixed row 与 true cubic 转成 complete complex-target ledger，并证明其 common-band 物理归一化比统一衰减。R0.72L 保留 actual \(K\) 与 \(x\)，用 local exact root/action floor 把闭合区推进到 \(\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\)。</p>'''
    new_route_end = r'''R0.72K 再对每个复根隙选择独立 norming direction，把 mixed row 与 true cubic 转成 complete complex-target ledger，并证明其 common-band 物理归一化比统一衰减。R0.72L 保留 actual \(K\) 与 \(x\)，用 local exact root/action floor 把闭合区推进到 \(\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\)。R0.72M 精确求出 scalar danger window，并在完整一载波 Bessel reference 上证明 action-poor placement 与 \((16/\pi^2)a^2\log\sigma\) cubic law。</p>'''
    html = once(html, old_route_end, new_route_end, "home route M prose")
    html = once(html, "→ moderate strong-coupling window → extreme remainder</p>", "→ moderate strong-coupling window → exact action danger window → dissipative one-carrier gate</p>", "home path M")
    nav_l = '                  <a class="milestone" href="/notes/r0-72l.html">R0.72L</a>\n'
    html = once(html, nav_l, nav_l + '                  <a class="milestone" href="/notes/r0-72m.html">R0.72M</a>\n', "home M route link")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "home next")
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', HOME_RECAP, "home recap")
    old_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72M：</strong>&nbsp;量化 extreme strong coupling 的 full-lattice cascade/enstrophy/action alternative。</p>
          </div>
        </section>'''
    new_tail = r'''            <p><strong style="color:var(--gold)">R0.72M 已完成：</strong>&nbsp;scalar danger window 与 full-lattice zero-diffusion reference 已闭合；dissipative one-carrier theorem 转入 R0.72N。</p>
          </div>

''' + HOME_M_CARD + r'''
        </section>'''
    html = once(html, old_tail, new_tail, "home M card")
    html = required(html, "/recap-r0-61-r0-72l.html", "/recap-r0-61-r0-72m.html", "home recap HTML endpoint")
    html = required(html, "/recap-r0-61-r0-72l.pdf", "/recap-r0-61-r0-72m.pdf", "home recap PDF endpoint")
    assert_clean(html, "R0.72M home")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    changes = [
        ("/i18n-en.js?v=1.25", "/i18n-en.js?v=1.26"),
        ("文献综述 v1.25 · 2026-08-27", "文献综述 v1.26 · 2026-08-27"),
        ("本站 R0.69P–R0.72L 只列为研究笔记", "本站 R0.69P–R0.72M 只列为研究笔记"),
        ("累计回顾与 102 节索引", "累计回顾与 103 节索引"),
        ("打开 102 节完整索引", "打开 103 节完整索引"),
        ("/recap-r0-61-r0-72l.html", "/recap-r0-61-r0-72m.html"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"literature {old}")
    html = once(html, "R0.72L 保留实际 enstrophy contrast 与 critical-log action，闭合随 \\(R\\) 增长的 moderate strong-coupling window；窗口上沿只给 \\(O(1)\\)，little-o 子区间才衰减。一般 Navier–Stokes 正则性仍开放。</p>", "R0.72L 保留实际 enstrophy contrast 与 critical-log action，闭合随 \\(R\\) 增长的 moderate strong-coupling window；窗口上沿只给 \\(O(1)\\)，little-o 子区间才衰减。R0.72M 精确求出 scalar action danger window，并在完整一载波 zero-diffusion chain 上证明 Bessel action-poor benchmark 与 sharp logarithmic cubic law。一般 Navier–Stokes 正则性仍开放。</p>", "literature M route")
    old_open = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72M</b><strong>extreme strong-coupling cascade ledger</strong></header><p>量化 full-lattice enstrophy、all-time action 或 improved cubic mixing，支付 \(\varepsilon^{7/3}p^{4/3}\) 余项；multiscale Schur ledger 保留为并列接口。</p></div>'''
    new_open = r'''              <div class="route-step closed"><header><b>R0.72M</b><strong>exact action danger window and full-lattice reference</strong></header><p>scalar cubic 的超水平集是显式中间开区间；完整一载波 zero-diffusion reference 有 Bessel 解、action-poor placement 与 \((16/\pi^2)a^2\log\sigma\) true-cubic law。<a href="/notes/r0-72m.html">研究笔记</a> <a href="/recap-r0-61-r0-72m.html">当前累计回顾</a> <a href="#r072m-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72N</b><strong>dissipative one-carrier cubic/action theorem</strong></header><p>证明 \(\mathcal C_{\rm diss}=O(a^2\log(1+\sigma))\)，或证明 \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\)。</p></div>'''
    html = once(html, old_open, new_open, "literature M cards")
    l_boundary = r'''          <div class="boundary"><strong>R0.72L 的主张边界</strong><p>限定检索没有找到项目公式或 \(p^{2/3}R^{2/3}(1+\log R)\) 窗口的直接前例，但这不构成新颖性或优先权证明。local floor 只属于带固定背景、phase-aligned、row-aligned、exact-corrected 的构造族；窗口上沿只给 \(O(1)\)，little-o 子区间才衰减；Galerkin 结果不是 full Fourier lattice 结论。</p></div>'''
    m_boundary = r'''

          <h3 id="r072m-boundary">R0.72M 的 full-lattice reference 与 enhanced-dissipation 边界</h3>
          <p><a href="https://doi.org/10.1063/1.858309">Waleffe</a> 的 triad analysis 说明 transfer 依赖精确 geometry 与 polarization；<a href="https://doi.org/10.1017/jfm.2013.637">Moffatt</a> 说明 truncated triad 与 exact evolution 可以不同。R0.72M 因此保留完整无限 convolution lattice，不把三模轨道当作 PDE 子系统。</p>
          <p><a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1112/jlms.12782">Coti Zelati–Gallay</a> 建立 shear enhanced-dissipation semigroup estimates，但这些结果不直接给本节带绝对值的 project-specific cubic variation。Bessel recurrence、fixed-order 渐近与 turning-region 统一 Airy 控制分别使用 <a href="https://dlmf.nist.gov/10.6">DLMF §10.6</a>、<a href="https://dlmf.nist.gov/10.17">§10.17</a>、<a href="https://dlmf.nist.gov/10.19.iii">§10.19(iii)</a> 和 <a href="https://dlmf.nist.gov/10.20.i">§10.20(i)</a>。</p>
          <div class="boundary"><strong>R0.72M 的主张边界</strong><p>解析定理覆盖 scalar superlevel set 与声明的一载波 zero-diffusion reference。删除 relative diagonal heat 不是 dissipative PDE reduction；两套 finite dissipative curves 只作 convergence diagnostic。限定检索不构成新颖性或优先权证明。</p></div>'''
    html = once(html, l_boundary, l_boundary + m_boundary, "literature M boundary")
    assert_clean(html, "R0.72M literature")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    note_count = len(list((PUBLIC / "notes").glob("*.html")))
    if note_count != 163:
        raise RuntimeError(f"expected 163 public HTML notes, found {note_count}")
    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({
        "latestCompletedRelease": "r072m", "siteVersion": "1.26",
        "publicHtmlNoteCount": note_count, "postR060RecapNodeCount": 103,
        "nextRelease": "r072n", "latestReleaseGate": "tests/r072m-danger-window-gate.test.mjs",
        "postR070APublishedReleaseCount": 65, "postR070AFormalSealedReleaseCount": 41,
        "legacyFormalFigureBacklogCount": 24,
    })
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.26", "latestRelease": "R0.72M", "publicHtmlNoteCount": note_count, "publishedDate": "2026-08-27"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update({"latestPublishedRelease": "r072m", "publishedReleaseCount": 65, "formalSealedReleaseCount": 41, "legacyFormalFigureBacklogCount": 24})
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072m" not in inventory[key]:
            inventory[key].append("r072m")
    if len(inventory["legacyFormalFigureBacklog"]) != 24:
        raise RuntimeError("legacy formal-figure backlog changed unexpectedly")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-72m.html", "recap-r0-61-r0-72m.html"):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({
        "release": "R0.72M", "siteVersion": "1.26", "notes": 163,
        "recapNodes": 103, "published": 65, "formalSealed": 41,
        "legacyBacklog": 24, "phases": 28, "next": "R0.72N",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
