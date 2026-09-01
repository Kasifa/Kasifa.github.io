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
  ["212 篇公开研究笔记，最新节点 R0.74J。", "212 public research notes, with R0.74J as the latest node."],
  ["第五支付壳给出的匹配完整支付律", "Matching complete-payment law from the fifth payment shell"],
  ["研究笔记总索引 · v1.76 · 2026-09-02", "Research-note master index · v1.76 · 2026-09-02"],
  ["最新节点 R0.74J · 持续修订", "Latest node R0.74J · continuously revised"],
  ["212 篇研究笔记总索引", "Master index of 212 research notes"],
  ["90 节完整封存", "90 sections fully sealed"],
  ["查看首页 R0.74J 卡片", "View the R0.74J homepage card"],
  ["当前端点 R0.74J", "Current endpoint R0.74J"],
  ["第五支付壳给出 \\(8e^{-8}B_j^3R_j^3\\) 下界；与已有上界合并后，精确解族满足 \\(P_j\\asymp B_j^3R_j^3\\)。", "The fifth payment shell gives the lower bound \\(8e^{-8}B_j^3R_j^3\\); combined with the existing upper bound, the exact family satisfies \\(P_j\\asymp B_j^3R_j^3\\)."],
  ["第五支付壳给出精确解族的完整支付下界；与已知上界合并后，Version M 与 F 共享匹配量级。普适平方根对数端点仍开放。", "The fifth payment shell gives a complete-payment lower bound on the exact family; combined with the known upper bound, Versions M and F share the matching scale. The universal square-root-log endpoint remains open."],
  ["分别检查 X_j 与领圈通量的匹配上界，并保留真实包的内向桥相关性。", "Treat the matching upper bounds for X_j and the collar flux separately while retaining the inward-bridge correlation of the true packet."],
  ["精确解族的第五支付壳给出完整支付下界；与已知上界合并后，Version M 与 F 共享 P_j≈B_j^3R_j^3。普适端点仍开放。", "The fifth payment shell of the exact family gives a complete-payment lower bound; combined with the known upper bound, Versions M and F share P_j≈B_j^3R_j^3. The universal endpoint remains open."],
  ["适合弱解移动管 → 第五支付壳 → 匹配完整支付 → 解族平方根对数尺度", "suitable-weak moving tube → fifth payment shell → matching complete payment → familywise square-root-log scale"],
  ["跳到首页 R0.74J 卡片 →", "Jump to the R0.74J homepage card →"],
  ["研究笔记 R0.74J · 2026-09-02", "Research note R0.74J · 2026-09-02"],
  ["阅读 R0.74J 完整中文笔记 →", "Read the complete Chinese R0.74J note →"],
  ["阅读最新 R0.74J 研究笔记 →", "Read the latest R0.74J research note →"],
  ["展开 122 篇公开笔记", "Expand 122 public notes"],
  ["只证明解族上的匹配支付；普适端点、\\(X_j\\) 与领圈通量的匹配上界仍开放。非 Clay 结论。", "Only the familywise matching payment is proved; the universal endpoint and the matching upper bounds for \\(X_j\\) and the collar flux remain open. This is not a Clay conclusion."],
  ["综述 v1.76 · 2026-09-02", "Review v1.76 · 2026-09-02"],
  ["R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 212 篇公开研究笔记", "The cumulative review after the R0.60 recap contains 140 nodes; the site now has 212 public research notes"],
  ["R0.70A–R0.74J · 114 节已公开", "R0.70A–R0.74J · 114 sections published"],
  ["R0.70A–R0.74J：114 节已公开，90 节完整封存", "R0.70A–R0.74J: 114 sections published, 90 fully sealed"],
  ["R0.74J 已在精确解族上证明匹配完整支付律。下一步要分别处理 X_j 与领圈通量的匹配上界，并保留真实包的桥相关性；普适端点和奇点处小量仍开放。", "R0.74J proves a matching complete-payment law on the exact family. The next step is to treat the matching upper bounds for X_j and the collar flux separately while retaining the true packet's bridge correlation; the universal endpoint and smallness at a singular point remain open."],
  ["R0.74J：第五支付壳与匹配完整支付律", "R0.74J: Fifth payment shell and matching complete-payment law"],
  ["R0.74J｜第五支付壳给出的匹配完整支付律", "R0.74J｜Matching complete-payment law from the fifth payment shell"],
  ["R0.74J｜第五支付壳与匹配完整支付律", "R0.74J｜Fifth payment shell and matching complete-payment law"],
  ["R0.74K 下一接口", "R0.74K next interface"],
  ["第五支付壳与匹配完整支付律", "Fifth payment shell and matching complete-payment law"],
  ["分别检查 \\(X_j\\) 与领圈通量的匹配上界，并保留真实包的内向桥相关性。", "Treat the matching upper bounds for \\(X_j\\) and the collar flux separately while retaining the inward-bridge correlation of the true packet."],
  ["精确解族的第五支付壳给出完整支付下界；与 R0.74G 上界合并后，Version M 与 F 的完整支付量都满足 \\(P_j\\asymp B_j^3R_j^3\\)。这不是普适端点上界。", "The fifth payment shell of the exact family gives a complete-payment lower bound; combined with the R0.74G upper bound, the complete payments of Versions M and F both satisfy \\(P_j\\asymp B_j^3R_j^3\\). This is not a universal endpoint upper bound."],
  ["开放接口 · R0.74K", "Open interface · R0.74K"],
  ["两个匹配上界方向", "Two matching-upper-bound directions"],
  ["文献综述 v1.76 · 2026-09-02", "Literature review v1.76 · 2026-09-02"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.74J 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74J only as research notes. I do not extrapolate computations or notes into regularity theorems."],
  ["限定主源审计覆盖 Yang、Vasseur--Yang、Lei--Ren 与 Wang--Wu--Zhou。移动柱、部分正则与一尺度 epsilon 机制已有先例。四篇论文中没有找到相同的匹配完整支付定理，但 finite non-hit 不证明新颖性或优先权。", "The bounded primary-source audit covers Yang, Vasseur--Yang, Lei--Ren, and Wang--Wu--Zhou. Moving cylinders, partial regularity, and one-scale epsilon mechanisms have precedents. The same matching complete-payment theorem was not found in the four papers, but a finite non-hit does not establish novelty or priority."],
  ["PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只在精确解族上闭合完整支付量级；普适平方根对数端点、两个可观测量的匹配上界与奇点处小量仍开放。", "PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY are separated in the research note. This section closes the complete-payment scale only on the exact family; the universal square-root-log endpoint, matching upper bounds for the two observables, and smallness at a singular point remain open."],
  ["R0.74J 的公开边界", "R0.74J public boundary"],
  ["R0.74J 的文献与主张边界", "R0.74J literature and claim boundary"],
  ["\\(X_j\\) 与 \\(\\mathfrak C_j\\) 的匹配上界仍未证明；", "The matching upper bounds for \\(X_j\\) and \\(\\mathfrak C_j\\) are not proved;"],
  ["01 / 第五支付壳", "01 / Fifth payment shell"],
  ["02 / 匹配支付", "02 / Matching payment"],
  ["03 / 对数率", "03 / Logarithmic rate"],
  ["04 / 平方根对数尺度", "04 / Square-root-log scale"],
  ["05 / 证据分层", "05 / Evidence layers"],
  ["07 / 开放边界", "07 / Open boundary"],
  ["79 项验证记录", "79-item validation record"],
  ["把上式与 R0.74G 的匹配上界及精确零 frame 恒等式合并，得到", "Combining the displayed bound with the matching R0.74G upper bound and the exact zero-frame identities gives"],
  ["从支付到可容许性、从外壳到移动核心的控制仍开放；", "Payment-to-admissibility and shell-to-moving-core control remain open;"],
  ["第五壳下界：PROVED", "Fifth-shell lower bound: PROVED"],
  ["第五壳下界与匹配支付链", "Fifth-shell lower bound and matching-payment chain"],
  ["第一个常数是完整支付的对数率；第二个常数记录实际支付序列的 lacunarity。二者只针对这一精确解族。", "The first constant is the logarithmic rate of the complete payment; the second records the lacunarity of the actual payment sequence. Both apply only to this exact family."],
  ["独立复算 287 字段：FINITE", "Independent reconstruction of 287 fields: FINITE"],
  ["分别检查 \\(X_j\\) 与 \\(\\mathfrak C_j\\) 的匹配上界，并保留精确包的内向桥与剪切滞后；在获得真实包估计前不外推普适端点或正则性。", "Treat the matching upper bounds for \\(X_j\\) and \\(\\mathfrak C_j\\) separately while retaining the exact packet's inward bridge and shear lag; do not extrapolate a universal endpoint or regularity before obtaining a true-packet estimate."],
  ["该等价关系解释了 R0.74I 中出现的平方根对数尺度，但它不是对任意解、任意尺度成立的普适端点上界。", "This equivalence explains the square-root-log scale appearing in R0.74I, but it is not a universal endpoint upper bound for arbitrary solutions and scales."],
  ["固定盒给出非负三次量下界", "A fixed box gives a nonnegative cubic lower bound"],
  ["绘图源码", "Plotting source"],
  ["解析证明、继承结果和有限复算分别记录", "Analytic proofs, inherited results, and finite reconstructions are recorded separately"],
  ["解族、零 frame 恒等式、\\(\\beta_j=B_jR_j^2\\to1/128\\) 与上界来自 R0.74F--H 和 R0.74G；本节新证明的是第五壳下界及其与这些结果的精确合并。", "The family, zero-frame identities, \\(\\beta_j=B_jR_j^2\\to1/128\\), and the upper bound come from R0.74F--H and R0.74G; this section newly proves the fifth-shell lower bound and its exact combination with those results."],
  ["精确光滑周期无外力解族上的第五支付壳下界、匹配完整支付律与平方根对数尺度", "Fifth-payment-shell lower bound, matching complete-payment law, and square-root-log scale on an exact smooth periodic unforced family"],
  ["可能奇点处的给定好尺度定理仍开放；", "A prescribed good-scale theorem at a possible singular point remains open;"],
  ["匹配完整支付律：PROVED", "Matching complete-payment law: PROVED"],
  ["匹配支付不等于普适端点或正则性", "Matching payment is not a universal endpoint or regularity result"],
  ["匹配支付解释了解族上的端点量级", "The matching payment explains the familywise endpoint scale"],
  ["普适端点上界：OPEN", "Universal endpoint upper bound: OPEN"],
  ["普适平方根对数端点上界仍为 OPEN；", "The universal square-root-log endpoint upper bound remains OPEN;"],
  ["取 \\(z_{0,j}=(65R_j^2,0)\\)、\\(A_5(2R_j)=\\{64R_j\\le |x|<128R_j\\}\\) 和 \\(\\Gamma_5=e^{-8}\\)。对所有充分大的 \\(j\\)，选定盒完全落在第五壳内，背景剪切在支付窗内至少为 \\(1/2\\)。因此", "Set \\(z_{0,j}=(65R_j^2,0)\\), \\(A_5(2R_j)=\\{64R_j\\le |x|<128R_j\\}\\), and \\(\\Gamma_5=e^{-8}\\). For every sufficiently large \\(j\\), the selected box lies entirely in the fifth shell and the background shear stays at least \\(1/2\\) throughout the payment window. Therefore"],
  ["全局正则性、奇点排除、新颖性与优先权均未证明。", "Global regularity, singularity exclusion, novelty, and priority are not proved."],
  ["热平台独立审计", "Independent heat-platform audit"],
  ["四篇主源只限定先例与非命中范围", "Four primary sources delimit only precedents and the non-hit scope"],
  ["图件 79/79：FINITE", "Figure checks 79/79: FINITE"],
  ["完整支付独立审计", "Independent complete-payment audit"],
  ["限定检索覆盖 Yang（2022）、Vasseur--Yang（2021）、Lei--Ren（2024）和 Wang--Wu--Zhou（2019）。移动柱、部分正则与一尺度 epsilon 机制已有先例。", "The bounded search covers Yang (2022), Vasseur--Yang (2021), Lei--Ren (2024), and Wang--Wu--Zhou (2019). Moving cylinders, partial regularity, and one-scale epsilon mechanisms have precedents."],
  ["研究笔记 R0.74J · 完整中文版本", "Research note R0.74J · complete Chinese version"],
  ["验证器", "Validator"],
  ["这里使用的是非负速度三次项。下界来自解析证明，不来自有限采样或仿真。", "This uses the nonnegative cubic velocity term. The lower bound comes from an analytic proof, not finite sampling or simulation."],
  ["这是一条精确解族上的匹配支付律，不是 Clay 千禧年问题的解答。", "This is a matching-payment law on an exact family, not a solution of the Clay Millennium Problem."],
  ["这四篇论文中没有找到相同的匹配完整支付定理；有限非命中不证明新颖性或优先权。", "The same matching complete-payment theorem was not found in the four papers; a finite non-hit does not establish novelty or priority."],
  ["这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我重新核对了 R0.74F--H 构造并在 R0.74I 中再次分析的精确、光滑、周期、无外力解族。在支付半径 \\(2R_j\\) 的第五壳，一个固定盒中的背景剪切在整个支付时间窗内保持至少 \\(1/2\\)，所以非负的速度三次项给出 \\(8e^{-8}B_j^3R_j^3\\) 的下界。与 R0.74G 已证明的上界合并后，Version M 和 Version F 的共同完整支付量满足 \\(P_j\\asymp B_j^3R_j^3\\)，并且 \\(\\log P_j/L_j^2\\to3/320\\)。这是一个精确解族上的匹配支付律，不是普适平方根对数端点上界；它没有给出 \\(X_j\\) 或 \\(\\mathfrak C_j\\) 的匹配上界，也没有在可能奇点处制造小量条件。", "This section still does not solve the three-dimensional Navier--Stokes Millennium Problem. I rechecked the exact smooth periodic unforced family constructed in R0.74F--H and reanalysed in R0.74I. In the fifth shell at payment radius \\(2R_j\\), the background shear on a fixed box stays at least \\(1/2\\) throughout the payment window, so the nonnegative cubic velocity term gives the lower bound \\(8e^{-8}B_j^3R_j^3\\). Combined with the upper bound proved in R0.74G, the common complete payment of Versions M and F satisfies \\(P_j\\asymp B_j^3R_j^3\\), and \\(\\log P_j/L_j^2\\to3/320\\). This is a matching-payment law on an exact family, not a universal square-root-log endpoint upper bound; it gives no matching upper bound for \\(X_j\\) or \\(\\mathfrak C_j\\), and it produces no smallness condition at a possible singular point."],
  ["证书 38/38：FINITE", "Certificate 38/38: FINITE"],
  ["支付增长率与稀疏系数都固定下来", "The payment growth rate and lacunarity coefficient are both fixed"],
  ["周期热平台下界、第五壳中的固定盒、非负速度三次下界、两种版本的匹配完整支付律、\\(3/320\\) 对数率与 \\(9/320\\) 稀疏系数。", "The periodic heat-platform lower bound, the fixed box in the fifth shell, the nonnegative cubic velocity lower bound, the matching complete-payment law for both versions, the logarithmic rate \\(3/320\\), and the lacunarity coefficient \\(9/320\\)."],
  ["状态 · R0.74J", "Status · R0.74J"],
  ["Python 证书 38/38 并逐字节复现冻结 JSON；独立 Ruby 复算 38/38，比较 287 个终端字段且零差异。图件 validator 79/79，24 文件封存通过。有限证书只核对精确算术和图件，不证明热方程或连续定理。", "The Python certificate passes 38/38 and reproduces the frozen JSON byte for byte; the independent Ruby reconstruction passes 38/38, compares 287 terminal fields, and finds zero differences. The figure validator passes 79/79 and seals 24 files. These finite certificates check exact arithmetic and the figure only; they do not prove the heat equation or a continuum theorem."],
  ["R0.74F--H 精确解族、零 frame 恒等式、振幅校准与 R0.74G 的匹配上界。", "The exact R0.74F--H family, zero-frame identities, amplitude calibration, and matching R0.74G upper bound."],
  ["R0.74G 上界：INHERITED", "R0.74G upper bound: INHERITED"],
  ["SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是解析关系图，不是 DNS、数值仿真、实验数据或奇点证据。", "SVG is the primary web figure; PNG is the fallback and 600 dpi archive, and PDF is the vector download. The figure is an analytic relation diagram, not DNS, numerical simulation, experimental data, or singularity evidence."],
  ["Version M 与 Version F 共享同一完整支付量", "Versions M and F share the same complete payment"],
];

const map = new Map(pairs);
assert.equal(map.size, pairs.length, "duplicate R0.74J Chinese translation keys");
for (const [zh, en] of pairs) {
  assert.ok(!containsChinese(en), `Chinese remains in translation: ${zh}`);
  assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(zh), `protected token drift: ${zh}`);
}

const [source, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
const missingBefore = source.filter((entry) => !currentByZh.has(entry.zh));
const checkOnly = process.argv.includes("--check-only");
if (checkOnly) {
  assert.equal(missingBefore.length, 0, "site still has untranslated Chinese strings");
  for (const [zh, en] of pairs)
    assert.equal(currentByZh.get(zh)?.en, en, `R0.74J translation drift: ${zh}`);
} else {
  for (const entry of missingBefore)
    assert.ok(map.has(entry.zh), `untranslated R0.74J source string: ${entry.zh}`);
  const prefixCount = current.filter((row) => /^r074j\d+$/.test(row.id)).length;
  const additions = missingBefore.map((entry, index) => ({
    id: `r074j${String(prefixCount + index + 1).padStart(3, "0")}`,
    ...entry,
    en: map.get(entry.zh),
  }));
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(JSON.stringify({
  release: "R0.74J", translationPath: translationRoute, dgxUsed,
  checked: map.size, applied: !checkOnly,
}, null, 2) + "\n");
