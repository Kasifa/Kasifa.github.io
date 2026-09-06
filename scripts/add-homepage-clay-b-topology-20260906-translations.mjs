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
const prefix = "homepageclaybtopology20260906";

const translations = new Map([
  ["文献综述 v2.50 · 2026-09-06", "Literature review v2.50 · 2026-09-06"],
  ["CB.1 · Clay-B 两尺度差能量的 filtering 文献与主张边界", "CB.1 · Literature and claim boundary for Clay-B two-scale difference energy and filtering"],
  ["CB.1 · ClayB-TwoScale-20260905 公开边界", "CB.1 · Public boundary for ClayB-TwoScale-20260905"],
  ["CB.2 · Clay-B 有符号尺度预算的 filtering 文献与主张边界", "CB.2 · Literature and claim boundary for Clay-B signed-scale budgets and filtering"],
  ["CB.2 · ClayB-SignedScale-20260905 公开边界", "CB.2 · Public boundary for ClayB-SignedScale-20260905"],
  ["CB.3 · Clay-B 物理时间伴随测试的文献与主张边界", "CB.3 · Literature and claim boundary for the Clay-B physical-time adjoint test"],
  ["CB.3 · ClayB-PhysicalAdjoint-20260906 公开边界", "CB.3 · Public boundary for ClayB-PhysicalAdjoint-20260906"],
  ["CB.4 · Clay-B 短窗口局部耗散的文献与主张边界", "CB.4 · Literature and claim boundary for Clay-B short-window local dissipation"],
  ["CB.4 · ClayB-WindowLocalisation-20260906 公开边界", "CB.4 · Public boundary for ClayB-WindowLocalisation-20260906"],
  ["CB.5 · Clay-B 平台时间能量历史的文献与主张边界", "CB.5 · Literature and claim boundary for Clay-B plateau-time energy history"],
  ["CB.5 · ClayB-PlateauHistory-20260906 公开边界", "CB.5 · Public boundary for ClayB-PlateauHistory-20260906"],
  ["CB.6 · Clay-B 固定球集中、原路径与持留成本的文献和主张边界", "CB.6 · Literature and claim boundary for Clay-B fixed-ball concentration, original paths, and persistence costs"],
  ["CB.6 · ClayB-ConcentrationLimits-20260906 公开边界", "CB.6 · Public boundary for ClayB-ConcentrationLimits-20260906"],
  ["章节：CB.1 · 标识：ClayB-TwoScale-20260905", "Chapter: CB.1 · identifier: ClayB-TwoScale-20260905"],
  ["这份独立笔记采用 Clay-B 内部章节号 CB.1；它不占用 R0 主序列编号，不是正则性证明，也不声称新颖性或优先权。指定中心合同 G 仍 OPEN。NOT CLAY.", "This independent note uses the internal Clay-B chapter number CB.1. It does not occupy an R0-series number, is not a regularity proof, and makes no novelty or priority claim. Prescribed-centre contract G remains OPEN. NOT CLAY."],
  ["CB.1 · Clay-B 独立桥梁笔记 · 2026-09-05", "CB.1 · Independent Clay-B bridge note · 2026-09-05"],
  ["研究笔记总索引 · v2.50 · 2026-09-06", "Research-note master index · v2.50 · 2026-09-06"],
  ["CB.1–CB.6 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.6 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["独立路线起点", "Independent-lane starting point"],
  ["独立路线章节", "Independent-lane chapter"],
  ["对同一真实 Navier–Stokes 解的两个滤波尺度相减，保留移动截止、时间截止、应力差与压力功。全时光滑检验族排除无额外支付的统一瞬时吸收；固定正尺度上得到由局部二次量、三次量和压力 3/2 次量支付的闭时间端点估计。", "Subtracting two filter scales of the same genuine Navier–Stokes solution retains the moving cutoff, time cutoff, stress difference, and pressure work. An all-time smooth test family rules out uniform instantaneous absorption without extra payment; at a fixed positive scale, the closed-time endpoint estimate is paid by local quadratic and cubic quantities and the pressure 3/2 quantity."],
  ["两尺度差场 → 完整移动截止差能量恒等式 → 统一瞬时吸收障碍 → 固定正尺度完整支付 E.5", "Two-scale difference field → complete moving-cutoff difference-energy identity → uniform instantaneous-absorption obstruction → fixed-positive-scale complete payment E.5"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.6 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.6 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一章保留完整时空失配，并检查零失配热对偶与真实收缩定位能否相容。", "The next chapter retains the full space-time mismatch and checks whether a zero-mismatch heat dual can coexist with genuine shrinking localization."],
  ["虚线：Clay-B 内部章节顺序，不表示由 R0 主序列推出", "Dashed line: internal Clay-B chapter order, not an implication from the R0 main sequence"],
  ["移动尺度、局部化与集中边界", "Moving scales, localization, and concentration boundaries"],
  ["有符号尺度预算已进入 CB.2", "The signed-scale budget continues in CB.2"],
  ["阅读 CB.1：两尺度完整支付", "Read CB.1: complete two-scale payment"],
  ["阅读最新 CB.6 集中边界笔记 →", "Read the latest CB.6 concentration-limits note →"],
  ["这条路线与 R0 主序列共享三维 Navier–Stokes 的研究目标，但不声明由 R0.76L 直接推出。虚线只连接 Clay-B 内部已经发布的章节顺序。", "This route shares the three-dimensional Navier–Stokes research objective with the R0 main sequence, but it is not claimed to follow directly from R0.76L. The dashed line connects only the published chapter order within Clay-B."],
  ["综述 v2.50 · 2026-09-06", "Review v2.50 · 2026-09-06"],
  ["CB.1 保留固定尺度完整支付；本章进一步闭合有符号时空预算和 S.8–S.15 失配台账，并证明指定非负热对偶若强制零失配，就不能同时保持真实收缩定位。", "CB.1 retains the complete fixed-scale payment. This chapter closes the signed space-time budget and the S.8–S.15 mismatch ledger, and proves that a prescribed nonnegative heat dual forced to have zero mismatch cannot also retain genuine shrinking localization."],
  ["CB.1 两尺度完整支付 → 嵌套热滤波带能量 → 完整时空失配 → 零失配定位障碍 → 统一 L² 真 NS 光滑族排除普适转移", "CB.1 complete two-scale payment → nested heat-filtered band energy → complete space-time mismatch → zero-mismatch localization obstruction → uniformly L²-bounded genuine smooth NS family excludes universal transfer"],
  ["CB.1–CB.6 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.6 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.1：两尺度完整支付", "CB.1: complete two-scale payment"],
  ["CB.1｜两尺度差能量：瞬时吸收的限制与完整支付", "CB.1 | Two-scale difference energy: limits of instantaneous absorption and complete payment"],
  ["CB.2 有符号尺度相消 → 放弃零失配热对偶 → 真实时间伴随弱端点 → 线性耗散矩界 → 质量尾界但非原移动管能量 → 原计时合同持留/上穿输入", "CB.2 signed-scale cancellation → abandon the zero-mismatch heat dual → physical-time adjoint weak endpoint → linear dissipative moment bound → mass-tail bound but not original moving-tube energy → persistence/upcrossing input for the original clock contract"],
  ["CB.2：有符号尺度相消", "CB.2: signed-scale cancellation"],
  ["CB.2｜从两尺度完整支付到有符号尺度相消", "CB.2 | From complete two-scale payment to signed-scale cancellation"],
  ["CB.3 物理时间伴随 → 正变差持留窗口 U → 固定尺度 L_t^(4/3) 与四次宽度 V → 局部/调和压力分解 W → 联合余项工作或带 cutoff 扣除的耗散分支 → doubled-radius 耗散债务 → 首次奇点量词复评", "CB.3 physical-time adjoint → positive-variation persistence window U → fixed-scale L_t^(4/3) control and quartic width V → local/harmonic pressure split W → joint-remainder work or dissipation branch with cutoff deduction → doubled-radius dissipation debt → reassessment of first-singularity quantifiers"],
  ["CB.3：伴随测试定位代价", "CB.3: localization cost of the adjoint test"],
  ["CB.3｜从零失配定位障碍到真实物理时间伴随预算", "CB.3 | From the zero-mismatch localization obstruction to the physical-time adjoint budget"],
  ["CB.4 窗口局部化 W → H 平台终点 / Q-R 全时间量词区分 X → 跨平台阈值窗与等号 Y.1–Y.2 → total dissipation + 负工作历史 Y.3–Y.8 → 条件耗散 Y.9 → doubled-radius 绝对账本 Y.10–Y.12 → A+P 非 A+Z → 首次奇点文献适用性核查", "CB.4 window localization W → distinction X between H plateau endpoints and Q-R all-time quantifiers → cross-plateau threshold windows and equality case Y.1–Y.2 → total dissipation plus negative-work history Y.3–Y.8 → conditional dissipation Y.9 → doubled-radius absolute ledger Y.10–Y.12 → A+P, not A+Z → first-singularity literature applicability audit"],
  ["CB.4：短窗口局部耗散", "CB.4: short-window local dissipation"],
  ["CB.4｜从正变差窗口到扩大域耗散债务", "CB.4 | From positive-variation windows to expanded-domain dissipation debt"],
  ["CB.5 平台历史 X/Y → 固定球文献输入 L → 固定 R 原路径 P → 解依赖慢对角半径 D → 时间可积性限制 I → 精确能量非 NS 模型 M/N → 真实 NS 无成本全窗口障碍 AA.1–AA.15 → 裸远源压力冲量 AA.16–AA.18 → 近源压力与黏性 OPEN", "CB.5 plateau history X/Y → fixed-ball literature input L → fixed-R original path P → solution-dependent slow diagonal radius D → time-integrability limit I → exact-energy non-NS model M/N → genuine-NS cost-free all-window obstruction AA.1–AA.15 → bare far-source pressure impulse AA.16–AA.18 → near pressure and viscosity OPEN"],
  ["CB.5：平台能量历史", "CB.5: plateau energy history"],
  ["CB.5｜从平台终点归约到 A+P 历史成本", "CB.5 | From plateau-endpoint reduction to the A+P history cost"],
  ["CB.6：固定球集中之后", "CB.6: after fixed-ball concentration"],
  ["CB.6｜从固定球集中到局部持留的准确缺口", "CB.6 | From fixed-ball concentration to the exact local-persistence gap"],
  ["CB.6｜固定球集中之后，还缺少什么", "CB.6 | What remains after fixed-ball concentration"],
  ["CB.7 只是下一章占位，不是已完成研究。成熟时间持留、近源压力、黏性、非线性输运、定量缩球、原路径柱及 G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。", "CB.7 is only a placeholder for the next chapter, not completed research. Mature-time persistence, near-source pressure, viscosity, nonlinear transport, quantitative shrinking, the original path cylinder, and G/G-P/G-C are not frozen; later research is not presented as proved."],
  ["Clay-B 独立路线停在 CB.6", "The independent Clay-B route stops at CB.6"],
  ["Clay-B 独立研究路线树", "Independent Clay-B research route tree"],
  ["Clay-B 局部集中与持留预算", "Clay-B local concentration and persistence budgets"],
  ["m≈κA⁴ bulk saddle、m≈A² 转换区、arbitrary packets、Version-M、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。这里不把 Clay-B 章节画成 R0.76L 的实线后继。", "The m≈κA⁴ bulk saddle, m≈A² transition, arbitrary packets, Version-M, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. The Clay-B chapters are not drawn here as a solid-line successor of R0.76L."],
  ["R0 主序列停在 R0.76L", "The R0 main sequence stops at R0.76L"],
  ["R0 主序列研究路线树", "R0 main-sequence research route tree"],
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
  assert.equal(rows.length, translations.size, "homepage Clay-B topology translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("Independent Clay-B research route tree"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "homepage Clay-B topology source-string count drift");
  const additions = missing.map((entry, index) => {
    const en = translations.get(entry.zh);
    assert.equal(typeof en, "string", "missing local translation: " + entry.zh);
    validateTranslation(entry.zh, en);
    return { id: prefix + String(index + 1).padStart(3, "0"), ...entry, en };
  });
  await writeFile(translationPath, JSON.stringify([...base, ...additions], null, 2) + "\n");
  const node = process.execPath;
  const built = spawnSync(node, ["scripts/build-i18n.mjs", "translations/en.json"], { cwd: root, encoding: "utf8" });
  assert.equal(built.status, 0, built.stdout + "\n" + built.stderr);
}

process.stdout.write(JSON.stringify({
  release: "Homepage-ClayB-Topology-20260906",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: translations.size,
  applied: !checkOnly,
}, null, 2) + "\n");
