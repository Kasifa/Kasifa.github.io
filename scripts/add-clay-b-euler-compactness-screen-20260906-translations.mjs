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
const prefix = "claybeulercompactnessscreen20260906";

const translations = new Map([
  ["。周期 Green 修正、短窗紧性与 L^(11/3) 周期无原子端点在本章正文重算。引用工具与存在性结论没有全部重证；没有穷尽文献、完成 Deep Research、新颖性审查或外部同行评审。", ". The periodic Green correction, short-window compactness, and periodic L^(11/3) no-atom endpoint are recomputed in this chapter. The cited tools and existence results are not fully reproved; no exhaustive literature review, completed Deep Research, novelty audit, or external peer review is claimed."],
  ["本轮有界核查", "This bounded review checks"],
  ["的 Euclidean Calderón–Zygmund 工具；", " for the Euclidean Calderón–Zygmund tools;"],
  ["文献综述 v2.61 · 2026-09-06", "Literature review v2.61 · 2026-09-06"],
  ["阅读完整 CB.17 笔记", "Read the complete CB.17 note"],
  ["CB.17 · Clay-B 临界 Euler 紧性的文献和主张边界", "CB.17 · Literature and claim boundary for Clay-B critical Euler compactness"],
  ["CB.17 · ClayB-EulerCompactnessScreen-20260906 公开边界", "CB.17 · Public boundary for ClayB-EulerCompactnessScreen-20260906"],
  ["CONDITIONAL COMPACTNESS：额外局部梯度界与短窗 L³ 下界推出规范压力局部 L^(5/3)、速度强 L³、压力强 L^(3/2) 及非零古老有限能量 Euler 极限；仅在此条件内压力输入冗余。LITERATURE OBSTRUCTION：Gavrilov 已知定常流排除宽目标类全零刚性，但不是固定 NS 历史可达性反例。CONDITIONAL ATOM：同一原解若实现 BL，终端能量原子至少为 ε_*^4/(2V^3)，这不是原子存在证明。KNOWN-METHOD ENDPOINT：额外强 L^(11/3) 排原子；基本能量 L^(10/3) 留下 -3/10 与 -9/20 的负截止幂。FINITE CHECKS ONLY：五份文本源、BK–BN 共 48 个标签、104/104 文件绑定、20 项精确算术检查与 3 项有限负对照不替代 PDE 证明。G、原解输入生成、带符号压力功上界、一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "CONDITIONAL COMPACTNESS: extra local gradient bounds and a short-window L³ lower bound yield local L^(5/3) canonical pressure, strong L³ velocity, strong L^(3/2) pressure, and a nonzero ancient finite-energy Euler limit; pressure is redundant only within these assumptions. LITERATURE OBSTRUCTION: Gavrilov's known steady flow rules out all-zero rigidity for the broad target class but is not a fixed-NS-history attainability counterexample. CONDITIONAL ATOM: if the same source realizes BL, its terminal energy atom is at least ε_*^4/(2V^3); this does not prove atom existence. KNOWN-METHOD ENDPOINT: extra strong L^(11/3) excludes an atom, while energy-level L^(10/3) leaves negative cutoff powers -3/10 and -9/20. FINITE CHECKS ONLY: five text sources, 48 BK–BN labels, 104/104 file bindings, 20 exact arithmetic checks, and three limited negative controls do not replace PDE proof. G, source-input generation, the signed pressure-work upper bound, and general regularity remain OPEN. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["Gavrilov 的紧支撑定常 Euler 流", "Gavrilov's compactly supported steady Euler flow"],
  ["Leslie–Shvydkoy 终端能量测度", "Leslie–Shvydkoy on terminal energy measures"],
  ["Shvydkoy 能量集中条件", "Shvydkoy on energy-concentration conditions"],
  ["临界 Euler 紧性：压力输入、能量原子与无原子端点", "Critical Euler compactness: pressure input, energy atoms, and a no-atom endpoint"],
  ["研究笔记总索引 · v2.61 · 2026-09-06", "Research-note master index · v2.61 · 2026-09-06"],
  ["CB.1–CB.17 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.17 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["· 本章不生成新 PDF", "· no new PDF is generated for this chapter"],
  ["固定中心、原时钟、规范压力、全部截止项与有符号通量；不预设持留宽度，不把嵌套窗口当作互不相交，检查正终端原子是否强迫与有限总耗散不相容的成本。", "Keep the center, original clock, canonical pressure, every cutoff term, and signed flux fixed. Assume no persistence width and do not count nested windows as disjoint; test whether a positive terminal atom forces a cost incompatible with finite total dissipation."],
  ["阶段复评已进入 CB.17", "The stage reassessment has entered CB.17"],
  ["宽 Euler 全零刚性被文献反例排除", "a literature counterexample rules out all-zero rigidity for the broad Euler class"],
  ["来源与主张边界", "sources and claim boundary"],
  ["明确的局部速度预算足以推出规范压力紧性和非零古老有限能量 Euler 极限，但宽 Euler 类已有非零定常反例。同一固定 NS 来源若实现该分支，终端能量原子成为条件必要结论；额外强 L^(11/3) 又给已知无原子端点。基本能量尚未接通两端。G OPEN。NOT CLAY.", "Explicit local velocity budgets suffice for canonical-pressure compactness and a nonzero ancient finite-energy Euler limit, but the broad Euler class already has a nonzero steady counterexample. If one fixed NS source realizes this branch, a terminal energy atom is conditionally necessary; additional strong L^(11/3) gives a known no-atom endpoint. Basic energy has not connected the two ends. G OPEN. NOT CLAY."],
  ["条件内压力输入可删", "pressure input can be removed within the conditional argument"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.17 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.17 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：原子—耗散下界测试", "Next research action: atom–dissipation lower-bound test"],
  ["原解输入生成与一般正则性 OPEN · NOT CLAY", "original-solution input generation and general regularity OPEN · NOT CLAY"],
  ["阅读 CB.17 HTML", "Read CB.17 HTML"],
  ["阅读最新 CB.17 临界紧性笔记 →", "Read the latest CB.17 critical-compactness note →"],
  ["综述 v2.61 · 2026-09-06", "Research review v2.61 · 2026-09-06"],
  ["BK 界定缩放窗口；BL 在额外局部速度假设下推出完整规范压力紧性、全短窗强收敛及非零古老有限能量 Euler 极限，压力不再是独立输入。", "BK identifies the scaling windows. Under extra local velocity hypotheses, BL derives complete canonical-pressure compactness, strong convergence on the full short window, and a nonzero ancient finite-energy Euler limit, so pressure is no longer an independent input."],
  ["BK–BN 已区分条件紧性、文献刚性障碍、原子必要条件与额外强端点；结果见下一个正式路线节点。", "BK–BN distinguish conditional compactness, the literature rigidity obstruction, the necessary atom condition, and the extra strong endpoint. The result is recorded in the next formal route node."],
  ["BM 用 Gavrilov 已知定常流排除宽类全零刚性，并证明固定 NS 来源若实现 BL 就必须产生定量终端能量原子；BN 在额外强 L^(11/3) 下重算已知无原子端点。两端没有由基本能量自动接通。", "BM uses Gavrilov's known steady flow to rule out all-zero rigidity for the broad class and proves that a fixed NS source realizing BL must produce a quantitative terminal energy atom. BN recomputes a known no-atom endpoint under extra strong L^(11/3). Basic energy does not automatically connect the two ends."],
  ["CB.1–CB.17 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.17 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.17｜临界 Euler 紧性：压力输入、能量原子与无原子端点", "CB.17 | Critical Euler compactness: pressure input, energy atoms, and a no-atom endpoint"],
  ["CB.18 只是下一章占位，不是已完成研究。正终端能量原子是否强迫不相容的耗散下界尚未冻结；G、原解输入生成、带符号压力功上界、一般正则性与 Clay 均未关闭。", "CB.18 is only a next-chapter placeholder, not completed research. Whether a positive terminal energy atom forces an incompatible dissipation lower bound is not frozen. G, original-solution input generation, the signed pressure-work upper bound, general regularity, and Clay remain open."],
  ["Clay-B 独立路线停在 CB.17", "The independent Clay-B route stops at CB.17"],
  ["Clay-B 临界 Euler 紧性笔记快捷入口", "Clay-B critical Euler compactness note shortcuts"],
  ["Clay-B 临界紧性筛查结论", "Clay-B critical-compactness screen conclusions"],
  ["Clay-B 已完成临界 Euler 紧性筛查：额外局部速度预算可删去独立压力输入，并导出条件性终端能量原子；但宽 Euler 类全零刚性已被文献反例排除，强 L^(11/3) 无原子端点仍是额外条件。下一步只测试原子与总耗散的关系。", "Clay-B has completed the critical Euler compactness screen. Extra local velocity budgets remove the independent pressure input and yield a conditional terminal energy atom, but a literature counterexample rules out all-zero rigidity for the broad Euler class, while the strong L^(11/3) no-atom endpoint remains an extra condition. The next step tests only the relation between an atom and total dissipation."],
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
  assert.equal(rows.length, translations.size, "EulerCompactnessScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.17"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "EulerCompactnessScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-EulerCompactnessScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
