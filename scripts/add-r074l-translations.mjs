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
  ["214 篇公开研究笔记，最新节点 R0.74L。", "214 public research notes, with R0.74L as the latest node."],
  ["变化的桥族、短时钟，和一个闭合的主领圈", "Changing bridges, a short clock, and a closed main collar"],
  ["研究笔记总索引 · v1.78 · 2026-09-02", "Research-note master index · v1.78 · 2026-09-02"],
  ["最新节点 R0.74L · 持续修订", "Latest node R0.74L · continuously revised"],
  ["214 篇研究笔记总索引", "Master index of 214 research notes"],
  ["92 节完整封存", "92 sections fully sealed"],
  ["变化的桥族已反演为共同前向律，主目标领圈由短时钟 BV 闭合；最近内领圈仍开放。", "The changing bridge family is inverted into a common forward law, and short-clock BV closes the main target collar; the nearest inward collar remains open."],
  ["查看首页 R0.74L 卡片", "View the R0.74L homepage card"],
  ["当前端点 R0.74L", "Current endpoint R0.74L"],
  ["共同前向律与短时钟 BV 关闭主目标领圈；最近内领圈、完整有符号条件和匹配上界仍开放。", "The common forward law and short-clock BV close the main target collar; the nearest inward collar, the complete signed condition, and the matching upper bounds remain open."],
  ["跳到首页 R0.74L 卡片 →", "Jump to the R0.74L homepage card →"],
  ["我把变化的后向桥族反演为共同前向律，并用短时钟 BV 闭合了精确解族的主目标领圈。最近内领圈仍为 OPEN。", "I invert the changing backward bridge family into a common forward law and use short-clock BV to close the main target collar for the exact solution family. The nearest inward collar remains OPEN."],
  ["研究笔记 R0.74L · 2026-09-02", "Research note R0.74L · 2026-09-02"],
  ["阅读完整中文笔记 →", "Read the complete Chinese note →"],
  ["阅读最新 R0.74L 研究笔记 →", "Read the latest R0.74L research note →"],
  ["展开 124 篇公开笔记", "Expand 124 public notes"],
  ["直接处理最近内领圈的定量正剪切排出；完整有符号条件仍开放。", "Treat quantitative positive-shear expulsion at the nearest inward collar directly; the complete signed condition remains open."],
  ["综述 v1.78 · 2026-09-02", "Review v1.78 · 2026-09-02"],
  ["R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 214 篇公开研究笔记", "The cumulative review after the R0.60 recap contains 140 nodes; the site now has 214 public research notes"],
  ["R0.70A–R0.74L · 116 节已公开", "R0.70A–R0.74L · 116 sections published"],
  ["R0.70A–R0.74L：116 节已公开，92 节完整封存", "R0.70A–R0.74L: 116 sections published, 92 fully sealed"],
  ["R0.74L 已关闭主目标领圈的时间重数；下一步只处理最近内领圈的定量正剪切排出。完整有符号条件、匹配上界与普适端点仍开放。", "R0.74L closes the temporal multiplicity of the main target collar; the next step treats only quantitative positive-shear expulsion at the nearest inward collar. The complete signed condition, matching upper bounds, and universal endpoint remain open."],
  ["R0.74L：共同前向律、短时钟与主目标领圈", "R0.74L: Common forward law, short clock, and main target collar"],
  ["R0.74L｜变化的桥族、短时钟，和一个闭合的主领圈", "R0.74L｜Changing bridges, a short clock, and a closed main collar"],
  ["R0.74M 下一接口", "R0.74M next interface"],
  ["变化的周期桥族先积分再反演为共同前向律；坏路径指数余量与好路径短时钟 BV 合并，关闭主目标领圈。最近内领圈仍开放。", "The changing periodic bridge family is first integrated and then inverted into a common forward law; the bad-path exponent reserve and good-path short-clock BV together close the main target collar. The nearest inward collar remains open."],
  ["共同前向律、短时钟与主目标领圈", "Common forward law, short clock, and main target collar"],
  ["开放接口 · R0.74M", "Open interface · R0.74M"],
  ["文献综述 v1.78 · 2026-09-02", "Literature review v1.78 · 2026-09-02"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.74L 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74L only as research notes. I do not extrapolate computations or notes into regularity theorems."],
  ["有界十篇主源审计没有找到直接给出或否定本节归一化周期桥--短时钟 BV 估计的定理。边缘投影与经典 Aronson 路线因算子不匹配而未使用；有限未命中不证明新颖性、优先权或检索完备性。", "The bounded ten-primary-source audit found no theorem that directly gives or refutes this section's normalized periodic-bridge--short-clock BV estimate. The marginal-projection and classical Aronson route was not used because the operators do not match; a finite non-hit proves neither novelty, priority, nor search completeness."],
  ["直接证明或否定最近内领圈的 expulsion；完整有符号条件与匹配上界保持开放。", "Prove or disprove expulsion at the nearest inward collar directly; the complete signed condition and matching upper bounds remain open."],
  ["最近内领圈的定量正剪切排出", "Quantitative positive-shear expulsion at the nearest inward collar"],
  ["PROVED、INHERITED、FINITE、LITERATURE BOUNDARY、OPEN 与 NOT CLAY 在研究笔记中分开。本节只关闭精确解族的主目标领圈；最近内领圈、完整有符号条件、匹配上界与普适正则性仍开放。", "PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY are separated in the research note. This section closes only the main target collar for the exact solution family; the nearest inward collar, complete signed condition, matching upper bounds, and universal regularity remain open."],
  ["R0.74L 的公开边界", "R0.74L public boundary"],
  ["R0.74L 的文献与主张边界", "R0.74L literature and claim boundary"],
  ["\\(\\mathfrak C_j\\) 与更强的 \\(X_j\\) 匹配上界仍为 OPEN；", "The matching upper bounds for \\(\\mathfrak C_j\\) and the stronger \\(X_j\\) remain OPEN;"],
  ["02 / 共同概率律", "02 / Common probability law"],
  ["03 / 坏路径", "03 / Bad paths"],
  ["04 / 短时钟与 BV", "04 / Short clock and BV"],
  ["22 项校验和", "22 checksums"],
  ["把变化的周期桥族反演为共同前向律，并用短时钟 BV 关闭精确解族的主目标领圈", "Invert the changing periodic bridge family into a common forward law and use short-clock BV to close the main target collar for the exact solution family"],
  ["保留 R0.74F--K 的精确光滑、周期、无外力解族。对正包 Jensen 上界量 \\(\\mathscr B_j\\)，本节证明", "Retain the exact smooth periodic unforced R0.74F--K solution family. For the positive-packet Jensen upper-bound quantity \\(\\mathscr B_j\\), this section proves"],
  ["本节只关闭精确解族的主目标领圈，不构成任意三维解的正则性或奇性结论。", "This section closes only the main target collar for the exact solution family; it is not a regularity or singularity conclusion for arbitrary three-dimensional solutions."],
  ["独立 Ruby 证书", "Independent Ruby certificate"],
  ["对 \\(j\\ge14\\)，坏事件满足 \\(\\mathbb P(\\mathcal G^c)\\le4e^{-A L_j^2}\\)，其中", "For \\(j\\ge14\\), the bad event satisfies \\(\\mathbb P(\\mathcal G^c)\\le4e^{-A L_j^2}\\), where"],
  ["共同前向律、短时钟与主领圈幂次", "Common forward law, short clock, and main-collar powers"],
  ["共同前向律：PROVED", "Common forward law: PROVED"],
  ["过渡区附近的稀有路径多付一个 \\(R_j\\)", "Rare paths near the transition region pay one extra \\(R_j\\)"],
  ["好路径只穿过一个短时钟区间", "Good paths cross only a short clock interval"],
  ["好事件上 \\(\\theta_j(t,h_j+X_t)>7/8\\)。目标领圈在时钟变量中的支撑长度为 \\(O(L_jR_j)\\)，对应物理时间只有 \\(O(L_jR_j^3)\\)。固定切片加厚后的 BV 界为", "On the good event, \\(\\theta_j(t,h_j+X_t)>7/8\\). The target collar has support length \\(O(L_jR_j)\\) in the clock variable, corresponding to only \\(O(L_jR_j^3)\\) in physical time. The thickened fixed-slice BV bound is"],
  ["后向桥依赖终端时刻，不能把不同终端的桥当成同一条路径来微分。我先对终点变量积分，再利用周期热核对称性，得到同一概率空间上的前向过程", "The backward bridge depends on the terminal time, so bridges with different terminals cannot be differentiated as one path. I first integrate over the endpoint variable and then use periodic heat-kernel symmetry to obtain a forward process on one probability space"],
  ["结合 \\(R_j=e^{-L_j^2/320}\\)，严格余量足以支付额外的 \\(R_j\\)；即使只用粗点态领圈界，坏路径仍贡献 \\(O(L_jR_j^5)\\)。", "Together with \\(R_j=e^{-L_j^2/320}\\), the strict reserve pays for the extra \\(R_j\\); even with only the rough pointwise collar bound, bad paths contribute \\(O(L_jR_j^5)\\)."],
  ["解析证明、继承输入、有限复算与文献筛查分开", "Analytic proofs, inherited inputs, finite reconstructions, and the literature screen are separated"],
  ["解析主文", "Analytic main text"],
  ["两个随机门槛只关闭了一个", "Only one of the two stochastic gates is closed"],
  ["图件 45/45：FINITE", "Figure checks 45/45: FINITE"],
  ["完整有符号条件：OPEN", "Complete signed condition: OPEN"],
  ["问题冻结", "Problem freeze"],
  ["先积分，再把变化的桥族精确反演", "Integrate first, then invert the changing bridge family exactly"],
  ["小振荡路径冻结到进入时刻；模量失效路径的粗界由 \\(\\exp[-c/(L_jR_j)]\\) 吸收。最终幂次账本为", "Small-oscillation paths are frozen at the entrance time; the rough bound for modulus-failure paths is absorbed by \\(\\exp[-c/(L_jR_j)]\\). The final power ledger is"],
  ["研究笔记 R0.74L · 完整中文版本", "Research note R0.74L · complete Chinese version"],
  ["由包反演对称性和 \\(|F_j|^2\\le2(|F_j^+|^2+|F_j^-|^2)\\)，得到", "Packet-inversion symmetry and \\(|F_j|^2\\le2(|F_j^+|^2+|F_j^-|^2)\\) give"],
  ["有界十篇主源审计没有找到直接给出或否定本节周期桥--短时钟 BV 估计的定理。边缘投影与经典 Aronson 捷径因算子不匹配而未使用；有限未命中不证明新颖性或优先权。", "The bounded ten-primary-source audit found no theorem that directly gives or refutes this section's periodic-bridge--short-clock BV estimate. The marginal-projection and classical Aronson shortcut was not used because the operators do not match; a finite non-hit proves neither novelty nor priority."],
  ["在正剪切区内，\\(dq_\\omega=B_j\\theta_j(t,h_j+X_t)dt\\) 只是普通路径积分恒等式，不再是对变化桥族的形式微分。", "Inside the positive-shear region, \\(dq_\\omega=B_j\\theta_j(t,h_j+X_t)dt\\) is an ordinary pathwise integral identity, not a formal differentiation of the changing bridge family."],
  ["这里保留全部周期绕行，也没有使用正负包之间的抵消。", "All periodic windings are retained, and no cancellation between the positive and negative packets is used."],
  ["这一节仍然没有解决三维 Navier--Stokes 千禧年问题。R0.74K 把真实被动包的领圈上界拆成主目标领圈的时间重数和最近内领圈的正剪切排出；我在本节只处理第一项。结果是：主目标领圈所需的归一化周期桥上界已经证明，并通过独立数学审计；最近内领圈仍然 OPEN。核心不是把真实包近似成自由热包，而是先把随终端时刻变化的后向桥族精确反演成同一个前向布朗概率律，再利用真实中心只穿过一个很短的“剪切时钟”区间。", "This section still does not solve the three-dimensional Navier--Stokes Millennium Problem. R0.74K split the true passive packet's collar upper bound into the temporal multiplicity of the main target collar and positive-shear expulsion at the nearest inward collar; this section treats only the first. The normalized periodic-bridge upper bound required for the main target collar is now proved and independently audited, while the nearest inward collar remains OPEN. The key is not to approximate the true packet by a free-heat packet, but first to invert the terminal-time-dependent backward bridge family exactly into one forward Brownian probability law, and then use the fact that the true center crosses only a very short shear-clock interval."],
  ["证书 24/24：FINITE", "Certificate 24/24: FINITE"],
  ["直接处理最近内领圈的正剪切排出；若不能得到定量驱逐，就把精确失败边界冻结为反例。", "Treat positive-shear expulsion at the nearest inward collar directly; if no quantitative expulsion is available, freeze the exact failure boundary as a counterexample."],
  ["周期折叠、共同前向律、坏路径指数余量、加厚固定切片 BV、逆时钟停止时刻、布朗模量，以及主目标领圈两包绝对上界。", "Periodic folding, the common forward law, the bad-path exponent reserve, thickened fixed-slice BV, inverse-clock stopping times, Brownian modulus control, and the absolute two-packet upper bound for the main target collar."],
  ["主目标领圈：PROVED", "Main target collar: PROVED"],
  ["主目标领圈的时间重数已经闭合", "The temporal multiplicity of the main target collar is closed"],
  ["主文、独立审计、证书与文献边界", "Main text, independent audit, certificates, and literature boundary"],
  ["状态 · R0.74L", "Status · R0.74L"],
  ["最近内领圈：OPEN", "Nearest inward collar: OPEN"],
  ["最近内领圈的定量正剪切排出仍为 OPEN；", "Quantitative positive-shear expulsion at the nearest inward collar remains OPEN;"],
  ["最终源文件重绑定", "Final source rebind"],
  ["Python 与独立 Ruby 各 24/24、零差异；图件验证 45/45，22/22 校验和通过。它们只认证有限常数、幂次和图件，不替代桥反演、停止时刻或 BV 解析证明。", "Python and independent Ruby each pass 24/24 with zero discrepancies; the figure passes 45/45 checks and 22/22 checksums. These certify only finite constants, powers, and figure assets; they do not replace the analytic bridge inversion, stopping-time, or BV proofs."],
  ["Python 证书", "Python certificate"],
  ["R0.74F--K 精确解族、\\(B_jR_j^2\\) 的大 \\(j\\) 校准、包反演对称性与目标领圈几何。", "The exact R0.74F--K solution family, the calibration of \\(B_jR_j^2\\) for large \\(j\\), packet-inversion symmetry, and target-collar geometry."],
  ["R0.74K 的完整有符号包条件仍为 OPEN；", "The complete signed-packet condition from R0.74K remains OPEN;"],
  ["SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是解析账本，不是 DNS、仿真、随机采样数据或奇点证据。", "SVG is the primary web figure; PNG is the fallback and 600 dpi archive, and PDF is the vector download. The figure is an analytic ledger, not DNS, simulation, random-sample data, or singularity evidence."],
];

const map = new Map(pairs);
assert.equal(map.size, pairs.length, "duplicate R0.74L Chinese translation keys");
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
    assert.equal(currentByZh.get(zh)?.en, en, `R0.74L translation drift: ${zh}`);
} else {
  for (const entry of missingBefore)
    assert.ok(map.has(entry.zh), `untranslated R0.74L source string: ${entry.zh}`);
  const prefixCount = current.filter((row) => /^r074l\d+$/.test(row.id)).length;
  const additions = missingBefore.map((entry, index) => ({
    id: `r074l${String(prefixCount + index + 1).padStart(3, "0")}`,
    ...entry,
    en: map.get(entry.zh),
  }));
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(JSON.stringify({
  release: "R0.74L", translationPath: translationRoute, dgxUsed,
  checked: map.size, applied: !checkOnly,
}, null, 2) + "\n");
