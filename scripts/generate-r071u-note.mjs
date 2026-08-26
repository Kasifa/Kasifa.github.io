import { access, copyFile, mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const notePath = resolve(root, "public/notes/r0-71u.html");
const figureSource = resolve(
  root,
  "figures/r071u-second-jet/fig-r071u-recurrence-packing",
);
const publicFigureDirectory = resolve(root, "public/figures");

await Promise.all([
  access(resolve(root, "research/r071u_report-source.md")),
  access(resolve(root, "research/r071u_gap_matrix.md")),
  access(resolve(root, "research/r071u_literature_audit.md")),
  access(resolve(root, "research/r071u_independent_audit.md")),
  access(resolve(root, "research/certificates/r071u/result.json")),
  access(resolve(root, "research/certificates/r071u/independent-result.json")),
]);

const html = String.raw`<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="description" content="研究笔记 R0.71U：Hilbert 零点采样给出 classical trajectory 上的 all-shell 二阶时间 jet 求和；真实无外力 2.5D NSE 解可在任意给定有限时刻返回同一紧支撑环带。">
  <meta property="og:type" content="article">
  <meta property="og:title" content="R0.71U｜二阶时间 jet 求和与真实有限 recurrence">
  <meta property="og:description" content="零点数无关的 Hilbert 采样、classical second-jet packing、Leray 边界、真实 2.5D NSE recurrence 与 shrinking-atom 边界。">
  <meta property="og:image" content="https://kasifa.github.io/figures/r0-71u-recurrence-packing.png">
  <title>R0.71U｜二阶时间 jet 求和与真实有限 recurrence</title>
  <script>window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.90">
  <style>.hero h1{font-size:clamp(1.68rem,3.6vw,3rem)}@media print{#reproduce{break-inside:avoid}}</style>
  <script defer src="/i18n-en.js?v=1.06"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner">
    <a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a>
    <nav><a href="#result">结论</a><a href="#sampling">采样</a><a href="#theorem">定理</a><a href="#ledger">账本</a><a href="#recurrence">回返</a><a href="#atoms">原子</a><a href="#correction">更正</a><a href="#literature">文献</a><a href="#audit">审计</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>
  </div></header>
  <main>
    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.71U · SECOND-TIME JET · EXACT RECURRENCE</div>
        <h1>二阶时间 jet 可以求和，<br>raw recurrence 不能计数</h1>
        <p class="lead">本节得到两个互补结论。对满足 \(\inf_KY&gt;0\) 的紧 classical 轨道区间，Hilbert 值零点采样把所有 global-shell positive entries 统一压到一阶与二阶时间 jet 的积分；常数不依赖零点数、最小间距或有限壳截断。第一行可由 normalized Leray–Lamb 账本支付，第二行保留 \(\omega_t\) 与 \(L_t\) 的 recurrence tax，因此不是 Leray-level closure。另一方面，一个真实、无外力、全局光滑的 2.5D NSE 不变类可在任意指定的有限时刻返回同一紧支撑环带；初始能量和 enstrophy 可统一限制在单位球内，但这些 entry atom 可以缩小。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.71U 两条定理完成</span><strong>classical second-jet bound；finite recurrence</strong><p>版本 v0.71U · 2026-08-26</p><p>exact audit: PASS</p><p>independent audit: PASS</p><p>2.5D lattice: corroboration</p><p>下一对象：weighted recurrence / excursion</p></div>
    </div></header>
    <div class="layout">
      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 本节判断</a></li><li><a href="#sampling">01 · 零点采样</a></li><li><a href="#theorem">02 · all-shell 定理</a></li><li><a href="#ledger">03 · NSE 账本</a></li><li><a href="#recurrence">04 · 真实 recurrence</a></li><li><a href="#atoms">05 · shrinking atom</a></li><li><a href="#correction">06 · R0.71T 更正</a></li><li><a href="#literature">07 · 文献边界</a></li><li><a href="#audit">08 · 双重审计</a></li><li><a href="#figure">09 · 正式附图</a></li><li><a href="#value">10 · 研究价值</a></li><li><a href="#next">11 · 下一步</a></li><li><a href="#claims">12 · 主张边界</a></li><li><a href="#reproduce">13 · 复现</a></li>
      </ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Direct verdict</div><h2>weighted jet 有 classical 求和定理，raw count 在真实 NSE 中无统一界</h2>
          <div class="boundary"><strong>本节判断</strong><p>global-shell entry 的 weighted mass 可以在 compact classical interval 上统一求和，但要支付二阶时间 jet。相反，在单位 energy–enstrophy ball 内，raw entry count 与 minimum separation 都不能由初值的这两个数统一控制。后一个结论不反驳前一个：构造中的 atom 可随 entry 数增加而缩小。</p></div>
          <p>这不是千禧年问题的解答。本节没有得到弱解零点 trace、继续性判据、有限时奇性或全局正则性。</p>
        </section>

        <section id="sampling"><div class="section-no">01 / Hilbert zero sampling</div><h2>连续零点之间的平均导数为零，免去 zero-spacing 常数</h2>
          <p>令 \(X\in H^2(I;H)\)，\(I\) 的长度为 \(\ell\)，并取任意有限个有序零点 \(X(t_k)=0\)；classical trace 允许零点落在闭区间端点。则</p>
          <div class="equation result">\[
            \sum_k\|X'(t_k)\|_H^2
            \le \frac2\ell\int_I\|X'\|_H^2\,dt
            +\frac{7\ell}{3}\int_I\|X''\|_H^2\,dt.
          \]</div>
          <p>首个样本由 \(H^1\) point trace 支付。对后续样本，连续两个零点给出 \(\int_{t_{k-1}}^{t_k}X'=0\)；精确积分公式和 Cauchy–Schwarz 把它压到互不相交的 gap 上。这里的 \(\ell\) 是整个审计区间长度，不是最小零点间距、Voronoi 半径或假设的 forward window。证明没有使用错误的 vector-valued Rolle theorem。</p>
        </section>

        <section id="theorem"><div class="section-no">02 / All-shell theorem</div><h2>在 \(\inf_KY&gt;0\) 的 classical 区间上，常数与零点数和壳截断无关</h2>
          <p>对 compact classical interval \(K\)，记 \(\ell=|K|\)、\(\mathcal R_Y(K)=\sup_KY/\inf_KY\)。在统一 annular support 与 upper frame bound 下，任意有限壳集 \(\Lambda\) 满足</p>
          <div class="equation result">\[
          \begin{aligned}
            \mu_{J,\Lambda}(K)\le c_0^{-4}\mathcal R_Y(K)\Bigg[&
            \frac2\ell\int_K\frac1Y\sum_{j\in\Lambda}\kappa_j^{-6}\|C_{j,t}\|_2^2\,dt\\
            &+\frac{7\ell}{3}\int_K\frac1Y\sum_{j\in\Lambda}\kappa_j^{-6}\|C_{j,tt}\|_2^2\,dt\Bigg].
          \end{aligned}
          \]</div>
          <p>正项可用 monotone convergence 延伸到 countable shells。该定理是 trajectory-wise classical estimate，明确要求 \(0&lt;\inf_KY\le\sup_KY&lt;\infty\)。它不是弱解定理，也不是标准的 \(|K|\)-Carleson estimate。</p>
        </section>

        <section id="ledger"><div class="section-no">03 / NSE ledger</div><h2>第一行是 Leray-level，第二行是尚未关闭的 recurrence tax</h2>
          <div class="equation result">\[
            \sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2
            \lesssim \nu^2Y+\|L\|_{\dot H^{-1}}^2,
          \]</div>
          <div class="equation result">\[
            \sum_j\kappa_j^{-6}\|C_{j,tt}\|_2^2
            \lesssim \nu^2\|\omega_t\|_2^2+\|L_t\|_{\dot H^{-1}}^2.
          \]</div>
          <p>除以 \(Y\) 后，第一行由 normalized Leray–Lamb ledger 加上 \(\nu^2|K|\) 控制；前面的 \(|K|^{-1}\) 是支付每壳首个 trace 所需的尺度。第二行只在 classical solution 上有限，ordinary Leray energy inequality 不控制 \(\omega_t\) 或 \(L_t\)。对 exact torus scaling，只使用 integer \(\lambda\) 并协变运输 time window 与 multiplier frame；两行连同 entry mass 都具有零尺度指数。</p>
          <p>同一时刻的所有 global-shell positive roots 还满足 \(\sum_jJ_j(t)\lesssim\|L(t)\|_{\dot H^{-1}}^2/Y(t)\)。真正困难是不同时间的 recurrence，而不是 same-time spatial batching。</p>
        </section>

        <section id="recurrence"><div class="section-no">04 / Exact 2.5D recurrence</div><h2>每个给定 finite time set 都可选择一个新的真实无外力 NSE 解</h2>
          <p>取精确不变类</p>
          <div class="equation result">\[
            u(x,y,z,t)=(f(y,z,t),0,v(y,t)),\qquad
            v_t=\nu v_{yy},\quad f_t+vf_z=\nu(f_{yy}+f_{zz}).
          \]</div>
          <p>它是三维不可压 NSE 的全局光滑无外力子类，不是 forced surrogate。对任意 \(N\ge1\) 和 \(0&lt;t_1&lt;\cdots&lt;t_N&lt;T\)，选择 \(2N+1\) 个 shear 参数。响应函数</p>
          <div class="equation">\[
            \phi_\ell(t)=e^{-\mu t}\frac{1-e^{-\beta_\ell t}}{\beta_\ell}
          \]</div>
          <p>构成 Chebyshev system。有限维隐函数定理据此给出一个参数曲线，使同一 compact real-even annular multiplier 的完整声明投影在每个 \(t_m\) 精确归零，并且每个零点都是 first-order positive entry。</p>
          <p>量词必须保持清楚：每个 finite set 和每个 \(N\) 可以选择一个新解。这里没有构造一条固定轨道去实现无限或任意可延长的 prescribed time set。</p>
        </section>

        <section id="atoms"><div class="section-no">05 / Uniform ball and atom boundary</div><h2>raw count 无统一界，但 weighted atom 可以塌缩</h2>
          <p>缩放 passive component 后，再沿足够小的隐函数曲线取非零点，可同时保证</p>
          <div class="equation result">\[
            \|u_0\|_2^2\le1,\qquad \|\omega_0\|_2^2\le1,
          \]</div>
          <p>并保留至少 \(N\) 个指定的 positive entries。因此 unit energy–enstrophy ball 上不存在 raw global-shell entry count 的统一上界，也没有统一 minimum separation。另一方面，沿小参数 \(s\)，每个原子只满足</p>
          <div class="equation result">\[
            J_{*,m}(s)=\frac{2|m_*|^2|g'(t_m)|^2}{\kappa_*^2Y_0(t_m)}s^2+O(s^3)&gt;0.
          \]</div>
          <p>admissible radius、插值斜率与 passive amplitude 都可能随 \(N\) 变小。这不是 weighted-atom counterexample，也没有排除未知的 Leray-paid packing law。</p>
        </section>

        <section id="correction"><div class="section-no">06 / R0.71T projection boundary</div><h2>四模 thin projection 与完整有限支撑是两个精确表述</h2>
          <p>R0.71T 的原始 IFT 变量精确覆盖 \(|k|^2=2\) 的 real-conjugate four-mode projection；它不能单凭四模 cancellation 推出一个含其他 active modes 的宽 annulus 为零。对与 seed shell 分离的 compact target support，可把 IFT 变量空间扩为该支撑上的完整有限维 real divergence-free space。此时</p>
          <div class="equation result">\[
            D_z\Phi(0,0)=e^{\nu\tau\Delta}|_{E_j}
          \]</div>
          <p>是对角可逆矩阵，可以同时消去每个 target-support mode。这个更正不改变 R0.71T 的 exact-thin theorem 或 scaling no-go。</p>
        </section>

        <section id="literature"><div class="section-no">07 / Primary-source boundary</div><h2>文献支持工具与 2D3C 背景，不替代本节证明</h2>
          <p><a href="https://doi.org/10.3792/pja/1195521421">Masuda</a>与 <a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持 classical trajectory 上的时间解析性与强解背景。<a href="https://doi.org/10.1140/epje/i2018-11612-1">Linkmann–Buzzicotti–Biferale</a>记录 2D3C reduction；<a href="https://books.google.com/books?id=P7Y-AAAAIAAJ">Karlin–Studden</a>给出 Chebyshev-system interpolation 背景。<a href="https://doi.org/10.1007/s00021-004-0110-1">Agrachev–Sarychev</a>与 <a href="https://doi.org/10.1016/J.ANIHPC.2006.04.002">Shirikyan</a>研究带外力的 finite-dimensional projection controllability；本节只选择初值、演化无外力，并允许解随 finite time set 改变，量词不同。<a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给 critical upper Carleson control；<a href="https://doi.org/10.4064/fm-7-1-225-236">Banach</a>、<a href="https://doi.org/10.4064/cm6583-3-2017">Łochowski</a>与 <a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>处理 level-integrated crossings、variation 或 local time。这些文献不直接给 fixed zero-level normalized derivative mass 的求和定理。</p>
          <p>bounded literature audit 没有定位到与本节完整量词相同的结果。这只是限定范围内的检索结论，不是原创性、优先权或不存在性声明。</p>
        </section>

        <section id="audit"><div class="section-no">08 / Exact and independent audit</div><h2>解析账本与独立重建分别检查关键边界</h2>
          <p>exact audit 检查 zero-gap sampling、eigenshell jet identity、NSE scaling、2.5D 代数、response derivatives、modular support isolation 与 R0.71T full-support IFT boundary。independent audit 不读取 producer 结果，重建零点插值、cutoff refinement、非零 slopes 与 forced-path method test。</p>
          <p>数值 shooting 只用于复核一个 \(N=3\) 的 finite lattice 例子。continuum theorem、uniform energy–enstrophy construction 与 classical second-jet bound 都来自解析证明。</p>
        </section>

        <section id="figure"><div class="section-no">09 / Journal figure</div><h2>附图显示三次指定回返、cutoff 稳定性与 shrinking-atom 边界</h2>
          <figure><img src="/figures/r0-71u-recurrence-packing.svg" alt="R0.71U 2.5D NSE 有限 recurrence、目标零点、cutoff refinement 与 jet atom"><figcaption>图 R0.71U。固定 \(\nu=0.02\)、\(K=L=1\)、\(d=8\) 与三个指定时刻，有限 lattice shooting 把完整目标 annulus 的唯一共轭模对压到零；三个 target slopes 非零。主 cutoff 与独立加密给出一致结果。该图复核 finite example，不代替无限维 IFT、Hilbert sampling lemma 或 energy–enstrophy 量词。</figcaption></figure>
        </section>

        <section id="value"><div class="section-no">10 / Research value</div><h2>零点计数路线已经关闭，weighted recurrence 成为明确缺口</h2>
          <p>本节把 R0.71T 的二择一改写为更精确的边界。entry jet 的确可求和，但现有证明必须支付 \(C_{tt}\)；真实 NSE recurrence 又说明 analyticity、simplicity 或 bounded initial energy/enstrophy 不能提供统一 raw count。继续只研究零点数量不会关闭尺度零 packing。</p>
          <p>可利用的正面结构是 second-time-jet inequality。它给出一个与 NSE scaling 完全匹配的 benchmark，后续任何替代量都必须解释如何支付或避免 recurrence tax，同时保留 atom mass。</p>
        </section>

        <section id="next"><div class="section-no">11 / Next finite gate</div><h2>R0.71V 比较 atom mass、二阶 jet 与 level-integrated excursion</h2>
          <p>下一步量化 recurrence family 的 weighted atom sum 相对定理两行的大小，检查 \(C_{tt}\) tax 是否在该族上必要。并行测试 level-integrated 或 amplitude-thresholded excursions 能否用 genuine Leray-paid variation 代替 fixed zero-level charge。</p>
          <p>负面结果必须阻止 atom mass 塌缩；正面结果必须控制 distinguished zero level，不能只控制 almost every positive level。</p>
        </section>

        <section id="claims"><div class="section-no">12 / Claim boundary</div><h2>本节证明什么，也明确不证明什么</h2>
          <ul>
            <li><strong>已证明：</strong>global atom 与 first-time jet 的 annular comparability；same-time all-shell batching；零点数无关的 Hilbert sampling；带 positive enstrophy floor 的 classical all-shell second-time-jet theorem；真实 unforced 2.5D finite recurrence；unit energy–enstrophy ball 上 raw count 无统一界。</li>
            <li><strong>未证明：</strong>删除 second-time-jet tax；由 Leray energy 控制 \(\omega_t\) 或 \(L_t\)；weighted atom no-go；weak-solution jet trace；single-trajectory infinite recurrence；continuation、finite-time singularity 或 global regularity。</li>
            <li><strong>recurrence 量词：</strong>每个 finite time set 可选一个新的 smooth solution；不声称一条固定解实现所有集合。</li>
            <li><strong>计算边界：</strong>finite lattice figure 是可复现的 corroboration，不是 DNS，也不承担 continuum proof。</li>
          </ul>
        </section>

        <section id="reproduce"><div class="section-no">13 / Reproduce</div><h2>报告、文献、证书与期刊附图包全部保留</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_independent_audit.md">独立审计说明</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071u">exact / independent 证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071u-second-jet/fig-r071u-recurrence-packing">附图、数据、manifest、progress 与源代码包</a> · <a href="/figures/r0-71u-recurrence-packing.pdf">期刊附图 PDF</a></p>
          <p><a href="/notes/r0-71u.pdf">下载同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-71u.html">阅读 R0.60 之后累计回顾</a> · <a href="/recap-r0-61-r0-71u.pdf">下载累计回顾 PDF</a></p>
          <pre><code>python3 research/r071u_exact_audit.py
python3 research/r071u_independent_audit.py
python3 figures/r071u-second-jet/fig-r071u-recurrence-packing/validate_data.py
python3 figures/r071u-second-jet/fig-r071u-recurrence-packing/independent_validate.py</code></pre>
        </section>
      </article>
    </div>
  </main>
  <footer><div>R0.71U · 2026-08-26 · 个人数学研究日志<br><a href="/">返回研究主页</a> · <a href="/literature-review.html">文献综述</a> · <a href="/recap-r0-61-r0-71u.html">累计回顾</a></div></footer>
</body>
</html>
`;

if (/我们/.test(html)) throw new Error("R0.71U note must use singular or neutral voice");
for (const token of [
  "\\frac2\\ell\\int_I\\|X'\\|_H^2",
  "\\frac{7\\ell}{3}",
  "0&lt;\\inf_KY",
  "不是 Leray-level closure",
  "每个 finite set 和每个 \\(N\\) 可以选择一个新解",
  "这不是 weighted-atom counterexample",
  "D_z\\Phi(0,0)=e^{\\nu\\tau\\Delta}|_{E_j}",
  "这不是千禧年问题的解答",
]) {
  if (!html.includes(token)) throw new Error("missing R0.71U boundary: " + token);
}
for (const forbidden of [
  "Millennium problem solved",
  "global regularity 已证明",
  "一条固定轨道实现任意时间集",
]) {
  if (html.includes(forbidden)) throw new Error("R0.71U overclaim remains: " + forbidden);
}

await mkdir(publicFigureDirectory, { recursive: true });
await Promise.all(
  ["svg", "pdf", "png"].map((extension) =>
    copyFile(
      resolve(figureSource, "figure." + extension),
      resolve(publicFigureDirectory, "r0-71u-recurrence-packing." + extension),
    ),
  ),
);
await writeFile(notePath, html);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71U",
      note: notePath,
      publicFigures: ["svg", "pdf", "png"],
      next: "R0.71V",
    },
    null,
    2,
  ),
);
