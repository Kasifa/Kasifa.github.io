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
const prefix = "claybfixedhistoryscreen20260906";

const translations = new Map([
  ["固定窗口与自动倍增上界未得", "fixed-window control and an automatic doubling-lag upper bound remain unavailable"],
  ["汇总浓集、局部平滑、压力功与古老解障碍，只选择真正减少未证输入且有明确全局出口的问题；不重复固定历史预检，也不把 Type I 或量词交换改名为已付条件。", "Consolidate the concentration, local-smoothing, pressure-work, and ancient-solution obstructions, then select only questions that genuinely reduce unpaid inputs and have a clear global exit. Do not repeat the fixed-history precheck or relabel Type I or a quantifier exchange as a paid condition."],
  ["同一固定初值的完整 mild 历史给出增长窗口 S_k=M_k^(1+η) 之外的真实旧尾小性；固定窗口控制仍未支付。在单位常向量条件分支中，中间增长时间段必须保留有符号贡献。record 时间账本只给倍增间隔下界，不自动给上界。G OPEN。NOT CLAY.", "The complete mild history from one fixed initial datum gives genuine old-tail smallness beyond the growing window S_k=M_k^(1+η); fixed-window control remains unpaid. In the conditional unit-constant branch, the intermediate growing-time slab must retain a signed contribution. The record-time ledger gives only a lower doubling-lag bound, not an automatic upper bound. G OPEN. NOT CLAY."],
  ["完整历史与 record 时间账本已进入 CB.16", "The complete history and record-time ledger have entered CB.16"],
  ["我把已经完成的研究整理为两条路线。R0.1–R0.76L 是实线主序列；CB.1–CB.16 是相对独立的 Clay-B 路线，以单独的虚线泳道表示。两者研究同一个 PDE 问题，但这里不把策略转向画成从 R0.76L 推出 Clay-B 的定理依赖。历史节点默认只显示阶段判断，最近公开笔记可直接打开原始记录。", "I organize the completed research into two routes. R0.1–R0.76L is the solid-line main sequence; CB.1–CB.16 is the relatively independent Clay-B route, shown in its own dashed lane. Both study the same PDE problem, but the strategic turn is not drawn here as a theorem-level dependency from R0.76L to Clay-B. Historical nodes show stage judgments by default, and the latest public note opens the underlying record directly."],
  ["下一研发动作：阶段策略复评", "Next research action: stage strategy reassessment"],
  ["阅读最新 CB.16 固定历史笔记 →", "Read the latest CB.16 fixed-history note →"],
  ["增长窗口外尾估计成立", "the tail estimate beyond the growing window holds"],
  ["这不是固定窗口控制。若古老局部极限是单位常向量，中间增长窗口必须保留有符号贡献；BJ 则证明 record 局部寿命只给 D_j 下界，有限总时间不自动给上界。有界子列或 Type I 都是额外输入。", "This is not fixed-window control. If the ancient local limit is a unit constant vector, the intermediate growing window must retain a signed contribution. BJ proves that local record lifetime gives only a lower bound for D_j, while finite total time does not automatically give an upper bound. A bounded subsequence or Type I is additional input."],
  ["综述 v2.60 · 2026-09-06", "Research review v2.60 · 2026-09-06"],
  ["BI 保留同一固定初值的完整周期 mild 历史，证明初始热项趋零，并用原解能量支付 ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k)；因此 S_k=M_k^(1+η) 之外的旧尾趋零。", "BI retains the complete periodic mild history from one fixed initial datum, proves that the initial heat term vanishes, and uses the original solution's energy to pay ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k). The old tail therefore vanishes beyond S_k=M_k^(1+η)."],
  ["BI/BJ 已核对增长窗口旧尾、固定窗口量词及倍增间隔上下界边界；结果见下一个正式路线节点。", "BI/BJ have checked the growing-window old tail, the fixed-window quantifiers, and the boundary between lower and upper doubling-lag bounds. The result is recorded in the next formal route node."],
  ["CB.1–CB.16 记录这条独立路线的内部研发顺序；编号不占用 R0 主序列，也不改变 R0.76L 的端点。", "CB.1–CB.16 record the internal research order of this independent route. Their numbering does not occupy the R0 main sequence or change the R0.76L endpoint."],
  ["CB.15 粗预算反检查 → BI 完整 mild 历史 → 增长窗口外旧尾小性 → 固定窗口量词不可交换 → BJ 倍增时间下界 / 上界缺口 → 阶段策略复评", "CB.15 coarse-budget countercheck → BI complete mild history → old-tail smallness beyond a growing window → fixed-window quantifiers cannot be exchanged → BJ lower doubling-lag bound / upper-bound gap → stage strategy reassessment"],
  ["CB.16：固定初值完整历史", "CB.16: complete fixed-data history"],
  ["CB.16｜固定初值完整历史：增长窗口尾项与时间账本边界", "CB.16 | Complete fixed-data history: growing-window tails and the time-ledger boundary"],
  ["CB.17 只是下一章占位，不是已完成研究。阶段策略复评尚未冻结；固定窗口控制、实际 NS 的 D_j 上界、Type I、非恒定古老解刚性、G/Q、带符号压力功上界、一般正则性与 Clay 均未关闭。", "CB.17 is only the next-chapter placeholder, not completed research. The stage strategy reassessment is not frozen. Fixed-window control, an actual NS upper bound for D_j, Type I, nonconstant ancient rigidity, G/Q, the signed pressure-work upper bound, general regularity, and Clay all remain open."],
  ["Clay-B 独立路线停在 CB.16", "The independent Clay-B route stops at CB.16"],
  ["Clay-B 固定初值完整历史笔记快捷入口", "Clay-B complete fixed-data history note shortcuts"],
  ["Clay-B 固定历史筛查结论", "Clay-B fixed-history screen conclusions"],
  ["Clay-B 已完成固定初值完整历史预检：原解能量支付增长窗口之外的旧非线性尾，但没有固定窗口控制；record 倍增账本只给下界而不自动给上界。下一研发动作转为阶段策略复评，G/Q 与一般正则性继续开放。", "Clay-B has completed the fixed-data complete-history precheck. The original solution's energy pays the old nonlinear tail beyond a growing window, but not fixed-window control; the record-doubling ledger supplies a lower bound but no automatic upper bound. The next research action is a stage strategy reassessment, while G/Q and general regularity remain open."],
  ["Type I、古老解刚性、G/Q OPEN · NOT CLAY", "Type I, ancient rigidity, and G/Q OPEN · NOT CLAY"],
  ["15 页并视觉检查页 2–4。后者 Theorem 1.2 只作未满足输入的对照：同一个全空间 mild 古老解须在一列趋于负无穷的时刻具有统一全空间 L³ 界。不同缩放在各自逃逸左端时刻的周期胞恒等式不满足该量词与域条件。标准外部 PDE 接口没有在此全部重证，也没有穷尽文献、Deep Research、新颖性或外部同行评审声明。", "in all 15 pages and visually checks pages 2–4. Its Theorem 1.2 is used only as an unmet-input comparison: the same whole-space mild ancient solution must have a uniform whole-space L³ bound at a sequence of times tending to minus infinity. Periodic-cell identities for different rescalings at their own escaping left endpoints do not satisfy that quantifier or domain condition. Standard external PDE interfaces are not fully re-proved here, and no exhaustive literature review, Deep Research, novelty review, or external peer review is claimed."],
  ["本轮重读", "This round rereads"],
  ["文献综述 v2.60 · 2026-09-06", "Literature review v2.60 · 2026-09-06"],
  ["阅读完整 CB.16 笔记", "Read the complete CB.16 note"],
  ["CB.16 · Clay-B 固定初值完整历史的文献和主张边界", "CB.16 · Literature and claim boundary for the Clay-B complete fixed-data history"],
  ["CB.16 · ClayB-FixedHistoryScreen-20260906 公开边界", "CB.16 · Public boundary for ClayB-FixedHistoryScreen-20260906"],
  ["PDF 页 6–13、18–20，并视觉检查页 7、10、11、19，用于核对 Stokes 散度源核、mild 表示、局部平滑与峰值紧性接口；另完整读取", "PDF pages 6–13 and 18–20, with visual checks of pages 7, 10, 11, and 19, to verify the Stokes divergence-source kernel, mild representation, local smoothing, and peak-compactness interfaces; it also reads"],
  ["PROVED IN STATED SCOPE：完整周期 mild 历史的初始热项趋零，并有 ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k)；取 S_k=M_k^(1+η)、0<η<1，增长窗口外旧尾趋零。CONDITIONAL：若局部古老极限为单位常向量，固定窗口内近期项趋零，中间增长窗口必须保留该常向量的有符号贡献；若另有有界 D_j 子列则极限非恒定。TIME-LEDGER BOUNDARY：局部寿命给 D_j≥4c_*，有限总时间只给 Σ4^(-j)D_j<∞；标量 d_*+j² 只反检查该推论，不是 NS。Type I 与古老解刚性仍是额外输入。FINITE CHECKS ONLY：四份文本源、52 个 BI/BJ 标签、89/89 文件绑定、23 项精确代数检查和 3 项有限负对照不替代 PDE 证明。OPEN：固定窗口控制、实际 NS 上界、G/Q、一般正则性与 Clay。无图件、仿真、新 PDF 或累计 recap。NOT CLAY。", "PROVED IN STATED SCOPE: the initial heat term in the complete periodic mild history vanishes, and ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k). With S_k=M_k^(1+η) and 0<η<1, the old tail beyond the growing window vanishes. CONDITIONAL: if the ancient local limit is a unit constant vector, the recent term in every fixed window vanishes and the signed intermediate growing-window contribution must retain that constant; if a bounded D_j subsequence is additionally available, the limit is nonconstant. TIME-LEDGER BOUNDARY: local lifetime gives D_j≥4c_*, while finite total time gives only Σ4^(-j)D_j<∞. The scalar family d_*+j² only counterchecks that inference and is not NS. Type I and ancient rigidity remain additional inputs. FINITE CHECKS ONLY: four text sources, 52 BI/BJ labels, 89/89 file bindings, 23 exact algebra checks, and three limited negative controls do not replace PDE proof. OPEN: fixed-window control, an actual NS upper bound, G/Q, general regularity, and Clay. There is no figure, simulation, new PDF, or cumulative recap. NOT CLAY."],
  ["固定初值完整历史：增长窗口尾项与时间账本边界", "Complete fixed-data history: growing-window tails and the time-ledger boundary"],
  ["研究笔记总索引 · v2.60 · 2026-09-06", "Research-note master index · v2.60 · 2026-09-06"],
  ["CB.1–CB.16 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。", "CB.1–CB.16 are independent chapter numbers for the Clay-B route. They do not occupy R0-series numbers or change the current R0.76L endpoint. From ClayB-SignedScale-20260905 onward, new releases generate HTML only; existing PDFs remain unchanged."],
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
  assert.equal(rows.length, translations.size, "FixedHistoryScreen translation count drift");
  for (const row of rows) {
    assert.equal(row.en, translations.get(row.zh), "translation drift: " + row.zh);
    validateTranslation(row.zh, row.en);
  }
  const bundle = await readFile(resolve(publicRoot, "i18n-en.js"), "utf8");
  assert.ok(bundle.includes("The independent Clay-B route stops at CB.16"), "translation bundle drift");
} else {
  const base = current.filter((entry) => !rowPattern.test(entry.id));
  const currentByZh = new Map(base.map((entry) => [entry.zh, entry]));
  const missing = source.filter((entry) => !currentByZh.has(entry.zh));
  assert.equal(missing.length, translations.size, "FixedHistoryScreen source-string count drift");
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
process.stdout.write(JSON.stringify({ release: "ClayB-FixedHistoryScreen-20260906", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: translations.size, applied: !checkOnly }, null, 2) + "\n");
