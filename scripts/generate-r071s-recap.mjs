import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const sourcePath = resolve(root, "public/recap-r0-61-r0-71r.html");
const outputPath = resolve(root, "public/recap-r0-61-r0-71s.html");
let html = await readFile(sourcePath, "utf8");

function replaceExact(before, after) {
  const count = html.split(before).length - 1;
  if (count !== 1) {
    throw new Error(
      "expected one match, found " + count + ": " + before.slice(0, 140),
    );
  }
  html = html.replace(before, after);
}

replaceExact(
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71R 的 82 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 Jensen 定理与 parabolic-incidence 两阶尺度错配的路线。"',
  'content="R0.60 之后的研究回顾：按时间整理 R0.61 到 R0.71S 的 83 个研究节点，记录从约化递推到 projected-Lamb 热体积、positive-entry batching、条件 incidence theorem，以及 packet/Bessel 与 NSE initial-face scaling 边界的路线。"',
);
replaceExact(
  'content="R0.61–R0.71R｜R0.60 之后的研究回顾"',
  'content="R0.61–R0.71S｜R0.60 之后的研究回顾"',
);
replaceExact(
  'content="十二个阶段、82 个节点：从约化递推到 positive-entry batching，再到条件 Jensen、有限 parabolic incidence theorem 与 rho=0/rho=2 两阶错配。"',
  'content="十二个阶段、83 个节点：从约化递推到 conditional incidence，再到 directional packets、critical Bessel tax 与只覆盖 NSE initial observation boundary 的 scaling no-go。"',
);
replaceExact(
  '<title>R0.61–R0.71R｜R0.60 之后的研究回顾</title>',
  '<title>R0.61–R0.71S｜R0.60 之后的研究回顾</title>',
);
replaceExact('/i18n-en.js?v=1.03', '/i18n-en.js?v=1.04');
replaceExact(
  '      .phase:nth-child(2){break-before:page;page-break-before:always}\n',
  '',
);
replaceExact(
  '      .phase:nth-child(7){break-before:page;page-break-before:always}\n',
  '',
);
replaceExact(
  '<div class="eyebrow">累计回顾 · R0.61–R0.71R · 2026-08-26</div>',
  '<div class="eyebrow">累计回顾 · R0.61–R0.71S · 2026-08-26</div>',
);
replaceExact(
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71R 的 82 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。',
  '这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.71S 的 83 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。',
);
replaceExact(
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71R</strong><p>收录节点：82</p><p>回顾截止时公开笔记：142</p><p>回顾截止节点：R0.71R</p><p>问题状态：仍未解决</p></div>',
  '<div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.71S</strong><p>收录节点：83</p><p>回顾截止时公开笔记：143</p><p>回顾截止节点：R0.71S</p><p>问题状态：仍未解决</p></div>',
);
replaceExact('02 · 82 节完整索引', '02 · 83 节完整索引');
replaceExact(
  '<div class="metric"><strong>82</strong><span>R0.61–R0.71R 研究节点</span></div>',
  '<div class="metric"><strong>83</strong><span>R0.61–R0.71S 研究节点</span></div>',
);
replaceExact(
  '<div class="metric"><strong>44</strong><span>R0.70A–R0.71R 完成版本</span></div>',
  '<div class="metric"><strong>45</strong><span>R0.70A–R0.71S 完成版本</span></div>',
);
replaceExact('后面的 82 个节点沿着这个缺口推进。', '后面的 83 个节点沿着这个缺口推进。');

replaceExact(
  String.raw`<article class="phase"><h3>R0.71G–R0.71R · denominator faces、temporal packing、Jensen 与 incidence scale audit</h3><p>R0.71O–P 依次恢复 soft quotient 的一侧 traces，并用 bounded overlap 与 \(\dot H^{-1}\) Lamb square sum 组成的一次 time-slice square-function estimate 吸收同刻 batch；R0.71Q 给出 finite conditional Jensen theorem，同时隔离 anchor、truncation、cover 与 H-envelope 四税。R0.71R 从 NSE 导出 localized observable 的 exact forced heat equation，并证明 finite conditional event-to-window theorem；统一 window lower height 与 essential same-observable overlap 明确保留为 hypotheses。\(\Gamma_\rho\) 是 upper comparison constant，\(1/\Gamma_\rho\) 编码 lower-charge strength。rho-dependent source ledger 显示：在 normalized zero-mean torus 上，rho=2 是最小 Leray-paid 指数；对 finite covariant event/window family，\(\Gamma_\rho^{\rm opt}\) 定义为 least admissible upper comparison constant，并在协变 integer/dyadic dilation 下按 lambda^rho 缩放。整数 Fourier 初始例只定义 first-jet surrogate Gamma_{2,jet}，不是 positive-time upper comparison constant 的下界。精确两阶判决只排除一参数 endpoint-square、termwise source-square certificate (3.3) 的无条件闭合，其他 Duhamel designs 与 signed / bilinear alternatives 保持开放。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/notes/r0-71r.html">R0.71R</a><a href="/figures/r0-71r-parabolic-incidence.pdf">最新附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071r">最新证书</a></div></article>`,
  String.raw`<article class="phase"><h3>R0.71G–R0.71S · temporal packing、incidence 与 packet/Bessel scale audit</h3><p>R0.71O–P 恢复 soft quotient 的一侧 traces，并用同刻 spatial batching 吸收有限 frame multiplicity；R0.71Q–R 给出带四税的 finite conditional Jensen theorem、localized forced heat equation、conditional incidence packing 和 rho=0/rho=2 source ledger。R0.71S 保留 entry direction，证明 finite conditional directional-packet payment：nonzero-mean packet 只有在 directional sampling coherence 与 complete indexed Bessel inequality 同时成立时才支付有限 entry family。critical packet 的对角范数平方是 \(\kappa_j^2\)，所以 \(B_{\rm crit}\ge\max\kappa_j^2\)，重复同一 packet \(N\) 次还要求 \(B_{\rm crit}\ge N\kappa_j^2\)；backward-heat adjoint 改变核形状但不移除该因子。bounded bilinear kernel 若消去 constant mode，就看不见 constant leading trace 与 even positive touch；若保留 constant mode，就支付同一 \(\kappa_j^2\) 税。genuine NSE covariant family 进一步证明：只要目标包含 initial observation-boundary entry，scale-invariant entry atom 保持不变，而 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) 按 \(\lambda^{-2}\) 缩放，因而不存在 scale-uniform payment。该结论不覆盖 internal entries，不是所有 nonlinear signed identities 的 impossibility theorem，也不证明继续性或正则性。</p><div class="links"><a href="/notes/r0-71g.html">R0.71G</a><a href="/notes/r0-71h.html">R0.71H</a><a href="/notes/r0-71i.html">R0.71I</a><a href="/notes/r0-71j.html">R0.71J</a><a href="/notes/r0-71k.html">R0.71K</a><a href="/notes/r0-71l.html">R0.71L</a><a href="/notes/r0-71m.html">R0.71M</a><a href="/notes/r0-71n.html">R0.71N</a><a href="/notes/r0-71o.html">R0.71O</a><a href="/notes/r0-71p.html">R0.71P</a><a href="/notes/r0-71q.html">R0.71Q</a><a href="/notes/r0-71r.html">R0.71R</a><a href="/notes/r0-71s.html">R0.71S</a><a href="/figures/r0-71r-parabolic-incidence.pdf">R0.71R 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071s">R0.71S 证书</a></div></article>`,
);

replaceExact(
  '<a href="/figures/r0-71r-parabolic-incidence.pdf">R0.71R 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071s">R0.71S 证书</a>',
  '<a href="/figures/r0-71r-parabolic-incidence.pdf">R0.71R 附图</a><a href="/figures/r0-71s-signed-packet.pdf">R0.71S 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r071s">R0.71S 证书</a>',
);
replaceExact(
  "backward-heat adjoint 改变核形状但不移除该因子。bounded bilinear kernel",
  String.raw`frozen-denominator backward-heat model 改变核形状但不移除该因子；variable \(Y\) 的归一化项未纳入这个线性模型。bounded bilinear kernel`,
);

replaceExact(
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71R 的 82 节公开笔记</h2>',
  '<section id="node-index"><div class="section-no">02 / 完整索引</div><h2>R0.61–R0.71S 的 83 节公开笔记</h2>',
);
replaceExact(
  '            <a href="/notes/r0-71q.html">R0.71Q</a>\n            <a href="/notes/r0-71r.html">R0.71R</a>\n          </div>',
  '            <a href="/notes/r0-71q.html">R0.71Q</a>\n            <a href="/notes/r0-71r.html">R0.71R</a>\n            <a href="/notes/r0-71s.html">R0.71S</a>\n          </div>',
);
replaceExact(
  String.raw`            <li>localized forced heat equation、带 uniform lower height 与 essential overlap hypotheses 的 finite conditional incidence packing、rho-dependent source ledger，以及 covariant optimal constant / rho=2 minimal Leray payment 的精确两阶错配；NSE 高频例只定义 initial first-jet surrogate。</li>`,
  String.raw`            <li>localized forced heat equation、带 uniform lower height 与 essential overlap hypotheses 的 finite conditional incidence packing、rho-dependent source ledger，以及 covariant optimal constant / rho=2 minimal Leray payment 的精确两阶错配；NSE 高频例只定义 initial first-jet surrogate。</li>
            <li>finite conditional directional-packet payment、critical Bessel diagonal 与 repeated-packet lower bounds、necessary directional Carleson condition、backward-heat kernel 和 bounded bilinear constant-mode dichotomy；genuine NSE scaling no-go 只覆盖 initial observation-boundary entry，不覆盖 internal entries。</li>`,
);

replaceExact(
  '<p>截至 R0.71R，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 82 个节点解释成对千禧年问题完成了某个比例。</p>',
  '<p>截至 R0.71S，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 83 个节点解释成对千禧年问题完成了某个比例。</p>',
);
replaceExact(
  String.raw`<p>目前最有内容的无条件正结果仍包括 Leray 能量级 projected-Lamb 热体积、有界重叠局部化、denominator mass、同刻 spatial batching，以及 R0.71R 在 rho=2 下由 Leray energy 支付的 truncation-uniform source integral；frame constants 因 frame 固定而不依赖 finite truncation。完整 theorem 右端仍可能因 upper comparison constant (Gamma_2) 与 essential overlap (M) 而不一致；uniform lower height 与 forward-window availability 是额外 theorem gates，不是右端因子，且同样尚未证明。</p>`,
  String.raw`<p>保留下来的无条件结构仍包括 Leray 能量级 projected-Lamb 热体积、有界重叠局部化、denominator mass、同刻 spatial batching，以及 R0.71R 在 rho=2 下由 Leray energy 支付的 truncation-uniform source integral。R0.71S 新增的是一个 finite conditional directional-packet theorem 和精确 method bounds：packet coherence 与 complete Bessel inequality 是 hypotheses；单 packet 对角已经强迫 \(B_{\rm crit}\ge\kappa_j^2\)，不能由更好的 overlap estimate 删除。</p>`,
);
replaceExact(
  String.raw`<p>R0.71R 把 certificate (3.3) 的一参数 endpoint-square、termwise source-square 缺口压成精确两阶：协变 integer/dyadic dilation 下的 optimal constant 按 lambda^rho 缩放，在 rho=0 不变，但 source ledger 要求 normalized \(L^2\)-Lamb 加 palinstrophy；Leray payment 的最小指数是 rho=2。initial jet 只给 Gamma_{2,jet} surrogate，不给 positive-time Gamma_2 下界。该方法判决不排除其他 Duhamel designs、signed、bilinear 或其他 scale-critical packet functional。</p>`,
  String.raw`<p>在 original scale-invariant positive-entry target、nonzero-mean linear 或 bounded bilinear temporal packet、以及 bare \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) payment 这一声明类内，两阶错配仍然存在。R0.71S 的 genuine NSE scaling theorem 只排除包含 initial observation-boundary entry 的 scale-uniform payment：它没有构造 internal NSE entry，没有排除 internal-entry nonlinear identity，也没有排除加入 scale-\(+2\) dynamical charge 的不同右端。</p>`,
);

replaceExact(
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71S 检查 signed / bilinear scale-critical packet</h2>',
  '<section id="next"><div class="section-no">05 / 下一步</div><h2>R0.71T 检查 internal-entry NSE identity 与 scale-invariant charge</h2>',
);
replaceExact(
  String.raw`<p>下一步保留 entry direction 与 signed pairing，不再把目标先压成 quadratic post-entry amplitude。R0.71S 将检查是否存在 frame-summable、由 \(\dot H^{-1}\) 支付且 scale covariant 的 directional or bilinear packet functional。</p>`,
  String.raw`<p>R0.71T 将把 initial observation boundary 与 internal entry 分开。第一条有限路线是只研究 internal entries，推导依赖完整 NSE 演化、而不是 generic temporal Bessel estimate 的 nonlinear identity；第二条路线是保留完整 entry target，但寻找真正 scale invariant 的 dynamical right side，不再使用 scale exponent 为 \(-2\) 的 bare time integral。</p>`,
);
replaceExact(
  String.raw`<p>候选必须通过 integer-torus initial jet、sequential recurrence 与 repeated-window pressure tests。若 localization 丢失符号，或预算退回 \(L^2\)-Lamb / palinstrophy，我会保留条件并停止该分支。这一步不宣称已解决千禧年问题。</p>`,
  String.raw`<p>任何 internal-entry 结论都必须先证明相应 NSE event 确实存在，并保留 localization commutator、recurrence 与 endpoint availability；不能从 initial face 外推。任何新右端都必须单独证明由 NSE 预算支付。R0.71T 仍是有限方法检查，不宣称继续性、奇性排除或全局正则性。</p>`,
);

replaceExact(
  '<a href="/notes/r0-71r.html">打开最新节点 R0.71R</a>',
  '<a href="/notes/r0-71s.html">打开最新节点 R0.71S</a>',
);
replaceExact(
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71r.pdf">下载同步 PDF</a></p>',
  '<p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="/recap-r0-61-r0-71s.pdf">下载同步 PDF</a></p>',
);
replaceExact(
  'R0.61–R0.71R 回顾 · 2026-08-26',
  'R0.61–R0.71S 回顾 · 2026-08-26',
);

const r071sLinks = html.split('href="/notes/r0-71s.html"').length - 1;
if (r071sLinks !== 3) {
  throw new Error("expected three R0.71S recap links, found " + r071sLinks);
}
if (!html.includes("收录节点：83") || !html.includes("回顾截止时公开笔记：143")) {
  throw new Error("recap totals were not updated");
}
if (!html.includes("R0.70A–R0.71S 完成版本") || !html.includes("<strong>45</strong>")) {
  throw new Error("45-release range was not updated");
}
for (const token of [
  "B_{\\rm crit}\\ge\\max\\kappa_j^2",
  "frozen-denominator backward-heat model 改变核形状但不移除该因子",
  "initial observation-boundary entry",
  "不覆盖 internal entries",
  "R0.71T 检查 internal-entry NSE identity 与 scale-invariant charge",
  "/i18n-en.js?v=1.04",
]) {
  if (!html.includes(token)) throw new Error("missing R0.71S recap boundary: " + token);
}
for (const forbidden of [
  "R0.71S 证明 internal entries 不可能",
  "R0.71S 证明全局正则性",
  "排除了所有 nonlinear signed identities",
  "Bessel tax 可由 overlap 删除",
]) {
  if (html.includes(forbidden)) throw new Error("recap overclaim remains: " + forbidden);
}
if (/我们/.test(html)) throw new Error("recap must use singular or neutral voice");

await writeFile(outputPath, html);
console.log(
  JSON.stringify(
    {
      status: "ok",
      source: sourcePath,
      output: outputPath,
      recapNodes: 83,
      publicNotes: 143,
      completedReleasesR070AToR071S: 45,
      endpoint: "R0.71S",
      next: "R0.71T",
      r071sNoteLinks: r071sLinks,
      i18nVersion: "1.04",
    },
    null,
    2,
  ),
);
