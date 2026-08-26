import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(value, label) {
  return {
    value,
    replace(before, after) {
      const count = this.value.split(before).length - 1;
      if (this.value.includes(after)) {
        if (count === 0 || after.includes(before)) return;
        throw new Error(label + ": old and new replacement tokens both present");
      }
      if (count !== 1) throw new Error(label + ": expected one match, found " + count);
      this.value = this.value.replace(before, after);
    },
    replaceAll(before, after) {
      const count = this.value.split(before).length - 1;
      if (count === 0 && this.value.includes(after)) return;
      if (count < 1) throw new Error(label + ": missing replacement token");
      this.value = this.value.replaceAll(before, after);
    },
    replaceBlock(start, end, replacement) {
      const startIndex = this.value.indexOf(start);
      if (startIndex < 0) throw new Error(label + ": start marker missing");
      const endIndex = this.value.indexOf(end, startIndex);
      if (endIndex < 0) throw new Error(label + ": end marker missing");
      this.value = this.value.slice(0, startIndex) + replacement + this.value.slice(endIndex + end.length);
    },
    count(token) {
      return this.value.split(token).length - 1;
    },
  };
}

const releaseCard = String.raw`

          <div class="task-one" id="r071x" data-release="r071x" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71X · 2026-08-26</p>
            <h3>固定小耦合在声明的 triangular family 内达到三分之一次方端点</h3>
            <p>
              固定充分小的 \(0&lt;\delta\le\delta_*\)，并取 \(\mathscr A_{q,\delta}=\delta q^2\)。uniform IFT 分支保留。ECT 零点预算、compact \(C^1\) 分离和半直线 integrating factor 共同证明：声明区间中的 positive target roots 恰好是预设的 \(N\) 个 simple roots。
            </p>
            <p>
              完整尺度为
              \[
                D_{q,\delta}\asymp\delta^2q^6,\qquad
                \mathcal J_{q,\delta}\asymp\delta^2q^2,\qquad
                \nu^2\le\Lambda_1\le C(\nu^2+\delta^2),
              \]
              因而 \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\)。fixed-\(\delta\) 下，\(\beta&lt;1/3\) 发散、\(\beta=1/3\) 饱和、\(\beta&gt;1/3\) 衰减。
            </p>
            <p><strong>结论边界：</strong>&nbsp;这是 fixed-dimensional declared triangular family internal saturation，不是 universal endpoint、bounded-data continuation、有限时奇性或 global regularity 结论。多块 energy proxy 不等于 exact operator IFT parameter；growing \(N\) 与 strong coupling 仍开放。</p>
            <p>
              <a href="/notes/r0-71x.html"><strong>阅读 R0.71X 研究笔记 →</strong></a><br>
              <a href="/notes/r0-71x.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-71x-endpoint-saturation.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071x">查看三组证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071x_independent_audit.md">查看独立审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation">查看附图、数据、进度与源代码包</a> ·
              <a href="/recap-r0-61-r0-71x.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71x.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71Y：</strong>&nbsp;量化 growing-dimensional ECT / IFT，并检查 weighted slope-energy / observability gate。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
homeEdit.replace("<strong>v1.09</strong>网页版本", "<strong>v1.10</strong>网页版本");
homeEdit.replace("<strong>147</strong>公开研究笔记", "<strong>148</strong>公开研究笔记");
homeEdit.replace("<strong>R0.71W</strong>最新研究节点", "<strong>R0.71X</strong>最新研究节点");
homeEdit.replace(
  "<strong>data-dependent payment / one-third boundary</strong>当前方向",
  "<strong>growing-dimensional ECT / weighted observability</strong>当前方向",
);
homeEdit.replace(
  '<div class="summary-item"><strong>我目前关注</strong><span>比较 amplitude-doped fixed-zero atom 与 data-dependent energy/enstrophy charge，检查 \\(D^{1/3}\\) 端点是否可以支付。</span></div>',
  '<div class="summary-item"><strong>我目前关注</strong><span>量化 growing-dimensional ECT / IFT 常数，并检查 weighted slope-energy 与 complete atom observability 能否同尺度闭合。</span></div>',
);
homeEdit.replace("Research topology · R0.1–R0.71W", "Research topology · R0.1–R0.71X");
homeEdit.replace('<a href="#r070a">R0.70A–R0.71W 完成版本</a>', '<a href="#r070a">R0.70A–R0.71X 完成版本</a>');
homeEdit.replaceAll("/recap-r0-61-r0-71w.html", "/recap-r0-61-r0-71x.html");
homeEdit.replaceAll("/recap-r0-61-r0-71w.pdf", "/recap-r0-61-r0-71x.pdf");
homeEdit.replace('<span class="route-range">R0.69P–R0.71W</span>', '<span class="route-range">R0.69P–R0.71X</span>');
homeEdit.replace(
  "<h3>从有符号环带障碍走到 complete first-row data-uniform no-go</h3>",
  "<h3>从 complete first-row no-go 走到族内三分之一次方端点</h3>",
);
homeEdit.replace(
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–T 建立 projected-Lamb 热体积、局部化与 temporal packing 边界。R0.71U–V 分开 second-time jet、Leray-paid excursion 和 fixed zero-level trace。R0.71W 的 amplitude-doped exact triangular 2.5D sequence 保留完整 \\(\\nu^2\\) baseline、enstrophy ratio 与 projected rotational charge 后，仍排除 data-independent complete first-row ledger；初始数据依赖仍开放。</p>",
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71U–V 分开 second-time jet、Leray-paid excursion 和 fixed zero-level trace。R0.71W 排除 data-independent complete first-row ledger。R0.71X 再固定充分小 \\(\\delta\\)，补齐全部实时间 target roots，并证明 complete atom sum 在声明的 exact triangular family 内饱和 \\(D^{1/3}\\Lambda_1\\)；一般端点、growing dimension 与 strong coupling 仍开放。</p>",
);
homeEdit.replace(
  "→ amplitude-doped complete first-row data-uniform no-go</p>",
  "→ amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation</p>",
);
homeEdit.replace("<summary>展开 57 篇公开笔记</summary>", "<summary>展开 58 篇公开笔记</summary>");
homeEdit.replace('aria-label="R0.69P–R0.71W"', 'aria-label="R0.69P–R0.71X"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71w.html">R0.71W</a>\n',
  '                  <a class="milestone" href="/notes/r0-71w.html">R0.71W</a>\n                  <a class="milestone" href="/notes/r0-71x.html">R0.71X</a>\n',
);
homeEdit.replaceBlock(
  '            <article class="tree-node next">',
  "            </article>",
  String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71Y</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>quantitative growing-dimensional ECT / IFT</h3>
              <p>量化 root separation、operator IFT radius 与 weighted slope-energy / observability；strong-coupling Bessel 留作后续候选。</p>
            </article>`,
);
homeEdit.replace(
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71W 路线放在同一张图中。",
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71X 路线放在同一张图中。",
);
homeEdit.replace("累计回顾 R0.61–R0.71W · 2026-08-26", "累计回顾 R0.61–R0.71X · 2026-08-26");
homeEdit.replace(
  "R0.60 recap 之后的累计回顾收录 87 个节点；全站现有 147 篇公开研究笔记",
  "R0.60 recap 之后的累计回顾收录 88 个节点；全站现有 148 篇公开研究笔记",
);
homeEdit.replace(
  "R0.60 之后的路线分成十七段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet、finite recurrence、Leray-paid excursion、fixed-zero boundary 与 complete first-row data-uniform no-go。R0.70A–R0.71W 共 49 个完成版本。",
  "R0.60 之后的路线分成十七段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet、finite recurrence、Leray-paid excursion、fixed-zero boundary、complete first-row data-uniform no-go 与 fixed-small-coupling one-third internal saturation。R0.70A–R0.71X 共 50 个完成版本。",
);
homeEdit.replace(
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71W 排除 data-independent complete first-row ledger；指定的 \\(m=2\\) atom 发散，enstrophy ratio 有界，normalized full rotational charge 消失。初始 energy/enstrophy 无界，因此 \\(D^{1/3}\\) 与一般 data-dependent estimate 仍开放。</p>",
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71X 在固定充分小 \\(\\delta\\) 的 uniform IFT branch 内证明 complete roots，并得到 \\(D\\asymp\\delta^2q^6\\)、complete \\(\\mathcal J\\asymp\\delta^2q^2\\) 与 \\(\\mathcal J/(D^{1/3}\\Lambda_1)\\asymp\\delta^{4/3}\\)。这只是声明的 fixed-dimensional triangular family 内部饱和。</p>",
);
homeEdit.replace(
  String.raw`<p><strong style="color:var(--gold)">下一步 R0.71X：</strong>&nbsp;检查 \(D^{1/3}\) 端点与 scale-compatible energy/enstrophy charge。</p>
          </div>
        </section>`,
  String.raw`<p><strong style="color:var(--gold)">R0.71X 已完成：</strong>&nbsp;固定充分小 coupling、complete root set 与 \(D^{1/3}\Lambda_1\) 的 declared-family internal saturation 已闭合。</p>
          </div>` + releaseCard + String.raw`
        </section>`,
);
homeEdit.replace("        综述 v1.09 · 2026-08-26<br>", "        综述 v1.10 · 2026-08-26<br>");
homeEdit.replace("        上次综述 v1.08 · 2026-08-26<br>", "        上次综述 v1.09 · 2026-08-26<br>");
homeEdit.replaceAll("/i18n-en.js?v=1.09", "/i18n-en.js?v=1.10");

if (homeEdit.count('data-release="r071x"') !== 1) throw new Error("home: R0.71X card count");
if (homeEdit.count('href="/notes/r0-71x.html"') !== 2) throw new Error("home: R0.71X note links");
if (homeEdit.count("<summary>展开 58 篇公开笔记</summary>") !== 1) throw new Error("home: route count");
if (/我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/.test(homeEdit.value)) {
  throw new Error("home must use singular or neutral voice");
}

const literaturePath = resolve(root, "public/literature-review.html");
const literatureEdit = editor(await readFile(literaturePath, "utf8"), "literature");
literatureEdit.replaceAll("/i18n-en.js?v=1.09", "/i18n-en.js?v=1.10");
literatureEdit.replaceAll("/recap-r0-61-r0-71w.html", "/recap-r0-61-r0-71x.html");
literatureEdit.replaceAll("R0.69P–R0.71W", "R0.69P–R0.71X");
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71x.html">累计回顾与 87 节索引</a>',
  '<a href="/recap-r0-61-r0-71x.html">累计回顾与 88 节索引</a>',
);
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71x.html#node-index">打开 87 节完整索引</a>',
  '<a href="/recap-r0-61-r0-71x.html#node-index">打开 88 节完整索引</a>',
);
literatureEdit.replace(
  "R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V 分离 Leray-paid excursion 与 fixed zero-level trace。R0.71W 的 amplitude-doped exact 2.5D sequence 进一步排除 data-independent complete first-row ledger；初始数据依赖仍开放。保留下来的结果都不是全局正则性结论。",
  "R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V–W 分离 fixed zero-level trace 并排除 data-uniform complete first-row ledger。R0.71X 在固定充分小 coupling 下补齐 complete roots，得到 declared triangular family 内的 one-third saturation。growing dimension 与一般正则性仍开放。",
);
literatureEdit.replace(
  String.raw`              <div class="route-step kept"><header><b>R0.71W</b><strong>data-uniform complete first-row ledger 失败</strong></header><p>amplitude-doped exact triangular 2.5D sequence 满足 \(J_{*,2,q}\to\infty\)、\(\mathcal R_Y=O(1)\)，且 normalized full projected rotational charge 趋零。初始 data size 无界。<a href="/notes/r0-71w.html">研究笔记</a> <a href="/recap-r0-61-r0-71x.html">当前累计回顾</a> <a href="#r071w-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71X</b><strong>data-dependent one-third boundary</strong></header><p>比较 exact atom scaling 与 \(D^{1/3}\) 或更强的 scale-compatible payment。</p></div>`,
  String.raw`              <div class="route-step kept"><header><b>R0.71W</b><strong>data-uniform complete first-row ledger 失败</strong></header><p>amplitude-doped exact triangular 2.5D sequence 满足 \(J_{*,2,q}\to\infty\)、\(\mathcal R_Y=O(1)\)，且 normalized full projected rotational charge 趋零。初始 data size 无界。<a href="/notes/r0-71w.html">研究笔记</a></p></div>
              <div class="route-step kept"><header><b>R0.71X</b><strong>fixed-small-coupling one-third internal saturation</strong></header><p>uniform IFT 内取 \(A=\delta q^2\)。ECT、compact \(C^1\) 与 half-line integrating factor 给 complete roots；\(D\asymp\delta^2q^6\)、complete \(\mathcal J\asymp\delta^2q^2\)、\(\nu^2\le\Lambda_1\le C(\nu^2+\delta^2)\)。<a href="/notes/r0-71x.html">研究笔记</a> <a href="/recap-r0-61-r0-71x.html">当前累计回顾</a> <a href="#r071x-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71Y</b><strong>quantitative growing-dimensional gate</strong></header><p>量化 ECT / IFT 常数与 weighted slope-energy / observability；strong-coupling Bessel 保留为后续候选。</p></div>`,
);
literatureEdit.replace(
  '<h3 id="r071w-boundary">R0.71W 关闭了什么，R0.71X 只检查什么</h3>',
  '<h3 id="r071x-boundary">R0.71X 关闭了什么，R0.71Y 只检查什么</h3>',
);
literatureEdit.replace(
  String.raw`<p>R0.71W 保留固定 target、固定宏观窗口、enstrophy ratio、\(\nu^2\) baseline 与 complete projected rotational charge。amplitude-doped exact triangular 2.5D sequence 仍使指定的 \(m=2\) atom 相对 complete first-row ledger 发散，因此该 data-uniform estimate 失败。构造的初始 energy/enstrophy 无界；它只排除 \(D^\beta\)、\(\beta&lt;1/3\)，不排除 \(D^{1/3}\)、更强数据依赖或 structurally different payment。R0.71X 只检查 data-dependent one-third boundary。我继续用下面六条筛选。</p>`,
  String.raw`<p>R0.71X 固定充分小的 \(\delta\)，在 R0.71W 的 uniform IFT 邻域内取 \(A=\delta q^2\)。ECT multiplicity bound、compact \(C^1\) separation 与 half-line integrating factor 给 complete real-time target roots；exact scales 给 \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\)。这是 fixed-dimensional declared triangular family internal saturation，不是 universal endpoint 或正则性定理。多块 energy proxy \(\varepsilon_N\) 不等于 exact \(\delta_{\mathrm{op},N}\)。R0.71Y 只量化 growing-dimensional ECT / IFT 与 weighted observability gate。下面六条筛选保持不变。</p>`,
);
literatureEdit.replace(
  String.raw`<div class="boundary"><strong>R0.71W 的一手文献边界</strong><p><a href="https://doi.org/10.1007/BF02547354">Leray</a>与 <a href="https://doi.org/10.1137/1.9781611970050">Temam</a>支持 weak-energy 与 semigroup framework；<a href="https://doi.org/10.1063/1.4990082">Biferale–Buzzicotti–Linkmann</a>记录 exact 2D3C reduction；<a href="https://link.springer.com/book/10.1007/978-1-4612-0915-5">Karlin–Studden</a>给 Chebyshev-system interpolation background。uniform rescaled IFT 与 complete rotational estimate 在本节直接证明。bounded audit 未定位到 data-uniform fixed-zero complete first-row theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
  String.raw`<div class="boundary"><strong>R0.71X 的一手文献边界</strong><p><a href="https://doi.org/10.1088/1361-6544/ab9246">Miller</a>给 whole-space cubic enstrophy ODE 与 small-data threshold；<a href="https://doi.org/10.1512/iumj.2008.57.3716">Lu–Doering</a>、<a href="https://doi.org/10.1017/jfm.2017.136">Ayala–Protas</a>和<a href="https://doi.org/10.1017/jfm.2020.204">Kang–Yun–Protas</a>研究极端 enstrophy growth；<a href="https://doi.org/10.4208/cmr.2021-0106">Lerner–Vigneron</a>给 projected-Lamb identities；<a href="https://doi.org/10.1080/03605308108820180">Foias–Guillopé–Temam</a>的三分之一次方指数属于高阶空间导数时间可积性。<a href="https://doi.org/10.1007/BF02096982">Constantin</a>与<a href="https://doi.org/10.1016/j.jde.2025.113486">Yang</a>处理空间 level / trace，<a href="https://doi.org/10.1016/j.jmaa.2022.126428">Wang–Gao–Xue</a>处理 time analyticity。限定的一手来源检索没有找到直接重合的 fixed temporal zero-slope complete atom theorem；这是 bounded non-collision，不作原创性、优先权或不存在性声明。</p></div>`,
);
literatureEdit.replace("文献综述 v1.09 · 2026-08-26", "文献综述 v1.10 · 2026-08-26");

if (literatureEdit.count("<b>R0.71X</b>") !== 1) throw new Error("literature: R0.71X node");
if (literatureEdit.count("开放接口 · R0.71Y") !== 1) throw new Error("literature: R0.71Y interface");
for (const release of "abcdefghijklmnopqrstuvwxyz".split("")) {
  const slug = "/notes/r0-70" + release + ".html";
  if (!literatureEdit.value.includes(slug)) throw new Error("literature: missing direct link " + slug);
}
for (const release of "abcdefghijklmnopqrstuvwx".split("")) {
  const slug = "/notes/r0-71" + release + ".html";
  if (!literatureEdit.value.includes(slug)) throw new Error("literature: missing direct link " + slug);
}
if (/我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/.test(literatureEdit.value)) {
  throw new Error("literature must use singular or neutral voice");
}

await Promise.all([
  writeFile(homePath, homeEdit.value),
  writeFile(literaturePath, literatureEdit.value),
]);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71X",
      siteVersion: "v1.10",
      publicNotes: 148,
      currentRouteNotes: 58,
      recapNodes: 88,
      completedReleasesR070AToR071X: 50,
      literatureDirectLinksR070AOnward: 50,
      next: "R0.71Y",
    },
    null,
    2,
  ),
);
