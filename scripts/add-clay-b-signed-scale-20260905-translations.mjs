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
const publicRoot = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const checkOnly = process.argv.includes("--check-only");
const prefix = "claybsignedscale20260905";

const translations = new Map([
  ["文献综述 v2.44 · 2026-09-05", "Literature review v2.44 · 2026-09-05"],
  ["只承担复合滤波、嵌套带能量和粗粒化 SGS 预算的经典背景；本节不把经典框架声明为新发现，也不从它们导入指定中心好尺度定理。", "supply only the classical background for composite filtering, nested band energy, and coarse-grained SGS budgets. This note does not claim the classical framework as new or import a prescribed-centre good-scale theorem from it."],
  ["Clay-B 有符号尺度预算的 filtering 文献与主张边界", "Filtering literature and claim boundary for the Clay-B signed-scale budget"],
  ["ClayB-SignedScale-20260905 公开边界", "Public boundary for ClayB-SignedScale-20260905"],
  ["PROVED LOCALLY：F.1–F.4 固定核预检；S.1–S.15 完整有符号局部预算和全部尺度失配；T.1–T.6 指定非负热对偶零失配设计与收缩定位不相容；T.7–T.12 的全时光滑真实 NS 族排除从重标热观测到原同尺度移动能量的普适转移。LITERATURE：经典 filtered stress、嵌套带能量与 SGS 预算。FINITE COMPUTATION：无。OPEN：合同 G、允许失配的临界可求和性、首次奇点附加条件与真实物理时间对偶候选。初始 L² 统一但 H¹ 不统一；T_R=128R² 随 R 变化且终点不是首次奇点。不反驳正则性准则，不声称新颖性。NOT CLAY。", "PROVED LOCALLY: the fixed-kernel preflight F.1-F.4; the complete signed local budget and every scale mismatch in S.1-S.15; the incompatibility of the specified nonnegative heat-dual zero-mismatch design with shrinking localization in T.1-T.6; and the globally smooth true NS family in T.7-T.12 that rules out universal transfer from the rescaled heat observable to the original same-scale moving energy. LITERATURE: classical filtered stress, nested band energy, and SGS budgets. FINITE COMPUTATION: none. OPEN: contract G, critical summability with admissible mismatch, first-singular-time hypotheses, and the physical-time dual candidate. The initial L2 bound is uniform but the H1 bound is not; T_R=128R² varies with R and the endpoint is not a first singular time. No regularity criterion is refuted and no novelty is claimed. NOT CLAY."],
  ["按政策不生成 PDF", "No PDF under the current policy"],
  ["独立 Clay-B 笔记不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "Independent Clay-B notes do not occupy an R0-series identifier or change the current R0.76L endpoint. Beginning with ClayB-SignedScale-20260905, new releases publish HTML only; existing PDFs remain unchanged."],
  ["研究笔记总索引 · v2.44 · 2026-09-05", "Research-note master index · v2.44 · 2026-09-05"],
  ["本节：有符号尺度相消", "This note: signed-scale cancellation"],
  ["并入当前路线", "Integrated into the current route"],
  ["策略调整后的 Clay-B 分支 · 2026-09-05", "Clay-B branch after the strategy change · 2026-09-05"],
  ["初始 H¹ 不统一，T_R=128R² 随 R 变化，终点不是首次奇点。下一候选尚未证明；允许失配的临界求和与合同 G 仍 OPEN。该分支不占用下一主序列编号。", "The initial H1 bound is not uniform, T_R=128R² varies with R, and the endpoint is not a first singular time. The next candidate is unproved; critical summation with admissible mismatch and contract G remain OPEN. This branch does not occupy the next canonical-series identifier."],
  ["从两尺度完整支付到有符号尺度相消", "From the fully paid two-scale estimate to signed-scale cancellation"],
  ["固定尺度完整有符号预算和逐层失配台账已经闭合；指定的非负热对偶若强制零失配，就不能同时保持真实收缩定位。一个初始 L² 统一、H¹ 不统一的全时光滑真实 NS 族进一步排除自动退化热观测到原同尺度移动能量的普适转移。普通终点 T_R=128R² 随尺度变化，不是首次奇点；合同 G 仍 OPEN。NOT CLAY.", "The complete fixed-scale signed budget and layer-by-layer mismatch ledger are closed. If the specified nonnegative heat-dual test is forced to have zero mismatch, it cannot also preserve genuine shrinking localization. A globally smooth true NS family with a uniform initial L2 bound but a nonuniform H1 bound further rules out universal transfer from an automatically degenerating heat observable to the original same-scale moving energy. The ordinary endpoint T_R=128R² varies with scale and is not a first singular time; contract G remains OPEN. NOT CLAY."],
  ["精确尺度相消与收缩定位的冲突", "Exact scale cancellation conflicts with shrinking localization"],
  ["零失配定位障碍：已证", "Zero-mismatch localization obstruction: proved"],
  ["前一节：两尺度完整支付", "Previous note: the fully paid two-scale estimate"],
  ["完整有符号预算：已证", "Complete signed budget: proved"],
  ["物理时间对偶与合同 G：OPEN · NOT CLAY", "Physical-time dual test and contract G: OPEN · NOT CLAY"],
  ["下一候选：真实物理时间对偶测试", "Next candidate: a true physical-time dual test"],
  ["阅读有符号尺度笔记 →", "Read the signed-scale note →"],
  ["综述 v2.44 · 2026-09-05", "Review v2.44 · 2026-09-05"],
  ["Clay-B 已写清完整有符号尺度预算、逐层失配和热对偶零失配的收缩定位障碍；一个初始 L² 统一、H¹ 不统一的真实光滑 NS 族排除了从自动退化热观测到原同尺度移动能量的普适转移。首次奇点附加条件、真实物理时间对偶候选与合同 G 仍开放。", "The Clay-B route now has a complete signed-scale budget, a layer-by-layer mismatch ledger, and a shrinking-localization obstruction for zero-mismatch heat-dual tests. A true smooth NS family with a uniform initial L2 bound but a nonuniform H1 bound rules out universal transfer from an automatically degenerating heat observable to the original same-scale moving energy. First-singular-time hypotheses, the physical-time dual candidate, and contract G remain open."],
  ["Clay-B 有符号尺度笔记快捷入口", "Clay-B signed-scale note shortcuts"],
  ["Clay-B 有符号尺度结论边界", "Clay-B signed-scale result boundary"],
  ["R0.76L 边界 → Clay-B 两尺度完整支付 → 嵌套热滤波带能量 → 完整时空失配 → 零失配定位障碍 → 统一 L² 真 NS 光滑族排除普适转移", "R0.76L boundary → fully paid Clay-B two-scale estimate → nested heat-filter band energy → complete spacetime mismatch → zero-mismatch localization obstruction → uniform-L2 true smooth NS family rules out universal transfer"],
  ["R0.76L 之后，研发策略转向 Clay-B 的移动尺度预算。前一节保留固定尺度完整支付；本节进一步闭合有符号时空预算和 S.8–S.15 失配台账，并证明指定非负热对偶若强制零失配，就不能同时保持真实收缩定位。", "After R0.76L, I redirected the research strategy toward the moving-scale Clay-B budget. The previous note retained the fully paid fixed-scale estimate; this note closes the signed spacetime budget and the S.8-S.15 mismatch ledger, and proves that forcing zero mismatch in the specified nonnegative heat-dual test is incompatible with genuine shrinking localization."],
]);

function validateTranslation(source, en) {
  assert.ok(!containsChinese(en), `Chinese remains in translation: ${source}`);
  assert.deepEqual(
    extractProtectedTokens(en),
    extractProtectedTokens(source),
    `protected token drift: ${source}`,
  );
}

process.chdir(root);
const [source, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);

if (checkOnly) {
  const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.deepEqual(missing, [], "site still has untranslated Chinese strings");
  const rows = current.filter((entry) => rowPattern.test(entry.id));
  assert.equal(rows.length, translations.size, "signed-scale translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), `translation drift: ${row.zh}`);
    validateTranslation(row.zh, row.en);
  }
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "signed-scale source-string count drift");
  const additions = missing.map((entry, index) => {
    const en = translations.get(entry.zh);
    assert.equal(typeof en, "string", `missing local translation: ${entry.zh}`);
    validateTranslation(entry.zh, en);
    return {
      id: `${prefix}${String(index + 1).padStart(3, "0")}`,
      ...entry,
      en,
    };
  });
  await writeFile(translationPath, `${JSON.stringify([...base, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({
  release: "ClayB-SignedScale-20260905",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: translations.size,
  applied: !checkOnly,
}, null, 2)}\n`);
