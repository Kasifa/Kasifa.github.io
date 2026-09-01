#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const translationRoute = "LOCAL_DIRECT_NO_DGX";
const dgxUsed = false;

const pairs = [
  ["开放接口 · R0.74J", "Open interface · R0.74J"],
  ["适合弱解移动管门与平方根对数支付边界", "Suitable-weak moving-tube gate and square-root-log payment boundary"],
  ["文献综述 v1.75 · 2026-09-02", "Literature review v1.75 · 2026-09-02"],
  ["我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.74I 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74I only as research notes. I do not extrapolate computations or notes into regularity theorems."],
  ["小量传播与端点决定", "Smallness propagation and endpoint decision"],
  ["PROVED、FINITE、OPEN、LITERATURE BOUNDARY 与 NOT CLAY 在研究笔记中分开。一尺度小量可进入既有正则门，但本节没有证明可能奇点处的小量、跨尺度传播或平方根对数端点上界。", "PROVED, FINITE, OPEN, LITERATURE BOUNDARY, and NOT CLAY are separated in the research note. One-scale smallness can enter an established regularity gate, but this section does not prove smallness at a possible singular point, cross-scale propagation, or the square-root-log endpoint upper bound."],
  ["R0.74I 的公开边界", "R0.74I public boundary"],
  ["R0.74I 的文献与主张边界", "R0.74I literature and claim boundary"],
  ["Version M 已推进到适合弱解；给定尺度上的小移动能量进入已有固定柱 epsilon 判据。精确双包族排除所有 \\(\\gamma<1/2\\) 的普适对数修复，端点上界仍开放。", "Version M now covers suitable weak solutions; small moving energy at a given scale enters an established fixed-cylinder epsilon criterion. The exact two-packet family excludes every universal logarithmic repair with \\(\\gamma<1/2\\), while the endpoint upper bound remains open."],
  ["Yang 与 Vasseur--Yang 已使用光滑化轨迹、参考时刻锚定和单侧后向斜柱；这些几何成分属于先例。限定式检索未找到相同的 Version-M 支付、正环带通量、移动到固定包含与局部标量支付组合，但 finite non-hit 不证明新颖性或优先权。", "Yang and Vasseur--Yang already use mollified trajectories, reference-time anchoring, and one-sided backward skewed cylinders; those geometric ingredients are precedents. A bounded search did not find the same combination of Version-M payment, positive collar flux, moving-to-fixed inclusion, and local scalar payment, but a finite non-hit does not establish novelty or priority."],
  ["211 篇公开研究笔记，最新节点 R0.74I。", "211 public research notes, with R0.74I as the latest node."],
  ["适合弱解的移动管门与平方根对数支付边界", "Suitable-weak moving-tube gate and square-root-log payment boundary"],
  ["研究笔记总索引 · v1.75 · 2026-09-02", "Research-note master index · v1.75 · 2026-09-02"],
  ["最新节点 R0.74I · 持续修订", "Latest node R0.74I · continuously revised"],
  ["索引页本身不计入研究笔记总数。43 篇早期笔记尚无同名 PDF，页面明确标为历史 HTML-only，不生成失效下载链接。", "The index page itself is not included in the research-note total. 43 early notes have no matching PDF; they are explicitly marked as historical HTML-only entries, and no broken download links are created."],
  ["\\(\\gamma=1/2\\) 未被否定，也没有被证明", "\\(\\gamma=1/2\\) is neither refuted nor proved"],
  ["\\[\\boxed{\\mathcal E^{M,R}(z_0,8R)\\le\\varepsilon_{\\rm tube}\\quad\\Longrightarrow\\quad z_0\\text{ 是正则点}.}\\]", "\\[\\boxed{\\mathcal E^{M,R}(z_0,8R)\\le\\varepsilon_{\\rm tube}\\quad\\Longrightarrow\\quad z_0\\text{ is regular}.}\\]"],
  ["\\[\\boxed{P_R^M\\le\\varepsilon_P\\quad\\Longrightarrow\\quad z_0\\text{ 是正则点}.}\\]", "\\[\\boxed{P_R^M\\le\\varepsilon_P\\quad\\Longrightarrow\\quad z_0\\text{ is regular}.}\\]"],
  ["01 / 弱解闭合", "01 / Suitable-weak closure"],
  ["02 / 正则门", "02 / Regularity gate"],
  ["03 / 移动到固定", "03 / Moving to fixed"],
  ["04 / 对数前沿", "04 / Logarithmic frontier"],
  ["05 / 端点边界", "05 / Endpoint boundary"],
  ["06 / 文献边界", "06 / Literature boundary"],
  ["08 / 结论边界", "08 / Conclusion boundary"],
  ["23 项证据与缺口矩阵", "23-item evidence and gap matrix"],
  ["82 项验证记录", "82-item validation record"],
  ["常数取到足够小时，\\(B_{R/2}(x_0)\\subset X_R(t)+B_R\\)。固定柱中的三次速度量于是满足", "For a sufficiently small constant, \\(B_{R/2}(x_0)\\subset X_R(t)+B_R\\). The cubic velocity quantity in the fixed cylinder therefore satisfies"],
  ["单尺度 epsilon 桥：PROVED", "One-scale epsilon bridge: PROVED"],
  ["当 \\(P_R^M\\le1\\) 时，线性项由 \\(P^{2/3}\\) 吸收：", "When \\(P_R^M\\le1\\), the linear term is absorbed by \\(P^{2/3}\\):"],
  ["低于平方根对数的普适修复全部失败", "Every universal repair below the square-root logarithm fails"],
  ["独立复算 269 字段：FINITE", "Independent reconstruction of 269 fields: FINITE"],
  ["端点上界与尺度传播：OPEN", "Endpoint upper bound and scale propagation: OPEN"],
  ["对笔记范围内的每个周期适合弱解和每个固定可容许尺度 \\(R\\)，终端锚定的光滑化轨迹可用于局部能量不等式，并得到", "For every periodic suitable weak solution in the scope of the note and every fixed admissible scale \\(R\\), the terminally anchored mollified trajectory can be used in the local energy inequality, yielding"],
  ["对所有声明范围内的光滑周期解与尺度成立。该障碍沿高度稀疏的实际支付序列出现，不是对每个大实数 \\(P\\) 的点态下界。", "for all smooth periodic solutions and scales in the stated scope. This obstruction occurs along a highly lacunary sequence of actual payments; it is not a pointwise lower bound for every large real \\(P\\)."],
  ["固定尺度 Caratheodory 路径、移动测试可容许性、Version-M 弱解双区间估计、路径受限与固定柱包含、仅速度的一尺度 epsilon 桥，以及 \\(\\gamma<1/2\\) 的对数修复排除。", "The fixed-scale Caratheodory path, admissibility of the moving test, the Version-M suitable-weak two-regime estimate, path confinement and fixed-cylinder inclusion, the velocity-only one-scale epsilon bridge, and exclusion of logarithmic repairs with \\(\\gamma<1/2\\)."],
  ["检查移动能量小量能否跨尺度传播，并分别决定平方根对数端点上界与匹配支付下界；在此之前不作全局正则性外推。", "Test whether moving-energy smallness propagates across scales, and decide the square-root-log endpoint upper bound and matching payment lower bound separately; no global-regularity extrapolation is made before then."],
  ["解析证明、有限复算与开放命题分开", "Analytic proofs, finite reconstructions, and open claims are separated"],
  ["精确双包家族同时排除了所有低于平方根对数的普适修复；\\(\\gamma=1/2\\) 只是第一个未被否定的端点，不是已证明上界。奇点处所需小量从何而来，仍然开放。", "The exact two-packet family excludes every universal repair below the square-root logarithm; \\(\\gamma=1/2\\) is only the first endpoint not ruled out, not a proved upper bound. The source of the required smallness at a singular point remains open."],
  ["路径受限后，固定半径柱落入移动管", "Path confinement places a fixed-radius cylinder inside the moving tube"],
  ["没有排除所有奇点、证明全局光滑或构造 blow-up；", "It does not exclude all singularities, prove global smoothness, or construct blow-up;"],
  ["没有证明平方根对数端点上界；", "It does not prove the square-root-log endpoint upper bound;"],
  ["没有证明任何可能奇点自动满足小量条件；", "It does not prove that any possible singular point automatically satisfies the smallness condition;"],
  ["没有证明小量从一个移动尺度传播到更小尺度；", "It does not prove propagation of smallness from one moving scale to a smaller scale;"],
  ["没有主张新颖性或发表优先权。", "No novelty or publication-priority claim is made."],
  ["任意三维初值的全局正则性与 Clay 千禧年问题仍然开放。", "Global regularity for arbitrary three-dimensional initial data and the Clay Millennium Problem remain open."],
  ["弱解扩展独立审计", "Independent suitable-weak extension audit"],
  ["适合弱解的 Version-M 移动管门、单尺度 epsilon 桥与平方根对数支付边界", "Suitable-weak Version-M moving-tube gate, one-scale epsilon bridge, and square-root-log payment boundary"],
  ["双语边界词典", "Bilingual boundary dictionary"],
  ["图件 82/82：FINITE", "Figure checks 82/82: FINITE"],
  ["图件 manifest", "Figure manifest"],
  ["限定式主源检索没有找到相同的 Version-M 支付、正环带通量、移动到固定包含与局部标量支付组合。这只是 finite non-hit，不证明新颖性或优先权。", "A bounded primary-source search did not find the same combination of Version-M payment, positive collar flux, moving-to-fixed inclusion, and local scalar payment. This is only a finite non-hit and does not establish novelty or priority."],
  ["小移动能量进入已有的一尺度判据", "Small moving energy enters an established one-scale criterion"],
  ["研究笔记 R0.74I · 完整中文版本", "Research note R0.74I · complete Chinese version"],
  ["一尺度门已经存在，缺的是小量来源与传播", "The one-scale gate exists; the source and propagation of smallness are missing"],
  ["移动管正则门与对数指数筛选", "Moving-tube regularity gate and logarithmic exponent screen"],
  ["移动轨迹与斜柱已有直接先例", "Moving trajectories and skewed cylinders have direct precedents"],
  ["因此，对每个固定 \\(\\gamma<1/2\\)，不存在统一常数使", "Therefore, for every fixed \\(\\gamma<1/2\\), no uniform constant makes"],
  ["在精确 R0.74F--H 双包族上，对 \\(Y_j=X_j\\) 和 \\(Y_j=\\mathfrak C_j\\)，Version M 与 Version F 都有", "On the exact R0.74F--H two-packet family, for \\(Y_j=X_j\\) and \\(Y_j=\\mathfrak C_j\\), both Version M and Version F satisfy"],
  ["在平方根对数端点，现有论证只给正的下比值，不给发散。任何普适端点上界都会迫使尚未证明的匹配支付下界", "At the square-root-log endpoint, the current argument gives only a positive lower ratio, not divergence. Any universal endpoint upper bound would force the still-unproved matching payment lower bound"],
  ["这两个命题都以某一给定尺度上的小量为前提。本节没有证明可能奇点处的 \\(P_R^M\\) 或移动能量必然小。", "Both statements assume smallness at a given scale. This section does not prove that \\(P_R^M\\) or the moving energy must be small at a possible singular point."],
  ["这是固定尺度、逐解成立的 Version-M 结果。Version F 的适合弱解扩展没有证明。", "This Version-M result holds solution by solution at a fixed scale. The suitable-weak extension of Version F is not proved."],
  ["这只是条件推论。不得把它写成冻结解族已经具有的下界，也不得把平方根对数称为已完成的上界定理。", "This is only a conditional implication. It must not be stated as a lower bound already possessed by the frozen solution family, and the square-root logarithm must not be called a completed upper-bound theorem."],
  ["证书 36/36：FINITE", "Certificate 36/36: FINITE"],
  ["终端锚定路径满足 \\(\\dot X_R=u_R(t,X_R)\\)。小移动能量给出", "The terminally anchored path satisfies \\(\\dot X_R=u_R(t,X_R)\\). Small moving energy gives"],
  ["主源文献边界", "Primary-source literature boundary"],
  ["状态 · R0.74I", "Status · R0.74I"],
  ["最后一步调用已有的仅速度一尺度 epsilon 正则判据；移动管本身并不自动产生正则性。", "The final step invokes an established velocity-only one-scale epsilon-regularity criterion; the moving tube itself does not automatically produce regularity."],
  ["epsilon 与对数独立审计", "Independent epsilon and logarithmic audit"],
  ["Python 证书 36/36；独立 Ruby 复算 36/36，核对 269 个终端字段且零差异。图件 validator 82/82，24 文件封存通过。有限证书只核对指数代数和图件，不证明 PDE 论证。", "The Python certificate passes 36/36 checks; the independent Ruby reconstruction passes 36/36, compares 269 terminal fields, and finds zero differences. The figure validator passes 82/82 and seals 24 files. These finite certificates check exponent algebra and the figure only; they do not prove the PDE argument."],
  ["R0.74H 的双区间估计原本只覆盖光滑周期解。本节把 Version M 推到适合弱解，并证明：若某一尺度上的移动局部能量足够小，就能进入已有的固定柱仅速度 epsilon 正则判据。", "The R0.74H two-regime estimate originally covered only smooth periodic solutions. This section extends Version M to suitable weak solutions and proves that sufficiently small moving local energy at one scale enters an established fixed-cylinder velocity-only epsilon-regularity criterion."],
  ["SVG 是网页主图；PNG 是回退与 600 dpi 归档，PDF 是矢量下载。图是严格蕴含与指数筛选图，不是 DNS、数值仿真或实验数据。", "SVG is the primary web figure; PNG is the fallback and 600 dpi archive, and PDF is the vector download. The figure is a strict implication and exponent-screening diagram, not DNS, numerical simulation, or experimental data."],
  ["Version M 保留双区间估计", "Version M retains the two-regime estimate"],
  ["Version-F 弱解扩展、奇点处小量机制、跨尺度轨迹比较、端点上界、匹配支付下界与通量的序列稳定性。", "The suitable-weak extension of Version F, a smallness mechanism at singular points, cross-scale trajectory comparison, the endpoint upper bound, the matching payment lower bound, and sequence-level flux stability."],
  ["Version-M 弱解闭合：PROVED", "Version-M suitable-weak closure: PROVED"],
  ["Yang 与 Vasseur--Yang 已使用光滑化流轨迹、参考时刻锚定和单侧后向斜柱；这些几何成分不主张新颖。固定柱插值与仅速度 epsilon 判据也来自已有文献。", "Yang and Vasseur--Yang already use mollified flow trajectories, reference-time anchoring, and one-sided backward skewed cylinders; no novelty is claimed for those geometric ingredients. The fixed-cylinder interpolation and velocity-only epsilon criterion also come from existing literature."],
  ["211 篇研究笔记总索引", "Master index of 211 research notes"],
  ["89 节完整封存", "89 sections fully sealed"],
  ["查看首页 R0.74I 卡片", "View the R0.74I homepage card"],
  ["当前端点 R0.74I", "Current endpoint R0.74I"],
  ["低于平方根对数的修复失败；端点上界、奇点处小量与尺度传播仍开放。", "Repairs below the square-root logarithm fail; the endpoint upper bound, smallness at singular points, and scale propagation remain open."],
  ["环带通量修复 → 适合弱解移动管 → 单尺度 epsilon 门 → 平方根对数边界", "collar-flux repair → suitable-weak moving tube → one-scale epsilon gate → square-root-log boundary"],
  ["检查移动能量小量的尺度传播，并分别处理平方根对数端点上界与匹配支付下界。", "Test the scale propagation of moving-energy smallness, and treat the square-root-log endpoint upper bound and matching payment lower bound separately."],
  ["跳到首页 R0.74I 卡片 →", "Jump to the R0.74I homepage card →"],
  ["研究笔记 R0.74I · 2026-09-02", "Research note R0.74I · 2026-09-02"],
  ["阅读 R0.74I 完整中文笔记 →", "Read the complete Chinese R0.74I note →"],
  ["阅读最新 R0.74I 研究笔记 →", "Read the latest R0.74I research note →"],
  ["展开 121 篇公开笔记", "Expand 121 public notes"],
  ["综述 v1.75 · 2026-09-02", "Review v1.75 · 2026-09-02"],
  ["R0.60 recap 之后的累计回顾收录 140 个节点；全站现有 211 篇公开研究笔记", "The cumulative review after the R0.60 recap contains 140 nodes; the site now has 211 public research notes"],
  ["R0.70A–R0.74I · 113 节已公开", "R0.70A–R0.74I · 113 sections published"],
  ["R0.70A–R0.74I：113 节已公开，89 节完整封存", "R0.70A–R0.74I: 113 sections published, 89 fully sealed"],
  ["R0.74I 已把 Version M 推到适合弱解，并建立给定尺度小移动能量到既有 epsilon 判据的桥。下一步要解释小量如何在可能奇点处出现或跨尺度传播；平方根对数端点也仍开放。", "R0.74I extends Version M to suitable weak solutions and builds a bridge from small moving energy at a given scale to an established epsilon criterion. The next step is to explain how smallness arises at a possible singular point or propagates across scales; the square-root-log endpoint also remains open."],
  ["R0.74I：适合弱解移动管门与平方根对数边界", "R0.74I: Suitable-weak moving-tube gate and square-root-log boundary"],
  ["R0.74I｜适合弱解的移动管门与平方根对数支付边界", "R0.74I｜Suitable-weak moving-tube gate and square-root-log payment boundary"],
  ["R0.74I｜适合弱解移动管门", "R0.74I｜Suitable-weak moving-tube gate"],
  ["R0.74J 下一接口", "R0.74J next interface"],
  ["Version M 已推进到适合弱解；给定尺度上的小移动能量进入既有固定柱 epsilon 判据。所有 gamma<1/2 的对数修复被排除，端点仍开放。", "Version M now covers suitable weak solutions; small moving energy at a given scale enters an established fixed-cylinder epsilon criterion. Every logarithmic repair with gamma<1/2 is excluded, while the endpoint remains open."],
  ["Version M 已推进到适合弱解；给定尺度上的小移动能量进入已有 epsilon 判据。低于平方根对数的修复失败，端点上界仍开放。", "Version M now covers suitable weak solutions; small moving energy at a given scale enters an established epsilon criterion. Repairs below the square-root logarithm fail, while the endpoint upper bound remains open."],
  ["Version M 已推进到适合弱解；给定尺度上的小移动能量进入已有的一尺度 epsilon 判据。", "Version M now covers suitable weak solutions; small moving energy at a given scale enters an established one-scale epsilon criterion."],
];

const map = new Map(pairs);
assert.equal(map.size, pairs.length, "duplicate R0.74I Chinese translation keys");
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
    assert.equal(currentByZh.get(zh)?.en, en, `R0.74I translation drift: ${zh}`);
} else {
  for (const entry of missingBefore)
    assert.ok(map.has(entry.zh), `untranslated R0.74I source string: ${entry.zh}`);
  const additions = missingBefore.map((entry, index) => ({
    id: `r074i${String(current.filter((row) => /^r074i\d+$/.test(row.id)).length + index + 1).padStart(3, "0")}`,
    ...entry,
    en: map.get(entry.zh),
  }));
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(JSON.stringify({
  release: "R0.74I",
  translationPath: translationRoute,
  dgxUsed,
  checked: map.size,
  applied: !checkOnly,
}, null, 2) + "\n");
