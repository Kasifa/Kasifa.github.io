#!/usr/bin/env node

import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const checkOnly = process.argv.includes("--check-only");
const prefix = "claybsameparentresidual20260906";

const translations = new Map([
  ["查看来源与主张边界", "View sources and claim boundary"],
  ["幅度一致压力功与自压力 OPEN · NOT CLAY", "amplitude-uniform pressure work and self-pressure OPEN · NOT CLAY"],
  ["混合压力普通时间 little-o", "ordinary-time little-o for mixed pressure"],
  ["混合张量 z⊗w 在全时间变量上趋零；完整周期混合压力 r=Π(z,w) 在负 Sobolev 范数消失，并有相对 h_w+h_z 的普通时间 little-o。没有临界速率、幅度一致压力功或对 BT 半单位端点的分量归属。", "The mixed tensor z⊗w tends to zero along the full time variable. The full-periodic mixed pressure r=Π(z,w) vanishes in negative Sobolev norms and has ordinary-time little-o relative to h_w+h_z. There is no critical rate, amplitude-uniform pressure work, or componentwise assignment of the BT half-unit endpoint."],
  ["目标点无残差原子与已付源方程", "no residual atom at the target and an equation with a paid source"],
  ["同一原解残差核算已进入 CB.22", "The same-parent residual calculation has entered CB.22"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.22 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.22 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：有符号幅度压力功", "Next research action: signed amplitude pressure work"],
  ["阅读 CB.22 HTML", "Read CB.22 HTML"],
  ["阅读最新 CB.22 残差笔记 →", "Read the latest CB.22 residual note →"],
  ["在 BP 正原子条件下，z=b+√m w 的终端能量测度 μ_res=μ_*−mδ_a 在目标点 a 无原子；z 满足保留 −2νΔb 源的正向抛物方程。固定截止端点合法，目标球内只得到未缩放对角小量。", "Under the BP positive-atom condition, the terminal energy measure μ_res=μ_*−mδ_a of z=b+√m w has no atom at the target a. The field z obeys a forward parabolic equation retaining the source −2νΔb. Fixed-cutoff endpoints are legitimate, and only unscaled diagonal smallness is obtained in the target ball."],
  ["正原子条件下，对齐残差测度在目标点无原子，正向残差方程保留 −2νΔb 源；混合张量全时间消失，完整周期混合压力得到普通时间 little-o。幅度一致压力功、自压力、强 L² 初迹与原子排除仍 OPEN。NOT CLAY.", "Under the positive-atom condition, the alignment-residual measure has no atom at the target, and the forward residual equation retains the source −2νΔb. The mixed tensor vanishes along the full time variable, and full-periodic mixed pressure has ordinary-time little-o. Amplitude-uniform pressure work, self-pressure, strong L² initial trace, and atom exclusion remain OPEN. NOT CLAY."],
  ["只检查混合压力的有符号时间积分能否得到不随 R 增长的控制；即使混合项关闭，自压力仍须单独分析。该审计尚未开始。", "Check only whether the signed time integral of mixed pressure admits control that does not grow with R. Even if the mixed term closes, self-pressure still requires separate analysis. This audit has not started."],
  ["综述 v2.66 · 2026-09-06", "Research review v2.66 · 2026-09-06"],
  ["BU 已把目标点残差测度、保留源的正向方程和完整周期混合压力小量写成正式结论；结果见下一个路线节点。", "BU formalizes the target-point residual measure, the forward equation retaining its source, and full-periodic mixed-pressure smallness. The result appears in the next route node."],
  ["CB.1–CB.22 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.22 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.22｜同一原解的对齐残差：能量、混合压力与终端边界", "CB.22 | Same-parent alignment residual: energy, mixed pressure, and terminal boundary"],
  ["CB.23 只是下一章占位，不是已完成研究。幅度一致混合压力功、自压力端点、原子存在或排除、强 L² 初迹、G、R.216–R.217、一般正则性与 Clay 均未关闭。", "CB.23 is only a next-chapter placeholder, not completed research. Amplitude-uniform mixed-pressure work, the self-pressure endpoint, atom existence or exclusion, strong L² trace, G, R.216–R.217, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.22", "The independent Clay-B route stops at CB.22"],
  ["Clay-B 同一原解残差笔记快捷入口", "Clay-B same-parent residual note shortcuts"],
  ["Clay-B 同一原解残差结论", "Clay-B same-parent residual conclusions"],
  ["Clay-B 已把同一原解的终端对齐展开为残差测度、带源正向方程和完整周期混合压力：目标点无残差原子，混合张量全时间消失，且混合压力相对能量梯度预算有普通时间 little-o；但幅度一致压力功、自压力端点、强 L² 与原子排除仍未闭合。下一步只检查有符号幅度压力功。", "Clay-B has expanded the same-parent terminal alignment into a residual measure, a forced forward equation, and full-periodic mixed pressure. The residual has no atom at the target, the mixed tensor vanishes along the full time variable, and mixed pressure has ordinary-time little-o relative to the energy-gradient budget. But amplitude-uniform pressure work, the self-pressure endpoint, strong L² trace, and atom exclusion remain open. The next step checks only signed amplitude pressure work."],
  ["本轮根任务完整重读已冻结 BP 正原子共同伴随章节与 BT §§1–5，并只重新打开", "This root-task round fully reread the frozen BP positive-atom common-adjoint chapter and BT §§1–5, and reopened only"],
  ["的元数据和摘要；没有重新读取该 PDF 或导入新的外部定理。周期有限指数 Leray/CZ 与 Sobolev 工具沿用 BP/BL 已核查接口。团队成员的有界历史比较只作内部去重，不扩大为根任务亲读范围、文献穷尽或新颖性结论。", "metadata and abstract. It did not reread the PDF or import a new external theorem. The finite-exponent periodic Leray/CZ and Sobolev tools retain the checked BP/BL interfaces. Bounded historical comparisons by team members serve only internal deduplication and do not expand the root task's direct reading range or support an exhaustive-literature or novelty conclusion."],
  ["文献综述 v2.66 · 2026-09-06", "Literature review v2.66 · 2026-09-06"],
  ["阅读完整 CB.22 笔记", "Read the complete CB.22 note"],
  ["CB.22 · Clay-B 同一原解残差的来源和主张边界", "CB.22 · Sources and claim boundary for the Clay-B same-parent residual"],
  ["CB.22 · ClayB-SameParentResidual-20260906 公开边界", "CB.22 · Public boundary for ClayB-SameParentResidual-20260906"],
  ["CONDITIONAL：全部 BU 结论假设 BP 的同一光滑无外力周期 NS 原解、目标点正终端原子 mδ_a、共同饱和伴随、常配对及终端定位。RESIDUAL MEASURE：z=b+√m w 的连续测试终端测度是 μ_res=μ_*−mδ_a≥0 且 μ_res({a})=0；交叉测度来自常配对和定位，不是弱极限乘法，背景能量及其他原子可以保留。PAID FORCED EQUATION：相反黏性给 zρ+b·∇z+∇q=νΔz−2νΔb；源属于 L²H⁻¹，全部压力、截止和源梯度项保留。固定截止端点合法，初始残差能量表示终端测度而非强 L² 迹；只得到未缩放对角局部小量。MIXED PRESSURE：||z⊗w||₁ 在完整时间变量上趋零，r=Π(z,w) 在 H^{-s}、s>3/2 消失。光滑辅助截止只分割输入张量，完整周期 CZ 常数与半径无关且无截止导数，因比值不含半径，得到 ||r||_{L²L³ᐟ²}=o(h_w+h_z) 的普通 δ→0 little-o；没有时间速率或联合缩球尺度。AMPLITUDE GAP：π=r−√mΠ(w,w)；固定 R 的混合功上界仍含 R，L³ᐟ² 压力不能直接和仅有 L² 的凸测试导数配对，负范数也不支付随 R,w 变化的测试。BT 的 1/2 边界不能分别归给自压力或混合压力。FINITE CHECKS ONLY：三份文本源、20 个 BU 标签、149/149 文件绑定、20 项有理复算和 4 项有限负对照不替代 PDE 证明。原子存在或排除、强 L² 初迹、幅度一致压力功、G、R.216–R.217、一般正则性与新颖性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "CONDITIONAL: every BU conclusion assumes the BP same smooth unforced periodic NS parent, the positive terminal atom mδ_a at the target, the common saturated adjoint, constant pairing, and terminal localization. RESIDUAL MEASURE: the continuous-test terminal measure of z=b+√m w is μ_res=μ_*−mδ_a≥0 with μ_res({a})=0. The cross measure follows from constant pairing and localization, not multiplication of weak limits; background energy and other atoms may remain. PAID FORCED EQUATION: opposite viscosity gives zρ+b·∇z+∇q=νΔz−2νΔb. The source belongs to L²H⁻¹, and all pressure, cutoff, and source-gradient terms are retained. Fixed-cutoff endpoints are legitimate; initial residual energy denotes the terminal measure rather than a strong L² trace, and only unscaled diagonal local smallness follows. MIXED PRESSURE: ||z⊗w||₁ tends to zero along the full time variable, and r=Π(z,w) vanishes in H^{-s} for s>3/2. A smooth auxiliary cutoff splits only the input tensor; the full-periodic CZ constant is radius independent and has no cutoff derivative. Because the ratio contains no radius, ||r||_{L²L³ᐟ²}=o(h_w+h_z) is ordinary δ→0 little-o, with no time rate or jointly shrinking scale. AMPLITUDE GAP: π=r−√mΠ(w,w). The fixed-R mixed-work bound still contains R; L³ᐟ² pressure cannot be paired directly with a convex-test derivative controlled only in L², and the negative norm does not pay for a test varying with R,w. The BT 1/2 boundary cannot be assigned separately to self-pressure or mixed pressure. FINITE CHECKS ONLY: three text sources, 20 BU labels, 149/149 file bindings, 20 rational recomputations, and four limited negative controls do not replace PDE proof. Atom existence or exclusion, strong L² trace, amplitude-uniform pressure work, G, R.216–R.217, general regularity, and novelty remain OPEN. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["同一原解的对齐残差：能量、混合压力与终端边界", "Same-parent alignment residual: energy, mixed pressure, and terminal boundary"],
  ["研究笔记总索引 · v2.66 · 2026-09-06", "Research-note master index · v2.66 · 2026-09-06"],
  ["CB.1–CB.22 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.22 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
]);

function validateTranslation(source, en) {
  assert.ok(!containsChinese(en), "Chinese remains in translation: " + source);
  assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(source), "protected token drift: " + source);
}

process.chdir(root);
const [source, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp("^" + prefix + "\\d+$");
if (checkOnly) {
  const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
  assert.deepEqual(source.filter((entry) => !currentByZh.has(entry.zh)), [], "site still has untranslated Chinese strings");
  const rows = current.filter((entry) => rowPattern.test(entry.id));
  assert.equal(rows.length, translations.size, "SameParentResidual translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.22"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "SameParentResidual source-string count drift");
  const additions = missing.map((entry, index) => {
    const en = translations.get(entry.zh);
    assert.equal(typeof en, "string", "missing local translation: " + entry.zh);
    validateTranslation(entry.zh, en);
    return { id: prefix + String(index + 1).padStart(3, "0"), ...entry, en };
  });
  await writeFile(translationPath, JSON.stringify([...base, ...additions], null, 2) + "\n");
  const built = spawnSync(process.execPath, ["scripts/build-i18n.mjs", "translations/en.json"], { cwd: root, encoding: "utf8" });
  assert.equal(built.status, 0, built.stdout + "\n" + built.stderr);
}

process.stdout.write(JSON.stringify({ release: "ClayB-SameParentResidual-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
