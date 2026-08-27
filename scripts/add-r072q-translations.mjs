import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const defaultRoot = resolve(import.meta.dirname, "..");
const root = resolve(process.env.R072Q_RELEASE_ROOT ?? defaultRoot);
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r072q-missing.json");
const checkOnly = process.argv.includes("--check-only");

const englishByChinese = new Map();
const row = (zh, en) => englishByChinese.set(zh, en);

row("固定 \\(M\\)、任意相位与 \\(Q_2\\le1/2\\) 下，恰有两个临界点，实际 shear 的 shape 常数为 \\((\\pi/12,81,36)\\)；1:2 caustic 给出尖锐半径 \\(1/4\\)。", "For fixed \\(M\\), arbitrary phases, and \\(Q_2\\le1/2\\), there are exactly two critical points; the physical shear has shape constants \\((\\pi/12,81,36)\\), and the 1:2 caustic gives the sharp radius \\(1/4\\).");
row("提供 Laurent-polynomial caustic 的代数几何背景，但不直接给出本站实 1:2 coefficient plane 的 nephroid 参数式、phase-uniform disk 或 ED corollary。", "provides the algebraic-geometric background for Laurent-polynomial caustics, but does not directly give the nephroid parametrization in the real 1:2 coefficient plane, the phase-uniform disk, or the enhanced-dissipation corollary used here.");
row("为单个非退化时变 shear 提供 modewise enhanced dissipation。R0.72Q 通过固定 critical boxes、统一 Hessian margin 与 fixed-\\(M\\) derivative ledger，从 proof 中抽取声明 family 的一致常数；这不是原论文逐字陈述的 arbitrary-phase family theorem。", "provides modewise enhanced dissipation for a single nondegenerate time-dependent shear. R0.72Q uses fixed critical boxes, a uniform Hessian margin, and the fixed-\\(M\\) derivative ledger to extract constants uniform over the stated family from the proof; this arbitrary-phase family theorem is not stated verbatim in the paper.");
row("研究受控 1:2:3 caustic 或逼近退化墙的 profile，定位 uniform shape contract 的新边界。", "Study a controlled 1:2:3 caustic or profiles approaching the degeneracy wall to locate a new boundary of the uniform shape contract.");
row("正结果只覆盖固定 \\(M\\)、dominant first harmonic 与 \\(Q_2\\le1/2\\)。正式 physical shape 常数为 \\((\\pi/12,81,36)\\)，归一化 \\(F\\) 的 away 常数 \\(12\\) 不可直接替代。增长 \\(M\\)、任意 time-dependent phases、无 jet dominance、跨越 caustic 的 profile、fixed-\\(R\\) arbitrary coupling 与一般三维问题仍开放；限定检索不构成新颖性或优先权证明。", "The positive result covers only fixed \\(M\\), a dominant first harmonic, and \\(Q_2\\le1/2\\). The formal physical shape constants are \\((\\pi/12,81,36)\\); the normalized profile \\(F\\) has away constant \\(12\\), which cannot be substituted directly. Growing \\(M\\), arbitrary time-dependent phases, the absence of jet dominance, profiles crossing the caustic, arbitrary coupling at fixed \\(R\\), and the general three-dimensional problem remain open; the bounded search establishes neither novelty nor priority.");
row("R0.72Q 的任意相位 shape theorem 与 caustic 文献边界", "Literature boundary for the R0.72Q arbitrary-phase shape theorem and caustic");
row("\\(F\\) 的局部 Hessian margin 大于 \\(1/3\\)。乘回 \\(W=e^{-y}F\\) 后，在 \\(0\\le y\\le1\\) 使用 \\(e^{-1}>1/3\\)，得到局部 slope 下界 \\(1/9\\) 与 away 下界 \\(1/36\\)。正式 ED 调用使用 \\(C_1=36\\)，不能把归一化常数 \\(12\\) 直接代入物理 shear。", "The local Hessian margin of \\(F\\) exceeds \\(1/3\\). After restoring \\(W=e^{-y}F\\), the interval \\(0\\le y\\le1\\) allows the bound \\(e^{-1}>1/3\\), giving the local slope lower bound \\(1/9\\) and the away lower bound \\(1/36\\). The formal enhanced-dissipation invocation uses \\(C_1=36\\); the normalized constant \\(12\\) cannot be substituted directly for the physical shear.");
row("02 · 临界点计数", "02 · Critical-point count");
row("04 · fixed-M 账本", "04 · Fixed-M ledger");
row("06 · 精确 caustic", "06 · Exact caustic");
row("07 · 墙分类", "07 · Wall classification");
row("08 · 独立证书", "08 · Independent certificate");
row("14 · 复现入口", "14 · Reproduction entry points");
row("版本 v0.72Q · 2026-08-28", "Version v0.72Q · 2026-08-28");
row("半群输入来自一手文献，任意相位 family uniformity 是本站的 proof-level 抽取", "Primary literature supplies the semigroup input; arbitrary-phase family uniformity is a proof-level extraction made here");
row("报告、独立审计、精确证书与正式附图包", "Report, independent audit, exact certificates, and formal figure package");
row("边界符号、严格单调与全局排除共同给出恰好两个临界点", "Boundary signs, strict monotonicity, and global exclusion together give exactly two critical points");
row("常数只依赖固定 \\(M\\) 与声明的 upper shape class，不依赖相位、\\(R\\)、\\(\\varepsilon\\) 或初值。", "The constants depend only on fixed \\(M\\) and the stated upper shape class, not on the phases, \\(R\\), \\(\\varepsilon\\), or the initial datum.");
row("从 \\(Q_2\\le1/2\\) 逐项得到 \\(Q_1\\le1/4\\) 与 \\(Q_0\\le1/8\\)；推导没有使用同相或反相结构。", "From \\(Q_2\\le1/2\\), termwise estimates give \\(Q_1\\le1/4\\) and \\(Q_0\\le1/8\\); the derivation uses no in-phase or antiphase structure.");
row("对 \\(W=e^{-y}F\\)、\\(0\\le y\\le1\\)，取 \\(r=\\pi/12\\)、\\(C_0=81\\)、\\(C_1=36\\)。", "For \\(W=e^{-y}F\\) on \\(0\\le y\\le1\\), take \\(r=\\pi/12\\), \\(C_0=81\\), and \\(C_1=36\\).");
row("对固定有限 \\(M\\)，任意相对相位与 \\(Q_2=\\sum_{m=2}^M m^2b_m\\le1/2\\)，归一化 profile 恰有两个临界点。实际 Coble shear 在 \\(0\\le y\\le1\\) 上具有 \\((r,\\mathfrak C_0,\\mathfrak C_1)=(\\pi/12,81,36)\\) 的统一 shape contract；归一化 \\(F\\) 保留更尖锐的 away 常数 \\(12\\)。1:2 退化集由精确 nephroid 参数式给出，phase-uniform 安全圆盘半径恰为 \\(1/4\\)。", "For fixed finite \\(M\\), arbitrary relative phases, and \\(Q_2=\\sum_{m=2}^M m^2b_m\\le1/2\\), the normalized profile has exactly two critical points. On \\(0\\le y\\le1\\), the physical Coble shear has the uniform shape contract \\((r,\\mathfrak C_0,\\mathfrak C_1)=(\\pi/12,81,36)\\), while normalized \\(F\\) retains the sharper away constant \\(12\\). The 1:2 degeneracy set has an exact nephroid parametrization, and the phase-uniform safe disk has radius exactly \\(1/4\\).");
row("固定 \\(M\\) 的任意相位 shape gate 已闭合；", "The arbitrary-phase shape gate for fixed \\(M\\) is closed;");
row("固定 \\(M\\) 与 \\(Q_2\\le1/2\\) 是真实边界，不是排版备注", "Fixed \\(M\\) and \\(Q_2\\le1/2\\) are genuine boundaries, not typographical qualifications");
row("固定 \\(M<\\infty\\)，所有 relative phases 任意，且 \\(Q_2\\le1/2\\)。", "Fix \\(M<\\infty\\), allow every relative phase, and assume \\(Q_2\\le1/2\\).");
row("固定 M 任意相位的统一 Morse shape contract 与 phase-uniform 半径 1/4。", "A uniform Morse shape contract for fixed M and arbitrary phases, with phase-uniform radius 1/4.");
row("归一化常数与实际 Coble shear 常数分账", "Separate the normalized constants from the physical Coble-shear constants");
row("结论仍止于 \\(Q_2\\le1/2\\) 的主谐波锥", "the conclusion still stops at the dominant-harmonic cone \\(Q_2\\le1/2\\)");
row("精确比较 \\(\\sin(\\pi/12)>1/4\\) 保证两个固定盒子的边界符号。盒内由 \\(|F_y''|\\ge\\cos(\\pi/12)-Q_2>0\\) 得严格单调；任一临界点又满足 \\(|\\sin\\phi|\\le Q_1\\le1/4\\)，因此盒外没有遗漏。", "The exact comparison \\(\\sin(\\pi/12)>1/4\\) fixes the boundary signs of the two boxes. The bound \\(|F_y''|\\ge\\cos(\\pi/12)-Q_2>0\\) gives strict monotonicity inside them; every critical point also obeys \\(|\\sin\\phi|\\le Q_1\\le1/4\\), so none can lie outside.");
row("两路独立重建 jet budget、radical comparisons、slow threshold 与 caustic ledger；comparator 要求 canonical payload 精确相等。正式 hash builder 拒绝临时 crosscheck、脏 source lineage、缺件、多件与 symlink。", "The two routes independently reconstruct the jet budget, radical comparisons, slow threshold, and caustic ledger; the comparator requires exact equality of the canonical payloads. The formal hash builder rejects a temporary crosscheck, dirty source lineage, missing or extra artifacts, and symlinks.");
row("临界点", "Critical points");
row("临界点各自在 \\(0\\) 与 \\(\\pi\\) 的 \\(\\pi/12\\) 邻域内，数量恰为二。", "There are exactly two critical points, located respectively near \\(0\\) and \\(\\pi\\), each within radius \\(\\pi/12\\).");
row("没有闭合增长 \\(M\\)、跨越 caustic 的 profile、任意 time-dependent phases、无 dominant first harmonic 的有限 pattern、fixed-\\(R\\) arbitrary coupling、一般三维 continuation、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。", "This section does not close growing \\(M\\), profiles crossing the caustic, arbitrary time-dependent phases, finite patterns without a dominant first harmonic, arbitrary coupling at fixed \\(R\\), general three-dimensional continuation, finite-time singularity, or global smoothness. The Clay Millennium Problem remains unsolved.");
row("其半径范围为 \\([1/4,1/2]\\)。因此 \\(|z|<1/4\\) 内所有相位都非退化且恰有两个临界点；半径 \\(1/4\\) 对 phase-uniform 圆盘是尖锐的。", "Its radial range is \\([1/4,1/2]\\). Thus every phase in \\(|z|<1/4\\) is nondegenerate and has exactly two critical points; the radius \\(1/4\\) is sharp for a phase-uniform disk.");
row("前三阶导数与 slow-time 门槛明确依赖固定 \\(M\\)", "The first three derivative bounds and the slow-time threshold depend explicitly on fixed \\(M\\)");
row("墙", "Wall");
row("墙上一般点满足 \\(f^{(3)}=-3\\sin\\phi\\ne0\\)，属于 \\(A_2\\) fold；\\(z=\\pm1/4\\) 的实轴端点满足三阶消失而四阶非零，属于 \\(A_3\\) cusp。这里没有证明 enhanced dissipation 在墙上失败。", "A generic wall point satisfies \\(f^{(3)}=-3\\sin\\phi\\ne0\\) and is an \\(A_2\\) fold; the real-axis endpoints \\(z=\\pm1/4\\) have vanishing third derivative and nonzero fourth derivative and are \\(A_3\\) cusps. This does not prove failure of enhanced dissipation on the wall.");
row("全局平移只固定第一谐波，其余相位无需对齐", "A global translation fixes only the first harmonic; the remaining phases need not align");
row("提供 caustic 的 Laurent-polynomial 语境。两者都不逐字陈述本站固定 \\(M\\)、\\(Q_2\\le1/2\\)、任意相位与 1:2 实系数 nephroid 的组合定理。", "provides the Laurent-polynomial context for caustics. Neither source states verbatim the combined theorem used here for fixed \\(M\\), \\(Q_2\\le1/2\\), arbitrary phases, and the real-coefficient 1:2 nephroid.");
row("提供时变非退化 shear 的 enhanced-dissipation 框架；", "provides the enhanced-dissipation framework for time-dependent nondegenerate shears;");
row("退化墙是一条精确 nephroid，而不是数值扫描曲线", "The degeneracy wall is an exact nephroid, not a numerically scanned curve");
row("下一节将研究受控的 1:2:3 caustic 或逼近退化墙的 profile，检验 uniform shape contract 在非主谐波锥中的首个失效或可延拓机制。", "The next section will study a controlled 1:2:3 caustic or profiles approaching the degeneracy wall, testing the first failure or continuation mechanism for the uniform shape contract outside the dominant-harmonic cone.");
row("相位限制被移除，但有限 carrier ceiling 与二阶矩小量仍是定理条件", "The phase restriction is removed, but a finite carrier ceiling and a small second moment remain theorem hypotheses");
row("研究笔记 R0.72Q · ARBITRARY PHASES · EXACT CAUSTIC", "Research note R0.72Q · ARBITRARY PHASES · EXACT CAUSTIC");
row("研究笔记 R0.72Q：固定 M、任意相位与 Q2≤1/2 下的两临界点 shape gate，以及精确 1:2 caustic。", "Research note R0.72Q: the two-critical-point shape gate for fixed M, arbitrary phases, and Q2≤1/2, together with the exact 1:2 caustic.");
row("一般墙点是 fold，实轴端点是 cusp；二者都只标记 Morse 适用性", "Generic wall points are folds and the real-axis endpoints are cusps; both mark only Morse applicability");
row("因此常数可对每个固定 \\(M\\) 的 compact shape class 统一，但没有得到 \\(M\\to\\infty\\) 的一致定理。", "The constants are therefore uniform on each compact shape class with fixed \\(M\\), but no theorem uniform as \\(M\\to\\infty\\) is obtained.");
row("增长 \\(M\\)、无 jet dominance、任意时变相位与一般 carrier 集仍开放。", "Growing \\(M\\), the absence of jet dominance, arbitrary time-dependent phases, and general carrier sets remain open.");
row("这是从特殊两载波相位线到相位鲁棒有限模式锥的实质扩张", "This is a substantive extension from a special two-carrier phase line to a phase-robust finite-mode cone");
row("正式附图区分任意相位安全锥、物理 shape 常数与精确 caustic", "The formal figure separates the arbitrary-phase safe cone, physical shape constants, and exact caustic");
row("状态 · R0.72Q 任意相位固定 M 正类完成", "Status · the arbitrary-phase fixed-M R0.72Q positive class is complete");
row("Coble–He 的 profile-by-profile 定理结合上述固定邻域、cutoffs 与 shape bounds，给固定 \\(M\\) 类的 proof-level uniform corollary；紧 \\(\\eta\\) 区间仍由精确 \\(L^2\\) 收缩补齐。", "The Coble–He profile-by-profile theorem, combined with the fixed neighborhoods, cutoffs, and shape bounds above, gives a proof-level uniform corollary for the fixed-\\(M\\) class; the compact \\(\\eta\\) range is still completed by exact \\(L^2\\) contraction.");
row("Python Fraction 与 JavaScript BigInt 双路只核验有限代数骨架", "The Python Fraction and JavaScript BigInt routes audit only the finite algebraic spine");
row("R0.72P 的完整传播结论扩展到声明的任意相位锥", "The full-propagation conclusion of R0.72P extends to the stated arbitrary-phase cone");
row("R0.72Q 移除了 R0.72P 的 real-collinear-phase 限制，并把临界点计数、uniform shape 与适用边界变成可审计的系数空间几何。它提高了机制类结果的稳健性，但仍不是一般三维稳定阈值。", "R0.72Q removes the real-collinear-phase restriction of R0.72P and turns critical-point counting, uniform shape, and the applicability boundary into auditable coefficient-space geometry. This makes the mechanism-class result more robust, but it is still not a general three-dimensional stability threshold.");
row("R0.72Q｜任意相位 shape gate 与精确 caustic", "R0.72Q｜Arbitrary-phase shape gate and exact caustic");
row("R0.72R：离开 dominant-first-harmonic cone", "R0.72R: leave the dominant-first-harmonic cone");
row("保留 R0.72P 历史回顾", "Retain the historical R0.72P recap");
row("二十八个阶段、107 个节点：从约化递推到固定 M 任意相位 shape gate。", "Twenty-eight phases and 107 nodes: from reduced recurrences to the fixed-M arbitrary-phase shape gate.");
row("相位鲁棒的有限模式锥已闭合，一般 superposition 仍远未完成", "A phase-robust finite-mode cone is closed; general superposition remains far from complete");
row("新的严格增量是 fixed-\\(M\\)、arbitrary-phase、\\(Q_2\\le1/2\\) 的 uniform shape gate，以及精确 1:2 caustic。", "The new rigorous increment is the uniform shape gate for fixed \\(M\\), arbitrary phases, and \\(Q_2\\le1/2\\), together with the exact 1:2 caustic.");
row("研究受控 1:2:3 caustic 或逼近退化墙的 profile，定位 uniform shape contract 的首个新边界。", "Study a controlled 1:2:3 caustic or profiles approaching the degeneracy wall to locate the first new boundary of the uniform shape contract.");
row("R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72Q 的 107 个节点；最新一节闭合固定 M 任意相位 shape gate。", "Research recap after R0.60: complete coverage of the 107 nodes from R0.61 through R0.72Q; the latest section closes the fixed-M arbitrary-phase shape gate.");
row("R0.72L–N 保留 actual ledger 并排除声明一载波上的 action-poor route；R0.72O 完成物理回填，R0.72P 在 fixed real-collinear-phase 1:2 正类上关闭完整传播门。", "R0.72L–N retain the actual ledger and exclude the action-poor route on the stated one-carrier class; R0.72O completes physical reinsertion, and R0.72P closes the full propagation gate on the fixed real-collinear-phase 1:2 positive class.");
row("R0.72L–R0.72Q · strong-coupling、物理回填与相位鲁棒 shape gate", "R0.72L–R0.72Q · strong coupling, physical reinsertion, and the phase-robust shape gate");
row("R0.72Q 的 fixed-\\(M\\) arbitrary-phase theorem：\\(Q_2\\le1/2\\) 保证恰有两个临界点，物理 shear 的正式 shape 常数为 \\((\\pi/12,81,36)\\)；1:2 caustic 给出尖锐 phase-uniform disk 半径 \\(1/4\\)。", "The R0.72Q fixed-\\(M\\) arbitrary-phase theorem: \\(Q_2\\le1/2\\) guarantees exactly two critical points, the physical shear has formal shape constants \\((\\pi/12,81,36)\\), and the 1:2 caustic gives the sharp phase-uniform disk radius \\(1/4\\).");
row("R0.72Q 再把相位限制移除：对固定 \\(M\\)、任意相位与 \\(Q_2\\le1/2\\)，恰有两个临界点，实际 Coble shear 可取 \\((\\pi/12,81,36)\\)；1:2 caustic 给出尖锐 phase-uniform 半径 \\(1/4\\)。增长 \\(M\\) 与一般 carrier 集仍开放。", "R0.72Q then removes the phase restriction: for fixed \\(M\\), arbitrary phases, and \\(Q_2\\le1/2\\), there are exactly two critical points and the physical Coble shear admits \\((\\pi/12,81,36)\\); the 1:2 caustic gives the sharp phase-uniform radius \\(1/4\\). Growing \\(M\\) and general carrier sets remain open.");
row("R0.72Q 只覆盖固定 \\(M\\)、任意相位、\\(Q_2\\le1/2\\) 的 dominant-first-harmonic cone。增长 \\(M\\)、一般 carrier 集和 Clay 正式问题保持开放。", "R0.72Q covers only the dominant-first-harmonic cone with fixed \\(M\\), arbitrary phases, and \\(Q_2\\le1/2\\). Growing \\(M\\), general carrier sets, and the formal Clay problem remain open.");
row("R0.72R 离开 dominant-first-harmonic cone", "R0.72R leaves the dominant-first-harmonic cone");
row("1:2 退化集是精确 nephroid \\(z(\\phi)=\\frac18e^{-3i\\phi}-\\frac38e^{-i\\phi}\\)，phase-uniform 安全圆盘半径恰为 \\(1/4\\)。", "The 1:2 degeneracy set is the exact nephroid \\(z(\\phi)=\\frac18e^{-3i\\phi}-\\frac38e^{-i\\phi}\\), and the phase-uniform safe disk has radius exactly \\(1/4\\).");
row("固定 \\(M\\) 的任意相位 Morse shape gate 已经闭合", "The arbitrary-phase Morse shape gate for fixed \\(M\\) is closed");
row("固定 \\(M\\) 与 jet dominance 不能删除；caustic 只标记 Morse applicability，不是 ED 失败。", "Fixed \\(M\\) and jet dominance cannot be removed; the caustic marks only Morse applicability, not failure of enhanced dissipation.");
row("累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72Q 的完整逐节点索引。R0.72Q 对固定 \\(M\\)、任意相位与 \\(Q_2\\le1/2\\) 证明 uniform shape gate，并给出精确 1:2 caustic。", "The cumulative recap retains twenty-eight problem phases and gives a complete node-by-node index through R0.72Q. R0.72Q proves the uniform shape gate for fixed \\(M\\), arbitrary phases, and \\(Q_2\\le1/2\\), and gives the exact 1:2 caustic.");
row("离开 dominant-first-harmonic cone。", "Leave the dominant-first-harmonic cone.");
row("上次综述 v1.29 · 2026-08-27", "Previous review v1.29 · 2026-08-27");
row("相位鲁棒有限模式锥已闭合；增长 \\(M\\)、一般 carrier 集与一般三维问题仍开放。", "The phase-robust finite-mode cone is closed; growing \\(M\\), general carrier sets, and the general three-dimensional problem remain open.");
row("研究受控的 1:2:3 caustic 或逼近退化墙的 profile，定位 uniform shape contract 的首个新边界。", "Study a controlled 1:2:3 caustic or profiles approaching the degeneracy wall to locate the first new boundary of the uniform shape contract.");
row("在 \\(Q_2\\le1/2\\) 下，所有 relative phases 都允许；临界点恰有两个，实际 Coble shear 可取 \\((r,C_0,C_1)=(\\pi/12,81,36)\\)。", "Under \\(Q_2\\le1/2\\), every relative phase is allowed; there are exactly two critical points, and the physical Coble shear admits \\((r,C_0,C_1)=(\\pi/12,81,36)\\).");
row("R0.72Q 已闭合 fixed-M arbitrary-phase、Q2≤1/2 的 shape gate；下一关是离开 dominant-first-harmonic cone。", "R0.72Q closes the fixed-M arbitrary-phase shape gate under Q2≤1/2; the next gate leaves the dominant-first-harmonic cone.");
row("开放接口 · R0.72R", "Open interface · R0.72R");
row("文献综述 v1.30 · 2026-08-28", "Literature review v1.30 · 2026-08-28");
row("我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72Q 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72Q on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.");
row("R0.72Q 的主张边界", "R0.72Q claim boundary");
row("02 · 107 节完整索引", "02 · Complete index of 107 notes");
row("查看 R0.72Q 精确证书", "View the exact R0.72Q certificates");
row("打开最新节点 R0.72Q", "Open the latest node R0.72Q");
row("回顾截止节点：R0.72Q", "Recap cutoff node: R0.72Q");
row("回顾截止时公开笔记：167", "Public notes at the recap cutoff: 167");
row("截至 R0.72Q，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 107 个节点或 69 个公开版本解释成 Clay 问题完成比例。", "Through R0.72Q there is no general three-dimensional continuation criterion and no proof of finite-time breakdown or global smoothness; 107 nodes or 69 public releases cannot be interpreted as a completion percentage for the Clay problem.");
row("累计回顾 · R0.61–R0.72Q · 2026-08-28", "Cumulative recap · R0.61–R0.72Q · 2026-08-28");
row("收录节点：107", "Included nodes: 107");
row("这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72Q 的 107 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。", "This page follows the phase recap for R0.00–R0.60 and organizes R0.61 through R0.72Q into 107 research nodes. I record chronologically what each segment actually proves, which proposals are excluded by concrete counterexamples or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the type of evidence and does not misstate release archiving as completion of a phase objective.");
row("R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 107 个节点沿着这个缺口推进；R0.70A–R0.72Q 的 69 个版本已经公开；其中 45 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。", "The material from R0.00–R0.60 remains in the previous phase recap. The conclusion at R0.60 is that the complete Fourier–Leray structure and higher-order computations can continue, but the critical quantity for general three-dimensional solutions is not yet controlled. The subsequent 107 nodes advance along this gap; 69 releases from R0.70A through R0.72Q are public, and 45 satisfy the current formal-figure complete-archive contract, while still including conditional theorems, counterexamples, finite diagnostics, and open gaps.");
row("R0.61–R0.72Q 的 107 节公开笔记", "The 107 public notes from R0.61 through R0.72Q");
row("R0.61–R0.72Q 回顾 · 2026-08-28", "R0.61–R0.72Q recap · 2026-08-28");
row("R0.61–R0.72Q 研究节点", "R0.61–R0.72Q research nodes");
row("R0.61–R0.72Q｜R0.60 之后的研究回顾", "R0.61–R0.72Q｜Research recap after R0.60");
row("R0.70A–R0.72Q 的 69 节已公开；45 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。", "Sixty-nine releases from R0.70A through R0.72Q are public; 45 are fully sealed under the current formal-figure contract, while 24 legacy archives still require backfill.");
row("R0.70A–R0.72Q 已公开版本", "Published releases from R0.70A through R0.72Q");
row("R0.72Q 附图", "R0.72Q figure");
row("R0.72Q 证书", "R0.72Q certificates");
row("累计回顾 R0.61–R0.72Q · 2026-08-28", "Cumulative recap R0.61–R0.72Q · 2026-08-28");
row("下一步 R0.72R：", "Next R0.72R:");
row("研究笔记 R0.72Q · 2026-08-28", "Research note R0.72Q · 2026-08-28");
row("阅读 R0.72Q 研究笔记 →", "Read research note R0.72Q →");
row("展开 77 篇公开笔记", "Expand 77 public research notes");
row("综述 v1.30 · 2026-08-28", "Review v1.30 · 2026-08-28");
row("R0.60 recap 之后的累计回顾收录 107 个节点；全站现有 167 篇公开研究笔记", "The cumulative recap after R0.60 contains 107 nodes; the site now has 167 public research notes");
row("R0.70A–R0.72Q 共 69 个版本已公开；45 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。", "A total of 69 releases from R0.70A through R0.72Q are public; 45 are fully archived under the current formal-figure contract, while 24 legacy figure packages remain on the backfill list.");
row("R0.70A–R0.72Q：69 节已公开，45 节完整封存", "R0.70A–R0.72Q: 69 published, 45 fully archived");

for (const relative of [
  "literature-review.html",
  "notes/r0-72q.html",
  "recap-r0-61-r0-72q.html",
  "research-review.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.30')) {
    throw new Error(relative + ": expected i18n cache version v1.30");
  }
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r072q\d+$/.test(entry.id));
const byChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (byChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72Q batch");
}
const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !byChinese.has(entry.zh));
const expectedFiles = [
  "literature-review.html",
  "notes/r0-72q.html",
  "recap-r0-61-r0-72q.html",
  "research-review.html",
];
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(expectedFiles)) {
  throw new Error("Unexpected R0.72Q missing-string files: " + JSON.stringify(missingFiles));
}

const expectedSnapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
const snapshot = missing.map(({ zh, count, files }) => ({ zh, count, files }));
if (JSON.stringify(expectedSnapshot) !== JSON.stringify(snapshot)) {
  throw new Error("R0.72Q missing-string snapshot is stale");
}

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh);
  if (!en) throw new Error("Missing explicit R0.72Q English row for: " + entry.zh);
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Invalid R0.72Q English row for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("First-person plural English is forbidden for: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("Protected-token mismatch for:\n" + entry.zh + "\n" + en);
  }
  return { ...entry, id: "r072q" + String(index + 1).padStart(3, "0"), en };
});
if (translatedEntries.length !== 109) {
  throw new Error(`Expected 109 R0.72Q English rows, found ${translatedEntries.length}`);
}

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  const values = finalTranslations.map((entry) => entry[field]);
  if (new Set(values).size !== values.length) {
    throw new Error("Duplicate final translation " + field);
  }
}

if (checkOnly) {
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.72Q translations/en.json batch is stale");
  }
} else {
  await writeFile(translationPath, JSON.stringify(finalTranslations, null, 2) + "\n");
}

console.log(JSON.stringify({
  checkOnly,
  added: translatedEntries.length,
  total: finalTranslations.length,
  liveStrings: source.length,
  missingBefore: missing.length,
  missingAfter: 0,
  files: missingFiles,
}));
