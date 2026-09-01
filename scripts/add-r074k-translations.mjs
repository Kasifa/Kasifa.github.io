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
  ["213 篇公开研究笔记，最新节点 R0.74K。", "213 public research notes, with R0.74K as the latest node."],
  ["研究笔记总索引 · v1.77 · 2026-09-02", "Research-note master index · v1.77 · 2026-09-02"],
  ["自由热指数为何只卡在最近内领圈", "Why the free-heat exponent fails only at the nearest inward collar"],
  ["最新节点 R0.74K · 持续修订", "Latest node R0.74K · continuously revised"],
  ["213 篇研究笔记总索引", "Master index of 213 research notes"],
  ["91 节完整封存", "91 sections fully sealed"],
  ["查看首页 R0.74K 卡片", "View the R0.74K homepage card"],
  ["当前端点 R0.74K", "Current endpoint R0.74K"],
  ["第五支付壳 → 匹配完整支付 → 单一坏内领圈 → 真实包桥边界", "fifth payment shell → matching complete payment → single adverse inward collar → true-packet bridge boundary"],
  ["更深内壳都有严格指数余量，最近内领圈仍阻断自由热替换。真实包桥估计和匹配上界保持开放。", "Every deeper inner shell has strict exponent room, while the nearest inward collar still blocks the free-heat replacement. The true-packet bridge estimate and matching upper bound remain open."],
  ["更深内壳都有严格指数余量；最近内领圈在正体积薄片上仍阻断自由热替换。", "Every deeper inner shell has strict exponent room; the nearest inward collar still blocks the free-heat replacement on a positive-volume slab."],
  ["跳到首页 R0.74K 卡片 →", "Jump to the R0.74K homepage card →"],
  ["研究笔记 R0.74K · 2026-09-02", "Research note R0.74K · 2026-09-02"],
  ["阅读 R0.74K 完整中文笔记 →", "Read the complete Chinese R0.74K note →"],
  ["阅读最新 R0.74K 研究笔记 →", "Read the latest R0.74K research note →"],
  ["展开 123 篇公开笔记", "Expand 123 public notes"],
  ["这里只排除一种比较方法；真实包桥估计、匹配上界和普适端点仍开放，不构成千禧年问题结论。", "This excludes only one comparison method; the true-packet bridge estimate, matching upper bound, and universal endpoint remain open. It is not a Millennium Problem conclusion."],
  ["直接证明或否定真实包的归一化桥—BV 领圈估计。", "Prove or disprove the normalized-bridge–BV collar estimate for the true packet directly."],
  ["自由热比较在所有更深内壳有余量，只在最近内领圈失败；真实包的桥—剪切相关估计仍开放。", "The free-heat comparison has room in every deeper inner shell and fails only at the nearest inward collar; the true packet's bridge–shear correlation estimate remains open."],
  ["综述 v1.77 · 2026-09-02", "Review v1.77 · 2026-09-02"],
  ["R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 213 篇公开研究笔记", "The cumulative review after the R0.60 recap contains 140 nodes; the site now has 213 public research notes"],
  ["R0.70A–R0.74K · 115 节已公开", "R0.70A–R0.74K · 115 sections published"],
  ["R0.70A–R0.74K：115 节已公开，91 节完整封存", "R0.70A–R0.74K: 115 sections published, 91 fully sealed"],
  ["R0.74K 把自由热比较的缺口缩到最近内领圈。下一步直接处理真实包的桥—剪切相关估计；匹配上界与普适端点仍开放。", "R0.74K reduces the free-heat comparison gap to the nearest inward collar. The next step treats the true packet's bridge–shear correlation estimate directly; the matching upper bound and universal endpoint remain open."],
  ["R0.74K：最近内领圈与真实包桥边界", "R0.74K: Nearest inward collar and true-packet bridge boundary"],
  ["R0.74K｜自由热指数为何只卡在最近内领圈", "R0.74K｜Why the free-heat exponent fails only at the nearest inward collar"],
  ["R0.74L 下一接口", "R0.74L next interface"],
  ["开放接口 · R0.74L", "Open interface · R0.74L"],
  ["文献综述 v1.77 · 2026-09-02", "Literature review v1.77 · 2026-09-02"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.74K 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74K only as research notes. I do not extrapolate computations or notes into regularity theorems."],
  ["限定主源审计覆盖 Bedrossian--Coti Zelati、Albritton--Beekie--Novack、Villringer、Gardner--Liss--Mattingly 与 Liss--Luan。现有结果没有提供这里所需的尺度依赖、有限时间、有符号领圈估计；有限非命中不证明新颖性或优先权。", "The bounded primary-source audit covers Bedrossian--Coti Zelati, Albritton--Beekie--Novack, Villringer, Gardner--Liss--Mattingly, and Liss--Luan. The existing results do not provide the scale-dependent, finite-window, signed collar estimate required here; a finite non-hit does not establish novelty or priority."],
  ["真实包桥—BV 领圈估计", "True-packet bridge–BV collar estimate"],
  ["直接证明或否定尺度依赖、有限时间、有符号的真实包领圈估计。", "Prove or disprove the scale-dependent, finite-window, signed true-packet collar estimate directly."],
  ["自由热比较在所有更深内壳有严格指数余量，只在最近内领圈留下正体积障碍；真实包桥—剪切相关估计保持开放。", "The free-heat comparison has strict exponent room in every deeper inner shell and leaves a positive-volume obstruction only at the nearest inward collar; the true-packet bridge–shear correlation estimate remains open."],
  ["最近内领圈与真实包桥边界", "Nearest inward collar and true-packet bridge boundary"],
  ["PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只排除指定的自由热替换，并给出一个仍待证明的真实包充分条件；匹配上界、普适端点与正则性仍开放。", "PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY are separated in the research note. This section excludes only the specified free-heat replacement and states a true-packet sufficient condition that remains unproved; the matching upper bound, universal endpoint, and regularity remain open."],
  ["R0.74K 的公开边界", "R0.74K public boundary"],
  ["R0.74K 的文献与主张边界", "R0.74K literature and claim boundary"],
  ["\\(\\mathfrak C_j\\) 和更强的 \\(X_j\\) 匹配上界仍为 OPEN；", "The matching upper bounds for \\(\\mathfrak C_j\\) and the stronger \\(X_j\\) remain OPEN;"],
  ["01 / 更深内壳", "01 / Deeper inner shells"],
  ["02 / 最近内领圈", "02 / Nearest inward collar"],
  ["03 / 参考尺度", "03 / Reference scale"],
  ["04 / 条件充分律", "04 / Conditional sufficient law"],
  ["05 / 证据边界", "05 / Evidence boundary"],
  ["06 / 开放边界", "06 / Open boundary"],
  ["41 项验证记录", "41-item validation record"],
  ["常剪切参考包固定了正确的领圈量级", "The constant-shear reference packet fixes the correct collar scale"],
  ["除最近一层外，自由热指数都有严格余量", "The free-heat exponent has strict room outside the nearest layer"],
  ["单一坏领圈：PROVED", "Single adverse collar: PROVED"],
  ["单一坏内领圈与真实包桥边界", "Single adverse inward collar and true-packet bridge boundary"],
  ["的真实包假设成立，则", " true-packet hypothesis holds, then"],
  ["该绝对值估计给出参考尺度，但没有处理真实包的时间重数。", "This absolute-value estimate gives the reference scale but does not treat the true packet's temporal multiplicity."],
  ["更深内壳的统一指数余量、最近内领圈的正体积障碍、常剪切参考尺度，以及“真实包假设推出匹配领圈上界”的条件命题。", "The uniform exponent room for deeper inner shells, the positive-volume obstruction at the nearest inward collar, the constant-shear reference scale, and the conditional statement that the true-packet hypothesis implies the matching collar upper bound."],
  ["归一化桥与 BV 的时间耦合估计仍为 OPEN；", "The time-coupled normalized-bridge–BV estimate remains OPEN;"],
  ["记 \\(d_m=c_h-2^{1-m}/\\lambda\\)、\\(G_m=c_\\gamma(1-4^{-m})\\)。对每个物理内壳 \\(2\\le m\\le j-1\\)，", "Write \\(d_m=c_h-2^{1-m}/\\lambda\\) and \\(G_m=c_\\gamma(1-4^{-m})\\). For every physical inner shell \\(2\\le m\\le j-1\\),"],
  ["固定 \\(\\lambda=63/32\\)、\\(c_h=15/16\\)、\\(c_\\gamma=8/3969\\)，并记 \\(d_m=c_h-2^{1-m}/\\lambda\\)、\\(G_m=c_\\gamma(1-4^{-m})\\)。对每个物理内壳 \\(2\\le m\\le j-1\\)，", "Fix \\(\\lambda=63/32\\), \\(c_h=15/16\\), and \\(c_\\gamma=8/3969\\), and write \\(d_m=c_h-2^{1-m}/\\lambda\\) and \\(G_m=c_\\gamma(1-4^{-m})\\). For every physical inner shell \\(2\\le m\\le j-1\\),"],
  ["解析、继承、有限复算和文献筛查分开", "Analytic results, inherited inputs, finite reconstructions, and the literature screen are separated"],
  ["领圈约化独立审计", "Independent collar-reduction audit"],
  ["内向尾独立审计", "Independent inward-tail audit"],
  ["匹配上界：OPEN", "Matching upper bound: OPEN"],
  ["匹配支付律：INHERITED", "Matching payment law: INHERITED"],
  ["普适平方根对数端点、奇点处好尺度与全局正则性仍为 OPEN。", "The universal square-root-log endpoint, a good scale at a singular point, and global regularity remain OPEN."],
  ["若这个仍为", "If this still-"],
  ["剩下的是相关路径估计，不是另一个自由热尾界", "What remains is a correlated path estimate, not another free-heat tail bound"],
  ["剩余问题被压缩成一个有符号包领圈估计", "The remaining problem reduces to one signed packet-collar estimate"],
  ["图件 41/41：FINITE", "Figure checks 41/41: FINITE"],
  ["图件独立审计", "Independent figure audit"],
  ["完整 25 文件图包", "Complete 25-file figure package"],
  ["限定主源筛查覆盖 Bedrossian--Coti Zelati、Albritton--Beekie--Novack、Villringer、Gardner--Liss--Mattingly 与 Liss--Luan。没有一篇被筛论文提供这里所需的尺度依赖、有限时间、有符号领圈估计；有限非命中不证明新颖性或优先权。", "The bounded primary-source screen covers Bedrossian--Coti Zelati, Albritton--Beekie--Novack, Villringer, Gardner--Liss--Mattingly, and Liss--Luan. None of the screened papers provides the scale-dependent, finite-window, signed collar estimate required here; a finite non-hit does not establish novelty or priority."],
  ["研究笔记 R0.74K · 完整中文版本", "Research note R0.74K · complete Chinese version"],
  ["因此，更深内壳只需要把已有桥账本做得更精确，不需要新的指数机制。", "Thus the deeper inner shells require only sharper bookkeeping for the existing bridge, not a new exponent mechanism."],
  ["再与继承下界及 R0.74J 合并，才可得到这一解族上的 \\(\\mathfrak C_j\\asymp P_j^{2/3}\\sqrt{1+\\log_+P_j}\\)。本节没有证明假设，也没有证明匹配上界。", "Only after combining it with the inherited lower bound and R0.74J would one obtain \\(\\mathfrak C_j\\asymp P_j^{2/3}\\sqrt{1+\\log_+P_j}\\) on this family. This section proves neither the hypothesis nor the matching upper bound."],
  ["在最近的 \\(j-1\\) 壳，冻结薄片的归一化体积为 \\(1/262144\\)，且", "In the nearest \\(j-1\\) shell, the frozen slab has normalized volume \\(1/262144\\), and"],
  ["在最近的 \\(j-1\\) 壳，取 \\(4033r_j/8064\\le x_3\\le(4033/8064+1/256)r_j\\)、\\(|x_1|,|x_2|<r_j/64\\)。冻结薄片的归一化体积为 \\(1/262144\\)，且", "In the nearest \\(j-1\\) shell, take \\(4033r_j/8064\\le x_3\\le(4033/8064+1/256)r_j\\) and \\(|x_1|,|x_2|<r_j/64\\). The frozen slab has normalized volume \\(1/262144\\), and"],
  ["这里只排除一种自由热比较方法并冻结下一条充分条件，不构成千禧年问题结论。", "This only excludes one free-heat comparison method and freezes the next sufficient condition; it is not a Millennium Problem conclusion."],
  ["这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我审计了 R0.74J 留下的两个匹配上界方向。精确指数核算表明：如果把真实被动包替换为自由热包，所有更深内壳都有严格指数余量，只有最近的 \\(j-1\\) 壳在一个正体积薄片上仍以 \\(536399/8583708672\\) 的系数向错误方向增长。因此，所选的归一化周期桥路线必须保留内向 Brownian bridge 与正剪切滞后之间的相关性。本文还给出一个精确充分条件：若对应的有符号包领圈积分不超过 \\(\\Gamma_jL_jR_j^5\\)，则该精确解族的领圈通量恰好饱和 \\(P_j^{2/3}\\sqrt{1+\\log P_j}\\) 尺度。这个随机路径估计尚未证明；匹配上界仍为 OPEN。", "This section still does not solve the three-dimensional Navier--Stokes Millennium Problem. I audited the two matching-upper-bound directions left by R0.74J. Exact exponent bookkeeping shows that if the true passive packet is replaced by a free-heat packet, every deeper inner shell has strict exponent room, while only the nearest \\(j-1\\) shell still grows in the wrong direction on a positive-volume slab with coefficient \\(536399/8583708672\\). The selected normalized periodic-bridge route must therefore retain the correlation between inward Brownian bridges and positive shear lag. This section also gives an exact sufficient condition: if the signed packet-collar integral is at most \\(\\Gamma_jL_jR_j^5\\), then the collar flux on this exact family saturates the scale \\(P_j^{2/3}\\sqrt{1+\\log P_j}\\). This stochastic path estimate is not proved; the matching upper bound remains OPEN."],
  ["真实包桥估计：OPEN", "True-packet bridge estimate: OPEN"],
  ["正体积薄片保留错误方向的增长", "A positive-volume slab retains growth in the wrong direction"],
  ["证书 41/41：FINITE", "Certificate 41/41: FINITE"],
  ["直接证明或否定真实包的归一化桥—BV 领圈估计；若失败，就把最近内领圈的正剪切排出缺口写成精确反例边界。", "Prove or disprove the normalized-bridge–BV collar estimate for the true packet directly; if it fails, record the positive-shear-expulsion gap at the nearest inward collar as an exact counterexample boundary."],
  ["主文、双重解析审计、证书与文献边界", "Main text, two analytic audits, certificate, and literature boundary"],
  ["状态 · R0.74K", "Status · R0.74K"],
  ["自由热包替换无法关闭这条指定路线。它不是对目标可观测量上界的反例；真实包仍含差分剪切位移与内向桥的相关性。", "The free-heat packet replacement cannot close this specified route. It is not a counterexample to the target observable upper bound; the true packet still contains the correlation between differential shear displacement and the inward bridge."],
  ["自由热替换：ROUTE OBSTRUCTION", "Free-heat replacement: ROUTE OBSTRUCTION"],
  ["最近内壳的正剪切排出与充分假设本身仍为 OPEN；", "Positive-shear expulsion at the nearest inner shell and the sufficient hypothesis itself remain OPEN;"],
  ["最近内领圈的自由热指数障碍、常剪切参考尺度与仍开放的真实包桥估计", "Free-heat exponent obstruction at the nearest inward collar, constant-shear reference scale, and the open true-packet bridge estimate"],
  ["Python 与独立 Ruby 证书各 41/41；图件验证 41/41，25 文件封存通过。它们只核对精确有理算术和条件指数账本，不证明 Brownian bridge 或 PDE 估计。", "The Python and independent Ruby certificates each pass 41/41; the figure validator passes 41/41 and the 25-file seal passes. They check exact rational arithmetic and the conditional exponent ledger only; they do not prove a Brownian-bridge or PDE estimate."],
  ["R0.74F--H 的精确光滑周期无外力解族、R0.74J 的 \\(P_j\\asymp B_j^3R_j^3\\)，以及 \\(\\mathfrak C_j\\) 的解族下界。", "The exact smooth periodic unforced R0.74F--H family, the R0.74J law \\(P_j\\asymp B_j^3R_j^3\\), and the familywise lower bound for \\(\\mathfrak C_j\\)."],
  ["SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是数学依赖图，不是 DNS、仿真、实验数据或奇点证据。", "SVG is the primary web figure; PNG is the fallback and 600 dpi archive, and PDF is the vector download. The figure is a mathematical dependency diagram, not DNS, simulation, experimental data, or singularity evidence."],
];

const map = new Map(pairs);
assert.equal(map.size, pairs.length, "duplicate R0.74K Chinese translation keys");
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
    assert.equal(currentByZh.get(zh)?.en, en, `R0.74K translation drift: ${zh}`);
} else {
  for (const entry of missingBefore)
    assert.ok(map.has(entry.zh), `untranslated R0.74K source string: ${entry.zh}`);
  const prefixCount = current.filter((row) => /^r074k\d+$/.test(row.id)).length;
  const additions = missingBefore.map((entry, index) => ({
    id: `r074k${String(prefixCount + index + 1).padStart(3, "0")}`,
    ...entry,
    en: map.get(entry.zh),
  }));
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(JSON.stringify({
  release: "R0.74K", translationPath: translationRoute, dgxUsed,
  checked: map.size, applied: !checkOnly,
}, null, 2) + "\n");
