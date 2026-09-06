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
const prefix = "claybadjointweaktracescreen20260906";

const translations = new Map([
  ["本轮核读四个原始接口：", "This round checked four primary interfaces:"],
  ["文献综述 v2.64 · 2026-09-06", "Literature review v2.64 · 2026-09-06"],
  ["阅读完整 CB.20 笔记", "Read the complete CB.20 note"],
  ["CB.20 · Clay-B 弱初迹伴随的文献和主张边界", "CB.20 · Literature and claim boundary for the Clay-B weak-trace adjoint"],
  ["CB.20 · ClayB-AdjointWeakTraceScreen-20260906 公开边界", "CB.20 · Public boundary for ClayB-AdjointWeakTraceScreen-20260906"],
  ["CONDITIONAL ENDPOINT AUDIT：在 BP 的额外正终端能量原子条件下，反时共同伴随是前向正黏性、压力耦合向量解，具有弱零初迹和单位能量右极限；反时漂移本身满足负黏性方程。FINITE-MODE FLUX：Π_N 对每个正时间几乎处处趋零，但固定初端窗口积分趋于 1/2，对 C¹ 时间测试趋于 δ₀/2；极限泛函有 Radon 表示，未证明通量测度总变差一致有界、测度弱星收敛或 suitable 缺陷测度识别。UNPAID TRACE INTERFACE：原子条件迫使投影张量散度与 w_t 的 L²H⁻¹ 范数及张量时空 L² 范数在每个初端区间无限；额外 Serrin 条件足够但不是基本能量。LITERATURE：ESS 的方向/迹/闭合条件、Lei 的有界 mild 全空间 NS 解类、CL 的临界压力对偶输入、BCC 的标量凸测试均不能原样导入。CL A.1–A.3 是 Theorems，C_tL³ 不可弱化为任意 L∞_tL³。该四项筛选不证明穷尽性文献缺失或新颖性。FINITE CHECKS ONLY：三份文本源、18 个 BS 标签、135/135 文件绑定、15 项算术检查和 3 项有限负对照不替代 PDE 证明。原子存在/排除、压力感知凸测试、G、一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "CONDITIONAL ENDPOINT AUDIT: under BP's additional positive-terminal-energy-atom condition, the reversed common adjoint is a forward positive-viscosity pressure-coupled vector solution with weak-zero initial trace and a unit-energy right limit; the reversed drift itself obeys a negative-viscosity equation. FINITE-MODE FLUX: Π_N tends to zero almost everywhere at positive times, but its integral over each fixed initial window tends to 1/2, and it tends to δ₀/2 against C¹ time tests. The limiting functional has a Radon representation, but no uniform total variation of the flux measures, measure weak-star convergence, or identification with a suitable defect measure is proved. UNPAID TRACE INTERFACE: the atom condition forces the projected tensor divergence and w_t to have infinite L²H⁻¹ norm, and the tensor to have infinite spacetime L² norm, on every initial interval. An additional Serrin condition is sufficient but is not basic energy. LITERATURE: the direction, trace, and closure conditions in ESS; Lei's bounded mild full-space NS solution class; CL's critical pressure-duality input; and BCC's scalar convex test cannot be imported unchanged. CL A.1–A.3 are Theorems, and C_tL³ cannot be weakened to arbitrary L∞_tL³. This four-interface screen proves neither exhaustive literature absence nor novelty. FINITE CHECKS ONLY: three text sources, 18 BS labels, 135/135 file bindings, 15 arithmetic checks, and three limited negative controls do not replace PDE proof. Atom existence/exclusion, the pressure-aware convex test, G, and general regularity remain OPEN. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["PDF 1–3 页；", "PDF pages 1–3;"],
  ["PDF 1–3、32–34 页及 Appendix A；", "PDF pages 1–3 and 32–34, including Appendix A;"],
  ["PDF 1–3、9–10 页；", "PDF pages 1–3 and 9–10;"],
  ["PDF 1、5–9 页，并完整读 Lemma 2.6 与 Theorem 2.7 的使用接口。没有把实际核读范围扩大成全篇证明重审。", "PDF pages 1 and 5–9, including the complete interfaces used from Lemma 2.6 and Theorem 2.7. The actual reading range is not expanded into a claim of full-proof review."],
  ["伴随的弱零初迹：边界通量与唯一性接口", "Weak-zero trace of the adjoint: boundary flux and uniqueness interfaces"],
  ["研究笔记总索引 · v2.64 · 2026-09-06", "Research-note master index · v2.64 · 2026-09-06"],
  ["CB.1–CB.20 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.20 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["额外 L²H⁻¹、张量 L² 或 Serrin 漂移条件会给强初迹并排除该跳跃，但基本能量没有支付。ESS、Lei–Yang–Yuan、Cheskidov–Luo 与 Bonicatto–Ciampa–Crippa 四个接口都不能在不增加假设时原样导入；这不是穷尽性文献结论。", "Additional L²H⁻¹, tensor L², or Serrin drift conditions would give a strong initial trace and exclude the jump, but basic energy does not pay them. The four interfaces of ESS, Lei–Yang–Yuan, Cheskidov–Luo, and Bonicatto–Ciampa–Crippa cannot be imported unchanged without additional assumptions. This is not an exhaustive literature conclusion."],
  ["反时共同伴随的零迹位于前向方程初端，但能量右极限为一。有限 Fourier 通量对 C¹ 时间测试趋于 δ₀/2，并非已证明的缺陷测度；额外 L²H⁻¹、张量 L² 或 Serrin 输入仍未支付。四文献核查是有限适用性筛选，不是穷尽性或新颖性结论。G OPEN。NOT CLAY.", "The reversed common adjoint has zero trace at the initial endpoint of a forward equation, but its energy right limit is one. The finite Fourier flux tends to δ₀/2 against C¹ time tests, not to an identified defect measure. Additional L²H⁻¹, tensor L², or Serrin input remains unpaid. The four-source check is a bounded applicability screen, not an exhaustive or novelty conclusion. G OPEN. NOT CLAY."],
  ["前向弱零初迹与精确边界通量", "forward weak-zero initial trace and exact boundary flux"],
  ["弱初迹端点核查已进入 CB.20", "The weak-trace endpoint audit has entered CB.20"],
  ["四个接口均有未付输入", "all four interfaces have unpaid inputs"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.20 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.20 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：压力感知的有界凸测试", "Next research action: a bounded pressure-aware convex test"],
  ["压力感知凸测试与一般正则性 OPEN · NOT CLAY", "pressure-aware convex testing and general regularity OPEN · NOT CLAY"],
  ["阅读 CB.20 HTML", "Read CB.20 HTML"],
  ["阅读最新 CB.20 弱初迹笔记 →", "Read the latest CB.20 weak-trace note →"],
  ["只检查同一 b,w 上完整保留压力、交换子和极限顺序的凸测试，是否产生比 BS 初端预算更强且已支付的信息。该审计尚未开始。", "Check only whether a convex test for the same b,w, retaining pressure, commutators, and the order of limits, yields stronger information than the BS initial-endpoint budget that is already paid. This audit has not started."],
  ["综述 v2.64 · 2026-09-06", "Research review v2.64 · 2026-09-06"],
  ["BS 把共同伴随反时为前向正黏性、压力耦合向量方程：初迹分布意义下为零，但能量右极限为一。有限 Fourier 通量对 C¹ 时间测试趋于边界泛函 δ₀/2，正时间几乎处处趋零，因而不一致可积。", "BS reverses the common adjoint into a forward positive-viscosity pressure-coupled vector equation. Its initial trace is zero in distributions, but its energy right limit is one. The finite Fourier flux tends to the boundary functional δ₀/2 against C¹ time tests, while tending to zero almost everywhere at positive times, and is therefore not uniformly integrable."],
  ["BS 已校准时间方向、弱初迹、有限模态通量和四个原始唯一性接口；结果见下一个正式路线节点。", "BS calibrates the time direction, weak initial trace, finite-mode flux, and four primary uniqueness interfaces. The result appears in the next formal route node."],
  ["CB.1–CB.20 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.20 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.20｜伴随的弱零初迹：边界通量与唯一性接口", "CB.20 | Weak-zero trace of the adjoint: boundary flux and uniqueness interfaces"],
  ["CB.21 只是下一章占位，不是已完成研究。压力感知凸测试、通量一致可积、原子存在或排除、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。", "CB.21 is only a next-chapter placeholder, not completed research. Pressure-aware convex testing, flux uniform integrability, atom existence or exclusion, G, arbitrary-singularity input generation, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.20", "The independent Clay-B route stops at CB.20"],
  ["Clay-B 弱初迹伴随笔记快捷入口", "Clay-B weak-trace adjoint note shortcuts"],
  ["Clay-B 弱初迹筛查结论", "Clay-B weak-trace screen conclusions"],
  ["Clay-B 已把共同伴随的唯一性问题校准为弱初迹端点通量：反时后是前向压力耦合方程，有限 Fourier 通量对 C¹ 时间测试趋于 δ₀/2，但总变差、测度弱星收敛和 suitable 缺陷识别均未证明。四个已核读唯一性接口仍需未付输入。下一步只检查压力感知的有界凸测试。", "Clay-B has calibrated the common-adjoint uniqueness question as a weak-trace endpoint flux. After time reversal it is a forward pressure-coupled equation, and the finite Fourier flux tends to δ₀/2 against C¹ time tests, but total variation, measure weak-star convergence, and suitable-defect identification are unproved. The four checked uniqueness interfaces still require unpaid inputs. The next step checks only a bounded pressure-aware convex test."],
]);

function validateTranslation(source, en) {
  assert.ok(!containsChinese(en), "Chinese remains in translation: " + source);
  assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(source), "protected token drift: " + source);
}

process.chdir(root);
const [source, current] = await Promise.all([collectSiteStrings(publicRoot), readFile(translationPath, "utf8").then(JSON.parse)]);
const rowPattern = new RegExp("^" + prefix + "\\d+$");
if (checkOnly) {
  const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
  assert.deepEqual(source.filter((entry) => !currentByZh.has(entry.zh)), [], "site still has untranslated Chinese strings");
  const rows = current.filter((entry) => rowPattern.test(entry.id));
  assert.equal(rows.length, translations.size, "AdjointWeakTraceScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.20"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "AdjointWeakTraceScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-AdjointWeakTraceScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
