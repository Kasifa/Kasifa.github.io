import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) {
        throw new Error(label + ": expected one match, found " + count + ": " + before.slice(0, 140));
      }
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) {
        throw new Error(label + ": expected at least " + minimum + " matches, found " + count + ": " + before);
      }
      value = value.split(before).join(after);
    },
    replaceBlock(start, end, after) {
      const count = value.split(start).length - 1;
      if (count !== 1) {
        throw new Error(label + ": expected one block start, found " + count + ": " + start);
      }
      const startIndex = value.indexOf(start);
      const endIndex = value.indexOf(end, startIndex + start.length);
      if (endIndex < 0) throw new Error(label + ": block end not found: " + end);
      value = value.slice(0, startIndex) + after + value.slice(endIndex + end.length);
    },
    count(fragment) {
      return value.split(fragment).length - 1;
    },
    get value() {
      return value;
    },
  };
}

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
const homeIsCurrent = homeEdit.count('data-release="r071p"') === 1;

const releaseCard = String.raw`

          <div class="task-one" id="r071p" data-release="r071p" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71P · 2026-08-26</p>
            <h3>同刻正进入可以做空间平方和，跨时累积仍需要 entry-time packing</h3>
            <p>
              \(A_{j,Q,+}\) 是逐 shell–cell 的 soft/zero-padded 正进入原子，不是 ordinary hard BV 的正跳跃，也不一般等于 signed aggregate 的正 Jordan 部：
              \[
                A_+-(A_+-A_-)^+=\min(A_+,A_-).
              \]
              偶阶 touch 可以让 hard positive jump 为零，同时保留完整 \(A_+\)。
            </p>
            <p>
              对同一时刻的全部 entries，leading direction 支撑在 cutoff cell 中。bounded overlap 与 annular \(\dot H^{-1}\) square sum 给出
              \[
                \mathsf e_\Lambda(t)
                \le M_\chi C_T\frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}
                \lesssim M_\chi C_T\|u(t)\|_2Y(t)^{1/2}.
              \]
              因而空间 cell multiplicity 被删除。
            </p>
            <p>
              完整目标精确变成
              \[
                \mathsf S_{\Lambda,+}(K)
                \le\int_K M_\chi C_T
                \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}
                \,d\mathfrak n_\Lambda(t).
              \]
              其中 \(\mathfrak n_\Lambda\) 只计不同 entry times。逐分量 relaxed 正原子已经非负，不能在该目标内部再做 shell–cell signed cancellation。半开窗口上的抽象 sequential path 使计数质量按 \(N\) 增长；真实 smooth NSE initial jet 则达到 cellwise 常数 \(A_+=\|F\|_2^2/Y=1/4\)。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节关闭同刻空间 multiplicity，没有给出 uniform NSE temporal packing、内部多 face、无限 frame、Leray 极限、继续性或全局正则性结论。</p>
            <p>
              <a href="/notes/r0-71p.html"><strong>阅读 R0.71P 研究笔记 →</strong></a> ·
              <a href="/notes/r0-71p.pdf">下载同步 PDF</a><br>
              <a href="/figures/r0-71p-positive-entry-batching.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071p">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071p_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071p_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071p_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071p_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071p-positive-entry-batching/fig-r071p-positive-entry-batching">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71p.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71p.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71Q：</strong>&nbsp;把 quantitative complex-time Jensen bound 放进 parabolic windows，显式检查 analytic radius、complex growth、projection anchor 与窗口覆盖是否能从 NSE 预算支付。</p>
          </div>`;

if (!homeIsCurrent) {
  homeEdit.replace('<strong>v1.00</strong>网页版本', '<strong>v1.01</strong>网页版本');
  homeEdit.replace('<strong>139</strong>公开研究笔记', '<strong>140</strong>公开研究笔记');
  homeEdit.replace('<strong>R0.71O</strong>最新研究节点', '<strong>R0.71P</strong>最新研究节点');
  homeEdit.replace(
    '<strong>fixed-partition weighted positive-entry sum</strong>当前方向',
    '<strong>quantitative complex-time zero packing</strong>当前方向',
  );
  homeEdit.replace(
    String.raw`<div class="summary-item"><strong>我目前关注</strong><span>固定 partition 上，检查全壳、全小区的正向进入和 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否有新的 cancellation 或必须保留额外条件。</span></div>`,
    String.raw`<div class="summary-item"><strong>我目前关注</strong><span>把 complex-time Jensen zero count 放进 parabolic windows，逐项核对 analytic radius、growth、projection anchor 与窗口 covering 是否能从 NSE 预算支付。</span></div>`,
  );
  homeEdit.replace('Research topology · R0.1–R0.71O', 'Research topology · R0.1–R0.71P');
  homeEdit.replaceAll('/recap-r0-61-r0-71o.html', '/recap-r0-61-r0-71p.html');
  homeEdit.replaceAll('/recap-r0-61-r0-71o.pdf', '/recap-r0-61-r0-71p.pdf');
  homeEdit.replace('<span class="route-range">R0.69P–R0.71O</span>', '<span class="route-range">R0.69P–R0.71P</span>');
  homeEdit.replace(
    '<h3>从有符号环带障碍走到 soft-denominator face boundary</h3>',
    '<h3>从有符号环带障碍走到 positive-entry temporal-packing boundary</h3>',
  );
  homeEdit.replace(
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft denominator 精确恢复 hard 一侧 traces：signed atoms 可以抵消，Jordan face costs 仍保留；ordinary budgets 不统一支付抽象 face count。</p>',
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–O 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge、signed second jet 与 soft denominator faces。R0.71P 再证明同刻正进入可由空间平方和支付，而完整累积仍需要 distinct entry-time packing。</p>',
  );
  homeEdit.replace(
    '→ signed second-jet boundary → soft-denominator face boundary</p>',
    '→ signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary</p>',
  );
  homeEdit.replace('<summary>展开 49 篇公开笔记</summary>', '<summary>展开 50 篇公开笔记</summary>');
  homeEdit.replace('aria-label="R0.69P–R0.71O"', 'aria-label="R0.69P–R0.71P"');
  homeEdit.replace(
    '                  <a class="milestone" href="/notes/r0-71o.html">R0.71O</a>\n',
    '                  <a class="milestone" href="/notes/r0-71o.html">R0.71O</a>\n                  <a class="milestone" href="/notes/r0-71p.html">R0.71P</a>\n',
  );
  homeEdit.replaceBlock(
    '            <article class="tree-node next">',
    '            </article>',
    String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71Q</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>Quantitative complex-time / parabolic-window zero packing</h3>
              <p>我把 Jensen zero-count 条件放进 parabolic windows，显式记录 analytic radius \(R\)、complex growth \(M\)、projection anchor \(\|C(t_*)\|\) 与窗口 covering；不把定性解析性写成 uniform count。</p>
            </article>`,
  );
  homeEdit.replace('累计回顾 R0.61–R0.71O · 2026-08-26', '累计回顾 R0.61–R0.71P · 2026-08-26');
  homeEdit.replace(
    'R0.60 recap 之后的累计回顾收录 79 个节点；全站现有 139 篇公开研究笔记',
    'R0.60 recap 之后的累计回顾收录 80 个节点；全站现有 140 篇公开研究笔记',
  );
  homeEdit.replace(
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、signed second jet 与 soft-denominator faces。R0.70A–R0.71O 共 41 个完成版本。',
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、soft-denominator faces 与 positive-entry temporal packing。R0.70A–R0.71P 共 42 个完成版本。',
  );
  homeEdit.replace(
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71O 证明 soft denominator 只平滑坐标，不删除一侧 face cost；signed atoms 可以抵消，Jordan masses 仍保留。固定 partition 上的 all-shell/all-cell weighted positive-entry sum 尚未闭合。</p>',
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71P 删除了同刻空间 cell multiplicity，并证明正进入 atoms 本身不能直接做 signed shell–cell cancellation；未闭合的是 distinct entry-time counting measure 的 uniform NSE packing。</p>',
  );
  homeEdit.replace(
    String.raw`<p><strong style="color:var(--gold)">下一步 R0.71P：</strong>&nbsp;固定 partition 上，检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否存在 NSE-specific cancellation 或新的必要输入。total-Jordan sum 是更强的后续变体。</p>`,
    String.raw`<p><strong style="color:var(--gold)">R0.71P 已完成：</strong>&nbsp;同刻正进入由 bounded-overlap 与 \(\dot H^{-1}\) Lamb square sum 支付；完整时间累积被精确归约到 distinct entry-time counting measure。</p>`,
  );
  homeEdit.replace(
    '          </div>\n        </section>\n\n      </article>',
    '          </div>' + releaseCard + '\n        </section>\n\n      </article>',
  );
  homeEdit.replace('综述 v1.00 · 2026-08-26', '综述 v1.01 · 2026-08-26');
  homeEdit.replace('上次综述 v0.99 · 2026-08-26', '上次综述 v1.00 · 2026-08-26');
  homeEdit.replaceAll('/i18n-en.js?v=1.00', '/i18n-en.js?v=1.01');
  homeEdit.replace(
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71O 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71P 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
  );
}

if (homeEdit.count('data-release="r071p"') !== 1) throw new Error("home: R0.71P release-card count is not one");
if (homeEdit.count('href="/notes/r0-71p.html"') !== 2) throw new Error("home: expected exactly two R0.71P note links");
if (homeEdit.count('<summary>展开 50 篇公开笔记</summary>') !== 1) throw new Error("home: route-note count is not 50");
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const litEdit = editor(await readFile(literaturePath, "utf8"), "literature");
const literatureIsCurrent = litEdit.count('<b>R0.71P</b>') === 1;

if (!literatureIsCurrent) {
  litEdit.replaceAll('/i18n-en.js?v=1.00', '/i18n-en.js?v=1.01');
  litEdit.replace('本站 R0.69P–R0.71O 只列为研究笔记', '本站 R0.69P–R0.71P 只列为研究笔记');
  litEdit.replaceAll('/recap-r0-61-r0-71o.html', '/recap-r0-61-r0-71p.html');
  litEdit.replace(
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71p.html">累计回顾与 79 节索引</a>中。R0.69P–R0.71O 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet，走到 soft-denominator face boundary。R0.71O 证明 soft quotient 恢复 hard 一侧迹，signed atoms 可以相消而 Jordan face costs 保留。保留下来的结果都不是全局正则性结论。</p>',
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71p.html">累计回顾与 80 节索引</a>中。R0.69P–R0.71P 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion、signed second jet 与 soft-denominator faces，走到 positive-entry temporal-packing boundary。R0.71P 删除同刻空间 cell multiplicity，留下 distinct entry-time packing。保留下来的结果都不是全局正则性结论。</p>',
  );
  litEdit.replace(
    '<a href="/recap-r0-61-r0-71p.html#node-index">打开 79 节完整索引</a>',
    '<a href="/recap-r0-61-r0-71p.html#node-index">打开 80 节完整索引</a>',
  );
  litEdit.replace(
    String.raw`              <div class="route-step closed"><header><b>R0.71O</b><strong>soft quotient 恢复一侧 traces 与 Jordan face atoms</strong></header><p>精确 factorization 把 soft source 分成 hard interior source 与 face layer。有限阶零点的 signed atom 可以消失，正负 Jordan masses 仍支付左右 traces；raw logarithms 只有联合后才有限。ordinary-budget 抽象族不等于 NSE 多-face 构造。<a href="/notes/r0-71o.html">研究笔记</a> <a href="/recap-r0-61-r0-71p.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71P</b><strong>fixed-partition all-shell/all-cell weighted positive-entry sum</strong></header><p>下一节固定 multiplier、cutoff 与 partition，检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\)；total-Jordan sum 是更强的后续变体，暂不进入 refresh 或 moving cutoffs。</p></div>`,
    String.raw`              <div class="route-step closed"><header><b>R0.71O</b><strong>soft quotient 恢复一侧 traces 与 Jordan face atoms</strong></header><p>精确 factorization 把 soft source 分成 hard interior source 与 face layer；signed atoms 可以相消而 Jordan face costs 保留。<a href="/notes/r0-71o.html">研究笔记</a></p></div>
              <div class="route-step kept"><header><b>R0.71P</b><strong>同刻 positive entries 由空间平方和支付，时间 packing 仍开放</strong></header><p>半开窗口上的 segmented/soft entry 与 hard BV 正跳跃精确分离，初始 trace 单独扣除；bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 删除同刻 cell multiplicity。完整和变成 time-slice budget 对 distinct entry-time counting measure 的积分；componentwise relaxed 正 atoms 内部没有 signed shell–cell cancellation，但它们不一般等于 signed aggregate 的正 Jordan 部。<a href="/notes/r0-71p.html">研究笔记</a> <a href="/recap-r0-61-r0-71p.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71Q</b><strong>quantitative complex-time / parabolic-window zero packing</strong></header><p>下一节显式检查 analytic radius、complex growth、projection anchor 与窗口 covering；定性时间解析性不被写成 uniform zero count。</p></div>`,
  );
  litEdit.replace(
    '<h3>R0.71O 关闭了什么，R0.71P 只检查什么</h3>',
    '<h3>R0.71P 关闭了什么，R0.71Q 只检查什么</h3>',
  );
  litEdit.replace(
    String.raw`<p>R0.71O 没有把 soft denominator 当作删除 \(d_Q=0\) faces 的规则。soft equation 精确恢复一侧 hard traces；signed atoms 可以抵消，但 Jordan variation 仍支付 entry 与 exit。抽象 smooth paths 只排除 ordinary budgets 的普适 face-count 控制，不是 NSE 多-face 反例。R0.71P 只检查 fixed-partition weighted positive-entry sum；total-Jordan sum 是更强的后续变体。我继续用下面六条筛选。</p>`,
    String.raw`<p>R0.71P 证明 \(A_+\) 与 ordinary hard positive jump 不同，并用 cutoff support overlap 与 \(\dot H^{-1}\) square sum 支付所有同刻 entries。逐 shell–cell 先取 soft 正部再求和后，relaxed 正测度内部没有符号抵消；它不一般等于 signed aggregate 的正 Jordan 部。留下的是 distinct entry-time counting measure。R0.71Q 只检查 quantitative complex-time/parabolic-window zero packing，不引入 moving cutoff、refresh 或 total-Jordan sum。我继续用下面六条筛选。</p>`,
  );
  litEdit.replace(
    String.raw`<div class="boundary"><strong>R0.71O 的一手文献边界</strong><p><a href="https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7">Temam</a>给出周期强解经典区间内的时间解析性背景；<a href="https://doi.org/10.1007/BF02196453">Reshetnyak</a>与<a href="https://www.mathnet.ru/eng/sm4127">Vol'pert</a>给出 variation-measure 稳定性和 BV chain-rule 基础；<a href="https://doi.org/10.1007/BF01236935">Fleming–Rishel</a>及<a href="https://arxiv.org/abs/1503.01746v4">Łochowski</a>连接 BV、coarea 与 crossing counts。它们不从 Leray energy 生成本站 fixed-cell quotient 的零层 face sum。限定检索未找到同时识别一侧 Jordan atoms、又支付完整 NSE frame–cell sum 的直接定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
    String.raw`<div class="boundary"><strong>R0.71P 的一手文献边界</strong><p><a href="https://doi.org/10.1007/BF01236935">Fleming–Rishel</a>与<a href="https://arxiv.org/abs/1503.01746v4">Łochowski</a>把已有 variation 写成 coarea/upcrossing 形式，不从 Leray energy 创造 positive-entry budget。<a href="https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7">Temam</a>只在 classical interval 给逐 observable 的时间解析性；<a href="https://doi.org/10.3792/pja/1195521421">Masuda</a>的唯一延拓针对完整速度场在空间开集消失；<a href="https://doi.org/10.1016/0022-1236(89)90015-3">Foias–Temam</a>的 spatial Gevrey decay 不计 temporal crossings。两轮限定检索未找到从这些工具支付完整 entry-time counting measure 的定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  );
  litEdit.replace('文献综述 v1.00 · 2026-08-26', '文献综述 v1.01 · 2026-08-26');
}

if (litEdit.count('<b>R0.71P</b>') !== 1) throw new Error("literature: expected one R0.71P route node");
if (litEdit.count('开放接口 · R0.71Q') !== 1) throw new Error("literature: expected one R0.71Q interface");
await writeFile(literaturePath, litEdit.value);

console.log(JSON.stringify({
  status: "ok",
  release: "R0.71P",
  siteVersion: "v1.01",
  publicNotes: 140,
  currentRouteNotes: 50,
  recapNodes: 80,
  completedReleasesR070AToR071P: 42,
  next: "R0.71Q",
}, null, 2));
