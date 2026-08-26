import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71t.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71u.html");
let html = await readFile(sourcePath, "utf8");

function replaceOne(before, after, label) {
  const count = html.split(before).length - 1;
  if (count !== 1) throw new Error(label + ": expected one match, found " + count);
  html = html.replace(before, after);
}

function replaceBlock(start, end, replacement, label) {
  const startIndex = html.indexOf(start);
  if (startIndex < 0) throw new Error(label + ": start marker missing");
  const endIndex = html.indexOf(end, startIndex);
  if (endIndex < 0) throw new Error(label + ": end marker missing");
  html = html.slice(0, startIndex) + replacement + html.slice(endIndex + end.length);
}

html = html.replaceAll("R0.61–R0.71T", "R0.61–R0.71U");
html = html.replaceAll("/recap-r0-61-r0-71t.pdf", "/recap-r0-61-r0-71u.pdf");
html = html.replaceAll("/i18n-en.js?v=1.05", "/i18n-en.js?v=1.06");
replaceOne(
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71T 的 84 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem，以及 packet/Bessel 与 NSE initial-face scaling 边界的路线。",
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71U 的 85 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem、internal-entry no-go，再到 second-time jet 与真实有限 recurrence 的路线。",
  "meta description",
);
html = html.replaceAll("R0.61 到 R0.71T 的 84 个研究节点", "R0.61 到 R0.71U 的 85 个研究节点");
replaceOne(
  "十二个阶段、84 个节点：从约化递推到 conditional incidence，再到 genuine positive-time internal entry、internal scaling no-go 与 outgoing occupation boundary。",
  "十二个阶段、85 个节点：从约化递推到 conditional incidence，再到 genuine internal entry、classical second-time-jet packing 与真实 2.5D finite recurrence。",
  "og description",
);
replaceOne("收录节点：84", "收录节点：85", "stamp nodes");
replaceOne("回顾截止时公开笔记：144", "回顾截止时公开笔记：145", "stamp notes");
replaceOne("回顾截止节点：R0.71T", "回顾截止节点：R0.71U", "stamp latest");
replaceOne("02 · 84 节完整索引", "02 · 85 节完整索引", "toc nodes");
replaceOne("<div class=\"metric\"><strong>84</strong><span>R0.61–R0.71U 研究节点</span></div>", "<div class=\"metric\"><strong>85</strong><span>R0.61–R0.71U 研究节点</span></div>", "metric nodes");
replaceOne("<div class=\"metric\"><strong>46</strong><span>R0.70A–R0.71T 完成版本</span></div>", "<div class=\"metric\"><strong>47</strong><span>R0.70A–R0.71U 完成版本</span></div>", "metric releases");
replaceOne("后面的 84 个节点沿着这个缺口推进", "后面的 85 个节点沿着这个缺口推进", "scope nodes");

replaceBlock(
  '            <article class="phase"><h3>R0.71G–R0.71T',
  "</article>",
  String.raw`            <article class="phase"><h3>R0.71G–R0.71U · temporal packing、internal entry 与 finite recurrence</h3><p>R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S 保留 entry direction 后证明 critical packet 单包即带 \(\kappa_j^2\) Bessel 税。R0.71T 用正向局部 NSE 流和 finite-dimensional IFT 构造 genuine positive-time internal entry，再以双尺度族排除 bare normalized Leray-Lamb time payment；outgoing coarea 只留下 scale-matched representation。R0.71U 对 global-shell entries 证明零点数与 separation 无关的 Hilbert sampling inequality，以及带 \(\inf_KY&gt;0\) 假设的 classical all-shell second-time-jet theorem。第一行由 normalized Leray–Lamb ledger 支付，第二行保留 \(\omega_t\) 与 \(L_t\) 的 recurrence tax，因此不是 Leray-level closure。另一个 exact unforced 2.5D NSE family 可在任意指定 finite time set 返回同一 compact annulus；unit energy–enstrophy ball 上 raw entry count 无统一界，但 atom mass 可以随 \(N\) 缩小。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/notes/r0-71r.html">R0.71R</a><a href="/notes/r0-71s.html">R0.71S</a><a href="/notes/r0-71t.html">R0.71T</a><a href="/notes/r0-71u.html">R0.71U</a><a href="/figures/r0-71t-internal-entry.pdf">R0.71T 附图</a><a href="/figures/r0-71u-recurrence-packing.pdf">R0.71U 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071u">R0.71U 证书</a></div></article>`,
  "last phase",
);

replaceOne("R0.61–R0.71U 的 84 节公开笔记", "R0.61–R0.71U 的 85 节公开笔记", "index heading");
replaceOne(
  '            <a href="/notes/r0-71t.html">R0.71T</a>\n          </div>',
  '            <a href="/notes/r0-71t.html">R0.71T</a>\n            <a href="/notes/r0-71u.html">R0.71U</a>\n          </div>',
  "index latest",
);
replaceOne(
  "            <li>R0.71T 的 finite-dimensional IFT positive-time internal-entry construction、global positive entry simplicity、induced local positive cell、bounded-energy/enstrophy internal scaling no-go、finite outgoing-coarea identity，以及带完整 \\(F_t\\)、\\(Y_t\\) 账本的 conditional trace-variation theorem。</li>",
  "            <li>R0.71T 的 finite-dimensional IFT positive-time internal-entry construction、global positive entry simplicity、induced local positive cell、bounded-energy/enstrophy internal scaling no-go、finite outgoing-coarea identity，以及带完整 \\(F_t\\)、\\(Y_t\\) 账本的 conditional trace-variation theorem。</li>\n            <li>R0.71U 的 zero-count-independent Hilbert sampling、classical all-shell second-time-jet theorem、Leray-level first row 与 stronger recurrence row；exact unforced 2.5D prescribed finite recurrence；unit energy–enstrophy ball 上 raw count 无统一界；以及 shrinking-atom 与 R0.71T target-support 边界。</li>",
  "retained latest",
);

replaceBlock(
  '        <section id="value">',
  "        </section>",
  String.raw`        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>raw count 已被真实 recurrence 排除，weighted mass 保留一条 classical 定理</h2>
          <p>截至 R0.71U，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 85 个节点解释成对千禧年问题完成了某个比例。</p>
          <p>R0.71U 的正面结果是 zero-count-independent second-time-jet estimate。它对满足 \(\inf_KY&gt;0\) 的 compact classical trajectory 成立，常数不依赖零点数、minimum separation 或 finite shell truncation。第一行有 normalized Leray–Lamb payment；第二行要求 \(\omega_t\) 与 \(L_t\)，ordinary Leray inequality 尚未关闭。</p>
          <p>负面边界同样具体：exact unforced globally smooth 2.5D NSE 解可以在每个指定 finite time set 返回同一 compact annulus，且初值保持在 unit energy–enstrophy ball 内。因此 analyticity、simplicity 与 raw counting 不能产生统一 packing law。但每个 finite set 可选择新解，atom 也可缩小；这不是 weighted-atom counterexample。</p>
        </section>`,
  "value section",
);

replaceBlock(
  '        <section id="next">',
  "        </section>",
  String.raw`        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71V 量化 weighted recurrence，并测试 Leray-paid excursion</h2>
          <p>下一有限任务比较 recurrence family 的 atom sum 与 second-time-jet theorem 两行，检查 \(C_{tt}\) recurrence tax 是否在该族上必要，并寻找不会随 \(N\) 塌缩的 normalized mass。</p>
          <p>并行测试 level-integrated 或 amplitude-thresholded excursion 是否能用 genuine Leray-paid variation 代替 fixed zero-level derivative charge。负面结论必须保持 atom mass；正面结论必须处理 distinguished zero level，而不只是 almost every positive level。R0.71V 仍不宣称继续性、奇性排除或全局正则性。</p>
        </section>`,
  "next section",
);

replaceOne(
  '<a href="/notes/r0-71t.html">打开最新节点 R0.71T</a>',
  '<a href="/notes/r0-71u.html">打开最新节点 R0.71U</a>',
  "latest note link",
);

if (/我们/.test(html)) throw new Error("R0.71U recap must use singular or neutral voice");
if ((html.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length < 85) {
  throw new Error("R0.71U recap lost public-note links");
}
for (const token of [
  "收录节点：85",
  "R0.70A–R0.71U 完成版本",
  "second-time-jet",
  "exact unforced globally smooth 2.5D NSE",
  "不是 weighted-atom counterexample",
  "R0.71V",
]) {
  if (!html.includes(token)) throw new Error("missing recap token: " + token);
}

await writeFile(outputPath, html);
console.log(JSON.stringify({ status: "ok", recap: outputPath, nodes: 85, next: "R0.71V" }, null, 2));
