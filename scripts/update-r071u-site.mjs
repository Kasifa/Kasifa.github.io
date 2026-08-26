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

          <div class="task-one" id="r071u" data-release="r071u" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71U · 2026-08-26</p>
            <h3>二阶时间 jet 可以求和，raw recurrence 不能计数</h3>
            <p>
              对满足 \(\inf_KY&gt;0\) 的 compact classical trajectory，Hilbert-valued zero sampling 给出 all-shell estimate
              \[
                \mu_J(K)\lesssim \mathcal R_Y(K)\left[
                |K|^{-1}\!\int_K\!Y^{-1}\sum_j\kappa_j^{-6}\|C_{j,t}\|_2^2
                +|K|\!\int_K\!Y^{-1}\sum_j\kappa_j^{-6}\|C_{j,tt}\|_2^2\right].
              \]
              常数不依赖 zero count、minimum separation 或 finite shell truncation。closed-interval endpoints 可用 classical trace 纳入。
            </p>
            <p>
              第一行由 normalized Leray–Lamb ledger 支付。第二行保留 \(\nu^2\|\omega_t\|_2^2+\|L_t\|_{\dot H^{-1}}^2\)，只在 classical level 有限，不由 ordinary Leray energy inequality 控制。exact torus covariance 只对 integer dilation 与协变运输的 frame/window 使用。
            </p>
            <p>
              exact unforced globally smooth 2.5D NSE family 可在任意指定 finite time set 返回同一 compact annulus。每个 finite set 与每个 \(N\) 选择一条新轨迹；unit energy–enstrophy ball 上 raw global-shell entry count 没有统一上界。entry atom 可以随 \(N\) 缩小，所以这不是 weighted-atom counterexample。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节没有删除 second-time-jet recurrence tax，没有得到 weak-solution jet trace、single-trajectory infinite recurrence、continuation、finite-time singularity 或 global regularity。</p>
            <p>
              <a href="/notes/r0-71u.html"><strong>阅读 R0.71U 研究笔记 →</strong></a><br>
              <a href="/notes/r0-71u.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-71u-recurrence-packing.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071u">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071u_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071u-second-jet/fig-r071u-recurrence-packing">查看附图、数据、进度与源代码包</a> ·
              <a href="/recap-r0-61-r0-71u.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71u.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71V：</strong>&nbsp;量化 recurrence family 的 weighted atom mass 与 second-time-jet 两行，并测试 level-integrated / amplitude-thresholded excursion。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
homeEdit.replace("<strong>v1.05</strong>网页版本", "<strong>v1.06</strong>网页版本");
homeEdit.replace("<strong>144</strong>公开研究笔记", "<strong>145</strong>公开研究笔记");
homeEdit.replace("<strong>R0.71T</strong>最新研究节点", "<strong>R0.71U</strong>最新研究节点");
homeEdit.replace(
  "<strong>global-shell jet / outgoing occupation packing</strong>当前方向",
  "<strong>weighted recurrence / Leray-paid excursion</strong>当前方向",
);
homeEdit.replace(
  String.raw`<div class="summary-item"><strong>我目前关注</strong><span>检查 global-shell simple-entry jet 与 outgoing occupation 能否得到 summed / Carleson payment；bare normalized \(\dot H^{-1}\)-Lamb time integral 已被 genuine internal family 排除。</span></div>`,
  String.raw`<div class="summary-item"><strong>我目前关注</strong><span>量化 exact 2.5D recurrence family 的 weighted atom mass 与 classical second-time-jet recurrence tax；并检查 level-integrated excursion 能否由 Leray variation 支付。</span></div>`,
);
homeEdit.replace("Research topology · R0.1–R0.71T", "Research topology · R0.1–R0.71U");
homeEdit.replaceAll("/recap-r0-61-r0-71t.html", "/recap-r0-61-r0-71u.html");
homeEdit.replaceAll("/recap-r0-61-r0-71t.pdf", "/recap-r0-61-r0-71u.pdf");
homeEdit.replace('<span class="route-range">R0.69P–R0.71T</span>', '<span class="route-range">R0.69P–R0.71U</span>');
homeEdit.replace(
  "<h3>从有符号环带障碍走到 genuine internal-entry scale boundary</h3>",
  "<h3>从有符号环带障碍走到 second-time jet 与真实 finite recurrence</h3>",
);
homeEdit.replace(
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–S 给出 conditional Jensen/incidence 与 packet/Bessel scale audits。R0.71T 用正向局部 NSE 流映射和 finite-dimensional IFT 构造 genuine smooth positive-time internal entry；双尺度族把 atom 与 bare normalized Leray-Lamb time budget 分别压到 λ⁻⁴ 与 λ⁻⁶，从而关闭 initial-boundary caveat。outgoing coarea 保留为 scale-matched representation，但 summed payment 仍开放。</p>",
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–T 给出 conditional Jensen/incidence、packet/Bessel scale audits 与 genuine internal-entry no-go。R0.71U 再证明 zero-count-independent classical second-time-jet packing；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D NSE family 同时排除 unit energy–enstrophy ball 上的统一 raw count，但 atom mass 可以塌缩。</p>",
);
homeEdit.replace(
  "→ genuine internal-entry scaling no-go → outgoing occupation boundary</p>",
  "→ genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence</p>",
);
homeEdit.replace("<summary>展开 54 篇公开笔记</summary>", "<summary>展开 55 篇公开笔记</summary>");
homeEdit.replace('aria-label="R0.69P–R0.71T"', 'aria-label="R0.69P–R0.71U"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71t.html">R0.71T</a>\n',
  '                  <a class="milestone" href="/notes/r0-71t.html">R0.71T</a>\n                  <a class="milestone" href="/notes/r0-71u.html">R0.71U</a>\n',
);
homeEdit.replaceBlock(
  '            <article class="tree-node next">',
  "            </article>",
  String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71V</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>weighted recurrence / Leray-paid excursion</h3>
              <p>比较 recurrence family 的 weighted atom sum 与 second-time-jet 两行；检查 level-integrated 或 amplitude-thresholded excursion 能否避免 \(C_{tt}\) tax。</p>
            </article>`,
);
homeEdit.replace(
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71T 路线放在同一张图中。",
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71U 路线放在同一张图中。",
);
homeEdit.replace("累计回顾 R0.61–R0.71T · 2026-08-26", "累计回顾 R0.61–R0.71U · 2026-08-26");
homeEdit.replace(
  "R0.60 recap 之后的累计回顾收录 84 个节点；全站现有 144 篇公开研究笔记",
  "R0.60 recap 之后的累计回顾收录 85 个节点；全站现有 145 篇公开研究笔记",
);
homeEdit.replace(
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel 与 internal-entry scale audit。R0.70A–R0.71T 共 46 个完成版本。",
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet 与 finite recurrence。R0.70A–R0.71U 共 47 个完成版本。",
);
homeEdit.replace(
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71T 已构造 genuine smooth positive-time internal entry，并用 energy/critical norm 趋零、enstrophy 有界的双尺度族排除 bare normalized Leray-Lamb time integral 的 scale-uniform internal payment。outgoing coarea 是 exact scale-matched representation，但零层 concentration、jet summability 与 recurrence packing 仍开放。</p>",
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71U 给出带 positive enstrophy floor 的 trajectory-wise classical second-time-jet theorem；第一行 Leray-paid，第二行非 Leray。exact 2.5D family 排除 unit energy–enstrophy ball 上 raw count 的统一界，但 atom 可缩小，weighted packing 仍开放。</p>",
);
homeEdit.replace(
  String.raw`              对 \(U=(0,\cos x_1,\cos x_2)\) 的 \(|k|^2=2\) 目标壳，标准局部 NSE 流映射与有限维 IFT 给出初值预补偿
              \[
                z(a)=-a^2\tau F_*+O(a^3),
              \]
              使整个目标壳在预定正时间 \(t=\tau\) 精确归零。事件 forcing 仍为 \(a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\)，所以该零点严格位于 observation window 内部、为 simple positive crossing，并满足`,
  String.raw`              对 \(U=(0,\cos x_1,\cos x_2)\) 的 \(|k|^2=2\) exact four-mode real-conjugate projection，标准局部 NSE 流映射与有限维 IFT 给出初值预补偿
              \[
                z(a)=-a^2\tau F_*+O(a^3).
              \]
              该精确 thin projection 在预定正时间 \(t=\tau\) 归零。若 compact target support 与 seed shell 分离，变量空间必须扩到全部 target-support modes，有限热半群矩阵才给 full-support cancellation。事件 forcing 仍为 \(a^2e^{-2\nu\tau}F_*+O(a^3)\ne0\)，所以该零点严格位于 observation window 内部、为 simple positive crossing，并满足`,
);
homeEdit.replace(
  String.raw`<p><strong style="color:var(--gold)">下一步 R0.71U：</strong>&nbsp;检查 global-shell simple-entry jet 与 outgoing occupation 是否有 summed / Carleson payment；并行保留 amplitude-thresholded excursion 分支。</p>
          </div>
        </section>`,
  String.raw`<p><strong style="color:var(--gold)">R0.71U 已完成：</strong>&nbsp;classical second-time-jet theorem 保留 recurrence tax；exact 2.5D finite recurrence 排除统一 raw count，但不排除 weighted packing。</p>
          </div>` + releaseCard + String.raw`
        </section>`,
);
homeEdit.replace("综述 v1.05 · 2026-08-26", "综述 v1.06 · 2026-08-26");
homeEdit.replace("上次综述 v1.04 · 2026-08-26", "上次综述 v1.05 · 2026-08-26");
homeEdit.replaceAll("/i18n-en.js?v=1.05", "/i18n-en.js?v=1.06");

if (homeEdit.count('data-release="r071u"') !== 1) throw new Error("home: R0.71U card count");
if (homeEdit.count('href="/notes/r0-71u.html"') !== 2) throw new Error("home: R0.71U note links");
if (homeEdit.count("<summary>展开 55 篇公开笔记</summary>") !== 1) throw new Error("home: route count");
if (/我们/.test(homeEdit.value)) throw new Error("home must use singular or neutral voice");
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const literatureEdit = editor(await readFile(literaturePath, "utf8"), "literature");
literatureEdit.replaceAll("/i18n-en.js?v=1.05", "/i18n-en.js?v=1.06");
literatureEdit.replaceAll("/recap-r0-61-r0-71t.html", "/recap-r0-61-r0-71u.html");
literatureEdit.replace(
  "本站 R0.69P–R0.71T 只列为研究笔记",
  "本站 R0.69P–R0.71U 只列为研究笔记",
);
literatureEdit.replace(
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71u.html">累计回顾与 84 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–S 给出 finite conditional Jensen/incidence 与 packet/Bessel scale audits。R0.71T 再构造 genuine smooth positive-time internal entry，并排除 bare normalized Leray-Lamb time integral 的 scale-uniform internal payment。保留下来的结果都不是全局正则性结论。</p>',
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71u.html">累计回顾与 85 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–T 给出 conditional Jensen/incidence、packet/Bessel 与 genuine internal-entry scale audits。R0.71U 再给出 classical second-time-jet packing，并用 exact unforced 2.5D NSE family 排除 unit energy–enstrophy ball 上的统一 raw count。保留下来的结果都不是全局正则性结论。</p>',
);
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71u.html#node-index">打开 84 节完整索引</a>',
  '<a href="/recap-r0-61-r0-71u.html#node-index">打开 85 节完整索引</a>',
);
literatureEdit.replace(
  String.raw`              <div class="route-step closed"><header><b>R0.71T</b><strong>genuine internal entry 保留同一两阶错配</strong></header><p>finite-dimensional IFT 构造 smooth positive-time full-shell root；double scaling 给 atom λ⁻⁴、bare budget λ⁻⁶。outgoing coarea 精确保留 entry，但 summed payment 未闭合。<a href="/notes/r0-71t.html">研究笔记</a> <a href="/recap-r0-61-r0-71u.html">当前累计回顾</a> <a href="#r071t-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71U</b><strong>global-shell jet / outgoing occupation packing</strong></header><p>检查 scale-zero jet 或 outgoing occupation 是否有 summed / Carleson estimate；并行保留 amplitude-thresholded excursion。</p></div>`,
  String.raw`              <div class="route-step closed"><header><b>R0.71T</b><strong>genuine internal entry 保留同一两阶错配</strong></header><p>finite-dimensional IFT 的精确对象是 four-mode thin projection；与 seed 分离的 compact full support 需要把变量扩到全部 target modes。double scaling 给 atom λ⁻⁴、bare budget λ⁻⁶。<a href="/notes/r0-71t.html">研究笔记</a></p></div>
              <div class="route-step kept"><header><b>R0.71U</b><strong>classical second-time jet 可求和，raw count 无统一界</strong></header><p>Hilbert sampling 给 zero-count-independent all-shell theorem；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D family 在每个 finite set 上选择新轨迹，排除 unit energy–enstrophy ball 上的统一 raw count；atoms 可缩小。<a href="/notes/r0-71u.html">研究笔记</a> <a href="/recap-r0-61-r0-71u.html">当前累计回顾</a> <a href="#r071u-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71V</b><strong>weighted recurrence / Leray-paid excursion</strong></header><p>比较 atom mass 与 second-time-jet 两行，并测试 level-integrated 或 amplitude-thresholded excursion。</p></div>`,
);
literatureEdit.replace(
  '<h3 id="r071t-boundary">R0.71T 关闭了什么，R0.71U 只检查什么</h3>',
  '<h3 id="r071u-boundary">R0.71U 关闭了什么，R0.71V 只检查什么</h3>',
);
literatureEdit.replace(
  String.raw`<p>R0.71T 用标准 local strong flow 与 finite-dimensional IFT 构造 genuine positive-time full-shell zero；event forcing 非零，所以 root 是 simple positive internal entry。取 a_lambda=lambda^-2 再作 covariant NSE dilation 后，entry atom 为 lambda^-4、bare normalized Leray-Lamb time budget 为 lambda^-6，比值按 lambda^2 发散；initial energy 与 critical norm 趋零，enstrophy 有界。因此 bare payment 的 internal-entry 版本也停止。outgoing coarea 是 exact scale-zero representation，但 zero-level concentration 尚无 a priori bound。R0.71U 只检查 global-shell jet / outgoing occupation packing 与 amplitude-thresholded excursion。我继续用下面六条筛选。</p>`,
  String.raw`<p>R0.71U 对带 \(\inf_KY&gt;0\) 的 compact classical trajectory 证明 all-shell second-time-jet estimate；closed-interval endpoints 由 classical trace 纳入。第一行有 normalized Leray–Lamb payment，第二行保留 \(\omega_t\) 与 \(L_t\)，所以不是 Leray closure。exact torus scaling 只按 integer dilation 和协变运输的 frame/window 陈述。另一个 exact unforced 2.5D family 对每个 finite time set 选择新轨迹，排除 unit energy–enstrophy ball 上 raw count 的统一界；atom 可缩小，故 weighted packing 仍开放。R0.71V 只比较 weighted recurrence、second-time-jet tax 与 Leray-paid excursion。我继续用下面六条筛选。</p>`,
);
literatureEdit.replace(
  String.raw`<div class="boundary"><strong>R0.71T 的一手文献边界</strong><p><a href="https://doi.org/10.1007/BF00276188">Fujita–Kato</a>、<a href="https://doi.org/10.1007/BF01174182">Kato</a>与 <a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持 smooth local flow-map input。<a href="https://doi.org/10.1002/cpa.3160350604">CKN</a>、<a href="https://arxiv.org/abs/1101.2193">Dascaliuc–Grujić</a>、<a href="https://math.berkeley.edu/~tataru/papers/nas.pdf">Koch–Tataru</a>分别控制 local energy/singular sets、averaged flux 与 upper Carleson norms，不给每次 smooth zero lower charge。<a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>与 <a href="https://arxiv.org/abs/1503.01746">Łochowski</a>支持 level-averaged occupation 或 positive-height crossings，不给 fixed zero-level raw count。两轮 bounded audit 未找到完整 R0.71T payment theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
  String.raw`<div class="boundary"><strong>R0.71U 的一手文献边界</strong><p><a href="https://doi.org/10.3792/pja/1195521421">Masuda</a>与 <a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持 classical time-analyticity 与 strong-solution background。<a href="https://doi.org/10.1140/epje/i2018-11612-1">Linkmann–Buzzicotti–Biferale</a>记录 exact 2D3C reduction；<a href="https://books.google.com/books?id=P7Y-AAAAIAAJ">Karlin–Studden</a>给 Chebyshev-system interpolation 背景。<a href="https://doi.org/10.1007/s00021-004-0110-1">Agrachev–Sarychev</a>与 <a href="https://doi.org/10.1016/J.ANIHPC.2006.04.002">Shirikyan</a>研究带外力的 projection controllability；本节只选择初值、演化无外力，并允许解随 finite time set 改变，量词不同。<a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给 upper critical Carleson control。<a href="https://doi.org/10.4064/fm-7-1-225-236">Banach</a>、<a href="https://doi.org/10.4064/cm6583-3-2017">Łochowski</a>与 <a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>处理 level-integrated crossings、variation 或 local time，不直接给 fixed zero-level normalized derivative mass。bounded audit 未定位到完整 R0.71U theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
);
literatureEdit.replace("文献综述 v1.05 · 2026-08-26", "文献综述 v1.06 · 2026-08-26");
if (literatureEdit.count("<b>R0.71U</b>") !== 1) throw new Error("literature: R0.71U node");
if (literatureEdit.count("开放接口 · R0.71V") !== 1) throw new Error("literature: R0.71V interface");
if (/我们/.test(literatureEdit.value)) throw new Error("literature must use singular or neutral voice");
await writeFile(literaturePath, literatureEdit.value);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71U",
      siteVersion: "v1.06",
      publicNotes: 145,
      currentRouteNotes: 55,
      recapNodes: 85,
      completedReleasesR070AToR071U: 47,
      next: "R0.71V",
    },
    null,
    2,
  ),
);
