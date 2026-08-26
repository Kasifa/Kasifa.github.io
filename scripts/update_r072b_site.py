#!/usr/bin/env python3

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, before: str, after: str, label: str) -> str:
    count = text.count(before)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(before, after, 1)


home_path = ROOT / "public" / "research-review.html"
home = home_path.read_text(encoding="utf-8")
home = home.replace("/recap-r0-61-r0-72a", "/recap-r0-61-r0-72b")
home = home.replace("R0.1–R0.72A", "R0.1–R0.72B")
home = home.replace("R0.69P–R0.72A", "R0.69P–R0.72B")
home = home.replace("R0.70A–R0.72A", "R0.70A–R0.72B")
home = home.replace("v1.14", "v1.15")
home = replace_once(
    home,
    "<span><strong>151</strong>公开研究笔记</span>",
    "<span><strong>152</strong>公开研究笔记</span>",
    "home note count",
)
home = replace_once(
    home,
    "<span><strong>R0.72A</strong>最新研究节点</span>",
    "<span><strong>R0.72B</strong>最新研究节点</span>",
    "latest node",
)
home = replace_once(
    home,
    "<span><strong>many-carrier local exposure / nonlinear charge</strong>当前方向</span>",
    "<span><strong>incoherent phases / positive pre-observation layer</strong>当前方向</span>",
    "current direction",
)
home = replace_once(
    home,
    "把局部暴露上界、exact Bessel 强耦合障碍与完整 nonlinear rotational charge 放进同一个 many-carrier 比较框架。",
    "检查 phase cancellation 与正 pre-observation layer 是否会破坏 target-row participation gain。",
    "summary direction",
)
home = replace_once(
    home,
    '<h3>从三分之一次方族内端点走到局部暴露强耦合边界</h3>',
    '<h3>从 complete-root 局部暴露走到 target-row participation 边界</h3>',
    "route heading",
)
home = replace_once(
    home,
    '              <p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–V 分开 second-time jet、Leray-paid excursion 和 fixed zero-level trace；R0.71W–Z 依次关闭 data-uniform complete first row、fixed-small-coupling endpoint、selected growing roots 与 bounded-coupling complete roots。R0.72A 把强耦合改写成局部暴露：all-root 上界只付 \\(\\eta\\min\\{L,C_\\kappa\\}\\)，有限支撑 launch 可放到 \\(A_0=0\\)，并给出 \\(\\eta=M^\\alpha\\)、\\(L=M^{-\\beta}\\) 的消失区域。exact Bessel 构造同时证明，不能把 rescaled target-row slope-mass 常数做成与 \\(\\eta\\) 无关；它没有推出 normalized nonlinear ledger 发散。</p>',
    '              <p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–Z 依次处理 second-time jet、complete first row、fixed-small-coupling endpoint、selected roots 与 complete roots。R0.72A 把强耦合代价局部化到实际观察层，并以 exact Bessel family 标出 logarithmic row-mass 障碍。R0.72B 再保留精确 target row：complete-root 前因子从 \\(M\\Omega^2\\) 收紧到 \\(M\\rho_A^2\\)；exact-launch 同相可比 family 的 normalized carrier prefactor 为 \\(M^{-10/3}\\)，充分消失区为 \\(\\alpha&lt;\\min\\{5/2,(10+3\\beta)/7\\}\\)。</p>',
    "route narrative",
)
home = replace_once(
    home,
    " → local-exposure phase region → exact Bessel logarithmic obstruction</p>",
    " → local-exposure phase region → exact Bessel logarithmic obstruction → target-row participation → coherent many-carrier exclusion</p>",
    "route path",
)
home = replace_once(home, "展开 61 篇公开笔记", "展开 62 篇公开笔记", "route count")
home = replace_once(
    home,
    'aria-label="R0.69P–R0.72B"',
    'aria-label="R0.69P–R0.72B"',
    "route aria",
)
home = replace_once(
    home,
    '                  <a class="milestone" href="/notes/r0-72a.html">R0.72A</a>\n                </nav>',
    '                  <a class="milestone" href="/notes/r0-72a.html">R0.72A</a>\n                  <a class="milestone" href="/notes/r0-72b.html">R0.72B</a>\n                </nav>',
    "route note link",
)

old_next = r'''          <div class="tree-row">
            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72B</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>many-carrier 局部暴露与完整 nonlinear charge</h3>
              <p>把 R0.72A 的单行 local-exposure 定理推广到 many-carrier profile，核对 full nonlinear rotational charge 与 enhanced-dissipation 时间尺度是否能在同一层宽上统一支付；若不能，就给出量词明确的失效族。</p>
            </article>
          </div>'''
new_next = r'''          <div class="tree-row">
            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72C</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>incoherent phases 与 positive pre-observation layer</h3>
              <p>检查 phase cancellation 是否能让 \(\chi_A\) 保持阶一，并处理 \(A_0&gt;0\) 后 heat weights 造成的 effective-carrier collapse；构造与排除都必须保留 full charge、freezing error 和 pre/tail ledger。</p>
            </article>
          </div>'''
home = replace_once(home, old_next, new_next, "next route node")

home = replace_once(
    home,
    "本站 R0.69P–R0.72B 路线放在同一张图中。",
    "本站 R0.69P–R0.72B 路线放在同一张图中。",
    "literature route summary",
)

old_recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72A · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 91 个节点；全站现有 151 篇公开研究笔记</h3>
            <p>R0.60 之后的累计回顾按十八个阶段组织：R0.61–R0.66 四阶递推与热加权周期；R0.67A–R0.68B-2f/g/h 六阶、八阶与高阶尾；R0.69A 完整 Picard 渐近；R0.69B–R0.69F 横向稳定与预解算子；R0.69G–R0.69O 有符号核、压力与远近场；R0.69P–R0.69W 拉伸几何、物理环带与静态族；R0.70A–R0.70I 移动尺度与时间 Hardy 核；R0.70J–R0.70O 偏差张量、协方差谱与有限观测；R0.70P–R0.70Z Parseval 框架、响应距离与谱隙；R0.71A–R0.71D 恒定投影、正输出与物质热 tent；R0.71E–R0.71F projected-Lamb 热体积与局部迹；R0.71G–R0.71I 驻留、projective heat 与 BV 归约；R0.71J–R0.71N 全 frame、matched cells 与融合账本；R0.71O–R0.71P 一侧 faces 与同刻空间打包；R0.71Q–R0.71R 条件 Jensen 与 incidence；R0.71S–R0.71T directional packets 与真实内部 entry；R0.71U–R0.71Z second-time jet、complete first row 与全部根边界；R0.72A 局部暴露相图与 exact Bessel 障碍。R0.70A–R0.72B 共 53 个完成版本。</p>
            <p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72A 在声明的 real-shear exact triangular class 中把 complete all-root 账本改成局部暴露上界，并给出强耦合—层宽消失区域；exact Bessel 构造排除了与 \(\eta\) 无关的 rescaled target-row slope-mass 常数，但没有证明 normalized nonlinear ledger 发散。这是模型类内的严格边界，不是一般 NSE 正则性结果。</p>
            <p><a href="/recap-r0-61-r0-72b.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72b.pdf">下载同步 PDF</a></p>
          </div>'''
new_recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72B · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 92 个节点；全站现有 152 篇公开研究笔记</h3>
            <p>R0.60 之后的累计回顾按十九个阶段组织。R0.61–R0.69O 保留约化递推、剪切边界、横向扰动与压力局部预算；R0.69P–R0.71T 依次检查静态环带、协方差谱、projected-Lamb heat、faces、incidence 与真实内部 entry；R0.71U–R0.71Z 处理 second-time jet、complete first row 与全部根边界；R0.72A 给出局部暴露相图与 exact Bessel 障碍；R0.72B 给出 target-row participation 与 coherent many-carrier exclusion。R0.70A–R0.72B 共 54 个完成版本。</p>
            <p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.72B 在声明的 exact-launch coherent triangular class 中得到 \(M^{-10/3}\) normalized carrier suppression，并分清 enhanced dissipation 只能改善 tail、不能抹去 pre-ledger。这是模型类内的严格边界，不是一般 NSE 正则性结果。</p>
            <p><a href="/recap-r0-61-r0-72b.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72b.pdf">下载同步 PDF</a></p>
          </div>'''
home = replace_once(home, old_recap, new_recap, "home recap card")

home = replace_once(
    home,
    '<p><strong style="color:var(--gold)">下一步 R0.72B：</strong>&nbsp;比较 many-carrier local exposure、full nonlinear rotational charge 与 enhanced-dissipation 时间尺度，寻找可统一支付的区域或量词明确的失效族。</p>',
    '<p><strong style="color:var(--gold)">R0.72B 已完成：</strong>&nbsp;target-row participation 把 coherent exact-launch many-carrier 的 normalized carrier prefactor 收紧到 \(M^{-10/3}\)。</p>',
    "r072a next marker",
)

r072b_card = r'''

          <div class="task-one" id="r072b" data-release="r072b" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72B · 2026-08-27</p>
            <h3>目标行参与率把 coherent many-carrier complete-root 账本进一步压到 \(M^{-10/3}\)</h3>
            <p>
              令 \(\rho_A=\|P_0V_z(A_0)\|\)、\(\chi_A=\rho_A^2/\Omega^2\)。显式 target row、合并后的 \(Q\) row 与 mixed exposure 给
              \[
                G_{\rm all}^{\rm ex}(I)
                \le e^{2\lambda_0L}M\rho_A^2
                [1+q_\rho+\eta\ell_\times],
                \qquad q_\rho\le3,\quad
                \ell_\times\le\min\{L,C_\times\}.
              \]
              complete normalized ledger 因而比 R0.72A 多一个 exact participation factor \(\chi_A\)，并继续保留 full \(\Lambda_1\) charge。
            </p>
            <p>
              exact launch、同相且幅度可比时，\(\chi_0=O(M^{-1})\)、\(\Omega^2/K_v=O(M^{-1})\)、\(M/K_s=O(M^{-2})\)，总 prefactor 为 \(M^{-10/3}\)。若 \(\eta=M^\alpha\)、\(L=M^{-\beta}\)，充分消失区为 \(\alpha&lt;\min\{5/2,(10+3\beta)/7\}\)。这个区域没有 converse。
            </p>
            <p><strong>结论边界：</strong>&nbsp;这是 exact-launch coherent triangular class 的 uniform exclusion。固定正 \(A_0\) 可让 effective carrier count 坍缩；incoherent phases、changing-profile enhanced dissipation 与 normalized many-carrier lower family 仍开放。</p>
            <p>
              <a href="/notes/r0-72b.html"><strong>阅读 R0.72B 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72b.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72b-row-coherence.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072b">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072b_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072b_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072b_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072b_independent_audit.md">查看独立审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072b-row-coherence/fig-r072b-row-coherence">查看附图、数据、进度与源代码包</a> ·
              <a href="/recap-r0-61-r0-72b.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72b.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.72C：</strong>&nbsp;检查 incoherent phases 与 positive pre-observation layer，寻找 phase-stable participation theorem 或 exact normalized lower family。</p>
          </div>'''
home = replace_once(
    home,
    '          </div>\n        </section>\n\n      </article>\n    </div>\n  </main>',
    '          </div>' + r072b_card + '\n        </section>\n\n      </article>\n    </div>\n  </main>',
    "append r072b card",
)

home_path.write_text(home, encoding="utf-8")


literature_path = ROOT / "public" / "literature-review.html"
literature = literature_path.read_text(encoding="utf-8")
literature = literature.replace("/recap-r0-61-r0-72a", "/recap-r0-61-r0-72b")
literature = literature.replace("R0.69P–R0.72A", "R0.69P–R0.72B")
literature = literature.replace("v1.14", "v1.15")
literature = replace_once(
    literature,
    "累计回顾与 91 节索引",
    "累计回顾与 92 节索引",
    "literature recap count",
)
literature = replace_once(
    literature,
    "打开 91 节完整索引",
    "打开 92 节完整索引",
    "literature index count",
)
literature = replace_once(
    literature,
    "本站 R0.69P–R0.72B 只列为研究笔记。",
    "本站 R0.69P–R0.72B 只列为研究笔记。",
    "literature scope",
)
literature = replace_once(
    literature,
    "；R0.72A 再把 strong-coupling loss 局部化到实际观察层，关闭 finite-support exact launch，并用 exact Bessel family 证明 selected row mass 至少可对数增长。一般 Navier–Stokes 正则性仍开放。",
    "；R0.72A 再把 strong-coupling loss 局部化到实际观察层并给出 exact Bessel logarithmic obstruction；R0.72B 保留 exact target-row participation，对 coherent exact-launch many-carrier family 得到 \(M^{-10/3}\) suppression。一般 Navier–Stokes 正则性仍开放。",
    "literature route intro",
)

old_open = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72B</b><strong>many-carrier / full nonlinear charge / uniform dissipation scale</strong></header><p>检查 one-carrier logarithmic root mass 能否扩展到 growing carrier count，并同时支付 \(M^{-2}\) lattice cost、完整 rotational charge 与 enhanced-dissipation comparison。</p></div>'''
new_open = r'''              <div class="route-step kept"><header><b>R0.72B</b><strong>target-row participation 与 coherent many-carrier exclusion</strong></header><p>complete-root 前因子从 \(M\Omega^2\) 收紧到 \(M\rho_A^2\)。exact-launch 同相可比 carriers 的 participation 与载频矩共同给出 \(M^{-10/3}\) prefactor，以及 \(\alpha&lt;\min\{5/2,(10+3\beta)/7\}\) 的 sufficient region。<a href="/notes/r0-72b.html">研究笔记</a> <a href="/recap-r0-61-r0-72b.html">当前累计回顾</a> <a href="#r072b-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72C</b><strong>incoherent phases / positive pre-observation layer</strong></header><p>检查 phase cancellation 与 heat-weighted effective-carrier collapse，寻找 phase-stable participation theorem 或 full normalized exact lower family。</p></div>'''
literature = replace_once(literature, old_open, new_open, "literature route step")

r072a_boundary = r'''          <div class="boundary"><strong>R0.72A 的一手与官方来源边界</strong><p><a href="#ref-71">Constantin–Kiselev–Ryzhik–Zlatoš</a>、<a href="#ref-72">Bedrossian–Coti Zelati</a>和<a href="#ref-73">Coti Zelati–Gallay</a>表明 fixed nonconstant profiles 在 large coupling 下通常产生 enhanced dissipation，定量率依赖 critical-point degeneracy 与 sublevel control。这些结果控制 observation time 的 semigroup norm，不直接控制此前累积的 coordinate zeros 或 slope mass，也不自动统一覆盖本节随 \(M\) 改变的 heat-decaying profile。对 frozen \(2\cos\theta\) 的比较率为 \(R^2/(\log R)^2\)，而本节 layer 为 \(O(R^{-3})\)，所以该 family 位于 comparison time 之前；这仍只是 autonomous frozen-profile comparison。限定检索不支持原创性、优先权或一般 NSE 结论。</p></div>'''
r072b_boundary = r'''
          <h3 id="r072b-boundary">R0.72B 怎样接入 time-dependent shear literature</h3>
          <p>R0.72B 不把 enhanced dissipation 当作 complete-root theorem 的前提。精确 target row 直接给 \(G_{\rm all}^{\rm ex}\le e^{2\lambda_0L}M\rho_A^2[1+q_\rho+\eta\ell_\times]\)。若在 burn-in 时刻已有独立证明的 energy decay，同一定理可改善 restart 后的 tail；launch 以来已累计的 nonnegative pre-ledger 不会被 terminal decay 抹去。</p>
          <div class="boundary"><strong>R0.72B 的主源边界</strong><p><a href="#ref-74">Coble–He</a>要求随时间慢变且具有统一临界结构的 shear；<a href="#ref-75">Gardner–Liss–Mattingly</a>处理 fixed shear 的 pathwise decay；<a href="#ref-76">Benthaus–Nobili</a>处理固定空间 profile 的标量时间调制；<a href="#ref-77">Benthaus–Coclite–Nobili</a>处理刚性平移正弦；<a href="#ref-78">Albritton–Beekie–Novack</a>给 fixed bracket geometry 的 hypoelliptic framework。已核对结果都没有同时提供随 \(M\) 改变的 heat-decaying Fourier sum 的 uniform critical/sublevel constants 与 launch-inclusive root-slope ledger。这个判断限于所列主源。</p></div>'''
literature = replace_once(
    literature,
    r072a_boundary,
    r072a_boundary + r072b_boundary,
    "r072b literature boundary",
)

ref73 = '            <li id="ref-73">M. Coti Zelati and T. Gallay. <a href="https://doi.org/10.1112/jlms.12782"><em>Enhanced dissipation and Taylor dispersion in higher-dimensional parallel shear flows</em></a>. J. Lond. Math. Soc. 108 (2023), 1358–1392.</li>'
new_refs = ref73 + r'''
            <li id="ref-74">D. Coble and S. He. <a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10"><em>A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent Shear Flows</em></a>. Commun. Math. Sci. 22 (2024); <a href="https://arxiv.org/abs/2309.15738">arXiv version</a>.</li>
            <li id="ref-75">V. Gardner, K. L. Liss and J. C. Mattingly. <a href="https://arxiv.org/abs/2410.05657"><em>A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows</em></a>. Preprint, 2024.</li>
            <li id="ref-76">J. Benthaus and C. Nobili. <a href="https://arxiv.org/abs/2501.16905"><em>Enhanced Dissipation via time-modulated velocity fields</em></a>. Preprint, 2025.</li>
            <li id="ref-77">J. Benthaus, G. M. Coclite and C. Nobili. <a href="https://arxiv.org/abs/2603.14624"><em>Mixing and enhanced dissipation in a time-translating shear flow</em></a>. Preprint, 2026.</li>
            <li id="ref-78">D. Albritton, R. Beekie and M. Novack. <a href="https://arxiv.org/abs/2105.12308"><em>Enhanced dissipation and Hörmander's hypoellipticity</em></a>. J. Funct. Anal. 283 (2022), 109522.</li>'''
literature = replace_once(literature, ref73, new_refs, "new primary references")
literature_path.write_text(literature, encoding="utf-8")

print(
    {
        "home": str(home_path),
        "home_bytes": len(home.encode("utf-8")),
        "literature": str(literature_path),
        "literature_bytes": len(literature.encode("utf-8")),
    }
)
