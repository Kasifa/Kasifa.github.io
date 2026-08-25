import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71m.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71n.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) {
    throw new Error(`expected one match, found ${count}: ${before.slice(0, 120)}`);
  }
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71M 的 77 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合与增量—投影接口的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71N 的 78 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合、增量—投影接口与 signed second jet 的路线。"',
);
replaceExact(
  'content="R0.61–R0.71M｜R0.60 之后的研究回顾"',
  'content="R0.61–R0.71N｜R0.60 之后的研究回顾"',
);
replaceExact(
  'content="十二个阶段、77 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性融合和 exact increment–projective bridge。"',
  'content="十二个阶段、78 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性融合、exact increment–projective bridge 与 signed second-jet boundary。"',
);
replaceExact(
  '<title>R0.61–R0.71M｜R0.60 之后的研究回顾</title>',
  '<title>R0.61–R0.71N｜R0.60 之后的研究回顾</title>',
);
replaceExact(
  '<script defer src="/i18n-en.js?v=0.98"></script>',
  '<script defer src="/i18n-en.js?v=0.99"></script>',
);
replaceExact(
  '<div class="eyebrow">累计回顾 · R0.61–R0.71M · 2026-08-26</div>',
  '<div class="eyebrow">累计回顾 · R0.61–R0.71N · 2026-08-26</div>',
);
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71M 的 77 个研究节点。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71N 的 78 个研究节点。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71M</strong><p>收录节点：77</p><p>回顾截止时公开笔记：137</p><p>回顾截止节点：R0.71M</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71N</strong><p>收录节点：78</p><p>回顾截止时公开笔记：138</p><p>回顾截止节点：R0.71N</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 77 节完整索引', '02 · 78 节完整索引');
replaceExact(
  '<div class="metric"><strong>77</strong><span>R0.61–R0.71M 研究节点</span></div>',
  '<div class="metric"><strong>78</strong><span>R0.61–R0.71N 研究节点</span></div>',
);
replaceExact('后面的 77 个节点沿着这个缺口推进。', '后面的 78 个节点沿着这个缺口推进。');
replaceExact(
  String.raw`<article class="phase"><h3>R0.71G–R0.71M · 驻留、匹配小区、黏性融合与增量—投影接口</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 和固定 aligned matched cells 上证明 \(K^{-2}\) 正生成与 \(O((\nu K^4)^{-1})\) heat payment 的两阶缺口。R0.71L 把 raw viscous collar 精确融合回 localized Laplacian row。R0.71M 随后证明 annular-filter Lamb commutator 的精确二次速度增量公式和完整 fixed-cell projective pairing；当前直接绝对估计产生四行临界充分账本。热包排除从标准能量类到所测试绝对临界预算的普适嵌入，但不是 NSE 解反例。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/figures/r0-71m-increment-commutator.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071m">最新证书</a></div></article>`,
  String.raw`<article class="phase"><h3>R0.71G–R0.71N · 驻留、匹配小区、黏性融合与 signed second jet</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 和固定 aligned matched cells 上证明 \(K^{-2}\) 正生成与 \(O((\nu K^4)^{-1})\) heat payment 的两阶缺口。R0.71L 把 raw viscous collar 精确融合回 localized Laplacian row；R0.71M 再给出 exact increment–projective bridge。R0.71N 从完整 \(B_{Q,t},d_{Q,t},Y_t\) 标量出发，证明 projective completion 中表面的正平方被 local filtered-enstrophy acceleration 精确消去。剩余 signed second jet 仍在临界尺度，且没有固定符号。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/figures/r0-71n-full-scalar.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071n">最新证书</a></div></article>`,
);
replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71M 的 77 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71N 的 78 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71m.html">R0.71M</a>\n          </div>',
  '            <a href="/notes/r0-71m.html">R0.71M</a>\n            <a href="/notes/r0-71n.html">R0.71N</a>\n          </div>',
);
replaceExact(
  '            <li>标准能量类与所测试 absolute increment、Carleson、normalized projected-Lamb budgets 的热包函数空间分离；该序列是线性热流，不是 NSE 解反例。</li>',
  String.raw`            <li>标准能量类与所测试 absolute increment、Carleson、normalized projected-Lamb budgets 的热包函数空间分离；该序列是线性热流，不是 NSE 解反例。</li>
            <li>完整 fixed-cell 标量的 square–residual form、\(\nu\kappa_j^2\) radial/projective 精确消去，以及 local filtered-enstrophy 代回后的正平方精确抵消。</li>
            <li>两个 \(z_Q&gt;0\) 的显式 smooth NSE initial jets 给出 \(\mathcal J_Q\) 双号；这是有限初始-jet 诊断，不是时间区间符号定理。</li>`,
);
replaceExact(
  '<p>截至 R0.71M，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 77 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71N，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 78 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–M 把直接路线继续收缩：residence 不足，逐壳正部没有免费 telescope，fixed matched cells 排除同一 heat endpoint，raw collar 融合回 signed row，increment route 又被压成四个明确消费者。完整 \(\mathcal J_Q\) 是否还有第二次 signed fusion、faces 和 refresh 仍未闭合。</p>`,
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–N 把 interior direct route 继续收缩：residence、heat-only、raw collar 与 increment split 依次被核对；完整 \(\mathcal J_Q\) 的正平方又被 local-enstrophy acceleration 精确消去。现在开放的是临界 signed second jet、soft denominator、零分母 faces 和 refresh，而不是另一个 interior quadratic rearrangement。</p>`,
);
replaceExact(
  String.raw`<p>R0.71M 对 critical increment 候选作了精确复核。\(\mathcal R_j\) 有二次速度增量表示，但 \(\operatorname{curl}\mathcal R_j\) 作为分裂行没有一般上频率支撑；只有与 resolved transport 融合后的 \(G_j\) 保持环带。热包证明能量类不普适支付当前 absolute budgets，但没有构造“bounded increment defect / unbounded signed tangent”的 NSE 反例，因此更深的 signed estimate 没有被排除。</p>`,
  String.raw`<p>R0.71N 对完整标量中的第二个正二次候选作了精确复核。完成平方会暂时出现非负 \(\mathcal P_Q^\square\)，但 \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 代回后，acceleration 中的同一 pairing 产生 \(-\mathcal P_Q^\square\) 并完全抵消。两个初始 jet 说明剩余量可以双向取号；它们没有排除时间积分后的其他 NSE signed mechanism。</p>`,
);
replaceExact(
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71N 检查完整标量的第二次融合或 signed residual</h2>',
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71O 检查 soft denominator 与一侧 face measure</h2>',
);
replaceExact(
  String.raw`<p>下一步仍不进入 faces、refresh 或 moving cells，也不把四行直接账本逐项绝对化。R0.71N 从完整 \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial identity 和 \(B_Q\) 的局部 filtered-enstrophy 表示，最后才取正部或绝对值。</p>`,
  String.raw`<p>下一步仍留在固定 cell，比较 hard denominator 与 \(R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon}\)。R0.71O 检查 \(\varepsilon\downarrow0\) 时的 source measures 和 \(d_Q=0\) 一侧 faces，能否由已有 energy 与 denominator-mass budgets 统一支付。</p>`,
);
replaceExact(
  String.raw`<p>可接受的结果有两个：得到第二个精确标量融合，或者留下一个公式明确、符号仍开放的 residual。局部 filtered enstrophy 与 \(d_Q\) 是不同状态量，所以两种结果都不能预设；审计完成前不进入 denominator faces 和 moving partitions。</p>`,
  '<p>这个有限门只处理 hard/soft 极限与一侧时间面，不进入 refresh atoms 或 moving cutoffs。若 source measure 需要未控制的逆分母或新的临界输入，应把它明确记为条件，而不是从 interior identity 中重复制造支付。</p>',
);
replaceExact(
  '<a href="/notes/r0-71m.html">打开最新节点 R0.71M</a>',
  '<a href="/notes/r0-71n.html">打开最新节点 R0.71N</a>',
);
replaceExact(
  '<a href="/recap-r0-61-r0-71m.pdf">下载同步 PDF</a>',
  '<a href="/recap-r0-61-r0-71n.pdf">下载同步 PDF</a>',
);
replaceExact(
  'R0.61–R0.71M 回顾 · 2026-08-26',
  'R0.61–R0.71N 回顾 · 2026-08-26',
);

const r071nLinks = html.split('href="/notes/r0-71n.html"').length - 1;
if (r071nLinks !== 3) {
  throw new Error(`expected three R0.71N recap links, found ${r071nLinks}`);
}
if (!html.includes('收录节点：78') || !html.includes('回顾截止时公开笔记：138')) {
  throw new Error('recap totals were not updated');
}
if (!html.includes('R0.71O 检查 soft denominator 与一侧 face measure')) {
  throw new Error('recap next gate was not updated');
}

await writeFile(outputPath, html);
console.log(JSON.stringify({
  status: "ok",
  source: sourcePath,
  output: outputPath,
  recapNodes: 78,
  publicNotes: 138,
  endpoint: "R0.71N",
  next: "R0.71O",
  r071nNoteLinks: r071nLinks,
}, null, 2));
