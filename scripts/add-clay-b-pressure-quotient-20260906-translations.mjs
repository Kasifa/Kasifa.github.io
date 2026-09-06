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
const prefix = "claybpressurequotient20260906";

const translations = new Map([
  ["给出相关的压力—速度混合积分条件准则；本站不把其定性模型讨论作为一般正则性输入。", "gives related conditional criteria using mixed pressure–velocity integrals. This site does not use its qualitative model discussion as a general regularity input."],
  ["文献综述 v2.52 · 2026-09-06", "Literature review v2.52 · 2026-09-06"],
  ["已经包含全空间光滑衰减设置中的 pressure moderator；取空间常量系数便包含速率函数抵消的光滑版本，所以该核心抵消不是本站的新发现。", "already contains the pressure moderator in a smooth decaying whole-space setting. Taking a spatially constant coefficient includes the smooth version of the speed-function cancellation, so this core cancellation is not a new discovery of this site."],
  ["阅读完整 CB.8 笔记", "Read the complete CB.8 note"],
  ["CB.8 · Clay-B 压力投影、残差准则与固定能量反检查的文献和主张边界", "CB.8 · Literature and claim boundary for Clay-B pressure projection, the residual criterion, and the fixed-energy stress test"],
  ["CB.8 · ClayB-PressureQuotient-20260906 公开边界", "CB.8 · Public boundary for ClayB-PressureQuotient-20260906"],
  ["PROVED LOCALLY：AE 在 q>0 上的 q、e、A、F 完整演化与两个代数形式，当前估计未闭合且不是加权方法 no-go；AF 对有界 Borel 速率函数的 ∫qΦ(q)F=0、L²(q dx) 条件期望投影、平台/零集/时间可测性和最小残差 R；AG 的准确 cutoff 外壳、Bernoulli 输运重组及整组而非单个非分隔等值面分量的零通量；AH 对每个固定 E₀ 构造光滑零均值周期无散初值，使 (R²/H)/(1+||∇u||²) 无界。LITERATURE / CONDITIONAL：核心 speed-only moderator 抵消已有文献；∫R²/H dt 有限可推出周期 L³_tL⁹_x、H¹ 重启和延拓，但该额外条件没有由能量给出。STRICT LIMITS：AH 只否定 R²≤C(E₀)H(1+||∇u||²) 这一具体瞬时候选界；大残差来自 F=0 平台，不能推出 W 很大、固定轨道时间积分失败、成熟时间或首次奇点反例；Bernoulli 只重组输运，局部投影保留外壳。FINITE COMPUTATION：无。OPEN：真实有符号压力功的能量已付时空控制、近源、外壳、成熟时间、固定解首次奇点、缩球、原路径和 G/G-P/G-C。没有图件、仿真、数值证书、新颖性、优先权、发表等级或 Clay 正则性主张；独立论文 v2 私有包不在本次发布。NOT CLAY。", "PROVED LOCALLY: AE gives the complete q, e, A, and F evolution on q>0 in two algebraic forms; the current estimate does not close and is not a no-go for weighted methods. AF gives ∫qΦ(q)F=0 for bounded Borel speed functions, conditional-expectation projection in L²(q dx), treatment of plateaus, zero sets, and time measurability, and the minimum residual R. AG gives the exact cutoff shell, Bernoulli transport recombination, and zero flux for the full collection rather than each individual nonseparating level-set component. For every fixed E₀, AH constructs smooth zero-mean periodic divergence-free data for which (R²/H)/(1+||∇u||²) is unbounded. LITERATURE / CONDITIONAL: the core speed-only moderator cancellation has prior literature; finite ∫R²/H dt yields periodic L³_tL⁹_x, H¹ restart, and continuation, but energy does not give this extra condition. STRICT LIMITS: AH rejects only the specific instantaneous candidate bound R²≤C(E₀)H(1+||∇u||²). The large residual comes from an F=0 plateau and does not imply large W, failure of a fixed-trajectory time integral, or a mature-time or first-singularity counterexample. Bernoulli only recombines transport, and local projection retains the shell. FINITE COMPUTATION: none. OPEN: energy-paid spacetime control of genuine signed pressure work, the near field, outer shell, mature time, a first singularity of one fixed solution, shrinking balls, original paths, and G/G-P/G-C. There is no figure, simulation, numerical certificate, novelty, priority, publication-level, or Clay regularity claim. The private independent-paper v2 package is outside this release. NOT CLAY."],
  ["压力投影：抵消成立，一个特定瞬时残差预算失败", "Pressure projection: the cancellation holds, and one specific instantaneous residual budget fails"],
  ["研究笔记总索引 · v2.52 · 2026-09-06", "Research-note master index · v2.52 · 2026-09-06"],
  ["CB.1–CB.8 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.8 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["∫R²/H dt 延拓：条件性", "Continuation from ∫R²/H dt: conditional"],
  ["从 H′+D=−∫pqF 出发，把能量已付部分和真正正增长区分开；新估计必须排除 F=0 平台的虚假成本，并实际支付近源与外壳，不能只添加另一条临界相关性假设。该问题尚未冻结。", "Start from H′+D=−∫pqF and separate the energy-paid part from genuine positive growth. A new estimate must exclude the false cost of F=0 plateaus and actually pay the near field and outer shell; merely adding another critical correlation hypothesis is not enough. This question is not yet frozen."],
  ["核心抵消、条件残差准则、局部外壳与固定能量瞬时反检查已经区分；结果见下一个正式路线节点。", "The core cancellation, conditional residual criterion, local shell, and fixed-energy instantaneous stress test have now been separated; the result appears in the next formal route node."],
  ["速率函数压力对全域压力功精确不可见，最佳 L²(q dx) 残差给出条件延拓接口；但固定能量单泡使一条特定瞬时 R²/H 候选界失败。大残差来自 F=0 常速平台，不能读成压力功大、时间积分失败、成熟时间或首次奇点反例。近源、外壳与合同 G 仍 OPEN。NOT CLAY.", "Speed-function pressure is exactly invisible to global pressure work, and the best L²(q dx) residual gives a conditional continuation interface. But a fixed-energy single bubble defeats one specific instantaneous R²/H candidate bound. The large residual comes from an F=0 constant-speed plateau and cannot be read as large pressure work, failure of a time integral, or a mature-time or first-singularity counterexample. The near field, outer shell, and contract G remain OPEN. NOT CLAY."],
  ["速率投影抵消：已证且有文献前例", "Speed-projection cancellation: proved with prior literature"],
  ["速率投影与残差候选已进入 CB.8", "Speed projection and the residual candidate now form CB.8"],
  ["特定瞬时界失败；真实压力功预算 OPEN · NOT CLAY", "Specific instantaneous bound fails; genuine pressure-work budget OPEN · NOT CLAY"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.8 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.8 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：真实压力功的带符号方向配对", "Next research question: signed direction pairing for genuine pressure work"],
  ["阅读最新 CB.8 压力投影笔记 →", "Read the latest CB.8 pressure-projection note →"],
  ["综述 v2.52 · 2026-09-06", "Review v2.52 · 2026-09-06"],
  ["AE 完整写出 F 的真实演化，但压力 Hessian、方向弯曲与二阶速度导数仍未支付。AF 用零集安全的 Borel 原函数证明 ∫qΦ(q)F=0，并在 L²(q dx) 中定义最佳压力残差 R；∫R²/H dt 有限可条件性推出 L³_tL⁹_x 与 H¹ 重启，但能量没有给出该积分。", "AE writes the genuine evolution of F in full, but the pressure Hessian, direction curvature, and second velocity derivatives remain unpaid. AF proves ∫qΦ(q)F=0 with a zero-set-safe Borel primitive and defines the best pressure residual R in L²(q dx). Finite ∫R²/H dt conditionally yields L³_tL⁹_x and H¹ restart, but energy does not provide this integral."],
  ["AH 的固定总能量单泡令特定瞬时 R²≤C(E₀)H(1+||∇u||²) 候选界失败；下界位于 F=0 常速平台，所以不代表压力功大或轨道时间积分失败。AG 显示局部投影保留外壳，Bernoulli 只重组输运。moderator 核心抵消已有文献前例，不作新颖性声明。", "AH's fixed-total-energy single bubble defeats the specific instantaneous candidate bound R²≤C(E₀)H(1+||∇u||²). The lower bound lies on an F=0 constant-speed plateau, so it does not represent large pressure work or failure of a trajectory time integral. AG shows that local projection retains the shell and Bernoulli only recombines transport. The core moderator cancellation has prior literature, and no novelty is claimed."],
  ["CB.1–CB.8 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.8 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.7 压力几何 → AE 真实 F 演化未闭合 → AF 速率投影与条件延拓 → AH 固定能量瞬时残差界失败但 W 不大 → AG 外壳与 Bernoulli 重组 → 真实有符号压力功配对 OPEN", "CB.7 pressure geometry → AE genuine F evolution unclosed → AF speed projection and conditional continuation → AH fixed-energy instantaneous residual bound fails but W is not large → AG shell and Bernoulli recombination → genuine signed pressure-work pairing OPEN"],
  ["CB.8：压力投影与瞬时反检查", "CB.8: pressure projection and instantaneous stress test"],
  ["CB.8｜速率投影抵消、条件残差准则与固定能量反检查", "CB.8 | Speed-projection cancellation, conditional residual criterion, and fixed-energy stress test"],
  ["CB.8｜压力投影：抵消成立，一个特定瞬时残差预算失败", "CB.8 | Pressure projection: the cancellation holds, and one specific instantaneous residual budget fails"],
  ["CB.9 只是下一章占位，不是已完成研究。真实有符号压力功的能量已付时空控制、近源、外壳、成熟时间、固定解首次奇点、缩球、原移动路径及 G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。", "CB.9 is only a placeholder for the next chapter, not completed research. Energy-paid spacetime control of genuine signed pressure work, the near field, outer shell, mature time, a first singularity of one fixed solution, shrinking balls, the original moving path, and G/G-P/G-C are not frozen; later research is not presented as proved."],
  ["Clay-B 的速率函数压力对全域压力功精确不可见；最佳加权残差的时间积分给出条件延拓接口，但未由能量支付。固定能量单泡排除一条特定瞬时残差候选界，同时揭示 F=0 平台可产生大残差而不做压力功；近源、外壳与合同 G 仍开放。", "Clay-B speed-function pressure is exactly invisible to global pressure work. The time integral of the best weighted residual gives a conditional continuation interface but is not paid by energy. A fixed-energy single bubble excludes one specific instantaneous residual candidate bound while showing that an F=0 plateau can produce a large residual without doing pressure work. The near field, outer shell, and contract G remain open."],
  ["Clay-B 独立路线停在 CB.8", "The independent Clay-B route stops at CB.8"],
  ["Clay-B 压力投影笔记快捷入口", "Clay-B pressure-projection note shortcuts"],
  ["Clay-B 压力投影结论", "Clay-B pressure-projection result boundary"],
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
  assert.equal(rows.length, translations.size, "PressureQuotient translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.8"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "PressureQuotient source-string count drift");
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

process.stdout.write(JSON.stringify({
  release: "ClayB-PressureQuotient-20260906",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: translations.size,
  applied: !checkOnly,
}, null, 2) + "\n");
