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
const prefix = "claybpressureworkwindow20260906";

const translations = new Map([
  ["处理全空间负阶 Besov 空间的小数据 norm inflation；", "treats small-data norm inflation in a negative-order Besov space on the whole space;"],
  ["固定初始 enstrophy 并数值优化终端 enstrophy。两者都不等同于本章固定初始速度 L² 能量、初始 H 与 enstrophy 发散的早时解族。", "fixes initial enstrophy and numerically optimizes terminal enstrophy. Neither is the early-time family here, which fixes the initial velocity L² energy while initial H and enstrophy diverge."],
  ["文献综述 v2.53 · 2026-09-06", "Literature review v2.53 · 2026-09-06"],
  ["已经给出 Lq 压力功恒等式和不贡献该积分的 speed-dependent pressure moderator；这些不是本站的新发现。", "already gives the Lq pressure-work identity and speed-dependent pressure moderators that do not contribute to that integral; these are not new discoveries of this site."],
  ["阅读完整 CB.9 笔记", "Read the complete CB.9 note"],
  ["CB.9 · Clay-B 正压力功短窗的文献和主张边界", "CB.9 · Literature and claim boundary for the Clay-B positive-pressure-work short window"],
  ["CB.9 · ClayB-PressureWorkWindow-20260906 公开边界", "CB.9 · Public boundary for ClayB-PressureWorkWindow-20260906"],
  ["PROVED LOCALLY：AI 通过 curl cutoff 和受控压力调制把固定周期正压力功种子转成光滑紧支撑 Euclidean 无散场；固定 E₀ 单泡满足 W≈ε⁻⁴、D≈ε⁻⁷ᐟ²、H≈ε⁻³ᐟ²、||∇u||₂²≈ε⁻²，并有真实初始净增长。AJ 给出扩张环面上一致的 H⁵ 生命周期、压力功连续性和 tε=τ₀ε^(5/2) 窗口，其中 H(tε)/H(0)≥1+δ₀，累计梯度平方为 O(√ε)。因此只排除从初始时刻起、前置系数为 1、无加性预算、C 仅依赖 E₀ 的精确指数估计。STRICT LIMITS：tε/ε²→0，严格早于成熟扩散时间；初始 H 与 enstrophy 发散，且解族随 ε 更换初值；不排除 K>1、加性预算或常数依赖更多初值范数的估计，也不构成一般 L³ norm inflation、固定单解首次奇点或正则性反例。FINITE COMPUTATION：无。OPEN：成熟时间同一解的有符号压力功、近源、外壳、首次奇点、缩球、原路径和 G/G-P/G-C。文献核查有界，不作新颖性、优先权、发表等级或 Clay 声明；无图件、仿真、数值证书或累计 recap。NOT CLAY。", "PROVED LOCALLY: through curl cutoff and controlled pressure modulation, AI turns a fixed periodic positive-pressure-work seed into a smooth compactly supported Euclidean solenoidal field. A fixed-E₀ single bubble has W≈ε⁻⁴, D≈ε⁻⁷ᐟ², H≈ε⁻³ᐟ², and ||∇u||₂²≈ε⁻², with genuine initial net growth. AJ gives a uniform H⁵ lifespan on expanding tori, continuity of pressure work, and a tε=τ₀ε^(5/2) window in which H(tε)/H(0)≥1+δ₀ and the accumulated squared gradient is O(√ε). This excludes only the exact exponential estimate required from initial time, with leading factor one, no additive budget, and C depending solely on E₀. STRICT LIMITS: tε/ε²→0, strictly before the mature diffusion time; initial H and enstrophy diverge, and the family changes its initial data with ε. Bounds with K>1, an additive budget, or dependence on more initial norms are not excluded, nor is this general L³ norm inflation, a first-singularity counterexample for one fixed solution, or a regularity counterexample. FINITE COMPUTATION: none. OPEN: signed pressure work for the same solution at mature time, the near field, outer shell, first singularity, shrinking balls, original paths, and G/G-P/G-C. The literature check is bounded; there is no novelty, priority, publication-level, or Clay claim, and no figure, simulation, numerical certificate, or cumulative recap. NOT CLAY."],
  ["固定总能量不能给出这条 L³ 增长预算", "Fixed total energy cannot provide this L³ growth budget"],
  ["研究笔记总索引 · v2.53 · 2026-09-06", "Research-note master index · v2.53 · 2026-09-06"],
  ["CB.1–CB.9 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.9 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["固定半径并进入 t≥Cε²，保留近源压力、外壳输运和黏性项，逐项说明时间、空间尺度、初值依赖与可积性来源；不能把变化初值族的早时窗口平移成成熟历史。该问题尚未冻结。", "Fix the radius and enter t≥Cε², retaining near-source pressure, outer-shell transport, and viscosity. For each term, identify the time and spatial scale, initial-data dependence, and source of integrability. The early window of a changing-data family cannot be shifted into a mature history. This question is not yet frozen."],
  ["固定比例 H 增长；作用量趋零", "Fixed relative H growth; action tends to zero"],
  ["紧支撑化保留严格正压力功；固定能量单泡在 tε=τ₀ε^(5/2) 内产生固定比例的真实 L³ 三次方增长，而累计梯度平方为 O(√ε)。这只排除前置系数为 1、无加性预算、常数仅依赖 E₀ 的准确估计；窗口严格早于成熟时间，固定单解、首次奇点和合同 G 仍 OPEN。NOT CLAY.", "Compact localization preserves strictly positive pressure work. At fixed energy, one bubble produces a fixed relative increase of the genuine cubic L³ quantity by tε=τ₀ε^(5/2), while the accumulated squared gradient is O(√ε). This excludes only the exact estimate with leading factor one, no additive budget, and a constant depending solely on E₀. The window is strictly before mature time; one fixed solution, first singularities, and contract G remain OPEN. NOT CLAY."],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.9 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.9 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：同一解的成熟时间压力功预算", "Next research question: mature-time pressure-work budget for the same solution"],
  ["阅读最新 CB.9 压力功窗口笔记 →", "Read the latest CB.9 pressure-work-window note →"],
  ["早于成熟时间；G OPEN · NOT CLAY", "Before mature time; G OPEN · NOT CLAY"],
  ["真实压力功短窗已进入 CB.9", "The genuine pressure-work short window now forms CB.9"],
  ["真实正压力功与净增长：已证", "Genuine positive pressure work and net growth: proved"],
  ["综述 v2.53 · 2026-09-06", "Review v2.53 · 2026-09-06"],
  ["AI 从固定有限 Fourier 周期种子出发，用 curl cutoff 和受控高频压力调制得到光滑紧支撑的全空间无散场，并在固定 L² 能量的单泡上得到真实初始净增长。其 W、D、H 和 enstrophy 尺度分别为 ε⁻⁴、ε⁻⁷ᐟ²、ε⁻³ᐟ² 和 ε⁻²。", "Starting from a fixed finite-Fourier periodic seed, AI uses curl cutoff and controlled high-frequency pressure modulation to obtain a smooth compactly supported whole-space solenoidal field, then gets genuine initial net growth from a fixed-L²-energy single bubble. Its W, D, H, and enstrophy scales are ε⁻⁴, ε⁻⁷ᐟ², ε⁻³ᐟ², and ε⁻², respectively."],
  ["AI/AJ 已把正压力功和净 L³ 增长保持到统一早时窗口；结果见下一个正式路线节点。", "AI/AJ now retain positive pressure work and net L³ growth over a uniform early-time window; the result appears in the next formal route node."],
  ["AJ 在扩张环面上建立与 L 和有效黏性无关的 H⁵ 短时控制，使正压力功维持到 tε=τ₀ε^(5/2)：H(tε)/H(0)≥1+δ₀，而累计梯度平方为 O(√ε)。因此一条量词准确的固定能量指数预算失败；允许额外前置因子、加性预算或初值范数依赖的估计并未被排除。", "On expanding tori, AJ establishes short-time H⁵ control independent of L and the effective viscosity, retaining positive pressure work until tε=τ₀ε^(5/2): H(tε)/H(0)≥1+δ₀, while the accumulated squared gradient is O(√ε). Thus one fixed-energy exponential budget with exact quantifiers fails. Estimates allowing an additional leading factor, additive budget, or dependence on initial norms are not excluded."],
  ["CB.1–CB.9 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.9 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.10 只是下一章占位，不是已完成研究。同一固定解在成熟时间的真实压力功、近源、外壳、首次奇点、缩球、原移动路径及 G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。", "CB.10 is only a placeholder for the next chapter, not completed research. Genuine pressure work for one fixed solution at mature time, the near field, outer shell, first singularity, shrinking balls, the original moving path, and G/G-P/G-C are not frozen; later research is not presented as proved."],
  ["CB.8 残差候选失败但不做功 → AI 紧支撑真实正压力功 → 固定能量初始净增长 → AJ 统一早时窗口与固定相对 H 增长 → 成熟时间同一解完整配对 OPEN", "CB.8 residual candidate fails but does no work → AI compact genuine positive pressure work → fixed-energy initial net growth → AJ uniform early window and fixed relative H growth → complete same-solution pairing at mature time OPEN"],
  ["CB.9：正压力功与统一早时窗口", "CB.9: positive pressure work and a uniform early-time window"],
  ["CB.9｜固定总能量不能给出这条 L³ 增长预算", "CB.9 | Fixed total energy cannot provide this L³ growth budget"],
  ["CB.9｜紧支撑正压力功与统一早时真实 L³ 增长", "CB.9 | Compact positive pressure work and uniform early-time genuine L³ growth"],
  ["Clay-B 独立路线停在 CB.9", "The independent Clay-B route stops at CB.9"],
  ["Clay-B 压力功窗口笔记快捷入口", "Clay-B pressure-work-window note shortcuts"],
  ["Clay-B 压力功窗口结论", "Clay-B pressure-work-window result boundary"],
  ["Clay-B 已把真实正压力功保持到统一早时窗口：固定能量单泡取得固定比例的 L³ 三次方增长，而累计梯度平方趋于零。这只排除一条量词精确的候选预算；窗口仍早于成熟扩散时间，同一固定解、近源、外壳与合同 G 继续开放。", "Clay-B now retains genuine positive pressure work through a uniform early-time window: a fixed-energy single bubble gains a fixed relative amount of the cubic L³ quantity while the accumulated squared gradient tends to zero. This excludes only one candidate budget with exact quantifiers. The window remains before the mature diffusion time; one fixed solution, the near field, outer shell, and contract G remain open."],
]);

function validateTranslation(source, en) {
  assert.ok(!containsChinese(en), "Chinese remains in translation: " + source);
  assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(source), "protected token drift: " + source);
}

process.chdir(root);
const [source, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp("^" + prefix + "\\d+$");

if (checkOnly) {
  const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
  assert.deepEqual(source.filter((entry) => !currentByZh.has(entry.zh)), [], "site still has untranslated Chinese strings");
  const rows = current.filter((entry) => rowPattern.test(entry.id));
  assert.equal(rows.length, translations.size, "PressureWorkWindow translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.9"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "PressureWorkWindow source-string count drift");
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

process.stdout.write(JSON.stringify({ release: "ClayB-PressureWorkWindow-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
