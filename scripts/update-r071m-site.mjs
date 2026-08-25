import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) throw new Error(`${label}: expected one match, found ${count}: ${before.slice(0, 120)}`);
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) throw new Error(`${label}: expected at least ${minimum} matches, found ${count}: ${before}`);
      value = value.split(before).join(after);
    },
    replaceIfPresent(before, after) {
      const count = value.split(before).length - 1;
      if (count > 1) throw new Error(`${label}: expected at most one match, found ${count}: ${before}`);
      if (count === 1) value = value.replace(before, after);
      else if (!value.includes(after)) throw new Error(`${label}: neither old nor new text was found: ${before}`);
    },
    replaceBlock(start, end, after) {
      const count = value.split(start).length - 1;
      if (count !== 1) throw new Error(`${label}: expected one block start, found ${count}: ${start}`);
      const startIndex = value.indexOf(start);
      const endIndex = value.indexOf(end, startIndex + start.length);
      if (endIndex < 0) throw new Error(`${label}: block end not found: ${end}`);
      value = value.slice(0, startIndex) + after + value.slice(endIndex + end.length);
    },
    count(fragment) {
      return value.split(fragment).length - 1;
    },
    get value() { return value; },
  };
}

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
const homeIsCurrent = homeEdit.count('data-release="r071m"') === 1;
if (!homeIsCurrent) {
homeEdit.replace('<strong>v0.97</strong>网页版本', '<strong>v0.98</strong>网页版本');
homeEdit.replace('<strong>136</strong>公开研究笔记', '<strong>137</strong>公开研究笔记');
homeEdit.replace('<strong>R0.71L</strong>最新研究节点', '<strong>R0.71M</strong>最新研究节点');
homeEdit.replace('<strong>signed fused tangent / critical increment</strong>当前方向', '<strong>full scalar fusion / signed residual</strong>当前方向');
homeEdit.replace(
  '保留 fixed-cell signed fused tangent，检查尺度临界的 velocity-increment / commutator budget 及其 Carleson 求和能否由 Leray energy 推出。',
  String.raw`从完整标量 \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，检查是否存在第二次精确融合或明确的有符号余项。`,
);
homeEdit.replace('Research topology · R0.1–R0.71L', 'Research topology · R0.1–R0.71M');
homeEdit.replaceAll('/recap-r0-61-r0-71l.html', '/recap-r0-61-r0-71m.html');
homeEdit.replaceAll('/recap-r0-61-r0-71l.pdf', '/recap-r0-61-r0-71m.pdf');
homeEdit.replace('<span class="route-range">R0.69P–R0.71L</span>', '<span class="route-range">R0.69P–R0.71M</span>');
homeEdit.replace(
  '<h3>从有符号环带障碍走到 fixed-cell viscous fusion</h3>',
  '<h3>从有符号环带障碍走到 exact increment–projective bridge</h3>',
);
homeEdit.replace(
  '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–D 关闭纯投影符号律、无权尺度打包、静态有符号传播和仅靠物质热几何获得增益的设想。R0.71E–F 把拉伸压成 projected-Lamb 注入，证明 Leray 能量级热体积及其有界重叠局部化。R0.71G–I 把时间缺口收缩到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 与固定 aligned matched cells 上给出两阶 heat-payment gap。R0.71L 再证明 raw viscous collar 与 localized Laplacian commutator 必须精确融合，rowwise absolute collar 不是独立 coercive payment；真正开放的是 signed fused projective tangent 与它的 critical increment budget。</p>',
  '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 从恒定投影障碍走到 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–K 把时间缺口收缩到全壳正缺陷与 fixed matched-cell heat gap；R0.71L 又把 raw viscous collar 精确融合回 localized Laplacian row。R0.71M 现在给出 annular-filter Lamb commutator 的精确二次速度增量公式、完整 fixed-cell projective pairing 与四行临界直接账本。热包说明这些绝对临界预算不由能量类普适推出，但不排除 NSE 特有的 signed cancellation。</p>',
);
homeEdit.replace(
  '→ fixed matched-cell heat gap → exact viscous fusion</p>',
  '→ fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge</p>',
);
homeEdit.replace('<summary>展开 46 篇公开笔记</summary>', '<summary>展开 47 篇公开笔记</summary>');
homeEdit.replace('aria-label="R0.69P–R0.71L"', 'aria-label="R0.69P–R0.71M"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71l.html">R0.71L</a>\n',
  '                  <a class="milestone" href="/notes/r0-71l.html">R0.71L</a>\n                  <a class="milestone" href="/notes/r0-71m.html">R0.71M</a>\n',
);
homeEdit.replace('<span class="route-range">NEXT · R0.71M</span>', '<span class="route-range">NEXT · R0.71N</span>');
homeEdit.replace('<h3>Signed fused tangent 与 critical increment budget</h3>', '<h3>完整标量的第二次融合或 signed residual</h3>');
homeEdit.replace(
  '<p>我不进入 faces、refresh 或 moving cells，也不再把 raw collar 分开绝对化。下一步保留 signed fused tangent，把 nonlinear source 与 viscous mismatch 写成尺度临界的 velocity-increment / commutator ledger；额外的 annular 或 Carleson 假设必须逐项记录，并检查是否真由 Leray energy 推出。</p>',
  String.raw`<p>我继续停在 fixed cells，不再把四行直接账本逐项绝对化。R0.71N 从完整 \(\mathcal J_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial pairing 与局部 filtered-enstrophy 表示。结果可以是第二个精确标量融合，也可以是一个明确保留下来的有符号 residual；二者都不能预设。</p>`,
);
homeEdit.replace('累计回顾 R0.61–R0.71L · 2026-08-26', '累计回顾 R0.61–R0.71M · 2026-08-26');
homeEdit.replace('R0.60 recap 之后的累计回顾收录 76 个节点；全站现有 136 篇公开研究笔记', 'R0.60 recap 之后的累计回顾收录 77 个节点；全站现有 137 篇公开研究笔记');
homeEdit.replace(
  'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、投影热曲率、单边联合生成、全壳正缺陷、固定匹配小区与黏性融合。',
  'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、全壳正缺陷、固定匹配小区、黏性融合与增量—投影接口。',
);
homeEdit.replace(
  '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71J–K 排除了 frequency-only 与 fixed matched-cell heat-only 支付；R0.71L 证明 raw viscous collar 只是 fused viscous row 的坐标展开，rowwise absolute collar route 同样关闭。signed projective tangent、critical increment budget、faces 和无条件 weighted BV 仍未闭合。</p>',
  '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71M 把 critical increment bridge 压成 exact commutator、exact projective pairing 与四行充分账本；它同时证明标准能量类不普适嵌入所测试的绝对临界预算。这个函数空间分离不是 NSE 解反例，完整标量的 signed fusion、faces 和无条件 weighted BV 仍未闭合。</p>',
);
homeEdit.replace(
  '<p><strong style="color:var(--gold)">下一步 R0.71M：</strong>&nbsp;保留 signed fused tangent，测试尺度临界的 velocity-increment / commutator bridge 及其 Carleson 求和。</p>',
  '<p><strong style="color:var(--gold)">R0.71M 已完成：</strong>&nbsp;精确增量交换子与 fixed-cell pairing 已写出；当前直接插入产生四行临界充分账本，但不能由 Leray energy 普适支付。</p>',
);
}

const releaseCard = String.raw`

          <div class="task-one" id="r071m" data-release="r071m" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71M · 2026-08-26</p>
            <h3>精确增量—投影桥成立，四行直接临界账本仍是额外条件</h3>
            <p>
              对每个平移不变的标量环带滤波器，Lamb 交换子
              \[
                \mathcal R_j=T_j(u\times\omega)-u\times T_j\omega
              \]
              有精确的二次速度增量公式。resolved transport 与 \(\operatorname{curl}\mathcal R_j\) 单独都不必保持环带支撑；只有二者融合后的 \(G_j\) 恢复 band limitation。
            </p>
            <p>
              固定小区的完整 projective pairing 精确化为
              \[
                \langle P_QF_j,P_QM_Q\rangle
                =\int\chi_Q\left(G_j-\frac{B_Q}{d_Q}\operatorname{curl}C_Q\right)
                \cdot(G_j+\nu H_j).
              \]
              当前直接 Cauchy 产生 resolved transport、differentiated commutator、projective denominator geometry 与 viscous annular mismatch 四行尺度临界消费者；这是充分账本，不是必要条件。
            </p>
            <p>
              一个 \(L^2\)-归一化无散热包族保持精确一致的 kinetic-energy equality，同时 Yu 型四次缺陷、velocity square-Carleson mass 与 normalized projected-Lamb integral 分别按 \(r^{-2}\)、\(r^{-1}\)、\(r^{-1}\) 增长。这排除从标准能量类到这些绝对预算的普适函数空间嵌入；热包不是非线性 NSE 解。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节关闭的是“已知 increment defect + 当前 Cauchy/Bernstein split”这一条直接证明路线。它没有证明 increment 在逻辑上不能控制更小的 signed tangent，也没有得到继续性、奇性或全局正则性结论。</p>
            <p>
              <a href="/notes/r0-71m.html"><strong>阅读 R0.71M 研究笔记 →</strong></a> ·
              <a href="/notes/r0-71m.pdf">下载同步 PDF</a><br>
              <a href="/figures/r0-71m-increment-commutator.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071m">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071m_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071m-increment-commutator/fig-r071m-increment-commutator-boundary">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71m.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71m.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71N：</strong>&nbsp;从完整 \(\mathcal J_Q\) 同时展开三个时间导数，检查第二次精确标量融合或明确的 signed residual。</p>
          </div>`;
if (!homeIsCurrent) {
  homeEdit.replace(
    '          </div>\n        </section>\n\n      </article>',
    `          </div>${releaseCard}\n        </section>\n\n      </article>`,
  );
  homeEdit.replace('综述 v0.97 · 2026-08-26', '综述 v0.98 · 2026-08-26');
  homeEdit.replace('上次综述 v0.96 · 2026-08-26', '上次综述 v0.97 · 2026-08-26');
  homeEdit.replaceAll('/i18n-en.js?v=0.97', '/i18n-en.js?v=0.98');
}

homeEdit.replaceBlock(
  '<div class="summary-item"><strong>我目前关注</strong><span>',
  '</span></div>',
  String.raw`<div class="summary-item"><strong>我目前关注</strong><span>从完整标量 \(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，检查是否存在第二次精确融合或明确的有符号余项。</span></div>`,
);
homeEdit.replaceBlock(
  '            <article class="tree-node next">',
  '            </article>',
  String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71N</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>完整标量的第二次融合或 signed residual</h3>
              <p>我继续停在 fixed cells，不再把四行直接账本逐项绝对化。R0.71N 从完整 \(\mathcal J_Q\) 出发，同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial pairing 与局部 filtered-enstrophy 表示。结果可以是第二个精确标量融合，也可以是一个明确保留下来的有符号 residual；二者都不能预设。</p>
            </article>`,
);
const indentedReleaseStart = '          <div class="task-one" id="r071m" data-release="r071m" style="margin-top:2rem">';
const releaseStart = homeEdit.count(indentedReleaseStart) === 1
  ? indentedReleaseStart
  : '<div class="task-one" id="r071m" data-release="r071m" style="margin-top:2rem">';
homeEdit.replaceBlock(
  releaseStart,
  '          </div>',
  releaseCard.slice(releaseCard.indexOf(indentedReleaseStart)),
);
homeEdit.replaceIfPresent(
  '<p><strong style="color:var(--gold)">R0.71M 已完成：</strong>&nbsp;精确增量交换子与 fixed-cell pairing 已写出；当前直接插入产生四行临界充分账本，但不能由 Leray energy 普适支付。</p>',
  '<p><strong style="color:var(--gold)">R0.71M 已完成：</strong>&nbsp;精确增量交换子与 fixed-cell pairing 已写出；当前审计没有从 Leray energy 推出四行总账，所测试的三个绝对临界预算也不由能量类普适嵌入。</p>',
);
homeEdit.replaceIfPresent(
  '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71L 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
  '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71M 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
);

if (homeEdit.count('data-release="r071m"') !== 1) throw new Error('home: R0.71M release-card count is not one');
if (homeEdit.count('href="/notes/r0-71m.html"') !== 2) throw new Error('home: expected exactly two R0.71M note links');
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const litEdit = editor(await readFile(literaturePath, "utf8"), "literature");
const literatureIsCurrent = litEdit.count('<b>R0.71M</b>') === 1;
if (!literatureIsCurrent) {
litEdit.replaceAll('/i18n-en.js?v=0.97', '/i18n-en.js?v=0.98');
litEdit.replace('本站 R0.69P–R0.71L 只列为研究笔记', '本站 R0.69P–R0.71M 只列为研究笔记');
litEdit.replaceAll('/recap-r0-61-r0-71l.html', '/recap-r0-61-r0-71m.html');
litEdit.replace(
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在<a href="/recap-r0-61-r0-71m.html">累计回顾与 76 节索引</a>中。R0.69P–R0.71L 从有符号物理环带经过协方差框架、projected-Lamb 热体积、全壳正缺陷与 matched-cell heat gap，走到 fixed-cell viscous fusion。R0.71L 证明 raw viscous collar 与 localized Laplacian commutator 必须精确融合；单 eigenspace 中两个非零 expanded rows 可以完全相消。Leray 能量支付 weighted denominator mass，但当前 direct estimate 还需 angular ratio 与 normalized Lamb quotient，尚未从标准能量不等式推出。保留下来的结果都不是全局正则性结论。</p>',
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71m.html">累计回顾与 77 节索引</a>中。R0.69P–R0.71M 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap 与 viscous fusion，走到 exact increment–projective bridge。R0.71M 给出 annular-filter Lamb commutator 的精确二次速度增量公式和完整 fixed-cell pairing；当前直接绝对估计产生四行临界充分账本。热包排除从 Leray energy 到所测试绝对临界预算的普适嵌入，但不是 NSE 解反例。保留下来的结果都不是全局正则性结论。</p>',
);
litEdit.replace('<a href="/recap-r0-61-r0-71m.html#node-index">打开 76 节完整索引</a>', '<a href="/recap-r0-61-r0-71m.html#node-index">打开 77 节完整索引</a>');
litEdit.replace(
  String.raw`<div class="route-step closed"><header><b>R0.71L</b><strong>raw viscous collar 精确融合，rowwise absolute payment 关闭</strong></header><p>固定 cutoff 下，viscous collar 与 localized Laplacian commutator 精确融合为 \(\nu\mathsf A_Q(\Delta+\kappa^2)W_j\)。aligned cutoff–curl numerator 逐格为零，denominator 有双侧比较；Leray 能量支付 denominator mass，而当前 direct tangent estimate 尚未从该能量界推出。<a href="/notes/r0-71l.html">研究笔记</a> <a href="/recap-r0-61-r0-71m.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71M</b><strong>signed fused tangent 与 critical increment bridge</strong></header><p>下一节不进入 faces 或 moving cells，也不再逐行绝对化 raw collar；先把 fused tangent 写成尺度临界的 velocity-increment / commutator ledger，并检查 annular 或 Carleson 假设能否由 Leray energy 推出。</p></div>`,
  String.raw`<div class="route-step closed"><header><b>R0.71L</b><strong>raw viscous collar 精确融合，rowwise absolute payment 关闭</strong></header><p>固定 cutoff 下，viscous collar 与 localized Laplacian commutator 精确融合为 \(\nu\mathsf A_Q(\Delta+\kappa^2)W_j\)。aligned cutoff–curl numerator 逐格为零，denominator 有双侧比较；Leray 能量支付 denominator mass。<a href="/notes/r0-71l.html">研究笔记</a></p></div>
              <div class="route-step closed"><header><b>R0.71M</b><strong>精确 increment–projective bridge 与四行直接临界账本</strong></header><p>环带 Lamb 交换子具有精确二次速度增量表示；fixed-cell projective pairing 同时保留 resolved transport、differentiated commutator、projective denominator geometry 与 viscous annular mismatch。热包只排除这些绝对预算的普适能量嵌入，不是 NSE 解反例。<a href="/notes/r0-71m.html">研究笔记</a> <a href="/recap-r0-61-r0-71m.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71N</b><strong>完整标量的第二次融合或 signed residual</strong></header><p>下一节仍留在 fixed cells，从整个 \(\mathcal J_Q\) 同时保留 \(B_{Q,t}\)、\(d_{Q,t}\) 与 \(Y_t\)，再代入 radial identity 和局部 filtered-enstrophy 表示；在此之前不取正部或逐行绝对值。</p></div>`,
);
litEdit.replace('<h3>R0.71L 关闭了什么，R0.71M 只检查什么</h3>', '<h3>R0.71M 关闭了什么，R0.71N 只检查什么</h3>');
litEdit.replace(
  '<p>R0.71L 没有把 localization boundary 当作自动增益。它证明 raw collar 与 localized Laplacian commutator 是同一个 signed fused row 的展开；单独绝对化会丢掉 exact cancellation。标准能量能支付 denominator mass；当前 rowwise Cauchy–Young 推论仍留下局部分母的逆、angular condition number 与 normalized Lamb quotient。这是 direct-estimate boundary，不是一般 Leray-level no-go。R0.71M 只检查一个尺度临界的 signed increment–commutator bridge，并继续用下面六条筛选。</p>',
  '<p>R0.71M 没有把“增量交换子”当作自动支付。它先证明 exact increment identity，再把 projective pairing 完整移过固定 cutoff。直接 Cauchy 后出现四行临界消费者，其中 differentiated commutator 没有可直接使用的上频率支撑；热包又说明所测试的绝对临界预算不由能量类普适给出。这是 checked direct-route boundary，不是一般 signed NSE no-go。R0.71N 只检查完整标量内是否还有第二次精确融合，并继续用下面六条筛选。</p>',
);
litEdit.replace(
  '<div class="boundary"><strong>R0.71L 的一手文献边界</strong><p><a href="https://doi.org/10.1002/cpa.3160350604">CKN</a>、<a href="https://arxiv.org/abs/1101.2193">Dascaliuc–Grujić</a> 与 <a href="https://arxiv.org/abs/1108.1165">Tao</a>提供 scalar local-energy/enstrophy cutoff 机制；<a href="https://arxiv.org/abs/1502.01258">Leitmeyer</a> 的 enstrophy cascade 需要 coherence、Kraichnan/Morrey 与 modulation 输入；<a href="https://arxiv.org/abs/2606.27560v1">Yu 2026</a> 的邻近账本使用 solution-adapted adjoint cutoff、increment defect、Carleson 与 shell summability。限定检索没有找到 fixed matched cells 上完整 fused projective tangent 的 Leray-only 定理，也没有找到同构的已发表 NSE 反例。这只是一项文献边界记录，不是原创性或优先权结论。<a href="#ref-11">[11]</a><a href="#ref-29">[29]</a><a href="#ref-49">[49]</a><a href="#ref-50">[50]</a><a href="#ref-51">[51]</a></p></div>',
  '<div class="boundary"><strong>R0.71M 的一手文献边界</strong><p><a href="https://web.math.princeton.edu/~weinan/papers/misc1.pdf">Constantin–E–Titi</a>, <a href="https://archive.numdam.org/item/SEDP_1999-2000____A13_0/">Duchon–Robert</a> 与 <a href="https://arxiv.org/abs/0704.0759">Cheskidov–Constantin–Friedlander–Shvydkoy</a> 给出能量通量的 increment/Besov 结构； <a href="https://arxiv.org/abs/physics/0606159">Eyink</a> 给出邻近的 filtered vortex-force 与 stress-divergence 公式； <a href="https://arxiv.org/abs/2606.27560v1">Yu 2026</a> 控制 derivative-compatible localized paired work，并在完整无权闭合中保留额外 summability 输入。它们都不等同于本站带局部 curl 分母的 fixed-cell projective tangent。限定检索未找到从 Leray energy 单独推出完整 pairing 与四行直接账本的定理；这不是不存在性、原创性或优先权结论。<a href="#ref-29">[29]</a></p></div>',
);
litEdit.replace('文献综述 v0.97 · 2026-08-26', '文献综述 v0.98 · 2026-08-26');
}

litEdit.replaceIfPresent(
  '<div class="boundary"><strong>R0.71M 的一手文献边界</strong><p><a href="https://web.math.princeton.edu/~weinan/papers/misc1.pdf">Constantin–E–Titi</a>、Duchon–Robert 与 <a href="https://arxiv.org/abs/0704.0759">Cheskidov–Constantin–Friedlander–Shvydkoy</a>给出能量通量的 increment/Besov 结构；<a href="https://arxiv.org/abs/physics/0606159">Eyink</a> 给出邻近的 filtered vortex-force 与 stress-divergence 公式；<a href="https://arxiv.org/abs/2606.27560v1">Yu 2026</a>控制 derivative-compatible localized paired work，并在完整无权闭合中保留额外 summability 输入。它们都不等同于本站带局部 curl 分母的 fixed-cell projective tangent。限定检索未找到从 Leray energy 单独推出完整 pairing 与四行直接账本的定理；这不是不存在性、原创性或优先权结论。<a href="#ref-19">[19]</a><a href="#ref-20">[20]</a><a href="#ref-29">[29]</a></p></div>',
  '<div class="boundary"><strong>R0.71M 的一手文献边界</strong><p><a href="https://web.math.princeton.edu/~weinan/papers/misc1.pdf">Constantin–E–Titi</a>, <a href="https://archive.numdam.org/item/SEDP_1999-2000____A13_0/">Duchon–Robert</a> 与 <a href="https://arxiv.org/abs/0704.0759">Cheskidov–Constantin–Friedlander–Shvydkoy</a> 给出能量通量的 increment/Besov 结构； <a href="https://arxiv.org/abs/physics/0606159">Eyink</a> 给出邻近的 filtered vortex-force 与 stress-divergence 公式； <a href="https://arxiv.org/abs/2606.27560v1">Yu 2026</a> 控制 derivative-compatible localized paired work，并在完整无权闭合中保留额外 summability 输入。它们都不等同于本站带局部 curl 分母的 fixed-cell projective tangent。限定检索未找到从 Leray energy 单独推出完整 pairing 与四行直接账本的定理；这不是不存在性、原创性或优先权结论。<a href="#ref-29">[29]</a></p></div>',
);

if (litEdit.count('<b>R0.71M</b>') !== 1) throw new Error('literature: expected one R0.71M route row');
if (litEdit.count('开放接口 · R0.71N') !== 1) throw new Error('literature: expected one R0.71N interface');
await writeFile(literaturePath, litEdit.value);

console.log(JSON.stringify({
  status: "ok",
  home: homePath,
  literature: literaturePath,
  homeR071mReleaseCards: homeEdit.count('data-release="r071m"'),
  homeR071mNoteLinks: homeEdit.count('href="/notes/r0-71m.html"'),
  routeNotes: 47,
  publicNotes: 137,
  latest: "R0.71M",
  next: "R0.71N",
}, null, 2));
