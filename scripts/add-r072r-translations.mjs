import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const defaultRoot = resolve(import.meta.dirname, "..");
const root = resolve(process.env.R072R_RELEASE_ROOT ?? defaultRoot);
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r072r-missing.json");
const checkOnly = process.argv.includes("--check-only");

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r072r\d+$/.test(entry.id));
const byChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (byChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72R batch");
}

const englishByChinese = new Map();
const row = (zh, en) => englishByChinese.set(zh, en);

row("打开 108 节完整索引", "Open the complete 108-note index");
row("给出 \\(A\\cos\\phi+B\\sin\\phi+g(\\phi)\\) 的一般 caustic 公式和 generic cusp geometry。R0.72R 的严格增量只是在 fixed-first-harmonic 四实维切片中给出一个显式 rational compact core，以及可支持热路径 ED 的统一 margins。", "gives the general caustic formula for \\(A\\cos\\phi+B\\sin\\phi+g(\\phi)\\) and generic cusp geometry. The rigorous R0.72R increment is only an explicit rational compact core in the fixed-first-harmonic four-real-dimensional slice, together with uniform margins that support enhanced dissipation along the heat path.");
row("给出 stationary degenerate critical points 的较慢 ED benchmarks；它们不等价于非自治 caustic crossing theorem，也说明 caustic 不是 ED 失败墙。", "give slower enhanced-dissipation benchmarks for stationary degenerate critical points. They are not a nonautonomous caustic-crossing theorem, and they also show that a caustic is not a wall of enhanced-dissipation failure.");
row("开放接口 · R0.72S", "Open interface · R0.72S");
row("累计回顾与 108 节索引", "Cumulative recap and 108-note index");
row("提供时变非退化 shear 的 semigroup input；polydisc、共同 shape constants 与 heat-path ledger 是本站供给的 family-uniform inputs。", "provides the semigroup input for time-dependent nondegenerate shears; the polydisc, common shape constants, and heat-path ledger are the family-uniform inputs supplied here.");
row("文献综述 · 资料截止 2026-08-28", "Literature review · Sources checked through 2026-08-28");
row("文献综述 v1.31 · 2026-08-28", "Literature review v1.31 · 2026-08-28");
row("我把已发表定理列为已知结果，2026 年预印本单独标记，本站 R0.69P–R0.72R 只列为研究笔记。我不把计算或笔记外推成正则性定理。", "I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72R on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.");
row("显式 rational polydisc 整体满足 \\(Q_2(0)\\ge14/25>1/2\\)，却沿热路径保持两个临界点与物理 shape constants \\((\\pi/48,144,240)\\)；旧锥 crossing 不是 caustic。", "The explicit rational polydisc satisfies \\(Q_2(0)\\ge14/25>1/2\\) throughout, yet retains two critical points and physical shape constants \\((\\pi/48,144,240)\\) along the heat path; crossing the old cone boundary is not a caustic.");
row("研究 univariate Laurent polynomial 的 caustic 与 Morse discriminant；complex discriminant 不能替代本站的 real self-inversive unit-circle incidence。", "studies the caustic and Morse discriminant of a univariate Laurent polynomial; a complex discriminant cannot replace the real self-inversive unit-circle incidence used here.");
row("已研究实三角多项式 maximal-real-critical regions 的拓扑，degree three 的这类区域并非本站新发现。", "already studies the topology of maximal-real-critical regions for real trigonometric polynomials; such a degree-three region is not a new discovery of this site.");
row("在明确紧系数盒上分离 generic \\(A_2\\)、\\(A_3\\) 与更高余维 strata，并研究逼近或穿越指定 wall 的热路径。", "Separate generic \\(A_2\\), \\(A_3\\), and higher-codimension strata on a declared compact coefficient box, then study a heat path approaching or crossing a specified wall.");
row("证明的是 \\(K\\subset\\mathbb C^2\\cong\\mathbb R^4\\) 位于一个 nondegenerate complement component 内的 compact core；complement component 本身是开集，不能把 \\(K\\) 称为完整紧致胞腔。没有完成整个四维 caustic 的 \\(A_2/A_3\\) stratification、全部 component count、\\(K\\) 的最大性或 wall-crossing ED。限定一手检索没有定位到该精确 polydisc 与全热路径定量组合，但不构成新颖性或优先权证明。", "The proved object is a compact core \\(K\\subset\\mathbb C^2\\cong\\mathbb R^4\\) inside one nondegenerate complement component. The complement component itself is open, so \\(K\\) must not be called a complete compact chamber. The full four-dimensional \\(A_2/A_3\\) stratification, all component counts, maximality of \\(K\\), and wall-crossing enhanced dissipation are not established. The bounded primary-source search did not locate this exact polydisc and full-heat-path quantitative package, but it establishes neither novelty nor priority.");
row("资料截止：2026-08-28。若后续论文状态、版本或官方判断发生变化，我会在此页更新并保留原来的证据标签。", "Sources checked through 2026-08-28. If publication status, versions, or official assessments change, I will update this page while preserving the original evidence labels.");
row("R0.72R 的四实维安全核与 caustic 文献边界", "Literature boundary for the R0.72R four-real-dimensional safe core and caustic");
row("R0.72R 的主张边界", "R0.72R claim boundary");

row("01 · 四实维安全核", "01 · Four-real-dimensional safe core");
row("02 · 旧锥 crossing", "02 · Old-cone crossing");
row("03 · 临界点计数", "03 · Critical-point count");
row("07 · 实系数切片", "07 · Real-coefficient slice");
row("安全核", "Safe core");
row("安全核是四实维 polydisc，不是一条相位线", "The safe core is a four-real-dimensional polydisc, not a phase line");
row("版本 v0.72R · 2026-08-28", "Version v0.72R · 2026-08-28");
row("报告、文献边界、独立审计、精确证书与正式附图包", "Report, literature boundary, independent audit, exact certificates, and formal figure package");
row("常数对 \\((z_2,z_3)\\in K\\)、\\(R\\)、\\(\\varepsilon_c\\) 和 row datum 一致，但依赖声明的 fixed-pattern reduction。", "The constants are uniform in \\((z_2,z_3)\\in K\\), \\(R\\), \\(\\varepsilon_c\\), and the row datum, subject to the stated fixed-pattern reduction.");
row("若第三 carrier 被计为 active，物理比较仍需固定 \\(|z_3|\\ge\\beta_->0\\)；没有 \\(\\beta_-\\downarrow0\\) 的一致性。", "If the third carrier is counted as active, the physical comparison still requires a fixed floor \\(|z_3|\\ge\\beta_->0\\); no uniformity as \\(\\beta_-\\downarrow0\\) is claimed.");
row("代数判别式必须再施加 unit-circle 可实现区间", "The algebraic discriminant must still be restricted to the unit-circle realizability interval");
row("等价地，若 \\(u=e^{i\\phi}\\)，则实 caustic 满足存在 \\(|u|=1\\) 使 \\(D(u)=D'(u)=0\\)。沿 incidence，\\(f'''=3(5B-\\sin\\phi)\\)、\\(f''''=3(15A-\\cos\\phi)\\)。这些公式给出墙的可审计坐标，但没有完成其 self-intersections、singular strata 或 complement components 的全局分类。", "Equivalently, with \\(u=e^{i\\phi}\\), the real caustic is characterized by the existence of \\(|u|=1\\) such that \\(D(u)=D'(u)=0\\). Along the incidence, \\(f'''=3(5B-\\sin\\phi)\\) and \\(f''''=3(15A-\\cos\\phi)\\). These formulas give auditable wall coordinates but do not globally classify its self-intersections, singular strata, or complement components.");
row("对 Clay 问题的直接价值仍低：第一谐波归一化、有限 commensurate pattern、affine-row invariance、triangular 2.5D reduction 与非退化 critical-point 条件仍远离任意三维初值。", "The direct value for the Clay problem remains low: first-harmonic normalization, a finite commensurate pattern, affine-row invariance, the triangular 2.5D reduction, and nondegenerate critical-point hypotheses remain far from arbitrary three-dimensional data.");
row("给出 \\(A\\cos\\phi+B\\sin\\phi+g(\\phi)\\) 的一般 caustic 公式和 generic cusp geometry；", "gives the general caustic formula for \\(A\\cos\\phi+B\\sin\\phi+g(\\phi)\\) and generic cusp geometry;");
row("给出 Laurent-polynomial Morse discriminant 的复代数背景；", "gives the complex-algebraic background for the Laurent-polynomial Morse discriminant;");
row("给出时变非退化 shear 的半群输入。限定一手检索没有定位到这里的精确 rational polydisc、全热路径 margins 与 family-uniform ED corollary 的组合陈述；这不构成新颖性或优先权证明。", "provides the semigroup input for time-dependent nondegenerate shears. The bounded primary-source search did not locate a combined statement of the exact rational polydisc, full-heat-path margins, and family-uniform enhanced-dissipation corollary used here; this establishes neither novelty nor priority.");
row("归一化 profile 的临界 tube 内有 Hessian 下界 \\(1/4\\)，tube 外有 away-gradient 下界 \\(1/80\\)。乘回 \\(e^{-y}\\) 后使用 \\(e^{-1}>1/3\\)，得到正式物理常数；它们没有被外推到 \\(y\\to\\infty\\)。", "The normalized profile has Hessian lower bound \\(1/4\\) inside the critical tubes and away-gradient lower bound \\(1/80\\) outside. Restoring \\(e^{-y}\\) and using \\(e^{-1}>1/3\\) gives the formal physical constants; they are not extrapolated to \\(y\\to\\infty\\).");
row("紧致 polydisc \\(K\\subset\\mathbb C^2\\cong\\mathbb R^4\\) 有非空内部，并整体位于 R0.72Q 的 \\(Q_2\\le1/2\\) 锥外。", "The compact polydisc \\(K\\subset\\mathbb C^2\\cong\\mathbb R^4\\) has nonempty interior and lies entirely outside the R0.72Q cone \\(Q_2\\le1/2\\).");
row("旧加权锥不是 caustic；", "The old weighted cone is not the caustic;");
row("旧条件是充分锥，不是退化墙", "The old condition is a sufficient cone, not the degeneracy wall");
row("旧锥 crossing", "Old-cone crossing");
row("两路独立重建 cone-exit margin、perturbation budgets、shape margins、slow-time identity、incidence identities 与 real-slice factorization；comparator 要求 canonical payload 精确相等。证书不替代连续单调性证明、Coble–He 定理或完整 caustic decomposition。", "The two routes independently reconstruct the cone-exit margin, perturbation budgets, shape margins, slow-time identity, incidence identities, and real-slice factorization; the comparator requires exact equality of the canonical payloads. The certificate does not replace the continuum monotonicity proof, the Coble–He theorem, or a complete caustic decomposition.");
row("没有分类整个四维 caustic、全部 complement components 或 wall-crossing dynamics。", "The full four-dimensional caustic, all complement components, and wall-crossing dynamics are not classified.");
row("没有证明整个 \\(\\mathbb C^2\\cong\\mathbb R^4\\) coefficient space 的 caustic stratification、全部临界点计数胞腔、\\(K\\) 的最大性、穿越 \\(A_2/A_3\\) 墙的非自治 ED、任意时变相位、增长 carrier ceiling、一般三维 continuation、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。", "This section does not prove the caustic stratification of the full \\(\\mathbb C^2\\cong\\mathbb R^4\\) coefficient space, every critical-point-count chamber, maximality of \\(K\\), nonautonomous enhanced dissipation through an \\(A_2/A_3\\) wall, arbitrary time-dependent phases, a growing carrier ceiling, general three-dimensional continuation, finite-time singularity, or global smoothness. The Clay Millennium Problem remains unsolved.");
row("每个初值严格越过旧锥，随后只穿过充分条件边界", "Every initial profile lies strictly beyond the old cone and later crosses only a sufficient-condition boundary");
row("每条声明热路径始终只有两个临界点；在 \\(0\\le y\\le1\\) 取 \\((r,C_0,C_1)=(\\pi/48,144,240)\\)。", "Every stated heat path retains exactly two critical points; on \\(0\\le y\\le1\\), take \\((r,C_0,C_1)=(\\pi/48,144,240)\\).");
row("实 caustic 包含两条 endpoint lines，以及 \\(a^2=3b(1-3b)\\) 上 \\(1/15\\le b\\le1/3\\) 的 internal arc。遗漏这个区间会把 unit circle 外的重复根误报为真实退化墙；本节也不把这张二维切片冒充四维分类。", "The real caustic contains two endpoint lines and the internal arc on \\(a^2=3b(1-3b)\\) with \\(1/15\\le b\\le1/3\\). Omitting this interval falsely reports a repeated root outside the unit circle as a real degeneracy wall; this two-dimensional slice is also not presented as a four-dimensional classification.");
row("实切片", "Real slice");
row("四个空间导数上界可取 \\(1161/1000,1323/1000,1649/1000,2307/1000\\)，其和小于 \\(161/25\\)。slow-reference 充分门槛为 \\(\\eta\\le(3/7)^4=81/2401\\)；完整阈值仍包含 Coble–He proof dependency \\(\\eta_{\\rm CH}\\)。", "The four spatial-derivative bounds may be taken as \\(1161/1000,1323/1000,1649/1000,2307/1000\\), with sum below \\(161/25\\). A sufficient slow-reference threshold is \\(\\eta\\le(3/7)^4=81/2401\\); the complete threshold still contains the Coble–He proof dependency \\(\\eta_{\\rm CH}\\).");
row("四维墙由实 unit-circle incidence 表达，而非复判别式替代", "The four-dimensional wall is expressed by real unit-circle incidence, not replaced by a complex discriminant");
row("完整 1:2:3 affine row 保留全部交叉项", "The complete 1:2:3 affine row retains every cross term");
row("完整 1:2:3 affine-row propagator 在 \\(K\\) 上具有 coefficient-uniform enhanced dissipation。", "The complete 1:2:3 affine-row propagator has coefficient-uniform enhanced dissipation on \\(K\\).");
row("下一节先在一个明确紧系数盒上分离 generic \\(A_2\\)、\\(A_3\\) 与更高余维 strata，再构造逼近或穿越其中一个 stratum 的热路径；完整全局 chamber 分类继续单列，除非获得完备 semialgebraic certificate。", "The next section will first separate generic \\(A_2\\), \\(A_3\\), and higher-codimension strata on a declared compact coefficient box, then construct a heat path approaching or crossing one such stratum. A complete global chamber classification remains separate unless a complete semialgebraic certificate is obtained.");
row("沿归一化热路径，\\(Q_2(y)=4|z_2|e^{-3y}+9|z_3|e^{-8y}\\) 严格下降，且 \\(Q_2(1)<20489/256000<1/2\\)。所以每条路径恰穿过旧边界一次，而临界点仍统一非退化；这次 crossing 不是 caustic。", "Along the normalized heat path, \\(Q_2(y)=4|z_2|e^{-3y}+9|z_3|e^{-8y}\\) decreases strictly and \\(Q_2(1)<20489/256000<1/2\\). Thus every path crosses the old boundary exactly once while its critical points remain uniformly nondegenerate; this crossing is not a caustic.");
row("研究笔记 R0.72R · FOUR-REAL-DIMENSIONAL CORE · BEYOND THE OLD CONE", "Research note R0.72R · FOUR-REAL-DIMENSIONAL CORE · BEYOND THE OLD CONE");
row("研究笔记 R0.72R：旧加权锥外的显式四实维 caustic-free core、统一 shape contract 与完整 1:2:3 enhanced dissipation。", "Research note R0.72R: an explicit four-real-dimensional caustic-free core beyond the old weighted cone, a uniform shape contract, and complete 1:2:3 enhanced dissipation.");
row("一个四实维紧致安全核已经越过它", "a four-real-dimensional compact safe core crosses it");
row("一个整体越过 Q2≤1/2 旧充分锥的显式 polydisc，仍沿热路径保持两个临界点。", "An explicit polydisc lying entirely beyond the old sufficient cone Q2≤1/2 still retains two critical points along the heat path.");
row("已研究 maximal-real-critical degree-three regions 的拓扑。存在 degree-three chamber 不是本站的新发现。", "already studies the topology of maximal-real-critical degree-three regions. The existence of a degree-three chamber is not a new discovery of this site.");
row("以 \\(F_y^0=\\cos\\phi+(3/20)e^{-3y}\\cos2\\phi\\) 为中心，扰动满足", "With \\(F_y^0=\\cos\\phi+(3/20)e^{-3y}\\cos2\\phi\\) as the center, the perturbation satisfies");
row("在 complex 1:2:3 coefficient space 中，显式 polydisc \\(K=\\{|z_2-3/20|\\le1/100,\\ |z_3|\\le1/1000\\}\\) 的全部初始 profile 都满足 \\(Q_2(0)\\ge14/25>1/2\\)，却沿整个声明热路径始终恰有两个临界点。实际 shear 在 \\(0\\le y\\le1\\) 具有统一 \\((r,\\mathfrak C_0,\\mathfrak C_1)=(\\pi/48,144,240)\\)，并给出系数一致的 full-superposition enhanced-dissipation corollary。", "In the complex 1:2:3 coefficient space, every initial profile in the explicit polydisc \\(K=\\{|z_2-3/20|\\le1/100,\\ |z_3|\\le1/1000\\}\\) satisfies \\(Q_2(0)\\ge14/25>1/2\\), yet retains exactly two critical points along the entire stated heat path. On \\(0\\le y\\le1\\), the physical shear has the uniform contract \\((r,\\mathfrak C_0,\\mathfrak C_1)=(\\pi/48,144,240)\\), yielding a coefficient-uniform full-superposition enhanced-dissipation corollary.");
row("这里第一谐波已由平移与归一化固定；\\((z_2,z_3)\\) 仍保留四个真实自由度。安全结论覆盖整个紧致集合，而不是有限样点。", "The first harmonic is fixed here by translation and normalization, while \\((z_2,z_3)\\) retains four real degrees of freedom. The safe conclusion covers the entire compact set, not finitely many samples.");
row("这是从 phase-uniform 内锥到显式非锥安全核的严格扩张", "This is a rigorous extension from a phase-uniform inner cone to an explicit safe core outside that cone");
row("正式附图区分旧充分锥、四维安全核与真实 caustic", "The formal figure separates the old sufficient cone, the four-dimensional safe core, and the true caustic");
row("中心 slope 写成 \\(-(\\sin\\phi)(1+4c(y)\\cos\\phi)\\)，第二因子至少为 \\(2/5\\)。在 \\(\\ell=\\pi/48\\) 的边界，保留精确正 margin \\(3047/1536000\\)；大盒内严格单调，盒外由 slope 排除。因此临界点恰有两个，分别落在 \\(0\\) 与 \\(\\pi\\) 的 \\(\\pi/48\\) 邻域。", "The central slope factors as \\(-(\\sin\\phi)(1+4c(y)\\cos\\phi)\\), and the second factor is at least \\(2/5\\). On the boundary \\(\\ell=\\pi/48\\), the exact positive margin \\(3047/1536000\\) remains; strict monotonicity holds in the larger boxes and the slope excludes the exterior. Thus there are exactly two critical points, lying respectively near \\(0\\) and \\(\\pi\\), each within \\(\\pi/48\\).");
row("中心因式分解与小扰动预算给出全局计数", "Central factorization and the small-perturbation budget give the global count");
row("状态 · R0.72R 四实维 caustic-free core 完成", "Status · the R0.72R four-real-dimensional caustic-free core is complete");
row("Arnol'd 已给一般 caustic 与 degree-three chamber 拓扑；本站只主张定量安全核", "Arnol'd already gives the general caustic and degree-three chamber topology; this site claims only a quantitative safe core");
row("caustic-free compact core 不等于完整四维 caustic classification", "A caustic-free compact core is not a complete four-dimensional caustic classification");
row("Python rational 与 JavaScript BigInt 双路核验有限代数骨架", "The Python rational and JavaScript BigInt routes audit the finite algebraic spine");
row("R0.72R 第一次给出整体处于旧 jet-safety cone 外、却具有统一 root localization、shape margins、heat-path ledger 与完整传播推论的四实维系数集。它可作为特殊 triangular mechanism 论文中的定量 lemma，也为逼近真实 caustic 提供有证书的起点。", "R0.72R first gives a four-real-dimensional coefficient set lying entirely outside the old jet-safety cone while retaining uniform root localization, shape margins, a heat-path ledger, and the complete propagation corollary. It can serve as a quantitative lemma in a paper on the special triangular mechanism and as a certified starting point for approaching the true caustic.");
row("R0.72R｜旧锥外的四实维 caustic-free core", "R0.72R｜A four-real-dimensional caustic-free core beyond the old cone");
row("R0.72S：从安全核推进到声明的 wall stratum", "R0.72S: advance from the safe core to a declared wall stratum");
row("root localization 被转换成实际 shear 的统一常数", "Root localization is converted into uniform constants for the physical shear");

row("02 · 108 节完整索引", "02 · Complete 108-note index");
row("保留 R0.72Q 历史回顾", "Retain the historical R0.72Q recap");
row("查看 R0.72R 精确证书", "View the exact R0.72R certificates");
row("打开最新节点 R0.72R", "Open the latest node R0.72R");
row("二十八个阶段、108 个节点：从约化递推到旧充分锥外的四实维安全核。", "Twenty-eight phases and 108 nodes: from reduced recurrences to a four-real-dimensional safe core beyond the old sufficient cone.");
row("回顾截止节点：R0.72R", "Recap endpoint: R0.72R");
row("回顾截止时公开笔记：168", "Public notes at recap cutoff: 168");
row("截至 R0.72R，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 108 个节点或 70 个公开版本解释成 Clay 问题完成比例。", "Through R0.72R there is no general three-dimensional continuation criterion and no proof of finite-time breakdown or global smoothness. The 108 nodes or 70 public releases must not be interpreted as a completion percentage for the Clay problem.");
row("旧安全锥已被严格越过，真实 caustic wall 仍是下一道边界", "The old safe cone is rigorously exceeded; the true caustic wall remains the next boundary");
row("累计回顾 · R0.61–R0.72R · 2026-08-28", "Cumulative recap · R0.61–R0.72R · 2026-08-28");
row("每条热路径恰穿过旧 \\(Q_2=1/2\\) 边界一次而不退化。R0.72R 只给一个 caustic-free compact core；完整四维 caustic stratification、wall crossing、任意时变相位与一般三维问题仍开放。", "Every heat path crosses the old \\(Q_2=1/2\\) boundary exactly once without degenerating. R0.72R gives only a caustic-free compact core; the complete four-dimensional caustic stratification, wall crossing, arbitrary time-dependent phases, and the general three-dimensional problem remain open.");
row("收录节点：108", "Nodes included: 108");
row("先在明确紧系数盒上分离 generic \\(A_2\\)、\\(A_3\\) 与更高余维 strata，再研究一条逼近或穿越指定 wall 的热路径。", "First separate generic \\(A_2\\), \\(A_3\\), and higher-codimension strata on a declared compact coefficient box, then study a heat path approaching or crossing a specified wall.");
row("新的严格增量是一个非空四实维紧致系数核：它整体位于 R0.72Q 加权锥外，却有全热路径 root localization、物理 shape contract 和 family-uniform ED。", "The new rigorous increment is a nonempty four-real-dimensional compact coefficient core lying entirely outside the R0.72Q weighted cone while retaining full-heat-path root localization, a physical shape contract, and family-uniform enhanced dissipation.");
row("这页接在 R0.00–R0.60 的阶段回顾之后，整理 R0.61 到 R0.72R 的 108 个研究节点。我按时间记录每一段实际证明了什么、哪条设想被具体反例或尺度分析排除，以及哪些条件还没有从 Navier–Stokes 方程中推出。这里的节点状态描述证据类型，不把版本封存误写成阶段目标已经解决。", "This page follows the R0.00–R0.60 phase recap and organizes the 108 research nodes from R0.61 through R0.72R. I record chronologically what each segment actually proves, which proposal is excluded by a concrete counterexample or scale analysis, and which hypotheses have not been derived from the Navier–Stokes equations. Node status describes the evidence type and does not misstate release sealing as resolution of a phase objective.");
row("R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.60 的结论是：完整 Fourier–Leray 结构与高阶计算可以继续做，但还没有控制一般三维解的临界量。后面的 108 个节点沿着这个缺口推进；R0.70A–R0.72R 的 70 个版本已经公开；其中 46 个满足当前 formal-figure 完整封存合同，但其中仍包含条件定理、反例、有限诊断和开放缺口。", "The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concludes that the full Fourier–Leray structure and higher-order calculations can continue, but the critical quantity of a general three-dimensional solution is not controlled. The following 108 nodes advance along that gap. The 70 releases from R0.70A through R0.72R are public, and 46 satisfy the current formal-figure sealing contract, but they still include conditional theorems, counterexamples, finite diagnostics, and open gaps.");
row("R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72R 的 108 个节点；最新一节闭合旧加权锥外的四实维 caustic-free core。", "Research recap after R0.60: complete coverage of the 108 nodes from R0.61 through R0.72R; the latest section closes a four-real-dimensional caustic-free core beyond the old weighted cone.");
row("R0.61–R0.72R 的 108 节公开笔记", "The 108 public notes from R0.61 through R0.72R");
row("R0.61–R0.72R 回顾 · 2026-08-28", "R0.61–R0.72R recap · 2026-08-28");
row("R0.61–R0.72R 研究节点", "R0.61–R0.72R research nodes");
row("R0.61–R0.72R｜R0.60 之后的研究回顾", "R0.61–R0.72R｜Research recap after R0.60");
row("R0.70A–R0.72R 的 70 节已公开；46 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。", "The 70 releases from R0.70A through R0.72R are public; 46 are fully sealed under the current formal-figure contract, while 24 legacy archives remain in the backfill queue.");
row("R0.70A–R0.72R 已公开版本", "Public releases from R0.70A through R0.72R");
row("R0.72L 保留 actual ledger；R0.72M 给出零扩散 action-poor reference，R0.72N 排除声明耗散一载波链上的该安全分支。R0.72O 完成物理回填，R0.72P 在 fixed real-collinear static-phase 1:2 正类上关闭完整传播门，R0.72Q 再闭合 fixed-\\(M\\) arbitrary-static-phase、\\(Q_2\\le1/2\\) 的 shape gate。", "R0.72L retains the actual ledger; R0.72M gives a zero-diffusion action-poor reference, and R0.72N excludes that safe branch on the stated dissipative one-carrier chain. R0.72O completes physical reinsertion, R0.72P closes the full propagation gate on the fixed real-collinear static-phase 1:2 positive class, and R0.72Q closes the fixed-\\(M\\), arbitrary-static-phase shape gate under \\(Q_2\\le1/2\\).");
row("R0.72L–R0.72R · strong-coupling、物理回填与 caustic-free coefficient geometry", "R0.72L–R0.72R · strong coupling, physical reinsertion, and caustic-free coefficient geometry");
row("R0.72R 的 four-real-dimensional caustic-free core：整个 \\(K\\) 严格位于旧 \\(Q_2\\le1/2\\) 充分锥外，沿声明热路径仍恰有两个临界点；物理 shape constants 为 \\((\\pi/48,144,240)\\)，完整 1:2:3 affine row 得到 coefficient-uniform ED corollary。", "The R0.72R four-real-dimensional caustic-free core: all of \\(K\\) lies strictly outside the old sufficient cone \\(Q_2\\le1/2\\), yet retains exactly two critical points along the stated heat path; the physical shape constants are \\((\\pi/48,144,240)\\), and the complete 1:2:3 affine row has a coefficient-uniform enhanced-dissipation corollary.");
row("R0.72R 附图", "R0.72R figure");
row("R0.72R 证明的是固定 first harmonic、commensurate 1:2:3、triangular affine-row class 中的显式 caustic-free compact core，不是整个 \\(\\mathbb C^2\\) coefficient space 的 chamber classification。caustic crossing、任意时变相位、增长 carrier ceiling 与 Clay 正式问题保持开放。", "R0.72R proves an explicit caustic-free compact core in a fixed-first-harmonic, commensurate 1:2:3 triangular affine-row class, not a chamber classification of the entire \\(\\mathbb C^2\\) coefficient space. Caustic crossing, arbitrary time-dependent phases, a growing carrier ceiling, and the formal Clay problem remain open.");
row("R0.72R 证明该 \\(Q_2\\) 条件只是一条充分锥：显式四实维 polydisc \\(K\\) 整体满足 \\(Q_2(0)\\ge14/25>1/2\\)，却沿每条声明热路径始终恰有两个临界点，并在 \\(0\\le y\\le1\\) 具有物理 shape constants \\((\\pi/48,144,240)\\) 与 coefficient-uniform full-superposition ED。", "R0.72R proves that the \\(Q_2\\) condition is only a sufficient cone: the explicit four-real-dimensional polydisc \\(K\\) satisfies \\(Q_2(0)\\ge14/25>1/2\\) throughout, yet retains exactly two critical points along every stated heat path and, on \\(0\\le y\\le1\\), has physical shape constants \\((\\pi/48,144,240)\\) with coefficient-uniform full-superposition enhanced dissipation.");
row("R0.72R 证书", "R0.72R certificates");
row("R0.72S 从安全核推进到声明的 caustic stratum", "R0.72S advances from the safe core to a declared caustic stratum");

row("从安全核推进到声明的 wall stratum。", "Advance from the safe core to a declared wall stratum.");
row("旧充分锥已被越过；完整四维 caustic stratification、wall crossing 与一般三维问题仍开放。", "The old sufficient cone has been exceeded; the complete four-dimensional caustic stratification, wall crossing, and the general three-dimensional problem remain open.");
row("旧加权锥外的四实维 caustic-free core 已经闭合", "The four-real-dimensional caustic-free core beyond the old weighted cone is closed");
row("累计回顾 R0.61–R0.72R · 2026-08-28", "Cumulative recap R0.61–R0.72R · 2026-08-28");
row("累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72R 的完整逐节点索引。R0.72R 给出旧加权锥外的四实维 caustic-free core、全热路径 root localization、物理 shape contract 与 coefficient-uniform full-superposition ED。", "The cumulative recap retains twenty-eight problem phases and gives a complete node-by-node index through R0.72R. R0.72R gives a four-real-dimensional caustic-free core beyond the old weighted cone, full-heat-path root localization, a physical shape contract, and coefficient-uniform full-superposition enhanced dissipation.");
row("每条路径都恰穿过旧 \\(Q_2=1/2\\) 充分条件边界一次而保持统一非退化。该 crossing 不是 caustic；R0.72R 只证明紧致安全核，不声称完成整个四维 caustic 或胞腔分类。", "Every path crosses the old sufficient-condition boundary \\(Q_2=1/2\\) exactly once while remaining uniformly nondegenerate. The crossing is not a caustic; R0.72R proves only a compact safe core and does not claim a complete four-dimensional caustic or chamber classification.");
row("上次综述 v1.30 · 2026-08-28", "Previous review v1.30 · 2026-08-28");
row("我另做了一页系统综述，把经典理论、五条文献主干、候选爆破排除树、2019—2026 年进展和本站 R0.69P–R0.72R 路线放在同一张图中。R0.61–R0.69O 的历史节点保留在累计回顾里。", "I maintain a separate systematic review placing the classical theory, five literature trunks, the candidate-blow-up exclusion tree, progress from 2019 through 2026, and this site's R0.69P–R0.72R route on one map. The historical R0.61–R0.69O nodes remain in the cumulative recap.");
row("下一步 R0.72S：", "Next R0.72S:");
row("显式 \\(K=\\{|z_2-3/20|\\le1/100,\\ |z_3|\\le1/1000\\}\\) 整体满足 \\(Q_2(0)\\ge14/25\\)，却沿声明热路径始终恰有两个临界点；实际 shear 在 \\(0\\le y\\le1\\) 可取 \\((r,C_0,C_1)=(\\pi/48,144,240)\\)。", "The explicit set \\(K=\\{|z_2-3/20|\\le1/100,\\ |z_3|\\le1/1000\\}\\) satisfies \\(Q_2(0)\\ge14/25\\) throughout, yet retains exactly two critical points along the stated heat path; on \\(0\\le y\\le1\\), the physical shear admits \\((r,C_0,C_1)=(\\pi/48,144,240)\\).");
row("研究笔记 R0.72R · 2026-08-28", "Research note R0.72R · 2026-08-28");
row("阅读 R0.72R 研究笔记 →", "Read research note R0.72R →");
row("在明确紧系数盒上分离 generic A2、A3 与更高余维 strata，并研究一条逼近或穿越指定 wall 的热路径。", "Separate generic A2, A3, and higher-codimension strata on a declared compact coefficient box, then study a heat path approaching or crossing a specified wall.");
row("展开 78 篇公开笔记", "Expand 78 public notes");
row("综述 v1.31 · 2026-08-28", "Review v1.31 · 2026-08-28");
row("family-uniform ED 仍属于固定 commensurate 1:2:3 triangular affine-row class；wall crossing、任意时变相位与一般三维问题未证明。", "Family-uniform enhanced dissipation remains confined to the fixed commensurate 1:2:3 triangular affine-row class; wall crossing, arbitrary time-dependent phases, and the general three-dimensional problem are not proved.");
row("R0.60 recap 之后的累计回顾收录 108 个节点；全站现有 168 篇公开研究笔记", "The cumulative recap after R0.60 contains 108 nodes; the site now has 168 public research notes");
row("R0.70A–R0.72R 共 70 个版本已公开；46 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。", "A total of 70 releases from R0.70A through R0.72R are public; 46 are fully sealed under the current formal-figure contract, while 24 legacy figure archives remain in the backfill queue.");
row("R0.70A–R0.72R：70 节已公开，46 节完整封存", "R0.70A–R0.72R: 70 releases public, 46 fully sealed");
row("R0.72R 严格离开旧加权锥：显式四实维 polydisc 整体满足 \\(Q_2(0)\\ge14/25>1/2\\)，却沿声明热路径保持恰好两个临界点与物理 shape constants \\((\\pi/48,144,240)\\)。每条路径穿过 \\(Q_2=1/2\\) 时仍统一非退化；旧边界因此不是 caustic。这里只证明 caustic-free compact core，不作完整四维 chamber 分类。", "R0.72R rigorously leaves the old weighted cone: the explicit four-real-dimensional polydisc satisfies \\(Q_2(0)\\ge14/25>1/2\\) throughout, yet retains exactly two critical points and physical shape constants \\((\\pi/48,144,240)\\) along the stated heat path. Every path remains uniformly nondegenerate when crossing \\(Q_2=1/2\\), so the old boundary is not the caustic. Only a caustic-free compact core is proved here, not a complete four-dimensional chamber classification.");
row("R0.72R 已闭合旧 Q2≤1/2 锥外的四实维 caustic-free core；下一关是指定 caustic stratum 的逼近或穿越。", "R0.72R closes a four-real-dimensional caustic-free core beyond the old Q2≤1/2 cone; the next gate approaches or crosses a specified caustic stratum.");

for (const relative of [
  "literature-review.html",
  "notes/r0-72r.html",
  "recap-r0-61-r0-72r.html",
  "research-review.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.31')) {
    throw new Error(relative + ": expected i18n cache version v1.31");
  }
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !byChinese.has(entry.zh));
const expectedFiles = [
  "literature-review.html",
  "notes/r0-72r.html",
  "recap-r0-61-r0-72r.html",
  "research-review.html",
];
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(expectedFiles)) {
  throw new Error("Unexpected R0.72R missing-string files: " + JSON.stringify(missingFiles));
}
const expectedSnapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
const snapshot = missing.map(({ zh, count, files }) => ({ zh, count, files }));
if (JSON.stringify(expectedSnapshot) !== JSON.stringify(snapshot)) {
  throw new Error("R0.72R missing-string snapshot is stale");
}

const longRoute = missing.filter(
  (entry) => entry.zh.startsWith("中。R0.69P–R0.71P") && entry.zh.includes("R0.72R 构造整体位于旧加权锥外"),
);
if (longRoute.length !== 1) {
  throw new Error(`Expected one extended R0.72R literature route string, found ${longRoute.length}`);
}
const oldRoute = retained.find((entry) => entry.id === "r072o011");
if (!oldRoute) throw new Error("Missing retained R0.72O literature-route translation");
const routeTail = " General Navier–Stokes regularity remains open.";
if (!oldRoute.en.endsWith(routeTail)) {
  throw new Error("Unexpected retained R0.72O literature-route English tail");
}
englishByChinese.set(
  longRoute[0].zh,
  oldRoute.en.slice(0, -routeTail.length)
    + " R0.72P closes the full propagation gate on the fixed real-collinear static-phase 1:2 positive class. R0.72Q then proves the fixed-\\(M\\), arbitrary-static-phase two-critical-point shape gate under \\(Q_2\\le1/2\\) and gives the exact 1:2 caustic. R0.72R constructs a four-real-dimensional rational polydisc lying entirely outside the old weighted cone and closes full-heat-path root localization, the physical shape contract \\((\\pi/48,144,240)\\), and coefficient-uniform 1:2:3 enhanced dissipation; the complete four-dimensional caustic stratification remains open."
    + routeTail,
);

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh);
  if (!en) throw new Error("Missing explicit R0.72R English row for: " + entry.zh);
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Invalid R0.72R English row for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("First-person plural English is forbidden for: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("Protected-token mismatch for:\n" + entry.zh + "\n" + en);
  }
  return { ...entry, id: "r072r" + String(index + 1).padStart(3, "0"), en };
});
if (translatedEntries.length !== 124) {
  throw new Error(`Expected 124 R0.72R English rows, found ${translatedEntries.length}`);
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
    throw new Error("R0.72R translations/en.json batch is stale");
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
