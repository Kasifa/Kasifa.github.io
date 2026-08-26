import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) throw new Error(`${label}: expected one match, found ${count}: ${before.slice(0, 160)}`);
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) throw new Error(`${label}: expected at least ${minimum} matches, found ${count}: ${before}`);
      value = value.split(before).join(after);
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
    get value() {
      return value;
    },
  };
}

const releaseCard = String.raw`

          <div class="task-one" id="r071q" data-release="r071q" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71Q · 2026-08-26</p>
            <h3>Jensen 给出有限条件计数，解析性本身仍不支付时间进入打包</h3>
            <p>
              Temam 的复时间瓣包含显式双侧圆盘。对固定有限截断和紧经典窗口，Hilbert 值 Jensen 公式与 finite ownership cover 给出
              \[
                \mathsf S_{\Lambda,+}(K)
                \le \sum_m H_m\sum_{\alpha\in\Lambda^*}
                \left\lfloor\frac{\log(M_\alpha/a_{\alpha m})}{\log2}\right\rfloor.
              \]
              这是严格的有限条件定理；右端不是 Leray data 的已知函数。
            </p>
            <p>
              三个显式解析族分别隔离缺口：有限 Blaschke 乘积证明固定半径与复上界允许任意多正进入，锚点对数与零点数同阶；线性分量族证明零点并集必须支付截断数；sine-square 族证明局部半径比、增长和相对锚点一致时，ownership cover 数仍可增长。
            </p>
            <p>
              加权目标还有独立的点态账本 \(H_m=\sup_{K_m}\mathcal H\)。Temam 尺度按 \((1+\sup\|u\|_{H^1}^2)^{-2}\) 缩小；若该尺度在潜在奇点端点一致，本身已经是 continuation-level input。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节分类并停止“仅靠时间解析性与复域上界”的直接路线；没有给出 uniform NSE zero count、无限 frame、Leray 极限、继续性或全局正则性结论。反例族不是 NSE 重复进入轨道。</p>
            <p>
              <a href="/notes/r0-71q.html"><strong>阅读 R0.71Q 研究笔记 →</strong></a> ·
              <a href="/notes/r0-71q.pdf">下载同步 PDF</a><br>
              <a href="/figures/r0-71q-jensen-window-audit.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071q">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071q_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071q_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071q_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071q_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71q.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71q.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71R：</strong>&nbsp;在 componentwise positive parts 之前回到 signed precursor/source，检查 NSE-specific parabolic incidence 或 Carleson packing law；候选必须同时通过 sequential path、Blaschke anchor 与 all-observable union 压力测试。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
const homeIsCurrent = homeEdit.count('data-release="r071q"') === 1;

if (!homeIsCurrent) {
  homeEdit.replace('<strong>v1.01</strong>网页版本', '<strong>v1.02</strong>网页版本');
  homeEdit.replace('<strong>140</strong>公开研究笔记', '<strong>141</strong>公开研究笔记');
  homeEdit.replace('<strong>R0.71P</strong>最新研究节点', '<strong>R0.71Q</strong>最新研究节点');
  homeEdit.replace('<strong>quantitative complex-time zero packing</strong>当前方向', '<strong>NSE-specific parabolic incidence packing</strong>当前方向');
  homeEdit.replace(
    '<div class="summary-item"><strong>我目前关注</strong><span>把 complex-time Jensen zero count 放进 parabolic windows，逐项核对 analytic radius、growth、projection anchor 与窗口 covering 是否能从 NSE 预算支付。</span></div>',
    '<div class="summary-item"><strong>我目前关注</strong><span>在逐分量正部之前回到 signed precursor/source，检查 NSE 动力学是否强迫 parabolic incidence 或 Carleson packing；不再把定性时间解析性当作 uniform count。</span></div>',
  );
  homeEdit.replace('Research topology · R0.1–R0.71P', 'Research topology · R0.1–R0.71Q');
  homeEdit.replaceAll('/recap-r0-61-r0-71p.html', '/recap-r0-61-r0-71q.html');
  homeEdit.replaceAll('/recap-r0-61-r0-71p.pdf', '/recap-r0-61-r0-71q.pdf');
  homeEdit.replace('<span class="route-range">R0.69P–R0.71P</span>', '<span class="route-range">R0.69P–R0.71Q</span>');
  homeEdit.replace(
    '<h3>从有符号环带障碍走到 positive-entry temporal-packing boundary</h3>',
    '<h3>从有符号环带障碍走到 complex-time packing method boundary</h3>',
  );
  homeEdit.replace(
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–O 依次核对 residence、matched-cell heat gap、viscous fusion、increment bridge、signed second jet 与 soft denominator faces。R0.71P 再证明同刻正进入可由空间平方和支付，而完整累积仍需要 distinct entry-time packing。</p>',
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–P 依次核对 residence、matched-cell heat gap、viscous fusion、signed second jet、soft denominator faces 与同刻 spatial batching。R0.71Q 给出有限 Jensen window theorem，并证明 anchor、component union、cover 与 pointwise envelope 仍是未支付账本。</p>',
  );
  homeEdit.replace(
    '→ spatial entry batching → temporal-packing boundary</p>',
    '→ spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary</p>',
  );
  homeEdit.replace('<summary>展开 50 篇公开笔记</summary>', '<summary>展开 51 篇公开笔记</summary>');
  homeEdit.replace('aria-label="R0.69P–R0.71P"', 'aria-label="R0.69P–R0.71Q"');
  homeEdit.replace(
    '                  <a class="milestone" href="/notes/r0-71p.html">R0.71P</a>\n',
    '                  <a class="milestone" href="/notes/r0-71p.html">R0.71P</a>\n                  <a class="milestone" href="/notes/r0-71q.html">R0.71Q</a>\n',
  );
  homeEdit.replaceBlock(
    '            <article class="tree-node next">',
    '            </article>',
    String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71R</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>NSE-specific parabolic incidence / Carleson packing</h3>
              <p>我回到 componentwise positive parts 之前的 signed precursor/source，检查 PDE 动力学能否耦合不同 observable 的 entry events；候选必须显式支付 anchor、cover、union 与 event-weight 账本。</p>
            </article>`,
  );
  homeEdit.replace('累计回顾 R0.61–R0.71P · 2026-08-26', '累计回顾 R0.61–R0.71Q · 2026-08-26');
  homeEdit.replace(
    'R0.60 recap 之后的累计回顾收录 80 个节点；全站现有 140 篇公开研究笔记',
    'R0.60 recap 之后的累计回顾收录 81 个节点；全站现有 141 篇公开研究笔记',
  );
  homeEdit.replace(
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、soft-denominator faces 与 positive-entry temporal packing。R0.70A–R0.71P 共 42 个完成版本。',
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、positive-entry temporal packing 与 complex-time Jensen method audit。R0.70A–R0.71Q 共 43 个完成版本。',
  );
  homeEdit.replace(
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71P 删除了同刻空间 cell multiplicity，并证明正进入 atoms 本身不能直接做 signed shell–cell cancellation；未闭合的是 distinct entry-time counting measure 的 uniform NSE packing。</p>',
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71Q 给出固定有限截断上的条件 Jensen bound，并以精确反例隔离 anchor、component-union 与 cover taxes；它们和点态 batch envelope 尚不能由 Leray 预算统一支付。</p>',
  );
  homeEdit.replace(
    String.raw`<p><strong style="color:var(--gold)">下一步 R0.71Q：</strong>&nbsp;把 quantitative complex-time Jensen bound 放进 parabolic windows，显式检查 analytic radius、complex growth、projection anchor 与窗口覆盖是否能从 NSE 预算支付。</p>`,
    String.raw`<p><strong style="color:var(--gold)">R0.71Q 已完成：</strong>&nbsp;有限 Jensen window theorem 成立；解析半径与复域上界不控制 uniform entry count，必须另外支付 anchor、truncation、cover 与 pointwise event-weight 账本。</p>`,
  );
  homeEdit.replace('          </div>\n        </section>\n\n      </article>', '          </div>' + releaseCard + '\n        </section>\n\n      </article>');
  homeEdit.replace('综述 v1.01 · 2026-08-26', '综述 v1.02 · 2026-08-26');
  homeEdit.replace('上次综述 v1.00 · 2026-08-26', '上次综述 v1.01 · 2026-08-26');
  homeEdit.replaceAll('/i18n-en.js?v=1.01', '/i18n-en.js?v=1.02');
  homeEdit.replace(
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71P 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71Q 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
  );
}

if (homeEdit.count('data-release="r071q"') !== 1) throw new Error("home: R0.71Q release-card count is not one");
if (homeEdit.count('href="/notes/r0-71q.html"') !== 2) throw new Error("home: expected exactly two R0.71Q note links");
if (homeEdit.count('<summary>展开 51 篇公开笔记</summary>') !== 1) throw new Error("home: route-note count is not 51");
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const litEdit = editor(await readFile(literaturePath, "utf8"), "literature");
const literatureIsCurrent = litEdit.count('<b>R0.71Q</b>') === 1;

if (!literatureIsCurrent) {
  litEdit.replaceAll('/i18n-en.js?v=1.01', '/i18n-en.js?v=1.02');
  litEdit.replace('本站 R0.69P–R0.71P 只列为研究笔记', '本站 R0.69P–R0.71Q 只列为研究笔记');
  litEdit.replaceAll('/recap-r0-61-r0-71p.html', '/recap-r0-61-r0-71q.html');
  litEdit.replace(
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71q.html">累计回顾与 80 节索引</a>中。R0.69P–R0.71P 从有符号物理环带经过 projected-Lamb 热体积、matched-cell heat gap、viscous fusion、signed second jet 与 soft-denominator faces，走到 positive-entry temporal-packing boundary。R0.71P 删除同刻空间 cell multiplicity，留下 distinct entry-time packing。保留下来的结果都不是全局正则性结论。</p>',
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71q.html">累计回顾与 81 节索引</a>中。R0.69P–R0.71P 从有符号物理环带走到 positive-entry temporal-packing boundary；R0.71Q 再把 complex-time Jensen route 写成有限条件定理，并隔离 anchor、component-union、cover 与 pointwise-envelope 账本。保留下来的结果都不是全局正则性结论。</p>',
  );
  litEdit.replace('<a href="/recap-r0-61-r0-71q.html#node-index">打开 80 节完整索引</a>', '<a href="/recap-r0-61-r0-71q.html#node-index">打开 81 节完整索引</a>');
  litEdit.replace(
    String.raw`              <div class="route-step kept"><header><b>R0.71P</b><strong>同刻 positive entries 由空间平方和支付，时间 packing 仍开放</strong></header><p>半开窗口上的 segmented/soft entry 与 hard BV 正跳跃精确分离，初始 trace 单独扣除；bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 删除同刻 cell multiplicity。完整和变成 time-slice budget 对 distinct entry-time counting measure 的积分；componentwise relaxed 正 atoms 内部没有 signed shell–cell cancellation，但它们不一般等于 signed aggregate 的正 Jordan 部。<a href="/notes/r0-71p.html">研究笔记</a> <a href="/recap-r0-61-r0-71q.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71Q</b><strong>quantitative complex-time / parabolic-window zero packing</strong></header><p>下一节显式检查 analytic radius、complex growth、projection anchor 与窗口 covering；定性时间解析性不被写成 uniform zero count。</p></div>`,
    String.raw`              <div class="route-step kept"><header><b>R0.71P</b><strong>同刻 positive entries 由空间平方和支付，时间 packing 仍开放</strong></header><p>bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 删除同刻 cell multiplicity，完整目标归约到 distinct entry-time counting measure。<a href="/notes/r0-71p.html">研究笔记</a></p></div>
              <div class="route-step closed"><header><b>R0.71Q</b><strong>有限 Jensen window theorem 成立，直接解析性路线停止</strong></header><p>Temam 复时间瓣给出显式双侧圆盘；finite ownership cover 与 Hilbert-valued Jensen 给出带 anchor、truncation、cover 和 pointwise-envelope 账本的条件 bound。Blaschke、component-union 与 sine-square families 证明前三类税不能由抽象解析性删除。<a href="/notes/r0-71q.html">研究笔记</a> <a href="/recap-r0-61-r0-71q.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71R</b><strong>NSE-specific parabolic incidence / Carleson packing</strong></header><p>回到 componentwise positive parts 之前的 signed precursor/source，检查 PDE 是否耦合不同 observable 的 entry events；不再重复定性解析性。</p></div>`,
  );
  litEdit.replace('<h3>R0.71P 关闭了什么，R0.71Q 只检查什么</h3>', '<h3>R0.71Q 关闭了什么，R0.71R 只检查什么</h3>');
  litEdit.replace(
    String.raw`<p>R0.71P 证明 \(A_+\) 与 ordinary hard positive jump 不同，并用 cutoff support overlap 与 \(\dot H^{-1}\) square sum 支付所有同刻 entries。逐 shell–cell 先取 soft 正部再求和后，relaxed 正测度内部没有符号抵消；它不一般等于 signed aggregate 的正 Jordan 部。留下的是 distinct entry-time counting measure。R0.71Q 只检查 quantitative complex-time/parabolic-window zero packing，不引入 moving cutoff、refresh 或 total-Jordan sum。我继续用下面六条筛选。</p>`,
    String.raw`<p>R0.71Q 从 Temam 复时间瓣抽取显式双侧圆盘，并用 finite ownership cover 与 Hilbert-valued Jensen 给出有限条件 entry bound。该 bound 必须支付 projection anchor、component union、window cover 与 pointwise batch envelope；三个精确解析族证明这些税不能在一般 holomorphic class 中删除。R0.71R 只检查 NSE-specific parabolic incidence / Carleson packing，并回到 componentwise positive parts 之前的 signed precursor/source。我继续用下面六条筛选。</p>`,
  );
  litEdit.replace(
    String.raw`<div class="boundary"><strong>R0.71P 的一手文献边界</strong><p><a href="https://doi.org/10.1007/BF01236935">Fleming–Rishel</a>与<a href="https://arxiv.org/abs/1503.01746v4">Łochowski</a>把已有 variation 写成 coarea/upcrossing 形式，不从 Leray energy 创造 positive-entry budget。<a href="https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7">Temam</a>只在 classical interval 给逐 observable 的时间解析性；<a href="https://doi.org/10.3792/pja/1195521421">Masuda</a>的唯一延拓针对完整速度场在空间开集消失；<a href="https://doi.org/10.1016/0022-1236(89)90015-3">Foias–Temam</a>的 spatial Gevrey decay 不计 temporal crossings。两轮限定检索未找到从这些工具支付完整 entry-time counting measure 的定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
    String.raw`<div class="boundary"><strong>R0.71Q 的一手文献边界</strong><p><a href="https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7">Temam</a>给出依赖强 \(V\)-norm 的复时间瓣与重新启动；<a href="https://doi.org/10.1007/BF02417878">Jensen</a>的零点公式保留中心锚点。<a href="https://doi.org/10.1016/j.physd.2008.03.007">Giga–Jo–Mahalov–Yoneda</a>、<a href="https://doi.org/10.1016/j.jfa.2020.108563">Dong–Zhang</a>与<a href="https://doi.org/10.1016/j.jmaa.2022.126428">Wang–Gao–Xue</a>支付解析半径或复域上界，但不支付 filtered-observable lower anchor 与全分量零点并集。两轮限定检索未找到从 Leray 数据支付完整 entry-time measure 的定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  );
  litEdit.replace('文献综述 v1.01 · 2026-08-26', '文献综述 v1.02 · 2026-08-26');
}

if (litEdit.count('<b>R0.71Q</b>') !== 1) throw new Error("literature: expected one R0.71Q route node");
if (litEdit.count('开放接口 · R0.71R') !== 1) throw new Error("literature: expected one R0.71R interface");
await writeFile(literaturePath, litEdit.value);

console.log(JSON.stringify({
  status: "ok",
  release: "R0.71Q",
  siteVersion: "v1.02",
  publicNotes: 141,
  currentRouteNotes: 51,
  recapNodes: 81,
  completedReleasesR070AToR071Q: 43,
  next: "R0.71R",
}, null, 2));
