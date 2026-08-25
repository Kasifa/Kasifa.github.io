import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71n.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71o.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) {
    throw new Error("expected one match, found " + count + ": " + before.slice(0, 120));
  }
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71N 的 78 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合、增量—投影接口与 signed second jet 的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71O 的 79 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、signed second jet 与 soft-denominator face measure 的路线。"',
);
replaceExact(
  'content="R0.61–R0.71N｜R0.60 之后的研究回顾"',
  'content="R0.61–R0.71O｜R0.60 之后的研究回顾"',
);
replaceExact(
  'content="十二个阶段、78 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性融合、exact increment–projective bridge 与 signed second-jet boundary。"',
  'content="十二个阶段、79 个节点：从约化递推到 projected-Lamb 局部热打包，再到 fixed-cell signed second jet 与 soft-denominator face boundary。"',
);
replaceExact(
  '<title>R0.61–R0.71N｜R0.60 之后的研究回顾</title>',
  '<title>R0.61–R0.71O｜R0.60 之后的研究回顾</title>',
);
replaceExact(
  '<script defer src="/i18n-en.js?v=0.99"></script>',
  '<script defer src="/i18n-en.js?v=1.00"></script>',
);
replaceExact(
  '<div class="eyebrow">累计回顾 · R0.61–R0.71N · 2026-08-26</div>',
  '<div class="eyebrow">累计回顾 · R0.61–R0.71O · 2026-08-26</div>',
);
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71N 的 78 个研究节点。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71O 的 79 个研究节点。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71N</strong><p>收录节点：78</p><p>回顾截止时公开笔记：138</p><p>回顾截止节点：R0.71N</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71O</strong><p>收录节点：79</p><p>回顾截止时公开笔记：139</p><p>回顾截止节点：R0.71O</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 78 节完整索引', '02 · 79 节完整索引');
replaceExact(
  '<div class="metric"><strong>78</strong><span>R0.61–R0.71N 研究节点</span></div>',
  '<div class="metric"><strong>79</strong><span>R0.61–R0.71O 研究节点</span></div>\n            <div class="metric"><strong>41</strong><span>R0.70A–R0.71O 完成版本</span></div>',
);
replaceExact('后面的 78 个节点沿着这个缺口推进。', '后面的 79 个节点沿着这个缺口推进。');
replaceExact(
  String.raw`<article class="phase"><h3>R0.71G–R0.71N · 驻留、匹配小区、黏性融合与 signed second jet</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 和固定 aligned matched cells 上证明 \(K^{-2}\) 正生成与 \(O((\nu K^4)^{-1})\) heat payment 的两阶缺口。R0.71L 把 raw viscous collar 精确融合回 localized Laplacian row；R0.71M 再给出 exact increment–projective bridge。R0.71N 从完整 \(B_{Q,t},d_{Q,t},Y_t\) 标量出发，证明 projective completion 中表面的正平方被 local filtered-enstrophy acceleration 精确消去。剩余 signed second jet 仍在临界尺度，且没有固定符号。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/figures/r0-71n-full-scalar.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071n">最新证书</a></div></article>`,
  String.raw`<article class="phase"><h3>R0.71G–R0.71O · 驻留、signed second jet 与 denominator faces</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–M 依次核对 matched-cell heat gap、viscous fusion 与 exact increment–projective bridge。R0.71N 证明表面的正平方被 local filtered-enstrophy acceleration 精确消去。R0.71O 再证明 soft quotient 精确恢复 hard 一侧迹；有限阶零点的 signed atom 可以相消，Jordan face cost 仍保留。raw source/radial logs 只有联合后才给出有限 face measure，ordinary budgets 不统一支付抽象 face count。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/figures/r0-71o-soft-denominator-faces.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071o">最新证书</a></div></article>`,
);
replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71N 的 78 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71O 的 79 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71n.html">R0.71N</a>\n          </div>',
  '            <a href="/notes/r0-71n.html">R0.71N</a>\n            <a href="/notes/r0-71o.html">R0.71O</a>\n          </div>',
);
replaceExact(
  '            <li>两个 \\(z_Q&gt;0\\) 的显式 smooth NSE initial jets 给出 \\(\\mathcal J_Q\\) 双号；这是有限初始-jet 诊断，不是时间区间符号定理。</li>',
  String.raw`            <li>两个 \(z_Q&gt;0\) 的显式 smooth NSE initial jets 给出 \(\mathcal J_Q\) 双号；这是有限初始-jet 诊断，不是时间区间符号定理。</li>
            <li>soft–hard 精确因子分解、孤立有限阶零点的一侧 traces、signed/Jordan atoms 与奇偶阶 face 分类。</li>
            <li>raw source/radial 对数质量的精确抵消、ordinary-budget 抽象分离，以及右 entry trace \(1/4\) 的 smooth NSE initial jet。</li>`,
);
replaceExact(
  '<p>截至 R0.71N，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 78 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71O，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 79 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–N 把 interior direct route 继续收缩：residence、heat-only、raw collar 与 increment split 依次被核对；完整 \(\mathcal J_Q\) 的正平方又被 local-enstrophy acceleration 精确消去。现在开放的是临界 signed second jet、soft denominator、零分母 faces 和 refresh，而不是另一个 interior quadratic rearrangement。</p>`,
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化与 denominator mass 支付。R0.71N 关闭了 fixed-cell interior 正平方候选；R0.71O 又关闭了“soft denominator 自动删除 faces”的想法。现在开放的是固定 partition 上的 all-shell/all-cell weighted positive-entry sum；total-Jordan sum 是更强的后续变体，refresh 与 moving-cutoff costs 则更靠后。</p>`,
);
replaceExact(
  String.raw`<p>R0.71N 对完整标量中的第二个正二次候选作了精确复核。完成平方会暂时出现非负 \(\mathcal P_Q^\square\)，但 \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 代回后，acceleration 中的同一 pairing 产生 \(-\mathcal P_Q^\square\) 并完全抵消。两个初始 jet 说明剩余量可以双向取号；它们没有排除时间积分后的其他 NSE signed mechanism。</p>`,
  String.raw`<p>R0.71O 把每个孤立有限阶零点的极限写成显式 atoms。signed jump 可能为零，但正负 Jordan masses 分别支付左右 traces。抽象 oscillatory paths 只排除 ordinary norms 单独控制 face count；一个真实 smooth NSE 初始 jet 给出 \(1/4\) 的右 entry trace，但没有构造大量内部 NSE faces。</p>`,
);
replaceExact(
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71O 检查 soft denominator 与一侧 face measure</h2>',
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71P 检查 fixed-partition all-shell/all-cell weighted positive-entry sum</h2>',
);
replaceExact(
  String.raw`<p>下一步仍留在固定 cell，比较 hard denominator 与 \(R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon}\)。R0.71O 检查 \(\varepsilon\downarrow0\) 时的 source measures 和 \(d_Q=0\) 一侧 faces，能否由已有 energy 与 denominator-mass budgets 统一支付。</p>`,
  String.raw`<p>下一步固定 multiplier、cutoff 与 partition，检查右侧正向进入 atoms 的主门槛 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\)。我先核对完整壳—小区求和是否存在 NSE-specific cancellation，或是否需要新的 crossing/transversality 输入。</p>`,
);
replaceExact(
  '<p>这个有限门只处理 hard/soft 极限与一侧时间面，不进入 refresh atoms 或 moving cutoffs。若 source measure 需要未控制的逆分母或新的临界输入，应把它明确记为条件，而不是从 interior identity 中重复制造支付。</p>',
  String.raw`<p>R0.71P 仍不引入 partition refresh 或 moving cutoffs。\(A_{j,Q,+}+A_{j,Q,-}\) 的 total-Jordan sum 是更强的后续变体，不是这一节的首要门槛；若正向进入和只能在额外 weighted-BV、zero-count 或 inverse-denominator 条件下闭合，我会把条件保留在 theorem 中。</p>`,
);
replaceExact(
  '<a href="/notes/r0-71n.html">打开最新节点 R0.71N</a>',
  '<a href="/notes/r0-71o.html">打开最新节点 R0.71O</a>',
);
replaceExact(
  '<a href="/recap-r0-61-r0-71n.pdf">下载同步 PDF</a>',
  '<a href="/recap-r0-61-r0-71o.pdf">下载同步 PDF</a>',
);
replaceExact(
  'R0.61–R0.71N 回顾 · 2026-08-26',
  'R0.61–R0.71O 回顾 · 2026-08-26',
);

const r071oLinks = html.split('href="/notes/r0-71o.html"').length - 1;
if (r071oLinks !== 3) {
  throw new Error("expected three R0.71O recap links, found " + r071oLinks);
}
if (!html.includes("收录节点：79") || !html.includes("回顾截止时公开笔记：139")) {
  throw new Error("recap totals were not updated");
}
if (!html.includes("R0.70A–R0.71O 完成版本")) {
  throw new Error("41-release range was not added");
}
if (!html.includes("R0.71P 检查 fixed-partition all-shell/all-cell weighted positive-entry sum")) {
  throw new Error("recap next gate was not updated");
}

await writeFile(outputPath, html);
console.log(JSON.stringify({
  status: "ok",
  source: sourcePath,
  output: outputPath,
  recapNodes: 79,
  publicNotes: 139,
  completedReleasesR070AToR071O: 41,
  endpoint: "R0.71O",
  next: "R0.71P",
  r071oNoteLinks: r071oLinks,
}, null, 2));
