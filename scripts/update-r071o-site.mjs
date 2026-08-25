import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) {
        throw new Error(label + ": expected one match, found " + count + ": " + before.slice(0, 120));
      }
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) {
        throw new Error(label + ": expected at least " + minimum + " matches, found " + count + ": " + before);
      }
      value = value.split(before).join(after);
    },
    replaceBlock(start, end, after) {
      const count = value.split(start).length - 1;
      if (count !== 1) {
        throw new Error(label + ": expected one block start, found " + count + ": " + start);
      }
      const startIndex = value.indexOf(start);
      const endIndex = value.indexOf(end, startIndex + start.length);
      if (endIndex < 0) throw new Error(label + ": block end not found: " + end);
      value = value.slice(0, startIndex) + after + value.slice(endIndex + end.length);
    },
    count(fragment) {
      return value.split(fragment).length - 1;
    },
    get value() {
      return value;
    },
  };
}

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
const homeIsCurrent = homeEdit.count('data-release="r071o"') === 1;

const releaseCard = String.raw`

          <div class="task-one" id="r071o" data-release="r071o" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71O · 2026-08-26</p>
            <h3>soft denominator 恢复一侧 hard traces，Jordan face cost 没有自动消失</h3>
            <p>
              在每个 \(d_Q&gt;0\) 分支上，
              \[
                \sigma_{Q,\varepsilon}=\frac{d_Q}{d_Q+\varepsilon},\qquad
                z_{Q,\varepsilon}=\sqrt{\sigma_{Q,\varepsilon}}z_Q,\qquad
                a_{Q,\varepsilon}=\sigma_{Q,\varepsilon}a_Q.
              \]
              因而 soft source 精确分成 hard interior source 与
              \((\sigma_{Q,\varepsilon})_ta_Q\) face layer。
            </p>
            <p>
              若 \(C_Q(t_0+\tau)=c\tau^m+O(|\tau|^{m+1})\)、
              \(C_{Q,t}(t_0+\tau)=mc\tau^{m-1}+O(|\tau|^m)\)，且 \(F_j,Y\) 的一阶导数局部有界，一侧 traces 由
              \(\gamma=\langle F_j(t_0),c\rangle/(\sqrt{Y(t_0)}\|c\|_2)\) 决定。
              奇阶零点的 signed atom 是 \(\gamma|\gamma|\delta_{t_0}\)，face variation 为
              \(\gamma^2\)；偶阶 signed atom 为零，但 \(\gamma&gt;0\) 时仍支付
              \(2\gamma^2\) 的 Jordan variation。
            </p>
            <p>
              raw source 与 radial term 各自按 \(\log(1/\varepsilon)\) 增长，联合后对数精确抵消。一个 smooth Hilbert path 使 face cost 按零点数增长，而 ordinary derivative、source 与 denominator-mass budgets 保持有界；它不是 NSE 多-face 构造。真实 smooth NSE 初始 jet 则给出精确右 entry trace \(1/4\)。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节关闭的是“soft denominator 自动删除 fixed-cell faces”这一想法。它没有证明完整 NSE weighted face sum 发散，也没有得到继续性、奇性或全局正则性结论。</p>
            <p>
              <a href="/notes/r0-71o.html"><strong>阅读 R0.71O 研究笔记 →</strong></a> ·
              <a href="/notes/r0-71o.pdf">下载同步 PDF</a><br>
              <a href="/figures/r0-71o-soft-denominator-faces.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071o">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071o_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071o_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071o_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071o_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071o-soft-denominator-faces/fig-r071o-soft-denominator-faces">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71o.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71o.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71P：</strong>&nbsp;固定 partition 上，检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否存在 NSE-specific cancellation 或新的必要输入。total-Jordan sum 是更强的后续变体。</p>
          </div>`;

if (!homeIsCurrent) {
  homeEdit.replace('<strong>v0.99</strong>网页版本', '<strong>v1.00</strong>网页版本');
  homeEdit.replace('<strong>138</strong>公开研究笔记', '<strong>139</strong>公开研究笔记');
  homeEdit.replace('<strong>R0.71N</strong>最新研究节点', '<strong>R0.71O</strong>最新研究节点');
  homeEdit.replace(
    '<strong>soft denominator / one-sided faces</strong>当前方向',
    '<strong>fixed-partition weighted positive-entry sum</strong>当前方向',
  );
  homeEdit.replace(
    String.raw`<div class="summary-item"><strong>我目前关注</strong><span>固定 cell 上比较 hard denominator 与 \(\sqrt{d_Q+\varepsilon}\)，检查 \(\varepsilon\downarrow0\) 的 source measure 和 \(d_Q=0\) 一侧 faces 能否由已有预算支付。</span></div>`,
    String.raw`<div class="summary-item"><strong>我目前关注</strong><span>固定 partition 上，检查全壳、全小区的正向进入和 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否有新的 cancellation 或必须保留额外条件。</span></div>`,
  );
  homeEdit.replace('Research topology · R0.1–R0.71N', 'Research topology · R0.1–R0.71O');
  homeEdit.replaceAll('/recap-r0-61-r0-71n.html', '/recap-r0-61-r0-71o.html');
  homeEdit.replaceAll('/recap-r0-61-r0-71n.pdf', '/recap-r0-61-r0-71o.pdf');
  homeEdit.replace('<span class="route-range">R0.69P–R0.71N</span>', '<span class="route-range">R0.69P–R0.71O</span>');
  homeEdit.replace(
    '<h3>从有符号环带障碍走到 signed second-jet boundary</h3>',
    '<h3>从有符号环带障碍走到 soft-denominator face boundary</h3>',
  );
  homeEdit.replace(
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–L 把时间缺口收缩到 fixed matched-cell heat gap 和 exact viscous fusion；R0.71M 再给出 exact increment–projective bridge。R0.71N 从完整标量同时保留三个时间导数，证明 projective completion 中表面的正平方被 local-enstrophy acceleration 精确消去。留下的是同尺度的 signed second jet，而不是新的耗散。</p>',
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–N 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet。R0.71O 证明 soft denominator 精确恢复 hard 一侧 traces：signed atoms 可以抵消，Jordan face costs 仍保留；ordinary budgets 不统一支付抽象 face count。</p>',
  );
  homeEdit.replace(
    '→ increment–projective bridge → signed second-jet boundary</p>',
    '→ increment–projective bridge → signed second-jet boundary → soft-denominator face boundary</p>',
  );
  homeEdit.replace('<summary>展开 48 篇公开笔记</summary>', '<summary>展开 49 篇公开笔记</summary>');
  homeEdit.replace('aria-label="R0.69P–R0.71N"', 'aria-label="R0.69P–R0.71O"');
  homeEdit.replace(
    '                  <a class="milestone" href="/notes/r0-71n.html">R0.71N</a>\n',
    '                  <a class="milestone" href="/notes/r0-71n.html">R0.71N</a>\n                  <a class="milestone" href="/notes/r0-71o.html">R0.71O</a>\n',
  );
  homeEdit.replaceBlock(
    '            <article class="tree-node next">',
    '            </article>',
    String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71P</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>Fixed-partition all-shell/all-cell weighted positive-entry sum</h3>
              <p>我保持 multiplier、cutoff 与 partition 固定，先检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\) 是否存在 NSE-specific cancellation；total-Jordan sum 是更强的后续变体，暂不引入 refresh atoms 或 moving cutoffs。</p>
            </article>`,
  );
  homeEdit.replace('累计回顾 R0.61–R0.71N · 2026-08-26', '累计回顾 R0.61–R0.71O · 2026-08-26');
  homeEdit.replace(
    'R0.60 recap 之后的累计回顾收录 78 个节点；全站现有 138 篇公开研究笔记',
    'R0.60 recap 之后的累计回顾收录 79 个节点；全站现有 139 篇公开研究笔记',
  );
  homeEdit.replace(
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、黏性融合、增量—投影接口与 signed second jet。',
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、signed second jet 与 soft-denominator faces。R0.70A–R0.71O 共 41 个完成版本。',
  );
  homeEdit.replace(
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71N 关闭了把 projective completion 中的正平方解释成新耗散的路线：local filtered enstrophy 代回后，同一平方被 acceleration 精确消去。剩余 signed second jet 仍是临界量；soft denominator、零分母 faces 和无条件 weighted BV 仍未闭合。</p>',
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71O 证明 soft denominator 只平滑坐标，不删除一侧 face cost；signed atoms 可以抵消，Jordan masses 仍保留。固定 partition 上的 all-shell/all-cell weighted positive-entry sum 尚未闭合。</p>',
  );
  homeEdit.replace(
    String.raw`<p><strong style="color:var(--gold)">下一步 R0.71O：</strong>&nbsp;固定 cell 上比较 hard denominator 与 \(\sqrt{d_Q+\varepsilon}\)，核对 \(d_Q=0\) 的一侧 faces 和 soft-limit source measure；暂不进入 refresh 或 moving cells。</p>`,
    '<p><strong style="color:var(--gold)">R0.71O 已完成：</strong>&nbsp;soft–hard factorization 与有限阶 face atoms 已显式闭合；额外 soft radial damping 没有 finite-order atom。</p>',
  );
  homeEdit.replace(
    '          </div>\n        </section>\n\n      </article>',
    '          </div>' + releaseCard + '\n        </section>\n\n      </article>',
  );
  homeEdit.replace('综述 v0.99 · 2026-08-26', '综述 v1.00 · 2026-08-26');
  homeEdit.replace('上次综述 v0.98 · 2026-08-26', '上次综述 v0.99 · 2026-08-26');
  homeEdit.replaceAll('/i18n-en.js?v=0.99', '/i18n-en.js?v=1.00');
  homeEdit.replace(
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71N 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71O 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
  );
}

if (homeEdit.count('data-release="r071o"') !== 1) {
  throw new Error("home: R0.71O release-card count is not one");
}
if (homeEdit.count('href="/notes/r0-71o.html"') !== 2) {
  throw new Error("home: expected exactly two R0.71O note links");
}
if (homeEdit.count('<summary>展开 49 篇公开笔记</summary>') !== 1) {
  throw new Error("home: route-note count is not 49");
}
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const litEdit = editor(await readFile(literaturePath, "utf8"), "literature");
const literatureIsCurrent = litEdit.count('<b>R0.71O</b>') === 1;

if (!literatureIsCurrent) {
  litEdit.replaceAll('/i18n-en.js?v=0.99', '/i18n-en.js?v=1.00');
  litEdit.replace('本站 R0.69P–R0.71N 只列为研究笔记', '本站 R0.69P–R0.71O 只列为研究笔记');
  litEdit.replaceAll('/recap-r0-61-r0-71n.html', '/recap-r0-61-r0-71o.html');
  litEdit.replace(
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71o.html">累计回顾与 78 节索引</a>中。R0.69P–R0.71N 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion 与 exact increment–projective bridge，走到完整 fixed-cell 标量的 signed second-jet boundary。R0.71N 证明 projective completion 中表面的正平方被 local filtered-enstrophy acceleration 精确消去；留下的临界二阶余项没有固定符号。保留下来的结果都不是全局正则性结论。</p>',
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71o.html">累计回顾与 79 节索引</a>中。R0.69P–R0.71O 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion、increment bridge 与 signed second jet，走到 soft-denominator face boundary。R0.71O 证明 soft quotient 恢复 hard 一侧迹，signed atoms 可以相消而 Jordan face costs 保留。保留下来的结果都不是全局正则性结论。</p>',
  );
  litEdit.replace(
    '<a href="/recap-r0-61-r0-71o.html#node-index">打开 78 节完整索引</a>',
    '<a href="/recap-r0-61-r0-71o.html#node-index">打开 79 节完整索引</a>',
  );
  litEdit.replace(
    String.raw`              <div class="route-step closed"><header><b>R0.71N</b><strong>正平方被 local-enstrophy acceleration 精确消去</strong></header><p>完整 \(B_{Q,t},d_{Q,t},Y_t\) 标量先写成 square–residual form；代入 \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 后，acceleration 中的同一 pairing 产生 \(-\mathcal P_Q^\square\)，恰好消去表面的正平方。两个 \(z_Q&gt;0\) 的 smooth NSE initial jets 给出 \(\mathcal J_Q\) 双号，但不是时间区间符号定理。<a href="/notes/r0-71n.html">研究笔记</a> <a href="/recap-r0-61-r0-71o.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71O</b><strong>soft denominator 与 \(d_Q=0\) 一侧 faces</strong></header><p>下一节仍留在 fixed cells，比较 hard components 与 \(\sqrt{d_Q+\varepsilon}\)，检查 \(\varepsilon\downarrow0\) 的 source measures 和 denominator-zero 一侧 faces；暂不进入 refresh 或 moving cutoffs。</p></div>`,
    String.raw`              <div class="route-step closed"><header><b>R0.71N</b><strong>正平方被 local-enstrophy acceleration 精确消去</strong></header><p>完整 fixed-cell 标量只留下临界 signed second jet。<a href="/notes/r0-71n.html">研究笔记</a></p></div>
              <div class="route-step closed"><header><b>R0.71O</b><strong>soft quotient 恢复一侧 traces 与 Jordan face atoms</strong></header><p>精确 factorization 把 soft source 分成 hard interior source 与 face layer。有限阶零点的 signed atom 可以消失，正负 Jordan masses 仍支付左右 traces；raw logarithms 只有联合后才有限。ordinary-budget 抽象族不等于 NSE 多-face 构造。<a href="/notes/r0-71o.html">研究笔记</a> <a href="/recap-r0-61-r0-71o.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71P</b><strong>fixed-partition all-shell/all-cell weighted positive-entry sum</strong></header><p>下一节固定 multiplier、cutoff 与 partition，检查 \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0\in\mathcal Z_{j,Q}}A_{j,Q,+}(t_0)\)；total-Jordan sum 是更强的后续变体，暂不进入 refresh 或 moving cutoffs。</p></div>`,
  );
  litEdit.replace(
    '<h3>R0.71N 关闭了什么，R0.71O 只检查什么</h3>',
    '<h3>R0.71O 关闭了什么，R0.71P 只检查什么</h3>',
  );
  litEdit.replace(
    '<p>R0.71N 没有把完成平方后的非负项当作自动耗散。完整时间导数与局部 filtered enstrophy 代回后，同一平方在 acceleration 中以负号出现并精确消去；最终只剩临界 signed second jet。这关闭的是一个 fixed-cell 代数候选，不是一般 signed NSE no-go。R0.71O 只检查 hard/soft denominator 极限与一侧 face measure，并继续用下面六条筛选。</p>',
    String.raw`<p>R0.71O 没有把 soft denominator 当作删除 \(d_Q=0\) faces 的规则。soft equation 精确恢复一侧 hard traces；signed atoms 可以抵消，但 Jordan variation 仍支付 entry 与 exit。抽象 smooth paths 只排除 ordinary budgets 的普适 face-count 控制，不是 NSE 多-face 反例。R0.71P 只检查 fixed-partition weighted positive-entry sum；total-Jordan sum 是更强的后续变体。我继续用下面六条筛选。</p>`,
  );
  litEdit.replace(
    String.raw`<div class="boundary"><strong>R0.71N 的一手文献边界</strong><p><a href="https://arxiv.org/abs/physics/0606159">Eyink</a> 给出 filtered vortex force 与 filtered enstrophy；<a href="https://arxiv.org/abs/1107.0058">Dascaliuc–Grujić</a> 和 <a href="https://arxiv.org/abs/1108.1165">Tao</a> 给出严谨 local-enstrophy cutoff ledger；<a href="https://arxiv.org/abs/chao-dyn/9709003">Galanti–Gibbon–Heritage</a> 给出单位涡量方向的切投影方程；<a href="https://arxiv.org/abs/2606.27560v1">Yu 2026 预印本</a>是已查到最邻近的 filtered-vorticity/local-cutoff 账本。它们都没有本站固定单元的 cutoff–curl denominator 与 \(B_Q/\sqrt{Yd_Q}\) 完整时间演化。限定检索未找到同时保留 \(B_{Q,t},d_{Q,t},Y_t\) 的直接来源；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
    String.raw`<div class="boundary"><strong>R0.71O 的一手文献边界</strong><p><a href="https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7">Temam</a>给出周期强解经典区间内的时间解析性背景；<a href="https://doi.org/10.1007/BF02196453">Reshetnyak</a>与<a href="https://www.mathnet.ru/eng/sm4127">Vol'pert</a>给出 variation-measure 稳定性和 BV chain-rule 基础；<a href="https://doi.org/10.1007/BF01236935">Fleming–Rishel</a>及<a href="https://arxiv.org/abs/1503.01746v4">Łochowski</a>连接 BV、coarea 与 crossing counts。它们不从 Leray energy 生成本站 fixed-cell quotient 的零层 face sum。限定检索未找到同时识别一侧 Jordan atoms、又支付完整 NSE frame–cell sum 的直接定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  );
  litEdit.replace('文献综述 v0.99 · 2026-08-26', '文献综述 v1.00 · 2026-08-26');
}

if (litEdit.count('<b>R0.71O</b>') !== 1) {
  throw new Error("literature: expected one R0.71O route row");
}
if (litEdit.count('开放接口 · R0.71P') !== 1) {
  throw new Error("literature: expected one R0.71P interface");
}
if (litEdit.count('bounded negative finding') !== 1) {
  throw new Error("literature: bounded-search boundary count is not one");
}
await writeFile(literaturePath, litEdit.value);

console.log(JSON.stringify({
  status: "ok",
  home: homePath,
  literature: literaturePath,
  homeR071oReleaseCards: homeEdit.count('data-release="r071o"'),
  homeR071oNoteLinks: homeEdit.count('href="/notes/r0-71o.html"'),
  routeNotes: 49,
  recapNodes: 79,
  publicNotes: 139,
  completedReleasesR070AToR071O: 41,
  latest: "R0.71O",
  next: "R0.71P",
}, null, 2));
