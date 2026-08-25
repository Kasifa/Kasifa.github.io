import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71i.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71j.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) {
    throw new Error("expected one match, found " + count + ": " + before.slice(0, 90));
  }
  html = html.replace(before, after);
}

function replaceBetween(start, end, replacement) {
  const startIndex = html.indexOf(start);
  if (startIndex < 0) throw new Error("start marker not found: " + start);
  const endIndex = html.indexOf(end, startIndex);
  if (endIndex < 0) throw new Error("end marker not found: " + end);
  if (html.indexOf(start, startIndex + start.length) >= 0) {
    throw new Error("start marker is not unique: " + start);
  }
  html =
    html.slice(0, startIndex) +
    replacement +
    html.slice(endIndex + end.length);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71I 的 73 个研究节点，记录从约化递推到 projected-Lamb 热体积、驻留边界、投影热曲率与联合单边生成的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71J 的 74 个研究节点，记录从约化递推到 projected-Lamb 热体积、联合单边生成、全壳正缺陷与完整宽父框架尺度边界的路线。"',
);
replaceExact(
  'content="R0.61–R0.71I｜R0.60 之后的研究回顾"',
  'content="R0.61–R0.71J｜R0.60 之后的研究回顾"',
);
replaceExact(
  'content="十二个阶段、73 个节点：从约化递推到 projected-Lamb 局部热打包，再到驻留门槛、联合抛物恒等式和零入口 2D3C 尺度边界。"',
  'content="十二个阶段、74 个节点：从约化递推到 projected-Lamb 局部热打包，再到联合抛物恒等式、全壳正缺陷和完整宽父框架尺度边界。"',
);
replaceExact(
  "<title>R0.61–R0.71I｜R0.60 之后的研究回顾</title>",
  "<title>R0.61–R0.71J｜R0.60 之后的研究回顾</title>",
);
replaceExact(
  '<script defer src="/i18n-en.js?v=0.94"></script>',
  '<script defer src="/i18n-en.js?v=0.95"></script>',
);
replaceExact(
  '<div class="eyebrow">累计回顾 · R0.61–R0.71I · 2026-08-26</div>',
  '<div class="eyebrow">累计回顾 · R0.61–R0.71J · 2026-08-26</div>',
);
replaceExact(
  "这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71I 的 73 个研究节点。",
  "这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71J 的 74 个研究节点。",
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71I</strong><p>收录节点：73</p><p>回顾截止时公开笔记：133</p><p>回顾截止节点：R0.71I</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71J</strong><p>收录节点：74</p><p>回顾截止时公开笔记：134</p><p>回顾截止节点：R0.71J</p><p>问题状态：仍未解决</p></div>',
);
replaceExact(
  '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 十二个研究阶段</a></li><li><a href="#node-index">02 · 73 节完整索引</a></li>',
  '<li><a href="#result">00 · 回顾范围</a></li><li><a href="#timeline">01 · 十二个研究阶段</a></li><li><a href="#node-index">02 · 74 节完整索引</a></li>',
);
replaceExact(
  '<div class="metric"><strong>73</strong><span>R0.61–R0.71I 研究节点</span></div>',
  '<div class="metric"><strong>74</strong><span>R0.61–R0.71J 研究节点</span></div>',
);
replaceExact(
  "后面的 73 个节点沿着这个缺口推进。",
  "后面的 74 个节点沿着这个缺口推进。",
);
replaceBetween(
  '<article class="phase"><h3>R0.71G–R0.71I',
  "</article>",
  '<article class="phase"><h3>R0.71G–R0.71J · 驻留边界、联合生成与 full-frame 正缺陷</h3><p>R0.71G 排除统一 sign-only 驻留常数；R0.71H 证明正分母分支上的 projective heat identity。R0.71I 把振幅 BV 精确归约为各分支入口、单边联合生成、时间面和刷新原子，并用零入口 2D3C 脉冲排除一个固定双环 component 的 heat-volume-only 支付。R0.71J 进一步证明，逐壳取正部以后，完整 frame 求和只留下 weighted endpoint telescope、黏性振幅质量和 negative-source defect。对 R0.71E §10.1 的完整 broad parent frame、每个固定 \\(\\nu&gt;0\\) 和所有充分大 dyadic \\(K\\)，全局光滑固定能量 2D3C 家族使正生成与同一 heat endpoint 的比值至少按 \\(K^2\\) 增长。frequency-only escape 已关闭；matched spatial cells、faces 和另一 NSE budget 仍开放。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/figures/r0-71j-full-frame-gap.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071j">最新证书</a></div></article>',
);
replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71I 的 73 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71J 的 74 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71i.html">R0.71I</a>\n          </div>',
  '            <a href="/notes/r0-71i.html">R0.71I</a>\n            <a href="/notes/r0-71j.html">R0.71J</a>\n          </div>',
);
replaceExact(
  "            <li>对称八目标模 2D3C 零入口序列：精确初值 Fourier 常数、固定窗口 \\(C^1\\) 渐近脉冲，以及声明双环分量上的 heat-volume-only 两阶频率反例。</li>",
  "            <li>对称八目标模 2D3C 零入口序列：精确初值 Fourier 常数、固定窗口 \\(C^1\\) 渐近脉冲，以及声明双环分量上的 heat-volume-only 两阶频率反例。</li>\n            <li>有限固定 frame/cell 的 all-shell positive-defect identity，以及 R0.71E parent-only broad frame 上完整 frequency-frame 的 \\(K^2\\) heat-payment 排除结论。</li>",
);
replaceExact(
  '<p>截至 R0.71I，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 73 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71J，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 74 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceBetween(
  "<p>目前最有内容的无条件正结果仍是",
  "</p>",
  '<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积及其有界重叠局部化。R0.71G–J 把时间缺口继续收缩：residence 不足，单位方向有精确热几何，联合阻尼把变差压到入口迹和单边生成，而 all-shell positive-defect identity 又排除了正部之后的免费 signed cancellation。</p>',
);
replaceBetween(
  "<p>R0.71I 的 2D3C 序列比此前点态反例更强",
  "</p>",
  '<p>R0.71J 把 R0.71I 的单 component 量词推进到 R0.71E 已声明的完整 broad parent frequency frame：对每个固定 \\(\\nu&gt;0\\) 和所有充分大 dyadic \\(K\\)，正生成至少是 \\(K^{-2}\\)，同一 full-frame heat endpoint 至多是 \\(K^{-4}\\)。这关闭的是 frequency-only payment，不是 child refinement、matched spatial localization、integrated face-paid BV 或另一 NSE-specific budget 的全面否定。</p>',
);
replaceBetween(
  '<section id="next">',
  "</section>",
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71K 检查 matched spatial localization</h2>\n          <p>下一对象仍是 \\(\\sum_{j,Q}K_j^{-2}\\int z_{j,Q}^+(\\mathcal J_{j,Q})^+dt\\)，但不再重复完整 frequency frame 的求和。global cell 将被一个固定、尺度匹配、有限重叠的 spatial partition 替代。</p>\n          <p>需要保留 cutoff–curl、transport、viscous collar、\\(Y_t/Y\\)、软分母时间面和刷新原子。若局部化只把同一个正缺陷搬到未控制的 faces，这条 temporal-residence 分支应停止；只有出现真正由 Leray-level input 支付的新 coercive term，才进入无限 frame–cell 与 soft-limit 步骤。</p>\n        </section>',
);
replaceExact(
  '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-71h.html">保留 R0.71H 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-71i.html">打开最新节点 R0.71I</a></p>',
  '<p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-71i.html">保留 R0.71I 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-71j.html">打开最新节点 R0.71J</a></p>',
);
replaceExact(
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71i.pdf">下载同步 PDF</a></p>',
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71j.pdf">下载同步 PDF</a></p>',
);
replaceExact(
  '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.71I 回顾 · 2026-08-26<br><a href="/">返回研究主页</a></div></footer>',
  '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.71J 回顾 · 2026-08-26<br><a href="/">返回研究主页</a></div></footer>',
);

await writeFile(outputPath, html);
console.log(JSON.stringify({ outputPath, bytes: Buffer.byteLength(html) }, null, 2));
