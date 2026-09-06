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
const prefix = "claybplateauhistory20260906";

const translations = new Map([
  ["本节：平台能量历史", "This note: plateau energy history"],
  ["策略调整后的 Clay-B 分支 · 2026-09-06 · X/Y 合并", "Clay-B branch after the strategy change · 2026-09-06 · combined X/Y"],
  ["窗口局部化 W → H 平台终点 / Q-R 全时间量词区分 X → 跨平台阈值窗与等号 Y.1–Y.2 → total dissipation + 负工作历史 Y.3–Y.8 → 条件耗散 Y.9 → doubled-radius 绝对账本 Y.10–Y.12 → A+P 非 A+Z → 首次奇点文献适用性核查", "Window localization W → distinction between H plateau endpoints and Q-R all-time quantifiers X → cross-ramp threshold windows and equality Y.1–Y.2 → total dissipation plus negative-work history Y.3–Y.8 → conditional dissipation Y.9 → doubled-radius absolute ledger Y.10–Y.12 → A+P, not A+Z → first-singularity literature applicability audit"],
  ["从平台终点归约到 A+P 历史成本", "From plateau-endpoint reduction to the A+P history cost"],
  ["对真正位于平台内的窗口，扩大 cutoff 的反向历史由终点能量、total dissipation、二次变差、完整空间积分后的负工作与弱端点 BV 迹共同支付。全壳绝对账本只得到 C(A+P)，扩大时钟不等于原时钟，Y.9 负修正仍可能使右端非正，完整 I_2R 上未加权 W.14 未获支付。", "For a window truly inside the plateau, backward history for the enlarged cutoff is paid jointly by terminal energy, total dissipation, quadratic variation, negative work after the full spatial integral, and the weak-endpoint BV trace. The all-shell absolute ledger yields only C(A+P); the enlarged clock is not the original clock, the negative correction in Y.9 may still make the right-hand side nonpositive, and unweighted W.14 on the full I_2R remains unpaid."],
  ["平台时间内能量历史的准确代价", "The exact cost of energy history inside the plateau"],
  ["平台终点归约：已证", "Plateau-endpoint reduction: proved"],
  ["平台终点量词与反向能量历史已进入下一节点", "Plateau-endpoint quantifiers and backward energy history now form the next node"],
  ["前一节：短窗口局部耗散", "Previous note: local dissipation on short windows"],
  ["区分固定球/抛物缩球、指定中心/事后中心、全空间/周期，并逐项登记 Type-I、临界范数、无穷远衰减和压力假设；必要条件不直接当作矛盾。", "Distinguish fixed balls from parabolic shrinking balls, prescribed from post-selected centres, and the whole space from the torus; record every Type-I, critical-norm, far-field-decay, and pressure assumption. A necessary condition is not itself a contradiction."],
  ["下一研发问题：核验首次奇点必要条件的适用范围", "Next research question: audit the scope of first-singularity necessary conditions"],
  ["原 H 的目标可先限制到末端平台，但原阈值窗口可能跨过平台起点，等号情形也必须保留。对平台内窗口，扩大 cutoff 的历史成本包括 total dissipation、负工作和弱端点 BV 迹；全壳绝对账本只给 A+P，没有改进为 A+Z，完整 W.14 仍未支付。OPEN / NOT CLAY.", "The original H target may first be restricted to the terminal plateau, but the original threshold window may cross the plateau start and the equality case must also be retained. For windows inside the plateau, the enlarged-cutoff history cost includes total dissipation, negative work, and the weak-endpoint BV trace. The all-shell absolute ledger gives only A+P, not A+Z, and full W.14 remains unpaid. OPEN / NOT CLAY."],
  ["阅读平台历史笔记 →", "Read the plateau-history note →"],
  ["综述 v2.48 · 2026-09-06", "Review v2.48 · 2026-09-06"],
  ["总耗散/负工作历史：已证", "Total-dissipation/negative-work history: proved"],
  ["A+Z、R 输入与合同 G：OPEN · NOT CLAY", "A+Z, R input, and Contract G: OPEN · NOT CLAY"],
  ["Clay-B 的辅助通量目标可先限制到 H 的末端平台，但平台终点的原阈值窗口仍可能跨入早期 cutoff 段。扩大 cutoff 的反向历史必须保留终点能量、total dissipation、二次变差、负工作及弱端点 BV 迹；全壳目前只得到 A+P，不是目标 A+Z。", "The auxiliary Clay-B flux target may first be restricted to H's terminal plateau, but the original threshold window at a plateau endpoint may still enter the early cutoff ramp. Backward history for the enlarged cutoff must retain terminal energy, total dissipation, quadratic variation, negative work, and the weak-endpoint BV trace. The all-shell result is currently only A+P, not the target A+Z."],
  ["Clay-B 平台历史笔记快捷入口", "Clay-B plateau-history note shortcuts"],
  ["Clay-B 平台历史结论边界", "Clay-B plateau-history result boundary"],
  ["H 的平台通量、Q/R 的全时间增强目标、跨平台阈值窗及扩大 cutoff 的历史成本已经逐项区分；结果见下一个正式路线节点。", "H's plateau flux, the strengthened all-time Q/R target, cross-ramp threshold windows, and the enlarged-cutoff history cost have now been distinguished item by item. The result appears in the next formal route node."],
  ["X 证明原 H 只需先处理末端平台好终点，不必先覆盖 Q/R 的全部早期终点；Y 随即保留原阈值窗口跨出平台的支路及等号情形，改选更短平台窗时不继承原逆宽度预算。", "X proves that the original H target needs only good endpoints on the terminal plateau first, rather than every early endpoint in Q/R. Y then retains the branch where the original threshold window crosses the plateau, including equality, and shows that a shorter selected plateau window does not inherit the original inverse-width budget."],
  ["文献综述 v2.48 · 2026-09-06", "Literature review v2.48 · 2026-09-06"],
  ["只承担 suitable 局部能量输入及压力局部/尾项/gauge 区分的经典背景。其全空间解类别不直接套用到周期提升，X/Y 公式均由本地推导支持。", "supplies only the classical background for suitable local energy and the local/tail/gauge pressure distinction. Its whole-space solution class is not directly imposed on the periodic lift, and every X/Y formula is supported by the local derivation."],
  ["只用于保持一般无外力三维周期初值、正黏性和问题 B 的最终范围；", "is used only to preserve the final scope of general unforced three-dimensional periodic initial data, positive viscosity, and Problem B;"],
  ["Clay-B 平台时间能量历史的文献与主张边界", "Literature and claim boundary for Clay-B plateau-time energy history"],
  ["ClayB-PlateauHistory-20260906 公开边界", "Public boundary for ClayB-PlateauHistory-20260906"],
  ["Fefferman 的 Clay 官方问题说明", "Fefferman's official Clay problem description"],
  ["PROVED LOCALLY：X.1–X.4 将原 H 的平台终点通量与 Q/R 的全时间增强目标分开，并给平台好终点的尾和归约；Y.1–Y.2 保留阈值窗口跨平台及等号情形；Y.3–Y.8 以扩大 cutoff、total dissipation、二次变差、完整空间积分后的负工作和弱端点 BV 迹控制历史质量；Y.10–Y.12 在正确 doubled-radius 权重下重做绝对账本，只得到 C(A+P)。CONDITIONAL：Y.9 的局部黏性耗散下界保留负 cutoff 修正，右端可能非正。LITERATURE：上述 Clay 问题范围、suitable 局部能量及压力结构。FINITE COMPUTATION：无。OPEN：跨平台支路、逆宽度与 R.216–R.217 动力学输入、A+Z 级负工作、耗散主导支、完整 I_2R 上未加权 W.14 支付及合同 G。扩大时钟不是原时钟；没有真实 NS 反例、图件、仿真、数值证书、新颖性或优先权声明。NOT CLAY。", "PROVED LOCALLY: X.1–X.4 separates the original H plateau-endpoint flux from the strengthened all-time Q/R target and gives the tail reduction at good plateau endpoints; Y.1–Y.2 retains threshold windows crossing the plateau and the equality case; Y.3–Y.8 controls historical mass using the enlarged cutoff, total dissipation, quadratic variation, negative work after the full spatial integral, and the weak-endpoint BV trace; Y.10–Y.12 rebuilds the absolute ledger with the correct doubled-radius weights and obtains only C(A+P). CONDITIONAL: the Y.9 local viscous-dissipation lower bound retains a negative cutoff correction and may have a nonpositive right-hand side. LITERATURE: the Clay problem scope, suitable local energy, and pressure structure above. FINITE COMPUTATION: none. OPEN: the cross-ramp branch, inverse width and R.216–R.217 dynamics, A+Z-level negative work, the dissipation-dominant branch, payment of unweighted W.14 over the full I_2R, and Contract G. The enlarged clock is not the original clock. There is no true NS counterexample, figure, simulation, numerical certificate, novelty claim, or priority claim. NOT CLAY."],
  ["研究笔记总索引 · v2.48 · 2026-09-06", "Research-note master index · v2.48 · 2026-09-06"],
]);

function validateTranslation(source, en) {
  assert.ok(!containsChinese(en), `Chinese remains in translation: ${source}`);
  assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(source), `protected token drift: ${source}`);
}

process.chdir(root);
const [source, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);

if (checkOnly) {
  const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
  assert.deepEqual(source.filter((entry) => !currentByZh.has(entry.zh)), [], "site still has untranslated Chinese strings");
  const rows = current.filter((entry) => rowPattern.test(entry.id));
  assert.equal(rows.length, translations.size, "PlateauHistory translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), `translation drift: ${row.zh}`);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The exact cost of energy history inside the plateau"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "PlateauHistory source-string count drift");
  const additions = missing.map((entry, index) => {
    const en = translations.get(entry.zh);
    assert.equal(typeof en, "string", `missing local translation: ${entry.zh}`);
    validateTranslation(entry.zh, en);
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...base, ...additions], null, 2)}\n`);
  const built = spawnSync(process.execPath, ["scripts/build-i18n.mjs", "translations/en.json"], { cwd: root, encoding: "utf8" });
  assert.equal(built.status, 0, `${built.stdout}\n${built.stderr}`);
}

process.stdout.write(`${JSON.stringify({ release: "ClayB-PlateauHistory-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2)}\n`);
