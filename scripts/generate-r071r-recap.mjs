import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71q.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71r.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) {
    throw new Error(
      "expected one match, found " + count + ": " + before.slice(0, 140),
    );
  }
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71Q 的 81 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、有限条件 Jensen 定理与四项 packing 税的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71R 的 82 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 Jensen 定理与 parabolic-incidence 两阶尺度错配的路线。"',
);
replaceExact(
  'content="R0.61–R0.71Q｜R0.60 之后的研究回顾"',
  'content="R0.61–R0.71R｜R0.60 之后的研究回顾"',
);
replaceExact(
  'content="十二个阶段、81 个节点：从约化递推到 projected-Lamb 局部热打包，再到 positive-entry batching、有限条件 Jensen 定理与 anchor、truncation、cover、H-envelope 四税。"',
  'content="十二个阶段、82 个节点：从约化递推到 positive-entry batching，再到条件 Jensen、有限 parabolic incidence theorem 与 rho=0/rho=2 两阶错配。"',
);
replaceExact(
  '<title>R0.61–R0.71Q｜R0.60 之后的研究回顾</title>',
  '<title>R0.61–R0.71R｜R0.60 之后的研究回顾</title>',
);
replaceExact('/i18n-en.js?v=1.02', '/i18n-en.js?v=1.03');
replaceExact(
  '<div class="eyebrow">累计回顾 · R0.61–R0.71Q · 2026-08-26</div>',
  '<div class="eyebrow">累计回顾 · R0.61–R0.71R · 2026-08-26</div>',
);
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71Q 的 81 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71R 的 82 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71Q</strong><p>收录节点：81</p><p>回顾截止时公开笔记：141</p><p>回顾截止节点：R0.71Q</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71R</strong><p>收录节点：82</p><p>回顾截止时公开笔记：142</p><p>回顾截止节点：R0.71R</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 81 节完整索引', '02 · 82 节完整索引');
replaceExact(
  '<div class="metric"><strong>81</strong><span>R0.61–R0.71Q 研究节点</span></div>',
  '<div class="metric"><strong>82</strong><span>R0.61–R0.71R 研究节点</span></div>',
);
replaceExact(
  '<div class="metric"><strong>43</strong><span>R0.70A–R0.71Q 完成版本</span></div>',
  '<div class="metric"><strong>44</strong><span>R0.70A–R0.71R 完成版本</span></div>',
);
replaceExact('后面的 81 个节点沿着这个缺口推进。', '后面的 82 个节点沿着这个缺口推进。');
replaceExact(
  String.raw`<article class="phase"><h3>R0.71G–R0.71Q · denominator faces、temporal packing 与条件 Jensen</h3><p>R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft quotient 恢复 hard 一侧迹，R0.71P 再把同刻 positive entries 合成可由 \(\dot H^{-1}\) Lamb square sum 支付的 spatial batch，剩下 distinct entry-time counting measure。R0.71Q 在固定紧致经典时间区间与有限观测截断上证明 finite conditional Jensen theorem：只有同时给出复时间窗、上界、非零中心值、有限所有权覆盖与窗口内 \(\mathcal H\) 包络，才得到有限 weighted entry bound。定理必须保留 anchor tax、truncation tax、cover tax 与 H-envelope tax。有限 Blaschke 族与多分量族证明 analytic radius 与 complex upper bound 单独无法给出 uniform zero count；因此直接解析零点路线的无条件版本在此失败。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/figures/r0-71q-jensen-window-audit.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071q">最新证书</a></div></article>`,
  String.raw`<article class="phase"><h3>R0.71G–R0.71R · denominator faces、temporal packing、Jensen 与 incidence scale audit</h3><p>R0.71O–P 依次恢复 soft quotient 的一侧 traces，并用 bounded overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收同刻 batch；R0.71Q 给出 finite conditional Jensen theorem，同时隔离 anchor、truncation、cover 与 H-envelope 四税。R0.71R 从 NSE 导出 localized observable 的 exact forced heat equation，并证明 finite conditional event-to-window theorem；统一 window lower height 与 essential same-observable overlap 明确保留为 hypotheses。\(\Gamma_\rho\) 是 upper comparison constant，\(1/\Gamma_\rho\) 编码 lower-charge strength。rho-dependent source ledger 显示：在 normalized zero-mean torus 上，rho=2 是最小 Leray-paid 指数；对 finite covariant event/window family，\(\Gamma_\rho^{\rm opt}\) 定义为 least admissible upper comparison constant，并在协变 integer/dyadic dilation 下按 lambda^rho 缩放。整数 Fourier 初始例只定义 first-jet surrogate Gamma_{2,jet}，不是 positive-time upper comparison constant 的下界。精确两阶判决只排除一参数 endpoint-square、termwise source-square certificate (3.3) 的无条件闭合，其他 Duhamel designs 与 signed / bilinear alternatives 保持开放。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/notes/r0-71r.html">R0.71R</a><a href="/figures/r0-71r-parabolic-incidence.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071r">最新证书</a></div></article>`,
);
replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71Q 的 81 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71R 的 82 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71p.html">R0.71P</a>\n            <a href="/notes/r0-71q.html">R0.71Q</a>\n          </div>',
  '            <a href="/notes/r0-71p.html">R0.71P</a>\n            <a href="/notes/r0-71q.html">R0.71Q</a>\n            <a href="/notes/r0-71r.html">R0.71R</a>\n          </div>',
);
replaceExact(
  String.raw`            <li>有限 owned parabolic windows 上的 Hilbert-valued conditional Jensen theorem、Temam lobe 内的显式双边圆盘，以及 anchor、truncation、cover、H-envelope 四税；radius 与 upper bound 单独不能给出 uniform entry packing。</li>`,
  String.raw`            <li>有限 owned parabolic windows 上的 Hilbert-valued conditional Jensen theorem、Temam lobe 内的显式双边圆盘，以及 anchor、truncation、cover、H-envelope 四税；radius 与 upper bound 单独不能给出 uniform entry packing。</li>
            <li>localized forced heat equation、带 uniform lower height 与 essential overlap hypotheses 的 finite conditional incidence packing、rho-dependent source ledger，以及 covariant optimal constant / rho=2 minimal Leray payment 的精确两阶错配；NSE 高频例只定义 initial first-jet surrogate。</li>`,
);
replaceExact(
  '<p>截至 R0.71Q，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 81 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71R，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 82 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  String.raw`<p>目前最有内容的无条件正结果仍是 Leray 能量级的 projected-Lamb 热体积、有界重叠局部化、denominator mass 与同刻 spatial batching。R0.71Q 给出了一个可复核的有限条件 Jensen 定理，但它没有将 distinct entry-time counting measure 改写成由 Leray 预算无条件支付的量。现在开放的是 NSE-specific parabolic incidence / Carleson packing，而不是再次套用定性时间解析性。</p>`,
  String.raw`<p>目前最有内容的无条件正结果仍包括 Leray 能量级 projected-Lamb 热体积、有界重叠局部化、denominator mass、同刻 spatial batching，以及 R0.71R 在 rho=2 下由 Leray energy 支付的 truncation-uniform source integral；frame constants 因 frame 固定而不依赖 finite truncation。完整 theorem 右端仍可能因 upper comparison constant (Gamma_2) 与 essential overlap (M) 而不一致；uniform lower height 与 forward-window availability 是额外 theorem gates，不是右端因子，且同样尚未证明。</p>`,
);
replaceExact(
  String.raw`<p>R0.71Q 把直接解析路线的缺口分成四税：Jensen 必须保留 \(\log(M/|f(t_*)|)\) 的 anchor tax；观测量零点并集必须保留 truncation tax；局部圆盘所有权必须保留 cover tax；从零点数转成 weighted entry mass 必须保留 H-envelope tax。Temam 型 analytic radius 与 complex upper bound 只能支付条件定理的一部分；Blaschke 族精确证明这两项单独不能 uniform 控制实零点或正进入数。</p>`,
  String.raw`<p>R0.71R 把 certificate (3.3) 的一参数 endpoint-square、termwise source-square 缺口压成精确两阶：协变 integer/dyadic dilation 下的 optimal constant 按 lambda^rho 缩放，在 rho=0 不变，但 source ledger 要求 normalized \(L^2\)-Lamb 加 palinstrophy；Leray payment 的最小指数是 rho=2。initial jet 只给 Gamma_{2,jet} surrogate，不给 positive-time Gamma_2 下界。该方法判决不排除其他 Duhamel designs、signed、bilinear 或其他 scale-critical packet functional。</p>`,
);
replaceExact(
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71R 检查 NSE-specific parabolic incidence / Carleson packing</h2>',
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71S 检查 signed / bilinear scale-critical packet</h2>',
);
replaceExact(
  '<p>下一步不再尝试从 analytic radius 与 complex upper bound 单独数零点，而是检查 NSE 方程是否在不同 entry events 之间给出额外的抛物耦合。R0.71R 将把 events 置于局部时空抛物柱中，测试 projected-Lamb、enstrophy 与 incidence measure 能否产生对尺度可求和的 Carleson packing。</p>',
  String.raw`<p>下一步保留 entry direction 与 signed pairing，不再把目标先压成 quadratic post-entry amplitude。R0.71S 将检查是否存在 frame-summable、由 \(\dot H^{-1}\) 支付且 scale covariant 的 directional or bilinear packet functional。</p>`,
);
replaceExact(
  '<p>R0.71R 只接受能在截断扩张和逼近潜在奇性端点时保持一致、且由已经证明的 NSE 预算支付的候选不等式。如果新参数只是重命名后的 anchor、inverse denominator、strong continuation norm 或 target BV，我会明确保留条件并停止。这一步不宣称已解决千禧年问题。</p>',
  String.raw`<p>候选必须通过 integer-torus initial jet、sequential recurrence 与 repeated-window pressure tests。若 localization 丢失符号，或预算退回 \(L^2\)-Lamb / palinstrophy，我会保留条件并停止该分支。这一步不宣称已解决千禧年问题。</p>`,
);
replaceExact(
  '<a href="/notes/r0-71q.html">打开最新节点 R0.71Q</a>',
  '<a href="/notes/r0-71r.html">打开最新节点 R0.71R</a>',
);
replaceExact(
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71q.pdf">下载同步 PDF</a></p>',
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71r.pdf">下载同步 PDF</a></p>',
);
replaceExact(
  '<p>R0.70A 以后每个完成并认证的研究版本都保留 HTML、PDF、首页路线入口和首页进展入口。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>',
  '<p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>',
);
replaceExact(
  'R0.61–R0.71Q 回顾 · 2026-08-26',
  'R0.61–R0.71R 回顾 · 2026-08-26',
);

const r071rLinks = html.split('href="/notes/r0-71r.html"').length - 1;
if (r071rLinks !== 3) {
  throw new Error("expected three R0.71R recap links, found " + r071rLinks);
}
if (!html.includes("收录节点：82") || !html.includes("回顾截止时公开笔记：142")) {
  throw new Error("recap totals were not updated");
}
if (!html.includes("R0.70A–R0.71R 完成版本") || !html.includes("<strong>44</strong>")) {
  throw new Error("44-release range was not updated");
}
for (const token of [
  "rho=2 是最小 Leray-paid 指数",
  "\\Gamma_\\rho^{\\rm opt}\\) 定义为 least admissible upper comparison constant",
  "first-jet surrogate Gamma_{2,jet}",
  "不排除其他 Duhamel designs",
  "R0.71S 检查 signed / bilinear scale-critical packet",
]) {
  if (!html.includes(token)) throw new Error("missing R0.71R recap boundary: " + token);
}
for (const forbidden of [
  "incidence constant 必须携带 frequency square",
  "二次 Duhamel lower-charge route 因精确两阶错配而停止",
  "Leray-paid total source measure",
  "删除同刻 cell multiplicity",
]) {
  if (html.includes(forbidden)) throw new Error("recap overclaim remains: " + forbidden);
}
if (/我们/.test(html)) throw new Error("recap must use singular or neutral voice");

await writeFile(outputPath, html);
console.log(
  JSON.stringify(
    {
      status: "ok",
      source: sourcePath,
      output: outputPath,
      recapNodes: 82,
      publicNotes: 142,
      completedReleasesR070AToR071R: 44,
      endpoint: "R0.71R",
      next: "R0.71S",
      r071rNoteLinks: r071rLinks,
    },
    null,
    2,
  ),
);
