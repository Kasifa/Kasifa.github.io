import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(value, label) {
  return {
    value,
    replace(before, after) {
      const count = this.value.split(before).length - 1;
      if (count !== 1) throw new Error(label + ": expected one match, found " + count);
      this.value = this.value.replace(before, after);
    },
    replaceAll(before, after) {
      const count = this.value.split(before).length - 1;
      if (count < 1) throw new Error(label + ": missing replacement token");
      this.value = this.value.replaceAll(before, after);
    },
    replaceBlock(start, end, replacement) {
      const startIndex = this.value.indexOf(start);
      if (startIndex < 0) throw new Error(label + ": start marker missing");
      const endIndex = this.value.indexOf(end, startIndex);
      if (endIndex < 0) throw new Error(label + ": end marker missing");
      this.value =
        this.value.slice(0, startIndex) +
        replacement +
        this.value.slice(endIndex + end.length);
    },
    count(token) {
      return this.value.split(token).length - 1;
    },
  };
}

const releaseCard = String.raw`

          <div class="task-one" id="r071w" data-release="r071w" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71W · 2026-08-26</p>
            <h3>amplitude doping 排除 data-uniform complete first-row ledger</h3>
            <p>
              在 exact triangular 2.5D class 中取
              \[
                \mathscr A_q=q^\alpha,\qquad 1&lt;\alpha&lt;2,\qquad
                \delta_q=\mathscr A_q/q^2\to0.
              \]
              uniform rescaled IFT 保持固定 target、固定宏观时间窗与指定的 \(m=2\) simple root。filtered \(C_{*,t}\) 的 target coefficient 与 \(a_t\) 只相差固定非零 factors。
            </p>
            <p>
              full nonlinear estimates 给
              \[
                J_{*,2,q}\asymp\mathscr A_q^2/q^2\to\infty,\qquad
                \mathcal R_{Y_q}=O(1),\qquad
                \ell^{-1}\!\int_I\frac{\|\mathbb P(u_q\times\omega_q)\|_{\dot H^{-1}}^2}{Y_q}\,dt
                =O(\mathscr A_q^2/q^4)\to0.
              \]
              所以带固定 \(\nu^2\) baseline 的 complete first-row ledger 也没有 data-independent bound。
            </p>
            <p>
              初始 data size \(D_q\asymp\mathscr A_q^2q^2=q^{2\alpha+2}\) 无界。该族排除每个固定 \(\beta&lt;1/3\) 的 \(D^\beta\) prefactor，但不排除 \(D^{1/3}\)、更强数据依赖或不同 charge。
            </p>
            <p><strong>结论边界：</strong>&nbsp;这是 data-uniform route-pruning theorem，不是 bounded-data no-go、继续性、finite-time singularity 或 global regularity 结论；finite truncated-coset calculation 只作 corroboration。</p>
            <p>
              <a href="/notes/r0-71w.html"><strong>阅读 R0.71W 研究笔记 →</strong></a><br>
              <a href="/notes/r0-71w.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-71w-amplitude-doping.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071w">查看三组证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071w_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071w_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071w_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071w_independent_audit.md">查看独立审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071w-complete-ledger/fig-r071w-amplitude-doping">查看附图、数据、进度与源代码包</a> ·
              <a href="/recap-r0-61-r0-71w.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71w.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71X：</strong>&nbsp;检查 \(D^{1/3}\) 端点与 scale-compatible energy/enstrophy charge。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
homeEdit.replace("<strong>v1.08</strong>网页版本", "<strong>v1.09</strong>网页版本");
homeEdit.replace("<strong>146</strong>公开研究笔记", "<strong>147</strong>公开研究笔记");
homeEdit.replace("<strong>R0.71V</strong>最新研究节点", "<strong>R0.71W</strong>最新研究节点");
homeEdit.replace(
  "<strong>complete Leray ledger / zero-level boundary</strong>当前方向",
  "<strong>data-dependent payment / one-third boundary</strong>当前方向",
);
homeEdit.replace(
  '<div class="summary-item"><strong>我目前关注</strong><span>检查 fixed-target high-frequency events 相对完整 \\(\\nu^2\\) baseline 与 projected rotational term 是否仍非坍缩；fixed zero-level trace 不能直接从 level-integrated occupation 读取。</span></div>',
  '<div class="summary-item"><strong>我目前关注</strong><span>比较 amplitude-doped fixed-zero atom 与 data-dependent energy/enstrophy charge，检查 \\(D^{1/3}\\) 端点是否可以支付。</span></div>',
);
homeEdit.replace("Research topology · R0.1–R0.71V", "Research topology · R0.1–R0.71W");
homeEdit.replace(
  '<a href="#r070a">R0.70A–R0.71V 完成版本</a>',
  '<a href="#r070a">R0.70A–R0.71W 完成版本</a>',
);
homeEdit.replaceAll("/recap-r0-61-r0-71v.html", "/recap-r0-61-r0-71w.html");
homeEdit.replaceAll("/recap-r0-61-r0-71v.pdf", "/recap-r0-61-r0-71w.pdf");
homeEdit.replace('<span class="route-range">R0.69P–R0.71V</span>', '<span class="route-range">R0.69P–R0.71W</span>');
homeEdit.replace(
  "<h3>从有符号环带障碍走到 Leray-paid excursion 与固定零层边界</h3>",
  "<h3>从有符号环带障碍走到 complete first-row data-uniform no-go</h3>",
);
homeEdit.replace(
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–T 建立 projected-Lamb 热体积、局部化、temporal packing 与 genuine internal-entry no-go。R0.71U 给出 classical second-time-jet theorem 与 exact finite recurrence。R0.71V 证明 right-rooted compact-shell excursion-height packing 可由 Leray–Hopf 第一行支付，窗口左端已为正的 component 需要另付 initial trace；weighted area formula、sine test 与 fixed-target 2.5D NSE 序列同时表明 distinguished zero-level slope 仍需 noncollapse 或另一 dynamical charge。</p>",
  "<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–T 建立 projected-Lamb 热体积、局部化与 temporal packing 边界。R0.71U–V 分开 second-time jet、Leray-paid excursion 和 fixed zero-level trace。R0.71W 的 amplitude-doped exact triangular 2.5D sequence 保留完整 \\(\\nu^2\\) baseline、enstrophy ratio 与 projected rotational charge 后，仍排除 data-independent complete first-row ledger；初始数据依赖仍开放。</p>",
);
homeEdit.replace(
  "→ exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction</p>",
  "→ exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go</p>",
);
homeEdit.replace("<summary>展开 56 篇公开笔记</summary>", "<summary>展开 57 篇公开笔记</summary>");
homeEdit.replace('aria-label="R0.69P–R0.71V"', 'aria-label="R0.69P–R0.71W"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71v.html">R0.71V</a>\n',
  '                  <a class="milestone" href="/notes/r0-71v.html">R0.71V</a>\n                  <a class="milestone" href="/notes/r0-71w.html">R0.71W</a>\n',
);
homeEdit.replaceBlock(
  '            <article class="tree-node next">',
  "            </article>",
  String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71X</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>data-dependent one-third boundary</h3>
              <p>比较 exact atom scaling 与 \(D^{1/3}\) 或更强的 scale-compatible energy/enstrophy payment。</p>
            </article>`,
);
homeEdit.replace(
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71V 路线放在同一张图中。",
  "我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71W 路线放在同一张图中。",
);
homeEdit.replace("累计回顾 R0.61–R0.71V · 2026-08-26", "累计回顾 R0.61–R0.71W · 2026-08-26");
homeEdit.replace(
  "R0.60 recap 之后的累计回顾收录 86 个节点；全站现有 146 篇公开研究笔记",
  "R0.60 recap 之后的累计回顾收录 87 个节点；全站现有 147 篇公开研究笔记",
);
homeEdit.replace(
  "R0.60 之后的路线分成十七段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet、finite recurrence、Leray-paid excursion 与 fixed-zero boundary。R0.70A–R0.71V 共 48 个完成版本。",
  "R0.60 之后的路线分成十七段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen/incidence、packet/Bessel、internal-entry scaling、second-time jet、finite recurrence、Leray-paid excursion、fixed-zero boundary 与 complete first-row data-uniform no-go。R0.70A–R0.71W 共 49 个完成版本。",
);
homeEdit.replace(
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71V 在 Leray–Hopf 层级支付 right-rooted scale-zero excursion height；左端已正的 component 另付 initial trace。fixed target/window 的 genuine 2.5D sequence 排除相对所选 singleton target shell first-time-jet row 的指定零点采样。second-time row 仍可支付，完整 global \\(\\nu^2\\) baseline 与替代账本尚未排除。</p>",
  "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71W 排除 data-independent complete first-row ledger；指定的 \\(m=2\\) atom 发散，enstrophy ratio 有界，normalized full rotational charge 消失。初始 energy/enstrophy 无界，因此 \\(D^{1/3}\\) 与一般 data-dependent estimate 仍开放。</p>",
);
homeEdit.replace(
  String.raw`<p><strong style="color:var(--gold)">下一步 R0.71W：</strong>&nbsp;检查带 \(\mathcal R_Y(K)\) 因子的完整 \(\nu^2\) baseline 与 projected rotational term，判断 fixed-target high-frequency events 相对完整第一行 Leray ledger 是否仍非坍缩。</p>
          </div>
        </section>`,
  String.raw`<p><strong style="color:var(--gold)">R0.71W 已完成：</strong>&nbsp;amplitude doping 排除带完整 \(\nu^2\) baseline 与 projected rotational charge 的 data-uniform first-row ledger。</p>
          </div>` + releaseCard + String.raw`
        </section>`,
);
homeEdit.replace("综述 v1.08 · 2026-08-26", "综述 v1.09 · 2026-08-26");
homeEdit.replace("上次综述 v1.06 · 2026-08-26", "上次综述 v1.08 · 2026-08-26");
homeEdit.replaceAll("/i18n-en.js?v=1.08", "/i18n-en.js?v=1.09");

if (homeEdit.count('data-release="r071w"') !== 1) throw new Error("home: R0.71W card count");
if (homeEdit.count('href="/notes/r0-71w.html"') !== 2) throw new Error("home: R0.71W note links");
if (homeEdit.count("<summary>展开 57 篇公开笔记</summary>") !== 1) throw new Error("home: route count");
if (/我们|攻关|主攻|三重审计|杀死错误想法|突破/.test(homeEdit.value)) {
  throw new Error("home must use singular or neutral voice");
}

const literaturePath = resolve(root, "public/literature-review.html");
const literatureEdit = editor(await readFile(literaturePath, "utf8"), "literature");
literatureEdit.replaceAll("/i18n-en.js?v=1.08", "/i18n-en.js?v=1.09");
literatureEdit.replaceAll("/recap-r0-61-r0-71v.html", "/recap-r0-61-r0-71w.html");
literatureEdit.replaceAll("R0.69P–R0.71V", "R0.69P–R0.71W");
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71w.html">累计回顾与 86 节索引</a>',
  '<a href="/recap-r0-61-r0-71w.html">累计回顾与 87 节索引</a>',
);
literatureEdit.replace(
  '<a href="/recap-r0-61-r0-71w.html#node-index">打开 86 节完整索引</a>',
  '<a href="/recap-r0-61-r0-71w.html#node-index">打开 87 节完整索引</a>',
);
literatureEdit.replace(
  "R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V 再证明 right-rooted Leray-paid excursion-height packing，左端已正 component 需要另付 initial trace，并用 weighted area hierarchy、sine test 和 genuine 2.5D sequence 分离 level integral 与 fixed zero-level trace。保留下来的结果都不是全局正则性结论。",
  "R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q–U 给出 conditional incidence、genuine internal-entry、second-time-jet 与 finite recurrence 边界。R0.71V 分离 Leray-paid excursion 与 fixed zero-level trace。R0.71W 的 amplitude-doped exact 2.5D sequence 进一步排除 data-independent complete first-row ledger；初始数据依赖仍开放。保留下来的结果都不是全局正则性结论。",
);
literatureEdit.replace(
  '<div class="route-step closed"><header><b>R0.70A–I</b><strong>从移动环带到时间 Hardy 核</strong></header><p>移动标签、反向桥、固定尺度覆盖和仿射一阶展开等捷径被逐项关闭；冻结低频区可以闭合，移动低频区与偏差对角项仍然开放。<a href="/notes/r0-70i.html">阶段终点</a></p></div>',
  '<div class="route-step closed"><header><b>R0.70A–I</b><strong>从移动环带到时间 Hardy 核</strong></header><p>移动标签、反向桥、固定尺度覆盖和仿射一阶展开等捷径被逐项关闭；冻结低频区可以闭合，移动低频区与偏差对角项仍然开放。<a href="/notes/r0-70a.html">A</a> <a href="/notes/r0-70b.html">B</a> <a href="/notes/r0-70c.html">C</a> <a href="/notes/r0-70d.html">D</a> <a href="/notes/r0-70e.html">E</a> <a href="/notes/r0-70f.html">F</a> <a href="/notes/r0-70g.html">G</a> <a href="/notes/r0-70h.html">H</a> <a href="/notes/r0-70i.html">I</a></p></div>',
);
literatureEdit.replace(
  '<div class="route-step closed"><header><b>R0.70J–O</b><strong>偏差张量与有限观测边界</strong></header><p>无迹性、helicity 和归一化各向异性不产生普适符号；有限高频盲观测也不能统一重建未过滤临界横向涡量。<a href="/notes/r0-70o.html">阶段终点</a></p></div>',
  '<div class="route-step closed"><header><b>R0.70J–O</b><strong>偏差张量与有限观测边界</strong></header><p>无迹性、helicity 和归一化各向异性不产生普适符号；有限高频盲观测也不能统一重建未过滤临界横向涡量。<a href="/notes/r0-70j.html">J</a> <a href="/notes/r0-70k.html">K</a> <a href="/notes/r0-70l.html">L</a> <a href="/notes/r0-70m.html">M</a> <a href="/notes/r0-70n.html">N</a> <a href="/notes/r0-70o.html">O</a></p></div>',
);
literatureEdit.replace(
  '<div class="route-step kept"><header><b>R0.70P–Z</b><strong>完整框架与响应距离通道</strong></header><p>条件投影桥和响应差的临界增益被保留；物理协方差面积、正主特征值和强谱隙仍不能决定有符号功。<a href="/notes/r0-70z.html">阶段终点</a></p></div>',
  '<div class="route-step kept"><header><b>R0.70P–Z</b><strong>完整框架与响应距离通道</strong></header><p>条件投影桥和响应差的临界增益被保留；物理协方差面积、正主特征值和强谱隙仍不能决定有符号功。<a href="/notes/r0-70p.html">P</a> <a href="/notes/r0-70q.html">Q</a> <a href="/notes/r0-70r.html">R</a> <a href="/notes/r0-70s.html">S</a> <a href="/notes/r0-70t.html">T</a> <a href="/notes/r0-70u.html">U</a> <a href="/notes/r0-70v.html">V</a> <a href="/notes/r0-70w.html">W</a> <a href="/notes/r0-70x.html">X</a> <a href="/notes/r0-70y.html">Y</a> <a href="/notes/r0-70z.html">Z</a></p></div>',
);
literatureEdit.replace(
  String.raw`              <div class="route-step kept"><header><b>R0.71V</b><strong>excursion height Leray-paid，fixed zero-level trace 仍开放</strong></header><p>compact-shell AC representatives 与 weighted Cauchy–Schwarz 给 right-rooted scale-zero excursion packing；左端已正 component 另付 initial trace。area formula、sine test 与 fixed-target genuine 2.5D sequence 排除相对所选 singleton target shell first-time-jet row 的 fixed-zero sampling；完整 \(\nu^2\) baseline 尚未排除。<a href="/notes/r0-71v.html">研究笔记</a> <a href="/recap-r0-61-r0-71w.html">当前累计回顾</a> <a href="#r071v-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71W</b><strong>complete Leray ledger / rotational term</strong></header><p>平衡 decoupled background，并比较 atom 与带 \(\mathcal R_Y(K)\) 因子的完整 \(\nu^2\) baseline、projected rotational charge。</p></div>`,
  String.raw`              <div class="route-step kept"><header><b>R0.71V</b><strong>excursion height Leray-paid，fixed zero-level trace 仍开放</strong></header><p>compact-shell AC representatives 与 weighted Cauchy–Schwarz 给 right-rooted scale-zero excursion packing；area formula、sine test 与 fixed-target genuine 2.5D sequence 排除 selected first-row fixed-zero sampling。<a href="/notes/r0-71v.html">研究笔记</a></p></div>
              <div class="route-step kept"><header><b>R0.71W</b><strong>data-uniform complete first-row ledger 失败</strong></header><p>amplitude-doped exact triangular 2.5D sequence 满足 \(J_{*,2,q}\to\infty\)、\(\mathcal R_Y=O(1)\)，且 normalized full projected rotational charge 趋零。初始 data size 无界。<a href="/notes/r0-71w.html">研究笔记</a> <a href="/recap-r0-61-r0-71w.html">当前累计回顾</a> <a href="#r071w-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71X</b><strong>data-dependent one-third boundary</strong></header><p>比较 exact atom scaling 与 \(D^{1/3}\) 或更强的 scale-compatible payment。</p></div>`,
);
literatureEdit.replace(
  '<h3 id="r071v-boundary">R0.71V 关闭了什么，R0.71W 只检查什么</h3>',
  '<h3 id="r071w-boundary">R0.71W 关闭了什么，R0.71X 只检查什么</h3>',
);
literatureEdit.replace(
  String.raw`<p>R0.71V 在 Leray–Hopf 层级证明 right-rooted compact-shell excursion-height packing；左端已正 component 另付 initial trace。它还写出 classical root atom 与 excursion 的精确无量纲转换因子 \(D_E\)。weighted area formula 只把 linear-slope level density 压到 first-time row；quadratic slope 需要 cubic time occupation，普通 \(L^1\) level control 不决定 distinguished zero-level trace。sine path 给抽象 method test，固定 target/window 的 genuine unforced 2.5D NSE 序列进一步排除相对所选 singleton target shell first-time-jet row 的指定零点采样。该序列不证明 second-time coefficient sharp，也不排除完整 global \(\nu^2\) baseline 或另一 dynamical charge。R0.71W 只检查带 \(\mathcal R_Y(K)\) 因子的完整 Leray ledger。我继续用下面六条筛选。</p>`,
  String.raw`<p>R0.71W 保留固定 target、固定宏观窗口、enstrophy ratio、\(\nu^2\) baseline 与 complete projected rotational charge。amplitude-doped exact triangular 2.5D sequence 仍使指定的 \(m=2\) atom 相对 complete first-row ledger 发散，因此该 data-uniform estimate 失败。构造的初始 energy/enstrophy 无界；它只排除 \(D^\beta\)、\(\beta&lt;1/3\)，不排除 \(D^{1/3}\)、更强数据依赖或 structurally different payment。R0.71X 只检查 data-dependent one-third boundary。我继续用下面六条筛选。</p>`,
);
literatureEdit.replace(
  String.raw`<div class="boundary"><strong>R0.71V 的一手文献边界</strong><p><a href="https://doi.org/10.1007/978-3-642-62010-2">Federer</a>给 weighted area formula；<a href="https://doi.org/10.4064/fm-7-1-225-236">Banach</a>给 level indicatrix 与 total variation；<a href="https://doi.org/10.1112/blms/bdu014">Bertoin–Yor</a>与 <a href="https://doi.org/10.4064/cm6583-3-2017">Łochowski</a>处理 occupation、crossings 与 truncated variation。<a href="https://doi.org/10.1063/1.4990082">Biferale–Buzzicotti–Linkmann</a>记录 exact 2D3C reduction；<a href="https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf">Temam</a>支持 weak energy spaces 与二维 strong-solution background。checked sources 给 level-integrated 或 almost-every-level 结论，不给 fixed zero-level quadratic trace。bounded audit 未定位到完整 R0.71V theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
  String.raw`<div class="boundary"><strong>R0.71W 的一手文献边界</strong><p><a href="https://doi.org/10.1007/BF02547354">Leray</a>与 <a href="https://doi.org/10.1137/1.9781611970050">Temam</a>支持 weak-energy 与 semigroup framework；<a href="https://doi.org/10.1063/1.4990082">Biferale–Buzzicotti–Linkmann</a>记录 exact 2D3C reduction；<a href="https://link.springer.com/book/10.1007/978-1-4612-0915-5">Karlin–Studden</a>给 Chebyshev-system interpolation background。uniform rescaled IFT 与 complete rotational estimate 在本节直接证明。bounded audit 未定位到 data-uniform fixed-zero complete first-row theorem；这不是原创性、优先权或不存在性结论。</p></div>`,
);
literatureEdit.replace("文献综述 v1.08 · 2026-08-26", "文献综述 v1.09 · 2026-08-26");

if (literatureEdit.count("<b>R0.71W</b>") !== 1) throw new Error("literature: R0.71W node");
if (literatureEdit.count("开放接口 · R0.71X") !== 1) throw new Error("literature: R0.71X interface");
for (const release of "abcdefghijklmnopqrstuvwxyz".split("")) {
  const slug = "/notes/r0-70" + release + ".html";
  if (!literatureEdit.value.includes(slug)) throw new Error("literature: missing direct link " + slug);
}
for (const release of "abcdefghijklmnopqrstuvw".split("")) {
  const slug = "/notes/r0-71" + release + ".html";
  if (!literatureEdit.value.includes(slug)) throw new Error("literature: missing direct link " + slug);
}
if (/我们|攻关|主攻|三重审计|杀死错误想法|突破/.test(literatureEdit.value)) {
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
      release: "R0.71W",
      siteVersion: "v1.09",
      publicNotes: 147,
      currentRouteNotes: 57,
      recapNodes: 87,
      completedReleasesR070AToR071W: 49,
      literatureDirectLinksR070AOnward: 49,
      next: "R0.71X",
    },
    null,
    2,
  ),
);
