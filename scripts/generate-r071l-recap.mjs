import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71k.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71l.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) throw new Error(`expected one match, found ${count}: ${before.slice(0, 100)}`);
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71K 的 75 个研究节点，记录从约化递推到 projected-Lamb 热体积、全壳正缺陷、匹配小区局部化与主阶 collar 边界的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71L 的 76 个研究节点，记录从约化递推到 projected-Lamb 热体积、匹配小区 heat gap、黏性融合与投影切向边界的路线。"',
);
replaceExact('content="R0.61–R0.71K｜R0.60 之后的研究回顾"', 'content="R0.61–R0.71L｜R0.60 之后的研究回顾"');
replaceExact(
  'content="十二个阶段、75 个节点：从约化递推到 projected-Lamb 局部热打包，再到全壳正缺陷、固定匹配小区 heat gap 和主阶 collar 边界。"',
  'content="十二个阶段、76 个节点：从约化递推到 projected-Lamb 局部热打包，再到固定匹配小区 heat gap、黏性精确融合和 projective tangent 边界。"',
);
replaceExact('<title>R0.61–R0.71K｜R0.60 之后的研究回顾</title>', '<title>R0.61–R0.71L｜R0.60 之后的研究回顾</title>');
replaceExact('<script defer src="/i18n-en.js?v=0.96"></script>', '<script defer src="/i18n-en.js?v=0.97"></script>');
replaceExact('<div class="eyebrow">累计回顾 · R0.61–R0.71K · 2026-08-26</div>', '<div class="eyebrow">累计回顾 · R0.61–R0.71L · 2026-08-26</div>');
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71K 的 75 个研究节点。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71L 的 76 个研究节点。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71K</strong><p>收录节点：75</p><p>回顾截止时公开笔记：135</p><p>回顾截止节点：R0.71K</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71L</strong><p>收录节点：76</p><p>回顾截止时公开笔记：136</p><p>回顾截止节点：R0.71L</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 75 节完整索引', '02 · 76 节完整索引');
replaceExact('<div class="metric"><strong>75</strong><span>R0.61–R0.71K 研究节点</span></div>', '<div class="metric"><strong>76</strong><span>R0.61–R0.71L 研究节点</span></div>');
replaceExact('后面的 75 个节点沿着这个缺口推进。', '后面的 76 个节点沿着这个缺口推进。');
replaceExact(
  '<article class="phase"><h3>R0.71G–R0.71K · 驻留、联合生成、全壳正缺陷与匹配小区</h3><p>R0.71G 排除统一 sign-only 驻留常数；R0.71H–I 把正分母方向和联合生成写成完整物理时间账本。R0.71J 证明逐壳取正部以后只留下 weighted endpoint、黏性振幅质量和 negative-source defect，并在完整 broad parent frame 上给出 \\(K^2\\) heat gap。R0.71K 再用一组预先固定、尺度协变、有限重叠的 aligned partitions，把零入口精确分到 \\(K^3\\) 个 matched cells：局部正生成仍为 \\(K^{-2}\\)，同一 local heat/support payment 仍为 \\(O((\\nu K^4)^{-1})\\)。frequency-only 与 fixed matched-cell heat-only 两条支付已关闭；viscous collar 和 tangent row 是同阶开放预算。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/figures/r0-71k-matched-cell-gap.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071k">最新证书</a></div></article>',
  '<article class="phase"><h3>R0.71G–R0.71L · 驻留、全壳正缺陷、匹配小区与黏性融合</h3><p>R0.71G–I 把时间缺口压到入口、单边联合生成与 faces。R0.71J–K 先在完整 broad parent frame、再在固定 aligned matched cells 上证明 \\(K^{-2}\\) 正生成与 \\(O((\\nu K^4)^{-1})\\) heat payment 的两阶缺口。R0.71L 进一步证明 raw viscous collar 与 localized Laplacian commutator 必须精确融合；逐行绝对化制造的是 representation-dependent cost。Leray 能量支付 weighted denominator mass，但当前 direct estimate 还需要 angular ratio 与 normalized Lamb quotient，尚未从标准能量不等式推出。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/figures/r0-71l-viscous-fusion.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071l">最新证书</a></div></article>',
);
replaceExact('<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71K 的 75 节公开笔记</h2>', '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71L 的 76 节公开笔记</h2>');
replaceExact(
  '            <a href="/notes/r0-71k.html">R0.71K</a>\n          </div>',
  '            <a href="/notes/r0-71k.html">R0.71K</a>\n            <a href="/notes/r0-71l.html">R0.71L</a>\n          </div>',
);
replaceExact(
  '            <li>一组固定 aligned matched partitions 上的逐格零入口、严格分母、\\(K^{-2}\\) local positive creation 和 \\((\\nu K^4)^{-1}\\) heat/support 上界；viscous collar 保留为主阶开放项。</li>',
  '            <li>一组固定 aligned matched partitions 上的逐格零入口、严格分母、\\(K^{-2}\\) local positive creation 和 \\((\\nu K^4)^{-1}\\) heat/support 上界。</li>\n            <li>固定 cutoff 的 viscous collar 与 localized Laplacian commutator 精确融合；aligned cutoff–curl numerator 逐格为零，Leray 能量支付 denominator mass，但 fused projective tangent 仍需额外临界输入。</li>',
);
replaceExact(
  '<p>截至 R0.71K，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 75 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71L，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 76 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  '<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积及其有界重叠局部化。R0.71G–K 把时间缺口继续收缩：residence 不足，联合阻尼把变差压到入口迹和单边生成，全壳正缺陷排除免费 signed cancellation，固定 matched cells 又排除同一 local heat/support endpoint。仍没有被控制的是 leading viscous collar、projective tangent、faces 和 refresh。</p>',
  '<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、它的有界重叠局部化，以及 fixed-cell denominator mass 的能量支付。R0.71G–L 把时间缺口继续收缩：residence 不足，逐壳正部没有免费 signed telescope，fixed matched cells 排除同一 heat/support endpoint，raw collar 又被证明只是 fused viscous row 的坐标展开。仍没有被控制的是 signed projective tangent、critical increment budget、faces 和 refresh。</p>',
);
replaceExact(
  '<p>R0.71K 把 R0.71J 的 global cell 量词推进到一组固定 aligned matched partitions。selected finite-cell positive creation 至少是 \\(K^{-2}\\)，完整 bounded-overlap local heat/support payment 至多是 \\((\\nu K^4)^{-1}\\)。这个结果关闭 fixed matched-cell heat-only payment，但不能排除显式 collar-paid、face-paid、moving-cell 或另一 NSE-specific budget。</p>',
  '<p>R0.71L 对 R0.71K 留下的 collar-paid 候选作了精确复核。黏性 collar 与 localized Laplacian commutator 融合为 \\(\\nu\\mathsf A_Q(\\Delta+\\kappa^2)W_j\\)；单 eigenspace 例子中两个非零 expanded rows 完全相消。直接 Cauchy 后需要 angular condition number 与 normalized projected-Lamb quotient，因此 rowwise absolute collar route 关闭，但更深的 signed critical estimate 没有被排除。</p>',
);
replaceExact('<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71L 检查 fixed-cell collar 与 tangent budget</h2>', '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71M 检查 signed fused tangent 的临界 increment bridge</h2>');
replaceExact(
  '<p>下一步保留 fixed matched partition，不先进入 moving cells、refresh 或无限 soft limit。需要把 viscous collar 和 projective tangent contributions 分离到不破坏 radial–tangent cancellation 的程度，再检查 weighted absolute budget 是否来自现有 Leray-level NSE quantity。</p>',
  '<p>下一步不进入 faces、refresh 或 moving cells，也不再对 raw collar 逐行绝对化。R0.71M 保留 signed fused tangent，把 nonlinear frequency source 与 viscous mismatch 写成尺度临界的 velocity-increment / commutator ledger，再逐项检查 annular 或 Carleson 假设是否真的由 Leray energy 推出。</p>',
);
replaceExact('<a href="/notes/r0-71k.html">打开最新节点 R0.71K</a>', '<a href="/notes/r0-71l.html">打开最新节点 R0.71L</a>');
replaceExact('<a href="/recap-r0-61-r0-71k.pdf">下载同步 PDF</a>', '<a href="/recap-r0-61-r0-71l.pdf">下载同步 PDF</a>');
replaceExact('R0.61–R0.71K 回顾 · 2026-08-26', 'R0.61–R0.71L 回顾 · 2026-08-26');

await writeFile(outputPath, html);
console.log(outputPath);
