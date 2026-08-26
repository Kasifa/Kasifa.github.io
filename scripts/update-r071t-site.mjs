import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(value, label) {
  return {
    value,
    replace(before, after) {
      const count = this.value.split(before).length - 1;
      if (count !== 1) throw new Error(label + ": expected one match, found " + count);
      this.value = this.value.replace(before, after);
    },
    replaceAll(before, after) {
      const count = this.value.split(before).length - 1;
      if (count < 1) throw new Error(label + ": missing replacement token");
      this.value = this.value.replaceAll(before, after);
    },
    replaceBlock(start, end, replacement) {
      const startIndex = this.value.indexOf(start);
      if (startIndex < 0) throw new Error(label + ": start marker missing");
      const endIndex = this.value.indexOf(end, startIndex);
      if (endIndex < 0) throw new Error(label + ": end marker missing");
      this.value =
        this.value.slice(0, startIndex) +
        replacement +
        this.value.slice(endIndex + end.length);
    },
    count(token) {
      return this.value.split(token).length - 1;
    },
  };
}

const releaseCard = String.raw`

          <div class="task-one" id="r071t" data-release="r071t" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71T · 2026-08-26</p>
            <h3>真实正时间内部 entry 排除裸 Leray 时间支付</h3>
            <p>
              对 \(U=(0,\cos x_1,\cos x_2)\) 的 \(|k|^2=2\) 目标壳，标准局部 NSE 流映射与有限维 IFT 给出初值预补偿
              \[
                z(a)=-a^2\tau F_*+O(a^3),
              \]
              使整个目标壳在预定正时间 \(t=\tau\) 精确归零。事件 forcing 仍为 \(a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\)，所以该零点严格位于 observation window 内部、为 simple positive crossing，并满足
              \[
                \kappa^{-2}A_+(a)=\frac{a^2e^{-2\nu\tau}}4+O(a^3).
              \]
            </p>
            <p>
              取 base amplitude \(a_\lambda=\lambda^{-2}\) 再作 compatible NSE dilation。internal atom 为 \(\lambda^{-4}\)，bare normalized \(\dot H^{-1}\)-Lamb time budget 为 \(\lambda^{-6}\)，两者之比按
              \[
                \frac{2\nu}{\sinh(2\nu\tau)}\lambda^2
              \]
              发散；与此同时 initial energy 与 \(\dot H^{1/2}\) norm 趋零，enstrophy 保持有界。因此 bare time integral 的 scale-uniform internal-entry payment 被 genuine smooth NSE family 排除。
            </p>
            <p>
              finite outgoing-coarea identity 对 odd crossings 与 even touches 都精确保留 \(A_+\)，但其 zero-level mollifier concentration 尚无 Leray payment。finite trace-variation theorem 也成立，却保留 strong Lamb、\(F_t\)、\(Y_t\) 与 repeated-direction Bessel ledgers。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节没有得到 outgoing occupation packing、continuation、singularity 或 global regularity。no-go 只排除 covariant frame/window、常数沿该解族一致、RHS 恰为 bare normalized Leray-Lamb time integral 的声明类。</p>
            <p>
              <a href="/notes/r0-71t.html"><strong>阅读 R0.71T 研究笔记 →</strong></a><br>
              <a href="/notes/r0-71t.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-71t-internal-entry.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071t">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071t_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071t-internal-entry/fig-r071t-internal-entry">查看附图、数据、进度与源代码包</a> ·
              <a href="/recap-r0-61-r0-71t.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71t.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71U：</strong>&nbsp;检查 global-shell simple-entry jet 与 outgoing occupation 是否有 summed / Carleson payment；并行保留 amplitude-thresholded excursion 分支。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
homeEdit.replace("<strong>v1.04</strong>网页版本", "<strong>v1.05</strong>网页版本");
homeEdit.replace("<strong>143</strong>公开研究笔记", "<strong>144</strong>公开研究笔记");
homeEdit.replace("<strong>R0.71S</strong>最新研究节点", "<strong>R0.71T</strong>最新研究节点");
homeEdit.replace(
  "<strong>internal-entry scale-zero dynamical charge</strong>当前方向",
  "<strong>global-shell jet / outgoing occupation packing</strong>当前方向",
);
homeEdit.replace(
  String.raw`<div class="summary-item"><strong>我目前关注</strong><span>移除 observation-boundary faces，只检查 internal entries 是否携带与原子同尺度的 NSE-specific dynamical charge；不再用裸 \(\dot H^{-1}\)-Lamb 时间积分支付尺度零目标。</span></div>`,
  String.raw`<div class="summary-item"><strong>我目前关注</strong><span>检查 global-shell simple-entry jet 与 outgoing occupation 能否得到 summed / Carleson payment；bare normalized \(\dot H^{-1}\)-Lamb time integral 已被 genuine internal family 排除。</span></div>`,
);
homeEdit.replace("Research topology · R0.1–R0.71S", "Research topology · R0.1–R0.71T");
homeEdit.replaceAll("/recap-r0-61-r0-71s.html", "/recap-r0-61-r0-71t.html");
homeEdit.replaceAll("/recap-r0-61-r0-71s.pdf", "/recap-r0-61-r0-71t.pdf");
homeEdit.replace('<span class="route-range">R0.69P–R0.71S</span>', '<span class="route-range">R0.69P–R0.71T</span>');
homeEdit.replace(
  "<h3>从有符号环带障碍走到 signed-packet scale–Bessel boundary</h3>",
  "<h3>从有符号环带障碍走到 genuine internal-entry scale boundary</h3>",
);
homeEdit.replace(
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–R 依次给出 finite conditional Jensen 与 incidence theorems。R0.71S 证明非零均值 signed/directional packet 的最优 Bessel 常数单包即带 κ²；frozen-denominator 反向热模型与一类 normalized bilinear kernels 不消去该代价。真实 NSE initial face 的协变缩放排除“原目标 + bare Leray time integral”的 observation-boundary 终局。</p>",
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–S 给出 conditional Jensen/incidence 与 packet/Bessel scale audits。R0.71T 用正向局部 NSE 流映射和 finite-dimensional IFT 构造 genuine smooth positive-time internal entry；双尺度族把 atom 与 bare normalized Leray-Lamb time budget 分别压到 λ⁻⁴ 与 λ⁻⁶，从而关闭 initial-boundary caveat。outgoing coarea 保留为 scale-matched representation，但 summed payment 仍开放。</p>",
);
homeEdit.replace(
  "→ signed-packet scale / Bessel boundary</p>",
  "→ signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary</p>",
);
homeEdit.replace("<summary>展开 53 篇公开笔记</summary>", "<summary>展开 54 篇公开笔记</summary>");
homeEdit.replace('aria-label="R0.69P–R0.71S"', 'aria-label="R0.69P–R0.71T"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71s.html">R0.71S</a>\n',
  '                  <a class="milestone" href="/notes/r0-71s.html">R0.71S</a>\n                  <a class="milestone" href="/notes/r0-71t.html">R0.71T</a>\n',
);
homeEdit.replaceBlock(
  '            <article class="tree-node next">',
  "            </article>",
  String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71U</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>global-shell jet / outgoing occupation packing</h3>
              <p>检查 \(\kappa_j^{-6}\|C_t(t_\beta)\|_2^2/Y(t_\beta)\) 是否有 summed / Carleson estimate，或由 recurrence family 排除；并行保留 amplitude-thresholded excursion。</p>
            </article>`,
);
homeEdit.replace(
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71S 路线放在同一张图中。",
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71T 路线放在同一张图中。",
);
homeEdit.replace("累计回顾 R0.61–R0.71S · 2026-08-26", "累计回顾 R0.61–R0.71T · 2026-08-26");
homeEdit.replace(
  "R0.60 recap 之后的累计回顾收录 83 个节点；全站现有 143 篇公开研究笔记",
  "R0.60 recap 之后的累计回顾收录 84 个节点；全站现有 144 篇公开研究笔记",
);
homeEdit.replace(
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen、parabolic incidence 与 signed-packet scale–Bessel audit。R0.70A–R0.71S 共 45 个完成版本。",
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel 与 internal-entry scale audit。R0.70A–R0.71T 共 46 个完成版本。",
);
homeEdit.replace(
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71S 的 finite directional-packet theorem 保留 sampling coherence、uniform positive height 与 Bessel hypotheses；单包 κ² lower bound、Gram clustering、frozen-denominator backward-heat exact norm 与 bilinear mean dichotomy 证明 bare Leray time integral 不能以尺度统一常数支付原目标。真实 NSE scaling 结论只覆盖 initial observation face；internal entries 仍开放。</p>",
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71T 已构造 genuine smooth positive-time internal entry，并用 energy/critical norm 趋零、enstrophy 有界的双尺度族排除 bare normalized Leray-Lamb time integral 的 scale-uniform internal payment。outgoing coarea 是 exact scale-matched representation，但零层 concentration、jet summability 与 recurrence packing 仍开放。</p>",
);
homeEdit.replace(
  String.raw`<p><strong style="color:var(--gold)">下一步 R0.71T：</strong>&nbsp;移除 observation-boundary faces，只检查 internal entries 是否携带一个与 entry 原子同尺度、不是裸 \(dt\) 积分的 NSE-specific dynamical charge。</p>
          </div>
        </section>`,
  String.raw`<p><strong style="color:var(--gold)">R0.71T 已完成：</strong>&nbsp;finite-dimensional IFT 构造 genuine smooth positive-time internal entry；double scaling 排除 bare normalized Leray-Lamb time payment；outgoing coarea 保留为未闭合的 scale-matched charge。</p>
          </div>` + releaseCard + String.raw`
        </section>`,
);
homeEdit.replace("综述 v1.04 · 2026-08-26", "综述 v1.05 · 2026-08-26");
homeEdit.replace("上次综述 v1.03 · 2026-08-26", "上次综述 v1.04 · 2026-08-26");
homeEdit.replaceAll("/i18n-en.js?v=1.04", "/i18n-en.js?v=1.05");

if (homeEdit.count('data-release="r071t"') !== 1) throw new Error("home: R0.71T card count");
if (homeEdit.count('href="/notes/r0-71t.html"') !== 2) throw new Error("home: R0.71T note links");
if (homeEdit.count("<summary>展开 54 篇公开笔记</summary>") !== 1) throw new Error("home: route count");
if (/我们/.test(homeEdit.value)) throw new Error("home must use singular or neutral voice");
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const literatureEdit = editor(await readFile(literaturePath, "utf8"), "literature");
literatureEdit.replaceAll("/i18n-en.js?v=1.04", "/i18n-en.js?v=1.05");
literatureEdit.replaceAll("/recap-r0-61-r0-71s.html", "/recap-r0-61-r0-71t.html");
literatureEdit.replace(
  "本站 R0.69P–R0.71S 只列为研究笔记",
  "本站 R0.69P–R0.71T 只列为研究笔记",
);
literatureEdit.replace(
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71t.html">累计回顾与 83 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S 再证明非零均值 directional packet 的 κ² Bessel 税，并用 genuine NSE initial-face scaling 排除 observation-boundary 版本的 bare Leray-time-integral 终局。保留下来的结果都不是全局正则性结论。</p>',
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71t.html">累计回顾与 84 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–S 给出 finite conditional Jensen/incidence 与 packet/Bessel scale audits。R0.71T 再构造 genuine smooth positive-time internal entry，并排除 bare normalized Leray-Lamb time integral 的 scale-uniform internal payment。保留下来的结果都不是全局正则性结论。</p>',
);
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71t.html#node-index">打开 83 节完整索引</a>',
  '<a href="/recap-r0-61-r0-71t.html#node-index">打开 84 节完整索引</a>',
);
literatureEdit.replace(
  String.raw`              <div class="route-step closed"><header><b>R0.71S</b><strong>nonzero-mean packet 保留 κ² Bessel 税</strong></header><p>finite directional-packet theorem 成立，但单包对角、same-direction Gram clustering、frozen-denominator backward heat 与限定 normalized bilinear kernels 都保留两阶或事件密度代价。variable \(Y\) 的归一化项不属于该线性模型。genuine NSE initial-face scaling 排除 observation-boundary 版本的 bare Leray-time-integral 终局；internal entries 不在该 no-go 范围。<a href="/notes/r0-71s.html">研究笔记</a> <a href="/recap-r0-61-r0-71t.html">当前累计回顾</a> <a href="#r071s-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71T</b><strong>internal-entry scale-zero dynamical charge</strong></header><p>排除 initial observation faces 后，检查 localized Lamb–vorticity coupling 是否给 internal zero 一个与原子同尺度、不是裸 dt 积分的 dynamical charge。</p></div>`,
  String.raw`              <div class="route-step closed"><header><b>R0.71S</b><strong>nonzero-mean packet 保留 κ² Bessel 税</strong></header><p>finite directional-packet theorem 成立，但单包对角、same-direction Gram clustering、frozen-denominator backward heat 与限定 normalized bilinear kernels 都保留两阶或事件密度代价。genuine NSE initial-face scaling 只排除 observation-boundary 版本。<a href="/notes/r0-71s.html">研究笔记</a></p></div>
              <div class="route-step closed"><header><b>R0.71T</b><strong>genuine internal entry 保留同一两阶错配</strong></header><p>finite-dimensional IFT 构造 smooth positive-time full-shell root；double scaling 给 atom λ⁻⁴、bare budget λ⁻⁶。outgoing coarea 精确保留 entry，但 summed payment 未闭合。<a href="/notes/r0-71t.html">研究笔记</a> <a href="/recap-r0-61-r0-71t.html">当前累计回顾</a> <a href="#r071t-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71U</b><strong>global-shell jet / outgoing occupation packing</strong></header><p>检查 scale-zero jet 或 outgoing occupation 是否有 summed / Carleson estimate；并行保留 amplitude-thresholded excursion。</p></div>`,
);
literatureEdit.replace(
  '<h3 id="r071s-boundary">R0.71S 关闭了什么，R0.71T 只检查什么</h3>',
  '<h3 id="r071t-boundary">R0.71T 关闭了什么，R0.71U 只检查什么</h3>',
);
literatureEdit.replace(
  String.raw`<p>R0.71S 保留 entry direction 与 signed pairing。finite directional-packet theorem 在 sampling coherence、uniform positive parabolic height 与 finite Bessel hypotheses 下成立；但 critical analysis vector 的单包对角已经给 B_crit&gt;=kappa^2，同向聚簇再使 Gram constant 按事件密度增长。frozen-denominator backward heat 与一类 normalized bilinear temporal kernels 不消去该两阶；variable \(Y\) 会带来额外归一化项，不能由这个线性模型处理。mean-zero/signed cancellation 则漏掉常值 directional signal 与 even touch。R0.71O 的 genuine NSE initial face 经 covariant scaling 后保持 weighted atom 不变，而 bare Leray time integral 按 lambda^-2 缩小。因此 observation-boundary 版本的原目标 + bare time integral 终局停止。R0.71T 只检查 internal entries 与 scale-zero dynamical charge。我继续用下面六条筛选。</p>`,
  String.raw`<p>R0.71T 用标准 local strong flow 与 finite-dimensional IFT 构造 genuine positive-time full-shell zero；event forcing 非零，所以 root 是 simple positive internal entry。取 a_lambda=lambda^-2 再作 covariant NSE dilation 后，entry atom 为 lambda^-4、bare normalized Leray-Lamb time budget 为 lambda^-6，比值按 lambda^2 发散；initial energy 与 critical norm 趋零，enstrophy 有界。因此 bare payment 的 internal-entry 版本也停止。outgoing coarea 是 exact scale-zero representation，但 zero-level concentration 尚无 a priori bound。R0.71U 只检查 global-shell jet / outgoing occupation packing 与 amplitude-thresholded excursion。我继续用下面六条筛选。</p>`,
);
literatureEdit.replace(
  String.raw`<div class="boundary"><strong>R0.71S 的一手文献边界</strong><p><a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给临界 parabolic bilinear map，<a href="https://doi.org/10.1016/0022-1236(85)90007-2">Coifman–Meyer–Stein</a>给 tent/Carleson integration，<a href="https://doi.org/10.1016/0022-1236(90)90137-A">Frazier–Jawerth</a>给 distribution pairings、smoothed samples 与 trace threshold，<a href="https://doi.org/10.1007/978-3-642-65161-8_3">Lions–Magenes</a>给 evolution endpoint pairing。它们不把 adaptive zero entry 变成由 bare Leray budget 支付的 uniform lower packet。普通 Leray–Hopf bounds 直接只给 L in L_t^(4/3) H_x^-1，不给 L_t^2 H_x^-1。两轮限定检索未找到完整 R0.71S theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  String.raw`<div class="boundary"><strong>R0.71T 的一手文献边界</strong><p><a href="https://doi.org/10.1007/BF00276188">Fujita–Kato</a>、<a href="https://doi.org/10.1007/BF01174182">Kato</a>与 <a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持 smooth local flow-map input。<a href="https://doi.org/10.1002/cpa.3160350604">CKN</a>、<a href="https://arxiv.org/abs/1101.2193">Dascaliuc–Grujić</a>、<a href="https://math.berkeley.edu/~tataru/papers/nas.pdf">Koch–Tataru</a>分别控制 local energy/singular sets、averaged flux 与 upper Carleson norms，不给每次 smooth zero lower charge。<a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>与 <a href="https://arxiv.org/abs/1503.01746">Łochowski</a>支持 level-averaged occupation 或 positive-height crossings，不给 fixed zero-level raw count。两轮 bounded audit 未找到完整 R0.71T payment theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
);
literatureEdit.replace("文献综述 v1.04 · 2026-08-26", "文献综述 v1.05 · 2026-08-26");
if (literatureEdit.count("<b>R0.71T</b>") !== 1) throw new Error("literature: R0.71T node");
if (literatureEdit.count("开放接口 · R0.71U") !== 1) throw new Error("literature: R0.71U interface");
if (/我们/.test(literatureEdit.value)) throw new Error("literature must use singular or neutral voice");
await writeFile(literaturePath, literatureEdit.value);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71T",
      siteVersion: "v1.05",
      publicNotes: 144,
      currentRouteNotes: 54,
      recapNodes: 84,
      completedReleasesR070AToR071T: 46,
      next: "R0.71U",
    },
    null,
    2,
  ),
);
