#!/usr/bin/env node

import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const checkOnly = process.argv.includes("--check-only");
const prefix = "claybwindowlocalisation20260906";

const translations = new Map([
  ["本节：短窗口局部耗散", "This note: local dissipation on short windows"],
  ["策略调整后的 Clay-B 分支 · 2026-09-06 · U/V/W 合并", "Clay-B branch after the strategy change · 2026-09-06 · combined U/V/W"],
  ["持留窗口、时间可积性与压力局部化已进入下一节点", "Persistence windows, time integrability, and pressure localization now form the next node"],
  ["从正变差窗口到扩大域耗散债务", "From positive-variation windows to enlarged-domain dissipation debt"],
  ["当前路线边界", "Current route boundary"],
  ["短窗口的局部耗散与压力余项", "Local dissipation and pressure remainders on short windows"],
  ["过窄窗口产生“联合余项工作较大”或“局部耗散满足带负 cutoff 修正的下界”二分支；后者右端可能非正。跨壳有限重叠只在半径 2R 权重下成立，因此新增扩大外壳耗散账本，不能写成原半径 R 的 P_R 已支付。", "A window below threshold yields either large joint remainder work or a local-dissipation lower bound with a negative cutoff correction; the latter may have a nonpositive right-hand side. Finite overlap across shells holds only with radius-2R weights, so it creates an enlarged-exterior dissipation ledger that cannot be recorded as already paid by the radius-R P_R."],
  ["扩大耗散支付与合同 G：OPEN · NOT CLAY", "Enlarged dissipation payment and Contract G: OPEN · NOT CLAY"],
  ["前一节：伴随测试定位代价", "Previous note: localization cost of the adjoint test"],
  ["区分 H/I 的平台时间通量、Q 的更强全时间目标与合同 G 在指定可能首次奇点只要求存在一个好尺度的原量词。不得偷带 Type-I 或临界范数假设；不继续只调整 V/W 常数。", "Distinguish the plateau-time flux in H/I, the stronger all-time target in Q, and Contract G's original quantifier requiring only one good scale at a prescribed possible first singularity. No Type-I or critical-norm assumption may be smuggled in, and the route will not continue by merely adjusting V/W constants."],
  ["物理时间伴随 → 正变差持留窗口 U → 固定尺度 L_t^(4/3) 与四次宽度 V → 局部/调和压力分解 W → 联合余项工作或带 cutoff 扣除的耗散分支 → doubled-radius 耗散债务 → 首次奇点量词复评", "Physical-time adjoint → positive-variation persistence window U → fixed-scale L_t^(4/3) and fourth-power width V → local/harmonic pressure split W → joint remainder work or dissipation with cutoff subtraction → doubled-radius dissipation debt → first-singularity quantifier audit"],
  ["下一研发问题：复评辅助条件的量词强度", "Next research question: audit the strength of auxiliary quantifiers"],
  ["原计时合同的正变差分支已经展开为 U/V/W：先量化固定尺度窗口宽度，再保留调和压力与中心漂移的联合有符号余项，最后核对扩大域耗散账本。结果见下一个正式路线节点。", "The positive-variation branch of the original clock contract has now been developed as U/V/W: first quantify the fixed-scale window width, then retain the joint signed remainder from harmonic pressure and centre drift, and finally audit the enlarged-domain dissipation ledger. The result appears in the next formal route node."],
  ["阅读窗口局部化笔记 →", "Read the window-localization note →"],
  ["正变差窗口、固定尺度 L_t^(4/3) 通量控制与环壳压力分解已经合并为一个连续节点。过窄窗口只导向联合有符号余项工作或带负 cutoff 修正的局部耗散分支；有限重叠需要半径 2R 的扩大域账本，原半径 R 的 P_R 不自动支付。OPEN / NOT CLAY.", "Positive-variation windows, fixed-scale L_t^(4/3) flux control, and the annular pressure split are combined into one continuous node. A window below threshold leads only to joint signed remainder work or a local-dissipation branch with a negative cutoff correction. Finite overlap requires an enlarged radius-2R ledger, which the original radius-R P_R does not automatically pay. OPEN / NOT CLAY."],
  ["综述 v2.46 · 2026-09-06", "Review v2.46 · 2026-09-06"],
  ["Clay-B 窗口局部化笔记快捷入口", "Clay-B window-localization note shortcuts"],
  ["Clay-B 窗口局部化结论边界", "Clay-B window-localization result boundary"],
  ["Clay-B 的正变差窗口与固定尺度时间 L^(4/3) 通量控制已给出定量持留宽度；环壳压力局部化把短窗口导向联合有符号余项工作或带 cutoff 扣除的局部耗散分支。有限重叠只由半径 2R 权重支付，扩大外壳耗散与合同 G 仍开放。", "Clay-B positive-variation windows and fixed-scale time L^(4/3) flux control give a quantitative persistence width. Annular pressure localization sends a short window to either joint signed remainder work or a local-dissipation branch with a cutoff subtraction. Finite overlap is paid only by radius-2R weights; enlarged-exterior dissipation and Contract G remain open."],
  ["U 从完整时钟的正变差抽出壳层持留窗口并支付二次 Q 分支；V 在固定尺度给出通量速率的时间 L^(4/3) 控制和四次窗口宽度；W 将压力拆成可支付的局部项与调和余项，并把中心漂移保留在同一个联合有符号工作中。", "U extracts a shellwise persistence window from positive variation of the complete clock and pays the quadratic Q branch. At fixed scale, V gives time L^(4/3) control of the flux rate and a fourth-power window width. W splits pressure into a payable local term and a harmonic remainder, retaining centre drift in the same joint signed work."],
  ["U/V 固定尺度窗口：已证", "U/V fixed-scale windows: proved"],
  ["W 压力分解与重叠账本：已证", "W pressure split and overlap ledger: proved"],
  ["文献综述 v2.46 · 2026-09-06", "Literature review v2.46 · 2026-09-06"],
  ["只承担局部奇异积分、尾项和时间 gauge 必须区分的压力展开背景。本节只对紧支撑源使用 Riesz 变换，并由周期 Navier--Stokes 压力方程直接得到内加厚域上的调和余项；不把该文的全空间 mildness 等价定理移植到周期提升。Sobolev、Calderón--Zygmund 与 Gagliardo--Nirenberg 只按经典工具使用。", "supplies only the pressure-expansion background distinguishing the local singular integral, tail, and time gauge. This note applies the Riesz transform only to a compactly supported source and obtains the harmonic remainder on the inner padded domain directly from the periodic Navier--Stokes pressure equation. It does not transplant the paper's whole-space mildness equivalence to the periodic lift. Sobolev, Calderón--Zygmund, and Gagliardo--Nirenberg are used only as classical tools."],
  ["Clay-B 短窗口局部耗散的文献与主张边界", "Literature and claim boundary for Clay-B local dissipation on short windows"],
  ["ClayB-WindowLocalisation-20260906 公开边界", "Public boundary for ClayB-WindowLocalisation-20260906"],
  ["PROVED LOCALLY：U.1–U.9 的正变差窗口和二次 Q 分支支付；V.1–V.12 的固定尺度时间 L^(4/3) 通量控制、四次窗口宽度及条件性 β 八次比值；W.1–W.6 的紧支撑局部压力/调和余项分解与调和压力加中心漂移的联合有符号工作；W.11–W.14 在正确 doubled-radius 权重下的有限重叠。CONDITIONAL：W.9–W.10 的联合余项工作/局部耗散二分支，耗散下界保留负的 cutoff 修正，右端可能非正。LITERATURE：上述局部压力结构及经典函数空间工具。FINITE COMPUTATION：无。OPEN：统一全壳宽度和 β 八次预算、有符号余项工作、扩大外壳耗散、真实 NS 对 R.216–R.217 的输入及指定首次奇点合同 G。没有真实 NS 反例、图件、仿真、数值证书、新颖性或优先权声明。NOT CLAY。", "PROVED LOCALLY: the U.1-U.9 positive-variation windows and quadratic Q-branch payment; the V.1-V.12 fixed-scale time L^(4/3) flux control, fourth-power window width, and conditional eighth-power β ratio; the W.1-W.6 compactly supported local-pressure/harmonic-remainder split and joint signed work from harmonic pressure plus centre drift; and finite overlap under the correct doubled-radius weights in W.11-W.14. CONDITIONAL: the W.9-W.10 joint-remainder-work/local-dissipation alternative; the dissipation lower bound retains a negative cutoff correction and may have a nonpositive right-hand side. LITERATURE: the local-pressure structure above and classical function-space tools. FINITE COMPUTATION: none. OPEN: uniform all-shell width and eighth-power β budgets, signed remainder work, enlarged-exterior dissipation, true-NS input for R.216-R.217, and prescribed-first-singularity Contract G. No true NS counterexample, figure, simulation, numerical certificate, novelty claim, or priority claim. NOT CLAY."],
  ["研究笔记总索引 · v2.46 · 2026-09-06", "Research-note master index · v2.46 · 2026-09-06"],
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
  assert.equal(rows.length, translations.size, "WindowLocalisation translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), `translation drift: ${row.zh}`);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("Local dissipation and pressure remainders on short windows"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "WindowLocalisation source-string count drift");
  const additions = missing.map((entry, index) => {
    const en = translations.get(entry.zh);
    assert.equal(typeof en, "string", `missing local translation: ${entry.zh}`);
    validateTranslation(entry.zh, en);
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...base, ...additions], null, 2)}\n`);
  const built = spawnSync(process.execPath, ["scripts/build-i18n.mjs", "translations/en.json"], {
    cwd: root,
    encoding: "utf8",
  });
  assert.equal(built.status, 0, `${built.stdout}\n${built.stderr}`);
}

process.stdout.write(`${JSON.stringify({
  release: "ClayB-WindowLocalisation-20260906",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: translations.size,
  applied: !checkOnly,
}, null, 2)}\n`);
