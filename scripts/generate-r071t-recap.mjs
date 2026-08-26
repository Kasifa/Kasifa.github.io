import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71s.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71t.html");
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

html = html.replaceAll("R0.61–R0.71S", "R0.61–R0.71T");
html = html.replaceAll("/recap-r0-61-r0-71s.pdf", "/recap-r0-61-r0-71t.pdf");
html = html.replaceAll("/i18n-en.js?v=1.04", "/i18n-en.js?v=1.05");
html = html.replaceAll("R0.61 到 R0.71S 的 83 个研究节点", "R0.61 到 R0.71T 的 84 个研究节点");
replaceOne(
  "十二个阶段、83 个节点：从约化递推到 conditional incidence，再到 directional packets、critical Bessel tax 与只覆盖 NSE initial observation boundary 的 scaling no-go。",
  "十二个阶段、84 个节点：从约化递推到 conditional incidence，再到 genuine positive-time internal entry、internal scaling no-go 与 outgoing occupation boundary。",
  "og description",
);
replaceOne("收录节点：83", "收录节点：84", "stamp nodes");
replaceOne("回顾截止时公开笔记：143", "回顾截止时公开笔记：144", "stamp notes");
replaceOne("回顾截止节点：R0.71S", "回顾截止节点：R0.71T", "stamp latest");
replaceOne("02 · 83 节完整索引", "02 · 84 节完整索引", "toc nodes");
replaceOne("<div class=\"metric\"><strong>83</strong><span>R0.61–R0.71T 研究节点</span></div>", "<div class=\"metric\"><strong>84</strong><span>R0.61–R0.71T 研究节点</span></div>", "metric nodes");
replaceOne("<div class=\"metric\"><strong>45</strong><span>R0.70A–R0.71S 完成版本</span></div>", "<div class=\"metric\"><strong>46</strong><span>R0.70A–R0.71T 完成版本</span></div>", "metric releases");
replaceOne("后面的 83 个节点沿着这个缺口推进", "后面的 84 个节点沿着这个缺口推进", "scope nodes");

replaceBlock(
  '            <article class="phase"><h3>R0.71G–R0.71S',
  "</article>",
  String.raw`            <article class="phase"><h3>R0.71G–R0.71T · temporal packing、internal entry 与 scale-matched occupation</h3><p>R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出 finite conditional Jensen 与 incidence theorems。R0.71S 保留 entry direction 后证明 critical packet 单包即带 \(\kappa_j^2\) Bessel 税，并用 genuine NSE initial face 排除 observation-boundary 版本的 bare payment。R0.71T 进一步用正向局部 NSE 流映射和有限维 IFT 构造预定正时间的 full-shell zero：event forcing 非零，所以它是 genuine smooth internal simple positive entry。选择 \(a_\lambda=\lambda^{-2}\) 再作协变 scaling 后，entry atom 为 \(\lambda^{-4}\)、bare normalized Leray-Lamb time budget 为 \(\lambda^{-6}\)，比值按 \(\lambda^2\) 发散；初始 energy 与 critical norm 趋零，enstrophy 有界。outgoing coarea 对所有 finite-order entries 给出 even-touch-safe 的 exact scale-zero representation，但其零层集中尚无 Leray payment。finite trace-variation theorem 则保留 strong Lamb、\(F_t\)、\(Y_t\) 与 repeated-direction Bessel ledgers。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/notes/r0-71r.html">R0.71R</a><a href="/notes/r0-71s.html">R0.71S</a><a href="/notes/r0-71t.html">R0.71T</a><a href="/figures/r0-71s-signed-packet.pdf">R0.71S 附图</a><a href="/figures/r0-71t-internal-entry.pdf">R0.71T 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071t">R0.71T 证书</a></div></article>`,
  "last phase",
);

replaceOne("R0.61–R0.71T 的 83 节公开笔记", "R0.61–R0.71T 的 84 节公开笔记", "index heading");
replaceOne(
  '            <a href="/notes/r0-71s.html">R0.71S</a>\n          </div>',
  '            <a href="/notes/r0-71s.html">R0.71S</a>\n            <a href="/notes/r0-71t.html">R0.71T</a>\n          </div>',
  "index latest",
);
replaceOne(
  "            <li>finite conditional directional-packet payment、critical Bessel diagonal 与 repeated-packet lower bounds、necessary directional Carleson condition、backward-heat kernel 和 bounded bilinear constant-mode dichotomy；genuine NSE scaling no-go 只覆盖 initial observation-boundary entry，不覆盖 internal entries。</li>",
  "            <li>finite conditional directional-packet payment、critical Bessel diagonal 与 repeated-packet lower bounds、necessary directional Carleson condition、backward-heat kernel 和 bounded bilinear constant-mode dichotomy；R0.71S 的 genuine NSE scaling no-go 只覆盖 initial observation-boundary entry。</li>\n            <li>R0.71T 的 finite-dimensional IFT positive-time internal-entry construction、global positive entry simplicity、induced local positive cell、bounded-energy/enstrophy internal scaling no-go、finite outgoing-coarea identity，以及带完整 \\(F_t\\)、\\(Y_t\\) 账本的 conditional trace-variation theorem。</li>",
  "retained latest",
);

replaceBlock(
  '        <section id="value">',
  "        </section>",
  String.raw`        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>内部事件已经存在，真正缺口转为 scale-zero charge 的总量控制</h2>
          <p>截至 R0.71T，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 84 个节点解释成对千禧年问题完成了某个比例。</p>
          <p>R0.71T 的实质进展是关闭 R0.71S 留下的 initial-boundary caveat：smooth positive-time internal entry 可以由 exact forward NSE flow 构造，且 bare normalized \(\dot H^{-1}\)-Lamb time integral 对它仍少两阶。这个 no-go 沿 energy 与 critical norm 趋零、enstrophy 有界的解族成立，因此不是高能数据假象。</p>
          <p>正面结构是 global-shell positive entries 自动 simple，full-shell root 至少诱导一个 positive local cell，outgoing coarea 精确保留 odd crossing 与 even touch。尚缺的是该 scale-zero occupation/jet charge 的 summed NSE estimate；finite trace-variation theorem 所需 strong Lamb、\(F_t\)、\(Y_t\) 与 multiplicity 仍未由 Leray inequality 关闭。</p>
        </section>`,
  "value section",
);

replaceBlock(
  '        <section id="next">',
  "        </section>",
  String.raw`        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71U 检查 global-shell jet 与 outgoing occupation packing</h2>
          <p>下一有限任务研究 simple global entries 的 \(q_\beta^{\rm jet}=\kappa_j^{-6}\|C_t(t_\beta)\|_2^2/Y(t_\beta)\)。它在单半径 full-shell root 上与 entry atom 精确同阶，也与 outgoing occupation representation 相容。</p>
          <p>目标是证明一个 summed/Carleson estimate，或构造 recurrence family 排除该估计。并行保留 fixed-packet amplitude-thresholded excursion：它已有真实 Leray-paid variation bound，但改变了 raw zero-entry target。R0.71U 仍不宣称继续性、奇性排除或全局正则性。</p>
        </section>`,
  "next section",
);

replaceOne(
  '<a href="/notes/r0-71s.html">打开最新节点 R0.71S</a>',
  '<a href="/notes/r0-71t.html">打开最新节点 R0.71T</a>',
  "latest note link",
);

if (/我们/.test(html)) throw new Error("R0.71T recap must use singular or neutral voice");
if ((html.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length < 84) {
  throw new Error("R0.71T recap lost public-note links");
}
for (const token of ["收录节点：84", "R0.70A–R0.71T 完成版本", "outgoing coarea", "R0.71U"]) {
  if (!html.includes(token)) throw new Error("missing recap token: " + token);
}

await writeFile(outputPath, html);
console.log(JSON.stringify({ status: "ok", recap: outputPath, nodes: 84, next: "R0.71U" }, null, 2));
