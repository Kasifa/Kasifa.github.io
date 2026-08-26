import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");

function editor(source, label) {
  let value = source;
  return {
    replace(before, after) {
      const count = value.split(before).length - 1;
      if (count !== 1) {
        throw new Error(
          `${label}: expected one match, found ${count}: ${before.slice(0, 180)}`,
        );
      }
      value = value.replace(before, after);
    },
    replaceAll(before, after, minimum = 1) {
      const count = value.split(before).length - 1;
      if (count < minimum) {
        throw new Error(
          `${label}: expected at least ${minimum} matches, found ${count}: ${before}`,
        );
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
      value =
        value.slice(0, startIndex) +
        after +
        value.slice(endIndex + end.length);
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

          <div class="task-one" id="r071r" data-release="r071r" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.71R · 2026-08-26</p>
            <h3>有限 incidence theorem 成立，certificate (3.3) 留下精确两阶错配</h3>
            <p>
              localized filtered-vorticity observable 满足
              \[
                C_{j,Q,t}-\nu\Delta C_{j,Q}=G_{j,Q}.
              \]
              对显式 forward height、post-entry upper comparison constant \(\Gamma_\rho\) 与 same-observable overlap，Duhamel 给出 finite conditional event-to-window packing theorem；\(1/\Gamma_\rho\) 编码 lower-charge strength。窗口假设包括 \(0&lt;\theta_-\le\theta_\beta\le\theta_*\) 的统一正下界；\(M\) 取 essential supremum。统一 \(\theta_-\) 与 forward-window availability 是 theorem gates，不是右端因子；缺少正下界时可以任意缩短窗口而平凡化 overlap。
            </p>
            <p>
              rho-dependent source ledger 表明，在 normalized zero-mean torus 上，\(\rho=2\) 是最小 Leray-paid 指数：Leray energy 支付 source integral，frame constants 则由固定 frame 给定；完整右端仍可能因 \(\Gamma_2\) 与 \(M\) 而不一致。对对应 finite covariant event/window family，\(\Gamma_\rho^{\rm opt}\) 定义为 least admissible upper comparison constant；固定 torus 的 compatible integer/dyadic dilation 必须协变搬运 multiplier、cutoff、event 与 window，此时只有 \(\Gamma_\rho^{\rm opt}\) 按 \(\lambda^\rho\) 缩放，并在 \(\rho=0\) 不变。\(\rho=0\) 需要的精确 normalized budget 是 \(\|L\|_2^2/Y+\nu^2\|\nabla\omega\|_2^2/Y\)；这里不声称它等价于 Serrin norm。
            </p>
            <p>
              integer-compatible torus initial data、covariant radial multiplier 与 cutoff 给出 exact Fourier first jet。它只定义 \(\Gamma_{2,\mathrm{jet}}:=A_+/(K^{-2}\|hC_t(0)\|_2^2/Y(0))=K^2/(4\theta^2)\)；这是 leading surrogate，不是 positive-time certificate (3.3) 的 upper comparison constant \(\Gamma_2\) 下界。even-touch、sequential 与 component-union families 只是 forced scalar method tests，不是 NSE trajectories。
            </p>
            <p><strong>结论边界：</strong>&nbsp;本节只排除 certificate (3.3) 的一参数 endpoint-square、termwise source-square 无条件闭合；其他 Duhamel designs 保持开放。这里没有证明 uniform incidence、temporal packing、continuation、singularity 或 global regularity，也不排除 signed / bilinear scale-critical packet。</p>
            <p>
              <a href="/notes/r0-71r.html"><strong>阅读 R0.71R 研究笔记 →</strong></a><br>
              <a href="/notes/r0-71r.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-71r-parabolic-incidence.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071r">查看双重证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071r_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071r_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071r_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r071r_independent_audit.md">查看独立数值审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r071r-parabolic-incidence/fig-r071r-parabolic-incidence">查看附图、数据与源代码包</a> ·
              <a href="/recap-r0-61-r0-71r.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-71r.pdf">下载累计回顾 PDF</a>
            </p>
            <p><strong style="color:var(--gold)">下一步 R0.71S：</strong>&nbsp;保留 entry direction 与 signed pairing，检查是否存在 frame-summable、\(\dot H^{-1}\)-paid 且 scale-covariant 的 bilinear packet functional。</p>
          </div>`;

const homePath = resolve(root, "public/research-review.html");
const homeEdit = editor(await readFile(homePath, "utf8"), "home");
const homeIsCurrent = homeEdit.count('data-release="r071r"') === 1;

if (!homeIsCurrent) {
  homeEdit.replace('<strong>v1.02</strong>网页版本', '<strong>v1.03</strong>网页版本');
  homeEdit.replace('<strong>141</strong>公开研究笔记', '<strong>142</strong>公开研究笔记');
  homeEdit.replace('<strong>R0.71Q</strong>最新研究节点', '<strong>R0.71R</strong>最新研究节点');
  homeEdit.replace(
    '<strong>NSE-specific parabolic incidence packing</strong>当前方向',
    '<strong>signed / bilinear scale-critical incidence packet</strong>当前方向',
  );
  homeEdit.replace(
    '<div class="summary-item"><strong>我目前关注</strong><span>在逐分量正部之前回到 signed precursor/source，检查 NSE 动力学是否强迫 parabolic incidence 或 Carleson packing；不再把定性时间解析性当作 uniform count。</span></div>',
    '<div class="summary-item"><strong>我目前关注</strong><span>保留 entry direction 与 signed pairing，检查是否有 frame-summable、由 \\(\\dot H^{-1}\\) 支付且 scale-covariant 的 bilinear packet；不把 certificate (3.3) 的两阶损失隐藏进新范数。</span></div>',
  );
  homeEdit.replace('Research topology · R0.1–R0.71Q', 'Research topology · R0.1–R0.71R');
  homeEdit.replaceAll('/recap-r0-61-r0-71q.html', '/recap-r0-61-r0-71r.html');
  homeEdit.replace('<span class="route-range">R0.69P–R0.71Q</span>', '<span class="route-range">R0.69P–R0.71R</span>');
  homeEdit.replace(
    '<h3>从有符号环带障碍走到 complex-time packing method boundary</h3>',
    '<h3>从有符号环带障碍走到 parabolic-incidence certificate boundary</h3>',
  );
  homeEdit.replace(
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–F 建立 Leray 能量级 projected-Lamb 热体积及其有界重叠局部化。R0.71G–P 依次核对 residence、matched-cell heat gap、viscous fusion、signed second jet、soft denominator faces 与同刻 spatial batching。R0.71Q 给出有限 Jensen window theorem，并证明 anchor、component union、cover 与 pointwise envelope 仍是未支付账本。</p>',
    '<p>静态环带族被严格排除后，主线转向协方差秩分层与全频投影桥。R0.71A–P 建立 projected-Lamb 热体积、局部化、denominator faces 与同刻 spatial batching。R0.71Q 给出 finite conditional Jensen theorem。R0.71R 再导出 exact forced heat equation 与 conditional incidence packing，并证明 certificate (3.3) 的一参数 endpoint-square、termwise source-square 方案在 rho=0 scale covariance 与 rho=2 minimal Leray payment 之间存在精确两阶错配。</p>',
  );
  homeEdit.replace(
    '→ complex-time anchor / truncation / cover boundary</p>',
    '→ complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary</p>',
  );
  homeEdit.replace('<summary>展开 51 篇公开笔记</summary>', '<summary>展开 52 篇公开笔记</summary>');
  homeEdit.replace('aria-label="R0.69P–R0.71Q"', 'aria-label="R0.69P–R0.71R"');
  homeEdit.replace(
    '                  <a class="milestone" href="/notes/r0-71q.html">R0.71Q</a>\n',
    '                  <a class="milestone" href="/notes/r0-71q.html">R0.71Q</a>\n                  <a class="milestone" href="/notes/r0-71r.html">R0.71R</a>\n',
  );
  homeEdit.replaceBlock(
    '            <article class="tree-node next">',
    '            </article>',
    String.raw`            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.71S</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>signed / bilinear scale-critical incidence packet</h3>
              <p>保留 entry direction 与 signed pairing，检查能否绕开 certificate (3.3) 的两阶错配；候选必须通过 initial-jet、sequential 与 repeated-window 压力测试，且不能把 normalized L2-Lamb 与 palinstrophy 误称为 Serrin-equivalent budget。</p>
            </article>`,
  );
  homeEdit.replace('累计回顾 R0.61–R0.71Q · 2026-08-26', '累计回顾 R0.61–R0.71R · 2026-08-26');
  homeEdit.replace(
    'R0.60 recap 之后的累计回顾收录 81 个节点；全站现有 141 篇公开研究笔记',
    'R0.60 recap 之后的累计回顾收录 82 个节点；全站现有 142 篇公开研究笔记',
  );
  homeEdit.replace(
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及驻留边界、固定匹配小区、positive-entry temporal packing 与 complex-time Jensen method audit。R0.70A–R0.71Q 共 43 个完成版本。',
    'R0.60 之后的路线分成十二段：约化 Picard 与剪切边界、横向扰动、压力局部预算、有符号物理环带、移动标签与 source–core 对偶、偏差张量与有限观测、完整框架协方差、恒定投影边界、正输出与物质热 tent、projected-Lamb 热体积、局部热打包与临界迹障碍，以及 positive-entry temporal packing、conditional Jensen 与 parabolic-incidence scale audit。R0.70A–R0.71R 共 44 个完成版本。',
  );
  homeEdit.replace(
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71Q 给出固定有限截断上的条件 Jensen bound，并以精确反例隔离 anchor、component-union 与 cover taxes；它们和点态 batch envelope 尚不能由 Leray 预算统一支付。</p>',
    '<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71R 证明 finite conditional incidence theorem；在 rho=2 下，Leray energy 支付 source integral，frame constants 因 frame 固定而不依赖 finite truncation。完整右端仍可能因 upper comparison constant Gamma_2 与 essential overlap M 而不一致；theta_- 与 forward windows 是额外 theorem gates，不是右端因子。协变 optimal constant 的 rho=0 与 minimal Leray payment 的 rho=2 只构成 certificate (3.3) 的精确两阶边界。</p>',
  );
  homeEdit.replace(
    '<p><a href="/recap-r0-61-r0-71r.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-71q.pdf">下载同步 PDF</a></p>',
    '<p><a href="/recap-r0-61-r0-71r.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-71r.pdf">下载同步 PDF</a></p>',
  );
  homeEdit.replace(
    '<p><strong style="color:var(--gold)">下一步 R0.71R：</strong>&nbsp;在 componentwise positive parts 之前回到 signed precursor/source，检查 NSE-specific parabolic incidence 或 Carleson packing law；候选必须同时通过 sequential path、Blaschke anchor 与 all-observable union 压力测试。</p>',
    '<p><strong style="color:var(--gold)">R0.71R 已完成：</strong>&nbsp;exact forced heat equation 与 finite conditional incidence theorem 成立；certificate (3.3) 的一参数 endpoint-square、termwise source-square 方案无法同时满足 rho=0 scale covariance 与 rho=2 minimal Leray payment，其他 Duhamel designs 保持开放。</p>',
  );
  homeEdit.replace('          </div>\n        </section>\n\n      </article>', '          </div>' + releaseCard + '\n        </section>\n\n      </article>');
  homeEdit.replace('综述 v1.02 · 2026-08-26', '综述 v1.03 · 2026-08-26');
  homeEdit.replace('上次综述 v1.01 · 2026-08-26', '上次综述 v1.02 · 2026-08-26');
  homeEdit.replaceAll('/i18n-en.js?v=1.02', '/i18n-en.js?v=1.03');
  homeEdit.replace(
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71Q 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
    '我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.71R 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。',
  );
} else {
  homeEdit.replaceBlock(
    '          <div class="task-one" id="r071r" data-release="r071r" style="margin-top:2rem">',
    '          </div>',
    releaseCard.trimEnd(),
  );
}

if (homeEdit.count('/recap-r0-61-r0-71q.pdf') > 0) {
  homeEdit.replaceAll('/recap-r0-61-r0-71q.pdf', '/recap-r0-61-r0-71r.pdf');
}
const recapLinkWithoutPdf =
  '<p><a href="/recap-r0-61-r0-71r.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a></p>';
if (homeEdit.count(recapLinkWithoutPdf) === 1) {
  homeEdit.replace(
    recapLinkWithoutPdf,
    '<p><a href="/recap-r0-61-r0-71r.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-71r.pdf">下载同步 PDF</a></p>',
  );
}

for (const [before, after] of [
  [
    String.raw`<p><strong style="color:var(--gold)">R0.71P 已完成：</strong>&nbsp;同刻正进入由 bounded-overlap 与 \(\dot H^{-1}\) Lamb square sum 支付；完整时间累积被精确归约到 distinct entry-time counting measure。</p>`,
    String.raw`<p><strong style="color:var(--gold)">R0.71P 已完成：</strong>&nbsp;bounded-overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收同刻 batch；完整时间累积被精确归约到 distinct entry-time counting measure。</p>`,
  ],
  [
    "因而空间 cell multiplicity 被删除。",
    "因而同刻 batch 被一次 time-slice square-function estimate 吸收。",
  ],
  [
    "<p><strong>结论边界：</strong>&nbsp;本节关闭同刻空间 multiplicity，没有给出 uniform NSE temporal packing、内部多 face、无限 frame、Leray 极限、继续性或全局正则性结论。</p>",
    "<p><strong>结论边界：</strong>&nbsp;本节证明同刻 batch 的一次 time-slice square-function estimate，没有给出 uniform NSE temporal packing、内部多 face、无限 frame、Leray 极限、继续性或全局正则性结论。</p>",
  ],
  [
    "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71R 证明 finite conditional incidence theorem；在 rho=2 下，source integral 与 fixed-frame constants 对 finite truncation 一致，但完整右端中的 Gamma_2、M、theta_- 与 forward windows 仍未推出。协变 optimal constant 的 rho=0 与 minimal Leray payment 的 rho=2 只构成 certificate (3.3) 的精确两阶边界。</p>",
    "<p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。R0.71R 证明 finite conditional incidence theorem；在 rho=2 下，Leray energy 支付 source integral，frame constants 因 frame 固定而不依赖 finite truncation。完整右端仍可能因 upper comparison constant Gamma_2 与 essential overlap M 而不一致；theta_- 与 forward windows 是额外 theorem gates，不是右端因子。协变 optimal constant 的 rho=0 与 minimal Leray payment 的 rho=2 只构成 certificate (3.3) 的精确两阶边界。</p>",
  ],
]) {
  if (homeEdit.count(before) === 1) homeEdit.replace(before, after);
}

if (homeEdit.count('data-release="r071r"') !== 1) throw new Error("home: R0.71R release-card count is not one");
if (homeEdit.count('href="/notes/r0-71r.html"') !== 2) throw new Error("home: expected exactly two R0.71R note links");
if (homeEdit.count('<summary>展开 52 篇公开笔记</summary>') !== 1) throw new Error("home: route-note count is not 52");
if (/我们/.test(homeEdit.value)) throw new Error("home must use singular or neutral voice");
await writeFile(homePath, homeEdit.value);

const literaturePath = resolve(root, "public/literature-review.html");
const litEdit = editor(await readFile(literaturePath, "utf8"), "literature");
const literatureIsCurrent = litEdit.count('<b>R0.71R</b>') === 1;

if (!literatureIsCurrent) {
  litEdit.replaceAll('/i18n-en.js?v=1.02', '/i18n-en.js?v=1.03');
  litEdit.replace('本站 R0.69P–R0.71Q 只列为研究笔记', '本站 R0.69P–R0.71R 只列为研究笔记');
  litEdit.replaceAll('/recap-r0-61-r0-71q.html', '/recap-r0-61-r0-71r.html');
  litEdit.replace(
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71r.html">累计回顾与 81 节索引</a>中。R0.69P–R0.71P 从有符号物理环带走到 positive-entry temporal-packing boundary；R0.71Q 再把 complex-time Jensen route 写成有限条件定理，并隔离 anchor、component-union、cover 与 pointwise-envelope 账本。保留下来的结果都不是全局正则性结论。</p>',
    '<p class="deck">这张本站路线图从 R0.69P 开始；R0.61–R0.69O 的历史节点没有删除，全部保留在 <a href="/recap-r0-61-r0-71r.html">累计回顾与 82 节索引</a>中。R0.69P–R0.71P 走到 positive-entry temporal-packing boundary，R0.71Q 隔离 analytic/Jensen 四税；R0.71R 再证明 finite conditional parabolic-incidence theorem，并为 certificate (3.3) 定位 rho=0 scale covariance 与 rho=2 minimal Leray payment 的两阶错配。保留下来的结果都不是全局正则性结论。</p>',
  );
  litEdit.replace('<a href="/recap-r0-61-r0-71r.html#node-index">打开 81 节完整索引</a>', '<a href="/recap-r0-61-r0-71r.html#node-index">打开 82 节完整索引</a>');
  litEdit.replace(
    String.raw`              <div class="route-step closed"><header><b>R0.71Q</b><strong>有限 Jensen window theorem 成立，直接解析性路线停止</strong></header><p>Temam 复时间瓣给出显式双侧圆盘；finite ownership cover 与 Hilbert-valued Jensen 给出带 anchor、truncation、cover 和 pointwise-envelope 账本的条件 bound。Blaschke、component-union 与 sine-square families 证明前三类税不能由抽象解析性删除。<a href="/notes/r0-71q.html">研究笔记</a> <a href="/recap-r0-61-r0-71r.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71R</b><strong>NSE-specific parabolic incidence / Carleson packing</strong></header><p>回到 componentwise positive parts 之前的 signed precursor/source，检查 PDE 是否耦合不同 observable 的 entry events；不再重复定性解析性。</p></div>`,
    String.raw`              <div class="route-step closed"><header><b>R0.71Q</b><strong>有限 Jensen window theorem 成立，直接解析性路线停止</strong></header><p>Temam 复时间瓣给出显式双侧圆盘；finite ownership cover 与 Hilbert-valued Jensen 给出带 anchor、truncation、cover 和 pointwise-envelope 账本的条件 bound。Blaschke、component-union 与 sine-square families 证明前三类税不能由抽象解析性删除。<a href="/notes/r0-71q.html">研究笔记</a></p></div>
              <div class="route-step kept"><header><b>R0.71R</b><strong>certificate (3.3) 有精确两阶错配</strong></header><p>exact forced heat equation 与 finite conditional incidence theorem 成立。normalized zero-mean torus 上 rho=2 是 minimal Leray-paid index；对 finite covariant event/window family 定义的 least admissible optimal upper comparison constant 在协变 integer/dyadic dilation 下按 lambda^rho 缩放。initial Fourier example 只定义 Gamma_{2,jet} surrogate，不给 positive-time upper comparison constant Gamma_2 下界。<a href="/notes/r0-71r.html">研究笔记</a> <a href="/recap-r0-61-r0-71r.html">当前累计回顾</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.71S</b><strong>signed / bilinear scale-critical packet</strong></header><p>保留 entry direction 与 signed pairing，检查能否绕开 certificate (3.3) 的两阶错配；其他 Duhamel designs 保持开放。</p></div>`,
  );
  litEdit.replace('<h3>R0.71Q 关闭了什么，R0.71R 只检查什么</h3>', '<h3>R0.71R 关闭了什么，R0.71S 只检查什么</h3>');
  litEdit.replace(
    String.raw`<p>R0.71Q 从 Temam 复时间瓣抽取显式双侧圆盘，并用 finite ownership cover 与 Hilbert-valued Jensen 给出有限条件 entry bound。该 bound 必须支付 projection anchor、component union、window cover 与 pointwise batch envelope；三个精确解析族证明这些税不能在一般 holomorphic class 中删除。R0.71R 只检查 NSE-specific parabolic incidence / Carleson packing，并回到 componentwise positive parts 之前的 signed precursor/source。我继续用下面六条筛选。</p>`,
    String.raw`<p>R0.71R 从 localized observable 的 exact forced heat equation 出发，证明 finite conditional packing theorem。uniform 0&lt;theta_-&lt;=theta_beta&lt;=theta_* 与 forward-window availability 是 theorem gates，不是右端因子；Gamma_rho 是 upper comparison constant，1/Gamma_rho 编码 lower-charge strength，M 是 essential same-observable overlap。rho=2 是 normalized zero-mean torus 上的 minimal Leray-paid index：Leray energy 支付 source integral，frame constants 由固定 frame 给定；完整右端仍可能因 Gamma_2 与 M 而不一致。对对应 finite covariant event/window family，Gamma_rho^opt 定义为 least admissible upper comparison constant；固定 torus 上 compatible integer/dyadic dilation 必须协变搬运 multiplier、cutoff、event 与 window，且只有 Gamma_rho^opt 按 lambda^rho 缩放。整数 Fourier example 只定义 Gamma_{2,jet}=K^2/(4 theta^2) surrogate，不给 positive-time upper comparison constant Gamma_2 下界。certificate (3.3) 以外的 Duhamel designs 保持开放；R0.71S 只检查 signed / bilinear scale-critical packet。我继续用下面六条筛选。</p>`,
  );
  litEdit.replace(
    String.raw`<div class="boundary"><strong>R0.71Q 的一手文献边界</strong><p><a href="https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7">Temam</a>给出依赖强 \(V\)-norm 的复时间瓣与重新启动；<a href="https://doi.org/10.1007/BF02417878">Jensen</a>的零点公式保留中心锚点。<a href="https://doi.org/10.1016/j.physd.2008.03.007">Giga–Jo–Mahalov–Yoneda</a>、<a href="https://doi.org/10.1016/j.jfa.2020.108563">Dong–Zhang</a>与<a href="https://doi.org/10.1016/j.jmaa.2022.126428">Wang–Gao–Xue</a>支付解析半径或复域上界，但不支付 filtered-observable lower anchor 与全分量零点并集。两轮限定检索未找到从 Leray 数据支付完整 entry-time measure 的定理；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
    String.raw`<div class="boundary"><strong>R0.71R 的一手文献边界</strong><p><a href="https://doi.org/10.1002/cpa.3160350604">Caffarelli–Kohn–Nirenberg</a>与<a href="https://doi.org/10.1016/j.aim.2024.109654">Lei–Ren</a>为 singularity / regularity cylinders 给 local-energy gate，不给 smooth filtered entry 的 lower charge。<a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给 parabolic square-Carleson upper norm；<a href="https://doi.org/10.1515/crll.1988.390.79">Angenent</a>的一维标量齐次 spatial zero-number law 还要求 uniform parabolicity、coefficient regularity、相应 boundary hypotheses 与 positive time。两者都不直接控制三维 Hilbert-valued forced observable 的 temporal entries。两轮限定检索未找到 uniform R0.71R incidence / overlap theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  );
  litEdit.replace('文献综述 v1.02 · 2026-08-26', '文献综述 v1.03 · 2026-08-26');
}

for (const [before, after] of [
  [
    String.raw`<div class="route-step kept"><header><b>R0.71P</b><strong>同刻 positive entries 由空间平方和支付，时间 packing 仍开放</strong></header><p>bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 删除同刻 cell multiplicity，完整目标归约到 distinct entry-time counting measure。<a href="/notes/r0-71p.html">研究笔记</a></p></div>`,
    String.raw`<div class="route-step kept"><header><b>R0.71P</b><strong>同刻 positive entries 由空间平方和支付，时间 packing 仍开放</strong></header><p>bounded support overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收同刻 batch，完整目标归约到 distinct entry-time counting measure。<a href="/notes/r0-71p.html">研究笔记</a></p></div>`,
  ],
  [
    String.raw`<div class="route-step kept"><header><b>R0.71R</b><strong>certificate (3.3) 有精确两阶错配</strong></header><p>exact forced heat equation 与 finite conditional incidence theorem 成立。normalized zero-mean torus 上 rho=2 是 minimal Leray-paid index；协变 integer/dyadic dilation 下只有 optimal constant 按 lambda^rho 缩放。initial Fourier example 只定义 Gamma_{2,jet} surrogate，不给 positive-time Gamma_2 下界。<a href="/notes/r0-71r.html">研究笔记</a> <a href="/recap-r0-61-r0-71r.html">当前累计回顾</a></p></div>`,
    String.raw`<div class="route-step kept"><header><b>R0.71R</b><strong>certificate (3.3) 有精确两阶错配</strong></header><p>exact forced heat equation 与 finite conditional incidence theorem 成立。normalized zero-mean torus 上 rho=2 是 minimal Leray-paid index；对 finite covariant event/window family 定义的 least admissible optimal upper comparison constant 在协变 integer/dyadic dilation 下按 lambda^rho 缩放。initial Fourier example 只定义 Gamma_{2,jet} surrogate，不给 positive-time upper comparison constant Gamma_2 下界。<a href="/notes/r0-71r.html">研究笔记</a> <a href="/recap-r0-61-r0-71r.html">当前累计回顾</a></p></div>`,
  ],
  [
    String.raw`<p>R0.71R 从 localized observable 的 exact forced heat equation 出发，证明带 uniform 0&lt;theta_-&lt;=theta_beta&lt;=theta_*、incidence constant 与 essential same-observable overlap 的 finite conditional packing theorem。rho-dependent source ledger 表明 rho=2 是 normalized zero-mean torus 上的 minimal Leray-paid index；固定 torus 上 compatible integer/dyadic dilation 必须协变搬运 multiplier、cutoff、event 与 window，且只有 optimal constant Gamma_rho^opt 按 lambda^rho 缩放。整数 Fourier example 只定义 Gamma_{2,jet}=K^2/(4 theta^2) surrogate，不给 positive-time Gamma_2 下界。certificate (3.3) 以外的 Duhamel designs 保持开放；R0.71S 只检查 signed / bilinear scale-critical packet。我继续用下面六条筛选。</p>`,
    String.raw`<p>R0.71R 从 localized observable 的 exact forced heat equation 出发，证明 finite conditional packing theorem。uniform 0&lt;theta_-&lt;=theta_beta&lt;=theta_* 与 forward-window availability 是 theorem gates，不是右端因子；Gamma_rho 是 upper comparison constant，1/Gamma_rho 编码 lower-charge strength，M 是 essential same-observable overlap。rho=2 是 normalized zero-mean torus 上的 minimal Leray-paid index：Leray energy 支付 source integral，frame constants 由固定 frame 给定；完整右端仍可能因 Gamma_2 与 M 而不一致。对对应 finite covariant event/window family，Gamma_rho^opt 定义为 least admissible upper comparison constant；固定 torus 上 compatible integer/dyadic dilation 必须协变搬运 multiplier、cutoff、event 与 window，且只有 Gamma_rho^opt 按 lambda^rho 缩放。整数 Fourier example 只定义 Gamma_{2,jet}=K^2/(4 theta^2) surrogate，不给 positive-time upper comparison constant Gamma_2 下界。certificate (3.3) 以外的 Duhamel designs 保持开放；R0.71S 只检查 signed / bilinear scale-critical packet。我继续用下面六条筛选。</p>`,
  ],
  [
    String.raw`<div class="boundary"><strong>R0.71R 的一手文献边界</strong><p><a href="https://doi.org/10.1002/cpa.3160350604">Caffarelli–Kohn–Nirenberg</a>与<a href="https://doi.org/10.1016/j.aim.2024.109654">Lei–Ren</a>为 singularity / regularity cylinders 给 local-energy gate，不给 smooth filtered entry 的 lower charge。<a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给 parabolic square-Carleson upper norm，<a href="https://doi.org/10.1515/crll.1988.390.79">Angenent</a>给一维标量齐次方程的 spatial zero-number law；两者都不直接控制三维 Hilbert-valued forced observable 的 temporal entries。两轮限定检索未找到 uniform R0.71R incidence / overlap theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
    String.raw`<div class="boundary"><strong>R0.71R 的一手文献边界</strong><p><a href="https://doi.org/10.1002/cpa.3160350604">Caffarelli–Kohn–Nirenberg</a>与<a href="https://doi.org/10.1016/j.aim.2024.109654">Lei–Ren</a>为 singularity / regularity cylinders 给 local-energy gate，不给 smooth filtered entry 的 lower charge。<a href="https://doi.org/10.1006/aima.2000.1937">Koch–Tataru</a>给 parabolic square-Carleson upper norm；<a href="https://doi.org/10.1515/crll.1988.390.79">Angenent</a>的一维标量齐次 spatial zero-number law 还要求 uniform parabolicity、coefficient regularity、相应 boundary hypotheses 与 positive time。两者都不直接控制三维 Hilbert-valued forced observable 的 temporal entries。两轮限定检索未找到 uniform R0.71R incidence / overlap theorem；这是 bounded negative finding，不是原创性、优先权或不存在性结论。</p></div>`,
  ],
]) {
  if (litEdit.count(before) === 1) litEdit.replace(before, after);
}

if (litEdit.count('<b>R0.71R</b>') !== 1) throw new Error("literature: expected one R0.71R route node");
if (litEdit.count('开放接口 · R0.71S') !== 1) throw new Error("literature: expected one R0.71S interface");
if (/我们/.test(litEdit.value)) throw new Error("literature must use singular or neutral voice");
await writeFile(literaturePath, litEdit.value);

console.log(
  JSON.stringify(
    {
      status: "ok",
      release: "R0.71R",
      siteVersion: "v1.03",
      publicNotes: 142,
      currentRouteNotes: 52,
      recapNodes: 82,
      completedReleasesR070AToR071R: 44,
      next: "R0.71S",
    },
    null,
    2,
  ),
);
