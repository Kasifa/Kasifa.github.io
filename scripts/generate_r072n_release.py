#!/usr/bin/env python3
"""Generate the deterministic R0.72N GitHub Pages release from site v1.26."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


ROOT = Path(os.environ.get("R072N_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
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
        <div class="eyebrow">研究笔记 R0.72N · DISSIPATIVE CHAIN · ENHANCED DISSIPATION</div>
        <h1>action-poor 路线在耗散链上失效；<br>true cubic 仍保持次线性</h1>
        <p class="lead">我回到带 diagonal heat 的完整一载波链。能量与二阶矩账本给 \(K_\sigma\lesssim1+\sigma^{2/3}\)，首耦合层却给 \(x_\sigma\gtrsim\sigma^{4/3}\log\sigma\)，所以声明 launch 上的 action-poor 条件不成立。把生成函数映到 Coble–He 的时变剪切方程后，我再由其 \(L^2\) 衰减推出本站推论 \(\mathcal C_{\rm diss}=O(a^2\sqrt\sigma)\)。对数 sharpen、多载波和一般三维问题仍开放。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72N 定理完成</span><strong>dissipative action no-go and sublinear cubic</strong><p>版本 v0.72N · 2026-08-27</p><p>action-poor route: DISPROVED FOR THIS LAUNCH</p><p>moment barrier: CLOSED</p><p>one-carrier sublinear cubic: CLOSED</p><p>logarithmic sharpen: OPEN</p><p>multi-carrier extension: OPEN</p><p>一般三维正则性：OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>同一个耗散 launch 给出一项否定和一项正面结论</h2>
          <div class="verdict-grid">
            <div class="verdict-card false"><strong>THEOREM · ACTION-POOR NO-GO</strong><p>对声明的 row-aligned launch，\(\sigma^{1/3}x_\sigma/K_\sigma\gtrsim\sigma\log\sigma\to\infty\)。R0.72M 提出的 action-poor 充分路线在这个耗散族上不成立。</p></div>
            <div class="verdict-card true"><strong>THEOREM · MOMENT BARRIER</strong><p>完整无限链满足 \(E'=-2D\) 与 \(D'\le-2D^2+4\sigma\sqrt D\)，从而 \(\sup D\le\max\{1,(2\sigma)^{2/3}\}\)。</p></div>
            <div class="verdict-card true"><strong>COROLLARY · SUBLINEAR CUBIC</strong><p>Coble–He 的时变剪切半群定理应用于重标度生成函数；坐标投影与时间积分再给本站推论 \(\mathcal C_{\rm diss}\lesssim a^2\sigma^{1/2}=o(\sigma a^2)\)。</p></div>
            <div class="verdict-card false"><strong>OPEN · SHARP RATE AND SUPERPOSITION</strong><p>有限曲线与 \(O(a^2\log\sigma)\) 相容，但没有证明该 sharpen。多载波交叉项和 multiscale physical absorption 也未闭合。</p></div>
          </div>
        </section>

        <section id="chain"><div class="section-no">01 / Dissipative chain</div><h2>证明对象保留完整格点和 diagonal heat</h2>
          <p>在 \(0\le y\le1\) 上取</p>
          <div class="equation result">\[
            \partial_y f_n^\sigma=-n^2f_n^\sigma+\sigma e^{-y}
            (f_{n-1}^\sigma-f_{n+1}^\sigma),
          \]</div>
          <p>并固定 \(f_1^\sigma(0)=2^{-1/2}\)、\(f_{-1}^\sigma(0)=-2^{-1/2}\)，其余行初值为零。这里没有删除 \(-n^2f_n\)，也没有把无限链换成有限 Galerkin 轨道。</p>
        </section>

        <section id="moment"><div class="section-no">02 / Energy and moment</div><h2>skew coupling 不改变能量，但会抬高二阶矩</h2>
          <p>令 \(E=\sum_n|f_n|^2\)、\(D=\sum_n n^2|f_n|^2\)、\(P=\sum_n n^4|f_n|^2\)。Galerkin 恒等式经抛物光滑极限给出</p>
          <div class="equation result">\[
            E'=-2D,\qquad D'\le-2D^2+4\sigma\sqrt D,
            \qquad D\le\max\{1,(2\sigma)^{2/3}\}.
          \]</div>
          <p>加入 R0.72L 的固定解耦背景后，实际 enstrophy contrast 满足 \(K_\sigma\lesssim1+\sigma^{2/3}\)。这是上界，不是匹配渐近。</p>
        </section>

        <section id="action"><div class="section-no">03 / Critical-log action</div><h2>首耦合层已经排除 action-poor 条件</h2>
          <p>对 R0.72F 的 critical-log weight，短时间 Duhamel 极限和全局能量界分别给</p>
          <div class="equation result">\[
            c\sigma^{-2/3}\log\sigma\le\mathscr A_\sigma\le C,
            \qquad c\sigma^{4/3}\log\sigma\le x_\sigma\le C\sigma^2.
          \]</div>
          <p>因此</p>
          <div class="equation result">\[
            \boxed{\frac{\sigma^{1/3}x_\sigma}{K_\sigma}
            \gtrsim\sigma\log\sigma\longrightarrow\infty.}
          \]</div>
          <p>这个 no-go 只覆盖声明的固定频带、row-aligned、one-carrier launch；它不是所有耗散数据的分类。</p>
        </section>

        <section id="screen"><div class="section-no">04 / Scalar screen</div><h2>实际 action 落入 R0.72M 的危险窗</h2>
          <p>代入 \(U_\sigma\asymp\sigma^{7/3}\)、\(V_\sigma\asymp\sigma^{1/3}\) 后，两个 reciprocal branches 给出</p>
          <div class="equation result">\[
            \boxed{T_\sigma=
            \frac{\min\{U_\sigma,V_\sigma x_\sigma\}}
            {K_\sigma+x_\sigma}\asymp\sigma^{1/3}.}
          \]</div>
          <p>所以 action denominator 不能关闭这个 launch。否定一条付款路线，不等于否定原始不等式或构造奇性。</p>
        </section>

        <section id="mapping"><div class="section-no">05 / Shear mapping</div><h2>时间重标度把链变成时变剪切的一个 Fourier mode</h2>
          <p>令 \(\nu=\sigma^{-1}\)、\(t=\sigma y\)，并以 \(F(t,\theta)=\sum_n f_n^\sigma(\nu t)e^{in\theta}\) 生成函数编码全链，则</p>
          <div class="equation result">\[
            \partial_tF=\nu\partial_\theta^2F
            +2ie^{-\nu t}\sin\theta\,F.
          \]</div>
          <p>它对应 Coble–He 方程的 \(k=-2\)、horizontal diffusion switch \(=0\) 和 \(V(t,\theta)=e^{-\nu t}\sin\theta\)。在 \(0\le t\le\nu^{-1}\) 上，临界点固定、振幅在 \([e^{-1},1]\) 内，Theorem 1.2 的非退化常数可统一选择。</p>
        </section>

        <section id="cubic"><div class="section-no">06 / Project corollary</div><h2>published semigroup estimate 与本站 cubic 推论必须分开署名</h2>
          <p><a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He, Theorem 1.2</a> 给出声明时段内的半群衰减</p>
          <div class="equation result">\[
            \|F(t)\|_2\le Ce^{-c\nu^{1/2}t}\|F(0)\|_2.
          \]</div>
          <p>再用 \(|f_1(f_0-f_2)|\le\sqrt2\sum_n|f_n|^2\) 投影并积分，得到</p>
          <div class="equation result">\[
            \boxed{\mathcal C_{\rm diss}\lesssim
            a^2\nu^{-1/2}=a^2\sigma^{1/2}=o(\sigma a^2).}
          \]</div>
          <p>最后一式是我在本站完成的 corollary，不是 Coble–He 原论文中的定理或原句。</p>
        </section>

        <section id="diagnostics"><div class="section-no">07 / Finite diagnostics</div><h2>有限曲线只保留为 sharpen 线索</h2>
          <p>producer 与 independent route 在声明截断、步长和 \(\sigma\) 网格上互相吻合，并与 \(O(a^2\log\sigma)\) 曲线相容。这只能说明有限离散没有暴露冲突；它不证明 continuum logarithmic bound，也不决定尖锐常数。</p>
        </section>

        <section id="figure"><div class="section-no">08 / Journal figure</div><h2>附图把 action no-go、published decay 和本站 corollary 分开</h2>
          <p><img src="/assets/r072n/fig-r072n-dissipative-carrier.svg" alt="R0.72N dissipative one-carrier action no-go and enhanced-dissipation corollary formal figure"></p>
          <p>彩图中的有限量是 fixed-geometry proxies：\(K_{\rm proxy}=1+D_{\max}\)、\(x_{\rm proxy}=\sigma^2\mathscr A_\sigma\)、\(U=\sigma^{7/3}\)、\(V=\sigma^{1/3}\)，并取 \(\mu=a=1\)，固定几何常数已压掉。它们不是实际物理常数；\(T/V\le1\) 是解析 ceiling。图中的 \(\sqrt\sigma\) 上界是本站从 Coble–He Theorem 1.2 推出的 corollary。</p>
          <p><a href="/assets/r072n/fig-r072n-dissipative-carrier.pdf">下载 PDF</a> · <a href="/assets/r072n/fig-r072n-dissipative-carrier.png">下载 PNG</a> · <a href="/assets/r072n/fig-r072n-dissipative-carrier.svg">打开 SVG</a></p>
        </section>

        <section id="literature"><div class="section-no">09 / Literature boundary</div><h2>published theorem、project corollary 与开放 sharpen 是三层结论</h2>
          <p><a href="https://arxiv.org/abs/2309.15738">Coble–He</a> 直接支持非退化时变剪切的 \(L^2\) enhanced dissipation。它不陈述本站 cubic functional、\(O(a^2\sigma^{1/2})\) 推论或 logarithmic rowwise variation。</p>
          <p><a href="https://doi.org/10.1002/cpa.21831">Coti Zelati–Delgadino–Elgindi</a> 给出 mixing 到 enhanced dissipation 的抽象方向；<a href="https://arxiv.org/abs/2511.18536">Albritton–Beekie</a> 的 fixed-shear sharp mixing 为 logarithmic sharpen 提供相邻线索。两者都不直接覆盖这里的时变振幅与 first-row total variation。限定检索不构成新颖性或优先权证明。</p>
        </section>

        <section id="value"><div class="section-no">10 / Research value</div><h2>价值是关闭错误分支，并留下一个可移植的次线性机制</h2>
          <p>R0.72N 严格排除了“耗散会自动把 action 压到 danger window 下方”的想法，同时把 raw \(O(\sigma a^2)\) cubic estimate 改进为一载波类中的 \(O(a^2\sqrt\sigma)\)。这比有限拟合更弱，但已是连续方程上的统一次线性结论。</p>
          <p>它没有闭合 R0.72L 的完整物理 ledger，也没有产生一般三维 continuation criterion。对 Clay 问题的作用仍是筛选机制和缩小接口，原问题保持开放。</p>
        </section>

        <section id="next"><div class="section-no">11 / Next gate</div><h2>R0.72O：回填物理账本并检查多载波稳定性</h2>
          <p>下一节先把 \(O(a^2\sqrt\sigma)\) 重新代入 R0.72L 的 normalized physical ledger，确定一载波强耦合窗口；随后检查有限或 common-band 多载波叠加是否因 cross terms 丢失 \(\sigma^{1/2}\) 增益。logarithmic BV sharpen 保留为可并行但非必需的目标。</p>
        </section>

        <section id="claims"><div class="section-no">12 / Claim boundary</div><h2>一般 Navier–Stokes 问题仍未解决</h2>
          <p>本节没有证明 matching asymptotic、logarithmic cubic、多载波、multiscale physical absorption、任意三维继续性、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="reproduce"><div class="section-no">13 / Reproduction</div><h2>报告、主张矩阵、文献审计和双路证书</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_independent_audit.md">独立审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072n">双路机器证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072n-dissipative-carrier/fig-r072n-dissipative-carrier">正式附图包</a> · <a href="/notes/r0-72n.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72n.html">累计回顾</a> · <a href="/recap-r0-61-r0-72n.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72O</span><span class="tree-state current">下一检查点</span></div>
              <h3>one-carrier physical reinsertion and multi-carrier stability</h3>
              <p>把 \(O(a^2\sqrt\sigma)\) 回填 R0.72L 的 normalized physical ledger，并检查有限或 common-band 多载波 cross terms 是否保留次线性增益。</p>
            </article>'''


HOME_RECAP = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72N · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 104 个节点；全站现有 164 篇公开研究笔记</h3>
            <p>累计回顾保持二十八个问题阶段，完整覆盖 R0.61–R0.72N。R0.72N 证明 action-poor 路线对声明耗散 launch 失效，并把 Coble–He 时变剪切衰减转成本站的 \(O(a^2\sqrt\sigma)\) cubic corollary。R0.70A–R0.72N 共 66 个版本已公开；42 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;一载波 true cubic 已统一次线性；logarithmic sharpen、物理回填和多载波稳定性仍开放。</p>
            <p><a href="/recap-r0-61-r0-72n.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72n.pdf">下载同步 PDF</a></p>
          </div>'''


HOME_N_CARD = r'''          <div class="task-one" id="r072n" data-release="r072n" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72N · 2026-08-27</p>
            <h3>耗散 action 不在安全分支；时变剪切仍给次线性 cubic</h3>
            <p>我证明 \(K_\sigma\lesssim1+\sigma^{2/3}\) 而 \(x_\sigma\gtrsim\sigma^{4/3}\log\sigma\)，所以 \(\sigma^{1/3}x_\sigma/K_\sigma\gtrsim\sigma\log\sigma\)。action-poor 路线在声明 launch 上失效，scalar screen 为 \(\sigma^{1/3}\) 量级。</p>
            <p>Coble–He Theorem 1.2 应用于重标度生成函数；坐标投影与时间积分再给本站 corollary \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma=o(\sigma a^2)\)。这不是原论文原句；logarithmic rate 仍未证明。</p>
            <p><strong>结论边界：</strong>&nbsp;多载波、multiscale physical absorption 与一般三维正则性仍开放。</p>
            <p><a href="/notes/r0-72n.html"><strong>阅读 R0.72N 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72n.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072n/fig-r072n-dissipative-carrier.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072n">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072n_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072n-dissipative-carrier/fig-r072n-dissipative-carrier">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72n.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72n.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72O：</strong>&nbsp;回填 normalized physical ledger，并检查多载波 cross terms。</p>
          </div>'''


def build_note() -> None:
    html = (PUBLIC / "notes" / "r0-72m.html").read_text(encoding="utf-8")
    replacements = [
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72N：耗散一载波 action-poor 路线失效；Coble–He 映射给出本站的次线性 cubic 推论。">', "description"),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72N｜耗散 action no-go 与次线性 cubic">', "og title"),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="完整耗散链的矩障碍、action 下界、时变剪切映射与开放的 logarithmic sharpen。">', "og description"),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072n/fig-r072n-dissipative-carrier.png">', "og image"),
        (r'<title>.*?</title>', '<title>R0.72N｜耗散 action no-go 与次线性 cubic</title>', "title"),
    ]
    for pattern, value, label in replacements:
        html = section(html, pattern, value, f"note {label}")
    html = required(html, "/i18n-en.js?v=1.26", "/i18n-en.js?v=1.27", "note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#chain">耗散链</a><a href="#moment">矩账本</a><a href="#action">action</a><a href="#screen">危险窗</a><a href="#mapping">剪切映射</a><a href="#cubic">cubic</a><a href="#diagnostics">诊断</a><a href="#figure">附图</a><a href="#literature">文献边界</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#chain">01 · 完整耗散链</a></li><li><a href="#moment">02 · 能量与二阶矩</a></li><li><a href="#action">03 · critical-log action</a></li><li><a href="#screen">04 · scalar screen</a></li><li><a href="#mapping">05 · 时变剪切映射</a></li><li><a href="#cubic">06 · 本站推论</a></li><li><a href="#diagnostics">07 · 有限诊断</a></li><li><a href="#figure">08 · 正式附图</a></li><li><a href="#literature">09 · 文献边界</a></li><li><a href="#value">10 · 研究价值</a></li><li><a href="#next">11 · R0.72O</a></li><li><a href="#claims">12 · 主张边界</a></li><li><a href="#reproduce">13 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72N · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>', "note footer")
    assert_clean(html, "R0.72N note")
    (PUBLIC / "notes" / "r0-72n.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72m.html").read_text(encoding="utf-8")
    changes = [
        ("/i18n-en.js?v=1.26", "/i18n-en.js?v=1.27"),
        ("R0.61–R0.72M", "R0.61–R0.72N"),
        ("R0.61 到 R0.72M 的 103 个研究节点", "R0.61 到 R0.72N 的 104 个研究节点"),
        ("收录节点：103", "收录节点：104"),
        ("回顾截止时公开笔记：163", "回顾截止时公开笔记：164"),
        ("回顾截止节点：R0.72M", "回顾截止节点：R0.72N"),
        ("02 · 103 节完整索引", "02 · 104 节完整索引"),
        ("<strong>103</strong><span>R0.61–R0.72N 研究节点</span>", "<strong>104</strong><span>R0.61–R0.72N 研究节点</span>"),
        ("<strong>65</strong><span>R0.70A–R0.72M 已公开版本</span>", "<strong>66</strong><span>R0.70A–R0.72N 已公开版本</span>"),
        ("<strong>41</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>42</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("后面的 103 个节点", "后面的 104 个节点"),
        ("R0.70A–R0.72M 的 65 个版本已经公开；其中 41 个", "R0.70A–R0.72N 的 66 个版本已经公开；其中 42 个"),
        ("R0.61–R0.72N 的 103 节公开笔记", "R0.61–R0.72N 的 104 节公开笔记"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"recap {old}")
    html = section(html, r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72N 的 104 个研究节点；最新一节排除 action-poor 路线并证明一载波 true cubic 次线性。">', "recap description")
    html = section(html, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十八个阶段、104 个节点：从约化递推和时间迹账本，到 critical-log action、耗散链与 enhanced-dissipation corollary。">', "recap og description")
    html = section(html, r'<title>.*?</title>', '<title>R0.61–R0.72N｜R0.60 之后的研究回顾</title>', "recap title")
    html = required(html, "/recap-r0-61-r0-72m.pdf", "/recap-r0-61-r0-72n.pdf", "recap self PDF")

    old_phase = r'''            <article class="phase"><h3>R0.72L–R0.72M · 中强耦合窗口与精确 action screen</h3>
              <p>R0.72L 把 actual enstrophy contrast \(K\) 与 actual action \(x\) 留在 complete-root denominator 中，将 closure 推进到随 \(R\) 增长的 moderate strong-coupling window。R0.72M 随后精确求出 scalar cubic 的全部超水平区间。</p>
              <p>完整一载波零扩散参考链有 Bessel 解、\(K_{\rm fr}\asymp\sigma^2\)、\(x_{\rm fr}\asymp\sigma^{4/3}\log\sigma\) 和 \(\mathcal C_{\rm fr}=(16/\pi^2)a^2\log\sigma+O(a^2)\)。它位于 action-poor 分支；带 diagonal heat 的耗散链仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/assets/r072m/fig-r072m-danger-window.pdf">R0.72M 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072m">R0.72M 证书</a></div></article>'''
    new_phase = r'''            <article class="phase"><h3>R0.72L–R0.72N · strong-coupling screen 与耗散决策</h3>
              <p>R0.72L 保留 actual \(K\) 与 \(x\)，R0.72M 把 scalar danger window 精确化。R0.72N 回到完整耗散一载波链，证明 \(K_\sigma\lesssim1+\sigma^{2/3}\) 而 \(x_\sigma\gtrsim\sigma^{4/3}\log\sigma\)，从而排除声明 launch 上的 action-poor route。</p>
              <p>Coble–He 的时变剪切 \(L^2\) 衰减经坐标投影和时间积分给本站 corollary \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma\)。logarithmic sharpen、多载波稳定性和物理账本回填仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/notes/r0-72n.html">R0.72N</a><a href="/assets/r072n/fig-r072n-dissipative-carrier.pdf">R0.72N 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072n">R0.72N 证书</a></div></article>'''
    html = once(html, old_phase, new_phase, "recap N phase")
    node_m = '            <span class="node-ref"><a href="/notes/r0-72m.html">R0.72M</a><span class="node-state kind-closed">闭</span></span>\n'
    node_n = '            <span class="node-ref"><a href="/notes/r0-72n.html">R0.72N</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_m, node_m + node_n, "recap N node")
    retained_n = r'''            <li>R0.72N 的 dissipative one-carrier theorem：声明 launch 上 \(K_\sigma\lesssim1+\sigma^{2/3}\)、\(x_\sigma\gtrsim\sigma^{4/3}\log\sigma\)，故 action-poor route 失效；Coble–He 的 published \(L^2\) decay 经本站投影给 \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma=o(\sigma a^2)\)。后者是本站 corollary；logarithmic rate 与多载波仍开放。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained_n + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained N")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>action-poor 分支已排除，一载波 true cubic 已统一次线性</h2>
          <p>截至 R0.72N，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 104 个节点或 66 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>新的严格结果是耗散链的 energy/moment barrier、critical-log action lower bound、action-poor no-go 和 \(T_\sigma\asymp\sigma^{1/3}\)。</p>
          <p>Coble–He published theorem 经本站坐标投影给 \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma\)。logarithmic sharpen、物理回填和多载波 cross terms 仍开放。</p>
        </section>''', "recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72O 回填物理账本并测试多载波</h2>
          <p>先把 \(O(a^2\sqrt\sigma)\) 代回 R0.72L normalized physical ledger，确定一载波强耦合窗口。</p>
          <p>随后检查有限或 common-band 多载波叠加中的 cross terms；logarithmic BV sharpen 保留为并行目标。</p>
        </section>''', "recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72N 的 66 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，42 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。</p>
          <p>R0.72N 只覆盖声明的 fixed-band、row-aligned、one-carrier chain。\(O(a^2\sqrt\sigma)\) 是本站从 Coble–He 半群估计推出的 corollary，不是原论文定理；有限 log 曲线不是证明，Clay 正式问题仍然开放。</p>
        </section>''', "recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72m.html">保留 R0.72M 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72n.html">打开最新节点 R0.72N</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072n">查看 R0.72N 双路证书</a> · <a href="/assets/r072n/fig-r072n-dissipative-carrier.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72n.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72m.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>''', "recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72N 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>', "recap footer")
    assert_clean(html, "R0.72N recap")
    (PUBLIC / "recap-r0-61-r0-72n.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    changes = [
        ('data-site-version="1.26"', 'data-site-version="1.27"'),
        ("/i18n-en.js?v=1.26", "/i18n-en.js?v=1.27"),
        ("/site-refresh.js?v=1.26", "/site-refresh.js?v=1.27"),
        ("<strong>v1.26</strong>网页版本", "<strong>v1.27</strong>网页版本"),
        ("<strong>163</strong>公开研究笔记", "<strong>164</strong>公开研究笔记"),
        ("<strong>R0.72M</strong>最新研究节点", "<strong>R0.72N</strong>最新研究节点"),
        ("<strong>dissipative one-carrier cubic/action theorem</strong>当前方向", "<strong>one-carrier physical reinsertion and multi-carrier stability</strong>当前方向"),
        ("Research topology · R0.1–R0.72M", "Research topology · R0.1–R0.72N"),
        ("R0.70A–R0.72M：65 节已公开，41 节完整封存", "R0.70A–R0.72N：66 节已公开，42 节完整封存"),
        ("<span class=\"route-range\">R0.69P–R0.72M</span>", "<span class=\"route-range\">R0.69P–R0.72N</span>"),
        ('aria-label="R0.69P–R0.72M"', 'aria-label="R0.69P–R0.72N"'),
        ("展开 73 篇公开笔记", "展开 74 篇公开笔记"),
        ("综述 v1.26 · 2026-08-27", "综述 v1.27 · 2026-08-27"),
        ("上次综述 v1.25 · 2026-08-27", "上次综述 v1.26 · 2026-08-27"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"home {old}")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', r'<div class="summary-item"><strong>我目前关注</strong><span>R0.72N 已排除声明耗散 launch 上的 action-poor 路线，并由 Coble–He 时变剪切衰减推出本站的 \(O(a^2\sqrt\sigma)\) cubic corollary；物理回填、多载波和 logarithmic sharpen 仍开放。</span></div>', "home summary")
    html = once(html, "从 moderate strong-coupling window 走到 exact action screen", "从 exact action screen 走到 dissipative one-carrier decision", "home route title")
    old_route_end = r'''R0.72M 精确求出 scalar danger window，并在完整一载波 Bessel reference 上证明 action-poor placement 与 \((16/\pi^2)a^2\log\sigma\) cubic law。</p>'''
    new_route_end = r'''R0.72M 精确求出 scalar danger window，并在完整一载波 Bessel reference 上证明 action-poor placement 与 \((16/\pi^2)a^2\log\sigma\) cubic law。R0.72N 回到耗散链，证明 action-poor route 对声明 launch 失效；再把 Coble–He 的时变剪切衰减转成本站的 \(O(a^2\sqrt\sigma)\) cubic corollary。</p>'''
    html = once(html, old_route_end, new_route_end, "home route N prose")
    html = once(html, "→ exact action danger window → dissipative one-carrier gate</p>", "→ exact action danger window → dissipative one-carrier decision → physical reinsertion and multi-carrier gate</p>", "home path N")
    nav_m = '                  <a class="milestone" href="/notes/r0-72m.html">R0.72M</a>\n'
    html = once(html, nav_m, nav_m + '                  <a class="milestone" href="/notes/r0-72n.html">R0.72N</a>\n', "home N route link")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "home next")
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', HOME_RECAP, "home recap")
    old_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72N：</strong>&nbsp;证明耗散一载波链的 logarithmic cubic bound 或 action-poor inequality。</p>
          </div>
        </section>'''
    new_tail = r'''            <p><strong style="color:var(--gold)">R0.72N 已完成：</strong>&nbsp;action-poor route 对声明耗散 launch 失效；one-carrier true cubic 已得到统一次线性上界。</p>
          </div>

''' + HOME_N_CARD + r'''
        </section>'''
    html = once(html, old_tail, new_tail, "home N card")
    html = required(html, "/recap-r0-61-r0-72m.html", "/recap-r0-61-r0-72n.html", "home recap HTML endpoint")
    html = required(html, "/recap-r0-61-r0-72m.pdf", "/recap-r0-61-r0-72n.pdf", "home recap PDF endpoint")
    assert_clean(html, "R0.72N home")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    changes = [
        ("/i18n-en.js?v=1.26", "/i18n-en.js?v=1.27"),
        ("文献综述 v1.26 · 2026-08-27", "文献综述 v1.27 · 2026-08-27"),
        ("本站 R0.69P–R0.72M 只列为研究笔记", "本站 R0.69P–R0.72N 只列为研究笔记"),
        ("累计回顾与 103 节索引", "累计回顾与 104 节索引"),
        ("打开 103 节完整索引", "打开 104 节完整索引"),
        ("/recap-r0-61-r0-72m.html", "/recap-r0-61-r0-72n.html"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"literature {old}")
    old_route = r'''R0.72M 精确求出 scalar action danger window，并在完整一载波 zero-diffusion chain 上证明 Bessel action-poor benchmark 与 sharp logarithmic cubic law。一般 Navier–Stokes 正则性仍开放。</p>'''
    new_route = r'''R0.72M 精确求出 scalar action danger window，并在完整一载波 zero-diffusion chain 上证明 Bessel action-poor benchmark 与 sharp logarithmic cubic law。R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma\)；logarithmic rate 与多载波仍开放。一般 Navier–Stokes 正则性仍开放。</p>'''
    html = once(html, old_route, new_route, "literature N route")
    old_open = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72N</b><strong>dissipative one-carrier cubic/action theorem</strong></header><p>证明 \(\mathcal C_{\rm diss}=O(a^2\log(1+\sigma))\)，或证明 \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\)。</p></div>'''
    new_open = r'''              <div class="route-step closed"><header><b>R0.72N</b><strong>dissipative action no-go and sublinear cubic</strong></header><p>声明 launch 上 action-poor route 失效；Coble–He published \(L^2\) decay 经本站投影给 \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma\)。logarithmic rate 仍开放。<a href="/notes/r0-72n.html">研究笔记</a> <a href="/recap-r0-61-r0-72n.html">当前累计回顾</a> <a href="#r072n-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72O</b><strong>physical reinsertion and multi-carrier stability</strong></header><p>把一载波次线性 cubic 回填 normalized physical ledger，并检查多载波 cross terms 是否保留 \(\sigma^{1/2}\) 增益。</p></div>'''
    html = once(html, old_open, new_open, "literature N cards")
    m_boundary = r'''          <div class="boundary"><strong>R0.72M 的主张边界</strong><p>解析定理覆盖 scalar superlevel set 与声明的一载波 zero-diffusion reference。删除 relative diagonal heat 不是 dissipative PDE reduction；两套 finite dissipative curves 只作 convergence diagnostic。限定检索不构成新颖性或优先权证明。</p></div>'''
    n_boundary = r'''

          <h3 id="r072n-boundary">R0.72N 的时变剪切映射与 cubic 署名边界</h3>
          <p><a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He, Theorem 1.2</a> 对非退化 time-dependent shear 给 \(L^2\) decay \(e^{-c\nu^{1/2}|k|^{1/2}t}\)。R0.72N 直接核对 \(k=-2\)、horizontal diffusion switch \(=0\)、\(V(t,\theta)=e^{-\nu t}\sin\theta\) 及 \(0\le t\le\nu^{-1}\) 上的统一常数。</p>
          <p>由坐标估计、Parseval 和时间积分得到 \(\mathcal C_{\rm diss}\lesssim a^2\sigma^{1/2}\)，这是本站从 published semigroup estimate 推出的 corollary，不是 Coble–He 原论文的定理或原句。<a href="https://doi.org/10.1002/cpa.21831">Coti Zelati–Delgadino–Elgindi</a> 的 mixing-to-dissipation 框架与 <a href="https://arxiv.org/abs/2511.18536">Albritton–Beekie</a> 的 fixed-shear sharp mixing 都不直接给这里的 logarithmic first-row variation。</p>
          <div class="boundary"><strong>R0.72N 的主张边界</strong><p>action-poor no-go 只覆盖声明的 fixed-band、row-aligned、one-carrier launch；\(O(a^2\log\sigma)\) 仍是有限诊断支持的开放 sharpen。matching asymptotic、多载波、multiscale physical absorption 和一般三维继续性均未闭合；限定检索不构成新颖性或优先权证明。</p></div>'''
    html = once(html, m_boundary, m_boundary + n_boundary, "literature N boundary")
    reference = r'''            <li id="ref-104">W. Stadje. <a href="https://doi.org/10.1017/S0013091500017417"><em>On functions with derivative of bounded variation: An analogue of Banach's indicatrix theorem</em></a>. Proc. Edinburgh Math. Soc. 29 (1986).</li>'''
    reference_n = reference + r'''
            <li id="ref-105">D. Coble and S. He. <a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10"><em>A Note on Enhanced Dissipation of Time-Dependent Shear Flows</em></a>. Communications in Mathematical Sciences 22(6) (2024). <a href="https://arxiv.org/abs/2309.15738">arXiv:2309.15738</a>.</li>'''
    html = once(html, reference, reference_n, "literature Coble-He reference")
    assert_clean(html, "R0.72N literature")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    note_count = len(list((PUBLIC / "notes").glob("*.html")))
    if note_count != 164:
        raise RuntimeError(f"expected 164 public HTML notes, found {note_count}")
    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({
        "latestCompletedRelease": "r072n", "siteVersion": "1.27",
        "publicHtmlNoteCount": note_count, "postR060RecapNodeCount": 104,
        "nextRelease": "r072o", "latestReleaseGate": "tests/r072n-dissipative-carrier-gate.test.mjs",
        "postR070APublishedReleaseCount": 66, "postR070AFormalSealedReleaseCount": 42,
        "legacyFormalFigureBacklogCount": 24,
    })
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.27", "latestRelease": "R0.72N", "publicHtmlNoteCount": note_count, "publishedDate": "2026-08-27"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update({"latestPublishedRelease": "r072n", "publishedReleaseCount": 66, "formalSealedReleaseCount": 42, "legacyFormalFigureBacklogCount": 24})
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072n" not in inventory[key]:
            inventory[key].append("r072n")
    if len(inventory["legacyFormalFigureBacklog"]) != 24:
        raise RuntimeError("legacy formal-figure backlog changed unexpectedly")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-72n.html", "recap-r0-61-r0-72n.html"):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({
        "release": "R0.72N", "siteVersion": "1.27", "notes": 164,
        "recapNodes": 104, "published": 66, "formalSealed": 42,
        "legacyBacklog": 24, "phases": 28, "next": "R0.72O",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
