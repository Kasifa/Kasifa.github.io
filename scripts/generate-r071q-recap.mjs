import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71p.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71q.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) {
    throw new Error("expected one match, found " + count + ": " + before.slice(0, 120));
  }
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71P 的 80 个研究节点，记录从约化递推到 projected-Lamb 热体积、soft-denominator faces、同刻 spatial batching 与 temporal-packing boundary 的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71Q 的 81 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、有限条件 Jensen 定理与四项 packing 税的路线。"',
);
replaceExact(
  'content="R0.61–R0.71P｜R0.60 之后的研究回顾"',
  'content="R0.61–R0.71Q｜R0.60 之后的研究回顾"',
);
replaceExact(
  'content="十二个阶段、80 个节点：从约化递推到 projected-Lamb 局部热打包，再到 soft-denominator faces、同刻 spatial batching 与 temporal-packing boundary。"',
  'content="十二个阶段、81 个节点：从约化递推到 projected-Lamb 局部热打包，再到 positive-entry batching、有限条件 Jensen 定理与 anchor、truncation、cover、H-envelope 四税。"',
);
replaceExact(
  '<title>R0.61–R0.71P｜R0.60 之后的研究回顾</title>',
  '<title>R0.61–R0.71Q｜R0.60 之后的研究回顾</title>',
);
replaceExact('/i18n-en.js?v=1.01', '/i18n-en.js?v=1.02');
replaceExact(
  '<div class="eyebrow">累计回顾 · R0.61–R0.71P · 2026-08-26</div>',
  '<div class="eyebrow">累计回顾 · R0.61–R0.71Q · 2026-08-26</div>',
);
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71P 的 80 个研究节点。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71Q 的 81 个研究节点。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71P</strong><p>收录节点：80</p><p>回顾截止时公开笔记：140</p><p>回顾截止节点：R0.71P</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71Q</strong><p>收录节点：81</p><p>回顾截止时公开笔记：141</p><p>回顾截止节点：R0.71Q</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 80 节完整索引', '02 · 81 节完整索引');
replaceExact(
  '<div class="metric"><strong>80</strong><span>R0.61–R0.71P 研究节点</span></div>',
  '<div class="metric"><strong>81</strong><span>R0.61–R0.71Q 研究节点</span></div>',
);
replaceExact(
  '<div class="metric"><strong>42</strong><span>R0.70A–R0.71P 完成版本</span></div>',
  '<div class="metric"><strong>43</strong><span>R0.70A–R0.71Q 完成版本</span></div>',
);
replaceExact('后面的 80 个节点沿着这个缺口推进。', '后面的 81 个节点沿着这个缺口推进。');
replaceExact(
  String.raw`<article class="phase"><h3>R0.71G–R0.71P · 驻留、denominator faces 与 temporal packing</h3><p>R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft quotient 恢复 hard 一侧迹，Jordan face cost 没有自动消失。R0.71P 再把正进入和识别为 componentwise relaxed positive-entry measure：它由逐 shell–cell 的 soft 正部先取极限、再求和得到，一般不等于 signed aggregate 的正 Jordan 部；该正测度内部没有直接的 signed shell–cell cancellation。同刻 entries 可由 bounded support overlap 与 \(\dot H^{-1}\) Littlewood–Paley square sum 做 spatial batching。完整累积仍是 time-slice budget 对 distinct entry-time counting measure 的积分，temporal packing 尚未闭合。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/figures/r0-71p-positive-entry-batching.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071p">最新证书</a></div></article>`,
  String.raw`<article class="phase"><h3>R0.71G–R0.71Q · denominator faces、temporal packing 与条件 Jensen</h3><p>R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft quotient 恢复 hard 一侧迹，R0.71P 再把同刻 positive entries 合成可由 \(\dot H^{-1}\) Lamb square sum 支付的 spatial batch，剩下 distinct entry-time counting measure。R0.71Q 在固定紧致经典时间区间与有限观测截断上证明 finite conditional Jensen theorem：只有同时给出复时间窗、上界、非零中心值、有限所有权覆盖与窗口内 \(\mathcal H\) 包络，才得到有限 weighted entry bound。定理必须保留 anchor tax、truncation tax、cover tax 与 H-envelope tax。有限 Blaschke 族与多分量族证明 analytic radius 与 complex upper bound 单独无法给出 uniform zero count；因此直接解析零点路线的无条件版本在此失败。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/figures/r0-71q-jensen-window-audit.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071q">最新证书</a></div></article>`,
);
replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71P 的 80 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71Q 的 81 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71p.html">R0.71P</a>\n          </div>',
  '            <a href="/notes/r0-71p.html">R0.71P</a>\n            <a href="/notes/r0-71q.html">R0.71Q</a>\n          </div>',
);
replaceExact(
  String.raw`            <li>同刻 positive entries 的 bounded-overlap spatial batching、distinct entry-time counting-measure reduction、有限解析截断与 sharp NSE initial entry。</li>`,
  String.raw`            <li>同刻 positive entries 的 bounded-overlap spatial batching、distinct entry-time counting-measure reduction、有限解析截断与 sharp NSE initial entry。</li>
            <li>有限 owned parabolic windows 上的 Hilbert-valued conditional Jensen theorem、Temam lobe 内的显式双边圆盘，以及 anchor、truncation、cover、H-envelope 四税；radius 与 upper bound 单独不能给出 uniform entry packing。</li>`,
);
replaceExact(
  '<p>截至 R0.71P，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 80 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71Q，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 81 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化与 denominator mass 支付。R0.71N 关闭 fixed-cell interior 正平方候选，R0.71O 关闭“soft denominator 自动删除 faces”的想法；R0.71P 又删除同刻 spatial multiplicity，并确认 componentwise relaxed 正 atoms 内部不能直接做 signed shell–cell cancellation。现在开放的是 distinct entry-time counting measure 的 uniform NSE packing。</p>`,
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化、denominator mass 与同刻 spatial batching。R0.71Q 给出了一个可复核的有限条件 Jensen 定理，但它没有将 distinct entry-time counting measure 改写成由 Leray 预算无条件支付的量。现在开放的是 NSE-specific parabolic incidence / Carleson packing，而不是再次套用定性时间解析性。</p>`,
);
replaceExact(
  String.raw`<p>R0.71P 把每个 entry time 的全部 faces 先合成一个 spatial batch，并由 cutoff support overlap 与 \(\dot H^{-1}\) Lamb square sum 支付。对半开窗口 \(K=[a,b)\) 且 \([a,b]\Subset I_{\rm strong}\)，固定有限 frame–cell 截断只有有限 entry mass；定性时间解析性却不给跨截断、跨解或逼近潜在奇性端点时的统一计数。sequential abstract path 只证明 ordinary budgets 不支付 distinct-time packing，不是 NSE 多-face 反例。</p>`,
  String.raw`<p>R0.71Q 把直接解析路线的缺口分成四税：Jensen 必须保留 \(\log(M/|f(t_*)|)\) 的 anchor tax；观测量零点并集必须保留 truncation tax；局部圆盘所有权必须保留 cover tax；从零点数转成 weighted entry mass 必须保留 H-envelope tax。Temam 型 analytic radius 与 complex upper bound 只能支付条件定理的一部分；Blaschke 族精确证明这两项单独不能 uniform 控制实零点或正进入数。</p>`,
);
replaceExact(
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71Q 检查 quantitative complex-time/parabolic-window zero packing</h2>',
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71R 检查 NSE-specific parabolic incidence / Carleson packing</h2>',
);
replaceExact(
  String.raw`<p>下一步把 quantitative complex-time Jensen bound 放进 parabolic windows，逐项记录 analytic radius \(R\)、complex growth \(M\)、projection anchor \(\|C(t_*)\|\) 与窗口 covering。目标是检查这些量能否给 distinct entry times 一个可由 NSE 预算支付的 packing estimate，而不是把定性解析性直接写成 uniform zero count。</p>`,
  String.raw`<p>下一步不再尝试从 analytic radius 与 complex upper bound 单独数零点，而是检查 NSE 方程是否在不同 entry events 之间给出额外的抛物耦合。R0.71R 将把 events 置于局部时空抛物柱中，测试 projected-Lamb、enstrophy 与 incidence measure 能否产生对尺度可求和的 Carleson packing。</p>`,
);
replaceExact(
  '<p>R0.71Q 仍不引入 moving cutoff、refresh 或更强的 total-Jordan sum。若 analytic radius、growth 或 anchor 只能由已知 continuation norm、inverse denominator、target BV 或额外 transversality 支付，我会把 zero-count route 保留为条件结论并停止这一分支。</p>',
  '<p>R0.71R 只接受能在截断扩张和逼近潜在奇性端点时保持一致、且由已经证明的 NSE 预算支付的候选不等式。如果新参数只是重命名后的 anchor、inverse denominator、strong continuation norm 或 target BV，我会明确保留条件并停止。这一步不宣称已解决千禧年问题。</p>',
);
replaceExact(
  '<a href="/notes/r0-71p.html">打开最新节点 R0.71P</a>',
  '<a href="/notes/r0-71q.html">打开最新节点 R0.71Q</a>',
);
replaceExact(
  '<a href="/recap-r0-61-r0-71p.pdf">下载同步 PDF</a>',
  '<a href="/recap-r0-61-r0-71q.pdf">下载同步 PDF</a>',
);
replaceExact(
  'R0.61–R0.71P 回顾 · 2026-08-26',
  'R0.61–R0.71Q 回顾 · 2026-08-26',
);

const r071qLinks = html.split('href="/notes/r0-71q.html"').length - 1;
if (r071qLinks !== 3) {
  throw new Error("expected three R0.71Q recap links, found " + r071qLinks);
}
if (!html.includes("收录节点：81") || !html.includes("回顾截止时公开笔记：141")) {
  throw new Error("recap totals were not updated");
}
if (!html.includes("R0.70A–R0.71Q 完成版本") || !html.includes("<strong>43</strong>")) {
  throw new Error("43-release range was not updated");
}
for (const tax of ["anchor tax", "truncation tax", "cover tax", "H-envelope tax"]) {
  if (!html.includes(tax)) {
    throw new Error("missing R0.71Q ledger: " + tax);
  }
}
if (!html.includes("finite conditional Jensen theorem")) {
  throw new Error("finite conditional Jensen theorem is missing");
}
if (!html.includes("analytic radius 与 complex upper bound 单独无法给出 uniform zero count")) {
  throw new Error("unconditional radius-plus-upper-bound failure is missing");
}
if (!html.includes("R0.71R 检查 NSE-specific parabolic incidence / Carleson packing")) {
  throw new Error("R0.71R next gate was not updated");
}
if (!html.includes("这一步不宣称已解决千禧年问题")) {
  throw new Error("Millennium-problem boundary is missing");
}

await writeFile(outputPath, html);
console.log(JSON.stringify({
  status: "ok",
  source: sourcePath,
  output: outputPath,
  recapNodes: 81,
  publicNotes: 141,
  completedReleasesR070AToR071Q: 43,
  endpoint: "R0.71Q",
  next: "R0.71R",
  r071qNoteLinks: r071qLinks,
  ledgers: ["anchor", "truncation", "cover", "H-envelope"],
}, null, 2));
