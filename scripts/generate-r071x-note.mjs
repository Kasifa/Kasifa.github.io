import { access, copyFile, mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const notePath = resolve(root, "public/notes/r0-71x.html");
const figureSource = resolve(
  root,
  "figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation",
);
const publicFigureDirectory = resolve(root, "public/figures");

await Promise.all([
  access(resolve(root, "research/r071x_report-source.md")),
  access(resolve(root, "research/r071x_gap_matrix.md")),
  access(resolve(root, "research/r071x_literature_audit.md")),
  access(resolve(root, "research/r071x_independent_audit.md")),
  access(resolve(root, "research/certificates/r071x/result.json")),
  access(resolve(root, "research/certificates/r071x/independent-result.json")),
  access(resolve(root, "research/certificates/r071x/truncated-coset-result.json")),
  ...["svg", "pdf", "png"].map((extension) =>
    access(resolve(figureSource, "figure." + extension)),
  ),
]);

const html = String.raw`<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="研究笔记 R0.71X：固定充分小耦合的 exact triangular 2.5D 家族在完整实时间根集上达到 D 的三分之一次方尺度；这是族内端点饱和，不是普适估计或正则性定理。">
  <meta property="og:type" content="article">
  <meta property="og:title" content="R0.71X｜固定小耦合与三分之一次方端点">
  <meta property="og:description" content="完整 prescribed-root atom sum 达到 D^(1/3) Lambda1 尺度；根完备性由 ECT、紧区间 C1 分离和半直线积分因子证明。">
  <meta property="og:image" content="https://kasifa.github.io/figures/r0-71x-endpoint-saturation.png">
  <title>R0.71X｜固定小耦合与三分之一次方端点</title>
  <script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.90">
  <style>.hero h1{font-size:clamp(1.68rem,3.6vw,3rem)}pre{max-width:100%;overflow-x:auto}@media print{#reproduce{break-inside:avoid}pre{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-size:7.5pt}}</style>
  <script defer src="/i18n-en.js?v=1.10"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#theorem">定理</a><a href="#ift">IFT</a><a href="#roots">根集</a><a href="#scales">尺度</a><a href="#ledger">账本</a><a href="#beta">指数</a><a href="#multiblock">多块</a><a href="#audit">审计</a><a href="#literature">文献</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.71X · FIXED SMALL COUPLING · ONE-THIRD ENDPOINT</div>
        <h1>固定充分小耦合达到三分之一次方尺度，<br>结论只属于声明的三角家族</h1>
        <p class="lead">本节回到 R0.71W 的 exact triangular 2.5D 不变类，把 rescaled coupling 固定为充分小的 \(\delta&gt;0\)，并取 \(\mathscr A_{q,\delta}=\delta q^2\)。统一 IFT 仍适用。完整实时间 target 根集恰好由预设的 \(N\) 个 simple roots 组成，complete atom sum 满足 \(\mathcal J_{q,\delta}\asymp\delta^2q^2\)，而初始数据量满足 \(D_{q,\delta}\asymp\delta^2q^6\)。因此该族在 \(D^{1/3}\Lambda_1\) 尺度上饱和，但没有给出普适端点估计。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.71X 完成</span><strong>declared-family endpoint saturation</strong><p>版本 v0.71X · 2026-08-26</p><p>analytic proof review: PASS</p><p>exact audit: 9/9</p><p>independent audit: 8/8</p><p>retained coset: 10/10</p><p>下一对象：growing-dimensional ECT / IFT</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节判断</a></li><li><a href="#theorem">01 · 端点定理</a></li><li><a href="#ift">02 · 固定小耦合</a></li><li><a href="#roots">03 · 完整根集</a></li><li><a href="#scales">04 · 精确尺度</a></li><li><a href="#ledger">05 · 完整账本</a></li><li><a href="#beta">06 · 指数三分</a></li><li><a href="#multiblock">07 · 多块边界</a></li><li><a href="#audit">08 · 三组审计</a></li><li><a href="#literature">09 · 文献边界</a></li><li><a href="#figure">10 · 正式附图</a></li><li><a href="#value">11 · 研究价值</a></li><li><a href="#next">12 · 下一步</a></li><li><a href="#claims">13 · 主张边界</a></li><li><a href="#reproduce">14 · 复现</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Direct verdict</div><h2>R0.71W 的下临界族可以推进到族内精确端点</h2>
          <div class="boundary"><strong>本节判断</strong><p>R0.71W 的 uniform IFT 允许固定的充分小 \(\delta\)，不要求 \(\delta_q\to0\)。取 \(\mathscr A_{q,\delta}=\delta q^2\) 后，完整 atom sum 与 \(D^{1/3}\Lambda_1\) 同阶。这是 fixed-dimensional local-IFT triangular family 的内部饱和定理。</p></div>
          <p>这不是三维 Navier–Stokes 全局正则性问题的解答，也不是对全部 triangular solutions 的 \(D^{1/3}\) 上界。</p>
        </section>

        <section id="theorem"><div class="section-no">01 / Endpoint theorem</div><h2>固定 \(\delta\) 后，完整 atom sum 保留非退化端点系数</h2>
          <p>存在 \(0&lt;\delta_*&lt;\delta_0\) 与 \(q_0\)，使每个 \(0&lt;\delta\le\delta_*\) 和充分大的 admissible \(q\) 都产生一条从 launch time 向前全局光滑、无外力的 exact triangular NSE 解，并且</p>
          <div class="equation result">\[
            D_{q,\delta}\asymp\delta^2q^6,\qquad
            \mathcal J_{q,\delta}\asymp\delta^2q^2,\qquad
            \nu^2\le\Lambda_1(I;u_{q,\delta})\le C_\Lambda(\nu^2+\delta^2).
          \]</div>
          <div class="equation result">\[
            \frac{\mathcal J_{q,\delta}}
            {D_{q,\delta}^{1/3}\Lambda_1(I;u_{q,\delta})}
            \asymp\delta^{4/3}.
          \]</div>
          <p>隐含常数可以依赖固定的几何、黏性、观察区间与 \(\delta_*\)，但不依赖声明范围内的 \(q\) 和 \(\delta\)。</p>
        </section>

        <section id="ift"><div class="section-no">02 / Uniform IFT branch</div><h2>物理振幅是 \(q^2\) 阶，小量仍是固定的 rescaled coupling</h2>
          <p>在 \(x=q^2(t-\sigma_q)\) 的 Fourier lattice 上，演化写成</p>
          <div class="equation result">\[
            \partial_xF_q=D_qF_q+\delta V_z(x)F_q,\qquad
            \mathscr A_{q,\delta}=\delta q^2.
          \]</div>
          <p>R0.71W 已经给出与 \(q\) 一致的局部 IFT 半径。只要固定 \(0&lt;\delta\le\delta_*\) 且 \(\delta_*\) 充分小，coefficient curve \(z_q(\delta)\) 与 simple-slope lower bound 都保持。这里没有把 coefficient-one 的 \(\delta=1\) 强行放进局部分支。</p>
        </section>

        <section id="roots"><div class="section-no">03 / Complete real-time roots</div><h2>ECT 零点预算、紧区间分离与半直线尾部共同排除额外根</h2>
          <p>极限目标 \(\Gamma\) 是常数加 \(N+1\) 个不同衰减指数。广义 Rolle 归纳证明这种非零 exponential polynomial 至多有 \(N+1\) 个实根，按重数计。已知的 \(0,\tau_1,\ldots,\tau_N\) 耗尽预算，因此全部 simple，且 \(\Gamma_\infty\ne0\)。</p>
          <p>固定紧区间上有 \(\|H_{q,\delta}-\Gamma\|_{C^1}\le\varepsilon_q+C\delta\)。根邻域内导数符号不变，补集上实部与零分离。半直线上再对 \(e^{\lambda_qx}H_{q,\delta}\) 使用积分因子；interaction kernel 可积，没有 \(\lambda_q^{-1}\) 损失，其极限趋于非零的 \(\Gamma_\infty\)。所以声明区间中的 real-time target roots 恰为预设的 \(N\) 个根。</p>
        </section>

        <section id="scales"><div class="section-no">04 / Exact scale ledger</div><h2>Parseval、根斜率和 enstrophy 给出两个独立的 \(q\) 次数</h2>
          <p>persistent background 给出 \(D\) 和 \(Y\) 的双侧界，根上的 exact multiplier normalization 给出</p>
          <div class="equation result">\[
            D_{q,\delta}\asymp Y_{q,\delta}\asymp\delta^2q^6,\qquad
            |\partial_ta_{q,\delta}(t_{m,q})|\asymp\delta^2q^4,\qquad
            J_{*,m,q,\delta}\asymp\delta^2q^2.
          \]</div>
          <p>固定 \(N\) 后求和不会改变次数。端点系数还可写成三个有统一上下界的 normalized factors 乘 \(\delta^{4/3}\)，所以这不只是形式上的 power count。</p>
        </section>

        <section id="ledger"><div class="section-no">05 / Complete first-row factor</div><h2>\(\Lambda_1\) 同时保留黏性 baseline 与 full-frequency rotational charge</h2>
          <div class="equation result">\[
            \Lambda_1(I;u)=\mathcal R_Y(I)\left[\nu^2+
            \frac1{|I|}\int_I\frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y}\,dt\right].
          \]</div>
          <p>该族满足 \(1\le\mathcal R_Y\le C\)，完整 rotational term 至多为 \(C\delta^2\)。因此 \(\Lambda_1\) 既不丢掉固定 \(\nu^2\) 项，也没有用 selected-shell proxy 替代全频 charge。</p>
        </section>

        <section id="beta"><div class="section-no">06 / Data-power trichotomy</div><h2>低于、等于和高于 \(1/3\) 的三种行为完全分开</h2>
          <p>对每个固定 \(0&lt;\delta\le\delta_*\)，</p>
          <div class="equation result">\[
            \frac{\mathcal J_{q,\delta}}
            {D_{q,\delta}^{\beta}\Lambda_1(I;u_{q,\delta})}
            \asymp_{\delta,\beta}q^{2-6\beta}.
          \]</div>
          <p>\(\beta&lt;1/3\) 时发散，\(\beta=1/3\) 时保持常数量级，\(\beta&gt;1/3\) 时被吸收。该三分只说明这一族对数据幂的分辨率，不证明 \(D^{1/3}\Lambda_1\) 支付任意解。</p>
        </section>

        <section id="multiblock"><div class="section-no">07 / Multiblock boundary</div><h2>固定维 small-coupling 分析没有产生端点以上的增益</h2>
          <p>多块审计区分 energy proxy 与 IFT 的真实 multiplication-operator parameter：</p>
          <div class="equation result">\[
            \varepsilon_N=\frac{P\sqrt{K_{v,N}}}{q^2}
            \ne
            \delta_{\mathrm{op},N}=\frac{P}{q^2}\sup_x\|V_{z_N}(x)\|.
          \]</div>
          <p>固定 \(N\) 的 selected-root 路线仍受 collective coupling 限制。growing \(N(q)\) 需要 quantitative ECT inverse、uniform IFT radius、weighted slope-energy 与完整 observability；strong-coupling Bessel 路线也仍只是后续候选。</p>
        </section>

        <section id="audit"><div class="section-no">08 / Three independent layers</div><h2>解析证明与三组有限计算承担不同职责</h2>
          <p>90 位 Decimal producer 通过 9/9，独立 binary64 重建通过 8/8，nonlinear retained-coset calculation 通过 10/10。后者复核根残差、\(q\) 次数、\(\delta^{4/3}\) collapse、截断稳定性与 finite tail sign。</p>
          <p>图和 retained-coset JSON 中的 <code>atomProxy</code> 不是 multiplier-locked \(J_*\)。数值选择 \(\delta=1/128\) 也没有被证明落在 continuum IFT 的量化半径内；解析定理只断言存在充分小的 \(\delta_*\)。</p>
        </section>

        <section id="literature"><div class="section-no">09 / Primary-source boundary</div><h2>文献中的三分之一次方、空间迹和时间解析性没有直接给出本节账本</h2>
          <p><a href="https://doi.org/10.1088/1361-6544/ab9246">Miller</a>给 whole-space cubic enstrophy ODE、显式 lifespan 与 small-data threshold；<a href="https://doi.org/10.1512/iumj.2008.57.3716">Lu–Doering</a>、<a href="https://doi.org/10.1017/jfm.2017.136">Ayala–Protas</a>和<a href="https://doi.org/10.1017/jfm.2020.204">Kang–Yun–Protas</a>研究极端 enstrophy growth；<a href="https://doi.org/10.4208/cmr.2021-0106">Lerner–Vigneron</a>给 projected Lamb identities；<a href="https://doi.org/10.1080/03605308108820180">Foias–Guillopé–Temam</a>的 \(H_2^{1/3}\in L_t^1\) 是高阶空间导数的时间可积指数，不是本节的初始数据幂。</p>
          <p><a href="https://doi.org/10.1007/BF02096982">Constantin</a>和<a href="https://doi.org/10.1016/j.jde.2025.113486">Yang</a>处理空间 level/trace；<a href="https://doi.org/10.1016/j.jmaa.2022.126428">Wang–Gao–Xue</a>给 time analyticity，但不提供由 \(D\) 支付 fixed temporal zero-slope sum 的定理。限定的一手来源检索没有发现直接重合；这不是原创性、优先权或不存在性声明。</p>
        </section>

        <section id="figure"><div class="section-no">10 / Journal figure</div><h2>附图把 \(q\) 次数、端点平台与 \(\delta^{4/3}\) collapse 分开显示</h2>
          <figure><img src="/figures/r0-71x-endpoint-saturation.svg" alt="R0.71X 固定小耦合端点尺度、三分之一次方平台和 delta 的三分之四次方 collapse"><figcaption>图 R0.71X-1。有限 retained-coset 数据显示 \(D\) 约为 \(q^6\)、complete two-root atomProxy 约为 \(q^2\)；独立高精度 ledger 显示 atomProxy 除以 \(D^{1/3}\) 的平台与 \(\delta^{4/3}\) collapse。atomProxy 不是 \(J_*\)，\(\delta=1/128\) 不是已认证的 continuum IFT 半径，图只作可复现 corroboration。</figcaption></figure>
        </section>

        <section id="value"><div class="section-no">11 / Research value</div><h2>端点已在一个 exact smooth family 内达到，但一般支付问题仍完整开放</h2>
          <p>R0.71W 只从下方逼近 \(1/3\)。本节证明固定充分小 prefactor 已经位于同一个 uniform IFT 分支中，并补上 complete real-time root set。于是 \(1/3\) 不再只是指数外推，而是声明家族内带非退化系数的 saturation law。</p>
          <p>它没有把一般奇性问题变成结论。下一项有信息量的门槛，是判断 growing-dimensional roots 或更强 coupling 能否在支付 exact operator norm 和完整 slope energy 后改变这个边界。</p>
        </section>

        <section id="next"><div class="section-no">12 / Next finite gate</div><h2>R0.71Y 检查 growing-dimensional ECT / IFT 与 weighted observability</h2>
          <p>下一节先量化随 \(N\) 增长的 exponential-Chebyshev inverse、coefficient curve 与 IFT 半径，再把 weighted slope-energy 和 full charge observability 放进同一账本。只有这些量同时闭合，\(\varepsilon_N^{4/3}\mathcal Q_N\) 才能被解释。</p>
          <p>strong-coupling Bessel/enhanced-dissipation 构造保留为更后的候选，不在 R0.71Y 预先当作已成立机制。</p>
        </section>

        <section id="claims"><div class="section-no">13 / Claim boundary</div><h2>本节证明什么，也明确不证明什么</h2>
          <ul>
            <li><strong>已证明：</strong>固定充分小 \(\delta\) 位于声明的 uniform-IFT branch；预设根构成完整 real-time target zero set；\(D\)、\(\mathcal J\)、\(\Lambda_1\) 的双侧尺度；族内 \(D^{1/3}\Lambda_1\) saturation 与 \(\beta\) 三分。</li>
            <li><strong>仍开放：</strong>growing-dimensional ECT/IFT、weighted slope-energy/observability、strong coupling、全部 triangular solutions 或一般三维解的 universal endpoint estimate。</li>
            <li><strong>没有得到：</strong>继续性判据、bounded-data no-go、有限时奇性或 global regularity。</li>
            <li><strong>计算边界：</strong>9/9、8/8、10/10 核对有限代数与数值层；continuum theorem 仍由解析证明承担。</li>
          </ul>
        </section>

        <section id="reproduce"><div class="section-no">14 / Reproduce</div><h2>报告、文献、证书与正式附图包全部保留</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_gap_matrix.md">多块与开放路线矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_independent_audit.md">独立审计说明</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071x">exact / independent / retained-coset 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation">附图、数据、manifest、validation 与源代码包</a> · <a href="/figures/r0-71x-endpoint-saturation.pdf">期刊附图 PDF</a></p>
          <p><a href="/notes/r0-71x.pdf">下载同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-71x.html">阅读 R0.60 之后累计回顾</a> · <a href="/recap-r0-61-r0-71x.pdf">下载累计回顾 PDF</a></p>
          <pre><code>python3 research/r071x_exact_audit.py --output research/certificates/r071x/result.json
python3 research/r071x_independent_audit.py --output research/certificates/r071x/independent-result.json
python3 research/r071x_truncated_coset_audit.py --output research/certificates/r071x/truncated-coset-result.json
python3 figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/produce_data.py --config figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/config.json
python3 figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/plot.py --config figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/config.json --output-stem figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/figure
python3 figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/validate.py --config figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/config.json --output figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/validation.json</code></pre>
        </section>
      </article>
    </div>
  </main>
  <footer><div>R0.71X · 2026-08-26 · 个人数学研究日志<br><a href="/">返回研究主页</a> · <a href="/literature-review.html">文献综述</a> · <a href="/recap-r0-61-r0-71x.html">累计回顾</a></div></footer>
</body>
</html>
`;

if (/我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/.test(html)) {
  throw new Error("R0.71X note must use singular or neutral voice");
}
for (const token of [
  "\\mathscr A_{q,\\delta}=\\delta q^2",
  "D_{q,\\delta}\\asymp\\delta^2q^6",
  "\\mathcal J_{q,\\delta}\\asymp\\delta^2q^2",
  "\\nu^2\\le\\Lambda_1",
  "\\asymp\\delta^{4/3}",
  "\\beta&lt;1/3",
  "\\delta_{\\mathrm{op},N}",
  "9/9",
  "8/8",
  "10/10",
  "atomProxy",
  "continuum IFT",
  "不是对全部 triangular solutions",
]) {
  if (!html.includes(token)) throw new Error("missing R0.71X boundary: " + token);
}

await mkdir(publicFigureDirectory, { recursive: true });
await Promise.all(
  ["svg", "pdf", "png"].map((extension) =>
    copyFile(
      resolve(figureSource, "figure." + extension),
      resolve(publicFigureDirectory, "r0-71x-endpoint-saturation." + extension),
    ),
  ),
);
await writeFile(notePath, html);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71X",
      note: notePath,
      publicFigures: ["svg", "pdf", "png"],
      next: "R0.71Y",
    },
    null,
    2,
  ),
);
