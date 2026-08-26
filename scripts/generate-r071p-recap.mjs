import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71o.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71p.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) {
    throw new Error("expected one match, found " + count + ": " + before.slice(0, 120));
  }
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71O 的 79 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、signed second jet 与 soft-denominator face measure 的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71P 的 80 个研究节点，记录从约化递推到 projected-Lamb 热体积、soft-denominator faces、同刻 spatial batching 与 temporal-packing boundary 的路线。"',
);
replaceExact(
  'content="R0.61–R0.71O｜R0.60 之后的研究回顾"',
  'content="R0.61–R0.71P｜R0.60 之后的研究回顾"',
);
replaceExact(
  'content="十二个阶段、79 个节点：从约化递推到 projected-Lamb 局部热打包，再到 fixed-cell signed second jet 与 soft-denominator face boundary。"',
  'content="十二个阶段、80 个节点：从约化递推到 projected-Lamb 局部热打包，再到 soft-denominator faces、同刻 spatial batching 与 temporal-packing boundary。"',
);
replaceExact(
  '<title>R0.61–R0.71O｜R0.60 之后的研究回顾</title>',
  '<title>R0.61–R0.71P｜R0.60 之后的研究回顾</title>',
);
replaceExact(
  '<script defer src="/i18n-en.js?v=1.00"></script>',
  '<script defer src="/i18n-en.js?v=1.01"></script>',
);
replaceExact(
  '<div class="eyebrow">累计回顾 · R0.61–R0.71O · 2026-08-26</div>',
  '<div class="eyebrow">累计回顾 · R0.61–R0.71P · 2026-08-26</div>',
);
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71O 的 79 个研究节点。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71P 的 80 个研究节点。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71O</strong><p>收录节点：79</p><p>回顾截止时公开笔记：139</p><p>回顾截止节点：R0.71O</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71P</strong><p>收录节点：80</p><p>回顾截止时公开笔记：140</p><p>回顾截止节点：R0.71P</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 79 节完整索引', '02 · 80 节完整索引');
replaceExact(
  '<div class="metric"><strong>79</strong><span>R0.61–R0.71O 研究节点</span></div>',
  '<div class="metric"><strong>80</strong><span>R0.61–R0.71P 研究节点</span></div>',
);
replaceExact(
  '<div class="metric"><strong>41</strong><span>R0.70A–R0.71O 完成版本</span></div>',
  '<div class="metric"><strong>42</strong><span>R0.70A–R0.71P 完成版本</span></div>',
);
replaceExact('后面的 79 个节点沿着这个缺口推进。', '后面的 80 个节点沿着这个缺口推进。');
replaceExact(
  String.raw`<article class="phase"><h3>R0.71G–R0.71O · 驻留、signed second jet 与 denominator faces</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–M 依次核对 matched-cell heat gap、viscous fusion 与 exact increment–projective bridge。R0.71N 证明表面的正平方被 local filtered-enstrophy acceleration 精确消去。R0.71O 再证明 soft quotient 精确恢复 hard 一侧迹；有限阶零点的 signed atom 可以相消，Jordan face cost 仍保留。raw source/radial logs 只有联合后才给出有限 face measure，ordinary budgets 不统一支付抽象 face count。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/figures/r0-71o-soft-denominator-faces.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071o">最新证书</a></div></article>`,
  String.raw`<article class="phase"><h3>R0.71G–R0.71P · 驻留、denominator faces 与 temporal packing</h3><p>R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft quotient 恢复 hard 一侧迹，Jordan face cost 没有自动消失。R0.71P 再把正进入和识别为 componentwise relaxed positive-entry measure：它由逐 shell–cell 的 soft 正部先取极限、再求和得到，一般不等于 signed aggregate 的正 Jordan 部；该正测度内部没有直接的 signed shell–cell cancellation。同刻 entries 可由 bounded support overlap 与 \(\dot H^{-1}\) Littlewood–Paley square sum 做 spatial batching。完整累积仍是 time-slice budget 对 distinct entry-time counting measure 的积分，temporal packing 尚未闭合。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/figures/r0-71p-positive-entry-batching.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071p">最新证书</a></div></article>`,
);
replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71O 的 79 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71P 的 80 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71o.html">R0.71O</a>\n          </div>',
  '            <a href="/notes/r0-71o.html">R0.71O</a>\n            <a href="/notes/r0-71p.html">R0.71P</a>\n          </div>',
);
replaceExact(
  String.raw`            <li>raw source/radial 对数质量的精确抵消、ordinary-budget 抽象分离，以及右 entry trace \(1/4\) 的 smooth NSE initial jet。</li>`,
  String.raw`            <li>raw source/radial 对数质量的精确抵消、ordinary-budget 抽象分离，以及右 entry trace \(1/4\) 的 smooth NSE initial jet。</li>
            <li>半开窗口上的 componentwise segmented/relaxed positive-entry decomposition：扣除 branch-interior variation 与 initial trace 后恢复 entries；ordinary hard BV 正跳跃与 soft entry 相差 \(\min(A_+,A_-)\)。</li>
            <li>同刻 positive entries 的 bounded-overlap spatial batching、distinct entry-time counting-measure reduction、有限解析截断与 sharp NSE initial entry。</li>`,
);
replaceExact(
  '<p>截至 R0.71O，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 79 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71P，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 80 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化与 denominator mass 支付。R0.71N 关闭了 fixed-cell interior 正平方候选；R0.71O 又关闭了“soft denominator 自动删除 faces”的想法。现在开放的是固定 partition 上的 all-shell/all-cell weighted positive-entry sum；total-Jordan sum 是更强的后续变体，refresh 与 moving-cutoff costs 则更靠后。</p>`,
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化与 denominator mass 支付。R0.71N 关闭 fixed-cell interior 正平方候选，R0.71O 关闭“soft denominator 自动删除 faces”的想法；R0.71P 又删除同刻 spatial multiplicity，并确认 componentwise relaxed 正 atoms 内部不能直接做 signed shell–cell cancellation。现在开放的是 distinct entry-time counting measure 的 uniform NSE packing。</p>`,
);
replaceExact(
  String.raw`<p>R0.71O 把每个孤立有限阶零点的极限写成显式 atoms。signed jump 可能为零，但正负 Jordan masses 分别支付左右 traces。抽象 oscillatory paths 只排除 ordinary norms 单独控制 face count；一个真实 smooth NSE 初始 jet 给出 \(1/4\) 的右 entry trace，但没有构造大量内部 NSE faces。</p>`,
  String.raw`<p>R0.71P 把每个 entry time 的全部 faces 先合成一个 spatial batch，并由 cutoff support overlap 与 \(\dot H^{-1}\) Lamb square sum 支付。对半开窗口 \(K=[a,b)\) 且 \([a,b]\Subset I_{\rm strong}\)，固定有限 frame–cell 截断只有有限 entry mass；定性时间解析性却不给跨截断、跨解或逼近潜在奇性端点时的统一计数。sequential abstract path 只证明 ordinary budgets 不支付 distinct-time packing，不是 NSE 多-face 反例。</p>`,
);
replaceExact(
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71P 检查 fixed-partition all-shell/all-cell weighted positive-entry sum</h2>',
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71Q 检查 quantitative complex-time/parabolic-window zero packing</h2>',
);
replaceExact(
  String.raw`<p>下一步固定 multiplier、cutoff 与 partition，检查右侧正向进入 atoms 的主门槛 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\)。我先核对完整壳—小区求和是否存在 NSE-specific cancellation，或是否需要新的 crossing/transversality 输入。</p>`,
  String.raw`<p>下一步把 quantitative complex-time Jensen bound 放进 parabolic windows，逐项记录 analytic radius \(R\)、complex growth \(M\)、projection anchor \(\|C(t_*)\|\) 与窗口 covering。目标是检查这些量能否给 distinct entry times 一个可由 NSE 预算支付的 packing estimate，而不是把定性解析性直接写成 uniform zero count。</p>`,
);
replaceExact(
  String.raw`<p>R0.71P 仍不引入 partition refresh 或 moving cutoffs。\(A_{j,Q,+}+A_{j,Q,-}\) 的 total-Jordan sum 是更强的后续变体，不是这一节的首要门槛；若正向进入和只能在额外 weighted-BV、zero-count 或 inverse-denominator 条件下闭合，我会把条件保留在 theorem 中。</p>`,
  '<p>R0.71Q 仍不引入 moving cutoff、refresh 或更强的 total-Jordan sum。若 analytic radius、growth 或 anchor 只能由已知 continuation norm、inverse denominator、target BV 或额外 transversality 支付，我会把 zero-count route 保留为条件结论并停止这一分支。</p>',
);
replaceExact(
  '<a href="/notes/r0-71o.html">打开最新节点 R0.71O</a>',
  '<a href="/notes/r0-71p.html">打开最新节点 R0.71P</a>',
);
replaceExact(
  '<a href="/recap-r0-61-r0-71o.pdf">下载同步 PDF</a>',
  '<a href="/recap-r0-61-r0-71p.pdf">下载同步 PDF</a>',
);
replaceExact(
  'R0.61–R0.71O 回顾 · 2026-08-26',
  'R0.61–R0.71P 回顾 · 2026-08-26',
);

const r071pLinks = html.split('href="/notes/r0-71p.html"').length - 1;
if (r071pLinks !== 3) {
  throw new Error("expected three R0.71P recap links, found " + r071pLinks);
}
if (!html.includes("收录节点：80") || !html.includes("回顾截止时公开笔记：140")) {
  throw new Error("recap totals were not updated");
}
if (!html.includes("R0.70A–R0.71P 完成版本")) {
  throw new Error("42-release range was not updated");
}
if (!html.includes("componentwise relaxed positive-entry measure")) {
  throw new Error("componentwise relaxed positive-entry statement is missing");
}
if (!html.includes("distinct entry-time counting measure")) {
  throw new Error("distinct entry-time packing boundary is missing");
}
if (!html.includes("R0.71Q 检查 quantitative complex-time/parabolic-window zero packing")) {
  throw new Error("recap next gate was not updated");
}

await writeFile(outputPath, html);
console.log(JSON.stringify({
  status: "ok",
  source: sourcePath,
  output: outputPath,
  recapNodes: 80,
  publicNotes: 140,
  completedReleasesR070AToR071P: 42,
  endpoint: "R0.71P",
  next: "R0.71Q",
  r071pNoteLinks: r071pLinks,
}, null, 2));
