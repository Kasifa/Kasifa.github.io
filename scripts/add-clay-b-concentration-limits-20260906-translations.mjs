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
const prefix = "claybconcentrationlimits20260906";

const translations = new Map([
  ["，本站按同一定义第 (3) 项、Proposition 2.2 和标准局部域关系解释为", ", which this site interprets, consistently with part (3) of the same definition, Proposition 2.2, and the standard local-domain relation, as"],
  ["：不是作者发布的勘误，也不是本站重证原定理。", ": it is neither an author-issued erratum nor a local reproof of the original theorem."],
  ["。这是显式", ". This is explicitly"],
  ["承担实际奇点处固定球内点 L³ 集中的文献输入。周期应用限制到坐标球并取 Γ=∅；其 Definition 2.1(1) 原页排成", "supplies the literature input for fixed-ball interior L³ concentration at an actual singularity. The periodic application restricts to a coordinate ball and takes Γ=∅; the printed Definition 2.1(1) reads"],
  ["文献综述 v2.49 · 2026-09-06", "Literature review v2.49 · 2026-09-06"],
  ["只承担经典局部光滑解及寿命依赖背景。", "is used only as classical background for local smooth solutions and lifespan dependence."],
  ["Clay-B 固定球集中、原路径与持留成本的文献和主张边界", "Literature and claim boundary for Clay-B fixed-ball concentration, original paths, and persistence costs"],
  ["ClayB-ConcentrationLimits-20260906 公开边界", "Public boundary for ClayB-ConcentrationLimits-20260906"],
  ["LITERATURE CONDITIONAL：Albritton--Barker 固定球结论及上述排字解释。PROVED LOCALLY：固定 R 的原指定路径漂移界；任意 α<2/5 的解依赖阶梯式慢对角半径；L_t^4L_x^3 与端点发散相容；精确能量逻辑模型的 curl/moment 非 NS 排除；真正平滑无外力黏性一周期 NS 族否定无初值/外部成本的所有光滑窗口 AA.1 型 L³ 持留；固定解固定球的裸远源压力冲量不超过 C c₀M²r⁻¹L⁻⁵。FINITE COMPUTATION：无。STRICT LIMITS：慢半径不是预设幂律或单一可微变尺度路径；非 NS 模型不是 NS 反例；真实 NS 族初始能量增长且 t_B/r²→0，不否定成熟时间或首次奇点限定版；AA.18 不是速度加权压力功。OPEN：近源压力、非线性输运、黏性变化、定量缩球、原路径柱、G/G-P/G-C、R.216–R.217 及此前 U/V/W/Y 缺口。没有图件、仿真、数值证书、新颖性、优先权、发表等级或 Clay 正则性主张。NOT CLAY。", "LITERATURE CONDITIONAL: the Albritton--Barker fixed-ball result and the typographical interpretation above. PROVED LOCALLY: the original prescribed-path drift bound at fixed R; solution-dependent stepwise slow diagonal radii for every α<2/5; compatibility of L_t^4L_x^3 with endpoint divergence; curl/moment exclusion of the exact-energy logical model from NS; a genuine smooth unforced viscosity-one periodic NS family that rejects AA.1-type L³ persistence on every smooth window without initial or exterior cost; and a bare far-source pressure impulse for a fixed solution and ball bounded by C c₀M²r⁻¹L⁻⁵. FINITE COMPUTATION: none. STRICT LIMITS: the slow radius is not a prescribed power law or one differentiable variable-scale path; the non-NS model is not an NS counterexample; the true NS family has growing initial energy and t_B/r²→0 and does not refute mature-time or first-singularity-only versions; AA.18 is not velocity-weighted pressure work. OPEN: near-source pressure, nonlinear transport, viscous change, quantitative shrinking, the original path cylinder, G/G-P/G-C, R.216–R.217, and the earlier U/V/W/Y gaps. There is no figure, simulation, numerical certificate, novelty, priority, publication-level, or Clay regularity claim. NOT CLAY."],
  ["Tao 的局部适定性讲义", "Tao's local well-posedness notes"],
  ["研究笔记总索引 · v2.49 · 2026-09-06", "Research-note master index · v2.49 · 2026-09-06"],
  ["本节：固定球集中之后", "This note: after fixed-ball concentration"],
  ["策略调整后的 Clay-B 分支 · 2026-09-06 · L/P/D/I/M/N/AA 合并", "Clay-B branch after the strategy change · 2026-09-06 · combined L/P/D/I/M/N/AA"],
  ["从固定球集中到局部持留的准确缺口", "From fixed-ball concentration to the exact local-persistence gap"],
  ["固定 R 原路径 / 解依赖半径：已证", "Fixed-R original path / solution-dependent radii: proved"],
  ["固定球集中、原路径与持留成本已进入下一节点", "Fixed-ball concentration, original paths, and persistence costs now form the next node"],
  ["固定球集中之后，还缺少什么", "What remains after fixed-ball concentration"],
  ["固定球文献输入可转移到固定尺度原路径，并给出解依赖的慢缩对角半径；它不是预设幂律或单一变尺度路径。精确能量反模型不是 NS，真正的平滑周期 NS 族只否定无初值/外部成本的全光滑窗口持留，且 t_B/r²→0。AA.18 只支付裸远源压力冲量；近源压力、黏性、成熟时间与首次奇点版仍 OPEN。NOT CLAY.", "The fixed-ball literature input transfers to the original path at fixed scale and gives a solution-dependent slowly shrinking diagonal radius; it is not a prescribed power law or one variable-scale path. The exact-energy countermodel is not NS. A genuine smooth periodic NS family rejects only all-smooth-window persistence without initial or exterior cost, and t_B/r²→0. AA.18 pays only the bare far-source pressure impulse; near pressure, viscosity, mature time, and the first-singularity version remain OPEN. NOT CLAY."],
  ["固定一个有限能量解、固定球与正成熟时间，分离近源压力、非线性输运和黏性变化，并核查它们与原路径柱、G/G-P/G-C 及 R.216–R.217 的接口。该后续问题尚未冻结或发布。", "Fix one finite-energy solution, one ball, and a positive mature time; separate near-source pressure, nonlinear transport, and viscous change, then audit their interfaces with the original path cylinder, G/G-P/G-C, and R.216–R.217. This later question is neither frozen nor published."],
  ["近源、黏性与首次奇点持留：OPEN · NOT CLAY", "Near field, viscosity, and first-singularity persistence: OPEN · NOT CLAY"],
  ["精确能量逻辑模型由 curl/moment 严格排除在 NS 之外。真正平滑无外力周期 NS 族否定不支付初值或外部压力成本的所有光滑窗口 L³ 持留，但其初始能量增长且 t_B/r²→0，不触及成熟时间或首次奇点限定版。固定解的远源压力裸冲量是 O(c₀M²r⁻¹L⁻⁵)；它不是速度加权压力功。", "The exact-energy logical model is rigorously excluded from NS by curl and moment. A genuine smooth unforced periodic NS family rejects L³ persistence on every smooth window without initial-data or exterior-pressure cost, but its initial energy grows and t_B/r²→0, so it does not reach mature-time or first-singularity-only versions. For a fixed solution, the bare far-source pressure impulse is O(c₀M²r⁻¹L⁻⁵); it is not velocity-weighted pressure work."],
  ["两条公开路线都停在各自已冻结边界", "Both public routes stop at their respective frozen boundaries"],
  ["平台历史 X/Y → 固定球文献输入 L → 固定 R 原路径 P → 解依赖慢对角半径 D → 时间可积性限制 I → 精确能量非 NS 模型 M/N → 真实 NS 无成本全窗口障碍 AA.1–AA.15 → 裸远源压力冲量 AA.16–AA.18 → 近源压力与黏性 OPEN", "Plateau history X/Y → fixed-ball literature input L → fixed-R original path P → solution-dependent slow diagonal radius D → time-integrability limit I → exact-energy non-NS model M/N → genuine-NS cost-free all-window obstruction AA.1–AA.15 → bare far-source pressure impulse AA.16–AA.18 → near pressure and viscosity OPEN"],
  ["前一节：平台能量历史", "Previous note: plateau energy history"],
  ["首次奇点文献适用性、固定尺度原路径、解依赖慢缩半径、无成本持留障碍和远源压力冲量已经逐项区分；结果见下一个正式路线节点。", "First-singularity literature applicability, the fixed-scale original path, solution-dependent slowly shrinking radii, the cost-free persistence obstruction, and the far-source pressure impulse have now been distinguished item by item. The result appears in the next formal route node."],
  ["无成本全窗口持留：已被真实 NS 族否定", "Cost-free all-window persistence: rejected by a genuine NS family"],
  ["下一研发问题：成熟时间下的局部 L³ 变化预算", "Next research question: a local L³ change budget at mature time"],
  ["阅读最新集中边界笔记 →", "Read the latest concentration-limits note →"],
  ["综述 v2.49 · 2026-09-06", "Review v2.49 · 2026-09-06"],
  ["Albritton–Barker 的固定球输入以 Definition 2.1 的显式排字解释作为 LITERATURE CONDITIONAL 使用。对每个固定 R，集中可进入原指定路径；对任意 α<2/5，只能构造依赖具体解的阶梯式慢缩半径，不是预设幂律、可微变尺度路径或完整路径柱。", "The Albritton–Barker fixed-ball input is used as LITERATURE CONDITIONAL with an explicit interpretation of the Definition 2.1 typography. At each fixed R, concentration enters the original prescribed path. For every α<2/5, one can construct only a solution-dependent stepwise slowly shrinking radius, not a prescribed power law, a differentiable variable-scale path, or a full path cylinder."],
  ["Clay-B 的固定球集中可进入固定尺度原路径，也可经对角化得到解依赖慢缩半径，但这不是预设幂律或单一变尺度路径。真正的平滑 NS 族排除了不支付初值或远场成本的全窗口持留；固定解的远源压力冲量可支付，近源压力、黏性、成熟时间与首次奇点接口仍开放。", "Clay-B fixed-ball concentration enters the original path at fixed scale and, by diagonalization, gives solution-dependent slowly shrinking radii, but not a prescribed power law or one variable-scale path. A genuine smooth NS family eliminates all-window persistence without initial or far-field cost. The far-source pressure impulse for a fixed solution can be paid, while near pressure, viscosity, mature time, and the first-singularity interface remain open."],
  ["Clay-B 集中边界笔记快捷入口", "Clay-B concentration-limits note shortcuts"],
  ["Clay-B 集中边界结论", "Clay-B concentration-limits result boundary"],
  ["R0 主序列仍停在 R0.76L：m≈κA⁴ bulk saddle、m≈A² 转换区、arbitrary packets、Version-M、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。Clay-B 独立路线停在本次集中边界：成熟时间持留、近源压力、黏性、非线性输运、定量缩球、原路径柱及 G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。", "The R0 main sequence remains at R0.76L: the m≈κA⁴ bulk saddle, the m≈A² transition, arbitrary packets, Version-M, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. The independent Clay-B route stops at this concentration boundary: mature-time persistence, near pressure, viscosity, nonlinear transport, quantitative shrinking, the original path cylinder, and G/G-P/G-C are not frozen. Later research is not presented as proved."],
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
  assert.equal(rows.length, translations.size, "ConcentrationLimits translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("What remains after fixed-ball concentration"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "ConcentrationLimits source-string count drift");
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

process.stdout.write(JSON.stringify({ release: "ClayB-ConcentrationLimits-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");

