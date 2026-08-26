import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71u.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71v.html");
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

html = html.replaceAll("R0.61–R0.71U", "R0.61–R0.71V");
html = html.replaceAll("R0.61 到 R0.71U", "R0.61 到 R0.71V");
html = html.replaceAll("/recap-r0-61-r0-71u.pdf", "/recap-r0-61-r0-71v.pdf");
html = html.replaceAll("/i18n-en.js?v=1.06", "/i18n-en.js?v=1.07");
replaceOne(
  ".phase{break-inside:avoid;page-break-inside:avoid;margin-bottom:1rem;position:static;width:100%;overflow:visible}",
  ".phase{break-inside:avoid;page-break-inside:avoid;margin-bottom:1rem;position:static;width:100%;overflow:visible;-webkit-box-decoration-break:clone;box-decoration-break:clone}",
  "print phase box decoration",
);

replaceOne(
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71V 的 85 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem、internal-entry no-go，再到 second-time jet 与真实有限 recurrence 的路线。",
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71V 的 86 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem、second-time jet，再到 Leray-paid excursion 与固定零层边界的路线。",
  "meta description",
);
replaceOne(
  "十二个阶段、85 个节点：从约化递推到 conditional incidence，再到 genuine internal entry、classical second-time-jet packing 与真实 2.5D finite recurrence。",
  "十二个阶段、86 个节点：从约化递推到 conditional incidence，再到 genuine internal entry、classical second-time-jet packing、Leray-paid excursion 与真实 NSE fixed-zero obstruction。",
  "og description",
);
html = html.replaceAll("R0.61 到 R0.71V 的 85 个研究节点", "R0.61 到 R0.71V 的 86 个研究节点");
replaceOne("收录节点：85", "收录节点：86", "stamp nodes");
replaceOne("回顾截止时公开笔记：145", "回顾截止时公开笔记：146", "stamp notes");
replaceOne("回顾截止节点：R0.71U", "回顾截止节点：R0.71V", "stamp latest");
replaceOne("02 · 85 节完整索引", "02 · 86 节完整索引", "toc nodes");
replaceOne(
  '<div class="metric"><strong>85</strong><span>R0.61–R0.71V 研究节点</span></div>',
  '<div class="metric"><strong>86</strong><span>R0.61–R0.71V 研究节点</span></div>',
  "metric nodes",
);
replaceOne(
  '<div class="metric"><strong>47</strong><span>R0.70A–R0.71U 完成版本</span></div>',
  '<div class="metric"><strong>48</strong><span>R0.70A–R0.71V 完成版本</span></div>',
  "metric releases",
);
replaceOne("后面的 85 个节点沿着这个缺口推进", "后面的 86 个节点沿着这个缺口推进", "scope nodes");

replaceBlock(
  '            <article class="phase"><h3>R0.71G–R0.71U',
  "</article>",
  String.raw`            <article class="phase"><h3>R0.71G–R0.71V · temporal packing、finite recurrence 与 fixed-zero boundary</h3><p>R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S–T 证明 critical packet 的 Bessel 税，并构造 genuine positive-time internal entry 以排除 bare normalized Leray–Lamb time payment。R0.71U 给出 zero-count-independent classical second-time-jet theorem；第一行 Leray-paid，第二行保留 recurrence tax，同时 exact unforced 2.5D family 排除 unit energy–enstrophy ball 上的统一 raw count。R0.71V 再证明 compact-shell excursion-height packing 可在 Leray–Hopf 层级由第一行支付，并写出 excursion-to-atom 因子 \(D_E\)。weighted area formula 与 sine test 表明 level integral 不能自动控制 distinguished zero-level quadratic trace；固定 target/window 的真实无外力 2.5D NSE 序列进一步使 second root atom 相对 first row 按 \(q^2\) 增长，而 second row 仍可支付。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/notes/r0-71r.html">R0.71R</a><a href="/notes/r0-71s.html">R0.71S</a><a href="/notes/r0-71t.html">R0.71T</a><a href="/notes/r0-71u.html">R0.71U</a><a href="/notes/r0-71v.html">R0.71V</a><a href="/figures/r0-71u-recurrence-packing.pdf">R0.71U 附图</a><a href="/figures/r0-71v-zero-level-boundary.pdf">R0.71V 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071v">R0.71V 证书</a></div></article>`,
  "last phase",
);

replaceOne("R0.61–R0.71V 的 85 节公开笔记", "R0.61–R0.71V 的 86 节公开笔记", "index heading");
replaceOne(
  '            <a href="/notes/r0-71u.html">R0.71U</a>\n          </div>',
  '            <a href="/notes/r0-71u.html">R0.71U</a>\n            <a href="/notes/r0-71v.html">R0.71V</a>\n          </div>',
  "index latest",
);
replaceOne(
  "            <li>R0.71U 的 zero-count-independent Hilbert sampling、classical all-shell second-time-jet theorem、Leray-level first row 与 stronger recurrence row；exact unforced 2.5D prescribed finite recurrence；unit energy–enstrophy ball 上 raw count 无统一界；以及 shrinking-atom 与 R0.71T target-support 边界。</li>",
  "            <li>R0.71U 的 zero-count-independent Hilbert sampling、classical all-shell second-time-jet theorem、Leray-level first row 与 stronger recurrence row；exact unforced 2.5D prescribed finite recurrence；unit energy–enstrophy ball 上 raw count 无统一界；以及 shrinking-atom 与 R0.71T target-support 边界。</li>\n            <li>R0.71V 的 Leray–Hopf compact-shell AC representatives、scale-zero excursion-height packing、精确 excursion-to-atom 因子、weighted area hierarchy 与 sine method test；以及固定 target/window 的 genuine unforced 2.5D first-row-only sampling obstruction。完整 global \\(\\nu^2\\) baseline 与替代 dynamical charge 尚未排除。</li>",
  "retained latest",
);

replaceBlock(
  '        <section id="value">',
  "        </section>",
  String.raw`        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>excursion height 已由 Leray 支付，fixed zero-level slope 仍是边界迹</h2>
          <p>截至 R0.71V，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 86 个节点解释成对千禧年问题完成了某个比例。</p>
          <p>正面结果是 Leray–Hopf compact-shell excursion theorem：归一化高度 \(H_E^2=\kappa_j^{-6}h_E^2/(\ell Y_E)\) 可统一求和，并给出 amplitude-thresholded excursion count。若另有统一 \(D_E\ge d_0&gt;0\)，它会把 R0.71U 的 root atoms 压回 first-time row；该 noncollapse 不是无条件输入。</p>
          <p>负面边界是 fixed zero-level trace。weighted coarea 对二次 slope 产生三次时间 occupation；sine path 显示 level integral 与零层迹可以分离。真实无外力 2.5D NSE 序列又在固定 target/window 下使第二个 atom 相对 first row 按 \(q^2\) 增长。它没有证明 second-time coefficient sharp，也没有排除完整 global \(\nu^2\) baseline 或另一 dynamical charge。</p>
        </section>`,
  "value section",
);

replaceBlock(
  '        <section id="next">',
  "        </section>",
  String.raw`        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71W 检查完整 Leray ledger</h2>
          <p>下一有限任务移除或平衡 decoupled background，量化 fixed-target high-frequency events 相对完整 \(\nu^2\) baseline 与 projected rotational term 的大小。</p>
          <p>负面结论必须让 atom 相对完整账本保持非坍缩；正面结论需要新的 dynamical inequality，不能从 \(L^1\) level occupation 直接读取 distinguished zero-level boundary trace。R0.71W 仍不宣称继续性、奇性排除或全局正则性。</p>
        </section>`,
  "next section",
);

replaceOne(
  '<a href="/notes/r0-71u.html">打开最新节点 R0.71U</a>',
  '<a href="/notes/r0-71v.html">打开最新节点 R0.71V</a>',
  "latest note link",
);

if (/我们|攻关|主攻|三重审计/.test(html)) throw new Error("R0.71V recap must use singular or neutral voice");
const index = html.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
if ((index.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length !== 86) {
  throw new Error("R0.71V recap node index must contain exactly 86 notes");
}
for (const token of [
  "收录节点：86",
  "回顾截止时公开笔记：146",
  "R0.70A–R0.71V 完成版本",
  "excursion-to-atom",
  "fixed zero-level",
  "完整 global \\(\\nu^2\\) baseline",
  "R0.71W",
]) {
  if (!html.includes(token)) throw new Error("missing recap token: " + token);
}

await writeFile(outputPath, html);
console.log(JSON.stringify({ status: "ok", recap: outputPath, nodes: 86, next: "R0.71W" }, null, 2));
