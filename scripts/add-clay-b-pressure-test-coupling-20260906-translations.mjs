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
const prefix = "claybpressuretestcoupling20260906";

const translations = new Map([
  ["本章的 HLS 与 Sobolev 嵌入是标准工具，不作为新正则性定理。实际核对了", "The HLS and Sobolev embeddings in this chapter are standard tools, not new regularity theorems. I directly checked"],
  ["的 HLS 核指数约定；周期版本另由均值分离、热核和周期 Riesz 变换适配。还有限读取", "for the HLS kernel-exponent convention. The periodic version is separately adapted using mean separation, the heat kernel, and periodic Riesz transforms. I also read a limited portion of"],
  ["的 Lemma 2.1、moderator 定义与相关展开，用于确认压力 moderator 不是新机制；没有调用其 Theorem 3.5，也未重审全部外部证明。历史压力正则性、局部平滑、averaged NS 和压力功记录继续保留各自前提与访问边界。", "covering Lemma 2.1, the moderator definition, and the related expansion, only to confirm that the pressure moderator is not a new mechanism. Theorem 3.5 is not invoked, and the complete external proof was not reaudited. Historical records on pressure regularity, local smoothing, averaged NS, and pressure work retain their own assumptions and access boundaries."],
  ["文献综述 v2.55 · 2026-09-06", "Literature review v2.55 · 2026-09-06"],
  ["阅读完整 CB.11 笔记", "Read the complete CB.11 note"],
  ["CB.11 · Clay-B 压力与测试配对的文献和主张边界", "CB.11 · Literature and claim boundary for Clay-B pressure/test coupling"],
  ["CB.11 · ClayB-PressureTestCoupling-20260906 公开边界", "CB.11 · Public boundary for ClayB-PressureTestCoupling-20260906"],
  ["PROVED LOCALLY：AR 将低输出成本写成 e_J(L)，AS 区分分离与可比输入，AT/AU 给全域和固定环带小尾持留，AV 证明换测试完整支付后返回原能量恒等式；AW 写全原压力符号并在保留测试输出匹配时证明 W_ang≤Cχ(M²g²+g⁴)。STATIC OBSTRUCTION：AX 在任意预先固定 K、L 下构造固定能量、统一 H¹ 的静态无散 Fourier 场，使实际高输出压力 Fourier-ℓ¹ 至少线性增长；这不是压力 L∞、原测试压力功、NS 轨道或成熟窗口反例。CONDITIONAL：所有终端窗口陈述仍以合法同一解大范数序列存在为条件；g⁴ 小量只是 AW 绝对值路线的充分成本。FINITE CHECKS ONLY：有限有理数核算和 37/37 源字节校验不替代证明。OPEN：真实时间有序演化能否改善 g⁴ 成本、AQ 的原带符号上界、移动缩球 G 与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。", "PROVED LOCALLY: AR expresses the low-output cost as e_J(L); AS separates comparable from separated inputs; AT/AU give global and fixed-annulus small-tail persistence; AV shows that fully paying for a changed test returns the original energy identity. AW retains the complete pressure symbol and proves W_ang≤Cχ(M²g²+g⁴) when the test-output matching is kept. STATIC OBSTRUCTION: for every preassigned K and L, AX constructs static divergence-free Fourier fields with fixed energy and a uniform H¹ bound whose actual high-output pressure Fourier-ℓ¹ grows at least linearly. This is not a counterexample for pressure L∞, original-test pressure work, an NS trajectory, or a mature window. CONDITIONAL: every terminal-window statement remains conditional on a legal large-norm sequence for the same solution. Smallness of g⁴ is only a sufficient cost for AW's absolute-value route. FINITE CHECKS ONLY: finite rational checks and 37/37 source-byte verification do not replace proof. OPEN: whether true time-ordered evolution improves the g⁴ cost, an upper bound for AQ's original signed quantity, moving shrinking G, and general regularity. No complete novelty review, external peer review, or Clay claim is made, and there is no figure, simulation, or cumulative recap. NOT CLAY."],
  ["Tao 245C Notes 1 当前 Corollary 46", "current Corollary 46 in Tao 245C Notes 1"],
  ["Tran–Yu 2019 作者稿", "Tran–Yu 2019 author manuscript"],
  ["压力不能与它的测试因子分开估计", "Pressure cannot be estimated apart from its test factor"],
  ["研究笔记总索引 · v2.55 · 2026-09-06", "Research-note master index · v2.55 · 2026-09-06"],
  ["CB.1–CB.11 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.11 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["保持 AQ 的同一解、固定环带、实际 s_J、窗口、K、坏时间权重与原 χ|u|u 测试，展开高频尾的热初始项和完整 Leray 源项。不能给起点添加小梯度假设，也不能把精确恒等式本身当成新上界。", "Keep AQ's same solution, fixed annulus, actual s_J, window, K, bad-time weight, and original χ|u|u test, then expand the heat initial term and complete Leray source of the high-frequency tail. No small-gradient assumption may be added at the initial time, and an exact identity is not itself a new upper bound."],
  ["固定能量与统一 H¹ 仍允许高频压力 Fourier 绝对和发散，但这不控制原测试压力功。保留最终测试输出匹配后，即使删除相位仍有 W_ang≤Cχ(M²g²+g⁴)；未付的是窗口内 g⁴ 的充分时间成本，而非已知动态障碍。AQ 上界、移动缩球 G 与一般正则性仍 OPEN。NOT CLAY.", "Fixed energy and a uniform H¹ bound still permit divergence of the high-frequency pressure Fourier absolute sum, but this does not control original-test pressure work. When final test-output matching is retained, W_ang≤Cχ(M²g²+g⁴) even after phases are deleted. The unpaid item is the sufficient time cost of g⁴ over the window, not a known dynamical obstruction. The AQ upper bound, moving shrinking G, and general regularity remain OPEN. NOT CLAY."],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.11 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.11 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：真实时间 Duhamel 能否改善 g⁴ 成本", "Next research question: can true-time Duhamel improve the g⁴ cost?"],
  ["压力侧 Fourier-ℓ¹：静态能量预算失败", "Pressure-side Fourier-ℓ¹: static energy budget fails"],
  ["压力侧与测试侧的区别已进入 CB.11", "The pressure-side/test-side distinction now forms CB.11"],
  ["原测试输出匹配：瞬时上界", "Original-test output matching: instantaneous upper bound"],
  ["阅读最新 CB.11 压力与测试配对笔记 →", "Read the latest CB.11 pressure/test-coupling note →"],
  ["综述 v2.55 · 2026-09-06", "Review v2.55 · 2026-09-06"],
  ["AR–AV 支付低压力输出、列出分频输入成本、证明全域与固定环带的高频尾持留，并说明换成高尾测试最终返回原局部立方能量恒等式。这些方法检查没有给出 AQ 的相反上界。", "AR–AV pay low pressure outputs, list dyadic input costs, prove global and fixed-annulus high-frequency-tail persistence, and show that changing to a high-tail test ultimately returns the original local cubic energy identity. These method checks do not give an upper bound opposite to AQ."],
  ["AR–AX 已分开静态压力 Fourier 绝对成本与保留原测试输出匹配的真实工作估计；结果见下一个正式路线节点。", "AR–AX now separate the static pressure Fourier absolute cost from the genuine work estimate that retains original-test output matching; the result appears in the next formal route node."],
  ["AW 保留原测试的输出频率匹配，得到与 K、L 无关的 W_ang≤Cχ(M²g²+g⁴)；AX 同时证明固定能量和统一 H¹ 不能控制压力侧 Fourier-ℓ¹。两者不矛盾，因为 AX 没有最终测试因子。真正未付的是 g⁴ 的时间充分成本。", "AW retains the original test's output-frequency matching and obtains W_ang≤Cχ(M²g²+g⁴), independent of K and L. AX separately proves that fixed energy and a uniform H¹ bound cannot control pressure-side Fourier-ℓ¹. The results do not conflict because AX omits the final test factor. The genuinely unpaid item is the sufficient time cost of g⁴."],
  ["CB.1–CB.11 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.11 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.10 坏时间必要下界 → AR 低输出转移 → AS 分频成本 → AT/AU 尾持留 → AV 换测试返回原恒等式 → AW 原测试匹配瞬时界 / AX 静态压力侧阻碍 → 真实时间 Duhamel 检查 OPEN", "CB.10 bad-time necessary lower bound → AR low-output transfer → AS dyadic cost → AT/AU tail persistence → AV test change returns the original identity → AW original-test-matched instantaneous bound / AX static pressure-side obstruction → true-time Duhamel check OPEN"],
  ["CB.11：压力与测试配对", "CB.11: pressure/test coupling"],
  ["CB.11｜压力不能与它的测试因子分开估计", "CB.11 | Pressure cannot be estimated apart from its test factor"],
  ["CB.11｜压力侧静态阻碍与原测试配对上界", "CB.11 | Static pressure-side obstruction and original-test-matched upper bound"],
  ["CB.12 只是下一章占位，不是已完成研究。g⁴ 时间成本、原带符号坏时间工作的真实 NS 上界、缩球一致常数、移动路径、G/G-P/G-C、实际 R.216–R.217 输入与首次奇点排除尚未冻结；不把后续 Duhamel 检查写成已证结论。", "CB.12 is only a placeholder for the next chapter, not completed research. The g⁴ time cost, a genuine NS upper bound for the original signed bad-time work, shrinking-scale uniform constants, moving paths, G/G-P/G-C, actual R.216–R.217 inputs, and first-singularity exclusion are not frozen. The later Duhamel check is not presented as proved."],
  ["Clay-B 独立路线停在 CB.11", "The independent Clay-B route stops at CB.11"],
  ["Clay-B 压力与测试配对笔记快捷入口", "Clay-B pressure/test-coupling note shortcuts"],
  ["Clay-B 压力与测试配对结论", "Clay-B pressure/test-coupling result boundary"],
  ["Clay-B 已把压力侧静态绝对成本与原测试压力功分开：固定能量和统一 H¹ 不能控制压力 Fourier-ℓ¹，但保留原测试输出匹配后有与截止无关的瞬时界。真正未付的是窗口内 g⁴ 的充分时间成本；AQ 上界、缩球路径和合同 G 继续开放。", "Clay-B now separates the static absolute pressure-side cost from original-test pressure work: fixed energy and a uniform H¹ bound cannot control pressure Fourier-ℓ¹, while retaining original-test output matching gives an instantaneous cutoff-independent bound. The genuinely unpaid item is the sufficient g⁴ time cost over the window. The AQ upper bound, shrinking path, and contract G remain open."],
  ["g⁴ 时间成本、AQ 上界与 G OPEN · NOT CLAY", "g⁴ time cost, AQ upper bound, and G OPEN · NOT CLAY"],
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
  assert.equal(rows.length, translations.size, "PressureTestCoupling translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.11"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "PressureTestCoupling source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-PressureTestCoupling-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
