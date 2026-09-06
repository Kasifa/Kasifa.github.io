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
const prefix = "clayblaggedpressurereduction20260906";

const translations = new Map([
  ["本章有限读取了", "This chapter makes a limited reading of"],
  ["的问题设置、Theorem 1.2、Proposition 3.1 完整陈述及 (3.7)–(3.15) 推导，只用于确认线性热项/非线性余量分解与热滞后本身不是新方法。该文的全空间统一临界 L³ 假设不属于当前周期能量框架，因此不调用其正则性结论；没有全文证明复审或穷尽新颖性检索。", "for its problem setting, Theorem 1.2, the complete statement of Proposition 3.1, and the derivation (3.7)–(3.15), only to confirm that the linear-heat/nonlinear-remainder split and heat lag are not new methods. Its whole-space uniform critical L³ hypothesis is outside the present periodic energy framework, so its regularity conclusion is not invoked. No full-proof review or exhaustive novelty search was performed."],
  ["文献综述 v2.56 · 2026-09-06", "Literature review v2.56 · 2026-09-06"],
  ["阅读完整 CB.12 笔记", "Read the complete CB.12 note"],
  ["CB.12 · Clay-B 滞后压力缩减的文献和主张边界", "CB.12 · Literature and claim boundary for the Clay-B lagged-pressure reduction"],
  ["CB.12 · ClayB-LaggedPressureReduction-20260906 公开边界", "CB.12 · Public boundary for ClayB-LaggedPressureReduction-20260906"],
  ["PROVED LOCALLY：AY 写全原 s_J 起点的时间有序压力并定位绝对值分拆成本；AZ 合法重选早时点并重建权重，但留下 A_J²Λ_A；BA/BB 保持 AQ 原 s_J、μ_J、坏集和 [s_J,t]，只另设窗口前热起点，并将旧压力控制为 εDχ+o(H_t)。CONDITIONAL REDUCTION：必要净工作只转到 Kχ(p(R))−(3/4−ε)Dχ，方向仍是下界而非上界。SUFFICIENT SCALE ONLY：τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹ 不是必要或最优；R 保留完整非线性源，不是自由小残差或无强迫 NS 解。FINITE CHECKS ONLY：八份文本源、98 个公式编号、51/51 文件哈希与 Fraction 指数核算不替代证明。OPEN：近期源自压力上界、实际 NS 输入、移动缩球 G、奇点排除与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。", "PROVED LOCALLY: AY writes the complete time-ordered pressure from the original s_J and locates the absolute-splitting costs. AZ legally reselects an early time and rebuilds the weight, but leaves A_J²Λ_A. BA/BB retain AQ's original s_J, μ_J, bad set, and [s_J,t], introduce only a separate pre-window heat start, and control old pressure by εDχ+o(H_t). CONDITIONAL REDUCTION: the necessary net work is transferred only to Kχ(p(R))−(3/4−ε)Dχ; the result remains a lower bound, not an upper bound. SUFFICIENT SCALE ONLY: τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹ is neither necessary nor optimal. R retains the complete nonlinear source and is not a freely small remainder or an unforced NS solution. FINITE CHECKS ONLY: eight text sources, 98 formula labels, 51/51 file hashes, and Fraction exponent arithmetic do not replace proof. OPEN: an upper bound for recent source pressure, actual NS inputs, moving shrinking G, singularity exclusion, and general regularity. No complete novelty review, external peer review, or Clay claim is made, and there is no figure, simulation, or cumulative recap. NOT CLAY."],
  ["旧热背景可以移走，近期源项仍待估计", "The old heat background can be removed; the recent source remains"],
  ["研究笔记总索引 · v2.56 · 2026-09-06", "Research-note master index · v2.56 · 2026-09-06"],
  ["CB.1–CB.12 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.12 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["保持 AQ 原 s_J、坏集、权重与积分域，在窗口前另设 Duhamel 热起点，可把旧压力控制为一份 εDχ 加 o(H_t)。必要净工作缩减到近期真实源自压力减剩余耗散；这仍是条件下界，不是上界。τ=Λ_A⁻⁸ᐟ³ 只是充分选择，近期源上界与 G 仍 OPEN。NOT CLAY.", "Retaining AQ's original s_J, bad set, weight, and integration domain while introducing a separate pre-window Duhamel heat start controls old pressure by one εDχ share plus o(H_t). The necessary net work is reduced to recent genuine source pressure minus the remaining dissipation; this is still a conditional lower bound, not an upper bound. τ=Λ_A⁻⁸ᐟ³ is only a sufficient choice. The recent-source upper bound and G remain OPEN. NOT CLAY."],
  ["固定 ε=1/8 与 AQ 原对象，检查 Kχ(p(R))−5Dχ/8 的 dyadic/Volterra 时间顺序。不能把 R 当作自由小残差，也不能重新使用已经支付旧压力的耗散份额。", "Fix ε=1/8 and AQ's original objects, then inspect the dyadic/Volterra time order of Kχ(p(R))−5Dχ/8. R cannot be treated as a freely small remainder, and the dissipation share already used to pay old pressure cannot be reused."],
  ["近期源上界与 G OPEN · NOT CLAY", "Recent-source upper bound and G OPEN · NOT CLAY"],
  ["旧压力：εDχ+o(H_t) 已付", "Old pressure: paid by εDχ+o(H_t)"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.12 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.12 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：近期源积分是否有动力学收益", "Next research question: does the recent-source integral yield a dynamical gain?"],
  ["阅读最新 CB.12 滞后压力缩减笔记 →", "Read the latest CB.12 lagged-pressure-reduction note →"],
  ["真实热滞后缩减已进入 CB.12", "The genuine heat-lag reduction now forms CB.12"],
  ["综述 v2.56 · 2026-09-06", "Review v2.56 · 2026-09-06"],
  ["AY–BB 已把窗口内起点的未付成本与窗口前滞后对旧压力的正面支付分开；结果见下一个正式路线节点。", "AY–BB now separate the unpaid costs of starting inside the window from the positive payment of old pressure by a pre-window lag; the result appears in the next formal route node."],
  ["AY/AZ 保留压力窗口内部起点时，分别留下热—实际耗散相关项或 A_J²Λ_A 的充分速率缺口；这些方法成本不是一般动力学 no-go。", "When AY/AZ retain a starting time inside the pressure window, they leave either a heat/actual-dissipation correlation or the sufficient A_J²Λ_A rate gap. These method costs are not a general dynamical no-go theorem."],
  ["BA/BB 在窗口前设置独立热起点，保持 AQ 原 s_J、坏集、μ_J 和 [s_J,t]。精确重组后，旧压力由一份 εDχ 和 o(H_t) 支付；τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹ 只是充分选择。剩余近期源自压力减耗散只有条件必要下界。", "BA/BB set a separate heat start before the window while retaining AQ's original s_J, bad set, μ_J, and [s_J,t]. After exact regrouping, old pressure is paid by one εDχ share and o(H_t); τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹ is only a sufficient choice. Recent source pressure minus dissipation retains only a conditional necessary lower bound."],
  ["CB.1–CB.12 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.12 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.11 原测试匹配界 → AY 原起点分拆成本 → AZ 联合早时速率缺口 → BA 窗口前真实热滞后 → BB 精确重组与充分尺度 → 近期源自压力上界 OPEN", "CB.11 original-test-matched bound → AY original-start splitting cost → AZ joint-early-time rate gap → BA genuine pre-window heat lag → BB exact regrouping and sufficient scale → recent source-pressure upper bound OPEN"],
  ["CB.12：滞后压力缩减", "CB.12: lagged-pressure reduction"],
  ["CB.12｜旧热背景可以移走，近期源项仍待估计", "CB.12 | The old heat background can be removed; the recent source remains"],
  ["CB.12｜旧热压力的耗散支付与近期源条件下界", "CB.12 | Dissipation payment for old heat pressure and a conditional lower bound for the recent source"],
  ["CB.13 只是下一章占位，不是已完成研究。近期源自压力上界、实际 NS 生成 R.216–R.217、缩球一致常数、移动路径、G/G-P/G-C 与首次奇点排除尚未冻结；不把候选源能量或 dyadic/Volterra 检查写成已证结论。", "CB.13 is only a placeholder for the next chapter, not completed research. The recent source-pressure upper bound, actual NS generation of R.216–R.217, shrinking-scale uniform constants, moving paths, G/G-P/G-C, and first-singularity exclusion are not frozen. Candidate source-energy or dyadic/Volterra checks are not presented as proved."],
  ["Clay-B 独立路线停在 CB.12", "The independent Clay-B route stops at CB.12"],
  ["Clay-B 已用窗口前真实热滞后支付所有含旧热分量的压力：成本是一份明确的 εDχ 加 o(H_t)，不是旧压力功自身 o(H_t)。必要净工作缩减到近期真实源自压力减剩余耗散；其上界、缩球路径和合同 G 继续开放。", "Clay-B now uses a genuine pre-window heat lag to pay every pressure term containing the old heat component. The cost is one explicit εDχ share plus o(H_t), not that old pressure work itself is o(H_t). The necessary net work is reduced to recent genuine source pressure minus the remaining dissipation; its upper bound, shrinking path, and contract G remain open."],
  ["Clay-B 滞后压力缩减笔记快捷入口", "Clay-B lagged-pressure-reduction note shortcuts"],
  ["Clay-B 滞后压力缩减结论", "Clay-B lagged-pressure-reduction result boundary"],
  ["τ=Λ_A⁻⁸ᐟ³：充分尺度", "τ=Λ_A⁻⁸ᐟ³: sufficient scale"],
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
  assert.equal(rows.length, translations.size, "LaggedPressureReduction translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.12"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "LaggedPressureReduction source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-LaggedPressureReduction-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
