import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) throw new Error(`${label}: expected one match, found ${count}: ${before.slice(0, 100)}`);
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) throw new Error(`${label}: expected at least ${minimum} matches, found ${count}: ${before}`);
      value = value.split(before).join(after);
    },
    get value() { return value; },
  };
}

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
homeEdit.replace('<strong>v0.96</strong>网页版本', '<strong>v0.97</strong>网页版本');
homeEdit.replace('<strong>135</strong>公开研究笔记', '<strong>136</strong>公开研究笔记');
homeEdit.replace('<strong>R0.71K</strong>最新研究节点', '<strong>R0.71L</strong>最新研究节点');
homeEdit.replace('<strong>fixed-cell collar / tangent budget</strong>当前方向', '<strong>signed fused tangent / critical increment</strong>当前方向');
homeEdit.replace(
  '在固定 matched spatial partition 上分离 viscous collar 与 projective tangent，检查它们的 weighted absolute budget 能否由现有 Leray-level 量非循环地支付。',
  '保留 fixed-cell signed fused tangent，检查尺度临界的 velocity-increment / commutator budget 及其 Carleson 求和能否由 Leray energy 推出。',
);
homeEdit.replace('Research topology · R0.1–R0.71K', 'Research topology · R0.1–R0.71L');
homeEdit.replace('<a href="/recap-r0-61-r0-71k.html">阅读 R0.60 之后的累计回顾</a>', '<a href="/recap-r0-61-r0-71l.html">阅读 R0.60 之后的累计回顾</a>');
homeEdit.replace('<span class="route-range">R0.69P–R0.71K</span>', '<span class="route-range">R0.69P–R0.71L</span>');
homeEdit.replace(
  '<h3>从有符号环带障碍走到固定 matched-cell collar 边界</h3>',
  '<h3>从有符号环带障碍走到 fixed-cell viscous fusion</h3>',
);
homeEdit.replace(
  '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–D 关闭纯投影符号律、无权尺度打包、静态有符号传播和仅靠物质热几何获得增益的设想。R0.71E–F 把拉伸压成 projected-Lamb 注入，证明 Leray 能量级热体积及其有界重叠局部化。R0.71G–I 把时间缺口收缩到入口、单边联合生成与 faces。R0.71J 在完整 broad parent frame 上给出全局光滑 2D3C 的 \\(K^2\\) heat-payment gap；R0.71K 又证明一组预先固定的 aligned matched partitions 仍保留同一个两阶缺口。frequency-only 与 fixed matched-cell heat-only 支付已关闭；viscous collar、projective tangent 和完整 face-paid BV 仍开放。</p>',
  '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–D 关闭纯投影符号律、无权尺度打包、静态有符号传播和仅靠物质热几何获得增益的设想。R0.71E–F 把拉伸压成 projected-Lamb 注入，证明 Leray 能量级热体积及其有界重叠局部化。R0.71G–I 把时间缺口收缩到入口、单边联合生成与 faces。R0.71J–K 在完整 broad parent frame 与固定 aligned matched cells 上给出两阶 heat-payment gap。R0.71L 再证明 raw viscous collar 与 localized Laplacian commutator 必须精确融合，rowwise absolute collar 不是独立 coercive payment；真正开放的是 signed fused projective tangent 与它的 critical increment budget。</p>',
);
homeEdit.replace(
  '→ fixed matched-cell heat gap</p>',
  '→ fixed matched-cell heat gap → exact viscous fusion</p>',
);
homeEdit.replace('<summary>展开 45 篇公开笔记</summary>', '<summary>展开 46 篇公开笔记</summary>');
homeEdit.replace('aria-label="R0.69P–R0.71K"', 'aria-label="R0.69P–R0.71L"');
homeEdit.replace(
  '                  <a class="milestone" href="/notes/r0-71k.html">R0.71K</a>\n',
  '                  <a class="milestone" href="/notes/r0-71k.html">R0.71K</a>\n                  <a class="milestone" href="/notes/r0-71l.html">R0.71L</a>\n',
);
homeEdit.replace('<span class="route-range">NEXT · R0.71L</span>', '<span class="route-range">NEXT · R0.71M</span>');
homeEdit.replace('<h3>Fixed-cell collar 与 tangent budget</h3>', '<h3>Signed fused tangent 与 critical increment budget</h3>');
homeEdit.replace(
  '<p>我先停在固定分割，不进入 moving cells、refresh 或无限 soft limit；把 viscous collar 与 projective tangent 从联合源中分离出来，检查 weighted absolute budget 是否能由现有 Leray-level NSE 量控制，同时保持 radial–tangent cancellation。只有得到独立、非循环的支付，才继续进入 faces 和 moving partitions。</p>',
  '<p>我不进入 faces、refresh 或 moving cells，也不再把 raw collar 分开绝对化。下一步保留 signed fused tangent，把 nonlinear source 与 viscous mismatch 写成尺度临界的 velocity-increment / commutator ledger；额外的 annular 或 Carleson 假设必须逐项记录，并检查是否真由 Leray energy 推出。</p>',
);
homeEdit.replace('累计回顾 R0.61–R0.71K · 2026-08-26', '累计回顾 R0.61–R0.71L · 2026-08-26');
homeEdit.replace('R0.60 recap 之后的累计回顾收录 75 个节点；全站现有 135 篇公开研究笔记', 'R0.60 recap 之后的累计回顾收录 76 个节点；全站现有 136 篇公开研究笔记');
homeEdit.replace(
  'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、投影热曲率、单边联合生成、全壳正缺陷与固定匹配小区。',
  'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、投影热曲率、单边联合生成、全壳正缺陷、固定匹配小区与黏性融合。',
);
homeEdit.replace(
  '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71J 证明逐壳取正部以后只留下时间端点 telescope 与两个非负缺陷；R0.71K 再证明一组固定 aligned matched partitions 仍保留 \\(K^2\\) heat-payment gap。frequency-only 与 fixed matched-cell heat-only 支付已关闭，viscous collar、projective tangent、faces 和无条件 weighted BV 仍未闭合。</p>',
  '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71J–K 排除了 frequency-only 与 fixed matched-cell heat-only 支付；R0.71L 证明 raw viscous collar 只是 fused viscous row 的坐标展开，rowwise absolute collar route 同样关闭。signed projective tangent、critical increment budget、faces 和无条件 weighted BV 仍未闭合。</p>',
);
homeEdit.replace('<a href="/recap-r0-61-r0-71k.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-71k.pdf">下载同步 PDF</a>', '<a href="/recap-r0-61-r0-71l.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-71l.pdf">下载同步 PDF</a>');
homeEdit.replace(
  '<p><strong style="color:var(--gold)">下一步 R0.71L：</strong>&nbsp;留在固定分割上分离 viscous collar 与 projective tangent，检查 weighted absolute budget 能否由现有 Leray-level NSE 量非循环地控制。</p>',
  '<p><strong style="color:var(--gold)">R0.71L 已完成：</strong>&nbsp;raw viscous collar 与 localized Laplacian commutator 精确融合；rowwise absolute collar 不是独立支付，signed projective tangent 仍开放。</p>',
);

const releaseCard = `

          <div class="task-one" id="r071l" data-release="r071l" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71L · 2026-08-26</p>
            <h3>黏性 collar 精确融合，投影切向的当前直接估计仍未闭合</h3>
            <p>
              固定 cutoff 下，完整 localized-vorticity row 满足
              \\[
                M_Q=\\mathsf A_Q\\left[\\nu(\\Delta+\\kappa^2)W_j+\\mathcal G_j\\right].
              \\]
              因而 raw viscous collar 与 localized Laplacian commutator 不是两个独立源。单 Laplace eigenspace 例子中，两个 expanded rows 分别非零却逐点完全相消；先分开取绝对值会制造 representation-dependent cost。
            </p>
            <p>
              normalization 与 projective row 也精确重组为
              \\[
                \\mathcal J_Q=z_{Q,t}+\\nu\\kappa^2z_Q.
              \\]
              aligned witness 还满足 cutoff–curl numerator 逐格为零，以及 \\(N^{-1}D_j\\le D_{\\rm loc}\\le C_{\\rm part}D_j\\)。Leray 能量支付 weighted denominator mass；当前 direct tangent Cauchy 还引入 angular condition number 与 normalized projected-Lamb quotient，尚未从标准能量不等式推出。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节关闭 bounded overlap + Bernstein + Leray energy + rowwise absolute values 这一条 fixed-cell collar 路线。它不排除 signed fused cancellation、额外临界 increment/Carleson 输入、faces、moving cells、继续性或全局正则性。</p>
            <p>
              <a href="/notes/r0-71l.html"><strong>阅读 R0.71L 研究笔记 →</strong></a> ·
              <a href="/notes/r0-71l.pdf">下载同步 PDF</a><br>
              <a href="/figures/r0-71l-viscous-fusion.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071l">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071l_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071l-viscous-fusion/fig-r071l-viscous-fusion-gap">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71l.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71l.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71M：</strong>&nbsp;保留 signed fused tangent，测试尺度临界的 velocity-increment / commutator bridge 及其 Carleson 求和。</p>
          </div>`;
homeEdit.replace(
  '          </div>\n        </section>\n\n      </article>',
  `          </div>${releaseCard}\n        </section>\n\n      </article>`,
);
homeEdit.replace('综述 v0.96 · 2026-08-26', '综述 v0.97 · 2026-08-26');
homeEdit.replace('上次综述 v0.95 · 2026-08-26', '上次综述 v0.96 · 2026-08-26');
homeEdit.replaceAll('/i18n-en.js?v=0.96', '/i18n-en.js?v=0.97');
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const litEdit = editor(await readFile(literaturePath, "utf8"), "literature");
litEdit.replaceAll('/i18n-en.js?v=0.96', '/i18n-en.js?v=0.97');
litEdit.replace('本站 R0.69P–R0.71K 只列为研究笔记', '本站 R0.69P–R0.71L 只列为研究笔记');
litEdit.replace(
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在<a href="/recap-r0-61-r0-71k.html">累计回顾与 75 节索引</a>中。R0.69P–R0.71K 从有符号物理环带经过协方差框架、响应距离和 signed refinement，走到 projected-Lamb 热体积、局部热打包、projective heat curvature、联合抛物失配、all-shell positive defect 与 matched-cell 局部化。R0.71K 证明：对一个固定、对齐、尺度协变的光滑 partition，所选父壳在 \\(K^3\\) 个 matched cells 上精确等分；局部正生成仍为 \\(K^{-2}\\) 量级，而同一 heat/support payment 至多为 \\((\\nu K^4)^{-1}\\) 量级。因此，这个固定 partition 下的 heat-only closure 已被关闭。viscous collar 与 projective tangent 仍处在正生成的同一主阶，尚未得到 Leray 级支付。保留下来的结果都不是全局正则性结论。</p>',
  '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在<a href="/recap-r0-61-r0-71l.html">累计回顾与 76 节索引</a>中。R0.69P–R0.71L 从有符号物理环带经过协方差框架、projected-Lamb 热体积、全壳正缺陷与 matched-cell heat gap，走到 fixed-cell viscous fusion。R0.71L 证明 raw viscous collar 与 localized Laplacian commutator 必须精确融合；单 eigenspace 中两个非零 expanded rows 可以完全相消。Leray 能量支付 weighted denominator mass，但当前 direct estimate 还需 angular ratio 与 normalized Lamb quotient，尚未从标准能量不等式推出。保留下来的结果都不是全局正则性结论。</p>',
);
litEdit.replace('<a href="/recap-r0-61-r0-71k.html#node-index">打开 75 节完整索引</a>', '<a href="/recap-r0-61-r0-71l.html#node-index">打开 76 节完整索引</a>');
litEdit.replace(
  '<div class="route-step closed"><header><b>R0.71K</b><strong>固定 aligned matched cells 精确等分，heat-only closure 仍有两阶缺口</strong></header><p>一个固定、对齐、尺度协变的光滑 partition 把所选父壳精确分到 \\(K^3\\) 个 matched cells：每格的 signed work 与局部分母都等于相应总量的 \\(K^{-3}\\)。求和后的正生成保留 \\(K^{-2}\\) 下界，而 heat/support payment 至多为 \\((\\nu K^4)^{-1}\\)。因此这一个固定 partition 不产生新的 coercive payment；结论不覆盖任意或移动 partition，也不支付 viscous collar、cutoff–curl、denominator collar 或 projective tangent。<a href="/notes/r0-71k.html">研究笔记</a> <a href="/recap-r0-61-r0-71k.html">当前累计回顾</a></p></div>\n              <div class="route-step pause"><header><b>开放接口 · R0.71L</b><strong>逐项检查 collar 与 tangent payment</strong></header><p>下一节不再测试同一 heat/support 端点，而是保留 cutoff–curl、denominator collar、viscous collar 与 projective tangent 的完整符号和尺度，检查其中是否存在可由 Leray 级输入支付的 coercive 组合。viscous collar 的加权总量与正生成同为 \\(K^{-2}\\) 主阶，不能先验忽略。</p></div>',
  '<div class="route-step closed"><header><b>R0.71K</b><strong>固定 aligned matched cells 精确等分，heat-only closure 仍有两阶缺口</strong></header><p>一个固定、对齐、尺度协变的光滑 partition 把所选父壳精确分到 \\(K^3\\) 个 matched cells：求和后的正生成保留 \\(K^{-2}\\) 下界，而 heat/support payment 至多为 \\((\\nu K^4)^{-1}\\)。因此这一固定 partition 不产生新的 heat coercivity。<a href="/notes/r0-71k.html">研究笔记</a></p></div>\n              <div class="route-step closed"><header><b>R0.71L</b><strong>raw viscous collar 精确融合，rowwise absolute payment 关闭</strong></header><p>固定 cutoff 下，viscous collar 与 localized Laplacian commutator 精确融合为 \\(\\nu\\mathsf A_Q(\\Delta+\\kappa^2)W_j\\)。aligned cutoff–curl numerator 逐格为零，denominator 有双侧比较；Leray 能量支付 denominator mass，而当前 direct tangent estimate 尚未从该能量界推出。<a href="/notes/r0-71l.html">研究笔记</a> <a href="/recap-r0-61-r0-71l.html">当前累计回顾</a></p></div>\n              <div class="route-step pause"><header><b>开放接口 · R0.71M</b><strong>signed fused tangent 与 critical increment bridge</strong></header><p>下一节不进入 faces 或 moving cells，也不再逐行绝对化 raw collar；先把 fused tangent 写成尺度临界的 velocity-increment / commutator ledger，并检查 annular 或 Carleson 假设能否由 Leray energy 推出。</p></div>',
);
litEdit.replace('<h3>R0.71K 得到了什么，R0.71L 只检查什么</h3>', '<h3>R0.71L 关闭了什么，R0.71M 只检查什么</h3>');
litEdit.replace(
  '<p>R0.71K 没有把 localization boundary 当作自动增益。对所选的固定 aligned partition，平移对称性给出逐格精确等分，入口逐格为零，所选窗口内分母为正，并且没有 denominator face 或 refresh atom。这个模型把 heat-only 支付排除得很干净，但也明确留下边界：cutoff–curl、denominator collar、viscous collar 与 projective tangent 没有被同一证书支付。R0.71L 将只检查这些同阶项能否形成可结算组合，并继续用下面六条筛选。</p>',
  '<p>R0.71L 没有把 localization boundary 当作自动增益。它证明 raw collar 与 localized Laplacian commutator 是同一个 signed fused row 的展开；单独绝对化会丢掉 exact cancellation。标准能量能支付 denominator mass；当前 rowwise Cauchy–Young 推论仍留下局部分母的逆、angular condition number 与 normalized Lamb quotient。这是 direct-estimate boundary，不是一般 Leray-level no-go。R0.71M 只检查一个尺度临界的 signed increment–commutator bridge，并继续用下面六条筛选。</p>',
);
litEdit.replace(
  '<div class="boundary"><strong>R0.71K 的一手文献边界</strong><p><a href="https://arxiv.org/abs/1101.2193">Dascaliuc–Grujić</a> 与 <a href="https://arxiv.org/abs/1502.01258">Leitmeyer</a> 已用 refined covers 在物理尺度组织局部通量与级联；<a href="https://arxiv.org/abs/1108.1165">Tao</a> 已系统使用局部能量、移动 cutoff 与支撑 collar 型误差；<a href="https://arxiv.org/abs/2606.27560v1">Yu 2026</a> 明确保留 filtered-vorticity 账本中的 localization residual。它们说明 partition、cutoff 与 collar 账本本身不是本站可声称的新颖点，也不会自动提供正的 coercive contribution。本站新增的限定检查是这个显式 2D3C 家族在一个固定 aligned matched partition 上的精确等分及其两阶 heat/support 缺口。限定检索没有找到同构陈述，但这只是一项文献边界记录，不是原创性或优先权结论。<a href="#ref-29">[29]</a><a href="#ref-46">[46]</a><a href="#ref-49">[49]</a><a href="#ref-50">[50]</a><a href="#ref-51">[51]</a></p></div>',
  '<div class="boundary"><strong>R0.71L 的一手文献边界</strong><p><a href="https://doi.org/10.1002/cpa.3160350604">CKN</a>、<a href="https://arxiv.org/abs/1101.2193">Dascaliuc–Grujić</a> 与 <a href="https://arxiv.org/abs/1108.1165">Tao</a>提供 scalar local-energy/enstrophy cutoff 机制；<a href="https://arxiv.org/abs/1502.01258">Leitmeyer</a> 的 enstrophy cascade 需要 coherence、Kraichnan/Morrey 与 modulation 输入；<a href="https://arxiv.org/abs/2606.27560v1">Yu 2026</a> 的邻近账本使用 solution-adapted adjoint cutoff、increment defect、Carleson 与 shell summability。限定检索没有找到 fixed matched cells 上完整 fused projective tangent 的 Leray-only 定理，也没有找到同构的已发表 NSE 反例。这只是一项文献边界记录，不是原创性或优先权结论。<a href="#ref-11">[11]</a><a href="#ref-29">[29]</a><a href="#ref-49">[49]</a><a href="#ref-50">[50]</a><a href="#ref-51">[51]</a></p></div>',
);
litEdit.replace('文献综述 v0.96 · 2026-08-26', '文献综述 v0.97 · 2026-08-26');
await writeFile(literaturePath, litEdit.value);

console.log(JSON.stringify({ home: homePath, literature: literaturePath }, null, 2));
