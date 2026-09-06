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
const prefix = "claybrecentsourcescreen20260906";

const translations = new Map([
  ["本章有限读取", "This chapter makes a limited reading of"],
  ["的紧支撑乘子核论证与 (2.3)–(2.5)，只作热核和频率局部化背景；该文预先假定的统一临界范数控制没有导入当前周期能量框架。另读取", "for its compactly supported multiplier-kernel argument and (2.3)–(2.5), solely as background for heat kernels and frequency localization. The uniform critical-norm control assumed there is not imported into the present periodic energy framework. I also read"],
  ["的摘要、引言、§2 设置、Definition 2.1、Theorem 2.2 与 §3 开头，并渲染核对 PDF 第 6–10 页。其全空间条件 (C)、Newton 势压力规范、中心一致上确界与左连续性没有从本站假设推出；§3 后续、§4 和主证明未完整读取，也不声称期刊版逐字相同或完成新颖性检索。", "for its abstract, introduction, §2 setting, Definition 2.1, Theorem 2.2, and the opening of §3, with PDF pages 6–10 rendered and checked visually. Its whole-space condition (C), Newton-potential pressure normalization, center-uniform supremum, and left continuity are not derived from this site's assumptions. The rest of §3, §4, and the main proof were not read in full, and no claim is made that the journal text is word-for-word identical or that a novelty search is complete."],
  ["文献综述 v2.57 · 2026-09-06", "Literature review v2.57 · 2026-09-06"],
  ["阅读完整 CB.13 笔记", "Read the complete CB.13 note"],
  ["CB.13 · Clay-B 近期源筛查的文献和主张边界", "CB.13 · Literature and claim boundary for the Clay-B recent-source screen"],
  ["CB.13 · ClayB-RecentSourceScreen-20260906 公开边界", "CB.13 · Public boundary for ClayB-RecentSourceScreen-20260906"],
  ["PROVED LOCALLY：BC 证明近期源 R 的窗口积分 H¹ 能量趋零，并定位足以与 BB 条件必要下界冲突的 Q_J；Q_J 仍未证。METHOD SCREEN：BD 保留完整源、Leray 投影、散度和时间顺序，证明普通逐块热核/Young 路线留下 N¹ᐟ² 或 N⁹ᐟ⁸ 正频率权重；其标量集中例不是 NS 反例，也不排除带符号方法。CONDITIONAL COMPARISON：BE 以静态有界背景复制旧压力支付指数，得到另一条件必要下界；R 不等同静态高通，p(P_>N u) 不等同 P_>N p，且没有上界。FINITE CHECKS ONLY：七份文本源、57 个公式编号、65/65 文件哈希、29 项有理算术与负向变异不替代证明。OPEN：Q_J、近期源净压力功上界、真实 NS 输入、移动缩球 G 与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。", "PROVED LOCALLY: BC proves that the recent source R has vanishing window-integrated H¹ energy and identifies Q_J as sufficient to conflict with BB's conditional necessary lower bound; Q_J remains unproved. METHOD SCREEN: BD retains the complete source, Leray projection, divergence, and time order, and proves that the ordinary blockwise heat-kernel/Young route leaves positive N¹ᐟ² or N⁹ᐟ⁸ frequency weights. Its scalar concentration example is not an NS counterexample and does not exclude signed methods. CONDITIONAL COMPARISON: BE uses a static bounded background to reproduce the old-pressure payment exponents and obtains another conditional necessary lower bound. R is not the static high pass, p(P_>N u) is not P_>N p, and no upper bound is obtained. FINITE CHECKS ONLY: seven text sources, 57 formula labels, 65/65 file hashes, 29 rational calculations, and negative mutations do not replace proof. OPEN: Q_J, the recent-source net pressure-work upper bound, actual NS inputs, moving shrinking G, and general regularity. No complete novelty review, external peer review, or Clay claim is made, and there is no figure, simulation, or cumulative recap. NOT CLAY."],
  ["近期源的能量与频率成本", "Energy and frequency costs of the recent source"],
  ["研究笔记总索引 · v2.57 · 2026-09-06", "Research-note master index · v2.57 · 2026-09-06"],
  ["CB.1–CB.13 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.13 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
  ["近期源 R 的积分 H¹ 能量确实趋零，但原压力测试所需的 Q_J 平方时间集中仍未证。逐频带热核/Young 路线留下正频率矩；静态背景复制旧压力支付指数，却不等同热余量或给出上界。本轮停止这条具体 norm 路线，Q_J、带符号上界与 G 仍 OPEN。NOT CLAY.", "The integrated H¹ energy of the recent source R does vanish, but the Q_J squared temporal concentration required by the original pressure test remains unproved. The frequency-by-frequency heat-kernel/Young route leaves a positive frequency moment; a static background reproduces the old-pressure payment exponents but is neither the heat remainder nor an upper bound. This specific norm route stops here, while Q_J, the signed upper bound, and G remain OPEN. NOT CLAY."],
  ["近期源方法筛查已进入 CB.13", "The recent-source method screen now forms CB.13"],
  ["绝对值/Young 路线停止", "Absolute-value/Young route stops"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.13 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.13 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategy change is not drawn as a theorem-level implication from R0.76L to Clay-B. Historical nodes show only their stage judgments by default, and the latest public notes open directly."],
  ["下一研发问题：单侧压力判据实际用了什么机制", "Next research question: what mechanism does the one-sided pressure criterion actually use?"],
  ["有限读取 Seregin–Šverák 原证明所需段落，区分条件 (C)、全空间压力规范与当前周期能量。若只重述附加假设或重复开放量，就停止该候选，不包装成新准则。", "Read the necessary portions of the original Seregin–Šverák proof within a bounded scope, separating condition (C), the whole-space pressure normalization, and present periodic energy. If the candidate merely restates extra assumptions or repeats open quantities, stop it instead of packaging it as a new criterion."],
  ["阅读最新 CB.13 近期源筛查笔记 →", "Read the latest CB.13 recent-source-screen note →"],
  ["综述 v2.57 · 2026-09-06", "Review v2.57 · 2026-09-06"],
  ["BC 证明实际 R 的窗口积分 H¹ 能量趋零，并把能与 BB 必要下界冲突的充分量定位为 Q_J；现有能量没有证明 Q_J，直接三角界反而留下带 L₃ 的四次耗散成本。", "BC proves that the actual R has vanishing window-integrated H¹ energy and identifies Q_J as sufficient to conflict with BB's necessary lower bound. Existing energy does not prove Q_J; the direct triangle bound instead leaves a quartic dissipation cost weighted by L₃."],
  ["BC–BE 已区分积分能量小量、原测试所需平方时间集中、逐块正频率矩与静态背景来源比较；结果见下一个正式路线节点。", "BC–BE now separate integrated energy smallness, the squared temporal concentration required by the original test, blockwise positive frequency moments, and the static-background source comparison; the result appears in the next formal route node."],
  ["BD 的完整逐块热核/Young 检查留下 N¹ᐟ² 或 N⁹ᐟ⁸ 正频率权重；BE 的静态有界背景可复制旧压力支付指数，却不等同热余量 R 与静态高通，也不提供源自压力上界。", "BD's complete blockwise heat-kernel/Young check leaves positive N¹ᐟ² or N⁹ᐟ⁸ frequency weights. BE's static bounded background can reproduce the old-pressure payment exponents, but it identifies neither the heat remainder R with the static high pass nor supplies a source-pressure upper bound."],
  ["CB.1–CB.13 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.13 record the internal research order of this independent route. The numbers do not occupy the R0 main sequence or change its R0.76L endpoint."],
  ["CB.12 旧压力已付 → BC 近期源能量基线与 Q_J → BD 逐块正频率矩未付 → BE 静态背景来源比较 → norm 路线停止 → 单侧压力原文机制对照 OPEN", "CB.12 old pressure paid → BC recent-source energy baseline and Q_J → BD unpaid blockwise positive frequency moment → BE static-background source comparison → norm route stops → original one-sided pressure mechanism comparison OPEN"],
  ["CB.13：近期源筛查", "CB.13: recent-source screen"],
  ["CB.13｜近期源的能量与频率成本", "CB.13 | Energy and frequency costs of the recent source"],
  ["CB.14 只是下一章占位，不是已完成研究。Q_J、近期源带符号净压力功上界、条件 (C) 的周期兼容机制、实际 NS 生成 R.216–R.217、移动缩球 G/G-P/G-C 与首次奇点排除均未冻结。", "CB.14 is only a placeholder for the next chapter, not completed research. Q_J, the signed recent-source net pressure-work upper bound, a periodic-compatible mechanism for condition (C), actual NS generation of R.216–R.217, moving shrinking G/G-P/G-C, and first-singularity exclusion are not frozen."],
  ["Clay-B 独立路线停在 CB.13", "The independent Clay-B route stops at CB.13"],
  ["Clay-B 近期源筛查笔记快捷入口", "Clay-B recent-source-screen note shortcuts"],
  ["Clay-B 近期源筛查结论", "Clay-B recent-source-screen result boundary"],
  ["Clay-B 已完成近期源的一轮有限方法筛查：R 的积分 H¹ 能量趋零，但原测试所需 Q_J 未证；逐块绝对值/Young 路线留下正频率矩，静态背景只复制旧压力支付指数。该 norm 路线停止，带符号上界、缩球路径和合同 G 继续开放。", "Clay-B has completed a bounded method screen of the recent source: R has vanishing integrated H¹ energy, but Q_J required by the original test remains unproved. The blockwise absolute-value/Young route leaves a positive frequency moment, and the static background only reproduces the old-pressure payment exponents. This norm route stops, while the signed upper bound, shrinking path, and contract G remain open."],
  ["Q_J、带符号上界与 G OPEN · NOT CLAY", "Q_J, the signed upper bound, and G OPEN · NOT CLAY"],
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
  assert.equal(rows.length, translations.size, "RecentSourceScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.13"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "RecentSourceScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-RecentSourceScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
