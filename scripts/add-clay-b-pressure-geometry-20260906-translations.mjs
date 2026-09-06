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
const prefix = "claybpressuregeometry20260906";

const translations = new Map([
  ["承担全空间 Leray–Hopf 类中附加方向可积性正则准则及其中间加权结构的文献背景；本站已核对全文六页，但不把全空间量词直接移植到周期域，也不把方向重写声明为新发现。", "supplies the literature background for the additional direction-integrability regularity criterion and its intermediate weighted structure in the whole-space Leray–Hopf class. This site checked all six pages, but does not transfer the whole-space quantifiers literally to the torus or claim the direction reformulation as new."],
  ["文献综述 v2.51 · 2026-09-06", "Literature review v2.51 · 2026-09-06"],
  ["阅读完整 CB.7 笔记", "Read the complete CB.7 note"],
  ["只承担周期次临界局部理论与 H¹ 重启范围背景。", "is used only as background for periodic subcritical local theory and the scope of H¹ restart."],
  ["CB.7 · Clay-B 压力功、速度方向与临界条件的文献和主张边界", "CB.7 · Literature and claim boundary for Clay-B pressure work, velocity direction, and the critical condition"],
  ["CB.7 · ClayB-PressureGeometry-20260906 公开边界", "CB.7 · Public boundary for ClayB-PressureGeometry-20260906"],
  ["PROVED LOCALLY：零速度正则化后的完整带符号局部 L³ 恒等式；固定同一解、固定 M/r 时带权远源压力功相对界 Cc₀M⁴r⁻²L⁻⁷；零集安全的 D=2D_r+D_θ、F=q div e=−e·∇q、W=−∫pqF 及 Z_e≤2D/5；显式零均值有限模态周期初值的压力功严格正负号；有限幅值放大后的真实黏性一 NS 瞬时及短时 L³ 增长。LITERATURE / CONDITIONAL：Vasseur 全空间方向准则为已知文献；周期 F∈L²_tL³_x 条件可推出 L³_tL⁹_x、H¹ 重启与越过有限 T 的延拓，但该条件没有由能量给出。STRICT LIMITS：远源小量固定 M/r，不支付近源、输运或外壳；短时符号例放大初值能量，不触及成熟时间或固定解首次奇点；周期 Taylor–Green 零线只给固定角锥 1/r 下界，不判定 Vasseur 全空间原类中的必要性。FINITE COMPUTATION：无。OPEN：F 的真实演化控制、近源压力、输运、黏性、外壳、缩球、原移动路径、G/G-P/G-C、R.216–R.217 与此前 U/V/W/Y 缺口。没有图件、仿真、数值证书、新颖性、优先权、发表等级或 Clay 正则性主张。NOT CLAY。", "PROVED LOCALLY: the complete signed local L³ identity after zero-speed regularization; at fixed M/r for the same solution, the relative weighted far-source pressure-work bound Cc₀M⁴r⁻²L⁻⁷; the zero-set-safe identities D=2D_r+D_θ, F=q div e=−e·∇q, W=−∫pqF, and Z_e≤2D/5; strictly positive and negative pressure work for explicit zero-mean finite-mode periodic data; and instantaneous and short-time L³ growth for genuine viscosity-one NS after finite-amplitude scaling. LITERATURE / CONDITIONAL: Vasseur's whole-space direction criterion is known literature; the periodic condition F∈L²_tL³_x yields L³_tL⁹_x, H¹ restart, and continuation beyond finite T, but energy does not supply this condition. STRICT LIMITS: the far-source smallness fixes M/r and does not pay for the near field, transport, or outer shell; the short-time sign example scales up the initial energy and does not reach mature time or a first singularity of one fixed solution; the periodic Taylor–Green zero line gives a 1/r lower bound only in a fixed angular cone and does not decide necessity in Vasseur's original whole-space class. FINITE COMPUTATION: none. OPEN: genuine evolution control of F, near pressure, transport, viscosity, the outer shell, shrinking balls, the original moving path, G/G-P/G-C, R.216–R.217, and the earlier U/V/W/Y gaps. There is no figure, simulation, numerical certificate, novelty, priority, publication-level, or Clay regularity claim. NOT CLAY."],
  ["压力功的符号、速度方向与临界条件", "Pressure-work signs, velocity direction, and the critical condition"],
  ["研究笔记总索引 · v2.51 · 2026-09-06", "Research-note master index · v2.51 · 2026-09-06"],
  ["CB.1–CB.7 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.7 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["固定 M、r 的带权远源压力功相对终点 L³ 能量按 L⁻⁷ 衰减；方向分解给出零集安全的条件接口，但能量只到 F∈L²_tL²_x，没有给出所需的 L²_tL³_x。显式有限模态初值使压力功取正负两种符号，并可产生放大初值能量后的短时真实 NS L³ 增长。近源、外壳、F 的真实演化与合同 G 仍 OPEN。NOT CLAY.", "For fixed M and r, weighted far-source pressure work decays relative to terminal L³ energy as L⁻⁷. The direction decomposition gives a zero-set-safe conditional interface, but energy reaches only F∈L²_tL²_x, not the required L²_tL³_x. Explicit finite-mode data make pressure work take either sign and can produce short-time genuine NS L³ growth after scaling the initial energy. The near field, outer shell, genuine evolution of F, and contract G remain OPEN. NOT CLAY."],
  ["固定 M/r 的带权远源功、零集安全方向分解、条件 F 接口与压力功正负号已经分开；结果见下一个正式路线节点。", "The fixed-M/r weighted far-source work, zero-set-safe direction decomposition, conditional F interface, and both signs of pressure work have now been separated; the result appears in the next formal route node."],
  ["固定 M/r 远源压力功：已支付", "Fixed-M/r far-source pressure work: paid"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.7 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.7 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：F 的真实演化是否产生可支付控制", "Next research question: whether the genuine evolution of F yields payable control"],
  ["压力功几何与方向接口已进入 CB.7", "Pressure-work geometry and the direction interface now form CB.7"],
  ["压力功无普适符号；F 演化 OPEN · NOT CLAY", "Pressure work has no universal sign; F evolution OPEN · NOT CLAY"],
  ["阅读最新 CB.7 压力几何笔记 →", "Read the latest CB.7 pressure-geometry note →"],
  ["在 q>0 上推导 F=−eᵀ(∇u)e 的完整物质热演化，逐项保留压力 Hessian、方向导数、高阶项与速度 cutoff；只有能由同一解能量和已知耗散支付的新结构才算推进。该问题尚未冻结。", "Derive the complete material heat evolution of F=−eᵀ(∇u)e on q>0, retaining the pressure Hessian, directional derivatives, higher-order terms, and velocity cutoff term by term. Only new structure paid by the same solution's energy and known dissipation counts as progress. This question is not yet frozen."],
  ["综述 v2.51 · 2026-09-06", "Review v2.51 · 2026-09-06"],
  ["AB 给出完整带符号局部 L³ 预算，并在固定 M、r 下支付带速度权重的远源压力功；标准全环面链条仍留下不可吸收的大 L 系数。AC 以零集安全的 F=q div e 分解方向耗散，并证明 F∈L²_tL³_x 的条件延拓接口，但能量只给 L²_tL²_x。", "AB gives the complete signed local L³ budget and pays the velocity-weighted far-source pressure work at fixed M and r; the standard full-torus chain still leaves a large non-absorbable coefficient in L. AC decomposes directional dissipation with the zero-set-safe F=q div e and proves the conditional F∈L²_tL³_x continuation interface, while energy gives only L²_tL²_x."],
  ["AD 的显式有限模态周期初值使压力功严格取正负两种符号；有限幅值放大可产生真实 NS 的瞬时和短时 L³ 增长，同时放大初值能量。周期 Taylor–Green 零线只说明同型未加权方向条件不是周期光滑性的必要条件，不判定 Vasseur 全空间原类中的必要性。", "AD's explicit finite-mode periodic data make pressure work strictly positive or negative. Finite-amplitude scaling can produce instantaneous and short-time L³ growth for genuine NS while also scaling up the initial energy. The periodic Taylor–Green zero line shows only that the analogous unweighted direction condition is not necessary for periodic smoothness; it does not decide necessity in Vasseur's original whole-space class."],
  ["CB.1–CB.7 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.7 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.6 集中与持留缺口 → AB 带符号 L³ 预算 → 固定 M/r 远源压力功 → AC 零集安全方向分解 → 条件 F∈L²_tL³_x 延拓 → AD 压力功正负号 → F 真实演化 OPEN", "CB.6 concentration and persistence gap → AB signed L³ budget → fixed-M/r far-source pressure work → AC zero-set-safe direction decomposition → conditional F∈L²_tL³_x continuation → AD positive and negative pressure-work signs → genuine F evolution OPEN"],
  ["CB.6：集中与持留边界", "CB.6: concentration and persistence boundary"],
  ["CB.7：压力功与方向几何", "CB.7: pressure work and direction geometry"],
  ["CB.7｜从带权远源压力功到方向临界缺口", "CB.7 | From weighted far-source pressure work to the critical direction gap"],
  ["CB.7｜压力功的符号、速度方向与临界条件", "CB.7 | Pressure-work signs, velocity direction, and the critical condition"],
  ["CB.8 只是下一章占位，不是已完成研究。F 的真实演化控制、近源压力、黏性、输运与外壳、缩球及原移动路径、G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。", "CB.8 is only a placeholder for the next chapter, not completed research. Genuine evolution control of F, near pressure, viscosity, transport and the outer shell, shrinking balls and the original moving path, and G/G-P/G-C are not frozen; later research is not presented as proved."],
  ["Clay-B 的固定 M/r 带权远源压力功已经支付；零集安全的方向分解给出 F∈L²_tL³_x 条件延拓接口，但能量只到 L²_tL²_x。显式周期初值证明压力功没有普适耗散符号；近源、外壳、F 的真实演化与合同 G 仍开放。", "Clay-B's fixed-M/r weighted far-source pressure work has been paid. The zero-set-safe direction decomposition gives a conditional F∈L²_tL³_x continuation interface, but energy reaches only L²_tL²_x. Explicit periodic data prove that pressure work has no universal dissipative sign; the near field, outer shell, genuine evolution of F, and contract G remain open."],
  ["Clay-B 独立路线停在 CB.7", "The independent Clay-B route stops at CB.7"],
  ["Clay-B 压力几何笔记快捷入口", "Clay-B pressure-geometry note shortcuts"],
  ["Clay-B 压力几何结论", "Clay-B pressure-geometry result boundary"],
  ["F 的 L²_tL³_x 控制：条件性", "F control in L²_tL³_x: conditional"],
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
  assert.equal(rows.length, translations.size, "PressureGeometry translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.7"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "PressureGeometry source-string count drift");
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
  release: "ClayB-PressureGeometry-20260906",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: translations.size,
  applied: !checkOnly,
}, null, 2) + "\n");
