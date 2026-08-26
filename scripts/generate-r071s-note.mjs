import { access, copyFile, mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const notePath = resolve(root, "public/notes/r0-71s.html");
const figureSource = resolve(
  root,
  "figures/r071s-signed-packet/fig-r071s-signed-packet",
);
const publicFigureDirectory = resolve(root, "public/figures");

await Promise.all([
  access(resolve(root, "research/r071s_report-source.md")),
  access(resolve(root, "research/r071s_gap_matrix.md")),
  access(resolve(root, "research/r071s_literature_audit.md")),
  access(resolve(root, "research/r071s_independent_audit.md")),
  access(resolve(root, "research/certificates/r071s/result.json")),
  access(resolve(root, "research/certificates/r071s/independent-result.json")),
]);

const html = String.raw`<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="研究笔记 R0.71S：有限 directional-packet theorem 成立；非零均值抛物 packet 的最优 Bessel 常数至少带 kappa 平方；冻结分母的反向热模型与一类归一化双线性核不能消去该代价；真实 NSE 初始 face 的协变缩放排除由裸 Leray 时间积分统一支付原目标。">
  <meta property="og:type" content="article">
  <meta property="og:title" content="R0.71S｜signed packet 看见 entry，但裸 Leray 时间积分仍少两阶">
  <meta property="og:description" content="有限 packet 定理、精确 Gram–Bessel 常数、反向热伴随、even-touch 二分与真实 NSE 初始面缩放边界。">
  <meta property="og:image" content="https://kasifa.github.io/figures/r0-71s-signed-packet.png">
  <title>R0.71S｜signed packet 看见 entry，但裸 Leray 时间积分仍少两阶</title>
  <script>
    window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};
  </script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.90">
  <style>.hero h1{font-size:clamp(1.68rem,3.6vw,3rem)}@media print{#reproduce{break-inside:avoid}}</style>
  <script defer src="/i18n-en.js?v=1.04"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#interface">接口</a><a href="#theorem">条件定理</a><a href="#bessel">Bessel 障碍</a><a href="#adjoint">热伴随</a><a href="#bilinear">双线性二分</a><a href="#scaling">NSE 缩放</a><a href="#literature">文献</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.71S · SIGNED PACKET · BESSEL AUDIT</div>
        <h1>signed packet 保留 entry direction，<br>但裸 Leray 时间积分仍少两阶</h1>
        <p class="lead">R0.71R 只排除了 endpoint-square、termwise source-square certificate。本节直接保留 \(e_\beta=c_\beta/\|c_\beta\|_2\) 与 signed pairing。有限 directional-packet theorem 可以严格证明；但任何能看见常值 directional signal 的非零均值抛物 packet，单包就需要至少 κ² 的最优 Bessel 常数。冻结分母的反向热模型和一类归一化双线性核保留同一代价；variable \(Y\) 另有归一化项。真实 NSE 初始 face 的协变缩放进一步排除“原目标只由裸 \(\dot H^{-1}\)-Lamb 时间积分以尺度统一常数支付”的方案。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.71S 有限定理与方法边界完成</span><strong>finite conditional theorem；scoped no-go</strong><p>版本 v0.71S · 2026-08-26</p><p>exact audit: PASS</p><p>independent audit: PASS</p><p>无 PDE 正时间推进</p><p>下一对象：internal-entry dynamical charge</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节判断</a></li><li><a href="#interface">01 · 目标与尺度</a></li><li><a href="#theorem">02 · 有限条件定理</a></li><li><a href="#bessel">03 · 对角与 Gram</a></li><li><a href="#adjoint">04 · 反向热伴随</a></li><li><a href="#bilinear">05 · 双线性与 even touch</a></li><li><a href="#scaling">06 · 真实 NSE 缩放</a></li><li><a href="#literature">07 · 文献边界</a></li><li><a href="#audit">08 · 双重审计</a></li><li><a href="#figure">09 · 正式附图</a></li><li><a href="#value">10 · 研究价值</a></li><li><a href="#next">11 · 下一步</a></li><li><a href="#claims">12 · 主张边界</a></li><li><a href="#reproduce">13 · 复现</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Direct verdict</div><h2>看见常值 entry 与 H⁻¹-uniform Bessel payment 不能同时成立</h2>
          <div class="boundary"><strong>本节判断</strong><p>对本节精确定义的 linear directional packets 与 normalized quadratic temporal kernels，存在一个严格二分：非零均值使 packet 能校正常值 entry，却强制最优常数至少按 κ² 增长；零均值消去该对角项，却对常值 directional signal 给出零。even touch 又使双侧 signed face 完全抵消。该结论关闭“原 positive-entry 目标 + 裸 Leray 时间积分”的这类 packet 终局，不关闭 internal entries 专属的 NSE 恒等式或带额外尺度权的动力学 charge。</p></div>
          <p>这里没有得到新的无条件继续性判据，也没有构造有限时奇性。结论是方法分类，不是对三维 Navier–Stokes 全局正则性的证明。</p>
        </section>

        <section id="interface"><div class="section-no">01 / Target and scaling</div><h2>entry 原子尺度为零，裸时间预算缩小两阶</h2>
          <div class="equation result">\[
            f_\beta(t)=\frac{\langle F_{j_\beta}(t),e_\beta\rangle}{\sqrt{Y(t)}},
            \qquad
            a_\beta=\kappa_{j_\beta}^{-2}\bigl(f_\beta(t_\beta)^+\bigr)^2.
          \]</div>
          <p>取 \(h_\beta=\theta_\beta\kappa_{j_\beta}^{-2}\)。在 normalized torus 的 compatible integer/dyadic NSE dilation 下，κ 的尺度是 \(+1\)，\(f\) 的尺度是 \(+1\)，所以 \(a_\beta\) 不变；而</p>
          <div class="equation">\[
            \int \sum_j\kappa_j^{-2}\frac{\|F_j(t)\|_2^2}{Y(t)}\,dt
          \]</div>
          <p>缩放为原来的 λ⁻²。任何尺度统一的终局必须说明这两个量之间缺少的两阶来自哪里。</p>
        </section>

        <section id="theorem"><div class="section-no">02 / Finite packet theorem</div><h2>在 sampling coherence 与 Bessel hypothesis 下，有限目标确实可支付</h2>
          <p>令 η∈L²(0,1)、‖η‖₂=1、μ=∫η&gt;0，并定义</p>
          <div class="equation">\[
            \eta_\beta(t)=h_\beta^{-1/2}\eta\!\left(\frac{t-t_\beta}{h_\beta}\right),
            \qquad
            p_\beta=\int_{I_\beta}\eta_\beta(t)f_\beta(t)\,dt.
          \]</div>
          <p>若 \(p_\beta\ge(1-\delta)\mu\sqrt{h_\beta}\,f_\beta(t_\beta)&gt;0\)，且 critical analysis vectors 在 \(L_t^2(\bigoplus_jL_x^2)\) 中的有限 Bessel 常数为 \(B_{\rm crit}\)，则</p>
          <div class="equation result">\[
            \sum_\beta a_\beta
            \le
            \frac{B_{\rm crit}}
            {\mu^2(1-\delta)^2\theta_-}
            \int\sum_j\kappa_j^{-2}\frac{\|F_j\|_2^2}{Y}\,dt.
          \]</div>
          <p>证明只有三步：sampling lower bound、有限 Bessel inequality、Littlewood–Paley \(\dot H^{-1}\) square sum。sampling coherence、统一 θ₋ 与 \(B_{\rm crit}\) 都是 hypotheses；该有限定理本身不是 temporal-packing theorem。</p>
        </section>

        <section id="bessel"><div class="section-no">03 / Sharp diagonal and Gram cost</div><h2>单包已经强制 κ²；同向聚簇再强制事件数</h2>
          <p>critical analysis vector 含有一个 κ 因子，因此精确对角范数为</p>
          <div class="equation result">\[
            \|\Phi_\beta\|^2=\kappa_{j_\beta}^2,
            \qquad
            B_{\rm crit}\ge\max_\beta\kappa_{j_\beta}^2.
          \]</div>
          <p>对长度 \(h\) 的 L²-normalized box packets，Gram 矩阵满足</p>
          <div class="equation">\[
            G_{k\ell}=\left(1-\frac{|b_k-b_\ell|}{h}\right)_+.
          \]</div>
          <p>最优有限 Bessel 常数正是 \(\lambda_{\max}(G)\)。若 \(N\) 个同向中心落在长度 εh 的簇中，则 \(\lambda_{\max}(G)\ge N(1-\varepsilon)\)；critical family 因而至少支付 \(N(1-\varepsilon)\kappa^2\)。这不是数值拟合，而是全一向量的 Rayleigh quotient。</p>
          <p>去掉 κ 因子可把单包对角降到常数，但右端随即变成 normalized L²-Lamb budget，而不是 Leray 支付的 H⁻¹ budget。</p>
        </section>

        <section id="adjoint"><div class="section-no">04 / Backward heat packet</div><h2>反向热伴随改进 source pairing，但没有改变量纲</h2>
          <p>令 \(g(t)=\langle F(t),e\rangle\)。纯 annular eigenmode 对这个未归一化方向源的精确模型是</p>
          <div class="equation">\[
            C_t+\nu\kappa^2C=\kappa^2g,
            \qquad h=\theta\kappa^{-2}.
          \]</div>
          <p>对应的 exact endpoint packet 为</p>
          <div class="equation">\[
            p_{\rm ad}=\kappa^{-1}C(h)
            =\kappa\int_0^h e^{-\nu\kappa^2(h-s)}g(s)\,ds.
          \]</div>
          <p>相对 strong \(g\in L_t^2\)，其算子范数平方是 \((1-e^{-2\nu\theta})/(2\nu)\)；在 frozen-denominator 模型 \(Y\equiv1\) 中，相对 Leray-order input \(\kappa^{-1}g\)，精确变成</p>
          <div class="equation result">\[
            \kappa^2\frac{1-e^{-2\nu\theta}}{2\nu}.
          \]</div>
          <p>这是一项 exact packet norm 与 frozen-denominator linear-model diagnostic，不是完整 normalized NSE identity。实际 \(f=g/\sqrt Y\) 会使 endpoint integrand 带上 \(\sqrt Y\)；若改为归一化 observable，则演化式增加 \(Y_t/(2Y)\)。Lions–Magenes pairing 不会自动控制这一项；局部 cutoff 还会留下 viscous commutator。</p>
        </section>

        <section id="bilinear"><div class="section-no">05 / Bilinear dichotomy and even touch</div><h2>正次数 bilinear 失去 amplitude invariance；零均值又看不见常值 entry</h2>
          <p>任何在未归一化 observable \(C\) 中具有正齐次次数的 bilinear charge，在 \(C\mapsto\varepsilon C\) 下趋于零，而 \(a_\beta\) 只依赖 leading direction、保持不变。若改用 \(C/\|C\|\) 形成 degree-zero direction，straight-ray \(C(t)=r(t)e\) 上就退化为上一节的 directional packet，因此继承 κ² 对角税。</p>
          <p>更一般地，对有界自伴时间核 \(K\)，常值输入只看见 \(k_0=\langle1,K1\rangle\)。若 \(k_0=0\)，常值 directional signal 完全不可见；若 \(k_0\ne0\)，相对 H⁻¹-normalized input 的单包常数至少为 κ²|k₀|。</p>
          <p>even touch \(C_\varepsilon(t)=\varepsilon(t-b)^2e\) 的左右 direction 相同，\(A_-=A_+&gt;0\)，因此 signed face \(A_+-A_-=0\)。这只是一项 abstract method test，不是 NSE trajectory。它说明只依赖 signed jump、direction jump 或 mean-zero wavelet 的方案会漏掉原 positive-entry 目标。</p>
        </section>

        <section id="scaling"><div class="section-no">06 / Genuine NSE initial-face scaling</div><h2>真实 NSE 初始 face 排除裸时间积分的尺度统一终局</h2>
          <p>R0.71O 的光滑 divergence-free 初值</p>
          <div class="equation">\[
            u_0=(0,\cos x_1,0)+(0,0,\cos x_2)
          \]</div>
          <p>配合 \(m(1)=0,m(\sqrt2)=1\) 的 covariant radial multiplier，产生 \(t=0\) 的真实一侧 entry，且 κ⁻²A₊=1/4。对 \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)\)，该原子仍为 \(1/4\)，而任意固定基准 \(T&gt;0\) 上</p>
          <div class="equation result">\[
            \int_0^{T/\lambda^2}
            \frac{\|L_\lambda(t)\|_{\dot H^{-1}}^2}{Y_\lambda(t)}\,dt
            =\lambda^{-2}
            \int_0^T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}\,dt.
          \]</div>
          <p>所以，任何包含 observation-boundary entry、使用 covariant windows、且常数独立 λ 的“原子和 ≤ 裸时间积分”不等式都矛盾。该结论不覆盖只计算 internal entries 的定理，也不排除 RHS 中加入 initial trace、外部时间尺度或一个真正带 +2 尺度的 dynamical charge。</p>
        </section>

        <section id="literature"><div class="section-no">07 / Primary-source boundary</div><h2>frame、tent 与 heat-adjoint 文献只支付积分 packet，不支付自适应 entry 下界</h2>
          <p><a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>证明临界 parabolic \(X,Y\) 空间中的 quadratic map 与 Duhamel map，但 \(Y\) 不是这里的 bare Leray class，也没有自适应 entry lower charge。<a href="https://doi.org/10.1016/0022-1236(85)90007-2">Coifman–Meyer–Stein</a>的 tent spaces 控制锥区积分、square functions 与 Carleson measures，不控制一般 L² 等价类的裸时间点值。</p>
          <p><a href="https://doi.org/10.1016/0022-1236(90)90137-A">Frazier–Jawerth</a>的离散系数是分布配对或先平滑后的样本；其 trace theorem 也显示零阶 L² 时间正则性不足以定义一般时间点迹。<a href="https://doi.org/10.1007/978-3-642-65161-8_3">Lions–Magenes</a>给 endpoint pairing 的合法性，不给解依赖 packet family 的统一 Bessel 性。</p>
          <p><a href="https://arxiv.org/abs/1101.2193">Dascaliuc–Grujić</a>的 signed flux 正下界依赖 Taylor-scale 条件、长时间平均和 optimal covering，不是逐 entry packet。两轮限定一手检索没有找到同时完成自适应 entry、signed/bilinear lower charge、packet sum 与 bare Leray payment 的现成定理。这是 bounded negative finding，不是不存在性、原创性或优先权声明。</p>
        </section>

        <section id="audit"><div class="section-no">08 / Exact and independent audit</div><h2>符号账本与独立浮点重建分别通过</h2>
          <p>exact producer 记录 packet normalization、对角 κ²、有限 box Gram 下界、backward-heat 常数、bilinear mean dichotomy、even-touch cancellation 与 genuine NSE scaling exponents。independent checker 不导入 producer，另行重建 Gram eigenvalues、热核积分、缩放比与图数据。两者都不进行 NSE time stepping。</p>
        </section>

        <section id="figure"><div class="section-no">09 / Journal figure</div><h2>附图分开显示尺度税、事件聚簇、热伴随与 signed cancellation</h2>
          <figure><img src="/figures/r0-71s-signed-packet.svg" alt="R0.71S directional packet 的 Bessel 尺度税、Gram 聚簇、热伴随与 even-touch signed cancellation"><figcaption>图 R0.71S。A：能看见常值 entry 的 critical packet 最优单包常数按 κ² 增长，strong-data 版本保持常数。B：同向聚簇 box packets 的 Gram 最大特征值随事件数增长。C：backward-heat packet 在 frozen-denominator 线性模型中相对 H⁻¹-order input 仍带 κ²，而相对 strong source 为常数；variable \(Y\) 的归一化项不在该面板内。D：even touch 的 positive entry 为一，signed jump 与 mean-zero response 为零。A–C 是精确 packet/线性模型；D 不是 NSE trajectory。</figcaption></figure>
        </section>

        <section id="value"><div class="section-no">10 / Research value</div><h2>价值在于关闭了比 R0.71R 更宽的一类逃逸方案</h2>
          <p>R0.71R 的两阶错配可能只是 endpoint-square 选择造成的；R0.71S 证明，只要 packet 必须在 parabolic window 内重构常值 directional entry，同样的两阶代价就由 Hilbert-space 对角本身出现。它与 source-square 估计无关；frozen-denominator 反向热核的 packet norm 也达到同一边界，variable \(Y\) 的归一化接口则单独保留。</p>
          <p>真实 NSE 初始面缩放把这个方法结论从 abstract forced path 提升为针对 observation-boundary 版本的 genuine NSE no-go。研究主线因此不再重复尝试“原目标 + bare H⁻¹ time integral”的 temporal packet，而转向适用范围更窄但尚未被排除的 internal-entry dynamics。</p>
        </section>

        <section id="next"><div class="section-no">11 / Next finite gate</div><h2>R0.71T 只检查 internal entries 是否携带额外的尺度零动力学 charge</h2>
          <p>下一步先移除 observation-boundary faces，只研究紧经典区间内部的 entry。候选 RHS 必须在 NSE 协变缩放下与 entry 原子同阶，不能只是裸 \(dt\) 积分，也不能把 κ² 隐藏进 Bessel 常数。</p>
          <p>首先检查 localized Lamb–vorticity coupling 是否在 internal zero 附近强制一个 signed commutator、time-frequency flux 或两尺度补偿项；若仍只得到 strong L²-Lamb、point trace 或事件计数假设，我会把分支停在条件定理。</p>
        </section>

        <section id="claims"><div class="section-no">12 / Claim boundary</div><h2>本节证明什么，也明确不证明什么</h2>
          <ul>
            <li><strong>已证明：</strong>finite directional-packet implication；sharp single-packet κ² Bessel lower bound；finite Gram optimum and clustering lower bound；frozen-denominator backward-heat exact norm；限定 quadratic-kernel dichotomy；observation-boundary NSE scaling no-go。</li>
            <li><strong>未证明：</strong>uniform internal-entry packing、NSE multi-entry counterexample、scale-zero internal dynamical charge、infinite-frame limit、continuation criterion、finite-time singularity 或 global regularity。</li>
            <li><strong>方法边界：</strong>no-go 只针对原 positive-entry target 由 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) 以尺度统一常数支付，并在 genuine NSE 部分包含 initial observation face。</li>
            <li><strong>反例边界：</strong>even-touch 与线性 packet families 是 method tests；只有 Section 06 使用真实 smooth NSE initial trace 与精确协变缩放。</li>
          </ul>
        </section>

        <section id="reproduce"><div class="section-no">13 / Reproduce</div><h2>报告、文献、证书、图数据和独立 checker 全部保留</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_independent_audit.md">独立审计说明</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071s">exact / independent 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071s-signed-packet/fig-r071s-signed-packet">附图、数据、manifest 与源代码包</a> · <a href="/figures/r0-71s-signed-packet.pdf">期刊附图 PDF</a></p>
          <p><a href="/notes/r0-71s.pdf">下载同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-71s.html">阅读 R0.60 之后累计回顾</a> · <a href="/recap-r0-61-r0-71s.pdf">下载累计回顾 PDF</a></p>
          <pre><code>python3 research/r071s_exact_audit.py
python3 research/r071s_independent_audit.py
python3 figures/r071s-signed-packet/fig-r071s-signed-packet/validate_data.py
python3 figures/r071s-signed-packet/fig-r071s-signed-packet/independent_validate.py</code></pre>
        </section>
      </article>
    </div>
  </main>
  <footer><div>R0.71S · 2026-08-26 · 个人数学研究日志<br><a href="/">返回研究主页</a> · <a href="/literature-review.html">文献综述</a> · <a href="/recap-r0-61-r0-71s.html">累计回顾</a></div></footer>
</body>
</html>
`;

if (/我们/.test(html)) throw new Error("R0.71S note must use singular or neutral voice");
for (const token of [
  "B_{\\rm crit}\\ge\\max_\\beta\\kappa_{j_\\beta}^2",
  "\\lambda_{\\max}(G)\\ge N(1-\\varepsilon)",
  "\\kappa^2\\frac{1-e^{-2\\nu\\theta}}{2\\nu}",
  "observation-boundary entry",
  "不覆盖只计算 internal entries 的定理",
  "bounded negative finding",
]) {
  if (!html.includes(token)) throw new Error("missing R0.71S boundary: " + token);
}
for (const forbidden of ["Millennium problem solved", "uniform internal-entry packing 已证明"]) {
  if (html.includes(forbidden)) throw new Error("R0.71S overclaim remains: " + forbidden);
}

await mkdir(publicFigureDirectory, { recursive: true });
await Promise.all(
  ["svg", "pdf", "png"].map((extension) =>
    copyFile(
      resolve(figureSource, "figure." + extension),
      resolve(publicFigureDirectory, "r0-71s-signed-packet." + extension),
    ),
  ),
);
await writeFile(notePath, html);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71S",
      note: notePath,
      publicFigures: ["svg", "pdf", "png"],
      next: "R0.71T",
    },
    null,
    2,
  ),
);
