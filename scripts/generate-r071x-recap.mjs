import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71w.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71x.html");
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

html = html.replaceAll("R0.61–R0.71W", "R0.61–R0.71X");
html = html.replaceAll("R0.61 到 R0.71W", "R0.61 到 R0.71X");
html = html.replaceAll("/recap-r0-61-r0-71w.pdf", "/recap-r0-61-r0-71x.pdf");
html = html.replaceAll("/i18n-en.js?v=1.09", "/i18n-en.js?v=1.10");

replaceOne(
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71X 的 87 个研究节点，记录从约化递推、projected-Lamb 热体积和 temporal packing，到 Leray-paid excursion、fixed-zero boundary 与 data-uniform complete first-row no-go 的完整路线。",
  "R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71X 的 88 个研究节点；最新一节在固定小耦合 triangular family 内完成指定实根并精确饱和 D 的三分之一次方端点，同时保留一般问题与增长维数边界。",
  "meta description",
);
replaceOne(
  "十七个阶段、87 个节点：从约化递推到 conditional incidence、second-time jet、Leray-paid excursion，再到 amplitude-doped exact 2.5D data-uniform complete first-row no-go；初始数据依赖仍开放。",
  "十七个阶段、88 个节点：从约化递推到 fixed-zero ledger，再到固定小耦合 triangular family 内 D 的三分之一次方端点饱和；增长维数与一般正则性仍开放。",
  "og description",
);
replaceOne("R0.61 到 R0.71X 的 87 个研究节点", "R0.61 到 R0.71X 的 88 个研究节点", "lead nodes");
replaceOne("收录节点：87", "收录节点：88", "stamp nodes");
replaceOne("回顾截止时公开笔记：147", "回顾截止时公开笔记：148", "stamp notes");
replaceOne("回顾截止节点：R0.71W", "回顾截止节点：R0.71X", "stamp latest");
replaceOne("02 · 87 节完整索引", "02 · 88 节完整索引", "toc nodes");
replaceOne(
  '<div class="metric"><strong>87</strong><span>R0.61–R0.71X 研究节点</span></div>',
  '<div class="metric"><strong>88</strong><span>R0.61–R0.71X 研究节点</span></div>',
  "metric nodes",
);
replaceOne(
  '<div class="metric"><strong>49</strong><span>R0.70A–R0.71W 完成版本</span></div>',
  '<div class="metric"><strong>50</strong><span>R0.70A–R0.71X 完成版本</span></div>',
  "metric releases",
);
replaceOne("后面的 87 个节点沿着这个缺口推进", "后面的 88 个节点沿着这个缺口推进", "scope nodes");

replaceBlock(
  '            <article class="phase"><h3>R0.71U–R0.71W',
  "</article>",
  String.raw`            <article class="phase"><h3>R0.71U–R0.71X · second-time jet、complete first row 与三分之一次方边界</h3>
              <p>R0.71U 给出 zero-count-independent all-shell second-time-jet theorem 与 finite prescribed recurrence。R0.71V 把第一行账本转成 Leray–Hopf right-rooted excursion-height packing，并分离 level integral 与 fixed zero-level atom。R0.71W 用 amplitude doping 排除带固定 \(\nu^2\) baseline 和 complete projected rotational charge 的 data-uniform first-row bound，但留下 \(D^{1/3}\) 端点。R0.71X 固定充分小的 \(\delta\)，在 uniform IFT 邻域内取 \(A=\delta q^2\)：ECT 零点计数、compact \(C^1\) 分离和半直线 integrating factor 合在一起，证明实时间 target roots 只有声明的两个 simple roots。该族满足 \(D\asymp\delta^2q^6\)、complete \(\mathcal J\asymp\delta^2q^2\) 与 \(\nu^2\le\Lambda_1\le C(\nu^2+\delta^2)\)，因而 \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\)。fixed-\(\delta\) 下，\(\beta&lt;1/3\) 发散、\(\beta=1/3\) 饱和、\(\beta&gt;1/3\) 衰减。</p>
              <div class="links"><a href="/notes/r0-71u.html">R0.71U</a><a href="/notes/r0-71v.html">R0.71V</a><a href="/notes/r0-71w.html">R0.71W</a><a href="/notes/r0-71x.html">R0.71X</a><a href="/figures/r0-71u-recurrence-packing.pdf">R0.71U 附图</a><a href="/figures/r0-71v-zero-level-boundary.pdf">R0.71V 附图</a><a href="/figures/r0-71w-amplitude-doping.pdf">R0.71W 附图</a><a href="/figures/r0-71x-endpoint-saturation.pdf">R0.71X 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071x">R0.71X 证书</a></div></article>`,
  "last phase",
);

replaceOne("R0.61–R0.71X 的 87 节公开笔记", "R0.61–R0.71X 的 88 节公开笔记", "index heading");
replaceOne(
  '            <a href="/notes/r0-71w.html">R0.71W</a>\n          </div>',
  '            <a href="/notes/r0-71w.html">R0.71W</a>\n            <a href="/notes/r0-71x.html">R0.71X</a>\n          </div>',
  "index latest",
);
replaceOne(
  "            <li>R0.71W 的 amplitude-doped exact triangular 2.5D sequence、uniform rescaled Fourier-lattice IFT、指定的 \\(m=2\\) exact simple root、\\(Y_q\\asymp\\mathscr A_q^2q^2\\)、full-frequency projected rotational charge bound 与 data-uniform complete first-row no-go。初始 data size 无界；只排除 \\(D^\\beta\\)、\\(\\beta&lt;1/3\\)，不排除 \\(D^{1/3}\\) 或更强数据依赖。</li>",
  "            <li>R0.71W 的 amplitude-doped exact triangular 2.5D sequence、uniform rescaled Fourier-lattice IFT、指定的 \\(m=2\\) exact simple root、\\(Y_q\\asymp\\mathscr A_q^2q^2\\)、full-frequency projected rotational charge bound 与 data-uniform complete first-row no-go。初始 data size 无界；只排除 \\(D^\\beta\\)、\\(\\beta&lt;1/3\\)，不排除 \\(D^{1/3}\\) 或更强数据依赖。</li>\n            <li>R0.71X 在固定充分小 \\(\\delta\\) 与 \\(A=\\delta q^2\\) 的 uniform IFT 邻域内，用 ECT、compact \\(C^1\\) 分离与半直线 integrating factor 完成全部实时间 target-root 账本；并证明 \\(D\\asymp\\delta^2q^6\\)、complete \\(\\mathcal J\\asymp\\delta^2q^2\\)、\\(\\nu^2\\le\\Lambda_1\\le C(\\nu^2+\\delta^2)\\) 和 \\(\\mathcal J/(D^{1/3}\\Lambda_1)\\asymp\\delta^{4/3}\\)。这是声明的固定维 triangular family 内部饱和，不是 universal endpoint 或正则性定理。</li>",
  "retained latest",
);

replaceBlock(
  '        <section id="value">',
  "        </section>",
  String.raw`        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>声明的 triangular family 已到三分之一次方内部边界</h2>
          <p>截至 R0.71X，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 88 个节点解释成对千禧年问题完成了某个比例。</p>
          <p>R0.71W 排除 data-uniform complete first-row bound。R0.71X 在固定充分小 \(\delta\) 的 uniform IFT 邻域内补齐全部实时间 roots，并把完整 atom、data size 与第一行 payment 放到同一尺度，得到 \(D^{1/3}\) 的非零有限比值。这里的结论是 fixed-dimensional declared triangular family internal saturation，不是一般初值类的 universal endpoint。</p>
          <p>多块推广中，energy proxy \(\varepsilon_N=P\sqrt{K_{v,N}}/q^2\) 不等于精确 operator IFT parameter \(\delta_{\mathrm{op},N}=(P/q^2)\sup_x\lVert V_{z,N}(x)\rVert\)。growing \(N\) 与 strong coupling 都仍开放；数值图中的 atomProxy 也不是 multiplier-locked \(J_*\)，\(\delta=1/128\) 没有被量化为 continuum IFT 半径。</p>
        </section>`,
  "value section",
);

replaceBlock(
  '        <section id="next">',
  "        </section>",
  String.raw`        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71Y 量化 growing-dimensional ECT/IFT 与 weighted observability gate</h2>
          <p>下一有限任务把 ECT root separation、uniform IFT radius 和 operator norm 随 block number 的增长写成可核对常数；同时建立 weighted slope-energy / observability gate，判断 complete atom sum 能否被同尺度数据量支付。</p>
          <p>strong-coupling Bessel 路线保留为后续候选，不在 R0.71Y 中混入。正面估计必须明确 growing-dimensional 常数；负面结论也必须保留 exact operator parameter 与 complete atom 口径。</p>
        </section>`,
  "next section",
);

replaceOne(
  '<a href="/notes/r0-71w.html">打开最新节点 R0.71W</a>',
  '<a href="/notes/r0-71x.html">打开最新节点 R0.71X</a>',
  "latest note link",
);
if (/我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/.test(html)) {
  throw new Error("R0.71X recap must use singular or neutral voice");
}
if ((html.match(/<article class="phase">/g) ?? []).length !== 17) {
  throw new Error("R0.71X recap must retain exactly 17 phases");
}
const index = html.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
if ((index.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length !== 88) {
  throw new Error("R0.71X recap node index must contain exactly 88 notes");
}
for (const token of [
  "收录节点：88",
  "回顾截止时公开笔记：148",
  "R0.70A–R0.71X 完成版本",
  "R0.71U–R0.71X",
  "D^{1/3}",
  "\\delta^{4/3}",
  "energy proxy",
  "delta_{\\mathrm{op},N}",
  "R0.71Y",
]) {
  if (!html.includes(token)) throw new Error("missing recap token: " + token);
}

await writeFile(outputPath, html);
console.log(
  JSON.stringify(
    { status: "ok", recap: outputPath, nodes: 88, phases: 17, next: "R0.71Y" },
    null,
    2,
  ),
);
