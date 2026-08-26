import { access, copyFile, mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const notePath = resolve(root, "public/notes/r0-71t.html");
const figureSource = resolve(
  root,
  "figures/r071t-internal-entry/fig-r071t-internal-entry",
);
const publicFigureDirectory = resolve(root, "public/figures");

await Promise.all([
  access(resolve(root, "research/r071t_report-source.md")),
  access(resolve(root, "research/r071t_gap_matrix.md")),
  access(resolve(root, "research/r071t_literature_audit.md")),
  access(resolve(root, "research/r071t_independent_audit.md")),
  access(resolve(root, "research/certificates/r071t/result.json")),
  access(resolve(root, "research/certificates/r071t/independent-result.json")),
]);

const html = String.raw`<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="研究笔记 R0.71T：用有限维隐函数定理构造真实光滑 NSE 正时间内部 entry；双尺度族排除由裸 normalized Leray-Lamb 时间积分统一支付该原子；outgoing coarea 给出尺度匹配的精确表示。">
  <meta property="og:type" content="article">
  <meta property="og:title" content="R0.71T｜真实内部 entry 排除裸 Leray 时间支付">
  <meta property="og:description" content="正时间 IFT 构造、内部缩放 no-go、outgoing occupation 表示、完整 trace-variation 账本与有限 Galerkin 复核。">
  <meta property="og:image" content="https://kasifa.github.io/figures/r0-71t-internal-entry.png">
  <title>R0.71T｜真实内部 entry 排除裸 Leray 时间支付</title>
  <script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.90">
  <style>.hero h1{font-size:clamp(1.68rem,3.6vw,3rem)}@media print{#reproduce{break-inside:avoid}}</style>
  <script defer src="/i18n-en.js?v=1.05"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#construction">内部构造</a><a href="#scaling">缩放</a><a href="#occupation">占据量</a><a href="#trace">变差</a><a href="#literature">文献</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.71T · INTERNAL ENTRY · SCALE AUDIT</div>
        <h1>真实正时间内部 entry，<br>排除裸 Leray 时间支付</h1>
        <p class="lead">R0.71S 的缩放结论只覆盖初始 observation face。本节对同一 Fourier seed 做有限壳预补偿：标准局部 NSE 流映射与有限维隐函数定理把精确的四模目标投影在预定正时间压到零，而 nonlinear Lamb forcing 仍非零。该零点是严格内部、simple、positive。随后取振幅 \(a_\lambda=\lambda^{-2}\) 再作 NSE 协变缩放，entry 原子按 λ⁻⁴、裸 normalized Leray-Lamb 时间预算按 λ⁻⁶，最优常数至少按 λ² 发散；初始能量与临界范数同时趋零。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.71T 构造与 no-go 完成</span><strong>genuine internal entry；scoped no-go</strong><p>版本 v0.71T · 2026-08-26</p><p>exact audit: PASS</p><p>independent audit: PASS</p><p>finite Galerkin: corroboration</p><p>下一对象：internal jet / occupation packing</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节判断</a></li><li><a href="#construction">01 · IFT 内部化</a></li><li><a href="#scaling">02 · 双尺度 no-go</a></li><li><a href="#occupation">03 · outgoing coarea</a></li><li><a href="#trace">04 · trace-variation</a></li><li><a href="#literature">05 · 文献边界</a></li><li><a href="#audit">06 · 双重审计</a></li><li><a href="#figure">07 · 正式附图</a></li><li><a href="#value">08 · 研究价值</a></li><li><a href="#next">09 · 下一步</a></li><li><a href="#claims">10 · 主张边界</a></li><li><a href="#reproduce">11 · 复现</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Direct verdict</div><h2>初始边界 caveat 已关闭，裸时间积分不再是候选终局</h2>
          <div class="boundary"><strong>本节判断</strong><p>存在一族真实光滑周期 NSE 解，使 R0.71P 的目标壳在正时间 \(t=\tau\) 精确归零并以正方向横穿。这个事件严格位于 \([0,2\tau)\) 内部。对其振幅—频率双尺度族，scale-zero entry target 与 bare normalized \(\dot H^{-1}\)-Lamb time integral 的比值按 λ² 发散；即使把数据限制在能量趋零、临界范数趋零和 enstrophy 有界的解族，该统一支付仍不成立。</p></div>
          <p>这不是千禧年问题的解答。它严格排除一个此前仍开放的支付机制，并把可行候选缩到 instantaneous jet、outgoing occupation 或改变目标后的 amplitude excursion。</p>
        </section>

        <section id="construction"><div class="section-no">01 / Positive-time construction</div><h2>只改初始目标空间，在预定正时间把完整声明投影压到零</h2>
          <p>取 \(U=(0,\cos x_1,\cos x_2)\)。它只含半径一的速度模，但二次 projected Lamb 场</p>
          <div class="equation result">\[
            F_*=(0,0,\cos x_1\sin x_2),\qquad
            \|F_*\|_2^2=\frac14,
          \]</div>
          <p>精确落在 \(|k|^2=2\) 的四个目标模。令 \(P_*\) 为该实共轭闭合壳的投影，\(S_t\) 为局部经典 NSE 流。对 \(z\) 属于目标壳，定义 \(\Phi(a,z)=P_*S_\tau(aU+z)\)。在零解处</p>
          <div class="equation result">\[
            D_z\Phi(0,0)=e^{-2\nu\tau}I.
          \]</div>
          <p>该有限矩阵可逆，隐函数定理给出真实修正 \(z(a)\)，使这个精确四模投影在 τ 为零。这里不能把四模消去误写成任意宽环带消去。若紧支撑目标与 seed shell 分离，我把变量空间扩为其全部有限 lattice support；此时 \(D_z\Phi=e^{\nu\tau\Delta}\) 在完整目标空间上仍为对角可逆矩阵，因而可以同时消去每个受支持模。</p>
          <p>二次 Duhamel 展开同时给出</p>
          <div class="equation result">\[
            z(a)=-a^2\tau F_*+O(a^3),\qquad
            F_*(u^a(\tau))=a^2e^{-2\nu\tau}F_*+O(a^3)\ne0.
          \]</div>
          <p>这不是 backward NSE，也不要求完整流映射在无限维空间局部满射；只使用光滑初值的标准正向局部流和一个有限维投影。</p>
          <p>事件时 \(W_*(\tau)=0\)，滤波涡量方程给 \(C_t(\tau)=-\Delta F_*(u^a(\tau))\)，于是 \(\langle F_*,C_t\rangle=\|\nabla F_*\|_2^2>0\)。零点为一阶、\(A_-=0\)，且</p>
          <div class="equation result">\[
            \kappa^{-2}A_+(a)=\frac{a^2e^{-2\nu\tau}}4+O(a^3).
          \]</div>
          <p>任意非负 covering partition 至少有一格满足 \(\langle F,c_Q\rangle=\int\chi_Q|\operatorname{curl}F|^2>0\)。该正号依赖 full-shell root；一般 localized zero 仍有 cutoff commutator，不能据此排除 even touch。</p>
        </section>

        <section id="scaling"><div class="section-no">02 / Internal scaling no-go</div><h2>atom 是 λ⁻⁴，bare budget 是 λ⁻⁶</h2>
          <p>base family 在 \([0,2\tau)\) 上满足</p>
          <div class="equation">\[
            R(a)=\int_0^{2\tau}\frac{\|L^a\|_{\dot H^{-1}}^2}{Y^a}\,dt
            =\frac{a^2(1-e^{-4\nu\tau})}{16\nu}+O(a^3).
          \]</div>
          <p>先取 \(a_\lambda=\lambda^{-2}\)，再作 \(u_\lambda(x,t)=\lambda u^{a_\lambda}(\lambda x,\lambda^2t)\)。内部事件移动到 \(\tau/\lambda^2\)，仍严格位于协变窗口内部。精确主阶为</p>
          <div class="equation result">\[
            a_{\beta,\lambda}=\frac{e^{-2\nu\tau}}{4\lambda^4}+O(\lambda^{-6}),
            \qquad
            R_\lambda=\frac{1-e^{-4\nu\tau}}{16\nu\lambda^6}+O(\lambda^{-8}),
          \]</div>
          <div class="equation result">\[
            \frac{a_{\beta,\lambda}}{R_\lambda}
            =\frac{2\nu}{\sinh(2\nu\tau)}\lambda^2+o(\lambda^2).
          \]</div>
          <p>同时 \(\|u_\lambda(0)\|_2^2=O(\lambda^{-2})\)、\(\|u_\lambda(0)\|_{\dot H^{1/2}}^2=O(\lambda^{-1})\)、\(\|\omega_\lambda(0)\|_2^2=1+o(1)\)。该 no-go 不是初始能量增长造成的。</p>
        </section>

        <section id="occupation"><div class="section-no">03 / Outgoing occupation</div><h2>尺度匹配的表示存在，但 Leray payment 尚未建立</h2>
          <p>对有限个孤立有限阶 internal zeros，令 \(r=\|C\|_2\)、\(\xi=C/r\)、\(q=\langle F,\xi\rangle_+^2/Y\)。任取单位质量的一侧 mollifier \(\rho_\delta\)，有 outgoing coarea identity</p>
          <div class="equation result">\[
            \sum_{\alpha,t_*}\kappa_j^{-2}A_{\alpha,+}(t_*)
            =\lim_{\delta\downarrow0}\sum_\alpha\kappa_j^{-2}
            \int q_\alpha\rho_\delta(r_\alpha)(r_{\alpha,t})_+\,dt.
          \]</div>
          <p>它对 odd crossing 与 even touch 都成立，且 NSE 给 \(r_t=\langle\xi,G\rangle-\nu\|\nabla C\|_2^2/r\)。但 \(\rho_\delta(r)\) 在零层附近按 δ⁻¹ 集中，普通 \(L_t^pG\) 上界不能统一支付该极限。因此这里是精确 representation，不是 a priori occupation theorem。</p>
        </section>

        <section id="trace"><div class="section-no">04 / Trace and variation</div><h2>无 sampling coherence 的有限条件定理保留三个 strong ledgers</h2>
          <p>对固定 entry direction 与对称窗口 \(h=\theta\kappa^{-2}\)，三角核恒等式给出</p>
          <div class="equation">\[
            \kappa^{-2}A_+
            \le\frac1{2\theta}\int q\,dt
            +\frac{\kappa^{-2}}2\int|q_t|\,dt.
          \]</div>
          <p>精确求导必须保留 \(f_t=\langle F_t,e\rangle/\sqrt Y-(Y_t/2Y)f\)。在 finite active-direction Bessel 条件下可求和，但右端包含 strong \(\|F_j\|_2^2/Y\)、\(\kappa_j^{-2}\|F_j\|_2\|F_{j,t}\|_2/Y\) 与 normalized \(Y_t\) variation。三项尺度都正确，却都不是 ordinary Leray budget；重复方向还会使 Bessel 常数增长。</p>
        </section>

        <section id="literature"><div class="section-no">05 / Primary-source boundary</div><h2>现有定理支付能量、平均 flux 或幅度 excursion，不支付裸零级 entry</h2>
          <p><a href="https://doi.org/10.1007/BF00276188">Fujita–Kato</a>、<a href="https://doi.org/10.1007/BF01174182">Kato</a>与 <a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持本节使用的局部强流映射。<a href="https://doi.org/10.1002/cpa.3160350604">CKN</a>控制 local energy 与 singular set，<a href="https://arxiv.org/abs/1101.2193">Dascaliuc–Grujić</a>控制 ensemble/time-averaged flux，<a href="https://math.berkeley.edu/~tataru/papers/nas.pdf">Koch–Tataru</a>控制 critical upper Carleson norms；这些结论都不为每次 smooth coefficient zero 提供 lower charge。</p>
          <p><a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>与 <a href="https://arxiv.org/abs/1503.01746">Łochowski</a>支持 level-averaged occupation 或 positive-height crossings。固定 smooth packet 的 amplitude-weighted excursions 确实由 Leray energy 支付；raw zero-entry count 不受 BV 或 W¹,² 控制。两轮 bounded audit 未定位到完整 raw-entry theorem；这不是原创性、优先权或不存在性声明。</p>
        </section>

        <section id="audit"><div class="section-no">06 / Exact and independent audit</div><h2>符号证书与独立 FFT / quadrature 重建分别通过</h2>
          <p>exact producer 用 sparse rational Fourier 与 SymPy 检查八组对象；independent checker 用 32³ FFT、adaptive quadrature、finite differences 与 λ=1…128 的直接 sweep 重建六组对象。coarea 最大单位质量残差为 \(6.661\times10^{-16}\)，trace residual 为 \(1.110\times10^{-16}\)，ratio/λ² 最大相对残差为 \(3.559\times10^{-16}\)。</p>
          <p>IFT 是 continuum analytic theorem，不由脚本替代。有限 Galerkin 只复核 root shooting、横穿方向与渐近量级。</p>
        </section>

        <section id="figure"><div class="section-no">07 / Journal figure</div><h2>附图把预补偿、内部横穿、原子与双尺度 no-go 分开显示</h2>
          <figure><img src="/figures/r0-71t-internal-entry.svg" alt="R0.71T 有限 Galerkin 内部 entry、预补偿、entry atom 与双尺度缩放"><figcaption>图 R0.71T。A：预补偿范数相对二次 Duhamel 主项收敛。B：目标壳主系数在预定正时间过零，横向残差保持在求根容差内。C：finite Galerkin entry atom 与 slope-charge identity 一致，并向小时间种子值 1/4 靠近。D：双尺度主阶 atom 为 λ⁻⁴、bare budget 为 λ⁻⁶、比值为 λ²。A–C 是 finite Fourier–Galerkin corroboration；D 是解析主阶重建；均不是 DNS。</figcaption></figure>
        </section>

        <section id="value"><div class="section-no">08 / Research value</div><h2>价值是把一个边界疑问变成严格内部 no-go</h2>
          <p>R0.71S 仍可能被质疑为“只在起始面失败”。R0.71T 用正向 NSE 流和有限维 IFT 消除了这个疑问：同一尺度错配在 genuine internal entry 上出现，而且数据的能量尺度更好。这个结论足以停止 bare \(H^{-1}\)-Lamb time integral 的继续包装，避免在不同 temporal kernels 上重复支付同一两阶税。</p>
          <p>正面价值同样明确。global-shell positive entries 自动 simple；outgoing coarea 给出 even-touch-safe 的尺度零 representation；fixed-packet amplitude excursions 给出真实 Leray-paid 替代对象。</p>
        </section>

        <section id="next"><div class="section-no">09 / Next finite gate</div><h2>R0.71U 检查 global-shell jet 与 outgoing occupation 能否求和</h2>
          <p>下一步首先研究 simple global entries 的 instantaneous jet</p>
          <div class="equation">\[
            q_\beta^{\rm jet}=\kappa_j^{-6}\frac{\|C_t(t_\beta)\|_2^2}{Y(t_\beta)}.
          \]</div>
          <p>它与 entry atom 同尺度，并在单半径 full-shell root 上精确等价。有限任务是证明一个 summed/Carleson estimate，或构造 recurrence family 排除它。并行保留 amplitude-thresholded excursion 这一保守 Leray-paid 分支。</p>
        </section>

        <section id="claims"><div class="section-no">10 / Claim boundary</div><h2>本节证明什么，也明确不证明什么</h2>
          <ul>
            <li><strong>已证明：</strong>真实 smooth positive-time exact-target internal entry；与 seed 分离的完整有限目标支撑扩展；至少一个 induced local positive cell；global positive entry 自动 simple；bounded-energy/enstrophy internal scaling no-go；finite outgoing-coarea identity；finite conditional trace-variation theorem。</li>
            <li><strong>未证明：</strong>outgoing occupation 的 Leray payment、jet sum、recurrence packing、任意 localized root 的 simplicity、continuation criterion、finite-time singularity 或 global regularity。</li>
            <li><strong>no-go 边界：</strong>只排除所有 smooth 解上、covariant frame/window 下、常数沿该解族一致、RHS 恰为 bare normalized \(\dot H^{-1}\)-Lamb time integral 的定理。</li>
            <li><strong>计算边界：</strong>Galerkin 图是截断 ODE 复核；continuum existence 与 no-go 来自解析证明和精确 NSE scaling。</li>
          </ul>
        </section>

        <section id="reproduce"><div class="section-no">11 / Reproduce</div><h2>报告、文献、证书、进度日志与独立 checker 全部保留</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_independent_audit.md">独立审计说明</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071t">exact / independent 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071t-internal-entry/fig-r071t-internal-entry">附图、数据、manifest、progress 与源代码包</a> · <a href="/figures/r0-71t-internal-entry.pdf">期刊附图 PDF</a></p>
          <p><a href="/notes/r0-71t.pdf">下载同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-71t.html">阅读 R0.60 之后累计回顾</a> · <a href="/recap-r0-61-r0-71t.pdf">下载累计回顾 PDF</a></p>
          <pre><code>python3 research/r071t_exact_audit.py
python3 research/r071t_independent_audit.py
python3 figures/r071t-internal-entry/fig-r071t-internal-entry/validate_data.py
python3 figures/r071t-internal-entry/fig-r071t-internal-entry/independent_validate.py</code></pre>
        </section>
      </article>
    </div>
  </main>
  <footer><div>R0.71T · 2026-08-26 · 个人数学研究日志<br><a href="/">返回研究主页</a> · <a href="/literature-review.html">文献综述</a> · <a href="/recap-r0-61-r0-71t.html">累计回顾</a></div></footer>
</body>
</html>
`;

if (/我们/.test(html)) throw new Error("R0.71T note must use singular or neutral voice");
for (const token of [
  "D_z\\Phi(0,0)=e^{-2\\nu\\tau}I",
  "\\frac{2\\nu}{\\sinh(2\\nu\\tau)}\\lambda^2",
  "outgoing coarea identity",
  "不是 a priori occupation theorem",
  "这不是千禧年问题的解答",
]) {
  if (!html.includes(token)) throw new Error("missing R0.71T boundary: " + token);
}
for (const forbidden of ["Millennium problem solved", "global regularity 已证明"]) {
  if (html.includes(forbidden)) throw new Error("R0.71T overclaim remains: " + forbidden);
}

await mkdir(publicFigureDirectory, { recursive: true });
await Promise.all(
  ["svg", "pdf", "png"].map((extension) =>
    copyFile(
      resolve(figureSource, "figure." + extension),
      resolve(publicFigureDirectory, "r0-71t-internal-entry." + extension),
    ),
  ),
);
await writeFile(notePath, html);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71T",
      note: notePath,
      publicFigures: ["svg", "pdf", "png"],
      next: "R0.71U",
    },
    null,
    2,
  ),
);
