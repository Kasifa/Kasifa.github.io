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
const prefix = "claybsignedmixedpressure20260907";

const translations = new Map([
  ["本轮完整读取冻结的 BU 与 BT。外部读取仅限", "This round fully read the frozen BU and BT. External reading was limited to"],
  ["的官方元数据和摘要，没有读取该 PDF 的定理或证明，也没有导入外部能量等式。旧 Hardy/BMO 比较只作团队范围核算，不扩大为穷尽检索、外部同行评审或新颖性结论。", "official metadata and abstract. The PDF's theorems and proofs were not read, and no external energy equality was imported. The prior Hardy/BMO comparison is only team-bounded accounting, not exhaustive search, external peer review, or a novelty claim."],
  ["文献综述 v2.67 · 2026-09-06", "Literature review v2.67 · 2026-09-06"],
  ["阅读完整 CB.23 笔记", "Read the complete CB.23 note"],
  ["CB.23 · Clay-B 有符号混合压力功的来源和主张边界", "CB.23 · Sources and claim boundary for Clay-B signed mixed-pressure work"],
  ["CB.23 · ClayB-SignedMixedPressure-20260907 公开边界", "CB.23 · Public boundary for ClayB-SignedMixedPressure-20260907"],
  ["CONDITIONAL：全部 BV 结论假设 BP/BU 的同一光滑无外力周期 NS 原解、额外正终端原子、共同饱和伴随与定位。PROVED IN STATED SCOPE：全周期投影与径向输运消去给 |M_R|≤C||z||₃||∇w||₂²，常数不依赖 R，但这只是逐时估计。SUFFICIENT INPUTS：W_z=∫||z||₃||∇w||₂²<∞ 或 r∈L²_{t,x} 各自足以推出 M_R→0 于 L¹；两者不同、均未支付，也未证明必要或等价。JOINT TRUNCATION：同幅联合 Hessian 有统一界，相反黏性交叉项抵消但两个 −2νc 源项保留；只有 sup_t|∫₀ᵗP_R|→0，不能升级为 L¹、总变差或 UI。REMAINDERS：T_R、E_R^q、E_R^π 与自压力均不能省略；累计 2νcD_w≤||z⊗w||₁→0 不支付残差加权耗散密度。FINITE CHECKS ONLY：三份文本源、23 个 BV 标签、156/156 文件绑定、25 项有理复算和 4 项有限负对照不替代 PDE 证明。原子存在或排除、G、R.216–R.217、一般正则性与新颖性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "CONDITIONAL: every BV conclusion assumes the BP/BU same smooth unforced periodic NS parent, the extra positive terminal atom, the common saturated adjoint, and localization. PROVED IN STATED SCOPE: full-periodic projection and radial transport cancellation give |M_R|≤C||z||₃||∇w||₂² with a constant independent of R, but this is only a pointwise-in-time estimate. SUFFICIENT INPUTS: either W_z=∫||z||₃||∇w||₂²<∞ or r∈L²_{t,x} is sufficient for M_R→0 in L¹. They are distinct and unpaid, and are not proved necessary or equivalent. JOINT TRUNCATION: same-amplitude joint Hessians have uniform bounds; opposite-viscosity cross terms cancel, but both −2νc source terms remain. Only sup_t|∫₀ᵗP_R|→0 is proved, not L¹, total variation, or UI. REMAINDERS: T_R, E_R^q, E_R^π, and self-pressure must all remain. The cumulative bound 2νcD_w≤||z⊗w||₁→0 does not pay the residual-weighted dissipation density. FINITE CHECKS ONLY: three text sources, 23 BV labels, 156/156 file bindings, 25 rational recomputations, and four limited negative controls do not replace PDE proof. Atom existence or exclusion, G, R.216–R.217, general regularity, and novelty remain OPEN. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["研究笔记总索引 · v2.67 · 2026-09-06", "Research-note master index · v2.67 · 2026-09-06"],
  ["有符号混合压力功：投影测试和联合截断", "Signed mixed-pressure work: projected tests and joint truncation"],
  ["CB.1–CB.23 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.23 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["固定有界凸压力测试给出精确恒等式与所有 1≤q<2 的强零初迹；额外正原子下，撤去幅度截断仍重现条件性半单位端点。", "Fixed bounded convex pressure tests give exact identities and strong zero initial traces for every 1≤q<2. Under the extra positive atom, removing the amplitude truncation still reproduces the conditional half-unit endpoint."],
  ["联合压力仅有符号累计消失", "joint pressure vanishes only as a signed cumulative quantity"],
  ["两条充分接口与自压力 OPEN · NOT CLAY", "two sufficient interfaces and self-pressure OPEN · NOT CLAY"],
  ["全周期投影把混合压力功改写为输运配对，并给出 |M_R|≤C||z||₃||∇w||₂² 的逐时幅度一致上界；但相应加权时间成本 W_z 尚未由能量类支付。", "Full-periodic projection rewrites mixed-pressure work as a transport pairing and gives the pointwise amplitude-uniform bound |M_R|≤C||z||₃||∇w||₂². The corresponding weighted-time cost W_z is not paid by the energy class."],
  ["同幅联合截断证明联合压力的有符号原函数一致趋零，而非 L¹、总变差或 UI。W_z 有限与 r∈L² 是两条不同的充分接口，均未闭合；三个余项和自压力必须保留。", "Same-amplitude joint truncation proves uniform decay of the signed joint-pressure primitive, not L¹, total variation, or UI. Finiteness of W_z and r∈L² are two distinct sufficient interfaces; neither closes. All three remainders and self-pressure must remain."],
  ["投影恒等式去掉逐时估计中显式的幅度成本；联合截断只控制有符号累计压力。加权时间成本与混合压力平方是两条不同且未付的充分接口，自压力与原子排除仍 OPEN。NOT CLAY.", "The projection identity removes explicit amplitude cost from the pointwise estimate, while joint truncation controls only signed cumulative pressure. The weighted-time cost and mixed-pressure square are distinct unpaid sufficient interfaces; self-pressure and atom exclusion remain OPEN. NOT CLAY."],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.23 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.23 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：源项与梯度能量审计", "Next research action: source and gradient-energy audit"],
  ["有符号混合压力功核算已进入 CB.23", "The signed mixed-pressure-work calculation has entered CB.23"],
  ["阅读 CB.23 HTML", "Read CB.23 HTML"],
  ["阅读最新 CB.23 笔记 →", "Read the latest CB.23 note →"],
  ["正原子条件下，终端残差测度在目标点无原子，正向方程保留 −2νΔb 源；混合张量全时间消失且完整周期混合压力有普通时间 little-o。", "Under the positive-atom condition, the terminal residual measure has no atom at the target, and the forward equation retains the source −2νΔb. The mixed tensor vanishes along the full time variable, and full-periodic mixed pressure has ordinary-time little-o."],
  ["直接核对同一原解和残差方程能否支付 W_z、混合压力平方或更弱的有符号控制；不把累计耗散误作加权密度控制。该审计尚未开始。", "Check directly whether the same-parent and residual equations pay W_z, the mixed-pressure square, or a weaker signed control. Do not mistake cumulative dissipation for weighted-density control. This audit has not started."],
  ["逐时幅度一致投影上界", "pointwise amplitude-uniform projected bound"],
  ["综述 v2.67 · 2026-09-06", "Research review v2.67 · 2026-09-06"],
  ["BV 已给出逐时幅度一致投影界、合法的联合截断恒等式与两条明确但未付的充分接口；结果见下一个路线节点。", "BV gives a pointwise amplitude-uniform projected bound, a legitimate joint-truncation identity, and two explicit but unpaid sufficient interfaces. The result appears in the next route node."],
  ["CB.1–CB.23 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.23 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.23｜有符号混合压力功：投影测试和联合截断", "CB.23 | Signed mixed-pressure work: projected tests and joint truncation"],
  ["CB.24 只是下一章占位，不是已完成研究。两条充分接口、自压力、原子存在或排除、G、R.216–R.217、一般正则性与 Clay 均未关闭。", "CB.24 is only a next-chapter placeholder, not completed research. The two sufficient interfaces, self-pressure, atom existence or exclusion, G, R.216–R.217, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.23", "The independent Clay-B route stops at CB.23"],
  ["Clay-B 已用全周期投影得到不显含截断幅度的逐时混合压力功上界，并以同幅联合截断证明联合压力的有符号原函数一致趋零；但加权时间成本与混合压力平方只是两条不同且未付的充分接口，三个余项、自压力与原子排除仍未闭合。下一步直接检查源项和梯度能量演化。", "Clay-B now has a pointwise mixed-pressure-work bound without explicit truncation amplitude from full-periodic projection, and same-amplitude joint truncation proves uniform decay of the signed joint-pressure primitive. But the weighted-time cost and mixed-pressure square are only distinct unpaid sufficient interfaces; the three remainders, self-pressure, and atom exclusion remain open. The next step directly audits source and gradient-energy evolution."],
  ["Clay-B 有符号混合压力笔记快捷入口", "Clay-B signed mixed-pressure note shortcuts"],
  ["Clay-B 有符号混合压力结论", "Clay-B signed mixed-pressure conclusions"],
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
  assert.equal(rows.length, translations.size, "SignedMixedPressure translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.23"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "SignedMixedPressure source-string count drift");
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

process.stdout.write(JSON.stringify({ release: "ClayB-SignedMixedPressure-20260907", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
