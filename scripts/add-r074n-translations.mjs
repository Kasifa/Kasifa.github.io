#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const translationRoute = "LOCAL_DIRECT_NO_DGX";
const dgxUsed = false;

const pairs = [
  ["216 篇公开研究笔记，最新节点 R0.74N。", "216 public research notes, with R0.74N as the latest node."],
  ["把所有壳层合起来，完整领圈条件闭合了", "Combining all shells closes the complete collar condition"],
  ["研究笔记总索引 · v1.80 · 2026-09-02", "Research-note master index · v1.80 · 2026-09-02"],
  ["最新节点 R0.74N · 持续修订", "Latest node R0.74N · continuously revised"],
  ["开放接口 · R0.74O", "Open interface · R0.74O"],
  ["全部内壳进入一致有界的正部弦长，主壳沿用绝对估计，全部外壳由超高斯权绝对求和；精确解族的 X_j 与领圈通量达到匹配尺度。", "All inward shells enter one uniformly bounded positive-part chord, the target shell retains its absolute estimate, and all outer shells are summed absolutely by super-Gaussian weights; for the exact family, X_j and the collar flux attain matching scales."],
  ["全壳层合成与精确族匹配端点律", "All-shell synthesis and the matching exact-family endpoint law"],
  ["任意流端点与可容许性接口", "Arbitrary-flow endpoint and admissibility interface"],
  ["任意流全壳层控制、payment-to-admissibility、指定点 core-from-shell 和耗散匹配下界继续开放。", "Arbitrary-flow all-shell control, payment-to-admissibility, prescribed-point core-from-shell control, and a matching dissipation lower bound remain open."],
  ["文献综述 v1.80 · 2026-09-02", "Literature review v1.80 · 2026-09-02"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.74N 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74N only as research notes. I do not extrapolate computations or notes into regularity theorems."],
  ["有界八篇一手文献检索找到了加权 Navier--Stokes 能量、局部能量聚合、剪切增强耗散和随机路径方法的先例，没有找到直接给出本节精确全壳层解族结论的定理。有限未命中不证明新颖性、优先权、检索完备性或可发表性。", "The bounded eight-primary-source search found precedents for weighted Navier--Stokes energy, local-energy aggregation, shear-enhanced dissipation, and stochastic path methods, but no theorem directly giving this section's exact all-shell family statement. A finite non-hit proves neither novelty, priority, search completeness, nor publishability."],
  ["PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 分开。本节关闭精确解族的完整全壳层条件，并得到匹配的 X_j 与领圈通量尺度；耗散匹配下界、任意流端点、正则性与 Clay 仍开放。", "PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY are separated. This section closes the complete all-shell condition for the exact family and obtains matching X_j and collar-flux scales; a matching dissipation lower bound, the arbitrary-flow endpoint, regularity, and Clay remain open."],
  ["R0.74N 的公开边界", "R0.74N public boundary"],
  ["R0.74N 的文献与主张边界", "R0.74N literature and claim boundary"],
  ["01 / 完整主结论", "01 / Complete main result"],
  ["02 / 全部内壳", "02 / All inward shells"],
  ["03 / 主壳与外壳", "03 / Target and outer shells"],
  ["04 / 纠正后的精确族结论", "04 / Corrected exact-family conclusion"],
  ["05 / 分量边界", "05 / Component boundary"],
  ["06 / 证据等级", "06 / Evidence classes"],
  ["25 项校验和", "25 checksums"],
  ["67 项验证记录", "67 validation records"],
  ["把全壳层领圈控制移到任意流，或建立 payment-to-admissibility 与指定点 core-from-shell 机制；精确族的耗散匹配下界也继续保持开放。", "Move all-shell collar control to arbitrary flows, or establish payment-to-admissibility and prescribed-point core-from-shell mechanisms; a matching dissipation lower bound for the exact family also remains open."],
  ["本节只处理一个精确构造解族，不能外推为任意三维 Navier--Stokes 解的定理。", "This section treats only one explicitly constructed solution family and cannot be extrapolated into a theorem for arbitrary three-dimensional Navier--Stokes solutions."],
  ["第二个分量没有已证明的匹配下界；这里不声称 \\(\\mathcal D_{{\\rm ext},j}\\ge cT_j\\)。", "No matching lower bound has been proved for the second component; I do not claim \\(\\mathcal D_{{\\rm ext},j}\\ge cT_j\\)."],
  ["对 R0.74F--N 的精确光滑、周期、无外力双包解族，存在与 \\(j\\) 无关的 \\(C<\\infty\\) 和 \\(j_0\\)，使每个 \\(j\\ge j_0\\) 满足", "For the exact smooth periodic unforced two-packet R0.74F--N family, independently of \\(j\\), there are a \\(C<\\infty\\) and a \\(j_0\\) such that every \\(j\\ge j_0\\) satisfies"],
  ["耗散分量单独的匹配下界仍为 OPEN；", "A matching lower bound for the dissipation component alone remains OPEN;"],
  ["耗散匹配下界：OPEN", "Matching dissipation lower bound: OPEN"],
  ["精确族 \\(X_j\\) 匹配律：PROVED", "Exact-family \\(X_j\\) matching law: PROVED"],
  ["精确族内部已闭合，任意流接口仍未跨越", "Closed inside the exact family; the arbitrary-flow interface remains uncrossed"],
  ["壳层独立审计", "Independent shell audit"],
  ["跨笔记推论审计", "Cross-note implication audit"],
  ["领圈通量和 \\(X_j\\) 都达到匹配平方根对数尺度", "The collar flux and \\(X_j\\) both attain the matching square-root-log scale"],
  ["令 \\(T_j=B_j^2L_jR_j^2\\)。分量结论是", "Let \\(T_j=B_j^2L_jR_j^2\\). The component conclusions are"],
  ["内壳联合和、主壳、外壳尾与精确族匹配尺度", "Combined inward sum, target shell, outer tail, and matching exact-family scale"],
  ["普适平方根对数端点、payment-to-admissibility 与指定点 core-from-shell 仍为 OPEN；", "The universal square-root-log endpoint, payment-to-admissibility, and prescribed-point core-from-shell control remain OPEN;"],
  ["全部壳层的完整有符号条件已闭合", "The complete signed condition across all shells is closed"],
  ["全部内壳、主壳和外壳合成为精确解族的完整有符号领圈条件，并给出匹配的 X_j 与领圈通量尺度", "All inward, target, and outer shells are synthesized into the complete signed collar condition for the exact family, with matching X_j and collar-flux scales"],
  ["任意流端点：OPEN", "Arbitrary-flow endpoint: OPEN"],
  ["任意流上的全壳层有符号领圈控制仍为 OPEN；", "Signed all-shell collar control for arbitrary flows remains OPEN;"],
  ["任意三维数据的正则性或奇性、全局存在与光滑性仍为 OPEN；", "Regularity or singularity, global existence, and smoothness for arbitrary three-dimensional data remain OPEN;"],
  ["所有内壳的联合支撑仍落在最大的 \\(j-1\\) 领圈内，所以 R0.74M 的支撑条件化最后时段排出机制可以一次作用于整个内壳和。坏路径由", "The union support of all inward shells remains inside the largest \\(j-1\\) collar, so R0.74M's support-conditioned final-segment expulsion mechanism can act on the entire inward sum at once. Bad paths are paid by"],
  ["所有内壳只留下一个一致有界的正部弦长", "All inward shells leave only one uniformly bounded positive-part chord"],
  ["图表合同", "Chart contract"],
  ["图件 67/67：FINITE", "Figure 67/67: FINITE"],
  ["外部动能有两侧界，耗散分量只有上界", "The exterior kinetic energy has two-sided bounds; dissipation has only an upper bound"],
  ["完整全壳层有符号条件、无抵消内壳联合和、外壳绝对尾、匹配领圈通量律、跨笔记推出的精确族 \\(X_j\\) 匹配律及分量边界。", "The complete signed all-shell condition, the cancellation-free combined inward sum, the absolute outer tail, the matching collar-flux law, the cross-note exact-family \\(X_j\\) matching law, and the component boundary."],
  ["完整有符号条件：PROVED", "Complete signed condition: PROVED"],
  ["尾和由首项控制，且有严格指数余量", "The tail sum is controlled by its first term with a strict exponent reserve"],
  ["我先逐壳取正部，再把权重放进联合弦长。这个上界故意放弃所有壳层抵消：", "I first take the positive part shell by shell, then place the weights in the combined chord. This upper bound deliberately gives up every shell cancellation:"],
  ["新颖性和优先权仍为 OPEN。", "Novelty and priority remain OPEN."],
  ["研究笔记 R0.74N · 完整中文版本", "Research note R0.74N · complete English version"],
  ["因此 \\(\\sup_\\tau|\\mathcal I_>|\\le C\\Gamma_jL_jR_j^5\\)，并同时得到有限截断到无限壳层的统一极限。", "Therefore \\(\\sup_\\tau|\\mathcal I_>|\\le C\\Gamma_jL_jR_j^5\\), and the uniform limit from finite truncations to infinitely many shells follows at the same time."],
  ["有界八篇一手文献检索没有找到直接给出本节精确全壳层解族结论的定理。有限未命中不证明新颖性、优先权、检索完备性或可发表性。", "The bounded eight-primary-source search found no theorem directly giving this section's exact all-shell family conclusion. A finite non-hit proves neither novelty, priority, search completeness, nor publishability."],
  ["这里的完整对象覆盖全部壳层，没有丢掉周期副本，也没有假设壳层或正负包之间发生抵消：", "The complete object covers every shell, discards no periodic copy, and assumes no cancellation between shells or between the positive and negative packets:"],
  ["这是跨笔记证明合成，不是新的随机引理，也不是任意流上的普适端点不等式。", "This is a cross-note proof synthesis, not a new stochastic lemma and not a universal endpoint inequality for arbitrary flows."],
  ["这一节仍然没有解决三维 Navier--Stokes 千禧年问题。R0.74L 处理了主壳，R0.74M 处理了最近内壳。这里我不再逐行追赶：全部内壳进入同一个有界正部弦长，全部外壳由超高斯权绝对求和。因而，冻结精确解族的完整 R0.74K 有符号领圈条件闭合。再与已经审计的能量闭合式和支付律合并，我得到该精确解族上的 \\(X_j\\) 与 \\(\\mathfrak C_j\\) 匹配平方根对数尺度。耗散分量只有上界，没有匹配下界；任意流端点估计和正则性问题仍然开放。", "This section still does not solve the three-dimensional Navier--Stokes Millennium Problem. R0.74L treats the target shell and R0.74M the nearest inward shell. Here I no longer chase the remaining rows one by one: all inward shells enter one bounded positive-part chord, while all outer shells are summed absolutely by super-Gaussian weights. The complete R0.74K signed collar condition therefore closes for the frozen exact family. Combining it with the audited energy closure and payment law gives matching square-root-log scales for \\(X_j\\) and \\(\\mathfrak C_j\\) on this exact family. The dissipation component has only an upper bound and no matching lower bound; the arbitrary-flow endpoint estimate and regularity remain open."],
  ["证书 84/84：FINITE", "Certificate 84/84: FINITE"],
  ["证书对抗审计", "Adversarial certificate audit"],
  ["支付；好路径进入超高斯尾。由此得到 \\(\\sup_\\tau[\\mathcal I_<]_+\\le C\\Gamma_jL_jR_j^5\\)。", "The remainder pays for bad paths, while good paths enter the super-Gaussian tail. Hence \\(\\sup_\\tau[\\mathcal I_<]_+\\le C\\Gamma_jL_jR_j^5\\)."],
  ["主壳使用 R0.74L 已审计的真实包绝对估计。外壳只需最大值原理、完整双面领圈导数总量和超高斯权：", "The target shell uses R0.74L's audited absolute estimate for the true packets. The outer shells require only the maximum principle, the complete two-sided collar derivative mass, and the super-Gaussian weights:"],
  ["主壳沿用绝对估计，外壳一次绝对求和", "Retain the absolute target-shell estimate and sum the outer shells absolutely in one step"],
  ["主文、跨笔记审计、双实现证书与完整图包", "Main text, cross-note audit, dual-implementation certificate, and complete figure package"],
  ["状态 · R0.74N", "Status · R0.74N"],
  ["Python Fraction 与独立 Ruby Rational 各 84/84、零差异；对抗审计拒绝两类有效 JSON 变异。图包含 26 个文件、24 个 manifest 条目、21 个外部绑定和 25 行校验和，验证器 67/67。有限复算不替代解析证明。", "Python Fraction and independent Ruby Rational each pass 84/84 with zero discrepancy; the adversarial audit rejects two valid-JSON mutations. The figure has 26 files, 24 manifest entries, 21 external bindings, and 25 checksum lines, and its validator passes 67/67. Finite reconstruction does not replace analytic proof."],
  ["R0.74F--H 精确解族、R0.74F 外部动能下界、R0.74H 能量闭合式、R0.74J 支付律、R0.74K 转换、R0.74L 主壳估计和 R0.74M 最后时段排出。", "The R0.74F--H exact family, the R0.74F exterior-kinetic lower bound, the R0.74H energy closure, the R0.74J payment law, the R0.74K conversion, the R0.74L target-shell estimate, and the R0.74M final-segment expulsion."],
  ["R0.74K 先把完整条件转换为领圈通量上界，再与 R0.74H、R0.74J 及 R0.74F 的已审计结论非循环地合并。我得到本节必须显式保留的精确族结论：", "R0.74K first converts the complete condition into a collar-flux upper bound. I then combine it non-circularly with the audited R0.74H, R0.74J, and R0.74F conclusions to obtain the exact-family statement that must remain explicit here:"],
  ["SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是确定性解析示意图，不是 DNS、仿真、随机样本路径或奇点证据。", "SVG is the primary web figure; PNG is the fallback and 600 dpi archive, and PDF is the vector download. The figure is a deterministic analytic schematic, not DNS, simulation, a sampled path, or singularity evidence."],
  ["216 篇研究笔记总索引", "Master index of 216 research notes"],
  ["94 节完整封存", "94 sections fully sealed"],
  ["把全壳层领圈控制移到任意流，或建立 payment-to-admissibility 与指定点 core-from-shell 机制。", "Move all-shell collar control to arbitrary flows, or establish payment-to-admissibility and prescribed-point core-from-shell mechanisms."],
  ["查看首页 R0.74N 卡片", "View the R0.74N homepage card"],
  ["当前端点 R0.74N", "Current endpoint R0.74N"],
  ["全部壳层在精确解族内完成合成，X_j 与领圈通量达到匹配尺度；耗散下界和任意流端点仍开放。", "All shells are synthesized within the exact family, and X_j and the collar flux attain matching scales; the dissipation lower bound and arbitrary-flow endpoint remain open."],
  ["全部内壳、主壳和外壳已合成；精确解族的 X_j 与领圈通量达到匹配平方根对数尺度，耗散下界和任意流端点仍开放。", "All inward, target, and outer shells are synthesized; the exact-family X_j and collar flux attain the matching square-root-log scale, while the dissipation lower bound and arbitrary-flow endpoint remain open."],
  ["全部内壳、主壳和外壳已合成；精确解族的领圈通量与 X_j 匹配，耗散下界和任意流端点仍开放。", "All inward, target, and outer shells are synthesized; the exact-family collar flux and X_j match, while the dissipation lower bound and arbitrary-flow endpoint remain open."],
  ["跳到首页 R0.74N 卡片 →", "Jump to the R0.74N homepage card →"],
  ["研究笔记 R0.74N · 2026-09-02", "Research note R0.74N · 2026-09-02"],
  ["阅读最新 R0.74N 研究笔记 →", "Read the latest R0.74N research note →"],
  ["展开 126 篇公开笔记", "Expand 126 public notes"],
  ["综述 v1.80 · 2026-09-02", "Review v1.80 · 2026-09-02"],
  ["R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 216 篇公开研究笔记", "The cumulative review after the R0.60 recap contains 140 nodes; the site now has 216 public research notes"],
  ["R0.70A–R0.74N · 118 节已公开", "R0.70A–R0.74N · 118 sections published"],
  ["R0.70A–R0.74N：118 节已公开，94 节完整封存", "R0.70A–R0.74N: 118 sections published, 94 fully sealed"],
  ["R0.74N 已关闭精确解族的完整全壳层领圈条件，并得到 X_j 与领圈通量匹配律；耗散匹配下界、任意流端点和 Clay 仍开放。", "R0.74N closes the complete all-shell collar condition for the exact family and obtains the matching X_j and collar-flux law; the matching dissipation lower bound, arbitrary-flow endpoint, and Clay remain open."],
  ["R0.74N：全壳层合成与完整领圈条件", "R0.74N: All-shell synthesis and the complete collar condition"],
  ["R0.74N｜把所有壳层合起来，完整领圈条件闭合了", "R0.74N｜Combining all shells closes the complete collar condition"],
  ["R0.74O 下一接口", "R0.74O next interface"],
];

const map = new Map(pairs);
assert.equal(map.size, pairs.length, "duplicate R0.74N Chinese translation keys");
for (const [zh, en] of pairs) {
  assert.ok(!containsChinese(en), `Chinese remains in translation: ${zh}`);
  assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(zh), `protected token drift: ${zh}`);
}

const [source, current] = await Promise.all([
  collectSiteStrings(publicRoot), readFile(translationPath, "utf8").then(JSON.parse),
]);
const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
const missingBefore = source.filter((entry) => !currentByZh.has(entry.zh));
const checkOnly = process.argv.includes("--check-only");
if (checkOnly) {
  assert.equal(missingBefore.length, 0, "site still has untranslated Chinese strings");
  for (const [zh, en] of pairs) assert.equal(currentByZh.get(zh)?.en, en, `R0.74N translation drift: ${zh}`);
} else {
  for (const entry of missingBefore) assert.ok(map.has(entry.zh), `untranslated R0.74N source string: ${entry.zh}`);
  const prefixCount = current.filter((row) => /^r074n\d+$/.test(row.id)).length;
  const additions = missingBefore.map((entry, index) => ({
    id: `r074n${String(prefixCount + index + 1).padStart(3, "0")}`,
    ...entry, en: map.get(entry.zh),
  }));
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(JSON.stringify({ release: "R0.74N", translationPath: translationRoute, dgxUsed, checked: pairs.length, applied: !checkOnly }, null, 2) + "\n");
