#!/usr/bin/env python3
"""Generate the deterministic R0.72K GitHub Pages release from site v1.23."""

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


HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72K · DIRECTIONAL ZERO SAMPLING · COMPLEX ROOT LEDGER</div>
        <h1>复轨道不需要复 Rolle；<br>每个根隙只需要自己的实方向</h1>
        <p class="lead">R0.72J 已经控制 mixed row 与 true cubic，却没有把复值目标的全部时间根装进一个账本。我在每个相邻根隙末端选择导数的 norming functional；它的实投影在该根隙上的平均值为零，因此可以用一次实中值论证支付右端根斜率。这个方向随根隙改变，不要求复导数本身消失，也不要求统一相位、根分离或根数上界。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72K 定理完成</span><strong>directional sampling closes the complex ledger</strong><p>版本 v0.72K · 2026-08-27</p><p>directional root-slope packing: CLOSED</p><p>factor two and first-root boundary: SHARP</p><p>complete complex-target ledger: CLOSED</p><p>common-band physical counterfamily: NO-GO</p><p>一般三维正则性：OPEN</p></div>
    </div></header>'''


ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Four decisions</div><h2>复 Rolle 是假的，但完整复目标根账本仍可闭合</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · DIRECTIONAL SAMPLING</strong><p>对实或复 Banach 空间中的 \(X\in W^{2,1}(I;B)\)，除第一个所选根外，全部根上的导数平方质量由 \(2\int_I\|X'\|\|X''\|\) 支付。</p></div>
            <div class="verdict-card true"><strong>SHARP · FACTOR TWO</strong><p>长浅负平台接短斜坡的标量族使比值趋于一，所以系数 2 在声明的正则性类中不能减小；单根仿射函数又说明首根付款不能删除。</p></div>
            <div class="verdict-card true"><strong>THEOREM · COMPLETE COMPLEX LEDGER</strong><p>对任意有限 triangular carrier set 和 \(\delta\ne0\)，完整扩展根质量由首根、mixed row 与 true cubic 三项统一控制，不再要求固定实 gauge。</p></div>
            <div class="verdict-card false"><strong>NO-GO · COMMON BAND</strong><p>声明的 perturbative common-band class 中，完整复根账本虽为 \(a^2N^2\) 量级，物理 critical-log 归一化后仍一致趋零。</p></div>
          </div>
        </section>

        <section id="direction"><div class="section-no">01 / Directional root-gap theorem</div><h2>每个根隙单独选择右端导数的 norming direction</h2>
          <p>设 \(t_1&lt;\cdots&lt;t_m\) 且 \(X(t_j)=0\)。对每个 \(j\ge2\)，用 Hahn–Banach 选择 \(\ell_j\in B^*\)，使 \(\|\ell_j\|=1\) 且 \(\ell_j(X'(t_j))=\|X'(t_j)\|_B&gt;0\)。复情形只需乘一个单位相位。</p>
          <div class="equation result">\[
            \boxed{\sum_{j=2}^{m}\|X'(t_j)\|_B^2
            \le 2\int_I\|X'(t)\|_B\,\|X''(t)\|_B\,dt.}
          \]</div>
          <p>这个结论与根数和最小间距无关。对任意根集，以有限子集上确界定义 extended nonnegative sum；首个所选根可由 \(\sup_{X(t)=0}\|X'(t)\|_B^2\) 统一支付，若根集有最小元则可固定支付该根。</p>
        </section>

        <section id="proof"><div class="section-no">02 / One real projection per gap</div><h2>零平均的是方向投影，不是复导数</h2>
          <p>令 \(\phi_j(t)=\operatorname{Re}\ell_j(X'(t))\)。相邻端点都是根，因此</p>
          <div class="equation result">\[
            \int_{t_{j-1}}^{t_j}\phi_j(t)\,dt
            =\operatorname{Re}\ell_j[X(t_j)-X(t_{j-1})]=0.
          \]</div>
          <p>连续实函数 \(\phi_j\) 在根隙内至少有一个零点 \(c_j\)。从 \(c_j\) 积分到右端并使用链式法则，就得到该根隙的系数 2 估计。不同根隙互不重叠，所以可以直接求和。</p>
          <p>反例 \(X(t)=e^{2\pi it}-1\) 的导数从不为零，说明 literal complex Rolle 不成立；本节没有声称它成立。</p>
        </section>

        <section id="sharp"><div class="section-no">03 / Sharpness and count boundary</div><h2>系数 2、首根付款和“质量不等于根数”都有独立边界</h2>
          <p>连续分段线性导数的 plateau–ramp family 满足两端同为根，并使</p>
          <div class="equation result">\[
            \int_0^1|X_\epsilon'||X_\epsilon''|\,dt
            =\frac{1+\epsilon^2}{2}\longrightarrow\frac12,
            \qquad |X_\epsilon'(1)|=1.
          \]</div>
          <p>\(X(t)=t\) 在零点有单位斜率而 \(X''=0\)，所以首个所选根必须另付。另一方面，\(N^{-3}(e^{2\pi iNt}-1)\) 可以有 \(N+1\) 个根而总斜率平方质量趋零；定理控制的是 derivative mass，不是 raw root count。</p>
        </section>

        <section id="triangular"><div class="section-no">04 / Exact triangular lift</div><h2>积分因子把根隙付款准确送到 mixed row 与 true cubic</h2>
          <p>triangular target 的两个精确行方程为</p>
          <div class="equation result">\[
            F_0'+\lambda_0F_0=\delta h,
            \qquad h'+\lambda_0h=QF+\delta b,
            \qquad b=P_0V^2F.
          \]</div>
          <p>对 \(X_0(x)=e^{\lambda_0(x-A)}F_0(x)\) 应用方向定理。因为根隙内 \(x\le\tau_j\)，反向指数核不超过一。对所有有限根子集取上确界后得到</p>
          <div class="equation result">\[
            \boxed{G_{\rm all}^{\rm ex}(I)
            \le E_A\rho_A^2+2\mathcal E_Q(I)+2\mathcal C_\times(I).}
          \]</div>
          <p>这里 \(\mathcal E_Q=\int_I|hQF|\)，\(\mathcal C_\times=|\delta|\int_I|hP_0V^2F|\)。结论不使用 root count、root separation、复解析锚点或统一相位；\(\delta=0\) 不在定理量词内。</p>
        </section>

        <section id="band"><div class="section-no">05 / Complete common-band theorem</div><h2>此前的 continuous-row 上界现在覆盖全部复根</h2>
          <p>代入 R0.72H 的 mixed-row payment 和 R0.72J 的 true-cubic minimum，可得 carrier-count-independent finite-row corollary。对 common-band aligned perturbative family，单个已构造复根给下界，而新定理给匹配上界：</p>
          <div class="equation result">\[
            \boxed{G_{\rm all}^{\rm ex}\asymp a^2N^2,
            \qquad \mathcal J_{\rm all}\asymp\frac{g^2N}{R^2}.}
          \]</div>
          <p>因此未枚举的其他复根也必须装进同一个 \(a^2N^2\) 预算；这不是通过假设根数有限得到的。</p>
        </section>

        <section id="physical"><div class="section-no">06 / Full physical normalization</div><h2>完整根账本没有在 critical-log 尺度上存活</h2>
          <div class="equation result">\[
            \boxed{\frac{\mathcal J_{\rm all}}
            {D^{1/3}\Lambda_{1,*}}
            \le CR^{-4/9}(1+\log R)^{-2/3}\longrightarrow0.}
          \]</div>
          <p>对 R0.72J 的相干 mixed-parity block，完整 raw root mass 为 \(R^2\) 量级、物理 root ledger 为 \(R\) 量级，归一化比仍为 \(R^{-2/3}\)。因此 cubic no-go 后面没有隐藏一批失控的复根。</p>
        </section>

        <section id="audit"><div class="section-no">07 / Producer and independent audit</div><h2>抽象方向恒等式和继承账本由两条实现核对</h2>
          <div class="audit-grid">
            <div class="audit-card"><strong>PRODUCER · ARCHIVED PASS</strong><p>生产路线核对 plateau–ramp sharpness、复圆周曲线、方向零点、R0.72J lineage hash，以及 complete-root measured/theorem ledgers。</p><p class="mini-kpi">analytic theorem first · finite corroboration only</p></div>
            <div class="audit-card"><strong>INDEPENDENT · ARCHIVED PASS</strong><p>独立路线改用不同 sharpness 参数和复二维 Hilbert 曲线，并从独立 R0.72J 行数据重建物理账本；它不导入生产代码或结果。</p><p class="mini-kpi"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_independent_audit.md">独立逐式审计</a></p></div>
          </div>
          <p>有限计算不枚举完整复根集，也不证明渐近率。证明来自方向采样引理、精确目标行和已经封闭的 continuous-row estimates。</p>
        </section>

        <section id="figure"><div class="section-no">08 / Journal figure</div><h2>正式附图分开展示方向投影、sharpness 与完整物理衰减</h2>
          <p><img src="/figures/r0-72k-directional-roots.svg" alt="R0.72K directional zero sampling and complete complex-root ledger formal figure"></p>
          <p><a href="/figures/r0-72k-directional-roots.pdf">下载 PDF</a> · <a href="/figures/r0-72k-directional-roots.png">下载 PNG</a> · <a href="/figures/r0-72k-directional-roots.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">09 / Research value</div><h2>关闭的是一个真正的量词缺口，而不是把复目标强行实化</h2>
          <p>R0.72J 只控制 continuous cubic row，不能据此声称全部 complex roots 已被支付。本节提供一个 root-count-independent 抽象引理，并把它精确接到 triangular row equations，所以 complete-root 结论现在覆盖任意物理相位。</p>
          <p>这个结果把 common-band 反族路线从“单个复根与 cubic 被控制”提升为“完整复根账本被控制”。它仍不触及多尺度 heat windows 或 strong coupling。</p>
        </section>

        <section id="next"><div class="section-no">10 / Next gate</div><h2>R0.72L：离开 perturbative common band，先检查 strong coupling</h2>
          <p>方向采样本身已经与 carrier 数和根数解耦。下一节应检查 continuous-row bounds 在 \(gB/R^2\not\ll1\) 时是否仍能由完整能量与 critical-log action 支付；若 strong coupling 不闭合，再进入 separated heat windows 的 multiscale sum。</p>
        </section>

        <section id="claims"><div class="section-no">11 / Claim boundary</div><h2>一般 Navier–Stokes 问题仍然开放</h2>
          <p>Banach-valued directional lemma 是抽象解析定理；complete-root consequence 限于 exact finite triangular 2.5D class，common-band no-go 还要求 row alignment、heat-stable multiplier 与 \(gB/R^2\le\gamma_0\)。</p>
          <p>本节没有证明 multiscale 或 strong-coupling physical inequality，没有给出一般三维 Navier–Stokes 的新继续性判据，没有构造有限时奇性，也没有证明全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="reproduce"><div class="section-no">12 / Reproduction</div><h2>报告、双路证书、附图与累计回顾</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_independent_audit.md">独立审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072k">双路机器证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072k-directional-roots/fig-r072k-directional-roots">正式附图包</a> · <a href="/notes/r0-72k.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72k.html">累计回顾</a> · <a href="/recap-r0-61-r0-72k.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


def build_note() -> None:
    html = (PUBLIC / "notes" / "r0-72j.html").read_text(encoding="utf-8")
    html = section(html, r'<meta name="description" content=".*?">',
                   '<meta name="description" content="研究笔记 R0.72K：方向零点采样引理把 real/complex Banach-valued roots 的导数质量装入零计数无关的连续账本，并闭合 finite triangular class 的 complete complex-target root ledger。">', "note description")
    html = section(html, r'<meta property="og:title" content=".*?">',
                   '<meta property="og:title" content="R0.72K｜每个复根隙只需要自己的实方向">', "note og title")
    html = section(html, r'<meta property="og:description" content=".*?">',
                   '<meta property="og:description" content="方向投影替代 literal complex Rolle；完整 common-band complex-root ledger 在物理 critical-log 归一化后仍衰减。">', "note og description")
    html = section(html, r'<meta property="og:image" content=".*?">',
                   '<meta property="og:image" content="https://kasifa.github.io/figures/r0-72k-directional-roots.png">', "note og image")
    html = section(html, r'<title>.*?</title>', '<title>R0.72K｜每个复根隙只需要自己的实方向</title>', "note title")
    html = required(html, "/i18n-en.js?v=1.23", "/i18n-en.js?v=1.24", "note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#direction">方向定理</a><a href="#proof">证明</a><a href="#sharp">尖锐性</a><a href="#triangular">目标行</a><a href="#band">共同频带</a><a href="#physical">物理尺度</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "note nav")
    html = section(html, r'    <header class="hero">.*?</header>', HERO, "note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 四句判断</a></li><li><a href="#direction">01 · 方向根隙定理</a></li><li><a href="#proof">02 · 实投影证明</a></li><li><a href="#sharp">03 · 尖锐边界</a></li><li><a href="#triangular">04 · triangular lift</a></li><li><a href="#band">05 · complete common band</a></li><li><a href="#physical">06 · 物理归一化</a></li><li><a href="#audit">07 · 双路审计</a></li><li><a href="#figure">08 · 正式附图</a></li><li><a href="#value">09 · 研究价值</a></li><li><a href="#next">10 · R0.72L</a></li><li><a href="#claims">11 · 主张边界</a></li><li><a href="#reproduce">12 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "note toc")
    html = section(html, r'      <article>.*?</article>', ARTICLE, "note article")
    html = section(html, r'<footer>.*?</footer>',
                   '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72K · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>',
                   "note footer")
    (PUBLIC / "notes" / "r0-72k.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72j.html").read_text(encoding="utf-8")
    changes = [
        ("R0.61 到 R0.72J 的 100 个研究节点", "R0.61 到 R0.72K 的 101 个研究节点"),
        ("二十六个阶段、100 个节点", "二十七个阶段、101 个节点"),
        ("gcd-reduced graph classification 与 common-band cubic no-go", "directional zero sampling 与 complete complex-root ledger"),
        ("/i18n-en.js?v=1.23", "/i18n-en.js?v=1.24"),
        ("收录节点：100", "收录节点：101"),
        ("回顾截止时公开笔记：160", "回顾截止时公开笔记：161"),
        ("回顾截止节点：R0.72J", "回顾截止节点：R0.72K"),
        ("01 · 二十六个研究阶段", "01 · 二十七个研究阶段"),
        ("02 · 100 节完整索引", "02 · 101 节完整索引"),
        ("<strong>100</strong><span>R0.61–R0.72J 研究节点</span>", "<strong>101</strong><span>R0.61–R0.72K 研究节点</span>"),
        ("<strong>62</strong><span>R0.70A–R0.72J 已公开版本</span>", "<strong>63</strong><span>R0.70A–R0.72K 已公开版本</span>"),
        ("<strong>38</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>39</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("<strong>26</strong><span>按问题划分的研究阶段</span>", "<strong>27</strong><span>按问题划分的研究阶段</span>"),
        ("后面的 100 个节点", "后面的 101 个节点"),
        ("R0.70A–R0.72J 的 62 个版本已经公开；其中 38 个", "R0.70A–R0.72K 的 63 个版本已经公开；其中 39 个"),
        ("R0.60 之后的路线分成二十六个阶段", "R0.60 之后的路线分成二十七个阶段"),
        ("R0.61–R0.72J 的 100 节公开笔记", "R0.61–R0.72K 的 101 节公开笔记"),
        ("R0.61–R0.72J", "R0.61–R0.72K"),
        ("/recap-r0-61-r0-72j", "/recap-r0-61-r0-72k"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"recap {old}")
    html = once(
        html,
        "      body{font-size:8.6pt;line-height:1.52}\n",
        "      body{font-size:8.6pt;line-height:1.52}\n"
        "      #retained li{margin:.14rem 0;line-height:1.4}\n",
        "recap print retained density",
    )
    html = section(html, r'<meta name="description" content=".*?">',
                   '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72K 的 101 个研究节点；最新一节以 directional zero sampling 闭合 complete complex-target root ledger。">', "recap description")
    html = section(html, r'<meta property="og:description" content=".*?">',
                   '<meta property="og:description" content="二十七个阶段、101 个节点：从约化递推和时间迹账本，到 critical-log candidate，再到 complete complex-target root ledger。">', "recap og description")
    phase_j_end = '<div class="links"><a href="/notes/r0-72j.html">R0.72J</a><a href="/figures/r0-72j-mixed-parity-cubic.pdf">R0.72J 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072j">R0.72J 证书</a></div></article>'
    phase_k = r'''
            <article class="phase"><h3>R0.72K · 方向零点采样与完整复目标根账本</h3>
              <p>我没有把 complex Rolle 当作前提。对每个相邻根隙，我在右端导数方向上选一个 norming functional；其实值投影的平均值为零，因此 \(\sum_{j=2}^m\|X'(t_j)\|^2\le2\int\|X'\|\|X''\|\)。系数 2 在 \(W^{2,1}\) 类中尖锐，首个所选根必须另付。</p>
              <p>把引理用于 \(e^{\lambda_0(x-A)}F_0\)，得到 \(G_{\rm all}^{\rm ex}\le E_A\rho_A^2+2\mathcal E_Q+2\mathcal C_\times\)。common-band mixed-parity class 中 \(G_{\rm all}^{\rm ex}\asymp a^2N^2\)、\(\mathcal J_{\rm all}\asymp g^2N/R^2\)，完整物理归一化比仍至多为 \(CR^{-4/9}(1+\log R)^{-2/3}\)。</p>
              <div class="links"><a href="/notes/r0-72k.html">R0.72K</a><a href="/figures/r0-72k-directional-roots.pdf">R0.72K 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072k">R0.72K 证书</a></div></article>'''
    html = once(html, phase_j_end, phase_j_end + phase_k, "recap K phase")
    node_j = '            <span class="node-ref"><a href="/notes/r0-72j.html">R0.72J</a><span class="node-state kind-closed">闭</span></span>\n'
    node_k = '            <span class="node-ref"><a href="/notes/r0-72k.html">R0.72K</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_j, node_j + node_k, "recap K node")
    kept = r'''            <li>R0.72K 的 directional root-slope theorem：对实或复 Banach-valued \(W^{2,1}\) 曲线，每个根隙使用自己的 norming direction，全部右端根的 derivative mass 由 \(2\int\|X'\|\|X''\|\) 支付；系数 2 尖锐，首根项必要。这个引理把 R0.72H–J 的 continuous-row bounds 升级成 complete complex-target ledger，并在 common band 内给出统一物理衰减。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", kept + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained K")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>复目标根的量词缺口已经闭合，common-band 完整反族路线被排除</h2>
          <p>截至 R0.72K，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 101 个节点或 63 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>新的可复用结果是 zero-count-independent directional derivative-mass theorem。它不依赖复导数零点，并把 finite triangular class 的 mixed row 与 true cubic 付款扩展到全部 complex target roots。</p>
          <p>common-band coherent block 的完整根账本没有存活。下一障碍是 strong coupling；multiscale separated heat windows 保留为并列后续接口。</p>
        </section>''', "recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72L 先检查 strong coupling 的 continuous-row ledger</h2>
          <p>方向采样已经脱离根数和 carrier 数。下一步应测试 \(gB/R^2\not\ll1\) 时，mixed row 与 true cubic 是否仍能由完整能量和 critical-log action 支付。</p>
          <p>若 strong coupling 不能闭合，再把 joint heat exposure 展开到多个 separated shells；不能把 common-band 结论直接外推到多尺度。</p>
        </section>''', "recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72K 的 63 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，39 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。</p>
          <p>R0.72K 的 complete-root theorem 限于 exact finite triangular 2.5D class；物理 no-go 还限于 perturbative common-band assumptions。它没有证明 multiscale、strong coupling 或一般三维 Navier–Stokes 的全局光滑性；Clay 正式问题仍然开放。</p>
        </section>''', "recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72j.html">保留 R0.72J 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72k.html">打开最新节点 R0.72K</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072k">查看 R0.72K 双路证书</a> · <a href="/figures/r0-72k-directional-roots.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72k.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72j.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>''', "recap reproduce")
    (PUBLIC / "recap-r0-61-r0-72k.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    if 'data-site-version="1.24"' in html:
        return
    changes = [
        ('data-site-version="1.23"', 'data-site-version="1.24"'),
        ("/i18n-en.js?v=1.23", "/i18n-en.js?v=1.24"),
        ("/site-refresh.js?v=1.23", "/site-refresh.js?v=1.24"),
        ("/recap-r0-61-r0-72j", "/recap-r0-61-r0-72k"),
        ("<strong>v1.23</strong>网页版本", "<strong>v1.24</strong>网页版本"),
        ("<strong>160</strong>公开研究笔记", "<strong>161</strong>公开研究笔记"),
        ("<strong>R0.72J</strong>最新研究节点", "<strong>R0.72K</strong>最新研究节点"),
        ("<strong>multi-scale / strong-coupling complex-root gate</strong>当前方向", "<strong>strong-coupling continuous-row ledger</strong>当前方向"),
        ("Research topology · R0.1–R0.72J", "Research topology · R0.1–R0.72K"),
        ("R0.70A–R0.72J：62 节已公开，38 节完整封存", "R0.70A–R0.72K：63 节已公开，39 节完整封存"),
        ("R0.69P–R0.72J", "R0.69P–R0.72K"),
        ("展开 70 篇公开笔记", "展开 71 篇公开笔记"),
        ("综述 v1.23 · 2026-08-27", "综述 v1.24 · 2026-08-27"),
        ("上次综述 v1.22 · 2026-08-27", "上次综述 v1.23 · 2026-08-27"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"home {old}")
    html = once(html,
        "R0.72J 已完成 gcd 约化 Cayley 图分类，并证明 non-bipartite 不等于 leading cubic；common-band coherent mixed-parity 族虽有 raw cubic 增长，true cubic contribution 的归一化比仍衰减。",
        r"R0.72K 已用逐根隙 directional projection 闭合 complete complex-target ledger；common-band 完整根质量虽为 \(a^2N^2\) 量级，物理 critical-log 归一化后仍统一衰减。", "home summary")
    html = once(html, "从 parity repair 走到 gcd-reduced graph classification 与 cubic no-go", "从 cubic no-go 走到 directional sampling 与 complete complex-root closure", "home route title")
    html = once(html,
        r"R0.72J 把 parity 修复提升为 gcd-reduced Cayley 图二分定理，区分 odd cycle 与 triangle return，并排除 common-band coherent cubic 反族。</p>",
        r"R0.72J 把 parity 修复提升为 gcd-reduced Cayley 图二分定理，区分 odd cycle 与 triangle return，并排除 common-band coherent cubic 反族。R0.72K 再对每个复根隙选择独立 norming direction，把 mixed row 与 true cubic 转成 complete complex-target ledger，并证明其 common-band 物理归一化比统一衰减。</p>", "home K route prose")
    html = once(html, "common-band cubic no-go</p>", "common-band cubic no-go → directional zero sampling → complete complex-root ledger</p>", "home route path")
    nav_j = '                  <a class="milestone" href="/notes/r0-72j.html">R0.72J</a>\n'
    html = once(html, nav_j, nav_j + '                  <a class="milestone" href="/notes/r0-72k.html">R0.72K</a>\n', "home K nav")
    html = section(html, r'            <article class="tree-node next">.*?</article>', r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72L</span><span class="tree-state current">下一检查点</span></div>
              <h3>strong-coupling continuous-row ledger</h3>
              <p>离开 \(gB/R^2\le\gamma_0\) 的 perturbative window，检查 mixed row 与 true cubic 能否继续由完整能量和 critical-log action 支付；multiscale separated heat windows 保留为并列后续接口。</p>
            </article>''', "home next")
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72K · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 101 个节点；全站现有 161 篇公开研究笔记</h3>
            <p>累计回顾现在分为二十七个问题阶段，完整覆盖 R0.61–R0.72K。我保留了 R0.72E 的 unweighted-payment no-go、R0.72F 的 critical-log boundary、R0.72G–J 的 finite-carrier root/cubic 路线，并追加 R0.72K 的 directional zero sampling 与 complete complex-target ledger。R0.70A–R0.72K 共 63 个版本已公开；39 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;common-band 完整复根账本已经闭合并统一衰减；下一障碍是 strong coupling，随后才是 multiscale heat-window summation。</p>
            <p><a href="/recap-r0-61-r0-72k.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72k.pdf">下载同步 PDF</a></p>
          </div>''', "home recap")
    old_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72K：</strong>&nbsp;检查 multi-scale triangles、strong-coupling physical ledger，或 complex target complete-root mechanism。</p>
          </div>
        </section>'''
    new_tail = r'''            <p><strong style="color:var(--gold)">R0.72K 已完成：</strong>&nbsp;方向零点采样闭合 complete complex-target ledger；common-band 完整物理根账本统一衰减。</p>
          </div>

          <div class="task-one" id="r072k" data-release="r072k" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72K · 2026-08-27</p>
            <h3>复导数不必为零；每个根隙只需要自己的实投影</h3>
            <p>对 \(X\in W^{2,1}(I;B)\) 的每个相邻根隙，我用右端导数的 norming functional 定义实投影。零端点使投影导数的平均值为零，由此得到 \(\sum_{j=2}^m\|X'(t_j)\|^2\le2\int\|X'\|\|X''\|\)。系数 2 尖锐，首根项必要。</p>
            <p>应用于 integrating-factor target 后，\(G_{\rm all}^{\rm ex}\le E_A\rho_A^2+2\mathcal E_Q+2\mathcal C_\times\)。common-band complete root mass 为 \(a^2N^2\) 量级，完整 physical ratio 仍按 \(R^{-4/9}(1+\log R)^{-2/3}\) 统一衰减。</p>
            <p><strong>结论边界：</strong>&nbsp;定理限于 exact finite triangular class；strong coupling、multiscale 与一般三维正则性仍然开放。</p>
            <p><a href="/notes/r0-72k.html"><strong>阅读 R0.72K 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72k.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72k-directional-roots.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072k">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072k_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072k-directional-roots/fig-r072k-directional-roots">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72k.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72k.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72L：</strong>&nbsp;检查 strong-coupling continuous-row ledger，并保留 multiscale heat windows 为后续接口。</p>
          </div>
        </section>'''
    html = once(html, old_tail, new_tail, "home K card")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    if "/i18n-en.js?v=1.24" in html:
        return
    changes = [
        ("/recap-r0-61-r0-72j", "/recap-r0-61-r0-72k"),
        ("/i18n-en.js?v=1.23", "/i18n-en.js?v=1.24"),
        ("文献综述 v1.23 · 2026-08-27", "文献综述 v1.24 · 2026-08-27"),
        ("本站 R0.69P–R0.72J 只列为研究笔记", "本站 R0.69P–R0.72K 只列为研究笔记"),
        ("累计回顾与 100 节索引", "累计回顾与 101 节索引"),
        ("打开 100 节完整索引", "打开 101 节完整索引"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"literature {old}")
    html = once(html,
        r"R0.72J 完成 gcd-reduced Cayley graph 的二分分类，区分 odd cycle 与 triangle return，并证明 common-band coherent mixed-parity cubic 在物理归一化后仍衰减。一般 Navier–Stokes 正则性仍开放。</p>",
        r"R0.72J 完成 gcd-reduced Cayley graph 的二分分类，区分 odd cycle 与 triangle return，并证明 common-band coherent mixed-parity cubic 在物理归一化后仍衰减。R0.72K 通过逐根隙 norming direction 闭合 complete complex-target ledger，并证明其 common-band 物理归一化比仍统一衰减。一般 Navier–Stokes 正则性仍开放。</p>", "literature K route")
    open_k = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72K</b><strong>multi-scale / strong-coupling or complex-root gate</strong></header><p>检查跨热时间尺度的 triangles、完整强耦合账本，或不依赖实 Rolle 符号交替的 complex target complete-root mechanism。</p></div>'''
    closed_k = r'''              <div class="route-step closed"><header><b>R0.72K</b><strong>directional zero sampling 与 complete complex-target ledger</strong></header><p>每个根隙使用右端导数的 norming direction，把复目标的全部 derivative mass 支付到 mixed row 与 true cubic；common-band complete ledger 在物理 critical-log 归一化后统一衰减。<a href="/notes/r0-72k.html">研究笔记</a> <a href="/recap-r0-61-r0-72k.html">当前累计回顾</a> <a href="#r072k-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72L</b><strong>strong-coupling continuous-row ledger</strong></header><p>检查离开 \(gB/R^2\le\gamma_0\) 后的 mixed-row 与 true-cubic payment；multiscale heat windows 保留为并列后续接口。</p></div>'''
    html = once(html, open_k, closed_k, "literature K cards")
    boundary_j = r'''          <div class="boundary"><strong>R0.72J 的主张边界</strong><p>本节的 graph classification 是精确离散定理；物理 no-go 只覆盖声明的 common-band aligned perturbative families。限定检索没有发现把这些三项直接组合成 arbitrary-carrier complete-root theorem 的来源；这是 bounded non-collision check，不是原创性、优先权或一般 NSE 结论。</p></div>'''
    boundary_k = r'''

          <h3 id="r072k-boundary">R0.72K 的 directional sampling 与 complex-root 边界</h3>
          <p><a href="https://doi.org/10.1017/S0013091500008786">McLeod</a> 用线性泛函表述 vector-valued mean-value conclusions；<a href="https://doi.org/10.4064/ap-8-1-29-32">Opial</a> 控制端点条件下的积分乘积；<a href="https://doi.org/10.1017/S0013091500017417">Stadje</a> 与 Banach indicatrix 理论处理 level crossings；<a href="https://doi.org/10.1090/S0025-5718-04-01708-9">Narcowich–Ward–Wendland</a> 的 scattered-zero estimate 需要 fill distance。它们都不直接给出 fixed endogenous zero level 上的 squared endpoint-derivative sum。</p>
          <p><a href="https://doi.org/10.1112/S002461079700536X">Novikov–Yakovenko</a> 的 complex Rolle framework 和 analytic zero-counting theories 使用复增长或方程结构；R0.72K 不寻找复导数零点，而是对每个实时间根隙单独投影。Navier–Stokes time analyticity 也不支付 mixed row 或 true cubic。</p>
          <div class="boundary"><strong>R0.72K 的主张边界</strong><p>方向引理的证明完整写出；限定检索未发现同一 fixed-level endpoint-slope packing 公式，但不据此主张新颖性或优先权。complete-root consequence 限于 finite triangular class，common-band decay 还保留 perturbative assumptions。</p></div>'''
    html = once(html, boundary_j, boundary_j + boundary_k, "literature K boundary")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    count = len(list((PUBLIC / "notes").glob("*.html")))
    if count != 161:
        raise RuntimeError(f"expected 161 public HTML notes, found {count}")
    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({"latestCompletedRelease": "r072k", "siteVersion": "1.24",
                    "publicHtmlNoteCount": count, "postR060RecapNodeCount": 101,
                    "nextRelease": "r072l",
                    "latestReleaseGate": "tests/r072k-directional-root-gate.test.mjs",
                    "postR070APublishedReleaseCount": 63,
                    "postR070AFormalSealedReleaseCount": 39,
                    "legacyFormalFigureBacklogCount": 24})
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.24", "latestRelease": "R0.72K", "publicHtmlNoteCount": count})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update({"latestPublishedRelease": "r072k", "publishedReleaseCount": 63,
                      "formalSealedReleaseCount": 39, "legacyFormalFigureBacklogCount": 24})
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072k" not in inventory[key]:
            inventory[key].append("r072k")
    if len(inventory["legacyFormalFigureBacklog"]) != 24:
        raise RuntimeError("legacy formal-figure backlog changed unexpectedly")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    print(json.dumps({"release": "R0.72K", "siteVersion": "1.24", "notes": 161,
                      "recapNodes": 101, "published": 63, "formalSealed": 39,
                      "legacyBacklog": 24, "phases": 27}, ensure_ascii=False))


if __name__ == "__main__":
    main()
