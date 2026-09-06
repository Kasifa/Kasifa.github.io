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
const prefix = "claybcommonadjointscreen20260906";

const translations = new Map([
  ["共同伴随核查已进入 CB.19", "The common-adjoint audit has entered CB.19"],
  ["全算子预算不是更弱出口", "the full operator budget is not a weaker exit"],
  ["同一原解与最终离散全尾结构保留", "the same parent and final discrete full-tail structure are retained"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.19 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.19 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：终端唯一性适用性核查", "Next research action: terminal-uniqueness applicability audit"],
  ["阅读 CB.19 HTML", "Read CB.19 HTML"],
  ["阅读最新 CB.19 共同伴随笔记 →", "Read the latest CB.19 common-adjoint note →"],
  ["正终端能量原子的条件分支保留同一原解驱动的共同伴随与最终离散全尾；固定后继解二阶作用发散，但基本能量不支付该成本。全单位初态延迟算子预算的有限性已等价于同一原解光滑延拓，而不是更弱的已支付条件。G OPEN。NOT CLAY.", "The positive-terminal-energy-atom branch retains a common adjoint driven by the same parent and the final discrete full tail. A fixed descendant has divergent second-order action, but basic energy does not pay that cost. Finiteness of the full unit-initial-data delayed operator budget is already equivalent to smooth continuation of the same parent, rather than a weaker paid condition. G OPEN. NOT CLAY."],
  ["终端唯一性适用性与一般正则性 OPEN · NOT CLAY", "terminal-uniqueness applicability and general regularity OPEN · NOT CLAY"],
  ["逐项比较带压力共同伴随的时间方向、弱终端迹、真实 NS 漂移空间、非局部投影和定义域。该核查尚未开始，不能展示成已适用或已支付的定理。", "Compare the pressure-coupled common adjoint's time direction, weak terminal trace, true NS drift space, nonlocal projection, and domain one by one. This audit has not started and cannot be displayed as an applicable or paid theorem."],
  ["综述 v2.63 · 2026-09-06", "Research review v2.63 · 2026-09-06"],
  ["BP/BQ 在正终端能量原子的额外条件下重构同一固定周期 NS 原解驱动的共同伴随和最终保留离散链全尾；一个固定后继解在互异时间单元上的二阶作用与 enstrophy 生产正部发散，但不与一阶能量矛盾。", "Under the additional positive-terminal-energy-atom condition, BP/BQ reconstruct a common adjoint driven by the same fixed periodic NS parent and the full tail of the final retained discrete chain. A fixed descendant has divergent second-order action and positive enstrophy-production part on disjoint time cells, without contradicting first-order energy."],
  ["BP/BQ/BR 已核对同一原解共同伴随、最终离散全尾、固定后继解二阶成本及全算子预算强度；结果见下一个正式路线节点。", "BP/BQ/BR verify the same-parent common adjoint, final discrete full tail, fixed-descendant second-order cost, and full-operator-budget strength. The result appears in the next formal route node."],
  ["BR 另证全单位初态延迟算子预算即使只对某一对时刻有限，也已等价于同一原解越过 T 光滑延拓。这个强度识别不证明预算有限，不排除原子，也不扩大一般正则性。", "BR separately proves that finiteness of the full unit-initial-data delayed operator budget for even one time pair is already equivalent to smooth continuation of the same parent across T. This strength identification proves no budget bound, excludes no atom, and enlarges no general regularity class."],
  ["CB.1–CB.19 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.19 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.19｜共同伴随与算子出口：结构保留，预算等价于延拓", "CB.19 | Common adjoint and operator exit: retained structure, budget equivalent to continuation"],
  ["CB.20 只是下一章占位，不是已完成研究。终端唯一性适用性核查尚未开始；原子存在或排除、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。", "CB.20 is only a next-chapter placeholder, not completed research. The terminal-uniqueness applicability audit has not started. Atom existence or exclusion, G, arbitrary-singularity input generation, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.19", "The independent Clay-B route stops at CB.19"],
  ["Clay-B 共同伴随筛查结论", "Clay-B common-adjoint screen conclusions"],
  ["Clay-B 共同伴随与算子出口笔记快捷入口", "Clay-B common-adjoint and operator-exit note shortcuts"],
  ["Clay-B 已完成共同伴随核心与算子出口强度核查：正原子条件下同一原解驱动的共同伴随和最终离散全尾可保留，固定后继解二阶作用发散；但全单位初态延迟算子预算的有限性已等价于原解光滑延拓，并非更弱的能量出口。下一步只核查终端唯一性的适用条件。", "Clay-B has completed the common-adjoint core and operator-exit strength audit. Under the positive-atom condition, the common adjoint driven by the same parent and the final discrete full tail are retained, while a fixed descendant has divergent second-order action. But finiteness of the full unit-initial-data delayed operator budget is already equivalent to smooth continuation of the parent, not a weaker energy exit. The next step audits only the applicability conditions for terminal uniqueness."],
  ["本轮完整使用", "This round uses in full"],
  ["的 §§2–7，但第 20 页未读，Appendix A 未完整核查；定向读取", " §§2–7, but page 20 was not read and Appendix A was not completely audited; the targeted reading of"],
  ["的 H¹ 局部存在、唯一性、光滑性、延拓与均值接口。两稿均已登记，不称新发现；引用的全部外部证明依赖未完全重审，没有穷尽性新颖性检索、完成 Deep Research 或外部同行评审。", " covered its H¹ local existence, uniqueness, smoothness, continuation, and mean interfaces. Both papers were already registered and are not presented as new discoveries. Not every cited external proof dependency was reaudited; no exhaustive novelty search, completed Deep Research, or external peer review is claimed."],
  ["文献综述 v2.63 · 2026-09-06", "Literature review v2.63 · 2026-09-06"],
  ["阅读完整 CB.19 笔记", "Read the complete CB.19 note"],
  ["CB.19 · Clay-B 共同伴随与算子出口的文献和主张边界", "CB.19 · Literature and claim boundary for the Clay-B common adjoint and operator exit"],
  ["CB.19 · ClayB-CommonAdjointScreen-20260906 公开边界", "CB.19 · Public boundary for ClayB-CommonAdjointScreen-20260906"],
  ["LITERATURE RECONSTRUCTION：在同一固定周期 NS 原解具有正终端能量原子的额外条件下，BP/BQ 重构共同伴随、弱零终端迹、原子定位、Cauchy 饱和及最终保留离散链的全尾；不是任意连续时间对或整个原目录。SECOND-ORDER OBSTRUCTION：一个固定后继解在互异晚期时间单元上的二阶作用及 enstrophy 生产正部发散，但一阶能量不支付二阶成本，因此没有矛盾。BUDGET STRENGTH AUDIT：BR 另证全单位初态延迟算子预算对某一对有限、对每一对有限与同一原解越过 T 光滑延拓等价；没有证明该预算有限，也不推广到弱解、外力或全空间。FINITE CHECKS ONLY：五份文本源、57 个 BP/BQ/BR 标签、125/125 文件绑定、31 项精确算术检查和 3 项有限负对照不替代 PDE 证明。原子存在/排除、终端唯一性适用性、G 与一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "LITERATURE RECONSTRUCTION: under the additional assumption that the same fixed periodic NS parent has a positive terminal energy atom, BP/BQ reconstruct a common adjoint, weak-zero terminal trace, atomic localization, Cauchy saturation, and the full tail of the final retained discrete chain. This is not every continuous-time pair or the whole original catalogue. SECOND-ORDER OBSTRUCTION: a fixed descendant has divergent second-order action and positive enstrophy-production part on disjoint late time cells, but first-order energy does not pay second-order cost, so there is no contradiction. BUDGET STRENGTH AUDIT: BR separately proves that finiteness of the full unit-initial-data delayed operator budget for one pair, for every pair, and smooth continuation of the same parent across T are equivalent. Its finiteness is not proved, and the equivalence is not extended to weak solutions, forcing, or full space. FINITE CHECKS ONLY: five text sources, 57 BP/BQ/BR labels, 125/125 file bindings, 31 exact arithmetic checks, and three limited negative controls do not replace PDE proof. Atom existence/exclusion, terminal-uniqueness applicability, G, and general regularity remain OPEN. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["Tao 周期局部理论 1108.1165v4", "Tao periodic local theory 1108.1165v4"],
  ["共同伴随与算子出口：结构保留，预算等价于延拓", "Common adjoint and operator exit: retained structure, budget equivalent to continuation"],
  ["研究笔记总索引 · v2.63 · 2026-09-06", "Research-note master index · v2.63 · 2026-09-06"],
  ["CB.1–CB.19 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.19 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
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
  assert.equal(rows.length, translations.size, "CommonAdjointScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.19"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "CommonAdjointScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-CommonAdjointScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
