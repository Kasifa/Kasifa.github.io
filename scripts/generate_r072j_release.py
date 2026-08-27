#!/usr/bin/env python3
"""Generate the deterministic R0.72J GitHub Pages release from site v1.22."""

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


def section(text: str, pattern: str, new: str, label: str) -> str:
    updated, count = re.subn(pattern, lambda _match: new, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return updated


HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72J · CAYLEY GRAPH · TRIANGLE RETURN · TRUE CUBIC</div>
        <h1>非二分图出现以后，<br>还要再问 cubic 是否真的存活</h1>
        <p class="lead">R0.72I 的奇偶修复不是“原整数全奇”这一种写法，而是 gcd 约化后的 Cayley 图二分性。离开二分情形只说明存在某条奇闭路；真实 \(P_0V^2F\) 在 aligned launch 上立即返回，还需要三步有符号关系。共同频带内即使安排大量三角关系，raw cubic 可以增长，true cubic contribution 的归一化比仍然衰减。这个方向需要进入多尺度或强耦合，不能把 non-bipartite 直接写成反例。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72J 负结果完成</span><strong>graph classified, common-band counterroute closed</strong><p>版本 v0.72J · 2026-08-27</p><p>gcd-reduced bipartite test: CLOSED</p><p>triangle return criterion: CLOSED</p><p>common-band normalized counterfamily: NO-GO</p><p>complete complex-root ledger: OPEN</p><p>一般三维正则性：OPEN</p></div>
    </div></header>'''


ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Four statements</div><h2>图论、cubic 返回、物理尺度和根账本不能混成一句</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · EXACT GRAPH TEST</strong><p>令 \(g=\gcd(r_1,\ldots,r_M)\)。目标连通分支的 Cayley 图二分，当且仅当每个约化载波 \(r_j/g\) 都是奇数。</p></div>
            <div class="verdict-card true"><strong>THEOREM · TRIANGLE IS STRICTER</strong><p>non-bipartite 只保证某条奇闭路；aligned launch 的二步返回要求 \(R_1(0)\cap R_2(0)\ne\varnothing\)，等价于存在有符号三载波关系。</p></div>
            <div class="verdict-card false"><strong>NO-GO · COMMON BAND</strong><p>在声明的 common-band perturbative scaling 下，true cubic contribution 的归一化比至多为 \(CR^{-4/9}(1+\log R)^{-2/3}\)，所以一致趋零。</p></div>
            <div class="verdict-card false"><strong>OPEN · COMPLETE ROOTS</strong><p>mixed-parity aligned target 一般是复值。前几节依赖实标量 Rolle 归约的 complete-root ledger 没有自动延伸到这里。</p></div>
          </div>
        </section>

        <section id="graph"><div class="section-no">01 / GCD-reduced Cayley graph</div><h2>真正的不变量是约化载波，不是原整数的表面奇偶</h2>
          <p>对 carrier set \(S=\{r_1,\ldots,r_M\}\subset\mathbb N\)，令 \(g=\gcd S\)，并在目标连通分支 \(g\mathbb Z\) 上连边 \(n\leftrightarrow n\pm r_j\)。除以 \(g\) 后得到由 \(a_j=r_j/g\) 生成的连通 Cayley 图。</p>
          <div class="equation result">\[
            \boxed{\operatorname{Cay}(\mathbb Z;\{\pm a_j\})\text{ 二分}
            \quad\Longleftrightarrow\quad a_j\equiv1\pmod2\ \text{对所有 }j.}
          \]</div>
          <p>若全部 \(a_j\) 为奇数，整数 parity 就是一组二着色，每条 carrier edge 都换色。反之，连通 Cayley 图的二着色从零点唯一延伸，并给出到 \(\mathbb Z_2\) 的群同态；每个生成元必须映到 1，因此不允许偶生成元。</p>
          <p>所以 \(\{2,6\}\) 虽然原载波全偶，除以 \(g=2\) 后是 \(\{1,3\}\)，仍属于 R0.72I 的二分修复。混合 parity 也必须先约化再判断。</p>
        </section>

        <section id="triangle"><div class="section-no">02 / Sphere one versus sphere two</div><h2>奇闭路可能很长；cubic 只看长度三</h2>
          <p>把带相位的 signed carrier coefficient 记为 \(c_s(x)\)，\(s\in\pm S\)。目标行的两个真实量为</p>
          <div class="equation result">\[
            h=(VF)_0=\sum_{s\in\pm S}c_sF_{-s},\qquad
            b=(V^2F)_0=\sum_{s,t\in\pm S}c_sc_tF_{-(s+t)}.
          \]</div>
          <p>aligned launch 支持在第一球 \(R_1(0)=\pm S\)。因此 \(b\) 在零时刻读到 launch，当且仅当</p>
          <div class="equation result">\[
            R_1(0)\cap R_2(0)\ne\varnothing
            \quad\Longleftrightarrow\quad
            \exists\,s,t,u\in\pm S:\ s+t+u=0.
          \]</div>
          <p>这是载波 Cayley 图中的三角关系。它严格强于 non-bipartite。例如约化集合 \(\{1,4\}\) 的图非二分，但最短奇闭路长度为五，没有三载波关系，所以 aligned launch 不产生 leading cubic return。</p>
        </section>

        <section id="band"><div class="section-no">03 / Common-band perturbative no-go</div><h2>三角关系使 cubic 非零，却没有克服物理归一化</h2>
          <p>对载波位于一个可比频带、系数和 launch 满足报告所列统一界的 mixed-parity family，真实 cubic payment 直接保留为</p>
          <div class="equation result">\[
            \mathcal C_{\times,R}=|\delta_R|\int_I|h_R(x)P_0V_R(x)^2F_R(x)|\,dx.
          \]</div>
          <p>不再使用 R0.72I 已排除的 \(B_AQ_*\) 分离。共同热时间 \(R^{-2}\)、aligned row 大小和 perturbative coupling window 联合给出</p>
          <div class="equation result">\[
            \boxed{\frac{2\Theta_R\mathcal C_{\times,R}}
            {D_R^{1/3}[1+\Theta_RQ_{*,R}]}
            \le C R^{-4/9}(1+\log R)^{-2/3}\longrightarrow0.}
          \]</div>
          <p>这是一条 common-band aligned perturbative no-go，不是 arbitrary-carrier 上界。它说明只在同一频带增加三角数，仍不能得到存活的 normalized cubic counterfamily。</p>
        </section>

        <section id="coherent"><div class="section-no">04 / Coherent dense family</div><h2>raw cubic 达到二次规模，true cubic contribution 的归一化比仍衰减</h2>
          <p>取最直接的 mixed-parity 稠密集合 \(S_R=\{R,R+1,\ldots,3R-1\}\)。若 \(T_R\) 计数 \((s,t,u)\in(\pm S_R)^3\) 中满足 \(s+t+u=0\) 的有序有符号三元组，则</p>
          <div class="equation result">\[
            \boxed{T_R=3R(R+1).}
          \]</div>
          <p>正关系 \(a+b=c\) 的有序对共有 \(R(R+1)/2\) 个，再乘负项位置和整体符号的六种选择。相位对齐后，真实 raw cubic 满足 \(\mathcal C_{\times,R}\asymp R^2\)，不是被 parity 消掉的零量。</p>
          <p>但相同数据的 physical lift、能量成本和 critical-log action 也同步增长。诊断缩放给</p>
          <div class="equation result">\[
            \boxed{\mathcal C_{\times,R}\asymp R^2,\qquad
            \frac{2\Theta_R\mathcal C_{\times,R}}
            {D_R^{1/3}[1+\Theta_RQ_{*,R}]}
            \asymp R^{-2/3}\longrightarrow0.}
          \]</div>
          <p>因此“很多三角关系”是 raw interaction 的充分来源，却不是物理归一化反例的充分来源。</p>
        </section>

        <section id="root"><div class="section-no">05 / Complex target obstruction</div><h2>当前结果没有闭合 mixed-parity complete-root ledger</h2>
          <p>R0.72G–I 的 Rolle–BV 归约使用兼容 gauge 把目标坐标和目标 row 变成实标量。mixed-parity coherent family 的 phase alignment 一般使目标轨道落在 \(\mathbb C\)，而复曲线的零点没有实函数符号交替。</p>
          <p>所以本节严格控制的是 aligned true-cubic interaction 与其物理尺度，不把它升级成 complete temporal self-zero theorem。要得到根账本，还需要复目标的二维零点机制、额外相位锁定，或不依赖 Rolle 的全新归约。</p>
        </section>

        <section id="audit"><div class="section-no">06 / Exact and independent audit</div><h2>组合计数、图分类和有限动力学由两条实现交叉核对</h2>
          <div class="audit-grid">
            <div class="audit-card"><strong>PRODUCER · ARCHIVED PASS</strong><p>\(R=64\) 时 \(T_R=12480\)、\(|b(0)|=8824.692629208112\)，且 \(\mathcal C_{\times,R}=69.2166385023\)。末三档 raw 与 normalized 斜率分别为 1.9501881021 和 -0.7370277418。</p><p class="mini-kpi">finite corroboration only · analytic exponents proved separately</p></div>
            <div class="audit-card"><strong>INDEPENDENT · ARCHIVED PASS</strong><p>独立 edge-list/RK45 路线在 \(R=64\) 得到 \(\mathcal C_{\times,R}=69.2166385022\)、normalized true cubic \(1.0386272844\times10^{-6}\)。</p><p class="mini-kpi"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_independent_audit.md">独立逐式审计</a></p></div>
          </div>
          <p>五个共同规模上的最大相对差为：\(Q_*\) 的 \(1.53322\times10^{-6}\)、\(\mathcal C_{\times,R}\) 的 \(2.94064\times10^{-12}\)、normalized true cubic 的 \(7.28034\times10^{-9}\)。有限审计只核对离散代数、实现与有限尺度趋势；渐近 no-go 由报告中的解析估计承担。</p>
        </section>

        <section id="figure"><div class="section-no">07 / Journal figure</div><h2>正式附图分开显示图分类、三角计数与归一化衰减</h2>
          <p><img src="/figures/r0-72j-mixed-parity-cubic.svg" alt="R0.72J mixed-parity cubic interaction formal figure"></p>
          <p><a href="/figures/r0-72j-mixed-parity-cubic.pdf">下载 PDF</a> · <a href="/figures/r0-72j-mixed-parity-cubic.png">下载 PNG</a> · <a href="/figures/r0-72j-mixed-parity-cubic.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">08 / Research value</div><h2>关闭的是一条看似直接的 mixed-parity 反族路线</h2>
          <p>这一步把 R0.72I 的 parity observation 提升成精确的 gcd-reduced graph theorem，并识别出真正进入 cubic row 的长度三 additive relation。它阻止两种误判：原载波有偶数就一定失去修复；图非二分就一定有 leading cubic。</p>
          <p>更关键的负结果是：即使选择三角数达到二次规模的 coherent block，true cubic contribution 的归一化比也没有存活。下一步必须改变尺度结构或耦合区间，而不是继续堆积同频带三角关系。</p>
        </section>

        <section id="next"><div class="section-no">09 / Next gate</div><h2>R0.72K：多尺度、强耦合，或复目标根机制</h2>
          <p>下一关只保留三个可能改变结论的接口：让 carrier triangles 跨多个热时间尺度；离开当前 perturbative coupling window 并重新支付完整能量与 action；或先建立 complex target 的 complete-root ledger。</p>
          <p>验收标准仍是直接控制真实 \(|\delta|\int|hP_0V^2F|\) 或真实根斜率账本，并在完整物理归一化后给出闭合上界或存活反族。</p>
        </section>

        <section id="claims"><div class="section-no">10 / Claim boundary</div><h2>一般 Navier–Stokes 问题仍然开放</h2>
          <p>图分类与 triangle-return 判据是精确离散结论。common-band no-go 和 coherent-family scaling 只覆盖报告中声明的 exact triangular 2.5D aligned perturbative families。</p>
          <p>本节没有证明 arbitrary-carrier physical inequality，没有 complete complex-root theorem，没有构造有限时奇性，也没有证明一般三维 Navier–Stokes 全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="reproduce"><div class="section-no">11 / Reproduction</div><h2>报告、双路证书、附图与累计回顾</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_independent_audit.md">独立审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072j">双路机器证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072j-mixed-parity-cubic/fig-r072j-mixed-parity-cubic">正式附图包</a> · <a href="/notes/r0-72j.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72j.html">累计回顾</a> · <a href="/recap-r0-61-r0-72j.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


def build_note() -> None:
    html = (PUBLIC / "notes" / "r0-72i.html").read_text(encoding="utf-8")
    changes = [
        ("研究笔记 R0.72I：R0.72H (6.5) 的正项上界不能逐项吸收到物理尺度，但同一全奇数 Rudin–Shapiro 族的真实完整根账本在 critical-log 归一化后趋于零。",
         "研究笔记 R0.72J：gcd 约化后的载波 Cayley 图二分性具有精确分类；真正的 cubic 返回要求三角关系。common-band 与 coherent mixed-parity 族的真实 cubic 虽非零，物理归一化后仍衰减。"),
        ("R0.72I｜吸收失败不等于物理反例", "R0.72J｜非二分不等于 cubic 反例"),
        ("B_AQ_* 的分离上界太粗；保留联合暴露或利用奇偶分裂后，真实全奇数 complete-root ledger 反而衰减。",
         "图论障碍、三角返回与物理归一化必须分开；当前 common-band 构造没有产生存活的 normalized cubic ledger。"),
        ("r0-72i-physical-absorption.png", "r0-72j-mixed-parity-cubic.png"),
        ("/i18n-en.js?v=1.22", "/i18n-en.js?v=1.23"),
    ]
    for old, new in changes:
        if old not in html:
            raise RuntimeError(f"note missing: {old}")
        html = html.replace(old, new)
    html = once(
        html,
        "    .mini-kpi{font-family:var(--mono);font-size:.84rem;color:var(--muted)}\n",
        "    .mini-kpi{font-family:var(--mono);font-size:.84rem;color:var(--muted)}\n"
        "    article img{max-width:100%;height:auto}\n",
        "note responsive figure",
    )
    nav = '<nav><a href="#result">结论</a><a href="#graph">图分类</a><a href="#triangle">三角返回</a><a href="#band">共同频带</a><a href="#coherent">相干族</a><a href="#root">根账本</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "note nav")
    html = section(html, r'    <header class="hero">.*?</header>', HERO, "note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 四句判断</a></li><li><a href="#graph">01 · gcd 约化图</a></li><li><a href="#triangle">02 · 三角返回</a></li><li><a href="#band">03 · 共同频带 no-go</a></li><li><a href="#coherent">04 · 相干稠密族</a></li><li><a href="#root">05 · 复目标根边界</a></li><li><a href="#audit">06 · 独立审计</a></li><li><a href="#figure">07 · 正式附图</a></li><li><a href="#value">08 · 研究价值</a></li><li><a href="#next">09 · R0.72K</a></li><li><a href="#claims">10 · 主张边界</a></li><li><a href="#reproduce">11 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "note toc")
    html = section(html, r'      <article>.*?</article>', ARTICLE, "note article")
    html = section(html, r'  <footer>.*?</footer>',
                   '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72J · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>',
                   "note footer")
    (PUBLIC / "notes" / "r0-72j.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72i.html").read_text(encoding="utf-8")
    changes = [
        ("R0.61–R0.72I｜R0.60 之后的研究回顾", "R0.61–R0.72J｜R0.60 之后的研究回顾"),
        ("R0.61 到 R0.72I 的 99 个研究节点", "R0.61 到 R0.72J 的 100 个研究节点"),
        ("二十五个阶段、99 个节点", "二十六个阶段、100 个节点"),
        ("最新一节分离了失败的正项吸收与真实完整根账本，并在全奇载波族上证明后者统一衰减。", "最新一节完成 gcd 约化 Cayley 图分类，并排除 common-band mixed-parity cubic 反族路线。"),
        ("physical absorption no-go 与 odd-carrier repair", "gcd-reduced graph classification 与 common-band cubic no-go"),
        ("/i18n-en.js?v=1.22", "/i18n-en.js?v=1.23"),
        ("累计回顾 · R0.61–R0.72I", "累计回顾 · R0.61–R0.72J"),
        ("<strong>R0.61–R0.72I</strong>", "<strong>R0.61–R0.72J</strong>"),
        ("收录节点：99", "收录节点：100"),
        ("回顾截止时公开笔记：159", "回顾截止时公开笔记：160"),
        ("回顾截止节点：R0.72I", "回顾截止节点：R0.72J"),
        ("01 · 二十五个研究阶段", "01 · 二十六个研究阶段"),
        ("02 · 99 节完整索引", "02 · 100 节完整索引"),
        ("<strong>99</strong><span>R0.61–R0.72I 研究节点</span>", "<strong>100</strong><span>R0.61–R0.72J 研究节点</span>"),
        ("<strong>61</strong><span>R0.70A–R0.72I 已公开版本</span>", "<strong>62</strong><span>R0.70A–R0.72J 已公开版本</span>"),
        ("<strong>37</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>38</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("<strong>25</strong><span>按问题划分的研究阶段</span>", "<strong>26</strong><span>按问题划分的研究阶段</span>"),
        ("后面的 99 个节点", "后面的 100 个节点"),
        ("R0.70A–R0.72I 的 61 个版本已经公开；其中 37 个", "R0.70A–R0.72J 的 62 个版本已经公开；其中 38 个"),
        ("R0.60 之后的路线分成二十五个阶段", "R0.60 之后的路线分成二十六个阶段"),
        ("R0.61–R0.72I 的 99 节公开笔记", "R0.61–R0.72J 的 100 节公开笔记"),
    ]
    for old, new in changes:
        if old not in html:
            raise RuntimeError(f"recap missing: {old}")
        html = html.replace(old, new)
    html = html.replace("完整物理" + "比值", "R0.72I complete-ledger 的物理归一化比值")
    phase_i = '<div class="links"><a href="/notes/r0-72i.html">R0.72I</a><a href="/figures/r0-72i-physical-absorption.pdf">R0.72I 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072i">R0.72I 证书</a></div></article>'
    phase_j = r'''
            <article class="phase"><h3>R0.72J · 约化 Cayley 图与真实 cubic no-go</h3>
              <p>令 \(g=\gcd(r_1,\ldots,r_M)\)。目标连通分支的 carrier Cayley 图二分，当且仅当所有约化载波 \(r_j/g\) 都是奇数。non-bipartite 只保证某条奇闭路；aligned launch 的 leading cubic 还要求第一球与第二球相交，即存在 \(s+t+u=0\) 的有符号三载波关系。</p>
              <p>共同频带 perturbative family 的 true cubic contribution 归一化比仍至多为 \(CR^{-4/9}(1+\log R)^{-2/3}\)。相干集合 \(S_R=\{R,\ldots,3R-1\}\) 有 \(T_R=3R(R+1)\) 个有序有符号三角，raw \(\mathcal C_{\times,R}\asymp R^2\)，其归一化比却按 \(R^{-2/3}\) 衰减。复目标的 complete-root Rolle 账本没有在本节闭合。</p>
              <div class="links"><a href="/notes/r0-72j.html">R0.72J</a><a href="/figures/r0-72j-mixed-parity-cubic.pdf">R0.72J 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072j">R0.72J 证书</a></div></article>'''
    html = once(html, phase_i, phase_i + phase_j, "recap J phase")
    node_i = '            <span class="node-ref"><a href="/notes/r0-72i.html">R0.72I</a><span class="node-state kind-closed">闭</span></span>\n'
    node_j = '            <span class="node-ref"><a href="/notes/r0-72j.html">R0.72J</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_i, node_i + node_j, "recap J node")
    kept = r'''            <li>R0.72J 的 gcd-reduced carrier theorem：目标 Cayley 图二分当且仅当所有约化载波为奇数；non-bipartite 不自动产生 cubic，leading return 需要三载波有符号关系。common-band aligned perturbative families 的 true cubic contribution 归一化比统一趋零；稠密相干块虽有 \(\mathcal C_{\times,R}\asymp R^2\)，仍不是 normalized counterfamily。complete complex-root ledger 保持开放。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", kept + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained J")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>图论分类已闭合，同频带 mixed-parity 反族路线被排除</h2>
          <p>截至 R0.72J，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 100 个节点或 62 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>本节把 parity repair 的适用范围精确扩大到 gcd 约化后全奇的 carrier sets，并证明 non-bipartite 与 leading cubic 之间还隔着 triangle relation。这个区分是可复用的结构结果。</p>
          <p>common-band 与 coherent dense block 都没有给出存活的 normalized cubic counterfamily。障碍已经转到多尺度、强耦合或 complex target complete-root mechanism。</p>
        </section>''', "recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72K 进入多尺度或强耦合，并单列 complex-root gate</h2>
          <p>下一步不再扩大同频带三角数。优先检查跨热时间尺度的 carrier triangles，或在完整能量与 critical-log action 重新结算后离开 perturbative coupling window。</p>
          <p>若目标保持复值，则 complete-root 结论必须先建立二维零点或相位锁定机制；不能直接复用实标量 Rolle 账本。</p>
        </section>''', "recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72J 的 62 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，38 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。</p>
          <p>R0.72J 的渐近 no-go 限于 exact triangular 2.5D common-band aligned perturbative families。它没有证明 arbitrary-carrier physical inequality，也没有证明一般三维 Navier–Stokes 的全局光滑性或有限时破裂；Clay 正式问题仍然开放。</p>
        </section>''', "recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72i.html">保留 R0.72I 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72j.html">打开最新节点 R0.72J</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072j">查看 R0.72J 双路证书</a> · <a href="/figures/r0-72j-mixed-parity-cubic.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72j.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72i.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>''', "recap reproduce")
    html = once(html, "R0.61–R0.72I 回顾 · 2026-08-27", "R0.61–R0.72J 回顾 · 2026-08-27", "recap footer")
    (PUBLIC / "recap-r0-61-r0-72j.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    if 'data-site-version="1.23"' in html:
        old_rate = r"\(CR^{-4/9}(\log R)^{-2/3}\)"
        new_rate = r"\(CR^{-4/9}(1+\log R)^{-2/3}\)"
        if old_rate in html:
            html = once(html, old_rate, new_rate, "home exact common-band rate")
        elif new_rate not in html:
            raise RuntimeError("home missing exact common-band rate")
        path.write_text(html, encoding="utf-8")
        return
    changes = [
        ('data-site-version="1.22"', 'data-site-version="1.23"'),
        ("/i18n-en.js?v=1.22", "/i18n-en.js?v=1.23"),
        ("/site-refresh.js?v=1.22", "/site-refresh.js?v=1.23"),
        ("/recap-r0-61-r0-72i", "/recap-r0-61-r0-72j"),
        ("<strong>v1.22</strong>网页版本", "<strong>v1.23</strong>网页版本"),
        ("<strong>159</strong>公开研究笔记", "<strong>160</strong>公开研究笔记"),
        ("<strong>R0.72I</strong>最新研究节点", "<strong>R0.72J</strong>最新研究节点"),
        ("<strong>mixed-parity cubic interaction</strong>当前方向", "<strong>multi-scale / strong-coupling complex-root gate</strong>当前方向"),
        ("Research topology · R0.1–R0.72I", "Research topology · R0.1–R0.72J"),
        ("R0.70A–R0.72I：61 节已公开，37 节完整封存", "R0.70A–R0.72J：62 节已公开，38 节完整封存"),
        ("R0.69P–R0.72I", "R0.69P–R0.72J"),
        ("展开 69 篇公开笔记", "展开 70 篇公开笔记"),
        ("综述 v1.22 · 2026-08-27", "综述 v1.23 · 2026-08-27"),
        ("上次综述 v1.21 · 2026-08-27", "上次综述 v1.22 · 2026-08-27"),
    ]
    for old, new in changes:
        if old not in html:
            raise RuntimeError(f"home missing: {old}")
        html = html.replace(old, new)
    html = html.replace("完整物理" + "比值", "R0.72I complete-ledger 的物理归一化比值")
    html = once(html, "R0.72I 已证明分离的 B_AQ_* 正项不能逐项物理吸收，但同一全奇载波族的真实 complete ledger 在 critical-log normalization 下统一衰减；下一步只审 mixed-parity 的真实 cubic row。", "R0.72J 已完成 gcd 约化 Cayley 图分类，并证明 non-bipartite 不等于 leading cubic；common-band coherent mixed-parity 族虽有 raw cubic 增长，true cubic contribution 的归一化比仍衰减。", "home summary")
    html = once(html, "从多载波 mixed-row 行级封闭走到物理吸收 no-go 与 parity repair", "从 parity repair 走到 gcd-reduced graph classification 与 cubic no-go", "home route title")
    html = once(html, r"R0.72I 逐项换回物理量，证明分离的 \(B_AQ_*\) 项不能统一吸收；joint exposure 与 odd-carrier parity 又证明真实 complete ledger 统一衰减。</p>", r"R0.72I 逐项换回物理量，证明分离的 \(B_AQ_*\) 项不能统一吸收；joint exposure 与 odd-carrier parity 又证明真实 complete ledger 统一衰减。R0.72J 把 parity 修复提升为 gcd-reduced Cayley 图二分定理，区分 odd cycle 与 triangle return，并排除 common-band coherent cubic 反族。</p>", "home J route prose")
    html = once(html, "termwise physical-absorption no-go → parity repair</p>", "termwise physical-absorption no-go → parity repair → gcd-reduced Cayley classification → triangle-return criterion → common-band cubic no-go</p>", "home route path")
    nav_i = '                  <a class="milestone" href="/notes/r0-72i.html">R0.72I</a>\n'
    html = once(html, nav_i, nav_i + '                  <a class="milestone" href="/notes/r0-72j.html">R0.72J</a>\n', "home J nav")
    html = section(html, r'            <article class="tree-node next">.*?</article>', r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72K</span><span class="tree-state current">下一检查点</span></div>
              <h3>multi-scale or strong-coupling / complex-root gate</h3>
              <p>检查跨多个热时间尺度的 carrier triangles，或在完整能量与 critical-log action 下进入强耦合；若目标保持复值，先建立不依赖实 Rolle 符号交替的 complete-root mechanism。</p>
            </article>''', "home next")
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72J · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 100 个节点；全站现有 160 篇公开研究笔记</h3>
            <p>累计回顾现在分为二十六个问题阶段，完整覆盖 R0.61–R0.72J。R0.72E 排除 unweighted payment，R0.72F 选出 critical-log 修正，R0.72G 封闭 one-carrier complete roots，R0.72H 封闭 finite multi-carrier mixed row，R0.72I 分离失败的正项吸收与真实 parity ledger，R0.72J 再完成 gcd-reduced graph classification 与 common-band cubic no-go。R0.70A–R0.72J 共 62 个版本已公开；38 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;同频带增加 carrier triangles 不能产生存活的 normalized cubic counterfamily；下一障碍是多尺度、强耦合或 complex-root ledger。</p>
            <p><a href="/recap-r0-61-r0-72j.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72j.pdf">下载同步 PDF</a></p>
          </div>''', "home recap")
    old_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72J：</strong>&nbsp;检查 mixed-parity carrier graph 的真实 cubic interaction，寻找 hybrid payment 或 actual normalized counterfamily。</p>
          </div>
        </section>'''
    new_tail = r'''            <p><strong style="color:var(--gold)">R0.72J 已完成：</strong>&nbsp;gcd 约化 Cayley 图的二分性已精确分类；non-bipartite 不自动产生 cubic，common-band coherent family 的 true cubic contribution 归一化比仍衰减。</p>
          </div>

          <div class="task-one" id="r072j" data-release="r072j" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72J · 2026-08-27</p>
            <h3>非二分图、三角返回和物理反族是三道不同的门</h3>
            <p>令 \(g=\gcd(r_1,\ldots,r_M)\)。carrier Cayley 图二分当且仅当所有 \(r_j/g\) 为奇数。离开二分情形只保证奇闭路；aligned launch 的 leading \(P_0V^2F\) 还需要 \(s+t+u=0\) 的三载波关系。</p>
            <p>相干集合 \(S_R=\{R,\ldots,3R-1\}\) 有 \(3R(R+1)\) 个有序有符号三角，raw \(\mathcal C_{\times,R}\asymp R^2\)；true cubic contribution 的归一化比仍按 \(R^{-2/3}\) 衰减。更一般的 common-band perturbative 上界为 \(CR^{-4/9}(1+\log R)^{-2/3}\)。</p>
            <p><strong>结论边界：</strong>&nbsp;mixed-parity 目标一般是复值，实 Rolle complete-root 账本没有在本节闭合。一般三维正则性仍然开放。</p>
            <p><a href="/notes/r0-72j.html"><strong>阅读 R0.72J 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72j.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72j-mixed-parity-cubic.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072j">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072j_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072j-mixed-parity-cubic/fig-r072j-mixed-parity-cubic">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72j.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72j.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72K：</strong>&nbsp;检查 multi-scale triangles、strong-coupling physical ledger，或 complex target complete-root mechanism。</p>
          </div>
        </section>'''
    html = once(html, old_tail, new_tail, "home J card")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    if "/i18n-en.js?v=1.23" in html:
        return
    html = html.replace("/recap-r0-61-r0-72i", "/recap-r0-61-r0-72j")
    for old, new in [
        ("/i18n-en.js?v=1.22", "/i18n-en.js?v=1.23"),
        ("文献综述 v1.22 · 2026-08-27", "文献综述 v1.23 · 2026-08-27"),
        ("本站 R0.69P–R0.72I 只列为研究笔记", "本站 R0.69P–R0.72J 只列为研究笔记"),
        ("累计回顾与 99 节索引", "累计回顾与 100 节索引"),
        ("打开 99 节完整索引", "打开 100 节完整索引"),
    ]:
        if old not in html:
            raise RuntimeError(f"literature missing: {old}")
        html = html.replace(old, new)
    html = once(html, r"R0.72I 证明分离的 \(B_AQ_*\) 正项不能逐项物理吸收，同时用 joint exposure 和 odd-carrier parity 证明真实 complete ledger 统一衰减。一般 Navier–Stokes 正则性仍开放。</p>", r"R0.72I 证明分离的 \(B_AQ_*\) 正项不能逐项物理吸收，同时用 joint exposure 和 odd-carrier parity 证明真实 complete ledger 统一衰减。R0.72J 完成 gcd-reduced Cayley graph 的二分分类，区分 odd cycle 与 triangle return，并证明 common-band coherent mixed-parity cubic 在物理归一化后仍衰减。一般 Navier–Stokes 正则性仍开放。</p>", "literature J route")
    open_j = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72J</b><strong>mixed-parity cubic interaction</strong></header><p>直接检查 \(|\delta|\int|hP_0V^2F|\) 的 carrier graph、hybrid payment 与 actual normalized counterfamily。</p></div>'''
    closed_j = r'''              <div class="route-step closed"><header><b>R0.72J</b><strong>gcd-reduced graph classification 与 common-band cubic no-go</strong></header><p>目标 carrier Cayley 图二分当且仅当所有约化载波为奇数；non-bipartite 不等于 triangle return。相干稠密块虽有 raw \(\mathcal C_{\times,R}\asymp R^2\)，true cubic contribution 的归一化比仍衰减。<a href="/notes/r0-72j.html">研究笔记</a> <a href="/recap-r0-61-r0-72j.html">当前累计回顾</a> <a href="#r072j-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72K</b><strong>multi-scale / strong-coupling or complex-root gate</strong></header><p>检查跨热时间尺度的 triangles、完整强耦合账本，或不依赖实 Rolle 符号交替的 complex target complete-root mechanism。</p></div>'''
    html = once(html, open_j, closed_j, "literature J cards")
    boundary_i = r'''<div class="boundary"><strong>R0.72I 的主源边界</strong><p>限定一手来源检索未发现同时给出 carrier-uniform \(B_A\) absorption、endogenous complete-root sampling 和 all-odd parity repair 的定理。本节只证明 exact triangular 2.5D class 内的 method obstruction 与 special-family repair；这是 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p></div>'''
    boundary_j = r'''

          <h3 id="r072j-boundary">R0.72J 的 Cayley graph、additive triangle 与 root 边界</h3>
          <p><a href="https://arxiv.org/abs/2411.19428">Árnadóttir–Gordeev–Lato–Randrianarisoa–Vermant</a> 的 Cayley graph homomorphism criterion 支持 gcd 约化后的二分分类；它不区分目标 row 的长度三返回与更长奇闭路。真实 cubic 返回由 \(R_1(0)\cap R_2(0)\) 决定，等价于三载波有符号关系。</p>
          <p><a href="https://arxiv.org/abs/math/0307142">Green–Ruzsa</a> 给出 sum-free sets 的标准语言，但不估计带相位、热权和物理 lift 的 signed convolution。<a href="https://arxiv.org/abs/1905.01374">Carbonaro–Dragičević</a>、<a href="https://arxiv.org/abs/2101.11694">Carbonaro–Dragičević–Kovač–Škreb</a> 与 <a href="https://arxiv.org/abs/1204.5082">Mei</a> 提供相邻的 bilinear、trilinear 和 semigroup Carleson 框架；它们不直接给出 endogenous \(h=P_0VF\)、\(b=P_0V^2F\) 的 joint exposure 或 complex-root ledger。</p>
          <div class="boundary"><strong>R0.72J 的主张边界</strong><p>本节的 graph classification 是精确离散定理；物理 no-go 只覆盖声明的 common-band aligned perturbative families。限定检索没有发现把这些三项直接组合成 arbitrary-carrier complete-root theorem 的来源；这是 bounded non-collision check，不是原创性、优先权或一般 NSE 结论。</p></div>'''
    html = once(html, boundary_i, boundary_i + boundary_j, "literature J boundary")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    count = len(list((PUBLIC / "notes").glob("*.html")))
    if count != 160:
        raise RuntimeError(f"expected 160 public HTML notes, found {count}")
    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({"latestCompletedRelease": "r072j", "siteVersion": "1.23",
                    "publicHtmlNoteCount": count, "postR060RecapNodeCount": 100,
                    "nextRelease": "r072k",
                    "latestReleaseGate": "tests/r072j-mixed-parity-gate.test.mjs",
                    "postR070APublishedReleaseCount": 62,
                    "postR070AFormalSealedReleaseCount": 38,
                    "legacyFormalFigureBacklogCount": 24})
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.23", "latestRelease": "R0.72J", "publicHtmlNoteCount": count})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update({"latestPublishedRelease": "r072j", "publishedReleaseCount": 62,
                      "formalSealedReleaseCount": 38, "legacyFormalFigureBacklogCount": 24})
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072j" not in inventory[key]:
            inventory[key].append("r072j")
    if len(inventory["legacyFormalFigureBacklog"]) != 24:
        raise RuntimeError("legacy formal-figure backlog changed unexpectedly")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    print(json.dumps({"release": "R0.72J", "siteVersion": "1.23", "notes": 160,
                      "recapNodes": 100, "published": 62, "formalSealed": 38,
                      "legacyBacklog": 24}, ensure_ascii=False))


if __name__ == "__main__":
    main()
