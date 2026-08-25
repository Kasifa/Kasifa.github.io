import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) {
        throw new Error(`${label}: expected one match, found ${count}: ${before.slice(0, 120)}`);
      }
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) {
        throw new Error(`${label}: expected at least ${minimum} matches, found ${count}: ${before}`);
      }
      value = value.split(before).join(after);
    },
    replaceBlock(start, end, after) {
      const count = value.split(start).length - 1;
      if (count !== 1) {
        throw new Error(`${label}: expected one block start, found ${count}: ${start}`);
      }
      const startIndex = value.indexOf(start);
      const endIndex = value.indexOf(end, startIndex + start.length);
      if (endIndex < 0) throw new Error(`${label}: block end not found: ${end}`);
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
const homeIsCurrent = homeEdit.count('data-release="r071n"') === 1;

const releaseCard = String.raw`

          <div class="task-one" id="r071n" data-release="r071n" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71N · 2026-08-26</p>
            <h3>表面的正平方在完整标量中精确消去，留下临界 signed second jet</h3>
            <p>
              固定小区上，完整标量先有精确的平方—余项表示
              \[
                \mathcal J_Q
                =\frac{\mathcal P_Q^\square+\mathfrak R_Q}{\sqrt{Yd_Q}},
                \qquad
                \mathcal P_Q^\square
                =\int\chi_Q\left|G_j+\frac\nu2H_j\right|^2.
              \]
              名义率 \(\nu\kappa_j^2\) 与 radial/projective 坐标中的项精确消去。
            </p>
            <p>
              令 \(e_Q=\frac12\int\chi_Q|W_j|^2\) 与
              \(D_Q^\chi=-\langle\chi_QW_j,\Delta W_j\rangle\)。局部 filtered-enstrophy 恒等式
              \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 代回后，\(\mathfrak R_Q\) 中出现
              \(-\mathcal P_Q^\square\)，恰好消去前面的正平方。剩余项仍是尺度临界的有符号二阶时间与混合归一化账本。
            </p>
            <p>
              两个显式五模光滑 NSE 初始 jet 都满足 \(z_Q&gt;0\)，但分别给出
              \(\mathcal J_Q=1.3523543\) 与 \(-7.3713441\)。48、64、80 三档 Fourier 网格一致；这是有限初始-jet 诊断，不是时间区间符号定理。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节关闭的是“完成 projective square 后把它当作新耗散”这一条 fixed-cell 代数路线。它没有证明 signed second jet 不能由其他 NSE 机制控制，也没有得到继续性、奇性或全局正则性结论。</p>
            <p>
              <a href="/notes/r0-71n.html"><strong>阅读 R0.71N 研究笔记 →</strong></a> ·
              <a href="/notes/r0-71n.pdf">下载同步 PDF</a><br>
              <a href="/figures/r0-71n-full-scalar.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071n">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071n_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071n_literature_audit.md">查看主源文献台账</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071n-full-scalar/fig-r071n-square-residual-boundary">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71n.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71n.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71O：</strong>&nbsp;固定 cell 上比较 hard denominator 与 \(\sqrt{d_Q+\varepsilon}\)，核对 \(d_Q=0\) 的一侧 faces 和 soft-limit source measure；暂不进入 refresh 或 moving cells。</p>
          </div>`;

if (!homeIsCurrent) {
  homeEdit.replace('<strong>v0.98</strong>网页版本', '<strong>v0.99</strong>网页版本');
  homeEdit.replace('<strong>137</strong>公开研究笔记', '<strong>138</strong>公开研究笔记');
  homeEdit.replace('<strong>R0.71M</strong>最新研究节点', '<strong>R0.71N</strong>最新研究节点');
  homeEdit.replace(
    '<strong>full scalar fusion / signed residual</strong>当前方向',
    '<strong>soft denominator / one-sided faces</strong>当前方向',
  );
  homeEdit.replace(
    String.raw`<div class="summary-item"><strong>我目前关注</strong><span>从完整标量 \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，检查是否存在第二次精确融合或明确的有符号余项。</span></div>`,
    String.raw`<div class="summary-item"><strong>我目前关注</strong><span>固定 cell 上比较 hard denominator 与 \(\sqrt{d_Q+\varepsilon}\)，检查 \(\varepsilon\downarrow0\) 的 source measure 和 \(d_Q=0\) 一侧 faces 能否由已有预算支付。</span></div>`,
  );
  homeEdit.replace('Research topology · R0.1–R0.71M', 'Research topology · R0.1–R0.71N');
  homeEdit.replaceAll('/recap-r0-61-r0-71m.html', '/recap-r0-61-r0-71n.html');
  homeEdit.replaceAll('/recap-r0-61-r0-71m.pdf', '/recap-r0-61-r0-71n.pdf');
  homeEdit.replace('<span class="route-range">R0.69P–R0.71M</span>', '<span class="route-range">R0.69P–R0.71N</span>');
  homeEdit.replace(
    '<h3>从有符号环带障碍走到 exact increment–projective bridge</h3>',
    '<h3>从有符号环带障碍走到 signed second-jet boundary</h3>',
  );
  homeEdit.replace(
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 从恒定投影障碍走到 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–K 把时间缺口收缩到全壳正缺陷与 fixed matched-cell heat gap；R0.71L 又把 raw viscous collar 精确融合回 localized Laplacian row。R0.71M 现在给出 annular-filter Lamb commutator 的精确二次速度增量公式、完整 fixed-cell projective pairing 与四行临界直接账本。热包说明这些绝对临界预算不由能量类普适推出，但不排除 NSE 特有的 signed cancellation。</p>',
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–L 把时间缺口收缩到 fixed matched-cell heat gap 和 exact viscous fusion；R0.71M 再给出 exact increment–projective bridge。R0.71N 从完整标量同时保留三个时间导数，证明 projective completion 中表面的正平方被 local-enstrophy acceleration 精确消去。留下的是同尺度的 signed second jet，而不是新的耗散。</p>',
  );
  homeEdit.replace(
    '→ exact viscous fusion → increment–projective bridge</p>',
    '→ exact viscous fusion → increment–projective bridge → signed second-jet boundary</p>',
  );
  homeEdit.replace('<summary>展开 47 篇公开笔记</summary>', '<summary>展开 48 篇公开笔记</summary>');
  homeEdit.replace('aria-label="R0.69P–R0.71M"', 'aria-label="R0.69P–R0.71N"');
  homeEdit.replace(
    '                  <a class="milestone" href="/notes/r0-71m.html">R0.71M</a>\n',
    '                  <a class="milestone" href="/notes/r0-71m.html">R0.71M</a>\n                  <a class="milestone" href="/notes/r0-71n.html">R0.71N</a>\n',
  );
  homeEdit.replaceBlock(
    '            <article class="tree-node next">',
    '            </article>',
    String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71O</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>Soft denominator 与 \(d_Q=0\) 一侧 faces</h3>
              <p>我继续使用 fixed cells，比较 hard components 与 \(R_{Q,\varepsilon}=\sqrt{d_Q+\varepsilon}\)。R0.71O 检查 \(\varepsilon\downarrow0\) 时的 source measures 和 denominator-zero 一侧 faces，能否由已有 energy 与 denominator-mass budgets 统一支付；暂不进入 refresh atoms 或 moving cutoffs。</p>
            </article>`,
  );
  homeEdit.replace('累计回顾 R0.61–R0.71M · 2026-08-26', '累计回顾 R0.61–R0.71N · 2026-08-26');
  homeEdit.replace(
    'R0.60 recap 之后的累计回顾收录 77 个节点；全站现有 137 篇公开研究笔记',
    'R0.60 recap 之后的累计回顾收录 78 个节点；全站现有 138 篇公开研究笔记',
  );
  homeEdit.replace(
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、全壳正缺陷、固定匹配小区、黏性融合与增量—投影接口。',
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、黏性融合、增量—投影接口与 signed second jet。',
  );
  homeEdit.replace(
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71M 把 critical increment bridge 压成 exact commutator、exact projective pairing 与四行充分账本；它同时证明标准能量类不普适嵌入所测试的绝对临界预算。这个函数空间分离不是 NSE 解反例，完整标量的 signed fusion、faces 和无条件 weighted BV 仍未闭合。</p>',
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71N 关闭了把 projective completion 中的正平方解释成新耗散的路线：local filtered enstrophy 代回后，同一平方被 acceleration 精确消去。剩余 signed second jet 仍是临界量；soft denominator、零分母 faces 和无条件 weighted BV 仍未闭合。</p>',
  );
  homeEdit.replace(
    String.raw`<p><strong style="color:var(--gold)">下一步 R0.71N：</strong>&nbsp;从完整 \(\mathcal J_Q\) 同时展开三个时间导数，检查第二次精确标量融合或明确的 signed residual。</p>`,
    '<p><strong style="color:var(--gold)">R0.71N 已完成：</strong>&nbsp;表面的正平方被 local-enstrophy acceleration 精确消去；完整 fixed-cell 标量只留下同尺度的 signed second jet。</p>',
  );
  homeEdit.replace(
    '          </div>\n        </section>\n\n      </article>',
    `          </div>${releaseCard}\n        </section>\n\n      </article>`,
  );
  homeEdit.replace('综述 v0.98 · 2026-08-26', '综述 v0.99 · 2026-08-26');
  homeEdit.replace('上次综述 v0.97 · 2026-08-26', '上次综述 v0.98 · 2026-08-26');
  homeEdit.replaceAll('/i18n-en.js?v=0.98', '/i18n-en.js?v=0.99');
  homeEdit.replace(
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71M 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71N 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
  );
}

if (homeEdit.count('data-release="r071n"') !== 1) {
  throw new Error('home: R0.71N release-card count is not one');
}
if (homeEdit.count('href="/notes/r0-71n.html"') !== 2) {
  throw new Error('home: expected exactly two R0.71N note links');
}
if (homeEdit.count('<summary>展开 48 篇公开笔记</summary>') !== 1) {
  throw new Error('home: route-note count is not 48');
}
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const litEdit = editor(await readFile(literaturePath, "utf8"), "literature");
const literatureIsCurrent = litEdit.count('<b>R0.71N</b>') === 1;

if (!literatureIsCurrent) {
  litEdit.replaceAll('/i18n-en.js?v=0.98', '/i18n-en.js?v=0.99');
  litEdit.replace('本站 R0.69P–R0.71M 只列为研究笔记', '本站 R0.69P–R0.71N 只列为研究笔记');
  litEdit.replaceAll('/recap-r0-61-r0-71m.html', '/recap-r0-61-r0-71n.html');
  litEdit.replace(
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71n.html">累计回顾与 77 节索引</a>中。R0.69P–R0.71M 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap 与 viscous fusion，走到 exact increment–projective bridge。R0.71M 给出 annular-filter Lamb commutator 的精确二次速度增量公式和完整 fixed-cell pairing；当前直接绝对估计产生四行临界充分账本。热包排除从 Leray energy 到所测试绝对临界预算的普适嵌入，但不是 NSE 解反例。保留下来的结果都不是全局正则性结论。</p>',
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71n.html">累计回顾与 78 节索引</a>中。R0.69P–R0.71N 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion 与 exact increment–projective bridge，走到完整 fixed-cell 标量的 signed second-jet boundary。R0.71N 证明 projective completion 中表面的正平方被 local filtered-enstrophy acceleration 精确消去；留下的临界二阶余项没有固定符号。保留下来的结果都不是全局正则性结论。</p>',
  );
  litEdit.replace(
    '<a href="/recap-r0-61-r0-71n.html#node-index">打开 77 节完整索引</a>',
    '<a href="/recap-r0-61-r0-71n.html#node-index">打开 78 节完整索引</a>',
  );
  litEdit.replace(
    String.raw`              <div class="route-step closed"><header><b>R0.71M</b><strong>精确 increment–projective bridge 与四行直接临界账本</strong></header><p>环带 Lamb 交换子具有精确二次速度增量表示；fixed-cell projective pairing 同时保留 resolved transport、differentiated commutator、projective denominator geometry 与 viscous annular mismatch。热包只排除这些绝对预算的普适能量嵌入，不是 NSE 解反例。<a href="/notes/r0-71m.html">研究笔记</a> <a href="/recap-r0-61-r0-71n.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71N</b><strong>完整标量的第二次融合或 signed residual</strong></header><p>下一节仍留在 fixed cells，从整个 \(\mathcal J_Q\) 同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial identity 和局部 filtered-enstrophy 表示；在此之前不取正部或逐行绝对值。</p></div>`,
    String.raw`              <div class="route-step closed"><header><b>R0.71M</b><strong>精确 increment–projective bridge 与四行直接临界账本</strong></header><p>环带 Lamb 交换子具有精确二次速度增量表示；fixed-cell projective pairing 保留四行临界消费者。热包只排除这些绝对预算的普适能量嵌入，不是 NSE 解反例。<a href="/notes/r0-71m.html">研究笔记</a></p></div>
              <div class="route-step closed"><header><b>R0.71N</b><strong>正平方被 local-enstrophy acceleration 精确消去</strong></header><p>完整 \(B_{Q,t},d_{Q,t},Y_t\) 标量先写成 square–residual form；代入 \(B_Q=e_{Q,t}+\nu D_Q^\chi\) 后，acceleration 中的同一 pairing 产生 \(-\mathcal P_Q^\square\)，恰好消去表面的正平方。两个 \(z_Q&gt;0\) 的 smooth NSE initial jets 给出 \(\mathcal J_Q\) 双号，但不是时间区间符号定理。<a href="/notes/r0-71n.html">研究笔记</a> <a href="/recap-r0-61-r0-71n.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71O</b><strong>soft denominator 与 \(d_Q=0\) 一侧 faces</strong></header><p>下一节仍留在 fixed cells，比较 hard components 与 \(\sqrt{d_Q+\varepsilon}\)，检查 \(\varepsilon\downarrow0\) 的 source measures 和 denominator-zero 一侧 faces；暂不进入 refresh 或 moving cutoffs。</p></div>`,
  );
  litEdit.replace(
    '<h3>R0.71M 关闭了什么，R0.71N 只检查什么</h3>',
    '<h3>R0.71N 关闭了什么，R0.71O 只检查什么</h3>',
  );
  litEdit.replace(
    '<p>R0.71M 没有把“增量交换子”当作自动支付。它先证明 exact increment identity，再把 projective pairing 完整移过固定 cutoff。直接 Cauchy 后出现四行临界消费者，其中 differentiated commutator 没有可直接使用的上频率支撑；热包又说明所测试的绝对临界预算不由能量类普适给出。这是 checked direct-route boundary，不是一般 signed NSE no-go。R0.71N 只检查完整标量内是否还有第二次精确融合，并继续用下面六条筛选。</p>',
    '<p>R0.71N 没有把完成平方后的非负项当作自动耗散。完整时间导数与局部 filtered enstrophy 代回后，同一平方在 acceleration 中以负号出现并精确消去；最终只剩临界 signed second jet。这关闭的是一个 fixed-cell 代数候选，不是一般 signed NSE no-go。R0.71O 只检查 hard/soft denominator 极限与一侧 face measure，并继续用下面六条筛选。</p>',
  );
  litEdit.replace(
    '<div class="boundary"><strong>R0.71M 的一手文献边界</strong><p><a href="https://web.math.princeton.edu/~weinan/papers/misc1.pdf">Constantin–E–Titi</a>, <a href="https://archive.numdam.org/item/SEDP_1999-2000____A13_0/">Duchon–Robert</a> 与 <a href="https://arxiv.org/abs/0704.0759">Cheskidov–Constantin–Friedlander–Shvydkoy</a> 给出能量通量的 increment/Besov 结构； <a href="https://arxiv.org/abs/physics/0606159">Eyink</a> 给出邻近的 filtered vortex-force 与 stress-divergence 公式； <a href="https://arxiv.org/abs/2606.27560v1">Yu 2026</a> 控制 derivative-compatible localized paired work，并在完整无权闭合中保留额外 summability 输入。它们都不等同于本站带局部 curl 分母的 fixed-cell projective tangent。限定检索未找到从 Leray energy 单独推出完整 pairing 与四行直接账本的定理；这不是不存在性、原创性或优先权结论。<a href="#ref-29">[29]</a></p></div>',
    String.raw`<div class="boundary"><strong>R0.71N 的一手文献边界</strong><p><a href="https://arxiv.org/abs/physics/0606159">Eyink</a> 给出 filtered vortex force 与 filtered enstrophy；<a href="https://arxiv.org/abs/1107.0058">Dascaliuc–Grujić</a> 和 <a href="https://arxiv.org/abs/1108.1165">Tao</a> 给出严谨 local-enstrophy cutoff ledger；<a href="https://arxiv.org/abs/chao-dyn/9709003">Galanti–Gibbon–Heritage</a> 给出单位涡量方向的切投影方程；<a href="https://arxiv.org/abs/2606.27560v1">Yu 2026 预印本</a>是已查到最邻近的 filtered-vorticity/local-cutoff 账本。它们都没有本站固定单元的 cutoff–curl denominator 与 \(B_Q/\sqrt{Yd_Q}\) 完整时间演化。限定检索未找到同时保留 \(B_{Q,t},d_{Q,t},Y_t\) 的直接来源；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  );
  litEdit.replace('文献综述 v0.98 · 2026-08-26', '文献综述 v0.99 · 2026-08-26');
}

if (litEdit.count('<b>R0.71N</b>') !== 1) {
  throw new Error('literature: expected one R0.71N route row');
}
if (litEdit.count('开放接口 · R0.71O') !== 1) {
  throw new Error('literature: expected one R0.71O interface');
}
if (litEdit.count('bounded negative finding') !== 1) {
  throw new Error('literature: bounded-search boundary count is not one');
}
await writeFile(literaturePath, litEdit.value);

console.log(JSON.stringify({
  status: "ok",
  home: homePath,
  literature: literaturePath,
  homeR071nReleaseCards: homeEdit.count('data-release="r071n"'),
  homeR071nNoteLinks: homeEdit.count('href="/notes/r0-71n.html"'),
  routeNotes: 48,
  recapNodes: 78,
  publicNotes: 138,
  latest: "R0.71N",
  next: "R0.71O",
}, null, 2));
