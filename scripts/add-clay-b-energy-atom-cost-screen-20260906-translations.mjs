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
const prefix = "claybenergyatomcostscreen20260906";

const translations = new Map([
  ["必要约束为 r⁴=o(δ_r)、δ_r=o(r²) 及 D_r≥c m^(5/4)E^(-3/4)r^(1/2)。成本趋零且尾窗口嵌套，不能相加或由下界相减，所以本次没有产生有限总耗散矛盾。", "The necessary constraints are r⁴=o(δ_r), δ_r=o(r²), and D_r≥c m^(5/4)E^(-3/4)r^(1/2). The cost vanishes and the tail windows are nested, so they cannot be added or subtracted through lower bounds; no finite-total-dissipation contradiction is obtained."],
  ["趋零成本不产生耗散矛盾", "the vanishing cost creates no dissipation contradiction"],
  ["完整阅读 full-tail 稿 §§3–6，核对冻结 Hodge 球、同一 NS 漂移、共同伴随提取、终端集中及整个有序时间三角上的统一性；§7 二阶障碍仍未进入已证范围。", "Read §§3–6 of the full-tail paper in full and audit the frozen Hodge balls, the same NS drift, common-adjoint extraction, terminal concentration, and uniformity on the entire ordered-time triangle. The second-order obstruction in §7 is still outside the proved scope."],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.18 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.18 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：共同伴随结构核查", "Next research action: common-adjoint structure audit"],
  ["原子—耗散测试已进入 CB.18", "The atom–dissipation test has entered CB.18"],
  ["原子存在/排除与一般正则性 OPEN · NOT CLAY", "atom existence/exclusion and general regularity OPEN · NOT CLAY"],
  ["阅读 CB.18 HTML", "Read CB.18 HTML"],
  ["阅读最新 CB.18 原子成本笔记 →", "Read the latest CB.18 atom-cost note →"],
  ["在同一固定原解具有正终端能量原子的条件分支中，最后阈值窗口与完整带符号局部平衡给出严格次抛物宽度和 r^(1/2) 全局尾耗散成本。但该成本趋零，窗口又相互嵌套，不能重复计费，因此没有形成有限总耗散矛盾。G OPEN。NOT CLAY.", "On the conditional branch where the same fixed source solution has a positive terminal energy atom, last-threshold windows and the complete signed local balance give strictly subparabolic width and an r^(1/2) global tail-dissipation cost. But the cost vanishes and the windows are nested, so they cannot be charged repeatedly; no finite-total-dissipation contradiction follows. G OPEN. NOT CLAY."],
  ["综述 v2.62 · 2026-09-06", "Research review v2.62 · 2026-09-06"],
  ["最后阈值与正带符号净通量成立", "last thresholds and positive signed net flux hold"],
  ["BO 已核对最后阈值、完整带符号通量、全局尾耗散成本及嵌套窗口不可重复计费；结果见下一个正式路线节点。", "BO verifies the last threshold, complete signed flux, global tail-dissipation cost, and why nested windows cannot be charged repeatedly. The result appears in the next formal route node."],
  ["BO 在同一固定周期 NS 原解具有质量 m 的正终端能量原子这一额外条件下，构造有序最后阈值窗口，保留完整规范压力、输运、黏性截止和局部耗散，得到 N_r≥m/8+D_(χ,r)。", "Under the additional assumption that the same fixed periodic NS solution has a positive terminal energy atom of mass m, BO constructs ordered last-threshold windows, retains the complete canonical pressure, transport, viscous cutoff, and local dissipation, and obtains N_r≥m/8+D_(χ,r)."],
  ["CB.1–CB.18 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.18 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.18｜终端能量原子的耗散成本：最后阈值窗口", "CB.18 | Dissipation cost of a terminal energy atom: the last-threshold window"],
  ["CB.19 只是下一章占位，不是已完成研究。full-tail 共同伴随核心、延迟二阶算子预算、原子存在或排除、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。", "CB.19 is only a next-chapter placeholder, not completed research. The full-tail common-adjoint core, delayed second-order operator budget, atom existence or exclusion, G, arbitrary-singularity input generation, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.18", "The independent Clay-B route stops at CB.18"],
  ["Clay-B 已完成终端能量原子的直接耗散成本测试：最后阈值窗口和完整带符号局部平衡给出严格次抛物宽度及 r^(1/2) 全局尾成本，但成本趋零且窗口嵌套，本次没有形成有限总耗散矛盾。下一步只核查 full-tail 的共同伴随结构。", "Clay-B has completed the direct dissipation-cost test for a terminal energy atom. Last-threshold windows and the complete signed local balance give strictly subparabolic width and an r^(1/2) global tail cost, but the cost vanishes and the windows are nested, so no finite-total-dissipation contradiction is obtained. The next step audits only the full-tail common-adjoint structure."],
  ["Clay-B 原子耗散成本筛查结论", "Clay-B atom-dissipation cost screen conclusions"],
  ["Clay-B 终端能量原子成本笔记快捷入口", "Clay-B terminal energy-atom cost note shortcuts"],
  ["；完整读取", "; read in full"],
  ["本轮定向复核", "This bounded review revisits"],
  ["全 17 页，但 FGT、Nash、Hardy–BMO 与周期交换子等外部依赖未全部重审；", "all 17 pages, but external dependencies including FGT, Nash, Hardy–BMO, and periodic commutators were not all reaudited;"],
  ["文献综述 v2.62 · 2026-09-06", "Literature review v2.62 · 2026-09-06"],
  ["阅读完整 CB.18 笔记", "Read the complete CB.18 note"],
  ["只读取 1–7 页，Theorem 2.3 的共同伴随核心与 §§3–7 完整证明仍待核查。两稿此前已登记，不称新发现；没有穷尽文献、完成 Deep Research、新颖性审查或外部同行评审。", "Only pages 1–7 were read; the common-adjoint core of Theorem 2.3 and the complete proofs in §§3–7 remain to be audited. Both papers were already registered and are not presented as new discoveries; no exhaustive literature review, completed Deep Research, novelty audit, or external peer review is claimed."],
  ["CB.18 · Clay-B 终端能量原子耗散成本的文献和主张边界", "CB.18 · Literature and claim boundary for Clay-B terminal energy-atom dissipation cost"],
  ["CB.18 · ClayB-EnergyAtomCostScreen-20260906 公开边界", "CB.18 · Public boundary for ClayB-EnergyAtomCostScreen-20260906"],
  ["CONDITIONAL NECESSITY：假设同一固定周期 NS 原解终端有质量 m 的正能量原子，最后阈值窗口满足 r⁴=o(δ_r)、δ_r=o(r²)。SIGNED FLUX：完整带符号局部平衡给 N_r≥m/8+D_(χ,r)。GLOBAL TAIL COST：D_r≥c m^(5/4)E^(-3/4)r^(1/2)，但这是趋零的全局尾耗散成本，不是局部耗散下界。ALGEBRAIC COMPATIBILITY：δ≈r^(5/2)、D≈r^(1/2) 只证明必要不等式相容，不是 NS 实现或最优率。嵌套窗口不能相加或由尾积分下界相减；本次没有有限总耗散矛盾。FINITE CHECKS ONLY：三份文本源、18 个 BO 标签、115/115 文件绑定、18 项精确算术检查和 3 项有限负对照不替代 PDE 证明。原子存在/排除、共同伴随核心、二阶算子预算、G、一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "CONDITIONAL NECESSITY: assume the same fixed periodic NS solution has a positive terminal energy atom of mass m. Its last-threshold windows satisfy r⁴=o(δ_r) and δ_r=o(r²). SIGNED FLUX: the complete signed local balance gives N_r≥m/8+D_(χ,r). GLOBAL TAIL COST: D_r≥c m^(5/4)E^(-3/4)r^(1/2), but this is a vanishing global tail-dissipation cost, not a localized dissipation lower bound. ALGEBRAIC COMPATIBILITY: δ≈r^(5/2), D≈r^(1/2) proves only that the necessary inequalities are compatible, not an NS realization or optimal rate. Nested windows cannot be added, nor can tail-integral lower bounds be subtracted; no finite-total-dissipation contradiction is obtained. FINITE CHECKS ONLY: three text sources, 18 BO labels, 115/115 file bindings, 18 exact arithmetic checks, and three limited negative controls do not replace PDE proof. Atom existence/exclusion, the common-adjoint core, the second-order operator budget, G, and general regularity remain OPEN. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["Huang 压力预印本 2608.30715v1", "Huang pressure preprint 2608.30715v1"],
  ["Huang full-tail 预印本 2608.04138v1", "Huang full-tail preprint 2608.04138v1"],
  ["研究笔记总索引 · v2.62 · 2026-09-06", "Research-note master index · v2.62 · 2026-09-06"],
  ["终端能量原子的耗散成本：最后阈值窗口", "Dissipation cost of a terminal energy atom: the last-threshold window"],
  ["CB.1–CB.18 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.18 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
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
  assert.equal(rows.length, translations.size, "EnergyAtomCostScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.18"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "EnergyAtomCostScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-EnergyAtomCostScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
