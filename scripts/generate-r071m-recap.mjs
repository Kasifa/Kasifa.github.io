import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71l.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71m.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) throw new Error(`expected one match, found ${count}: ${before.slice(0, 120)}`);
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71L 的 76 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合与投影切向边界的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71M 的 77 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合与增量—投影接口的路线。"',
);
replaceExact('content="R0.61–R0.71L｜R0.60 之后的研究回顾"', 'content="R0.61–R0.71M｜R0.60 之后的研究回顾"');
replaceExact(
  'content="十二个阶段、76 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性精确融合和 projective tangent 边界。"',
  'content="十二个阶段、77 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性融合和 exact increment–projective bridge。"',
);
replaceExact('<title>R0.61–R0.71L｜R0.60 之后的研究回顾</title>', '<title>R0.61–R0.71M｜R0.60 之后的研究回顾</title>');
replaceExact('<script defer src="/i18n-en.js?v=0.97"></script>', '<script defer src="/i18n-en.js?v=0.98"></script>');
replaceExact(
  '      .phase:nth-child(7){break-before:page;page-break-before:always}\n',
  '      .phase:nth-child(7){break-before:page;page-break-before:always}\n      .phase:nth-child(12){break-before:page;page-break-before:always}\n',
);
replaceExact('<div class="eyebrow">累计回顾 · R0.61–R0.71L · 2026-08-26</div>', '<div class="eyebrow">累计回顾 · R0.61–R0.71M · 2026-08-26</div>');
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71L 的 76 个研究节点。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71M 的 77 个研究节点。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71L</strong><p>收录节点：76</p><p>回顾截止时公开笔记：136</p><p>回顾截止节点：R0.71L</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71M</strong><p>收录节点：77</p><p>回顾截止时公开笔记：137</p><p>回顾截止节点：R0.71M</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 76 节完整索引', '02 · 77 节完整索引');
replaceExact('<div class="metric"><strong>76</strong><span>R0.61–R0.71L 研究节点</span></div>', '<div class="metric"><strong>77</strong><span>R0.61–R0.71M 研究节点</span></div>');
replaceExact('后面的 76 个节点沿着这个缺口推进。', '后面的 77 个节点沿着这个缺口推进。');
replaceExact(
  String.raw`<article class="phase"><h3>R0.71G–R0.71L · 驻留、全壳正缺陷、匹配小区与黏性融合</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 先在完整 broad parent frame、再在固定 aligned matched cells 上证明 \(K^{-2}\) 正生成与 \(O((\nu K^4)^{-1})\) heat payment 的两阶缺口。R0.71L 进一步证明 raw viscous collar 与 localized Laplacian commutator 必须精确融合；逐行绝对化制造的是 representation-dependent cost。Leray 能量支付 weighted denominator mass，但当前 direct estimate 还需要 angular ratio 与 normalized Lamb quotient，尚未从标准能量不等式推出。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/figures/r0-71l-viscous-fusion.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071l">最新证书</a></div></article>`,
  String.raw`<article class="phase"><h3>R0.71G–R0.71M · 驻留、匹配小区、黏性融合与增量—投影接口</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 和固定 aligned matched cells 上证明 \(K^{-2}\) 正生成与 \(O((\nu K^4)^{-1})\) heat payment 的两阶缺口。R0.71L 把 raw viscous collar 精确融合回 localized Laplacian row。R0.71M 随后证明 annular-filter Lamb commutator 的精确二次速度增量公式和完整 fixed-cell projective pairing；当前直接绝对估计产生四行临界充分账本。热包排除从标准能量类到所测试绝对临界预算的普适嵌入，但不是 NSE 解反例。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/figures/r0-71m-increment-commutator.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071m">最新证书</a></div></article>`,
);
replaceExact('<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71L 的 76 节公开笔记</h2>', '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71M 的 77 节公开笔记</h2>');
replaceExact(
  '            <a href="/notes/r0-71l.html">R0.71L</a>\n          </div>',
  '            <a href="/notes/r0-71l.html">R0.71L</a>\n            <a href="/notes/r0-71m.html">R0.71M</a>\n          </div>',
);
replaceExact(
  '            <li>固定 cutoff 的 viscous collar 与 localized Laplacian commutator 精确融合；aligned cutoff–curl numerator 逐格为零，Leray 能量支付 denominator mass，但 fused projective tangent 仍需额外临界输入。</li>',
  '            <li>固定 cutoff 的 viscous collar 与 localized Laplacian commutator 精确融合；aligned cutoff–curl numerator 逐格为零，Leray 能量支付 denominator mass。</li>\n            <li>annular-filter Lamb commutator 的精确二次速度增量公式，以及 fixed-cell projective pairing、radial identity 与四行尺度临界直接账本。</li>\n            <li>标准能量类与所测试 absolute increment、Carleson、normalized projected-Lamb budgets 的热包函数空间分离；该序列是线性热流，不是 NSE 解反例。</li>',
);
replaceExact(
  '<p>截至 R0.71L，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 76 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71M，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 77 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  '<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–L 把时间缺口继续收缩：residence 不足，逐壳正部没有免费 signed telescope，fixed matched cells 排除同一 heat/support endpoint，raw collar 又被证明只是 fused viscous row 的坐标展开。当前路线仍未闭合 signed projective tangent、critical increment budget、faces 和 refresh。</p>',
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–M 把直接路线继续收缩：residence 不足，逐壳正部没有免费 telescope，fixed matched cells 排除同一 heat endpoint，raw collar 融合回 signed row，increment route 又被压成四个明确消费者。完整 \(\mathcal J_Q\) 是否还有第二次 signed fusion、faces 和 refresh 仍未闭合。</p>`,
);
replaceExact(
  String.raw`<p>R0.71L 对 R0.71K 留下的 collar-paid 候选作了精确复核。黏性 collar 与 localized Laplacian commutator 融合为 \(\nu\mathsf A_Q(\Delta+\kappa^2)W_j\)；单 eigenspace 例子中两个非零 expanded rows 完全相消。直接 Cauchy 后需要 angular condition number 与 normalized projected-Lamb quotient，因此 rowwise absolute collar route 关闭，但更深的 signed critical estimate 没有被排除。</p>`,
  String.raw`<p>R0.71M 对 critical increment 候选作了精确复核。\(\mathcal R_j\) 有二次速度增量表示，但 \(\operatorname{curl}\mathcal R_j\) 作为分裂行没有一般上频率支撑；只有与 resolved transport 融合后的 \(G_j\) 保持环带。热包证明能量类不普适支付当前 absolute budgets，但没有构造“bounded increment defect / unbounded signed tangent”的 NSE 反例，因此更深的 signed estimate 没有被排除。</p>`,
);
replaceExact('<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71M 检查 signed fused tangent 的临界 increment bridge</h2>', '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71N 检查完整标量的第二次融合或 signed residual</h2>');
replaceExact(
  '<p>下一步不进入 faces、refresh 或 moving cells，也不再对 raw collar 逐行绝对化。R0.71M 保留 signed fused tangent，把 nonlinear frequency source 与 viscous mismatch 写成尺度临界的 velocity-increment / commutator ledger，再逐项检查 annular 或 Carleson 假设是否真的由 Leray energy 推出。</p>',
  String.raw`<p>下一步仍不进入 faces、refresh 或 moving cells，也不把四行直接账本逐项绝对化。R0.71N 从完整 \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial identity 和 \(B_Q\) 的局部 filtered-enstrophy 表示，最后才取正部或绝对值。</p>`,
);
replaceExact(
  String.raw`<p>如果唯一上界需要未控制的导数，或只是重述完整 \(\mathcal J_Q\)，temporal-residence 分支应停止。只有出现独立、非循环的 payment，才进入 denominator faces 和 moving partitions。</p>`,
  String.raw`<p>可接受的结果有两个：得到第二个精确标量融合，或者留下一个公式明确、符号仍开放的 residual。局部 filtered enstrophy 与 \(d_Q\) 是不同状态量，所以两种结果都不能预设；审计完成前不进入 denominator faces 和 moving partitions。</p>`,
);
replaceExact('<a href="/notes/r0-71l.html">打开最新节点 R0.71L</a>', '<a href="/notes/r0-71m.html">打开最新节点 R0.71M</a>');
replaceExact('<a href="/recap-r0-61-r0-71l.pdf">下载同步 PDF</a>', '<a href="/recap-r0-61-r0-71m.pdf">下载同步 PDF</a>');
replaceExact('R0.61–R0.71L 回顾 · 2026-08-26', 'R0.61–R0.71M 回顾 · 2026-08-26');

const r071mLinks = html.split('href="/notes/r0-71m.html"').length - 1;
if (r071mLinks !== 3) throw new Error(`expected three R0.71M recap links, found ${r071mLinks}`);
if (!html.includes('收录节点：77') || !html.includes('回顾截止时公开笔记：137')) {
  throw new Error('recap totals were not updated');
}

await writeFile(outputPath, html);
console.log(JSON.stringify({
  status: "ok",
  source: sourcePath,
  output: outputPath,
  recapNodes: 77,
  publicNotes: 137,
  endpoint: "R0.71M",
  next: "R0.71N",
  r071mNoteLinks: r071mLinks,
}, null, 2));
