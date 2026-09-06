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
const prefix = "claybancientconstantscreen20260906";

const translations = new Map([
  ["本轮读取", "This round reads"],
  ["的引言与第 3–6 节（PDF 页 6–24），并视觉检查 PDF 页 18–20，用于区分 mild 解、古老解、峰值提取及 Proposition 6.1 后的常向量障碍；另核对", "the introduction and §§3–6 (PDF pages 6–24), and visually checks PDF pages 18–20 to distinguish mild solutions, ancient solutions, peak extraction, and the constant-vector obstacle following Proposition 6.1; it also checks"],
  ["的指定页段与第 5 节证明，用于识别中间应变特征值的条件正则性目标。2025/2026 出版方材料只作有限时效核验。未读部分、外引局部存在与正则性理论、一般三维古老解分类均未扩写为已审计结论；没有穷尽文献、Deep Research、新颖性或外部同行评审声明。", "in the specified passages and §5 proofs to identify the conditional middle-strain-eigenvalue regularity target. Publisher material from 2025/2026 supplies only a bounded freshness check. Unread sections, external local-existence and regularity theory, and the general three-dimensional ancient-solution classification are not rewritten as audited conclusions; no exhaustive literature review, Deep Research, novelty review, or external peer review is claimed."],
  ["文献综述 v2.59 · 2026-09-06", "Literature review v2.59 · 2026-09-06"],
  ["阅读完整 CB.15 笔记", "Read the complete CB.15 note"],
  ["CB.15 · Clay-B 常向量古老极限的文献和主张边界", "CB.15 · Literature and claim boundary for Clay-B constant ancient limits"],
  ["CB.15 · ClayB-AncientConstantScreen-20260906 公开边界", "CB.15 · Public boundary for ClayB-AncientConstantScreen-20260906"],
  ["Koch–Nadirashvili–Seregin–Šverák 作者预印本", "Koch–Nadirashvili–Seregin–Šverák author preprint"],
  ["PROVED METHOD OBSTRUCTION：BH 构造的每一项都是真实、无外力、单位黏性光滑周期 NS 有限段；在零均值、过去速度 1+o(1)、终点单位峰值、整胞能量 O(周期尺度) 与归一化耗散趋零下，局部极限仍可为非零常向量。FIXED-HISTORY NOT REPRODUCED：它不是同一固定初值的首次爆破序列，不是每项精确 running record；真正固定初值历史保留 b/ℓ²→T_*>0 与遥远左端速度趋零，本构造对应极限分别为 0 与 1。常向量是合法古老 mild 解，不是一般常量分类的反例。FINITE CHECKS ONLY：三份文本源、18 个 BH 标签、81/81 文件绑定与 22 项缩放复算不替代 PDE 证明。OPEN：固定初值完整历史、mild 时间排序、一般古老解刚性、G/Q、奇点排除与 Clay。无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "PROVED METHOD OBSTRUCTION: every member of the BH construction is a genuine smooth, periodic, unforced, unit-viscosity NS finite segment. With zero mean, past velocity 1+o(1), a terminal unit peak, cell energy O(period scale), and normalized dissipation tending to zero, the local limit may still be a nonzero constant vector. FIXED-HISTORY NOT REPRODUCED: this is not a first-blow-up sequence from one fixed initial datum, and its members are not exact running records. A genuine fixed-data history retains b/ℓ²→T_*>0 and vanishing velocity at the remote left endpoint; the corresponding limits here are 0 and 1. Constant vectors are legitimate ancient mild solutions, not counterexamples to a general classification by constants. FINITE CHECKS ONLY: three text sources, 18 BH labels, 81/81 file bindings, and 22 scaling recomputations do not replace PDE proof. OPEN: the complete fixed-data history, mild temporal ordering, general ancient rigidity, G/Q, singularity exclusion, and Clay. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["常向量古老极限：真实 NS 有限段的粗预算反检查", "Constant ancient limits: a coarse-budget countercheck with genuine NS segments"],
  ["研究笔记总索引 · v2.59 · 2026-09-06", "Research-note master index · v2.59 · 2026-09-06"],
  ["CB.1–CB.15 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.15 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["查看原始来源与主张边界", "Review the primary sources and claim boundary"],
  ["粗预算自动排常量停止", "automatic constant exclusion from coarse budgets stops"],
  ["固定初值完整历史、G/Q 与正则性 OPEN · NOT CLAY", "Complete fixed-data history, G/Q, and regularity OPEN · NOT CLAY"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.15 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.15 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：固定初值完整历史", "Next research question: the complete fixed-data history"],
  ["阅读最新 CB.15 常向量反检查笔记 →", "Read the latest CB.15 constant-limit countercheck →"],
  ["这只排除用 BH.1 粗预算自动排常量的方法。序列没有复制同一固定初值、首次候选奇点、精确 running record、b/ℓ²→T_*>0 或遥远初值速度趋零；常向量也不是一般分类命题的反例。", "This blocks only automatic constant exclusion from the BH.1 coarse budgets. The sequence does not reproduce one fixed initial datum, a first candidate singularity, an exact running record, b/ℓ²→T_*>0, or vanishing remote initial velocity; nor is the constant vector a counterexample to a general classification theorem."],
  ["真实 NS 常向量反检查已进入 CB.15", "The genuine-NS constant-limit countercheck now forms CB.15"],
  ["真实 NS 有限段构造成立", "Genuine NS finite-segment construction established"],
  ["真实、无外力、单位黏性光滑 NS 有限段，在零均值、过去速度 1+o(1)、终点单位峰值、整胞能量 O(周期尺度) 和归一化耗散趋零的粗预算下，仍可局部趋于非零常向量。这只阻断粗预算自动排常量，不复制同一固定初值、首次爆破或精确 record。G OPEN。NOT CLAY.", "Genuine smooth, unforced, unit-viscosity NS finite segments can converge locally to a nonzero constant vector while retaining zero mean, past velocity 1+o(1), a terminal unit peak, cell energy O(period scale), and normalized dissipation tending to zero. This blocks only automatic constant exclusion from coarse budgets; it does not reproduce one fixed initial datum, a first blow-up, or an exact record. G OPEN. NOT CLAY."],
  ["只检查峰值归一化后的时间排序与 mild 表达式：线性项虽趋零，遥远过去的非线性尾是否仍能留下常向量尚未支付。若只能重写未知正则性条件，就停止该尝试。", "Check only temporal ordering and the mild formula after peak normalization. Although the linear term tends to zero, it remains unpaid whether the nonlinear tail from the remote past can leave a constant vector. If the attempt only restates an unknown regularity condition, stop it."],
  ["综述 v2.59 · 2026-09-06", "Review v2.59 · 2026-09-06"],
  ["BH 构造扩张周期域上的真实、无外力、单位黏性光滑 NS 有限段：零均值、终点单位峰值、过去速度 1+o(1)、整胞能量 O(周期尺度)、归一化耗散趋零，并局部收敛到单位常向量。", "BH constructs genuine smooth, unforced, unit-viscosity NS finite segments on expanding periodic domains: zero mean, a terminal unit peak, past velocity 1+o(1), cell energy O(period scale), normalized dissipation tending to zero, and local convergence to a unit constant vector."],
  ["BH 已用真实光滑 NS 有限段检验粗预算排常量机制，同时保留固定初值完整历史、精确 record 与一般古老解刚性的边界；结果见下一个正式路线节点。", "BH has tested coarse-budget constant exclusion with genuine smooth NS finite segments while preserving the boundary around complete fixed-data history, exact records, and general ancient-solution rigidity; the result appears in the next formal route node."],
  ["CB.1–CB.15 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.15 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.14 energy-only 候选停止 → BH 真实 NS 有限段 → 两次精确缩放 → 非零常向量局部极限 → 粗预算排常量受阻 → 固定初值完整历史仍 OPEN", "CB.14 energy-only candidate stops → BH genuine NS finite segments → two exact scalings → nonzero constant-vector local limit → coarse-budget constant exclusion blocked → complete fixed-data history remains OPEN"],
  ["CB.15：常向量极限反检查", "CB.15: constant-limit countercheck"],
  ["CB.15｜常向量古老极限：真实 NS 有限段的粗预算反检查", "CB.15 | Constant ancient limits: a coarse-budget countercheck with genuine NS segments"],
  ["CB.16 只是下一章占位，不是已完成研究。同一固定初值完整历史的定量非恒定性、mild 时间排序、一般古老解刚性、G/Q、带符号压力功上界、首次奇点排除与 Clay 均未冻结。", "CB.16 is only a placeholder for the next chapter, not completed research. Quantitative nonconstancy in one complete fixed-data history, mild temporal ordering, general ancient-solution rigidity, G/Q, the signed pressure-work upper bound, first-singularity exclusion, and Clay are not frozen."],
  ["Clay-B 常向量反检查结论", "Clay-B constant-limit countercheck boundary"],
  ["Clay-B 常向量极限反检查笔记快捷入口", "Clay-B constant-limit countercheck shortcuts"],
  ["Clay-B 独立路线停在 CB.15", "The independent Clay-B route stops at CB.15"],
  ["Clay-B 已完成常向量古老极限的一轮真实 NS 反检查：光滑有限段在粗能量预算下仍可趋于非零常向量，因此自动排常量的方法停止；同一固定初值、完整历史比例、精确 record、mild 时间排序与合同 G 继续开放。", "Clay-B has completed a genuine-NS countercheck of constant ancient limits. Smooth finite segments can still approach a nonzero constant vector under the coarse energy budgets, so automatic constant exclusion stops. One fixed initial datum, the complete-history ratio, exact records, mild temporal ordering, and contract G remain open."],
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
  assert.equal(rows.length, translations.size, "AncientConstantScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.15"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "AncientConstantScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-AncientConstantScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
