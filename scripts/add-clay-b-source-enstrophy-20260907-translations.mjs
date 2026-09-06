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
const prefix = "claybsourceenstrophy20260907";

const translations = new Map([
  ["本轮有界第一手来源核查读取", "This bounded primary-source check read"],
  ["本轮只核对元数据与摘要。没有重审前者 §3/§5 全部证明、外部依赖或周期迁移，也不主张穷尽性、外部同行评审或文献新颖性。", "This round checked only metadata and abstract. The former paper's full §3/§5 proofs, external dependencies, and periodic transfer were not reaudited, and no exhaustiveness, external peer review, or literature novelty is claimed."],
  ["的全空间设定、Theorem 1.2、Proposition 3.1 与完整 §4；这些结论保留额外可积性或 Type I 条件，没有自动支付 BW 的周期能量类输入。", "full-space setup, Theorem 1.2, Proposition 3.1, and complete §4. These results retain extra integrability or Type I conditions and do not automatically pay BW's periodic energy-class input."],
  ["文献综述 v2.68 · 2026-09-06", "Literature review v2.68 · 2026-09-06"],
  ["阅读完整 CB.24 笔记", "Read the complete CB.24 note"],
  ["CB.24 · Clay-B 源项与梯度能量的来源和主张边界", "CB.24 · Sources and claim boundary for Clay-B sources and gradient energy"],
  ["CB.24 · ClayB-SourceEnstrophy-20260907 公开边界", "CB.24 · Public boundary for ClayB-SourceEnstrophy-20260907"],
  ["CONDITIONAL：全部 BW 结论假设 BP/BU 的同一周期无外力光滑 NS 原解、额外正终端能量原子与共同伴随。STRICT POSITIVE TIME：全周期线性无散梯度测试消掉压力，但保留反号黏性、二阶源、应变及未受控梯度端点；非线性或截止测试仍有压力。FINITE CLASS：任意固定正定 2×2 二次梯度组合的 sym(KA) 行列式为 −ν²a(e+2cd+c²a)<0，只排除对任意 Hessian 方向共同正耗散的常系数类，不是实际 NS 轨道或全部能量方法的 no-go。CONDITIONAL DIVERGENCE：正原子分支上，每个 0<δ≤L 都有 ∫₀^δ||Δw||₂⁴ᐟ³=∞；若有限，则 b∈L⁴L³ 使 w_ρ∈L¹L² 并产生与弱零迹、范数趋一矛盾的强 L² 迹。ONE-WAY ONLY：BW.18 的充分上界右端无穷不能反推 W_z 无穷；没有范数等价、混合功不可能性或 G 输入减少。BV 的两条充分接口、自压力和端点仍未付。FINITE CHECKS ONLY：三份文本源、18 个 BW 标签、164/164 文件绑定、25 项有理复算和 5 项有限负对照不替代 PDE 证明。未来 R/S 五项去重尚未开始；原子生成/排除、G、R.216–R.217、一般正则性和新颖性 OPEN；无图、仿真、新 PDF 或 recap。NOT CLAY。", "CONDITIONAL: every BW conclusion assumes the BP/BU same periodic unforced smooth NS parent, the extra positive terminal-energy atom, and the common adjoint. STRICT POSITIVE TIME: full-periodic linear divergence-free gradient tests remove pressure but retain opposite viscosity, second-order sources, strain, and uncontrolled gradient endpoints; nonlinear or cutoff tests retain pressure. FINITE CLASS: every fixed positive-definite 2×2 quadratic gradient combination has det sym(KA)=−ν²a(e+2cd+c²a)<0. This excludes only common positive dissipation in arbitrary Hessian directions for the constant-coefficient class, not actual NS trajectories or all energy methods. CONDITIONAL DIVERGENCE: on the positive-atom branch, ∫₀^δ||Δw||₂⁴ᐟ³=∞ for every 0<δ≤L. If finite, b∈L⁴L³ gives w_ρ∈L¹L² and a strong L² trace contradicting weak trace zero and norm tending to one. ONE-WAY ONLY: an infinite right side of the sufficient BW.18 bound does not imply W_z=∞. No norm equivalence, impossibility of mixed-work control, or reduction of G input is proved. BV's two sufficient interfaces, self-pressure, and endpoints remain unpaid. FINITE CHECKS ONLY: three text sources, 18 BW labels, 164/164 file bindings, 25 rational recomputations, and five limited negative controls do not replace PDE proof. The five future R/S deduplication checks have not started. Atom generation or exclusion, G, R.216–R.217, general regularity, and novelty remain OPEN. There is no figure, simulation, new PDF, or recap. NOT CLAY."],
  ["残差的梯度能量：源项、应变与二次组合的边界", "Residual gradient energy: sources, strain, and the boundary of quadratic combinations"],
  ["研究笔记总索引 · v2.68 · 2026-09-06", "Research-note master index · v2.68 · 2026-09-06"],
  ["CB.1–CB.24 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.24 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["不能反推 W_z · G OPEN · NOT CLAY", "no reverse implication for W_z · G OPEN · NOT CLAY"],
  ["常二次组合有限类障碍", "finite-class obstruction for constant quadratic combinations"],
  ["全周期梯度测试消掉压力，却留下二阶源项和应变；固定正定二次组合不能共同正耗散。正原子分支迫使 Δw 的 L⁴ᐟ³_tL²_x 成本发散，但不能反推 W_z 发散、范数等价或混合功不可控。G 仍 OPEN。NOT CLAY.", "Full-periodic gradient tests remove pressure but retain second-order sources and strain. Fixed positive-definite quadratic combinations cannot give common positive dissipation. The positive-atom branch forces divergence of the L⁴ᐟ³_tL²_x cost of Δw, but this does not imply divergence of W_z, norm equivalence, or impossibility of mixed-work control. G remains OPEN. NOT CLAY."],
  ["全周期线性无散梯度测试消掉压力，但二阶源项、应变与梯度端点仍未支付；常系数正定二次型的扩散对称部分行列式恒负，只排除任意 Hessian 方向的固定二次组合。", "Full-periodic linear divergence-free gradient tests remove pressure, but second-order sources, strain, and gradient endpoints remain unpaid. The symmetric diffusion part of every constant positive-definite quadratic form has negative determinant, excluding only fixed quadratic combinations in arbitrary Hessian directions."],
  ["投影给出逐时幅度一致上界；联合截断只控制有符号累计压力。W_z 与混合压力平方是两条不同且未付的充分接口，三个余项和自压力均保留。", "Projection gives a pointwise amplitude-uniform bound, while joint truncation controls only signed cumulative pressure. W_z and the mixed-pressure square are distinct unpaid sufficient interfaces; all three remainders and self-pressure remain."],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.24 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.24 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：一般中心的 R/S 历史去重", "Next research action: R/S historical deduplication at a general centre"],
  ["先完整读取五项已定位的时钟与边界账本，再判断是否存在尚未测试的 NS 有符号项。去重与推导均尚未开始。", "First fully read the five located clock and boundary ledgers, then decide whether an untested signed NS term remains. Neither deduplication nor derivation has started."],
  ["严格正时间梯度恒等式", "strict-positive-time gradient identities"],
  ["源项与梯度能量核查已进入 CB.24", "The source and gradient-energy audit has entered CB.24"],
  ["阅读 CB.24 HTML", "Read CB.24 HTML"],
  ["阅读最新 CB.24 笔记 →", "Read the latest CB.24 note →"],
  ["正原子分支迫使 Δw∉L⁴ᐟ³_tL²_x，否则投影方程给出矛盾的强 L² 初迹。这不反推 W_z 发散、范数等价或混合功不可控，也未减少 G 的未证输入。", "The positive-atom branch forces Δw∉L⁴ᐟ³_tL²_x; otherwise the projected equation gives a contradictory strong L² initial trace. This does not imply divergence of W_z, norm equivalence, or impossibility of mixed-work control, and it reduces no unproved input of G."],
  ["综述 v2.68 · 2026-09-06", "Research review v2.68 · 2026-09-06"],
  ["BW 已写清严格正时间恒等式、常二次组合的有限类障碍与条件性 4/3 二阶成本发散；结果见下一个路线节点。", "BW records the strict-positive-time identities, the finite-class obstruction for constant quadratic combinations, and conditional divergence of the 4/3 second-order cost. The result appears in the next route node."],
  ["CB.1–CB.24 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.24 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.24｜残差的梯度能量：源项、应变与二次组合的边界", "CB.24 | Residual gradient energy: sources, strain, and the boundary of quadratic combinations"],
  ["CB.25 只是下一章占位，不是已完成研究。R/S 去重、W_z、混合压力平方、自压力、原子存在或排除、G、R.216–R.217、一般正则性与 Clay 均未关闭。", "CB.25 is only a next-chapter placeholder, not completed research. R/S deduplication, W_z, the mixed-pressure square, self-pressure, atom existence or exclusion, G, R.216–R.217, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.24", "The independent Clay-B route stops at CB.24"],
  ["Clay-B 已核清同父残差的梯度能量边界：全周期线性无散测试消掉压力，却留下二阶源项、应变和梯度端点；固定正定二次组合不能共同正耗散，正原子分支还迫使 Δw 的 L⁴ᐟ³_tL²_x 成本发散。但这不反推 W_z 发散、混合功不可控或 G 输入减少。下一步先做一般中心 R/S 历史去重。", "Clay-B has clarified the same-parent residual gradient-energy boundary. Full-periodic linear divergence-free tests remove pressure but retain second-order sources, strain, and gradient endpoints. Fixed positive-definite quadratic combinations cannot give common positive dissipation, and the positive-atom branch forces divergence of the L⁴ᐟ³_tL²_x cost of Δw. But this does not imply divergence of W_z, impossibility of mixed-work control, or reduction of G input. The next step first performs R/S historical deduplication at a general centre."],
  ["Clay-B 源项与梯度能量笔记快捷入口", "Clay-B source and gradient-energy note shortcuts"],
  ["Clay-B 源项与梯度能量结论", "Clay-B source and gradient-energy conclusions"],
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
  assert.equal(rows.length, translations.size, "SourceEnstrophy translation count drift");
  for (const row of rows) { assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh); validateTranslation(row.zh, row.en); }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.24"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "SourceEnstrophy source-string count drift");
  const additions = missing.map((entry, index) => {
    const en = translations.get(entry.zh); assert.equal(typeof en, "string", "missing local translation: " + entry.zh); validateTranslation(entry.zh, en);
    return { id: prefix + String(index + 1).padStart(3, "0"), ...entry, en };
  });
  await writeFile(translationPath, JSON.stringify([...base, ...additions], null, 2) + "\n");
  const built = spawnSync(process.execPath, ["scripts/build-i18n.mjs", "translations/en.json"], { cwd: root, encoding: "utf8" });
  assert.equal(built.status, 0, built.stdout + "\n" + built.stderr);
}

process.stdout.write(JSON.stringify({ release: "ClayB-SourceEnstrophy-20260907", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
