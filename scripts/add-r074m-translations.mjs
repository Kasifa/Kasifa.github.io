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
  ["215 篇公开研究笔记，最新节点 R0.74M。", "215 public research notes, with R0.74M as the latest node."],
  ["研究笔记总索引 · v1.79 · 2026-09-02", "Research-note master index · v1.79 · 2026-09-02"],
  ["最新节点 R0.74M · 持续修订", "Latest node R0.74M · continuously revised"],
  ["最后一小段布朗路径，排出了最近内领圈", "A final short Brownian segment expels the nearest inward collar"],
  ["合成剩余壳层，检查 R0.74K 完整有符号条件；匹配上界与普适端点保持开放。", "Synthesize the remaining shell rows and test the complete R0.74K signed condition; matching upper bounds and the universal endpoint remain open."],
  ["开放接口 · R0.74N", "Open interface · R0.74N"],
  ["其余壳层行与完整有符号条件", "Remaining shell rows and the complete signed condition"],
  ["文献综述 v1.79 · 2026-09-02", "Literature review v1.79 · 2026-09-02"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.74M 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74M only as research notes. I do not extrapolate computations or notes into regularity theorems."],
  ["相关支撑上的最后一小段布朗路径产生渐近大于领圈尺度的正剪切位移；快速回返路径由明确高斯尾支付。", "The final short Brownian segment on the correlated support produces a positive shear displacement asymptotically larger than the collar scale; fast-return paths are paid by an explicit Gaussian tail."],
  ["有界七篇一手文献检索没有找到直接给出或否定这里的端点相关、随 j 一致、指数变平的有符号最近内领圈估计。Malliavin 密度、Hörmander 光滑性、Markov 桥表示和固定剪切混合结果都缺少至少一个必要结构；有限未命中不证明新颖性、优先权或检索完备性。", "The bounded seven-primary-source search found no theorem that directly gives or refutes the endpoint-correlated, j-uniform, exponentially flat signed nearest-inward-collar estimate used here. Malliavin-density, Hörmander-smoothness, Markov-bridge, and fixed-shear mixing results each miss at least one required structure; a finite non-hit proves neither novelty, priority, nor search completeness."],
  ["最后时段排出与最近内领圈", "Final-segment expulsion and the nearest inward collar"],
  ["PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只关闭精确解族的最近内领圈完整行；其余壳层合成、匹配上界、普适端点与全局正则性仍开放。", "PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY are separated in the research note. This section closes only the complete nearest-inward row for the exact solution family; remaining-shell synthesis, matching upper bounds, the universal endpoint, and global regularity remain open."],
  ["R0.74M 的公开边界", "R0.74M public boundary"],
  ["R0.74M 的文献与主张边界", "R0.74M literature and claim boundary"],
  ["02 / 相关支撑", "02 / Correlated support"],
  ["03 / 最后时段", "03 / Final segment"],
  ["04 / 尺度分离", "04 / Scale separation"],
  ["05 / 坏路径", "05 / Bad paths"],
  ["06 / 完整两包行", "06 / Complete two-packet row"],
  ["07 / 证据等级", "07 / Evidence classes"],
  ["23 项校验和", "23 checksums"],
  ["49 项验证记录", "49 validation records"],
  ["本节只推进精确解族内部的领圈分析，不能外推为任意三维 Navier--Stokes 解的定理。", "This section advances collar analysis only inside the exact solution family and cannot be extrapolated to a theorem for arbitrary three-dimensional Navier--Stokes solutions."],
  ["好、坏路径合并后，正包非负上界满足", "After combining good and bad paths, the positive-packet nonnegative majorant satisfies"],
  ["合成其余壳层行，直接检查 R0.74K 完整有符号条件；匹配上界与普适端点继续保持开放。", "Synthesize the remaining shell rows and test the complete R0.74K signed condition directly; matching upper bounds and the universal endpoint remain open."],
  ["后面的排出结论只在这个相关支撑上证明；没有使用“给定终点就必然排出”的原则。", "The expulsion conclusion below is proved only on this correlated support; it does not use the principle that a prescribed endpoint is necessarily expelled."],
  ["坏事件是最后 \\(R_j^2/64\\) 内的布朗振幅超过 \\(L_jR_j/16\\)。反射估计给出 \\(\\mathbb P(\\mathcal H_t^c)\\le4e^{-L_j^2/16}\\)。所需指数余量为", "During the final \\(R_j^2/64\\), the bad event is that the Brownian amplitude exceeds \\(L_jR_j/16\\). The reflection estimate gives \\(\\mathbb P(\\mathcal H_t^c)\\le4e^{-L_j^2/16}\\). The required exponent reserve is"],
  ["解析证明、沿用输入、有限复算和文献边界分开", "Analytic proofs, inherited inputs, finite reconstructions, and the literature boundary are separated"],
  ["快速回返事件由明确高斯尾支付", "Fast-return events are paid by an explicit Gaussian tail"],
  ["两个局部门槛已闭合，全壳层合成仍未完成", "Both local gates are closed, while full shell synthesis remains incomplete"],
  ["领圈位置与剪切滞后留在同一个期望里", "The collar location and shear lag remain in the same expectation"],
  ["普适平方根对数端点、任意三维数据的正则性或奇性仍为 OPEN；", "The universal square-root-log endpoint and regularity or singularity for arbitrary three-dimensional data remain OPEN;"],
  ["其余壳层行的合成和 R0.74K 完整有符号条件仍为 OPEN；", "Synthesis of the remaining shell rows and the complete R0.74K signed condition remain OPEN;"],
  ["权重正好换回 \\(\\Gamma_j\\)。再用反演对称性和 \\(|F_j^++F_j^-|^2\\le2(|F_j^+|^2+|F_j^-|^2)\\) 得到主定理，不需要交叉项的符号信息。", "The weight converts exactly back to \\(\\Gamma_j\\). Inversion symmetry and \\(|F_j^++F_j^-|^2\\le2(|F_j^+|^2+|F_j^-|^2)\\) then give the main theorem without using sign information from the cross term."],
  ["若终点落在最近内领圈，而最后一段布朗路径离终点不超过 \\(L_jR_j/16\\)，则路径保持在 \\(|h_j+X_s|\\le3L_jR_j/5\\) 内。未含 padding 的几何余量为", "If the endpoint lies in the nearest inward collar and the final Brownian segment stays within \\(L_jR_j/16\\) of it, then the path remains inside \\(|h_j+X_s|\\le3L_jR_j/5\\). The geometric reserve before padding is"],
  ["审计后中文 reader source", "Audited Chinese reader source"],
  ["四倍安全上界把一包估计送回原始行", "The factor-four safe majorant returns the one-packet estimate to the original row"],
  ["它足以支付额外的 \\(R_j\\) 和壳权差；这个指数来自最后时段长度与允许振幅，不是数值拟合。", "It pays for the extra \\(R_j\\) and the annular weight gap; this exponent comes from the final-segment length and permitted amplitude, not a numerical fit."],
  ["图件 49/49：FINITE", "Figure checks 49/49: FINITE"],
  ["完整壳层合成：OPEN", "Complete shell synthesis: OPEN"],
  ["完整支撑另含 \\(R_j/8\\) padding；归一化余量是 \\(149/5040-1/(8L_j)\\)，所以包含关系只对充分大的 \\(L_j\\) 使用。内向热流缺陷与平台缺陷比较后得到", "The complete support also contains \\(R_j/8\\) padding; the normalized reserve is \\(149/5040-1/(8L_j)\\), so the inclusion is used only for sufficiently large \\(L_j\\). Comparing the inward caloric defect with the plateau defect gives"],
  ["位移趋于零，但比领圈尺度大得越来越多", "The displacement tends to zero but becomes increasingly larger than the collar scale"],
  ["我没有把真实被动包换成自由热包。R0.74L 的共同前向概率律保留端点领圈与剪切滞后的相关性，其中 \\(T=R_j^2+t\\)，", "I do not replace the true passive packet with a free heat packet. The R0.74L common forward law retains the correlation between the endpoint collar and shear lag, where \\(T=R_j^2+t\\),"],
  ["新颖性和优先权判断仍为 OPEN。", "Novelty and priority judgments remain OPEN."],
  ["沿用 \\(R_j=e^{-L_j^2/320}\\)、\\(\\Gamma_{j-1}/\\Gamma_j=e^{G_1L_j^2}\\)、\\(G_1=2/1323\\)，并固定 \\(s_{R_j}=61R_j^2\\)、\\(I_{R_j}=(64R_j^2,65R_j^2)\\)。本节证明：存在与 \\(j\\) 无关的 \\(C<\\infty\\)，使充分大的 \\(j\\) 满足", "Retain \\(R_j=e^{-L_j^2/320}\\), \\(\\Gamma_{j-1}/\\Gamma_j=e^{G_1L_j^2}\\), and \\(G_1=2/1323\\), and fix \\(s_{R_j}=61R_j^2\\) and \\(I_{R_j}=(64R_j^2,65R_j^2)\\). This section proves that, independently of \\(j\\), there is a \\(C<\\infty\\) such that every sufficiently large \\(j\\) satisfies"],
  ["研究笔记 R0.74M · 完整中文版本", "Research note R0.74M · complete English version"],
  ["因此领圈支撑迫使横向热核导数在距离至少 \\(\\Sigma_{L_j}/2\\) 处取值，好路径进入", "The collar support therefore forces the horizontal heat-kernel derivative to be evaluated at distance at least \\(\\Sigma_{L_j}/2\\), so good paths enter"],
  ["有界七篇一手文献检索没有找到直接给出或否定这里的端点相关、随 \\(j\\) 一致、指数变平的有符号领圈估计。有限未命中不证明新颖性、优先权或检索完备性。", "The bounded seven-primary-source search found no theorem directly giving or refuting the endpoint-correlated, \\(j\\)-uniform, exponentially flat signed collar estimate used here. A finite non-hit proves neither novelty, priority, nor search completeness."],
  ["这里控制完整的 \\(j-1\\) 截止函数导数，保留全部周期绕行、两包自项和交叉项；四倍安全上界不假设正负包抵消。", "This controls the complete \\(j-1\\) cutoff derivative and retains every periodic winding, both packet self-terms, and the cross term; the factor-four safe majorant assumes no positive-negative packet cancellation."],
  ["这样的超高斯尾。这里的“排出”不是常数量级位移，而是两个趋零尺度之间的严格分离。", "such a super-Gaussian tail. Here, expulsion is not an order-one displacement but a strict separation between two vanishing scales."],
  ["这一节仍然没有解决三维 Navier--Stokes 千禧年问题。R0.74L 关闭了主目标领圈；我在本节处理另一个局部门槛：最近内领圈 \\(k=j-1\\) 的完整有符号行。真实剪切在最后一小段物理时间内把典型布朗路径对应的横向中心推出领圈，少数来得太快的路径则由明确的高斯尾支付。结论只属于 R0.74F--H 构造的精确光滑、周期、无外力解族。", "This section still does not solve the three-dimensional Navier--Stokes Millennium Problem. R0.74L closes the main target collar; here I treat another local gate, the complete signed row for the nearest inward collar \\(k=j-1\\). During the final short physical-time segment, the true shear pushes the horizontal centers associated with typical Brownian paths out of the collar, while an explicit Gaussian tail pays for the few paths that return too quickly. The result belongs only to the exact smooth periodic unforced R0.74F--H solution family."],
  ["主文、独立审计、双实现证书与完整图包", "Main text, independent audit, dual-implementation certificates, and the complete figure package"],
  ["状态 · R0.74M", "Status · R0.74M"],
  ["最后 \\(R_j^2/64\\) 产生可量化正位移", "The final \\(R_j^2/64\\) produces a quantitative positive displacement"],
  ["最后时段排出、尺度分离与好坏路径支付", "Final-segment expulsion, scale separation, and good/bad path payments"],
  ["最后时段排出：PROVED", "Final-segment expulsion: PROVED"],
  ["最后一小段布朗路径给出相关支撑上的正剪切位移，关闭精确解族的最近内领圈完整有符号行", "A final short Brownian segment gives a positive shear displacement on the correlated support, closing the complete signed nearest-inward row for the exact solution family"],
  ["最近内领圈完整行、相关支撑上的最后时段正剪切位移、好路径超高斯尾、坏路径高斯支付，以及全部周期绕行与两包交叉项的安全控制。", "The complete nearest-inward row, final-segment positive shear displacement on the correlated support, the good-path super-Gaussian tail, the bad-path Gaussian payment, and safe control of every periodic winding and the two-packet cross term."],
  ["最近内领圈完整行：PROVED", "Complete nearest-inward row: PROVED"],
  ["最近内领圈完整有符号行已闭合", "The complete signed nearest-inward row is closed"],
  ["Python 与独立 Ruby 各 38/38、零差异；图件验证 49/49，23 项校验和通过。有限复算只认证常数、阈值、指数余量和幂次账本，不替代解析证明。", "Python and independent Ruby each pass 38/38 with zero discrepancies; the figure passes 49/49 checks and 23 checksums. Finite reconstruction certifies only constants, thresholds, exponent reserves, and power ledgers; it does not replace the analytic proof."],
  ["R0.74F--H 精确光滑周期无外力解族、R0.74L 共同前向概率律、\\(B_jR_j^2\\) 校准、反演对称性和截止几何。", "The exact smooth periodic unforced R0.74F--H solution family, the R0.74L common forward law, the \\(B_jR_j^2\\) calibration, inversion symmetry, and cutoff geometry."],
  ["reader source 独立审计", "Independent reader-source audit"],
  ["SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是解析账本，不是 DNS、仿真、布朗样本路径或奇点证据。", "SVG is the primary web figure; PNG is the fallback and 600 dpi archive, and PDF is the vector download. The figure is an analytic ledger, not DNS, simulation, a sampled Brownian path, or singularity evidence."],
  ["215 篇研究笔记总索引", "Master index of 215 research notes"],
  ["93 节完整封存", "93 sections fully sealed"],
  ["查看首页 R0.74M 卡片", "View the R0.74M homepage card"],
  ["当前端点 R0.74M", "Current endpoint R0.74M"],
  ["典型相关路径由最后时段正剪切推出领圈，快速回返路径由高斯尾支付；最近内领圈完整行已闭合。", "Typical correlated paths are pushed out of the collar by positive shear on the final segment, while a Gaussian tail pays for fast-return paths; the complete nearest-inward row is closed."],
  ["合成其余壳层行并检查 R0.74K 完整有符号条件；匹配上界仍开放。", "Synthesize the remaining shell rows and test the complete R0.74K signed condition; matching upper bounds remain open."],
  ["跳到首页 R0.74M 卡片 →", "Jump to the R0.74M homepage card →"],
  ["相关支撑上的最后时段排出关闭最近内领圈完整行；全壳层合成、匹配上界和普适端点仍开放。", "Final-segment expulsion on the correlated support closes the complete nearest-inward row; full shell synthesis, matching upper bounds, and the universal endpoint remain open."],
  ["研究笔记 R0.74M · 2026-09-02", "Research note R0.74M · 2026-09-02"],
  ["阅读最新 R0.74M 研究笔记 →", "Read the latest R0.74M research note →"],
  ["展开 125 篇公开笔记", "Expand 125 public notes"],
  ["综述 v1.79 · 2026-09-02", "Review v1.79 · 2026-09-02"],
  ["最后一小段布朗路径把典型相关支撑推出最近内领圈；完整壳层合成与匹配上界仍开放。", "A final short Brownian segment pushes typical correlated support out of the nearest inward collar; complete shell synthesis and matching upper bounds remain open."],
  ["R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 215 篇公开研究笔记", "The cumulative review after the R0.60 recap contains 140 nodes; the site now has 215 public research notes"],
  ["R0.70A–R0.74M · 117 节已公开", "R0.70A–R0.74M · 117 sections published"],
  ["R0.70A–R0.74M：117 节已公开，93 节完整封存", "R0.70A–R0.74M: 117 sections published, 93 fully sealed"],
  ["R0.74M 已关闭最近内领圈完整行；下一步合成其余壳层并检查 R0.74K 完整有符号条件。匹配上界与普适端点仍开放。", "R0.74M closes the complete nearest-inward row; the next step synthesizes the remaining shell rows and tests the complete R0.74K signed condition. Matching upper bounds and the universal endpoint remain open."],
  ["R0.74M：最后时段排出与最近内领圈", "R0.74M: Final-segment expulsion and the nearest inward collar"],
  ["R0.74M｜最后一小段布朗路径，排出了最近内领圈", "R0.74M｜A final short Brownian segment expels the nearest inward collar"],
  ["R0.74N 下一接口", "R0.74N next interface"],
];

const map = new Map(pairs);
assert.equal(map.size, pairs.length, "duplicate R0.74M Chinese translation keys");
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
    assert.equal(currentByZh.get(zh)?.en, en, `R0.74M translation drift: ${zh}`);
} else {
  for (const entry of missingBefore)
    assert.ok(map.has(entry.zh), `untranslated R0.74M source string: ${entry.zh}`);
  const prefixCount = current.filter((row) => /^r074m\d+$/.test(row.id)).length;
  const additions = missingBefore.map((entry, index) => ({
    id: `r074m${String(prefixCount + index + 1).padStart(3, "0")}`,
    ...entry,
    en: map.get(entry.zh),
  }));
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(JSON.stringify({
  release: "R0.74M", translationPath: translationRoute, dgxUsed,
  checked: map.size, applied: !checkOnly,
}, null, 2) + "\n");
