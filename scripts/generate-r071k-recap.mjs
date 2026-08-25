import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71j.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71k.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) throw new Error("expected one match, found " + count + ": " + before.slice(0, 90));
  html = html.replace(before, after);
}

function replaceBetween(start, end, replacement) {
  const startIndex = html.indexOf(start);
  if (startIndex < 0) throw new Error("start marker not found: " + start);
  const endIndex = html.indexOf(end, startIndex);
  if (endIndex < 0) throw new Error("end marker not found: " + end);
  html = html.slice(0, startIndex) + replacement + html.slice(endIndex + end.length);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71J 的 74 个研究节点，记录从约化递推到 projected-Lamb 热体积、联合单边生成、全壳正缺陷与完整宽父框架尺度边界的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71K 的 75 个研究节点，记录从约化递推到 projected-Lamb 热体积、全壳正缺陷、匹配小区局部化与主阶 collar 边界的路线。"',
);
replaceExact('content="R0.61–R0.71J｜R0.60 之后的研究回顾"', 'content="R0.61–R0.71K｜R0.60 之后的研究回顾"');
replaceExact(
  'content="十二个阶段、74 个节点：从约化递推到 projected-Lamb 局部热打包，再到联合抛物恒等式、全壳正缺陷和完整宽父框架尺度边界。"',
  'content="十二个阶段、75 个节点：从约化递推到 projected-Lamb 局部热打包，再到全壳正缺陷、固定匹配小区 heat gap 和主阶 collar 边界。"',
);
replaceExact("<title>R0.61–R0.71J｜R0.60 之后的研究回顾</title>", "<title>R0.61–R0.71K｜R0.60 之后的研究回顾</title>");
replaceExact('<script defer src="/i18n-en.js?v=0.95"></script>', '<script defer src="/i18n-en.js?v=0.96"></script>');
replaceExact(
  '      .timeline{display:block}\n      .phase{break-inside:avoid;page-break-inside:avoid;margin-bottom:1rem}',
  '      .timeline{display:block;overflow:visible}\n      .phase{break-inside:avoid;page-break-inside:avoid;margin-bottom:1rem;position:static;width:100%;overflow:visible}\n      .phase:nth-child(2){break-before:page;page-break-before:always}\n      .phase:nth-child(7){break-before:page;page-break-before:always}',
);
replaceExact('<div class="eyebrow">累计回顾 · R0.61–R0.71J · 2026-08-26</div>', '<div class="eyebrow">累计回顾 · R0.61–R0.71K · 2026-08-26</div>');
replaceExact(
  "这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71J 的 74 个研究节点。",
  "这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71K 的 75 个研究节点。",
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71J</strong><p>收录节点：74</p><p>回顾截止时公开笔记：134</p><p>回顾截止节点：R0.71J</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71K</strong><p>收录节点：75</p><p>回顾截止时公开笔记：135</p><p>回顾截止节点：R0.71K</p><p>问题状态：仍未解决</p></div>',
);
replaceExact(
  '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 十二个研究阶段</a></li><li><a href="#node-index">02 · 74 节完整索引</a></li>',
  '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 十二个研究阶段</a></li><li><a href="#node-index">02 · 75 节完整索引</a></li>',
);
replaceExact('<div class="metric"><strong>74</strong><span>R0.61–R0.71J 研究节点</span></div>', '<div class="metric"><strong>75</strong><span>R0.61–R0.71K 研究节点</span></div>');
replaceExact("后面的 74 个节点沿着这个缺口推进。", "后面的 75 个节点沿着这个缺口推进。");
replaceBetween(
  '<article class="phase"><h3>R0.71G–R0.71J',
  "</article>",
  String.raw`<article class="phase"><h3>R0.71G–R0.71K · 驻留、联合生成、全壳正缺陷与匹配小区</h3><p>R0.71G 排除统一 sign-only 驻留常数；R0.71H–I 把正分母方向和联合生成写成完整物理时间账本。R0.71J 证明逐壳取正部以后只留下 weighted endpoint、黏性振幅质量和 negative-source defect，并在完整 broad parent frame 上给出 \(K^2\) heat gap。R0.71K 再用一组预先固定、尺度协变、有限重叠的 aligned partitions，把零入口精确分到 \(K^3\) 个 matched cells：局部正生成仍为 \(K^{-2}\)，同一 local heat/support payment 仍为 \(O((\nu K^4)^{-1})\)。frequency-only 与 fixed matched-cell heat-only 两条支付已关闭；viscous collar 和 tangent row 是同阶开放预算。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/figures/r0-71k-matched-cell-gap.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071k">最新证书</a></div></article>`,
);
replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71J 的 74 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71K 的 75 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71j.html">R0.71J</a>\n          </div>',
  '            <a href="/notes/r0-71j.html">R0.71J</a>\n            <a href="/notes/r0-71k.html">R0.71K</a>\n          </div>',
);
replaceExact(
  "            <li>有限固定 frame/cell 的 all-shell positive-defect identity，以及 R0.71E parent-only broad frame 上完整 frequency-frame 的 \\(K^2\\) heat-payment 排除结论。</li>",
  "            <li>有限固定 frame/cell 的 all-shell positive-defect identity，以及 R0.71E parent-only broad frame 上完整 frequency-frame 的 \\(K^2\\) heat-payment 排除结论。</li>\n            <li>一组固定 aligned matched partitions 上的逐格零入口、严格分母、\\(K^{-2}\\) local positive creation 和 \\((\\nu K^4)^{-1}\\) heat/support 上界；viscous collar 保留为主阶开放项。</li>",
);
replaceExact(
  '<p>截至 R0.71J，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 74 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71K，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 75 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceBetween(
  "<p>目前最有内容的无条件正结果仍是",
  "</p>",
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积及其有界重叠局部化。R0.71G–K 把时间缺口继续收缩：residence 不足，联合阻尼把变差压到入口迹和单边生成，全壳正缺陷排除免费 signed cancellation，固定 matched cells 又排除同一 local heat/support endpoint。仍没有被控制的是 leading viscous collar、projective tangent、faces 和 refresh。</p>`,
);
replaceBetween(
  "<p>R0.71J 把 R0.71I",
  "</p>",
  String.raw`<p>R0.71K 把 R0.71J 的 global cell 量词推进到一组固定 aligned matched partitions。selected finite-cell positive creation 至少是 \(K^{-2}\)，完整 bounded-overlap local heat/support payment 至多是 \((\nu K^4)^{-1}\)。这个结果关闭 fixed matched-cell heat-only payment，但不能排除显式 collar-paid、face-paid、moving-cell 或另一 NSE-specific budget。</p>`,
);
replaceBetween(
  '<section id="next">',
  "</section>",
  String.raw`<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71L 检查 fixed-cell collar 与 tangent budget</h2>
          <p>下一步保留 fixed matched partition，不先进入 moving cells、refresh 或无限 soft limit。需要把 viscous collar 和 projective tangent contributions 分离到不破坏 radial–tangent cancellation 的程度，再检查 weighted absolute budget 是否来自现有 Leray-level NSE quantity。</p>
          <p>如果唯一上界需要未控制的导数，或只是重述完整 \(\mathcal J_Q\)，temporal-residence 分支应停止。只有出现独立、非循环的 payment，才进入 denominator faces 和 moving partitions。</p>
        </section>`,
);
replaceExact(
  '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-71i.html">保留 R0.71I 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-71j.html">打开最新节点 R0.71J</a></p>',
  '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-71j.html">保留 R0.71J 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-71k.html">打开最新节点 R0.71K</a></p>',
);
replaceExact(
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71j.pdf">下载同步 PDF</a></p>',
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71k.pdf">下载同步 PDF</a></p>',
);
replaceExact(
  '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.71J 回顾 · 2026-08-26<br><a href="/">返回研究主页</a></div></footer>',
  '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.71K 回顾 · 2026-08-26<br><a href="/">返回研究主页</a></div></footer>',
);

await writeFile(outputPath, html);
console.log(JSON.stringify({ outputPath, bytes: Buffer.byteLength(html) }, null, 2));
