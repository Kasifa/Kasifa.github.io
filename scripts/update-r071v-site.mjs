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

          <div class="task-one" id="r071v" data-release="r071v" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71V · 2026-08-26</p>
            <h3>excursion height 可由 Leray 支付，固定零层斜率仍需额外信息</h3>
            <p>
              compact Fourier shells 在 Leray–Hopf 层级有绝对连续代表。对每个正 excursion \(E\)，
              \[
                H_E^2=\frac{\kappa_j^{-6}h_E^2}{\ell Y_E},
                \qquad
                \sum_{j,E}H_E^2\le\frac{B_1(K)}{\ell}.
              \]
              因此 amplitude-thresholded excursion count 有尺度零上界，并可由 finite family 经 Tonelli 与 monotone convergence 扩展。
            </p>
            <p>
              classical root atom 与 excursion 的精确转换因子是
              \[
                D_E=\frac{h_E^2Y(t_E)}{\ell Y_Es_E^2}.
              \]
              统一 \(D_E\ge d_0&gt;0\) 会关闭 first-row payment；weighted area formula 与 sine test 说明，这种 fixed-zero noncollapse 不能从 level-integrated \(L^1\) 控制自动推出。
            </p>
            <p>
              固定 target \(K_y=K_z=1\) 与固定 macroscopic window 的 exact unforced 2.5D NSE 序列，对 second prescribed root 与 selected singleton target-shell rows 满足
              \[
                J_{2,q}/((2/\ell)B_{1,q}^{(*)})\asymp q^2,\qquad
                J_{2,q}/((7\ell/3)B_{2,q}^{(*)})\asymp q^{-2}.
              \]
              selected second-time row 能支付该事件，同一 selected first-time row 单独不能；singleton selection 已经失败。这不是 complete fixed-frame ledger 的 no-go。该族不证明 \(7\ell/3\) sharp，也不排除完整 global \(\nu^2\) baseline 或另一 dynamical charge。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节没有得到 weak zero-jet、继续性、finite-time singularity 或 global regularity；closed-response figure 只作可复现 corroboration。</p>
            <p>
              <a href="/notes/r0-71v.html"><strong>阅读 R0.71V 研究笔记 →</strong></a><br>
              <a href="/notes/r0-71v.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-71v-zero-level-boundary.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071v">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071v_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071v_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071v_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071v_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071v-level-boundary/fig-r071v-zero-level-boundary">查看附图、数据、进度与源代码包</a> ·
              <a href="/recap-r0-61-r0-71v.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71v.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71W：</strong>&nbsp;检查完整 \(\nu^2\) baseline 与 projected rotational term，判断 fixed-target high-frequency events 相对完整 Leray ledger 是否仍非坍缩。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
homeEdit.replace("<strong>v1.06</strong>网页版本", "<strong>v1.07</strong>网页版本");
homeEdit.replace("<strong>145</strong>公开研究笔记", "<strong>146</strong>公开研究笔记");
homeEdit.replace("<strong>R0.71U</strong>最新研究节点", "<strong>R0.71V</strong>最新研究节点");
homeEdit.replace(
  "<strong>weighted recurrence / Leray-paid excursion</strong>当前方向",
  "<strong>complete Leray ledger / zero-level boundary</strong>当前方向",
);
homeEdit.replace(
  '<div class="summary-item"><strong>我目前关注</strong><span>量化 exact 2.5D recurrence family 的 weighted atom mass 与 classical second-time-jet recurrence tax；并检查 level-integrated excursion 能否由 Leray variation 支付。</span></div>',
  '<div class="summary-item"><strong>我目前关注</strong><span>检查 fixed-target high-frequency events 相对完整 \\(\\nu^2\\) baseline 与 projected rotational term 是否仍非坍缩；fixed zero-level trace 不能直接从 level-integrated occupation 读取。</span></div>',
);
homeEdit.replace("Research topology · R0.1–R0.71U", "Research topology · R0.1–R0.71V");
homeEdit.replaceAll("/recap-r0-61-r0-71u.html", "/recap-r0-61-r0-71v.html");
homeEdit.replaceAll("/recap-r0-61-r0-71u.pdf", "/recap-r0-61-r0-71v.pdf");
homeEdit.replace('<span class="route-range">R0.69P–R0.71U</span>', '<span class="route-range">R0.69P–R0.71V</span>');
homeEdit.replace(
  "<h3>从有符号环带障碍走到 second-time jet 与真实 finite recurrence</h3>",
  "<h3>从有符号环带障碍走到 Leray-paid excursion 与固定零层边界</h3>",
);
homeEdit.replace(
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q–T 给出 conditional Jensen/incidence、packet/Bessel scale audits 与 genuine internal-entry no-go。R0.71U 再证明 zero-count-independent classical second-time-jet packing；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D NSE family 同时排除 unit energy–enstrophy ball 上的统一 raw count，但 atom mass 可以塌缩。</p>",
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–T 建立 projected-Lamb 热体积、局部化、temporal packing 与 genuine internal-entry no-go。R0.71U 给出 classical second-time-jet theorem 与 exact finite recurrence。R0.71V 证明 compact-shell excursion-height packing 可由 Leray–Hopf 第一行支付；weighted area formula、sine test 与 fixed-target 2.5D NSE 序列同时表明 distinguished zero-level slope 仍需 noncollapse 或另一 dynamical charge。</p>",
);
homeEdit.replace(
  "→ classical second-time-jet packing → exact finite recurrence</p>",
  "→ classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero first-row obstruction</p>",
);
homeEdit.replace("<summary>展开 55 篇公开笔记</summary>", "<summary>展开 56 篇公开笔记</summary>");
homeEdit.replace('aria-label="R0.69P–R0.71U"', 'aria-label="R0.69P–R0.71V"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71u.html">R0.71U</a>\n',
  '                  <a class="milestone" href="/notes/r0-71u.html">R0.71U</a>\n                  <a class="milestone" href="/notes/r0-71v.html">R0.71V</a>\n',
);
homeEdit.replaceBlock(
  '            <article class="tree-node next">',
  "            </article>",
  String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71W</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>complete Leray ledger / rotational term</h3>
              <p>移除或平衡 decoupled background，比较 fixed-target high-frequency atom 与完整 \(\nu^2\) baseline、projected rotational term。</p>
            </article>`,
);
homeEdit.replace(
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71U 路线放在同一张图中。",
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71V 路线放在同一张图中。",
);
homeEdit.replace("累计回顾 R0.61–R0.71U · 2026-08-26", "累计回顾 R0.61–R0.71V · 2026-08-26");
homeEdit.replace(
  "R0.60 recap 之后的累计回顾收录 85 个节点；全站现有 145 篇公开研究笔记",
  "R0.60 recap 之后的累计回顾收录 86 个节点；全站现有 146 篇公开研究笔记",
);
homeEdit.replace(
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet 与 finite recurrence。R0.70A–R0.71U 共 47 个完成版本。",
  "R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet、finite recurrence、Leray-paid excursion 与 fixed-zero boundary。R0.70A–R0.71V 共 48 个完成版本。",
);
homeEdit.replace(
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71U 给出带 positive enstrophy floor 的 trajectory-wise classical second-time-jet theorem；第一行 Leray-paid，第二行非 Leray。exact 2.5D family 排除 unit energy–enstrophy ball 上 raw count 的统一界，但 atom 可缩小，weighted packing 仍开放。</p>",
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71V 在 Leray–Hopf 层级支付 scale-zero excursion height；fixed target/window 的 genuine 2.5D sequence 排除只保留 first-time row 的指定零点采样。second-time row 仍可支付，完整 global \\(\\nu^2\\) baseline 与替代账本尚未排除。</p>",
);
homeEdit.replace(
  String.raw`<p><strong style="color:var(--gold)">下一步 R0.71V：</strong>&nbsp;量化 recurrence family 的 weighted atom mass 与 second-time-jet 两行，并测试 level-integrated / amplitude-thresholded excursion。</p>
          </div>
        </section>`,
  String.raw`<p><strong style="color:var(--gold)">R0.71V 已完成：</strong>&nbsp;Leray–Hopf excursion-height packing 成立；fixed zero-level atom 不能只由同一 first-time row 统一支付。</p>
          </div>` + releaseCard + String.raw`
        </section>`,
);
homeEdit.replace("综述 v1.06 · 2026-08-26", "综述 v1.07 · 2026-08-26");
homeEdit.replace("上次综述 v1.05 · 2026-08-26", "上次综述 v1.06 · 2026-08-26");
homeEdit.replaceAll("/i18n-en.js?v=1.06", "/i18n-en.js?v=1.07");

if (homeEdit.count('data-release="r071v"') !== 1) throw new Error("home: R0.71V card count");
if (homeEdit.count('href="/notes/r0-71v.html"') !== 2) throw new Error("home: R0.71V note links");
if (homeEdit.count("<summary>展开 56 篇公开笔记</summary>") !== 1) throw new Error("home: route count");
if (/我们|攻关|主攻|三重审计/.test(homeEdit.value)) throw new Error("home must use singular or neutral voice");
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const literatureEdit = editor(await readFile(literaturePath, "utf8"), "literature");
literatureEdit.replaceAll("/i18n-en.js?v=1.06", "/i18n-en.js?v=1.07");
literatureEdit.replaceAll("/recap-r0-61-r0-71u.html", "/recap-r0-61-r0-71v.html");
literatureEdit.replace(
  "本站 R0.69P–R0.71U 只列为研究笔记",
  "本站 R0.69P–R0.71V 只列为研究笔记",
);
literatureEdit.replace(
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71v.html">累计回顾与 85 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–T 给出 conditional Jensen/incidence、packet/Bessel 与 genuine internal-entry scale audits。R0.71U 再给出 classical second-time-jet packing，并用 exact unforced 2.5D NSE family 排除 unit energy–enstrophy ball 上的统一 raw count。保留下来的结果都不是全局正则性结论。</p>',
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71v.html">累计回顾与 86 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V 再证明 Leray-paid excursion-height packing，并用 weighted area hierarchy、sine test 和 genuine 2.5D sequence 分离 level integral 与 fixed zero-level trace。保留下来的结果都不是全局正则性结论。</p>',
);
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71v.html#node-index">打开 85 节完整索引</a>',
  '<a href="/recap-r0-61-r0-71v.html#node-index">打开 86 节完整索引</a>',
);
literatureEdit.replace(
  String.raw`              <div class="route-step kept"><header><b>R0.71U</b><strong>classical second-time jet 可求和，raw count 无统一界</strong></header><p>Hilbert sampling 给 zero-count-independent all-shell theorem；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D family 在每个 finite set 上选择新轨迹，排除 unit energy–enstrophy ball 上的统一 raw count；atoms 可缩小。<a href="/notes/r0-71u.html">研究笔记</a> <a href="/recap-r0-61-r0-71v.html">当前累计回顾</a> <a href="#r071u-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71V</b><strong>weighted recurrence / Leray-paid excursion</strong></header><p>比较 atom mass 与 second-time-jet 两行，并测试 level-integrated 或 amplitude-thresholded excursion。</p></div>`,
  String.raw`              <div class="route-step kept"><header><b>R0.71U</b><strong>classical second-time jet 可求和，raw count 无统一界</strong></header><p>Hilbert sampling 给 zero-count-independent all-shell theorem；第一行 Leray-paid，第二行保留 recurrence tax。exact unforced 2.5D family 排除 unit energy–enstrophy ball 上的统一 raw count；atoms 可缩小。<a href="/notes/r0-71u.html">研究笔记</a></p></div>
              <div class="route-step kept"><header><b>R0.71V</b><strong>excursion height Leray-paid，fixed zero-level trace 仍开放</strong></header><p>compact-shell AC representatives 与 weighted Cauchy–Schwarz 给 scale-zero excursion packing。area formula、sine test 与 fixed-target genuine 2.5D sequence 排除 first-row-only fixed-zero sampling；完整 \(\nu^2\) baseline 尚未排除。<a href="/notes/r0-71v.html">研究笔记</a> <a href="/recap-r0-61-r0-71v.html">当前累计回顾</a> <a href="#r071v-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71W</b><strong>complete Leray ledger / rotational term</strong></header><p>平衡 decoupled background，并比较 atom 与完整 \(\nu^2\) baseline、projected rotational charge。</p></div>`,
);
literatureEdit.replace(
  '<h3 id="r071u-boundary">R0.71U 关闭了什么，R0.71V 只检查什么</h3>',
  '<h3 id="r071v-boundary">R0.71V 关闭了什么，R0.71W 只检查什么</h3>',
);
literatureEdit.replace(
  String.raw`<p>R0.71U 对带 \(\inf_KY&gt;0\) 的 compact classical trajectory 证明 all-shell second-time-jet estimate；closed-interval endpoints 由 classical trace 纳入。第一行有 normalized Leray–Lamb payment，第二行保留 \(\omega_t\) 与 \(L_t\)，所以不是 Leray closure。exact torus scaling 只按 integer dilation 和协变运输的 frame/window 陈述。另一个 exact unforced 2.5D family 对每个 finite time set 选择新轨迹，排除 unit energy–enstrophy ball 上 raw count 的统一界；atom 可缩小，故 weighted packing 仍开放。R0.71V 只比较 weighted recurrence、second-time-jet tax 与 Leray-paid excursion。我继续用下面六条筛选。</p>`,
  String.raw`<p>R0.71V 在 Leray–Hopf 层级证明 compact-shell excursion-height packing，并写出 classical root atom 与 excursion 的精确无量纲转换因子 \(D_E\)。weighted area formula 只把 linear-slope level density 压到 first-time row；quadratic slope 需要 cubic time occupation，普通 \(L^1\) level control 不决定 distinguished zero-level trace。sine path 给抽象 method test，固定 target/window 的 genuine unforced 2.5D NSE 序列进一步排除只保留同一 first-time row 的指定零点采样。该序列不证明 second-time coefficient sharp，也不排除完整 global \(\nu^2\) baseline 或另一 dynamical charge。R0.71W 只检查完整 Leray ledger。我继续用下面六条筛选。</p>`,
);
literatureEdit.replace(
  String.raw`<div class="boundary"><strong>R0.71U 的一手文献边界</strong><p><a href="https://doi.org/10.3792/pja/1195521421">Masuda</a>与 <a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持 classical time-analyticity 与 strong-solution background。<a href="https://doi.org/10.1140/epje/i2018-11612-1">Linkmann–Buzzicotti–Biferale</a>记录 exact 2D3C reduction；<a href="https://books.google.com/books?id=P7Y-AAAAIAAJ">Karlin–Studden</a>给 Chebyshev-system interpolation 背景。<a href="https://doi.org/10.1007/s00021-004-0110-1">Agrachev–Sarychev</a>与 <a href="https://doi.org/10.1016/J.ANIHPC.2006.04.002">Shirikyan</a>研究带外力的 projection controllability；本节只选择初值、演化无外力，并允许解随 finite time set 改变，量词不同。<a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给 upper critical Carleson control。<a href="https://doi.org/10.4064/fm-7-1-225-236">Banach</a>、<a href="https://doi.org/10.4064/cm6583-3-2017">Łochowski</a>与 <a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>处理 level-integrated crossings、variation 或 local time，不直接给 fixed zero-level normalized derivative mass。bounded audit 未定位到完整 R0.71U theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
  String.raw`<div class="boundary"><strong>R0.71V 的一手文献边界</strong><p><a href="https://doi.org/10.1007/978-3-642-62010-2">Federer</a>给 weighted area formula；<a href="https://doi.org/10.4064/fm-7-1-225-236">Banach</a>给 level indicatrix 与 total variation；<a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>与 <a href="https://doi.org/10.4064/cm6583-3-2017">Łochowski</a>处理 occupation、crossings 与 truncated variation。<a href="https://doi.org/10.1063/1.4990082">Biferale–Buzzicotti–Linkmann</a>记录 exact 2D3C reduction；<a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持 weak energy spaces 与二维 strong-solution background。checked sources 给 level-integrated 或 almost-every-level 结论，不给 fixed zero-level quadratic trace。bounded audit 未定位到完整 R0.71V theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
);
literatureEdit.replace("文献综述 v1.06 · 2026-08-26", "文献综述 v1.07 · 2026-08-26");
if (literatureEdit.count("<b>R0.71V</b>") !== 1) throw new Error("literature: R0.71V node");
if (literatureEdit.count("开放接口 · R0.71W") !== 1) throw new Error("literature: R0.71W interface");
if (/我们|攻关|主攻|三重审计/.test(literatureEdit.value)) throw new Error("literature must use singular or neutral voice");
await writeFile(literaturePath, literatureEdit.value);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71V",
      siteVersion: "v1.07",
      publicNotes: 146,
      currentRouteNotes: 56,
      recapNodes: 86,
      completedReleasesR070AToR071V: 48,
      next: "R0.71W",
    },
    null,
    2,
  ),
);
