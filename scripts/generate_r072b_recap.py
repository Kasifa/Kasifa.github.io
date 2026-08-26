#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "public" / "recap-r0-61-r0-72a.html"
OUTPUT = ROOT / "public" / "recap-r0-61-r0-72b.html"
html = SOURCE.read_text(encoding="utf-8")


def replace_once(before: str, after: str, label: str) -> None:
    global html
    count = html.count(before)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    html = html.replace(before, after, 1)


replace_once(
    '<meta name="description" content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72A 的 91 个研究节点；最新一节给出局部暴露强耦合上界、层宽相图与 exact Bessel 对数 rescaled target-row 质量障碍。">',
    '<meta name="description" content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72B 的 92 个研究节点；最新一节以精确目标行参与率证明 coherent many-carrier 的 M^{-10/3} complete normalized exclusion。">',
    "description",
)
replace_once(
    '<meta property="og:title" content="R0.61–R0.72A｜R0.60 之后的研究回顾">',
    '<meta property="og:title" content="R0.61–R0.72B｜R0.60 之后的研究回顾">',
    "og title",
)
replace_once(
    '<meta property="og:description" content="十八个阶段、91 个节点：从约化递推和 R0.70A 之后的动态路线，到 fixed-zero ledger、三分之一次方族内端点、bounded-coupling all-root suppression，再到局部暴露相图与 exact Bessel 障碍。">',
    '<meta property="og:description" content="十九个阶段、92 个节点：从约化递推和动态路线，到 complete-root local exposure、exact Bessel 障碍，再到 target-row participation 与 coherent many-carrier 排除。">',
    "og description",
)
replace_once(
    "<title>R0.61–R0.72A｜R0.60 之后的研究回顾</title>",
    "<title>R0.61–R0.72B｜R0.60 之后的研究回顾</title>",
    "title",
)
replace_once('/i18n-en.js?v=1.14', '/i18n-en.js?v=1.15', "i18n version")
replace_once(
    '<div class="eyebrow">累计回顾 · R0.61–R0.72A · 2026-08-27</div>',
    '<div class="eyebrow">累计回顾 · R0.61–R0.72B · 2026-08-27</div>',
    "eyebrow",
)
replace_once(
    '<p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72A 的 91 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。</p>',
    '<p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72B 的 92 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。</p>',
    "lead",
)
replace_once(
    '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72A</strong><p>收录节点：91</p><p>回顾截止时公开笔记：151</p><p>回顾截止节点：R0.72A</p><p>问题状态：仍未解决</p></div>',
    '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72B</strong><p>收录节点：92</p><p>回顾截止时公开笔记：152</p><p>回顾截止节点：R0.72B</p><p>问题状态：仍未解决</p></div>',
    "stamp",
)
replace_once(
    '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 十八个研究阶段</a></li><li><a href="#node-index">02 · 91 节完整索引</a></li>',
    '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 十九个研究阶段</a></li><li><a href="#node-index">02 · 92 节完整索引</a></li>',
    "toc counts",
)
replace_once(
    '<div class="metric"><strong>91</strong><span>R0.61–R0.72A 研究节点</span></div>\n            <div class="metric"><strong>53</strong><span>R0.70A–R0.72A 完成版本</span></div>\n            <div class="metric"><strong>18</strong><span>按问题划分的研究阶段</span></div>',
    '<div class="metric"><strong>92</strong><span>R0.61–R0.72B 研究节点</span></div>\n            <div class="metric"><strong>54</strong><span>R0.70A–R0.72B 完成版本</span></div>\n            <div class="metric"><strong>19</strong><span>按问题划分的研究阶段</span></div>',
    "metrics",
)
replace_once(
    "后面的 91 个节点沿着这个缺口推进；R0.70A 之后的每个完成版本都保留在路线和索引中。",
    "后面的 92 个节点沿着这个缺口推进；R0.70A 之后的每个完成版本都保留在路线和索引中。",
    "scope count",
)
replace_once(
    '<section id="timeline"><div class="section-no">01 / 研究过程</div><h2>R0.60 之后的路线分成十八段</h2>',
    '<section id="timeline"><div class="section-no">01 / 研究过程</div><h2>R0.60 之后的路线分成十九段</h2>',
    "timeline phase count",
)

phase_anchor = '              <div class="links"><a href="/notes/r0-72a.html">R0.72A</a><a href="/figures/r0-72a-local-bessel.pdf">R0.72A 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072a">R0.72A 证书</a></div></article>'
new_phase = r'''
            <article class="phase"><h3>R0.72B · 目标行参与率与 coherent many-carrier 排除</h3>
              <p>complete target-root theorem 不必由完整 multiplier norm 支付。令 \(\rho_A=\|P_0V_z(A_0)\|\)、\(\chi_A=\rho_A^2/\Omega^2\)，则全部 exact roots 的 nonnegative row mass 至多为 \(e^{2\lambda_0L}M\rho_A^2[1+q_\rho+\eta\ell_\times]\)，其中 \(q_\rho\le3\)、\(\ell_\times\le\min\{L,C_\times\}\)。normalized ledger 因而比 R0.72A 多一个 exact participation factor \(\chi_A\)，并继续保留完整 \(\Lambda_1\) charge。</p>
              <p>在 exact launch、同相且幅度可比的 distinct positive carriers 上，\(\chi_0=O(M^{-1})\)、\(\Omega^2/K_v=O(M^{-1})\)、\(M/K_s=O(M^{-2})\)，总载频前因子为 \(M^{-10/3}\)。对 \(\eta=M^\alpha\)、\(L=M^{-\beta}\)，充分消失区域扩到 \(\alpha&lt;\min\{5/2,(10+3\beta)/7\}\)。这是 coherent class 的 uniform exclusion，不是外部区域的 converse 或一般 NSE 结论。</p>
              <div class="links"><a href="/notes/r0-72b.html">R0.72B</a><a href="/figures/r0-72b-row-coherence.pdf">R0.72B 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072b">R0.72B 证书</a></div></article>'''
replace_once(phase_anchor, phase_anchor + new_phase, "new phase")

replace_once(
    '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.72A 的 91 节公开笔记</h2>',
    '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.72B 的 92 节公开笔记</h2>',
    "index title",
)
replace_once(
    '            <a href="/notes/r0-72a.html">R0.72A</a>\n          </div>',
    '            <a href="/notes/r0-72a.html">R0.72A</a>\n            <a href="/notes/r0-72b.html">R0.72B</a>\n          </div>',
    "index link",
)
old_retained = r'''            <li>R0.72A 的 local-exposure closure：complete-root 账本的强耦合代价收紧为 \(\eta\min\{L,C_\kappa\}\)，从而给出 \(\eta=M^\alpha\)、\(L=M^{-\beta}\) 下 \(\alpha&lt;\min\{3/2,(6+3\beta)/7\}\) 的充分消失区域；有限支撑 launch 可从 \(A_0=0\) 开始。互补的 exact Bessel 构造产生 \((8/\pi^2)\log R+O(1)\) 的 selected rescaled target-row mass，排除 \(\eta\)-independent rescaled target-row all-root 常数，但不证明 normalized nonlinear ledger 发散。</li>'''
new_retained = old_retained + r'''
            <li>R0.72B 的 target-row mixed-exposure theorem：complete-root 前因子从 \(M\Omega^2\) 收紧到 \(M\rho_A^2\)，精确 \(Q\)-row payment 为 3，mixed exposure 常数为 \(C_\times=\sqrt{C_\kappa/(2\kappa)}\)。full normalized ledger 获得 \(\chi_A=\rho_A^2/\Omega^2\)；exact-launch 同相可比 family 的 carrier prefactor 为 \(M^{-10/3}\)，充分区域为 \(\alpha&lt;\min\{5/2,(10+3\beta)/7\}\)。enhanced dissipation 只能改善 restart 后的 tail，不能抹去 pre-ledger。</li>'''
replace_once(old_retained, new_retained, "retained result")

old_value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>局部暴露关闭一片强耦合区域，Bessel 构造标出另一侧障碍；一般问题仍开放</h2>
          <p>截至 R0.72A，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 91 个节点解释成对千禧年问题完成了某个比例。</p>
          <p>R0.71X–Z 依次关闭 fixed-small-coupling endpoint、selected growing roots 与 bounded-coupling complete roots。R0.72A 进一步证明，强耦合的 complete-root 代价可由观察层内的实际暴露支付；当 \(\eta=M^\alpha\)、\(L=M^{-\beta}\) 时，normalized upper bound 在 \(\alpha&lt;\min\{3/2,(6+3\beta)/7\}\) 内消失。这个区域是充分上界，不是 sharp converse。</p>
          <p>exact Bessel 构造说明，即使 observation layer 缩到 \(O(R^{-3})\)，前 \(R\) 个 simple roots 仍可留下对数 rescaled target-row mass；相应物理 \(x\)-导数质量多一个 \(\delta_R^2\) 因子。因此 \(\eta\)-independent rescaled target-row all-root 常数不存在。它没有证明 normalized nonlinear ledger 发散，也没有控制 full nonlinear rotational charge。结论仍限于声明的 triangular lattice，不是一般 NSE 的 complete atom theorem。</p>
        </section>'''
new_value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>coherent many-carrier promotion 被进一步压缩，剩余风险转向 phase cancellation 与正时间退化</h2>
          <p>截至 R0.72B，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 92 个节点解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72A 以 local exposure 关闭一片强耦合—缩层区域，并用 exact Bessel family 排除 \(\eta\)-independent row-mass 常数。R0.72B 再把 complete-root payment 从 full multiplier norm 收紧到 exact target row；同相可比的 growing-\(M\) family 同时受到 participation、载频矩和 \(K_s\) 的 \(M^{-10/3}\) suppression。</p>
          <p>这一排除仍限于 exact-launch coherent triangular class。incoherent phases、正 pre-observation layers、changing-profile enhanced dissipation 和 normalized many-carrier lower construction 仍开放。full nonlinear charge 保留在账本中，但没有被单独计算成新下界。</p>
        </section>'''
replace_once(old_value, new_value, "value section")

old_next = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72B 比较 many-carrier local exposure 与完整 nonlinear charge</h2>
          <p>下一有限任务把 R0.72A 的单行 local-exposure 定理推广到 many-carrier profile，检查 carrier 几何、局部 \(L^2\) exposure 与 full nonlinear rotational charge 能否在同一 shrinking layer 上统一支付。</p>
          <p>同时把 exact Bessel 强耦合时间尺度与 fixed-profile enhanced-dissipation 结果分开比较。目标是得到一块量词清楚的统一区域，或给出能说明具体哪项 uniformity 失效的构造；不把模型时间尺度推断成一般 NSE 结论。</p>
        </section>'''
new_next = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72C 检查 incoherent phases 与 positive pre-observation layer</h2>
          <p>下一有限任务先检查 multiplier peak 因 phase cancellation 而不再对应大 effective participation 的 profiles，并寻找 \(\chi_A\) 不衰减但 full normalized charge 仍可严格支付的 exact family。</p>
          <p>另一分支处理 \(A_0&gt;0\) 后 heat weights 让 \(M_{\rm eff}\) 坍缩的问题。无论得到构造还是上界，都必须保留 exact roots、\(\Xi_M\)、frozen ED comparison 与 pre/tail ledger 的量词区别。</p>
        </section>'''
replace_once(old_next, new_next, "next section")

replace_once(
    '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-71z.html">保留 R0.71Z 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72a.html">打开最新节点 R0.72A</a></p>',
    '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72a.html">保留 R0.72A 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72b.html">打开最新节点 R0.72B</a></p>',
    "reproduce navigation",
)
replace_once(
    '<a href="/recap-r0-61-r0-72a.pdf">下载同步 PDF</a>',
    '<a href="/recap-r0-61-r0-72b.pdf">下载同步 PDF</a>',
    "recap pdf",
)
replace_once(
    '<div>R0.61–R0.72A 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div>',
    '<div>R0.61–R0.72B 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div>',
    "footer",
)

OUTPUT.write_text(html, encoding="utf-8")
print({"source": str(SOURCE), "output": str(OUTPUT), "bytes": len(html.encode("utf-8"))})
