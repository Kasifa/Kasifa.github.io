import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) {
        throw new Error(
          `${label}: expected one match, found ${count}: ${before.slice(0, 180)}`,
        );
      }
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) {
        throw new Error(
          `${label}: expected at least ${minimum} matches, found ${count}: ${before}`,
        );
      }
      value = value.split(before).join(after);
    },
    replaceBlock(start, end, after) {
      const count = value.split(start).length - 1;
      if (count !== 1) {
        throw new Error(`${label}: expected one block start, found ${count}: ${start}`);
      }
      const startIndex = value.indexOf(start);
      const endIndex = value.indexOf(end, startIndex + start.length);
      if (endIndex < 0) throw new Error(`${label}: block end not found: ${end}`);
      value =
        value.slice(0, startIndex) +
        after +
        value.slice(endIndex + end.length);
    },
    count(fragment) {
      return value.split(fragment).length - 1;
    },
    get value() {
      return value;
    },
  };
}

const releaseCard = String.raw`

          <div class="task-one" id="r071s" data-release="r071s" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71S · 2026-08-26</p>
            <h3>signed packet 能看见 entry，但裸 Leray 时间积分仍少两阶</h3>
            <p>
              对 \(h_\beta=\theta_\beta\kappa_{j_\beta}^{-2}\) 的 directional packet，sampling coherence 与有限 Bessel hypothesis 给出
              \[
                \sum_\beta a_\beta
                \le
                \frac{B_{\rm crit}}{\mu^2(1-\delta)^2\theta_-}
                \int\sum_j\kappa_j^{-2}\frac{\|F_j\|_2^2}{Y}\,dt.
              \]
              这是严格的 finite conditional theorem；sampling coherence、统一正 \(\theta_-\) 与 \(B_{\rm crit}\) 都没有从 NSE 中自动推出。
            </p>
            <p>
              非零均值 packet 的单包对角精确满足 \(B_{\rm crit}\ge\kappa_j^2\)。同向聚簇事件的最优有限常数是 Gram 矩阵的最大特征值，并随事件密度增长。反向热伴随对未归一化方向源 \(g=\langle F,e\rangle\) 的 strong norm 为常数；在 frozen-denominator 模型中，相对 Leray-order input \(\kappa^{-1}g\) 精确带回 \(\kappa^2\)。variable \(Y\) 还会产生 \(\sqrt Y\) 或 \(Y_t/(2Y)\) 项。一类 normalized bilinear temporal kernels 服从同一二分：非零均值看见 entry 并支付两阶；零均值漏掉常值 directional signal。even touch 还使双侧 signed face 完全抵消。
            </p>
            <p>
              R0.71O 的真实 smooth NSE initial face 经 compatible integer/dyadic dilation 后，\(\kappa^{-2}A_+=1/4\) 保持不变，而 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) 缩小为 \(\lambda^{-2}\)。因此，包含 observation-boundary entry、使用 covariant windows、且常数独立尺度的“原 positive-entry 目标 \(\le\) 裸时间积分”终局不可能成立。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节关闭的是原目标由 bare Leray time integral 支付的这一类 temporal-packet 方案。genuine NSE no-go 包含 initial observation face，不覆盖只计算 internal entries 的定理；这里没有构造 NSE 多进入轨道，也没有得到 continuation、singularity 或 global regularity。</p>
            <p>
              <a href="/notes/r0-71s.html"><strong>阅读 R0.71S 研究笔记 →</strong></a><br>
              <a href="/notes/r0-71s.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-71s-signed-packet.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071s">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071s_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071s-signed-packet/fig-r071s-signed-packet">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71s.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71s.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71T：</strong>&nbsp;移除 observation-boundary faces，只检查 internal entries 是否携带一个与 entry 原子同尺度、不是裸 \(dt\) 积分的 NSE-specific dynamical charge。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");

homeEdit.replace("<strong>v1.03</strong>网页版本", "<strong>v1.04</strong>网页版本");
homeEdit.replace("<strong>142</strong>公开研究笔记", "<strong>143</strong>公开研究笔记");
homeEdit.replace("<strong>R0.71R</strong>最新研究节点", "<strong>R0.71S</strong>最新研究节点");
homeEdit.replace(
  "<strong>signed / bilinear scale-critical incidence packet</strong>当前方向",
  "<strong>internal-entry scale-zero dynamical charge</strong>当前方向",
);
homeEdit.replace(
  String.raw`<div class="summary-item"><strong>我目前关注</strong><span>保留 entry direction 与 signed pairing，检查是否有 frame-summable、由 \(\dot H^{-1}\) 支付且 scale-covariant 的 bilinear packet；不把 certificate (3.3) 的两阶损失隐藏进新范数。</span></div>`,
  String.raw`<div class="summary-item"><strong>我目前关注</strong><span>移除 observation-boundary faces，只检查 internal entries 是否携带与原子同尺度的 NSE-specific dynamical charge；不再用裸 \(\dot H^{-1}\)-Lamb 时间积分支付尺度零目标。</span></div>`,
);
homeEdit.replace("Research topology · R0.1–R0.71R", "Research topology · R0.1–R0.71S");
homeEdit.replaceAll("/recap-r0-61-r0-71r.html", "/recap-r0-61-r0-71s.html");
homeEdit.replaceAll("/recap-r0-61-r0-71r.pdf", "/recap-r0-61-r0-71s.pdf");
homeEdit.replace('<span class="route-range">R0.69P–R0.71R</span>', '<span class="route-range">R0.69P–R0.71S</span>');
homeEdit.replace(
  "<h3>从有符号环带障碍走到 parabolic-incidence certificate boundary</h3>",
  "<h3>从有符号环带障碍走到 signed-packet scale–Bessel boundary</h3>",
);
homeEdit.replace(
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q 给出 finite conditional Jensen theorem。R0.71R 再导出 exact forced heat equation 与 conditional incidence packing，并证明 certificate (3.3) 的一参数 endpoint-square、termwise source-square 方案在 rho=0 scale covariance 与 rho=2 minimal Leray payment 之间存在精确两阶错配。</p>",
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–R 依次给出 finite conditional Jensen 与 incidence theorems。R0.71S 证明非零均值 signed/directional packet 的最优 Bessel 常数单包即带 κ²；frozen-denominator 反向热模型与一类 normalized bilinear kernels 不消去该代价。真实 NSE initial face 的协变缩放排除“原目标 + bare Leray time integral”的 observation-boundary 终局。</p>",
);
homeEdit.replace(
  "→ parabolic-incidence rho=0 / rho=2 boundary</p>",
  "→ parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary</p>",
);
homeEdit.replace("<summary>展开 52 篇公开笔记</summary>", "<summary>展开 53 篇公开笔记</summary>");
homeEdit.replace('aria-label="R0.69P–R0.71R"', 'aria-label="R0.69P–R0.71S"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71r.html">R0.71R</a>\n',
  '                  <a class="milestone" href="/notes/r0-71r.html">R0.71R</a>\n                  <a class="milestone" href="/notes/r0-71s.html">R0.71S</a>\n',
);
homeEdit.replaceBlock(
  '            <article class="tree-node next">',
  "            </article>",
  String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71T</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>internal-entry scale-zero dynamical charge</h3>
              <p>先排除 observation-boundary faces，只检查紧经典区间内部的 entries。候选 RHS 必须与 entry 原子同尺度，不能只是裸 \(dt\) 积分，也不能把 κ² 隐藏进 Bessel 常数。</p>
            </article>`,
);
homeEdit.replace(
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71R 路线放在同一张图中。",
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71S 路线放在同一张图中。",
);
homeEdit.replace("累计回顾 R0.61–R0.71R · 2026-08-26", "累计回顾 R0.61–R0.71S · 2026-08-26");
homeEdit.replace(
  "R0.60 recap 之后的累计回顾收录 82 个节点；全站现有 142 篇公开研究笔记",
  "R0.60 recap 之后的累计回顾收录 83 个节点；全站现有 143 篇公开研究笔记",
);
homeEdit.replace(
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen 与 parabolic-incidence scale audit。R0.70A–R0.71R 共 44 个完成版本。",
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen、parabolic incidence 与 signed-packet scale–Bessel audit。R0.70A–R0.71S 共 45 个完成版本。",
);
homeEdit.replace(
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71R 证明 finite conditional incidence theorem；在 rho=2 下，Leray energy 支付 source integral，frame constants 因 frame 固定而不依赖 finite truncation。完整右端仍可能因 upper comparison constant Gamma_2 与 essential overlap M 而不一致；theta_- 与 forward windows 是额外 theorem gates，不是右端因子。协变 optimal constant 的 rho=0 与 minimal Leray payment 的 rho=2 只构成 certificate (3.3) 的精确两阶边界。</p>",
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71S 的 finite directional-packet theorem 保留 sampling coherence、uniform positive height 与 Bessel hypotheses；单包 κ² lower bound、Gram clustering、frozen-denominator backward-heat exact norm 与 bilinear mean dichotomy 证明 bare Leray time integral 不能以尺度统一常数支付原目标。真实 NSE scaling 结论只覆盖 initial observation face；internal entries 仍开放。</p>",
);
homeEdit.replace(
  String.raw`<p><strong style="color:var(--gold)">下一步 R0.71S：</strong>&nbsp;保留 entry direction 与 signed pairing，检查是否存在 frame-summable、\(\dot H^{-1}\)-paid 且 scale-covariant 的 bilinear packet functional。</p>`,
  "<p><strong style=\"color:var(--gold)\">R0.71S 已完成：</strong>&nbsp;nonzero-mean directional packet、frozen-denominator backward heat 与限定 normalized bilinear kernels 都保留 κ² Bessel 税；genuine NSE initial-face scaling 排除原目标由 bare Leray time integral 统一支付的 observation-boundary 终局。</p>",
);
homeEdit.replace(
  "          </div>\n        </section>\n\n      </article>",
  "          </div>" + releaseCard + "\n        </section>\n\n      </article>",
);
homeEdit.replace("综述 v1.03 · 2026-08-26", "综述 v1.04 · 2026-08-26");
homeEdit.replace("上次综述 v1.02 · 2026-08-26", "上次综述 v1.03 · 2026-08-26");
homeEdit.replaceAll("/i18n-en.js?v=1.03", "/i18n-en.js?v=1.04");

if (homeEdit.count('data-release="r071s"') !== 1) {
  throw new Error("home: R0.71S release-card count is not one");
}
if (homeEdit.count('href="/notes/r0-71s.html"') !== 2) {
  throw new Error("home: expected exactly two R0.71S note links");
}
if (homeEdit.count("<summary>展开 53 篇公开笔记</summary>") !== 1) {
  throw new Error("home: route-note count is not 53");
}
if (/我们/.test(homeEdit.value)) throw new Error("home must use singular or neutral voice");
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const literatureEdit = editor(await readFile(literaturePath, "utf8"), "literature");
literatureEdit.replaceAll("/i18n-en.js?v=1.03", "/i18n-en.js?v=1.04");
literatureEdit.replaceAll("/recap-r0-61-r0-71r.html", "/recap-r0-61-r0-71s.html");
literatureEdit.replace(
  "本站 R0.69P–R0.71R 只列为研究笔记",
  "本站 R0.69P–R0.71S 只列为研究笔记",
);
literatureEdit.replace(
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71s.html">累计回顾与 82 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q 隔离 analytic/Jensen 四税；R0.71R 再证明 finite conditional parabolic-incidence theorem，并为 certificate (3.3) 定位 rho=0 scale covariance 与 rho=2 minimal Leray payment 的两阶错配。保留下来的结果都不是全局正则性结论。</p>',
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71s.html">累计回顾与 83 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S 再证明非零均值 directional packet 的 κ² Bessel 税，并用 genuine NSE initial-face scaling 排除 observation-boundary 版本的 bare Leray-time-integral 终局。保留下来的结果都不是全局正则性结论。</p>',
);
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71s.html#node-index">打开 82 节完整索引</a>',
  '<a href="/recap-r0-61-r0-71s.html#node-index">打开 83 节完整索引</a>',
);
literatureEdit.replace(
  String.raw`              <div class="route-step kept"><header><b>R0.71R</b><strong>certificate (3.3) 有精确两阶错配</strong></header><p>exact forced heat equation 与 finite conditional incidence theorem 成立。normalized zero-mean torus 上 rho=2 是 minimal Leray-paid index；对 finite covariant event/window family 定义的 least admissible optimal upper comparison constant 在协变 integer/dyadic dilation 下按 lambda^rho 缩放。initial Fourier example 只定义 Gamma_{2,jet} surrogate，不给 positive-time upper comparison constant Gamma_2 下界。<a href="/notes/r0-71r.html">研究笔记</a> <a href="/recap-r0-61-r0-71s.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71S</b><strong>signed / bilinear scale-critical packet</strong></header><p>保留 entry direction 与 signed pairing，检查能否绕开 certificate (3.3) 的两阶错配；其他 Duhamel designs 保持开放。</p></div>`,
  String.raw`              <div class="route-step kept"><header><b>R0.71R</b><strong>certificate (3.3) 有精确两阶错配</strong></header><p>exact forced heat equation 与 finite conditional incidence theorem 成立。normalized zero-mean torus 上 rho=2 是 minimal Leray-paid index；对 finite covariant event/window family 定义的 least admissible optimal upper comparison constant 在协变 integer/dyadic dilation 下按 lambda^rho 缩放。initial Fourier example 只定义 Gamma_{2,jet} surrogate，不给 positive-time upper comparison constant Gamma_2 下界。<a href="/notes/r0-71r.html">研究笔记</a></p></div>
              <div class="route-step closed"><header><b>R0.71S</b><strong>nonzero-mean packet 保留 κ² Bessel 税</strong></header><p>finite directional-packet theorem 成立，但单包对角、same-direction Gram clustering、backward heat 与限定 normalized bilinear kernels 都保留两阶或事件密度代价。genuine NSE initial-face scaling 排除 observation-boundary 版本的 bare Leray-time-integral 终局；internal entries 不在该 no-go 范围。<a href="/notes/r0-71s.html">研究笔记</a> <a href="/recap-r0-61-r0-71s.html">当前累计回顾</a> <a href="#r071s-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71T</b><strong>internal-entry scale-zero dynamical charge</strong></header><p>排除 initial observation faces 后，检查 localized Lamb–vorticity coupling 是否给 internal zero 一个与原子同尺度、不是裸 dt 积分的 dynamical charge。</p></div>`,
);
literatureEdit.replace(
  "<h3>R0.71R 关闭了什么，R0.71S 只检查什么</h3>",
  "<h3 id=\"r071s-boundary\">R0.71S 关闭了什么，R0.71T 只检查什么</h3>",
);
literatureEdit.replace(
  "same-direction Gram clustering、backward heat 与限定 normalized bilinear kernels 都保留两阶或事件密度代价。genuine NSE",
  "same-direction Gram clustering、frozen-denominator backward heat 与限定 normalized bilinear kernels 都保留两阶或事件密度代价。variable \\(Y\\) 的归一化项不属于该线性模型。genuine NSE",
);
literatureEdit.replace(
  String.raw`<p>R0.71R 从 localized observable 的 exact forced heat equation 出发，证明 finite conditional packing theorem。uniform 0&lt;theta_-&lt;=theta_beta&lt;=theta_* 与 forward-window availability 是 theorem gates，不是右端因子；Gamma_rho 是 upper comparison constant，1/Gamma_rho 编码 lower-charge strength，M 是 essential same-observable overlap。rho=2 是 normalized zero-mean torus 上的 minimal Leray-paid index：Leray energy 支付 source integral，frame constants 由固定 frame 给定；完整右端仍可能因 Gamma_2 与 M 而不一致。对对应 finite covariant event/window family，Gamma_rho^opt 定义为 least admissible upper comparison constant；固定 torus 上 compatible integer/dyadic dilation 必须协变搬运 multiplier、cutoff、event 与 window，且只有 Gamma_rho^opt 按 lambda^rho 缩放。整数 Fourier example 只定义 Gamma_{2,jet}=K^2/(4 theta^2) surrogate，不给 positive-time upper comparison constant Gamma_2 下界。certificate (3.3) 以外的 Duhamel designs 保持开放；R0.71S 只检查 signed / bilinear scale-critical packet。我继续用下面六条筛选。</p>`,
  String.raw`<p>R0.71S 保留 entry direction 与 signed pairing。finite directional-packet theorem 在 sampling coherence、uniform positive parabolic height 与 finite Bessel hypotheses 下成立；但 critical analysis vector 的单包对角已经给 B_crit&gt;=kappa^2，同向聚簇再使 Gram constant 按事件密度增长。backward heat 与一类 normalized bilinear temporal kernels 不消去该两阶；mean-zero/signed cancellation 则漏掉常值 directional signal 与 even touch。R0.71O 的 genuine NSE initial face 经 covariant scaling 后保持 weighted atom 不变，而 bare Leray time integral 按 lambda^-2 缩小。因此 observation-boundary 版本的原目标 + bare time integral 终局停止。R0.71T 只检查 internal entries 与 scale-zero dynamical charge。我继续用下面六条筛选。</p>`,
);
literatureEdit.replace(
  "增长。backward heat 与一类 normalized bilinear temporal kernels 不消去该两阶；mean-zero",
  "增长。frozen-denominator backward heat 与一类 normalized bilinear temporal kernels 不消去该两阶；variable \\(Y\\) 会带来额外归一化项，不能由这个线性模型处理。mean-zero",
);
literatureEdit.replace(
  String.raw`<div class="boundary"><strong>R0.71R 的一手文献边界</strong><p><a href="https://doi.org/10.1002/cpa.3160350604">Caffarelli–Kohn–Nirenberg</a>与<a href="https://doi.org/10.1016/j.aim.2024.109654">Lei–Ren</a>为 singularity / regularity cylinders 给 local-energy gate，不给 smooth filtered entry 的 lower charge。<a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给 parabolic square-Carleson upper norm；<a href="https://doi.org/10.1515/crll.1988.390.79">Angenent</a>的一维标量齐次 spatial zero-number law 还要求 uniform parabolicity、coefficient regularity、相应 boundary hypotheses 与 positive time。两者都不直接控制三维 Hilbert-valued forced observable 的 temporal entries。两轮限定检索未找到 uniform R0.71R incidence / overlap theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  String.raw`<div class="boundary"><strong>R0.71S 的一手文献边界</strong><p><a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给临界 parabolic bilinear map，<a href="https://doi.org/10.1016/0022-1236(85)90007-2">Coifman–Meyer–Stein</a>给 tent/Carleson integration，<a href="https://doi.org/10.1016/0022-1236(90)90137-A">Frazier–Jawerth</a>给 distribution pairings、smoothed samples 与 trace threshold，<a href="https://doi.org/10.1007/978-3-642-65161-8_3">Lions–Magenes</a>给 evolution endpoint pairing。它们不把 adaptive zero entry 变成由 bare Leray budget 支付的 uniform lower packet。普通 Leray–Hopf bounds 直接只给 L in L_t^(4/3) H_x^-1，不给 L_t^2 H_x^-1。两轮限定检索未找到完整 R0.71S theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
);
literatureEdit.replace("文献综述 v1.03 · 2026-08-26", "文献综述 v1.04 · 2026-08-26");

if (literatureEdit.count("<b>R0.71S</b>") !== 1) {
  throw new Error("literature: expected one R0.71S route node");
}
if (literatureEdit.count("开放接口 · R0.71T") !== 1) {
  throw new Error("literature: expected one R0.71T interface");
}
if (/我们/.test(literatureEdit.value)) {
  throw new Error("literature must use singular or neutral voice");
}
await writeFile(literaturePath, literatureEdit.value);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71S",
      siteVersion: "v1.04",
      publicNotes: 143,
      currentRouteNotes: 53,
      recapNodes: 83,
      completedReleasesR070AToR071S: 45,
      next: "R0.71T",
    },
    null,
    2,
  ),
);
