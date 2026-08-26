#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "public" / "recap-r0-61-r0-72c.html"
OUTPUT = ROOT / "public" / "recap-r0-61-r0-72d.html"
html = SOURCE.read_text(encoding="utf-8")


def replace_once(before: str, after: str, label: str) -> None:
    global html
    count = html.count(before)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    html = html.replace(before, after, 1)


replace_once(
    '<meta name="description" content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72C 的 93 个研究节点；最新一节把 arbitrary physical phases 纳入共轭配对模型，并确定 phase-uniform M^{-8/3} 与正时间 tail M^{-3} 的尖锐代数前因子。">',
    '<meta name="description" content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.72D 的 94 个研究节点；最新一节构造高频平移 Rudin–Shapiro 内点根，并在保留 full rotational charge 后得到非消失 normalized complete-root ledger。">',
    "description",
)
replace_once(
    '<meta property="og:title" content="R0.61–R0.72C｜R0.60 之后的研究回顾">',
    '<meta property="og:title" content="R0.61–R0.72D｜R0.60 之后的研究回顾">',
    "og title",
)
replace_once(
    '<meta property="og:description" content="二十个阶段、93 个节点：从约化递推和动态路线，到 complete-root 账本、target-row participation，再到 arbitrary physical phases 与尖锐 phase-free carrier 尺度。">',
    '<meta property="og:description" content="二十一个阶段、94 个节点：从约化递推和 complete-root 账本，到 physical phases，再到真实内点根与 full-charge normalized saturation。">',
    "og description",
)
replace_once(
    "<title>R0.61–R0.72C｜R0.60 之后的研究回顾</title>",
    "<title>R0.61–R0.72D｜R0.60 之后的研究回顾</title>",
    "title",
)
replace_once('/i18n-en.js?v=1.16', '/i18n-en.js?v=1.17', "i18n version")
replace_once(
    '<div class="eyebrow">累计回顾 · R0.61–R0.72C · 2026-08-27</div>',
    '<div class="eyebrow">累计回顾 · R0.61–R0.72D · 2026-08-27</div>',
    "eyebrow",
)
replace_once(
    '<p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72C 的 93 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。</p>',
    '<p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72D 的 94 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。</p>',
    "lead",
)
replace_once(
    '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72C</strong><p>收录节点：93</p><p>回顾截止时公开笔记：153</p><p>回顾截止节点：R0.72C</p><p>问题状态：仍未解决</p></div>',
    '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72D</strong><p>收录节点：94</p><p>回顾截止时公开笔记：154</p><p>回顾截止节点：R0.72D</p><p>问题状态：仍未解决</p></div>',
    "stamp",
)
replace_once(
    '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 二十个研究阶段</a></li><li><a href="#node-index">02 · 93 节完整索引</a></li>',
    '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 二十一个研究阶段</a></li><li><a href="#node-index">02 · 94 节完整索引</a></li>',
    "toc counts",
)
replace_once(
    '<div class="metric"><strong>93</strong><span>R0.61–R0.72C 研究节点</span></div>\n            <div class="metric"><strong>55</strong><span>R0.70A–R0.72C 已公开并封存版本</span></div>\n            <div class="metric"><strong>20</strong><span>按问题划分的研究阶段</span></div>',
    '<div class="metric"><strong>94</strong><span>R0.61–R0.72D 研究节点</span></div>\n            <div class="metric"><strong>56</strong><span>R0.70A–R0.72D 已公开并封存版本</span></div>\n            <div class="metric"><strong>21</strong><span>按问题划分的研究阶段</span></div>',
    "metrics",
)
replace_once(
    "后面的 93 个节点沿着这个缺口推进；R0.70A–R0.72C 的 55 个版本已经公开并封存",
    "后面的 94 个节点沿着这个缺口推进；R0.70A–R0.72D 的 56 个版本已经公开并封存",
    "scope counts",
)
replace_once(
    '<section id="timeline"><div class="section-no">01 / 研究过程</div><h2>R0.60 之后的路线分成二十段</h2>',
    '<section id="timeline"><div class="section-no">01 / 研究过程</div><h2>R0.60 之后的路线分成二十一个阶段</h2>',
    "phase count",
)

phase_anchor = '              <div class="links"><a href="/notes/r0-72c.html">R0.72C</a><a href="/figures/r0-72c-phase-participation.pdf">R0.72C 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072c">R0.72C 证书</a></div></article>'
phase_d = r'''
            <article class="phase"><h3>R0.72D · 高频平移 Rudin–Shapiro 与真实 normalized saturation</h3>
              <p>把 Rudin–Shapiro 符号块平移到 \(r_j=M+j\) 后，任意前缀界与 Abel 求和保持 \(\Omega_0\asymp\sqrt M\)，同时把 \(\int\|V\|\) 和 \(\int\|V\|^2\) 分别压到 \(M^{-3/2}\) 与 \(M^{-1}\)。取 \(\delta a=\gamma M^{3/2}\) 后，effective coupling 为 \(\eta\asymp\gamma M^2\)，但 total Dyson exposure 仍为 \(O(\gamma)\)。</p>
              <p>与 target row 对齐的 launch data 在 \(\tau_M=M^{-3}\) 经过一个 \(O(M^{-1/2})e_0\) 调整后产生 exact simple interior root，root slope 为 \(aM\) 量级。匹配的 \(z\)-independent background 支付完整 \(D\) 并保持 \(\mathcal R_Y=O(1)\)；exact identity \(\mathbb P(u\times\omega)=(-vf_z,0,0)\) 给 full-frequency charge \(O(\gamma^2)\)。最终 \(\mathcal J_{\rm all}/(D^{1/3}\Lambda_1)\) 有严格正下界，与 R0.72C upper ledger 同为 \(M^0\)。这不是发散或一般三维正则性结果。</p>
              <div class="links"><a href="/notes/r0-72d.html">R0.72D</a><a href="/figures/r0-72d-dynamical-ledger.pdf">R0.72D 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072d">R0.72D 证书</a></div></article>'''
replace_once(phase_anchor, phase_anchor + phase_d, "R0.72D phase")

replace_once(
    '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.72C 的 93 节公开笔记</h2>',
    '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.72D 的 94 节公开笔记</h2>',
    "index title",
)
replace_once(
    '            <span class="node-ref"><a href="/notes/r0-72c.html">R0.72C</a><span class="node-state kind-closed">闭</span></span>\n          </div>',
    '            <span class="node-ref"><a href="/notes/r0-72c.html">R0.72C</a><span class="node-state kind-closed">闭</span></span>\n            <span class="node-ref"><a href="/notes/r0-72d.html">R0.72D</a><span class="node-state kind-closed">闭</span></span>\n          </div>',
    "index node",
)

retained_c = r'''            <li>R0.72C 的 arbitrary-physical-phase extension：相反位移必须携带 \(w_l\) 与 \(\overline{w_l}\)，不能把旧公式直接复系数化。标量 slope estimate 对每个实 \(\delta\) 成立；target-row root-mass theorem 只在 \(\delta\ne0\) 时成立。联合 participation inequality 给出 exact-launch phase-uniform \(M^{-8/3}\) 与固定正时间 tail \(M^{-3}\)；Rudin–Shapiro 与同相族分别使这两个代数前因子达到同阶。它们不是 actual root-mass lower bounds，也不触及一般三维正则性。</li>'''
retained_d = r'''
            <li>R0.72D 的 shifted Rudin–Shapiro dynamical saturation：\(r_j=M+j\) 的热权 multiplier 满足 \(\int\|V_M\|\lesssim M^{-3/2}\)、\(\int\|V_M\|^2\lesssim M^{-1}\)；\(\eta\asymp M^2\) 时仍有 bounded Dyson exposure。一个 \(O(M^{-1/2})\) launch adjustment 在 \(\tau_M=M^{-3}\) 产生 exact simple interior root，slope 为 \(M\) 量级。匹配 background 与 full-frequency projected charge 给 bounded \(\mathcal R_Y\) 和 \(\Lambda_1\)，从而 complete normalized ledger 有正下界。该比值不发散，结论仍限于 exact triangular class。</li>'''
replace_once(retained_c, retained_c + retained_d, "retained R0.72D")

old_value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>任意物理相位的代数逃逸被定量压缩，真正开放的问题转向动力学下界</h2>
          <p>截至 R0.72C，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 93 个节点或 55 个已公开并封存版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72B 的 \(M^{-10/3}\) 是 exact-launch coherent family 的改进率。R0.72C 证明它不能 phase-uniform 保持：任意物理相位在正确的共轭配对模型中仍受 \(M^{-8/3}\) 上界，而 Rudin–Shapiro 符号族使这个代数前因子达到同阶。固定正时间的热参与率再把 tail 压到 \(M^{-3}\)，但 pre-ledger 仍不可删除。</p>
          <p>留下的核心缺口不再是静态相位代数本身，而是实际 target-root mass 是否能饱和上界、完整 rotational charge 后是否还有非消失 normalized lower family，以及 changing phase profile 是否有 carrier-count-uniform enhanced dissipation。现有证明全部停留在声明的 finite-carrier triangular 2.5D class。</p>
        </section>'''
new_value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>静态 phase-free 上界已经由真实动力学达到，但比值仍停在 order one</h2>
          <p>截至 R0.72D，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 94 个节点或 56 个已公开并封存版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72C 留下的实际根缺口已经关闭。高频平移 Rudin–Shapiro family 同时保留真实 positive-time root、complete target slope、full data cost、fixed-interval enstrophy contrast 和 full rotational charge；normalized complete ledger 不再随 \(M\) 消失。</p>
          <p>这个结果仍是 exact triangular 2.5D class 内的 sharpness theorem。比值保持有限，没有反驳 \(D^{1/3}\Lambda_1\) payment。一般三维 vortex stretching 与 critical-norm continuation 仍未被触及。</p>
        </section>'''
replace_once(old_value, new_value, "value section")

old_next = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72D 转向实际根质量与完整归一化下界</h2>
          <p>下一有限任务需要二选一地形成可审计结果：构造一条 phase-cancelled family，明确 launch data、coupling、observation interval、全部 exact roots 与非消失 normalized lower ledger；或证明使用动力学信息的更强排除定理，把 R0.72C 的静态前因子上界继续压低。</p>
          <p>任何构造都必须同时记录 pre-ledger 与 restarted tail，保留 \(\delta\ne0\) 的 target-row 量词，并把 algebraic prefactor sharpness、actual root-mass lower bound、normalized ledger saturation 和一般三维 NSE 主张分开。</p>
        </section>'''
new_next = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72E 检查 supercritical growth 与 universal order-one ceiling</h2>
          <p>第一条路线把 \(\eta\) 提到 \(M^2\) 以上，并同时改变 block height、width 或 phase geometry，检查 numerator 是否能比 full rotational charge 更快增长。</p>
          <p>如果所有 supercritical routes 都让 \(\Lambda_1\) 同阶增加，第二条路线就证明 triangular class 的 order-one ceiling。两条路线都必须保留 positive-time exact root、固定物理区间、完整 background cost 和 full-frequency charge。</p>
        </section>'''
replace_once(old_next, new_next, "next section")

replace_once(
    '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72b.html">保留 R0.72B 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72c.html">打开最新节点 R0.72C</a></p>',
    '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72c.html">保留 R0.72C 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72d.html">打开最新节点 R0.72D</a></p>',
    "reproduce navigation",
)
replace_once(
    '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072c">查看 R0.72C 双路证书</a> · <a href="/recap-r0-61-r0-72c.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72b.pdf">上一版累计回顾 PDF</a>',
    '<a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072d">查看 R0.72D 双路证书</a> · <a href="/recap-r0-61-r0-72d.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72c.pdf">上一版累计回顾 PDF</a>',
    "reproduce links",
)
replace_once(
    '<div>R0.61–R0.72C 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div>',
    '<div>R0.61–R0.72D 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div>',
    "footer",
)

OUTPUT.write_text(html, encoding="utf-8")
print({"source": str(SOURCE), "output": str(OUTPUT), "bytes": len(html.encode("utf-8"))})

