import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71v.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71w.html");
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

html = html.replaceAll("R0.61–R0.71V", "R0.61–R0.71W");
html = html.replaceAll("R0.61 到 R0.71V", "R0.61 到 R0.71W");
html = html.replaceAll("/recap-r0-61-r0-71v.pdf", "/recap-r0-61-r0-71w.pdf");
html = html.replaceAll("/i18n-en.js?v=1.08", "/i18n-en.js?v=1.09");

replaceOne(
  "    .phase h3{margin:.45rem 0 .55rem;font-size:1.15rem}.phase p{margin:.45rem 0}",
  "    .phase h3{margin:.45rem 0 .55rem;font-size:1.15rem}.phase p{margin:.45rem 0}\n    .print-page-break{display:none}",
  "print page-break sentinel",
);
replaceOne(
  "      .phase{break-inside:avoid;page-break-inside:avoid;margin-bottom:1rem;position:static;width:100%;overflow:visible;-webkit-box-decoration-break:clone;box-decoration-break:clone}",
  "      .timeline{display:block}\n      .phase{display:table;break-inside:avoid;page-break-inside:avoid;margin-bottom:1rem;position:static;width:100%;overflow:visible;-webkit-box-decoration-break:clone;box-decoration-break:clone}",
  "print timeline pagination",
);
replaceOne(
  "      .phase:nth-child(12){break-before:page;page-break-before:always}",
  "      .print-page-break{display:block;break-before:page;page-break-before:always;height:1px}",
  "print phase page boundaries",
);
replaceOne(
  '            <article class="phase"><h3>R0.71A–R0.71D',
  '            <div class="print-page-break" aria-hidden="true"></div>\n            <article class="phase"><h3>R0.71A–R0.71D',
  "print break before phase ten",
);
replaceOne(
  '            <article class="phase"><h3>R0.71G–R0.71I',
  '            <div class="print-page-break" aria-hidden="true"></div>\n            <article class="phase"><h3>R0.71G–R0.71I',
  "print break before phase twelve",
);
replaceOne(
  '            <article class="phase"><h3>R0.71S–R0.71T',
  '            <div class="print-page-break" aria-hidden="true"></div>\n            <article class="phase"><h3>R0.71S–R0.71T',
  "print break before phase sixteen",
);

replaceOne(
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71W 的 86 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem、second-time jet，再到 Leray-paid excursion 与固定零层边界的路线。",
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71W 的 87 个研究节点，记录从约化递推、projected-Lamb 热体积和 temporal packing，到 Leray-paid excursion、fixed-zero boundary 与 data-uniform complete first-row no-go 的完整路线。",
  "meta description",
);
replaceOne(
  "十七个阶段、86 个节点：从约化递推到 conditional incidence，再到 genuine internal entry、classical second-time-jet packing、Leray-paid excursion 与固定 target/window 的真实 NSE selected-singleton first-time-row obstruction；完整 ν² ledger 未排除。",
  "十七个阶段、87 个节点：从约化递推到 conditional incidence、second-time jet、Leray-paid excursion，再到 amplitude-doped exact 2.5D data-uniform complete first-row no-go；初始数据依赖仍开放。",
  "og description",
);
replaceOne("R0.61 到 R0.71W 的 86 个研究节点", "R0.61 到 R0.71W 的 87 个研究节点", "lead nodes");
replaceOne("收录节点：86", "收录节点：87", "stamp nodes");
replaceOne("回顾截止时公开笔记：146", "回顾截止时公开笔记：147", "stamp notes");
replaceOne("回顾截止节点：R0.71V", "回顾截止节点：R0.71W", "stamp latest");
replaceOne("02 · 86 节完整索引", "02 · 87 节完整索引", "toc nodes");
replaceOne(
  '<div class="metric"><strong>86</strong><span>R0.61–R0.71W 研究节点</span></div>',
  '<div class="metric"><strong>87</strong><span>R0.61–R0.71W 研究节点</span></div>',
  "metric nodes",
);
replaceOne(
  '<div class="metric"><strong>48</strong><span>R0.70A–R0.71V 完成版本</span></div>',
  '<div class="metric"><strong>49</strong><span>R0.70A–R0.71W 完成版本</span></div>',
  "metric releases",
);
replaceOne("后面的 86 个节点沿着这个缺口推进", "后面的 87 个节点沿着这个缺口推进", "scope nodes");

replaceBlock(
  '            <article class="phase"><h3>R0.71U–R0.71V',
  "</article>",
  String.raw`            <article class="phase"><h3>R0.71U–R0.71W · second-time jet、fixed-zero boundary 与 complete first-row no-go</h3>
              <p>R0.71U 给出 zero-count-independent all-shell second-time-jet theorem 与 finite prescribed recurrence。R0.71V 把第一行账本转成 Leray–Hopf right-rooted excursion-height packing，并分离 level integral 与 fixed zero-level atom。R0.71W 取 \(\mathscr A_q=q^\alpha\)、\(1&lt;\alpha&lt;2\)，用 uniform rescaled IFT 保持指定的 \(m=2\) simple root，并证明 \(J_{*,2,q}\asymp\mathscr A_q^2/q^2\to\infty\)、\(\mathcal R_Y=O(1)\)、normalized full projected rotational charge \(O(\mathscr A_q^2/q^4)\to0\)。因此带固定 \(\nu^2\) baseline 的 complete first-row ledger 也没有 data-independent bound。初始 data size \(D_q\asymp\mathscr A_q^2q^2\) 无界，所以 \(D^{1/3}\) 端点和一般 data-dependent estimate 仍开放。</p>
              <div class="links"><a href="/notes/r0-71u.html">R0.71U</a><a href="/notes/r0-71v.html">R0.71V</a><a href="/notes/r0-71w.html">R0.71W</a><a href="/figures/r0-71u-recurrence-packing.pdf">R0.71U 附图</a><a href="/figures/r0-71v-zero-level-boundary.pdf">R0.71V 附图</a><a href="/figures/r0-71w-amplitude-doping.pdf">R0.71W 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071w">R0.71W 证书</a></div></article>`,
  "last phase",
);

replaceOne("R0.61–R0.71W 的 86 节公开笔记", "R0.61–R0.71W 的 87 节公开笔记", "index heading");
replaceOne(
  '            <a href="/notes/r0-71v.html">R0.71V</a>\n          </div>',
  '            <a href="/notes/r0-71v.html">R0.71V</a>\n            <a href="/notes/r0-71w.html">R0.71W</a>\n          </div>',
  "index latest",
);
replaceOne(
  "            <li>R0.71V 的 Leray–Hopf compact-shell AC representatives、right-rooted scale-zero excursion-height packing、左端已正 component 的 initial-trace 例外、精确 excursion-to-atom 因子、weighted area hierarchy 与 sine method test；以及固定 target/window 下、相对所选 singleton target shell first-time-jet row 的 genuine unforced 2.5D sampling obstruction，其中第一个 prescribed root 已另行支付。完整 global \\(\\nu^2\\) baseline 与替代 dynamical charge 尚未排除。</li>",
  "            <li>R0.71V 的 Leray–Hopf compact-shell AC representatives、right-rooted scale-zero excursion-height packing、左端已正 component 的 initial-trace 例外、精确 excursion-to-atom 因子、weighted area hierarchy 与 sine method test；以及固定 target/window 下、相对所选 singleton target shell first-time-jet row 的 genuine unforced 2.5D sampling obstruction，其中第一个 prescribed root 已另行支付。完整 global \\(\\nu^2\\) baseline 与替代 dynamical charge 尚未排除。</li>\n            <li>R0.71W 的 amplitude-doped exact triangular 2.5D sequence、uniform rescaled Fourier-lattice IFT、指定的 \\(m=2\\) exact simple root、\\(Y_q\\asymp\\mathscr A_q^2q^2\\)、full-frequency projected rotational charge bound 与 data-uniform complete first-row no-go。初始 data size 无界；只排除 \\(D^\\beta\\)、\\(\\beta&lt;1/3\\)，不排除 \\(D^{1/3}\\) 或更强数据依赖。</li>",
  "retained latest",
);

replaceBlock(
  '        <section id="value">',
  "        </section>",
  String.raw`        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>完整第一行的 data-uniform 路线已经关闭，data-dependent payment 成为下一边界</h2>
          <p>截至 R0.71W，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 87 个节点解释成对千禧年问题完成了某个比例。</p>
          <p>R0.71U–V 先把 root atom、second-time tax、Leray-paid excursion 和 fixed zero-level trace 分开。R0.71W 再保留固定 \(\nu^2\) baseline、enstrophy ratio 与完整 projected rotational charge，仍得到指定的 \(m=2\) atom 对 complete first-row ledger 的发散。这是一条 data-uniform no-go，不是 selected-shell omission 或抽象 path test。</p>
          <p>边界同样明确：构造的初始 energy/enstrophy \(D_q\asymp q^{2\alpha+2}\) 无界。它排除所有固定 \(\beta&lt;1/3\) 的 \(D^\beta\) prefactor，但不排除 \(D^{1/3}\)、更强数据依赖、persistence condition、time-regularity charge 或不同 observable。</p>
        </section>`,
  "value section",
);

replaceBlock(
  '        <section id="next">',
  "        </section>",
  String.raw`        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71X 检查 \(D^{1/3}\) 端点与 scale-compatible charge</h2>
          <p>下一有限任务把 exact atom scaling 与 data-dependent energy/enstrophy payments 放在同一尺度比较，判断 \(1/3\) 是 triangular amplitude-doping family 的特征，还是更普遍的结构边界。</p>
          <p>正面估计必须明确 bounded-data class 或 data prefactor；负面结论也必须保留相同数据口径。R0.71X 仍不宣称继续性、奇性排除或全局正则性。</p>
        </section>`,
  "next section",
);

replaceOne(
  '<a href="/notes/r0-71v.html">打开最新节点 R0.71V</a>',
  '<a href="/notes/r0-71w.html">打开最新节点 R0.71W</a>',
  "latest note link",
);

if (/我们|攻关|主攻|三重审计|杀死错误想法|突破/.test(html)) {
  throw new Error("R0.71W recap must use singular or neutral voice");
}
if ((html.match(/<article class="phase">/g) ?? []).length !== 17) {
  throw new Error("R0.71W recap must retain exactly 17 phases");
}
const index = html.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
if ((index.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length !== 87) {
  throw new Error("R0.71W recap node index must contain exactly 87 notes");
}
for (const token of [
  "收录节点：87",
  "回顾截止时公开笔记：147",
  "R0.70A–R0.71W 完成版本",
  "R0.71U–R0.71W",
  "complete first-row",
  "\\beta&lt;1/3",
  "D^{1/3}",
  "R0.71X",
]) {
  if (!html.includes(token)) throw new Error("missing recap token: " + token);
}
if (html.includes("第二个正根")) throw new Error("ambiguous root description remains");

await writeFile(outputPath, html);
console.log(
  JSON.stringify(
    { status: "ok", recap: outputPath, nodes: 87, phases: 17, next: "R0.71X" },
    null,
    2,
  ),
);
