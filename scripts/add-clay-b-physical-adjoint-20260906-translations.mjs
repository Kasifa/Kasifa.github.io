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
const prefix = "claybphysicaladjoint20260906";

const translations = new Map([
  ["伴随测试的定位代价", "The localization cost of an adjoint test"],
  ["本节：伴随测试定位代价", "This note: the localization cost of an adjoint test"],
  ["策略调整后的 Clay-B 分支 · 2026-09-06", "Clay-B branch after the strategy change · 2026-09-06"],
  ["从零失配定位障碍到真实物理时间伴随预算", "From the zero-mismatch localization obstruction to a physical-time adjoint budget"],
  ["固定正尺度的真实时间伴随测试保留 suitable 弱端点、早期能量、残余输运和压力，并把提升二阶矩控制改进为 C(1+D_J/R)。真实光滑 NS 剪切族排除了不含幅值或漂移支付的免费矩定位；原移动管比较、临界有符号项与合同 G 仍 OPEN。NOT CLAY.", "At fixed positive scale, the physical-time adjoint test retains suitable weak endpoints, early energy, residual transport, and pressure, while improving the lifted second-moment bound to C(1+D_J/R). A true smooth NS shear family rules out free moment localization with no amplitude or drift payment. The original moving-tube comparison, critical signed terms, and Contract G remain OPEN. NOT CLAY."],
  ["零失配热对偶被排除后，改为真实物理时间反向推进，并显式保留弱端点、早期能量、残余输运与压力。结果见下一个正式路线节点。", "After the zero-mismatch heat dual is ruled out, the test is evolved backward in true physical time while explicitly retaining weak endpoints, early energy, residual transport, and pressure. The result is the next formal route node."],
  ["前一节：有符号尺度相消", "Previous note: signed-scale cancellation"],
  ["仍需把条件性的伴随抽取与真实 NS 预算接通，控制原移动管能量、临界压力和残余输运；不能把已证条件式误写成前提自动成立。该分支不占用 R0.76M。", "The conditional adjoint extraction must still be connected to the true NS budget, with control of the original moving-tube energy, critical pressure, and residual transport. A proved conditional statement must not be rewritten as an automatically satisfied premise. This branch does not occupy R0.76M."],
  ["弱端点预算：已证", "Weak-endpoint budget: proved"],
  ["下一候选：原计时合同的持留/上穿控制", "Next candidate: persistence/upcrossing control for the original clock contract"],
  ["线性矩代价：已证", "Linear moment cost: proved"],
  ["有符号尺度相消 → 放弃零失配热对偶 → 真实时间伴随弱端点 → 线性耗散矩界 → 质量尾界但非原移动管能量 → 原计时合同持留/上穿输入", "Signed-scale cancellation → abandon the zero-mismatch heat dual → physical-time adjoint weak endpoints → linear dissipation moment bound → mass-tail bound but not original moving-tube energy → persistence/upcrossing input for the original clock contract"],
  ["原计时合同持留/上穿：OPEN · NOT CLAY", "Original clock-contract persistence/upcrossing: OPEN · NOT CLAY"],
  ["阅读伴随测试笔记 →", "Read the adjoint-test note →"],
  ["真实时间反向伴随测试在固定正尺度上合法进入 suitable Leray–Hopf 局部能量不等式；起点须为强 L² 右 Lebesgue 时间，终点可取弱代表。提升二阶矩满足 C(1+D_J/R) 的线性代价，但该结论不使 D_J/R 自动有界或变小。", "At fixed positive scale, the backward physical-time adjoint is admissible in the suitable Leray-Hopf local-energy inequality. The start must be a strong right-Lebesgue time in L2, while the endpoint may be a weak representative. The lifted second moment pays the linear cost C(1+D_J/R), but this does not make D_J/R automatically bounded or small."],
  ["真实物理时间伴随测试已进入下一节点", "The physical-time adjoint test now forms the next node"],
  ["Clay-B 伴随测试结论边界", "Clay-B adjoint-test result boundary"],
  ["Clay-B 的真实物理时间伴随测试已给出 suitable 弱端点预算和线性定位代价 C(1+D_J/R)；真实光滑 NS 剪切族排除了不含初值幅值或漂移支付的免费矩定位。原移动管能量比较、临界压力/残余输运，以及原计时合同的持留/上穿输入仍开放。", "The Clay-B physical-time adjoint now provides a suitable weak-endpoint budget and the linear localization cost C(1+D_J/R). A true smooth NS shear family rules out free moment localization without an initial-amplitude or drift payment. The original moving-tube energy comparison, critical pressure and residual transport, and persistence/upcrossing input for the original clock contract remain open."],
  ["Clay-B 物理时间伴随笔记快捷入口", "Clay-B physical-time adjoint note shortcuts"],
  ["的 Gaussian 常数依赖临界漂移范数。三者都不提供免费的指定中心梯度或原移动球能量比较。", "has Gaussian constants that depend on the critical drift norm. None of the three sources supplies a free prescribed-centre gradient estimate or an original moving-ball energy comparison."],
  ["区分全空间集中度比较与周期限制；", "distinguish whole-space concentration comparison from periodic limitations;"],
  ["文献综述 v2.45 · 2026-09-06", "Literature review v2.45 · 2026-09-06"],
  ["综述 v2.45 · 2026-09-06", "Review v2.45 · 2026-09-06"],
  ["只承担全空间不可压缩漂移下 L¹→L∞ 衰减的背景；", "supplies only the whole-space L1-to-L-infinity decay background for incompressible drift;"],
  ["Clay-B 物理时间伴随测试的文献与主张边界", "Literature and claim boundary for the Clay-B physical-time adjoint test"],
  ["ClayB-PhysicalAdjoint-20260906 公开边界", "Public boundary for ClayB-PhysicalAdjoint-20260906"],
  ["PROVED LOCALLY：B.1–B.5 固定 R 的真实时间伴随弱端点预算；B.6–B.13 提升二阶矩的线性代价 C(1+D_J/R)；B.14–B.16 周期 Nash 高度界与直接 Hölder 缺口；C.1–C.6 的全时光滑真实 NS 剪切族排除不含初值幅值或漂移支付的统一欧氏提升矩界。LITERATURE：上述三个原始来源的限定范围。FINITE COMPUTATION：无。OPEN：原移动管比较、临界压力与残余输运、真实 NS 对 D_J/R 的控制、原计时合同的持留/上穿输入和合同 G。剪切族固定 R、T，初始 L²/H¹ 均不统一，终点不是首次奇点；不证明 B.8 最优，不声称新颖性。NOT CLAY。", "PROVED LOCALLY: the fixed-R physical-time adjoint weak-endpoint budget B.1-B.5; the linear lifted second-moment cost C(1+D_J/R) in B.6-B.13; the periodic Nash height estimate and direct Holder gap in B.14-B.16; and the globally smooth true NS shear family C.1-C.6 that rules out a uniform Euclidean lifted-moment bound with no initial-amplitude or drift payment. LITERATURE: the limited domains of the three primary sources above. FINITE COMPUTATION: none. OPEN: the original moving-tube comparison, critical pressure and residual transport, true-NS control of D_J/R, persistence/upcrossing input for the original clock contract, and Contract G. The shear family fixes R and T, has nonuniform initial L2 and H1, and does not use a first singular endpoint. It does not prove B.8 optimal and makes no novelty claim. NOT CLAY."],
  ["研究笔记总索引 · v2.45 · 2026-09-06", "Research-note master index · v2.45 · 2026-09-06"],
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
  assert.equal(rows.length, translations.size, "PhysicalAdjoint translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), `translation drift: ${row.zh}`);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The localization cost of an adjoint test"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "PhysicalAdjoint source-string count drift");
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
  release: "ClayB-PhysicalAdjoint-20260906",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: translations.size,
  applied: !checkOnly,
}, null, 2)}\n`);
