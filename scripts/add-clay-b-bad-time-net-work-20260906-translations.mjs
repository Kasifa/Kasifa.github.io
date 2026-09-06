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
const prefix = "claybbadtimenetwork20260906";

const translations = new Map([
  ["本轮只返回元数据；实际核对使用", "returned only metadata in this check; the actual reading used the"],
  ["的 Theorem B、正则点定义及覆盖位置，转录 OCR 存在符号损坏，因此不声称重审全篇证明。", "for Theorem B, the definition of regular points, and the covering argument. The transcription has OCR damage in mathematical symbols, so no full-proof reaudit is claimed."],
  ["的耗散/决定波数具有不同域、范数与量词，不能替代本章的局部压力功预算。", "use dissipation or determining wavenumbers with different domains, norms, and quantifiers; they cannot replace the local pressure-work budget in this chapter."],
  ["公开原文转录", "public transcription of the original article"],
  ["文献综述 v2.54 · 2026-09-06", "Literature review v2.54 · 2026-09-06"],
  ["阅读完整 CB.10 笔记", "Read the complete CB.10 note"],
  ["只用于交叉核对固定环带接口。", "are used only to cross-check the fixed-annulus interface."],
  ["Caffarelli–Kohn–Nirenberg 1982 正式书目入口", "Caffarelli–Kohn–Nirenberg 1982 formal bibliographic entry"],
  ["CB.10 · Clay-B 坏时间净工作的文献和主张边界", "CB.10 · Literature and claim boundary for Clay-B bad-time net work"],
  ["CB.10 · ClayB-BadTimeNetWork-20260906 公开边界", "CB.10 · Public boundary for ClayB-BadTimeNetWork-20260906"],
  ["PROVED LOCALLY：AK 支付完整低频压力配对并量化能量高频尾；AL 在周期规范下复证带基线 1 和 a⁻²ν⁻² 依赖的耗散波数能量接口；AM 用无散增益支付所有含低频速度的压力，保留 p(h) 的全部高高低输出；AN 给保留原速度测试的全环面小尾原型；AP 从已知 CKN 部分正则性为同一 suitable continuation 选择依解的固定正则环带；AO 显式处理近远源、频率截止交换子、环带 B||∇u||₂² 成本和积分因子，在局部尾小的好时间吸收高高压力。NECESSARY CONDITION：对同一解、固定环带/半径/截止/能量界/c₀ 的每个合法大局部 L³ 成熟窗口序列，AQ 证明 liminf 𝓑_J/Hχ(t)≥1，其中 𝓑_J 是坏时间上 [Kχ(p_h)−¾Dχ]_+ 的积分；带权带符号版本也保留。STRICT LIMITS：这是下界，不是上界；不证明该序列或奇点存在，也不证明它们不可能；没有总变差控制时不可免费删除趋近 1 的时间权重；固定环带常数不称为缩球一致。FINITE COMPUTATION：无。OPEN：𝓑_J 的真实 NS 上界、缩球、移动路径、G/G-P/G-C、R.216–R.217、首次奇点排除与一般正则性。文献核查有界，访问限制与 OCR 风险如上；没有新颖性、优先权、发表等级或 Clay 声明，无图件、仿真、数值证书或累计 recap。NOT CLAY。", "PROVED LOCALLY: AK pays the complete low-frequency pressure pairing and quantifies the energy high-frequency tail. AL rederives the periodic dissipation-wavenumber energy interface with baseline one and a⁻²ν⁻² dependence. AM uses a solenoidal gain to pay all pressure involving low velocity frequencies while retaining every high–high low output in p(h). AN gives a whole-torus small-tail prototype with the original velocity test. From known CKN partial regularity, AP selects a solution-dependent fixed regular annulus for the same suitable continuation. AO explicitly treats near and far sources, the frequency-cutoff commutator, the annular B||∇u||₂² cost, and the integrating factor, absorbing high–high pressure on good times with a small local tail. NECESSARY CONDITION: for every legal mature-window sequence with large local L³ norm for the same solution and fixed annulus, radius, cutoffs, energy bound, and c₀, AQ proves liminf 𝓑_J/Hχ(t)≥1, where 𝓑_J integrates [Kχ(p_h)−¾Dχ]_+ on bad times; the weighted signed version is retained. STRICT LIMITS: this is a lower bound, not an upper bound. It proves neither existence nor nonexistence of the sequence or a singularity. Without total-variation control, the time weight tending to one cannot be removed for free. Fixed-annulus constants are not called uniform under shrinking. FINITE COMPUTATION: none. OPEN: a genuine NS upper bound for 𝓑_J, shrinking balls, moving paths, G/G-P/G-C, R.216–R.217, first-singularity exclusion, and general regularity. The literature check is bounded and retains the access and OCR risks above. There is no novelty, priority, publication-level, or Clay claim, and no figure, simulation, numerical certificate, or cumulative recap. NOT CLAY."],
  ["坏时间净压力工作：从频率支付到必要下界", "Bad-time net pressure work: from frequency payment to a necessary lower bound"],
  ["研究笔记总索引 · v2.54 · 2026-09-06", "Research-note master index · v2.54 · 2026-09-06"],
  ["CB.1–CB.10 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.10 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["保持 AQ.7–AQ.8 的同一窗口、截止、测试速度、坏时间集合与时间权重，逐频带寻找真实无散增益或符号抵消；不能用坏集合小测度替代工作积分，也不能免费删除积分因子。该问题尚未冻结。", "Keep the same window, cutoffs, test velocity, bad-time set, and time weight from AQ.7–AQ.8, and seek a genuine solenoidal gain or signed cancellation frequency band by frequency band. Small measure of the bad set cannot replace control of the work integral, and the integrating factor cannot be removed for free. This question is not yet frozen."],
  ["成熟窗口坏时间机制已进入 CB.10", "The mature-window bad-time mechanism now forms CB.10"],
  ["低频与好时间压力：已支付", "Low-frequency and good-time pressure: paid"],
  ["坏时间正净工作：必要下界", "Positive bad-time net work: necessary lower bound"],
  ["所需上界、缩球与 G OPEN · NOT CLAY", "Required upper bound, shrinking balls, and G OPEN · NOT CLAY"],
  ["同一解的低频参与压力与固定环带好时间高高压力已经支付。若合法的大局部 L³ 成熟窗口序列存在，坏时间正净工作满足 liminf 𝓑_J/Hχ(t)≥1，并保留带权带符号版本。它是条件必要下界，不是上界，不证明序列、奇点或合同 G。NOT CLAY.", "For the same solution, pressure involving low velocity frequencies and fixed-annulus high–high pressure on good times are paid. If a legal mature-window sequence with large local L³ norm exists, positive bad-time net work satisfies liminf 𝓑_J/Hχ(t)≥1, with a weighted signed version retained. This is a conditional necessary lower bound, not an upper bound, and it proves neither the sequence, a singularity, nor contract G. NOT CLAY."],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.10 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.10 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：坏时间带符号高高压力工作的 NS 上界", "Next research question: an NS upper bound for signed bad-time high–high pressure work"],
  ["阅读最新 CB.10 坏时间净工作笔记 →", "Read the latest CB.10 bad-time-net-work note →"],
  ["综述 v2.54 · 2026-09-06", "Review v2.54 · 2026-09-06"],
  ["AK–AQ 已区分已付低频/好时间压力与坏时间必要净工作；结果见下一个正式路线节点。", "AK–AQ now separate paid low-frequency and good-time pressure from necessary bad-time net work; the result appears in the next formal route node."],
  ["AK/AL 定位能量尾的时间速率缺口；AM 借无散结构支付所有含低频速度的压力。AP 从 CKN 文献输入选出依解的固定正则环带，AO 在局部高频尾小的好时间吸收高高压力，同时保留截止交换子、环带能量成本与坏时间带符号净工作。", "AK/AL identify the missing time rate for the energy tail. AM uses solenoidality to pay all pressure involving low velocity frequencies. From the CKN literature input, AP selects a solution-dependent fixed regular annulus. AO absorbs high–high pressure on good times with a small local high-frequency tail while retaining cutoff commutators, annular energy costs, and signed bad-time net work."],
  ["AQ 对同一解、固定参数的一列合法大局部 L³ 成熟窗口证明 liminf 𝓑_J/Hχ(t)≥1，并保留实际积分因子和符号。方向是必要下界，不是上界；不证明序列或奇点存在，也不把固定环带常数称为缩球一致。", "For a legal mature-window sequence with large local L³ norm for the same solution and fixed parameters, AQ proves liminf 𝓑_J/Hχ(t)≥1 while retaining the actual integrating factor and sign. The direction is a necessary lower bound, not an upper bound. It proves neither the sequence nor a singularity, and does not call fixed-annulus constants uniform under shrinking."],
  ["CB.1–CB.10 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.10 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.10：坏时间净工作必要下界", "CB.10: necessary lower bound for bad-time net work"],
  ["CB.10｜坏时间净压力工作：从频率支付到必要下界", "CB.10 | Bad-time net pressure work: from frequency payment to a necessary lower bound"],
  ["CB.10｜频率支付、固定环带与坏时间净工作必要下界", "CB.10 | Frequency payment, a fixed annulus, and the necessary lower bound for bad-time net work"],
  ["CB.11 只是下一章占位，不是已完成研究。坏时间带符号净工作的真实 NS 上界、缩球一致常数、移动路径、G/G-P/G-C、实际 R.216–R.217 输入与首次奇点排除尚未冻结；不把后续研发写成已证结论。", "CB.11 is only a placeholder for the next chapter, not completed research. A genuine NS upper bound for signed bad-time net work, shrinking-scale uniform constants, moving paths, G/G-P/G-C, actual R.216–R.217 inputs, and first-singularity exclusion are not frozen; later research is not presented as proved."],
  ["CB.9 真实压力功早时增长 → AK/AL 频率速率缺口 → AM 低频参与压力已付 → AP/AO 固定环带好时间已付 → AQ 坏时间正净工作必要下界 → 真实 NS 上界 OPEN", "CB.9 genuine early-time pressure-work growth → AK/AL missing frequency rate → AM pays pressure involving low velocity frequencies → AP/AO pay good times on a fixed annulus → AQ necessary lower bound for positive bad-time net work → genuine NS upper bound OPEN"],
  ["Clay-B 独立路线停在 CB.10", "The independent Clay-B route stops at CB.10"],
  ["Clay-B 坏时间净工作笔记快捷入口", "Clay-B bad-time-net-work note shortcuts"],
  ["Clay-B 坏时间净工作结论", "Clay-B bad-time-net-work result boundary"],
  ["Clay-B 已在同一解的固定成熟窗口中支付低频参与压力和固定环带好时间高高压力；若合法的大局部 L³ 序列存在，坏时间正净工作必须达到终端局部能量量级。这是必要下界，不是上界；真正的 NS 上界、缩球路径和合同 G 继续开放。", "Within fixed mature windows for the same solution, Clay-B now pays pressure involving low velocity frequencies and fixed-annulus high–high pressure on good times. If a legal large-local-L³ sequence exists, positive bad-time net work must reach the scale of the terminal local energy. This is a necessary lower bound, not an upper bound. A genuine NS upper bound, shrinking paths, and contract G remain open."],
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
  assert.equal(rows.length, translations.size, "BadTimeNetWork translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.10"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "BadTimeNetWork source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-BadTimeNetWork-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
