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
const prefix = "claybfrequencyactivation20260907";

const translations = new Map([
  ["本轮进行有界本地去重，并核对", "This round performed bounded local deduplication and checked"],
  ["的官方元数据和摘要。没有导入新的外部 PDE 定理，也没有完整论文证明审计、PDF 核验、Deep Research 或穷尽性新颖性搜索。AJ 已包含固定能量、扩大环面与 N⁻⁵ᐟ² 短时工具；本章增加严格空的原速度目标带、固定正能量首次激活及匹配普遍下界的组合，不主张缩放机制新颖性、优先权或外部同行评审结论。", "official metadata and abstracts. No new external PDE theorem, complete-paper proof audit, PDF review, Deep Research, or exhaustive novelty search was imported. AJ already contains the fixed-energy expanding-torus N⁻⁵ᐟ² short-time tools. This chapter adds the combination of a strictly empty velocity output band, fixed positive-energy first activation, and a matching universal lower bound; it claims no novelty of the scaling mechanism, priority, or external peer-review conclusion."],
  ["文献综述 v2.69 · 2026-09-06", "Literature review v2.69 · 2026-09-06"],
  ["阅读完整 CB.25 笔记", "Read the complete CB.25 note"],
  ["CB.25 · Clay-B 频带激活的来源和主张边界", "CB.25 · Sources and claim boundary for Clay-B frequency activation"],
  ["CB.25 · ClayB-FrequencyActivation-20260907 公开边界", "CB.25 · Public boundary for ClayB-FrequencyActivation-20260907"],
  ["PROVED：固定周期、ν>0、E₀>0 和固定光滑带乘子下，任意光滑完整无外力 NS 解的指定正振幅上升至少耗时常数倍 N⁻⁵ᐟ²；另有初值随 N 改变、目标带初始严格为空且总能量精确为 E₀ 的完整光滑解族，在同阶时间首次达到某个固定存在性阈值 η∈(0,E₀)。THRESHOLD：η 与 N 无关，但不是数值认证的能量比例。SPECIFIED COUNTEREXAMPLE：这排除仅依赖固定能量、黏性、滤波器和阈值的普遍 N⁻² 抛物激活等待下界，也排除能量级幂次 α<5/2 的普遍替换。BOUNDARY：首次激活不等于到达后驻留；初始能量已在 N 附近，初值与高阶范数随 N 变化，不是低频起始、同一初值的无限级联、奇点或长期行为。FINITE CHECKS ONLY：8/8 源与来源记录、17 个 FA 标签、16 项独立有理复算及 4 项有限负对照不代替解析证明；唯一完整非作者审查者 C 接受 FA.1–17 与必需 AJ 局部理论。G、R.216–R.217、一般终端缺口、一般正则性与新颖性 OPEN；无图、仿真、新 PDF 或 recap。NOT CLAY。", "PROVED: on the fixed torus, with ν>0, E₀>0 and a fixed smooth band multiplier, every smooth full unforced NS solution needs at least a constant multiple of N⁻⁵ᐟ² time for a prescribed positive amplitude rise. There is also a full smooth family whose data vary with N, whose target band is initially strictly empty, and whose total energy is exactly E₀, reaching a fixed existential threshold η∈(0,E₀) for the first time on the same scale. THRESHOLD: η is independent of N but is not a numerically certified energy fraction. SPECIFIED COUNTEREXAMPLE: this rules out a universal N⁻² parabolic activation waiting bound depending only on fixed energy, viscosity, filter, and threshold, and also rules out a uniform energy-only replacement exponent α<5/2. BOUNDARY: first activation is not residence after arrival. Initial energy is already near N, while the data and higher norms vary with N. This is not a low-frequency origin, an infinite cascade from one fixed datum, a singularity, or long-time behavior. FINITE CHECKS ONLY: 8/8 source and provenance records, 17 FA labels, 16 independent rational recomputations, and four limited negative controls do not replace analytic proof. The sole complete nonauthor reviewer C accepted FA.1–17 and the necessary AJ local theory. G, R.216–R.217, the general terminal gap, general regularity, and novelty remain OPEN. There is no figure, simulation, new PDF, or recap. NOT CLAY."],
  ["固定能量下的频带激活：尖锐的 N⁻⁵ᐟ² 时间尺度", "Band activation at fixed energy: the sharp N⁻⁵ᐟ² timescale"],
  ["研究笔记总索引 · v2.69 · 2026-09-06", "Research-note master index · v2.69 · 2026-09-06"],
  ["CB.1–CB.25 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.25 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["本冻结包没有接受下一条无条件候选；不能把首次激活重命名为驻留、固定数据级联或新缩放机制。", "This freeze accepts no next unconditional candidate. First activation must not be renamed as residence, a fixed-data cascade, or a new scaling mechanism."],
  ["能量级激活时钟已进入 CB.25", "The energy-level activation clock has entered CB.25"],
  ["能量级源项估计给出首次激活的 N⁻⁵ᐟ² 下界；严格空带、固定能量、完整无外力周期 NS 的光滑解族在同阶时间达到固定正阈值。", "The energy-level source estimate gives an N⁻⁵ᐟ² lower bound for first activation. A smooth full unforced periodic NS family with fixed energy and a strictly empty band reaches a fixed positive threshold on the same scale."],
  ["能量预算给出空频带达到固定正阈值的普遍 N⁻⁵ᐟ² 下界，一族完整无外力周期光滑 NS 解达到同阶上界。因此仅靠总能量的普遍 N⁻² 抛物等待时间被排除；首次激活不等于到达后驻留，也不是同一初值的无限级联。OPEN · NOT CLAY.", "The energy budget gives a universal N⁻⁵ᐟ² lower bound for an empty band to reach a fixed positive threshold, and a family of full unforced periodic smooth NS solutions attains the same-order upper bound. Thus a universal N⁻² parabolic waiting time from total energy alone is excluded. First activation is not residence after arrival or an infinite cascade from one fixed datum. OPEN · NOT CLAY."],
  ["全周期梯度测试保留二阶源项、应变与端点；固定正定二次组合存在有限类障碍，正原子分支迫使特定二阶成本发散，但不能反推 W_z 发散。", "Full-periodic gradient tests retain second-order sources, strain, and endpoints. Fixed positive-definite quadratic combinations face a finite-class obstruction, and the positive-atom branch forces divergence of a specific second-order cost, without implying divergence of W_z."],
  ["投影给出逐时幅度一致上界；联合截断只控制有符号累计压力。W_z 与混合压力平方是两条不同且未付的充分接口。", "Projection gives a pointwise amplitude-uniform bound, while joint truncation controls only signed cumulative pressure. W_z and the mixed-pressure square are two distinct unpaid sufficient interfaces."],
  ["完整 NS 家族达到同阶", "full NS family attains the same scale"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.25 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.25 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["无驻留或固定数据级联结论 · NOT CLAY", "no residence or fixed-data cascade result · NOT CLAY"],
  ["下一研究候选必须支付额外动态输入", "The next research candidate must pay an additional dynamical input"],
  ["阅读 CB.25 HTML", "Read CB.25 HTML"],
  ["阅读最新 CB.25 笔记 →", "Read the latest CB.25 note →"],
  ["这排除指定的普遍 N⁻² 抛物等待时间，但不证明到达后驻留、低频起始、同一初值的无限级联、奇点或全局正则性。", "This excludes the specified universal N⁻² parabolic waiting time, but proves no post-arrival residence, low-frequency origin, infinite cascade from one fixed datum, singularity, or global regularity."],
  ["综述 v2.69 · 2026-09-06", "Research review v2.69 · 2026-09-06"],
  ["CB.1–CB.25 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.25 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.25｜固定能量下的频带激活：尖锐的 N⁻⁵ᐟ² 时间尺度", "CB.25 | Band activation at fixed energy: the sharp N⁻⁵ᐟ² timescale"],
  ["CB.26 只是下一章占位，不是已完成研究。到达后驻留、成熟历史、固定数据无限级联、G、R.216–R.217、一般终端缺口、一般正则性与 Clay 均未关闭。", "CB.26 is only a next-chapter placeholder, not completed research. Post-arrival residence, mature history, an infinite fixed-data cascade, G, R.216–R.217, the general terminal gap, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.25", "The independent Clay-B route stops at CB.25"],
  ["Clay-B 频带激活笔记快捷入口", "Clay-B frequency-activation note shortcuts"],
  ["Clay-B 频带激活结论", "Clay-B frequency-activation conclusions"],
  ["Clay-B 已得到固定能量下频带首次激活的尖锐 N⁻⁵ᐟ² 时钟：普遍能量估计给下界，严格空带的完整无外力周期 NS 光滑解族达到同阶。这排除仅靠总能量的普遍 N⁻² 等待时间，但不提供到达后驻留、低频起始或同一初值的无限级联。下一候选必须支付真正额外的动态输入。", "Clay-B has obtained the sharp N⁻⁵ᐟ² clock for fixed-energy first band activation: a universal energy estimate gives the lower bound, and a smooth full unforced periodic NS family with a strictly empty band attains the same scale. This excludes a universal N⁻² waiting time from total energy alone, but provides no post-arrival residence, low-frequency origin, or infinite cascade from one fixed datum. The next candidate must pay a genuinely additional dynamical input."],
  ["FA 给出空频带首次达到固定正阈值的 N⁻⁵ᐟ² 普遍下界，并由完整 NS 光滑解族达到同阶。", "FA gives a universal N⁻⁵ᐟ² lower bound for an empty band to first reach a fixed positive threshold, attained on the same scale by a smooth full NS family."],
  ["N⁻⁵ᐟ² 普遍下界", "universal N⁻⁵ᐟ² lower bound"],
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
  assert.equal(rows.length, translations.size, "FrequencyActivation translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.25"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "FrequencyActivation source-string count drift");
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

process.stdout.write(JSON.stringify({ release: "ClayB-FrequencyActivation-20260907", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
