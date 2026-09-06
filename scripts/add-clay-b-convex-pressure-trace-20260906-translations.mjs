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
const prefix = "claybconvexpressuretrace20260906";

const translations = new Map([
  ["幅度端点仍承担 δ₀/2", "the amplitude endpoint still carries δ₀/2"],
  ["固定凸测试与次二次强初迹", "fixed convex tests and subquadratic strong trace"],
  ["固定有界凸测试在压力梯度 L¹ 时间预算下得到精确恒等式，并推出所有 1≤q<2 的强零初迹；额外正原子下，撤去幅度截断仍重现 δ₀/2 的端点压力成本。强 L² 初迹、原子排除与一般正则性 OPEN。NOT CLAY.", "Fixed bounded convex tests have exact identities under the L¹ time budget for the pressure gradient and give strong-zero initial trace for every 1≤q<2. Under the additional positive atom, removing the amplitude cutoff still reproduces the endpoint pressure cost δ₀/2. Strong L² trace, atom exclusion, and general regularity remain OPEN. NOT CLAY."],
  ["同一原解对齐残差与强 L² OPEN · NOT CLAY", "same-parent alignment residual and strong L² OPEN · NOT CLAY"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.21 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.21 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：同一原解的对齐残差", "Next research action: the same-parent alignment residual"],
  ["有界凸压力测试已进入 CB.21", "The bounded convex pressure test has entered CB.21"],
  ["阅读 CB.21 HTML", "Read CB.21 HTML"],
  ["阅读最新 CB.21 凸压力笔记 →", "Read the latest CB.21 convex-pressure note →"],
  ["在额外正能量原子条件下，幅度 R→∞ 的压力通量仍对 C¹ 时间测试趋于 δ₀/2；低幅度能量估计与普遍消压局部测试分类都是必要校准，不排除原子，也不是一般正则性结论。", "Under the additional positive-energy-atom condition, the pressure flux for amplitude R→∞ still tends to δ₀/2 against C¹ time tests. The low-amplitude energy estimate and classification of local tests that universally cancel pressure are necessary calibrations; they neither exclude the atom nor prove general regularity."],
  ["只检查 b+√m w 的残差梯度是否产生当前未付的压力抵消或临界控制。该审计尚未开始。", "Check only whether the residual gradient of b+√m w produces a pressure cancellation or critical control that is currently unpaid. This audit has not started."],
  ["综述 v2.65 · 2026-09-06", "Research review v2.65 · 2026-09-06"],
  ["BT 已付清压力梯度可积性、固定凸测试和次二次强初迹，并校准幅度端点与普遍局部测试分类；结果见下一个正式路线节点。", "BT pays for pressure-gradient integrability, fixed convex tests, and subquadratic strong trace, and calibrates the amplitude endpoint and universal local-test classification. The result appears in the next formal route node."],
  ["BT 用有限指数 Leray 投影得到 ∇π∈L¹_tL³ᐟ²_x，并为每个固定有界凸测试建立含弱初端点的精确恒等式。特定 β_R 推出 ||w(t)||₁≤κ(t)，从而所有 1≤q<2 都有强零初迹，但不包括 q=2。", "BT uses finite-exponent Leray projection to obtain ∇π∈L¹_tL³ᐟ²_x and proves an exact identity including the weak initial endpoint for every fixed bounded convex test. A specific β_R gives ||w(t)||₁≤κ(t), hence strong-zero initial trace for every 1≤q<2, but not q=2."],
  ["CB.1–CB.21 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.21 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.21｜有界凸压力测试：次二次强初迹与幅度端点", "CB.21 | Bounded convex pressure tests: subquadratic strong trace and amplitude endpoint"],
  ["CB.22 只是下一章占位，不是已完成研究。同一原解对齐残差、非局部压力抵消、原子存在或排除、强 L² 初迹、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。", "CB.22 is only a next-chapter placeholder, not completed research. The same-parent alignment residual, nonlocal pressure cancellation, atom existence or exclusion, strong L² trace, G, arbitrary-singularity input generation, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.21", "The independent Clay-B route stops at CB.21"],
  ["Clay-B 已完成固定有界凸压力测试：能量类给出压力梯度时间 L¹ 可积性和所有 1≤q<2 的强零初迹；但额外正原子下撤去幅度截断仍重现 δ₀/2 的端点成本，强 L² 与原子排除没有闭合。下一步只检查同一原解的对齐残差。", "Clay-B has completed the fixed bounded convex pressure test. The energy class gives L¹ time integrability of the pressure gradient and strong-zero initial trace for every 1≤q<2. But under the additional positive atom, removing the amplitude cutoff still reproduces the endpoint cost δ₀/2; strong L² trace and atom exclusion do not close. The next step checks only the same-parent alignment residual."],
  ["Clay-B 有界凸压力笔记快捷入口", "Clay-B bounded convex pressure note shortcuts"],
  ["Clay-B 有界凸压力结论", "Clay-B bounded convex pressure conclusions"],
  ["本轮根任务复核", "This root-task round rechecked"],
  ["文献综述 v2.65 · 2026-09-06", "Literature review v2.65 · 2026-09-06"],
  ["元数据，并完整提取、视觉复读 PDF 6–8 页，包括 Definition 2.3、Lemma 2.6 和 Theorem 2.7 的完整证明。该文是标量连续性方程接口；本章的向量压力扩展是局部推导，不冒充原文结论。Vasseur、Frehse–Specovius-Neugebauer 等更宽读取只记作内部 B-only 范围，没有作为根任务完整核读或新增定理导入。", "metadata and fully extracted and visually reread PDF pages 6–8, including the complete proofs of Definition 2.3, Lemma 2.6, and Theorem 2.7. The paper provides a scalar continuity-equation interface; this chapter's vector-pressure extension is a local derivation and is not presented as a result from the paper. Wider reading of Vasseur, Frehse–Specovius-Neugebauer, and related sources is recorded only as an internal B-only range, not as root-task full reading or an imported additional theorem."],
  ["阅读完整 CB.21 笔记", "Read the complete CB.21 note"],
  ["CB.21 · Clay-B 有界凸压力测试的文献和主张边界", "CB.21 · Literature and claim boundary for the Clay-B bounded convex pressure test"],
  ["CB.21 · ClayB-ConvexPressureTrace-20260906 公开边界", "CB.21 · Public boundary for ClayB-ConvexPressureTrace-20260906"],
  ["PROVED IN STATED SCOPE：BT.1–BT.12 只假设固定三维环面、ν>0、无散 b,w∈L∞L²∩L²H¹、投影线性方程、w∈C_wL² 与弱零初迹；不假设原子、初始能量不等式或 b 满足 NS。PRESSURE INTEGRABILITY：有限指数投影给 ∇π∈L¹_tL³ᐟ²_x 和 κ(t)→0，不是 L²H⁻¹ 接口。DIRECT DERIVATION：每个固定光滑凸 β 若梯度与 Hessian 有界，则空间卷积、一个 L¹ 交换子、压力梯度形式与强 L² 梯度收敛给出含弱初端点的精确凸恒等式。SUBQUADRATIC TRACE：β_R 在 R↓0 后给 ||w(t)||₁≤κ(t) 与所有 1≤q<2 的强零初迹，不包括 q=2。CONDITIONAL ENDPOINT：只从 BT.13 起增加 BP 正原子；R→∞ 后幅度压力通量积分为 1/2，正时间几乎处处为零，对 C¹ 时间测试趋于 δ₀/2；无一致总变差、测度弱星收敛或 suitable 缺陷识别。AMPLITUDE ESCAPE：低幅度能量上界与 κ(t)||w(t)||∞≥||w(t)||²₂ 是必要约束，不是矛盾。BT.20 仅在几乎每个固定时间给等价有符号压力配对；只有有界梯度形式证明时空 L¹。LOCAL-TEST CLASSIFICATION：对每个独立光滑压力都普遍消压的 C² 状态局部测试只能是各向同性二次加仿射；该前提强于实际 NS，不排除同一 NS 压力、时空耦合或非局部测试。FINITE CHECKS ONLY：三份文本源、22 个 BT 标签、142/142 文件绑定、17 项算术或秩检查和 4 项有限负对照不替代 PDE 证明。非零弱零迹解、原子存在或排除、强 L² 初迹、对齐残差、G、一般正则性与新颖性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "PROVED IN STATED SCOPE: BT.1–BT.12 assumes only a fixed three-dimensional torus, ν>0, divergence-free b,w∈L∞L²∩L²H¹, the projected linear equation, w∈C_wL², and weak-zero initial trace. It assumes no atom, initial energy inequality, or NS equation for b. PRESSURE INTEGRABILITY: finite-exponent projection gives ∇π∈L¹_tL³ᐟ²_x and κ(t)→0, not the L²H⁻¹ interface. DIRECT DERIVATION: for every fixed smooth convex β with bounded gradient and Hessian, spatial convolution, one L¹ commutator, gradient-form pressure, and strong L² gradient convergence give the exact convex identity including the weak initial endpoint. SUBQUADRATIC TRACE: after R↓0, β_R gives ||w(t)||₁≤κ(t) and strong-zero initial trace for every 1≤q<2, not q=2. CONDITIONAL ENDPOINT: only BT.13 onward adds the BP positive atom. After R→∞, the amplitude pressure-flux integral is 1/2, the flux is zero almost everywhere at positive times, and it tends to δ₀/2 against C¹ time tests. No uniform total variation, measure weak-star convergence, or suitable-defect identification is proved. AMPLITUDE ESCAPE: the low-amplitude energy bound and κ(t)||w(t)||∞≥||w(t)||²₂ are necessary constraints, not a contradiction. BT.20 gives equivalent signed pressure pairings only at almost every fixed time; only the bounded-gradient form is proved spacetime L¹. LOCAL-TEST CLASSIFICATION: a C² state-local test that universally cancels every independent smooth pressure can only be an isotropic quadratic plus an affine function. This premise is stronger than actual NS pressure and does not exclude same-NS pressure or time-space-coupled or nonlocal tests. FINITE CHECKS ONLY: three text sources, 22 BT labels, 142/142 file bindings, 17 arithmetic or rank checks, and four limited negative controls do not replace PDE proof. A nonzero weak-zero-trace solution, atom existence or exclusion, strong L² trace, alignment residual, G, general regularity, and novelty remain OPEN. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["研究笔记总索引 · v2.65 · 2026-09-06", "Research-note master index · v2.65 · 2026-09-06"],
  ["有界凸压力测试：次二次强初迹与幅度端点", "Bounded convex pressure tests: subquadratic strong trace and amplitude endpoint"],
  ["CB.1–CB.21 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.21 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
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
  assert.equal(rows.length, translations.size, "ConvexPressureTrace translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.21"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "ConvexPressureTrace source-string count drift");
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

process.stdout.write(JSON.stringify({ release: "ClayB-ConvexPressureTrace-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
