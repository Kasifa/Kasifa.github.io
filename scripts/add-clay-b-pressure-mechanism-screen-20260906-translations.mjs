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
const prefix = "claybpressuremechanismscreen20260906";

const translations = new Map([
  ["本轮完整阅读", "This round reads"],
  ["的 §2–§4（PDF 第 3–20 页、期刊第 67–84 页），并核对", "§§2–4 in full (PDF pages 3–20; journal pages 67–84), and checks"],
  ["的相关 §2–§4；书目信息由", "for the corresponding §§2–4; the bibliographic details are cross-checked against"],
  ["文献综述 v2.58 · 2026-09-06", "Literature review v2.58 · 2026-09-06"],
  ["与机构页交叉确认。原文径向恒等式本身不需要条件 C；后续还使用中心、时间一致压力势界、强 L² 左连续性、势的左连续性、局部能量和小量正则性。正式版的远场极限按 R→∞、末段按 ε_*(1) 核对，局部迭代尺度按 θ^kρ 理解。外引正则性论文未逐篇全文重审，整套全空间定理没有导入周期能量框架，也未做穷尽新颖性检索。", "and the institutional catalogue page. The original radial identity itself does not need condition C; the later proof also uses a center- and time-uniform pressure-potential bound, strong L² left continuity, left continuity of the potential, local energy, and epsilon regularity. The published far-field limit is checked as R→∞, its final step as ε_*(1), and the local iteration scale is read as θ^kρ. The externally cited regularity papers were not individually reread in full, the complete whole-space theorem was not imported into the periodic energy framework, and no exhaustive novelty search was performed."],
  ["阅读完整 CB.14 笔记", "Read the complete CB.14 note"],
  ["CB.14 · Clay-B 单侧压力机制的文献和主张边界", "CB.14 · Literature and claim boundary for the Clay-B one-sided pressure mechanism"],
  ["CB.14 · ClayB-PressureMechanismScreen-20260906 公开边界", "CB.14 · Public boundary for ClayB-PressureMechanismScreen-20260906"],
  ["MiS 92/2001 预印本", "MiS 92/2001 preprint"],
  ["PROVED LOCALLY：BF 精确重算规范周期压力的径向空间恒等式，固定外尺度平滑修正由能量支付，但局部环带与时间一致单侧压力势未付。ENERGY-CLASS OBSTRUCTION：BG 给真实 p_- 势的尺度一致 L¹_t 与固定 R 的 L_t^(4/3) 上界；一个弱连续、满足全局标量能量不等式的抽象时间族具有发散端点势，但它直接违反 NS 涡量方程，不是弱 NS、suitable 解或 NS 反例。两套能量界不宣称最优时间指数。FINITE CHECKS ONLY：四份文本源、37 个公式编号、74/74 文件哈希、25 项有理复算与负向变异不替代证明。OPEN：真实 NS 是否强制或绕过条件 C，Q_J、净压力功上界、移动缩球 G 与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。", "PROVED LOCALLY: BF exactly recomputes the radial spatial identity for normalized periodic pressure. Energy pays the smooth fixed-outer-scale correction, but not the local annulus or the time-uniform one-sided pressure potential. ENERGY-CLASS OBSTRUCTION: BG gives a scale-uniform L¹_t bound and a fixed-R L_t^(4/3) bound for the genuine p_- potential. A weakly continuous abstract time family satisfying a global scalar energy inequality has a divergent endpoint potential, but it directly violates the NS vorticity equation and is neither a weak NS solution, a suitable solution, nor an NS counterexample. Neither energy bound is claimed to have an optimal time exponent. FINITE CHECKS ONLY: four text sources, 37 formula labels, 74/74 file hashes, 25 rational recomputations, and negative mutations do not replace proof. OPEN: whether genuine NS forces or bypasses condition C, Q_J, the net pressure-work upper bound, moving shrinking G, and general regularity. No complete novelty review, external peer review, or Clay claim is made, and there is no figure, simulation, or cumulative recap. NOT CLAY."],
  ["Seregin–Šverák 正式发表版作者副本", "Seregin–Šverák author copy of the published paper"],
  ["单侧压力机制：周期恒等式与能量类边界", "One-sided pressure mechanism: periodic identity and energy-class boundary"],
  ["研究笔记总索引 · v2.58 · 2026-09-06", "Research-note master index · v2.58 · 2026-09-06"],
  ["CB.1–CB.14 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.14 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["查看原始证明与主张边界", "Review the primary proof and claim boundary"],
  ["规范周期压力的径向空间恒等式可以精确重算，固定外尺度修正由能量支付；局部环带和时间一致负压力势仍未付。基本能量只给时间可积控制。一个抽象端点反检查明确不是 NS 解，因此本轮停止 energy-only 候选，而不排除真实 NS 动力学。G OPEN。NOT CLAY.", "The radial spatial identity for normalized periodic pressure can be recomputed exactly, and energy pays the fixed-outer-scale correction. The local annulus and time-uniform negative-pressure potential remain unpaid. Basic energy supplies only time-integrable control. An abstract endpoint countercheck is explicitly not an NS solution, so this round stops the energy-only candidate without excluding genuine NS dynamics. G OPEN. NOT CLAY."],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.14 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.14 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：有界路线重评", "Next research question: bounded route reassessment"],
  ["阅读最新 CB.14 压力机制筛查笔记 →", "Read the latest CB.14 pressure-mechanism-screen note →"],
  ["真实 NS 机制、Q_J 与 G OPEN · NOT CLAY", "Genuine NS mechanism, Q_J, and G OPEN · NOT CLAY"],
  ["只保留真正使用 NS 演化、尚未落入既有范数成本的候选。每条必须提出明确的新不等式或紧性/刚性命题及其缺失输入；否则不另起章节或计算任务。", "Retain only candidates that genuinely use NS evolution and have not already fallen into the known norm costs. Each must state a specific new inequality or compactness/rigidity proposition and its missing inputs; otherwise no new chapter or computation task is opened."],
  ["周期径向恒等式精确成立", "Periodic radial identity holds exactly"],
  ["周期压力机制筛查已进入 CB.14", "The periodic pressure-mechanism screen now forms CB.14"],
  ["综述 v2.58 · 2026-09-06", "Review v2.58 · 2026-09-06"],
  ["BF 在零均值周期压力规范下精确重算径向恒等式：固定外尺度平滑修正由总能量支付，但局部环带仍只有随内尺度恶化的粗界，时间一致单侧压力势仍是额外输入。", "BF exactly recomputes the radial identity under the zero-mean periodic pressure normalization. Total energy pays the smooth fixed-outer-scale correction, but the local annulus retains only a coarse bound that worsens with the inner scale, and the time-uniform one-sided pressure potential remains an extra input."],
  ["BF–BG 已区分精确空间恒等式、固定外尺度能量修正、未付局部环带、时间可积压力势与明确非 NS 的端点反检查；结果见下一个正式路线节点。", "BF–BG now separate the exact spatial identity, the fixed-outer-scale energy correction, the unpaid local annulus, the time-integrable pressure potential, and an endpoint countercheck that is explicitly non-NS; the result appears in the next formal route node."],
  ["BG 给真实 p_- 势的尺度一致 L¹_t 与固定尺度 L_t^(4/3) 界，并以明确非 NS 的抽象能量时间族阻断端点推断；这不构成 NS 反例，也不宣称 4/3 最优。", "BG gives a scale-uniform L¹_t bound and a fixed-scale L_t^(4/3) bound for the genuine p_- potential, then blocks the endpoint inference with an abstract energy time family that is explicitly non-NS. This is not an NS counterexample, and 4/3 is not claimed optimal."],
  ["CB.1–CB.14 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.14 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.13 近期源 norm 路线停止 → BF 周期径向恒等式 → 固定外尺度修正已付、局部环带未付 → BG 能量类仅给时间可积 → 非 NS 抽象端点反检查 → energy-only 候选停止", "CB.13 recent-source norm route stops → BF periodic radial identity → fixed-outer-scale correction paid, local annulus unpaid → BG energy class gives only time integrability → non-NS abstract endpoint countercheck → energy-only candidate stops"],
  ["CB.14：压力机制筛查", "CB.14: pressure-mechanism screen"],
  ["CB.14｜单侧压力机制：周期恒等式与能量类边界", "CB.14 | One-sided pressure mechanism: periodic identity and energy-class boundary"],
  ["CB.15 只是下一章占位，不是已完成研究。真正使用 NS 演化的新机制、Q_J、近期源带符号净压力功上界、条件 C 的动态强制或绕过、移动缩球 G/G-P/G-C 与首次奇点排除均未冻结。", "CB.15 is only a placeholder for the next chapter, not completed research. A new mechanism that genuinely uses NS evolution, Q_J, the signed recent-source net pressure-work upper bound, dynamical enforcement or bypass of condition C, moving shrinking G/G-P/G-C, and first-singularity exclusion are not frozen."],
  ["Clay-B 独立路线停在 CB.14", "The independent Clay-B route stops at CB.14"],
  ["Clay-B 压力机制筛查笔记快捷入口", "Clay-B pressure-mechanism-screen note shortcuts"],
  ["Clay-B 压力机制筛查结论", "Clay-B pressure-mechanism-screen result boundary"],
  ["Clay-B 已完成单侧压力机制的一轮有界筛查：周期径向恒等式精确成立，固定外尺度修正由能量支付；基本能量只给负压力势的时间可积控制，抽象端点反检查明确不是 NS 解。energy-only 候选停止，真实 NS 机制、Q_J 和合同 G 继续开放。", "Clay-B has completed a bounded screen of the one-sided pressure mechanism. The periodic radial identity holds exactly and energy pays the fixed-outer-scale correction. Basic energy gives only time-integrable control of the negative-pressure potential, while the abstract endpoint countercheck is explicitly not an NS solution. The energy-only candidate stops; genuine NS mechanisms, Q_J, and contract G remain open."],
  ["energy-only 端点推断停止", "energy-only endpoint inference stops"],
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
  assert.equal(rows.length, translations.size, "PressureMechanismScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.14"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "PressureMechanismScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-PressureMechanismScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
